from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class BoardVolumeConfigTest(unittest.TestCase):
    def test_board_run_defaults_target_raw_256x64_matrix(self):
        makefile = read("Makefile")
        host = read("ps/host.cpp")
        run_sh = read("run.sh")

        self.assertIn("DATA_GRID_ROWS ?= 64", makefile)
        self.assertIn("DATA_ITER ?= 64", makefile)
        self.assertIn("--raw-volume --kind $(DATA_KIND)", makefile)
        self.assertIn("BOARD_GRID_ROWS ?= 64", makefile)
        self.assertIn("BOARD_GRID_DEPTH ?= 1", makefile)
        self.assertIn("BOARD_DATA_ITER ?= 64", makefile)
        self.assertIn("BOARD_DATA_DIR ?= ./board_data", makefile)
        self.assertIn("--package.sd_dir $(BOARD_DATA_DIR)", makefile)

        self.assertIn(
            "constexpr int DEFAULT_ITER = BOARD_GRID_ROWS * BOARD_GRID_DEPTH;",
            host,
        )
        self.assertIn(
            "constexpr int BOARD_OUTPUT_ROWS = BOARD_GRID_ROWS * BOARD_GRID_DEPTH;",
            host,
        )
        self.assertNotIn("BOARD_RAW_ROWS_PER_DEPTH", host)
        self.assertNotIn("board_volume_mode", host)

        self.assertIn("ITER=${2:-64}", run_sh)
        self.assertIn("INPUT_TXT=${3:-./board_data/input.txt}", run_sh)
        self.assertIn("aie_out_1lane_256x64_raw.txt", run_sh)

    def test_toppl_directly_streams_and_stores_every_raw_volume_row(self):
        toppl = read("pl/TopPL.cpp")

        self.assertIn("#define TRI1PLIO_MAX_ITER 64", toppl)
        self.assertIn("#define TRI1PLIO_MAX_DDR_WORDS 1024", toppl)
        self.assertIn("constexpr int kBoardGridRows = 64;", toppl)
        self.assertIn("constexpr int kBoardGridDepth = 1;", toppl)
        self.assertIn(
            "constexpr int kBoardIter = kBoardGridRows * kBoardGridDepth;",
            toppl,
        )
        self.assertNotIn("kBoardRawRowsPerDepth", toppl)
        self.assertNotIn("board_volume_mode", toppl)
        self.assertNotIn("in_plane_r", toppl)
        self.assertIn("out_words.write(input[i]);", toppl)
        self.assertIn("output[i] = in_words.read();", toppl)

    def test_board_path_uses_128_bit_plio(self):
        top_graph = read("aie/TopGraph.h")
        toppl = read("pl/TopPL.cpp")
        gen_case = read("data/gen_case.py")
        convert = read("data/convert.py")

        self.assertIn("plio_128_bits", top_graph)
        self.assertNotIn("plio_64_bits", top_graph)

        self.assertIn("using plio_word_t = ap_uint<128>;", toppl)
        self.assertIn("constexpr int kPlioWordBits = 128;", toppl)
        self.assertIn("constexpr int kIntsPerPlioWord = 4;", toppl)
        self.assertIn(
            "constexpr int kPlioWordsPerDdrWord = kIntsPerDdrWord / kIntsPerPlioWord;",
            toppl,
        )

        self.assertIn("write_plio128_i32", gen_case)
        self.assertNotIn("write_plio64_i32", gen_case)
        self.assertIn("4 int32 per line", gen_case)
        self.assertIn("write_plio128_i32", convert)
        self.assertNotIn("write_plio64_i32", convert)

    def test_toppl_has_four_stage_dataflow_with_axis_registers(self):
        toppl = read("pl/TopPL.cpp")

        self.assertIn("void read_ddr_words(", toppl)
        self.assertIn("void pack_to_plio128(", toppl)
        self.assertIn("void unpack_from_plio128(", toppl)
        self.assertIn("void write_ddr_words(", toppl)
        self.assertIn("#pragma HLS INTERFACE axis port=to_aie register_mode=both", toppl)
        self.assertIn("#pragma HLS INTERFACE axis port=from_aie register_mode=both", toppl)
        self.assertIn("hls::stream<ddr_word_t> input_words;", toppl)
        self.assertIn("hls::stream<ddr_word_t> output_words;", toppl)
        self.assertIn("#pragma HLS STREAM variable=input_words depth=128", toppl)
        self.assertIn("#pragma HLS STREAM variable=output_words depth=128", toppl)

        self.assertRegex(
            toppl,
            r"#pragma HLS DATAFLOW\s+read_ddr_words\(input, total_words, input_words\);\s+"
            r"pack_to_plio128\(input_words, total_words, to_aie\);\s+"
            r"unpack_from_plio128\(from_aie, total_words, output_words\);\s+"
            r"write_ddr_words\(output, total_words, output_words\);",
        )

    def test_host_reports_bounded_pipeline_time(self):
        host = read("ps/host.cpp")

        self.assertIn("constexpr int BOARD_GRID_ROWS = 64;", host)
        self.assertIn("constexpr int BOARD_GRID_DEPTH = 1;", host)
        self.assertIn("constexpr int BOARD_OUTPUT_ROWS = BOARD_GRID_ROWS * BOARD_GRID_DEPTH;", host)
        self.assertIn("topStencil.run(iter_cnt / hdiff_cfg::kRowsPerCall);", host)
        self.assertIn("topStencil.wait();", host)
        self.assertIn("topStencil.end();", host)
        self.assertIn("const long long pl_transfer_us = elapsed_us(pl_t0, pl_t1);", host)
        self.assertIn("const long long aie_run_us = elapsed_us(aie_t0, aie_t1);", host)
        self.assertRegex(
            host,
            r"const auto aie_t0 = Clock::now\(\);\s+"
            r"topStencil\.run\(iter_cnt / hdiff_cfg::kRowsPerCall\);\s+"
            r"const auto pl_t0 = Clock::now\(\);",
        )
        self.assertRegex(
            host,
            r"toppl_run\.wait\(\);\s+"
            r"const auto pl_t1 = Clock::now\(\);\s+"
            r"const long long pl_transfer_us = elapsed_us\(pl_t0, pl_t1\);\s+"
            r"topStencil\.wait\(\);\s+"
            r"const auto aie_t1 = Clock::now\(\);",
        )
        self.assertIn('std::printf("pl_transfer_us : %lld\\n", pl_transfer_us);', host)
        self.assertIn('std::printf("aie_run_us     : %lld\\n", aie_run_us);', host)
        self.assertNotIn("topStencil.run();", host)
        self.assertNotIn("repeat      :", host)
        self.assertNotIn("graph_pipeline_us", host)
        self.assertNotIn("toppl_t0", host)

    def test_aie_input_broadcast_fifo_depths_keep_default_short_run_values(self):
        config = read("aie/Config.h")
        core_graph = read("aie/ProcessGraph/StencilCoreGraph.h")
        xrt_ini = read("xrt.ini")

        self.assertIn("constexpr int kInputObjectFifoDepth = 2;", config)
        self.assertIn("constexpr int kDelayedInputObjectFifoDepth = 2;", config)
        self.assertIn("constexpr int kFluxInterObjectFifoDepth = 2;", config)
        self.assertIn("constexpr int kOutputObjectFifoDepth = 2;", config)
        self.assertIn("fifo_depth(net_in_lap)     = hdiff_cfg::kInputObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_in_flux1)   = hdiff_cfg::kDelayedInputObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_in_flux2)   = hdiff_cfg::kDelayedInputObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_lap_f1)      = hdiff_cfg::kFluxInterObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_lap_f2)      = hdiff_cfg::kFluxInterObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_f1_f2)       = hdiff_cfg::kFluxInterObjectFifoDepth;", core_graph)
        self.assertIn("fifo_depth(net_out)         = hdiff_cfg::kOutputObjectFifoDepth;", core_graph)
        self.assertIn("profile=false", xrt_ini)
        self.assertNotIn("stall_trace=all", xrt_ini)
        self.assertNotIn("aie_profile=true", xrt_ini)
        self.assertNotIn("aie_status=true", xrt_ini)

    def test_aie_kernels_avoid_per_call_constant_arrays_and_unused_state(self):
        lap = read("aie/ProcessUnit/hdiff_lap.cc")
        flux1 = read("aie/ProcessUnit/hdiff_flux1.cc")
        flux2 = read("aie/ProcessUnit/hdiff_flux2.cc")

        for src in (lap, flux1, flux2):
            self.assertNotIn("#define kernel_load", src)

        self.assertIn("static const int32_t kCoeffNeg4Raw[8]", lap)
        self.assertIn("static const int32_t kCoeffNeg1Raw[8]", lap)
        self.assertIn("const v8int32 coeff_neg4 = *(const v8int32*)kCoeffNeg4Raw;", lap)
        self.assertIn("const v8int32 coeff_neg1 = *(const v8int32*)kCoeffNeg1Raw;", lap)
        self.assertNotIn("static const v8int32 kCoeffNeg4", lap)
        self.assertNotIn("static const v8int32 kCoeffNeg1", lap)
        self.assertNotIn("alignas(32) int32_t weights", lap)
        self.assertNotIn("alignas(32) int32_t weights_rest", lap)

        self.assertIn("static const std::int32_t kCoeffOneRaw[8]", flux2)
        self.assertIn("static const std::int32_t kCoeffNeg7Raw[8]", flux2)
        self.assertIn("const v8int32 coeff_one = *(const v8int32*)kCoeffOneRaw;", flux2)
        self.assertIn("const v8int32 coeff_neg7 = *(const v8int32*)kCoeffNeg7Raw;", flux2)
        self.assertNotIn("static const v8int32 kCoeffOne", flux2)
        self.assertNotIn("static const v8int32 kCoeffNeg7", flux2)
        self.assertNotIn("alignas(32) std::int32_t weights1", flux2)
        self.assertNotIn("alignas(32) std::int32_t flux_out_arr", flux2)
        self.assertNotIn("v8int32* __restrict ptr_out = nullptr;", flux2)


if __name__ == "__main__":
    unittest.main()

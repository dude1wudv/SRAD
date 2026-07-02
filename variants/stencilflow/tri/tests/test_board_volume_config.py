from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


TRI_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (TRI_ROOT / relative_path).read_text(encoding="utf-8")


class TriBoardVolumeConfigTest(unittest.TestCase):
    def test_make_all_builds_256x256x64_board_data(self):
        makefile = read_text("Makefile")

        self.assertIn("BOARD_GRID_ROWS ?= 256", makefile)
        self.assertIn("BOARD_GRID_DEPTH ?= 64", makefile)
        self.assertIn("BOARD_DATA_ITER ?= 16384", makefile)
        self.assertIsNotNone(
            re.search(r"^all:\s+board_data aie kernels xsa host package$", makefile, re.M)
        )
        self.assertIn("--package.sd_dir $(BOARD_DATA_DIR)", makefile)
        self.assertIsNotNone(re.search(r"^\$\(HOST\):", makefile, re.M))
        self.assertIsNotNone(re.search(r"^host:\s+\$\(HOST\)$", makefile, re.M))

    def test_aie_graph_uses_current_single_input_128_bit_plio_semantics(self):
        top_graph = read_text("aie/TopGraph.h")
        stencil_graph = read_text("aie/ProcessGraph/StencilCoreGraph.h")
        config = read_text("aie/Config.h")

        self.assertIn("plio_128_bits", top_graph)
        self.assertIn("input_plio  in_plio[1];", top_graph)
        self.assertIn("output_plio out_plio[1];", top_graph)
        self.assertIn("connect<>(in_plio[0].out[0], core.in);", top_graph)
        self.assertIn("connect<>(core.out, out_plio[0].in[0]);", top_graph)
        self.assertIn("port<input>  in;", stencil_graph)
        self.assertIn("port<output> out;", stencil_graph)
        self.assertIn("connect(in, k_lap.in[0])", stencil_graph)
        self.assertIn("connect(in, k_flux1.in[0])", stencil_graph)
        self.assertIn("constexpr int kBatchRows = 2;", config)
        self.assertNotIn("kRowsPerCall", config)

    def test_pl_and_host_use_single_16384_row_run(self):
        toppl = read_text("pl/TopPL.cpp")
        host = read_text("ps/host.cpp")
        run_sh = read_text("run.sh")

        self.assertIn("#define TRI1PLIO_MAX_ITER 16384", toppl)
        self.assertIn("#define TRI1PLIO_MAX_DDR_WORDS 262144", toppl)
        self.assertIn("using plio_word_t = ap_uint<128>;", toppl)
        self.assertIn("void TopPL(const ddr_word_t* input", toppl)
        self.assertIn("int iter_cnt,", toppl)
        self.assertNotIn("int repeat,", toppl)
        self.assertNotIn("port=repeat", toppl)
        self.assertIn("const int total_words = iter_cnt * kDdrWordsPerRow;", toppl)
        self.assertIn("write_ddr_words(output, total_words, output_words);", toppl)
        self.assertIn("topStencil.run(iter_cnt / ROWS_PER_GRAPH_RUN);", host)
        self.assertIn("auto toppl_run = toppl(input_bo, output_bo, iter_cnt);", host)
        self.assertIn("constexpr int BOARD_GRID_ROWS = 256;", host)
        self.assertIn("constexpr int BOARD_GRID_DEPTH = 64;", host)
        self.assertIn("ITER=${2:-16384}", run_sh)
        self.assertIn("INPUT_TXT=${3:-./board_data/input.txt}", run_sh)

    def test_data_generator_emits_raw_volume_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(TRI_ROOT / "data" / "gen_case.py"),
                    "--data-dir",
                    str(out_dir),
                    "--grid-rows",
                    "4",
                    "--depth",
                    "2",
                    "--iter",
                    "8",
                    "--raw-volume",
                    "--skip-gold",
                    "--kind",
                    "zeros",
                ],
                cwd=TRI_ROOT,
                text=True,
                capture_output=True,
                check=True,
            )

            input_rows = (out_dir / "input.txt").read_text(encoding="utf-8").splitlines()
            plio_rows = (out_dir / "input_plio.txt").read_text(encoding="utf-8").splitlines()

        self.assertIn("logical workload : 4 x 256 x 2", result.stdout)
        self.assertEqual(8, len(input_rows))
        self.assertEqual(512, len(plio_rows))


if __name__ == "__main__":
    unittest.main()

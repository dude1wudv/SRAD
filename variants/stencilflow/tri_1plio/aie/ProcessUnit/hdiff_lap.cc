#include <adf.h>
#include <aie_api/aie.hpp>
#include <cstdint>
#include "include.h"
#include "hdiff.h"

using namespace adf;

namespace {

alignas(32) static const int32_t kCoeffNeg4Raw[8] =
    {-4, -4, -4, -4, -4, -4, -4, -4};
alignas(32) static const int32_t kCoeffNeg1Raw[8] =
    {-1, -1, -1, -1, -1, -1, -1, -1};

inline v8int32 load_row_chunk(const int32_t* row_base, unsigned chunk) {
  return ((v8int32*)row_base)[chunk];
}

} // namespace

void hdiff_lap(lap_input_buffer& __restrict in_window,
               output_buffer<int32_t>& __restrict sub_pack_for_flux1,
               output_buffer<int32_t>& __restrict sub_pack_for_flux2) {
  int32_t* __restrict sub_flux1_base = sub_pack_for_flux1.data();
  int32_t* __restrict sub_flux2_base = sub_pack_for_flux2.data();

  const int32_t* __restrict base_ptr = in_window.data();
  const v8int32 coeff_neg4 = *(const v8int32*)kCoeffNeg4Raw;
  const v8int32 coeff_neg1 = *(const v8int32*)kCoeffNeg1Raw;

  for (unsigned r = 0; r < hdiff_cfg::kRowsPerCall; ++r) {
    const unsigned in_off  = r * COL;
    const unsigned out_off = r * hdiff_cfg::kFluxForwardPackRows * COL;

    v8int32* __restrict out_flux1_left =
        (v8int32*)(sub_flux1_base + out_off + (0 * COL));
    v8int32* __restrict out_flux1_right =
        (v8int32*)(sub_flux1_base + out_off + (1 * COL));
    v8int32* __restrict out_flux1_up =
        (v8int32*)(sub_flux1_base + out_off + (2 * COL));
    v8int32* __restrict out_flux1_down =
        (v8int32*)(sub_flux1_base + out_off + (3 * COL));
    v8int32* __restrict out_flux2_left =
        (v8int32*)(sub_flux2_base + out_off + (0 * COL));
    v8int32* __restrict out_flux2_right =
        (v8int32*)(sub_flux2_base + out_off + (1 * COL));
    v8int32* __restrict out_flux2_up =
        (v8int32*)(sub_flux2_base + out_off + (2 * COL));
    v8int32* __restrict out_flux2_down =
        (v8int32*)(sub_flux2_base + out_off + (3 * COL));

    // data() points at the margin/history region followed by the current row.
    const int32_t* row0_base = base_ptr + in_off + (0 * COL);
    const int32_t* row1_base = base_ptr + in_off + (1 * COL);
    const int32_t* row2_base = base_ptr + in_off + (2 * COL);
    const int32_t* row3_base = base_ptr + in_off + (3 * COL);
    const int32_t* row4_base = base_ptr + in_off + (4 * COL);

    v16int32 data_buf1 = null_v16int32();
    v16int32 data_buf2 = null_v16int32();

    v8acc80 acc_0 = null_v8acc80();
    v8acc80 acc_1 = null_v8acc80();

    v8int32 lap_ij = null_v8int32();
    v8int32 lap_0  = null_v8int32();

    data_buf1 = upd_w(data_buf1, 0, load_row_chunk(row3_base, 0));
    data_buf1 = upd_w(data_buf1, 1, load_row_chunk(row3_base, 1));
    data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row1_base, 0));
    data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row1_base, 1));

    for (unsigned i = 0; i < COL / 8; i++)
    chess_prepare_for_pipelining
    chess_loop_range(1, ) {
      v16int32 flux_sub;

      acc_0 = lmul8(data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_1 = lmul8(data_buf2, 1, 0x76543210, coeff_neg1, 0, 0x00000000);

      acc_0 = lmac8(acc_0, data_buf1, 2, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_1 = lmac8(acc_1, data_buf1, 1, 0x76543210, coeff_neg1, 0, 0x00000000);

      data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row2_base, i));
      data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row2_base, i + 1));

      acc_0 = lmac8(acc_0, data_buf2, 1, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmsc8(acc_0, data_buf2, 2, 0x76543210, coeff_neg4, 0, 0x00000000);
      acc_0 = lmac8(acc_0, data_buf2, 3, 0x76543210, coeff_neg1, 0, 0x00000000);

      lap_ij = srs(acc_0, 0);

      acc_1 = lmac8(acc_1, data_buf2, 0, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_1 = lmsc8(acc_1, data_buf2, 1, 0x76543210, coeff_neg4, 0, 0x00000000);
      acc_1 = lmac8(acc_1, data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);

      lap_0 = srs(acc_1, 0);

      flux_sub =
          sub16(concat(lap_ij, undef_v8int32()), 0, 0x76543210, 0xFEDCBA98,
                concat(lap_0,  undef_v8int32()), 0, 0x76543210, 0xFEDCBA98);
      v8int32 sub_v = ext_w(flux_sub, 0);
      out_flux1_left[i] = sub_v;
      out_flux2_left[i] = sub_v;

      acc_0 = lmul8(data_buf1, 3, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmsc8(acc_0, data_buf2, 3, 0x76543210, coeff_neg4, 0, 0x00000000);

      data_buf1 = upd_w(data_buf1, 0, load_row_chunk(row1_base, i));
      data_buf1 = upd_w(data_buf1, 1, load_row_chunk(row1_base, i + 1));

      acc_0 = lmac8(acc_0, data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmac8(acc_0, data_buf2, 4, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmac8(acc_0, data_buf1, 3, 0x76543210, coeff_neg1, 0, 0x00000000);

      lap_0 = srs(acc_0, 0);

      flux_sub =
          sub16(concat(lap_0,  undef_v8int32()), 0, 0x76543210, 0xFEDCBA98,
                concat(lap_ij, undef_v8int32()), 0, 0x76543210, 0xFEDCBA98);
      sub_v = ext_w(flux_sub, 0);
      out_flux1_right[i] = sub_v;
      out_flux2_right[i] = sub_v;

      acc_1 = lmul8(data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmul8(data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);

      data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row0_base, i));
      data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row0_base, i + 1));

      acc_1 = lmsc8(acc_1, data_buf1, 2, 0x76543210, coeff_neg4, 0, 0x00000000);
      acc_1 = lmac8(acc_1, data_buf1, 1, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_1 = lmac8(acc_1, data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);

      data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row4_base, i));
      data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row4_base, i + 1));

      acc_1 = lmac8(acc_1, data_buf1, 3, 0x76543210, coeff_neg1, 0, 0x00000000);
      acc_0 = lmac8(acc_0, data_buf2, 2, 0x76543210, coeff_neg1, 0, 0x00000000);

      lap_0 = srs(acc_1, 0);

      flux_sub =
          sub16(concat(lap_ij, undef_v8int32()), 0, 0x76543210, 0xFEDCBA98,
                concat(lap_0,  undef_v8int32()), 0, 0x76543210, 0xFEDCBA98);
      sub_v = ext_w(flux_sub, 0);
      out_flux1_up[i] = sub_v;
      out_flux2_up[i] = sub_v;

      data_buf1 = upd_w(data_buf1, 0, load_row_chunk(row3_base, i));
      data_buf1 = upd_w(data_buf1, 1, load_row_chunk(row3_base, i + 1));

      acc_0 = lmsc8(acc_0, data_buf1, 2, 0x76543210, coeff_neg4, 0, 0x00000000);
      acc_0 = lmac8(acc_0, data_buf1, 1, 0x76543210, coeff_neg1, 0, 0x00000000);

      data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row1_base, i + 1));
      data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row1_base, i + 2));

      acc_0 = lmac8(acc_0, data_buf1, 3, 0x76543210, coeff_neg1, 0, 0x00000000);

      flux_sub =
          sub16(concat(srs(acc_0, 0), undef_v8int32()), 0, 0x76543210, 0xFEDCBA98,
                concat(lap_ij,        undef_v8int32()), 0, 0x76543210, 0xFEDCBA98);
      sub_v = ext_w(flux_sub, 0);
      out_flux1_down[i] = sub_v;
      out_flux2_down[i] = sub_v;

      data_buf1 = upd_w(data_buf1, 0, load_row_chunk(row3_base, i + 1));
      data_buf1 = upd_w(data_buf1, 1, load_row_chunk(row3_base, i + 2));
    }
  }
}

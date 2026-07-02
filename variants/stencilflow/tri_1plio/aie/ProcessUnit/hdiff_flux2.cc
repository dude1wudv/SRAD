#include <adf.h>
#include <aie_api/aie.hpp>
#include <cstdint>

#include "include.h"
#include "hdiff.h"

using namespace adf;

namespace {

alignas(32) static const std::int32_t kCoeffOneRaw[8] =
    {1, 1, 1, 1, 1, 1, 1, 1};
alignas(32) static const std::int32_t kCoeffNeg7Raw[8] =
    {-7, -7, -7, -7, -7, -7, -7, -7};

inline v8int32 load_row_chunk(const std::int32_t* row_base, unsigned chunk) {
  return ((v8int32*)row_base)[chunk];
}

inline v16int32 select_flux(unsigned int take_mask, v8int32 diff_vec) {
  return select16(take_mask,
                  concat(diff_vec, undef_v8int32()),
                  null_v16int32());
}

} // namespace

void hdiff_flux2(input_buffer<std::int32_t>& __restrict mask_pack,
                 flux2_input_buffer& __restrict in_window,
                 input_buffer<std::int32_t>& __restrict sub_pack,
                 output_buffer<std::int32_t>& __restrict out) {
  std::int32_t* __restrict mask_base = mask_pack.data();
  const std::int32_t* __restrict raw_base  = in_window.data();
  std::int32_t* __restrict sub_base  = sub_pack.data();
  std::int32_t* __restrict out_base  = out.data();
  const v8int32 coeff_one = *(const v8int32*)kCoeffOneRaw;
  const v8int32 coeff_neg7 = *(const v8int32*)kCoeffNeg7Raw;

  for (unsigned r = 0; r < hdiff_cfg::kRowsPerCall; ++r) {
    const unsigned in_off   = r * COL;
    const unsigned sub_off  = r * hdiff_cfg::kFluxForwardPackRows * COL;
    const unsigned mask_off = r * 4 * hdiff_cfg::kFluxMaskWordsPerRow;
    const unsigned out_off  = r * COL;

    v8int32* __restrict sub_left  = (v8int32*)(sub_base + sub_off + (0 * COL));
    v8int32* __restrict sub_right = (v8int32*)(sub_base + sub_off + (1 * COL));
    v8int32* __restrict sub_up    = (v8int32*)(sub_base + sub_off + (2 * COL));
    v8int32* __restrict sub_down  = (v8int32*)(sub_base + sub_off + (3 * COL));
    std::int32_t* __restrict mask_left  =
        mask_base + mask_off + (0 * hdiff_cfg::kFluxMaskWordsPerRow);
    std::int32_t* __restrict mask_right =
        mask_base + mask_off + (1 * hdiff_cfg::kFluxMaskWordsPerRow);
    std::int32_t* __restrict mask_up =
        mask_base + mask_off + (2 * hdiff_cfg::kFluxMaskWordsPerRow);
    std::int32_t* __restrict mask_down =
        mask_base + mask_off + (3 * hdiff_cfg::kFluxMaskWordsPerRow);
    // data() points at the margin/history region followed by the current row.
    const std::int32_t* __restrict row2_base = raw_base + in_off + (1 * COL);
    v8int32* __restrict out_row = (v8int32*)(out_base + out_off);

    v16int32 data_buf2 = null_v16int32();

    data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row2_base, 0));
    data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row2_base, 1));

    for (unsigned i = 0; i < COL / 8; ++i)
    chess_prepare_for_pipelining
    chess_loop_range(1, ) {
      v8int32 flux_sub;

      flux_sub = sub_left[i];
      v16int32 out_flx_inter1 =
          select_flux((unsigned int)mask_left[i], flux_sub);

      flux_sub = sub_right[i];
      v16int32 out_flx_inter2 =
          select_flux((unsigned int)mask_right[i], flux_sub);

      v16int32 flx_out2 = sub16(out_flx_inter2, out_flx_inter1);

      flux_sub = sub_up[i];
      v16int32 out_flx_inter3 =
          select_flux((unsigned int)mask_up[i], flux_sub);

      v16int32 flx_out3 = sub16(flx_out2, out_flx_inter3);

      flux_sub = sub_down[i];
      v16int32 out_flx_inter4 =
          select_flux((unsigned int)mask_down[i], flux_sub);

      v16int32 flx_out4 = add16(flx_out3, out_flx_inter4);

      v8acc80 final_output =
          lmul8(flx_out4, 0, 0x76543210, coeff_neg7, 0, 0x00000000);
      final_output =
          lmac8(final_output, data_buf2, 2, 0x76543210,
                concat(coeff_one, undef_v8int32()), 0, 0x76543210);

      out_row[i] = srs(final_output, 0);

      data_buf2 = upd_w(data_buf2, 0, load_row_chunk(row2_base, i + 1));
      data_buf2 = upd_w(data_buf2, 1, load_row_chunk(row2_base, i + 2));
    }
  }
}

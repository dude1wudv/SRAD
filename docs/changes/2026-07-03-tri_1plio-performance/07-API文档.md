# 接口文档

## Host 入口

`./host.exe <xclbin> [iter_cnt] [input_txt] [output_txt]`

当前两个目标目录均使用该入口形式。

## TopPL 接口

当前 `tri` 与 `tri_1plio` 的 TopPL 函数形态一致：

```cpp
void TopPL(const ddr_word_t* input,
           ddr_word_t* output,
           int iter_cnt,
           hls::stream<plio_word_t>& to_aie,
           hls::stream<plio_word_t>& from_aie)
```

## 需要统一的输出字段

建议两边至少统一输出：

- `pl_transfer_us`
- `aie_run_us`
- `pipeline_total_us`
- `iter_cnt`
- `input_elems`
- `output_elems`

是否改 host 输出字段，待用户确认后执行。

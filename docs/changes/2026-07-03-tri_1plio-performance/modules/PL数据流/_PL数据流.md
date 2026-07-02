上级：[[tri_1plio 性能优化]]
下级：[[DDR 到 PLIO 打包]]、[[PLIO 到 DDR 解包]]
依赖：[[计时口径]]、[[参数规模]]
---

# PL 数据流

当前 `tri` 与 `tri_1plio` 的 PL TopPL 结构基本一致：

- DDR 512-bit read，II=1。
- 512-bit 拆成 4 个 128-bit PLIO word。
- AIE 输出 4 个 128-bit PLIO word 合回 512-bit。
- DDR 512-bit write，II=1。

低优先级原因：

- 两边 TopPL 差异主要是规模常量从 20 改到 64。
- 若同口径计时确认 `pl_transfer_us` 已经接近理论流式传输下限，优先改 AIE。

仍需检查：

- `TRI1PLIO_MAX_DDR_WORDS` 是否覆盖 256*256*64。
- m_axi depth 元数据是否与实际 `iter_cnt` 一致。
- host BO size 是否与 TopPL 循环访问范围一致。

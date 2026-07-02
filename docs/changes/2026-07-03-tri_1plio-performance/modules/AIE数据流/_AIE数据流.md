上级：[[tri_1plio 性能优化]]
下级：[[单 PLIO 三路 fanout]]、[[sub_pack 与 mask_pack]]、[[FIFO depth 扫描]]
依赖：[[计时口径]]、[[参数规模]]
---

# AIE 数据流

当前 `tri_1plio` 的主要结构变化在 AIE 内部，而不是 PL 打包代码。

核心差异：

- `tri`：单输入进入 core，lap 和 flux1 消费同一路输入；lap 给 flux1 4 路；flux1 给 flux2 5 路。
- `tri_1plio`：单输入 PLIO fanout 到 lap、flux1、flux2；lap 的 `sub_pack` 同时给 flux1 和 flux2；flux1 只给 flux2 `mask_pack`。

瓶颈假设：

- 小数据 emu 下，减少 flux1->flux2 大包让 `tri_1plio` 更快。
- 大数据板上，单 PLIO 三路 fanout、lap 输出二次消费、FIFO backpressure 可能盖过中间包缩减收益。

优先实验：

1. 扫描 FIFO depth：2、4、6、8。
2. 打开 AIE profile/stall 采样，确认是否卡在 input fanout 或 lap->flux2。
3. 做只改 fanout 的最小实验：保留 `tri_1plio` kernel 逻辑，改输入/延迟策略。

## 已实施

- lap 的 `sub_pack` 输出从单输出 fanout 改为双输出。
- `k_lap.out[0]` 只连接 flux1，`k_lap.out[1]` 只连接 flux2。
- lap kernel 内对两个输出 buffer 写入相同 sub_pack，参考 `tri_8plio/tri_16plio` 的成熟连接模式。

上级：[[03-索引]]
下级：无
依赖：[[aie/Config.h]]、[[aie/ProcessGraph/StencilCoreGraph.h]]、[[pl/TopPL.cpp]]、[[conn.cfg]]
---

# 96-vs-192-diagnosis

场景：判断 `ours_192lane` 是否应继续沿着“复制 96lane 并翻倍”的方向推进。

触发：用户说明 96lane 已在板上跑通，192lane 布局布线压力大且编译不成功。

逻辑：

1. 以 `ours_96lane` 为稳定基线，不因本地老化测试否定它。
2. 比较 96 与 192 的 lane、AIE kernel、TopPL CU、stream_connect、stream depth、pktmerge、TopPL FIFO。
3. 若差异显示 192 同时推高 AIE、PL、stream、DDR/NoC 压力，则判定“直接翻倍”方向风险高。
4. 若缺少实际 impl 日志，则只给概率诊断，不声称唯一 root cause。

结论：当前证据支持停止硬怼 192 直接翻倍，先做缩小架构或针对 pktmerge/depth 的 A/B。

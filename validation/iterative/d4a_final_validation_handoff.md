# Corrected D4-A：首个 VALID_MET 后最短交接表

2026-09-23 执行顺序修订：用户明确批准将唯一一次 CE production 提前，与既有 Picard 接续并行。只改变先后顺序，保持冻结的模型、20,000 × 300 批、100 inactive、seed 731942、18 threads、900 秒硬上限；失败不自动重试。该次已正常完成（OpenMC 111.22 秒），产物在 `validation/artifacts/d4a-corrected-ce-production-20260923`。首次审计因 statepoint 缺失 Git 属性而拒绝；用户随后批准限于该封存构建的格式兼容修正，原文件 CE-only 重放现已通过，见 [CE 结果与重放记录](../d4_reference/d4a_ce_production_result_20260923.md)。最终 SPOT–CE 比较仍必须等首个独立验收的 corrected `VALID_MET` 和完整 lineage，并再次复验 CE。已经执行过的 CE production 不得在收敛后再次启动。

最新启动记录（2026-09-23）：用户在修复提交 `70039e3` 后再次批准接续。新 `$CONT` 已通过启动前清单/身份检查，日志确认 `CLOSED/8 -> PROJECTED/9`，径向 Dragon 已启动；启动后两处 canonical SHA 均仍为原值。最多 maps 9–12，单轮径向 32400 秒、轴向 180 秒，首次 MET 即停，任何失败即停且不自动重试。启动不是完成或持续存活证明，接手时须核对实际进程、日志和封存回执；当前已验收结果仍只到 map 8。

此前事件（保留）：maps 1–8 均为 `VALID_NOT_MET / NEXT_MAP_PARENT_ONLY`。旧 series 已封存 `map-001.portable` 至 `map-003.portable`（全局 maps 6–8），随后 map 9 中断。上次获批接续又在径向第 1 平面即主动停止：旧 one-map runner 的隐式构建重新链接了已冻结的 Dragon，且硬链接同时改动了 release 副本。未完成任何新 map，不能作为数值不收敛证据或接续父态。

已从另一份 SHA 完全一致的冻结副本恢复原 binary，分离工作/release 两个 inode，38 项 release 清单复验通过。运行时构建已删除，改为预检既有 canonical hash 与现成 host 工具；当时未自动重试。两次不完整 map-9 目录（旧 `map-004.raw` 和 `FAILED_CONT/map-001.raw`）都不作输入；仍从 `CLOSED/8` 接续。本页不宣称固定点、最终 k 或 CE 结果。

7 项启动预检短测与现有 10 项 series 短测通过，均不启动输运。map 8 的完整清单再次通过，当前 host 重放的独立检查与三缺陷 gate 日志逐字节一致。恢复源为 `validation/artifacts/iterative-d4a-rank2-picard-map8/frozen_runtime/Dragon`，只是取回同一 binary，不采用该历史物理态。`resume_d4a_rank2_picard_after_radial.sh` 等历史旁路不用于本次接续；修复范围限于活动 one-map runner。

## 主动接续与精度风险（2026-09-23）

用户要求自主推进，不再等待逐步指令。当前线程已启用每 15 分钟的接续
`spot-d4-a`：实际主线有新结果时处理结果，正常计算而无新结果时不重复通知。
它不扩大 maps 9–12 的既有计算预算，不允许自动重试、修改冻结模型或放宽验收。
需要新增长期计算或实质改变物理路线时，仍须明确说明证据与所需授权。

**收敛与精度必须分开。** 已保存的 corrected map 8 是 `VALID_NOT_MET`，
其 `SPOT-KEFF64=1.2721230284653975`；已独立审计的 CE 为
`1.3030848883933903 ± 0.0003319711641137808`（一倍标准差）。
仅作风险排查的算术比较给出
`1e5*(1/k_CE-1/k_map8)=-1867.7778410161716 pcm`。
现有精度门槛为 `500+3*sigma_pcm=558.6511050793662 pcm`，对应
`k_SPOT` 区间 `[1.293667380384685, 1.3126405150953528]`。
最近 map-8 的 `rho=1/k` 改变量只有 `0.104927399302568 pcm`。
这不是最终精度拒绝或剩余误差上界，也不是严格的收敛外推；但不能再假定
仅等外迭代完成就能消除当前差异。最终 comparator 仍只接收首个 MET。

有界独立源审查未发现新的生产边界/几何/材料错配。尤其 D4 的 1/12 对称切面
在 SALT 的 TISO 路线上做镜像全展开并删除切面元素，不是额外保留的 white
边界（`SAL_GEOMETRY_MOD.f90:237–270,3472–3474,3562–3568`）。
CE 六个外侧面为 white、两端 vacuum，总高 150 cm，三个温度层顺序保持一致。

优先排查以下两项，而不是拟合系数或仅增加 Picard 次数：

1. **轴向离散。** `d4a_rank2_basis.x2m:18–26` 只有三个 50 cm 数值单元，
   `SPOT1P64.f90:250–251` 仅支持 constant diamond，角度为 SN8。
   三个物理温度层正确不等于轴向空间/角度离散已验证收敛。
   最小下一实验应固定已存径向算子、POD 基、截面、150 cm 总高与温度界面，
   只对轴向网格做预先声明的细化；作为隔离敏感性实验，不回写生产链、不冒充
   新的耦合固定点，不根据 CE 值选择网格。
   已完成最小静态修正：`SPOASM.f` 的 FIXB 入口不再要求径向基载体的旧轴向
   `NUNKN` 等于目标网格的 `NUNKN`，仍检查旧值为正，以及群数、径向维数、
   snapshots、rank、体积逐位一致和基/provenance。输出长度始终来自新 TRACK。
   `run_spophys_smoke.sh` 的合成 7/14 存储长度双回环通过，B/径向算子/截面保持
   不变；旧长度无效、群数错配、径向体积错配三个负测均拒绝。两路独立审查
   未发现 P1/P2。该测试不是实际 3→6 floor 几何或 D4 REAL64 输运验证。
   canonical 与 release binary 均未重建、SHA 未变；真实细化实验须使用隔离
   候选程序，由新 GEOM→SPOT→SYSTEM→FLUX 自然生成对象，不能改封存头或
   将旧轴向通量冒充新网格状态。SPOSTATE/SPORATE 已支持按 MAT1D 汇总细网格
   到三个温度层；现有三层专用诊断器不能直接当作细网格检查器。
   随后已做一次隔离短实验：canonical/candidate 的 3-cell 冷启动 k64 同为
   `1.2721209124951036`，370 群径向包逐位不变；相对 map 8 暖启动差
   `-0.1307531197 pcm`。6-cell 在预声明的 30 秒上限停止，没有结果、没有重试，
   12-cell 未启动；**网格敏感性仍未完成**。见 [实验记录](d4a_axial_mesh_probe_result.md)。
   不能将该不完整实验加入生产 lineage，接续任务不得自动重跑。
2. **核数据处理与闭包。** APOL、ANIS3、TONE/370 群链与 CE 连续能量温度插值
   的差异，以及 2D/1D 闭包与 POD 误差，尚未分离。
   DLIB 目标目录同样标记 ENDF/B-VIII.1，不能说已证实评价库不同，更不能将
   总差值全部归为 POD。先用现有冻结证据定位，不启动新的多群/CE 长计算。

并行交付链审查未发现当前会阻断后处理的 P1/P2：canonical/host/deck 身份、
连续全局 epoch 与短 XSM 路径、fresh 输出目录以及 CE 的已批准格式兼容均可衔接。
这只表示实现路径就绪，不替代实际 MET 或物理精度门槛。

## 路径与严格顺序

以下变量在 `/Users/wen/spot` 下使用；`<…>` 必须由实际封存结果替换，不能原样执行。

```sh
cd /Users/wen/spot
A=/Users/wen/spot/validation/artifacts
BOOT="$A/d4a-corrected-closed0-runtime-release-20260920"
M1="$A/d4a-corrected-material-rank2-map1-portable-detached-20260920"
M2="$A/d4a-corrected-material-rank2-map2-portable-detached-20260920"
M3="$A/d4a-corrected-material-rank2-map3-portable-detached-20260921"
M4="$A/d4a-corrected-material-rank2-map4-portable-detached-20260921"
M5="$A/d4a-corrected-material-rank2-map5-portable-detached-20260922"
SERIES="$A/d4a-corrected-material-rank2-series-from-map5-20260922"
FAILED_CONT="$A/d4a-corrected-material-rank2-series-from-map8-20260923"
CONT="$A/d4a-corrected-material-rank2-series-from-map8-restart-20260923"
FINAL='<实际首个 VALID_MET 的完整 portable 路径>'
OBS='<不存在的新 observables 目录绝对路径>'
RESULT='<不存在的新 result-export 目录绝对路径>'
CE="$A/d4a-corrected-ce-production-20260923"
PY=/Users/wen/miniforge3/envs/openmc-dev/bin/python
XS=/Users/wen/openmc-workspace/data/endfb-viii.1-hdf5/cross_sections.xml
OPENMC=/Users/wen/miniforge3/envs/openmc-dev/bin/openmc
```

验收参数必须依次为 **M1、M2、M3、M4、M5，再接当前 series 的 maps 6–8 portable，以及后续获批新 series 的完整连续 portable，直到且包括 FINAL，每个仅一次**。以各 `picard_series.tsv` 的 `epoch`、`portable` 和封存回执为准；不可遗漏中间 map，不可加入首个 MET 后的 map，不可用 `.raw` 替代。

| 当前 series 局部路径 | 全局 epoch |
|---|---|
| `$SERIES/map-001.portable` | map 6，已封存，`VALID_NOT_MET` |
| `$SERIES/map-002.portable` | map 7，已封存，`VALID_NOT_MET` |
| `$SERIES/map-003.portable` | map 8，已封存，`VALID_NOT_MET` |
| `$CONT/map-001.portable` 起的实际封存结果 | 从 map 9 连续到首个 MET，最多 map 12；尚未完成，不可提前纳入 |

下列命令模板中的 `<SERIES_PORTABLES_IN_ORDER_THROUGH_FINAL>` 应展开为上述实际路径的逐项引用列表；`<REPEATED_SERIES_SPOT_MAP_ARGS>` 则对同一列表逐项写 `--spot-map "绝对路径"`。不得猜测首个 MET 的 map 号，FINAL 不另重复追加。

当前日志为 `$CONT.runner.log`，完成结果以 `$CONT/picard_series.tsv` 及实际 portable 回执为准。此前停止记录为 `$FAILED_CONT.runner.log`，其结果表没有已完成 map。改动后的 binary 保留为 `$FAILED_CONT/interrupted_solver_Dragon`（SHA `0019568a653b81cebeaad742948adedc984a766a2c9ed25629abd1b23f75f67d`）；原 canonical SHA 仍是 `2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`，未重签任何收据。新启动使用独立目录，不复用失败现场。

## 执行顺序（由主代理在前置门槛成立后执行）

| 顺序 | 操作与通过条件 |
|---|---|
| 1 | 在后续获批 continuation 到首个冻结 `VALID_MET / CONVERGED_MAP` 并停止后，核对每个 portable 的 `result.sha256`、分类与连续 epoch。三缺陷均须 `<= 5e-7`，固定 rank 2、α=1、无经验系数不变。 |
| 2 | 从 FINAL 提取 k 与底/中/顶全局归一化 ν-fission 份额，再完整回放 lineage；必须得到 `D4A-CORRECTED-ACCEPT OVERALL PASS`。提取及验收会调用 canonical Dragon 的只读 GREP + SPORATE，不是新的输运求解，但仍属于进程启动。 |
| 3 | 导出 `result.json`、`power.csv` 并验证 `export_result.sha256`；导出器不能替代步骤 2。 |
| 4 | 使用 2026-09-23 单独获批提前执行的唯一 CE production 产物；不得因 SPOT 收敛而再次启动。若该次失败或超时，停止并请求处置，不自动重试。 |
| 5 | 独立 CE checker 再验完整 SPOT lineage、CE 静态模型、核数据、运行身份和最终 statepoint；仅成功终止行 `D4A SPOT-CE RECEIPT COMPARISON PASS` 可作为现有比较门槛通过证据。 |

```sh
# 1：对有序列表中的每个 portable 分别验证（P 为当前实际路径）
(cd "$P" && shasum -a 256 -c result.sha256)
# 2
TIMEOUT_SECONDS=10 sh validation/iterative/run_d4a_corrected_final_observables.sh "$BOOT" "$FINAL" "$OBS"
D4A_OBSERVABLES_DIR="$OBS" sh validation/iterative/check_d4a_corrected_acceptance.sh \
  "$BOOT" "$M1" "$M2" "$M3" "$M4" "$M5" <SERIES_PORTABLES_IN_ORDER_THROUGH_FINAL>
# 3
python3 validation/iterative/export_d4a_corrected_result.py "$FINAL" "$OBS" "$RESULT"
(cd "$RESULT" && shasum -a 256 -c export_result.sha256)
# 4：只核验提前获批的唯一 CE 产物，禁止在收敛后重跑。
(cd "$CE" && shasum -a 256 -c result_receipt.sha256)
# 5
"$PY" validation/d4_reference/check_d4a_spot_ce_receipts.py \
  --corrected-build "$BOOT" --spot-map "$M1" --spot-map "$M2" \
  --spot-map "$M3" --spot-map "$M4" --spot-map "$M5" \
  <REPEATED_SERIES_SPOT_MAP_ARGS> \
  --spot-observables "$OBS" --ce-result "$CE" --cross-sections "$XS" \
  --openmc-exec "$OPENMC"
```

## 停止条件与真实功率验证边界

任何回执、独立回放、链路、身份或门槛失败立即停止交接，不改 rank、α、模型或阈值，不编译、不自动重跑。series 达其批准的步数上限但未 MET（退出 3 / `NO_CONVERGENCE_CLAIM`）不是收敛；不得另起竞争任务。保留失败/未完成目录，后续处置交主代理。

CE 冻结协议：每批 20,000 粒子、300 批、100 inactive、200 active、4,000,000 active histories，seed 731942、1 MPI、18 threads、900 秒上限。超时、非零退出、非最终 statepoint、realizations 不符或 `sigma_pcm = 1e5*sigma_k/k_CE² > 50` 都拒收，不拼接结果或根据 SPOT 值挑 seed/样本量。反应性门槛仅为 `1e5*abs(1/k_SPOT - 1/k_CE) <= 500 + 3*sigma_pcm`。

当前 SPOT 导出仅含三层全局归一化 ν-fission 份额，不是逐针功率或绝对热功率。CE checker 重建 651 个 cell/floor/pin 的 ν-fission tally 以验证回执，但只报告三层差异且明确 `status=REPORTED_ONLY`；没有功率形状验收阈值、没有 SPOT 对 CE 的逐针功率通过判定。即使总体比较 PASS，也不得写成“针功率验证通过”。真实逐针功率验证仍需匹配的 SPOT 逐针观测量、全局归一化/映射及预先约定的验收准则，属于另行审定的边界，不在本交接中添加。

SPOT–CE 的反应性差异是两条计算链的总差异，不能全部归因于 rank-2/SPOD：SPOT 使用多群库、APOL 输运修正与 TONE 自屏蔽，CE 使用连续能量和温度插值；分别封存库身份不等于证明评价及处理链完全等价。源码核对未发现几何、边界、材料公式或三层映射的生产阻断不匹配。新的材料-only 短测试已逐项报告三温度各 59 个材料/核素密度，保留 750 C 旧锚点；最大相对 SPOT 打印值/CE 差异为 `6.02742707e-7`，仅报告差异，不增设容差或声称逐位相等。参见 [material audit](../d4_reference/material_epoch_audit_result.md)。

依据：[quickstart](D4A_CORRECTED_QUICKSTART.md)、[CE protocol](../d4_reference/d4a_ce_production_protocol.md)、[CE README](../d4_reference/README.md)及上述现有脚本。

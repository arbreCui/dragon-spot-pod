# Corrected D4-A：首个 VALID_MET 后最短交接表

## 最高优先级更新：散射实现缺陷，旧链暂停验收（2026-09-23）

下文的“首个 MET 后验收”流程目前禁用，直到修复版通过短测并建立新链。
审查发现 `SPOASM` 从只有 P0 的径向截面记录读入三列数组后，写出未初始化
P1/P2；`FLU` 将 TRACK 的空间字段 9/10 当作角阶，漏掉跨群高阶散射。
真实 map 8、9 的轴向 P1 列均全零，而宏库 6660 个正混合物 P1 对角项全部
非零。源码缺陷早于冻结 binary；旧的逐位审计没有覆盖物理散射语义。
证据在 `validation/artifacts/d4a-scattering-audit-20260923`，输入清单读前后
一致。旧 sealed 文件及分类不改写，但不再具有声明 SCAT3 方法的物理验证资格。

最小修复：轴向显式各向异性使用原宏库 NTOT0/SIGW，各向同性路径保留原
径向 transport-corrected 截面；径向闭包仍使用原径向权威数据，公式不变。
FLU 读取 15/16 并按声明散射阶截断；SPOT 跨群源用原始 Legendre 矩，
`(2l+1)/2` 只在轴向 kernel 展开一次。未加经验参数或放宽阈值。
目前显式各向异性 `NW>0 / P0_TOTAL` 不在修复支持范围，明确拒绝而非猜测。

已通过：带非零 P1、负 P2 的 SPOASM 合成回环，正负泄漏及预扣/未扣泄漏
P0 数据；8 个畸形/来源负例拒绝；32/64 SPOT 下散/热循环、标量/向量源组装
共 8 例，以及非 SPOT 4 例原行为回归。源测试替换最终求解入口，不能冒充
实际输运测试。原 level-2 kernel/换基/闭包测试也通过。

主线程尝试仅终止本次专用监督进程 PID 54771，被沙箱以 operation not
permitted 拒绝；不能宣称进程已停，也不能尝试绕过权限。其后旧控制器自行
完成 map 10（仍 NOT_MET）并进入 map 11；这些旧实现产物一律不用于修复版
验收。54771 已不存在，不得再按旧 PID 操作。最后实际核对：控制器 17661、
map-11 专用监督 74248、Dragon 74249；操作前必须重新确认命令/父子关系。
用户已收到更新的停止请求。旧控制会话为 24596；确认终止前不改 canonical、
库或活动 runner。其他项目进程不属于本线程，禁止操作。旧链自动验收已暂停。

下一步先完成修复版独立短测试和审查；只允许隔离新二进制。原 90 秒 6-cell
诊断仍未获用户答复，不执行。不得自动从旧 CLOSED/9 接成新物理链，不得
重跑 CE。下方先前状态仅保留作历史追踪。

更新：隔离修复版已完成真实 D4 组装；370 群轴向各阶截面与原宏库逐位一致，
4070 条 POD/径向记录（含 RADIAL-OP64）逐位不变。但其唯一一次 3-cell
轴向试算在 30 秒硬上限停止，无有效 k/通量、未重试。已另行请求一次 90 秒
修复版 **3-cell** 验证，尚无用户答复。原 6-cell 请求仍不执行。
详见[散射修复记录](d4a_scattering_fix_result.md)。新增实际 kernel 制造解已验证
反射/周期边界下 raw P0/P1/P2 归一化；完整快速回归及本轮短测通过。

## 以下为散射缺陷发现前的历史状态

2026-09-23 执行顺序修订：用户明确批准将唯一一次 CE production 提前，与既有 Picard 接续并行。只改变先后顺序，保持冻结的模型、20,000 × 300 批、100 inactive、seed 731942、18 threads、900 秒硬上限；失败不自动重试。该次已正常完成（OpenMC 111.22 秒），产物在 `validation/artifacts/d4a-corrected-ce-production-20260923`。首次审计因 statepoint 缺失 Git 属性而拒绝；用户随后批准限于该封存构建的格式兼容修正，原文件 CE-only 重放现已通过，见 [CE 结果与重放记录](../d4_reference/d4a_ce_production_result_20260923.md)。最终 SPOT–CE 比较仍必须等首个独立验收的 corrected `VALID_MET` 和完整 lineage，并再次复验 CE。已经执行过的 CE production 不得在收敛后再次启动。

最新结果（2026-09-23）：用户在修复提交 `70039e3` 后再次批准的 `$CONT` 已完成 map 9，封存为 `CLOSED/9 / VALID_NOT_MET / NEXT_MAP_PARENT_ONLY`。完整 `result.sha256`、input/output 清单和 map-8 父态身份核验通过；现成独立检查器与 gate 的只读重放均与封存日志逐字节相同。求解日志的 REAL64 `k=1.2721229193478445`，相对 map 8 的反应性变化为 `-0.006742740199516817 pcm`。这不是最终固定点或独立精度验收。

| 外迭代缺陷 | map 9 | 与 `5e-7` 门槛之比 | 状态 |
|---|---:|---:|---|
| Rrho | 6.7427401995168168e-8 | 0.134855 | PASS |
| Rleak | 8.9211010879356053e-7 | 1.784220 | NOT MET |
| Ra | 3.5292261241480969e-6 | 7.058452 | NOT MET |

三项分别为 map-8 值的约 `0.06426 / 0.28749 / 0.26928`，仅报告这一次实测下降，不外推固定收敛率或剩余步数。map-9 `result.sha256` 的 SHA 为 `598e517ec7c4f011556ec071b812de0620079105f7939fef5e0d5324fa4d9b7c`。原接续控制器已启动 map 10，并进入径向 plane 1；启动本身不能作为此后持续存活的证明。仍最多 maps 9–12，单轮径向 32400 秒、轴向 180 秒，首次 MET 或任何失败即停、不自动重试。两处 canonical SHA 核验仍为原值；未重新编译、改 rank、α 或阈值。接手时继续核对实际会话、日志和封存回执。

只读耗时排查未发现“每轮清零冷启动”：`SPOR64_B2H` 以既有 SOLVED 通量为底，替换标量区域为本轮 POD 投影、保留其他未知量；`SPOR64_B2B` 的 CONT 分支读取该 PROJECTED 态的 REAL64 FLUX；`SPOR64_A9` 将其作为当前外迭代初值，`SPOR64_A8` 传入并更新该初值。GMRES 清零的是 Krylov 工作数组，不是物理初值。这个静态核查不等于运行时性能剖析，也不证明当前初值最优；没有据此修改生产求解器或新增缓存/参数。

map-9 原日志的 `cle2000_c: cpu time` 分别为径向 `18021.00 second`、轴向 `1.00 second`，即约 5 小时 CPU 时间对 1 秒。这是已完成这一次调用的计时，不是墙钟、后续轮次耗时保证或细粒度性能剖析；主要计算成本在径向半步，不能把等待都归于验收工作。

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
   后续只读比对已有 CE 原生 global leakage tally，得到每单位裂变源的两端
   泄漏：map 8 为 `k*L/F=0.08964776528619689`，CE 为
   `0.062301665075948254 +/- 0.00012926235482585316`（批均值标准误）。
   SPOT 高出约 2.735 个百分点；这使轴向离散检查有了直接物理观测依据，
   但不证明网格是唯一原因，也不是反应性差的因果分解。F 使用既有 REAL32
   镜像积分，map 8 尚未 MET；详见[同态泄漏诊断](d4a_axial_current_result.md#saved-ce-leakage-comparison-a-concrete-accuracy-diagnostic)。
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
| `$CONT/map-001.portable` | map 9，已封存，`VALID_NOT_MET` |
| `$CONT/map-002.portable` 起的实际封存结果 | 从 map 10 连续到首个 MET，最多 map 12；尚未完成，不可提前纳入 |

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
| 6 | 对同一 FINAL 按现有 [逐针只读提取步骤](../d4_reference/d4a_pin_diagnostic_result.md) 生成 75 个区域率和 651 个针/温区 ν-fission 份额，再用 `compare_d4a_pin_rates.py` 与同一 CE `reference_result.json` 比较并冻结输出。记录 FINAL 清单、原始输入和输出 SHA；不得使用 map-8 诊断代替最终提取。逐针差异仍是 REPORTED_ONLY，不增加精度阈值或宣称热功率验证。 |

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

当前主 `result.json/power.csv` 导出仅含三层全局归一化 ν-fission 份额，不是逐针功率或绝对热功率。CE checker 重建 651 个 cell/floor/pin 的 ν-fission tally 以验证回执，但只报告三层差异且明确 `status=REPORTED_ONLY`；没有功率形状验收阈值、没有 SPOT 对 CE 的逐针功率通过判定。即使总体比较 PASS，也不得写成“针功率验证通过”。真实逐针功率验证仍需最终固定点的匹配观测量及预先约定的验收准则；步骤 6 只交付既有全局归一化/映射下的差异报告，不增设判据。

逐针后处理已用真实数据预演：map 8（NOT_MET）的 651 个份额与已重验的 CE
生产结果全部唯一匹配，最大逐针相对差 1.8599%、RMS 0.8752%；这只是包含
CE 统计噪声的暂态差异，不能作为最终功率验收。步骤 6 复用已实现的映射、
导出和比较工具，不增加输运或新模型；主 `result.json/power.csv` 的原有三层
格式保持不变，逐针文件另存独立目录。

SPOT–CE 的反应性差异是两条计算链的总差异，不能全部归因于 rank-2/SPOD：SPOT 使用多群库、APOL 输运修正与 TONE 自屏蔽，CE 使用连续能量和温度插值；分别封存库身份不等于证明评价及处理链完全等价。源码核对未发现几何、边界、材料公式或三层映射的生产阻断不匹配。新的材料-only 短测试已逐项报告三温度各 59 个材料/核素密度，保留 750 C 旧锚点；最大相对 SPOT 打印值/CE 差异为 `6.02742707e-7`，仅报告差异，不增设容差或声称逐位相等。参见 [material audit](../d4_reference/material_epoch_audit_result.md)。

依据：[quickstart](D4A_CORRECTED_QUICKSTART.md)、[CE protocol](../d4_reference/d4a_ce_production_protocol.md)、[CE README](../d4_reference/README.md)及上述现有脚本。

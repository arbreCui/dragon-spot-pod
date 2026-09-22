# Corrected D4-A：首个 VALID_MET 后最短交接表

2026-09-22 只读核对：下列已有目录、回执及命令入口均存在；maps 1–6 均为 `VALID_NOT_MET / NEXT_MAP_PARENT_ONLY`。当前 series 已封存 `map-001.portable`（全局 map 6），`map-002.raw`（全局 map 7）正在计算；本页不宣称固定点、最终 k 或 CE 结果。

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
FINAL='<实际首个 VALID_MET 的完整 portable 路径>'
OBS='<不存在的新 observables 目录绝对路径>'
RESULT='<不存在的新 result-export 目录绝对路径>'
CE='<不存在的新 CE-production 目录绝对路径>'
PY=/Users/wen/miniforge3/envs/openmc-dev/bin/python
XS=/Users/wen/openmc-workspace/data/endfb-viii.1-hdf5/cross_sections.xml
OPENMC=/Users/wen/miniforge3/envs/openmc-dev/bin/openmc
```

验收参数必须依次为 **M1、M2、M3、M4、M5，再接当前 series 的全部已封存 portable，直到且包括 FINAL，每个仅一次**。以 `picard_series.tsv` 的 `epoch`、`portable` 和封存回执为准；不可遗漏中间 map，不可加入首个 MET 后的 map，不可用 `.raw` 替代。

| 当前 series 局部路径 | 全局 epoch |
|---|---|
| `$SERIES/map-001.portable` | map 6，已封存，`VALID_NOT_MET` |
| `$SERIES/map-002.portable` 至 `$SERIES/map-007.portable` | maps 7–12，按局部编号递增；只取实际存在且到首个 MET 为止 |

下列命令模板中的 `<SERIES_PORTABLES_IN_ORDER_THROUGH_FINAL>` 应展开为上述实际路径的逐项引用列表；`<REPEATED_SERIES_SPOT_MAP_ARGS>` 则对同一列表逐项写 `--spot-map "绝对路径"`。不得猜测首个 MET 的 map 号，FINAL 不另重复追加。

## 执行顺序（由主代理在前置门槛成立后执行）

| 顺序 | 操作与通过条件 |
|---|---|
| 1 | 等待现有 series 自行到首个冻结 `VALID_MET / CONVERGED_MAP` 并停止；核对每个 portable 的 `result.sha256`、分类与连续 epoch。三缺陷均须 `<= 5e-7`，固定 rank 2、α=1、无经验系数不变。 |
| 2 | 从 FINAL 提取 k 与底/中/顶全局归一化 ν-fission 份额，再完整回放 lineage；必须得到 `D4A-CORRECTED-ACCEPT OVERALL PASS`。提取及验收会调用 canonical Dragon 的只读 GREP + SPORATE，不是新的输运求解，但仍属于进程启动。 |
| 3 | 导出 `result.json`、`power.csv` 并验证 `export_result.sha256`；导出器不能替代步骤 2。 |
| 4 | 仅步骤 2 通过后，执行一次既有 CE production wrapper；不得直接运行 builder 的生产模式。 |
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
# 4
"$PY" validation/d4_reference/run_d4a_ce_production.py \
  --output "$CE" --cross-sections "$XS" --openmc-exec "$OPENMC"
# 5
"$PY" validation/d4_reference/check_d4a_spot_ce_receipts.py \
  --corrected-build "$BOOT" --spot-map "$M1" --spot-map "$M2" \
  --spot-map "$M3" --spot-map "$M4" --spot-map "$M5" \
  <REPEATED_SERIES_SPOT_MAP_ARGS> \
  --spot-observables "$OBS" --ce-result "$CE" --cross-sections "$XS" \
  --openmc-exec "$OPENMC"
```

## 停止条件与真实功率验证边界

任何回执、独立回放、链路、身份或门槛失败立即停止交接，不改 rank、α、模型或阈值，不编译、不自动重跑。series 达七步上限但未 MET（退出 3 / `NO_CONVERGENCE_CLAIM`）不是收敛；当前运行不另起竞争任务。保留失败/未完成目录，后续处置交主代理。

CE 冻结协议：每批 20,000 粒子、300 批、100 inactive、200 active、4,000,000 active histories，seed 731942、1 MPI、18 threads、900 秒上限。超时、非零退出、非最终 statepoint、realizations 不符或 `sigma_pcm = 1e5*sigma_k/k_CE² > 50` 都拒收，不拼接结果或根据 SPOT 值挑 seed/样本量。反应性门槛仅为 `1e5*abs(1/k_SPOT - 1/k_CE) <= 500 + 3*sigma_pcm`。

当前 SPOT 导出仅含三层全局归一化 ν-fission 份额，不是逐针功率或绝对热功率。CE checker 重建 651 个 cell/floor/pin 的 ν-fission tally 以验证回执，但只报告三层差异且明确 `status=REPORTED_ONLY`；没有功率形状验收阈值、没有 SPOT 对 CE 的逐针功率通过判定。即使总体比较 PASS，也不得写成“针功率验证通过”。真实逐针功率验证仍需匹配的 SPOT 逐针观测量、全局归一化/映射及预先约定的验收准则，属于另行审定的边界，不在本交接中添加。

SPOT–CE 的反应性差异是两条计算链的总差异，不能全部归因于 rank-2/SPOD：SPOT 使用多群库、APOL 输运修正与 TONE 自屏蔽，CE 使用连续能量和温度插值；分别封存库身份不等于证明评价及处理链完全等价。本轮源码核对未发现几何、边界、材料公式或三层映射的生产阻断不匹配，但没有重跑输运；既有直接原子密度锚点审计仅覆盖 `750/620/475 C`，不宣称已逐项验证全部三温度运行时密度相等。参见 [material audit](../d4_reference/material_epoch_audit_result.md)。

依据：[quickstart](D4A_CORRECTED_QUICKSTART.md)、[CE protocol](../d4_reference/d4a_ce_production_protocol.md)、[CE README](../d4_reference/README.md)及上述现有脚本。

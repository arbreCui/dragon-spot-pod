# D4-A 固定径向响应的轴向网格短诊断（2026-09-23）

结果：**原网格基线通过；6-cell 在预声明的 30 秒上限停止，12-cell 未启动。**
本次没有网格收敛结论、没有新的耦合固定点，也没有 SPOT–CE 精度 PASS。

## 固定项与最小改动

输入只读复制自 corrected map 8 portable 的 `candidate_radial.xsm`、
`basis_reference.xsm`、`initial_axial_macrolib.xsm` 与 `candidate_system.xsm`。
固定 rank 2、径向响应及截面、三个 50 cm 温区、150 cm 总高、两端 vacuum、
SN8/constant diamond/SCAT3。仅预声明轴向单元数 3、6、12；不按 CE 调参。
各 case 都由新 GEO→SPOT→ASM FIXB→FLU 自然生成，不修改封存 header。
全部 cold start，EXTE 500，EXTE/UNKT/THER 同为 2e-6，REBA OFF，ACCE 3 3。
没有 SPOLEAK、径向反馈、松弛或经验系数。

候选程序仅将修改后的 SPOASM 单独链接到既有静态库之前。没有调用 make、
修改主库或替换运行中的 canonical Dragon。实验前后核对 canonical、构建输入、
四份原始 XSM 及其复制件 SHA 一致。

## 实际执行

| case | k64 | 墙钟 | 结论 |
|---|---:|---:|---|
| canonical，3 cells | 1.2721209124951036 | 23.83 s | 完成 |
| candidate，3 cells | 1.2721209124951036 | 25.05 s | 完成，k64 与三温区率同值 |
| candidate，6 cells | 无有效结果 | 30 s 上限 | 已停止，无重试 |
| candidate，12 cells | 无 | 未启动 | 不得推断结果 |

两个 3-cell case 的三温区全局归一化 ν-fission 份额同为
`0.259753302, 0.484196691, 0.256050007`。这是 SPORATE 的既有 REAL32 镜像
观测口径及打印精度，不是整个 FLUX64 场逐位一致的声明。
原网格 cold solve 的实际终止：外迭代 13，EEXT=3.21947690e-10、
EUNK=EINR=1.72943430e-6，均按原 solver 门槛完成。

独立只读检查器对每个完成 case 的 370 群逐项比对 13 个径向记录：
NREG2D、NSNAP、POD-NMODE、VOL2D、POD-BASIS、POD-COEFF、RADIAL-OP、
RADIAL-OP64、POD-SIGMA、POD-REC-ERR、POD-ORTHO、DRAGON-TXSC、
DRAGON-S0XSC，全都与 map 8 原系统逐位一致。新 track 的 MAT1D/VOL1D
及 k64/状态 k 一致性也通过。不能把该通过延伸到未完成的 6/12-cell。

原 map 8 暖启动 k=1.2721230284653975；本次相同径向输入的 3-cell 冷启动
相对它的反应性差为 `1e5*(1/k_warm - 1/k_cold)=-0.1307531197 pcm`。
这是本次冷暖启动差异的实测，不是剩余迭代误差上界；未改变终止门槛。
它不能解释此前约 −1868 pcm 的暂态 SPOT–CE 总差异。

## 范围与后续

本次只排除了“FIXB 接口修正改变了原网格 k/径向包”和较大的本次冷暖启动
k 差异。**尚未回答轴向细化是否改善精度。** 6-cell 在 FLU 内超时，没有导出
新轴向态；正常的主 Picard 进程不受影响，既有 maps 9–12 预算保持不变。
不得自动反复启动本诊断或把预设上限当作物理不收敛。需要后续独立、明确
预算的网格实验时，应保留这一失败现场，不复用半成品或改变物理门槛。

入口：[run_d4a_axial_mesh_probe.py](run_d4a_axial_mesh_probe.py)，
[甲板](d4a_axial_mesh_probe.x2m)，[只读检查器](check_d4a_axial_mesh_probe.f90)。
本次现场：`validation/artifacts/d4a-frozen-radial-axial-mesh-probe-20260923`。
`results.json` 只包含两个已完成的 3-cell；`experiment_status.json` 明确整个
网格实验未完成。该目录不属于生产 map、parent 或最终验收输入。

开发预检曾因清单中的 `./` 路径前缀触发 KeyError，当时尚未创建输出目录、
编译或启动求解；修正路径规范化后执行上述唯一一次实验，不是输运重试。

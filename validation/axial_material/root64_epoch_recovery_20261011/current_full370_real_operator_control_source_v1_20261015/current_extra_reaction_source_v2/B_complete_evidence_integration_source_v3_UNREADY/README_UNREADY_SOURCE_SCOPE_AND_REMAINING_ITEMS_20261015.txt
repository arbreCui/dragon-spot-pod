B 完整提取 / 六阶段集成：UNREADY Source 小包（未准入）

已准备：原 extractor、context parser、engine、adapter 和新capture B binding 整文件复制并记录全PF；新worker仅适配完整caps元数据、新capture Host嵌套资源/watchdog和独立操作根。原数学文件字节不变。55 contexts、8 native trees、6 phases完整保留。

正式执行前仍缺：
1. B capture 真正 Root0、完整manifest/binding及独立post0；真实post schema/status/role字段审核。全部future凭证目前NULL。
2. 独立新操作根、完整最新prefix、包含全部历史失败的ledger原始凭证；不可将capture输入binding的旧路径重写为新路径。
3. 原始资源控制器当前实测：整包预留extract512MiB+aggregate320MiB+B OVERV16MiB+Source16MiB=864MiB，连同完整当前累计字节、外部元数据与open-unlinked须低于原2GiB，并保留cold/meta/history/free约束。空间不足先作另行准入的精确已完成ASCII退役/无损归档，不预测可释放字节。
4. Owning Root host、exclusive claim、原OwnRSS/SerialExecutor与原bounded Source绑定、同一完整资源控制器、每阶段600/整体1800/SELF512/一线程一子进程零重试、write-once GEN/publisher/完整24argv/require_escalated。本包没有上述执行入口，不能直接跑现有worker main。
5. 父host须将stage_reservation_binding与真实原resource snapshot精确绑定，并在每阶段前后重新计算全累计。worker子Budget只接收ordinary live metadata；SDK/tool当前7角色由外层精确角色保留，不得将UID0工具或已退役路径塞入ordinary元数据表。
6. 提取actual child2及原FAILED/error记录须如实保留，通过单独Root evidence closure与独立post；aggregate另需真实8对SQL/pool/55context独立全词审核、coverage凭证。不能用完整map或离线结果充当物理通过。
7. B55 OVERV另阶段：本次B最终SQL/pool、ENERGY371、370组每组8 OVERV，原混精度native/integer controls及独立post。A55 control不能替代。当前原engine仍保留SOURCE_CONTEXT_NOT_SAVED事件，不会自动降issue_count。
8. 上述Source和metadata准入完成后，才可正式freeze、Root GEN、独立Source review、pub、Light及实际执行。

本包只作Source/AST/字节逆变换检查；未导入helper、未读/散列科学数据、未编译、未运行native、未GEN/pub、未删除文件。

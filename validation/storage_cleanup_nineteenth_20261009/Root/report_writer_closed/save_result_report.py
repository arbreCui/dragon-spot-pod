from pathlib import Path
import json, hashlib, gzip, shutil, subprocess, runpy

TMP = Path('/private/tmp/spot_storage_nineteenth_root_20261009')
DEST = Path('/Users/wen/spot/validation/storage_cleanup_nineteenth_20261009')
helpers = runpy.run_path(str(TMP/'prepare_review.py'), run_name='pure_metadata_helpers_only')
sha = helpers['sha']

def main():
    post = json.loads((TMP/'postcheck_report.json').read_text())
    assert post['status'] == 'PASS_EXACT_DELETION_WHOLE_REMAINDER_AND_FINAL_STATE_PRESERVATION'
    assert not DEST.exists()
    observation = {
        'cleanup_actual_tool': {'chunk_id': '0a4d34', 'exit_code': 0, 'closed': True},
        'whole_remainder_actual_postcheck_tool': {'chunk_id': '7effa2', 'exit_code': 0, 'closed': True},
        'Root_pre_retirement_joint_actual_tool': {'chunk_id': 'eb8391', 'exit_code': 0, 'closed': True},
        'fixed_plan_sha256': sha(TMP/'fixed_candidate_plan.json'),
        'cleanup_result_sha256': sha(TMP/'cleanup_result.json'),
        'postcheck_report_sha256': sha(TMP/'postcheck_report.json'),
        'scientific_execution': False,
    }
    (TMP/'actual_cleanup_and_postcheck_tool_return.json').write_text(json.dumps(observation, ensure_ascii=False, indent=2)+'\n')
    sources = {
        'Root': TMP,
        'current_dependencies': Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009'),
        'current_native_read_paths': Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009'),
        'result_preservation': Path('/private/tmp/spot_storage_nineteenth_AAA_early_snapshots_preservation_review_20261009'),
        'cache_backup_review': Path('/private/tmp/spot_storage_nineteenth_cache_backup_readonly_20261009'),
    }
    entries = []
    DEST.mkdir()
    for label, source in sources.items():
        target = DEST/label
        target.mkdir()
        for p in sorted(source.iterdir()):
            if not p.is_file() or p.is_symlink():
                continue
            if p.name == 'save_result_report.py':
                continue
            data = p.read_bytes()
            compress = len(data) > 150000 and p.suffix == '.json'
            q = target/(p.name+'.gz' if compress else p.name)
            q.write_bytes(gzip.compress(data, mtime=0) if compress else data)
            restored = gzip.decompress(q.read_bytes()) if compress else q.read_bytes()
            assert restored == data
            entries.append({'source': str(p), 'saved': str(q), 'original_bytes': len(data), 'saved_bytes': q.stat().st_size, 'original_sha256': hashlib.sha256(data).hexdigest(), 'saved_sha256': sha(q), 'lossless_gzip': compress})
    (DEST/'evidence_preservation_manifest.json').write_text(json.dumps({'files': entries, 'count': len(entries), 'all_saved_bytes_or_gzip_inverse_exact': True}, ensure_ascii=False, indent=2)+'\n')
    before_gib = post['before_du_kib']/2**20
    after_gib = post['after_du_kib']/2**20
    text = f'''SPOT 旧迭代文件清理结果（第十九轮，2026-10-09）

本轮实际删除18份旧迭代工作快照及18条关联链接，原分配空间合计3.98907 GiB。清理操作前后项目目录实测从{before_gib:.5f} GiB降到{after_gib:.5f} GiB；保存本报告及核验记录后的读数见Root_actual_storage_closeout.json。

删除范围：
1. axial-material-production-qualified-AB-white-trace-20261004/AAA：map001至map008的closed_snapshots.xsm，约1.77292 GiB。
2. axial-material-production-qualified-AB-rank1-factor-cache-20261007/AAA：map001至map009的closed_snapshots.xsm，约1.99453 GiB。
3. axial-material-production-qualified-AB-compensated-20261004/AAA：map001的closed_snapshots.xsm，约0.22161 GiB。
另删除上述状态在下一轮早期map中的parent_snapshots_closed.xsm链接，共18条；没有删除目录或其他文件。

保留结果：
这三组现有结果文档、数值汇总、全部迭代结果JSON、检查日志、运行日志、源码、参数和输入均留在原位置。各组最后三个closed状态和最后两轮的现存文件及其有效父状态链接继续保留；bootstrap、其他快照、此前失败场景及原精度失败事实保持。
原始材料数据、当前A/B输入、当前声明与准备文件、全部旧恢复主本和97份恢复压缩包保持。常见缓存与备份未发现新增可安全清理项，159份有当前依赖的缓存继续保留。Git历史未清理。

为什么可退役：
18份普通文件的完整内容校验与原SEALED_STAGE_OUTPUTS记录逐份一致，18条链接只服务于这些早期迭代工作状态。当前37,395项读取集合、35,647项输入主本、86组目录约束、186条输入链接及实际运行入口均不读取这36条选定路径；全项目没有未处理的其他指向待删状态的链接。
旧恢复工具及既有删除账本没有把这些状态作为直接复制恢复的唯一主本。现有结果和日志保留，不增加新的物理、耦合或精度通过结论。

重验边界：
本轮未为退役快照建立新的大文件备份。若以后需要重做早期逐阶段的完整文件核验，应在独立目录用保留的原源码、输入和参数重算，并核对原记录后恢复；最终状态不能无损替代早期状态。此前已退役的9份其他阶段文件在原账本中有记录，本轮没有把它们的既有缺席算作新清理，也没有宣称原历史阶段清单当前全部完整。

实际核验：
固定清单36路径均已缺席。其余160,404份已有普通文件、669条链接及7,064个目录路径的保护指纹前后完全相同；当前输入清单、输入图、控制文档与原迭代记录全文校验保持。9份保留closed状态与原阶段记录内容校验一致，最后两轮6条父状态链接仍有效。科学进度、物理参数、阈值和计算程序未修改，本轮没有启动科学计算。

查看清单与证据：
Root/fixed_candidate_plan.json保存逐路径清单、原内容校验和保留边界；Root/cleanup_result.json保存实际删除账本；Root/protected_before.json、protected_after.json及postcheck_report.json保存完整剩余集合核验。current_dependencies/、current_native_read_paths/、result_preservation/、cache_backup_review/保存独立复查资料。较大的审查JSON以无损gzip保存，已核对解压内容与原文件完全一致。
Root_actual_storage_closeout.json保存实际工具退出凭证及最终目录占用。目录占用下降不等于APFS立即释放的独占空闲量。
'''
    (DEST/'REPORT.txt').write_text(text)
    # The destination is excluded only from the old-file preservation comparison.
    plan = json.loads((TMP/'fixed_candidate_plan.json').read_text())
    excluded = {x['path'] for x in plan['regular']+plan['symlinks']}
    baseline = json.loads((TMP/'protected_before.json').read_text())
    final = helpers['inventory'](excluded)
    assert final['counts'] == baseline['counts'] and final['fingerprints'] == baseline['fingerprints']
    for p, h in baseline['control_document_pins'].items():
        assert sha(Path(p)) == h
    closeout = {'status': 'COMPLETE_EXACT_18_EARLY_SNAPSHOTS_AND_18_LINK_RETIREMENT_WITH_RESULTS_PRESERVED', 'deleted_regular': 18, 'deleted_symlinks': 18, 'selected_allocated_gib': post['selected_original_allocated_gib'], 'before_du_kib': post['before_du_kib'], 'after_operation_du_kib': post['after_du_kib'], 'whole_existing_protected_set_preserved_after_report_save': True, 'protected_counts': final['counts'], 'evidence_files': len(entries), 'evidence_inverse_exact': True, 'actual_tools': observation, 'scientific_goal_still_active_not_qualified_by_storage': True, 'business_executed': False}
    q = DEST/'Root_actual_storage_closeout.json'
    q.write_text(json.dumps(closeout, ensure_ascii=False, indent=2)+'\n')
    closeout['final_du_kib_after_report'] = int(subprocess.check_output(['du', '-sk', str(helpers['ROOT'])], text=True).split()[0])
    closeout['final_project_gib'] = closeout['final_du_kib_after_report']/2**20
    closeout['final_net_decrease_gib'] = (closeout['before_du_kib']-closeout['final_du_kib_after_report'])/2**20
    q.write_text(json.dumps(closeout, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': closeout['status'], 'report': str(DEST/'REPORT.txt'), 'final_project_gib': closeout['final_project_gib'], 'final_net_decrease_gib': closeout['final_net_decrease_gib'], 'evidence_files': len(entries)}, ensure_ascii=False))

if __name__ == '__main__':
    main()

import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/wen/spot')
TMP = Path('/private/tmp/spot_storage_seventeenth_root_readonly_20261009')
DEST = ROOT / 'validation/storage_review_seventeenth_20261009'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(path, expected=None):
    data = path.read_bytes()
    if expected is not None:
        assert digest(data) == expected, str(path)
    return json.loads(data)

baseline = load(TMP / 'before.json')
baseline_tool = load(TMP / 'actual_baseline_tool_return.json')
assert baseline_tool['actual_tool_result'] == {
    'initial_chunk_id': '7fef04', 'session_id': None,
    'terminal_chunk_id': '7fef04', 'exit_code': 0, 'closed': True}
assert baseline_tool['baseline_sha256'] == digest((TMP / 'before.json').read_bytes())
assert baseline['counts'] == {'regular': 174519, 'symlink': 687, 'directory_paths': 7031}
assert baseline['project_du_KiB'] == 155928840

groups = [
    ('graph_and_current_binding', Path('/private/tmp/spot_storage_review_seventeenth_graph_20261009'),
     '6ea8bda4f66eaf62912ced5328eded5a1258c98e6eb5b138e15fafe07b9108f4',
     'actual_readonly_tool_return.json',
     '3418234fd7d1eea359d24309d1e627bf75c737b5fa6d0bcfc355cef2ffee49d7',
     {'initial_chunk_id': '85da9f', 'session_id': 16531,
      'terminal_chunk_id': '8b8354', 'exit_code': 0, 'closed': True}),
    ('recovery_and_old_results', Path('/private/tmp/spot_storage_review_seventeenth_recovery_20261009'),
     '84b502a8608b025cd7dbfdcc9125568c8fe405c525c622d2bab8e726c42aeac3',
     'actual_readonly_tool_receipt.json',
     '78d6f2b56aa98e16d834c7e3f8040a5850d1b9969917554d4371a5342a380353',
     {'initial_chunk_id': '268808', 'session_id': None,
      'terminal_chunk_id': '268808', 'exit_code': 0, 'closed': True}),
    ('git_project_build_cache', Path('/private/tmp/spot_storage_review_seventeenth_build_cache_20261009'),
     '0e7685370305044a323a5b1a605a947e7b2d7a465582e77d84b1213194fdac33',
     'actual_readonly_tool_receipt.json',
     'fd6dd4028e2a5a7ea1db8fa111a01f14499ed1f56ad9e4aec26865f78ad3296e',
     {'initial_chunk_id': '995cf8', 'session_id': 37931,
      'terminal_chunk_id': '06faf4', 'exit_code': 0})]

reviewers = []
files = []
for name, directory, report_sha, receipt_name, receipt_sha, actual in groups:
    report = load(directory / 'REPORT.json', report_sha)
    receipt = load(directory / receipt_name, receipt_sha)
    assert report['status'] in ('PASS', 'NO_NEW_SAFE_DELETE_CANDIDATES')
    assert report['approved_deletion_candidates'] == []
    assert report['files_deleted'] == 0 and report['project_written'] is False
    for key, value in actual.items():
        assert receipt['actual_tool_result'][key] == value
    assert type(receipt['actual_tool_result']['exit_code']) is int
    assert receipt['actual_tool_result'].get('closed', receipt.get('closed')) is True
    reviewers.append({'name': name, 'report_sha256': report_sha,
                      'receipt_sha256': receipt_sha, 'actual_tool_result': actual})
    for path in sorted(directory.iterdir()):
        assert path.is_file() and not path.is_symlink()
        data = path.read_bytes()
        assert len(data) < 1024**2
        files.append((path, Path(name) / path.name, data))

for name in ('before.json', 'actual_baseline_tool_return.json',
             'preservation_readonly.py', 'incremental_metadata_screen.json', 'save_review_only.py'):
    path = TMP / name
    files.append((path, Path(name), path.read_bytes()))
assert sum(len(data) for _, _, data in files) < 2 * 1024**2
for rel, sha in baseline['document_sha256'].items():
    assert digest((ROOT / rel).read_bytes()) == sha, rel
assert not DEST.exists()
DEST.mkdir()
copied = []
for source, rel, data in files:
    target = DEST / rel
    target.parent.mkdir(exist_ok=True)
    with target.open('xb') as stream:
        stream.write(data)
    assert digest(target.read_bytes()) == digest(data)
    copied.append({'source': str(source), 'destination': str(target),
                   'sha256': digest(data), 'bytes': len(data)})

report_text = '''SPOT 第十七轮旧文件与存储复查（2026-10-09）

本轮已完成三组独立复查，新增可安全删除项0，实际删除0，已证明回收量0。
项目本轮起始实测约148.7053 GiB，比第十六轮收尾增加60.38 MiB。新增own_rss_binding.json约57.79 MiB，是当前实际绑定结果和后续校核准确路径依赖；配套收据、审查文档和Git也有变化。总量增幅不等同于可回收或独占空间。

逐类结论及保留理由：
1. 两批完整历史输入合计约24.71 GiB；分层和斜向完整数值主数据合计约22.49 GiB，仍被当前输入图、结果复核或后续科学校核引用。最大的60个旧文件与第十六轮逐路径及七项文件身份完全相同，原保留依据没有解除。
2. 当前声明31文件、准备及绑定45文件、终态9文件完整保留。程序、两份运行元数据及声明的4份工作副本虽与主本完全同字节，仍受逐路径清单校验约束，不能因内容重复删除。
3. 159份缓存的完整路径与身份均与第十二/十五/十六轮保留集合一致，逻辑约4.06 MiB、分配约4.32 MiB；没有新增无依赖缓存。已删的64项没有重复计算收益。
4. 14个旧清理目录仍有873份文件。97份永久恢复压缩档合计约2.39 GiB：89份是已退役材料的恢复主本，8份是旧清单的恢复主本，原压缩内容共97个不同组，没有新增可合并副本。恢复工具、映射、账本和被引用的大清单继续保留。
5. 项目本体3016份普通文件与已认可旧基线逐路径及身份相同；编译对象、库及程序仍有直接构建或校核依赖。Git约2.81 GiB，含79份恢复对象和大量未提交工作，没有可安全丢弃的新依据；未执行Git维护。

结果文档与历史事实：
全部原报告、图表、数值结论、完整日志、失败记录、收据、源码、清单和恢复入口保留原位置。原运行失败及原精度FAIL保持。本轮未执行科学业务、恢复原数据或增加任何科学验收信用。
validation/README.md与科学current_progress.json按本轮起始全文SHA保持，不修改索引或科学进度。R16之后此前科学阶段的正常新增和进度更新不被误称为损坏；最终保留检查只比较本轮固定窗口。

核验与结果文件：
graph_and_current_binding/保存当前输入与副本保留依据；recovery_and_old_results/保存恢复包和旧结果资料复查；git_project_build_cache/保存编译、缓存和Git复查。Root_review_evidence_preservation.json列出每份小型证据的原路径、保存路径、全文SHA和真实工具终态。
Root以全项目元数据与路径指纹核对原文件保留；小型控制、结果文档和恢复控制做全文SHA。大科学数据沿用最近完整核验与当前不变身份，不重复读取35GB科学内容，不把存储复查计作科学内容验证。
Git自动本地快照和本轮新报告目录排除在原文件身份比较之外。分配量不等于APFS即时独占空闲量；自然分配变化不记作清理回收。
最终实际收尾结论见Root_actual_preservation_closeout.json。
'''
with (DEST / 'REPORT.txt').open('x') as stream:
    stream.write(report_text)
manifest = {'schema': 'SPOT_R17_ROOT_REVIEW_EVIDENCE_PRESERVATION_V1',
            'status': 'NO_NEW_SAFE_DELETE_CANDIDATES_REPORTS_SAVED_PENDING_FINAL_PRESERVATION_CHECK',
            'independent_actual_reviews': reviewers, 'evidence_copies': copied,
            'report_sha256': digest((DEST / 'REPORT.txt').read_bytes()),
            'files_deleted': 0, 'storage_reclaimed_bytes': 0,
            'original_project_files_modified': False, 'scientific_business_executed': False,
            'copied_large_scientific_payloads': False}
with (DEST / 'Root_review_evidence_preservation.json').open('x') as stream:
    json.dump(manifest, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'status': manifest['status'], 'report': str(DEST / 'REPORT.txt'),
                  'report_sha256': manifest['report_sha256'], 'evidence_copies': len(copied),
                  'copied_evidence_bytes': sum(row['bytes'] for row in copied),
                  'files_deleted': 0, 'storage_reclaimed_bytes': 0}, ensure_ascii=False))

import hashlib
import json
from pathlib import Path
import time

ROOT = Path('/Users/wen/spot')
DEST = ROOT / 'validation/storage_review_sixteenth_20261009'
BASE = Path('/private/tmp/spot_storage_sixteenth_root_readonly_20261009')
GRAPH = Path('/private/tmp/spot_storage_sixteenth_graph_readonly_20261009')
RECOVERY = Path('/private/tmp/spot_storage_sixteenth_recovery_readonly_20261009')

def pin(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    s = p.stat()
    b = p.read_bytes()
    identity = lambda x: [x.st_dev, x.st_ino, x.st_mode, x.st_size, x.st_mtime_ns, x.st_ctime_ns, x.st_nlink]
    assert identity(p.stat()) == identity(s), str(p)
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), identity=identity(s))

g = json.loads((GRAPH / 'REPORT.json').read_bytes())
r = json.loads((RECOVERY / 'REPORT.json').read_bytes())
b = json.loads((BASE / 'before.json').read_bytes())
assert g['status'] == 'PASS' and g['approved_deletion_candidates'] == []
assert r['status'] == 'NO_NEW_SAFE_DELETE_CANDIDATES' and r['approved_delete_paths'] == []
assert pin(GRAPH / 'REPORT.json')['sha256'] == 'ebd5ada6401e63e584cc07b4d801e3e011f3b1407fe0ba3b8785f19244771294'
assert pin(RECOVERY / 'REPORT.json')['sha256'] == 'b262ed38ca260ddaea3795a269fea0e896558972247318e8ff08e8bf2297ff4a'
assert pin(ROOT / 'validation/storage_review_fifteenth_20261009/Root_actual_preservation_closeout.json')['sha256'] == '9f437b45a3d5b21ab96cf5eff5ed909fde37b95e55c4871c8a131a7a5f5b1e87'
fresh = []
for value in g['pins'].values():
    v = pin(Path(value['path']))
    assert v['sha256'] == value['sha256'] and v['bytes'] == value['size_bytes'] and v['identity'] == value['identity']
    fresh.append(v)
for rel, expected in b['document_sha256'].items():
    assert pin(ROOT / rel)['sha256'] == expected
assert g['cache_set']['count'] == 159 and g['cache_set']['new_paths'] == []
assert g['cache_set']['missing_held_paths'] == [] and g['OUTPUT44_inventory_exact43_localfiles_plus_prepared'] is True
assert r['core_no_new_missing_changed_paths_vs_baseline_in_R15_reader'] == dict(added=[], missing=[], changed=[])

DEST.mkdir(exist_ok=False)
copied = []
def copy(p, target):
    original = pin(p)
    with target.open('xb') as stream:
        stream.write(p.read_bytes())
    saved = pin(target)
    assert saved['sha256'] == original['sha256'] and saved['bytes'] == original['bytes']
    copied.append(dict(source=original, saved=saved))

for source, subdir in [(GRAPH, 'graph_and_current_runtime'), (RECOVERY, 'recovery_git_and_project')]:
    target = DEST / subdir
    target.mkdir()
    for p in sorted(source.iterdir()):
        copy(p, target / p.name)
for p in sorted(BASE.iterdir()):
    copy(p, DEST / p.name)
copy(Path('/private/tmp/spot_sixteenth_storage_preservation_readonly_20261009.py'), DEST / 'preservation_readonly.py')
copy(Path(__file__), DEST / 'save_review_only.py')

text = '''SPOT 第十六轮旧产物复查（2026-10-09）

本轮没有找到新增可安全删除项，实际删除0，已证明回收量0。
项目起始实测约148.646 GiB，比第十五轮收尾增加83.19 MiB。新冷启动声明、准备和终态目录合计约79 MiB，是当前校核准确路径依赖，继续保留；余量不凭总占用变化推断具体来源。

逐类复查结果：
1. 新SOURCE的31个文件、准备目录的43个local_files及prepared.json继续被完整清单约束。程序、两份较大元数据及声明副本与主本全文SHA相同，但后续验证仍读取这些准确原路径，不能仅因重复字节删除。
2. 159份缓存与第十二/十五轮的保留集合完全相同，逻辑约4.06 MiB，文件分配约4.32 MiB，没有新增无依赖缓存。
3. 两批完整历史输入合计约24.71 GiB，分层和斜向数值主数据合计约22.49 GiB，当前完整输入与后续科学校核依赖仍在，继续保留。
4. 14个旧清理目录的873份文件约2.57 GiB，包含97份永久恢复压缩档。89份材料档和8份清单档是已退役原文件的恢复来源；原报告、恢复映射、审查源码和受引用大清单继续保留。上一轮已删的9份清单及5份旧程序没有重复计入本轮回收。
5. Git约2.81 GiB，含79份恢复对象及大量未提交工作，没有新的安全丢弃依据。本轮只做只读统计。项目非validation的3016份普通文件与此前保留基线逐项身份相同；编译对象和库仍有准确源码或构建依赖，没有批准整批清空。

结果文档与失败事实：
全部原结果正文、图表、数值结论、日志、失败记录、收据、源码、清单、退休账本及恢复入口保留原位置。旧运行失败与原精度FAIL保持；本轮没有执行求解或增加科学验收信用。
validation/README.md和科学current_progress.json均保持全文SHA与原文件身份，本轮不改索引或科学进度。

检查方式与范围：
Root做全项目元数据与路径指纹，两个独立复查分别检查当前输入/副本/缓存，以及恢复/Git/项目编译依赖。当前小型绑定文件、恢复控制文件及报告做全文SHA复核；科学大文件沿用最近完整核验的身份与当前依赖证据，没有再次全文读取35 GB输入。
Git自动本地快照及本轮新增报告目录排除在原文件身份比较之外。文件分配量不等于APFS即时独占空闲量；永久压缩档分配量的自然观察变化没有计作本轮回收。

本目录保存完整小型复查报告、实际工具终态、全项目指纹及复制映射。保留核对的最终结论见Root_actual_preservation_closeout.json。
'''
with (DEST / 'REPORT.txt').open('x') as f:
    f.write(text)
record = dict(schema='SPOT_SIXTEENTH_ROOT_REVIEW_EVIDENCE_PRESERVATION_V1', observed_unix=time.time(),
              status='NO_SAFE_DELETION_CANDIDATES_DURABLE_REPORTS_SAVED_AFTER_TRUE_READONLY_REVIEWS',
              graph_report_sha256='ebd5ada6401e63e584cc07b4d801e3e011f3b1407fe0ba3b8785f19244771294',
              recovery_report_sha256='b262ed38ca260ddaea3795a269fea0e896558972247318e8ff08e8bf2297ff4a',
              actual_graph_readonly_tool=dict(initial_chunk_id='bb8457', session_id=None, terminal_chunk_id='bb8457', exit_code=0, closed=True),
              actual_recovery_readonly_tool=dict(initial_chunk_id='9007f4', session_id=37315, terminal_chunk_id='8083bd', exit_code=0, closed=True),
              freshly_verified_small_source_and_evidence_pins=fresh, evidence_copies=copied,
              original_project_paths_written=[], files_deleted=0, reclaimed_bytes=0,
              scientific_business_executed=False, no_new_scientific_credit=True)
with (DEST / 'Root_review_evidence_preservation.json').open('x') as f:
    json.dump(record, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps(dict(report=str(DEST / 'REPORT.txt'), preserved_evidence_files=len(copied), freshly_verified_small_pins=len(fresh), files_deleted=0, reclaimed_bytes=0), ensure_ascii=False))

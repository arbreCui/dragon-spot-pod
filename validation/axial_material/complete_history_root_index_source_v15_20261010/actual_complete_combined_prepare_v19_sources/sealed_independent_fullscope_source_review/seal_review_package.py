"""Seal this finite SOURCE review package; no project API or business execution."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).parent
names = (
    'review_script.py', 'REVIEW.json', 'SOURCE_LAST_USE_AND_ALIAS_WITNESSES.json', 'REPORT.txt',
    'ready_append_review_script.py', 'READY_APPEND_REVIEW.json', 'READY_APPEND_REPORT.txt',
    'actual_source_review_tool_returns.json', 'FINAL_REPORT.txt', 'seal_review_package.py')
assert len(names) == len(set(names)) == 10
keys = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')

def read(name):
    path = OUT / name
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    identity = [getattr(before, k) for k in keys]
    assert identity == [getattr(after, k) for k in keys] and len(raw) == before.st_size
    return raw, dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity7=identity)

body_raw, body_pin = read('REVIEW.json')
ready_raw, ready_pin = read('READY_APPEND_REVIEW.json')
assert body_pin['sha256'] == 'ddd09a20482fd407e7ba0b245a5414a46929fadd0bf1f054e051f30c5aa1ea9d'
assert ready_pin['sha256'] == 'b8e9c7ccdf39ab8fcd4d984e593bc814b38965cca25c8085fbe3a296bfdff333'
body, ready = json.loads(body_raw), json.loads(ready_raw)
assert body['status'] == 'SOURCE_PASS_COMPLETE_V19_UNREADY_LAST_USE_ONLY_NO_RUNTIME_CREDIT'
assert ready['status'] == 'SOURCE_PASS_COMPLETE_V19_READY_BINDING_ONLY_NO_RUNTIME_CREDIT'
assert len(body['checks']) == 163 and len(ready['checks']) == 333
assert all(type(v) is bool and v is True for r in (body, ready) for v in r['checks'].values())
assert not body['blocking_findings'] and not ready['blocking_findings']
assert all(type(v) is bool and v is False for r in (body, ready) for v in r['qualification'].values())
receipts = json.loads(read('actual_source_review_tool_returns.json')[0])
for key in ('source_body_independent_review', 'ready_binding_independent_review'):
    receipt = receipts[key]
    actual = receipt['actual_tool_return']
    assert type(actual['exit_code']) is int and actual['exit_code'] == 0
    assert 'session_id' not in actual
    assert receipt['exit_code_typed_integer'] is True and receipt['exit_code_actual_zero'] is True and receipt['no_live_session_reported'] is True
with (OUT / 'FINAL_REPORT.txt').open('x') as f:
    f.write('V19 完整 SOURCE 独立有限复核：SOURCE_PASS，仅源码资格。\n'
            '完整585e /180475B：163项检查、真实工具816a09整数退出0；整文件inverse逐字回V18实际5c4b。原If/Assert/Raise顺序、非minimal调用序列与原3次gc语义边界保持；原codec完整相等检查先于minimal。只有require_ready/create两定义改，其余68、prepare_build和完整V18 INPUT相位字节不变。\n'
            '释放对象真正结束使用；requirements没有caller Load，fresh/new_pins完整codec比较后结束；actual完整两长度检查后结束；audit完整独立snapshot且退出active trace后结束；trim/failed flat-map在全部owner/namespace复制后结束，binding/failed namespace义务保留。后续helper只读原minimal四字段内字段，原两阶段fullEOF/9closure/trace/aliases/全部原谓词与scope保留。\n'
            'READY34ef /180593B：333项检查、真实工具f6a0ed整数退出0；仅doc/status两改，inverse逐字回已独审585e再回5c4b。全70定义、全部其他global和module AST保持，6futureNone、bcd/d490及原caps保持。作者没有用V18独审代替V19独审。\n'
            '未安装或调用project/helper/API/业务，未读取numeric payload/ART，未写canonical/project/ART，未执行资源检查。独立PREP host retarget另行审查；本包不授予PREP/build/INPUT/native/AAA/ABA/物理平衡或目标完成资格。未观测V18 RSS失败具体源码行，未证明或预测V19 RSS成功；仍需真实完整PREP在原512MiB和原全部限额下给出新闭合结果。\n')
members = [read(name)[1] for name in names]
manifest = dict(
    schema='AXMAT_V19_COMPLETE_INDEPENDENT_SOURCE_REVIEW_SEALED_MANIFEST_V1',
    status='SEALED_SOURCE_PASS_COMPLETE_V19_CALLER_AND_READY_BINDING_NO_RUNTIME_CREDIT',
    members=members, member_count=len(members),
    complete_body_review=body_pin, ready_binding_review=ready_pin,
    source_body_checks=163, ready_binding_checks=333, all_496_SOURCE_checks_typed_true=True,
    actual_SOURCE_tools_closed_integer_exit0=True,
    actual_SOURCE_tool_chunk_ids=['816a09', 'f6a0ed'],
    candidate=dict(path='/private/tmp/axmat_v19_complete_combined_READY_source_binding_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py', sha256='34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b', size_bytes=180593),
    complete_585e_body_reviewed=True, READY_two_bindings_reviewed=True,
    scope=dict(project_helper_API_called=False, business_executed=False, numeric_payload_read=False, ART_read_or_written=False, canonical_or_project_written=False, resource_helper_called=False, source_line_RSS_cause_observed=False, actual_RSS_PASS_proved=False, native_AAA_ABA_balance_or_goal_credit=False),
    standalone_PREP_host_review_included=False)
with (OUT / 'sealed_manifest.json').open('x') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    f.write('\n')
for member in members:
    raw, actual = read(Path(member['path']).name)
    assert actual == member
raw, pin = read('sealed_manifest.json')
print(json.dumps(dict(status=manifest['status'], directory=str(OUT), manifest_sha256=pin['sha256'], manifest_bytes=pin['size_bytes'], member_count=10, source_body_review_sha256=body_pin['sha256'], ready_append_review_sha256=ready_pin['sha256'], all_496_SOURCE_checks_typed_true=True, actual_prior_SOURCE_tools_closed_integer_exit0=True, project_helper_API_called=False, business_executed=False, numeric_payload_read=False, ART_read_or_written=False, actual_RSS_PASS_proved=False), indent=2))

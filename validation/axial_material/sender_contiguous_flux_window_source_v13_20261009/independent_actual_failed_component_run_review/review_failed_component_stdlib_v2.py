#!/usr/bin/env python3
"""Read actual FAILED evidence only; never run factory, auditor or raw math gates."""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
from collections import Counter

D = Path('/private/tmp/axmat_v13_actual_component_failed_RUN_independent_review_20261010')
AM = Path('/Users/wen/spot/validation/axial_material')
ART = Path('/Users/wen/spot/validation/artifacts')
O = ART/'axial-material-sender-contiguous-flux-window-build-v13-20261009'
S = ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009'
T = ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009'
F = AM/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
R = AM/'sender_contiguous_flux_window_source_v13_20261009/actual_component_execution_receipts/Root_actual_failed_run_tool_return.json'
PREP = Path('/private/tmp/axmat_v13_actual_component_PREP_declaration_independent_review_20261009')
pins = {}

def ident(p):
    x=p.lstat()
    return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]

def hash_file(p):
    p=Path(p)
    before=ident(p)
    assert stat.S_ISREG(before[2]) and before[3]==1, str(p)
    h=hashlib.sha256()
    with p.open('rb') as stream:
        for part in iter(lambda:stream.read(4*1024*1024),b''):h.update(part)
    assert ident(p)==before, str(p)
    value={'path':str(p),'sha256':h.hexdigest(),'size_bytes':before[4],'identity':before}
    pins[str(p)]=value
    return value

def read(p,want=None):
    value=hash_file(p)
    if want is not None:assert value['sha256']==want, str(p)
    return json.loads(Path(p).read_text())

def tree_ids(root):
    root=Path(root)
    result={}
    for p in [root,*sorted(root.rglob('*'))]:
        i=ident(p)
        assert stat.S_ISDIR(i[2]) or (stat.S_ISREG(i[2]) and i[3]==1), str(p)
        result[str(p.relative_to(root))]=i
    return result

def save(name,data):
    (D/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

D.mkdir(exist_ok=True,parents=True)
initial_output_ids=tree_ids(O)
initial_source_ids=tree_ids(S)
initial_terminal_ids=tree_ids(T)
failed=read(T/'failed_terminal_return.json','563cfe132989daed8de2a10ca539fa0892f348941c659557246155b0a64569fa')
actual=read(R,failed['Root_actual_tool_return']['sha256'])
assert type(actual['terminal']['exit_code']) is int and actual['terminal']['exit_code']==1
assert actual['initial']['chunk_id']=='b76b46' and actual['initial']['session_id']==34813
assert actual['terminal']['chunk_id']=='176835' and 'session_id' not in actual['terminal']
assert actual['actual_tool_terminal_return_observed'] is True and actual['session_closed'] is True
assert type(failed['returncode']) is int and failed['returncode']==1
assert failed['actual_tool_result']=={'initial_chunk_id':'b76b46','session_id':34813,'terminal_chunk_id':'176835','exit_code':1}
assert failed['record_written_after_actual_terminal_return'] is True
assert actual['input']['argv']==failed['command']
factory_pin=hash_file(F)
assert factory_pin['sha256']==failed['source']['sha256']=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
decl=read(O/'declaration.json',failed['declaration']['sha256'])
assert failed['declaration']['sha256']=='ccdbad6c0e6d767ee98b9e7287c5f3be8120604f57069730289bbd761b947b0f'
driver=read(O/'driver_result.json',failed['driver_result']['sha256'])
stages=read(O/'SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13/stages.json',failed['stages']['sha256'])['stages']
watch=read(O/'audit/audit.watchdog.json',failed['last_audit_watchdog']['sha256'])
for k in ['full_stdout','full_stderr','last_audit_log']:
    v=failed[k]
    assert hash_file(v['path'])['sha256']==v['sha256']
assert (T/'full_stdout.json').stat().st_size==0
stderr=(T/'full_stderr.txt').read_text()
assert 'own-child wall cap reached' in stderr and 'whole build wall budget exceeded' in stderr
assert (O/'audit/audit.log').stat().st_size==0
assert driver['classification']=='FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_NO_RETRY'
assert 'whole build wall budget exceeded' in driver['error']
assert driver['elapsed_seconds']==failed['driver_elapsed_seconds']==1816.2817324589705
assert driver['elapsed_seconds']>=1800
assert {x:decl[x] for x in ['total_wall_seconds','stage_wall_seconds','rss_cap_mib','numeric_children_at_once','retries','archive_reserve_bytes','artifact_budget_bytes','min_free_bytes']}=={
    'total_wall_seconds':1800,'stage_wall_seconds':600,'rss_cap_mib':512,'numeric_children_at_once':1,'retries':0,
    'archive_reserve_bytes':2147483648,'artifact_budget_bytes':103079215104,'min_free_bytes':8589934592}
assert type(decl['threads']) is int and decl['threads']==1
assert all(k+'=1' in actual['input']['cmd'] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'])

prep_report=read(PREP/'REPORT.json','bb2fe51788110ea9d4ff580a28aeda2c4688ac62c94a961918e000a69152ca34')
prep_receipt=read(PREP/'actual_readonly_tool_return.json','026dcafc69f9607f79b6418e2c166c316c8ce3db0cc891a65d969da8229cd9cf')
plan=read(PREP/'complete_declaration_stage_recipe_and_source_evidence.json')
assert prep_report['status'].startswith('PASS')
assert len(stages)==len(plan['full86_stage_plan'])==86
stage_summaries=[]
resources=[]
for i,(s,p) in enumerate(zip(stages,plan['full86_stage_plan'])):
    assert s['label']==p['label'] and s['command']==p['command']
    assert 0<s['wall_cap_seconds']<=600
    w=read(O/(s['label']+'.watchdog.json'))
    log=hash_file(O/(s['label']+'.log'))
    assert w['command']==s['command']
    assert type(w['pid']) is int and w['pid']>0 and type(w['returncode']) is int
    assert w['own_child_only'] is True and w['liveness_group_cleanup'] is True
    assert w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512
    assert 0<w['wall_cap_seconds']<=s['wall_cap_seconds']
    if i<85:
        assert w['returncode']==p['expected_returncode']
        assert w['limit_failure'] is None and 0<=w['elapsed_seconds']<w['wall_cap_seconds']
        assert s['status']==('PASS' if p['expected_returncode']==0 else 'FAILED')
        if s['status']=='PASS':assert s['log_sha256']==log['sha256']
    else:
        assert p['expected_returncode']==0 and s['status']=='FAILED'
        assert w['returncode']==-15 and w['limit_failure']=="RuntimeError('own-child wall cap reached')"
        assert s['wall_cap_seconds']==34.87850716605317 and w['wall_cap_seconds']==33.39447033306351
        assert w['elapsed_seconds']==33.50602420902578 and w['sampled_peak_rss_mib']==76.125
        assert s['elapsed_seconds']==34.999609916005284
    for key in ['resource_before','resource_after']:
        if key in s:
            r=s[key]
            assert r['artifact_budget_bytes']==103079215104 and r['min_free_bytes']==8589934592
            assert r['artifact_bytes']<r['artifact_budget_bytes'] and r['disk_free_bytes']>r['min_free_bytes']
            assert r['declared_resource_roots']==decl['resource_roots']
            assert set(r['declared_resource_roots'])<=set(r['resource_roots'])
            resources.append({'stage_index':i+1,'epoch':key,'artifact_bytes':r['artifact_bytes'],'regular_files':r['regular_files'],'disk_free_bytes':r['disk_free_bytes'],'checked_unix':r['checked_unix']})
    stage_summaries.append({'index':i+1,'label':s['label'],'status':s['status'],'expected_returncode':p['expected_returncode'],'actual_returncode':w['returncode'],'recorded_stage_wall_cap_seconds':s['wall_cap_seconds'],'actual_child_wall_cap_seconds':w['wall_cap_seconds'],'child_elapsed_seconds':w['elapsed_seconds'],'sampled_peak_rss_mib':w['sampled_peak_rss_mib'],'limit_failure':w['limit_failure'],'watchdog_sha256':pins[str(O/(s['label']+'.watchdog.json'))]['sha256'],'log_sha256':log['sha256']})
assert Counter(s['status'] for s in stages)=={'PASS':61,'FAILED':25}
assert Counter(s['expected_returncode'] for s in plan['full86_stage_plan'][:-1])=={0:61,23:20,1:4}
assert failed['stage_status_counts']=={'PASS':61,'FAILED':25}
assert failed['completed_before_final_audit']==85
r=driver['resources']
assert r['artifact_bytes']==73053417775 and r['disk_free_bytes']==208591114240
assert r['artifact_budget_bytes']==103079215104 and r['min_free_bytes']==8589934592
assert r['artifact_bytes']<103079215104 and r['disk_free_bytes']>8589934592
assert r['declared_resource_roots']==decl['resource_roots']

# Byte preservation of SOURCE and built artifacts is evidence, never admission.
assert decl['source_inventory']['symlinks']=={}
assert set(decl['source_inventory']['files'])==set(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
for name,sha in decl['source_inventory']['files'].items():
    q=S/name
    v=hash_file(q)
    assert v['sha256']==sha
    baseline=plan['frozen_file_fullSHA_and_7identity'][str(q)]
    assert v['sha256']==baseline['sha256'] and v['identity']==baseline['identity']
build=read(O/'runtime/build_identity.json')
assert len(build['files'])==12 and build['sole_new_production_overrides']==['SPOT1P64.o','FLU2DR64.o']
for name,sha in build['files'].items():assert hash_file(O/name)['sha256']==sha

# Retain exact tree, file hashes, byte sizes, raw manifests; do not decode FP.
raw=read(O/'raw_sender_controls_receipt.json')
oldraw=read(O/'raw_controls_receipt.json')
assert oldraw['before_numeric_gates'] is True and oldraw['declared_control_contract']==decl['control_contract']
assert raw['before_numeric_gates'] is True and raw['raw_identity_before_after_equal'] is True
assert raw['declared_sender_control_contract']==decl['sender_control_contract']
sender_ids=tree_ids(O/'sender_controls')
assert sender_ids==raw['raw_identity_snapshot']
case_summaries=[]
rawcount=rawbytes=0
all_names=set()
for c in decl['sender_control_contract']['cases']:
    root=O/'sender_controls'/c['name']
    assert {p.name for p in root.iterdir()}==set(c['strict_case_namespace'])
    assert all(p.is_file() and not p.is_symlink() for p in root.iterdir())
    for p in root.iterdir():
        rel=str(p.relative_to(O));all_names.add(rel)
        assert hash_file(p)['sha256']==raw['files'][rel]
    for b in c['raw_files']:
        q=root/b['name']
        assert q.stat().st_size==b['size_bytes']
        rawcount+=1;rawbytes+=b['size_bytes']
    manifest=root/'wrapper_manifest.jsonl'
    lines=[json.loads(x) for x in manifest.read_text().splitlines()]
    assert len(lines)==c['manifest_lines']
    if c['negative']:
        assert c['expected_message'] in (root/'execute.log').read_text()
    case_summaries.append({'name':c['name'],'expected_returncode':c['expected_returncode'],'actual_returncode':json.loads((root/'execute.watchdog.json').read_text())['returncode'],'namespace_matches_contract':True,'raw_count':len(c['raw_files']),'raw_bytes':sum(b['size_bytes'] for b in c['raw_files']),'JSONL_lines_preserved':len(lines),'JSONL_truth_flags_are_original_self_reports_not_independent_numeric_acceptance':True})
assert len(all_names)==112 and set(raw['files'])==all_names
assert rawcount==70 and rawbytes==288241824

absent=[O/'seal.json',O/'audit/result.json',O/'runtime/compiled_unit_controls.json',O/'closeout_failure.json',T/'terminal_return.json',T/'declaration_terminal_return.json']
# This component's PREP is recorded under AM source receipts, not success TERM.
assert all(not os.path.lexists(p) for p in absent)
for key in ['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']:
    assert actual[key] is None and failed[key] is None
for key in ['component_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:
    assert actual[key] is False and failed[key] is False
assert failed['build_seal'] is None and actual['build_seal_present'] is False
assert not any(x in driver for x in ['control_counts','sender_window_control_counts','sender_window_controls_passed','all_new_cache_outputs_bitwise_equal_to_uncached'])
assert all(driver[x] is False for x in ['actual_full_FLU_entry_executed','transport_launched','AAA_accuracy_qualified','ABA_admitted'])

# Pin the real guard source and statements that explain two distinct clocks.
source=F.read_text();tree=ast.parse(source)
run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_build')
run_text=ast.get_source_segment(source,run)
assert 'remaining = TOTAL_WALL - (time.monotonic()-started)' in run_text
assert 'runner = full.OwnRSSSerialExecutor(OUT, remaining, FAMILY, resources)' in run_text
assert 'if actual_size >= ARCHIVE_RESERVE or elapsed >= TOTAL_WALL:' in run_text
serial_path=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
serial=serial_path.read_text();hash_file(serial_path)
assert 'limit = min(float(cap), remaining)' in serial
assert 'process_limit = min(limit - (time.monotonic() - started), self.deadline - time.monotonic())' in serial
rss_path=AM/'qualify_refined_AAA_layered_full.py';rss_text=rss_path.read_text();hash_file(rss_path)
assert "if now-started>=limit:raise RuntimeError('own-child wall cap reached')" in rss_text
assert "if peak>=512:raise RuntimeError('own-child 512 MiB RSS cap reached')" in rss_text
assert 'self.bounded.terminate_group(process)' in rss_text

assert tree_ids(O)==initial_output_ids and tree_ids(S)==initial_source_ids and tree_ids(T)==initial_terminal_ids
for v in pins.values():assert ident(Path(v['path']))==v['identity']
save('actual_failed_RUN_complete_stage_raw_byte_evidence.json',{
    'schema':'AXMAT_V13_ACTUAL_FAILED_COMPONENT_STAGES_AND_RAW_PRESERVATION_V1',
    'source_and_file_fullSHA_7identity':pins,'stage_observations':stage_summaries,
    'sender_case_preservation_observations':case_summaries,'resource_epoch_observations':resources,
    'output_namespace_7identity_before_after':initial_output_ids,
    'source_namespace_7identity_before_after':initial_source_ids,
    'terminal_namespace_7identity_before_after':initial_terminal_ids,
    'absent_success_artifact_paths':[str(p) for p in absent],
    'raw_control_receipt_files_count':len(oldraw['files']),
    'raw_original_controls_all_bytes_not_reaudited':True,
    'full70_sender_raw_bytes_hashed_not_float_decoded':True})
report={
    'schema':'AXMAT_V13_ACTUAL_FAILED_COMPONENT_INDEPENDENT_REVIEW_V1','status':'PASS_ACTUAL_FAILURE_EVIDENCE_ONLY',
    'actual_Root_tool_terminal':{'initial_chunk_id':'b76b46','session_id':34813,'terminal_chunk_id':'176835','exit_code':1,'exit_code_type':'int','closed':True},
    'factory_sha256':factory_pin['sha256'],'declaration_sha256':failed['declaration']['sha256'],
    'Root_failed_terminal_sha256':pins[str(T/'failed_terminal_return.json')]['sha256'],
    'Root_actual_tool_receipt_sha256':pins[str(R)]['sha256'],
    'driver_result_sha256':pins[str(O/'driver_result.json')]['sha256'],
    'full_stage_count':86,'normal_PASS_stages':61,'expected_keycodec_rc23_FAILED_stages':20,
    'expected_sender_rc1_FAILED_stages':4,'unexpected_terminal_audit_FAILED_stages':1,
    'actual14_sender_modes_returned_declared_rc':True,'full12_build_stages_returned0':True,
    'original68_controls_not_qualified_without_original_final_audit':True,
    'original_caps':{'whole_seconds':1800,'stage_seconds':600,'OwnRSS_MiB':512,'threads':decl['threads'],'children_at_once':1,'retries':0,'archive_reserve_bytes':2147483648,'history_budget_bytes':103079215104,'min_free_bytes':8589934592},
    'final_audit':{'stage_wall_cap_seconds':34.87850716605317,'child_wall_cap_seconds_after_resource_check':33.39447033306351,'child_elapsed_seconds':33.50602420902578,'stage_elapsed_seconds':34.999609916005284,'sampled_peak_rss_mib':76.125,'pid':watch['pid'],'returncode':-15,'limit_failure':watch['limit_failure'],'own_child_only':True,'liveness_group_cleanup':True},
    'driver_elapsed_seconds':driver['elapsed_seconds'],'driver_error':driver['error'],
    'failure_cause':'child whole-deadline remainder exhausted; final factory whole-wall rejection preserved; not RSS cap rejection',
    'full_stdout_size_bytes':0,'full_stderr_size_bytes':(T/'full_stderr.txt').stat().st_size,
    'source15_fullSHA_and_inherited_PREP_7identities_unchanged':True,
    'all12_built_artifact_fullSHA_equal_runtime_identity_record':True,
    '70_sender_raw_file_count':70,'sender_raw_bytes':288241824,'112_sender_case_files_fullSHA_exact_original_raw_receipt':True,
    'sender_full_tree127_7identities_exact_raw_archival_snapshot':True,
    'raw_numeric_math_bitwise_finite_LOC_carry_acceptance_executed_by_this_review':False,
    'original_positive_JSONL_PASS_flags_are_selfreports_only':True,
    'audit_result_seal_success_terminal_absent':True,'four_success_tail_fields':None,
    'component_qualified':False,'combined_qualified':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,
    'business_imported':False,'factory_auditor_called':False,'numerical_controls_compiler_started':False,'Root_handle_polled':False,'project_written':False,
    'audit_retried':False,'budget_changed':False,
    'scope_limit':'Preservation and actual failure semantics only. No postterminal replacement acceptance or component qualification. Historical 35GB graph and all original raw math controls not reexecuted.',
    'evidence_files':['actual_failed_RUN_complete_stage_raw_byte_evidence.json'],
    'transparent_readonly_exploration_error':{'chunk_id':'518b35','exit_code':1,'reason':'assumed actual_component_execution_receipts under ART SOURCE; actual receipt is under AM sender source; no business called'},
    'actual_readonly_tool_terminal_return':None}
save('REPORT.json',report)
(D/'REPORT.txt').write_text('V13 实际组件失败已核实。Root 原运行 b76b46 / 34813 → 176835，整数退出 1、已关闭。\n'
    '86 阶段：61 正常 PASS、20 keycodec 预期退出 23、4 sender 预期退出 1；最后独立审核阶段实际 FAILED。\n'
    '审核 child 剩余时限 33.394470333 秒，采样 RSS 76.125 MiB，退出 -15，own-group 清理真实完成。总 driver 1816.281732459 秒超过原 1800 秒，预算未变。\n'
    '12 编译/链接实际返回 0、14 sender 模式均按原合同返回；70 原始二进制共 288241824 字节、全部 112 sender 文件的原存档 SHA 和 127 节点身份保持。这里只核保留字节，不补跑数值/LOC/bitwise 审核。\n'
    '正式 audit result、seal、success terminal、四收尾字段均缺失。原 JSONL 自报 PASS 不能替代最终审核。组件、combined、native RSS、AAA/ABA 均未准入。\n'
    '源码 15 件 SHA/原 PREP 身份未变。只读脚本未导入业务、不执行控制/编译/审核、未轮询 Root、未修改项目。初次目录浏览路径误猜的只读退出 1 已透明列明。\n')
print(json.dumps({'status':report['status'],'REPORT_path':str(D/'REPORT.json'),'REPORT_sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),'component_qualified':False,'stage_count':86,'sender_raw_count':70,'sender_raw_bytes':rawbytes,'all_read_files_before_after_identity_equal':True},ensure_ascii=False))

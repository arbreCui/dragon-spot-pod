"""Actual original native failure postreview: stdlib metadata/bytes only."""
import ast
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import time

D=Path('/private/tmp/axmat_v9_actual_native_failed_graph_resource_independent_review_20261009')
ART=Path('/Users/wen/spot/validation/artifacts')
W=ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
S=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
R=Path('/Users/wen/spot/validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009')
G=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')
B=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
START=time.monotonic();PINS={}

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p,wanted=None):
    p=Path(p);before=identity(p)
    assert stat.S_ISREG(before[2]) and p.resolve(strict=True)==p,str(p)
    if str(p) in PINS:
        row=PINS[str(p)]
        assert row['identity']==before and (wanted is None or row['sha256']==wanted),str(p)
        return row
    h=hashlib.sha256()
    with p.open('rb')as f:
        assert [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino]==before[:2]
        while block:=f.read(4*2**20):h.update(block)
    assert identity(p)==before,str(p)
    row=dict(path=str(p),identity=before,bytes=before[3],sha256=h.hexdigest())
    assert wanted is None or row['sha256']==wanted,str(p)
    PINS[str(p)]=row;return row

def unique_pairs(items):
    value={}
    for k,v in items:
        assert k not in value
        value[k]=v
    return value

def read(p,wanted=None):
    row=pin(p,wanted)
    value=json.loads(Path(p).read_bytes(),object_pairs_hook=unique_pairs,
                     parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))
    assert identity(p)==row['identity']
    return value

def canonical_pieces(value):
    return json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value)

def digest(value):
    h=hashlib.sha256()
    for text in canonical_pieces(value):h.update(text.encode('utf-8'))
    return h.hexdigest()

root=read(R/'Root_actual_V9_cold_failure_tool_return.json','5a8601cbf5ae42cd397afc59bb990a3f09b3645dc94d8ec1acc1c8c79026eaee')
assert root['actual_tool_result']==dict(initial_chunk_id='cefa98',session_id=53935,terminal_chunk_id='afac4e',exit_code=1,closed=True)
assert type(root['actual_tool_result']['exit_code']) is int and root['successful_recorder_executed'] is False
receipt=read(T/'cold_failed_terminal_return.json','89e9c3d69d7d7e1f80934a5a3415525d3aba02d4808ea98e00ce775b67c80502')
assert receipt['actual_tool_result']=={k:v for k,v in root['actual_tool_result'].items()if k!='closed'}
assert receipt['closed'] is True and type(receipt['returncode'])is int and receipt['returncode']==1
assert receipt['actual_tool_terminal_return_observed']is True and receipt['record_written_after_actual_terminal_return']is True
assert receipt['record_producer']=='root' and receipt['transport_started'] is True
for key in ('full_stdout','full_stderr','source_failure','actual_run_status','actual_stages','failed_stage_watchdog','failed_stage_full_log','original_prepared_cold','input_declaration_terminal_evidence'):
    row=receipt[key];assert pin(row['path'],row['sha256'])['bytes']==row['bytes']
assert receipt['full_stdout']['bytes']==0 and receipt['full_stderr']['bytes']==3643
assert b'own-child 512 MiB RSS cap reached' in Path(receipt['full_stderr']['path']).read_bytes()
assert all(receipt[k]is False and root[k]is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'))

g=read(G/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba')
b=read(B/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
assert g['status']==b['status']=='PASS'
old=read('/private/tmp/axmat_v9_native_launch_boundary_source_check_20261009/REPORT.json','b98654a48279a04c15f040c0dea92f3e5a644bfa3f1262013e3ad726f170cbd6')
assert receipt['original_launch_command']==old['external_source_derived_cli']
prepared=read(W/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
assert prepared['budgets']==old['original_budgets']
pin(W/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
m=read(S/'rank1_factor_cache_admission.json','564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742')
binding=read(W/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
expected=dict(m['files']);assert set(expected).isdisjoint(b['additional_expected_files'])
expected.update(b['additional_expected_files'])
assert len(m['files'])==37339 and len(expected)==37395 and expected==binding['files']
assert digest(expected)==g['expected_map_sha256']
metadata_before={p:identity(p)for p in m['files']}
assert digest(metadata_before)==g['metadata37339_beforeafter_identity_digest']
extra_before={p:pin(p,sha)['identity']for p,sha in b['additional_expected_files'].items()}
assert len(extra_before)==56 and digest(extra_before)==b['additional_before_after_identity_digest']
gp=g['graph_whole_pin'];graph=read(gp['path'],gp['sha256']);assert identity(gp['path'])==gp['identity']
assert gp['sha256']=='0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
canonical={r['path']:r['sha256']for r in graph['canonical_files']}
assert len(canonical)==35647 and all(expected[p]==sha for p,sha in canonical.items())
canon_before={p:identity(p)for p in canonical}
assert digest(canon_before)==g['canonical_full_seven_field_beforeafter_digest']

# Compile/execute only independently reviewed filesystem/metadata utility defs.
# No business module, original producer/helper or controller is imported.
utility=G/'review_actual_controls_graph_resources_readonly.py';upin=pin(utility)
tree=ast.parse(utility.read_text())
want={'current_graph_namespace','aliases_and_absences','dynamic_roots','root_validation','resource_inventory','decode_rows'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in want]
assert {n.name for n in nodes}==want
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(utility),'exec'),globals())
ns=[current_graph_namespace(r,canonical)for r in graph['namespaces']]
aa=aliases_and_absences(graph,canonical)
assert len(ns)==86 and ns==g['namespaces86_beforeafter'] and aa==g['aliases186_absences445_beforeafter']
row_count=sum(1 for _ in decode_rows(graph['requirements']))
assert row_count==235528
roots=dynamic_roots(prepared['resource_roots'],ART)
assert len(roots)==236 and roots==prepared['resource_roots']==binding['resource_info']['resource_roots']
resources_before=resource_inventory(roots,ART);free_before=shutil.disk_usage(ART).free
assert resources_before['artifact_bytes']<96*2**30 and free_before>8*2**30

stages=read(receipt['actual_stages']['path'],receipt['actual_stages']['sha256'])['stages']
status=read(receipt['actual_run_status']['path'],receipt['actual_run_status']['sha256'])
failure=read(receipt['source_failure']['path'],receipt['source_failure']['sha256'])
assert [s['label']for s in stages]==old['first_nine_original_stages'][:7]
assert [s['status']for s in stages]==['PASS']*6+['FAILED']
assert status['classification']=='FAILED_NO_RETRY' and status['completed_maps']==0 and status['cases']=={}
assert status['prepared_sha256']==receipt['original_prepared_cold']['sha256']
assert status['resource_roots']==roots and status['wall_cap_seconds_per_case']==43200
assert failure['classification']=='FAILED_COMBINED_COLD_NO_RETRY'
assert 0<failure['actual_elapsed_seconds']<43200
assert all(failure[k]is False for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted'))
budgets=[120,120,120,120,120,120,4200]
watch_rows=[];stage_log_bytes=0
for number,(s,cap)in enumerate(zip(stages,budgets)):
    label=s['label'];log=W/(label+'.log');watch=read(W/(label+'.watchdog.json'))
    lp=pin(log,s['log_sha256']if number<6 else receipt['failed_stage_full_log']['sha256'])
    stage_log_bytes+=lp['bytes']
    assert watch['command']==s['command'] and 0<watch['wall_cap_seconds']<=s['wall_cap_seconds']<=cap
    assert 0<=watch['elapsed_seconds']<=s['elapsed_seconds']<s['wall_cap_seconds']
    assert watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512
    assert watch['rss_peak_observation_contract']=='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'
    assert type(watch['live_rss_sample_count'])is int and watch['live_rss_sample_count']>=0
    observed=watch['observed_peak_rss_mib'];sampled=watch['sampled_peak_rss_mib'];kernel=watch['own_pid_wait4_peak_rss_mib']
    assert all(type(x)in(int,float)and math.isfinite(x)and x>=0 for x in (sampled,observed))
    assert observed==max(sampled,kernel if kernel is not None else 0)
    if number<6:
        assert watch['returncode']==0 and type(watch['returncode'])is int and watch['limit_failure']is None
        assert watch['own_pid_wait4_observed']is True and watch['own_pid_wait4_pid']==watch['pid']
        raw=watch['own_pid_wait4_ru_maxrss_bytes'];exitstatus=watch['own_pid_wait4_status']
        assert type(raw)in(int,float)and math.isfinite(raw)and raw>0 and raw==int(raw)
        assert type(exitstatus)is int and os.WIFEXITED(exitstatus) and os.waitstatus_to_exitcode(exitstatus)==0
        assert kernel==raw/2**20 and 0<observed<512
    else:
        assert watch['pid']==35128 and watch['returncode']==-15 and watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"
        assert sampled==observed==513.890625 and watch['live_rss_sample_count']==580
        assert watch['own_pid_wait4_observed']is False
        assert all(watch[k]is None for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'))
        assert 'log_sha256'not in s and 'resource_after'not in s
    for key in ('resource_before','resource_after'):
        if key not in s:continue
        snap=s[key]
        assert snap['resource_roots']==roots and snap['artifact_budget_bytes']==96*2**30 and snap['min_free_bytes']==8*2**30
        assert snap['artifact_bytes']<96*2**30 and snap['disk_free_bytes']>8*2**30 and 'reason'not in snap
    watch_rows.append(dict(label=label,stage_status=s['status'],stage_elapsed=s['elapsed_seconds'],wall_cap=s['wall_cap_seconds'],raw_watch=watch,raw_log=lp))

# Whole new output bytes, including failed unsealed partial files; old aliases
# are validated through the immutable expected input union without rehashing.
new_namespace={};new_roots=[]
for name in ('archives','training','AAA'):
    rootpath=W/name;files={};links={};dirs=[]
    for p in sorted(rootpath.rglob('*')):
        rel=str(p.relative_to(W))
        if p.is_symlink():
            target=p.resolve(strict=True);links[rel]=dict(identity=identity(p),text=os.readlink(p),target=str(target))
            if str(target)in expected:links[rel]['expected_target_sha256']=expected[str(target)]
            else:
                assert W in target.parents and target.is_file(),str(p)
                links[rel]['new_target_sha256']=pin(target)['sha256']
        elif p.is_dir():dirs.append(rel)
        else:files[rel]=pin(p)
    new_namespace[name]=dict(files=files,symlinks=links,directories=dirs)
    new_roots.append(dict(path=str(rootpath),regular_files=len(files),regular_bytes=sum(r['bytes']for r in files.values()),symlinks=len(links),directories=len(dirs)))
sealed=[]
for name in ('archives','training'):
    folder=W/name;seal=read(folder/'result.json')
    assert seal['classification']=='SEALED_STAGE_OUTPUTS' and type(seal['sha256'])is dict
    actual={p.name for p in folder.iterdir()if p.is_file()and p.name!='result.json'}
    assert set(seal['sha256'])==actual
    for base,sha in seal['sha256'].items():
        assert Path(base).name==base
        p=folder/base;target=p.resolve(strict=True)
        if p.is_symlink():
            if str(target)in expected:assert expected[str(target)]==sha
            else:
                assert W in target.parents and str(target)in PINS,str(p)
                assert PINS[str(target)]['sha256']==sha,str(p)
        else:pin(p,sha)
    sealed.append(dict(path=str(folder/'result.json'),pin=PINS[str(folder/'result.json')],all_original_seal_outputs_SHA_exact=True))
absent_success=[W/'cold_source_complete_result.json',W/'cold_closeout_seal.json',T/'terminal_return.json',W/'AAA/bootstrap/result.json',W/'AAA/map001',W/'ABA']
assert all(not os.path.lexists(p)for p in absent_success)
assert not any(p.name.startswith('map')for p in (W/'AAA').iterdir())
assert all(k not in failure and k not in receipt for k in ('full_closeout_tail_gate','actual_archive_bytes','actual_resources'))

assert metadata_before=={p:identity(p)for p in m['files']}
assert extra_before=={p:identity(p)for p in b['additional_expected_files']}
assert canon_before=={p:identity(p)for p in canonical}
assert ns==[current_graph_namespace(r,canonical)for r in graph['namespaces']]
assert aa==aliases_and_absences(graph,canonical)
resources_after=resource_inventory(roots,ART);assert resources_after==resources_before
for p,row in PINS.items():assert identity(p)==row['identity'],p

report=dict(
    schema='AXMAT_V9_ACTUAL_ORIGINAL_NATIVE_FAILED_GRAPH_RESOURCES_STAGES_COMPLETE_SCOPE_REVIEW_V1',status='PASS_ACTUAL_FAILURE_EVIDENCE_ONLY',
    Root_actual_native_tool=root['actual_tool_result'],Root_failed_receipt=PINS[str(T/'cold_failed_terminal_return.json')],
    actual_failure_classification=failure['classification'],actual_controller_classification=status['classification'],
    actual_initial_stage_count=7,actual_completed_initial_stages=6,actual_completed_maps=0,
    all_seven_stage_raw_watch_and_full_log=watch_rows,all_seven_raw_log_bytes=stage_log_bytes,
    failed_own_PID=35128,failed_observed_peak_rss_mib=513.890625,original_rss_cap_mib=512,
    failed_returncode=-15,failed_wait4_unobserved_four_None_preserved=True,failed_stage_has_no_PASS_only_logSHA_or_resource_after=True,
    full_stdout_bytes=0,full_stderr_bytes=3643,
    canonical35647_full_seven_identity_digest=digest(canon_before),canonical35803098221_fullSHA_inherited_with_unchanged_identities=True,new_old35GB_payload_reads=0,
    metadata37339_full_seven_identity_digest=digest(metadata_before),expected37395_complete_map_digest=digest(expected),
    extra56_fresh_fullSHA_identity_digest=digest(extra_before),graph_full_current_wire_pin=PINS[gp['path']],all235528_wire_rows_independently_decoded=True,
    exhaustive86_namespaces=ns,aliases186_absences445=aa,
    declared231_graph_roots_unchanged_with_exact_whole_graph_pin=True,current_dynamic236_resource_roots=roots,current_dynamic_resource_beforeafter=resources_after,
    disk_free_before=free_before,original96GiB_history_and8GiB_free_gates_retained=True,resource_observations_not_old_frozen_count_gate=True,
    all_new_native_partial_outputs_wholeSHA=new_namespace,all_new_native_output_counts=new_roots,
    two_completed_original_directory_seals_fullSHA=sealed,bootstrap_partial_files_unsealed_and_not_qualified=True,
    actual_failed_elapsed_seconds=failure['actual_elapsed_seconds'],source_failure_full_body=failure,
    genuine_missing_success_endpoints=list(map(str,absent_success)),no_success_four_tail_promotion=True,success_recorder_not_executed_as_Root_observed=True,
    no_retry_executed=True,failed_bootstrap_cannot_be_reused_by_original_fresh_attempt_gate=True,
    native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,
    business_imported=False,business_executed=False,project_written=False,files_deleted=0,
    first_reviewer_training_alias_assertion_failure_preserved=True,
    fresh_new_payload_byte_reads_include_failed_reviewer_and_corrected_reviewer=True,
    current_SOURCE31_and_original_prepared_typed_scope_is_complementary_peer_not_claimed_here=True,
    evidence_full_read_pins=PINS,elapsed_seconds=time.monotonic()-START)
with(D/'REPORT.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with(D/'REPORT.txt').open('x')as f:
    f.write('V9 原生唯一运行真实失败后验：证据范围 PASS，不是运行成功。\nRoot cefa98/53935→afac4e 退出1并关闭。6个初始阶段PASS，第7 bootstrap_axial因原512MiB门失败：PID35128，513.890625MiB，-15，580次实时样本，已清理进程组；未获得wait4，四个kernel字段保持None。\n全部7个原始watch与日志、完成archives/training原seal及所有新生成/失败partial字节鲜SHA通过；bootstrap未封存，maps0，不授予数值资格。\n当前35647 canonical、37339 metadata及37395完整期望读集全7身份保持，235528行解码完整，86namespace/186alias/445absence不变；旧35GB未重新读取。236动态资源根和原96GiB/free8GiB门保持，按当前文件计算。\nstdout0/stderr3643完整留存，失败Root收据已绑定；成功seal/terminal/四尾缺席，无重试、无AAA精度或ABA准入。下一次必须新源独审与新鲜尝试，不能复用此失败bootstrap。\n本核验只读TMP，未调用业务或修改项目。SOURCE31/完整prepared型与顺序由互补评审负责，尚未在本报告假填joint。\n')
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT.json'),sha256=hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),new_old35GB_reads=0,elapsed_seconds=report['elapsed_seconds'])))

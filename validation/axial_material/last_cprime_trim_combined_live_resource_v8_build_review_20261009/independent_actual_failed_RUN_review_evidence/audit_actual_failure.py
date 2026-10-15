import ast
import hashlib
import json
import math
import os
import stat
import time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009')
TMP=Path('/private/tmp/axmat_v8_actual_failed_RUN_independent_review_20261009')
FAIL_SHA='d4cacd55b43b590647ca9c1e6ec1168c58f8ddea7ec52b925b9048c556497039'
PINS={}
START=time.monotonic()

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p,sha=None):
    p=Path(p);before=identity(p)
    assert stat.S_ISREG(before[2]) and p.parent.resolve(strict=True)==p.parent,str(p)
    if str(p) in PINS:
        assert PINS[str(p)]['identity']==before
        result=PINS[str(p)]
    else:
        h=hashlib.sha256()
        fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
        with os.fdopen(fd,'rb') as f:
            s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
            while block:=f.read(4*1024**2):h.update(block)
        assert identity(p)==before
        result=dict(path=str(p),sha256=h.hexdigest(),size=before[3],identity=before)
        PINS[str(p)]=result
    if sha:assert result['sha256']==sha,str(p)
    return result

def read(p,sha=None):
    record=pin(p,sha)
    def pairs(items):
        out={}
        for key,value in items:
            assert key not in out
            out[key]=value
        return out
    def reject(text):raise ValueError(text)
    def floating(text):
        v=float(text);assert math.isfinite(v);return v
    value=json.loads(Path(p).read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=reject,parse_float=floating)
    assert identity(p)==record['identity']
    return value

def inventory(root):
    files={};dirs=[]
    for dp,dn,fn in os.walk(root,followlinks=False):
        for name in dn:
            p=Path(dp)/name;assert stat.S_ISDIR(p.lstat().st_mode) and not p.is_symlink()
            dirs.append(str(p.relative_to(root)))
        for name in fn:
            p=Path(dp)/name;assert not p.is_symlink()
            files[str(p.relative_to(root))]=pin(p)['sha256']
    return dict(files=files,symlinks={},directories=sorted(dirs))

def main():
    c=read(T/'config.json','ef9a8eb5d7b5b87ee63e1b36c5f3fd1f068fd73a48b7f00b64ad74cc36d86b0a')
    R,O,S,E=(Path(c[k]) for k in ('R','OUT','SOURCE','TERM'))
    assert c['failed_terminal_sha']==FAIL_SHA and all(c[k] is None for k in ('sealSha','terminalSha','terminalPath'))
    f=pin(c['F'],'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4')
    writer=pin(T/'record_root_actual_failure.py','74c2f6feef7f5b948f1a97b36330b437d2f4c6f6f6563682debe0fe03c89f9bf')
    pin(R/'actual_failed_RUN_record_root_actual_failure.py',writer['sha256'])
    assert (R/'actual_failed_RUN_config.json').read_bytes()==(T/'config.json').read_bytes()
    pin(R/'actual_failed_RUN_config.json',PINS[str(T/'config.json')]['sha256'])
    pin(T/'record_root_terminal.py','0fce254f46ac85606569a0343920e6c49fa60dc9674eaeca363dacffec55de4e')
    tool=read(R/'run_terminal_tool_return.json','4abe2350a3c227c5b60993a4334c701b6329b93996eeb04478d9c240cd9f81bc')
    assert type(tool['exit_code']) is int and tool['exit_code']==1 and tool['closed'] is True
    assert (tool['initial_chunk_id'],tool['session_id'],tool['terminal_chunk_id'])==('d68fa5',22770,'c5f80c')
    assert tool['success_recorder_called'] is False and tool['no_runtime_build_completion_or_science_credit'] is True
    receipt=read(E/'terminal_return.json',FAIL_SHA)
    assert (R/'run_terminal_return.json').read_bytes()==(E/'terminal_return.json').read_bytes()
    pin(R/'run_terminal_return.json',FAIL_SHA)
    assert receipt['actual_tool_result']==tool and type(receipt['returncode']) is int and receipt['returncode']==1
    assert receipt['record_producer']=='root' and receipt['actual_tool_terminal_return_observed'] is True and receipt['record_written_after_actual_terminal_return'] is True
    d=read(O/'declaration.json','3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae')
    prep=read(E/'declaration_terminal_return.json','b61c126fa40179d6133ce4258df599156e0c55a0092227f9ca4669b8a9581c56')
    assert type(prep['returncode']) is int and prep['returncode']==0
    assert receipt['source']==dict(path=f['path'],sha256=f['sha256'])
    assert receipt['declaration']==dict(path=str(O/'declaration.json'),sha256=c['declarationSha'])
    assert receipt['prep_terminal_evidence']==dict(path=str(E/'declaration_terminal_return.json'),sha256=c['prepSha'])
    command=[c['P'],c['F'],'run-build','--sha256',c['declarationSha'],'--prep-sha256',c['prepSha']]
    assert receipt['command']==tool['actual_child_command']==command
    assert receipt['schema']=='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V8_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
    for key in ('full_stdout','full_stderr','driver_result','stages','failed_python_audit_watch','failed_python_audit_log'):
        pin(receipt[key]['path'],receipt[key]['sha256'])
    assert Path(receipt['full_stdout']['path']).parent==E and Path(receipt['full_stderr']['path']).parent==E
    assert pin(T/'run.stdout')['size']==pin(receipt['full_stdout']['path'])['size']==0
    assert pin(T/'run.stderr')['size']==pin(receipt['full_stderr']['path'])['size']==1212
    assert (T/'run.stdout').read_bytes()==Path(receipt['full_stdout']['path']).read_bytes()
    assert (T/'run.stderr').read_bytes()==Path(receipt['full_stderr']['path']).read_bytes()
    assert tool['full_stdout_path']==str(T/'run.stdout') and tool['full_stderr_path']==str(T/'run.stderr')
    stderr=(T/'run.stderr').read_text()
    assert "own-child 512 MiB RSS cap reached" in stderr and "runner.execute(OUT/'audit'" in stderr
    driver=read(receipt['driver_result']['path'],receipt['driver_result']['sha256'])
    stages=read(receipt['stages']['path'],receipt['stages']['sha256'])['stages']
    watch=read(receipt['failed_python_audit_watch']['path'],receipt['failed_python_audit_watch']['sha256'])
    claim=read(O/'execution_claim.json')
    assert type(claim['parent_pid']) is int and claim['parent_pid']>0 and claim['retries']==0
    assert claim['declaration_sha256']==c['declarationSha'] and claim['prep_terminal_evidence']==receipt['prep_terminal_evidence']
    assert driver['classification']=='FAILED_COMBINED_RUNTIME_LINK_NO_RETRY'
    assert driver['error']==watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"
    labels=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
    assert len(stages)==5 and [s['label'] for s in stages]==labels and [s['status'] for s in stages]==['PASS']*4+['FAILED']
    art=ROOT/'validation/artifacts'
    nm='/usr/bin/nm';otool='/usr/bin/otool'
    targets=[O/'runtime/Dragon',art/'axial-material-rank1-factor-cache-build-20261007/runtime/Dragon',art/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007/runtime/Dragon',art/'axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon',art/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008/runtime/Dragon']
    commands=[d['production_link_command'],[nm,'-g',*d['actual_production_objects']],[nm,'-g',str(targets[0])],[otool,'-L',*map(str,targets)],[c['P'],c['F'],'audit-build','--sha256',c['declarationSha'],'--prep-sha256',c['prepSha']]]
    assert [s['command'] for s in stages]==commands
    summaries=[]
    for i,stage in enumerate(stages):
        log=O/(stage['label']+'.log');w=read(log.with_suffix('.watchdog.json'))
        assert w['command']==stage['command'] and w['rss_cap_mib']==512
        assert w['own_child_only'] is True and w['liveness_group_cleanup'] is True
        assert 0<=w['elapsed_seconds']<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=600
        if i<4:
            assert type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None
            assert 0<=w['sampled_peak_rss_mib']<512 and pin(log)['sha256']==stage['log_sha256']
        else:
            assert w==watch and type(w['returncode']) is int and w['returncode']==-15
            assert w['pid']==8231 and w['sampled_peak_rss_mib']==516.46875>=512
            assert stage['error']=='own-child 512 MiB RSS cap reached' and 'log_sha256' not in stage
            assert stage['elapsed_seconds']==32.61025991698261 and w['elapsed_seconds']==31.506270624988247
        summaries.append({key:w[key] for key in ('pid','returncode','sampled_peak_rss_mib','elapsed_seconds','wall_cap_seconds','rss_cap_mib','limit_failure','own_child_only','liveness_group_cleanup')}|dict(label=stage['label'],status=stage['status'],stage_elapsed_seconds=stage['elapsed_seconds'],log=pin(log)))
    raw=read(O/'raw_metadata_receipt.json')
    assert raw['files']=={label+'.log':pin(O/(label+'.log'))['sha256'] for label in labels[:4]}
    assert raw['before_binary_identity_gates'] is True and raw['complete_raw_tools_and_link_stdout'] is True
    assert pin(O/'audit/audit.log')['size']==0
    assert receipt['failed_python_audit_pid']==watch['pid'] and receipt['failed_python_audit_peak_rss_mib']==watch['sampled_peak_rss_mib']
    assert receipt['failed_python_audit_elapsed_seconds']==watch['elapsed_seconds'] and receipt['failed_stage_elapsed_seconds']==stages[-1]['elapsed_seconds']
    assert receipt['failed_driver_elapsed_seconds']==driver['elapsed_seconds']==291.0427399170003<1800
    assert receipt['failed_archive_bytes_before_closeout']==driver['archive_bytes_before_closeout']==153409544<2147483648
    assert receipt['failed_python_audit_cleanup'] is True and receipt['actual_original_failure_line_or_function_not_localized'] is True
    assert receipt['failed_driver_resource_observation']==driver['resources']
    res=driver['resources']
    assert res['artifact_budget_bytes']==d['artifact_budget_bytes']==103079215104 and res['min_free_bytes']==d['min_free_bytes']==8589934592
    assert res['artifact_bytes']==72343429515<res['artifact_budget_bytes'] and res['disk_free_bytes']==201718423552>res['min_free_bytes']
    assert res['declared_resource_roots']==d['resource_roots'] and res['resource_roots']==d['resource_roots'] and len(d['resource_roots'])==228
    assert res['resource_scope_policy']==d['resource_scope_policy'] and res['resource_scope_contract']==d['resource_scope_contract']
    flags=('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
    assert all(driver[key] is False and receipt[key] is False and d[key] is False for key in flags)
    assert all(receipt[key] is False for key in ('successful_combined_link_completion_observed','successful_new_runtime_build_observed','production_admission_observed','scientific_qualification'))
    assert receipt['build_seal'] is None and all(receipt[key] is None for key in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'))
    absent=[O/'seal.json',O/'audit/result.json',O/'audit/binary_identity.json',O/'closeout_failure.json',E/'run_full_stdout.json',E/'run_full_stderr.txt']
    assert all(not os.path.lexists(p) for p in absent)
    pin(O/'input_graph.json','242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
    source_inventory=inventory(S)
    assert source_inventory==d['source_inventory'] and len(source_inventory['files'])==11
    partial_inventory=inventory(O)
    current_archive=sum(pin(S/name)['size'] for name in source_inventory['files'])+sum(pin(O/name)['size'] for name in partial_inventory['files'])
    assert current_archive==153467780 and current_archive-pin(O/'driver_result.json')['size']==driver['archive_bytes_before_closeout']
    old_path=art/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/terminal_return.json'
    old=read(old_path,'7f555a40cc7867e99537a550b1d94d70d116afd35b56a17625d37a8cc17f8679')
    assert set(old)==set(receipt) and type(old['returncode']) is int and old['returncode']==old['actual_tool_result']['exit_code']==1
    assert old['build_seal'] is None and all(old[key] is None for key in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'))
    assert all(old[key] is False for key in flags+('scientific_qualification','successful_combined_link_completion_observed','successful_new_runtime_build_observed','production_admission_observed'))
    pin(old['source']['path'],old['source']['sha256'])
    assert read(T/'config.json')==c
    for path,record in PINS.items():assert identity(path)==record['identity']
    report=dict(schema='AXMAT_V8_ACTUAL_FAILED_RUN_INDEPENDENT_TERMINAL_REVIEW_V1',status='PASS',actual_RUN_outcome='FAILED_EXIT1_NO_RETRY_NO_RUNTIME_OR_SCIENCE_ADMISSION',
        failure_terminal_sha256=FAIL_SHA,Root_tool_observation_pin=PINS[str(R/'run_terminal_tool_return.json')],actual_Root_terminal_tool=dict(initial_chunk_id='d68fa5',session_id=22770,terminal_chunk_id='c5f80c',exit_code=1,closed=True,success_recorder_called=False),
        factory_pin=f,actual_failure_writer_source_pin=writer,declaration_sha256=c['declarationSha'],Root_PREP_sha256=c['prepSha'],config_pin=PINS[str(T/'config.json')],
        exact_Root_TERMINAL_and_review_copy_equal=True,receipt_keyset_same_as_frozen_V7_failure=True,old_V7_failure_and_source_original_facts_remain_failed=True,
        stdout_bytes=0,stderr_bytes=1212,full_raw_stdout_stderr_pins_and_copies_verified=True,
        driver_classification=driver['classification'],driver_error=driver['error'],exact_five_commands_and_stage_status_order_verified=True,stage_summaries=summaries,
        failed_python_audit_watch=watch,failed_driver_elapsed_seconds=driver['elapsed_seconds'],failed_stage_elapsed_seconds=stages[-1]['elapsed_seconds'],
        resource_observation_summary={k:res[k] for k in ('checked_unix','min_free_bytes','artifact_budget_bytes','artifact_bytes','regular_files','disk_free_bytes','resource_scope_policy')},declared_resource_root_count=228,actual_observed_root_count=228,resource_roots_and_original_scope_contract_exact=True,
        actual_Root_stored_free_disk_observation_not_attributed_to_RUN=True,archive_bytes_before_driver_closeout=driver['archive_bytes_before_closeout'],current_complete_SOURCE_OUT_bytes=current_archive,driver_result_bytes_added_after_precloseout_measure=pin(O/'driver_result.json')['size'],
        fresh_SOURCE11_inventory=source_inventory,fresh_complete_partial_OUT_inventory=partial_inventory,actual_partial_link_and_raw_metadata_are_inert_unsealed_evidence=True,
        failed_build_seal_None=True,four_success_tails_None=True,success_config_fields_None=True,failed_config_field_bound=True,success_seal_and_audit_result_absent=True,
        old_failed_RUN_or_capture_RSS_credit_transferred=False,native_transport_executed=False,combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,
        failure_scope=receipt['failure_scope'],actual_original_allocating_function_not_localized=True,
        scope_limits=['This review proves preservation and consistent accounting of the actual failed Python audit child. It does not establish the internal allocation cause or justify attributing the observed peak to one helper function.','The link and three raw metadata stages passed; the fifth stage failed before audit/binary_identity.json and audit/result.json, so the generated executable has no completed whole link-identity or native/science eligibility.','The unchanged input graph is freshly hashed here; its 35647-member complete fresh input verification was already independently passed for PREP and is not repeated as business execution after this failure.'],
        pins=list(PINS.values()),Root_closed_session_polled=False,business_factory_or_scientific_module_imported=False,metadata_graph_helper_imported=False,business_API_constructor_or_audit_build_PREP_RUN_executed=False,
        native_or_numeric_tools_executed=False,files_deleted=0,formal_or_ART_writes=False,write_scope='Own TMP audit/report only',audit_source_pin=pin(Path(__file__)),elapsed_seconds=time.monotonic()-START)
    TMP.mkdir(parents=True,exist_ok=True)
    p=TMP/'independent_actual_failure_review.json'
    with p.open('x') as out:json.dump(report,out,indent=2);out.write('\n')
    print(json.dumps(dict(status='PASS',outcome=report['actual_RUN_outcome'],path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),failed_RSS_MiB=watch['sampled_peak_rss_mib'],five_statuses=[s['status'] for s in stages],source11=True,seal=False,fourtails=None,science=False,pins=len(PINS))))

if __name__=='__main__':main()

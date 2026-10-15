"""UNREADY future saved-BUILD reviewer. Standard library only.
Run only after Root supplies true closed BUILD, closed metadata writer, frozen
Source and final snapshots. Never execute/import project/helper/guard/binder,
and never read binary, graph, trace, gzip, material or DB payload bytes.
Source files and explicitly supplied small META alone are read to EOF.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import tempfile

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_combined_build_v25_poststage_temporaries_sources'
E=B/'actual_complete_combined_build_v25_poststage_temporaries_receipts'
ART=Path('/Users/wen/spot/validation/artifacts')
H=ART/'axial-material-complete-combined-build-host-v25-poststage-temporaries-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010'
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py')
CAPS=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)
LABELS=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
PINS={};CHECKS=[]

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p):
    p=Path(p);assert p.is_absolute() and '..' not in p.parts
    for q in [*reversed(p.parents),p]:
        i=identity(q);assert not stat.S_ISLNK(i[2]) and (q==p or stat.S_ISDIR(i[2]))
    return p

def pin(p):
    p=ordinary(p);i=identity(p);assert stat.S_ISREG(i[2]) and i[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    q=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
    if str(p) in PINS:assert PINS[str(p)]==q
    PINS[str(p)]=q;return q

def normalize(q):
    assert type(q) is dict and {'path','sha256'}<=q.keys()
    i=q.get('identity',q.get('identity7'));assert type(i) is list and len(i)==7 and all(type(v) is int for v in i)
    assert stat.S_ISREG(i[2]) and i[3]>=1 and q.get('size_bytes',i[4])==i[4]
    assert type(q['sha256']) is str and len(q['sha256'])==64 and all(c in '0123456789abcdef' for c in q['sha256'])
    return dict(path=q['path'],sha256=q['sha256'],size_bytes=i[4],identity=i)

def exact(q):
    q=normalize(q);assert pin(q['path'])==q;return q

def current7ID(q):
    q=normalize(q);ordinary(q['path']);assert identity(q['path'])==q['identity'];return q

def pairs(rows):
    d={}
    for k,v in rows:assert k not in d;d[k]=v
    return d

def reject(s):raise ValueError('nonfinite META '+s)

def meta(q):
    q=exact(q);p=Path(q['path'])
    assert p.suffix in ('.json','.txt','.log') and p.name not in ('declaration.json','input_graph.json','input_creation_python_open_trace.json')
    v=json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=reject)
    assert pin(p)==q
    return v

def check(name,value):
    assert type(value) is bool and name not in {q['id'] for q in CHECKS}
    CHECKS.append(dict(id=name,passed=value))
    if not value:raise ValueError('saved META check failed: '+name)

def closed(d,exit0=False):
    assert d['closed'] is True
    assert d.get('observed_after_actual_terminal_return',d.get('observed_terminal',d.get('actual_tool_terminal_return_observed',False))) is True
    tr=d.get('terminal_tool_return',d.get('actual_tool_return'))
    assert type(tr['exit_code']) is int and 'session_id' not in tr
    assert d.get('session_repolled_after_close',False) is False
    if exit0:assert tr['exit_code']==0
    return tr

def statview(root):
    root=Path(root)
    if not os.path.lexists(root):return dict(root=str(root),present=False,files={},directories={},symlinks={})
    ordinary(root);files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        i=identity(p);r=str(p.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):dirs[r]=i
        else:assert stat.S_ISREG(i[2]);files[r]=dict(path=str(p),identity=i)
    assert all(identity(root/r)==i for r,i in dirs.items())
    return dict(root=str(root),present=True,files=files,directories=dirs,symlinks={})

def bytes_of(view):return sum(q['identity'][4] for q in view['files'].values())

def current_namespace(row):
    v=statview(row['root']);assert v['present']==row['present'] and v['symlinks']==row['symlinks']=={}
    assert v['directories']==row['directories'] and set(v['files'])==set(row['files'])
    assert all(current7ID(q)['identity']==v['files'][r]['identity'] for r,q in row['files'].items())
    return v

def main():
    assert len(sys.argv)==2 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    cp=pin(Path(sys.argv[1]));config=meta(cp)
    assert config['schema']=='ROOT_V25_POSTSTAGE_ACTUAL_CLOSED_BUILD_SAVED_SOURCE_META_REVIEW_INPUTS_V1'
    assert config['status']=='ACTUAL_ROOT_BUILD_AND_METADATA_WRITER_CLOSED_INPUTS_READY'
    roles=config['actual_input_pins'];required={'Root_terminal','metadata_writer_terminal','summary','namespace','formal_terminal','source_freeze','prelaunch','canonical_Source','host_Source','postclose_writer_Source','prelaunch_E_snapshot','postclose_E_snapshot'}
    assert set(roles)==required and all(type(q) is dict for q in roles.values())
    # UNREADY None entries fail here before any candidate/guard/business access.
    q={k:normalize(v) for k,v in roles.items()}
    for key in ('canonical_Source','host_Source','postclose_writer_Source'):exact(q[key])
    assert q['canonical_Source']['path']==str(C) and q['canonical_Source']['sha256']=='6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649'
    assert q['host_Source']['path']==str(D/'combined_build_host.py') and q['host_Source']['sha256']=='d5024a468b204d988fb8f929303481fdcd5e0c311b6a282536bc1dea5a979159'
    assert q['postclose_writer_Source']['path']==str(D/'write_actual_build_postclose_META.py') and q['postclose_writer_Source']['sha256']=='7a7c8d59ddea37397592591ba96d6ac7dbca1dda1acce7f9d12b9ae6dcaa278a'
    check('current_qualified_complete_Source_roles_exact',True)
    root=meta(q['Root_terminal']);tr=closed(root);writer=meta(q['metadata_writer_terminal']);wt=closed(writer,True)
    assert root['record_producer']=='root' and root['observed_after_actual_terminal_return'] is True and type(root['exit_code']) is int and root['exit_code']==tr['exit_code']
    initial=root['initial_tool_return'];sid=root['original_session_id'];assert type(sid) is int and initial['session_id']==sid and 'exit_code' not in initial
    observations=root['observations'];assert observations and observations[-1]==tr
    assert all('exit_code' not in x for x in observations[:-1]) and all(x.get('session_id',sid)==sid for x in observations)
    check('true_Root_and_writer_terminal_lifecycle_closed',True)
    summary=meta(q['summary']);namespace=meta(q['namespace']);formal=meta(q['formal_terminal']);freeze=meta(q['source_freeze']);prelaunch=meta(q['prelaunch'])
    assert normalize(summary['actual_Root_terminal'])==q['Root_terminal'] and normalize(summary['namespace_manifest'])==q['namespace'] and normalize(summary['formal_build_terminal'])==q['formal_terminal']
    assert normalize(namespace['actual_Root_terminal'])==q['Root_terminal'] and normalize(namespace['exact_formal_terminal'])==q['formal_terminal']
    assert formal['returncode']==tr['exit_code'] and formal['actual_tool_result']==tr and formal['record_producer']=='root' and formal['record_written_after_actual_terminal_return'] is True
    observed=json.loads(wt['output']);assert normalize(observed['namespace_manifest'])==q['namespace'] and normalize(observed['summary'])==q['summary'] and observed['actual_tool_exit_code']==tr['exit_code']
    check('summary_namespace_formal_and_true_writer_stdout_fullpin_coupling',True)
    assert summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_BUILD_POSTCLOSE_SUMMARY_V1' and namespace['schema']=='ROOT_V25_ACTUAL_COMPLETE_BUILD_POSTCLOSE_FINITE_NAMESPACES_V1'
    capkeys=('whole_wall_cap_seconds','inner_stage_wall_cap_seconds','rss_cap_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children_at_once','retries')
    assert tuple(summary[k] for k in capkeys)==CAPS and all(type(summary[k]) is int for k in capkeys)
    assert summary['original_caps_preserved'] is True
    check('all_original_whole_stage_resource_caps_preserved',True)
    assert freeze['schema']=='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and freeze['source_root']==str(D) and freeze['symlinks']=={} and freeze['no_SOURCE_append_after_freeze'] is True
    v=statview(D);assert v['directories']==freeze['complete_directories'] and set(v['files'])==set(freeze['complete_files'])
    for r,row in freeze['complete_files'].items():assert exact(row)['identity']==v['files'][r]['identity']
    assert freeze['actual_complete_SOURCE_file_count']==len(v['files'])==summary['full_SOURCE_file_count']
    check('complete_actual_BUILD_Source_EOF_7ID_namespaces_no_append',True)
    fixed=prelaunch['fixed_input_pins'];assert type(fixed) is list and len(fixed)==prelaunch['fixed_input_entries_count']==summary['original_fixed_input_entry_count']
    assert namespace['ordered_original_fixed_input_expected_pins']==fixed
    for row in fixed:current7ID(row)
    assert len(namespace['unchanged_ordered_original_fixed_input_results'])==len(fixed) and namespace['original_fixed_input_failures']==[] and summary['all_original_fixed_inputs_unchanged'] is True
    assert all(row['index']==index and normalize(row['pin'])==normalize(fixed[index]) for index,row in enumerate(namespace['unchanged_ordered_original_fixed_input_results']))
    check('all_ordered_original_fixed_inputs_including_repeats_Root_EOF_current7ID',True)
    roots={str(p) for p in (H,S,O,T,D,E)};rows=namespace['namespaces'];assert len(rows)==6 and {r['root'] for r in rows}==roots
    for row in rows:
        if Path(row['root'])!=E:current_namespace(row)
    check('all_six_original_postclose_namespace_full_savedpins_current7ID',True)
    enext=meta(q['postclose_E_snapshot']);epre=meta(q['prelaunch_E_snapshot'])
    assert enext['root']==str(E) and epre['root']==str(E)
    ev=statview(E);assert set(ev['files'])==set(enext['files']) and ev['directories']==enext['directories'] and enext['symlinks']=={}
    for row in enext['files'].values():exact(row)
    old=next(row for row in rows if row['root']==str(E));expected={**old['files'],Path(q['summary']['path']).name:q['summary'],Path(q['namespace']['path']).name:q['namespace']}
    for row in config['actual_later_E_file_pins']:expected[Path(row['path']).name]=exact(row)
    assert set(expected)==set(enext['files']) and all(normalize(enext['files'][r])==normalize(row) for r,row in expected.items())
    assert old['directories']['.'][:3]==enext['directories']['.'][:3] and set(old['directories'])==set(enext['directories'])
    assert all(old['directories'][r]==enext['directories'][r] for r in old['directories'] if r!='.')
    assert all(normalize(row)==normalize(enext['files'][r]) for r,row in epre['files'].items())
    check('E_exact_before_append_snapshot_and_all_true_later_members',True)
    actual_joint=sum(bytes_of(row) for row in rows)+q['namespace']['size_bytes']+q['summary']['size_bytes']+q['canonical_Source']['size_bytes']+q['postclose_writer_Source']['size_bytes']
    assert actual_joint==summary['joint_archive_bytes_after_summary']<CAPS[3]
    extras=[statview(Path(r)) for r in prelaunch['complete_joint_scope_roots']]
    assert len(extras)==9 and sum(bytes_of(r) for r in extras)+q['canonical_Source']['size_bytes']<CAPS[3]
    check('historical_writer_six_scope_and_complete_Root_nine_scope_byte_caps',True)
    assert namespace['no_whole_INPUT_native_science_credit'] is True and namespace['no_business_or_numeric_API_called_by_writer'] is True
    for key in ('whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved','mathematical_controls_newly_executed','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete'):
        assert summary[key] is False and formal[key] is False
    assert summary['separate_child_stderr_captured'] is False and summary['independent_child_stderr_empty_verified'] is False
    check('original_science_and_merged_child_capture_boundaries',True)
    success=namespace['mode']=='SUCCESSFUL_COMPLETE_BUILD_LINK_IDENTITY_METADATA_ONLY'
    if success:
        assert tr['exit_code']==0 and summary['status']=='ACTUAL_COMPLETE_FIVE_STAGE_LINK_IDENTITY_BUILD_EXIT0_CLOSED_ONLY'
        assert summary['original_five_build_stages_executed'] is True and summary['all_five_build_stages_passed'] is True and summary['completed_inner_stage_labels']==LABELS
        stages=summary['actual_inner_stages'];watches=summary['actual_inner_watchdogs'];assert len(stages)==len(watches)==5
        assert [row['label'] for row in stages]==LABELS and all(row['status']=='PASS' for row in stages)
        for stage,watch in zip(stages,watches):
            assert watch['command']==stage['command'] and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None
            assert 0<=watch['sampled_peak_rss_mib']<512 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=600
            assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
        outer=summary['actual_outer_watchdog'];assert type(outer['returncode']) is int and outer['returncode']==0 and outer['limit_failure'] is None and 0<=outer['sampled_peak_rss_mib']<512
        assert 0<=summary['canonical_child_seconds']<=summary['whole_seconds']<1800
        tails=summary['actual_tail_fields'];assert set(tails)=={'actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'} and tails['actual_tail_check']=='PASS'
        assert 0<=tails['actual_elapsed_seconds']<1800 and 0<tails['actual_archive_bytes']<2*2**30
        assert namespace['full_declared_physical_input_finalpass_claimed'] is True
        for row in namespace['full_declared_physical_input_postclose_pins']:current7ID(row)
        check('actual_closed_whole_build_five_watches_audit_tails_success_only',True)
    else:
        assert namespace['mode']=='FAILED_BUILD_SAVED_METADATA_ONLY' and summary['original_five_build_stages_executed'] is False and summary['all_five_build_stages_passed'] is False
        assert formal['successful_new_runtime_build_observed'] is False and summary['completed_inner_stage_labels']==[]
        assert namespace['full_declared_physical_input_finalpass_claimed'] is False and namespace['full_declared_physical_input_postclose_pins']==[]
        assert summary['original_host_final_input_revalidation_observed'] is False and summary['Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass'] is True
        assert formal['metadata_check_errors'] and (tr['exit_code']!=0 or summary['status']=='ACTUAL_ROOT_EXIT0_METADATA_CHECK_FAILED_NO_SUCCESS_RECEIPT')
        assert not os.path.lexists(T/'terminal_return.json')
        check('honest_actual_failed_or_EXIT0_metadata_failed_only_no_success_credit',True)
    F=Path(tempfile.mkdtemp(prefix='axmat_V25_actual_poststage_BUILD_saved_Source_META_independent_',dir='/private/tmp'))
    report=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_BUILD_SAVED_SOURCE_META_REVIEW_V1',status='PASS_ACTUAL_COMPLETE_LINK_IDENTITY_BUILD_METADATA_ONLY' if success else 'PASS_ACTUAL_FAILED_BUILD_EVIDENCE_ONLY',source_only=True,source_only_reviewer=True,all_checks_typed_true=True,checks=CHECKS,check_count=len(CHECKS),blockers=[],actual_review_input_contract_pin=cp,actual_Root_BUILD_terminal_pin=q['Root_terminal'],actual_METADATA_writer_terminal_pin=q['metadata_writer_terminal'],actual_Root_BUILD_summary_pin=q['summary'],actual_complete_namespace_manifest_pin=q['namespace'],actual_Root_terminal_chunk=tr['chunk_id'],actual_metadata_writer_terminal_chunk=wt['chunk_id'],all_complete_EOF_Source_small_META_pins=list(PINS.values()),Root_full_EOF_physical_payload_pins_verified_current7ID_only=True,physical_graph_trace_gzip_binary_material_DB_payload_read=False,whole_combined_build_qualified=success,whole_combined_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,goal_complete=False,candidate_binder_helper_guard_API_compile_material_numeric_executed=False)
    with (F/'REVIEW.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(package=str(F),review_pin=pin(F/'REVIEW.json'),status=report['status'],check_count=len(CHECKS),source_only=True),allow_nan=False))

if __name__=='__main__':main()

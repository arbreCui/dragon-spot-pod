import hashlib,importlib.util,json,os,shutil,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010';A=R/'validation/artifacts';ART=A
D=B/'actual_complete_combined_build_v25_memory_observation_capture_pre_graph_gc_sources';E=B/'actual_complete_combined_build_v25_memory_observation_capture_pre_graph_gc_receipts';PRE=B/'actual_complete_combined_prepare_v25_memory_observation_capture_pre_graph_gc_receipts'
H=A/'axial-material-complete-combined-build-host-v25-memory-observation-capture-pre-graph-gc-20261010';S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-memory-observation-capture-pre-graph-gc-20261010';O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010';T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-memory-observation-capture-pre-graph-gc-20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py'

PREP_H=ART/'axial-material-complete-combined-prepare-host-v25-memory-observation-capture-pre-graph-gc-20261010'
PREP_D=B/'actual_complete_combined_prepare_v25_memory_observation_capture_pre_graph_gc_sources'
MOTHER=None  # UNREADY until installed actual finite request
SAVED_PREP_PEER=None  # UNREADY until installed actual finite request
MOTHER_PEER=None  # UNREADY until installed actual finite request
MOTHER_SEAL=None  # UNREADY until installed actual finite request
BINDING_RECEIPT=None  # UNREADY until installed actual finite request
OLD_TERMINAL=B/'actual_complete_combined_build_v22_receipts/Root_actual_build_tool_terminal_return.json'
UTILITY=None  # UNREADY until installed actual finite request
MOTHER_SHA=None  # UNREADY until installed actual finite request
BOUND_SHA=None  # UNREADY until installed actual finite request
SAVED_PREP_SHA=None  # UNREADY until installed actual finite request
MOTHER_PEER_SHA=None  # UNREADY until installed actual finite request
SUMMARY_SHA=None  # UNREADY until installed actual finite request
NS_SHA=None  # UNREADY until installed actual finite request
HOST_SHA=None  # UNREADY until installed actual finite request
WRITER_SHA=None  # UNREADY until installed actual finite request
C_SHA=None  # UNREADY until installed actual finite request
FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
OUTPUTS=('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','build_memory_diagnostic.jsonl','audit/binary_identity.json','audit/result.json',FAMILY+'/stages.json','runtime/Dragon')
BUILD_MEMORY_DIAGNOSTIC_CONTRACT = {'schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_OUTPUT_CONTRACT_V1', 'relative_path': 'build_memory_diagnostic.jsonl', 'row_schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_ROW_V1', 'phases': ['run_build', 'declaration_admission', 'before_build_link', 'before_metadata_objects', 'before_metadata_executable', 'before_metadata_dependencies', 'run_finally'], 'points': ['declaration_enter', 'declaration_return', 'commands_constructed', 'execute_enter', 'execute_return', 'environment_enter', 'environment_return', 'complete_input_enter', 'specs1_enter', 'specs1_return', 'owned1_enter', 'owned1_return', 'current_before_enter', 'current_before_return', 'verify_graph_enter', 'verify_graph_return', 'snapshot_enter', 'snapshot_return', 'trace_digest_enter', 'trace_digest_return', 'specs2_enter', 'specs2_return', 'current_after_enter', 'current_after_return', 'owned2_enter', 'owned2_return', 'graph2_enter', 'graph2_return', 'bindings_enter', 'bindings_return', 'lengths_enter', 'lengths_return', 'complete_input_return', 'archive_resources_return', 'normal_pre_inventory'], 'max_rows': 256, 'max_line_bytes_including_newline': 4096, 'max_bytes': 1048576, 'open_flags': 'O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW', 'mode_octal': '0600', 'one_parent_descriptor': True, 'write_only': True, 'read_during_active_input_audit': False, 'last_normal_marker': 'normal_pre_inventory', 'close_before_original_OUT_inventory': True, 'no_append_after_close': True, 'ru_maxrss_semantics': 'DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK', 'diagnostic_runtime_dependency_provenance': 'FUTURE_ROOT_SOURCE_BIND_AND_PRELAUNCH_ENVIRONMENT_WITNESS_REQUIRED', 'actual_runtime_pin': None, 'current_RSS_qualified': False, 'whole_INPUT_build_native_or_science_qualified': False}

def memory_diagnostic_declaration(d):
    expected=BUILD_MEMORY_DIAGNOSTIC_CONTRACT
    actual=d.get('build_memory_diagnostic_output_contract')
    if json.dumps(actual,sort_keys=True,allow_nan=False)!=json.dumps(expected,sort_keys=True,allow_nan=False):
        raise ValueError('exact declared write-only bounded output diagnostic contract required')
    forecast=d['complete_archive_forecast']
    fields=('copied_SOURCE_metadata_bound','trim_whole_component_metadata_and_trace_bound','full_graph_and_creation_trace_bound','combined_runtime_and_link_transient_bound','complete_raw_tools_and_closeout_bound','diagnostic_max_bytes','total_bound')
    if any(type(forecast[k]) is not int or forecast[k]<0 for k in fields):
        raise ValueError('exact integer complete forecast and diagnostic reservation required')
    if forecast['diagnostic_max_bytes']!=expected['max_bytes'] or forecast['total_bound']!=sum(forecast[k] for k in fields[:-1]) or forecast['total_bound']>=2*2**30:
        raise ValueError('all original complete forecast components plus diagnostic remain below original 2GiB')
    return actual

def ident(p):
    v=p.lstat();return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]
def pin(p,wanted=None):
    p=Path(p);before=ident(p);assert p.resolve()==p and stat.S_ISREG(before[2]) and before[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert ident(p)==before
    q=dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
    if wanted:assert q['sha256']==wanted
    return q
def exact(q):
    c=pin(q['path']);assert {k:c[k] for k in q}==q;return c
def read(p,sha=None):
    q=pin(p,sha);d=json.loads(p.read_text());assert pin(p)==q;return d,q
def joint_size(roots):
    total=0
    for root in roots:
        if not root.exists():continue
        assert root.is_dir() and not root.is_symlink()
        for p in root.rglob('*'):
            assert not p.is_symlink()
            if p.is_file():total+=p.lstat().st_size
    return total

def full_view(root):
    assert root.is_absolute() and root.resolve()==root and root.is_dir() and not root.is_symlink()
    files={};dirs={'.':ident(root)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink();i=ident(p);key=str(p.relative_to(root))
        if stat.S_ISREG(i[2]):files[key]=pin(p)
        else:assert stat.S_ISDIR(i[2]);dirs[key]=i
    for key,q in files.items():exact(q)
    for key,i in dirs.items():assert ident(root/key)==i
    return dict(root=str(root),files=files,directories=dirs,symlinks={})
def original_host_pin(q):
    # Genuine support.pin returns these exact three keys; preserve ordered repeats for the original writer comparison.
    return {k:q[k] for k in ('path','sha256','identity')}
def check_PREP(summary):
    ns,nspin=read(PRE/'Root_actual_complete_prepare_namespace_manifest.json',NS_SHA)
    assert {k:nspin[k] for k in summary['namespace_manifest']}==summary['namespace_manifest']
    assert ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1'
    assert [Path(v['root']) for v in ns['namespaces']]==[PREP_H,S,O,T,PREP_D]
    views=[]
    for saved in ns['namespaces']:
        v=full_view(Path(saved['root']));assert saved['symlinks']=={} and set(v['files'])==set(saved['files'])
        for q in saved['files'].values():exact(q)
        assert {k:i for k,i in v['directories'].items() if k!='.'}=={q['path']:q['identity'] for q in saved['directories']}
        views.append(v)
    ph,php=read(Path(summary['actual_host_result']['path']),summary['actual_host_result']['sha256']);exact(summary['actual_host_result'])
    prep=ph['input_sources']+[ph['original_helper'],ph['resource_factory']]
    scope.prepare_input_scope(ph,summary)
    assert len(prep)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(prep)
    for q in prep:exact(q)
    return ns,nspin,ph,php,prep,views

def strict_closed_zero(record):
    assert record['closed'] is True
    tr=record.get('terminal_tool_return',record.get('actual_tool_return'))
    assert type(tr) is dict and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr

def verify_frozen_source(freeze):
    assert freeze['schema']=='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and freeze['source_root']==str(D)
    assert freeze['symlinks']=={} and freeze['no_SOURCE_append_after_freeze'] is True
    v=full_view(D);assert v['files']==freeze['complete_files'] and v['directories']==freeze['complete_directories']
    assert type(freeze['actual_complete_SOURCE_file_count']) is int and freeze['actual_complete_SOURCE_file_count']==len(v['files'])
    return v

def main():
    global scope,SUMMARY_SHA,NS_SHA,HOST_SHA,WRITER_SHA,C_SHA
    assert len(sys.argv)==1 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    sys.dont_write_bytecode=True
    freeze,freeze_pin=read(E/'Root_prelaunch_complete_build_source_freeze.json');source_view=verify_frozen_source(freeze)
    assert Path(__file__)==D/'Root_prelaunch_checker.py' and pin(Path(__file__))==freeze['complete_files']['Root_prelaunch_checker.py']

    assert pin(D/'Root_poststage_Source_META_contract.py')==freeze['complete_files']['Root_poststage_Source_META_contract.py']
    import Root_poststage_Source_META_contract as scope
    assert Path(scope.__file__).resolve()==D/'Root_poststage_Source_META_contract.py'
    request,installed=scope.installed_request(D,'BUILD');prep_fact=request['actual_new_PREP'];roles=request['bound']['roles']
    SUMMARY_SHA=prep_fact['summary']['sha256'];NS_SHA=prep_fact['namespace']['sha256'];HOST_SHA=roles['build_host']['sha256'];WRITER_SHA=roles['build_writer']['sha256'];C_SHA=pin(C)['sha256']
    summary,summary_pin=read(PRE/'Root_actual_complete_combined_prepare_summary.json',SUMMARY_SHA)
    assert summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
    ns,nspin,ph,php,prep_inputs,prepared=check_PREP(summary)
    strict_closed_zero(read(PRE/'Root_actual_prepare_tool_terminal_return.json')[0])
    strict_closed_zero(read(PRE/'Root_actual_prepare_metadata_writer_tool_terminal_return.json')[0])
    current_pre=full_view(PRE)
    installation,_=read(D/'Root_complete_SOURCE_install_record.json')
    assert installation['complete_actual_PREP_E_source']==current_pre
    assert installation['all_actual_PREP_fixed_inputs_unchanged']==[exact(q) for q in prep_inputs]
    # This is the exact ordered host input construction, including repeated paths; no set or mapping deduplication.
    fixed=[original_host_pin(exact(q)) for q in ph['input_sources'][:7]]
    fixed+=[original_host_pin(pin(p)) for p in sorted(D.rglob('*')) if p.is_file()]
    fixed+=[original_host_pin(exact(summary['actual_declaration'])),original_host_pin(exact(summary['formal_PREP_terminal'])),original_host_pin(exact(summary['actual_complete_input_graph'])),original_host_pin(exact(summary['actual_complete_creation_trace']))]
    fixed+=[original_host_pin(pin(p)) for root in (S,T) for p in sorted(root.rglob('*')) if p.is_file()]
    fixed+=[original_host_pin(exact(summary['actual_root_terminal'])),original_host_pin(summary_pin),original_host_pin(exact(ph['original_helper'])),original_host_pin(exact(ph['resource_factory']))]
    host_pin=pin(D/'combined_build_host.py',HOST_SHA);writer_pin=pin(D/'write_actual_build_postclose_META.py',WRITER_SHA)
    assert pin(C,C_SHA)==exact(fixed[1]) and not os.path.lexists(H)
    assert all(set(q)=={'path','sha256','identity'} for q in fixed)
    for rel in OUTPUTS:assert not os.path.lexists(O/rel)
    support_path=Path(fixed[0]['path']);assert fixed[0]['sha256']=='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
    spec=importlib.util.spec_from_file_location('Root_v25_memory_observation_capture_pre_graph_gc_complete_build_prelaunch_original_support',support_path)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    assert Path(sys.executable).resolve()==support.PYTHON and support.THREAD_KEYS==THREAD_KEYS and all(os.environ.get(k)=='1' for k in support.THREAD_KEYS)
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'Root_v25_memory_observation_capture_pre_graph_gc_build_prelaunch_genuine619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'Root_v25_memory_observation_capture_pre_graph_gc_build_prelaunch_genuine_ebbb')
    full,production=helper.modules();helper.guard_admission(full)
    assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
    assert Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
    assert fixed[-2]==hpin and fixed[-1]==rpin
    roots=resource.history_roots([str(p) for p in (H,S,O,T)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    actual_resources=resources.check()
    assert actual_resources['artifact_bytes']+2*2**30<96*2**30 and actual_resources['disk_free_bytes']-2*2**30>=8*2**30
    extra_roots=[H,S,O,T,D,E,PREP_H,PREP_D,PRE]
    extra_views=[full_view(p) for p in extra_roots if p.exists()]
    canonical_pin=pin(C,C_SHA)
    before_bytes=joint_size(extra_roots)+canonical_pin['size_bytes']
    assert before_bytes==sum(q['size_bytes'] for v in extra_views for q in v['files'].values())+canonical_pin['size_bytes'] and before_bytes<2*2**30
    # Canonical source and validation receipts lie outside ART and must count against the complete history reserve too.
    outside_art_bytes=sum(q['size_bytes'] for v in extra_views if not Path(v['root']).is_relative_to(A) for q in v['files'].values())+canonical_pin['size_bytes']
    assert actual_resources['artifact_bytes']+outside_art_bytes+2*2**30<96*2**30
    q=dict(schema='ROOT_V25_COMPLETE_BUILD_FINAL_PRELAUNCH_SOURCE_INPUT_RESERVE_CHECK_V1',status='PRELAUNCH_PASS_NO_BUILD_EXECUTED',fixed_input_pins=fixed,fixed_input_entries_count=len(fixed),source_freeze=freeze_pin,complete_SOURCE_files=freeze['complete_files'],complete_SOURCE_directories=freeze['complete_directories'],prepared_namespace_manifest=nspin,actual_PREP_summary=summary_pin,actual_PREP_host_result=php,current_complete_PREP_E=current_pre,canonical_factory=fixed[1],normal_host=host_pin,postclose_META_writer=writer_pin,genuine_guard_original_MRO_verified=True,actual_genuine_history_resources=actual_resources,complete_joint_scope_roots=[str(p) for p in extra_roots],complete_joint_scope_preappend_views=extra_views,canonical_fullpin=canonical_pin,complete_joint_bytes_before_prelaunch_record=before_bytes,complete_history_extra_outside_ART_bytes=outside_art_bytes,original_host_joint_scope_is_H_S_O_T_D=True,complete_Root_extra_scope_ledger_does_not_modify_host_guard=True,whole_seconds_cap=1800,stage_seconds_cap=600,rss_mib_cap=512,joint_archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0,HOST_fresh=True,all_new_build_outputs_absent=True,all_original_PREP_inputs_unchanged=True,actual_original_PREP_input_count=len(prep_inputs),old144_count_is_provenance_only=True,all_prepared_namespaces_unchanged=True,SOURCE_frozen_no_append=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,numeric_or_build_executed=False)
    out=E/'Root_final_prelaunch_source_input_and_reserve_check.json'
    with out.open('x') as f:json.dump(q,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    own_pin=pin(out);after_bytes=joint_size(extra_roots)+canonical_pin['size_bytes']
    assert after_bytes==before_bytes+own_pin['size_bytes'] and after_bytes<2*2**30
    assert actual_resources['artifact_bytes']+outside_art_bytes+own_pin['size_bytes']+2*2**30<96*2**30 and shutil.disk_usage(R).free-2*2**30>=8*2**30
    for v in extra_views:
        now=full_view(Path(v['root']))
        if Path(v['root'])==E:
            assert now['files']=={**v['files'],out.name:own_pin}
            assert set(now['directories'])==set(v['directories']) and now['directories']['.'][:3]==v['directories']['.'][:3]
            for k,i in v['directories'].items():
                if k!='.':assert now['directories'][k]==i
        else:assert now==v
    verify_frozen_source(freeze)
    for q in fixed:exact(q)
    assert full_view(PRE)==current_pre
    print(json.dumps(dict(status='PRELAUNCH_PASS_NO_BUILD_EXECUTED',complete_Source_files=len(freeze['complete_files']),fixed_input_entries=len(fixed),preflight=own_pin,actual_history_bytes=actual_resources['artifact_bytes'],free_bytes=shutil.disk_usage(R).free,complete_joint_bytes=after_bytes,new_build_or_numeric_executed=False)))
if __name__=='__main__':main()

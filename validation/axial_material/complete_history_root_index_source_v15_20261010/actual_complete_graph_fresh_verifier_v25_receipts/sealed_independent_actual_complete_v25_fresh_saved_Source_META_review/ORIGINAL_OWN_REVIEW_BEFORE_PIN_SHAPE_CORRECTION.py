"""Finite saved SOURCE/small META review only; no candidate/API/gzip payload run."""
from pathlib import Path
import ast
import gzip
import hashlib
import json
import shutil
import stat
import sys
import tarfile

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
A=Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_graph_fresh_verifier_v25_sources'
E=B/'actual_complete_graph_fresh_verifier_v25_receipts'
H=A/'axial-material-complete-graph-inactive-audit-fresh-verifier-host-v25-20261010'
O=A/'axial-material-complete-graph-inactive-audit-fresh-verifier-v25-20261010'
ROOT=Path(__file__).resolve().parent
GN=('EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz')
checks=[]
reads={}
gzip_refs={}

def check(label,value,evidence=None):
    passed=type(value) is bool and value is True
    checks.append(dict(check=label,passed=passed,evidence=evidence))
    if not passed:raise AssertionError(label)

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def shape(ref):
    return type(ref) is dict and {'path','sha256','identity'}<=set(ref) and type(ref['identity']) is list and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']) and type(ref['sha256']) is str and len(ref['sha256'])==64 and all(c in '0123456789abcdef' for c in ref['sha256']) and ('size_bytes' not in ref or type(ref['size_bytes']) is int and ref['size_bytes']==ref['identity'][4])

def pin(p):
    p=Path(p);before=identity(p)
    assert stat.S_ISREG(before[2]) and before[3]==1
    digest=hashlib.sha256();n=0
    with p.open('rb') as stream:
        while data:=stream.read(1024*1024):digest.update(data);n+=len(data)
    assert identity(p)==before and n==before[4]
    value=dict(path=str(p),sha256=digest.hexdigest(),size_bytes=n,identity=before)
    if str(p) in reads:assert reads[str(p)]==value
    reads[str(p)]=value
    return value

def ref_match(ref,actual):
    return shape(ref) and all(ref[k]==actual[k] for k in ('path','sha256','identity')) and ('size_bytes' not in ref or ref['size_bytes']==actual['size_bytes'])

def pairs(rows):
    out={}
    for k,v in rows:
        if k in out:raise ValueError('duplicate saved META key')
        out[k]=v
    return out

def reject(v):raise ValueError('nonfinite saved META '+v)

def decode(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)

def read(p,sha=None):
    value=pin(p)
    if sha is not None:check('fixed actual SHA '+str(p),value['sha256']==sha)
    result=decode(Path(p).read_bytes());assert pin(p)==value
    return result,value

def view(root):
    paths=sorted(root.rglob('*'));assert not any(p.is_symlink() for p in paths)
    files=[]
    for p in paths:
        if p.is_file():
            if str(p) in gzip_refs:
                ref=gzip_refs[str(p)];assert shape(ref) and identity(p)==ref['identity']
                files.append({k:ref[k] for k in ('path','sha256','size_bytes','identity')})
            else:files.append(pin(p))
    return dict(root=str(root),files=files,directories={'.':identity(root),**{p.relative_to(root).as_posix():identity(p) for p in paths if p.is_dir()}})

def fullpin_check(ref):
    return shape(ref) and ref_match(ref,pin(ref['path']))

def archive_sources(info):
    package=info['original_complete_package'];wanted=dict(package['members'])
    name=Path(package['manifest']['path']).relative_to(package['root']).as_posix();wanted[name]=package['manifest']
    wanted_dirs={'.',*package['directories']};files={};dirs=set();captured={};parsed=[]
    path=Path(info['compressed_archive']['path']);check('complete Source archive actual pin '+path.name,fullpin_check(info['compressed_archive']))
    with path.open('rb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='rb') as zipped:
            with tarfile.open(fileobj=zipped,mode='r|') as archive:
                for entry in archive:
                    name=entry.name;assert name=='.' or not Path(name).is_absolute() and '..' not in Path(name).parts
                    if entry.isdir():assert name in wanted_dirs and name not in dirs;dirs.add(name);continue
                    assert entry.isfile() and name in wanted and name not in files
                    handle=archive.extractfile(entry);assert handle is not None
                    digest=hashlib.sha256();n=0;chunks=[]
                    keep=name in {'ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json','ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json','REVIEW.json','MANIFEST.json','ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_WITNESS.json','ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_RECORD.json'} or '/' not in name and name.endswith('.py')
                    with handle:
                        while data:=handle.read(1024*1024):
                            digest.update(data);n+=len(data)
                            if keep or name.endswith('.py'):chunks.append(data)
                    assert n==entry.size==wanted[name]['size_bytes'] and digest.hexdigest()==wanted[name]['sha256']
                    files[name]=dict(size_bytes=n,sha256=digest.hexdigest())
                    if keep:captured[name]=b''.join(chunks)
                    if name.endswith('.py'):ast.parse(b''.join(chunks));parsed.append(name)
            while zipped.read(1024*1024):pass
    check('all Source archive members manifest dirs SHA EOF '+path.name,set(files)==set(wanted) and dirs==wanted_dirs and files==info['full_decompressed_members'] and sorted(dirs)==info['full_decompressed_directories'] and len(files)==info['complete_file_count_including_manifest'] and len(dirs)==info['complete_directory_count_including_root'])
    check('honest complete lossless Source archive flags '+path.name,info['compression']=='lossless_tar_gzip_complete_members_manifest_and_directories' and info['all_member_bytes_and_SHA_verified_after_decompression'] is True and info['no_original_member_omission'] is True and info['runtime_Source_entrypoints_are_separate_original_bytes'] is True)
    return dict(archive_pin=info['compressed_archive'],all_members=files,all_directories=sorted(dirs),parsed_Source_files=parsed),captured

def literals(source):
    result={}
    for n in ast.parse(source).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:result[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return result

def write(name,value):
    p=ROOT/name;assert not p.exists();p.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def main():
    check('own finite stdlib saved Source META only',sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv)==1)
    summary,sp=read(E/'Root_actual_complete_qualification_postclose_summary.json','a8f87e41083804691ab4bf21726c472db016884eabbda462841c656be7fd33f6')
    ns,np=read(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json','2acfd8ee254a9abcad16c918ed3901cf22fd3cc81d16a4eb58743a9c80eff574')
    terminal,tp=read(E/'Root_actual_complete_qualification_tool_terminal_return.json','22e1a8a0dfb891ab5290ac283731a1b2042673f8cff2effdd0f867ad6ccca832')
    freeze,fp=read(E/'Root_final_complete_qualification_SOURCE_freeze.json')
    pre,pp=read(E/'Root_actual_complete_qualification_prelaunch_frozen_D_E.json')
    host,hp=read(H/'result.json');report,rp=read(O/'ACTUAL_REPORT.json');claim,cp=read(O/'ACTUAL_RUN_CLAIM.json');watch,wp=read(H/'run/admit.watchdog.json');stages,stp=read(H/'COMPLETE_FRESH_VERIFIER/stages.json')
    for name in GN:
        ref=next(v for v in ns['views']['O']['files'] if v['path']==str(O/name));assert shape(ref) and identity(O/name)==ref['identity'];gzip_refs[str(O/name)]=ref
    before={k:view(root) for k,root in [('H',H),('O',O),('D',D),('E',E)]}
    check('actual Root summary exact scope closed0',summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and summary['kind']=='fresh' and summary['status']=='ACTUAL_COMPLETE_CONTROLS_CLOSED0_PENDING_INDEPENDENT_SAVED_REVIEW' and summary['actual_closed'] is True and type(summary['actual_exit_code']) is int and summary['actual_exit_code']==0 and summary['actual_complete_control_success'] is True and summary['actual_failure'] is None and summary['actual_terminal_chunk_id']=='d1d77b')
    check('real Root terminal exact0 closed honest streams',terminal['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and terminal['kind']=='fresh' and terminal['closed'] is True and terminal['actual_tool_terminal_return_observed'] is True and terminal['merged_stdout_stderr_only'] is True and terminal['independent_stdout_captured'] is False and terminal['independent_stderr_captured'] is False and terminal['original_outputs_preserved'] is True)
    tr=terminal['terminal_tool_return'];check('true terminal integer0 no live session',type(tr['exit_code']) is int and tr['exit_code']==0 and tr['chunk_id']=='d1d77b' and ('session_id' not in tr or tr['session_id'] is None) and terminal['observations'][-1]['actual_tool_return']==tr and len(terminal['observations'])==2 and terminal['observations'][0]['actual_tool_return']['session_id']==97127)
    stdout=decode(tr['output']);check('exact Python Root stdout Source pins',ref_match(stdout['actual_host_result'],hp) and ref_match(stdout['actual_merged_child_stdout_stderr'],pin(H/'run/admit.log')) and stdout['status']==host['status'] and stdout['independent_child_stdout_captured'] is False and stdout['independent_child_stderr_captured'] is False)
    check('summary namespace terminal prelaunch fullpin coupling',summary['actual_terminal_receipt']==tp and summary['namespace_manifest']==np and summary['actual_prelaunch']==pp and ns['closed_actual_tool']==tp and pre['source_freeze']==fp)
    writer,writerp=read(E/'Root_actual_complete_qualification_postclose_tool_return.json');wtr=writer['terminal_tool_return'];wout=decode(wtr['output'])
    check('true postclose writer typed0 exact outputs',writer['schema']=='ROOT_V25_ACTUAL_COMPLETE_QUALIFICATION_POSTCLOSE_WRITER_TOOL_RETURN_V1' and writer['closed'] is True and type(wtr['exit_code']) is int and wtr['exit_code']==0 and wtr['chunk_id']=='75edf5' and ('session_id' not in wtr or wtr['session_id'] is None) and wout['summary']==sp and wout['namespace_manifest']==np and wout['actual_terminal_receipt']==tp and wout['actual_closed_success'] is True and wout['actual_exit_code']==0)
    check('frozen complete D10 root1 before after',len(pre['D']['files'])==10 and len(pre['D']['directories'])==1 and pre['D']==before['D']==ns['views']['D']==freeze['source_namespace'] and summary['frozen_D_files']==10 and summary['frozen_D_directories']==1)
    check('frozen initial E2 root1 saved unchanged',len(pre['E']['files'])==2 and len(pre['E']['directories'])==1 and summary['frozen_E_files']==2 and summary['frozen_E_directories']==1 and all(fullpin_check(v) for v in pre['E']['files']) and summary['whole_frozen_D_E_files_and_directories_unchanged_before_writer'] is True and ns['original_frozen_D_E_unchanged_before_writer'] is True)
    check('whole saved H O namespace exact SourceMETA and gzip lstat',before['H']==ns['views']['H'] and all(before['O'][k]==ns['views']['O'][k] for k in ['root','files','directories']) and ns['views']['O']['original_fixture_symlinks']==[] and ns['all_declared_members_fresh_full_EOF_SHA7ID'] is True)
    check('whole saved E original files unchanged and writer self exclusions honest',all(fullpin_check(v) for v in ns['views']['E']['files']) and ns['E_explicit_self_excluded_current_writer_outputs']==[str(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json'),str(E/'Root_actual_complete_qualification_postclose_summary.json')] and len(before['E']['files'])==len(ns['views']['E']['files'])+3)
    archives={};captured={}
    for name,info in freeze['lossless_complete_Source_archives'].items():archives[name],captured[name]=archive_sources(info)
    bound=captured['sealed_full_ROOT_BOUND_qualification_SOURCE'];peer=captured['sealed_independent_complete_BOUND_qualification_SOURCE_review']
    bm=decode(bound['ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json']);pr=decode(peer['REVIEW.json']);bp=freeze['complete_bound_source']['manifest']
    check('complete bound Source provenance matches original676 peer',bp['sha256']=='2326404a413cf988d86fa3a980cdb1f1fbb91bbf532900e9056d633740940839' and pr['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_BOUND_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_REVIEW_V1' and pr['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION' and pr['source_only'] is True and pr['all_checks_typed_true'] is True and pr['blockers']==[] and type(pr['check_count']) is int and pr['check_count']==len(pr['checks'])==676 and all(type(c['passed']) is bool and c['passed'] is True for c in pr['checks']) and pr['bound_manifest_pin']==bp and hashlib.sha256(peer['REVIEW.json']).hexdigest()==freeze['bound_Source_peer_report']['sha256']=='7379cd4563fa6698e847291643f5b72d45c70c31e0c031719a630514eda0a76f')
    roles=['pure_helper_controls.py','pure_helper_controls_host.py','fresh_verifier_controls.py','fresh_verifier_host.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py']
    check('all five runtime Source entire bytes match complete bound archive',all((D/name).read_bytes()==bound[name] and pr['qualified_bound_Source_pins'][name]['sha256']==hashlib.sha256(bound[name]).hexdigest() for name in roles))
    inverse=decode(bound['ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json']);check('complete original all4 byteAST inverse source proof preserved',inverse['schema']=='ROOT_V25_ACTUAL_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_BINDING_INVERSES_V1' and inverse['new_actual_helper_qualification'] is None and inverse['six_future_business_pins']==[None]*6 and len(inverse['all_four_full_Source_bindings'])==4 and all(v['all_definitions_bytes_AST_unchanged'] is True and v['full_template_bytes_AST_inverse'] is True for v in inverse['all_four_full_Source_bindings'].values()))
    ds=(D/'fresh_verifier_controls.py').read_text();hs=(D/'fresh_verifier_host.py').read_text();ms=(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py').read_text();dg=literals(ds);hg=literals(hs);mg=literals(ms)
    check('complete source guard scope full27 full37112 gzip predicates retained',all(s in hs for s in ['OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','helper.guard_admission(full)','DynamicHistoryResources','declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)','json.dumps(expected,**encoder)!=json.dumps(verified,**encoder)','_gzip_object','list(verified)!=RETURN_FIELDS']) and all(s in ds for s in ['exact_value(expected,verified','len(actual_paths)==len(set(actual_paths))==37112','set(actual_paths)==paths|{GRAPH_PIN[','trace[\'subprocess_records\']==[]','trace=audit.snapshot(_consume=True)','del trace','full_consumed_snapshot_wire_compare']))
    check('whole Source namespace unchanged runtime',host['source_namespace_before']==host['source_namespace_after'] and host['source_namespace_before']['complete_dynamic_before_after'] is True and host['source_namespace_before']['files']==pre['D']['files'])
    check('fixed inputs all Source graph META before after unchanged',report['fixed_inputs_before']==report['fixed_inputs_after'] and set(report['fixed_inputs_before'])=={'driver','old_parent','new_helper','stored_graph','private_snapshot_controls'} and all(shape(v) and identity(v['path'])==v['identity'] for v in report['fixed_inputs_before'].values()) and all(shape(v) and identity(v['path'])==v['identity'] for v in host['input_sources']) and len(host['input_sources'])==20)
    source_inputs={v['path']:pin(v['path']) for v in host['input_sources'] if Path(v['path']).suffix=='.py'}
    check('all normal host Source inputs fullEOF SHA7ID unchanged',all(ref_match(v,source_inputs[v['path']]) for v in host['input_sources'] if v['path'] in source_inputs) and fullpin_check(freeze['actual_installed_helper']) and all(fullpin_check(v) for v in freeze['original_helper_Q_canonical_fullEOF_unchanged']))
    check('one genuine child PASS full stages',stages['stages']==host['stage_records'] and len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['label']=='run/admit' and watch==host['watchdog'] and watch['command']==host['actual_canonical_command']==host['stage_records'][0]['command'] and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
    check('original real timing RSS caps unchanged',host['whole_wall_cap_seconds']==1800 and host['stage_wall_cap_seconds']==600 and host['rss_cap_mib']==watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=host['stage_records'][0]['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512 and host['whole_seconds']<1800 and summary['actual_child_seconds']==watch['elapsed_seconds'] and summary['actual_own_child_sampled_peak_RSS_MiB']==watch['sampled_peak_rss_mib'] and summary['whole_host_seconds']==host['whole_seconds'])
    check('actual host child PID complete claim link',type(watch['pid']) is int and watch['pid']==claim['PID']==report['PID']==host['actual_full_controls']['actual_child_PID'] and claim['parent_PID']==report['parent_PID']==host['actual_host_PID'] and claim['phase']=='helper_complete_fresh_verifier_control' and host['actual_full_controls']['actual_claim_parent_and_watch_PID_match'] is True)
    check('original full report resource contract',tuple(report[k] for k in ['whole_host_seconds','stage_seconds','rss_mib','joint_HOST_SOURCE_OUT_archive_bytes','history_bytes','min_free_bytes','threads','children','retries'])==(1800,600,512,64*2**20,96*2**30,8*2**30,1,1,0) and tuple(host[k] for k in ['archive_cap_bytes','threads','children_at_once','retries'])==(64*2**20,1,1,0) and host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False)
    resource_states=[host['resources_before'],host['resources_after'],host['stage_records'][0]['resource_before'],host['stage_records'][0]['resource_after']]
    check('complete original dynamic history96 free8 saved resource checks',all(v['min_free_bytes']==8*2**30 and v['artifact_budget_bytes']==96*2**30 and v['artifact_bytes']<96*2**30 and v['disk_free_bytes']>=8*2**30 and v['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and all(Path(p).is_relative_to(A) and Path(p)!=A for p in v['declared_resource_roots']) for v in resource_states) and host['resources_before']['artifact_bytes']+64*2**20<96*2**30 and host['resources_before']['disk_free_bytes']-64*2**20>=8*2**30)
    check('complete full output6 exact fields and honest streams',set(p.name for p in O.iterdir())==set(GN)|{'ACTUAL_REPORT.json','ACTUAL_RUN_CLAIM.json','private_trace_fixture.txt'} and host['independent_child_stdout_captured'] is False and host['independent_child_stderr_captured'] is False and ref_match(host['actual_control_report'],rp) and ref_match(host['actual_full_controls']['actual_report'],rp) and ref_match(host['actual_full_controls']['actual_claim'],cp))
    check('all public27 return field order retained',report['complete_return_fields_retained']==hg['RETURN_FIELDS'] and len(hg['RETURN_FIELDS'])==27 and report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is True and host['actual_full_controls']['complete_current_graph_verifier_returned'] is True)
    check('all actual37111 plus graph37112 fresh opens retained',report['actual_complete_trace_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True) and report['independent_full_saved_graph_metadata']['canonical_files']==37111 and report['independent_full_saved_graph_metadata']['requirement_row_count']==238441 and len(report['independent_full_saved_graph_metadata']['complete_coverage_fields'])==9)
    positive=report['private_trace_controls']['positive_controls'];negative=report['private_trace_controls']['rejections']
    check('all original private trace4positive3reject full evidence',len(positive)==4 and {v['case'] for v in positive}=={'default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True'} and all(v['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True and (v.get('caller_full_identity_type_order_value_floatbits_unchanged') is True or v.get('owned_list_completely_cleared') is True) for v in positive) and len(negative)==3 and {v['case'] for v in negative}=={'nonbool_consume','tuple_True','list_subclass_True'} and all(v['rejected'] is True and v['class_name']=='InputGraphError' and v['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for v in negative) and report['private_trace_controls']['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is True)
    snap=report['private_full_inactive_audit_snapshot_controls'];wire=snap['complete_consumed_vs_default_wire'];default=snap['default_complete_descriptor_type_order_floatbit_pin']
    check('same actual inactive audit full9 fields type order bits and clear',all(snap[k] is True for k in ['default_snapshot_full_original_records_unchanged','owned_same_builtin_records_map_completely_cleared','all_other_audit_state_unchanged','all_nine_fields_full_type_order_value_floatbits_and_counts_equal','no_second_graph_or_input_phase_substituted','all37112_actual_reads_from_same_genuine_phase','no_cross_phase_hash_or_stat_cache']) and default==snap['consumed_complete_descriptor_type_order_floatbit_pin'] and default['complete_node_count']==779371 and default['no_fields_or_rows_selected'] is True and default['mutable_identities_included'] is False and wire['complete_nine_snapshot_fields']==mg['SNAPSHOT_FIELDS']==hg['TRACE_FIELDS'] and len(mg['SNAPSHOT_FIELDS'])==9 and wire['uncompressed_JSON_bytes']==21411449 and all(wire[k] is True for k in ['every_default_and_consumed_wire_byte_compared','full_gzip_EOF_verified','no_fields_or_records_selected']) and snap['new_helper_qualification_created'] is False and snap['business_or_science_qualification_created'] is False)
    reportgz=[report[k] for k in ['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace']]
    check('three complete gzip Rootpins lstat fullEOF Source evidence no replay',all(shape(v) and identity(v['path'])==v['identity'] and v['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and v['no_fields_or_records_filtered'] is True and ref_match(v,gzip_refs[v['path']]) for v in reportgz) and reportgz[0]['uncompressed_JSON_bytes']==reportgz[1]['uncompressed_JSON_bytes']==1220216 and reportgz[0]['uncompressed_JSON_sha256']==reportgz[1]['uncompressed_JSON_sha256'] and reportgz[0]['sha256']==reportgz[1]['sha256'] and snap['default_full_trace_gzip']==reportgz[2] and wire['uncompressed_JSON_sha256']==reportgz[2]['uncompressed_JSON_sha256'] and wire['uncompressed_JSON_bytes']==reportgz[2]['uncompressed_JSON_bytes'])
    check('all success helper graph trace pins consistent',report['actual_success_pins']==dict(helper=report['fixed_inputs_before']['new_helper'],graph=report['fixed_inputs_before']['stored_graph'],full_return=reportgz[1],full_trace=reportgz[2]) and claim['helper']==report['fixed_inputs_before']['new_helper'] and claim['graph']==report['fixed_inputs_before']['stored_graph'] and claim['driver']==report['fixed_inputs_before']['driver'])
    false_report=['business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified']
    false_summary=['actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']
    check('saved metadata honest no newQ business or science credit',all(report[k] is False for k in false_report) and all(summary[k] is False for k in false_summary) and summary['new_actual_helper_qualification'] is None and freeze['new_actual_helper_qualification'] is None and freeze['six_future_business_pins']==[None]*6 and host['UNKNOWN_Q'] is None and host['UNKNOWN_BUSINESS_PINS'] is None and summary['independent_saved_review_pending'] is True)
    snapshot_bytes=sum(v['size_bytes'] for k in ['H','O','D','E'] for v in ns['views'][k]['files'])+sp['size_bytes']+np['size_bytes']
    current_bytes=sum(v['size_bytes'] for k in before for v in before[k]['files'])
    check('original64MiB full HODE saved writer snapshot and laterreceipt honest',summary['normal_host_archive_scope']=='H+O+D+E' and summary['original_archive_cap_bytes']==64*2**20 and summary['complete_HODE_bytes']==snapshot_bytes==5203326 and summary['normal_HOD_bytes']==sum(v['size_bytes'] for k in ['H','O','D'] for v in before[k]['files'])==4338035 and current_bytes==snapshot_bytes+writerp['size_bytes'] and current_bytes<64*2**20 and summary['original_normal_archive_under_cap'] is True and summary['Root_separate_conservative_HODE_under_64MiB'] is True)
    after={k:view(root) for k,root in [('H',H),('O',O),('D',D),('E',E)]}
    check('all reviewed HODE files dirs current before after unchanged',after==before and all(pin(p)==v for p,v in list(reads.items())))
    write('COMPLETE_SAVED_SOURCE_META_EVIDENCE_BEFORE_AFTER.json',dict(source_only=True,namespace_before=before,namespace_after=after,full_Source_META_read_pins=reads,result_gzip_Rootpins_lstat_only_no_redecode=gzip_refs,complete_lossless_Source_archive_reviews=archives,original_Root_writer_snapshot_HODE_bytes=snapshot_bytes,current_all_HODE_including_actual_writer_receipt_bytes=current_bytes))
    copies=ROOT/'COMPLETE_REVIEWED_SMALL_META_AND_RUNTIME_SOURCE';copies.mkdir()
    for path in list(reads):
        q=Path(path)
        if q.parent==D and q.suffix=='.py' or q.parent==E or q in [H/'result.json',H/'run/admit.watchdog.json',H/'run/admit.log',H/'COMPLETE_FRESH_VERIFIER/stages.json',O/'ACTUAL_REPORT.json',O/'ACTUAL_RUN_CLAIM.json']:
            if q.suffix=='.gz':continue
            name=('D__' if q.is_relative_to(D) else 'E__' if q.is_relative_to(E) else 'H__' if q.is_relative_to(H) else 'O__')+q.name
            shutil.copyfile(q,copies/name)
    result=dict(schema='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_FRESH_SAVED_SOURCE_META_REVIEW_V1',status='PASS_SAVED_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_META_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,actual_Root_fresh_summary_pin=sp,actual_Root_fresh_terminal_pin=tp,actual_complete_namespace_manifest_pin=np,actual_postclose_writer_tool_receipt_pin=writerp,actual_host_result_pin=hp,actual_control_report_pin=rp,actual_watchdog_pin=wp,actual_claim_pin=cp,actual_prelaunch_pin=pp,actual_complete_Source_freeze_pin=fp,actual_Root_terminal_exit_code=0,actual_Root_terminal_closed=True,actual_Root_terminal_chunk_id='d1d77b',actual_genuine_child_elapsed_seconds=watch['elapsed_seconds'],actual_genuine_child_peak_RSS_MiB=watch['sampled_peak_rss_mib'],actual_whole_host_seconds=host['whole_seconds'],full27fields_37112reads_three_original_gzips_and_private_full9_snapshot_saved_evidence_verified=True,complete_Source_archives_streamed_all_members_manifest_directories_SHA_EOF=True,complete_original_Source_scope_cap_and_genuine_guard_evidence_retained=True,Root_gzip_complete_wire_EOF_type_order_bits_evidence_reviewed_without_redo=True,gzip_payloads_or_material_arrays_opened_or_decoded=False,actual_original_writer_HODE_bytes=snapshot_bytes,current_complete_HODE_with_actual_writer_receipt_bytes=current_bytes,original64MiB_cap_retained=True,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,actual_complete_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,candidate_helper_guard_controller_API_or_solver_executed=False,independent_stdout_or_stderr_not_claimed=True)
    write('REVIEW.json',result)
    print(json.dumps(dict(status=result['status'],source_only=True,check_count=result['check_count'],review_pin=pin(ROOT/'REVIEW.json'),original_writer_HODE_bytes=snapshot_bytes,current_HODE_bytes=current_bytes,output=str(ROOT)),separators=(',',':')))

if __name__=='__main__':main()

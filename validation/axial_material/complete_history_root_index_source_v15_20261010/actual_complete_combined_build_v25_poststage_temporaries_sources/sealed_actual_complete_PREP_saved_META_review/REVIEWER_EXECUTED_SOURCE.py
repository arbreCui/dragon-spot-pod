"""UNREADY independent saved PREP Source/small-META reviewer.
Run only after Root supplies genuine new CLOSED0 PREP/writer and all18 fullpins.
All Source is inspected, never imported or executed. Business payload files
are checked against Root's saved full-EOF pins and present exact7ID only;
graph/trace/gzip/material/native payloads are never read by this reviewer.
"""
import argparse,ast,hashlib,json,math,os,stat,struct,sys
from pathlib import Path
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010';ART=R/'validation/artifacts'
D=B/'actual_complete_combined_prepare_v25_poststage_temporaries_sources';E=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
H=ART/'axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';HELPER=R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py';CASE=R/'validation/axial_material/case_spec.json'
QSHA='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b';CSHA='6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649';HSHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children=1,retries=0)
KEYS=('actual_PREP_summary_pin','actual_PREP_terminal_pin','actual_PREP_metadata_writer_terminal_pin','actual_complete_namespace_manifest_pin','actual_prelaunch_Source_freeze_pin','actual_final_prelaunch_reserve_pin','actual_E_prelaunch_snapshot_pin','actual_E_postclose_snapshot_pin','actual_installed_canonical_pin','actual_Q_pin','actual_Q_writer_terminal_pin','actual_Q_saved_peer_pin','actual_Q_saved_peer_retention_pin','actual_bound_Source_peer_report_pin','actual_bound_Source_peer_manifest_pin','actual_bound_Source_peer_seal_pin','actual_root_source_install_record_pin','actual_case_spec_pin')
CHECKS=[];PINS={};ROOT_EOF_PINS={};SOURCE_DEFINITION_COUNTS={}
def ck(name,v):
    if any(q['check']==name for q in CHECKS):raise ValueError('duplicate check '+name)
    if type(v) is not bool or v is not True:raise ValueError(name)
    CHECKS.append(dict(check=name,passed=True))
def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return list(a)==list(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) in(list,tuple):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    if type(a) is float:return struct.pack('>d',a)==struct.pack('>d',b)
    return a==b
def ident(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p):
    p=Path(p);a=ident(p)
    if not(p.is_absolute() and not any(x.is_symlink() for x in(p,*p.parents)) and stat.S_ISREG(a[2]) and a[3]==1):raise ValueError('ordinary singlelink Source/META')
    if p.name in ('input_graph.json','input_creation_python_open_trace.json') or p.suffix in('.gz','.xsm','.sqlite','.db','.h5','.hdf5','.so','.a','.o') or p.name.startswith('draglib'):raise ValueError('business payload EOF read forbidden')
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=a:raise ValueError('Source/META changed while full EOF')
    q=dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
    if str(p) in PINS and not exact(PINS[str(p)],q):raise ValueError('Source/META repeated pin changed')
    PINS[str(p)]=q;return q
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
def meta(p):
    q=full(p);v=strict(Path(p).read_bytes())
    if not exact(full(p),q):raise ValueError('META parse changed')
    return v
def ref(q,read_bytes=True):
    if type(q) is not dict or not {'path','sha256'}.issubset(q):raise ValueError('actual typed pin')
    if type(q['sha256']) is not str or len(q['sha256'])!=64 or q['sha256']=='0'*64 or any(c not in '0123456789abcdef' for c in q['sha256']):raise ValueError('full actual SHA')
    if read_bytes:
        observed=full(q['path'])
        if any(not exact(observed[k],q[k]) for k in q if k in('path','sha256','size_bytes','identity')):raise ValueError('actual Source/META fullpin')
        return observed
    i=q['identity'];p=Path(q['path'])
    if not(type(i) is list and len(i)==7 and all(type(x) is int for x in i) and stat.S_ISREG(i[2]) and i[3]==1 and p.is_absolute() and not any(x.is_symlink() for x in(p,*p.parents)) and ident(p)==i and ('size_bytes' not in q or q['size_bytes']==i[4])):raise ValueError('Root observed fullEOF payload pin current7ID')
    v=dict(path=q['path'],sha256=q['sha256'],size_bytes=i[4],identity=i)
    if str(p) in ROOT_EOF_PINS and not exact(ROOT_EOF_PINS[str(p)],v):raise ValueError('Root payload observation changed')
    ROOT_EOF_PINS[str(p)]=v;return v
def source(p):
    q=full(p);raw=Path(p).read_bytes();t=ast.parse(raw)
    if not exact(full(p),q):raise ValueError('Source AST read changed')
    SOURCE_DEFINITION_COUNTS[str(p)]=len([n for n in ast.walk(t) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))])
    return raw.decode(),t
def tree(root,source_bytes=False):
    root=Path(root);ri=ident(root);fs={};ds={}
    if root.is_symlink() or not root.is_dir():raise ValueError('actual regular namespace')
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));i=ident(p)
        if stat.S_ISDIR(i[2]):ds[rel]=i
        elif stat.S_ISREG(i[2]):fs[rel]=full(p) if source_bytes else i
        else:raise ValueError('nonregular or alias namespace')
    if ident(root)!=ri:raise ValueError('namespace changed during independent view')
    return dict(root=str(root),root_identity=ri,files=fs,directories=ds,symlinks={})
def namespace(saved,root,source_bytes=False):
    v=tree(root,source_bytes);ds=saved['directories']
    if type(ds) is list:ds={q['path']:q['identity'] for q in ds}
    if ds!=v['directories'] or set(saved['files'])!=set(v['files']) or saved['root']!=str(root) or saved['symlinks']!={}:raise ValueError('whole namespace domains and directory7ID')
    for rel,q in saved['files'].items():
        if q['path']!=str(root/rel):raise ValueError('whole namespace physical path')
        observed=ref(q,source_bytes)
        if source_bytes and not exact(observed,v['files'][rel]):raise ValueError('whole Source namespace EOF')
    return v
def terminal(doc,wanted):
    fields=[k for k in('terminal_tool_return','actual_tool_return','exec_command_result') if k in doc]
    if not fields:raise ValueError('actual original terminal object')
    t=doc[fields[0]]
    if any(not exact(doc[k],t) for k in fields[1:]):raise ValueError('actual terminal alias disagreement')
    if not(doc['closed'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and t['chunk_id']==wanted and all(doc.get(k,False) is False for k in('session_repolled_after_close','closed_session_repolled'))):raise ValueError('actual strict closed0 no repoll')
    return t
def caps(d,mapping):
    return all(type(d[k]) is int and d[k]==CAPS[v] for k,v in mapping.items())
def peer(r,schema,status):
    return r['schema']==schema and r['status']==status and r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[] and type(r['check_count']) is int and r['check_count']==len(r['checks']) and len({c['check'] for c in r['checks']})==len(r['checks']) and all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--actual-Root-inputs',required=True);ap.add_argument('--actual-Root-inputs-sha256',required=True);ap.add_argument('--fresh-TMP-output',required=True);a=ap.parse_args();out=Path(a.fresh_TMP_output)
    if not(out.is_absolute() and out.is_relative_to(Path('/private/tmp')) and not os.path.lexists(out)):raise ValueError('fresh review TMP')
    inputpin=full(a.actual_Root_inputs);cfg=meta(a.actual_Root_inputs)
    ck('real Root18 actual fullpin config only after newPREP and writer closed0',inputpin['sha256']==a.actual_Root_inputs_sha256 and cfg['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_SAVED_REVIEW_INPUTS_V1' and cfg['status']=='ACTUAL_ROOT_COMPLETE_PREP_AND_METADATA_WRITER_CLOSED0' and set(cfg['actual_terminal_chunks'])=={'PREP','metadata_writer'} and all(type(cfg[k]) is dict and set(cfg[k])=={'path','sha256','size_bytes','identity'} for k in KEYS))
    given={k:ref(cfg[k]) for k in KEYS};fixed={'actual_PREP_summary_pin':E/'Root_actual_complete_combined_prepare_summary.json','actual_PREP_terminal_pin':E/'Root_actual_prepare_tool_terminal_return.json','actual_PREP_metadata_writer_terminal_pin':E/'Root_actual_prepare_metadata_writer_tool_terminal_return.json','actual_complete_namespace_manifest_pin':E/'Root_actual_complete_prepare_namespace_manifest.json','actual_prelaunch_Source_freeze_pin':E/'Root_prelaunch_complete_source_freeze.json','actual_final_prelaunch_reserve_pin':E/'Root_final_prelaunch_source_and_reserve_check.json','actual_installed_canonical_pin':C,'actual_Q_pin':Q,'actual_root_source_install_record_pin':D/'Root_actual_complete_SOURCE_install_record.json','actual_case_spec_pin':CASE}
    ck('all actual18 config proof roles fixed newPREP paths no old namespace substitution',all(given[k]['path']==str(p) for k,p in fixed.items()))
    rt_doc=meta(given['actual_PREP_terminal_pin']['path']);rt=terminal(rt_doc,cfg['actual_terminal_chunks']['PREP']);wt_doc=meta(given['actual_PREP_metadata_writer_terminal_pin']['path']);wt=terminal(wt_doc,cfg['actual_terminal_chunks']['metadata_writer'])
    events=rt_doc['all_actual_tool_observations'];initial=rt_doc['initial_tool_return'];sid=initial['session_id']
    ck('genuine newRoot c1d780 session48765 complete live observations closed0 no oldPREP substitution',rt_doc['observed_terminal'] is True and rt_doc['closed_session_not_repolled'] is True and rt_doc['actual_tool_return_not_synthetic'] is True and initial['chunk_id']=='c1d780' and type(sid) is int and sid==48765 and events[0]==initial and exact(events[-1],rt) and all(q['session_id']==sid and 'exit_code' not in q for q in events[:-1]))
    ck('genuine frozen postclose writer strict0 after actual newPREP',wt_doc['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_METADATA_POSTCLOSE_WRITER_TOOL_RETURN_V1' and wt_doc['observed_terminal'] is True and wt_doc['actual_tool_return_not_synthetic'] is True and wt_doc['closed_session_not_repolled'] is True and exact(wt_doc['initial_tool_return'],wt) and wt_doc['new_build_whole_INPUT_native_or_science_qualification_created'] is False)
    summary=meta(E/'Root_actual_complete_combined_prepare_summary.json');ns=meta(E/'Root_actual_complete_prepare_namespace_manifest.json');freeze=meta(E/'Root_prelaunch_complete_source_freeze.json');reserve=meta(E/'Root_final_prelaunch_source_and_reserve_check.json');install=meta(D/'Root_actual_complete_SOURCE_install_record.json');request=meta(D/'Root_actual_Source_META_install_request.byte_exact.json')
    ck('actual newPREP summary writer full5 namespaces original order PREP-only',summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD' and ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and ns['no_build_or_native_credit'] is True and [q['root'] for q in ns['namespaces']]==[str(p) for p in(H,S,O,T,D)] and ref(summary['namespace_manifest'])==given['actual_complete_namespace_manifest_pin'])
    writer_output=strict(wt['output'])
    ck('real writer4bfa1b raw tool stdout exactly current summary original metrics no reconstruction',wt['chunk_id']=='4bfa1b' and writer_output=={k:summary[k] for k in ('status','whole_seconds','child_seconds','sampled_peak_rss_mib','joint_archive_bytes','all_source_files_verified_count')} and ident(E/'Root_actual_prepare_tool_terminal_return.json')[5]<=ident(E/'Root_actual_complete_combined_prepare_summary.json')[5]<=ident(E/'Root_actual_prepare_metadata_writer_tool_terminal_return.json')[5])
    views={str(root):namespace(saved,root,root==D) for root,saved in zip((H,S,O,T,D),ns['namespaces'])}
    epostdoc=meta(given['actual_E_postclose_snapshot_pin']['path']);epost=epostdoc['namespace'];views[str(E)]=namespace(epost,E);epre=meta(given['actual_E_prelaunch_snapshot_pin']['path'])['namespace']
    ck('whole saved6namespace identity file domains dirs full RootEOF pins closure',len(views)==6 and all(v['symlinks']=={} for v in views.values()) and set(epre['files']).issubset(epost['files']) and all(exact(ref(q),ref(epost['files'][r])) for r,q in epre['files'].items()) and epostdoc['phase']=='postclose' and epostdoc['root_identity_at_snapshot']==views[str(E)]['root_identity'])
    dv=views[str(D)];ck('actual complete297D34dirs no SOURCE append fullEOF7ID freeze',freeze['file_count']==297 and freeze['directory_count']==34 and len(dv['files'])==297 and freeze['complete_files']==dv['files'] and freeze['complete_directories']==dv['directories'] and freeze['source_root_identity']==dv['root_identity'] and freeze['no_SOURCE_append_after_freeze'] is True and freeze['all_file_SHA7ID_recorded'] is True)
    owner_rows=install['complete_Source_owner_copies'];owner_total=0
    for row in owner_rows:
        v=row['original'];prefix=row['destination_prefix'];current=tree(v['root'],True)
        if current['files']!=v['files'] or {'.':current['root_identity'],**current['directories']}!=v['directories']:raise ValueError('whole original Source owner actual EOF7ID')
        owner_total+=len(v['files'])
        for rel,q in v['files'].items():
            saved=ref(freeze['complete_files'][prefix+'/'+rel])
            if (saved['sha256'],saved['size_bytes'])!=(q['sha256'],q['size_bytes']):raise ValueError('all sourceowner files retained losslessly')
    ck('all7 Source owner full trees lossless280 Source members plus17 top files',len(owner_rows)==7 and owner_total==280 and len(freeze['complete_files'])==owner_total+17 and install['original_parent_Source_file_count']==135 and install['metadata_writer_and_prelaunch_included_before_freeze'] is True and install['new_PREP_or_build_executed'] is False)
    for name,record in install['complete_enumerable_package_copies'].items():
        if 'original' in record and 'saved' in record:
            a1=ref(record['original']);b1=ref(record['saved'])
            if(a1['sha256'],a1['size_bytes'])!=(b1['sha256'],b1['size_bytes']):raise ValueError('explicit top Sourcecopy byte equality')
    ck('installed request Source only utility30 peer boundPREP24 roles fully coupled',request['schema']=='ROOT_V25_POSTSTAGE_FINITE_ACTUAL_SOURCE_META_INSTALL_REQUEST_V1' and request['phase']=='PREP' and request['actual_new_PREP'] is None and all(v is None for v in request['new_business_results'].values()) and request['installation_executed'] is False and install['installed_request']==full(D/'Root_actual_Source_META_install_request.byte_exact.json') and install['canonical_installed']==given['actual_installed_canonical_pin'])
    bp=meta(given['actual_bound_Source_peer_report_pin']['path']);up=meta(request['utility']['peer']['review']['path']);ck('real saved Source-only actual24bound and30utility independent peers no transferred business success',peer(bp,'INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1','PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED') and bp['check_count']==24 and peer(up,'INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1','PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION') and up['check_count']==30 and bp['actual_complete_bound_Source_manifest_pin']==request['bound']['manifest'] and up['qualified_complete_utility_manifest_pin']==request['utility']['manifest'])
    for family,report in [('bound',bp),('utility',up)]:
        proof=request[family]['peer'];mf=meta(proof['manifest']['path']);seal=meta(proof['seal']['path']);st=terminal(seal,seal['terminal_tool_return']['chunk_id']);so=strict(st['output']);pv=tree(Path(proof['manifest']['path']).parent,True)
        if not(so['manifest_pin']==ref(proof['manifest']) and so['review_pin']==ref(proof['review']) and mf['members']=={k:q for k,q in pv['files'].items() if k!='MANIFEST.json'} and mf['directories']=={'.':pv['root_identity'],**pv['directories']} and mf['member_count']==len(mf['members'])):raise ValueError('whole actual independent Source peer manifest seal closure')
    ck('both actual original bound24 utility30 Source peer whole packages actual true seal coupled',ref(request['bound']['peer']['manifest'])==given['actual_bound_Source_peer_manifest_pin'] and ref(request['bound']['peer']['seal'])==given['actual_bound_Source_peer_seal_pin'] and ref(request['bound']['peer']['review'])==given['actual_bound_Source_peer_report_pin'])
    for role,p in [('canonical',C),('prepare_host',D/'combined_prepare_host.py'),('prepare_writer',D/'write_actual_prepare_terminal.py')]:
        q=ref(bp['actual_ready_role_Source_pins'][role]);installed=full(p);source(p)
        if(q['sha256'],q['size_bytes'])!=(installed['sha256'],installed['size_bytes']):raise ValueError('qualified bound Source role installedbyte exactly')
    for name,q in up['qualified_role_Source_pins'].items():
        actual=full(D/name);source(D/name)
        if(actual['sha256'],actual['size_bytes'])!=(q['sha256'],q['size_bytes']):raise ValueError('qualified all7 utility roles actual installedSource')
    h=meta(H/'result.json');w=meta(H/'run/prepare.watchdog.json');d=meta(O/'declaration.json');sa=meta(S/'source_admission.json');formal=meta(T/'declaration_terminal_return.json');cp=d['actual_external_prepare_terminal_contract'];stage_doc=meta(H/'COMBINED_PREPARATION/stages.json')['stages'];all_inputs=h['input_sources']+[h['original_helper'],h['resource_factory']]
    prefix=install['exact_original_host_prefix_seven_input_pins'];ordered=prefix+[{k:q[k] for k in('path','sha256','identity')} for rel,q in sorted(freeze['complete_files'].items())]
    ck('exact304 ordered host Sourceinputs plus2 total306 originalprefix allD retain no shortening',len(ordered)==304 and exact(h['input_sources'],ordered) and exact(reserve['exact_original_host_input_sources'],ordered) and len(all_inputs)==306 and exact(ns['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged'],all_inputs) and summary['all_original_pinned_inputs_unchanged_count']==306)
    for q in all_inputs:ref(q)
    launch='env -u PYTHONOPTIMIZE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'combined_prepare_host.py')+' > '+str(E/'parent_stdout.log')+' 2> '+str(E/'parent_stderr.log')
    writer_launch='env -u PYTHONOPTIMIZE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'write_actual_prepare_terminal.py')
    ck('actual Root launches fixed fullSource originalPython B unoptimized five threads and frozen writer',rt_doc['actual_launch_arguments']['cmd']==launch and wt_doc['actual_launch_arguments']['cmd']==writer_launch and reserve['metadata_writer_already_frozen'] is True and reserve['all_new_H_S_O_T_absent'] is True and reserve['PREP_or_build_launched'] is False and reserve['native_or_science_qualified'] is False and caps(freeze,dict(original_whole_seconds='whole_seconds',original_stage_seconds='stage_seconds',original_RSS_mib='rss_mib',original_joint_archive_bytes='joint_archive_bytes',original_history_bytes='history_bytes',original_free_floor_bytes='free_floor_bytes',original_threads='threads',original_children='children',original_retries='retries')))
    command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(C),'prepare-build'];stored=strict(json.dumps(h['stage_records'],sort_keys=True,allow_nan=False));stage=stage_doc[0]
    ck('one genuine original supervised PREP child stage savedwatchdog exact full values',len(stage_doc)==1 and exact(stage_doc,stored) and stage['status']=='PASS' and stage['label']=='run/prepare' and exact(h['watchdog'],w) and type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True and exact(h['actual_canonical_command'],command) and exact(w['command'],command) and exact(formal['command'],command) and exact(cp['command'],command))
    ck('actual PREP elapsed RSS original bounds finite no prediction of futureBUILD',all(type(v) in(int,float) and math.isfinite(v) for v in(h['whole_seconds'],w['elapsed_seconds'],w['sampled_peak_rss_mib'])) and 0<w['elapsed_seconds']<=w['wall_cap_seconds']<=600 and w['elapsed_seconds']<=h['whole_seconds']<1800 and 0<=w['sampled_peak_rss_mib']<512 and w['rss_cap_mib']==512 and exact(summary['whole_seconds'],h['whole_seconds']) and exact(summary['child_seconds'],w['elapsed_seconds']) and exact(summary['sampled_peak_rss_mib'],w['sampled_peak_rss_mib']))
    ck('all original host declaration summary frozen Source caps exact9int',caps(h,dict(whole_wall_cap_seconds='whole_seconds',stage_wall_cap_seconds='stage_seconds',rss_cap_mib='rss_mib',archive_cap_bytes='joint_archive_bytes',threads='threads',children_at_once='children',retries='retries')) and caps(d,dict(total_wall_seconds='whole_seconds',stage_wall_seconds='stage_seconds',rss_cap_mib='rss_mib',archive_reserve_bytes='joint_archive_bytes',artifact_budget_bytes='history_bytes',min_free_bytes='free_floor_bytes',threads='threads',numeric_children_at_once='children',retries='retries')) and caps(summary,dict(whole_wall_cap_seconds='whole_seconds',stage_wall_cap_seconds='stage_seconds',rss_mib='rss_mib',joint_archive_cap_bytes='joint_archive_bytes',history_cap_bytes='history_bytes',free_floor_bytes='free_floor_bytes',threads='threads',children='children',retries='retries')))
    resource_rows=[reserve['actual_original_resource_check'],h['resources_before'],stage['resource_before'],stage['resource_after'],h['resources_after']]
    ck('all genuine savedresource checks exact dynamic wholehistory96 free8 scope',all(row['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and row['artifact_budget_bytes']==CAPS['history_bytes'] and row['min_free_bytes']==CAPS['free_floor_bytes'] and set(row['resource_roots'])==set(row['declared_resource_roots'])==set(d['resource_roots']) and row['artifact_bytes']<CAPS['history_bytes'] and row['disk_free_bytes']>=CAPS['free_floor_bytes'] for row in resource_rows) and reserve['actual_original_resource_check']['artifact_bytes']+CAPS['joint_archive_bytes']<CAPS['history_bytes'] and reserve['actual_original_resource_check']['disk_free_bytes']-CAPS['joint_archive_bytes']>=CAPS['free_floor_bytes'])
    ck('genuine original MRO helper resource Source savedconstructor scope unchanged',h['supervisor_class_or_MRO_modified'] is False and h['profile_used'] is False and reserve['genuine_supervisor_MRO_unchanged'] is True and d['actual_supervisor_constructor_preflight']['actual_original_constructor_exercised'] is True and d['actual_supervisor_constructor_preflight']['native_or_numeric_child_launched'] is False and d['actual_supervisor_constructor_preflight']['class_name']=='OwnRSSSerialExecutor' and d['actual_supervisor_constructor_preflight']['genuine_parent_class_name']=='SerialExecutor')
    for k in('genuine_supervisor_source','genuine_parent_class_source','actual_local_supervisor_helper','actual_resource_class_factory','original_factory_ancestry_descriptor'):ref(d[k])
    ck('formal truePREP actual Rootterminal values launchargs floatbits exact',formal['schema']==cp['schema']=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25_ACTUAL_EXTERNAL_PREP_RETURN_V1' and formal['returncode']==0 and exact(formal['actual_tool_result'],rt) and exact(formal['actual_root_host_launchargs'],rt_doc['actual_launch_arguments']) and all(formal[k] is True for k in('successful_declaration_input_observed','actual_tool_terminal_return_observed','record_written_after_actual_terminal_return')))
    for p1,p2 in [(H/'run/prepare.log',T/'actual_child_merged_stdout_stderr.json'),(E/'parent_stderr.log',T/'actual_external_host_stderr.txt'),(E/'parent_stdout.log',T/'actual_external_host_stdout.json'),(E/'Root_actual_prepare_tool_terminal_return.json',T/'actual_external_Root_tool_terminal.json')]:
        a1=full(p1);b1=full(p2)
        if(a1['sha256'],a1['size_bytes'])!=(b1['sha256'],b1['size_bytes']):raise ValueError('complete streams exact copied bytes')
    ck('honest merged childstream separate real external stderr completecopy scope',formal['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False and full(E/'parent_stderr.log')['size_bytes']==0 and strict((H/'run/prepare.log').read_bytes())==dict(declaration=str(O/'declaration.json'),declaration_sha256=full(O/'declaration.json')['sha256']))
    inventory=meta(T/'Root_actual_SOURCE_inventory.json');sf=ns['namespaces'][1]['files']
    ck('all11 generated Source files RootfullEOF observation matches declaration and originalSourceinventory',summary['all_source_files_verified_count']==len(sf)==11 and inventory==d['source_inventory'] and inventory['files']=={k:q['sha256'] for k,q in sf.items()} and inventory['directories']==sorted(q['path'] for q in ns['namespaces'][1]['directories']) and formal['observed_at_unix']>=stage['started_unix']+w['elapsed_seconds'])
    graph=ref(summary['actual_input_graph'],False);trace=ref(summary['actual_complete_creation_trace'],False)
    ck('complete actualgraph trace RootEOF pins coupled savedO namespace without payload read',graph==ref(ns['namespaces'][2]['files']['input_graph.json'],False) and trace==ref(ns['namespaces'][2]['files']['input_creation_python_open_trace.json'],False) and summary['actual_complete_input_graph']==summary['actual_input_graph'])
    ck('existing trim META API actualRoot scope original arithmetic unchanged',sa['trim_component_API_executed_in_this_PREP'] is True and d['trim_component_API_executed_in_this_PREP'] is True and formal['trim_component_API_executed_in_this_PREP'] is True and sa['inherited_mathematical_controls_not_newly_executed'] is True and sa['retained_cache_math_unchanged'] is True and sa['no_Fortran_or_observer_source_written'] is True)
    false_rows=[(summary,('new_five_stage_build_executed','original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete')),(h,('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')),(d,('original_component_APIs_executed_now','historical_failed_combined_RUN_promoted','mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')),(sa,('original_component_APIs_executed_now','historical_failed_combined_RUN_grants_success','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')),(formal,cp['false_fields'])]
    ck('all5 future BUILD stages and all science credit false no old success transferred',d['stages']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'] and all(row[k] is False for row,keys in false_rows for k in keys) and not os.path.lexists(O/'seal.json') and not os.path.lexists(T/'terminal_return.json'))
    q=meta(Q);qp=meta(given['actual_Q_saved_peer_pin']['path']);qr=meta(given['actual_Q_saved_peer_retention_pin']['path']);qt=meta(given['actual_Q_writer_terminal_pin']['path']);terminal(qt,'94520a')
    ck('real c6Q3b helper saved48 retention10 original protocol Source only',given['actual_Q_pin']['sha256']==QSHA and full(HELPER)['sha256']==HSHA and peer(qp,'INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1','PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY') and qp['check_count']==48 and qp['Root_actual_Q_pin']==given['actual_Q_pin'] and qp['Root_actual_Q_writer_terminal_pin']==given['actual_Q_writer_terminal_pin'] and qr['complete_original_member_count']==len(qr['complete_original_members'])==10 and q['independent_saved_review_counts']==dict(pure=55,fresh=42,auxiliary_pure_small_controls=136))
    qfalse=('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired','supervisor_class_or_MRO_modified','profile_used')
    ck('Q helper only original340 owners controls48 Source provenance no whole native science transfer',all(q[k] is False for k in qfalse) and len(q['full_protocol'])==13 and [len(q['private_owner_consume_controls'][k]) for k in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections')]==[4,3,2,2] and [len(q['private_inactive_audit_snapshot_controls'][k]) for k in ('positive_controls','private_guard_rejections','last_use_failure_controls')]==[5,13,3] and all(qp[k] is False for k in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')))
    text,t=source(C);assign={n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    business=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
    ck('installed canonical completeSource same Q all6 future businesspinsNone',full(C)['sha256']==CSHA and all(isinstance(assign[k],ast.Constant) and assign[k].value is None for k in business) and ast.literal_eval(assign['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==QSHA)
    case=meta(CASE);ck('complete original physics case bytes temperature materials geometry groups and accuracy thresholds unchanged',given['actual_case_spec_pin']['sha256']=='ac3e67ffdc25f5bfa45bca5170253de8e875c983550e5ee878ee30c5d1a4c2c4' and case['cases']==dict(AAA=['A','A','A'],ABA=['A','B','A']) and case['geometry']['physical_z_edges_cm']==[0,50,100,150] and case['geometry']['radial_regions']==8 and case['production']['groups']==370 and case['materials']['temperature_C_in_every_zone']==dict(fuel_and_hole=750,clad_and_gap=620,sodium=475) and case['predeclared_decisions']['shape_targets']['normalized_nu_fission_max_relative_difference_in_fuel_bins']==.03 and case['predeclared_decisions']['shape_targets']['fission_normalized_scalar_flux_volume_weighted_relative_l2_max']==.01)
    current_joint=sum(i['size_bytes'] for i in ROOT_EOF_PINS.values() if any(Path(i['path']).is_relative_to(p) for p in(H,S,O,T,E)))+sum(q['size_bytes'] for q in dv['files'].values())+full(C)['size_bytes'];later=[ref(q) for q in cfg['later_E_files_after_writer_joint_sample']]
    historical=current_joint-sum(q['size_bytes'] for q in later)
    ck('complete Root2GiB joint namespace current and originalwriter sample explicitlaterE accounting',len({q['path'] for q in later})==len(later) and all(Path(q['path']).parent==E for q in later) and historical==summary['joint_archive_bytes'] and 0<historical<CAPS['joint_archive_bytes'] and current_joint<CAPS['joint_archive_bytes'])
    for p,q in list(PINS.items()):
        if not exact(full(p),q):raise ValueError('final Source/smallMETA fullEOF stability')
    for p,q in list(ROOT_EOF_PINS.items()):ref(q,False)
    ck('final all Source META EOF and all Rootobserved namespace7ID unchanged',all(tree(root,root==str(D))==v for root,v in views.items()))
    report=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1',status='PASS_ACTUAL_COMPLETE_PREP_ONLY',source_only=True,source_only_reviewer=True,stdlib_only=True,actual_PREP_closed_EXIT0_verified=True,actual_metadata_writer_closed_EXIT0_verified=True,actual_PREP_metadata_only=True,all_complete_scope_verified=True,all_checks_typed_true=True,checks=CHECKS,check_count=len(CHECKS),blockers=[],actual_Root_PREP_summary_pin=given['actual_PREP_summary_pin'],actual_Root_PREP_terminal_pin=given['actual_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=given['actual_complete_namespace_manifest_pin'],actual_metadata_writer_terminal_pin=given['actual_PREP_metadata_writer_terminal_pin'],actual_PREP_terminal_chunk=rt['chunk_id'],actual_metadata_writer_terminal_chunk=wt['chunk_id'],actual_review_input_contract_pin=inputpin,actual_source_freeze_pin=given['actual_prelaunch_Source_freeze_pin'],complete_actual_input_entries=306,complete_source_files=297,complete_source_subdirectories=34,complete_namespace_counts={root:dict(files=len(v['files']),directories=len(v['directories'])) for root,v in views.items()},full_EOF_Source_and_small_META_pins=PINS,Root_actual_full_EOF_business_payload_pins_verified_current7ID_only=ROOT_EOF_PINS,complete_definition_occurrence_counts=SOURCE_DEFINITION_COUNTS,large_business_payload_independently_read_to_EOF=False,graph_trace_gzip_native_material_or_DB_payload_read=False,actual_genuine_guard_caps=CAPS,metrics=dict(whole_seconds=h['whole_seconds'],child_seconds=w['elapsed_seconds'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],historical_joint_bytes=historical,current_joint_bytes=current_joint),actual_ROOT_existing_trim_metadata_API_executed=True,new_reviewer_business_or_API_execution=False,whole_combined_build_qualified=False,whole_combined_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,goal_complete=False)
    out.mkdir()
    with(out/'REVIEW.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    with(out/'REVIEWER_EXECUTED_SOURCE.py').open('xb') as f:f.write(Path(__file__).read_bytes())
    print(json.dumps(dict(schema=report['schema'],status=report['status'],source_only=True,review_pin=full(out/'REVIEW.json'),check_count=len(CHECKS),blockers=[],actual_Root_PREP_summary_pin=given['actual_PREP_summary_pin'],actual_Root_PREP_terminal_pin=given['actual_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=given['actual_complete_namespace_manifest_pin'],new_business_or_science_execution=False)),flush=True)
if __name__=='__main__':main()

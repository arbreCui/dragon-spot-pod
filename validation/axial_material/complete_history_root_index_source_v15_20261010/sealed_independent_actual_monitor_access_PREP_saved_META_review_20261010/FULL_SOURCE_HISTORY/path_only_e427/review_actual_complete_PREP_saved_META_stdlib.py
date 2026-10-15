"""Independent complete V25 saved PREP evidence reviewer.

This is stdlib Source/META inspection. No inspected Source is imported,
compiled or executed; graph, creation trace, gzip and native/material payloads
are streamed only for complete EOF SHA/size/7ID. Root supplies actual full pins
after its real PREP and pre-frozen metadata writer have closed. No future value
is inferred from this design. The six BUILD/science credit fields stay False.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct
import sys

R = Path('/Users/wen/spot')
B = R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = R/'validation/artifacts'
D = B/'actual_complete_combined_prepare_v25_monitor_access_sources'
E = B/'actual_complete_combined_prepare_v25_monitor_access_receipts'
H = ART/'axial-material-complete-combined-prepare-host-v25-monitor-access-20261010'
S = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010'
O = ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010'
T = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010'
C = R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py'
HELPER = R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
Q = B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
CASE = R/'validation/axial_material/case_spec.json'
CASE_SHA = 'ac3e67ffdc25f5bfa45bca5170253de8e875c983550e5ee878ee30c5d1a4c2c4'
Q_SHA = 'c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
STAGES = ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0)
BUSINESS = ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
CREDIT = ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')
INPUT_KEYS = ('actual_PREP_summary_pin','actual_PREP_terminal_pin','actual_PREP_metadata_writer_terminal_pin','actual_complete_namespace_manifest_pin','actual_prelaunch_Source_freeze_pin','actual_final_prelaunch_reserve_pin','actual_E_prelaunch_snapshot_pin','actual_E_postclose_snapshot_pin','actual_installed_canonical_pin','actual_Q_pin','actual_Q_writer_terminal_pin','actual_Q_saved_peer_pin','actual_Q_saved_peer_retention_pin','actual_bound_Source_peer_report_pin','actual_bound_Source_peer_manifest_pin','actual_bound_Source_peer_seal_pin','actual_root_source_install_record_pin','actual_case_spec_pin')
PINS = {}
CHECKS = []
JSON_READS = []
SOURCE_READS = []


def need(value,label):
    if type(value) is not bool or value is not True:
        raise ValueError(label)
    CHECKS.append(dict(check=label,passed=True))


def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def full(path):
    p=Path(path)
    need(p.is_absolute() and '..' not in p.parts,'absolute canonical pin path '+str(p))
    before=identity(p)
    need(stat.S_ISREG(before[2]) and before[3]==1,'single-link regular file '+str(p))
    with p.open('rb') as f:
        sha=hashlib.file_digest(f,'sha256').hexdigest()
    need(identity(p)==before,'complete EOF file unchanged '+str(p))
    q=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
    if str(p) in PINS:
        need(exact(PINS[str(p)],q),'repeated full pin unchanged '+str(p))
    else:
        PINS[str(p)]=q
    return q


def exact(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return list(a)==list(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):
        return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    if type(a) is float:
        return struct.pack('>d',a)==struct.pack('>d',b)
    return a==b


def pin4(ref,label='fullpin'):
    need(type(ref) is dict and type(ref.get('path')) is str and type(ref.get('sha256')) is str,label+' typed path/SHA')
    need(len(ref['sha256'])==64 and ref['sha256']!='0'*64 and all(c in '0123456789abcdef' for c in ref['sha256']),label+' lowercase nonzero SHA')
    if 'identity' in ref:
        i=ref['identity']
        need(type(i) is list and len(i)==7 and all(type(v) is int for v in i),label+' seven exact Python integers')
        need(stat.S_ISREG(i[2]) and i[3]==1 and i[4]>=0,label+' regular seven-field identity')
    else:
        i=None
    v=full(ref['path'])
    need(v['sha256']==ref['sha256'],label+' actual full EOF SHA '+ref['path'])
    if i is not None: need(exact(v['identity'],i),label+' actual 7ID '+ref['path'])
    if 'size_bytes' in ref:
        need(type(ref['size_bytes']) is int and ref['size_bytes']==v['size_bytes'],label+' actual complete byte size '+ref['path'])
    return v


def supplied(ref,label):
    need(type(ref) is dict and set(ref)=={'path','sha256','size_bytes','identity'},label+' Root supplied exact four-field fullpin')
    return pin4(ref,label)


def pairs(items):
    out={}
    for k,v in items:
        if k in out: raise ValueError('duplicate JSON key '+k)
        out[k]=v
    return out


def strict_bytes(raw):
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite JSON '+v)))


def meta(path):
    p=Path(path)
    need(p.name not in ('input_graph.json','input_creation_python_open_trace.json') and p.suffix not in ('.gz','.xsm','.sqlite','.db','.h5','.hdf5','.so','.a','.o'),'META read excludes graph/trace/native/material payload '+str(p))
    before=full(p)
    v=strict_bytes(p.read_bytes())
    need(exact(full(p),before),'strict META read full EOF unchanged '+str(p))
    JSON_READS.append(str(p))
    return v


def source(path):
    p=Path(path); before=full(p); raw=p.read_bytes()
    need(exact(full(p),before),'complete Source read unchanged '+str(p))
    text=raw.decode('utf-8'); tree=ast.parse(text,filename=str(p))
    SOURCE_READS.append(str(p))
    return text,tree


def references(value,label):
    if type(value) is dict:
        if type(value.get('path')) is str and type(value.get('sha256')) is str:
            pin4(value,label)
        for v in value.values(): references(v,label)
    elif type(value) is list:
        for v in value: references(v,label)


def terminal(doc,label,wanted=None):
    need(type(doc) is dict and doc.get('closed') is True,label+' actual closed wrapper')
    keys=[k for k in ('terminal_tool_return','actual_tool_return','exec_command_result') if k in doc]
    need(len(keys)==1,label+' one actual terminal field')
    tr=doc[keys[0]]
    need(type(tr) is dict and type(tr.get('exit_code')) is int and tr['exit_code']==0 and 'session_id' not in tr,label+' typed integer EXIT0 and no session')
    need(type(tr.get('chunk_id')) is str and bool(tr['chunk_id']),label+' genuine terminal chunk present')
    if wanted is not None: need(tr['chunk_id']==wanted,label+' exact Root supplied terminal chunk')
    need(type(tr.get('wall_time_seconds')) in (int,float) and math.isfinite(tr['wall_time_seconds']) and tr['wall_time_seconds']>=0,label+' finite actual tool elapsed')
    for key in ('session_repolled_after_close','closed_session_repolled'):
        if key in doc: need(doc[key] is False,label+' no closed session repoll')
    return tr


def walk(root):
    root=Path(root);need(root.is_dir() and not root.is_symlink(),'regular complete namespace root '+str(root))
    root_id=identity(root); files={};dirs={};syms={}
    for folder,subdirs,names in os.walk(root,followlinks=False):
        for name in subdirs+names:
            p=Path(folder)/name; rel=str(p.relative_to(root)); i=identity(p)
            if stat.S_ISLNK(i[2]): syms[rel]=dict(identity=i,literal_target=os.readlink(p))
            elif stat.S_ISDIR(i[2]): dirs[rel]=i
            elif stat.S_ISREG(i[2]): files[rel]=full(p)
            else: raise ValueError('nonregular namespace member '+str(p))
    need(identity(root)==root_id,'namespace root stable during full walk '+str(root))
    return dict(root=str(root),root_identity=root_id,files=files,directories=dirs,symlinks=syms)


def normalize_namespace(doc):
    if 'namespace' in doc: return doc['namespace']
    if 'namespaces' in doc:
        need(type(doc['namespaces']) is list and len(doc['namespaces'])==1,'one complete E namespace in separate Root snapshot')
        return doc['namespaces'][0]
    return doc


def verify_namespace(doc,root,allow_directory_root_change=False):
    need(type(doc) is dict and doc['root']==str(root),'exact declared namespace root '+str(root))
    actual=walk(root)
    need(type(doc['files']) is dict and set(actual['files'])==set(doc['files']),'complete namespace file domain '+str(root))
    for rel,ref in doc['files'].items():
        need(ref['path']==str(root/rel),'exact logical namespace path '+str(root/rel))
        need(exact(pin4(ref,'saved namespace'),actual['files'][rel]),'complete namespace full pin '+str(root/rel))
    rawdirs=doc['directories']
    expected={v['path']:v['identity'] for v in rawdirs} if type(rawdirs) is list else rawdirs
    need(type(expected) is dict and all(type(v) is list and len(v)==7 and all(type(x) is int for x in v) for v in expected.values()) and actual['directories']==expected,'complete namespace directory identities '+str(root))
    need(exact(actual['symlinks'],doc['symlinks']),'complete literal namespace symlinks '+str(root))
    if 'root_identity' in doc and not allow_directory_root_change:
        need(exact(actual['root_identity'],doc['root_identity']),'complete namespace root 7ID '+str(root))
    return actual


def cap_values(doc,mapping,label):
    for k,capkey in mapping.items():
        need(type(doc[k]) is int and doc[k]==CAPS[capkey],label+' original cap '+k)


def resource(row,declaration_roots,label):
    need(row['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1',label+' original whole history scope')
    need(type(row['artifact_budget_bytes']) is int and row['artifact_budget_bytes']==CAPS['history_bytes'] and type(row['min_free_bytes']) is int and row['min_free_bytes']==CAPS['free_floor_bytes'],label+' original history96/free8')
    roots=row['resource_roots']; declared=row['declared_resource_roots']
    need(type(roots) is list and len(roots)==len(set(roots)) and set(roots)==set(declared)==set(declaration_roots),label+' complete genuine dynamic root domain')
    need(all(type(p) is str and Path(p).is_relative_to(ART) and Path(p)!=ART for p in roots),label+' all history roots strict ART descendants')
    for k in ('artifact_bytes','disk_free_bytes','regular_files','checked_unix'):
        need(type(row[k]) in (int,float) and math.isfinite(row[k]),label+' finite saved '+k)
    need(row['artifact_bytes']<CAPS['history_bytes'] and row['disk_free_bytes']>=CAPS['free_floor_bytes'],label+' actual saved resource under original caps')


def passed_peer(doc,schema,label):
    need(doc['schema']==schema and doc['source_only'] is True and doc['all_checks_typed_true'] is True and type(doc['blockers']) is list and doc['blockers']==[],label+' exact Source META peer scope')
    need(type(doc['checks']) is list and type(doc['check_count']) is int and doc['check_count']==len(doc['checks']) and doc['check_count']>0,label+' exact check count')
    need(all(type(row) is dict and type(row.get('passed')) is bool and row['passed'] is True for row in doc['checks']),label+' every check typed True')


def review(args):
    need(not os.path.lexists(args.output) and args.output.is_relative_to(Path('/private/tmp')),'genuinely fresh independent saved review output')
    supplied(args.config_pin,'review input contract')
    inputs=meta(args.config_pin['path'])
    need(inputs['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_SAVED_REVIEW_INPUTS_V1' and inputs['status']=='ACTUAL_ROOT_COMPLETE_PREP_AND_METADATA_WRITER_CLOSED0','actual inputs replace future None only after real Root execution')
    need(type(inputs['actual_terminal_chunks']) is dict and set(inputs['actual_terminal_chunks'])=={'PREP','metadata_writer'} and all(type(v) is str and bool(v) for v in inputs['actual_terminal_chunks'].values()),'Root actually observed PREP and metadatawriter chunks')
    given={k:supplied(inputs[k],'Root actual '+k) for k in INPUT_KEYS}
    fixed={'actual_PREP_summary_pin':E/'Root_actual_complete_combined_prepare_summary.json','actual_PREP_terminal_pin':E/'Root_actual_prepare_tool_terminal_return.json','actual_PREP_metadata_writer_terminal_pin':E/'Root_actual_prepare_metadata_writer_tool_return.json','actual_complete_namespace_manifest_pin':E/'Root_actual_complete_prepare_namespace_manifest.json','actual_prelaunch_Source_freeze_pin':E/'Root_prelaunch_complete_source_freeze.json','actual_final_prelaunch_reserve_pin':E/'Root_final_prelaunch_source_and_reserve_check.json','actual_installed_canonical_pin':C,'actual_Q_pin':Q,'actual_root_source_install_record_pin':D/'Root_actual_complete_SOURCE_install_record.json','actual_case_spec_pin':CASE}
    for k,path in fixed.items(): need(given[k]['path']==str(path),'fixed actual proof path '+k)
    need(given['actual_Q_pin']['sha256']==Q_SHA,'actual new Q c6 exact full EOF')
    need(given['actual_case_spec_pin']['sha256']==CASE_SHA,'whole original physical case specification byte-exact, not selected fields')
    trdoc=meta(given['actual_PREP_terminal_pin']['path']);rt=terminal(trdoc,'Root actual complete PREP',inputs['actual_terminal_chunks']['PREP'])
    need(trdoc['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' and trdoc['observed_terminal'] is True and trdoc['session_repolled_after_close'] is False,'true complete PREP receipt and no repoll')
    wrdoc=meta(given['actual_PREP_metadata_writer_terminal_pin']['path']);wt=terminal(wrdoc,'Root actual frozen metadata writer',inputs['actual_terminal_chunks']['metadata_writer'])
    need(wrdoc['metadata_only'] is True,'metadatawriter has no new native or science execution')
    summary=meta(given['actual_PREP_summary_pin']['path'])
    need(summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD','true V25 PREP only summary')
    ns=meta(given['actual_complete_namespace_manifest_pin']['path'])
    need(ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and ns['no_build_or_native_credit'] is True,'original writer H/S/O/T/D scope only')
    need([row['root'] for row in ns['namespaces']]==[str(p) for p in (H,S,O,T,D)],'all original full H/S/O/T/D in writer order')
    observed={str(p):verify_namespace(row,p) for p,row in zip((H,S,O,T,D),ns['namespaces'])}
    epost=normalize_namespace(meta(given['actual_E_postclose_snapshot_pin']['path']))
    observed[str(E)]=verify_namespace(epost,E)
    epre=normalize_namespace(meta(given['actual_E_prelaunch_snapshot_pin']['path']))
    need(epre['root']==str(E) and type(epre['files']) is dict and type(epre['symlinks']) is dict and epre['symlinks']=={},'actual separate full prelaunch E snapshot')
    need(set(epre['files']).issubset(observed[str(E)]['files']),'all E prelaunch files remain')
    for rel,ref in epre['files'].items():
        need(ref['path']==str(E/rel),'complete prelaunch E logical path '+rel)
        need(exact(pin4(ref,'prelaunch E file'),observed[str(E)]['files'][rel]),'all original E full EOF SHA7ID unchanged '+rel)
    freeze=meta(given['actual_prelaunch_Source_freeze_pin']['path']);reserve=meta(given['actual_final_prelaunch_reserve_pin']['path'])
    need(freeze['schema']=='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1' and freeze['source_root']==str(D),'complete frozen D schema/root')
    need(exact(freeze['source_root_identity'],observed[str(D)]['root_identity']),'frozen D root unchanged 7ID')
    need(set(freeze['complete_files'])==set(observed[str(D)]['files']) and freeze['complete_directories']==observed[str(D)]['directories'] and freeze['symlinks']==observed[str(D)]['symlinks']=={},'complete frozen D file/dir/symlink domain unchanged')
    for rel,ref in freeze['complete_files'].items():
        need(exact(supplied(ref,'frozen D file'),observed[str(D)]['files'][rel]),'all prelaunch D full pins unchanged '+rel)
    need(type(freeze['file_count']) is int and freeze['file_count']==len(freeze['complete_files']) and type(freeze['directory_count']) is int and freeze['directory_count']==len(freeze['complete_directories']),'complete D counts derived from actual domains')
    need(freeze['no_SOURCE_append_after_freeze'] is True and freeze['all_file_SHA7ID_recorded'] is True and freeze['actual_PREP_not_started'] is True,'D genuinely frozen before PREP')
    need(exact(pin4(freeze['canonical_factory'],'frozen canonical'),given['actual_installed_canonical_pin']) and exact(pin4(ns['canonical_factory'],'namespace canonical'),given['actual_installed_canonical_pin']),'same installed and frozen canonical full pin')
    need(reserve['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_FINAL_PRELAUNCH_SOURCE_AND_GENUINE_RESERVE_CHECK_V1' and reserve['all_SOURCE_full_EOF_SHA7ID_unchanged'] is True and reserve['genuine_supervisor_MRO_unchanged'] is True,'true complete reserve check scope')
    need(reserve['complete_SOURCE_file_count']==freeze['file_count'] and reserve['complete_SOURCE_directory_count']==freeze['directory_count'],'actual reserve complete frozen D counts')
    need(exact(pin4(reserve['full_SOURCE_freeze'],'reserve freeze'),given['actual_prelaunch_Source_freeze_pin']) and exact(pin4(reserve['canonical'],'reserve canonical'),given['actual_installed_canonical_pin']),'reserve correct fullfreeze and canonical coupling')
    need(reserve['metadata_writer_already_frozen'] is True and reserve['all_new_H_S_O_T_absent'] is True and reserve['PREP_or_build_launched'] is False and reserve['native_or_science_qualified'] is False,'prelaunch freezes real writer with all outputs absent')
    h=meta(H/'result.json');w=meta(H/'run/prepare.watchdog.json');stages=meta(H/'COMBINED_PREPARATION/stages.json')['stages']
    d=meta(O/'declaration.json');sa=meta(S/'source_admission.json');formal=meta(T/'declaration_terminal_return.json');cp=d['actual_external_prepare_terminal_contract']
    need(h['schema']=='AXMAT_V25_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1' and h['status']=='ACTUAL_COMPLETE_COMBINED_PREPARE_EXTERNAL_ROOT_REQUIRED','genuine original PREP host correct external terminal scope')
    all_inputs=h['input_sources']+[h['original_helper'],h['resource_factory']]
    need(exact(all_inputs,ns['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']),'all ordered actual input Sources exactly retained')
    need(type(h['input_sources']) is list and len(h['input_sources'])==7+freeze['file_count'],'all seven fixed original inputs plus complete frozen D')
    need({row['path'] for row in h['input_sources'][7:]}=={row['path'] for row in freeze['complete_files'].values()},'complete input set contains every D file')
    for row in all_inputs: pin4(row,'complete actual fixed input')
    need(h['input_sources'][1]['path']==str(C) and h['input_sources'][5]['path']==str(HELPER) and h['input_sources'][5]['sha256']==HELPER_SHA and h['input_sources'][6]['path']==str(Q) and h['input_sources'][6]['sha256']==Q_SHA,'actual unchanged helper3b and real Q c6 inputs')
    command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(C),'prepare-build']
    need(exact(h['actual_canonical_command'],command) and exact(w['command'],command) and exact(cp['command'],command) and exact(formal['command'],command),'one actual normal canonical PREP command')
    expected_cmd='env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'combined_prepare_host.py')+' > '+str(E/'parent_stdout.log')+' 2> '+str(E/'parent_stderr.log')
    need(trdoc['actual_launch_arguments']['cmd']==expected_cmd,'actual Root one-thread unprofiled -B host launch')
    need(type(stages) is list and len(stages)==1 and exact(stages,h['stage_records']),'one complete saved PREP stage')
    stage=stages[0]
    need(stage['label']=='run/prepare' and stage['status']=='PASS' and exact(stage['command'],command) and stage['wall_cap_seconds']==600.0,'actual full one child stage PASS')
    need(type(w['pid']) is int and w['pid']>0 and type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True,'genuine actual PID/EXIT0/cap/no-retry cleanup')
    need(exact(h['watchdog'],w),'full saved host/watchdog values types order and float bits exact')
    for key in ('elapsed_seconds','sampled_peak_rss_mib','wall_cap_seconds','rss_cap_mib'):
        need(type(w[key]) in (int,float) and math.isfinite(w[key]),'finite actual watchdog '+key)
    need(type(h['whole_seconds']) in (int,float) and math.isfinite(h['whole_seconds']) and 0<w['elapsed_seconds']<=w['wall_cap_seconds']<=600 and w['elapsed_seconds']<=h['whole_seconds']<1800 and 0<=w['sampled_peak_rss_mib']<512 and w['rss_cap_mib']==512,'actual PREP original runtime caps')
    cap_values(h,dict(whole_wall_cap_seconds='whole_seconds',stage_wall_cap_seconds='stage_seconds',rss_cap_mib='rss_mib',archive_cap_bytes='joint_archive_bytes',threads='threads',children_at_once='children',retries='retries'),'host')
    cap_values(d,dict(total_wall_seconds='whole_seconds',stage_wall_seconds='stage_seconds',rss_cap_mib='rss_mib',archive_reserve_bytes='joint_archive_bytes',artifact_budget_bytes='history_bytes',min_free_bytes='free_floor_bytes',threads='threads',numeric_children_at_once='children',retries='retries'),'declaration')
    cap_values(summary,dict(whole_wall_cap_seconds='whole_seconds',stage_wall_cap_seconds='stage_seconds',rss_mib='rss_mib',joint_archive_cap_bytes='joint_archive_bytes',history_cap_bytes='history_bytes',free_floor_bytes='free_floor_bytes',threads='threads',children='children',retries='retries'),'summary')
    cap_values(freeze,dict(original_whole_seconds='whole_seconds',original_stage_seconds='stage_seconds',original_RSS_mib='rss_mib',original_joint_archive_bytes='joint_archive_bytes',original_history_bytes='history_bytes',original_free_floor_bytes='free_floor_bytes',original_threads='threads',original_children='children',original_retries='retries'),'freeze')
    need(exact(summary['whole_seconds'],h['whole_seconds']) and exact(summary['child_seconds'],w['elapsed_seconds']) and exact(summary['sampled_peak_rss_mib'],w['sampled_peak_rss_mib']),'summary actual runtime float bits')
    for label,row in [('reserve',reserve['actual_original_resource_check']),('host before',h['resources_before']),('stage before',stage['resource_before']),('stage after',stage['resource_after']),('host after',h['resources_after'])]: resource(row,d['resource_roots'],label)
    need(reserve['actual_original_resource_check']['artifact_bytes']+CAPS['joint_archive_bytes']<CAPS['history_bytes'] and reserve['actual_original_resource_check']['disk_free_bytes']-CAPS['joint_archive_bytes']>=CAPS['free_floor_bytes'],'actual full original reserve checked before launch')
    need(h['supervisor_class_or_MRO_modified'] is False and h['profile_used'] is False and reserve['genuine_supervisor_MRO_unchanged'] is True,'unchanged original MRO and no profiling')
    for key in ('genuine_supervisor_source','genuine_parent_class_source','actual_local_supervisor_helper','actual_resource_class_factory','original_factory_ancestry_descriptor'): pin4(d[key],'genuine supervisor Source')
    preflight=d['actual_supervisor_constructor_preflight']
    need(preflight['actual_original_constructor_exercised'] is True and preflight['native_or_numeric_child_launched'] is False and preflight['class_name']=='OwnRSSSerialExecutor' and preflight['genuine_parent_class_name']=='SerialExecutor','actual original constructor META scope')
    need(d['actual_resource_class_factory']['genuine_class_not_overlay'] is True and d['original_factory_ancestry_descriptor']['genuine_class_not_overlay'] is True,'genuine resource class no overlay')
    need(exact(d['stages'],STAGES),'all five future BUILD stages preserved, none credited')
    need(not os.path.lexists(O/'seal.json') and not os.path.lexists(T/'terminal_return.json'),'no BUILD terminal or seal fabricated by PREP')
    need(cp['schema']==formal['schema']=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25_ACTUAL_EXTERNAL_PREP_RETURN_V1' and cp['root']==str(T) and cp['receipt']==str(T/'declaration_terminal_return.json'),'formal true PREP schema/root/receipt')
    need(type(formal['returncode']) is int and formal['returncode']==0 and exact(formal['actual_tool_result'],rt) and exact(formal['actual_root_host_launchargs'],trdoc['actual_launch_arguments']),'formal actual Root tool type/order/float bits')
    for key in ('successful_declaration_input_observed','actual_tool_terminal_return_observed','record_written_after_actual_terminal_return'): need(formal[key] is True,'formal genuine observed '+key)
    need(type(formal['observed_at_unix']) in (int,float) and math.isfinite(formal['observed_at_unix']) and formal['observed_at_unix']>=stage['started_unix']+w['elapsed_seconds'],'formal receipt recorded after child completion')
    for key in ('source','declaration','source_inventory','full_stdout','full_stderr','actual_child_watchdog','actual_root_host_terminal_tool_return','actual_root_host_stdout','original_executor_merged_capture_source'): pin4(formal[key],'formal complete stream/Source pin')
    need(formal['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False,'honest merged child stream versus independent outer stderr')
    for src,dst in [(H/'run/prepare.log',T/'actual_child_merged_stdout_stderr.json'),(E/'parent_stderr.log',T/'actual_external_host_stderr.txt'),(E/'parent_stdout.log',T/'actual_external_host_stdout.json'),(E/'Root_actual_prepare_tool_terminal_return.json',T/'actual_external_Root_tool_terminal.json')]:
        need(full(src)['sha256']==full(dst)['sha256'] and full(src)['size_bytes']==full(dst)['size_bytes'],'complete byte-exact stream copy '+str(dst))
    need(full(E/'parent_stderr.log')['size_bytes']==0,'real outer host stderr empty only')
    log=meta(H/'run/prepare.log')
    need(exact(log,dict(declaration=str(O/'declaration.json'),declaration_sha256=full(O/'declaration.json')['sha256'])) and stage['log_sha256']==full(H/'run/prepare.log')['sha256'],'entire canonical merged stream exact')
    hout=meta(E/'parent_stdout.log')
    need(hout['status']==h['status'] and hout['actual_external_Root_terminal_required'] is True,'entire real host stdout correct scope')
    for key in ('actual_host_result','actual_prepare_stdout'): pin4(hout[key],'whole host stdout pointer')
    for key in ('actual_declaration','actual_prepare_stdout','actual_source_admission','actual_watchdog'): pin4(h[key],'actual host saved output')
    for key in ('actual_root_terminal','actual_host_result','formal_PREP_terminal','actual_declaration','actual_input_graph','actual_complete_creation_trace','namespace_manifest'): pin4(summary[key],'actual summary complete pin')
    need(exact(summary['Root_actual_terminal'],summary['actual_root_terminal']) and exact(summary['actual_complete_input_graph'],summary['actual_input_graph']),'actual summary alias values types order exact')
    for key in ('input_graph','historical_whole_component_body','historical_PREP','actual_last_cprime_trim_component_INPUT'):
        need(exact(formal[key],d[key]),'formal original complete typed metadata '+key)
    sf=observed[str(S)]['files'];sd=observed[str(S)]['directories']
    inv=dict(files={rel:row['sha256'] for rel,row in sf.items()},directories=sorted(sd),symlinks={})
    need(inv==d['source_inventory']==meta(T/'Root_actual_SOURCE_inventory.json'),'all SOURCE file/dir inventory complete')
    need(type(summary['all_source_files_verified_count']) is int and summary['all_source_files_verified_count']==len(sf) and type(summary['all_original_pinned_inputs_unchanged_count']) is int and summary['all_original_pinned_inputs_unchanged_count']==len(all_inputs),'actual derived Source and complete input counts')
    need(sa['trim_component_API_executed_in_this_PREP'] is True and d['trim_component_API_executed_in_this_PREP'] is True and formal['trim_component_API_executed_in_this_PREP'] is True,'Root actual existing trim metadata API honestly retained')
    need(sa['inherited_mathematical_controls_not_newly_executed'] is True and sa['retained_cache_math_unchanged'] is True and sa['no_Fortran_or_observer_source_written'] is True,'inherited arithmetic and physics Source unchanged')
    for container,keys,label in [(summary,('new_five_stage_build_executed','original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'),'summary'),(h,('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'),'host'),(d,('original_component_APIs_executed_now','historical_failed_combined_RUN_promoted','mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'),'declaration'),(sa,('original_component_APIs_executed_now','historical_failed_combined_RUN_grants_success','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'),'Source admission'),(formal,cp['false_fields'],'formal')]:
        for key in keys: need(container[key] is False,label+' no transferred science/build credit '+key)
    need(summary['original_caps_preserved'] is True and d['original_operator_capture_RSS_scope_not_transferred'] is True,'original caps and no transferred native RSS')
    text,tree=source(C);assign={t.id:node.value for node in tree.body if isinstance(node,ast.Assign) for t in node.targets if isinstance(t,ast.Name)}
    need(ast.literal_eval(assign['DRAFT_STATUS'])=='READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','actual canonical READY Source status')
    need(ast.literal_eval(assign['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==Q_SHA,'same actual Q in installed Source')
    for name in BUSINESS: need(isinstance(assign[name],ast.Constant) and assign[name].value is None,'all original future business pins still None '+name)
    for name,key in [('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','actual_Q_writer_terminal_pin'),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','actual_Q_saved_peer_pin'),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN','actual_Q_saved_peer_retention_pin')]:
        need(exact(pin4(ast.literal_eval(assign[name]),'installed external Q proof'),given[key]),'same exact installed actual external Q proof '+name)
    calls=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='snapshot' and any(k.arg=='_consume' for k in node.keywords)]
    need(len(calls)==3 and all(next(k.value for k in node.keywords if k.arg=='_consume').value is True for node in calls),'all three reviewed private inactive audit snapshots consume at last use')
    q=meta(Q);need(q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25' and q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25','actual new helper Q exact schema/status')
    need(exact(pin4(q['helper'],'actual helper Q Source'),full(HELPER)) and full(HELPER)['sha256']==HELPER_SHA,'same true3b helper Source')
    need(q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE','Q remains helper META only')
    need(q['independent_saved_review_counts']==dict(pure=55,fresh=42,auxiliary_pure_small_controls=136),'all actual55/42 saved control peers retained')
    for key in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired','supervisor_class_or_MRO_modified','profile_used'):
        need(q[key] is False,'actual helper Q grants no whole/native/science '+key)
    for label,family,chunk,count in [('pure',q,'ca2666',55),('fresh',q['complete_current_graph_fresh_verifier'],'d1d77b',42)]:
        savedterm=meta(family['actual_root_terminal']['path']);terminal(savedterm,'actual saved '+label+' helper Root terminal',chunk)
        need(savedterm['actual_tool_terminal_return_observed'] is True and savedterm['new_actual_helper_qualification'] is None,'saved '+label+' qualification scope exact')
        p=meta(family['independent_actual_review']['path'])
        need(p['source_only'] is True and p['all_checks_typed_true'] is True and type(p['blockers']) is list and p['blockers']==[] and type(p['check_count']) is int and p['check_count']==len(p['checks'])==count and all(type(row['passed']) is bool and row['passed'] is True for row in p['checks']),'saved complete '+label+' review all'+str(count)+' exact typed checks')
    owners=q['private_owner_consume_controls'];snap=q['private_inactive_audit_snapshot_controls']
    need([len(owners[key]) for key in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections')]==[4,3,2,2],'all original full owner controls retained')
    need([len(snap[key]) for key in ('positive_controls','private_guard_rejections','last_use_failure_controls')]==[5,13,3],'all new full snapshot controls retained')
    need(len(q['full_protocol'])==13 and q['complete_current_graph_fresh_verifier']['complete_actual_read_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True),'whole original protocol/current complete canonical read count')
    qp=meta(given['actual_Q_saved_peer_pin']['path']);passed_peer(qp,'INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1','actual saved Q48')
    need(qp['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY' and qp['check_count']==48,'actual complete saved Q48')
    for key in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','candidate_helper_writer_guard_API_or_numeric_executed','large_graph_trace_gzip_SQLite_material_or_Source_archive_member_payload_read'):
        need(qp[key] is False,'actual saved Q48 helper-only scope '+key)
    need(exact(pin4(qp['Root_actual_Q_pin'],'saved Q peer Q'),given['actual_Q_pin']) and exact(pin4(qp['Root_actual_Q_writer_terminal_pin'],'saved Q peer writer'),given['actual_Q_writer_terminal_pin']),'new actual Q peer coupled full pins')
    qt=meta(given['actual_Q_writer_terminal_pin']['path']);terminal(qt,'actual Q writer','94520a')
    need(qt['actual_tool_terminal_return_observed'] is True and qt['no_closed_session_repoll'] is True,'real observed Q writer terminal retained')
    qr=meta(given['actual_Q_saved_peer_retention_pin']['path']);need(qr['source_only'] is True and qr['new_qualification_created'] is False and qr['helper_guard_business_executed'] is False and qr['complete_original_member_count']==len(qr['complete_original_members'])==10,'all original saved Q48 Source META package retained')
    for label,value in [('complete actual helper Q',q),('complete actual saved48',qp),('complete saved48 retention',qr)]: references(value,label)
    bp=meta(given['actual_bound_Source_peer_report_pin']['path']);passed_peer(bp,'INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1','actual bound canonical host writer Source peer')
    need(bp['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION','actual full bound Source qualified without business credit')
    bound_manifest_pin=pin4(bp['qualified_bound_manifest_pin'],'qualified actual bound Source member manifest')
    bound_manifest=meta(bound_manifest_pin['path']);references(bound_manifest,'all complete actual bound Source members')
    roles=bp['qualified_role_Source_pins']
    need(set(roles)=={'canonical','prepare_host','prepare_writer'},'all three actual bound executable Source roles')
    for key,target in [('canonical',C),('prepare_host',D/'combined_prepare_host.py'),('prepare_writer',D/'write_actual_prepare_terminal.py')]:
        row=pin4(roles[key],'peer reviewed complete role'); installed=full(target)
        need(row['sha256']==installed['sha256'] and row['size_bytes']==installed['size_bytes'],'peer reviewed byte-exact installed complete '+key)
        source(target)
    bm=meta(given['actual_bound_Source_peer_manifest_pin']['path']);references(bm,'whole bound independent Source peer member manifest')
    need(exact(pin4(bm['members']['REVIEW.json'],'sealed actual Source peer report'),given['actual_bound_Source_peer_report_pin']),'complete independent peer manifest contains exact reviewed report')
    need(type(bm['member_count']) is int and bm['member_count']==len(bm['members']),'complete independent Source peer manifest member count exact')
    peerroot=Path(given['actual_bound_Source_peer_manifest_pin']['path']).parent;peerview=walk(peerroot)
    need(set(peerview['files'])==set(bm['members'])|{'MANIFEST.json'},'complete original independent Source peer member domain no omission')
    for rel,ref in bm['members'].items(): need(ref['path']==str(peerroot/rel) and exact(pin4(ref,'complete original Source peer member'),peerview['files'][rel]),'every independent Source peer member full EOF SHA7ID '+rel)
    bs=meta(given['actual_bound_Source_peer_seal_pin']['path']);bst=terminal(bs,'actual bound Source peer seal')
    bsout=strict_bytes(bst['output'])
    need(exact(pin4(bsout['manifest_pin'],'actual Source peer sealed manifest'),given['actual_bound_Source_peer_manifest_pin']) and exact(pin4(bsout['review_pin'],'actual Source peer sealed report'),given['actual_bound_Source_peer_report_pin']) and exact(pin4(bsout['qualified_bound_manifest_pin'],'actual Source peer qualified bound manifest'),bound_manifest_pin),'actual genuine closed Source seal couples peer/report/bound complete manifests')
    install=meta(given['actual_root_source_install_record_pin']['path'])
    need(install['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1' and install['source_only'] is True and install['metadata_writer_and_prelaunch_included_before_freeze'] is True and install['new_PREP_or_build_executed'] is False and install['whole_build_INPUT_native_or_science_qualified'] is False,'true complete Source-only installation before freeze')
    need(exact(pin4(install['canonical_installed'],'actual installed canonical'),given['actual_installed_canonical_pin']),'true installed canonical fullpin')
    references(install,'complete unchanged Source installation proofs')
    case=meta(CASE)
    need(case['status']=='PREDECLARED_BEFORE_NEW_PHYSICAL_SOLVES' and case['cases']==dict(AAA=['A','A','A'],ABA=['A','B','A']),'original ordered AAA before ABA experiment')
    need(case['geometry']['physical_z_edges_cm']==[0,50,100,150] and case['geometry']['radial_regions']==8 and case['geometry']['axial_boundary']=='vacuum at both ends' and case['geometry']['radial_boundary']=='white isotropic albedo one, NOT specular reflection','whole original150cm and radial white/axial vacuum physical configuration')
    need(case['materials']['temperature_C_in_every_zone']==dict(fuel_and_hole=750,clad_and_gap=620,sodium=475) and case['materials']['A']==dict(rnr_cc_p_Pu=.21,rnr_cc_p_U=.79) and case['materials']['B']==dict(rnr_cc_p_Pu=.2436,rnr_cc_p_U=.7564),'original same-temperature A/B fuel materials')
    need(case['production']['groups']==370 and case['production']['fission_components']==32 and case['production']['sn']==8 and case['production']['scat']==3 and case['basis']['requested_rank']==2 and case['basis']['training_slots']==['A','B','A'],'original requested full370G/32-fission/3-scatter and common rank2 scope retained')
    need(case['predeclared_decisions']['shape_targets']['normalized_nu_fission_max_relative_difference_in_fuel_bins']==.03 and case['predeclared_decisions']['shape_targets']['fission_normalized_scalar_flux_volume_weighted_relative_l2_max']==.01 and case['predeclared_decisions']['keff']['abs_reactivity_difference_pcm_max']=='500 + 3*sigma_pcm','original accuracy thresholds unchanged and not qualified by PREP')
    # Stored graph and trace are never parsed or decoded here; Root's actual
    # bounded canonical was their producer, and complete byte pins are saved.
    graphpin=full(O/'input_graph.json');tracepin=full(O/'input_creation_python_open_trace.json')
    need(exact(pin4(summary['actual_input_graph'],'whole graph bytes'),graphpin) and exact(pin4(summary['actual_complete_creation_trace'],'whole creation trace bytes'),tracepin),'entire new graph and trace bytes with no metadata/payload decoding')
    current_joint=sum(row['size_bytes'] for view in observed.values() for row in view['files'].values())+full(C)['size_bytes']
    later=inputs['later_E_files_after_writer_joint_sample']
    need(type(later) is list and len(later)>=2,'explicit complete later-E sample additions supplied by Root')
    laterpins=[supplied(row,'actual later E fullpin') for row in later]
    need(len({row['path'] for row in laterpins})==len(laterpins) and all(Path(row['path']).parent==E for row in laterpins),'finite distinct later E files inside original E root')
    need(str(E/'Root_actual_complete_combined_prepare_summary.json') in {row['path'] for row in laterpins} and str(E/'Root_actual_prepare_metadata_writer_tool_return.json') in {row['path'] for row in laterpins},'summary and genuine writer receipt sampled only later')
    historical_joint=current_joint-sum(row['size_bytes'] for row in laterpins)
    need(type(summary['joint_archive_bytes']) is int and historical_joint==summary['joint_archive_bytes'],'exact original Root writer joint byte sample restored by explicit later outputs')
    need(0<historical_joint<CAPS['joint_archive_bytes'] and current_joint<CAPS['joint_archive_bytes'],'full historical and current H/S/O/T/D/E plus canonical under original2GiB')
    # Every unique pin is reread to full EOF; read-only inspection changes no
    # namespace root, directory, Source or earlier file identity.
    initial=dict(PINS)
    for path,row in initial.items(): need(exact(full(path),row),'final all complete EOF SHA7ID unchanged '+path)
    for root,view in observed.items():
        latest=walk(Path(root));need(exact(latest,view),'final complete files directories aliases unchanged '+root)
    need(type(CHECKS) is list and all(type(row['passed']) is bool and row['passed'] is True for row in CHECKS),'all independent Source META checks exact typed True')
    counts={root:dict(files=len(view['files']),directories=len(view['directories']),symlinks=len(view['symlinks'])) for root,view in observed.items()}
    report=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1',status='PASS_ACTUAL_COMPLETE_PREP_ONLY',source_only=True,source_only_reviewer=True,stdlib_only=True,actual_PREP_closed_EXIT0_verified=True,actual_metadata_writer_closed_EXIT0_verified=True,actual_PREP_metadata_only=True,all_complete_scope_verified=True,all_checks_typed_true=True,check_count=len(CHECKS),checks=CHECKS,blockers=[],actual_PREP_terminal_chunk=rt['chunk_id'],actual_metadata_writer_terminal_chunk=wt['chunk_id'],actual_Root_PREP_summary_pin=given['actual_PREP_summary_pin'],actual_Root_PREP_terminal_pin=given['actual_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=given['actual_complete_namespace_manifest_pin'],actual_metadata_writer_terminal_pin=given['actual_PREP_metadata_writer_terminal_pin'],actual_review_input_contract_pin=args.config_pin,actual_source_freeze_pin=given['actual_prelaunch_Source_freeze_pin'],actual_complete_E_prelaunch_snapshot_pin=given['actual_E_prelaunch_snapshot_pin'],actual_complete_E_postclose_snapshot_pin=given['actual_E_postclose_snapshot_pin'],complete_actual_input_entries=len(all_inputs),complete_unique_reviewed_files=len(PINS),complete_full_EOF_input_pins=list(PINS.values()),namespace_counts=counts,metrics=dict(whole_seconds=h['whole_seconds'],child_seconds=w['elapsed_seconds'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],historical_joint_bytes=historical_joint,current_joint_bytes=current_joint),actual_genuine_guard_caps=CAPS,actual_complete_graph_byte_pin=graphpin,actual_complete_creation_trace_byte_pin=tracepin,large_graph_or_trace_json_or_gzip_payload_read=False,reviewer_called_any_reviewed_API=False,reviewer_imported_or_compiled_candidate=False,numeric_or_native_payload_replayed=False,existing_trim_metadata_API_was_actually_executed_by_Root_PREP=True,original_physical_configuration_and_acceptance_thresholds_preserved=True,independent_reference_admitted=False,new_business_or_numeric_execution=False,cleanup_performed=False,goal_complete=False)
    report.update({key:False for key in CREDIT})
    args.output.mkdir()
    with (args.output/'REVIEW.json').open('x') as f: json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    with (args.output/'REPORT.txt').open('x') as f:
        f.write('PASS: actual complete V25 PREP only. Actual Root closed EXIT0 and its pre-frozen metadata writer closed EXIT0 verified.\n')
        f.write('Full H/S/O/T/D current saved namespaces and separately provided complete E postclose/prelaunch snapshots verified. All original fixed inputs, Source roles and installed canonical unchanged at full EOF SHA/size/7ID.\n')
        f.write('Original1800/600/512/2GiB/96GiB/free8GiB/one-child/one-thread/zero-retry limits retained; actual measurements reported without transferred native RSS credit.\n')
        f.write('All five future BUILD stages and original physical configuration/accuracy thresholds retained. Graph and creation trace are full byte pins only; no payload JSON decoding, business codec, helper/API/native/material execution by this reviewer.\n')
        f.write('Whole BUILD/whole INPUT/native RSS/AAA/ABA/physical balance remain False.\n')
    print(json.dumps(dict(schema=report['schema'],status=report['status'],source_only=True,check_count=report['check_count'],all_checks_typed_true=True,review_pin=raw_full(args.output/'REVIEW.json'),actual_Root_PREP_summary_pin=given['actual_PREP_summary_pin'],actual_Root_PREP_terminal_pin=given['actual_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=given['actual_complete_namespace_manifest_pin'],namespace_counts=counts,metrics=report['metrics']),allow_nan=False))


def raw_full(path):
    p=Path(path); before=identity(p)
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('own saved review changed')
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--inputs',required=True)
    parser.add_argument('--inputs-sha256',required=True)
    parser.add_argument('--inputs-size-bytes',required=True,type=int)
    parser.add_argument('--inputs-identity-json',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('unprofiled nonoptimized independent stdlib reviewer')
    args.config_pin=dict(path=args.inputs,sha256=args.inputs_sha256,size_bytes=args.inputs_size_bytes,identity=strict_bytes(args.inputs_identity_json))
    args.output=Path(args.output)
    review(args)


if __name__=='__main__': main()

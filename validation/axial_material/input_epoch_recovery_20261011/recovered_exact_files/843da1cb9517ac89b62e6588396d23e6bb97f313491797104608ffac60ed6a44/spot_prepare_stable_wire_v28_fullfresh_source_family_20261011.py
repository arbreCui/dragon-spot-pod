from pathlib import Path
import ast
import gc
import hashlib
import json
import os
import resource
import stat
import tempfile
import time

START = time.monotonic()
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
OLD = BASE/'actual_complete_graph_fresh_verifier_v25_sources'
ART = Path('/Users/wen/spot/validation/artifacts')
R = Path(tempfile.mkdtemp(prefix='SPOT_stable_wire_v28_fullfresh_source_only_', dir='/private/tmp'))
S = R/'sources'
S.mkdir()
RECEIPTS = R/'receipts'
RECEIPTS.mkdir()
suffix = R.name.rsplit('_',1)[-1]
HOST = ART/('axial-material-stable-wire-sort-complete-fresh-host-v28-20261011-'+suffix)
OUT = ART/('axial-material-stable-wire-sort-complete-fresh-v28-20261011-'+suffix)
assert not os.path.lexists(HOST) and not os.path.lexists(OUT)

def ident(path):
    v=Path(path).lstat()
    return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]

def pin(path,sha=None):
    path=Path(path);before=ident(path)
    assert stat.S_ISREG(before[2]) and before[3]==1 and not path.is_symlink()
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    h=hashlib.sha256();count=0
    try:
        v=os.fstat(fd)
        assert [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]==before
        for block in iter(lambda:os.read(fd,524288),b''):
            h.update(block);count+=len(block)
        v=os.fstat(fd)
        assert [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]==before
    finally:os.close(fd)
    assert count==before[4] and ident(path)==before
    digest=h.hexdigest()
    if sha is not None:assert digest==sha
    return dict(path=str(path),sha256=digest,size_bytes=count,identity=before)

def compact(p):return {k:p[k] for k in ('path','sha256','identity')}

def put(path,value):
    with Path(path).open('x',encoding='utf8') as stream:
        json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False)
        stream.write('\n');stream.flush();os.fsync(stream.fileno())

def read_json(p):
    before=pin(p)
    value=json.loads(Path(p).read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
    assert pin(p)==before
    return value,before

old_pins={n:pin(OLD/n) for n in ('fresh_verifier_controls.py','fresh_verifier_host.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py','pure_helper_controls.py','pure_helper_controls_host.py')}
assert old_pins['fresh_verifier_controls.py']['sha256']=='a4e0173321ba22ef70fb8179d766c4492e1c1c3d88489d538666bf22f3164e49'
assert old_pins['fresh_verifier_host.py']['sha256']=='3f4c7bff5cc17c79353ef76ee8f6a990e115db63b62b45bd0d6897413c8d2258'
assert old_pins['inactive_audit_snapshot_controls_SOURCE_ONLY.py']['sha256']=='d439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483'
helper=pin('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py','6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3')
assert helper['identity']==[16777229,49645417,33188,1,152950,1791696656438509035,1791696656438509035]
install=pin(ART/'axial-material-stable-wire-sort-source-install-20261011/ACTUAL_SOURCE_INSTALL_WITNESS.json','8a7ec7765b0ecd4acd43d17d70daeb5b2409daffd9caf301757685d7ec8fff38')
installtools=pin('/private/tmp/Root_stable_wire_source_install_actual_tool_returns_20261011.json','7c8897152c3cb390f30ff0ac6b3acb3669159d06753168c92317d091fd7a7309')
graph=pin(ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/input_graph.json','a91c1e63bd768575e715e735886f168b9af6722fddf2bb002317376da5d63ad1')
storage,graph_read_pin=read_json(graph['path'])
assert graph_read_pin==graph
assert type(storage) is dict and set(storage)=={'schema','graph'} and storage['schema']=='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1'
g=storage['graph']
assert g['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and g['consumer_scope'] is None
canonical=g['canonical_files'];trace_table=g['read_trace']['records']
assert canonical['columns']==['path','sha256','size_bytes'] and type(canonical['rows']) is list
assert type(trace_table['row_count']) is int and trace_table['row_count']==len(trace_table['rows'])
attempt_positions={}
for lid,layout in enumerate(trace_table['layouts']):
    matches=[pos for pos,(column,is_string) in enumerate(layout,1) if trace_table['columns'][column]=='attempt_count' and is_string is False]
    assert len(matches)==1
    attempt_positions[lid]=matches[0]
saved_attempts=0
for row in trace_table['rows']:
    attempt=row[attempt_positions[row[0]]]
    assert type(attempt) is int and attempt>0
    saved_attempts+=attempt
assert saved_attempts==g['trace_coverage']['actual_read_open_attempts']
counts=dict(canonical_files=len(canonical['rows']),requirement_row_count=g['requirements']['rows']['row_count'],requirement_column_count=g['requirements']['rows']['column_count'],owners=len(g['owners']['rows']),namespaces=len(g['namespaces']),aliases=len(g['aliases']),saved_trace_records=trace_table['row_count'],saved_trace_actual_attempts=saved_attempts,absence_inputs=len(g['absence_inputs']),closure_categories=len(g['closure_categories']),coverage_categories=len(g['coverage']),actual_canonical_bytes=sum(v[2] for v in canonical['rows']),graph_content_sha256=g['content_sha256'])
assert counts['canonical_files']==37445 and counts['requirement_row_count']==238780 and counts['requirement_column_count']==5
assert counts['namespaces']==86 and counts['aliases']==186 and counts['absence_inputs']==479 and counts['closure_categories']==counts['coverage_categories']==9
assert g['newly_declared_input_paths']=={} and g['newly_declared_input_pins']=={} and g['read_trace']['subprocess_records']==[]
assert all(g[k] is False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified'))
del storage,g,canonical,trace_table,attempt_positions,layout,row;gc.collect()

closure_dir=ART/'axial-material-stable-wire-sort-original-pure-controls-root-closure-v27-20261011-v3'
closure=pin(closure_dir/'ROOT_EXTERNAL_CLOSED_BINDING.json','418da5c9433ee53ed7f2993cbde62bae78fd3ccfb1aa5ad9ddd4d13d5bd966e9')
pure_host=pin(ART/'axial-material-stable-wire-sort-original-pure-controls-host-v27-20261011-odcl3yl4/result.json','0aaed12e13c6109345ab859305d0fbef73a73b8a056343a02e1b0ffd07e974f6')
pure_report=pin(ART/'axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_REPORT.json','b167686da6d8e73123285dc355fd7e3686481b67b82359202c27f28f9fa4ae0f')
pure_tools=pin('/private/tmp/Root_v27_pure_protocol_actual_tool_returns_20261011.json','83cda24cd118a688362eb4f3207d22c459378ca840b2849059ca1a4812cbd45a')
closure_tools=pin('/private/tmp/Root_v27_pure_external_closure_v3_actual_tool_returns_20261011.json')
pure_sources=Path('/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources')
prior_pins=dict(host_result=compact(pure_host),control_report=compact(pure_report),actual_launch_and_closed_tool_returns=compact(pure_tools),Root_external_closed_binding=compact(closure),Root_external_binding_tool_returns=compact(closure_tools))
cl,_=read_json(closure['path']);ph,_=read_json(pure_host['path']);pr,_=read_json(pure_report['path']);pt,_=read_json(pure_tools['path'])
assert cl['schema']=='SPOT_ROOT_ACTUAL_V27_PURE_PROTOCOL_EXTERNAL_CLOSED_BINDING_V1' and cl['status']=='ROOT_BOUND_ACTUAL_PURE_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION'
assert all(cl[k] is False for k in ('new_Q_created','whole_522_to_512_memory_pass','Native_started','AAA_accuracy_qualified','ABA_admitted'))
assert compact(cl['actual_host_result'])==compact(pure_host) and compact(cl['actual_control_report'])==compact(pure_report) and compact(cl['actual_genuine_tool_returns'])==compact(pure_tools)
assert ph['status']=='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' and ph['complete_original_pure_controls_retained'] is True
assert all(ph[k] is False for k in ('helper_admission_created','new_Q_created','whole_family_memory_pass','profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert (ph['whole_wall_cap_seconds'],ph['stage_wall_cap_seconds'],ph['rss_cap_mib'],ph['archive_cap_bytes'],ph['threads'],ph['children_at_once'],ph['retries'])==(60,60,512,64*2**20,1,1,0)
assert pr['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' and compact(pr['helper'])==compact(helper)
assert pt['initial']['chunk_id']=='68ece3' and pt['initial']['session_id']==62042 and pt['closed']['chunk_id']=='3a9510' and type(pt['closed']['exit_code']) is int and pt['closed']['exit_code']==0
actual_terminal_json=json.loads(pt['closed']['output'])
assert actual_terminal_json['status']==ph['status'] and actual_terminal_json['actual_host_result']==compact(pure_host)
del cl,ph,pr,pt,actual_terminal_json;gc.collect()

FRESH=ART/'axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input'
extra_evidence=[pin(pure_sources/n) for n in ('pure_helper_controls.py','pure_helper_controls_host.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py','read_open_short_index_state_controls.py','wire67_saved_evidence_review.py')]
extra_evidence += [pin(Path('/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4')/n) for n in ('FINAL_REVIEW_EVIDENCE_MANIFEST.json','FINAL_SOURCE_ONLY_MANIFEST.json','SOURCE_ONLY_CONTRACT.json','SOURCE_DERIVATION_FULL_INVERSE.json','SOURCE_FAMILY_DECLARATION.json','STATIC_SOURCE_AND_GUARD_REVIEW.json','ACTUAL_STATIC_SOURCE_REVIEW_TOOL_RETURN.json','REPORT_SOURCE_ONLY.txt')]
extra_evidence += [pin(FRESH/n) for n in ('ACTUAL_V3_COMPLETE_VERIFY_GRAPH_PROFILE.json','ACTUAL_V3_FRESH_READ_OPEN_SNAPSHOT.json','FRESH_COMPLETE_V3_PROFILE_DRIVER.py','FRESH_DRIVER_SOURCE_DERIVATION.json','ACTUAL_FRESH_V3_PRELAUNCH_MANIFEST.json','ACTUAL_FRESH_V3_LAUNCH_TOOL_RETURN.json','ACTUAL_FRESH_V3_CLOSED_TOOL_RETURN.json','FINAL_FRESH_COMPLETE_V3_EVIDENCE_MANIFEST.json','FRESH_COMPLETE_V3_SCOPE_REPORT.txt')]
extra_evidence += [pin(FRESH.parent/n) for n in ('ACTUAL_RESULT_PUBLICATION_WITNESS.json','ADDITIONAL_ACTUAL_RESULT_PUBLICATION_WITNESS.json')]
extra_evidence += [pin('/private/tmp/Root_v27_independent_source_review_20261011.json','bcc874295ff418ee1d17c516d015b2eccbb4d7b30117e9e0dcb6ef149505f028')]
evidence=[helper,install,installtools,graph,pure_host,pure_report,pure_tools,closure,closure_tools]+extra_evidence

for name in ('inactive_audit_snapshot_controls_SOURCE_ONLY.py','pure_helper_controls.py','pure_helper_controls_host.py'):
    with (S/name).open('xb') as stream:stream.write((OLD/name).read_bytes())
    assert pin(S/name)['sha256']==old_pins[name]['sha256']

edits={}
def replacement(text,old,new,name,tag,expected=None):
    count=text.count(old)
    assert count>0 and (expected is None or count==expected),(name,tag,count,expected)
    edits.setdefault(name,[]).append(dict(tag=tag,old=old,new=new,occurrences=count))
    return text.replace(old,new)

driver_name='fresh_verifier_controls.py'
d=(OLD/driver_name).read_text()
d=replacement(d,d[:d.index('from __future__')],'''"""Independent installed6a complete current-graph fresh verifier SOURCE only.

No helper, graph, guard or business API is loaded at import. Original complete
default snapshot, three unfiltered gzip artifacts and same-phase private
consume/wire comparison, four positive and three rejection controls remain.
Only Root may authorize the future one-use genuine OwnRSS host execution.
This Source preparation creates no helper Q, whole-build or science admission.
"""
''',driver_name,'honest Source-only description',1)
old_helper='/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
d=replacement(d,repr(old_helper),repr(helper['path']),driver_name,'installed6a path',1)
d=replacement(d,"'3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'",repr(helper['sha256']),driver_name,'installed6a SHA',1)
d=replacement(d,'NEW_HELPER_SOURCE_BYTES = 150986','NEW_HELPER_SOURCE_BYTES = '+str(helper['size_bytes']),driver_name,'installed6a complete bytes',1)
d=replacement(d,'NEW_HELPER_IDENTITY = [16777229, 49430225, 33188, 1, 150986, 1791616446797499263, 1791616446797506096]','NEW_HELPER_IDENTITY = '+repr(helper['identity']),driver_name,'installed6a actual7ID',1)
old_audit=str(OLD/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')
d=replacement(d,repr(old_audit),repr(str(S/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')),driver_name,'byte-identical controller private Source path',1)
d=replacement(d,"OUTPUT_PATH = '/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-v25-20261010'",'OUTPUT_PATH = '+repr(str(OUT)),driver_name,'new exclusive output family',1)
graph_start=d.index('GRAPH_PIN = {');graph_end=d.index('\nPHASE =',graph_start)
d=replacement(d,d[graph_start:graph_end],'GRAPH_PIN = '+repr(compact(graph)),driver_name,'actual current v25 stored graph EOF+7ID',1)
for before,after,label in [('37111',str(counts['canonical_files']),'canonical count'),('37112',str(counts['canonical_files']+1),'same-phase actual graph+canonical opens'),('238441',str(counts['requirement_row_count']),'full requirement rows'),('4473',str(counts['owners']),'complete logical owners'),('63469',str(counts['saved_trace_records']),'complete saved trace records')]:
    d=replacement(d,before,after,driver_name,label)
d=replacement(d,'fixed V20','fixed current V25',driver_name,'current graph provenance label')
ast.parse(d)
with (S/driver_name).open('x') as stream:stream.write(d)
driver=pin(S/driver_name)

host_name='fresh_verifier_host.py'
h=(OLD/host_name).read_text()
h=replacement(h,'"""UNREADY complete current graph fresh verifier, unchanged genuine guard."""','"""Source-only installed6a full fresh protocol; original genuine guard unchanged."""',host_name,'honest Source-only description',1)
for old_line,new_line,tag in [
 ("HOST = Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-host-v25-20261010')",'HOST = Path('+repr(str(HOST))+')','new genuine host family'),
 ("OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-v25-20261010')",'OUT = Path('+repr(str(OUT))+')','new exclusive full output family'),
 ("SOURCE_ARCHIVE = BASE/'actual_complete_graph_fresh_verifier_v25_sources'",'SOURCE_ARCHIVE = Path('+repr(str(S))+')','new Source namespace'),
 ("RECEIPTS = BASE/'actual_complete_graph_fresh_verifier_v25_receipts'",'RECEIPTS = Path('+repr(str(RECEIPTS))+')','new receipt namespace; unchanged joint64MiB accounting'),
 ("TARGET_SHA = 'a4e0173321ba22ef70fb8179d766c4492e1c1c3d88489d538666bf22f3164e49'",'TARGET_SHA = '+repr(driver['sha256']),'actual frozen new driver SHA'),
 (repr(old_audit),repr(str(S/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')),'byte-identical controller actual Source')]:
    h=replacement(h,old_line,new_line,host_name,tag,1)
for variable,newpin in [('BOUND_HELPER_PIN',compact(helper)),('INSTALL_WITNESS_PIN',compact(installtools)),('SOURCE_INSTALL_RECORD_PIN',compact(install))]:
    old_line=next(line for line in h.splitlines() if line.startswith(variable+' = '))
    h=replacement(h,old_line,variable+' = '+repr(newpin),host_name,variable+' actual installed Source/Root closed pins',1)
for variable,value in [('GRAPH_PATH','Path('+repr(graph['path'])+')'),('GRAPH_SHA',repr(graph['sha256'])),('GRAPH_IDENTITY',repr(graph['identity']))]:
    old_line=next(line for line in h.splitlines() if line.startswith(variable+'='))
    h=replacement(h,old_line,variable+'='+value,host_name,variable+' actual current full stored graph',1)
for before,after,label in [('37111',str(counts['canonical_files']),'canonical count'),('37112',str(counts['canonical_files']+1),'same-phase actual graph+canonical opens'),('238441',str(counts['requirement_row_count']),'full requirement rows'),('4473',str(counts['owners']),'complete logical owners'),('63469',str(counts['saved_trace_records']),'complete saved trace records')]:
    h=replacement(h,before,after,host_name,label)
addition='PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS = '+repr(prior_pins)+'\nSUPPORTING_ACTUAL_EVIDENCE_PINS = '+repr([compact(p) for p in extra_evidence])+'\n'
h=replacement(h,'UNKNOWN_Q=None\n',addition+'UNKNOWN_Q=None\n',host_name,'actual already closed v27 protocol plus finite fresh ancestry; no Q',1)
old_inputs="    inputs=[support.pin(TARGET,TARGET_SHA),"
evidence_block='''    # Ordinary saved receipts and complete control report are full EOF pinned.
    # Purpose-built protocol fixture symlinks remain in Root's lstat closure;
    # no regular-file Source pin follows or relabels those symlinks here.
    prior_pins=list(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS.values())+SUPPORTING_ACTUAL_EVIDENCE_PINS
    if [support.pin(p['path'],p['sha256']) for p in prior_pins]!=prior_pins:
        raise ValueError('actual closed6a protocol/finite observation evidence changed')
    prior_host=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['host_result']['path'])
    prior_control=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['control_report']['path'])
    prior_tool=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['actual_launch_and_closed_tool_returns']['path'])
    prior_closed=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['Root_external_closed_binding']['path'])
    if prior_host['status']!='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' or prior_host['complete_original_pure_controls_retained'] is not True or any(prior_host[k] is not False for k in ('helper_admission_created','new_Q_created','whole_family_memory_pass','profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')):
        raise ValueError('saved genuine6a pure protocol and honest prior scope required')
    if (prior_host['whole_wall_cap_seconds'],prior_host['stage_wall_cap_seconds'],prior_host['rss_cap_mib'],prior_host['archive_cap_bytes'],prior_host['threads'],prior_host['children_at_once'],prior_host['retries'])!=(60,60,512,64*2**20,1,1,0) or prior_control['status']!='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' or {k:prior_control['helper'][k] for k in ('path','sha256','identity')}!=BOUND_HELPER_PIN:
        raise ValueError('complete original actual60/60 installed6a pure protocol binding required')
    if prior_tool['initial']['chunk_id']!='68ece3' or type(prior_tool['initial']['session_id']) is not int or prior_tool['initial']['session_id']!=62042 or prior_tool['closed']['chunk_id']!='3a9510' or type(prior_tool['closed']['exit_code']) is not int or prior_tool['closed']['exit_code']!=0:
        raise ValueError('one real Root pure protocol launch/closed0 required')
    prior_terminal=json.loads(prior_tool['closed']['output'],parse_constant=_fail_constant)
    if prior_terminal['status']!=prior_host['status'] or prior_terminal['actual_host_result']!=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['host_result']:
        raise ValueError('actual complete untruncated pure terminal host binding required')
    if prior_closed['schema']!='SPOT_ROOT_ACTUAL_V27_PURE_PROTOCOL_EXTERNAL_CLOSED_BINDING_V1' or prior_closed['status']!='ROOT_BOUND_ACTUAL_PURE_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION' or any(prior_closed[k] is not False for k in ('new_Q_created','whole_522_to_512_memory_pass','Native_started','AAA_accuracy_qualified','ABA_admitted')):
        raise ValueError('actual external Root pure closure remains finite evidence only')
    for field,key in (('actual_host_result','host_result'),('actual_control_report','control_report'),('actual_genuine_tool_returns','actual_launch_and_closed_tool_returns')):
        if {k:prior_closed[field][k] for k in ('path','sha256','identity')}!=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS[key]:raise ValueError('actual Root closure full ordinary evidence bindings differ')
    # A saved pure control result and the earlier sampled fresh observation
    # never replace this new phase's actual complete graph and canonical reads.
    del prior_host,prior_control,prior_tool,prior_closed,prior_terminal
'''
h=replacement(h,old_inputs,evidence_block+old_inputs,host_name,'bind original6a actual pure protocol without replacing fresh qualification',1)
old_tail="INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN]+source_before['files']"
h=replacement(h,old_tail,old_tail+'+prior_pins',host_name,'before-after EOF+7ID pins for every new saved evidence input',1)
h=replacement(h,"schema='AXMAT_V25_GENUINE_COMPLETE_PRIVATE_INACTIVE_AUDIT_CURRENT_GRAPH_HOST_V1'","schema='AXMAT_V28_GENUINE_COMPLETE_SHORT_INDEX_STABLE_WIRE_SORT_PRIVATE_INACTIVE_AUDIT_CURRENT_GRAPH_HOST_V1',prior_actual_6a_pure_protocol_closed_pins=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS,supporting_finite_actual_evidence_pins=SUPPORTING_ACTUAL_EVIDENCE_PINS,new_Q_created=False,whole_522_to_512_memory_pass=False",host_name,'distinct family and explicit noQ/no whole-build qualification',1)
ast.parse(h)
with (S/host_name).open('x') as stream:stream.write(h)
host=pin(S/host_name)

def top_functions(src):
    return {v.name:ast.dump(v,include_attributes=False) for v in ast.parse(src).body if isinstance(v,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

ast_reviews={}
for name,original,newsrc,allowed in [(driver_name,(OLD/driver_name).read_text(),d,{'expected_return_from_old','run'}),(host_name,(OLD/host_name).read_text(),h,{'_full_controls','main'})]:
    o=top_functions(original);n=top_functions(newsrc)
    assert set(o)==set(n)
    changes=[k for k in o if o[k]!=n[k]]
    assert set(changes)==allowed,(name,changes)
    restored=newsrc
    for e in reversed(edits[name]):
        assert restored.count(e['new'])==e['occurrences'],(name,e['tag'],'inverse occurrence differs')
        restored=restored.replace(e['new'],e['old'])
    assert restored.encode()==original.encode() and hashlib.sha256(restored.encode()).hexdigest()==old_pins[name]['sha256']
    ast_reviews[name]=dict(only_changed_functions=changes,complete_inverse_bytes_sha_equal_original=True,complete_AST_restored_equal_original=True,all_other_original_function_and_class_AST_exact=True,original_source=old_pins[name],candidate_source=driver if name==driver_name else host)

oldh=(OLD/host_name).read_text()
guard_start="    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')"
guard_end="        value=dict("
assert oldh[oldh.index(guard_start):oldh.index(guard_end)]==h[h.index(guard_start):h.index(guard_end)]
old_private=(OLD/driver_name).read_text()
old_ast=top_functions(old_private);new_ast=top_functions(d)
for name in ('private_trace_controls','_old_parent_complete_return_constructors','lossless_json_gzip','exact_value','checkpoint','load_snapshot_control_Source','value_snapshot','main'):
    assert old_ast[name]==new_ast[name]

all_external_after=[pin(p['path'],p['sha256']) for p in evidence]
assert all_external_after==evidence
assert {n:pin(OLD/n) for n in old_pins}==old_pins
source_pins=[pin(p) for p in sorted(S.iterdir())]
directory_id=ident(S)
expected_trace_fields=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
contract=dict(schema='SPOT_INSTALLED6A_ORIGINAL_FULL_FRESH_PROTOCOL_SOURCE_ONLY_CONTRACT_V28',status='FIXED_SOURCE_ONLY_PENDING_ROOT_INDEPENDENT_REVIEW_NO_EXECUTION',installed_helper=helper,installed_source_witness=install,actual_install_launch_closed_receipts=installtools,actual_prior_pure_protocol_closed_pins=prior_pins,complete_current_graph=graph,complete_current_graph_counts=counts,Source_archive=str(S),Source_namespace_directory_identity=directory_id,Source_files=source_pins,HOST=str(HOST),OUT=str(OUT),RECEIPTS=str(RECEIPTS),phase='helper_complete_fresh_verifier_control',caps=dict(whole_host_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_SOURCE_OUT_SOURCE_RECEIPTS_archive_bytes=64*2**20,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0),original_complete_contract=dict(expected_return_source='independently pinned original bcd strict parser and all original complete return constructors; no fresh old baseline',genuine_new_phase_reads='all37445 canonical bytes EOF plus one original stored graph read; no cache or selected files',actual_complete_read_open_records=37446,default_snapshot='all original records identity/type/order/value/floatbits unchanged',gzip='all expected return, actual return and actual default trace JSON fields/rows; full decompression EOF/SHA',private_last_use='same original inactive audit builtin dict and same graph/input phase; default buffer released only after complete gzip and full ordered/type/bit pin',consumed_vs_default='all nine fields, types/order/values/IEEE/counts, every encoded byte against same-phase complete default gzip EOF',trace_fields=expected_trace_fields,small_trace_controls='same original four positive and three rejection control function AST',genuine_supervision='original619 guard + OwnRSSSerialExecutor/production.SerialExecutor MRO, five original history roots, dynamic history/free checks and original own-worker process observer unchanged'),new_helper_Q_created=False,whole_522_to_512_memory_pass=False,physical_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,Native_solver_training_or_PS_started=False,Root_external_review_and_actual_launch_closed0_required=True,environment='original openmc-dev Python3.12 -B; five thread variables1; future host own-worker/child ps needs original require_escalated authorization, never a monitor patch or sandbox-default retry')
put(RECEIPTS/'SOURCE_CONTRACT.json',contract)
derivation=dict(schema='SPOT_INSTALLED6A_ORIGINAL_FULL_FRESH_PROTOCOL_SOURCE_DERIVATION_V28',edits=edits,AST_and_complete_inverse_reviews=ast_reviews,original_genuine_guard_supervision_resource_archive_and_final_checks_byte_exact=True,byte_identical_copied_original_ancestry={n:dict(original=old_pins[n],candidate=pin(S/n)) for n in ('inactive_audit_snapshot_controls_SOURCE_ONLY.py','pure_helper_controls.py','pure_helper_controls_host.py')},actual_complete_current_graph_metadata_read_only=counts,no_canonical_payloads_read=True,no_helper_or_Controller_imported=True,no_protocol_controls_executed=True,no_original_Source_or_result_written=True,all_external_inputs_before_after=evidence)
put(RECEIPTS/'SOURCE_DERIVATION_RECORD.json',derivation)
declaration=dict(schema='SPOT_FULL_FRESH_V28_ONE_USE_DECLARATION_SOURCE_ONLY',status='PENDING_ROOT_INDEPENDENT_REVIEW_NOT_LAUNCHED',HOST=str(HOST),OUT=str(OUT),SOURCE=str(S),RECEIPTS=str(RECEIPTS),declared_history_roots=[str(HOST),str(OUT),str(ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'),str(ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'),str(ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010')],complete_history_root=str(ART),original_complete_history_guard='DynamicHistoryResources original full metadata scan before/during/after; no selected old history',archive_roots=[str(HOST),str(OUT),str(S),str(RECEIPTS)],archive_cap_bytes=64*2**20,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,original_external_DE_history='Parent Root retains original joint DE accounting and freezes; this host does not broaden or replace their original guard',launch_requires_original_own_worker_ps_escalation=True,no_child_retry=True,no_Native_or_solver=True,no_Q=True,no_whole_build_RSS_claim=True)
put(RECEIPTS/'DECLARATION_SOURCE_ONLY.json',declaration)
report='''Installed6a original full fresh protocol Source-only, independent v28 family.

No host/driver/helper/controller was imported or executed. No canonical payload
was read, no Q or Native/solver/PS was created, and no project file was written.
Original v25 Source is immutable; new sources and inverse evidence are TMP only.

The new driver binds the actual installed 152950-byte 6a helper and the entire
current v25 stored graph. Independent expected all27 return constructors remain
the original bcd implementation; this does not run an old fresh baseline.
The future once-only fresh phase reads all37445 canonical files plus the graph.
It retains default complete snapshot, all three full lossless gzip artifacts,
same inactive builtin owned map consumption, all9 snapshot fields, complete
type/order/value/IEEE/counts and every consumed/default encoded byte against
the same-phase default gzip through full EOF. Four positive and three rejection
controls and their AST remain exactly original. No fields or rows are selected.

Original genuine OwnRSS supervisor/MRO and complete guard block are byte-exact.
Caps remain1800/600s,512MiB,archive64MiB,history96GiB,free8GiB,threads1,
children1,retries0. Actual prior v27 pure protocol remains60/60,distinct evidence;
it does not qualify the new full fresh phase. New family binds actual complete
v27 host/control report, genuine untruncated launch/closed0 tool receipt and
Root closed binding. Publication tool output truncation is not parsed as facts.
Intentional protocol fixture symlinks are not followed by normal Source pins.

All original Sources and ordinary actual receipts were fullEOF+7ID pinned before
and after preparation. Full replacement inverse recovers original bytes/SHA/AST.
Only expected_return_from_old/run in driver and _full_controls/main in host
change, plus binding constants and honest descriptions. All original copied
ancestry files are byte-identical and are not reused as new-helper PASS results.

This is NOT an executed full fresh result, NOT new6aQ, NOT a whole-build512MiB
pass and NOT science admission. Root independent Source review is required before
the future unique host launch. Own-worker/child process observation must use the
original require_escalated route; do not patch monitoring or retry old family.
'''
with (RECEIPTS/'REPORT_SOURCE_ONLY.txt').open('x') as stream:stream.write(report)
manifest=dict(schema='SPOT_FULL_FRESH_V28_FIXED_SOURCE_ONLY_MANIFEST',status='SOURCE_FIXED_NOT_EXECUTED_PENDING_ROOT_REVIEW',root=str(R),Source_namespace_directory_identity=directory_id,Source_files=source_pins,receipt_files=[pin(p) for p in sorted(RECEIPTS.iterdir())],all_external_actual_evidence_pins=evidence,old_Source_pins=list(old_pins.values()),driver=driver,host=host,HOST=str(HOST),OUT=str(OUT),unique_future_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(S/host_name)],thread_environment={k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')},Root_independent_review_required=True,launches_performed=0,children_started=0,helper_or_controller_imports=0,Q_created=False,whole512_RSS_verified=False,science_qualified=False,Source_preparation_seconds=time.monotonic()-START,Source_preparation_own_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert manifest['Source_preparation_seconds']<60 and manifest['Source_preparation_own_peak_rss_bytes']<512*2**20
put(R/'FINAL_SOURCE_ONLY_MANIFEST.json',manifest)
assert ident(S)==directory_id and [pin(p) for p in sorted(S.iterdir())]==source_pins
print(json.dumps(dict(status=manifest['status'],root=str(R),driver=driver,host=host,manifest=pin(R/'FINAL_SOURCE_ONLY_MANIFEST.json'),contract=pin(RECEIPTS/'SOURCE_CONTRACT.json'),derivation=pin(RECEIPTS/'SOURCE_DERIVATION_RECORD.json'),counts=counts,elapsed_seconds=time.monotonic()-START,own_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),allow_nan=False),flush=True)

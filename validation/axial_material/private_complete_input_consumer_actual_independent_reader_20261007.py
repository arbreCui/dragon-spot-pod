import ast,hashlib,json,math,os,stat,struct
from pathlib import Path
D=Path('/Users/wen/spot/validation/artifacts/axial-material-private-complete-input-consumer-pilot-evidence-20261007')
ROOT_SHA='d1d319069eecc4ac19ddeb8ef35de108bc2d3d987400b18520d9caca9b3c4f0e'
OUT=Path('/private/tmp/axmat_zero_private_complete_input_pilot_actual_readonly_report_20261007.json')
SIG=('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink')
def sig(s):return tuple(getattr(s,k)for k in SIG)
def normal(p):
 p=Path(p);assert p.is_absolute() and '..'not in p.parts
 for a in [*reversed(p.parents),p]:
  s=a.lstat();assert not stat.S_ISLNK(s.st_mode)
  if a!=p:assert stat.S_ISDIR(s.st_mode)
 return p
fresh={};inodes={}
def hashed(p):
 p=normal(p);first=p.lstat();assert stat.S_ISREG(first.st_mode) and first.st_nlink==1
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  opened=os.fstat(fd);assert sig(first)==sig(opened);h=hashlib.sha256();n=0
  while block:=os.read(fd,1024*1024):h.update(block);n+=len(block)
  final=os.fstat(fd);normal(p);post=p.lstat();assert sig(first)==sig(final)==sig(post) and n==first.st_size
 finally:os.close(fd)
 fresh[str(p)]={'sha256':h.hexdigest(),'bytes':n};key=(first.st_dev,first.st_ino)
 if key in inodes:assert inodes[key]==str(p)
 inodes[key]=str(p);return h.hexdigest(),n

def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d;d[k]=v
 return d

def parsed(p):
 def finite(x):
  v=float(x);assert math.isfinite(v);return v
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique,parse_float=finite,parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite')))

def same(a,b):
 assert type(a)is type(b)
 if type(a)is dict:
  assert set(a)==set(b)
  for k in a:same(a[k],b[k])
 elif type(a)is list:
  assert len(a)==len(b)
  for x,y in zip(a,b):same(x,y)
 elif type(a)is float:assert struct.pack('>d',a)==struct.pack('>d',b)
 else:assert a==b

def scan():
 normal(D);files={};dirs=[];dirstats={}
 def walk(folder):
  before=folder.lstat();assert stat.S_ISDIR(before.st_mode);names=[]
  with os.scandir(folder)as entries:
   for ent in entries:
    p=Path(ent.path);s=ent.stat(follow_symlinks=False);names.append(ent.name)
    assert not stat.S_ISLNK(s.st_mode)
    relative=str(p.relative_to(D))
    if stat.S_ISDIR(s.st_mode):dirs.append(relative);walk(p)
    else:assert stat.S_ISREG(s.st_mode);files[relative]=hashed(p)
  assert sorted(names)==sorted(os.listdir(folder)) and sig(before)==sig(folder.lstat())
 walk(D);return files,sorted(dirs)
files,dirs=scan();assert files['Root_terminal_return.json'][0]==ROOT_SHA
r=parsed(D/'Root_terminal_return.json');v=r['payload_inventory']
assert len(files)==36 and v['file_count']==35 and v['bytes']==1057342 and v['symlinks']=={}
assert dirs==sorted(v['directories']) and {k:a[0]for k,a in files.items()if k!='Root_terminal_return.json'}==v['files']
assert sum(a[1]for k,a in files.items()if k!='Root_terminal_return.json')==v['bytes']
assert set(r['source_payload_pins'])==set(v['files'])
for k,h in v['files'].items():assert r['source_payload_pins'][k]['sha256']==h
assert r['schema']=='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_ROOT_ACTUAL_RETURN_V1'
same(r['actual_tool'],dict(initial_chunk_id='95f8ac',session_id=20693,terminal_chunk_id='ba86b2',exit_code=0))
assert type(r['actual_exit_code'])is int and r['actual_exit_code']==0 and r['record_written_after_actual_tool_return'] is True

def durable_pin(x,rel):same(x,dict(path=str(D/rel),sha256=files[rel][0]))
for key,rel in {'successful_pilot_binding':'v2_sources/pilot_binding.json','actual_host_result':'v2_work/result.json','actual_child_result':'v2_work/consumer/result.json','actual_watchdog':'v2_work/consumer/consume.watchdog.json','actual_stage_records':'v2_work/STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT/stages.json','host_stdout':'v2_terminal/host.stdout','host_stderr':'v2_terminal/host.stderr','whole_child_merged_stream':'v2_work/consumer/consume.log','prior_failed_host_receipt':'v1_terminal/Root_terminal_return.json'}.items():durable_pin(r[key],rel)
h=parsed(D/'v2_work/result.json');c=parsed(D/'v2_work/consumer/result.json');watch=parsed(D/'v2_work/consumer/consume.watchdog.json');stage_doc=parsed(D/'v2_work/STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT/stages.json');stages=stage_doc['stages'];binding=parsed(D/'v2_sources/pilot_binding.json')
assert set(stage_doc)=={'stages'} and len(stages)==1
same(parsed(D/'v2_terminal/host.stdout'),h);assert files['v2_terminal/host.stderr'][1]==0
assert (D/'v2_work/consumer/consume.log').read_bytes()==b'AXMAT-PRIVATE-COMPLETE-INPUT-CONSUMER-PILOT-RETURNED\n'
assert h['schema']=='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_ACTUAL_HOST_V1' and c['schema']=='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_ACTUAL_CHILD_V1'
prefix='/private/tmp/axmat-private-complete-input-consumer-pilot-bound-v2-20261007';work='/private/tmp/axmat-private-complete-input-consumer-pilot-actual-v2-20261007';python='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12';bsha='0715187b8ce9cd34999615e58b0d8af340bd8bd3e82ecba6754d06803bae29fa'
assert files['v2_sources/pilot_binding.json'][0]==bsha
expected_binding=dict(path=prefix+'/pilot_binding.json',sha256=bsha);same(h['binding'],expected_binding);same(c['binding'],expected_binding)
command=[python,prefix+'/readonly_complete_input_consumer_pilot_child.py','--binding',expected_binding['path'],'--binding-sha256',bsha]
same(r['actual_host_command'],[python,prefix+'/readonly_complete_input_consumer_pilot_host.py','--binding',expected_binding['path'],'--binding-sha256',bsha])
for obj in (h,watch,stages[0]):same(obj['actual_command']if 'actual_command'in obj else obj['command'],command)
same(h['watchdog'],watch);same(h['stage_records'],stages)
same(h['child_result'],dict(path=work+'/consumer/result.json',sha256=files['v2_work/consumer/result.json'][0]))
assert stages[0]['label']=='consumer/consume' and stages[0]['status']=='PASS' and stages[0]['log_sha256']==files['v2_work/consumer/consume.log'][0]
assert type(watch['returncode'])is int and watch['returncode']==0 and type(watch['pid'])is int and watch['pid']==35998
assert watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['rss_cap_mib']==512
assert 0<watch['sampled_peak_rss_mib']==r['sampled_private_consumer_child_peak_RSS_mib']==440.40625<512
assert 0<c['elapsed_seconds']<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stages[0]['wall_cap_seconds']<=600
assert stages[0]['elapsed_seconds']<600 and 0<h['whole_elapsed_seconds']==r['whole_elapsed_seconds']<1800
assert r['actual_child_pid']==watch['pid'] and type(r['actual_child_returncode'])is int and r['actual_child_returncode']==watch['returncode']
for obj in (r,h):
 assert obj['total_wall_cap_seconds']==1800 and obj['stage_wall_cap_seconds']==600 and obj['RSS_cap_mib']==512 and obj['threads']==1 and obj['children_at_once']==1 and obj['retries']==0
assert r['history_cap_GiB']==96 and r['min_free_GiB']==8
false=['cold_MRO_proved','cold_fixture_passed','component_API_executed','cold_controller_imported','cold_controller_bound','cold_prepared','physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted']
for obj in (r,h,c):
 for k in false:assert obj[k]is False
assert c['consumer_scope_used']is False and c['RSS_qualification_claimed']is False
assert r['raw_phase_open_trace_separately_persisted']is False and r['phase_open_count_checked_in_actual_source']is True
assert r['separate_child_stderr_observation_claimed']is False and r['child_stderr_combined_into_actual_log']is True
same(c['complete_INPUT_evidence'],r['complete_INPUT_phase_observation']);e=c['complete_INPUT_evidence']
counts=dict(canonical_graph_files=29141,canonical_graph_bytes=35310152108,logical_owner_edges=196284,exhaustive_graph_namespaces=75,total_canonical_expected_files=29204,additional_success_intake_bytes=55089235,additional_canonical_files_freshly_read=62)
for k,n in counts.items():assert type(e[k])is int and e[k]==n
assert 29141+62+1==29204
assert e['semantics']=='COMPLETE_FRESH_COLD_INPUT_REUSE_NOT_COMPONENT_API_REEXECUTION' and e['phase']=='standalone_readonly_pilot'
for k in ('trace_content_sha256','additional_trace_content_sha256'):assert len(e[k])==64 and all(x in '0123456789abcdef'for x in e[k])
for k in ('original_component_APIs_executed_in_this_process','consumer_scope_used','new_binding_fixture_pass_claimed','science_qualification'):assert e[k]is False
assert c['whole_component_return_keys']==['original92','memory438','physical','dedup','capture','combined']
for when in ('current_before','current_after'):
 cc=e[when];assert cc['ordinary']['original_ordinary_files']==26784 and cc['ordinary']['original_literal_aliases']==2 and cc['ordinary']['original_namespace_roots']==9
 assert len(cc['paths']['current_component_labels'])==7 and len(cc['paths']['original_named_absences'])==24 and cc['paths']['producer_modules_called']is False
 cb=cc['cold_binding'];assert cb['current_cold_MRO_established']is False and cb['new_binding_fixture_pass_claimed']is False and cb['INPUT_only_no_controller_or_transport_credit']is True
 resources=cb['resources'];assert resources['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
 assert resources['artifact_budget_bytes']==96*2**30 and resources['min_free_bytes']==8*2**30 and resources['artifact_bytes']<96*2**30 and resources['disk_free_bytes']>8*2**30
for name in ('resources_before','resources_after'):
 res=h[name];assert res['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and res['artifact_budget_bytes']==96*2**30 and res['min_free_bytes']==8*2**30 and res['artifact_bytes']<96*2**30 and res['disk_free_bytes']>8*2**30
assert binding['pilot_context']['runtime_context']is None and binding['pilot_context']['allow_unbound_initial_INPUT_declaration']is True and 'binding_descriptor'not in binding
assert len(binding['supervisor_expected_files'])==113
for p,s in binding['supervisor_expected_files'].items():assert binding['pilot_context']['additional_expected_files'][p]==s
for name in ('readonly_complete_input_consumer.py','readonly_complete_input_consumer_pilot_host.py','readonly_complete_input_consumer_pilot_child.py'):
 assert binding['pilot_context']['additional_expected_files'][prefix+'/'+name]==files['v2_sources/'+name][0]
 assert (D/'v2_sources'/name).read_bytes()==(D/'v1_sources'/name).read_bytes()
same(c['private_consumer'],binding['binding_source']);same(c['actual_child_source'],binding['pilot_child'])
assert binding['pilot_context']['additional_expected_files'][work+'/runtime/run_bounded_dragon.py']==files['v2_work/runtime/run_bounded_dragon.py'][0]=='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
assert binding['api_return']['sha256']=='26e553e717b443e4cdfb5afc1df9471b4a6cd4100ec4f137b328354c25c37709' and binding['actual_bounded_api_terminal_evidence']['sha256']=='2f1f45f38ededf7cc6d30736cf1777ca792478fa536c54ac81b96cf304a9347e'
assert binding['complete_historical_input_graph']['sha256']=='a95a9ba555e082628637aaafab0941d84a189de66d42ea987f19cf6b4b2fad06'
assert h['supervisor_source']['sha256']=='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6' and h['parent_source']['sha256']=='38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
def defs(s):return {n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
consumer=(D/'v2_sources/readonly_complete_input_consumer.py').read_text();draft=(D/'source_draft/readonly_complete_input_consumer.py').read_text();assert consumer==draft and len(defs(consumer))==23
inverse=parsed(D/'source_draft/consumer_source_inverse.json');assert inverse['old_source']['sha256']=='81ceb9daac17747a35c8d874226f47ac5b459ea888df4e2948b229f9bd71bc76'
restored=consumer
for region in reversed(inverse['regions']):assert restored.count(region['new'])==1;restored=restored.replace(region['new'],region['old'],1)
assert hashlib.sha256(restored.encode()).hexdigest()==inverse['old_source']['sha256'] and defs(restored)==defs(consumer)
assert 'len(regular)!=len(pathset)'in consumer and "len(regular)!=verified['canonical_files_read']"in consumer and "any(r['attempt_count']!=1 for r in regular)"in consumer
assert "{r['path']for r in extra_trace['records']}!=set(additional)"in consumer
v1=parsed(D/'v1_terminal/Root_terminal_return.json');assert files['v1_terminal/Root_terminal_return.json'][0]=='33a58cea92aa2ac87a6aaeb411489a18f72d9f02310e7e47c995de202519586d'
assert v1['actual_tool']['chunk_id']=='939a4d' and type(v1['actual_tool']['exit_code'])is int and v1['actual_tool']['exit_code']==1 and v1['actual_tool']['session_id']is None
assert v1['exclusive_work_base_absent_observed']is True and v1['actual_child_started']is False and v1['stage_or_watchdog_or_result_created']is False and files['v1_terminal/host.stdout'][1]==0
assert b'probe_refined_AAA_white_odd_response.py' in (D/'v1_terminal/host.stderr').read_bytes()
for k in ('actual_pilot_performance_qualified','cold_controller_bound','cold_prepared','cold_fixture_passed','combined_native_RSS_proved','AAA_accuracy_qualified','ABA_admitted'):assert v1[k]is False
assert parsed(D/'v2_sources/source_binding_owner_addition_review.json')['provenance']['original_declaration']['sha256']=='f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b'
second_files,second_dirs=scan();assert files==second_files and dirs==second_dirs
report=dict(schema='AXMAT_ZERO_PRIVATE_COMPLETE_INPUT_PILOT_ACTUAL_READONLY_AUDIT_V1',classification='PASS_ACTUAL_STANDALONE_COMPLETE_INPUT_PILOT_EVIDENCE_ONLY',root_receipt=dict(path=str(D/'Root_terminal_return.json'),sha256=ROOT_SHA),actual_tool=r['actual_tool'],fresh_hash_scope=dict(payload_files=35,payload_bytes=v['bytes'],root_receipt_bytes=files['Root_terminal_return.json'][1],total_regular_files=36,total_bytes=sum(x[1]for x in files.values()),directory_count=len(dirs),namespace_enumerations=2,no_aliases=True,nlink1=True,distinct_file_inodes=len(inodes),all_retained_payload_and_root_SHA_fresh=True,external_graph_or35GB_inputs_freshly_hashed_by_this_reader=False),actual_single_child=dict(pid=watch['pid'],returncode=watch['returncode'],sampled_peak_RSS_mib=watch['sampled_peak_rss_mib'],elapsed_seconds=watch['elapsed_seconds'],limit_failure=watch['limit_failure'],cleanup=watch['liveness_group_cleanup'],whole_host_seconds=h['whole_elapsed_seconds']),saved_complete_INPUT_counts=counts,raw_trace_limit=dict(trace_digests_retained=True,raw_trace_separately_saved=False,source_open_count_assertions_present=True,raw_trace_independently_recounted_by_this_reader=False),actual_current_and_all_expected_binding_retained=True,consumer_23defs_inverse_81ce=True,source_owner_v2_fix_only=True,original_supervisor_MRO_source_identity_bound=True,v1_failed_without_child_preserved=True,original_caps=dict(family_GiB=96,free_GiB=8,RSS_mib=512,total_seconds=1800,stage_seconds=600,threads=1,children=1,retries=0),scope_limit='This actual readonly callback pilot demonstrates the retained standalone INPUT consumption under its own recorded limits. It does not establish cold callback binding/MRO fixture, native transport RSS, full FLU, AAA/ABA science, or104GiB authorization.',flags={k:False for k in ['project_API_invoked_by_reader','business_imported_by_reader','solver_or_fixture_reexecuted','ART_modified','cold_native_or_science_qualification_granted']},payload_hashes={k:{'sha256':x[0],'bytes':x[1]}for k,x in files.items()})
with OUT.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(classification=report['classification'],report=str(OUT),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),fresh_regular_files=len(files),actual_child_RSS_mib=watch['sampled_peak_rss_mib'],whole_seconds=h['whole_elapsed_seconds']),indent=2))

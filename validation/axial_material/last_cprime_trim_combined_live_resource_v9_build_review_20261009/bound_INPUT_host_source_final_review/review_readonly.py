import ast
import copy
import datetime
import hashlib
import json
import os
import stat
from pathlib import Path

HERE=Path(__file__).resolve().parent
A=Path('/Users/wen/spot/validation/axial_material')
B=Path('/Users/wen/spot/validation/artifacts')
R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
T=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
D=Path('/private/tmp/axmat-trim-v9-bounded-runtime-input-intake-source-draft-20261009')
C=Path('/private/tmp/axmat-trim-v9-bounded-runtime-input-intake-bound-candidate-20261009')
NAME='axmat_trim_v9_standalone_bounded_runtime_api_intake_host_20261009.py'
PINS=[]

def ident(p):
 s=p.lstat()
 assert stat.S_ISREG(s.st_mode) and not stat.S_ISLNK(s.st_mode)
 return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def read(p,sha=None):
 before=ident(p); raw=p.read_bytes(); after=ident(p)
 assert before==after, str(p)
 h=hashlib.sha256(raw).hexdigest()
 if sha is not None: assert h==sha,(str(p),h,sha)
 PINS.append(dict(path=str(p),bytes=len(raw),sha256=h,identity=before))
 return raw

def meta(p,sha=None):return json.loads(read(p,sha))
def assigns(tree):
 return {n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}

mother=read(D/NAME,'9c1676f346d118b0d9fad344cde6b5c40705b681a7e971b703c8cefa8f688627').decode()
candidate=read(C/NAME,'180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae').decode()
mt=ast.parse(mother); ct=ast.parse(candidate); ma=assigns(mt); ca=assigns(ct)
actual={
 'DECL_SHA':'7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0',
 'SEAL_SHA':'ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed',
 'RUN_SHA':'709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27',
 'PREP_SHA':'0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'}
expected=dict(actual,DRAFT_STATUS='READY_REVIEWED_TRIM_V9_STANDALONE_INPUT_ONLY')
assert set(ma)==set(ca)
changed=[k for k in ma if ast.dump(ma[k],include_attributes=False)!=ast.dump(ca[k],include_attributes=False)]
assert set(changed)==set(expected) and len(changed)==5
inverse=candidate
changes=[]
for key,value in expected.items():
 assert ast.literal_eval(ca[key].value)==value
 if key!='DRAFT_STATUS':assert ast.literal_eval(ma[key].value) is None
 old=ast.get_source_segment(mother,ma[key]); new=ast.get_source_segment(candidate,ca[key])
 assert inverse.count(new)==1
 inverse=inverse.replace(new,old,1)
 changes.append(dict(name=key,mother=old,candidate=new))
assert inverse.encode()==mother.encode()
normalized=copy.deepcopy(ct)
for n in normalized.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in expected:
  n.value=copy.deepcopy(ma[n.targets[0].id].value)
assert ast.dump(normalized,include_attributes=False)==ast.dump(mt,include_attributes=False)
assert not any(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) for n in ct.body)
command=ca['command'].value
assert isinstance(command,ast.List) and len(command.elts)==9
assert ast.unparse(command)=="[PYTHON, str(FACTORY), 'admit', '--sha256', SEAL_SHA, '--terminal-evidence', str(TERM / 'terminal_return.json'), '--terminal-evidence-sha256', RUN_SHA]"
for needle in [
 "runner.execute(BASE/'intake','admit',command,600)",
 "runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)",
 "full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)",
 "type(watch['returncode'])is not int or watch['returncode']!=0",
 "not 0<=watch['sampled_peak_rss_mib']<512", "not elapsed<1800",
 "sys.flags.optimize!=0", "os.environ.get('PYTHONOPTIMIZE')", "sys.dont_write_bytecode=True",
 "body=f.read(log)", "child_stderr_combined_into_actual_log=True,separate_child_stderr_observation_claimed=False",
 "threads=1,children_at_once=1,retries=0", "f.absent(BASE)"]:
 assert needle in candidate,needle
assert candidate.count('runner.execute(')==1

factory=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
fr=read(factory,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46').decode()
ft=ast.parse(fr)
assert len([n for n in ft.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))])==65
main=next(n for n in ft.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'")
admission_calls=[n for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='production_admission']
assert len(admission_calls)==1 and len(admission_calls[0].args)==3 and not admission_calls[0].keywords

witnesses={'DECL_SHA':O/'declaration.json','SEAL_SHA':O/'seal.json','RUN_SHA':T/'terminal_return.json','PREP_SHA':T/'declaration_terminal_return.json'}
wd={k:meta(p,actual[k]) for k,p in witnesses.items()}
for k in ('RUN_SHA','PREP_SHA'):
 assert type(wd[k]['returncode']) is int and wd[k]['returncode']==0
 assert wd[k]['actual_tool_terminal_return_observed'] is True
 assert wd[k]['record_written_after_actual_terminal_return'] is True
runobs=meta(R/'run_terminal_tool_return.json','40ed15561767b5352e64ec45ecdc7f6110bef46335e1523d6dbfe6d3cb810bc3')
assert type(runobs['exit_code']) is int and runobs['exit_code']==0 and runobs['closed'] is True
assert (runobs['initial_chunk_id'],runobs['session_id'],runobs['terminal_chunk_id'])==('bace6e',37772,'d425ef')
ad=meta(R/'Root_actual_full_RUN_independent_admission.json','544cea19378f91f4d42c248e06f285f4f033246bfd8cac8e74827fbb1c8aeeed')
assert ad['status']=='FULL_ACTUAL_RUN_SOURCE_AND_COMPLETE_GRAPH_INDEPENDENT_PASS_ADMITTED_FOR_BOUND_INPUT_HOST_SOURCE_ONLY'
assert ad['actual_INPUT_started'] is False and ad['cold_RSS_native_or_science_credit'] is False
assert ad['bindings']==dict(declaration_sha256=actual['DECL_SHA'],PREP_sha256=actual['PREP_SHA'],terminal_sha256=actual['RUN_SHA'],seal_sha256=actual['SEAL_SHA'])
copied={}
for row in ad['copied_review_files']:
 raw=read(Path(row['path']),row['sha256']); copied[Path(row['path']).name]=raw
joint=json.loads(copied['combined_source_and_graph_actual_SCOPE_binding.json'])
assert joint['status']=='PASS' and joint['actualRoot']==dict(initial_chunk_id='bace6e',session_id=37772,terminal_chunk_id='d425ef',exit_code=0,closed=True)
assert joint['independent_SOURCE11_PREP4_OUT22_5watch_rawbinary4tails_PASS'] is True
assert joint['independent_complete35647canon35GB235528rows86ns186aliases445absence231resources_PASS'] is True
assert joint['native_transport_fullFLU_AAA_ABA_or_combined_transport_RSS_credit'] is False
assert json.loads(copied['REPORT.json'])['status']=='PASS'
assert json.loads(copied['complete_graph_actual_RUN_review.json'])['status']=='PASS'

handoff=meta(D/'STOPPED_handoff.json')
assert handoff['status']=='STOPPED_SOURCE_ONLY_UNREADY'
assert all(v is None for v in handoff['actual_bindings'].values())
future=[handoff[k] for k in ('intake_WORK','durable_evidence_family','planned_host_stdout','planned_host_stderr')]
assert len(set(future))==4 and all(not os.path.lexists(p) for p in future)
recorder=read(D/'axmat_trim_v9_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py','dfa00040ac8440744c3301f9b5c6a1959d3f14ad3bafdd2b95e735a351bffd67').decode()
ra=assigns(ast.parse(recorder))
assert ast.literal_eval(ra['DRAFT_STATUS'].value)=='UNREADY_ACTUAL_HOST_COMPONENT_AND_ROOT_BINDINGS_PENDING'
assert ast.literal_eval(ra['HOST_SHA'].value)=='9c1676f346d118b0d9fad344cde6b5c40705b681a7e971b703c8cefa8f688627'
for k in ('DECL_SHA','SEAL_SHA','RUN_SHA','PREP_SHA','API_RETURN_SHA'):assert ast.literal_eval(ra[k].value) is None
assert all(not os.path.lexists(p) for p in future)
assert all(ident(Path(p['path']))==p['identity'] for p in PINS)
report=dict(
 schema='AXMAT_V9_BOUND_INPUT_HOST_FINAL_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS',
 scope='Only final bound host source admission; actual host/API outcome remains unknown.',
 host_sha256='180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae',
 mother_sha256='9c1676f346d118b0d9fad344cde6b5c40705b681a7e971b703c8cefa8f688627',
 complete_five_assignment_inverse_exact=True,full_AST_except_five_assignments_exact=True,
 all_other_source_bytes_guards_MRO_whole_INPUT_resource_scope_unchanged=True,changes=changes,
 command_nine_tokens_standard_three_arg_API=True,execute_call_count=1,
 caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,RSS_mib=512,threads=1,children_at_once=1,retries=0,archive_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592),
 factory_sha256='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46',factory_all65_functions_retained=True,
 actual_component_witnesses=actual,actual_full_RUN_joint_review_status='PASS',
 Root_actual_full_RUN_admission_sha256='544cea19378f91f4d42c248e06f285f4f033246bfd8cac8e74827fbb1c8aeeed',
 Root_RUN_actual_tool=dict(initial_chunk_id='bace6e',session_id=37772,terminal_chunk_id='d425ef',exit_code=0,closed=True),
 four_future_outputs_absent=future,recorder_still_UNREADY_and_all5_actual_SHA_None=True,
 recorder_HOST_SHA_still_mother_and_requires_future_finalhost_binding=True,
 actual_host_exit=None,actual_API_return_sha256=None,actual_host_tool_handle=None,
 host_or_API_or_business_module_constructor_executed=False,formal_or_ART_written=False,
 cold_native_fullFLU_AAA_ABA_or_combined_transport_RSS_credit=False,
 whole_graph_35GB_not_reread_in_this_source_scope=True,
 whole_graph_actual_prior_independent_PASS_fresh_bound=True,
 raw_read_pin_count=len(PINS),fresh_pins=PINS,
 observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
rp=HERE/'REPORT.json'
with rp.open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',report=str(rp),report_sha256=hashlib.sha256(rp.read_bytes()).hexdigest(),pin_count=len(PINS),source_only=True),ensure_ascii=False),flush=True)

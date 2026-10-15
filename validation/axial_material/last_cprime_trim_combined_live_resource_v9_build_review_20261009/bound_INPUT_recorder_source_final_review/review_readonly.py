import ast,copy,hashlib,json,math,os,stat
from pathlib import Path
H=Path(__file__).resolve().parent;A=Path('/Users/wen/spot/validation/axial_material');B=Path('/Users/wen/spot/validation/artifacts')
NAME='axmat_trim_v9_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py'
D=Path('/private/tmp/axmat-trim-v9-bounded-runtime-input-intake-source-draft-20261009')/NAME
C=Path('/private/tmp/axmat-trim-v9-bounded-runtime-input-intake-postterminal-bound-candidate-20261009')/NAME
HOST=Path('/private/tmp/axmat-trim-v9-bounded-runtime-input-intake-bound-candidate-20261009/axmat_trim_v9_standalone_bounded_runtime_api_intake_host_20261009.py')
BASE=Path('/private/tmp/axmat-trim-v9-standalone-bounded-runtime-api-intake-20261009')
OUT=B/'axial-material-owned-specs-trim-v9-standalone-bounded-runtime-api-intake-evidence-20261009'
PINS=[]
def ident(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and p.resolve(strict=True)==p
 return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,sha=None):
 before=ident(p);v=p.read_bytes();h=hashlib.sha256(v).hexdigest();assert before==ident(p)
 if sha:assert h==sha,(str(p),h,sha)
 PINS.append(dict(path=str(p),sha256=h,bytes=len(v),identity=before));return v
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def reject(s):raise ValueError(s)
def floating(s):
 v=float(s)
 if not math.isfinite(v):raise ValueError('nonfinite JSON')
 return v
def obj(p,sha=None):return json.loads(raw(p,sha),object_pairs_hook=pairs,parse_constant=reject,parse_float=floating)
def assignments(t):return {n.targets[0].id:n for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
mother=raw(D,'dfa00040ac8440744c3301f9b5c6a1959d3f14ad3bafdd2b95e735a351bffd67').decode()
candidate=raw(C,'5bd181e59b3229398ec7725e8513da5cf055791400522935f5ebfc2b9bd0d03e').decode()
mt=ast.parse(mother);ct=ast.parse(candidate);ma=assignments(mt);ca=assignments(ct)
expected=dict(DRAFT_STATUS='READY_REVIEWED_ROOT_POSTTERMINAL_INTAKE_RECORD_ONLY',HOST=str(HOST),HOST_SHA='180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae',
 DECL_SHA='7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0',SEAL_SHA='ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed',RUN_SHA='709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27',PREP_SHA='0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb',API_RETURN_SHA='0e5727aee267c24c3a74c387c628b3633a23826e38c41eda1bfe14ecd02872f5')
changed=[k for k in ma if ast.dump(ma[k],include_attributes=False)!=ast.dump(ca[k],include_attributes=False)]
assert set(changed)==set(expected)and len(changed)==8
inverse=candidate;norm=copy.deepcopy(ct)
for key,val in expected.items():
 v=ca[key].value
 if key=='HOST':assert isinstance(v,ast.Call)and ast.unparse(v.func)=='Path'and len(v.args)==1 and ast.literal_eval(v.args[0])==val
 else:assert ast.literal_eval(v)==val
 old=ast.get_source_segment(mother,ma[key]);new=ast.get_source_segment(candidate,ca[key]);assert inverse.count(new)==1;inverse=inverse.replace(new,old,1)
for n in norm.body:
 if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in expected:n.value=copy.deepcopy(ma[n.targets[0].id].value)
assert inverse.encode()==mother.encode()and ast.dump(norm,include_attributes=False)==ast.dump(mt,include_attributes=False)
helper=Path('/private/tmp/axmat_root_historical_owned_specs_combined_runtime_actual_bound_recorder_20261007.py');hr=raw(helper,'0b8a9a0a3b71bdea15269a14e54011d142e00c92979fbedef8ade3bcac7ec047').decode();ast.parse(hr)
assert not any(s in hr for s in ('subprocess','os.system(','.exec_module(','ctypes','production_admission('))
raw(HOST,expected['HOST_SHA'])
root=obj(A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009/Root_actual_bound_INPUT_host_tool_return.json','ed535093a16ab98a897bc3b895189a99a9eff4cb07165ea69d7f720b374a7434')
assert root['actual_tool']==dict(initial_chunk_id='0a5d42',session_id=11005,terminal_chunk_id='cbbfbe',exit_code=0,closed=True)
assert type(root['actual_tool']['exit_code'])is int and root['actual_tool_terminal_return_observed']is True and root['written_after_actual_tool_return']is True
x=obj(BASE/'result.json',root['actual_host_result_sha256']);stdout=Path('/private/tmp/axmat-trim-v9-standalone-bounded-runtime-api-intake-host-20261009.stdout');stderr=stdout.with_suffix('.stderr')
assert obj(stdout,root['actual_host_stdout_sha256'])==x;assert len(raw(stderr,root['actual_host_stderr_sha256']))==0
log=BASE/'intake/admit.log';assert len(raw(log,expected['API_RETURN_SHA']))==root['whole_API_merged_stream_bytes']==25266286
w=obj(BASE/'intake/admit.watchdog.json');st=obj(BASE/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json');assert set(st)=={'stages'}and len(st['stages'])==1
assert x['stage_records']==st['stages']and x['watchdog']==w and st['stages'][0]['status']=='PASS'
assert st['stages'][0]['log_sha256']==expected['API_RETURN_SHA']and x['actual_command']==st['stages'][0]['command']==w['command']==root['host_result_summary']['actual_command']and len(x['actual_command'])==9
assert type(w['pid'])is int and w['pid']==20473 and type(w['returncode'])is int and w['returncode']==0
assert w['sampled_peak_rss_mib']==497.84375 and w['elapsed_seconds']==43.68955924996408 and w['elapsed_seconds']<600
assert w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True
assert x['whole_elapsed_seconds']==49.04454591701506 and x['whole_elapsed_seconds']<1800
assert tuple(x[k]for k in ('total_wall_cap_seconds','stage_wall_cap_seconds','RSS_cap_mib','threads','children_at_once','retries'))==(1800,600,512,1,1,0)
false=('cold_controller_imported','cold_controller_bound','cold_prepared','physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
assert all(x[k]is False for k in false)
assert x['child_stderr_combined_into_actual_log']is True and x['separate_child_stderr_observation_claimed']is False
for key in ('producer','declaration','build_seal','actual_run','actual_PREP','actual_API_whole_merged_stream','actual_API_whole_return','supervisor_source','parent_source','bounded_helper'):raw(Path(x[key]['path']),x[key]['sha256'])
assert [x[k]['sha256']for k in ('declaration','build_seal','actual_run','actual_PREP')]==[expected[k]for k in ('DECL_SHA','SEAL_SHA','RUN_SHA','PREP_SHA')]
assert x['producer']['sha256']=='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
assert not os.path.lexists(OUT);assert all(ident(Path(p['path']))==p['identity']for p in PINS)
payload=ca['payload'].value;assert isinstance(payload,ast.Dict)and len(payload.keys)==9
names=[ast.literal_eval(n)for n in payload.keys]
assert names==['host.py','postterminal_recorder.py','host.stdout','host.stderr','result.json','runtime/run_bounded_dragon.py','intake/admit.log','intake/admit.watchdog.json','STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json']
assert "r.write(OUT/'Root_terminal_return.json',receipt)"in candidate and "inv,size=r.inventory(OUT)"in candidate
report=dict(status='PASS',schema='AXMAT_V9_TRUE_HOST_BOUND_POSTTERMINAL_RECORDER_SOURCE_INDEPENDENT_REVIEW_V1',scope='Only successful postterminal recorder source admission backed by real completed host; not durable payload or full INPUT semantic postreview yet.',
 recorder_sha256='5bd181e59b3229398ec7725e8513da5cf055791400522935f5ebfc2b9bd0d03e',mother_recorder_sha256='dfa00040ac8440744c3301f9b5c6a1959d3f14ad3bafdd2b95e735a351bffd67',complete_eight_assignment_inverse_wholebyte_exact=True,all_other_AST_guards_payload_caps_scope_same=True,bound_assignments=expected,pure_helper_sha256='0b8a9a0a3b71bdea15269a14e54011d142e00c92979fbedef8ade3bcac7ec047',
 actual_Root_host_tool=root['actual_tool'],actual_Root_host_observation_sha256='ed535093a16ab98a897bc3b895189a99a9eff4cb07165ea69d7f720b374a7434',host_whole_seconds=x['whole_elapsed_seconds'],child_PID=w['pid'],child_returncode=0,child_elapsed_seconds=w['elapsed_seconds'],child_sampled_peak_RSS_mib=w['sampled_peak_rss_mib'],one_original_PASS_stage=True,whole_merged_API_log_bytes=25266286,whole_merged_API_log_sha256=expected['API_RETURN_SHA'],host_stderr_truly_empty=True,separate_child_stderr_claimed=False,
 caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,RSS_mib=512,threads=1,children_at_once=1,retries=0),exact_nine_future_payload_names=names,independent_tenth_Root_receipt_retained=True,future_ART_family_absent=True,
 actual_recorder_execution=None,actual_durable_Root_receipt_sha256=None,actual_whole65_API_semantic_postreview=None,target_recorder_helper_host_API_or_business_executed_by_reviewer=False,formal_ART_written=False,new_cold_native_fullFLU_AAA_ABA_or_combined_native_RSS_credit=False,
 fresh_source_context_pins=PINS,limits=['Complete actual API log was fullSHA/read as raw bytes here, not semantically audited. Entire65fields/fullseven/fulltrim semantics wait for genuine recorder0 and durable9+1 payload.','Child peak is sampled ownPID ps RSS, not exact continuous or whole host peak.','Pure helper source inspected/AST parsed only, never imported or called.','Root external actual tool0 remains authoritative; JSON/PASS logs alone would not establish successful host exit.'])
rp=H/'source_review.json'
with rp.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',report=str(rp),sha256=hashlib.sha256(rp.read_bytes()).hexdigest(),source_only=True,actual_recorder_executed=False)),flush=True)

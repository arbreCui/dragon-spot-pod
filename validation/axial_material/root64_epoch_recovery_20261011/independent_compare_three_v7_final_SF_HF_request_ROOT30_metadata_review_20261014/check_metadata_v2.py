from pathlib import Path
import hashlib,importlib.util,json,os,shlex,stat,sys
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts'
P=R/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014';D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<=64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes']
def tool0(t,p):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
def terminal0(t):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_terminal_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None;return z
def union(rows):
 out=[]
 for row in rows:
  if row not in out:out.append(row)
 return out
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
sp=pin(P/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json');hp=pin(P/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json');dp=pin(P/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json');sf=load(sp);hf=load(hp);dyn=load(dp)
assert sp['sha256'].startswith('7f0fcf73')and sp['size_bytes']==2602057 and hp['sha256'].startswith('62898dba')and hp['size_bytes']==2590872 and dp['sha256'].startswith('f1bf731e')and dp['size_bytes']==4166
ap=pin(R/'ROOT_EXACT_COMPARE_THREE_V7_ACTUAL30_ARGV_20261014.json');args=load(ap);rp=args['actual_request_pin'];request=load(rp)
assert rp['sha256'].startswith('a4034e14')and rp['size_bytes']==2591910 and len(args['argv'])==30 and args['argv'][:24]==dyn['known_argv_prefix']and args['published_dynamic_interface_pin']==dyn
assert shlex.split(args['shell_safe_command'])==args['argv']and args['argv'][24:]==['--request-summary',rp['path'],'--request-sha256',rp['sha256'],'--request-seven-id',json.dumps(rp['identity'],separators=(',',':'))]
assert dyn['selected_source_freeze_pin']==sp and dyn['selected_host_freeze_pin']==hp and dyn['host_source_pin']==hf['host_source']and dyn['actual_request_pin']is None and dyn['is_complete_executable_argv']is False
assert request['schema']=='CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'and request['operation']=='compare-three'and request['complete_source_freeze_pin']==sp and request['request_preparation_only']is True and request['actual_stage_executed']is False
pp=pin(R/'ROOT_ACTUAL_COMPARE_THREE_V7_SOURCE_ONCE_PUBLICATION_TRUE_TOOL_RETURNS_20261014.json');pub=load(pp);pz=terminal0(pub);pout=json.loads(pz['output']);assert pout['Source_freeze_pin']==sp and pout['Host_freeze_pin']==hp and pout['dynamic_interface_pin']==dp
qp=pin(R/'ROOT_ACTUAL_COMPARE_THREE_V7_REQUEST25_TRUE_TOOL_RETURNS_20261014.json');qt=load(qp);qz=terminal0(qt);assert qt['actual_initial_return']['session_id']==3526 and qz['chunk_id']=='5a1c23'and json.loads(qz['output'])['request']==rp
qap=pin(R/'ROOT_EXACT_COMPARE_THREE_V7_REQUEST25_ARGV_20261014.json');qa=load(qap);assert shlex.split(qt['exact_executed_command'])==qa['argv']and len(qa['argv'])==25
sourceD=R/'independent_compare_three_v7_candidate_writer_Source_review_20261014';sreviewp=pin(sourceD/'REVIEW.json');stoolp=pin(sourceD/'TRUE_TOOL_RETURNS.json');sreview=load(sreviewp);tool0(load(stoolp),sreviewp)
assert sreview['failure']is None and sreview['Source_candidate_PASS']is True and sf['same_round_independent_Source_review_pin']==sreviewp and sf['same_round_independent_Source_tools_pin']==stoolp
ready=load(P/'SOURCE_REVIEW_READY.json');plan=load(ready['plan_pin']);assert sf['control_plan_pin']==ready['plan_pin']and sf['complete_source_file_pins']==plan['complete_source_file_pins_candidate']and len(sf['complete_source_file_pins'])==13
for p in sf['complete_source_file_pins']:assert pin(p['path'])==p
assert hf['host_source']==ready['host_source_pin']==dyn['host_source_pin']and len(hf['dependencies'])==6048
assert sf['candidate_executed']is False and hf['candidate_executed']is False and sf['physics_qualified']is False and hf['physics_qualified']is False
current={}
for p in hf['dependencies']+sf['complete_source_file_pins']+request['complete_input_pins']+[sp,hp,dp,rp,ap,pp,qp,qap,sreviewp,stoolp]:
 assert p['path']not in current or current[p['path']]==p;current[p['path']]=p;seven(p)
assert len(request['complete_input_pins'])==len({p['path']for p in request['complete_input_pins']})==6026 and sp in request['complete_input_pins']
assert len(request['actual_native_producers'])==3 and [x['plane']for x in request['actual_native_producers']]==[1,2,3]and all(type(x['plane'])is int for x in request['actual_native_producers'])
for p in plan['projection_current_live_pins']+plan['retained_actual_GENDF_current_dependency_pins']:assert current[p['path']]==p
assert request['explicit_cumulative_metadata_file_pins']==sf['retained_actual_GENDF_explicit_metadata_file_pins']==sreview['explicit_external_metadata_file_pins']and len(request['explicit_cumulative_metadata_file_pins'])==4
assert request['retained_actual_GENDF_resource_authority_pins']==sf['retained_actual_GENDF_resource_authority_pins']
out=Path(request['owning_host_output_directory']);childout=Path(request['output_directory']);reqroot=Path(rp['path']).parent
assert out.parent==ART and childout==out.with_name(out.name+'-evidence')and not os.path.lexists(out)and not os.path.lexists(childout)
sub={plan['planned_actual_output_root']:str(out),plan['planned_actual_output_root']+'-evidence':str(childout),plan['planned_actual_request_root']:str(reqroot)}
expected=[sub.get(x,x)for x in plan['planned_complete_cumulative_compare_roots']];roots=request['joint_archive_roots'];assert roots==expected and len(roots)==len(set(roots))==25
assert request['original_compare_sixteen_role_roots']==[sub.get(x,x)for x in plan['original_compare_sixteen_root_projection']]and request['original_five_role_roots']==roots[:5]
assert union(request['original_compare_sixteen_role_roots']+sf['retained_actual_GENDF_and_control_joint_roots'])==roots
assert not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2**31,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0);assert request['original_caps']==caps
for k,v in request.items():
 if k.endswith('_qualified')or k in ['historical_native_RAM_bits_verified','original_XSM_memory_bits_verified','historical_unsaved_context_recovered','ABA_admitted','goal_complete']:assert v is False
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
commonpin=next(p for p in sf['complete_source_file_pins']if Path(p['path']).name=='guarded_warm_A_common.py');common=module(Path(commonpin['path']),'compare25_review_current_common')
support=module(common.SUPPORT,'compare25_review_original_support');assert pin(common.SUPPORT)['sha256']==common.SUPPORT_SHA
helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'compare25_review_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'compare25_review_original_factory');full,production=helper.modules()
assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
history=factory.DynamicHistoryResources(ART,factory.history_roots([str(out)],ART),8*2**30,96*2**30,production.ResourceFailure).check()
fresh=production.DiskResources(ROOT/'validation',roots,8*2**30,2**31).check()
extras=request['explicit_cumulative_metadata_file_pins'];external=0;nodes=set()
for p in extras:
 s=Path(p['path']).lstat();assert s.st_uid==os.getuid()and s.st_nlink==1 and not any(a.is_symlink()for a in(Path(p['path']),*Path(p['path']).parents));seven(p)
 assert(s.st_dev,s.st_ino)not in nodes;nodes.add((s.st_dev,s.st_ino))
 if not any(Path(p['path']).is_relative_to(Path(x))for x in roots):external+=s.st_size
assert external==22676 and fresh['artifact_bytes']+external<2**31 and fresh['resource_roots']==roots
margin=96*2**30-history['artifact_bytes']-20971764748-64*2**20-2**31
assert margin>0 and fresh['disk_free_bytes']-20971764748-2**31>=8*2**30
for p in current.values():seven(p)
assert not os.path.lexists(out)and not os.path.lexists(childout)
result=dict(schema='INDEPENDENT_COMPARE_THREE_V7_FINAL_SF_HF_REQUEST_ROOT30_METADATA_REVIEW_V1',status='PASS_COMPARE_THREE_V7_FINAL_METADATA_READY_FOR_UNIQUE_RUNTIME',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,actual_Source_freeze_pin=sp,actual_Host_freeze_pin=hp,actual_dynamic_interface_pin=dp,actual_request_pin=rp,actual_Root_argv_pin=ap,actual_Source_publication_true_tool_pin=pp,actual_request_preparation_true_tool_pin=qp,actual_request_preparation_argv_pin=qap,actual_same_round_Source_review_pin=sreviewp,actual_same_round_Source_tools_pin=stoolp,reviewer_source_pin=pin(__file__),actual_source_count=13,actual_HF_dependency_count=6048,actual_request_input_count=6026,actual_distinct_current_pin_count=len(current),all_current7_verified_twice=True,all13_bounded_selected_Source_complete_EOF_SHA_verified=True,actual_three_plane_producer_count=3,actual_root_argv_count=30,actual_request_preparation_argv_count=25,actual_dynamic_prefix_count=24,actual_runtime_request_Source_freeze_bound=True,actual_cumulative_joint_root_count=25,actual_cumulative_joint_roots=roots,explicit_external_metadata_file_pins=extras,actual_external_metadata_bytes=external,original_caps=caps,actual_current_original_factory_metadata=dict(history=history,joint_fresh=fresh,complete_joint_roots_plus_metadata_bytes=fresh['artifact_bytes']+external,fullfresh2_cold_metadata_history_reserve_margin_bytes=margin,fullfresh2_reserve_admitted=True),original_fullfresh2_cold_meta_history96_free8_gate_current=True,actual_output_pair_absent=True,old_scientific_or_three_archive_body_EOF_repeated=False,original_native_tree_decode_performed=False,actual_compare_three_runtime_return=None,actual_compare_three_report_pin=None)
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),actual_distinct_current_pin_count=len(current),actual_joint25_plus_external4_bytes=fresh['artifact_bytes']+external,actual_fullfresh2_reserve_margin_bytes=margin)),flush=True)

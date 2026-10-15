from pathlib import Path
import ast,hashlib,json,os,stat
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');S=REC/'current_formal_material_authority_exact_cache70_source_v7';OLD=REC/'current_formal_material_authority_exact_cache70_source_v6';D=REC/'material_exact_cache70_v7_author_finite_source_review_20261013'
def pin(p):
 p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert stat.S_ISREG(s.st_mode)and i[0]==16777229
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
  f=os.fstat(fd);assert[f.st_dev,f.st_ino,f.st_mode,f.st_nlink,f.st_size,f.st_mtime_ns,f.st_ctime_ns]==i
 finally:os.close(fd)
 t=p.lstat();assert[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==i and n==i[4]
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i)
def read(n):return json.loads((S/n).read_bytes())
draft=read('UNFROZEN_PRECISE_V7_CURRENT_V11_SOURCE_REBIND_DRAFT.json')
for p in draft['old_v6_complete_regular_Source_tree_fullpins']:assert pin(p['path'])==p
deltas=[]
for p in sorted(OLD.glob('*.py')):
 a=p.read_bytes();b=(S/p.name).read_bytes();ast.parse(a);ast.parse(b)
 if p.name=='build_current_observation_runtime.py':x=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v6'";z=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v7'"
 elif p.name=='current_material_prerequisite_admission.py':x=b'actual prerequisite must consume exact frozen v10 host Source';z=b'actual prerequisite must consume exact frozen v11 host Source'
 else:assert a==b;continue
 assert a.count(x)==b.count(z)==1 and a.replace(x,z)==b and b.replace(z,x)==a
 deltas.append(dict(name=p.name,old_fullpin=pin(p),new_fullpin=pin(S/p.name),old_literal=x.decode(),new_literal=z.decode(),full_forward_and_reverse_byte_equal=True))
assert len(deltas)==2
oldmath=json.loads((OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json').read_bytes());math=read('COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json');hf=read('COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json');phf=read('COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json');cli=read('ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json');inv=read('COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json')
assert math['original_caps']==oldmath['original_caps']==hf['original_caps']
oldhf=json.loads((OLD/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json').read_bytes());assert hf['selected_actual_build70_report']==oldhf['selected_actual_build70_report']and hf['required_actual_saved_audit_host_freeze_pin']==oldhf['required_actual_saved_audit_host_freeze_pin']and hf['required_actual_saved_audit_output_directory']==oldhf['required_actual_saved_audit_output_directory']
assert hf['required_actual_AAA3_host_freeze_pin']==pin(REC/'aaa_three_plane_streaming_pipeline_source_v11/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
assert hf['required_actual_AAA3_output_directory']=='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11'
assert hf['required_future_receipt_arguments']==oldhf['required_future_receipt_arguments']and cli['is_complete_executable_argv']is False and phf['future_actual75_report_not_predicted_or_pinned']is True
oldinv=json.loads((OLD/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json').read_bytes());assert inv['complete70_order']==oldinv['complete70_order']and len(inv['complete75_order'])==75
assert [p for p in inv['complete75_order']if p not in inv['observer_objects']]==inv['complete70_order']
assert len(inv['entire_byte_copy_pins'])==18
for row in inv['entire_byte_copy_pins']:
 assert pin(row['original']['path'])==row['original']and pin(row['copy']['path'])==row['copy'];assert Path(row['original']['path']).read_bytes()==Path(row['copy']['path']).read_bytes()
names=['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json','COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json','ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json','COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json','EXACT_V6_TO_V7_CURRENT_V11_SOURCE_BINDING_BYTE_DELTA.json','PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_ADMISSION.json']
report=dict(schema='FINAL_FROZEN_MATERIAL_CURRENT70_OBSERVER75_V7_SOURCE_AND_AUTHOR_REVIEW_HANDOFF_V1',status='FROZEN_SOURCE_ONLY_AUTHOR_REVIEW_PASS_PENDING_INDEPENDENT_REVIEW',Source_namespace=str(S),Source_writes_stopped=True,frozen_all_regular_Source_tree_fullpins=[pin(p)for p in sorted(S.rglob('*'))if p.is_file()],key_Source_SF_HF_CLI_inverse_fullpins=[pin(S/n)for n in names],exact_two_Source_delta_fullpins=deltas,immutable_v6_complete_tree_fullpins=draft['old_v6_complete_regular_Source_tree_fullpins'],all_author_evidence_pins=[pin(p)for p in sorted(D.iterdir())if p.is_file()],selected_real_v11_HF_pin=hf['required_actual_AAA3_host_freeze_pin'],required_actual_AAA3_output_directory=hf['required_actual_AAA3_output_directory'],future_actual_receipts_not_predicted=True,incomplete_until_Root_supplies_genuine_completed_AAA3_and_saved_receipts=True,observer75_report_is_dynamic_required_parameter=True,full70_to75_order_unchanged=True,complete18math_byte_equal=True,original_caps=hf['original_caps'],candidate_imported=False,compiler_or_material_or_science_business_started=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with(D/'FINAL_FROZEN_SOURCE_AND_AUTHOR_REVIEW_HANDOFF.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],complete_frozen_Source_regular_files=len(report['frozen_all_regular_Source_tree_fullpins']),handoff_pin=pin(D/'FINAL_FROZEN_SOURCE_AND_AUTHOR_REVIEW_HANDOFF.json'),key_fullpins=report['key_Source_SF_HF_CLI_inverse_fullpins'])))

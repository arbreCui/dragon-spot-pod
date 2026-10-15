import ast
import difflib
import hashlib
import json
import os
import stat
from pathlib import Path

D=Path('/private/tmp/axmat_v11_combined_actual_component_pins_unready_source_draft_20261009')
BASE=Path('/private/tmp/axmat_v11_combined_component_contract_source_draft_20261009')
NAME='prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.UNREADY.py'
ART=Path('/Users/wen/spot/validation/artifacts')
SOURCE=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'
OUT=ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
TERM=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009'
EXPECTED={
 'TRIM_DECL_SHA':(OUT/'declaration.json','2e5c1cda328ee1be5484e756e01337d134a956ae9e6d8623215f49f75e9b42ee'),
 'TRIM_SEAL_SHA':(OUT/'seal.json','5517c1ada26e43ba55683092baf8f63f8676eeff58ee907cd03560047c7a0b19'),
 'TRIM_TERMINAL_SHA':(TERM/'terminal_return.json','26ef721c5b76af13036e6a486468f40d7362b584485c20a8713da82a23a9f430'),
 'TRIM_SOURCE_ADMISSION_SHA':(SOURCE/'source_admission.json','a065b026e1e03b2523c945e8b7a6fd508debbea7489fc2707606c3954bb0c1e8'),
 'TRIM_OBJECT_SHA':(OUT/'build/SPOT1P64.o','271bd5f7d768b3380b8d976c177a468cd038faee81ba156f49969bfb8c061131'),
 'TRIM_RUNTIME_SHA':(OUT/'runtime/Dragon','05765aeb40f494e9502c0278bfc652c243f8970c31256d11abec5789de7df79b'),
}
def sha(b):return hashlib.sha256(b).hexdigest()
def idstat(s):return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def fresh(p):
 for a in [*reversed(p.parents),p]:
  st=a.lstat();assert not stat.S_ISLNK(st.st_mode),str(a)
  if a!=p:assert stat.S_ISDIR(st.st_mode),str(a)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  first=os.fstat(fd);assert stat.S_ISREG(first.st_mode);h=hashlib.sha256();parts=[]
  while raw:=os.read(fd,1024*1024):h.update(raw);parts.append(raw)
  last=os.fstat(fd);assert idstat(first)==idstat(last)==idstat(p.lstat())
  raw=b''.join(parts);assert len(raw)==first.st_size
  return raw,dict(path=str(p),sha256=h.hexdigest(),identity=idstat(last))
 finally:os.close(fd)
pins={};data={}
for slot,(path,wanted) in EXPECTED.items():
 raw,p=fresh(path);assert wanted is None or p['sha256']==wanted
 pins[slot]=p;data[slot]=raw
decl=json.loads(data['TRIM_DECL_SHA']);seal=json.loads(data['TRIM_SEAL_SHA']);term=json.loads(data['TRIM_TERMINAL_SHA'])
assert decl['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_DECLARATION_V1'
assert decl['family']=='RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11'
assert decl['source_root']==str(SOURCE)
assert seal['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1'
assert seal['files']['declaration.json']==pins['TRIM_DECL_SHA']['sha256']
assert seal['files']['build/SPOT1P64.o']==pins['TRIM_OBJECT_SHA']['sha256']
assert seal['files']['runtime/Dragon']==pins['TRIM_RUNTIME_SHA']['sha256']
assert decl['source_inventory']['files']['source_admission.json']==pins['TRIM_SOURCE_ADMISSION_SHA']['sha256']
assert decl['files'][str(SOURCE/'source_admission.json')]==pins['TRIM_SOURCE_ADMISSION_SHA']['sha256']
assert term['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
assert term['record_producer']=='root' and type(term['returncode']) is int and term['returncode']==0
assert term['actual_tool_terminal_return_observed']is True and term['record_written_after_actual_terminal_return']is True
assert term['declaration']==dict(path=str(OUT/'declaration.json'),sha256=pins['TRIM_DECL_SHA']['sha256'])
assert term['build_seal']==dict(path=str(OUT/'seal.json'),sha256=pins['TRIM_SEAL_SHA']['sha256'])
tool=term['actual_tool_provenance']['actual_terminal_return'];assert type(tool['exit_code'])is int and tool['exit_code']==0
assert term['actual_tool_provenance']['no_restart']is True
source_path=Path(term['source']['path']);raw,source_pin=fresh(source_path)
assert source_pin['sha256']==term['source']['sha256']=='f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
admission=json.loads(data['TRIM_SOURCE_ADMISSION_SHA'])
assert admission['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_SOURCE_ADMISSION_V1'
assert admission['source_patch_proof']['candidate_kernel_sha256']=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'
assert admission['source_patch_proof']['inherited_v10_complete_proof']['candidate_kernel_sha256']=='5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809'
assert admission['source_patch_proof']['inherited_v10_complete_proof']['last_cprime_trim']['candidate_kernel_sha256']=='343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1'
raw,base_pin=fresh(BASE/NAME);assert base_pin['sha256']=='45e336c9b37cbc49b0552fdb472c28eda0bca9e35d71fb429499e678953bf777'
base=raw.decode();tree=ast.parse(base);out=base;changes=[]
assigns={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
for name,pin in pins.items():
 node=assigns[name];assert ast.literal_eval(node.value)is None
 old=ast.get_source_segment(base,node);new=name+' = '+repr(pin['sha256'])
 assert out.count(old)==1;out=out.replace(old,new,1);changes.append(dict(name=name,old=old,new=new))
inverse=out
for row in reversed(changes):assert inverse.count(row['new'])==1;inverse=inverse.replace(row['new'],row['old'],1)
assert inverse==base
adapter_edits_raw,adapter_edits_pin=fresh(BASE/'adapter_region_edits.json');adapter_edits=json.loads(adapter_edits_raw);assert len(adapter_edits)==17
identity_inverse=inverse
for row in reversed(adapter_edits):
 assert identity_inverse.count(row['new'])==1;identity_inverse=identity_inverse.replace(row['new'],row['old'],1)
identity_path=Path('/private/tmp/axmat_v11_minimal_combined_cold_retarget_plan_20261009')/NAME
raw,identity_pin=fresh(identity_path);assert identity_inverse.encode()==raw and identity_pin['sha256']=='711762b183d81189f4727e237f21e4c0aff30065bf7d58b0932c504fe2f39709'
ot=ast.parse(out)
before_functions={n.name:ast.get_source_segment(base,n) for n in tree.body if isinstance(n,ast.FunctionDef)}
after_functions={n.name:ast.get_source_segment(out,n) for n in ot.body if isinstance(n,ast.FunctionDef)}
assert before_functions==after_functions and len(after_functions)==65
assert len([n for n in ast.walk(ot) if isinstance(n,ast.FunctionDef)])==70
oa={n.targets[0].id:n.value for n in ot.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
assert ast.literal_eval(oa['DRAFT_STATUS'])=='UNREADY_PENDING_ACTUAL_V11_COMPONENT_BUILD_WITNESSES_AND_SOURCE_REVIEW'
for name in ('SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY','INPUT_SPECS','INPUT_SPECS_SHA','INPUT_HELPERS'):
 assert ast.dump(assigns[name].value,include_attributes=False)==ast.dump(oa[name],include_attributes=False),name
for name,(path,expected) in EXPECTED.items():
 st=path.lstat();assert idstat(st)==pins[name]['identity']
 assert fresh(path)[1]==pins[name]
assert fresh(source_path)[1]==source_pin and fresh(BASE/NAME)[1]==base_pin
draft=D/NAME;draft.write_text(out)
(D/'actual_six_pin_region_edits.json').write_text(json.dumps(changes,indent=2)+'\n')
(D/'complete_17_plus_6_region_edits.json').write_text(json.dumps(adapter_edits+changes,indent=2)+'\n')
(D/'actual_six_pin.diff').write_text(''.join(difflib.unified_diff(base.splitlines(True),out.splitlines(True),fromfile=str(BASE/NAME),tofile=str(draft))))
proof=dict(schema='AXMAT_V11_COMBINED_ACTUAL_COMPONENT_SIX_PINS_COMPLETE_INVERSE_V1',draft_sha256=sha(out.encode()),six_pin_inverse_to_45e_byteexact=True,source_adapter_17_region_inverse_byteexact=True,all23_inverse_to_711_identity_draft_byteexact=True,component_contract_source_draft=base_pin,identity_only_draft=identity_pin,source_adapter_region_edits=adapter_edits_pin,all65_top_and70_total_function_bodies_byteexact_to_45e=True,UNREADY_status_byteexact_to_45e=True)
(D/'complete_inverse_proof.json').write_text(json.dumps(proof,indent=2)+'\n')
report=dict(schema='AXMAT_V11_COMBINED_ACTUAL_COMPONENT_PINS_SOURCE_ONLY_V1',status='UNREADY_ACTUAL_SIX_COMPONENT_PINS_ONLY',draft=dict(path=str(draft),sha256=sha(out.encode())),actual_component_pins=pins,component_factory=source_pin,component_root_true0_terminal=dict(path=str(TERM/'terminal_return.json'),sha256=pins['TRIM_TERMINAL_SHA']['sha256'],actual_terminal_tool_return=tool),source_identity_and_full_SHA_before_after_equal=True,object_runtime_pins_bound_by_actual_new_seal=True,source_admission_pin_bound_by_actual_new_declaration=True,complete_inverse=proof,source_layers=dict(current0800='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5',inherited5e='5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809',last_cprime343e='343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1'),formal_component_production_admission_independently_reviewed=None,source_admission_of_this_combined_draft_completed=None,actual_new_combined=None,actual_new_bounded_INPUT=None,actual_new_cold=None,business_imported=False,business_API_executed=False,compiled=False,project_written=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limit='Only six actual new component SHA assignments changed; still UNREADY pending Root formal admission plus complete source review. No former V10 run witnesses used, no business or combined success represented.')
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('V11组合TMP草稿仅填入6项真实新组件凭据，仍UNREADY。\n声明/封存/Root实际退出0收据按指定完整SHA鲜核；object、runtime、source_admission从真正V11路径全文读取，分别与封存和声明一致。\n六行修改完整逆回45e；此前17区域继续逆回711身份草稿，合计23区域。\n65顶层/70全部函数、whole INPUT、物理、预算、真实类/MRO完全不变。\n正式组件admit完成状态仍None；新combined/INPUT/cold成功全None，不能执行本草稿。\n')
print(json.dumps(dict(status=report['status'],draft_sha256=sha(out.encode()),report_sha256=sha((D/'REPORT.json').read_bytes()),actual_six_component_SHA={name:pin['sha256'] for name,pin in pins.items()},inverse_regions=23)))

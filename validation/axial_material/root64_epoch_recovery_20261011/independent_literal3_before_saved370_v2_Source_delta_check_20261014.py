import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'storage_release_literal3_before_saved370_old_pack_and_macro_source_v2_20261014'
D=R/'independent_literal3_before_saved370_v2_Source_delta_review_20261014'
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_size<=64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert identity(os.fstat(f.fileno()))==identity(s);x=f.read();assert identity(os.fstat(f.fileno()))==identity(s)
 assert identity(p.lstat())==identity(s)
 return dict(path=str(p),sha256=hashlib.sha256(x).hexdigest(),size_bytes=len(x),identity=identity(s))
def exact(p):assert pin(p['path'])==p;return Path(p['path']).read_bytes()
def read(p):return json.loads(exact(p))
def functions(x):
 t=x.decode();return {n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
def inverse_check(i):
 result=[]
 for e in i['entries']:
  old=exact(e['predecessor_pin']);new=exact(e['candidate_pin']);x=new.decode()
  for c in reversed(e['changes']):assert x.count(c['after'])==1;x=x.replace(c['after'],c['before'],1)
  assert x.encode()==old;ast.parse(new);result.append(dict(predecessor_pin=e['predecessor_pin'],candidate_pin=e['candidate_pin'],exact_inverse=True,change_count=len(e['changes'])))
 return result
sfpin=pin(P/'COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json');assert sfpin['sha256']=='5e7acb3344cf381e3530568df8448a4ed843a6ea4b9e8a32f4237d5aaf9a3952';sf=read(sfpin)
assert sf['source_only']is True and sf['manifest_prepared']is False and sf['deletion_executed']is False and sf['compiler_or_business_executed']is False
inv=read(sf['strict_low_level_Source_provenance_pin']);back=inverse_check(inv);assert len(back)==3
assert inv['all_functions_wholebytes_equal']is True and inv['seven_lowlevel_and_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal']is True
oldsf=read(sf['predecessor_Source_freeze_pin']);oldinv=read(oldsf['strict_low_level_Source_provenance_pin']);oldback=inverse_check(oldinv)
methods=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
for e in inv['entries']:assert functions(exact(e['candidate_pin']))==functions(exact(e['predecessor_pin']))
e=oldinv['entries'][0];newfunc=functions(exact(e['candidate_pin']));oldfunc=functions(exact(e['predecessor_pin']));assert all(newfunc[n]==oldfunc[n]for n in methods)
# The primitive syscall, immediate durable receipt, parent fsync and first-failure sequence is unchanged.
e=oldinv['entries'][2];a=exact(e['predecessor_pin']).decode();b=exact(e['candidate_pin']).decode();start='                os.unlink(target.name,dir_fd=fd)';end='        for r in protected+'
assert a[a.index(start):a.index(end)]==b[b.index(start):b.index(end)]
text=(P/'literal11_release_common.py').read_text();tree=ast.parse(text)
safe={'_base','source_gate','closed_proofs','full50_closed_proof','runtime_completed_proof','monitor_closed_proof'}
# Execute only declarations and the named metadata gates, never the candidate module or its business entry.
body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.AnnAssign))or isinstance(n,ast.FunctionDef)and n.name in safe]
g={'__file__':str(P/'literal11_release_common.py'),'__name__':'independent_extracted_readonly_metadata'}
exec(compile(ast.Module(body=body,type_ignores=[]),str(P/'literal11_release_common.py'),'exec'),g)
g['source_gate'](sfpin);facts=g['closed_proofs']();assert len(facts)==14
plan=read(sf['exact_role_plan_pin']);targets=g['TARGET_SELECTED_PINS'];keep=g['ROLE_KEEP_PINS']
assert targets==plan['literal3_fullpins']==sf['literal3_fullpins'] and len(targets)==3 and sum(x['size_bytes']for x in targets)==526645544
assert len(keep)==9 and keep==plan['current_original_science9_input_pins']
assert plan['exact_current_MF3_indices_migrated_to_history']==[2605,4177,4467] and plan['all_other8808_PF_rows_data_retained']is True
mf=read(plan['previous8811_manifest_pin']);mp=mf['current_protected_full_EOF_pins'];assert len(mp)==8811
assert [mp[k]for k in [2605,4177,4467]]==targets
rebind=sf['exact_old_v3_raw_document_current_rebinding'];assert rebind==plan['exact_old_v3_raw_document_current_rebinding']==inv['exact_one_document_selected_current_rebinding']
a=rebind['historical_selected_pin'];b=rebind['actual_current_pin'];assert a['path']==b['path'] and a['sha256']==b['sha256'] and a['size_bytes']==b['size_bytes'] and a['identity'][1:]==b['identity'][1:] and a['identity'][0]==16777234 and b['identity'][0]==16777229
assert mp[2632]==b and g['HISTORICAL_PINS']['oldv3PACK_owner_complete_raw']==g['OLD_PACK_V3_AUTHORITY']['complete_raw_pin']==b;exact(b)
assert rebind['changed_identity_indices']==[0] and rebind['no_general_device_remapping_or_tolerant_pin_rule']is True
# Direct current dependencies do not demand the three obsolete bodies.
def fullpins(v):
 if isinstance(v,dict):
  if {'path','sha256','size_bytes','identity'}<=v.keys():yield {k:v[k]for k in ('path','sha256','size_bytes','identity')}
  else:
   for x in v.values():yield from fullpins(x)
 elif isinstance(v,list):
  for x in v:yield from fullpins(x)
paths={p['path']for p in targets};hf=read(plan['current_HF3955_pin']);assert len(hf['dependencies'])==3955 and not paths.intersection(x['path']for x in fullpins(hf['dependencies']))
binding=read(g['HISTORICAL_PINS']['saved3301_original_binding']);assert not paths.intersection(x['path']for x in fullpins(binding))
assert plan['owner_file_count']==541 and plan['owner_directory_count']==69 and plan['retained_other_file_count']==538
inventory=plan['complete_owner_inventory'];assert len(inventory['ordinary_file_identities'])==541 and len(inventory['directory_identities'])==69
assert all(inventory['ordinary_file_identities'][p['path']]==p['identity']for p in targets)
macro=next(p for p in keep if p['path'].endswith('/axial_macro.xsm'));assert all(p['sha256']==macro['sha256'] and p['size_bytes']==macro['size_bytes'] and p['identity'][:2]!=macro['identity'][:2]for p in targets[1:])
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='disjoint');guard=fn.body[0].test;expression=compile(ast.Expression(guard),'<actual disjoint count>','eval');assert eval(expression,g)is False
negative=dict(g);negative['TARGETS']=g['TARGETS'][:-1];assert eval(expression,negative)is True
negative=dict(g);duplicate=list(targets);duplicate[2]=duplicate[1];negative['TARGET_SELECTED_PINS']=duplicate;assert sum(p['size_bytes']for p in duplicate)==g['BYTES'] and eval(expression,negative)is True
for _ in range(2):
 nodes=[]
 for p in targets+keep:
  s=Path(p['path']).lstat();assert identity(s)==p['identity'] and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1;nodes.append((s.st_dev,s.st_ino))
 assert len(nodes)==len(set(nodes))==12
assert all(v is None for k,v in sf.items()if k.startswith('future_')) and all(v is None for k,v in plan.items()if k.startswith('future_'))
rawpin=pin(R/'ACTUAL_LITERAL3_BEFORE_SAVED370_V2_CURRENT_RAW_DOC_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json');raw=read(rawpin);q=raw['actual_Source_preparation_return'];assert raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0 and type(q['exit_code'])is int and q['exit_code']==0 and q.get('session_id')is None
assert sfpin in list(fullpins(json.loads(q['output'].strip().splitlines()[-1])))
assert not Path(g['FINAL']).exists()
report=dict(schema='INDEPENDENT_LITERAL3_BEFORE_SAVED370_V2_SOURCE_DELTA_REVIEW_V1',status='PASS_LITERAL3_BEFORE_SAVED370_V2_SOURCE_DELTA_REVIEW',source_only=True,failure=None,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,files_deleted=False,manifest_prepared=False,Source_freeze_pin=sfpin,Source_pins=sf['Source_pins'],exact_role_plan_pin=sf['exact_role_plan_pin'],source_inverse_pin=sf['strict_low_level_Source_provenance_pin'],Source_preparer_pin=sf['Source_preparer_pin'],actual_Source_preparation_tool_pin=rawpin,whole_v2_to_v1_three_script_inverses=back,whole_v1_to_original_literal18_three_script_inverses=oldback,all_v2_functions_whole_bytes_equal_v1=True,seven_low_level_methods_whole_bytes_equal_original=methods,unlink_immediate_truthful_receipt_directory_fsync_FirstFailure_whole_bytes_equal=True,actual_readonly_extracted_source_gate_and_closed_proofs_passed=True,actual_closed_authority_count=14,exact_old_raw_document_current_rebinding=rebind,only_exact3_MF8811_rows_migrated_to_history=[2605,4177,4467],all_other8808_MF_rows_retained=True,no_current_HF3955_or_saved_binding_target_direct_role=True,target_count=3,target_logical_bytes=526645544,owner_file_count=541,owner_directory_count=69,retained_other_file_count=538,actual_disjoint_count3_and_equal_size_duplicate_node_negative_checked=True,target3_and_scientific9_current_all7_UID_singlelink_twice_verified=True,original_caps=sf['original_caps'],predicted_margin_is_not_actual_admission=True,scientific_body_EOF_repeated=False,target_body_EOF_repeated=False,physics_qualified=False)
D.mkdir();rp=D/'REVIEW.json'
with rp.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(review_pin=pin(rp),target_count=3,actual_closed_authority_count=14,source_only=True,business_executed=False,deletion_executed=False)))

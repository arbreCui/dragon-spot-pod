from pathlib import Path
import ast,difflib,hashlib,json,tarfile,stat
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
parent=(P/'PARENT_SOURCE/Root_bound_complete_native_genuine_host.py').read_bytes();text=parent.decode();tree=ast.parse(text);lines=text.splitlines(keepends=True);records=[]
def change(start,end,new,role):
 old=''.join(lines[start:end]);records.append(dict(role=role,old_start0=start,old_end0=end,old_full_lines=old.splitlines(keepends=True),new_full_lines=new.splitlines(keepends=True)))
for node in tree.body:
 if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
  key=node.targets[0].id
  if key in ('SOURCE_STATUS','SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA'):
   value="'UNREADY_SOURCE_ONLY'"if key=='SOURCE_STATUS'else'None';change(node.lineno-1,node.end_lineno,key+' = '+value+'\n','replace_bound_global_'+key)
 if isinstance(node,ast.FunctionDef)and node.name=='main':
  new='''def main():
    started=time.monotonic()
    require(len(sys.argv)==1 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile()is None,'fixed unprofiled nonoptimized genuine observation host')
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and all(type(v)is str and bool(v)for v in(SOURCE_ARCHIVE,RECEIPTS,HOST,OUT,CONTROL,TARGET,TARGET_SHA,BINDING,BINDING_SHA,SOURCE_ADMISSION_SHA)),'UNREADY Source refuses any runtime/native action')
    require(PROTOCOL is None and PROTOCOL_SHA is None and all(v is None for v in(ACTUAL_PROTOCOL_QUALIFICATION_SHA256,ACTUAL_TRANSFER_QUALIFICATION_SHA256,REACTION_MULTIPLICITY_QUALIFICATION_SHA256,ACTUAL_SCIENTIFIC_REFERENCE_SHA256)),'all future science/native qualifications unknown')
    import hashlib
    require(hashlib.sha256(SUPPORT.read_bytes()).hexdigest()==SUPPORT_SHA,'original complete genuine support Source')
    spec=importlib.util.spec_from_file_location('axmat_original_observation_support',SUPPORT);support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    require(Path(support.__file__).resolve()==SUPPORT.resolve()and all(os.environ.get(k)=='1'for k in support.THREAD_KEYS)and Path(sys.executable).resolve()==support.PYTHON and os.environ.get('SPOT_AXMAT_OBSERVATION')=='ADMITTED_SOURCE_ONLY','original Python and all five thread variables1 plus admitted observer env')
    support.pin(SUPPORT,SUPPORT_SHA);support.pin(BINDING,BINDING_SHA);b=strict_json(Path(BINDING).read_bytes())
    require(b['namespaces']==dict(host=HOST,output=OUT,control=CONTROL,source=SOURCE_ARCHIVE,receipts=RECEIPTS)and b['independent_observation_Source_admission_pin']['sha256']==SOURCE_ADMISSION_SHA,'whole actual Root namespace/admission binding')
    target_pin=support.pin(TARGET,TARGET_SHA);require(b['bound_runtime_pin']==dict(target_pin,size_bytes=target_pin['identity'][4]),'exact complete bound runtime Source pin')
    runtime,runtime_pin=support.load(Path(TARGET),TARGET_SHA,'axmat_Root_bound_observation_runtime')
    require(runtime.SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','bound runtime status exact')
    runtime.run(sys.modules[__name__],support,b,b['actual_author_Source_contract'],started)
'''
  change(node.lineno-1,node.end_lineno,new,'replace_whole_original_main_with_complete_observation_entry')
for h in sorted(records,key=lambda h:h['old_start0'],reverse=True):lines[h['old_start0']:h['old_end0']]=h['new_full_lines']
result=''.join(lines).encode();ast.parse(result);(P/'complete_observation_genuine_host.UNREADY.py').write_bytes(result)
inverse=result
for h in records:
 new=''.join(h['new_full_lines']).encode();old=''.join(h['old_full_lines']).encode();assert inverse.count(new)==1;inverse=inverse.replace(new,old,1)
assert inverse==parent
(P/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_ORIGINAL_NATIVE_GENUINE_HOST_OBSERVATION_ENTRY_SOURCE_INVERSE_V1',source_only=True,original_Source_sha256=hashlib.sha256(parent).hexdigest(),derived_Source_sha256=hashlib.sha256(result).hexdigest(),complete_full_inverse_hunks=records,all_original_support_guard_helpers_byte_for_byte_unchanged=True,original_class_MRO_and_guard_Source_unchanged=True,actual_runtime=None),indent=2)+'\n')
for draft,name in [('runtime','complete_observation_BUILD5_AB_runtime.UNREADY.py'),('binder','bind_complete_observation_SOURCE_only.UNREADY.py'),('postclose','Root_observation_postclose_META_writer.UNREADY.py')]:
 raw=Path('/private/tmp/axmat_observation_'+draft+'_source_draft.py').read_bytes();ast.parse(raw);(P/name).write_bytes(raw)
rows=[]
with tarfile.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as t:
 for orig,derived in [('LIBMIX.f','LIBMIX.observe.UNREADY.f'),('LIBDEN.f','LIBDEN.observe.UNREADY.f'),('TONDRV.f','TONDRV.context_observe.UNREADY.f'),('TONSPH.f','TONSPH.observe.UNREADY.f')]:
  original=t.extractfile('Dragon/src/'+orig).read();observed=(P/'OBSERVATION_SOURCE'/derived).read_bytes();old=original.decode().splitlines(keepends=True);new=observed.decode().splitlines(keepends=True);hunks=[]
  for tag,i,j,a,b in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes():
   if tag!='equal':assert tag=='insert',(orig,tag);hunks.append(dict(tag=tag,old_start0=i,old_end0=j,new_start0=a,new_end0=b,old_full_lines=old[i:j],new_full_lines=new[a:b]))
  restored=list(new)
  for h in reversed(hunks):restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
  assert ''.join(restored).encode()==original
  rows.append(dict(original_archive_member='Dragon/src/'+orig,derived_Source_member='OBSERVATION_SOURCE/'+derived,original_sha256=hashlib.sha256(original).hexdigest(),derived_sha256=hashlib.sha256(observed).hexdigest(),complete_insert_only_hunks=hunks,full_inverse_original_physical_Source_equal=True))
(P/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_FOUR_MATERIAL_NATIVE_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_FULL_SOURCE_INVERSE_V1',source_only=True,derivations=rows,all_original_numeric_and_branch_Source_bytes_retained=True,observer_has_no_numerical_assignment_to_original_routine_parameters=True,all_actual_observations_unknown=True,actual_observation=None,actual_native_Source_binary_linkage=None),indent=2)+'\n')
print(json.dumps(dict(host_full_inverse_hunks=len(records),physical_source_insert_hunks=sum(len(r['complete_insert_only_hunks'])for r in rows),all_new_Python_Source_AST_parsed=True,actual_Runtime=None)))

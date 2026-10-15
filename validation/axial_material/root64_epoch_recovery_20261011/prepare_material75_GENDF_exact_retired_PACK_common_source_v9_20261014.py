"""Rebase only Source namespaces/current Common metadata; no business or SCI EOF."""
import ast,hashlib,importlib.util,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD_M=R/'current_formal_material_authority_exact_cache70_post_curated66_latest_full50_source_v8_20261014'
OLD_G=R/'current_eleven_saved_gendf_post_curated66_latest_full50_host_source_v5_20261014'
M=R/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
G=R/'current_eleven_saved_gendf_post_literal3_latest_full50_host_source_v6_20261014'
C=R/'post_literal3_old_pack_current_catalog_common_source_v1_20261014'
PLAN_NAME='MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_PREPARATION_PLAN.json'
SF_NAME='COMPLETE_POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('ordinary bounded metadata/Source only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  z=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('current7')
 return dict(path=str(p),sha256=hashlib.sha256(z).hexdigest(),size_bytes=len(z),identity=identity(s))
def read(p):
 if isinstance(p,dict):
  if pin(p['path'])!={k:p[k]for k in('path','sha256','size_bytes','identity')}:raise RuntimeError('exact metadata PF')
  p=p['path']
 else:pin(p)
 return json.loads(Path(p).read_bytes())
def write(p,v):
 z=v if isinstance(v,bytes)else v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(z);f.flush();os.fsync(f.fileno())
 return pin(p)
def ispin(v):return isinstance(v,dict)and {'path','sha256','size_bytes','identity'}<=set(v)
def substitute(v,mapping):
 if ispin(v):
  pair=mapping.get(v['path'])
  if pair:
   if {k:v[k]for k in('path','sha256','size_bytes','identity')}!=pair[0]:raise RuntimeError('exact selected PF substitution')
   return pair[1]
  return v
 if isinstance(v,list):return[substitute(x,mapping)for x in v]
 if isinstance(v,dict):return{k:substitute(x,mapping)for k,x in v.items()}
 return v
def unique(rows):
 out={}
 for p in rows:
  if not ispin(p):raise RuntimeError('actual PF only')
  if p['path']in out and out[p['path']]!=p:raise RuntimeError('conflicting current PF')
  out[p['path']]=p
 return sorted(out.values(),key=lambda p:p['path'])
def current7(rows):
 for p in unique(rows):
  if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('every actual selected full7 unchanged')
def main():
 if M.exists()or G.exists():raise RuntimeError('two unique Source namespaces')
 oldplanpin=pin(OLD_M/PLAN_NAME);old=read(oldplanpin);pubpin=pin(OLD_M/'COMPLETE_ACTUAL_V18_SAVED370_BOUND_MATERIAL_GENDF_ONCE_METADATA_PUBLICATION.json');pub=read(pubpin)
 common_sf_pin=pin(C/SF_NAME)
 if common_sf_pin['sha256']!='472991dd73110a25e61c4abaa73d2e2de43bc193d3ff94fd5e4b10068bfe9747':raise RuntimeError('exact one source-only Common freeze')
 common=read(common_sf_pin)
 newchoices={'selected_new_Common_Source_pin':common['actual_common_source_pin'],'selected_new_Common_Source_freeze_pin':common_sf_pin,'selected_new_catalog_pin':common['actual_catalog_pin'],'selected_new_binding_pin':common['actual_binding_pin']}
 mapping={old[k]['path']:(old[k],p)for k,p in newchoices.items()}
 current7(old['dependencies']+list(newchoices.values())+common['files'])
 oldcommon=Path(old['selected_new_Common_Source_pin']['path']).parent.name
 copied=[];inverse=[];M.mkdir();G.mkdir()
 for row in old['source_copies']:
  beforepin=row['candidate_pin'];p=Path(beforepin['path']);raw=p.read_bytes()
  if pin(p)!=beforepin:raise RuntimeError('v8 all original source bytes exact')
  folder=M if p.parent==OLD_M else G if p.parent==OLD_G else None
  if folder is None:raise RuntimeError('declared24 source two namespaces')
  text=raw.decode();blocks=[]
  for before,after in ((oldcommon,C.name),(OLD_M.name,M.name),(OLD_G.name,G.name)):
   count=text.count(before)
   if count:
    if count!=1:raise RuntimeError('one exact Source namespace/Common literal')
    text=text.replace(before,after,1);blocks.append(dict(before=before,after=after))
  if p.suffix=='.py':ast.parse(text)
  back=text
  for b in reversed(blocks):
   if back.count(b['after'])!=1:raise RuntimeError('exact one inverse literal')
   back=back.replace(b['after'],b['before'],1)
  if back.encode()!=raw:raise RuntimeError('complete v8 Source byte inverse')
  afterpin=write(folder/p.name,text);mapping[beforepin['path']]=(beforepin,afterpin)
  entry=dict(row);entry.update(predecessor_pin=beforepin,candidate_pin=afterpin,immediate_predecessor_v8_pin=beforepin,exact_literal_change_blocks=blocks)
  copied.append(entry);inverse.append(dict(predecessor_pin=beforepin,candidate_pin=afterpin,changes=blocks))
 if len(copied)!=24 or sum(Path(x['candidate_pin']['path']).suffix in('.py','.f','.f90')for x in copied)!=22:raise RuntimeError('unchanged22code2static count')
 invpin=write(M/'COMPLETE_MATERIAL_GENDF_V8_TO_V9_EXACT_COMMON_AND_NAMESPACE_BYTE_INVERSE.json',dict(schema='COMPLETE_MATERIAL_GENDF_V8_TO_V9_EXACT_COMMON_AND_NAMESPACE_BYTE_INVERSE_V1',entries=inverse,predecessor_source_plan_pin=oldplanpin,predecessor_complete_inverse_pin=old['complete_inverse_pin'],all_Fortran_math_thresholds_guard_methods_unchanged=True,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False))
 templates=[]
 for t in old['current_live_metadata_templates']:
  name=Path(t['original_metadata_pin']['path']).name;beforepin=pub['actual_metadata_pins'][name];original=read(beforepin);value=json.loads(json.dumps(original));fields=list(t['selected_live_fields'])
  for key in fields:value[key]=substitute(value[key],mapping)
  for key in ('required_actual_aaa3_output_directory','required_actual_saved_audit_output_directory','required_actual_aaa3_host_freeze_pin','required_actual_saved_audit_host_freeze_pin'):
   if key in original and value[key]!=original[key]:raise RuntimeError('actual v18/saved upstream prerequisites unchanged')
  futures=[]
  for x in t['future_owning_metadata_field_bindings']:
   key=x['field'];p=original[key]
   if not ispin(p):raise RuntimeError('actual v8 owning predecessor pin')
   futures.append(dict(field=key,predecessor_pin=p,future_owning_pin=None,must_bind_actual_reviewed_new_metadata_before_runtime=True));value[key]=None
  for key in ('dependencies','selected_current_Common_Source_pin','selected_current_Common_binding_pin','selected_current_Common_Source_freeze_pin','selected_current_mount_catalog_pin','current_Common_Source_freeze_pin','actual_current_catalog_pin'):
   if key in value:value[key]=substitute(value[key],mapping)
  templates.append(dict(original_metadata_pin=beforepin,original_metadata_value=original,selected_live_fields=fields,proposed_current_metadata=value,owning_frozen_metadata_pin=None,requires_final_independent_Source_review_before_owning_freeze=True,future_owning_metadata_field_bindings=futures))
 deps=unique(substitute(old['dependencies'],mapping)+[oldplanpin,pubpin,old['complete_inverse_pin'],common_sf_pin]+common['files']+list(newchoices.values())+[invpin]+[p for x in copied for p in (x['predecessor_pin'],x['candidate_pin'])]+[x['original_metadata_pin']for x in templates])
 current7(deps)
 plan=json.loads(json.dumps(old));plan.update(newchoices);plan.update(actual_Source_revision=9,material_Source_namespace=str(M),GENDF_Source_namespace=str(G),source_copies=copied,complete_inverse_pin=invpin,current_live_metadata_templates=templates,dependencies=deps,selected_exact_retired_PACK_Common_Source_freeze_pin=common_sf_pin,predecessor_actual_material8_Source_plan_pin=oldplanpin,predecessor_owning_metadata_publication_pin=pubpin,old_v8_preoutput_failure_Root_tool_pin=pin(R/'ROOT_ACTUAL_MATERIAL75_BUILD_V8_PREOUTPUT_CATALOG_RETIRED_PACK_FAILURE_TRUE_TOOL_RETURNS_20261014.json'),old_v8_output_namespace_was_absent_and_no_compiler_or_stage=True,only_current_Common_selection_and_source_namespaces_changed=True,required_saved370_actual_authority_still_pending=False,compiler_executed=False,numerical_executed=False,material_job_executed=False,GENDF_executed=False,files_deleted=False)
 pp=write(M/PLAN_NAME,plan)
 ready=write(M/'SOURCE_REVIEW_READY.json',dict(schema='MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_REVIEW_READY_V1',status='SOURCE_ONLY_READY_FOR_INDEPENDENT_REVIEW_NOT_RUNTIME_FREEZE',failure=None,plan_pin=pp,inverse_pin=invpin,source_copies=copied,selected_Common_Source_freeze_pin=common_sf_pin,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual=old['future_actual']))
 oldwriter=R/'write_once_material75_GENDF_after_actual_v18_saved370_HFs_CLIs_v2_20261014.py';raw=oldwriter.read_text();text=raw;changes=[]
 replacements=[(OLD_M.name,M.name),(OLD_G.name,G.name),(oldplanpin['sha256'],pp['sha256']),('ACTUAL_MATERIAL75_GENDF_AFTER_V18_AND_SAVED370_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json','ACTUAL_MATERIAL75_GENDF_V9_EXACT_COMMON_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json'),('GEN_TOOLS_SHA=\'ccd02c373e7aaf9b5ccfdd8a5d5978c49450b5ddb268b0f1ce30b381b7a8e796\'','GEN_TOOLS_SHA=None'),('build-only-after-v18-saved370-20261014-v8','build-only-after-v18-saved370-20261014-v9'),('observations-after-v18-saved370-20261014-v8','observations-after-v18-saved370-20261014-v9'),('GENDF-after-v18-saved370-20261014-v5','GENDF-after-v18-saved370-20261014-v6')]
 for before,after in replacements:
  if text.count(before)!=1:raise RuntimeError('one exact writer namespace/actualplan/gen-tool selector')
  text=text.replace(before,after,1);changes.append(dict(before=before,after=after))
 # The final fullPF for the actual generation tool is not available inside its
 # own running producer; a later exact one-token binder fills it after closure.
 w=write(R/'write_once_material75_GENDF_v9_exact_common_HFs_CLIs_unbound_source_20261014.py',text)
 wi=write(M/'COMPLETE_MATERIAL_GENDF_V8_TO_V9_ONCE_WRITER_NAMESPACE_BYTE_INVERSE.json',dict(schema='COMPLETE_MATERIAL_GENDF_V8_TO_V9_ONCE_WRITER_NAMESPACE_BYTE_INVERSE_V1',predecessor_pin=pin(oldwriter),candidate_pin=w,changes=changes,actual_generation_tool_SHA_binding_still_pending=True,source_only=True))
 for folder in(M,G):
  fd=os.open(folder,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(fd)
  finally:os.close(fd)
 print(json.dumps(dict(status='MATERIAL_GENDF_V9_EXACT_RETIRED_PACK_COMMON_SOURCE_ONLY_READY',plan_pin=pp,ready_pin=ready,inverse_pin=invpin,source_copies=copied,unbound_once_writer_source_pin=w,once_writer_inverse_pin=wi,selected_Common_Source_freeze_pin=common_sf_pin,dependency_count=len(deps),compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

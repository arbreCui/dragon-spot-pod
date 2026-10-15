"""Publish reviewed Source metadata once; never compiler/material/GENDF execution.

Fill only the already declared eleven metadata templates in dependency order.
The original962 cache70 plus5 observers/nineFortran/science33+51 stays intact.
Actual observer75, firstA, owned979740136 release and GENDF reports stay unknown.
"""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
M=REC/'current_formal_material_authority_exact_cache70_post_curated66_latest_full50_source_v8_20261014'
G=REC/'current_eleven_saved_gendf_post_curated66_latest_full50_host_source_v5_20261014'
PLAN=M/'MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_PREPARATION_PLAN.json'
PLAN_SHA='56c48fa8ca257df71a7979605630db00e4776271675006a3014eb07fa3c18515'
GEN_TOOLS=REC/'ACTUAL_MATERIAL75_GENDF_AFTER_V18_AND_SAVED370_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json'
GEN_TOOLS_SHA='ccd02c373e7aaf9b5ccfdd8a5d5978c49450b5ddb268b0f1ce30b381b7a8e796'
BUILD_OUT=R/'validation/artifacts/axial-material-new-current-material-observer-complete75-build-only-after-v18-saved370-20261014-v8'
MATERIAL_OUT=R/'validation/artifacts/axial-material-new-current-formal-material-observations-after-v18-saved370-20261014-v8'
GENDF_OUT=R/'validation/artifacts/axial-material-current-eleven-saved-GENDF-after-v18-saved370-20261014-v5'
PF=('path','sha256','size_bytes','identity')
ORDER=('EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json','CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json','COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json','CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in PF}
def ancestors(p):
 p=Path(p)
 if not p.is_absolute()or '..'in p.parts:raise RuntimeError('absolute canonical file')
 for q in reversed(p.parents):
  if not stat.S_ISDIR(q.lstat().st_mode):raise RuntimeError('ordinary ancestor')
def pin(p):
 p=Path(p);ancestors(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata EOF only')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def same7(p):
 q=Path(p['path']);ancestors(q);s=q.lstat()
 if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']or s.st_size!=p['size_bytes']:raise RuntimeError('current exact7 '+str(q))
 # General dependencies retain their exact original link counts, including
 # the immutable compiler's legitimate two-link role.
def load(p):
 if pin(p['path'])!=norm(p):raise RuntimeError('exact Source/metadata fullPF')
 return json.loads(Path(p['path']).read_bytes())
def unique(rows):
 out={}
 for p in rows:
  p=norm(p)
  if p['path']in out and out[p['path']]!=p:raise RuntimeError('conflicting current fullPF')
  out[p['path']]=p
 return list(out.values())
def write(path,value):
 ancestors(path);raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p=pin(path);s=Path(path).lstat()
 if s.st_nlink!=1 or s.st_uid!=os.getuid():raise RuntimeError('own metadata ordinary UID singlelink')
 return p
def terminal0(result):
 if type(result.get('exit_code'))is not int or result['exit_code']!=0 or result.get('session_id')is not None or not isinstance(result.get('output'),str):raise RuntimeError('genuine original terminal integer0')
def substitute(value,mapping):
 if isinstance(value,dict):
  if set(value)==set(PF):
   pair=mapping.get(value['path'])
   if pair is None:return value
   if value!=pair[0]:raise RuntimeError('exact selected old metadata fullPF mismatch')
   return pair[1]
  return{k:substitute(v,mapping)for k,v in value.items()}
 if isinstance(value,list):return[substitute(v,mapping)for v in value]
 return value

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 roles=('source-plan','Source-generation-tools','peer-review','peer-tools')
 for role in roles:
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();pins={}
 for role in roles:
  attr=role.replace('-','_');p=pin(getattr(a,attr+'_summary'))
  if p['sha256']!=getattr(a,attr+'_sha256')or p['identity']!=json.loads(getattr(a,attr+'_seven_id')):raise RuntimeError('external exact Source authority '+role)
  pins[role]=p
 if pins['source-plan']['path']!=str(PLAN)or pins['source-plan']['sha256']!=PLAN_SHA or pins['Source-generation-tools']['path']!=str(GEN_TOOLS)or pins['Source-generation-tools']['sha256']!=GEN_TOOLS_SHA:raise RuntimeError('one actual prepared source plan and true generation0')
 plan=load(pins['source-plan']);generation=load(pins['Source-generation-tools']);review=load(pins['peer-review']);tools=load(pins['peer-tools']);selfpin=pin(Path(__file__).absolute())
 for k in('actual_Source_preparation_return','actual_Source_generation_return'):terminal0(generation[k])
 if generation['observed_closed']is not True or type(generation['original_integer_exit_code'])is not int or generation['original_integer_exit_code']!=0:raise RuntimeError('actual Source generation observedclosed0')
 emitted=json.loads(generation['actual_Source_generation_return']['output'].strip().splitlines()[-1])
 if emitted['plan_pin']!=pins['source-plan']:raise RuntimeError('Source generation true originalstdout plan fullPF')
 if review['plan_pin']!=pins['source-plan']or review['writer_source_pin']!=selfpin or review['source_only']is not True or review['failure']is not None or any(review[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('same-round independent candidate and writer Source-only review')
 terminal0(tools['actual_review_return'])
 if tools['observed_closed']is not True or type(tools['original_integer_exit_code'])is not int or tools['original_integer_exit_code']!=0 or json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']!=pins['peer-review']:raise RuntimeError('genuine independent Source0/stdout exactreport')
 templates={Path(t['original_metadata_pin']['path']).name:t for t in plan['current_live_metadata_templates']}
 if set(templates)!=set(ORDER)or len(templates)!=11:raise RuntimeError('exact eleven declared metadata templates')
 outputs=[(G if 'GENDF'in name else M)/name for name in ORDER]
 cli_paths=[M/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json',M/'ROOT_REVIEWABLE_MATERIAL_FIRST_A_DYNAMIC_INTERFACE_SOURCE_ONLY.json',M/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json',G/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json',M/'COMPLETE_ACTUAL_V18_SAVED370_BOUND_MATERIAL_GENDF_ONCE_METADATA_PUBLICATION.json']
 if any(os.path.lexists(p)for p in outputs+cli_paths)or any(os.path.lexists(p)for p in (BUILD_OUT,MATERIAL_OUT,GENDF_OUT,GENDF_OUT.with_name(GENDF_OUT.name+'-evidence'))):raise RuntimeError('all owning metadata/output namespaces fresh; no rewrite or retry')
 copies=plan['source_copies']
 if len(copies)!=24 or sum(Path(r['candidate_pin']['path']).suffix in('.py','.f','.f90')for r in copies)!=22:raise RuntimeError('original22code2static exact copies')
 for row in copies:
  if pin(row['candidate_pin']['path'])!=row['candidate_pin']:raise RuntimeError('actual copied Source fullPF')
 mapping={t['original_metadata_pin']['path']:(t['original_metadata_pin'],None)for t in plan['current_live_metadata_templates']}
 # No future owning pin is invented: known Source references below are filled
 # only after the corresponding real O_EXCL write in the declared order.
 mapping={}
 savedpins=plan['selected_actual_saved370_authority_pins'];audit=load(savedpins['report']);savedhf=load(plan['selected_current_saved370_Host_freeze_pin']);savedcli=load(plan['selected_current_saved370_CLI_pin'])
 if audit['status']!='ACTUAL_SAVED_FULL370_THREE_AXIAL_MOMENT_DIAGNOSTIC_CLOSED0_ONLY'or audit['failure']is not None or audit['after_check_error']is not None or len(audit['fixed_current_pins'])!=3349 or len(audit['actual_TMP_output_pins'])!=24 or len(audit['output_pins'])!=30 or plan['selected_current_saved370_Host_freeze_pin']not in audit['fixed_current_pins']:raise RuntimeError('actual Saved0/current3349/output30/TMP24 whole live scope')
 savedpost=load(savedpins['post_review']);savedtools=load(savedpins['post_tools']);terminal0(savedtools['actual_review_return'])
 if savedpost['schema']!='INDEPENDENT_SAVED370_AFTER_V18_V3_ACTUAL_DIAGNOSTIC_POSTVERIFICATION_V1'or savedpost['status']!='PASS_ACTUAL_SAVED370_AFTER_V18_V3_ORIGINAL_SCOPE_DIAGNOSTIC_POSTVERIFICATION'or savedpost['failure']is not None or savedpost['actual_report_pin']!=savedpins['report']:raise RuntimeError('actual Saved post0 bound source prerequisite')
 full=load(plan['selected_actual_latest_full50_report_pin']);fullhf=load(plan['selected_actual_latest_full50_Host_freeze_pin'])
 if full['status']!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or full['engineering_three_plane_closed0']is not True or full['failure']is not None or len(full['records'])!=50:raise RuntimeError('actual v18 full50 upstream')
 roots=unique(plan['dependencies']+list(savedpins.values())+[plan['selected_current_saved370_Host_freeze_pin'],plan['selected_current_saved370_CLI_pin']]+savedhf['fixed_source_files']+audit['fixed_current_pins']+audit['output_pins']+audit['actual_TMP_output_pins']+fullhf['dependencies']+full['fixed_current_pins']+full['output_pins']+list(pins.values())+[selfpin,pin(M/'SOURCE_REVIEW_READY.json')])
 for t in templates.values():roots=unique(roots+[t['original_metadata_pin']]+t['proposed_current_metadata'].get('dependencies',[]))
 for p in roots:same7(p)
 inverse=plan['complete_inverse_pin'];current70=templates['COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json']['proposed_current_metadata']['selected_actual_build70_report'];build=load(current70)
 if current70['sha256']!='962c1c5810fd409db47db2ac65742b835f9f360af253978068239f6fdcc0bf44'or build['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY':raise RuntimeError('original selected962 cache70, never repaired runtime inserted into material75')
 old70=build['actual_complete70_link_inputs'];order=templates['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json']['proposed_current_metadata']['original_five_Source_order']
 if len(old70)!=70 or len(order)!=5 or old70[57].split('/')[-1]!='SPOT1P64.o'or sum(p.endswith('.a')for p in old70)!=4:raise RuntimeError('original70 math57/fourarchives + exact5 order')
 outpins={};created=[]
 for name in ORDER:
  t=templates[name];value=json.loads(json.dumps(t['proposed_current_metadata']));fields=list(t['selected_live_fields']);folder=G if 'GENDF'in name else M
  # Only declared live fields are rebound. No traversal of archived reports or
  # current scientific origin tables reclassifies historical bodies as live.
  for key in fields:value[key]=substitute(value[key],mapping)
  for required in t['future_owning_metadata_field_bindings']:
   key=required['field'];old=required['predecessor_pin']
   if value[key]is not None:raise RuntimeError('exact future-own placeholder expected')
   if name=='CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json'and key=='complete_scoped_byte_inverse_pin':value[key]=inverse
   else:
    pair=mapping.get(old['path'])
    if pair is None or pair[0]!=old:raise RuntimeError('owning topology predecessor not yet actually written: '+name+'/'+key)
    value[key]=pair[1]
  if 'dependencies'in value:value['dependencies']=unique(substitute(value['dependencies'],mapping)+roots+created)
  if name=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json':value['dependencies']=unique(value['dependencies']+[outpins['COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json']])
  if name=='CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json':value.update(planned_actual_output_root=str(GENDF_OUT),planned_actual_evidence_root=str(GENDF_OUT)+'-evidence')
  value.update(actual_latest_full50_and_saved370_proof_bound=True,actual_latest_full50_report_pin=plan['selected_actual_latest_full50_report_pin'],actual_saved370_report_pin=savedpins['report'],same_round_independent_Source_review_pin=pins['peer-review'],same_round_independent_Source_tools_pin=pins['peer-tools'],once_writer_Source_pin=selfpin,scientific_body_EOF_not_repeated_by_writer=True,physics_qualified=False)
  p=write(folder/name,value);outpins[name]=p;created.append(p);mapping[t['original_metadata_pin']['path']]=(t['original_metadata_pin'],p)
  for q in roots:same7(q)
 env=load(plan['selected_actual_latest_full50_Root_argv_pin'])['exact_argv'][:11]
 def base(host):return env+[str(host)]
 def triple(role,p):return['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 buildargv=base(M/'build_current_observation_runtime.py')
 for role,p in [('current70',current70),('source-freeze',outpins['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json']),('host-freeze',outpins['COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json']),('aaa3',plan['selected_actual_latest_full50_report_pin']),('saved-audit',savedpins['report'])]:buildargv+=triple(role,p)
 buildargv+=['--output-dir',str(BUILD_OUT)]
 if len(buildargv)!=44:raise RuntimeError('actual Source parser build5triples+output44')
 bcli=write(cli_paths[0],dict(schema='ROOT_REVIEWABLE_ACTUAL_V18_SAVED370_ORIGINAL_CACHE70_OBSERVER75_EXACT_BUILD_ARGV_V1',exact_reviewable_argv=buildargv,argv=buildargv,shell_safe_command=shlex.join(buildargv),selected_source_freeze_pin=outpins['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'],selected_host_freeze_pin=outpins['COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'],host_source_pin=pin(M/'build_current_observation_runtime.py'),selected_actual_original962cache70_report_pin=current70,selected_actual_v18_full50_report_pin=plan['selected_actual_latest_full50_report_pin'],selected_actual_saved370_report_pin=savedpins['report'],planned_output_root=str(BUILD_OUT),complete_executable_argv=True,compiler_executed=False,material_job_executed=False,physics_qualified=False))
 producer_known=base(M/'produce_current_formal_material_observations.py')+triple('seed-plan',pin(M/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json'))+triple('host-freeze',outpins['COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'])
 mcli=write(cli_paths[1],dict(schema='MATERIAL_FIRST_A_EXACT_SOURCE_INTERFACE_FUTURE_ACTUAL_OBSERVER75_REPORT_REQUIRED_V1',known_argv_prefix=producer_known,required_actual_prefix='observer75',each_required_suffix=['summary','sha256','seven-id'],actual_observer75_report_pin=None,final_output_option=['--output-dir',str(MATERIAL_OUT)],is_complete_executable_argv=False,first_A_only_original_Host_semantics=True,actual_first_A_report_pin=None,actual_owned979740136_release_receipt_pin=None,compiler_or_material_executed=False,physics_qualified=False))
 ecli=write(cli_paths[2],dict(schema='MATERIAL_EVIDENCE_SOURCE_INTERFACE_FUTURE_ACTUAL_REQUEST_REQUIRED_V1',host_source_pin=pin(M/'run_current_material_lineage_evidence.py'),selected_source_freeze_pin=outpins['COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json'],selected_host_freeze_pin=outpins['COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json'],known_argv_prefix=base(M/'run_current_material_lineage_evidence.py')+triple('source-freeze',outpins['COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json'])+triple('host-freeze',outpins['COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json']),required_actual_prefix='request',each_required_suffix=['summary','sha256','seven-id'],actual_request_pin=None,is_complete_executable_argv=False,original_intended_exit2_not_changed_to_PASS=True,joint_minimum_five_roots_full2GiB_and_free8GiB_unchanged=True,compiler_or_material_executed=False,physics_qualified=False))
 gargv=base(G/'run_current_eleven_gendf_extraction.py')+triple('source-freeze',outpins['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json'])+triple('host-freeze',outpins['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json'])
 gcli=write(cli_paths[3],dict(schema='ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY',argv_prefix=gargv,final_output_option=['--output-dir',str(GENDF_OUT)],selected_source_freeze_pin=outpins['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json'],selected_host_freeze_pin=outpins['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json'],host_source_pin=pin(G/'run_current_eleven_gendf_extraction.py'),required_actual_material_observation_report_pin=None,requires_actual_first_A0_and_owned979740136_release_and_original_five_root_2GiB_free8=True,is_complete_executable_argv=False,GENDF_executed=False,physics_qualified=False))
 closure=write(cli_paths[4],dict(schema='ACTUAL_V18_SAVED370_BOUND_MATERIAL_GENDF_ONE_SOURCE_METADATA_PUBLICATION_V1',actual_metadata_pins=outpins,actual_CLI_pins=dict(build=bcli,material_first_A_dynamic=mcli,evidence_dynamic=ecli,GENDF_dynamic=gcli),same_round_Source_review_pin=pins['peer-review'],same_round_Source_tools_pin=pins['peer-tools'],actual_Source_generation_tool_pin=pins['Source-generation-tools'],once_writer_source_pin=selfpin,explicit_current_root_pins=roots,current_root_count=len(roots),Saved3349_fixed_output30_TMP24_all_remain_live=True,actual_full50_fixed_output_roots_all_remain_live=True,old_json_nested_PFs_not_promoted=True,original962_cache70_plus_five_observers_and_nine_Fortran_unchanged=True,actual_observer75_report_pin=None,actual_first_A_material_report_pin=None,actual_owned_library979740136_release_pin=None,actual_GENDF_report_pin=None,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,physics_qualified=False))
 for p in roots+created+[bcli,mcli,ecli,gcli,closure]:same7(p)
 for folder in (M,G):
  fd=os.open(folder,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(fd)
  finally:os.close(fd)
 print(json.dumps(dict(status='MATERIAL_GENDF_OWNING_SOURCE_METADATA_AND_EXACT_BUILD_CLI_ONCE_PUBLISHED_NO_BUSINESS',metadata_pins=outpins,actual_build_CLI_pin=bcli,actual_GENDF_dynamic_CLI_pin=gcli,publication_pin=closure,current_root_count=len(roots),compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

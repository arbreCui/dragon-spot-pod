"""Once-only Source metadata publication. No numerical or GENDF child is launched."""
import argparse,copy,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path);s=p.lstat()
 if not p.is_absolute()or not stat.S_ISREG(s.st_mode)or any(a.is_symlink()for a in(p,*p.parents))or s.st_size>64*2**20:raise RuntimeError('bounded ordinary Source/metadata')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('afterEOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('current7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 if pin(p['path'])!=p:raise RuntimeError('complete Source/metadata PF')
 return json.loads(Path(p['path']).read_bytes())
def same7(p):
 s=Path(p['path']).lstat()
 if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']:raise RuntimeError('current live seven fields '+p['path'])
def term0(t):
 if type(t['exit_code'])is not int or t['exit_code']!=0 or t.get('session_id')is not None or not isinstance(t['output'],str):raise RuntimeError('genuine typed terminal0')
def write(p,v):
 with p.open('xb')as f:f.write((json.dumps(v,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(p)
def unique(rows):
 table={}
 for p in rows:
  if p['path']in table and table[p['path']]!=p:raise RuntimeError('ambiguous fullPF')
  table[p['path']]=p
 return list(table.values())
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 roles=('Source-review','Source-tools','Source-generation-tools','aggregate-report','aggregate-Root-tools','aggregate-Root-argv','aggregate-post-review','aggregate-post-tools')
 for role in roles:
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();pins={}
 for role in roles:
  n=role.replace('-','_');p=pin(getattr(a,n+'_summary'))
  if p['sha256']!=getattr(a,n+'_sha256')or p['identity']!=json.loads(getattr(a,n+'_seven_id')):raise RuntimeError('required explicit full authority '+role)
  pins[role]=p
 ready=exact(pin(BASE/'SOURCE_REVIEW_READY.json'));plan=exact(ready['plan_pin'])
 for p in ready['selected_Source_pins']:
  if pin(p['path'])!=p:raise RuntimeError('SourcePF')
 peer=exact(pins['Source-review']);pt=exact(pins['Source-tools'])
 if peer['source_only']is not True or peer['failure']is not None or any(peer[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('same-round Source review only')
 for p in ready['selected_Source_pins']:
  if p not in peer['final_selected_Source_pins']:raise RuntimeError('peer exact final Source selection')
 if pin(BASE/'SOURCE_REVIEW_READY.json')not in peer['final_selected_Source_pins']:raise RuntimeError('peer exact READY Source selection')
 term0(pt['actual_review_return'])
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or json.loads(pt['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']!=pins['Source-review']:raise RuntimeError('closed Source review0 exactstdout')
 gen=exact(pins['Source-generation-tools']);term0(gen['actual_Source_preparation_return'])
 if gen['observed_closed']is not True or type(gen['original_integer_exit_code'])is not int or gen['original_integer_exit_code']!=0 or json.loads(gen['actual_Source_preparation_return']['output'].strip().splitlines()[-1])['ready_pin']!=pin(BASE/'SOURCE_REVIEW_READY.json'):raise RuntimeError('closed Source preparation0/exactREADY')
 agg=exact(pins['aggregate-report']);root=exact(pins['aggregate-Root-tools']);argv=exact(pins['aggregate-Root-argv']);post=exact(pins['aggregate-post-review']);tools=exact(pins['aggregate-post-tools'])
 term0(root['actual_terminal_return'])
 if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=argv['exact_argv']or len(argv['exact_argv'])!=30:raise RuntimeError('actual closed aggregate Root0/exact30')
 if Path(pins['aggregate-report']['path']).parent!=Path(plan['future_aggregation_artifact_roots'][0])or agg['operation']!='aggregate'or agg['schema']!='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'or agg['status']!='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'or agg['failure']is not None or agg['after_check_error']is not None or agg['actual_intentional_exit2_normal_closure']is not True:raise RuntimeError('same cumulative actual aggregation owner; no scientific qualification')
 if len(agg['records'])!=1 or agg['records'][0]['status']!='FAILED' or agg['records'][0]['error']!='own-child stage failed; no retry':raise RuntimeError('original intentional child2 retained')
 watch=exact(agg['actual_watchdog_full_pin'])
 if type(watch['returncode'])is not int or watch['returncode']!=2 or watch['limit_failure']is not None:raise RuntimeError('original actual aggregate watch2/noLimit')
 childpin=agg['actual_complete_child_receipt']['report']
 if Path(childpin['path']).parent!=Path(plan['future_aggregation_artifact_roots'][1]):raise RuntimeError('actual cumulative aggregate evidence owner')
 exact(childpin)
 if post['schema']!='INDEPENDENT_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_ACTUAL_EVIDENCE_POSTVERIFICATION_V1' or post['status']!='PASS_ACTUAL_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_EVIDENCE_POSTVERIFICATION' or post['failure']is not None or any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('explicit actual aggregate independent post protocol')
 canon={'actual_report_pin':pins['aggregate-report'],'actual_Root_true_tool_return_pin':pins['aggregate-Root-tools'],'actual_Root_argv_pin':pins['aggregate-Root-argv']}
 if any(post[k]!=p for k,p in canon.items()):raise RuntimeError('actual aggregate post exact canonical authorities')
 for key in('actual_review_return','actual_postverification_return'):
  term0(tools[key])
  if json.loads(tools[key]['output'].strip().splitlines()[-1])['review_pin']!=pins['aggregate-post-review']:raise RuntimeError('actual independent post0 stdoutPF')
 if tools['observed_closed']is not True or type(tools['original_integer_exit_code'])is not int or tools['original_integer_exit_code']!=0:raise RuntimeError('actual independent post closed0')
 selected=ready['selected_Source_pins']+[pin(BASE/'SOURCE_REVIEW_READY.json'),pin(plan['Source_author_pin']['path'])]+list(pins.values())+plan['selected_closed_current_authority_pins']+[childpin]+agg['fixed_current_pins']+agg['complete_output_pins']
 sf=exact(plan['predecessor_source_freeze_pin']);hf=exact(plan['predecessor_host_freeze_pin']);recipe=exact(plan['predecessor_recipe_pin'])
 replacements={r['predecessor_pin']['path']:r['candidate_pin']for r in plan['source_copies']}
 sf['complete_source_file_pins']=[replacements.get(p['path'],p)for p in sf['complete_source_file_pins']]
 sf.update(current_plan_pin=ready['plan_pin'],complete_cumulative_ten_root_byte_inverse_pin=ready['complete_inverse_pin'],expected_original_DiskResources_ART_role_count=8,complete_joint_source_tree_role_count=2,complete_cumulative_joint_root_count=10,cumulative_artifact_root_paths=plan['cumulative_artifact_root_paths'],cumulative_Source_root_paths=plan['cumulative_Source_root_paths'],selected_actual_aggregation_report_pin=pins['aggregate-report'],selected_actual_aggregation_post_pin=pins['aggregate-post-review'],same_round_Source_review_pin=pins['Source-review'],same_round_Source_tools_pin=pins['Source-tools'],actual_Source_generation_tool_pin=pins['Source-generation-tools'],source_only=True,candidate_executed=False,parser_executed=False,GENDF_executed=False,physics_qualified=False)
 for p in sf['complete_source_file_pins']:
  if pin(p['path'])!=p:raise RuntimeError('complete unchanged/modified Source EOF pin')
 sp=write(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json',sf)
 hf.update(host_source=plan['candidate_host_source_pin'],selected_source_freeze_pin=sp,dependencies=unique(hf['dependencies']+selected+[sp]),same_round_Source_review_pin=pins['Source-review'],same_round_Source_tools_pin=pins['Source-tools'],actual_Source_generation_tool_pin=pins['Source-generation-tools'],selected_actual_aggregation_report_pin=pins['aggregate-report'],selected_actual_aggregation_post_pin=pins['aggregate-post-review'],complete_cumulative_joint_root_count=10,candidate_executed=False,parser_executed=False,GENDF_executed=False,physics_qualified=False)
 for p in hf['dependencies']:same7(p)
 hp=write(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json',hf)
 recipe.update(argv_prefix=recipe['argv_prefix'][:11]+[plan['candidate_host_source_pin']['path'],'--source-freeze-summary',sp['path'],'--source-freeze-sha256',sp['sha256'],'--source-freeze-seven-id',json.dumps(sp['identity'],separators=(',',':')),'--host-freeze-summary',hp['path'],'--host-freeze-sha256',hp['sha256'],'--host-freeze-seven-id',json.dumps(hp['identity'],separators=(',',':'))],final_output_option=['--output-dir',plan['planned_actual_output_root']],selected_source_freeze_pin=sp,selected_host_freeze_pin=hp,host_source_pin=plan['candidate_host_source_pin'],requires_original_closed_capture_plus_extraction_plus_aggregation_complete_cumulative_ten_roots=True,is_complete_executable_argv=False,GENDF_executed=False,physics_qualified=False)
 rp=write(BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json',recipe)
 for p in hf['dependencies']:same7(p)
 fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='GENDF_TEN_ROOTS_SOURCE_METADATA_PUBLISHED_ONLY',source_freeze_pin=sp,host_freeze_pin=hp,recipe_pin=rp,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)),flush=True)
if __name__=='__main__':main()

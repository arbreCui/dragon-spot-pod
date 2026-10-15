"""Publish only the reviewed short-FIL producer's own metadata; no material run."""
import argparse,importlib.util,json,os,shlex
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec=importlib.util.spec_from_file_location('bounded_metadata',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write,identity,norm=h.pin,h.read,h.write,h.identity,h.norm
OLD=R/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
OUT=R/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
def main():
 p=argparse.ArgumentParser()
 for prefix in('source-plan','peer-review','peer-tools'):
  for suffix in('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
 a=p.parse_args()
 def load(prefix):
  path=getattr(a,prefix+'_summary');q=pin(path)
  if q['sha256']!=getattr(a,prefix+'_sha256')or q['identity']!=json.loads(getattr(a,prefix+'_seven_id')):raise RuntimeError('exact Source publication argumentPF')
  return read(q),q
 plan,pp=load('source_plan');review,rp=load('peer_review');tools,tp=load('peer_tools');wp=pin(__file__)
 if pp['path']!=str(OUT/'SHORT_FIL_FIRST_A_PRODUCER_SOURCE_PLAN.json')or plan['schema']!='SHORT_FIL_FIRST_A_PRODUCER_SOURCE_PLAN_V1'or plan['source_only']is not True:raise RuntimeError('one immutable short-FIL plan')
 if review['source_only']is not True or review['failure']is not None or any(review[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))or review['plan_pin']!=pp or review['writer_source_pin']!=wp or review['producer_source_pin']!=plan['producer_source_pin']:raise RuntimeError('same round genuine Source review exact ownPF')
 q=tools['actual_review_return']
 if tools['observed_closed']is not True or type(tools['original_integer_exit_code'])is not int or tools['original_integer_exit_code']!=0 or type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or norm(json.loads(q['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('genuine independent Source0 closed noSession stdout exactPF')
 ready=read(OUT/'READY.json');hf=read(plan['predecessor_Producer_HF_pin']);oldcli=read(plan['predecessor_actual32_CLI_pin']);post=read(plan['actual_build75_post_pin']);pt=read(plan['actual_build75_post_tool_pin'])
 if post['schema']!='INDEPENDENT_MATERIAL75_AFTER_V18_SAVED370_V9_ACTUAL_BUILD_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_MATERIAL75_AFTER_V18_SAVED370_V9_BUILD_POSTVERIFICATION'or post['failure']is not None or post['actual_report_pin']!=plan['actual_build75_report_pin']or post['actual_Root_true_tool_return_pin']!=plan['actual_build75_Root_pin']or post['actual_Root_argv_pin']!=plan['actual_build75_Root_argv_pin']:raise RuntimeError('unchanged actual observer75 authority')
 for k in('actual_review_return','actual_postverification_return'):
  q=pt[k]
  if type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or norm(json.loads(q['output'].strip().splitlines()[-1])['review_pin'])!=plan['actual_build75_post_pin']:raise RuntimeError('actual observer75 independent0')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('actual observer75 post closed0')
 def current(p):
  if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('current dependency all7')
 own=[plan['producer_source_pin'],plan['helper_source_pin'],plan['seed_plan_pin'],plan['inverse_pin'],pp,pin(OUT/'READY.json'),wp,rp,tp,pin(R/'ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json')]+ready['Source_pins']+[ready['preparer_pin'],plan['actual_build75_post_pin'],plan['actual_build75_post_tool_pin']]
 rows={}
 for q in hf['dependencies']+own:
  current(q)
  if q['path']in rows and rows[q['path']]!=q:raise RuntimeError('ambiguous current fullPF')
  rows[q['path']]=q
 for q in rows.values():current(q)
 hf.update(host_source=plan['producer_source_pin'],dependencies=sorted(rows.values(),key=lambda p:p['path']),selected_seed_plan_pin=plan['seed_plan_pin'],same_round_independent_Source_review_pin=rp,same_round_independent_Source_tools_pin=tp,once_writer_Source_pin=wp,short_FIL_only_producer_Source_plan_pin=pp,short_FIL_source_inverse_pin=plan['inverse_pin'],predecessor_Producer_HF_pin=plan['predecessor_Producer_HF_pin'],logical_library_roles_preserved=True,physical_library_filenames={'DLIB_ACTUAL':'A','DLIB8R1_370':'B'},maximum_consumed_relative_filename_characters=12,old_failed_two_library_copy_pins_are_historical_candidates_not_current_dependencies=plan['failed_private_two_copy_historical_candidates'],future_actual_short_FIL_first_A_report_pin=None,future_actual_short_FIL_979740136_release_pin=None,requires_actual_current_original_resource_budget_admission=True)
 out=Path('/Users/wen/spot/validation/artifacts/axial-material-new-current-formal-material-observations-short-FIL-after-v18-saved370-20261014-v10')
 if os.path.lexists(out):raise RuntimeError('one fresh runtime output remains uncreated')
 hp=write(OUT/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json',hf)
 argv=list(oldcli['exact_argv']);argv[11]=plan['producer_source_pin']['path']
 for prefix,pf in(('seed-plan',plan['seed_plan_pin']),('host-freeze',hp)):
  for suffix,value in(('summary',pf['path']),('sha256',pf['sha256']),('seven-id',json.dumps(pf['identity'],separators=(',',':')))):
   key='--'+prefix+'-'+suffix
   if argv.count(key)!=1:raise RuntimeError('original32 exact declared role')
   argv[argv.index(key)+1]=value
 if os.path.lexists(out)or len(argv)!=32 or argv[-2]!='--output-dir':raise RuntimeError('one new actual32 fresh namespace')
 argv[-1]=str(out)
 cp=write(OUT/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_SHORT_FIL_V10_ARGV_20261014.json',dict(schema='ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_SHORT_FIL_V10_SOURCE_ONLY_CLI_V1',exact_argv=argv,argv=argv,exact_reviewable_argv=argv,exact_command=shlex.join(argv),predecessor_actual32_CLI_pin=plan['predecessor_actual32_CLI_pin'],host_source_pin=plan['producer_source_pin'],Host_freeze_pin=hp,seed_plan_pin=plan['seed_plan_pin'],actual_observer75_report_pin=plan['actual_build75_report_pin'],actual_observer75_Root_true_tool_pin=plan['actual_build75_Root_pin'],actual_observer75_Root_argv_pin=plan['actual_build75_Root_argv_pin'],actual_observer75_independent_post_pin=plan['actual_build75_post_pin'],actual_observer75_independent_post_tool_pin=plan['actual_build75_post_tool_pin'],same_round_independent_Source_review_pin=rp,same_round_independent_Source_tools_pin=tp,output_root=str(out),is_complete_executable_argv=True,only_short_FIL_physical_filenames_and_corresponding_ordinary_copy_layout_changed=True,original_math_capture_62fields_370_and_resource_guards_unchanged=True,current_runtime_budget_admission_not_issued_by_this_writer=True,actual_first_A_report_pin=None,actual_owned979740136_release_receipt_pin=None,actual_GENDF_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False))
 fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='ACTUAL_SHORT_FIL_V10_OWN_HF_CLI_PUBLICATION_SOURCE_ONLY',Host_freeze_pin=hp,CLI_pin=cp,source_plan_pin=pp,peer_review_pin=rp,peer_tools_pin=tp,writer_source_pin=wp,actual_dependency_count=len(rows),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

"""Bind the published first-A interface to real observer75/Root/post0 metadata only.
No host imports, compilers, children, material/GENDF jobs, scientific EOF or deletions.
Future independent build post pins are required CLI inputs, never default credentials.
"""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
M=REC/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
DYNAMIC=M/'ROOT_REVIEWABLE_MATERIAL_FIRST_A_DYNAMIC_INTERFACE_SOURCE_ONLY.json'
DYNAMIC_SHA='4e49a9f6ec558765ee7a2b14741d44b0de6407606478798585f63590628166c4'
BUILD_CLI=M/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json'
ROOT_TOOLS=REC/'ROOT_ACTUAL_MATERIAL75_OBSERVER_BUILD_AFTER_V18_SAVED370_V9_TRUE_TOOL_RETURNS_20261014.json'
ROOT_ARGV=REC/'ROOT_EXACT_MATERIAL75_OBSERVER_BUILD_AFTER_V18_SAVED370_V9_ACTUAL_ARGV_20261014.json'
OUT_CLI=M/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json'
POST_SCHEMA='INDEPENDENT_MATERIAL75_AFTER_V18_SAVED370_V9_ACTUAL_BUILD_POSTVERIFICATION_V1'
POST_STATUS='PASS_ACTUAL_MATERIAL75_AFTER_V18_SAVED370_V9_BUILD_POSTVERIFICATION'
FUTURE_AUTHORITIES=dict(actual_build_post_review_pin=None,actual_build_post_tools_pin=None,actual_first_A_report_pin=None,actual_owned979740136_release_receipt_pin=None,actual_GENDF_report_pin=None)
PF=('path','sha256','size_bytes','identity')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path)
 if not p.is_absolute()or '..'in p.parts:raise RuntimeError('absolute canonical Source metadata file')
 for a in reversed(p.parents):
  if not stat.S_ISDIR(a.lstat().st_mode):raise RuntimeError('ordinary metadata ancestors')
 s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata fullEOF only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 if pin(p['path'])!=p:raise RuntimeError('metadata fullPF')
 return json.loads(Path(p['path']).read_bytes())
def same7(p):
 s=Path(p['path']).lstat()
 if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']:raise RuntimeError('existing exact current7 '+p['path'])
def term0(t):
 if type(t.get('exit_code'))is not int or t['exit_code']!=0 or t.get('session_id')is not None or not isinstance(t.get('output'),str):raise RuntimeError('genuine typed terminal integer0/noSession')
def triple(prefix,p):return['--'+prefix+'-summary',p['path'],'--'+prefix+'-sha256',p['sha256'],'--'+prefix+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
def vector_pin(argv,prefix):
 keys=['--'+prefix+'-summary','--'+prefix+'-sha256','--'+prefix+'-seven-id']
 if any(argv.count(k)!=1 for k in keys):raise RuntimeError('one published exact prefix '+prefix)
 p=pin(argv[argv.index(keys[0])+1])
 if p['sha256']!=argv[argv.index(keys[1])+1]or p['identity']!=json.loads(argv[argv.index(keys[2])+1]):raise RuntimeError('published vector exact Source PF')
 return p
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 roles=('observer75','Root-tools','Root-argv','post-review','post-tools')
 for role in roles:
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();pins={}
 for role in roles:
  attr=role.replace('-','_');p=pin(getattr(a,attr+'_summary'))
  if p['sha256']!=getattr(a,attr+'_sha256')or p['identity']!=json.loads(getattr(a,attr+'_seven_id')):raise RuntimeError('required actual authority '+role)
  pins[role]=p
 if pins['Root-tools']['path']!=str(ROOT_TOOLS)or pins['Root-argv']['path']!=str(ROOT_ARGV):raise RuntimeError('one actual observer75 v9 Root')
 dynamicpin=pin(DYNAMIC)
 if dynamicpin['sha256']!=DYNAMIC_SHA:raise RuntimeError('exact already published dynamic interface')
 dynamic=exact(dynamicpin);bclipin=pin(BUILD_CLI);bcli=exact(bclipin)
 build=exact(pins['observer75']);root=exact(pins['Root-tools']);ra=exact(pins['Root-argv']);post=exact(pins['post-review']);pt=exact(pins['post-tools'])
 term0(root['actual_terminal_return'])
 if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=ra['exact_argv']or len(ra['exact_argv'])!=44 or ra['exact_argv']!=bcli['exact_reviewable_argv']or ra['interface_pin']!=bclipin or ra['Host_freeze_pin']!=bcli['selected_host_freeze_pin']:raise RuntimeError('genuine Root44argv/publicHF/CLI closed0')
 if pins['observer75']['path']!=str(Path(ra['output_root'])/'Root_actual_observation_build_summary.json'):raise RuntimeError('Root report exact original output namespace')
 if post['schema']!=POST_SCHEMA or post['status']!=POST_STATUS or post['failure']is not None or any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('exact independent observer75 post protocol')
 canonical={'actual_report_pin':pins['observer75'],'actual_Host_freeze_pin':bcli['selected_host_freeze_pin'],'actual_CLI_pin':bclipin,'actual_Root_true_tool_return_pin':pins['Root-tools'],'actual_Root_argv_pin':pins['Root-argv']}
 if any(post[k]!=p for k,p in canonical.items()):raise RuntimeError('independent post actual five canonical PF')
 for key in('actual_review_return','actual_postverification_return'):
  term0(pt[key])
  if json.loads(pt[key]['output'].strip().splitlines()[-1])['review_pin']!=pins['post-review']:raise RuntimeError('post original stdout REVIEW pin')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('independent genuine observedclosed0')
 if build['schema']!='ACTUAL_CURRENT_FORMAL_FIVE_OBSERVATION_SOURCE_COMPLETE75_BUILD_ONLY_V1'or build['status']!='ACTUAL_FIVE_COMPILE_COMPLETE75_LINK_CLOSED0_ONLY'or build['failure']is not None or build['after_check_error']is not None or build['Dragon_linked']is not True or build['compiler_executed']is not True or build['material_job_executed']is not False or build['final_report_bytes_in_original_resources']is not True:raise RuntimeError('actual compile5/link75 only report')
 records=build['records']
 if len(records)!=6 or [q['label']for q in records]!=['build/compile_'+str(i)for i in range(5)]+['build/link_Dragon']or any(q['status']!='PASS'for q in records)or len(records[-1]['command'][3:-2])!=75:raise RuntimeError('exact original six actual stage labels/75link')
 if build['original_guard_class']!='OwnRSSSerialExecutor'or build['original_guard_MRO_unchanged']is not True or type(build['SELF_peak_bytes'])is not int or not 0<=build['SELF_peak_bytes']<512*2**20 or not 0<build['wall_seconds']<1800:raise RuntimeError('original build caps')
 if len(build['actual_watchdog_checks'])!=6 or build['fixed_current_pins'].count(bcli['selected_host_freeze_pin'])!=1 or build['current70_actual_origin']!=bcli['selected_actual_original962cache70_report_pin']:raise RuntimeError('own HF and original962cache70')
 outputs={p['path']:p for p in build['output_pins']}
 for q,w in zip(records,build['actual_watchdog_checks']):
  if w['path']not in outputs or outputs[w['path']]['sha256']!=w['sha256']:raise RuntimeError('six fullPF watch paths')
  watch=exact(outputs[w['path']])
  if type(watch['returncode'])is not int or watch['returncode']!=0 or watch['limit_failure']is not None or watch['command']!=q['command']or watch['own_child_only']is not True or watch['rss_cap_mib']!=512 or not 0<watch['wall_cap_seconds']<=600:raise RuntimeError('each actual closed child watch0/noLimit')
 for p in build['fixed_current_pins']+build['output_pins']:same7(p)
 if dynamic['schema']!='MATERIAL_FIRST_A_EXACT_SOURCE_INTERFACE_FUTURE_ACTUAL_OBSERVER75_REPORT_REQUIRED_V1'or dynamic['required_actual_prefix']!='observer75'or dynamic['each_required_suffix']!=['summary','sha256','seven-id']or dynamic['is_complete_executable_argv']is not False or dynamic['actual_observer75_report_pin']is not None or dynamic['actual_first_A_report_pin']is not None or dynamic['actual_owned979740136_release_receipt_pin']is not None:raise RuntimeError('unchanged published dynamic firstA interface')
 prefix=dynamic['known_argv_prefix'];final=dynamic['final_output_option']
 if len(prefix)!=24 or len(final)!=2 or final[0]!='--output-dir'or os.path.lexists(final[1]):raise RuntimeError('published firstA24prefix and original fresh output')
 hostpin=pin(prefix[11]);hfp=vector_pin(prefix,'host-freeze');seedpin=vector_pin(prefix,'seed-plan');hf=exact(hfp)
 if hostpin!=hf['host_source']or hf['schema']!='COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_ONLY_FREEZE_V3'or hf['selected_build_host_freeze_pin']!=bcli['selected_host_freeze_pin']or hf['selected_seed_plan_pin']!=seedpin or hf['selected_actual_build70_report']!=build['current70_actual_origin']:raise RuntimeError('unchanged producer host/seed/buildHF current exact binding')
 argv=prefix+triple(dynamic['required_actual_prefix'],pins['observer75'])+final
 if len(argv)!=32:raise RuntimeError('actual original producer 32 argv')
 for p in build['fixed_current_pins']+build['output_pins']:same7(p)
 value=dict(schema='ROOT_REVIEWABLE_ACTUAL_FIRST_A_MATERIAL_AFTER_OBSERVER75_V9_ARGV_V1',exact_argv=argv,argv=argv,exact_command=shlex.join(argv),selected_dynamic_interface_pin=dynamicpin,host_source_pin=hostpin,Host_freeze_pin=hfp,seed_plan_pin=seedpin,actual_observer75_report_pin=pins['observer75'],actual_observer75_Root_true_tool_pin=pins['Root-tools'],actual_observer75_Root_argv_pin=pins['Root-argv'],actual_observer75_independent_post_pin=pins['post-review'],actual_observer75_independent_post_tool_pin=pins['post-tools'],output_root=final[1],binder_source_pin=pin(Path(__file__).absolute()),is_complete_executable_argv=True,original_producer_math_conditions_62fields_and_370_scope_unchanged=True,original_owned979740136_capture_release_lifecycle_unchanged=True,original512_600_1800_fresh2_cold_meta96GiB_and_free8GiB_guards_unchanged=True,required_current_Root_original_budget_admission_before_execution=True,current_runtime_budget_admission_not_issued_by_this_binder=True,actual_first_A_report_pin=None,actual_owned979740136_release_receipt_pin=None,actual_GENDF_report_pin=None,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,physics_qualified=False)
 raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with OUT_CLI.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 fd=os.open(M,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps({'status':'ACTUAL_FIRST_A32_ARGV_BOUND_TO_BUILD75_ROOT0_AND_INDEPENDENT_POST0_SOURCE_ONLY_NO_JOB','CLI_pin':pin(OUT_CLI),'actual_argv_count':len(argv),'current_runtime_budget_admission_issued':False,'business_executed':False,'compiler_executed':False,'numerical_executed':False,'files_deleted':False}),flush=True)
if __name__=='__main__':main()


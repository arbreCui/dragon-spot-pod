#!/usr/bin/env python3
"""One original-guard saved-data diagnostic, only when the owning Root releases it.

This host does not certify upstream three-plane production or online BOOT. Root
must complete those before invoking this host, as required by the ordered goal.
Historical captured inputs remain historical; this does not bind new outputs as
old saved evidence or qualify AAA/ABA. The science Source is never imported here.
"""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
BASE=Path(__file__).resolve().parent
BIND=BASE/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'
FREEZE=BASE/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json'
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-AAA-saved-full370-after-latest-full50-20261014-v3')
TMP_OUT=Path('/private/tmp/SPOT_AAA_full370_after_latest_full50_ACTUAL_ONCE_20261014_v3')
SUPPORT=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p)
 if not stat.S_ISREG(before[2]):raise RuntimeError('regular non-symlink file required: '+str(p))
 with p.open('rb')as f:
  s=os.fstat(f.fileno())
  if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=before:raise RuntimeError('opened7ID differs')
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
  if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=before:raise RuntimeError('fullEOF7ID differs')
 if identity(p)!=before:raise RuntimeError('after7ID differs')
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def verify(rows):
 for row in rows:
  if pin(row['path'])!=row:raise RuntimeError('exact current fullEOF SHA/7ID differs: '+row['path'])
def write(p,d):
 with Path(p).open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def verify_current_mount_derivation(binding):
 """Actual frozen per-input declarations; no stat or old metadata rewriting."""
 selected=binding['complete_current_mount_mapping_pin']
 if pin(selected['path'])!=selected:raise RuntimeError('exact current mapping fullpin')
 mapping=json.loads(Path(selected['path']).read_text())
 if mapping['schema']!='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_V2':raise RuntimeError('current mapping schema')
 if binding.get('historical_non_live_Source_origins_explicitly_reclassified')is not True:raise RuntimeError('owning Root must explicitly classify absent historical Source origins before frozen CLI release')
 if mapping['errors']or len(mapping['rows'])!=3301 or len(mapping['historical_non_live_declarations'])!=4:raise RuntimeError('complete original3305 lineage accounting')
 original=binding['original_v1_binding_current_pin']
 if pin(original['path'])!=original:raise RuntimeError('actual original unmodified binding fullpin')
 original_binding=json.loads(Path(original['path']).read_text())
 if len(original_binding['fixed_current_pins'])!=3305:raise RuntimeError('original complete fixed list')
 historical=[];current=[]
 for row in mapping['rows']:
  old=row['historical_pin'];now=row['current_pin']
  if pin(now['path'])!=now:raise RuntimeError('every current mapping row actual fullEOF/7ID')
  if(old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])!=(now['path'],now['sha256'],now['size_bytes'],now['identity'][1:])or old['identity'][0]not in(16777234,16777229)or now['identity'][0]!=16777229:raise RuntimeError('only explicitly attested device transition')
  historical.append(old);current.append(now)
 for declaration in mapping['historical_non_live_declarations']:
  old=declaration['historical_pin']
  if declaration['current_pin']is not None or declaration['in_scientific_1129_inputs']is not False or declaration['original_v1_mandatory']is not True:raise RuntimeError('absent Source-only origins remain historical and never gain current PF')
  if old not in original_binding['fixed_current_pins']:raise RuntimeError('exact absent historical original PF')
  if old['path']in[p['path']for p in binding['fixed_current_pins']]:raise RuntimeError('absent origins cannot be used as mandatory current execution inputs')
  historical.append(old)
 if sorted(historical,key=lambda p:p['path'])!=sorted(original_binding['fixed_current_pins'],key=lambda p:p['path']):raise RuntimeError('all original3305 declarations accounted without omission')
 if any(p not in binding['fixed_current_pins']for p in current):raise RuntimeError('all3301 current declarations remain mandatory')
 if len(binding['science_original_input_pins'])!=1129 or any(p not in current for p in binding['science_original_input_pins']):raise RuntimeError('all1129 scientific current inputs retained')
 verify(current)
 return dict(mapping_pin=selected,original_unmodified_v1_binding_current_pin=original,actual_fullEOF_current_declarations=3301,original_historical_declarations=3305,complete_scientific_inputs=1129,absent_historical_Source_only_origins=mapping['historical_non_live_declarations'],only_device_reattestation=True,system_stat_or_original_metadata_modified=False,new_scientific_execution_or_physics_qualification_inferred=False)

def replace_just_created_owned_report(p,wanted,d):
 """Honest failure publication after a forced final cap check, own file only."""
 p=Path(p)
 if p!=OUT/'Root_actual_saved_full370_diagnostic_summary.json'or wanted['identity'][3]!=1 or pin(p)!=wanted:raise RuntimeError('only exact just-created regular owned summary may be replaced')
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode()
 fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
 with os.fdopen(fd,'r+b')as f:
  s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if opened!=wanted['identity']or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:raise RuntimeError('owned failure summary same opened7ID')
  if hashlib.file_digest(f,'sha256').hexdigest()!=wanted['sha256']:raise RuntimeError('owned failure summary same-fd fullEOF SHA')
  s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if after!=opened or identity(p)!=opened:raise RuntimeError('owned failure summary unchanged through fullEOF')
  f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())
  s=os.fstat(f.fileno());closed=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if closed[:4]!=opened[:4]or s.st_size!=len(raw):raise RuntimeError('owned failure summary replacement ownership/length')
 if identity(p)!=closed:raise RuntimeError('owned failure summary final path7ID')
 actual=pin(p)
 if actual['sha256']!=hashlib.sha256(raw).hexdigest():raise RuntimeError('owned failure summary completed fullEOF bytes')
 return actual

def tmp_inventory():
 """No-follow counting of this one fresh TMP output, no aliases or exclusions."""
 total=count=0
 if TMP_OUT.is_symlink():raise RuntimeError('TMP output alias refused')
 stack=[TMP_OUT]if TMP_OUT.exists()else[]
 while stack:
  p=stack.pop();fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   with os.scandir(fd)as entries:
    for e in entries:
     s=e.stat(follow_symlinks=False)
     if stat.S_ISDIR(s.st_mode):stack.append(p/e.name)
     elif stat.S_ISREG(s.st_mode):total+=s.st_size;count+=1
     else:raise RuntimeError('TMP output nonregular/symlink entry refused')
  finally:os.close(fd)
 return total,count

def verify_latest_full50_authority(binding):
 """Only exact closed0 upstream facts; no science payload reader or qualification here."""
 import shlex
 selected=binding['actual_latest_full50_authority_pins'];contract=binding['actual_latest_full50_post_contract']
 if set(selected)!=set(('report','Host_freeze','CLI','Root_tools','Root_argv','post_review','post_tools')):raise RuntimeError('seven exact actual upstream authorities')
 if set(contract)!=set(('schema','status','fields'))or not isinstance(contract['schema'],str)or not contract['schema']or not isinstance(contract['status'],str)or not contract['status']or not isinstance(contract['fields'],dict)or set(contract['fields'])!=set(('report','Host_freeze','CLI','Root_tools','Root_argv','ordered50_verified','expected33_verified'))or any(not isinstance(v,str)or not v for v in contract['fields'].values()):raise RuntimeError('exact Source-approved latest full50 post protocol; None refused')
 values={}
 for key,row in selected.items():
  if not isinstance(row,dict)or set(row)!=set(('path','sha256','size_bytes','identity'))or pin(row['path'])!=row:raise RuntimeError('exact selected actual full50 authority fullpin')
  values[key]=json.loads(Path(row['path']).read_text())
 def terminal0(value):
  if not isinstance(value,dict)or type(value.get('exit_code'))is not int or value['exit_code']!=0 or value.get('session_id')is not None:raise RuntimeError('genuine full50 closed integer0/no session')
 report=values['report'];root=values['Root_tools'];argv=values['Root_argv'];post=values['post_review'];pt=values['post_tools'];cli=values['CLI'];hf=values['Host_freeze']
 terminal0(root['actual_terminal_return'])
 if root.get('observed_closed')is not True or type(root.get('original_integer_exit_code'))is not int or root['original_integer_exit_code']!=0 or not isinstance(argv.get('exact_argv'),list)or len(argv['exact_argv'])!=96 or shlex.split(root['exact_executed_command'])!=argv['exact_argv']or root['exact_executed_command']!=argv['exact_command']or cli['exact_reviewable_argv']!=argv['exact_argv']or argv['Host_freeze_pin']!=selected['Host_freeze']or argv['interface_pin']!=selected['CLI']:raise RuntimeError('latest actual full50 Root0/exact96/own HF CLI')
 if report.get('schema')!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or report.get('status')!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or report.get('failure')is not None or report.get('after_check_error')is not None or report.get('engineering_three_plane_closed0')is not True or report.get('all_new_storage_entry_controls_closed')is not True or len(report['records'])!=50 or report['first_failure_secondary_errors']!=[]or type(report.get('SELF_peak_bytes'))is not int or not 0<=report['SELF_peak_bytes']<512*2**20 or type(report.get('wall_seconds'))not in (int,float)or not 0<report['wall_seconds']<1800:raise RuntimeError('actual original complete50 engineering closure; no prior singleBOOT or Source qualification')
 if pt.get('observed_closed')is not True or type(pt.get('original_integer_exit_code'))is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('actual independent full50 post closed0')
 for key in ('actual_review_return','actual_postverification_return'):
  result=pt[key];terminal0(result)
  if json.loads(result['output'].strip().splitlines()[-1])['review_pin']!=selected['post_review']:raise RuntimeError('genuine independent post stdout exact PF')
 if post.get('schema')!=contract['schema']or post.get('status')!=contract['status']or post.get('failure')is not None:raise RuntimeError('exact actual full50 post contract')
 for key in ('report','Host_freeze','CLI','Root_tools','Root_argv'):
  if post[contract['fields'][key]]!=selected[key]:raise RuntimeError('post binds exact actual '+key)
 if post[contract['fields']['ordered50_verified']]is not True or post[contract['fields']['expected33_verified']]is not True:raise RuntimeError('independent actual original50 order and33 exact refusal messages')
 return dict(actual_full50_authority_pins=selected,actual_original50_post_verified=True,qualification_granted_by_saved_source=False)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--freeze-sha256',required=True);parser.add_argument('--freeze-seven-id',required=True)
 args=parser.parse_args();start=time.monotonic()
 if OUT.exists()or OUT.is_symlink()or TMP_OUT.exists()or TMP_OUT.is_symlink():raise RuntimeError('both output namespaces fresh, once, no retry')
 if any(os.environ.get(k)!='1'for k in THREADS)or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None:raise RuntimeError('original one-thread unoptimized unprofiled environment')
 fp=pin(FREEZE)
 if fp['sha256']!=args.freeze_sha256 or fp['identity']!=json.loads(args.freeze_seven_id):raise RuntimeError('Root external exact complete Source freeze fullpin')
 freeze=json.loads(FREEZE.read_text())
 if freeze['schema']!='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V2':raise RuntimeError('exact Source freeze schema')
 verify(freeze['fixed_source_files']);binding=json.loads(BIND.read_text())
 upstream_actual_admission=verify_latest_full50_authority(binding)
 if pin(BIND)!=freeze['input_binding_pin']or pin(Path(__file__).resolve())!=freeze['host_pin']:raise RuntimeError('explicit whole current binding and executed host')
 fixed=binding['fixed_current_pins']+freeze['fixed_source_files']+[fp]
 verify(fixed)
 metadata_reattestation=verify_current_mount_derivation(binding)
 if pin(SUPPORT)['sha256']!=SUPPORT_SHA:raise RuntimeError('original support Source')
 spec=importlib.util.spec_from_file_location('saved_full370_original_support',SUPPORT);support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
 if Path(sys.executable).resolve()!=support.PYTHON:raise RuntimeError('original exact Python')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'saved_full370_original_helper')
 factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'saved_full370_original_resources')
 full,production=helper.modules();guard_files=helper.guard_admission(full)
 if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:raise RuntimeError('original genuine supervisor MRO/Source paths')
 for p in guard_files:
  q=pin(p)
  if q not in fixed:raise RuntimeError('complete original actual guard proof Source/dependency pin')
 manifest=json.loads(Path(binding['science_manifest_pin']['path']).read_text())
 if len(manifest['inputs'])!=1129 or any(next(r for r in binding['science_original_input_pins']if r['path']==p)['sha256']!=sha for p,sha in manifest['inputs'].items()):raise RuntimeError('all1129 exact scientific input SHA')
 prepared=json.loads(Path(binding['formal_prepared_pin']['path']).read_text());case=json.loads(Path(binding['formal_case_spec_pin']['path']).read_text());cfg=prepared['production_config']
 if cfg['rank']!=1 or case['basis']['requested_rank']!=1 or cfg['cells_per_zone']*3!=48 or cfg['sn']!=32 or case['cases']['AAA']!=['A','A','A']:raise RuntimeError('exact formal rank1/48/SN32/AAA inputs')
 if prepared['case_spec']['path']!=binding['formal_case_spec_pin']['path']or prepared['case_spec']['sha256']!=binding['formal_case_spec_pin']['sha256']:raise RuntimeError('formal independently declared case fullbinding')
 history=factory.DynamicHistoryResources(ART,factory.history_roots([str(OUT)],ART),8*2**30,96*2**30,production.ResourceFailure)
 fresh=production.DiskResources(ART,[str(OUT)],8*2**30,2*2**30)
 class Resources:
  def check(self):
   # The original ART monitors retain their true paths and exact caps. They
   # reject out-of-tree roots, so this explicit TMP monitor adds all its bytes
   # to both actual totals and checks both filesystems, without fake aliases.
   h=history.check();f=fresh.check();tb,tc=tmp_inventory()
   if h['artifact_bytes']+tb+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB original cold reserve including actual TMP')
   if f['artifact_bytes']+tb>=2*2**30:raise RuntimeError('whole fresh2GiB includes ART and actual TMP')
   free=min(f['disk_free_bytes'],shutil.disk_usage(TMP_OUT.parent).free)
   if free-20971764748-2*2**30<8*2**30:raise RuntimeError('both filesystems8GiB original reserves')
   if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original SELF512MiB cap')
   if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 cap')
   return dict(h,fresh_output=f,external_TMP_bytes=tb,external_TMP_files=tc,combined_history_bytes=h['artifact_bytes']+tb,combined_fresh_bytes=f['artifact_bytes']+tb,both_filesystems_min_free_bytes=free)
 resources=Resources();before=resources.check()
 if before['combined_history_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:raise RuntimeError('initial full fresh2GiB history reserve')
 command=binding['planned_science_command']
 expected=[str(support.PYTHON),'-B',binding['science_source_pin']['path'],'--manifest',binding['science_manifest_pin']['path'],'--manifest-sha256',binding['science_manifest_pin']['sha256'],'--source-sha256',binding['science_source_pin']['sha256'],'--out',str(TMP_OUT)]
 if command!=expected:raise RuntimeError('exact one complete science command/Source/manifest/output')
 OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'AAA_SAVED_AUDIT').mkdir();shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
 copied=pin(OUT/'runtime/run_bounded_dragon.py');original=pin(support.BOUNDED)
 if copied['sha256']!=original['sha256']or copied['size_bytes']!=original['size_bytes']or copied['identity']==original['identity']:raise RuntimeError('original bounded Source wholebytes with new owned7ID')
 runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA_SAVED_AUDIT',resources)
 if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('real original bounded ownRSS binding')
 write(OUT/'Root_current_saved_full370_binding.json',dict(fixed_current_pins=fixed,actual_commands=[command],owned_runtime_pin=copied,science_output_root=str(TMP_OUT),resources_before=before,workflow_order='Root invokes only after real three-plane publication and online BOOT; this host does not certify upstream',new_state_or_old_qualification_inherited=False))
 failure=after_error=None;after=result=watch=None;outputs=[];preserved=[]
 try:
  verify(fixed);runner.execute(OUT/'AAA_SAVED_AUDIT','saved_terminal_source_all370',command,600);watch=helper.check_watch(OUT,runner.records[-1]);verify(fixed)
  result=json.loads((TMP_OUT/'RESULT.json').read_text())
  if result['classification']!='COMPLETE_SAVED_TERMINAL_THREE_AXIAL_MOMENT_SOURCE_DIAGNOSTIC_ONLY_NDIM3_NINE_MOMENTS_UNREADY'or(result['groups'],result['regions'],result['axial_cells'])!=(370,8,48):raise RuntimeError('full actual370/3moment/48 saved-data result')
  if result['axes']['known_NDIM3_R_indices_0based']!=[0,2,6]or result['axes']['unknown_NDIM3_R_indices_0based']!=[1,3,4,5,7,8]or result['nine_moment_status']!='UNKNOWN_SIX_TRANSVERSE_OR_MIXED_MOMENTS_NOT_OBSERVED; no zero completion, no fitted/angular reconstruction':raise RuntimeError('six genuinely unobserved moments remain UNKNOWN')
  if any(result.get(k)is not False for k in ('full_neutron_balance_qualified','full_eigen_reference_qualified','AAA_qualified','ABA_admitted','original_physics_thresholds_changed'))or result['no_clip_no_drop_no_local_renormalization']is not True or result['child_launch_attempts']!=[]:raise RuntimeError('saved-data diagnostic exact original scope')
  outputs=[pin(p)for p in sorted(TMP_OUT.iterdir())if p.is_file()]
  if sum(p['size_bytes']for p in outputs)>=64*2**20 or(TMP_OUT/'FAILED.json').exists():raise RuntimeError('original actual64MiB scientific result cap/no failure')
  (OUT/'retained_science_result').mkdir()
  for p in outputs:
   target=OUT/'retained_science_result'/Path(p['path']).name;shutil.copy2(p['path'],target);new=pin(target)
   if(new['sha256'],new['size_bytes'])!=(p['sha256'],p['size_bytes'])or new['identity']==p['identity']:raise RuntimeError('retained actual result complete bytes and new7ID')
   preserved.append(dict(actual_TMP_pin=p,retained_pin=new))
  verify(fixed);verify(outputs);after=resources.check()
 except BaseException as error:
  failure=repr(error)
  try:after=resources.check()
  except BaseException as error2:after_error=repr(error2)
 report=dict(schema='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V2',status='ACTUAL_SAVED_FULL370_THREE_AXIAL_MOMENT_DIAGNOSTIC_CLOSED0_ONLY'if failure is None else'FAILED_SAVED_FULL370_DIAGNOSTIC_NO_RETRY',failure=failure,after_check_error=after_error,records=runner.records,fixed_current_pins=fixed,owned_runtime_pin=copied,actual_watchdog_check=watch,actual_result=result,actual_TMP_output_pins=outputs,retained_actual_result_file_origins=preserved,output_pins=[pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],resources_before=before,resources_after=after,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,science_Source_imported_by_host=False,new_three_plane_inputs_audited=False,upstream_three_plane_or_BOOT_qualification_granted_by_host=False,transport_or_eigen_solver_executed=False,full_neutron_balance_qualified=False,full_eigen_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 report['explicit_current_mount_input_reattestation_provenance']=metadata_reattestation
 report['final_report_bytes_in_original_resources']=True
 report['postwrite_cap_PASS_requires_actual_true_closed0']=True
 summary=OUT/'Root_actual_saved_full370_diagnostic_summary.json';write(summary,report);summary_pin=pin(summary)
 try:
  verify(fixed);verify(outputs);resources.check()
 except BaseException as final_error:
  failure=repr(final_error)
  report['status']='FAILED_SAVED_FULL370_DIAGNOSTIC_NO_RETRY';report['failure']=failure
  report['after_check_error']=failure;report['late_postwrite_cap_error']=failure
  report['wall_seconds']=time.monotonic()-start;report['SELF_peak_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  replace_just_created_owned_report(summary,summary_pin,report)
 print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))
 return 0 if failure is None else 1
if __name__=='__main__':raise SystemExit(main())

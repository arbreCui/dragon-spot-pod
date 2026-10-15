#!/usr/bin/env python3
"""Write immutable Source candidates only; never import or run the scientific audit."""
from pathlib import Path
import ast,hashlib,json,os,stat

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=REC/'saved_full370_terminal_audit_host_source_v1'
ORIGINAL=Path('/private/tmp/SPOT_AAA_full370_terminal_source_UNRUN_20261012')
SCIENCE_SHA='2027ec61895902575165869d753926808e882e5233e89c26a3ca9c973408024f'
PLAN_SHA='52821a9171f834eeba17dfddd0a917fc100fd2c98a8760d0528842d21b45e39f'

def sid(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=sid(p.lstat());assert stat.S_ISREG(before[2]),str(p)
 with p.open('rb')as f:
  assert sid(os.fstat(f.fileno()))==before;sha=hashlib.file_digest(f,'sha256').hexdigest();assert sid(os.fstat(f.fileno()))==before
 assert sid(p.lstat())==before
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def write(p,raw):
 if isinstance(raw,dict):raw=(json.dumps(raw,indent=2,allow_nan=False)+'\n').encode()
 if isinstance(raw,str):raw=raw.encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())

HOST='''#!/usr/bin/env python3
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
OUT=ART/'axial-material-AAA-saved-full370-terminal-source-diagnostic-guarded-20261012'
TMP_OUT=Path('/private/tmp/SPOT_AAA_full370_terminal_source_ACTUAL_ONCE_20261012')
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
 with Path(p).open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\\n');f.flush();os.fsync(f.fileno())
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

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--freeze-sha256',required=True);parser.add_argument('--freeze-seven-id',required=True)
 args=parser.parse_args();start=time.monotonic()
 if OUT.exists()or OUT.is_symlink()or TMP_OUT.exists()or TMP_OUT.is_symlink():raise RuntimeError('both output namespaces fresh, once, no retry')
 if any(os.environ.get(k)!='1'for k in THREADS)or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None:raise RuntimeError('original one-thread unoptimized unprofiled environment')
 fp=pin(FREEZE)
 if fp['sha256']!=args.freeze_sha256 or fp['identity']!=json.loads(args.freeze_seven_id):raise RuntimeError('Root external exact complete Source freeze fullpin')
 freeze=json.loads(FREEZE.read_text())
 if freeze['schema']!='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V1':raise RuntimeError('exact Source freeze schema')
 verify(freeze['fixed_source_files']);binding=json.loads(BIND.read_text())
 if pin(BIND)!=freeze['input_binding_pin']or pin(Path(__file__).resolve())!=freeze['host_pin']:raise RuntimeError('explicit whole current binding and executed host')
 fixed=binding['fixed_current_pins']+freeze['fixed_source_files']+[fp]
 verify(fixed)
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
 report=dict(schema='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V1',status='ACTUAL_SAVED_FULL370_THREE_AXIAL_MOMENT_DIAGNOSTIC_CLOSED0_ONLY'if failure is None else'FAILED_SAVED_FULL370_DIAGNOSTIC_NO_RETRY',failure=failure,after_check_error=after_error,records=runner.records,fixed_current_pins=fixed,owned_runtime_pin=copied,actual_watchdog_check=watch,actual_result=result,actual_TMP_output_pins=outputs,retained_actual_result_file_origins=preserved,output_pins=[pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],resources_before=before,resources_after=after,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,science_Source_imported_by_host=False,new_three_plane_inputs_audited=False,upstream_three_plane_or_BOOT_qualification_granted_by_host=False,transport_or_eigen_solver_executed=False,full_neutron_balance_qualified=False,full_eigen_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(OUT/'Root_actual_saved_full370_diagnostic_summary.json',report);print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))
 return 0 if failure is None else 1
if __name__=='__main__':raise SystemExit(main())
'''

def main():
 assert not BASE.exists();BASE.mkdir()
 s=ORIGINAL/'audit_saved_terminal_source_all370.py';p=ORIGINAL/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json'
 sp=pin(s);pp=pin(p);assert sp['sha256']==SCIENCE_SHA and pp['sha256']==PLAN_SHA
 ast.parse(s.read_text());raw=p.read_bytes();plan=json.loads(raw);assert len(plan['inputs'])==1129
 write(BASE/s.name,s.read_bytes());science=pin(BASE/s.name)
 old_literal=('"source": {\n    "path": "'+str(s)+'",').encode();new_literal=('"source": {\n    "path": "'+str(BASE/s.name)+'",').encode();assert raw.count(old_literal)==1
 rebound=raw.replace(old_literal,new_literal);assert rebound.replace(new_literal,old_literal)==raw
 write(BASE/p.name,rebound);manifest=pin(BASE/p.name)
 rows=[]
 for path,sha in plan['inputs'].items():
  row=pin(path);assert row['sha256']==sha;rows.append(row)
 prepared=next(row for row in rows if Path(row['path']).name=='prepared.json');d=json.loads(Path(prepared['path']).read_text());case=pin(d['case_spec']['path']);assert case['sha256']==d['case_spec']['sha256'];cs=json.loads(Path(case['path']).read_text())
 assert d['production_config']['rank']==cs['basis']['requested_rank']==1 and d['production_config']['sn']==32 and d['production_config']['cells_per_zone']*3==48
 old_bind=REC/'native_warm_A2_A3_bounded_host_source_v2/CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json';old=json.loads(old_bind.read_text())
 fixed={}
 for row in rows+old['fixed_current_pins']+[science,manifest,sp,pp,case,pin(Path(__file__).resolve()),pin(old_bind),pin(ORIGINAL/'PARSER_SOURCE_PROOF.json'),pin(ORIGINAL/'SCIENTIFIC_REVIEW_AND_SOURCE_ONLY_HANDOFF.txt'),pin(ROOT/'validation/axial_material/refined_AAA_full_group_source_reaction_ledger_diagnostic_20261010.py'),pin('/bin/ps')]:
  row={k:row[k]for k in ('path','sha256','size_bytes','identity')};assert pin(row['path'])==row
  if row['path']in fixed:assert fixed[row['path']]==row
  fixed[row['path']]=row
 host=BASE/'run_actual_saved_full370_terminal_source_original_guard.py';ast.parse(HOST);write(host,HOST);fixed[str(host)]=pin(host)
 python=pin('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12');fixed[python['path']]=python
 command=[python['path'],'-B',science['path'],'--manifest',manifest['path'],'--manifest-sha256',manifest['sha256'],'--source-sha256',science['sha256'],'--out','/private/tmp/SPOT_AAA_full370_terminal_source_ACTUAL_ONCE_20261012']
 binding=dict(schema='CURRENT_SAVED_FULL370_TERMINAL_SOURCE_ORIGINAL_GUARD_INPUT_BINDING_V1',fixed_current_pins=[fixed[x]for x in sorted(fixed)],science_original_input_pins=rows,science_source_pin=science,science_manifest_pin=manifest,original_science_source_pin=sp,original_input_plan_pin=pp,formal_prepared_pin=prepared,formal_case_spec_pin=case,planned_science_command=command,requires_host_process_metadata_access=True,Source_only=True,candidate_imported_or_executed=False,workflow_order='Root must first close true three-plane publication and online BOOT before execution',original_guard_and_ART_resources_not_modified=True,TMP_nofollow_bytes_added_to_actual_history_and_fresh_totals=True,mathematics_or_thresholds_or_input_SHA_changed=False,AAA_qualified=False,ABA_admitted=False)
 bp=BASE/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json';write(bp,binding)
 proof=dict(schema='SOURCE_ONLY_DURABLE_SCIENCE_AND_MANIFEST_LITERAL_REBIND_PROOF_V1',original_source=sp,new_source=science,science_Source_wholebytes_identical=s.read_bytes()==(BASE/s.name).read_bytes(),original_plan=pp,new_plan=manifest,old_literal=old_literal.decode(),new_literal=new_literal.decode(),literal_count=1,fullbyte_reverse_equal=True,inputs_exactly_unchanged=json.loads(rebound)['inputs']==plan['inputs'],actual_full_EOF_SHA_and_current7ID_matching_inputs=len(rows),total_input_bytes=sum(x['size_bytes']for x in rows),source_review_tools=['72ff51 EXIT0 all1129 actual SHA/7ID','8f1b18 EXIT0 four complete reader definitions literal equal','5dfb76 EXIT0 complete1110/19 index and syntax'],candidate_imported_or_executed=False,original_Source_and_inputs_unmodified=True,host_pin=pin(host),binding_pin=pin(bp),original_old_frozen_warm_runtime_closure_pin=pin(old_bind),guard_scope='original genuine OwnRSS class/MRO; original ART monitors plus explicit outside-ART TMP accounting, both filesystem floors, no fake aliases',AAA_qualified=False)
 pr=BASE/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_DERIVATION.json';write(pr,proof)
 print(json.dumps(dict(status='FULL370_SAVED_DIAGNOSTIC_HOST_SOURCE_WRITTEN_UNRUN',host=pin(host),binding=pin(bp),proof=pin(pr),science=science,manifest=manifest,source_imported_or_science_executed=False)))
if __name__=='__main__':main()

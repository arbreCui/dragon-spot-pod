import ast, hashlib, json, os, stat, time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
AUTHOR=Path(__file__).resolve().parent
SOURCE=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_source_v1'
ORIGINAL=REC/'aaa_three_plane_streaming_pipeline_source_v11'
OLDOUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
NEWOUT=OLDOUT.parent/'axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v1'
START=time.monotonic();ALL={};checks=0

def pin(path,wanted=None):
 global checks
 p=Path(path);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(i[2])and not any(x.is_symlink()for x in(p,*p.parents))
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
  h=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
 s=p.lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
 v=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
 if wanted is not None:assert v==wanted,(str(p),'currentPF differs')
 assert str(p)not in ALL or ALL[str(p)]==v
 ALL[str(p)]=v;checks+=1;return v

def write(path,value):
 with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

hostpath=ORIGINAL/'run_actual_three_plane_pipeline.py';host=hostpath.read_text();tree=ast.parse(host)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
lines=host.splitlines(keepends=True)
def textnode(n):return ''.join(lines[n.lineno-1:n.end_lineno])
phase=textnode(next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources'))
nested={n.name:textnode(n)for n in main.body if isinstance(n,ast.FunctionDef)}
fragment=host[host.index("    hf,phf=ext(args,'host_freeze')"):host.index('    resources=PhaseResources(base_resources)')]
# Preserve full original scientific/metadata admission; owning Source predicate
# refers to original v11 Source, because this is a distinct diagnostic host.
adapted=fragment.replace('Path(__file__).resolve()', 'ORIGINAL_HOST.resolve()').replace('c.same_pin(__file__,hf[\'host_source\'])','c.same_pin(ORIGINAL_HOST,hf[\'host_source\'])')
assert adapted.count('ORIGINAL_HOST')==2
milestones=[("    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)\n", "    checkpoint('original_Common_initialize_complete')\n"),
("    c.verify_rows(build['fixed_current_pins']);c.verify_rows(build['output_pins'])\n", "    checkpoint('actual70_full_metadata_admitted')\n"),
("    c.verify_rows(current69['fixed_current_pins']);c.verify_rows(current69['output_pins'])\n", "    checkpoint('current69_full_metadata_admitted')\n"),
("    c.verify_rows(original69['fixed_current_pins']);c.verify_rows(original69['output_pins'])\n", "    checkpoint('original69_full_metadata_admitted')\n"),
("    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)\n", "    checkpoint('current17_full_metadata_admitted')\n"),
("    for row in producer_reports:c.closed_report(row,helper,Path(row['actual_output_pin']['path']).parent.parent,4)\n", "    checkpoint('three_independent_producer_reports_admitted')\n"),
("    c.verify_rows(fixed)\n", "    checkpoint('all_original_fixed_PF_admitted_before_metadata_close')\n"),
("    gc.collect()\n", "    checkpoint('original_v11_metadata_lifetime_close_and_single_GC')\n")]
for old,addition in milestones:assert adapted.count(old)==1;adapted=adapted.replace(old,old+addition)
reverse=adapted
for old,addition in reversed(milestones):reverse=reverse.replace(old+addition,old)
reverse=reverse.replace('ORIGINAL_HOST.resolve()', 'Path(__file__).resolve()').replace('c.same_pin(ORIGINAL_HOST,hf[\'host_source\'])','c.same_pin(__file__,hf[\'host_source\'])')
assert reverse==fragment
cli_path=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json';cli=json.loads(cli_path.read_text());oldhf=json.loads((ORIGINAL/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').read_text())
rawpath=OLDOUT/'Root_actual_complete_execution_record_before_final_publication.json';raw=json.loads(rawpath.read_bytes());stagepath=OLDOUT/'AAA3-streaming/stages.json';stages=json.loads(stagepath.read_bytes())
assert len(raw['records'])==45 and stages=={'stages':raw['records']} and len(raw['owned_runtime_pins'])==163
inputs=[]
for name in ['projected_boot.xsm','ax_current.xsm','axial_track.xsm','initial_system.xsm','axial_macro.xsm','global_rcon.xsm','radial1.bin','radial2.bin','radial3.bin','pair_rank_type.x2m']:
 p=OLDOUT/'AAA'/name;row=next(x for x in raw['owned_runtime_pins']if x['path']==str(p));inputs.append(dict(role='exact_original_rank_type_deck'if name.endswith('.x2m')else'current_readonly_data',destination_name=name,source_pin=pin(p,row)))
for name in ['Dragon','run_bounded_dragon.py']:
 p=OLDOUT/'runtime'/name;row=next(x for x in raw['owned_runtime_pins']if x['path']==str(p));inputs.append(dict(role='original_runtime',destination_name=name,source_pin=pin(p,row)))
assert sum(x['source_pin']['size_bytes']for x in inputs)==812951170
assert inputs[9]['source_pin']['sha256']=='15b9e6d5694f1cead5b7c71cd24fad872f853d9739fa92e258d19f57dce2164f'
rawpin=pin(rawpath);stagepin=pin(stagepath)
commonpin=pin(REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py')
datapin=pin(ORIGINAL/'actual_inputs_and_readback.py')
SOURCE.mkdir(exist_ok=True)
header='''#!/usr/bin/env python3
"""One diagnostic pretransport rejection, only after explicit Root authorization.

The first45 records are unmodified historical evidence, never reexecuted. Only
one new original executor stage may run. Original classes, limits, serializer,
resource snapshots and real SELF peak remain intact. No physics qualification.
"""
import argparse, gc, hashlib, importlib.util, json, os, resource, shutil, stat
import subprocess, sys, threading, time
from pathlib import Path
sys.dont_write_bytecode=True
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=REC/'aaa_three_plane_streaming_pipeline_source_v11'
ORIGINAL_HOST=HERE/'run_actual_three_plane_pipeline.py'
OUT=Path(OUT_LITERAL)
WORK=OUT/'AAA';MI=2**20
START=time.monotonic();SAMPLES=[];MONITOR_ERRORS=[];CAP_OBSERVATIONS=[]
STOP=threading.Event();LOCK=threading.Lock();PHASE='source_admission'

def bootstrap_pin(path,wanted):
 p=Path(path);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if not stat.S_ISREG(i[2])or any(x.is_symlink()for x in(p,*p.parents)):raise RuntimeError('regular non-symlink source')
 with p.open('rb')as f:
  s=os.fstat(f.fileno())
  if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=i:raise RuntimeError('opened source7ID')
  h=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
  if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=i:raise RuntimeError('source fullEOF7ID')
 if i!=[p.lstat().st_dev,p.lstat().st_ino,p.lstat().st_mode,p.lstat().st_nlink,p.lstat().st_size,p.lstat().st_mtime_ns,p.lstat().st_ctime_ns]:raise RuntimeError('source after7ID')
 actual=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
 if actual!=wanted:raise RuntimeError('exact Source bootstrap PF')
 return actual

def verified_module(wanted,name):
 bootstrap_pin(wanted['path'],wanted);spec=importlib.util.spec_from_file_location(name,wanted['path'])
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
 bootstrap_pin(wanted['path'],wanted);return obj

c=verified_module(COMMON_LITERAL,'single_diagnostic_original_Common')
data=verified_module(DATA_LITERAL,'single_diagnostic_original_data')

def measurement(label):
 ps=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
 if ps.returncode or not ps.stdout.strip().isdigit():raise RuntimeError('real parent current RSS unavailable')
 sample=dict(phase=label,elapsed_seconds=time.monotonic()-START,
  current_RSS_bytes=int(ps.stdout.strip())*1024,ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  allocated_blocks=sys.getallocatedblocks(),gc_count=list(gc.get_count()))
 with LOCK:
  if len(SAMPLES)>=10000:raise RuntimeError('finite telemetry capacity reached')
  SAMPLES.append(sample)
  if sample['ru_maxrss_bytes']>=512*MI or sample['elapsed_seconds']>=1800:
   CAP_OBSERVATIONS.append(sample)
 return sample

def checkpoint(label):
 global PHASE
 with LOCK:PHASE=label
 value=measurement(label)
 if CAP_OBSERVATIONS:raise RuntimeError('original SELF512 or whole1800 diagnostic ceiling reached')
 if MONITOR_ERRORS:raise RuntimeError('real parent monitoring unavailable: '+MONITOR_ERRORS[0])
 return value

def telemetry():
 while not STOP.wait(.2):
  try:
   with LOCK:label=PHASE
   measurement(label)
   if CAP_OBSERVATIONS:break
  except BaseException as exc:
   MONITOR_ERRORS.append(type(exc).__name__+': '+str(exc));break

def ext(args,prefix):
 return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))

def unique(rows):
 out={}
 for row in rows:
  if row['path']in out and out[row['path']]!=row:raise RuntimeError('inconsistent independent full pins')
  out[row['path']]=row
 return list(out.values())

'''.replace('OUT_LITERAL',repr(str(NEWOUT))).replace('COMMON_LITERAL',repr(commonpin)).replace('DATA_LITERAL',repr(datapin))
# Exact original admission lives in its own function, with small retained state
# returned explicitly. Parent long-lived closures contain no closed report.
admit="def admit_original_v11(args,start):\n"+adapted+'''    return dict(fixed=fixed,hf=hf,phf=phf,support=support,helper=helper,full=full,
      base_resources=base_resources,before=before,plan=plan,direct_binding=direct_binding,
      exe=exe,compiler=compiler,includes=includes,archives=archives,bounded_sha256=bounded_sha256,
      link_command=link_command,direct_original_inputs=direct_original_inputs)

'''
# Original functions are nested in diagnostic main. retain's extra source-inode
# check is implemented in wrapper before invoking its unmodified body.
function_names=['stable','retain','copy','clean_driver_scratch_before','stash_closed_driver_scratch']
functions=''.join(''.join(line[2:]if line.strip()else line for line in nested[x].splitlines(keepends=True))for x in function_names)
# stable originally uses fixed/owned. Add separate historical/diagnostic checks
# without changing original function itself via fixed list bound in this main.
suffix='''
def main():
 global PHASE
 p=argparse.ArgumentParser()
 for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze','diagnostic-freeze']:
  for suffix in ['summary','sha256','seven-id']:p.add_argument('--'+prefix+'-'+suffix,required=True)
 args=p.parse_args();start=START
 first_error=None;after_errors=[];child_error=None;runner=None;owned=[];scratch_ledger=[]
 retained_state=None;historical_raw=None;historical_current_owned=[];refusal=None
 final_all7_completed=False;report_pin=None;publication_error=None;authority=None;dh=None
 monitor=threading.Thread(target=telemetry,name='readonly-parent-memory-monitor',daemon=True);monitor.start()
 try:
  checkpoint('diagnostic_Source_entry')
  dh,dhpin=ext(args,'diagnostic_freeze')
  if dh['schema']!='SINGLE_ORIGINAL_PAIR_RANK_TYPE_PRETRANSPORT_DIAGNOSTIC_HOST_FREEZE_V1' or dh['host_source']['path']!=str(Path(__file__).resolve()):raise RuntimeError('exact diagnostic Source freeze')
  c.same_pin(__file__,dh['host_source']);c.verify_rows(dh['source_files']);c.verify_rows(dh['dependencies'])
  for name,expected in dh['original_v11_external_bindings'].items():
   key=name.replace('-','_')
   if [getattr(args,key+'_summary'),getattr(args,key+'_sha256'),json.loads(getattr(args,key+'_seven_id'))]!=[expected['path'],expected['sha256'],expected['identity']]:raise RuntimeError('all seven original external fullpins required unchanged')
  authority,checked=c._read_current_json_exact(dh['input_authority_pin']['path'],dh['input_authority_pin'])
  if checked!=dh['input_authority_pin']:raise RuntimeError('exact input authority')
  checkpoint('complete_diagnostic_Source_and_current_inputs_full_EOF')
  retained_state=admit_original_v11(args,start)
  original_fixed=retained_state['fixed'];hf=retained_state['hf'];support=retained_state['support'];full=retained_state['full']
  historical_raw,rp=c._read_current_json_exact(authority['old_raw_record_pin']['path'],authority['old_raw_record_pin'])
  old_ledger,lp=c._read_current_json_exact(authority['old_stage_ledger_pin']['path'],authority['old_stage_ledger_pin'])
  if len(historical_raw['records'])!=45 or old_ledger!={'stages':historical_raw['records']} or historical_raw['fixed_current_pins']!=original_fixed:raise RuntimeError('true unmodified old45 and original full fixed2643 required')
  if historical_raw['engineering_three_plane_closed0']is not False or historical_raw['actual_terminal']is not None or historical_raw['failure']!='RuntimeError: original SELF 512MiB cap':raise RuntimeError('historical failed v11 may not become success')
  historical_current_owned=historical_raw['owned_runtime_pins']
  if len(historical_current_owned)!=163:raise RuntimeError('complete true original current owned163')
  c.verify_rows(historical_current_owned)
  del old_ledger
  # Keep genuine raw45 and the original runtime collections, sharing those
  # objects. No extra giant decoded ledger is retained or requalified.
  retained_state.update(proofs=historical_raw['actual_complete_readback_proofs'],
   cases=historical_raw['actual_operator_refusals'],private_release_ledger=historical_raw['actual_private_release_ledger'],
   scratch=historical_raw['actual_closed_CLE_scratch_archival_ledger'],
   direct_alias_build=historical_raw['actual_direct_alias_build'],
   direct_alias_case_names=historical_raw['actual_direct_structural_alias_control_names'],
   forecast=authority['original_storage_forecast'])
  checkpoint('historical_raw45_full_runtime_state_and_owned163_live')
  # Original Source code stable/retain/copy/stash below uses a fixed namespace
  # binding consisting of original fixed2643 plus explicit diagnostic pins and
  # historical current-owned inputs. Historical rows remain separately reported.
  fixed=unique(original_fixed+historical_current_owned+dh['dependencies']+dh['source_files']+[dhpin,dh['host_source']])
  resources=PhaseResources(retained_state['base_resources']);resources.phase='BOOT_storage_controls'
  OUT.mkdir();(OUT/'runtime').mkdir();WORK.mkdir();(OUT/'AAA3-streaming').mkdir()
  # The runtime is exact genuine current70, not compiled or altered here.
  for entry in authority['inputs']:
   if entry['role']!='original_runtime':continue
   checkpoint('copy_runtime_'+entry['destination_name'])
   source=entry['source_pin'];destination=OUT/'runtime'/entry['destination_name']
   c.same_pin(source['path'],source);shutil.copy2(source['path'],destination);actual=c.pin(destination)
   if actual['sha256']!=source['sha256']or actual['size_bytes']!=source['size_bytes']or actual['identity'][3]!=1 or any(actual['identity'][:2]==x['identity'][:2]for x in fixed):raise RuntimeError('exact runtime independent physical inode')
   owned.append(actual);c.check_full_current(fixed,owned);resources.check();checkpoint('copied_runtime_'+entry['destination_name'])
  if next(x for x in owned if Path(x['path']).name=='Dragon')['sha256']!=retained_state['exe']['sha256']or next(x for x in owned if Path(x['path']).name=='run_bounded_dragon.py')['sha256']!=retained_state['bounded_sha256']:raise RuntimeError('original admitted current70 and bounded runtime bytes')
  runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA3-streaming',resources)
  if type(runner)is not full.OwnRSSSerialExecutor or full.OwnRSSSerialExecutor.__bases__!=(runner.__class__.__bases__[0],)or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('genuine original supervisor and runtime binding')
  # Exact old rows remain shared and untouched; append affects this shallow list
  # only. They are historical baseline, never new stages or new PASS claims.
  runner.records=list(historical_raw['records'])
FUNCTIONS_LITERAL
  for entry in authority['inputs']:
   if entry['role']=='original_runtime':continue
   checkpoint('copy_input_'+entry['destination_name']);copy(entry['source_pin'],entry['destination_name']);checkpoint('copied_input_'+entry['destination_name'])
  deck=WORK/'pair_rank_type.x2m'
  if c.pin(deck)['sha256']!=authority['exact_original_deck_pin']['sha256']or deck.read_bytes()!=Path(authority['exact_original_deck_pin']['path']).read_bytes():raise RuntimeError('original deck bytes unchanged')
  if any(len(line.rstrip())>120 for line in deck.read_text().splitlines()):raise RuntimeError('unchanged CLE line width')
  stable();clean_driver_scratch_before();checkpoint('immediately_before_one_original_execute_full46_serializer')
  try:
   runner.execute(WORK,'pair_rank_type',[str(OUT/'runtime/Dragon')],600,deck=deck.name)
  except BaseException as exc:
   child_error=type(exc).__name__+': '+str(exc)
  checkpoint('original_execute_and_final_full46_dump_returned')
  if len(runner.records)!=46 or runner.records[:45]!=historical_raw['records']:raise RuntimeError('old45 unchanged, only one new actual stage')
  stash_closed_driver_scratch('pair_rank_type');checkpoint('original_same_inode_scratch_archival_complete')
  record=runner.records[45];wp=WORK/'pair_rank_type.watchdog.json';lp=WORK/'pair_rank_type.log'
  w=json.loads(wp.read_text());text=lp.read_text()
  if child_error!='RuntimeError: own-child stage failed; no retry' or record['status']!='FAILED' or record.get('error')!='own-child stage failed; no retry' or type(w['returncode'])is not int or w['returncode']!=1 or w['limit_failure']is not None:raise RuntimeError('exact one intended original child refusal required')
  forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1','ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE','SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
  if text.count(authority['expected_abort'])!=1 or any(x in text for x in forbidden):raise RuntimeError('exact abort once and no positive transport/solver trace')
  if w['command']!=record['command'] or w['command']!=[str(OUT/'runtime/Dragon')] or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or w['rss_cap_mib']!=512 or not 0<=w['sampled_peak_rss_mib']<512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True:raise RuntimeError('original actual watchdog limits and closed group')
  # Independent actual liveness readback; no group cleanup is presumed merely
  # from an unexamined report. The original finish_liveness_watchdog already ran.
  groups=subprocess.run(['/bin/ps','-axo','pid=,pgid='],capture_output=True,text=True,timeout=2)
  if groups.returncode or any(int(line.split()[1])==w['pid']for line in groups.stdout.splitlines()if len(line.split())==2):raise RuntimeError('original child process group remains live')
  dumped=json.loads(runner.stages_path.read_text())
  if dumped!={'stages':runner.records}:raise RuntimeError('original full46 ledger differs from actual runner records')
  del dumped
  for entry in authority['inputs']:
   target=OUT/'runtime'/entry['destination_name']if entry['role']=='original_runtime'else WORK/entry['destination_name']
   actual=next(x for x in owned if x['path']==str(target));c.same_pin(target,actual)
   if actual['sha256']!=entry['source_pin']['sha256']or actual['size_bytes']!=entry['source_pin']['size_bytes']:raise RuntimeError('owned readonly input complete byte readback')
  stable();checkpoint('all_current_Source_original_inputs_old163_and_new_copies_fullEOF_closed')
  final_all7_completed=True
  refusal=dict(case='pair_rank_type',expected_abort=authority['expected_abort'],actual_exit_code=1,
   original_execution_record_index=45,original_execution_record_label=record['label'],
   actual_abort_message_exact=True,all_actual_assertions_completed=True,
   no_positive_solver_or_seal_trace=True,pre_transport_abort_at_frozen_validation_branch=True,
   actual_log_pin=c.pin(lp),actual_watchdog_pin=c.pin(wp),original_full46_ledger_pin=c.pin(runner.stages_path))
 except BaseException as exc:
  first_error=type(exc).__name__+': '+str(exc)
 finally:
  # Preserve the first exception before attempting further checks/publication.
  # These checks can fail separately; neither can replace the primary cause.
  if retained_state is not None:
   try:
    c.verify_rows(retained_state['fixed']);c.verify_rows(historical_current_owned);c.verify_rows(owned)
    if dh is not None:c.verify_rows(dh['dependencies']);c.verify_rows(dh['source_files']);c.same_pin(__file__,dh['host_source'])
    retained_state['base_resources'].check()
    if 'resources'in locals():resources.check()
    checkpoint('failure_or_success_final_fullEOF_resource_SELF_whole_guard')
   except BaseException as exc:after_errors.append(type(exc).__name__+': '+str(exc))
  STOP.set();monitor.join(timeout=3)
  if monitor.is_alive():MONITOR_ERRORS.append('readonly monitor did not close')
  outputs=[]
  if OUT.exists():
   for path in sorted(OUT.rglob('*')):
    if path.is_file()and not path.is_symlink():
     try:outputs.append(c.pin(path))
     except BaseException as exc:after_errors.append('output pin '+str(path)+': '+type(exc).__name__+': '+str(exc))
  status='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY'if first_error is None and not after_errors and not MONITOR_ERRORS and not CAP_OBSERVATIONS and final_all7_completed else'SINGLE_PRETRANSPORT_DIAGNOSTIC_FAILED_EVIDENCE_RETAINED'
  report=dict(schema='ACTUAL_SINGLE_ORIGINAL_PAIR_RANK_TYPE_COMBINATION_MEMORY_DIAGNOSTIC_V1',status=status,
   primary_error=first_error,after_check_errors=after_errors,monitor_errors=MONITOR_ERRORS,child_execute_error=child_error,
   cap_observations=CAP_OBSERVATIONS,wall_seconds=time.monotonic()-START,
   SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,measurements=SAMPLES,
   old45_only_historical_baseline=True,old45_reexecuted=False,old45_counted_as_new_PASS=False,
   original_historical_raw45_pin=None if authority is None else authority['old_raw_record_pin'],
   original_historical_stage45_pin=None if authority is None else authority['old_stage_ledger_pin'],
   old45_prefix_unchanged=runner is not None and historical_raw is not None and runner.records[:45]==historical_raw['records'],
   new_actual_stage_count=0 if runner is None else len(runner.records)-45,
   new_actual_stage_indices=[]if runner is None else list(range(45,len(runner.records))),
   new_actual_refusal=refusal,exact_original_guard_class_MRO_serializer_rusage_unmodified=True,
   original_limit_values=dict(child_stage_seconds=600,whole_seconds=1800,SELF_bytes=512*MI,child_rss_mib=512,
    history_bytes=96*2**30,fresh_bytes=2*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*MI,min_free_bytes=8*2**30),
   final_all7_completed=final_all7_completed,historical_current_owned_pins=historical_current_owned,
   new_owned_copy_and_archival_pins=owned,observed_existing_outputs_before_receipt=outputs,
   originals_and_owned_copies_deleted=False,owned_copies_retained_for_separate_exact_release=True,
   original_v11_closed50_succeeded=False,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
  if OUT.exists():
   report_path=OUT/'DIAGNOSTIC_REVIEW.json'
   try:
    # Exclusive, owned same FD failure publication. Guard failures after this
    # write are reported truthfully without losing the original primary error.
    fd=os.open(report_path,os.O_CREAT|os.O_EXCL|os.O_RDWR|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w+',encoding='utf-8')as stream:
     json.dump(report,stream,indent=2,allow_nan=False);stream.write('\\n');stream.flush();os.fsync(stream.fileno())
     initial=os.fstat(stream.fileno());initial_id=[initial.st_dev,initial.st_ino,initial.st_mode,initial.st_nlink]
     try:
      c.check_full_current(retained_state['fixed']+historical_current_owned,owned)
      retained_state['base_resources'].check()
      if 'resources'in locals():resources.check()
      if time.monotonic()-START>=1800:raise RuntimeError('original whole1800 elapsed cap after publication')
      if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*MI:raise RuntimeError('original SELF512 cap after publication')
     except BaseException as exc:
      after_errors.append('after report write: '+type(exc).__name__+': '+str(exc));report['status']='SINGLE_PRETRANSPORT_DIAGNOSTIC_FAILED_EVIDENCE_RETAINED'
      report['after_check_errors']=after_errors;report['SELF_peak_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;report['wall_seconds']=time.monotonic()-START
      current=report_path.lstat()
      if [current.st_dev,current.st_ino,current.st_mode,current.st_nlink]!=initial_id or current.st_nlink!=1:raise RuntimeError('same owned report FD/path identity changed')
      stream.seek(0);stream.truncate(0);json.dump(report,stream,indent=2,allow_nan=False);stream.write('\\n');stream.flush();os.fsync(stream.fileno())
     final=os.fstat(stream.fileno());pathstat=report_path.lstat()
     if [final.st_dev,final.st_ino,final.st_mode,final.st_nlink]!=initial_id or [pathstat.st_dev,pathstat.st_ino,pathstat.st_mode,pathstat.st_nlink]!=initial_id:raise RuntimeError('same FD final publication identity changed')
    report_pin=c.pin(report_path)
   except BaseException as exc:publication_error=type(exc).__name__+': '+str(exc)
  print(json.dumps(dict(status=report['status'],primary_error=first_error,after_check_errors=after_errors,
    monitor_errors=MONITOR_ERRORS,publication_error=publication_error,actual_report_pin=report_pin,
    new_actual_stage_count=report['new_actual_stage_count'],old45_historical_only=True,
    actual_v11_qualified=False,AAA_qualified=False,ABA_admitted=False),allow_nan=False),flush=True)
  # Exit is based on every true error. The original expected child refusal alone
  # is evidence; a first admission/stash/guard/publication error is never masked.
  if report['status']!='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY'or publication_error is not None:raise SystemExit(1)

if __name__=='__main__':main()
'''.replace('FUNCTIONS_LITERAL',functions.rstrip())
script=header+phase+'\n'+admit+suffix
ast.parse(script)
scriptpath=SOURCE/'run_single_pair_rank_type_memory_diagnostic.py';scriptpath.write_text(script)
authority=dict(schema='CURRENT_V11_SINGLE_PRETRANSPORT_DIAGNOSTIC_INPUT_AUTHORITY_V1',inputs=inputs,old_raw_record_pin=rawpin,old_stage_ledger_pin=stagepin,
 expected_abort='SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.',exact_original_deck_pin=inputs[9]['source_pin'],original_storage_forecast=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='STORAGE_FORECAST'for x in n.targets)))if False else json.loads((REC/'independent_v11_combined_bounded_transfer_memory_fixture_20261013/combined-current-readback/REVIEW.json').read_text()).get('original_storage_forecast',{}))
# Preserve the complete original forecast literal via a standalone static AST
# evaluation in a safe literal namespace (no imports/business/candidate call).
forecastnode=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='STORAGE_FORECAST'for x in n.targets))
env={'MI':2**20};exec(compile(ast.Module(body=[forecastnode],type_ignores=[]),'<original literal forecast>','exec'),env);authority['original_storage_forecast']=env['STORAGE_FORECAST']
write(SOURCE/'INPUT_AUTHORITY.json',authority)
write(SOURCE/'COMPLETE_ORIGINAL_FRAGMENT_BYTE_INVERSE.json',dict(schema='DIAGNOSTIC_ADMISSION_AND_ORIGINAL_GUARD_FRAGMENT_EXACT_BYTE_INVERSE_V1',original_host_pin=pin(hostpath),original_admission=fragment,diagnostic_admission=adapted,exact_inverse_recovered_original=True,
 admission_exact_owner_replacements=[['Path(__file__).resolve()','ORIGINAL_HOST.resolve()'],["c.same_pin(__file__,hf['host_source'])","c.same_pin(ORIGINAL_HOST,hf['host_source'])"]],monitor_only_insertions=milestones,
 original_PhaseResources_complete_text=phase,diagnostic_PhaseResources_complete_text=phase,original_nested_functions={x:nested[x]for x in ['stable','retain','copy','clean_driver_scratch_before','stash_closed_driver_scratch']},
 nested_functions_only_uniform_leading_indent_minus_two_spaces=True,diagnostic_nested_functions_complete_text=functions,original_classes_MRO_serializer_guard_not_modified=True))
plan=dict(schema='SINGLE_PRETRANSPORT_COMBINATION_MEMORY_DIAGNOSTIC_SOURCE_ONLY_PLAN_V1',planned_output=str(NEWOUT),stage='pair_rank_type',actual_new_stages=1,unmodified_historical_prefix_count=45,new_stage_index=45,
 old45_status_labels_commands_resources_never_modified=True,old45_not_reexecuted_or_new_PASS=True,parent_original_dump_writes_complete46=True,baseline_keep='all original admitted small state, current catalogue, fixed2643, oldowned163 separately, genuine raw45 and shared proofs/cases/releases/scratch/directaliases',
 exact_deck_includes=['RECOVER three PROJECT items','MACRO0 copies','three ASM','RANK 1.0 exact validation refusal'],refusal_before_positive_transport_required=True,
 new_physical_input_scope=inputs,base_input_bytes=812951170,nonPROJECT_input_bytes=63595218,nonPROJECT_planning_room_before_evidence_bytes=70622510,
 original_caps_unchanged=dict(whole_seconds=1800,stage_seconds=600,SELF_MiB=512,child_MiB=512,fresh_GiB=2,history_GiB=96,cold_bytes=20971764748,metadata_MiB=64,minfree_GiB=8,remaining_MiB=128,PROJECT_MiB=800),
 no_SOURCE_class_MRO_serializer_rusage_guard_patch=True,no_positive_BOOT_or_GLOBAL_or_numerical_retry=True,owned_inputs_kept_until_later_independent_exact_release=True,original_inputs_never_deleted=True,
 monitor='readonly .2 second thread real parent ps RSS, RUSAGE_SELF peak never reset, allocated blocks; phase boundaries admission/copy/original_execute+2dumps/stash/finalEOF/publication; no resource snapshot alteration',
 future_actual_report_pin=None,Source_prepared_only=True,actual_executed=False,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(SOURCE/'PLAN_SOURCE_ONLY.json',plan)
# Every currently live original raw-fixed and historical-current-owned row is
# protected. Released old raw proofs remain historical, not current PF claims.
deps=raw['fixed_current_pins']+raw['owned_runtime_pins']+oldhf['dependencies']+[pin(ORIGINAL/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),pin(cli_path),rawpin,stagepin,commonpin,datapin]
for name in ['ACTUAL_PIPELINE_V11_TRUE_TOOL_RETURNS_20261013.json','ACTUAL_PIPELINE_V11_PARENT_SELF_MEMORY_REFUSAL_CAUSE_20261013.json']:
 deps.append(pin(REC/name))
table={}
for p in deps:
 actual=pin(p['path'],p)
 assert p['identity'][3]==1 or(p['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and p['identity'][3]==2 and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492')
 assert p['path']not in table or table[p['path']]==p;table[p['path']]=p
sourcefiles=[pin(p)for p in sorted(SOURCE.iterdir())]
hf=dict(schema='SINGLE_ORIGINAL_PAIR_RANK_TYPE_PRETRANSPORT_DIAGNOSTIC_HOST_FREEZE_V1',host_source=pin(scriptpath),source_files=sourcefiles,dependencies=list(table.values()),
 input_authority_pin=pin(SOURCE/'INPUT_AUTHORITY.json'),original_v11_external_bindings=cli['mandatory_external_bindings'],
 own_future_output=str(NEWOUT),future_actual_report_pin=None,prepared_only=True,actual_guard_not_executed=True,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False)
hfpath=SOURCE/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json';write(hfpath,hf);hfpin=pin(hfpath)
oldargv=cli['argv'];oldscript=oldargv.index(str(hostpath));argv=oldargv[:oldscript]+[str(scriptpath)]
# Original CLI contains -B and script. Derive only the original complete seven
# external pin flags, replacing no Source/data or report bytes.
oldargv=cli['argv'];oldscript=oldargv.index(str(hostpath));argv+=oldargv[oldscript+1:]
argv+=['--diagnostic-freeze-summary',str(hfpath),'--diagnostic-freeze-sha256',hfpin['sha256'],'--diagnostic-freeze-seven-id',json.dumps(hfpin['identity'],separators=(',',':'))]
argvpath=AUTHOR/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json'
write(argvpath,dict(schema='ROOT_REVIEWABLE_SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ARGV_SOURCE_ONLY_V1',argv=argv,host_freeze_pin=hfpin,
 required_explicit_Root_authorization_before_execute=True,all_seven_original_external_bindings=cli['mandatory_external_bindings'],
 environment={x:'1'for x in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']},
 expected_actual_new_stages=1,historical_not_reexecuted_stages=45,prepared_only=True,actual_executed=False,future_actual_report_pin=None,AAA_qualified=False,ABA_admitted=False))
# Finite author static audit, not candidate import or compiler or guard run.
nt=ast.parse(script);assert textnode(next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources'))==phase
assert script.count('runner.execute(')==1 and 'runner.records=list(historical_raw[\'records\'])'in script and 'runner.records[:45]!=historical_raw[\'records\']'in script
assert functions.rstrip()in script
for x in function_names:
 adjusted=''.join(line[2:]if line.strip()else line for line in nested[x].splitlines(keepends=True))
 assert ''.join('  '+line if line.strip()else line for line in adjusted.splitlines(keepends=True))==nested[x]
assert not NEWOUT.exists()
report=dict(schema='AUTHOR_SOURCE_ONLY_SINGLE_DIAGNOSTIC_FINITE_REVIEW_V1',candidate_not_imported=True,compiler_and_Dragon_and_guard_not_executed=True,
 exact_PhaseResources_bytes_and5_original_function_uniform_indent_inverse_preserved=True,complete_admission_inverse_to_original_v11_bytes=True,
 one_executor_call_with_original600_cap=True,historical45_prefix_no_relabel_or_status_mutation=True,all_live_fixed2643_and_owned163_fullEOF=True,
 future_business_pins_not_predicted=True,new_ART_not_created=True,checks=checks,unique_fullEOF_files=len(ALL),unique_fullEOF_bytes=sum(x['size_bytes']for x in ALL.values()),wall_seconds=time.monotonic()-START,
 Source_tree_fullpins=[pin(p)for p in sorted(SOURCE.iterdir())],CLI_pin=pin(argvpath),host_freeze_pin=hfpin,actual_executed=False,qualified=False)
write(AUTHOR/'AUTHOR_FINITE_SOURCE_REVIEW.json',report)
write(AUTHOR/'FINAL_FROZEN_SOURCE_HANDOFF.json',dict(schema='FROZEN_SINGLE_PRETRANSPORT_DIAGNOSTIC_SOURCE_REVIEW_HANDOFF_V1',Source=str(SOURCE),all_Source_tree_pins=report['Source_tree_fullpins'],CLI_pin=pin(argvpath),author_review_pin=pin(AUTHOR/'AUTHOR_FINITE_SOURCE_REVIEW.json'),host_freeze_pin=hfpin,Source_frozen=True,Source_writes_stopped=True,actual_executed=False,Root_authorization_required_before_execution=True))
print(json.dumps(dict(checks=checks,unique_files=len(ALL),unique_bytes=sum(x['size_bytes']for x in ALL.values()),handoff_pin=pin(AUTHOR/'FINAL_FROZEN_SOURCE_HANDOFF.json'),CLI_pin=pin(argvpath),host_freeze_pin=hfpin,Source_only=True),allow_nan=False),flush=True)

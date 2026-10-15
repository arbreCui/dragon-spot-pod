#!/usr/bin/env python3
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
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2')
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

c=verified_module({'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_mount_full_identity_common_source_v1/guarded_warm_A_common.py', 'sha256': 'baed0ead3b1159b7874c5f606bf97978673e11074ef131131c402bec50982454', 'size_bytes': 20521, 'identity': [16777229, 49923959, 33188, 1, 20521, 1791804997861817826, 1791804997861817826]},'single_diagnostic_original_Common')
data=verified_module({'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/aaa_three_plane_streaming_pipeline_source_v11/actual_inputs_and_readback.py', 'sha256': '8bc8faa93cb6d5ad42553e3b69345e4111e735f840bf75ea6f602b0df40b8a5a', 'size_bytes': 17003, 'identity': [16777229, 50017620, 33188, 1, 17003, 1791873144659910636, 1791873144659910636]},'single_diagnostic_original_data')

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

class PhaseResources:
    def __init__(self,original):self.original=original;self.phase='input';self.peaks={};self.pending_publication_reserved_bytes=0
    def check(self):
        r=self.original.check();fresh=r['fresh_output']['artifact_bytes']
        caps={'initial_pack.xsm':480*MI,'global.xsm':560*MI,'BOOT-GLOBAL64-STAGE.xsm':560*MI,
              'projected_boot.xsm':800*MI,'negative_pack.xsm':480*MI,'negative_project.xsm':800*MI,
              'BOOT-SOLVED-STAGE.xsm':480*MI,'closed_boot_archive.xsm':480*MI}
        main=0
        for name,cap in caps.items():
            p=WORK/name
            if p.exists():
                n=p.stat().st_size
                if n>cap:raise RuntimeError('strict storage planning bound exceeded: '+name)
                main+=n
        # Input producer aliases are deliberately finite, owned phase copies.
        for i in range(1,4):
            p=WORK/('native_A'+str(i)+'.xsm')
            if p.exists():
                if p.stat().st_size!=156880856:raise RuntimeError('actual finite producer copy size')
                main+=p.stat().st_size
        if fresh-main+self.pending_publication_reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')
        if fresh+self.pending_publication_reserved_bytes>=2*2**30:raise RuntimeError('original total fresh2GiB')
        self.peaks[self.phase]=max(self.peaks.get(self.phase,0),fresh)
        return dict(r,publication_reserved_bytes=self.pending_publication_reserved_bytes,actual_phase=self.phase,observed_fresh_peak_bytes=self.peaks[self.phase])

def admit_original_v11(args,start):
    hf,phf=ext(args,'host_freeze')
    if hf['schema']!='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11' or \
       Path(hf['host_source']['path']).resolve()!=ORIGINAL_HOST.resolve():
        raise RuntimeError('exact owning complete Host Source freeze')
    c.same_pin(ORIGINAL_HOST,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    checkpoint('original_Common_initialize_complete')
    if before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:
        raise RuntimeError('initial history96GiB reserves originalcold/metadata/fullfresh2GiB')
    build,pbuild=ext(args,'build70')
    if pbuild!=hf['selected_actual_build70_report']:raise RuntimeError('exact external selected actual70 report pin required')
    if build['schema']!='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2' or \
       build['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       build['failure'] is not None or build['after_check_error'] is not None or \
       build['Dragon_linked'] is not True or len(build['records'])!=3 or \
       build['final_report_resource_check_passed']is not True or \
       build['old69_inputs_identical_and_retained'] is not True or \
       build['remaining68_original_inputs_identical_and_retained'] is not True or \
       build['old_nine_objects_identical_and_retained'] is not True or \
       [record['label'].rsplit('/',1)[-1]for record in build['records']]!=['compile_module','compile_driver','link_Dragon']:
        raise RuntimeError('actual cache-module/driver compile and complete70 link required')
    c.closed_report(build,helper,Path(pbuild['path']).parent,3)
    c.verify_rows(build['fixed_current_pins']);c.verify_rows(build['output_pins'])
    checkpoint('actual70_full_metadata_admitted')
    current69_pin=build['original_actual69_handle_lifetime_report_pin']
    current69,checked_current69_pin=c.load_json_exact(current69_pin['path'],current69_pin['sha256'],json.dumps(current69_pin['identity']))
    if checked_current69_pin!=current69_pin or \
       current69_pin!=hf['selected_original_actual69_handle_lifetime_report'] or \
       current69['schema']!='ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1' or \
       current69['status']!='ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       current69['failure'] is not None or current69['after_check_error'] is not None or \
       current69['Dragon_linked'] is not True or len(current69['records'])!=2 or \
       current69['remaining68_link_inputs_identical_and_retained'] is not True or \
       current69['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('separate actual native-handle complete69 two-stage premise required')
    c.closed_report(current69,helper,Path(current69_pin['path']).parent,2)
    c.verify_rows(current69['fixed_current_pins']);c.verify_rows(current69['output_pins'])
    checkpoint('current69_full_metadata_admitted')
    original69_pin=build['original_actual69_v4_report_pin']
    original69,checked_original69_pin=c.load_json_exact(original69_pin['path'],original69_pin['sha256'],json.dumps(original69_pin['identity']))
    if checked_original69_pin!=original69_pin or \
       current69['original_actual69_v4_report_pin']!=original69_pin or \
       original69_pin!=hf['selected_original_actual69_v4_report'] or \
       original69['schema']!='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       original69['status']!='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       original69['failure'] is not None or original69['after_check_error'] is not None or \
       original69['Dragon_linked'] is not True or len(original69['records'])!=10:
        raise RuntimeError('original actual nine-alias complete69 ten-stage premise required')
    c.closed_report(original69,helper,Path(original69_pin['path']).parent,10)
    c.verify_rows(original69['fixed_current_pins']);c.verify_rows(original69['output_pins'])
    checkpoint('original69_full_metadata_admitted')
    original69_link=original69['records'][-1]['command'][3:-2]
    current69_link=current69['records'][-1]['command'][3:-2]
    current70_link=build['records'][-1]['command'][3:-2]
    if len(original69_link)!=69 or len(current69_link)!=69 or \
       [i for i,(old_path,new_path)in enumerate(zip(original69_link,current69_link))if old_path!=new_path]!=[37] or \
       Path(original69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       Path(current69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o':
        raise RuntimeError('only actual native-driver object position37 changed in the separate complete69 premise')
    module_positions=[i for i,path in enumerate(current70_link)if Path(path).name=='SPOT1P64.o']
    first_archive=next(i for i,path in enumerate(current69_link)if path.endswith('.a'))
    if len(current70_link)!=70 or len(set(current70_link))!=70 or module_positions!=[first_archive] or \
       build['actual_complete70_link_inputs']!=current70_link or \
       build['replacement_zero_based_current69_input_index']!=37 or \
       build['module_insertion_current69_before_archive_index']!=first_archive or \
       [row['path']for row in build['original_current69_ordered_input_pins']]!=current69_link:
        raise RuntimeError('one genuine cache module inserted immediately before the original first archive')
    stripped70=current70_link[:first_archive]+current70_link[first_archive+1:]
    if [i for i,(old_path,new_path)in enumerate(zip(current69_link,stripped70))if old_path!=new_path]!=[37] or \
       Path(stripped70[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       [path for path in current70_link if path.endswith('.a')]!=[path for path in current69_link if path.endswith('.a')]:
        raise RuntimeError('removing the new cache helper and restoring only driver37 must recover exact original69 order')
    native_freeze_pin=hf['selected_native_exact_block_cache_source_freeze']
    native_sf,checked_native_freeze_pin=c.read_bound_json_current(native_freeze_pin['path'],native_freeze_pin)
    if checked_native_freeze_pin!=native_freeze_pin or build['actual_new_Source_freeze_pin']!=native_freeze_pin or \
       native_sf['schema']!='COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_ONLY_FREEZE_V1' or \
       native_sf['candidate_imported_or_executed']is not False or native_sf['compiled']is not False:
        raise RuntimeError('actual complete70 must bind the exact two-Fortran cache Source freeze')
    native_sf_rows=native_sf['files']+native_sf['original_source_pins']+native_sf['control_sources']+\
                   [native_sf['complete_byte_inverse_pin'],native_sf['control_plan_pin'],native_sf['logical_memory_key_contract_pin']]
    c.verify_rows(native_sf_rows)
    actual_new_sources=build['actual_new_Source_pins']
    if len(actual_new_sources)!=2 or \
       [Path(row['path']).name for row in actual_new_sources]!=['SPOT1P64.f90','SPOT_GLOBAL_NATIVE_DRIVER64.f'] or \
       any(row not in native_sf['files']for row in actual_new_sources) or \
       native_freeze_pin not in build['fixed_current_pins'] or \
       current69_pin not in build['fixed_current_pins'] or original69_pin not in build['fixed_current_pins']:
        raise RuntimeError('actual complete70 fixed pins must retain exact Sources and both genuine69 premises')
    c.verify_rows(build['original_current69_ordered_input_pins'])
    old9=binding['seventeen_required_same_production_object_pins']
    if len(old9)!=9 or any(row['path']not in current70_link for row in old9) or \
       any(row not in build['fixed_current_pins']for row in old9):
        raise RuntimeError('all original nine core objects remain exact current fixed inputs in complete70')
    direct_binding_path=HERE/'DIRECT_ALIAS_ENTRY_BINDING.json'
    if not all(any(row['path']==str(HERE/name)for row in hf['dependencies'])
               for name in ['DIRECT_ALIAS_ENTRY_BINDING.json','direct_alias_entry_controls.f90']):
        raise RuntimeError('direct-entry binding and Fortran main must belong to the complete frozen Host Source')
    direct_probe_source_pin=next(row for row in hf['dependencies']
                                 if row['path']==str(HERE/'direct_alias_entry_controls.f90'))
    direct_binding_pin=next(row for row in hf['dependencies']if row['path']==str(direct_binding_path))
    direct_binding,checked_direct_binding_pin=c.read_bound_json_current(direct_binding_path,direct_binding_pin)
    if checked_direct_binding_pin!=direct_binding_pin:raise RuntimeError('exact current direct-entry binding fullpin')
    link_command=build['records'][-1]['command']
    direct_original_inputs=direct_binding['actual_original_ordered_70_link_inputs']
    removed_main=direct_binding['excluded_original_main_pin']
    if direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V2' or \
       direct_binding['selected_actual_build70_report_pin']!=pbuild or \
       direct_binding['new_probe_source']!=str(HERE/'direct_alias_entry_controls.f90') or \
       direct_binding['only_main_object_replacement']is not True or \
       direct_binding['physics_qualification']is not False or \
       link_command[:3]!=[build['records'][0]['command'][0],'-O2','-ffp-contract=off'] or \
       link_command[-2:]!=['-o',next(row['path']for row in build['output_pins']if Path(row['path']).name=='Dragon')] or \
       link_command[3:-2]!=[row['path']for row in direct_original_inputs] or \
       len(direct_original_inputs)!=70 or \
       sum(Path(row['path']).suffix=='.o'for row in direct_original_inputs)!=66 or \
       sum(Path(row['path']).suffix=='.a'for row in direct_original_inputs)!=4 or \
       [row for row in direct_original_inputs if Path(row['path']).name=='DRAGON.o']!=[removed_main] or \
       direct_original_inputs[12]!=removed_main or \
       set(direct_binding['three_direct_control_modes'])!={'pack_original_alias','initial_contract_alias','view_system_alias'}:
        raise RuntimeError('exact actual ordered70 inputs with only original DRAGON main replacement required')
    c.verify_rows(direct_original_inputs)
    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    checkpoint('current17_full_metadata_admitted')
    sf,psf=ext(args,'source_freeze')
    if psf!=hf['selected_fortran_freeze']:raise RuntimeError('exact external selected frozen Fortran Source required')
    if sf['schema']!='COMPLETE_NEW_FORTRAN_STORAGE_SOURCE_FROZEN_V1':raise RuntimeError('complete Fortran Source freeze')
    c.verify_rows(sf['files']);c.same_pin(sf['formal_and_actual_input_plan']['path'],sf['formal_and_actual_input_plan'])
    formal_plan_pin=next(row for row in hf['dependencies']if row['path']==str(data.PLAN))
    c.same_pin(data.PLAN,formal_plan_pin)
    plan,producer_fixed,producer_reports=data.validate_actual_producers(c,args)
    for row in producer_reports:c.closed_report(row,helper,Path(row['actual_output_pin']['path']).parent.parent,4)
    checkpoint('three_independent_producer_reports_admitted')
    fixed=unique(fixed+[phf,hf['host_source'],pbuild,p17,psf]+hf['dependencies']+sf['files']+
                 [sf['formal_and_actual_input_plan']]+producer_fixed+build['fixed_current_pins']+build['output_pins']+direct_original_inputs+
                 seventeen['fixed_current_pins']+seventeen['output_pins']+native_sf_rows+
                 [current69_pin,original69_pin]+current69['fixed_current_pins']+current69['output_pins']+
                 original69['fixed_current_pins']+original69['output_pins'])
    c.verify_rows(fixed)
    checkpoint('all_original_fixed_PF_admitted_before_metadata_close')
    # Admission and full EOF checks are complete. Keep their immutable full pins,
    # the original ordered link command and the plan; close only unused JSONs.
    exe=dict(next(x for x in build['output_pins']if Path(x['path']).name=='Dragon'))
    compiler=build['records'][0]['command'][0]
    includes=tuple(x for x in build['records'][0]['command']if x.startswith('-I'))
    archives=tuple(x for x in build['records'][-1]['command']if x.endswith('.a'))
    bounded_sha256=binding['original_bounded']['sha256']
    del build,current69,original69,seventeen,producer_reports,row,producer_fixed,sf,binding,native_sf
    del native_sf_rows,actual_new_sources,old9,original69_link,current69_link,current70_link,stripped70,module_positions
    gc.collect()
    checkpoint('original_v11_metadata_lifetime_close_and_single_GC')
    return dict(fixed=fixed,hf=hf,phf=phf,support=support,helper=helper,full=full,
      base_resources=base_resources,before=before,plan=plan,direct_binding=direct_binding,
      exe=exe,compiler=compiler,includes=includes,archives=archives,bounded_sha256=bounded_sha256,
      link_command=link_command,direct_original_inputs=direct_original_inputs)


def main():
 global PHASE
 p=argparse.ArgumentParser()
 for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze','diagnostic-freeze']:
  for suffix in ['summary','sha256','seven-id']:p.add_argument('--'+prefix+'-'+suffix,required=True)
 args=p.parse_args();start=START
 first_error=None;after_errors=[];child_error=None;runner=None;owned=[];scratch_ledger=[]
 retained_state=None;historical_raw=None;historical_current_owned=[];refusal=None
 created_OUT=False;historical_prefix_installed=False
 final_all7_completed=False;report_pin=None;publication_error=None;authority=None;dh=None
 monitor=threading.Thread(target=telemetry,name='readonly-parent-memory-monitor',daemon=True);monitor.start()
 try:
  checkpoint('diagnostic_Source_entry')
  dh,dhpin=ext(args,'diagnostic_freeze')
  if dh['schema']!='SINGLE_ORIGINAL_PAIR_RANK_TYPE_PRETRANSPORT_DIAGNOSTIC_HOST_FREEZE_V2' or dh['host_source']['path']!=str(Path(__file__).resolve()):raise RuntimeError('exact diagnostic Source freeze')
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
  OUT.mkdir();created_OUT=True;(OUT/'runtime').mkdir();WORK.mkdir();(OUT/'AAA3-streaming').mkdir()
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
  if type(runner)is not full.OwnRSSSerialExecutor or full.OwnRSSSerialExecutor.__bases__!=(full.SerialExecutor,)or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('genuine original supervisor and runtime binding')
  # Exact old rows remain shared and untouched; append affects this shallow list
  # only. They are historical baseline, never new stages or new PASS claims.
  runner.records=list(historical_raw['records']);historical_prefix_installed=True
  def stable():
      c.check_full_current(fixed,owned);resources.check()
      if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 elapsed cap')
  def retain(path):
      row=c.pin(path)
      if row['identity'][3]!=1 or any(tuple(row['identity'][:2])==tuple(x['identity'][:2])for x in fixed):
          raise RuntimeError('owned regular single-link distinct physical file required')
      if any(x['path']==row['path']for x in owned):raise RuntimeError('owned current file cannot be silently rebound')
      owned.append(row);return row
  def copy(row,name):
      target=WORK/name
      if target.exists()or target.is_symlink():raise RuntimeError('fresh owned alias only')
      c.same_pin(row['path'],row);shutil.copy2(row['path'],target);actual=retain(target)
      if actual['sha256']!=row['sha256']or actual['size_bytes']!=row['size_bytes']or actual['identity'][:2]==row['identity'][:2]:
          raise RuntimeError('complete exact copy with independent7ID')
      stable();return actual
  def clean_driver_scratch_before():
      for name in ('_main001','_DUMMY'):
          target=WORK/name
          if target.exists()or target.is_symlink():
              raise RuntimeError('fresh actual CLE scratch paths required before each Dragon; no overwrite or retry')
  def stash_closed_driver_scratch(label):
      # Ganlib creates these only after the verified pre-launch absence. An
      # XABORT exit1 bypasses normal CLE teardown. Preserve exact raw bytes;
      # no deletion, no shared/producer object, no altered refusal oracle.
      if not label.replace('_','').isalnum():raise RuntimeError('finite literal driver label')
      record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
      w=json.loads(wp.read_text());logpin=c.pin(lp);watchpin=c.pin(wp)
      if record['label']!='AAA/'+label or record['status']not in ('PASS','FAILED')or \
         w['command']!=record['command']or w['command']!=[str(OUT/'runtime/Dragon')]or \
         type(w.get('pid'))is not int or w['pid']<=0 or type(w['returncode'])is not int or \
         w['limit_failure']is not None or w['rss_cap_mib']!=512 or w['own_child_only']is not True or \
         w['liveness_group_cleanup']is not True or \
         not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or \
         not 0<=w['sampled_peak_rss_mib']<512:
          raise RuntimeError('only genuine completed guarded Dragon permits scratch archival')
      if (record['status']=='PASS')!=(w['returncode']==0):raise RuntimeError('actual child closure status differs')
      receipt=dict(actual_stage_index=len(runner.records)-1,actual_stage_label=record['label'],
        actual_pid=w['pid'],actual_returncode=w['returncode'],actual_log_full_pin=logpin,
        actual_watchdog_full_pin=watchpin,exact_preserved_scratch_files=[],
        scratch_protocol_sources=hf['scratch_protocol_sources'],no_qualification_from_archival=True)
      folder=OUT/'cle_scratch_archive'/(str(len(runner.records)).zfill(3)+'_'+label)
      for name in ('_main001','_DUMMY'):
          source=WORK/name
          if not source.exists()and not source.is_symlink():continue
          before_pin=c.pin(source)
          if source.parent!=WORK or source.is_symlink()or before_pin['identity'][3]!=1 or \
             any(before_pin['identity'][:2]==row['identity'][:2]for row in fixed+owned):
              raise RuntimeError('scratch must be distinct exclusively owned regular single-link file')
          stable();folder.mkdir(parents=True,exist_ok=True)
          if folder.is_symlink()or folder.parent.is_symlink():raise RuntimeError('own scratch archive directories only')
          target=folder/name
          if target.exists()or target.is_symlink():raise RuntimeError('fresh archival target; no overwrite')
          c.same_pin(source,before_pin);source.rename(target);after_pin=retain(target)
          if after_pin['sha256']!=before_pin['sha256']or after_pin['size_bytes']!=before_pin['size_bytes']or \
             after_pin['identity'][:6]!=before_pin['identity'][:6]or source.exists()or source.is_symlink():
              raise RuntimeError('same physical scratch inode and complete raw bytes required after rename')
          receipt['exact_preserved_scratch_files'].append(dict(before_full_pin=before_pin,after_full_pin=after_pin,
            ctime_may_change_during_rename=True,exact_physical_raw_replay_retained=True))
          stable()
      clean_driver_scratch_before();scratch_ledger.append(receipt)
      rp=OUT/('Root_actual_closed_CLE_scratch_stash_'+str(len(runner.records)).zfill(3)+'.json')
      c.write(rp,receipt);retain(rp);stable()
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
    if 'resources'in locals():resources.pending_publication_reserved_bytes=8*MI
    c.verify_rows(retained_state['fixed']);c.verify_rows(historical_current_owned);c.verify_rows(owned)
    if dh is not None:c.verify_rows(dh['dependencies']);c.verify_rows(dh['source_files']);c.same_pin(__file__,dh['host_source'])
    retained_state['base_resources'].check()
    if 'resources'in locals():resources.check()
    checkpoint('failure_or_success_final_fullEOF_resource_SELF_whole_guard')
   except BaseException as exc:after_errors.append(type(exc).__name__+': '+str(exc))
  STOP.set();monitor.join(timeout=3)
  if monitor.is_alive():MONITOR_ERRORS.append('readonly monitor did not close')
  outputs=[]
  if created_OUT:
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
   old45_prefix_unchanged=historical_prefix_installed and runner.records[:45]==historical_raw['records'],
   new_actual_stage_count=0 if not historical_prefix_installed else len(runner.records)-45,
   new_actual_stage_indices=[]if not historical_prefix_installed else list(range(45,len(runner.records))),
   new_actual_refusal=refusal,exact_original_guard_class_MRO_serializer_rusage_unmodified=True,
   original_limit_values=dict(child_stage_seconds=600,whole_seconds=1800,SELF_bytes=512*MI,child_rss_mib=512,
    history_bytes=96*2**30,fresh_bytes=2*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*MI,min_free_bytes=8*2**30),
   final_all7_completed=final_all7_completed,historical_current_owned_pins=historical_current_owned,
   new_owned_copy_and_archival_pins=owned,observed_existing_outputs_before_receipt=outputs,
   originals_and_owned_copies_deleted=False,owned_copies_retained_for_separate_exact_release=True,
   original_v11_closed50_succeeded=False,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
  if created_OUT:
   report_path=OUT/'DIAGNOSTIC_REVIEW.json'
   try:
    # Exclusive, owned same FD failure publication. Guard failures after this
    # write are reported truthfully without losing the original primary error.
    fd=os.open(report_path,os.O_CREAT|os.O_EXCL|os.O_RDWR|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w+',encoding='utf-8')as stream:
     json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
     initial=os.fstat(stream.fileno());initial_id=[initial.st_dev,initial.st_ino,initial.st_mode,initial.st_nlink]
     try:
      measurement('after_initial_receipt_write_before_final_publication')
      report['SELF_peak_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;report['wall_seconds']=time.monotonic()-START
      stream.seek(0);stream.truncate(0);json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
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
      stream.seek(0);stream.truncate(0);json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
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

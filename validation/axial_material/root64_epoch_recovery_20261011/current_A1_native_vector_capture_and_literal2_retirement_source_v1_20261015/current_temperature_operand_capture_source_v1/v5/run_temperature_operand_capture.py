"""Reviewed once Root entry; one original owning guarded child copies 1984 bytes."""
import argparse,hashlib,json,os,resource,shutil,stat,struct,sys,time
from pathlib import Path
import temperature_capture_helpers as h

def child(planpin,parent):
 start=time.monotonic();h.require(os.getppid()==parent and not sys.flags.optimize and sys.getprofile() is None and all(os.environ.get(k)=='1' for k in h.THREADS),'owning parent/unoptimized/thread1 child');plan=h.read(planpin)
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);h.require(peak<512*2**20 and time.monotonic()-start<600,'SELF512/stage600')
 out=Path(plan['output_directory'])/'capture';temp=out/'sqlite_temp';temp.mkdir();sql,pool=plan['scientific_input_current7_pins'];saved=h.SavedNativeInput(sql,pool,temp,budget);parts=[];rows=[]
 try:
  for expected in plan['selected_original_records']:
   row,raw=saved.fixed_small(expected['path'],expected['kind'],expected['declared_count']);h.require(row==expected,'exact original native row, shape, range and payload hash');parts.append(raw);rows.append(row)
 finally:saved.close()
 payload=b''.join(parts);h.require(len(payload)==1984 and [r['path'][0] for r in rows]==['ISOTOPESTEMP','ISOTOPESUSED','ISOTOPERNAME','ISOTOPESMIX'],'complete literal four-record payload in original selected order')
 temps=struct.unpack('<62f',parts[0]);mixes=struct.unpack('<62i',parts[3]);case=h.read(plan['current_case_spec_pin']);material=case['materials'];slots=[];all_equal=True
 for i,(tempK,mix) in enumerate(zip(temps,mixes)):
  budget();h.require(1<=mix<=8,'original mix index1..8');key=plan['expected_C_by_mix'][str(mix)];celsius=material['temperature_C_in_every_zone'][key];expected=struct.pack('<f',float(celsius)+float(material['kelvin_offset']));actual=parts[0][4*i:4*i+4];equal=actual==expected;all_equal=all_equal and equal
  slots.append(dict(slot_one_based=i+1,original_mix=mix,original_USED_12byte_hex=parts[1][12*i:12*i+12].hex(),original_RNAME_12byte_hex=parts[2][12*i:12*i+12].hex(),original_USED_ascii=parts[1][12*i:12*i+12].decode('ascii'),original_RNAME_ascii=parts[2][12*i:12*i+12].decode('ascii'),original_native_REAL32_temperature_K=tempK,original_native_REAL32_word_hex=actual.hex(),current_parameter_temperature_C=celsius,current_kelvin_offset=material['kelvin_offset'],expected_C_to_K_REAL32_word_hex=expected.hex(),expected_C_to_K_REAL32_words_equal=equal))
 h.require(len(slots)==62 and all_equal,'all original native REAL32 temperature words equal current C-to-K expected words; no fitting')
 rawpath=out/'original_four_temperature_operand_records_1984B.bin'
 with rawpath.open('xb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
 s=rawpath.lstat();rawpin=dict(path=str(rawpath),sha256=hashlib.sha256(payload).hexdigest(),size_bytes=s.st_size,identity=h.identity(s));h.current(rawpin);budget()
 offsets=[];offset=0
 for row,raw in zip(rows,parts):offsets.append(dict(original_record=row,captured_offset_bytes=offset,captured_bytes=len(raw),captured_sha256=hashlib.sha256(raw).hexdigest()));offset+=len(raw)
 report=dict(schema='ACTUAL_CURRENT_62SLOT_TEMPERATURE_OPERAND_CAPTURE_V1',status='CURRENT_62SLOT_NATIVE_REAL32_TEMP_MIX_NAMES_AND_EXPECTED_C_TO_K_WORDS_CAPTURED_ONLY',plan_pin=planpin,original_SQLite_pin=sql,original_pool_pin=pool,original_fixed_context_pin=h.read(plan['seed_pin'])['fixed_context_pin'],raw_capture_pin=rawpin,selected_descriptors=offsets,slots=slots,captured_record_count=4,captured_bytes=1984,captured_temperature_slots=62,all62_expected_C_to_K_REAL32_words_equal=all_equal,original_native_input_written=False,original_XSM_redecoded=False,original_saved_native_functions_used_whole=True,current_root_only_full_SQL_pool_EOF_before_selected_pread=False,actual_child_full_input_EOF_loops_per_file=2,child_input_full_EOF_stages=['original_constructor_before_selected_pread','original_close_after_selected_pread'],selected_pread_payload_bytes_only=1984,original_caps=h.CAPS,child_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),child_elapsed_seconds=time.monotonic()-start,actual_temperature_operand_capture_executed=True,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**h.FALSE)
 rp=h.write(out/'ACTUAL_TEMPERATURE_OPERAND_CAPTURE.json',report);budget();print(json.dumps(dict(status=report['status'],report_pin=rp,**h.FALSE)),flush=True)

def root_claimed(a,start):
 ready_pin=h.meta_pin(h.BASE/'SOURCE_REVIEW_READY.json');ready=h.read(ready_pin);planpin=ready['plan_pin'];plan=h.read(planpin);peerpin=json.loads(a.review_pin);peer=h.read(peerpin);toolpin=json.loads(a.review_tools_pin);genpin=json.loads(a.generation_tools_pin)
 h.require(peer['status'].startswith('PASS') and peer.get('failure') is None and all(h.contains(peer,p) for p in ready['selected_Source_and_metadata_pins']+[planpin,ready_pin,genpin]),'same-round complete Source peer0/READY/GEN proof');h.closed0(h.read(toolpin),'actual_review_return',peerpin,'review_pin');h.closed0(h.read(genpin),'actual_Source_preparation_return',ready_pin,'ready_pin')
 for p in ready['selected_Source_and_metadata_pins']+[planpin,ready_pin,toolpin,peerpin,genpin]:h.exact(p)
 support=h.load(plan['original_support_Source_pin'],'temperature_original_support');common=h.load(plan['original_Common_Source_pin'],'temperature_original_common');h.require(Path(sys.executable).resolve()==support.PYTHON and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None and all(os.environ.get(k)=='1' for k in h.THREADS),'original Python/thread1/unprofiled Root')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'temperature_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'temperature_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full);h.require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,) and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original guard MRO');roots=plan['complete_joint_roots'];h.require(len(roots)==56 and any(h.BASE.is_relative_to(Path(root)) for root in roots) and plan['original_caps']==h.CAPS,'same inherited56/original caps')
 out=Path(plan['output_directory']);h.require(out.is_relative_to(h.BASE) and not os.path.lexists(out),'fresh once output nested in already-counted Source TOP, no retry');joined=production.DiskResources(common.ROOT/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(common.ART,factory.history_roots([],common.ART),8*2**30,96*2**30,production.ResourceFailure)
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);h.require(peak<512*2**20 and time.monotonic()-start<1800,'whole1800/hostSELF512');hist=history.check();joint=joined.check();extra=0
   for p in plan['inherited_explicit_metadata_pins']:
    h.current(p)
    if not any(Path(p['path']).is_relative_to(Path(r)) for r in roots):extra+=p['size_bytes']
   opened={}
   for n in os.listdir('/dev/fd'):
    try:s=os.fstat(int(n))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode) and s.st_nlink==0:opened[s.st_dev,s.st_ino]=s.st_size
   h.require(hist['artifact_bytes']+h.CAPS['cold_reserve_bytes']+64*2**20<96*2**30 and joint['artifact_bytes']+extra+sum(opened.values())<2*2**30 and joint['disk_free_bytes']-h.CAPS['cold_reserve_bytes']-2*2**30>=8*2**30,'original history96/cumulative2/external/open-unlinked/cold/free8');return dict(original_history=hist,complete_joint=joint,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(opened.values()),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();h.require(before['original_history']['artifact_bytes']+h.CAPS['cold_reserve_bytes']+64*2**20+2*2**30<96*2**30,'unchanged original fullfresh2/history reservation')
 # Owning Root parent verifies each entire SQL/pool once here. The unchanged
 # child SavedNativeInput constructor and close each verify both files again.
 # Thus three whole EOF loops per input file; selected payload pread is1984B.
 for p in plan['scientific_input_current7_pins']:h.verify_full_pin(p,resources.check)
 for p in (plan['original_final55_XSM_current7_pin'],plan['logical_inventory_current7_pin']):h.current(p)
 out.mkdir();(out/'runtime').mkdir();(out/'capture').mkdir();(out/'temperature').mkdir();shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');h.require(h.meta_pin(out/'runtime/run_bounded_dragon.py')['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'temperature',resources)
 h.require(type(runner) is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py' and Path(sys.executable).resolve()==support.PYTHON,'exact original runner/resources/private copied bounded module/interpreter before child')
 fixed_rows=ready['selected_Source_and_metadata_pins']+[planpin,ready_pin,toolpin,peerpin,genpin,plan['original_support_Source_pin'],plan['original_Common_Source_pin'],plan['original_bounded_Source_pin'],h.meta_pin(out/'runtime/run_bounded_dragon.py')]+[h.meta_pin(p0) for p0 in guard_files];fixed={}
 for p0 in fixed_rows:
  h.require(p0['path'] not in fixed or fixed[p0['path']]==p0,'one exact fullPF per fixed Source/metadata path');fixed[p0['path']]=p0
 def check_fixed():
  for p0 in fixed.values():h.current(p0);h.exact(p0)
  for p0 in plan['scientific_input_current7_pins']+[plan['original_final55_XSM_current7_pin'],plan['logical_inventory_current7_pin']]:h.current(p0)
  return resources.check()
 check_fixed();failure=None;first_error=None;secondary=[];receipt=None;watch=None;after=None;fixed_after_verified=False
 try:
  cmd=[str(support.PYTHON),'-B',str(Path(__file__).absolute()),'--mode','child','--plan-pin',json.dumps(planpin,separators=(',',':')),'--expected-parent',str(os.getpid())];runner.execute(out/'capture','temperature_operand',cmd,600);watch=helper.check_watch(out,runner.records[-1]);lines=(out/'capture/temperature_operand.log').read_text().splitlines();h.require(len(lines)==1 and len(runner.records)==1 and runner.records[0]['status']=='PASS','one original guarded child0/no retry');receipt=json.loads(lines[0]);e=h.read(receipt['report_pin']);h.require(e['captured_bytes']==1984 and e['captured_temperature_slots']==62 and e['all62_expected_C_to_K_REAL32_words_equal'] is True,'actual complete narrow operand evidence');after=check_fixed();fixed_after_verified=True
 except BaseException as error:failure=repr(error);first_error=error
 try:
  check_fixed();fixed_after_verified=True
 except BaseException as error:
  if first_error is None:first_error=error;failure=repr(error)
  else:secondary.append(repr(error))
 target=out/'Root_actual_temperature_operand_capture_summary.json';report=dict(schema='ACTUAL_ROOT_62SLOT_TEMPERATURE_OPERAND_CAPTURE_V1',status='PENDING_FINAL_RESOURCE_CHECK' if failure is None else 'FAILED_TEMPERATURE_OPERAND_CAPTURE_NO_RETRY',failure=failure,secondary_failures=secondary,records=runner.records,actual_child_receipt=receipt,actual_watchdog=watch,plan_pin=planpin,source_review_pin=peerpin,source_review_tools_pin=toolpin,source_generation_tools_pin=genpin,complete_joint_roots=roots,original_caps=h.CAPS,resources_before=before,resources_after=after,fixed_Source_metadata_before_after_full_PF_pins=list(fixed.values()),selected_Source_and_metadata_before_verified=True,selected_Source_and_metadata_after_verified=fixed_after_verified,selected_Source_and_metadata_before_after_verified=fixed_after_verified,initial_original_science_whole_PF_pins=plan['scientific_input_current7_pins'],current_root_only_full_SQL_pool_EOF_before_selected_pread=False,actual_Root_parent_full_input_EOF_loops_per_file=1,planned_full_input_EOF_loops_per_file=plan['planned_full_input_EOF_loops_per_file'],actual_completed_child_full_input_EOF_loops_per_file=2 if receipt is not None else None,selected_pread_payload_bytes_only=1984,output_paths=[str(p) for p in sorted(out.rglob('*')) if p.is_file()],actual_temperature_operand_capture_executed=receipt is not None,final_report_resource_check_passed=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**h.FALSE);owned=h.write(target,report)
 try:resources.check()
 except BaseException as error:
  if first_error is None:first_error=error;failure=repr(error)
  else:secondary.append(repr(error))
 report.update(status='ACTUAL_TEMPERATURE_OPERAND_CAPTURE_CLOSED0_ONLY' if first_error is None else 'FAILED_TEMPERATURE_OPERAND_CAPTURE_NO_RETRY',failure=failure,secondary_failures=secondary,final_report_resource_check_passed=first_error is None)
 h.current(owned);fd=os.open(target,os.O_WRONLY|os.O_NOFOLLOW)
 try:
  h.require(h.identity(os.fstat(fd))==owned['identity'],'own summary opened7 unchanged')
  with os.fdopen(fd,'w') as f:fd=None;json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 finally:
  if fd is not None:os.close(fd)
 rp=h.meta_pin(target)
 if first_error is not None:raise first_error
 resources.check()
 print(json.dumps(dict(status='ACTUAL_TEMPERATURE_OPERAND_CAPTURE_CLOSED0_ONLY',report_pin=rp,**h.FALSE)),flush=True);return rp

def root(a):
 claimed_start=time.monotonic()
 claim_path=Path(__file__).absolute().parent/'ROOT_EXECUTION_CLAIM_RECEIPT.json'
 receipt=dict(schema='ACTUAL_TEMPERATURE_OPERAND_ONCE_ROOT_CLAIM_V1',status='CLAIMED_ONCE_BEFORE_ADMISSION_CHECKS_OR_PAYLOAD_HASHES',failure=None,source_path=str(Path(__file__).absolute()),exclusive_claim_before_source_metadata_resource_or_scientific_input_checks=True,actual_temperature_operand_capture_executed=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**h.FALSE)
 with claim_path.open('xb') as claimed:
  def persist():
   claimed.seek(0);claimed.write((json.dumps(receipt,indent=2,allow_nan=False)+'\n').encode());claimed.truncate();claimed.flush();os.fsync(claimed.fileno())
  try:
   persist();h.require(all(x is not None for x in (a.review_pin,a.review_tools_pin,a.generation_tools_pin)),'reviewed root args after exclusive claim');rp=root_claimed(a,claimed_start);receipt.update(status='ACTUAL_ONCE_TEMPERATURE_OPERAND_CAPTURE_RETURNED0_ONLY',actual_temperature_operand_capture_executed=True,actual_Root_report_pin=rp);persist()
  except BaseException as error:
   receipt.update(status='FAILED_ONCE_TEMPERATURE_OPERAND_ROOT_CLAIM_RETAINED_NO_RETRY',failure=repr(error));persist();raise

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=['root','child'],required=True);ap.add_argument('--review-pin');ap.add_argument('--review-tools-pin');ap.add_argument('--generation-tools-pin');ap.add_argument('--plan-pin');ap.add_argument('--expected-parent',type=int);a=ap.parse_args()
 if a.mode=='child':h.require(a.plan_pin is not None and a.expected_parent is not None,'exact child binding');child(json.loads(a.plan_pin),a.expected_parent)
 else:root(a)
if __name__=='__main__':main()

"""Root child: unchanged original v6 tiny-vector lookup; private 104B current capture."""
import argparse,hashlib,json,os,resource,sys,time
from pathlib import Path
import capture_source_common as c
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args();started=time.monotonic()
 c.require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and sys.getprofile() is None and all(os.environ.get(k)=='1' for k in c.THREADS),'original owning parent/unoptimized/single-thread child')
 class Budget:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);c.require(peak<512*2**20 and time.monotonic()-started<600,'original child SELF512/stage600')
 budget=Budget();pb=json.loads(a.binding_pin);b=c.read(pb);c.require(b['schema']=='A1_NATIVE_VECTOR_CAPTURE_EXECUTION_BINDING_V1' and b['original_caps']==c.CAPS and b['both_A1_inputs_whole_PF_verified_by_original_parent_before_child'] is True,'exact actual capture binding');plan=c.read(b['control_plan_pin']);c.require(plan['original_caps']==c.CAPS and plan['complete_joint_roots']==b['complete_joint_roots'] and len(plan['complete_joint_roots'])==54,'same inherited completed finite52 plus whole Source/output54')
 # Import only the original saved-data adapter dependencies; no kernel or
 # transport module is loaded or called. The original v6 helper's main is not called.
 sys.path.insert(0,plan['exact_saved_adapter_source_root'])
 for r in plan['saved_adapter_import_bindings']:c.load(r['pin'],r['module'])
 adapter=sys.modules['actual_track_saved_adapter'];helper=c.load(plan['original_v6_vector_helper_pin'],'original_v6_A1_small_vectors');temp=Path(b['output_directory'])/'sqlite_temp';temp.mkdir()
 vectors,rows=helper.small_vectors(plan['native_A1_SQLite_pin'],plan['native_A1_pool_pin'],c.VECTOR_PATHS,adapter,temp,budget)
 descriptors=[];parts=[];offset=0
 for (path,count),values,row in zip(c.VECTOR_PATHS,vectors,rows):
  budget.check();c.require(values.dtype.str=='<f4' and values.shape==(count,) and bool(helper.np.isfinite(values).all()),'exact original finite little-endian REAL32 words');raw=values.view(helper.np.uint8).tobytes(order='C');sha=hashlib.sha256(raw).hexdigest();c.require(len(raw)==4*count and sha==row['native_payload_sha256'],'copied original tiny-vector bytes unchanged');parts.append(raw);descriptors.append(dict(name=path[-1],path=list(path),kind=2,words=count,offset_bytes=offset,original_native_row=row,native_payload_sha256=row['native_payload_sha256'],captured_payload_sha256=sha,captured_word_encoding='little_endian_REAL32',captured_bytes=len(raw)));offset+=len(raw)
 payload=b''.join(parts);c.require(len(descriptors)==4 and offset==len(payload)==104,'exact4 native records/26 REAL32 words/104B');out=Path(b['output_directory']);rawpath=out/'A1_native_track_vectors_f4.bin'
 with rawpath.open('xb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
 pRaw=c.pin(rawpath);c.require(pRaw['size_bytes']==104 and pRaw['sha256']==hashlib.sha256(payload).hexdigest(),'complete private104B fullPF');c.current(plan['native_A1_SQLite_pin']);c.current(plan['native_A1_pool_pin']);c.exact(pb);budget.check()
 report=dict(schema='ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE_V1',status='A1_NATIVE_26_REAL32_WORDS_104B_CAPTURE_CLOSED0_ONLY',execution_binding_pin=pb,control_plan_pin=b['control_plan_pin'],source_freeze_pin=b['source_freeze_pin'],compact_vector_full_pin=pRaw,native_vector_record_descriptors=descriptors,original_A1_SQLite_pin=plan['native_A1_SQLite_pin'],original_A1_pool_pin=plan['native_A1_pool_pin'],original_v6_vector_helper_pin=plan['original_v6_vector_helper_pin'],original_small_vectors_called_unchanged=True,captured_original_record_count=4,captured_REAL32_words=26,captured_bytes=104,native_vector_capture_executed=True,current_capture_not_historical_machine_replay=True,original_XSM_redecoded=False,native_engines_started=0,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,original_caps=c.CAPS,child_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),child_elapsed_seconds=time.monotonic()-started,**c.FALSE)
 pr=c.write(out/'ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE.json',report);budget.check();print(json.dumps(dict(status=report['status'],report_pin=pr,**c.FALSE)),flush=True)
if __name__=='__main__':main()

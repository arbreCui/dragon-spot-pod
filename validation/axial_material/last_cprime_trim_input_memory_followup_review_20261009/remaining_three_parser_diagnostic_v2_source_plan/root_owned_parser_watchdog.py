"""Root must explicitly invoke --execute after candidate/source approval.

V2 executes only the remaining three cases. Prior original_DECL is never rerun.
Default invocation does not spawn any worker. No factory/business API is loaded.
"""
import argparse
import hashlib
import json
import os
import signal
import stat
import subprocess
import time
from pathlib import Path

ROOT=Path('/Users/wen/spot');PLAN=Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_v2_20261009')
PYTHON=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12');PS=Path('/bin/ps')
ORIGINAL=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'
ORIGINAL_SHA='4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
CANDIDATE=Path('/private/tmp/axmat_v9_strict_json_local_immutable_sharing_candidate_20261009/strict_json_bytes_local_immutable_sharing_candidate.py')
CANDIDATE_SHA='15383b532973a9dc68fcdaeb7251723ee3379a075472bddadfb6bdbf9b9ec8d3'
DATA=(('DECL',ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/declaration.json','3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae'),('FULL_SEVEN_INPUT',ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'))
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
CAP_SECONDS=120;CAP_MIB=512;SAMPLE_SECONDS=.02

PRIOR_OUT=Path('/private/tmp/axmat_v9_isolated_parser_metadata_root_execution_20261009')
PRIOR_SHAS={'original_DECL/child_report.json':'f256dcf384caf449db97c01e609dd69b802df41dfa200c001d1e58e0e44219b8','original_DECL/latest_phase.json':'60de8f1738dbef8bd99e1f174d405401531efa15db012f5828432cfc1135d328','original_DECL/own_pid_ps_samples.jsonl':'409c6a5e63b6d9cf18d92de65db5d505c42fcde0cccf11fb85dbefd992ec364b','original_DECL/owned_child_start.json':'6994cc1f635006af90ca5e9bff410adf3b3495e3afa99525095994345576db1b','original_DECL/stderr.txt':'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','original_DECL/stdout.jsonl':'a48d9eced3466de26e91056768ae0e6763a701c3c59b424535e3fb3371c966c2','root_actual_failed_tool_return.json':'615bc19512db52979fbadf85241f98d698e26d01f2ebe6c267cb4ad8cbf3adcf'}
REMAINING_CASES=(('candidate','DECL'),('original','FULL_SEVEN_INPUT'),('candidate','FULL_SEVEN_INPUT'))
RETAINED_PHASES=('parse_return_value_and_raw_retained','parsed_value_retained_raw_released','parsed_value_retained_after_validation','after_fresh_pins_value_retained','parsed_value_released_with_explicit_gc')

def identity(path):
 s=Path(path).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(path,sha=None):
 path=Path(path);before=identity(path);assert stat.S_ISREG(before[2]) and path.parent.resolve(strict=True)==path.parent
 h=hashlib.sha256();fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
  while block:=f.read(1024**2):h.update(block)
 assert identity(path)==before
 if sha:assert h.hexdigest()==sha
 return dict(path=str(path),identity=before,size=before[3],sha256=h.hexdigest())

def atomic(path,value):
 p=Path(path);temporary=p.with_name(p.name+'.pending-'+str(os.getpid()))
 with temporary.open('xb') as f:f.write((json.dumps(value,allow_nan=False,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
 try:os.link(temporary,p)
 finally:temporary.unlink()

def clean_owned_group(proc):
 signals=[];exit_races=[]
 for sig,label in ((signal.SIGTERM,'SIGTERM'),(signal.SIGKILL,'SIGKILL')):
  if proc.poll() is not None:break
  try:
   assert os.getpgid(proc.pid)==proc.pid
   os.killpg(proc.pid,sig);signals.append(label)
  except ProcessLookupError:
   exit_races.append(label+' process already exited before own-group signal')
  try:proc.wait(timeout=2)
  except subprocess.TimeoutExpired:
   if sig==signal.SIGKILL:raise
 if proc.poll() is None:raise RuntimeError('own parser child was not reaped after cleanup')
 return dict(owned_pid=proc.pid,owned_session_and_group=proc.pid,signals=signals,exit_races=exit_races,wait_returncode=proc.returncode,direct_child_reaped=True)

def read_phase(case,pid):
 p=case/'latest_phase.json'
 if not p.exists():return dict(phase='worker_bootstrap',sequence=0)
 observation=json.loads(p.read_text());assert observation['worker_pid']==pid and observation['scope']=='PARSER_METADATA_DIAGNOSTIC_ONLY'
 assert type(observation['sequence']) is int and observation['sequence']>0 and type(observation['phase']) is str
 return dict(phase=observation['phase'],sequence=observation['sequence'])

def own_rss(pid,remaining):
 result=subprocess.run([str(PS),'-o','pid=','-o','rss=','-p',str(pid)],capture_output=True,text=True,timeout=max(.01,min(1,remaining)))
 assert result.returncode==0
 lines=[line.split() for line in result.stdout.splitlines() if line.strip()]
 assert len(lines)==1 and len(lines[0])==2 and all(s.isdigit() for s in lines[0]) and int(lines[0][0])==pid
 return int(lines[0][1]),result.stdout

def run_case(out,label,source,source_sha,data,data_sha,worker_pin):
 case=out/label;case.mkdir();stdout=case/'stdout.jsonl';stderr=case/'stderr.txt';before_source=pin(source,source_sha);before_data=pin(data,data_sha)
 env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONSTARTUP',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1'
 for k in THREAD_KEYS:env[k]='1'
 command=[str(PYTHON),str(PLAN/'parser_metadata_worker.py'),'--source',str(source),'--source-sha',source_sha,'--data',str(data),'--data-sha',data_sha,'--case-dir',str(case)]
 started=time.monotonic();proc=None;failure=None;count=0;peak=0.;phases={};cleanup=None
 with stdout.open('xb') as outlog,stderr.open('xb') as errlog,(case/'own_pid_ps_samples.jsonl').open('x') as samplelog:
  try:
   proc=subprocess.Popen(command,cwd=case,env=env,stdin=subprocess.DEVNULL,stdout=outlog,stderr=errlog,start_new_session=True)
   try:assert os.getpgid(proc.pid)==proc.pid
   except ProcessLookupError:
    proc.wait(timeout=2);raise RuntimeError('owned child exited before group admission')
   atomic(case/'owned_child_start.json',dict(pid=proc.pid,process_group=proc.pid,command=command,monotonic=started,scope='ISOLATED_METADATA_DIAGNOSTIC_ONLY',wall_cap_seconds=CAP_SECONDS,rss_cap_mib=CAP_MIB,numeric_or_business_stage=False))
   while proc.poll() is None:
    elapsed=time.monotonic()-started;remaining=CAP_SECONDS-elapsed
    if remaining<=0:failure='120 second isolated child wall cap reached';break
    phase_before=read_phase(case,proc.pid)
    try:rss_kib,raw=own_rss(proc.pid,remaining)
    except BaseException as error:
     if proc.poll() is not None:break
     failure='live own-PID ps RSS observation failed: '+repr(error);break
    now=time.monotonic();phase_after=read_phase(case,proc.pid)
    stable_phase=phase_before==phase_after
    phase=phase_after['phase'] if stable_phase else 'phase_transition_ambiguous';sequence=phase_after['sequence']
    rss=rss_kib/1024;peak=max(peak,rss);count+=1
    agg=phases.setdefault(phase,dict(samples=0,min_mib=rss,max_mib=rss,last_mib=rss))
    agg.update(samples=agg['samples']+1,min_mib=min(agg['min_mib'],rss),max_mib=max(agg['max_mib'],rss),last_mib=rss)
    samplelog.write(json.dumps(dict(pid=proc.pid,rss_kib=rss_kib,rss_mib=rss,elapsed_seconds=now-started,phase=phase,phase_sequence=sequence,stable_phase=stable_phase,phase_before=phase_before,phase_after=phase_after,raw_ps=raw),separators=(',',':'))+'\n');samplelog.flush()
    if rss>=CAP_MIB:failure='own-child 512 MiB ps RSS cap reached';break
    if now-started>=CAP_SECONDS:failure='120 second isolated child wall cap reached';break
    time.sleep(min(SAMPLE_SECONDS,max(0,CAP_SECONDS-(time.monotonic()-started))))
   if failure is None:proc.wait(timeout=2)
  except BaseException as error:
   failure=repr(error)
  finally:
   if proc is not None:cleanup=clean_owned_group(proc)
   samplelog.flush();os.fsync(samplelog.fileno())
 elapsed=time.monotonic()-started
 after_source=pin(source,source_sha);after_data=pin(data,data_sha)
 assert before_source==after_source and before_data==after_data and pin(PLAN/'parser_metadata_worker.py')==worker_pin
 report_path=case/'child_report.json';child=None
 if report_path.exists():
  child=json.loads(report_path.read_text());assert child['worker_pid']==proc.pid
  assert child['source_before']==child['source_after']==before_source and child['data_before']==child['data_after']==before_data
  assert child['classification']=='PARSED_METADATA_DIAGNOSTIC_ONLY' and child['business_import_or_API_or_constructor_or_PREP_RUN'] is False and child['native_or_science_credit'] is False
 passed=failure is None and proc is not None and proc.returncode==0 and elapsed<CAP_SECONDS and count>0 and peak<CAP_MIB and child is not None
 retained_phase_names=('parse_return_value_and_raw_retained','parsed_value_retained_raw_released','parsed_value_retained_after_validation','after_fresh_pins_value_retained','parsed_value_released_with_explicit_gc')
 retained_phase_coverage={name:phases.get(name,{}).get('samples',0)>0 for name in retained_phase_names}
 if passed and not all(retained_phase_coverage.values()):
  passed=False;failure='required stable retained-value RSS phase was not observed; no retained-memory measurement credited'
 if passed and child['rusage_maxrss']['MiB'] is not None and child['rusage_maxrss']['MiB']>=CAP_MIB:
  passed=False;failure='supplemental process high-water at or over512MiB despite sampled ps peak; no bounded diagnostic success credited'
 value=dict(schema='ROOT_OWNED_ISOLATED_PARSER_PS_WATCHDOG_RECEIPT_V1',status='PASS_ISOLATED_PARSER_DIAGNOSTIC_ONLY' if passed else 'FAILED_ISOLATED_PARSER_DIAGNOSTIC_NO_RETRY',command=command,child_pid=None if proc is None else proc.pid,child_returncode=None if proc is None else proc.returncode,wall_cap_seconds=CAP_SECONDS,rss_cap_mib=CAP_MIB,elapsed_seconds=elapsed,own_PID_ps_sample_count=count,own_PID_ps_sampled_peak_mib=peak,phase_RSS_samples=phases,stable_retained_phase_coverage=retained_phase_coverage,limit_or_observation_failure=failure,own_group_cleanup=cleanup,source_before=before_source,source_after=after_source,data_before=before_data,data_after=after_data,worker_source_pin=worker_pin,stdout_pin=pin(stdout),stderr_pin=pin(stderr),samples_pin=pin(case/'own_pid_ps_samples.jsonl'),child_report_pin=None if child is None else pin(report_path),retained_RSS_scope='Actual sampled process RSS while entire parsed builtin value is still retained; raw-release and explicit-gc phases are separate. Samples crossing phase boundaries are marked ambiguous. No object-size or original business-caller footprint is inferred.',rusage_maxrss=None if child is None else child['rusage_maxrss'],ROOT_business_RUNNING_stage_faked=False,business_or_native_or_combined_RSS_or_science_credit=False)
 atomic(case/'watchdog_receipt.json',value)
 return value,child

def load_prior_original_decl(original_pin,decl_pin):
 before={name:pin(PRIOR_OUT/name,sha) for name,sha in PRIOR_SHAS.items()}
 assert not (PRIOR_OUT/'original_DECL/watchdog_receipt.json').exists() and not (PRIOR_OUT/'diagnostic_summary.json').exists()
 failed=json.loads((PRIOR_OUT/'root_actual_failed_tool_return.json').read_text())
 assert failed['closed'] is True and type(failed['exit_code']) is int and failed['exit_code']==1 and failed['science_credit'] is False
 assert failed['initial_tool']['chunk_id']=='c8a0a5' and failed['initial_tool']['session_id']==66201
 assert failed['completion_tool']['chunk_id']=='24b476' and type(failed['completion_tool']['exit_code']) is int and failed['completion_tool']['exit_code']==1
 child=json.loads((PRIOR_OUT/'original_DECL/child_report.json').read_text());start=json.loads((PRIOR_OUT/'original_DECL/owned_child_start.json').read_text())
 assert type(child['worker_pid']) is int and child['worker_pid']==11722 and start['pid']==start['process_group']==11722
 assert start['command']==[str(PYTHON),'/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_20261009/parser_metadata_worker.py','--source',str(ORIGINAL),'--source-sha',ORIGINAL_SHA,'--data',str(DATA[0][1]),'--data-sha',DATA[0][2],'--case-dir',str(PRIOR_OUT/'original_DECL')]
 assert start['wall_cap_seconds']==CAP_SECONDS and start['rss_cap_mib']==CAP_MIB and start['numeric_or_business_stage'] is False
 assert child['source_before']==child['source_after']==original_pin and child['data_before']==child['data_after']==decl_pin
 assert child['classification']=='PARSED_METADATA_DIAGNOSTIC_ONLY' and child['business_import_or_API_or_constructor_or_PREP_RUN'] is False and child['native_or_science_credit'] is False
 assert child['optimization_disabled'] is True and child['bytecode_disabled'] is True and child['mutable_container_independence'] is True
 assert child['python_executable']==str(PYTHON) and child['thread_environment']=={k:'1' for k in THREAD_KEYS}
 samples=[json.loads(line) for line in (PRIOR_OUT/'original_DECL/own_pid_ps_samples.jsonl').read_text().splitlines()]
 assert len(samples)==59
 phases={};peak=0.;stable_count=0
 for row in samples:
  assert type(row['pid']) is int and row['pid']==11722 and type(row['rss_kib']) is int and row['rss_kib']>=0
  assert row['rss_mib']==row['rss_kib']/1024 and 0<=row['elapsed_seconds']<CAP_SECONDS and row['rss_mib']<CAP_MIB
  raw=row['raw_ps'].split();assert raw==[str(row['pid']),str(row['rss_kib'])]
  assert type(row['stable_phase']) is bool and row['stable_phase']==(row['phase_before']==row['phase_after'])
  peak=max(peak,row['rss_mib'])
  if not row['stable_phase']:
   assert row['phase']=='phase_transition_ambiguous';continue
  assert row['phase']==row['phase_after']['phase'] and row['phase_sequence']==row['phase_after']['sequence'];stable_count+=1
  rss=row['rss_mib'];agg=phases.setdefault(row['phase'],dict(samples=0,min_mib=rss,max_mib=rss,last_mib=rss))
  agg.update(samples=agg['samples']+1,min_mib=min(agg['min_mib'],rss),max_mib=max(agg['max_mib'],rss),last_mib=rss)
 assert stable_count==57 and peak==55.46875 and all(phases.get(name,{}).get('samples',0)>0 for name in RETAINED_PHASES)
 after={name:pin(PRIOR_OUT/name,sha) for name,sha in PRIOR_SHAS.items()};assert before==after
 baseline=dict(status='PRIOR_PARENT_FAILED_PARTIAL_CHILD_OUTPUT_AND_ACTUAL_RSS_ONLY',prior_parent_actual_exit_code=1,prior_parent_tool_chunks=['c8a0a5','24b476'],prior_parent_session_id=66201,original_child_pid=11722,original_child_wait_returncode=None,original_parent_watchdog_receipt_present=False,original_child_success_qualification=False,overall_four_case_watchdog_qualification=False,actual_ps_sample_count=len(samples),actual_stable_ps_sample_count=stable_count,actual_ps_sampled_peak_mib=peak,stable_phase_RSS_samples=phases,prior_file_pins=before,output_equality_baseline_scope='Pinned prior actual child report full builtin/type/insertion-order output digests only; missing parent receipt and child wait code are not reconstructed.',RSS_comparison_baseline_scope='Pinned prior actual own-PID ps samples in stable phases only; two phase-transition samples excluded from phase comparison; prior parent failed; no prior watchdog or four-case success.',no_combined_runtime_native_AAA_ABA_or_science_credit=True)
 return baseline,child

def compare_output_and_stable_phase_RSS(original,changed,original_phases,candidate_phases):
 fields=('plain_builtin_type_counts','type_and_insertion_order_shape_sha256','whole_insertion_order_JSON_output_sha256','whole_insertion_order_JSON_output_bytes','mutable_container_independence')
 outputs={k:original[k]==changed[k] for k in fields};RSS={}
 for name in RETAINED_PHASES:
  a=original_phases.get(name,{});b=candidate_phases.get(name,{})
  assert a.get('samples',0)>0 and b.get('samples',0)>0
  RSS[name]=dict(original_actual_stable_phase_samples=a,candidate_actual_stable_phase_samples=b,candidate_minus_original_max_mib=b['max_mib']-a['max_mib'],scope='Same named actually observed stable retained-value phase; process RSS only; no allocation-line or original caller footprint claim')
 return outputs,RSS

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');parser.add_argument('--candidate-source');parser.add_argument('--candidate-sha');parser.add_argument('--output')
 a=parser.parse_args()
 if not a.execute:
  print(json.dumps(dict(status='SOURCE_PLAN_V2_ONLY_NO_CHILD_STARTED',future_candidate_source=a.candidate_source,future_actual_terminal=None,planned_cases=[source+'_'+data for source,data in REMAINING_CASES],original_DECL_rerun=False,overall_four_case_watchdog_qualification=False,original_child_wait_returncode=None,caps=dict(seconds=120,MiB=512,threads=1,retries=0,workers_at_once=1))));return
 assert __debug__ and a.candidate_source and a.candidate_sha and a.output
 candidate=Path(a.candidate_source);out=Path(a.output)
 assert candidate.is_absolute() and candidate.parent.resolve(strict=True)==candidate.parent and candidate.is_relative_to(Path('/private/tmp/axmat_v9_strict_json_local_immutable_sharing_candidate_20261009'))
 assert candidate==CANDIDATE and a.candidate_sha==CANDIDATE_SHA
 assert len(a.candidate_sha)==64 and all(c in '0123456789abcdef' for c in a.candidate_sha)
 assert out.is_absolute() and str(out)==a.output and '..' not in out.parts and out.parent.resolve(strict=True)==out.parent and out.is_relative_to(Path('/private/tmp')) and out!=PLAN and not out.is_relative_to(PLAN)
 assert out!=PRIOR_OUT and not out.is_relative_to(PRIOR_OUT)
 worker=pin(PLAN/'parser_metadata_worker.py','9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552');selfpin=pin(Path(__file__));pin(PYTHON,'ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860');pspin=pin(PS);original_pin=pin(ORIGINAL,ORIGINAL_SHA);pin(candidate,a.candidate_sha)
 baseline,prior_child=load_prior_original_decl(original_pin,pin(DATA[0][1],DATA[0][2]))
 out.mkdir(exist_ok=False)
 receipts=[];results={('DECL','original'):prior_child};phase_results={('DECL','original'):baseline['stable_phase_RSS_samples']};failure=False
 data_map={label:(data,sha) for label,data,sha in DATA}
 for source_label,data_label in REMAINING_CASES:
  assert (source_label,data_label)!=('original','DECL')
  source,source_sha=(ORIGINAL,ORIGINAL_SHA) if source_label=='original' else (candidate,a.candidate_sha)
  data,data_sha=data_map[data_label]
  receipt,child=run_case(out,source_label+'_'+data_label,source,source_sha,data,data_sha,worker);receipts.append(receipt)
  if receipt['status']!='PASS_ISOLATED_PARSER_DIAGNOSTIC_ONLY':failure=True;break
  results[(data_label,source_label)]=child;phase_results[(data_label,source_label)]=receipt['phase_RSS_samples']
 matches={};RSS_matches={}
 if not failure:
  assert len(receipts)==3
  for data_label,_,_ in DATA:
   outputs,RSS=compare_output_and_stable_phase_RSS(results[(data_label,'original')],results[(data_label,'candidate')],phase_results[(data_label,'original')],phase_results[(data_label,'candidate')])
   matches[data_label]=outputs;RSS_matches[data_label]=RSS
   if not all(outputs.values()):failure=True
 assert pin(PLAN/'parser_metadata_worker.py','9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552')==worker and pin(Path(__file__))==selfpin
 assert {name:pin(PRIOR_OUT/name,sha) for name,sha in PRIOR_SHAS.items()}==baseline['prior_file_pins']
 result=dict(schema='ROOT_OWNED_REMAINING_THREE_SERIAL_ISOLATED_PARSER_METADATA_DIAGNOSTICS_V2',status='FAILED_REMAINING_ISOLATED_DIAGNOSTIC_NO_RETRY' if failure else 'PASS_REMAINING_THREE_ISOLATED_PARSER_METADATA_DIAGNOSTICS_ONLY',completed_cases=len(receipts),expected_cases=3,planned_cases=[source+'_'+data for source,data in REMAINING_CASES],receipts=receipts,prior_original_DECL_baseline=baseline,prior_original_DECL_child_wait_returncode=None,prior_parent_actual_exit_code=1,overall_four_case_watchdog_qualification=False,remaining_three_case_diagnostic_success=not failure,whole_builtin_insertion_order_JSON_output_comparisons=matches,actual_stable_phase_RSS_comparisons=RSS_matches,worker_source_pin=worker,watchdog_source_pin=selfpin,ps_executable_pin=pspin,one_worker_at_once=True,retries=0,original_DECL_rerun=False,no_business_factory_import_or_API_constructor_PREP_RUN=True,no_combined_runtime_native_AAA_ABA_or_science_credit=True,actual_V8_allocating_line_localized=False,Root_tool_terminal_observation=None)
 atomic(out/'diagnostic_summary.json',result)
 print(json.dumps(dict(status=result['status'],report=str(out/'diagnostic_summary.json'),sha256=pin(out/'diagnostic_summary.json')['sha256'],completed_cases=len(receipts),overall_four_case_watchdog_qualification=False,no_science=True)))
 if failure:raise SystemExit(1)

if __name__=='__main__':main()

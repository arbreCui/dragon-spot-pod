#!/usr/bin/env python3
"""Serial genuine controls under an additional Root boundary; no Native solve."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');V=ROOT/'validation/axial_material';ART=ROOT/'validation/artifacts'
BASE=V/'complete_history_root_index_source_v15_20261010'
D=BASE/'actual_frame_encoder_current_epoch_monitor_controls_sources_20261011'
E=BASE/'actual_frame_encoder_current_epoch_monitor_controls_receipts_20261011'
BINDING=D/'Root_current_fresh_frame_controls_Source_binding.json'
REVIEW=E/'Source_prelaunch_review.json'
OUT=ART/'axial-material-frame-encoder-current-epoch-controls-Root-host-20261011'
PYTHON=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
BOUNDED=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py'
sys.path.insert(0,str(V))
from run_real64_common_rank2_training import TrainingResources

def main():
    started=time.monotonic()
    if OUT.exists()or OUT.is_symlink():raise RuntimeError('fresh permanent Root output; no retry')
    if Path(sys.executable).resolve()!=PYTHON or sys.flags.optimize:raise RuntimeError('original exact nonoptimized Python')
    if any(os.environ.get(k)!='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')):raise RuntimeError('original one thread')
    spec=importlib.util.spec_from_file_location('current_original_bounded',BOUNDED)
    bounded=importlib.util.module_from_spec(spec);spec.loader.exec_module(bounded)
    if hashlib.sha256(BOUNDED.read_bytes()).hexdigest()!='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09':raise RuntimeError('original bounded bytes')
    def pin(p):
        p=Path(p);s=p.stat();ids=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
        before=ids(s)
        with p.open('rb')as f:
            if ids(os.fstat(f.fileno()))!=before:raise RuntimeError('opened identity')
            sha=hashlib.file_digest(f,'sha256').hexdigest()
            if ids(os.fstat(f.fileno()))!=before:raise RuntimeError('EOF identity')
        if ids(p.stat())!=before:raise RuntimeError('after identity')
        return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=before)
    bp=pin(BINDING);rp=pin(REVIEW);b=json.loads(BINDING.read_text());review=json.loads(REVIEW.read_text())
    if (review.get('all_checks_passed')is not True or review.get('blockers')!=[]or review['new_Source_binding_pin']!=bp):raise RuntimeError('actual independent Source prelaunch required')
    fixed=[bp,rp,b['adapter_Source_pin'],b['control_entry_Source_pin'],b['original_N9_controls_Source_binding_pin']]
    guard=TrainingResources(OUT)
    checkpoints=[]
    def check(label):
        if time.monotonic()-started>=1800:raise RuntimeError('Root whole1800 cap')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('Root SELF512 cap')
        g=guard.check()
        if g['complete_history']['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB including original cold reserve')
        if g['fresh_output']['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('original free floor and reserves')
        checkpoints.append(dict(label=label,original=g))
    check('before');OUT.mkdir();records=[];current=None;failure=None
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    try:
        for case in b['case_execution_order']:
            for item in fixed:
                if pin(item['path'])!=item:raise RuntimeError('immutable current binding/Source changed')
            check('before_'+case)
            folder=OUT/case;folder.mkdir();command=[str(PYTHON),'-B',b['control_entry_Source_pin']['path'],'--binding',str(BINDING),'--binding-sha256',bp['sha256'],'--independent-prelaunch-review',str(REVIEW),'--case',case]
            peak=0.;stage=time.monotonic();last_account=stage
            current=None;watchdog=None;readfd=None;writefd=None
            attempt_exception=None;actual_error=None;cleanup_errors=[]
            actual_wait_return=None;wait_return_observed=False
            def error_record(error):
                return dict(type=type(error).__module__+'.'+type(error).__qualname__,repr=repr(error),text=str(error))
            def cleanup_error(step,error):
                cleanup_errors.append(dict(step=step,actual_error=error_record(error)))
            try:
                with (folder/'stdout.log').open('xb')as stdout,(folder/'stderr.log').open('xb')as stderr:
                    try:
                        current=subprocess.Popen(command,stdout=stdout,stderr=stderr,env=os.environ.copy(),start_new_session=True)
                        readfd,writefd=os.pipe()
                        watchdog=bounded.start_liveness_watchdog(readfd,current.pid,bounded.TERM_GRACE_SECONDS)
                        os.close(readfd);readfd=None
                        while current.poll()is None:
                            now=time.monotonic()
                            if now-stage>=600 or now-started>=1800:raise RuntimeError('original stage600/whole1800')
                            observed=subprocess.run(['/bin/ps','-o','rss=','-p',str(current.pid)],capture_output=True,text=True,timeout=min(2.,max(.05,600-(now-stage))))
                            if observed.returncode and current.poll()is None:raise RuntimeError('Root current control RSS unavailable')
                            if observed.stdout.strip():peak=max(peak,float(observed.stdout.strip())/1024.)
                            if peak>=512:raise RuntimeError('Root current control SELF512 MiB')
                            if now-last_account>=5:check('live_'+case);last_account=now
                            try:current.wait(timeout=min(.2,max(.001,600-(time.monotonic()-stage))))
                            except subprocess.TimeoutExpired:pass
                    except BaseException as error:
                        attempt_exception=error;actual_error=error_record(error)
                    finally:
                        # Every genuinely attempted control is closed and its
                        # complete streams saved, including an RSS/clock/disk
                        # refusal. Unknown/failed waits retain None/errors.
                        if current is not None:
                            if attempt_exception is not None:
                                try:bounded.terminate_group(current)
                                except BaseException as error:cleanup_error('original_bounded_terminate_group',error)
                            try:
                                actual_wait_return=current.wait(timeout=0)
                                if type(actual_wait_return)is not int or actual_wait_return!=current.returncode:raise RuntimeError('actual original Popen wait return remains unproven')
                                wait_return_observed=True
                            except BaseException as error:cleanup_error('actual_original_Popen_wait',error)
                        if readfd is not None:
                            try:os.close(readfd)
                            except BaseException as error:cleanup_error('close_original_watchdog_readfd',error)
                            readfd=None
                        if watchdog is not None and writefd is not None:
                            try:bounded.finish_liveness_watchdog(writefd,watchdog)
                            except BaseException as error:cleanup_error('original_bounded_finish_liveness_watchdog',error)
                            writefd=None
                        elif writefd is not None:
                            try:os.close(writefd)
                            except BaseException as error:cleanup_error('close_unstarted_watchdog_writefd',error)
                            writefd=None
                        for name,stream in(('stdout',stdout),('stderr',stderr)):
                            try:stream.flush();os.fsync(stream.fileno())
                            except BaseException as error:cleanup_error(name+'_complete_stream_fsync',error)
            except BaseException as error:
                if attempt_exception is None:attempt_exception=error;actual_error=error_record(error)
                else:cleanup_error('complete_stream_context_close',error)
            stream_pins={}
            for name in('stdout','stderr'):
                try:stream_pins[name]=pin(folder/(name+'.log'))
                except BaseException as error:
                    stream_pins[name]=None;cleanup_error(name+'_complete_stream_full_EOF_pin',error)
            record=dict(case=case,actual_command=command,pid=None if current is None else current.pid,
                returncode=None if current is None else current.returncode,
                wall_seconds=time.monotonic()-stage,Root_sampled_control_SELF_peak_mib=peak,
                stdout=stream_pins['stdout'],stderr=stream_pins['stderr'],
                actual_error=actual_error,actual_cleanup_errors=cleanup_errors,
                actual_original_Popen_wait_return=actual_wait_return,
                original_Popen_wait_return_observed=wait_return_observed,
                raw_wait_status_tuple_claimed=False,unknown_or_failed_wait_promoted_to_zero=False,
                expected_negative_business_stage_is_not_promoted=True)
            records.append(record);write(folder/'Root_actual_terminal.json',record)
            print(json.dumps({k:record[k]for k in('case','pid','returncode','wall_seconds','Root_sampled_control_SELF_peak_mib')}),flush=True)
            if attempt_exception is not None:raise attempt_exception
            if cleanup_errors:raise RuntimeError('actual control cleanup/persistence/wait failed; remaining cases not launched')
            if not wait_return_observed or current is None or current.returncode!=0:raise RuntimeError('actual control failed or closure unproven; remaining cases not launched')
            current=None;check('after_'+case)
        for item in fixed:
            if pin(item['path'])!=item:raise RuntimeError('fixed current Source changed at close')
        check('after_all')
    except BaseException as error:failure=repr(error)
    summary=dict(schema='ROOT_CURRENT_FRAME_ENCODER_GENUINE_CONTROLS_ACTUAL_V1',
        status='ALL_TEN_ACTUAL_CONTROLS_CLOSED0_SAVED_REVIEW_REQUIRED'if failure is None else 'FAILED_ACTUAL_CONTROLS_NO_RETRY',
        fixed_current_Source_pins=fixed,actual_case_records=records,failure=failure,
        original_order=b['case_execution_order'],completed_cases=len(records),
        all_ten_control_entries_closed0=failure is None and len(records)==10,
        resource_checkpoints=checkpoints,whole_seconds=time.monotonic()-started,
        Root_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        native_compilation_or_transport_executed=False,complete_Native_qualified=False,
        scientific_accuracy_qualified=False,online_BOOT_qualified=False,goal_complete=False)
    write(OUT/'Root_actual_controls_summary.json',summary)
    print(json.dumps(dict(status=summary['status'],completed_cases=len(records),failure=failure)),flush=True)
    return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())

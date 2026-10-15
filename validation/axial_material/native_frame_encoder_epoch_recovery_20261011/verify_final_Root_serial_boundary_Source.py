"""Pure AST/current full-EOF review of the Root serial control boundary.

This does not import or execute the boundary, create a child, or mock an OS
outcome. The independently admitted D/E contract remains unchanged.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'complete_history_root_index_source_v15_20261010'
D=BASE/'actual_frame_encoder_current_epoch_monitor_controls_sources_20261011'
E=BASE/'actual_frame_encoder_current_epoch_monitor_controls_receipts_20261011'
ROOT_SOURCE=HERE/'run_current_genuine_controls.py'
START=time.monotonic()
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
CHECKS=[]

def need(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def check(value,message):need(value,message);CHECKS.append(message)

def bounded():
    need(time.monotonic()-START<600,'pure outerSource metadata600 cap')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    need(peak<512*2**20,'pure outerSource self512 cap')

def identity(s):return [getattr(s,k)for k in FIELDS]

def pin(path,single=True):
    path=Path(path);before=identity(path.lstat());need(stat.S_ISREG(before[2])and(before[3]==1 if single else before[3]>=1),'actual regular Source/pin')
    digest=hashlib.sha256();size=0
    with path.open('rb')as stream:
        need(identity(os.fstat(stream.fileno()))==before,'actual opened identity')
        while True:
            bounded();raw=stream.read(2**20)
            if not raw:break
            size+=len(raw);digest.update(raw)
        need(identity(os.fstat(stream.fileno()))==before,'actual EOF identity')
    need(identity(path.lstat())==before and size==before[4],'actual current Source unchanged')
    return dict(path=str(path),sha256=digest.hexdigest(),size_bytes=size,identity=before)

def main():
    sourcepin=pin(ROOT_SOURCE);raw=ROOT_SOURCE.read_text();tree=ast.parse(raw)
    mainfn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    loops=[n for n in ast.walk(mainfn)if isinstance(n,ast.For)and ast.unparse(n.iter)=="b['case_execution_order']"]
    check(len(loops)==1,'one original binding case-order loop, no retry loop')
    loop=loops[0]
    popens=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and ast.unparse(n.func)=='subprocess.Popen']
    check(len(popens)==1 and popens[0]in list(ast.walk(loop)),'sole serial original Popen command launch site')
    check(any(k.arg=='start_new_session'and isinstance(k.value,ast.Constant)and k.value.value is True for k in popens[0].keywords),'genuine original child process group isolation')
    outer_guard=next(n for n in ast.walk(mainfn)if isinstance(n,ast.FunctionDef)and n.name=='check')
    guardtext=ast.get_source_segment(raw,outer_guard)
    check('>=1800'in guardtext and '>=512*2**20'in guardtext,'unchanged Root whole1800 and SELF512 checks')
    check('20971764748+64*2**20>=96*2**30'in guardtext and '20971764748-2*2**30<8*2**30'in guardtext,'unchanged history96GiB/cold reserve/metadata64MiB/free8GiB/fresh joint reserve')
    check("if now-stage>=600 or now-started>=1800:"in raw and 'if peak>=512:'in raw,'unchanged live child stage600/whole1800/SELF512 checks')
    check("if now-last_account>=5:check('live_'+case);last_account=now"in raw,'unchanged five-second actual resource account cadence')
    check("['/bin/ps','-o','rss=','-p',str(current.pid)]"in raw,'original actual full current child RSS diagnostic Source retained')
    check("bounded.start_liveness_watchdog(readfd,current.pid,bounded.TERM_GRACE_SECONDS)"in raw
        and "bounded.finish_liveness_watchdog(writefd,watchdog)"in raw
        and "bounded.terminate_group(current)"in raw,'original unchanged bounded watchdog/termination methods used')
    finalizers=[n for n in ast.walk(loop)if isinstance(n,ast.Try)and n.finalbody]
    complete_finalizer=next((n for n in finalizers if 'actual_wait_return=current.wait(timeout=0)'in '\n'.join(ast.get_source_segment(raw,s)for s in n.finalbody)),None)
    check(complete_finalizer is not None,'actual original wait and complete stream fsync in per-attempt finally')
    finaltext='\n'.join(ast.get_source_segment(raw,s)for s in complete_finalizer.finalbody)
    check("bounded.terminate_group(current)"in finaltext and "actual_wait_return=current.wait(timeout=0)"in finaltext,'original bounded failure termination then actual original wait observation')
    check("for name,stream in(('stdout',stdout),('stderr',stderr)):"in finaltext and 'os.fsync(stream.fileno())'in finaltext,'both actual complete streams flush/fsync on normal and failed attempt paths')
    check("cleanup_error('actual_original_Popen_wait',error)"in finaltext and "cleanup_error('original_bounded_terminate_group',error)"in finaltext
        and "cleanup_error('original_bounded_finish_liveness_watchdog',error)"in finaltext,'actual termination/wait/watchdog failures saved separately')
    looptext=ast.get_source_segment(raw,loop)
    check("pid=None if current is None else current.pid"in looptext and "returncode=None if current is None else current.returncode"in looptext,'real attempted PID/returncode retained; unlaunched or unknown stays None')
    check('actual_error=actual_error,actual_cleanup_errors=cleanup_errors'in looptext and 'actual_original_Popen_wait_return=actual_wait_return'in looptext,'original actual error distinct from cleanup error and actual wait return')
    check("stream_pins[name]=None;cleanup_error(name+'_complete_stream_full_EOF_pin',error)"in looptext,'full EOF log pin failure retained without forged pin')
    check("records.append(record);write(folder/'Root_actual_terminal.json',record)"in looptext,'every attempt gets terminal record before error propagation')
    check(looptext.index("records.append(record);write(folder/'Root_actual_terminal.json',record)")<looptext.index('if attempt_exception is not None:raise attempt_exception'),'failed attempt terminal persisted before stopping later cases')
    check('if cleanup_errors:raise RuntimeError'in looptext and 'if not wait_return_observed or current is None or current.returncode!=0:raise RuntimeError'in looptext,'cleanup/wait/nonzero failures stop serial loop; no retries or zero promotion')
    check('unknown_or_failed_wait_promoted_to_zero=False'in looptext and 'raw_wait_status_tuple_claimed=False'in looptext,'no raw wait tuple or normalized unknown-success claim')
    check("status='ALL_TEN_ACTUAL_CONTROLS_CLOSED0_SAVED_REVIEW_REQUIRED'if failure is None else 'FAILED_ACTUAL_CONTROLS_NO_RETRY'"in raw
        and 'all_ten_control_entries_closed0=failure is None and len(records)==10'in raw,'ten success requires all original case entries completed and no failure')
    prelaunch=E/'Source_prelaunch_review.json';pp=pin(prelaunch);r=json.loads(prelaunch.read_bytes())
    check(r['schema']=='INDEPENDENT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_PRELAUNCH_REVIEW_V1'and r['source_only']is True
        and r['all_checks_passed']is True and r['blockers']==[],'actual admitted complete ten-control current Source review')
    check(pp['sha256']=='7864b1428c25d91d7c82d0de312b9c95f890d3a4ec09c82d717f8f771addffe1','unchanged complete D/E prelaunch review')
    for key in('new_Source_binding_pin','adapter_Source_pin','control_entry_Source_pin'):
        check(pin(r[key]['path'])==r[key],'inner genuine control binding/Source unchanged '+key)
    for p in r['complete_original21_current_author_pins'].values():check(pin(p['path'])==p,'inner original author Source unchanged '+p['path'])
    for p in r['original_guard_Source_pins']:check(pin(p['path'])==p,'inner original guard class/method/MRO Source unchanged '+p['path'])
    check(r['original_case_order']==['closed-before-first','exit7','transient','unlinked-duplicates','escaped','echild','unobserved-cache','deadline','persistent-topology','journal-failure'],'all original ten cases unique and serial')
    check(pin(ROOT_SOURCE)==sourcepin,'final edited Root boundary current full EOF unchanged through pure AST review')
    result=dict(schema='INDEPENDENT_FINAL_ROOT_SERIAL_CONTROL_BOUNDARY_SOURCE_REVIEW_V1',source_only=True,
        status='PASS_SOURCE_STRUCTURE_ONLY_REAL_EXECUTION_REQUIRED',all_checks_passed=True,blockers=[],
        reviewed_Root_serial_boundary_Source_pin=sourcepin,reviewer_Source_pin=pin(Path(__file__).resolve()),
        current_inner_Source_prelaunch_review_pin=pp,actual_checks=CHECKS,check_count=len(CHECKS),
        original_inner_OwnRSS_owner_MRO_methods_Source_unchanged=True,
        per_attempt_error_cleanup_wait_and_complete_stream_records_preserved=True,
        unknown_wait_or_failed_child_promoted_to_zero=False,remaining_cases_not_launched_on_failure=True,
        original_caps_or_case_order_changed=False,D_E_Source_contract_dependencies_added=False,
        actual_PS_lsof_or_child_executed=False,OS_outcome_mocked=False,
        actual_controls_or_Native_qualified=False,scientific_qualification=False,actual_goal_achieved=False,
        limitations=['This is complete Source/AST and current pin verification. Actual child closure, complete stream files, resource observations and ten-control results require one real bounded run.',
            'The outer boundary records actual original Popen wait returns and explicitly does not claim raw wait status tuples; the unchanged inner owner observer supplies its own original recorded-wait evidence.'],
        actual_elapsed_seconds=time.monotonic()-START)
    out=HERE/'FINAL_ROOT_SERIAL_BOUNDARY_SOURCE_REVIEW.json'
    with out.open('x',encoding='utf-8')as stream:json.dump(result,stream,ensure_ascii=False,allow_nan=False,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=pin(out),final_Root_Source_pin=sourcepin,
        checks=len(CHECKS),actual_PS_lsof_or_child_executed=False),allow_nan=False),flush=True)

if __name__=='__main__':main()

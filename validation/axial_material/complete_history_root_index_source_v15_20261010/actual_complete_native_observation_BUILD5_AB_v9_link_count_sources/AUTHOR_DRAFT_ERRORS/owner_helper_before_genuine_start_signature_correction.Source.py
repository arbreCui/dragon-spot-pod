"""UNREADY exact owned-Popen evidence; no import-time actions or qualification.

Only the Root-qualified complete runtime may attach this to a genuine original
runner.  No class, MRO, global wait API, cleanup callable, or guard Source is
replaced.  The declared per-instance wait instrumentation records actual waitpid
tuples under the original Popen lock.  ECHILD is unknown, never synthetic zero.
"""
import errno
import hashlib
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import threading
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_REQUIRES_ACTUAL_CONTROLS'
EXPECTED_STDLIB_PATH = '/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/subprocess.py'
EXPECTED_STDLIB_SHA256 = '85d29b2bf0249f5436838298c9a60ee93508b1102e9ac43b001f8a7e7ae8f375'

class OwnershipUnknown(RuntimeError):
    """A non-OSError refusal which original Popen cannot convert into zero."""

def require(value, message):
    if type(value) is not bool or not value:
        raise OwnershipUnknown(message)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def actual_stdlib_Source(expected):
    require(type(expected) is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact stdlib Source fullpin')
    require(expected['path']==EXPECTED_STDLIB_PATH and expected['sha256']==EXPECTED_STDLIB_SHA256,'single exact original Python subprocess Source role')
    require(type(expected['size_bytes']) is int and expected['size_bytes']==88747 and type(expected['identity']) is list and len(expected['identity'])==7 and all(type(x) is int and x>=0 for x in expected['identity']),'typed original stdlib Source pin')
    p=Path(expected['path']);before=identity(p.lstat())
    require(before==expected['identity'] and before[3]>=1 and stat.S_ISREG(before[2]) and all(not q.is_symlink() for q in (p,*p.parents)),'exact actual positive stdlib link count only')
    with p.open('rb') as stream:
        require(identity(os.fstat(stream.fileno()))==before,'stdlib opened identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require(identity(os.fstat(stream.fileno()))==before,'stdlib EOF identity')
    require(identity(p.lstat())==before and digest==expected['sha256'],'complete stdlib Source unchanged')
    require(Path(subprocess.__file__).resolve()==p and subprocess.Popen.__module__=='subprocess','exact loaded original stdlib module')
    return expected

class ExactOwnerScopeObserver:
    """Current full parent closure plus captured descendants and actual PGIDs.

    A process can leave a group before any census.  Such ownership cannot be
    recovered from later PS output: a leader closed before its first observed
    live census makes this observer refuse, even if its group is now empty.
    Closed cached returncode without a real recorded wait status also refuses.
    No observed group absence is called historical cleanup or atomic closure.
    """
    def __init__(self,runner,resources,monitor,full,stdlib_pin,started,deadline_getter,control_mode=False):
        require(type(control_mode) is bool,'explicit Source-bound controls mode')
        require(type(runner) is full.OwnRSSSerialExecutor and runner.resources is resources,'exact genuine runner object and resources')
        require(resources._genuine_full is full,'factory/genuine class identity')
        actual_stdlib_Source(stdlib_pin)
        self.runner=runner;self.resources=resources;self.monitor=monitor;self.full=full
        self.started=started;self.deadline_getter=deadline_getter;self.control_mode=control_mode
        self.original_waitpid=os.waitpid;self.original_Popen=subprocess.Popen
        self.original_poll_code=subprocess.Popen._internal_poll.__code__
        self.original_try_wait_code=subprocess.Popen._try_wait.__code__
        self.original_process_code=full.OwnRSSSerialExecutor._process.__code__
        self.original_start=None;self.start_wrapper=None
        self.owners={};self.captured_descendants=set();self.last_scope=None;self.unknown=[]
        self.host_pid=os.getpid();self.stdlib_pin=stdlib_pin;self.restored=False
        self.environment()
    def environment(self):
        require(time.monotonic()-self.started<1800,'unchanged whole1800 clock')
        deadline=self.deadline_getter()
        require(deadline is None or time.monotonic()<deadline,'unchanged active stage600 clock')
        require(os.waitpid is self.original_waitpid and subprocess.Popen is self.original_Popen,'original global APIs never replaced')
        require(subprocess.Popen._internal_poll.__code__ is self.original_poll_code and subprocess.Popen._try_wait.__code__ is self.original_try_wait_code,'original class wait methods unchanged')
        require(self.full.OwnRSSSerialExecutor._process.__code__ is self.original_process_code,'original genuine process method unchanged')
        require(threading.current_thread() is threading.main_thread() and len(threading.enumerate())==1,'actual main-thread sole Python waiter prerequisite')
        require(signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL,'actual default SIGCHLD; no ignored or custom status handler')
        require(sys.getprofile() is None and sys.gettrace() is None and not sys.flags.optimize,'uninstrumented nonoptimized Python environment')
    def fail(self,message,record=None):
        evidence=dict(message=message,record=record)
        self.unknown.append(evidence)
        raise OwnershipUnknown(message)
    def record_wait(self,owner,flags):
        self.environment()
        process=owner['process']
        require(process._waitpid_lock.locked(),'original Popen wait lock held during single original waitpid call')
        require(type(flags) is int and flags in (0,os.WNOHANG),'original permitted wait flags only')
        try:
            result=self.original_waitpid(process.pid,flags)
        except OSError as error:
            record=dict(pid=process.pid,wait_flags=flags,actual_errno=error.errno,actual_error=repr(error),closed_proven=False)
            owner['last_wait']=record
            # Non-OSError is deliberate: the original poll/ECHILD handler
            # must not synthesize zero from unknown ownership or permissions.
            self.fail('actual owned waitpid failed; no ECHILD-zero fallback',record)
        require(type(result) is tuple and len(result)==2 and all(type(x) is int for x in result),'actual typed waitpid tuple')
        pid,status=result
        record=dict(pid=process.pid,wait_flags=flags,actual_waitpid_pid=pid,actual_wait_status=status,closed_proven=False)
        owner['last_wait']=record
        require(pid in (0,process.pid) and status>=0,'original exact own waitpid result')
        if pid==process.pid:
            require(os.WIFEXITED(status) or os.WIFSIGNALED(status),'stopped/traced status is not process closure')
            record['closed_proven']=True
            record['actual_exit_code']=os.waitstatus_to_exitcode(status)
            owner['closed_wait']=dict(record)
        return result
    def register(self,process,role,args):
        self.environment()
        require(type(process) is self.original_Popen and type(process.pid) is int and process.pid>0,'actual exact original Popen instance/PID')
        require(process.returncode is None and process.args==args,'registration before any unobserved cached status')
        require(process.pid not in self.owners,'no PID reuse or duplicate owner registration')
        require('_internal_poll' not in process.__dict__ and '_try_wait' not in process.__dict__,'no preexisting instance wait overrides')
        original_poll=process._internal_poll;original_try_wait=process._try_wait
        require(original_poll.__self__ is process and original_poll.__func__.__code__ is self.original_poll_code,'exact original bound poll')
        require(original_try_wait.__self__ is process and original_try_wait.__func__.__code__ is self.original_try_wait_code,'exact original bound try_wait')
        defaults=original_poll.__func__.__defaults__
        require(len(defaults)==4 and defaults[0] is None and defaults[1] is self.original_waitpid and defaults[2]==os.WNOHANG and defaults[3]==errno.ECHILD,'exact original poll defaults')
        owner=dict(process=process,pid=process.pid,pgid=process.pid,role=role,args=args,
            original_poll=original_poll,original_try_wait=original_try_wait,closed_wait=None,last_wait=None,
            live_census_seen=False,descendants=set())
        def tracked_waitpid(pid,flags):
            require(type(pid) is int and pid==process.pid,'wait callback exact own PID')
            return self.record_wait(owner,flags)
        def tracked_poll(_deadstate=None,_waitpid=defaults[1],_WNOHANG=defaults[2],_ECHILD=defaults[3]):
            self.environment()
            require(_waitpid is defaults[1] and _WNOHANG==defaults[2] and _ECHILD==defaults[3],'no injected alternate wait implementation')
            if process.returncode is not None:
                proof=owner['closed_wait']
                require(proof is not None and type(process.returncode) is int and process.returncode==proof['actual_exit_code'],'cached status requires actual recorded exit tuple')
            result=original_poll(_deadstate=_deadstate,_waitpid=tracked_waitpid,_WNOHANG=_WNOHANG,_ECHILD=_ECHILD)
            if result is not None:
                proof=owner['closed_wait']
                require(proof is not None and type(result) is int and result==proof['actual_exit_code'],'poll returned exact real exit status')
            return result
        def tracked_try_wait(wait_flags):
            # This finite replacement reproduces the original normal body,
            # delegating original os.waitpid once under its original lock.
            # Its original ChildProcessError->(pid,0) fallback is refused.
            return self.record_wait(owner,wait_flags)
        process._internal_poll=tracked_poll;process._try_wait=tracked_try_wait
        owner['poll_wrapper']=tracked_poll;owner['try_wrapper']=tracked_try_wait
        self.owners[process.pid]=owner
        return owner
    def install_original_start_capture(self):
        require(self.original_start is None,'install original start capture once')
        original=self.runner.bounded.start_liveness_watchdog
        require(callable(original),'original bounded start callable')
        self.original_start=original
        def start_liveness_watchdog(guard_source,child_pgid,grace=0.8):
            frame=sys._getframe(1)
            try:
                require(frame.f_code is self.original_process_code and frame.f_locals.get('self') is self.runner,'exact genuine _process caller frame/runner')
                process=frame.f_locals.get('process');command=frame.f_locals.get('command')
                require(type(child_pgid) is int and process is not None and child_pgid==process.pid,'original new-session child group equals exact Popen PID')
                require(Path(guard_source).resolve()==Path(self.runner.bounded.__file__).resolve(),'original pinned bounded Source path')
                self.register(process,'business',command)
            finally:
                del frame
            # The exact original start is called once.  No new business child,
            # waiter, poll loop, retry, or cleanup action is added here.
            result=original(guard_source,child_pgid,grace)
            read_fd,write_fd,watchdog=result
            self.register(watchdog,'watchdog',watchdog.args)
            return result
        self.start_wrapper=start_liveness_watchdog
        self.runner.bounded.start_liveness_watchdog=start_liveness_watchdog
        return self
    def poll_for_snapshot(self):
        self.environment()
        for owner in self.owners.values():
            process=owner['process']
            require(process._internal_poll is owner['poll_wrapper'] and process._try_wait is owner['try_wrapper'],'exact owned instance wait wrappers retained')
            process.poll()
        require(not self.unknown,'unknown wait observation cannot acquire scope qualification')
    def expand_selection(self,rows,original_parent_closure,diagnostic_pid):
        self.environment()
        require(type(rows) is dict and all(type(pid) is int and pid>0 and type(row) is dict and set(row)=={'pid','ppid','pgid'} and row['pid']==pid and all(type(row[k]) is int and row[k]>=0 for k in row) for pid,row in rows.items()),'strict complete actual fullPS row table')
        require(type(original_parent_closure) is set and self.host_pid in original_parent_closure,'full original host parentchain retained')
        selected=set(original_parent_closure)
        groups={o['pgid'] for o in self.owners.values()}
        # Remember descendants before closed-parent exclusion.  Existing
        # captured descendants and any current same-group reparented member
        # remain in the union, even after an exact leader was reaped.
        selected|={p for p,r in rows.items() if r['pgid'] in groups}
        selected|={p for p in self.captured_descendants if p in rows}
        while True:
            expanded=selected|{p for p,r in rows.items() if r['ppid'] in selected}
            if expanded==selected:break
            selected=expanded
        self.captured_descendants|=selected-{self.host_pid,diagnostic_pid}
        excluded=[]
        for pid,owner in self.owners.items():
            row=rows.get(pid);proof=owner['closed_wait']
            if proof is None:
                require(owner['process'].returncode is None,'no unproven cached closed returncode')
                require(row is not None and row['pgid']==owner['pgid'],'unclosed exact owner present in fullPS with original actual group')
                owner['live_census_seen']=True;selected.add(pid)
            else:
                require(owner['live_census_seen'],'leader closed before any live census: escaped descendants ownership remains unknown')
                require(row is None,'closed exact PID reappeared or census raced; no reuse/unknown exclusion')
                selected.discard(pid);excluded.append(dict(pid=pid,role=owner['role'],actual_closed_wait=proof))
        selected.discard(diagnostic_pid)
        require(self.host_pid in selected and not self.unknown,'host retained; all unknowns fail closed')
        self.last_scope=dict(current_actual_parentchain=sorted(original_parent_closure),captured_descendants=sorted(self.captured_descendants),captured_original_groups=sorted(groups),actual_selected_PIDs=sorted(selected),individually_proven_closed_exclusions=excluded,
            current_full_PS_rows={str(p):r for p,r in rows.items() if p in selected or r['pgid'] in groups},
            atomic_or_continuous_ownership_claimed=False,escaped_before_first_census_proven=False)
        return selected
    def summary(self):
        return dict(schema='ACTUAL_N8_EXACT_OWNER_SCOPE_STATE_V1',actual_host_PID=self.host_pid,
            owners=[dict(pid=o['pid'],pgid=o['pgid'],role=o['role'],args=o['args'],last_wait=o['last_wait'],closed_wait=o['closed_wait'],live_census_seen=o['live_census_seen']) for o in self.owners.values()],
            last_actual_scope=self.last_scope,unknown=list(self.unknown),restored=self.restored,
            current_default_SIGCHLD_and_single_main_thread_required=True,
            ECHILD_never_synthetic_zero=True,original_classes_MRO_guard_Source_unchanged=True,
            waitid_API_used=False,new_monitor_qualification_created=False)
    def restore_original_objects(self):
        if self.original_start is not None:
            require(self.runner.bounded.start_liveness_watchdog is self.start_wrapper,'start wrapper identity before restoration')
            self.runner.bounded.start_liveness_watchdog=self.original_start
        for owner in self.owners.values():
            process=owner['process']
            require(process._internal_poll is owner['poll_wrapper'] and process._try_wait is owner['try_wrapper'],'owned wrappers identity before restoration')
            del process._internal_poll;del process._try_wait
        self.restored=True


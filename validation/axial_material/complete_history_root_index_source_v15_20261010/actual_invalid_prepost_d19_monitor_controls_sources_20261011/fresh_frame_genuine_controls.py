"""UNREADY finite real controls for the NEW fresh-frame Source, no native work.

Six groups, ten separately bound cases. Each invocation has one genuine
business Popen, no restart, fresh H/O/C and its own original whole1800/stage600.
An expected negative control does not convert the failed business stage to PASS.
Root must independently save the real tool terminal and current group closure.

The complete-candidate, fatal, cleanup and failure-result paths are unchanged.
ADAPTER_SHA pins the new private invalid append: one genuinely current full
preappend account, exact complete UTF8 admission, and one true full postappend
account inside the SAME original fixed two-second window. Last-only completed
in-memory proofs are observed and coupled to real saved invalid UTF8 lines; no
prewrite raw event claims a future postaccount. Old ten/16 qualification is not
inherited. All ten real fixtures require a new actual Root run.
"""
import argparse
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

SUPPORT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
ADAPTER_SHA='a2b507e0f5e5470c227484f1d8a1e63367aed2313cb15695a9c46b57a2d444cc'
POLICY='FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
GROUPS={'transient':'01_transient_then_fresh','escaped':'02_captured_escape_and_topology',
 'closed-before-first':'03_real_wait_and_unknown','echild':'03_real_wait_and_unknown',
 'unobserved-cache':'03_real_wait_and_unknown','deadline':'04_deadline_and_journal',
 'persistent-topology':'04_deadline_and_journal',
 'journal-failure':'04_deadline_and_journal','unlinked-duplicates':'05_unlinked_and_ownappend',
 'exit7':'06_real_nonzero_stays_failed'}
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)

def read(raw):
    def pairs(items):
        result={}
        for k,v in items:require(k not in result,'duplicate control META key');result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def pin(path):
    path=Path(path);s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(path.is_absolute()and all(not q.is_symlink()for q in(path,*path.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'ordinary full Source/META pin')
    with path.open('rb')as stream:
        require([getattr(os.fstat(stream.fileno()),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]==before,'control Source opened identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require([getattr(os.fstat(stream.fileno()),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]==before,'control Source EOF identity')
    require([getattr(path.lstat(),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]==before,'control Source unchanged')
    return dict(path=str(path),sha256=digest,size_bytes=s.st_size,identity=before)

def metadata(p):
    require(type(p)is dict and pin(p['path'])==p,'full Source/META pin matched')
    return read(Path(p['path']).read_bytes())

def write_new(path,value):
    path=Path(path);temporary=path.with_name(path.name+'.'+str(os.getpid())+'.writing')
    require(not os.path.lexists(path),'fresh actual control marker, no overwrite')
    with temporary.open('x')as stream:
        json.dump(value,stream,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    require(not os.path.lexists(path),'fresh marker remains absent before atomic rename')
    temporary.rename(path)

def wait_file(path,deadline):
    while not path.exists():
        require(time.monotonic()<deadline,'control wait within original/active deadline');time.sleep(.005)
    return read(path.read_bytes())

def private_child(case,root,deadline,parent):
    root=Path(root)
    require(os.getppid()==parent and os.environ.get('AXMAT_FRESH_FRAME_GENUINE_CONTROL_PARENT')==str(parent),'private fixture only from bound genuine control host')
    require(root.is_absolute()and root.is_dir()and all(os.environ.get(k)=='1'for k in THREAD_KEYS),'private fixture root and original one-thread environment')
    if case=='closed-before-first':return
    if case=='persistent-topology':
        generation=0
        while not(root/'leader_release').exists():
            require(time.monotonic()<deadline,'private churn within original stage600')
            child=os.fork();suffix=format(generation,'04d')
            if child==0:
                write_new(root/('descendant_ready_'+suffix+'.json'),dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),generation=generation))
                release=root/('descendant_release_'+suffix)
                while not release.exists()and not(root/'leader_release').exists():
                    require(time.monotonic()<deadline,'private churn child within original stage600');time.sleep(.005)
                os._exit(0)
            if generation==0:write_new(root/'leader_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),descendant_pid=child))
            write_new(root/('generation_'+suffix+'.json'),dict(pid=child,generation=generation))
            waited,status=os.waitpid(child,0)
            write_new(root/('descendant_real_wait_'+suffix+'.json'),dict(pid=waited,status=status,exited=os.WIFEXITED(status),exitcode=os.waitstatus_to_exitcode(status)))
            generation+=1
        return
    fd=None;duplicate=None;child=None
    if case in('transient','escaped','unlinked-duplicates','journal-failure'):
        target=root/'actual_deleted_control_file'
        fd=os.open(target,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
        data=b'actual private control bytes\n';os.write(fd,data);os.fsync(fd)
        duplicate=os.dup(fd);os.unlink(target)
        child=os.fork()
        if child==0:
            try:
                write_new(root/'descendant_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),actual_fds=[fd,duplicate],actual_size_bytes=len(data)))
                if case=='escaped':
                    wait_file(root/'escape_release',deadline);os.setsid()
                    write_new(root/'escaped_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp()))
                wait_file(root/'descendant_release',deadline)
            finally:
                os.close(duplicate);os.close(fd)
            os._exit(0)
    write_new(root/'leader_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),descendant_pid=child))
    if case in('transient','journal-failure'):
        wait_file(root/'descendant_release',deadline)
        waited,status=os.waitpid(child,0)
        write_new(root/'descendant_real_wait.json',dict(pid=waited,status=status,exited=os.WIFEXITED(status),exitcode=os.waitstatus_to_exitcode(status)))
    wait_file(root/'leader_release',deadline)
    if child is not None and case=='unlinked-duplicates':
        if not(root/'descendant_release').exists():write_new(root/'descendant_release',{})
        waited,status=os.waitpid(child,0)
        write_new(root/'descendant_real_wait.json',dict(pid=waited,status=status,exited=os.WIFEXITED(status),exitcode=os.waitstatus_to_exitcode(status)))
    if duplicate is not None:os.close(duplicate);os.close(fd)
    if case=='exit7':raise SystemExit(7)

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--binding',required=True);cli.add_argument('--binding-sha256',required=True)
    cli.add_argument('--independent-prelaunch-review',required=True)
    cli.add_argument('--case',required=True,choices=tuple(GROUPS));a=cli.parse_args()
    started=time.monotonic();binding_pin=pin(a.binding)
    require(binding_pin['sha256']==a.binding_sha256,'exact new Source binding SHA')
    b=metadata(binding_pin)
    require(b['schema']=='ROOT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_BINDING_V1'and b['source_only']is True and b['policy']==POLICY and b['original_caps']==CAPS and all(type(v)is int for v in b['original_caps'].values())and b['actual_control_execution']is None and b['old_controls_qualification_inherited']is False,'new finite Source contract, no old Q inheritance')
    require(b['adapter_Source_pin']['sha256']==ADAPTER_SHA,'exact new invalid pre/post adapter Source; old ten controls not inherited')
    require(pin(Path(__file__).resolve())==b['control_entry_Source_pin'],'this exact new control entry Source')
    base=metadata(b['original_N9_controls_Source_binding_pin']);author=base['actual_author_Source_contract']
    require(base['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1'and base['source_only']is True and base['original_caps']==CAPS,'original Source-binding provenance only')
    for p in author.values():require(pin(p['path'])==p,'all original control Source owners full EOF unchanged')
    require(b['owner_helper_Source_pin']==author['owner_scope_helper']and b['actual_stdlib_subprocess_Source_pin']==base['actual_stdlib_subprocess_Source_pin']and b['tool_pins']==base['tool_pins'],'original owner helper/stdlib/tools unchanged')
    review_pin=pin(a.independent_prelaunch_review);review=metadata(review_pin)
    require(review['schema']=='INDEPENDENT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_PRELAUNCH_REVIEW_V1'and review['source_only']is True and review['all_checks_passed']is True and review['blockers']==[] and review['new_Source_binding_pin']==binding_pin and review['adapter_Source_pin']==b['adapter_Source_pin']and review['control_entry_Source_pin']==b['control_entry_Source_pin'],'independent new Source-only review, no claimed execution')
    require(not sys.flags.optimize and sys.gettrace()is None and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREAD_KEYS),'original nonoptimized one-thread environment')
    require(hashlib.sha256(SUPPORT.read_bytes()).hexdigest()==SUPPORT_SHA,'original genuine support Source')
    spec=importlib.util.spec_from_file_location('fresh_frame_original_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    require(Path(sys.executable).resolve()==support.PYTHON,'original exact Python')
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'fresh_frame_original_helper')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'fresh_frame_original_resources')
    full,production=helper.modules();helper.guard_admission(full)
    runtime,actual_adapter=support.load(Path(b['adapter_Source_pin']['path']),b['adapter_Source_pin']['sha256'],'fresh_frame_new_Source')
    require(pin(b['adapter_Source_pin']['path'])==b['adapter_Source_pin'],'exact new adapter full pin')
    ns=b['case_namespaces'][a.case];roots=tuple(Path(ns[k])for k in('host','output','control','source','receipts'))
    host,out,control,source,receipts=roots
    require(len(set(roots))==5 and not any(p.is_relative_to(q)for p in roots for q in roots if p!=q),'disjoint HOCDE')
    require(all(p.is_absolute()and p!=support.ART and p.is_relative_to(support.ART)and all(not q.is_symlink()for q in(p,*p.parents))for p in roots[:3])and all(p.is_relative_to(support.BASE)and p!=support.BASE for p in roots[3:]),'original ART/base namespace scope')
    require(not any(os.path.lexists(p)for p in roots[:3]),'fresh HOC, zero business retries')
    dfreeze,efreeze=runtime.tree(source),runtime.tree(receipts)
    host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir();(host/'CONTROLS').mkdir()
    shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
    require(pin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original bounded Source bytes')
    history=resource.history_roots([str(p)for p in(host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    resources,monitor=runtime.build_exact_owner_resources(support,roots,b['tool_pins'],started,dfreeze,efreeze,history,(resource,full,production))
    resources._fresh_frame_Source_contract=dict(policy=POLICY,adapter_Source_pin=b['adapter_Source_pin'],new_Source_binding_pin=binding_pin,old_controls_qualification_inherited=False)
    before=resources.check()
    require(before['artifact_bytes']+2*2**30<96*2**30 and before['disk_free_bytes']-2*2**30>=8*2**30,'original reserve within unchanged caps')
    runner=full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'CONTROLS',resources)
    runner.env['AXMAT_FRESH_FRAME_GENUINE_CONTROL_PARENT']=str(os.getpid())
    monitor.install_bounded_wrappers(runner);deadline=time.monotonic()+600;monitor.stage_deadline=deadline
    observer=runtime.attach_exact_owner_observer(runner,resources,monitor,b['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,b['owner_helper_Source_pin'],support,control_mode=True)
    transitions=[];triggered=False;actual_error=None;after=None
    completed_invalid_append_proofs=[];seen_invalid_append_keys=set()
    after_execute_observed_monotonic=None;persistent_negative_deadline_basis=None
    def observe_completed_invalid_append_proof(phase):
        # Observe only a proof the production helper already completed. Do not
        # patch the monitor, replay accounts or supplement its saved raw event.
        proof=getattr(monitor,'_fresh_frame_last_invalid_append_proof',None)
        if proof is None:return
        require(type(proof)is dict and proof.get('actual_pre_and_post_full_accounts_completed')is True
            and proof.get('actual_original_disk_account_calls_completed')==2
            and proof.get('failed_frame_accepted')is False and proof.get('resource_PASS')is False,
            'only genuinely completed two-call invalid proof, never future postaccount or resource PASS')
        key=(proof['complete_appended_UTF8_sha256'],proof['exact_complete_appended_UTF8_bytes'],proof['fixed_window_started_monotonic'])
        if key in seen_invalid_append_keys:return
        observed=time.monotonic()
        snapshot=read(json.dumps(proof,ensure_ascii=False,allow_nan=False))
        require(observed>=snapshot['actual_post_append_full_account_returned_monotonic'],
            'real completed postaccount preceded this observation')
        seen_invalid_append_keys.add(key);completed_invalid_append_proofs.append(snapshot)
        transitions.append(dict(event='actual_completed_invalid_prepost_append_observation',
            phase=phase,actual_observed_monotonic=observed,actual_proof=snapshot))
    def barrier(rows,selected):
        nonlocal triggered
        observe_completed_invalid_append_proof('original_barrier_beginning')
        end=min(deadline,resources._fresh_frame_active_deadline)
        owners=[o for o in observer.owners.values()if o['role']=='business']
        if not owners:return
        owner=owners[-1]
        if not(out/'leader_ready.json').exists():return
        ready=read((out/'leader_ready.json').read_bytes())
        require(ready['pid']==owner['pid']and ready['pgid']==owner['pgid'],'actual ready matches original registered owner')
        last=getattr(resources,'_fresh_frame_last_accepted',{})
        if a.case=='persistent-topology':
            ready_paths=sorted(out.glob('descendant_ready_*.json'))
            for path in ready_paths:
                desc=read(path.read_bytes());target=desc['pid'];suffix=format(desc['generation'],'04d')
                release=out/('descendant_release_'+suffix)
                if release.exists():continue
                if target not in selected or target not in rows:return
                require(not rows[target]['state'].startswith('Z')and all(rows[target][k]==desc[k]for k in('pid','ppid','pgid')),'actual live churn descendant before release')
                triggered=True;write_new(release,{})
                waited=wait_file(out/('descendant_real_wait_'+suffix+'.json'),end)
                require(waited['pid']==target and waited['exited']is True and waited['exitcode']==0,'real parent wait for each churn generation')
                transitions.append(dict(event='actual_each_frame_descendant_exit',actual_row=rows[target],actual_wait=waited))
                return
            # If pre-PS caught the real inter-fork gap, wait for the next real
            # child before post-PS. It stays alive until a later pre census
            # selects it. Thus this control invalidates the gap frame too.
            next_generation=0 if not ready_paths else read(ready_paths[-1].read_bytes())['generation']+1
            wait_file(out/('descendant_ready_'+format(next_generation,'04d')+'.json'),end)
            return
        if triggered:
            if a.case in('transient','unlinked-duplicates')and last.get('open_unlinked_bytes')==29:
                if not(out/'leader_release').exists():write_new(out/'leader_release',{})
            if a.case=='escaped'and last.get('open_unlinked_bytes')==29:
                escape=[e for e in transitions if e['event']=='actual_escape_and_closed_leader']
                if escape:
                    target=escape[-1]['actual_escape']['pid']
                    scan=monitor.latest_original_scan or{}
                    post=(scan.get('fresh_frame_post_PS')or{}).get('complete_rows')or{}
                    row=post.get(target)
                    if target in last.get('live_own_processes_observed',[])and row is not None and row['pgid']==target and row['ppid']!=owner['pid']:
                        if not(out/'descendant_release').exists():write_new(out/'descendant_release',{})
            return
        if a.case in('transient','escaped','unlinked-duplicates','journal-failure'):
            if not(out/'descendant_ready.json').exists():return
            desc=read((out/'descendant_ready.json').read_bytes());target=desc['pid']
            if target not in selected or target not in rows:return
            require(target in selected and target in rows and not rows[target]['state'].startswith('Z')and all(rows[target][k]==desc[k]for k in('pid','ppid','pgid')),'real selected live descendant before transition')
            transitions.append(dict(event='actual_selected_descendant_before_transition',ready=desc,actual_row=rows[target]))
        triggered=True
        if a.case in('transient','journal-failure'):
            if a.case=='journal-failure':
                path=host/'runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'
                # Initial successful frame already wrote this ordinary file.
                # Move its complete bytes within H, then create a real directory
                # at the exact next append target: no OS outcome is mocked.
                path.rename(host/'runtime/INITIAL_COMPLETE_FRAME_JOURNAL.jsonl');path.mkdir()
            write_new(out/'descendant_release',{})
            waited=wait_file(out/'descendant_real_wait.json',end)
            require(waited['pid']==target and waited['exited']is True and waited['exitcode']==0,'actual descendant parent wait tuple')
            transitions.append(dict(event='actual_descendant_parent_wait',actual_wait=waited))
        elif a.case=='escaped':
            write_new(out/'escape_release',{})
            escaped=wait_file(out/'escaped_ready.json',end)
            require(escaped['pid']==target and escaped['pgid']==target,'actual descendant setsid, not fabricated PS')
            write_new(out/'leader_release',{})
            code=owner['process'].wait(timeout=max(.001,end-time.monotonic()))
            require(code==0 and owner['closed_wait']is not None,'actual leader reaped while captured descendant lives')
            transitions.append(dict(event='actual_escape_and_closed_leader',actual_escape=escaped,actual_owner_wait=owner['closed_wait']))
        elif a.case in('echild','unobserved-cache'):
            write_new(out/'leader_release',{})
            if a.case=='echild':
                while True:
                    pid,status=os.waitpid(owner['pid'],os.WNOHANG)
                    if pid==owner['pid']:break
                    require(pid==0 and time.monotonic()<end,'bounded actual external negative reaper');time.sleep(.005)
                transitions.append(dict(event='actual_external_reap_for_ECHILD',actual_pid_status=[pid,status]))
            else:
                while owner['original_poll']()is None:
                    require(time.monotonic()<end,'bounded original uninstrumented negative poll');time.sleep(.005)
                require(owner['process'].returncode==0 and owner['closed_wait']is None,'real original poll cache without observer wait proof')
                transitions.append(dict(event='actual_unobserved_original_poll_cache',cached_returncode=owner['process'].returncode,closed_wait=None))
        elif a.case=='deadline':
            write_new(out/'leader_release',{})
            while time.monotonic()<=end:time.sleep(.005)
            transitions.append(dict(event='actual_control_barrier_exceeded_fixed_window',actual_monotonic=time.monotonic(),fixed_deadline=end))
        elif a.case=='exit7':
            write_new(out/'leader_release',{})
            code=owner['process'].wait(timeout=max(.001,end-time.monotonic()))
            require(code==7 and owner['closed_wait']['actual_exit_code']==7,'actual original exit7 wait retained')
        elif a.case=='unlinked-duplicates':pass
    resources._actual_control_barrier=barrier
    if a.case=='closed-before-first':
        def early(owner,watchdog):
            code=owner['process'].wait(timeout=min(2,max(.001,deadline-time.monotonic())))
            require(code==0 and owner['closed_wait']is not None,'original real wait before first census')
            transitions.append(dict(event='actual_closed_before_first_census',actual_wait=owner['closed_wait']))
        observer.control_after_original_start=early
        resources._actual_control_barrier=None
    command=[str(support.PYTHON),'-B',str(Path(__file__).resolve()),'--private-child',a.case,str(out),repr(deadline),str(os.getpid())]
    try:
        try:runner.execute(host/'CONTROLS','actual_private_control',command,min(600,deadline-time.monotonic()))
        except BaseException as error:actual_error=runtime.monitor_error(error)
        after_execute_observed_monotonic=time.monotonic()
        observe_completed_invalid_append_proof('runner_execute_returned_or_refused')
        expected_negative=a.case in('echild','unobserved-cache','deadline','persistent-topology','journal-failure','exit7')
        require((actual_error is not None)==expected_negative,'genuine stage outcome must match positive or explicit negative control')
        require(a.case=='closed-before-first'or triggered,'real controls barrier occurred')
        events=[]
        journal=monitor.journal
        if journal is not None and journal.is_file():events=[read(line)for line in journal.read_bytes().splitlines()]
        events+=monitor.unpersisted
        invalid=[e for e in events if e.get('event')=='fresh_frame_invalid_not_resource_PASS']
        candidates=[e for e in events if e.get('event')=='fresh_frame_complete_candidate']
        if a.case=='transient':
            targets={e['ready']['pid']for e in transitions if e['event']=='actual_selected_descendant_before_transition'}
            matching=[]
            for event in invalid:
                f=event['complete_frame'];pre=f.get('pre_PS')or{};ls=f.get('lsof')or{}
                returned=ls.get('actual_returned_PIDs',[])
                refused=ls.get('actual_returncode')not in(None,0)or(ls.get('actual_returncode')==0 and any(p not in returned for p in targets))
                if pre.get('actual_returncode')==0 and pre.get('streams_complete')is True and ls.get('streams_complete')is True and any(p in(pre.get('actual_selected_PIDs')or[])for p in targets)and refused:
                    matching.append(event)
            require(bool(matching)and any(c['fixed_window_started_monotonic']==e['fixed_window_started_monotonic']and c['frame_ordinal']>e['frame_ordinal']for e in matching for c in candidates),'specific real selected-descendant lsof refusal then a NEW complete frame in the same window')
        if a.case=='escaped':
            escaped=[e for e in transitions if e['event']=='actual_escape_and_closed_leader']
            require(bool(escaped),'actual escape/leader real wait recorded')
            target=escaped[-1]['actual_escape']['pid'];leader=escaped[-1]['actual_owner_wait']['pid']
            captured=False
            for event in candidates:
                f=event['complete_frame'];post=f.get('post_PS')or{};row=(post.get('complete_rows')or{}).get(str(target))
                captured|=f.get('actual_complete_unlinked_bytes')==29 and target in(post.get('actual_selected_PIDs')or[])and row is not None and row['pgid']==target and row['ppid']!=leader
            require(any(e.get('complete_frame',{}).get('actual_pre_post_scope_equal')is False for e in invalid)and captured,'actual changed topology refused, then escaped/reparented FD in NEW complete frame')
        if a.case=='echild':require(any((o.get('last_wait')or{}).get('actual_errno')==errno.ECHILD for o in observer.owners.values())and any(e.get('event')=='fresh_frame_window_fatal_no_resource_PASS'and(e.get('actual_error')or{}).get('type','').endswith('.OwnershipUnknown')and 'actual owned waitpid failed; no ECHILD-zero fallback'in(e.get('actual_error')or{}).get('repr','')for e in events),'actual ECHILD OwnershipUnknown, never unrelated failure or synthetic zero')
        if a.case=='closed-before-first':
            owner=next(o for o in observer.owners.values()if o['role']=='business')
            require(owner['closed_wait']is not None and owner['closed_wait']['actual_exit_code']==0 and owner['live_census_seen']is False and owner['pid']not in observer.last_scope['actual_selected_PIDs'],'actual early closed wait0 excludes ONLY that owner without a live-census gate')
        if a.case=='unobserved-cache':
            require(any(e['event']=='actual_unobserved_original_poll_cache'for e in transitions)and any(e.get('event')=='fresh_frame_window_fatal_no_resource_PASS'and(e.get('actual_error')or{}).get('type','').endswith('.OwnershipUnknown')and 'cached status requires actual recorded exit tuple'in(e.get('actual_error')or{}).get('repr','')for e in events),'actual cache-proof OwnershipUnknown, not an unrelated deadline or cleanup error')
        if a.case=='deadline':require(any(e['event']=='actual_control_barrier_exceeded_fixed_window'for e in transitions),'actual elapsed deadline, not fake tool timeout')
        if a.case=='persistent-topology':
            controlled={e['actual_wait']['pid']for e in transitions if e['event']=='actual_each_frame_descendant_exit'}
            fatal=[e for e in events if e.get('event')=='fresh_frame_window_fatal_no_resource_PASS'and 'fresh-frame fixed total2s observation deadline'in(e.get('actual_error')or{}).get('repr','')]
            sustained=False
            for end_event in fatal:
                start=end_event['fixed_window_started_monotonic']
                same=[e for e in invalid if e['fixed_window_started_monotonic']==start and any(p in((e['complete_frame'].get('pre_PS')or{}).get('actual_selected_PIDs')or[])for p in controlled)]
                no_candidate=not any(e['fixed_window_started_monotonic']==start for e in candidates)
                last=getattr(resources,'_fresh_frame_last_accepted',{})
                sustained|=len(same)>=2 and no_candidate and last.get('fixed_window_started_monotonic')!=start
            if sustained:persistent_negative_deadline_basis='actual_saved_original_fatal_fixed_deadline'
            if not sustained:
                # A real invalid-helper account/clock error escapes. Its prior
                # recording error makes the unchanged original fatal persist
                # refuse; never fabricate a fatal line or a completed postproof.
                deadline_repr="ValueError('fresh-frame fixed total2s observation deadline')"
                helper_trace='in private_record_invalid_frame'
                adapter_path=b['adapter_Source_pin']['path']
                genuine_error=(type(actual_error)is dict
                    and actual_error.get('type')=='builtins.ValueError'
                    and actual_error.get('repr')==deadline_repr
                    and helper_trace in actual_error.get('complete_traceback','')
                    and adapter_path in actual_error.get('complete_traceback','')
                    and any(type(e)is dict and type(e.get('actual_record_appended'))is bool
                        and (e.get('recording_error')or{}).get('type')=='builtins.ValueError'
                        and (e.get('recording_error')or{}).get('repr')==deadline_repr
                        and helper_trace in(e.get('recording_error')or{}).get('complete_traceback','')
                        and adapter_path in(e.get('recording_error')or{}).get('complete_traceback','')
                        for e in monitor.recording_errors))
                if genuine_error and invalid:
                    latest=max(invalid,key=lambda e:e['sequence'])
                    start=latest['fixed_window_started_monotonic'];end=latest['fixed_window_deadline_monotonic']
                    same=[e for e in invalid if e['fixed_window_started_monotonic']==start
                        and e['fixed_window_deadline_monotonic']==end
                        and e.get('failed_frame_accepted')is False and e.get('resource_PASS')is False
                        and ((e.get('complete_frame')or{}).get('pre_PS')or{}).get('actual_returncode')==0
                        and ((e.get('complete_frame')or{}).get('pre_PS')or{}).get('streams_complete')is True
                        and ((e.get('complete_frame')or{}).get('post_PS')or{}).get('actual_returncode')==0
                        and ((e.get('complete_frame')or{}).get('post_PS')or{}).get('streams_complete')is True
                        and ((e.get('complete_frame')or{}).get('lsof')or{}).get('streams_complete')is True
                        and any(p in(((e.get('complete_frame')or{}).get('pre_PS')or{}).get('actual_selected_PIDs')or[])for p in controlled)]
                    last=getattr(resources,'_fresh_frame_last_accepted',{})
                    sustained=(type(start)is float and type(end)is float and end==start+2
                        and type(after_execute_observed_monotonic)is float and after_execute_observed_monotonic>=end
                        and len(same)>=2 and not any(e['fixed_window_started_monotonic']==start for e in candidates)
                        and last.get('fixed_window_started_monotonic')!=start
                        and any(r['status']=='FAILED'for r in runner.records))
                    if sustained:persistent_negative_deadline_basis='actual_private_invalid_append_fixed_deadline_error_with_original_recording_errors_preserved'
            require(sustained,'at least two actual controlled invalid frames, no candidate/accepted publication, and this same fixed2s deadline exhausted')
        if a.case=='journal-failure':require(bool(monitor.recording_errors)and bool(monitor.unpersisted),'actual journal destination failure stopped recovery')
        if a.case=='exit7':require(any(o['role']=='business'and o['closed_wait']is not None and o['closed_wait']['actual_exit_code']==7 for o in observer.owners.values())and any(r['status']=='FAILED'for r in runner.records),'real exit7 business stage remains FAILED')
        if a.case=='unlinked-duplicates':
            require(any(e['complete_frame'].get('actual_complete_unlinked_bytes')==29 and e['complete_frame'].get('actual_complete_unlinked_device_inode_count')==1 for e in candidates),'real duplicate FD unique D/i counted once at29B')
            duplicate_seen=False
            for event in candidates:
                records=[];row={}
                for line in event['complete_frame']['lsof']['actual_stdout'].splitlines():
                    if line.startswith('f'):
                        if row:records.append(row)
                        row={'f':line[1:]}
                    elif line and line[0]in'nsiDtk':row[line[0]]=line[1:]
                if row:records.append(row)
                counts={}
                for row in records:
                    if row.get('t')=='REG'and row.get('k')=='0'and row.get('s')=='29'and str(out)in row.get('n',''):
                        key=(row.get('D'),row.get('i'));counts[key]=counts.get(key,0)+1
                duplicate_seen|=any(all(k)and n>=2 for k,n in counts.items())
            require(duplicate_seen,'actual canonical lsof shows duplicate k0 D/i FD records')
            last=resources._fresh_frame_last_accepted
            require(last['complete_joint_HOCDE_bytes']>=last['actual_complete_frame_journal_pin']['size_bytes']+last['open_unlinked_bytes'],'accepted whole byte count includes its own complete journal')
        if not expected_negative:after=resources.check()
        # Proof validation reads the genuine complete UTF8 journal after the
        # business returned/refused. These are Source-bound observations only;
        # the two production accounts already finished inside the original 2s.
        invalid_raw_by_key={};actual_invalid_append_journal_snapshots=[]
        for journal_path in(host/'runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl',
                            host/'runtime/INITIAL_COMPLETE_FRAME_JOURNAL.jsonl'):
            if not journal_path.is_file():continue
            journal_pin=pin(journal_path);raw_journal=journal_path.read_bytes()
            require(pin(journal_path)==journal_pin and len(raw_journal)==journal_pin['size_bytes']
                and hashlib.sha256(raw_journal).hexdigest()==journal_pin['sha256'],
                'real whole invalid-proof journal snapshot EOF pin before and after read')
            actual_invalid_append_journal_snapshots.append(journal_pin)
            for raw_line in raw_journal.splitlines(keepends=True):
                require(raw_line.endswith(b'\n'),'complete saved UTF8 journal line with its true newline')
                event=read(raw_line)
                if event.get('event')!='fresh_frame_invalid_not_resource_PASS':continue
                key=(hashlib.sha256(raw_line).hexdigest(),len(raw_line),event['fixed_window_started_monotonic'])
                require(key not in invalid_raw_by_key,'one unique actual saved invalid UTF8 line for each proof')
                invalid_raw_by_key[key]=(event,journal_pin)
        actual_invalid_prepost_raw_couplings=[]
        for proof in completed_invalid_append_proofs:
            key=(proof['complete_appended_UTF8_sha256'],proof['exact_complete_appended_UTF8_bytes'],proof['fixed_window_started_monotonic'])
            require(key in invalid_raw_by_key,'completed invalid proof matches actual saved full UTF8 SHA/length/window')
            event,journal_pin=invalid_raw_by_key[key]
            start=proof['fixed_window_started_monotonic'];end=proof['fixed_window_deadline_monotonic']
            times=[proof[k]for k in('actual_pre_append_full_account_started_monotonic',
                'actual_pre_append_full_account_returned_monotonic','actual_post_append_full_account_started_monotonic',
                'actual_post_append_full_account_returned_monotonic')]
            require(all(type(v)is float and 0<=v<float('inf')for v in(start,end,*times))
                and end==start+2 and start<=times[0]<=times[1]<=times[2]<=times[3]<end,
                'both true full accounts completed in same unchanged original total2s window')
            require(event['fixed_window_started_monotonic']==start and event['fixed_window_deadline_monotonic']==end
                and event['failed_frame_accepted']is False and event['resource_PASS']is False
                and event['fresh_frame_policy']==POLICY
                and event['fresh_frame_Source_contract']['adapter_Source_pin']==b['adapter_Source_pin']
                and event['fresh_frame_Source_contract']['new_Source_binding_pin']==binding_pin,
                'saved original invalid event couples actual Source binding and rejects resource PASS')
            pre=proof['actual_pre_append_full_account'];post=proof['actual_post_append_full_account']
            require(event['actual_diagnostic_write_byte_account_before']==pre
                and pre['additional_record_bytes']==key[1] and post['additional_record_bytes']==0,
                'actual first account exact complete UTF8 admission and true second account increment0')
            accounting=event['actual_private_invalid_append_accounting']
            require(accounting['policy']=='ONE_CURRENT_FULL_PRE_APPEND_ACCOUNT_EXACT_UTF8_THEN_TRUE_FULL_POST_APPEND_ACCOUNT_V1'
                and accounting['actual_original_disk_account_calls_completed_before_append']==1
                and accounting['actual_pre_append_original_disk_account_increment']==0
                and accounting['actual_pre_append_full_account_started_monotonic']==times[0]
                and accounting['actual_pre_append_full_account_returned_monotonic']==times[1]
                and accounting['additional_record_bytes_is_derived_complete_UTF8_length']is True
                and accounting['exact_complete_UTF8_append_bytes_prechecked']is True
                and accounting['outer_or_prior_account_reused']is False
                and accounting['true_postappend_full_account_still_required']is True
                and accounting['postappend_completion_not_observed_at_prewrite']is True
                and accounting['original_record_and_disk_account_methods_unchanged']is True
                and accounting['same_fixed_total2s_window']is True and accounting['resource_PASS']is False
                and accounting['atomic_or_continuous_history_claimed']is False,
                'prewrite saved metadata is truthful about one actual call and future postaccount')
            for account,increment in((pre,key[1]),(post,0)):
                history=account['actual_original_history_check']
                require(all(type(v)is int and v>=0 for v in(account['actual_regular_joint_bytes'],
                    account['previous_complete_open_unlinked_bytes'],account['external_D_E_bytes'],
                    history['artifact_bytes'],history['disk_free_bytes'],increment))
                    and account['actual_regular_joint_bytes']+account['previous_complete_open_unlinked_bytes']+increment<CAPS['joint_archive_bytes']
                    and history['artifact_bytes']+account['external_D_E_bytes']+account['previous_complete_open_unlinked_bytes']+increment<=CAPS['history_bytes']
                    and history['disk_free_bytes']-increment>=CAPS['free_floor_bytes']
                    and account['current_open_unlinked_verified']is False
                    and account['failed_scan_never_replaced_by_this_account']is True
                    and account['clock']['whole_cap_satisfied']is True and account['clock']['stage_cap_satisfied']is True,
                    'each genuine account obeys original three disk caps and makes no unlinked/resource PASS substitution')
            actual_invalid_prepost_raw_couplings.append(dict(actual_journal_snapshot_pin=journal_pin,
                complete_appended_UTF8_sha256=key[0],exact_complete_appended_UTF8_bytes=key[1],
                fixed_window_started_monotonic=start,fixed_window_deadline_monotonic=end,
                actual_raw_event_sequence=event['sequence'],actual_raw_frame_ordinal=event['frame_ordinal']))
        if a.case in('transient','escaped'):
            relevant=matching if a.case=='transient'else[e for e in invalid if(e.get('complete_frame')or{}).get('actual_pre_post_scope_equal')is False]
            require(any(c['actual_raw_event_sequence']==e['sequence']
                and c['fixed_window_started_monotonic']==e['fixed_window_started_monotonic']
                for c in actual_invalid_prepost_raw_couplings for e in relevant),
                'positive recovery genuinely exercised new invalid pre/post path with fixture-specific raw SHA/len and same-window completed two calls')
        require(runtime.tree(source)==dfreeze and runtime.tree(receipts)==efreeze,'D/E remain fully frozen')
        try:monitor_summary=monitor.summary(include_unpersisted=True)
        except BaseException as error:
            # The deliberate real journal-directory negative must not be
            # hidden by repairing its target just to make fullpin() succeed.
            monitor_summary=dict(actual_original_summary_error=runtime.monitor_error(error),
                actual_journal_target=None if monitor.journal is None else str(monitor.journal),
                actual_journal_target_identity=None if monitor.journal is None else runtime.identity(monitor.journal.lstat()),
                actual_recording_errors=monitor.recording_errors,
                complete_unpersisted_events=monitor.unpersisted,
                journal_repaired_for_report=False,resource_PASS=False)
        facts=dict(schema='ACTUAL_FRESH_FRAME_GENUINE_CONTROL_CASE_FACTS_V1',group_id=GROUPS[a.case],case_id=a.case,
            new_Source_binding_pin=binding_pin,independent_Source_prelaunch_review_pin=review_pin,
            adapter_Source_pin=b['adapter_Source_pin'],control_entry_Source_pin=b['control_entry_Source_pin'],
            original_owner_helper_Source_pin=b['owner_helper_Source_pin'],original_helper_pin=hpin,original_resource_pin=rpin,
            actual_host_PID=os.getpid(),actual_business_command=command,actual_stage_records=runner.records,
            actual_expected_negative=expected_negative,actual_error=actual_error,actual_transitions=transitions,
            actual_invalid_prepost_append_proofs=completed_invalid_append_proofs,
            actual_invalid_prepost_raw_couplings=actual_invalid_prepost_raw_couplings,
            actual_invalid_append_journal_snapshots=actual_invalid_append_journal_snapshots,
            actual_after_execute_observed_monotonic=after_execute_observed_monotonic,
            actual_persistent_negative_deadline_basis=persistent_negative_deadline_basis,
            invalid_postproof_origin_is_completed_last_only_memory=True,
            prewrite_invalid_raw_not_rewritten_to_claim_future_postaccount=True,
            actual_owner_state=observer.summary(),actual_monitor_evidence=monitor_summary,
            actual_resources_before=before,actual_resources_after=after,last_complete_resource_frame=getattr(resources,'_fresh_frame_last_accepted',None),
            complete_D_freeze=dfreeze,complete_E_freeze=efreeze,original_caps=CAPS,whole_seconds=time.monotonic()-started,
            actual_expected_outcome_observed=True,OS_rows_or_tool_outcomes_mocked=False,
            original_classes_MRO_modified=False,old_controls_qualification_inherited=False,
            actual_Root_tool_terminal=None,actual_Root_current_group_closure=None,new_control_qualification=None,
            actual_native_build_or_AB_executed=False,scientific_qualification_created=False)
        path=host/'ACTUAL_FRESH_FRAME_CONTROL_FACTS.json';monitor.write_failure_result(path,facts)
        require(path.is_file(),'full actual facts persisted within original failure-only byte accounting')
        print(json.dumps(dict(status='ACTUAL_FRESH_FRAME_CONTROL_FACTS_ONLY_EXTERNAL_ROOT_CLOSURE_AND_REVIEW_REQUIRED',actual_facts_pin=pin(path),new_control_qualification=None,old_Q_inherited=False,native_or_scientific_qualification_created=False),allow_nan=False),flush=True)
    finally:
        try:
            if a.case=='persistent-topology':
                # Stop future forks first. An already-started generation may
                # publish after a glob snapshot, so rescan until the original
                # owned Popen actually closes or the bounded cleanup refuses.
                if not(out/'leader_release').exists():write_new(out/'leader_release',{})
                cleanup_deadline=min(deadline,time.monotonic()+2)
                while True:
                    for path in out.glob('descendant_ready_*.json'):
                        desc=read(path.read_bytes());release=out/('descendant_release_'+format(desc['generation'],'04d'))
                        if not release.exists():write_new(release,{})
                    business=[o for o in observer.owners.values()if o['role']=='business']
                    if not business or business[-1]['process'].poll()is not None:break
                    require(time.monotonic()<cleanup_deadline,'real bounded private churn closure remains unproven');time.sleep(.005)
            for name in('leader_release','descendant_release','escape_release'):
                if not(out/name).exists():write_new(out/name,{})
        finally:
            try:observer.restore_original_objects()
            finally:monitor.restore_bounded_objects()

if __name__=='__main__':
    if len(sys.argv)==6 and sys.argv[1]=='--private-child':
        private_child(sys.argv[2],sys.argv[3],float(sys.argv[4]),int(sys.argv[5]))
    else:main()

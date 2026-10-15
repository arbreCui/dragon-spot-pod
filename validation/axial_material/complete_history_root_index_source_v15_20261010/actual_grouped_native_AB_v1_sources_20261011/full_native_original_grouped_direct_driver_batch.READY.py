"""UNREADY fullNative library scheduling with original direct-driver OwnRSS.
No import-time work or child-controller CLI. The old compiler/controller batch
is NOT used: every original native argv is a direct genuine _process child.
Only a future Root-bound reviewed runtime may call compile_all_batch.
Consecutive identical-prefix Source groups1..16 are a new UNREADY schedule.
Every group uses the unchanged genuine direct-driver stage. Tiny controls must
call the same public production group helper; no new qualification is implied.
"""
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
            joint_archive_bytes=2*2**30,history_bytes=96*2**30,
            free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
COMPONENT_COUNTS = dict(Ganlib=78,Utilib=122,Trivac=220,Dragon=917)


def require(value,message):
    if type(value) is not bool or not value:
        raise ValueError(message)


class DirectDriverLibraryStage:
    """Library-level scheduling, not an alternative supervisor class.
    All driver processes run through the same original OwnRSS bound method.
    Same-process resource checks/journal writes have one synchronous owner.
    """
    def __init__(self,runtime,runner,resources,folder,component,started,deadline,budget):
        self.runtime,self.runner,self.resources = runtime,runner,resources
        self.folder,self.component = folder,component
        self.started,self.deadline,self.budget = started,deadline,budget
        self.monitor = getattr(resources,'_failure_only_monitor',None)
        self.owner = getattr(resources,'_exact_owner_observer',None)
        self.full = resources._genuine_full
        require(type(runner) is self.full.OwnRSSSerialExecutor and runner.resources is resources,
                'same genuine OwnRSS instance/resources')
        require(runner._process.__self__ is runner
                and runner._process.__func__ is self.full.OwnRSSSerialExecutor._process,
                'exact original directly bound _process')
        require(len(self.full.OwnRSSSerialExecutor.__bases__) == 1
                and self.full.OwnRSSSerialExecutor.__bases__[0].__name__ == 'SerialExecutor',
                'original class/MRO shape; canonical admission remains runtime responsibility')
        require(self.owner is not None and self.owner.runner is runner
                and self.owner.resources is resources
                and self.owner.original_process_code is runner._process.__func__.__code__,
                'same actual installed genuine start/wait owner observer')
        self.original_process = runner._process
        self.original_process_code = self.original_process.__func__.__code__
        self.original_execute = runner.execute
        require(self.original_execute.__self__ is runner,'same original inherited execute method')
        self.dump_records = self.original_execute.__func__.__globals__['dump_json']
        self.original_deadline = runner.deadline
        self.record = dict(label=str(folder.relative_to(runner.work)/('library_'+component)),
                           command=None,command_granularity='library_aggregate',
                           status='RUNNING',started_unix=time.time(),
                           wall_cap_seconds=600,all_actual_commands=[],
                           unit_SerialExecutor_execute_called=False,
                           unit_execute_extra_pre_post_resource_checks_inherited=False,
                           unit_execute_stages_json_writes_inherited=False,
                           original_OwnRSS_process_checks_preserved=True,
                           direct_native_driver_RSS_scope_preserved=True)
        self.journal = None
        self.previous_monitor_deadline = None

    def checkpoint(self):
        self.budget()
        require(self.runner.deadline == self.original_deadline,'original whole runner deadline unchanged')
        require(time.monotonic() < min(self.deadline,self.runner.deadline),
                'entire library600 and original whole1800 remaining')
        require(type(self.runner) is self.full.OwnRSSSerialExecutor
                and self.runner._process.__func__ is self.original_process.__func__
                and self.runner._process.__func__.__code__ is self.original_process_code,
                'original guard method/class still exact')
        self.owner.environment()

    def __enter__(self):
        if self.monitor is not None:
            self.previous_monitor_deadline = self.monitor.stage_deadline
            self.monitor.stage_deadline = self.deadline
        self.runner.records.append(self.record)
        try:
            self.checkpoint()
            self.record['resource_before'] = self.resources.check()
            self.checkpoint()
            self.dump_records(self.runner.stages_path,{'stages':self.runner.records})
            journal_path = self.folder/('library_'+self.component+'_DIRECT_DRIVER_EVENTS.jsonl')
            self.journal = journal_path.open('x',encoding='utf-8')
            self.record['actual_driver_event_journal_path'] = str(journal_path)
            return self
        except BaseException as error:
            self.record.update(status='FAILED',error=repr(error),elapsed_seconds=time.monotonic()-self.started)
            try:
                self.dump_records(self.runner.stages_path,{'stages':self.runner.records})
            finally:
                if self.monitor is not None:
                    self.monitor.stage_deadline = self.previous_monitor_deadline
            raise

    def event(self,value):
        self.journal.write(json.dumps(value,allow_nan=False)+'\n')
        self.journal.flush()
        os.fsync(self.journal.fileno())

    def execute_driver(self,folder,label,argv,deadline,budget):
        require(folder == self.folder and deadline == self.deadline and budget is self.budget,
                'same library caller/fixed deadline; no per-driver reset')
        self.checkpoint()
        log = folder/(label+'.log')
        watch_path = folder/(label+'.watchdog.json')
        require(not os.path.lexists(log) and not os.path.lexists(watch_path),
                'fresh driver log/watchdog, no failed-stage reuse or retry')
        remaining = min(600,self.deadline-time.monotonic(),self.runner.deadline-time.monotonic())
        require(remaining > 0,'true remaining library/whole time before native driver')
        self.event(dict(event='driver_enter',label=label,command=argv,
                        stage_deadline=self.deadline,actual_host_PID=os.getpid()))
        owners_before = set(self.owner.owners)
        try:
            # This is the original method, unmodified. It makes native compiler
            # a direct Popen child, samples its PID against512, installs original
            # watchdog/cleanup, checks resources first/5s/exit and uses its exact
            # instrumented original Popen wait. No controller process intervenes.
            with log.open('xb') as out:
                self.checkpoint()
                remaining = min(600,self.deadline-time.monotonic(),self.runner.deadline-time.monotonic())
                require(remaining > 0,'remaining after journal/log and before original Popen')
                self.original_process(argv,folder,subprocess.DEVNULL,out,remaining)
            self.checkpoint()
            watch = self.runtime.strict_json(watch_path.read_bytes())
            require(type(watch['pid']) is int and watch['pid'] > 0
                    and type(watch['returncode']) is int and watch['returncode'] == 0
                    and watch['command'] == argv and watch['limit_failure'] is None
                    and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True,
                    'actual original direct native-driver watchdog closed0')
            require(type(watch['sampled_peak_rss_mib']) in (int,float)
                    and not isinstance(watch['sampled_peak_rss_mib'],bool)
                    and math.isfinite(watch['sampled_peak_rss_mib'])
                    and 0 <= watch['sampled_peak_rss_mib'] < 512
                    and 0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= remaining <= 600
                    and watch['rss_cap_mib'] == 512,'original direct PID RSS/wall scope')
            driver = self.owner.owners[watch['pid']]
            proof = driver['closed_wait']
            require(driver['role'] == 'business' and driver['args'] == argv
                    and driver['process'].pid == watch['pid']
                    and proof is not None and proof['closed_proven'] is True
                    and type(proof['actual_exit_code']) is int and proof['actual_exit_code'] == 0
                    and proof['actual_waitpid_pid'] == watch['pid'],
                    'same-host exact compiler Popen actual original wait tuple')
            fresh_owners = [self.owner.owners[p] for p in set(self.owner.owners)-owners_before]
            watchdogs = [o for o in fresh_owners if o['role'] == 'watchdog']
            require(len(fresh_owners) == 2 and len(watchdogs) == 1,
                    'one original native driver and its original watchdog captured')
            watchdog = watchdogs[0]
            require(watchdog['closed_wait'] is not None
                    and watchdog['closed_wait']['closed_proven'] is True,
                    'original watchdog actual wait closure retained')
            value = dict(label=label,command=argv,
                         actual_watchdog_pin=self.runtime.fullpin(watch_path,budget),
                         actual_merged_stdout_stderr_pin=self.runtime.fullpin(log,budget),
                         actual_child_PID=watch['pid'],watchdog=watch,
                         actual_host_PID=os.getpid(),native_driver_is_original_OwnRSS_direct_child=True,
                         unit_SerialExecutor_execute_called=False,
                         actual_native_driver_closed_wait=dict(proof),
                         actual_original_watchdog_PID=watchdog['pid'],
                         actual_original_watchdog_closed_wait=dict(watchdog['closed_wait']),
                         watchdog_exit_zero_claimed=False,
                         actual_process_group_cleanup_proven_by_flag=False,
                         actual_stdlib_Source_pin=self.owner.stdlib_pin,
                         compiler_grandchildren_RSS_scope_not_certified=True)
            self.record['all_actual_commands'].append(value)
            self.event(dict(event='driver_return',status='PASS',**value))
            self.checkpoint()
            return value
        except BaseException as error:
            self.event(dict(event='driver_failed',label=label,command=argv,error=repr(error),
                            actual_watchdog_pin_if_saved=self.runtime.fullpin(watch_path)
                            if watch_path.is_file() else None,
                            actual_merged_stdout_stderr_pin_if_saved=self.runtime.fullpin(log)
                            if log.is_file() else None))
            raise

    def __exit__(self,error_type,error,traceback):
        try:
            if error is None:
                try:
                    self.checkpoint()
                    self.record['resource_after'] = self.resources.check()
                    self.checkpoint()
                    self.record['status'] = 'PASS'
                except BaseException as failure:
                    self.record.update(status='FAILED',error=repr(failure))
                    raise
            else:
                self.record.update(status='FAILED',error=repr(error))
        finally:
            try:
                if self.journal is not None:
                    self.journal.flush()
                    os.fsync(self.journal.fileno())
                    journal_path = Path(self.journal.name)
                    self.journal.close()
                    self.record['actual_driver_event_journal_pin'] = self.runtime.fullpin(journal_path)
                self.record['elapsed_seconds'] = time.monotonic()-self.started
                self.dump_records(self.runner.stages_path,{'stages':self.runner.records})
                if self.record['status'] == 'PASS':
                    try:
                        self.checkpoint()
                    except BaseException as failure:
                        self.record.update(status='FAILED',error=repr(failure),
                                           elapsed_seconds=time.monotonic()-self.started)
                        self.dump_records(self.runner.stages_path,{'stages':self.runner.records})
                        raise
            except BaseException as persistence_error:
                self.record.update(status='FAILED',persistence_or_final_checkpoint_error=repr(persistence_error))
                raise
            finally:
                if self.monitor is not None:
                    self.monitor.stage_deadline = self.previous_monitor_deadline
        return False



# The selected original first-eligible compile execution order is unchanged.
# A group is a consecutive segment of that order, never a new sorting pass.
MAX_COMPILE_GROUP_UNITS = 16
ORIGINAL_CPP_COUNTS = dict(Ganlib=4,Utilib=0,Trivac=0,Dragon=9)


def original_unit_dependencies(path,by_source,module_source):
    uses = [] if path not in by_source else by_source[path].uses
    return {module_source[m] for m in uses
            if m in module_source and module_source[m] != path}


def original_compile_unit_plan(folder,component,recipe,tools,path):
    """Pure argv/output plan. No import, filesystem read or native action."""
    folder,path = Path(folder),Path(path)
    require(type(component) is str and component in COMPONENT_COUNTS
            and folder.is_absolute() and path.parent == folder,
            'one original component src CWD for every group member')
    require(path.suffix in ('.c','.f90','.F90','.f','.F'),
            'only original five native Source suffixes')
    source = path.with_suffix('.pp.f90' if path.suffix == '.F90' else '.pp.f') \
             if path.suffix in ('.F','.F90') else path
    preprocess = None
    if source != path:
        require(recipe['PREPRO'] is not None,
                'original selected Makefile PREPRO undefined; never invent it')
        preprocess = [tools[recipe['PREPRO']]['path'],'-P','-W','-traditional',*recipe['FLAGS']]
        if path.suffix == '.F':preprocess += recipe['FMPI']
        preprocess += [str(path),str(source)]
    if path.suffix == '.c':
        require(recipe['C'] is not None,'original selected Makefile C undefined')
        prefix = [tools[recipe['C']]['path'],*recipe['CFLAGS'],*recipe['FLAGS'],
                  *recipe['opt'],*recipe['COMP'],'-c']
    else:
        flags = recipe['FFLAG77'] if path.suffix in ('.f','.F') else recipe['FFLAGS']
        prefix = [tools[recipe['F90']]['path'],*flags,*recipe['opt'],
                  *recipe['COMP'],*recipe['INCLUDE'],'-c']
    obj = path.with_suffix('.o')
    default = folder/(source.stem+'.o')
    return dict(component=component,cwd=str(folder),original_source=str(path),
                compiler_source=str(source),compiler_prefix=prefix,
                original_object=str(obj),compiler_default_object=str(default),
                original_preprocessor_argv=preprocess,
                original_single_unit_argv=[*prefix,str(source),'-o',str(obj)])


def select_original_compile_group(folder,component,recipe,tools,pending,completed,
                                  by_source,module_source):
    """At most16 consecutive original first-eligible units, same complete prefix.

    A dependent may follow its provider in argv order within one group. The
    compiler must really consume that order; only fresh real controls/build can
    establish that. Preprocessed units are singleton boundaries so all original
    cpp commands stay at their original position relative to compile units.
    """
    require(type(pending) is list and bool(pending)
            and len(set(pending)) == len(pending)
            and type(completed) is set and not (set(pending)&completed),
            'unique pending original units disjoint from actually completed')
    virtual_pending = list(pending);virtual_completed = set(completed);group = []
    while virtual_pending and len(group) < MAX_COMPILE_GROUP_UNITS:
        chosen = None
        for path in virtual_pending:
            if original_unit_dependencies(path,by_source,module_source) <= virtual_completed:
                chosen = path;break
        require(chosen is not None,
                'original native module dependencies must be acyclic and satisfied')
        plan = original_compile_unit_plan(folder,component,recipe,tools,chosen)
        if group:
            if plan['compiler_prefix'] != group[0]['compiler_prefix'] \
                    or plan['component'] != group[0]['component'] \
                    or plan['cwd'] != group[0]['cwd'] \
                    or plan['original_preprocessor_argv'] is not None \
                    or group[0]['original_preprocessor_argv'] is not None:
                break
        group.append(plan);virtual_pending.remove(chosen);virtual_completed.add(chosen)
        if plan['original_preprocessor_argv'] is not None:break
    require(1 <= len(group) <= MAX_COMPILE_GROUP_UNITS,'finite compiler group1..16')
    return group


def compile_group_preflight(runtime,folder,component,recipe,tools,group,completed,
                            by_source,module_source,all_original_objects,
                            expected_Source_pins,budget):
    """Production input/default-output admission, also called by actual controls.

    No process is started here. A changed Source or preexisting object fails
    before any group compiler; this is not a cached resource/account snapshot.
    """
    require(type(group) is list and 1 <= len(group) <= MAX_COMPILE_GROUP_UNITS,
            'bounded nonempty reviewed actual group')
    originals = list(map(Path,all_original_objects))
    require(len(set(originals)) == len(originals)
            and len({str(p).casefold() for p in originals}) == len(originals),
            'original output basename collision refused, including case aliases')
    require(all(p.parent == folder and p.suffix == '.o' for p in originals),
            'all original object names in same component CWD')
    defaults = [Path(p['compiler_default_object']) for p in group]
    targets = [Path(p['original_object']) for p in group]
    require(len(set(defaults)) == len(defaults) and len(set(targets)) == len(targets)
            and len({str(p).casefold() for p in defaults}) == len(defaults)
            and len({str(p).casefold() for p in targets}) == len(targets),
            'distinct actual compiler default and original object basenames')
    require(set(targets) <= set(originals),'every group target is original indexed output')
    for default,target in zip(defaults,targets):
        require(default == target or all(str(default).casefold() != str(p).casefold()
                for p in originals),'pp default basename cannot alias any original target')
    before_objects = {p for p in folder.glob('*.o')}
    require(before_objects == {p.with_suffix('.o') for p in completed},
            'only previous actually completed original objects present')
    records = [];virtual_completed = set(completed)
    for plan in group:
        path = Path(plan['original_source'])
        require(plan == original_compile_unit_plan(folder,component,recipe,tools,path),
                'full original recipe compiler/preprocessor argv/output plan exact')
        require(plan['compiler_prefix'] == group[0]['compiler_prefix']
                and plan['component'] == component and plan['cwd'] == str(folder),
                'one exact full compiler prefix/component/CWD; no mixed flags')
        dependencies = original_unit_dependencies(path,by_source,module_source)
        require(dependencies <= virtual_completed,
                'every same-component module provider is earlier, never guessed')
        require(not os.path.lexists(plan['original_object'])
                and not os.path.lexists(plan['compiler_default_object']),
                'fresh original/default objects, no reuse or overwrite')
        source = Path(plan['compiler_source'])
        if source != path:require(not os.path.lexists(source),'fresh original cpp output')
        pin = runtime.fullpin(path,budget)
        require(type(expected_Source_pins) is dict
                and expected_Source_pins.get(str(path)) == pin,
                'complete Source fullpin matches frozen expected input before native action')
        records.append(dict(plan=plan,original_source_pin=pin,
                            local_module_provider_sources=sorted(map(str,dependencies))))
        virtual_completed.add(path)
    require(len(group) == 1 or all(p['original_preprocessor_argv'] is None for p in group),
            'original cpp positions preserved by singleton boundaries')
    return records,before_objects


def compile_group_output_closure(runtime,native,folder,component,recipe,tools,
                                 group,records,before_objects,actual_compile,
                                 active_stage,budget,ordinal):
    """Same production post-driver closure, exposed for actual tiny refusals.

    Only a real completed original _process return recorded by the currently
    active genuine library stage can reach input/output mapping. No fake driver,
    borrowed argv, watchdog flag or synthetic wait tuple grants admission.
    """
    require(type(active_stage) is DirectDriverLibraryStage
            and active_stage.runtime is runtime and active_stage.folder == folder
            and active_stage.component == component and active_stage.budget is budget
            and recipe == runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]
            and active_stage.record['status'] == 'RUNNING'
            and active_stage.journal is not None and not active_stage.journal.closed,
            'same currently active genuine original recipe/stage for output closure')
    active_stage.checkpoint()
    require(type(group) is list and 1 <= len(group) <= MAX_COMPILE_GROUP_UNITS
            and type(records) is list and len(records) == len(group)
            and type(before_objects) is set and type(ordinal) is int and ordinal > 0
            and [r['plan'] for r in records] == group
            and all(p == original_compile_unit_plan(folder,component,recipe,tools,
                    Path(p['original_source'])) for p in group)
            and all(p['compiler_prefix'] == group[0]['compiler_prefix'] for p in group),
            'same complete original post-driver plans, inputs and bounded group')
    argv = [*group[0]['compiler_prefix'],*[p['compiler_source'] for p in group]]
    label = 'compile_group_'+format(ordinal,'04d')+'_'+Path(group[0]['original_source']).stem
    require(type(actual_compile) is dict
            and sum(value is actual_compile for value in active_stage.record['all_actual_commands']) == 1
            and actual_compile['command'] == argv and actual_compile['label'] == label
            and actual_compile['native_driver_is_original_OwnRSS_direct_child'] is True
            and actual_compile['actual_host_PID'] == os.getpid(),
            'actual unchanged execute_driver return identity and exact grouped argv')
    owner = active_stage.owner.owners[actual_compile['actual_child_PID']]
    proof = owner['closed_wait']
    require(owner['role'] == 'business' and owner['args'] == argv
            and owner['process'].pid == actual_compile['actual_child_PID']
            and proof is not None and proof == actual_compile['actual_native_driver_closed_wait']
            and proof['closed_proven'] is True and type(proof['actual_exit_code']) is int
            and proof['actual_exit_code'] == 0
            and proof['actual_waitpid_pid'] == owner['pid'],
            'same actual original compiler owner/wait tuple closed zero')
    watchdog = active_stage.owner.owners[actual_compile['actual_original_watchdog_PID']]
    require(watchdog['role'] == 'watchdog' and watchdog['closed_wait'] is not None
            and watchdog['closed_wait'] == actual_compile['actual_original_watchdog_closed_wait']
            and watchdog['closed_wait']['closed_proven'] is True,
            'same actual original watchdog owner wait closure')
    runtime.recheck(actual_compile['actual_watchdog_pin'],budget)
    runtime.recheck(actual_compile['actual_merged_stdout_stderr_pin'],budget)
    watch = runtime.strict_json(Path(actual_compile['actual_watchdog_pin']['path']).read_bytes())
    require(watch == actual_compile['watchdog'] and watch['command'] == argv
            and watch['pid'] == owner['pid'] and watch['returncode'] == 0
            and watch['limit_failure'] is None,
            'full actual saved watchdog agrees with same closed driver')
    stage = actual_compile
    defaults = {Path(p['compiler_default_object']) for p in group}
    require({p for p in folder.glob('*.o')} == before_objects|defaults,
            'one and only one fresh default object for every consumed group input')
    default_pins = [runtime.fullpin(p['compiler_default_object'],budget) for p in group]
    rows = []
    for position,(record,default_pin) in enumerate(zip(records,default_pins)):
        plan = record['plan'];source = Path(plan['compiler_source'])
        default,target = Path(plan['compiler_default_object']),Path(plan['original_object'])
        runtime.recheck(record['original_source_pin'],budget)
        runtime.recheck(record['actual_compiler_input_pin'],budget)
        runtime.recheck(default_pin,budget)
        action = 'fresh_default_basename_already_original'
        if default != target:
            require(not os.path.lexists(target),'fresh original pp object target before move')
            default.rename(target)
            require(not os.path.lexists(default),'default pp object moved; no retained duplicate')
            action = 'fresh_closed_driver_default_pp_object_renamed'
        op = runtime.fullpin(target,budget)
        require(op['sha256'] == default_pin['sha256']
                and op['size_bytes'] == default_pin['size_bytes'],
                'mapped original object is full exact actual compiler default bytes')
        retained_preprocessed = None
        if record['preprocessor_output_pin'] is not None:
            retained = native.parent/'retained_preprocessor_Source'/component/source.name
            retained.parent.mkdir(parents=True,exist_ok=True)
            require(not os.path.lexists(retained),'fresh complete retained cpp Source')
            shutil.copy2(source,retained);retained_preprocessed=runtime.fullpin(retained,budget)
            require(retained_preprocessed['sha256'] == record['preprocessor_output_pin']['sha256']
                    and retained_preprocessed['size_bytes'] == record['preprocessor_output_pin']['size_bytes'],
                    'lossless complete actual preprocessed input retained')
            runtime.recheck(record['actual_compiler_input_pin'],budget);source.unlink()
        row = dict(original_source_pin=record['original_source_pin'],
                   preprocessor_output_pin=record['preprocessor_output_pin'],
                   actual_compiler_input_pin=record['actual_compiler_input_pin'],
                   retained_complete_preprocessor_Source_pin=retained_preprocessed,
                   actual_compile=stage,new_object_pin=op,
                   actual_group_member_index=position,actual_group_member_count=len(group),
                   original_single_unit_argv_for_recipe_provenance_only=plan['original_single_unit_argv'],
                   old_single_unit_argv_executed=False,
                   actual_compiler_default_object_pin_before_mapping=default_pin,
                   actual_default_to_original_object_mapping=dict(default_path=str(default),
                        original_path=str(target),action=action,complete_bytes_preserved=True),
                   local_module_provider_sources=record['local_module_provider_sources'])
        rows.append(row)
    active_stage.checkpoint()
    return rows


def compile_original_source_group(runtime,native,folder,component,recipe,tools,
                                  pending,completed,by_source,module_source,
                                  all_original_objects,expected_Source_pins,
                                  active_stage,budget,ordinal):
    """Production path: select, admit, genuine native execute, map, fullpin.

    Public for fresh Root-bound tiny controls. It does not call compile_all_batch
    or alter its UNREADY gate. It accepts only the same genuine library stage.
    No business Python controller, new supervisor or resource strategy exists.
    """
    require(type(active_stage) is DirectDriverLibraryStage
            and active_stage.runtime is runtime and active_stage.folder == folder
            and active_stage.component == component and active_stage.budget is budget
            and recipe == runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component],
            'same original bound direct-driver stage and exact selected recipe')
    require(type(ordinal) is int and ordinal > 0,'fresh monotonically assigned group label')
    active_stage.checkpoint()
    group = select_original_compile_group(folder,component,recipe,tools,pending,completed,
                                         by_source,module_source)
    records,before_objects = compile_group_preflight(runtime,folder,component,recipe,tools,
        group,completed,by_source,module_source,all_original_objects,expected_Source_pins,budget)
    commands = []
    for record in records:
        plan = record['plan'];source = Path(plan['compiler_source'])
        preprocessed = None
        if plan['original_preprocessor_argv'] is not None:
            commands.append(active_stage.execute_driver(folder,
                'preprocess_'+Path(plan['original_source']).stem,
                plan['original_preprocessor_argv'],active_stage.deadline,budget))
            preprocessed = runtime.fullpin(source,budget)
        record['preprocessor_output_pin'] = preprocessed
        record['actual_compiler_input_pin'] = preprocessed or record['original_source_pin']
    # Recheck actual compiler inputs after any real cpp, before original Popen.
    for record in records:
        runtime.recheck(record['original_source_pin'],budget)
        runtime.recheck(record['actual_compiler_input_pin'],budget)
        require(not os.path.lexists(record['plan']['original_object'])
                and not os.path.lexists(record['plan']['compiler_default_object']),
                'both target names remain fresh immediately before compiler')
    argv = [*group[0]['compiler_prefix'],*[p['compiler_source'] for p in group]]
    require('-o' not in argv,'multi-source default objects; no invalid shared -o')
    label = 'compile_group_'+format(ordinal,'04d')+'_'+Path(group[0]['original_source']).stem
    stage = active_stage.execute_driver(folder,label,argv,active_stage.deadline,budget)
    commands.append(stage)
    rows = compile_group_output_closure(runtime,native,folder,component,recipe,tools,
        group,records,before_objects,stage,active_stage,budget,ordinal)
    active_stage.checkpoint()
    summary = dict(component=component,cwd=str(folder),compiler_group_ordinal=ordinal,
                   group_size=len(group),maximum_group_size=MAX_COMPILE_GROUP_UNITS,
                   exact_original_compiler_prefix=group[0]['compiler_prefix'],
                   actual_group_argv=argv,actual_group_compile=stage,
                   original_selected_Source_order=[p['original_source'] for p in group],
                   original_cpp_singleton_positions_preserved=True,
                   compiler_input_pins=[r['actual_compiler_input_pin'] for r in rows],
                   original_Source_pins=[r['original_source_pin'] for r in rows],
                   new_object_pins=[r['new_object_pin'] for r in rows],
                   actual_default_to_original_object_mappings=[r['actual_default_to_original_object_mapping'] for r in rows],
                   original_single_unit_argv_byte_equality_claimed=False,
                   default_object_or_debug_bytes_equality_to_old_build_claimed=False)
    return group,rows,commands,summary


def compile_all_batch(runtime,native,index,observation_source,tools,runner,support,resources,budget,batch_Source_pin):
    require(SOURCE_STATUS == 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','UNREADY direct-driver batch refuses any native action')
    require(runtime.CAPS == CAPS,'exact original9caps')
    runtime.recheck(batch_Source_pin,budget)
    require(batch_Source_pin['path'] == str(Path(__file__).absolute()),'exact added frozen Source')
    fullpin,recheck,frozen_sources = runtime.fullpin,runtime.recheck,runtime.frozen_sources
    ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES = runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES
    FUTURE = runtime.FUTURE
    active_stage = None
    def guarded(runner_arg,support_arg,resources_arg,folder,label,argv,deadline,budget_arg):
        require(runner_arg is runner and support_arg is support and resources_arg is resources,'same genuine factory/runner/resource ownership')
        if active_stage is None:
            return runtime.guarded(runner,support,resources,folder,label,argv,deadline,budget_arg)
        return active_stage.execute_driver(folder,label,argv,deadline,budget_arg)
    require(platform.system()=='Darwin'and platform.machine()=='arm64','exact original selected Makefile platform, no inferred compiler flags')
    original=frozen_sources(native,index,observation_source);generator,generator_pin=support.load(native/'script/make_depend.py',next(r['input_pin']['sha256']for r in original if r['relative_path']=='script/make_depend.py'),'axmat_observation_original_native_make_depend')
    sources={r['relative_path']:r['input_pin']for r in original};stages=[];archives={};all_objects=[]
    require(list(ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES)==['Ganlib','Utilib','Trivac','Dragon'],'all original component-specific recipe variables')
    for component in ('Ganlib','Utilib','Trivac','Dragon'):
        started=time.monotonic();deadline=started+600;folder=native/component/'src';recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]
        with DirectDriverLibraryStage(runtime,runner,resources,folder,component,started,deadline,budget) as active_stage:
            library_dir=native/component/'lib/Darwin_arm64';library_dir.mkdir(parents=True)
            if recipe['lib_module']is not None:(native/recipe['lib_module']).mkdir(parents=True)
            require(not any(p.suffix in('.o','.a','.mod')for p in folder.iterdir()),'all native objects/archives/modules fresh; no old build reuse')
            c=sorted(folder.glob('*.c'));f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))];f77_lower=sorted(folder.glob('*.f'));f77_upper=sorted(folder.glob('*.F'));f77=[*f77_lower,*f77_upper]
            # The original default generator excludes module-contained include files.
            ordered90=[Path(v)for v in generator.build_dependency_order([str(p)for p in f90])]
            objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]
            require(len(set(objects_order))==len(objects_order),'original object basename uniqueness');require(len(objects_order)==COMPONENT_COUNTS[component],'all original1336 plus observer1')
            units=generator.build_units([str(p)for p in [*f90,*f77]]);module_source={u.module:Path(u.name)for u in units if u.module};by_source={Path(u.name):u for u in units};pending=[*c,*ordered90,*f77];commands=[];objects=[];completed=set()
            groups=[];group_ordinal=0
            expected_Source_pins={r['input_pin']['path']:r['input_pin']for r in original}
            while pending:
                group_ordinal+=1
                group,rows,group_commands,group_evidence=compile_original_source_group(
                    runtime,native,folder,component,recipe,tools,pending,completed,
                    by_source,module_source,objects_order,expected_Source_pins,
                    active_stage,budget,group_ordinal)
                # Commit completion only after genuine closure, all input/output
                # fullpins and mapping/retention succeeded. Failures never resume.
                for plan in group:
                    path=Path(plan['original_source']);pending.remove(path);completed.add(path)
                objects.extend(rows);all_objects.extend(rows);commands.extend(group_commands);groups.append(group_evidence)
            require(len(objects)==COMPONENT_COUNTS[component]
                    and sum(len(g['original_selected_Source_order'])for g in groups)==len(objects),
                    'complete original component input coverage once, group1..16')
            require(sum(r['preprocessor_output_pin']is not None for r in objects)==ORIGINAL_CPP_COUNTS[component],
                    'all and only original13 cpp; original argv and singleton positions')
            require({x['new_object_pin']['path']for x in objects}==set(map(str,objects_order)),'all original library objects compiled exactly once')
            archive=folder/('lib'+component+'.a');argv=[tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)];archive_stage=guarded(runner,support,resources,folder,'archive_'+component,argv,deadline,budget);ap=fullpin(archive,budget)
            for row in objects:recheck(row['new_object_pin'],budget)
            # Original ar emits src/lib*.a, then original cp places the same fresh
            # archive into each component's own lib directory used by final link.
            library_copy=library_dir/archive.name;require(not os.path.lexists(library_copy),'fresh original recipe library copy')
            shutil.copy2(archive,library_copy);library_copy_pin=fullpin(library_copy,budget)
            require(library_copy_pin['sha256']==ap['sha256']and library_copy_pin['size_bytes']==ap['size_bytes'],'original library copy full bytes equal actual fresh ar output')
            module_copy_pins=[]
            if recipe['module_copy']:
                modules=native/recipe['lib_module'];generated_modules=list(folder.glob('*.mod'))
                require(component!='Utilib'or bool(generated_modules),'original Utilib unguarded cp *.mod requires actual modules')
                for p in generated_modules:
                    target=modules/p.name;require(not os.path.lexists(target),'original per-library module namespace fresh')
                    shutil.copy2(p,target);module_copy_pins.append(dict(original_generated_module_pin=fullpin(p,budget),original_recipe_module_copy_pin=fullpin(target,budget)))
            # Trivac's original library recipe never copies module files.
            require(time.monotonic()-started<600,'entire library compile/archive group600 cap')
            archives[component]=library_copy_pin;stages.append(dict(component=component,exact_original_selected_recipe=recipe,original_recipe_library_copy_pin=library_copy_pin,original_recipe_module_copy_pins=module_copy_pins,archive_object_source_suffix_group_order=['.c','original_dependency_order(.f90_then_.F90)','.f','.F'],execution_record_granularity='library',actual_consecutive_compile_groups=groups,maximum_compile_group_units=MAX_COMPILE_GROUP_UNITS,unit_SerialExecutor_execute_called=False,direct_driver_OwnRSS_scope_preserved=True,stage_wall_cap_seconds=600,elapsed_seconds=time.monotonic()-started,all_object_inputs_in_original_archive_order=[r for p in objects_order for r in objects if r['new_object_pin']['path']==str(p)],all_commands=commands,actual_archive_command=archive_stage,new_archive_pin=ap))
            require(frozen_sources(native,index,observation_source)==original,'complete native Source freeze after whole group')
        stages[-1]['elapsed_seconds'] = active_stage.record['elapsed_seconds']
        stages[-1]['actual_library_execution_record'] = active_stage.record
        stages[-1]['actual_driver_event_journal_pin'] = active_stage.record['actual_driver_event_journal_pin']
        active_stage = None
    link_started=time.monotonic();link_deadline=link_started+600;exe=native/'Dragon/src/Dragon';dragon_o=native/'Dragon/src/DRAGON.o';require(not os.path.lexists(exe),'new final executable required')
    link_inputs=[fullpin(dragon_o,budget),*[archives[k]for k in('Dragon','Trivac','Utilib','Ganlib')]]
    link_recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Dragon'];argv=[tools[link_recipe['F90']]['path'],*link_recipe['opt'],*link_recipe['COMP'],*[p['path']for p in link_inputs],*link_recipe['LFLAGS'],'-o',str(exe)];link=guarded(runner,support,resources,native/'Dragon/src','Dragon_link',argv,link_started+600,budget)
    ep=fullpin(exe,budget)
    for p in link_inputs:recheck(p,budget)
    for r in all_objects:recheck(r['new_object_pin'],budget)
    require(frozen_sources(native,index,observation_source)==original,'whole native Source-to-new-object/archive/link final freeze')
    evidence=dict(schema='ACTUAL_FROZEN_COMPLETE_NATIVE_GROUPED_DIRECT_DRIVER_LIBRARY_BATCH_EVIDENCE_V1',source_only=False,frozen_all_compiled_and_include_Source=original,original_Source_index_pin=fullpin(index['_path'],budget),original_dependency_generator_pin=dict(generator_pin,size_bytes=generator_pin['identity'][4]),original_platform=dict(OS='Darwin',ARCH='arm64',openmp=0,mpi=0,hdf5=0,opt=['-O','-g']),stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],all_four_complete_library_build_stages=stages,actual_final_link_command=link,all_actual_link_input_pins=link_inputs,new_actual_executable_pin=ep,all_sources_objects_archives_checked_after_actual_link=True,no_old_binary_object_archive_used=True,compiler_descendant_RSS_scope_not_certified=True,original_compiler_driver_RSS_scope_preserved=True,execution_record_granularity='library',unit_SerialExecutor_execute_called=False,unit_execute_extra_pre_post_checks_inherited=False,original_own_child_guard_scope_preserved=True,whole5stage_executed=True,maximum_compile_group_units=MAX_COMPILE_GROUP_UNITS,all1337_units_compiled_once=True,original13_cpp_commands_preserved=True,original_single_unit_argv_byte_equality_claimed=False,debug_or_binary_byte_equality_to_old_build_claimed=False,**FUTURE)
    runtime.recheck(batch_Source_pin,budget)
    budget();require(time.monotonic()<min(link_deadline,runner.deadline),'whole fifth stage link+full EOF+Source closeout within original600/whole1800')
    return ep,evidence

if __name__ == '__main__':
    raise RuntimeError('UNREADY Source helper has no standalone compiler/controller CLI')

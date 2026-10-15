"""UNREADY fullNative library scheduling with original direct-driver OwnRSS.
No import-time work or child-controller CLI. The old compiler/controller batch
is NOT used: every original native argv is a direct genuine _process child.
Only a future Root-bound reviewed runtime may call compile_all_batch.
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

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
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
            while pending:
                chosen=None
                for p in pending:
                    uses=[]if p not in by_source else by_source[p].uses
                    dependencies={module_source[m]for m in uses if m in module_source and module_source[m]!=p}
                    if dependencies<=completed:chosen=p;break
                require(chosen is not None,'original native module dependencies must be acyclic; never guess ordering');pending.remove(chosen);p=chosen;budget();sp=fullpin(p,budget);obj=p.with_suffix('.o');require(not os.path.lexists(obj),'new object required')
                src=p
                if p.suffix in('.F','.F90'):
                    src=p.with_suffix('.pp.f90'if p.suffix=='.F90'else'.pp.f');require(not os.path.lexists(src),'fresh actual preprocessor output')
                    require(recipe['PREPRO']is not None,'original selected Makefile PREPRO undefined for this suffix; no invented tool')
                    argv=[tools[recipe['PREPRO']]['path'],'-P','-W','-traditional',*recipe['FLAGS']]
                    if p.suffix=='.F':argv+=recipe['FMPI']
                    argv+=[str(p),str(src)]
                    commands.append(guarded(runner,support,resources,folder,'preprocess_'+p.stem,argv,deadline,budget));preprocessed=fullpin(src,budget)
                else:preprocessed=None
                if p.suffix=='.c':
                    require(recipe['C']is not None,'original selected Makefile C undefined, no invented compiler')
                    argv=[tools[recipe['C']]['path'],*recipe['CFLAGS'],*recipe['FLAGS'],*recipe['opt'],*recipe['COMP'],'-c',str(src),'-o',str(obj)]
                else:
                    flags=recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']
                    argv=[tools[recipe['F90']]['path'],*flags,*recipe['opt'],*recipe['COMP'],*recipe['INCLUDE'],'-c',str(src),'-o',str(obj)]
                stage=guarded(runner,support,resources,folder,'compile_'+p.stem,argv,deadline,budget);op=fullpin(obj,budget);require(fullpin(p,budget)==sp,'compiler Source unchanged')
                retained_preprocessed=None
                if preprocessed is not None:
                    retained=native.parent/'retained_preprocessor_Source'/component/src.name;retained.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,retained);retained_preprocessed=fullpin(retained,budget);require(retained_preprocessed['sha256']==preprocessed['sha256']and retained_preprocessed['size_bytes']==preprocessed['size_bytes'],'lossless exact actual preprocessed compiler input kept');src.unlink()
                row=dict(original_source_pin=sp,preprocessor_output_pin=preprocessed,retained_complete_preprocessor_Source_pin=retained_preprocessed,actual_compile=stage,new_object_pin=op);objects.append(row);all_objects.append(row);commands.append(stage);completed.add(p)
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
            archives[component]=library_copy_pin;stages.append(dict(component=component,exact_original_selected_recipe=recipe,original_recipe_library_copy_pin=library_copy_pin,original_recipe_module_copy_pins=module_copy_pins,archive_object_source_suffix_group_order=['.c','original_dependency_order(.f90_then_.F90)','.f','.F'],execution_record_granularity='library',unit_SerialExecutor_execute_called=False,direct_driver_OwnRSS_scope_preserved=True,stage_wall_cap_seconds=600,elapsed_seconds=time.monotonic()-started,all_object_inputs_in_original_archive_order=[r for p in objects_order for r in objects if r['new_object_pin']['path']==str(p)],all_commands=commands,actual_archive_command=archive_stage,new_archive_pin=ap))
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
    evidence=dict(schema='ACTUAL_FROZEN_COMPLETE_NATIVE_DIRECT_DRIVER_LIBRARY_BATCH_EVIDENCE_V1',source_only=False,frozen_all_compiled_and_include_Source=original,original_Source_index_pin=fullpin(index['_path'],budget),original_dependency_generator_pin=dict(generator_pin,size_bytes=generator_pin['identity'][4]),original_platform=dict(OS='Darwin',ARCH='arm64',openmp=0,mpi=0,hdf5=0,opt=['-O','-g']),stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],all_four_complete_library_build_stages=stages,actual_final_link_command=link,all_actual_link_input_pins=link_inputs,new_actual_executable_pin=ep,all_sources_objects_archives_checked_after_actual_link=True,no_old_binary_object_archive_used=True,compiler_descendant_RSS_scope_not_certified=True,original_compiler_driver_RSS_scope_preserved=True,execution_record_granularity='library',unit_SerialExecutor_execute_called=False,unit_execute_extra_pre_post_checks_inherited=False,original_own_child_guard_scope_preserved=True,whole5stage_executed=True,**FUTURE)
    runtime.recheck(batch_Source_pin,budget)
    budget();require(time.monotonic()<min(link_deadline,runner.deadline),'whole fifth stage link+full EOF+Source closeout within original600/whole1800')
    return ep,evidence

if __name__ == '__main__':
    raise RuntimeError('UNREADY Source helper has no standalone compiler/controller CLI')

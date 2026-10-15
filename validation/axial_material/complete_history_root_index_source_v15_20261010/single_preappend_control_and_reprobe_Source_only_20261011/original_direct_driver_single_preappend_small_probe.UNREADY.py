"""Source-only, Root-bound four-driver cost probe; no complete Native build.

The existing host calls the unchanged genuine OwnRSS _process through the
unchanged DirectDriverLibraryStage. No child Python controller is introduced.
The four tiny inputs are private controls, not any of the original 1337 units.
There is no import-time work. Root supplies an actual Source binding/review.

The new private normal single-preappend adapter is fixed by ADAPTER_SHA.
Future ten-control RESULT/review pins are fixed in the actual Root binding and
matched by the independent prelaunch Source review, never guessed in Source.
The old ten-control qualification is not inherited. All four tiny drivers and
the original guards, argv, timing buckets and failure behavior are unchanged.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import sys
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
SCOPE = 'ROOT_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_ONLY'
PROBE = 'CANONICAL_CPP_GCC_GFORTRAN_AR_SMALL_DIRECT_V1'
POLICY = 'FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
            joint_archive_bytes=2*2**30,history_bytes=96*2**30,
            free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
SUPPORT = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
ADAPTER_SHA = 'd18ce676d776b674429d0c3e976466f5ab417ef4439f16f47aadef6a7ce9f50d'
BATCH_SHA = '5bafb5b5ca5a779ab949ee6ef2de5a0f10e6ba818ace783c2b0c499df436b709'
CONTROL_ORDER = ('closed-before-first','exit7','transient','unlinked-duplicates',
                 'escaped','echild','unobserved-cache','deadline',
                 'persistent-topology','journal-failure')
SMALL_INPUTS = {
    'probe.F90': b'#define AXMAT_PROBE_VALUE 7\nsubroutine axmat_direct_probe_fortran(value)\n  integer, intent(out) :: value\n  value = AXMAT_PROBE_VALUE\nend subroutine axmat_direct_probe_fortran\n',
    'probe.c': b'int axmat_direct_probe_c(void) { return 11; }\n',
}
NOT_QUALIFIED = dict(full_Native_build_qualified=False,
    actual_AB_material_context_qualified=False,complete_context_aggregation_qualified=False,
    actual_native_transport_executed=False,full_reference_qualified=False,
    scientific_qualification_created=False,physical_neutron_balance_qualified=False,
    AAA_accuracy_qualified=False,ABA_started=False,native_RSS_qualified=False,
    small_driver_composition_self_qualified=False,historical_cleanup_proven=False)


def require(value,message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path,positive_links=False):
    path = Path(path)
    before = identity(path.lstat())
    require(path.is_absolute() and '..' not in path.parts
            and all(not p.is_symlink() for p in (path,*path.parents))
            and stat.S_ISREG(before[2])
            and (before[3] >= 1 if positive_links else before[3] == 1),
            'full nonalias ordinary input; positive links only explicit original stdlib role')
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == before,'opened full input identity')
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
        require(identity(os.fstat(stream.fileno())) == before,'full EOF input identity')
    require(identity(path.lstat()) == before,'full input path identity unchanged')
    return dict(path=str(path),sha256=digest,size_bytes=before[4],identity=before)


def read(raw):
    def pairs(items):
        result = {}
        for key,value in items:
            require(key not in result,'no duplicate Source/META key')
            result[key] = value
        return result
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))


def pin_shape(expected):
    require(type(expected) is dict
            and set(expected) == {'path','sha256','size_bytes','identity'}
            and type(expected['path']) is str and Path(expected['path']).is_absolute()
            and type(expected['sha256']) is str and len(expected['sha256']) == 64
            and all(c in '0123456789abcdef' for c in expected['sha256'])
            and type(expected['size_bytes']) is int and expected['size_bytes'] >= 0
            and type(expected['identity']) is list and len(expected['identity']) == 7
            and all(type(value) is int and value >= 0 for value in expected['identity'])
            and expected['size_bytes'] == expected['identity'][4],
            'exact full SHA/size and seven real integer identity fields; bools refused')


def metadata(expected):
    pin_shape(expected)
    require(pin(expected['path']) == expected,'full ordinary Source/META pin')
    return read(Path(expected['path']).read_bytes())


def load_source(expected,name):
    require(pin(expected['path']) == expected,'exact Source before import')
    spec = importlib.util.spec_from_file_location(name,expected['path'])
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    require(Path(module.__file__).resolve() == Path(expected['path'])
            and pin(expected['path']) == expected,'exact Source after import')
    return module


def small_input_contract():
    return {name:dict(size_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
            for name,raw in SMALL_INPUTS.items()}


def fixed_driver_commands(folder,tools,recipe):
    pp = folder/'probe.pp.f90';cobj = folder/'probe_c.o'
    fobj = folder/'probe_fortran.o';archive = folder/'libSmallDriverProbe.a'
    return [
        ('cpp',[tools['cpp']['path'],'-P','-W','-traditional',
            *recipe['FLAGS'],str(folder/'probe.F90'),str(pp)],pp),
        ('c',[tools['c']['path'],*recipe['CFLAGS'],*recipe['FLAGS'],
            *recipe['opt'],*recipe['COMP'],'-c',str(folder/'probe.c'),'-o',str(cobj)],cobj),
        ('fortran',[tools['fortran']['path'],*recipe['FFLAGS'],
            *recipe['opt'],*recipe['COMP'],*recipe['INCLUDE'],'-c',str(pp),'-o',str(fobj)],fobj),
        ('ar',[tools['ar']['path'],'rcs',str(archive),str(cobj),str(fobj)],archive),
    ]


def accepted_window_timing(joint,phase):
    return dict(phase=phase,window_started_monotonic=joint['fixed_window_started_monotonic'],
        window_deadline_monotonic=joint['fixed_window_deadline_monotonic'],
        fresh_frame_ordinal=joint['fresh_frame_ordinal'],
        accepted_fresh_window_seconds=joint['fresh_window_elapsed_seconds'],
        invalid_frames_preserved=joint['invalid_frames_preserved'],
        actual_candidate_journal_append=joint['actual_candidate_journal_append'],
        observed_PIDs=joint['live_own_processes_observed'],
        actual_joint_bytes=joint['complete_joint_HOCDE_bytes'],
        actual_history_bytes=joint['artifact_bytes'],actual_free_bytes=joint['disk_free_bytes'])


def add_saved_timing_buckets(windows,journal,runtime,budget):
    """Derive only time boundaries actually present in the complete raw.

    Individual lsof duration and individual history walks are not recorded by
    the unchanged adapter. No manufactured fine-grained measurements are used.
    """
    events = [read(line) for line in journal.read_bytes().splitlines()]
    candidates = {}
    for event in events:
        budget()
        if event.get('event') == 'fresh_frame_complete_candidate':
            key = (event['fixed_window_started_monotonic'],event['frame_ordinal'])
            require(key not in candidates,'unique complete candidate journal key')
            candidates[key] = event
    for window in windows:
        budget()
        key = (window['window_started_monotonic'],window['fresh_frame_ordinal'])
        event = candidates[key]
        require(event['resource_PASS'] is False and event['failed_frame_accepted'] is False,
                'candidate journal remains evidence, not a self-published resource PASS')
        frame = event['complete_frame']
        pre = frame['pre_PS']['started_monotonic']
        post = frame['post_PS']['started_monotonic']
        end = window['window_started_monotonic'] + window['accepted_fresh_window_seconds']
        require(window['window_started_monotonic'] <= pre <= post <= end
                and end < window['window_deadline_monotonic'],'actual ordered accepted timing boundaries')
        window['observed_time_buckets'] = dict(
            before_accepted_pre_PS_including_prior_invalid_frames_seconds=pre-window['window_started_monotonic'],
            pre_PS_owner_lsof_and_pre_post_gap_seconds=post-pre,
            post_PS_parse_journal_history_free_freeze_and_publication_seconds=end-post,
            fine_grained_lsof_history_or_syscall_times_measured=False)
    return dict(complete_journal_pin=runtime.fullpin(journal,budget),
        candidate_count=len(candidates),invalid_count=sum(
            e.get('event') == 'fresh_frame_invalid_not_resource_PASS' for e in events),
        fatal_count=sum(e.get('event') == 'fresh_frame_window_fatal_no_resource_PASS' for e in events),
        accepted_window_count=len(windows),complete_raw_events_retained=True)


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--binding',required=True)
    cli.add_argument('--binding-sha256',required=True)
    cli.add_argument('--independent-prelaunch-review',required=True)
    args = cli.parse_args()
    started = time.monotonic()
    probe_deadline = None
    def budget():
        now = time.monotonic()
        require(now-started < 1800,'original whole1800 includes bootstrap and final report')
        require(probe_deadline is None or now < probe_deadline,
                'fixed small-probe600 includes inputs, all4 drivers and final report')
    binding_pin = pin(args.binding)
    require(binding_pin['sha256'] == args.binding_sha256,'Root-bound exact new binding SHA')
    b = metadata(binding_pin)
    require(b['schema'] == 'ROOT_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_SOURCE_BINDING_V1'
            and b['source_only'] is True and b['Root_only_actual_execution'] is True
            and b['execution_scope'] == SCOPE and b['probe_id'] == PROBE
            and b['policy'] == POLICY and b['original_caps'] == CAPS
            and all(type(value) is int for value in b['original_caps'].values())
            and b['actual_execution'] is None and b['old_controls_qualification_inherited'] is False
            and b['driver_execution_order'] == ['cpp','c','fortran','ar']
            and b['small_input_contract'] == small_input_contract(),
            'Source-bound fixed four-driver control only, unchanged typed nine caps')
    require(pin(Path(__file__).resolve()) == b['probe_entry_Source_pin'],
            'this exact Source-only entry; no unreviewed replacement')
    fresh = metadata(b['fresh_controls_Source_binding_pin'])
    require(fresh['schema'] == 'ROOT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_BINDING_V1'
            and fresh['policy'] == POLICY and fresh['source_only'] is True
            and fresh['original_caps'] == CAPS and fresh['old_controls_qualification_inherited'] is False,
            'same qualified fresh policy Source, no old Q inheritance')
    require(b['adapter_Source_pin'] == fresh['adapter_Source_pin']
            and b['adapter_Source_pin']['sha256'] == ADAPTER_SHA
            and b['original_N9_controls_Source_binding_pin'] == fresh['original_N9_controls_Source_binding_pin']
            and b['owner_helper_Source_pin'] == fresh['owner_helper_Source_pin']
            and b['actual_stdlib_subprocess_Source_pin'] == fresh['actual_stdlib_subprocess_Source_pin']
            and b['tool_pins'] == fresh['tool_pins'],'unchanged adapter, original binding/helper/stdlib/six tools')
    original = metadata(b['original_N9_controls_Source_binding_pin'])
    author = original['actual_author_Source_contract']
    require(original['schema'] == 'ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1'
            and original['source_only'] is True and original['original_caps'] == CAPS
            and type(author) is dict and len(author) == 21
            and b['original21_author_Source_contract'] == author
            and b['owner_helper_Source_pin'] == author['owner_scope_helper'],
            'all original21 complete author roles retained, old binding is Source provenance only')
    protected = [binding_pin,b['probe_entry_Source_pin'],b['direct_driver_batch_Source_pin'],
        b['adapter_Source_pin'],b['fresh_controls_Source_binding_pin'],
        b['original_N9_controls_Source_binding_pin'],b['fresh_controls_saved_RESULT_pin'],
        b['fresh_controls_independent_saved_review_pin'],b['support_Source_pin'],
        *author.values(),*[original[key] for key in (
            'actual_independent_Source_review_pin','actual_Source_admission_pin',
            'actual_Root_Source_admission_tool_terminal_pin','actual_canonical_tools_META_pin',
            'actual_stdlib_Source_witness_pin')],*b['genuine_guard_Source_pins'].values()]
    for expected in protected:
        pin_shape(expected)
        budget();require(pin(expected['path']) == expected,'all full external Source and saved input pins held')
    require(b['support_Source_pin']['path'] == str(SUPPORT)
            and b['support_Source_pin']['sha256'] == SUPPORT_SHA
            and b['direct_driver_batch_Source_pin']['sha256'] == BATCH_SHA,
            'original genuine support and exact FINAL direct-driver Source')
    saved = metadata(b['fresh_controls_saved_RESULT_pin'])
    require(saved['schema'] == 'ROOT_ACTUAL_TEN_FRESH_FRAME_CONTROLS_SAVED_EVIDENCE_V1'
            and saved['status'] == 'TEN_EXPECTED_CONTROL_OUTCOMES_AND_CURRENT_CLOSEOUT_PASS_ONLY'
            and saved['actual_source_binding_pin'] == b['fresh_controls_Source_binding_pin']
            and saved['original_caps'] == CAPS and saved['actual_control_count'] == 10
            and saved['all_tool_terminals_closed_zero'] is True
            and saved['all_captured_group_checks_passed'] is True
            and saved['all_negative_business_stages_remain_failed'] is True,
            'fixed actual ten controls plus actual distinct-author saved review; driver composition still unqualified')
    cases = saved['all_ten_actual_controls']
    require([case['case_id'] for case in cases] == list(CONTROL_ORDER)
            and all(case['actual_control_expected_outcome_observed'] is True
                    and case['all_observed_groups_currently_absent'] is True for case in cases),
            'complete saved original ten outcomes and current closeout, no filtered control subset')
    for case in cases:
        for key in ('actual_facts_pin','actual_tool_terminal_pin',
                    'actual_postclose_pin','actual_postclose_tool_terminal_pin'):
            expected = case[key];pin_shape(expected);budget()
            require(pin(expected['path']) == expected,'all ten actual saved facts/closed terminal/closure fullpins still exact')
            protected.append(expected)
    review_pin = pin(args.independent_prelaunch_review)
    review = metadata(review_pin)
    require(review['schema'] == 'INDEPENDENT_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_SOURCE_REVIEW_V1'
            and review['source_only'] is True and review['all_checks_passed'] is True
            and review['blockers'] == [] and review['new_Source_binding_pin'] == binding_pin
            and review['probe_entry_Source_pin'] == b['probe_entry_Source_pin']
            and review['adapter_Source_pin'] == b['adapter_Source_pin']
            and review['direct_driver_batch_Source_pin'] == b['direct_driver_batch_Source_pin']
            and review['fresh_controls_saved_RESULT_pin'] == b['fresh_controls_saved_RESULT_pin']
            and review['fresh_controls_independent_saved_review_pin'] == b['fresh_controls_independent_saved_review_pin'],
            'different-author review of this exact new combination, only Source permission')
    protected.append(review_pin)
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
            and sys.gettrace() is None and sys.getprofile() is None
            and all(os.environ.get(key) == '1' for key in THREAD_KEYS),
            'original nonoptimized unprofiled one-thread environment')
    sys.dont_write_bytecode = True
    support = load_source(b['support_Source_pin'],'small_direct_original_support')
    require(Path(sys.executable).resolve() == support.PYTHON
            and platform.system() == 'Darwin' and platform.machine() == 'arm64',
            'actual original canonical Python/Darwin arm64')
    expected_guards = dict(original_helper=(support.OLD_HELPER,support.OLD_HELPER_SHA),
        resource_factory=(support.RESOURCE_FACTORY,support.RESOURCE_SHA),
        full=(support.FULL,support.FULL_SHA),production=(support.PARENT,support.PARENT_SHA),
        bounded=(support.BOUNDED,support.BOUNDED_SHA))
    require(set(b['genuine_guard_Source_pins']) == set(expected_guards)
            and all(b['genuine_guard_Source_pins'][role]['path'] == str(path)
                    and b['genuine_guard_Source_pins'][role]['sha256'] == digest
                    for role,(path,digest) in expected_guards.items()),'all five exact original guard/helper/resource Source roles')
    helper,hpin = support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'small_direct_original_helper')
    resource,rpin = support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'small_direct_original_resources')
    full,production = helper.modules();helper.guard_admission(full)
    runtime = load_source(b['adapter_Source_pin'],'small_direct_qualified_fresh_adapter')
    batch = load_source(b['direct_driver_batch_Source_pin'],'small_direct_FINAL_batch_Source')
    require(runtime.CAPS == CAPS and batch.CAPS == CAPS
            and runtime.SOURCE_STATUS == 'UNREADY_SOURCE_ONLY'
            and batch.SOURCE_STATUS == 'UNREADY_SOURCE_ONLY',
            'unchanged UNREADY modules; neither Native run nor compile_all_batch is called')
    require(pin(b['actual_stdlib_subprocess_Source_pin']['path'],positive_links=True)
            == b['actual_stdlib_subprocess_Source_pin'],'actual stdlib original positive-link7ID full EOF')
    for role,expected in b['tool_pins'].items():
        budget();runtime.recheck(expected,tool_role=role)
    ns = b['namespaces'];roots = tuple(Path(ns[key]) for key in ('host','output','control','source','receipts'))
    host,out,control,source,receipts = roots
    require(set(ns) == {'host','output','control','source','receipts'}
            and len(set(roots)) == 5
            and not any(p.is_relative_to(q) for p in roots for q in roots if p != q),
            'exact disjoint fresh HOC and minimal frozen new D/E')
    require(all(p.is_absolute() and p != support.ART and p.is_relative_to(support.ART)
                and all(not q.is_symlink() for q in (p,*p.parents)) for p in roots[:3])
            and all(p != support.BASE and p.is_relative_to(support.BASE)
                    and all(not q.is_symlink() for q in (p,*p.parents)) for p in roots[3:]),
            'original ART/base namespace scopes')
    require(not any(os.path.lexists(p) for p in roots[:3])
            and Path(binding_pin['path']).parent == source
            and Path(b['probe_entry_Source_pin']['path']).parent == source
            and Path(b['direct_driver_batch_Source_pin']['path']).parent == source
            and Path(review_pin['path']).parent == receipts,'fresh no-retry HOC; new frozen Source/review roles')
    dfreeze,efreeze = runtime.tree(source),runtime.tree(receipts)
    fresh_d = cases[0]['original_D_freeze'];fresh_e = cases[0]['original_E_freeze']
    fresh_d_root = Path(b['fresh_controls_Source_binding_pin']['path']).parent
    fresh_e_root = Path(fresh['case_namespaces']['closed-before-first']['receipts'])
    require(runtime.tree(fresh_d_root) == fresh_d and runtime.tree(fresh_e_root) == fresh_e,
            'qualified controls D/E remain completely frozen; never modify or reuse as new D/E')
    folder = host/'DIRECT_DRIVER_PROBE'
    recipe = runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Ganlib']
    commands = fixed_driver_commands(folder,b['tool_pins'],recipe)
    require(b['planned_driver_commands'] == [dict(role=role,label='small_'+role,
                command=argv,new_output_path=str(product)) for role,argv,product in commands],
            'all four exact Source-bound original recipe argv and fresh products')
    host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir();folder.mkdir()
    shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
    require(pin(host/'runtime/run_bounded_dragon.py')['sha256'] == support.BOUNDED_SHA,
            'original bounded Source copied before first resources.check')
    history = resource.history_roots([str(p) for p in
        (host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    resources,monitor = runtime.build_exact_owner_resources(support,roots,b['tool_pins'],
        started,dfreeze,efreeze,history,(resource,full,production))
    resources._fresh_frame_Source_contract = dict(policy=POLICY,
        adapter_Source_pin=b['adapter_Source_pin'],new_Source_binding_pin=binding_pin,
        old_controls_qualification_inherited=False)
    runner = None;observer = None;windows = [];timings = [];phase = ['initial_resource']
    inputs = [];outputs = [];actual_error = None
    def scan_sink(joint,scan,owner_state):
        # Existing declared controls-only sink, RAM only. No check or syscall,
        # added waiter, diagnostic, file write, changed guard, or retry here.
        windows.append(accepted_window_timing(joint,phase[0]))
    try:
        before = resources.check();budget()
        windows.append(accepted_window_timing(before,'initial_resource'))
        require(before['artifact_bytes']+2*2**30 < 96*2**30
                and before['disk_free_bytes']-2*2**30 >= 8*2**30,
                'original full-history/free complete reserve')
        runner = full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'DIRECT_DRIVER_PROBE',resources)
        monitor.install_bounded_wrappers(runner)
        observer = runtime.attach_exact_owner_observer(runner,resources,monitor,
            b['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,
            b['owner_helper_Source_pin'],support,control_mode=True)
        require(observer.control_after_original_start is None
                and resources._actual_control_barrier is None,'no controls transition or mocked OS outcome')
        resources._actual_control_scan_sink = scan_sink
        stage_started = time.monotonic();probe_deadline = stage_started+600
        monitor.stage_deadline = probe_deadline;phase[0] = 'aggregate_stage_enter'
        with batch.DirectDriverLibraryStage(runtime,runner,resources,folder,'SmallDriverProbe',
                stage_started,probe_deadline,budget) as stage:
            for name,raw in SMALL_INPUTS.items():
                budget();path = folder/name
                with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
                inputs.append(runtime.fullpin(path,budget))
            for role,argv,product in commands:
                budget();phase[0] = 'direct_'+role
                require(not os.path.lexists(product)
                        and all(o['closed_wait'] is not None for o in observer.owners.values()
                                if o['role'] == 'business'),'fresh output and no previous live business, zero retry')
                owner_count = len(observer.owners);window_first = len(windows);entered = time.monotonic()
                returned = stage.execute_driver(folder,'small_'+role,argv,probe_deadline,budget)
                finished = time.monotonic();budget()
                generated = runtime.fullpin(product,budget)
                require(generated['size_bytes'] > 0,'complete new ordinary nonempty compiler output')
                outputs.append(dict(role=role,new_output_pin=generated))
                if role == 'cpp':inputs.append(generated)
                fresh_windows = windows[window_first:]
                timings.append(dict(role=role,actual_argv=argv,
                    direct_stage_call_started_monotonic=entered,direct_stage_call_finished_monotonic=finished,
                    direct_stage_call_seconds=finished-entered,actual_original_driver=returned,
                    new_owner_count=len(observer.owners)-owner_count,
                    accepted_fresh_windows_count=len(fresh_windows),
                    accepted_fresh_windows_seconds=sum(w['accepted_fresh_window_seconds'] for w in fresh_windows),
                    original_process_watchdog_elapsed_seconds=returned['watchdog']['elapsed_seconds'],
                    sampled_driver_peak_rss_mib=returned['watchdog']['sampled_peak_rss_mib'],
                    positive_RSS_sample_present=returned['watchdog']['sampled_peak_rss_mib'] > 0,
                    zero_RSS_sample_does_not_create_effective_memory_qualification=True,
                    compiler_descendant_RSS_scope_not_certified=True))
                for expected in inputs:runtime.recheck(expected,budget)
            require(len(timings) == 4 and len(observer.owners) == 8
                    and all(o['closed_wait'] is not None for o in observer.owners.values()),
                    'exact four original drivers plus four actual watchdog wait closures')
            phase[0] = 'aggregate_stage_exit'
        phase[0] = 'final_resources';after = resources.check();budget()
        require(len(runner.records) == 1 and runner.records[0]['status'] == 'PASS'
                and not observer.unknown and not monitor.recording_errors and not monitor.unpersisted,
                'only actual small aggregate returned PASS; no unknown/persistence failure hidden')
        for expected in protected:
            budget();require(pin(expected['path']) == expected,'all protected complete Source inputs still exact')
        for role,expected in b['tool_pins'].items():runtime.recheck(expected,budget,tool_role=role)
        require(pin(b['actual_stdlib_subprocess_Source_pin']['path'],positive_links=True)
                == b['actual_stdlib_subprocess_Source_pin'],'full original stdlib remained exact')
        require(runtime.tree(source) == dfreeze and runtime.tree(receipts) == efreeze
                and runtime.tree(fresh_d_root) == fresh_d and runtime.tree(fresh_e_root) == fresh_e,
                'complete new and original qualified controls D/E final freeze')
        for row in outputs:runtime.recheck(row['new_output_pin'],budget)
        saved_timing = add_saved_timing_buckets(windows,monitor.journal,runtime,budget)
        require(saved_timing['fatal_count'] == 0,'no fatal monitor window converted into small driver PASS')
        facts = dict(schema='ACTUAL_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_FACTS_V1',
            status='SMALL_FOUR_DRIVER_COST_EVIDENCE_ONLY_ROOT_TERMINAL_CURRENT_CLOSEOUT_AND_REVIEW_REQUIRED',
            source_only=False,probe_id=PROBE,new_Source_binding_pin=binding_pin,
            independent_Source_prelaunch_review_pin=review_pin,actual_host_PID=os.getpid(),
            adapter_Source_pin=b['adapter_Source_pin'],direct_driver_batch_Source_pin=b['direct_driver_batch_Source_pin'],
            original21_author_Source_contract=author,complete_protected_input_pins=protected,
            original_stdlib_Source_pin=b['actual_stdlib_subprocess_Source_pin'],tool_pins=b['tool_pins'],
            original_helper_pin=hpin,original_resource_factory_pin=rpin,original_caps=CAPS,
            fresh_monitor_controls_RESULT_pin=b['fresh_controls_saved_RESULT_pin'],
            fresh_monitor_controls_independent_saved_review_pin=b['fresh_controls_independent_saved_review_pin'],
            old_controls_qualification_inherited=False,small_inputs_are_original1337_Native_units=False,
            actual_small_source_inputs=inputs,actual_small_generated_outputs=outputs,
            actual_driver_timings=timings,actual_accepted_fresh_windows=windows,
            actual_saved_monitor_timing=saved_timing,actual_stage_records=runner.records,
            actual_owner_state=observer.summary(),actual_monitor_evidence=monitor.summary(include_unpersisted=True),
            actual_resources_before=before,actual_resources_after=after,
            complete_D_freeze=dfreeze,complete_E_freeze=efreeze,
            preserved_qualified_controls_D_freeze=fresh_d,preserved_qualified_controls_E_freeze=fresh_e,
            actual_original_classes_MRO_guard_Helper_modified=False,
            actual_python_business_controller_used=False,actual_retry_count=0,
            whole_seconds=time.monotonic()-started,probe_seconds=time.monotonic()-stage_started,
            actual_Root_tool_terminal=None,actual_Root_current_all_PID_PGID_closeout=None,
            small_driver_composition_qualification=None,original1337_build_time_forecast_qualified=False,
            **NOT_QUALIFIED)
        result = host/'ACTUAL_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_FACTS.json'
        monitor.write_failure_result(result,facts)
        require(result.is_file() and not monitor.recording_errors and not monitor.unpersisted,
                'complete small probe facts persisted and final write accounting did not fail')
        account = monitor.disk_account(0);budget()
        print(json.dumps(dict(status=facts['status'],actual_facts_pin=pin(result),
            actual_final_report_append_account=account,whole_seconds=time.monotonic()-started,
            probe_seconds=time.monotonic()-stage_started,
            actual_external_Root_terminal_current_closeout_and_review_required=True,
            **NOT_QUALIFIED),allow_nan=False),flush=True)
    except BaseException as error:
        actual_error = runtime.monitor_error(error)
        try:summary = monitor.summary(include_unpersisted=True)
        except BaseException as summary_error:
            summary = dict(actual_summary_error=runtime.monitor_error(summary_error),
                complete_unpersisted_events=monitor.unpersisted,
                complete_recording_errors=monitor.recording_errors,journal_repaired=False,resource_PASS=False)
        monitor.write_failure_result(host/'FAILED_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_FACTS.json',dict(
            schema='FAILED_ORIGINAL_DIRECT_DRIVER_SMALL_PROBE_FACTS_V1',status='FAILED_NO_RETRY_NO_QUALIFICATION',
            new_Source_binding_pin=binding_pin,actual_host_PID=os.getpid(),actual_error=actual_error,
            actual_stage_records=[] if runner is None else runner.records,
            actual_owner_state=None if observer is None else observer.summary(),
            actual_monitor_evidence=summary,actual_completed_driver_timings=timings,
            actual_accepted_fresh_windows=windows,original_caps=CAPS,
            whole_seconds=time.monotonic()-started,new_resource_check_used_to_repair_failure=False,
            actual_Root_tool_terminal=None,actual_Root_current_all_PID_PGID_closeout=None,**NOT_QUALIFIED))
        raise
    finally:
        resources._actual_control_scan_sink = None
        try:
            if observer is not None:observer.restore_original_objects()
        finally:monitor.restore_bounded_objects()


if __name__ == '__main__':
    main()

"""Source-only complete Native build and genuine A then B observation workflow.

No imports of candidates, compiler, OS diagnostic or business action occur at
import time. This helper has no standalone execution CLI. Root must bind the
whole reviewed workflow, an immutable READY copy of the tested grouped helper,
the actual grouped controls and their separate saved-result review. The fresh
monitor's real ten-control results are checked by the same public contract
admission helper as the tiny grouped controls. Old N8 qualification is not used.

The original complete archive, overlays, 1337 units, original five stages and
material decks are retained. Only the already specified three procedure FIL
literals may differ. Material observation is evidence, not physical acceptance.
"""
import hashlib
import os
import platform
from pathlib import Path
import sys
import shutil
import stat
import tarfile
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
READY_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
POLICY = 'FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
    joint_archive_bytes=2*2**30,history_bytes=96*2**30,
    free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
UNREADY_GROUPED_SHA = 'ef35a10a289b99b02cd9136dbcdeed8732c02fe07e495d0af16aec27444720b7'
ADAPTER_SHA = 'a2b507e0f5e5470c227484f1d8a1e63367aed2313cb15695a9c46b57a2d444cc'
BUILD_ORDER = ['Ganlib','Utilib','Trivac','Dragon','Dragon_link']
PAYLOAD_ROLES = {
    'native_Source_archive':'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz',
    'native_Source_index':'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json',
    'LIBMIX_observation':'OBSERVATION_SOURCE/LIBMIX.observe.UNREADY.f',
    'LIBDEN_observation':'OBSERVATION_SOURCE/LIBDEN.observe.UNREADY.f',
    'TONDRV_observation':'OBSERVATION_SOURCE/TONDRV.context_observe.UNREADY.f',
    'TONSPH_observation':'OBSERVATION_SOURCE/TONSPH.observe.UNREADY.f',
    'observer_module':'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',
}


def require(value,message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def unique_regular_bytes(freezes):
    seen = set();total = 0
    for freeze in freezes:
        for p in freeze['files']:
            key = tuple(p['identity'][:2])
            require(key not in seen,'all external D/E regular identities disjoint')
            seen.add(key);total += p['size_bytes']
    return total


def validate_full_request(runtime,contract,b,binding_pin,review_pin,budget):
    """Full admission, separate from the old fixed-v9/N8 runtime.run gate."""
    require(SOURCE_STATUS == READY_STATUS,'UNREADY full workflow refuses Native action')
    require(b['schema'] == 'ROOT_GROUPED_COMPLETE_NATIVE_AB_SOURCE_BINDING_V1'
        and b['source_only'] is True and b['Root_only_actual_execution'] is True
        and b['actual_execution'] is None and b['policy'] == POLICY
        and b['old_controls_qualification_inherited'] is False
        and b['original_caps'] == CAPS
        and all(type(v) is int for v in b['original_caps'].values()),
        'Root complete workflow Source binding, exact original typed nine caps')
    runtime.recheck(binding_pin,budget);runtime.recheck(review_pin,budget)
    runtime.recheck(b['full_workflow_Source_pin'],budget)
    require(b['full_workflow_Source_pin']['path'] == str(Path(__file__).absolute())
        and b['adapter_Source_pin']['sha256'] == ADAPTER_SHA,
        'this exact full workflow and genuinely controlled d18 adapter')
    original = contract.admit_original_contract_and_actual_ten_controls(
        b,binding_pin,budget,[b['full_workflow_Source_pin'],
            b['grouped_READY_Source_pin'],b['contract_entry_Source_pin']])
    require(type(original) is dict and set(original) == {'fresh','author','cases','protected'},
        'same public full original and actual ten-control admission context')
    author = original['author'];protected = original['protected']
    require(b['original21_author_Source_contract'] == author and len(author) == 21,
        'complete original21 Source roles remain unchanged')
    for key,value in runtime.FUTURE.items():
        require(b[key] is value,'no future physical or context qualification: '+key)
    require(b['state_order'] == ['A','B'] and b['build_stage_order'] == BUILD_ORDER
        and b['SPOT_AXMAT_OBSERVATION'] == 'ADMITTED_SOURCE_ONLY'
        and b['material_input_layout'] == runtime.SHARED_INPUT_LIBRARY_LAYOUT,
        'original five complete stages, A then B and exact shared-input layout')
    seed = contract.metadata(author['original_material_seed_contract'])
    require(b['original129_input_pins'] == seed['original129_input_pins']
        and len(b['original129_input_pins']) == 129
        and len({p['path'] for p in b['original129_input_pins']}) == 129,
        'all original129 ordered full input pins')
    protected.extend(b['original129_input_pins'])
    require(type(b['states']) is dict and list(b['states']) == ['A','B'],
        'original complete ordered material states')
    for state in ('A','B'):
        rows = b['states'][state]['native_stage_inputs']
        require([r['destination'] for r in rows]
            == runtime.SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order'],
            'all seven original material input roles in order')
        for row in rows:
            require(type(row) is dict and set(row) == {'destination','input_pin'},
                'only an original complete input pin and literal destination')
            p = row['input_pin'];runtime.recheck(p,budget);protected.append(p)
            wanted = seed['states'][state].get(row['destination'])
            if wanted is not None:
                require(p == wanted,'unchanged original full material seed')
            else:
                library = seed['libraries'][row['destination']]
                require(p['path'] == library['path']
                    and p['sha256'] == library['generation_sha256'],
                    'whole original generated library path and bytes')
        require(b['states'][state]['original_material_deck_pin'] == rows[0]['input_pin'],
            'actual original material deck, no regenerated physics')
    ready = b['grouped_READY_Source_pin'];runtime.recheck(ready,budget)
    tested = b['grouped_tested_UNREADY_Source_pin'];runtime.recheck(tested,budget)
    raw = Path(ready['path']).read_bytes()
    marker = ("SOURCE_STATUS = '"+READY_STATUS+"'").encode('ascii')
    require(raw.count(marker) == 1 and tested['sha256'] == UNREADY_GROUPED_SHA
        and hashlib.sha256(raw.replace(marker,b"SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'",1)).hexdigest()
            == tested['sha256'],
        'immutable READY Source differs from tested V2 only by one readiness literal')
    protected.extend([tested,ready])
    gate_pin = b['actual_grouped_controls_gate_pin'];gate = contract.metadata(gate_pin)
    require(gate['schema'] == 'ROOT_GROUPED_DIRECT_COMPILER_SAVED_CONTROLS_V1'
        and gate['source_only'] is False and gate['all_required_controls_passed'] is True
        and gate['blockers'] == [] and gate['original_caps'] == CAPS
        and gate['tested_UNREADY_Source_pin'] == tested
        and gate['actual_entry_Source_pin'] == b['contract_entry_Source_pin']
        and gate['required_case_ids'] == b['grouped_controls_required_case_ids']
        and gate['required_case_ids'] == list(contract.CONTROL_ORDER_GROUPED)
        and len(gate['required_case_ids']) == 16
        and gate['full_Native_build_qualified'] is False
        and gate['scientific_qualification_created'] is False,
        'complete actual grouped controls admission, not guessed or inherited results')
    protected.append(gate_pin)
    for key in ('actual_facts_pin','actual_closed_zero_tool_return_pin',
                'actual_current_closeout_pin','independent_saved_result_review_pin'):
        p = gate[key];runtime.recheck(p,budget);protected.append(p)
    terminal = contract.metadata(gate['actual_closed_zero_tool_return_pin'])
    actual = terminal['terminal_tool_return']
    require(terminal['closed'] is True and terminal['observed_terminal'] is True
        and type(actual['exit_code']) is int and actual['exit_code'] == 0
        and 'session_id' not in actual and terminal['actual_terminal_chunk'] == actual['chunk_id'],
        'genuine observed CLOSED zero grouped control tool return')
    # The genuine external tool output is empty because the original streams
    # were redirected before launch. Never rewrite it to contain saved stdout.
    require(actual['output'] == '', 'actual redirected CLOSED tool output kept byteexact')
    for key in ('actual_complete_stdout_pin','actual_complete_stderr_pin',
                'actual_capture_tool_receipt_pin'):
        p = gate[key];runtime.recheck(p,budget);protected.append(p)
    capture = contract.metadata(gate['actual_capture_tool_receipt_pin'])
    require(capture['schema'] == 'ROOT_GENUINE_GROUPED16_TINY_CONTROLS_TOOL_AND_COMPLETE_CAPTURE_V1'
        and capture['actual_final_tool_return'] == actual
        and capture['actual_terminal_closed'] is True
        and capture['complete_original_stdout_available'] is True
        and capture['raw_output_truncation_preserved'] is False
        and capture['stdout_and_stderr_redirected_to_fresh_files_before_launch'] is True
        and capture['files_copied_only_after_actual_terminal_closed'] is True
        and capture['captured_streams_reconstructed'] is False
        and capture['actual_stdout_file_pin'] == gate['actual_complete_stdout_pin']
        and capture['actual_stderr_file_pin'] == gate['actual_complete_stderr_pin'],
        'complete real prelaunch redirected stdout/stderr coupled to exact actual terminal')
    raw_receipt = capture['actual_redirected_tool_receipt_pin']
    runtime.recheck(raw_receipt,budget);protected.append(raw_receipt)
    redirected = contract.metadata(raw_receipt)
    require(redirected['actual_final_tool_return'] == actual
        and redirected['actual_terminal_closed'] is True
        and redirected['fresh_redirect_paths_checked_before_launch'] is True
        and redirected['shell_noclobber_enforced'] is True,
        'original genuine redirected tool receipt preserved, no rebuilt streams')
    output = contract.metadata(gate['actual_complete_stdout_pin'])
    require(output['actual_facts_pin'] == gate['actual_facts_pin'],
        'complete actual captured stdout coupled to exact complete actual facts')
    facts = contract.metadata(gate['actual_facts_pin'])
    require(facts['schema'] == 'ACTUAL_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS_V2'
        and facts['source_only'] is False and facts['original_caps'] == CAPS
        and facts['direct_driver_batch_Source_pin'] == tested
        and facts['new_Source_binding_pin'] == gate['actual_controls_Source_binding_pin']
        and facts['independent_Source_prelaunch_review_pin'] == gate['actual_controls_Source_review_pin']
        and facts['fresh_monitor_controls_RESULT_pin'] == b['fresh_controls_saved_RESULT_pin']
        and facts['original_stdlib_Source_pin'] == b['actual_stdlib_subprocess_Source_pin']
        and facts['tool_pins'] == b['tool_pins']
        and facts['original21_author_Source_contract'] == author
        and facts['actual_grouped_control_manifest'] == contract.grouped_control_manifest()
        and [c['case_id'] for c in facts['actual_all_sixteen_grouped_controls']] == gate['required_case_ids']
        and all(c['expected_outcome_observed'] is True
            for c in facts['actual_all_sixteen_grouped_controls'])
        and [r['status'] for r in facts['actual_stage_records']] == ['PASS']*5+['FAILED']*4
        and facts['actual_retry_count'] == 0 and facts['old_controls_qualification_inherited'] is False
        and facts['actual_python_business_controller_used'] is False
        and facts['actual_monitor_evidence']['additional_recording_errors'] == []
        and facts['actual_monitor_evidence']['unpersisted_complete_events'] == []
        and facts['actual_saved_monitor_timing']['fatal_count'] == 0,
        'all exact sixteen actual grouped controls, Source/caps/monitor/waits and retained failures')
    for key,value in contract.NOT_QUALIFIED.items():
        require(facts[key] is value,'tiny control facts grant no Native or science: '+key)
    for p in (gate['actual_controls_Source_binding_pin'],gate['actual_controls_Source_review_pin']):
        runtime.recheck(p,budget);protected.append(p)
    actual_group_binding = contract.metadata(gate['actual_controls_Source_binding_pin'])
    require(actual_group_binding['probe_entry_Source_pin'] == b['contract_entry_Source_pin']
        and actual_group_binding['direct_driver_batch_Source_pin'] == tested
        and actual_group_binding['control_execution_order'] == list(contract.CONTROL_ORDER_GROUPED)
        and actual_group_binding['small_input_contract'] == contract.grouped_input_contract()
        and actual_group_binding['planned_control_manifest'] == contract.grouped_control_manifest(),
        'actual grouped Source contract matches this whole frozen entry and fixture set')
    close = contract.metadata(gate['actual_current_closeout_pin'])
    require(close['all_recorded_PIDs_and_groups_currently_absent'] is True,
        'actual grouped controls currently closed, no historical cleanup inference')
    review = contract.metadata(review_pin)
    require(review['schema'] == 'INDEPENDENT_GROUPED_COMPLETE_NATIVE_AB_SOURCE_REVIEW_V1'
        and review['source_only'] is True and review['all_checks_passed'] is True
        and review['blockers'] == [] and review['new_Source_binding_pin'] == binding_pin
        and review['full_workflow_Source_pin'] == b['full_workflow_Source_pin']
        and review['grouped_READY_Source_pin'] == ready
        and review['actual_grouped_controls_gate_pin'] == gate_pin,
        'separate complete Source review of this exact full binding and actual controls')
    protected.append(review_pin)
    require(type(b['native_payload_pins']) is dict
        and set(b['native_payload_pins']) == set(PAYLOAD_ROLES),
        'whole original archive/index and all five observation overlay roles')
    droot = Path(b['namespaces']['source'])
    original_manifest = contract.metadata(author['qualified_source_manifest'])
    declared = original_manifest['members']
    require(len({r['relative_path'] for r in declared}) == len(declared),
        'unique complete original author Source manifest members')
    original_members = {r['relative_path']:r['fullpin'] for r in declared}
    for role,relative in PAYLOAD_ROLES.items():
        copy = b['native_payload_pins'][role];original_pin = b['original_native_payload_pins'][role]
        runtime.recheck(copy,budget);runtime.recheck(original_pin,budget)
        require(original_members.get(relative) == original_pin
            and copy['path'] == str(droot/relative)
            and copy['sha256'] == original_pin['sha256']
            and copy['size_bytes'] == original_pin['size_bytes'],
            'complete original payload copied unchanged into new frozen D')
        protected.extend([copy,original_pin])
    require(b['original_native_payload_pins']['native_Source_archive'] == author['native_Source_archive']
        and b['original_native_payload_pins']['native_Source_index'] == author['native_Source_index']
        and b['original_native_payload_pins']['observer_module'] == author['observer_module'],
        'actual original native archive/index and observer Source roles')
    # All fullpins remain bound, including repeated declaration consistency.
    by_path = {}
    for p in protected:
        budget();require(p['path'] not in by_path or by_path[p['path']] == p,
            'all duplicate protected declarations agree exactly')
        by_path[p['path']] = p
    tool_roles = {p['path']:role for role,p in b['tool_pins'].items()}
    for role,p in b['tool_pins'].items():
        runtime.recheck(p,budget,tool_role=role)
        require(p['path'] not in by_path or by_path[p['path']] == p,
            'all six canonical tool declarations agree')
        by_path[p['path']] = p
    for p in by_path.values():runtime.recheck(p,budget,tool_role=tool_roles.get(p['path']))
    return dict(author=author,protected=list(by_path.values()),
        fresh_control_cases=original['cases'],fresh_binding=original['fresh'],
        scope=dict(schema='ACTUAL_GROUPED_COMPLETE_NATIVE_AB_SCOPE_COUPLING_V1',
            actual_ten_controls_saved_RESULT_pin=b['fresh_controls_saved_RESULT_pin'],
            actual_grouped_controls_gate_pin=gate_pin,full_Source_review_pin=review_pin,
            all_original129_and21_roles_retained=True,**runtime.FUTURE))


def run_workflow(runtime,contract,b,binding_pin,review_pin,started,support,batch):
    """Whole actual build + A/B + final checks within the original1800 seconds."""
    require(SOURCE_STATUS == READY_STATUS,'UNREADY full workflow refuses Native action')
    def budget():
        require(time.monotonic()-started < CAPS['whole_seconds'],
            'whole1800 includes binding, bootstrap, five stages, A/B and closure')
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
        and sys.gettrace() is None and sys.getprofile() is None
        and all(os.environ.get(k) == '1' for k in runtime.THREAD_KEYS)
        and Path(sys.executable).resolve() == support.PYTHON
        and platform.system() == 'Darwin' and platform.machine() == 'arm64',
        'actual original nonoptimized unprofiled canonical Python/Darwin and five thread caps')
    sys.dont_write_bytecode = True
    require(Path(runtime.__file__).resolve() == Path(b['adapter_Source_pin']['path'])
        and Path(contract.__file__).resolve() == Path(b['contract_entry_Source_pin']['path'])
        and Path(batch.__file__).resolve() == Path(b['grouped_READY_Source_pin']['path'])
        and Path(support.__file__).resolve() == Path(b['support_Source_pin']['path']),
        'same exact loaded runtime/contract/batch/support Source roles')
    expected_guards = dict(original_helper=(support.OLD_HELPER,support.OLD_HELPER_SHA),
        resource_factory=(support.RESOURCE_FACTORY,support.RESOURCE_SHA),
        full=(support.FULL,support.FULL_SHA),production=(support.PARENT,support.PARENT_SHA),
        bounded=(support.BOUNDED,support.BOUNDED_SHA))
    require(set(b['genuine_guard_Source_pins']) == set(expected_guards)
        and all(b['genuine_guard_Source_pins'][role]['path'] == str(path)
            and b['genuine_guard_Source_pins'][role]['sha256'] == digest
            for role,(path,digest) in expected_guards.items()),
        'all five exact original guard/helper/resource Source roles')
    context = validate_full_request(runtime,contract,b,binding_pin,review_pin,budget)
    author = context['author'];inputs = context['protected'];scope = context['scope']
    fullpin,recheck,tree,write_new = runtime.fullpin,runtime.recheck,runtime.tree,runtime.write_new
    require(runtime.CAPS == CAPS and batch.CAPS == CAPS
        and runtime.SOURCE_STATUS == 'UNREADY_SOURCE_ONLY'
        and batch.SOURCE_STATUS == READY_STATUS,
        'unchanged public d18 functions and separately admitted immutable grouped Source')
    require(contract.pin(b['contract_entry_Source_pin']['path']) == b['contract_entry_Source_pin']
        and contract.pin(b['actual_stdlib_subprocess_Source_pin']['path'],positive_links=True)
            == b['actual_stdlib_subprocess_Source_pin'],
        'same public contract entry and actual full original stdlib with real positive links')
    host,out,control,archive,receipts = roots = tuple(Path(b['namespaces'][k])
        for k in ('host','output','control','source','receipts'))
    require(set(b['namespaces']) == {'host','output','control','source','receipts'}
        and len(set(roots)) == 5
        and not any(p.is_relative_to(q) for p in roots for q in roots if p != q),
        'five complete disjoint H/O/C/D/E paths')
    require(all(p.is_absolute() and p != support.ART and p.is_relative_to(support.ART)
        and all(not q.is_symlink() for q in (p,*p.parents)) for p in roots[:3])
        and all(p.is_absolute() and p != support.BASE and p.is_relative_to(support.BASE)
        and all(not q.is_symlink() for q in (p,*p.parents)) for p in roots[3:])
        and not any(os.path.lexists(p) for p in roots[:3])
        and Path(binding_pin['path']).parent == archive
        and Path(review_pin['path']).parent == receipts,
        'original ART/base scopes, frozen new D/E, fresh zero-retry HOC')
    dfreeze,efreeze = tree(archive),tree(receipts)
    external = unique_regular_bytes((dfreeze,efreeze))
    fresh_cases = context['fresh_control_cases'];fresh = context['fresh_binding']
    old_d = Path(b['fresh_controls_Source_binding_pin']['path']).parent
    old_e = Path(fresh['case_namespaces']['closed-before-first']['receipts'])
    require(tree(old_d) == fresh_cases[0]['original_D_freeze']
        and tree(old_e) == fresh_cases[0]['original_E_freeze'],
        'qualified monitor control D/E held; no reuse or modification')
    tool_roles = {p['path']:role for role,p in b['tool_pins'].items()}
    helper,hpin = support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'grouped_AB_original619')
    resource,rpin = support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'grouped_AB_original_ebbb')
    full,production = helper.modules();helper.guard_admission(full)
    require(full.OwnRSSSerialExecutor.__bases__ == (production.SerialExecutor,)
        and Path(full.__file__).resolve() == support.FULL
        and Path(production.__file__).resolve() == support.PARENT,
        'genuine unchanged original supervisor classes, MRO and Source paths')
    genuine = [support.pin(support.FULL,support.FULL_SHA),
        support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
    history = resource.history_roots([str(p) for p in
        (host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    disk = resource.DynamicHistoryResources(support.ART,history,
        CAPS['free_floor_bytes'],CAPS['history_bytes'],production.ResourceFailure)
    runner = None;owner = None;resources = None;monitor = None;before = None;bootstrap = None
    try:
        # Genuine original disk-only admission before any output directory.
        # This is not a passing fulljoint PS/lsof census. External D/E count
        # once; the original2GiB future reserve applies to history/free only.
        budget();disk_before = disk.check();budget()
        require(external < CAPS['joint_archive_bytes']
            and disk_before['artifact_bytes']+external+CAPS['joint_archive_bytes'] < CAPS['history_bytes']
            and disk_before['disk_free_bytes']-CAPS['joint_archive_bytes'] >= CAPS['free_floor_bytes'],
            'actual original complete-history/free reserve and existing strict joint D/E')
        bootstrap = dict(actual_original_disk_only_before=disk_before,
            actual_complete_external_D_E_regular_bytes=external,
            fulljoint_process_census_claimed=False,future_joint_reserve_inside_joint_cap=False)
        host.mkdir();out.mkdir();control.mkdir()
        (host/'runtime').mkdir();(host/'OBSERVATION_BUILD').mkdir()
        shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
        require(fullpin(host/'runtime/run_bounded_dragon.py',budget)['sha256'] == support.BOUNDED_SHA,
            'original bounded guard Source copied before full monitor check')
        resources,monitor = runtime.build_exact_owner_resources(support,roots,b['tool_pins'],
            started,dfreeze,efreeze,history,(resource,full,production))
        resources._fresh_frame_Source_contract = dict(policy=POLICY,
            adapter_Source_pin=b['adapter_Source_pin'],new_Source_binding_pin=binding_pin,
            old_controls_qualification_inherited=False)
        resources._required_monitor_controls_scope = scope
        runner = full.OwnRSSSerialExecutor(host,CAPS['whole_seconds']-(time.monotonic()-started),
            'OBSERVATION_BUILD',resources)
        require(type(runner) is full.OwnRSSSerialExecutor and runner.resources is resources
            and Path(runner.bounded.__file__).resolve() == host/'runtime/run_bounded_dragon.py',
            'same original genuine guarded runner and local bounded Source')
        monitor.install_bounded_wrappers(runner)
        owner = runtime.attach_exact_owner_observer(runner,resources,monitor,
            b['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,
            b['owner_helper_Source_pin'],support,control_mode=False)
        require(resources._actual_control_barrier is None and resources._actual_control_scan_sink is None
            and owner.control_after_original_start is None
            and all(runner.env.get(k) == '1' for k in runtime.THREAD_KEYS),
            'actual production scope, original one-thread environment, no control hooks')
        before = resources.check();budget()
        runner.env['SPOT_AXMAT_OBSERVATION'] = 'ADMITTED_SOURCE_ONLY'
        native = host/'native';native.mkdir()
        index = runtime.strict_json((archive/PAYLOAD_ROLES['native_Source_index']).read_bytes())
        index['_path'] = str(archive/PAYLOAD_ROLES['native_Source_index'])
        members = {r['relative_path']:r for r in index['members']}
        require(len(members) == len(index['members']) == 1365,
            'complete original1365 unique archive entries')
        with tarfile.open(archive/PAYLOAD_ROLES['native_Source_archive'],'r:gz') as t:
            entries = t.getmembers()
            require(len(entries) == len(members) and {m.name for m in entries} == set(members),
                'whole complete original archive indexed exact member coverage')
            for member in entries:
                budget();require(member.isfile() and member.name in members
                    and '..' not in Path(member.name).parts and not Path(member.name).is_absolute(),
                    'only indexed ordinary safe native Source members')
                dest = native/member.name;dest.parent.mkdir(parents=True,exist_ok=True)
                with t.extractfile(member) as src,dest.open('xb') as dst:
                    shutil.copyfileobj(src,dst,2**20)
                p = fullpin(dest,budget);expected = members[member.name]['full_original_Source_pin']
                require(p['sha256'] == expected['sha256'] and p['size_bytes'] == expected['size_bytes'],
                    'all full original archive bytes consumed unchanged')
        observer = archive/'OBSERVATION_SOURCE'
        for original,derived in [('LIBMIX.f','LIBMIX.observe.UNREADY.f'),
                ('LIBDEN.f','LIBDEN.observe.UNREADY.f'),
                ('TONDRV.f','TONDRV.context_observe.UNREADY.f'),('TONSPH.f','TONSPH.observe.UNREADY.f')]:
            target = native/'Dragon/src'/original
            require(fullpin(target,budget)['sha256']
                == members['Dragon/src/'+original]['full_original_Source_pin']['sha256'],
                'original physical Source before exact observation overlay')
            target.write_bytes((observer/derived).read_bytes())
        shutil.copy2(observer/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',
            native/'Dragon/src/AXMAT_CONTEXT_OBSERVATION_MOD.f90')
        ep,build = batch.compile_all_batch(runtime,native,index,observer,b['tool_pins'],
            runner,support,resources,budget,b['grouped_READY_Source_pin'])
        require(build['stage_order'] == BUILD_ORDER and build['all1337_units_compiled_once'] is True
            and build['original13_cpp_commands_preserved'] is True,
            'all original1337 units and13 cpp plus original five complete stages')
        write_new(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',build)
        bp = fullpin(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',budget)
        states = {};shared = runtime.prepare_shared_libraries(out,b,budget);resources.check()
        for state in ('A','B'):
            budget();recheck(ep,budget);folder = out/state;folder.mkdir()
            shared_before = runtime.recheck_shared_libraries(shared,budget)
            copies,mapping,procedure = runtime.copy_state_seeds(folder,
                b['states'][state]['native_stage_inputs'],shared,budget)
            resources.check()
            stage = runtime.guarded(runner,support,resources,folder,'material',[ep['path']],
                time.monotonic()+CAPS['stage_seconds'],budget,deck='material.x2m',
                marker='AXMAT-MATERIAL-'+state+'-COMPLETE')
            for p in copies:recheck(p,budget)
            shared_after = runtime.recheck_shared_libraries(shared,budget)
            require(shared_before == shared_after,'original/shared library complete bytes and identities held')
            states[state] = runtime.collect_state(folder,state,
                b['states'][state]['original_material_deck_pin'],ep,stage,budget)
            states[state]['actual_material_seed_copy_pins'] = copies
            states[state]['actual_material_seed_role_mapping'] = mapping
            states[state]['actual_original_and_consumed_procedure_Source_evidence'] = procedure
            shared['actual_state_library_full_EOF_observations'][state] = dict(
                before_actual_material_stage=shared_before,after_actual_material_stage=shared_after)
            recheck(ep,budget);closure = resources.check()
            require(not any(Path(p).is_relative_to(folder)
                or Path(p).is_relative_to(Path(shared['shared_library_directory']))
                for p in closure['actual_open_regular_paths']),
                'all observed own state/shared-library handles closed before next state')
            states[state]['actual_no_open_state_handles_observation'] = closure
            write_new(control/('ACTUAL_'+state+'_CLOSED_OBSERVATION_CAPTURE.json'),states[state])
            resources.check();budget()
        manifest = dict(schema='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1',
            source_only=False,state_order=['A','B'],states=states,
            material_input_layout=runtime.SHARED_INPUT_LIBRARY_LAYOUT,
            actual_shared_input_library_evidence=shared,
            complete_state_snapshot_inputs={k:v['complete_state_snapshot_inputs'] for k,v in states.items()},
            complete_context_inputs={k:v['complete_context_pins'] for k,v in states.items()},
            legacy_context_source_snapshot_request_rows={k:v['legacy_context_source_snapshot_request_rows']
                for k,v in states.items()},
            legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',
            actual_native_snapshot_root_prefix=[],all_A_handles_closed_before_B=True,
            actual_Source_binary_link_evidence_pin=bp,actual_observer_executable_pin=ep,
            actual_full_Source_review_pin=review_pin,actual_Source_scope_coupling=scope,
            original_caps=CAPS,actual_material_build_and_observation_executed=True,
            Root_observed_tool_terminal=None,Root_postclose_coverage_contract=None,
            new_native_walker_controls_actual_run=None,new_complete_aggregation_controls_actual_run=None,
            actual_frozen_native_Source_object_link_exe_evidence_saved=True,**runtime.FUTURE)
        write_new(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',manifest)
        mp = fullpin(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',budget)
        for p in inputs:recheck(p,budget,tool_role=tool_roles.get(p['path']))
        require(contract.pin(b['actual_stdlib_subprocess_Source_pin']['path'],positive_links=True)
            == b['actual_stdlib_subprocess_Source_pin'],'whole original stdlib remains exact')
        require(tree(old_d) == fresh_cases[0]['original_D_freeze']
            and tree(old_e) == fresh_cases[0]['original_E_freeze'],
            'qualified ten-control Source/receipts remain wholly frozen after business')
        after = resources.check()
        require(tree(archive) == dfreeze and tree(receipts) == efreeze,'new complete D/E final freeze')
        budget()
        value = dict(schema='ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_GENUINE_HOST_RESULT_V1',
            status='ACTUAL_COMPLETE_FIVE_STAGE_BUILD_AND_AB_OBSERVATION_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REQUIRED',
            source_only=False,actual_host_PID=os.getpid(),original_caps=CAPS,
            original_helper_pin=hpin,resource_factory_pin=rpin,genuine_guard_pins=genuine,
            supervisor_class_or_MRO_modified=False,own_child_RSS_scope_only=True,
            compiler_descendant_RSS_scope_not_certified=True,actual_build_evidence_pin=bp,
            actual_observation_manifest_pin=mp,all_stage_records=runner.records,
            complete_input_pins_before_and_after=inputs,complete_Source_D_freeze=dfreeze,
            complete_receipt_E_freeze=efreeze,actual_bootstrap_disk_only_evidence=bootstrap,
            resources_before=before,resources_after=after,whole_seconds=time.monotonic()-started,
            actual_Source_scope_coupling=scope,actual_Root_observed_terminal=None,
            actual_failure_only_monitor_evidence=monitor.summary(),**runtime.FUTURE)
        # The same original monitored writer enforces complete actual account
        # before and after this successful evidence append; it grants no science.
        monitor.write_failure_result(host/'result.json',value)
        require((host/'result.json').is_file()
            and not monitor.recording_errors and not monitor.unpersisted,
            'successful complete result written without swallowed recording or account errors')
        result_pin = fullpin(host/'result.json',budget)
        saved = contract.metadata(result_pin);budget()
        require(saved['schema'] == value['schema'] and saved['status'] == value['status']
            and saved['original_caps'] == CAPS
            and saved['actual_build_evidence_pin'] == bp
            and saved['actual_observation_manifest_pin'] == mp
            and all(saved[k] is v for k,v in runtime.FUTURE.items()),
            'whole saved successful JSON result retains actual build/material evidence and no future qualification')
        recheck(result_pin,budget)
        resources.check();budget()
        require(not monitor.recording_errors and not monitor.unpersisted,
            'successful final account has no unpersisted or swallowed recording errors')
        recheck(result_pin,budget)
        print(__import__('json').dumps(dict(status=value['status'],
            actual_host_result_pin=result_pin,
            actual_observation_manifest_pin=mp,actual_build_evidence_pin=bp,
            actual_external_Root_typed_CLOSED_required=True,**runtime.FUTURE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():
            errors = [];after_inputs = [];after_D_E = None;after_resources = None
            for p in inputs:
                try:after_inputs.append(recheck(p,tool_role=tool_roles.get(p['path'])))
                except BaseException as e:errors.append(dict(path=p['path'],error=repr(e)))
            try:
                after_D_E = dict(Source=tree(archive),receipts=tree(receipts))
                require(after_D_E == dict(Source=dfreeze,receipts=efreeze),'failed whole D/E freeze')
                after_resources = disk.check() if resources is None else resources.check()
            except BaseException as e:errors.append(dict(scope='failed_D_E_and_resource',error=repr(e)))
            failure = dict(schema='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1',
                status='FAILED_NO_RETRY_NO_QUALIFICATION',error=repr(error),
                actual_bootstrap_disk_only_evidence=bootstrap,complete_input_pins_before=inputs,
                complete_input_pins_after_failure=after_inputs,
                complete_D_E_freeze_before=dict(Source=dfreeze,receipts=efreeze),
                complete_D_E_freeze_after_failure=after_D_E,full_postfailure_freeze_errors=errors,
                full_postfailure_freeze_checked=(errors == []),actual_resources_after_failure=after_resources,
                all_stage_records=[] if runner is None else runner.records,
                whole_seconds=time.monotonic()-started,original_caps=CAPS,
                actual_Root_observed_terminal=None,
                actual_failure_only_monitor_evidence=None if monitor is None
                    else monitor.summary(include_unpersisted=True),**runtime.FUTURE)
            if monitor is not None:
                monitor.write_failure_result(host/'failed_host_result.json',failure)
            else:
                # A partial mkdir/copy bootstrap can precede monitor creation.
                # Its evidence is finite within the already admitted reserve;
                # record the actual disk result, never fake a fulljoint census.
                raw = (__import__('json').dumps(failure,indent=2,allow_nan=False)+'\n').encode('utf-8')
                account = disk.check();regular = external
                for root in roots[:3]:
                    if not root.exists():continue
                    for p in root.rglob('*'):
                        s = p.lstat();require(not stat.S_ISLNK(s.st_mode),'partial bootstrap nonalias')
                        if stat.S_ISDIR(s.st_mode):continue
                        require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1,'partial bootstrap regular singlelink')
                        regular += s.st_size
                require(regular+len(raw) < CAPS['joint_archive_bytes']
                    and account['artifact_bytes']+external+len(raw) <= CAPS['history_bytes']
                    and account['disk_free_bytes']-len(raw) >= CAPS['free_floor_bytes'],
                    'actual partial-bootstrap evidence bytes within original disk caps')
                with (host/'failed_host_result.json').open('xb') as stream:
                    stream.write(raw);stream.flush();os.fsync(stream.fileno())
                disk.check()
        raise
    finally:
        try:
            if owner is not None:owner.restore_original_objects()
        finally:
            if monitor is not None:monitor.restore_bounded_objects()


if __name__ == '__main__':
    raise RuntimeError('UNREADY Source-only full workflow has no standalone execution CLI')

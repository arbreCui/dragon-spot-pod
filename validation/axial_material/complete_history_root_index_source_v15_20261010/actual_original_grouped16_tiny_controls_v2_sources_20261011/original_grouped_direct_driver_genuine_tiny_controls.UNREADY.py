"""UNREADY Source only; Root-bound genuine grouped tiny compiler controls.

Inherits the full e291 original admission, protected Sources, actual ten monitor
controls, guards, owner observer, six tools, fixed caps and failure/finally path.
No candidate import-time work, READY assignment, compiler controller, full batch
or material run. Tiny controls call the same public production helper/closure.
Root must supply a fresh binding and independent review before any execution.
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
SCOPE = 'ROOT_ORIGINAL_GROUPED_DIRECT_DRIVER_GENUINE_TINY_CONTROLS_ONLY'
PROBE = 'CANONICAL_ORIGINAL_GROUPED16_GENUINE_TINY_CONTROLS_V2'
POLICY = 'FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
            joint_archive_bytes=2*2**30,history_bytes=96*2**30,
            free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
SUPPORT = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
ADAPTER_SHA = 'd18ce676d776b674429d0c3e976466f5ab417ef4439f16f47aadef6a7ce9f50d'
BATCH_SHA = 'ef35a10a289b99b02cd9136dbcdeed8732c02fe07e495d0af16aec27444720b7'
CONTROL_ORDER = ('closed-before-first','exit7','transient','unlinked-duplicates',
                 'escaped','echild','unobserved-cache','deadline',
                 'persistent-topology','journal-failure')
NOT_QUALIFIED = dict(full_Native_build_qualified=False,
    actual_AB_material_context_qualified=False,complete_context_aggregation_qualified=False,
    actual_native_transport_executed=False,full_reference_qualified=False,
    scientific_qualification_created=False,physical_neutron_balance_qualified=False,
    AAA_accuracy_qualified=False,ABA_admitted=False,ABA_started=False,native_RSS_qualified=False,
    scientific_accuracy_qualified=False,native_transport_executed=False,
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


CONTROL_ORDER_GROUPED = (
    'positive-mini-libraries',
    'preexisting-original-object','preexisting-default-pp-object','preexisting-pp-source',
    'case-basename-collision','mixed-flags','mixed-cwd','mixed-component',
    'unmet-dependency-preflight','unmet-dependency-planner','source-pin-mutation',
    'pp-default-original-collision',
    'closed-driver-missing-object','closed-driver-extra-object','closed-driver-source-mutation',
    'second-input-syntax-error')
GENERATOR_SHA = '243823cbddbffbf9a3ecd234cf4d676d3600fb7c3ad7d66aad3ccbb7b49363ff'
GANLIB_CONTROL_MODULE = 'axmat_grouped_control_ganlib_mod_20261011'


def f77_fixture(name,value):
    return ('      SUBROUTINE '+name+'(V)\n      INTEGER V\n      V='+str(value)+'\n      END\n').encode('ascii')


def successful_inputs():
    ganlib = {('c'+format(i,'02d')+'.c'):('int axmat_grouped_c'+str(i)+'(void) { return '+str(i)+'; }\n').encode('ascii') for i in range(17)}
    ganlib.update({
        'aa_provider.f90': ('module '+GANLIB_CONTROL_MODULE+'\ncontains\n  subroutine grouped_ganlib_value(v)\n    integer, intent(out) :: v\n    v = 7\n  end subroutine grouped_ganlib_value\nend module '+GANLIB_CONTROL_MODULE+'\n').encode('ascii'),
        'ab_user.f90': ('subroutine grouped_ganlib_user(v)\n  use '+GANLIB_CONTROL_MODULE+'\n  integer, intent(out) :: v\n  call grouped_ganlib_value(v)\nend subroutine grouped_ganlib_user\n').encode('ascii'),
        'zz_free.F90': b'#define GROUPED_FREE_VALUE 17\nsubroutine grouped_ganlib_pp_free(v)\n  integer, intent(out) :: v\n  v = GROUPED_FREE_VALUE\nend subroutine grouped_ganlib_pp_free\n',
        'fixed_a.f': f77_fixture('GROUPED_GANLIB_FIXED_A',3),
        'fixed_b.f': f77_fixture('GROUPED_GANLIB_FIXED_B',5),
        'zz_fixed.F': b'#define GROUPED_FIXED_VALUE 13\n      SUBROUTINE GROUPED_GANLIB_PP_FIXED(V)\n      INTEGER V\n      V=GROUPED_FIXED_VALUE\n      END\n'})
    utilib = {
        'c_a.c': b'int grouped_utilib_c_a(void) { return 19; }\n',
        'c_b.c': b'int grouped_utilib_c_b(void) { return 23; }\n',
        'aa_provider.f90': b'module axmat_grouped_control_utilib_mod_20261011\ncontains\n  subroutine grouped_utilib_value(v)\n    integer, intent(out) :: v\n    v = 29\n  end subroutine grouped_utilib_value\nend module axmat_grouped_control_utilib_mod_20261011\n',
        'ab_user.f90': b'subroutine grouped_utilib_user(v)\n  use axmat_grouped_control_utilib_mod_20261011\n  integer, intent(out) :: v\n  call grouped_utilib_value(v)\nend subroutine grouped_utilib_user\n',
        'fixed_a.f': f77_fixture('GROUPED_UTILIB_FIXED_A',31),
        'fixed_b.f': f77_fixture('GROUPED_UTILIB_FIXED_B',37)}
    trivac = {
        'trivac_a.f90': ('subroutine grouped_trivac_a(v)\n  use '+GANLIB_CONTROL_MODULE+'\n  integer, intent(out) :: v\n  call grouped_ganlib_value(v)\nend subroutine grouped_trivac_a\n').encode('ascii'),
        'trivac_b.f90': b'subroutine grouped_trivac_b(v)\n  integer, intent(out) :: v\n  v = 41\nend subroutine grouped_trivac_b\n',
        'fixed_a.f': f77_fixture('GROUPED_TRIVAC_FIXED_A',43),
        'fixed_b.f': f77_fixture('GROUPED_TRIVAC_FIXED_B',47)}
    dragon = {
        'c_a.c': b'int grouped_dragon_c_a(void) { return 53; }\n',
        'c_b.c': b'int grouped_dragon_c_b(void) { return 59; }\n',
        'DRAGON.f90': ('program grouped_tiny_dragon\n  use '+GANLIB_CONTROL_MODULE+'\n  integer :: v\n  call grouped_ganlib_value(v)\nend program grouped_tiny_dragon\n').encode('ascii'),
        'dragon_user.f90': ('subroutine grouped_dragon_user(v)\n  use '+GANLIB_CONTROL_MODULE+'\n  integer, intent(out) :: v\n  call grouped_ganlib_value(v)\nend subroutine grouped_dragon_user\n').encode('ascii'),
        'zz_free.F90': b'#define GROUPED_DRAGON_VALUE 61\nsubroutine grouped_dragon_pp_free(v)\n  integer, intent(out) :: v\n  v = GROUPED_DRAGON_VALUE\nend subroutine grouped_dragon_pp_free\n',
        'fixed_a.f': f77_fixture('GROUPED_DRAGON_FIXED_A',67),
        'fixed_b.f': f77_fixture('GROUPED_DRAGON_FIXED_B',71),
        'zz_fixed.F': b'#define GROUPED_DRAGON_FIXED_VALUE 73\n      SUBROUTINE GROUPED_DRAGON_PP_FIXED(V)\n      INTEGER V\n      V=GROUPED_DRAGON_FIXED_VALUE\n      END\n'}
    return dict(Ganlib=ganlib,Utilib=utilib,Trivac=trivac,Dragon=dragon)


def refusal_inputs(case):
    if case in ('preexisting-default-pp-object','preexisting-pp-source','pp-default-original-collision'):
        result = {'one.F': b'#define GROUPED_VALUE 7\n      SUBROUTINE GROUPED_REFUSAL(V)\n      INTEGER V\n      V=GROUPED_VALUE\n      END\n'}
        if case == 'pp-default-original-collision':result['one.pp.f'] = f77_fixture('GROUPED_REFUSAL_COLLISION',11)
        return result
    if case == 'case-basename-collision':
        return {'case.c': b'int grouped_case(void) { return 7; }\n',
                'CASE.f90': b'subroutine grouped_case_f(v)\n  integer :: v\n  v = 11\nend subroutine grouped_case_f\n'}
    if case.startswith('unmet-dependency'):
        return {'aa_provider.f90': b'module axmat_grouped_missing_provider_mod_20261011\n  integer, parameter :: grouped_missing_value = 7\nend module axmat_grouped_missing_provider_mod_20261011\n',
                'ab_user.f90': b'subroutine grouped_missing_user(v)\n  use axmat_grouped_missing_provider_mod_20261011\n  integer :: v\n  v = grouped_missing_value\nend subroutine grouped_missing_user\n'}
    result = {'first.c': b'int grouped_private_first(void) { return 7; }\n',
              'second.c': b'int grouped_private_second(void) { return 11; }\n'}
    if case == 'second-input-syntax-error':result['second.c'] = b'int grouped_private_second(void) { this is invalid C; }\n'
    return result


def grouped_input_contract():
    rows = {}
    for component,files in successful_inputs().items():
        for name,raw in files.items():
            rows['positive-mini-libraries/'+component+'/src/'+name] = dict(size_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    for case in CONTROL_ORDER_GROUPED[1:]:
        for name,raw in refusal_inputs(case).items():
            rows[case+'/Ganlib/src/'+name] = dict(size_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    return rows


def grouped_control_manifest():
    return dict(order=list(CONTROL_ORDER_GROUPED),
        positive_expected_groups=dict(Ganlib=[16,1,2,1,2,1],Utilib=[2,2,2],Trivac=[2,2],Dragon=[2,2,1,2,1]),
        positive_expected_cpp_counts=dict(Ganlib=2,Utilib=0,Trivac=0,Dragon=2),
        positive_component_order=['Ganlib','Utilib','Trivac','Dragon'],
        archive_object_order='c_sorted_then_original_f90_dependency_order_then_f_sorted_then_F_sorted',
        final_link_input_order=['DRAGON.o','libDragon.a','libTrivac.a','libUtilib.a','libGanlib.a'],
        executable_run=False,all_cases_share_one_total_stage_seconds=600,
        no_process_refusals=list(CONTROL_ORDER_GROUPED[1:12]),
        actual_closed_driver_refusals=list(CONTROL_ORDER_GROUPED[12:15]),
        genuine_nonzero_driver_case='second-input-syntax-error',
        source_count=len(grouped_input_contract()),all_inputs_are_private_controls=True,
        original1337_native_units_executed=False,compiler_driver_descendant_RSS_qualified=False,
        arbitrary_post_driver_stale_replacement_before_first_output_pin_detected=False)


def write_fixture(runtime,folder,files,budget):
    folder.mkdir(parents=True)
    rows = {}
    for name,raw in files.items():
        budget();path = folder/name
        require(path.parent == folder and not os.path.lexists(path),'fresh private ordinary fixture')
        with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        rows[str(path)] = runtime.fullpin(path,budget)
    return rows


def original_order_and_dependencies(generator,folder):
    c = sorted(folder.glob('*.c'))
    f90 = [*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))]
    lower = sorted(folder.glob('*.f'));upper = sorted(folder.glob('*.F'))
    ordered90 = [Path(v) for v in generator.build_dependency_order([str(p) for p in f90])]
    pending = [*c,*ordered90,*lower,*upper]
    units = generator.build_units([str(p) for p in [*f90,*lower,*upper]])
    return pending,{Path(u.name):u for u in units},{u.module:Path(u.name) for u in units if u.module}


def current_private_files(runtime,folder,budget):
    return [runtime.fullpin(p,budget) for p in sorted(folder.iterdir()) if p.is_file()]


def run_grouped_tiny_controls(runtime,batch,generator,runner,resources,monitor,observer,
                              host,tools,probe_deadline,budget,phase,windows,timings,inputs,outputs,cases):
    root = host/'GROUPED_TINY_CONTROLS';root.mkdir()
    positive = root/'positive-mini-libraries';archives = {};positive_rows = [];positive_components = []
    manifest = grouped_control_manifest()
    for component,files in successful_inputs().items():
        folder = positive/component/'src';recipe = runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]
        expected = write_fixture(runtime,folder,files,budget);inputs.extend(expected.values())
        pending,by_source,module_source = original_order_and_dependencies(generator,folder)
        order = list(pending);objects_order = [p.with_suffix('.o') for p in order]
        completed = set();groups = [];rows = [];commands = [];ordinal = 0
        include_pins = []
        if component in ('Trivac','Dragon'):
            imported = positive/'Ganlib/lib/Darwin_arm64/modules'/(GANLIB_CONTROL_MODULE+'.mod')
            require(not os.path.lexists(folder/imported.name),'actual original relative INCLUDE; no local module substitute')
            include_pins.append(runtime.fullpin(imported,budget))
        stage_started = time.monotonic();phase[0] = 'positive_'+component
        with batch.DirectDriverLibraryStage(runtime,runner,resources,folder,component,
                stage_started,probe_deadline,budget) as active_stage:
            while pending:
                ordinal += 1;first = len(windows);entered = time.monotonic()
                group,unit_rows,group_commands,summary = batch.compile_original_source_group(
                    runtime,positive,folder,component,recipe,tools,pending,completed,
                    by_source,module_source,objects_order,expected,active_stage,budget,ordinal)
                finished = time.monotonic()
                timings.append(dict(case='positive-mini-libraries',component=component,
                    group_ordinal=ordinal,direct_public_helper_seconds=finished-entered,
                    actual_group_driver=summary['actual_group_compile'],actual_group_size=len(group),
                    accepted_fresh_windows_count=len(windows)-first,
                    accepted_fresh_windows_seconds=sum(w['accepted_fresh_window_seconds'] for w in windows[first:]),
                    native_driver_RSS_qualified=False,compiler_descendant_RSS_scope_not_certified=True))
                for plan in group:
                    path=Path(plan['original_source']);pending.remove(path);completed.add(path)
                rows.extend(unit_rows);commands.extend(group_commands);groups.append(summary)
            require([g['group_size'] for g in groups] == manifest['positive_expected_groups'][component]
                    and sum(row['preprocessor_output_pin'] is not None for row in rows)
                        == manifest['positive_expected_cpp_counts'][component],
                    'true16+1 boundary, f90 provider order, F77 pair and cpp singleton positions')
            if component == 'Ganlib':
                provider = str(folder/'aa_provider.f90');user = str(folder/'ab_user.f90')
                require(any(g['original_selected_Source_order'] == [provider,user] for g in groups),
                        'same actual argv consumes original module provider then user')
            require({r['new_object_pin']['path'] for r in rows} == set(map(str,objects_order)),
                    'every tiny original object mapped exactly once')
            archive = folder/('lib'+component+'.a')
            argv = [tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)]
            archived = active_stage.execute_driver(folder,'archive_'+component,argv,probe_deadline,budget)
            ap = runtime.fullpin(archive,budget)
            for row in rows:runtime.recheck(row['new_object_pin'],budget)
            library_dir = positive/component/'lib/Darwin_arm64';library_dir.mkdir(parents=True)
            target = library_dir/archive.name
            require(not os.path.lexists(target),'original library-copy namespace fresh')
            shutil.copy2(archive,target);target_pin = runtime.fullpin(target,budget)
            require(target_pin['sha256'] == ap['sha256'] and target_pin['size_bytes'] == ap['size_bytes'],
                    'complete original fresh archive copy')
            module_copy = []
            if recipe['module_copy']:
                module_dir = positive/recipe['lib_module'];module_dir.mkdir(parents=True)
                generated = sorted(folder.glob('*.mod'))
                require(component != 'Utilib' or bool(generated),'original Utilib module-copy actual output required')
                for module in generated:
                    copied = module_dir/module.name
                    require(not os.path.lexists(copied),'fresh original module-copy target')
                    generated_pin=runtime.fullpin(module,budget);shutil.copy2(module,copied)
                    copy_pin=runtime.fullpin(copied,budget)
                    require(copy_pin['sha256'] == generated_pin['sha256']
                            and copy_pin['size_bytes'] == generated_pin['size_bytes'],
                            'actual generated module copied by original recipe')
                    module_copy.append(dict(generated_pin=generated_pin,copied_pin=copy_pin))
                    outputs.append(dict(role='module_copy',new_output_pin=copy_pin))
            for expected_pin in expected.values():runtime.recheck(expected_pin,budget)
            for expected_pin in include_pins:runtime.recheck(expected_pin,budget)
            archives[component]=target_pin;positive_rows.extend(rows)
            outputs.extend(dict(role='positive_object',new_output_pin=row['new_object_pin']) for row in rows)
            outputs.extend([dict(role='positive_archive',new_output_pin=ap),dict(role='positive_library_copy',new_output_pin=target_pin)])
            positive_components.append(dict(component=component,exact_original_recipe=recipe,
                original_selected_source_order=list(map(str,order)),actual_groups=groups,
                actual_commands=commands,all_object_rows=rows,actual_archive=archived,
                archive_object_order=list(map(str,objects_order)),new_archive_pin=ap,
                new_library_copy_pin=target_pin,actual_module_copy_pins=module_copy,
                original_relative_INCLUDE_module_input_pins=include_pins))
        require(active_stage.record['status'] == 'PASS','positive genuine original library stage PASS')
        positive_components[-1]['actual_stage_record']=active_stage.record
    folder = positive/'Dragon/src';recipe=runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Dragon']
    link_inputs = [runtime.fullpin(folder/'DRAGON.o',budget),*[archives[k] for k in ('Dragon','Trivac','Utilib','Ganlib')]]
    exe = folder/'Dragon';require(not os.path.lexists(exe),'fresh tiny final link output')
    argv=[tools[recipe['F90']]['path'],*recipe['opt'],*recipe['COMP'],*[p['path'] for p in link_inputs],*recipe['LFLAGS'],'-o',str(exe)]
    phase[0]='positive_final_link'
    with batch.DirectDriverLibraryStage(runtime,runner,resources,folder,'Dragon_link',
            time.monotonic(),probe_deadline,budget) as link_stage:
        linked=link_stage.execute_driver(folder,'Dragon_link',argv,probe_deadline,budget)
        exe_pin=runtime.fullpin(exe,budget)
        for expected_pin in link_inputs:runtime.recheck(expected_pin,budget)
        for row in positive_rows:runtime.recheck(row['new_object_pin'],budget)
    outputs.append(dict(role='tiny_linked_executable_never_run',new_output_pin=exe_pin))
    cases.append(dict(case_id='positive-mini-libraries',expected_outcome_observed=True,
        status='PRIVATE_TINY_GROUPED_DRIVERS_ARCHIVE_LINK_ONLY_PASS',
        actual_components=positive_components,actual_final_link=linked,
        actual_final_link_input_pins=link_inputs,actual_linked_executable_pin=exe_pin,
        actual_final_link_stage=link_stage.record,linked_executable_run=False,
        original1337_native_sources_compiled=False,full_Native_build_qualified=False))

    for case in CONTROL_ORDER_GROUPED[1:12]:
        phase[0]=case;native=root/case;folder=native/'Ganlib/src'
        expected=write_fixture(runtime,folder,refusal_inputs(case),budget)
        pending,by_source,module_source=original_order_and_dependencies(generator,folder)
        recipe=runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Ganlib']
        objects=[p.with_suffix('.o') for p in pending];completed=set()
        group=[batch.original_compile_unit_plan(folder,'Ganlib',recipe,tools,p) for p in pending]
        mutation=None
        if case == 'preexisting-original-object':
            path=folder/'first.o';path.write_bytes(b'private stale object refusal fixture\n');mutation=runtime.fullpin(path,budget)
        elif case == 'preexisting-default-pp-object':
            path=folder/'one.pp.o';path.write_bytes(b'private stale pp default refusal fixture\n');mutation=runtime.fullpin(path,budget)
        elif case == 'preexisting-pp-source':
            path=folder/'one.pp.f';path.write_bytes(b'private stale pp Source refusal fixture\n');mutation=runtime.fullpin(path,budget)
        elif case == 'mixed-flags':group[1]['compiler_prefix']=[*group[1]['compiler_prefix'],'-O2']
        elif case == 'mixed-cwd':group[1]['cwd']=str(native/'wrong_cwd')
        elif case == 'mixed-component':group[1]['component']='Utilib'
        elif case.startswith('unmet-dependency'):
            user=folder/'ab_user.f90';group=[batch.original_compile_unit_plan(folder,'Ganlib',recipe,tools,user)]
            pending=[user]
        elif case == 'source-pin-mutation':
            path=folder/'first.c'
            with path.open('ab') as stream:stream.write(b'/* intentional private pre-driver Source mutation */\n');stream.flush();os.fsync(stream.fileno())
            mutation=runtime.fullpin(path,budget)
        inputs.extend(expected.values())
        before_files=current_private_files(runtime,folder,budget);owners_before=set(observer.owners)
        records_before=len(runner.records);error=None
        try:
            if case == 'unmet-dependency-planner':
                batch.select_original_compile_group(folder,'Ganlib',recipe,tools,pending,completed,by_source,module_source)
            else:
                batch.compile_group_preflight(runtime,folder,'Ganlib',recipe,tools,group,
                    completed,by_source,module_source,objects,expected,budget)
        except ValueError as failure:error=repr(failure)
        require(error is not None and set(observer.owners) == owners_before
                and len(runner.records) == records_before
                and current_private_files(runtime,folder,budget) == before_files,
                'actual public admission refusal without process, stage, or post-refusal mutation')
        cases.append(dict(case_id=case,expected_outcome_observed=True,status='EXPECTED_PUBLIC_NO_PROCESS_REFUSAL',
            actual_error=error,actual_expected_Source_pins=list(expected.values()),
            actual_private_fixture_mutation_pin=mutation,actual_pre_refusal_files=before_files,
            actual_post_refusal_files=before_files,actual_proposed_group=group,
            owner_PID_set_before=sorted(owners_before),owner_PID_set_after=sorted(observer.owners),
            actual_new_process_count=0,no_mocked_driver_or_OS=True))

    for case in CONTROL_ORDER_GROUPED[12:15]:
        phase[0]=case;native=root/case;folder=native/'Ganlib/src'
        expected=write_fixture(runtime,folder,refusal_inputs(case),budget);inputs.extend(expected.values())
        pending,by_source,module_source=original_order_and_dependencies(generator,folder)
        recipe=runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Ganlib'];objects=[p.with_suffix('.o') for p in pending]
        owners_before=set(observer.owners);error=None;closure_evidence=None;mutation=None
        try:
            with batch.DirectDriverLibraryStage(runtime,runner,resources,folder,'Ganlib',
                    time.monotonic(),probe_deadline,budget) as active_stage:
                group,rows,commands,summary=batch.compile_original_source_group(runtime,native,folder,'Ganlib',recipe,
                    tools,pending,set(),by_source,module_source,objects,expected,active_stage,budget,1)
                records=[dict(plan=plan,original_source_pin=row['original_source_pin'],
                    local_module_provider_sources=row['local_module_provider_sources'],
                    preprocessor_output_pin=row['preprocessor_output_pin'],
                    actual_compiler_input_pin=row['actual_compiler_input_pin']) for plan,row in zip(group,rows)]
                retained_dir=native/'retained_actual_genuine_objects_before_mutation';retained_dir.mkdir()
                retained_objects=[]
                for row in rows:
                    actual=Path(row['new_object_pin']['path']);backup=retained_dir/actual.name
                    runtime.recheck(row['new_object_pin'],budget)
                    shutil.copy2(actual,backup);backup_pin=runtime.fullpin(backup,budget)
                    require(backup_pin['sha256'] == row['new_object_pin']['sha256']
                            and backup_pin['size_bytes'] == row['new_object_pin']['size_bytes'],
                            'complete genuine produced object bytes retained before destructive private control')
                    retained_objects.append(dict(original_genuine_object_pin=row['new_object_pin'],
                        complete_retained_object_pin=backup_pin))
                retained_source=[]
                for original_pin in expected.values():
                    actual=Path(original_pin['path']);backup=retained_dir/actual.name
                    runtime.recheck(original_pin,budget);shutil.copy2(actual,backup)
                    backup_pin=runtime.fullpin(backup,budget)
                    require(backup_pin['sha256'] == original_pin['sha256']
                            and backup_pin['size_bytes'] == original_pin['size_bytes'],
                            'complete real original private Source bytes retained before mutation')
                    retained_source.append(dict(original_Source_pin=original_pin,complete_retained_Source_pin=backup_pin))
                closure_evidence=dict(actual_real_group_summary=summary,actual_real_object_rows_before_mutation=rows,
                    actual_public_closure_records=records,actual_before_objects=[],
                    actual_closed_driver=summary['actual_group_compile'],
                    actual_pre_mutation_files=current_private_files(runtime,folder,budget),
                    complete_retained_genuine_objects_before_mutation=retained_objects,
                    complete_retained_real_private_Source_before_mutation=retained_source)
                if case == 'closed-driver-missing-object':
                    removed=runtime.fullpin(folder/'first.o',budget);(folder/'first.o').unlink()
                    mutation=dict(action='delete_actual_genuine_object',actual_original_object_pin=removed,
                        current_missing_path=str(folder/'first.o'))
                elif case == 'closed-driver-extra-object':
                    original=runtime.fullpin(folder/'first.o',budget);extra=folder/'extra.o'
                    shutil.copy2(folder/'first.o',extra);extra_pin=runtime.fullpin(extra,budget)
                    require(original['sha256'] == extra_pin['sha256'] and original['size_bytes'] == extra_pin['size_bytes'],
                            'extra private object contains real genuine-produced compiler bytes')
                    mutation=dict(action='extra_copy_of_actual_genuine_object',actual_original_object_pin=original,
                        actual_extra_object_pin=extra_pin)
                else:
                    changed=folder/'first.c'
                    with changed.open('ab') as stream:stream.write(b'/* intentional private post-driver Source mutation */\n');stream.flush();os.fsync(stream.fileno())
                    mutation=dict(action='mutate_actual_genuine_compiler_Source_after_wait',
                        actual_original_Source_pin=expected[str(changed)],actual_mutated_Source_pin=runtime.fullpin(changed,budget))
                closure_evidence['actual_post_mutation_files']=current_private_files(runtime,folder,budget)
                batch.compile_group_output_closure(runtime,native,folder,'Ganlib',recipe,tools,group,records,set(),
                    summary['actual_group_compile'],active_stage,budget,1)
        except ValueError as failure:error=repr(failure)
        require(error is not None and closure_evidence is not None
                and active_stage.record['status'] == 'FAILED'
                and set(observer.owners)-owners_before == {closure_evidence['actual_closed_driver']['actual_child_PID'],
                    closure_evidence['actual_closed_driver']['actual_original_watchdog_PID']}
                and not any(folder.glob('*.a')),
                'public closure actually refuses genuine closed driver output; stage FAILED, no archive/retry')
        cases.append(dict(case_id=case,expected_outcome_observed=True,status='EXPECTED_GENUINE_POST_DRIVER_CLOSURE_REFUSAL',
            actual_error=error,actual_stage_record=active_stage.record,actual_closure_evidence=closure_evidence,
            actual_private_mutation=mutation,actual_no_new_driver_during_closure=True,
            actual_partial_files=current_private_files(runtime,folder,budget),actual_retry_count=0,
            arbitrary_post_driver_same_name_stale_substitution_detection_claimed=False))

    case='second-input-syntax-error';phase[0]=case;native=root/case;folder=native/'Ganlib/src'
    expected=write_fixture(runtime,folder,refusal_inputs(case),budget);inputs.extend(expected.values())
    pending,by_source,module_source=original_order_and_dependencies(generator,folder)
    recipe=runtime.ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Ganlib'];objects=[p.with_suffix('.o') for p in pending]
    owners_before=set(observer.owners);error=None
    try:
        with batch.DirectDriverLibraryStage(runtime,runner,resources,folder,'Ganlib',
                time.monotonic(),probe_deadline,budget) as active_stage:
            batch.compile_original_source_group(runtime,native,folder,'Ganlib',recipe,tools,pending,set(),
                by_source,module_source,objects,expected,active_stage,budget,1)
    except RuntimeError as failure:error=repr(failure)
    fresh=[observer.owners[p] for p in set(observer.owners)-owners_before]
    business=[row for row in fresh if row['role'] == 'business'];watchdogs=[row for row in fresh if row['role'] == 'watchdog']
    require(error is not None and active_stage.record['status'] == 'FAILED'
            and len(fresh) == 2 and len(business) == 1 and len(watchdogs) == 1,
            'one true nonzero original grouped compiler and its original watchdog; FAILED stage')
    proof=business[0]['closed_wait'];expected_argv=[*batch.original_compile_unit_plan(folder,'Ganlib',recipe,tools,pending[0])['compiler_prefix'],*map(str,pending)]
    require(proof is not None and proof['closed_proven'] is True
            and type(proof['actual_exit_code']) is int and proof['actual_exit_code'] != 0
            and proof['actual_waitpid_pid'] == business[0]['pid']
            and business[0]['args'] == expected_argv
            and watchdogs[0]['closed_wait'] is not None
            and watchdogs[0]['closed_wait']['closed_proven'] is True
            and (folder/'first.o').is_file() and not os.path.lexists(folder/'second.o')
            and not any(folder.glob('*.a')),
            'actual second-input syntax refusal retains exact argv/wait and true first partial object, no archive/retry')
    for expected_pin in expected.values():runtime.recheck(expected_pin,budget)
    cases.append(dict(case_id=case,expected_outcome_observed=True,status='EXPECTED_GENUINE_NONZERO_GROUP_FAILED_WITH_PARTIAL_OUTPUT',
        actual_error=error,actual_stage_record=active_stage.record,actual_business_PID=business[0]['pid'],
        actual_original_business_closed_wait=dict(proof),actual_original_watchdog_PID=watchdogs[0]['pid'],
        actual_original_watchdog_closed_wait=dict(watchdogs[0]['closed_wait']),
        actual_argv=expected_argv,actual_partial_files=current_private_files(runtime,folder,budget),
        actual_first_partial_object_pin=runtime.fullpin(folder/'first.o',budget),
        actual_second_object_absent=True,actual_archive_absent=True,actual_retry_count=0))
    require([row['case_id'] for row in cases] == list(CONTROL_ORDER_GROUPED)
            and all(row['expected_outcome_observed'] is True for row in cases),
            'all16 original expected genuine/no-process control outcomes, no filtered subset')
    return manifest


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


def admit_original_contract_and_actual_ten_controls(b,binding_pin,budget,additional_Source_pins):
    """Public complete inherited admission for new Root-bound entries.

    Full native callers independently admit their own entry, controls, binding,
    D/E and material coverage; this function does not grant execution or physics
    qualification. It rechecks the entire original external contract and all
    forty actual monitor-control facts/terminal/current-closeout pins.
    """
    require(type(additional_Source_pins) in (list,tuple) and bool(additional_Source_pins),
            'caller supplies its exact additional protected Source fullpins')
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
    protected = [binding_pin,*additional_Source_pins,b['direct_driver_batch_Source_pin'],
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
            'original genuine support and exact frozen shared-closure V2 Source')
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
    return dict(fresh=fresh,author=author,cases=cases,protected=protected)


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
                'fixed grouped-controls600 includes fixtures, all16 cases and final report')
    binding_pin = pin(args.binding)
    require(binding_pin['sha256'] == args.binding_sha256,'Root-bound exact new binding SHA')
    b = metadata(binding_pin)
    require(b['schema'] == 'ROOT_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_SOURCE_BINDING_V2'
            and b['source_only'] is True and b['Root_only_actual_execution'] is True
            and b['execution_scope'] == SCOPE and b['probe_id'] == PROBE
            and b['policy'] == POLICY and b['original_caps'] == CAPS
            and all(type(value) is int for value in b['original_caps'].values())
            and b['actual_execution'] is None and b['old_controls_qualification_inherited'] is False
            and b['control_execution_order'] == list(CONTROL_ORDER_GROUPED)
            and b['small_input_contract'] == grouped_input_contract()
            and b['planned_control_manifest'] == grouped_control_manifest(),
            'Source-bound exact sixteen grouped controls only, unchanged typed nine caps')
    require(pin(Path(__file__).resolve()) == b['probe_entry_Source_pin'],
            'this exact Source-only entry; no unreviewed replacement')
    admitted = admit_original_contract_and_actual_ten_controls(b,binding_pin,budget,
        [b['probe_entry_Source_pin'],b['dependency_generator_Source_pin']])
    fresh,author,cases,protected = (admitted[key] for key in ('fresh','author','cases','protected'))
    review_pin = pin(args.independent_prelaunch_review)
    review = metadata(review_pin)
    require(review['schema'] == 'INDEPENDENT_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_SOURCE_REVIEW_V2'
            and review['source_only'] is True and review['all_checks_passed'] is True
            and review['blockers'] == [] and review['new_Source_binding_pin'] == binding_pin
            and review['probe_entry_Source_pin'] == b['probe_entry_Source_pin']
            and review['adapter_Source_pin'] == b['adapter_Source_pin']
            and review['direct_driver_batch_Source_pin'] == b['direct_driver_batch_Source_pin']
            and review['fresh_controls_saved_RESULT_pin'] == b['fresh_controls_saved_RESULT_pin']
            and review['fresh_controls_independent_saved_review_pin'] == b['fresh_controls_independent_saved_review_pin']
            and review['dependency_generator_Source_pin'] == b['dependency_generator_Source_pin']
            and review['planned_control_manifest'] == b['planned_control_manifest'],
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
    batch = load_source(b['direct_driver_batch_Source_pin'],'grouped_tiny_shared_V2_batch_Source')
    native_index = metadata(author['native_Source_index'])
    generator_rows = [r for r in native_index['members'] if r['relative_path'] == 'script/make_depend.py']
    require(len(generator_rows) == 1
            and b['dependency_generator_Source_pin']['sha256'] == GENERATOR_SHA
            and b['dependency_generator_Source_pin']['size_bytes'] == 8473
            and generator_rows[0]['full_original_Source_pin']['sha256'] == GENERATOR_SHA
            and generator_rows[0]['full_original_Source_pin']['size_bytes'] == 8473,
            'genuine complete original frozen dependency generator, no synthetic units')
    generator = load_source(b['dependency_generator_Source_pin'],'grouped_tiny_original_dependency_generator')
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
    require(b['planned_control_manifest'] == grouped_control_manifest(),
            'exact fixed tiny public-helper recipe/negative-control manifest')
    host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir()
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
    inputs = [];outputs = [];grouped_cases = [];actual_error = None
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
        runner = full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'GROUPED_TINY_CONTROLS',resources)
        monitor.install_bounded_wrappers(runner)
        observer = runtime.attach_exact_owner_observer(runner,resources,monitor,
            b['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,
            b['owner_helper_Source_pin'],support,control_mode=True)
        require(observer.control_after_original_start is None
                and resources._actual_control_barrier is None,'no controls transition or mocked OS outcome')
        resources._actual_control_scan_sink = scan_sink
        stage_started = time.monotonic();probe_deadline = stage_started+600
        monitor.stage_deadline = probe_deadline
        actual_grouped_manifest = run_grouped_tiny_controls(runtime,batch,generator,runner,resources,
            monitor,observer,host,b['tool_pins'],probe_deadline,budget,phase,windows,timings,
            inputs,outputs,grouped_cases)
        require(len(grouped_cases) == 16 and len(runner.records) == 9
                and [r['status'] for r in runner.records] == ['PASS']*5+['FAILED']*4
                and all(o['closed_wait'] is not None and o['closed_wait']['closed_proven'] is True
                        for o in observer.owners.values()),
                'five actual positive stages plus four retained expected FAILED stages and real owner waits')
        phase[0] = 'final_resources';after = resources.check();budget()
        require([r['status'] for r in runner.records] == ['PASS']*5+['FAILED']*4
                and not observer.unknown and not monitor.recording_errors and not monitor.unpersisted,
                'expected actual FAILED stages retained; no unknown/persistence failure hidden')
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
        facts = dict(schema='ACTUAL_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS_V2',
            status='SIXTEEN_GENUINE_GROUPED_TINY_OUTCOMES_ONLY_ROOT_TERMINAL_CURRENT_CLOSEOUT_AND_REVIEW_REQUIRED',
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
            actual_small_input_pins_include_historical_intentional_private_mutations=True,
            actual_driver_timings=timings,actual_accepted_fresh_windows=windows,
            actual_grouped_control_manifest=actual_grouped_manifest,
            actual_all_sixteen_grouped_controls=grouped_cases,
            original_dependency_generator_Source_pin=b['dependency_generator_Source_pin'],
            arbitrary_post_driver_stale_replacement_before_first_output_pin_detected=False,
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
        result = host/'ACTUAL_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS.json'
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
        monitor.write_failure_result(host/'FAILED_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS.json',dict(
            schema='FAILED_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS_V2',status='FAILED_NO_RETRY_NO_QUALIFICATION',
            new_Source_binding_pin=binding_pin,actual_host_PID=os.getpid(),actual_error=actual_error,
            actual_stage_records=[] if runner is None else runner.records,
            actual_owner_state=None if observer is None else observer.summary(),
            actual_monitor_evidence=summary,actual_completed_driver_timings=timings,
            actual_completed_grouped_controls=grouped_cases,
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

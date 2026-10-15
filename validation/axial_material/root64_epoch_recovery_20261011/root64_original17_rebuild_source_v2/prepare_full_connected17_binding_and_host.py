from pathlib import Path
import ast
import hashlib
import json
import time

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE=Path(__file__).resolve().parent
OUT=ART/'axial-material-new-ROOT64-full-connected17-controls-v2-20261012'
OLD_BIND=ART/'axial-material-ROOT64-connected-typed-fixture-original-guard-20261011/Root_fixed_source_and_exact_command_binding.json'
OLD_HOST=REC/'run_current_ROOT64_native_core_controls.py'
SOURCE=PACKAGE/'test_ROOT64_full_connected17_v2.f90'
COMPILER=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')


def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path):
    p=Path(path);before=identity(p.stat());data=p.read_bytes();after=identity(p.stat())
    assert before==after and len(data)==before[4]
    return dict(path=str(p),size_bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),identity=before)


def put(name,data):
    p=PACKAGE/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb')as f:f.write(data if isinstance(data,bytes)else data.encode())
    return pin(p)


start=time.monotonic()
old=json.loads(OLD_BIND.read_bytes())
names=[c[-1]for c in old['control_commands']]
assert names==['positive','global_wrong_scope','missing_producer_seal',
    'root_flux32_disguised','wrong_root_mirror','missing_global64','bad_seed_epoch',
    'fabricated_projected','uncommitted_source','wrong_source_epoch','wrong_source_dimensions',
    'mutated_macro','mutated_track','mutated_system','different_route','qfiss32_disguised',
    'coherent_source_tamper']
source_pin=pin(SOURCE)
assert source_pin['sha256']=='28e229ff6d1eb3d9f0b4d3ee0c1e96b207d5b1d417876f2f2653947bade45273'
flags=old['compile_commands'][0][1:10]
assert flags==['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g',
               '-fPIC','-frecord-marker=4','-ffixed-line-length-none']
build=OUT/'build';exe=build/'full_connected17_unqualified'
qbuild=ART/'axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012/build'
pbuild=ART/'axial-material-new-bootstrap-global-projection-v2-compile-only-20261012/build'
nbase=ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build'
includes=[pbuild,qbuild,nbase,ART/'axial-material-r64-system-normalization-20261003/build',
          ROOT/'lib/Darwin_arm64/modules',ROOT/'Ganlib/lib/Darwin_arm64/modules']
objects=[pbuild/'SPOR64_BOOT_PUBLISH64.o',pbuild/'SPOR64_BOOT_PROJECT64.o',
         qbuild/'SPOR64_BOOTQ64.o',qbuild/'SPOR64_BOOT_CANONICAL64.o',qbuild/'SPOR64_BOOT_CONTEXT64.o',
         pbuild/'SPOR64_B2H.o',nbase/'SPOR64_BOOT64.o',nbase/'SPOR64_RCONTRACT.o',nbase/'SPOR64_VERIFY.o']
libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',
           ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
compile_command=[str(COMPILER),*flags,*['-I'+str(d)for d in includes],'-J'+str(build),
                 '-c',str(SOURCE),'-o',str(build/'test_ROOT64_full_connected17_v2.o')]
link_command=[str(COMPILER),*old['compile_commands'][-1][1:3],
              str(build/'test_ROOT64_full_connected17_v2.o'),*[str(p)for p in objects+libraries],'-o',str(exe)]
run_commands=[[str(exe),n]for n in names[:-1]]+[
    [str(exe),'coherent_source_tamper','prepare'],[str(exe),'coherent_source_tamper','rewrite']]
q_binding=REC/'bootstrap_qfiss_source_v2/SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json'
q=json.loads(q_binding.read_bytes())
paths={Path(p['path'])for p in q['source_pins']+q['actual_dependency_pins']}
paths.update(objects+libraries+[SOURCE,COMPILER,OLD_BIND,OLD_HOST,q_binding,
    REC/'bootstrap_global_projection_publish_source_v2/SPOR64_BOOT_PUBLISH64.f90',
    REC/'bootstrap_global_projection_publish_source_v2/SPOR64_BOOT_PROJECT64.f90',
    REC/'bootstrap_global_projection_publish_source_v2/COMPLETE_SOURCE_DERIVATION_AND_UNQUALIFIED_SCOPE.json',
    REC/'native_core_controls_source/test_current_ROOT64_native_core.f90',
    PACKAGE/'COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json',
    PACKAGE/'EXACT_UNFROZEN_V1_TO_V2_SOURCE_WRITER_DERIVATION.json',
    PACKAGE/'generate_full_connected17_source.py',
    PACKAGE/'rebuild_consumed_archive_admission_source.py',
    PACKAGE/'rebuild_connected17_host_binding_source.py',

    ROOT/'Ganlib/src/LCMTLC.f90'])
module_files=sorted({p for d in includes for p in d.glob('*.mod')})
paths.update(module_files)
dependencies=[pin(p)for p in sorted(paths)]
mutations=[
 'none: actual complete CAN/GLOBAL/PROJECT/all3 QBUILD/QREAD/native publish/read/import',
 'GLOBAL64 ROLE becomes NATIVE-K64 while retaining other full fields; wrong producer scope',
 'delete actual consumed ARCHIVE/FLUX plane3 ROOT64-SEAL; owning admission must refuse before QBUILD and return no product',
 'actual consumed ARCHIVE/FLUX plane3 ROOT-FLUX64 group370 is type2 instead oftype4; owning Native admission refuses',
 'actual consumed ARCHIVE/FLUX plane3 FLUX32 mirror group370 region1 changes by one binary32 ulp; owning Native admission refuses',
 'delete PROJECTED archive GLOBAL64 full tree',
 'PROJECTED root SPOT-R64/EPOCH becomes1 instead of0',
 'PROJECTED plane2 group370 scalar64 changes consistently in all three mirrors; canonical recomputation must still refuse',
 'delete SOURCE plane1 SPOT-R64/EPOCH commit record',
 'SOURCE plane1 SPOT-R64/EPOCH becomes1 while authority PROJECTED is0',
 'SOURCE plane1 STATE-VECTOR/nunk becomes4 instead of3',
 'MACRO_OUT plane1 group370 NTOT0 changes by one binary32 ulp; complete fullphysical macro recomputation detects it',
 'independent AXTRACK nested TRACK-META/RAW64 one binary64 ulp change; preserved GLOBAL full context differs',
 'independent AXSYSTEM group370 CORE-TAG64 one binary64 ulp change; preserved GLOBAL full context differs',
 'independent valid RCON CASE-NAME becomes CORE-OTHER, numerical contract unchanged',
 'SOURCE ROOT-QFISS64 and SPOT-R64/QFISS group370 both become type2 instead oftype4',
 'actual coherent new graph changes real Native group370 lowbit and global scalar input; all canonical/source/mirror/context values regenerated; persisted internal READs accept; external baseline fullEOF SHA/7ID refuses']
oracle=[]
for i,(name,mutation)in enumerate(zip(names,mutations),1):
    native=3 if i in (1,17)else(1 if i in (3,4,5)else 0)
    qr=3 if i in (1,17)else 1
    upstream=i in (2,6,7,8)
    oracle.append(dict(case=name,mutation=mutation,
        assertion_boundary=('independent_host_full_EOF_SHA_seven_ID'if i==17 else
            'owning_connected_Native_admission_before_QBUILD_READ'if i in (3,4,5,15)else
            'actual_complete_module_calls'),
        expected_actual_native_read_status=native,expected_actual_q_read_status=qr,
        expected_actual_global_checks=3 if i==17 else(2 if i==1 else 1),
        expected_actual_project_checks=3 if i==17 else(2 if i==1 or upstream else 1),
        expected_explicit_q_build_calls=4 if upstream else 3,
        expected_explicit_q_read_calls=9 if i==17 else(6 if i==1 else(3 if i in (3,4,5,15)else 4)),
        expected_explicit_native_publish_calls=4,
        expected_actual_archive_native_read_calls=51 if i==17 else(39 if i==1 else(
            33 if upstream or i in (3,4,5)else(28 if i==15 else 30))),
        expected_actual_archive_native_gate_calls=17 if i==17 else(13 if i==1 else(
            11 if upstream or i in (3,4,5)else 10)),
        expected_actual_archive_native_last_status=1 if i in (3,4,5,15)else 3,
        expected_actual_connected_q_build_calls=4 if upstream or i in (3,4,5)else 3,
        expected_actual_connected_q_read_calls=9 if i==17 else(6 if i==1 else 4),
        require_refused_QBUILD_products_empty=upstream or i in (3,4,5),
        external_only_refusal=i==17,
        expected_internal_acceptance_after_coherent_rewrite=i==17))
bind=dict(schema='CURRENT_COMPLETE_ROOT64_CONNECTED17_FIXED_SOURCE_ORACLE_AND_COMMAND_BINDING_V2',
    status='NEW_SOURCE_ONLY_17_SEMANTIC_REBUILD_NOT_COMPILED_OR_RUN',
    planned_output_root=str(OUT),source_pin=source_pin,
    actual_current_full_EOF_dependency_pins=dependencies,
    original_lost17_binding=pin(OLD_BIND),original_case_names=names,
    original_lost17_Source=dict(path='/private/tmp/SPOT_ROOT64_BOOT_CONNECTED_SOURCE_ONLY_14hrb510/controls/test_ROOT64_BOOT_connected.f90',
        expected_sha256='40fdaeb6264f71c58cfc1ae477333e2467e3f56313aeb9985805711a8536e55d',
        recovered=False,PASS_inherited=False),
    complete_current_mother_inverse_pin=pin(PACKAGE/'COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json'),
    declared_case_oracles=oracle,planned_compile_command=compile_command,planned_link_command=link_command,
    planned_run_commands=run_commands,logical_control_count=17,actual_run_phase_count=18,
    independent_host_coherent_binding=dict(filename='coherent_complete_context.xsm',
        baseline_phase='prepare',rewrite_phase='rewrite',
        before_external_manifest='Host_independent_coherent_baseline_full_EOF_SHA_7ID.json',
        expected_internal_reader_statuses=[3,3],
        required_refusal='actual complete EOF SHA must change and entire 7ID must change relative to independent baseline; immutable external manifest stays exact',
        Fortran_must_not_claim_internal_refusal=True),
    current_fixture=dict(synthetic_protocol_fixture=True,global_unknowns=14,global_scalar_regions=6,
        radial_unknowns=3,radial_scalar_regions=2,planes=3,groups=370,fission_slots=32,
        all32_NUSIGF_slots_nonzero=True,requested_rank=1,
        archive_full_SYSTEM_list=True,consumed_archive_native_plane_identities=[1,2,3],
        archive_Native_PUBLISH_before_GLOBAL_PROJECT_Q=True,
        owning_archive_Native_gate_before_all_QBUILD_QREAD=True,
        frozen_Context_Q_internal_Native_or_external_auth_contract=False,
        synthetic_rank_not_scientific_SVD_admission=True,
        EPS_TERMINAL=[2.5e-7,5.0e-8,2.5e-8],caps=[500,740],radial_ACCE=[3,3],global_route='B1/SIGS TYPE3 REBA0',radial_route='B0'),
    original_nine_numeric_flags=flags,original_guard_caps=dict(SELF_RSS_bytes=512*2**20,whole_wall_seconds=1800,
        single_step_seconds=600,history_bytes=96*2**30,fresh_bytes=2*2**30,free_floor_bytes=8*2**30,
        cold_reserve_bytes=20971764748,one_thread=True),
    complete_old_fixture_bytes_or_exact_old_oracle_data_proved=False,
    opaque_old_archives_source_to_object_mapping_proved=False,
    compiler_executed=False,link_executed=False,native_solver_or_transport_executed=False,
    genuine_producer_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,
    all17_current_semantic_controls_passed=False)
bind_pin=put('CURRENT_FULL_CONNECTED17_SOURCE_ORACLE_AND_COMMAND_BINDING.json',json.dumps(bind,ensure_ascii=False,indent=2)+'\n')

original_host=OLD_HOST.read_bytes().decode();host=original_host;host_changes=[]


def splice(before,after):
    global host
    assert host.count(before)==1,before[:120]
    host=host.replace(before,after,1);host_changes.append([before,after])


splice('"""Actual compile/link and 83 GANLIB core controls; no transport or old qualification."""',
       '"""Proposed original guarded full connected17 controls; never a solver or old PASS."""')
splice("OUT=ART/'axial-material-new-ROOT64-native-core-controls-20261011'",f"OUT=Path({str(OUT)!r})")
splice("CONTROL_BIND=REC/'native_core_controls_source/CURRENT_NATIVE_CORE_CONTROL_SOURCE_BINDING.json'",
       f"CONTROL_BIND=Path({bind_pin['path']!r})")
splice("if hashlib.sha256(CONTROL_BIND.read_bytes()).hexdigest()!='142e6869a49c8e2b623e2039be64f624d76d4e41874b67388eecf545460b80f0'",
       f"if hashlib.sha256(CONTROL_BIND.read_bytes()).hexdigest()!={bind_pin['sha256']!r}")
splice("    sources=[REC/'native_core_controls_source/test_current_ROOT64_native_core.f90']",
       f"    sources=[Path({str(SOURCE)!r})]")
old_includes="""    includes=[ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build',
              ART/'axial-material-r64-system-normalization-20261003/build',
              ROOT/'lib/Darwin_arm64/modules',ROOT/'Ganlib/lib/Darwin_arm64/modules']"""
splice(old_includes,'    includes='+repr(includes).replace('PosixPath(', 'Path('))
splice("    reviewed_new_sources={str(sources[0]):'94ab9ccc25d03d4affc5b54490e0aebd4e5fe618687aa68493557fbe99f212c6'}",
       f"    reviewed_new_sources={{str(sources[0]):{source_pin['sha256']!r}}}")
splice("    commands=[control['planned_compile_command'],control['planned_link_command'],control['planned_run_command']]",
'''    commands=[control['planned_compile_command'],control['planned_link_command']]+control['planned_run_commands']
    old_case_names=[command[-1]for command in old['control_commands']]
    if control['original_case_names']!=old_case_names or len(old_case_names)!=17 or len(commands)!=20:
        raise RuntimeError('all17 original names and18 actual run phases required')
    if [command[1]for command in control['planned_run_commands'][:16]]!=old_case_names[:16]:
        raise RuntimeError('exact originally declared first16 case order')
    if [command[1:]for command in control['planned_run_commands'][16:]]!=[
        ['coherent_source_tamper','prepare'],['coherent_source_tamper','rewrite']]:
        raise RuntimeError('explicit independent external binding phases')''')
splice("scope='compile/link/83 current GANLIB core controls; no transport or old qualification'",
       "scope='compile/link/current full17 connected synthetic protocol controls; no solver/old PASS/physics qualification'")
splice('    failure=None;watchdog_checks=[];after=None;after_check_error=None;actual_cases=[];actual_control_summary=None',
'''    failure=None;watchdog_checks=[];after=None;after_check_error=None;actual_cases=[]
    coherent_baseline=None;coherent_after=None;coherent_manifest_pin=None;external_refusal=None''')
loop="""            runner.execute(build,'compile_'+str(index),command,600)
            watchdog_checks.append(helper.check_watch(OUT,runner.records[-1]))"""
splice(loop,'''            if index==19:
                if coherent_baseline is None or coherent_manifest_pin is None:
                    raise RuntimeError('independent coherent baseline missing before actual rewrite')
                if pin(coherent_manifest_pin['path'])!=coherent_manifest_pin:
                    raise RuntimeError('independent coherent baseline manifest changed before rewrite')
                if pin(build/'coherent_complete_context.xsm')!=coherent_baseline:
                    raise RuntimeError('baseline full EOF and7ID changed before intended rewrite')
            runner.execute(build,'compile_'+str(index),command,600)
            watchdog_checks.append(helper.check_watch(OUT,runner.records[-1]))
            if index==18:
                coherent_baseline=pin(build/'coherent_complete_context.xsm')
                external_manifest=OUT/'Host_independent_coherent_baseline_full_EOF_SHA_7ID.json'
                write(external_manifest,dict(schema='INDEPENDENT_HOST_COHERENT_BASELINE_FULL_FILE_BINDING_V1',
                    actual_before_pin=coherent_baseline,expected_case='coherent_source_tamper',
                    Source_or_internal_labels_are_not_authority=True))
                coherent_manifest_pin=pin(external_manifest)
            if index==19:
                coherent_after=pin(build/'coherent_complete_context.xsm')
                if pin(coherent_manifest_pin['path'])!=coherent_manifest_pin:
                    raise RuntimeError('independent host baseline manifest changed')
                if coherent_after['sha256']==coherent_baseline['sha256']:
                    raise RuntimeError('no actual coherent full-file byte mutation occurred')
                if coherent_after['identity']==coherent_baseline['identity']:
                    raise RuntimeError('actual coherent rewrite lacks changed7ID')
                external_refusal=dict(case='coherent_source_tamper',
                    assertion='independent host exact fullEOF SHA and7ID binding',
                    before=coherent_baseline,after=coherent_after,
                    actual_SHA_matches=False,actual_seven_ID_matches=False,
                    actual_refused=True,Fortran_internal_refusal_claimed=False)''')
begin=host.index("        rows=[json.loads(line)for line in (build/'compile_2.log')")
end=host.index('        after=resources.check()',begin)
splice(host[begin:end],'''        for phase_index,command in enumerate(control['planned_run_commands']):
            rows=[json.loads(line)for line in (build/('compile_'+str(phase_index+2)+'.log')).read_text().splitlines()]
            if len(rows)!=2:raise RuntimeError('exact actual assertion row and actual call-status row required')
            actual,counts=rows
            name=command[1];phase=command[2]if len(command)==3 else 'single'
            oracle=next(p for p in control['declared_case_oracles']if p['case']==name)
            if actual.get('case')!=name or actual.get('phase')!=phase or counts.get('case')!=name or counts.get('phase')!=phase:
                raise RuntimeError('actual case/phase differs from independently declared oracle')
            if actual.get('all_actual_assertions_completed')is not True or actual.get('synthetic_fixture')is not True:
                raise RuntimeError('actual complete Source assertions missing')
            if any(actual.get(k)is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
                raise RuntimeError('synthetic component scope must remain explicit')
            for key in ('actual_native_read_status','actual_q_read_status','actual_global_checks','actual_project_checks',
                        'explicit_q_build_calls','explicit_q_read_calls','explicit_native_publish_calls',
                        'actual_archive_native_read_calls','actual_archive_native_gate_calls',
                        'actual_archive_native_last_status','actual_connected_q_build_calls',
                        'actual_connected_q_read_calls'):
                if counts.get(key)!=oracle['expected_'+key]:
                    raise RuntimeError('actual module status/count differs from independently declared oracle '+name+' '+key)
            actual_cases.append(dict(case=name,phase=phase,assertions=actual,actual_statuses_and_call_counts=counts))
        if len(actual_cases)!=18 or [p['case']for p in actual_cases[:16]]!=control['original_case_names'][:16]:
            raise RuntimeError('all17 semantic controls, including two true coherent phases, required')
        if external_refusal is None or external_refusal['actual_refused']is not True:
            raise RuntimeError('actual independent host full-file coherent rejection required')
''')
begin=host.index("    report=dict(schema='ACTUAL_NEW_ROOT64_GANLIB_CORE_CONTROLS_ROOT_V1',")
end=host.index("    write(OUT/'Root_actual_compile_only_summary.json',report)",begin)
splice(host[begin:end],'''    report=dict(schema='ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V2',
        status='ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY'if failure is None else 'FAILED_CURRENT17_COMPONENT_CONTROLS_NO_RETRY',
        failure=failure,after_check_error=after_check_error,records=runner.records,fixed_current_pins=fixed,
        actual_cases=actual_cases,actual_logical_control_count=17 if failure is None else None,
        actual_run_phase_count=len(actual_cases),actual_independent_host_coherent_refusal=external_refusal,
        independent_coherent_baseline_manifest_pin=coherent_manifest_pin,
        actual_watchdog_checks=watchdog_checks,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_pins=[pin(p)for p in sorted(build.iterdir())if p.is_file()],
        original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
        resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
        all17_original_names_exercised=failure is None,
        lost_old17_fixture_bytes_or_exact_old_data_reexecuted=False,
        old_seventeen_PASS_inherited=False,synthetic_fixture=True,
        complete_native_build_qualified=False,Dragon_linked=False,transport_executed=False,
        continuous_REAL64_producer_qualified=False,online_BOOT_qualified=False,
        AAA_qualified=False,ABA_admitted=False,goal_complete=False)
''')
ast.parse(host)
inverse=host
for before,after in reversed(host_changes):
    assert inverse.count(after)==1
    inverse=inverse.replace(after,before,1)
assert inverse==original_host
host_pin=put('proposed_original_guarded_full_connected17_runner.py',host)
host_retained=put('original_exact_source/run_current_ROOT64_native_core_controls.py',original_host)
host_proof=put('COMPLETE_ORIGINAL_GUARDED_HOST_EXACT_BYTE_INVERSE.json',json.dumps(dict(
    schema='COMPLETE_CORE_HOST_TO_NEW_CONNECTED17_GUARDED_RUNNER_BYTE_INVERSE_V1',
    original=pin(OLD_HOST),retained_complete_original=host_retained,new=host_pin,
    literal_changes=host_changes,full_byte_inverse_matches=inverse==original_host,
    original_pin_fullEOF7ID_function_Resources_MRO_runner_watchdog_caps_preserved=True,
    original_nine_numeric_flags=flags,Python_AST_parse_only=True,
    compiler_or_native_or_transport_executed=False),ensure_ascii=False,indent=2)+'\n')
put('ABI_ORACLE_EXTERNAL_HOST_AND_UNQUALIFIED_SCOPE.txt','''NEW complete seventeen semantic component controls, Source-only. No old PASS inherited.
Old /tmp fullfixture 40fdaeb6 was lost. It is not claimed recovered or byte-equivalent.
Complete extant83core Source 94ab9ccc is the exact retained mother; all old fixture
factory/helper bytes remain, but the83main is not used as a substitute for17controls.

Full positive path publishes each actual ARCHIVE/FLUX plane independently with
its real same-index TRACK/SYSTEM/MICROLIB2, RCON, plane=p/e0 before GLOBAL. The
owning connected caller actually Native READs all three consumed archive leaves
before GLOBAL, PROJECT, every QBUILD and QREAD; full XSM reopen uses the same gate.
CAN WRITE, GLOBAL PUBLISH, PROJECT ARCHIVE, all3plane QBUILD/QREAD and the retained
independent Native PUBLISH/READ/IMPORT are actual calls. Negative3/4/5 mutate the
consumed archive plane3, not the independent radial sibling; owning QBUILD refuses
and fresh outputs stay empty, then owning QREAD refuses with no loaded authority.
Frozen Context/Q modules do not themselves claim Native seal or external fullfile
authentication. The explicit owning gate is new test/caller Source, not hidden
qualification of an unchanged production caller. Synthetic values exercise
true current serialization and readers without invoking a transport/physics solver.
GLOBAL has six scalar regions plus eight face-current unknowns. Radial has two
scalars and one signedzero surface unknown. All370groups and all32fission slots
are complete and nonzero. Full physical macro/context trees are retained.

All17 exact names come from the retained original fixed binding. The new declared
oracle states every mutation and actual module status/count before execution.
Coherent control has18th run phase because external host must register the real
complete XSM EOF SHA/7ID afterprepare, then guard that independent manifest while
the realrewrite program creates a new mathematically/contextually coherent graph.
Persisted XSM is reopenedreadonly and actual internal readers must accept both
phases. The actual external host comparison must reject changed SHA and7ID.
Fortran refuses no coherent case; no fake metadata boolean stands in for rejection.

Proposed host is the complete existing original guarded core runner with exact
local reversible Source substitutions. It keeps real support imports, original
MRO/OwnRSSSerialExecutor/Resources/check_watch/fullEOF7ID pin function, one thread,
all original nine numeric flags, wholewall1800s/step600s/SELF512MiB, history96GiB,
fresh2GiB/freefloor8GiB and original cold reserve. It has not been executed here.

Parent must independently review and freeze Source/binding/host, then perform
actual bounded compile/link and all20guarded process steps (2build+18casephases).
Runtime failure is no retry. Current17semantic completion must be established
from actual module assertions/statuses and actual host fullfile rejection.
No oldfixture qualification, genuine producer/solver/transport/onlineBOOT,
full-source archivebuild, formalAAA or ABA qualification is granted.
''')
print(json.dumps(dict(source_pin=source_pin,binding_pin=bind_pin,host_pin=host_pin,
    host_inverse_pin=host_proof,dependency_count=len(dependencies),current_case_count=17,
    actual_phase_count=18,planned_guarded_process_steps=20,Python_AST_parse_only=True,
    compiler_or_solver_executed=False,elapsed_seconds=time.monotonic()-start)))

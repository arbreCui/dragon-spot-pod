from pathlib import Path
import json
import hashlib
import ast
import time

HERE=Path(__file__).resolve().parent
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p.stat());b=p.read_bytes();z=ident(p.stat());assert a==z and len(b)==a[4]
    return dict(path=str(p),size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),identity=a)
def full_inverse(name):
    proof=json.loads((HERE/name).read_bytes())
    original=proof['original'];new=proof['new']
    assert pin(original['path'])==original and pin(new['path'])==new
    s=Path(new['path']).read_text()
    for before,after in reversed(proof['literal_changes']):
        assert s.count(after)==1
        s=s.replace(after,before,1)
    assert s.encode()==Path(original['path']).read_bytes()
    retained=proof.get('retained_complete_original',proof.get('retained_complete_original',proof.get('retained')))
    assert Path(retained['path']).read_bytes()==s.encode() and pin(retained['path'])==retained
    return dict(proof_pin=pin(HERE/name),literal_change_count=len(proof['literal_changes']),
                whole_file_inverse_matches=True,original_current_pin=original,new_current_pin=new)

start=time.monotonic()
proofs=[full_inverse(p)for p in (
    'COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json',
    'COMPLETE_ORIGINAL_GUARDED_HOST_EXACT_BYTE_INVERSE.json',
    'EXACT_UNFROZEN_V1_TO_V2_SOURCE_WRITER_DERIVATION.json',
    'EXACT_UNFROZEN_V1_TO_V2_BINDING_WRITER_DERIVATION.json')]
binding=json.loads((HERE/'CURRENT_FULL_CONNECTED17_SOURCE_ORACLE_AND_COMMAND_BINDING.json').read_bytes())
for p in binding['actual_current_full_EOF_dependency_pins']:assert pin(p['path'])==p
assert pin(binding['source_pin']['path'])==binding['source_pin']
for p in HERE.glob('*.py'):ast.parse(p.read_text())
source=Path(binding['source_pin']['path']).read_text()
assert max(map(len,source.splitlines()))<=132
assert 'systems=LCMLID(f%archive,\'SYSTEM\',NP)' in source
archive_start=source.index("systems=LCMLID(f%archive,'SYSTEM',NP)")
publish=source.index('call SPOR64_BOOT64_PUBLISH_NATIVE(seed,seedtrack,seedsystem,seedmaterial,')
global_publish=source.index('call SPOR64_BOOT_GLOBAL_PUBLISH(f%global,')
assert archive_start<publish<global_publish
assert 'f%radial%route,p,0,f%radial%image,K64,gates,2,1,1,ps)' in source
assert "case(3)\n      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)" in source
assert 'actual bound archive Native READ refusal' in source
assert 'owning BUILD refusal output atomicity' in source
assert 'call archive_native_admission(f,ok)' in source
assert 'call assert_connected(saved)' in source
assert 'call LCMOP(bundle,filename,2,2,0)' in source
assert source.count('call SPOR64_BOOTQ64_BUILD(')==1
assert source.count('call SPOR64_BOOTQ64_READ(')==1
read_body=source[source.index('  subroutine read_q'):source.index('  end subroutine read_q')]
build_body=source[source.index('  subroutine connected_q_build'):source.index('  end subroutine connected_q_build')]
for body in (read_body,build_body):
    assert body.index('call archive_native_admission(f,ok)')<body.index('if(.not.ok) return')
assert source.count('call SPOR64_BOOT64_PUBLISH_NATIVE(seed,seedtrack,seedsystem,seedmaterial,')==1

# Independently enumerate the actual candidate's call graph, without executing
# Fortran, loading native modules, or claiming that any declared oracle passed.
# Base: GLOBAL gate1 + PROJECT gate1 +3 BUILD gates + assert top1/3 READ gates =9.
# Each full assert adds4 gates (3 Native READs per gate); coherent also savedassert.
oracles=binding['declared_case_oracles'];assert len(oracles)==17
expected_names=['positive','global_wrong_scope','missing_producer_seal','root_flux32_disguised',
    'wrong_root_mirror','missing_global64','bad_seed_epoch','fabricated_projected',
    'uncommitted_source','wrong_source_epoch','wrong_source_dimensions','mutated_macro',
    'mutated_track','mutated_system','different_route','qfiss32_disguised','coherent_source_tamper']
assert binding['original_case_names']==expected_names
static=[]
for i,p in enumerate(oracles,1):
    assert p['case']==expected_names[i-1]
    upstream=i in (2,6,7,8);native_bad=i in (3,4,5);route_bad=i==15
    extra_asserts=2 if i==17 else(1 if i==1 else 0)
    extra_build=1 if upstream or native_bad else 0
    extra_read=0 if i in (1,17)else 1
    gates=9+4*extra_asserts+extra_build+extra_read
    reads=3*gates-(2 if route_bad else 0)
    read_extra_core=extra_read if not(native_bad or route_bad)else 0
    expected=dict(actual_native_read_status=3 if i in (1,17)else(1 if native_bad else 0),
        actual_q_read_status=3 if i in (1,17)else 1,
        actual_global_checks=1+extra_asserts,
        actual_project_checks=1+extra_asserts+(1 if upstream else 0),
        explicit_q_build_calls=3+(1 if upstream else 0),
        explicit_q_read_calls=3+3*extra_asserts+read_extra_core,
        explicit_native_publish_calls=4,
        actual_archive_native_read_calls=reads,actual_archive_native_gate_calls=gates,
        actual_archive_native_last_status=1 if native_bad or route_bad else 3,
        actual_connected_q_build_calls=3+extra_build,
        actual_connected_q_read_calls=3+3*extra_asserts+extra_read)
    for k,v in expected.items():assert p['expected_'+k]==v,(p['case'],k,p['expected_'+k],v)
    static.append(dict(case=p['case'],static_source_call_graph_expected_counts=expected,
                       actual_native_or_host_control_executed=False))
assert len(binding['planned_run_commands'])==18
assert len([binding['planned_compile_command'],binding['planned_link_command']]+
           binding['planned_run_commands'])==20
host=(HERE/'proposed_original_guarded_full_connected17_runner.py').read_text()
assert binding['source_pin']['sha256'] in host
assert pin(HERE/'CURRENT_FULL_CONNECTED17_SOURCE_ORACLE_AND_COMMAND_BINDING.json')['sha256'] in host
assert 'coherent_after[\'sha256\']==coherent_baseline[\'sha256\']' in host
assert 'coherent_after[\'identity\']==coherent_baseline[\'identity\']' in host
assert "pin(coherent_manifest_pin['path'])!=coherent_manifest_pin" in host
assert "Fortran_internal_refusal_claimed=False" in host
report=dict(schema='COMPLETE_CONNECTED17_V2_SOURCE_BYTE_AND_DECLARED_ORACLE_AUDIT_ONLY',
    whole_byte_inverse_proofs=proofs,
    current_dependency_count=len(binding['actual_current_full_EOF_dependency_pins']),
    all_declared_current_dependencies_match_full_EOF_SHA_seven_ID=True,
    exact_original17_names_18_phases_20_planned_steps=True,
    consumed_archive_Native_identity_and_before_GLOBAL_order_static_checked=True,
    connected_QBUILD_QREAD_owning_Native_gate_static_checked=True,
    negative_seal_cases_mutate_consumed_plane3_static_checked=True,
    host_external_full_file_coherent_boundary_static_checked=True,
    static_source_call_graph_oracles=static,
    Python_AST_parse_only=True,Fortran_parser_or_compiler_executed=False,
    actual17_controls_passed=False,native_solver_or_transport_executed=False,
    physical_or_producer_qualification=False,
    elapsed_seconds=time.monotonic()-start)
out=HERE/'COMPLETE_SOURCE_ONLY_BYTE_AND_ORACLE_AUDIT.json'
with out.open('x')as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(dict(audit_pin=pin(out),current_dependencies=report['current_dependency_count'],
    inverse_proof_count=len(proofs),full_inverse_and_current_pins=True,
    static_declared_oracle_count=len(static),compiler_or_native_executed=False,
    elapsed_seconds=report['elapsed_seconds'])))

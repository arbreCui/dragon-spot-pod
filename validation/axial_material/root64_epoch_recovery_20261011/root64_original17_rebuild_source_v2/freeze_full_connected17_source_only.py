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

start=time.monotonic()
source=pin(HERE/'test_ROOT64_full_connected17_v2.f90')
assert source['sha256']=='28e229ff6d1eb3d9f0b4d3ee0c1e96b207d5b1d417876f2f2653947bade45273'
bindpin=pin(HERE/'CURRENT_FULL_CONNECTED17_SOURCE_ORACLE_AND_COMMAND_BINDING.json')
assert bindpin['sha256']=='5c814055544fe6308dd19cdcf09b9b8d6626a963233fdd18dd85084a6df82b93'
hostpin=pin(HERE/'proposed_original_guarded_full_connected17_runner.py')
assert hostpin['sha256']=='ffe957817aac56638fd486a40a471a2606083a52c8525d7b59f9022b5dbce3c7'
review_path=HERE/'INDEPENDENT_SOURCE_REVIEW_ACTUAL_MESSAGE.json'
review=json.loads(review_path.read_bytes())
assert review['actual_reviewed_source_sha256']==source['sha256']
assert review['consumed_archive_seal_lineage_gap_fixed']is True
assert review['known_material_source_blocker_remaining']is False
assert review['compiler_or_controls_or_solver_executed_by_review']is False
binding=json.loads(Path(bindpin['path']).read_bytes())
for p in binding['actual_current_full_EOF_dependency_pins']:assert pin(p['path'])==p
audit=HERE/'COMPLETE_SOURCE_ONLY_BYTE_AND_ORACLE_AUDIT.json'
assert pin(audit)['sha256']=='36415b84fc1812bdf1e136682b32d9e77c0b808ba20837db15ed01c9d22c70c2'
for p in HERE.glob('*.py'):ast.parse(p.read_text())
receipts=dict(schema='ACTUAL_STD_LIBRARY_SOURCE_WRITER_TOOL_RETURNS_NO_NATIVE_V2',
    actual_tools=[
        dict(chunk_id='b72c89',exit_code=0,operation='write complete consumed-archive Source writer from exact unfrozen v1 writer'),
        dict(chunk_id='e04ef8',exit_code=0,elapsed_self_seconds=0.0015009160015324596,
             operation='write complete Fortran Source and7-splice complete mother inverse proof'),
        dict(chunk_id='976cf7',exit_code=0,operation='write complete connected17 binding/host writer from exact unfrozen v1 writer'),
        dict(chunk_id='3aa408',exit_code=0,elapsed_self_seconds=0.020621084000595147,
             operation='write exact independent17oracle126dep binding/full originalguarded host and13-splice inverse'),
        dict(chunk_id='2e2c2d',exit_code=0,elapsed_self_seconds=0.023697999997239094,
             operation='pure fullbyteinverse/current126pins/PythonAST/static Source-callgraph oracle audit')],
    failed_unfrozen_v1_writer_attempt_preserved=dict(chunk_id='ebc5b2',exit_code=1,
        reason='program rename splice also matched end program; no Fortran file created on that attempt',
        no_old_v1_PASS_inherited=True),
    unqualified_initial_v1_consumed_archive_seal_lineage_gap=True,
    no_compiler_native_transport_or_cleanup_executed=True)
receipt_path=HERE/'SOURCE_ONLY_REBUILD_ACTUAL_TOOL_RECEIPTS.json'
with receipt_path.open('x')as f:json.dump(receipts,f,indent=2);f.write('\n')
package_pins=[pin(p)for p in sorted(HERE.rglob('*'))if p.is_file()]
freeze=dict(schema='COMPLETE_CONNECTED_ROOT64_ORIGINAL17_SEMANTIC_REBUILD_SOURCE_FREEZE_V2',
    status='FROZEN_REVIEWED_SOURCE_ONLY_NOT_COMPILED_OR_RUN',
    source_pin=source,binding_pin=bindpin,host_pin=hostpin,
    actual_dependency_full_EOF_pins=binding['actual_current_full_EOF_dependency_pins'],
    complete_package_file_pins_before_manifest=package_pins,
    independent_review_message_pin=pin(review_path),
    byte_inverse_and_static_oracle_audit_pin=pin(audit),
    actual_source_writer_receipts_pin=pin(receipt_path),
    original17_names=binding['original_case_names'],logical_controls=17,planned_phases=18,planned_guarded_steps=20,
    consumed_archive_native_seal_published_and_checked_plane_identities=[1,2,3],epoch=0,
    full_SYSTEM_TRACK_MICROLIB2_FLUX_and_RCON_authority_preserved=True,
    all370_groups_all32_fission_slots_native_non_scalar_fields_preserved=True,
    missingseal_rootType2_mirror_controls_on_consumed_tailplane3_tailgroup370=True,
    explicit_owning_Native_gate_before_GLOBAL_PROJECT_QBUILD_QREAD=True,
    actual_production_frozen_CLE_entry_automatically_acquires_fixture_gate=False,
    Context_Q_internally_authenticates_Native_seal_or_external_host_SHA=False,
    coherent_internal_acceptance_requires_real_external_host_fullEOF_SHA_7ID_refusal=True,
    whole_original83mother_and_originalguardedhost_reverse_bytes_proved=True,
    exact_lost_old17_fixture_bytes_or_old_data_oracles_recovered=False,
    old17_PASS_inherited=False,actual17_controls_passed=False,
    actual_compiler_link_native_solver_transport_or_cleanup_executed=False,
    synthetic_protocol_fixture_only=True,original_guard_and_nine_numeric_flags_unchanged=True,
    opaque_archive_source_to_object_mapping_proved=False,
    genuine_producer_qualified=False,online_BOOT_qualified=False,
    scientific_AAA_qualified=False,ABA_admitted=False,goal_complete=False,
    remaining_scope=['Parent independent bounded compile/link and actual18phase17control execution with20realguardedsteps',
       'Actual production caller must own its relevant Native/fullcontext/externalhost boundaries; fixture gate is not inherited',
       'Genuine3plane strict terminal solver lifecycle, trueglobal/projection/Q/BOOT still require actual guarded qualification',
       'Science formal uniform-rank1 AAA7/8 end3.9525259224%>3%; ABA notadmitted; independentrank2 route353/370 remains separate'],
    elapsed_seconds=time.monotonic()-start)
out=HERE/'COMPLETE_CONNECTED17_V2_SOURCE_FREEZE.json'
with out.open('x')as f:json.dump(freeze,f,indent=2);f.write('\n')
assert pin(Path(source['path']))==source and pin(Path(bindpin['path']))==bindpin and pin(Path(hostpin['path']))==hostpin
print(json.dumps(dict(freeze_pin=pin(out),source_pin=source,host_pin=hostpin,binding_pin=bindpin,
    package_files=len(package_pins),current_dependency_count=len(binding['actual_current_full_EOF_dependency_pins']),
    compiler_or_controls_or_solver_executed=False,elapsed_seconds=freeze['elapsed_seconds'])))

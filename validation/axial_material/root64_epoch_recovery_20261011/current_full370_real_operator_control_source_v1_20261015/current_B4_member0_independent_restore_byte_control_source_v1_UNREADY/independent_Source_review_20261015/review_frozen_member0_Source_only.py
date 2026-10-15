"""Independent Source/meta review only; never imports the candidate or helpers."""
import ast
import hashlib
import json
import pathlib
import stat

HERE = pathlib.Path(__file__).absolute().parent
BASE = HERE.parent
EXPECTED_SOURCE_SHA = '9db28de32457c18c7fe946de3bb2691ebbd2d567c9e3bd3dbcb6a781a9a4b8c5'
EXPECTED_AUTHOR_SHA = 'd06f2998ba6a6255e7fc7ebad0fb49d75f0ef2f85497689347aae5c97953208e'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def small(p):
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_size < 8 * 1024 * 1024
    raw = p.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest and identity(s) == identity(p.lstat())
    return raw, dict(path=str(p), sha256=digest, size_bytes=s.st_size, identity=identity(s))


def main():
    author_raw, author_pin = small(BASE / 'AUTHOR_SOURCE_ONLY_FREEZE.json')
    assert author_pin['sha256'] == EXPECTED_AUTHOR_SHA and author_pin['size_bytes'] == 4175
    author = json.loads(author_raw)
    assert author['Source_author_task'] == '/root/b_capture_source_peer'
    texts = {}
    for p in author['whole_Source_and_NULL_template_file_pins']:
        raw, actual = small(pathlib.Path(p['path']))
        assert actual == p
        texts[pathlib.Path(p['path']).name] = raw.decode('utf-8')
    source_pin = author['algorithm_Source_pin']
    assert source_pin['sha256'] == EXPECTED_SOURCE_SHA and source_pin['size_bytes'] == 18290
    source = texts['verify_B4_member0_original_bytes_Root_only.UNREADY.py']
    tree = ast.parse(source)
    binding = json.loads(texts['DRAFT_BINDING_PENDING_GENUINE_FAILURE_POST0.json'])
    arguments = json.loads(texts['ROOT_ARGUMENT_TEMPLATE_PENDING_SUPPLEMENT0.json'])
    assert binding['actual_preconditions_closed'] is False and binding['actual_failed_archive_and_post_roles_audited'] is False
    assert binding['actual_failed_archive_closure_pins']['supplement'] is None
    assert binding['actual_failed_archive_closure_pins']['supplement_tools'] is None
    assert binding['actual_failure_supplement_key_projection'] is None
    assert len(binding['complete_joint_roots']) == 73
    archive_raw, archive_pin = small(pathlib.Path(binding['original_B4_execution_binding_pin']['path']))
    assert archive_pin == binding['original_B4_execution_binding_pin']
    archive_binding = json.loads(archive_raw)
    assert binding['complete_joint_roots'] == archive_binding['complete_joint_roots']
    common_raw, common_pin = small(pathlib.Path(binding['frozen_B4_common_Source_pin']['path']))
    assert common_pin == binding['frozen_B4_common_Source_pin']
    common = common_raw.decode('utf-8')
    ast.parse(common)
    assert 'resources=c.Resources(archive_binding,started,600)' in source
    assert 'c.admit(' not in source
    assert 'last_full_completed=time.monotonic()' in source
    assert 'time.monotonic()-last_full_completed>=5.0' in source
    assert source.count('blind_gzip_sha()') == 3
    assert 'budget();chunk=f.read(2**20)' in source
    assert 'budget();chunk=stream.read(2**20)' in source
    assert 'post[k[\'recorded_child_codes_field\']]==[]' in source
    assert 'self.joined=production.DiskResources' in common
    assert 'binding[\'complete_joint_roots\']' in common
    assert 'own_open_unlinked_bytes' in common and '20971764748' in common
    supplement_path = BASE.parent / 'current_B4_complete_products_lossless_archive_source_v1_UNREADY/supplemental_failure_member0_metadata_source_v1_UNREADY/verify_recorded_B4_failure_child1_member0_metadata.UNREADY.py'
    supplement_raw, supplement_pin = small(supplement_path)
    supplement_source = supplement_raw.decode('utf-8')
    ast.parse(supplement_source)
    assert "'supplemental_actual_recorded_child_integer_exit_codes': [watch['returncode']]" in supplement_source
    assert "'recorded_complete_member000': entry" in supplement_source
    assert "all(type(v)is str for v in sk.values())" in source
    assert "type(supplement[sk['child_integer_exit_code_field']])is int" in source
    assert "supplement[sk['original0_pin_field']]==original" in source
    report = dict(
        schema='INDEPENDENT_B4_MEMBER0_ROOT_ONLY_VERIFIER_SOURCE_REVIEW_V1',
        status='BLOCKED_SOURCE_INTERFACE_AND_PENDING_TRUE_SUPPLEMENT_NO_EXECUTION_ADMISSION',
        source_only=True, review_completed=True, candidate_executed=False,
        Source_author_task='/root/b_capture_source_peer', independent_reviewer_task='/root/b2_build_source_peer',
        author_freeze_pin=author_pin, algorithm_Source_pin=source_pin,
        complete_frozen_Source_and_NULL_template_pins=author['whole_Source_and_NULL_template_file_pins'],
        original_B4_binding_pin=archive_pin, original_B4_common_Source_pin=common_pin,
        pending_supplement_Source_pin_used_for_interface_review=supplement_pin,
        blocking_findings=[
            dict(kind='SOURCE_INTERFACE_DEFECT', file=source_pin['path'], line=76,
                 detail='String-only top-level projection at lines76-77 cannot represent the frozen supplement report: original0 is recorded_complete_member000.original_plain_full_pin; child code is supplemental_actual_recorded_child_integer_exit_codes[0]. There is no top-level original0 PF or child integer scalar. A new frozen verifier Source must admit exact nested/index roles; preserve the original report and tool objects.'),
            dict(kind='EXPECTED_PENDING_RUNTIME_PRECONDITION', detail='Genuine independent supplement0 report/tools PF and audited exact schema projection remain NULL. Do not authorize the Root byte verifier until actual closed typed0 and exact stdout report PF have been bound.')
        ],
        other_blocking_Source_findings=[],
        reviewed_algorithm_scope=dict(
            original_complete_joint_roots=73, entire_original_prefix_preserved=True,
            original_common_Resources_wholebytes_reused=True, fresh_output_admit_not_called=True,
            Root_SELF_cap_mib=512, Root_stage_cap_seconds=600, new_Source_cap_bytes=16*1024*1024,
            every_compressed_and_decompressed_chunk_light_guard=True,
            heavy_original_resource_scan_completion_based_interval_seconds=5.0,
            full_history_cold_metadata_free_external_and_open_unlinked_accounting_retained=True,
            original_B4_output64MiB_and_Source16MiB_component_bounds_retained=True,
            original_m_xsm_current7_only=True, complete_gzip000_only_payload_read=True,
            blind_gzip_full_SHA_passes=2, full_streamed_decompression_passes=1,
            no_restored_product_file_emitted=True, no_child_or_native_or_compiler=True,
            streamed_decompressed_SHA_and_length_must_equal_saved_original_fullPF=True,
            actual_Root1_child1_required=True, original_post_child_codes_empty_preserved=True,
            all4_success_not_inferred=True),
        exact_argument_requirements=dict(
            explicit_flags=['--binding-pin','--source-pin'],
            source_pin_exactly=source_pin,
            binding_role_schema='ROOT_CURRENT_B4_MEMBER0_RESTORATION_BYTE_CONTROL_BINDING_V1',
            new_actual_binding_required=True,
            actual_preconditions_closed=True, actual_failed_archive_and_post_roles_audited=True,
            genuine_supplement0_report_tools_and_exact_nested_projection_required=True,
            original_73_prefix_binding_and_all_original_role_PFs_must_remain_exact=True,
            original_environment_required=dict(PYTHONOPTIMIZE='unset',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1'),
            exact_interpreter='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',
            Source_author_reviewer_must_not_execute_Root_only_program=True),
        execution_admitted=False, gzip_or_original_product_body_opened=False,
        helper_or_candidate_imported=False, Source_GEN_or_publication_executed=False,
        compiler_native_or_child_executed=False, files_deleted=False,
        all4_archive_complete=False, retirement_authorized=False,
        physics_qualified=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False,
    )
    target=HERE/'REVIEW.json'
    with target.open('x') as f:
        json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps({'status':report['status'],'review_pin':small(target)[1]}))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Create the immutable, failure-only PHYS inventory Source; never compile/run."""
import hashlib
import json
import os
from pathlib import Path
import stat

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD = REC / 'boot_v16_BIND64_82_explicit_return_diagnostic_source_v1_20261014'
OUT = REC / 'boot_v16_BIND64_failed_PHYS_inventory_diagnostic_source_v1_20261014'
EVENT_SCHEMA = 'ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1'


def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read_pin(path):
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError('ordinary Source/proof required')
        chunks = []
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block:
                break
            chunks.append(block)
        data = b''.join(chunks)
        after = os.fstat(fd)
        if seven(before) != seven(after) or len(data) != before.st_size:
            raise RuntimeError('Source/proof changed while read')
    finally:
        os.close(fd)
    return data, dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                      size_bytes=len(data), identity=seven(before))


def write_new(name, data):
    path = OUT / name
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(fd, 'wb', closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(fd)
    finally:
        os.close(fd)
    result, pin = read_pin(path)
    if result != data or pin['identity'][3] != 1:
        raise RuntimeError('owned Source publication mismatch')
    return pin


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def main():
    source_bytes, source_pin = read_pin(OLD / 'SPOR64_BOOT_BIND64.f90')
    if source_pin['sha256'] != '3e41669ac342b567aef5dc8d2bb801265e9b61a58cdbc106adf64a18cf41022b':
        raise RuntimeError('exact actual BIND82 Source required')
    predecessor_sf_bytes, predecessor_sf_pin = read_pin(
        OLD / 'COMPLETE_BOOT_BIND64_82_EXPLICIT_RETURN_DIAGNOSTIC_SOURCE_FREEZE.json')
    predecessor_sf = json.loads(predecessor_sf_bytes)
    if predecessor_sf['diagnostic_source_pin'] != source_pin:
        raise RuntimeError('predecessor freeze exact Source pin')
    schema_bytes, schema_pin = read_pin('/Users/wen/spot/src/SPOR64_SCHEMA.f90')
    producer_bytes, producer_pin = read_pin(
        '/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build/MCGASM.f')
    post_bytes, post_pin = read_pin(
        REC / 'independent_BIND47_explicit_return_diagnostic_v1_actual_failure_postverify_20261014/REVIEW.json')
    post = json.loads(post_bytes)
    if (post['schema'] != 'INDEPENDENT_BIND47_EXPLICIT_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'
            or post['failure'] is not None or post['actual_Root_exit_code'] != 1
            or post['actual_Root_closed'] is not True):
        raise RuntimeError('actual failed BIND47 provenance')
    report_bytes, report_pin = read_pin(post['actual_report_pin']['path'])
    if report_pin != post['actual_report_pin']:
        raise RuntimeError('exact immutable failed report')
    report = json.loads(report_bytes)
    log_bytes, log_pin = read_pin(post['actual_failure_log_pin']['path'])
    if log_pin != post['actual_failure_log_pin']:
        raise RuntimeError('exact actual failure log')
    source = source_bytes.decode()
    old_system = '''          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(macro_group,'NTOT0',nmat,2)) then'''
    new_system = '''          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        write(6,'(A,I0,A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
          '"event":"caller","original_return_source_line":168,"group_index":', &
          ig,',"plane_index":',plane,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(macro_group,'NTOT0',nmat,2)) then'''
    old_response = '''          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        return
      endif
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)'''
    new_response = '''          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        block
          character(len=72) :: diag_file
          character(len=12) :: diag_object,diag_name,diag_first
          character(len=24) :: diag_name_hex
          integer :: diag_length,diag_type,diag_count,diag_j,diag_object_length
          logical :: diag_empty,diag_lcm,diag_associated,diag_complete,diag_truncated
          diag_file=' ';diag_object=' ';diag_name=' ';diag_first=' '
          diag_object_length=0;diag_empty=.false.;diag_lcm=.false.
          diag_count=0;diag_complete=.false.;diag_truncated=.false.
          diag_associated=c_associated(group)
          if(diag_associated)then
            call LCMINF(group,diag_file,diag_object,diag_empty,diag_object_length,diag_lcm)
          endif
          write(6,'(A,I0,A,I0,A,I0,A,I0,A)') &
            '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
            '"event":"begin","original_return_source_line":236,"maximum_records":64,'// &
            '"expected_schema":"SCHEMA_RESPONSE_GROUP_PHYS","expected_count":15,'// &
            '"associated_integer":',merge(1,0,diag_associated), &
            ',"empty_integer":',merge(1,0,diag_empty), &
            ',"object_length":',diag_object_length, &
            ',"memory_integer":',merge(1,0,diag_lcm),'}'
          if(diag_associated.and.diag_object_length==-1)then
            if(diag_empty)then
              diag_complete=.true.
            else
              call LCMNXT(group,diag_name)
              if(diag_name/=' ')then
                diag_first=diag_name
                do
                  diag_count=diag_count+1
                  call LCMLEN(group,diag_name,diag_length,diag_type)
                  do diag_j=1,12
                    write(diag_name_hex(2*diag_j-1:2*diag_j),'(Z2.2)') &
                      iachar(diag_name(diag_j:diag_j))
                  enddo
                  write(6,'(A,I0,A,A,A,I0,A,I0,A)') &
                    '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
                    '"event":"record","ordinal":',diag_count, &
                    ',"name_bytes_hex":"',diag_name_hex,'","length":',diag_length, &
                    ',"type":',diag_type,'}'
                  call LCMNXT(group,diag_name)
                  if(diag_name==diag_first)then
                    diag_complete=.true.
                    exit
                  endif
                  if(diag_count==64)then
                    diag_truncated=.true.
                    exit
                  endif
                  if(diag_name==' ')exit
                enddo
              endif
            endif
          endif
          write(6,'(A,I0,A,I0,A,I0,A)') &
            '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
            '"event":"end","original_return_source_line":236,"record_count":',diag_count, &
            ',"complete_integer":',merge(1,0,diag_complete), &
            ',"truncated_integer":',merge(1,0,diag_truncated),'}'
          flush(6)
        end block
        return
      endif
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)'''
    changes = [dict(before=old_response, after=new_response,
                    reason='Only after original PHYS inventory failure: at most64 names encoded as exact12-byte hex, LCMLEN header, and truthful completion/truncation; no payload.'),
               dict(before=old_system, after=new_system,
                    reason='Only original SYSTEM168 failed RESPONSE call: output already initialized native loop ig and plane; original status event and return preserved.')]
    for change in changes:
        if source.count(change['before']) != 1:
            raise RuntimeError('exact unique predecessor Source block required')
        source = source.replace(change['before'], change['after'], 1)
    restored = source
    for change in reversed(changes):
        if restored.count(change['after']) != 1:
            raise RuntimeError('inverse unique new Source block required')
        restored = restored.replace(change['after'], change['before'], 1)
    if restored.encode() != source_bytes or max(map(len, source.splitlines())) > 132:
        raise RuntimeError('whole Source inverse/Fortran line bound')
    if source.count('ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1') != 82:
        raise RuntimeError('all original82 exact failed-site events retained')
    OUT.mkdir()
    new_pin = write_new('SPOR64_BOOT_BIND64.f90', source.encode())
    inverse = dict(schema='COMPLETE_BIND82_TO_FAILED_PHYS_INVENTORY_SOURCE_WHOLE_BYTE_INVERSE_V1',
                   original_source_pin=source_pin, candidate_source_pin=new_pin,
                   changes=changes, whole_byte_inverse_exact=True,
                   original82_mapping_pin=predecessor_sf_pin)
    inverse_pin = write_new('COMPLETE_FAILED_PHYS_INVENTORY_DIAGNOSTIC_WHOLE_BYTE_INVERSE.json', encoded(inverse))
    selected70 = report['actual_ordered70_link_inputs']
    if len(selected70) != 70:
        raise RuntimeError('actual base ordered70')
    plan = dict(schema='SOURCE_ONLY_BIND64_FAILED_PHYS_GROUP_HEADER_INVENTORY_DIAGNOSTIC_PLAN_V1',
                source_only=True, compiled=False, numerical_executed=False,
                business_executed=False, files_deleted=False,
                diagnostic_source_pin=new_pin, predecessor_diagnostic_source_pin=source_pin,
                predecessor_Fortran_Source_freeze_pin=predecessor_sf_pin,
                complete_byte_inverse_pin=inverse_pin, original_schema_Source_pin=schema_pin,
                active_MCGASM8_Source_pin=producer_pin,
                actual_failed_prior_report_pin=report_pin,
                actual_failed_prior_post_review_pin=post_pin, actual_failed_prior_log_pin=log_pin,
                prior_sealed_summary_and_Source_not_modified=True,
                known_prior_parser_Source_defect=dict(actual_response_parent_original_line=168,
                     incorrect_parser_mirror_line=173, line173_is='NTOT0 finite check',
                     sealed_outcome=None, explicit_transparent_actual_post_evidence=True),
                only_replacement_zero_based_link_index=47,
                selected_actual_base_ordered70_paths=selected70,
                required_unchanged_indices=[37,40,49,57,68],
                all_other69_ordered_inputs_and_four_archives_must_be_exactly_retained=True,
                new_generated_module_must_be_whole_byte_equal_original_ABI=True,
                all_original_conditions_once_and_boolean_status_math_loops_assignments_thresholds_preserved=True,
                all_original82_failed_return_events_and_returns_preserved=True,
                failed_source_SITE=236, failed_caller_SITE=168,
                inventory_event_schema=EVENT_SCHEMA,
                inventory_event_order=['original_RESPONSE236_failure','begin','record*','end',
                    'original_SYSTEM168_failure','caller','original_READ97_failure',
                    'original_BOOTB466_failure','original_BOXX_plane1_status1_required8'],
                maximum_actual_inventory_records=64,
                exact_name_encoding='24 uppercase hexadecimal characters for all12 original LCM name bytes',
                actual_record_content_not_read_or_dumped=True,
                complete_and_truncated_are_observed_flags_not_assumed=True,
                source_possible_native_extra_keys=['AXMAT-V64','PJJ64$MCCG'],
                actual_group_index_and_names_not_yet_observed=True,
                native_schema_gate_not_changed=True,
                original_caps=report['original_caps'],
                original_resource_snapshot_not_a_new_current_budget=True,
                future_current_budget_pin=None,future_cleanup_manifest_pin=None,
                future_actual_object_pin=None,future_actual_mod_pin=None,
                future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,
                future_actual_group_index=None,future_actual_inventory=None,
                physics_qualified=False,engineering_qualified=False)
    plan_pin = write_new('SOURCE_ONLY_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_PLAN.json', encoded(plan))
    ready = dict(schema='PREPARED_BIND64_FAILED_PHYS_INVENTORY_SOURCE_ONLY_V1',
                 status='PASS_SOURCE_ONLY_PREPARATION_NO_COMPILE_OR_BUSINESS',failure=None,
                 source_only=True,compiled=False,numerical_executed=False,business_executed=False,
                 files_deleted=False,preparer_pin=read_pin(__file__)[1],
                 candidate_source_pin=new_pin,complete_byte_inverse_pin=inverse_pin,
                 control_plan_pin=plan_pin,whole_byte_inverse_exact=True,
                 future_actual_object_pin=None,future_actual_module_pin=None,
                 future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None)
    ready_pin = write_new('READY.json', encoded(ready))
    dfd=os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    print(json.dumps(dict(status=ready['status'],source_only=True,compiled=False,
                         numerical_executed=False,package=str(OUT),
                         source_pin=new_pin,inverse_pin=inverse_pin,plan_pin=plan_pin,
                         ready_pin=ready_pin),ensure_ascii=False))


if __name__ == '__main__':
    main()

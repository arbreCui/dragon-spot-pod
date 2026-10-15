"""Draft complete B2 extraction algorithm; no executable owning host is bound.

Root must supply frozen original budget/metadata callbacks after the current
epoch bridge and exact presence archive/retirement close. Nothing runs on import.
The physical walker is a whole-byte Source copy, with no record/path filtering.
"""
import os
from pathlib import Path

REQUEST_SCHEMA = 'CURRENT_NATIVEWARM_B2_COMPLETE_READONLY_EXTRACTION_REQUEST_V1'
REQUIRED_OPS = ('require', 'check', 'pin', 'current7', 'identity',
                'module', 'write', 'admit_B2_metadata_and_original_owning_guard')


def extract_complete_B2(request, output, budget, source_table, ops):
    """Future Root-only child, called by a separately frozen owning host."""
    assert all(callable(ops.get(k)) for k in REQUIRED_OPS)
    require = ops['require']
    require(request['schema'] == REQUEST_SCHEMA, 'one complete B2 extraction')
    require(request['root_owning_runtime_Source_binding'] is not None and
            request['actual_B2_current_epoch_bridge_report_pin'] is not None and
            request['actual_B2_current_epoch_bridge_post_pin'] is not None and
            request['actual_presence_archive_post_pin'] is not None and
            request['actual_presence_retirement_post_pin'] is not None and
            request['actual_latest_complete_prefix_plan_pin'] is not None,
            'all actual current epoch, storage and owning prerequisites required')
    ops['admit_B2_metadata_and_original_owning_guard'](request, budget.check)
    budget.check()
    expected = request['actual_current_epoch_B2_archive_pin']
    require(type(expected) is dict, 'future current-epoch B2 PF remains NULL')
    ops['check'](expected, budget.check)
    out = Path(output)
    require(out == Path(request['child_output_directory']) and out.is_dir() and
            not any(out.iterdir()), 'fresh literal owning extraction directory')
    native = ops['module']('complete_B2_original_physical_walker',
        'complete_observed_old_post_final_XSM_extractor.UNREADY.py',
        source_table, budget.check)
    index = out / 'complete_native_original_path_index.sqlite'
    payload = out / 'complete_native_original_value_bytes.bin'
    physical_path = out / 'complete_native_physical_directory_slots.jsonl'
    rows = native.DiskRecords(index)
    try:
        with Path(expected['path']).open('rb') as stream, \
                physical_path.open('x') as physical, payload.open('xb') as pool:
            require(ops['identity'](os.fstat(stream.fileno())) == expected['identity'],
                    'exact current-epoch opened B2 inode')
            tree = native.XSM(native.ReadOnlyFileBytes(stream), physical,
                              pool, budget, rows)
            tree.walk()  # Full physical root, including unrelated containers.
            rows.checkpoint()
            handle = rows.get(('MICROLIB2', 1, 'MACROLIB'))
            require(handle is not None and handle['kind'] == 0,
                    'exact physical MICROLIB2 list1 MACROLIB directory')
            complete_macro_count = 0
            for row in rows.iter_rows():
                budget.check()
                if row['path'][:3] == ['MICROLIB2', 1, 'MACROLIB']:
                    complete_macro_count += 1
            require(complete_macro_count == 19620,
                    'complete original MACROLIB typed root and all records')
            physical.flush(); os.fsync(physical.fileno())
            pool.flush(); os.fsync(pool.fileno())
            require(ops['identity'](os.fstat(stream.fileno())) == expected['identity'],
                    'current-epoch B2 unchanged throughout full physical walk')
            facts = dict(complete_physical_tree_records=len(rows),
                complete_directories=tree.directory_count,
                complete_extents=tree.extent_count,
                complete_MICROLIB2_list1_MACROLIB_records=complete_macro_count)
    finally:
        rows.close()
    ops['check'](expected, budget.check)
    # Both original physical/API ordinals, every typed path and complete original
    # record metadata are durable SQL columns. No duplicate JSONL is needed to
    # preserve the same information, and no macro-only tree is substituted.
    artifacts = [ops['pin'](p, budget.check) for p in (index, payload, physical_path)]
    report = dict(schema='ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_V1',
        status='COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_READONLY_EVIDENCE_ONLY',
        actual_current_epoch_B2_archive_pin=expected,
        historical_B2_archive_pin=request['historical_B2_archive_pin'],
        actual_B2_current_epoch_bridge_report_pin=request['actual_B2_current_epoch_bridge_report_pin'],
        actual_B2_lineage_metadata_audit_pin=request['actual_B2_lineage_metadata_audit_pin'],
        paired_SQLite_pin=artifacts[0], paired_original_pool_pin=artifacts[1],
        complete_physical_directory_slots_pin=artifacts[2],
        all_output_file_pins=artifacts,
        entire_original_physical_tree_walked=True,
        all_original_types_counts_words_and_physical_API_orders_saved=True,
        unrelated_original_containers_retained=True,
        full_original_scope_not_replaced_by_19249_constructed_fields=True,
        native_library_or_solver_invoked=False, ASCII_used_or_invented=False,
        original_RAM_bits_qualified=False, physics_qualified=False,
        AAA_qualified=False, ABA_admitted=False, goal_complete=False, **facts)
    path = out / 'ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_REPORT.json'
    ops['write'](path, report)
    budget.check()
    return path


if __name__ == '__main__':
    raise SystemExit('UNREADY Source draft: no genuine owning host or actual admission is bound; no payload read')

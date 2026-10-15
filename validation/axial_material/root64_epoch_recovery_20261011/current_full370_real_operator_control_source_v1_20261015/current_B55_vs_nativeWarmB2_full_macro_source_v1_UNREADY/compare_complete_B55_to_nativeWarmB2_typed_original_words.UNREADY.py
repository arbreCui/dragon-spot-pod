"""Draft single-B2 adaptation of the complete saved three-macro comparator.

Exact typed path inventories and all original words remain mandatory. The AAA
three original producers are untouched. No saved pair or owning host is bound.
"""
import itertools
import json
import os
from pathlib import Path

REQUEST_SCHEMA = 'CURRENT_B55_TO_NATIVEWARM_B2_COMPLETE_TYPED_WORD_COMPARISON_REQUEST_V1'


def under(saved, prefix):
    for value in saved.iter_all():
        if tuple(value['record']['path'][:len(prefix)]) == prefix:
            yield value


def keys(saved, prefix, adapter, require):
    result = set()
    for value in under(saved, prefix):
        original = value['record']['path']
        canonical = original if prefix == ('MACROLIB',) else original[2:]
        require(canonical[:1] == ['MACROLIB'],
                'only MICROLIB2 integer1 full MACROLIB prefix normalized')
        key = adapter.path_key(canonical)
        require(key not in result, 'unique canonical typed full path')
        result.add(key)
    return result


def compare_complete_B55_B2(request, output, budget, source_table, ops):
    """Future owning child; no top-level data access and no CLI admission yet."""
    require = ops['require']
    require(request['schema'] == REQUEST_SCHEMA and
            request['root_owning_runtime_Source_binding'] is not None and
            request['actual_B2_complete_extraction_report_pin'] is not None and
            request['actual_B2_complete_extraction_post_pin'] is not None,
            'separate actual full B2 extraction and genuine owning guard required')
    ops['admit_B2_metadata_and_original_owning_guard'](request, budget.check)
    adapter = ops['module']('complete_B2_saved_native_input_adapter',
        'saved_native_data_access_adapter.UNREADY.py', source_table, budget.check)
    out = Path(output)
    require(out == Path(request['child_output_directory']) and out.is_dir() and
            not any(out.iterdir()), 'fresh separate owning comparison directory')
    pair = request['observed_B55_pair']; row = request['native_B2_pair']
    require(type(row) is dict and row['archive_pin'] ==
            request['actual_current_epoch_B2_archive_pin'], 'actual B2 pair only')
    ops['current7'](row['archive_pin'])
    temp = out / 'sqlite_temp'; temp.mkdir()
    saved = adapter.SavedNativeInput(pair['sqlite_pin'], pair['native_pool_pin'],
                                    temp, budget.check)
    try:
        observed_keys = keys(saved, ('MACROLIB',), adapter, require)
        require(len(observed_keys) == 19620,
                'all original 19620 typed records including root')
        native = adapter.SavedNativeInput(row['sqlite_pin'], row['native_pool_pin'],
                                         temp, budget.check)
        try:
            native_keys = keys(native, ('MICROLIB2', 1, 'MACROLIB'), adapter, require)
            require(native_keys == observed_keys,
                    'complete bidirectional typed inventories, no dropped/invented path')
            count = words = word_mismatches = metadata_mismatches = 0
            detail = out / 'B55_nativeWarmB2_complete_canonical_macro_comparison.jsonl'
            with detail.open('x') as output_stream:
                # Keep observed physical/API order. Typed lookup never relies on
                # positional order or sorts/rewrites either original archive.
                for value in under(saved, ('MACROLIB',)):
                    budget.check(); a = value['record']
                    right_path = ['MICROLIB2', 1] + a['path']
                    b = native.row(right_path)
                    require(b is not None, 'exact typed full native path lookup')
                    right_info = native.db.execute(
                        'SELECT ordinal,api_key FROM records WHERE key=?',
                        (adapter.path_key(right_path),)).fetchone()
                    require(right_info is not None, 'physical/API order retained')
                    meta = a['path_types'] == b['path_types'][2:] and all(
                        a[k] == b[k] for k in ('kind', 'declared_count', 'original_word_count'))
                    nwords = ndiff = 0
                    for aa, bb in itertools.zip_longest(saved.iter_raw(a),
                            native.iter_raw(b), fillvalue=b''):
                        budget.check()
                        nwords += max(len(aa), len(bb)) // 4
                        ndiff += sum(aa[i:i+4] != bb[i:i+4]
                            for i in range(0, max(len(aa), len(bb)), 4))
                    count += 1; words += nwords; word_mismatches += ndiff
                    metadata_mismatches += int(not meta)
                    item = dict(canonical_path=a['path'], kind=a['kind'],
                        declared_count=a['declared_count'],
                        original_word_count=a['original_word_count'],
                        metadata_equal=meta, raw_word_mismatches=ndiff,
                        compared_words=nwords,
                        observation_payload_SHA=a['native_payload_sha256'],
                        archive_payload_SHA=b['native_payload_sha256'],
                        original_observation_ordinal=value['physical_ordinal'],
                        original_observation_api_key=value['api_key'],
                        original_archive_ordinal=right_info[0],
                        original_archive_api_key=right_info[1])
                    output_stream.write(json.dumps(item, separators=(',', ':'),
                                                   allow_nan=False) + '\n')
                output_stream.flush(); os.fsync(output_stream.fileno())
            require(count == len(observed_keys) == len(native_keys) == 19620,
                    'every original macro record compared once including root')
        finally:
            native.close()
    finally:
        saved.close()
    ops['current7'](row['archive_pin'])
    report = dict(schema='ACTUAL_B55_NATIVEWARM_B2_FULL_TYPED_PATH_RAW_WORD_COMPARISON_V1',
        status='ACTUAL_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_ONLY',
        observed_B55_pair=pair, native_B2_pair=row,
        actual_B2_complete_extraction_report_pin=request['actual_B2_complete_extraction_report_pin'],
        actual_B2_complete_extraction_post_pin=request['actual_B2_complete_extraction_post_pin'],
        actual_B2_lineage_metadata_audit_pin=request['actual_B2_lineage_metadata_audit_pin'],
        compared_all_macro_records=count, compared_original_payload_words=words,
        raw_word_mismatches=word_mismatches, metadata_mismatches=metadata_mismatches,
        path_sets_equal=True, all_original_records_and_typed_root_preserved=True,
        original_archive_not_redecoded=True, original_orders_not_sorted_or_rewritten=True,
        comparison_contract='EXACT_TYPED_FULL_PATH_KIND_COUNT_WORDS_AND_ALL_RAW_BYTES',
        detail_pin=ops['pin'](detail, budget.check),
        constructed_19249_field_subset_used=False,
        original_AAA_three_producers_replaced=False,
        physics_qualified=False, AAA_qualified=False, ABA_admitted=False,
        goal_complete=False)
    path = out / 'ACTUAL_B55_NATIVEWARM_B2_COMPLETE_TYPED_MACRO_COMPARISON_REPORT.json'
    ops['write'](path, report); budget.check()
    return path


if __name__ == '__main__':
    raise SystemExit('UNREADY Source draft: no actual B2 saved pair or genuine owning host is bound; no payload read')

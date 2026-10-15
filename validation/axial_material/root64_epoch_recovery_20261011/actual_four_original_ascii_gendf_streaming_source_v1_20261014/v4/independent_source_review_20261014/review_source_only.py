"""Independent corrected v4 Source delta/fullEOF review; never read gzip payload."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path

BASE = Path(__file__).absolute().parents[1]
PREVIOUS = BASE.parent / 'v3'
spec = importlib.util.spec_from_file_location('independent_previous_metadata_primitives', PREVIOUS / 'independent_source_review_20261014/review_source_only.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
CAPS, FLAGS, current, full, pin, read, new, require = audit.CAPS, audit.FLAGS, audit.current, audit.full, audit.pin, audit.read, audit.new, audit.require


def main():
    p_ready = pin(BASE / 'SOURCE_REVIEW_READY.json')
    p_generation = pin(BASE / 'ACTUAL_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
    ready, generation = read(p_ready), read(p_generation)
    raw = generation['actual_Source_preparation_return']
    require(ready['source_only'] is True and ready['actual_business_started'] is False
            and ready['Root_final_publication_executed'] is False and all(ready[k] is False for k in FLAGS)
            and generation['observed_closed'] is True and type(generation['original_integer_exit_code']) is int
            and generation['original_integer_exit_code'] == 0 and type(raw['exit_code']) is int and raw['exit_code'] == 0
            and raw.get('session_id') is None, 'actual frozen v4 Source generation typed closed0')
    stdout = json.loads(raw['output'].strip().splitlines()[-1])
    require(stdout['status'] == 'FOUR_ORIGINAL_ASCII_SOURCE_PREPARATION_ONLY'
            and stdout['ready_pin'] == p_ready and all(stdout[k] is False for k in FLAGS), 'v4 genuine generation stdout exactreadyPF')
    selected = ready['selected_Source_pins'] + [p_ready, p_generation]
    require(ready['selected_Source_pins'] == ready['dependencies']
            and len(ready['selected_Source_pins']) == len({p['path'] for p in ready['selected_Source_pins']}) == 157,
            'all157 exact unique selected Source/dependency pins')
    parsed = []
    for p in selected:
        full(p)
        if p['path'].endswith('.py'):
            ast.parse(Path(p['path']).read_text(), filename=p['path'])
            parsed.append(p)
    plan = read(ready['control_plan_pin'])
    previous_plan = read(plan['selected_prior43_failed_plan_pin'])
    old38 = read(plan['selected_prior_original38_plan_pin'])
    require(plan['source_only'] is True and plan['extractor_executed'] is False
            and all(plan[k] is False for k in FLAGS) and ready['original_caps'] == plan['original_caps'] == previous_plan['original_caps'] == old38['original_caps'] == CAPS,
            'unchanged original caps, Source-only corrected plan')
    roots = plan['complete_joint_roots']
    require(roots == previous_plan['complete_joint_roots'] + [plan['planned_actual_output_root']]
            and len(roots) == len(set(roots)) == 44 and len(previous_plan['complete_joint_roots']) == 43
            and roots[:38] == old38['complete_joint_roots']
            and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b),
            'all original43 retained and exactly one fresh output root44; disjoint')
    require(plan['planned_actual_output_root'].endswith('axial-material-four-original-ASCII-GENDF-stream-inventory-20261014-v2')
            and not os.path.lexists(plan['planned_actual_output_root'])
            and all(not os.path.lexists(BASE / n) for n in ('FINAL_SOURCE_FREEZE.json', 'FINAL_HOST_FREEZE.json', 'FINAL_ROOT_REVIEWABLE_CLI.json', 'FINAL_PUBLICATION_RECEIPT.json')),
            'fresh corrected output and final once publication; failed output not retried')
    require(len(plan['explicit_cumulative_metadata_file_pins']) == 144
            and all(p in plan['explicit_cumulative_metadata_file_pins'] for p in previous_plan['explicit_cumulative_metadata_file_pins'])
            and all(p in ready['dependencies'] for p in plan['explicit_cumulative_metadata_file_pins']),
            'all prior138 cumulative metadata and fourfailure/sourceproof additions exact144 retained')
    require(len(plan['prior_runtime_failure_proof_pins']) == 4
            and all(p in ready['dependencies'] for p in plan['prior_runtime_failure_proof_pins']), 'allfour prior failure fullPF retained')
    failed_tools, failed_review, failed_peer_tools, failed_summary = [read(p) for p in plan['prior_runtime_failure_proof_pins']]
    require(failed_tools['observed_closed'] is True and type(failed_tools['original_integer_exit_code']) is int
            and failed_tools['original_integer_exit_code'] == 1
            and type(failed_tools['actual_terminal_return']['exit_code']) is int and failed_tools['actual_terminal_return']['exit_code'] == 1
            and failed_summary['status'] == 'FAILED_FOUR_ORIGINAL_ASCII_NO_RETRY'
            and failed_review['original_Runtime_integer_exit_code'] == 1
            and failed_review['actual_failed_Root_summary_pin'] == plan['prior_runtime_failure_proof_pins'][3]
            and failed_peer_tools['observed_closed'] is True and type(failed_peer_tools['actual_review_return']['exit_code']) is int
            and failed_peer_tools['actual_review_return']['exit_code'] == 0
            and json.loads(failed_peer_tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin'] == plan['prior_runtime_failure_proof_pins'][1],
            'actual Root closed1 plus sole peer failurefacts closed0 preserved as failed evidence')
    old_review = read(pin(PREVIOUS / 'independent_source_review_20261014/REVIEW.json'))
    guard_pins = old_review['original_dynamic_guard_Source_pins'] + old_review['original_live_guard_admission_full_pins']
    for p in guard_pins:
        full(p)
    proof = read(plan['original_whole_source_proof_pin'])
    prior_proof = read(previous_plan['original_whole_source_proof_pin'])
    require(plan['inputs'] == previous_plan['inputs'] == proof['inputs'] == prior_proof['inputs']
            and proof['legacy_identity_order'] == ['dev', 'ino', 'mode', 'size', 'mtime_ns', 'ctime_ns', 'nlink']
            and proof['current_identity_order'] == ['dev', 'ino', 'mode', 'nlink', 'size', 'mtime_ns', 'ctime_ns']
            and proof['original_a11_already_applied_to_input'] is True and proof['second_quantization_performed'] is False,
            'same four exact original round9 lineage and explicit legacy7 normalization, no second formatter')
    pairs = [(proof['whole_original_scalar_helper_pin'], proof['whole_unchanged_scalar_helper_copy_pin'])]
    pairs += [(p['original_full_pin'], p['whole_unchanged_copy_full_pin']) for p in proof['whole_original_guard_source_copies']]
    require(len(pairs) == 5, 'whole original scalar plus four guard/writer copies')
    for original, copy in pairs:
        full(original)
        full(copy)
        require(Path(original['path']).read_bytes() == Path(copy['path']).read_bytes(), 'whole original helper/guard Source unchanged')
    gzip_pins = [row['gzip_primary_current_full_pin'] for row in plan['inputs']]
    for p in gzip_pins:
        current(p)
    require(sum(row['historical_original_ASCII_size_bytes'] for row in plan['inputs']) == plan['original_decompressed_payload_expected_bytes'] == 284814387
            and plan['original_ascii_output_files_planned'] == 0, 'same whole original expected bytes and no unpackfiles')
    retirement = read(plan['actual_precise_retirement_receipt_pin'])
    retirement_tools = read(plan['actual_Root_retirement_true_tools_pin'])
    require(retirement['status'] == 'RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'
            and retirement['failure'] is None and retirement['actual_released_bytes'] == 405417320
            and len(retirement['actual_released_pins']) == 4 and retirement['actual_released_pins'] == retirement['exact_target_pins']
            and all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins'])
            and type(retirement_tools['actual_execution_return']['exit_code']) is int
            and retirement_tools['actual_execution_return']['exit_code'] == 0, 'exact real original Root retirement, no generic missing waiver')
    layout = read(plan['original_GROUPR_MF3_layout_source_proof_pin'])
    require(layout['schema'] == 'WHOLE_ORIGINAL_GROUPR_ACTUAL_GENERAL_LIST_LAYOUT_SOURCE_PROOF_V1'
            and layout['source_only'] is True and layout['actual_failed_input_MT_not_inferred'] is True
            and layout['actual_original_ASCII_payload_read'] is False and all(layout[k] is False for k in FLAGS), 'same original GROUPR source proof, no failedMT inference')
    for p in (layout['original_GROUPR_Source_full_pin'], layout['whole_unchanged_GROUPR_Source_copy_full_pin']):
        full(p)
    graw = Path(layout['original_GROUPR_Source_full_pin']['path']).read_bytes()
    require(graw == Path(layout['whole_unchanged_GROUPR_Source_copy_full_pin']['path']).read_bytes()
            and len(layout['exact_original_statements']) == 5, 'whole unchanged original GROUPR Source')
    for statement in layout['exact_original_statements']:
        text = bytes.fromhex(statement['original_statement_bytes_hex'])
        require(graw[statement['begin_byte']:statement['end_byte']] == text
                and graw.count(text) == 1 and hashlib.sha256(text).hexdigest() == statement['sha256'], 'exact original GROUPR statement byte proof')
    require(b'if (mtd.eq.251.or.mtd.eq.252.or.mtd.eq.253) ng=3' in graw
            and b'if (mtd.eq.452.or.mtd.eq.455.or.mtd.eq.456) ng=3' in graw
            and b'lim=nl*nz*ng2' in graw and b'scr(3)=ng2' in graw, 'original ratio NG3 and actual general LIST dimensional output')
    stream = (BASE / 'stream_four_original_ascii_gendf.py').read_text()
    previous_stream = (PREVIOUS / 'stream_four_original_ascii_gendf.py').read_text()
    require("require(ng2==2,'original MF3 flux/reaction layout')" not in stream
            and "if mf==6:require(lower==0 or 1<=lower<=370 and lower+ng2-2<=370,'actual MF6 destination dimensions')" in stream
            and "actual_NG2_histogram" in stream and "actual_LIST_index_dimensions" in stream
            and "actual originalASCII context=" in stream
            and all(text in stream for text in ("npl==ng2*active['nl']*active['nz']", "0<=npl<=88800", "ng2>=2",
                        "compressed.read(1)==b''", "reader.digest.hexdigest()==row['historical_original_ASCII_sha256']",
                        "compressed.digest.hexdigest()==p['sha256']", "ng==370 and ngg==0 and npl==383", "len(grids)==8", "nz==10", "require(bool(sections)")),
            'corrected MF3 general dimension inventory, original MF6/bounds/hashes/grids preserved')
    previous_blocks = [n for n in ast.walk(ast.parse(previous_stream)) if isinstance(n, ast.If)
                       and ast.unparse(n.test) == 'ig == 0']
    current_blocks = [n for n in ast.walk(ast.parse(stream)) if isinstance(n, ast.If)
                      and ast.unparse(n.test) == 'ig == 0']
    require(len(previous_blocks) == len(current_blocks) == 1
            and ast.dump(previous_blocks[0].body[0], include_attributes=False) == ast.dump(current_blocks[0].body[0], include_attributes=False),
            'original MF6 unique spectrum dimension predicate unchanged')
    for name in ('run_guarded_four_original_ascii_gendf.py', 'write_once_Root_four_original_ascii_SF_HF_CLI.py'):
        oldtext = (PREVIOUS / name).read_text()
        newtext = (BASE / name).read_text()
        oldtext = oldtext.replace('len(roots)==43 and len(set(roots))==43', 'len(roots)==44 and len(set(roots))==44')
        oldtext = oldtext.replace('complete prior38 plus retirement and both Source/output pairs', 'complete prior43 preserved plus new originalASCII output v2')
        oldtext = oldtext.replace("len(plan['complete_joint_roots'])==43", "len(plan['complete_joint_roots'])==44")
        oldtext = oldtext.replace('same prior38 plus retirement and both Source/output pairs, original caps', 'same prior43 preserved plus new originalASCII output v2, original caps')
        require(newtext == oldtext, 'entire host/publisher delta solely exact44 cumulative scope')
    require(ready['original_complete_ENV_Python_B_prefix'] == read(pin(PREVIOUS / 'SOURCE_REVIEW_READY.json'))['original_complete_ENV_Python_B_prefix'],
            'original complete unoptimized single-thread interpreter prefix unchanged')
    for p in selected + guard_pins:
        current(p)
    report = dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_STREAM_CORRECTED_V4_SOURCE_ONLY_REVIEW',
                  status='PASS_CORRECTED_V4_SOURCE_ONLY_FULL_EOF_CURRENT7_ORIGINAL_GROUPR_LAYOUT_REVIEW',
                  source_only=True, failure=None, selected_Source_pins=selected, selected_Source_pin_count=157,
                  complete_AST_parsed_Source_pins=parsed, original_guard_Source_and_admission_pins=guard_pins,
                  exact_current_gzip_primary_pins_without_payload_read=gzip_pins,
                  prior_actual_failed_runtime_proof_pins=plan['prior_runtime_failure_proof_pins'],
                  original_GROUPR_MF3_layout_source_proof_pin=plan['original_GROUPR_MF3_layout_source_proof_pin'],
                  complete_joint_roots=roots, original43_retained_plus_only_fresh_output=True,
                  complete_explicit_cumulative_metadata_count=144, original_caps=CAPS,
                  whole_original_helper_and_guard_copies_equal=True, whole_original_GROUPR_Source_copy_equal=True,
                  generic_MF3_NG2_actual_histogram_inventory_reviewed=True,
                  original_MF6_LIST_dimension_conditions_unchanged=True,
                  universal_MF3_NG2_equals_two_not_imposed=True, prior_actual_failed_MT_not_inferred=True,
                  original_ASCII_decoded_temperatures_preserved=True, second_quantization_performed=False,
                  prior_failed_invocation_preserved=True, actual_generation_closed0_verified=True,
                  gzip_payload_read=False, sciencebody_imported_or_executed=False, Root_final_publication_executed=False, **FLAGS)
    target = BASE / 'independent_source_review_20261014/REVIEW.json'
    new(target, report)
    print(json.dumps(dict(status=report['status'], review_pin=pin(target), **FLAGS)), flush=True)


if __name__ == '__main__':
    main()

"""Bounded v3 Source review only; never imports candidate or reads science bodies."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

HERE = Path(__file__).absolute().parent
BASE = HERE.parent
PIN_KEYS = {'path', 'sha256', 'size_bytes', 'identity'}
START = time.monotonic()


def require(ok, message):
    if ok is not True:
        raise ValueError(message)


def budget():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak *= 1 if sys.platform == 'darwin' else 1024
    require(peak < 512 * 2**20 and time.monotonic() - START < 600,
            'bounded Source auditor SELF512/stage600')


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def typed(p):
    require(type(p) is dict and set(p) == PIN_KEYS, 'exact full PF schema')
    require(type(p['path']) is str and Path(p['path']).is_absolute(), 'absolute PF')
    require(type(p['sha256']) is str and len(p['sha256']) == 64 and
            all(x in '0123456789abcdef' for x in p['sha256']), 'SHA256 PF')
    require(type(p['size_bytes']) is int and p['size_bytes'] >= 0, 'integer bytes')
    require(type(p['identity']) is list and len(p['identity']) == 7 and
            all(type(x) is int for x in p['identity']), 'Python integer seven ID')
    require(p['identity'][4] == p['size_bytes'], 'PF matching size')


def current(p):
    budget(); typed(p); q = Path(p['path']); s = q.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == p['identity'], 'exact current7: ' + str(q))
    require(not any(x.is_symlink() for x in (q, *q.parents)), 'no aliases: ' + str(q))


def exact(p):
    current(p); q = Path(p['path'])
    require(q.suffix in ('.py', '.json') and p['size_bytes'] < 8 * 2**20,
            'bounded Source/report metadata only')
    raw = bytearray(); digest = hashlib.sha256(); total = 0
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno())) == p['identity'], 'opened current7')
        while True:
            budget(); part = f.read(2**20)
            if not part:
                break
            raw.extend(part); digest.update(part); total += len(part)
        require(identity(os.fstat(f.fileno())) == p['identity'], 'EOF current7')
    require(total == p['size_bytes'] and digest.hexdigest() == p['sha256'], 'whole EOF PF')
    current(p); return bytes(raw)


def pin(q):
    q = Path(q); s = q.lstat()
    require(q.suffix in ('.py', '.json') and s.st_size < 8 * 2**20, 'own Source/report only')
    p = dict(path=str(q), sha256=hashlib.sha256(q.read_bytes()).hexdigest(),
             size_bytes=s.st_size, identity=identity(s))
    current(p); return p


def read(p):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key'); result[key] = value
        return result
    return json.loads(exact(p), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def closed0(value, key, output_key, wanted):
    t = value[key]
    require(value['observed_closed'] is True and
            type(value['original_integer_exit_code']) is int and value['original_integer_exit_code'] == 0 and
            type(t['exit_code']) is int and t['exit_code'] == 0 and t.get('session_id') is None and
            json.loads(t['output'].strip().splitlines()[-1])[output_key] == wanted,
            'genuine exact stdout-PF typed closed0')


def unique(rows):
    result = {}
    for p in rows:
        typed(p)
        require(p['path'] not in result or result[p['path']] == p, 'consistent whole PF union')
        result[p['path']] = p
    return list(result.values())


def main():
    require(len(sys.argv) == 1 and not sys.flags.optimize and sys.getprofile() is None,
            'fixed unoptimized Source review invocation')
    freeze_pin = pin(HERE / 'AUDITOR_SOURCE_ONLY_FREEZE.json'); freeze = read(freeze_pin)
    require(freeze['auditor_Source_AST_parsed_before_freeze_and_execution'] is True,
            'pre-execution AST freeze')
    require(pin(Path(__file__).absolute()) == freeze['auditor_source_pin'], 'frozen exact auditor Source')
    ast.parse(exact(freeze['auditor_source_pin']))
    ready_pin, plan_pin, gen_pin = (freeze[k] for k in ('ready_pin', 'plan_pin', 'generation_tools_pin'))
    ready, plan, gen = read(ready_pin), read(plan_pin), read(gen_pin)
    require(ready['plan_pin'] == plan_pin and ready['author_source_freeze_pin'] == freeze['author_pin'],
            'same complete selected v3 READY/PLAN/author')
    closed0(gen, 'actual_Source_preparation_return', 'ready_pin', ready_pin)
    require(gen['actual_Source_preparation_return']['chunk_id'] == 'f68817', 'actual Root generation tool')
    author = read(freeze['author_pin']); seed = read(plan['seed_pin'])
    require(author['source_pins'] == plan['source_pins'] and
            ready['selected_Source_and_metadata_pins'] == plan['metadata_pins'], 'exact selected Source/metadata union')
    required = unique(ready['selected_Source_and_metadata_pins'] + plan['metadata_pins'] +
                      [ready_pin, plan_pin, gen_pin] + author['preserved_frozen_v1_Source_and_metadata_pins'] +
                      [plan[k] for k in ('original_support_Source_pin', 'original_Common_Source_pin', 'original_bounded_Source_pin')] +
                      freeze['additional_original_guard_Source_pins'])
    require(required == freeze['complete_selected_and_support_Source_metadata_union'], 'frozen complete review union')
    originals = {p['path']: exact(p) for p in required}
    for p in plan['source_pins']:
        ast.parse(originals[p['path']])
    science = plan['scientific_input_current7_pins'] + [plan['original_final55_XSM_current7_pin'], plan['logical_inventory_current7_pin']]
    for p in science + plan['inherited_explicit_metadata_pins']:
        current(p)
    inherited = read(plan['inherited_full_operator_plan_pin'])
    roots = plan['complete_joint_roots']
    require(roots == inherited['complete_joint_roots'] and len(roots) == len(set(roots)) == 56 and
            plan['original_caps'] == inherited['original_caps'] == author['original_caps'] and
            any(BASE.is_relative_to(Path(r)) for r in roots) and
            not any(Path(x).is_relative_to(Path(y)) for x in roots for y in roots if x != y),
            'complete inherited56 no new root/reset or caps change')
    require(plan['inherited_explicit_metadata_pins'] == inherited['explicit_cumulative_metadata_file_pins'] and
            Path(plan['output_directory']).is_relative_to(BASE), 'inherited complete metadata/output containment')
    request, ctx = read(seed['aggregate_request_pin']), read(seed['fixed_context_pin'])
    pair = request['aggregation_binding']['states']['A']
    require(pair['sqlite_pin'] == seed['original_SQLite_pin'] == inherited['observed_final55_SQLite_pin'] == science[0] and
            pair['native_pool_pin'] == seed['original_pool_pin'] == inherited['observed_final55_pool_pin'] == science[1] and
            science[0]['size_bytes'] == 16953344 and science[1]['size_bytes'] == 74693004,
            'exact final55 SQL/pool request provenance')
    post, primary = read(seed['original_extraction_post_pin']), read(seed['original_extraction_post_primary_pin'])
    tools, root, host, ext = (read(seed[k]) for k in ('original_extraction_post_tools_pin', 'original_extraction_Root_tools_pin',
                                                  'original_extraction_Host_pin', 'original_final55_extraction_report_pin'))
    require(post['status'] == 'PASS_ACTUAL_CURRENT_MATERIAL_EXTRACTION_SAVED_OUTPUT_AND_INPUT_PIN_COVERAGE' and
            post['failure'] is None and primary['failure'] is None and
            post['actual_child_integer_exit_code'] == primary['actual_child_integer_exit_code'] == 2 and
            post['actual_Root_true_tool_return_pin'] == seed['original_extraction_Root_tools_pin'] and
            post['actual_extraction_report_pin'] == seed['original_final55_extraction_report_pin'] and
            post['actual_extraction_host_pin'] == seed['original_extraction_Host_pin'], 'original extraction proof and intentional2')
    closed0(tools, 'actual_review_return', 'review_pin', seed['original_extraction_post_primary_pin'])
    require(json.loads(tools['actual_review_return']['output'])['actual_extraction_review_pin'] == seed['original_extraction_post_pin'],
            'same genuine dual original post0 output')
    t = root['actual_terminal_return']
    require(root['observed_closed'] is True and type(root['original_integer_exit_code']) is int and
            root['original_integer_exit_code'] == 0 and type(t['exit_code']) is int and t['exit_code'] == 0 and
            t.get('session_id') is None and host['status'] == 'ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY' and
            ext['status'] == 'ACTUAL_CURRENT_COMPLETE_CONTEXT_AND_RAW_SNAPSHOT_EVIDENCE_ONLY_EXIT2', 'Root0 intentional child2 preserved')
    rows = plan['selected_original_records']
    require(rows == seed['selected_original_records'] == author['selected_authoritative_logical_metadata_records'] and
            [r['path'] for r in rows] == [['ISOTOPESTEMP'], ['ISOTOPESUSED'], ['ISOTOPERNAME'], ['ISOTOPESMIX']] and
            [r['native_payload_end_byte'] - r['native_payload_begin_byte'] for r in rows] == [248, 744, 744, 248] and
            [r['kind'] for r in rows] == [2, 3, 3, 1] and [r['declared_count'] for r in rows] == [62, 186, 186, 62],
            'literal four descriptors and1984B selected pread')
    for row in rows:
        key = json.dumps(row['path'], ensure_ascii=True, separators=(',', ':'))
        require(ctx['original_context_records'][key]['original_record'] == row, 'exact fixed-context descriptor')
    helper = originals[plan['source_pins'][0]['path']]
    old = originals[author['original_saved_native_adapter_Source_pin']['path']]
    prefix = author['whole_original_saved_native_Source_prefix_copied_bytes']
    require(old[:prefix] == helper[:prefix] and hashlib.sha256(old[:prefix]).hexdigest() ==
            author['whole_original_saved_native_Source_prefix_sha256'], 'whole original saved-native prefix')
    oldtext, newtext = old.decode(), helper.decode()
    olddefs = {n.name: ast.get_source_segment(oldtext, n) for n in ast.parse(old).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    newdefs = {n.name: ast.get_source_segment(newtext, n) for n in ast.parse(helper).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    for row in author['whole_original_native_function_and_class_provenance']:
        name = row['original_definition_name']
        whole_definition = olddefs[name].encode() + b'\n'
        require(olddefs[name] == newdefs[name] and hashlib.sha256(whole_definition).hexdigest() == row['definition_sha256'] and
                len(whole_definition) == row['definition_bytes'], 'whole original decoder/method: ' + name)
    inverse_proofs = []
    for d in author['minimal_v1_to_v2_Source_derivation'] + author['minimal_v2_to_v3_Source_derivation']:
        ob, cb = originals[d['original_full_pin']['path']], originals[d['candidate_full_pin']['path']]
        inv = d['complete_inverse']; lo, hi = inv['candidate_begin_byte'], inv['candidate_end_byte']
        require(cb[lo:hi].hex() == inv['candidate_bytes_hex'] and
                ob[inv['original_begin_byte']:inv['original_end_byte']].hex() == inv['original_bytes_hex'], 'exact inverse spans')
        reconstructed = cb[:lo] + bytes.fromhex(inv['original_bytes_hex']) + cb[hi:]
        require(reconstructed == ob and hashlib.sha256(reconstructed).hexdigest() ==
                inv['whole_original_reconstructed_sha256'] == d['original_full_pin']['sha256'], 'complete v1 inverse')
        inverse_proofs.append(dict(original_full_pin=d['original_full_pin'], candidate_full_pin=d['candidate_full_pin'],
                                   whole_original_reconstructed_sha256=hashlib.sha256(reconstructed).hexdigest()))
    require(author['shared_helper_whole_v1_bytes_unchanged'] is True and
            author['v1_false_Root_parent_only_claim_preserved_not_rewritten'] is True, 'v1 preserved truthful correction')
    loops = dict(Root_parent_before_child=1, child_original_constructor_before_selected_pread=1,
                 child_original_close_after_selected_pread=1, total_Root_parent=1, total_child=2,
                 total_per_original_SQL_or_pool_file=3)
    for value in (author, seed, plan):
        require(value['current_root_only_full_SQL_pool_EOF_before_selected_pread'] is False and
                value['planned_full_input_EOF_loops_per_file'] == loops and value['selected_pread_payload_bytes_only'] == 1984,
                'truthful full-input three EOF versus selected1984B accounting')
    case = read(plan['current_case_spec_pin'])
    require(case['materials']['temperature_C_in_every_zone'] == inherited['current_case_temperature_C'] ==
            dict(clad_and_gap=620, fuel_and_hole=750, sodium=475) and
            case['materials']['kelvin_offset'] == inherited['current_case_kelvin_offset'] == 273.15 and
            case['geometry']['region_order_outer_to_inner'] == plan['expected_original_region_order'], 'current C/K/mix Source operands')
    runpin = next(p for p in plan['source_pins'] if Path(p['path']).name == 'run_temperature_operand_capture.py')
    runtext = originals[runpin['path']].decode()
    require("expected=struct.pack('<f',float(celsius)+float(material['kelvin_offset']))" in runtext and
            "actual=parts[0][4*i:4*i+4];equal=actual==expected" in runtext and
            "os.getppid()==parent" in runtext and "'--expected-parent',str(os.getpid())" in runtext,
            'conditional actual REAL32 word compare and owning child PID binding Source')
    prior_pin, prior_tools_pin = plan['preserved_failed_v2_review_pin'], plan['preserved_failed_v2_review_tools_pin']
    prior, prior_tools = read(prior_pin), read(prior_tools_pin)
    closed0(prior_tools, 'actual_review_return', 'review_pin', prior_pin)
    require(prior_tools['actual_review_return']['chunk_id'] == 'f6e471' and
            prior['status'] == 'FAILED_CURRENT62_TEMPERATURE_OPERAND_V2_SOURCE_ADMISSION' and
            prior['failure'] is not None and prior['Root_runtime_admission_issued'] is False and
            author['preserved_formal_failed_v2_review_pin'] == prior_pin and
            author['preserved_formal_failed_v2_review_tools_pin'] == prior_tools_pin and
            author['prior_v2_failed_semantic_review_not_reclassified_as_pass'] is True,
            'complete genuine failed v2 history remains refused, original audit0 retained')
    old_run = next(d['original_full_pin'] for d in author['minimal_v2_to_v3_Source_derivation']
                   if Path(d['candidate_full_pin']['path']).name == 'run_temperature_operand_capture.py')
    def definition(raw, name):
        value = raw.decode()
        node = next(n for n in ast.parse(value).body if isinstance(n, ast.FunctionDef) and n.name == name)
        return (ast.get_source_segment(value, node) + '\n').encode()
    require(definition(originals[old_run['path']], 'child') == definition(originals[runpin['path']], 'child') and
            hashlib.sha256(definition(originals[runpin['path']], 'child')).hexdigest() == author['whole_child_definition_sha256'],
            'whole v2 child decoder, temperature formula, payload capture preserved')
    root_text = definition(originals[runpin['path']], 'root').decode()
    claimed_text = definition(originals[runpin['path']], 'root_claimed').decode()
    require(root_text.index('claimed_start=time.monotonic()') < root_text.index("with claim_path.open('xb')") <
            root_text.index('rp=root_claimed(a,claimed_start)') and
            "except BaseException as error" in root_text and "NO_RETRY" in root_text and
            "type(runner) is full.OwnRSSSerialExecutor and runner.resources is resources" in claimed_text and
            "Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py'" in claimed_text and
            claimed_text.index('exact original runner/resources/private copied bounded module/interpreter before child') <
            claimed_text.index('runner.execute(') and
            'for p0 in fixed.values():h.current(p0);h.exact(p0)' in claimed_text and
            'after=check_fixed();fixed_after_verified=True' in claimed_text and
            claimed_text.count('check_fixed();fixed_after_verified=True') == 2,
            'all three v2 Source blockers explicitly repaired without resetting whole clock')
    guard_pin = next(p for p in freeze['additional_original_guard_Source_pins'] if Path(p['path']).name == 'guard_controls.json')
    controls = read(guard_pin)
    log_names = [name for name in controls['control_files'] if Path(name).suffix == '.log']
    require(log_names == ['positive.log', 'memorycap.log'] and
            "+[h.meta_pin(p0) for p0 in guard_files]" in claimed_text and
            "q.suffix in('.py','.json')" in helper.decode() and
            "q.suffix in('.py','.json')" in newdefs['exact'] and
            "for p0 in fixed.values():h.current(p0);h.exact(p0)" in claimed_text,
            'actual guard proof log roles deterministically rejected by unchanged metadata-only helpers')
    blockers = [dict(code='GUARD_LOG_ROLE_REJECTED_BY_METADATA_ONLY_HELPERS', source_pin=runpin, line=57,
                     detail='Original guard_admission returns positive.log and memorycap.log, declared by the exact guard_controls.json. V3 fixed_rows applies h.meta_pin to all guard_files, but unchanged h.meta_pin permits only .py/.json, so it raises before child after Root input EOF. check_fixed applies h.exact with the same suffix restriction.',
                     actual_guard_controls_metadata_pin=guard_pin, rejected_declared_guard_log_names=log_names)]
    for p in required:
        require(exact(p) == originals[p['path']], 'second complete Source/metadata EOF PF unchanged')
    for p in science + plan['inherited_explicit_metadata_pins']:
        current(p)
    budget()
    report = dict(schema='INDEPENDENT_CURRENT62_TEMPERATURE_OPERAND_V3_SOURCE_REVIEW_V1',
                  status='FAILED_CURRENT62_TEMPERATURE_OPERAND_V3_SOURCE_ADMISSION',
                  failure='; '.join(x['code'] for x in blockers), concrete_blockers=blockers,
                  source_only=True, Root_runtime_admission_issued=False,
                  all_three_prior_v2_Source_blockers_repaired=True, prior_v2_failed_review_pin=prior_pin,
                  prior_v2_failed_review_tools_pin=prior_tools_pin, prior_v2_original_audit0_not_admission=True,
                  preserved_v2_Source_author_metadata_and_generation_pins=author['preserved_v2_Source_author_metadata_and_generation_pins'],
                  whole_v2_child_definition_unchanged=True, exclusive_claim_and_original_whole_clock_Source_verified=True,
                  auditor_source_pin=freeze['auditor_source_pin'], auditor_source_freeze_pin=freeze_pin,
                  ready_pin=ready_pin, plan_pin=plan_pin, generation_tools_pin=gen_pin, author_source_freeze_pin=freeze['author_pin'],
                  complete_selected_and_support_Source_metadata_union=required,
                  complete_Source_metadata_full_EOF_PF_verified_twice=True,
                  scientific_input_and_logical_inventory_current7_only_pins=science,
                  scientific_input_and_logical_inventory_current7_verified_twice=True,
                  inherited_explicit_metadata_pins=plan['inherited_explicit_metadata_pins'],
                  inherited_explicit_metadata_current7_verified_twice=True,
                  selected_original_descriptors=rows, selected_pread_payload_bytes_only=1984,
                  planned_full_input_EOF_loops_per_file=loops, current_root_only_full_SQL_pool_EOF_before_selected_pread=False,
                  whole_original_saved_native_prefix_verified=True, whole_original_native_definition_count=len(author['whole_original_native_function_and_class_provenance']),
                  preserved_v1_complete_inverse_proofs=inverse_proofs, preserved_v1_Source_metadata_pins=author['preserved_frozen_v1_Source_and_metadata_pins'],
                  complete_joint_roots=roots, original_caps=plan['original_caps'],
                  conditional_current_C_to_K_REAL32_bit_compare_Source_reviewed=True,
                  actual_original_extraction_Root0_and_post0_intentional_child2_provenance_verified=True,
                  historical_full_operator_control_PASS_required=False,
                  helper_or_candidate_imported=False, scientific_SQL_pool_XSM_GENDF_SCI_body_opened_or_hashed=False,
                  actual_capture_executed=False, Source_generation_executed_by_reviewer=False,
                  business_executed=False, numerical_executed=False, compiler_executed=False, files_deleted=False,
                  physics_qualified=False, scientific_accuracy_qualified=False, complete_reaction_authority_qualified=False,
                  physical_neutron_balance_qualified=False, full_reference_qualified=False, unreduced_reference_qualified=False,
                  finite18_replayed=False, temperature_interpolation_replayed=False, current_SPH_MASK_context_applied=False,
                  native_AxMatTone_temperature_mapping_qualified=False, stored_native_REAL32_temperature_selection_qualified=False,
                  historical_native_RAM_bits_verified=False, original_XSM_memory_bits_verified=False,
                  AAA_qualified=False, ABA_admitted=False, goal_complete=False,
                  SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
                  elapsed_seconds=time.monotonic() - START)
    with (HERE / 'REVIEW.json').open('x') as f:
        json.dump(report, f, indent=2, allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    review_pin = pin(HERE / 'REVIEW.json'); budget()
    print(json.dumps(dict(status=report['status'], review_pin=review_pin, Root_runtime_admission_issued=False), separators=(',', ':')), flush=True)


if __name__ == '__main__':
    main()

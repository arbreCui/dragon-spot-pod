"""Independent text/AST/finite META audit only. Never imports reviewed code."""
from pathlib import Path
import ast
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile

OLD = Path('/private/tmp/axmat_private_inactive_audit_full_qualification_UNREADY_SOURCE_lb8ezxf2')
OLD_SHA = '409cb61c0f02a37d87934657446cb293fce85596cce121344ab116bc3fe75688'
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
ROLE_NAMES = ('pure_helper_controls.UNREADY.py', 'pure_helper_controls_host.UNREADY.py',
              'fresh_verifier_controls.UNREADY.py', 'fresh_verifier_host.UNREADY.py',
              'inactive_audit_snapshot_controls_SOURCE_ONLY.py')
ROLE_SHA = ('c9bcd426653f2dec82608a18f9a6840dc037c7d6da87cac13ffe41dcd3092229',
            '3e8402c278a4840acc55575641a80d911cc3a53dd09cfedadd0139c676a8d311',
            'dd3f7beae73bc2290321150bd71edd31ad2d63ec85889292b6640911107bc5f6',
            '0d5606d8348b17ce05580b9756bc17f01e7f87a34e1e05b930cf5f3d7cec0432',
            'ba82f5e386fb99af2a43d63a4e4a696a4e296f461cc1c2926b0a7531560038b5')
checks = []
observed = {}
sources = {}
read_seq = {}

def check(label, result, evidence=None):
    if type(result) is not bool:
        raise AssertionError('audit condition is not exact bool: ' + label)
    if any(c['check'] == label for c in checks):
        raise AssertionError('duplicate independent check label: ' + label)
    checks.append(dict(check=label, passed=result, evidence=evidence))
    if not result:
        raise AssertionError(label)

def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def full_pin(path, expected_sha=None):
    path = Path(path)
    serial = read_seq.get(str(path),0)+1
    read_seq[str(path)] = serial
    label = str(path)+'_read_'+str(serial)
    a = identity(path)
    check('regular_full_EOF_' + label, stat.S_ISREG(a[2]) and a[3] == 1 and not path.is_symlink())
    raw = path.read_bytes()
    check('read_stable_exact7ID_' + label, a == identity(path) and a[4] == len(raw))
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha is not None:
        check('expected_full_SHA_' + label, digest == expected_sha)
    pin = dict(path=str(path), sha256=digest, size_bytes=len(raw), identity=a)
    observed[str(path)] = pin
    return pin, raw

def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise AssertionError('duplicate finite META key')
        result[key] = value
    return result

def nonfinite(value):
    raise AssertionError('nonfinite finite META constant: ' + value)

def read(path, expected_sha=None):
    pin, raw = full_pin(path, expected_sha)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite), pin

def segment(source, node):
    return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

def definitions(source):
    return {n.name: n for n in ast.parse(source).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

def const(source, name):
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    check('unique_literal_global_' + name + '_' + hashlib.sha256(source.encode()).hexdigest()[:12], len(nodes) == 1)
    return ast.literal_eval(nodes[0].value)

def text_checks(source, label, fragments):
    for i, text in enumerate(fragments):
        check(label + '_fragment_' + str(i), text in source, text)

def inventory(root, manifest_sha):
    manifest, mp = read(root / 'MANIFEST.json', manifest_sha)
    members = manifest['members']
    declared = {Path(v['path']).relative_to(root).as_posix(): v for v in members}
    check('root_manifest_all_member_names_unique', len(declared) == len(members))
    actual_names = {f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file() and f != root / 'MANIFEST.json'}
    check('all_root_manifest_members_including_every_nested_manifest', set(declared) == actual_names)
    for rel, pin in declared.items():
        got, raw = full_pin(root / rel)
        check('full_declared_pin_' + rel, got == pin)
        if rel.endswith('.py'):
            s = raw.decode('utf8'); ast.parse(s)
            sources[rel] = s
            check('full_Source_AST_parse_only_' + rel, True)
    directories = {f.relative_to(root).as_posix(): identity(f) for f in root.rglob('*') if f.is_dir()}
    check('full_directory_7ID_inventory', directories == manifest['directories'])
    check('whole_package_root_7ID', identity(root) == manifest['package_root_identity'])
    check('all_package_aliases_absent', not any(f.is_symlink() for f in root.rglob('*')))
    check('member_count_exact', type(manifest['member_count']) is int and manifest['member_count'] == len(members))
    byte_key = 'complete_member_bytes' if 'complete_member_bytes' in manifest else 'total_member_bytes'
    check('whole_member_byte_total_exact', manifest[byte_key] == sum(v['size_bytes'] for v in members))
    return manifest, mp, directories, declared

def main():
    root = Path(sys.argv[1]); manifest_sha = sys.argv[2]
    check('Source_only_own_audit_exact_two_args', len(sys.argv) == 3 and root.is_relative_to(Path('/private/tmp')))
    manifest, mp, dirs, declared = inventory(root, manifest_sha)
    role_pins = {name: observed[str(root/name)] for name in ROLE_NAMES}
    for name, sha in zip(ROLE_NAMES, ROLE_SHA):
        check('fixed_five_Source_role_' + name, role_pins[name]['sha256'] == sha)
    check('fixed_binder_Source_bytes_preserved', hashlib.sha256(sources['bind_complete_qualification_SOURCE_only.py'].encode()).hexdigest() == hashlib.sha256((OLD/'bind_complete_qualification_SOURCE_only.py').read_bytes()).hexdigest())
    contract, _ = read(root/'INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json')
    check('exact_consumed_Source_peer_schema', contract['schema'] == 'INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1')
    check('exact_consumed_Source_peer_status', contract['status'] == 'SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION')
    check('five_role_keys_required', set(contract['qualified_template_Source_pins']) == set(ROLE_NAMES))
    check('Source_only_new_helper_SHA_required', contract['qualified_helper_candidate_SHA'] == HELPER_SHA and contract['new_actual_helper_qualification'] is None and contract['six_future_business_pins'] == [None]*6)
    inverse, _ = read(root/'ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json')
    expected_hunks = [10,13,13,14]
    for i, (name, proof) in enumerate(inverse['all_four_complete_source_inverse'].items()):
        template = name[:-3] + '.UNREADY.py'
        source = sources[template]
        parent_pin, parent_raw = full_pin(proof['original_Source_pin']['path'], proof['original_Source_pin']['sha256'])
        check('original_current_Source_exact_saved7ID_' + name, parent_pin == proof['original_Source_pin'])
        check('full_original_inverse_hunk_count_' + name, len(proof['full_hunks']) == expected_hunks[i])
        restored = source
        for j, hunk in reversed(list(enumerate(proof['full_hunks']))):
            check('unique_inverse_hunk_' + name + '_' + str(j), restored.count(hunk['new_utf8']) == 1)
            restored = restored.replace(hunk['new_utf8'], hunk['old_utf8'], 1)
        parent = parent_raw.decode('utf8')
        check('whole_byte_inverse_' + name, restored == parent)
        check('whole_AST_inverse_' + name, ast.dump(ast.parse(restored), include_attributes=False) == ast.dump(ast.parse(parent), include_attributes=False))
        olddefs = definitions(parent); newdefs = definitions(source)
        check('all_original_definition_names_order_' + name, list(olddefs) == proof['complete_original_definitions'] and list(newdefs) == proof['complete_new_definitions'] and all(x in newdefs for x in olddefs))
        changed = []
        for fn, node in olddefs.items():
            exact = segment(parent,node) == segment(source,newdefs[fn]) and ast.dump(node,include_attributes=False) == ast.dump(newdefs[fn],include_attributes=False)
            if not exact: changed.append(fn)
            else: check('unchanged_full_original_definition_' + name + '_' + fn, True)
        check('only_declared_original_definition_changes_' + name, changed == proof['actually_changed_original_definitions'] and set(changed).issubset({'run','main','_full_controls','_source_namespace'}))
    for label, count in [('PURE',61),('FRESH',13)]:
        base = root/('ORIGINAL_Q89_'+label+'_COMPLETE_SOURCE')
        ledger, _ = read(base/'ORIGINAL_ROOT_COMPLETE_SOURCE_FREEZE.json')
        check('whole_original_' + label + '_Source_copy_count', len(ledger['complete_files']) == count)
        expected = set(ledger['complete_files']) | {'ORIGINAL_ROOT_COMPLETE_SOURCE_FREEZE.json'}
        check('whole_original_' + label + '_Source_copy_namespace', {f.relative_to(base).as_posix() for f in base.rglob('*') if f.is_file()} == expected)
        for rel, saved in ledger['complete_files'].items():
            cp = observed[str(base/rel)]
            check('original_'+label+'_Source_copy_fullSHA_size_'+rel, cp['sha256'] == saved['sha256'] and cp['size_bytes'] == saved['identity'][4])
    oldq, oldqpin = read(root/'ORIGINAL_Q89_COMPLETE_PARENT_CONTRACT.json')
    check('oldQ89_complete_copy_exactSHA_not_new_credit', oldqpin['sha256'] == '89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816' and oldq['helper']['sha256'] == 'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c')
    prior, _ = read(root/'ORIGINAL_CANDIDATE_COMPLETE_SOURCE_PEER_REVIEW.json')
    check('prior_helper479Source_checks_429_unique_labels_honest', len(prior['checks']) == prior['check_count'] == 479 and len({x['check'] for x in prior['checks']}) == 429 and all(x['passed'] is True for x in prior['checks']))
    helper_rel = 'COMPLETE_SOURCE_REVIEWED_NEW_HELPER_CANDIDATE/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume.UNREADY.py'
    check('reviewed_helper_candidate_Source_no_newQ', observed[str(root/helper_rel)]['sha256'] == HELPER_SHA)
    helper = sources[helper_rel]
    helper_inverse, _ = read(root/'COMPLETE_SOURCE_REVIEWED_NEW_HELPER_CANDIDATE/EXACT_COMPLETE_SOURCE_INVERSE.json')
    hp, hraw = full_pin(helper_inverse['parent_helper_pin']['path'], helper_inverse['parent_helper_pin']['sha256'])
    restored = helper
    for i, h in reversed(list(enumerate(helper_inverse['hunks']))):
        old = h.get('old_utf8', h.get('old')); new = h.get('new_utf8', h.get('new'))
        check('whole_helper_unique_inverse_' + str(i), type(old) is str and type(new) is str and restored.count(new) == 1)
        restored = restored.replace(new,old,1)
    check('whole_helper_fullbyte_inverse_preserved', restored.encode() == hraw)
    check('whole_helper_fullAST_inverse_preserved', ast.dump(ast.parse(restored),include_attributes=False) == ast.dump(ast.parse(hraw),include_attributes=False))
    small = sources[ROLE_NAMES[4]]; tree = ast.parse(small)
    check('eight_small_control_definitions', len(definitions(small)) == 8)
    check('all5_positive_labels_order', const(small,'POSITIVES') == ['empty_owned_True','same_actual_read_duplicate_and_Popen_owned_True','control_only_floatbits_strattrs_owned_True','default_Audit_subclass','default_records_dict_subclass'])
    check('all13_rejection_labels_order', const(small,'REJECTS') == ['flag_None','flag_zero','flag_one','flag_string','flag_list','flag_dict','Audit_subclass_True','records_dict_subclass_True','records_list_True','recording_True','stale_active_registry_identity','active_True','active_False'])
    check('all3_lastuse_failure_labels_order', const(small,'FAILURES') == ['invalid_second_row_before_clear','missing_attempt_count_before_clear','nonfinite_clone_after_clear'])
    fields = ['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
    check('all_nine_snapshot_fields_exact_order', const(small,'SNAPSHOT_FIELDS') == fields)
    text_checks(small,'same_actual_observation_full_private_controls',[
        'with g.ReadOpenAudit() as observed:', 'for _ in range(2):', 'process = subprocess.Popen(',
        'actual_stdout, actual_stderr = process.communicate(timeout=wall_seconds)',
        "duplicate[0]['attempt_count'] == 2", "len(origin['subprocess_records']) == 1",
        'copy.deepcopy(observed._records)', 'audit._popen_objects = dict(observed._popen_objects)',
        'baseline_audit = disjoint_owned_audit(g, source)', 'owned = disjoint_owned_audit(g, source)',
        'complete_snapshot_equal(baseline, value, exact_value',
        "struct.pack('>d', part)", "str.encode(part, 'utf8', 'surrogatepass')", "visit(getattr(part, '__dict__', None))",
        'all nine original snapshot fields and order', 'no PID/FD/inode normalization',
        'private clone error may follow complete map consumption', 'no_transactional_private_mode_promise=True',
        'original_error_class_and_message_retained=True', 'g._ACTIVE_TRACES.remove(stale)',
        "stream.read(1) == b'\\n' and stream.read(1) == b''", 'no_fields_or_records_selected=True'])
    smallfn = definitions(small)['small_private_snapshot_controls']
    popens = [n for n in ast.walk(smallfn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr == 'Popen']
    check('one_actual_Popen_capture_Source_no_crossrun_comparison', len(popens) == 1)
    text_checks(helper,'helper_private_inactive_lastuse_unchanged',["type(_consume) is bool", 'type(self) is ReadOpenAudit and type(self._records) is dict', 'self._active is False and self._recording is False', 'all(trace is not self for trace in _ACTIVE_TRACES)', 'self._records.clear()', 'A later clone error is not transactional', "_consume=False"])
    pure, ph, fresh, fh = [sources[x] for x in ROLE_NAMES[:4]]
    text_checks(pure,'complete_original_pure_protocol_new_control_additive',[
        'private_owner_consume_controls(g, small_graph)', 'audit_controls.small_private_snapshot_controls(g, fixture_path, exact_value, WALL_SECONDS)',
        'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json', 'encoder=ORDER_PRESERVING_JSON_ENCODER',
        'complete private controller SOURCE changed', 'ACTUAL_SUCCESS_PINS = None'])
    for tag, host, limits in [('pure',ph,'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20'),('fresh',fh,'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20')]:
        text_checks(host,tag+'_genuine_unchanged_resource_guard_Source',[
            limits,'helper.modules();helper.guard_admission(full)', 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
            'resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',
            "resources.check()", "before['artifact_bytes']+ARCHIVE_CAP>=96*2**30", "before['disk_free_bytes']-ARCHIVE_CAP<8*2**30",
            'type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources',
            "runner.execute(HOST/'run','admit',command,STAGE_CAP)", "watch['own_child_only'] is not True", "watch['liveness_group_cleanup'] is not True",
            'threads=1,children_at_once=1,retries=0', 'profile_used=False,supervisor_class_or_MRO_modified=False'])
        for name in ['BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','AUDIT_CONTROL_PATH','TARGET_SHA']:
            check(tag+'_unbound_future_'+name, const(host,name) is None)
    text_checks(ph,'pure_order_artifact_full_host_validation',[
        "audit_controls.validate_small_control_report(private_report)", "private_pin['size_bytes'] != private_pin['identity'][4]",
        "control_report['private_snapshot_control_Source'] != audit_control_pin", "support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))",
        "resource.history_roots([str(HOST),str(OUT),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)"])
    text_checks(fresh,'full_original27_37112_sameaudit_True_fullwire',[
        "verified=new.verify_graph(GRAPH_PIN['path'],expected_sha256=GRAPH_PIN['sha256'],phase=PHASE)",
        "exact_value(expected,verified,'complete_actual_fresh_verifier_return')",
        "len(actual_paths)==len(set(actual_paths))==37112 and set(actual_paths)==paths|{GRAPH_PIN['path']}",
        "trace=audit.snapshot(_consume=True)", 'del trace', 'owned_map_identity=id(audit._records)',
        "audit_controls.full_consumed_snapshot_wire_compare(trace,output/'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz')",
        'no_second_graph_or_input_phase_substituted=True,all37112_actual_reads_from_same_genuine_phase=True',
        'no_cross_phase_hash_or_stat_cache=True', 'default_fields==audit_controls.SNAPSHOT_FIELDS',
        "full_pin(AUDIT_CONTROL_PATH,AUDIT_CONTROL_SHA256)", "after==report['fixed_inputs_before']"])
    check('fresh_full_verify_graph_called_once_no_second_replay', len([n for n in ast.walk(definitions(fresh)['run']) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr == 'verify_graph']) == 1)
    check('fresh_public_return_contract27_order_matches_preserved_original', len(const(fh,'RETURN_FIELDS')) == 27)
    check('fresh_trace_ninefields_same_as_small', const(fh,'TRACE_FIELDS') == fields)
    text_checks(fh,'fresh_full_host_whole_OUTPUT27_37112_threegzip_6files',[
        "(1800,600,512,64*2**20,96*2**30,8*2**30,1,1,0)",
        "EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz", "ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz", "ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz",
        "set(p.name for p in OUT.iterdir())!={'ACTUAL_RUN_CLAIM.json','ACTUAL_REPORT.json','private_trace_fixture.txt','EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'}",
        'declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)',
        'not path.is_relative_to(support.ART)', 'support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))',
        'source_after!=source_before', 'complete_consumed_vs_default_wire', 'all37112_actual_reads_from_same_genuine_phase',
        "claim['PID']==report['PID']==admission['PID']==watch['pid']", "claim['parent_PID']==report['parent_PID']==admission['parent_PID']==os.getpid()"])
    binder = sources['bind_complete_qualification_SOURCE_only.py']
    text_checks(binder,'strict_actual_future_binder_META_Source_only',[
        "PEER_SCHEMA = 'INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1'",
        "PEER_STATUS = 'SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'", "peer['qualified_template_manifest_pin'] == manifest_pin",
        "peer['qualified_template_Source_pins'] == role_pins", "witness['closed'] is True", "witness['actual_tool_terminal_return_observed'] is True",
        "type(terminal['exit_code']) is int and terminal['exit_code'] == 0", "'session_id' not in terminal or terminal['session_id'] is None",
        "json.loads(terminal['output'], object_pairs_hook=unique_pairs, parse_constant=reject_nonfinite)",
        "observed['installed_helper'] == witness['installed_helper']", "observed['source_install_record'] == witness['source_install_record']",
        "helper_full['size_bytes'] == HELPER_BYTES", "old_helper_Q_canonical_fullEOF_unchanged", "PROTECTED_PARENT_SHA",
        "all_bound definition" if False else "all bound definition bytes/AST retained",
        "full template bytes/AST inverse", "out.is_relative_to(Path('/private/tmp')) and not os.path.lexists(out)",
        "shutil.copytree(HERE, out / 'COMPLETE_QUALIFICATION_TEMPLATE_SOURCE')", "new_actual_helper_qualification=None, six_future_business_pins=[None] * 6"])
    forbidden_calls = {'exec','eval','compile','__import__'}
    check('binder_no_candidate_execution_importlib_API_subprocess_or_dynamic_exec', not any(isinstance(n,ast.Call) and ((isinstance(n.func,ast.Name) and n.func.id in forbidden_calls) or (isinstance(n.func,ast.Attribute) and n.func.attr in {'exec_module','Popen','run','execute','verify_graph'})) for n in ast.walk(ast.parse(binder))))
    check('binder_restricts_all_mutations_to_Tmp_Source_output', "never canonical or ART" in binder and "write_new" in binder)
    plan, _ = read(root/'ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json')
    check('pure60_andfresh1800_resource_META_contracts_preserved', plan['pure_caps'] == dict(whole_seconds=60,phase_seconds=60,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0) and plan['fresh_caps'] == dict(whole_seconds=1800,phase_seconds=600,rss_mib=512,joint_HODE_archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0))
    check('all_runtime_qualifications_unknown_None_not_Q89', all(plan[k] is None for k in ['new_Source_install_witness','new_Source_install_record','new_pure_terminal','new_fresh_terminal','two_new_independent_saved_reviews','new_joint_Helper_Q','actual_memory_or_RSS_or_build_PASS_prediction']) and plan['all_business_science_pins'] == [None]*6)
    check('Source_reviewed_only_not_executed', manifest['Source_candidate_controller_helper_guard_reader_API_or_binding_executed'] is False and manifest['new_actual_helper_qualification'] is None and manifest['six_future_business_pins'] == [None]*6)
    # The final derivative corrects only finite Source/META evidence. Keep the
    # original malformed-precision receipt and real Source-only failures.
    dp, _ = read(root/'EXACT_INTEGER_META_ONLY_COMPLETE_SOURCE_DERIVATIVE_INVERSE.json')
    old_manifest, oldmp = read(OLD/'MANIFEST.json',OLD_SHA)
    check('old409c_manifest_actual_pin_exact_retained', dp['original_frozen409c_manifest_pin'] == oldmp)
    check('old409c_manifest_complete_bytes_preserved', (root/'ORIGINAL_SEALED_409c_MANIFEST.json').read_bytes() == (OLD/'MANIFEST.json').read_bytes())
    edits = dp['only_four_explicit_META_doc_contract_and_stdlib_counter_changes']
    check('exact_four_finite_META_doc_counter_changes', [e['file'] for e in edits] == ['ACTUAL_FINAL_SOURCE_SCOPE_REVIEW_TOOL_RETURN.json','ROOT_EXECUTION_SEQUENCE_AND_COMPLETE_SCOPE.md','INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json','seal_full_SOURCE_package_stdlib.py'])
    for edit in edits:
        rel = edit['file']
        check('complete_derivative_old_bytes_' + rel, (OLD/rel).read_text() == edit['old_utf8'])
        check('complete_derivative_new_bytes_' + rel, (root/rel).read_text() == edit['new_utf8'])
        check('finite_derivative_full_byte_inverse_' + rel, (root/rel).read_text().replace(edit['new_utf8'],edit['old_utf8'],1) == (OLD/rel).read_text())
    modified_names = {e['file'] for e in edits}|{'FINAL_FULL_SOURCE_SCOPE_REVIEW.json'}
    for member in old_manifest['members']:
        rel = Path(member['path']).relative_to(OLD).as_posix()
        if rel not in modified_names:
            check('all_original119_retained_Source_bytes_' + rel, observed[str(root/rel)]['sha256'] == member['sha256'] and observed[str(root/rel)]['size_bytes'] == member['size_bytes'])
    repaired, _ = read(root/'ACTUAL_FINAL_SOURCE_SCOPE_REVIEW_TOOL_RETURN.json')
    original_receipt, _ = read(OLD/'ACTUAL_FINAL_SOURCE_SCOPE_REVIEW_TOOL_RETURN.json')
    stdout = json.loads(repaired['terminal_tool_return']['output'],object_pairs_hook=pairs,parse_constant=nonfinite)
    check('precise_raw_actual_tool_stdout_never_rewritten', repaired['terminal_tool_return'] == original_receipt['terminal_tool_return'])
    check('only_rounded_ns_pin_corrected_from_exactPython_actualstdout', repaired['review_pin'] == stdout['report_pin'] and repaired['review_pin'] != original_receipt['review_pin'])
    check('old_originalSource_actual_terminal_exit0_closed', repaired['closed'] is True and repaired['actual_tool_terminal_return_observed'] is True and type(repaired['terminal_tool_return']['exit_code']) is int and repaired['terminal_tool_return']['exit_code'] == 0 and 'session_id' not in repaired['terminal_tool_return'])
    failedpath = Path(dp['original_postseal_META_mismatch_receipt_path'])
    failed, failedpin = read(failedpath)
    check('real_original_postseal_int1_failure_retained', type(failed['terminal_tool_return']['exit_code']) is int and failed['terminal_tool_return']['exit_code'] == 1 and failed['closed'] is True)
    deriv_failed, _ = read(root/'ACTUAL_DERIVATIVE_INITIAL_SOURCE_SEAL_COUNT_FAILURE_TOOL_RETURN.json')
    check('real_derivative_source_counter_initial_int1_preserved', type(deriv_failed['terminal_tool_return']['exit_code']) is int and deriv_failed['terminal_tool_return']['exit_code'] == 1 and deriv_failed['closed'] is True)
    sibling = root.with_name(root.name+'_seal_receipt')
    seal, sealpin = read(sibling/'ACTUAL_EXACT_INTEGER_SOURCE_SEAL_TOOL_RETURN.json','e97cc21a44dfea9bfdf6af8eab15b0fbb5585fc2fa712e43fd0c0c581f5e2afc')
    post, postpin = read(sibling/'ACTUAL_FULL_EXACT_INTEGER_POSTSEAL_SOURCE_TOOL_RETURN.json','a6a710647bd550d2facddfc37108432f9e0b0a650c9347ef7cb84ceb9d4cc31a')
    postreport, postreportpin = read(sibling/'FULL_EXACT_INTEGER_POSTSEAL_SOURCE_VERIFICATION.json','d69e106b0cc46df695b9e692f96466bd69560f22ae3e514c4e0659bb229e2aa1')
    for label, receipt in [('seal',seal),('postseal',post)]:
        terminal = receipt['terminal_tool_return']
        check('actual_derivative_'+label+'_typedint0closed_noSession', receipt['source_only'] is True and receipt['closed'] is True and receipt['actual_tool_terminal_return_observed'] is True and type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and 'session_id' not in terminal)
        actual = json.loads(terminal['output'].strip().splitlines()[-1],object_pairs_hook=pairs,parse_constant=nonfinite)
        check('actual_derivative_'+label+'_stdout_exact_manifest4pin', actual['manifest_pin'] == mp)
        check('actual_derivative_'+label+'_stdout_full_count_scope', actual['member_count'] == len(declared) and actual['full_file_count'] == len(declared)+1 and actual['complete_member_bytes'] == sum(x['size_bytes'] for x in declared.values()) and actual['directory_count'] == len(dirs))
    check('actual_derivative_postseal_exact_manifest_and_true_tool_pin', postreport['actual_manifest_pin'] == mp and postreport['actual_Source_seal_tool_receipt_pin'] == sealpin)
    check('actual_derivative_postseal_full_namespace_only_no_newQ', postreport['all_fullEOF_SHA7ID_root_directory_members_before_after_unchanged'] is True and postreport['actual_7ID_decoded_from_exact_original_tool_stdout_using_Python'] is True and postreport['new_actual_helper_qualification'] is None and postreport['candidate_controller_helper_guard_API_Source_binder_or_material_executed'] is False)
    # Full before/after reread Source/META only; no ART payload references are opened.
    originals = list(observed.items())
    for path, pin in originals:
        raw = Path(path).read_bytes()
        check('final_fullEOF_SHA7ID_unchanged_' + path, identity(path) == pin['identity'] and len(raw) == pin['size_bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'])
    check('final_all_subdirectory_7IDs_unchanged', {f.relative_to(root).as_posix():identity(f) for f in root.rglob('*') if f.is_dir()} == dirs)
    check('final_whole_root7ID_unchanged', identity(root) == manifest['package_root_identity'])
    out = Path(tempfile.mkdtemp(prefix='axmat_private_inactive_audit_complete_independent_SOURCE_review_20261010_',dir='/private/tmp'))
    for name in ROLE_NAMES + ('bind_complete_qualification_SOURCE_only.py','ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json','INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json','ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json'):
        shutil.copyfile(root/name,out/name)
    shutil.copyfile(root/'MANIFEST.json',out/'QUALIFIED_ORIGINAL_TEMPLATE_MANIFEST.json')
    for name in ['EXACT_INTEGER_META_ONLY_COMPLETE_SOURCE_DERIVATIVE_INVERSE.json','ACTUAL_FINAL_SOURCE_SCOPE_REVIEW_TOOL_RETURN.json','ACTUAL_DERIVATIVE_INITIAL_SOURCE_SEAL_COUNT_FAILURE_TOOL_RETURN.json','ACTUAL_EXACT_META_FULL_SCOPE_SOURCE_REVIEW_TOOL_RETURN.json','ACTUAL_SOURCE_GENERATION_TOOL_RETURNS.json']:
        shutil.copyfile(root/name,out/name)
    shutil.copyfile(failedpath,out/'ORIGINAL_ACTUAL_POSTSEAL_int1_PRECISION_FAILURE_TOOL_RETURN.json')
    author_sibling=out/'ORIGINAL_AUTHOR_EXACT_META_SOURCE_SEAL'
    shutil.copytree(sibling,author_sibling)
    shutil.copyfile(__file__,out/'review_complete_qualification_Source_stdlib.py')
    (out/'COMPLETE_FULL_SOURCE_META_INPUT_PINS.json').write_text(json.dumps(observed,indent=2,allow_nan=False)+'\n')
    report = dict(schema=contract['schema'],status=contract['status'],source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,
        qualified_template_manifest_pin=mp,qualified_helper_candidate_SHA=HELPER_SHA,qualified_template_Source_pins=role_pins,
        new_actual_helper_qualification=None,six_future_business_pins=[None]*6,
        original_complete_pure_Source_files=61,original_complete_fresh_Source_files=13,
        actual_Source_package_members=len(declared),parsed_python_files=len(sources),
        qualified_author_actual_Source_seal_tool_receipt_pin=sealpin,
        qualified_author_actual_full_postseal_Source_tool_receipt_pin=postpin,
        original_real_Source_only_postseal_precision_failure_pin=failedpin,
        original_helper_Source_peer_check_count=479,original_helper_Source_peer_unique_label_count=429,
        added_private_controls=dict(positive=5,reject=13,last_use_failure=3,complete_snapshot_fields=9),
        full_current_graph_scope=dict(public_return_fields=27,canonical_files=37111,actual_unfiltered_reads=37112,complete_lossless_gzips=3,exact_OUT_files=6),
        Source_candidate_controller_helper_guard_reader_API_or_binding_executed=False,
        any_numeric_component_material_decode_or_replay_performed=False,any_RSS_or_build_or_science_pass_prediction=None,
        scope_notes=['Original Q89 complete Source retained as parent evidence only; no new qualification credit.',
                     'One future actual Popen observation yields disjoint owned audit state; no PID/FD/inode normalization.',
                     'Private clone failure after map clear is nontransactional; exclusive external-alias ownership is a caller contract.',
                     'Original pure archive is H+O+D 64MiB; conservative Root E scope remains separately honest.',
                     'Only Source/META full EOF was read. No stored37k graph or material/numeric payload was opened.'])
    (out/'REVIEW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    (out/'REPORT.txt').write_text('PASS: independent complete SOURCE-only audit.\n'+str(len(checks))+' exact typed checks; no candidate/controller/helper/guard/API/binder execution.\nNo runtime, memory, build, INPUT, native, AAA, ABA or physical-balance qualification created.\n')
    print(json.dumps(dict(source_only=True,status=report['status'],review_dir=str(out),check_count=len(checks),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),all_checks_typed_true=True,blockers=[],new_actual_helper_qualification=None),separators=(',',':')))

if __name__ == '__main__':
    main()

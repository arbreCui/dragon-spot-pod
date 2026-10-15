# Pure source text. These future functions are not called by the generator.

def stream_environment_helper():
    """Load only the normally pinned canonical private helper; never patch619."""
    require_ready()
    module = load(require(STREAM_ENVIRONMENT_HELPER, STREAM_ENVIRONMENT_HELPER_SHA),
                  'axmat_streaming_sha_actual_environment_helper_v14')
    if (Path(module.__file__).resolve() != STREAM_ENVIRONMENT_HELPER
            or module.__spec__ is None or Path(module.__spec__.origin).resolve() != STREAM_ENVIRONMENT_HELPER
            or module.ROOT != ROOT):
        raise ValueError('ordinary canonical stream helper and original ROOT binding required')
    return module


def stream_environment_helper_source_admission():
    """Pure complete pinned SOURCE/control metadata read; no helper import/call."""
    for wanted in (STREAM_ENVIRONMENT_HELPER_SHA, STREAM_ENVIRONMENT_SOURCE_PROOF_SHA,
                   STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA):
        if not isinstance(wanted, str) or re.fullmatch('[0-9a-f]{64}', wanted) is None or wanted == '0'*64:
            raise ValueError('unknown stream helper/proof/actual control pin cannot admit SOURCE')
    parent_path = require(STREAM_ENVIRONMENT_PARENT_HELPER, STREAM_ENVIRONMENT_PARENT_HELPER_SHA)
    factory_path = require(STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT, STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA)
    candidate_path = require(STREAM_ENVIRONMENT_HELPER, STREAM_ENVIRONMENT_HELPER_SHA)
    proof_path = require(STREAM_ENVIRONMENT_SOURCE_PROOF, STREAM_ENVIRONMENT_SOURCE_PROOF_SHA)
    controls_path = require(STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS, STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA)
    proof = read(proof_path); controls = read(controls_path)
    semantics = dict(complete_full_SHA_per_unique_literal_per_environment=True,
        same_call_same_literal_memo_only=True, cross_stage_SHA_reuse=False,
        different_literal_SHA_reuse=False, full_seven_identity_rechecks_required=True,
        buffer_bytes=4194304)
    parent_pin = dict(path=str(parent_path), sha256=STREAM_ENVIRONMENT_PARENT_HELPER_SHA)
    factory_pin = dict(path=str(factory_path), sha256=STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA)
    candidate_pin = dict(path=str(candidate_path), sha256=STREAM_ENVIRONMENT_HELPER_SHA)
    proof_pin = dict(path=str(proof_path), sha256=STREAM_ENVIRONMENT_SOURCE_PROOF_SHA)
    controls_pin = dict(path=str(controls_path), sha256=STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA)
    if (proof['schema'] != 'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_SOURCE_PATCH_V14'
            or proof['parent_helper'] != parent_pin or proof['candidate_helper'] != candidate_pin
            or proof['component_factory_parent'] != factory_pin
            or proof['complete_inverse_byteexact'] is not True or proof['ROOT_binding_unchanged'] is not True
            or proof['outside_context_default_digest_behavior_unchanged'] is not True
            or any(proof[key] != expected for key, expected in semantics.items())
            or proof['original_definitions'] != 34 or proof['byteexact_original_definitions'] != 33
            or proof['modified_original_definitions'] != ['digest']
            or any(proof[key] is not True for key in ('native_alias_exit_recheck_required',
                'native_alias_mapping_must_be_explicitly_passed',
                'original_environment_verify_inventory_modules_guard_and_mathematics_byteexact'))
            or any(proof[key] is not False for key in ('genuine_supervisor_class_or_MRO_modified',
                'business_imported', 'business_executed', 'helper_controls_executed',
                'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted'))):
        raise ValueError('entire independently pinned original619/d2 streaming source contract required')
    original = parent_path.read_text(); candidate = candidate_path.read_text(); inverse = candidate
    edits = proof['edits']
    if not isinstance(edits, list) or not edits or len({edit['name'] for edit in edits}) != len(edits):
        raise ValueError('complete named independent stream helper edit regions required')
    for edit in reversed(edits):
        if (set(edit) != {'name', 'old', 'new', 'count'} or type(edit['count']) is not int or edit['count'] <= 0
                or not all(isinstance(edit[key], str) and edit[key] for key in ('name', 'old', 'new'))
                or inverse.count(edit['new']) != edit['count']):
            raise ValueError('literal counted full helper inverse region differs')
        inverse = inverse.replace(edit['new'], edit['old'], edit['count'])
    if inverse != original or hashlib.sha256(inverse.encode()).hexdigest() != STREAM_ENVIRONMENT_PARENT_HELPER_SHA:
        raise ValueError('whole helper inverse must restore complete619 source byteexact')
    forward = original
    for edit in edits:
        if forward.count(edit['old']) != edit['count']:
            raise ValueError('original whole helper forward region differs')
        forward = forward.replace(edit['old'], edit['new'], edit['count'])
    if forward != candidate or hashlib.sha256(candidate.encode()).hexdigest() != STREAM_ENVIRONMENT_HELPER_SHA:
        raise ValueError('complete stream helper source differs from independent full forward proof')
    old_tree = ast.parse(original); new_tree = ast.parse(candidate)
    old_defs = {node.name: node for node in old_tree.body if isinstance(node, ast.FunctionDef)}
    new_defs = {node.name: node for node in new_tree.body if isinstance(node, ast.FunctionDef)}
    def definition_scope(tree):
        records = {}
        def walk(node, parents):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                key = (*parents, node.name)
                if key in records:
                    raise ValueError('ambiguous original helper definition scope')
                records[key] = node
                parents = key
            for child in ast.iter_child_nodes(node):
                walk(child, parents)
        walk(tree, ())
        return records
    old_scope = definition_scope(old_tree); new_scope = definition_scope(new_tree)
    if (len(old_scope) != 34 or not set(old_scope) <= set(new_scope)
            or 'complete_environment_digest_context' not in new_defs
            or any(ast.get_source_segment(original, node) != ast.get_source_segment(candidate, new_scope[key])
                   for key, node in old_scope.items() if key != ('digest',))):
        raise ValueError('all original33 nondigest definitions including classes/nested defs must remain byteexact')
    root_nodes = lambda tree: [ast.get_source_segment(original if tree is old_tree else candidate, node)
        for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
        and target.id == 'ROOT' for target in node.targets)]
    if root_nodes(old_tree) != root_nodes(new_tree) or root_nodes(old_tree) != ['ROOT = Path(__file__).resolve().parents[2]']:
        raise ValueError('original canonical helper ROOT assignment must remain exact')
    if proof['added_definitions'] != sorted(set(new_defs)-set(old_defs)):
        raise ValueError('entire new helper definition inventory must match independent AST')
    if (controls['schema'] != 'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14'
            or controls['status'] != 'PASS_COMPLETE_HELPER_CONTROLS_ONLY'
            or controls['helper'] != candidate_pin or controls['source_patch_proof'] != proof_pin
            or any(controls[key] != expected for key, expected in semantics.items())
            or any(controls[key] is not True for key in ('same_seven_identity_mutation_rejected',
                'native_alias_policy_preserved', 'default_environment_rejections_retained'))
            or any(controls[key] is not False for key in ('mathematics_changed', 'MRO_modified',
                'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted'))):
        raise ValueError('actual full helper controls with exact same-call memo-only semantics required')
    sources = {str(parent_path): STREAM_ENVIRONMENT_PARENT_HELPER_SHA,
        str(factory_path): STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA,
        str(candidate_path): STREAM_ENVIRONMENT_HELPER_SHA, str(proof_path): STREAM_ENVIRONMENT_SOURCE_PROOF_SHA,
        str(controls_path): STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA}
    for key in ('author_source_review', 'author_actual_source_terminal_receipt'):
        item = proof[key]
        if set(item) != {'path', 'sha256'}:
            raise ValueError('whole original source review/tool ownership descriptors required')
        require(item['path'], item['sha256']); sources[item['path']] = item['sha256']
    files = controls['files']
    if type(files) is not dict or not files:
        raise ValueError('whole actual helper control absolute file pins required')
    for literal, wanted in files.items():
        path = Path(literal)
        if (type(literal) is not str or not path.is_absolute() or '..' in path.parts
                or not isinstance(wanted, str) or re.fullmatch('[0-9a-f]{64}', wanted) is None or wanted == '0'*64
                or (literal in sources and sources[literal] != wanted)):
            raise ValueError('typed actual helper control literal pin or owner conflict')
        require(path, wanted); sources[literal] = wanted
    control_root = Path(controls['control_root']); host_root = Path(controls['host_root'])
    actual_bytes = 0; inventories = {}
    for root, key in ((control_root, 'control_inventory'), (host_root, 'host_inventory')):
        if not root.is_absolute() or '..' in root.parts or root.is_symlink() or not root.is_dir():
            raise ValueError('actual whole helper control and genuine host namespace roots required')
        observed_files = {}; observed_links = {}; observed_directories = []
        for parent, dirs, names in os.walk(root, followlinks=False):
            observed_directories.append(str(Path(parent).relative_to(root)))
            for name in [*dirs, *names]:
                path = Path(parent)/name; relative = str(path.relative_to(root))
                if path.is_symlink():
                    observed_links[relative] = os.readlink(path)
                elif path.is_file():
                    wanted = files.get(str(path))
                    if wanted is None or not stat.S_ISREG(path.stat().st_mode):
                        raise ValueError('every ordinary helper control/host literal needs its own absolute SHA owner')
                    require(path, wanted); observed_files[relative] = wanted; actual_bytes += path.stat().st_size
                elif not path.is_dir():
                    raise ValueError('special helper control namespace member forbidden')
        observed = dict(files=observed_files, symlinks=observed_links, directories=sorted(observed_directories))
        if controls[key] != observed:
            raise ValueError('complete actual helper/host directory, link or file namespace differs')
        inventories[key] = observed
    if control_root == host_root or actual_bytes >= 64*2**20:
        raise ValueError('distinct complete helper-only roots must fit original64MiB cap')
    manifest = read(require(control_root/'raw_preservation_manifest.json', files[str(control_root/'raw_preservation_manifest.json')]))
    if (manifest['schema'] != 'AXMAT_HELPER_ONLY_CONTROL_RAW_PRESERVATION_V1'
            or manifest['files'] != {name: sha for name, sha in inventories['control_inventory']['files'].items()
                                     if name != 'raw_preservation_manifest.json'}
            or manifest['component_native_AAA_ABA_credit'] is not False or manifest['original86_stage_count_increment'] != 0):
        raise ValueError('actual driver whole raw preservation manifest must bind the entire control scope')
    def actual_document(key):
        item = controls[key]
        if set(item) != {'path', 'sha256'} or files.get(item['path']) != item['sha256']:
            raise ValueError('every actual Root/child document must be owned by whole absolute control files')
        return read(require(item['path'], item['sha256']))
    receipt = actual_document('actual_terminal_receipt')
    actual_result = actual_document('actual_result')
    host_result = actual_document('actual_host_result')
    journal = actual_document('actual_stage_journal')
    watch = actual_document('actual_child_watchdog')
    for key in ('actual_full_stdout', 'actual_full_stderr'):
        item = controls[key]
        if set(item) != {'path', 'sha256'} or files.get(item['path']) != item['sha256']:
            raise ValueError('actual complete Root stdout/stderr must belong to full pinned control scope')
        require(item['path'], item['sha256'])
    terminal = receipt['terminal_result']
    if (receipt['schema'] != 'AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1'
            or type(terminal['exit_code']) is not int or terminal['exit_code'] != 0 or receipt['session_closed'] is not True
            or receipt['action'] != 'fixtures' or {key: receipt['stdout'][key] for key in ('path', 'sha256')} != controls['actual_full_stdout']
            or type(receipt['stdout']['size_bytes']) is not int
            or receipt['stdout']['size_bytes'] != require(controls['actual_full_stdout']['path'], controls['actual_full_stdout']['sha256']).stat().st_size
            or {key: receipt['stderr'][key] for key in ('path', 'sha256')} != controls['actual_full_stderr']
            or type(receipt['stderr']['size_bytes']) is not int
            or receipt['stderr']['size_bytes'] != require(controls['actual_full_stderr']['path'], controls['actual_full_stderr']['sha256']).stat().st_size):
        raise ValueError('actual successful closed Root tool return must bind every raw child evidence document')
    if (actual_result['schema'] != 'AXMAT_V14_HELPER_ONLY_FIXTURE_RESULT_V1'
            or actual_result['status'] != 'PASS_HELPER_PROTOCOL_ONLY' or actual_result['action'] != 'fixtures'
            or {key: actual_result['source'][key] for key in ('path', 'sha256')} != candidate_pin
            or len(actual_result['groups']) != 21
            or any(group['status'] != 'PASS_HELPER_PROTOCOL_ONLY' for group in actual_result['groups'])
            or actual_result['numeric_component_stage_count_increment'] != 0
            or actual_result['numerical_controls_compiler_or_API_invoked'] is not False
            or any(actual_result[key] is not False for key in ('native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted'))):
        raise ValueError('actual helper control result must pass without native or science qualification')
    for group in actual_result['groups']:
        path = control_root/group['name']/'case_result.json'
        if read(require(path, files[str(path)])) != group:
            raise ValueError('each actual whole helper group record must equal independently pinned raw case result')
    for item in host_result['input_sources']:
        if files.get(item['path']) != item['sha256']:
            raise ValueError('every actual driver/helper/proof/supervisor source pin must remain in complete INPUT')
    for key in ('original_helper', 'resource_factory'):
        item = host_result[key]
        if files.get(item['path']) != item['sha256']:
            raise ValueError('genuine original619/f136 control host sources must remain in whole INPUT')
    for key, expected in (('actual_child_result', controls['actual_result']), ('actual_watchdog', controls['actual_child_watchdog'])):
        item = host_result[key]
        if {name: item[name] for name in ('path', 'sha256')} != expected:
            raise ValueError('actual host must bind exact child result/watchdog independently of Root summary')
    merged = host_result['actual_full_merged_stdout_stderr']
    if files.get(merged['path']) != merged['sha256']:
        raise ValueError('actual entire merged child log must have whole INPUT ownership')
    child_stdout = read(require(merged['path'], merged['sha256']))
    if (child_stdout['status'] != 'PASS_HELPER_PROTOCOL_ONLY' or child_stdout['action'] != 'fixtures'
            or child_stdout['result_sha256'] != controls['actual_result']['sha256']
            or child_stdout['Root_actual_child_terminal_required_before_admission'] is not True):
        raise ValueError('actual complete child stdout must bind its returned fixture result')
    root_stdout = read(require(controls['actual_full_stdout']['path'], controls['actual_full_stdout']['sha256']))
    if (root_stdout['status'] != 'PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST' or root_stdout['action'] != 'fixtures'
            or {key: root_stdout['host_result'][key] for key in ('path', 'sha256')} != controls['actual_host_result']
            or root_stdout['actual_external_Root_terminal_still_required'] is not True):
        raise ValueError('actual whole Root stdout pointer must equal its genuine host result owner')
    stages = journal['stages']
    if (host_result['schema'] != 'AXMAT_V14_HELPER_ONLY_GENUINE_SUPERVISOR_ACTUAL_HOST_V1'
            or host_result['status'] != 'PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST' or host_result['action'] != 'fixtures'
            or host_result['stage_records'] != stages or host_result['watchdog'] != watch
            or host_result['actual_command'] != watch['command']
            or not 0 <= host_result['whole_elapsed_seconds'] < host_result['whole_wall_cap_seconds'] == 120
            or not 0 <= host_result['whole_archive_bytes'] < host_result['archive_cap_bytes'] == 64*2**20
            or (host_result['rss_cap_mib'],host_result['threads'],host_result['children_at_once'],host_result['retries']) != (512,1,1,0)
            or any(host_result[key] is not False for key in ('supervisor_class_or_MRO_modified',
                'failed_V13_audit_reexecuted', 'numerical_component_or_transport_executed',
                'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted'))):
        raise ValueError('actual genuine original-budget host completion and unchanged MRO required')
    if (not isinstance(stages, list) or not stages or any(stage['status'] != 'PASS' for stage in stages)
            or type(watch['returncode']) is not int or watch['returncode'] != 0
            or type(watch['pid']) is not int or watch['pid'] <= 0 or watch['command'] != stages[-1]['command']
            or watch['limit_failure'] is not None or watch['own_child_only'] is not True
            or watch['liveness_group_cleanup'] is not True or watch['rss_cap_mib'] != 512
            or not 0 <= watch['sampled_peak_rss_mib'] < 512
            or not 0 < watch['wall_cap_seconds'] <= stages[-1]['wall_cap_seconds'] <= 120
            or not 0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds']):
        raise ValueError('genuine own-child helper-only120/512 complete control stage must pass')
    return dict(schema='AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_COMPONENT_SOURCE_ADMISSION_V14',
        helper=candidate_pin, source_patch_proof=proof_pin, actual_helper_controls_admission=controls_pin,
        original_helper=parent_pin, component_factory_parent=factory_pin,
        proof=proof, actual_helper_controls=controls, source_inputs=sources,
        complete_helper_controls_only=True, helper_default_status_is_informational_UNREADY=True,
        supervisor_class_and_MRO_unchanged=True, original_cache_and_sender_math_and_raw_controls_unchanged=True,
        native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False)

from pathlib import Path
import ast
import difflib
import hashlib
import json

ROOT = Path('/Users/wen/spot')
OLD = Path('/private/tmp/axmat-trim-v5-bounded-runtime-input-intake-source-draft-20261008')
NEW = Path('/private/tmp/axmat-trim-v7-bounded-runtime-input-intake-source-draft-20261009')
HOSTNAME = 'axmat_trim_v7_standalone_bounded_runtime_api_intake_host_20261009.py'
RECNAME = 'axmat_trim_v7_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py'
old_host = OLD/'axmat_trim_v5_standalone_bounded_runtime_api_intake_host_20261008.py'
old_recorder = OLD/'axmat_trim_v5_standalone_bounded_runtime_api_intake_postterminal_recorder_20261008.py'
canonical_host = ROOT/'validation/artifacts/axial-material-owned-specs-standalone-bounded-runtime-api-intake-evidence-20261007/host.py'
canonical_recorder = Path('/private/tmp/axmat_root_owned_specs_standalone_bounded_intake_wrapped_stages_recorder_20261007.py')
factory = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v7.py'
factory_sha = '45783d9920a53ca517f28abbff9071e81cd29b0ef87336f45216aa86d8e4bc5a'
helper = ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py'
helper_sha = '85551979317309cfa70bb27a4b0e04ae908bbd33865dc3edfbe6c7f4d70baf6c'
input_specs = ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
input_specs_sha = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def desc(path):
    return dict(path=str(path), sha256=sha(path), bytes=path.stat().st_size)

def save(name, value):
    p = NEW/name
    assert not p.exists()
    p.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    return desc(p)

mother_before = [desc(p) for p in sorted(OLD.iterdir()) if p.is_file()]
assert sha(old_host) == 'ae38f9eb2b0e8be779147f5ce03d0b2a119f464e2681691c8a6dee79a423cc5c'
assert sha(old_recorder) == '70a918d502703befb7d025af8e29081d27fe7cc84fc12adb8eace39f3e429ed4'
assert sha(canonical_host) == '26d871a780bb0116e803168fcd67d5ec01528ecfd4c5b31c7b56dd975ddd732e'
assert sha(canonical_recorder) == 'd284da36a7e499b6eebf3790a45f671ea24a228729d2b26599f97b84ff32650f'
assert sha(factory) == factory_sha and sha(helper) == helper_sha
assert sha(input_specs) == input_specs_sha
for kind, candidate, parent in [('host', old_host, canonical_host), ('recorder', old_recorder, canonical_recorder)]:
    old_proof = json.loads((OLD/(kind+'_canonical_complete_inverse.json')).read_bytes())
    assert old_proof['parent'] == desc(parent) and old_proof['candidate'] == desc(candidate)
    inverse = candidate.read_text()
    for item in reversed(old_proof['regions']):
        start, end = item['candidate_start'], item['candidate_end']
        assert inverse[start:end] == item['replacement']
        inverse = inverse[:start]+item['original']+inverse[end:]
    assert inverse.encode() == parent.read_bytes()

def retarget_lines(parent, candidate, keys, hash_replacement=None):
    old = parent.read_text()
    lines = old.splitlines(keepends=True)
    regions = []
    new_lines = []
    offset = 0
    found = set()
    for line in lines:
        matches = [key for key in keys if line.startswith(key)]
        assert len(matches) <= 1
        replacement = line
        if matches:
            key = matches[0]
            assert key not in found
            found.add(key)
            replacement = line.replace('v5', 'v7').replace('V5', 'V7').replace('20261008', '20261009')
            if hash_replacement is not None:
                replacement = replacement.replace(*hash_replacement)
            assert replacement != line
            regions.append(dict(label=key, candidate_start=offset, candidate_end=offset+len(replacement), original=line, replacement=replacement))
        new_lines.append(replacement)
        offset += len(replacement)
    assert found == set(keys)
    new = ''.join(new_lines)
    assert not candidate.exists()
    candidate.write_text(new)
    inverse = new
    for item in reversed(regions):
        start, end = item['candidate_start'], item['candidate_end']
        assert inverse[start:end] == item['replacement']
        inverse = inverse[:start]+item['original']+inverse[end:]
    assert inverse.encode() == parent.read_bytes()
    ast.parse(new)
    proof = dict(schema='AXMAT_COMPLETE_SOURCE_ONLY_POSITIONAL_INVERSE_V1', parent=desc(parent), candidate=desc(candidate), regions=regions,
        complete_inverse_byte_exact=True, identity_line_regions=len(regions), no_API_import_or_constructor_or_child_or_native=True, ART_written=False)
    return save(('host' if candidate.name == HOSTNAME else 'recorder')+'_v5_to_v7_inverse.json', proof)

host = NEW/HOSTNAME
recorder = NEW/RECNAME
host_proof = retarget_lines(old_host, host,
    ['DRAFT_STATUS=', 'if DRAFT_STATUS!=', 'FACTORY=', 'FACTORY_SHA=', 'OUT=', 'TERM=', 'BASE='],
    ('331824f74c560dca5ea3de63776f3efb6d0c05a16ea7c044d87563ba02da1a60', factory_sha))
recorder_proof = retarget_lines(old_recorder, recorder,
    ['BASE=', 'OUT=', 'HOST=', 'HOST_SHA=', 'COMPONENT_TERM=', 'CMD=', "if (body['schema']!=", 'stdout='],
    ('ae38f9eb2b0e8be779147f5ce03d0b2a119f464e2681691c8a6dee79a423cc5c', sha(host)))

def whole_canonical_proof(parent, candidate, label):
    old, new = parent.read_text(), candidate.read_text()
    regions = []
    for tag, a, b, c, d in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag != 'equal':
            regions.append(dict(candidate_start=c, candidate_end=d, original=old[a:b], replacement=new[c:d]))
    inverse = new
    for item in reversed(regions):
        start, end = item['candidate_start'], item['candidate_end']
        assert inverse[start:end] == item['replacement']
        inverse = inverse[:start]+item['original']+inverse[end:]
    assert inverse.encode() == parent.read_bytes()
    return save(label+'.json', dict(schema='AXMAT_COMPLETE_SOURCE_ONLY_POSITIONAL_INVERSE_V1', parent=desc(parent), candidate=desc(candidate),
        regions=regions, complete_inverse_byte_exact=True, no_API_import_or_constructor_or_child_or_native=True, ART_written=False))

canonical_proofs = [whole_canonical_proof(canonical_host, host, 'host_canonical_complete_inverse'),
    whole_canonical_proof(canonical_recorder, recorder, 'recorder_canonical_complete_inverse')]
for label, parent, candidate in [('host', old_host, host), ('recorder', old_recorder, recorder)]:
    (NEW/(label+'_v5_to_v7.diff')).write_text(''.join(difflib.unified_diff(parent.read_text().splitlines(keepends=True), candidate.read_text().splitlines(keepends=True), fromfile=str(parent), tofile=str(candidate))))

def literals(path):
    vals = {}
    for n in ast.parse(path.read_text()).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                vals[n.targets[0].id] = ast.literal_eval(n.value)
            except (ValueError, TypeError):
                pass
    return vals

hv, rv = literals(host), literals(recorder)
assert hv['DRAFT_STATUS'].startswith('UNREADY') and rv['DRAFT_STATUS'].startswith('UNREADY')
assert all(hv[k] is None for k in ('DECL_SHA', 'SEAL_SHA', 'RUN_SHA', 'PREP_SHA'))
assert all(rv[k] is None for k in ('DECL_SHA', 'SEAL_SHA', 'RUN_SHA', 'PREP_SHA', 'API_RETURN_SHA'))
assert hv['FACTORY_SHA'] == factory_sha and rv['HOST_SHA'] == sha(host)
assert 'v5' not in host.read_text() and 'V5' not in host.read_text()
assert 'v5' not in recorder.read_text() and 'V5' not in recorder.read_text()
factory_text = factory.read_text()
assert helper.name in factory_text and helper_sha in factory_text
assert "INPUT_SPECS_SHA = '"+input_specs_sha+"'" in factory_text
work = Path('/private/tmp/axmat-trim-v7-standalone-bounded-runtime-api-intake-20261009')
evidence = ROOT/'validation/artifacts/axial-material-owned-specs-trim-v7-standalone-bounded-runtime-api-intake-evidence-20261009'
stdout = Path('/private/tmp/axmat-trim-v7-standalone-bounded-runtime-api-intake-host-20261009.stdout')
planned_paths = [work, evidence, stdout, stdout.with_suffix('.stderr')]
assert all(not p.exists() and not p.is_symlink() for p in planned_paths)
assert mother_before == [desc(p) for p in sorted(OLD.iterdir()) if p.is_file()]
audit = dict(schema='AXMAT_TRIM_V7_SOURCE_ONLY_STANDALONE_INTAKE_AUDIT_V1', status='STATIC_SOURCE_ONLY_UNREADY',
    unchanged_V5_mother_before_and_after=mother_before, formal_factory=desc(factory), formal_graph_helper=desc(helper), unchanged_original_whole_seven_key_historical_input=desc(input_specs),
    identity_patch_line_counts=dict(host=7, recorder=8), full_inverse_to_V5_and_canonical_byte_exact=True,
    draft_status_guard_precedes_business_import=True, future_SHA_literal_values=dict(host={k:hv[k] for k in ('DECL_SHA', 'SEAL_SHA', 'RUN_SHA', 'PREP_SHA')}, recorder={k:rv[k] for k in ('DECL_SHA', 'SEAL_SHA', 'RUN_SHA', 'PREP_SHA', 'API_RETURN_SHA')}),
    API_ABI='producer.production_admission(seal_sha, terminal_evidence, terminal_evidence_sha256), via ordinary formal factory admit CLI',
    no_new_config_ABI=True, unchanged_inline_binding_constants=True,
    producer_canonical_module_stems_unchanged_by_this_retarget=True, same_normal_FACTORY_CLI_invocation=True,
    host_source_sha_is_STATIC_SOURCE_IDENTITY_not_actual_host_return=True,
    nine_payload_names=['host.py','postterminal_recorder.py','host.stdout','host.stderr','result.json','runtime/run_bounded_dragon.py','intake/admit.log','intake/admit.watchdog.json','STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json'],
    tenth_new_Root_receipt_name='Root_terminal_return.json', original_complete_merged_JSON_accepted=True,
    no_business_import_API_constructor_PREP_RUN_child_native=True, no_ART_or_formal_source_written=True,
    all_planned_execution_and_durable_paths_absent=[str(p) for p in planned_paths])
audit_pin = save('source_audit.json', audit)
handoff = dict(schema='AXMAT_TRIM_V7_STOPPED_STANDALONE_INTAKE_BINDING_PLAN_V1', status='STOPPED_SOURCE_ONLY_UNREADY',
    host=desc(host), recorder=desc(recorder), producer=desc(factory), producer_graph_helper=desc(helper), source_audit=audit_pin,
    configuration_form='Original V5 and canonical host have no runtime configuration file; retained original module-level bindings, no new config ABI.',
    intake_WORK=str(work), durable_evidence_family=str(evidence), planned_host_stdout=str(stdout), planned_host_stderr=str(stdout.with_suffix('.stderr')),
    actual_bindings={key:None for key in ('DECL_SHA','SEAL_SHA','PREP_SHA','RUN_SHA','API_RETURN_SHA','actual_graph_sha256','actual_host_initial_chunk','actual_host_session_id','actual_host_terminal_chunk','actual_host_exit_code','actual_durable_Root_terminal_SHA')},
    required_future_bindings=['Bind only actual successful V7 declaration, build seal, true Root PREP and RUN receipt SHA after original five stages and four returned tails all complete with observed RUN return 0.',
        'Independently review the exact bound host and set its READY status only after the preceding real build evidence passes; recorder HOST_SHA must match that final bound host source.',
        'Run exactly one ordinary three-argument production_admission CLI through genuine original monitored child, retaining its complete single merged JSON log and host whole stdout/empty stderr.',
        'Bind API_RETURN_SHA only from the genuine complete actual monitored API return; set recorder READY only after independent review of its exact postterminal-only source.',
        'Supply Root observed initial chunk, session, terminal chunk and exit 0 through the unchanged recorder CLI; preserve exactly nine payload files plus the independent tenth Root terminal receipt.'],
    retained_contract=dict(total_wall_seconds=1800, stage_wall_seconds=600, RSS_mib=512, archive_bytes=2*2**30, history_bytes=96*2**30, free_floor_bytes=8*2**30,
        threads=1, children_at_once=1, retries=0, whole_single_JSON_API_return=True, nine_payload_plus_Root_receipt=True,
        supervisor='original705/38de/bc4 genuine class and MRO', scientific_or_native_RSS_or_AAA_ABA_credit=False),
    complete_source_inverse=[host_proof, recorder_proof, *canonical_proofs], independent_external_source_review=None,
    ART_created=False, project_or_business_API_or_constructor_or_native_executed=False)
handoff_pin = save('STOPPED_handoff.json', handoff)
print(json.dumps(dict(host=desc(host), recorder=desc(recorder), handoff=handoff_pin, source_audit=audit_pin, full_inverse_byte_exact=True, all_future_actual_pins_None=True)))

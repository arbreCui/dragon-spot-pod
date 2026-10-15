"""SOURCE-only finite wiring of the genuine whole five-stage build host."""
import ast
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
DEST = BASE / 'actual_complete_combined_build_v17_sources'
PARENT = BASE / 'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
PARENT_SHA = '37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3'
PEER = Path('/private/tmp/axmat_v17_prep_receipt_and_five_stage_host_source_review_20261010_9pcwjuzc')
DECL_SHA = 'cb1984ee991230e9b56a9783acafe36bfb9063b4b641ebe64387d3e60c29fb30'
PREP_SHA = 'c743c01c3f40ac32e06a4f3371c82dfa4b84314b0c85509aa1710216afe569b2'
old = PARENT.read_text()
assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == PARENT_SHA
plan = json.loads((PEER / 'FIVE_STAGE_HOST_ADAPTATION_PLAN.json').read_text())
assert plan['actual_prep_receipt']['sha256'] == PREP_SHA
assert plan['actual_declaration']['sha256'] == DECL_SHA
assert plan['outer_command_wall_cap_seconds'] == 1800
assert plan['inner_original_stage_wall_cap_seconds'] == 600
commands = plan['expected_inner_five_stage_commands_derived_from_literal_SOURCE_without_API']
labels = plan['expected_inner_five_stage_labels']
assert len(commands) == len(labels) == 5
text = old
changes = []
def replace(before, after, count=1):
    global text
    assert text.count(before) == count, before[:100]
    text = text.replace(before, after)
    changes.append(dict(before=before, after=after, count=count))

replace('One normal complete combined preparation under the unchanged genuine guard.', 'One normal whole five-stage combined build under the unchanged genuine guard.')
replace("HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v17-20261010')", "HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v17-20261010')")
replace("SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v17_sources')", "SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_build_v17_sources')\nDECLARATION_SHA=" + repr(DECL_SHA) + "\nPREP_SHA=" + repr(PREP_SHA) + "\nINNER_FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V17'\nEXPECTED_LABELS=" + repr(labels) + "\nEXPECTED_COMMANDS=" + repr(commands))
replace("    if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL)):raise ValueError('fresh combined preparation namespaces required; no retry')", "    if os.path.lexists(HOST):raise ValueError('fresh one-use whole build host required; no retry')\n    if not all(p.is_dir() for p in (SOURCE,OUT,TERMINAL)):raise ValueError('actual prepared SOURCE/OUT/TERMINAL required')\n    if any(os.path.lexists(OUT/p) for p in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','audit/binary_identity.json','audit/result.json',INNER_FAMILY+'/stages.json','runtime/Dragon')):raise ValueError('no prior build execution or build retry allowed')")
line = next(x for x in text.splitlines() if x.startswith('    inputs=['))
replace(line, line + "\n    inputs += [support.pin(OUT/'declaration.json',DECLARATION_SHA),support.pin(TERMINAL/'declaration_terminal_return.json',PREP_SHA),support.pin(OUT/'input_graph.json','968801a327739feab4eafa5e77bb500dbf2f6f6c7a7303bf51fb528e7b4875a4'),support.pin(OUT/'input_creation_python_open_trace.json','6fb8fa8b22eee736c84dd8af4b06953635cc0a270fde51ad48062da3bd0e6b2e')]\n    inputs += [support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]\n    inputs += [support.pin(BASE/'actual_complete_combined_prepare_v17_receipts/Root_actual_prepare_tool_terminal_return.json'),support.pin(BASE/'actual_complete_combined_prepare_v17_receipts/Root_actual_complete_combined_prepare_summary.json','07494a308553d0e42f861732f7f2c782bc0f77e7668aa307551fcc82c27bbf3e')]")
replace("'COMBINED_PREPARATION'", "'COMPLETE_COMBINED_BUILD'", 2)
replace("        command=[str(support.PYTHON),str(TARGET),'prepare-build']\n        runner.execute(HOST/'run','prepare',command,STAGE_CAP)\n        log=HOST/'run/prepare.log';watch_path=HOST/'run/prepare.watchdog.json'", "        command=[str(support.PYTHON),str(TARGET),'run-build','--sha256',DECLARATION_SHA,'--prep-sha256',PREP_SHA]\n        runner.execute(HOST/'run','build',command,WHOLE_CAP)\n        log=HOST/'run/build.log';watch_path=HOST/'run/build.watchdog.json'")
start = text.index('        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())')
end = text.index('        if len(runner.records)!=1', start)
replace(text[start:end], '''        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())
        declaration=OUT/'declaration.json';d=json.loads(declaration.read_text())
        if support.pin(declaration)['sha256']!=DECLARATION_SHA:raise ValueError('immutable declaration changed')
        if d['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_DECLARATION_V1' or d['stages']!=EXPECTED_LABELS or (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'])!=(1800,600,512,2*2**30):raise ValueError('original complete five stages and caps required')
        if set(admission)!=set(('result','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')):raise ValueError('full whole-build return and four actual tails required')
        result=json.loads((OUT/'driver_result.json').read_text());audit=json.loads((OUT/'audit/result.json').read_text())
        if admission['result']!=result or result['classification']!='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or result['error'] is not None or result['fresh_cold_AAA_required'] is not True:raise ValueError('actual complete build-only return required')
        if audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS' or audit['declaration_sha256']!=DECLARATION_SHA or audit['historical_whole_component_body']!=d['historical_whole_component_body'] or audit['actual_last_cprime_trim_component_INPUT']!=d['actual_last_cprime_trim_component_INPUT']:raise ValueError('complete original link audit required')
        if any(value[k] is not False for value in (result,audit) for k in ('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')):raise ValueError('link identity only science boundaries required')
        inner=json.loads((OUT/INNER_FAMILY/'stages.json').read_text())['stages']
        if len(inner)!=5 or [s['label'] for s in inner]!=EXPECTED_LABELS or [s['command'] for s in inner]!=EXPECTED_COMMANDS or any(s['status']!='PASS' for s in inner):raise ValueError('all exact five original supervised commands must pass once')
        inner_watches=[]
        for stage in inner:
            raw_log=OUT/(stage['label']+'.log');iw=json.loads(raw_log.with_suffix('.watchdog.json').read_text())
            if iw['command']!=stage['command'] or type(iw['returncode']) is not int or iw['returncode']!=0 or iw['limit_failure'] is not None or iw['rss_cap_mib']!=512 or not 0<=iw['sampled_peak_rss_mib']<512 or not 0<iw['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 or not 0<=iw['elapsed_seconds']<iw['wall_cap_seconds'] or iw['own_child_only'] is not True or iw['liveness_group_cleanup'] is not True or support.pin(raw_log)['sha256']!=stage['log_sha256']:raise ValueError('each unchanged genuine inner stage watch required')
            inner_watches.append(iw)
        if inner_watches!=result['watchdogs'] or inner_watches[:-1]!=audit['previous_stage_watchdogs']:raise ValueError('all five watches must agree')
        raw=json.loads((OUT/'raw_metadata_receipt.json').read_text())
        if raw['files']!={label+'.log':support.pin(OUT/(label+'.log'))['sha256'] for label in EXPECTED_LABELS[:4]} or raw['before_binary_identity_gates'] is not True or raw['complete_raw_tools_and_link_stdout'] is not True:raise ValueError('complete raw metadata before all identity gates required')
        seal=json.loads((OUT/'seal.json').read_text());files={};directories=[]
        for folder,dirs,names in os.walk(OUT,followlinks=False):
            for name in dirs:
                p=Path(folder)/name
                if p.is_symlink():raise ValueError('unexpected build output symlink')
                directories.append(str(p.relative_to(OUT)))
            for name in names:
                p=Path(folder)/name
                if p.is_symlink():raise ValueError('unexpected build output symlink')
                files[str(p.relative_to(OUT))]=support.pin(p)['sha256']
        if seal['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_BUILD_SEAL_V1' or seal['symlinks']!={} or seal['directories']!=sorted(directories) or set(files)!=set(seal['files'])|{'seal.json'} or any(files[k]!=v for k,v in seal['files'].items()):raise ValueError('complete original OUT seal required')
        if result['corrected_runtime']!={k:support.pin(OUT/'runtime/Dragon')[k] for k in ('path','sha256')}:raise ValueError('actual built runtime identity required')
        actual_size=support.archive_bytes((SOURCE,OUT));tail_resources=admission['actual_resources']
        if admission['actual_tail_check']!='PASS' or not result['elapsed_seconds']<=admission['actual_elapsed_seconds']<WHOLE_CAP or type(admission['actual_archive_bytes']) is not int or admission['actual_archive_bytes']!=actual_size or not 0<actual_size<ARCHIVE_CAP or tail_resources['artifact_budget_bytes']!=96*2**30 or tail_resources['min_free_bytes']!=8*2**30 or tail_resources['declared_resource_roots']!=d['resource_roots'] or tail_resources['resource_scope_policy']!=d['resource_scope_policy'] or tail_resources['resource_scope_contract']!=d['resource_scope_contract'] or not set(d['resource_roots']).issubset(tail_resources['resource_roots']) or not actual_size<=tail_resources['artifact_bytes']<=96*2**30 or tail_resources['disk_free_bytes']<8*2**30:raise ValueError('all original actual post-seal budget tails required')
        resource.validate_history_roots(tail_resources['resource_roots'],support.ART)
''')
replace('(HOST,SOURCE,OUT,SOURCE_ARCHIVE)', '(HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE)', 2)
replace("schema='AXMAT_V17_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1',status='ACTUAL_COMPLETE_COMBINED_PREPARE_EXTERNAL_ROOT_REQUIRED'", "schema='AXMAT_V17_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',status='ACTUAL_COMPLETE_COMBINED_BUILD_EXTERNAL_ROOT_REQUIRED'")
replace('actual_prepare_stdout=support.pin(log),actual_declaration=', 'actual_build_stdout=support.pin(log),actual_build_seal=support.pin(OUT/\'seal.json\'),actual_driver_result=support.pin(OUT/\'driver_result.json\'),actual_inner_stages=inner,actual_inner_watchdogs=inner_watches,actual_tail_fields={k:admission[k] for k in (\'actual_tail_check\',\'actual_elapsed_seconds\',\'actual_archive_bytes\',\'actual_resources\')},outer_command_wall_cap_seconds=WHOLE_CAP,inner_original_stage_wall_cap_seconds=STAGE_CAP,whole_combined_INPUT_admitted=False,actual_declaration=')
replace('actual_prepare_stdout=support.pin(log),actual_external_Root_terminal_required=True', 'actual_build_stdout=support.pin(log),actual_external_Root_terminal_required=True')
replace('FAILED_COMPLETE_COMBINED_PREPARE_NO_RETRY', 'FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY')
ast.parse(text)
inverse = text
for item in reversed(changes):
    assert inverse.count(item['after']) == item['count']
    inverse = inverse.replace(item['after'], item['before'])
assert inverse == old
host = DEST/'combined_build_host.py'
assert not host.exists()
host.write_text(text)
peer_dest=DEST/'sealed_prep_receipt_and_stage_source_review'
assert not peer_dest.exists();peer_dest.mkdir()
for p in sorted(PEER.iterdir()):
    assert p.is_file() and not p.is_symlink();q=peer_dest/p.name;shutil.copy2(p,q)
    assert p.read_bytes()==q.read_bytes()
proof=dict(schema='AXMAT_V17_FINITE_BUILD_HOST_SOURCE_INVERSE_V1',status='SOURCE_ONLY_NOT_EXECUTED',parent_path=str(PARENT),parent_sha256=PARENT_SHA,host_path=str(host),host_sha256=hashlib.sha256(host.read_bytes()).hexdigest(),finite_change_count=len(changes),changes=changes,full_byte_inverse_to_unchanged_parent=True,genuine_guard_and_MRO_unchanged=True,outer_whole_command_seconds=1800,original_inner_stages=5,original_inner_stage_seconds=600,original_rss_mib=512,archive_scope_includes_H_SOURCE_OUT_TERMINAL_SOURCE_ARCHIVE=True,original_archive_cap_bytes=2147483648,business_executed=False,native_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (DEST/'Root_finite_build_host_source_inverse.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
assert not Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v17-20261010').exists()
print(json.dumps(dict(status='SOURCE_ONLY_NOT_EXECUTED',host_sha256=proof['host_sha256'],finite_change_count=len(changes),full_inverse=True,actual_declaration_sha256=DECL_SHA,actual_prep_terminal_sha256=PREP_SHA,whole_command_seconds=1800,inner_stage_seconds=600)))

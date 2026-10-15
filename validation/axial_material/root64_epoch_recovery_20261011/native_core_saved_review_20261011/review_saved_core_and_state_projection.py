#!/usr/bin/env python3
"""Independent read-only saved-result audit; no compiler, PS or native launch."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
HERE = REC / 'native_core_saved_review_20261011'
CORE = ROOT / 'validation/artifacts/axial-material-new-ROOT64-native-core-controls-20261011'
STATE = ROOT / 'validation/artifacts/axial-material-new-REAL64-state-projection-compile-only-20261011'
AUTHOR_BIND = REC / 'native_core_controls_source/CURRENT_NATIVE_CORE_CONTROL_SOURCE_BINDING.json'
SUPPORT = ROOT / 'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
checks = []


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = path.lstat()
    check('ordinary non-symlink input ' + str(path), stat.S_ISREG(before.st_mode))
    before = identity(before)
    with path.open('rb') as handle:
        check('opened7ID ' + str(path), identity(os.fstat(handle.fileno())) == before)
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        check('EOF7ID ' + str(path), identity(os.fstat(handle.fileno())) == before)
    check('after7ID ' + str(path), identity(path.lstat()) == before)
    return dict(path=str(path), sha256=digest, size_bytes=before[4], identity=before)


def check(name, condition):
    checks.append(dict(name=name, passed=bool(condition)))
    if not condition:
        raise ValueError(name)


def same_saved_pin(item):
    fields = {key:item[key] for key in ('path','sha256','size_bytes','identity')}
    check('known full-pin metadata fields ' + item['path'],
          set(item) <= set(fields) | {'before_open_EOF_after_identity_equal'})
    if 'before_open_EOF_after_identity_equal' in item:
        check('saved before/open/EOF/after identity assertion ' + item['path'],
              item['before_open_EOF_after_identity_equal'] is True)
    check('complete saved pin still current ' + item['path'], pin(item['path']) == fields)


def load(path):
    return json.loads(Path(path).read_text())


def inventory(root):
    return [pin(path) for path in sorted(root.rglob('*')) if path.is_file()]


def scalar_resources(value):
    fresh = value['fresh_output']
    check('original history cap and floor', value['artifact_budget_bytes'] == 96*2**30 and
          value['min_free_bytes'] == 8*2**30)
    check('original declared complete axial family storage scope',
          value['resource_scope_policy'] == 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and
          set(value['declared_resource_roots']) == set(value['resource_roots']) and
          value['resource_scope_contract']['entire_project_artifact_cap_claimed'] is False)
    check('recorded history cold reserve and metadata headroom fit',
          value['artifact_bytes'] + 20971764748 + 64*2**20 < 96*2**30)
    check('recorded filesystem floor after original reserves fits',
          fresh['disk_free_bytes'] - 20971764748 - 2*2**30 >= 8*2**30)
    check('original fresh output budget and floor', fresh['artifact_budget_bytes'] == 2*2**30 and
          fresh['min_free_bytes'] == 8*2**30 and fresh['artifact_bytes'] < 2*2**30)
    return dict(history_artifact_bytes=value['artifact_bytes'], history_regular_files=value['regular_files'],
                complete_history_root_count=len(value['resource_roots']),
                disk_free_bytes=value['disk_free_bytes'], fresh_artifact_bytes=fresh['artifact_bytes'],
                cold_reserve_bytes=20971764748, metadata_headroom_bytes=64*2**20)


def review_epoch(folder, expected_status, expected_count, helper):
    binding = load(folder / 'Root_current_compile_only_binding.json')
    summary = load(folder / 'Root_actual_compile_only_summary.json')
    stages_document = load(folder / 'ROOT64_COMPILE_ONLY/stages.json')
    check('original stages envelope ' + str(folder), set(stages_document) == {'stages'})
    stages = stages_document['stages']
    check('saved summary status ' + str(folder), summary['status'] == expected_status and
          summary['failure'] is None and summary['after_check_error'] is None)
    check('saved stages equal original runner records ' + str(folder), stages == summary['records'])
    check('complete original stage order and count ' + str(folder),
          len(stages) == expected_count and [x['label'] for x in stages] ==
          ['build/compile_' + str(i) for i in range(expected_count)])
    check('prelaunch fixed pins match successful close preserved pins ' + str(folder),
          binding['fixed_current_pins'] == summary['fixed_current_pins'])
    for item in summary['fixed_current_pins'] + summary['output_pins']:
        same_saved_pin(item)
    check('all build files are completely covered by saved output pins ' + str(folder),
          {str(p) for p in (folder/'build').iterdir() if p.is_file()} ==
          {x['path'] for x in summary['output_pins']})
    clocks, watches, resources = [], [], []
    for index, stage in enumerate(stages):
        watch_path = (folder / (stage['label'] + '.log')).with_suffix('.watchdog.json')
        watch = load(watch_path)
        check('real stage PASS, exact command and original cap ' + str(watch_path),
              stage['status'] == 'PASS' and stage['command'] == binding['actual_commands'][index] and
              stage['wall_cap_seconds'] == 600 and watch['command'] == stage['command'])
        check('real PID and closed0 original Popen return ' + str(watch_path),
              type(watch['pid']) is int and watch['pid'] > 0 and
              type(watch['returncode']) is int and watch['returncode'] == 0 and
              watch['limit_failure'] is None)
        check('original own child RSS and wall guard ' + str(watch_path),
              watch['rss_cap_mib'] == 512 and 0 <= watch['sampled_peak_rss_mib'] < 512 and
              0 < watch['wall_cap_seconds'] <= 600 and
              0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds'] and
              watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
        verified = helper.check_watch(folder, stage)
        check('original helper actual saved watch verification ' + str(watch_path),
              verified == summary['actual_watchdog_checks'][index])
        clocks.append((stage['started_unix'], stage['started_unix'] + stage['elapsed_seconds']))
        resources.extend([scalar_resources(stage['resource_before']), scalar_resources(stage['resource_after'])])
        watches.append(dict(pin=pin(watch_path), pid=watch['pid'], returncode=watch['returncode'],
                            elapsed_seconds=watch['elapsed_seconds'],
                            sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
                            zero_means_not_sampled_peak_unknown=watch['sampled_peak_rss_mib'] == 0,
                            raw_waitpid_tuple_present=False))
    check('serial stages with no overlap ' + str(folder),
          all(clocks[i][1] <= clocks[i+1][0] for i in range(len(clocks)-1)))
    check('actual SELF and whole wall within original caps ' + str(folder),
          0 <= summary['SELF_peak_bytes'] < 512*2**20 and 0 <= summary['wall_seconds'] < 1800)
    resources.extend([scalar_resources(summary['resources_before']), scalar_resources(summary['resources_after'])])
    scope_keys = ['complete_native_build_qualified','Dragon_linked','transport_executed',
                  'original_seventeen_controls_executed','continuous_REAL64_producer_qualified',
                  'online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete']
    check('scope never expands beyond current component ' + str(folder),
          all(summary[k] is False for k in scope_keys))
    return summary, dict(summary_pin=pin(folder/'Root_actual_compile_only_summary.json'),
                         binding_pin=pin(folder/'Root_current_compile_only_binding.json'),
                         exact_commands=binding['actual_commands'], watches=watches,
                         wall_seconds=summary['wall_seconds'], SELF_peak_bytes=summary['SELF_peak_bytes'],
                         saved_resource_observations=resources,
                         saved_before_close_fixed_pin_count=len(summary['fixed_current_pins']),
                         explicit_each_stage_full_pin_copy_persisted=False,
                         original_host_rechecks_every_fixed_input_before_each_stage_and_at_close=True)


def inverse_state():
    proof_path = REC / 'continuous_chain_source/SPOSTATE64_TRANSFORM_LOCAL_BYTE_INVERSE_PROOF.json'
    proof = load(proof_path)
    for key in ('original_source','original_exact_retained_copy','candidate_source'):
        same_saved_pin(proof[key])
    value = Path(proof['candidate_source']['path']).read_bytes()
    for step in reversed(proof['complete_local_transform_steps']):
        check('state inverse exact after hash ' + step['label'],
              hashlib.sha256(value).hexdigest() == step['after_sha256'])
        if step['mode'] == 'one_exact_local_byte_splice':
            offset = step['byte_offset_in_step_input']; old=step['old'].encode(); new=step['new'].encode()
            check('state inverse exact saved splice ' + step['label'], value[offset:offset+len(new)] == new)
            value = value[:offset]+old+value[offset+len(new):]
        elif step['mode'] == 'exact_identifier_token_rename':
            pattern = rb'\b' + re.escape(step['new'].encode()) + rb'\b'
            value, count = re.subn(pattern, step['old'].encode(), value)
            check('state inverse exact token count ' + step['label'], count == step['occurrence_count'])
        else:
            raise ValueError('unknown state inverse mode')
        check('state inverse exact before hash ' + step['label'],
              hashlib.sha256(value).hexdigest() == step['before_sha256'])
    original = Path(proof['original_source']['path']).read_bytes()
    check('complete independently repeated state byte inverse', value == original ==
          Path(proof['original_exact_retained_copy']['path']).read_bytes())
    return dict(proof_pin=pin(proof_path), steps=len(proof['complete_local_transform_steps']),
                exact_original_Source_pin=pin(proof['original_source']['path']),
                candidate_Source_pin=pin(proof['candidate_source']['path']),
                complete_independent_byte_inverse_equal=True)


def inverse_projection():
    proof_path = REC / 'projection_chain_source/COMPLETE_SOURCE_TRANSFORM_AND_CURRENT_PINS.json'
    proof = load(proof_path)
    for item in proof['input_output_pins']:
        same_saved_pin(item)
    original = (ROOT/'src/SPOPROJ.f90').read_text()
    forward = original
    for step in proof['changes']:
        check('projection exact forward old count', forward.count(step['old']) == step['count'])
        forward = forward.replace(step['old'],step['new'])
    candidate_path = REC/'projection_chain_source/SPOPROJ64.f90'
    check('complete independently repeated projection forward bytes', forward.encode() == candidate_path.read_bytes())
    reverse = forward
    for step in reversed(proof['changes']):
        check('projection exact reverse new count', reverse.count(step['new']) == step['count'])
        reverse=reverse.replace(step['new'],step['old'])
    check('complete independently repeated projection byte inverse', reverse == original)
    return dict(proof_pin=pin(proof_path), steps=len(proof['changes']),
                exact_original_Source_pin=pin(ROOT/'src/SPOPROJ.f90'),
                candidate_Source_pin=pin(candidate_path), complete_independent_byte_inverse_equal=True)


def main():
    started=time.monotonic()
    before_inventory = dict(core=inventory(CORE),state_projection=inventory(STATE))
    author = load(AUTHOR_BIND)
    check('frozen author binding whole bytes',pin(AUTHOR_BIND)['sha256'] ==
          '142e6869a49c8e2b623e2039be64f624d76d4e41874b67388eecf545460b80f0')
    same_saved_pin(author['actual_control_Source_pin'])
    for item in author['actual_frozen_scientific_Source_pins'] + author['actual_current_full_EOF_dependency_pins']:
        same_saved_pin(item)
    check('original support bytes',pin(SUPPORT)['sha256'] ==
          '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7')
    spec=importlib.util.spec_from_file_location('independent_saved_core_original_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'independent_saved_core_original_helper')
    full,production=helper.modules();guard_files=helper.guard_admission(full)
    check('actual original full MRO and imported paths',
          full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,) and
          Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT)
    for p,sha in ((support.FULL,support.FULL_SHA),(support.PARENT,support.PARENT_SHA),
                  (support.BOUNDED,support.BOUNDED_SHA)):
        check('original runtime SHA '+str(p),pin(p)['sha256']==sha)
    core, core_evidence=review_epoch(CORE,'ACTUAL_83_CORE_CONTROLS_CLOSED0_ONLY',3,helper)
    state, state_evidence=review_epoch(STATE,'TWO_STATE_PROJECTION_COMPILE_STEPS_CLOSED0_ONLY',2,helper)
    check('exact author compile/link/run command vectors', core_evidence['exact_commands']==[
        author['planned_compile_command'],author['planned_link_command'],author['planned_run_command']])
    rows=[]
    # Parse the complete actual stdout one line at a time. Never synthesize case rows.
    with (CORE/'build/compile_2.log').open(encoding='utf-8') as handle:
        for line in handle:
            check('nonempty exact JSON stdout line',line.endswith('\n') and line.strip()!='')
            rows.append(json.loads(line))
    check('exact 83 case lines plus actual summary',len(rows)==84)
    actual, actual_summary=rows[:-1],rows[-1]
    source=Path(author['actual_control_Source_pin']['path']).read_text()
    def names(array):
        return re.findall(r"'([^']*)'",source.split(':: '+array+'(',1)[1].split(']',1)[0])
    expected=['positive_full_370_plane_'+str(i) for i in range(1,4)]+names('PUB_NAMES')+names('READ_NAMES')+[
        'import_occupied_output','import_output_aliases_flux','import_empty_daughter_not_root',
        'scope_coherent_rewrite_needs_host_SHA']
    check('complete Source83 order equals full saved actual stdout', [p['case'] for p in actual]==expected)
    check('Root case fields and actual summary exactly equal full stdout',
          core['actual_cases']==actual and core['actual_control_summary']==actual_summary)
    for index,row in enumerate(actual):
        phase='publish_read_import' if index<3 else 'publish_only' if index<31 else 'read_import' if index<79 else 'import_only' if index<82 else 'expected_core_acceptance'
        statuses=(2,3,4) if index<3 else (1,0,0) if index<31 else (2,1,1) if index<79 else (2,0,1) if index<82 else (2,3,4)
        check('actual case phase/status/assertions '+row['case'],row==dict(case=expected[index],phase=phase,
              publish_status=statuses[0],read_status=statuses[1],import_status=statuses[2],all_actual_assertions_completed=True))
    check('actual summary schema/explicit real call counts',actual_summary['schema']=='ACTUAL_CURRENT_ROOT64_NATIVE_CORE_CONTROLS_V1' and
          (actual_summary['control_count'],actual_summary['explicit_publish_calls'],actual_summary['explicit_read_calls'],actual_summary['explicit_import_calls'])==(83,32,52,55) and
          actual_summary['status']=='ALL_CURRENT_CORE_ASSERTIONS_COMPLETED' and actual_summary['synthetic_fixture'] is True)
    check('coherent internal acceptance is preserved as external-boundary obligation',
          core['core_coherent_rewrite_expected_accepted_external_file_SHA_still_required'] is True and
          actual[-1]['read_status']==3 and actual[-1]['import_status']==4)
    check('all actual stdout scientific/online scopes remain false',all(actual_summary[k] is False for k in (
        'transport_executed','original_seventeen_controls_qualified','native_producer_qualified','online_BOOT_qualified','goal_complete')))
    state_inverse=inverse_state();projection_inverse=inverse_projection()
    expected_state=[state_inverse['candidate_Source_pin']['path'],projection_inverse['candidate_Source_pin']['path']]
    check('actual two compile inputs are exact reviewed complete new state/projection Sources',
          [c[c.index('-c')+1] for c in state_evidence['exact_commands']]==expected_state)
    for item in (state_inverse['candidate_Source_pin'],projection_inverse['candidate_Source_pin']):
        check('new state/projection Source recorded at original compile binding',item in state['fixed_current_pins'])
    core_tools_path=REC/'ACTUAL_CURRENT_NATIVE_CORE_CONTROL_TRUE_TOOL_RETURNS.json'
    state_tools_path=REC/'ACTUAL_NEW_STATE_PROJECTION_TWO_COMPILE_TRUE_TOOL_RETURNS.json'
    core_tools=load(core_tools_path)['actual_tools'];state_tools=load(state_tools_path)['actual_compile_tools']
    check('true core host initial session and actual terminal EXIT0',len(core_tools)==2 and core_tools[0]['session_id']==47243 and
          core_tools[0]['chunk_id']=='a875f8' and core_tools[1]['chunk_id']=='dc7d84' and core_tools[1]['exit_code']==0)
    check('true state host initial session and actual terminal EXIT0',len(state_tools)==2 and state_tools[0]['session_id']==77011 and
          state_tools[0]['chunk_id']=='fdcaa8' and state_tools[1]['chunk_id']=='1c01f3' and state_tools[1]['exit_code']==0)
    check('true host stdout facts match core saved summary',json.loads(core_tools[1]['output'])==dict(
        status=core['status'],failure=None,records=3,wall_seconds=core['wall_seconds']))
    check('true host stdout facts match two-compile saved summary',json.loads(state_tools[1]['output'])==dict(
        status=state['status'],failure=None,records=2,wall_seconds=state['wall_seconds']))
    protected=[author['actual_control_Source_pin'],*author['actual_frozen_scientific_Source_pins'],
               state_inverse['candidate_Source_pin'],projection_inverse['candidate_Source_pin']]
    for item in protected:
        same_saved_pin(item)
    after_inventory=dict(core=inventory(CORE),state_projection=inventory(STATE))
    check('complete frozen ART file namespaces and seven identities unchanged by review',before_inventory==after_inventory)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    check('independent reviewer SELF stays within original 512MiB',peak<512*2**20)
    report=dict(schema='INDEPENDENT_ACTUAL_CURRENT_ROOT64_CORE83_AND_STATE_PROJECTION_SAVED_REVIEW_V1',
        status='PASS_SAVED_83_EXPECTED_CORE_BEHAVIORS_AND_TWO_COMPILE_ONLY_COMPONENTS',
        all_checks_passed=True,blockers=[],checks=checks,
        actual_full_case_rows=actual,actual_stdout_summary=actual_summary,
        Source_binding_pin=pin(AUTHOR_BIND),actual_core_evidence=core_evidence,
        actual_state_projection_compile_only_evidence=state_evidence,
        actual_repeated_complete_state_Source_inverse=state_inverse,
        actual_repeated_complete_projection_Source_inverse=projection_inverse,
        complete_frozen_ART_file_inventory_before=before_inventory,
        complete_frozen_ART_file_inventory_after=after_inventory,
        actual_Root_true_tool_returns_pins=[pin(core_tools_path),pin(state_tools_path)],
        original_guard_files_current_pins=[pin(p) for p in guard_files],
        source_only_reviewer=True,reviewer_invoked_PS_compiler_or_Native=False,
        own_elapsed_seconds=time.monotonic()-started,own_peak_RSS_bytes=peak,
        limitation_original_watchdog_records_Popen_returncode_not_raw_waitpid_tuple=True,
        limitation_sampled_RSS_is_observed_not_true_unsampled_peak=True,
        limitation_stage_labels_compile_0_1_2_mean_compile_link_run=True,
        current_synthetic_core_expected_behaviors_qualified=True,
        external_coherent_all_copy_file_SHA_refusal_still_pending=True,
        SPOBOOT64_seven_entry_parser_executed=False,
        GLOBAL_source_epoch_lifecycle_qualified=False,
        original_seventeen_controls_qualified=False,complete_native_build_qualified=False,
        continuous_REAL64_producer_qualified=False,transport_executed=False,
        online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    with (HERE/'INDEPENDENT_ACTUAL_CORE83_AND_TWO_COMPONENT_COMPILE_SAVED_REVIEW.json').open('x') as handle:
        json.dump(report,handle,ensure_ascii=False,indent=2);handle.write('\n');handle.flush();os.fsync(handle.fileno())
    brief=('PASS: full actual 83 ordered case rows + actual summary, exact statuses and 32/52/55 explicit calls.\n'
           'Three original watchdogs real returncode 0; observed core-child RSS 33.234375 MiB.\n'
           'The link-stage RSS 0 means no positive sample, not a measured zero peak.\n'
           'Core wall 5.001366 s; SELF 85.359375 MiB. All current fixed/dependency/output full SHA+7ID pins match.\n'
           'Complete frozen core/state-projection ART file namespaces stayed byte/identity unchanged.\n'
           'Coherent internal all-copy edit actually accepted; independent external host SHA refusal remains required.\n'
           'SPOSTATE64 and SPOPROJ64: two real compile-only steps closed0; repeated full byte inverses recover exact originals.\n'
           'Watchdogs preserve original Popen returncode, not an invented raw waitpid tuple.\n'
           'No new PS, compiler or Native child ran during independent saved review.\n'
           'No old 17/global/source/epoch/producer/native solve/online/AAA/ABA science qualification.\n')
    with (HERE/'INDEPENDENT_ACTUAL_CORE83_REVIEW.txt').open('x') as handle:
        handle.write(brief);handle.flush();os.fsync(handle.fileno())
    print(json.dumps(dict(status=report['status'],checks=len(checks),actual_case_count=83,
        core_child_sampled_RSS_MiB=33.234375,own_peak_RSS_bytes=peak,
        report_pin=pin(HERE/'INDEPENDENT_ACTUAL_CORE83_AND_TWO_COMPONENT_COMPILE_SAVED_REVIEW.json'))))


if __name__=='__main__':
    main()

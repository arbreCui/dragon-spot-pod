"""One normal whole five-stage combined build under the unchanged genuine guard."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SUPPORT=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v19-20261010')
TARGET=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')
TARGET_SHA='34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b'
SOURCE=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010')
TERMINAL=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010')
SEAL_SHA='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
TERM_SHA='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_build_v19_sources')
DECLARATION_SHA='30f64a1704917564125b2a3f13c215959e00c1fa4cc239cb76b11acdbf44f2fb'
PREP_SHA='fca4f17d7336f7de54d13aaa2e8d28e56ffe4d1e35dbe7ac143c02ac3e573f4c'
INNER_FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19'
EXPECTED_LABELS=['build/link', 'metadata/objects', 'metadata/executable', 'metadata/dependencies', 'audit/audit']
EXPECTED_COMMANDS=[['/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', '-O2', '-march=native', '-ffp-contract=off', '-g', '/Users/wen/spot/src/DRAGON.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-compensated-flight-20261004/build/SPOR64_A8.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-compensated-flight-20261004/build/AXMAT_MCGFCF_COMP.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-angular-convergence-20261005/build/axmat_white_trace_model.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/SPOT1P64.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-cold-control-paths-20261004/build/SPOF64.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/FLU2DR64.o', '/Users/wen/spot/validation/artifacts/axial-material-moment-order-build-20261006/build/FLU.o', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o', '/Users/wen/spot/lib/Darwin_arm64/libDragon.a', '/Users/wen/spot/Trivac/lib/Darwin_arm64/libTrivac.a', '/Users/wen/spot/Utilib/lib/Darwin_arm64/libUtilib.a', '/Users/wen/spot/Ganlib/lib/Darwin_arm64/libGanlib.a', '-o', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010/runtime/Dragon'], ['/usr/bin/nm', '-g', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/SPOT1P64.o', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/FLU2DR64.o', '/Users/wen/spot/validation/artifacts/axial-material-moment-order-build-20261006/build/FLU.o'], ['/usr/bin/nm', '-g', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010/runtime/Dragon'], ['/usr/bin/otool', '-L', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/runtime/Dragon'], ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py', 'audit-build', '--sha256', '30f64a1704917564125b2a3f13c215959e00c1fa4cc239cb76b11acdbf44f2fb', '--prep-sha256', 'fca4f17d7336f7de54d13aaa2e8d28e56ffe4d1e35dbe7ac143c02ac3e573f4c']]
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30

def main():
    started=time.monotonic()
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed unprofiled nonoptimized read-only admission host required')
    import hashlib
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:
        raise ValueError('fixed normal support source required')
    spec=importlib.util.spec_from_file_location('axmat_v15_normal_readonly_admission_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    support_pin=support.pin(SUPPORT,SUPPORT_SHA)
    if any(os.environ.get(k)!='1' for k in support.THREAD_KEYS) or Path(sys.executable).resolve()!=support.PYTHON:
        raise ValueError('original single-thread Python required')
    if os.path.lexists(HOST):raise ValueError('fresh one-use whole build host required; no retry')
    if not all(p.is_dir() for p in (SOURCE,OUT,TERMINAL)):raise ValueError('actual prepared SOURCE/OUT/TERMINAL required')
    if any(os.path.lexists(OUT/p) for p in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','audit/binary_identity.json','audit/result.json',INNER_FAMILY+'/stages.json','runtime/Dragon')):raise ValueError('no prior build execution or build retry allowed')
    inputs=[support_pin,support.pin(TARGET,TARGET_SHA),support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA)]+[support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),support.pin(Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json'),'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8')]+[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]
    inputs += [support.pin(OUT/'declaration.json',DECLARATION_SHA),support.pin(TERMINAL/'declaration_terminal_return.json',PREP_SHA),support.pin(OUT/'input_graph.json','257ddbd44f3123dd85f7b0cf50572ca68c92475b9a491ef83d0ec21b74e63d60'),support.pin(OUT/'input_creation_python_open_trace.json','c1e2daeef559de7c518ce7407230c43e5c911062e3d744651e8a6e007dd05712')]
    inputs += [support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]
    inputs += [support.pin(BASE/'actual_complete_combined_prepare_v19_receipts/Root_actual_prepare_tool_terminal_return.json'),support.pin(BASE/'actual_complete_combined_prepare_v19_receipts/Root_actual_complete_combined_prepare_summary.json','17992f59e84611b0456e3451f0e6abbdc56baf2a0e985f5e1ad895d24e52c046')]
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        HOST.mkdir()
        for name in ('runtime','run','COMPLETE_COMBINED_BUILD'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_COMBINED_BUILD',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),str(TARGET),'run-build','--sha256',DECLARATION_SHA,'--prep-sha256',PREP_SHA]
        runner.execute(HOST/'run','build',command,WHOLE_CAP)
        log=HOST/'run/build.log';watch_path=HOST/'run/build.watchdog.json'
        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())
        declaration=OUT/'declaration.json';d=json.loads(declaration.read_text())
        if support.pin(declaration)['sha256']!=DECLARATION_SHA:raise ValueError('immutable declaration changed')
        if d['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_DECLARATION_V1' or d['stages']!=EXPECTED_LABELS or (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'])!=(1800,600,512,2*2**30):raise ValueError('original complete five stages and caps required')
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
        if seal['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_BUILD_SEAL_V1' or seal['symlinks']!={} or seal['directories']!=sorted(directories) or set(files)!=set(seal['files'])|{'seal.json'} or any(files[k]!=v for k,v in seal['files'].items()):raise ValueError('complete original OUT seal required')
        if result['corrected_runtime']!={k:support.pin(OUT/'runtime/Dragon')[k] for k in ('path','sha256')}:raise ValueError('actual built runtime identity required')
        actual_size=support.archive_bytes((SOURCE,OUT));tail_resources=admission['actual_resources']
        if admission['actual_tail_check']!='PASS' or not result['elapsed_seconds']<=admission['actual_elapsed_seconds']<WHOLE_CAP or type(admission['actual_archive_bytes']) is not int or admission['actual_archive_bytes']!=actual_size or not 0<actual_size<ARCHIVE_CAP or tail_resources['artifact_budget_bytes']!=96*2**30 or tail_resources['min_free_bytes']!=8*2**30 or tail_resources['declared_resource_roots']!=d['resource_roots'] or tail_resources['resource_scope_policy']!=d['resource_scope_policy'] or tail_resources['resource_scope_contract']!=d['resource_scope_contract'] or not set(d['resource_roots']).issubset(tail_resources['resource_roots']) or not actual_size<=tail_resources['artifact_bytes']<=96*2**30 or tail_resources['disk_free_bytes']<8*2**30:raise ValueError('all original actual post-seal budget tails required')
        resource.validate_history_roots(tail_resources['resource_roots'],support.ART)
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        value=dict(schema='AXMAT_V19_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',status='ACTUAL_COMPLETE_COMBINED_BUILD_EXTERNAL_ROOT_REQUIRED',input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_build_stdout=support.pin(log),actual_build_seal=support.pin(OUT/'seal.json'),actual_driver_result=support.pin(OUT/'driver_result.json'),actual_inner_stages=inner,actual_inner_watchdogs=inner_watches,actual_tail_fields={k:admission[k] for k in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')},outer_command_wall_cap_seconds=WHOLE_CAP,inner_original_stage_wall_cap_seconds=STAGE_CAP,whole_combined_INPUT_admitted=False,actual_declaration=support.pin(declaration),actual_source_admission=support.pin(SOURCE/'source_admission.json'),actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_build_stdout=support.pin(log),actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()

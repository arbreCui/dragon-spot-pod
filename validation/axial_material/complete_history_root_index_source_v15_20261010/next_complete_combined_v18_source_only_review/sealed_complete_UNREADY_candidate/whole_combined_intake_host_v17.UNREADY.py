'UNREADY bounded whole V17 canonical INPUT admit source-only draft. V17 actual build failed before driver_result/seal; no successful seal/run terminal exists, so this host cannot run. Normal original genuine OwnRSS class/MRO and real complete-history96/free8 resource constructor remain required. Only a later independently qualified fresh family may receive new source retargeting and true actual pins; no retry of failed V17 is authorized. Full canonical descriptor stdout/stderr is retained without field selection.'
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
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-whole-input-admission-host-v17-20261010')
TARGET=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
TARGET_SHA='feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'
SOURCE=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010')
TERMINAL=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010')
SOURCE_ARCHIVE=BASE/'actual_combined_admission_v17_sources'
OUTSIDE_ARCHIVE=BASE/'actual_combined_admission_v17_receipts'
DRAFT_STATUS='UNREADY_SOURCE_ONLY_V17_BUILD_FAILED_NO_SUCCESS_PINS'
SEAL_SHA=None
TERM_SHA=None
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20

def main():
    started=time.monotonic()
    if DRAFT_STATUS!='READY_REVIEWED_FRESH_COMBINED_WHOLE_INPUT_HOST_V17' or any(type(v)is not str or len(v)!=64 or any(c not in '0123456789abcdef'for c in v)or v=='0'*64 for v in (SEAL_SHA,TERM_SHA)):
        raise ValueError('UNREADY: actual V17 failed build has no successful seal or run terminal; no execution or retry')
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
    if os.path.lexists(HOST):raise ValueError('fresh one-use admission host required; no retry')
    inputs=[support_pin,support.pin(TARGET,TARGET_SHA),support.pin(OUT/'seal.json',SEAL_SHA),support.pin(TERMINAL/'terminal_return.json',TERM_SHA),support.pin(Path(__file__).resolve()),support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
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
        for name in ('runtime','run','COMBINED_WHOLE_INPUT_ADMISSION'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMBINED_WHOLE_INPUT_ADMISSION',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),str(TARGET),'admit','--sha256',SEAL_SHA,'--terminal-evidence',str(TERMINAL/'terminal_return.json'),'--terminal-evidence-sha256',TERM_SHA]
        runner.execute(HOST/'run','admit',command,STAGE_CAP)
        log=HOST/'run/admit.log';watch_path=HOST/'run/admit.watchdog.json'
        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())
        if admission['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1' or admission['admission']!='COMBINED_RUNTIME_INPUT_ONLY' or admission['build_seal_sha256']!=SEAL_SHA:
            raise ValueError('real complete normal canonical admission required')
        if any(admission[k] is not False for k in ('native_transport_executed','combined_runtime_native_RSS_proved','trim_native_RSS_proof_obtained','AAA_accuracy_qualified','ABA_admitted','actual_full_FLU_entry_executed','production_pipeline_prepared','original_component_APIs_executed_now')):
            raise ValueError('runtime INPUT only science boundaries required')
        if set(admission['actual_components'])!={'original92','physical','dedup','capture','mathematical_controls_inherited_not_newly_executed','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved'} or admission['complete_literal_owner_edges_preserved_by_graph']is not True or admission['historical_whole_component_body']['whole_seven_key_body_retained']is not True:
            raise ValueError('complete seven-key actual historical body and all graph owner edges required')
        if admission['actual_external_terminal_evidence']!=dict(path=str(TERMINAL/'terminal_return.json'),sha256=TERM_SHA) or admission['actual_prepare_terminal_evidence']['path']!=str(TERMINAL/'declaration_terminal_return.json'):
            raise ValueError('actual successful fresh Root build/PREP terminal bindings required')
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,SOURCE_ARCHIVE,OUTSIDE_ARCHIVE))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        value=dict(schema='AXMAT_V17_GENUINE_COMBINED_WHOLE_INPUT_ADMISSION_HOST_V1',status='ACTUAL_COMBINED_WHOLE_INPUT_ONLY_EXTERNAL_ROOT_REQUIRED',input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_admission_stdout=support.pin(log),actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,SOURCE_ARCHIVE,OUTSIDE_ARCHIVE))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_admission_stdout=support.pin(log),actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_READONLY_ADMISSION_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()

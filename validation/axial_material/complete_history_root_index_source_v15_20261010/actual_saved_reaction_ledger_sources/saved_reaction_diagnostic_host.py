"""One complete saved reaction/flux diagnostic under the unchanged genuine guard."""
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
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-host-20261010')
TARGET=Path('/Users/wen/spot/validation/axial_material/refined_AAA_full_group_source_reaction_ledger_diagnostic_20261010.py')
TARGET_SHA='4851d9151dfe5682a36f450fff8d0acb42c69865e177affe81c4b703119f7874'
OUTPUT=Path('/Users/wen/spot/validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-20261010')
SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_saved_reaction_ledger_sources')
SEAL_SHA='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
TERM_SHA='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20

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
    if any(os.path.lexists(p) for p in (HOST,OUTPUT)):raise ValueError('fresh one-use saved diagnostic namespaces required; no retry')
    inputs=[support.pin(TARGET,TARGET_SHA),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/bootstrap/initial_axial_track.xsm'),'b8302889d66f37947b3060f5caef2be43c7da5dfd6673daaa1ffb66fd81997d6'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/bootstrap/initial_axial_macrolib.xsm'),'bca18875dbde9b5ae14f916f3df902ab071c173adff02c1b09ef647116282510'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/map012/closed_axial.xsm'),'fcb6e4144a05d943f5a54637c0124ec59498b7176ca077db295f0878ef60e01a'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/map012/candidate_system.xsm'),'994bacfea61f3145d0ba73f7889494215bca77fb5a341152fdd652e8f168c5e4'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/run_status.json'),'1acb16adc59f91e66599f74d11993d300bae73647dc870d148936935d199012f'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/AAA/map012/result.json'),'f3716289ced3716fa89747ecb99b01757cd8d0f85ed202548f2fb68d5518606c'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/prepared.json'),'024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AAA-white-trace-refined-observables-20261005/protocol.json'),'3f5c23d7d79c8d26162229d1cda51d3ee2218645222c8aec27b428280a93cadf'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AAA-white-trace-refined-observables-20261005/observables.regions.csv'),'2fd4096bf31098cc8323fd7eae791a5c1bedb10bf01daf8a637a3c238b256327'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AAA-white-trace-refined-observables-20261005/observables.faces.csv'),'02f9d68c41f2bd0be79f691094db862fa6cfaee371071c094e3ad1b0322057b9'),support.pin(Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AAA-white-trace-refined-observables-20261005/observables.summary.txt'),'7b430da7fc916ee54abefba63e4ad21e0c490826bbf8170e9d176995e9171612'),support_pin,support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA)]
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    roots=resource.history_roots([str(HOST),str(OUTPUT),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        HOST.mkdir()
        for name in ('runtime','run','SAVED_REACTION_DIAGNOSTIC'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'SAVED_REACTION_DIAGNOSTIC',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),'-B',str(TARGET),'--evaluator-sha256',TARGET_SHA,'--out-root',str(OUTPUT)]
        runner.execute(HOST/'run','admit',command,STAGE_CAP)
        log=HOST/'run/admit.log';watch_path=HOST/'run/admit.watchdog.json'
        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())
        report=json.loads((OUTPUT/'result.json').read_text());manifest=json.loads((OUTPUT/'payload_manifest.json').read_text())
        if admission['classification']!='ALL_370_GROUP_SAVED_SOURCE_REACTION_FLUX_DIAGNOSTICS_COMPLETE_NOT_PHYSICAL_BALANCE_QUALIFIED' or report['classification']!=admission['classification'] or admission['scientific_accuracy_qualified'] is not False:raise ValueError('actual saved diagnostic scope required')
        if any(report[k] is not False for k in ('scientific_accuracy_qualified','AAA_qualified','ABA_admitted','same_MG_unreduced_reference_qualified','reaction_raw_transfer_equivalence_qualified','full_physical_neutron_balance_qualified','transport_launched','basis_rank_or_white_coefficients_modified')):raise ValueError('full saved diagnostic no science qualification required')
        if report['dimensions']!={'groups':370,'mixtures':24,'fission_components':32,'cells':384,'faces':392,'radial_regions':8,'axial_cells':48,'unknowns_per_group':1800} or report['full_group_fine_cell_coverage'] is not True:raise ValueError('all groups cells faces required')
        if admission['result']!=str(OUTPUT/'result.json') or admission['sha256']!=support.pin(OUTPUT/'result.json')['sha256'] or admission['payload_manifest']!=str(OUTPUT/'payload_manifest.json') or admission['manifest_sha256']!=support.pin(OUTPUT/'payload_manifest.json')['sha256']:raise ValueError('actual complete payload result pins required')
        actual={str(p.relative_to(OUTPUT)):support.pin(p)['sha256'] for p in OUTPUT.rglob('*') if p.is_file() and p.name!='payload_manifest.json'}
        if actual!={k:v['sha256'] for k,v in manifest['files'].items()}:raise ValueError('entire actual payload manifest required')
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,OUTPUT,SOURCE_ARCHIVE))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        value=dict(schema='AXMAT_GENUINE_SAVED_FULL_GROUP_REACTION_DIAGNOSTIC_HOST_V1',status='ACTUAL_SAVED_FULL_GROUP_REACTION_DIAGNOSTIC_EXTERNAL_ROOT_REQUIRED',input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_diagnostic_stdout=support.pin(log),actual_diagnostic_result=support.pin(OUTPUT/'result.json'),actual_diagnostic_manifest=support.pin(OUTPUT/'payload_manifest.json'),actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,OUTPUT,SOURCE_ARCHIVE))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_diagnostic_stdout=support.pin(log),actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_SAVED_REACTION_DIAGNOSTIC_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()

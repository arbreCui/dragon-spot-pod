"""One isolated real runtime-input API child under the genuine fixed supervisor.

Only this standalone process imports the producer's canonical modules. No cold
controller is imported, rebound or launched. The child is the actual three-arg
API CLI, with the original 1800/600/512, one-thread/one-child/no-retry guards.
Its complete combined stdout/stderr stream is retained; no separate child
stderr observation is claimed. Root must observe this host's actual return.
"""
import sys,os,time,json,hashlib,importlib.util,shutil
from pathlib import Path
DRAFT_STATUS='READY_REVIEWED_FACTOR_DIAGONAL_TRIM_V10_STANDALONE_INPUT_ONLY'
if DRAFT_STATUS!="READY_REVIEWED_FACTOR_DIAGONAL_TRIM_V10_STANDALONE_INPUT_ONLY":raise ValueError("UNREADY: no actual new intake or component evidence")
STARTED=time.monotonic()
if sys.flags.optimize!=0 or os.environ.get('PYTHONOPTIMIZE'):raise ValueError('nonoptimized Python required')
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
if any(os.environ.get(k)!='1'for k in THREAD_KEYS):raise ValueError('single-thread environment required')
sys.dont_write_bytecode=True
PYTHON='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py')
FACTORY_SHA='c55ca2680d9e1326979649f835d9612a8fd80df5aecee1adc25765c419329efc'
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-factor-diagonal-trim-live-resource-scopes-v10-20261009')
TERM=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-factor-diagonal-trim-live-resource-scopes-v10-20261009')
SEAL_SHA='3d1094466cb03a08d3bdb08eee0a1f4f3c2b75bb676400beaf5fe7a4892001b5'
RUN_SHA='aec9364827742e68d545ef7ea63ad7d656201c9de13938a1ddceb4b13bbc2bd9'
PREP_SHA='defbc6c30603c334f7c1f8c883c4fb4af6c8fb6cc7ea2ae8df41591be0872658'
BASE=Path('/private/tmp/axmat-factor-diagonal-trim-v10-standalone-bounded-runtime-api-intake-20261009')
FAMILY='STANDALONE_BOUNDED_RUNTIME_API_INTAKE'
DECL_SHA='32370a3b0daee193b48a70de428397ccb3a65793fbefc4f5d60b8698d592356a'
for value in (DECL_SHA,SEAL_SHA,RUN_SHA,PREP_SHA):
 if type(value)is not str or len(value)!=64 or any(c not in '0123456789abcdef'for c in value)or value=='0'*64:raise ValueError('UNREADY: exact actual component pins required')
if str(Path(sys.executable).resolve())!=PYTHON:raise ValueError('actual build Python3.12 required')
if hashlib.sha256(FACTORY.read_bytes()).hexdigest()!=FACTORY_SHA:raise ValueError('formal producer changed')
spec=importlib.util.spec_from_file_location('actual_standalone_bounded_runtime_input_producer',FACTORY)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f);f.require_ready()
d=f.read(f.require(OUT/'declaration.json',DECL_SHA))
f.require(OUT/'seal.json',SEAL_SHA);f.require(TERM/'terminal_return.json',RUN_SHA);f.require(TERM/'declaration_terminal_return.json',PREP_SHA)
b,h,full,c=f.modules()
if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):raise ValueError('genuine supervisor MRO required')
if f.pin(Path(full.__file__).resolve())!=d['genuine_supervisor_source']or f.pin(Path(c.__file__).resolve())!=d['genuine_parent_class_source']:
 raise ValueError('original direct supervisor/parent sources differ')
resources=f.resources_for(d['resource_roots'],c.ResourceFailure);before=resources.check()
f.absent(BASE);BASE.mkdir();(BASE/'runtime').mkdir();(BASE/'intake').mkdir();(BASE/FAMILY).mkdir()
shutil.copy2(f.require(OUT/'runtime/run_bounded_dragon.py',f.BOUNDED_SHA),BASE/'runtime/run_bounded_dragon.py')
runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)
if Path(runner.bounded.__file__).resolve()!=BASE/'runtime/run_bounded_dragon.py'or type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:
 raise ValueError('actual copied bounded helper/constructor differs')
command=[PYTHON,str(FACTORY),'admit','--sha256',SEAL_SHA,'--terminal-evidence',str(TERM/'terminal_return.json'),'--terminal-evidence-sha256',RUN_SHA]
runner.execute(BASE/'intake','admit',command,600)
log=BASE/'intake/admit.log';body=f.read(log)
if (body['schema']!=f.PREFIX+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'or body['admission']!='COMBINED_RUNTIME_INPUT_ONLY'
 or body['actual_external_terminal_evidence']!=dict(path=str(TERM/'terminal_return.json'),sha256=RUN_SHA)
 or body['actual_prepare_terminal_evidence']!=dict(path=str(TERM/'declaration_terminal_return.json'),sha256=PREP_SHA)
 or any(body[k]is not False for k in ('original_component_APIs_executed_now','production_pipeline_prepared','native_transport_executed',
 'combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):raise ValueError('whole true INPUT-only API return required')
watch=f.read(log.with_suffix('.watchdog.json'));elapsed=time.monotonic()-STARTED;after=resources.check()
if (len(runner.records)!=1 or runner.records[0]['status']!='PASS'or runner.records[0]['command']!=command
 or type(watch['returncode'])is not int or watch['returncode']!=0 or watch['command']!=command
 or watch['limit_failure']is not None or not 0<=watch['sampled_peak_rss_mib']<512
 or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True or not elapsed<1800):raise ValueError('actual complete guarded API child required')
result=dict(schema='AXMAT_OWNED_SPECS_STANDALONE_BOUNDED_RUNTIME_API_INTAKE_ACTUAL_HOST_V1',
 producer=f.pin(FACTORY),declaration=f.pin(OUT/'declaration.json'),build_seal=f.pin(OUT/'seal.json'),
 actual_run=f.pin(TERM/'terminal_return.json'),actual_PREP=f.pin(TERM/'declaration_terminal_return.json'),
 actual_API_whole_merged_stream=f.pin(log),child_stderr_combined_into_actual_log=True,separate_child_stderr_observation_claimed=False,
 actual_API_whole_return=f.pin(log),supervisor_source=f.pin(Path(full.__file__).resolve()),parent_source=f.pin(Path(c.__file__).resolve()),
 bounded_helper=f.pin(BASE/'runtime/run_bounded_dragon.py'),actual_command=command,stage_records=runner.records,watchdog=watch,
 resources_before=before,resources_after=after,whole_elapsed_seconds=elapsed,threads=1,children_at_once=1,retries=0,
 total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,canonical_old_modules_only_in_isolated_process=True,
 cold_controller_imported=False,cold_controller_bound=False,cold_prepared=False,physics_or_native_transport_executed=False,
 combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
f.write_new(BASE/'result.json',result)
print(json.dumps(result,allow_nan=False),flush=True)

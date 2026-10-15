"""STOPPED one-child input allocation diagnostic under the fixed real supervisor.

This source wrapper reuses the original 705/38de/bc4 supervisor and limits.
The child produces a multi-line boundary log and a separate small result, not
an API return. Only Root-observed actual tool output can establish its exit.
"""
import sys,os,time,json,hashlib,importlib,shutil,argparse
from pathlib import Path
STARTED=time.monotonic()
if sys.flags.optimize!=0 or os.environ.get('PYTHONOPTIMIZE'):raise ValueError('nonoptimized Python required')
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
if any(os.environ.get(k)!='1'for k in THREAD_KEYS):raise ValueError('single-thread environment required')
sys.dont_write_bytecode=True
parser=argparse.ArgumentParser();parser.add_argument('--config',required=True);parser.add_argument('--config-sha256',required=True);args=parser.parse_args()
payload=Path(args.config).read_bytes()
if hashlib.sha256(payload).hexdigest()!=args.config_sha256:raise ValueError('external diagnostic config SHA differs')
config=json.loads(payload);del payload
if config['schema']!='AXMAT_TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC_CONFIG_V1'or config['status']!='READY_ROOT_REVIEWED_INPUT_DIAGNOSTIC_ONLY':raise ValueError('UNREADY: source-only stopped diagnostic')
if config['caps']!=dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0):raise ValueError('original diagnostic caps differ')
PYTHON=config['python_executable'];FACTORY=Path(config['factory']['path']);FACTORY_SHA=config['factory']['sha256']
OUT=Path(config['declaration']['path']).parent;TERM=Path(config['actual_PREP']['path']).parent
BASE=Path(config['base']);FAMILY=config['family']
if str(Path(sys.executable).resolve())!=PYTHON:raise ValueError('actual build Python3.12 required')
for descriptor in (config['host_source'],config['child_source'],config['factory']):
 path=Path(descriptor['path'])
 if not path.is_absolute()or path.is_symlink()or path.resolve(strict=True)!=path or hashlib.sha256(path.read_bytes()).hexdigest()!=descriptor['sha256']:raise ValueError('actual ordinary wrapper/source differs')
if Path(__file__).resolve()!=Path(config['host_source']['path']):raise ValueError('actual host source binding differs')
if hashlib.sha256(FACTORY.read_bytes()).hexdigest()!=FACTORY_SHA:raise ValueError('formal producer changed')
name=FACTORY.stem;prior=sys.modules.get(name)
if prior is not None and Path(prior.__file__).resolve()!=FACTORY:raise ValueError('foreign pre-existing producer module')
sys.path.insert(0,str(FACTORY.parent));f=importlib.import_module(name)
if f.__name__!=name or Path(f.__file__).resolve()!=FACTORY or f.__spec__ is None or Path(f.__spec__.origin).resolve()!=FACTORY:raise ValueError('normal canonical producer import required')
f.require_ready()
d=f.read(f.require(OUT/'declaration.json',config['declaration']['sha256']))
f.require(TERM/'declaration_terminal_return.json',config['actual_PREP']['sha256'])
b,h,full,c=f.modules()
if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):raise ValueError('genuine supervisor MRO required')
if f.pin(Path(full.__file__).resolve())!=d['genuine_supervisor_source']or f.pin(Path(c.__file__).resolve())!=d['genuine_parent_class_source']:
 raise ValueError('original direct supervisor/parent sources differ')
if d['genuine_supervisor_source']!=config['supervisor_source']or d['genuine_parent_class_source']!=config['parent_source']:raise ValueError('config genuine fixed source binding differs')
resources=f.resources_for(d['resource_roots'],c.ResourceFailure);before=resources.check()
if BASE.parent!=f.ART or not BASE.name.startswith('axial-material-')or FAMILY!='TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC':raise ValueError('exclusive diagnostic axial family required')
f.absent(BASE);BASE.mkdir();(BASE/'runtime').mkdir();(BASE/'diagnostic').mkdir();(BASE/FAMILY).mkdir()
shutil.copy2(f.require(OUT/'runtime/run_bounded_dragon.py',f.BOUNDED_SHA),BASE/'runtime/run_bounded_dragon.py')
if f.BOUNDED_SHA!=config['bounded_helper_sha256']:raise ValueError('actual bc4 helper binding differs')
runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)
if Path(runner.bounded.__file__).resolve()!=BASE/'runtime/run_bounded_dragon.py'or type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:
 raise ValueError('actual copied bounded helper/constructor differs')
command=[PYTHON,config['child_source']['path'],'--config',str(Path(args.config).resolve()),'--config-sha256',args.config_sha256]
runner.execute(BASE/'diagnostic','declaration-input',command,600)
log=BASE/'diagnostic/declaration-input.log'
# The complete merged log is raw evidence. It is deliberately not parsed as one API JSON.
body=f.read(Path(config['result_path']))
if (body['schema']!='AXMAT_TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC_CHILD_V1'
 or body['classification']!='COMPLETE_INPUT_ADMISSION_ALLOCATION_DIAGNOSTIC_ONLY'
 or body['factory']!=config['factory']or body['declaration']!=config['declaration']or body['actual_PREP']!=config['actual_PREP']
 or body['actual_input_admission_returned']is not True or body['actual_true_build_interpreter_branch']is not True
 or body['profile_disabled']is not True or body['genuine_constructor_preflight_in_true_original_call']is not True
 or body['profiling_overhead_is_inside_limits']is not True
 or any(body[k]is not False for k in ('audit_build_executed','production_admission_executed','new_build_seal_admitted',
 'native_or_numerical_child_executed','cold_prepared','combined_runtime_native_RSS_proved','AAA_accuracy_qualified','ABA_admitted'))):raise ValueError('complete input-only diagnostic result required')
watch=f.read(log.with_suffix('.watchdog.json'));elapsed=time.monotonic()-STARTED;after=resources.check()
if (len(runner.records)!=1 or runner.records[0]['status']!='PASS'or runner.records[0]['command']!=command
 or type(watch['returncode'])is not int or watch['returncode']!=0 or watch['command']!=command
 or watch['limit_failure']is not None or not 0<=watch['sampled_peak_rss_mib']<512
 or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True or not elapsed<1800):raise ValueError('actual complete guarded diagnostic child required')
archive_bytes=sum(path.stat().st_size for path in BASE.rglob('*')if path.is_file()and not path.is_symlink())
if archive_bytes>=2*2**30:raise ValueError('diagnostic SOURCEOUT2GiB limit exceeded')
result=dict(schema='AXMAT_TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC_ACTUAL_HOST_V1',
 classification='COMPLETE_GUARDED_INPUT_ALLOCATION_DIAGNOSTIC_ONLY',
 producer=f.pin(FACTORY),declaration=f.pin(OUT/'declaration.json'),actual_PREP=f.pin(TERM/'declaration_terminal_return.json'),
 diagnostic_config=dict(path=str(Path(args.config).resolve()),sha256=args.config_sha256),
 child_source=config['child_source'],host_source=config['host_source'],
 actual_child_whole_merged_stream=f.pin(log),child_stderr_combined_into_actual_log=True,separate_child_stderr_observation_claimed=False,
 actual_child_result=f.pin(Path(config['result_path'])),supervisor_source=f.pin(Path(full.__file__).resolve()),parent_source=f.pin(Path(c.__file__).resolve()),
 bounded_helper=f.pin(BASE/'runtime/run_bounded_dragon.py'),actual_command=command,stage_records=runner.records,watchdog=watch,
 resources_before=before,resources_after=after,whole_elapsed_seconds=elapsed,archive_bytes_before_result=archive_bytes,
 threads=1,children_at_once=1,retries=0,total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,
 allocation_profile_not_normal_performance_measurement=True,cold_controller_imported=False,cold_controller_bound=False,
 cold_prepared=False,physics_or_native_transport_executed=False,combined_runtime_native_RSS_proved=False,
 actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
f.write_new(BASE/'result.json',result)
if sum(path.stat().st_size for path in BASE.rglob('*')if path.is_file()and not path.is_symlink())>=2*2**30:raise ValueError('complete diagnostic SOURCEOUT2GiB limit exceeded')
print(json.dumps(result,allow_nan=False),flush=True)

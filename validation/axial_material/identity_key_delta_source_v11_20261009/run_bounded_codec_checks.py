"""New identity codec primitive checks only. No transport or full component admission."""
import ast, hashlib, importlib.util, json, os, sys, time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot')
SRC=ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009'
OUT=ROOT/'validation/artifacts/axial-material-rank1-cross-group-key-delta-codec-checks-v11-20261009'
FAMILY='IDENTITY_KEY_DELTA_CODEC_CHECKS_V11'
CAPS=dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,archive_reserve_bytes=2*2**30,history_cap_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,numeric_children_at_once=1,retries=0)
PINS={
 SRC/'SPOT1P64.f90':'0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5',
 SRC/'keycodec_controls.f90':'3f59d94d49c049b206419b49c3a3ac437aa3d980548ab8fb27632ba4dfd472f7',
 ROOT/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_factor_diagonal_trim_production.py':'d82d89daa779c8e1f3087e5c49f05279d35a9b3320ea1ae0257f7eaa586ebc8e',
}
def pin(p):
 b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(p,d):
 if p.exists():raise ValueError('fresh codec paths required: '+str(p))
 p.write_text(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n')
def archive_bytes():
 return sum(p.stat().st_size for base in (SRC,OUT) for p in base.rglob('*') if p.is_file() and not p.is_symlink())
def load(p,name):
 sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
started=time.monotonic()
for p,h in PINS.items():
 if pin(p)['sha256']!=h:raise ValueError('source pin differs: '+str(p))
if Path(sys.executable).resolve()!=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12').resolve():raise ValueError('original P12 build interpreter required')
if OUT.exists():raise ValueError('one fresh codec attempt; no retry')
f=load(next(p for p in PINS if p.name.startswith('prepare_qualified')),'actual_v10_factory_for_original_bounded_unit_guard')
d=f.read(f.require(ROOT/'validation/artifacts/axial-material-rank1-factor-cache-factor-diagonal-trim-build-20261009/declaration.json','f03dab4ce9e8376b4f64491dc934489df1ddd766c3bd38e4ba58a1771c966501'))
f.environment(d)
h=f.helper();full,production=h.modules();guard=h.guard_admission(full)
resources=f.resources_for([*d['resource_roots'],SRC,OUT],production.ResourceFailure)
snapshot=resources.check()
if snapshot['artifact_bytes']+CAPS['archive_reserve_bytes']>CAPS['history_cap_bytes']:raise ValueError('original complete history reservation')
if snapshot['free_bytes']-CAPS['archive_reserve_bytes']<CAPS['min_free_bytes']:raise ValueError('original free reservation')
OUT.mkdir();(OUT/'build').mkdir();(OUT/'runtime').mkdir()
compile_kernel=list(d['build_commands'][0]);oldbuild=str(f.OUT/'build');newbuild=str(OUT/'build')
compile_kernel=[x.replace(oldbuild,newbuild) for x in compile_kernel]
compile_kernel[compile_kernel.index('-c')+1]=str(SRC/'SPOT1P64.f90');compile_kernel[compile_kernel.index('-o')+1]=str(OUT/'build/SPOT1P64.o')
compile_driver=list(compile_kernel);compile_driver[compile_driver.index('-c')+1]=str(SRC/'keycodec_controls.f90');compile_driver[compile_driver.index('-o')+1]=str(OUT/'build/keycodec_controls.o')
compiler=d['build_commands'][0][0];link_flags=['-O2','-march=native','-ffp-contract=off','-g']
libs=d['build_commands'][5][-6:-2]
if len(libs)!=4 or not all(x.endswith('.a') for x in libs):raise ValueError('original four static kernel libraries')
white=str(f.WHITE_OBJECT)
link_driver=[compiler,*link_flags,str(OUT/'build/keycodec_controls.o'),str(OUT/'build/SPOT1P64.o'),white,*libs,'-o',str(OUT/'runtime/keycodec_controls')]
descriptor=[compiler,*link_flags,'-I'+newbuild,'-I'+str(f.ANG),str(SRC/'descriptor_sizes.f90'),'-o',str(OUT/'runtime/descriptor_sizes')]
mutations=['unchanged_word','difference_word','stored_difference_word','base_word','input_length','load_length','ineligible_existing','corrupt_index_zero','corrupt_index_high','missing_anchor']
commands=[('build/kernel',compile_kernel,0),('build/driver',compile_driver,0),('build/link',link_driver,0),('build/descriptor',descriptor,0),('descriptor/execute',[str(OUT/'runtime/descriptor_sizes')],0),('positive/execute',[str(OUT/'runtime/keycodec_controls'),'positive'],0)]
commands.extend((f'negative_{name}_p{phase}/execute',[str(OUT/'runtime/keycodec_controls'),'negative',name,str(phase)],23) for phase in (1,2) for name in mutations)
write(OUT/'declaration.json',dict(classification='PRIMITIVE_CODEC_CHECKS_ONLY_NOT_ORIGINAL45_OR_TRANSPORT',caps=CAPS,inputs={str(p):pin(p) for p in PINS},descriptor_source=pin(SRC/'descriptor_sizes.f90'),original_build_declaration=pin(f.OUT/'declaration.json'),genuine_guard_sources=[pin(p) for p in guard],commands=commands,resources_before=snapshot,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
write(OUT/'execution_claim.json',dict(parent_pid=os.getpid(),started_unix=time.time(),retries=0))
remaining=CAPS['total_wall_seconds']-(time.monotonic()-started)
runner=full.OwnRSSSerialExecutor(OUT,remaining,FAMILY,resources)
result=dict(classification='FAILED_CODEC_CHECKS_NO_RETRY',completed=[],original45_controls_completed=False,actual_full_FLU_entry_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
try:
 for label,command,expected in commands:
  f.environment(d)
  folder=OUT/Path(label).parent;folder.mkdir(parents=True,exist_ok=True);error=None
  try:runner.execute(folder,Path(label).name,command,CAPS['stage_wall_seconds'])
  except BaseException as exc:
   error=repr(exc)
   if expected==0:raise
  watch=json.loads((OUT/(label+'.watchdog.json')).read_text())
  if watch['command']!=command or watch['returncode']!=expected or watch['limit_failure'] is not None or watch['sampled_peak_rss_mib']>=512 or watch['elapsed_seconds']>=600:raise ValueError('actual primitive stage cap/exit differs: '+label)
  if expected==23:
   if error is None or (folder/'unexpected_return.txt').exists() or (folder/'actual_xabort.txt').read_text()!='SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.\n':raise ValueError('negative must actually reject exact mutation: '+label)
  elif error is not None:raise ValueError('unexpected positive error')
  result['completed'].append(dict(label=label,expected_returncode=expected,actual_watchdog=pin(OUT/(label+'.watchdog.json')),expected_rejection=expected==23,actual_supervisor_error=error))
  print(label+' CLOSED expected_exit='+str(expected),flush=True)
  if archive_bytes()>CAPS['archive_reserve_bytes'] or time.monotonic()-started>=1800:raise ValueError('original whole primitive archive/time cap')
 resources.check()
 result.update(classification='ACTUAL_CODEC_OPERATIONS_CLOSED_EXTERNAL_BYTE_AUDIT_REQUIRED',actual_elapsed_seconds=time.monotonic()-started,actual_archive_bytes=archive_bytes(),actual_tail_check=True,actual_resources=resources.check(),all_declared_operations_executed=True,positive_count=1,expected_negative_rejection_count=20)
finally:
 write(OUT/'driver_result.json',result)

"""Complete current Source-only host support. Imports the unchanged original guard.

No code below runs a child at import. The owning Root alone executes the entry
hosts after current actual controls close. Internal labels do not authenticate
producer files: exact fullEOF SHA and all seven identity fields remain mandatory.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import shutil
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
REC = ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE = Path(__file__).resolve().parent
BIND = BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'
SUPPORT = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FLAGS = ['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']
CASE_NAMES = ['positive','global_wrong_scope','missing_producer_seal','root_flux32_disguised',
 'wrong_root_mirror','missing_global64','bad_seed_epoch','fabricated_projected',
 'uncommitted_source','wrong_source_epoch','wrong_source_dimensions','mutated_macro',
 'mutated_track','mutated_system','different_route','qfiss32_disguised','coherent_source_tamper']

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);before=identity(p)
    if not stat.S_ISREG(before[2]):raise RuntimeError('regular non-symlink input required: '+str(p))
    with p.open('rb') as f:
        s=os.fstat(f.fileno())
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=before:
            raise RuntimeError('opened7ID differs')
        sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=before:
            raise RuntimeError('fullEOF7ID differs')
    if identity(p)!=before:raise RuntimeError('after7ID differs')
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)

def same_pin(p,wanted):
    actual=pin(p)
    if any(actual[k]!=wanted[k] for k in ('path','sha256','size_bytes','identity')):
        raise RuntimeError('current fullEOF SHA/7ID differs: '+str(p))
    return actual

def write(p,d):
    with Path(p).open('x') as f:
        json.dump(d,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def verify_rows(rows):
    for row in rows:same_pin(row['path'],row)

def load_json_exact(path,sha,seven):
    p=pin(path)
    if p['sha256']!=sha or p['identity']!=json.loads(seven):raise RuntimeError('external owning report fullpin')
    return json.loads(Path(path).read_text()),p

def closed_report(d,helper,root,count):
    if d.get('failure') is not None or d.get('after_check_error') is not None:
        raise RuntimeError('actual prerequisite report failure')
    if d.get('original_guard_class')!='OwnRSSSerialExecutor' or d.get('original_guard_MRO_unchanged') is not True:
        raise RuntimeError('actual original prerequisite guard')
    if type(d.get('SELF_peak_bytes')) is not int or not 0<=d['SELF_peak_bytes']<512*2**20:
        raise RuntimeError('actual prerequisite SELF cap')
    if type(d.get('wall_seconds')) not in (int,float) or not 0<d['wall_seconds']<1800:
        raise RuntimeError('actual prerequisite whole cap')
    if len(d['records'])!=count:raise RuntimeError('actual prerequisite complete stage count')
    verify_rows(d['fixed_current_pins']);verify_rows(d['output_pins'])
    for record in d['records']:
        if record['status']!='PASS':raise RuntimeError('actual prerequisite non-PASS stage')
        helper.check_watch(root,record)

def admit17(path,sha,seven,helper):
    d,p=load_json_exact(path,sha,seven)
    if p!=json.loads(BIND.read_text())['selected_actual_current17_report']:
        raise RuntimeError('exact Root-selected current17 report fullpin required')
    if d.get('schema')!='ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V2' or d.get('status')!='ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY':
        raise RuntimeError('current corrected connected17 V2 actual terminal required')
    closed_report(d,helper,Path(path).parent,20)
    if d.get('actual_logical_control_count')!=17 or d.get('actual_run_phase_count')!=18 or d.get('all17_original_names_exercised') is not True:
        raise RuntimeError('all17 actual logical controls required')
    # The actual running host states its precise oracle authority. Same-schema
    # older or unqualified JSON may also be frozen inputs; none is a candidate.
    # Inspect only the explicit Root-selected report, never scan directories.
    table={}
    for row in d['fixed_current_pins']:
        if row['path'] in table and table[row['path']]!=row:
            raise RuntimeError('same fixed path with inconsistent complete pins')
        table[row['path']]=row
    authority=d['actual_current_control_binding_pin']
    source=d['actual_current_control_source_pin'];freeze=d['actual_current_control_freeze_pin']
    for row in (authority,source,freeze):
        if table.get(row['path'])!=row:raise RuntimeError('actual own-host authority pin absent from fixed inputs')
        same_pin(row['path'],row)
    oracle=json.loads(Path(authority['path']).read_text())
    if not str(oracle.get('schema','')).startswith('CURRENT_COMPLETE_ROOT64_CONNECTED17_FIXED_SOURCE_ORACLE_AND_COMMAND_BINDING'):
        raise RuntimeError('actual corrected full17 oracle protocol')
    actual_commands=[r['command']for r in d['records']]
    planned=[oracle['planned_compile_command'],oracle['planned_link_command']]+oracle['planned_run_commands']
    if oracle['planned_output_root']!=str(Path(path).parent) or planned!=actual_commands or len(planned)!=20:
        raise RuntimeError('actual20 commands from the exact owning current oracle')
    if source!=oracle['source_pin'] or source['path']not in oracle['planned_compile_command']:
        raise RuntimeError('actual active complete control Source differs from current oracle/compiler command')
    package=json.loads(Path(freeze['path']).read_text())
    package_rows=package.get('complete_package_file_pins_before_manifest',[])+package.get('actual_dependency_full_EOF_pins',[])
    if not package_rows:raise RuntimeError('actual complete Source freeze dependency and package pins')
    package_table={}
    for row in package_rows:
        if row['path']in package_table and package_table[row['path']]!=row:
            raise RuntimeError('inconsistent actual freeze path pins')
        package_table[row['path']]=row
        same_pin(row['path'],row)
    if package_table.get(source['path'])!=source or package_table.get(authority['path'])!=authority:
        raise RuntimeError('actual current Source and oracle not both in the genuine complete package freeze')
    required=json.loads(BIND.read_text())['seventeen_required_same_production_object_pins']
    if len(required)!=9:raise RuntimeError('complete nine genuine production-object equality gate')
    for row in required:
        if row['path'] not in oracle['planned_link_command'] or table.get(row['path'])!=row:
            raise RuntimeError('actual17 object differs from exact current production runtime')
        same_pin(row['path'],row)
    if oracle['original_case_names']!=CASE_NAMES:raise RuntimeError('original17 exact names')
    phases=[(n,'single')for n in CASE_NAMES[:16]]+[(CASE_NAMES[-1],'prepare'),(CASE_NAMES[-1],'rewrite')]
    if len(d['actual_cases'])!=18:raise RuntimeError('complete actual18 phases')
    for row,(name,phase) in zip(d['actual_cases'],phases):
        a=row['assertions'];c=row['actual_statuses_and_call_counts']
        if (row['case'],row['phase'])!=(name,phase) or a.get('all_actual_assertions_completed') is not True:
            raise RuntimeError('actual17 assertion order/phase')
        declared=next(x for x in oracle['declared_case_oracles'] if x['case']==name)
        for key,value in declared.items():
            if key.startswith(('expected_actual_','expected_explicit_')) and c.get(key[9:])!=value:
                raise RuntimeError('actual V2 count/status oracle '+name+' '+key)
        if any(a.get(k) is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
            raise RuntimeError('17 synthetic scope')
    e=d['actual_independent_host_coherent_refusal']
    if e['actual_refused'] is not True or e['Fortran_internal_refusal_claimed'] is not False:
        raise RuntimeError('independent owning host actual coherent refusal')
    if e['before']['sha256']==e['after']['sha256'] or e['before']['identity']==e['after']['identity']:
        raise RuntimeError('actual coherent complete-file mutation')
    baseline=d['independent_coherent_baseline_manifest_pin'];same_pin(baseline['path'],baseline)
    if json.loads(Path(baseline['path']).read_text())['actual_before_pin']!=e['before']:
        raise RuntimeError('independent real before manifest differs from actual refusal baseline')
    return d,p

def initialize(out,start):
    if len(sys.argv)==1:raise RuntimeError('mandatory owning current17 report fullpin arguments')
    if out.exists() or out.is_symlink():raise RuntimeError('fresh namespace, once, no retry or overwrite')
    if any(os.environ.get(k)!='1' for k in THREADS) or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise RuntimeError('original one-thread nonoptimized unprofiled environment')
    if pin(SUPPORT)['sha256']!=SUPPORT_SHA:raise RuntimeError('original exact support Source')
    spec=importlib.util.spec_from_file_location('current_warm_original_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
    if Path(sys.executable).resolve()!=support.PYTHON:raise RuntimeError('original exact Python')
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'current_warm_original_helper')
    factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'current_warm_original_resources')
    full,production=helper.modules();guard_files=helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise RuntimeError('original supervisor MRO and genuine Source paths')
    binding=json.loads(BIND.read_text());verify_rows(binding['fixed_current_pins'])
    fixed=binding['fixed_current_pins']+[pin(BIND)]+[pin(p)for p in guard_files]
    history=factory.DynamicHistoryResources(ART,factory.history_roots([str(out)],ART),8*2**30,96*2**30,production.ResourceFailure)
    fresh=production.DiskResources(ART,[str(out)],8*2**30,2*2**30)
    class Resources:
        def check(self):
            h=history.check();f=fresh.check()
            if h['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB original cold reserve')
            if f['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('filesystem8GiB original reserves')
            return dict(h,fresh_output=f)
    resources=Resources();before=resources.check()
    return binding,fixed,support,helper,full,resources,before

def create_runtime(out,start,support,full,resources,binding,case):
    out.mkdir();(out/'runtime').mkdir();(out/'build').mkdir();(out/case).mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py')
    shutil.copy2(binding['current_POD56_Dragon']['path'],out/'runtime/Dragon')
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),case,resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=out/'runtime/run_bounded_dragon.py':
        raise RuntimeError('genuine current runner binding')
    owned=[pin(out/'runtime/run_bounded_dragon.py'),pin(out/'runtime/Dragon')]
    for row,actual in zip([binding['original_bounded'],binding['current_POD56_Dragon']],owned):
        if row['sha256']!=actual['sha256'] or row['size_bytes']!=actual['size_bytes'] or row['identity']==actual['identity']:
            raise RuntimeError('owned runtime exact bytes with new7ID required')
    return runner,owned

def probe_commands(out,binding):
    c=binding['compiler']['path'];src=str(BASE/'verify_native_A_archive64.f90')
    obj=str(out/'build/verify_native_A_archive64.o');exe=str(out/'runtime/verify_native_A_archive64')
    command=[c,*FLAGS,*['-I'+p for p in binding['probe_include_directories']],'-J'+str(out/'build'),'-c',src,'-o',obj]
    link=[c,'-O2','-ffp-contract=off',obj,*[p['path']for p in binding['probe_link_dependencies']],'-o',exe]
    return [command,link]

def check_full_current(fixed,owned):
    verify_rows(fixed);verify_rows(owned)
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original SELF 512MiB cap')

def scope():
    return dict(three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)

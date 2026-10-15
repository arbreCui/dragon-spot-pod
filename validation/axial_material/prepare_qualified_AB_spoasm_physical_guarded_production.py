"""Future bounded isolated physical-Pn SPOASM build; no import-time activity.

The current successful rank-one-cache runtime is an immutable predecessor.
Only SPOASM.o is added before its unchanged library in the production link.
Recovered Git source, actual archive/object provenance and a three-way native
assembly control establish the input contract. No FLU, transport, solve, CE
sample or qualification occurs here. A new cold AAA and all original gates
remain necessary. Root alone records true completed terminal returns.
"""
import argparse
import ast
import copy
import difflib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-qualified-AB-spoasm-physical-guarded-build-admission-20261007'
OUT=ART/'axial-material-spoasm-physical-guarded-build-20261007'
TERMINAL=ART/'axial-material-qualified-AB-spoasm-physical-guarded-build-terminal-20261007'
PARENT=ART/'axial-material-rank1-factor-cache-build-20261007'
PARENT_FACTORY=ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_production.py'
PARENT_FACTORY_SHA='92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
PARENT_SEAL='e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f'
PARENT_TERMINAL=ART/'axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007/terminal_return.json'
PARENT_TERMINAL_SHA='c5eecbff0064a9285460c98bc01bad26ab9180a4b4e38a6186be779378ba9d96'
PARENT_RUNTIME_SHA='292c10b259ead4d9123dcba7efd48dea0bf31b41963c620149c685c93906663c'
# The expected runtime SHA is verified against the genuine parent receipt;
# no path or filename is allowed to substitute for that identity.
OPERATOR_FACTORY=ROOT/'validation/axial_material/prepare_rank1_cache_axial_operator_audit.py'
OPERATOR_FACTORY_SHA='7f07c194c8f3c425c9c5f0a4259e73d6fbb404b9a7b0bf2b31e63d8e5c3297b6'
PATCH_HELPER=ROOT/'validation/axial_material/spoasm_physical_angular_patch.py'
CONTROL_SOURCE=ROOT/'validation/axial_material/spoasm_physical_angular_controls.f90'
PATCH_HELPER_SHA='6dc064e8f2806f714a0dce60094d6c5a967488b9904c683b5e9d959af01de12a'
CONTROL_SOURCE_SHA='bc54c1b63b62ed28043a960632827d791aa3dd8f5ab668f667cb2ac9ba865a9f'
BASE_REVISION='299546c405a47f7e3a7f75af54d392492d649781'
BASE_SOURCE_SHA='25435d9be70540c094346452b063c90ef3f212e905a6f57a949504fb2f7e8d26'
BASE_OBJECT=ROOT/'src/SPOASM.o'
BASE_OBJECT_SHA='8a5fbf4dc7395710c2b3aa4c33e153d54f15acd87a50becdb8eb26dae0fca298'
LIBRARY=ROOT/'lib/Darwin_arm64/libDragon.a'
LIB_SHA='954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9'
PROD=ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
FINAL=PROD/'AAA/map012'
FINAL_SEAL_SHA='64293bc1022a44d3cbf5e738bf1b79f4f2aa7b8958d572a59cc8c2b3ca968d59'
STATUS_SHA='03b68ebd59c7bfff9eca8f02961e1ae528bf4debf815dd23ae0d0a2cdf03051d'
CURRENT_INPUTS={
 'macro':dict(path=str(PROD/'AAA/bootstrap/initial_axial_macrolib.xsm'),sha256='bca18875dbde9b5ae14f916f3df902ab071c173adff02c1b09ef647116282510'),
 'track':dict(path=str(PROD/'AAA/bootstrap/initial_axial_track.xsm'),sha256='b8302889d66f37947b3060f5caef2be43c7da5dfd6673daaa1ffb66fd81997d6'),
 'snapshots':dict(path=str(FINAL/'candidate_radial.xsm'),sha256='4b2aa5644d7c1aa67cfe08db9029b834a285d16f6ae531afd43f1eb9d33377fc'),
 'basis':dict(path=str(PROD/'AAA/bootstrap/basis_reference.xsm'),sha256='5b05340f1ccaa6f6d41cb111dae0f5f87fab01cce12237e2ccad89ef9b316a19')}
NATIVE_INPUT_SHORT_NAMES={key:key+'.xsm' for key in CURRENT_INPUTS}
TOTAL_WALL,STAGE_WALL,RSS_CAP=1800,600,512
ARCHIVE_RESERVE=2*2**30;HISTORY_CAP=96*2**30;FREE_FLOOR=8*2**30
FAMILY='SPOASM_PHYSICAL_BUILD'
HISTORY_SCOPE_POLICY='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
TERMINAL_SCHEMA='AXMAT_SPOASM_PHYSICAL_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
TAIL_FIELDS=('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')

# The prior factory failed in the genuine supervisor constructor before its
# first child. These exact bytes are failed-history INPUT only; no old plan,
# partial output, source inventory or nested terminal record is promoted.
OLD_FACTORY=ROOT/'validation/axial_material/prepare_qualified_AB_spoasm_physical_production.py'
OLD_FACTORY_SHA='be60bfc524ccd76253d53e67d2c7e80650a152dfef11b6dc0b3a19ac65b5460c'
OLD_SOURCE=ART/'axial-material-qualified-AB-spoasm-physical-build-admission-20261007'
OLD_OUT=ART/'axial-material-spoasm-physical-build-20261007'
OLD_TERMINAL=ART/'axial-material-qualified-AB-spoasm-physical-build-terminal-20261007'
OLD_DECLARATION_SHA='85f681379574c797b23268e9a82e76a2f4085d93bf5f188e1c751c9bd1648d2e'
PRIOR_FAILURE_FILES={
    str(OLD_FACTORY):OLD_FACTORY_SHA,
    str(OLD_SOURCE/'source_admission.json'):'e63703889c9aecad576f34efc8f755ebf64766eae01371c16b52539f1fcab80f',
    str(OLD_OUT/'declaration.json'):OLD_DECLARATION_SHA,
    str(OLD_TERMINAL/'terminal_return.json'):'2bd3673caad096f099da6f52b5eb15499c35532d43373b627841737b4c7a6864',
    str(OLD_TERMINAL/'build_full_stdout.json'):'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    str(OLD_TERMINAL/'build_full_stderr.txt'):'c8e11dc7459d424f9b5df1394ee5c2ebda4a7631dbd0bdcb549b9a7f3dcb1a99',
    str(OLD_OUT/'execution_claim.json'):'627b10f4d3cf5ffb7ba9a8c9a3e42ecc781cb8029571d3f4154d29ce01734918'}
BOUNDED_HELPER=PARENT/'runtime/run_bounded_dragon.py'
BOUNDED_HELPER_SHA='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'


def digest(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        a=os.fstat(f.fileno());result=hashlib.file_digest(f,'sha256').hexdigest();b=os.fstat(f.fileno())
        if (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)!=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns):
            raise ValueError('input changed during byte hash')
        return result


def require(path,expected=None):
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts or path.is_symlink() or not path.is_file():
        raise ValueError('absolute regular nonalias input required: '+str(path))
    cursor=path.parent
    while cursor!=cursor.parent:
        if cursor.is_symlink() or not cursor.is_dir():raise ValueError('input ancestor alias/non-directory')
        cursor=cursor.parent
    if expected is not None and digest(path)!=expected:raise ValueError('pinned input changed: '+str(path))
    return path


def pin(path):return dict(path=str(require(path)),sha256=digest(path))
def read(path):return json.loads(Path(path).read_text())
def write_new(path,value):
    with Path(path).open('x') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def absent(path):
    if os.path.lexists(path):raise ValueError('exclusive new root/claim required; no retry')
def add_expected(files,path,wanted):
    path=str(require(path,wanted))
    if path in files and files[path]!=wanted:raise ValueError('conflicting pinned owners')
    files[path]=wanted

def load(path,name):
    path=require(path)
    if name in sys.modules:
        obj=sys.modules[name]
        if Path(obj.__file__).resolve()!=path:raise ValueError('real module provenance mismatch')
        return obj
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec)
    sys.modules[name]=obj;spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve()!=path:raise ValueError('real module source mismatch')
    return obj

def parent_factory():return load(require(PARENT_FACTORY,PARENT_FACTORY_SHA),'spoasm_actual_cache_predecessor')
def helper():return parent_factory().helper()
def resource_scope_contract():return parent_factory().resource_scope_contract()
def history_roots(roots,art):return parent_factory().history_roots(roots,art)
def validate_history_roots(roots,art):return parent_factory().validate_history_roots(roots,art)
def DynamicHistoryResources(art,roots,free,cap,failure_type=None):
    return parent_factory().DynamicHistoryResources(art,roots,free,cap,failure_type)
def actual_resource_class_factory():return parent_factory().parent_factory()
def modules():
    op=load(require(OPERATOR_FACTORY,OPERATOR_FACTORY_SHA),'spoasm_actual_guard_host')
    c,full,builder,parent,provenance=op.modules()
    if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):raise ValueError('real tested supervisor/base binding required')
    return c,full,provenance

def resources_for(roots,failure=None):return DynamicHistoryResources(ART,[str(p) for p in validate_history_roots(roots,ART)],FREE_FLOOR,HISTORY_CAP,failure)
def archive_bytes():
    total=0
    validate_history_roots([str(SOURCE),str(OUT)],ART)
    for base in (SOURCE,OUT):
        if not base.exists():continue
        for folder,dirs,names in os.walk(base,followlinks=False):
            if any((Path(folder)/x).is_symlink() for x in dirs+names):raise ValueError('new archive aliases forbidden')
            for name in names:
                p=require(Path(folder)/name);total+=p.stat().st_size
    return total

def resource_admission(resources):
    v=resources.check()
    if v['artifact_bytes']+ARCHIVE_RESERVE>=HISTORY_CAP or v['disk_free_bytes']-ARCHIVE_RESERVE<FREE_FLOOR:
        raise ValueError('fresh 2GiB reservation does not fit original family96/globalfree8')
    return v

def predecessor_admission(seal,terminal,terminal_sha):
    if seal!=PARENT_SEAL or Path(terminal)!=PARENT_TERMINAL or terminal_sha!=PARENT_TERMINAL_SHA:
        raise ValueError('actual successful cache build with actual Root exit-zero chain required')
    value=parent_factory().production_admission(seal,terminal,terminal_sha)
    if (value['schema']!='AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or value['build_root']!=str(PARENT) or value['rank1_factor_cache_budget_bytes']!=536870912
        or value['corrected_runtime']!=dict(path=str(PARENT/'runtime/Dragon'),sha256=PARENT_RUNTIME_SHA)
        or value['AAA_accuracy_qualified'] is not False or value['ABA_admitted'] is not False
        or value['resource_scope_contract']!=resource_scope_contract()):raise ValueError('parent input contract differs')
    return value

def recovered_baseline():
    value=subprocess.run(['git','show',BASE_REVISION+':src/SPOASM.f'],cwd=ROOT,check=True,capture_output=True,timeout=10).stdout
    if hashlib.sha256(value).hexdigest()!=BASE_SOURCE_SHA:raise ValueError('actual recovered baseline bytes differ')
    return value.decode('utf-8')


def prior_constructor_failure_input():
    """Validate only the actual stopped failure body, never its nested plan."""
    for path,wanted in PRIOR_FAILURE_FILES.items():require(path,wanted)
    e=strict_terminal_json(OLD_TERMINAL/'terminal_return.json')
    d=strict_terminal_json(OLD_OUT/'declaration.json')
    a=strict_terminal_json(OLD_SOURCE/'source_admission.json')
    claim=strict_terminal_json(OLD_OUT/'execution_claim.json')
    stdout=OLD_TERMINAL/'build_full_stdout.json'
    stderr=OLD_TERMINAL/'build_full_stderr.txt'
    def old_pin(path):return dict(path=str(path),sha256=PRIOR_FAILURE_FILES[str(path)])
    if (e['schema']!=TERMINAL_SCHEMA or e['record_producer']!='root'
        or e['actual_tool_terminal_return_observed'] is not True
        or e['record_written_after_actual_terminal_return'] is not True
        or type(e['returncode']) is not int or e['returncode']!=1
        or e['actual_tool_result']!=dict(initial_chunk_id='55b45e',session_id=88652,terminal_chunk_id='545c78',exit_code=1)
        or e['source']!=old_pin(OLD_FACTORY) or e['declaration']!=old_pin(OLD_OUT/'declaration.json')
        or e['full_stdout']!=old_pin(stdout) or e['full_stderr']!=old_pin(stderr)
        or e['execution_claim']!=old_pin(OLD_OUT/'execution_claim.json')
        or e['command']!=[d['build_python_executable'],str(OLD_FACTORY),'run-build','--sha256',OLD_DECLARATION_SHA]
        or type(e['new_native_children_started']) is not int or e['new_native_children_started']!=0
        or type(e['retries']) is not int or e['retries']!=0
        or any(e[k] is not False for k in ('new_compilation_started','native_assembly_controls_started',
            'successful_build_admitted','AAA_accuracy_qualified','ABA_admitted'))
        or any(e[k] is not None for k in ('build_seal','driver_result',*TAIL_FIELDS))
        or d['schema']!='AXMAT_SPOASM_PHYSICAL_BUILD_DECLARATION_V1'
        or d['source_root']!=str(OLD_SOURCE) or d['files'].get(str(OLD_FACTORY))!=OLD_FACTORY_SHA
        or a['schema']!='AXMAT_SPOASM_PHYSICAL_SOURCE_ADMISSION_V1'
        or a['recovered_source_sha256']!=BASE_SOURCE_SHA
        or claim['declaration_sha256']!=OLD_DECLARATION_SHA
        or type(claim['retries']) is not int or claim['retries']!=0
        or type(claim['parent_pid']) is not int or claim['parent_pid']<=0
        or stdout.read_bytes()!=b''):
        raise ValueError('exact actual pre-child constructor failure INPUT required')
    text=stderr.read_text()
    missing=OLD_OUT/'runtime/run_bounded_dragon.py'
    if ("FileNotFoundError: [Errno 2]" not in text or str(missing) not in text
        or 'runner=full.OwnRSSSerialExecutor(OUT,remaining,FAMILY,resources)' not in text
        or 'production_runner.py", line 677, in __init__' not in text):
        raise ValueError('retained stderr must show the exact actual constructor missing-file failure')
    absent_paths=[missing,OLD_OUT/FAMILY/'stages.json',OLD_OUT/'driver_result.json',
        OLD_OUT/'seal.json',OLD_OUT/'build/SPOASM.o',OLD_OUT/'runtime/Dragon']
    for path in absent_paths:
        if os.path.lexists(path):raise ValueError('old failed build acquired unclaimed completion bytes')
    return dict(schema='AXMAT_SPOASM_PRIOR_CONSTRUCTOR_FAILURE_INPUT_V1',
        classification='ACTUAL_PRE_CHILD_CONSTRUCTOR_FAILURE_INPUT_ONLY',files=dict(PRIOR_FAILURE_FILES),
        missing_paths=[str(p) for p in absent_paths],actual_returncode=1,actual_native_children_started=0,
        actual_completed_stages=0,build_seal=None,driver_result=None,retries=0,
        stopped_failure_body_not_recursively_promoted=True,old_partial_outputs_are_not_new_control_results=True,
        scientific_or_numerical_credit_granted=False,AAA_accuracy_qualified=False,ABA_admitted=False)


def bounded_helper_contract():
    require(BOUNDED_HELPER,BOUNDED_HELPER_SHA)
    require(OUT/'runtime/run_bounded_dragon.py',BOUNDED_HELPER_SHA)
    return dict(schema='AXMAT_SPOASM_GENUINE_SUPERVISOR_LOCAL_INPUT_V1',
        original=dict(path=str(BOUNDED_HELPER),sha256=BOUNDED_HELPER_SHA),
        private=dict(path=str(OUT/'runtime/run_bounded_dragon.py'),sha256=BOUNDED_HELPER_SHA),
        copy_operation='shutil.copy2',byte_equivalence=True,
        required_by_actual_SerialExecutor_constructor=True,constructor_local_regular_files=['runtime/run_bounded_dragon.py'])


def genuine_constructor_preflight(c,full,resources,provenance):
    """Construct the unchanged real supervisor; no execute, child or claim."""
    contract=bounded_helper_contract()
    if (full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)
        or full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__
        or pin(c.__file__)!=provenance['controller']
        or pin(full.__file__)!=provenance['actual_own_rss_source']):
        raise ValueError('actual unchanged tested supervisor constructor required')
    untouched=[OUT/'execution_claim.json',OUT/FAMILY/'stages.json',OUT/'driver_result.json',OUT/'seal.json']
    for path in untouched:absent(path)
    if list((OUT/'build').iterdir()):raise ValueError('constructor-only preflight cannot consume build results')
    runner=full.OwnRSSSerialExecutor(OUT,STAGE_WALL,FAMILY,resources)
    if (runner.records!=[] or runner.work!=OUT or runner.stages_path!=OUT/FAMILY/'stages.json'
        or runner.resources is not resources or Path(runner.bounded.__file__)!=OUT/'runtime/run_bounded_dragon.py'
        or pin(runner.bounded.__file__)!=contract['private']
        or any(runner.env[k]!='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE'))):
        raise ValueError('genuine constructor must load the exact local helper without execution')
    for path in untouched:absent(path)
    if list((OUT/'build').iterdir()):raise ValueError('constructor-only preflight created build results')
    return dict(schema='AXMAT_SPOASM_ACTUAL_SUPERVISOR_CONSTRUCTOR_PREFLIGHT_V1',
        actual_serial_source=provenance['controller'],actual_own_rss_source=provenance['actual_own_rss_source'],
        bounded_helper=contract,records=[],native_children_started=0,compilation_started=False,
        stage_or_execution_claim_written=False,constructor_only=True,
        transport_RSS_fitness_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False)

def archive_member(path,name):
    with require(path,LIB_SHA).open('rb') as f:
        if f.read(8)!=b'!<arch>\n':raise ValueError('ordinary archive required')
        hits=[]
        while True:
            h=f.read(60)
            if not h:break
            if len(h)!=60 or h[58:60]!=b'`\n':raise ValueError('malformed library archive')
            n=int(h[48:58]);tag=h[:16].decode().rstrip();data=f.read(n)
            if len(data)!=n:raise ValueError('short archive member')
            if tag.startswith('#1/'):
                prefix=int(tag[3:]);tag=data[:prefix].rstrip(b'\0').decode();data=data[prefix:]
            else:tag=tag.rstrip('/')
            if tag==name:hits.append(data)
            if n%2:f.read(1)
        if len(hits)!=1:raise ValueError('exactly one original SPOASM member required')
        return hits[0]

def patch_admission(patch_sha,controls_sha):
    if patch_sha!=PATCH_HELPER_SHA or controls_sha!=CONTROL_SOURCE_SHA or '0'*64 in (patch_sha,controls_sha):
        raise ValueError('actual reviewed new source identities required')
    patch=load(require(PATCH_HELPER,patch_sha),'spoasm_physical_source_patch')
    require(CONTROL_SOURCE,controls_sha)
    original=recovered_baseline();changed=patch.patch_source(original);contract=patch.control_contract()
    if (changed['proof']['exact_inverse_source_restoration'] is not True
        or changed['proof']['radial_P0_solver_and_R_formula_source_bytes_preserved'] is not True
        or changed['proof']['original_source_sha256']!=BASE_SOURCE_SHA
        or contract['all_groups']!=list(range(1,371)) or contract['transport_calls']!=0
        or contract['linear_solves']!=0 or contract['raw_before_numeric_gates'] is not True):
        raise ValueError('complete original math/source scope and full group controls required')
    actual=archive_member(LIBRARY,'SPOASM.o')
    if hashlib.sha256(actual).hexdigest()!=BASE_OBJECT_SHA or actual!=require(BASE_OBJECT,BASE_OBJECT_SHA).read_bytes():
        raise ValueError('actual inherited compiled archive SPOASM differs from frozen object')
    return original,changed,contract


def input_admission():
    member=read(require(FINAL/'result.json',FINAL_SEAL_SHA));status=read(require(PROD/'AAA/run_status.json',STATUS_SHA))
    if (status['classification']!='WAITING_REFERENCE' or status['completed_maps']!=12
        or status['cases']['AAA']['classification']!='VALID_MET' or member['classification']!='SEALED_STAGE_OUTPUTS'):
        raise ValueError('actual completed input case required, without inheriting accuracy qualification')
    labels=dict(macro='initial_axial_macrolib.xsm',track='initial_axial_track.xsm',snapshots='candidate_radial.xsm',basis='basis_reference.xsm')
    aliases={}
    for key,item in CURRENT_INPUTS.items():
        literal=FINAL/labels[key];actual=require(item['path'],item['sha256'])
        if member['sha256'][labels[key]]!=item['sha256']:raise ValueError('original sealed member pin differs')
        if literal!=actual:
            if not literal.is_symlink() or os.readlink(literal)!=str(actual) or literal.resolve(strict=True)!=actual:
                raise ValueError('actual original final/bootstrap alias differs')
            aliases[str(literal)]=dict(literal_target=os.readlink(literal),target=str(actual),sha256=item['sha256'])
    return dict(schema='AXMAT_SPOASM_TRUE_CURRENT_INPUT_CONTROL_V1',files=CURRENT_INPUTS,
        member_seal=dict(path=str(FINAL/'result.json'),sha256=FINAL_SEAL_SHA),
        status=dict(path=str(PROD/'AAA/run_status.json'),sha256=STATUS_SHA),aliases=aliases,
        case_accuracy_qualification_inherited=False,assembly_only=True,transport_calls=0)


def environment(d,require_build_interpreter=True):
    helper().environment(d,require_build_interpreter=require_build_interpreter)
    if d['resource_scope_contract']!=resource_scope_contract():raise ValueError('original live resource scope differs')
    if (d['actual_local_supervisor_helper']!=bounded_helper_contract()
        or d['prior_constructor_failure_input']!=prior_constructor_failure_input()):
        raise ValueError('actual local supervisor or stopped failure INPUT identity differs')
    for key,item in d['actual_current_input_control']['files'].items():require(item['path'],item['sha256'])
    for key,name in NATIVE_INPUT_SHORT_NAMES.items():require(OUT/'controls/current_input'/name,CURRENT_INPUTS[key]['sha256'])
    for path,value in d['actual_current_input_control']['aliases'].items():
        p=Path(path)
        if not p.is_symlink() or os.readlink(p)!=value['literal_target'] or str(p.resolve(strict=True))!=value['target']:
            raise ValueError('actual input alias changed')


def control_commands(d):
    exe=str(OUT/'runtime/spoasm_physical_controls')
    return [[exe,'positive'],[exe,'production-input',*[NATIVE_INPUT_SHORT_NAMES[k] for k in ('macro','track','snapshots','basis')]],
        *[[exe,*row['args']] for row in d['control_contract']['negative_cases']]]

def control_labels(d):return ['positive','current_input',*['negative_'+row['name'] for row in d['control_contract']['negative_cases']]]
def stage_commands(d,sha):return [*d['build_commands'],*control_commands(d),[d['build_python_executable'],str(Path(__file__).resolve()),'audit-build','--sha256',sha]]
def stage_labels(d):return [*['build/build_'+f'{i:02}' for i in range(len(d['build_commands']))],*['controls/'+x+'/execute' for x in control_labels(d)],'audit/audit']
def terminal_contract(python):return dict(schema=TERMINAL_SCHEMA,producer='root',factory_must_not_write_own_terminal_record=True,
    actual_completed_tool_returncode=0,fixed_terminal_root=str(TERMINAL),actual_command_template=[python,str(Path(__file__).resolve()),'run-build','--sha256','ACTUAL_DECLARATION_SHA256'],
    required_tail_fields=list(TAIL_FIELDS),full_stdout_and_stderr_are_retained=True,
    combined_archive_roots=[str(SOURCE),str(OUT)],total_wall_seconds=TOTAL_WALL,
    own_child_rss_cap_mib=RSS_CAP,original_scientific_qualification_granted=False)


def prepare_build(parent_seal,parent_terminal,parent_terminal_sha,patch_sha,controls_sha):
    for path in (SOURCE,OUT,TERMINAL):absent(path)
    prior_failure=prior_constructor_failure_input()
    prior=predecessor_admission(parent_seal,parent_terminal,parent_terminal_sha)
    original,changed,contract=patch_admission(patch_sha,controls_sha);inputs=input_admission()
    c,full,provenance=modules();old=read(require(PARENT/'declaration.json'))
    parentlink=list(old['build_commands'][2]);compiler=parentlink[0];link=list(parentlink)
    if link.count(str(LIBRARY))!=1 or link[-2:]!=['-o',str(PARENT/'runtime/Dragon')]:raise ValueError('actual cache link identity differs')
    link.insert(link.index(str(LIBRARY)),str(OUT/'build/SPOASM.o'));link[-1]=str(OUT/'runtime/Dragon')
    restored=list(link);restored.remove(str(OUT/'build/SPOASM.o'));restored[-1]=str(PARENT/'runtime/Dragon')
    if restored!=parentlink:raise ValueError('sole new archive-preceding override must invert to the exact actual cache link')
    common=[compiler,'-O2','-march=native','-ffp-contract=off','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
        '-I'+str(OUT/'build'),'-I'+str(ROOT/'lib/Darwin_arm64/modules'),'-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(OUT/'build')]
    units=[('SPOASM.f','SPOASM.o'),('SPOASM.baseline_rebuilt.f','SPOASM.baseline_rebuilt.o'),('SPOASM.physical_unit.f','SPOASM.physical_unit.o'),
        ('spoasm_physical_angular_controls.f90','spoasm_physical_angular_controls.o')]
    commands=[[*common,'-c',str(SOURCE/src),'-o',str(OUT/'build'/obj)] for src,obj in units]
    commands.append(link)
    commands.append([*parentlink[:5],str(OUT/'build/spoasm_physical_angular_controls.o'),str(OUT/'build/SPOASM.baseline_rebuilt.o'),
        str(OUT/'build/SPOASM.physical_unit.o'),*[x for x in parentlink if x.endswith('.a')],'-o',str(OUT/'runtime/spoasm_physical_controls')])
    files=dict(old['files'])
    for p,w in read(PARENT/'seal.json')['files'].items():add_expected(files,PARENT/p,w)
    if files.get(str(BOUNDED_HELPER))!=BOUNDED_HELPER_SHA:
        raise ValueError('actual original parent seal must own the genuine supervisor helper')
    for p,w in PRIOR_FAILURE_FILES.items():add_expected(files,p,w)
    for p in (PARENT_FACTORY,OPERATOR_FACTORY,PATCH_HELPER,CONTROL_SOURCE,BASE_OBJECT,Path(__file__).resolve(),Path('/usr/bin/nm'),Path('/usr/bin/otool'),Path('/usr/bin/dwarfdump'),PROD/'runtime/snapshot_control_preflight.py'):
        add_expected(files,p,digest(require(p)))
    for p,w in ((LIBRARY,LIB_SHA),(PARENT_TERMINAL,PARENT_TERMINAL_SHA),(FINAL/'result.json',FINAL_SEAL_SHA),(PROD/'AAA/run_status.json',STATUS_SHA)):
        add_expected(files,p,w)
    for item in [*CURRENT_INPUTS.values(),prior['actual_external_terminal_evidence'],prior['actual_external_terminal_validation']['full_stdout']]:
        add_expected(files,item['path'],item['sha256'])
    for item in [*provenance['tested_guard_files'],provenance['controller'],provenance['actual_own_rss_source'],provenance['actual_dynamic_resource_class_source']]:
        add_expected(files,item['path'],item['sha256'])
    for item in commands:
        for arg in item:
            p=Path(arg)
            if p.is_absolute() and p.is_file() and not p.is_relative_to(OUT) and not p.is_relative_to(SOURCE):
                if str(p) not in files:add_expected(files,p,digest(require(p)))
    # Metadata-only reservation: raw true-input native object copies are bounded
    # by twice all original file sizes plus32MiB. No float/control is run here.
    true_input_bound=2*sum(require(x['path']).stat().st_size for x in CURRENT_INPUTS.values())+32*2**20
    forecast=dict(schema='AXMAT_SPOASM_BUILD_ARCHIVE_FORECAST_V1',combined_roots=[str(SOURCE),str(OUT)],
        true_input_native_copy_upper_bound_bytes=true_input_bound,synthetic_raw_allowance_bytes=64*2**20,
        source_build_logs_binaries_and_metadata_allowance_bytes=1*2**30)
    forecast['genuine_supervisor_helper_included_in_metadata_allowance']=dict(
        source=dict(path=str(BOUNDED_HELPER),sha256=BOUNDED_HELPER_SHA),
        destination=str(OUT/'runtime/run_bounded_dragon.py'),actual_byte_length=require(BOUNDED_HELPER,BOUNDED_HELPER_SHA).stat().st_size,
        allowance_field='source_build_logs_binaries_and_metadata_allowance_bytes',additional_reservation_bytes=0)
    forecast['complete_forecast_bytes']=sum(forecast[k] for k in ('true_input_native_copy_upper_bound_bytes','synthetic_raw_allowance_bytes','source_build_logs_binaries_and_metadata_allowance_bytes'))
    if forecast['complete_forecast_bytes']>=ARCHIVE_RESERVE:raise ValueError('whole source/out forecast exceeds unchanged2GiB')
    roots=history_roots(sorted(set(old['resource_roots'])|set(read(PROD/'prepared.json')['resource_roots'])|
        {str(SOURCE),str(OUT),str(TERMINAL)}),ART);resources=resources_for(roots,c.ResourceFailure);before=resource_admission(resources)
    SOURCE.mkdir();OUT.mkdir()
    for name in ('build','runtime','controls','audit',FAMILY):(OUT/name).mkdir()
    shutil.copy2(require(BOUNDED_HELPER,BOUNDED_HELPER_SHA),OUT/'runtime/run_bounded_dragon.py')
    add_expected(files,OUT/'runtime/run_bounded_dragon.py',BOUNDED_HELPER_SHA)
    local_supervisor=bounded_helper_contract()
    ctor_preflight=genuine_constructor_preflight(c,full,resources,provenance)
    for name in ('positive','current_input',*['negative_'+x['name'] for x in contract['negative_cases']]):(OUT/'controls'/name).mkdir()
    # GANLIB's LCMOP name ABI is 72 bytes. These immutable short-name copies
    # are literal original bytes, not aliases or transformed native inputs.
    for key,name in NATIVE_INPUT_SHORT_NAMES.items():
        target=OUT/'controls/current_input'/name
        shutil.copy2(require(CURRENT_INPUTS[key]['path'],CURRENT_INPUTS[key]['sha256']),target)
        add_expected(files,target,CURRENT_INPUTS[key]['sha256'])
    for name,content in (('SPOASM.original.f',original),('SPOASM.f',changed['production_source']),('SPOASM.baseline_rebuilt.f',changed['reference_source']),('SPOASM.physical_unit.f',changed['unit_source'])):
        (SOURCE/name).write_text(content)
    shutil.copy2(CONTROL_SOURCE,SOURCE/CONTROL_SOURCE.name)
    (SOURCE/'SPOASM.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),changed['production_source'].splitlines(True),fromfile='299546c:SPOASM.f',tofile='private:SPOASM.f')))
    write_new(SOURCE/'source_admission.json',dict(schema='AXMAT_SPOASM_PHYSICAL_SOURCE_ADMISSION_V1',source_patch_proof=changed['proof'],
        original_compiled_object=pin(BASE_OBJECT),original_library=pin(LIBRARY),recovered_source_sha256=BASE_SOURCE_SHA,original_revision=BASE_REVISION,
        historical_DWARF_matching_source_is_semantically_checked_against_actual_archive_by_controls=True,
        original_object_full_source_byte_reproduction_claimed=False,source_equivalence_for_changed_physical_operator_claimed=False,
        actual_current_input_control=inputs,sole_new_production_override='SPOASM.o',exact_parent_link_inverse=True,
        native_readonly_short_name_copy_ABI_max_bytes=72,
        native_readonly_short_name_copy_files={key:dict(path=str(OUT/'controls/current_input'/name),sha256=CURRENT_INPUTS[key]['sha256']) for key,name in NATIVE_INPUT_SHORT_NAMES.items()},
        corrected_source_factor_selector_and_factor_cache_retained=True,radial_P0_recipe_preserved=True,
        actual_local_supervisor_helper=local_supervisor,actual_supervisor_constructor_preflight=ctor_preflight,
        prior_constructor_failure_input=prior_failure,
        collision_self_operator_unchanged=False,anisotropic_axial_physical_T_and_self_Pn_restored=True,
        fitting=False,transport_launched=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    inventory=helper().inventory(SOURCE)
    for p,w in inventory['files'].items():add_expected(files,SOURCE/p,w)
    d=copy.deepcopy(old)
    d.update(schema='AXMAT_SPOASM_PHYSICAL_BUILD_DECLARATION_V1',family=FAMILY,source_root=str(SOURCE),source_inventory=inventory,
        files=files,build_commands=commands,inherited_rank1_cache_admission=prior,actual_current_input_control=inputs,
        actual_local_supervisor_helper=local_supervisor,actual_supervisor_constructor_preflight=ctor_preflight,
        prior_constructor_failure_input=prior_failure,
        source_namespace_directories=[],native_input_short_names=NATIVE_INPUT_SHORT_NAMES,
        patch_helper=pin(PATCH_HELPER),controls_source=pin(CONTROL_SOURCE),source_patch_proof=changed['proof'],control_contract=contract,
        parent_production_link=parentlink,complete_archive_forecast=forecast,resource_roots=roots,resources_before=before,
        total_wall_seconds=TOTAL_WALL,stage_wall_seconds=STAGE_WALL,rss_cap_mib=RSS_CAP,archive_reserve_bytes=ARCHIVE_RESERVE,
        artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,threads=1,numeric_children_at_once=1,retries=0,
        resource_scope_policy=HISTORY_SCOPE_POLICY,resource_scope_contract=resource_scope_contract(),guard_provenance=provenance,
        actual_external_terminal_return_contract=terminal_contract(old['build_python_executable']),
        sole_new_production_overrides=['SPOASM.o'],collision_self_operator_unchanged=False,physical_data_unchanged=True,
        radial_arithmetic_unchanged=True,white_closure_unchanged=True,angle_grid_unchanged=True,original_accuracy_thresholds_changed=False,
        transport_launched=False,actual_full_FLU_entry_executed=False,fresh_cold_AAA_required=True,AAA_accuracy_qualified=False,ABA_admitted=False)
    environment(d);write_new(OUT/'declaration.json',d)
    if archive_bytes()>=ARCHIVE_RESERVE:raise ValueError('whole new SOURCE+OUT cap reached')
    resources.check()
    print(json.dumps(dict(classification='DECLARED_SPOASM_PHYSICAL_BUILD_ONLY',declaration=str(OUT/'declaration.json'),declaration_sha256=digest(OUT/'declaration.json')),allow_nan=False))


def declaration_admission(sha,require_build_interpreter=True):
    d=read(require(OUT/'declaration.json',sha))
    if (not re.fullmatch('[0-9a-f]{64}',sha or '') or d['schema']!='AXMAT_SPOASM_PHYSICAL_BUILD_DECLARATION_V1'
        or d['family']!=FAMILY or d['source_root']!=str(SOURCE) or d['sole_new_production_overrides']!=['SPOASM.o']
        or d['total_wall_seconds']!=1800 or d['stage_wall_seconds']!=600 or d['rss_cap_mib']!=512
        or d['archive_reserve_bytes']!=ARCHIVE_RESERVE or d['artifact_budget_bytes']!=HISTORY_CAP or d['min_free_bytes']!=FREE_FLOOR
        or d['threads']!=1 or d['numeric_children_at_once']!=1 or d['retries']!=0 or d['fresh_cold_AAA_required'] is not True
        or any(d[k] is not False for k in ('transport_launched','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))
        or d['actual_external_terminal_return_contract']!=terminal_contract(d['build_python_executable'])
        or d['native_input_short_names']!=NATIVE_INPUT_SHORT_NAMES or d['source_namespace_directories']!=[]):raise ValueError('complete original bounded input-only declaration required')
    environment(d,require_build_interpreter);helper().verify(d['files']);helper().verify_inventory(SOURCE,d['source_inventory'])
    expected_ctor=dict(schema='AXMAT_SPOASM_ACTUAL_SUPERVISOR_CONSTRUCTOR_PREFLIGHT_V1',
        actual_serial_source=d['guard_provenance']['controller'],actual_own_rss_source=d['guard_provenance']['actual_own_rss_source'],
        bounded_helper=bounded_helper_contract(),records=[],native_children_started=0,compilation_started=False,
        stage_or_execution_claim_written=False,constructor_only=True,
        transport_RSS_fitness_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    if (d['actual_supervisor_constructor_preflight']!=expected_ctor
        or d['files'].get(str(OUT/'runtime/run_bounded_dragon.py'))!=BOUNDED_HELPER_SHA
        or any(d['files'].get(p)!=w for p,w in PRIOR_FAILURE_FILES.items())):
        raise ValueError('complete declared genuine constructor and failed-history INPUT pins required')
    if namespace_directories(SOURCE)!=d['source_namespace_directories']:raise ValueError('exact new source directories required')
    patch=load(require(PATCH_HELPER,PATCH_HELPER_SHA),'spoasm_physical_source_patch')
    proof=patch.verify_sources((SOURCE/'SPOASM.original.f').read_text(),(SOURCE/'SPOASM.f').read_text(),
        (SOURCE/'SPOASM.baseline_rebuilt.f').read_text(),(SOURCE/'SPOASM.physical_unit.f').read_text())
    if proof!=d['source_patch_proof'] or patch.control_contract()!=d['control_contract'] or input_admission()!=d['actual_current_input_control']:
        raise ValueError('exact source/input/control contract changed')
    prior=predecessor_admission(PARENT_SEAL,PARENT_TERMINAL,PARENT_TERMINAL_SHA)
    if prior!=d['inherited_rank1_cache_admission']:raise ValueError('full genuine predecessor chain changed')
    resources_for(d['resource_roots']).check();return d


def raw_inventory(folder):
    folder=Path(folder)
    if folder.is_symlink() or not folder.is_dir():raise ValueError('actual raw directory missing or aliased')
    result={}
    for parent,dirs,names in os.walk(folder,followlinks=False):
        if any((Path(parent)/name).is_symlink() for name in dirs+names):raise ValueError('new raw namespace aliases forbidden')
        for name in names:
            path=require(Path(parent)/name);result[str(path.relative_to(folder))]=digest(path)
    return result

def namespace_directories(folder):
    folder=Path(folder)
    if folder.is_symlink() or not folder.is_dir():raise ValueError('actual namespace root missing or aliased')
    result=[]
    for parent,dirs,names in os.walk(folder,followlinks=False):
        if any((Path(parent)/name).is_symlink() for name in dirs+names):raise ValueError('new namespace aliases forbidden')
        for name in dirs:
            path=Path(parent)/name
            if not path.is_dir():raise ValueError('non-directory namespace entry')
            result.append(str(path.relative_to(folder)))
        for name in names:require(Path(parent)/name)
    return sorted(result)

def check_watch(stage):
    v=helper().check_watch(OUT,stage)
    w=read(require(v['path'],v['sha256']))
    if (w['rss_cap_mib']!=512 or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True
        or not 0<=w['elapsed_seconds']<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 or w['limit_failure'] is not None):
        raise ValueError('actual own-child originalcaps and complete cleanup required')
    return v


def output_records(path,nl,precision,variant):
    blob=require(path).read_bytes();head=struct.unpack_from('<12q',blob)
    if head!=(1,variant,370,8,3,24,14,1800,48,32,nl,precision):raise ValueError('native output shape/ABI identity differs')
    groupbytes=100+100*nl+(192 if precision==64 else 0)+96+32+12+24+16
    if len(blob)!=256+370*groupbytes+10404:raise ValueError('complete output archive length differs')
    state=struct.unpack_from('<40i',blob,96)
    if state[0]!=1 or state[7:11]!=(370,1800,24,nl):raise ValueError('actual output STATE identity differs')
    rows=[]
    for g in range(370):
        pos=256+g*groupbytes;r=blob[pos:pos+groupbytes]
        rows.append(dict(total=r[:100],self=r[100:100+100*nl],recipe=r[100+100*nl:]))
    return blob,state,rows,blob[256+370*groupbytes:]


def finite_words(blob,kind):
    count=len(blob)//struct.calcsize(kind)
    if len(blob)!=count*struct.calcsize(kind) or not all(math.isfinite(v[0]) for v in struct.iter_unpack('<'+kind,blob)):
        raise ValueError('nonfinite/malformed defined native output words')


def expected_synthetic(path,nl,precision):
    blob=require(path).read_bytes();head=struct.unpack_from('<12q',blob)
    if head!=(1,370,8,3,24,14,1800,48,32,nl,precision,1):raise ValueError('raw synthetic input ABI differs')
    sizes=[24*370*4,24*3*370*4,9*3*370*4,9*3*370*4,14*3*370*8,14*3*370*8,14*3*370*8,370*3*8,32,32,160,160]
    if len(blob)!=96+sum(sizes):raise ValueError('complete synthetic input length differs')
    t=memoryview(blob)[96:96+sizes[0]];s=memoryview(blob)[96+sizes[0]:96+sizes[0]+sizes[1]]
    return [(b'\0'*4+bytes(t[g*96:(g+1)*96]),b''.join(b'\0'*4+bytes(s[(g*3+l)*96:(g*3+l+1)*96]) for l in range(nl))) for g in range(370)]


def true_input_raw_comparison(folder,d):
    """Compare every actual record/entry/type against original sealed inputs.

    The native copy is an input archive, not an observation or numerical result.
    Its internal block addresses may differ; original record bytes may not.
    """
    op=load(require(OPERATOR_FACTORY,OPERATOR_FACTORY_SHA),'spoasm_actual_guard_host')
    reader=load(require(PROD/'runtime/snapshot_control_preflight.py','f60309e54947de8dc43e7080fd19ca6255652d840493db23b37ff7003c6a0819'),'spoasm_actual_xsm_reader')
    counts=dict(records=0,radial_scalar_group_records=0,physical_macro_moment_records=0,
        macro_self_diagonal_words=0,explicit_stored_self_diagonal_words=0,structurally_absent_P2_positive_zero_words=0)
    diagonal_mapping=[]
    expected=[]
    def compare_directory(a,ad,b,bd):
        if set(ad)!=set(bd):raise ValueError('true-input copy namespace differs')
        for key,(off,length,typ) in ad.items():
            target=bd[key]
            if target[1:]!=(length,typ):raise ValueError('copied true-input native ABI differs')
            if typ==0 and length==-1:
                compare_directory(a,a.directory(off),b,b.directory(target[0]))
            elif typ==10:
                aa=a.integers(off,length);bb=b.integers(target[0],length)
                for x,y in zip(aa,bb):compare_directory(a,a.directory(x),b,b.directory(y))
            else:
                if length<0 or a.read(off,length)!=b.read(target[0],length):raise ValueError('true input record bytes changed during native copy')
                counts['records']+=1
    copied=folder/'actual_inputs.xsm'
    with op.stream_xsm(copied,reader) as data:
        root=data.root
        if set(root)!={'MACRO','TRACK','SNAPSHOTS','BASIS'}:raise ValueError('actual copied input root differs')
        roots={}
        for key,name in (('macro','MACRO'),('track','TRACK'),('snapshots','SNAPSHOTS'),('basis','BASIS')):
            node=root[name]
            if node[1:]!=(-1,0):raise ValueError('real native input tables required')
            target=data.directory(node[0]);roots[key]=target
            with op.stream_xsm(Path(d['actual_current_input_control']['files'][key]['path']),reader) as original:
                compare_directory(original,original.root,data,target)
        track=roots['track'];mat=struct.unpack('<384i',data.record(track,'MATCOD',384,1))
        mat1=struct.unpack('<48i',data.record(track,'MAT1D',48,1))
        if mat1!=(1,)*16+(2,)*16+(3,)*16:raise ValueError('actual true48-layer snapshot mapping differs')
        if any(mat[r*48+z]!=(z//16)*8+r+1 for r in range(8) for z in range(48)):raise ValueError('actual material24 map differs')
        def lists(directory,key):
            off,n,typ=directory[key]
            if typ!=10:raise ValueError('native lists required')
            out=[]
            for address in data.integers(off,n):
                entry=data.directory(address);handle=entry['***HANDLE***']
                if handle[1:]!=(-1,0):raise ValueError('native object handle required')
                out.append(data.directory(handle[0]))
            return out
        mg=lists(roots['macro'],'GROUP')
        if len(mg)!=370:raise ValueError('every real current group required')
        for group_number,group in enumerate(mg,1):
            t=b'\0'*4+data.record(group,'NTOT0',24,2)
            s=b''.join(b'\0'*4+data.record(group,f'SIGW{l:02}',24,2) for l in range(3))
            expected.append((t,s));counts['physical_macro_moment_records']+=3
            # ASMDRV's packed convention is JG=IJJS-JND+1 with one-based
            # coefficient IPOS+JND-1. Compare IEEE words, without 2l+1.
            # Missing P2 diagonals are structural +0 from native SXSC=0.0;
            # they must match the actual SIGW word and are explicitly counted.
            for order in range(3):
                njj=struct.unpack('<24i',data.record(group,f'NJJS{order:02}',24,1))
                ijj=struct.unpack('<24i',data.record(group,f'IJJS{order:02}',24,1))
                ipos=struct.unpack('<24i',data.record(group,f'IPOS{order:02}',24,1))
                coefficient_count=sum(njj);entry=group.get(f'SCAT{order:02}')
                if any(n<0 for n in njj):raise ValueError('negative original compressed SCAT count')
                if entry is None:
                    if coefficient_count or order!=2:raise ValueError('missing nonzero/non-P2 compressed scattering record')
                    packed=b''
                else:
                    if entry[1:]!=(coefficient_count,2):raise ValueError('complete original compressed scattering ABI differs')
                    packed=data.read(entry[0],entry[1])
                sigw=data.record(group,f'SIGW{order:02}',24,2)
                for material,n in enumerate(njj):
                    if n and not (1<=ipos[material]<=coefficient_count and ipos[material]+n-1<=coefficient_count
                        and 1<=ijj[material]-n+1<=ijj[material]<=370):
                        raise ValueError('compressed original material/source-group mapping outside bounds')
                    jnd=ijj[material]-group_number+1
                    sigw_bits=sigw[4*material:4*(material+1)]
                    if 1<=jnd<=n:
                        word_index=ipos[material]+jnd-2
                        coefficient_bits=packed[4*word_index:4*(word_index+1)]
                        if len(coefficient_bits)!=4 or coefficient_bits!=sigw_bits:
                            raise ValueError('actual raw compressed self-scattering word differs from physical SIGW')
                        counts['explicit_stored_self_diagonal_words']+=1
                        absence='EXPLICIT_STORED_SELF_DIAGONAL'
                    else:
                        if order!=2 or sigw_bits!=b'\0'*4:
                            raise ValueError('absent self diagonal requires explicit exact native positive-zero P2 word')
                        word_index=None;coefficient_bits=None
                        counts['structurally_absent_P2_positive_zero_words']+=1
                        absence='NO_PACKED_SELF_TERM_NATIVE_SXSC_INITIAL_POSITIVE_ZERO_MATCHES_ACTUAL_SIGW'
                    diagonal_mapping.append(dict(group=group_number,material=material+1,order=order,
                        NJJS=n,IJJS=ijj[material],IPOS=ipos[material],SCAT_record_present=entry is not None,
                        SCAT_zero_based_word_index=word_index,SCAT_bits_hex=None if coefficient_bits is None else coefficient_bits.hex(),
                        actual_SIGW_bits_hex=sigw_bits.hex(),comparison=absence))
                    counts['macro_self_diagonal_words']+=1
        sr=lists(roots['snapshots'],'SYSTEM');tr=lists(roots['snapshots'],'TRACK')
        if len(sr)!=3 or len(tr)!=3:raise ValueError('all three actual radial snapshots required')
        for sysrow,trow in zip(sr,tr):
            st=struct.unpack('<40i',data.record(sysrow,'STATE-VECTOR',40,1));ts=struct.unpack('<40i',data.record(trow,'STATE-VECTOR',40,1))
            if st[10]!=1 or ts[5]!=1:raise ValueError('actual radial NANI1 contract required')
            groups=lists(sysrow,'GROUP')
            if len(groups)!=370:raise ValueError('all true radial groups required')
            for group in groups:
                for name in ('DRAGON-TXSC','DRAGON-S0XSC','SPOT-S0-PHYS'):data.record(group,name,9,2)
                counts['radial_scalar_group_records']+=1
    if counts['macro_self_diagonal_words']!=26640:raise ValueError('all370x24x3 original self diagonal words required')
    return expected,counts,dict(schema='AXMAT_ACTUAL_MACRO_PACKED_SELF_DIAGONAL_BIT_COMPARISON_V1',
        count=26640,raw_inputs_already_archived_before_gate=True,no_extra_2l_plus_1=True,
        zero_SIGW_words_not_reassigned=True,rows=diagonal_mapping)


def control_audit(d):
    receipt=read(require(OUT/'raw_controls_receipt.json'))
    if receipt['before_numeric_gates'] is not True or receipt['files']!=raw_inventory(OUT/'controls'):
        raise ValueError('all raw outputs must be archived before any numeric gate')
    fixtures=[*d['control_contract']['positive_fixtures'],dict(name='actualphysical370_64',scat=3,real64_authority=True)]
    counts=dict(fixtures=5,groups_per_fixture=370,actual_assembly_invocations=15,negative_commands=len(d['control_contract']['negative_cases']),
        physical_T_self_words=0,actual_input_records=0,radial_groups=0,actual_macro_moment_records=0,
        macro_self_diagonal_words=0,explicit_stored_self_diagonal_words=0,structurally_absent_P2_positive_zero_words=0)
    actual_diagonal_comparison=None
    for fixture in fixtures:
        name=fixture['name'];nl=fixture['scat'];precision=64 if fixture['real64_authority'] else 32
        folder=OUT/'controls'/('current_input' if name.startswith('actual') else 'positive')
        lines=[json.loads(x) for x in require(folder/'manifest.jsonl').read_text().splitlines()]
        selected=[x for x in lines if x.get('fixture')==name and x['kind']=='output']
        if [x['variant'] for x in selected]!=['archive','rebuilt','physical_unit'] or any(x['file']!=name+'.'+x['variant']+'.bin' for x in selected):
            raise ValueError('all real native assembly callers/outputs required')
        records=[output_records(folder/(name+'.'+variant+'.bin'),nl,precision,i+1) for i,variant in enumerate(('archive','rebuilt','physical_unit'))]
        if records[0][1]!=records[1][1] or records[0][1]!=records[2][1]:raise ValueError('actual assembly STATE changed')
        if any(records[0][3]!=r[3] for r in records[1:]):raise ValueError('radial source/leak/removal/root recipe changed')
        if name.startswith('actual'):
            expected,coverage,actual_diagonal_comparison=true_input_raw_comparison(folder,d)
            counts['actual_input_records']=coverage['records'];counts['radial_groups']=coverage['radial_scalar_group_records'];counts['actual_macro_moment_records']=coverage['physical_macro_moment_records']
            for key in ('macro_self_diagonal_words','explicit_stored_self_diagonal_words','structurally_absent_P2_positive_zero_words'):counts[key]=coverage[key]
        else:expected=expected_synthetic(folder/(name+'.inputs.bin'),nl,precision)
        for g in range(370):
            old,rebuilt,new=[row[2][g] for row in records]
            # The old anisotropic tail was malloc-owned/undefined. Preserve it,
            # but never assert finite/bitwise correctness or use it as physics.
            if old['total']!=rebuilt['total'] or old['self'][:100]!=rebuilt['self'][:100]:raise ValueError('recovered source does not reproduce defined actual archive fields')
            if old['recipe']!=rebuilt['recipe'] or old['recipe']!=new['recipe']:raise ValueError('actual radial R/basis/coeff/sigma/error recipes changed')
            if nl==1:
                if new['total']!=old['total'] or new['self']!=old['self']:raise ValueError('legacy scalar assembly changed')
            elif new['total']!=expected[g][0] or new['self']!=expected[g][1]:raise ValueError('physical T/P0/P1/P2 are not exact original macro bytes')
            finite_words(new['total'],'f');finite_words(new['self'],'f')
            # Recipe layout: optionalR64, R32, B32, coeff32, sigma64,error64.
            cursor=0
            if precision==64:
                finite_words(new['recipe'][:192],'d');cursor=192
                real64=struct.unpack('<24d',new['recipe'][:192])
                mirror=b''.join(struct.pack('<f',x) for x in real64)
                if mirror!=new['recipe'][192:288]:raise ValueError('R64/R32 demote mirror differs')
            finite_words(new['recipe'][cursor:cursor+140],'f');finite_words(new['recipe'][cursor+140:],'d')
            counts['physical_T_self_words']+=25*(1+nl)
    if (counts['radial_groups']!=1110 or counts['actual_macro_moment_records']!=1110 or counts['macro_self_diagonal_words']!=26640
        or counts['explicit_stored_self_diagonal_words']+counts['structurally_absent_P2_positive_zero_words']!=26640):raise ValueError('actual370x3 true radial and macro-moment/diagonal input coverage incomplete')
    for case in d['control_contract']['negative_cases']:
        folder=OUT/'controls'/('negative_'+case['name'])
        lines=[json.loads(x) for x in (folder/'manifest.jsonl').read_text().splitlines()]
        if lines[-1]!=dict(kind='negative_expected',case=case['name'],expected_XABORT=case['expected_message']):raise ValueError('negative identity-specific declaration differs')
        if require(folder/'actual_abort.txt').read_text()!=case['expected_message']+'\n' or (folder/'unexpected_return.txt').exists():raise ValueError('actual native exact expected rejection required')
        for p in ('damaged_macro.xsm','damaged_snapshots.xsm','negative_'+case['name']+'.inputs.bin'):require(folder/p)
    return dict(schema='AXMAT_SPOASM_FULL_RAW_NATIVE_CONTROL_AUDIT_V1',classification='PASS',counts=counts,
        actual_archive_and_rebuilt_defined_fields_bitexact=True,all_physical_T_self_Pn_bitexact=True,
        radial_R_basis_recipe_diagnostics_bitexact=True,legacy_scalar_bitexact=True,all_true_input_records_bitexact=True,
        actual_current_370x3_radial_scalar_ABI_verified=True,all_native_negative_rejections=True,
        actual_macro_packed_self_diagonal_comparison=actual_diagonal_comparison,
        no_extra_2l_plus_1_in_self_coefficients=True,raw_receipt=pin(OUT/'raw_controls_receipt.json'),
        old_undefined_higher_tail_not_used_as_equivalence_target=True,full_original_object_instruction_equivalence_claimed=False,
        scientific_qualification=False,transport_calls=0,linear_solves=0)


def binary_audit(d):
    paths=dict(production_object=OUT/'build/SPOASM.o',rebuilt_reference=OUT/'build/SPOASM.baseline_rebuilt.o',unit=OUT/'build/SPOASM.physical_unit.o',
        actual_original=BASE_OBJECT,runtime=OUT/'runtime/Dragon',controls=OUT/'runtime/spoasm_physical_controls')
    raw={}
    for name,path in paths.items():
        for kind,args in (('symbols',['/usr/bin/nm','-gU',str(path)]),('debug',['/usr/bin/dwarfdump','--debug-info',str(path)])):
            target=OUT/'audit'/(name+'_'+kind+'.txt')
            stderr=OUT/'audit'/(name+'_'+kind+'.stderr')
            with target.open('xb') as f,stderr.open('xb') as err:subprocess.run(args,check=True,stdout=f,stderr=err,timeout=60)
            raw[name+'_'+kind]=pin(target)
            raw[name+'_'+kind+'_stderr']=pin(stderr)
    for name in ('production_object','actual_original'):
        target=OUT/'audit'/(name+'_instructions.txt')
        stderr=OUT/'audit'/(name+'_instructions.stderr')
        with target.open('xb') as f,stderr.open('xb') as err:
            subprocess.run(['/usr/bin/otool','-tV',str(paths[name])],check=True,stdout=f,stderr=err,timeout=60)
        raw[name+'_instructions']=pin(target)
        raw[name+'_instructions_stderr']=pin(stderr)
    write_new(OUT/'audit/raw_binary_receipt.json',dict(files=raw,before_binary_gates=True))
    def symbols(name):return [x.split()[-1] for x in Path(raw[name+'_symbols']['path']).read_text().splitlines() if x.split()]
    for name,symbol in (('production_object','_spoasm_'),('actual_original','_spoasm_'),('rebuilt_reference','_spoasm_baseline_rebuilt_'),('unit','_spoasm_physical_unit_')):
        if symbols(name).count(symbol)!=1:raise ValueError('actual distinct original/rebuilt/private native definitions required')
    for sym in ('_spoasm_','_flu_','_flu2dr64_','_spot1p64_'):
        if symbols('runtime').count(sym)!=1:raise ValueError('production definitions are missing/duplicated')
    for sym in ('_spoasm_','_spoasm_baseline_rebuilt_','_spoasm_physical_unit_'):
        if symbols('controls').count(sym)!=1:raise ValueError('actual archive/rebuilt/private calls must coexist in real control executable')
    for name,source in (('production_object','SPOASM.f'),('rebuilt_reference','SPOASM.baseline_rebuilt.f'),('unit','SPOASM.physical_unit.f')):
        if str(SOURCE/source) not in Path(raw[name+'_debug']['path']).read_text():raise ValueError('actual compiled private source unit differs')
    link=list(d['build_commands'][4]);override=str(OUT/'build/SPOASM.o')
    if link.count(override)!=1 or link.index(override)>=link.index(str(LIBRARY)):raise ValueError('real new SPOASM override must precede unchanged archive')
    link.remove(override);link[-1]=str(PARENT/'runtime/Dragon')
    if link!=d['parent_production_link']:raise ValueError('exact cache production link inverse differs')
    if digest(paths['runtime'])==PARENT_RUNTIME_SHA or digest(paths['production_object'])==BASE_OBJECT_SHA:raise ValueError('new assembly source must actually be compiled/linked')
    if hashlib.sha256(archive_member(LIBRARY,'SPOASM.o')).hexdigest()!=BASE_OBJECT_SHA:raise ValueError('original archive member provenance changed')
    return dict(status='PASS',sole_new_production_override='SPOASM.o',exact_parent_link_inverse=True,actual_native_definitions_verified=True,
        actual_original_archive_object_verified=True,raw_metadata=raw,objects={k:pin(v) for k,v in paths.items()},
        complete_source_to_original_object_instruction_equivalence_claimed=False,
        actual_original_archive_semantics_covered_by_three_way_defined_field_controls=True)


def audit_build(sha):
    d=declaration_admission(sha);resources_for(d['resource_roots']).check()
    stages=read(OUT/FAMILY/'stages.json')['stages']
    if [r['label'] for r in stages[:-1]]!=stage_labels(d)[:-1] or [r['command'] for r in stages[:-1]]!=stage_commands(d,sha)[:-1]:raise ValueError('all real ordered build/control stages required')
    if any(r['status']!='PASS' for r in stages[:-1]):raise ValueError('real native commands must all pass once')
    watches=[check_watch(r) for r in stages[:-1]]
    controls=control_audit(d);write_new(OUT/'audit/controls.json',controls)
    binary=binary_audit(d);write_new(OUT/'audit/binary_identity.json',binary)
    write_new(OUT/'audit/result.json',dict(classification='PASS_SPOASM_PHYSICAL_BUILD_CONTROLS_ONLY',declaration_sha256=sha,
        controls=controls,control_status='PASS',binary_status='PASS',previous_stage_watchdogs=watches,
        inherited_rank1_cache_admission=d['inherited_rank1_cache_admission'],fresh_cold_AAA_required=True,
        transport_launched=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    print('AXMAT-SPOASM-PHYSICAL-BUILD-AUDITED',flush=True)


def run_build(sha):
    started=time.monotonic();d=declaration_admission(sha)
    c,full,_=modules();resources=resources_for(d['resource_roots'],c.ResourceFailure);resource_admission(resources)
    write_new(OUT/'execution_claim.json',dict(declaration_sha256=sha,parent_pid=os.getpid(),started_monotonic=started,started_unix=time.time(),retries=0))
    remaining=TOTAL_WALL-(time.monotonic()-started)
    if remaining<=0:raise ValueError('whole build timer exhausted before first child')
    runner=full.OwnRSSSerialExecutor(OUT,remaining,FAMILY,resources)
    result=dict(classification='FAILED_SPOASM_PHYSICAL_BUILD_NO_RETRY',error=None,transport_launched=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,fresh_cold_AAA_required=True)
    try:
        for i,cmd in enumerate(d['build_commands']):
            environment(d);runner.execute(OUT/'build',f'build_{i:02}',cmd,STAGE_WALL)
        write_new(OUT/'runtime/build_identity.json',dict(schema='AXMAT_SPOASM_PHYSICAL_COMPILED_RUNTIME_IDENTITY_V1',
            sole_new_production_overrides=['SPOASM.o'],actual_build_commands=d['build_commands'],
            production_object=pin(OUT/'build/SPOASM.o'),corrected_runtime=pin(OUT/'runtime/Dragon'),
            inherited_rank1_cache_runtime=d['inherited_rank1_cache_admission']['corrected_runtime'],
            inherited_selector_and_source_objects_unchanged=True,exact_parent_link_inverse=True,
            original_library=pin(LIBRARY),actual_original_SPOASM_object=pin(BASE_OBJECT),
            complete_instruction_equivalence_claimed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        try:
            for label,cmd in zip(control_labels(d),control_commands(d)):
                environment(d);runner.execute(OUT/'controls'/label,'execute',cmd,STAGE_WALL)
        finally:
            write_new(OUT/'raw_controls_receipt.json',dict(files=raw_inventory(OUT/'controls'),before_numeric_gates=True))
        runner.execute(OUT/'audit','audit',stage_commands(d,sha)[-1],STAGE_WALL,'AXMAT-SPOASM-PHYSICAL-BUILD-AUDITED')
        stages=read(OUT/FAMILY/'stages.json')['stages']
        if ([r['label'] for r in stages]!=stage_labels(d) or [r['command'] for r in stages]!=stage_commands(d,sha)
            or any(r['status']!='PASS' for r in stages)):raise ValueError('complete all real guarded stages required')
        audit=read(OUT/'audit/result.json')
        if audit['classification']!='PASS_SPOASM_PHYSICAL_BUILD_CONTROLS_ONLY':raise ValueError('full raw/binary audit must pass')
        result.update(classification='COMPLETE_SPOASM_PHYSICAL_BUILD_CONTROLS_ONLY',watchdogs=[check_watch(r) for r in stages],
            runtime_sha256=digest(OUT/'runtime/Dragon'),control_counts=audit['controls']['counts'])
    except BaseException as e:
        result['error']=repr(e);raise
    finally:
        try:
            environment(d);helper().verify_inventory(SOURCE,d['source_inventory']);result['resources']=resources.check()
            size=archive_bytes();elapsed=time.monotonic()-started
            if size>=ARCHIVE_RESERVE or elapsed>=TOTAL_WALL:raise ValueError('whole actual source/out or build time cap exceeded')
            result.update(elapsed_seconds=elapsed,archive_bytes_before_closeout=size)
        except BaseException as e:
            result.update(classification='FAILED_SPOASM_PHYSICAL_BUILD_NO_RETRY',error=repr(e),elapsed_seconds=time.monotonic()-started)
            write_new(OUT/'driver_result.json',result);raise
        write_new(OUT/'driver_result.json',result)
    write_new(OUT/'seal.json',dict(schema='AXMAT_SPOASM_PHYSICAL_BUILD_SEAL_V1',files=raw_inventory(OUT),
        namespace_directories=namespace_directories(OUT)))
    try:
        final_resources=resources.check();final_size=archive_bytes();final_elapsed=time.monotonic()-started
        if final_size>=ARCHIVE_RESERVE or final_elapsed>=TOTAL_WALL:raise ValueError('full post-seal terminal tail cap exceeded')
    except BaseException as e:
        write_new(OUT/'closeout_failure.json',dict(error=repr(e),complete=False,AAA_accuracy_qualified=False,ABA_admitted=False));raise
    print(json.dumps(dict(result=result,actual_tail_check='PASS',actual_elapsed_seconds=final_elapsed,
        actual_archive_bytes=final_size,actual_resources=final_resources),allow_nan=False),flush=True)


def strict_terminal_json(path):
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate key in actual external terminal JSON")
            value[key] = item
        return value
    def reject_constant(value):
        raise ValueError("nonfinite JSON constant in actual external terminal JSON: " + value)
    result = json.loads(Path(path).read_text(), object_pairs_hook=unique_object, parse_constant=reject_constant)
    if type(result) is not dict:
        raise ValueError("the full actual terminal output must be one JSON object")
    return result


def terminal_file(value, expected_sha=None):
    if not isinstance(value, (str, Path)):
        raise ValueError("actual external terminal evidence requires an absolute canonical regular path")
    path = Path(value)
    if (not path.is_absolute() or ".." in path.parts or str(value) != str(path)
            or path.parent != TERMINAL or path.resolve(strict=True) != path):
        raise ValueError("actual external terminal path is outside its independent fixed root")
    cursor = path
    while True:
        if cursor.is_symlink():
            raise ValueError("external terminal evidence or ancestor is a symlink")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    return require(path, expected_sha)


def external_terminal_admission(d, declared_sha, expected_seal, sealed_result,
                                terminal_evidence, terminal_evidence_sha256):
    """Require Root's retained real exit-zero proof after all closeout work.

    A success seal can exist while this parent still runs or after interruption.
    It is never sufficient without this independently produced terminal record.
    This factory neither creates that record nor infers exit zero from a flag.
    """
    if (not isinstance(terminal_evidence_sha256, str) or len(terminal_evidence_sha256) != 64
            or any(c not in "0123456789abcdef" for c in terminal_evidence_sha256)):
        raise ValueError("actual independent terminal-return receipt SHA256 is mandatory")
    if (TERMINAL.parent != ART or TERMINAL in (SOURCE, OUT)
            or any(TERMINAL.is_relative_to(root) or root.is_relative_to(TERMINAL) for root in (SOURCE, OUT))
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("external terminal root must be independent and within the declared total-history scope")
    receipt = terminal_file(terminal_evidence, terminal_evidence_sha256)
    if receipt != TERMINAL / "terminal_return.json":
        raise ValueError("only the fixed actual external terminal-return record is eligible")
    e = strict_terminal_json(receipt)
    factory = Path(__file__).resolve()
    source_pin = dict(path=str(factory), sha256=digest(require(factory)))
    command = [d["build_python_executable"], str(factory), "run-build", "--sha256", declared_sha]
    if (e["schema"] != TERMINAL_SCHEMA or e["record_producer"] != "root"
            or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True
            or type(e["returncode"]) is not int or e["returncode"] != 0
            or e["command"] != command or e["source"] != source_pin
            or d["files"].get(str(factory)) != source_pin["sha256"]
            or e["declaration"] != dict(path=str(OUT / "declaration.json"), sha256=declared_sha)
            or e["build_seal"] != dict(path=str(OUT / "seal.json"), sha256=expected_seal)):
        raise ValueError("actual Root exit-zero evidence must bind this exact source/declaration/build seal")
    stdout = terminal_file(e["full_stdout"]["path"], e["full_stdout"]["sha256"])
    stdout_pin = dict(path=str(stdout), sha256=digest(stdout))
    stderr = terminal_file(e['full_stderr']['path'],e['full_stderr']['sha256'])
    stderr_pin = dict(path=str(stderr),sha256=digest(stderr))
    if len({receipt,stdout,stderr})!=3 or e["full_stdout"] != stdout_pin or e['full_stderr']!=stderr_pin:
        raise ValueError("full actual stdout/stderr must be separately retained regular files")
    returned = strict_terminal_json(stdout)
    tail = {key: returned[key] for key in TAIL_FIELDS}
    if returned != dict(result=sealed_result, **tail) or any(e[key] != tail[key] for key in TAIL_FIELDS):
        raise ValueError("full actual stdout, sealed result and Root terminal-tail values differ")
    elapsed, retained_bytes, snapshot = tail["actual_elapsed_seconds"], tail["actual_archive_bytes"], tail["actual_resources"]
    actual_bytes = archive_bytes()
    if (tail["actual_tail_check"] != "PASS" or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or type(retained_bytes) is not int or not 0 <= retained_bytes < ARCHIVE_RESERVE or retained_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or snapshot["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["declared_resource_roots"] != d["resource_roots"]
            or type(snapshot["resource_roots"]) is not list
            or not set(d["resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int
            or not retained_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float) or not math.isfinite(snapshot["checked_unix"])
            or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete terminal-tail wall/archive/resource gates must hold")
    validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=dict(path=str(receipt), sha256=digest(receipt)), full_stdout=stdout_pin, full_stderr=stderr_pin,
                command=command, schema=TERMINAL_SCHEMA, **tail)


def production_admission(build_seal_sha,terminal_evidence,terminal_evidence_sha256):
    """Read-only input admission after true Root terminal return; never AAA/ABA."""
    if not re.fullmatch('[0-9a-f]{64}',build_seal_sha or ''):raise ValueError('actual successful build seal SHA required')
    seal=read(require(OUT/'seal.json',build_seal_sha))
    if seal['schema']!='AXMAT_SPOASM_PHYSICAL_BUILD_SEAL_V1':raise ValueError('actual new build seal required')
    actual=raw_inventory(OUT)
    if (set(actual)!=set(seal['files'])|{'seal.json'} or any(actual[p]!=wanted for p,wanted in seal['files'].items())
        or namespace_directories(OUT)!=seal['namespace_directories']):raise ValueError('exact complete successful build file/directory namespace required')
    declared_sha=digest(OUT/'declaration.json');d=declaration_admission(declared_sha,require_build_interpreter=False)
    result=read(require(OUT/'driver_result.json'));audit=read(require(OUT/'audit/result.json'))
    if (result['classification']!='COMPLETE_SPOASM_PHYSICAL_BUILD_CONTROLS_ONLY' or result['error'] is not None
        or audit['classification']!='PASS_SPOASM_PHYSICAL_BUILD_CONTROLS_ONLY' or audit['declaration_sha256']!=declared_sha
        or audit['control_status']!='PASS' or audit['binary_status']!='PASS'
        or audit['inherited_rank1_cache_admission']!=d['inherited_rank1_cache_admission']
        or result['runtime_sha256']!=digest(OUT/'runtime/Dragon') or result['control_counts']!=audit['controls']['counts']
        or result['fresh_cold_AAA_required'] is not True or audit['fresh_cold_AAA_required'] is not True
        or any(result[k] is not False or audit[k] is not False for k in ('transport_launched','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('only complete actual native assembly controls may admit this runtime as an input')
    controls=control_audit(d)
    if controls!=read(require(OUT/'audit/controls.json')) or audit['controls']!=controls:raise ValueError('complete fresh raw native control audit differs')
    binary=read(require(OUT/'audit/binary_identity.json'))
    if (binary['status']!='PASS' or binary['sole_new_production_override']!='SPOASM.o'
        or binary['exact_parent_link_inverse'] is not True or binary['actual_native_definitions_verified'] is not True
        or binary['actual_original_archive_object_verified'] is not True
        or binary['actual_original_archive_semantics_covered_by_three_way_defined_field_controls'] is not True):
        raise ValueError('actual native source/object/archive/link identities required')
    for item in [*binary['raw_metadata'].values(),*binary['objects'].values()]:require(item['path'],item['sha256'])
    identity=read(require(OUT/'runtime/build_identity.json'))
    if (identity['sole_new_production_overrides']!=['SPOASM.o'] or identity['actual_build_commands']!=d['build_commands']
        or identity['production_object']!=pin(OUT/'build/SPOASM.o') or identity['corrected_runtime']!=pin(OUT/'runtime/Dragon')
        or identity['inherited_rank1_cache_runtime']!=d['inherited_rank1_cache_admission']['corrected_runtime']
        or identity['inherited_selector_and_source_objects_unchanged'] is not True or identity['exact_parent_link_inverse'] is not True
        or identity['original_library']!=pin(LIBRARY) or identity['actual_original_SPOASM_object']!=pin(BASE_OBJECT)):
        raise ValueError('sole new override and unchanged actual cache link inputs required')
    stages=read(require(OUT/FAMILY/'stages.json'))['stages']
    if ([r['label'] for r in stages]!=stage_labels(d) or [r['command'] for r in stages]!=stage_commands(d,declared_sha)
        or any(r['status']!='PASS' for r in stages)):raise ValueError('complete real ordered original supervised stages required')
    watches=[check_watch(r) for r in stages]
    if watches!=result['watchdogs'] or watches[:-1]!=audit['previous_stage_watchdogs']:raise ValueError('sealed actual bounded stage watches differ')
    terminal=external_terminal_admission(d,declared_sha,build_seal_sha,result,terminal_evidence,terminal_evidence_sha256)
    resources_for(d['resource_roots']).check()
    prior=d['inherited_rank1_cache_admission']
    inherited={k:prior[k] for k in ('future_contract','capture_dependency','source_and_receiver_controls','dispatch_evidence',
        'compiled_selector','actual_control_rows','actual_selector_invocations','actual_source_unit_invocations',
        'inherited_native_receiver_calls','newly_executed_original_interface_receiver_calls','cache_unit_control_counts',
        'rank1_factor_cache_controls_passed','all_new_cache_outputs_bitwise_equal_to_uncached',
        'operator_identity_guard_negative_controls_passed','rank1_factor_cache_math_and_rhs_order_unchanged',
        'rank1_factor_cache_budget_bytes','future_actual_factor_cache_observer_required','future_actual_FLU_observer_required',
        'future_bounded_progress_observer')}
    return dict(schema='AXMAT_SPOASM_PHYSICAL_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',
        admission='SPOASM_PHYSICAL_ASSEMBLY_RUNTIME_INPUT_ONLY',build_root=str(OUT),source_root=str(SOURCE),
        build_seal_sha256=build_seal_sha,corrected_runtime=pin(OUT/'runtime/Dragon'),source_admission=pin(SOURCE/'source_admission.json'),
        inherited_rank1_cache_admission=prior,predecessor=prior,actual_current_input_control=d['actual_current_input_control'],
        actual_external_terminal_evidence=terminal['receipt'],actual_external_terminal_validation=terminal,
        actual_local_supervisor_helper=d['actual_local_supervisor_helper'],
        actual_supervisor_constructor_preflight=d['actual_supervisor_constructor_preflight'],
        prior_constructor_failure_input=d['prior_constructor_failure_input'],
        compiled_unit_controls=pin(OUT/'audit/controls.json'),compiled_physical_assembly_identity=pin(OUT/'audit/binary_identity.json'),
        compiled_cache_identity=prior['compiled_cache_identity'],compiled_cache_controls=prior['compiled_unit_controls'],
        inherited_selector_source_cache_controls_not_newly_executed=True,source_and_receiver_controls_inherited_not_newly_executed=True,
        inherited_controls_are_input_identity_not_current_transport_accuracy=True,
        actual_physical_assembly_control_counts=controls['counts'],all_actual370x3_radial_inputs_and_physical_macro_moments_bitexact=True,
        all_defined_original_archive_and_rebuilt_fields_bitexact=True,radial_P0_R_basis_source_and_recipe_unchanged=True,
        actual_macro_NW_supported=0,actual_macro_TRANC_option_not_mistaken_for_already_corrected_raw_XS=True,
        legacy_scalar_assembly_bitexact=True,no_extra_2l_plus_1_in_self_coefficients=True,
        sole_new_production_overrides=['SPOASM.o'],corrected_sender_retained=True,white_closure_unchanged=True,
        collision_self_operator_unchanged=False,angle_grid_unchanged=True,radial_arithmetic_unchanged=True,physical_data_unchanged=True,
        original_accuracy_thresholds_changed=False,no_CE_fitting=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY,resource_scope_contract=d['resource_scope_contract'],current_complete_history_admission_required=True,
        actual_dynamic_resource_class_factory=pin(actual_resource_class_factory().__file__),new_build_factory_is_lazy_class_constructor=True,
        cache_memory_hardcap_and_OwnRSS_are_distinct=True,new_transport_RSS_fitness_proved_by_assembly_controls=False,
        fresh_cold_AAA_required=True,actual_full_FLU_entry_executed=False,full_FLU_entry_execution_proved_by_build=False,
        production_pipeline_prepared=False,AAA_accuracy_qualified=False,ABA_admitted=False,**inherited)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare-build','run-build','audit-build','admit'))
    parser.add_argument('--rank1-cache-build-seal-sha256')
    parser.add_argument('--rank1-cache-terminal-evidence')
    parser.add_argument('--rank1-cache-terminal-evidence-sha256')
    parser.add_argument('--patch-helper-sha256');parser.add_argument('--controls-source-sha256')
    parser.add_argument('--sha256');parser.add_argument('--terminal-evidence');parser.add_argument('--terminal-evidence-sha256')
    args=parser.parse_args()
    {'prepare-build':lambda:prepare_build(args.rank1_cache_build_seal_sha256,args.rank1_cache_terminal_evidence,
        args.rank1_cache_terminal_evidence_sha256,args.patch_helper_sha256,args.controls_source_sha256),
     'run-build':lambda:run_build(args.sha256),'audit-build':lambda:audit_build(args.sha256),
     'admit':lambda:print(json.dumps(production_admission(args.sha256,args.terminal_evidence,args.terminal_evidence_sha256),allow_nan=False))}[args.action]()

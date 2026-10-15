"""Reviewed factory for a combined-runtime link, with no new mathematical controls.

Two admitted production objects are linked into the complete original92 recipe.
This family does not execute Dragon or compile a replacement numerical source.
The actual file-SNAP capture seal and Root exit-zero are prerequisite inputs;
that original-operator capture gives no combined-runtime RSS or cold qualification.
Business actions require the reviewed formal source location and single threads.
Actual link execution, complete Root closeout and three-argument admission remain
mandatory before this new runtime can be used as an input to fresh cold AAA.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
SOURCE = ART/'axial-material-qualified-AB-physical-dedup-combined-runtime-build-admission-20261007'
OUT = ART/'axial-material-physical-dedup-combined-runtime-build-20261007'
TERMINAL = ART/'axial-material-qualified-AB-physical-dedup-combined-runtime-build-terminal-20261007'
FAMILY = 'COMBINED_RUNTIME_LINK'
DRAFT_STATUS = 'READY_REVIEWED_ACTUAL_CAPTURE_AND_FORMAL_FACTORY'
CAPTURE_SEAL_SHA = '12756df88672c4438149119026edba0b2ef78780dffa5dcc522bcd06771d5296'
CAPTURE_TERMINAL_SHA = 'd5496707eb1ad08826eec599dbf6035b9e39df67cf68a92e84db62bcbb753e63'
CAPTURE_FACTORY = ROOT/'validation/axial_material/prepare_rank1_cache_memory_dedup_file_snapshot_native_angular_capture.py'
CAPTURE_FACTORY_SHA = '48ffa6568487bd4d57503cb9a6e8ee8b70ae7e24584e1757363a1ab4874bfc6c'
CAPTURE_OUT = ART/'axial-material-rank1-cache-memory-dedup-file-snapshot-native-angular-capture-20261007'
CAPTURE_SOURCE = ART/'axial-material-rank1-cache-memory-dedup-file-snapshot-native-angular-capture-admission-20261007'
CAPTURE_TERMINAL = ART/'axial-material-rank1-cache-memory-dedup-file-snapshot-native-angular-capture-terminal-20261007/terminal_return.json'
OLD = ART/'axial-material-rank1-factor-cache-build-20261007'
OLD_SOURCE = ART/'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007'
OLD_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_production.py'
OLD_FACTORY_SHA = '92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
OLD_SEAL_SHA = 'e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f'
OLD_TERMINAL = ART/'axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007/terminal_return.json'
OLD_TERMINAL_SHA = 'c5eecbff0064a9285460c98bc01bad26ab9180a4b4e38a6186be779378ba9d96'
PHYSICAL = ART/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007'
PHYSICAL_SOURCE = ART/'axial-material-qualified-AB-spoasm-physical-abi-serial-guarded-build-admission-20261007'
PHYSICAL_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_spoasm_physical_abi_serial_guarded_production.py'
PHYSICAL_FACTORY_SHA = 'b7f361bc1d8dcdcfabf1cd2d33af3730ffb146ebe610e12370ea2b409f1ca230'
PHYSICAL_SEAL_SHA = 'bad5921e7c7b5a21b9c983b80c74ce0938594200c267e16040242b1bfbf6777d'
PHYSICAL_TERMINAL = ART/'axial-material-qualified-AB-spoasm-physical-abi-serial-guarded-build-terminal-20261007/terminal_return.json'
PHYSICAL_TERMINAL_SHA = '16117d4183730050016cf96b9d8b513f596e286ad66a3107d20356e0f6c2f2f1'
PHYSICAL_OBJECT = PHYSICAL/'build/SPOASM.o'
PHYSICAL_OBJECT_SHA = 'ef6e7dedd4adf634a6835c69bede0c29216ad969558b468e6d93ea888227a424'
DEDUP = ART/'axial-material-rank1-factor-cache-memory-dedup-build-20261007'
DEDUP_SOURCE = ART/'axial-material-qualified-AB-rank1-factor-cache-memory-dedup-build-admission-20261007'
DEDUP_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_memory_dedup_production.py'
DEDUP_FACTORY_SHA = '4ae768d5e06b64685c1626326de6e93d2e87b7d502f991bf1d7c06f169622c29'
DEDUP_SEAL_SHA = 'fd63bae4d542d735a8ad363de63c8e978b4318e4baea0176820d93624b39ea61'
DEDUP_TERMINAL = ART/'axial-material-qualified-AB-rank1-factor-cache-memory-dedup-build-terminal-20261007/terminal_return.json'
DEDUP_TERMINAL_SHA = '09b904094ecaf1fcc7d9979a02bf95629d26f761c53c06e66a7dd2ce52bd070e'
DEDUP_OBJECT = DEDUP/'build/SPOT1P64.o'
DEDUP_OBJECT_SHA = 'c3983c6a0af16d91f737225c026d08319a07b91ce4f5e12d626ae3e3f38c6d79'
DEDUP_KERNEL_SHA = '50071dfc713cd1a7f319e392706686c73ef250ea03049a91ef29d5dec341adb6'
BOUNDED = OLD/'runtime/run_bounded_dragon.py'
BOUNDED_SHA = 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
NM, OTOOL = Path('/usr/bin/nm'), Path('/usr/bin/otool')
TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512
RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30
HISTORY_POLICY = 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
TAIL_FIELDS = ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
PREFIX = 'AXMAT_COMBINED_PHYSICAL_DEDUP_RUNTIME'
TERMINAL_SCHEMA = PREFIX+'_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'


def nonzero_sha(value):
    if not isinstance(value,str) or re.fullmatch('[0-9a-f]{64}',value) is None or value=='0'*64:
        raise ValueError('actual nonplaceholder SHA256 required')
    return value


def require_ready():
    # This check precedes all actual reads, imports, resource probes and writes.
    if DRAFT_STATUS!='READY_REVIEWED_ACTUAL_CAPTURE_AND_FORMAL_FACTORY':
        raise ValueError('UNREADY: actual successful capture and formal source review required')
    nonzero_sha(CAPTURE_SEAL_SHA);nonzero_sha(CAPTURE_TERMINAL_SHA)
    if Path(__file__).absolute().parent!=ROOT/'validation/axial_material':
        raise ValueError('TMP-only source cannot perform a business action')
    if any(os.environ.get(key)!='1' for key in THREAD_KEYS):
        raise ValueError('single-thread environment required before any project import')


def normal(path,missing=False):
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts:raise ValueError('absolute canonical path required')
    for p in [*reversed(path.parents),path]:
        try:s=p.lstat()
        except FileNotFoundError:
            if missing:continue
            raise
        if stat.S_ISLNK(s.st_mode):raise ValueError('ordinary root/ancestor aliases forbidden: '+str(p))
        if p!=path and not stat.S_ISDIR(s.st_mode):raise ValueError('ordinary parent must be a directory')
    return path


def digest(path):
    path=normal(path)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd)
        if not stat.S_ISREG(first.st_mode):raise ValueError('only regular inputs may be hashed')
        h=hashlib.sha256();count=0
        while raw:=os.read(fd,1024*1024):h.update(raw);count+=len(raw)
        last=os.fstat(fd)
        if (first.st_dev,first.st_ino,first.st_size,first.st_mtime_ns,first.st_ctime_ns)!=(last.st_dev,last.st_ino,last.st_size,last.st_mtime_ns,last.st_ctime_ns) or count!=first.st_size:
            raise ValueError('input changed during its fresh byte verification')
        return h.hexdigest()
    finally:os.close(fd)


def require(path,sha=None):
    path=normal(path)
    if not path.is_file() or (sha is not None and digest(path)!=nonzero_sha(sha)):
        raise ValueError('missing/changed input: '+str(path))
    return path


def pin(path):return dict(path=str(require(path)),sha256=digest(path))


def strict_json_bytes(raw):
    def pairs(items):
        value={}
        for key,item in items:
            if key in value:raise ValueError('duplicate JSON key')
            value[key]=item
        return value
    def reject(value):raise ValueError('nonfinite JSON constant: '+value)
    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)
    def finite(item):
        if isinstance(item,float) and not math.isfinite(item):raise ValueError('nonfinite JSON number')
        if isinstance(item,dict):
            for v in item.values():finite(v)
        elif isinstance(item,list):
            for v in item:finite(v)
    finite(value);return value


def read(path):return strict_json_bytes(require(path).read_bytes())


def write_new(path,value):
    path=normal(path,missing=True)
    with path.open('x') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())


def inventory(root):
    root=normal(root);files={};directories=[]
    if not root.is_dir():raise ValueError('complete inventory requires a directory')
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs:
            path=normal(Path(folder)/name)
            if not path.is_dir():raise ValueError('invalid inventory directory')
            directories.append(str(path.relative_to(root)))
        for name in names:
            path=require(Path(folder)/name);files[str(path.relative_to(root))]=digest(path)
    return dict(files=files,symlinks={},directories=sorted(directories))


def verify_inventory(root,wanted):
    if inventory(root)!=wanted:raise ValueError('complete file/directory/alias namespace differs')


def absent(path):
    normal(path,missing=True)
    if os.path.lexists(path):raise ValueError('exclusive new family; no overwrite or retry')


def load(path,sha,name):
    require_ready();path=require(path,sha)
    if name in sys.modules:
        m=sys.modules[name]
        if Path(m.__file__).resolve()!=path or Path(m.__spec__.origin).resolve()!=path:raise ValueError('actual module binding differs')
        return m
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m;spec.loader.exec_module(m)
    if Path(m.__file__).resolve()!=path or Path(m.__spec__.origin).resolve()!=path:raise ValueError('actual import source differs')
    return m


def builder():return load(OLD_FACTORY,OLD_FACTORY_SHA,'combined_runtime_actual_original92')


def modules():
    b=builder();h=b.helper();full,c=h.modules();h.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):raise ValueError('genuine tested class/MRO required')
    return b,h,full,c


def DynamicHistoryResources(art,roots,free,cap,failure_type=None):
    return builder().DynamicHistoryResources(art,roots,free,cap,failure_type)


def resources_for(roots,failure=None):
    b=builder();values=[str(p) for p in b.validate_history_roots(roots,ART)]
    return DynamicHistoryResources(ART,values,FREE_FLOOR,HISTORY_CAP,failure)


def archive_bytes():
    total=0
    for root in (SOURCE,OUT):
        normal(root,missing=True)
        if not root.exists():continue
        for folder,dirs,names in os.walk(root,followlinks=False):
            for n in dirs:normal(Path(folder)/n)
            for n in names:total+=require(Path(folder)/n).stat().st_size
    return total


def combined_link_command(old_link,physical_object,dedup_object,output):
    """Exactly two object substitutions/additions and the output identity."""
    old_kernel=OLD/'build/SPOT1P64.o';archive=ROOT/'lib/Darwin_arm64/libDragon.a'
    command=list(old_link)
    if (Path(physical_object)!=PHYSICAL_OBJECT or Path(dedup_object)!=DEDUP_OBJECT
        or Path(output)!=OUT/'runtime/Dragon' or command.count(str(old_kernel))!=1
        or command.count(str(archive))!=1 or command[-2:]!=['-o',str(OLD/'runtime/Dragon')]
        or any(Path(token).name=='SPOASM.o' for token in command)
        or command.index(str(old_kernel))>=command.index(str(archive))):
        raise ValueError('complete original92 link and genuine component object identities required')
    command[command.index(str(old_kernel))]=str(dedup_object)
    command.insert(command.index(str(archive)),str(physical_object));command[-1]=str(output)
    inverse=list(command);inverse.remove(str(physical_object))
    inverse[inverse.index(str(dedup_object))]=str(old_kernel);inverse[-1]=str(OLD/'runtime/Dragon')
    if inverse!=list(old_link):raise ValueError('whole link-token inverse differs')
    return command,dict(original_link_command=list(old_link),combined_link_command=command,
        exact_original92_token_inverse=True,sole_object_changes=['SPOT1P64.o','SPOASM.o'],
        all_other_objects_flags_library_tokens_unchanged=True,observer_objects_linked=False)


def component_contract(original,physical,dedup,capture,physical_identity,old_d,physical_d,dedup_d):
    """Whole actual immutable returns, with explicit independent scope checks."""
    if (original['schema']!='AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or physical['schema']!='AXMAT_SPOASM_PHYSICAL_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or dedup['schema']!='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or capture['schema']!='AXMAT_RANK1_MEMORY_DEDUP_FILE_SNAPSHOT_NATIVE_ANGULAR_CAPTURE_INPUT_ADMISSION_V1'
        or physical['inherited_rank1_cache_admission']!=original
        or dedup['inherited_rank1_factor_cache_admission']!=original
        or capture['inherited_current_build_admission']!=original
        or capture['inherited_memory_build_admission']!=dedup['inherited_rank1_factor_cache_memory_admission']
        or capture['inherited_dedup_build_admission']!=dedup):raise ValueError('all component full returns and common ancestry must agree')
    if (original['admission']!='RANK1_FACTOR_CACHE_RUNTIME_INPUT_ONLY'
        or physical['admission']!='SPOASM_PHYSICAL_ASSEMBLY_RUNTIME_INPUT_ONLY'
        or dedup['admission']!='RANK1_FACTOR_CACHE_MEMORY_DEDUP_RUNTIME_INPUT_ONLY'
        or capture['admission']!='CURRENT_MAP012_NATIVE_ANGULAR_DIAGNOSTIC_ONLY'):
        raise ValueError('all exact INPUT-only component admission scopes required')
    for value,root,seal,terminal,terminal_sha in ((original,OLD,OLD_SEAL_SHA,OLD_TERMINAL,OLD_TERMINAL_SHA),
        (physical,PHYSICAL,PHYSICAL_SEAL_SHA,PHYSICAL_TERMINAL,PHYSICAL_TERMINAL_SHA),
        (dedup,DEDUP,DEDUP_SEAL_SHA,DEDUP_TERMINAL,DEDUP_TERMINAL_SHA)):
        if (value['build_root']!=str(root) or value['build_seal_sha256']!=seal
            or value['actual_external_terminal_evidence']!=dict(path=str(terminal),sha256=terminal_sha)
            or value['resource_scope_policy']!=HISTORY_POLICY
            or value['resource_scope_contract']!=original['resource_scope_contract']
            or value['actual_full_FLU_entry_executed'] is not False
            or value['AAA_accuracy_qualified'] is not False or value['ABA_admitted'] is not False):
            raise ValueError('actual component INPUT-only Root chain/scope differs')
    if (physical['collision_self_operator_unchanged'] is not False
        or physical['new_transport_RSS_fitness_proved_by_assembly_controls'] is not False
        or any(physical[k] is not True for k in ('all_actual370x3_radial_inputs_and_physical_macro_moments_bitexact',
            'all_defined_original_archive_and_rebuilt_fields_bitexact','radial_P0_R_basis_source_and_recipe_unchanged',
            'legacy_scalar_assembly_bitexact','no_extra_2l_plus_1_in_self_coefficients','physical_data_unchanged',
            'angle_grid_unchanged','white_closure_unchanged','radial_arithmetic_unchanged'))):raise ValueError('actual physical controls required without transport credit')
    if (dedup['compiled_kernel']!=dict(path=str(DEDUP_OBJECT),sha256=DEDUP_OBJECT_SHA)
        or dedup['compiled_kernel_source']['sha256']!=DEDUP_KERNEL_SHA
        or physical_identity['production_object']!=dict(path=str(PHYSICAL_OBJECT),sha256=PHYSICAL_OBJECT_SHA)
        or physical_identity['sole_new_production_overrides']!=['SPOASM.o']
        or physical_identity['actual_build_commands']!=physical_d['build_commands']
        or any(dedup[k] is not True for k in ('lower_repeated_blocks_losslessly_deduplicated',
            'all_original_memory_and_dictionary_controls_bitwise_passed','full_shape_MATMUL_and_RHS_order_unchanged',
            'canonical_dictionary_signed_zero_and_all_unique_fallback_verified'))
        or dedup['native_RSS_proof_obtained'] is not False):raise ValueError('genuine component object/full bit controls required')
    if (capture['actual_native_RSS_under_512_guard_passed'] is not True or capture['scientific_qualification'] is not False
        or capture['AAA_accuracy_qualified'] is not False or capture['ABA_admitted'] is not False
        or capture['production_solver_promoted'] is not False
        or capture['capture_seal']!=dict(path=str(CAPTURE_OUT/'seal.json'),sha256=CAPTURE_SEAL_SHA)
        or capture['actual_external_terminal_evidence']!=dict(path=str(CAPTURE_TERMINAL),sha256=CAPTURE_TERMINAL_SHA)):
        raise ValueError('actual successful original-operator capture, not combined-runtime RSS, required')
    old=old_d['build_commands'][2]
    current=list(dedup_d['production_link_command'])
    if current!=dedup_d['build_commands'][1] or current!=dedup['production_link_command']:raise ValueError('explicit dedup link identity differs')
    current[current.index(str(DEDUP_OBJECT))]=str(OLD/'build/SPOT1P64.o');current[-1]=str(OLD/'runtime/Dragon')
    if current!=old:raise ValueError('complete dedup link inverse differs')
    current=list(physical_d['build_commands'][4]);current.remove(str(PHYSICAL_OBJECT));current[-1]=str(OLD/'runtime/Dragon')
    if current!=old:raise ValueError('complete physical link inverse differs')
    return dict(original92=original,physical=physical,dedup=dedup,capture=capture,
        mathematical_controls_inherited_not_newly_executed=True,
        capture_scope_is_original_operator_only=True,combined_runtime_RSS_not_proved=True)


def actual_components():
    require_ready();b=builder()
    original=b.production_admission(OLD_SEAL_SHA,str(OLD_TERMINAL),OLD_TERMINAL_SHA)
    physical=load(PHYSICAL_FACTORY,PHYSICAL_FACTORY_SHA,'combined_runtime_actual_physical').production_admission(
        PHYSICAL_SEAL_SHA,str(PHYSICAL_TERMINAL),PHYSICAL_TERMINAL_SHA)
    dedup=load(DEDUP_FACTORY,DEDUP_FACTORY_SHA,'combined_runtime_actual_dedup').production_admission(
        DEDUP_SEAL_SHA,str(DEDUP_TERMINAL),DEDUP_TERMINAL_SHA)
    capture=load(CAPTURE_FACTORY,CAPTURE_FACTORY_SHA,'combined_runtime_actual_capture').diagnostic_admission(
        CAPTURE_SEAL_SHA,str(CAPTURE_TERMINAL),CAPTURE_TERMINAL_SHA)
    docs={name:read(root/'declaration.json') for name,root in [('original92',OLD),('physical',PHYSICAL),('dedup',DEDUP),('capture',CAPTURE_OUT)]}
    identity=read(PHYSICAL/'runtime/build_identity.json')
    bodies=component_contract(original,physical,dedup,capture,identity,docs['original92'],docs['physical'],docs['dedup'])
    return bodies,docs


def add_input(files,aliases,path,expected):
    path=Path(path);nonzero_sha(expected)
    if not path.is_absolute() or '..' in path.parts:raise ValueError('explicit absolute input endpoint required')
    target=path.resolve(strict=True);normal(target)
    for part in [*reversed(path.parents),path]:
        if part.is_symlink():
            item=dict(text=os.readlink(part),target=str(part.resolve(strict=True)))
            if str(part) in aliases and aliases[str(part)]!=item:raise ValueError('conflicting explicit alias')
            aliases[str(part)]=item
    key=str(target)
    if key in files and files[key]!=expected:raise ValueError('conflicting true input SHA owner')
    require(target,expected);files[key]=expected


def descriptor_inputs(value,files,aliases):
    if isinstance(value,dict):
        if 'path' in value and 'sha256' in value:add_input(files,aliases,value['path'],value['sha256'])
        for item in value.values():descriptor_inputs(item,files,aliases)
    elif isinstance(value,list):
        for item in value:descriptor_inputs(item,files,aliases)


def verify_inputs(d):
    for path,item in d['aliases'].items():
        p=Path(path)
        if not p.is_symlink() or os.readlink(p)!=item['text'] or str(p.resolve(strict=True))!=item['target']:
            raise ValueError('declared alias literal/canonical target changed')
        normal(item['target'])
    for path,sha in d['files'].items():require(path,sha)
    for entry in d['component_namespaces']:verify_inventory(entry['root'],entry['inventory'])
    verify_inventory(SOURCE,d['source_inventory'])


def environment(d,require_build_interpreter=True):
    require_ready();b=builder();b.helper().environment(read(OLD/'declaration.json'),
        require_build_interpreter=require_build_interpreter)
    if any(os.environ.get(key)!='1' for key in THREAD_KEYS):raise ValueError('all declared thread variables must equal one')
    if d['resource_scope_contract']!=b.resource_scope_contract() or d['resource_scope_policy']!=HISTORY_POLICY:
        raise ValueError('original family96/globalfree8 resource contract differs')
    bodies,_=actual_components()
    if bodies!=d['actual_components']:raise ValueError('whole actual component returns changed')
    verify_inputs(d);resources_for(d['resource_roots']).check()


def stage_labels():return ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']


def stage_commands(d,expected):
    obj=d['actual_production_objects']
    return [d['production_link_command'],[str(NM),'-g',*obj],
        [str(NM),'-g',str(OUT/'runtime/Dragon')],
        [str(OTOOL),'-L',str(OUT/'runtime/Dragon'),str(OLD/'runtime/Dragon'),str(PHYSICAL/'runtime/Dragon'),str(DEDUP/'runtime/Dragon')],
        [d['python_command'],str(Path(__file__).resolve()),'audit-build','--sha256',expected]]


def terminal_contract(python):
    return dict(schema=TERMINAL_SCHEMA,root=str(TERMINAL),receipt=str(TERMINAL/'terminal_return.json'),
        python=python,action='run-build',record_producer='root',actual_tool_exit_zero_required=True,
        full_stdout_required=True,full_stderr_required=True,tail_fields=list(TAIL_FIELDS),
        record_written_after_actual_terminal_return_required=True,complete_archive_scope_roots=[str(SOURCE),str(OUT)],
        combined_runtime_RSS_proved=False,full_FLU_proved=False,scientific_qualification=False)


def supervisor_constructor_preflight(full,c,resources):
    """Real original constructor and actual local bc4 file; no child launch."""
    require(OUT/'runtime/run_bounded_dragon.py',BOUNDED_SHA)
    if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):raise ValueError('actual original supervisor MRO required')
    runner=full.OwnRSSSerialExecutor(OUT,TOTAL_WALL,FAMILY,resources)
    if (type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources
        or runner.stages_path!=OUT/FAMILY/'stages.json' or runner.records!=[]
        or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py'
        or any(runner.env.get(k)!='1' for k in THREAD_KEYS)):
        raise ValueError('real inherited constructor/local bounded helper binding differs')
    return dict(actual_original_constructor_exercised=True,native_or_numeric_child_launched=False,
        local_bounded_helper=pin(OUT/'runtime/run_bounded_dragon.py'),
        genuine_supervisor_source=pin(Path(full.__file__).resolve()),
        genuine_parent_class_source=pin(Path(c.__file__).resolve()),
        class_name='OwnRSSSerialExecutor',genuine_parent_class_name='SerialExecutor',
        whole_stage_storage_parent_created=True,stages_path=str(OUT/FAMILY/'stages.json'))


def expected_supervisor_constructor(d):
    """Immutable build proof; readonly consumer never imports old canonical c."""
    h=builder().helper();parent=Path(h.PROD)/'runtime/production_runner.py'
    supervisor=dict(path=str(h.FULL_SOURCE),sha256=h.FULL_SHA)
    expected_parent=dict(path=str(parent),sha256=d['files'][str(parent)])
    if d['genuine_supervisor_source']!=supervisor or d['genuine_parent_class_source']!=expected_parent:
        raise ValueError('real frozen original supervisor/parent source owners differ')
    return dict(actual_original_constructor_exercised=True,native_or_numeric_child_launched=False,
        local_bounded_helper=dict(path=str(OUT/'runtime/run_bounded_dragon.py'),sha256=BOUNDED_SHA),
        genuine_supervisor_source=supervisor,genuine_parent_class_source=expected_parent,
        class_name='OwnRSSSerialExecutor',genuine_parent_class_name='SerialExecutor',
        whole_stage_storage_parent_created=True,stages_path=str(OUT/FAMILY/'stages.json'))


def prepare_build():
    require_ready()
    for root in (SOURCE,OUT,TERMINAL):absent(root)
    bodies,docs=actual_components();b,h,full,c=modules()
    if str(Path(sys.executable).resolve())!=docs['original92']['build_python_executable']:
        raise ValueError('actual admitted original92 build interpreter required')
    require(BOUNDED,BOUNDED_SHA);require(DEDUP_OBJECT,DEDUP_OBJECT_SHA);require(PHYSICAL_OBJECT,PHYSICAL_OBJECT_SHA)
    link,linkproof=combined_link_command(docs['original92']['build_commands'][2],PHYSICAL_OBJECT,DEDUP_OBJECT,OUT/'runtime/Dragon')
    files={};aliases={}
    for doc in docs.values():
        for path,sha in doc['files'].items():add_input(files,aliases,path,sha)
        for entry in doc.get('preserved_predecessors',[]):
            for name,sha in entry['inventory']['files'].items():add_input(files,aliases,Path(entry['root'])/name,sha)
    descriptor_inputs(bodies,files,aliases)
    source_roots=[OLD_SOURCE,PHYSICAL_SOURCE,DEDUP_SOURCE,CAPTURE_SOURCE]
    roots=[OLD,PHYSICAL,DEDUP,CAPTURE_OUT]
    namespaces=[]
    for root in [*source_roots,*roots]:
        value=inventory(root);namespaces.append(dict(root=str(root),inventory=value))
        for name,sha in value['files'].items():add_input(files,aliases,root/name,sha)
    for p in [Path(__file__).resolve(),NM,OTOOL,BOUNDED,Path(sys.executable),Path(full.__file__).resolve(),Path(c.__file__).resolve()]:
        add_input(files,aliases,p,digest(p.resolve(strict=True)))
    for token in link:
        p=Path(token)
        if p.is_absolute() and p!=OUT/'runtime/Dragon':add_input(files,aliases,p,digest(p.resolve(strict=True)))
    guard_inputs=h.guard_admission(full)
    for path in guard_inputs:add_input(files,aliases,path,digest(path))
    declared=set().union(*(set(doc['resource_roots']) for doc in docs.values()))|{str(SOURCE),str(OUT),str(TERMINAL)}
    resource_roots=[str(p) for p in b.validate_history_roots(b.history_roots(sorted(declared),ART),ART)]
    resources=resources_for(resource_roots,c.ResourceFailure);before=resources.check()
    if before['artifact_bytes']+RESERVE>=HISTORY_CAP or before['disk_free_bytes']-RESERVE<FREE_FLOOR:
        raise ValueError('fresh combined-link 2GiB reservation refused by unchanged family96/globalfree8')
    # A conservative storage bound is disclosed before any exclusive root is
    # created. It is an INPUT-only link forecast, not a measured runtime result.
    component_json_bytes=len(json.dumps(bodies,allow_nan=False).encode('utf-8'))
    linked_input_bytes=sum(require(Path(t).resolve()).stat().st_size for t in link
        if Path(t).is_absolute() and Path(t)!=OUT/'runtime/Dragon')
    forecast=dict(schema=PREFIX+'_COMPLETE_SOURCE_OUT_STORAGE_FORECAST_V1',
        roots=[str(SOURCE),str(OUT)],actual_component_JSON_bytes=component_json_bytes,
        original_link_input_bytes=linked_input_bytes,
        SOURCE_and_copied_factory_and_metadata_bound=16*component_json_bytes+16*2**20,
        combined_runtime_and_link_transient_bound=2*linked_input_bytes,
        complete_raw_nm_otool_log_and_receipt_reserve=128*2**20,
        total_bound=16*component_json_bytes+16*2**20+2*linked_input_bytes+128*2**20,
        measured_native_RSS=False,mathematical_controls_newly_executed=False)
    if forecast['total_bound']>=RESERVE:raise ValueError('precreation complete SOURCE+OUT forecast exceeds unchanged 2GiB')
    SOURCE.mkdir();OUT.mkdir()
    for name in ('runtime','build','metadata','audit',FAMILY):(OUT/name).mkdir()
    shutil.copy2(require(BOUNDED,BOUNDED_SHA),OUT/'runtime/run_bounded_dragon.py')
    require(OUT/'runtime/run_bounded_dragon.py',BOUNDED_SHA)
    constructor=supervisor_constructor_preflight(full,c,resources)
    shutil.copy2(Path(__file__).resolve(),SOURCE/'combined_runtime_factory.py')
    write_new(SOURCE/'source_admission.json',dict(schema=PREFIX+'_SOURCE_ADMISSION_V1',link_inverse=linkproof,
        actual_components=bodies,no_Fortran_or_observer_source_written=True,
        inherited_mathematical_controls_not_newly_executed=True,physics_operator_changed_by_admitted_SPOASM=True,
        retained_cache_math_unchanged=True,combined_runtime_native_RSS_not_proved=True,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    for name,sha in inventory(SOURCE)['files'].items():files[str(SOURCE/name)]=sha
    files[str(OUT/'runtime/run_bounded_dragon.py')]=BOUNDED_SHA
    sender=OLD/'build/FLU2DR64.o';selector=ART/'axial-material-moment-order-build-20261006/build/FLU.o'
    d=dict(schema=PREFIX+'_DECLARATION_V1',files=files,aliases=aliases,source_inventory=inventory(SOURCE),
        component_namespaces=namespaces,actual_components=bodies,production_link_command=link,link_inverse=linkproof,
        actual_production_objects=list(map(str,[DEDUP_OBJECT,PHYSICAL_OBJECT,sender,selector])),
        original_sender=pin(sender),original_selector=pin(selector),python_command=sys.executable,
        build_python_executable=str(Path(sys.executable).resolve()),actual_local_supervisor_helper=pin(OUT/'runtime/run_bounded_dragon.py'),
        genuine_supervisor_source=pin(Path(full.__file__).resolve()),genuine_parent_class_source=pin(Path(c.__file__).resolve()),
        actual_supervisor_constructor_preflight=constructor,
        resource_roots=resource_roots,resource_scope_contract=b.resource_scope_contract(),resource_scope_policy=HISTORY_POLICY,
        complete_archive_forecast=forecast,
        resources_before=before,total_wall_seconds=TOTAL_WALL,stage_wall_seconds=STAGE_WALL,rss_cap_mib=RSS,
        threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=RESERVE,
        complete_archive_scope_roots=[str(SOURCE),str(OUT)],artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,
        stages=stage_labels(),actual_external_terminal_return_contract=terminal_contract(sys.executable),
        mathematical_controls_newly_executed=False,native_transport_executed=False,production_pipeline_prepared=False,
        original_operator_capture_RSS_scope_not_transferred=True,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    verify_inputs(d)
    if archive_bytes()>=RESERVE:raise ValueError('complete SOURCE+OUT reserve exceeded before declaration')
    write_new(OUT/'declaration.json',d)
    print(json.dumps(dict(declaration=str(OUT/'declaration.json'),declaration_sha256=digest(OUT/'declaration.json')),allow_nan=False),flush=True)


def declaration_admission(expected,require_build_interpreter=True):
    require_ready();nonzero_sha(expected);d=read(require(OUT/'declaration.json',expected))
    if (d['schema']!=PREFIX+'_DECLARATION_V1' or d['total_wall_seconds']!=TOTAL_WALL or d['stage_wall_seconds']!=STAGE_WALL
        or d['rss_cap_mib']!=RSS or d['threads']!=1 or d['numeric_children_at_once']!=1 or d['retries']!=0
        or d['archive_reserve_bytes']!=RESERVE or d['artifact_budget_bytes']!=HISTORY_CAP or d['min_free_bytes']!=FREE_FLOOR
        or d['complete_archive_scope_roots']!=[str(SOURCE),str(OUT)] or d['stages']!=stage_labels()
        or d['actual_external_terminal_return_contract']!=terminal_contract(d['python_command'])
        or d['original_operator_capture_RSS_scope_not_transferred'] is not True
        or any(d[k] is not False for k in ('mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared',
            'combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('original bounded INPUT-only combined-link contract changed')
    if (d['complete_archive_forecast']['roots']!=[str(SOURCE),str(OUT)]
        or d['complete_archive_forecast']['total_bound']>=RESERVE
        or require_build_interpreter and str(Path(sys.executable).resolve())!=d['build_python_executable']):
        raise ValueError('actual admitted interpreter/complete precreation storage bound differs')
    environment(d,require_build_interpreter)
    old=read(OLD/'declaration.json')['build_commands'][2]
    link,proof=combined_link_command(old,PHYSICAL_OBJECT,DEDUP_OBJECT,OUT/'runtime/Dragon')
    if d['production_link_command']!=link or d['link_inverse']!=proof:raise ValueError('complete original-token link inverse changed')
    require(OUT/'runtime/run_bounded_dragon.py',BOUNDED_SHA)
    if expected_supervisor_constructor(d)!=d['actual_supervisor_constructor_preflight']:
        raise ValueError('actual original constructor/local bounded-helper source binding changed')
    if require_build_interpreter:
        _,_,full,c=modules()
        current_ctor=supervisor_constructor_preflight(full,c,resources_for(d['resource_roots'],c.ResourceFailure))
        if current_ctor!=d['actual_supervisor_constructor_preflight']:
            raise ValueError('actual real build constructor/MRO/helper differs')
    if archive_bytes()>=RESERVE:raise ValueError('complete SOURCE+OUT archive cap exceeded')
    return d


def check_watch(stage):
    log=OUT/(stage['label']+'.log');w=read(log.with_suffix('.watchdog.json'))
    actual=w['wall_cap_seconds'];declared=stage['wall_cap_seconds']
    if (w['command']!=stage['command'] or w['returncode']!=0 or w['limit_failure'] is not None
        or w['rss_cap_mib']!=RSS or not 0<=w['sampled_peak_rss_mib']<RSS
        or not 0<actual<=declared<=STAGE_WALL or not 0<=w['elapsed_seconds']<actual
        or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True
        or digest(log)!=stage['log_sha256']):raise ValueError('actual direct-child command/watch/log differs')
    return w


def defined_symbols(text):
    """Only default nm -g definition records; no guessed disassembly."""
    result=[]
    for line in text.splitlines():
        if not line.strip():continue
        match=re.fullmatch(r'\s*([0-9a-fA-F]+)\s+([A-Za-z])\s+(\S+)\s*',line)
        if match:
            if match[2].upper()!='U':result.append(dict(address=match[1],kind=match[2],name=match[3]))
        elif re.fullmatch(r'\s*U\s+\S+\s*',line):continue
        else:raise ValueError('unrecognized actual nm record: '+line[:120])
    return result


def object_nm_sections(text,paths):
    aliases={str(Path(p)):str(Path(p)) for p in paths}
    for p in paths:
        basename=Path(p).name
        if basename in aliases:raise ValueError('ambiguous object basename')
        aliases[basename]=str(Path(p))
    sections={};current=None
    for line in text.splitlines():
        if line.endswith(':') and line[:-1] in aliases:
            current=aliases[line[:-1]]
            if current in sections:raise ValueError('duplicate actual object nm section')
            sections[current]=[]
        elif line.strip():
            if current is None:raise ValueError('object symbol outside actual named section')
            sections[current].append(line)
    if set(sections)!=set(paths):raise ValueError('complete actual object nm sections required')
    return {p:defined_symbols('\n'.join(lines)) for p,lines in sections.items()}


def dependency_sections(text,paths):
    result={};current=None
    for line in text.splitlines():
        if line.endswith(':') and line[:-1] in paths:
            current=line[:-1]
            if current in result:raise ValueError('duplicate actual dependency section')
            result[current]=[]
        elif line.strip():
            if current is None or not line.startswith(('\t',' ')):raise ValueError('unknown actual dependency record')
            result[current].append(line.strip())
    if set(result)!=set(paths) or any(not lines for lines in result.values()):raise ValueError('all complete dependency lists required')
    return result


def binary_audit(d):
    paths=d['actual_production_objects'];objects=object_nm_sections(read_text_log('metadata/objects'),paths)
    executable=defined_symbols(read_text_log('metadata/executable'))
    required={paths[0]:'_spot1p64_',paths[1]:'_spoasm_',paths[2]:'_flu2dr64_',paths[3]:'_flu_'}
    definitions={}
    for path,name in required.items():
        hits=[s for s in objects[path] if s['name']==name and s['kind'].upper()=='T']
        actual=[s for s in executable if s['name']==name and s['kind'].upper()=='T']
        if len(hits)!=1 or len(actual)!=1:raise ValueError('one actual production object/executable definition required')
        definitions[name]=dict(object=pin(path),object_symbol=hits[0],executable_symbol=actual[0])
    for row in executable:
        name=row['name'].lower()
        if any(word in name for word in ('axmat_capture','axmat_rank1_capture','spot1p64_original','spot1p64_dense','original_cache_mod','dense_cache_mod','physical_unit')):
            raise ValueError('observer/unit/reference symbol must not enter combined production runtime')
    targets=list(map(str,[OUT/'runtime/Dragon',OLD/'runtime/Dragon',PHYSICAL/'runtime/Dragon',DEDUP/'runtime/Dragon']))
    deps=dependency_sections(read_text_log('metadata/dependencies'),targets)
    if any(deps[p]!=deps[targets[0]] for p in targets[1:]):raise ValueError('complete old/component/combined dynamic dependency lists differ')
    old=read(OLD/'declaration.json')['build_commands'][2]
    link,proof=combined_link_command(old,PHYSICAL_OBJECT,DEDUP_OBJECT,OUT/'runtime/Dragon')
    if link!=d['production_link_command'] or proof!=d['link_inverse']:raise ValueError('independent complete link inverse differs')
    return dict(status='PASS',raw_metadata={label:pin(OUT/(label+'.log')) for label in stage_labels()[1:4]},
        actual_object_definitions=definitions,actual_runtime=pin(OUT/'runtime/Dragon'),dependencies=deps,
        exact_original92_token_inverse=True,sole_object_changes=['SPOT1P64.o','SPOASM.o'],
        all_other_original_link_inputs_unchanged=True,production_references_and_observers_excluded=True,
        whole_instruction_equivalence_claimed=False,actual_full_FLU_entry_executed=False,
        combined_runtime_native_RSS_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False)


def read_text_log(label):return require(OUT/(label+'.log')).read_text(encoding='utf-8')


def audit_build(expected):
    d=declaration_admission(expected);claim=read(OUT/'execution_claim.json');stages=read(OUT/FAMILY/'stages.json')['stages']
    if (claim['parent_pid']!=os.getppid() or claim['declaration_sha256']!=expected
        or len(stages)!=5 or [s['label'] for s in stages]!=stage_labels()
        or [s['command'] for s in stages]!=stage_commands(d,expected)
        or [s['status'] for s in stages]!=['PASS']*4+['RUNNING']
        or stages[-1]['command']!=[sys.executable,*sys.argv]):raise ValueError('actual supervised final audit child/command required')
    watches=[check_watch(s) for s in stages[:-1]];raw=read(OUT/'raw_metadata_receipt.json')
    expected_raw={str((OUT/(label+'.log')).relative_to(OUT)):digest(OUT/(label+'.log')) for label in stage_labels()[:4]}
    if raw['files']!=expected_raw or raw['before_binary_identity_gates'] is not True:raise ValueError('all complete raw metadata before gates required')
    binary=binary_audit(d);write_new(OUT/'audit/binary_identity.json',binary)
    write_new(OUT/'audit/result.json',dict(classification='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY',
        declaration_sha256=expected,binary_status='PASS',actual_components=d['actual_components'],
        previous_stage_watchdogs=watches,mathematical_controls_newly_executed=False,
        native_transport_executed=False,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    print('AXMAT-COMBINED-RUNTIME-LINK-AUDITED',flush=True)


def run_build(expected):
    require_ready();started=time.monotonic();d=declaration_admission(expected);b,h,full,c=modules()
    resources=resources_for(d['resource_roots'],c.ResourceFailure);resources.check()
    absent(OUT/'execution_claim.json')
    write_new(OUT/'execution_claim.json',dict(parent_pid=os.getpid(),declaration_sha256=expected,started_monotonic=started,retries=0))
    remaining=TOTAL_WALL-(time.monotonic()-started)
    if remaining<=0:raise ValueError('whole link budget exhausted')
    runner=full.OwnRSSSerialExecutor(OUT,remaining,FAMILY,resources)
    result=dict(classification='FAILED_COMBINED_RUNTIME_LINK_NO_RETRY',error=None,native_transport_executed=False,
        mathematical_controls_newly_executed=False,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    try:
        commands=stage_commands(d,expected)
        try:
            for label,command in zip(stage_labels()[:4],commands[:4]):
                environment(d);directory,stem=label.split('/')
                runner.execute(OUT/directory,stem,command,STAGE_WALL)
        finally:
            raw={label+'.log':digest(OUT/(label+'.log')) for label in stage_labels()[:4] if (OUT/(label+'.log')).is_file()}
            write_new(OUT/'raw_metadata_receipt.json',dict(files=raw,before_binary_identity_gates=True,complete_raw_tools_and_link_stdout=True))
        runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL,'AXMAT-COMBINED-RUNTIME-LINK-AUDITED')
        stages=read(OUT/FAMILY/'stages.json')['stages']
        if (len(stages)!=5 or [s['label'] for s in stages]!=stage_labels()
            or [s['command'] for s in stages]!=commands or any(s['status']!='PASS' for s in stages)):raise ValueError('exact five supervised stages must pass once')
        audit=read(OUT/'audit/result.json')
        if (audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS'
            or audit['actual_components']!=d['actual_components']):
            raise ValueError('only actual complete identity audit accepted')
        result.update(classification='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY',watchdogs=[check_watch(s) for s in stages],
            corrected_runtime=pin(OUT/'runtime/Dragon'),fresh_cold_AAA_required=True)
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        try:
            environment(d);size=archive_bytes();snapshot=resources.check();elapsed=time.monotonic()-started
            if size>=RESERVE or elapsed>=TOTAL_WALL:raise ValueError('complete source/out or whole-link budget exceeded')
            result.update(elapsed_seconds=elapsed,archive_bytes_before_closeout=size,resources=snapshot)
        except BaseException as error:
            result.update(classification='FAILED_COMBINED_RUNTIME_LINK_NO_RETRY',error=repr(error),elapsed_seconds=time.monotonic()-started)
            write_new(OUT/'driver_result.json',result);raise
        write_new(OUT/'driver_result.json',result)
    complete=inventory(OUT);write_new(OUT/'seal.json',dict(schema=PREFIX+'_BUILD_SEAL_V1',**complete))
    try:
        snapshot=resources.check();size=archive_bytes();elapsed=time.monotonic()-started
        if size>=RESERVE or elapsed>=TOTAL_WALL:raise ValueError('mandatory complete post-seal tail failed')
        print(json.dumps(dict(result=result,actual_tail_check='PASS',actual_elapsed_seconds=elapsed,
            actual_archive_bytes=size,actual_resources=snapshot),allow_nan=False),flush=True)
    except BaseException as error:
        write_new(OUT/'closeout_failure.json',dict(error=repr(error),complete=False,AAA_accuracy_qualified=False,ABA_admitted=False));raise


def terminal_file(path,sha):
    path=normal(path)
    if path.parent!=TERMINAL:raise ValueError('independent fixed Root terminal file required')
    return require(path,sha)


def external_terminal(d,seal_sha,result,path,sha):
    receipt=terminal_file(path,sha)
    if receipt!=TERMINAL/'terminal_return.json':raise ValueError('Root actual run-build receipt required')
    e=read(receipt);decl_sha=digest(OUT/'declaration.json');source=pin(Path(__file__).resolve())
    command=[d['python_command'],source['path'],'run-build','--sha256',decl_sha]
    if (e['schema']!=TERMINAL_SCHEMA or e['record_producer']!='root' or e['actual_tool_terminal_return_observed'] is not True
        or e['record_written_after_actual_terminal_return'] is not True or type(e['returncode']) is not int or e['returncode']!=0
        or type(e['actual_tool_result']['exit_code']) is not int or e['actual_tool_result']['exit_code']!=0
        or e['command']!=command or e['source']!=source
        or d['files'][source['path']]!=source['sha256'] or e['declaration']!=dict(path=str(OUT/'declaration.json'),sha256=decl_sha)
        or e['build_seal']!=dict(path=str(OUT/'seal.json'),sha256=seal_sha)):raise ValueError('true Root zero/source/declaration/seal chain required')
    stdout=terminal_file(e['full_stdout']['path'],e['full_stdout']['sha256']);stderr=terminal_file(e['full_stderr']['path'],e['full_stderr']['sha256'])
    if len({receipt,stdout,stderr})!=3:raise ValueError('separately retained complete stdout/stderr required')
    body=read(stdout);tail={key:body[key] for key in TAIL_FIELDS}
    if body!=dict(result=result,**tail) or any(e[key]!=tail[key] for key in TAIL_FIELDS):raise ValueError('actual full stdout/sealed result/four tails differ')
    elapsed,size,s=tail['actual_elapsed_seconds'],tail['actual_archive_bytes'],tail['actual_resources']
    if (tail['actual_tail_check']!='PASS' or type(elapsed) not in (int,float) or not math.isfinite(elapsed)
        or not result['elapsed_seconds']<=elapsed<TOTAL_WALL or type(size) is not int or size!=archive_bytes() or not 0<size<RESERVE
        or s['artifact_budget_bytes']!=HISTORY_CAP or s['min_free_bytes']!=FREE_FLOOR
        or s['resource_scope_policy']!=HISTORY_POLICY or s['resource_scope_contract']!=d['resource_scope_contract']
        or s['declared_resource_roots']!=d['resource_roots'] or not set(d['resource_roots']).issubset(s['resource_roots'])
        or not size<=s['artifact_bytes']<=HISTORY_CAP or s['disk_free_bytes']<FREE_FLOOR):raise ValueError('mandatory actual complete budget tail required')
    builder().validate_history_roots(s['resource_roots'],ART)
    return dict(receipt=pin(receipt),full_stdout=pin(stdout),full_stderr=pin(stderr),command=command,schema=TERMINAL_SCHEMA,**tail)


def production_admission(seal_sha,terminal_evidence,terminal_evidence_sha256):
    require_ready();nonzero_sha(seal_sha);nonzero_sha(terminal_evidence_sha256)
    seal=read(require(OUT/'seal.json',seal_sha));actual=inventory(OUT)
    if (seal['schema']!=PREFIX+'_BUILD_SEAL_V1' or actual['directories']!=seal['directories'] or actual['symlinks']!=seal['symlinks']
        or set(actual['files'])!=set(seal['files'])|{'seal.json'} or any(actual['files'][p]!=v for p,v in seal['files'].items())):
        raise ValueError('complete successful raw/watch/runtime/source inventory required')
    declared=digest(OUT/'declaration.json');d=declaration_admission(declared,require_build_interpreter=False)
    result=read(OUT/'driver_result.json');audit=read(OUT/'audit/result.json');stages=read(OUT/FAMILY/'stages.json')['stages']
    if (result['classification']!='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or result['error'] is not None
        or audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS'
        or audit['declaration_sha256']!=declared
        or audit['actual_components']!=d['actual_components'] or len(stages)!=5
        or [s['label'] for s in stages]!=stage_labels() or [s['command'] for s in stages]!=stage_commands(d,declared)
        or any(s['status']!='PASS' for s in stages)
        or any(result[k] is not False or audit[k] is not False for k in ('native_transport_executed',
            'mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('only complete link identity may be admitted as a runtime input')
    watches=[check_watch(s) for s in stages]
    if watches!=result['watchdogs'] or watches[:-1]!=audit['previous_stage_watchdogs']:raise ValueError('all actual watches must agree')
    raw=read(OUT/'raw_metadata_receipt.json')
    expected_raw={label+'.log':digest(OUT/(label+'.log')) for label in stage_labels()[:4]}
    if raw['files']!=expected_raw or raw['before_binary_identity_gates'] is not True:
        raise ValueError('independently fresh complete metadata-before-gates receipt required')
    if binary_audit(d)!=read(OUT/'audit/binary_identity.json'):raise ValueError('independent raw symbol/link audit differs')
    terminal=external_terminal(d,seal_sha,result,terminal_evidence,terminal_evidence_sha256)
    resources_for(d['resource_roots']).check()
    descriptor_files=dict(d['files'])
    def own(path,sha):
        key=str(Path(path));nonzero_sha(sha)
        if key in descriptor_files and descriptor_files[key]!=sha:raise ValueError('true immutable descriptor ownership conflict')
        descriptor_files[key]=sha
    for name,sha in seal['files'].items():own(OUT/name,sha)
    own(OUT/'seal.json',seal_sha)
    for field in ('receipt','full_stdout','full_stderr'):own(terminal[field]['path'],terminal[field]['sha256'])
    return dict(schema=PREFIX+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',admission='COMBINED_RUNTIME_INPUT_ONLY',
        build_root=str(OUT),source_root=str(SOURCE),build_seal_sha256=seal_sha,corrected_runtime=pin(OUT/'runtime/Dragon'),
        compiled_dedup_kernel=pin(DEDUP_OBJECT),compiled_physical_assembly=pin(PHYSICAL_OBJECT),
        actual_local_supervisor_helper=d['actual_local_supervisor_helper'],
        actual_supervisor_constructor_preflight=d['actual_supervisor_constructor_preflight'],
        source_admission=pin(SOURCE/'source_admission.json'),compiled_link_identity=pin(OUT/'audit/binary_identity.json'),
        production_link_command=d['production_link_command'],actual_components=d['actual_components'],
        descriptor_files=descriptor_files,input_aliases=d['aliases'],
        inherited_rank1_cache_admission=d['actual_components']['original92'],inherited_physical_admission=d['actual_components']['physical'],
        inherited_dedup_admission=d['actual_components']['dedup'],
        inherited_rank1_factor_cache_memory_admission=d['actual_components']['dedup']['inherited_rank1_factor_cache_memory_admission'],
        original_operator_capture_dependency=d['actual_components']['capture'],
        future_contract=d['actual_components']['original92']['future_contract'],
        actual_external_terminal_evidence=terminal['receipt'],actual_external_terminal_validation=terminal,
        resource_scope_policy=HISTORY_POLICY,resource_scope_contract=d['resource_scope_contract'],
        actual_resource_class_factory=d['actual_components']['dedup']['actual_resource_class_factory'],
        sole_object_changes=['SPOT1P64.o','SPOASM.o'],all_other_original92_tokens_unchanged=True,
        mathematical_controls_inherited_not_newly_executed=True,physical_self_operator_changed=True,
        retained_cache_mathematics_and_rhs_order_unchanged=True,observer_objects_linked=False,
        future_actual_FLU_observer_required=d['actual_components']['dedup']['future_actual_FLU_observer_required'],
        future_actual_factor_cache_observer_required=d['actual_components']['dedup']['future_actual_factor_cache_observer_required'],
        white_closure_unchanged=True,angle_grid_unchanged=True,radial_arithmetic_unchanged=True,physical_data_unchanged=True,
        collision_self_operator_unchanged=False,original_accuracy_thresholds_changed=False,no_CE_fitting=True,
        original_operator_capture_RSS_scope_not_transferred=True,fresh_combined_runtime_cold_AAA_required=True,
        original_cold_storage_reservation_still_required=True,production_pipeline_prepared=False,
        native_transport_executed=False,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)


if __name__=='__main__':
    require_ready()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare-build','run-build','audit-build','admit'])
    parser.add_argument('--sha256');parser.add_argument('--terminal-evidence');parser.add_argument('--terminal-evidence-sha256')
    a=parser.parse_args()
    if a.action=='prepare-build':prepare_build()
    elif a.action=='run-build':run_build(a.sha256)
    elif a.action=='audit-build':audit_build(a.sha256)
    else:print(json.dumps(production_admission(a.sha256,a.terminal_evidence,a.terminal_evidence_sha256),allow_nan=False),flush=True)

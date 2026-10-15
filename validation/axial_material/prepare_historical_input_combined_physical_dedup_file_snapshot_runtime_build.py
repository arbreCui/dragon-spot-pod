"""Reviewed formal factory: historical PREP INPUT reuse with fresh full phases.

The historical bf469 successful PREP anchors only the unfiltered immutable
seven-key component INPUT body. Its later failed RUN supplies no build or
runtime credit. Every new phase freshly verifies the entire canonical union,
all exhaustive namespaces, original aliases and current source-owned predicates.
Original component admission APIs are not reexecuted by this explicit INPUT
reuse contract. All five original link/metadata/audit stages, actual direct-child
supervision, fresh constructor, new Root PREP and RUN witnesses, successful
output sealing and four complete closeout tails remain mandatory.

The 1800/600-second, 512-MiB, one-thread/one-child/no-retry and SOURCE+OUT 2-GiB
limits remain unchanged, as do complete history 96 GiB and free-space 8 GiB.
This source readiness does not prove actual preparation, successful linking,
native transport RSS, full FLU, new mathematical controls, cold AAA or ABA.
The original cold storage reservation remains mandatory and currently fails.
"""
import argparse
import gc
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

if sys.flags.optimize != 0 or os.environ.get('PYTHONOPTIMIZE'):
    raise ValueError('all original assert predicates require nonoptimized Python')

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
SOURCE = ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-20261007'
OUT = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-20261007'
TERMINAL = ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-20261007'
FAMILY = 'HISTORICAL_INPUT_COMBINED_RUNTIME_LINK'
DRAFT_STATUS = 'READY_REVIEWED_HISTORICAL_PREP_INPUT_REUSE_FORMAL_FACTORY'
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
PREFIX = 'AXMAT_HISTORICAL_INPUT_COMBINED_PHYSICAL_DEDUP_RUNTIME'
TERMINAL_SCHEMA = PREFIX+'_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'

PREP_TERMINAL_SCHEMA = PREFIX+'_ACTUAL_EXTERNAL_PREP_RETURN_V1'
FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_historical_input_combined_physical_dedup_file_snapshot_runtime_build.py'
HISTORICAL_FACTORY = ROOT/'validation/axial_material/prepare_combined_physical_dedup_file_snapshot_runtime_build.py'
HISTORICAL_FACTORY_SHA = 'bf4692a57209ace55e22f85c6e9ffabf80850dcb1b610348e7dc97b74a80040c'
HISTORICAL_DECL = ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
HISTORICAL_DECL_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
HISTORICAL_PREP = ART/'axial-material-qualified-AB-physical-dedup-combined-runtime-build-terminal-20261007/declaration_terminal_return.json'
HISTORICAL_PREP_SHA = '1b2956eafedde4a4fec61cd40c3f55af484678ac82abaf0db2797c05d387a280'
INPUT_SPECS = ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
INPUT_SPECS_SHA = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
INPUT_HELPERS = {
 'graph': (ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph.py','ac3fb3bc6a3d67a685482183ee01c9b0bc0df6f71528a3a895416519db687cf4'),
 'codec': (ROOT/'validation/axial_material/combined_runtime_typed_specs_codec.py','758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69'),
 'current': (ROOT/'validation/axial_material/combined_runtime_current_predicates.py','0e7423bb39c6a6c5c55e2ba12dede62d3d779dd1805342eedc39e6bf40e5c779'),
 'checks': (ROOT/'validation/axial_material/combined_runtime_historical_input_checks.py','86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'),
 'ordinary': (ROOT/'validation/axial_material/combined_runtime_current_ordinary_path_checks.py','47e7f9eb2e7ff89e96c30b91f98a25d37d66d82a029dcfbf4845c8f5968482d5'),
}
BODY_BINDING = dict(path=str(INPUT_SPECS),sha256=INPUT_SPECS_SHA,
    encoding_schema='AXMAT_COMBINED_RUNTIME_LOSSLESS_TYPED_INPUT_METADATA_ENCODING_V1',
    pointer='/metadata/historical_actual_components',whole_seven_key_body_retained=True,
    original_component_API_execution_claimed=False,historical_FAILED_RUN_promoted=False)
GRAPH_NAME = 'input_graph.json'
PREP_NAME = 'declaration_terminal_return.json'



def nonzero_sha(value):
    if not isinstance(value,str) or re.fullmatch('[0-9a-f]{64}',value) is None or value=='0'*64:
        raise ValueError('actual nonplaceholder SHA256 required')
    return value


def require_ready():
    if sys.flags.optimize != 0 or os.environ.get('PYTHONOPTIMIZE'):
        raise ValueError('nonoptimized Python required before project input read')
    if DRAFT_STATUS != 'READY_REVIEWED_HISTORICAL_PREP_INPUT_REUSE_FORMAL_FACTORY':
        raise ValueError('UNREADY: source-only new contract, no new business Root witness or constructor')
    if Path(__file__).absolute()!=FORMAL_FACTORY:
        raise ValueError('TMP draft cannot perform a business action')
    if any(os.environ.get(key)!='1' for key in THREAD_KEYS):
        raise ValueError('single-thread environment required before project import')
    nonzero_sha(CAPTURE_SEAL_SHA);nonzero_sha(CAPTURE_TERMINAL_SHA)


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
    """Historical whole INPUT return, not any original API invocation now."""
    require_ready();g=input_modules()['graph']
    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA)
    metadata=encoded['metadata'];bodies=metadata['historical_actual_components']
    if metadata['declaration']!=dict(path=str(HISTORICAL_DECL),sha256=HISTORICAL_DECL_SHA):
        raise ValueError('exact historical component body owner differs')
    records={row['label']:row for row in metadata['reached_component_records']}
    docs={name:g.strict_json(records[name]['declaration']['path'],records[name]['declaration']['sha256'])
          for name in ('original92','physical','dedup','capture')}
    identity_path=PHYSICAL/'runtime/build_identity.json'
    physical_seal=g.strict_json(records['physical']['seal']['path'],records['physical']['seal']['sha256'])
    identity=g.strict_json(str(identity_path),physical_seal['files']['runtime/build_identity.json'])
    expected=component_contract(bodies['original92'],bodies['physical'],bodies['dedup'],bodies['capture'],
        identity,docs['original92'],docs['physical'],docs['dedup'])
    if bodies!=expected:raise ValueError('entire historical seven-key body differs; no field filtering')
    del encoded,metadata,records,physical_seal,expected;gc.collect()
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


def verify_inputs(d,phase='input_reuse',require_build_interpreter=True):
    """New complete fresh union contract; never label this a callee API call."""
    return complete_input_phase(d,phase,require_build_interpreter=require_build_interpreter)


def environment(d,require_build_interpreter=True,phase='environment'):
    require_ready()
    if d['historical_whole_component_body']!=BODY_BINDING:
        raise ValueError('unfiltered historical INPUT-only component body binding changed')
    if d['resource_scope_contract']!=builder().resource_scope_contract() or d['resource_scope_policy']!=HISTORY_POLICY:
        raise ValueError('original family96/globalfree8 contract differs')
    observed=verify_inputs(d,phase,require_build_interpreter)
    resources_for(d['resource_roots']).check()
    return observed


def stage_labels():return ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']


def stage_commands(d,expected):
    obj=d['actual_production_objects']
    prep=nonzero_sha(d['actual_prep_terminal_sha256'])
    return [d['production_link_command'],[str(NM),'-g',*obj],
        [str(NM),'-g',str(OUT/'runtime/Dragon')],
        [str(OTOOL),'-L',str(OUT/'runtime/Dragon'),str(OLD/'runtime/Dragon'),str(PHYSICAL/'runtime/Dragon'),str(DEDUP/'runtime/Dragon')],
        [d['python_command'],str(Path(__file__).resolve()),'audit-build','--sha256',expected,'--prep-sha256',prep]]


def terminal_contract(python):
    return dict(schema=TERMINAL_SCHEMA,root=str(TERMINAL),receipt=str(TERMINAL/'terminal_return.json'),
        python=python,action='run-build',command=[python,str(FORMAL_FACTORY),'run-build','--sha256','<ACTUAL_DECLARATION_SHA256>',
            '--prep-sha256','<ACTUAL_ROOT_PREP_TERMINAL_SHA256>'],actual_prepare_terminal_evidence_required=True,
        record_producer='root',actual_tool_exit_zero_required=True,
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
    helpers=input_modules();g=helpers['graph'];codec=helpers['codec']
    historic=g.strict_json(str(HISTORICAL_DECL),HISTORICAL_DECL_SHA)
    original_prep_input(g)
    b,h,full,c=modules()
    if str(Path(sys.executable).resolve())!=historic['build_python_executable']:
        raise ValueError('original build interpreter required')
    original_aliases=historic['aliases'];historical_roots=historic['resource_roots']
    del historic;gc.collect()
    declared=set(historical_roots)|{str(SOURCE),str(OUT),str(TERMINAL)}
    roots=[str(p)for p in b.validate_history_roots(b.history_roots(sorted(declared),ART),ART)]
    resources=resources_for(roots,c.ResourceFailure);before=resources.check()
    if before['artifact_bytes']+RESERVE>=HISTORY_CAP or before['disk_free_bytes']-RESERVE<FREE_FLOOR:
        raise ValueError('unchanged family96/free8 refuses new 2GiB link reservation')
    link,linkproof=combined_link_command(read(OLD/'declaration.json')['build_commands'][2],PHYSICAL_OBJECT,DEDUP_OBJECT,OUT/'runtime/Dragon')
    input_metadata_bytes=require(INPUT_SPECS,INPUT_SPECS_SHA).stat().st_size
    linked_input_bytes=sum(require(Path(t).resolve()).stat().st_size for t in link
        if Path(t).is_absolute()and Path(t)!=OUT/'runtime/Dragon')
    forecast=dict(schema=PREFIX+'_COMPLETE_SOURCE_OUT_STORAGE_FORECAST_V1',roots=[str(SOURCE),str(OUT)],
        encoded_complete_input_specs_bytes=input_metadata_bytes,
        copied_SOURCE_metadata_bound=16*input_metadata_bytes+32*2**20,
        full_graph_and_creation_trace_bound=256*2**20,
        combined_runtime_and_link_transient_bound=2*linked_input_bytes,
        complete_raw_tools_and_closeout_bound=128*2**20,
        total_bound=16*input_metadata_bytes+32*2**20+256*2**20+2*linked_input_bytes+128*2**20,
        original_cold_reservation_bytes=20971764748,cold_reservation_reduced=False,
        measured_native_RSS=False,mathematical_controls_newly_executed=False)
    if forecast['total_bound']>=RESERVE:raise ValueError('SOURCE+OUT forecast exceeds unchanged 2GiB')
    SOURCE.mkdir();OUT.mkdir()
    for name in ('runtime','build','metadata','audit',FAMILY):(OUT/name).mkdir()
    (SOURCE/'runtime').mkdir()
    shutil.copy2(require(BOUNDED,BOUNDED_SHA),OUT/'runtime/run_bounded_dragon.py')
    constructor=supervisor_constructor_preflight(full,c,resources)
    shutil.copy2(require(Path(__file__).resolve()),SOURCE/'historical_input_combined_runtime_factory.py')
    for name,(path,sha)in INPUT_HELPERS.items():shutil.copy2(require(path,sha),SOURCE/'runtime'/(name+'.py'))
    shutil.copy2(require(INPUT_SPECS,INPUT_SPECS_SHA),SOURCE/'input_specs.json')
    write_new(SOURCE/'source_admission.json',dict(schema=PREFIX+'_SOURCE_ADMISSION_V1',link_inverse=linkproof,
        historical_whole_component_body=BODY_BINDING,historical_PREP=dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA),
        historical_failed_combined_RUN_grants_success=False,original_component_APIs_executed_now=False,
        no_Fortran_or_observer_source_written=True,inherited_mathematical_controls_not_newly_executed=True,
        physics_operator_changed_by_admitted_SPOASM=True,retained_cache_math_unchanged=True,
        combined_runtime_native_RSS_not_proved=True,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    source_inventory=inventory(SOURCE)
    extra={str(Path(__file__).resolve()):digest(Path(__file__).resolve()),str(OUT/'runtime/run_bounded_dragon.py'):BOUNDED_SHA,
           **{str(path):sha for path,sha in INPUT_HELPERS.values()},**{str(SOURCE/name):sha for name,sha in source_inventory['files'].items()}}
    graph_binding,files,complete_aliases=create_complete_input_graph(helpers,source_inventory,extra)
    sender=OLD/'build/FLU2DR64.o';selector=ART/'axial-material-moment-order-build-20261006/build/FLU.o'
    d=dict(schema=PREFIX+'_DECLARATION_V1',files=files,aliases=original_aliases,complete_input_aliases=complete_aliases,source_inventory=source_inventory,
        historical_whole_component_body=BODY_BINDING,historical_PREP=dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA),
        input_graph=graph_binding,input_graph_source_root_inventory_is_exhaustive=True,
        original_component_APIs_executed_now=False,historical_failed_combined_RUN_promoted=False,
        production_link_command=link,link_inverse=linkproof,actual_production_objects=list(map(str,[DEDUP_OBJECT,PHYSICAL_OBJECT,sender,selector])),
        original_sender=pin(sender),original_selector=pin(selector),python_command=sys.executable,
        build_python_executable=str(Path(sys.executable).resolve()),actual_local_supervisor_helper=pin(OUT/'runtime/run_bounded_dragon.py'),
        genuine_supervisor_source=pin(Path(full.__file__).resolve()),genuine_parent_class_source=pin(Path(c.__file__).resolve()),
        actual_supervisor_constructor_preflight=constructor,resource_roots=roots,resource_scope_contract=b.resource_scope_contract(),resource_scope_policy=HISTORY_POLICY,
        complete_archive_forecast=forecast,resources_before=before,total_wall_seconds=TOTAL_WALL,stage_wall_seconds=STAGE_WALL,rss_cap_mib=RSS,
        threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=RESERVE,
        complete_archive_scope_roots=[str(SOURCE),str(OUT)],artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,
        stages=stage_labels(),actual_external_terminal_return_contract=terminal_contract(sys.executable),
        actual_external_prepare_terminal_contract=prepare_terminal_contract(sys.executable),
        mathematical_controls_newly_executed=False,native_transport_executed=False,production_pipeline_prepared=False,
        original_operator_capture_RSS_scope_not_transferred=True,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    if archive_bytes()>=RESERVE:raise ValueError('complete SOURCE+OUT reserve exceeded')
    write_new(OUT/'declaration.json',d)
    print(json.dumps(dict(declaration=str(OUT/'declaration.json'),declaration_sha256=digest(OUT/'declaration.json')),allow_nan=False),flush=True)


def declaration_admission(expected,require_build_interpreter=True,prep_sha256=None):
    require_ready();nonzero_sha(expected);d=read(require(OUT/'declaration.json',expected))
    if (d['schema']!=PREFIX+'_DECLARATION_V1' or d['total_wall_seconds']!=TOTAL_WALL or d['stage_wall_seconds']!=STAGE_WALL
        or d['rss_cap_mib']!=RSS or d['threads']!=1 or d['numeric_children_at_once']!=1 or d['retries']!=0
        or d['archive_reserve_bytes']!=RESERVE or d['artifact_budget_bytes']!=HISTORY_CAP or d['min_free_bytes']!=FREE_FLOOR
        or d['complete_archive_scope_roots']!=[str(SOURCE),str(OUT)] or d['stages']!=stage_labels()
        or d['actual_external_terminal_return_contract']!=terminal_contract(d['python_command'])
        or d['actual_external_prepare_terminal_contract']!=prepare_terminal_contract(d['python_command'])
        or d['historical_whole_component_body']!=BODY_BINDING or d['historical_failed_combined_RUN_promoted']is not False
        or d['original_component_APIs_executed_now']is not False
        or any(d[k]is not False for k in ('mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared',
            'combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('complete original bounded new INPUT-only contract changed')
    if d['complete_archive_forecast']['total_bound']>=RESERVE:raise ValueError('unchanged reserve exceeded')
    proof=prepare_terminal_admission(d,expected,nonzero_sha(prep_sha256))
    environment(d,require_build_interpreter,phase='declaration_admission')
    link,inverse=combined_link_command(read(OLD/'declaration.json')['build_commands'][2],PHYSICAL_OBJECT,DEDUP_OBJECT,OUT/'runtime/Dragon')
    if d['production_link_command']!=link or d['link_inverse']!=inverse:raise ValueError('original-token link differs')
    if expected_supervisor_constructor(d)!=d['actual_supervisor_constructor_preflight']:raise ValueError('constructor source/input differs')
    if require_build_interpreter:
        _,_,full,c=modules()
        if supervisor_constructor_preflight(full,c,resources_for(d['resource_roots'],c.ResourceFailure))!=d['actual_supervisor_constructor_preflight']:
            raise ValueError('genuine fresh new constructor differs')
    if archive_bytes()>=RESERVE:raise ValueError('complete SOURCE+OUT cap exceeded')
    # Runtime local field only; never write or replace immutable declaration.
    d['actual_prep_terminal_sha256']=proof['receipt']['sha256']
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


def audit_build(expected,prep_sha256):
    d=declaration_admission(expected,prep_sha256=prep_sha256);claim=read(OUT/'execution_claim.json');stages=read(OUT/FAMILY/'stages.json')['stages']
    if (claim['parent_pid']!=os.getppid() or claim['declaration_sha256']!=expected or claim['prep_terminal_evidence']!=dict(path=str(TERMINAL/PREP_NAME),sha256=prep_sha256)
        or len(stages)!=5 or [s['label'] for s in stages]!=stage_labels()
        or [s['command'] for s in stages]!=stage_commands(d,expected)
        or [s['status'] for s in stages]!=['PASS']*4+['RUNNING']
        or stages[-1]['command']!=[sys.executable,*sys.argv]):raise ValueError('actual supervised final audit child/command required')
    watches=[check_watch(s) for s in stages[:-1]];raw=read(OUT/'raw_metadata_receipt.json')
    expected_raw={str((OUT/(label+'.log')).relative_to(OUT)):digest(OUT/(label+'.log')) for label in stage_labels()[:4]}
    if raw['files']!=expected_raw or raw['before_binary_identity_gates'] is not True:raise ValueError('all complete raw metadata before gates required')
    binary=binary_audit(d);write_new(OUT/'audit/binary_identity.json',binary)
    write_new(OUT/'audit/result.json',dict(classification='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY',
        declaration_sha256=expected,binary_status='PASS',historical_whole_component_body=d['historical_whole_component_body'],
        previous_stage_watchdogs=watches,mathematical_controls_newly_executed=False,
        native_transport_executed=False,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    print('AXMAT-COMBINED-RUNTIME-LINK-AUDITED',flush=True)


def run_build(expected,prep_sha256):
    require_ready();started=time.monotonic();d=declaration_admission(expected,prep_sha256=prep_sha256);b,h,full,c=modules()
    resources=resources_for(d['resource_roots'],c.ResourceFailure);resources.check()
    absent(OUT/'execution_claim.json')
    write_new(OUT/'execution_claim.json',dict(parent_pid=os.getpid(),declaration_sha256=expected,started_monotonic=started,retries=0,prep_terminal_evidence=dict(path=str(TERMINAL/PREP_NAME),sha256=prep_sha256)))
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
                environment(d,phase='before_'+label.replace('/','_'));directory,stem=label.split('/')
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
            or audit['historical_whole_component_body']!=d['historical_whole_component_body']):
            raise ValueError('only actual complete identity audit accepted')
        result.update(classification='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY',watchdogs=[check_watch(s) for s in stages],
            corrected_runtime=pin(OUT/'runtime/Dragon'),fresh_cold_AAA_required=True)
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        try:
            environment(d,phase='run_finally');size=archive_bytes();snapshot=resources.check();elapsed=time.monotonic()-started
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
    command=[d['python_command'],source['path'],'run-build','--sha256',decl_sha,'--prep-sha256',d['actual_prep_terminal_sha256']]
    if (e['schema']!=TERMINAL_SCHEMA or e['record_producer']!='root' or e['actual_tool_terminal_return_observed'] is not True
        or e['record_written_after_actual_terminal_return'] is not True or type(e['returncode']) is not int or e['returncode']!=0
        or type(e['actual_tool_result']['exit_code']) is not int or e['actual_tool_result']['exit_code']!=0
        or e['command']!=command or e['source']!=source
        or d['files'][source['path']]!=source['sha256'] or e['declaration']!=dict(path=str(OUT/'declaration.json'),sha256=decl_sha)
        or e['prep_terminal_evidence']!=dict(path=str(TERMINAL/PREP_NAME),sha256=d['actual_prep_terminal_sha256'])
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
    declared=digest(OUT/'declaration.json')
    raw_terminal=read(terminal_file(terminal_evidence,terminal_evidence_sha256))
    prep=raw_terminal['prep_terminal_evidence']
    if prep['path']!=str(TERMINAL/PREP_NAME):raise ValueError('new Root PREP witness missing')
    d=declaration_admission(declared,require_build_interpreter=False,prep_sha256=nonzero_sha(prep['sha256']))
    result=read(OUT/'driver_result.json');audit=read(OUT/'audit/result.json');stages=read(OUT/FAMILY/'stages.json')['stages']
    if (result['classification']!='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or result['error'] is not None
        or audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS'
        or audit['declaration_sha256']!=declared
        or audit['historical_whole_component_body']!=d['historical_whole_component_body'] or len(stages)!=5
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
    own(d['input_graph']['path'],d['input_graph']['sha256'])
    prep=prepare_terminal_admission(d,declared,d['actual_prep_terminal_sha256'])
    for field in ('receipt','source_inventory','full_stdout','full_stderr'):own(prep[field]['path'],prep[field]['sha256'])
    # The full seven-key body is materialized only AFTER full graph verification
    # and its large temporary maps have been released. No original API runs.
    bodies,_=actual_components()
    return dict(schema=PREFIX+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',admission='COMBINED_RUNTIME_INPUT_ONLY',
        build_root=str(OUT),source_root=str(SOURCE),build_seal_sha256=seal_sha,corrected_runtime=pin(OUT/'runtime/Dragon'),
        compiled_dedup_kernel=pin(DEDUP_OBJECT),compiled_physical_assembly=pin(PHYSICAL_OBJECT),
        actual_local_supervisor_helper=d['actual_local_supervisor_helper'],
        actual_supervisor_constructor_preflight=d['actual_supervisor_constructor_preflight'],
        source_admission=pin(SOURCE/'source_admission.json'),compiled_link_identity=pin(OUT/'audit/binary_identity.json'),
        production_link_command=d['production_link_command'],actual_components=bodies,
        component_INPUT_semantics='HISTORICAL_PREP_REUSE_WITH_COMPLETE_FRESH_PHASES_NOT_API_REEXECUTION',
        original_component_APIs_executed_now=False,historical_whole_component_body=BODY_BINDING,
        actual_prepare_terminal_evidence=dict(path=str(TERMINAL/PREP_NAME),sha256=d['actual_prep_terminal_sha256']),
        descriptor_files=descriptor_files,input_aliases=d['complete_input_aliases'],historical_input_graph=d['input_graph'],
        original_two_literal_aliases=d['aliases'],complete_literal_owner_edges_preserved_by_graph=True,
        inherited_rank1_cache_admission=bodies['original92'],inherited_physical_admission=bodies['physical'],
        inherited_dedup_admission=bodies['dedup'],
        inherited_rank1_factor_cache_memory_admission=bodies['dedup']['inherited_rank1_factor_cache_memory_admission'],
        original_operator_capture_dependency=bodies['capture'],
        future_contract=bodies['original92']['future_contract'],
        actual_external_terminal_evidence=terminal['receipt'],actual_external_terminal_validation=terminal,
        resource_scope_policy=HISTORY_POLICY,resource_scope_contract=d['resource_scope_contract'],
        actual_resource_class_factory=bodies['dedup']['actual_resource_class_factory'],
        sole_object_changes=['SPOT1P64.o','SPOASM.o'],all_other_original92_tokens_unchanged=True,
        mathematical_controls_inherited_not_newly_executed=True,physical_self_operator_changed=True,
        retained_cache_mathematics_and_rhs_order_unchanged=True,observer_objects_linked=False,
        future_actual_FLU_observer_required=bodies['dedup']['future_actual_FLU_observer_required'],
        future_actual_factor_cache_observer_required=bodies['dedup']['future_actual_factor_cache_observer_required'],
        white_closure_unchanged=True,angle_grid_unchanged=True,radial_arithmetic_unchanged=True,physical_data_unchanged=True,
        collision_self_operator_unchanged=False,original_accuracy_thresholds_changed=False,no_CE_fitting=True,
        original_operator_capture_RSS_scope_not_transferred=True,fresh_combined_runtime_cold_AAA_required=True,
        original_cold_storage_reservation_still_required=True,production_pipeline_prepared=False,
        native_transport_executed=False,combined_runtime_native_RSS_proved=False,
        actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)



def input_modules():
    require_ready()
    return {name:load(path,sha,'historical_reuse_actual_'+name)for name,(path,sha)in INPUT_HELPERS.items()}


def merge_expected(target,values):
    for path,sha in values.items():
        nonzero_sha(sha)
        if path in target and target[path]!=sha:raise ValueError('conflicting original expected byte owner')
        target[path]=sha


def graph_input_bindings(g,graph):
    """Complete expected canonical union, retaining every literal owner in graph.

    This reads metadata only. It must follow this phase's actual full fresh
    graph verification or the actual full creation phase. Expected digests come
    from the original typed owners and exhaustive namespace members; observed
    digests never grant an unowned historical input a new PASS predicate.
    """
    table=graph['requirements'];g._validate_requirement_table(table)
    paths=table['paths'];literal_to_canonical={}
    for row in table['rows']:
        literal,canonical=paths[row[0]],paths[row[1]]
        old=literal_to_canonical.get(literal)
        if old is not None and old!=canonical:raise ValueError('same literal has conflicting canonical edges')
        literal_to_canonical[literal]=canonical
    files={};owners=graph['owners']
    for path_index,sha_index in owners['expected_file_pins']:
        merge_expected(files,{literal_to_canonical[paths[path_index]]:owners['expected_sha256s'][sha_index]})
    for namespace in graph['namespaces']:
        for relative,sha in namespace['files'].items():
            merge_expected(files,{literal_to_canonical[os.path.join(namespace['root'],relative)]:sha})
        for relative,link in namespace['symlinks'].items():
            if link['kind']=='file'and 'sha256'in link:
                merge_expected(files,{literal_to_canonical[os.path.join(namespace['root'],relative)]:link['sha256']})
    actual={row['path']:row['sha256']for row in graph['canonical_files']}
    if len(actual)!=len(graph['canonical_files'])or files!=actual:
        raise ValueError('complete original expected canonical SHA union differs from just-fresh pins')
    aliases={row['path']:{key:value for key,value in row.items()if key!='path'}for row in graph['aliases']}
    if len(aliases)!=len(graph['aliases']):raise ValueError('duplicate literal alias bindings')
    return files,aliases


def original_prep_input(g):
    e=g.strict_json(str(HISTORICAL_PREP),HISTORICAL_PREP_SHA)
    if (e['record_producer']!='root' or e['actual_tool_terminal_return_observed']is not True
        or e['record_written_after_actual_terminal_return']is not True
        or type(e['returncode'])is not int or e['returncode']!=0
        or type(e['actual_tool_result']['exit_code'])is not int or e['actual_tool_result']['exit_code']!=0
        or e['source']!=dict(path=str(HISTORICAL_FACTORY),sha256=HISTORICAL_FACTORY_SHA)
        or e['declaration']!=dict(path=str(HISTORICAL_DECL),sha256=HISTORICAL_DECL_SHA)
        or e['successful_declaration_input_observed']is not True
        or e['successful_combined_link_completion_observed']is not False
        or e['production_admission_observed']is not False
        or e['schema']!='AXMAT_COMBINED_PHYSICAL_DEDUP_RUNTIME_ACTUAL_EXTERNAL_DECLARATION_RETURN_V1'
        or e['command']!=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(HISTORICAL_FACTORY),'prepare-build']
        or e['build_seal']is not None
        or any(e[key]is not False for key in ('scientific_qualification','native_transport_executed',
            'mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed',
            'AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('historical PREP is INPUT-only; failed later RUN cannot provide credit')
    stdout=g.strict_json(e['full_stdout']['path'],e['full_stdout']['sha256'])
    if stdout!=dict(declaration=str(HISTORICAL_DECL),declaration_sha256=HISTORICAL_DECL_SHA):
        raise ValueError('historical complete PREP stdout differs')
    if g.strict_pin(e['full_stderr']['path'],e['full_stderr']['sha256'])['size_bytes']!=0:
        raise ValueError('successful historical PREP stderr not empty')
    return dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA,scope='IMMUTABLE_INPUT_ONLY_NO_CURRENT_API_OR_RUN_CREDIT')


def minimal_live_specs(encoded):
    return {key:encoded['metadata'][key]for key in ('reached_component_records','independent_directory_owners','remaining_source_owned_requirements','aliases')}


def current_input_predicates(helpers,specs,require_build_interpreter):
    provider=helpers['current'].actual_module(HISTORICAL_FACTORY,HISTORICAL_FACTORY_SHA,'historical_reuse_actual_current_provider')
    return dict(ordinary=helpers['ordinary'].check_original_ordinary_paths(helpers['graph'],provider),
        live=helpers['current'].check_current_predicate_subset(helpers['graph'],specs,provider,require_build_interpreter=require_build_interpreter),
        members=helpers['checks'].check_member_and_directory_predicates(helpers['graph'],specs,{}))


def create_complete_input_graph(helpers,source_inventory,extra):
    g=helpers['graph'];codec=helpers['codec'];checks=helpers['checks']
    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);expanded=codec.unpack_specs(encoded);del encoded;gc.collect()
    owners=g._owners(expanded['owners']+[dict(owner='NEW SOURCE-owned historical INPUT reuse implementation',category='code_environment',expected_files=extra)])
    aliases=checks.bind_aliases(g,expanded,owners);namespaces=checks.bind_namespaces(g,expanded,aliases)
    namespaces.append(g.explicit_sealed_namespace(str(SOURCE),source_inventory['files'],{},
        owner=str(SOURCE)+'#new_exhaustive_source',category='source_namespace',directories=source_inventory['directories']))
    before=current_input_predicates(helpers,expanded,True)
    with g.ReadOpenAudit()as audit:
        requirements,actual,new_pins,fresh=g._phase(owners,namespaces,aliases,{},json_input=dict(path=str(INPUT_SPECS),sha256=INPUT_SPECS_SHA))
    if new_pins or codec.pack_specs(expanded)!=fresh['parsed']:raise ValueError('whole INPUT codec/byte identity differs')
    lengths=checks.check_failed_lengths_and_owned_negative_bytes(g,expanded,aliases,actual)
    trace=audit.snapshot();current_input_predicates(helpers,expanded,True)
    write_new(OUT/'input_creation_python_open_trace.json',trace)
    # Release all expanded duplicate owner/ns maps, while normalized full owners,
    # full namespaces and complete actual trace remain. No edge is dropped.
    del expanded['owners'],expanded['namespace_specs'];del requirements,actual,new_pins,fresh,audit;gc.collect()
    graph=g.create_graph(typed_snapshot=dict(semantics='HISTORICAL_PREP_INPUT_ONLY_REUSE_NO_API_REEXECUTION',
        historical_whole_component_body=BODY_BINDING,historical_PREP=dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA),
        failed_historical_combined_RUN_promoted=False,original_component_APIs_executed_now=False),
        owners=owners,namespaces=namespaces,aliases=aliases.values(),read_trace=trace)
    if graph['consumer_scope']is not None:raise ValueError('whole INPUT closure cannot use consumer scope')
    pins={row['path']:row for row in graph['canonical_files']}
    if checks.check_failed_lengths_and_owned_negative_bytes(g,expanded,aliases,pins)!=lengths:
        raise ValueError('just-fresh failed sizes differ across creation phases')
    current_input_predicates(helpers,expanded,True)
    # Graph lives in OUT and is not included in its own SOURCE namespace or byte
    # owners. The declaration pins its exact bytes without a self-hash cycle.
    with normal(OUT/GRAPH_NAME,missing=True).open('x')as f:
        json.dump(graph,f,separators=(',',':'),allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    files,complete_aliases=graph_input_bindings(g,graph)
    binding=dict(path=str(OUT/GRAPH_NAME),sha256=digest(OUT/GRAPH_NAME),content_sha256=graph['content_sha256'],scope='COMPLETE_HISTORICAL_INPUT_ONLY')
    return binding,files,complete_aliases


def complete_input_phase(d,phase,require_build_interpreter):
    helpers=input_modules();g=helpers['graph'];checks=helpers['checks']
    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded;gc.collect()
    original_aliases={row['path']:row['binding']for row in specs['aliases']
        if row['expected_metadata']==dict(path=str(HISTORICAL_DECL),sha256=HISTORICAL_DECL_SHA)}
    if len(original_aliases)!=2 or d['aliases']!=original_aliases:
        raise ValueError('complete original two literal alias obligations differ')
    # New implementation/copy endpoints have ordinary path semantics. The old
    # 16f weak-alias inputs keep their original separate source-owned rights.
    current_new_owned_paths(d)
    before=current_input_predicates(helpers,specs,require_build_interpreter)
    with g.ReadOpenAudit()as audit:
        verified=g.verify_graph(d['input_graph']['path'],expected_sha256=d['input_graph']['sha256'],phase=phase)
    if verified['consumer_scope']is not None or verified['graph_content_sha256']!=d['input_graph']['content_sha256']:
        raise ValueError('whole immutable INPUT graph identity changed')
    trace=audit.snapshot();graph_path=d['input_graph']['path']
    regular=[x for x in trace['records']if x['kind']=='path'and x['path']!=graph_path]
    paths={row['path']for row in regular}
    graph_reads=[row for row in trace['records']if row['kind']=='path'and row['path']==graph_path]
    if (len(regular)!=len(paths)or len(regular)!=verified['canonical_files_read']
        or any(x['attempt_count']!=1 for x in regular)
        or len(graph_reads)!=1 or graph_reads[0]['attempt_count']!=1):
        raise ValueError('every canonical input and the external graph must be freshly opened once')
    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()
    after=current_input_predicates(helpers,specs,require_build_interpreter)
    current_new_owned_paths(d)
    graph=g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])
    expected_snapshot=dict(semantics='HISTORICAL_PREP_INPUT_ONLY_REUSE_NO_API_REEXECUTION',
        historical_whole_component_body=BODY_BINDING,historical_PREP=dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA),
        failed_historical_combined_RUN_promoted=False,original_component_APIs_executed_now=False)
    if graph['typed_snapshot']!=expected_snapshot:
        raise ValueError('complete historical INPUT-only snapshot changed')
    files,complete_aliases=graph_input_bindings(g,graph)
    if d['files']!=files or d['complete_input_aliases']!=complete_aliases or paths!=set(files):
        raise ValueError('declaration full canonical SHA/alias union or actual path opens differ')
    pins={row['path']:row for row in graph['canonical_files']}
    lengths=checks.check_failed_lengths_and_owned_negative_bytes(g,specs,g._alias_map(graph['aliases']),pins)
    # No full historical body or expanded complete graph survives this helper.
    del graph,pins,specs,files,complete_aliases,paths;gc.collect()
    return dict(phase=phase,canonical_files=verified['canonical_files_read'],bytes=verified['actual_bytes_read'],
        logical_edges=verified['logical_owner_requirements'],namespaces=verified['exhaustive_namespaces_checked'],
        trace_content_sha256=trace_digest,current_before=before,current_after=after,original_failed_lengths=lengths,
        historical_INPUT_only=True,original_component_APIs_executed_now=False,new_runtime_or_science_credit=False)


def current_new_owned_paths(d):
    normal(SOURCE);normal(OUT)
    files=[str(Path(__file__).absolute()),str(OUT/'runtime/run_bounded_dragon.py'),
        str(INPUT_SPECS),*[str(path)for path,sha in INPUT_HELPERS.values()],
        *[str(SOURCE/name)for name in d['source_inventory']['files']]]
    for path in files:
        if not normal(path).is_file()or path not in d['files']:
            raise ValueError('new source-owned ordinary endpoint differs')
    return dict(ordinary_new_source_owned_endpoints=len(files),byteverification_scope='COMPLETE_FRESH_GRAPH_PHASE')


def prepare_terminal_contract(python):
    return dict(schema=PREP_TERMINAL_SCHEMA,root=str(TERMINAL),receipt=str(TERMINAL/PREP_NAME),
        command=[python,str(FORMAL_FACTORY),'prepare-build'],record_producer='root',
        actual_tool_exit0_required=True,full_stdout_required=True,full_stderr_required=True,
        observed_after_actual_return_required=True,source_inventory_required=True,
        complete_whole_historical_body=BODY_BINDING,input_only=True,
        false_fields=['successful_new_runtime_build_observed','original_component_APIs_executed_now',
            'native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved',
            'actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'])


def prepare_terminal_admission(d,declared,sha):
    e=read(terminal_file(TERMINAL/PREP_NAME,sha));source=pin(Path(__file__).resolve())
    if (e['schema']!=PREP_TERMINAL_SCHEMA or e['record_producer']!='root'
        or e['successful_declaration_input_observed']is not True
        or e['actual_tool_terminal_return_observed']is not True or e['record_written_after_actual_terminal_return']is not True
        or type(e['returncode'])is not int or e['returncode']!=0
        or type(e['actual_tool_result']['exit_code'])is not int or e['actual_tool_result']['exit_code']!=0
        or e['source']!=source or e['command']!=[d['python_command'],source['path'],'prepare-build']
        or e['declaration']!=dict(path=str(OUT/'declaration.json'),sha256=declared)
        or e['input_graph']!=d['input_graph']or e['historical_whole_component_body']!=BODY_BINDING
        or e['historical_PREP']!=dict(path=str(HISTORICAL_PREP),sha256=HISTORICAL_PREP_SHA)
        or e['successful_new_runtime_build_observed']is not False
        or any(e[key]is not False for key in ('original_component_APIs_executed_now','native_transport_executed',
            'mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed',
            'AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('true Root new declaration exit0 with INPUT-only historical body required')
    source_inventory_pin=e['source_inventory'];snapshot=read(terminal_file(source_inventory_pin['path'],source_inventory_pin['sha256']))
    if snapshot!=d['source_inventory']:raise ValueError('Root independently pinned SOURCE inventory differs')
    verify_inventory(SOURCE,snapshot)
    stdout=read(terminal_file(e['full_stdout']['path'],e['full_stdout']['sha256']))
    if stdout!=dict(declaration=str(OUT/'declaration.json'),declaration_sha256=declared):
        raise ValueError('complete actual new PREP stdout differs')
    if terminal_file(e['full_stderr']['path'],e['full_stderr']['sha256']).stat().st_size!=0:
        raise ValueError('successful new PREP stderr must be empty')
    if len({e['full_stdout']['path'],e['full_stderr']['path'],source_inventory_pin['path'],str(TERMINAL/PREP_NAME)})!=4:
        raise ValueError('independent Root PREP proof paths must be distinct')
    return dict(receipt=dict(path=str(TERMINAL/PREP_NAME),sha256=sha),source_inventory=source_inventory_pin,
        full_stdout=e['full_stdout'],full_stderr=e['full_stderr'],
        input_graph=d['input_graph'],historical_whole_component_body=BODY_BINDING)


if __name__=='__main__':
    require_ready()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare-build','run-build','audit-build','admit'])
    parser.add_argument('--sha256');parser.add_argument('--prep-sha256');parser.add_argument('--terminal-evidence');parser.add_argument('--terminal-evidence-sha256')
    a=parser.parse_args()
    if a.action=='prepare-build':prepare_build()
    elif a.action=='run-build':run_build(a.sha256,a.prep_sha256)
    elif a.action=='audit-build':audit_build(a.sha256,a.prep_sha256)
    else:print(json.dumps(production_admission(a.sha256,a.terminal_evidence,a.terminal_evidence_sha256),allow_nan=False),flush=True)

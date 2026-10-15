"""Root-bound canonical read-only metadata timing diagnostic; no build credit.

Only Root may bind and run this source. Importing this driver creates no output.
The future action imports the canonical new factory and invokes exactly four
already audited pure-read metadata functions once directly. It never invokes
prepare/build/audit/admit, helpers, numerical controls or transport.
"""
import argparse
import ast
from collections import Counter
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import stat
import struct
import sys
import time
import types

STATUS='READY_ROOT_BOUND_READONLY_METADATA_DIAGNOSTIC_ONLY'
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
CANONICAL_TARGET=ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
TARGET_FACTORY=CANONICAL_TARGET
TARGET_FACTORY_SHA256='4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
OUT_PREFIX='axial-material-complete-environment-metadata-timing-v14b-'
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FUNCTIONS=('sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs')
SUPPORT=('require','read','pin','digest')
ARCHIVE_CAP=64*2**20
PYTHON=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')

def identity(path):
    x=Path(path).lstat()
    return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]

def pin(path,wanted=None):
    path=Path(path);before=identity(path)
    if not stat.S_ISREG(before[2]):raise ValueError('diagnostic input must be an unaliased regular file: '+str(path))
    with path.open('rb') as stream:
        value=hashlib.file_digest(stream,'sha256').hexdigest()
    if identity(path)!=before or (wanted is not None and value!=wanted):
        raise ValueError('complete metadata diagnostic input drift: '+str(path))
    return dict(path=str(path),sha256=value,size_bytes=before[4],identity=before)

def write_new(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)
        stream.write('\n')

def unique(items):
    result={}
    for key,value in items:
        if key in result:raise ValueError('duplicate metadata JSON key')
        result[key]=value
    return result

def read(path):
    return json.loads(Path(path).read_text(),object_pairs_hook=unique,
        parse_constant=lambda token:(_ for _ in ()).throw(ValueError(token)))

def load_canonical():
    if (TARGET_FACTORY is None or Path(TARGET_FACTORY)!=CANONICAL_TARGET
            or type(TARGET_FACTORY_SHA256) is not str or len(TARGET_FACTORY_SHA256)!=64
            or any(c not in '0123456789abcdef' for c in TARGET_FACTORY_SHA256)):
        raise ValueError('UNREADY: exact canonical target source and SHA must be bound by Root')
    source=pin(TARGET_FACTORY,TARGET_FACTORY_SHA256)
    name='axmat_v14b_readonly_metadata_timing_canonical_factory'
    if name in sys.modules:raise ValueError('fresh canonical diagnostic module identity required')
    spec=importlib.util.spec_from_file_location(name,TARGET_FACTORY)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    if (Path(module.__file__)!=CANONICAL_TARGET or module.ROOT!=ROOT
            or pin(TARGET_FACTORY,TARGET_FACTORY_SHA256)!=source):
        raise ValueError('normal canonical module source or ROOT binding differs')
    return module,source

def source_input_pins(module):
    """Independently enumerate each literal the four frozen readers may open.

    All declared expected SHA values come from pinned source/JSON owners. The
    original parent declaration has no expectedSHA in source_inputs(); its
    current fullSHA/identity is independently bound before and after profiling.
    This enumeration does not call a factory metadata function.
    """
    expected={}
    def add(path,wanted):
        literal=str(path)
        if not Path(literal).is_absolute() or type(wanted) is not str or len(wanted)!=64:
            raise ValueError('complete literal metadata source pin required')
        old=expected.get(literal)
        if old is not None and old!=wanted:raise ValueError('diagnostic source owner SHA conflict')
        expected[literal]=wanted
    text=Path(TARGET_FACTORY).read_text();tree=ast.parse(text)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='source_inputs')
    assignment=next(n for n in fn.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='expected' for t in n.targets))
    if not isinstance(assignment.value,ast.Dict):raise ValueError('frozen literal source_inputs owner map required')
    for key,value in zip(assignment.value.keys,assignment.value.values):
        if not isinstance(key,ast.Name) or not isinstance(value,ast.Name):
            raise ValueError('literal owner/sourceSHA names must remain complete')
        add(getattr(module,key.id),getattr(module,value.id))
    pairs=(('SENDER_PATCH_HELPER','SENDER_PATCH_HELPER_SHA'),('SENDER_SOURCE','SENDER_SOURCE_SHA'),
        ('CANDIDATE_SENDER_SOURCE','CANDIDATE_SENDER_SHA'),('SENDER_SOURCE_PROOF','SENDER_SOURCE_PROOF_SHA'),
        ('SENDER_SOURCE_INPUT','SENDER_SOURCE_INPUT_SHA'),('SENDER_FACTORY_SOURCE_PARENT','SENDER_FACTORY_SOURCE_PARENT_SHA'),
        ('SENDER_CONTROL_SOURCE','SENDER_CONTROL_SOURCE_SHA'),('SENDER_CONTROL_CONTRACT','SENDER_CONTROL_CONTRACT_SHA'),
        ('SENDER_CONTROLS_AUDITOR','SENDER_CONTROLS_AUDITOR_SHA'),
        ('STREAM_ENVIRONMENT_PARENT_HELPER','STREAM_ENVIRONMENT_PARENT_HELPER_SHA'),
        ('STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT','STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA'),
        ('STREAM_ENVIRONMENT_HELPER','STREAM_ENVIRONMENT_HELPER_SHA'),
        ('STREAM_ENVIRONMENT_SOURCE_PROOF','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA'),
        ('STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA'))
    for pathattr,shaattr in pairs:add(getattr(module,pathattr),getattr(module,shaattr))
    # Plain JSON observations, not calls to any helper or factory metadata API.
    proof=read(module.SENDER_SOURCE_PROOF);senderinput=read(module.SENDER_SOURCE_INPUT)
    add(module.CANDIDATE_SENDER_SOURCE.parent/'FLUSP64.candidate_unit.f',proof['candidate_wrapper_sha256'])
    add(module.CANDIDATE_SENDER_SOURCE.parent/'FLUSP64.original_reference_unit.f',proof['reference_wrapper_sha256'])
    add(senderinput['original_receiver']['path'],senderinput['original_receiver']['sha256'])
    streamproof=read(module.STREAM_ENVIRONMENT_SOURCE_PROOF)
    for key in ('author_source_review','author_actual_source_terminal_receipt'):
        add(streamproof[key]['path'],streamproof[key]['sha256'])
    controls=read(module.STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS)
    for literal,wanted in controls['files'].items():add(literal,wanted)
    parent=module.PARENT/'declaration.json'
    add(parent,pin(parent)['sha256'])
    records=[pin(Path(literal),wanted) for literal,wanted in expected.items()]
    return records

def profile_registry(module):
    allcode={}
    for name,value in vars(module).items():
        if isinstance(value,types.FunctionType) and value.__module__==module.__name__:
            allcode[value.__code__]=name
    allowed={};definition={}
    text=Path(TARGET_FACTORY).read_text();tree=ast.parse(text)
    for name in (*FUNCTIONS,*SUPPORT):
        fn=getattr(module,name)
        if not isinstance(fn,types.FunctionType) or fn.__module__!=module.__name__:
            raise ValueError('one real canonical Python metadata function required')
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
        source=ast.get_source_segment(text,node)
        definition[name]=dict(name=name,line=node.lineno,end_line=node.end_lineno,
            source_sha256=hashlib.sha256(source.encode()).hexdigest(),canonical_file=str(TARGET_FACTORY))
        def walk(code):
            if code.co_filename!=str(TARGET_FACTORY):raise ValueError('canonical function code filename differs')
            key=code.co_qualname+'@'+str(code.co_firstlineno)
            allowed[code]=key
            for item in code.co_consts:
                if isinstance(item,types.CodeType):walk(item)
        walk(fn.__code__)
    return allowed,{code:name for code,name in allcode.items() if code not in allowed},definition

def plain_return(value):
    if type(value) is float:
        if not math.isfinite(value):raise ValueError('nonfinite diagnostic return is forbidden')
        return value
    if type(value) in (str,int,bool) or value is None:return value
    if type(value) in (tuple,list):return [plain_return(x) for x in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):raise ValueError('complete returned metadata keys must be strings')
        return {key:plain_return(item) for key,item in value.items()}
    raise ValueError('unexpected factory metadata return type: '+type(value).__name__)

def run_profile(module,out):
    allowed,forbidden,definitions=profile_registry(module)
    stats={key:dict(calls=0,returns=0,inclusive_ns=0,exclusive_selected_canonical_ns=0) for key in allowed.values()}
    stack=[];edges=Counter();direct=Counter();phase=None
    violations=[]
    def observe(frame,event,arg):
        nonlocal phase
        if event not in ('call','return'):return
        code=frame.f_code
        if event=='call' and code in forbidden:
            violations.append(dict(name=forbidden[code],phase=phase,line=frame.f_lineno))
            raise ValueError('forbidden non-metadata canonical function called: '+forbidden[code])
        if code not in allowed:return
        now=time.perf_counter_ns();key=allowed[code]
        if event=='call':
            stats[key]['calls']+=1
            caller=allowed.get(frame.f_back.f_code,'DIRECT_DRIVER') if frame.f_back else 'NO_PARENT'
            edges[(phase,caller,key)]+=1
            stack.append(dict(frame=id(frame),key=key,start=now,selected_children=0))
        else:
            if not stack or stack[-1]['frame']!=id(frame):raise ValueError('complete selected-frame profile stack differs')
            row=stack.pop();elapsed=now-row['start']
            stats[key]['returns']+=1;stats[key]['inclusive_ns']+=elapsed
            stats[key]['exclusive_selected_canonical_ns']+=elapsed-row['selected_children']
            if stack:stack[-1]['selected_children']+=elapsed
    if sys.getprofile() is not None:raise ValueError('fresh nonnested diagnostic profiler required')
    results=[];started=time.monotonic()
    try:
        sys.setprofile(observe)
        for name in FUNCTIONS:
            phase=name;before=time.monotonic()
            direct[name]+=1;value=getattr(module,name)()
            elapsed=time.monotonic()-before
            # Profiler selected only canonical code; output encoding is outside
            # the four measured calls and does not alter the imported module.
            path=out/(name+'.return.json')
            write_new(path,dict(function=name,python_return_type=type(value).__name__,
                               return_value=plain_return(value)))
            results.append(dict(function=name,direct_invocations=1,
                elapsed_seconds_including_passive_profile=elapsed,complete_return=pin(path)))
    finally:
        sys.setprofile(None)
    if stack or violations or set(direct)!=set(FUNCTIONS) or any(count!=1 for count in direct.values()):
        raise ValueError('complete four pure metadata calls and clean passive profile required')
    if any(row['calls']!=row['returns'] or row['exclusive_selected_canonical_ns']<0 for row in stats.values()):
        raise ValueError('complete calls/returns/nonnegative canonical timing required')
    return dict(direct_invocations=dict(direct),profiled_functions=stats,
        call_edges=[dict(action=a,caller=b,callee=c,calls=count) for (a,b,c),count in sorted(edges.items())],
        selected_definition_sources=definitions,complete_function_returns=results,
        total_diagnostic_seconds_including_return_output=time.monotonic()-started,
        profile_semantics='Inclusive elapsed spans and exclusive subtraction of selected canonical Python children only. Unprofiled stdlib/C work remains in the selected frame; profiler overhead is not removed.',
        no_module_function_replacements=True,profiler_cleared=sys.getprofile() is None,
        forbidden_canonical_calls=violations)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True);args=parser.parse_args()
    if STATUS!='READY_ROOT_BOUND_READONLY_METADATA_DIAGNOSTIC_ONLY':
        raise ValueError('UNREADY: diagnostic source and bindings need Root review')
    if (Path(sys.executable).resolve()!=PYTHON or sys.flags.optimize or not sys.dont_write_bytecode
            or os.environ.get('PYTHONOPTIMIZE') or any(os.environ.get(k)!='1' for k in THREAD_KEYS)):
        raise ValueError('original nonoptimized bytecode-off single-thread Python3.12 required')
    out=Path(args.out)
    if not out.is_absolute() or out.parent!=ART or not out.name.startswith(OUT_PREFIX) or os.path.lexists(out):
        raise ValueError('new exclusive metadata diagnostic namespace required; no retry')
    started=time.monotonic();module,source=load_canonical()
    inputs=source_input_pins(module)
    out.mkdir()
    try:
        profile=run_profile(module,out)
        for row in inputs:
            if pin(row['path'],row['sha256'])!=row:
                raise ValueError('complete input SHA/7identity changed across metadata diagnostic')
        if pin(TARGET_FACTORY,TARGET_FACTORY_SHA256)!=source:
            raise ValueError('canonical target source changed across metadata diagnostic')
        value=dict(schema='AXMAT_V14B_READONLY_COMPLETE_METADATA_TIMING_DIAGNOSTIC_RESULT_V1',
            status='READONLY_METADATA_PROFILE_COMPLETE_DIAGNOSTIC_ONLY',source=source,
            all_metadata_input_pins_before_after=inputs,profile=profile,
            elapsed_seconds=time.monotonic()-started,threads=1,children_at_once=1,retries=0,
            archive_cap_bytes=ARCHIVE_CAP,external_original_watchdog_required=dict(wall_seconds=120,rss_mib=512),
            old_failed_V13_factory_imported_or_called=False,prepare_build_run_build_audit_or_admit_called=False,
            numerical_controls_compiler_or_transport_executed=False,original86_stage_count_increment=0,
            component_or_native_or_AAA_ABA_credit=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        write_new(out/'result.json',value)
        files={str(p.relative_to(out)):pin(p)['sha256'] for p in sorted(out.iterdir()) if p.is_file()}
        write_new(out/'raw_preservation_manifest.json',dict(schema='AXMAT_V14B_READONLY_METADATA_TIMING_RAW_MANIFEST_V1',
            files=files,original86_stage_count_increment=0,component_native_AAA_ABA_credit=False))
        if sum(p.stat().st_size for p in out.iterdir())>=ARCHIVE_CAP:raise ValueError('original64MiB diagnostic archive bound exceeded')
        print(json.dumps(dict(status=value['status'],result_sha256=pin(out/'result.json')['sha256'],
            Root_actual_child_terminal_required_before_admission=True),allow_nan=False),flush=True)
    except BaseException as error:
        write_new(out/'failed_result.json',dict(status='FAILED_READONLY_METADATA_DIAGNOSTIC_NO_RETRY',
            error=repr(error),elapsed_seconds=time.monotonic()-started,component_native_AAA_ABA_credit=False))
        raise

if __name__=='__main__':main()

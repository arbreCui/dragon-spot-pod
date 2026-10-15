from pathlib import Path
import ast
import gc
import gzip
import hashlib
import json
import math
import os
import resource
import signal
import stat
import struct
import sys
import tempfile
import threading
import time
from types import SimpleNamespace

started=time.monotonic()
assert sys.flags.optimize==0 and sys.dont_write_bytecode
assert threading.active_count()==1
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):assert os.environ.get(name)=='1'
CHILD_ATTEMPTS=[]
def no_child(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.exec','os.posix_spawn','os.spawn','os.startfile','os.startfile/2'):
        CHILD_ATTEMPTS.append(event)
        raise RuntimeError('Source-only preparation forbids Python process-launch attempt: '+event)
sys.addaudithook(no_child)
def deadline(signum,frame):raise TimeoutError('600s Source-only preparation cap')
signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,600)
def checkpoint():
    own=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    assert 0<=own<512*2**20 and time.monotonic()-started<600 and threading.active_count()==1 and not CHILD_ATTEMPTS
    return dict(elapsed_seconds=time.monotonic()-started,own_historical_peak_rss_bytes=own,threads=1,Python_process_launch_attempts=list(CHILD_ATTEMPTS))
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path)
    for q in (p,*p.parents):assert not q.is_symlink(),str(q)
    before=p.lstat();assert stat.S_ISREG(before.st_mode) and before.st_nlink==1
    h=hashlib.sha256();count=0
    with p.open('rb') as f:
        assert identity(os.fstat(f.fileno()))==identity(before)
        for block in iter(lambda:f.read(524288),b''):h.update(block);count+=len(block)
        assert identity(os.fstat(f.fileno()))==identity(before)
    assert identity(p.lstat())==identity(before) and count==before.st_size
    return dict(path=str(p),size_bytes=count,sha256=h.hexdigest(),identity=identity(before))
def put(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    return pin(p)
def pairs(items):
    result={}
    for k,v in items:assert k not in result;result[k]=v
    return result
def finite(v):raise ValueError('nonfinite saved JSON '+v)
def read_json(p):
    before=pin(p)
    with Path(p).open('rt',encoding='utf8') as f:v=json.load(f,object_pairs_hook=pairs,parse_constant=finite)
    assert pin(p)==before and type(v) is dict
    return v
def require_fixed(p):
    got=pin(p['path']);assert got==p
    return got
def gzip_object(desc):
    before=pin(desc['path'])
    assert {k:before[k] for k in ('path','sha256','identity')}=={k:desc[k] for k in ('path','sha256','identity')} and before['size_bytes']==desc['size_bytes']
    assert desc['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and desc['no_fields_or_records_filtered'] is True
    h=hashlib.sha256();n=0
    with gzip.open(desc['path'],'rb') as f:
        for block in iter(lambda:f.read(524288),b''):h.update(block);n+=len(block)
    assert type(desc['uncompressed_JSON_bytes']) is int and n==desc['uncompressed_JSON_bytes'] and h.hexdigest()==desc['uncompressed_JSON_sha256']
    with gzip.open(desc['path'],'rt',encoding='ascii') as f:v=json.load(f,object_pairs_hook=pairs,parse_constant=finite)
    assert type(v) is dict and pin(desc['path'])==before
    checkpoint()
    return v
def compare_full_gzip_bytes(left,right):
    count=0;h=hashlib.sha256()
    with gzip.open(left['path'],'rb') as a,gzip.open(right['path'],'rb') as b:
        while True:
            av=a.read(524288);bv=b.read(524288);assert av==bv
            if not av:break
            count+=len(av);h.update(av)
    assert count==left['uncompressed_JSON_bytes']==right['uncompressed_JSON_bytes'] and h.hexdigest()==left['uncompressed_JSON_sha256']==right['uncompressed_JSON_sha256']
    return dict(full_uncompressed_byte_comparison=True,full_both_EOF=True,bytes=count,sha256=h.hexdigest(),fields_or_rows_selected=False)
def independent_full_snapshot_pin(value):
    h=hashlib.sha256();nodes=0
    def emit(tag,payload=b''):h.update(tag);h.update(struct.pack('>Q',len(payload)));h.update(payload)
    def visit(part):
        nonlocal nodes
        nodes+=1;kind=type(part)
        emit(b'T',(kind.__module__+'.'+kind.__qualname__).encode('utf8'))
        if kind in (dict,list,tuple):
            emit(b'N',str(len(part)).encode('ascii'))
            if kind is dict:
                for k,v in part.items():visit(k);visit(v)
            else:
                for v in part:visit(v)
        elif kind is str:emit(b'S',str.encode(part,'utf8','surrogatepass'))
        elif kind is bytes:emit(b'B',part)
        elif kind is float:emit(b'F',struct.pack('>d',part))
        elif kind is int:emit(b'J',str(part).encode('ascii'))
        elif kind is bool:emit(b'Z',b'1' if part else b'0')
        elif part is None:emit(b'0')
        else:raise TypeError(kind)
    visit(value)
    return dict(schema='FULL_STREAM_TYPE_ORDER_VALUE_ATTRS_FLOATBITS_CONTROL_PIN_V1',sha256=h.hexdigest(),complete_node_count=nodes,mutable_identities_included=False,no_fields_or_rows_selected=True)

OLD_DIR=Path('/private/tmp/SPOT_V28_ACTUAL_FULLFRESH_ROOT_CLOSEOUT_SOURCE_ONLY_k2lypmeg')
OLD=OLD_DIR/'ROOT_CLOSE_ACTUAL_V28_FULLFRESH_COMPLETE_EVIDENCE.py'
OLD_MANIFEST=OLD_DIR/'SOURCE_ONLY_REVIEW_MANIFEST.json'
PRE=Path('/private/tmp/Root_v28_fullfresh_original_resource_precheck_v2_20261011.py')
oldpin=pin(OLD);assert oldpin['sha256']=='10cd7c565df9b23bebe4f27b8060b5ed23cfeb6939a08ec5404e86db242f9395'
oldmanifestpin=pin(OLD_MANIFEST);assert oldmanifestpin['sha256']=='3da84dca7fbedbeae5c59928b4dd71d9252be1008aab06e59f45eab709f6e3a1'
old=OLD.read_text();prefix=PRE.read_text().split('value=account(64*2**20)',1)[0]
assert old.startswith(prefix)
outdir=Path('/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011')
assert not outdir.exists() and not outdir.is_symlink()
R=Path(tempfile.mkdtemp(prefix='SPOT_V28_ACTUAL_FULLFRESH_ROOT_CLOSEOUT_SOURCE_ONLY_V2_SCHEMA_CHECKED_',dir='/private/tmp'))
P=R/'ROOT_CLOSE_ACTUAL_V28_FULLFRESH_COMPLETE_EVIDENCE.py'
oldtree=ast.parse(old)
assigns={x.targets[0].id:x.value for x in oldtree.body if isinstance(x,ast.Assign) and len(x.targets)==1 and isinstance(x.targets[0],ast.Name)}
fixed=ast.literal_eval(assigns['FIXED_INPUT_PINS'])
copyplan=ast.literal_eval(assigns['COPY_PLAN'])
extra=[oldpin,oldmanifestpin,pin(Path(__file__).resolve()),pin('/private/tmp/SPOT_v28_closeout_v2_saved_metadata_projection_initial_failure_actual_tools_20261011.json')]
fixed+=extra
for p,name in zip(extra,('ROOT_CLOSEOUT_UNEXECUTED_V1_SOURCE.py','ROOT_CLOSEOUT_UNEXECUTED_V1_MANIFEST.json','ROOT_CLOSEOUT_V2_SOURCE_PREPARATION_AND_SAVED_METADATA_CHECK.py','ACTUAL_SOURCE_PREPARATION_PROJECTION_INITIAL_FAILURE_TOOL_RETURNS.json')):
    copyplan.append(dict(original=p,destination='Source_and_Root_actual_evidence/'+name))
audit=r'''# Python-level process-launch attempts are blocked before the original guard imports.
# This observes the named Python audit events, not native/C process creation.
import sys
ROOT_PYTHON_PROCESS_LAUNCH_ATTEMPTS = []
ROOT_PYTHON_PROCESS_LAUNCH_AUDIT_EVENTS = ('subprocess.Popen','os.system','os.fork','os.forkpty','os.exec','os.posix_spawn','os.spawn','os.startfile','os.startfile/2')
def _Root_forbid_Python_process_launch(event,args):
    if event in ROOT_PYTHON_PROCESS_LAUNCH_AUDIT_EVENTS:
        ROOT_PYTHON_PROCESS_LAUNCH_ATTEMPTS.append(dict(event=event))
        raise RuntimeError('external Root metadata closeout forbids Python process-launch attempt: '+event)
sys.addaudithook(_Root_forbid_Python_process_launch)

'''
changes=[]
def change(before,after):
    global source
    assert source.count(before)==1,(before[:100],source.count(before))
    source=source.replace(before,after,1);changes.append((before,after))
source=old
change('FIXED_INPUT_PINS = '+repr(ast.literal_eval(assigns['FIXED_INPUT_PINS'])),'FIXED_INPUT_PINS = '+repr(fixed))
change('COPY_PLAN = '+repr(ast.literal_eval(assigns['COPY_PLAN'])),'COPY_PLAN = '+repr(copyplan))
change('ORIGINAL_PREFIX_BYTES = '+str(len(prefix.encode())), 'ORIGINAL_PREFIX_BYTES = '+str(len(prefix.encode()))+'\nORIGINAL_PREFIX_OFFSET_BYTES = '+str(len(audit.encode())))
change('assert 0<=rss<512*2**20 and time.monotonic()-started<600 and threading.active_count()==1\n    return dict(seconds=time.monotonic()-started,own_historical_peak_rss_bytes=rss,threads=1,children_started=0)',
       "assert 0<=rss<512*2**20 and time.monotonic()-started<600 and threading.active_count()==1 and not ROOT_PYTHON_PROCESS_LAUNCH_ATTEMPTS\n    return dict(seconds=time.monotonic()-started,own_historical_peak_rss_bytes=rss,threads=1,Python_process_launch_audit_installed_before_original_guard_imports=True,Python_process_launch_attempts=list(ROOT_PYTHON_PROCESS_LAUNCH_ATTEMPTS),blocked_Python_audit_events=list(ROOT_PYTHON_PROCESS_LAUNCH_AUDIT_EVENTS),audit_scope='NAMED_PYTHON_PROCESS_LAUNCH_ATTEMPTS_AFTER_HOOK_INSTALL',native_C_child_creation_observed=False,process_creation_before_script_hook_observed=False)")
change("Path(__file__).read_bytes()[:ORIGINAL_PREFIX_BYTES]", "Path(__file__).read_bytes()[ORIGINAL_PREFIX_OFFSET_BYTES:ORIGINAL_PREFIX_OFFSET_BYTES+ORIGINAL_PREFIX_BYTES]")
change("SPOT_ROOT_ACTUAL_V28_COMPLETE_FULLFRESH_PRIVATE_SNAPSHOT_EXTERNAL_CLOSED_BINDING_V1", "SPOT_ROOT_ACTUAL_V28_COMPLETE_FULLFRESH_PRIVATE_SNAPSHOT_EXTERNAL_CLOSED_BINDING_V2")
change("original_guards_prefix_byte_exact_sha256=ORIGINAL_PREFIX_SHA256,external_closeout_checkpoint=checkpoint()", "original_guards_prefix_byte_exact_sha256=ORIGINAL_PREFIX_SHA256,original_guards_prefix_byte_offset=ORIGINAL_PREFIX_OFFSET_BYTES,external_closeout_checkpoint=checkpoint()")
change("No helper Q, Native/solver/training, whole-build memory qualification, AAA accuracy or ABA admission was created.\\n'",
       "No helper Q, Native/solver/training, whole-build memory qualification, AAA accuracy or ABA admission was created.\\nA Python audit hook blocks the named process-launch attempts from before original guard imports; its actual attempt list is empty at every checkpoint. Native/C child creation and process creation before this script hook are not observed by this hook. The no Native/solver/training/PS scope also follows the saved Source; it is not OS-wide monitoring.\\n'")
source=audit+source
assert source.encode()[len(audit.encode()):len(audit.encode())+len(prefix.encode())]==prefix.encode()
inverse=source[len(audit):]
for before,after in reversed(changes):assert inverse.count(after)==1;inverse=inverse.replace(after,before,1)
assert inverse.encode()==old.encode()
newtree=ast.parse(source)
oldfuncs={x.name:ast.dump(x,include_attributes=False) for x in ast.parse(prefix).body if isinstance(x,ast.FunctionDef)}
newfuncs={x.name:ast.dump(x,include_attributes=False) for x in newtree.body if isinstance(x,ast.FunctionDef)}
assert all(newfuncs[k]==v for k,v in oldfuncs.items())
P.write_text(source);sourcepin=pin(P)

# Execute only the saved-metadata assertion projection, never the closeout
# writer, original guard prefix, graph/helper, controller or a process monitor.
constants={}
newassigns={x.targets[0].id:x.value for x in newtree.body if isinstance(x,ast.Assign) and len(x.targets)==1 and isinstance(x.targets[0],ast.Name)}
for name in ('FIXED_INPUT_PINS','ACTUAL_TOOL_PIN','ACTUAL_HOST_PIN','ACTUAL_CONTROL_PIN','INDEPENDENT_REVIEW_PIN','RETURN_FIELDS','TRACE_FIELDS','SNAPSHOT_CONTROL_PIN'):
    constants[name]=ast.literal_eval(newassigns[name])
beforepins=[require_fixed(p) for p in fixed]
startidx=next(i for i,x in enumerate(newtree.body) if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id=='source_review')
endidx=next(i for i,x in enumerate(newtree.body) if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id=='original_archive_before')
projection=newtree.body[startidx:endidx]
projection_original_ast_sha=hashlib.sha256(ast.dump(ast.Module(body=projection,type_ignores=[]),include_attributes=False).encode()).hexdigest()
filtered=[];excluded=[]
for node in projection:
    targets=[x.id for x in node.targets if isinstance(x,ast.Name)] if isinstance(node,ast.Assign) else []
    controller_import_call=(isinstance(node,ast.Expr) and ast.get_source_segment(source,node)=='spec.loader.exec_module(controller)')
    if any(name in ('spec','controller') for name in targets) or controller_import_call:
        excluded.append(dict(line=node.lineno,source=ast.get_source_segment(source,node),reason='No controller import or execution; independent complete builtin snapshot fingerprint supplied'))
    else:filtered.append(node)
assert len(excluded)==3
assert not any(isinstance(x,(ast.Import,ast.ImportFrom,ast.With,ast.FunctionDef,ast.ClassDef,ast.Try,ast.While)) for x in ast.walk(ast.Module(body=filtered,type_ignores=[])))
readlog={};assertlog={}
def observe_read(expr,container,key):
    result=container[key]
    label=expr+' [key='+repr(key)+']'
    entry=readlog.setdefault(label,dict(expression=expr,key_repr=repr(key),container_builtin_type=type(container).__name__,result_builtin_type=type(result).__name__,successful_reads=0))
    entry['successful_reads']+=1
    return result
def observe_assert(line,expression):
    entry=assertlog.setdefault(str(line),dict(source_line=line,expression=expression,executions=0));entry['executions']+=1
class Instrument(ast.NodeTransformer):
    def visit_Subscript(self,node):
        expr=ast.get_source_segment(source,node)
        node=self.generic_visit(node)
        if isinstance(node.ctx,ast.Load):
            assert not isinstance(node.slice,ast.Slice)
            return ast.copy_location(ast.Call(func=ast.Name(id='observe_read',ctx=ast.Load()),args=[ast.Constant(expr),node.value,node.slice],keywords=[]),node)
        return node
    def visit_Assert(self,node):
        expr=ast.get_source_segment(source,node.test)
        line=node.lineno;node=self.generic_visit(node)
        observed=ast.copy_location(ast.Expr(ast.Call(func=ast.Name(id='observe_assert',ctx=ast.Load()),args=[ast.Constant(line),ast.Constant(expr)],keywords=[])),node)
        return [observed,node]
module=ast.fix_missing_locations(Instrument().visit(ast.Module(body=filtered,type_ignores=[])))
controller=SimpleNamespace(snapshot_order_type_bit_pin=independent_full_snapshot_pin)
env=dict(constants,read_json=read_json,pairs=pairs,finite=finite,json=json,Path=Path,AO=Path('/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-complete-fresh-v28-20261011-dwah5ubd'),math=math,gzip_object=gzip_object,compare_full_gzip_bytes=compare_full_gzip_bytes,gc=gc,require_fixed=require_fixed,checkpoint=checkpoint,controller=controller,observe_read=observe_read,observe_assert=observe_assert)
exec(compile(module,str(P)+'::saved_metadata_assert_projection','exec'),env)
assert [require_fixed(p) for p in fixed]==beforepins
assert pin(OLD)==oldpin and pin(OLD_MANIFEST)==oldmanifestpin and pin(P)==sourcepin and not outdir.exists()
report=env['report'];host=env['host']
assert any(x['expression']=="actual['actual_bytes_read']" for x in readlog.values())
assert any(x['expression']=="report['caps_checkpoint']['own_peak_rss_bytes']" for x in readlog.values())
actual_assert_count=sum(x['executions'] for x in assertlog.values())
static=dict(schema='SPOT_V28_SAVED_METADATA_ASSERT_PROJECTION_ACTUAL_REVIEW_V1',status='ALL_ACTUAL_SAVED_METADATA_ASSERTS_PASSED_NO_WRITER_OR_CONTROLLER_EXECUTION',actual_candidate_Source=sourcepin,projection_start_line=newtree.body[startidx].lineno,projection_end_before_line=newtree.body[endidx].lineno,projection_original_ast_sha256=projection_original_ast_sha,projection_all_original_metadata_asserts_kept=True,static_assert_sites=len(assertlog),actual_assert_executions=actual_assert_count,all_successful_subscript_reads=list(readlog.values()),actual_assertions=list(assertlog.values()),excluded_controller_import_assignments=excluded,independent_full_builtin_snapshot_type_order_floatbits_algorithm=True,full_three_gzip_EOF_SHA_and_complete_expected_actual_wire_byte_comparison=True,all_nine_trace_fields_and_37446_complete_records_retained=True,critical_actual_field_values=dict(actual_bytes_read=36433696447,host_whole_seconds=host['whole_seconds'],original_watch_sampled_peak_mib=host['watchdog']['sampled_peak_rss_mib'],child_report_own_peak_rss_bytes=report['caps_checkpoint']['own_peak_rss_bytes'],child_report_elapsed_seconds=report['caps_checkpoint']['elapsed_seconds']),actual_source_and_saved_inputs_before_after=beforepins,checkpoint=checkpoint(),Python_audit_process_attempts=list(CHILD_ATTEMPTS),graph_helper_controller_writer_resourceprefix_or_Native_executed=False,project_or_ART_written=False,original_37445_payloads_reread=False,Q_created=False)
staticpin=put(R/'ACTUAL_SAVED_METADATA_SCHEMA_ASSERT_REVIEW.json',static)
manifest=dict(schema='SPOT_V28_ACTUAL_EXTERNAL_CLOSEOUT_SOURCE_ONLY_REVIEW_V2',status='FIXED_SCHEMA_ACTUALLY_CHECKED_NOT_EXECUTED_PENDING_ROOT_REVIEW',writer_Source=sourcepin,previous_unexecuted_v1_Source=oldpin,previous_unexecuted_v1_manifest=oldmanifestpin,original_precheck_Source=pin(PRE),original_prefix_bytes=len(prefix.encode()),original_prefix_offset_bytes=len(audit.encode()),original_prefix_sha256=hashlib.sha256(prefix.encode()).hexdigest(),prefix_frozen_joint_account_and_training_resources_byte_exact=True,all_original_precheck_function_AST_identical=True,whole_v2_inverse_to_unexecuted_v1_byte_exact=True,exact_forward_changes=[dict(before=a,after=b) for a,b in changes],added_header=audit,strict_Python_process_launch_audit_before_guard_imports=True,Python_hook_scope='Named Python audit process-launch events after script hook; not native/C or pre-script OS monitoring',saved_metadata_actual_assert_review=staticpin,actual_fixed_inputs=fixed,complete_closed_namespaces=ast.literal_eval(newassigns['FROZEN_COMPLETE_NAMESPACES']),complete_copy_plan=copyplan,copy_plan_files=len(copyplan)+1,copy_plan_data_bytes=sum(x['original']['size_bytes'] for x in copyplan)+sourcepin['size_bytes'],future_out=str(outdir),Source_preparation_and_saved_metadata_projection_only=True,closeout_executed=False,Q_created=False,Native_started=False,whole_522_to_512_memory_pass=False,preparation_Source=pin(Path(__file__).resolve()),actual_preparation_checkpoint=checkpoint())
manifestpin=put(R/'SOURCE_ONLY_REVIEW_MANIFEST.json',manifest)
assert pin(P)==sourcepin and pin(OLD)==oldpin and pin(OLD_MANIFEST)==oldmanifestpin and [pin(p['path']) for p in fixed]==beforepins and not outdir.exists()
signal.setitimer(signal.ITIMER_REAL,0)
print(json.dumps(dict(root=str(R),Source=sourcepin,manifest=manifestpin,saved_metadata_actual_review=staticpin,static_assert_sites=len(assertlog),actual_assert_executions=actual_assert_count,successful_read_expressions=len(readlog),source_only_not_executed=True,checkpoint=checkpoint())),flush=True)

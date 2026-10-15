"""TMP-only exact full-edge wire-sort comparison; no graph verification or Q."""
import ast,ctypes,gc,hashlib,importlib.util,inspect,json,os,resource,signal,stat,struct,sys,time,tracemalloc
from pathlib import Path,PurePosixPath

sys.dont_write_bytecode=True
D=Path('/private/tmp/SPOT_private_builtin_wire_stable_sort_bn9q4own')
H=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_20261011.py')
C=D/'candidate_graph_helper_builtin_stable_wire_sort_v3.py'
P=D/'SOURCE_ONLY_INVERSE_PROOF_V3.json'
G=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/input_graph.json')
EXPECTED={str(H):'c6e617b25d1df6fd5e1f18f2bd54b648e0abdd892659e51e3693eccb7b57b477',str(C):'6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3',str(P):'9361fcc292adca4a12035769fd805a82484e10f71c78788da730ec5da2c7105c',str(G):'a91c1e63bd768575e715e735886f168b9af6722fddf2bb002317376da5d63ad1'}
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or any(os.environ.get(k)!='1' for k in THREAD_KEYS):raise ValueError('optimize0/thread1 environment required')
start=time.monotonic();phase='initial';samples=[];peak_live=0;phase_peaks={};watch_count=0;declared_reads={str(p):0 for p in (H,C,P,G,Path(__file__))}
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
class GuardViolation(BaseException):pass
class TaskInfo(ctypes.Structure):
    _fields_=[(k,ctypes.c_uint64) for k in ('virtual_size','resident_size','total_user','total_system','threads_user','threads_system')]+[(k,ctypes.c_int32) for k in ('policy','faults','pageins','cow_faults','messages_sent','messages_received','syscalls_mach','syscalls_unix','csw','threadnum','numrunning','priority')]
lib=ctypes.CDLL('/usr/lib/libproc.dylib');lib.proc_pidinfo.argtypes=(ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int);lib.proc_pidinfo.restype=ctypes.c_int
def own():
    t=TaskInfo();got=lib.proc_pidinfo(os.getpid(),4,0,ctypes.byref(t),ctypes.sizeof(t))
    if got!=ctypes.sizeof(t) or t.resident_size<=0:raise GuardViolation('self PID task info unavailable')
    return int(t.resident_size),int(t.threadnum)
def measure():
    global peak_live
    rss,threads=own();peak_live=max(peak_live,rss);phase_peaks[phase]=max(phase_peaks.get(phase,0),rss)
    if rss>=512*2**20:raise GuardViolation('own current RSS 512 MiB cap exceeded')
    if threads!=1:raise GuardViolation('own actual thread count is not one')
    if time.monotonic()-start>=600:raise GuardViolation('whole 600 second cap exceeded')
    return rss,threads
def observe(point,detail=None):
    rss,threads=measure();row=dict(point=point,phase=phase,elapsed_seconds=time.monotonic()-start,own_current_rss_bytes=rss,own_historical_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,own_threads=threads)
    if detail is not None:row['detail']=detail
    samples.append(row);return row
def watch(signum,frame):
    global watch_count
    watch_count+=1;measure()
    if watch_count%20==0:observe('periodic_self_task_info')
signal.signal(signal.SIGALRM,watch);signal.setitimer(signal.ITIMER_REAL,.1,.1)
def safety(event,args):
    if event in ('subprocess.Popen','os.fork','os.forkpty','os.posix_spawn','os.system'):raise GuardViolation('no child process permitted')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)):
            path=str(Path(os.fsdecode(path)).absolute())
            if path in declared_reads:declared_reads[path]+=1
            if isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND) and not Path(path).is_relative_to(D):raise GuardViolation('only this TMP evidence root may be written')
sys.addaudithook(safety)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);s=path.lstat()
    if not stat.S_ISREG(s.st_mode):raise ValueError('regular no-symlink pin required')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
    try:
        if identity(os.fstat(fd))!=identity(s):raise ValueError('pin fd identity differs')
        while True:
            b=os.read(fd,524288)
            if not b:break
            h.update(b);n+=len(b)
        if identity(os.fstat(fd))!=identity(s):raise ValueError('pin changed while reading')
    finally:os.close(fd)
    if n!=s.st_size or identity(path.lstat())!=identity(s):raise ValueError('pin full EOF or identity differs')
    v=dict(path=str(path),size_bytes=n,sha256=h.hexdigest(),identity=identity(s))
    if str(path) in EXPECTED and v['sha256']!=EXPECTED[str(path)]:raise ValueError('fixed Source/saved graph digest differs')
    return v
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def typed(value):
    k=type(value)
    if k is float:return ['float',struct.pack('>d',value).hex()]
    if k is dict:return ['dict',[[typed(a),typed(b)] for a,b in value.items()]]
    if k in (list,tuple):return [k.__name__,[typed(v) for v in value]]
    if isinstance(value,str):return [k.__name__,str.__str__(value),typed(vars(value)) if hasattr(value,'__dict__') else None]
    if k in (type(None),int,bool):return [k.__name__,value]
    if isinstance(value,PurePosixPath):return [k.__name__,str(value)]
    return [k.__name__,repr(value)]
def identities(value):
    if type(value) in (list,tuple):return [id(value),[identities(v) for v in value]]
    if type(value) is dict:return [id(value),[[identities(k),identities(v)] for k,v in value.items()]]
    return id(value)
events=[]
class TaggedStr(str):
    def __new__(cls,value,tag):
        x=super().__new__(cls,value);x.tag=tag;return x
    def __lt__(self,other):
        events.append(['lt',self.tag,str.__str__(self),str.__str__(other) if isinstance(other,str) else repr(other)])
        return super().__lt__(other)
    def __str__(self):return 'custom __str__:'+str.__str__(self)
class Reiterable:
    def __init__(self,first,second):self.first=first;self.second=second;self.calls=0;self.length_calls=0
    def __iter__(self):self.calls+=1;return iter(self.first if self.calls==1 else self.second)
    def __len__(self):self.length_calls+=1;return len(self.second)
class RowList(list):pass
class RowTuple(tuple):pass
def state(value):
    if isinstance(value,Reiterable):return ['Reiterable',typed(value.first),typed(value.second),value.calls,value.length_calls]
    if inspect.isgenerator(value):return ['generator',inspect.getgeneratorstate(value)]
    return typed(value)
def attempt(module,build,method='_wire_requirement_table_compact'):
    global events
    value=build();before=state(value);before_ids=identities(value);events=[]
    try:
        answer=getattr(module,method)(value);outcome=dict(kind='return',complete_typed_return=typed(answer))
        try:outcome['complete_canonical_bytes_hex']=module._canonical_json(answer).hex()
        except GuardViolation:raise
        except BaseException as e:outcome['canonical_encoding_exception']=[type(e).__name__,str(e)]
    except GuardViolation:raise
    except BaseException as e:outcome=dict(kind='raise',exception_class=type(e).__name__,exception_message=str(e))
    return dict(outcome=outcome,comparison_events=list(events),caller_before=before,caller_after=state(value),caller_all_nested_identity_unchanged=before_ids==identities(value))
def traced_builder(module,rows,label):
    global phase
    phase=label;gc.collect();entry=observe(label+'_enter');profile_counts={'tuple_keys':0,'tuple_key_shallow_bytes_sum':0,'builtin_string_keys':0,'other_key_types':{}}
    def prof(frame,event,arg):
        if event=='return' and frame.f_code.co_filename==str(H if module is old else C) and frame.f_code.co_name=='<lambda>':
            if type(arg)is tuple:
                profile_counts['tuple_keys']+=1;profile_counts['tuple_key_shallow_bytes_sum']+=sys.getsizeof(arg)
            elif type(arg)is str:profile_counts['builtin_string_keys']+=1
            else:
                name=type(arg).__name__;profile_counts['other_key_types'][name]=profile_counts['other_key_types'].get(name,0)+1
    tracemalloc.start(1);sys.setprofile(prof);t=time.monotonic()
    try:
        value=module._wire_requirement_table_compact(rows);current,peak=tracemalloc.get_traced_memory()
    finally:sys.setprofile(None);tracemalloc.stop()
    ret=observe(label+'_return')
    return value,dict(elapsed_seconds=time.monotonic()-t,tracemalloc_return_live_bytes=current,tracemalloc_function_peak_bytes=peak,tracemalloc_peak_minus_return_live_bytes=peak-current,actual_key_lambda_returns=profile_counts,entry_self_observation=entry,return_self_observation=ret,measurement_has_tracemalloc_and_profile_overhead=True)
result=dict(schema='SPOT_TMP_COMPLETE_REAL_EDGE_WIRE_SORT_EXACT_PURE_DATA_CONTROL_V1',status='FAIL_CLOSED_NO_QUALIFICATION',source_candidate_admitted=False,Q_created=False,Native_solver_train_PS_started=False,child_processes_started=0,project_or_ART_mutated=False,full_payload_phase_reexecuted=False,whole_522_to_512_RSS_proved=False)
try:
    before={str(p):pin(p) for p in (Path(__file__),H,C,P,G)};observe('fixed_source_payload_driver_before_pins')
    proof=json.loads(P.read_text());a=H.read_bytes();b=C.read_bytes()
    if a.count(proof['exact_before'].encode())!=1 or b!=a.replace(proof['exact_before'].encode(),proof['exact_after'].encode()) or b.replace(proof['exact_after'].encode(),proof['exact_before'].encode())!=a:raise ValueError('complete Source forward/inverse differs')
    aa=ast.parse(a);bb=ast.parse(b)
    if len(aa.body)!=len(bb.body):raise ValueError('Source AST length differs')
    changed=[getattr(x,'name',type(x).__name__) for x,y in zip(aa.body,bb.body) if ast.dump(x,include_attributes=False)!=ast.dump(y,include_attributes=False)]
    if changed!=['_wire_requirement_table_compact']:raise ValueError('unintended AST change')
    del a,b,aa,bb;old=load(H,'spot_tmp_wire_sort_old');new=load(C,'spot_tmp_wire_sort_candidate')
    base=('/pure/control/a','/pure/control/canonical','owner',old.CLOSURE_CATEGORIES[0],old.REQUIREMENT_ROLES[0])
    valid=[base,('/pure/control/b','/pure/control/canonical','owner',old.CLOSURE_CATEGORIES[1],old.REQUIREMENT_ROLES[0]),('/pure/control/a','/pure/control/canonical','ownerZ',old.CLOSURE_CATEGORIES[0],old.REQUIREMENT_ROLES[1]),base]
    fixtures=[('empty',lambda:[]),('complete_duplicates_and_key_ties',lambda:list(reversed(valid))),('tuple_container',lambda:tuple(valid)),('generator_original_exhaustion',lambda:(r for r in valid)),('row_list_rejected',lambda:[list(base)]),('list_subclass_shape_rejected',lambda:[RowList(base)]),('tuple_subclass_shape_rejected',lambda:[RowTuple(base)]),('empty_tuple_rejected',lambda:[()]),('short_tuple_rejected',lambda:[base[:-1]]),('long_tuple_rejected',lambda:[base+('extra',)]),('relative_path_rejected',lambda:[('relative',)+base[1:]]),('unnormalized_path_rejected',lambda:[('/pure/../control/a',)+base[1:]]),('nul_path_rejected',lambda:[('/pure/\x00/a',)+base[1:]]),('blank_owner_rejected',lambda:[base[:2]+(' ',)+base[3:]]),('bad_category_rejected',lambda:[base[:3]+('unknown',)+base[4:]]),('bad_role_rejected',lambda:[base[:4]+('unknown',)])]
    for field in range(5):
        fixtures.append(('accepted_str_subclass_field_'+str(field),lambda field=field:[tuple(TaggedStr(v,'field_'+str(i)) if i==field else v for i,v in enumerate(r)) for r in reversed(valid)]))
        for name,value in [('negative_zero',-0.0),('finite_float',1.25),('nan_payload',struct.unpack('>d',bytes.fromhex('7ff8000000000042'))[0]),('positive_inf',float('inf')),('negative_inf',-float('inf')),('bool',True),('none',None)]:
            fixtures.append((name+'_field_'+str(field),lambda field=field,value=value:[tuple(value if i==field else v for i,v in enumerate(base))]))
    fixtures.append(('accepted_PurePosixPath_nonexact_fields',lambda:[(PurePosixPath(base[0]),PurePosixPath(base[1]))+base[2:]]))
    for name,second in [('None',[None]),('short_tuple',[('/pure/control/a',)]),('list',[list(base)]),('valid_changed',[valid[1],base,base]),('invalid_nonexact',[('/pure/control/a','/pure/control/canonical','owner','unknown',old.REQUIREMENT_ROLES[0])])]:
        fixtures.append(('reiterable_second_pass_'+name,lambda second=second:Reiterable([base],second)))
    fixture_results=[]
    phase='fixtures_original_and_candidate'
    for name,build in fixtures:
        left=attempt(old,build);right=attempt(new,build)
        if left!=right:raise ValueError('wire fixture exact typed/state/exception/comparison difference: '+name)
        fixture_results.append(dict(case=name,old_equals_candidate_complete_return_or_exception=True,original_complete_evidence=left))
    json_fixtures=[('finite_types_order_floatbits',lambda:{'z':[True,1,1.0,-0.0,0.0,1e-300,None],'a':{'b':'text','a':[1.25]}}),('json_str_subclass',lambda:{'x':TaggedStr('text','json')}),('json_nonfinite_nan',lambda:{'x':float('nan')}),('json_nonfinite_inf',lambda:[float('inf')]),('json_nonfinite_negative_inf',lambda:[-float('inf')])]
    for name,build in json_fixtures:
        left=attempt(old,build,'_json_clone');right=attempt(new,build,'_json_clone')
        if left!=right:raise ValueError('unchanged full JSON protocol fixture differs: '+name)
        fixture_results.append(dict(case=name,old_equals_candidate_complete_return_or_exception=True,original_complete_evidence=left))
    result['fixture_results']=fixture_results;observe('all_fixtures_exact_return_exception_state_and_comparison_complete')
    phase='saved_graph_strict_json_decode_once';graph=old.strict_json(str(G),EXPECTED[str(G)]);observe('saved_graph_full_strict_JSON_return')
    saved=graph['requirements'];old._validate_wire_requirement_table(saved)
    if saved['rows']['row_count']!=238780:raise ValueError('real complete logical edge count differs')
    del graph;gc.collect();observe('unneeded_saved_graph_sections_released_after_strict_parse')
    phase='decode_complete_real_edge_rows';paths=saved['paths'];names=saved['owners'];categories=saved['categories'];roles=saved['binding_roles'];limits=(len(paths),len(paths),len(names),len(categories),len(roles))
    requirements=[];previous=None;duplicates=0
    for ids in old._decoded_requirement_rows(saved['rows'],limits):
        row=(paths[ids[0]],paths[ids[1]],names[ids[2]],categories[ids[3]],roles[ids[4]])
        if not all(type(v)is str for v in row):raise ValueError('saved graph symbols are not exact builtin strings')
        if row==previous:duplicates+=1
        requirements.append(row);previous=row
    if len(requirements)!=238780:raise ValueError('complete real edge decode count differs')
    original_row_identities=tuple(id(row) for row in requirements);del previous,ids,row;observe('complete_real_exact_builtin_rows_decoded',{'rows':len(requirements),'adjacent_full_duplicate_edges':duplicates})
    old_table,old_measure=traced_builder(old,requirements,'original_full_wire_builder')
    candidate_table,new_measure=traced_builder(new,requirements,'candidate_full_wire_builder')
    phase='complete_wire_tables_encoded_bytes_exact'
    if old_table!=saved or candidate_table!=saved or typed(old_table)!=typed(candidate_table):raise ValueError('complete real wire table or full field type/order differs')
    old_encoded=old._canonical_json(old_table);new_encoded=new._canonical_json(candidate_table);saved_encoded=old._canonical_json(saved)
    if old_encoded!=new_encoded or old_encoded!=saved_encoded:raise ValueError('complete wire canonical bytes differ')
    if old_table['rows']['data']!=candidate_table['rows']['data'] or old_table['rows']['row_count']!=238780:raise ValueError('complete row codec bytes/count differ')
    if original_row_identities!=tuple(id(row) for row in requirements):raise ValueError('caller row identities/order changed')
    if old_measure['actual_key_lambda_returns']['tuple_keys']!=238780 or new_measure['actual_key_lambda_returns']['tuple_keys']!=0 or new_measure['actual_key_lambda_returns']['builtin_string_keys']!=5*238780:raise ValueError('actual full old/new sort key returns differ from bound Source')
    old_out=D/'ACTUAL_ORIGINAL_COMPLETE_WIRE_TABLE.json';new_out=D/'ACTUAL_CANDIDATE_COMPLETE_WIRE_TABLE.json';old_out.write_bytes(old_encoded+b'\n');new_out.write_bytes(new_encoded+b'\n')
    result.update(status='PASS_FULL_REAL_EDGE_WIRE_BYTES_AND_TYPED_FIXTURES_ONLY_UNADMITTED',changed_top_level_AST_definition=changed,full_Source_forward_and_inverse_byte_exact=True,logical_edges=238780,all_input_rows_exact_builtin_tuple_and_strings=True,caller_complete_row_identity_order_unchanged=True,adjacent_full_duplicate_edges_retained=duplicates,complete_wire_table_old_candidate_saved_bytes_equal=True,complete_wire_table_bytes=len(old_encoded),complete_wire_table_sha256=hashlib.sha256(old_encoded).hexdigest(),complete_encoded_row_data_ascii_bytes=len(old_table['rows']['data']),complete_encoded_row_data_sha256=hashlib.sha256(old_table['rows']['data'].encode('ascii')).hexdigest(),full_output_pins={'old':pin(old_out),'candidate':pin(new_out)},original_full_function_measurement=old_measure,candidate_full_function_measurement=new_measure,measured_key_tuple_shallow_bytes_allocated_original=old_measure['actual_key_lambda_returns']['tuple_key_shallow_bytes_sum'],measured_key_tuple_shallow_bytes_allocated_candidate=0,tracemalloc_function_peak_difference_bytes=old_measure['tracemalloc_function_peak_bytes']-new_measure['tracemalloc_function_peak_bytes'],RSS_scope='One sequential instrumented pure-data process. Allocator reuse and earlier strict graph decode remain in OS RSS; phase differences are not independent whole-process peak improvements or production qualification.')
    observe('complete_real_wire_bytes_and_rows_equal_saved_and_candidate')
    phase='final_Source_and_payload_full_EOF_pins';after={str(p):pin(p) for p in (Path(__file__),H,C,P,G)}
    if before!=after:raise ValueError('Source/driver/proof/saved graph full EOF and seven-field identities changed')
    result.update(before_full_EOF_pins=before,after_full_EOF_pins=after,all_declared_before_after_full_EOF_pins_and_identity_exact=True,saved_graph_strict_json_parse_calls=1,all_37445_canonical_payloads_read=False,fixture_case_count=len(fixture_results));observe('final_full_EOF_pins_exact')
except BaseException as e:
    result.update(status='FAIL_CLOSED_NO_QUALIFICATION',exception_class=type(e).__name__,exception_message=str(e))
finally:
    signal.setitimer(signal.ITIMER_REAL,0);sys.setprofile(None)
    if tracemalloc.is_tracing():tracemalloc.stop()
    result.update(elapsed_seconds=time.monotonic()-start,whole_wall_cap_seconds=600,CPU_cap_seconds=600,own_RSS_fail_closed_threshold_bytes=512*2**20,own_sampled_peak_current_rss_bytes=peak_live,own_historical_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,phase_own_sampled_peak_current_rss_bytes=phase_peaks,own_actual_mainthread_observations=watch_count,samples=samples,declared_paths_open_attempt_counts=declared_reads,OS_hard_RSS_limit_established=False)
    out=D/'ACTUAL_BOUNDED_COMPLETE_WIRE_SORT_CONTROL_RESULT.json'
    with out.open('x')as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    print(json.dumps(dict(path=str(out),size_bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),status=result['status'],elapsed_seconds=result['elapsed_seconds'],own_sampled_peak_current_rss_bytes=peak_live,exception=result.get('exception_message'),fixture_cases=result.get('fixture_case_count'),logical_edges=result.get('logical_edges')),allow_nan=False),flush=True)
    if result['status'].startswith('FAIL'):sys.exit(1)

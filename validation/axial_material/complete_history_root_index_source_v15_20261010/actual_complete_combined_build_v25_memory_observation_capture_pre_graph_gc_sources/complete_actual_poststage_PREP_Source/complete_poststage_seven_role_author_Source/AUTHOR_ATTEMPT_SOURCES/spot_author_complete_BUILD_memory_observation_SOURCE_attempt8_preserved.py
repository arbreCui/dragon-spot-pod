"""Author Source text and finite AST/byte proofs only; never import candidates."""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
import tempfile
import textwrap

PYTHON='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
PLAN=Path('/private/tmp/axmat_V25_closed_BUILD_memory_Source_plan_f5iafdww/SOURCE_MEMORY_LOCALIZATION_AND_DIAGNOSTIC_PLAN.json')
PLAN_SHA='1da0198fa461a438922e65842085cbde31d73ccba535cacf047bd9b662d03988'
ROLES={
 'canonical':P/'canonical.V25.UNREADY.full.py',
 'prepare_binder':P/'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py',
 'build_binder':P/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py',
 **{role:P/'host_and_postclose_templates'/(role+'.V25.UNREADY.full.py') for role in ('prepare_host','prepare_writer','build_host','build_writer')},
 **{name:U/name for name in ('Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_complete_PREP_E_snapshot.py','Root_prepare_poststage_REQUEST.Source_META_only.py','Root_source_installer.py','Root_prelaunch_checker.py','Root_poststage_Source_META_contract.py')}}
NAMES={role:(('host_and_postclose_templates/'+role+'.V25.UNREADY.full.py') if role in ('prepare_host','prepare_writer','build_host','build_writer') else {'canonical':'canonical.V25.UNREADY.full.py','prepare_binder':'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','build_binder':'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'}.get(role,'utilities/'+role)) for role in ROLES}

def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=identity(p);assert stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink()
 payload=p.read_bytes();assert identity(p)==a
 return dict(path=str(p),sha256=hashlib.sha256(payload).hexdigest(),size_bytes=len(payload),identity=a)
def dump(p,d):
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def definitions(s):
 return [(n.name,ast.get_source_segment(s,n),ast.dump(n,include_attributes=False)) for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def replace(role,old,new,label):
 s=texts[role];count=s.count(old);assert count>0 and old!=new,(role,label,count)
 edits[role].append(dict(label=label,old=old,new=new,count=count));texts[role]=s.replace(old,new)
def before_def(role,source,label):
 s=texts[role];index=s.index('\ndef ');replace(role,s[:index],s[:index]+source,label)
def inverse(s,rows):
 for r in reversed(rows):
  assert s.count(r['new'])==r['count'],r['label'];s=s.replace(r['new'],r['old'])
 return s

PHASES=('run_build','declaration_admission','before_build_link','before_metadata_objects','before_metadata_executable','before_metadata_dependencies','run_finally')
POINTS=('declaration_enter','declaration_return','commands_constructed','execute_enter','execute_return','environment_enter','environment_return','complete_input_enter','specs1_enter','specs1_return','owned1_enter','owned1_return','current_before_enter','current_before_return','verify_graph_enter','verify_graph_return','snapshot_enter','snapshot_return','trace_digest_enter','trace_digest_return','specs2_enter','specs2_return','current_after_enter','current_after_return','owned2_enter','owned2_return','graph2_enter','graph2_return','bindings_enter','bindings_return','lengths_enter','lengths_return','complete_input_return','archive_resources_return','normal_pre_inventory')
CONTRACT=dict(schema='AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_OUTPUT_CONTRACT_V1',relative_path='build_memory_diagnostic.jsonl',row_schema='AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_ROW_V1',phases=list(PHASES),points=list(POINTS),max_rows=256,max_line_bytes_including_newline=4096,max_bytes=1048576,open_flags='O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW',mode_octal='0600',one_parent_descriptor=True,write_only=True,read_during_active_input_audit=False,last_normal_marker='normal_pre_inventory',close_before_original_OUT_inventory=True,no_append_after_close=True,ru_maxrss_semantics='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK',diagnostic_runtime_dependency_provenance='FUTURE_ROOT_SOURCE_BIND_AND_PRELAUNCH_ENVIRONMENT_WITNESS_REQUIRED',actual_runtime_pin=None,current_RSS_qualified=False,whole_INPUT_build_native_or_science_qualified=False)
COMMON='\nBUILD_MEMORY_DIAGNOSTIC_CONTRACT = '+repr(CONTRACT)+'''\n
def memory_diagnostic_declaration(d):
    expected=BUILD_MEMORY_DIAGNOSTIC_CONTRACT
    actual=d.get('build_memory_diagnostic_output_contract')
    if json.dumps(actual,sort_keys=True,allow_nan=False)!=json.dumps(expected,sort_keys=True,allow_nan=False):
        raise ValueError('exact declared write-only bounded output diagnostic contract required')
    forecast=d['complete_archive_forecast']
    fields=('copied_SOURCE_metadata_bound','trim_whole_component_metadata_and_trace_bound','full_graph_and_creation_trace_bound','combined_runtime_and_link_transient_bound','complete_raw_tools_and_closeout_bound','diagnostic_max_bytes','total_bound')
    if any(type(forecast[k]) is not int or forecast[k]<0 for k in fields):
        raise ValueError('exact integer complete forecast and diagnostic reservation required')
    if forecast['diagnostic_max_bytes']!=expected['max_bytes'] or forecast['total_bound']!=sum(forecast[k] for k in fields[:-1]) or forecast['total_bound']>=2*2**30:
        raise ValueError('all original complete forecast components plus diagnostic remain below original 2GiB')
    return actual
'''

LOGGER='''
FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN = None
_BUILD_MEMORY_JOURNAL = None

class BuildMemoryDiagnosticJournal:
    """Output-only parent high-water markers; no input reads or subprocess."""
    def __init__(self):
        if sys.platform!='darwin':raise ValueError('Darwin native-byte ru_maxrss semantics required')
        self.fd=None;self.rows=0;self.bytes=0;self.last_time=None;self.last_high_water=None;self.deferred=None
        self.fd=os.open(OUT/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:
            s=os.fstat(self.fd)
            if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size!=0 or stat.S_IMODE(s.st_mode)!=0o600:
                raise ValueError('fresh ordinary single-link private diagnostic descriptor required')
        except BaseException:
            os.close(self.fd);self.fd=None;raise
    def point(self,phase,point):
        if self.fd is None:raise ValueError('diagnostic was closed; no post-inventory append permitted')
        contract=BUILD_MEMORY_DIAGNOSTIC_CONTRACT
        if phase not in contract['phases'] or point not in contract['points']:raise ValueError('fixed diagnostic phase/point required')
        now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if type(peak) is not int or peak<0 or not math.isfinite(now):raise ValueError('exact native historical ru_maxrss bytes and finite monotonic clock required')
        if self.last_time is not None and (now<self.last_time or peak<self.last_high_water):raise ValueError('monotonic clock and historical high-water must not decrease')
        row=dict(schema=contract['row_schema'],sequence_exact_int=self.rows,pid_exact_int=os.getpid(),phase_fixed_enum=phase,point_fixed_enum=point,monotonic_seconds_finite=now,self_ru_maxrss_native_bytes_exact_int=peak,ru_maxrss_semantics=contract['ru_maxrss_semantics'])
        payload=(json.dumps(row,separators=(',',':'),allow_nan=False)+'\\n').encode('ascii')
        if self.rows>=contract['max_rows'] or len(payload)>contract['max_line_bytes_including_newline'] or self.bytes+len(payload)>contract['max_bytes']:
            raise ValueError('fixed output diagnostic byte/line/row bounds exceeded')
        offset=0
        while offset<len(payload):
            written=os.write(self.fd,payload[offset:])
            if type(written) is not int or written<=0:raise OSError('diagnostic short write without progress')
            offset+=written
        os.fsync(self.fd)
        self.rows+=1;self.bytes+=len(payload);self.last_time=now;self.last_high_water=peak
    def close(self):
        fd=self.fd;self.fd=None
        if fd is not None:os.close(fd)
        if self.deferred is not None:raise self.deferred

def memory_diagnostic_point(phase,point):
    journal=_BUILD_MEMORY_JOURNAL
    if journal is None:return
    if journal.deferred is not None:return
    try:journal.point(phase,point)
    except BaseException as error:
        if phase!='run_finally':raise
        # Defer only this diagnostic failure until ALL original finally gates
        # have completed or raised; close() then raises it, preserving context.
        journal.deferred=error
'''

READER='''
def memory_diagnostic_pin(path):
    path=Path(path);s=path.lstat()
    ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if path.is_symlink() or not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('ordinary single-link diagnostic required')
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    s=path.lstat();after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if after!=ident:raise ValueError('full EOF diagnostic changed during pin')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=ident[4],identity=ident)

def memory_diagnostic_rows(path,expected_pid=None,success=False):
    contract=BUILD_MEMORY_DIAGNOSTIC_CONTRACT;path=Path(path)
    if not os.path.lexists(path):
        if success:raise ValueError('successful build requires complete saved diagnostic')
        return dict(parse_status='ABSENT',journal_if_present=None,saved_complete_rows=[],trailing_fragment=None,final_marker_observed=False,diagnostic_credit=False)
    before=memory_diagnostic_pin(path)
    output=dict(parse_status='INVALID_DIAGNOSTIC',journal_if_present=before,saved_complete_rows=[],trailing_fragment=None,final_marker_observed=False,diagnostic_credit=False,fsync_or_close_proved_by_rows_alone=False,ru_maxrss_is_original_guard_peak=False)
    try:
        if before['size_bytes']>contract['max_bytes']:raise ValueError('diagnostic exceeds reserved byte bound')
        with path.open('rb') as stream:raw=stream.read(contract['max_bytes']+1)
        if len(raw)!=before['size_bytes']:raise ValueError('diagnostic bounded read differs from full pin')
        pieces=raw.split(b'\\n');fragment=pieces.pop()
        if fragment:
            output['trailing_fragment']=dict(size_bytes=len(fragment),sha256=hashlib.sha256(fragment).hexdigest())
        if len(pieces)>contract['max_rows']:raise ValueError('diagnostic row count exceeds bound')
        rows=output['saved_complete_rows'];last_time=None;last_high_water=None;parent=expected_pid
        keys={'schema','sequence_exact_int','pid_exact_int','phase_fixed_enum','point_fixed_enum','monotonic_seconds_finite','self_ru_maxrss_native_bytes_exact_int','ru_maxrss_semantics'}
        def pairs(items):
            out={}
            for key,value in items:
                if key in out:raise ValueError('duplicate diagnostic JSON key')
                out[key]=value
            return out
        def bad_constant(value):raise ValueError('nonfinite diagnostic JSON constant '+value)
        for index,line in enumerate(pieces):
            if len(line)+1>contract['max_line_bytes_including_newline']:raise ValueError('diagnostic line exceeds bound')
            row=json.loads(line.decode('ascii'),object_pairs_hook=pairs,parse_constant=bad_constant)
            if type(row) is not dict or set(row)!=keys:raise ValueError('exact eight diagnostic fields required')
            if row['schema']!=contract['row_schema'] or row['ru_maxrss_semantics']!=contract['ru_maxrss_semantics']:raise ValueError('diagnostic schema/native-byte semantics changed')
            if type(row['sequence_exact_int']) is not int or row['sequence_exact_int']!=index:raise ValueError('strict consecutive diagnostic sequence')
            pid=row['pid_exact_int'];peak=row['self_ru_maxrss_native_bytes_exact_int'];clock=row['monotonic_seconds_finite']
            if type(pid) is not int or pid<=0 or type(peak) is not int or peak<0 or type(clock) not in (int,float) or not math.isfinite(clock):raise ValueError('strict PID/high-water integers and finite clock')
            if parent is None:parent=pid
            if type(parent) is not int or parent<=0 or pid!=parent:raise ValueError('single actual canonical parent PID required')
            if row['phase_fixed_enum'] not in contract['phases'] or row['point_fixed_enum'] not in contract['points']:raise ValueError('fixed phase/point required')
            if last_time is not None and (clock<last_time or peak<last_high_water):raise ValueError('diagnostic clock/high-water decreased')
            rows.append(row);last_time=clock;last_high_water=peak
        if fragment and len(fragment)>=contract['max_line_bytes_including_newline']:raise ValueError('trailing fragment exceeds line bound')
        output['parse_status']='PARTIAL_TRAILING_FRAGMENT' if fragment else 'COMPLETE_LINES'
        output['final_marker_observed']=bool(rows and rows[-1]['phase_fixed_enum']=='run_build' and rows[-1]['point_fixed_enum']=='normal_pre_inventory')
        if success and (fragment or not rows or not output['final_marker_observed'] or any(r['point_fixed_enum']=='normal_pre_inventory' for r in rows[:-1])):
            raise ValueError('successful diagnostic requires unique final pre-inventory marker and no fragment')
    except BaseException as error:
        output['parse_status']='INVALID_DIAGNOSTIC';output['validation_error']=repr(error)
        if success:raise
    after=memory_diagnostic_pin(path)
    if after!=before:raise ValueError('saved diagnostic changed during bounded postclose read')
    return output
'''

ENV_BINDER='''
def diagnostic_resource_environment_witness(path,sha256):
    # Root creates this genuine small META witness before SOURCE binding.
    # It is a SOURCE/prelaunch dependency, never an active graph-audit input.
    wanted=source_pin(require(path,sha256));body=read(wanted['path'])
    if body.get('schema')!='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1' or body.get('diagnostic_dependency_verified') is not True or body.get('source_only') is not True or body.get('platform')!='darwin':raise ValueError('actual independent diagnostic environment witness required')
    for field in ('actual_python_fullpin','actual_resource_module_fullpin','actual_environment_tool_terminal_fullpin'):
        q=helper_Q_fullpin(body[field]);actual=source_pin(require(q['path'],q['sha256']))
        if actual!=q:raise ValueError('diagnostic environment witness complete fullpin differs')
    if body['actual_python_fullpin']['path']!='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12':raise ValueError('unchanged exact Python endpoint')
    terminal=read(body['actual_environment_tool_terminal_fullpin']['path']);tr=terminal['terminal_tool_return']
    if terminal.get('observed_terminal') is not True or terminal.get('closed') is not True or terminal.get('session_repolled_after_close',False) is not False or type(tr.get('exit_code')) is not int or tr['exit_code']!=0 or 'session_id' in tr:raise ValueError('actual diagnostic environment closed terminal required')
    observed=json.loads(tr['output'])
    for field in ('actual_python_fullpin','actual_resource_module_fullpin','self_ru_maxrss_native_bytes_observed','ru_maxrss_semantics','platform'):
        if json.dumps(observed[field],sort_keys=True,allow_nan=False)!=json.dumps(body[field],sort_keys=True,allow_nan=False):raise ValueError('actual environment terminal output and witness differ')
    if type(body.get('self_ru_maxrss_native_bytes_observed')) is not int or body['self_ru_maxrss_native_bytes_observed']<0 or body.get('ru_maxrss_semantics')!=BUILD_MEMORY_DIAGNOSTIC_CONTRACT['ru_maxrss_semantics']:raise ValueError('actual raw native-byte diagnostic observation required')
    if any(body.get(k) is not False for k in ('whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified')):raise ValueError('diagnostic dependency cannot grant business or science')
    return wanted
'''

planpin=pin(PLAN);assert planpin['sha256']==PLAN_SHA;plan=json.loads(PLAN.read_text())
out=Path(tempfile.mkdtemp(prefix='axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_',dir='/private/tmp'))
(out/'ORIGINAL_PARENT_SOURCE').mkdir();(out/'utilities').mkdir();(out/'host_and_postclose_templates').mkdir();(out/'SOURCE_AND_ACTUAL_SMALL_META').mkdir()
parents={role:path.read_text() for role,path in ROLES.items()};parentpins={role:pin(path) for role,path in ROLES.items()}
texts=dict(parents);edits={role:[] for role in ROLES}
for role in ROLES:
 (out/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).write_text(parents[role])
 for old,new in [('v25-poststage-temporaries','v25-memory-observation'),('v25_poststage_temporaries','v25_memory_observation')]:
  if old in texts[role]:replace(role,old,new,'fresh_namespace_'+old)
 (out/Path(NAMES[role])).parent.mkdir(parents=True,exist_ok=True)
for role in ROLES:
 if role in ('canonical','prepare_host','prepare_writer','build_host','build_writer','prepare_binder','build_binder','Root_poststage_Source_META_contract.py','Root_source_installer.py','Root_prelaunch_checker.py'):
  before_def(role,COMMON,'fixed_bounded_output_diagnostic_declaration_contract')
for role in ('prepare_host','build_host'):
 replace(role,'import importlib.util','import hashlib\nimport math\nimport stat\nimport importlib.util','bounded_reader_standard_library_imports')
 before_def(role,READER,'bounded_saved_diagnostic_reader')
for role in ('build_writer',):before_def(role,READER,'bounded_saved_diagnostic_reader')
role='canonical'
replace(role,'import gc','import gc\nimport resource','Darwin_resource_dependency_import_outside_active_audit')
before_def(role,LOGGER,'parent_only_exclusive_output_journal_and_deferred_finally_failure')
replace(role,'    require_ready();started=time.monotonic();d=declaration_admission(expected,prep_sha256=prep_sha256);b,h,full,c=modules()',
'''    global _BUILD_MEMORY_JOURNAL
    require_ready();started=time.monotonic()
    if _BUILD_MEMORY_JOURNAL is not None:raise ValueError('exclusive parent diagnostic lifecycle')
    journal=BuildMemoryDiagnosticJournal();_BUILD_MEMORY_JOURNAL=journal
    try:
        memory_diagnostic_point('run_build','declaration_enter')
        d=declaration_admission(expected,prep_sha256=prep_sha256)
        memory_diagnostic_point('run_build','declaration_return')
        b,h,full,c=modules()''','outer_diagnostic_initialization_before_original_declaration')
# Indent the exact remaining old run_build body within the new descriptor scope.
s=parents[role];tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='run_build')
segment=ast.get_source_segment(s,node)
start=segment.index("    resources=resources_for(d['resource_roots'],c.ResourceFailure);resources.check()")
tail=segment[start:];newtail='\n'.join('    '+line if line else line for line in tail.split('\n'))+'''\n    finally:
        _BUILD_MEMORY_JOURNAL=None
        journal.close()'''
replace(role,tail,newtail,'whole_original_run_build_body_nested_under_descriptor_finally')
replace(role,'            commands=stage_commands(d,expected)','            commands=stage_commands(d,expected)\n            memory_diagnostic_point(\'run_build\',\'commands_constructed\')','commands_boundary')
replace(role,'                    runner.execute(OUT/directory,stem,command,STAGE_WALL)',"                    memory_diagnostic_point('before_'+label.replace('/','_'),'execute_enter')\n                    runner.execute(OUT/directory,stem,command,STAGE_WALL)\n                    memory_diagnostic_point('before_'+label.replace('/','_'),'execute_return')",'four_original_execute_boundaries')
replace(role,"            runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL,'AXMAT-COMBINED-RUNTIME-LINK-AUDITED')","            memory_diagnostic_point('run_build','execute_enter')\n            runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL,'AXMAT-COMBINED-RUNTIME-LINK-AUDITED')\n            memory_diagnostic_point('run_build','execute_return')",'original_audit_execute_boundaries')
replace(role,"                result.update(elapsed_seconds=elapsed,archive_bytes_before_closeout=size,resources=snapshot)","                result.update(elapsed_seconds=elapsed,archive_bytes_before_closeout=size,resources=snapshot)\n                memory_diagnostic_point('run_finally','archive_resources_return')",'all_original_finally_gates_before_deferred_diagnostic_failure')
replace(role,"        complete=inventory(OUT);write_new(OUT/'seal.json',dict(schema=PREFIX+'_BUILD_SEAL_V1',**complete))","        if journal.deferred is not None:raise journal.deferred\n        memory_diagnostic_point('run_build','normal_pre_inventory')\n        journal.close();_BUILD_MEMORY_JOURNAL=None\n        complete=inventory(OUT);write_new(OUT/'seal.json',dict(schema=PREFIX+'_BUILD_SEAL_V1',**complete))",'final_marker_close_before_original_inventory_no_later_append')
replace(role,'def environment(d,require_build_interpreter=True,phase=\'environment\'):\n',"def environment(d,require_build_interpreter=True,phase='environment'):\n    memory_diagnostic_point(phase,'environment_enter')\n",'environment_enter')
replace(role,"    resources_for(d['resource_roots']).check()\n    return observed","    resources_for(d['resource_roots']).check()\n    memory_diagnostic_point(phase,'environment_return')\n    return observed",'environment_return_after_original_gates')
replace(role,'def complete_input_phase(d,phase,require_build_interpreter):\n','def complete_input_phase(d,phase,require_build_interpreter):\n    memory_diagnostic_point(phase,\'complete_input_enter\')\n','complete_input_enter')
anchors=[
("    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded;gc.collect()","    memory_diagnostic_point(phase,'specs1_enter')\n    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded;gc.collect()\n    memory_diagnostic_point(phase,'specs1_return')"),
("    current_new_owned_paths(d)\n    before=current_input_predicates(helpers,specs,require_build_interpreter)","    memory_diagnostic_point(phase,'owned1_enter')\n    current_new_owned_paths(d)\n    memory_diagnostic_point(phase,'owned1_return')\n    memory_diagnostic_point(phase,'current_before_enter')\n    before=current_input_predicates(helpers,specs,require_build_interpreter)\n    memory_diagnostic_point(phase,'current_before_return')"),
("    with g.ReadOpenAudit()as audit:\n        verified=g.verify_graph(d['input_graph']['path'],expected_sha256=d['input_graph']['sha256'],phase=phase)","    memory_diagnostic_point(phase,'verify_graph_enter')\n    with g.ReadOpenAudit()as audit:\n        verified=g.verify_graph(d['input_graph']['path'],expected_sha256=d['input_graph']['sha256'],phase=phase)\n    memory_diagnostic_point(phase,'verify_graph_return')"),
("    trace=audit.snapshot(_consume=True);graph_path=d['input_graph']['path']","    memory_diagnostic_point(phase,'snapshot_enter')\n    trace=audit.snapshot(_consume=True);graph_path=d['input_graph']['path']\n    memory_diagnostic_point(phase,'snapshot_return')\n    memory_diagnostic_point(phase,'trace_digest_enter')"),
("    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()","    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()\n    memory_diagnostic_point(phase,'trace_digest_return')"),
("    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded\n    after=current_input_predicates(helpers,specs,require_build_interpreter)\n    current_new_owned_paths(d)","    memory_diagnostic_point(phase,'specs2_enter')\n    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded\n    memory_diagnostic_point(phase,'specs2_return')\n    memory_diagnostic_point(phase,'current_after_enter')\n    after=current_input_predicates(helpers,specs,require_build_interpreter)\n    memory_diagnostic_point(phase,'current_after_return')\n    memory_diagnostic_point(phase,'owned2_enter')\n    current_new_owned_paths(d)\n    memory_diagnostic_point(phase,'owned2_return')"),
("    graph=g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])\n    expected_snapshot=", "    memory_diagnostic_point(phase,'graph2_enter')\n    graph=g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])\n    memory_diagnostic_point(phase,'graph2_return')\n    memory_diagnostic_point(phase,'bindings_enter')\n    expected_snapshot="),
("    del files,complete_aliases,paths,expected_snapshot\n    pins=","    del files,complete_aliases,paths,expected_snapshot\n    memory_diagnostic_point(phase,'bindings_return')\n    memory_diagnostic_point(phase,'lengths_enter')\n    pins="),
("    del graph,pins,length_specs;gc.collect()\n    return dict(phase=phase","    del graph,pins,length_specs;gc.collect()\n    memory_diagnostic_point(phase,'lengths_return')\n    memory_diagnostic_point(phase,'complete_input_return')\n    return dict(phase=phase")]
for i,(old,new) in enumerate(anchors):replace(role,old,new,'complete_input_atomic_boundary_'+str(i))
replace(role,'        complete_raw_tools_and_closeout_bound=128*2**20,','        complete_raw_tools_and_closeout_bound=128*2**20,\n        diagnostic_max_bytes=BUILD_MEMORY_DIAGNOSTIC_CONTRACT[\'max_bytes\'],','PREP_forecast_explicit_diagnostic_reservation')
replace(role,'total_bound=16*input_metadata_bytes+32*2**20+256*2**20+2*linked_input_bytes+128*2**20+trim_metadata_bound,','total_bound=16*input_metadata_bytes+32*2**20+256*2**20+2*linked_input_bytes+128*2**20+trim_metadata_bound+BUILD_MEMORY_DIAGNOSTIC_CONTRACT[\'max_bytes\'],','PREP_forecast_total_includes_diagnostic')
replace(role,'        complete_archive_forecast=forecast,resources_before=before,','        build_memory_diagnostic_output_contract=BUILD_MEMORY_DIAGNOSTIC_CONTRACT,\n        complete_archive_forecast=forecast,resources_before=before,','PREP_fixed_output_contract_not_input_or_actual_fact')
replace(role,"    if d['complete_archive_forecast']['total_bound']>=RESERVE:raise ValueError('unchanged reserve exceeded')","    memory_diagnostic_declaration(d)\n    if d['complete_archive_forecast']['total_bound']>=RESERVE:raise ValueError('unchanged reserve exceeded')",'declaration_exact_diagnostic_contract_and_complete_forecast')
replace(role,'    require_ready();started=time.monotonic()','    require_ready();started=time.monotonic()', 'unreachable') if False else None
# Only a literal SOURCE-bound environment witness is tested at readiness;
# its actual reads belong to Root stdlib binding/prelaunch, not active audits.
replace(role,"    if DRAFT_STATUS !=", "    if FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN is None:raise ValueError('UNREADY diagnostic resource environment witness')\n    if DRAFT_STATUS !=",'future_actual_diagnostic_dependency_required_before_ready')

for role in ('prepare_host','build_host'):
 replace(role,"declaration=OUT/'declaration.json';d=json.loads(declaration.read_text())","declaration=OUT/'declaration.json';d=json.loads(declaration.read_text());memory_diagnostic_declaration(d)",'host_exact_diagnostic_declaration')
if True:
 role='prepare_host';replace(role,'        value=dict(schema=',"        if os.path.lexists(OUT/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']):raise ValueError('BUILD-only diagnostic must remain absent after PREP')\n        value=dict(schema=",'PREP_diagnostic_absent')
 role='prepare_writer';replace(role,"    d=json.loads((O/'declaration.json').read_text())","    d=json.loads((O/'declaration.json').read_text());memory_diagnostic_declaration(d)\n    if os.path.lexists(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']):raise ValueError('BUILD-only diagnostic absent after PREP')",'PREP_writer_fixed_contract_and_absence')
 role='build_host';replace(role,"'raw_metadata_receipt.json','audit/binary_identity.json'","'raw_metadata_receipt.json','build_memory_diagnostic.jsonl','audit/binary_identity.json'",'BUILD_absent_outputs_include_new_journal')
 replace(role,'        value=dict(schema=',"        diagnostic=memory_diagnostic_rows(OUT/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],json.loads((OUT/'execution_claim.json').read_text())['parent_pid'],success=True)\n        if diagnostic['journal_if_present']['sha256']!=seal['files'][BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']]:raise ValueError('saved diagnostic matches whole OUT seal')\n        value=dict(actual_build_memory_diagnostic=diagnostic,schema=",'host_bounded_postclosed_diagnostic_fullpin_and_seal')
 role='build_writer';replace(role,"    command=[d['python_command'],str(FACTORY),'run-build'","    memory_diagnostic_declaration(d)\n    command=[d['python_command'],str(FACTORY),'run-build'",'success_fixed_diagnostic_declaration')
 replace(role,"    if result['corrected_runtime']!=short(O/'runtime/Dragon'):","    diagnostic=memory_diagnostic_rows(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],read(O/'execution_claim.json')['parent_pid'],success=True)\n    if h['actual_build_memory_diagnostic']!=diagnostic or diagnostic['journal_if_present']['sha256']!=seal['files'][BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']]:raise ValueError('actual host/full OUT sealed diagnostic coupling')\n    if result['corrected_runtime']!=short(O/'runtime/Dragon'):",'success_bounded_diagnostic_coupling')
 replace(role,'    summary=dict(schema=',"    diagnostic=memory_diagnostic_rows(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],success=False)\n    summary=dict(actual_build_memory_diagnostic=diagnostic,schema=",'failure_or_success_actual_diagnostic_preserved_no_reconstructed_rows')

for role in ('prepare_binder','build_binder'):
 before_def(role,ENV_BINDER,'Root_only_actual_environment_witness_SOURCE_binding')
 replace(role,'args=parser.parse_args()' if role=='prepare_binder' else 'args=a.parse_args()',("parser.add_argument('--actual-diagnostic-resource-environment-witness',required=True);parser.add_argument('--actual-diagnostic-resource-environment-witness-sha256',required=True);args=parser.parse_args()" if role=='prepare_binder' else "a.add_argument('--actual-diagnostic-resource-environment-witness',required=True);a.add_argument('--actual-diagnostic-resource-environment-witness-sha256',required=True);args=a.parse_args()"),'mandatory_actual_diagnostic_environment_witness_CLI')
 replace(role,'    deps=helper_Q_admission()',"    resource_environment_pin=diagnostic_resource_environment_witness(args.actual_diagnostic_resource_environment_witness,args.actual_diagnostic_resource_environment_witness_sha256)\n    deps=helper_Q_admission()",'actual_environment_witness_before_Source_binding')
 if role=='prepare_binder':
  replace(role,"    bound={'canonical':text};canonical_sha=hashlib.sha256(text.encode()).hexdigest()","    text=source_replace(text,edits['canonical'],'FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN = None','FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN = '+repr(resource_environment_pin),'actual_diagnostic_dependency_fullpin')\n    bound={'canonical':text};canonical_sha=hashlib.sha256(text.encode()).hexdigest()",'actual_canonical_environment_literal_binding')
  replace(role,"actual_Q=qpin,canonical=source_pin", "actual_diagnostic_resource_environment_witness=resource_environment_pin,actual_Q=qpin,canonical=source_pin",'actual_bound_environment_stdout_fullpin')
  replace(role,"    (output/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json').write_bytes(ACTUAL_HELPER_Q_PATH.read_bytes())","    (output/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json').write_bytes(ACTUAL_HELPER_Q_PATH.read_bytes())\n    (output/'ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json').write_bytes(Path(resource_environment_pin['path']).read_bytes())\n    resource_environment_body=read(resource_environment_pin['path'])\n    (output/'ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_TOOL_TERMINAL.byte_exact.json').write_bytes(Path(resource_environment_body['actual_environment_tool_terminal_fullpin']['path']).read_bytes())",'complete_bound_environment_META_and_true_terminal_D_owner_copies')

 else:
  replace(role,"    cp=source_pin(require(TARGET,args.actual_canonical_sha256));", "    declaration_body=read(outrefs['declaration']['path']);memory_diagnostic_declaration(declaration_body)\n    if os.path.lexists(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']):raise ValueError('new journal absent before genuine BUILD')\n    cp=source_pin(require(TARGET,args.actual_canonical_sha256));",'BUILD_binding_PREP_diagnostic_declaration_and_absence')
  replace(role,"    for k in BUSINESS:helper_Q_check", "    helper_Q_check(helper_Q_fullpin(ast.literal_eval(assignments['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN']))==resource_environment_pin,'same actual SOURCE/prelaunch environment witness')\n    for k in BUSINESS:helper_Q_check",'same_environment_witness_in_actual_canonical')

for role in ('Root_source_installer.py','Root_prelaunch_checker.py'):
 replace(role,"'raw_metadata_receipt.json','audit/binary_identity.json'","'raw_metadata_receipt.json','build_memory_diagnostic.jsonl','audit/binary_identity.json'",'utility_BUILD_fresh_outputs_include_journal')
role='Root_poststage_Source_META_contract.py'
# New Source qualifications are CLI-pinned, never reused old actual successes.
for name,old in [('AUTHOR',"Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')"),('AUTHOR_SHA',"'9085afa282c04c927118323d101c9d23ffce51ebcdd2f2ddda7e4b8d0500d6bd'"),('AUTHOR_PEER',"Path('/private/tmp/axmat_V25_poststage_temporaries_complete_Source_independent_V2_20261010')"),('AUTHOR_PEER_SHA',"'6e1627dae76811f4f2c845a10520c5fb5decee9adcbd0b5f03359c800b4b4367'"),('AUTHOR_PEER_SEAL',"Path(str(AUTHOR_PEER)+'_seal_receipt/ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')"),('AUTHOR_PEER_SEAL_SHA',"'64cfd24fbcb261e24e889d4254719bf6c21c5a4dc1580d658db2eb3dbd4783e3'"),('PREP_BOUND',"Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')"),('PREP_BOUND_SHA',"'531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef'"),('PREP_BINDING',"B/'Root_actual_V25_poststage_PREP_Source_binding_tool_terminal_return.json'"),('PREP_BINDING_SHA',"'c3cb0eb7ec35e33f83f64bd0f2f2adcddb35eb4112fab4a686b7353345cb39c2'")]:
 anchor=name+'='+old
 # Namespace replacement has changed old literal spelling, too.
 anchor=anchor.replace('v25_poststage_temporaries','v25_memory_observation')
 replace(role,anchor,name+'=None  # UNREADY: actual new Source proof required','future_actual_'+name)
replace(role,'def author_facts():\n','def author_facts():\n    if any(v is None for v in (AUTHOR,AUTHOR_SHA,AUTHOR_PEER,AUTHOR_PEER_SHA,AUTHOR_PEER_SEAL,AUTHOR_PEER_SEAL_SHA)):raise ValueError(\'UNREADY new complete Source author/peer binding\')\n','strict_no_old_author_admission')
replace(role,"'INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1','PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'","'INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1','PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'",'new_author_peer_scope')
replace(role,"r['qualified_complete_Source_manifest_pin']==ap and r['check_count']==658","r['qualified_complete_Source_manifest_pin']==ap and type(r['check_count']) is int and r['check_count']==len(r['checks']) and r['check_count']>0",'new_actual_peer_count_not_old658')
replace(role,"'INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1','PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'",'"INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1","PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION"','new_combined_utility_peer_scope')
replace(role,"    expected={name:uv['files'][name] for name in UTILITY_ROLES}","    expected={name:uv['files']['utilities/'+name] for name in UTILITY_ROLES}",'complete_utility_subdir_actualpins')
replace(role,"    um,up,uv=package(Path(root)/'MANIFEST.json',a.utility_manifest_sha256)","    root=Path(root);package_root=root.parent if root.name=='utilities' else root\n    um,up,uv=package(package_root/'MANIFEST.json',a.utility_manifest_sha256)",'utility_manifest_parent_matches_combined_packet')
before_def(role,'''
def memory_resource_environment_binding(canonical_path):
    q=literal_values(canonical_path)['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN']
    q=exact(q);body,actual=read(q['path'],q['sha256']);assert q==actual
    assert body['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1' and body['source_only'] is True and body['platform']=='darwin' and body['diagnostic_dependency_verified'] is True
    for field in ('actual_python_fullpin','actual_resource_module_fullpin','actual_environment_tool_terminal_fullpin'):exact(body[field])
    assert body['actual_python_fullpin']['path']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
    observed,tp,tr=terminal(body['actual_environment_tool_terminal_fullpin']['path'],body['actual_environment_tool_terminal_fullpin']['sha256']);assert tp==body['actual_environment_tool_terminal_fullpin']
    actual_observation=json.loads(tr['output'])
    for field in ('actual_python_fullpin','actual_resource_module_fullpin','self_ru_maxrss_native_bytes_observed','ru_maxrss_semantics','platform'):assert json.dumps(actual_observation[field],sort_keys=True,allow_nan=False)==json.dumps(body[field],sort_keys=True,allow_nan=False)
    assert type(body['self_ru_maxrss_native_bytes_observed']) is int and body['self_ru_maxrss_native_bytes_observed']>=0 and body['ru_maxrss_semantics']==BUILD_MEMORY_DIAGNOSTIC_CONTRACT['ru_maxrss_semantics']
    assert all(body[k] is False for k in ('whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified'))
    return q
''','Root_prelaunch_full_environment_witness_and_terminal_coupling_outside_active_audit')
replace(role,"    return dict(manifest=bp,view=bv,roles=roles,binding_terminal=bip,peer=pp)","    diagnostic_environment=memory_resource_environment_binding(roles['canonical']['path'] if phase=='PREP' else C)\n    if phase=='PREP':assert actual['actual_diagnostic_resource_environment_witness']==diagnostic_environment\n    return dict(manifest=bp,view=bv,roles=roles,binding_terminal=bip,peer=pp,diagnostic_resource_environment_witness=diagnostic_environment)",'full_future_bound_and_prelaunch_environment_evidence')

replace(role,"r['qualified_complete_utility_manifest_pin']==up","r['qualified_complete_Source_manifest_pin']==up",'new_combined_utility_manifest_contract')
replace(role,"r['qualified_role_Source_pins']==expected and set(expected)==set(UTILITY_ROLES)","r['qualified_utility_Source_pins']==expected and set(expected)==set(UTILITY_ROLES)",'new_combined_utility_roles_contract')
old="        assert root==PREP_BOUND and bp['sha256']==PREP_BOUND_SHA and bip['path']==str(PREP_BINDING) and bip['sha256']==PREP_BINDING_SHA and tr['chunk_id']=='91304c'"
replace(role,old,"        if PREP_BOUND is None or PREP_BOUND_SHA is None or PREP_BINDING is None or PREP_BINDING_SHA is None:raise ValueError('UNREADY new actual bound PREP Source pins')\n        assert root==PREP_BOUND and bp['sha256']==PREP_BOUND_SHA and bip['path']==str(PREP_BINDING) and bip['sha256']==PREP_BINDING_SHA",'new_actual_PREP_Source_binding_no_oldchunk')
replace(role,"        assert (roles['canonical']['sha256'],roles['prepare_host']['sha256'],roles['prepare_writer']['sha256'])==('6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649','9475d42436aa242e834d8388ee018d3217f8b0bf2326d2384258b3c50b610e0c','e5144866b187ead27dab8b3441d0dcce9dd2c53f94429d22300daec0873d53f0')","        assert all(type(q['sha256']) is str and len(q['sha256'])==64 for q in roles.values())",'complete_new_roles_coupled_to_new_actual_binder_and_peer')
replace(role,"    assert pin(C)['sha256']=='6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649'","    declaration,_=read(O/'declaration.json');memory_diagnostic_declaration(declaration)\n    assert not os.path.lexists(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'])\n    assert pin(C)==exact(ns['canonical_factory'])",'new_PREP_canonical_exact_namespace_pin_and_diagnostic_absence')
replace(role,'def request_main():\n',"def request_main():\n    global AUTHOR,AUTHOR_SHA,AUTHOR_PEER,AUTHOR_PEER_SHA,AUTHOR_PEER_SEAL,AUTHOR_PEER_SEAL_SHA,PREP_BOUND,PREP_BOUND_SHA,PREP_BINDING,PREP_BINDING_SHA\n",'future_actual_Source_roles_CLI_globals')
replace(role,"    a=ap.parse_args();out=Path(a.fresh_TMP_output);", "    for key in ('author-manifest','author-manifest-sha256','author-peer-manifest','author-peer-manifest-sha256','author-peer-seal','author-peer-seal-sha256'):ap.add_argument('--'+key,required=True)\n    a=ap.parse_args()\n    AUTHOR=Path(a.author_manifest).parent;AUTHOR_SHA=a.author_manifest_sha256;AUTHOR_PEER=Path(a.author_peer_manifest).parent;AUTHOR_PEER_SHA=a.author_peer_manifest_sha256;AUTHOR_PEER_SEAL=Path(a.author_peer_seal);AUTHOR_PEER_SEAL_SHA=a.author_peer_seal_sha256\n    if a.phase=='PREP':PREP_BOUND=Path(a.bound_manifest).parent;PREP_BOUND_SHA=a.bound_manifest_sha256;PREP_BINDING=Path(a.binding_terminal);PREP_BINDING_SHA=a.binding_terminal_sha256\n    out=Path(a.fresh_TMP_output);",'new_author_and_PREP_Source_metadata_CLI_binding')
replace(role,"    d,p=read(path,sha);assert d['schema']==REQUEST_SCHEMA", "    global AUTHOR,AUTHOR_SHA,AUTHOR_PEER,AUTHOR_PEER_SHA,AUTHOR_PEER_SEAL,AUTHOR_PEER_SEAL_SHA,PREP_BOUND,PREP_BOUND_SHA,PREP_BINDING,PREP_BINDING_SHA\n    d,p=read(path,sha)\n    AUTHOR=Path(d['author']['manifest']['path']).parent;AUTHOR_SHA=d['author']['manifest']['sha256'];AUTHOR_PEER=Path(d['author']['peer']['manifest']['path']).parent;AUTHOR_PEER_SHA=d['author']['peer']['manifest']['sha256'];AUTHOR_PEER_SEAL=Path(d['author']['peer']['seal']['path']);AUTHOR_PEER_SEAL_SHA=d['author']['peer']['seal']['sha256']\n    if phase=='PREP':PREP_BOUND=Path(d['bound']['manifest']['path']).parent;PREP_BOUND_SHA=d['bound']['manifest']['sha256'];PREP_BINDING=Path(d['bound']['binding_terminal']['path']);PREP_BINDING_SHA=d['bound']['binding_terminal']['sha256']\n    assert d['schema']==REQUEST_SCHEMA",'installed_request_revalidates_actual_dynamic_Sourceproofs')
replace(role,"    expected=contract()['seven_author_role_Source_pins']","    expected={name:pin(AUTHOR/rel) for name,rel in "+repr({k:NAMES[k] for k in ('canonical','prepare_host','prepare_writer','build_host','build_writer','prepare_binder','build_binder')})+".items()}",'new_author_actual_roles_no_immutable_self_pin_cycle')

for role in ('prepare_binder','build_binder','Root_poststage_Source_META_contract.py'):
 for old,new in [('INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1','INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1'),('PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED','PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED'),('INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1','INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_POSTCLOSE_META_SOURCE_REVIEW_V1'),('PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY','PASS_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_AND_POSTCLOSE_META_SOURCE_ONLY')]:
  if old in texts[role]:replace(role,old,new,'new_bound_Source_peer_family_'+old)
role='prepare_binder'
replace(role,'READY Source binding only for V25 poststage-temporaries complete sender/root-index flow.','READY Source binding only for V25 memory-observation complete sender/root-index flow, with separately observed Darwin resource environment witness.','truthful_new_diagnostic_Source_binding_doc')

for role in ROLES:
 target=out/NAMES[role];target.write_text(texts[role]);ast.parse(texts[role])
 assert inverse(texts[role],edits[role])==parents[role]
 assert ast.dump(ast.parse(inverse(texts[role],edits[role])),include_attributes=False)==ast.dump(ast.parse(parents[role]),include_attributes=False)

# Preserve all old owner fullpins as lineage, with new actual Source and all
# future Source/business facts explicitly unknown instead of old successes.
oldcontract=json.loads((U/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json').read_text())
newcontract=dict(oldcontract)
newcontract['schema']='ROOT_V25_MEMORY_OBSERVATION_FIXED_COMPLETE_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT_V1'
newcontract['namespaces']={k:v.replace('v25-poststage-temporaries','v25-memory-observation').replace('v25_poststage_temporaries','v25_memory_observation') for k,v in oldcontract['namespaces'].items()}
for key in ('seven_author_role_Source_pins','author_manifest','author_peer_manifest','actual_new_PREP_bound_Source_manifest','actual_new_PREP_Source_binding_terminal'):newcontract[key]=None
newcontract['old_Source_actual_qualification_pins_are_lineage_only']={k:oldcontract[k] for k in ('seven_author_role_Source_pins','author_manifest','author_peer_manifest','actual_new_PREP_bound_Source_manifest','actual_new_PREP_Source_binding_terminal')}
newcontract['build_memory_diagnostic_output_contract']=CONTRACT
newcontract['future_actual_diagnostic_resource_environment_witness']=None
dump(out/'utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json',newcontract)
dump(out/'SOURCE_AND_ACTUAL_SMALL_META/ORIGINAL_COMPLETE_463_OWNER_CONTRACT.byte_exact.json',oldcontract)
(out/'SOURCE_AND_ACTUAL_SMALL_META/SOURCE_MEMORY_LOCALIZATION_AND_DIAGNOSTIC_PLAN.byte_exact.json').write_bytes(PLAN.read_bytes())
for j,(path,q) in enumerate(plan['source_pins'].items()):
 original=Path(path);actual=pin(original);assert all(actual[k]==q[k] for k in ('path','sha256','size_bytes','identity'))
 (out/'SOURCE_AND_ACTUAL_SMALL_META'/('SOURCE_'+str(j).zfill(2)+'_'+original.name)).write_bytes(original.read_bytes())
for j,(path,q) in enumerate(plan['actual_small_META_pins_and_facts'].items()):
 original=Path(path)
 if not original.is_file():continue
 actual=pin(original)
 expected=q.get('pin',q)
 if all(k in expected for k in actual):assert actual==expected
 assert actual['size_bytes']<1024*1024
 (out/'SOURCE_AND_ACTUAL_SMALL_META'/('ACTUAL_SMALL_META_'+str(j).zfill(2)+'_'+original.name)).write_bytes(original.read_bytes())

proof=dict(schema='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_WHOLE_SOURCE_INVERSES_V1',source_only=True,exact_finite_transforms=edits,role_current_paths={role:NAMES[role] for role in ROLES},original_parent_fullpins=parentpins,complete_byte_and_AST_inverses_verified=True,definitions_by_role={role:dict(original_count=len(definitions(parents[role])),new_count=len(definitions(texts[role])),unchanged_original_definition_occurrences=[dict(name=a[0],occurrence=i,whole_bytes_and_AST_unchanged=(a==b)) for i,(a,b) in enumerate(zip(definitions(parents[role]),[n for n in definitions(texts[role]) if n[0] in {x[0] for x in definitions(parents[role])}]))]) for role in ROLES})
dump(out/'COMPLETE_SOURCE_INVERSES.json',proof)
dump(out/'ROOT_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_REQUIRED_CONTRACT.UNREADY.json',dict(schema='ROOT_REQUIRED_DARWIN_RESOURCE_SELF_RUSAGE_ENVIRONMENT_WITNESS_CONTRACT_V1',source_only=True,actual_witness=None,actual_witness_schema='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1',required_fields=['schema','source_only','platform','diagnostic_dependency_verified','actual_python_fullpin','actual_resource_module_fullpin','actual_environment_tool_terminal_fullpin','self_ru_maxrss_native_bytes_observed','ru_maxrss_semantics','whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified'],actual_module_query_or_witness_executed_here=False,binding_scope='Root stdlib Source binding and D/prelaunch evidence; never inside active ReadOpenAudit and never added to d.files',canonical_requires_nonNone_literal=True,actual_extra_environment_dependency_runtime_qualification=False,contract=CONTRACT))
(out/'ROOT_NEXT_STEPS.txt').write_text('''UNREADY Source-only; no business, guard, helper, module-query, compiler, native or numeric execution occurred here.
1. Independently review this complete 14-role Source package and all whole-byte/AST inverses. New peer schema INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1 / status PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION. Report qualified_complete_Source_manifest_pin, qualified_role_Source_pins seven roles, qualified_utility_Source_pins seven basename roles; typed checks and genuine seal/postseal. Old Source peer and old PREP/BUILD are lineage only.
2. Root creates the true Darwin resource SELF-rusage small environment witness according to ROOT_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_REQUIRED_CONTRACT.UNREADY.json. Observe actual resolved Python/resource module full EOF/7ID and genuine closed terminal; raw sample is native historical bytes. It gives no RSS/build/INPUT/science admission.
3. Root stdlib prepare binder: actual Q path + c6 Q SHA + fresh TMP, original --actual-new-Q-writer-terminal/--actual-Q-saved-peer/--actual-Q-saved-peer-retention fullpins and new --actual-diagnostic-resource-environment-witness/--actual-diagnostic-resource-environment-witness-sha256. Binder imports no candidate/helper/guard/API. All six business slots remain None. Independently review actual bound three roles.
4. Root prepares actual Source/META install request using utilities/Root_prepare_poststage_REQUEST.Source_META_only.py with original CLI and six --author-manifest/sha256,--author-peer-manifest/sha256,--author-peer-seal/sha256 slots. Install/freezes all original owners exactly once, including true environment witness and its complete actual provenance in D before freeze. Fresh namespaces use v25-memory-observation / v25_memory_observation. Root full PREP once; preserve genuine terminal, all streams/namespaces/freeze and independent saved PREP review. BUILD diagnostic remains absent in PREP.
5. Root stdlib complete BUILD binder uses new actual PREP/canonical/Q fullpins and same environment witness, with original saved-PREP peer contract; bounded Source only. Independent actual bound BUILD Source review then original install/freezes/prelaunch. All seven utilities are complete Source derivatives; no actual new utility/installed/bound peer pins are known here.
6. Root genuine whole BUILD once under original 1800/600/512MiB/2GiB/96GiB/8GiB/1thread/1child/0retry. Diagnostic is only additional exclusive OUT file, <=256 rows*4096 bytes including LF, forecast reserves 1MiB inside 2GiB. Original full two graph parses, all input read counts, five commands/raw logs, MRO and single-JSON stdout remain.
7. Store genuine Root terminal before postclose writer; preserve complete partial journal including trailing fragment in full namespace. Success requires original whole guards/seal/tails plus actual sealed diagnostic pin. Final normal_pre_inventory row alone proves neither fsync/close nor inventory/tails; last complete rows after termination may have been written before fsync. Source-intended marker/fsync/close ordering is evidence only together with genuine CLOSED0 and unchanged complete seal/7ID. No later append after original inventory.
Remaining actual unknowns: new environment witness/Source and bound peers/install/prelaunch, fresh complete PREP and whole BUILD/diagnostic measurements. No prediction of current RSS, peak line, gc benefit, native, AAA or ABA qualification. AAA remains 7/8; ABA not started.
''')
checks=[]
def check(label,value):
 assert type(value)is bool;checks.append(dict(check=label,passed=value));assert value,label
for role in ROLES:
 check('whole_byte_inverse_'+role,inverse(texts[role],edits[role])==parents[role])
 check('whole_AST_inverse_'+role,ast.dump(ast.parse(inverse(texts[role],edits[role])),include_attributes=False)==ast.dump(ast.parse(parents[role]),include_attributes=False))
 check('parent_before_after_fullpin_'+role,pin(ROLES[role])==parentpins[role])
check('actual_C6693_all77_def_AST_match_UNREADY_parent',[(n,a) for n,_,a in definitions(Path(next(iter(plan['source_pins']))).read_text())]==[(n,a) for n,_,a in definitions(parents['canonical'])])
check('all_complete_old463_owners_preserved',newcontract['complete_old_frozen_Source_owners']==oldcontract['complete_old_frozen_Source_owners'])
check('all_six_canonical_future_business_pins_None',all(isinstance(n.value,ast.Constant)and n.value.value is None for n in ast.parse(texts['canonical']).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')))
check('journal_never_in_declared_input_files_or_owners',"BUILD_MEMORY_DIAGNOSTIC_CONTRACT" not in ast.get_source_segment(texts['canonical'],next(n for n in ast.parse(texts['canonical']).body if isinstance(n,ast.FunctionDef)and n.name=='current_new_owned_paths')))
check('helper3b_not_modified_or_qualified_again',pin(Path(list(plan['source_pins'])[1]))['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')
check('original_snapshot_consume_and_scope_preserved',texts['canonical'].count('trace=audit.snapshot(_consume=True);graph_path=')==1)
check('only_write_syscalls_in_logger_no_read_or_subprocess',all(not any(x in ast.dump(n,include_attributes=False) for x in ("attr='read'","attr='read_bytes'","attr='read_text'","id='subprocess'","id='importlib'")) for n in ast.walk(ast.parse(LOGGER)) if isinstance(n,ast.Call)))
check('max_marker_Source_path_below256',6*(26+2)+3+10+2<256)
check('literal_positive_original_caps_retained',all(x in texts['canonical'] for x in ('TOTAL_WALL','STAGE_WALL','RSS','RESERVE','HISTORY_CAP','FREE_FLOOR')))
check('actual_plan_Source_and_small_META_only_no_large_payload_EOF',all(p.stat().st_size<1024*1024 for p in (out/'SOURCE_AND_ACTUAL_SMALL_META').iterdir()))
class RemoveMemoryPoints(ast.NodeTransformer):
 def visit_Expr(self,node):
  if isinstance(node.value,ast.Call)and isinstance(node.value.func,ast.Name)and node.value.func.id=='memory_diagnostic_point':return None
  return self.generic_visit(node)
original_tree=ast.parse(parents['canonical']);new_tree=ast.parse(texts['canonical'])
for name in ('complete_input_phase','environment'):
 a=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 b=next(n for n in new_tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 check('remove_only_journal_calls_restores_entire_'+name+'_AST',ast.dump(a,include_attributes=False)==ast.dump(RemoveMemoryPoints().visit(b),include_attributes=False))
withs=lambda tree:[ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,ast.With)and any('ReadOpenAudit' in ast.dump(i.context_expr,include_attributes=False) for i in n.items)]
check('all_original_ReadOpenAudit_bodies_whole_AST_unchanged',withs(original_tree)==withs(new_tree))
for name in ('stage_commands','stage_labels','current_new_owned_paths'):
 a=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 b=next(n for n in new_tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 check('entire_original_'+name+'_AST_unchanged',ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))
check('all_three_last_use_snapshot_arguments_preserved',texts['canonical'].count('snapshot(_consume=True)')==parents['canonical'].count('snapshot(_consume=True)')==3)
check('journal_forecast_declared_1MiB_and_original_cap_unchanged',CONTRACT['max_bytes']==256*4096==2**20 and CONTRACT['actual_runtime_pin'] is None)
check('future_diagnostic_dependency_None_and_bound_mandatory_CLI',all('actual-diagnostic-resource-environment-witness' in texts[k] for k in ('prepare_binder','build_binder')) and 'FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN = None' in texts['canonical'])
check('failure_diagnostic_all_bytes_pin_and_trailing_fragment_preserved',all(x in READER for x in ('memory_diagnostic_pin(path)','PARTIAL_TRAILING_FRAGMENT','trailing_fragment','fsync_or_close_proved_by_rows_alone=False')))
check('whole_parent_current_77_definitions_retained',len(definitions(parents['canonical']))==77 and {x[0] for x in definitions(parents['canonical'])}.issubset({x[0] for x in definitions(texts['canonical'])}))
report=dict(schema='AUTHOR_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_REPORT_V1',status='UNREADY_COMPLETE_SOURCE_ONLY_NOT_INDEPENDENT_OR_RUNTIME_QUALIFICATION',source_only=True,checks=checks,check_count=len(checks),all_checks_typed_true=True,blockers=[],qualified_role_Source_pins={role:pin(out/NAMES[role]) for role in ROLES if role in ('canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer')},qualified_utility_Source_pins={role:pin(out/NAMES[role]) for role in ROLES if role not in ('canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer')},parent_source_fullpins=parentpins,plan_fullpin=planpin,fixed_diagnostic_contract=CONTRACT,actual_future_resource_environment_witness=None,all_actual_future_business_pins=None,diagnostic_runtime_controls_executed=False,candidate_guard_helper_API_module_query_compile_material_or_numeric_executed=False,project_ART_or_frozen_Source_written=False,whole_BUILD_INPUT_RSS_native_science_qualified=False,limitations=['Only Source author checks; independent peer and every actual new binding/install/PREP/BUILD remain future.','Darwin resource.getrusage dependency environment witness has not been produced here.','ru_maxrss is historical SELF native bytes, not current or sampled original guard RSS.','A saved row alone does not prove fsync or close; partial row/fragment remains actual unknown.','The existing peak interval only follows first link and precedes saved second metadata result; no precise peak line or cause is established.'])
dump(out/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT.json',report)
# Preserve this exact author Source as evidence, not as a candidate role.
(out/'AUTHOR_SOURCE_TEXT_ONLY.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(dict(source_only=True,output=str(out),author_report=pin(out/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT.json'),roles=report['qualified_role_Source_pins'],utility_roles=report['qualified_utility_Source_pins'],check_count=len(checks),all_checks_typed_true=True,business_executed=False)))

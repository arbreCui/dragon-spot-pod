"""Read saved failed terminal and Source/META only; never execute guard or diagnostics."""
import ast
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_native_observation_BUILD5_AB_v4_sources';E=B/'actual_complete_native_observation_BUILD5_AB_v4_receipts'
PRE=Path('/private/tmp/axmat_N4_actual_binding_prelaunch_Source_META_independent_fd2j7fgx/ACTUAL_SOURCE_NAMESPACE_PINS.json')
FAILED=B/'Root_actual_complete_observation_v4_pre_namespace_failure_tool_terminal_return.json'
Q=Path(tempfile.mkdtemp(prefix='axmat_N4_closed_pre_namespace_failure_META_independent_',dir='/private/tmp'))
checks=[];errors=[];pins={}

def ck(name,value):
    ok=type(value)is bool and value is True;checks.append(dict(check=name,passed=ok))
    if not ok:raise ValueError(name)

def identity(p):
    s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);before=identity(p)
    if not(p.is_absolute()and not any(x.is_symlink()for x in(p,*p.parents))and stat.S_ISREG(before[2])and before[3]==1):raise ValueError('regular singlelink Source/META only')
    with p.open('rb')as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before:raise ValueError('fullEOF7ID changed')
    value=dict(path=str(p),sha256=d,size_bytes=before[4],identity=before)
    if str(p)in pins and pins[str(p)]!=value:raise ValueError('Source/META changed')
    pins[str(p)]=value;return value

def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def load(p):
    old=pin(p);value=strict(Path(p).read_bytes())
    if pin(p)!=old:raise ValueError('parse7ID changed')
    return value

def tree(root):
    ds={'.':identity(root)};fs={}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));s=p.lstat()
        if stat.S_ISDIR(s.st_mode):ds[rel]=identity(p)
        elif stat.S_ISREG(s.st_mode):fs[rel]=pin(p)
        else:raise ValueError('namespace nonordinary member')
    return dict(directories=ds,files=fs)

try:
    old=load(PRE);previews=old['namespace_views'];before={'D':tree(D),'E':tree(E)}
    ck('actual prelaunch evidence exact immutable fullSHA',pin(PRE)['sha256']=='ee6e32075bb96a4bda760af7f8bc8b3d7192f8fbf3ae417e9c563e377535c78f')
    ck('complete D102 E5 fullEOF SHA7ID and directory13 plus1 equal prelaunch',before==previews and(len(before['D']['files']),len(before['E']['files']),len(before['D']['directories']),len(before['E']['directories']))==(102,5,13,1))
    failed=load(FAILED);tr=failed['terminal_tool_return'];initial=failed['initial_tool_return'];observations=failed['observations'];binding=load(D/'Root_actual_observation_SOURCE_binding.json');ns=binding['namespaces']
    ck('actual failed Root wrapper strict CLOSED observed integer1 no terminal session',failed['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_PRE_NAMESPACE_FAILURE_TOOL_TERMINAL_RETURN_V1'and failed['closed']is True and failed['observed_terminal']is True and failed['observed_after_actual_terminal_return']is True and failed['record_producer']=='root'and failed['session_repolled_after_close']is False and type(failed['exit_code'])is int and failed['exit_code']==1 and tr['chunk_id']=='63d442'and type(tr['exit_code'])is int and tr['exit_code']==1 and 'session_id'not in tr)
    ck('actual initial live14035 and terminal63d442 observations preserved exactly',initial['chunk_id']=='a6bfc4'and type(initial['session_id'])is int and initial['session_id']==failed['original_session_id']==14035 and 'exit_code'not in initial and observations==[initial,tr])
    hostpath=D/'Root_bound_complete_observation_genuine_host.py';runtimepath=D/'Root_bound_complete_observation_runtime.py';hr=hostpath.read_bytes();rr=runtimepath.read_bytes();hs=hr.decode();rs=rr.decode();ht=ast.parse(hr);rt=ast.parse(rr)
    ck('failed actual bound host runtime complete Source bytes still prelaunch',pin(hostpath)==previews['D']['files'][hostpath.name]and pin(runtimepath)==previews['D']['files'][runtimepath.name]and str(hostpath)in failed['actual_launch_arguments']['cmd'])
    ck('failed actual CLI same five one-thread environment observation flag',all(x+'=1'in failed['actual_launch_arguments']['cmd']for x in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))and 'SPOT_AXMAT_OBSERVATION=ADMITTED_SOURCE_ONLY'in failed['actual_launch_arguments']['cmd'])
    out=tr['output']
    ck('actual raw traceback initial resource check joint_bytes lsof failure matches exact Source frames',str(hostpath)in out and str(runtimepath)in out and 'line 347, in run'in out and 'line 340, in check'in out and 'line 191, in joint_bytes'in out and "ValueError: full live own process file scan required"in out and rs.splitlines()[190].strip()=="require(observed.returncode==0,'full live own process file scan required')")
    run=next(n for n in rt.body if isinstance(n,ast.FunctionDef)and n.name=='run');joint=next(n for n in rt.body if isinstance(n,ast.FunctionDef)and n.name=='joint_bytes');attempt=next(n for n in run.body if isinstance(n,ast.Try));first=attempt.body[0]
    ck('Source try first resource check precedes all namespace creation and native compile',first.lineno==347 and 'before=resources.check()'in ast.get_source_segment(rs,first)and attempt.body[2].lineno>first.lineno and rs.index('before=resources.check();')<rs.index('host.mkdir();out.mkdir();control.mkdir();')<rs.index('ep,build=compile_all(')<rs.index("for state in('A','B'):",rs.index('ep,build=compile_all(')))
    ck('Source diagnostic failed lsof exact canonical contract no command execution by reviewer',"subprocess.run([lsof_tool,'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)"in ast.get_source_segment(rs,joint)and binding['tool_pins']['lsof']['path']=='/usr/sbin/lsof'and binding['tool_pins']['ps']['path']=='/bin/ps')
    ck('actual H O C absent after closed failure D E current exact namespace',ns['source']==str(D)and ns['receipts']==str(E)and all(not os.path.lexists(ns[k])for k in('host','output','control')))
    ck('Source failure handler writes only if host exists so no failure artifact created here',"if host.is_dir():"in ast.get_source_segment(rs,attempt.handlers[0])and not os.path.lexists(Path(ns['host'])/'failed_host_result.json'))
    ck('saved Root failure honestly grants no compile material observation science success',failed['new_native_compile_or_material_execution_observed']is False and failed['scientific_qualification_created']is False and binding['actual_observation_manifest']is None and binding['actual_observer_native_execution']is None and binding['scientific_accuracy_qualified']is False and binding['complete_context_aggregation_qualified']is False)
    after={'D':tree(D),'E':tree(E)}
    ck('complete namespace and failed original terminal unchanged throughout own review',after==before and pin(FAILED)==pins[str(FAILED)]and pin(PRE)==pins[str(PRE)])
except Exception as ex:errors.append(dict(type=type(ex).__name__,message=str(ex)))

blockers=[c['check']for c in checks if c['passed']is not True]+[x['message']for x in errors]
report=dict(schema='INDEPENDENT_ACTUAL_N4_CLOSED_PRE_NAMESPACE_FAILURE_SOURCE_META_REVIEW_V1',status='VERIFIED_CLOSED_EXIT1_PRE_NAMESPACE_FAILURE_NO_COMPILE_MATERIAL_OR_SCIENCE_CREDIT'if not blockers else'BLOCKED_SAVED_FAILURE_META_REVIEW',source_only_saved_failure_META_review=True,all_checks_typed_true=not blockers,check_count=len(checks),checks=checks,blockers=blockers,errors=errors,actual_failed_Root_terminal_chunk='63d442',actual_original_live_session_id=14035,actual_prelaunch_namespace_evidence_pin=pins.get(str(PRE)),actual_saved_failed_terminal_pin=pins.get(str(FAILED)),actual_bound_host_pin=pins.get(str(D/'Root_bound_complete_observation_genuine_host.py')),actual_bound_runtime_pin=pins.get(str(D/'Root_bound_complete_observation_runtime.py')),failure_scope='genuine host entered runtime initial resource accounting; nonzero lsof branch before H/O/C creation and before native compile or A/B material child',actual_H_O_C_absent=not blockers,complete_D_E_unchanged=not blockers,actual_lsof_exact_returncode=None,actual_lsof_original_stdout=None,actual_lsof_original_stderr=None,lsof_nonzero_branch_supported_by_saved_traceback_and_exact_Source=True if not blockers else False,scope_limits=['Root genuine host and initial input hashing/guard loading/process diagnostic paths were entered; this is an actual failed attempt, not an unexecuted Source-only candidate.','The saved traceback proves the lsof nonzero check failed, but does not contain its exact return code or original diagnostic stdout/stderr.','No successful whole observation/native build/material observation or scientific qualification follows from this review.'],reviewer_candidate_guard_API_compile_lsof_ps_native_numeric_or_Rootwriter_executed=False,reviewer_material_or_DB_payload_read=False,reviewer_project_D_E_or_progress_written=False,reviewer_session_repolled=False,actual_native_compile_started=False,actual_AB_material_child_started=False,actual_observation_success=False,scientific_qualification_created=False)
with(Q/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with(Q/'ACTUAL_SAVED_ROOT_FAILED_TERMINAL.byte_exact.json').open('xb')as f:f.write(FAILED.read_bytes())
with(Q/'reviewer_Source.py').open('xb')as f:f.write(Path(__file__).read_bytes())
print(json.dumps(dict(status=report['status'],report_pin=pin(Q/'REVIEW.json'),actual_saved_failed_terminal_copy_pin=pin(Q/'ACTUAL_SAVED_ROOT_FAILED_TERMINAL.byte_exact.json'),reviewer_Source_pin=pin(Q/'reviewer_Source.py'),checks=len(checks),blockers=blockers,candidate_or_native_or_guard_or_diagnostics_executed_by_reviewer=False),allow_nan=False),flush=True)
sys.exit(0 if not blockers else 1)

"""Finite independent Source and saved environment META review. No resource API import/call."""
import ast,hashlib,json,math,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_INDEPENDENT_Darwin_resource_environment_witness_puchj6jp')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
M=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
OLD=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
PY=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
RESOURCE=Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so')
RESOURCE_SHA='cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164'
SEMANTICS='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
ROLES={
 'actual_witness':(B/'Root_actual_Darwin_resource_SELF_rusage_diagnostic_environment_witness.json','945b3d52207b4d3dde2c672c017dd643a51e0d586375193faf0ec91b53184aa1',3145),
 'actual_query_terminal':(B/'Root_actual_Darwin_resource_SELF_rusage_environment_tool_terminal_return.json','b189f3a09b77771110576138370d42bf6f06d19449285b4810a4f8a240cdebf3',2879),
 'actual_META_writer_terminal':(B/'Root_actual_Darwin_resource_environment_witness_META_writer_tool_terminal_return.json','3f55206a5af60d3ad319dad105b3dbcf75143d2a60d0b9df1873e0f5fe57183b',1398),
 'actual_producer_Source':(Path('/private/tmp/spot_ROOT_actual_Darwin_resource_SELF_rusage_environment_query_20261010.py'),'2aee11d786088a82e5e53c964c0f0c962887a4f4e08a526cbf2255d7f689dd12',2491),
 'actual_META_writer_Source':(Path('/private/tmp/spot_ROOT_write_actual_Darwin_resource_SELF_rusage_environment_witness_Source_META_20261010.py'),'46c91d2e0163c46639d47ab9c3d15c2758b1fa82e3d1dd012a5ae3582c6a73fc',3554),
 'actual_required_contract':(M/'ROOT_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_REQUIRED_CONTRACT.UNREADY.json','23aa3b55ec7413adb27c49cc640c171e075365e4c94e66adebfc0dc27d7e9165',3956),
 'actual_PREP_binder_Source':(M/'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','b3297d5b954c9cabb10accca0ba288ec530a68cdd3dfa4e9b212f3eb46c058a2',68987),
 'actual_BUILD_binder_Source':(M/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py','0828e947fea8a1601a4465ed96aac156f5c72a86de6bba688220be8b87e2def8',58029)}
checks=[];pins={};copies={}
def check(name,value,evidence):
 assert type(value)is bool and name not in [r['name']for r in checks];checks.append(dict(name=name,passed=value,evidence=evidence))
 if not value:raise AssertionError(name)
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(p,resource_endpoint=False):
 p=Path(p);assert p.is_absolute()and '..'not in p.parts
 for q in [*reversed(p.parents),p]:
  s=q.lstat();assert not stat.S_ISLNK(s.st_mode)and(q==p or stat.S_ISDIR(s.st_mode))
 i=identity(p);assert stat.S_ISREG(i[2])and type(i[3])is int
 if resource_endpoint:assert p==RESOURCE and i[3]==2
 else:assert i[3]==1
 h=hashlib.sha256();n=0
 with p.open('rb')as f:
  while True:
   raw=f.read(2**20)
   if not raw:break
   h.update(raw);n+=len(raw)
 assert identity(p)==i and n==i[4]
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);pins[str(p)]=q;return q
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
def load(p):
 q=fullpin(p);m=strict(Path(p).read_bytes());assert fullpin(p)==q;return m,q
def source(p):
 q=fullpin(p);s=Path(p).read_text();t=ast.parse(s,filename=str(p));assert fullpin(p)==q;return s,t,q
def pinshape(q):
 return type(q)is dict and set(q)=={'path','sha256','size_bytes','identity'}and type(q['path'])is str and Path(q['path']).is_absolute()and type(q['sha256'])is str and len(q['sha256'])==64 and all(x in '0123456789abcdef'for x in q['sha256'])and type(q['size_bytes'])is int and q['size_bytes']>=0 and type(q['identity'])is list and len(q['identity'])==7 and all(type(i)is int for i in q['identity'])and q['identity'][4]==q['size_bytes']
def funcs(s,t,name):
 lines=s.splitlines(keepends=True)
 return [(ast.dump(n,include_attributes=False),''.join(lines[n.lineno-1:n.end_lineno]))for n in ast.walk(t)if isinstance(n,ast.FunctionDef)and n.name==name]
def assignments(t):
 return {n.targets[0].id:ast.literal_eval(n.value)for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ('BUILD_MEMORY_DIAGNOSTIC_CONTRACT','BUSINESS')}
def terminal(m,schema,chunk):
 assert m['schema']==schema and m['closed']is True and m['observed_terminal']is True and m['session_repolled_after_close']is False
 t=m['terminal_tool_return'];assert type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==chunk and type(t['output'])is str
 return t,strict(t['output'])
def copy(role,p):
 p=Path(p);q=fullpin(p);out=F/'REVIEWED_SOURCE_AND_SMALL_META'/role;out.parent.mkdir(exist_ok=True);out.write_bytes(p.read_bytes());cq=fullpin(out)
 assert q==fullpin(p)and cq['sha256']==q['sha256']and cq['size_bytes']==q['size_bytes'];copies[role]=dict(original_pin=q,review_copy_pin=cq)

def main():
 assert len(sys.argv)==1 and not sys.flags.optimize and sys.getprofile()is None
 values={};rolepins={}
 for role,(p,sha,size)in ROLES.items():
  if role.endswith('_Source'):v=source(p);values[role]=v;q=v[2]
  else:v,q=load(p);values[role]=v
  assert(q['sha256'],q['size_bytes'])==(sha,size);rolepins[role]=q
 check('all_current_actual_environment_Source_small_META_roles_complete_EOF_SHA_size_7ID_noalias',True,dict(role_fullpins=rolepins,only_endpoint_extra_reads=[str(PY),str(RESOURCE)]))
 witness=values['actual_witness'];qt,qbody=terminal(values['actual_query_terminal'],'ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_ENVIRONMENT_TOOL_TERMINAL_RETURN_V1','5ae744')
 wt,wout=terminal(values['actual_META_writer_terminal'],'ROOT_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_WITNESS_META_WRITER_TOOL_TERMINAL_RETURN_V1','066a1d')
 assert qbody['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_QUERY_V1'and witness['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1'
 expected=dict(qbody);expected['schema']=witness['schema'];expected['actual_environment_tool_terminal_fullpin']=rolepins['actual_query_terminal'];expected['environment_witness_META_writer_Source_fullpin']=rolepins['actual_META_writer_Source'];expected['diagnostic_dependency_scope']='ISOLATED_ACTUAL_RESOURCE_IMPORT_AND_ONE_SELF_QUERY_ONLY_NOT_CURRENT_RSS_OR_BUSINESS_GUARD'
 assert witness==expected and wout['witness_pin']==rolepins['actual_witness']and wout['actual_query_terminal_chunk']=='5ae744'and type(wout['query_count'])is int and wout['query_count']==1
 assert wout['cleanup_performed']is False and values['actual_META_writer_terminal']['cleanup_performed']is False
 check('genuine_closed_query_and_META_writer_rawstdout_exactly_couple_one_current_witness_no_reexecution',True,dict(query_chunk='5ae744',query_exit_code=0,META_writer_chunk='066a1d',META_writer_exit_code=0,query_output_bytes=len(qt['output'].encode()),META_writer_output_bytes=len(wt['output'].encode()),witness_pin=rolepins['actual_witness'],all_original_query_fields_retained=True))
 for field,p,sha,size,special in [('actual_python_fullpin',PY,'ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860',6672384,False),('actual_resource_module_fullpin',RESOURCE,RESOURCE_SHA,53552,True)]:
  q=witness[field];assert pinshape(q)and q['path']==str(p)and(q['sha256'],q['size_bytes'])==(sha,size)and fullpin(p,resource_endpoint=special)==q
 assert witness['actual_environment_producer_Source_fullpin']==rolepins['actual_producer_Source']
 check('actual_exact_Python_and_resource_environment_endpoints_have_current_complete_EOF_SHA7ID',True,dict(actual_python_fullpin=witness['actual_python_fullpin'],actual_resource_module_fullpin=witness['actual_resource_module_fullpin'],resource_positive_nlink_exception_exclusive_to_exact_endpoint=True,resource_observed_nlink=2,default_other_read_Source_and_META_singlelink=True,endpoints_read_as_bytes_only_neither_imported_nor_called_by_reviewer=True))
 assert witness['source_only']is True and witness['platform']=='darwin'and witness['diagnostic_dependency_verified']is True
 assert type(witness['actual_python_optimization'])is int and witness['actual_python_optimization']==0 and witness['actual_thread_environment']==dict.fromkeys(THREADS,'1')and type(witness['query_count'])is int and witness['query_count']==1
 assert type(witness['self_ru_maxrss_native_bytes_observed'])is int and witness['self_ru_maxrss_native_bytes_observed']==15548416 and witness['ru_maxrss_semantics']==SEMANTICS
 assert type(witness['elapsed_seconds'])is float and math.isfinite(witness['elapsed_seconds'])and 0<witness['elapsed_seconds']<30
 qcmd=values['actual_query_terminal']['actual_launch_args']['cmd'];assert qcmd=='env -u PYTHONOPTIMIZE '+' '.join(k+'=1'for k in THREADS)+' '+str(PY)+' -B '+str(ROLES['actual_producer_Source'][0])
 wcmd=values['actual_META_writer_terminal']['actual_launch_args']['cmd'];assert wcmd==str(PY)+' -B '+str(ROLES['actual_META_writer_Source'][0])
 check('single_actual_native_byte_historical_SELF_observation_preserves_exact_thread_and_optimization_environment',True,dict(actual_native_bytes=15548416,query_count=1,actual_python_version=witness['actual_python_version'],five_thread_values=witness['actual_thread_environment'],optimization=0,actual_query_launch=qcmd,actual_META_writer_launch=wcmd,semantics=SEMANTICS,not_current_RSS=True,not_genuine_guard_peak=True))
 ps,pt,pp=values['actual_producer_Source'];ws,wst,wp=values['actual_META_writer_Source']
 producer_imports=[]
 for n in pt.body:
  if isinstance(n,ast.Import):producer_imports.extend(a.name for a in n.names)
  elif isinstance(n,ast.ImportFrom):producer_imports.append(n.module)
 assert set(producer_imports)=={'hashlib','json','os','stat','sys','resource','time','pathlib'}
 calls=[n for n in ast.walk(pt)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='resource'and n.func.attr=='getrusage']
 assert len(calls)==1 and len(calls[0].args)==1 and ast.dump(calls[0].args[0],include_attributes=False)==ast.dump(ast.Attribute(value=ast.Name(id='resource',ctx=ast.Load()),attr='RUSAGE_SELF',ctx=ast.Load()),include_attributes=False)
 assert 'resource.__file__==str(MOD)'in ps and 'sys.executable==str(PY)'in ps and "mod_before['sha256']==SHA"in ps and 'type(raw) is int'in ps
 assert ps.index('py_before=pin(PY);mod_before=pin(MOD)')<ps.index('raw=resource.getrusage')<ps.index('assert pin(PY)==py_before and pin(MOD)==mod_before')
 assert "before[3]>0"in ps and "p=Path(p)"in funcs(ps,pt,'pin')[0][1]
 check('complete_actual_producer_AST_has_exact_one_SELF_query_and_pin_before_after_with_no_candidate_or_business_imports',True,dict(actual_producer_pin=pp,full_Source_AST_parsed=True,actual_resource_calls=1,resource_api_executed_by_reviewer=False,producer_endpoint_positive_nlink_only_used_for_three_fixed_Python_resource_ownSource_calls=True))
 assert "tr['chunk_id']=='5ae744'"in ws and "d['actual_resource_module_fullpin']['identity'][3]==2"in ws and 'body=dict(d)'in ws and "body['actual_environment_tool_terminal_fullpin']=tp"in ws and "with OUT.open('x')"in ws
 assert "type(tr['exit_code']) is int"in ws and "'session_id' not in tr"in ws and "assert pin(d[k]['path'])==d[k]"in ws
 writer_imports=[a.name for n in wst.body if isinstance(n,ast.Import)for a in n.names]+[n.module for n in wst.body if isinstance(n,ast.ImportFrom)]
 assert set(writer_imports)=={'hashlib','json','stat','pathlib'}
 check('complete_actual_META_writer_Source_preserves_full_original_query_body_and_true_closed_tool_coupling_without_resource_query',True,dict(actual_writer_Source_pin=wp,full_AST_parsed=True,no_resource_or_candidate_import=True,exclusive_fresh_witness_write=True))
 contract=values['actual_required_contract'];assert contract['schema']=='ROOT_REQUIRED_DARWIN_RESOURCE_SELF_RUSAGE_ENVIRONMENT_WITNESS_CONTRACT_V1'and contract['source_only']is True and contract['actual_witness']is None
 assert contract['actual_witness_schema']==witness['schema']and set(contract['required_fields']).issubset(witness)and contract['resource_role_path']==str(RESOURCE)and contract['resource_role_SHA']==RESOURCE_SHA and contract['resource_role_size_bytes']==53552
 assert contract['exclusive_dependency_role_exact_positive_nlink_preserved']is True and contract['default_other_Source_singlelink_not_relaxed']is True and contract['actual_module_query_or_witness_executed_here']is False and contract['actual_extra_environment_dependency_runtime_qualification']is False
 assert contract['contract']['ru_maxrss_semantics']==SEMANTICS and contract['contract']['actual_runtime_pin']is None and contract['contract']['current_RSS_qualified']is False and contract['contract']['whole_INPUT_build_native_or_science_qualified']is False
 assert contract['binding_scope']=='Root stdlib Source binding and D/prelaunch evidence; never inside active ReadOpenAudit and never added to d.files'
 check('actual_witness_satisfies_complete_UNREADY_environment_dependency_contract_without_filling_future_business_or_runtime_pins',True,dict(contract_pin=rolepins['actual_required_contract'],required_fields=contract['required_fields'],actual_Source_contract_witness_literal_remains_None=True,scope=contract['binding_scope'],contract_future_runtime_pin=None))
 binders={};fn_bodies=[];old_generic_pins={}
 for role in ['actual_PREP_binder_Source','actual_BUILD_binder_Source']:
  s,t,q=values[role];name=ROLES[role][0].name;osrc,ot,oq=source(OLD/name);old_generic_pins[role]=oq
  fns=funcs(s,t,'diagnostic_resource_environment_witness');assert len(fns)==1;fn_bodies.append(fns[0]);body=fns[0][1]
  required=["body.get('schema')!='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1'","for field in ('actual_python_fullpin','actual_resource_module_fullpin','actual_environment_tool_terminal_fullpin')", "if field=='actual_resource_module_fullpin'",str(RESOURCE),RESOURCE_SHA,"q['identity'][3]<1","actual=source_pin(require(q['path'],q['sha256']))","if actual!=q",str(PY),"type(tr.get('exit_code')) is not int","'session_id' in tr","observed=json.loads(tr['output'])","type(body.get('self_ru_maxrss_native_bytes_observed')) is not int","return wanted"]
  assert all(fragment in body for fragment in required)
  for generic in ['normal','require','read','source_pin','helper_Q_fullpin']:
   assert funcs(s,t,generic)==funcs(osrc,ot,generic)and len(funcs(s,t,generic))==1
  assert 'resource_environment_pin=diagnostic_resource_environment_witness(args.actual_diagnostic_resource_environment_witness,args.actual_diagnostic_resource_environment_witness_sha256)'in s
  assert "'--actual-diagnostic-resource-environment-witness'"in s and "'--actual-diagnostic-resource-environment-witness-sha256'"in s
  binders[role]=dict(Source_pin=q,function_start=next(n.lineno for n in ast.walk(t)if isinstance(n,ast.FunctionDef)and n.name=='diagnostic_resource_environment_witness'),whole_function_Source=fns[0][1],whole_function_AST=fns[0][0],generic_Source_input_functions_byte_AST_preserved_to_original=True,original_binder_pin=oq)
  copy('original_generic_'+name,OLD/name)
 assert fn_bodies[0]==fn_bodies[1]
 check('complete_PREP_and_BUILD_binder_witness_consumers_have_identical_full_Source_contract_and_preserve_original_generic_Source_functions',True,dict(binder_contracts=binders,original_generic_function_pins=old_generic_pins,resource_positive_nlink_branch_exact_endpoint_only=True,no_candidate_binder_executed=True))
 prep_s=values['actual_PREP_binder_Source'][0];build_s=values['actual_BUILD_binder_Source'][0]
 assert "'FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN = None'"in prep_s and "'ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json'"in prep_s and "'ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_TOOL_TERMINAL.byte_exact.json'"in prep_s
 assert "assignments['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN']"in build_s and "'same actual SOURCE/prelaunch environment witness'"in build_s
 for s,t,q in [values['actual_PREP_binder_Source'],values['actual_BUILD_binder_Source']]:
  literal=assignments(t);assert literal['BUILD_MEMORY_DIAGNOSTIC_CONTRACT']==contract['contract'] and len(literal['BUSINESS'])==6
 check('future_PREP_literal_copy_and_BUILD_same_witness_coupling_preserve_read_audit_scope_and_all_six_unknown_business_contracts',True,dict(PREP_witness_and_query_terminal_byte_copies_declared=True,BUILD_checks_same_bound_canonical_witness_literal=True,diagnostic_contract_full_equal_to_required_contract=True,actual_new_BIND_PREP_BUILD_controls_or_science_success_created=False))
 for obj in [witness,qbody,wout,values['actual_query_terminal'],values['actual_META_writer_terminal']]:
  assert all(obj[k]is False for k in ['whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified'])
 assert witness['candidate_guard_helper_compile_material_or_numeric_executed']is False
 check('environment_dependency_only_never_asserts_current_RSS_original_guard_peak_BUILD_INPUT_native_or_science_qualification',True,dict(environment_dependency_observed=True,query_native_historical_highwater_bytes=15548416,current_RSS=None,genuine_guard_sampled_peak=None,actual_BUILD=None,actual_INPUT=None,native_or_science_qualified=False))
 for role,(p,sha,size)in ROLES.items():copy(role+('.py'if role.endswith('_Source')else'.json'),p)
 # Environment binaries are allowed EOF endpoints, deliberately not copied into this finite Source/META packet.
 for field,sp in [('actual_python_fullpin',False),('actual_resource_module_fullpin',True)]:assert fullpin(witness[field]['path'],resource_endpoint=sp)==witness[field]
 for q in list(pins.values()):assert identity(Path(q['path']))==q['identity']
 check('all_original_Source_small_META_and_two_exact_environment_endpoints_unchanged_after_independent_review_and_lossless_copies',True,dict(lossless_copy_count=len(copies),project_or_parent_modified=False,binary_endpoints_not_copied=True,resource_API_not_imported_or_called=True))
 report=dict(schema='INDEPENDENT_ROOT_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_WITNESS_SOURCE_SMALL_META_REVIEW_V1',status='PASS_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_DEPENDENCY_ONLY_NO_BUILD_INPUT_OR_SCIENCE',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=True,all_checks_typed_true=True,blockers=[],qualified_actual_witness_pin=rolepins['actual_witness'],actual_Root_query_terminal_pin=rolepins['actual_query_terminal'],actual_Root_META_writer_terminal_pin=rolepins['actual_META_writer_terminal'],actual_Root_producer_Source_pin=pp,actual_Root_META_writer_Source_pin=wp,actual_environment_endpoints=dict(python=witness['actual_python_fullpin'],resource=witness['actual_resource_module_fullpin']),actual_Root_query_chunk='5ae744',actual_Root_META_writer_chunk='066a1d',actual_query_count=1,actual_SELF_ru_maxrss_native_historical_bytes=15548416,ru_maxrss_semantics=SEMANTICS,actual_python_optimization=0,actual_five_thread_environment=witness['actual_thread_environment'],actual_current_environment_contract_pin=rolepins['actual_required_contract'],actual_complete_binder_contracts=binders,actual_dependency_only_verified=True,exclusive_resource_dependency_role_nlink2_preserved=True,generic_Source_endpoint_input_functions_not_changed=True,all_original_read_Source_small_META_and_environment_fullpins={k:v for k,v in pins.items()if not Path(k).is_relative_to(F)},finite_lossless_Source_small_META_copies=copies,environment_binary_endpoints_not_copied=True,no_resource_getrusage_guard_API_PS_lsof_candidate_binder_compiler_material_or_numeric_executed_by_reviewer=True,project_or_parent_modified=False,current_RSS_verified=False,genuine_guard_peak_verified=False,whole_BUILD_qualified=False,whole_INPUT_qualified=False,native_or_science_qualified=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,actual_independent_reviewer_Source_pin=fullpin(Path(__file__)))
 out=F/'REVIEW.json';out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 print(json.dumps(dict(status=report['status'],review_pin=fullpin(out),check_count=len(checks),all_checks_typed_true=True,blockers=[],review_copy_count=len(copies),actual_witness_pin=rolepins['actual_witness'],actual_query_chunk='5ae744',actual_META_writer_chunk='066a1d',native_or_science_qualified=False),allow_nan=False))
if __name__=='__main__':main()

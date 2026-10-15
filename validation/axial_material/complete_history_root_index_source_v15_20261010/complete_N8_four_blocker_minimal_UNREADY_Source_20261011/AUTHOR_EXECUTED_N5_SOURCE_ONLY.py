from pathlib import Path
import ast,hashlib,json,os,stat,tempfile,tarfile

OLD=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_role_limited_OS_tools_N4_UNREADY_Source_3gnnt2it')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
P=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_N5_closed_PS_only_UNREADY_Source_',dir='/private/tmp'))
READ_PINS={}
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1 and not p.is_symlink();raw=p.read_bytes();assert i7(a)==i7(p.lstat())
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i7(a))
def read(p):
 p=Path(p);before=pin(p);raw=p.read_bytes();assert pin(p)==before;READ_PINS[str(p)]=before;return raw
def put(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb')as f:f.write(raw)
def dump(p,o):put(p,(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
mf=json.loads(read(OLD/'MANIFEST.json'))
assert mf['member_count']==97 and len(mf['members'])==97
members={row['relative_path']:row['fullpin']for row in mf['members']}
directories=mf['complete_directory_identity']
oldfiles={str(p.relative_to(OLD))for p in OLD.rglob('*')if p.is_file()};olddirs={'.'}|{str(p.relative_to(OLD))for p in OLD.rglob('*')if p.is_dir()}
assert oldfiles==set(members)|{'MANIFEST.json'}and olddirs==set(directories)
for rel,row in directories.items():assert i7((OLD if rel=='.'else OLD/rel).lstat())==row
for rel,wanted in members.items():
 raw=read(OLD/rel);assert READ_PINS[str(OLD/rel)]==wanted;put(P/rel,raw)
put(P/'PREVIOUS_SEALED_N4_SOURCE_PROVENANCE/MANIFEST.json',read(OLD/'MANIFEST.json'))
runtime='complete_observation_BUILD5_AB_runtime.UNREADY.py'
original=(P/runtime).read_text();tree=ast.parse(original);n=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='joint_bytes');oldfunc=ast.get_source_segment(original,n)
old_ps="    ps=subprocess.run([ps_tool,'-axo','pid=,ppid='],capture_output=True,text=True,timeout=2,check=True)\n    parents={int(a):int(b)for a,b in(line.split()for line in ps.stdout.splitlines())}"
new_ps="""    ps_argv=[ps_tool,'-axo','pid=,ppid=']
    with subprocess.Popen(ps_argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)as ps_process:
        ps_diagnostic_pid=ps_process.pid
        try:
            ps_stdout,ps_stderr=ps_process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            ps_process.kill();ps_process.wait();raise
        except BaseException:
            ps_process.kill();raise
        ps_returncode=ps_process.poll()
        if ps_returncode:
            raise subprocess.CalledProcessError(ps_returncode,ps_process.args,output=ps_stdout,stderr=ps_stderr)
    require(type(ps_diagnostic_pid)is int and ps_diagnostic_pid>0 and type(ps_returncode)is int and ps_returncode==0,'exact actual PS diagnostic closed EXIT0 before PID exclusion')
    parents={int(a):int(b)for a,b in(line.split()for line in ps_stdout.splitlines())}"""
assert oldfunc.count(old_ps)==1;newfunc=oldfunc.replace(old_ps,new_ps)
anchor="        selected=expanded\n    observed=subprocess.run("
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"        selected=expanded\n    # Exclude only this captured, already reaped EXIT0 diagnostic child.\n    # Every actual own business descendant remains in the same full closure.\n    selected.discard(ps_diagnostic_pid)\n    observed=subprocess.run(")
assert original.count(oldfunc)==1;candidate=original.replace(oldfunc,newfunc)
(P/runtime).write_text(candidate)
put(P/'PREVIOUS_SEALED_N4_SOURCE_PROVENANCE/ORIGINAL_N4_RUNTIME.full.py',original.encode())
checks=[]
def check(label,value):
 assert type(value)is bool and value,label;assert label not in[x['check']for x in checks];checks.append(dict(check=label,passed=True))
restored=candidate.replace(newfunc,oldfunc)
check('whole_runtime_byte_and_AST_inverse',restored==original and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
def defs(text):return [(x.name,ast.get_source_segment(text,x),ast.dump(x,include_attributes=False))for x in ast.parse(text).body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
before=defs(original);after=defs(candidate)
check('only_joint_bytes_definition_changes',len(before)==len(after)and all(a[0]==b[0]and(a[0]=='joint_bytes'or a[1:]==b[1:])for a,b in zip(before,after)))
check('all_runtime_global_and_import_AST_unchanged',[ast.dump(x,include_attributes=False)for x in ast.parse(candidate).body if not isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]==[ast.dump(x,include_attributes=False)for x in ast.parse(original).body if not isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))])
check('all_other_96_N4_source_members_complete_byte_exact',all((P/rel).read_bytes()==(OLD/rel).read_bytes()for rel in members if rel!=runtime))
oldjoint=next(x for x in ast.parse(oldfunc).body if isinstance(x,ast.FunctionDef));newjoint=next(x for x in ast.parse(newfunc).body if isinstance(x,ast.FunctionDef))
check('original_return_all_fields_types_order_preserved',ast.dump(oldjoint.body[-1],include_attributes=False)==ast.dump(newjoint.body[-1],include_attributes=False))
oldtail=oldfunc[oldfunc.index('    observed=subprocess.run('):];newtail=newfunc[newfunc.index('    observed=subprocess.run('):]
check('entire_original_lsof_strict_zero_2seconds_8MiB_parser_unlinked_and_return_tail_unchanged',oldtail==newtail)
check('full_original_regular_and_singlelink_joint_prefix_unchanged',oldfunc.split('    ps=subprocess.run(')[0]==newfunc.split('    ps_argv=')[0])
check('same_PS_argv_text_capture_timeout_two',"ps_argv=[ps_tool,'-axo','pid=,ppid=']"in newfunc and 'stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True'in newfunc and 'communicate(timeout=2)'in newfunc)
check('actual_Popen_pid_captured_before_communicate',newfunc.index('ps_diagnostic_pid=ps_process.pid')<newfunc.index('ps_process.communicate(timeout=2)'))
check('timeout_POSIX_kill_wait_raise_and_other_exception_lifecycle_preserved','except subprocess.TimeoutExpired:\n            ps_process.kill();ps_process.wait();raise'in newfunc and 'except BaseException:\n            ps_process.kill();raise'in newfunc)
check('checkTrue_nonzero_CalledProcessError_has_actual_args_stdout_stderr','raise subprocess.CalledProcessError(ps_returncode,ps_process.args,output=ps_stdout,stderr=ps_stderr)'in newfunc)
check('only_one_exact_captured_closed_PS_pid_discard',[ast.unparse(x)for x in ast.walk(newjoint)if isinstance(x,ast.Call)and isinstance(x.func,ast.Attribute)and x.func.attr in('discard','remove','difference','difference_update')]==['selected.discard(ps_diagnostic_pid)'])
check('exact_typed_closed_zero_before_only_exclusion',newfunc.index("type(ps_returncode)is int and ps_returncode==0")<newfunc.index('selected.discard(ps_diagnostic_pid)'))
check('full_original_descendant_closure_preserved',oldfunc[oldfunc.index('    selected={os.getpid()}'):oldfunc.index('    observed=subprocess.run(')].rstrip()==newfunc[newfunc.index('    selected={os.getpid()}'):newfunc.index('    # Exclude only')].rstrip())

evidence_root=P/'ACTUAL_PRIOR_N4_FAILURE_AND_NEW_DIAGNOSTIC_META'
inputs={
 'Root_actual_complete_observation_v4_pre_namespace_failure_tool_terminal_return.json':B/'Root_actual_complete_observation_v4_pre_namespace_failure_tool_terminal_return.json',
 'Root_actual_original_PS_lsof_own_process_scan_diagnostic_20261010.json':B/'Root_actual_original_PS_lsof_own_process_scan_diagnostic_20261010.json',
 'Root_actual_original_PS_lsof_diagnostic_tool_terminal_return.json':B/'Root_actual_original_PS_lsof_diagnostic_tool_terminal_return.json',
 'Root_actual_closed_PS_PID_only_lsof_comparison_diagnostic_20261010.json':B/'Root_actual_closed_PS_PID_only_lsof_comparison_diagnostic_20261010.json',
 'Root_actual_closed_PS_PID_only_lsof_comparison_tool_terminal_return.json':B/'Root_actual_closed_PS_PID_only_lsof_comparison_tool_terminal_return.json',
 'ACTUAL_ROOT_NEW_DIAGNOSTIC_SOURCE.py':Path('/private/tmp/spot_ROOT_closed_PS_PID_only_lsof_comparison_diagnostic_20261010.py'),
}
for q in sorted((B/'actual_complete_native_observation_BUILD5_AB_v4_receipts').iterdir()):
 assert q.is_file()and q.suffix=='.json';inputs['ROOT_ACTUAL_N4_SOURCE_ADMISSION_REQUEST_BIND_META/'+q.name]=q
failure_peer=Path('/private/tmp/axmat_N4_closed_pre_namespace_failure_META_independent_i0szs66h')
for q in sorted(failure_peer.rglob('*')):
 assert not q.is_symlink()
 if q.is_file():inputs['ACTUAL_INDEPENDENT_13_CHECK_SAVED_N4_FAILURE_META_PEER/'+str(q.relative_to(failure_peer))]=q
for rel,q in inputs.items():
 raw=read(q);put(evidence_root/rel,raw)
 if q.suffix=='.json':json.loads(raw)
diag=json.loads((evidence_root/'Root_actual_closed_PS_PID_only_lsof_comparison_diagnostic_20261010.json').read_bytes());term=json.loads((evidence_root/'Root_actual_closed_PS_PID_only_lsof_comparison_tool_terminal_return.json').read_bytes())
check('actual_new_diagnostic_full_pin_and_closed_tool_truth',READ_PINS[str(B/'Root_actual_closed_PS_PID_only_lsof_comparison_diagnostic_20261010.json')]['sha256']=='0fea855286e5770acd0a097b20096828d79ea01e5db50dfd2bf42324463c2fdd'and term['closed']is True and term['observed_terminal']is True and type(term['terminal_tool_return']['exit_code'])is int and term['terminal_tool_return']['exit_code']==0 and 'session_id'not in term['terminal_tool_return']and term['terminal_tool_return']['chunk_id']=='3bd6fc')
check('actual_comparison_kept_only_captured_PS_exclusion',type(diag['captured_ps_pid'])is int and diag['captured_PS_closed_EXIT0']is True and set(diag['original_selected_pids'])-set(diag['selected_pids_excluding_only_actual_closed_PS_diagnostic'])=={diag['captured_ps_pid']}and diag['all_other_selected_pids_preserved']is True)
check('actual_same_flags_lsof_original_one_fixed_zero_no_failure_reconstruction',diag['original_selection_lsof']['returncode']==1 and diag['closed_PS_only_excluded_lsof']['returncode']==0 and diag['same_original_lsof_flags_timeout_and_output_limit']is True and diag['original_N4_failure_lsof_raw_returncode_not_recovered']is True)
failure=json.loads((evidence_root/'Root_actual_complete_observation_v4_pre_namespace_failure_tool_terminal_return.json').read_bytes());check('actual_N4_closed_nonzero_before_namespaces_no_compile_material',failure['closed']is True and type(failure['terminal_tool_return']['exit_code'])is int and failure['terminal_tool_return']['exit_code']==1 and failure['new_native_compile_or_material_execution_observed']is False and failure['scientific_qualification_created']is False)
fp=json.loads((failure_peer/'REVIEW.json').read_bytes());check('actual_saved_failure_peer_13_typed_checks',fp['check_count']==13 and len(fp['checks'])==13 and all(type(x['passed'])is bool and x['passed']is True for x in fp['checks'])and fp['blockers']==[])
check('actual_original_PS_and_both_full_lsof_raw_stdout_preserved',all(type(x['stdout'])is str and type(x['stderr'])is str for x in (diag['ps'],diag['original_selection_lsof'],diag['closed_PS_only_excluded_lsof']))and len(diag['original_selection_lsof']['stdout'].encode())==2121 and len(diag['closed_PS_only_excluded_lsof']['stdout'].encode())==2121)

# Original compile Source archive is Source text, not material or numerical data.
index=json.loads((P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());archive=P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz'
with tarfile.open(archive,'r:gz')as tf:
 members=tf.getmembers();regular=[x for x in members if x.isfile()]
 # The exact original index layout is preserved and recorded; all archive
 # members are read through gzip EOF/CRC independently of its key conventions.
 total=0
 for member in regular:
  raw=tf.extractfile(member).read();assert len(raw)==member.size;total+=len(raw)
 check('original_full_compile_Source_archive_all_1365_member_EOF',len(regular)==1365 and total>0)
 ast_count=0
 for q in P.rglob('*.py'):ast.parse(q.read_bytes());ast_count+=1
 check('all_complete_Python_Source_AST_parse_only_no_import',ast_count>0)
newproof=dict(schema='N5_COMPLETE_JOINT_BYTES_CLOSED_PS_ONLY_FULL_SOURCE_INVERSE_V1',source_only=True,original_N4_manifest_pin=READ_PINS[str(OLD/'MANIFEST.json')],original_runtime_pin=READ_PINS[str(OLD/runtime)],new_runtime_pin=pin(P/runtime),changed_role='runtime_template',changed_definition='joint_bytes',whole_hunk_count=1,exact_finite_transforms=[dict(label='joint_bytes_capture_actual_closed_PS_and_exclude_only_it',old=oldfunc,new=newfunc,count=1)],complete_byte_inverse=True,complete_AST_inverse=True,all_other_96_original_N4_members_byte_exact=True,all_original_runtime_other_definitions_and_globals_byte_AST_exact=True,original_lsof_tail_bytes_exact=True,original_return_fields_order_types_unchanged=True,new_business_or_science_qualification=False)
dump(P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json',newproof)
request=json.loads((B/'actual_complete_native_observation_BUILD5_AB_v4_receipts/Root_actual_observation_build_binding_request.json').read_bytes())
namespace_fields=request['namespaces']
assert type(namespace_fields)is dict and set(namespace_fields)=={'host','output','control','source','receipts'}and all(type(v)is str for v in namespace_fields.values())
new_ns={k:v.replace('v4','v5')for k,v in namespace_fields.items()}
assert new_ns and all(v!=namespace_fields[k]for k,v in new_ns.items())
check('all_v5_future_namespaces_absent',all(not os.path.lexists(x)for x in new_ns.values()))
dump(P/'N5_FUTURE_ROOT_NAMESPACE_AND_SOURCE_ADMISSION_CONTRACT.UNREADY.json',dict(source_only=True,status='UNREADY_NEW_N5_ROOT_SOURCE_ADMISSION_REQUEST_BIND_REQUIRED',original_N4_namespaces=namespace_fields,required_new_v5_namespaces=new_ns,N4_actual_Source_admission_applies_to_N4_only=True,N5_actual_Source_admission_pin=None,N5_independent_Source_peer_pin=None,N5_actual_request_pin=None,N5_actual_Source_binding_pin=None,N5_actual_runtime_or_host_controls_qualification_pin=None,N5_actual_observation_build_material_result_pin=None,N5_actual_Source_object_archive_link_binary_proof_pin=None,N5_actual_native_context_aggregation_qualification_pin=None,N5_scientific_qualification_pin=None,all_original_future_global_None_and_science_false_preserved=True,all_original154inputs_and_five_compile_group_contract_preserved=True,original_caps=dict(whole=1800,stage=600,rss_mib=512,joint_HOCDE=2*2**30,history=96*2**30,free=8*2**30,threads=1,children=1,retries=0),no_general_lsof_rc_one_acceptance=True,only_actual_closed_diagnostic_PID_excluded=True))
put(P/'N5_ROOT_NEXT_STEPS_SOURCE_ONLY.txt',b'Independent complete Source review of new N5 exact manifest/full14roles and original N4 chain first. Root must write a fresh Source-only admission for N5, not reuse N4 admission. Run original request preparer only as Root Source/META with exact original129/tool6/library2 plus current full N5 author/peer/admission pins; choose every namespace from N5_FUTURE_ROOT_NAMESPACE_AND_SOURCE_ADMISSION_CONTRACT.UNREADY.json. Root alone Source-binds to a fresh D_v5 and independently reviews bound Source, freezes complete D. Then original preflight/caps/MRO and genuine host are used exactly once, with /bin/ps monitor access and no concurrent business child. Keep N4 failed63d442 and all new diagnostics as distinct actual events; original N4 lsof raw returncode remains unavailable/None. No new compile/material/input/native/science success is supplied here. Every original five compile group,1365Source14physicalhunks/12hostinverse/A thenB/154inputs/512/1800/600/2GiB/96GiB/8GiB/1/1/0 remains. Root must save actual business terminal under H before closed postclose E capture; D must never append; all H/O/C/D/E files/dirs and open-unlinked bytes remain counted, E legitimate own append uses original fullpin same-sort contract. Future actual pins remain None until genuine Root events.\n')
roles=ast.literal_eval(next(n.value for n in ast.parse((P/'bind_complete_observation_SOURCE_only.UNREADY.py').read_bytes()).body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ROLES'for x in n.targets)))
rolepins={k:pin(P/v)for k,v in roles.items()if k!='qualified_source_manifest'}
check('complete14role_names_preserved_manifest_only_future',len(roles)==14 and len(rolepins)==13)
dump(P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json',dict(schema='AUTHOR_COMPLETE_NATIVE_OBSERVATION_N5_CLOSED_PS_ONLY_SOURCE_REVIEW_V1',status='AUTHOR_SOURCE_ONLY_COMPLETE_UNREADY_NO_EXECUTION',source_only=True,author_not_independent_peer=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],actual_author_Source_roles_except_manifest=rolepins,original_N4_manifest=READ_PINS[str(OLD/'MANIFEST.json')],one_runtime_definition_hunk_only=True,all_other_original_N4_Source_byte_exact=True,diagnostic_source_does_not_reconstruct_original_N4_missing_raw=True,actual_prior_N4_failure_and_new_diagnostic_evidence_pins={rel:READ_PINS[str(q)]for rel,q in inputs.items()},candidate_helper_guard_PS_lsof_compiler_material_or_numeric_executed=False,new_business_or_science_qualification=False))
put(P/'AUTHOR_EXECUTED_N5_SOURCE_ONLY.py',Path(__file__).read_bytes())
for path,row in READ_PINS.items():assert pin(Path(path))==row
for rel,row in directories.items():assert i7((OLD if rel=='.'else OLD/rel).lstat())==row
dump(P/'N5_ALL_ORIGINAL_SOURCE_AND_SMALL_META_FULLPINS.json',dict(source_only=True,all_original_inputs_unchanged=True,pins=list(READ_PINS.values()),N4_original_directories=directories))
print(json.dumps(dict(source_only=True,package=str(P),runtime=pin(P/runtime),report=pin(P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json'),inverse=pin(P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json'),check_count=len(checks),all_checks_typed_true=True,all_original_inputs_unchanged=True,candidate_helper_guard_PS_lsof_compiler_material_or_numeric_executed=False,new_business_or_science_qualified=False)))

from pathlib import Path
import ast,hashlib,json,os,stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');P=R/'literal2_new_compare_duplicate_physical_release_source_20261014';D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<=64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes'];return s
def fn(t,name):return next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name==name)
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
pp=pin(P/'PLAN.json');sourcepin=pin(P/'release_literal2_duplicate_physical_v3.py');plan=load(pp);code=Path(sourcepin['path']).read_text();tree=ast.parse(code)
assert pp['sha256'].startswith('48dfaa08')and pp['size_bytes']==2589252 and sourcepin['sha256'].startswith('5a005327')and sourcepin['size_bytes']==5441
post=load(plan['post_review_pin']);tools=load(plan['post_tools_pin']);assert post['status']=='PASS_ACTUAL_COMPARE_THREE_V7_FAILURE_FACTS_POSTVERIFICATION'and post['failure']is None and post['actual_Root_integer_exit_code']==1 and post['actual_original_resource_failure_retained']is True
assert tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0
for k in ['actual_review_return','actual_postverification_return']:
 z=tools[k];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==plan['post_review_pin']
host=load(post['actual_aggregate_host_pin']);assert plan['fixed_current_pins']==host['fixed_current_pins']and len(plan['fixed_current_pins'])==6050
base=Path('/Users/wen/spot/validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence');owner=plan['retained_complete_owner_pin'];targets=plan['target_pins']
assert owner['path']==str(base/'A1/physical.jsonl')and [p['path']for p in targets]==[str(base/'A2/physical.jsonl'),str(base/'A3/physical.jsonl')]
assert len(targets)==2 and all(p in post['actual_complete_new_output_pins']and p['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60'and p['size_bytes']==34371817 for p in [owner,*targets])
assert post['all18_new_outputs_full_EOF_SHA_and_current7_verified']is True and plan['planned_released_bytes']==sum(p['size_bytes']for p in targets)==68743634
retained=plan['retained_new_output_pins'];assert retained==[p for p in post['actual_complete_new_output_pins']if p not in targets]and len(retained)==16 and owner in retained
assert not({p['path']for p in targets}&{p['path']for p in plan['fixed_current_pins']+retained})and len({p['identity'][1]for p in [owner,*targets]})==3
assert plan['prior_Root_exit_code']==1 and plan['prior_budget_failure_retained']is True and plan['physics_qualified']is False and plan['all_original_archives_and_saved_SQLite_pool_comparison_report_logs_retained']is True
scope=dict(Path=Path,os=os,stat=stat)
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn(tree,k)for k in ['require','identity','current']],type_ignores=[])),'<actual readonly current7 method>','exec'),scope)
for p in plan['fixed_current_pins']+retained+[owner,*targets]:assert scope['current'](p)==Path(p['path']);seven(p)
for p in [owner,*targets]:s=seven(p);assert s.st_nlink==1 and s.st_uid==os.getuid()and not any(a.is_symlink()for a in(Path(p['path']),*Path(p['path']).parents))
compiler=[p for p in plan['fixed_current_pins']if p['identity'][3]==2];assert len(compiler)==1 and compiler[0]['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'
system=[p for p in plan['fixed_current_pins']if Path(p['path']).lstat().st_uid==0];assert {p['path']for p in system}=={'/bin/ps','/usr/sbin/lsof'}
old=Path(P/'release_literal2_duplicate_physical.py').read_text()
before="q=Path(p['path']);s=q.lstat();require(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity']"
after="q=Path(p['path']);s=q.lstat();require(q.is_absolute()and stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity']"
assert old.count(before)==1;expected=old.replace(before,after)
expected=expected.replace("q=current(p);h=hashlib.sha256();fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)","q=current(p);require(p['identity'][3]==1 and q.lstat().st_uid==os.getuid(),'single-link owned release data and authority');h=hashlib.sha256();fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)")
expected=expected.replace("os.unlink('physical.jsonl',dir_fd=fd);os.fsync(fd)","os.unlink('physical.jsonl',dir_fd=fd);deleted.append(p);os.fsync(fd)").replace('    deleted.append(p)\n','')
assert expected==code
full=ast.get_source_segment(code,fn(tree,'full'));assert "p['identity'][3]==1 and q.lstat().st_uid==os.getuid()"in full and 'os.O_NOFOLLOW'in full and "'opened full7'"in full and "'closed full7'"in full and 'full EOF SHA'in full
assert "['/usr/sbin/lsof','-nP','-F','pfn','--',p['path']]"in code and 'z.returncode==1 and not z.stdout and not z.stderr'in code
execute=next(n for n in ast.walk(fn(tree,'main'))if isinstance(n,ast.If)and ast.unparse(n.test)=="a.mode == 'execute'")
unlinkcalls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and ast.unparse(n.func)=='os.unlink'];assert len(unlinkcalls)==1 and unlinkcalls[0]in list(ast.walk(execute))and ast.literal_eval(unlinkcalls[0].args[0])=='physical.jsonl'
releasefor=execute.body[0];assert isinstance(releasefor,ast.For)and ast.unparse(releasefor.iter)=='targets'
tryblock=next(n for n in releasefor.body if isinstance(n,ast.Try));calls=[ast.unparse(n.value.func)for n in tryblock.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)];assert calls==['require','os.unlink','deleted.append','os.fsync']
assert "os.stat('physical.jsonl',dir_fd=fd,follow_symlinks=False)"in code and 'os.O_DIRECTORY|os.O_NOFOLLOW'in code and "write(BASE/'ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_FAILED_RECEIPT.json',dict(failure=repr(e),actual_released_pins=deleted"in code
assert "with p.open('xb')"in code and 'f.flush();os.fsync(f.fileno())'in code and 'all(not os.path.lexists'in code
readonlyrawpin=pin(P/'ROOT_V3_READONLY_TRUE_TOOL_RETURNS.json');readonlyraw=load(readonlyrawpin);assert readonlyraw['observed_closed']is True and type(readonlyraw['original_integer_exit_code'])is int and readonlyraw['original_integer_exit_code']==0
returnkey=next(k for k,v in readonlyraw.items()if isinstance(v,dict)and v.get('exit_code')==0 and 'output'in v);rz=readonlyraw[returnkey];assert type(rz['exit_code'])is int and rz.get('session_id')is None
receiptpin=pin(P/'EXACT_LITERAL2_DUPLICATE_PHYSICAL_READONLY_RECEIPT.json');receipt=load(receiptpin);assert receiptpin['sha256'].startswith('27a0b2da')and receipt['status']=='EXACT_LITERAL2_READONLY_READY'and receipt['actual_released_pins']==[]and receipt['actual_released_bytes']==0 and receipt['failure']is None
assert receipt['plan_pin']==pp and receipt['exact_target_pins']==targets and receipt['retained_complete_owner_pin']==owner and receipt['original_Root_exit_code_retained']==1 and receipt['original_resource_failure_retained']is True
assert 'release_literal2_duplicate_physical_v3.py'in readonlyraw['exact_executed_command']
for p in plan['fixed_current_pins']+retained+[owner,*targets]:seven(p)
result=dict(schema='INDEPENDENT_LITERAL2_NEW_COMPARE_DUPLICATE_PHYSICAL_SELECTED_V3_SOURCE_REVIEW_V1',status='PASS_LITERAL2_NEW_COMPARE_DUPLICATE_PHYSICAL_SELECTED_V3_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,Source_candidate_PASS=True,selected_Source_pin=sourcepin,selected_plan_pin=pp,final_selected_Source_pins=[sourcepin,pp],actual_solo_compare_post_review_pin=plan['post_review_pin'],actual_solo_compare_post_tools_pin=plan['post_tools_pin'],actual_Root_v3_readonly_true_tool_pin=readonlyrawpin,actual_Root_v3_readonly_receipt_pin=receiptpin,actual_Root_v3_readonly_integer_exit_code=0,actual_readonly_deleted_count=0,retained_complete_owner_pin=owner,exact_target_pins=targets,actual_target_count=2,planned_target_bytes=68743634,exact6050_fixed_and16_new_outputs_retained=True,all_fixed_and_retained_current7_verified_twice=True,original_compiler_two_links_and_two_root_owned_system_tools_exact_identities_preserved=True,private_owner_and_targets_strict_single_link_current_UID_noalias_current7_preserved=True,three_duplicate_full_EOF_original_solepost_proofs_bound_no_peer_payload_reread=True,selected_v3_only_two_required_identity_and_partial_receipt_deltas_from_v1=True,exact_check_mode_has_no_unlink=True,execute_mode_only_two_literal_target_paths_unlink=True,exact_immediate_parentfd_noFollow_target7_before_unlink=True,unlink_success_recorded_before_directory_fsync_or_close=True,directory_fsync_and_file_fsync_receipts_preserved=True,partial_failure_actual_released_pins_recorded=True,no_generic_missing_or_device_skip_added=True,original_Root_exit_code_retained=1,original_resource_failure_retained=True,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,actual_execute_return=None,actual_execute_receipt_pin=None,reviewer_source_pin=pin(__file__))
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),Source_candidate_PASS=True,exact_target_count=2,planned_released_bytes=68743634,files_deleted=False)),flush=True)

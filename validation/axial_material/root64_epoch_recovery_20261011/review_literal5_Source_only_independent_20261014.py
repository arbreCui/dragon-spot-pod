import pathlib,json,ast,hashlib,os,stat,shlex
R=pathlib.Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
H=R/'storage_release_literal5_closed_failed_v15_private_source_v1_20261014'
O=R/'independent_literal5_closed_failed_v15_private_Source_review_20261014'
def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k] for k in ('path','sha256','size_bytes','identity')}
def eof(path,expect=None):
 p=pathlib.Path(path);s=p.lstat();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert seven(os.fstat(fd))==seven(s);pieces=[]
  while True:
   x=os.read(fd,1024*1024)
   if not x:break
   pieces.append(x)
  assert seven(os.fstat(fd))==seven(s)
 finally:os.close(fd)
 b=b''.join(pieces);assert seven(p.lstat())==seven(s) and stat.S_ISREG(s.st_mode)
 q={'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'identity':seven(s)}
 if expect is not None:assert q==norm(expect),(str(p),'EOF mismatch')
 return q,b
def load(path,expect=None):
 p,b=eof(path,expect);return p,json.loads(b)
def current(p):assert seven(os.lstat(p['path']))==p['identity'],p['path']
def defs(b):
 s=b.decode();return{n.name:ast.get_source_segment(s,n).encode() for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
sfp,sf=load(H/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json')
assert sfp['sha256']=='89bab0941d2a60a6134035c46763e613780dbfdd834d9030c880f6a39d1bd7d7'
assert sf['source_only'] is True and sf['manifest_prepared'] is False and sf['deletion_executed'] is False and sf['compiler_or_business_executed'] is False
for k in ['future_manifest_pin','future_readonly_receipt_pin','future_actual_release_receipt_pin']:assert sf[k] is None
assert sf['default_readonly'] is True and sf['execute_requires_one_literal_flag'] is True and sf['no_retry_or_overwrite'] is True and sf['qualification_promoted'] is False
sources={};sourcepins=[]
for p in sf['Source_pins']:
 q,b=eof(p['path'],p);ast.parse(b);sources[pathlib.Path(p['path']).name]=b;sourcepins.append(q)
ip,inv=load(sf['strict_low_level_Source_provenance_pin']['path'],sf['strict_low_level_Source_provenance_pin'])
pp,plan=load(sf['exact_role_plan_pin']['path'],sf['exact_role_plan_pin'])
oldsource={}
for key in ['old_common_source_pin','old_prepare_source_pin','old_verify_source_pin']:
 p,b=eof(inv[key]['path'],inv[key]);oldsource[pathlib.Path(p['path']).name]=b
change_counts={}
for rec in inv['whole_source_inverse_records']:
 new=sources[rec['new_name']];old=oldsource[rec['old_name']];lines=new.decode().splitlines(keepends=True)
 assert hashlib.sha256(new).hexdigest()==rec['new_sha256'] and hashlib.sha256(old).hexdigest()==rec['old_sha256']
 for block in reversed(rec['exact_change_blocks']):
  a,b=block['new_start_line0'],block['new_end_line0'];assert ''.join(lines[a:b])==block['new_exact_bytes'];lines[a:b]=block['old_exact_bytes'].splitlines(keepends=True)
 assert ''.join(lines).encode()==old and rec['whole_byte_inverse_matches_old_source'] is True
 change_counts[rec['new_name']]=len(rec['exact_change_blocks'])
newdefs=defs(sources['literal5_release_common.py']);olddefs=defs(oldsource['literal2_release_common.py'])
for name in inv['unchanged_shared_functions']:assert newdefs[name]==olddefs[name] and hashlib.sha256(newdefs[name]).hexdigest()==inv['shared_function_SHA256'][name]
assert inv['unchanged_shared_functions']==['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
v=sources['verify_or_execute_literal5.py'].decode();ov=oldsource['verify_or_execute_literal2.py'].decode()
start='                os.unlink(target.name,dir_fd=fd)';end='        for r in protected+'
nb=v[v.index(start):v.index(end,v.index(start))];ob=ov[ov.index(start):ov.index(end,ov.index(start))]
assert nb==ob and hashlib.sha256(nb.encode()).hexdigest()==inv['literal2_v2_complete_unlink_fsync_FirstFailure_block_SHA256']
assert "p.add_argument('--execute',action='store_true')" in v and "sys.argv[1:].count('--execute')!=(1 if a.execute else 0)" in v
assert v.index('if not a.execute:')<v.index('os.unlink(target.name,dir_fd=fd)')
assert v.index("value['deletion_records'].append")<v.index('os.fsync(fd)') and 'unlink_return_not_yet_observed=True' in v
assert 'actual.st_uid!=os.getuid()or actual.st_nlink!=1' in v and 'os.O_DIRECTORY|os.O_NOFOLLOW' in v
assert 'now[3]!=previous[3]-1' in v and 'now[4]!=previous[4]-32' in v and 'raise first_fd_error.with_traceback(first_fd_tb)' in v
assert "'STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY'" in v
const={}
for node in ast.parse(sources['literal5_release_common.py']).body:
 if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
  try:const[node.targets[0].id]=ast.literal_eval(node.value)
  except ValueError:pass
assert const['TARGET_SELECTED_PINS']==sf['literal5_fullpins']==plan['literal5_target_fullpins']
assert const['HISTORICAL_PINS']==sf['historical_evidence_pins'] and const['CURRENT_SELECTIONS']==sf['current_actual_selections'] and const['CLOSED_V15']==sf['closed_failed_v15_authority']
targets=sf['literal5_fullpins'];paths={p['path'] for p in targets};nodes={tuple(p['identity'][:2]) for p in targets}
assert len(paths)==len(nodes)==len(targets)==5 and sum(p['size_bytes'] for p in targets)==1478165640
for p in targets:
 current(p);s=os.lstat(p['path']);assert s.st_uid==os.getuid() and s.st_nlink==1 and stat.S_ISREG(s.st_mode)
oldmp,oldmf=load(sf['historical_evidence_pins']['previous7251_manifest']['path'],sf['historical_evidence_pins']['previous7251_manifest'])
rows=oldmf['current_protected_full_EOF_pins'];idx=[4160,4161,4294,4607,4612]
assert len(rows)==7251 and const['HISTORICAL_TARGET_INDICES']==plan['only_exact_migrated_indices']==idx
assert {rows[i]['path']:norm(rows[i]) for i in idx}=={p['path']:p for p in targets} and {p['path'] for p in rows}&paths==paths
keep=[p for i,p in enumerate(rows) if i not in idx];assert len(keep)==7246==plan['retained_previous_protected_count']
for p in keep:current(p);assert p['path'] not in paths and tuple(p['identity'][:2]) not in nodes
for p in plan['eight_v14_alias_candidates_retained']:current(p);assert p['path'] not in paths
assert len(plan['eight_v14_alias_candidates_retained'])==8 and plan['SPOASM_retained'] is True
cv=const['CLOSED_V15'];vp,summary=load(cv['summary_pin']['path'],cv['summary_pin'])
rtp,rt=load(cv['Root_true_tool_pin']['path'],cv['Root_true_tool_pin']);postp,post=load(cv['independent_postreview_pin']['path'],cv['independent_postreview_pin'])
ptp,pt=load(cv['independent_posttools_pin']['path'],cv['independent_posttools_pin']);arp,ar=load(cv['Root_exact_argv_pin']['path'],cv['Root_exact_argv_pin'])
t=rt['actual_terminal_return'];a=pt['actual_review_return']
assert rt['observed_closed'] is True and type(t['exit_code']) is int and t['exit_code']==1 and t.get('session_id') is None and shlex.split(rt['exact_executed_command'])==ar['argv'] and len(ar['argv'])==78
assert pt['observed_closed'] is True and type(a['exit_code']) is int and a['exit_code']==0 and a.get('session_id') is None and json.loads(a['output'].strip().splitlines()[-1])['review_pin']==postp and a['chunk_id']=='60e48a'
assert post['failure'] is None and post['summary_pin']==vp and post['actual_pipeline_tool_exit_code']==1 and post['all3011_fixed_seven_id_before_after_equal'] is True
assert len(summary['fixed_current_pins'])==3011 and len(summary['output_pins'])==191 and len(summary['owned_runtime_pins'])==119
assert summary['engineering_three_plane_closed0'] is False and summary['AAA_qualified'] is False and summary['ABA_admitted'] is False
for p in summary['fixed_current_pins']+summary['output_pins']+summary['owned_runtime_pins']+[vp]:current(p);assert p['path'] not in paths and tuple(p['identity'][:2]) not in nodes
assert sf['original_caps']==const['CAPS']==plan['original_budget_caps'] and sf['original_caps']['fresh_bytes']==2147483648 and sf['original_caps']['SELF_mib']==512
assert plan['reference_budget_prediction_is_not_admission'] is True and plan['actual_budget_required_after_future_release'] is True and plan['reference_predicted_reserve_remaining']==110319645
assert plan['remaining_owned_file_count_after_future_exact5']==323 and len(const['BASELINE_OWNED_INVENTORIES']['ordinary_file_identities'])==328
for p,i in const['BASELINE_OWNED_INVENTORIES']['ordinary_file_identities'].items():assert seven(os.lstat(p))==i
for p,i in const['BASELINE_OWNED_INVENTORIES']['directory_identities'].items():assert seven(os.lstat(p))==i
assert not const['BASELINE_OWNED_INVENTORIES']['symlinks']
for item in const['DOWNSTREAM_ORIGINS']:
 d=load(item['metadata_pin']['path'],item['metadata_pin'])[1]
 assert len(d['rows'])==item['current_row_count'] and [norm(x['current_pin']) for x in d['rows']]==item['current_pins']
 for p in item['current_pins']:current(p);assert p['path'] not in paths and tuple(p['identity'][:2]) not in nodes
assert [x['current_row_count'] for x in const['DOWNSTREAM_ORIGINS']]==[33,51]
for p in sourcepins+[sfp,ip,pp,oldmp,vp,rtp,postp,ptp,arp]:current(p)
report={'schema':'INDEPENDENT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_SOURCE_REVIEW_V1','status':'PASS_LITERAL5_EXACT_SOURCE_ONLY_READY_FOR_ROOT_MANIFEST_PREPARATION','failure':None,'source_only':True,'business_executed':False,'compiler_executed':False,'numerical_executed':False,'deletion_executed':False,'Source_imported':False,'Source_freeze_pin':sfp,'Source_pins':sourcepins,'inverse_pin':ip,'role_plan_pin':pp,'three_entire_Source_inverse_matches_literal2_v2':True,'exact_changed_block_counts':change_counts,'seven_shared_low_level_methods_wholebytes_equal':True,'complete_unlink_truthful_receipt_directory_fsync_firsterror_block_wholebytes_equal':True,'targets':targets,'target_count':5,'target_bytes':1478165640,'target_current_seven_id_UID_nlink1_nonsymlink_disjoint':True,'target_large_EOF_repeated':False,'previous7251_manifest_pin':oldmp,'only_exact_old_protected_indices_migrated_to_historical':idx,'original_other7246_current_seven_id_equal':True,'owned_old_v14_and_failedpublic5_before_file_count':328,'retained_owned_old_file_count_after_future_exact5':323,'eight_aliases_and_SPOASM_retained':True,'v15_summary_pin':vp,'Root_closed_failed_v15_true_tool_pin':rtp,'Root_exact78_argv_pin':arp,'independent_v15_failure_post0_pin':postp,'independent_v15_failure_post0_tools_pin':ptp,'actual_v15_business_exit_code':1,'v15_complete192_scene3011fixed119owned_current_protected':True,'material33_and_GENDF51_direct_current_science_protected':True,'default_readonly':True,'execute_requires_exactly_one_literal_execute_flag':True,'no_retry_or_overwrite':True,'strict_owned_receipt_same_inode_fsync_before_unlink':True,'actual_unlink_return_fsynced_before_target_directory_fsync_and_close':True,'first_exception_object_traceback_preserved':True,'exact_APFS_parent_nlink_minus1_size_minus32_per_unlink':True,'real_PS_and_lsof_gate_required_before_and_after':True,'original_caps':sf['original_caps'],'future_after_release_real_budget_admission_required':True,'reference_predicted_reserve_remaining_not_admission':110319645,'future_manifest_pin':None,'future_readonly_receipt_pin':None,'future_actual_release_receipt_pin':None,'science_full_EOF_repeated':False,'all_file_descriptors_closed':True,'qualification_promoted':False,'prior_reviewer_failure_preserved':'13bc08 EXIT1 own digest-span newline mismatch; c04ee4 and ce2f0f verified exact author AST and os.unlink span. No candidate Source defect or business failure was inferred.','limitation':'Source-only audit; Root must prepare actual full EOF manifest, default-readonly verification, writer gates and real after-release original reserve. Exact old5 private path replay will be lost only after a separately executed release.'}
O.mkdir();path=O/'REVIEW.json';b=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
try:
 view=memoryview(b)
 while view:view=view[os.write(fd,view):]
 os.fsync(fd)
finally:os.close(fd)
print(json.dumps({'status':report['status'],'review_pin':eof(path)[0],'Source_freeze_pin':sfp,'failure':None,'business_executed':False},ensure_ascii=False))

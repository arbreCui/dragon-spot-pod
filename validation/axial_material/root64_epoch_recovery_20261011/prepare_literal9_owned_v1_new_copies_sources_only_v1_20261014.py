"""Prepare nine closed failed-run input copies; no MF, solver, compiler or unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal11_next_A8_owned_views_duplicates_source_v1_20261014'
OUT=R/'storage_release_literal9_owned_v1_new_copies_source_v1_20261014'
POST=R/'independent_A8_18_owned_MAP_lifetime_v1_actual_monitor_access_failure_postverify_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
TOTAL=802234184
LABEL='LITERAL9_OWNED_V1_NEW_COPIES_DUPLICATES'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('only bounded Source metadata EOF')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  b=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('fd7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):
 if isinstance(p,dict):
  if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata PF')
  p=p['path']
 else:pin(p)
 return json.loads(Path(p).read_bytes())
def write(p,v):
 if isinstance(v,dict):v=(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 elif isinstance(v,str):v=v.encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(v);f.flush();os.fsync(f.fileno())
def inventory(root):
 out=dict(ordinary_file_identities={},directory_identities={},symlinks={});stack=[root]
 while stack:
  p=stack.pop();s=p.lstat();before=identity(s)
  if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary owner directory')
  out['directory_identities'][str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   if identity(os.fstat(fd))!=before:raise RuntimeError('dirfd7')
   with os.scandir(fd)as it:
    for e in it:
     q=p/e.name;t=e.stat(follow_symlinks=False)
     if stat.S_ISDIR(t.st_mode):stack.append(q)
     elif stat.S_ISREG(t.st_mode):out['ordinary_file_identities'][str(q)]=identity(t)
     else:raise RuntimeError('ordinary entries only')
   if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('dir after7')
  finally:os.close(fd)
 return out
MONITOR=r'''def monitor_closed_proof():
 d=read(CLOSED_OWNED_MONITOR_FAILED['summary_pin']);t=read(CLOSED_OWNED_MONITOR_FAILED['Root_true_tool_pin']);a=read(CLOSED_OWNED_MONITOR_FAILED['Root_exact_argv_pin']);p=read(CLOSED_OWNED_MONITOR_FAILED['independent_postreview_pin']);pt=read(CLOSED_OWNED_MONITOR_FAILED['independent_posttools_pin']);terminal=t['actual_terminal_return'];ret=pt['actual_review_return']
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_command']!=t['exact_executed_command']or len(a['exact_argv'])!=42:raise RuntimeError('actual failed Root42 typed terminal1')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(ret['exit_code'])is not int or ret['exit_code']!=0 or ret.get('session_id')is not None or b.norm(json.loads(ret['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_OWNED_MONITOR_FAILED['independent_postreview_pin']:raise RuntimeError('actual independent failed-monitor post0')
 if p['schema']!='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V1_ACTUAL_MONITOR_ACCESS_FAILURE_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_MONITOR_ACCESS_FAILURE_FACTS_POSTVERIFIED_NO_RUNTIME_QUALIFICATION'or p['failure']is not None or p['verification_failure']is not None or p['actual_report_pin']!=CLOSED_OWNED_MONITOR_FAILED['summary_pin']or p['actual_Root_true_tool_return_pin']!=CLOSED_OWNED_MONITOR_FAILED['Root_true_tool_pin']or p['actual_Root_exact_argv_pin']!=CLOSED_OWNED_MONITOR_FAILED['Root_exact_argv_pin']or p['actual_Host_freeze_pin']!=CLOSED_OWNED_MONITOR_FAILED['Host_freeze_pin']or p['actual_CLI_pin']!=CLOSED_OWNED_MONITOR_FAILED['exact_cli_pin']or p['actual_Root_exit_code']!=1 or p['actual_Root_closed']is not True or p['actual_stage_count']!=1 or p['actual_compiler_child_started']is not True or p['actual_compile_stage_passed']is not False or p['actual_compiled_object_exists']is not False or p['actual_link_executed']is not False or p['actual_BOOT_executed']is not False or p['actual_monitor_failure_is_bin_ps_permission_error']is not True or p['actual_monitor_own_child_group_was_terminated_minus15']is not True or p['actual_original_first_failure_object_traceback_preserved']is not True or p['current_fixed_count']!=3893 or p['current_HF_dependency_count']!=3892 or p['actual_output_file_count']!=16 or p['current_fixed_all7_twice_verified']is not True or p['current_HF_all7_twice_verified']is not True or p['current18_input_sources_all7_twice_preserved']is not True or p['actual_owner_bit_controls_or_runtime_lifetime_fix_not_proved']is not True or p['engineering_qualified']is not False or p['physics_qualified']is not False:raise RuntimeError('exact actual monitor PermissionError; no object link BOOT or math qualification')
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('readonly independent reviewer')
 if d['schema']!='ACTUAL_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_V1'or d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!=p['actual_summary_failure']or d['first_failure_secondary_errors']!=[]or d['actual_outcome']is not None or len(d['records'])!=1 or d['records'][0]['status']!='FAILED'or len(d['fixed_current_pins'])!=3893 or len(d['output_pins'])!=15 or d['engineering_qualified']is not False:raise RuntimeError('sealed original first failure preserved; partial module is not compiled-object qualification')
 return CLOSED_OWNED_MONITOR_FAILED'''
PROTECT=r'''def current_protection(sfpin,reviews):
 f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8733_manifest']);table={};roles={};cache={}
 rows=old['current_protected_full_EOF_pins']
 if len(rows)!=8733 or any(p['path']in TARGET_PATHS for p in rows):raise RuntimeError('all8733 protected rows preserved; new failed copied9 have no current MF role')
 def add(p,role):
  p=b.norm(p);path=p['path']
  if path in TARGET_PATHS:raise RuntimeError('nine generated failed-copy bodies are only historical declarations')
  actual=cache.get(path)
  if actual is None:actual=pin(path);cache[path]=actual
  elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected7 changed')
  if actual!=p or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected physical disjoint exact PF')
  if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
  table[path]=p;roles.setdefault(role,set()).add(path)
 for i,p in enumerate(rows):add(p,'unchanged_previous8733_index_'+str(i))
 before=inventory()
 if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=16 or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('all16 closed failed-scene ordinary files unchanged')
 retained=[]
 for path in sorted(before['ordinary_file_identities']):
  if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_seven_failed_scene_files_kept');retained.append(p)
 if len(retained)!=7:raise RuntimeError('exact nine copies only, all seven other files retained')
 current12=inventory([V12_OUT])
 if current12!=V12_BASELINE:raise RuntimeError('v12 unchanged')
 d=read(CLOSED_OWNED_MONITOR_FAILED['summary_pin']);hf=read(CLOSED_OWNED_MONITOR_FAILED['Host_freeze_pin'])
 if len(hf['dependencies'])!=3892 or len(d['fixed_current_pins'])!=3893 or len(d['output_pins'])!=15 or any(p['path']in TARGET_PATHS for p in hf['dependencies']+d['fixed_current_pins']):raise RuntimeError('all3892 HF and3893 fixed retained; no target current role')
 for p in [CLOSED_OWNED_MONITOR_FAILED['summary_pin'],CLOSED_OWNED_MONITOR_FAILED['Host_freeze_pin'],CLOSED_OWNED_MONITOR_FAILED['exact_cli_pin'],hf['host_source']]+hf['dependencies']+d['fixed_current_pins']:add(p,'unchanged_latest_failed_v1_current_fixed_and_HF')
 for p in ROLE_KEEP_PINS:add(p,'all_current18_original9_capture9_kept')
 for p in BIND_NEW_SOURCE_PINS:add(p,'original_math_and_owned18_Source_proofs_kept')
 for origin in DOWNSTREAM_ORIGINS:
  x=read(origin['metadata_pin'])
  if [b.norm(v['current_pin'])for v in x['rows']]!=origin['current_pins']or len(x['rows'])!=origin['current_row_count']:raise RuntimeError('material33 GENDF51 unchanged')
  add(origin['metadata_pin'],'downstream_metadata')
  for p in origin['current_pins']:add(p,'downstream_science')
 for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_reports_logs_immutable')
 for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_tools0')
 return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8733,all_original8733_PF_rows_data_retained=True,exact_current_HF3892_no_rows_migrated=True,explicit_exact9_historical_body_declarations=[dict(original_body_pin=p,original_live_role='closed_failed_v1_new_ordinary_input_copy',planned_next_role='EXACT_NINE_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True)for p in TARGET_SELECTED_PINS],retained_other_file_count=7,all_owner_directory_nodes_kept=True,all_original9_capture9_current18_and_current70_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12),retained,before'''
def main():
 if OUT.exists():raise RuntimeError('one new Source package')
 rp=pin(POST/'REVIEW.json');tp=pin(POST/'TRUE_TOOL_RETURNS.json');p=read(rp);t=read(tp);a=t['actual_review_return']
 if rp['sha256']!='b3b6c4d2734316b45c1d9101c7996b175d3a3e5288432f0b7e59ab307cefb77b'or tp['sha256']!='eafa3577315a2d2a34c7a7c15418c21e1fff977242ba9d7be21333c3faba609e'or type(a['exit_code'])is not int or a['exit_code']!=0 or a.get('session_id')is not None or t['observed_closed']is not True or norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('strict actual independent failure post0')
 latest=dict(summary_pin=p['actual_report_pin'],Root_true_tool_pin=p['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=p['actual_Root_exact_argv_pin'],Host_freeze_pin=p['actual_Host_freeze_pin'],exact_cli_pin=p['actual_CLI_pin'],independent_postreview_pin=rp,independent_posttools_pin=tp,actual_output_root=str(Path(p['actual_report_pin']['path']).parent))
 d=read(latest['summary_pin']);hf=read(latest['Host_freeze_pin']);hp=read(hf['diagnostic_host_plan_pin']);targets=[norm(x['owned_readonly_copy_pin'])for x in d['exact_owned_readonly_input_copy_proofs']];keep=hp['retained_original_v16_nine_input_pins']+hp['retained_latest_capture_nine_input_copy_pins']
 if len(targets)!=9 or sum(x['size_bytes']for x in targets)!=TOTAL or len(keep)!=18 or len({tuple(x['identity'][:2])for x in targets+keep})!=27 or len(hf['dependencies'])!=3892 or len(d['fixed_current_pins'])!=3893:raise RuntimeError('exact9 new ordinary duplicates and18 disjoint inputs')
 for row,target in zip(d['exact_owned_readonly_input_copy_proofs'],targets):
  original=norm(row['original_readonly_pin'])
  if original not in keep or target['sha256']!=original['sha256']or target['size_bytes']!=original['size_bytes']:raise RuntimeError('same whole body SHA retained capture original')
 for q in targets+keep:
  st=Path(q['path']).lstat()
  if identity(st)!=q['identity']or not stat.S_ISREG(st.st_mode)or st.st_uid!=os.getuid()or st.st_nlink!=1:raise RuntimeError('actual current UID singlelink seven')
 root=Path(latest['actual_output_root']);before=inventory(root)
 if before['symlinks']or len(before['ordinary_file_identities'])!=16 or set(before['ordinary_file_identities'])!={x['path']for x in d['output_pins']}|{latest['summary_pin']['path']}:raise RuntimeError('all16 actual owner files')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL11_NEXT_A8_OWNED_VIEWS_DUPLICATES_SOURCE_FREEZE.json');oldsf=read(oldsfpin);old=(OLD/NAMES[0]).read_text();current=old;changes=[];const={}
 for n in ast.parse(old).body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:const[n.targets[0].id]=ast.literal_eval(n.value)
   except(ValueError,TypeError):pass
 previous=R/'storage_release_literal11_next_A8_owned_views_duplicates_source_v1_20261014/EXACT_LITERAL11_NEXT_A8_OWNED_VIEWS_DUPLICATES_MANIFEST.json';mfpin=pin(previous);mf=read(mfpin)
 if len(mf['current_protected_full_EOF_pins'])!=8733 or any(x['path']in{q['path']for q in targets}for x in mf['current_protected_full_EOF_pins']+hf['dependencies']):raise RuntimeError('new nine copied bodies have no old current MF or HF rows')
 hist=dict(const['HISTORICAL_PINS']);hist.update(previous8733_manifest=mfpin,predecessor_cleanup_Source_freeze=oldsfpin,actual_owned_v1_monitor_failed_report=latest['summary_pin'],actual_owned_v1_monitor_failed_Root=latest['Root_true_tool_pin'],actual_owned_v1_monitor_failed_Root_argv=latest['Root_exact_argv_pin'],actual_owned_v1_monitor_failed_post=rp,actual_owned_v1_monitor_failed_post_tools=tp,actual_owned_v1_HF=latest['Host_freeze_pin'],actual_owned_v1_CLI=latest['exact_cli_pin'])
 sourcepins=list(const['BIND_NEW_SOURCE_PINS'])
 for folder in [R/'boot_v16_A8_18_owned_persistent_MAP_lifetime_source_v1_20261014',R/'boot_v16_A8_18_owned_MAP_lifetime_host_source_v1_20261014']:
  for q in sorted(folder.iterdir()):
   if q.is_file():sourcepins.append(pin(q))
 sourcepins.append(pin(R/'ACTUAL_A8_18_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json'));sourcepins=list({x['path']:x for x in sourcepins}.values())
 def change(before,after):
  nonlocal current
  if current.count(before)!=1:raise RuntimeError('unique Source splice')
  current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
 def node(name):return next(x for x in ast.parse(current).body if isinstance(x,ast.Assign)and len(x.targets)==1 and isinstance(x.targets[0],ast.Name)and x.targets[0].id==name)
 def assign(name,value):change(ast.get_source_segment(current,node(name)),name+'='+repr(value))
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[]),('HISTORICAL_HF_TARGET_INDICES',[]),('BASELINE_OWNED_INVENTORIES',before),('ROLE_KEEP_PINS',keep),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',16),('OWNER_DIRECTORY_COUNT',len(before['directory_identities']))]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path('+repr(str(root))+')]')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal9_owned_v1_new_copies_actual_receipts_20261014'\nCLOSED_OWNED_MONITOR_FAILED="+repr(latest))
 for k,v in [('SF','COMPLETE_LITERAL9_OWNED_V1_NEW_COPIES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL9_OWNED_V1_NEW_COPIES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 def fn(name):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==name))
 g=fn('source_gate');change(g,g.replace('LITERAL11_NEXT_A8_OWNED_VIEWS_DUPLICATES',LABEL).replace('len(TARGETS)!=11','len(TARGETS)!=9').replace('len(TARGET_PATHS)!=11','len(TARGET_PATHS)!=9').replace("f['closed_latest_capture_probe_authority']!=CLOSED_LATEST_CAPTURE","f['closed_latest_capture_probe_authority']!=CLOSED_LATEST_CAPTURE or f['closed_owned_v1_monitor_failed_authority']!=CLOSED_OWNED_MONITOR_FAILED"))
 g=fn('disjoint');change(g,g.replace('!=11','!=9'))
 g=fn('closed_proofs');tail='    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9,CLOSED_LATEST_A8,CLOSED_LATEST_CAPTURE]'
 if g.count(tail)!=1:raise RuntimeError('complete eleven original authorities')
 change(g,g.replace(tail,'    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9,CLOSED_LATEST_A8,CLOSED_LATEST_CAPTURE,monitor_closed_proof()]')+'\n\n'+MONITOR)
 change(fn('current_protection'),PROTECT);ast.parse(current)
 other=[]
 for name in NAMES[1:]:
  beforetext=(OLD/name).read_text();after=beforetext.replace('LITERAL11_NEXT_A8_OWNED_VIEWS_DUPLICATES',LABEL).replace('target_count=11','target_count=9').replace("m['target_count']!=11","m['target_count']!=9").replace("before['regular_files']-after['regular_files']!=11","before['regular_files']-after['regular_files']!=9").replace('deleted_files=11','deleted_files=9');ast.parse(after);other.append((name,beforetext,after))
 funcs=lambda s:{x.name:ast.get_source_segment(s,x)for x in ast.parse(s).body if isinstance(x,ast.FunctionDef)}
 low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(old)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven low-level methods wholebytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";original=other[1][1];new=other[1][2]
 if original[original.index(start):original.index(end)]!=new[new.index(start):new.index(end)]:raise RuntimeError('unlink-returnreceipt-dirfsync-FirstFailure original bytes')
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,after in other:write(OUT/name,after)
 pp=OUT/'EXACT_LITERAL9_OWNED_V1_NEW_COPIES_ROLE_SOURCE_PLAN.json';write(pp,dict(schema='EXACT_LITERAL9_OWNED_V1_NEW_COPIES_ROLE_SOURCE_PLAN_V1',source_only=True,literal9_fullpins=targets,target_count=9,target_bytes=TOTAL,previous8733_manifest_pin=mfpin,all8733_original_current_rows_retained=True,current_HF3892_pin=latest['Host_freeze_pin'],all3892_original_current_rows_retained=True,no_current_MF_or_HF_rows_migrated=True,current18_input_pins=keep,complete_owner_inventory=before,owner_file_count=16,retained_other_file_count=7,exact_closed_monitor_failure_authority=latest,original_caps=const['CAPS'],legacy_three_Script_basenames_and_literal11_fullpins_SF_key_retained_for_unchanged_low_level_contract=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,predicted_margin_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/name),candidate_pin=pin(OUT/name),changes=[dict(before=a,after=b)])for name,a,b in other]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('unique inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('complete inverse')
 ip=OUT/'COMPLETE_LITERAL11_TO_LITERAL9_OWNED_V1_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_LITERAL11_TO_LITERAL9_OWNED_V1_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);sf.update(schema='COMPLETE_LITERAL9_OWNED_V1_NEW_COPIES_DUPLICATES_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal9_fullpins=targets,target_count=9,target_bytes=TOTAL,historical_evidence_pins=hist,closed_owned_v1_monitor_failed_authority=latest,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=OUT/'COMPLETE_LITERAL9_OWNED_V1_NEW_COPIES_SOURCE_FREEZE.json';write(sp,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT9_FAILED_V1_NEW_ORDINARY_INPUT_COPIES_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),target_count=9,target_bytes=TOTAL,retained_other_file_count=7,old_current_MF8733_and_HF3892_all_preserved=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)))
if __name__=='__main__':main()

"""Prepare nine closed failed-run input copies; no MF, solver, compiler or unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal9_owned_v1_new_copies_source_v1_20261014'
OUT=R/'storage_release_literal18_capture_and_owned_duplicate_nines_source_v1_20261014'
POST=R/'independent_A8_18_owned_MAP_lifetime_v2_actual_runtime_postverify_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
TOTAL=1604468368
LABEL='LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES'
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
MONITOR="def runtime_completed_proof():\n d=read(CLOSED_RUNTIME_COMPLETED['summary_pin']);t=read(CLOSED_RUNTIME_COMPLETED['Root_true_tool_pin']);a=read(CLOSED_RUNTIME_COMPLETED['Root_exact_argv_pin']);p=read(CLOSED_RUNTIME_COMPLETED['independent_postreview_pin']);pt=read(CLOSED_RUNTIME_COMPLETED['independent_posttools_pin']);terminal=t['actual_terminal_return'];ret=pt['actual_review_return']\n if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_command']!=t['exact_executed_command']or len(a['exact_argv'])!=42:raise RuntimeError('original Root1 completion parser failure retained')\n if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(ret['exit_code'])is not int or ret['exit_code']!=0 or ret.get('session_id')is not None or b.norm(json.loads(ret['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_RUNTIME_COMPLETED['independent_postreview_pin']:raise RuntimeError('only genuine independently completed pair readback0')\n if p['schema']!='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_THREE_STAGE0_COMPLETE_PAIR_FACTS_POSTVERIFIED_HOST_COMPLETION_PARSER_FAILURE_RETAINED'or p['failure']is not None or p['verification_failure']is not None or p['actual_report_pin']!=CLOSED_RUNTIME_COMPLETED['summary_pin']or p['actual_Root_true_tool_return_pin']!=CLOSED_RUNTIME_COMPLETED['Root_true_tool_pin']or p['actual_Root_exact_argv_pin']!=CLOSED_RUNTIME_COMPLETED['Root_exact_argv_pin']or p['actual_Host_freeze_pin']!=CLOSED_RUNTIME_COMPLETED['Host_freeze_pin']or p['actual_CLI_pin']!=CLOSED_RUNTIME_COMPLETED['exact_cli_pin']or p['actual_Root_exit_code']!=1 or p['actual_Root_closed']is not True or p['actual_stage_count']!=3 or p['actual_BOOT_exit_code']!=0 or p['actual_single_BOOT_completed']is not True or p['actual_Host_completion_parser_failure_observed']is not True or p['actual_host_summary_failed_status_and_outcomeNone_preserved']is not True or p['actual_original_first_failure_object_traceback_preserved']is not True or p['actual_completion_stdout_unique']is not True or p['actual_terminal_pair_full370x3_readback_verified']is not True or p['actual_Fortran_complete_copy_readback']!={'schema':'ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1','status':'PASS','all_payload_bits_equal':True,'complete_lifecycle_checked':True,'groups':370,'planes':3,'epoch':0,'AAA_qualified':False,'ABA_admitted':False}or p['actual_terminal_pair_readback']!=p['complete_terminal_readback']or p['only_ordered70_index1_changed']is not True or p['actual_other69_ordered70_inputs_full_EOF_unchanged']is not True or p['actual_module6092_fullSHA_matches_original']is not True or p['all_three_watches_closed_without_limit_failure']is not True or p['current_fixed_count']!=3906 or p['current_HF_dependency_count']!=3905 or p['actual_output_file_count']!=24 or p['current_fixed_all7_twice_verified']is not True or p['current_HF_all7_twice_verified']is not True or p['current18_input_sources_all7_twice_preserved']is not True or p['engineering_qualified']is not False or p['physics_qualified']is not False or p['full50_executed']is not False:raise RuntimeError('actual threeStage0/singleBOOT0/pair readback0 facts; no full50 qualification')\n if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('independent readonly post')\n if d['schema']!='ACTUAL_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_V1'or d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!=p['actual_summary_failure']or d['first_failure_secondary_errors']!=[]or d['actual_outcome']is not None or len(d['records'])!=3 or [r['status']for r in d['records']]!=['PASS','PASS','PASS']or len(d['fixed_current_pins'])!=3906 or len(d['output_pins'])!=23 or d['engineering_qualified']is not False:raise RuntimeError('original sealed failed Host metadata retained with actual stage0 facts')\n return CLOSED_RUNTIME_COMPLETED"
PROTECT="def current_protection(sfpin,reviews):\n f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8779_manifest']);table={};roles={};cache={};historical=[];rows=old['current_protected_full_EOF_pins']\n if len(rows)!=8779 or len(HISTORICAL_TARGET_INDICES)!=9 or [b.norm(rows[i])for i in HISTORICAL_TARGET_INDICES]!=TARGET_SELECTED_PINS[:9]or {p['path']for p in rows}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[:9]}:raise RuntimeError('MF8779 only exact9 capture input rows historical; other8770 preserved')\n def add(p,role):\n  p=b.norm(p);path=p['path']\n  if path in TARGET_PATHS:\n   if p!=next(q for q in TARGET_SELECTED_PINS if q['path']==path):raise RuntimeError('exact18 original declared fullpin')\n   historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_EIGHTEEN_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return\n  actual=cache.get(path)\n  if actual is None:actual=pin(path);cache[path]=actual\n  elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7')\n  if actual!=p or tuple(p['identity'][:2])in{tuple(q['identity'][:2])for q in TARGET_SELECTED_PINS}:raise RuntimeError('current fullpin and physical disjoint')\n  if path in table and table[path]!=p:raise RuntimeError('inconsistent current fullpin')\n  table[path]=p;roles.setdefault(role,set()).add(path)\n for i,p in enumerate(rows):add(p,'previous8779_exact_index_'+str(i))\n before=inventory()\n if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=OWNER_FILE_COUNT or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('complete two closed owners unchanged')\n retained=[]\n for path in sorted(before['ordinary_file_identities']):\n  if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_two_owner_files_and_success_pair_kept');retained.append(p)\n if len(retained)!=OWNER_FILE_COUNT-18:raise RuntimeError('only exact18 ordinary duplicate copies removed')\n current12=inventory([V12_OUT])\n if current12!=V12_BASELINE:raise RuntimeError('v12 unchanged')\n d=read(CLOSED_RUNTIME_COMPLETED['summary_pin']);hf=read(CLOSED_RUNTIME_COMPLETED['Host_freeze_pin'])\n if len(hf['dependencies'])!=3905 or len(d['fixed_current_pins'])!=3906 or len(d['output_pins'])!=23 or len(HISTORICAL_HF_TARGET_INDICES)!=9 or [b.norm(hf['dependencies'][i])for i in HISTORICAL_HF_TARGET_INDICES]!=TARGET_SELECTED_PINS[:9]or {p['path']for p in hf['dependencies']}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[:9]}:raise RuntimeError('HF3905 exact9 capture input history, all other3896 retained')\n for p in [CLOSED_RUNTIME_COMPLETED['summary_pin'],CLOSED_RUNTIME_COMPLETED['Host_freeze_pin'],CLOSED_RUNTIME_COMPLETED['exact_cli_pin'],hf['host_source']]+hf['dependencies']+d['fixed_current_pins']+d['output_pins']+d['owned_runtime_pins']:add(p,'actual_runtime_current_root_with_only_exact18_history')\n post=read(CLOSED_RUNTIME_COMPLETED['independent_postreview_pin'])\n for p in [post['actual_terminal_axial_pin'],post['actual_terminal_archive_pin'],post['actual_new_object1_pin'],post['actual_Module_ABI_pin'],post['actual_Fortran_Source_freeze_pin']]:add(p,'successful_pair_and_runtime_code_current')\n for p in ROLE_KEEP_PINS:add(p,'all_original_scientific9_current_input_role_kept')\n for p in BIND_NEW_SOURCE_PINS:add(p,'all_Fortran_and_Source_proofs_kept')\n for origin in DOWNSTREAM_ORIGINS:\n  x=read(origin['metadata_pin'])\n  if [b.norm(v['current_pin'])for v in x['rows']]!=origin['current_pins']or len(x['rows'])!=origin['current_row_count']:raise RuntimeError('material33 GENDF51 unchanged')\n  add(origin['metadata_pin'],'downstream_metadata')\n  for p in origin['current_pins']:add(p,'downstream_science')\n for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_reports_logs_immutable')\n for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_tools0')\n return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8779,exact_previous_MF9_indices_migrated_to_history=HISTORICAL_TARGET_INDICES,all_other8770_PF_rows_data_retained=True,exact_current_HF3905_indices_migrated_to_history=HISTORICAL_HF_TARGET_INDICES,explicit_exact18_historical_body_declarations=historical,retained_other_file_count=len(retained),all_owner_directory_nodes_kept=True,all_original_science9_and_success_pair_and_current70_kept=True,next_full50_inputs_use_original_scientific9_only=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12),retained,before"
def main():
 if OUT.exists():raise RuntimeError('one new Source package')
 rp=pin(POST/'REVIEW.json');tp=pin(POST/'TRUE_TOOL_RETURNS.json');p=read(rp);t=read(tp);a=t['actual_review_return']
 if rp['sha256']!='e7cb7036ca25e60604b6270e459b44122a3129b51b07ce71202e13c70d27ac24'or tp['sha256']!='75babd25ace45f4ca2076e3e5424bbf19266419f295640440a2efc5fe0d9f23b'or type(a['exit_code'])is not int or a['exit_code']!=0 or a.get('session_id')is not None or t['observed_closed']is not True or norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('strict actual independent failure post0')
 latest=dict(summary_pin=p['actual_report_pin'],Root_true_tool_pin=p['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=p['actual_Root_exact_argv_pin'],Host_freeze_pin=p['actual_Host_freeze_pin'],exact_cli_pin=p['actual_CLI_pin'],independent_postreview_pin=rp,independent_posttools_pin=tp,actual_output_root=str(Path(p['actual_report_pin']['path']).parent))
 d=read(latest['summary_pin']);hf=read(latest['Host_freeze_pin']);hp=read(hf['diagnostic_host_plan_pin']);targets=[norm(x['original_readonly_pin'])for x in d['exact_owned_readonly_input_copy_proofs']]+[norm(x['owned_readonly_copy_pin'])for x in d['exact_owned_readonly_input_copy_proofs']];keep=hp['retained_original_v16_nine_input_pins']
 if len(targets)!=18 or sum(x['size_bytes']for x in targets)!=TOTAL or len(keep)!=9 or len({tuple(x['identity'][:2])for x in targets+keep})!=27 or len(hf['dependencies'])!=3905 or len(d['fixed_current_pins'])!=3906:raise RuntimeError('exact9 new ordinary duplicates and18 disjoint inputs')
 for row,target in zip(d['exact_owned_readonly_input_copy_proofs'],targets[9:]):
  original=norm(row['original_readonly_pin'])
  if original not in targets[:9] or not any(q['sha256']==original['sha256']and q['size_bytes']==original['size_bytes']for q in keep)or target['sha256']!=original['sha256']or target['size_bytes']!=original['size_bytes']:raise RuntimeError('same whole body SHA retained capture original')
 for q in targets+keep:
  st=Path(q['path']).lstat()
  if identity(st)!=q['identity']or not stat.S_ISREG(st.st_mode)or st.st_uid!=os.getuid()or st.st_nlink!=1:raise RuntimeError('actual current UID singlelink seven')
 root=Path(latest['actual_output_root']);roots=[Path(targets[0]['path']).parents[1],root];before=dict(ordinary_file_identities={},directory_identities={},symlinks={})
 for branch in roots:
  inv=inventory(branch)
  for key in before:
   if set(before[key])&set(inv[key]):raise RuntimeError('distinct owner roots')
   before[key].update(inv[key])
 ownerfiles=len(before['ordinary_file_identities']);ownerdirs=len(before['directory_identities'])
 if before['symlinks']or set(inventory(root)['ordinary_file_identities'])!={x['path']for x in d['output_pins']}|{latest['summary_pin']['path']}or not set(x['path']for x in targets)<=set(before['ordinary_file_identities']):raise RuntimeError('all16 actual owner files')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL9_OWNED_V1_NEW_COPIES_SOURCE_FREEZE.json');oldsf=read(oldsfpin);old=(OLD/NAMES[0]).read_text();current=old;changes=[];const={}
 for n in ast.parse(old).body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:const[n.targets[0].id]=ast.literal_eval(n.value)
   except(ValueError,TypeError):pass
 previous=R/'storage_release_literal9_owned_v1_new_copies_source_v1_20261014/EXACT_LITERAL9_OWNED_V1_NEW_COPIES_MANIFEST.json';mfpin=pin(previous);mf=read(mfpin)
 def indices(rows):
  out=[]
  for q in targets[:9]:
   ix=[i for i,p in enumerate(rows)if norm(p)==q]
   if len(ix)!=1:raise RuntimeError('unique exact9 current rows')
   out+=ix
  return out
 mi=indices(mf['current_protected_full_EOF_pins']);hi=indices(hf['dependencies'])
 if len(mf['current_protected_full_EOF_pins'])!=8779 or {q['path']for q in targets}&{q['path']for q in mf['current_protected_full_EOF_pins']}!={q['path']for q in targets[:9]}or {q['path']for q in targets}&{q['path']for q in hf['dependencies']}!={q['path']for q in targets[:9]}:raise RuntimeError('only9 capture inputs current; nine new owned copies not current')
 hist=dict(const['HISTORICAL_PINS']);hist.update(previous8779_manifest=mfpin,predecessor_cleanup_Source_freeze=oldsfpin,actual_owned_v2_runtime_report=latest['summary_pin'],actual_owned_v2_runtime_Root=latest['Root_true_tool_pin'],actual_owned_v2_runtime_Root_argv=latest['Root_exact_argv_pin'],actual_owned_v2_runtime_post=rp,actual_owned_v2_runtime_post_tools=tp,actual_owned_v2_HF=latest['Host_freeze_pin'],actual_owned_v2_CLI=latest['exact_cli_pin'])
 sourcepins=list(const['BIND_NEW_SOURCE_PINS'])
 for folder in [R/'boot_v16_A8_18_owned_persistent_MAP_lifetime_source_v1_20261014',R/'boot_v16_A8_18_owned_MAP_lifetime_host_source_v1_20261014',R/'boot_v16_A8_18_owned_MAP_lifetime_host_source_v2_20261014']:
  for q in sorted(folder.iterdir()):
   if q.is_file():sourcepins.append(pin(q))
 sourcepins.append(pin(R/'ACTUAL_A8_18_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json'));sourcepins=list({x['path']:x for x in sourcepins}.values())
 def change(before,after):
  nonlocal current
  if current.count(before)!=1:raise RuntimeError('unique Source splice')
  current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
 def node(name):return next(x for x in ast.parse(current).body if isinstance(x,ast.Assign)and len(x.targets)==1 and isinstance(x.targets[0],ast.Name)and x.targets[0].id==name)
 def assign(name,value):change(ast.get_source_segment(current,node(name)),name+'='+repr(value))
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',mi),('HISTORICAL_HF_TARGET_INDICES',hi),('BASELINE_OWNED_INVENTORIES',before),('ROLE_KEEP_PINS',keep),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',ownerfiles),('OWNER_DIRECTORY_COUNT',len(before['directory_identities']))]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal18_capture_and_owned_duplicate_nines_actual_receipts_20261014'\nCLOSED_RUNTIME_COMPLETED="+repr(latest))
 for k,v in [('SF','COMPLETE_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 def fn(name):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==name))
 g=fn('source_gate');change(g,g.replace('LITERAL9_OWNED_V1_NEW_COPIES_DUPLICATES',LABEL).replace('len(TARGETS)!=9','len(TARGETS)!=18').replace('len(TARGET_PATHS)!=9','len(TARGET_PATHS)!=18').replace("f['closed_owned_v1_monitor_failed_authority']!=CLOSED_OWNED_MONITOR_FAILED","f['closed_owned_v1_monitor_failed_authority']!=CLOSED_OWNED_MONITOR_FAILED or f['closed_runtime_completed_authority']!=CLOSED_RUNTIME_COMPLETED"))
 g=fn('disjoint');change(g,g.replace('!=9','!=18'))
 g=fn('closed_proofs');tail='    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9,CLOSED_LATEST_A8,CLOSED_LATEST_CAPTURE,monitor_closed_proof()]'
 if g.count(tail)!=1:raise RuntimeError('complete eleven original authorities')
 change(g,g.replace(tail,'    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9,CLOSED_LATEST_A8,CLOSED_LATEST_CAPTURE,monitor_closed_proof(),runtime_completed_proof()]')+'\n\n'+MONITOR)
 change(fn('current_protection'),PROTECT);ast.parse(current)
 other=[]
 for name in NAMES[1:]:
  beforetext=(OLD/name).read_text();after=beforetext.replace('LITERAL9_OWNED_V1_NEW_COPIES_DUPLICATES',LABEL).replace('target_count=9','target_count=18').replace("m['target_count']!=9","m['target_count']!=18").replace("before['regular_files']-after['regular_files']!=9","before['regular_files']-after['regular_files']!=18").replace('deleted_files=9','deleted_files=18');ast.parse(after);other.append((name,beforetext,after))
 funcs=lambda s:{x.name:ast.get_source_segment(s,x)for x in ast.parse(s).body if isinstance(x,ast.FunctionDef)}
 low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(old)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven low-level methods wholebytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";original=other[1][1];new=other[1][2]
 if original[original.index(start):original.index(end)]!=new[new.index(start):new.index(end)]:raise RuntimeError('unlink-returnreceipt-dirfsync-FirstFailure original bytes')
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,after in other:write(OUT/name,after)
 pp=OUT/'EXACT_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_ROLE_SOURCE_PLAN.json';write(pp,dict(schema='EXACT_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_ROLE_SOURCE_PLAN_V1',source_only=True,literal18_fullpins=targets,target_count=18,target_bytes=TOTAL,previous8779_manifest_pin=mfpin,exact_current_MF9_indices_migrated_to_history=mi,all_other8770_PF_rows_retained=True,current_HF3905_pin=latest['Host_freeze_pin'],exact_current_HF9_indices_migrated_to_history=hi,all_other3896_PF_rows_retained=True,current_original_science9_input_pins=keep,complete_owner_inventory=before,owner_file_count=ownerfiles,retained_other_file_count=ownerfiles-18,exact_closed_monitor_failure_authority=latest,original_caps=const['CAPS'],legacy_three_Script_basenames_and_literal11_fullpins_SF_key_retained_for_unchanged_low_level_contract=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,predicted_margin_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/name),candidate_pin=pin(OUT/name),changes=[dict(before=a,after=b)])for name,a,b in other]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('unique inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('complete inverse')
 ip=OUT/'COMPLETE_LITERAL9_TO_LITERAL18_DUPLICATE_NINES_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_LITERAL9_TO_LITERAL18_DUPLICATE_NINES_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);del sf['literal9_fullpins'];sf.update(schema='COMPLETE_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal18_fullpins=targets,target_count=18,target_bytes=TOTAL,historical_evidence_pins=hist,closed_runtime_completed_authority=latest,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=OUT/'COMPLETE_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_SOURCE_FREEZE.json';write(sp,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT18_DUPLICATE_NINES_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),target_count=18,target_bytes=TOTAL,retained_other_file_count=ownerfiles-18,old_MF8779_and_HF3905_only_exact9_current_rows_historical=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)))
if __name__=='__main__':main()

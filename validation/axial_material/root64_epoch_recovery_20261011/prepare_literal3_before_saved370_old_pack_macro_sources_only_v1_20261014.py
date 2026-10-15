"""Prepare exact3 Source only; no MF, compiler, solver, body rehash or unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal18_capture_and_owned_duplicate_nines_source_v1_20261014'
OUT=R/'storage_release_literal3_before_saved370_old_pack_and_macro_source_v1_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
LABEL='LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO';TOTAL=526645544
INDICES=[2605,4177,4467]
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded ordinary Source metadata only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def read(p):
 if isinstance(p,dict):
  if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata fullPF')
  p=p['path']
 else:pin(p)
 return json.loads(Path(p).read_bytes())
def write(p,v):
 raw=v.encode()if isinstance(v,str)else v if isinstance(v,bytes)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def inventory(roots):
 out=dict(ordinary_file_identities={},directory_identities={},symlinks={});stack=list(roots)
 while stack:
  p=stack.pop();s=p.lstat();before=identity(s)
  if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary closed owner directory')
  out['directory_identities'][str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   if identity(os.fstat(fd))!=before:raise RuntimeError('dirfd7')
   with os.scandir(fd)as it:
    for e in it:
     q=p/e.name;t=e.stat(follow_symlinks=False)
     if stat.S_ISDIR(t.st_mode):stack.append(q)
     elif stat.S_ISREG(t.st_mode):out['ordinary_file_identities'][str(q)]=identity(t)
     else:raise RuntimeError('ordinary owner entries only')
   if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('directory after7')
  finally:os.close(fd)
 return out
FULL50="""def full50_closed_proof():
 d=read(CLOSED_FULL50['summary_pin']);t=read(CLOSED_FULL50['Root_true_tool_pin']);a=read(CLOSED_FULL50['Root_exact_argv_pin']);p=read(CLOSED_FULL50['independent_postreview_pin']);pt=read(CLOSED_FULL50['independent_posttools_pin']);hf=read(CLOSED_FULL50['Host_freeze_pin']);cli=read(CLOSED_FULL50['exact_cli_pin'])
 terminal=t['actual_terminal_return']
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(terminal['exit_code'])is not int or terminal['exit_code']!=0 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_command']!=t['exact_executed_command']or a['exact_argv']!=cli['exact_reviewable_argv']or len(a['exact_argv'])!=96 or a['Host_freeze_pin']!=CLOSED_FULL50['Host_freeze_pin']or a['interface_pin']!=CLOSED_FULL50['exact_cli_pin']:raise RuntimeError('genuine latest full50 Root0/exact96/frozenown authority')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('independent latest full50 closed0')
 for k in('actual_review_return','actual_postverification_return'):
  q=pt[k]
  if type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or b.norm(json.loads(q['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_FULL50['independent_postreview_pin']:raise RuntimeError('latest full50 exact independent originalstdout review0')
 if p['schema']!='READONLY_ACTUAL_V18_FULL50_ENGINEERING_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_V18_FULL50_ENGINEERING_POSTVERIFICATION'or p['failure']is not None or p['actual_report_pin']!=CLOSED_FULL50['summary_pin']or p['actual_Root_true_tool_return_pin']!=CLOSED_FULL50['Root_true_tool_pin']or p['actual_Root_argv_pin']!=CLOSED_FULL50['Root_exact_argv_pin']or p['actual_Host_freeze_pin']!=CLOSED_FULL50['Host_freeze_pin']or p['actual_CLI_pin']!=CLOSED_FULL50['exact_cli_pin']or p['actual_Root_exit_code']!=0 or p['actual_stage_count']!=50 or p['actual_positive_count']!=17 or p['actual_exact_refusal_count']!=33 or any(p[k]is not True for k in('actual_ordered50_labels_verified','actual_exact33_case_message_mapping_verified','actual_engineering_three_plane_closed0','all_actual_child_watch_limit_failures_absent','actual_complete_pair_payload_bits_equal','all_current_output_pins_full_EOF_SHA_all7'))or any(p[k]is not False for k in('independent_business_executed','independent_compiler_executed','independent_numerical_executed','independent_deletion_executed','physics_qualified')):raise RuntimeError('actual full50 strict post fields; engineering only no physics')
 if d['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or d['status']!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or d['failure']is not None or d['after_check_error']is not None or d['first_failure_secondary_errors']!=[]or d['engineering_three_plane_closed0']is not True or len(d['records'])!=50 or sum(r['status']=='PASS'for r in d['records'])!=17 or sum(r['status']=='FAILED'for r in d['records'])!=33 or len(d['fixed_current_pins'])!=3956 or len(d['output_pins'])!=294 or len(hf['dependencies'])!=3955 or d['actual_terminal']!=p['actual_terminal']:raise RuntimeError('current Root fifty records/fullpair and exact3955/3956/294 bound')
 for path in (OLD_PACK_V3_AUTHORITY['summary_pin'],OLD_PACK_V3_AUTHORITY['complete_raw_pin']):same(path)
 pack=read(OLD_PACK_V3_AUTHORITY['summary_pin'])
 if pack['status']!='FAILED_UNQUALIFIED_NO_RETRY'or pack['failure']is None:raise RuntimeError('old private PACK from genuine closed failed v3, not current science')
 return CLOSED_FULL50"""
PROTECTION="""def current_protection(sfpin,reviews):
 f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8811_manifest']);table={};roles={};cache={};historical=[];rows=old['current_protected_full_EOF_pins']
 if len(rows)!=8811 or HISTORICAL_TARGET_INDICES!=[2605,4177,4467]or [b.norm(rows[i])for i in HISTORICAL_TARGET_INDICES]!=TARGET_SELECTED_PINS or {p['path']for p in rows}&TARGET_PATHS!=TARGET_PATHS:raise RuntimeError('MF8811 only3 exactindices historical; all other8808 rows preserved')
 def add(p,role):
  p=b.norm(p);path=p['path']
  if path in TARGET_PATHS:
   if p!=next(q for q in TARGET_SELECTED_PINS if q['path']==path):raise RuntimeError('exact3 original wholePF target')
   historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_THREE_OLD_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return
  actual=cache.get(path)
  if actual is None:actual=pin(path);cache[path]=actual
  elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7')
  if actual!=p or tuple(p['identity'][:2])in{tuple(q['identity'][:2])for q in TARGET_SELECTED_PINS}:raise RuntimeError('current exactPF physically disjoint')
  if path in table and table[path]!=p:raise RuntimeError('inconsistent current fullpin')
  table[path]=p;roles.setdefault(role,set()).add(path)
 for i,p in enumerate(rows):add(p,'previous8811_exact_index_'+str(i))
 before=inventory()
 if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=OWNER_FILE_COUNT or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('complete oldv3/v14/v15 closed owner inventories')
 retained=[]
 for path in sorted(before['ordinary_file_identities']):
  if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_v3_v14_v15_owner_files_kept');retained.append(p)
 if len(retained)!=OWNER_FILE_COUNT-3:raise RuntimeError('only3 private body scope, all other files kept')
 current12=inventory([V12_OUT])
 if current12!=V12_BASELINE:raise RuntimeError('allv12 inventory unchanged')
 d=read(CLOSED_FULL50['summary_pin']);hf=read(CLOSED_FULL50['Host_freeze_pin']);post=read(CLOSED_FULL50['independent_postreview_pin'])
 for p in [CLOSED_FULL50['summary_pin'],CLOSED_FULL50['Host_freeze_pin'],CLOSED_FULL50['exact_cli_pin'],hf['host_source']]+hf['dependencies']+d['fixed_current_pins']+d['output_pins']+d['owned_runtime_pins']+post['actual_all_physical_output_fullpins']:add(p,'latest_v18_complete50_current_fixed_outputs_pair_and_source')
 for p in ROLE_KEEP_PINS:add(p,'all_original_scientific9_current')
 for p in BIND_NEW_SOURCE_PINS:add(p,'new_saved370_candidates_and_all_Source_proofs')
 for origin in DOWNSTREAM_ORIGINS:
  x=read(origin['metadata_pin'])
  if [b.norm(v['current_pin'])for v in x['rows']]!=origin['current_pins']or len(x['rows'])!=origin['current_row_count']:raise RuntimeError('material33 GENDF51 unchanged')
  add(origin['metadata_pin'],'downstream_metadata')
  for p in origin['current_pins']:add(p,'downstream_science')
 for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_reports_logs_immutable')
 for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_tools0')
 return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8811,exact_previous_MF3_indices_migrated_to_history=HISTORICAL_TARGET_INDICES,all_other8808_PF_rows_data_retained=True,current_HF3955_targets_absent_from_direct_current_rows=True,explicit_exact3_historical_body_declarations=historical,retained_other_file_count=len(retained),all_owner_directory_nodes_kept=True,all_original_science9_and_both_success_pairs_and_current70_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12),retained,before"""
def main():
 if OUT.exists():raise RuntimeError('one unique new Source package')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_SOURCE_FREEZE.json');oldsf=read(oldsfpin);mfpin=pin(OLD/'EXACT_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_MANIFEST.json');mf=read(mfpin);targets=[norm(mf['current_protected_full_EOF_pins'][i])for i in INDICES]
 if len(mf['current_protected_full_EOF_pins'])!=8811 or sum(p['size_bytes']for p in targets)!=TOTAL or len({tuple(p['identity'][:2])for p in targets})!=3:raise RuntimeError('exact3 original MF8811 selected wholePF')
 for q in targets:
  st=Path(q['path']).lstat()
  if identity(st)!=q['identity']or not stat.S_ISREG(st.st_mode)or st.st_uid!=os.getuid()or st.st_nlink!=1:raise RuntimeError('exact target current7 UID ordinary singlelink')
 postdir=R/'independent_v18_full50_engineering_actual_terminal_postverify_20261014';rp=pin(postdir/'REVIEW.json');tp=pin(postdir/'TRUE_TOOL_RETURNS.json');post=read(rp);pt=read(tp)
 if rp['sha256']!='991a1990b2ca24025922c0309c508b1af01f8c530c89058f9ef1a9a957ef57f5'or tp['sha256']!='d154d9caac44dd89d4cb8d09df20a49ce341c99f21a0aae43274a04cbbd4aead':raise RuntimeError('exact full50 post0 authorities')
 latest=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=rp,independent_posttools_pin=tp,actual_output_root=str(Path(post['actual_report_pin']['path']).parent))
 d=read(latest['summary_pin']);hf=read(latest['Host_freeze_pin']);keep=hf['retained_original_science_nine_input_pins'];paths={p['path']for p in targets};saved=read(R/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
 if len(keep)!=9 or any(paths&{p['path']for p in rows}for rows in [hf['dependencies'],d['fixed_current_pins'],d['output_pins'],saved['fixed_current_pins'],saved['science_original_input_pins']]):raise RuntimeError('no direct current HF3955/v18/Saved3301/science1129 target role')
 if len(saved['science_original_input_pins'])!=1129 or len(saved['fixed_current_pins'])!=3301:raise RuntimeError('original saved370 scientific authorities unchanged')
 macro=next(p for p in keep if Path(p['path']).name=='axial_macro.xsm')
 if any(q['sha256']!=macro['sha256']or q['size_bytes']!=macro['size_bytes']or q['identity'][:2]==macro['identity'][:2]for q in targets[1:]):raise RuntimeError('two private macro copies equal retained science body, distinct nodes')
 catalog=read(hf['selected_post_release_current_catalog_pin']);catrows=[(i,x)for i,x in enumerate(catalog['rows'])if x.get('current_pin',{}).get('path')==targets[0]['path']]
 if len(catrows)!=1 or catrows[0][1]['mandatory']is not False or any(not s.startswith('recursive_full_PF_from_current_JSON:')for s in catrows[0][1]['roles']):raise RuntimeError('oldPACK only optional recursive historical catalog role')
 roots=[Path(p['path']).parents[1]for p in targets];before=inventory(roots);ownerfiles=len(before['ordinary_file_identities']);ownerdirs=len(before['directory_identities'])
 if len(set(roots))!=3 or not paths<=set(before['ordinary_file_identities']):raise RuntimeError('three exact closed old roots')
 source=(OLD/NAMES[0]).read_text();current=source;changes=[]
 def change(a,b):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('one complete Source splice')
  current=current.replace(a,b,1);changes.append(dict(before=a,after=b))
 def node(name):return next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
 def const(name):return ast.literal_eval(node(name).value)
 def assign(name,v):change(ast.get_source_segment(current,node(name)),name+'='+repr(v))
 def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
 hist=dict(const('HISTORICAL_PINS'));hist.update(previous8811_manifest=mfpin,predecessor_cleanup_Source_freeze=oldsfpin,latest_v18_report=latest['summary_pin'],latest_v18_HF=latest['Host_freeze_pin'],latest_v18_CLI=latest['exact_cli_pin'],latest_v18_Root=latest['Root_true_tool_pin'],latest_v18_Root_argv=latest['Root_exact_argv_pin'],latest_v18_post=rp,latest_v18_post_tools=tp,saved3301_original_binding=pin(R/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'))
 oldpackroot=roots[0];oldpack=read(oldpackroot/'Root_actual_three_plane_engineering_summary.json');oldpackauth=dict(summary_pin=pin(oldpackroot/'Root_actual_three_plane_engineering_summary.json'),complete_raw_pin=oldpack['complete_unmodified_execution_records_pin'] if 'complete_unmodified_execution_records_pin'in oldpack else pin(oldpackroot/'Root_actual_complete_execution_record_before_final_publication.json'))
 hist.update(oldv3PACK_owner_summary=oldpackauth['summary_pin'],oldv3PACK_owner_complete_raw=oldpackauth['complete_raw_pin'])
 sourcepins=list(const('BIND_NEW_SOURCE_PINS'))+[pin(p)for p in sorted((R/'saved_full370_after_latest_full50_source_v3_20261014').iterdir())if p.is_file()]
 sourcepins+=list(latest.values())[:-1];sourcepins=list({p['path']:p for p in sourcepins}.values())
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',INDICES),('HISTORICAL_HF_TARGET_INDICES',[]),('BASELINE_OWNED_INVENTORIES',before),('ROLE_KEEP_PINS',keep),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',ownerfiles),('OWNER_DIRECTORY_COUNT',ownerdirs)]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal3_before_saved370_old_pack_and_macro_actual_receipts_20261014'\nCLOSED_FULL50="+repr(latest)+'\nOLD_PACK_V3_AUTHORITY='+repr(oldpackauth))
 for k,v in [('SF','COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace('LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES',LABEL).replace('len(TARGETS)!=18','len(TARGETS)!=3').replace('len(TARGET_PATHS)!=18','len(TARGET_PATHS)!=3').replace("f['closed_runtime_completed_authority']!=CLOSED_RUNTIME_COMPLETED","f['closed_runtime_completed_authority']!=CLOSED_RUNTIME_COMPLETED or f['closed_latest_full50_authority']!=CLOSED_FULL50"))
 g=fn('disjoint');change(g,g.replace('!=18','!=3'))
 g=fn('closed_proofs');change(g,g.replace('monitor_closed_proof(),runtime_completed_proof()]','monitor_closed_proof(),runtime_completed_proof(),full50_closed_proof()]')+'\n\n'+FULL50)
 change(fn('current_protection'),PROTECTION);ast.parse(current)
 others=[]
 for name in NAMES[1:]:
  beforetext=(OLD/name).read_text();after=beforetext.replace('LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES',LABEL).replace('target_count=18','target_count=3').replace("m['target_count']!=18","m['target_count']!=3").replace("before['regular_files']-after['regular_files']!=18","before['regular_files']-after['regular_files']!=3").replace('deleted_files=18','deleted_files=3');ast.parse(after);others.append((name,beforetext,after))
 funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(source)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven low-level methods wholebytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";a=others[1][1];b=others[1][2]
 if a[a.index(start):a.index(end)]!=b[b.index(start):b.index(end)]:raise RuntimeError('exact unlink-returnreceipt-fsync-dirFirstFailure bytes')
 # The only pure validation executed here checks existing small authority JSON;
 # no candidate import, Source business entry or scientific body is executed.
 namespace={'read':read,'CLOSED_FULL50':latest,'OLD_PACK_V3_AUTHORITY':oldpackauth,'shlex':__import__('shlex'),'json':json,'b':type('B',(),{'norm':staticmethod(norm)})(),'same':lambda p:pin(p['path'])==norm(p)}
 exec(compile(FULL50,'<Source-only-closed-full50-metadata-proof>','exec'),namespace);namespace['full50_closed_proof']()
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,after in others:write(OUT/name,after)
 pp=write(OUT/'EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_ROLE_SOURCE_PLAN_V1',source_only=True,literal3_fullpins=targets,target_count=3,target_bytes=TOTAL,previous8811_manifest_pin=mfpin,exact_current_MF3_indices_migrated_to_history=INDICES,all_other8808_PF_rows_data_retained=True,current_HF3955_pin=latest['Host_freeze_pin'],no_target_direct_current_HF3955_Saved3301_or_science1129_role=True,current_original_science9_input_pins=keep,optional_oldPACK_catalog_row_index=catrows[0][0],optional_oldPACK_catalog_role_declaration=catrows[0][1],oldPACK_generated_closed_private_intermediate_not_required_sameSHAduplicate=True,two_macros_equal_retained_scientific_macro_fullSHA_size_distinctnodes=True,complete_owner_inventory=before,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_file_count=ownerfiles-3,closed_latest_full50_authority=latest,old_v3_PACK_owner_authority=oldpackauth,original_caps=oldsf['original_caps'],legacy_three_script_names_and_literal11_fullpins_SF_contract_retained=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,future_original_current_fullfresh2_budget_admission=None,predicted_margin_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=b)])for n,a,b in others]
 for entry in entries:
  back=Path(entry['candidate_pin']['path']).read_text()
  for c in reversed(entry['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('exact one complete inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(entry['predecessor_pin']['path']).read_bytes():raise RuntimeError('three complete byte inverses')
 ip=write(OUT/'COMPLETE_LITERAL18_TO_LITERAL3_BEFORE_SAVED370_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL18_TO_LITERAL3_BEFORE_SAVED370_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);sf.pop('literal18_fullpins');sf.update(schema='COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal3_fullpins=targets,target_count=3,target_bytes=TOTAL,historical_evidence_pins=hist,closed_latest_full50_authority=latest,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=ip,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=write(OUT/'COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json',sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT3_BEFORE_SAVED370_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=pp,inverse_pin=ip,preparer_pin=pin(__file__),target_count=3,target_bytes=TOTAL,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_file_count=ownerfiles-3,old_MF8811_only_exact3_history_other8808_kept=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()

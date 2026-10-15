"""Exact Source-only map005/006 retirement; never MF, body EOF, business or unlink."""
import ast,importlib.util,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal3_closed_old_maps_before_A10_completion_source_v2_20261014'
ACTOR_BASE=R/'storage_release_literal4_before_short_FIL_material_retry_source_v3_20261014'
OUT=R/'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014'
LABEL='LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE';OLDLABEL='LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION';ACTORLABEL='LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY'
spec=importlib.util.spec_from_file_location('original_source_helpers',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write,inventory,identity,norm=h.pin,h.read,h.write,h.inventory,h.identity,h.norm
PROTECTION=r'''def current_protection(sfpin,reviews):
 f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous9626_manifest']);table={};roles={};cache={};rows=old['current_protected_full_EOF_pins']
 if len(rows)!=9626 or HISTORICAL_TARGET_INDICES!=[5948,5949]or [b.norm(rows[i])for i in HISTORICAL_TARGET_INDICES]!=RELEASED_A10_LIBRARY_PINS or {p['path']for p in rows}&TARGET_PATHS:raise RuntimeError('exact mother9626 releasedlibrary2 history and noncurrent map2')
 retired={p['path']:p for p in RELEASED_A10_LIBRARY_PINS};historical=[]
 def add(p,role):
  p=b.norm(p);path=p['path']
  if path in retired:
   if p!=retired[path]or os.path.lexists(path):raise RuntimeError('only exact actual release receipt libraries absent historical')
   historical.append(dict(original_body_pin=p,original_role=role,current_pin=None));return
  if path in TARGET_PATHS:raise RuntimeError('noncurrent selected map intermediate cannot be promoted')
  actual=cache.get(path)
  if actual is None:actual=pin(path);cache[path]=actual
  elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7')
  if actual!=p or tuple(p['identity'][:2])in{tuple(q['identity'][:2])for q in TARGET_SELECTED_PINS}:raise RuntimeError('protected exactPF and physical disjoint')
  if path in table and table[path]!=p:raise RuntimeError('inconsistent current fullpin')
  table[path]=p;roles.setdefault(role,set()).add(path)
 for i,p in enumerate(rows):add(p,'all_previous9626_rows_'+str(i))
 if len(table)!=9624:raise RuntimeError('all other9624 mother rows kept')
 before=inventory()
 if before!=BASELINE_OWNED_INVENTORIES or len(before['ordinary_file_identities'])!=OWNER_FILE_COUNT or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('two exact old map parent inventories')
 retained=[]
 for path in sorted(before['ordinary_file_identities']):
  if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_map005006_files_kept');retained.append(p)
 if len(retained)!=OWNER_FILE_COUNT-2:raise RuntimeError('only two selected intermediate files retired')
 current12=inventory([V12_OUT])
 if current12!=V12_BASELINE:raise RuntimeError('V12 spectator unchanged')
 d=read(A10_CAPTURE_AUTHORITY['report_pin']);p=read(A10_CAPTURE_AUTHORITY['post_pin']);hf=read(A10_CAPTURE_AUTHORITY['HF_pin'])
 for q in list(A10_CAPTURE_AUTHORITY.values())+hf['dependencies']+d['fixed_current_pins']+d['output_pins']+d['owned_input_copy_pins']+p['actual_scene_full_EOF_pins']+p['actual_original_library_input_pins']:add(q,'original_A10_capture_only_exact_released_library2_historical')
 for c in [CLOSED_A10_COMPLETION,CLOSED_EXTRACTION]:
  d=read(c['report_pin']);p=read(c['post_pin'])
  outputs=d['output_pins']if c is CLOSED_A10_COMPLETION else d['complete_output_pins']
  for q in list(c.values())+d['fixed_current_pins']+outputs:add(q,'actual_closed_completion_and_extraction_all_current')
  add(c['report_pin'],'actual_current_summary_file')
 for q in ROLE_KEEP_PINS:add(q,'all_original_scientific9_current')
 for q in OLD_MAP_AUTHORITY['retained_metadata_pins']+OLD_MAP_AUTHORITY['retained_final_file_pins']:add(q,'old_owner_docs_archives_and_final_map012_remain_current')
 for q in BIND_NEW_SOURCE_PINS+f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(q,'all_Source_docs_reports_logs_immutable')
 for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_tools0')
 return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=9626,exact_previous_MF_indices_migrated_to_history=[5948,5949],all_other9624_PF_rows_data_retained=True,exact_already_released_A10_library_historical_declarations=historical,explicit_exact2_historical_body_declarations=[dict(original_body_pin=q,original_live_role='closed_nonfinal_map_projected_intermediate',planned_next_role='EXACT_TWO_CLOSED_OLD_MAP005006_INTERMEDIATES_HISTORICAL',actual_retirement_not_yet_claimed=True)for q in TARGET_SELECTED_PINS],retained_other_file_count=len(retained),all_owner_directory_nodes_kept=True,all_original_science9_and_pairs_and_liveTMP_and_build75_kept=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,pending_A10_exact_owned_library_release_pins=[],pending_A10_library_bytes=0,current_fullfresh2_not_admitted_by_this_Source=True),retained,before
'''
ADDITIONAL=r'''def current_completion_and_extraction_closed_proof():
 for c,schema,status in [(CLOSED_A10_COMPLETION,'INDEPENDENT_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_ACTUAL_COMPLETION_POSTVERIFICATION_V1','PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'),(CLOSED_EXTRACTION,'INDEPENDENT_SIX_ROOT_FIRST_A_FULLFIELD_EXTRACTION_ACTUAL_EVIDENCE_POSTVERIFICATION_V1','PASS_ACTUAL_SIX_ROOT_FIRST_A_FULLFIELD_EXTRACTION_EVIDENCE_POSTVERIFICATION')]:
  p=read(c['post_pin']);pt=read(c['post_tools_pin']);t=read(c['Root_tools_pin']);a=read(c['Root_argv_pin']);q=t['actual_terminal_return']
  if p['schema']!=schema or p['status']!=status or p['failure']is not None or any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('strict independent actual completion/extraction post')
  if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or len(a['exact_argv'])!=(62 if c is CLOSED_A10_COMPLETION else 30):raise RuntimeError('strict genuine closed Root0/exact62 or30')
  if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('actual independent post closed0')
  for k in('actual_review_return','actual_postverification_return'):
   z=pt[k]
   if type(z['exit_code'])is not int or z['exit_code']!=0 or z.get('session_id')is not None or b.norm(json.loads(z['output'].strip().splitlines()[-1])['review_pin'])!=c['post_pin']:raise RuntimeError('actual post original output reviewPF')
  for k,v in [('actual_report_pin','report_pin'),('actual_Host_freeze_pin','HF_pin'),('actual_Root_true_tool_return_pin','Root_tools_pin'),('actual_Root_argv_pin','Root_argv_pin')]:
   if p[k]!=c[v]:raise RuntimeError('exact canonical actual authority '+k)
 p=read(CLOSED_A10_COMPLETION['post_pin']);rel=read(CLOSED_A10_COMPLETION['release_pin']);d=read(CLOSED_A10_COMPLETION['report_pin'])
 if p['actual_closed_owned_library_copy_release_pin']!=CLOSED_A10_COMPLETION['release_pin']or p['actual_observation_manifest_pin']!=CLOSED_A10_COMPLETION['manifest_pin']or p['actual_original_Root_integer_exit_code']!=1 or p['actual_new_material_child_launch_count']!=0 or rel['owned_copy_pins_before_release']!=RELEASED_A10_LIBRARY_PINS or rel['total_owned_bytes_released']!=979740136 or rel['all_owned_copy_paths_absent_after_release']is not True or any(os.path.lexists(x['path'])for x in RELEASED_A10_LIBRARY_PINS)or PENDING_A10_LIBRARY_PINS!=[]:raise RuntimeError('actual released979 private2 historical; pending0')
 if d['status']!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'or d['failure']is not None or d['after_check_error']is not None or d['records']!=read(A10_CAPTURE_AUTHORITY['report_pin'])['records']or d['original_Root_exit_code_retained']!=1:raise RuntimeError('original single child0 record preserved; original Root1 not forged')
 d=read(CLOSED_EXTRACTION['report_pin'])
 if d['schema']!='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'or d['status']!='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'or d['operation']!='extract'or d['failure']is not None or d['after_check_error']is not None or d['actual_intentional_exit2_normal_closure']is not True or len(d['records'])!=1 or d['records'][0]['status']!='FAILED'or len(d['fixed_current_pins'])!=5871 or len(d['complete_output_pins'])!=46:raise RuntimeError('actual extraction intentional child2 and current5871/output46 preserved')
 return dict(actual_completion_authority=CLOSED_A10_COMPLETION,actual_extraction_authority=CLOSED_EXTRACTION,exact_released_A10_historical_pins=RELEASED_A10_LIBRARY_PINS,pending_A10_library_bytes=0)
'''
def main():
 if OUT.exists():raise RuntimeError('unique Source namespace')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_SOURCE_FREEZE.json');sf=read(oldsfpin);mfpin=pin(OLD/'EXACT_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_MANIFEST.json');rows=read(mfpin)['current_protected_full_EOF_pins']
 def authority(dirname):
  pd=R/dirname;pp=pin(pd/'REVIEW.json');pt=pin(pd/'TRUE_TOOL_RETURNS.json');p=read(pp)
  c=dict(report_pin=p['actual_report_pin'],HF_pin=p['actual_Host_freeze_pin'],Root_tools_pin=p['actual_Root_true_tool_return_pin'],Root_argv_pin=p['actual_Root_argv_pin'],post_pin=pp,post_tools_pin=pt)
  return c,p
 completion,cp=authority('independent_short_FIL_A10_closed_capture_continuation_v3_actual_completion_postverify_20261014');completion.update(CLI_pin=cp['actual_CLI_pin'],manifest_pin=cp['actual_observation_manifest_pin'],release_pin=cp['actual_closed_owned_library_copy_release_pin'])
 extraction,ep=authority('independent_six_root_first_A_fullfield_extraction_actual_evidence_postverify_20261014');extraction.update(Source_freeze_pin=ep['actual_Source_freeze_pin'],dynamic_pin=ep['actual_dynamic_interface_pin'],request_pin=ep['actual_request_pin'],child_report_pin=ep['actual_child_report_pin'],manifest_pin=ep['actual_observation_manifest_pin'],coverage_pin=ep['actual_extraction_review_pin'])
 released=read(completion['release_pin'])['owned_copy_pins_before_release']
 if len(rows)!=9626 or [norm(rows[i])for i in[5948,5949]]!=released or any(os.path.lexists(p['path'])for p in released):raise RuntimeError('exact actual released mother9626 library2 roles')
 source=(OLD/'literal11_release_common.py').read_text();current=source;changes=[]
 def node(n):
  ns=[x for x in ast.parse(current).body if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name)and x.targets[0].id==n]
  if len(ns)!=1:raise RuntimeError('unique exact assignment '+n)
  return ns[0]
 def const(n):return ast.literal_eval(node(n).value)
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('one exact Source splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 def assign(n,v):change(ast.get_source_segment(current,node(n)),n+'='+repr(v))
 def fn(n):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==n))
 oma=dict(const('OLD_MAP_AUTHORITY'));root=Path(oma['run_status_pin']['path']).parent;targets=[];results=[]
 for num,sha in [(5,'81f649ef8ec9c8f1d9bcfe4dee152d25a1e80b1eaf2e2da243f8967e982269de'),(6,'e1d7a7ba754d0d4f59950d1c5668c1e706c37ad71683a710f1bc174c5159d6f3')]:
  p=root/('map'+format(num,'03d'))/'projected_proposal.xsm';s=p.lstat();rp=pin(p.parent/'result.json');r=read(rp)
  if s.st_uid!=os.getuid()or s.st_nlink!=1 or not stat.S_ISREG(s.st_mode)or s.st_size!=231698876 or r['sha256']['projected_proposal.xsm']!=sha:raise RuntimeError('exact map005006 sealed SHA/current ordinary UID1')
  targets.append(dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=identity(s)));results.append(rp)
 if {p['path']for p in targets}&{p['path']for p in rows}:raise RuntimeError('targets not mother live rows')
 oma['target_result_pins']=results;before=inventory([Path(p['path']).parent for p in targets]);hist=dict(const('HISTORICAL_PINS'));hist.update(previous9626_manifest=mfpin,previous_oldmaps3_Source_freeze=oldsfpin)
 for label,c in [('actual_A10_completion',completion),('actual_extraction',extraction)]:
  for k,v in c.items():hist[label+'_'+k]=v
 for i,p in enumerate(results):hist['map005006_result'+str(i)]=p
 for name,value in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[5948,5949]),('BASELINE_OWNED_INVENTORIES',before),('OWNER_FILE_COUNT',len(before['ordinary_file_identities'])),('OWNER_DIRECTORY_COUNT',len(before['directory_identities'])),('BYTES',463397752),('OLD_MAP_AUTHORITY',oma),('PENDING_A10_LIBRARY_PINS',[])]:assign(name,value)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=['+','.join('Path('+repr(str(Path(p['path']).parent))+')'for p in targets)+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal2_old_map005006_before_aggregate_actual_receipts_20261014'\nRELEASED_A10_LIBRARY_PINS="+repr(released)+'\nCLOSED_A10_COMPLETION='+repr(completion)+'\nCLOSED_EXTRACTION='+repr(extraction))
 for k,v in [('SF','COMPLETE_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace(OLDLABEL,LABEL).replace('len(TARGETS)!=3','len(TARGETS)!=2').replace('len(TARGET_PATHS)!=3','len(TARGET_PATHS)!=2').replace("f['pending_A10_library_pins']!=PENDING_A10_LIBRARY_PINS","f['pending_A10_library_pins']!=[]or f['released_A10_library_pins']!=RELEASED_A10_LIBRARY_PINS or f['actual_A10_completion_authority']!=CLOSED_A10_COMPLETION or f['actual_extraction_authority']!=CLOSED_EXTRACTION"))
 d=fn('disjoint');change(d,d.replace('len(TARGETS)!=3','len(TARGETS)!=2').replace('len(TARGET_PATHS)!=3','len(TARGET_PATHS)!=2').replace("len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=3","len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=2"))
 oldproof=fn('closed_old_maps_and_A10_capture_proof');prefix=oldproof[:oldproof.index(" p=read(A10_CAPTURE_AUTHORITY")];change(oldproof,prefix+" return dict(old_closed_map_authority=OLD_MAP_AUTHORITY,original_A10_failed_report_facts_retained=True)\n\n"+ADDITIONAL.rstrip())
 change(fn('closed_proofs'),fn('closed_proofs').replace('closed_old_maps_and_A10_capture_proof()]','closed_old_maps_and_A10_capture_proof(),current_completion_and_extraction_closed_proof()]'))
 change(fn('current_protection'),PROTECTION.rstrip())
 oldpins=const('BIND_NEW_SOURCE_PINS');assign('BIND_NEW_SOURCE_PINS',list({p['path']:p for p in oldpins+list(completion.values())+list(extraction.values())}.values()))
 ast.parse(current);funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)};low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(source)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven original lowmethods wholebytes')
 others=[]
 for name in h.NAMES[1:]:
  a=(ACTOR_BASE/name).read_text();z=a.replace(ACTORLABEL,LABEL).replace('target_count=4','target_count=2').replace("m['target_count']!=4","m['target_count']!=2").replace("before['regular_files']-after['regular_files']!=4","before['regular_files']-after['regular_files']!=2").replace('deleted_files=4','deleted_files=2');ast.parse(z);others.append((name,a,z))
 a,z=others[1][1:];start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)"
 if a[a.index(start):a.index(end)]!=z[z.index(start):z.index(end)]or "after['original_initial_reserve_admitted']is not True"not in z or 'pending_A10'in z:raise RuntimeError('original truthful syscall/dirfsync/firsttb and actual afterfullfreshTrue actor')
 OUT.mkdir();write(OUT/h.NAMES[0],current)
 for name,_,z in others:write(OUT/name,z)
 plan=write(OUT/'EXACT_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_ROLE_SOURCE_PLAN_V1',source_only=True,target_count=2,target_bytes=463397752,literal2_fullpins=targets,mother9626_manifest_pin=mfpin,exact_released_library_MF_indices_migrated_to_history=[5948,5949],released_library_pins= released,all_other9624_mother_rows_kept=True,actual_A10_completion_authority=completion,actual_extraction_authority=extraction,pending_A10_library_bytes=0,actor_after_actual_fullfresh2_required=True,complete_owner_inventory=before,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-2,old_closed_map_authority=oma,original_caps=sf['original_caps'],future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_original_current_fullfresh2_budget_admission=None,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/h.NAMES[0]),candidate_pin=pin(OUT/h.NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(ACTOR_BASE/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=z)])for n,a,z in others]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('unique complete inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('three full byte inverses')
 iv=write(OUT/'COMPLETE_OLDMAP3_SCOPE4_TO_NEXTMAP2_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_OLDMAP3_SCOPE4_TO_NEXTMAP2_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_equal=True,actor_actual_after_fullfresh2True_original=True,source_only=True))
 sf.update(schema='COMPLETE_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal2_fullpins=targets,target_count=2,target_bytes=463397752,historical_evidence_pins=hist,closed_old_map_authority=oma,pending_A10_library_pins=[],released_A10_library_pins=released,actual_A10_completion_authority=completion,actual_extraction_authority=extraction,Source_pins=[pin(OUT/n)for n in h.NAMES],exact_role_plan_pin=plan,strict_low_level_Source_provenance_pin=iv,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_original_current_fullfresh2_budget_admission=None)
 sp=write(OUT/'COMPLETE_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_SOURCE_FREEZE.json',sf);print(json.dumps(dict(status='NEXT_MAP005006_EXACT2_SOURCE_ONLY_READY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=plan,inverse_pin=iv,Source_author_pin=pin(__file__),target_count=2,target_bytes=463397752,pending_A10_library_bytes=0,actor_afterfullfresh2_actualTrue_required=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()

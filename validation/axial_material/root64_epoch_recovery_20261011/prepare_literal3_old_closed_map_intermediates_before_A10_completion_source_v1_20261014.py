"""Prepare three exact closed map intermediates; no manifest or deletion."""
import ast, importlib.util, json, os, stat
from pathlib import Path

R = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec = importlib.util.spec_from_file_location('source_metadata_helpers', R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py')
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
pin, read, write, inventory, identity, norm = h.pin, h.read, h.write, h.inventory, h.identity, h.norm
OLD = R/'storage_release_literal4_before_short_FIL_material_retry_source_v3_20261014'
OUT = R/'storage_release_literal3_closed_old_maps_before_A10_completion_source_v1_20261014'
NAMES = h.NAMES
OLD_LABEL = 'LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY'
LABEL = 'LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION'
TOTAL = 695096628

PROOF = '''def closed_old_maps_and_A10_capture_proof():
 d=read(OLD_MAP_AUTHORITY['run_status_pin']);st=read(OLD_MAP_AUTHORITY['stages_pin'])
 case=d['cases']['AAA']
 if d['classification']!='WAITING_REFERENCE'or d['completed_maps']!=12 or case['completed_maps']!=12 or case['classification']!='VALID_MET'or case['final_directory']!=OLD_MAP_AUTHORITY['retained_final_directory']or type(d['finished_unix'])not in(int,float)or len(st['stages'])!=105 or any(z['status']!='PASS'for z in st['stages']):raise RuntimeError('closed old maps finished at retained map012')
 for p,r in zip(TARGET_SELECTED_PINS,OLD_MAP_AUTHORITY['target_result_pins']):
  result=read(r)
  if result['classification']!='SEALED_STAGE_OUTPUTS'or result['sha256']['projected_proposal.xsm']!=p['sha256']:raise RuntimeError('exact original sealed intermediate SHA')
 p=read(A10_CAPTURE_AUTHORITY['post_pin']);t=read(A10_CAPTURE_AUTHORITY['post_tools_pin']);d=read(A10_CAPTURE_AUTHORITY['report_pin'])
 if p['schema']!='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'or p['failure']is not None or p['actual_material_stage_closed0']is not True or p['actual_stage_statuses']!=['PASS']or p['actual_owned_library_copy_pins_current']!=PENDING_A10_LIBRARY_PINS or p['actual_observation_manifest_pin']is not None or p['actual_closed_owned_library_copy_release_pin']is not None or p['actual_release_precondition_missing_lsof_exact_pin_confirmed']is not True:raise RuntimeError('only actual A10 stage0 capture with release blocked')
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))or t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0:raise RuntimeError('A10 readonly factual post closed0')
 for key in('actual_review_return','actual_postverification_return'):
  z=t[key]
  if type(z['exit_code'])is not int or z['exit_code']!=0 or z.get('session_id')is not None or b.norm(json.loads(z['output'].strip().splitlines()[-1])['review_pin'])!=A10_CAPTURE_AUTHORITY['post_pin']:raise RuntimeError('A10 exact actual post stdout PF')
 for k,v in(('actual_report_pin','report_pin'),('actual_Host_freeze_pin','HF_pin'),('actual_CLI_pin','CLI_pin'),('actual_Root_true_tool_return_pin','Root_tools_pin'),('actual_Root_argv_pin','Root_argv_pin')):
  if p[k]!=A10_CAPTURE_AUTHORITY[v]:raise RuntimeError('A10 canonical actual authority '+k)
 if d['status']!='FAILED_CURRENT_OBSERVATION_NO_RETRY'or len(d['records'])!=1 or d['records'][0]['status']!='PASS'or len(d['fixed_current_pins'])!=5737 or len(d['output_pins'])!=86 or len(p['actual_scene_full_EOF_pins'])!=87 or d['actual_closed_owned_library_copy_release_pin']is not None or sum(q['size_bytes']for q in PENDING_A10_LIBRARY_PINS)!=979740136:raise RuntimeError('original Host1 capture87 and unreleased exact library2 preserved')
 return dict(old_closed_map_authority=OLD_MAP_AUTHORITY,actual_A10_stage0_capture_authority=A10_CAPTURE_AUTHORITY,original_A10_Root1_preserved=True,initial_fullfresh2_admission_not_claimed=True)
'''

PROTECTION = '''def current_protection(sfpin,reviews):
 f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous9428_manifest']);table={};roles={};cache={};rows=old['current_protected_full_EOF_pins']
 if len(rows)!=9428 or HISTORICAL_TARGET_INDICES!=[]or {p['path']for p in rows}&TARGET_PATHS:raise RuntimeError('all mother9428 rows current; no target direct row')
 def add(p,role):
  p=b.norm(p);path=p['path']
  if path in TARGET_PATHS:raise RuntimeError('noncurrent map intermediate cannot be promoted')
  actual=cache.get(path)
  if actual is None:actual=pin(path);cache[path]=actual
  elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7')
  if actual!=p or tuple(p['identity'][:2])in{tuple(q['identity'][:2])for q in TARGET_SELECTED_PINS}:raise RuntimeError('protected exactPF and physical disjoint')
  if path in table and table[path]!=p:raise RuntimeError('inconsistent current fullpin')
  table[path]=p;roles.setdefault(role,set()).add(path)
 for i,p in enumerate(rows):add(p,'all_previous9428_rows_'+str(i))
 before=inventory()
 if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=OWNER_FILE_COUNT or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('three exact old map parent inventories')
 retained=[]
 for path in sorted(before['ordinary_file_identities']):
  if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_three_map_files_kept');retained.append(p)
 if len(retained)!=OWNER_FILE_COUNT-3:raise RuntimeError('only three intermediate files retired')
 current12=inventory([V12_OUT])
 if current12!=V12_BASELINE:raise RuntimeError('V12 spectator unchanged')
 d=read(A10_CAPTURE_AUTHORITY['report_pin']);p=read(A10_CAPTURE_AUTHORITY['post_pin']);hf=read(A10_CAPTURE_AUTHORITY['HF_pin'])
 for q in list(A10_CAPTURE_AUTHORITY.values())+hf['dependencies']+d['fixed_current_pins']+d['output_pins']+d['owned_input_copy_pins']+p['actual_scene_full_EOF_pins']+p['actual_original_library_input_pins']:add(q,'actual_A10_capture87_Source_and_library2_remain_current')
 for q in ROLE_KEEP_PINS:add(q,'all_original_scientific9_current')
 for q in OLD_MAP_AUTHORITY['retained_metadata_pins']+OLD_MAP_AUTHORITY['retained_final_file_pins']:add(q,'old_owner_docs_archives_and_final_map012_remain_current')
 for q in BIND_NEW_SOURCE_PINS+f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(q,'all_Source_docs_reports_logs_immutable')
 for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_tools0')
 return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=9428,exact_previous_MF_indices_migrated_to_history=[],all_other9428_PF_rows_data_retained=True,explicit_exact3_historical_body_declarations=[dict(original_body_pin=q,original_live_role='closed_nonfinal_map_projected_intermediate',planned_next_role='EXACT_THREE_CLOSED_OLD_MAP_INTERMEDIATES_HISTORICAL',actual_retirement_not_yet_claimed=True)for q in TARGET_SELECTED_PINS],retained_other_file_count=len(retained),all_owner_directory_nodes_kept=True,all_original_science9_and_both_success_pairs_and_current75_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,current_fullfresh2_not_admitted_by_this_cleanup=True,pending_A10_exact_owned_library_release_pins=PENDING_A10_LIBRARY_PINS),retained,before
'''

def main():
 if OUT.exists():raise RuntimeError('unique Source namespace')
 original=(OLD/NAMES[0]).read_text(); current=original;changes=[]
 def node(n):return next(x for x in ast.parse(current).body if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name)and x.targets[0].id==n)
 def const(n):return ast.literal_eval(node(n).value)
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('unique exact Source splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 def assign(n,v):change(ast.get_source_segment(current,node(n)),n+'='+repr(v))
 def fn(n):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==n))
 mf=pin(OLD/'EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_MANIFEST.json');oldsfpin=pin(OLD/'COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_FREEZE.json');sf=read(oldsfpin)
 branch=Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-source-factor-20261006');roots=[branch/'AAA'/n for n in('map002','map003','map004')]
 targets=[];results=[]
 for root in roots:
  rp=pin(root/'result.json');d=read(rp);p=root/'projected_proposal.xsm';s=p.lstat()
  if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or s.st_uid!=os.getuid()or s.st_size!=231698876:raise RuntimeError('exact ordinary original intermediate')
  targets.append(dict(path=str(p),sha256=d['sha256'][p.name],size_bytes=s.st_size,identity=identity(s)));results.append(rp)
 if len({tuple(p['identity'][:2])for p in targets})!=3 or sum(p['size_bytes']for p in targets)!=TOTAL:raise RuntimeError('three physical distinct targets')
 pp=pin(R/'independent_material_first_A_short_FIL_v10_actual_stage0_capture_release_blocked_postverify_20261014/REVIEW.json');pt=pin(Path(pp['path']).with_name('TRUE_TOOL_RETURNS.json'));post=read(pp)
 a10=dict(report_pin=post['actual_report_pin'],HF_pin=post['actual_Host_freeze_pin'],CLI_pin=post['actual_CLI_pin'],Root_tools_pin=post['actual_Root_true_tool_return_pin'],Root_argv_pin=post['actual_Root_argv_pin'],post_pin=pp,post_tools_pin=pt)
 pending=post['actual_owned_library_copy_pins_current']
 if len(pending)!=2 or sum(p['size_bytes']for p in pending)!=979740136:raise RuntimeError('exact two pending owned library copies')
 oldmap=dict(run_status_pin=pin(branch/'AAA/run_status.json'),stages_pin=pin(branch/'AAA/stages.json'),target_result_pins=results,retained_final_directory=str(branch/'AAA/map012'),retained_metadata_pins=[pin(branch/p)for p in ('declaration.json','prepared.json','AAA/run_claim.json','archives/result.json')],retained_final_file_pins=[])
 final_result=read(pin(branch/'AAA/map012/result.json'))
 for p in sorted((branch/'AAA/map012').iterdir()):
  if not p.is_file():raise RuntimeError('ordinary final map files')
  s=p.lstat();sha=final_result['sha256'].get(p.name)
  q=dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=identity(s))if sha else pin(p)
  oldmap['retained_final_file_pins'].append(q)
 tables=[read(mf)['current_protected_full_EOF_pins'],read(a10['HF_pin'])['dependencies']]
 common=R/'post_literal3_old_pack_current_catalog_common_source_v1_20261014'
 cat=pin(common/'CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json');bind=pin(common/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json')
 tables += [[q['current_pin']for q in read(cat)['rows']],read(bind)['fixed_current_pins']]
 if any(any(q['path']==p['path']for q in t)for p in targets for t in tables):raise RuntimeError('old intermediate has direct current role')
 before=inventory(roots);hist=dict(const('HISTORICAL_PINS'));hist.update(previous9428_manifest=mf,predecessor_literal4_Source_freeze=oldsfpin,old_map_run_status=oldmap['run_status_pin'],old_map_stages=oldmap['stages_pin'],actual_A10_capture_post=pp,actual_A10_capture_tools=pt,current_catalog=cat,current_binding=bind)
 late=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v3_20261014';extras=[pin(p)for p in sorted(late.iterdir())if p.is_file()]
 sourcepins=list({p['path']:p for p in const('BIND_NEW_SOURCE_PINS')+extras+list(a10.values())+results+oldmap['retained_metadata_pins']}.values())
 for n,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[]),('BASELINE_OWNED_INVENTORIES',before),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',len(before['ordinary_file_identities'])),('OWNER_DIRECTORY_COUNT',len(before['directory_identities']))]:assign(n,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal3_closed_old_maps_before_A10_completion_actual_receipts_20261014'\nOLD_MAP_AUTHORITY="+repr(oldmap)+'\nA10_CAPTURE_AUTHORITY='+repr(a10)+'\nPENDING_A10_LIBRARY_PINS='+repr(pending)+'\nOLD_FAILED_M9_LIBRARY_PINS='+repr(read(const('CLOSED_FAILED_A')['independent_postreview_pin'])['actual_owned_library_copy_pins_current']))
 for n,v in [('SF','COMPLETE_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_MANIFEST.json')]:change(ast.get_source_segment(current,node(n)),n+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace(OLD_LABEL,LABEL).replace('len(TARGETS)!=4','len(TARGETS)!=3').replace('len(TARGET_PATHS)!=4','len(TARGET_PATHS)!=3').replace("f['closed_old_AX_owner_authorities']!=OLD_AX_OWNER_AUTHORITIES","f['closed_old_AX_owner_authorities']!=OLD_AX_OWNER_AUTHORITIES or f['closed_old_map_authority']!=OLD_MAP_AUTHORITY or f['actual_A10_capture_authority']!=A10_CAPTURE_AUTHORITY or f['pending_A10_library_pins']!=PENDING_A10_LIBRARY_PINS"))
 g=fn('disjoint');change(g,g.replace('len(TARGETS)!=4','len(TARGETS)!=3').replace('len(TARGET_PATHS)!=4','len(TARGET_PATHS)!=3').replace("len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=4","len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=3"))
 g=fn('failed_material_A_closed_proof');change(g,g.replace("p['actual_owned_library_copy_pins_current']!=TARGET_SELECTED_PINS[:2]","p['actual_owned_library_copy_pins_current']!=OLD_FAILED_M9_LIBRARY_PINS"))
 g=fn('closed_proofs');change(g,g.replace('failed_material_A_closed_proof()]','failed_material_A_closed_proof(),closed_old_maps_and_A10_capture_proof()]')+'\n\n'+PROOF)
 change(fn('current_protection'),PROTECTION)
 others=[]
 for n in NAMES[1:]:
  a=(OLD/n).read_text();z=a.replace(OLD_LABEL,LABEL).replace('target_count=4','target_count=3').replace("m['target_count']!=4","m['target_count']!=3").replace("before['regular_files']-after['regular_files']!=4","before['regular_files']-after['regular_files']!=3").replace('deleted_files=4','deleted_files=3')
  if n==NAMES[2]:
   acheck="or after['original_initial_reserve_admitted']is not True"
   if z.count(acheck)!=1:raise RuntimeError('exact one actor reserve role gate')
   z=z.replace(acheck,"or after['remaining_after_original_initial_reserves_bytes']+after['initial_fresh_reserve_bytes']<=0 or after['remaining_after_original_initial_reserves_bytes']+sum(q['size_bytes']for q in s.PENDING_A10_LIBRARY_PINS)<=0",1)
   anchor="        value.update(status="
   if z.count(anchor)!=1:raise RuntimeError('one actor completion publication')
   z=z.replace(anchor,"        for q in s.PENDING_A10_LIBRARY_PINS:\n            if s.identity(Path(q['path']).lstat())!=q['identity']:raise RuntimeError('pending A10 original release copies remain exact current7')\n"+anchor,1)
   z=z.replace('original_budget_after=after,affected_parent_changes=changes','original_budget_after=after,fullfresh2_scientific_runtime_admitted=False,pending_A10_owned_library_copy_bytes=sum(q[\'size_bytes\']for q in s.PENDING_A10_LIBRARY_PINS),predicted_margin_after_future_original_A10_release_bytes=after[\'remaining_after_original_initial_reserves_bytes\']+sum(q[\'size_bytes\']for q in s.PENDING_A10_LIBRARY_PINS),future_release_prediction_is_not_admission=True,affected_parent_changes=changes')
  ast.parse(z);others.append((n,a,z))
 ast.parse(current);functions=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)};low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(functions(original)[n]!=functions(current)[n]for n in low):raise RuntimeError('low seven methods changed')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";a,z=others[1][1:]
 if a[a.index(start):a.index(end)]!=z[z.index(start):z.index(end)]:raise RuntimeError('unlink truthreceipt dirfsync and original FirstFailure changed')
 OUT.mkdir();write(OUT/NAMES[0],current)
 for n,_,z in others:write(OUT/n,z)
 plan=write(OUT/'EXACT_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_ROLE_SOURCE_PLAN_V1',source_only=True,target_count=3,target_bytes=TOTAL,literal3_fullpins=targets,mother9428_manifest_pin=mf,exact_MF_indices_migrated_to_history=[],all_mother9428_rows_preserved=True,nonfinal_closed_generated_intermediates_not_sameSHA_duplicates=True,closed_old_map_authority=oldmap,actual_A10_capture_authority=a10,pending_A10_library_pins=pending,complete_owner_inventory=before,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-3,actor_after_reserve_role='cold96_free8_actual_and_future_library979_prediction_only_no_fullfresh2_admission',original_caps=sf['original_caps'],future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,future_fullfresh2_admission=None,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=z)])for n,a,z in others]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('whole inverse unique splice')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('complete original wholebytes inverse')
 iv=write(OUT/'COMPLETE_LITERAL4_TO_LITERAL3_CLOSED_OLD_MAPS_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL4_TO_LITERAL3_CLOSED_OLD_MAPS_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_equal=True,actor_after_reserve_role_only_delta=True,source_only=True))
 sf.update(schema='COMPLETE_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal3_fullpins=targets,target_count=3,target_bytes=TOTAL,historical_evidence_pins=hist,closed_old_map_authority=oldmap,actual_A10_capture_authority=a10,pending_A10_library_pins=pending,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=plan,strict_low_level_Source_provenance_pin=iv,Source_preparer_pin=pin(Path(__file__)),predecessor_Source_freeze_pin=oldsfpin,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,source_only=True)
 sp=write(OUT/'COMPLETE_LITERAL3_CLOSED_OLD_MAPS_BEFORE_A10_COMPLETION_SOURCE_FREEZE.json',sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT3_CLOSED_OLD_MAPS_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=plan,inverse_pin=iv,preparer_pin=pin(Path(__file__)),target_count=3,target_bytes=TOTAL,retained_other_file_count=len(before['ordinary_file_identities'])-3,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)

if __name__=='__main__':main()

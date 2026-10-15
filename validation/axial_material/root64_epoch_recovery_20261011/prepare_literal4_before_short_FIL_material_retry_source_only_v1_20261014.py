"""Source-only exact failed-library2 plus old AX2 release; never MF or unlink."""
import ast,importlib.util,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec=importlib.util.spec_from_file_location('original_source_helpers',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write,inventory,identity,norm=h.pin,h.read,h.write,h.inventory,h.identity,h.norm
OLD=R/'storage_release_literal1_before_material_first_A_v14_ax_source_v2_20261014'
OUT=R/'storage_release_literal4_before_short_FIL_material_retry_source_v1_20261014'
NAMES=h.NAMES;LABEL='LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY';OLD_LABEL='LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE';TOTAL=1014071384
PROOF="""def failed_material_A_closed_proof():
 c=CLOSED_FAILED_A;p=read(c['independent_postreview_pin']);pt=read(c['independent_posttools_pin']);d=read(c['summary_pin']);t=read(c['Root_true_tool_pin']);a=read(c['Root_exact_argv_pin']);cli=read(c['exact_cli_pin']);q=t['actual_terminal_return']
 if p['schema']!='INDEPENDENT_MATERIAL_FIRST_A_AFTER_OBSERVER75_V9_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_MATERIAL_FIRST_A_AFTER_OBSERVER75_V9_FAILED_ATTEMPT_FACTUAL_POSTVERIFICATION'or p['failure']is not None:raise RuntimeError('exact failed A factual post0')
 for k,v in(('actual_report_pin','summary_pin'),('actual_Root_true_tool_return_pin','Root_true_tool_pin'),('actual_Root_argv_pin','Root_exact_argv_pin'),('actual_Host_freeze_pin','Host_freeze_pin'),('actual_CLI_pin','exact_cli_pin')):
  if p[k]!=c[v]:raise RuntimeError('failed A canonical '+k)
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))or p['actual_observation_manifest_pin']is not None or p['actual_closed_owned_library_copy_release_pin']is not None or p['actual_owned_library_copy_pins_current']!=TARGET_SELECTED_PINS[:2]:raise RuntimeError('only actual nonMF failed private2, no capture')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('post genuine closed0')
 for k in('actual_review_return','actual_postverification_return'):
  z=pt[k]
  if type(z['exit_code'])is not int or z['exit_code']!=0 or z.get('session_id')is not None or b.norm(json.loads(z['output'].strip().splitlines()[-1])['review_pin'])!=c['independent_postreview_pin']:raise RuntimeError('post exact original stdoutPF0')
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(q['exit_code'])is not int or q['exit_code']!=1 or q.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_argv']!=cli['exact_argv']or len(a['exact_argv'])!=32:raise RuntimeError('original failed Root1 exact32 retained')
 if d['schema']!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or d['status']!='FAILED_CURRENT_OBSERVATION_NO_RETRY'or len(d['records'])!=1 or d['records'][0]['status']!='FAILED'or len(d['fixed_current_pins'])!=5719 or len(d['output_pins'])!=21 or d['actual_full_A_observation_executed']is not False or p['actual_axobs_event_file_count']!=0 or p['actual_scene_file_count']!=22 or p['actual_owned_library_copy_bytes_current']!=979740136:raise RuntimeError('true failed1/zero contexts/current owned979')
 for row in OLD_AX_OWNER_AUTHORITIES:
  s=read(row['summary_pin']);raw=read(row['raw_pin']);target=row['target_pin'];compact=lambda rr:[{k:v for k,v in x.items()if k not in('resource_before','resource_after')}for x in rr]
  if s['status']!='FAILED_UNQUALIFIED_NO_RETRY'or s['failure']!='RuntimeError: original SELF 512MiB cap'or s['after_check_error']!='RuntimeError: original SELF 512MiB cap'or s['engineering_three_plane_closed0']is not False or len(s['records'])!=row['record_count']or compact(s['records'])!=compact(raw['records'])or s['owned_runtime_pins'][117]!=target or raw['owned_runtime_pins'][117]!=target:raise RuntimeError('old AX owners exact closed raw owned117')
 return c
"""
def main():
 if OUT.exists():raise RuntimeError('unique Source namespace')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_SOURCE_FREEZE.json');oldsf=read(oldsfpin)
 mfpin=pin(OLD/'EXACT_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_MANIFEST.json');rows=read(mfpin)['current_protected_full_EOF_pins']
 pd=R/'independent_material_first_A_after_observer75_v9_actual_failed_observation_postverify_20261014';pp=pin(pd/'REVIEW.json');pt=pin(pd/'TRUE_TOOL_RETURNS.json');post=read(pp)
 failed=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=pp,independent_posttools_pin=pt)
 targets=post['actual_owned_library_copy_pins_current']+[norm(rows[i])for i in [1834,2095]]
 if len(rows)!=9382 or len(targets)!=4 or sum(p['size_bytes']for p in targets)!=TOTAL or any(p in rows for p in targets[:2]):raise RuntimeError('only MF9382 twoAX and exact nonMF library2')
 source=(OLD/NAMES[0]).read_text();current=source;changes=[]
 def node(n):return next(x for x in ast.parse(current).body if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name)and x.targets[0].id==n)
 def const(n):return ast.literal_eval(node(n).value)
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('exact complete unique splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 def assign(n,v):change(ast.get_source_segment(current,node(n)),n+'='+repr(v))
 def fn(n):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==n))
 v10=R/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
 extras=[pin(p)for p in v10.iterdir()if p.is_file()]+[pin(R/'ROOT_ACTUAL_SHORT_FIL_V10_OWN_HF_CLI_ONCE_PUBLICATION_TRUE_TOOL_RETURNS_20261014.json'),pin(R/'ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json'),pin(R/'write_once_material_first_A_short_FIL_v10_HF_CLI_20261014.py')]
 v10hf=read(pin(v10/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'));oldhf=read(failed['Host_freeze_pin']);build=read(const('CLOSED_BUILD75')['summary_pin']);saved=read(const('CLOSED_SAVED')['summary_pin'])
 c=R/'post_literal3_old_pack_current_catalog_common_source_v1_20261014';cat=read(pin(c/'CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json'));bind=read(pin(c/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json'))
 direct=[oldhf['dependencies'],v10hf['dependencies'],build['fixed_current_pins'],saved['fixed_current_pins'],[x['current_pin']for x in cat['rows']],bind['fixed_current_pins']]+[x['current_pins']for x in const('DOWNSTREAM_ORIGINS')]
 scientific=next(p for p in const('ROLE_KEEP_PINS')if Path(p['path']).name=='ax_current.xsm')
 for p in targets:
  s=Path(p['path']).lstat()
  if identity(s)!=p['identity']or s.st_uid!=os.getuid()or s.st_nlink!=1 or any(any(x['path']==p['path']for x in rr)for rr in direct):raise RuntimeError('target current UID/all7/singlelink/no direct Source science role')
 for p in targets[2:]:
  if p['sha256']!=scientific['sha256']or p['size_bytes']!=scientific['size_bytes']or p['identity'][:2]==scientific['identity'][:2]:raise RuntimeError('retained SCI distinct sameSHA')
 owners=[]
 for v,count,p in zip([10,11],[46,45],targets[2:]):
  if '20261012-v'+str(v)+'/AAA/ax_current.xsm'not in p['path']:raise RuntimeError('exact oldAX path')
  root=Path(p['path']).parents[1];owners.append(dict(summary_pin=pin(root/'Root_actual_three_plane_engineering_summary.json'),raw_pin=pin(root/'Root_actual_complete_execution_record_before_final_publication.json'),target_pin=p,record_count=count))
 roots=[Path(failed['summary_pin']['path']).parent]+[Path(p['path']).parents[1]for p in targets[2:]]
 before=inventory(roots);v12before=inventory([Path(const('CLOSED_OWNER_V12')['summary_pin']['path']).parent])
 if len(v12before['ordinary_file_identities'])!=259 or len(v12before['directory_identities'])!=32:raise RuntimeError('spectator V12 actual259/32')
 hist=dict(const('HISTORICAL_PINS'));hist.update(previous9382_manifest=mfpin,predecessor_literal1_Source_freeze=oldsfpin)
 for k,p in failed.items():hist['failed_M9_A_'+k]=p
 for i,row in enumerate(owners):
  for k in ['summary_pin','raw_pin']:hist['old_AX_owner'+str(i)+'_'+k]=row[k]
 sourcepins=list({p['path']:p for p in const('BIND_NEW_SOURCE_PINS')+list(failed.values())+extras}.values())
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[1834,2095]),('BASELINE_OWNED_INVENTORIES',before),('V12_BASELINE',v12before),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',len(before['ordinary_file_identities'])),('OWNER_DIRECTORY_COUNT',len(before['directory_identities']))]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=['+','.join('Path('+repr(str(p))+')'for p in roots)+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal4_before_short_FIL_material_retry_actual_receipts_20261014'\nCLOSED_FAILED_A="+repr(failed)+'\nOLD_AX_OWNER_AUTHORITIES='+repr(owners))
 for k,v in [('SF','COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace(OLD_LABEL,LABEL).replace('len(TARGETS)!=1','len(TARGETS)!=4').replace('len(TARGET_PATHS)!=1','len(TARGET_PATHS)!=4').replace("f['closed_previous_v12_physical_completion_authority']!=CLOSED_V12_COMPLETION","f['closed_previous_v12_physical_completion_authority']!=CLOSED_V12_COMPLETION or f['closed_failed_M9_material_A_authority']!=CLOSED_FAILED_A or f['closed_old_AX_owner_authorities']!=OLD_AX_OWNER_AUTHORITIES"))
 change(fn('disjoint'),fn('disjoint').replace('!=1','!=4'))
 change(fn('closed_proofs'),fn('closed_proofs').replace('prior_v12_physical_completion_proof()]','prior_v12_physical_completion_proof(),failed_material_A_closed_proof()]')+'\n\n'+PROOF)
 f=fn('current_protection').replace("HISTORICAL_PINS['previous9239_manifest']","HISTORICAL_PINS['previous9382_manifest']").replace('9239','9382').replace('9238','9380').replace('[4203]','[1834,2095]').replace('!=TARGET_SELECTED_PINS or','!=TARGET_SELECTED_PINS[2:] or').replace('&TARGET_PATHS!=TARGET_PATHS',"&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[2:]}").replace('OWNER_FILE_COUNT-1','OWNER_FILE_COUNT-4').replace('only1','only4').replace('exact1','exact4').replace('EXACT_ONE_V14_PRIVATE_AX_COPY_BODY_HISTORICAL','EXACT_FOUR_FAILED_LIBRARY_AND_OLD_AX_BODIES_HISTORICAL').replace('MF1_indices','MF2_indices')
 anchor=" for p in ROLE_KEEP_PINS:add(p,'all_original_scientific9_current')"
 block=" failed_actual=read(CLOSED_FAILED_A['summary_pin']);failed_post=read(CLOSED_FAILED_A['independent_postreview_pin'])\n for p in list(CLOSED_FAILED_A.values())+failed_actual['fixed_current_pins']+failed_actual['output_pins']+failed_actual['owned_input_copy_pins']+failed_post['actual_scene_full_EOF_pins']:add(p,'closed_failed_M9_scene_only_exact_private_library2_historical')\n for p in failed_post['actual_original_library_input_pins'].values():add(p,'two_original_scientific_libraries_current')\n"
 if f.count(anchor)!=1:raise RuntimeError('one exact closure insertion')
 change(fn('current_protection'),f.replace(anchor,block+anchor))
 others=[]
 for name in NAMES[1:]:
  a=(OLD/name).read_text();z=a.replace(OLD_LABEL,LABEL).replace('target_count=1','target_count=4').replace("m['target_count']!=1","m['target_count']!=4").replace("before['regular_files']-after['regular_files']!=1","before['regular_files']-after['regular_files']!=4").replace('deleted_files=1','deleted_files=4');ast.parse(z);others.append((name,a,z))
 ast.parse(current);funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)};low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(source)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven original lowlevel wholebytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";a,z=others[1][1:]
 if a[a.index(start):a.index(end)]!=z[z.index(start):z.index(end)]:raise RuntimeError('immediate truthful unlink receipt dirfsync original FirstFailure bytes')
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,z in others:write(OUT/name,z)
 plan=write(OUT/'EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_ROLE_SOURCE_PLAN_V1',source_only=True,literal4_fullpins=targets,target_count=4,target_bytes=TOTAL,mother9382_manifest_pin=mfpin,exact_MF_indices_migrated_to_history=[1834,2095],all_other9380_MF_rows_kept=True,explicit_nonMF_owned_library_targets=targets[:2],failed_material_A_authority=failed,closed_old_AX_owner_authorities=owners,current_short_FIL_v10_actual_pins=extras,retained_sameSHA_science_AX_pin=scientific,complete_owner_inventory=before,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-4,V12_spectator_inventory=v12before,original_caps=oldsf['original_caps'],future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,future_original_current_fullfresh2_budget_admission=None,prediction_is_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=z)])for n,a,z in others]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('exact inverse splice')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('three complete byte inverses')
 iv=write(OUT/'COMPLETE_LITERAL1_TO_LITERAL4_BEFORE_SHORT_FIL_RETRY_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL1_TO_LITERAL4_BEFORE_SHORT_FIL_RETRY_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);sf.update(schema='COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal4_fullpins=targets,target_count=4,target_bytes=TOTAL,historical_evidence_pins=hist,closed_failed_M9_material_A_authority=failed,closed_old_AX_owner_authorities=owners,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=plan,strict_low_level_Source_provenance_pin=iv,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=write(OUT/'COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_FREEZE.json',sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT4_SHORT_FIL_RETRY_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=plan,inverse_pin=iv,preparer_pin=pin(__file__),target_count=4,target_bytes=TOTAL,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-4,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()


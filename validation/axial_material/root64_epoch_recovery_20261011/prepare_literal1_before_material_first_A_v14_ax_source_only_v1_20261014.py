"""Prepare exactly one retired private v14 AX copy; no scientific EOF or mutation."""
import ast, importlib.util, json, os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec=importlib.util.spec_from_file_location('bounded_source_helpers',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write,inventory,identity,norm=h.pin,h.read,h.write,h.inventory,h.identity,h.norm
OLD=h.OUT
OUT=R/'storage_release_literal1_before_material_first_A_v14_ax_source_v1_20261014'
NAMES=h.NAMES
OLD_LABEL='LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES'
LABEL='LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE'
TOTAL=17165624
BUILD_PROOF="""def material75_build_closed_proof():
 p=read(CLOSED_BUILD75['independent_postreview_pin']);pt=read(CLOSED_BUILD75['independent_posttools_pin']);d=read(CLOSED_BUILD75['summary_pin']);t=read(CLOSED_BUILD75['Root_true_tool_pin']);a=read(CLOSED_BUILD75['Root_exact_argv_pin']);cli=read(CLOSED_BUILD75['exact_cli_pin']);q=t['actual_terminal_return']
 if p['schema']!='INDEPENDENT_MATERIAL75_AFTER_V18_SAVED370_V9_ACTUAL_BUILD_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_MATERIAL75_AFTER_V18_SAVED370_V9_BUILD_POSTVERIFICATION'or p['failure']is not None:raise RuntimeError('exact material75 build post0 protocol')
 for k,v in(('actual_report_pin','summary_pin'),('actual_Root_true_tool_return_pin','Root_true_tool_pin'),('actual_Root_argv_pin','Root_exact_argv_pin'),('actual_Host_freeze_pin','Host_freeze_pin'),('actual_CLI_pin','exact_cli_pin')):
  if p[k]!=CLOSED_BUILD75[v]:raise RuntimeError('material75 exact canonical '+k)
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('material75 independent readonly only')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('material75 post closed0')
 for k in('actual_review_return','actual_postverification_return'):
  z=pt[k]
  if type(z['exit_code'])is not int or z['exit_code']!=0 or z.get('session_id')is not None or b.norm(json.loads(z['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_BUILD75['independent_postreview_pin']:raise RuntimeError('material75 genuine post typed0')
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_argv']!=cli['exact_reviewable_argv']or len(a['exact_argv'])!=44:raise RuntimeError('material75 original Root0 exact44')
 if d['schema']!='ACTUAL_CURRENT_FORMAL_FIVE_OBSERVATION_SOURCE_COMPLETE75_BUILD_ONLY_V1'or d['status']!='ACTUAL_FIVE_COMPILE_COMPLETE75_LINK_CLOSED0_ONLY'or d['failure']is not None or d['after_check_error']is not None or len(d['records'])!=6 or any(z['status']!='PASS'for z in d['records'])or len(d['fixed_current_pins'])!=5697 or len(d['output_pins'])!=20 or p['actual_Dragon_linked']is not True or p['actual_material_job_execution_by_Root']is not False or p['actual_observation_context_produced']is not False:raise RuntimeError('actual compile5 link75 only; no firstA qualification')
 return CLOSED_BUILD75

def prior_v12_physical_completion_proof():
 p=read(CLOSED_V12_COMPLETION['independent_postreview_pin']);pt=read(CLOSED_V12_COMPLETION['independent_posttools_pin']);t=read(CLOSED_V12_COMPLETION['Root_true_tool_pin']);r=read(CLOSED_V12_COMPLETION['receipt_pin'])
 if p['schema']!='INDEPENDENT_LITERAL2_BEFORE_MATERIAL75_V12_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_LITERAL2_BEFORE_MATERIAL75_V12_EXACT_RELEASE_PHYSICAL_COMPLETION_POSTVERIFICATION_ROOT_POSTCHECK_FAILURE_RETAINED'or p['failure']is not None or p['actual_Root_exit_code']!=1 or p['original_Root_terminal_failure_preserved']is not True or p['actual_two_ordered_unlinks_directory_fsync_and_absence_complete']is not True or p['actual_deleted_count']!=2 or p['actual_logical_bytes_released']!=45167892 or p['all2_exact_targets_absent']is not True:raise RuntimeError('exact previous V12 physical completion with Root1 retained')
 for k,v in(('actual_release_receipt_pin','receipt_pin'),('actual_Root_true_tool_pin','Root_true_tool_pin'),('actual_manifest_pin','manifest_pin')):
  if p[k]!=CLOSED_V12_COMPLETION[v]:raise RuntimeError('previous V12 canonical '+k)
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','deletion_executed_by_reviewer'))or r['status']!='STOPPED_POSTCHECK'or t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1:raise RuntimeError('original V12 postcheck failure immutable')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('previous V12 completion post closed0')
 for k in('actual_review_return','actual_postverification_return'):
  z=pt[k]
  if type(z['exit_code'])is not int or z['exit_code']!=0 or z.get('session_id')is not None or b.norm(json.loads(z['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_V12_COMPLETION['independent_postreview_pin']:raise RuntimeError('previous V12 genuine post typed0')
 return CLOSED_V12_COMPLETION
"""
def main():
 if OUT.exists():raise RuntimeError('unique Source-only namespace')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_SOURCE_FREEZE.json');oldsf=read(oldsfpin)
 mfpin=pin(OLD/'EXACT_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_MANIFEST.json');mf=read(mfpin);rows=mf['current_protected_full_EOF_pins'];target=norm(rows[4203]);targets=[target]
 expected='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/AAA/ax_current.xsm'
 if len(rows)!=9239 or target['path']!=expected or target['size_bytes']!=TOTAL or target['sha256']!='784d17d00e9398d580a90c3fd08061e0f16a99090794f20620e7f3a36f92aac2':raise RuntimeError('exact1 MF9239 index4203')
 root=Path(target['path']).parents[1];st=Path(target['path']).lstat()
 if identity(st)!=target['identity']or st.st_uid!=os.getuid()or st.st_nlink!=1:raise RuntimeError('target full current7 UID singlelink')
 source=(OLD/NAMES[0]).read_text();current=source;changes=[]
 def node(n):return next(x for x in ast.parse(current).body if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name)and x.targets[0].id==n)
 def const(n):return ast.literal_eval(node(n).value)
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('unique complete splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 def assign(n,v):change(ast.get_source_segment(current,node(n)),n+'='+repr(v))
 def fn(n):return ast.get_source_segment(current,next(x for x in ast.parse(current).body if isinstance(x,ast.FunctionDef)and x.name==n))
 bpdir=R/'independent_material75_after_v18_saved370_v9_actual_build_postverify_20261014';bp=pin(bpdir/'REVIEW.json');bt=pin(bpdir/'TRUE_TOOL_RETURNS.json');post=read(bp)
 build=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=bp,independent_posttools_pin=bt)
 cpdir=R/'independent_literal2_before_material75_v12_actual_completion_postverify_20261014';cp=pin(cpdir/'REVIEW.json');ct=pin(cpdir/'TRUE_TOOL_RETURNS.json');completionpost=read(cp)
 completion=dict(receipt_pin=completionpost['actual_release_receipt_pin'],Root_true_tool_pin=completionpost['actual_Root_true_tool_pin'],manifest_pin=completionpost['actual_manifest_pin'],independent_postreview_pin=cp,independent_posttools_pin=ct)
 d=read(build['summary_pin']);hf=read(build['Host_freeze_pin']);latest=const('CLOSED_FULL50');full=read(latest['summary_pin']);fullhf=read(latest['Host_freeze_pin']);saved=const('CLOSED_SAVED');sd=read(saved['summary_pin']);keep=const('ROLE_KEEP_PINS')
 direct=[hf['dependencies'],d['fixed_current_pins'],d['output_pins'],full['fixed_current_pins'],full['output_pins'],fullhf['dependencies'],sd['fixed_current_pins'],sd['output_pins'],sd['actual_TMP_output_pins']]+[x['current_pins']for x in const('DOWNSTREAM_ORIGINS')]
 if any(any(p['path']==target['path']for p in rr)for rr in direct):raise RuntimeError('target absent from every direct current runtime/science authority')
 same=next(p for p in keep if Path(p['path']).name=='ax_current.xsm')
 if same['sha256']!=target['sha256']or same['size_bytes']!=TOTAL or same['identity'][:2]==target['identity'][:2]or identity(Path(same['path']).lstat())!=same['identity']:raise RuntimeError('retained scientific original completeSHA and distinct current node')
 before=inventory([root]);v12root=Path(const('CLOSED_OWNER_V12')['summary_pin']['path']).parent;v12before=inventory([v12root])
 if len(v12before['ordinary_file_identities'])!=259 or len(v12before['directory_identities'])!=32:raise RuntimeError('actual postcompletion V12 259files32dirs baseline')
 hist=dict(const('HISTORICAL_PINS'));hist.update(previous9239_manifest=mfpin,predecessor_cleanup_Source_freeze=oldsfpin,latest_build75_post=bp,latest_build75_posttools=bt,previous_v12_physical_completion_post=cp,previous_v12_physical_completion_posttools=ct)
 for key,p in build.items():hist['actual_material75_'+key]=p
 for key,p in completion.items():hist['previous_v12_completion_'+key]=p
 extra=[pin(R/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/COMPLETE_POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json'),pin(R/'bind_actual_material_first_A_after_observer75_v9_source_only_v1_20261014.py'),pin(R/'ACTUAL_FIRST_A_AFTER_OBSERVER75_V9_SOURCE_ONLY_CLI_BINDING_TRUE_TOOL_RETURNS_20261014.json')]
 mdir=Path(build['Host_freeze_pin']['path']).parent
 extra+=[pin(mdir/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json'),pin(mdir/'COMPLETE_ACTUAL_V18_SAVED370_BOUND_MATERIAL_GENDF_ONCE_METADATA_PUBLICATION.json')]
 sourcepins=list({p['path']:p for p in list(const('BIND_NEW_SOURCE_PINS'))+list(build.values())+list(completion.values())+extra}.values())
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[4203]),('HISTORICAL_HF_TARGET_INDICES',[]),('BASELINE_OWNED_INVENTORIES',before),('V12_BASELINE',v12before),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',len(before['ordinary_file_identities'])),('OWNER_DIRECTORY_COUNT',len(before['directory_identities']))]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path('+repr(str(root))+')]')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal1_before_material_first_A_v14_ax_actual_receipts_20261014'\nCLOSED_BUILD75="+repr(build)+'\nCLOSED_V12_COMPLETION='+repr(completion))
 for k,v in [('SF','COMPLETE_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace(OLD_LABEL,LABEL).replace('len(TARGETS)!=2','len(TARGETS)!=1').replace('len(TARGET_PATHS)!=2','len(TARGET_PATHS)!=1').replace("f['closed_v12_owner_authority']!=CLOSED_OWNER_V12","f['closed_v12_owner_authority']!=CLOSED_OWNER_V12 or f['closed_current_build75_authority']!=CLOSED_BUILD75 or f['closed_previous_v12_physical_completion_authority']!=CLOSED_V12_COMPLETION"))
 change(fn('disjoint'),fn('disjoint').replace('!=2','!=1'))
 change(fn('closed_proofs'),fn('closed_proofs').replace('saved370_closed_proof()]','saved370_closed_proof(),material75_build_closed_proof(),prior_v12_physical_completion_proof()]')+'\n\n'+BUILD_PROOF)
 f=fn('current_protection').replace("HISTORICAL_PINS['previous9163_manifest']","HISTORICAL_PINS['previous9239_manifest']").replace('9163','9239').replace('9161','9238').replace('[2319,2320]','[4203]').replace('OWNER_FILE_COUNT-2','OWNER_FILE_COUNT-1').replace('only2','only1').replace('exact2','exact1').replace('EXACT_TWO_V12_PRIVATE_COPY_BODIES_HISTORICAL','EXACT_ONE_V14_PRIVATE_AX_COPY_BODY_HISTORICAL').replace('MF2_indices','MF1_indices').replace('all_other_v12_owner_files_kept','all_other_v14_owner_files_kept')
 anchor=" for p in ROLE_KEEP_PINS:add(p,'all_original_scientific9_current')"
 block=" build_actual=read(CLOSED_BUILD75['summary_pin']);build_post=read(CLOSED_BUILD75['independent_postreview_pin']);build_hf=read(CLOSED_BUILD75['Host_freeze_pin'])\n for p in list(CLOSED_BUILD75.values())+build_hf['dependencies']+build_actual['fixed_current_pins']+build_actual['output_pins']+build_post['actual_scene_full_EOF_pins']:add(p,'actual_current_observer75_build_all_Source_objects_and_outputs')\n for p in list(CLOSED_V12_COMPLETION.values()):add(p,'previous_V12_physical_completion_original_Root1_and_readonly_post0')\n"
 if f.count(anchor)!=1:raise RuntimeError('one current build closure insertion')
 change(fn('current_protection'),f.replace(anchor,block+anchor));ast.parse(current)
 others=[]
 for name in NAMES[1:]:
  a=(OLD/name).read_text();z=a.replace(OLD_LABEL,LABEL).replace('target_count=2','target_count=1').replace("m['target_count']!=2","m['target_count']!=1").replace("before['regular_files']-after['regular_files']!=2","before['regular_files']-after['regular_files']!=1").replace('deleted_files=2','deleted_files=1');ast.parse(z);others.append((name,a,z))
 funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(source)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven low-level funcs complete originalbytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";a,z=others[1][1:]
 if a[a.index(start):a.index(end)]!=z[z.index(start):z.index(end)]:raise RuntimeError('original unlink truthreceipt dirfsync FirstFailure bytes')
 ns=dict(read=read,CLOSED_BUILD75=build,CLOSED_V12_COMPLETION=completion,shlex=__import__('shlex'),json=json,b=type('B',(),{'norm':staticmethod(norm)}))
 exec(compile(BUILD_PROOF,'<Source-only-actual-build-and-previous-physical-completion>','exec'),ns);ns['material75_build_closed_proof']();ns['prior_v12_physical_completion_proof']()
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,z in others:write(OUT/name,z)
 pp=write(OUT/'EXACT_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_ROLE_SOURCE_PLAN_V1',source_only=True,literal1_fullpins=targets,target_count=1,target_bytes=TOTAL,previous9239_manifest_pin=mfpin,exact_current_MF1_indices_migrated_to_history=[4203],all_other9238_PF_rows_data_retained=True,current_HF_target_indices=[],retained_sameSHA_distinctnode_original_science_pin=same,complete_owner_inventory=before,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-1,postcompletion_current_V12_spectator_inventory=v12before,closed_current_build75_authority=build,closed_previous_v12_physical_completion_authority=completion,live_saved_TMP24_allscience9_two_pairs_build75_outputs_kept=True,original_caps=oldsf['original_caps'],future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,future_original_current_fullfresh2_budget_admission=None,predicted_margin_bytes=1973055,predicted_margin_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=z)])for n,a,z in others]
 for e in entries:
  back=Path(e['candidate_pin']['path']).read_text()
  for c in reversed(e['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('unique wholeinverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('three wholebyte inverses')
 ip=write(OUT/'COMPLETE_LITERAL2_TO_LITERAL1_BEFORE_MATERIAL_FIRST_A_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL2_TO_LITERAL1_BEFORE_MATERIAL_FIRST_A_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);sf.update(schema='COMPLETE_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal3_fullpins=targets,literal2_fullpins=targets,literal1_fullpins=targets,target_count=1,target_bytes=TOTAL,historical_evidence_pins=hist,closed_current_build75_authority=build,closed_previous_v12_physical_completion_authority=completion,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=ip,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=write(OUT/'COMPLETE_LITERAL1_BEFORE_MATERIAL_FIRST_A_V14_AX_DUPLICATE_SOURCE_FREEZE.json',sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT1_BEFORE_MATERIAL_FIRST_A_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=pp,inverse_pin=ip,preparer_pin=pin(__file__),target_count=1,target_bytes=TOTAL,owner_file_count=len(before['ordinary_file_identities']),owner_directory_count=len(before['directory_identities']),retained_other_file_count=len(before['ordinary_file_identities'])-1,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()

"""Independent Source/metadata/current7 review only. Never imports candidate code."""
from pathlib import Path
import ast,hashlib,json,os,stat,time
D=Path(__file__).parent.parent
HERE=Path(__file__).parent
START=time.monotonic()
SYSTEM=[]
def need(v,m):
 if not v:raise RuntimeError(m)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute() and not any(x.is_symlink() for x in (q,*q.parents)) and stat.S_ISREG(s.st_mode) and identity(s)==p['identity'] and s.st_size==p['size_bytes'],'exact current7 '+str(q))
 fortran=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256')=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and s.st_nlink==2
 need(s.st_nlink==1 or fortran,'single-link role')
 need(s.st_uid==os.getuid() or (s.st_uid==0 and p in SYSTEM),'exact existing system role ownership')
 return q
def full(p):
 q=current(p);need(p['size_bytes']<8*2**20,'small Source/metadata only')
 for _ in range(2):
  h=hashlib.sha256(q.read_bytes()).hexdigest();need(h==p['sha256'],'small whole SHA '+str(q));current(p)
 return q.read_text()
def ownpin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes();need(identity(q.lstat())==identity(s),'own metadata stable7')
 return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=s.st_size,identity=identity(s))
def meta(p):return json.loads(full(p))
def functions(p):
 s=Path(p).read_text();t=ast.parse(s)
 return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def genuine(raw,p,outkey,code=0):
 t=raw['actual_review_return'] if outkey=='review_pin' else raw['actual_terminal_return']
 need(raw['observed_closed'] is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine closed typed return')
 need(json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine artifact pin')
def main():
 ap=ownpin(D/'AUTHOR_SOURCE_FREEZE.json');need(ap['sha256']=='3f928ba94b19fd43e10febea6fbefab8833177578379f41625ffba7375296095' and ap['size_bytes']==6483,'exact final author')
 author=meta(ap);plan=meta(author['plan_pin']);need(author['plan_pin']['sha256']=='598a7942d690afdd34b7dbcfa631747c24b1609c6655611645eff7a48961ddeb','exact final plan')
 build=json.loads(Path(plan['original_guard_build_plan_pin']['path']).read_text())
 SYSTEM.extend(build['readonly_system_tool_metadata_pins']+build['readonly_system_SDK_header_pins']+[build['C_compiler_pin']])
 need(meta(build['C_compiler_tool_full_pin_metadata'])['compiler_tool_pin']==build['C_compiler_pin'],'exact frozen existing C tool role')
 full(plan['original_guard_build_plan_pin'])
 pins=plan['complete_source_file_pins'];need(pins==author['complete_source_file_pins'] and len(pins)==5 and pins==[plan[k] for k in ('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin')],'whole exact five Sources')
 texts={Path(p['path']).name:full(p) for p in pins}
 for s in texts.values():ast.parse(s)
 evidence=meta(author['whole_original_math_inverse_evidence_pin']);static=meta(author['scope_resource_static_evidence_pin'])
 for row in evidence['whole_four_file_reverse_evidence']:
  old=full(row['original_Source_pin']);new=full(row['new_Source_pin']);restored=new
  for edit in sorted(row['whole_file_inverse_edits'],key=lambda r:r['new_offset'],reverse=True):
   i=edit['new_offset'];v=edit['new_exact'];need(restored[i:i+len(v)]==v,'inverse exact fragment');restored=restored[:i]+edit['original_exact']+restored[i+len(v):]
  need(restored==old,'whole-file inverse exact')
  current(row['new_Source_pin'])
 deck=functions(plan['deck_builder_Source_pin']['path']);reader=functions(plan['readback_Source_pin']['path']);launcher=functions(plan['launcher_Source_pin']['path'])
 for oldpath,row in evidence['whole_original_function_proofs'].items():
  full(row['full_Source_pin']);orig=functions(oldpath)
  target=reader if 'white_receiver_tracking.py' in oldpath else launcher if 'open_exact_three' in oldpath else deck
  for name in row['whole_function_names']:need(target[name]==orig[name],'whole original function '+name)
 oldread=evidence['whole_four_file_reverse_evidence'][3]['original_Source_pin'];orig=functions(oldread['path'])
 for name in evidence['whole_bounded_readback_nine_math_functions']:need(reader[name]==orig[name],'whole readback function '+name)
 full(evidence['SPOLIB_SPOCPD_Source_pin']);full(evidence['SPOT_source_formula_reference_pin'])
 for name in ['geometry_MIX_is_snapshot_selector_not_global_material_number','no_NMIX1_assumption','IPOS_absent_SCAT_exact_LCMLEN_zero_semantics_preserved']:need(evidence[name]is True,'material mapping source evidence')
 need(evidence['actual_library_compiled_SPOT_Source_identity_automatically_claimed']is False,'no unsaved library Source identity claim')
 need("s.get(scatname,(None,0,None))[1]" in reader['verify_macro_blocks'] and "for g in range(1,371)" in reader['verify_macro_blocks'],'full SPOLIB SCAT/IPOS/370 scope')
 mapping=reader['verify_complete_three_plane_material_mapping']
 for fragment in ['for region in range(nreg)','for floor in range(48)','original+(slot-1)*nmix','tuple(expected)!=actual or middle==0','outtrack[3]!=3*nmix or outmacro[1]!=3*nmix']:
  need(fragment in mapping,'complete actual MATCOD mapping gate')
 out=Path(plan['planned_actual_output_root']);roots=plan['complete_joint_roots']
 need(len(roots)==len(set(roots))==87 and str(out)==roots[-1] and not os.path.lexists(out),'complete87 and fresh owning output')
 need(not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'disjoint full roots')
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 need(plan['original_caps']==caps and plan['bounded_new_output_reservation_bytes']==128*2**20 and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20,'unchanged caps and local conditional128/Source8')
 cfg=plan['production_config'];prepared=meta(plan['formal_prepared_current_epoch_full_pin']);di=meta(plan['formal_deck_inputs_current_epoch_full_pin']);spec=meta(plan['formal_case_spec_current_epoch_full_pin'])
 need(cfg==prepared['production_config']==di['config']==author['formal_frozen_config'] and cfg['rank']==1 and cfg['cells_per_zone']==16 and cfg['sn']==32 and cfg['eps_mccg']==2.5e-8,'actual frozen configuration')
 need(di['training_slots']==spec['basis']['training_slots']==['A','B','A'] and spec['basis']['fixed_once_for_both_cases']is True and spec['basis']['requested_rank']==1,'original one shared rank1 training contract')
 pp=meta(plan['PACK_actual_post_pin']);pt=meta(plan['PACK_actual_post_tools_pin']);rr=meta(plan['PACK_Root_report_pin']);rt=meta(plan['PACK_Root_tools_pin'])
 genuine(pt,plan['PACK_actual_post_pin'],'review_pin');genuine(rt,plan['PACK_Root_report_pin'],'report_pin')
 need(rr['failure']is None and pp['failure']is None and rr['actual_complete_PACK_pin']==pp['actual_complete_PACK_pin']==plan['PACK_full_pin'] and rr['actual_ordered_three_RCON_pins']==pp['actual_ordered_three_RCON_pins']==plan['ordered_three_plane_RCON_pins'],'actual new PACK0/post0 exact roles')
 need(pp['Root_recorded_full18_and_three_RCON_and_strict_plane_readback_verified']is True and len(pp['actual_independent_complete18_tree_proofs'])==18 and len(pp['actual_independent_three_RCON_tree_proofs'])==3 and len(pp['actual_independent_strict_plane_case_epoch_type4_keff_proofs'])==3,'prior complete18/RCON/strict real readback')
 need(roots==rr['complete_joint_roots']+[str(out)],'inherits complete86 into87')
 for k in ['future_actual_Root_report_pin','future_actual_Root_tools_pin','future_actual_independent_post_pin','future_actual_independent_post_tools_pin','future_actual_new_context_scientific_outputs','future_actual_new_common_basis_rank_admission','future_actual_Root_tools_current_epoch_EOF_proof_pins','latest_actual_resource_reservation']:need(plan[k]is None,'future actual remains NULL')
 for k in ['GLOBAL_or_PROJECT_produced','new_B_formal13_compatible','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete','old_allA_basis_or_context_reused']:need(plan[k]is False,'no premature qualification')
 need(plan['small_tools_current_epoch_EOF_proof_not_yet_executed']is True and plan['new_shared_basis_and_rank_not_yet_computed']is True,'no future tool/basis claim')
 tables=['explicit_cumulative_metadata_file_pins','retained_current7_pins','retained_archive_metadata_current7_pins','retained_B2_current_epoch_readonly_pins','selected31_current_epoch_readonly_pins','readonly_history_code_and_selected_native_pins']
 rows={}
 for table in tables:
  for p in plan[table]:
   if p['path']in rows:need(rows[p['path']]==p,'one complete pin per path')
   rows[p['path']]=p
 for p in [plan['runtime_pin'],plan['PACK_full_pin'],*plan['ordered_three_plane_RCON_pins'],*plan['small_tool_saved_SHA_and_current7_candidate_roles'].values()]:current(p)
 for row in plan['producers']:current(row['archive']);current(row['radial_binary_track'])
 for table in ['retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins']:
  for p in plan[table]:need(set(p)=={'path','size_bytes','identity'},'failed partial stat-only schema');current(p)
 for _ in range(2):
  for p in rows.values():current(p)
  need(len(plan['exact59_historical_absent_pins'])==59 and all(not os.path.lexists(p['path'])for p in plan['exact59_historical_absent_pins']),'exact historical59 absent only')
 cli=json.loads((D/'ROOT_REVIEWABLE_CLI_PENDING_GENUINE_SOURCE_PEER0.json').read_text());args=cli['argv']
 need(len(args)==20 and json.loads(args[13])==plan['host_source_pin'] and json.loads(args[15])==author['plan_pin'] and args[17]=='__GENUINE_INDEPENDENT_SOURCE_REVIEW_FULL_PIN__' and args[19]=='__GENUINE_INDEPENDENT_SOURCE_REVIEW_TOOLS_FULL_PIN__','exact twenty argv two placeholders only')
 need(cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','Root actual permission mode')
 need(static['original_caps']==caps and static['complete_joint_roots']==roots and static['remaining_fresh_bytes_before_final_PLAN_author_metadata']>0,'bounded Source-only resource evidence')
 host=texts[Path(plan['host_source_pin']['path']).name]
 for fragment in ['claim_before_bound_metadata_or_helper_import=True','full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)','small-tool SHA and actual current7 fullEOF before any invocation',"['train','rank','white_tracking','make_route_contract','initial','axial']",'time.monotonic()-readback_started<600','last_scan=time.monotonic()']:
  need(fragment in host,'reviewed owning Host guard/control flow')
 report=dict(schema='INDEPENDENT_SOURCE_ONLY_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT',source_only=True,failure=None,source_pin=plan['host_source_pin'],plan_pin=author['plan_pin'],complete_source_file_pins=pins,author_freeze_pin=ap,whole_inverse_evidence_pin=author['whole_original_math_inverse_evidence_pin'],source_resource_evidence_pin=author['scope_resource_static_evidence_pin'],reviewer_Source_pin=ownpin(__file__),reviewer_task_name='/root/b2_build_source_peer',complete_joint_root_count=87,original_caps=caps,conditional_output_limit_bytes=128*2**20,local_Source_limit_bytes=8*2**20,complete_retained_current7_unique_count=len(rows),whole_original_geometry_rank_white_FD_functions_equal=True,whole_four_Source_inverse_independently_reconstructed=True,full_SPOLIB_all370_all_metadata_and_SCAT_IPOS_NMIX_NFIS_semantics_reviewed=True,full_region_major48floor_original_MATCOD_and_middle_B_block_verification_required=True,old_library_compiled_SPOT_Source_equivalence_claimed=False,genuine_new_PACK_Root0_and_independent_post0_bound=True,small_tool_SHA_EOF_is_future_Root_guarded_action=True,six_stage_business_and_readback_not_executed=True,scientific_body_opened=False,scientific_body_SHA_recomputed=False,candidate_or_helper_imported=False,compiler_or_native_or_worker_executed=False,files_deleted=False,GLOBAL_or_PROJECT_produced=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,wall_seconds=time.monotonic()-START)
 q=HERE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=ownpin(q))),flush=True)
if __name__=='__main__':main()

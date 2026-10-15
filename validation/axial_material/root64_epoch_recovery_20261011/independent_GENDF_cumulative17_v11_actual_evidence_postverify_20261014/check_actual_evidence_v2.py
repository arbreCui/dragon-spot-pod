from pathlib import Path
import collections,hashlib,json,math,os,shlex,stat,traceback
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
A=Path('/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11')
E=A.with_name(A.name+'-evidence');D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes'];return s
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<=64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def tool0(t,p):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
def actual_inventory(root):
 out=[]
 for cwd,dirs,files in os.walk(root,followlinks=False):
  assert not Path(cwd).is_symlink()
  for n in dirs:assert not(Path(cwd)/n).is_symlink()
  for n in files:
   p=Path(cwd)/n;s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink();out.append((str(p),s.st_size))
 return out
def main(result):
 hp=pin(A/'Root_actual_eleven_saved_gendf_extraction_summary.json');h=load(hp)
 ap=pin(R/'ROOT_EXACT_GENDF_CUMULATIVE17_ACTUAL32_ARGV_20261014.json');argv=load(ap)
 tp=pin(R/'ROOT_ACTUAL_GENDF_CUMULATIVE17_ACTUAL32_TRUE_TOOL_RETURNS_20261014.json');true=load(tp);z=true['actual_terminal_return']
 assert true['observed_closed']is True and type(true['original_integer_exit_code'])is int and true['original_integer_exit_code']==0
 assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and z['output']==''
 assert true['actual_initial_return']['session_id']==52360 and true['actual_initial_return']['chunk_id']=='974f28'and z['chunk_id']=='c947c6'
 assert true['exact_executed_command']==argv['shell_safe_command']and shlex.split(true['exact_executed_command'])==argv['argv']and len(argv['argv'])==32
 assert h['schema']=='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_GUARDED_ROOT_V1'and h['status']=='ACTUAL_ELEVEN_SAVED_MT5_EXTRACTION_CLOSED0_ONLY'and h['failure']is None and h['after_check_error']is None
 result.update(actual_aggregate_host_pin=hp,actual_aggregate_report_pin=h['actual_child_receipt']['report'],actual_Root_true_tool_pin=tp,actual_Root_argv_pin=ap,actual_Root_integer_exit_code=z['exit_code'],actual_host_status=h['status'],actual_host_failure=h['failure'],actual_host_after_check_error=h['after_check_error'])
 fdir=R/'independent_GENDF_cumulative17_final_SF_HF_recipe_ROOT32_metadata_review_20261014';fp=pin(fdir/'REVIEW.json');ft=pin(fdir/'TRUE_TOOL_RETURNS.json');final=load(fp);tool0(load(ft),fp)
 assert final['failure']is None and final['status']=='PASS_GENDF_CUMULATIVE17_FINAL_METADATA_READY_FOR_UNIQUE_RUNTIME'and final['actual_Root_argv_pin']==ap
 sf=load(final['actual_Source_freeze_pin']);hf=load(final['actual_Host_freeze_pin']);assert h['source_freeze_pin']==final['actual_Source_freeze_pin']and h['actual_material_observation_report_pin']==argv['actual_material_observation_report_pin']==final['actual_material_observation_report_pin']
 fixed=h['fixed_current_pins'];table={p['path']:p for p in hf['dependencies']+[final['actual_Host_freeze_pin']]}
 assert len(fixed)==len({p['path']for p in fixed})==6001 and table=={p['path']:p for p in fixed}
 for p in fixed:seven(p)
 for p in sf['cumulative_explicit_metadata_file_pins']:assert pin(p['path'])==p
 cp=h['actual_child_receipt']['report'];c=load(cp);assert c['schema']=='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_EXTRACTION_EVIDENCE_V1'and c['status']==h['actual_child_receipt']['status']=='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY'
 binding=load(c['execution_binding_pin']);assert binding['fixed_current_pins']==fixed and binding['source_freeze_pin']==h['source_freeze_pin']==c['source_freeze_pin']and binding['actual_material_observation_report_pin']==h['actual_material_observation_report_pin']==c['actual_material_observation_report_pin']
 assert binding['selected_genDF_source_plan_pin']==c['selected_genDF_source_plan_pin']==h['selected_genDF_source_plan_pin']and binding['requested_mts']==[5]and binding['output_directory']==str(E)
 planned=load(h['selected_genDF_source_plan_pin']);assert len(planned['inputs'])==len(c['actual_extractions'])==11 and c['all370_P0_entries_masks_and_actual_grids_retained']is True and c['original_parser_math_unchanged']is True
 quals=['DRAGR_packed_raw_words_replayed','current_SPH_MASK_context_applied','three_current_raw_MACRO_comparisons_performed','complete_reaction_authority_qualified','physical_neutron_balance_qualified','unreduced_reference_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','goal_complete']
 for o in [h,c,binding,h['actual_child_receipt']]:
  for k in quals:assert o[k]is False
 for o in [h,c]:assert o['native_engines_started']==0 and o['original_input_or_library_writes']==0
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2**31,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 assert h['original_caps']==c['original_caps']==binding['original_caps']==sf['original_caps']==final['original_caps']==caps
 outputs=h['complete_output_pins'];assert len(outputs)==len({p['path']for p in outputs})==17
 for p in outputs:assert pin(p['path'])==p
 inventory=dict(actual_inventory(A)+actual_inventory(E));assert set(inventory)=={p['path']for p in outputs}|{hp['path']}
 assert all(inventory[p['path']]==p['size_bytes']for p in outputs+[hp])
 assert all(p in outputs for p in h['owned_input_pins'])and cp in outputs
 assert len(h['records'])==len(h['actual_watchdog_checks'])==1
 record=h['records'][0];watchpin=next(p for p in outputs if p['path']==h['actual_watchdog_checks'][0]['path']);watch=load(watchpin)
 assert watchpin['sha256']==h['actual_watchdog_checks'][0]['sha256']and watch['command']==record['command']and record['status']=='PASS'and record['label']=='gendf-stage/all_eleven_saved_MT5'
 assert type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True
 assert watch['sampled_peak_rss_mib']==h['actual_watchdog_checks'][0]['peak_rss_mib']and watch['elapsed_seconds']==h['actual_watchdog_checks'][0]['elapsed_seconds']
 logpin=next(p for p in outputs if p['path']==str(A/'gendf-stage/all_eleven_saved_MT5.log'));assert logpin['sha256']==record['log_sha256']
 assert load(next(p for p in outputs if p['path']==str(A/'gendf-stage/stages.json')))==h['records']
 assert type(h['SELF_peak_bytes'])is int and h['SELF_peak_bytes']<512*2**20 and 0<h['wall_seconds']<1800
 roots=sf['cumulative_artifact_root_paths']+sf['cumulative_Source_root_paths'];assert len(roots)==len(set(roots))==sf['complete_cumulative_joint_root_count']==17 and len(sf['cumulative_artifact_root_paths'])==10 and len(sf['cumulative_Source_root_paths'])==7 and binding['joint_archive_roots']==roots==final['cumulative_joint_roots']
 assert binding['cumulative_explicit_metadata_file_pins']==sf['cumulative_explicit_metadata_file_pins']==final['cumulative_explicit_metadata_file_pins']and len(binding['cumulative_explicit_metadata_file_pins'])==2
 metadata_bytes=sum(p['size_bytes']for p in binding['cumulative_explicit_metadata_file_pins']);assert metadata_bytes==15660
 for i,p in enumerate(roots):
  q=Path(p);assert q.is_dir()and not q.is_symlink()
  for other in roots[i+1:]:assert not q.is_relative_to(other)and not Path(other).is_relative_to(q)
 srcinventory=[pair for root in sf['cumulative_Source_root_paths']for pair in actual_inventory(root)];srcbytes=sum(n for p,n in srcinventory)+metadata_bytes;srccount=len(srcinventory)+2
 resource_snapshots=[record['resource_before'],record['resource_after'],h['resources_after']]
 for snap in resource_snapshots:
  j=snap['complete_joint_fresh'];history=snap['original_history_cold_free']
  assert j['resource_roots']==sf['cumulative_artifact_root_paths']and j['artifact_budget_bytes']==2**31 and j['min_free_bytes']==8*2**30
  assert snap['complete_Source_roots']==sf['cumulative_Source_root_paths']and snap['complete_Source_bytes']==srcbytes and snap['complete_Source_regular_files']==srccount
  assert type(snap['host_open_unlinked_bytes'])is int and snap['host_open_unlinked_bytes']>=0
  assert snap['complete_seventeen_role_joint_bytes']==j['artifact_bytes']+srcbytes+snap['host_open_unlinked_bytes']<=2**31
  assert history['artifact_budget_bytes']==96*2**30 and history['min_free_bytes']==8*2**30 and history['artifact_bytes']+2**31+20971764748+64*2**20<=96*2**30 and history['disk_free_bytes']>=8*2**30
  assert snap['host_SELF_peak_bytes']<512*2**20 and snap['host_whole_elapsed_seconds']<1800
 stats=[];inputpins=[];totals=collections.Counter()
 for row,decl in zip(c['actual_extractions'],planned['inputs']):
  assert row['nuclide']==decl['nuclide']and row['mat']==decl['mat']and row['input_pin']==decl['preserved_binary_GENDf_input_pin']and table[row['input_pin']['path']]==row['input_pin'];seven(row['input_pin']);inputpins.append(row['input_pin'])
  p=row['actual_complete_extraction_pin'];assert p in outputs;x=load(p)
  assert x['schema']=='SAVED_BINARY_GENDF_REACTION_P0_EXTRACTION_ONLY_V1'and x['input_pin']==row['input_pin']and x['mat']==row['mat']and x['energy_groups']==370 and x['requested_mts']==[5]and x['whole_file_records']==row['actual_whole_file_records']
  assert x['P0_reduction_arithmetic']=='binary64 math.fsum of all saved outgoing contributions; no renormalization'
  for k in ['current_SPH_MASK_context_produced','DRAGR_packed_raw_words_replayed','complete_reaction_authority_qualified','physical_neutron_balance_qualified','unreduced_reference_qualified']:assert x[k]is False
  assert x['native_engines_started']==x['library_writes']==0
  grids=x['original_full_MF1_temperature_dilution_energy_grids'];sections=x['actual_P0_sections'];assert len(grids)==row['actual_grid_count']and len(sections)==row['actual_sections']==2*len(grids)
  for g in grids:
   assert math.isfinite(g['temperature_K'])and len(g['ascending_energy_eV'])==371 and all(math.isfinite(v)and v>0 for v in g['ascending_energy_eV'])and all(a<b for a,b in zip(g['ascending_energy_eV'],g['ascending_energy_eV'][1:]))and len(g['sigma0_barn'])>0 and all(math.isfinite(v)and v>0 for v in g['sigma0_barn'])
  assert collections.Counter((s['temperature_K'],s['mf'])for s in sections)==collections.Counter((g['temperature_K'],mf)for g in grids for mf in [3,6])
  values=[];present=0
  for s in sections:
   assert s['mat']==row['mat']and s['mt']==5 and s['mf']in [3,6]and s['nz']==1 and s['nl']in [1,2]and type(s['LIST_records'])is int and s['LIST_records']>0
   assert len(s['incident_present'])==len(s['separable_spectrum_present'])==370 and all(type(v)is bool for v in s['incident_present']+s['separable_spectrum_present'])
   assert len(s['P0_vector64'])==s['nz']and all(len(vec)==370 and all(type(v)in [int,float]and math.isfinite(v)for v in vec)for vec in s['P0_vector64'])
   if s['separable_spectrum64']is not None:assert len(s['separable_spectrum64'])==370 and all(math.isfinite(v)for v in s['separable_spectrum64'])
   values.extend(v for vec in s['P0_vector64']for v in vec);present+=sum(s['incident_present'])
  summary=dict(nuclide=row['nuclide'],mat=row['mat'],input_pin=row['input_pin'],actual_complete_extraction_pin=p,actual_whole_file_records=x['whole_file_records'],actual_section_count=len(sections),actual_grid_count=len(grids),actual_energy_group_count=370,actual_temperatures_K=[g['temperature_K']for g in grids],actual_dilution_counts=[len(g['sigma0_barn'])for g in grids],actual_MT5_MF3_sections=len(grids),actual_MT5_MF6_sections=len(grids),actual_P0_entry_count=len(values),actual_finite_P0_entries=len(values),actual_nonzero_P0_entries=sum(v!=0 for v in values),actual_incident_mask_true_entries=present,actual_minimum_P0=min(values),actual_maximum_P0=max(values),actual_reaction_inventory_rows=len(x['reaction_inventory']))
  stats.append(summary);totals.update(whole_file_records=x['whole_file_records'],MT5_sections=len(sections),grids=len(grids),P0_entries=len(values),P0_finite_entries=len(values),P0_nonzero_entries=summary['actual_nonzero_P0_entries'],incident_mask_true_entries=present)
 assert totals['MT5_sections']==158 and totals['grids']==79 and totals['P0_entries']==58460
 for p in fixed:seven(p)
 for p in outputs+[hp,ap,tp,fp,ft]:seven(p)
 resource=h['resources_after'];hist=resource['original_history_cold_free']
 result.update(status='PASS_ACTUAL_GENDF_CUMULATIVE17_EVIDENCE_POSTVERIFICATION',failure=None,actual_child_status=c['status'],actual_child_integer_exit_code=watch['returncode'],actual_Source_freeze_pin=final['actual_Source_freeze_pin'],actual_Host_freeze_pin=final['actual_Host_freeze_pin'],actual_material_observation_report_pin=h['actual_material_observation_report_pin'],actual_execution_binding_pin=c['execution_binding_pin'],actual_final_metadata_review_pin=fp,actual_final_metadata_tools_pin=ft,all6001_fixed_current7_verified_twice=True,actual_fixed_input_count=6001,actual_complete_new_output_pins=outputs+[hp],actual_complete_new_output_count=18,actual_complete_new_output_bytes=sum(p['size_bytes']for p in outputs+[hp]),all_new_output_files_verified_EOF_SHA_and_current7=True,actual11_original_saved_GENDF_input_pins=inputpins,actual11_input7_verified_no_second_payload_EOF=True,actual_MT5_numerical_result_totals=dict(totals),actual_per_nuclide_results=stats,original_caps=caps,actual_watchdog_pin=watchpin,actual_watchdog_returncode=watch['returncode'],actual_watchdog_limit_failure=watch['limit_failure'],actual_watchdog_elapsed_seconds=watch['elapsed_seconds'],actual_watchdog_peak_rss_mib=watch['sampled_peak_rss_mib'],actual_SELF_peak_bytes=h['SELF_peak_bytes'],actual_host_wall_seconds=h['wall_seconds'],actual_cumulative_joint_roots=roots,actual_cumulative_ART_root_count=10,actual_cumulative_REC_root_count=7,actual_explicit_metadata_file_pins=binding['cumulative_explicit_metadata_file_pins'],actual_explicit_metadata_file_bytes=metadata_bytes,actual_complete_source_metadata_file_count=srccount,actual_complete_source_metadata_bytes=srcbytes,actual_after_joint_bytes=resource['complete_seventeen_role_joint_bytes'],actual_host_open_unlinked_bytes=resource['host_open_unlinked_bytes'],actual_after_history_bytes=hist['artifact_bytes'],actual_after_free_disk_bytes=hist['disk_free_bytes'],actual_original_history_cold_fresh2_metadata_reserve_margin_bytes=96*2**30-hist['artifact_bytes']-2**31-20971764748-64*2**20,original_17roots_plus2_explicit_metadata_same2GiB_verified=True,actual_current_original_factory_snapshots_preserved=True,old_scientific_payload_or_native_tree_repeated=False,only_new_small_output_EOF_read=True,diagnostic_scope='Saved binary GENDF MT5 P0 extraction, all 370 entries, explicit incident masks, MF1 temperature/dilution/energy grids; no renormalization.',qualification_limitations=planned['limitations'],reaction_multiplicity_or_complete_reaction_authority_inferred=False,all_original_qualification_flags_remain_false=True)
result=dict(schema='INDEPENDENT_ACTUAL_GENDF_CUMULATIVE17_EVIDENCE_POSTVERIFICATION_V1',status='FAILED_ACTUAL_GENDF_CUMULATIVE17_EVIDENCE_POSTVERIFICATION',failure=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
assert not(D/'REVIEW_v2.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
exitcode=0
try:main(result)
except Exception as e:result.update(failure=repr(e),actual_checker_traceback=traceback.format_exc());exitcode=1
result['reviewer_source_pin']=pin(__file__)
p=D/'REVIEW_v2.json'
with p.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],failure=result['failure'],review_pin=pin(p),actual_fixed_current_pin_count=result.get('actual_fixed_input_count'),actual_new_output_count=result.get('actual_complete_new_output_count'),actual_MT5_numerical_result_totals=result.get('actual_MT5_numerical_result_totals'))),flush=True)
raise SystemExit(exitcode)

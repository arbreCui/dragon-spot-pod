"""Independent actual PREP audit: STDlib reads only, no business module loaded."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,math,os,shlex,stat,struct,time

H=Path(__file__).resolve().parent
A=Path('/Users/wen/spot/validation/axial_material'); B=A.parent/'artifacts'
R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
F=A/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
FS='59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8'
S=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
O=B/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
C=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
BASE=B/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
PS='35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7'
TS='2bcce12bb05d50b7dabce828f14dc7bd1dbff2a3383af5ac0ab81dbc10d8050a'
DS='6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c'
DTS='d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c'
PINS={};READ_BYTES=0
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,wanted=None,retain=True):
 global READ_BYTES
 p=Path(p);before=ident(p);assert stat.S_ISREG(before[2]),(str(p),'ordinary file required')
 h=hashlib.sha256();parts=[]
 with p.open('rb')as f:
  while b:=f.read(1024*1024):
   h.update(b)
   if retain:parts.append(b)
 assert ident(p)==before,(str(p),'immutable identity changed during read')
 sha=h.hexdigest()
 if wanted:assert sha==wanted,(str(p),'full SHA mismatch',sha,wanted)
 READ_BYTES+=before[3];PINS[str(p)]={'path':str(p),'sha256':sha,'bytes':before[3],'identity':before}
 return b''.join(parts)if retain else sha
def obj(p,wanted=None):return json.loads(raw(p,wanted))
def typed(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return list(a)==list(b)and all(typed(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
 if type(a)is float:return math.isfinite(a)and math.isfinite(b)and struct.pack('!d',a)==struct.pack('!d',b)
 return a==b
def sorted_boundary(v):return json.loads(json.dumps(v,sort_keys=True,allow_nan=False))
def namespace(root):
 files={};dirs=[]
 for base,ds,fs in os.walk(root,followlinks=False):
  for name in ds:
   p=Path(base)/name;assert stat.S_ISDIR(p.lstat().st_mode);dirs.append(str(p.relative_to(root)))
  for name in fs:
   p=Path(base)/name;assert stat.S_ISREG(p.lstat().st_mode);files[str(p.relative_to(root))]=p
 return files,sorted(dirs)
def segment_pins(p,expected):
 text=raw(p).decode();tree=ast.parse(text);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 for name,row in expected.items():
  n=defs[name];assert(n.lineno,n.end_lineno)==(row['start'],row['end'])
  assert hashlib.sha256(ast.get_source_segment(text,n).encode()).hexdigest()==row['sha256']
 return text,tree
def main():
 start=time.monotonic();p=argparse.ArgumentParser();p.add_argument('--app-observation-sha',required=True);args=p.parse_args()
 e=obj(T/'prepare_terminal_return.json',TS)
 assert e['schema']=='AXMAT_ROOT_ACTUAL_COLD_PREPARE_RETURN_V1'
 assert e['record_producer']=='root'and e['actual_tool_terminal_return_observed']is e['record_written_after_actual_terminal_return']is True
 actual=e['actual_tool_result'];assert actual==dict(initial_chunk_id='1a53dd',session_id=2047,terminal_chunk_id='d7ffa4',exit_code=0)and type(actual['exit_code'])is int
 assert type(e['returncode'])is int and e['returncode']==0 and e['scientific_qualification']is e['transport_started']is False
 app=obj(R/'Root_actual_V9_cold_prepare_app_command_execution.json',args.app_observation_sha)
 assert app['prior_genuine_Root_tool_result']==dict(actual,closed=True)
 item=app['actual_app_command_execution']['item'];assert item['status']=='completed'and type(item['exitCode'])is int and item['exitCode']==0 and item['durationMs']==203361
 assert app['actual_execve_syscall_argv_trace']is None and app['source_derived_execve_argv_is_not_separate_syscall_observation']is True
 assert e['source']=={'path':str(F),'sha256':FS}and e['prepared']=={'path':str(O/'prepared.json'),'sha256':PS}
 root=obj(R/'Root_actual_V9_cold_prepare_tool_return.json','c1e24c926bb6aedd909f641717b3a4ec60970ec418aa3f3dfa023b696dd18f16')
 assert root['actual_tool_result']==dict(actual,closed=True)and root['actual_success_recorder_tool']==dict(chunk_id='15dda0',exit_code=0,closed=True)
 assert root['prepared']==e['prepared']and root['prepare_terminal']['sha256']==TS
 for row in root['copied_pure_Root_provenance']:raw(row['path'],row['sha256'])
 provenance=R/'cold_v9_actual_PREP_postterminal_provenance'
 cfg_before=obj(provenance/'Root_phase_config_before_actual_prepare_recording.json');cfg_after=obj(provenance/'Root_phase_config.json');cfg_restored=copy.deepcopy(cfg_after)
 cfg_restored['status']=cfg_before['status'];cfg_restored['future_values']['prepared_sha256']=cfg_before['future_values']['prepared_sha256'];cfg_restored['observations']['prepare']=cfg_before['observations']['prepare']
 assert typed(cfg_restored,cfg_before)and cfg_after['future_values']['prepared_sha256']==PS and cfg_after['observations']['prepare']['actual_tool_result']==actual
 assert cfg_after['observations']['prepare']['tool_closed']is True and all(cfg_after['future_values'][k]is None for k in('binding_sha256','control_seal_sha256','control_terminal_sha256','prepared_cold_sha256'))
 prior=obj(R/'Root_actual_full_V9_cold_DECLARE_independent_admission.json','8e70bb2130f827dd22d97fdd7f21890ffe1addfb91891763647f2d2222470df8')
 assert prior['whole_scope_complementary_reports_pass']is True and prior['actual_prepare_tool']is None
 bundle={}
 for row in prior['preserved_complete_review_bundles']:
  raw(row['durable'],row['sha256']);bundle[Path(row['source']).name]=row['durable']
 # Exact durable source report is addressed via preserved row, not guessed folder.
 source_row=next(row for row in prior['preserved_complete_review_bundles']if row['sha256']=='a469254569903ab9fe2869c8fd34f28b890897346f85a3f5a98e44a7b2b01ad5')
 full=obj(source_row['durable'],source_row['sha256']);assert full['status']=='PASS_ACTUAL_DECLARE_SOURCE_ENVIRONMENT_PARENT_METADATA_SCOPE'
 assert len(full['all_fresh_pins'])==1919
 for row in full['all_fresh_pins']:
  assert ident(row['path'])==row['identity'],(row['path'],'prior DECLARE immutable identity changed')
  raw(row['path'],row['sha256'],False)
 decl=obj(S/'declaration.json',DS);seal=obj(S/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
 source={name:raw(S/name,sha)for name,sha in seal['files'].items()}
 assert len(source)==30 and set(namespace(S)[0])==set(source)|{'factory_seal.json'}and namespace(S)[1]==[]
 eq=json.loads(source['source_equivalence.json']);env=json.loads(source['analysis_environment.json']);spec=json.loads(source['case_spec.json']);admission=json.loads(source['rank1_factor_cache_admission.json'])
 plan=obj('/private/tmp/spot_v9_cold_PREP_actual_review_scope_preparation_20261009/PREP_postterminal_review_scope_plan.json','b49cdaa2c2c295653240cea2212299e2ca988a007f446ba45344a2e0e6728fd1')
 ftext,ft=segment_pins(F,plan['factory_function_pins']);ctext,ct=segment_pins(S/'production_runner.py',plan['controller_function_pins'])
 for n in ft.body:
  if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in('FORMAL_FACTORY_SHA','BINDING_CONTROLS_ACTUAL'):assert ast.literal_eval(n.value)is None
 generated_inverse=[]
 for name in('production_runner.py','qualified_snapshot_ingestion.py','numerical_layout_admission.py'):
  proof=eq['patches'][name];original=raw(BASE/'runtime'/name,proof['original_sha256']).decode();recovered=source[name].decode()
  for before,after in reversed(proof['replacements']):assert recovered.count(after)==1;recovered=recovered.replace(after,before,1)
  assert recovered==original;generated_inverse.append(name)
 for name,row in eq['unchanged_files'].items():assert source[name]==raw(row['parent']['path'],row['parent']['sha256'])
 assert len(eq['unchanged_files'])==7
 info=obj(O/'prepared.json',PS);assert info['classification']=='PREPARED_NO_TRANSPORT'and info['cases']==['AAA','ABA']and 'own_child_supervision'not in info
 stdout=raw(e['full_stdout']['path'],e['full_stdout']['sha256']);stderr=raw(e['full_stderr']['path'],e['full_stderr']['sha256'])
 assert len(stdout)==365 and stderr==b''and typed(json.loads(stdout),sorted_boundary({'prepared':str(O/'prepared.json'),'sha256':PS,'classification':'PREPARED_NO_TRANSPORT'}))
 assert stdout==raw('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/prepare.stdout',e['full_stdout']['sha256'])
 assert stderr==raw('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/prepare.stderr',e['full_stderr']['sha256'])
 assert e['input_declaration_terminal_evidence']=={'path':str(T/'declaration_terminal_return.json'),'sha256':DTS};obj(T/'declaration_terminal_return.json',DTS)
 expected_cli=[env['executable'],str(F),'prepare','--factory-sha256',FS,'--sha256',DS,'--declaration-terminal-sha256',DTS]
 assert e['command']==expected_cli
 assert root['launch_command']==expected_cli and root['full_stdout']==e['full_stdout']and root['full_stderr']==e['full_stderr']
 command=shlex.split(item['command']);assert command[0:2]==['/bin/zsh','-lc'];shell=shlex.split(command[2]);assert shell[0:3]==['env','-u','PYTHONOPTIMIZE']
 idx=shell.index(env['executable']);assert shell[idx:idx+9]==expected_cli
 envvalues=dict(x.split('=',1)for x in shell[3:idx]);threads=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']
 assert all(envvalues[k]=='1'for k in threads)and envvalues['PYTHONDONTWRITEBYTECODE']=='1'and envvalues['AXMAT_COLD_FACTORY_SHA256']==FS
 assert envvalues['PYTHONPATH']==str(B/'axial-material-cold-cp314-scipy-dependency-20261008/target')
 assert shell[idx+9:]==['>','/private/tmp/axmat-v9-cold-root-actual-execution-20261009/prepare.stdout','2>','/private/tmp/axmat-v9-cold-root-actual-execution-20261009/prepare.stderr']
 expression='c=f.normal_runtime_preload(f.SOURCE); r=c.prepare(f.SOURCE/"declaration.json",'+repr(DS)+',f.OUTPUT); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
 program=('import hashlib,sys,os; from pathlib import Path\n'+'if sys.flags.optimize!=0 or "PYTHONOPTIMIZE" in os.environ: raise ValueError("nonoptimized cold source predicates required")\n'+'sys.dont_write_bytecode=True; '+'p=Path('+repr(str(F))+'); assert hashlib.sha256(p.read_bytes()).hexdigest()=='+repr(FS)+'; '+'sys.path.insert(0,str(p.parent)); import '+F.stem+' as f; '+'assert Path(f.__file__).resolve()==p; '+expression)
 assert root['source_derived_handoff_command']==[env['executable'],'-c',program]and root['actual_execve_syscall_argv_trace']is None
 assert typed(info['inputs'],sorted_boundary(decl['inputs']))and typed(info['production_config'],sorted_boundary(decl['production_config']))and typed(info['budgets'],sorted_boundary(decl['budgets']))
 assert typed(info['budgets'],sorted_boundary(plan['original_budgets']))and info['schema_version']==1 and info['experiment_id']==decl['experiment_id']and info['artifact_root']==str(B)
 assert typed(info['resource_roots'],decl['resource_roots'])
 for key in('case_spec','rank_addendum'):assert typed(info[key],sorted_boundary(decl[key]));obj(info[key]['path'],info[key]['sha256'])
 assert typed(info['declaration'],sorted_boundary({'path':str(S/'declaration.json'),'sha256':DS}))and raw(O/'declaration.json',DS)==source['declaration.json']
 assert len(info['inputs'])==8 and info['inputs']['radial_track_A']['sha256']==info['inputs']['radial_track_B']['sha256']and info['inputs']['snapshot_A']['sha256']!=info['inputs']['snapshot_B']['sha256']
 expected={}
 for name,row in info['runtime_sources'].items():expected['runtime/'+name]=row['sha256'];assert raw(O/'runtime'/name,row['sha256'])==raw(row['path'],row['sha256'])
 for name in('production_runner.py','production_inputs.py','snapshot_control_preflight.py','conditional_white_receiver_variant.json','white_receiver_tracking.py','numerical_layout_admission.py','rank1_factor_cache_admission.py','rank1_factor_cache_admission.json','combined_cold_own_rss_host.py','combined_cold_own_rss_controls.py','combined_cold_file_snapshot_decks.py','cold_component_input_consumer_last_cprime_trim_own_pid_peak.py','physical_common_basis_admission.py','qualified_snapshot_ingestion.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py','check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
  expected['runtime/'+name]=seal['files'][name];assert raw(O/'runtime'/name,seal['files'][name])==source[name]
 assert len(info['runtime_sources'])==13 and len(expected)==31
 assert all(info['local_files'][k]==v for k,v in expected.items())and len(info['local_files'])==43
 files,dirs=namespace(O);assert set(files)==set(info['local_files'])|{'prepared.json'}and dirs==['decks','runtime']
 for name,sha in info['local_files'].items():assert not Path(name).is_absolute()and '..'not in Path(name).parts;raw(O/name,sha)
 manifest=obj(O/'decks/production_inputs.json');proof=obj(O/'decks/deferred_snapshot_inverse.json');assert typed(manifest['runner_deferred_snapshot_inputs'],proof)
 assert typed(manifest['config'],info['production_config'])and manifest['case_slots']=={'AAA':['A','A','A'],'ABA':['A','B','A']}and manifest['training_slots']==['A','B','A']
 assert manifest['required_dimensions']=={'fission_components':32,'groups':370,'regions':8,'snapshots':3}and manifest['classification']=='PREPARED_INPUTS_ONLY_NO_TRANSPORT'
 deck_originals={}
 for name,row in proof['independent_deck_inverses'].items():
  recovered=raw(O/'decks'/name,row['candidate_file_snapshot_sha256'])
  for inv in row['inverse_operations']:assert recovered.count(inv['remove'].encode())==1;recovered=recovered.replace(inv['remove'].encode(),inv['restore'].encode(),1)
  assert hashlib.sha256(recovered).hexdigest()==row['original_sha256']and recovered==raw(BASE/'decks'/name,row['original_sha256'])
  assert row['all_scientific_statements_in_original_order_byte_exact']is row['whole_deck_inverse_byte_exact']is row['storage_medium_inverse_byte_exact']is True
  assert row['actual_native_RSS_under_512MiB_proved']is row['bootstrap_or_map_solve_executed']is row['predicted_RSS_saving_claimed']is row['prior_failed_peak_cause_claimed']is False
  deck_originals[name]=row['original_sha256']
 assert set(deck_originals)=={'bootstrap_axial.x2m','picard_axial.x2m'}
 for name in('bootstrap_radial.x2m','case_setup.x2m','checker_parent.x2m','common_basis.x2m','pack_archives.x2m','picard_radial.x2m','rank_precision.x2m'):assert raw(O/'decks'/name)==raw(BASE/'decks'/name)
 for name,sha in manifest['deck_sha256'].items():raw(O/'decks'/name,sha)
 base=obj(BASE/'prepared.json','7d2154e9c722eab23f4411c9a8588ed8250da658ae880298c24dfb53308656b5')
 runtime_inverse=copy.deepcopy(info['runtime_sources']);runtime_inverse['Dragon']=base['runtime_sources']['Dragon'];assert typed(runtime_inverse,base['runtime_sources'])
 assert set(info)=={'artifact_root','budgets','case_spec','cases','classification','declaration','experiment_id','inputs','local_files','preflight_resources','producer_admission','production_config','rank_addendum','resource_roots','runtime_sources','schema_version','snapshot_control_audits'}
 base_manifest=obj(BASE/'decks/production_inputs.json',base['local_files']['decks/production_inputs.json']);restored=copy.deepcopy(manifest);del restored['runner_deferred_snapshot_inputs']
 for name,sha in deck_originals.items():restored['deck_sha256'][name]=sha
 assert typed(restored,base_manifest)
 for key in('production_config','budgets','snapshot_control_audits'):assert typed(info[key],base[key])
 producer=copy.deepcopy(info['producer_admission']);assert producer['online_receiver_sha256']==info['runtime_sources']['Dragon']['sha256'];producer['online_receiver_sha256']=base['producer_admission']['online_receiver_sha256'];assert typed(producer,base['producer_admission'])
 assert info['producer_admission']['coupled_qualified']is info['producer_admission']['offline_r64_directly_consumed_by_boot']is False
 recipe=obj(admission['reference_analysis_recipe']['path'],admission['reference_analysis_recipe']['sha256']);assert recipe['fixed_history']=={'inactive_batches':100,'active_batches':2000,'particles_per_generation':10000,'generations_per_batch':10,'first_active':101,'last_active':2100,'raw_generation_entries':21000,'batched_generation_entries':2100}
 assert recipe['original_eight_checks']==['input_equivalence','source_convergence','block_stability','statistical_resolution','keff','scalar_flux','nu_fission','currents_balance_symmetry']and recipe['AAA_accuracy_qualified']is recipe['ABA_admitted']is recipe['analysis_executed']is recipe['new_transport_launched']is False
 assert spec['reference']['active_batches']==250
 caps=spec['resource_caps'];assert(caps['new_case_artifact_budget_GiB'],caps['disk_min_free_GiB'],caps['new_child_threads'],caps['new_numeric_children_at_once'],caps['automatic_retries_after_solver_failure'])==(96,8,1,1,0)
 resource=info['preflight_resources'];assert resource['artifact_budget_bytes']==96*2**30 and resource['min_free_bytes']==8*2**30 and resource['artifact_bytes']<=resource['artifact_budget_bytes']and resource['disk_free_bytes']>=resource['min_free_bytes']
 assert resource['declared_resource_roots']==info['resource_roots']and resource['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
 assert proof['actual_bootstrap_RSS_or_mathematical_output_credit']is proof['scientific_qualification']is proof['AAA_accuracy_qualified']is proof['ABA_admitted']is False
 assert proof['actual_cfb_map012_capture_credit_not_inherited']is proof['actual_file_snapshot_map012_capture_credit_not_inherited']is True
 assert not os.path.lexists(C)and all(not os.path.lexists(O/name)for name in('own_rss_binding.json','prepared_cold.json','prepare_failure.json','AAA','ABA'))
 assert all(ident(row['path'])==row['identity']for row in PINS.values())
 report={'status':'PASS','scope':'ACTUAL_PREP_COMPLETE_SOURCE_LOCAL_DECK_METADATA_WITNESS_SCOPE; needs complementary graph/resource report for full joint admission','actual_PREP_tool':dict(actual,closed=True),'Root_observer_sha256':'c1e24c926bb6aedd909f641717b3a4ec60970ec418aa3f3dfa023b696dd18f16','prepare_terminal_sha256':TS,'prepared_sha256':PS,'actual_app_duration_seconds':item['durationMs']/1000,'source31_exact_fullSHA_namespace':True,'inherited_complete_DECLARE_source_environment_freshSHA_and_identity_pins':1919,'inherited_original430_plus_SciPy1424_and_expanded_environment1860_whole_source_evidence_unchanged':True,'generated3_whole_source_byte_inverses_rechecked':generated_inverse,'original7_UNCHANGED_sources_fresh_exact':True,'complete43_local_files_and_all31_runtime_copies_fullSHA':True,'complete_prepared_all_fields_checked':True,'complete2_axial_decks_inverse_to_original_bytes':deck_originals,'all7_other_deck_bytes_unchanged':True,'whole_production_inputs_manifest_inverse_to_original_base_typed_order_floatbits':True,'complete_original_AB_inputs_config_budget_parent_snapshot_control_outputs_preserved':True,'whole_original_producer_admission_inverse_only_current_receiver_SHA':True,'complete_independent_reference2000_and_original8_checks_retained_as_dependency_only':True,'reference_policy_boundary':{'unchanged_legacy_case_spec_active_batches':250,'legacy_250_spec_not_promoted_to_accuracy_qualification':True,'separate_frozen_recipe_fixed_history_active_batches':2000,'first_active_statepoint':101,'last_active_statepoint':2100,'original_all8_checks_required':recipe['original_eight_checks'],'recipe_admitted_new_science_or_reference_result':False,'source_recipe_path':admission['reference_analysis_recipe']['path'],'source_recipe_sha256':admission['reference_analysis_recipe']['sha256']},'original_physics_dtype_layout_trace_bytefresh_gates_inherited_by_same_source_bytes':True,'external_original9token_cli_exact':expected_cli,'source_derived_normal_execve_three_arguments':[env['executable'],'-c',program],'actual_execve_syscall_argv_observation':None,'actual_preflight_resources':resource,'dynamic_resource_and_canonical_metadata_scope':'peer complementary independent PREP scope pending; original full35GB from DECLARE31f29c only','original_DECLARE_admission_sha256':'8e70bb2130f827dd22d97fdd7f21890ffe1addfb91891763647f2d2222470df8','full35GB_numeric_canonical_bytes_reread':False,'new_controls_bound':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'scientific_qualification':False,'source_FUNCTION_PLAN12_segments_all_same':True,'all_fresh_pins':list(PINS.values()),'distinct_fullSHA_pins':len(PINS),'fullbytes_read_including_repeats':READ_BYTES,'readonly_review_elapsed_seconds':time.monotonic()-start,'only_TMP_written':True,'business_factory_consumer_controller_helper_API_constructor_PREP_RUN_native_executed':False,'limits':['This is preparation/admission evidence only; original preflight control outputs were independently compared to immutable prior full records, not recomputed by business readers.','Original numerical/graph fullbyte credit comes from completed DECLARE evidence with complementary fresh metadata identity checks, not a new35GB read.','Source-derived internal execve argv is not a captured syscall trace.','No own-child RSS, fresh training/bootstrap/maps, native science, AAA accuracy or ABA qualification credited.']}
 with (H/'REPORT.json').open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
 print(json.dumps({'status':report['status'],'report_path':str(H/'REPORT.json'),'report_sha256':hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),'distinct_fullSHA_pins':len(PINS),'bytes_read':READ_BYTES,'43local_fullSHA':True,'no_business':True}))
if __name__=='__main__':main()

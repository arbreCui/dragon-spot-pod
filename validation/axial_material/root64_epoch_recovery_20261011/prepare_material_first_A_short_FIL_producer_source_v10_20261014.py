"""Source-only short physical filenames for the unchanged original A producer."""
import ast,copy,importlib.util,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
sp=importlib.util.spec_from_file_location('bounded_metadata',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
pin,read,write,identity=h.pin,h.read,h.write,h.identity
OLD=R/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
OUT=R/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
ART=Path('/Users/wen/spot/validation/artifacts')
def main():
 if OUT.exists():raise RuntimeError('one new short-FIL Source package')
 src=OLD/'produce_current_formal_material_observations.py';original=src.read_text();current=original;changes=[]
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('one exact original Source splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 tree=ast.parse(current);n=next(n for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='SHARED_INPUT_LIBRARY_LAYOUT');layout=ast.literal_eval(n.value);newlayout=copy.deepcopy(layout)
 newlayout['shared_directory']='s';newlayout['physical_file_names']={'DLIB_ACTUAL':'A','DLIB8R1_370':'B'}
 newlayout['literal_replacements'][0]['derived']="FIL: '../s/A'";newlayout['literal_replacements'][1]['derived']="FIL: '../s/B'"
 change(ast.get_source_segment(current,n),'SHARED_INPUT_LIBRARY_LAYOUT='+repr(newlayout))
 change('recheck(p,budget);dest=shared/name',"recheck(p,budget);dest=shared/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name]")
 change('len(new.split(b"\'")[1])<=64', 'len(new.split(b"\'")[1])<=12')
 change('all and only original FIL literal occurrences fit actual NAMFIL64','all and only original FIL literal occurrences fit actual LIBLIC and LIBSUB NAMFIL(:12)')
 change("folder/('../shared_input_libraries/'+name)","folder/('../s/'+SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name])")
 change("directory==out/'shared_input_libraries'", "directory==out/'s'")
 change("Path(p['path'])==directory/name", "Path(p['path'])==directory/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name]")
 ast.parse(current);back=current
 for c in reversed(changes):
  if back.count(c['after'])!=1:raise RuntimeError('unique complete Source inverse')
  back=back.replace(c['after'],c['before'],1)
 if back.encode()!=src.read_bytes():raise RuntimeError('whole producer source inverse')
 funcs=lambda text:{n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
 a,z=funcs(original),funcs(current);unchanged=[k for k in a if a[k]==z[k]]
 if set(a)!=set(z)or set(a)-set(unchanged)!={'prepare_shared_libraries','derive_original_procedure','copy_state_seeds','release_closed_owned_library_copies'}:raise RuntimeError('only four original path consumers changed; main/math/capture unchanged')
 seedpath=OLD/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json';seed=read(seedpath)
 if seed['material_input_layout']!=layout:raise RuntimeError('original complete seed layout')
 newseed=copy.deepcopy(seed);newseed['material_input_layout']=newlayout
 cli=read(OLD/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json');hf=read(OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json')
 oldargv=read(R/'ROOT_EXACT_FIRST_A_MATERIAL_AFTER_OBSERVER75_V9_ACTUAL_ARGV_20261014.json');failedraw=pin(R/'ROOT_ACTUAL_FIRST_A_MATERIAL_AFTER_OBSERVER75_V9_TRUE_TOOL_RETURNS_20261014.json');failed=read(failedraw)
 if oldargv['exact_argv']!=cli['exact_argv']or failed['observed_closed']is not True or type(failed['original_integer_exit_code'])is not int or failed['original_integer_exit_code']!=1:raise RuntimeError('exact closed failed original A attempt kept')
 failedout=Path(oldargv['exact_argv'][-1]);phase=pin(failedout/'Root_actual_material_observation_execution_summary.json');d=read(phase)
 if d['schema']!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or d['status']!='FAILED_CURRENT_OBSERVATION_NO_RETRY'or len(d['records'])!=1 or d['records'][0]['status']!='FAILED'or d['actual_full_A_observation_executed']is not False or d['actual_B_observation_executed']is not False:raise RuntimeError('real failed A unqualified')
 copies={p['path']:p for p in d['owned_input_copy_pins']if str(failedout/'shared_input_libraries')+'/'in p['path']}
 if len(copies)!=2 or sum(p['size_bytes']for p in copies.values())!=979740136 or d['actual_closed_owned_library_copy_release_pin']is not None:raise RuntimeError('only two full failed private library copies retained; no release qualification')
 sources=[pin(src),pin(seedpath),pin(OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'),pin(OLD/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json'),pin(R/'ROOT_EXACT_FIRST_A_MATERIAL_AFTER_OBSERVER75_V9_ACTUAL_ARGV_20261014.json'),failedraw,phase]
 OUT.mkdir();producer=write(OUT/src.name,current);helper=write(OUT/'current_material_prerequisite_admission.py',(OLD/'current_material_prerequisite_admission.py').read_bytes());newseedpin=write(OUT/seedpath.name,newseed)
 inv=write(OUT/'COMPLETE_V9_TO_V10_SHORT_FIL_PRODUCER_AND_SEED_BYTE_INVERSE.json',dict(schema='COMPLETE_V9_TO_V10_SHORT_FIL_PRODUCER_AND_SEED_BYTE_INVERSE_V1',source_only=True,producer_predecessor_pin=pin(src),producer_candidate_pin=producer,producer_changes=changes,whole_producer_inverse_equal=True,unchanged_function_bytes=unchanged,helper_predecessor_pin=pin(OLD/'current_material_prerequisite_admission.py'),helper_candidate_pin=helper,helper_whole_bytes_equal=True,seed_predecessor_pin=pin(seedpath),seed_candidate_pin=newseedpin,seed_only_material_input_layout_replaced=dict(before=layout,after=newlayout),all_seed_scientific_rows_original_bytes_and_values_unchanged=True))
 pp=write(OUT/'SHORT_FIL_FIRST_A_PRODUCER_SOURCE_PLAN.json',dict(schema='SHORT_FIL_FIRST_A_PRODUCER_SOURCE_PLAN_V1',source_only=True,producer_source_pin=producer,helper_source_pin=helper,seed_plan_pin=newseedpin,inverse_pin=inv,predecessor_Producer_HF_pin=pin(OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'),predecessor_actual32_CLI_pin=pin(OLD/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json'),actual_build75_report_pin=cli['actual_observer75_report_pin'],actual_build75_Root_pin=cli['actual_observer75_Root_true_tool_pin'],actual_build75_Root_argv_pin=cli['actual_observer75_Root_argv_pin'],actual_build75_post_pin=cli['actual_observer75_independent_post_pin'],actual_build75_post_tool_pin=cli['actual_observer75_independent_post_tool_pin'],original_material_four_function_path_consumers_only=True,original_main_capture_maths_conditions_and_limits_unchanged=True,literal_paths=['../s/A','../s/B'],maximum_literal_filename_length=12,actual_consuming_LIBLIC_or_LIBSUB_branch_unknown=True,logical_library_role_order=['DLIB_ACTUAL','DLIB8R1_370'],ordinary_distinct_copy_files_no_symlink_or_hardlink=True,failed_v9_original_report_pin=phase,failed_v9_original_Root_tools_pin=failedraw,failed_v9_original_Root_argv_pin=pin(R/'ROOT_EXACT_FIRST_A_MATERIAL_AFTER_OBSERVER75_V9_ACTUAL_ARGV_20261014.json'),failed_private_two_copy_historical_candidates=list(copies.values()),failed_copy_current_role_not_promoted_in_new_HF=True,future_failed_v9_post_pin=None,future_failed_v9_copy_release_receipt_pin=None,future_actual_v10_first_A_report_pin=None,future_actual_v10_observation_manifest_pin=None,future_actual_v10_979740136_release_pin=None,future_actual_evidence_or_GENDF_pin=None,original_runtime_budget_gate_required=True,compiler_executed=False,business_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False))
 ready=write(OUT/'READY.json',dict(schema='SHORT_FIL_FIRST_A_PRODUCER_SOURCE_READY_V1',source_only=True,status='SOURCE_ONLY_READY_FOR_SAME_ROUND_CANDIDATE_WRITER_REVIEW',producer_source_pin=producer,helper_source_pin=helper,seed_plan_pin=newseedpin,inverse_pin=inv,plan_pin=pp,preparer_pin=pin(__file__),Source_pins=sources,future_actual_runtime_HF_pin=None,future_actual_CLI_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 print(json.dumps(dict(status='SHORT_FIL_FIRST_A_V10_SOURCE_ONLY_READY',producer_source_pin=producer,helper_source_pin=helper,seed_plan_pin=newseedpin,inverse_pin=inv,plan_pin=pp,ready_pin=ready,preparer_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

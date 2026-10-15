"""Prepare two finite independent candidates; never calls unlink or a child."""
import ast,json,os
from pathlib import Path
import time
import release_source_common as s
c=s.c

def main():
 for p in s.PACKAGE.glob('*.py'):ast.parse(p.read_bytes())
 source=[c.pin(p)for p in sorted(s.PACKAGE.glob('*.py'))]+[c.pin(s.PRIOR),c.pin(Path(c.__file__)),c.pin(Path(s.previous.b.__file__)),c.pin(s.previous.b.LIBRARY)]
 protected,provenance=s.protect();material_before=provenance['current_material_v4_plan_pin']
 formal=c.read_pinned_json(c.pin(s.REC/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json'))
 originals={}
 for i,row in enumerate(formal['producers'],1):originals['native_A'+str(i)+'.xsm']=row['archive']
 for name,original in [('axial_macro.xsm','initial_axial_macrolib.xsm'),('axial_track.xsm','initial_axial_track.xsm'),('basis.xsm','basis_reference.xsm'),('global_rcon.xsm','route_contract.xsm')]:originals[name]=next(r for r in formal['formal_inputs']if Path(r['path']).name==original)
 summaries=[]
 for name,b in s.BATCHES.items():
  target_manifest=s.PACKAGE/b['manifest']
  if target_manifest.exists():raise RuntimeError('immutable candidate manifest already exists; no overwrite')
  proof=s.proof(name);before=s.inventory(b['branch']);targets=[c.pin(p)for p in b['targets']]
  if len(targets)!=b['count']or sum(p['size_bytes']for p in targets)!=b['bytes']:raise RuntimeError('literal finite target shape/bytes changed')
  s.disjoint(targets,protected);names={p['path']for p in targets};retained=[c.pin(p)for p in sorted(before['ordinary_file_identities'])if p not in names]
  if s.inventory(b['branch'])!=before:raise RuntimeError('closed branch changed during readonly audit')
  original_provenance=[]
  if name=='failed-v3-seven':
   for row in targets:
    original=originals[Path(row['path']).name];c.same(original)
    if original['sha256']!=row['sha256']or original['size_bytes']!=row['size_bytes']or original['identity'][:2]==row['identity'][:2]:raise RuntimeError('complete independent failed owned copy only')
    original_provenance.append(dict(candidate_pin=row,retained_original_pin=original))
   badpin=provenance['invalid_v3_PACK_explicit_full_pin_retained']
   if not any(r==badpin for r in retained):raise RuntimeError('invalid original PACK must remain exact causal raw evidence')
  # These are ordinary files and metadata observations. No resource program or
  # compiler/numerical child is run in this preparation; Root execution uses
  # original actual budget before/after and decides whether either is needed.
  for row in targets+retained+protected+source:c.same(row)
  current_material=c.pin(s.REC/'current_formal_material_authority_source_v1/CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_PLAN_V4.json')
  if current_material!=material_before:raise RuntimeError('actual selected material v4 plan changed before/after preparation')
  m=dict(schema='ROOT_REVIEWABLE_INDEPENDENT_EXACT_STORAGE_BATCH_SOURCE_MANIFEST_V1',batch=name,created_unix=time.time(),action_executed=False,unlink_executed=False,target_count=b['count'],total_target_logical_bytes=b['bytes'],target_full_EOF_pins=targets,retained_ordinary_full_EOF_pins=retained,complete_before_inventory=before,current_protected_full_EOF_pins=protected,Source_DAG_provenance=provenance,Source_pins=source,closed_branch_proof=proof,original_copied_input_provenance=original_provenance,material_selected_plan_before_and_after_pin=material_before,default_execution_is_readonly=True,exact_batch_independent_selection_required=True,original_guards_and_caps_unchanged=True,APFS_parent_metadata_expectations=dict(ordinary_entry_count_decrease_per_unlink=1,directory_size_byte_decrease_per_unlink=32,device_inode_mode_preserved=True,mtime_ctime_natural_changes_only=True),retention_scope='All other files, results/logs/Source/original producers retained. v3 initial_pack remains immutable current SF2 causal evidence. Optional map003/004 raws are from completed12 WAITING_REFERENCE, and map005..012/bootstrap/training remain.',historical_raw_replay_loss_scope='Only the exact chosen finite batch raw files if Root later explicitly executes. No current input or physical result is removed.',scientific_computation_started=False,pipeline_or_physics_qualification_created=False,goal_complete=False)
  c.write_new(target_manifest,m)
  review=dict(schema='FINITE_READONLY_EXACT_STORAGE_CANDIDATE_SOURCE_REVIEW_V1',status='FULL_EOF_CANDIDATE_AND_RETAINED_CURRENT_DAG_VERIFIED_NO_DELETE',batch=name,manifest_pin=c.pin(target_manifest),target_count=b['count'],target_bytes=b['bytes'],retained_branch_ordinary_files=len(retained),retained_symlink_entries=len(before['symlinks']),current_protected_full_EOF_count=len(protected),candidate_Source_reference_or_path_or_physical_inode_intersection=False,entire_Source_copy_field_and_relative_dynamic_file_construction_reviewed=True,actual_current69v4_and_pipeline4_andSF2_and_material_v4_and_all1129_science_protected=True,invalid_v3_PACK_retained=True,original_history_budget_resource_API_called=False,original_SELF_RSS_and_elapsed_guards_preserved=True,compiler_or_numerical_or_delete_child_started=False,all_source_files_AST_read=True,self_review_scope='Finite Source producer/preparation audit; independent Root review and explicit Root-selected manifest required before any deletion.',goal_complete=False)
  review_file=s.PACKAGE/(name+'_SOURCE_REVIEW.json');c.write_new(review_file,review)
  summaries.append(dict(batch=name,manifest_pin=review['manifest_pin'],review_pin=c.pin(review_file),target_count=b['count'],target_bytes=b['bytes'],retained_files=len(retained),protected_files=len(protected)))
 for row in protected+source:c.same(row)
 if c.pin(material_before['path'])!=material_before:raise RuntimeError('material selected v4 plan changed at final EOF')
 print(json.dumps(dict(status='TWO_INDEPENDENT_FINITE_CANDIDATE_PACKAGES_PREPARED_NO_DELETE',batches=summaries,numerical_or_delete_child_executed=False),indent=2))
if __name__=='__main__':main()

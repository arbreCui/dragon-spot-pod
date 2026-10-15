import ast
import hashlib
import json
import os
import stat
from pathlib import Path
B=Path('/private/tmp/spot_storage_thirteenth_current_dependency_exact_runtime_review_20261009')
ROOT=Path('/Users/wen/spot');V=ROOT/'validation'
F=V/'axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
R=V/'axial_material/prepare_qualified_AB_moment_order_production.py'
INV=Path('/private/tmp/spot_storage_recheck_20261009_root13/full_metadata_inventory.jsonl')
PINS={}
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,sha=None):
 p=Path(p);before=ident(p);assert stat.S_ISREG(before[2])and p.parent.resolve(strict=True)==p.parent
 h=hashlib.sha256()
 with p.open('rb')as f:
  while b:=f.read(4*1024**2):h.update(b)
 assert ident(p)==before
 result=dict(path=str(p),sha256=h.hexdigest(),size=before[3],identity=before)
 if sha is not None:assert result['sha256']==sha
 PINS[str(p)]=result;return result
basepin=pin(B/'REPORT.json','e8144d7b6d23f1c3901370f66209a3c781cbac37ecc01a6c742c926c8bccc9e5')
b=json.loads((B/'REPORT.json').read_text());assert b['status']=='PASS'and b['exact_selected_count']==2
candidatepin=pin(B/'exact2_runtime_candidates.json');candidate=json.loads((B/'exact2_runtime_candidates.json').read_text());assert len(candidate['candidates'])==2
sourceproofpin=pin(B/'current_actual_source_readchain_proof.json');firstproof=json.loads((B/'current_actual_source_readchain_proof.json').read_text());assert firstproof['status']=='PASS_READONLY_SOURCE_ONLY'
fp=pin(F,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46');rp=pin(R,'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41');ip=pin(INV,b['root_inventory']['sha256'])
fs=F.read_text();ft=ast.parse(fs);rs=R.read_text();rt=ast.parse(rs)
def function(tree,text,path,name):
 nodes=[n for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name];assert len(nodes)==1
 n=nodes[0];value=ast.get_source_segment(text,n)
 return dict(source=PINS[str(path)],definition=name,start_line=n.lineno,end_line=n.end_lineno,exact_definition=value,whole_definition_sha256=hashlib.sha256(value.encode()).hexdigest())
functions=[function(ft,fs,F,name)for name in ('production_admission','external_terminal','declaration_admission','prepare_terminal_admission','actual_components','archive_bytes','environment','verify_inventory','expected_supervisor_constructor')]
functions.append(function(rt,rs,R,'check'))
by={p['definition']:p['exact_definition']for p in functions}
assert "size!=archive_bytes()"in by['external_terminal']
assert "snapshot!=d['source_inventory']"in by['prepare_terminal_admission'] and 'verify_inventory(SOURCE,snapshot)'in by['prepare_terminal_admission']
assert "complete_archive_scope_roots']!=[str(SOURCE),str(OUT)]"in by['declaration_admission']
assert 'complete_input_phase' not in by['external_terminal']
assert "g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA)" in by['actual_components'] and "Historical whole INPUT return, not any original API invocation now." in by['actual_components']
assert 'resources_for(d[\'resource_roots\']).check()'in by['production_admission']
assert 'total > self.max_bytes' in by['check'] and 'snapshot["disk_free_bytes"] < self.min_free_bytes'in by['check']
assert 'item.st_size'in by['check'] and 'entry.stat(follow_symlinks=False)'in by['check']
assert 'read('not in by['check'] and 'digest('not in by['check'] and 'seal'not in by['check'].lower()
# Determine actual paths solely from the frozen source constants/config and
# verify both old targets are outside current SOURCE9/OUT9 archive scope.
cfg=json.loads(Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009/config.json').read_text())
for row in candidate['candidates']:
 assert not Path(row['path']).is_relative_to(Path(cfg['SOURCE']))and not Path(row['path']).is_relative_to(Path(cfg['OUT']))
 fresh=pin(row['path'],row['sha256']);assert fresh['identity']==row['identity']and fresh['size']==row['size']
 primary=pin(row['retained_primary'],row['sha256']);assert primary['identity']==row['retained_primary_pin']['identity']and primary['size']==row['size']
# Initial report used the unsupported label regular for Root's type=file.
# Keep it immutable and transparently correct only the ancillary R9 allocation.
r9=V/'storage_cleanup_ninth_20261009';byinode={};logical=0;files=0
with INV.open()as f:
 for line in f:
  row=json.loads(line);p=Path(row['path'])if row['path'].startswith('/')else ROOT/row['path']
  if row['type']=='file'and p.is_relative_to(r9):
   logical+=row['size'];files+=1;byinode[(row['dev'],row['ino'])]=row['allocated']
assert files>0 and sum(byinode.values())>2*1024**3
supp=dict(schema='SPOT_EXACT2_RUNTIME_EXTERNAL_PREP_HISTORICAL_AND_FRESH_RESOURCE_TAIL_SOURCE_SUPPLEMENT_V1',status='PASS',base_review_pin=basepin,exact_candidate_pin=candidatepin,current_readchain_proof_pin=sourceproofpin,all_typed_true_actual_readonly_source_and_3_full_exe_hashes=True,
 source_clauses=functions,external_terminal_historical_current_RUN_tails_and_SOURCE9_OUT9_archive_bytes_unchanged=True,
 historical_RUN_resource_snapshot_compared_only_to_its_saved_stdout_and_root_tail_not_fresh_resource_snapshot=True,
 fresh_resource_check_only_dynamic_root_set_and_96GiB_free8_caps_not_fixed_old_payload_identity_or_count=True,
 current_declaration_and_PREP_verify_only_currentSOURCE9_and_fixed_originalnormative_INPUT_namespaces_not_oldV7V8RUN_inventory=True,
 actual_components_whole2cad_loaded_without_original_API_calls_no_oldV7V8runtime=True,
 both_targets_outside_current_SOURCE9_OUT9_exactarchive_scope=True,
 R9_initial_report_allocation0_was_ancillary_inventory_type_label_error=dict(original_value=b['R9_total_allocated_from_Root_inventory'],original_label='regular',actual_Root_inventory_label='file',old_report_preserved=True,corrected_regular_files=files,corrected_logical_bytes=logical,corrected_unique_inode_allocated_bytes=sum(byinode.values()),no_candidate_or_dependency_decision_was_based_on_incorrect_value=True),
 no_business_import_API_or_Ctor_or_INPUT_or_PREP_or_RUN=True,formal_ART_write=False,files_deleted=0,science_credit=False,pins=list(PINS.values()))
with (B/'tail_and_R9_allocation_supplement.json').open('x')as f:json.dump(supp,f,indent=2);f.write('\n')
final=dict(schema='SPOT_STORAGE_THIRTEENTH_EXACT2_RUNTIME_FULL_SOURCE_CANDIDATE_FINAL_REVIEW_V1',status='PASS',classification='READONLY_EXACT2_CANDIDATE_PROOF_NOT_DELETE_AUTHORITY',manifest_candidate_count=2,logical_bytes=18451440,allocated_bytes=18456576,unique_inode_allocated_bytes=18456576,
 exact_candidate_pin=candidatepin,full_current_readchain_source_proof_pin=sourceproofpin,base_review_pin=basepin,additional_tail_source_proof_pin=pin(B/'tail_and_R9_allocation_supplement.json'),
 static_complete_current_INPUT_and_oldnormative_source_dependency_exclusion=True,no_current_business_whole_V7_V8_output_inventory_or_expected_filecount_found=True,
 source_observer_dynamic_only_caps_and_fixed_rootset=True,all_original_root_dirs_and_normative_metadata_and_source_remain=True,
 retained_primary=dict(path=candidate['retained_primary']['path'],sha256=candidate['retained_primary']['sha256'],size=candidate['retained_primary']['size']),
 exact_future_Root_restore_required_for_oldpackage_binary_recheck=True,old_sealed_result_metadata_source_logs_full_old_failed_facts_preserved=True,
 bootstrap51_not_selected_current_test_dependency_HOLD=True,permanent89_R9_gzip_and_prior_restore_primaries_HOLD=True,
 every_candidate_and_main_source_fullSHA_identity_current=True,
 next_step='Root fixedmanifest+restorer/source independent audit, then fresh exact preflight and independent PASS before any actual deletion. Only these2 compiledbyte copies; no INPUT/cold execution or whole failed-package deletion.',
 business_import_or_API_or_native_or_INPUT_or_PREP_or_RUN_executed=False,formal_or_ART_write=False,files_deleted=0,science_credit=False)
with (B/'FINAL_REPORT.json').open('x')as f:json.dump(final,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',report=str(B/'FINAL_REPORT.json'),sha256=hashlib.sha256((B/'FINAL_REPORT.json').read_bytes()).hexdigest(),candidate_count=2,logical_bytes=18451440,allocated_bytes=18456576,R9_corrected_allocated_bytes=sum(byinode.values()),business=False)))

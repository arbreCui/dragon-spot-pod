from pathlib import Path
import ast,hashlib,json,os
p=Path('/private/tmp/axmat_saved_source_phase_normal_host_SOURCE_candidate_20261010_rohryp7y')
q=p/'saved_source_phase_diagnostic_host.CANDIDATE.py';b=q.read_bytes();sha=hashlib.sha256(b).hexdigest();assert sha=='230cfe009d989253d49bb18afc04a1fe64cafea53941e61100c6cd19d953634c'
s=b.decode();t=ast.parse(s);proof=json.loads((p/'FINITE_INVERSE_PROOF.json').read_text());original=Path(proof['parent']['path']).read_text();reverted=s
for change in reversed(proof['finite_replacements']):
 assert reverted.count(change['after'])==change['occurrences'];reverted=reverted.replace(change['after'],change['before'])
assert reverted==original and hashlib.sha256(original.encode()).hexdigest()=='3064dbf8c2a332d456d2d892b55ad424b5086172bada81e55b83ba1966ff647a'
fn={n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,ast.FunctionDef)}
metadata=ast.parse(fn['metadata_inputs'])
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('open','read','read_bytes','read_text','pin') for n in ast.walk(metadata))
main=ast.parse(fn['main']);execs=[n for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='runner' and n.func.attr=='execute'];assert len(execs)==1
assert 'numpy' not in s and 'sys.settrace' not in s and 'sys.setprofile' not in s and '__bases__=' not in s
# SOURCE-only full-byte admission observations on the now installed actual D.
d=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_saved_source_phase_diagnostic_sources')
source_pins={}
for f in sorted(d.rglob('*')):
 assert not f.is_symlink()
 if f.is_file():
  raw=f.read_bytes();source_pins[str(f.relative_to(d))]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
assert len(source_pins)>=28  # Root added its actual install return after the initial 28-member observation
wanted=['1eb226b3d02da061c0c8e1750540f925c1ec9f6baf23afbbe0f6b24cd00fb991','58d1cad3ed22b3d56f7db4d721ed3166cae04fd7d86e5c95f6c9df1532023fb9','a99db7ea44374e9c86159f102aa7f32c7fcaff0b7311ba71db341caff417dece','06623a9481878b4eeb543cdcafe005dfc0a361d4e9f819e331a1d566cdf5dd57','73806690ec7abf26771978c7beec67df5f4c3ec7b2274d444053c0a212323efc','bd86427d38677730da4738ddf9a6ac7fd43610a0075dbd760eb2ee3860db671e','4104f091a85aa3b302ed4e0092535b833d82eb62c904b01e8baf60cfada0d34d','e4eed9d520499cf15dae35c56adb1b7a3dea54e67e73046dd828ee47a1225fcf']
assert set(wanted).issubset({v['sha256'] for v in source_pins.values()})
contracts=[d/name for name,entry in source_pins.items() if Path(name).name=='input_contract.json' and entry['sha256']==wanted[0]];assert len(contracts)==1
contract=json.loads(contracts[0].read_text())['inputs'];assert len(contract)==1140
canonical=Path('/Users/wen/spot/validation/axial_material/refined_AAA_full_group_saved_source_phase_consistency_diagnostic_20261010.py');ready=canonical.read_bytes();assert hashlib.sha256(ready).hexdigest()==wanted[-1] and len(ready)==290156
orig=Path('/private/tmp/axmat_saved_source_phase_source_only_20261010_nx62ri4n/complete_saved_S2_source_phase_consistency.UNREADY.py').read_bytes();assert ready.replace(b"SOURCE_STATUS = 'READY'\n",b"SOURCE_STATUS = 'UNREADY'\n",1)==orig
paths={}
for role,entry in contract.items():
 path=Path(entry['path']);st=path.stat();observed={k:getattr(st,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')};assert observed==entry['observed_metadata_7id'];paths[role]=observed
assert sum(v['st_size'] for v in paths.values())==96042876
for name in ('axial-material-AAA-refined-all-group-saved-source-phase-consistency-host-20261010','axial-material-AAA-refined-all-group-saved-source-phase-consistency-20261010'):
 assert not os.path.lexists(Path('/Users/wen/spot/validation/artifacts')/name)
f=p/'source_only_generation_failure_7a883d.json';failure=json.loads(f.read_text());failure['actual_observed_tool_return']['output_excerpt']=failure['actual_observed_tool_return'].pop('output');f.write_text(json.dumps(failure,indent=2)+'\n')
audit={'schema':'AXMAT_SAVED_SOURCE_PHASE_HOST_FINAL_STATIC_REVIEW_V1','status':'PASS_SOURCE_ONLY_NO_RUNTIME_QUALIFICATION','candidate_sha256':sha,'candidate_bytes':len(b),'finite_inverse_3064_whole_byte_exact':True,'finite_replacements':16,'SOURCE_archive_actual_current_path':str(d),'SOURCE_archive_metadata_and_source_bytes_count':len(source_pins),'SOURCE_archive_source_bytes_total':sum(entry['bytes'] for entry in source_pins.values()),'SOURCE_archive_full_byte_pins':source_pins,'source_contract_actual_path':str(contracts[0]),'canonical_READY_source_SHA':wanted[-1],'canonical_all15functions_original_unchanged':True,'all1140_input_stat_only_7id_metadata_reobserved':paths,'numeric_input_EOF_SHA_not_performed_by_this_source_review':True,'no_support_pin_or_raw_read_in_metadata_input_observer':True,'one_original_runner_execute_only':True,'original_705_MRO_and_full_guard_source_unchanged':True,'numpy_not_imported_or_used_by_host':True,'host_candidate_not_imported_or_executed':True,'helpers_and_driver_not_imported_or_executed':True,'numeric_payload_read':False,'canonical_written':False,'future_actual_host_pin':None,'future_actual_terminal_pin':None,'future_actual_output_pins':None}
(p/'FINAL_STATIC_REVIEW.json').write_text(json.dumps(audit,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':audit['status'],'directory':str(p),'candidate_SHA':sha,'candidate_bytes':len(b),'final_static_review_SHA':hashlib.sha256((p/'FINAL_STATIC_REVIEW.json').read_bytes()).hexdigest(),'finite_inverse_exact':True,'source_only':True,'numeric_payload_read':False,'candidate_helpers_driver_not_executed':True},indent=2))

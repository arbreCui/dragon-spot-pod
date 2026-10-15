"""Root-only Source preparation after genuine completed finite v6/post0."""
import argparse,ast,hashlib,json,os
from pathlib import Path
import capture_source_common as c

def inverse(original,candidate):
 a=Path(original).read_bytes();b=Path(candidate).read_bytes();i=0
 while i<min(len(a),len(b)) and a[i]==b[i]:i+=1
 j=0
 while j<min(len(a)-i,len(b)-i) and a[-1-j]==b[-1-j]:j+=1
 ae=len(a)-j;be=len(b)-j;rebuilt=b[:i]+a[i:ae]+b[be:];c.require(rebuilt==a,'whole original complete byte inverse')
 return dict(original_full_pin=c.pin(original),candidate_full_pin=c.pin(candidate),edit_map=[dict(original_begin_byte=i,original_end_byte=ae,candidate_begin_byte=i,candidate_end_byte=be,original_bytes_hex=a[i:ae].hex(),candidate_bytes_hex=b[i:be].hex())],whole_original_reconstructed_sha256=hashlib.sha256(rebuilt).hexdigest(),complete_inverse_reconstructed_original=True)

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 ap.add_argument('--finite-post-schema',required=True);ap.add_argument('--finite-post-status',required=True);a=ap.parse_args()
 c.require(not os.path.lexists(c.OUT) and not any((c.BASE/n).exists() for n in ('PLAN.json','SOURCE_REVIEW_READY.json','ORIGINAL_SOURCE_AND_MINIMAL_INVERSE.json')),'fresh once Source preparation/output, no retry')
 author_pin=c.pin(c.BASE/'AUTHOR_SOURCE_ONLY_FREEZE.json');author=c.read(author_pin)
 c.require(author['source_only'] is True and author['source_preparation_executed'] is False and author['compiler_executed'] is False and author['numerical_executed'] is False,'frozen author Source only')
 for p in author['source_pins']:c.require(c.pin(p['path'])==p,'unchanged whole authored Source');ast.parse(c.exact(p),filename=p['path'])
 finite_plan_pin=c.pin(c.FINITE_ENTRY/'PLAN.json');finite=c.read(finite_plan_pin)
 c.require(finite['original_caps']==c.CAPS and finite['planned_actual_output_root']==str(c.FINITE_OUT) and len(finite['complete_joint_roots'])==52,'completed finite v6 same output/caps52')
 proof={k:c.pin(p) for k,p in dict(host=c.FINITE_OUT/'Root_actual_eight_fuel_finite18_SCAT_summary.json',child=c.FINITE_OUT/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json',root_tools=c.FINITE_ENTRY/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json',post=c.FINITE_ENTRY/'actual_postverify_20261015/corrected_argument_identity_v2/REVIEW.json',post_tools=c.FINITE_ENTRY/'actual_postverify_20261015/corrected_argument_identity_v2/TRUE_TOOL_RETURNS.json').items()}
 c.check_finite(proof,a.finite_post_schema,a.finite_post_status)
 mother_pin=c.pin(c.V6/'PLAN.json');mother=c.read(mother_pin);mother_hf_pin=c.pin(c.V6/'COMPLETE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_HOST_SOURCE_ONLY_FREEZE.json');mother_hf=c.read(mother_hf_pin)
 science=[mother[k] for k in ('native_A1_SQLite_pin','native_A1_pool_pin')]
 c.require([p['path'] for p in science]==[str(c.ART/'axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence/A1'/n) for n in ('original_archive_index.sqlite','original_words.bin')] and [p['sha256'] for p in science]==['d600af50d3fa394eba033798af415afab71d8e10577feb0f0a545804a5a42734','b1bddebf913115e3b13891082f98716eb1e46cd3f9205ccd291567d477fb696c'] and sum(p['size_bytes'] for p in science)==202708660,'only exact literal2 A1 original current producer spools')
 for p in science:c.current(p)
 old_plan_pin=c.pin(c.OLD_RETIRE/'PLAN.json');old=c.read(old_plan_pin);old_receipt_pin=c.pin(c.OLD_RETIRE/'EXECUTION_RECEIPT.json');oldreceipt=c.read(old_receipt_pin)
 c.require(oldreceipt['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and oldreceipt['failure'] is None and oldreceipt['actual_released_pins']==oldreceipt['exact_target_pins'] and oldreceipt['actual_released_bytes']==405417320,'original completed literal4 history unchanged')
 for p in oldreceipt['actual_released_pins']:c.require(not os.path.lexists(p['path']),'old literal4 remains absent')
 original_helper=c.pin(c.V6/'run_one_actual_track_component.py');helper=c.pin(c.BASE/'original_v6_run_one_actual_track_component.py');retire_original=c.pin(c.OLD_RETIRE/'retire_literal4_completed_compare_spools.py');retire_copy=c.pin(c.BASE/'original_retire_literal4_completed_compare_spools.py')
 c.require(helper['sha256']==original_helper['sha256'] and helper['size_bytes']==original_helper['size_bytes'] and retire_copy['sha256']==retire_original['sha256'] and retire_copy['size_bytes']==retire_original['size_bytes'],'whole unchanged original vector helper and literal4 closure Source')
 adapter_rows=[r for r in mother['explicit_import_bindings'] if r['module']=='actual_track_saved_adapter'];c.require(len(adapter_rows)==1,'only original saved-data adapter, no transport/kernel imports')
 c.exact(adapter_rows[0]['pin'])
 preserved=[p for p in old['preserved_current7_pins'] if p['path'] not in c.SCIENCE_PATHS]
 for p in preserved:c.current(p)
 old_history_pins=[c.pin(q) for q in sorted(c.OLD_RETIRE.iterdir()) if q.is_file()]
 preserved_full=c.unique(old_history_pins+[p for pair in old['original_native_pairs'] for p in (pair['archive_pin'],)]+list(old['closure_pins'].values())+[old_plan_pin,old_receipt_pin,retire_original])
 for p in preserved_full:c.current(p)
 roots=list(finite['complete_joint_roots'])+[str(c.TOP),str(c.OUT)]
 c.require(len(roots)==54 and len(set(roots))==54 and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'inherited finite52 + whole capture TOP/output54 without reset')
 wanted={mother[k]['path'] for k in ('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin')}
 wanted.update(str(c.REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'/n) for n in ('prepare_qualified_AB_source_factor_production.py','runtime/production_runner.py'))
 wanted.update(str(p) for p in (c.R/'validation/axial_material/qualify_refined_AAA_layered_full.py',c.R/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'))
 support_dependencies=[p for p in mother_hf['dependencies'] if p['path'] in wanted]
 c.require({p['path'] for p in support_dependencies}==wanted,'complete original guard support Source roles')
 for p in support_dependencies:c.exact(p)
 original_guard=c.BASE/'original_all34_guard_host.py';actual_guard=c.REC/'current_all34_original_ASCII_infinite_SCAT_producer_source_v1_20261015/v2/run_guarded_all34_original_ascii_infinite_SCAT.py';actual_writer=c.REC/'current_full370_real_operator_control_source_v1_20261015/write_once_full370_real_operator_control_SF_HF_CLI.py';writer_copy=c.BASE/'original_full_control_once_writer.py'
 for oldp,copy in ((actual_guard,original_guard),(actual_writer,writer_copy)):
  c.require(c.pin(oldp)['sha256']==c.pin(copy)['sha256'] and oldp.read_bytes()==copy.read_bytes(),'whole unchanged original guard/writer Source copies')
 guard=c.BASE/'run_guarded_A1_native_vector_capture.py';oldguard=original_guard.read_text();newguard=guard.read_text();start=' class Resources:';end=' resources=Resources();';c.require(oldguard[oldguard.index(start):oldguard.index(end)]==newguard[newguard.index(start):newguard.index(end)],'whole original Resources methods unchanged')
 copies=[dict(original_full_pin=c.pin(actual_guard),whole_unchanged_copy_full_pin=c.pin(original_guard)),dict(original_full_pin=c.pin(actual_writer),whole_unchanged_copy_full_pin=c.pin(writer_copy)),dict(original_full_pin=original_helper,whole_unchanged_copy_full_pin=helper),dict(original_full_pin=retire_original,whole_unchanged_copy_full_pin=retire_copy)]
 source_proof=dict(schema='A1_NATIVE_VECTOR_CAPTURE_LITERAL2_ORIGINAL_SOURCE_AND_MINIMAL_INVERSE_V1',whole_original_source_copies=copies,original_small_vectors_function_sha256=hashlib.sha256(c.exact(helper)[c.exact(helper).index(b'def small_vectors('):c.exact(helper).index(b'def main():')]).hexdigest(),whole_original_small_vectors_called_unchanged=True,host_complete_byte_inverse=inverse(original_guard,guard),retirement_complete_byte_inverse=inverse(c.BASE/'original_retire_literal4_completed_compare_spools.py',c.BASE/'retire_literal2_completed_A1_compare_spools.py'),publisher_complete_byte_inverse=inverse(c.BASE/'original_full_control_once_writer.py',c.BASE/'write_once_A1_native_vector_capture_SF_HF_CLI.py'),scientific_math_changed=False,scientific_payload_read=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)
 proof_pin=c.write(c.BASE/'ORIGINAL_SOURCE_AND_MINIMAL_INVERSE.json',source_proof)
 metadata=c.unique(old_history_pins+finite['explicit_cumulative_metadata_file_pins']+list(proof.values())+[finite_plan_pin,mother_pin,mother_hf_pin,author_pin,old_plan_pin,old_receipt_pin,proof_pin]+list(old['closure_pins'].values()))
 dependencies=c.unique(old_history_pins+author['source_pins']+support_dependencies+[helper,original_helper,retire_original]+[r['pin'] for r in adapter_rows]+science+list(proof.values())+[finite_plan_pin,mother_pin,mother_hf_pin,author_pin,old_plan_pin,old_receipt_pin,proof_pin]+list(old['closure_pins'].values()))
 plan=dict(schema='A1_NATIVE_VECTOR_CAPTURE_AND_LITERAL2_RETIREMENT_SOURCE_ONLY_PLAN_V1',source_only=True,original_caps=c.CAPS,complete_joint_roots=roots,inherited_complete_joint_roots=finite['complete_joint_roots'],inherited_finite_plan_pin=finite_plan_pin,planned_actual_output_root=str(c.OUT),explicit_cumulative_metadata_file_pins=metadata,source_dependency_pins=dependencies,scientific_input_current7_pins=science,native_A1_SQLite_pin=science[0],native_A1_pool_pin=science[1],target_pins=science,planned_released_bytes=202708660,closure_pins=old['closure_pins'],original_native_pairs=old['original_native_pairs'],preserved_current7_pins=preserved,preserved_full_provenance_pins=preserved_full,actual_original_literal4_receipt_pin=old_receipt_pin,actual_original_literal4_plan_pin=old_plan_pin,original_literal4_closure_Source_pin=retire_copy,original_v6_vector_helper_pin=helper,original_v6_vector_helper_provenance_pin=original_helper,saved_adapter_import_bindings=adapter_rows,exact_saved_adapter_source_root=str(Path(adapter_rows[0]['pin']['path']).parent),worker_source_pin=c.pin(c.BASE/'capture_A1_native_vectors.py'),host_source_pin=c.pin(guard),retirement_source_pin=c.pin(c.BASE/'retire_literal2_completed_A1_compare_spools.py'),original_Common_Source_pin=mother['original_Common_Source_pin'],original_support_Source_pin=mother['original_support_Source_pin'],original_bounded_Source_pin=mother['original_bounded_Source_pin'],finite_prerequisite_pins=proof,finite_post_schema=a.finite_post_schema,finite_post_status=a.finite_post_status,expected_vector_record_count=4,expected_REAL32_words=26,expected_capture_bytes=104,expected_vector_offsets_bytes=[0,16,32,48],native_XSM_redecode_required=False,new_control_reserved_bytes=8*2**20,scope='Current native A1 26 REAL32 words only; exact two completed comparison spools retirement after actual capture/post0. No native engine, compiler or scientific arithmetic.',business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)
 pp=c.write(c.BASE/'PLAN.json',plan)
 ready=c.write(c.BASE/'SOURCE_REVIEW_READY.json',dict(schema='A1_NATIVE_VECTOR_CAPTURE_SOURCE_REVIEW_READY_V1',source_only=True,source_preparation_only=True,source_pins=author['source_pins'],selected_metadata_pins=metadata,plan_pin=pp,author_source_freeze_pin=author_pin,worker_source_pin=plan['worker_source_pin'],host_source_pin=plan['host_source_pin'],retirement_source_pin=plan['retirement_source_pin'],original_Source_proof_pin=proof_pin,finite_actual_completed_prerequisite_pins=proof,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE))
 print(json.dumps(dict(status='A1_NATIVE_VECTOR_CAPTURE_LITERAL2_SOURCE_PREPARED_ONLY',ready_pin=ready,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)),flush=True)
if __name__=='__main__':main()

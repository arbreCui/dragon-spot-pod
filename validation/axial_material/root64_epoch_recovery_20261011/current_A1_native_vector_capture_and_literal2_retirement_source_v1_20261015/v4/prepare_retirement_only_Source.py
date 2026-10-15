"""Root-only fresh retirement metadata route; never prepares capture again."""
import argparse,ast,hashlib,json,os
from pathlib import Path
import capture_source_common as c
BASE=Path(__file__).absolute().parent;CAPTURE_ENTRY=BASE.parent/'v2';PRIOR_FAILED_ENTRY=BASE.parent/'v3'

def inverse(original,candidate):
 a=Path(original).read_bytes();b=Path(candidate).read_bytes();i=0
 while i<min(len(a),len(b)) and a[i]==b[i]:i+=1
 j=0
 while j<min(len(a)-i,len(b)-i) and a[-1-j]==b[-1-j]:j+=1
 ae=len(a)-j;be=len(b)-j;rebuilt=b[:i]+a[i:ae]+b[be:];c.require(rebuilt==a,'complete original Source byte inverse')
 return dict(original_full_pin=c.pin(original),candidate_full_pin=c.pin(candidate),edit_map=[dict(original_begin_byte=i,original_end_byte=ae,candidate_begin_byte=i,candidate_end_byte=be,original_bytes_hex=a[i:ae].hex(),candidate_bytes_hex=b[i:be].hex())],whole_original_reconstructed_sha256=hashlib.sha256(rebuilt).hexdigest(),complete_inverse_reconstructed_original=True)

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--capture-post-schema',required=True);ap.add_argument('--capture-post-status',required=True);a=ap.parse_args()
 c.require(not any((BASE/n).exists() for n in ('PLAN.json','SOURCE_REVIEW_READY.json','ORIGINAL_RETIREMENT_SOURCE_ROUTE_INVERSE.json')),'fresh retirement-only metadata generation once')
 author_pin=c.pin(BASE/'AUTHOR_RETIREMENT_ONLY_SOURCE_FREEZE.json');author=c.read(author_pin)
 c.require(author['source_only'] is True and author['source_preparation_executed'] is False and author['business_executed'] is False and author['files_deleted'] is False,'frozen unexecuted retirement-only author Source')
 for p in author['source_pins']:c.require(c.pin(p['path'])==p,'whole unchanged frozen Source');ast.parse(c.exact(p),filename=p['path'])
 prior={n:c.pin(PRIOR_FAILED_ENTRY/n) for n in ('AUTHOR_RETIREMENT_ONLY_SOURCE_FREEZE.json','PLAN.json','SOURCE_REVIEW_READY.json','ORIGINAL_RETIREMENT_SOURCE_ROUTE_INVERSE.json','ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json','independent_source_review_20261015/REVIEW.json','independent_source_review_20261015/TRUE_TOOL_RETURNS.json','ROOT_FINAL_PUBLICATION_TRUE_TOOL_RETURNS.json','RETIREMENT_SOURCE_PUBLICATION_RECEIPT.json')}
 prior_author=c.read(prior['AUTHOR_RETIREMENT_ONLY_SOURCE_FREEZE.json']);prior_ready=c.read(prior['SOURCE_REVIEW_READY.json']);prior_review=c.read(prior['independent_source_review_20261015/REVIEW.json']);prior_pub=c.read(prior['ROOT_FINAL_PUBLICATION_TRUE_TOOL_RETURNS.json']);prior_receipt=c.read(prior['RETIREMENT_SOURCE_PUBLICATION_RECEIPT.json'])
 for pp0 in prior_author['source_pins']:c.require(c.pin(pp0['path'])==pp0,'prior v3 five frozen Sources remain unchanged')
 c.closed0(c.read(prior['ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json']),'actual_Source_preparation_return',prior['SOURCE_REVIEW_READY.json'],'ready_pin')
 c.require(prior_review['status'].startswith('PASS') and prior_review['failure'] is None,'prior genuine passing Source review unchanged')
 c.closed0(c.read(prior['independent_source_review_20261015/TRUE_TOOL_RETURNS.json']),'actual_review_return',prior['independent_source_review_20261015/REVIEW.json'],'review_pin')
 terminal=prior_pub['actual_publication_return'];c.require(prior_pub['observed_closed'] is True and type(prior_pub['original_integer_exit_code']) is int and prior_pub['original_integer_exit_code']==1 and type(terminal['exit_code']) is int and terminal['exit_code']==1 and terminal.get('session_id') is None and "KeyError: 'identity'" in terminal['output'],'prior actual publication typed1 caused by Root PF argument schema')
 c.require(prior_receipt['status']=='FAILED_ONCE_RETIREMENT_SOURCE_PUBLICATION_NO_RETRY' and prior_receipt['failure']=="KeyError('identity')" and prior_receipt['files_deleted'] is False and prior_receipt['capture_republished'] is False and prior_receipt['capture_rerun'] is False,'prior claimed/failed once receipt retained, no successful publication or deletion inferred')
 for n in ('RETIREMENT_SOURCE_ONLY_FREEZE.json','READONLY_RETIREMENT_RECEIPT.json','EXECUTION_RETIREMENT_RECEIPT.json','ROOT_RETIREMENT_EXECUTION_TRUE_TOOL_RETURNS.json'):c.require(not os.path.lexists(PRIOR_FAILED_ENTRY/n),'prior failed v3 operation remains unexecuted/unpublished')
 prior_source_pins=prior_author['source_pins'];whole_entry_proof=[]
 for oldp in prior_source_pins:
  newpath=BASE/Path(oldp['path']).name;newp=c.pin(newpath);unchanged=oldp['sha256']==newp['sha256'] and oldp['size_bytes']==newp['size_bytes'];c.require(unchanged or newpath.name=='prepare_retirement_only_Source.py','only prior failure admission preparer Source may differ');whole_entry_proof.append(dict(original_full_pin=oldp,candidate_full_pin=newp,whole_copy_unchanged=unchanged,complete_inverse=inverse(oldp['path'],newp['path'])))
 pp=c.pin(CAPTURE_ENTRY/'PLAN.json');old=c.read(pp);sfpin=c.pin(CAPTURE_ENTRY/'FINAL_SOURCE_FREEZE.json');sf=c.read(sfpin)
 c.require(old['schema']=='A1_NATIVE_VECTOR_CAPTURE_AND_LITERAL2_RETIREMENT_SOURCE_ONLY_PLAN_V1' and sf['control_plan_pin']==pp and old['original_caps']==c.CAPS and len(old['complete_joint_roots'])==54 and str(BASE.parent) in old['complete_joint_roots'],'original capture v2 same PLAN/SF/wholeTOP54/caps')
 proof={k:c.pin(q) for k,q in dict(host=c.OUT/'Root_actual_A1_native_vector_capture_summary.json',child=c.OUT/'inventories/ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE.json',root_tools=CAPTURE_ENTRY/'ROOT_CAPTURE_ACTUAL24_TRUE_TOOL_RETURNS.json',post=CAPTURE_ENTRY/'actual_capture_postverify_20261015/corrected_process_access_v2/REVIEW.json',post_tools=CAPTURE_ENTRY/'actual_capture_postverify_20261015/corrected_process_access_v2/TRUE_TOOL_RETURNS.json').items()}
 h=c.read(proof['host']);e=c.read(proof['child']);post=c.read(proof['post']);compact=e['compact_vector_full_pin'];c.current(compact)
 c.require(h['status']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_26R4_104B_CLOSED0_ONLY' and h['failure'] is None and h['secondary_failures']==[] and h['final_report_resource_check_passed'] is True and h['actual_evidence']==e and e['captured_bytes']==104 and e['captured_REAL32_words']==26 and e['captured_original_record_count']==4 and e['original_small_vectors_called_unchanged'] is True and [e['original_A1_SQLite_pin'],e['original_A1_pool_pin']]==old['target_pins'],'actual capture same literal2 producer provenance')
 c.closed0(c.read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin')
 c.require(post['schema']==a.capture_post_schema and post['status']==a.capture_post_status and a.capture_post_status.startswith('PASS') and post['failure'] is None and all(c.contains(post,proof[k]) for k in ('host','child','root_tools')) and c.contains(post,compact),'genuine corrected process-access capture post0 exact proofs')
 c.closed0(c.read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')
 c.check_finite(old['finite_prerequisite_pins'],old['finite_post_schema'],old['finite_post_status'])
 for p in old['target_pins']:c.current(p)
 candidate=c.pin(BASE/'retire_literal2_completed_A1_compare_spools.py');original=c.pin(CAPTURE_ENTRY/'retire_literal2_completed_A1_compare_spools.py');copy=c.pin(BASE/'original_retire_literal2_completed_A1_compare_spools_v2.py')
 c.require(original['sha256']==copy['sha256'] and original['size_bytes']==copy['size_bytes'] and Path(original['path']).read_bytes()==Path(copy['path']).read_bytes(),'whole original v2 retirement Source retained')
 source_proof=c.write(BASE/'ORIGINAL_RETIREMENT_SOURCE_ROUTE_INVERSE.json',dict(schema='RETIREMENT_ONLY_V3_ORIGINAL_V2_SOURCE_ROUTE_INVERSE_V1',original_full_source_pin=original,whole_unchanged_original_copy_pin=copy,candidate_full_source_pin=candidate,complete_byte_inverse=inverse(copy['path'],candidate['path']),only_provenance_post_and_fresh_Source_paths_changed=True,target2_unlink_closure_hash_and_resource_math_unchanged=True,prior_v3_failed_once_publication_pins=prior,prior_v3_actual_publication_integer_exit_code=1,prior_v3_complete_Source_inverse_proofs=whole_entry_proof,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE))
 plan=json.loads(json.dumps(old));plan.update(retirement_only=True,source_only=True,original_capture_plan_pin=pp,original_capture_source_freeze_pin=sfpin,retirement_source_pin=candidate,original_retirement_v2_source_pin=original,original_retirement_v2_whole_copy_pin=copy,original_retirement_source_route_inverse_pin=source_proof,actual_corrected_capture_proof_pins=proof,actual_compact_capture_full_pin=compact,capture_post_schema=a.capture_post_schema,capture_post_status=a.capture_post_status,source_author_freeze_pin=author_pin,capture_republished=False,capture_rerun=False,prior_v3_failed_once_publication_pins=prior,prior_v3_original_publication_exit_code=1,prior_v3_failure_not_retried=True)
 selected=c.unique(prior_source_pins+list(prior.values())+author['source_pins']+[author_pin,pp,sfpin,source_proof,original]+list(proof.values())+[p for p in old['source_dependency_pins'] if p['path'] not in c.SCIENCE_PATHS])
 plan['retirement_only_selected_Source_and_metadata_pins']=selected
 plan_pin=c.write(BASE/'PLAN.json',plan)
 ready=c.write(BASE/'SOURCE_REVIEW_READY.json',dict(schema='RETIREMENT_ONLY_SOURCE_REVIEW_READY_V1',source_only=True,source_preparation_only=True,plan_pin=plan_pin,retirement_source_pin=candidate,selected_Source_and_metadata_pins=selected,actual_corrected_capture_proof_pins=proof,source_author_freeze_pin=author_pin,source_route_inverse_pin=source_proof,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,capture_republished=False,capture_rerun=False,**c.FALSE))
 print(json.dumps(dict(status='RETIREMENT_ONLY_LITERAL2_V4_SOURCE_PREPARED_ONLY',ready_pin=ready,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)),flush=True)
if __name__=='__main__':main()

"""UNREADY metadata-only lifecycle: exact original1 + remaining3 = original4.

Only exact saved PF roles can become historical. No payload, helper import,
decompression, deletion, generic missing-path skip, or scientific operation.
"""
import json,os
from pathlib import Path
SCHEMA='CURRENT_B4_SPLIT1_PLUS3_EXACT_ARCHIVED_RETIRED_PRODUCT_ROLES_ADMISSION_V2'
ROLE_KEYS={
 'member0_restore':('Root_report_pin','Root_tools_pin','post_pin','post_tools_pin'),
 'exact2_recovery':('receipt_pin','Root_tools_pin','post_pin','post_tools_pin','plan_pin','inherited_archive_binding_pin'),
 'complete4_archive':('Root_report_pin','Root_tools_pin','child_report_pin','index_pin','post_pin','post_tools_pin'),
 'remaining3_retirement':('receipt_pin','Root_tools_pin','post_pin','post_tools_pin')}
def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def document(v,schema,status):
 need(v['schema']==schema and v['status']==status and v['failure']is None,'exact actual schema/status/failure; no generic PASS')
def closed(v,key,chunk,field,expected):
 r=v[key]
 need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and type(chunk)is str and r['chunk_id']==chunk,'exact genuine closed typed0 return')
 need(json.loads(r['output'].strip().splitlines()[-1])[field]==expected,'genuine stdout exact metadata PF')
def at(v,path):
 need(type(path)is list and len(path)>0 and all(type(k)in(str,int)for k in path),'explicit audited metadata key/index path')
 for k in path:v=v[k]
 return v
def metadata_pins(spec,require_complete=True):
 need(type(spec)is dict and spec['schema']==SCHEMA,'explicit split1+3 lifecycle')
 rows=[spec['actual_B_capture_manifest_pin'],spec['member0_complete_entry_pin']]
 entries=spec['ordered_exact4_current_entry_pins']
 if entries is None:need(require_complete is False,'future four durable entry PFs still NULL')
 else:need(type(entries)is list and len(entries)==4,'explicit complete4 entry PF list');rows+=entries
 for phase,keys in ROLE_KEYS.items():
  stage=spec[phase];need(type(stage)is dict,'explicit phase roles')
  for key in keys:
   p=stage[key]
   if p is None:need(require_complete is False,'future archive/remaining3 real PF still NULL')
   else:need(type(p)is dict,'exact metadata PF');rows.append(p)
 return rows
def known_first_original(spec,original,read):
 m=spec['member0_restore'];mr=read(m['Root_report_pin']);mt=read(m['Root_tools_pin']);mp=read(m['post_pin']);mpt=read(m['post_tools_pin'])
 closed(mt,'actual_terminal_return','5826fd','report_pin',m['Root_report_pin']);closed(mpt,'actual_review_return','9345ca','review_pin',m['post_pin'])
 document(mr,'ROOT_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1','PASS_CURRENT_B4_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY')
 document(mp,'RECORDED_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_METADATA_POSTVERIFY_V1','PASS_ACTUAL_ROOT_MEMBER0_STREAMED_ORIGINAL_SHA_LENGTH_CLOSED0_METADATA_ONLY_ALL4_REMAINS_FAILED')
 gz=spec['member0_complete_gzip_pin'];ep=spec['member0_complete_entry_pin']
 need(mp['actual_member0_Root_report_pin']==m['Root_report_pin']and mp['actual_Root_tools_pin']==m['Root_tools_pin']and mp['actual_child_integer_exit_code']is None and mp['actual_member0_children_started']==0,'same genuine Root-only member0 post0; no invented child0')
 need(mr['original_member0_saved_full_pin']==mp['original_member0_saved_full_pin']==original[0]and mr['complete_member0_gzip_pin']==mp['complete_member0_gzip_pin']==gz and mr['retained_member0_entry_pin']==mp['retained_member0_entry_pin']==ep,'same exact member0/gzip/entry')
 need(mr['streamed_complete_member0_verified']is True and mp['Root_actual_complete_member0_stream_verified']is True and mr['streamed_decompressed_SHA']==mp['actual_streamed_decompressed_SHA']==original[0]['sha256']and type(mr['streamed_decompressed_length'])is int and mr['streamed_decompressed_length']==mp['actual_streamed_decompressed_length']==original[0]['size_bytes'],'actual independent complete restoration SHA/length; never replayed here')
 need(mp['original_failed_Root_integer_exit_code']==1 and mp['original_failed_child_integer_exit_code']==1 and mp['original_limited_failure_post_recorded_child_codes']==[]and mp['all4_archive_complete']is False,'old all4 Root1/child1/post0[] preserved')
 e=spec['exact2_recovery'];rr=read(e['receipt_pin']);rt=read(e['Root_tools_pin']);rp=read(e['post_pin']);rpt=read(e['post_tools_pin'])
 closed(rt,'actual_terminal_return','78ceda','receipt_pin',e['receipt_pin']);closed(rpt,'actual_review_return','7b7ebe','review_pin',e['post_pin'])
 document(rr,'CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1','RETIRED_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED')
 document(rp,'CURRENT_B4_EXACT2_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1','PASS_ACTUAL_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED_METADATA_ONLY')
 need(rp['actual_execution_receipt_pin']==e['receipt_pin']and rp['actual_Root_tools_pin']==e['Root_tools_pin']and rp['metadata_only']is True and rp['actual_Root_integer_exit_code']==0 and rp['files_deleted']is True and rp['files_deleted_by_post']is False,'actual exact2 Root0 and independent post0')
 need(rr['plan_pin']==e['plan_pin'],'explicit same exact2 plan role');plan=read(e['plan_pin'])
 need(plan['inherited_complete_archive_plan_pin']==e['inherited_archive_binding_pin'],'explicit same inherited archive binding role');oldarchive=read(e['inherited_archive_binding_pin'])
 need(oldarchive['all4_product_pins']==original and plan['actual_single_member_verification_closure_pins']==dict(Root_report=m['Root_report_pin'],Root_tools=m['Root_tools_pin'],post=m['post_pin'],post_tools=m['post_tools_pin']),'same original4 and actual independent member0 proof')
 partial=spec['historical_incomplete_partial001_pin'];exact2=[original[0],partial]
 need(rr['actual_released_pins']==rp['actual_released_pins']==rr['exact_target_pins']==plan['exact_target_pins']==exact2 and type(rr['actual_released_bytes'])is int and rr['actual_released_bytes']==rp['actual_released_bytes']==sum(p['size_bytes']for p in exact2)==101693287,'exact2 is one original plus one fragment, not two original products')
 need(partial['path']==str(Path(oldarchive['planned_actual_output_root'])/'archives/001_u.asc.gz')and partial['size_bytes']==25099039 and partial['path']not in{p['path']for p in original},'fragment explicit role excluded from original4')
 need(rp['historical_original_member0_full_pin']==original[0]and rp['retained_complete_member0_gzip_pin']==gz and rp['retained_member0_entry_pin']==ep and rp['complete_result_member0_bytes_preserved']is True and rp['exact_two_targets_absent_verified_twice']is True and rp['all4_archive_complete']is False and rp['original_failure_post_recorded_child_codes']==[],'exact first original retired; complete saved member0 and historical failure retained')
 need(spec['first_retired_original_product_pins']==[original[0]]and spec['remaining3_original_product_pins']==original[1:]and not os.path.lexists(original[0]['path'])and not os.path.lexists(partial['path']),'only explicit proven first original and exact fragment absent')
 return dict(original1=[original[0]],fragment=partial,gzip0=gz,entry0=ep)
def archived_original4(spec,original,first,read):
 a=spec['complete4_archive'];p=a['actual_role_projection'];need(type(p)is dict,'archivev2 projection remains NULL until actual closure')
 h=read(a['Root_report_pin']);raw=read(a['Root_tools_pin']);child=read(a['child_report_pin']);index=read(a['index_pin']);post=read(a['post_pin']);pt=read(a['post_tools_pin'])
 for v,which,artifact in((raw,'Root_return','Root_report_pin'),(pt,'post_return','post_pin')):
  x=p[which];closed(v,x['return_field'],x['genuine_terminal_chunk_id'],x['output_artifact_field'],a[artifact])
 document(h,'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_GUARDED_HOST_REPORT_V2','ACTUAL_CURRENT_B4_ALL_PRODUCTS_ARCHIVE_REUSE_MEMBER0_CLOSED0_ONE_RETIRED_THREE_LIVE')
 document(child,'ACTUAL_CURRENT_B4_SERIAL_LOSSLESS_ARCHIVE_REUSE_MEMBER0_REPORT_V2','ALL4_COMPLETE_B_PRODUCT_BYTE_PROOF_CLOSED0_ONE_RETIRED_THREE_LIVE')
 need(h['actual_child_receipt']['report_pin']==a['child_report_pin']and child['index_pin']==a['index_pin']and h['archive_complete']is True and h['final_report_resource_check_passed']is True and h['retired_original_product_pins']==child['retired_original_product_pins']==[original[0]]and h['live_original_product_pins']==child['live_original_product_pins']==original[1:],'actual Host/child explicitly one retired plus three live at archive time')
 need(child['completed_count']==4 and child['newly_archived_count']==3 and child['reused_complete_archive_count']==1 and index['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V2'and index['status']=='ALL4_COMPLETE_B_PRODUCTS_BYTE_PROOF_CLOSED_ONE_RETIRED_THREE_LIVE'and index['retired_original_product_pins']==[original[0]]and index['live_original_product_pins']==original[1:],'complete4 index is reused1 plus new3')
 entries=index['entries'];need(len(entries)==4 and [e['original_plain_full_pin']for e in entries]==original,'ordered original4 exact manifest index')
 compressed=[e['compressed_archive_full_pin']for e in entries];entrypins=[e['entry_pin']for e in entries]
 need(spec['ordered_exact4_current_entry_pins']==entrypins and len({v['path']for v in entrypins})==4 and entrypins[0]==first['entry0'],'all four durable entry files explicitly preserved in index order')
 need(len({v['path']for v in compressed})==4 and spec['ordered_exact4_current_archive_pins']==compressed and compressed[0]==first['gzip0']and index['reused_member0_gzip_pin']==first['gzip0']and index['reused_member0_entry_pin']==first['entry0'],'all four current gzip PFs and old gzip0/entry0 retained exactly')
 for e,o in zip(entries,original):
  need(e['compression_input_SHA']==e['streamed_decompressed_SHA']==o['sha256']and type(e['compression_input_length'])is int and e['compression_input_length']==e['streamed_decompressed_length']==o['size_bytes']and e['exact_original_plain_bytes_recoverable']is True,'all four recorded original whole-byte SHA/length proofs')
 need(entries[0]['reused_complete_archive_from_failed_v1']is True and entries[0]['original_plain_preserved']is False and entries[0]['entry_pin']==first['entry0']and entries[0]['actual_exact2_cleanup_execution_receipt_pin']==spec['exact2_recovery']['receipt_pin'],'entry0 explicit reused archive after original0 retirement')
 pp=p['post'];document(post,pp['schema'],pp['status'])
 need(post['metadata_only']is True and at(post,pp['Root_report_pin_path'])==a['Root_report_pin']and at(post,pp['Root_tools_pin_path'])==a['Root_tools_pin']and at(post,pp['child_report_pin_path'])==a['child_report_pin']and at(post,pp['index_pin_path'])==a['index_pin']and at(post,pp['all4_complete_byte_proofs_verified_path'])is True,'independent archive post0 same Host/child/index and full4 byte-proof facts')
 return compressed,entrypins
def remaining3_closed(spec,original,compressed,read):
 a=spec['remaining3_retirement'];p=a['actual_role_projection'];need(type(p)is dict,'remaining3 actual projection remains NULL until closure')
 r=read(a['receipt_pin']);rt=read(a['Root_tools_pin']);post=read(a['post_pin']);pt=read(a['post_tools_pin'])
 for v,which,artifact in((rt,'Root_return','receipt_pin'),(pt,'post_return','post_pin')):
  x=p[which];closed(v,x['return_field'],x['genuine_terminal_chunk_id'],x['output_artifact_field'],a[artifact])
 rp=p['receipt'];pp=p['post'];document(r,rp['schema'],rp['status']);document(post,pp['schema'],pp['status'])
 need(post['metadata_only']is True and at(post,pp['receipt_pin_path'])==a['receipt_pin']and at(post,pp['Root_tools_pin_path'])==a['Root_tools_pin'],'future independent post0 same remaining3 Root receipt/tools')
 released=at(r,rp['released_pins_path'])
 need(released==at(post,pp['released_pins_path'])==original[1:]and len(released)==len({v['path']for v in released})==3 and at(r,rp['released_bytes_path'])==at(post,pp['released_bytes_path'])==sum(v['size_bytes']for v in original[1:]),'only remaining3 exact original PFs actually retired')
 need(at(r,rp['archive_index_pin_path'])==at(post,pp['archive_index_pin_path'])==spec['complete4_archive']['index_pin']and at(r,rp['retained_archive_pins_path'])==at(post,pp['retained_archive_pins_path'])==compressed,'remaining3 retirement consumes same full4 index and preserves all four archives')
 return released
def admit(request,read,current):
 spec=request['exact_B4_product_lifecycle_binding'];need(type(spec)is dict and spec['schema']==SCHEMA,'explicit split1+3 lifecycle binding required')
 metadata_pins(spec,True)
 m=read(spec['actual_B_capture_manifest_pin']);original=m['states']['B']['actual_material_product_pins']
 need(m['state_order']==['B']and set(m['states'])=={'B'}and m['actual_B_observation_executed']is True and m['actual_A_observation_executed']is False and spec['actual_B_capture_manifest_pin']==request['actual_observation_manifest_pin'],'same genuine B-only manifest')
 need(len(original)==len({p['path']for p in original})==4 and [Path(p['path']).name for p in original]==['m.xsm','u.asc','a.asc','t.asc']and spec['ordered_exact4_historical_product_pins']==original,'only original4 complete products; not context/snapshot/pool or fragment roles')
 first=known_first_original(spec,original,read);compressed,entrypins=archived_original4(spec,original,first,read);rest=remaining3_closed(spec,original,compressed,read)
 union=first['original1']+rest
 need(union==original and len({v['path']for v in union})==4 and first['fragment']['path']not in{v['path']for v in union},'strict original1+remaining3 fullPF union exactly original4; fragment never counted')
 retired={v['path']for v in union};need(all(not os.path.lexists(x)for x in retired),'only proven original4 historical names absent')
 need(not retired&{v['path']for v in request['complete_input_pins']+request['explicit_cumulative_metadata_file_pins']},'historical original4 never ordinary live pins')
 pairs=request['aggregation_binding']['actual_context_states']['B']['all_snapshot_pairs'];contexts=request['aggregation_binding']['actual_context_states']['B']['complete_context_pins']
 protected=[v for row in pairs for v in(row['input_pin'],row['sqlite_pin'],row['native_pool_pin'])]+contexts
 need(len(pairs)==8 and len(contexts)==55 and not(retired|{first['fragment']['path']})&{v['path']for v in protected},'complete8 native/SQL/pool pairs and55contexts remain live; no generic missing skip')
 for v in compressed+entrypins+[spec['complete4_archive']['index_pin']]+protected:current(v)
 return dict(schema=SCHEMA,exact_four_historical_fullPFs_preserved=original,exact_four_current_archive_pins=compressed,exact_four_current_entry_pins=entrypins,first_retired_original_product_pins=first['original1'],remaining3_retired_original_product_pins=rest,explicit1_plus3_union_exactly_original4=True,partial_fragment_excluded_from_original4=True,retired_paths_exactly_absent=True,all8_native_tree_SQL_pool_pairs_and55_contexts_retained=True,scientific_arrays_recomputed=False)

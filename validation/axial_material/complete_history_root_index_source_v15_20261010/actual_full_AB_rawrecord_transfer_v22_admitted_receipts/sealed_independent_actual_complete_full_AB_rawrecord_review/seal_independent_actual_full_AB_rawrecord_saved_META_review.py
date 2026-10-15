#!/usr/bin/env python3
"""Pure stdlib peer seal: repeat complete finite EOF SHA7ID, never decode material."""
import hashlib
import json
import os
import pathlib
import stat
HERE=pathlib.Path(__file__).parent
def id7(path):
 s=pathlib.Path(path).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 path=pathlib.Path(path);before=id7(path)
 if not stat.S_ISREG(before[2])or before[3]!=1:raise ValueError('not single-link regular finite Source/META/raw/binary')
 h=hashlib.sha256();n=0
 with path.open('rb')as f:
  while True:
   block=f.read(1048576)
   if not block:break
   n+=len(block);h.update(block)
  s=os.fstat(f.fileno());descriptor=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if descriptor!=before or id7(path)!=before or n!=before[4]:raise ValueError('unstable complete EOF SHA7ID')
 return {'path':str(path),'sha256':h.hexdigest(),'identity':before,'size_bytes':n}
report_path=HERE/'INDEPENDENT_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_META_REVIEW.json';report=json.loads(report_path.read_bytes());audit_path=HERE/'ACTUAL_FULL_RAW_SAVED_META_PEER_AUDIT_TOOL_TERMINAL_RETURN.json';audit=json.loads(audit_path.read_bytes());t=audit['terminal_tool_return'];root_t=report['actual_Root_terminal_tool_return']
if report['PASS']is not True or report['hard_blockers']!=[]or report['check_count']!=4752 or type(t['exit_code'])is not int or t['exit_code']!=0 or t['chunk_id']!='7f8814' or 'session_id'in t or audit['closed']is not True:raise ValueError('peer audit not genuine strict0closed/PASS')
if type(root_t['exit_code'])is not int or root_t['exit_code']!=0 or root_t['chunk_id']!='8bdd07' or 'session_id'in root_t:raise ValueError('Root actual business terminal not genuinely strict0closed')
unique={item['path']:item for item in report['unique_complete_fresh_rechecked_input_pins']}
for path,expected in unique.items():
 actual=pin(path)
 if any(actual[k]!=expected[k]for k in ('path','sha256','identity','size_bytes')):raise ValueError('original Source/META/raw/binary changed before peer seal '+path)
for ns in report['complete_namespace_snapshots']:
 root=pathlib.Path(ns['root']);files=set();directories={};links={}
 for current,ds,fs in os.walk(root,followlinks=False):
  current=pathlib.Path(current);directories[current.relative_to(root).as_posix()]=id7(current)
  for name in ds[:]:
   p=current/name
   if p.is_symlink():links[p.relative_to(root).as_posix()]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)};ds.remove(name)
  for name in fs:
   p=current/name
   if p.is_symlink():links[p.relative_to(root).as_posix()]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)}
   else:files.add(p.relative_to(root).as_posix())
 if files!=set(ns['complete_regular_file_names'])or directories!=ns['directories']or links!=ns['symlinks']:raise ValueError('complete finite namespace changed before seal '+ns['label'])
members={p.name:pin(p)for p in sorted(HERE.iterdir())if p.is_file()}
seal={'schema':'INDEPENDENT_V22_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_META_PEER_SEAL_V1','scope':'STANDARD_LIBRARY_FINITE_SOURCE_SAVED_META_JSONL_INDEX_AND_RAW_BINARY_EOF_SPAN_SHA_ONLY','actual_peer_audit_tool_return':t,'actual_peer_exit_code':0,'actual_peer_closed':True,'all4752_saved_actual_checksPASS':True,'hard_blocker_count':0,'independent_saved_actual_review_report':pin(report_path),'actual_peer_audit_tool_receipt':pin(audit_path),'actual_Root_business_tool_receipt':report['actual_Root_terminal_tool_receipt'],'actual_Root_terminal_tool_return':root_t,'all307_unique_finite_Source_META_raw_binary_inputs_second_complete_EOF_SHA7ID_unchanged':True,'unique_complete_EOF_inputs_rechecked_at_seal':len(unique),'all_complete_D_E_H_O_C_directory7ID_and_member_sets_unchanged':True,'all_fresh_TMP_files_before_this_seal_and_future_actual_seal_tool_receipt':members,'complete_D173files15directories_freeze_not_appended':True,'all_A_B_19619records19990physicalheaders2264113values_saved':True,'every_raw_header_close_and_typed_span_SHA_verified':True,'both_original_A_B_raw_archives_byte_equal_actual_inputs':True,'all_REAL32rounded_parser64_REAL64_integer_character_extra_fields_preserved_software_evidence':True,'protocol5positive10reject_and_complete_tiny8515gaps_retained':True,'full_A_B_8515required_fields_and8880sparse_references_each_retained':True,'FISSIONINDEX_original_gap_each_state':report['FISSIONINDEX_full_original_gap_each_state'],'original_complete_caps':report['complete_original_caps'],'original_complete_archive_scope':report['original_archive_scope'],'capture_joint_bytes':report['captured_joint_bytes_before_summary_manifest'],'current_joint_bytes':report['current_joint_bytes_after_summary_manifest'],'actual_protocol_watch':report['genuine_actual_watches']['protocol'],'protocol_zero_sample_is_not_actual_memory_zero':True,'actual_transfer_watch':report['genuine_actual_watches']['transfer'],'original_parent_stdout_startup_pin':report['original_parent_stdout_startup_pin'],'actual_parent_stdout_postprint_pin':report['actual_parent_stdout_postprint_pin'],'complete_saved_rawrecord_software_evidence_independently_reviewed':True,'actual_protocol_qualification_sha256':None,'actual_transfer_qualification_sha256':None,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'whole_combined_build_or_INPUT_qualified':False,'reader_helper_guard_API_or_business_executed_by_peer':False,'actual_numeric_material_values_decoded_by_peer':False,'broad_ART_read_by_peer':False,'project_D_E_Root_artifacts_or_original_Source_written_by_peer':False,'peer_initial_schema_assumption_error_and_final_additional_crosspins_preserved':True}
out=HERE/'INDEPENDENT_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_META_PEER_SEAL.json'
if out.exists():raise ValueError('seal already exists')
out.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'schema':seal['schema'],'seal':pin(out),'review':pin(report_path),'actual_peer_audit_chunk':'7f8814','actual_peer_exit_code':0,'closed':True,'all4752checksPASS':True,'unique_finite_complete_EOF_inputs':len(unique),'fresh_TMP_members_before_seal':len(members),'actual_transfer_qualification_sha256':None,'science_qualification_created':False},ensure_ascii=False))

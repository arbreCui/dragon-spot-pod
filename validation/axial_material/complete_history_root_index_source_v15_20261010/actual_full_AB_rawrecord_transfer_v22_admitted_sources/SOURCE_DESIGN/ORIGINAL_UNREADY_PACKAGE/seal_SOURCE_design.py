"""Seal SOURCE-only wrapper design; never load reviewed code or material data."""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat

ROOT=Path(__file__).parent
def pin(p):
 s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:raise ValueError('ordinary SOURCE member required')
 with p.open('rb')as f:
  raw=f.read()
  if f.read(1)!=b'':raise ValueError('full SOURCE EOF required')
 t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 if before!=after or len(raw)!=s.st_size:raise ValueError('SOURCE member changed')
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
checks=json.loads((ROOT/'SOURCE_CHECKS.json').read_text())
actual=json.loads((ROOT/'actual_SOURCE_generation_tool_return.json').read_text());tr=actual['terminal_tool_return']
if actual['closed']is not True or type(tr['exit_code'])is not int or tr['exit_code']!=0 or 'session_id'in tr or tr['chunk_id']!='82881e':raise ValueError('actual closed Source-only EXIT0 required')
printed=json.loads(tr['output'])
if printed['wrapper']!=pin(ROOT/'transfer_full_AB_rawrecord_UNREADY.py')or checks['wrapper']!=printed['wrapper']or checks['blockers']!=[]or checks['all_checks_typed_true']is not True or any(c['value']is not True for c in checks['all_source_checks']):raise ValueError('complete real Source check output required')
names=['transfer_full_AB_rawrecord_UNREADY.py','generate_and_check_SOURCE_design.py','wrapper_before_reader_pin_SOURCE.txt','original_native_records_full.SOURCE.py','original_stream_records_full.SOURCE.py','full_reader_SOURCE_pin_inverse.json','ROOT_BINDING_TEMPLATE.UNREADY.json','COMPLETE_DATA_LAYOUT.json','ROOT_FUTURE_TRUE_STEPS.txt','FUTURE_PROTOCOL_CONTROLS.UNEXECUTED.json','SOURCE_CHECKS.json','actual_SOURCE_generation_tool_return.json','seal_SOURCE_design.py']
if sorted(p.name for p in ROOT.iterdir())!=sorted(names):raise ValueError('whole finite Source inventory required')
members={n:pin(ROOT/n)for n in names}
wrapper=(ROOT/'transfer_full_AB_rawrecord_UNREADY.py').read_text();tree=ast.parse(wrapper)
globalvalues={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
future=['SOURCE_QUALIFICATION_SHA256','ACTUAL_ROOT_BINDING_RECEIPT_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256']
if any(ast.literal_eval(globalvalues[x])is not None for x in future)or ast.literal_eval(globalvalues['SOURCE_STATUS'])!='UNREADY_SOURCE_ONLY_ROOT_TRUE_BINDING_AND_GENUINE_SUPERVISOR_REQUIRED':raise ValueError('unready future pins must remain None')
binding=json.loads((ROOT/'ROOT_BINDING_TEMPLATE.UNREADY.json').read_text())
for p in [*binding['inputs'].values(),binding['python']]:
 if any(p[k]is not None for k in ('sha256','size_bytes','identity')):raise ValueError('unknown actual input/Python pins remain None')
manifest={'schema':'CURRENT150_AB_FULL_RAWRECORD_WRAPPER_COMPLETE_UNREADY_SOURCE_SEAL_V1','status':'SEALED_UNREADY_SOURCE_ONLY_NOT_ACTUAL_TRANSFER_OR_PEER_SCIENTIFIC_ADMISSION','package_path':str(ROOT),'members_excluding_manifest':len(members),'bytes_excluding_manifest':sum(p['size_bytes']for p in members.values()),'files':members,'actual_SOURCE_generation_terminal_chunk':tr['chunk_id'],'actual_SOURCE_generation_typed_integer_exit_code':tr['exit_code'],'actual_SOURCE_generation_closed':True,'Source_checks':len(checks['all_source_checks']),'complete_original_default_reader_sources':checks['complete_original_readers'],'known_reader_SOURCE_pin_complete_2hunk_byte_AST_inverse':True,'both_default_full_readers_no_record_filter':'native_records.decode(raw_bytes); stream_records.decode_stream(binary_iterator), no select/reaction_selection','large_object_lifetime':'full first dict spooled then released before full second dict; second released before next A/B state','all_raw_original_records_header_spans_order_kind_count_padded_bytes_and_decoded_IEEE_bits_preserved_by_design':True,'missing_records_and_multiplicity_semantics_remain_real_gap_no_zero_fill':True,'original_caps':checks['declared_original_caps'],'all_unknown_qualification_success_fields':{x:None for x in future},'all_actual_input_SHA_bytes_7ID_unknown':True,'material_payload_opened':False,'reviewed_wrapper_or_reader_imported_called_or_compiled':False,'business_guard_native_numeric_executed':False,'canonical_or_frozen_namespace_written':False,'actual_transfer_software_qualified':False,'scientific_accuracy_or_neutron_balance_AAA_ABA_qualified':False,'root_actual_genuine_resource_admission_or_terminal_created':False,'RSS_or_time_improvement_predicted':False,'blockers':[]}
with(ROOT/'sealed_SOURCE_manifest.json').open('x')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
for n,before in members.items():
 if pin(ROOT/n)!=before:raise ValueError('sealed Source member changed')
print(json.dumps({'status':manifest['status'],'manifest':pin(ROOT/'sealed_SOURCE_manifest.json'),'members':len(members),'member_bytes':manifest['bytes_excluding_manifest'],'wrapper':checks['wrapper'],'actual_source_generation_exit_code':tr['exit_code'],'Source_checks':manifest['Source_checks'],'actual_parser_payload_business_science_executed':False}))

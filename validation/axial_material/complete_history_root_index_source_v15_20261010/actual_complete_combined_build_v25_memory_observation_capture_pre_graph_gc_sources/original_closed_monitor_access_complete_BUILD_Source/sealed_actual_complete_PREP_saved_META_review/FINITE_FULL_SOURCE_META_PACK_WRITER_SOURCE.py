"""Copy finite full Source and small META proof artifacts; no payload copies."""
import hashlib,json,stat
from pathlib import Path
P=Path('/private/tmp/axmat_v25_monitor_access_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_ORIGINAL_STAGE_STORAGE_20261010')
LATEST=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ORIGINAL_STAGE_JSON_STORAGE_SOURCE_UNREADY_20261010')
INPUT=Path('/private/tmp/spot_v25_monitor_access_actual_COMPLETE_PREP_saved_META_inputs_ROOT_20261010.json')
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def copy(p,q):
 before=pin(p);assert not q.exists();q.write_bytes(p.read_bytes());after=pin(q)
 assert pin(p)==before and (before['sha256'],before['size_bytes'])==(after['sha256'],after['size_bytes'])
 return dict(original=before,saved=after)
r=json.loads((P/'REVIEW.json').read_bytes());assert r['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and r['check_count']==21204 and r['blockers']==[]
assert pin(P/'REVIEW.json')['sha256']=='06e7eb3c329d652bc74e14eaf41fad675b478bc9fdb56f29a08b48c4b3f37e54'
assert pin(INPUT)==r['actual_review_input_contract_pin']
cfg=json.loads(INPUT.read_bytes());assert cfg['actual_terminal_chunks']=={'PREP':'505668','metadata_writer':'af20d1'}
for k in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):assert r[k] is False
source_dir=P/'FULL_SOURCE_HISTORY';meta_dir=P/'FULL_SMALL_META_PROOFS';source_dir.mkdir();meta_dir.mkdir();copies={}
versions={
 'original8843':'/private/tmp/axmat_v25_complete_PREP_saved_META_reviewer_UNREADY_an2zkybe',
 'path_only_e427':'/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_UNREADY_20261010',
 'historical_transfer_e3b_unexecuted':'/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_CURRENT_RETAINED_SOURCE_UNREADY_20261010',
 'historical_transfer80d2':'/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_CURRENT_RETAINED_SOURCE_V2_UNREADY_20261010',
 'receipt_route705_failed946':'/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_RECEIPT_ROUTE_UNREADY_20261010',
 'closed_receipts200_failed245':'/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_CLOSED_RECEIPTS_SOURCE_UNREADY_20261010',
 'original_stage_storage_e860_actual_PASS':str(LATEST)}
for version,directory in versions.items():
 root=Path(directory);dest=source_dir/version;dest.mkdir()
 for src in sorted(root.iterdir()):
  if src.is_file() and (src.suffix=='.py' or src.name.endswith('_INVERSE.json') or src.name.endswith('_TOOL_RETURN.json')):
   copies[version+'/'+src.name]=copy(src,dest/src.name)
copies['executed_reviewer_Source']=copy(LATEST/'review_actual_complete_PREP_saved_META_stdlib.py',P/'REVIEWER_EXECUTED_SOURCE.py')
copies['unchanged_original_sealer_Source']=copy(LATEST/'seal_actual_complete_PREP_saved_META_review_stdlib.py',P/'seal_actual_complete_PREP_saved_META_review_stdlib.py')
assert copies['executed_reviewer_Source']['saved']['sha256']=='e86034b60d272baf2bab03890ccf287c93c0620ddbf0ee288843fff1629a45d5'
assert copies['unchanged_original_sealer_Source']['saved']['sha256']=='6274b7a346809b3e8117bf4f8f2d7ce5febd272dc545f5dfb437a61f477c904c'
copies['actual_18pin_input']=copy(INPUT,P/'ACTUAL_ROOT_18PIN_INPUTS.json')
for key,value in cfg.items():
 if key.startswith('actual_') and type(value) is dict and set(value)=={'path','sha256','size_bytes','identity'}:
  src=Path(value['path']);assert src.suffix in ('.json','.py') and src.name not in ('input_graph.json','input_creation_python_open_trace.json') and pin(src)==value
  copies[key]=copy(src,meta_dir/(key+src.suffix))
for chunk in ('946e8b','2452d6'):
 src=Path('/private/tmp/axmat_v25_monitor_access_actual_saved_PREP_REVIEW_FAILURE_'+chunk)/'ACTUAL_CLOSED_SAVED_REVIEW_FAILURE_TOOL_RETURN.json'
 copies['actual_saved_review_failure_'+chunk]=copy(src,meta_dir/('ACTUAL_SAVED_REVIEW_FAILURE_'+chunk+'.json'))
copies['finite_pack_writer_Source']=copy(Path(__file__),P/'FINITE_FULL_SOURCE_META_PACK_WRITER_SOURCE.py')
with (P/'COMPLETE_FINITE_SOURCE_META_COPIES.json').open('x') as f:json.dump(dict(source_only=True,copies=copies,complete_copies_count=len(copies),all_complete_Source_and_small_META_no_payload_copies=True,new_business_or_science_qualification_created=False),f,indent=2,allow_nan=False);f.write('\n')
for value in copies.values():assert pin(Path(value['original']['path']))==value['original'] and pin(Path(value['saved']['path']))==value['saved']
print(json.dumps(dict(source_only=True,finite_full_Source_META_copies_count=len(copies),actual_report_pin=pin(P/'REVIEW.json'),actual_review_tool_receipt_pin=pin(P/'ACTUAL_SOURCE_META_REVIEW_TOOL_RETURN.json'),all18_actual_inputs_copied_fullbytes=True,no_mother_history_material_native_graph_trace_or_gzip_payload_copied=True)))

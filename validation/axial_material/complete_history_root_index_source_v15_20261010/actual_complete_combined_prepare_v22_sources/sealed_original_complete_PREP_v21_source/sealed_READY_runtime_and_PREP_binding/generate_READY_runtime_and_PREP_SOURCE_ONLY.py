"""Metadata-only actual joint-Q binding into complete runtime and PREP SOURCE.

No project/helper/guard/candidate import or business execution occurs here.
All outputs are fresh private TMP SOURCE; installation and PREP belong to Root.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat

BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
UNREADY_PACKAGE=Path('/private/tmp/axmat_v21_complete_runtime_UNREADY_source_design_20261010')
UNREADY=UNREADY_PACKAGE/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.UNREADY.py'
UNREADY_SHA='75969eafb9e1eead11e25d8838c6e3be13ea64babdc56ee222252a5e11bded62'
UNREADY_MANIFEST_SHA='d11f2dd71e1cc87d85d51345ace6dfa42b727f4065043efa8b44c2db0270f7ce'
HOST_PARENT=BASE/'actual_complete_combined_prepare_v20_sources/combined_prepare_host.py'
HOST_PARENT_SHA='a9d4a1eadae7f6f346138029ea4bbd5e9a5c26c0b5efbb8d256c08b06e757de1'
OLD_Q_READER=BASE/'actual_complete_combined_prepare_v18_sources/sealed_READY_source_binding/source_binding_generator.py'
OLD_Q_READER_SHA='4d54cc988d47918017bdabcf082918bf528cf0ef2a94000a7a082cec68989f0f'
Q_PATH=BASE/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json'
Q_SHA='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'
Q_SCHEMA='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21'
Q_STATUS='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21'
Q_CREATOR_TERMINAL=BASE/'actual_complete_graph_fresh_verifier_v21b_receipts/Root_actual_joint_helper_admission_META_tool_return.json'
HELPER=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
HELPER_SHA='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
HELPER_BYTES=147870
HELPER_ID=[16777229,49380106,33188,1,147870,1791589379138539325,1791589879966481802]
READY_STATUS='READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
FUTURE=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
RETURN_FIELDS=['schema','classification','consumer_scope','consumer_selected_literal_and_canonical_paths','consumer_complete_namespace_root_sequence','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','coverage','trace_coverage','live_io_scope','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','absence_inputs_are_not_regular_bytes_or_science','caller_must_recheck_current_OS_identity_and_live_probe_results','typed_snapshot','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources']
checks=[]
source_inputs={}
ART_references={}

def require(condition,message):
 if type(condition)is not bool or not condition:raise ValueError(message)
 checks.append(dict(name=message,value=True))
def sha(value):return type(value)is str and len(value)==64 and value!='0'*64 and all(c in '0123456789abcdef'for c in value)
def identity(path):
 s=path.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ordinary(path):
 require(path.is_absolute() and '..'not in path.parts,'absolute ordinary SOURCE path')
 for parent in [*reversed(path.parents),path]:
  s=parent.lstat();require(not stat.S_ISLNK(s.st_mode),'SOURCE/META parent has no aliases')
  if parent!=path:require(stat.S_ISDIR(s.st_mode),'normal SOURCE parent directory')
 s=path.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'normal singlelink SOURCE/META file')
def read_source(path,expected_sha=None,expected_identity=None,max_bytes=10*2**20):
 path=Path(path)
 require(not path.is_relative_to(ART),'SOURCE binder never reads ART payload')
 ordinary(path);before=identity(path)
 require(before[4]<=max_bytes,'bounded full SOURCE/META input')
 digest=hashlib.sha256();count=0;blocks=[]
 with path.open('rb')as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   digest.update(block);count+=len(block);blocks.append(block)
 require(identity(path)==before and count==before[4],'full EOF SOURCE/META SHA7ID unchanged')
 actual=dict(path=str(path),sha256=digest.hexdigest(),size_bytes=count,identity=before)
 if expected_sha is not None:require(sha(expected_sha)and actual['sha256']==expected_sha,'exact actual SOURCE/META SHA')
 if expected_identity is not None:require(type(expected_identity)is list and len(expected_identity)==7 and all(type(v)is int for v in expected_identity)and before==expected_identity,'exact integer7 SOURCE/META identity')
 if str(path)in source_inputs:require(source_inputs[str(path)]==actual,'one SOURCE input cannot change between fullreads')
 source_inputs[str(path)]=actual
 return b''.join(blocks),actual
def pairs(items):
 value={}
 for k,v in items:
  require(k not in value,'strict small META duplicatekey rejection');value[k]=v
 return value
def nonfinite(value):raise ValueError('nonfinite small META '+value)
def meta(raw):
 value=json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)
 require(type(value)is dict,'complete small META object')
 return value
def record_pin(record):
 require(type(record)is dict and set(record)=={'path','sha256','size_bytes','identity'},'complete actual Q reference pin fields')
 require(type(record['path'])is str and Path(record['path']).is_absolute()and sha(record['sha256'])and type(record['size_bytes'])is int and record['size_bytes']>=0 and type(record['identity'])is list and len(record['identity'])==7 and all(type(v)is int for v in record['identity'])and record['identity'][4]==record['size_bytes'],'typed whole actual Q pin')
 path=Path(record['path'])
 if path.is_relative_to(ART):
  if str(path)in ART_references:require(ART_references[str(path)]==record,'same complete ART pin must agree')
  ART_references[str(path)]=record
  return None
 raw,actual=read_source(path,record['sha256'],record['identity'])
 require(actual==record,'whole actual Q SOURCE/META reference pin exact')
 return raw
def typed_zero(tr,chunk):
 require(type(tr)is dict and tr.get('chunk_id')==chunk and type(tr.get('exit_code'))is int and tr['exit_code']==0 and 'session_id'not in tr,'actual typed integerzero CLOSED terminal '+chunk)
def actual_terminal(value,schema,initial_chunk,session,final_chunk,pure):
 require(value['schema']==schema and value['closed']is True,'actual recorded closed terminal schema')
 initial=value['initial_tool_return'];last=value['terminal_tool_return']
 require(initial['chunk_id']==initial_chunk and type(initial['session_id'])is int and initial['session_id']==session,'actual initial session/terminal identity')
 typed_zero(last,final_chunk)
 if pure:require(value['session_repolled_after_close']is False,'actual pure session was not repolled')
 else:require(value['no_closed_session_repoll']is True and value['retries']==0 and value['actual_tool_terminal_return_observed']is True,'actual fresh observed zero closed no retry')
def globals_ast(tree):return {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def definitions(raw):
 s=raw.decode();return {n.name:ast.get_source_segment(s,n)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def edit_source(raw,changes,label):
 text=raw.decode();hunks=[]
 for old,new in changes:
  require(type(old)is str and type(new)is str and text.count(old)==1,label+' unique complete finite binding anchor')
  text=text.replace(old,new,1);hunks.append(dict(before=old,after=new))
 restored=text
 for h in reversed(hunks):
  require(restored.count(h['after'])==1,label+' unique complete inverse anchor')
  restored=restored.replace(h['after'],h['before'],1)
 require(restored.encode()==raw,label+' full entirebyte inverse')
 require(ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),label+' full entireAST inverse')
 compile(text,label,'exec') # Standard-library compile only; never execute.
 return text.encode(),hunks
def write_source(path,raw):
 with path.open('xb')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
 return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(path))
def write_json(path,value):return write_source(path,(json.dumps(value,indent=2,allow_nan=False)+'\n').encode())

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--qualification',required=True)
 parser.add_argument('--qualification-sha256',required=True)
 parser.add_argument('--output-dir',required=True)
 args=parser.parse_args()
 require(Path(args.qualification)==Q_PATH and args.qualification_sha256==Q_SHA,'exact Root actual jointQ path/SHA supplied')
 out=Path(args.output_dir)
 require(out.is_absolute()and out.is_relative_to(Path('/private/tmp'))and '..'not in out.parts and not os.path.lexists(out)and out.parent.is_dir()and not out.parent.is_symlink(),'fresh TMP Source-only output no retry')
 qraw,qpin=read_source(Q_PATH,Q_SHA,max_bytes=2*2**20);q=meta(qraw)
 require(len(qraw)==19363 and q['schema']==Q_SCHEMA and q['status']==Q_STATUS,'actual V21 joint Q schema/status/bytes exact')
 require(all(q[key]is False for key in ('supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified')),'newQ has no business native scientific qualification')
 require(q['Root_finite_joint_META_only_no_project_API_or_numeric']is True and type(q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count'])is int and q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count']==151,'actual Root finite joint metadata151input proof')
 fresh=q['complete_current_graph_fresh_verifier']
 pure_refs=['helper','actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest','full_protocol_additional_complete_fixture_artifact','full_protocol_additional_complete_codec_artifact']
 fresh_refs=['actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','sealed_independent_actual_review_manifest','source_manifest','source_binding_record']
 pure_meta={key:record_pin(q[key])for key in pure_refs}
 fresh_meta={key:record_pin(fresh[key])for key in fresh_refs}
 require(set(fresh['complete_gzips'])=={'expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace'},'three complete gzip references no filtering')
 for key,record in fresh['complete_gzips'].items():require(record_pin(record)is None,'gzip payload is bound by actual Q only')
 helper=q['helper'];require(helper['path']==str(HELPER)and helper['sha256']==HELPER_SHA and helper['size_bytes']==HELPER_BYTES and helper['identity']==HELPER_ID,'actual same complete installed dc01 helper Source147870 exact7ID')
 protocol=q['full_protocol']
 require(all(protocol[key]is True for key in ('original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation')),'actual entire original pure protocol true predicates')
 require(type(protocol['accepted_str_subtype_groups'])is int and protocol['accepted_str_subtype_groups']==2 and type(protocol['small_codec_rejections'])is int and protocol['small_codec_rejections']==61,'actual two subtype61 rejection groups')
 counts=protocol['complete_original_graph_counts']
 require(all(type(counts[k])is int and counts[k]==v for k,v in {'read_trace_records':62332,'requirements':237767,'canonical_files':36776}.items())and type(protocol['complete_new_creation_trace_records'])is int and protocol['complete_new_creation_trace_records']==63379 and protocol['complete_new_creation_trace_actual_attempts']==175886,'all actual original wholegraph and newtrace counts')
 caps=dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
 require(q['original_caps']==caps and all(type(q['original_caps'][k])is int for k in caps),'pure original60 caps preserved exactlytyped')
 fm=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_OUT_SOURCE_E_archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
 require(fresh['original_caps']==fm and all(type(fresh['original_caps'][k])is int for k in fm),'fresh complete1800/600 caps preserved separately')
 for scope,whole,stage in ((q,60,60),(fresh,1800,600)):
  measurement=scope['actual_measurement']
  for key,limit in (('whole_seconds',whole),('child_seconds',stage),('sampled_peak_rss_mib',512)):
   require(type(measurement[key])in(int,float)and math.isfinite(measurement[key])and 0<=measurement[key]<limit,'actual measurement below original '+key)
 require(type(q['actual_measurement']['actual_final_host_out_source_bytes'])is int and q['actual_measurement']['actual_final_host_out_source_bytes']<64*2**20,'actual pure joint64 saved size')
 require(fresh['actual_measurement']['sample_and_self_peaks_are_distinct']is True and type(fresh['actual_measurement']['driver_reported_own_peak_rss_mib'])in(int,float)and 0<=fresh['actual_measurement']['driver_reported_own_peak_rss_mib']<512 and type(fresh['actual_measurement']['current_joint_regular_bytes_after_saved_peer_and_copy_receipts'])is int and fresh['actual_measurement']['current_joint_regular_bytes_after_saved_peer_and_copy_receipts']<64*2**20,'actual fresh self/watch distinct and current joint64')
 actual_terminal(meta(pure_meta['actual_root_terminal']),'ROOT_V21_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1','ea406f',49247,'5e1034',True)
 actual_terminal(meta(fresh_meta['actual_root_terminal']),'AXMAT_V21B_ROOT_ACTUAL_COMPLETE_FRESH_VERIFIER_TOOL_TERMINAL_V1','45eca8',38770,'59fbf2',False)
 pure_peer=meta(pure_meta['independent_actual_review']);fresh_peer=meta(fresh_meta['independent_actual_review'])
 require(pure_peer['schema']=='FINITE_V21_ACTUAL_60S_PROTOCOL_SAVED_META_REVIEW_V1'and pure_peer['status']=='ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER'and pure_peer['blockers']==[]and pure_peer['all_explicit_input_SHA7ID_before_after_exact']is True and pure_peer['full_report_original_metadata_and_both_strict_entrances_equal']is True and pure_peer['full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified']is True,'actual original pure saved independent full review')
 require(fresh_peer['schema']=='AXMAT_V21B_ACTUAL_COMPLETE_FRESH_VERIFIER_FINITE_SAVED_META_INDEPENDENT_REVIEW_V1'and fresh_peer['status']=='SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED'and fresh_peer['all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal']is True and fresh_peer['all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal']is True and fresh_peer['complete_expected_actual_JSON_wire_bytes_equal']is True and fresh_peer['one_genuine_stage_PASS']is True and fresh_peer['liveness_group_cleanup']is True and fresh_peer['limit_failure']is None and fresh_peer['retries']==0 and fresh_peer['private_positive_controls']==4 and fresh_peer['private_rejections']==3,'actual complete current fresh saved independent full review')
 pure_tools=meta(pure_meta['independent_actual_review_tool_return']);fresh_tools=meta(fresh_meta['independent_actual_review_tool_return'])
 typed_zero(pure_tools['actual_review_tool_result'],'2eb342');typed_zero(fresh_tools['actual_review_terminal_return'],'45cf76')
 require(fresh_tools['actual_review_closed']is True,'fresh saved peer actual review closed')
 pure_summary=meta(pure_meta['actual_controls_summary']);fresh_summary=meta(fresh_meta['actual_controls_summary'])
 require(pure_summary['closed']is True and pure_summary['actual_original_pure_protocol_pass']is True and pure_summary['installed_helper']=={k:helper[k]for k in ('path','sha256','identity')},'actual pure summary installedhelper identity')
 require(fresh_summary['complete_27_fields_and_nested_type_order_value_floatbits_wire_equal']is True and fresh_summary['complete_Source33_full_EOF_SHA7ID_before_after_unchanged']is True and type(fresh_summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged'])is int and fresh_summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged']==45 and fresh_summary['complete_current_graph_full_EOF_SHA7ID_before_after_unchanged']is True,'actual fresh summary complete Source33/input45/full27/fullgraph proof')
 require(fresh['full_public_return_field_order']==RETURN_FIELDS and fresh['all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal']is True and fresh['complete_actual_unfiltered_read_trace_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True)and fresh['private_positive_controls']==4 and fresh['private_reject_controls']==3 and fresh['SOURCE33_and_all_fixed_inputs_before_after_unchanged']is True and fresh['actual_external_Root_exit0_closed_and_saved_peer_pass']is True,'actual full27/37112/4positive3reject Source33 joint metadata contract')
 expected_meta={'requirement_row_count':238441,'requirement_column_count':5,'canonical_files':37111,'owners':4473,'namespaces':86,'aliases':186,'saved_trace_records':63469,'absence_inputs':479,'closure_categories':9,'scope':'INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION','consumer_scope':None,'newly_declared_input_paths':{},'newly_declared_input_pins':{}}
 require(all(type(fresh['full_current_graph_metadata'][k])is type(v)and fresh['full_current_graph_metadata'][k]==v for k,v in expected_meta.items()),'complete current graph full metadata counts/scope')
 creator_raw,creator_pin=read_source(Q_CREATOR_TERMINAL,max_bytes=2*2**20);creator=meta(creator_raw)
 require(creator['schema']=='ROOT_V21_ACTUAL_JOINT_HELPER_ADMISSION_META_TOOL_RETURN_V1'and creator['closed']is True and creator['Root_META_only']is True and creator['whole_build_INPUT_native_AAA_ABA_physics_qualified']is False,'actual Root joint Q creator closed metadata-only')
 typed_zero(creator['terminal_tool_return'],'7b37a2');observed=meta(creator['terminal_tool_return']['output'])
 require(observed['qualification']==qpin and observed['status']==Q_STATUS and observed['pure_Root_terminal']=='5e1034'and observed['fresh_Root_terminal']=='59fbf2','actual Root Q creation exact integers/pins from original output')
 manifest_raw,manifest_pin=read_source(UNREADY_PACKAGE/'sealed_manifest.json',UNREADY_MANIFEST_SHA);manifest=meta(manifest_raw)
 require(manifest['member_count']==10 and sorted(x.name for x in UNREADY_PACKAGE.iterdir())==sorted([e['relative']for e in manifest['files']]+['sealed_manifest.json']),'whole complete sealed UNREADY package inventory')
 for member in manifest['files']:
  _,pin=read_source(UNREADY_PACKAGE/member['relative'],member['sha256'],member['identity7']);require(pin['size_bytes']==member['size_bytes'],'whole sealed UNREADY member bytes')
 unready,unready_pin=read_source(UNREADY,UNREADY_SHA);parent_host,parent_host_pin=read_source(HOST_PARENT,HOST_PARENT_SHA);oldreader,oldreader_pin=read_source(OLD_Q_READER,OLD_Q_READER_SHA)
 g=globals_ast(ast.parse(unready));require(len(definitions(unready))==70 and all(ast.literal_eval(g[n])is None for n in FUTURE),'all70 original definitions and six future business None')
 doc='READY Source-bound V21 complete sender/root-index full graph private verifier revision. Root actual joint helper Q binds the same dc01 installed helper to two distinct successful bounded trials: the original full60-second producer/codec protocol and complete current-graph fresh verifier, each with its actual closed integer-zero terminal and complete saved independent review. This qualification covers helper metadata protocol and complete input verification only. The approved strict reader last-use change preserves original UTF-8 decoding, JSON hooks and finite-value checks. All original PREP, complete five-stage build, whole INPUT admission, two complete fresh graph/specs phases, full graph/trace, historical seven-key bodies, aliases, namespaces, nine coverage categories, physical inputs, genuine guard/MRO and original budgets remain required. Actual V15 complete86 component INPUT prerequisites remain unchanged. This fresh V21 business family has executed no PREP/build/whole INPUT/native/AAA/ABA or physical validation; all six future business success pins remain None. No Source binding predicts business RSS or future PASS.'
 runtime,runtime_hunks=edit_source(unready,[(unready.decode().splitlines()[0],repr(doc)),("DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_PRIVATE_VERIFIER_FORMAL_FACTORY'","DRAFT_STATUS = "+repr(READY_STATUS)),("'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',None)","'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',"+repr(HELPER_SHA)+')'),('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None','FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = '+repr(Q_SHA))],'complete V21 runtime')
 require(definitions(runtime)==definitions(unready),'all70 runtime functions/classes byteexact to full75969')
 rg=globals_ast(ast.parse(runtime));changed=[n for n in g if ast.dump(g[n],include_attributes=False)!=ast.dump(rg[n],include_attributes=False)]
 require(changed==['DRAFT_STATUS','INPUT_HELPERS','FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'],'only three necessary runtime global AST bindings')
 require(all(ast.literal_eval(rg[n])is None for n in FUTURE),'READY source six future business pins stillNone')
 rsha=hashlib.sha256(runtime).hexdigest()
 old_helper_call="support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6')"
 old_Q_call="support.pin(Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json'),'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8')"
 host_changes=[('axial-material-complete-combined-prepare-host-v20-20261010','axial-material-complete-combined-prepare-host-v21-20261010'),('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py'),('566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3',rsha),('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010'),('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'),('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010'),('actual_complete_combined_prepare_v20_sources','actual_complete_combined_prepare_v21_sources'),('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V20_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_DECLARATION_V1'),('AXMAT_V20_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V21_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1'),(old_helper_call,'support.pin(Path('+repr(str(HELPER))+'),'+repr(HELPER_SHA)+')'),(old_Q_call,'support.pin(Path('+repr(str(Q_PATH))+'),'+repr(Q_SHA)+')')]
 host,host_hunks=edit_source(parent_host,host_changes,'complete genuine PREP host')
 require(len(runtime_hunks)==4 and len(host_hunks)==11,'exact4runtime11host finite hunks')
 require(len(definitions(host))==len(definitions(parent_host))==1,'original complete PREP main function retained')
 for sourcepin in list(source_inputs.values()):
  _,after=read_source(Path(sourcepin['path']),sourcepin['sha256'],sourcepin['identity']);require(after==sourcepin,'all fullSOURCE Qmeta inputs unchanged after binding')
 out.mkdir(mode=0o700)
 runtime_pin=write_source(out/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py',runtime)
 host_pin=write_source(out/'combined_prepare_host.py',host)
 write_source(out/'UNREADY_parent_exact_source.txt',unready)
 write_source(out/'genuine_PREP_parent_exact_source.txt',parent_host)
 write_source(out/'original_READY_Q_reader_exact_SOURCE.txt',oldreader)
 write_source(out/'actual_joint_Q_exact_METADATA_copy.json',qraw)
 proof=dict(schema='AXMAT_V21_ACTUAL_JOINT_Q_READY_RUNTIME_AND_PREP_FULL_INVERSE_V1',status='SOURCE_READY_UNINSTALLED_NOT_EXECUTED',runtime=runtime_pin,host=host_pin,unready_parent=unready_pin,genuine_host_parent=parent_host_pin,actual_joint_Q=qpin,actual_joint_Q_creator_tool_record=creator_pin,actual_helper=helper,original_READY_Q_reader_SOURCE=oldreader_pin,runtime_ordered_hunks=runtime_hunks,host_ordered_hunks=host_hunks,full_runtime_byte_AST_inverse_to75969=True,all70runtime_definitions_byteexact=True,full_host_byte_AST_inverse_to_a9d4=True,complete11host_namespace_SHA_helperQretargets_only=True,all_other_runtime_globals_and_all_physics_inputs_caps_whole_payloads_unchanged=True,all_SOURCE_Q_meta_references_full_EOF_SHA7ID_before_after=list(source_inputs.values()),ART_references_bound_by_actual_Q_only_never_read=list(ART_references.values()),source_archive_all_actual_members_dynamically_retained=True,Source37_old_and46input_shape_are_not_truncation_limits=True,original_five_build_stages_and_two_complete_graph_specs_phases_retained=True,future_business_six_pins={name:None for name in FUTURE},actual_helper_joint_metadata_qualified=True,new_business_PREP_build_INPUT_native_AAA_ABA_physics_qualified=False,installed=False,business_API_guard_helper_called=False,current_ART_graph_numeric_or_history_read=False)
 proof_pin=write_json(out/'full_READY_runtime_and_genuine_PREP_SOURCE_inverse.json',proof)
 report=dict(schema='AXMAT_V21_ACTUAL_JOINT_Q_SOURCE_READY_BINDING_REPORT_V1',status='SOURCE_READY_UNINSTALLED_ROOT_SOURCE_REVIEW_AND_ONE_FRESH_PREP_REQUIRED',runtime=runtime_pin,host=host_pin,proof=proof_pin,qualification=qpin,actual_pure_terminal='5e1034',actual_fresh_terminal='59fbf2',actual_Q_META_creator_terminal='7b37a2',canonical_four_bindings_only=True,genuine_host_eleven_atomic_bindings_only=True,all70runtime_function_class_bodies_unchanged=True,original_limits=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_SOURCE_OUT_SOURCEarchive_bytes=2*2**30,wholeINPUT_metadata_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0),checks=checks,all_checks_typed_true=True,actual_helper_metadata_protocol_and_freshverifier_only=True,future_business_six_pins={name:None for name in FUTURE},source_compile_only=True,installed=False,business_executed=False,helper_or_guard_API_called=False,ART_payload_read=False)
 report_pin=write_json(out/'SOURCE_REPORT.json',report)
 members=[]
 for path in sorted(out.iterdir()):
  raw=path.read_bytes();members.append(dict(relative=path.name,path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(path)))
 manifest_pin=write_json(out/'generated_SOURCE_manifest.json',dict(schema='AXMAT_V21_GENERATED_READY_RUNTIME_PREP_SOURCE_MANIFEST_V1',status='SOURCE_READY_UNINSTALLED_NO_BUSINESS',source_only=True,members=members,member_count=len(members),runtime=runtime_pin,host=host_pin,qualification=qpin,all70definitions_exact=True,future_business_six_pins={name:None for name in FUTURE},installed=False,business_executed=False,ART_payload_read=False))
 print(json.dumps(dict(status=report['status'],runtime=runtime_pin,host=host_pin,manifest=manifest_pin,proof=proof_pin,report=report_pin,checks=len(checks),SOURCE_only=True,installed=False,helper_or_guard_API_called=False,ART_payload_read=False),allow_nan=False))

if __name__=='__main__':main()

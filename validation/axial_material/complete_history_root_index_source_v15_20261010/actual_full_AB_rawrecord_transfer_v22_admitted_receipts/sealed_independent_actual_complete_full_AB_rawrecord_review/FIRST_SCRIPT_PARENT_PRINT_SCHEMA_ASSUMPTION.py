#!/usr/bin/env python3
"""Saved complete fresh verifier Source/META audit; no helper/guard/driver execution."""
import ast
import collections
import gzip
import hashlib
import json
import os
import pathlib
import stat
import struct
import sys

HERE=pathlib.Path(__file__).parent
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_full_AB_rawrecord_transfer_v22_admitted_sources'
E=B/'actual_full_AB_rawrecord_transfer_v22_admitted_receipts'
H=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-current150-AB-full-rawrecord-transfer-host-v22-20261010')
O=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-current150-AB-full-rawrecord-transfer-v22-20261010')
CHECKS=[];READS=[]
def check(name,ok,details=None):
 row={'check':name,'PASS':bool(ok)}
 if details is not None:row['details']=details
 CHECKS.append(row)
def id7(p):
 s=pathlib.Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full_pin(path,expected=None,sha=None):
 p=pathlib.Path(path);before=id7(p);check('regular single-link finite Source/META '+str(p),stat.S_ISREG(before[2]) and before[3]==1)
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk);n+=len(chunk)
  s=os.fstat(f.fileno());check('descriptor stable through full EOF '+str(p),[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before)
 actual={'path':str(p),'sha256':h.hexdigest(),'identity':id7(p),'size_bytes':n}
 check('full EOF byte count and7ID stable '+str(p),actual['identity']==before and n==before[4])
 if expected is not None:
  check('exact saved full SHA7ID '+str(p),all(actual[k]==expected[k] for k in ('path','sha256','identity')))
  if 'size_bytes'in expected:check('explicit saved full size '+str(p),actual['size_bytes']==expected['size_bytes'])
 if sha is not None:check('Root exact terminal/META SHA '+str(p),actual['sha256']==sha)
 READS.append(actual);return actual
def meta(p,limit=8*1024*1024):
 p=pathlib.Path(p);check('bounded explicit saved META decode '+str(p),p.stat().st_size<=limit)
 if p.stat().st_size>limit:raise ValueError('META too large for decoding')
 return json.loads(p.read_bytes())
def norm(p):return {k:p[k] for k in ('path','sha256','identity')}
def value_signature(v):
 t=type(v)
 if t is dict:return ['dict',[[value_signature(k),value_signature(x)] for k,x in v.items()]]
 if t is list:return ['list',[value_signature(x) for x in v]]
 if t is float:return ['float',struct.pack('>d',v).hex()]
 return [t.__name__,v]
def exact(a,b):return value_signature(a)==value_signature(b)
def stage_signature(v):
 if type(v)is dict:return ['dict',[[stage_signature(k),stage_signature(v[k])]for k in sorted(v)]]
 if type(v)is list:return ['list',[stage_signature(x)for x in v]]
 return value_signature(v)
def tree(root):
 files={};dirs={};links={};root=pathlib.Path(root)
 for current,ds,fs in os.walk(root,followlinks=False):
  current=pathlib.Path(current);dirs[current.relative_to(root).as_posix()]=id7(current)
  for name in ds[:]:
   p=current/name
   if p.is_symlink():links[p.relative_to(root).as_posix()]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)};ds.remove(name)
  for name in fs:
   p=current/name;relative=p.relative_to(root).as_posix()
   if p.is_symlink():links[relative]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)}
   else:files[relative]=id7(p)
 return files,dirs,links

def no_duplicate_pairs(pairs):
 result={}
 for key,value in pairs:
  if key in result:raise ValueError('duplicate saved META key '+key)
  result[key]=value
 return result
def strict_json(raw):
 return json.loads(raw,object_pairs_hook=no_duplicate_pairs,parse_constant=lambda text:(_ for _ in ()).throw(ValueError('nonfinite '+text)))
def meta(p,limit=8*1024*1024):
 p=pathlib.Path(p);check('bounded explicit saved META decode '+str(p),p.stat().st_size<=limit)
 if p.stat().st_size>limit:raise ValueError('META too large for decoding')
 return strict_json(p.read_bytes())
def gzip_meta(pin):
 full_pin(pin['path'],pin);h=hashlib.sha256();chunks=[];n=0
 with gzip.open(pin['path'],'rb') as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk);n+=len(chunk)
   if n>67108864:raise ValueError('saved META gzip exceeds original64MiB')
   chunks.append(chunk)
 raw=b''.join(chunks)
 check('complete gzip CRC/decompression EOF rawJSON bytes SHA '+pin['path'],n==pin['uncompressed_JSON_bytes'] and h.hexdigest()==pin['uncompressed_JSON_sha256'] and pin['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and pin['no_fields_or_records_filtered']is True)
 return strict_json(raw),raw

C=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-current150-AB-full-rawrecord-protocol-v22-20261010')
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2147483648,'history_bytes':103079215104,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
terminal_pin=full_pin(E/'Root_actual_full_rawrecord_tool_terminal_return.json',sha='9c99c9b5edbc98fa350d34a5fa1a8020c608176e6d9191d16401e65e01168f5d')
summary_pin=full_pin(E/'Root_actual_full_AB_rawrecord_summary.json',sha='987a6f38240bddc3f1f96fa5c0a412fde222d7ee293f655f5abd5bc2ff01e773')
manifest_pin=full_pin(E/'Root_actual_complete_full_rawrecord_namespace_manifest.json',sha='5d59a2af91ee31d92295fa96fab8420747bcd184266d9c2ea8d9cd4597cba551')
terminal=meta(terminal_pin['path']);summary=meta(summary_pin['path']);manifest=meta(manifest_pin['path']);t=terminal['terminal_tool_return']
check('genuine Root8bdd07 strictint0 closed43424 no retry/repoll',terminal['schema']=='ROOT_V22_ACTUAL_FULL_AB_RAWRECORD_HOST_TOOL_TERMINAL_RETURN_V1' and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='8bdd07' and 'session_id'not in t and terminal['closed']is True and terminal['actual_tool_terminal_return_observed']is True and terminal['initial_tool_return']['session_id']==43424 and terminal['initial_tool_return']['chunk_id']=='5eadf3' and terminal['observations'][-1]==t and terminal['session_repolled_after_close']is False and terminal['retries']==0 and terminal['business_full_rawrecord_wrapper_and_two_readers_executed']is True and terminal['transport_numeric_or_native_engines_executed']is False)
check('Root complete actual summary exact realterminal and manifest pins',summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_SUMMARY_V1' and summary['status']=='ACTUAL_FULL_AB_RAW_SOFTWARE_TRANSFER_EXIT0_CLOSED_INDEPENDENT_SAVED_REVIEW_REQUIRED' and type(summary['actual_exit_code'])is int and summary['actual_exit_code']==0 and summary['closed']is True and summary['Root_terminal_chunk']=='8bdd07' and norm(summary['actual_tool_terminal'])==norm(terminal_pin) and norm(summary['complete_namespace_manifest'])==norm(manifest_pin))
check('complete original5 finite namespaces D E H O C',manifest['schema']=='ROOT_V22_ACTUAL_COMPLETE_RAWRECORD_FINITE_NAMESPACES_V1' and set(manifest['complete_namespaces'])=={'D','E_pre_summary','H','O','C'})
snapshots=[];current_joint=0;captured_joint=0
later_E={'Root_actual_full_AB_rawrecord_summary.json','Root_actual_complete_full_rawrecord_namespace_manifest.json','Root_actual_full_rawrecord_postclose_META_tool_terminal_return.json'}
postclose_meta_pin=full_pin(E/'Root_actual_full_rawrecord_postclose_META_tool_terminal_return.json',sha='ef1f61cac9d8a47ef96f83020ab873a5312c1967cd0f2c1a2349d45e6b18170f')
for label,ns in manifest['complete_namespaces'].items():
 root=pathlib.Path(ns['root']);files,dirs,links=tree(root)
 check(label+' exact literal root',root=={'D':D,'E_pre_summary':E,'H':H,'O':O,'C':C}[label])
 check(label+' all hidden/regular members retained no crop/symlink',set(files)==set(ns['files'])|(later_E if label=='E_pre_summary' else set()) and set(dirs)==set(ns['directories']) and links=={})
 check(label+' complete saved counts',ns['file_count']==len(ns['files']) and ns['directory_count']==len(ns['directories']))
 for rel,pin in ns['files'].items():
  check(label+' full literal rooted file '+rel,pathlib.Path(pin['path'])==root/rel);full_pin(pin['path'],pin)
 for rel,identity in ns['directories'].items():
  if label=='E_pre_summary' and rel=='.':check('Eroot exact append boundary not immutable forever',dirs[rel]!=identity and dirs[rel][:3]==identity[:3],{'captured_pre_summary':identity,'current_after_summary_manifest':dirs[rel]})
  else:check(label+' full directory7ID unchanged '+rel,dirs[rel]==identity)
 current_joint+=sum(x[4]for x in files.values());captured_joint+=sum(x['identity'][4]for x in ns['files'].values())
 snapshots.append({'label':label,'root':str(root),'complete_regular_file_names':sorted(files),'directories':dirs,'symlinks':links,'file_count':len(files),'directory_count':len(dirs)})
check('all full original namespace membercounts unchanged D173/15 Epre5 H7/5 O16/3 C7/1',[(manifest['complete_namespaces'][k]['file_count'],manifest['complete_namespaces'][k]['directory_count'])for k in ('D','E_pre_summary','H','O','C')]==[(173,15),(5,1),(7,5),(16,3),(7,1)])
freeze=meta(summary['source_freeze']['path']);full_pin(summary['source_freeze']['path'],summary['source_freeze'],sha='fc67e4abf96ae1063b18fda30b032310e073e97dfe656082a418fc270ce2a007')
check('original complete D173files15dirs fullfreeze exact no append',freeze['schema']=='ROOT_V22_FINAL_FULL_RAWRECORD_SOURCE_FREEZE_PREFLIGHT_V1' and freeze['file_count']==173 and freeze['directory_count']==15 and freeze['complete_files']==manifest['complete_namespaces']['D']['files'] and freeze['complete_directories']==manifest['complete_namespaces']['D']['directories'] and freeze['no_Source_append_after_this_freeze']is True and summary['D173_files_15_directories_unchanged']is True and all(freeze[k]is True for k in ('complete_original_derivative_SOURCE119_unfiltered','complete_independent_new_SOURCE_review12_retained','complete_Root_metadata_writer_SOURCE19_retained','complete_actual_admissions4_retained','complete_all_binding_input_pins_full_EOF_SHA7ID_unchanged','ready_wrapper_protocol_host_full_bytes_inverse_and_all_function_AST_original')))
host=meta(H/'result.json');protocol=meta(C/'ACTUAL_PROTOCOL_REPORT.json');transfer=meta(O/'ACTUAL_TRANSFER_REPORT.json');payload_manifest=meta(O/'complete_payload_manifest.json');parent=meta(E/'parent_stdout.log');stages=meta(H/'FULL_RAWRECORD_TRANSFER/stages.json')
for key in ('actual_host_result','actual_protocol_report','actual_transfer_report','actual_parent_stdout','actual_parent_stderr'):full_pin(summary[key]['path'],summary[key])
check('normal genuine actual host schema PID and externalrequired',host['schema']=='CURRENT150_AB_GENUINE_COMPLETE_RAWRECORD_TRANSFER_HOST_V1' and host['status']=='ACTUAL_SAVED_COMPLETE_SOFTWARE_TRANSFER_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED' and type(host['actual_host_PID'])is int and host['actual_host_PID']==16128 and host['actual_software_payload_saved']is True and host['external_actual_Root_typed_EXIT0_CLOSED_required']is True)
check('full original protocol and transfer report schema scopes',protocol['schema']=='CURRENT150_AB_ACTUAL_COMPLETE_RAWRECORD_PROTOCOL_CONTROLS_V1' and protocol['status']=='ACTUAL_FULL_SMALL_PROTOCOL_CONTROLS_ONLY_EXTERNAL_GENUINE_ROOT_CLOSURE_REQUIRED' and transfer['schema']=='CURRENT150_AB_ACTUAL_FULL_RAWRECORD_SOFTWARE_TRANSFER_REPORT_V1' and transfer['status']=='ACTUAL_COMPLETE_TWO_READER_RAW_TRANSFER_ONLY_SCIENTIFIC_INPUT_NOT_ADMITTED' and transfer['actual_full_raw_and_typed_two_reader_transfer_complete']is True and transfer['all_both_reader_records_default_retained']is True)
check('parent finalprint pinned result/protocol/transfer without forgedstartup unchanged',norm(parent['actual_host_result'])==norm(summary['actual_host_result']) and norm(parent['actual_protocol_report'])==norm(summary['actual_protocol_report']) and norm(parent['actual_transfer_report'])==norm(summary['actual_transfer_report']))
startup=summary['original_parent_stdout_startup_pin'];current_stdout=summary['actual_parent_stdout']
check('original empty stdout startup is historical changed only samefile finalprint',startup['path']==current_stdout['path']==str(E/'parent_stdout.log') and startup['sha256']=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' and startup['identity'][4]==0 and current_stdout['identity'][4]==918 and startup['identity'][:4]==current_stdout['identity'][:4] and startup['identity']!=current_stdout['identity'] and manifest['original_parent_stdout_startup_pin']==startup and norm(manifest['actual_parent_stdout_postprint'])==norm(current_stdout) and summary['all_host_input_pins_postclose_exact_except_original_parent_stdout_after_final_print']is True)
check('all268 original ordered hostpins retain exact originalstdout exception',len(host['input_sources'])==268 and sum(x['path']==str(E/'parent_stdout.log')for x in host['input_sources'])==1)
for i,pin in enumerate(host['input_sources']):
 if pin['path']==str(E/'parent_stdout.log'):check('original host startup stdout pin matches exact historicalMETA',pin==startup)
 else:full_pin(pin['path'],pin)
for pin in [host['original_helper'],host['resource_factory']]+host['genuine_guard_sources']:full_pin(pin['path'],pin)
binding=meta(D/'Root_actual_rawrecord_SOURCE_binding.json');inverse=meta(D/'READY_SOURCE_binding_inverse.json')
check('actual Source binding/schema two full API defaults no filtering',binding['schema']=='ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1' and binding['source_only']is True and binding['public_reader_calls']==['native_records.decode(raw_bytes)','stream_records.decode_stream(binary_iterator)'] and binding['full_default_retention']is True and binding['namespaces']=={'source':str(D),'receipts':str(E),'host':str(H),'transfer':str(O),'protocol':str(C)} and len(binding['input_pins'])==90)
for pin in binding['input_pins']:full_pin(pin['path'],pin)
check('both original complete readers fullEOF current sourcepins',binding['readers']['native_records']['sha256']=='67fe414c25f5867e80cc0509c9951522253e572b92998c83c6b32a254c59342b' and binding['readers']['stream_records']['sha256']=='dc2d4e5f6cfa6b6d312669f44db98df5873d049707672bb166b26719fad2df0f')
for pin in binding['readers'].values():full_pin(pin['path'],pin);ast.parse(pathlib.Path(pin['path']).read_bytes())
source_originals={'ready_wrapper':D/'SOURCE_DESIGN/ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py','ready_protocol':D/'SOURCE_DESIGN/full_rawrecord_protocol_controls_UNREADY.py','ready_genuine_host':D/'SOURCE_DESIGN/full_AB_rawrecord_genuine_host_UNREADY.py'}
for key,hunks_key in [('ready_wrapper','wrapper_three_global_hunks'),('ready_protocol','protocol_one_status_hunk'),('ready_genuine_host','host_global_only_hunks')]:
 ready=pathlib.Path(inverse[key]['path']).read_bytes();original=source_originals[key].read_bytes();restored=ready
 for old,new in inverse[hunks_key]:
  check('only one complete Sourceinverse global hunk '+key+' '+old.split('=')[0],restored.count(new.encode())==1);restored=restored.replace(new.encode(),old.encode(),1)
 check(key+' full bytes inverse exact original EOF',restored==original)
 ready_ast=ast.parse(ready);original_ast=ast.parse(original)
 check(key+' all original function/class complete AST unchanged',[(x.name,ast.dump(x,include_attributes=False))for x in ready_ast.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]==[(x.name,ast.dump(x,include_attributes=False))for x in original_ast.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))])
check('original wrapper098 fullSHA provenance unchanged',hashlib.sha256(source_originals['ready_wrapper'].read_bytes()).hexdigest()=='098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116' and inverse['all_actual_success_pins_remain_None']is True)
wrapper_source=pathlib.Path(inverse['ready_wrapper']['path']).read_text();host_source=pathlib.Path(inverse['ready_genuine_host']['path']).read_text()
for snippet in ['records = first_reader.decode(raw)','del records','second_records, second_stats = second_reader.decode_stream(binary_lines)','del first_reader,second_reader']:
 check('original full retention sequential ownership Source '+snippet,snippet in wrapper_source)
for snippet in ['helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','Path(full.__file__).resolve()!=support.FULL','Path(production.__file__).resolve()!=support.PARENT','resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)','type(runner) is not full.OwnRSSSerialExecutor','joint_paths=(host,out,control,archive,receipts)']:
 check('original genuine guard MRO full archive roots source '+snippet,snippet in host_source)
check('both exact monitored stage rows all values floatbits listorder independent serializer',stage_signature(host['stage_records'])==stage_signature(stages['stages']) and [x['label']for x in host['stage_records']]==['protocol_run/protocol','transfer_run/transfer'] and all(x['status']=='PASS'for x in host['stage_records']))
watches={}
for kind,child_report,expected_pid in [('protocol',protocol,16142),('transfer',transfer,16147)]:
 receipt=host['actual_'+kind];watch=meta(receipt['watchdog_file']['path']);stdout=meta(receipt['actual_merged_child_stdout_and_stderr']['path']);watches[kind]=watch
 full_pin(receipt['watchdog_file']['path'],receipt['watchdog_file']);full_pin(receipt['actual_merged_child_stdout_and_stderr']['path'],receipt['actual_merged_child_stdout_and_stderr'])
 check(kind+' complete Rootreceipt same genuine host values',exact(receipt,summary['actual_'+kind]) and norm(receipt['report'])==norm(summary['actual_'+kind+'_report']))
 check(kind+' real watch strictint0 ownchild no limits cleanup PID',exact(watch,receipt['watchdog']) and type(watch['returncode'])is int and watch['returncode']==0 and type(watch['pid'])is int and watch['pid']==expected_pid==child_report['actual_child_PID'] and child_report['actual_parent_PID']==host['actual_host_PID']==16128 and watch['command']==receipt['command'] and watch['rss_cap_mib']==512 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and receipt['actual_child_PID_equals_watch_PID']is True and receipt['actual_parent_PID_equals_host_PID']is True and receipt['child_separate_stderr_saved']is False)
 check(kind+' exact original prefixed stage command/report/log integrity',receipt['label']==kind and receipt['command']==host['stage_records'][0 if kind=='protocol'else 1]['command'] and receipt['actual_merged_child_stdout_and_stderr']['sha256']==host['stage_records'][0 if kind=='protocol'else 1]['log_sha256'] and norm(stdout['report'])==norm(receipt['report']))
 check(kind+' all time wallcap checks unchanged',0<child_report['child_seconds']<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and host['stage_records'][0 if kind=='protocol'else 1]['wall_cap_seconds']==600)
check('true transient missing protocol sample not zero actualmemory',watches['protocol']['sampled_peak_rss_mib']==summary['protocol_sampled_peak_rss_mib']==0.0 and summary['protocol_sampled_zero_is_not_proof_of_zero_actual_memory']is True and watches['protocol']['elapsed_seconds']==0.4329463749891147)
check('true transfer270.8125MiB/7.078265s host9.939067s allunder',watches['transfer']['sampled_peak_rss_mib']==summary['transfer_sampled_peak_rss_mib']==270.8125 and watches['transfer']['elapsed_seconds']==7.078265291987918 and host['whole_seconds']==summary['whole_seconds']==9.93906679097563 and host['whole_seconds']<1800 and watches['transfer']['sampled_peak_rss_mib']<512)
check('all original resource caps complete exact',all(exact(x,CAPS)for x in (summary['original_caps'],host['original_caps'],freeze['original_caps'],binding['original_caps'],protocol['original_caps'],transfer['declared_original_caps'])) and host['threads']==host['children_at_once']==1 and host['retries']==0 and host['profile_used']is False and host['supervisor_class_or_MRO_modified']is False)
for key in ('resources_before','resources_between','resources_after'):
 row=host[key];check('full original declaredhistory/free metadata '+key,row['min_free_bytes']==8589934592 and row['artifact_budget_bytes']==103079215104 and row['artifact_bytes']<103079215104 and row['disk_free_bytes']>=8589934592 and row['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and all(str(x)in row['declared_resource_roots']for x in (H,O,C)))
check('full H O C D E original2GiB archive scope capture/current honest',host['archive_roots']==[str(x)for x in (H,O,C,D,E)] and captured_joint==manifest['joint_bytes_at_capture']==summary['joint_bytes_at_namespace_capture']==184045088 and current_joint==captured_joint+summary_pin['size_bytes']+manifest_pin['size_bytes']+postclose_meta_pin['size_bytes'] and current_joint<2147483648 and host['archive_before_result_bytes']+summary['actual_host_result']['identity'][4]<captured_joint and host['source_and_receipts_outsideART_counted_separately']is True,{'captured_before_summary_manifest_bytes':captured_joint,'current_after_summary_manifest_METAreceipt_bytes':current_joint,'host_postresult_before_new_terminal_bytes':host['archive_before_result_bytes']+summary['actual_host_result']['identity'][4]})
check('real Source Root launch all singlethread settings',str(D/'full_AB_rawrecord_genuine_host_READY.py')in terminal['actual_arguments']['cmd'] and all(x+'=1'in terminal['actual_arguments']['cmd']for x in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')))
check('complete5positive10negative scope retained',protocol['positive_count']==len(protocol['complete_positive_controls'])==5 and protocol['negative_count']==len(protocol['complete_negative_controls'])==10 and all(x['actual_control_passed']is True for x in protocol['complete_positive_controls']))
for row in protocol['complete_negative_controls']:
 if 'actual_observed_errors'in row:check('both independent actual reader reject '+row['name'],row['both_full_readers_rejected']is True and [x['reader']for x in row['actual_observed_errors']]==['native_default','stream_default'] and len(row['actual_observed_errors'])==2 and all(x['error_type']=='ValueError'and type(x['error'])is str for x in row['actual_observed_errors']))
 else:check('actual complete typed negative '+row['name'],row['observed_rejection']is True and type(row['error'])is str)
check('protocol negative exact10 distinct cases no omissions',[x['name']for x in protocol['complete_negative_controls']]==['duplicate full record key','truncated final numeric payload','nonfinite real payload','missing terminal root close','wrong raw character width','truncated raw character payload','truncated malformed full header','REAL32 overflow or nonfinite resulting cast rejected, finite ordinary rounding allowed','key order mutation rejected','signed zero parser/REAL64 bit mutation rejected'])
check('complete payload manifest14 statefiles no omissions',payload_manifest['schema']=='CURRENT150_AB_FULL_RAWRECORD_PAYLOAD_MANIFEST_V1' and len(payload_manifest['files'])==14 and set(payload_manifest['files'])=={state+'/'+name for state in ('A','B')for name in ('complete_raw_header_span_inventory.jsonl','complete_typed_record_index.jsonl','complete_typed_payload.bin','full_required_field_contract.jsonl','full_sparse_reference_spans.jsonl','original_macro.ascii','small_state_metadata.json')} and payload_manifest['complete_RAW_TYPED_contract_and_sparse_payload_retained']is True and payload_manifest['all_raw_original_inputs_unchanged']is True)
for rel,pin in payload_manifest['files'].items():check('payload full literal relative file '+rel,pathlib.Path(pin['path'])==O/rel);full_pin(pin['path'],pin)
def jsonl(path):
 rows=[]
 with pathlib.Path(path).open('rb')as f:
  for line in f:
   if not line.endswith(b'\n'):raise ValueError('JSONL missing final newline')
   rows.append(strict_json(line))
 return rows
def span_sha(f,begin,end):
 if type(begin)is not int or type(end)is not int or begin<0 or end<begin:raise ValueError('invalid exact span')
 f.seek(begin);left=end-begin;h=hashlib.sha256()
 while left:
  data=f.read(min(left,1048576))
  if not data:raise ValueError('truncated raw/binary savedspan')
  left-=len(data);h.update(data)
 return h.hexdigest()
def audit_index(root,indexname,headername,payloadname,rawname,record_count,header_count,numeric_count):
 index=jsonl(root/indexname);headers=jsonl(root/headername);kinds=collections.Counter(x['kind']for x in index)
 check(str(root)+' complete record/physicalheader/numeric counts all strictorder',len(index)==record_count and len(headers)==header_count and [x['record_index']for x in index]==list(range(record_count)) and [x['physical_header_index']for x in headers]==list(range(header_count)) and sum(x['declared_count']for x in index if x['kind']in (1,2,4))==numeric_count)
 record_headers=[x for x in headers if x['entry']=='record'];closes=[x for x in headers if x['entry']=='close']
 check(str(root)+' every physical header closes contiguous fullASCII bytes no gap',len(record_headers)==record_count and len(closes)==header_count-record_count and headers[0]['raw_begin_byte']==0 and headers[-1]['raw_end_byte']==(root/rawname).stat().st_size and headers[-1]['entry']=='close' and headers[-1]['level']==-1 and all(headers[i]['raw_end_byte']==headers[i+1]['raw_begin_byte']for i in range(header_count-1)))
 check(str(root)+' all record path/key types kinds flags counts originalheader exact',all(x['entry']=='record'and len(x['path'])==len(x['path_types'])and all(type(v)is (str if t=='str'else int)for v,t in zip(x['path'],x['path_types']))and all(type(x[k])is int for k in ('record_index','physical_header_index','level','flags','kind','declared_count'))and all(x[k]==h[k]for k in h)for x,h in zip(index,record_headers)) and len({tuple((type(v).__name__,v)for v in x['path'])for x in index})==record_count)
 raw_bad=[];typed_bad=[]
 with(root/rawname).open('rb')as rawf,(root/payloadname).open('rb')as payloadf:
  check(str(root)+' original24byte typed magic header exact',payloadf.read(24)==b'AXMAT_FULL_TYPED_LCM_V1\x00')
  for i,row in enumerate(headers):
   if span_sha(rawf,row['raw_begin_byte'],row['raw_end_byte'])!=row['raw_span_sha256']:raw_bad.append(i)
  for i,row in enumerate(index):
   if span_sha(payloadf,row['typed_payload_begin_byte'],row['typed_payload_end_byte'])!=row['typed_payload_sha256']:typed_bad.append(i)
 check(str(root)+' every raw span/header includingcloses fullbyte SHA exact',not raw_bad,{'all_headers_verified':len(headers),'mismatch_indices':raw_bad})
 check(str(root)+' every full typed payload span byte SHA exact no decoding',not typed_bad and index[0]['typed_payload_begin_byte']==24 and index[-1]['typed_payload_end_byte']==(root/payloadname).stat().st_size and all(index[i]['typed_payload_end_byte']==index[i+1]['typed_payload_begin_byte']for i in range(record_count-1)),{'all_record_spans_verified':len(index),'mismatch_indices':typed_bad})
 encodings={0:'directory_count_in_header',10:'list_count_in_header',99:'empty_in_header',1:'exact_signed_decimal_integer_lines',2:'little_endian_IEEE_float32_plus_parser_float64_per_value',3:'ASCII_decoded_character_with_original_padding_in_raw_span',4:'little_endian_IEEE_float64'}
 check(str(root)+' all numeric bit widths32plusparser64 and64 separate recordencodings',all(x['payload_encoding']==encodings[x['kind']]and (x['typed_payload_end_byte']-x['typed_payload_begin_byte']==x['declared_count']*(12 if x['kind']==2 else 8)if x['kind']in (2,4)else True)and (x['typed_payload_end_byte']==x['typed_payload_begin_byte']if x['kind']in (0,10,99)else True)for x in index))
 return {'records':record_count,'physical_headers_including_closes':header_count,'numeric_values':numeric_count,'kind_counts':dict(kinds),'close_count':len(closes),'all_raw_span_SHA_verified':True,'all_typed_span_SHA_verified':True,'all_complete_path_type_order_sequence_sha256':hashlib.sha256(json.dumps([(x['path'],x['path_types'],x['kind'],x['declared_count'])for x in index],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()},index
state_evidence=[]
for state in ('A','B'):
 root=O/state;small=meta(root/'small_state_metadata.json');evidence,index=audit_index(root,'complete_typed_record_index.jsonl','complete_raw_header_span_inventory.jsonl','complete_typed_payload.bin','original_macro.ascii',19619,19990,2264113)
 check(state+' fullsmall metadata count/result/defaultreader complete',small['state']==state and small['full_inventory']=={'records':19619,'physical_headers_including_closes':19990,'numeric_values':2264113,'full_original_raw_byte_interval_coverage':True} and small['independent_full_reader_comparison']=={'all_records':19619,'all_paths_types_order_values_floatbits_equal':True,'all_stream_records_retained':True,'full_first_payload_compared_byteexact':True,'complete_stream_statistics':{'lines':498494,'all_records_validated':19619,'retained_records':19619,'numeric_values_validated':2264113}} and small['source_total_object_lifetime']=='one complete reader record dict at a time; first released before second and state released before next state')
 full_pin(small['original_input']['path'],small['original_input']);full_pin(small['full_raw_archive']['path'],small['full_raw_archive'])
 with pathlib.Path(small['original_input']['path']).open('rb')as original, pathlib.Path(small['full_raw_archive']['path']).open('rb')as archive:
  equal=True
  while True:
   first=original.read(1048576);second=archive.read(1048576)
   if first!=second:equal=False;break
   if not first:break
 check(state+' original ASCII archive complete byteequal with actualinputs no parse',equal and small['original_input']['sha256']==small['full_raw_archive']['sha256'] and small['original_input']['size_bytes']==small['full_raw_archive']['size_bytes']==39546544)
 contracts=jsonl(root/'full_required_field_contract.jsonl');gaps=[x for x in contracts if x['gap_reasons']];sparse=jsonl(root/'full_sparse_reference_spans.jsonl');science=small['scientific_contract_inventory'];pathmap={tuple(x['path']):x for x in index}
 check(state+' entire8515 requiredfield inventory missinggaps no substitution',len(contracts)==science['required_record_checks']==8515 and gaps==[{'path':['FISSIONINDEX'],'expected_original_kind_one_of':[1],'expected_count':256,'present':True,'actual_kind':1,'actual_count':64,'gap_reasons':['unexpected_actual_count']}] and science['gap_counts']=={'unexpected_actual_count':1} and all(x['present']is True and tuple(x['path'])in pathmap and x['actual_kind']==pathmap[tuple(x['path'])]['kind'] and x['actual_count']==(None if pathmap[tuple(x['path'])]['kind']==3 else pathmap[tuple(x['path'])]['declared_count'])for x in contracts))
 check(state+' actual52GROUP names all extra reactions no crop TRANC retained',science['all_actual_GROUP_field_names_including_extra_reactions']==sorted({x['path'][2]for x in index if len(x['path'])==3 and x['path'][0]=='GROUP'}) and len(science['all_actual_GROUP_field_names_including_extra_reactions'])==52 and 'TRANC'in science['all_actual_GROUP_field_names_including_extra_reactions'] and science['actual_STATE_VECTOR'][:4]==[370,8,3,32] and science['raw_Legendre_no_angular_factor_applied']is True and science['no_fields_filled_clipped_normalized_or_inferred']is True)
 check(state+' all8880 full sparse spans370x8x3 rawindexvalid padding no packing assumption',len(sparse)==8880 and {(x['destination_group'],x['mixture'],x['raw_Legendre_moment'])for x in sparse}=={(g,m,l)for g in range(1,371)for m in range(1,9)for l in range(3)} and all(x['valid_referenced_span']is True and x['raw_unreferenced_padding_retained_without_interpretation']is True and x['contiguous_packing_required_or_assumed']is False and x['source_indices_formula']=='top-jnd+1 for jnd=1..count' and x['raw_SCAT_record_count']==pathmap[('GROUP',x['destination_group'],'SCAT'+str(x['raw_Legendre_moment']).zfill(2))]['declared_count'] and (x['count']==0 or 1<=x['one_based_raw_offset']and x['one_based_raw_offset']+x['count']-1<=x['raw_SCAT_record_count'])for x in sparse))
 for key in ('original_LCM_memory_bit_identity_directly_verified','true_physical_loss_reaction_multiplicity_verified','transport_correction_semantics_qualified','future_solver_scientific_input_admitted'):check(state+' honest original scientific limit '+key,science[key]is False)
 evidence.update({'state':state,'small_state_metadata':small,'full_required_field_rows':len(contracts),'actual_full_gap_rows':gaps,'full_sparse_reference_rows':len(sparse)});state_evidence.append(evidence)
 del index,contracts,gaps,sparse,pathmap,small,science
tiny_evidence,tiny_index=audit_index(C,'complete_tiny_typed_index.jsonl','complete_tiny_raw_header_spans.jsonl','complete_tiny_typed_payload.bin','complete_tiny_protocol_fixture.ascii',44,47,139)
check('protocol tiny complete44records47headers139values includesREAL64 unknownkind zero',protocol['full_tiny_raw_inventory']=={'records':44,'physical_headers_including_closes':47,'numeric_values':139,'full_original_raw_byte_interval_coverage':True} and tiny_evidence['kind_counts']=={3:2,1:21,2:16,4:1,99:1,10:1,0:2} and any(x['path']==['ROUND64']and x['kind']==4 for x in tiny_index))
tiny_contract=jsonl(C/'complete_tiny_required_field_gap_inventory.jsonl');tiny_sparse=jsonl(C/'complete_tiny_sparse_spans.jsonl');tiny_gapcounts=collections.Counter(reason for x in tiny_contract for reason in x['gap_reasons'])
check('tiny whole8515 required missingfields honest gapinventory and1110sparse rows no zeros',len(tiny_contract)==8515 and dict(tiny_gapcounts)=={'unexpected_actual_count':27,'missing_real_record_no_substitution':8478} and len(tiny_sparse)==1110 and all(x.get('status')=='required_raw_sparse_fields_missing_or_malformed_no_expansion'or x.get('raw_unreferenced_padding_retained_without_interpretation')is True for x in tiny_sparse))
check('actual scientificFISSIONINDEX gap retained exact256vs64 bothstates',summary['scientific_contract_gap_each_state']=={'path':['FISSIONINDEX'],'expected_count':256,'actual_count':64,'gap':'unexpected_actual_count','gap_not_repaired_or_hidden':True} and summary['A_and_B_each_full_record_count']==19619 and summary['A_and_B_each_numeric_value_count']==2264113 and summary['all_original_records_and_fields_retained']is True and summary['actual_complete_full_two_reader_data_consistency']is True)
sciencekeys=['original_XSM_memory_bits_verified','reaction_multiplicity_verified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','coupled_370group_reference_qualified','native_transport_executed','whole_combined_build_or_INPUT_qualified']
for label,obj in [('Rootsummary',summary),('host',host),('protocol',protocol),('transfer',transfer),('payloadmanifest',payload_manifest),('Sourcebinding',binding)]:
 for key in sciencekeys:
  if key in obj:check(label+' no science/native/multiplicity/reference/AAA/ABA promotion '+key,obj[key]is False)
check('software rawtransfer not original qualification and no modelchange',host['actual_protocol_qualified']is False and host['actual_full_rawrecord_transfer_qualified']is False and host['actual_protocol_qualification_sha256']is None and host['actual_transfer_qualification_sha256']is None and summary['actual_protocol_qualification_sha256']is None and summary['actual_transfer_qualification_sha256']is None and summary['independent_saved_actual_review_pass']is False and transfer['production_model_or_physics_modified']is False and protocol['actual_material_payload_parsed']is False)
check('Root firstpostcloseMETA stageprefix check not actualbusinessfailure',summary['Root_first_postclose_META_check']=={'chunk_id':'6a1a61','exit_code':1,'closed':True,'reason':'Root expected unprefixed stage labels; original runner saved protocol_run/protocol and transfer_run/transfer','actual_protocol_or_transfer_retried':False,'no_summary_or_manifest_created_before_correction':True})
unique={x['path']:x for x in READS};stable=[]
for path,pin in unique.items():stable.append(full_pin(path,pin))
hard=[x for x in CHECKS if not x['PASS']]
result={'schema':'INDEPENDENT_V22_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_SOURCE_META_PEER_REVIEW_V1','scope':'STANDARD_LIBRARY_FINITE_COMPLETE_SOURCE_SAVED_METADATA_JSONL_INDEX_SPANS_AND_RAW_BINARY_EOF_HASH_ONLY_NO_READER_HELPER_GUARD_OR_BUSINESS_API_EXECUTION','PASS':not hard,'hard_blockers':hard,'check_count':len(CHECKS),'checks':CHECKS,'actual_Root_terminal_tool_receipt':terminal_pin,'actual_Root_terminal_tool_return':t,'Root_summary_pin':summary_pin,'Root_namespace_manifest_pin':manifest_pin,'complete_namespace_snapshots':snapshots,'complete_full_EOF_reads':READS,'unique_complete_fresh_rechecked_input_pins':stable,'complete_original_caps':CAPS,'genuine_actual_watches':watches,'full_state_record_and_span_evidence':state_evidence,'complete_tiny_protocol_span_evidence':tiny_evidence,'complete_5positive10negative_protocol_controls':{'positive':protocol['complete_positive_controls'],'negative':protocol['complete_negative_controls']},'original_archive_scope':['H','O','C','D','E'],'captured_joint_bytes_before_summary_manifest':captured_joint,'current_joint_bytes_after_summary_manifest':current_joint,'original_parent_stdout_startup_pin':startup,'actual_parent_stdout_postprint_pin':current_stdout,'FISSIONINDEX_full_original_gap_each_state':summary['scientific_contract_gap_each_state'],'complete_saved_rawrecord_software_evidence_independently_reviewed':not hard,'actual_protocol_qualification_sha256':None,'actual_transfer_qualification_sha256':None,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'whole_combined_build_or_INPUT_qualified':False,'honest_scope_notes':['Peer read complete finite original Source/META and every saved JSONL index/header/contract/sparse row; original raw ASCII and typed binary files were read through EOF and every saved raw/header/typed span SHA independently checked without decoding material values or calling business readers.','Both original A/B raw archives were compared byte for byte with their original pinned inputs. Numerical values/parser float bits equality is the exact saved normal business comparison, complete typed binary spans and unchanged complete Source proof; peer did not rerun numeric readers.','Real32 rounded bits plus parser64 bits are retained separately at12bytes/value; REAL64 bits remain8bytes/value and complete tiny proof retained. No original XSM in-memory bit identity or reaction/science qualification is claimed.','FISSIONINDEX expected256 actual64 eachstate is retained as the one scientific contract gap, not repaired/hidden/normalized. Angular/source-layout investigation is separate.','Protocol watcher0.0MiB is missing transient sampled observation, not proof of actual zero memory. Transfer watch270.8125MiB/7.078265291987918s and host9.93906679097563s are genuine saved metrics.','Original empty startup parent stdout pin is historical; the same file changes only after finalprint. Actual postprint pin and complete bytes are separately retained. Eroot receives summary/manifest after its honest snapshot, not claimed immutable.','Root6a1a61 META check failed only unprefixed stage-label assumption before any summary/manifest writes; original runner stage labels have prefixes. No protocol or transfer retry occurred.','This review creates no protocol/transfer qualification receipt, runtime wholeINPUT/build/native RSS/scientific/reference/AAA/ABA qualification.']}
out=HERE/'INDEPENDENT_ACTUAL_COMPLETE_FULL_AB_RAWRECORD_SAVED_META_REVIEW.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'schema':result['schema'],'report':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size_bytes':out.stat().st_size,'PASS':result['PASS'],'check_count':len(CHECKS),'hard_blockers':hard,'unique_complete_Source_META_raw_binary_EOF_inputs':len(unique),'actual_Root_terminal_chunk':'8bdd07','current_joint_archive_bytes':current_joint,'no_science_qualification':True},ensure_ascii=False));sys.exit(0 if not hard else 1)

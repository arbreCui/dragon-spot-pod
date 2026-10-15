#!/usr/bin/env python3
"""Saved complete fresh verifier Source/META audit; no helper/guard/driver execution."""
import ast
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
D=B/'actual_complete_graph_fresh_verifier_v22_sources'
E=B/'actual_complete_graph_fresh_verifier_v22_receipts'
H=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v22-20261010')
O=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v22-20261010')
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

terminal_pin=full_pin(E/'Root_actual_fresh_verifier_tool_terminal_return.json',sha='de3750d802a442329089c5301d36939bda610ddc88bc7770dbe0c0f7f65a76f4')
summary_pin=full_pin(E/'Root_actual_fresh_verifier_summary.json',sha='fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e')
manifest_pin=full_pin(E/'Root_actual_fresh_verifier_namespace_manifest.json',sha='f22cb50803831a86c5ec1e8a40a464c84dc753ab6c0f855706c93c7400b3ee1f')
terminal=meta(terminal_pin['path']);summary=meta(summary_pin['path']);manifest=meta(manifest_pin['path']);t=terminal['terminal_tool_return']
check('real Root57a6f5 strictint0 closed29568 no repoll',terminal['schema']=='ROOT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_TOOL_TERMINAL_RETURN_V1' and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='57a6f5' and 'session_id'not in t and terminal['closed']is True and terminal['actual_tool_terminal_return_observed']is True and terminal['initial_tool_return']['session_id']==29568 and terminal['subsequent_actual_tool_observations'][-1]==t and terminal['session_repolled_after_close']is False and terminal['retries']==0)
check('Root summary terminal status exact scope',summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1' and summary['status']=='ACTUAL_EXIT0_CLOSED_COMPLETE_FRESH_CONTROLS_SAVED_REVIEW_REQUIRED' and summary['terminal_chunk_id']=='57a6f5' and type(summary['actual_Root_exit_code'])is int and summary['actual_Root_exit_code']==0 and summary['closed']is True and norm(summary['actual_external_Root_terminal'])==norm(terminal_pin) and norm(summary['complete_namespace_manifest'])==norm(manifest_pin))
check('finite full saved namespace schema roots',manifest['schema']=='ROOT_V22_COMPLETE_QUALIFICATION_FINITE_NAMESPACE_V1' and set(manifest['complete_namespaces'])=={'D','H','O','E_pre_summary'})
snapshots=[];regular_DHO=0;regular_E=0
later_E={'Root_actual_fresh_verifier_summary.json','Root_actual_fresh_verifier_namespace_manifest.json'}
for label,ns in manifest['complete_namespaces'].items():
 root=pathlib.Path(ns['root']);files,dirs,links=tree(root)
 check(label+' correct literal root',root=={'D':D,'H':H,'O':O,'E_pre_summary':E}[label])
 check(label+' complete finite member names no crop',set(files)==set(ns['files'])|(later_E if label=='E_pre_summary' else set()) and set(dirs)==set(ns['directories']) and links==ns['symlinks'])
 check(label+' saved exact complete counts',ns['file_count']==len(ns['files']) and ns['directory_count']==len(ns['directories']) and ns['symlink_count']==len(ns['symlinks']))
 for rel,pin in ns['files'].items():
  check(label+' full saved literal relative path '+rel,pathlib.Path(pin['path'])==root/rel);full_pin(pin['path'],pin)
 for rel,identity in ns['directories'].items():
  if label=='E_pre_summary' and rel=='.':check('E_root append2 honest snapshot/current boundary',dirs[rel]!=identity and dirs[rel][:3]==identity[:3],{'before_summary_manifest':identity,'current_after_append':dirs[rel]})
  else:check(label+' full directory7ID unchanged '+rel,dirs[rel]==identity)
 if label=='E_pre_summary':regular_E=sum(x[4]for x in files.values())
 else:regular_DHO+=sum(x[4]for x in files.values())
 snapshots.append({'label':label,'root':str(root),'complete_regular_files':{r:ns['files'].get(r)for r in files},'directories':dirs,'symlinks':links,'regular_file_count':len(files),'directory_count':len(dirs)})
check('original complete D13/2 H5/4 O6/1 Epre4/1 retained',[(len(manifest['complete_namespaces'][k]['files']),len(manifest['complete_namespaces'][k]['directories']),len(manifest['complete_namespaces'][k]['symlinks']))for k in ('D','H','O','E_pre_summary')]==[(13,2,0),(5,4,0),(6,1,0),(4,1,0)])
freeze=meta(summary['source_namespace_freeze']['path']);full_pin(summary['source_namespace_freeze']['path'],summary['source_namespace_freeze'])
check('full D13 files2dirs freeze untouched no append',freeze['schema']=='ROOT_V22_FINAL_COMPLETE_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['source_root']==str(D) and freeze['complete_files']==manifest['complete_namespaces']['D']['files'] and freeze['complete_directories']==manifest['complete_namespaces']['D']['directories'] and freeze['no_Source_append_after_freeze']is True and summary['source_file_count']==13 and summary['all_source_files_before_after_exact']is True and manifest['D_frozen_files_directories_exact']is True and freeze['Source_peer_check_count']==759 and freeze['new_Q']is None and freeze['actual_qualifiers_executed']is False)
host=meta(H/'result.json');watch=meta(H/'run/admit.watchdog.json');child=meta(H/'run/admit.log');parent=meta(E/'parent_stdout.log');report=meta(O/'ACTUAL_REPORT.json');claim=meta(O/'ACTUAL_RUN_CLAIM.json');stages=meta(H/'COMPLETE_FRESH_VERIFIER/stages.json')
for key in ('actual_host_result','actual_control_report','actual_watchdog','actual_control_child_merged_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr'):full_pin(summary[key]['path'],summary[key])
check('normal actual fresh host Source-qualified schema/status',host['schema']=='AXMAT_V22_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1' and host['status']=='ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED' and parent['status']==host['status'] and norm(parent['actual_host_result'])==norm(summary['actual_host_result']) and norm(parent['actual_merged_child_stdout_stderr'])==norm(summary['actual_control_child_merged_stdout_stderr']) and parent['actual_external_Root_terminal_required']is True)
check('full actual report34fields exact Root saved object',report['schema']=='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1' and report['status']=='ACTUAL_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_RETURNED_PENDING_EXTERNAL_ROOT' and len(report)==34 and exact(report,summary['complete_actual_report']) and child['status']==report['status'] and norm(child['report'])==norm(host['actual_control_report'])==norm(summary['actual_control_report']))
sourceNs=host['source_namespace_before']
check('genuine host complete Source namespace before/after identity exact',exact(sourceNs,host['source_namespace_after']) and sourceNs['schema']=='AXMAT_V22_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_NAMESPACE_V1' and sourceNs['root']==str(D) and sourceNs['symlinks']==[] and sourceNs['complete_dynamic_before_after']is True and sourceNs['Root_external_freeze_and_host_source_pin_required']is True and {pathlib.Path(x['path']).relative_to(D).as_posix():norm(x)for x in sourceNs['files']}=={rel:norm(x)for rel,x in freeze['complete_files'].items()} and {pathlib.Path(x['path']).relative_to(D).as_posix():x['identity']for x in sourceNs['directories']}==freeze['complete_directories'])
command=[str(pathlib.Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')),'-B',str(D/'fresh_verifier_controls.py'),'--output-dir',str(O),'--driver-sha256','de3384af3860177cabfb3fa87b6c413aac83a8f17570df01f0a14b3f6600da08']
check('real watchdog int0 ownchild345.390625 no failure cleanup',exact(host['watchdog'],watch) and type(watch['returncode'])is int and watch['returncode']==0 and type(watch['pid'])is int and watch['pid']==15414 and watch['sampled_peak_rss_mib']==345.390625 and watch['rss_cap_mib']==512 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['command']==host['actual_canonical_command']==command)
actual=host['actual_full_controls']
check('actual claim watch and host parent-child PID tied',type(report['PID'])is int and report['PID']==claim['PID']==actual['actual_child_PID']==child['PID']==watch['pid']==15414 and type(report['parent_PID'])is int and report['parent_PID']==claim['parent_PID']==actual['actual_host_PID']==child['parent_PID']==host['actual_host_PID']==15413 and actual['actual_claim_parent_and_watch_PID_match']is True)
full_pin(actual['actual_claim']['path'],actual['actual_claim'])
check('all complete host predicates true without premature Root/Q',actual['complete_private_controls']is True and actual['complete_current_graph_verifier_returned']is True and actual['external_Root_closed_terminal_required']is True and norm(actual['actual_report'])==norm(summary['actual_control_report']))
check('one genuine full actual monitored stage',exact(host['stage_records'],stages['stages']) and len(stages['stages'])==1 and stages['stages'][0]['label']=='run/admit' and stages['stages'][0]['status']=='PASS' and stages['stages'][0]['command']==watch['command'] and stages['stages'][0]['log_sha256']==summary['actual_control_child_merged_stdout_stderr']['sha256'])
check('whole/stage and two distinct observed memory metrics under original caps',host['whole_seconds']==summary['whole_seconds']==30.926444750046358 and watch['elapsed_seconds']==summary['child_seconds']==29.723590500070713 and summary['sampled_peak_rss_mib']==345.390625 and report['caps_checkpoint']['own_peak_rss_bytes']==child['final_checkpoint']['own_peak_rss_bytes']==372441088 and report['caps_checkpoint']['own_peak_rss_bytes']/2**20==355.1875 and 0<report['caps_checkpoint']['elapsed_seconds']<child['final_checkpoint']['elapsed_seconds']<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stages['stages'][0]['wall_cap_seconds']<=600 and host['whole_seconds']<1800 and report['caps_checkpoint']['own_peak_rss_bytes']<512*2**20)
check('complete unchanged original caps host/report/summary',[(host[k])for k in ('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_cap_mib','archive_cap_bytes','threads','children_at_once','retries')]==[1800,600,512,67108864,1,1,0] and [(report[k])for k in ('whole_host_seconds','stage_seconds','rss_mib','joint_HOST_SOURCE_OUT_archive_bytes','history_bytes','min_free_bytes','threads','children','retries')]==[1800,600,512,67108864,103079215104,8589934592,1,1,0] and [(summary[k])for k in ('whole_seconds_cap','stage_seconds_cap','rss_mib_cap','archive_bytes_cap','history_bytes_cap','free_bytes_floor','threads','children','retries')]==[1800,600,512,67108864,103079215104,8589934592,1,1,0])
source_receipt_prelaunch_bytes=freeze_pin_bytes=summary['source_namespace_freeze']['identity'][4]
archive_scope={'original_normal_guard_scope':['H','O','D','E'],'Root_saved_DHO_ledger_bytes':regular_DHO,'original_business_post_result_HODE_bytes':regular_DHO+source_receipt_prelaunch_bytes,'peer_current_full_HODE_bytes':regular_DHO+regular_E,'current_E_bytes':regular_E,'Root_DHO_ledger_is_not_original_HODE_scope':True}
check('full original HODE archive scope under64MiB with E honest append',regular_DHO==manifest['joint_D_H_O_bytes']==summary['joint_source_host_out_bytes']==1611101 and regular_E==53201 and regular_DHO+regular_E==1664302 and host['archive_before_result_bytes']+summary['actual_host_result']['identity'][4]==regular_DHO+source_receipt_prelaunch_bytes==1620310 and regular_DHO+regular_E<67108864,archive_scope)
check('23 ordered inputs plus2 original helper/resource all current full',len(host['input_sources'])==23 and summary['host_input_sources_and_original_helper_resource_factory_post_close_exact']==25)
for i,pin in enumerate(host['input_sources']):full_pin(pin['path'],pin);check('all exact7 strictint ordered hostpin '+str(i),len(pin['identity'])==7 and all(type(x)is int for x in pin['identity']))
for pin in (host['original_helper'],host['resource_factory']):full_pin(pin['path'],pin)
check('all D13 files included original fixed10 plus complete namespace',len(host['input_sources'][10:])==13 and set(x['path']for x in host['input_sources'][10:])==set(x['path']for x in freeze['complete_files'].values()))
check('real Root launch approved host all1threads',str(D/'fresh_verifier_host.py')in terminal['actual_arguments']['cmd'] and all(k+'=1'in terminal['actual_arguments']['cmd']for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')))
driver_source=(D/'fresh_verifier_controls.py').read_bytes();host_source=(D/'fresh_verifier_host.py').read_bytes();ast.parse(driver_source);ast.parse(host_source)
check('driver/host complete Source-qualified bound SHA',hashlib.sha256(driver_source).hexdigest()=='de3384af3860177cabfb3fa87b6c413aac83a8f17570df01f0a14b3f6600da08' and hashlib.sha256(host_source).hexdigest()=='3561c87b99d74c6f75b506fd4d5ccd7df1532c806f60644ae6f875d7c2f77468')
for snippet in ['full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','Path(full.__file__).resolve()!=support.FULL','Path(production.__file__).resolve()!=support.PARENT','helper.guard_admission(full)','type(runner) is not full.OwnRSSSerialExecutor','resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)','support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))']:
 check('complete genuine guard/MRO/full archive scope Source '+snippet,snippet in host_source.decode())
for name in ('resources_before','resources_after'):
 resource=host[name];check('genuine saved complete history/free limits '+name,resource['min_free_bytes']==8589934592 and resource['artifact_budget_bytes']==103079215104 and resource['artifact_bytes']<103079215104 and resource['disk_free_bytes']>=8589934592 and resource['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and all(str(p)in resource['declared_resource_roots']for p in (H,O,pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'),pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'),pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'))))
check('all fixedbefore/after4 complete order/type/value/pins same',exact(report['fixed_inputs_before'],report['fixed_inputs_after']) and list(report['fixed_inputs_before'])==['driver','old_parent','new_helper','stored_graph'])
for pin in report['fixed_inputs_before'].values():full_pin(pin['path'],pin)
check('exact bcd complete oracle and cf0helper unchanged',report['fixed_inputs_before']['old_parent']['sha256']=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6' and report['fixed_inputs_before']['new_helper']['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c' and norm(host['installed_helper'])==norm(report['fixed_inputs_before']['new_helper'])==norm(summary['installed_helper']))
check('actual success pins exactly full helper/graph/gzip/trace pins',list(report['actual_success_pins'])==['helper','graph','full_return','full_trace'] and exact(report['actual_success_pins']['helper'],report['fixed_inputs_before']['new_helper']) and exact(report['actual_success_pins']['graph'],report['fixed_inputs_before']['stored_graph']) and exact(report['actual_success_pins']['full_return'],report['actual_complete_verifier_return']) and exact(report['actual_success_pins']['full_trace'],report['actual_complete_ReadOpenAudit_trace']))
expected,expected_raw=gzip_meta(report['expected_complete_return_contract']);returned,returned_raw=gzip_meta(report['actual_complete_verifier_return']);trace,trace_raw=gzip_meta(report['actual_complete_ReadOpenAudit_trace'])
check('all complete expected/actual rawJSON wire types order values floatbits exact',expected_raw==returned_raw and exact(expected,returned) and report['expected_complete_return_contract']['sha256']==report['actual_complete_verifier_return']['sha256']=='a2a1645d2ee61e1dd12ee47455bfc4dee982b93fb42931f20d7bee55ff055dd4')
RETURN_FIELDS=['schema','classification','consumer_scope','consumer_selected_literal_and_canonical_paths','consumer_complete_namespace_root_sequence','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','coverage','trace_coverage','live_io_scope','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','absence_inputs_are_not_regular_bytes_or_science','caller_must_recheck_current_OS_identity_and_live_probe_results','typed_snapshot','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources']
check('all original27 fields exact ordered retain without projection',list(returned)==list(expected)==report['complete_return_fields_retained']==RETURN_FIELDS and report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal']is True and len(returned)==27)
check('full scope none no consumer filtering and canonical logical ns aliasabsence counts',returned['schema']=='AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2' and returned['classification']=='FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY' and returned['consumer_scope']is None and returned['consumer_selected_literal_and_canonical_paths']is None and returned['consumer_complete_namespace_root_sequence']is None and returned['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and returned['phase']=='helper_complete_fresh_verifier_control' and [(returned[k])for k in ('canonical_files_read','actual_bytes_read','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','declared_absence_inputs_checked_before_and_after_bytes')]==[37111,36182827268,238441,86,186,479] and returned['byte_count_scope']=='CANONICAL_INPUT_UNION_ONLY_EXCLUDES_STORED_GRAPH_JSON' and returned['live_io_scope']=='LIVE_OS_PROBE_STDIO_ONLY_NO_INPUT_BYTES_OR_SCIENCE')
contract=returned['fresh_reader_contract']
check('all original10 freshreader contract retained no cache/filter',len(contract)==10 and contract['schema']=='AXMAT_REFERENCE_FRESH_UNION_SINGLE_PARENT_JSON_READER_V1' and contract['chunk_bytes']==8388608 and contract['max_json_bytes']==67108864 and all(v is True for k,v in contract.items()if k not in ('schema','chunk_bytes','max_json_bytes')))
for key in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified','live_subprocesses_reexecuted'):check('return false strict '+key,returned[key]is False)
for key in ('absence_inputs_are_not_regular_bytes_or_science','caller_must_recheck_current_OS_identity_and_live_probe_results','caller_must_verify_live_environment_modules_PID_time_and_resources'):check('full obligations true '+key,returned[key]is True)
metadata=report['independent_full_saved_graph_metadata']
check('all original full saved graph table/countscope retained',len(metadata)==16 and [(metadata[k])for k in ('requirement_row_count','requirement_column_count','canonical_files','owners','namespaces','aliases','saved_trace_records','saved_trace_actual_attempts','absence_inputs','closure_categories')]==[238441,5,37111,4473,86,186,63469,176426,479,9] and metadata['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and metadata['consumer_scope']is None and metadata['newly_declared_input_paths']=={} and metadata['newly_declared_input_pins']=={} and sorted(returned['coverage'])==metadata['complete_coverage_fields'] and sorted(returned['trace_coverage'])==metadata['complete_tracecoverage_fields'] and len(returned['coverage'])==9 and len(returned['trace_coverage'])==10)
for key,row in returned['coverage'].items():check('full coverage all owners/types/values '+key,type(row)is dict and set(row)=={'canonical_files','bytes','owners'} and type(row['canonical_files'])is int and row['canonical_files']>=0 and type(row['bytes'])is int and row['bytes']>=0 and type(row['owners'])is list and all(type(x)is str for x in row['owners']))
typed=returned['typed_snapshot']
check('original seven-key complete typed snapshot no historical promotion',len(typed)==7 and typed['failed_historical_combined_RUN_promoted']is False and typed['original_component_APIs_executed_now']is False and typed['historical_whole_component_body']['whole_seven_key_body_retained']is True and typed['historical_whole_component_body']['historical_FAILED_RUN_promoted']is False and typed['historical_whole_component_body']['original_component_API_execution_claimed']is False and typed['actual_last_cprime_trim_component_INPUT']['original_historical_seven_key_body_unchanged']is True and typed['actual_last_cprime_trim_component_INPUT']['old_capture_RSS_transferred']is False and typed['actual_last_cprime_trim_component_INPUT']['trim_native_RSS_proof_obtained']is False and typed['prior_failed_PREP_input']['actual_exit_code']==1)
TRACE_FIELDS=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
records=trace['records'];graph_path=report['fixed_inputs_before']['stored_graph']['path'];paths=[x['path']for x in records]
check('all unfiltered37112actual trace records9fields no subprocess',list(trace)==TRACE_FIELDS and trace['schema']=='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' and trace['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' and len(records)==trace['unique_records']==trace['actual_read_open_attempts']==37112 and trace['subprocess_records']==[] and trace['record_storage']=='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' and trace['success_of_open_attempt_is_not_observed']is True and trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced']is True)
check('all37112 entire typed record fields/open modes/1attempt and order retained',all(type(x)is dict and list(x)==['access','attempt_count','cwd','event','flags','kind','literal_path','mode','observation','path'] and x['access']=='read' and type(x['attempt_count'])is int and x['attempt_count']==1 and x['cwd']==str(H/'run') and x['event']=='open' and type(x['flags'])is int and x['kind']=='path' and type(x['path'])is str and x['literal_path']==x['path'] and x['mode']is None and x['observation']=='OPEN_ATTEMPT'for x in records) and len(set(paths))==37112 and paths[0]==graph_path and paths.count(graph_path)==1)
check('37111 canonical opens plus1graph actual exact count',report['actual_complete_trace_counts']=={'records':37112,'attempts':37112,'canonical_files':37111,'external_graph_reads':1,'no_subprocess_reexecuted':True} and len(paths)-paths.count(graph_path)==returned['canonical_files_read'])
trace_sequence_sha=hashlib.sha256(json.dumps(paths,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
controls=report['private_trace_controls'];small=controls['actual_small_ReadOpenAudit'];augmented=controls['control_only_augmented_records']
check('private fixture1 genuineopen with explicitly augmented separate control',small['schema']==trace['schema'] and small['coverage']==trace['coverage'] and len(small['records'])==small['unique_records']==small['actual_read_open_attempts']==1 and small['subprocess_records']==[] and small['records'][0]['path']==str(O/'private_trace_fixture.txt') and controls['augmented_records_are_not_claimed_as_actual_full_verifier_trace']is True and controls['old60pure_control_functions_not_changed']is True and len(augmented)==1 and exact({k:v for k,v in augmented[0].items()if k!='control_only_builtin_json_witness'},small['records'][0]) and exact(augmented[0]['control_only_builtin_json_witness'],{'floatbits':[-0.0,1e-300,1.25],'ordered':[True,0,None,'text']}))
positive=controls['positive_controls'];negative=controls['rejections']
check('all original private trace4positive3reject complete order',[x['case']for x in positive]==['default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True'] and [x['case']for x in negative]==['nonbool_consume','tuple_True','list_subclass_True'])
for row in positive:check('private trace complete typed order floatbits oldbcd equivalence '+row['case'],row['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd']is True and (row.get('caller_full_identity_type_order_value_floatbits_unchanged')is True if row['case']!='probe_owned_builtin_list_True' else row['owned_list_completely_cleared']is True))
for row in negative:check('private trace actual class/message no caller mutation '+row['case'],row['class_name']=='InputGraphError' and row['message']=='private trace consume needs a bool and an exclusively owned builtin list' and row['rejected']is True and row['caller_type_identity_nested_value_order_floatbits_unchanged']is True)
for report_key,host_key in [('expected_complete_return_contract','complete_expected_return'),('actual_complete_verifier_return','complete_actual_return'),('actual_complete_ReadOpenAudit_trace','complete_actual_unfiltered_trace')]:check('host validates entire gzip actualpin '+report_key,norm(report[report_key])==norm(actual[host_key]))
check('original merged child streams honest no independent stderr claim',host['independent_child_stdout_captured']is False and host['independent_child_stderr_captured']is False and parent['independent_child_stdout_captured']is False and parent['independent_child_stderr_captured']is False and summary['separate_child_stderr_capture_verified']is False and summary['child_stdout_stderr_merge_is_original_normal_guard']is True and summary['actual_external_parent_stderr']['identity'][4]==0)
for name,obj,keys in [('Roottool',terminal,['complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']),('summary',summary,['whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified']),('host',host,['helper_metadata_qualified','whole_business_INPUT_qualified','physical_balance_qualified','profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']),('report',report,['business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified'])]:
 for key in keys:check(name+' no Q/build/Input/native/science promotion '+key,obj[key]is False)
check('saved summary prior review false and actualfreshpass true no Q yet',summary['actual_fresh_controls_pass']is True and summary['independent_saved_actual_review_pass']is False and summary['actual_new_helper_qualification_sha256']is None and terminal['actual_new_helper_qualification_sha256']is None and host['UNKNOWN_Q']is None and host['UNKNOWN_BUSINESS_PINS']is None)
unique={x['path']:x for x in READS};stable=[]
for path,pin in unique.items():
 actual_pin=full_pin(path,pin);stable.append(actual_pin)
hard=[x for x in CHECKS if not x['PASS']]
result={'schema':'INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1','scope':'INDEPENDENT_FINITE_SOURCE_AND_SAVED_META_ONLY_NO_HELPER_GUARD_DRIVER_API_OR_NUMERIC_EXECUTION','PASS':not hard,'hard_blockers':hard,'check_count':len(CHECKS),'checks':CHECKS,'actual_Root_fresh_tool_receipt':terminal_pin,'actual_Root_terminal_tool_return':t,'Root_summary_pin':summary_pin,'Root_namespace_manifest_pin':manifest_pin,'actual_watchdog':watch,'complete_namespace_snapshots':snapshots,'complete_full_EOF_reads':READS,'unique_complete_fresh_rechecked_input_pins':stable,'original_archive_full_HODE_scope':archive_scope,'genuine_watchdog_sampled_peak_rss_mib':345.390625,'driver_own_peak_rss_bytes':372441088,'driver_own_peak_rss_mib':355.1875,'all_three_complete_gzip_pins':{k:report[k]for k in ('expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace')},'all27_return_fields':RETURN_FIELDS,'complete_typed_snapshot':typed,'complete_saved_graph_counts_and_fields':metadata,'unfiltered37112trace_complete_order_path_sequence_sha256':trace_sequence_sha,'actual_private_trace_controls':controls,'full_current_graph_saved_evidence_independently_reviewed':not hard,'helper_metadata_qualification_receipt_created':False,'new_Q':None,'complete_build_qualified':False,'whole_INPUT_admitted':False,'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False,'honest_scope_notes':['All three saved gzip streams were read through decompression EOF with CRC, exact compressed/uncompressed SHA/bytes and complete strict JSON type/order/floatbits comparison; no fields or records filtered.','Stored current input graph was finite full-EOF SHA/7ID checked only, not JSON decoded; canonical material files were not read by peer. Actual complete graph execution is evidenced by pinned normal driver/host, complete old bcd oracle, saved full result and actual audit trace, not a peer rerun.','Root manifest D/H/O ledger is explicitly1611101 bytes. Original host archive cap covers H/O/D/E; peer independently checked full current HODE1664302 bytes and original post-result HODE1620310 bytes.','Source freeze prelaunch metadata actual_qualifiers_executed=False is historical; genuine actualRoot57a6f5 strictint0closed is separate.','Genuine watchdog sampled345.390625MiB differs from driver self372441088B=355.1875MiB; both retained separately.','No Q, business build, whole INPUT admission, native RSS or science qualification is created by this finite saved-META review.']}
out=HERE/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_REVIEW.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'schema':result['schema'],'report':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size_bytes':out.stat().st_size,'PASS':result['PASS'],'check_count':len(CHECKS),'hard_blockers':hard,'unique_full_EOF_Source_META_inputs':len(unique),'all27_fields':len(RETURN_FIELDS),'actual_trace_records':len(records),'actual_root_terminal_chunk':'57a6f5','all_actual_current_HODE_bytes':regular_DHO+regular_E,'new_Q':None},ensure_ascii=False))
sys.exit(0 if not hard else 1)

"""Run only after Root provides its genuine closed PREP witness; no business imports."""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009'
OUT=ART/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
FACTORY=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
HELPER=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
FACTORY_SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
HELPER_SHA='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
SPECS=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
SPECS_SHA='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
PREFIX='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12'
GRAPH_SCHEMA='AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
STORAGE_SCHEMA='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1'
INPUT_SCOPE='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
CAP=67108864
COLS=['path','sha256','size_bytes']
FULL_SOURCE_NAMES={'historical_input_combined_runtime_factory.py','input_specs.json','source_admission.json','trim_component_admission_INPUT.json','trim_component_API_python_open_trace.json','trim_component_API_absence_INPUT.json','runtime/graph.py','runtime/codec.py','runtime/current.py','runtime/checks.py','runtime/ordinary.py'}

def sig(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink)
def valid_sha(v):return type(v)is str and len(v)==64 and all(c in '0123456789abcdef'for c in v)
def normal(p):
 p=Path(p)
 assert p.is_absolute() and '..' not in p.parts
 for q in [*reversed(p.parents),p]:assert not q.is_symlink(),str(q)
 return p
def fresh(p,expected=None,collect=False,max_bytes=None):
 p=normal(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);parts=[] if collect else None;h=hashlib.sha256();n=0
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode)
  if max_bytes is not None:assert before.st_size<=max_bytes
  while True:
   b=os.read(fd,1048576)
   if not b:break
   n+=len(b)
   if max_bytes is not None:assert n<=max_bytes
   h.update(b)
   if collect:parts.append(b)
  after=os.fstat(fd);assert sig(before)==sig(after)==sig(p.stat()) and n==before.st_size
 finally:os.close(fd)
 digest=h.hexdigest()
 if expected is not None:assert valid_sha(expected) and digest==expected,str(p)
 return dict(path=str(p),sha256=digest,bytes=n,seven_identity=list(sig(after))),b''.join(parts)if collect else None
def bad_constant(v):raise ValueError('nonfinite JSON '+v)
def finite_float(v):
 v=float(v);assert math.isfinite(v);return v
def strict(p,expected=None,max_bytes=CAP):
 pin,raw=fresh(p,expected,True,max_bytes);text=raw.decode('utf-8');del raw
 strings={};integers={}
 def intern_values(v):
  if type(v)is str:return strings.setdefault(v,v)
  if type(v)is list:
   for i,x in enumerate(v):v[i]=intern_values(x)
  return v
 def pairs(items):
  value={}
  for k,v in items:
   assert k not in value,'duplicate JSON key'
   value[k]=v
  return {strings.setdefault(k,k):intern_values(value[k])for k in sorted(value)}
 def integer(s):
  v=int(s);return integers.setdefault(v,v)
 try:value=json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=finite_float,parse_constant=bad_constant)
 finally:strings.clear();integers.clear()
 del text
 return value,pin

import re
import time
TERMINAL=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009'
REVIEW=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
DEST=Path('/private/tmp/axmat_v12_actual_build_seal_independent_readonly_audit_20261009')
DECL_SHA='410720642a1952480ad9190ed48292e96cf9f17d8ab02967b5503713caa09f5d'
PREP_SHA='f431490002fb5e2d4de0cee17979c5ef5b5725740f16fea85fdcfd3fd502ddb5'
TERM_SHA='396697c31e8112040b7fab32f452e5fabd8592ec41379d3daf2eda1519df7b28'
SEAL_SHA='1f0ddf9751140abc2eb114918695b33007725cd34839e278b2e4b04f9c779dfa'
ROOT_RETURN_SHA='049ba06c1c0295f2992e6e8a5f12b41f6da57d90151fa85d46254e5f92593f9f'
RUNTIME_SHA='8328a2a9a1c943f2d6703d9ec64ac42530c0017016b0a976645803a3256d4855'
FAMILY='OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_LINK_V12'
LABELS=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
FALSE_FIELDS=['native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted']
CHECKS=[]
def check(name,value):
 assert value,name
 CHECKS.append(name)
def get(p,sha=None):return strict(p,sha)[0]
def inventory_exact(root,expected,additional=None):
 files={};dirs=[];links={};pins={}
 for current,folders,names in os.walk(normal(root),followlinks=False):
  rel=Path(current).relative_to(root)
  if rel.parts:dirs.append(str(rel))
  for name in folders+names:
   p=Path(current)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p)
  for name in names:
   p=Path(current)/name
   if not p.is_symlink():
    pin,_=fresh(p);r=str(p.relative_to(root));files[r]=pin['sha256'];pins[r]=pin
 actual=dict(files=files,symlinks=links,directories=sorted(dirs))
 expected_files=dict(expected['files'])
 if additional:expected_files.update(additional)
 check('exact inventory '+str(root),actual==dict(files=expected_files,symlinks=expected['symlinks'],directories=expected['directories']))
 return actual,pins,sum(pin['bytes'] for pin in pins.values())
def zero_actual(value,label):
 check(label+' actual Root typed integer zero',value['record_producer']=='root' and value['actual_tool_terminal_return_observed'] is True and value['record_written_after_actual_terminal_return'] is True and type(value['returncode']) is int and value['returncode']==0 and type(value['actual_tool_result']['exit_code']) is int and value['actual_tool_result']['exit_code']==0)
def floatbound(value,lo,hi):return type(value)in(int,float) and math.isfinite(value) and lo<=value<hi
def resources(value,d,label,archive_size):
 check(label+' original scope and caps',value['artifact_budget_bytes']==96*2**30 and value['min_free_bytes']==8*2**30 and value['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and value['resource_scope_contract']==d['resource_scope_contract'] and value['declared_resource_roots']==d['resource_roots'] and set(d['resource_roots']).issubset(value['resource_roots']) and type(value['artifact_bytes'])is int and archive_size<=value['artifact_bytes']<=96*2**30 and type(value['disk_free_bytes'])is int and value['disk_free_bytes']>=8*2**30)
 check(label+' normalized distinct live roots',len(value['resource_roots'])==len(set(value['resource_roots'])) and value['resource_roots']==sorted(value['resource_roots']) and all(Path(p).is_absolute() and '..'not in Path(p).parts and str(Path(p))==p for p in value['resource_roots']))
 return dict(artifact_bytes=value['artifact_bytes'],disk_free_bytes=value['disk_free_bytes'],scope_root_count=len(value['resource_roots']),artifact_budget_bytes=value['artifact_budget_bytes'],min_free_bytes=value['min_free_bytes'])
def nm_symbols(text):
 result=[]
 for line in text.splitlines():
  if not line.strip():continue
  match=re.fullmatch(r'\s*([0-9a-fA-F]+)\s+([A-Za-z])\s+(\S+)\s*',line)
  if match:
   if match[2].upper()!='U':result.append(dict(address=match[1],kind=match[2],name=match[3]))
  else:assert re.fullmatch(r'\s*U\s+\S+\s*',line),line
 return result
def nm_objects(text,paths):
 aliases={str(Path(p)):str(Path(p)) for p in paths}
 for p in paths:
  base=Path(p).name;assert base not in aliases;aliases[base]=p
 sections={};current=None
 for line in text.splitlines():
  if line.endswith(':')and line[:-1]in aliases:
   current=aliases[line[:-1]];assert current not in sections;sections[current]=[]
  elif line.strip():assert current is not None;sections[current].append(line)
 assert set(sections)==set(paths)
 return {p:nm_symbols('\n'.join(lines))for p,lines in sections.items()}
def deps_sections(text,paths):
 result={};current=None
 for line in text.splitlines():
  if line.endswith(':')and line[:-1]in paths:
   current=line[:-1];assert current not in result;result[current]=[]
  elif line.strip():assert current is not None and line.startswith(('\t',' '));result[current].append(line.strip())
 assert set(result)==set(paths)and all(result.values())
 return result

def main():
 root,root_pin=strict(REVIEW/'Root_actual_build_tool_terminal_return.json',ROOT_RETURN_SHA);zero_actual(root,'Root build receipt')
 check('closed exact genuine build tool',root['initial_chunk_id']=='83e71b' and root['closed_session_id']==95394 and root['actual_tool_result']['chunk_id']=='f5ceb8' and root['actual_tool_result']['output']=='')
 term,term_pin=strict(TERMINAL/'terminal_return.json',TERM_SHA);zero_actual(term,'external terminal')
 check('new exact terminal schema',term['schema']==PREFIX+'_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1' and term['actual_tool_result']==root['actual_tool_result'])
 d,decl_pin=strict(OUT/'declaration.json',DECL_SHA)
 seal,seal_pin=strict(OUT/'seal.json',SEAL_SHA)
 check('fresh declaration and seal schemas',d['schema']==PREFIX+'_DECLARATION_V1'and seal['schema']==PREFIX+'_BUILD_SEAL_V1')
 check('immutable identity chain',root['terminal_evidence']==dict(path=str(TERMINAL/'terminal_return.json'),sha256=TERM_SHA) and root['source']==term['source']==dict(path=str(FACTORY),sha256=FACTORY_SHA) and root['declaration']==term['declaration']==dict(path=str(OUT/'declaration.json'),sha256=DECL_SHA) and root['build_seal']==term['build_seal']==dict(path=str(OUT/'seal.json'),sha256=SEAL_SHA) and root['prepare_terminal']==term['prep_terminal_evidence']==dict(path=str(TERMINAL/'declaration_terminal_return.json'),sha256=PREP_SHA))
 factory_pin,_=fresh(FACTORY,FACTORY_SHA);helper_pin,_=fresh(HELPER,HELPER_SHA)
 prep,prep_pin=strict(TERMINAL/'declaration_terminal_return.json',PREP_SHA);zero_actual(prep,'PREP terminal')
 check('PREP schema matches new successful declaration',prep['schema']==PREFIX+'_ACTUAL_EXTERNAL_PREP_RETURN_V1'and prep['declaration']==term['declaration'])
 snapshot,source_snapshot_pin=strict(prep['source_inventory']['path'],prep['source_inventory']['sha256'])
 check('complete original eleven SOURCE inventory',snapshot==d['source_inventory']and set(snapshot['files'])==FULL_SOURCE_NAMES and snapshot['symlinks']=={})
 source_inventory,source_pins,source_bytes=inventory_exact(SOURCE,snapshot)
 check('installed sources exact preserved',source_inventory['files']['historical_input_combined_runtime_factory.py']==FACTORY_SHA and source_inventory['files']['runtime/graph.py']==HELPER_SHA and source_inventory['files']['input_specs.json']==SPECS_SHA)
 out_inventory,out_pins,out_bytes=inventory_exact(OUT,seal,{'seal.json':SEAL_SHA})
 check('21 sealed members plus only seal file',len(seal['files'])==21 and len(out_pins)==22 and len(seal['directories'])==5 and seal['symlinks']=={})
 check('graph storage under unchanged 64MiB cap',out_pins['input_graph.json']['bytes']<CAP and out_pins['input_graph.json']['sha256']==d['input_graph']['sha256']=='4ba5f793ca13018d2d9ac5d29d76827a1503b0368c7e5c9f70ba08e0435f0c9e')
 check('complete caps unchanged',(d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['threads'],d['numeric_children_at_once'],d['retries'],d['archive_reserve_bytes'],d['artifact_budget_bytes'],d['min_free_bytes'])==(1800,600,512,1,1,0,2*2**30,96*2**30,8*2**30)and d['complete_archive_scope_roots']==[str(SOURCE),str(OUT)]and d['stages']==LABELS)
 archive_size=source_bytes+out_bytes
 check('fresh complete SOURCE plus OUT byte accounting',archive_size==term['actual_archive_bytes']==159526441 and 0<archive_size<2*2**30)
 result=get(OUT/'driver_result.json',seal['files']['driver_result.json']);audit=get(OUT/'audit/result.json',seal['files']['audit/result.json']);binary=get(OUT/'audit/binary_identity.json',seal['files']['audit/binary_identity.json'])
 check('complete build identity classification',result['classification']=='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'and result['error'] is None and result['fresh_cold_AAA_required'] is True and audit['classification']=='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'and audit['binary_status']=='PASS'and audit['declaration_sha256']==DECL_SHA)
 check('all scope flags preserved false',all(result[k]is False and audit[k]is False for k in FALSE_FIELDS)and all(term[k]is False and root[k]is False for k in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']))
 check('whole seven INPUT binding unchanged',audit['historical_whole_component_body']==d['historical_whole_component_body']==prep['historical_whole_component_body']and audit['actual_last_cprime_trim_component_INPUT']==d['actual_last_cprime_trim_component_INPUT']and d['historical_whole_component_body']['sha256']==SPECS_SHA and d['historical_whole_component_body']['whole_seven_key_body_retained']is True and d['historical_whole_component_body']['original_component_API_execution_claimed']is False and d['historical_whole_component_body']['historical_FAILED_RUN_promoted']is False)
 fresh(SPECS,SPECS_SHA)
 stages=get(OUT/FAMILY/'stages.json',seal['files'][FAMILY+'/stages.json'])['stages']
 old=ART/'axial-material-rank1-factor-cache-build-20261007';physical=ART/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007';dedup=ART/'axial-material-rank1-factor-cache-memory-dedup-build-20261007';trim=ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
 objects=d['actual_production_objects'];targets=list(map(str,[OUT/'runtime/Dragon',old/'runtime/Dragon',physical/'runtime/Dragon',dedup/'runtime/Dragon',trim/'runtime/Dragon']))
 commands=[d['production_link_command'],['/usr/bin/nm','-g',*objects],['/usr/bin/nm','-g',str(OUT/'runtime/Dragon')],['/usr/bin/otool','-L',*targets],[d['python_command'],str(FACTORY),'audit-build','--sha256',DECL_SHA,'--prep-sha256',PREP_SHA]]
 check('exact five original stage commands and PASS',len(stages)==5 and [s['label']for s in stages]==LABELS and [s['command']for s in stages]==commands and all(s['status']=='PASS' for s in stages))
 watches=[];resource_summaries=[]
 for stage in stages:
  label=stage['label'];watch=get(OUT/(label+'.watchdog.json'),seal['files'][label+'.watchdog.json']);watches.append(watch)
  check(label+' direct own child typed zero and log',watch['command']==stage['command'] and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and floatbound(watch['sampled_peak_rss_mib'],0,512) and floatbound(watch['elapsed_seconds'],0,watch['wall_cap_seconds']) and type(watch['wall_cap_seconds'])in(int,float)and 0<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and stage['log_sha256']==out_pins[label+'.log']['sha256'] and type(watch['pid'])is int and watch['pid']>0)
  for position in ['resource_before','resource_after']:resource_summaries.append(dict(label=label,position=position,**resources(stage[position],d,label+' '+position,0)))
 check('watchdog result/audit exact equality',watches==result['watchdogs'] and watches[:-1]==audit['previous_stage_watchdogs'] and len({w['pid']for w in watches})==5)
 check('actual audit child peak under original cap',watches[-1]['sampled_peak_rss_mib']==508.671875)
 raw=get(OUT/'raw_metadata_receipt.json',seal['files']['raw_metadata_receipt.json'])
 check('all four complete metadata before gates',raw==dict(files={label+'.log':out_pins[label+'.log']['sha256']for label in LABELS[:4]},before_binary_identity_gates=True,complete_raw_tools_and_link_stdout=True))
 claim=get(OUT/'execution_claim.json',seal['files']['execution_claim.json'])
 check('single no retry actual execution claim',type(claim['parent_pid'])is int and claim['parent_pid']>0 and claim['declaration_sha256']==DECL_SHA and claim['retries']==0 and claim['prep_terminal_evidence']==term['prep_terminal_evidence'])
 stdout,stdout_pin=strict(term['full_stdout']['path'],term['full_stdout']['sha256']);stderr_pin,stderr=fresh(term['full_stderr']['path'],term['full_stderr']['sha256'],True)
 check('separate complete streams paths',term['full_stdout']['path']==str(TERMINAL/'build_full_stdout.json')and term['full_stderr']['path']==str(TERMINAL/'build_full_stderr.txt')and len({str(TERMINAL/'terminal_return.json'),term['full_stdout']['path'],term['full_stderr']['path']})==3 and stderr==b'')
 tail={k:term[k]for k in ['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']}
 check('whole full stdout and all four exact tails',stdout==dict(result=result,**tail)and tail['actual_tail_check']=='PASS'and floatbound(result['elapsed_seconds'],0,tail['actual_elapsed_seconds']+1e-10)and floatbound(tail['actual_elapsed_seconds'],result['elapsed_seconds'],1800))
 check('exact actual external run-build command',term['command']==[d['python_command'],str(FACTORY),'run-build','--sha256',DECL_SHA,'--prep-sha256',PREP_SHA]and term['actual_tool_provenance']['initial_chunk_id']=='83e71b'and term['actual_tool_provenance']['session_id']==95394 and term['actual_tool_provenance']['bytecode_disabled_environment']is True)
 tail_resources=resources(tail['actual_resources'],d,'actual complete tail',archive_size);driver_resources=resources(result['resources'],d,'driver closeout',result['archive_bytes_before_closeout'])
 check('driver precloseout smaller than exact sealed full archive',type(result['archive_bytes_before_closeout'])is int and 0<result['archive_bytes_before_closeout']<archive_size)
 # Independent parse of recorded nm/otool text, with no new tool execution or business API.
 logs={label:(OUT/(label+'.log')).read_text(encoding='utf-8')for label in LABELS[1:4]}
 object_symbols=nm_objects(logs['metadata/objects'],objects);executable_symbols=nm_symbols(logs['metadata/executable']);names=['_spot1p64_','_spoasm_','_flu2dr64_','_flu_'];defs={};object_pins=[]
 for p,name in zip(objects,names):
  pin,_=fresh(p,d['files'][p]);object_pins.append(pin)
  oh=[s for s in object_symbols[p]if s['name']==name and s['kind'].upper()=='T'];eh=[s for s in executable_symbols if s['name']==name and s['kind'].upper()=='T'];assert len(oh)==len(eh)==1
  defs[name]=dict(object=dict(path=p,sha256=pin['sha256']),object_symbol=oh[0],executable_symbol=eh[0])
 check('four genuine objects and complete raw symbol equality',defs==binary['actual_object_definitions']and objects==[str(trim/'build/SPOT1P64.o'),str(physical/'build/SPOASM.o'),str(old/'build/FLU2DR64.o'),str(ART/'axial-material-moment-order-build-20261006/build/FLU.o')])
 forbidden=('axmat_capture','axmat_rank1_capture','spot1p64_original','spot1p64_dense','original_cache_mod','dense_cache_mod','physical_unit')
 check('recorded executable observer symbols absent',not any(any(word in row['name'].lower()for word in forbidden)for row in executable_symbols))
 deps=deps_sections(logs['metadata/dependencies'],targets)
 check('complete old/component/combined dependencies exact',deps==binary['dependencies']and all(deps[p]==deps[targets[0]]for p in targets[1:]))
 check('new runtime exact independently hashbound',binary['actual_runtime']==result['corrected_runtime']==root['runtime']==dict(path=str(OUT/'runtime/Dragon'),sha256=RUNTIME_SHA)and out_pins['runtime/Dragon']['sha256']==RUNTIME_SHA)
 old_decl=get(old/'declaration.json',d['files'][str(old/'declaration.json')]);original=old_decl['build_commands'][2];archive=str(ROOT/'lib/Darwin_arm64/libDragon.a');old_kernel=str(old/'build/SPOT1P64.o');fixed=list(original)
 assert fixed.count(old_kernel)==1 and fixed.count(archive)==1 and fixed[-2:]==['-o',str(old/'runtime/Dragon')]
 fixed[fixed.index(old_kernel)]=objects[0];fixed.insert(fixed.index(archive),objects[1]);fixed[-1]=str(OUT/'runtime/Dragon')
 inverse=list(fixed);inverse.remove(objects[1]);inverse[inverse.index(objects[0])]=old_kernel;inverse[-1]=str(old/'runtime/Dragon')
 expected_linkproof=dict(original_link_command=original,combined_link_command=fixed,exact_original92_token_inverse=True,sole_object_changes=['SPOT1P64.o','SPOASM.o'],all_other_objects_flags_library_tokens_unchanged=True,observer_objects_linked=False)
 check('original full link inverse unchanged remaining tokens',inverse==original and fixed==d['production_link_command'] and expected_linkproof==d['link_inverse'])
 check('raw metadata identity pins all current',binary['raw_metadata']=={label:dict(path=str(OUT/(label+'.log')),sha256=out_pins[label+'.log']['sha256'])for label in LABELS[1:4]})
 check('binary INPUT ONLY flags and exact inverse',binary['status']=='PASS'and binary['exact_original92_token_inverse']is True and binary['sole_object_changes']==['SPOT1P64.o','SPOASM.o']and binary['all_other_original_link_inputs_unchanged']is True and binary['production_references_and_observers_excluded']is True and all(binary[k]is False for k in ['whole_instruction_equivalence_claimed','actual_full_FLU_entry_executed','combined_runtime_native_RSS_proved','AAA_accuracy_qualified','ABA_admitted']))
 # No new parse of the complete graph/historical phase: preserve the exact prior peer PREP result.
 prior,pprior=strict(Path('/private/tmp/axmat_v12_actual_prepare_source_graph_independent_audit_20261009/REPORT.json'),'515aaf19d8cbfaf218316345d4c12e569eb451d2400fb2edb22e567adb771ad9')
 report=dict(schema='AXMAT_V12_CLOSED_ACTUAL_BUILD_INDEPENDENT_READONLY_AUDIT_V1',status='PASS_CLOSED_BUILD_LINK_IDENTITY_EVIDENCE_ONLY',checked_unix=time.time(),checks=CHECKS,root_actual_build_receipt=root_pin,actual_external_terminal=term_pin,declaration=decl_pin,prep_terminal=prep_pin,seal=seal_pin,canonical_factory=factory_pin,canonical_graph_helper=helper_pin,source_exact_inventory=source_inventory,source_fresh_file_pins=source_pins,out_exact_inventory=out_inventory,out_fresh_file_pins=out_pins,source_bytes=source_bytes,out_bytes_including_seal=out_bytes,actual_source_plus_out_bytes=archive_size,actual_complete_stdout=stdout_pin,actual_complete_stderr=stderr_pin,stage_labels=LABELS,actual_stage_watchdogs=watches,actual_total_elapsed_seconds=tail['actual_elapsed_seconds'],driver_elapsed_seconds=result['elapsed_seconds'],audit_child_sampled_peak_rss_mib=watches[-1]['sampled_peak_rss_mib'],rss_margin_mib=512-watches[-1]['sampled_peak_rss_mib'],recorded_resources=resource_summaries,driver_closeout_resources=driver_resources,complete_tail_resources=tail_resources,corrected_runtime=binary['actual_runtime'],production_object_fresh_pins=object_pins,complete_raw_symbol_and_dependency_identity_reconstructed=True,original_link_complete_inverse=expected_linkproof,prior_independent_PREP_full_graph_report=pprior,full_graph_or_business_phase_reexecuted=False,business_imports_or_calls=False,project_writes=False,new_native_run_executed=False,build_native_RSS_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False,known_pure_metadata_reader_error=dict(chunk_id='967997',exit_code=1,reason='Initial reader guessed nonexistent OUT/runtime/build_identity.json; current combined uses audit/binary_identity.json. No business or source error; no business retry.'),limitations=['508.671875MiB is actual audit own-child sampled peak; it does not certify native Dragon or cold controller RSS.','This tool rehashes exact immutable SOURCE/OUT and parses sealed metadata/streams; it never imports or reruns production admission, historical full phase, or mathematical controls.','Full graph logical content and original seven INPUT body were independently audited after PREP; this report hashes the same graph and SOURCE pins and references that frozen audit.'])
 path=DEST/'REPORT.json';assert not path.exists();path.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n');pin,_=fresh(path);print(json.dumps(dict(status=report['status'],report=pin,checks=len(CHECKS),source_files=len(source_pins),sealed_files=len(seal['files']),source_plus_out_bytes=archive_size,actual_total_elapsed_seconds=tail['actual_elapsed_seconds'],actual_audit_child_peak_mib=watches[-1]['sampled_peak_rss_mib']),ensure_ascii=False))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Finite independent review of actual SOURCE binding, no project execution."""
from pathlib import Path
import ast,hashlib,json,math,stat
DEST=Path(__file__).absolute().parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_graph_fresh_verifier_v21_sources';E=B/'actual_complete_graph_fresh_verifier_v21_receipts'
T=Path('/private/tmp/axmat_v21_complete_fresh_verifier_ART_roots_SOURCE_fix_20261010_angular_ws815t4g')
PRIOR=Path('/private/tmp/axmat_v21_fresh_probe_ART_root_fix_independent_SOURCE_review_20261010/INDEPENDENT_REVIEW.json')
SHA=dict(driver='ee552f1458957281a695f84c8cd74fb8c25450228eaa6aec4bbd48601d29395a',
host='3633e8ea03992293b6a481f49baa0c783a28446fbca2e37325177cd6c9e3fba2',
freeze='e7ef597da8a46cb84627346d1664a6a4d8b2babae32ee9100c8dfd484b724171',
result='83ca26fe59485aa6ea770854d7ae00b52c83fea84a1ecfc29a0de389105903c4',
manifest='a459771501251a152ac596df26d2ffb93190a40386bb03f4a1b1f974e223316a',
helper='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7',
witness='f8e83e8ca68397f30657ed5a8fc5b0f2fdcb0e4bd8071a006cca75ba570a68b9')
PINS=[];CHECKS=[]
def sha(x):return hashlib.sha256(x).hexdigest()
def id7(p,regular=True):
 s=p.lstat()
 if regular and (not stat.S_ISREG(s.st_mode) or s.st_nlink!=1):raise ValueError('fixed normal single-link SOURCE/META required')
 if not regular and (not stat.S_ISDIR(s.st_mode) or p.is_symlink()):raise ValueError('fixed normal SOURCE directory required')
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def check(name,truth):
 if type(truth)is not bool or not truth:raise AssertionError(name)
 CHECKS.append(dict(name=name,typed_bool=True,value=True))
def read(p,want=None):
 a=id7(p);raw=p.read_bytes();b=id7(p)
 if a!=b or len(raw)!=a[4] or (want is not None and sha(raw)!=want):raise ValueError('complete SOURCE/META EOF SHA7ID changed')
 PINS.append(dict(path=str(p),sha256=sha(raw),identity7=a,size_bytes=len(raw)));return raw
def pairs(values):
 out={}
 for k,v in values:
  if k in out:raise ValueError('duplicate Root SOURCE metadata key')
  out[k]=v
 return out
def reject(v):raise ValueError('nonfinite Root SOURCE metadata '+v)
def obj(raw):
 value=json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)
 def finite(v):
  if type(v)is float and not math.isfinite(v):raise ValueError('nonfinite Root Source metadata number')
  if type(v)is dict:
   for x in v.values():finite(x)
  elif type(v)is list:
   for x in v:finite(x)
 finite(value)
 if type(value)is not dict:raise ValueError('complete Root Source metadata object required')
 return value
def typed(p):
 check('typed exact Source pin '+str(p.get('path')),type(p)is dict and set(p)=={'path','sha256','identity'} and type(p['path'])is str and Path(p['path']).is_absolute() and type(p['sha256'])is str and len(p['sha256'])==64 and all(x in '0123456789abcdef' for x in p['sha256']) and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity']))
 raw=read(Path(p['path']),p['sha256']);check('actual current complete Source pin '+p['path'],PINS[-1]['identity7']==p['identity']);return raw
def dump(x):return ast.dump(x,include_attributes=False)
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def globals_(tree):
 return {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def segment(raw,node):return ''.join(raw.decode().splitlines(True)[node.lineno-1:node.end_lineno])
def write(name,v):
 raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
 with (DEST/name).open('xb') as f:f.write(raw)
 return dict(path=str(DEST/name),sha256=sha(raw),size_bytes=len(raw),identity7=id7(DEST/name))
def main():
 dir_before=id7(D,False)
 freeze=obj(read(E/'Root_generated_full_SOURCE_namespace_freeze.json',SHA['freeze']))
 result=obj(read(E/'Root_generated_SOURCE_binding_only.json',SHA['result']))
 prior=obj(read(PRIOR,'01b90b3ccda13ac7cb57128a4f5f8c075cbde253419260f4e910f41bfd220d1d'))
 check('prior full SOURCE pass exact122 independent checks',prior['status']=='SOURCE_PASS_FOR_ROOT_METADATA_BINDING_ONLY_NOT_RUNTIME_QUALIFICATION' and prior['independent_check_count']==122 and prior['blockers']==[])
 check('Root real generated Source freeze complete contract',freeze['schema']=='AXMAT_V21_ROOT_GENERATED_FRESH_VERIFIER_SOURCE_FREEZE_V1' and freeze['source_root']==str(D) and freeze['source_directory_identity']==dir_before and freeze['symlinks']==[] and freeze['subdirectories']==[] and freeze['no_SOURCE_append_after_freeze']is True and freeze['actual_runtime_executed']is False)
 filepins=freeze['complete_files']
 check('actual Source count23 complete regular flat inventory',len(filepins)==result['source_file_count']==23 and len({x['path'] for x in filepins})==23 and {p.name for p in D.iterdir()}=={Path(x['path']).name for x in filepins} and all(Path(x['path']).parent==D for x in filepins))
 raws={}
 for p in filepins:raws[Path(p['path']).name]=typed(p)
 check('Root exact driver and host hashes and sizes',sha(raws['fresh_verifier_controls.py'])==SHA['driver'] and len(raws['fresh_verifier_controls.py'])==23482 and sha(raws['fresh_verifier_host.py'])==SHA['host'] and len(raws['fresh_verifier_host.py'])==24650)
 manifestraw=read(T/'MANIFEST.json',SHA['manifest']);manifest=obj(manifestraw)
 check('source package exact manifest copy full17 originalmembers',raws['TEMPLATE_PACKAGE_MANIFEST.json']==manifestraw and manifest['member_count']==len(manifest['members'])==17)
 for p in manifest['members']:
  raw=read(T/p['name'],p['sha256'])
  check('actual copied entire Source package member '+p['name'],raw==raws[p['name']] and len(raw)==p['size_bytes'] and PINS[-1]['identity7']==p['identity'])
 inverse=obj(raws['actual_READY_binding_complete_SOURCE_inverse.json'])
 check('actual complete Source inverse shape',inverse['schema']=='AXMAT_V21_ROOT_BOUND_FRESH_VERIFIER_SOURCE_INVERSES_V1' and len(inverse['driver_hunks'])==6 and len(inverse['host_hunks'])==5)
 changed_globals={}
 for kind,fn,allowed in [('driver','fresh_verifier_controls',{'SOURCE_STATUS','NEW_HELPER_PATH','NEW_HELPER_SHA256','NEW_HELPER_SOURCE_BYTES','NEW_HELPER_IDENTITY','OUTPUT_PATH'}),('host','fresh_verifier_host',{'SOURCE_STATUS','TARGET_SHA','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN'})]:
  current=raws[fn+'.py'];template=raws[fn+'.UNREADY.py'];restored=current.decode()
  for i,h in reversed(list(enumerate(inverse[kind+'_hunks']))):
   check(kind+' full6/5 inverse unique '+str(i),restored.count(h['after'])==1)
   restored=restored.replace(h['after'],h['before'],1)
  check(kind+' whole actual binding inverse bytes AST',restored.encode()==template and dump(ast.parse(restored))==dump(ast.parse(template)))
  a,b=ast.parse(current),ast.parse(template);ad,bd=defs(a),defs(b)
  check(kind+' entire function names/order exact',list(ad)==list(bd))
  for name in ad:check(kind+' whole function byteexact '+name,segment(current,ad[name])==segment(template,bd[name]))
  ag,bg=globals_(a),globals_(b);check(kind+' full module globals inventory exact',list(ag)==list(bg))
  changed={n for n in ag if dump(ag[n])!=dump(bg[n])}
  check(kind+' only6/5 globals changed',changed==allowed);changed_globals[kind]=sorted(changed)
  for raw in (current,template):ast.parse(raw);compile(raw,fn,'exec',dont_inherit=True,optimize=0)
 check('no unknown actual newQ or business successes introduced',all(inverse[k]is None for k in ('UNKNOWN_Q','UNKNOWN_BUSINESS_PINS')) and all(inverse[k]is False for k in ('actual_controls_run','helper_metadata_qualified','whole_business_INPUT','native','AAA','ABA','physics_balance')) and result['UNKNOWN_Q']is None and result['UNKNOWN_BUSINESS_PINS']is None and all(result[k]is False for k in ('helper_API_guard_business_numeric_executed','helper_metadata_qualified','whole_business_INPUT','native','AAA','ABA','physics_balance','external_Root_terminal_fabricated')))
 check('actual Source-only binding metadata correct schema status caps',result['schema']=='AXMAT_V21_ROOT_FRESH_VERIFIER_SOURCE_BINDING_ONLY_V1' and result['status']=='SOURCE_READY_BINDING_GENERATED_NOT_EXECUTED' and [result[k] for k in ('whole_seconds','stage_seconds','rss_mib','joint_HOST_SOURCE_OUT_receipts_archive_bytes','history_bytes','min_free_bytes','threads','children','retries')]==[1800,600,512,64*2**20,96*2**30,8*2**30,1,1,0])
 helper=result['installed_helper'];helperraw=typed(helper)
 check('actual new canonical helper Source exact qualified Source candidate only',helper['path']=='/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py' and helper['sha256']==SHA['helper'] and len(helperraw)==helper['identity'][4]==147870 and inverse['helper']==helper)
 witnessraw=typed(result['actual_install_witness']);witness=obj(witnessraw)
 check('actual exact Source witness copy SHA schema',sha(witnessraw)==SHA['witness'] and raws['installed_SOURCE_witness_exact_copy.json']==witnessraw and witness['schema']=='ROOT_V21_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1' and witness['closed']is True and witness['actual_tool_terminal_return_observed']is True and witness['source_only']is True)
 tr=witness['terminal_tool_return']
 check('actual observed installation terminal typedinteger0closed exact original JSON',type(tr)is dict and type(tr.get('exit_code'))is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='464ada' and type(tr['output'])is str and type(tr['wall_time_seconds'])in(int,float) and math.isfinite(tr['wall_time_seconds']) and tr['wall_time_seconds']>=0)
 output=obj(tr['output'])
 check('witness exact integers genuinely from preserved actual terminal output',witness['exact_integer_pins_decoded_from_actual_terminal_output']is True and witness['original_actual_terminal_output_preserved_exact']is True and output['installed_helper']==witness['installed_helper']==helper and output['source_install_record']==witness['source_install_record']==result['source_install_record'])
 check('install witness has no protocol/business/science success',witness['actual_new_helper_qualification_sha256']is None and all(witness[k]is False for k in ('actual_pure_helper_protocol_qualified','actual_full_current_graph_verifier_qualified','complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')))
 recordraw=typed(result['source_install_record']);record=obj(recordraw)
 check('actual complete Source record copy helper and false future qualifiers',recordraw==raws['installed_SOURCE_record_exact_copy.json'] and record['installed_helper']==helper and record['source_only']is True and record['actual_new_helper_qualification_sha256']is None and all(record[k]is False for k in ('actual_pure_helper_protocol_qualified','actual_full_current_graph_verifier_qualified','actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','business_or_guard_or_helper_API_executed')))
 dg=globals_(ast.parse(raws['fresh_verifier_controls.py']));hg=globals_(ast.parse(raws['fresh_verifier_host.py']))
 check('all actual6 driver globals exactly metadata sourced',ast.literal_eval(dg['SOURCE_STATUS'])=='READY_SOURCE_BOUND_BY_ROOT' and ast.literal_eval(dg['NEW_HELPER_PATH'])==helper['path'] and ast.literal_eval(dg['NEW_HELPER_SHA256'])==helper['sha256'] and type(ast.literal_eval(dg['NEW_HELPER_SOURCE_BYTES']))is int and ast.literal_eval(dg['NEW_HELPER_SOURCE_BYTES'])==147870 and ast.literal_eval(dg['NEW_HELPER_IDENTITY'])==helper['identity'] and ast.literal_eval(dg['OUTPUT_PATH'])=='/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21-20261010')
 check('all actual5 host globals exactly source/metadata pins',ast.literal_eval(hg['SOURCE_STATUS'])=='READY_SOURCE_BOUND_BY_ROOT' and ast.literal_eval(hg['TARGET_SHA'])==SHA['driver'] and ast.literal_eval(hg['BOUND_HELPER_PIN'])==helper and ast.literal_eval(hg['INSTALL_WITNESS_PIN'])==result['actual_install_witness'] and ast.literal_eval(hg['SOURCE_INSTALL_RECORD_PIN'])==result['source_install_record'])
 for k in ('UNKNOWN_Q','UNKNOWN_BUSINESS_PINS'):check('both actual templates '+k+' remainNone',ast.literal_eval(dg[k])is None and ast.literal_eval(hg[k])is None)
 check('actual Source lexical5 roots retained and full archive scope unchanged',all(x in raws['fresh_verifier_host.py'].decode() for x in ('declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)','path==support.ART or not path.is_relative_to(support.ART)','support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20','len(sys.argv)!=1')))
 check('inverse receipts point exactly actual driver host witness record',inverse['driver']==result['driver'] and inverse['host']==result['host'] and inverse['actual_closed_SOURCE_witness']==result['actual_install_witness'] and inverse['actual_source_record']==result['source_install_record'])
 check('copied driver full27/private4positive3reject/37111+1 and gzip contract unchanged by entirefunction bytes',prior['all27_return_fields_types_order_floatbits_whole_contract_retained']is True and prior['full37111plus1_actual_read_open_contract_retained']is True and prior['full_unfiltered_gzip_trace_and_return_contract_retained']is True and prior['private4positives3rejects_and_full_calleridentity_contract_retained']is True)
 for p in PINS:
  q=Path(p['path']);a=id7(q);raw=q.read_bytes();b=id7(q)
  if a!=b or b!=p['identity7'] or len(raw)!=p['size_bytes'] or sha(raw)!=p['sha256']:raise ValueError('actual complete Source/RootMETA changed after review')
 check('complete frozen Source directory unchanged after allreads',id7(D,False)==dir_before and {q.name for q in D.iterdir()}==set(raws))
 rp=write('INDEPENDENT_REVIEW.json',dict(schema='AXMAT_V21_ACTUAL_BOUND_FRESH_PROBE_FINITE_SOURCE_REVIEW_V1',status='SOURCE_PASS_ACTUAL_ROOT_BOUND_DRIVER_HOST_NOT_RUNTIME_QUALIFICATION',independent_checks=CHECKS,independent_check_count=len(CHECKS),blockers=[],Source_directory_identity_before_after=dir_before,actual_frozen_Source_files=23,full_freeze_sha256=SHA['freeze'],Source_binding_result_sha256=SHA['result'],Source_package_manifest_sha256=SHA['manifest'],actual_driver_sha256=SHA['driver'],actual_host_sha256=SHA['host'],actual_driver_bytes=23482,actual_host_bytes=24650,actual11_global_bindings=changed_globals,full6_driver5_host_inverse_to_actual_a459_templates=True,all14driver8host_functions_byteexact=True,all_other_globals_imports_module_scope_restored_byteexact=True,all_27_return_gzip37111plus1_private4positive3reject_fullSource7ID_contracts_retained=True,Root_install_actual_typed0closed_integer_pin_preserved_output_verified=True,actual_helper_source_only_pin=helper,actual_witness_source_only_pin=result['actual_install_witness'],no_D_append_or_mutation=True,full_source_META_pins_before_after=PINS,reviewer_standard_library_Source_smallRootMETA_only=True,Root_reported_binding_tool_chunk='ae06c6',reviewer_external_binder_tool_receipt_read=False,actual_new_helper_Q=None,Root_prelaunch_complete_Source7ID_joint_D_E_under64_and_H_OUT_absence_recheck_required=True,project_helper_guard_API_currentgraph_ARTpayload_numeric_historyscan_import_or_execution=False,canonical_ART_frozen_results_modified=False,actual_controls_or_business_run=False,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False,actual_RSS_or_memory_improvement_proven=False))
 print(json.dumps(dict(status='SOURCE_PASS_ACTUAL_ROOT_BOUND_DRIVER_HOST_NOT_RUNTIME_QUALIFICATION',review=rp,checks=len(CHECKS),blockers=0,frozen_Source_files=23,source_only=True),ensure_ascii=False))
if __name__=='__main__':main()

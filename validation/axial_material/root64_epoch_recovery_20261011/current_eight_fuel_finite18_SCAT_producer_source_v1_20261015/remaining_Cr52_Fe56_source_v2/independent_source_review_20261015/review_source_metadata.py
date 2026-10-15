"""Frozen Source eligibility review only; never import a candidate or science helper."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

HERE=Path(__file__).absolute().parent; BASE=HERE.parent; FUEL=BASE.parent/'v6'
R=Path('/Users/wen/spot'); ART=R/'validation/artifacts'
OUT=ART/'axial-material-current-remaining-Cr52-Fe56-finite9-SCAT-producer-20261015-v2'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,
 history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,
 free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
EXTRACT=ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence'
EXCEPTIONS={str(EXTRACT/(n+'_actual_saved_MT5_P0.json')) for n in
 ('U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55')}
LARGE={str(ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1'/n)
 for n in ('Root_actual_all34_original_ASCII_infinite_SCAT_summary.json','inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')}
LARGE.add(str(ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2/Root_actual_eight_fuel_finite18_SCAT_summary.json'))
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,
 physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,
 physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,
 finite9_replayed=False,P1_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,
 AAA_qualified=False,ABA_admitted=False,goal_complete=False)
START=time.monotonic(); HASHED={}

def need(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def limits():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(peak<512*2**20 and time.monotonic()-START<600,'review own SELF512/stage600')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def strict(raw):
 def pairs(items):
  result={}
  for k,v in items:need(k not in result,'duplicate JSON key');result[k]=v
  return result
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda value:(_ for _ in()).throw(ValueError('nonfinite JSON '+value)))
def current(p):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str
  and type(p['sha256'])is str and len(p['sha256'])==64 and all(x in '0123456789abcdef'for x in p['sha256'])
  and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7
  and all(type(v)is int for v in p['identity'])and p['identity'][4]==p['size_bytes'],'strict fullPF Python types')
 q=Path(p['path']); s=q.lstat()
 compiler=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==2
 need(q.is_absolute()and '..'not in q.parts and not any(v.is_symlink()for v in(q,*q.parents))
  and stat.S_ISREG(s.st_mode)and s.st_nlink==(2 if compiler else 1)and identity(s)==p['identity'],'current7 '+str(q))
 limits();return q
def eof(p):
 q=current(p);need(str(q)not in EXCEPTIONS and q.name not in('SCI1','SCI2')and not q.name.startswith('tape')
  and (q.suffix in('.py','.f90','.json','.jsonl','.txt','.make','.in','.sha256','.log')
       or q.name.startswith(('file_data_gendf_','file_data_dendf_'))), 'Source/report-metadata role only; no science body')
 need(p['size_bytes']<(64*2**20 if str(q)in LARGE else 8*2**20),'exact metadata role read ceiling')
 h=hashlib.sha256();n=0
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(identity(os.fstat(fd))==p['identity'],'opened7')
  while True:
   raw=os.read(fd,2**20)
   if not raw:break
   n+=len(raw);h.update(raw);limits()
  need(identity(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 current(p);need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'whole EOF/SHA '+str(q));HASHED[str(q)]=p
def read(p):
 eof(p);need(p['size_bytes']<8*2**20,'only small metadata parsed');value=strict(Path(p['path']).read_bytes());current(p);return value
def unique(rows):
 table={}
 for p in rows:need(p['path']not in table or table[p['path']]==p,'one consistent fullPF per path');table[p['path']]=p
 return list(table.values())
def contains(value,p):return value==p or type(value)is dict and any(contains(v,p)for v in value.values())or type(value)is list and any(contains(v,p)for v in value)
def terminal(tools,key,code):
 r=tools[key];need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int
  and tools['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and r.get('session_id')is None,'genuine original closed integer')
 return r
def closed(tools,key,p,outkey):need(strict(terminal(tools,key,0)['output'].strip().splitlines()[-1])[outkey]==p,'genuine stdout exact fullPF')
def definition(raw,name):
 text=raw.decode();tree=ast.parse(text);return ast.get_source_segment(text,next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)).encode()
def inverse(value):
 a=value['original_Source_pin'];b=value['candidate_Source_pin'];eof(a);eof(b)
 original=Path(a['path']).read_bytes();candidate=Path(b['path']).read_bytes();edit=value['edit']
 ob=bytes.fromhex(edit['original_bytes_hex']);cb=bytes.fromhex(edit['candidate_bytes_hex'])
 need(original[edit['original_begin_byte']:edit['original_end_byte']]==ob
  and candidate[edit['candidate_begin_byte']:edit['candidate_end_byte']]==cb,'Source inverse literal intervals')
 restored=candidate[:edit['candidate_begin_byte']]+ob+candidate[edit['candidate_end_byte']:]
 need(restored==original and value['complete_inverse_reconstructs_original']is True
  and hashlib.sha256(restored).hexdigest()==value['restored_original_sha256'],'complete original Source inverse')
def own_pin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes();need(len(raw)<8*2**20 and identity(q.lstat())==identity(s),'own bounded metadata pin')
 return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--reviewer-freeze-pin',required=True);args=ap.parse_args()
 fp=strict(args.reviewer_freeze_pin);freeze=read(fp);eof(freeze['reviewer_source_pin'])
 need(freeze['schema']=='INDEPENDENT_REMAINING_CR52_FE56_V2_SOURCE_REVIEWER_FREEZE_V1'
  and freeze['reviewer_AST_passed_before_freeze']is True and freeze['reviewer_source_pin']['path']==str(Path(__file__).absolute()),'own frozen reviewer Source')
 ready=read(freeze['ready_pin']);generation=read(freeze['canonical_generation_tools_pin'])
 need(freeze['ready_pin']['sha256']=='37ac86903c48f8d79fcd94e89f68d7e35fe9f3bde31b3c0f74cb7db9c129873c'
  and freeze['ready_pin']['size_bytes']==736766,'exact actual same-round READY')
 closed(generation,'actual_Source_preparation_return',freeze['ready_pin'],'ready_pin')
 need(generation['schema']=='ROOT_REMAINING_CR52_FE56_FINITE9_V2_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_V1'and generation['actual_Source_preparation_return']['chunk_id']=='618d4f'and generation['actual_initial_return']['session_id']==74863,'genuine new sole generation0, no adapter or rerun inferred')
 need(ready['schema']=='REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_REVIEW_READY_V1'and ready['source_only']is True
  and ready['actual_business_started']is False and ready['Root_final_publication_executed']is False
  and ready['scientific_payload_read']is False and ready['original_caps']==CAPS
  and ready['selected_Source_pins']==ready['dependencies'],'Source-only exact selected scope')
 selected=unique(ready['selected_Source_pins']+[freeze['ready_pin'],freeze['canonical_generation_tools_pin']])
 exceptions=[p for p in selected if p['path']in EXCEPTIONS]
 need(len(exceptions)==11,'eleven explicit science-valued document exceptions')
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 plan=read(ready['control_plan_pin']);proof=read(plan['original_whole_math_inverse_proof_pin']);author=read(plan['author_Pre_Root_generation_Source_freeze_pin'])
 need(plan['schema']=='REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_ONLY_PLAN_V1'and plan['original_caps']==CAPS
  and author['schema']=='AUTHOR_PRE_ROOT_REMAINING_CR52_FE56_FINITE9_V2_PERMISSION_ROUTE_SOURCE_FREEZE_V1'
  and author['Source_files_frozen_before_Root_generation']is True and author['Source_author_STOP_WRITES']is True
  and author['Source_preparation_executed_by_author']is False and author['business_executed_by_author']is False,'author frozen before sole Root generation')
 for value in (ready,plan,proof,author):
  need(all(value[k]is False for k in FALSE if k in value),'all business/qualification flags false')
 for p in author['whole_Source_file_pins']:eof(p)
 need(len(author['whole_Source_file_pins'])==10 and len(ready['complete_source_file_pins'])==11,'four candidate Sources and six whole originals plus inverse proof')
 for p in ready['complete_source_file_pins']:
  if Path(p['path']).suffix=='.py':ast.parse(Path(p['path']).read_bytes(),filename=p['path'])
 need(not os.path.lexists(OUT)and not any(os.path.lexists(BASE/n)for n in
  ('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_EXECUTION_CLAIM_RECEIPT.json')),'unexecuted output, publication and execution claim')
 prior=read(plan['inherited_complete58_plan_pin']);roots=plan['complete_joint_roots']
 need(roots==prior['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))==59
  and len(prior['complete_joint_roots'])==58 and str(BASE.parent)in roots[:-1]
  and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'retain failed58 and append only fresh OUT59')
 inherited=unique(ready['inherited_metadata_current7_pins'])
 need(inherited==plan['inherited_metadata_current7_pins']==prior['explicit_cumulative_metadata_file_pins'],'complete inherited metadata current7 scope without rehash')
 for p in inherited:current(p)
 expected=(2,1,7,63,189,2,2,14,14,126,378)
 keys=('expected_serial_children','expected_per_child_archives','expected_per_child_native_temperature_records','expected_per_child_finite_nodes','expected_per_child_leaf_records','expected_nuclides','expected_archives','expected_temperature_records','expected_archive_temperature_records','expected_finite_dilution_nodes','expected_leaf_records')
 need(tuple(plan[k]for k in keys)==expected and plan['execution_nuclides']==['Cr52','Fe56']
  and plan['original_decompressed_payload_expected_bytes']==26790912,'exact two singles/14T/126nodes/378 P0 leaves')
 science=[plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[row['current_original_input_full_pin']for row in plan['inputs']]
 need(len(plan['inputs'])==2 and [row['input_encoding']for row in plan['inputs']]==['gzip','ASCII'],'original compressed Cr52 and ASCII Fe56 routes')
 for row,name,mat in zip(plan['inputs'],('Cr52','Fe56'),(2431,2631)):
  need(row['nuclide']==name and row['mat']==mat and row['lane']=='single'and row['SCI_role']=='SCI1'
   and row['original_nimpo_unit']==0 and row['original_nexpo_unit']==30 and row['original_ipflag']==0
   and row['original_DRAGR_NBESP']==0 and row['original_expected_nz']==10
   and row['original_drahd_existing_ENERGY_REAL32_branch']is False
   and row['original_source_deck_temperatures_K']==[293.,550.,748.1500244140625,893.1500244140625,900.,1200.,2000.]
   and row['original_selfshielding_energy_bounds_eV']==[4.632489,1050830.0],'nimpo0 new-binary64 ENERGY/own infinity original exact route')
 for p in science:current(p)
 need(plan['bounded_Source_generation_metadata_reservation_bytes']==16*2**20
  and plan['bounded_new_output_reservation_bytes']==96*2**20
  and plan['new_output_reservation_components']==dict(two_child_reports=16*2**20,aggregate_report=16*2**20,host_summary=32*2**20,execution_binding=2*2**20,runtime_watch_logs_stage_other=30*2**20)
  and sum(plan['new_output_reservation_components'].values())==96*2**20
  and plan['Source_only_cumulative_bytes_before_reserved_new_metadata']+112*2**20<2*2**30,'original cumulative cap and explicit16/96MiB bounds')
 need(sum((BASE/n).stat().st_size for n in('ORIGINAL_MATH_AND_MINIMAL_SOURCE_INVERSE.json','PLAN.json','SOURCE_REVIEW_READY.json'))<16*2**20,'three generated metadata roles actual total below16MiB')
 for prefix,status in (('prior_fuel','PASS_ACTUAL_EIGHT_FUEL_64T_128LANET_1152NODES_3456_FINITE_P0_LEAF_WORDS'),('current_temperature','PASS_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_ONLY_POSTVERIFICATION')):
  root=read(plan[prefix+'_actual_tools_pin']);post=read(plan[prefix+'_actual_post_pin']);tools=read(plan[prefix+'_actual_post_tools_pin'])
  closed(root,'actual_terminal_return',plan[prefix+'_actual_summary_pin'],'report_pin');closed(tools,'actual_review_return',plan[prefix+'_actual_post_pin'],'review_pin')
  need(post['status']==status and post['failure']is None and contains(post,plan[prefix+'_actual_summary_pin'])
   and contains(post,plan[prefix+'_actual_tools_pin']),'actual completed prerequisite and sole post0 linkage')
 failed=read(plan['prior_fullv5_failed_tools_pin']);terminal(failed,'actual_terminal_return',1)
 facts=read(plan['prior_fullv5_failure_post_pin']);factst=read(plan['prior_fullv5_failure_post_tools_pin'])
 closed(factst,'actual_review_return',plan['prior_fullv5_failure_post_pin'],'review_pin')
 need(facts['status']=='PASS_FAILURE_FACTS_ONLY'and facts['actual_Root_original_integer_exit_code']==1
  and facts['actual_child_original_integer_exit_code']==1 and facts['actual_host_report_pin']==plan['prior_fullv5_failed_summary_pin']
  and facts['actual_Root_true_tools_pin']==plan['prior_fullv5_failed_tools_pin'],'prior fullv5 original1 preserved, not converted to control pass')
 for row in proof['whole_original_source_copies']:
  a=row['original_full_pin'];b=row['whole_unchanged_copy_full_pin'];eof(a);eof(b)
  need(Path(a['path']).read_bytes()==Path(b['path']).read_bytes(),'whole original helper bytes unchanged')
 need(len(proof['whole_original_source_copies'])==6,'all six original scalar/SCI/stream/Fortran/guard/publisher copies')
 for key in('worker_complete_byte_inverse','host_complete_byte_inverse','publisher_complete_byte_inverse'):inverse(proof[key])
 worker=(BASE/'compare_remaining_Cr52_Fe56_finite9_SCAT.py').read_bytes();v1=BASE.parent/'remaining_Cr52_Fe56_source_v1';old=(v1/'compare_remaining_Cr52_Fe56_finite9_SCAT.py').read_bytes()
 numeric=proof['whole_v1_numerical_function_Source_and_AST'];names=('require','identity','current','metadata','pin','write','module','target_leaf','compare_leaf','replay_temperature','extract')
 need(numeric['whole_v1_function_AST_unchanged']==list(names)and all(definition(worker,n)==definition(old,n)for n in names),'eleven complete original v1 function Source/AST unchanged')
 restored=worker
 for a,b in ((b'len(roots)==59 and len(set(roots))==59',b'len(roots)==58 and len(set(roots))==58'),(b'complete inherited58 plus newoutput59 disjoint roots',b'complete inherited57 plus newoutput58 disjoint roots'),(b'same cumulative59 plan',b'same cumulative58 plan')):
  need(restored.count(a)==1,'one exact worker ledger/diagnostic adapter');restored=restored.replace(a,b,1)
 need(restored==old,'whole v2 worker restores entire v1 by three ledger/diagnostic-only replacements')
 oldhost=(v1/'run_guarded_remaining_Cr52_Fe56_finite9_SCAT.py').read_bytes();newhost=(BASE/'run_guarded_remaining_Cr52_Fe56_finite9_SCAT.py').read_bytes();restored_host=newhost
 for a,b in ((b"Root_required_exec_command_sandbox_permissions='require_escalated',",b''),(b'len(roots)==59 and len(set(roots))==59',b'len(roots)==58 and len(set(roots))==58'),(b'complete inherited58 exact prefix plus new output59',b'complete inherited57 exact prefix plus new output58')):
  need(restored_host.count(a)==1,'one exact host permission/ledger adapter');restored_host=restored_host.replace(a,b,1)
 need(restored_host==oldhost,'whole v1 host runtime and arithmetic restored; original PS guard remains unchanged')
 retained=plan['prior_failed_v1_evidence_pins'];retained_map={p['path']:p for p in retained}
 def previous(q):return read(retained_map[str(q)])
 prior_actual=previous(v1/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');terminal(prior_actual,'actual_terminal_return',1)
 need(prior_actual['actual_execution_permission_mode']=='use_default'and prior_actual['actual_execution_retried']is False,'original v1 default-sandbox actual1, no retry')
 postpin=retained_map[str(v1/'actual_postverify_20261015/corrected_metadata_roles_v2/REVIEW.json')];post=read(postpin);posttools=previous(v1/'actual_postverify_20261015/corrected_metadata_roles_v2/TRUE_TOOL_RETURNS.json');closed(posttools,'actual_review_return',postpin,'review_pin')
 need(post['status']=='PASS_FAILURE_FACTS_ONLY'and post['failure']is None and post['metadata_only']is True
  and post['actual_Root_original_integer_exit_code']==1 and post['actual_child_original_integer_exit_code']==-15
  and post['reported_full_comparison_complete']is False and post['producer_word_comparison_pass_claimed']is False
  and post['actual_original_child_report_present']is False and post['actual_aggregate_report_present']is False
  and post['actual_Source_peer_original_integer_exit_code']==0 and post['actual_Source_generation_original_integer_exit_code']==0
  and post['actual_Source_publication_original_integer_exit_code']==0 and post['original_post_checker_integer_exit_code']==1
  and post['original_first_LIGHT_integer_exit_code']==1 and post['corrected_LIGHT_original_integer_exit_code']==0,
  'v1 Source/pub0, actualRoot1/child-15, no comparison and first own failures retained')
 need(post['actual_Root_tools_pin']==retained_map[str(v1/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')]
  and post['original_owned_parent_child_groups_absent']is True,'exact v1 actual failure and owned-process-absence chain')
 for p in (post['actual_owned_process_absence_pin'],post['actual_process_absence_corroboration_pin'],post['actual_process_absence_true_tools_pin']):need(p in retained,'exact process absence provenance retained')
 absence=read(post['actual_process_absence_corroboration_pin']);absence_tools=read(post['actual_process_absence_true_tools_pin']);closed(absence_tools,'actual_readonly_process_absence_return',post['actual_process_absence_corroboration_pin'],'receipt_pin')
 need(absence['matched_process_rows']==[]and absence['process_census_returncode']==0 and absence['original_parent_pid']==55952
  and absence['original_child_pid']==55955 and absence_tools['execution_permission_mode']=='require_escalated','genuine readonly escalated process absence0; no new PS executed')
 for p in retained:need(p in selected,'complete literal v1 failure history in selected scope')
 need(plan['prior_failed_v1_actual_Root_integer_exit_code']==1 and plan['prior_failed_v1_own_child_returncode']==-15
  and plan['prior_failed_v1_original_word_equality_unknown']is True and plan['original_failed_v1_metadata_not_reclassified_as_success']is True
  and ready['Root_actual_exec_command_sandbox_permissions_required']==plan['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated',
  'unchanged original permission route contract; numerical pass remains unknown')
 text=worker.decode();host=(BASE/'run_guarded_remaining_Cr52_Fe56_finite9_SCAT.py').read_text()
 publisher=(BASE/'write_once_Root_remaining_Cr52_Fe56_finite9_SCAT_SF_HF_CLI.py').read_text();prep=(BASE/'prepare_remaining_Cr52_Fe56_finite9_SCAT_Source.py').read_text()
 need(text.index('now-self.started<600 and peak<512*2**20')<text.index('if now-self.last<0.25:return')
  and text.count('self.started=time.monotonic()')==1 and 'self.last=time.monotonic()'in text,'original clock and every-callback SELF/wall gate before disk-scan scheduling')
 for token in ('len(dilutions)==9 and len(set(dilutions))==9',"scalar.packed(value,True,(igres0,igres1),total[0])",'flux[0]!=0',"struct.pack('<f',sigma)","len(results)==1 and len(native)==7 and len(temperatures)==7 and len(targets)==63",'single_remaining_finite9_P0_producer_raw_words_replayed',"len(raw)<8*2**20"):
  need(token in text,'exact original scalar replay/REAL32 route/raw closure/child output bound')
 need(host.index("with claim.open('x')")<host.index("sf,psf=argument('source-freeze')")
  <host.index("source_module(plan['original_Common_Source_pin']"),'exclusive claim before Source checks/hash/import/business')
 for token in ('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)',"runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources)",'runner.execute(directory,label,cmd,600)','sys.getprofile()is None','peak<512*2**20 and time.monotonic()-start<1800',"len(runner.records)==2",'len(extractions)==2 and len(temperatures)==14 and len(native)==14 and len(targets)==126',"c['mismatching_raw_words']==0",'32*2**20','16*2**20','2*2**20',"out/'gendf-stage/stages.json'"):
  need(token in host,'original owning serial Runner/caps/complete closure/report hard bound')
 need(host.index('owned.append(pchild);child_pins.append(pchild);child_receipts.append(child_receipt);results.append(child);check_all()')<host.index('result=aggregate_reports(results,child_pins,pb,psf,aggregate_plan)'), 'both persisted actual closed0 reports before aggregate')
 for token in ("selected=ready['selected_Source_pins']+[pready,pg]","peer['source_only']is True", "tools['actual_review_return']", "generation['actual_Source_preparation_return']", "for role in('peer-review','peer-tools','generation','retirement')",'REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_PREPARATION_ONLY'):
  need(token in publisher,'exact publisher four PF triples and genuine peer/generation0 contract')
 need('runner.execute'not in publisher and "sum(p.stat().st_size for p in owning if p.exists())+len(raw)<16*2**20"in prep,'publication only and enforced total Source metadata reserve')
 need(len(ready['original_complete_ENV_Python_B_prefix'])==11,'original ENV/Python/-B prefix')
 retirement=read(plan['actual_precise_retirement_receipt_pin']);need(retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'
  and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'
  and retirement['failure']is None and retirement['actual_released_bytes']==405417320
  and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==4,'original literal4 receipt authority retained')
 for p in retirement['actual_released_pins']:need(not os.path.lexists(p['path']),'precise retired paths remain absent')
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 for p in inherited+science:current(p)
 for p in list(HASHED.values()):eof(p)
 need(not os.path.lexists(OUT),'output remains absent; no business eligibility inferred')
 report=dict(schema='INDEPENDENT_REMAINING_CR52_FE56_FINITE9_V2_FROZEN_SOURCE_REVIEW_V1',
  status='PASS_SOURCE_METADATA_SCOPE_WITH_SCIENTIFIC_DOCUMENT_CURRENT7_ONLY',failure=None,source_only=True,metadata_only=True,
  reviewer_source_freeze_pin=fp,reviewer_source_pin=freeze['reviewer_source_pin'],selected_Source_pins=selected,
  Source_ready_pin=freeze['ready_pin'],control_plan_pin=ready['control_plan_pin'],canonical_generation_tools_pin=freeze['canonical_generation_tools_pin'],
  original_Source_generation_integer_exit_code=0,canonical_v2_generation_wrapper_matches_genuine_terminal0=True,Source_preparation_reexecuted=False,
  fullEOF_Source_metadata_pins_verified_twice=list(HASHED.values()),selected_pin_count=len(selected),
  eleven_scientific_document_exception_pins_current7_twice=exceptions,scientific_document_exception_count=11,
  all_selected_new_fullEOF_claimed=False,inherited_metadata_current7_only_pins_verified_twice=inherited,
  original_scientific_input_current7_only_pins_verified_twice=science,scientific_document_bodies_opened_or_hashed=False,
  old_SCI_GENDF_SQL_pool_XSM_bodies_opened_hashed_or_decoded=False,candidate_or_helpers_imported=False,
  six_original_helpers_whole_bytes_unchanged=True,eleven_v1_functions_whole_bytes_and_AST_unchanged=True,whole_worker_inverse_restores_v1_by_ledger_count_and_labels_only=True,whole_host_inverse_restores_v1_by_ledger_count_and_permission_claim_only=True,numerical_arithmetic_and_loop_order_unchanged=True,
  original_support_REAL32_1e_minus6_and_tail_REAL32_1e_minus8_preserved=True,
  exact_REAL32_DILUTION_identity_mapping=True,new_GENDF_binary64_ENERGY_branch=True,
  exclusive_execution_claim_precedes_checks=True,original_guard_Runner_clock_profiler_caps_preserved=True,
  two_serial_children_each_closed0_report_before_next_and_aggregate=True,partial_evidence_cannot_close_complete_target=True,
  complete_joint_roots=roots,original_caps=CAPS,Source_generation_metadata_bound_bytes=16*2**20,new_output_hard_bound_bytes=96*2**20,
  expected_original_archives=2,expected_native_temperatures=14,expected_finite_nodes=126,expected_P0_leaf_records=378,
  prior_fuel_actual0_and_post0_preserved=True,prior_fullv5_actual_Root1_child1_preserved=True,current_temperature_actual0_and_post0_preserved=True,prior_finite_v1_Root1_child_minus15_preserved=True,prior_v1_no_report_no_aggregate_no_word_equality_pass_preserved=True,prior_v1_Source_generation_review_publication0_preserved=True,prior_v1_LIGHT_first_failure1_and_post_first_failure1_preserved=True,prior_v1_genuine_readonly_process_absence0_preserved=True,required_future_Root_exec_command_sandbox_permissions='require_escalated',future_process_permission_access_proved=False,
  planned_actual_output_root=str(OUT),planned_actual_output_root_absent=True,actual_future_execution_success_claimed=False,
  runtime_or_SELF_RSS_fit_proved=False,Source_preparation_executed_by_peer=False,Source_publication_executed_by_peer=False,
  sciencebody_imported_or_executed=False,native_engines_started_by_peer=0,native_executed=False,scientific_payload_read=False,
  SCI_payload_read=False,gzip_payload_read=False,original_ASCII_payload_read=False,matrix_math_recomputed_by_peer=False,
  auditor_elapsed_seconds=time.monotonic()-START,**FALSE)
 target=HERE/'REVIEW.json';need(not os.path.lexists(target),'fresh review output only')
 with target.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=own_pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

"""Focused independent v6 frozen Source audit; no candidate imports or science reads."""
import ast,hashlib,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parents[1];TOP=BASE.parent;V4=TOP/'v4';V5=TOP/'v5';HERE=Path(__file__).absolute().parent
R=Path('/Users/wen/spot');OUT=R/'validation/artifacts/axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
LARGE=(R/'validation/artifacts/axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',R/'validation/artifacts/axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,finite18_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
HASHED={};CHECKS=[];START=time.monotonic()
def require(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'} and type(p['path']) is str and type(p['sha256']) is str and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']) and type(p['size_bytes']) is int and type(p['identity']) is list and len(p['identity'])==7 and all(type(v) is int for v in p['identity']) and p['identity'][4]==p['size_bytes'],'strict fullPF schema')
 q=Path(p['path']);s=q.lstat();compiler=(q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15') and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2)
 require(q.is_absolute() and not any(v.is_symlink() for v in(q,*q.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and identity(s)==p['identity'],'literal current7 '+str(q))
def allowed(q,size):
 require(q.suffix in('.py','.f90','.json','.jsonl','.txt','.make','.in','.sha256','.log') or q.name.startswith(('file_data_gendf_','file_data_dendf_')),'Source/bounded metadata only')
 require(q.name not in('SCI1','SCI2') and not q.name.startswith('tape') and size<(64*2**20 if q in LARGE else 8*2**20),'exact two upstream large JSON metadata roles only; science body prohibited')
def pin(q):
 q=Path(q);s=q.lstat();allowed(q,s.st_size);p=dict(path=str(q),sha256='0'*64,size_bytes=s.st_size,identity=identity(s));current(p)
 with q.open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened Source/metadata7');p['sha256']=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==p['identity'],'whole EOF Source/metadata7')
 current(p);HASHED[str(q)]=p;return p
def verify(p):require(pin(p['path'])==p,'exact Source/metadata fullPF '+p['path'])
def read(p):
 verify(p);v=json.loads(Path(p['path']).read_bytes());current(p);return v
def get(q):
 p=pin(q);return read(p),p
def false(v):require(all(v[k] is False for k in FALSE if k in v),'all execution/qualification flags false')
def check(v):CHECKS.append(v)
def typed0(v,key,p,outkey):
 t=v[key];require(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code']==0 and type(t['exit_code']) is int and t['exit_code']==0 and t.get('session_id') is None and json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine original typed0 and exact stdout fullPF')
def source_defs(q):
 source=q.read_text();tree=ast.parse(source,filename=str(q));return source,{n.name:ast.get_source_segment(source,n).encode() for n in tree.body if isinstance(n,ast.FunctionDef)},tree
def class_source(source,tree,name):return ast.get_source_segment(source,next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==name)).encode()
def inverse(inv):
 verify(inv['original_full_pin']);verify(inv['candidate_full_pin']);a=Path(inv['original_full_pin']['path']).read_bytes();b=Path(inv['candidate_full_pin']['path']).read_bytes()
 edits=inv.get('edit_map',[inv])
 for e in sorted(edits,key=lambda v:v['candidate_begin_byte'],reverse=True):
  ob=bytes.fromhex(e['original_bytes_hex']);cb=bytes.fromhex(e['candidate_bytes_hex']);require(a[e['original_begin_byte']:e['original_end_byte']]==ob and b[e['candidate_begin_byte']:e['candidate_end_byte']]==cb,'inverse exact original/candidate intervals');b=b[:e['candidate_begin_byte']]+ob+b[e['candidate_end_byte']:]
 require(b==a and inv['complete_inverse_reconstructed_original'] is True,'whole original reconstructed exactly')
 if 'whole_original_reconstructed_sha256' in inv:require(hashlib.sha256(b).hexdigest()==inv['whole_original_reconstructed_sha256'],'whole original inverse SHA')
def audit():
 ready,pr=get(BASE/'SOURCE_REVIEW_READY.json');generation,pg=get(BASE/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
 require(pr['sha256']=='a8171fb2238273a86b4dca6b2d2c543715c986b5a0b5678722c5d8d35c5dc441' and pr['size_bytes']==401579 and pg['sha256']=='971eb2f704feac462eeb2528d20f86462a3380ff4a6f6bc8b1e3467f7c7d9d22' and pg['size_bytes']==1233,'exact real Root v6 READY and generation fullPFs')
 typed0(generation,'actual_Source_preparation_return',pr,'ready_pin');false(ready)
 require(ready['schema']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_REVIEW_READY_V1' and ready['source_only'] is True and ready['actual_business_started'] is False and ready['Root_final_publication_executed'] is False and ready['scientific_payload_read'] is False and ready['original_caps']==CAPS and len(ready['selected_Source_pins'])==445 and ready['selected_Source_pins']==ready['dependencies'],'exact frozen445 Source-only dependencies')
 for p in ready['selected_Source_pins']:verify(p)
 plan=read(ready['control_plan_pin']);false(plan);require(plan['original_caps']==CAPS and plan['schema']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_ONLY_PLAN_V1','exact Source plan/caps')
 author=read(plan['author_Pre_Root_generation_Source_freeze_pin']);false(author)
 require(author['Source_files_frozen_before_Root_generation'] is True and author['Source_preparation_executed_by_author'] is False and author['Source_publication_executed_by_author'] is False,'author pre-generation freeze, no business/publication')
 for p in author['whole_Source_file_pins']:verify(p)
 derive=read(author['source_derivation_pin']);false(derive)
 for p in ready['complete_source_file_pins']:
  if Path(p['path']).suffix=='.py':ast.parse(Path(p['path']).read_text(),filename=p['path'])
 require(not os.path.lexists(OUT) and not any(os.path.lexists(BASE/n) for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')),'fresh v2 output and no premature Source publication')
 check('All445 selected bounded Source/metadata fullPFs, exact Root v6 generation0/READY, frozen Source flags and ASTs')
 failed=read(plan['selected_prior51_failed_plan_pin']);v5plan=read(plan['retained_v5_source_plan_pin'])
 roots=plan['complete_joint_roots'];require(len(failed['complete_joint_roots'])==51 and roots==failed['complete_joint_roots']+[str(OUT)]==v5plan['complete_joint_roots'] and len(roots)==len(set(roots))==52 and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'exact prior51 retained plus one fresh output52; same wholeTOP')
 require(plan['inputs']==failed['inputs']==v5plan['inputs'] and plan['actual_current_SCI1_pin']==failed['actual_current_SCI1_pin'] and plan['expected_serial_children']==8 and plan['expected_per_child_archives']==2 and plan['expected_per_child_native_temperature_records']==8 and plan['expected_per_child_finite_nodes']==144 and plan['expected_per_child_leaf_records']==432 and plan['expected_archives']==16 and plan['expected_temperature_records']==64 and plan['expected_archive_temperature_records']==128 and plan['expected_finite_dilution_nodes']==1152 and plan['expected_leaf_records']==3456,'same original16 archives and exact per-child/global scope')
 science=[plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[r['current_original_input_full_pin'] for r in plan['inputs']]
 for p in science:current(p)
 oldtools=read(plan['prior_finite_failed_Root_true_tools_pin']);oldh=read(plan['prior_finite_failed_Root_report_pin']);facts=read(plan['prior_finite_failure_facts_review_pin']);factst=read(plan['prior_finite_failure_facts_true_tools_pin'])
 require(oldtools['observed_closed'] is True and type(oldtools['original_integer_exit_code']) is int and oldtools['original_integer_exit_code']==1 and type(oldtools['actual_terminal_return']['exit_code']) is int and oldtools['actual_terminal_return']['exit_code']==1 and oldtools['actual_terminal_return'].get('session_id') is None and oldh['status']=='FAILED_EIGHT_FUEL_FINITE18_SCAT_NO_RETRY' and oldh['failure']=="RuntimeError('own-child wall cap reached')" and oldh['actual_child_receipt'] is None and oldh['actual_evidence'] is None,'original v4 failed1/equality unknown preserved')
 require(facts['status']=='PASS_FACTS_ONLY_ACTUAL_FAILED_FINITE18_WALL_CAP_NO_COMPLETION_EVIDENCE' and facts['failure'] is None and facts['original_Root_integer_exit_code']==1 and facts['actual_original_finite_P0_equality_unknown'] is True and facts['actual_failed_pipeline_reclassified_as_success'] is False and facts['finite_P0_raw_words_equal_qualified'] is False and plan['prior_failed_finite_equality_inferred'] is False,'sole v4 facts-only assessment is not science success')
 typed0(factst,'actual_review_return',plan['prior_finite_failure_facts_review_pin'],'review_pin')
 for p in facts['all_actual_six_output_full_pins']:verify(p)
 for p in plan['preserved_finite_v1_v2_v3_v4_Source_pins']+plan['retained_frozen_v5_source_metadata_pins']:verify(p)
 v5tools=read(plan['retained_v5_source_generation_true_tools_pin']);typed0(v5tools,'actual_Source_preparation_return',plan['retained_v5_source_ready_pin'],'ready_pin');require(plan['v5_business_failure_invented'] is False,'real v5 Source generation0 preserved; no invented business attempt/failure')
 check('Exact52 cumulative roots, original16 inputs, v1-v5 provenance and genuine v4failed1/facts-only0 plus v5Source-generation0 preserved')
 w4,d4,t4=source_defs(V4/'compare_eight_fuel_finite18_SCAT.py');w,d,t=source_defs(BASE/'compare_eight_fuel_finite18_SCAT.py')
 names=[n for n in d4 if n!='main'];require(len(names)==11 and all(d[n]==d4[n] for n in names),'all11 worker function definitions whole unchanged from v4')
 require((V5/'compare_eight_fuel_finite18_SCAT.py').read_bytes()==(BASE/'compare_eight_fuel_finite18_SCAT.py').read_bytes() and (V5/'write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py').read_bytes()==(BASE/'write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py').read_bytes(),'v5-v6 worker and oncewriter whole Source equality')
 old_budget=class_source(w4,t4,'Budget');new_budget=class_source(w,t,'Budget')
 expected=old_budget.replace(b'len(roots)==51 and len(set(roots))==51',b'len(roots)==52 and len(set(roots))==52').replace(b'complete prior49 plus Source/output51 disjoint roots',b'complete prior51 plus newoutput52 disjoint roots').replace(b'  self.last=now;total=0\n',b'  total=0\n')+b'\n  self.last=time.monotonic()'
 require(expected==new_budget,'Budget only root52 count/text and last-after-successful-fullscan edit')
 require(w.index('now-self.started<600 and peak<512*2**20')<w.index('if now-self.last<0.25:return') and w.count('budget.last=0;budget.check()')==w4.count('budget.last=0;budget.check()')==2 and 'budget=Budget' in w and 'budget.check();plan=metadata' in w,'SELF/wall every callback and forced startup/pre/post-output scans unchanged')
 host=(BASE/'run_guarded_eight_fuel_finite18_SCAT.py').read_text();oldhost=(V4/'run_guarded_eight_fuel_finite18_SCAT.py').read_text();host5=(V5/'run_guarded_eight_fuel_finite18_SCAT.py').read_text()
 a=' class Resources:';b=' resources=Resources();';require(host[host.index(a):host.index(b)]==oldhost[oldhost.index(a):oldhost.index(b)],'whole original Root Resources class unchanged')
 old=derive['host_only_change_old_statement'];new=derive['host_only_change_new_statement'];require(host5.count(old)==1 and host5.replace(old,new,1)==host,'v6 host whole reconstructed by exact stage-ledger field correction only')
 for inv in derive['complete_v5_to_v6_source_inverses']:inverse(inv)
 proof=read(plan['original_whole_math_inverse_proof_pin']);false(proof)
 for row in proof['whole_original_source_copies']:
  a=row['original_full_pin'];b=row['whole_unchanged_copy_full_pin'];verify(a);verify(b);require(Path(a['path']).read_bytes()==Path(b['path']).read_bytes()==(V4/Path(b['path']).name).read_bytes(),'all6 original helper/Fortran Sources whole unchanged')
 for k in('host_complete_byte_inverse','worker_complete_byte_inverse','publisher_complete_byte_inverse'):inverse(proof[k])
 require(proof['original_finite_support_and_suffix_tail_called_unchanged'] is True and proof['low_lane_own_infinite_and_elasticflux_reference_preserved'] is True and proof['original_REAL32_DILUTION_word_selects_original_SUBMAT'] is True,'original finite support/suffix and exact own-lane REAL32 routes retained')
 check('Exact authorized scan timestamp edit only, SELF/wall checks every callback and forced scans; whole Root Resources,11 worker functions,6 helpers and complete Source inverses unchanged')
 nucs=['Am241','Pu238','Pu239','Pu240','Pu241','Pu242','U235','U238'];require(plan['execution_nuclides']==nucs,'exact eight unique original nuclides')
 for token in("ap.add_argument('--nuclide',required=True,choices=('Am241','Pu238','Pu239','Pu240','Pu241','Pu242','U235','U238'))", "selected=[row for row in plan['inputs']if row['nuclide']==a.nuclide]", "require(len(selected)==2 and [row['lane']for row in selected]==['low','high']", "for row in selected:budget.check();results.append(extract(row,scalar,streamer,budget.check,sci,energy))", "len(results)==2 and len(native)==8 and len(temperatures)==16 and len(targets)==144 and len(set(stamps))==144", "report=out/('ACTUAL_'+a.nuclide+'_FINITE18_SCAT_EVIDENCE.json')", "require(exact,'actual original finite18 P0 mismatch retained; no retry')"):
  require(token in w,'exact per-nuclide selector/persistence/coverage/exit0 gate')
 for token in("runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources)", "full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)", 'for nuclide in names:', 'runner.execute(directory,label,cmd,600)', "record['status']=='PASS'and len(runner.records)==len(results)+1", "child['compared_finite_dilution_nodes']==144 and child['compared_original_leaf_records']==432", "results.append(child);check_all()", "require(len(runner.records)==8 and len({r['label']for r in runner.records})==8 and all(r['status']=='PASS'for r in runner.records)", "len(extractions)==16 and len(temperatures)==128 and len(native)==64 and len(targets)==1152 and len(stamps)==len(set(stamps))", "all(c['exact_raw_words_equal']is True and c['mismatching_raw_words']==0 and c['original_raw_sha256']==c['replayed_raw_sha256']", "original_stage_ledger_pin=c.pin(out/'gendf-stage/stages.json')"):
  require(token in host,'original serial owning control, every part persisted0 before next, complete8 aggregate and exact original ledger path')
 require(host.index('owned.append(pchild);child_pins.append(pchild);child_receipts.append(child_receipt);results.append(child);check_all()')<host.index('aggregate_reports(results,child_pins,pb,psf,aggregate_plan)'), 'aggregate only after all persisted child reports')
 production=R/'validation/axial_material/root64_epoch_recovery_20261011/streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/runtime/production_runner.py';pProduction=pin(production);psource=production.read_text()
 for token in ('self.stages_path = work / case / "stages.json"','remaining = self.deadline - time.monotonic()','limit = min(float(cap), remaining)','total wall-time budget exhausted; no next stage started','self.deadline - time.monotonic()'):
  require(token in psource,'actual original stage ledger and remaining whole-time bound')
 require('good=first.error is None and verified' in host and "'FAILED_EIGHT_FUEL_FINITE18_SCAT_NO_RETRY'" in host,'partial reports cannot qualify full target closure')
 publisher=(BASE/'write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py').read_text();require("len(plan['complete_joint_roots'])==52" in publisher and "selected=ready['selected_Source_pins']+[pready,pg]" in publisher and "gd['ready_pin']==pready" in publisher and 'runner.execute' not in publisher,'once Source publication binds exact peer/generation/new52; never business')
 check('Exact per-nuclide2archive/8T/144node/432leaf stages; persisted closed0 report before next; all8/1152/3456 aggregate gates; unchanged OwnRSS/min600-remaining1800; ledger field matches real SerialExecutor; no false partial closure')
 for p in ready['selected_Source_pins']+[pr,pg]:current(p)
 for p in science:current(p)
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);require(peak<512*2**20 and time.monotonic()-START<600,'bounded own metadata audit512/600')
 return dict(selected_Source_pins=ready['selected_Source_pins']+[pr,pg],Source_ready_pin=pr,Root_generation_true_tools_pin=pg,
  control_plan_pin=ready['control_plan_pin'],author_source_freeze_pin=plan['author_Pre_Root_generation_Source_freeze_pin'],
  hash_checked_Source_metadata_pins=list(HASHED.values()),original_science_files_dual_current7_only_pins=science,
  complete_joint_roots=roots,original_caps=CAPS,unchanged_v4_worker_function_names=names,
  original_six_helpers_whole_unchanged=True,only_authorized_Budget_scan_completion_timestamp_changed=True,
  original_SELF_wall_checks_every_callback_preserved=True,forced_budget_scans_preserved=True,
  original_Root_Resources_whole_unchanged=True,original_serial_executor_Source_pin=pProduction,
  original_stage_ledger_field_exact_path='gendf-stage/stages.json',eight_unique_serial_parts_each_persisted_before_next=True,
  partial_comparison_reports_cannot_qualify_complete8=True,per_child_archives=2,per_child_native_temperature_records=8,
  per_child_finite_nodes=144,per_child_leaf_records=432,expected_archives=16,expected_native_temperature_records=64,
  expected_archive_temperature_records=128,expected_finite_nodes=1152,expected_leaf_records=3456,
  prior_actual_Root_failed_integer_exit_code=1,prior_actual_finite_equality_unknown=True,
  prior_failure_facts_review_pin=plan['prior_finite_failure_facts_review_pin'],retained_v5_source_generation_true_tools_pin=plan['retained_v5_source_generation_true_tools_pin'],
  candidate_business_executed=False,performance_benchmark_executed=False,actual_failed_run_progress_inferred=False,
  future_execution_success_claimed=False,auditor_SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-START)
def main():
 target=HERE/'REVIEW.json';require(not os.path.lexists(target),'once Source review; preserve failures');error=None
 report=dict(schema='INDEPENDENT_EIGHT_FUEL_FINITE18_V6_FROZEN_SOURCE_ONLY_REVIEW_V1',status='FAIL_FROZEN_V6_SOURCE_REVIEW',failure=None,
  source_only=True,scientific_payload_read=False,SCI_payload_read=False,gzip_payload_read=False,original_ASCII_payload_read=False,
  candidate_imported=False,sciencebody_imported_or_executed=False,Source_preparation_executed_by_peer=False,
  Source_publication_executed_by_peer=False,matrix_math_recomputed_by_peer=False,native_engines_started_by_peer=0,
  scope='Frozen v6 Source eligibility only: eight serial original fuel nuclides, exact unchanged numerical replay and resource caps. No actual finite replay, measured performance, material/SPH/physics/reference/AAA/ABA qualification.',**FALSE)
 try:report.update(audit());report['status']='PASS_INDEPENDENT_V6_EIGHT_SERIAL_FUEL_FINITE18_P0_FROZEN_SOURCE_ONLY'
 except BaseException as e:error=e;report['failure']=repr(e)
 report['checks_completed']=CHECKS;report['audit_source_pin']=pin(Path(__file__).absolute())
 with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),**FALSE)),flush=True)
 if error is not None:raise error
if __name__=='__main__':main()

"""Frozen Source eligibility review only; never import a candidate or science helper."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

HERE=Path(__file__).absolute().parent; BASE=HERE.parent; CAPTURE=BASE.parent/'current_extra_reaction_source_v2'
R=Path('/Users/wen/spot'); ART=R/'validation/artifacts'
OUT=ART/'axial-material-current-extra21-captured-operand-independent-replay-20261015-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,
 history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,
 free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
EXTRACT=ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence'
EXCEPTIONS={str(EXTRACT/(n+'_actual_saved_MT5_P0.json')) for n in
 ('U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55')}
EXCEPTIONS.add(str(ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json'))
LARGE={str(ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1'/n)
 for n in ('Root_actual_all34_original_ASCII_infinite_SCAT_summary.json','inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')}
LARGE.add(str(ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2/Root_actual_eight_fuel_finite18_SCAT_summary.json'))
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,
 physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,
 physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,
 MT5_partition_qualified=False,fission_producer_replayed=False,reaction_exclusive_partition_qualified=False,selected_capture_complete=False,
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

def digest_scope(pins):return hashlib.sha256((json.dumps(pins,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()).hexdigest()
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--reviewer-freeze-pin',required=True);a=ap.parse_args();fp=strict(a.reviewer_freeze_pin);freeze=read(fp);eof(freeze['reviewer_source_pin'])
 need(freeze['schema']=='INDEPENDENT_EXTRA21_OPERAND_REPLAY_SOURCE_REVIEWER_FREEZE_V1'and freeze['reviewer_AST_passed_before_freeze']is True and freeze['reviewer_source_pin']['path']==str(Path(__file__).absolute()),'own frozen stdlib reviewer Source')
 ready=read(freeze['ready_pin']);gen=read(freeze['canonical_generation_tools_pin']);closed(gen,'actual_Source_preparation_return',freeze['ready_pin'],'ready_pin')
 stdout=strict(gen['actual_Source_preparation_return']['output'].strip().splitlines()[-1]);need(stdout['status']=='EXTRA21_CAPTURED_OPERAND_INDEPENDENT_REPLAY_SOURCE_PREPARATION_ONLY'and all(stdout[k]is False for k in('business_executed','numerical_executed','compiler_executed','files_deleted')),'genuine Sourcegen0 only')
 need(ready['schema']=='EXTRA21_CAPTURED_OPERAND_INDEPENDENT_REPLAY_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['actual_business_started']is False and ready['Root_final_publication_executed']is False and ready['scientific_payload_read']is False and ready['selected_Source_pins']==ready['dependencies']and ready['original_caps']==CAPS,'exact same-round Source-only scope')
 selected=unique(ready['selected_Source_pins']+[freeze['ready_pin'],freeze['canonical_generation_tools_pin']]);old_science=unique(ready['old_scientific_current7_only_pins']);new_npz=unique(ready['new_captured_operand_current7_only_pins']);old_paths={p['path']for p in old_science};new_paths={p['path']for p in new_npz};EXCEPTIONS.update(old_paths|new_paths)
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 for p in old_science+new_npz:current(p)
 plan=read(ready['control_plan_pin']);proof=read(plan['original_independent_replay_Source_proof_pin']);author=read(plan['author_Pre_Root_generation_Source_freeze_pin'])
 need(plan['schema']=='EXTRA21_CAPTURED_OPERAND_INDEPENDENT_REPLAY_SOURCE_ONLY_PLAN_V1'and plan['original_caps']==CAPS and author['schema']=='AUTHOR_EXTRA21_CAPTURED_OPERAND_INDEPENDENT_REPLAY_PRE_ROOT_GENERATION_SOURCE_FREEZE_V1'and author['Source_files_frozen_before_Root_generation']is True and all(author[k]is False for k in('Source_preparation_executed_by_author','Source_publication_executed_by_author','business_executed_by_author','new_NPZ_arrays_opened_or_decoded_by_author','old_scientific_inputs_opened_hashed_imported_or_decoded_by_author')),'Source frozen before sole Root generation/numerical decoding')
 for value in(ready,plan,proof,author):need(all(value[k]is False for k in FALSE if k in value),'all physical/qualification flags false')
 need(all(value[k]is False for value in(ready,plan,proof,author)for k in('original_evaluation_neutron_yield_branch_captured','MF6_GENDF_label_proves_original_processing_branch')),'original processing branch remains unknown')
 for p in author['whole_Source_file_pins']:
  eof(p)
  if Path(p['path']).suffix=='.py':ast.parse(Path(p['path']).read_bytes(),filename=p['path'])
 need(len(ready['complete_source_file_pins'])==9 and len(author['whole_Source_file_pins'])==9,'eight selected Source/docs plus proof, author preserves draft failure too')
 absent=('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_EXECUTION_CLAIM_RECEIPT.json')
 need(not os.path.lexists(OUT)and not any(os.path.lexists(BASE/n)for n in absent),'no publication/current business/output')
 prior=read(plan['inherited_complete60_plan_pin']);roots=plan['complete_joint_roots'];need(roots==prior['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))==61 and len(prior['complete_joint_roots'])==60 and str(BASE.parent)in roots[:-1]and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'complete60 unchanged prefix plus only thin OUT61')
 inherited=unique(ready['inherited_metadata_current7_pins']);need(inherited==plan['inherited_metadata_current7_pins']==prior['explicit_cumulative_metadata_file_pins'],'original inherited metadata scope unchanged')
 for p in inherited:current(p)
 need(plan['inputs']==[]and {p['path']:p for p in new_npz}=={p['path']:p for p in plan['new_captured_operand_file_pins']}and len(new_npz)==131 and len(new_paths)==131 and len(old_science)==31,'old science inaccessible; exactly131 new operand roles and retained31 old roles')
 for p in new_npz:need(p['identity'][3]==1 and p['size_bytes']<2*2**20 and Path(p['path']).suffix=='.npz','ordinary captured NPZ current7 only')
 need(plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['bounded_new_output_reservation_bytes']==16*2**20 and plan['child_report_hard_bound_bytes']==8*2**20 and plan['host_summary_hard_bound_bytes']==6*2**20 and plan['binding_runtime_log_watchdog_hard_combined_bound_bytes']==2*2**20 and plan['Source_only_cumulative_bytes_before_reservations']+32*2**20<2*2**30,'unchanged2GiB and Source16/thinOUT16 decomposition')
 own=[BASE/n for n in('ORIGINAL_FVECT_FMATR_INDEPENDENT_REPLAY_SOURCE_PROOF.json','PLAN.json','SOURCE_REVIEW_READY.json')];need(all(q.stat().st_size<8*2**20 for q in own)and sum(q.stat().st_size for q in own)<16*2**20,'actual generated individual8/combined16MiB bounds')
 nz=plan['actual_original_MF1_nz_by_nuclide'];need(len(nz)==17 and all(type(x)is int and x==1 for x in nz.values())and nz==author['actual_original_MF1_nz_by_nuclide']==proof['original_MF1_global_nz_by_nuclide']=={s['input']['nuclide']:s['input']['original_expected_nz']for s in prior['selected_inputs']},'exact original MF1 grid NZ17all1 from completed input metadata')
 root=read(plan['prior_capture_actual0_true_tools_pin']);post=read(plan['prior_capture_post0_pin']);posttools=read(plan['prior_capture_post0_true_tools_pin']);closed(root,'actual_terminal_return',plan['prior_capture_actual0_Host_report_pin'],'report_pin');closed(posttools,'actual_review_return',plan['prior_capture_post0_pin'],'review_pin')
 need(root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False and post['schema']=='INDEPENDENT_EXTRA21_ACTUAL_RECORDED_CAPTURE_METADATA_BLIND_OUTPUT_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_EXTRA21_RECORDED_CAPTURE_METADATA_AND_BLIND_OUTPUT_SHA_ONLY'and post['failure']is None and post['actual_Root_original_integer_exit_code']==0 and post['actual_Root_tools_pin']==plan['prior_capture_actual0_true_tools_pin']and post['actual_Host_report_pin']==plan['prior_capture_actual0_Host_report_pin']and post['actual_capture_report_pin']==plan['actual_captured_operands_report_pin'],'true prior capture0/post0 provenance only')
 for k in('new_NPZ_archive_members_or_numeric_arrays_opened_or_decoded','matrix_or_flux_arithmetic_recomputed','neutron_multiplicity_or_production_diagnostics_recomputed'):need(post[k]is False,'prior post blind bytes only, not a numerical qualification')
 need(post['new_NPZ_files_blind_EOF_SHA_verified_twice']is True and post['reported_channel_temperature_records']==131 and post['reported_MF3_MF6_sections']==262 and post['reported_MF3_LIST_records']==768 and post['reported_MF6_LIST_records']==576 and {p['path']:p for p in post['actual_new_operand_full_pins']}=={p['path']:p for p in new_npz},'complete prior131 recorded-role PF scope')
 for item in proof['whole_original_source_copies']:
  p=item['original_Source_pin'];q=item['whole_unchanged_copy_full_pin'];eof(p);eof(q);need(Path(p['path']).read_bytes()==Path(q['path']).read_bytes(),'whole authoritative primary/guard/publisher copy')
 need(len(proof['whole_original_source_copies'])==3,'exact three whole originals')
 worker=(BASE/'reconstruct_new_captured_extra21_operands.py').read_text();host=(BASE/'run_guarded_new_captured_extra21_independent_replay.py').read_text();publisher=(BASE/'write_once_Root_extra21_captured_operand_replay_SF_HF_CLI.py').read_text();prep=(BASE/'prepare_extra21_captured_operand_replay_Source.py').read_text();tree=ast.parse(worker);globals={n.targets[0].id:ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in('MEMBERS','CONTEXTS')}
 need(len(globals['MEMBERS'])==len(set(globals['MEMBERS']))==28 and len(globals['CONTEXTS'])==8 and len(set(globals['MEMBERS'])-set(globals['CONTEXTS']))==20,'exact28 members/eight contexts/20 derived arrays')
 need('scalar.matrix('not in worker and 'importlib'not in worker and 'capture_extra21_original_ascii'not in worker,'independent direct implementation without original numerical helper/capturer import')
 for token in("g=370-ig;flux3[g]=data[0];event[g]=data[1]","1<=ig<=370 and len(data)==2","0<=ig<=370","spectrum[lower-1+k]=data[k]","outgoing=370-(lower+k-1)","float(matrix[g,outgoing])+float(data[k])","float(spectrum[369-outgoing])*float(data[k])","float(matrix[g,outgoing])+product","for outgoing in range(370):total+=float(matrix[g,outgoing])","if common[g]:delta[g]","if ratio_mask[g]:ratio[g]","if recon_ratio_mask[g]:recon_ratio[g]","struct.pack('<4i',ig,lower,ng2,npl)","incident_mask[ig-1]=1","spectrum_present=True","dimension_digest.hexdigest()==canonical['LIST_dimension_sequence_sha256']","bytes(incident_mask).hex()==canonical['incident_present_mask_hex']","spectrum_present==canonical['spectrum_LIST_present']","numeric_sha==proof['selected_P0_LIST_numeric_f8_sha256']","if original_nl==1:","sum(r.file_size for r in records)<2*2**20","allow_pickle=False","actual.tobytes(order='C')","struct.pack('<d',value)==struct.pack('<d',expected)","original_ASCII_or_full_NL2_payload_hash_independently_replayed=False","plan['actual_original_MF1_nz_by_nuclide'][row['nuclide']]"):
  need(token in worker,'direct original index/order/semantic/raw-provenance/byte comparison Source')
 need(worker.index('now-self.started<600 and peak<512*2**20')<worker.index('if now-self.last<0.25:return')and worker.count('self.started=time.monotonic()')==1 and 'self.last=time.monotonic()'in worker,'every callback original SELF/wall before disk scan schedule')
 need(host.index("claim.open('x')")<host.index("sf,psf=argument('source-freeze')")<host.index("source_module(plan['original_Common_Source_pin']"),'original Root exclusive claim before checks/hash/import')
 for token in('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)',"runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources)","runner.execute(stage,'extra21_new_captured_operands_independent_f8_replay',cmd,600)","len(runner.records)==1",'sys.getprofile()is None','peak<512*2**20 and time.monotonic()-start<1800',"own_bytes<plan['bounded_new_output_reservation_bytes']","aux_bytes<plan['binding_runtime_log_watchdog_hard_combined_bound_bytes']","result['compared_derived_arrays']==2620","result['different_values']==0 and result['different_bits']==0"):
  need(token in host,'original one owning child/control resources and complete zero-bit report closure')
 need('current_original_input_full_pin'not in host and "plan['new_captured_operand_file_pins']"in host,'host never selects old scientific primary files')
 for token in("for role in('peer-review','peer-tools','generation','retirement')","tools['actual_review_return']","generation['actual_Source_preparation_return']","selected=ready['selected_Source_pins']+[pready,pg]","exec_command_sandbox_permissions='require_escalated'"):
  need(token in publisher,'exact publisher PF/genuine0/permission contract')
 need('runner.execute'not in publisher and "sum(p.stat().st_size for p in own if p.exists())+len(raw)<16*2**20"in prep and 'len(raw)<8*2**20'in prep,'once publication only and original Source output limits')
 need(ready['Root_actual_exec_command_sandbox_permissions_required']==plan['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and len(ready['original_complete_ENV_Python_B_prefix'])==11,'unchanged process guard permission and original11 prefix/24argv construction')
 retirement=read(plan['actual_precise_retirement_receipt_pin']);need(retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==4,'original completed literal4 retirement retained')
 for p in retirement['actual_released_pins']:need(not os.path.lexists(p['path']),'original retired paths still absent')
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 for p in inherited+old_science+new_npz:current(p)
 for p in list(HASHED.values()):eof(p)
 need(not os.path.lexists(OUT),'output remains unexecuted')
 report=dict(schema='INDEPENDENT_EXTRA21_CAPTURED_OPERAND_REPLAY_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_METADATA_SCOPE_WITH_SCIENTIFIC_PAYLOAD_CURRENT7_ONLY',failure=None,source_only=True,metadata_only=True,reviewer_source_freeze_pin=fp,reviewer_source_pin=freeze['reviewer_source_pin'],Source_ready_pin=freeze['ready_pin'],canonical_generation_tools_pin=freeze['canonical_generation_tools_pin'],control_plan_pin=ready['control_plan_pin'],selected_Source_pins=selected,selected_pin_count=len(selected),all_selected_fullEOF_claimed=False,fullEOF_Source_metadata_scope_count=len(HASHED),fullEOF_Source_metadata_scope_ordered_fullPF_sha256=digest_scope(list(HASHED.values())),fullEOF_Source_metadata_scope_reference='Selected scope minus declared old science roles plus author/proof/own reviewer Source pins; whole EOF+SHA/current7 twice.',selected_current7_only_scientific_document_count=sum(p['path']in old_paths for p in selected),old_scientific_current7_scope_count=len(old_science),old_scientific_current7_scope_ordered_fullPF_sha256=digest_scope(old_science),old_scientific_scope_reference=dict(ready_pin=freeze['ready_pin'],field='old_scientific_current7_only_pins'),new_NPZ_current7_scope_count=len(new_npz),new_NPZ_current7_scope_ordered_fullPF_sha256=digest_scope(new_npz),new_NPZ_scope_reference=dict(ready_pin=freeze['ready_pin'],field='new_captured_operand_current7_only_pins'),inherited_metadata_current7_scope_count=len(inherited),inherited_metadata_current7_scope_ordered_fullPF_sha256=digest_scope(inherited),inherited_scope_reference=dict(plan_pin=ready['control_plan_pin'],field='inherited_metadata_current7_pins'),current7_scopes_verified_twice=True,old_science_payload_or_new_NPZ_bodies_opened_hashed_decoded=False,new_NPZ_archive_members_or_arrays_opened=False,candidate_or_scientific_helpers_imported=False,original_Source_generation_integer_exit_code=0,Source_preparation_executed_by_peer=False,Source_preparation_reexecuted=False,Source_publication_executed_by_peer=False,prior_capture0_and_post0_preserved=True,prior_post_remains_blind_SHA_metadata_only=True,Source_independent_reconstruction_only_from_new_raw_P0_contexts=True,original_FVECT_FMATR_index_order_zero_initialization_preserved=True,canonical_raw_LIST_dimension_order_SHA_masks_spectrum_checks_preserved=True,retained_P0_and_NL1_full_numeric_scope_honest=True,full_NL2_and_original_ASCII_replay_claimed=False,twenty_derived_arrays_strict_zero_bits_and_exact_f8_stats_required=True,signed_ratios_and_observed_absence_masks_distinct=True,actual_MF1_grid_nz17all1_bound=True,zip28_members_combined2MiB_bound=True,three_original_Source_copies_whole_unchanged=True,original_guard_OwnRSS_PS_MRO_clock_profiler_caps_preserved=True,expected_new_NPZ_files=131,expected_derived_arrays_per_file=20,expected_total_derived_comparisons=2620,expected_P0_LIST_records=1344,complete_joint_roots=roots,original_caps=CAPS,own_Source_generated_metadata_bound_bytes=16*2**20,new_output_hard_bound_bytes=16*2**20,new_output_component_bounds_bytes=dict(child_report=8*2**20,host_summary=6*2**20,auxiliary=2*2**20),planned_actual_output_root=str(OUT),planned_actual_output_root_absent=True,required_future_Root_exec_command_sandbox_permissions='require_escalated',actual_future_execution_success_claimed=False,runtime_or_SELF_RSS_fit_proved=False,scientific_payload_read=False,matrix_math_recomputed_by_peer=False,native_engines_started_by_peer=0,native_executed=False,auditor_elapsed_seconds=time.monotonic()-START,original_evaluation_neutron_yield_branch_captured=False,MF6_GENDF_label_proves_original_processing_branch=False,**FALSE)
 target=HERE/'REVIEW.json';need(not os.path.lexists(target),'fresh once review output')
 with target.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 limits();print(json.dumps(dict(status=report['status'],review_pin=own_pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

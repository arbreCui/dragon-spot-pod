"""Root once preparation: Source and evidence metadata, scientific current7 only."""
import ast, hashlib, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts'
BASE=Path(__file__).absolute().parent;FUEL=BASE.parent/'v6';ALL34=REC/'current_all34_original_ASCII_infinite_SCAT_producer_source_v1_20261015/v2';FULL=REC/'current_full370_real_operator_control_source_v1_20261015/v5'
TEMP=REC/'current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5'
OUT=ART/'axial-material-current-remaining-Cr52-Fe56-finite9-SCAT-producer-20261015-v1'
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,finite9_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,P1_replayed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
SOURCE_NAMES=('compare_remaining_Cr52_Fe56_finite9_SCAT.py','run_guarded_remaining_Cr52_Fe56_finite9_SCAT.py','write_once_Root_remaining_Cr52_Fe56_finite9_SCAT_SF_HF_CLI.py','prepare_remaining_Cr52_Fe56_finite9_SCAT_Source.py','original_check_mt51_repair.py','original_bounded_SCI_helpers.py','original_four_ascii_stream_helpers.py','original_dragr.f90','original_guard_host.py','original_once_publisher.py')
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size==p['size_bytes']and identity(s)==p['identity'],'ordinary exact current7; no scientific body read')
def pin(q):
 q=Path(q);s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(q):
 p=pin(q);limit=64*2**20 if Path(q)==ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2/Root_actual_eight_fuel_finite18_SCAT_summary.json'else 8*2**20;require(p['size_bytes']<limit,'literal bounded evidence metadata');v=json.loads(Path(q).read_bytes());require(pin(q)==p,'same whole metadata');return v,p
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'new Source-preparation metadata below8MiB each')
 owning=(BASE/'ORIGINAL_MATH_AND_MINIMAL_SOURCE_INVERSE.json',BASE/'PLAN.json',BASE/'SOURCE_REVIEW_READY.json');require(Path(q)in owning and sum(p.stat().st_size for p in owning if p.exists())+len(raw)<16*2**20,'all three owning Source-generation metadata files below16MiB reserved bound')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def unique(rows):
 table={}
 for p in rows:
  if p['path']in table:require(table[p['path']]==p,'same path consistent fullPF')
  table[p['path']]=p
 return list(table.values())
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def genuine(v,key,code):
 t=v[key];require(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'original genuine typed terminal integer retained')
 return json.loads(t['output'].strip().splitlines()[-1])if code==0 else None
def post_pair(directory,report_pin,tools_pin,actual_code,status):
 review,pr=read(directory/'REVIEW.json');tools,pt=read(directory/'TRUE_TOOL_RETURNS.json');stdout=genuine(tools,'actual_review_return',0)
 require(stdout['review_pin']==pr and review['status']==status and review['failure']is None and contains(review,report_pin)and contains(review,tools_pin),'sole independent actual post exact genuine evidence linkage')
 if status=='PASS_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_ONLY_POSTVERIFICATION':
  require(review['schema']=='INDEPENDENT_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_POSTVERIFY_V1'and review['actual_Root_integer_exit_code']==actual_code and review['old_SQL_pool_XSM_GENDF_SCI_bodies_opened_or_hashed']is False and review['new_raw1984B_only_decoded']is True and all(review[k]is False for k in('business_executed','numerical_executed','compiler_executed','files_deleted','native_child_reexecuted','actual_capture_executed_by_reviewer','Source_generation_executed_by_reviewer')),'exact temperature post permits new1984B-only verification and no old science body')
  require(review['selected_pread_payload_bytes_only']==1984 and all(review[k]is True for k in('complete_metadata_Source_full_EOF_PF_verified_twice','actual_Host_fixed_Source_metadata_current7_verified_twice','old_scientific_inputs_current7_verified_twice','inherited_metadata_current7_verified_twice'))and all(review[k]is False for k in('temperature_interpolation_replayed','current_SPH_MASK_context_applied','native_AxMatTone_temperature_mapping_qualified','physics_qualified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete')),'actual stored temperature operand pass only; node and interpolation mapping remain unqualified')
 elif status=='PASS_FAILURE_FACTS_ONLY':
  require(review['schema']=='INDEPENDENT_ACTUAL_FULL370_V5_FAILURE_FACTS_METADATA_ASSESSMENT_V1'and review['metadata_only']is True and review['actual_Root_original_integer_exit_code']==actual_code,'exact fullv5 failure-facts metadata only, actual1 retained')
 else:
  require(review['schema']=='INDEPENDENT_EIGHT_SERIAL_FUEL_FINITE18_SCAT_ACTUAL_RUNTIME_METADATA_POSTVERIFY_V1'and review['metadata_only']is True and actual_code==0,'exact completed fuel finite18 metadata post only')
 return review,pr,pt
def numerical_AST_proof():
 old=(FUEL/'compare_eight_fuel_finite18_SCAT.py').read_text();new=(BASE/SOURCE_NAMES[0]).read_text();ot=ast.parse(old);nt=ast.parse(new);original={v.name:v for v in ot.body if isinstance(v,(ast.FunctionDef,ast.ClassDef))};candidate={v.name:v for v in nt.body if isinstance(v,(ast.FunctionDef,ast.ClassDef))};unchanged=[]
 for name in('require','identity','current','metadata','pin','module','target_leaf','compare_leaf','extract'):
  require(ast.dump(original[name],include_attributes=False)==ast.dump(candidate[name],include_attributes=False),'whole original unchanged mathematical extraction/leaf function AST');unchanged.append(name)
 def excerpt(text,node):return '\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
 a=excerpt(old,original['replay_temperature']);b=excerpt(new,candidate['replay_temperature']);restored=b;changes=[]
 allowed=(('len(dilutions)==9 and len(set(dilutions))==9','len(dilutions)==18 and len(set(dilutions))==18'),('SCI1 original9 ascending finite dilution words','SCI1 original18 ascending finite dilution words'),('original single archive infinite+9 widths/ipflag0','original fuel infinite+9 widths/ipflag0'),('finite original accumulated all10 single-archive P0','finite original accumulated all10 fuel P0'),('exact_finite9_lane_P0_raw_words_equal','exact_finite18_lane_P0_raw_words_equal'))
 for candidate_text,original_text in allowed:
  require(restored.count(candidate_text)==1,'sole exact replay adapter source occurrence');restored=restored.replace(candidate_text,original_text);changes.append(dict(candidate=candidate_text,original=original_text))
 require(restored==a and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(a),include_attributes=False),'sole nine-DILUTION membership plus diagnostic labels; entire replay numerical AST reconstructed')
 return dict(whole_original_function_AST_unchanged=unchanged,replay_temperature_original_Source_hex=a.encode().hex(),replay_temperature_candidate_Source_hex=b.encode().hex(),exact_replay_adapter_inverse=changes,replay_numerical_AST_restored_exactly=True,replay_arithmetic_assignments_loop_order_and_calls_unchanged=True,normalized_original_AST_sha256=hashlib.sha256(ast.dump(ast.parse(a),include_attributes=False).encode()).hexdigest())
def inverse(old,new):
 a=Path(old).read_bytes();b=Path(new).read_bytes();start=0
 while start<min(len(a),len(b))and a[start]==b[start]:start+=1
 tail=0
 while tail<min(len(a)-start,len(b)-start)and a[-1-tail]==b[-1-tail]:tail+=1
 ae=len(a)-tail;be=len(b)-tail;restored=b[:start]+a[start:ae]+b[be:];require(restored==a,'whole original byte inverse')
 return dict(original_Source_pin=pin(old),candidate_Source_pin=pin(new),edit=dict(original_begin_byte=start,original_end_byte=ae,candidate_begin_byte=start,candidate_end_byte=be,original_bytes_hex=a[start:ae].hex(),candidate_bytes_hex=b[start:be].hex()),complete_inverse_reconstructs_original=True,restored_original_sha256=hashlib.sha256(restored).hexdigest())
def route_decks(row):
 proof=row['historical_proof'];gp=Path(proof['actual_GROUPR_deck_pin']['path']);dp=Path(proof['actual_DRAGR_deck_pin']['path']);require(pin(gp)==proof['actual_GROUPR_deck_pin']and pin(dp)==proof['actual_DRAGR_deck_pin'],'exact original existing deck Source pins');lines=[s.strip()for s in gp.read_text().splitlines()if s.strip()];i=lines.index('groupr');card=[int(v)for v in lines[i+2].split()];require(card[0]==row['mat']and card[5]==7 and card[6]==10,'original MAT/7T/NZ10 GROUPR');at=i+3
 while lines[at].startswith("'"):at+=1
 parts=[]
 while True:
  parts.append(lines[at]);at+=1
  if '/'in parts[-1]:break
 temps=[float(v)for v in ' '.join(parts).split('/')[0].split()];require(temps==row['original_source_deck_temperatures_K'],'whole original deck exact seven temperatures');parts=[]
 while True:
  parts.append(lines[at]);at+=1
  if '/'in parts[-1]:break
 sigma=[float(v)for v in ' '.join(parts).split('/')[0].split()];require(sigma==[1e10,1e4,3546.310,1257.430,445.8898,158.1139,56.0677,19.8818,7.0501,2.5],'original infinity plus nine finite sigma0 deck')
 lines=[s.strip()for s in dp.read_text().splitlines()if s.strip()];i=lines.index('dragr');card=[int(v)for v in lines[i+1].split('/')[0].split()];require(len(card)==11 and card[5]==0 and card[6]==30 and card[7]==0,'original nimpo0/nexpo30/ipflag0');i=lines.index(row['original_DRAGR_material_card_ascii']);require(row['original_DRAGR_material_card_ascii']==str(row['mat'])+' '+row['nuclide']+' 0 /'and lines[i+1].startswith("'"),'original NBESP0 literal material card');bounds=[float(v)for v in lines[i+2].split('/')[0].split()];require(bounds==[4.632489,1050830.0]and float(lines[i+3].split('/')[0])==4.0,'original selfshield/thermal cards');return bounds
def cumulative(roots,explicit):
 total=0
 for root in roots:
  if not Path(root).exists():continue
  for q in Path(root).rglob('*'):
   s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'no inherited joint namespace alias')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 for p in explicit:
  current(p)
  if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):total+=p['size_bytes']
 return total
def main():
 require(not os.path.lexists(OUT)and not os.path.lexists(BASE/'PLAN.json')and not os.path.lexists(BASE/'SOURCE_REVIEW_READY.json'),'once fresh remaining producer Source preparation')
 author,pa=read(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');require(author['Source_files_frozen_before_Root_generation']is True and author['Source_preparation_executed_by_author']is False and author['Source_publication_executed_by_author']is False and author['business_executed_by_author']is False,'Root sole execution and frozen Source before generation')
 for p in author['whole_Source_file_pins']:require(pin(p['path'])==p,'all author Source unchanged')
 prior,pp=read(FUEL/'PLAN.json');ready,pReady=read(FUEL/'SOURCE_REVIEW_READY.json');oldproof,pOldProof=read(FUEL/'ORIGINAL_MATH_AND_MINIMAL_SOURCE_INVERSE.json');all34,pAll34=read(ALL34/'PLAN.json');full,pFull=read(FULL/'PLAN.json')
 require(prior['original_caps']==CAPS and full['original_caps']==CAPS and len(prior['complete_joint_roots'])==52 and len(full['complete_joint_roots'])==57 and full['complete_joint_roots'][:52]==prior['complete_joint_roots']and str(BASE.parent)in full['complete_joint_roots'],'exact whole prior52 included in current57; nested Source adds no root')
 roots=full['complete_joint_roots']+[str(OUT)];require(len(roots)==58 and len(set(roots))==58 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'append only one fresh output58; no root reset')
 actual,ptools=read(FUEL/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');stdout=genuine(actual,'actual_terminal_return',0);host,pHost=read(ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2/Root_actual_eight_fuel_finite18_SCAT_summary.json');require(stdout['report_pin']==pHost and host['status']=='ACTUAL_EIGHT_FUEL_64T_FINITE18_P0_WORDS_CLOSED0_ONLY'and host['failure']is None and host['final_report_resource_check_passed']is True,'original completed fuel finite18 retained, not repeated');_,pFuelPost,pFuelPostTools=post_pair(FUEL/'actual_postverify_20261015/corrected_argument_identity_v2',pHost,ptools,0,'PASS_ACTUAL_EIGHT_FUEL_64T_128LANET_1152NODES_3456_FINITE_P0_LEAF_WORDS')
 failed,pFailTools=read(FULL/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');genuine(failed,'actual_terminal_return',1);fh,pFailHost=read(ART/'axial-material-current-full370-real-operator-control-20261015-v3/Root_actual_full370_real_operator_control_summary.json');require(fh['failure']is not None and fh['actual_control_results']is None and fh['original_caps']==CAPS,'full370 failed actual1 and no invented control completion');_,pFailPost,pFailPostTools=post_pair(FULL/'actual_failure_metadata_assessment_20261015',pFailHost,pFailTools,1,'PASS_FAILURE_FACTS_ONLY')
 temp,pTempTools=read(TEMP/'ROOT_ACTUAL_TRUE_TOOL_RETURNS.json');genuine(temp,'actual_terminal_return',0);th,pTempHost=read(TEMP/'actual_temperature_operand_capture/Root_actual_temperature_operand_capture_summary.json');require(th['status']=='ACTUAL_TEMPERATURE_OPERAND_CAPTURE_CLOSED0_ONLY'and th['failure']is None,'actual temperature capture only retained');_,pTempPost,pTempPostTools=post_pair(TEMP/'actual_postverify_20261015',pTempHost,pTempTools,0,'PASS_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_ONLY_POSTVERIFICATION')
 inputs=[];deckpins=[]
 for name,mat in(('Cr52',2431),('Fe56',2631)):
  row=dict(next(v for v in all34['inputs']if v['nuclide']==name));require(row['mat']==mat and row['SCI_role']=='SCI1'and row['original_DRAGR_NBESP']==0 and row['original_expected_nz']==10 and row['original_nimpo_unit']==0 and row['original_ipflag']==0 and row['original_drahd_existing_ENERGY_REAL32_branch']is False and row['original_source_deck_temperatures_K']==[293.0,550.0,748.1500244140625,893.1500244140625,900.0,1200.0,2000.0],'literal original remaining single archive route');current(row['current_original_input_full_pin']);row.update(lane='single',original_selfshielding_energy_bounds_eV=route_decks(row),source_claim_scope='single original archive own infinity and elastic flux to all nine actual finite SCI1 P0 delta words only');inputs.append(row);deckpins.extend(p for p in row['historical_proof'].values()if type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'})
 require([v['input_encoding']for v in inputs]==['gzip','ASCII']and sum(v['original_ASCII_expected_size_bytes']for v in inputs)==26790912,'two distinct original archives exact26790912 ASCII EOF bytes')
 current(prior['actual_current_SCI1_pin']);copies=[]
 for name in SOURCE_NAMES[4:]:
  po=pin(FUEL/name);pc=pin(BASE/name);require(po['sha256']==pc['sha256']and po['size_bytes']==pc['size_bytes']and (FUEL/name).read_bytes()==(BASE/name).read_bytes(),'whole original math/stream/SCI/guard/publisher Source copies');copies.append(dict(original_full_pin=po,whole_unchanged_copy_full_pin=pc))
 proof=dict(schema='REMAINING_CR52_FE56_FINITE9_ORIGINAL_MATH_SOURCE_INVERSE_V1',prior_original_math_proof_pin=pOldProof,whole_original_source_copies=copies,exact_function_Source_and_AST_inverse=numerical_AST_proof(),worker_complete_byte_inverse=inverse(FUEL/'compare_eight_fuel_finite18_SCAT.py',BASE/SOURCE_NAMES[0]),host_complete_byte_inverse=inverse(FUEL/'run_guarded_eight_fuel_finite18_SCAT.py',BASE/SOURCE_NAMES[1]),publisher_complete_byte_inverse=inverse(FUEL/'write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py',BASE/SOURCE_NAMES[2]),math_scalar_matrix_and_packed_whole_unchanged=True,original_P0_sum_thermal_order_cutoffs_flux_ratio_and_own_infinity_unchanged=True,original_REAL32_temperature_and_DILUTION_identity_mapping_preserved=True,original_REAL32_support_1e_minus6_and_tail_1e_minus8_retained=True,new_GENDF_binary64_ENERGY_cutoff_branch_required=True,SCI_DILUTION_actual_nine_membership_required=True,scientific_payload_read=False,**FALSE);write(BASE/'ORIGINAL_MATH_AND_MINIMAL_SOURCE_INVERSE.json',proof);pProof=pin(BASE/'ORIGINAL_MATH_AND_MINIMAL_SOURCE_INVERSE.json')
 metadataPins=unique(ready['dependencies']+deckpins+[pp,pReady,pOldProof,pAll34,pFull,pa,ptools,pHost,pFuelPost,pFuelPostTools,pFailTools,pFailHost,pFailPost,pFailPostTools,pTempTools,pTempHost,pTempPost,pTempPostTools])
 for p in metadataPins:require(pin(p['path'])==p,'whole retained Source/metadata dependencies unchanged; no science body')
 inherited=unique(full['explicit_cumulative_metadata_file_pins']);explicit=unique(inherited+metadataPins+[pProof]+[pin(BASE/n)for n in SOURCE_NAMES]);before=cumulative(roots,explicit);require(before+16*2**20+96*2**20<2*2**30,'unchanged cumulative2GiB reserves16MiB Source metadata and96MiB new output')
 plan=dict(prior);plan.update(schema='REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_ONLY_PLAN_V1',planned_actual_output_root=str(OUT),complete_joint_roots=roots,inherited_complete57_plan_pin=pFull,inherited_metadata_current7_pins=inherited,explicit_cumulative_metadata_file_pins=explicit,inputs=inputs,execution_nuclides=['Cr52','Fe56'],expected_serial_children=2,expected_per_child_archives=1,expected_per_child_native_temperature_records=7,expected_per_child_finite_nodes=63,expected_per_child_leaf_records=189,expected_nuclides=2,expected_archives=2,expected_temperature_records=14,expected_archive_temperature_records=14,expected_finite_dilution_nodes=126,expected_leaf_records=378,original_decompressed_payload_expected_bytes=26790912,original_compressed_payload_expected_bytes=inputs[0]['current_original_input_full_pin']['size_bytes'],prior_fuel_actual_summary_pin=pHost,prior_fuel_actual_tools_pin=ptools,prior_fuel_actual_post_pin=pFuelPost,prior_fuel_actual_post_tools_pin=pFuelPostTools,prior_fullv5_failed_summary_pin=pFailHost,prior_fullv5_failed_tools_pin=pFailTools,prior_fullv5_failure_post_pin=pFailPost,prior_fullv5_failure_post_tools_pin=pFailPostTools,current_temperature_actual_summary_pin=pTempHost,current_temperature_actual_tools_pin=pTempTools,current_temperature_actual_post_pin=pTempPost,current_temperature_actual_post_tools_pin=pTempPostTools,author_Pre_Root_generation_Source_freeze_pin=pa,original_scalar_helper_source_copy_pin=copies[0]['whole_unchanged_copy_full_pin'],original_bounded_SCI_helpers_copy_pin=copies[1]['whole_unchanged_copy_full_pin'],original_stream_helpers_copy_pin=copies[2]['whole_unchanged_copy_full_pin'],original_whole_math_inverse_proof_pin=pProof,bounded_new_output_reservation_bytes=96*2**20,bounded_Source_generation_metadata_reservation_bytes=16*2**20,new_output_reservation_components=dict(two_child_reports=16*2**20,aggregate_report=16*2**20,host_summary=32*2**20,execution_binding=2*2**20,runtime_watch_logs_stage_other=30*2**20),Source_only_cumulative_bytes_before_reserved_new_metadata=before,scope='Two remaining current SCI1 Cr52/Fe56 single original archives;14 native temperatures;126 finite dilution nodes;378 SCAT00/NJJS00/IJJS00 P0 leaf records only. Interpolation, P1, current SPH/MASK mapping, reaction multiplicity, complete neutron balance, independent reference and AAA/ABA remain unqualified.',**FALSE);write(BASE/'PLAN.json',plan);pPlan=pin(BASE/'PLAN.json');sources=[pin(BASE/n)for n in SOURCE_NAMES]+[pProof];dependencies=unique(metadataPins+sources+[pPlan]);oldCLI,_=read(FUEL/'FINAL_ROOT_REVIEWABLE_CLI.json')
 value=dict(schema='REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pPlan,host_source_pin=pin(BASE/SOURCE_NAMES[1]),final_publisher_Source_pin=pin(BASE/SOURCE_NAMES[2]),complete_source_file_pins=sources,dependencies=dependencies,selected_Source_pins=dependencies,inherited_metadata_current7_pins=inherited,original_caps=CAPS,original_complete_ENV_Python_B_prefix=oldCLI['argv'][:11],actual_business_started=False,Root_final_publication_executed=False,scientific_payload_read=False,**FALSE);write(BASE/'SOURCE_REVIEW_READY.json',value);require(cumulative(roots,unique(explicit+[pPlan,pin(BASE/'SOURCE_REVIEW_READY.json')]))+96*2**20<2*2**30,'Source generation and bounded future output preserve original cumulative cap');print(json.dumps(dict(status='REMAINING_CR52_FE56_FINITE9_SCAT_SOURCE_PREPARATION_ONLY',ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json'),**FALSE)),flush=True)
if __name__=='__main__':main()

"""Root-only once Source preparation; old science bodies remain unopened."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts';BASE=Path(__file__).absolute().parent
PRIOR=REC/'current_eight_fuel_finite18_SCAT_producer_source_v1_20261015/remaining_Cr52_Fe56_source_v2';ALL34=REC/'current_all34_original_ASCII_infinite_SCAT_producer_source_v1_20261015/v2'
ALL34OUT=ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1'
OUT=ART/'axial-material-current-extra21-reaction-event-production-capture-20261015-v1'
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,MT5_partition_qualified=False,fission_producer_replayed=False,reaction_exclusive_partition_qualified=False,selected_capture_complete=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
NAMES=('capture_extra21_original_ascii_event_production.py','run_guarded_extra21_original_ascii_event_production.py','write_once_Root_extra21_reaction_capture_SF_HF_CLI.py','prepare_extra21_reaction_capture_Source.py','original_check_mt51_repair.py','original_four_ascii_stream_helpers.py','original_dragr.f90','original_guard_host.py','original_once_publisher.py')
MTS={'Cr50':[44],'Cr53':[32],'Ni58':[22],'Ni60':[22],'Ni61':[22,32],'Ni62':[22],'Ni64':[22],'O16':[22,23],'Si28':[22],'Ti48':[22],'Mo92':[22],'Mo94':[22],'Mo95':[22,24,41],'Mo96':[22],'Mo97':[22],'Mo98':[22],'Mo100':[22]}
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes'],'ordinary exact current7')
def pin(q):
 q=Path(q);s=q.lstat()
 with q.open('rb')as h:digest=hashlib.file_digest(h,'sha256').hexdigest();require(identity(os.fstat(h.fileno()))==identity(s),'Source/metadata fullEOF opened7')
 p=dict(path=str(q),sha256=digest,size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(q):
 p=pin(q);require(p['size_bytes']<8*2**20,'bounded exact Source preparation metadata');v=json.loads(Path(q).read_bytes());require(pin(q)==p,'same whole metadata');return v,p
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'new Source metadata8MiB each');own=[BASE/n for n in('ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json','PLAN.json','SOURCE_REVIEW_READY.json')];require(sum(p.stat().st_size for p in own if p.exists())+len(raw)<16*2**20,'all owning Source generation metadata below16MiB reserve')
 with Path(q).open('xb')as h:h.write(raw);h.flush();os.fsync(h.fileno())
def unique(rows):
 out={}
 for p in rows:
  if p['path']in out:require(out[p['path']]==p,'same path same complete PF')
  out[p['path']]=p
 return list(out.values())
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def genuine(v,key,code):
 t=v[key];require(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'original genuine closed typed integer')
 return json.loads(t['output'].strip().splitlines()[-1])if code==0 else None
def cumulative(roots,explicit):
 total=0
 for root in roots:
  if not Path(root).exists():continue
  for q in Path(root).rglob('*'):
   s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'no cumulative namespace aliases')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 for p in explicit:
  current(p)
  if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):total+=p['size_bytes']
 return total
def main():
 require(not os.path.lexists(OUT)and not os.path.lexists(BASE/'PLAN.json')and not os.path.lexists(BASE/'SOURCE_REVIEW_READY.json'),'new once Source/output entry')
 author,pa=read(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');require(author['Source_files_frozen_before_Root_generation']is True and all(author[k]is False for k in('Source_preparation_executed_by_author','Source_publication_executed_by_author','business_executed_by_author')),'Root sole generation/publication/business')
 for p in author['whole_Source_file_pins']:require(pin(p['path'])==p,'complete author Source unchanged')
 prior,pp=read(PRIOR/'PLAN.json');priorready,pr=read(PRIOR/'SOURCE_REVIEW_READY.json');require(prior['original_caps']==CAPS and len(prior['complete_joint_roots'])==59 and str(BASE.parent)in prior['complete_joint_roots'],'all prior59 roots and already-counted SourceTOP')
 actual,pactual=read(PRIOR/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');stdout=genuine(actual,'actual_terminal_return',0);post,ppost=read(PRIOR/'actual_postverify_20261015/REVIEW.json');posttools,pptools=read(PRIOR/'actual_postverify_20261015/TRUE_TOOL_RETURNS.json');pstdout=genuine(posttools,'actual_review_return',0)
 require(pstdout['review_pin']==ppost and post['schema']=='INDEPENDENT_REMAINING_CR52_FE56_ACTUAL_RECORDED_COMPARISON_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_REMAINING_CR52_FE56_FINITE9_RECORDED_COMPARISON_METADATA_ONLY'and post['failure']is None and post['actual_Root_original_integer_exit_code']==0 and post['actual_Host_report_pin']==stdout['report_pin']and post['actual_Root_tools_pin']==pactual and post['reported_P0_leaf_records']==378 and post['reported_raw_word_mismatches']==0,'genuine completed remaining Cr52/Fe56 finite P0 actual0/post0 inherited59')
 roots=prior['complete_joint_roots']+[str(OUT)];require(len(roots)==60 and len(set(roots))==60 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete inherited59 exact ordered prefix plus sole newoutput60')
 allplan,pallplan=read(ALL34/'PLAN.json');allactual=ALL34OUT/'inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json';pallactual=pin(allactual);require(pallactual['size_bytes']<32*2**20,'literal all34 metadata report32MiB');allvalue=json.loads(allactual.read_bytes());require(pin(allactual)==pallactual and allvalue['schema']=='ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_PRODUCER_COMPARISON_V1'and allvalue['compared_unique_nuclides']==34 and allvalue['compared_temperature_records']==234,'canonical complete actual compact all34 ledger, no scientific array decoding')
 selected=[];pairs=[]
 for row in allplan['inputs']:
  if row['nuclide']not in MTS:continue
  current(row['current_original_input_full_pin']);original=next(r for r in allvalue['actual_extractions']if r['nuclide']==row['nuclide']);ledger=original['actual_MF3_MF6_compact_inventory'];require(original['current_original_input_full_pin']==row['current_original_input_full_pin']and original['actual_original_ASCII_EOF_SHA256']==row['original_ASCII_expected_sha256'],'same actual all34 original source input lineage')
  for mt in MTS[row['nuclide']]:
   a=[s for s in ledger if s['mf']==3 and s['mt']==mt];b=[s for s in ledger if s['mf']==6 and s['mt']==mt];require(len(a)==len(b)==len(row['original_source_deck_temperatures_K'])and [s['temperature_K']for s in a]==[s['temperature_K']for s in b]and all(s['nl']==1 and s['nz']==1 for s in a)and all(s['nl']==(1 if row['SCI_role']=='SCI2'else 2)and s['nz']==1 for s in b),'exact original channel/nativeT/NL/NZ coverage')
   pairs.append(dict(nuclide=row['nuclide'],MT=mt,SCI_role=row['SCI_role'],native_temperature_sections=len(a),actual_native_temperatures_K=[s['temperature_K']for s in a],MF3_nl=1,MF6_nl=b[0]['nl'],actual_nz=1,MT5_in_both_MF3_MF6=any(s['mf']==3 and s['mt']==5 for s in ledger)and any(s['mf']==6 and s['mt']==5 for s in ledger),MT5_partition_qualified=False))
  selected.append(dict(input=row,selected_MTs=MTS[row['nuclide']],all_compact_metadata_sections=ledger))
 selectedMF3Lists=sum(v['LIST_records']for s in selected for v in s['all_compact_metadata_sections']if v['mf']==3 and v['mt']in s['selected_MTs']);selectedMF6Lists=sum(v['LIST_records']for s in selected for v in s['all_compact_metadata_sections']if v['mf']==6 and v['mt']in s['selected_MTs']);require(selectedMF3Lists==768 and selectedMF6Lists==576,'canonical selected raw P0 LIST metadata counts768/576')
 require(len(selected)==17 and len(pairs)==21 and sum(p['native_temperature_sections']for p in pairs)==131 and sum(v['input']['original_ASCII_expected_size_bytes']for v in selected)==92876787,'exact selected17 NU/21 pairs/131T/92,876,787 original ASCII bytes')
 copies=[]
 for name in('original_check_mt51_repair.py','original_four_ascii_stream_helpers.py','original_dragr.f90','original_once_publisher.py'):
  a=pin(PRIOR/name);b=pin(BASE/name);require(a['sha256']==b['sha256']and a['size_bytes']==b['size_bytes']and(PRIOR/name).read_bytes()==(BASE/name).read_bytes(),'whole original Source copy unchanged');copies.append(dict(original_Source_pin=a,whole_unchanged_copy_full_pin=b))
 oldhost=pin(ALL34/'run_guarded_all34_original_ascii_infinite_SCAT.py');require((BASE/'original_guard_host.py').read_bytes()==Path(oldhost['path']).read_bytes(),'whole old original guard host Source preserved');copies.append(dict(original_Source_pin=oldhost,whole_unchanged_copy_full_pin=pin(BASE/'original_guard_host.py')))
 for name in NAMES:
  if name.endswith('.py'):ast.parse((BASE/name).read_text())
 worker=(BASE/NAMES[0]).read_text();host=(BASE/NAMES[1]).read_text();require("for outgoing in range(370):total+=float(p0[ig,outgoing])"in worker and "matrix,flux=scalar.matrix(section)"in worker and "active['event'][370-ig]=p0[1]"in worker and "self.last=time.monotonic()"in worker and "claim.open('x')"in host and host.index("claim.open('x')")<host.index("sf,psf=argument('source-freeze')")and "Path(runner.bounded.__file__).resolve()==runtime/'run_bounded_dragon.py'"in host,'explicit original parser/matrix/FVECT association, fixed full-scan clock and Root claim/bounded runner identity')
 proof=dict(schema='EXTRA21_ORIGINAL_PARSER_MATRIX_FVECT_AND_GUARD_SOURCE_PROOF_V1',whole_original_source_copies=copies,original_fvect_source_line_scope=[2350,2354],original_fmatr_source_line_scope=[2235,2263],original_fvect_flux_first_event_second_NLNZ_row=True,original_scalar_number_and_matrix_functions_copied_whole_and_called=True,original_GROUPR_already_formatted_no_requantization=True,own_flux_division_performed=False,P0_only_selected_from_original_NLNZ_stride=True,selected_nz1_actual_metadata_exact=True,original_Mo_ipflag1_not_applied_to_raw_production_matrix=True,original_budget_disk_stamp_after_full_scan=True,entire_output192MiB_additional_bound=True,original_OwnRSS_serial_executor_and_Process_PS_MRO_reused=True,Root_actual_exec_command_require_escalated_required=True,Source_author_no_scientific_payload=True,**FALSE);write(BASE/'ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json',proof);pproof=pin(BASE/'ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json')
 scientificDocs=unique(post['eleven_scientific_extraction_document_pins']+[pallactual]);metadata=unique(priorready['dependencies']+[pp,pr,pactual,ppost,pptools,pallplan,pallactual,pa,pproof,pin(BASE/'EXTRA_REACTION_SOURCE_SCOPE_DRAFT.json')]);scientificDocPaths={p['path']for p in scientificDocs}
 for p in metadata:
  current(p)
  if p['path']not in scientificDocPaths:require(pin(p['path'])==p,'same retained metadata/Source fullEOF, old scientific documents current7 only')
 inherited=unique(prior['explicit_cumulative_metadata_file_pins']);sources=[pin(BASE/n)for n in NAMES]+[pproof];explicit=unique(inherited+metadata+sources);before=cumulative(roots,explicit);require(before+16*2**20+192*2**20<2*2**30,'unchanged cumulative2GiB strict owning Source16MiB+entire output192MiB reserve; no reset')
 cli,pcli=read(PRIOR/'FINAL_ROOT_REVIEWABLE_CLI.json');plan=dict(prior);plan.update(schema='EXTRA21_REACTION_CAPTURE_SOURCE_ONLY_PLAN_V1',planned_actual_output_root=str(OUT),complete_joint_roots=roots,inherited_complete59_plan_pin=pp,inherited_metadata_current7_pins=inherited,explicit_cumulative_metadata_file_pins=explicit,selected_inputs=selected,inputs=[s['input']for s in selected],selected_channel_pairs=pairs,expected_nuclides=17,expected_channel_pairs=21,expected_channel_temperature_records=131,expected_selected_sections=262,original_decompressed_payload_expected_bytes=92876787,bounded_new_output_reservation_bytes=192*2**20,bounded_new_Source_metadata_reservation_bytes=16*2**20,retained_P0_dense_matrix_payload_bytes=143471200,expected_selected_MF3_LIST_records=768,expected_selected_MF6_LIST_records=576,selected_raw_P0_LIST_numeric_upper_bound_bytes=1721856,raw_selected_P0_LIST_operands_planned=True,scientific_extraction_documents_current7_only_pins=scientificDocs,prior_remaining_Cr52_Fe56_actual0_pin=pactual,prior_remaining_Cr52_Fe56_post0_pin=ppost,prior_remaining_Cr52_Fe56_post_tools0_pin=pptools,canonical_all34_compact_inventory_pin=pallactual,original_scalar_helper_source_copy_pin=pin(BASE/'original_check_mt51_repair.py'),original_stream_helpers_copy_pin=pin(BASE/'original_four_ascii_stream_helpers.py'),original_source_proof_pin=pproof,author_Pre_Root_generation_Source_freeze_pin=pa,Root_actual_exec_command_sandbox_permissions_required='require_escalated',Source_only_cumulative_bytes_before_reservations=before,scope='Selected21 nonfission MF3 event/MF6 P0 neutron production operands; 131 native cohorts. Raw original before Mo diagonal lump. No reaction-completeness/fission/MT5/exclusive-partition/reference/physics/AAA/ABA admission.',**FALSE);write(BASE/'PLAN.json',plan);pplan=pin(BASE/'PLAN.json');dependencies=unique(metadata+sources+[pplan]);ready=dict(schema='EXTRA21_REACTION_CAPTURE_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pplan,host_source_pin=pin(BASE/NAMES[1]),final_publisher_Source_pin=pin(BASE/NAMES[2]),complete_source_file_pins=sources,dependencies=dependencies,selected_Source_pins=dependencies,inherited_metadata_current7_pins=inherited,scientific_extraction_documents_current7_only_pins=scientificDocs,original_caps=CAPS,original_complete_ENV_Python_B_prefix=cli['argv'][:11],actual_business_started=False,Root_final_publication_executed=False,Root_actual_exec_command_sandbox_permissions_required='require_escalated',scientific_payload_read=False,**FALSE);write(BASE/'SOURCE_REVIEW_READY.json',ready);require(cumulative(roots,unique(explicit+[pplan,pin(BASE/'SOURCE_REVIEW_READY.json')]))+192*2**20<2*2**30,'exact all Sourcegen metadata plus next entire output192MiB preserves cumulative2GiB');print(json.dumps(dict(status='EXTRA21_REACTION_CAPTURE_SOURCE_PREPARATION_ONLY',ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json'),**FALSE)),flush=True)
if __name__=='__main__':main()

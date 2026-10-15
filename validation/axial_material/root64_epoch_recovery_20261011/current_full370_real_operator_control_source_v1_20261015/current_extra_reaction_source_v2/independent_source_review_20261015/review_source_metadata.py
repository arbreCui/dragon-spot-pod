"""Frozen Source eligibility review only; never import a candidate or science helper."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

HERE=Path(__file__).absolute().parent; BASE=HERE.parent; PREVIOUS=BASE.parent/'current_extra_reaction_source_v1'
R=Path('/Users/wen/spot'); ART=R/'validation/artifacts'
OUT=ART/'axial-material-current-extra21-reaction-event-production-capture-20261015-v1'
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

MTS={'Cr50':[44],'Cr53':[32],'Ni58':[22],'Ni60':[22],'Ni61':[22,32],'Ni62':[22],'Ni64':[22],'O16':[22,23],'Si28':[22],'Ti48':[22],'Mo92':[22],'Mo94':[22],'Mo95':[22,24,41],'Mo96':[22],'Mo97':[22],'Mo98':[22],'Mo100':[22]}
COLUMNS=('section_index_one_based','mat','mf','mt','nl','nz','energy_groups','temperature_K','section_header_sha256','LIST_records','LIST_dimension_sequence_sha256','incident_present_mask_hex','spectrum_LIST_present')
def rowbytes(row):
 need(set(row)==set(COLUMNS),'exact original thirteen compact fields')
 return(json.dumps(row,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def function_or_class(raw,name):
 text=raw.decode();node=next(n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name)
 return ast.get_source_segment(text,node).encode()
def source_inverse(old,new):
 # Only the complete inventory representation, validation and report metadata change.
 text=new.decode();previous=old.decode()
 added="COMPACT_ROW_COLUMNS="+text.split('COMPACT_ROW_COLUMNS=',1)[1].split('class Budget:',1)[0]
 need('def canonical_compact_record_bytes(row):'in added and len(added.splitlines())==4,'one added canonical metadata serializer')
 text=text.replace(added,'',1)
 def get(value,prefix):
  rows=[line for line in value.splitlines(keepends=True)if line.startswith(prefix)];need(len(rows)==1,'unique approved metadata adapter line');return rows[0]
 for prefix in(" row=selected['input'];", "   require(key is None,'complete original final boundary');", " current(p);return dict(nuclide=row['nuclide']"):
  text=text.replace(get(text,prefix),get(previous,prefix),1)
 begin=text.index("   require(cursor<selected['all_compact_metadata_section_count']")
 end=text.index("   if active['selected']:\n    active['metadata']=e",begin)
 oldbegin=previous.index("   require(cursor<len(expected)")
 oldend=previous.index("   if active['selected']:\n    active['metadata']=e",oldbegin)
 replacement=text[begin:end]
 need('full_inventory_digest.update(canonical_compact_record_bytes(observed))'in replacement and "observed==e"in replacement,'approved all-inventory digest and selected exact-row metadata adapter')
 text=text[:begin]+previous[oldbegin:oldend]+text[end:]
 need(text.encode()==old,'complete v2 worker restores whole v1 after four metadata adapters only')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--reviewer-freeze-pin',required=True);a=ap.parse_args()
 fp=strict(a.reviewer_freeze_pin);freeze=read(fp);eof(freeze['reviewer_source_pin'])
 need(freeze['schema']=='INDEPENDENT_EXTRA21_V2_SOURCE_REVIEWER_FREEZE_V1'and freeze['reviewer_AST_passed_before_freeze']is True and freeze['reviewer_source_pin']['path']==str(Path(__file__).absolute()),'exact own frozen Source')
 ready=read(freeze['ready_pin']);generation=read(freeze['canonical_generation_tools_pin'])
 closed(generation,'actual_Source_preparation_return',freeze['ready_pin'],'ready_pin')
 gs=strict(generation['actual_Source_preparation_return']['output'].strip().splitlines()[-1])
 need(gs['status']=='EXTRA21_REACTION_CAPTURE_SOURCE_PREPARATION_ONLY'and all(gs[k]is False for k in('business_executed','numerical_executed','compiler_executed','files_deleted')),'genuine Source preparation0 only')
 need(ready['schema']=='EXTRA21_REACTION_CAPTURE_SOURCE_REVIEW_READY_V1'and ready['Source_entry_version']==2 and ready['source_only']is True and ready['actual_business_started']is False and ready['Root_final_publication_executed']is False and ready['original_caps']==CAPS and ready['selected_Source_pins']==ready['dependencies'],'same-round selected Source metadata')
 selected=unique(ready['selected_Source_pins']+[freeze['ready_pin'],freeze['canonical_generation_tools_pin']])
 exceptions=[p for p in selected if p['path']in EXCEPTIONS]
 need(len(exceptions)==12 and {p['path']:p for p in ready['scientific_extraction_documents_current7_only_pins']}=={p['path']:p for p in exceptions},'exact eleven extraction documents plus canonical all34 report exceptions')
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 plan=read(ready['control_plan_pin']);proof=read(plan['original_source_proof_pin']);author=read(plan['author_Pre_Root_generation_Source_freeze_pin'])
 need(plan['schema']=='EXTRA21_REACTION_CAPTURE_SOURCE_ONLY_PLAN_V1'and plan['Source_entry_version']==2 and plan['original_caps']==CAPS and author['schema']=='AUTHOR_EXTRA21_REACTION_CAPTURE_PRE_ROOT_GENERATION_SOURCE_FREEZE_V2'and author['Source_files_frozen_before_Root_generation']is True and author['Source_preparation_executed_by_author']is False and author['business_executed_by_author']is False,'frozen sole Root Source preparation domain')
 for value in(ready,plan,proof,author):
  need(all(value[k]is False for k in FALSE if k in value),'original unqualified business/physics flags')
 for p in author['whole_Source_file_pins']:eof(p)
 need(len(ready['complete_source_file_pins'])==10,'nine candidate/copied files plus Source proof')
 for p in author['whole_Source_file_pins']:
  if Path(p['path']).suffix=='.py':ast.parse(Path(p['path']).read_bytes(),filename=p['path'])
 absent=('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_EXECUTION_CLAIM_RECEIPT.json')
 need(not os.path.lexists(OUT)and not any(os.path.lexists(BASE/n)for n in absent),'no current publication/business claim/output')
 prior=read(plan['inherited_complete59_plan_pin']);roots=plan['complete_joint_roots']
 need(roots==prior['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))==60 and len(prior['complete_joint_roots'])==59 and str(BASE.parent)in roots[:-1]and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'unchanged inherited59 plus only never-claimed pending OUT60')
 inherited=unique(ready['inherited_metadata_current7_pins'])
 need(inherited==plan['inherited_metadata_current7_pins']==prior['explicit_cumulative_metadata_file_pins'],'complete inherited metadata current7 scope')
 for p in inherited:current(p)
 need(plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['bounded_new_output_reservation_bytes']==192*2**20 and plan['Source_only_cumulative_bytes_before_reservations']+208*2**20<2*2**30,'unchanged cumulative2GiB strict Source16/output192 reservation')
 owning=[BASE/n for n in('ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json','PLAN.json','SOURCE_REVIEW_READY.json')]
 need(all(q.stat().st_size<8*2**20 for q in owning)and sum(q.stat().st_size for q in owning)<16*2**20 and owning[0].stat().st_size<65536,'actual metadata individual8/total16/proof64KiB bounds')
 need(ready['scientific_extraction_documents_current7_only_pins']==plan['scientific_extraction_documents_current7_only_pins'],'same report-science exceptions')
 need(plan['expected_nuclides']==17 and plan['expected_channel_pairs']==21 and plan['expected_channel_temperature_records']==131 and plan['expected_selected_sections']==262 and plan['original_decompressed_payload_expected_bytes']==92876787 and plan['retained_P0_dense_matrix_payload_bytes']==143471200 and plan['expected_selected_MF3_LIST_records']==768 and plan['expected_selected_MF6_LIST_records']==576 and plan['selected_raw_P0_LIST_numeric_upper_bound_bytes']==1721856,'exact original17/21/131/262 and P0 retained payload bounds')
 rows=plan['selected_inputs'];science=[p['current_original_input_full_pin']for p in plan['inputs']]
 need(len(rows)==17 and {s['input']['nuclide']:s['selected_MTs']for s in rows}==MTS and [s['input']for s in rows]==plan['inputs'],'exact canonical selected channel inputs')
 total=fullcount=mf3=mf6=0
 for s in rows:
  parts=s['selected_compact_metadata_sections'];count=s['all_compact_metadata_section_count'];digest=s['all_compact_metadata_ordered_canonical_sha256'];indices=[v['section_index_one_based']for v in parts]
  need('all_compact_metadata_sections'not in s and s['all_compact_metadata_canonical_columns']==list(COLUMNS)and type(count)is int and count>0 and len(digest)==64 and all(c in '0123456789abcdef'for c in digest)and indices==sorted(set(indices))and all(1<=i<=count for i in indices),'selected original indices and complete ordered digest/count, no full unselected arrays')
  nt=len(s['input']['original_source_deck_temperatures_K']);need(len(parts)==2*nt*len(s['selected_MTs']),'complete selected same nativeT cohort rows')
  for v in parts:
   rowbytes(v);need(v['mat']==s['input']['mat']and v['mf']in(3,6)and v['mt']in s['selected_MTs']and v['energy_groups']==370 and v['nz']==1 and v['nl']==(1 if v['mf']==3 or s['input']['SCI_role']=='SCI2'else 2),'actual selected original NL/NZ/header dimensions')
   if v['mf']==3:mf3+=v['LIST_records']
   else:mf6+=v['LIST_records']
  total+=len(parts);fullcount+=count
 need(total==262 and fullcount==10591 and mf3==768 and mf6==576,'complete selected rows and17 inventory count metadata')
 for p in science:current(p)
 need(sum(s['input']['original_ASCII_expected_size_bytes']for s in rows)==92876787,'original selected full input byte scope')
 actual=read(plan['prior_remaining_Cr52_Fe56_actual0_pin']);post=read(plan['prior_remaining_Cr52_Fe56_post0_pin']);posttools=read(plan['prior_remaining_Cr52_Fe56_post_tools0_pin'])
 hostpin=strict(terminal(actual,'actual_terminal_return',0)['output'].strip().splitlines()[-1])['report_pin']
 closed(posttools,'actual_review_return',plan['prior_remaining_Cr52_Fe56_post0_pin'],'review_pin')
 need(post['schema']=='INDEPENDENT_REMAINING_CR52_FE56_ACTUAL_RECORDED_COMPARISON_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_REMAINING_CR52_FE56_FINITE9_RECORDED_COMPARISON_METADATA_ONLY'and post['failure']is None and post['actual_Root_original_integer_exit_code']==0 and post['actual_Host_report_pin']==hostpin and post['actual_Root_tools_pin']==plan['prior_remaining_Cr52_Fe56_actual0_pin']and post['reported_P0_leaf_records']==378 and post['reported_raw_word_mismatches']==0,'actual prior producer/post0 evidence preserved')
 oldauthor=read(plan['prior_v1_author_freeze_pin']);oldfailure=read(plan['prior_v1_failed_Sourcegen_true_tools_pin']);oldproof=read(plan['prior_v1_partial_Source_proof_pin']);builder=read(plan['prior_v1_Root_argv_builder_field_failure_true_tools_pin'])
 t=terminal(oldfailure,'actual_Source_preparation_return',1)
 need(t['chunk_id']=='73061c'and t['output'].splitlines()[-1]=='RuntimeError: new Source metadata8MiB each'and oldfailure['business_started']is False and oldfailure['Source_preparation_retried']is False and plan['prior_v1_partial_Source_proof_pin']['size_bytes']==7168,'genuine v1 size failure1 and partial proof, no reinterpretation')
 need(builder['actual_return']['chunk_id']=='cb9e7c'and type(builder['actual_return']['exit_code'])is int and builder['actual_return']['exit_code']==1 and type(builder['original_integer_exit_code'])is int and builder['original_integer_exit_code']==1 and builder['Source_preparation_executed']is False and builder['business_executed']is False and builder['actual_return']['output'].splitlines()[-1]=="KeyError: 'Source_preparation_exact_argv'",'genuine first argv-builder1 preserved')
 for p in oldauthor['whole_Source_file_pins']:eof(p)
 need(not any(os.path.lexists(PREVIOUS/n)for n in absent+('PLAN.json','SOURCE_REVIEW_READY.json')),'v1 no PLAN/READY/publication/claim, pending output never claimed')
 worker=(BASE/'capture_extra21_original_ascii_event_production.py').read_bytes();oldworker=(PREVIOUS/'capture_extra21_original_ascii_event_production.py').read_bytes();host=(BASE/'run_guarded_extra21_original_ascii_event_production.py').read_bytes();pub=(BASE/'write_once_Root_extra21_reaction_capture_SF_HF_CLI.py').read_bytes();prep=(BASE/'prepare_extra21_reaction_capture_Source.py').read_bytes()
 names=('require','identity','current','metadata','pin','write','module','Budget','retained_channel','main')
 need(author['whole_v1_scientific_worker_function_Source_unchanged']==list(names)and all(function_or_class(worker,n)==function_or_class(oldworker,n)for n in names),'whole ten v1 numerical/setup/guard functions unchanged')
 source_inverse(oldworker,worker)
 for name in('run_guarded_extra21_original_ascii_event_production.py','write_once_Root_extra21_reaction_capture_SF_HF_CLI.py','original_check_mt51_repair.py','original_four_ascii_stream_helpers.py','original_dragr.f90','original_guard_host.py','original_once_publisher.py'):
  need((BASE/name).read_bytes()==(PREVIOUS/name).read_bytes(),'whole v1 host/publisher/five helpers')
 for item in proof['whole_original_source_copies']:
  p=item['original_Source_pin'];q=item['whole_unchanged_copy_full_pin'];eof(p);eof(q);need(Path(p['path']).read_bytes()==Path(q['path']).read_bytes(),'whole authoritative original helper copy')
 need(len(proof['whole_original_source_copies'])==5,'exact original five helper copies')
 need(definition(worker,'canonical_compact_record_bytes')==definition(prep,'canonical_compact_record_bytes'),'same whole canonical serializer prep/worker')
 wt=worker.decode();ht=host.decode();pt=pub.decode();st=prep.decode()
 for token in("matrix,flux=scalar.matrix(section)","active['event'][370-ig]=p0[1]","for outgoing in range(370):total+=float(p0[ig,outgoing])","reconstructed_delta=production-mf3['event']","union=(a!=0)|(b!=0)","mf3_only=(a!=0)&(b==0)","mf6_only=(a==0)&(b!=0)","payload[::active['nl']*active['nz']]","full_inventory_digest.update(canonical_compact_record_bytes(observed))","full_inventory_digest.hexdigest()==selected['all_compact_metadata_ordered_canonical_sha256']","observed==e","raw_original_matrix_before_Mo_ipflag1_diagonal_lumping=True","own_flux_division_performed=False"):
  need(token in wt,'original matrix/P0/FVECT/left-fold/masks/normalization/digest Source')
 need(wt.index('now-self.started<600 and peak<512*2**20')<wt.index('if now-self.last<0.25:return')and wt.count('self.started=time.monotonic()')==1 and 'self.last=time.monotonic()'in wt,'original every-callback SELF/wall and full-scan timestamp')
 need(ht.index("claim.open('x')")<ht.index("sf,psf=argument('source-freeze')")<ht.index("source_module(plan['original_Common_Source_pin']"),'exclusive claim before metadata/fullEOF/import/business')
 for token in ('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)',"runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources)","runner.execute(stage,'extra21_original_ASCII_131T_event_production_capture',cmd,600)","len(runner.records)==1",'sys.getprofile()is None','peak<512*2**20 and time.monotonic()-start<1800',"own_bytes<plan['bounded_new_output_reservation_bytes']"):
  need(token in ht,'original guarded one-child/caps/whole output bound')
 for token in("for role in('peer-review','peer-tools','generation','retirement')","tools['actual_review_return']","generation['actual_Source_preparation_return']","selected=ready['selected_Source_pins']+[pready,pg]","exec_command_sandbox_permissions='require_escalated'"):
  need(token in pt,'publisher exact PF/genuine0/permission contract')
 need('runner.execute'not in pt and 'len(raw)<8*2**20'in st and 'sum(p.stat().st_size for p in own if p.exists())+len(raw)<16*2**20'in st,'once publication only and original bounded Source serialization')
 need(ready['Root_actual_exec_command_sandbox_permissions_required']==plan['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and len(ready['original_complete_ENV_Python_B_prefix'])==11,'unchanged original process guard permission and ENV/Python/-B prefix')
 size=read(author['prospective_Source_metadata_size_facts_pin']);size_tools=read(author['prospective_Source_metadata_shape_original_true_tools_pin'])
 need(size['prospective_combined_upper_bound_bytes']==2210793 and size['selected_exact_rows']==262 and size['full_inventory_rows_bound_by_count_and_digest']==10591 and size['Source_preparer_imported_or_invoked']is False and size['Source_preparation_executed']is False and size['business_executed']is False and size['hypothetical_future_PF_identity_20_digits_is_size_envelope_not_actual_PF']is True,'bounded Source-only size facts, hypothetical PF not scientific admission')
 retirement=read(plan['actual_precise_retirement_receipt_pin']);need(retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==4,'original completed literal4 retirement retained')
 for p in retirement['actual_released_pins']:need(not os.path.lexists(p['path']),'literal4 paths remain absent')
 for p in selected:
  if p['path']in EXCEPTIONS:current(p)
  else:eof(p)
 for p in inherited+science:current(p)
 for p in list(HASHED.values()):eof(p)
 need(not os.path.lexists(OUT),'unexecuted output still absent')
 report=dict(schema='INDEPENDENT_EXTRA21_V2_FROZEN_SOURCE_METADATA_REVIEW_V1',status='PASS_SOURCE_METADATA_SCOPE_WITH_SCIENTIFIC_DOCUMENT_CURRENT7_ONLY',failure=None,source_only=True,metadata_only=True,reviewer_source_freeze_pin=fp,reviewer_source_pin=freeze['reviewer_source_pin'],Source_ready_pin=freeze['ready_pin'],canonical_generation_tools_pin=freeze['canonical_generation_tools_pin'],control_plan_pin=ready['control_plan_pin'],selected_Source_pins=selected,selected_pin_count=len(selected),fullEOF_Source_metadata_pins_verified_twice=list(HASHED.values()),scientific_document_exception_pins_current7_twice=exceptions,scientific_document_exception_count=12,inherited_metadata_current7_only_pins_verified_twice=inherited,original_scientific_input_current7_only_pins_verified_twice=science,all_selected_new_fullEOF_claimed=False,scientific_document_bodies_opened_or_hashed=False,old_SCI_GENDF_SQL_pool_XSM_bodies_opened_hashed_or_decoded=False,candidate_or_helpers_imported=False,original_Source_generation_integer_exit_code=0,Source_preparation_executed_by_peer=False,Source_publication_executed_by_peer=False,Source_preparation_reexecuted=False,whole_v1_ten_worker_functions_unchanged=True,whole_worker_metadata_inverse_restores_v1=True,whole_v1_host_publisher_five_helpers_unchanged=True,canonical13field_all10591_inventory_order_count_digest_preserved=True,selected262_original_section_indices_bound=True,numerical_arithmetic_R4_semantics_P0_selection_and_loop_order_unchanged=True,FVECT_flux_first_event_second_preserved=True,own_flux_division_performed=False,second_formatter_quantization_performed=False,full370_reconstructed_signed_diagnostics_and_distinct_observed_masks_retained=True,raw_original_Mo_matrix_before_ipflag1_lump_retained=True,prior_v1_Sourcegen1_and_builder1_preserved=True,prior_v1_no_PLAN_READY_pub_claim_or_business_output_preserved=True,prior_Cr52_Fe56_actual0_post0_preserved=True,complete_joint_roots=roots,original_caps=CAPS,Source_generation_metadata_bound_bytes=16*2**20,new_output_hard_bound_bytes=192*2**20,expected_nuclides=17,expected_channel_pairs=21,expected_channel_temperature_records=131,expected_selected_MF3_MF6_sections=262,expected_selected_MF3_LIST_records=768,expected_selected_MF6_LIST_records=576,required_future_Root_exec_command_sandbox_permissions='require_escalated',future_process_permission_access_proved=False,planned_actual_output_root=str(OUT),planned_actual_output_root_absent=True,actual_future_execution_success_claimed=False,runtime_or_SELF_RSS_fit_proved=False,original_guard_Runner_clock_profiler_caps_preserved=True,sciencebody_imported_or_executed=False,native_engines_started_by_peer=0,native_executed=False,scientific_payload_read=False,SCI_payload_read=False,gzip_payload_read=False,original_ASCII_payload_read=False,matrix_math_recomputed_by_peer=False,auditor_elapsed_seconds=time.monotonic()-START,**FALSE)
 target=HERE/'REVIEW.json';need(not os.path.lexists(target),'fresh review output only')
 with target.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 limits();print(json.dumps(dict(status=report['status'],review_pin=own_pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

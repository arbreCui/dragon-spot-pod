"""Source-only prospective JSON shape; never invokes/imports Source preparer.

Only the two known metadata-constructor ASTs are evaluated with metadata and
hypothetical future PF envelopes. No admission, science or runtime occurs.
"""
import ast,hashlib,json,os,pathlib,stat
R=pathlib.Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';BASE=pathlib.Path(__file__).absolute().parent;PREVIOUS=BASE.parent/'current_extra_reaction_source_v1';PRIOR=REC/'current_eight_fuel_finite18_SCAT_producer_source_v1_20261015/remaining_Cr52_Fe56_source_v2';ALL34=REC/'current_all34_original_ASCII_infinite_SCAT_producer_source_v1_20261015/v2';ART=R/'validation/artifacts'
OUT=ART/'axial-material-current-extra21-reaction-event-production-capture-20261015-v1'
NAMES=('capture_extra21_original_ascii_event_production.py','run_guarded_extra21_original_ascii_event_production.py','write_once_Root_extra21_reaction_capture_SF_HF_CLI.py','prepare_extra21_reaction_capture_Source.py','original_check_mt51_repair.py','original_four_ascii_stream_helpers.py','original_dragr.f90','original_guard_host.py','original_once_publisher.py')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
 q=pathlib.Path(q);s=q.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
 return dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s))
def future(q):return dict(path=str(q),sha256='f'*64,size_bytes=8*2**20,identity=[99999999999999999999]*4+[8*2**20]+[99999999999999999999]*2)
def unique(rows):
 out={}
 for p in rows:
  if p['path']in out:assert out[p['path']]==p
  out[p['path']]=p
 return list(out.values())
def size(v):return len((json.dumps(v,indent=2,allow_nan=False)+'\n').encode())
def main():
 prior=json.load(open(PRIOR/'PLAN.json'));priorready=json.load(open(PRIOR/'SOURCE_REVIEW_READY.json'));post=json.load(open(PRIOR/'actual_postverify_20261015/REVIEW.json'));allplan=json.load(open(ALL34/'PLAN.json'));cli=json.load(open(PRIOR/'FINAL_ROOT_REVIEWABLE_CLI.json'))
 q=ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json';v=json.load(open(q));pallactual=next(p for p in priorready['dependencies']if p['path']==str(q))
 columns=('section_index_one_based','mat','mf','mt','nl','nz','energy_groups','temperature_K','section_header_sha256','LIST_records','LIST_dimension_sequence_sha256','incident_present_mask_hex','spectrum_LIST_present')
 mts={'Cr50':[44],'Cr53':[32],'Ni58':[22],'Ni60':[22],'Ni61':[22,32],'Ni62':[22],'Ni64':[22],'O16':[22,23],'Si28':[22],'Ti48':[22],'Mo92':[22],'Mo94':[22],'Mo95':[22,24,41],'Mo96':[22],'Mo97':[22],'Mo98':[22],'Mo100':[22]};selected=[];pairs=[];fullrows=0
 for row in allplan['inputs']:
  if row['nuclide']not in mts:continue
  orig=next(x for x in v['actual_extractions']if x['nuclide']==row['nuclide']);ledger=orig['actual_MF3_MF6_compact_inventory'];digest=hashlib.sha256();fullrows+=len(ledger)
  for record in ledger:
   assert set(record)==set(columns);digest.update((json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii'))
  selected.append(dict(input=row,selected_MTs=mts[row['nuclide']],selected_compact_metadata_sections=[r for r in ledger if r['mf']in(3,6)and r['mt']in mts[row['nuclide']]],all_compact_metadata_section_count=len(ledger),all_compact_metadata_ordered_canonical_sha256=digest.hexdigest(),all_compact_metadata_canonical_columns=list(columns)))
  for mt in mts[row['nuclide']]:
   a=[r for r in ledger if r['mf']==3 and r['mt']==mt];b=[r for r in ledger if r['mf']==6 and r['mt']==mt];pairs.append(dict(nuclide=row['nuclide'],MT=mt,SCI_role=row['SCI_role'],native_temperature_sections=len(a),actual_native_temperatures_K=[r['temperature_K']for r in a],MF3_nl=1,MF6_nl=b[0]['nl'],actual_nz=1,MT5_in_both_MF3_MF6=any(r['mf']==3 and r['mt']==5 for r in ledger)and any(r['mf']==6 and r['mt']==5 for r in ledger),MT5_partition_qualified=False))
 poldauthor=pin(PREVIOUS/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');pbuilderFailure=pin(PREVIOUS/'ROOT_FIRST_GENERATION_ARGV_FIELD_FAILURE_TRUE_TOOL_RETURN.json');pfailed=pin(PREVIOUS/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json');poldproof=pin(PREVIOUS/'ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json');pp=pin(PRIOR/'PLAN.json');pr=pin(PRIOR/'SOURCE_REVIEW_READY.json');pactual=pin(PRIOR/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');ppost=pin(PRIOR/'actual_postverify_20261015/REVIEW.json');pptools=pin(PRIOR/'actual_postverify_20261015/TRUE_TOOL_RETURNS.json');pallplan=pin(ALL34/'PLAN.json');pa=future(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');pproof=future(BASE/'ORIGINAL_PARSER_MATRIX_AND_GUARD_SOURCE_PROOF.json');scientificDocs=unique(post['eleven_scientific_extraction_document_pins']+[pallactual]);metadata=unique(priorready['dependencies']+[poldauthor,pbuilderFailure,pfailed,poldproof,pp,pr,pactual,ppost,pptools,pallplan,pallactual,pa,pproof,pin(BASE/'EXTRA_REACTION_SOURCE_SCOPE_DRAFT.json')]);sources=[pin(BASE/n)for n in NAMES]+[pproof];inherited=unique(prior['explicit_cumulative_metadata_file_pins']);explicit=unique(inherited+metadata+sources);roots=prior['complete_joint_roots']+[str(OUT)];before=99999999999999999999;CAPS=prior['original_caps']
 tree=ast.parse((BASE/'prepare_extra21_reaction_capture_Source.py').read_text());mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');planCall=next(n for n in ast.walk(mainnode)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='plan'and n.func.attr=='update');readyCall=next(n.value for n in ast.walk(mainnode)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ready'for t in n.targets));falseNode=next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FALSE'for t in n.targets));FALSE=eval(compile(ast.Expression(falseNode),'<literal Source false metadata flags>','eval'),{'dict':dict},{})
 context=dict(globals());context.update(locals());plan=dict(prior)
 for kw in planCall.keywords:
  if kw.arg is None:plan.update(context[kw.value.id])
  else:plan[kw.arg]=eval(compile(ast.Expression(kw.value),'<prospective metadata constructor keyword only>','eval'),{'__builtins__':{},'str':str},context)
 pplan=future(BASE/'PLAN.json');dependencies=unique(metadata+sources+[pplan]);context.update(plan=plan,pplan=pplan,dependencies=dependencies);ready=eval(compile(ast.Expression(readyCall),'<prospective READY metadata constructor only>','eval'),{'__builtins__':{},'dict':dict},context)
 planBytes=size(plan);readyBytes=size(ready);proofUpper=64*2**10;lateSlack=64*2**10;assert planBytes+lateSlack<8*2**20 and readyBytes+lateSlack<8*2**20 and planBytes+readyBytes+proofUpper+2*lateSlack<16*2**20
 value=dict(schema='AUTHOR_SOURCE_ONLY_PROSPECTIVE_COMPACT_METADATA_SIZE_FACTS_V2',Source_preparer_imported_or_invoked=False,Source_preparation_executed=False,Source_publication_executed=False,business_executed=False,old_scientific_bodies_hashed_or_decoded=False,only_declared_compact_inventory_metadata_fields_read=True,prospective_constructor_AST_only_evaluated_without_gate_or_writer=True,prospective_plan_metadata_envelope_bytes=planBytes,prospective_READY_metadata_envelope_bytes=readyBytes,proof_metadata_static_upper_bound_bytes=proofUpper,late_author_metadata_PF_slack_each_bytes=lateSlack,per_file_original_cap_bytes=8*2**20,three_file_total_original_cap_bytes=16*2**20,prospective_combined_upper_bound_bytes=planBytes+readyBytes+proofUpper+2*lateSlack,selected_exact_rows=262,full_inventory_rows_bound_by_count_and_digest=fullrows,serialized_full_ledger_row_arrays_removed=True,hypothetical_future_PF_identity_20_digits_is_size_envelope_not_actual_PF=True,old_Sourcegen1_preserved_not_retried=True,pending_OUT_v1_reused_without_business_claim=True)
 with open(BASE/'AUTHOR_PROSPECTIVE_COMPACT_METADATA_SIZE_FACTS.json','x')as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(value))
if __name__=='__main__':main()

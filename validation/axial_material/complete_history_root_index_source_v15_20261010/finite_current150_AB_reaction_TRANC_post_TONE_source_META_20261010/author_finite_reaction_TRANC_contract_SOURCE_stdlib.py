"""Finite Source/META evidence only; no import/run of reviewed sources or payload."""
import ast, hashlib, json, os, stat
from pathlib import Path
P=Path(__file__).resolve().parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
files=[
 ('already_fixed_reference_route_REPORT',B/'finite_current150_AB_reference_source_route_20261010/REPORT.txt'),
 ('current_scientific_gaps',B/'CURRENT_SCIENTIFIC_GAPS.txt'),
 ('already_fixed_source_phase_report',B/'next_saved_source_phase_consistency_source_only_review/REPORT.txt'),
 ('already_fixed_reaction_multiplicity_Source',B/'next_saved_source_phase_consistency_source_only_review/reaction_SOURCE_evidence.json'),
 ('existing_actual_reaction_META_review',B/'independent_actual_saved_reaction_diagnostic_review/REPORT.txt'),
 ('existing_native_layout_META_review',B/'actual_full_AB_rawrecord_transfer_v22_admitted_receipts/sealed_finite_native_FISSIONINDEX_layout_SOURCE_META_review/REVIEW.json'),
 ('material_results_smallMETA',Path('/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003/material_results.json')),
 ('case_spec',Path('/Users/wen/spot/validation/axial_material/case_spec.json')),
 ('material_inputs_Source',Path('/Users/wen/spot/validation/axial_material/material_inputs.py')),
]
for name in('LIB.f','LIBLIC.f','LIBADD.f','LIBDRB.f','LIBDEN.f','LIBMIX.f','LIBIPS.f','TONE.f','TONDRV.f','TONSPH.f','TONCMI.f','ASM.f','ASMDRV.f','SPOASM.f','MGXEXP.f90'):
 files.append((name,Path('/Users/wen/spot/src')/name))
checks=[]
def check(n,v):
 if type(v)is not bool or not v:raise ValueError(n)
 checks.append(dict(check=n,passed=True))
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def readpin(p):
 s=p.lstat();check('regular finite Source/META '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<2**20)
 with p.open('rb')as f:
  check('Source/META open7ID '+str(p),ident(os.fstat(f.fileno()))==ident(s))
  raw=f.read();check('Source/META EOF7ID '+str(p),len(raw)==s.st_size and ident(os.fstat(f.fileno()))==ident(s))
 check('Source/META path7ID '+str(p),ident(p.lstat())==ident(s))
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s)),raw
sources={};pins=[]
D=P/'FINITE_SOURCE_META_COPIES';D.mkdir()
for ordinal,(role,p)in enumerate(files):
 pin,raw=readpin(p);sources[role]=raw.decode('utf-8');dest=D/(str(ordinal).zfill(2)+'_'+p.name)
 with dest.open('xb')as f:f.write(raw)
 pins.append(dict(role=role,original_fullpin=pin,full_copy_path=str(dest)))
 if p.suffix=='.py':check('whole Source AST '+role,isinstance(ast.parse(raw,filename=str(p)),ast.Module))
case=json.loads(sources['case_spec']);mat=json.loads(sources['material_results_smallMETA']);oldreact=json.loads(sources['already_fixed_reaction_multiplicity_Source']);layout=json.loads(sources['existing_native_layout_META_review'])
check('scope two original3708_32 material states',list(mat['states'])==['A','B']and all(x['groups']==370 and x['regions']==8 and x['fission_components']==32 for x in mat['states'].values()))
check('saved actual material scope explicitly not physical',mat['physical_accuracy_accepted']is False and mat['retained_material_limit']=='Native TONE masked criterion; SPH boundary factor not saved, not independently replayed')
check('original12reaction channels remain unqualified',len(oldreact['channels'])==12 and all(c['actual_allgroup_multiplicity_qualified']is False for c in oldreact['channels']))
check('top microlib finite observed 62isotope_3moments_APOL',all(row['observed']['STATE-VECTOR']['values'][:5]==[8,62,370,3,1]and row['observed']['STATE-VECTOR']['values'][12]==18 for row in layout['actual_top_microlib_metadata']))
contracts={
 'initial_material_declares_APOL_3moments':('material_inputs_Source',"EDIT 0 NMIX 8 CTRA APOL ANIS 3"),
 'TONE_material_TRAN_PIJ_no_NOSP':('material_inputs_Source',"EDIT 1 MXIT 20 EPS 1.0E-5 TRAN PIJ"),
 'APOL_sets_type1':('LIB.f',"ELSE IF(CARLIR(1:4) .EQ. 'APOL') THEN"),
 'TONE_defaults_SPH1':('TONE.f','KSPH=1'),
 'PIJ_sets_phase2_not_SPH_off':('TONE.f',"ELSE IF(TEXT4.EQ.'PIJ') THEN"),
 'actual_SPH_branch_uses_NBNRS_guard':('TONDRV.f','IF(NBNRS.GT.1) THEN'),
 'TONE_POST_SPH_LIBMIX':('TONDRV.f','CALL LIBMIX(IPLIB,NBMIX,NGRO,NBISO,ISONAM,MIX,DEN,MASK,MASKL,'),
 'TONSPH_calls_true_MICRO_correction':('TONSPH.f','CALL TONCMI(IPLIB,IMPX,NBM,NBISO,NGRO,NL,NED,NDEL,MASKI,SPH)'),
 'TRANC_divided_by_SPH':('TONCMI.f',"(HMAKE(J).EQ.'TRANC')) THEN"),
 'raw_named_edits_real_same_scope':('TONCMI.f',"IF((LENGTH.GT.0).AND.(TEXT8.NE.'TRANC')) THEN"),
 'NTOT_unchanged_SPH':('TONCMI.f',"ELSE IF(HMAKE(J)(:4).EQ.'NTOT') THEN"),
 'evenmoment_source_scaling':('TONCMI.f','WSCAT(IG1,IG2,IL)=WSCAT(IG1,IG2,IL)*SPH(IBM,IG2)'),
 'oddmoment_destination_scaling':('TONCMI.f','WSCAT(IG1,IG2,IL)=WSCAT(IG1,IG2,IL)/SPH(IBM,IG1)'),
 'P0_SIGS_independent_vector_update':('TONCMI.f','GAR(IG2,2+IL)=GAR(IG2,2+IL)*SPH(IBM,IG2)+GAR(IG2,3+NL)*'),
 'other_SIGS_column_sum_update':('TONCMI.f','GAR(IG2,2+IL)=REAL(DSUM)'),
 'initial_TRANC_contains_total_difference':('LIBADD.f','WORK(IG1)=WR2(IG1)-WORK(IG1)'),
 'initial_APOL_P1_input':('LIBADD.f','CALL XDRLGS(KPLIB,-1,0,1,1,1,NGRO,WR2,SCAT,ITY)'),
 'initial_TRANC_transport_and_leakage_explicit':('LIBADD.f',"***CAUTION*** 'TRANC' CONTAINS BOTH TRANSPORT AND LEAKAGE"),
 'final_TRANC_density_aggregate':('LIBDEN.f','GAF(IBM,LLL,11)=GAF(IBM,LLL,11)+GA1(LLL)*DENISO'),
 'final_TRANC_saved_REAL32':('LIBDEN.f',"CALL LCMPUT(KPLIB,'TRANC',NBMIX,2,GAF(1,LLL,11))"),
 'final_macroflag_record2':('LIBDEN.f','IF(ITRANC.NE.0) IDATA(6)=2'),
 'final_extra_vector_density_aggregate':('LIBDEN.f','GAF(IBM,LLL,1)=GAF(IBM,LLL,1)+GA1(LLL)*DENISO'),
 'full_source_SPARSE_SCAT_density_aggregate':('LIBDEN.f','GAF(IBM,IG1,IBLK)=GAF(IBM,IG1,IBLK)+GA2(IOF)*DEN(ISOT)*FACT'),
 'SIGS_separate_not_forced_columnsum':('LIBDEN.f',"CALL LCMPUT(KPLIB,'SIGS'//CM,NBMIX,2,GAR(1,IBLK))"),
 'full_scatter_macro_self':('LIBDEN.f',"CALL LCMPUT(KPLIB,'SIGW'//CM,NBMIX,2,GAR(1,1))"),
 'raw_ISO_order_alias_actual_directory':('LIBMIX.f','CALL LIBIPS(IPLIB,NBISO,IPISO)'),
 'ASM_common_P0_total_self_TRANC':('ASMDRV.f','XSSIGT(IMAT,IGR,1)=XSSIGT(IMAT,IGR,1)-XSSCOR(IMAT,IGR)'),
 'ASM_common_P0_self_TRANC':('ASMDRV.f','XSSIGW(IMAT,1,IGR)=XSSIGW(IMAT,1,IGR)-XSSCOR(IMAT,IGR)'),
 'ASM_explicit_anisotropy_disables_TRANC':('ASM.f','IF((ITRANC.NE.0).AND.(NANI.GT.1).AND.(ISTRM.EQ.1)) THEN'),
 'SPOT_explicit_3moment_axial_raw_total':('SPOASM.f',"CALL LCMGET(KPMACAX,'NTOT0',TXSC(1,IGR))"),
 'SPOT_RADIAL_uses_saved_corrected_operators':('SPOASM.f',"CALL LCMGET(MPSNAP,'DRAGON-TXSC',TXSC2D)"),
 'MGXEXP_synthetic_absorption_is_present_not_true_event_contract':('MGXEXP.f90','absorption(igr)=absorption(igr)+excess_multiplicity(igr)'),
}
source_evidence=[]
for label,(role,fragment)in contracts.items():
 text=sources[role];check(label,fragment in text)
 lines=text.splitlines();hits=[i+1 for i,line in enumerate(lines)if fragment in line]
 source_evidence.append(dict(fact=label,source_role=role,exact_matching_line_numbers=hits,matching_lines=[lines[i-1]for i in hits]))
# The algebraic implication is reasoned from the full Source, not counted as an actual numerical or payload check.
for item in pins:
 actual,_=readpin(Path(item['original_fullpin']['path']));check('complete finite originals unchanged '+item['role'],actual==item['original_fullpin'])
(P/'FULL_SOURCE_AND_META_PROVENANCE.json').write_text(json.dumps(dict(schema='FINITE_CURRENT_AB_POST_TONE_REACTION_TRANC_SOURCE_META_PROVENANCE_V1',source_only=True,pins=pins,no_material_native_ASCII_GNDF_ENDF_binary_payload_read=True),indent=2)+'\n')
(P/'SOURCE_LINE_FACTS.json').write_text(json.dumps(dict(source_only=True,facts=source_evidence),indent=2)+'\n')
report=dict(schema='FINITE_CURRENT150_AB_POST_TONE_REACTION_TRANC_SOURCE_CONTRACT_V1',source_only=True,status='SOURCE_AND_EXISTING_SMALL_META_ONLY_NEW_PROCESSING_CONTRACT_NO_SCIENCE',original_scope=dict(states=['A','B'],groups=370,radial_regions=8,raw_legendre_moments=3,fission_components=32,full_macro_records_per_state=19619,microlib_isotope_slots=62,full_declared_extra_vector_edits=18,height_cm=150),all_checks_passed=True,checks=checks,check_count=len(checks),new_determined_Source_facts=[
 'Current deck asks APOL3/TONE TRAN PIJ; PIJ sets IPHASE2 and does not disable default KSPH1. Actual NBNRS/SPH branch and h not established here.',
 'Initial LIBADD APOL TRANC is total-leakage difference plus raw first Legendre production transfer. It is not absorption.',
 'If actual TONCMI executes: TRANC->TRANC/h; named event vectors/NUSIGF->h*value; NTOT0/NTOT1 unchanged; P0/P2 production column->h scaling plus NTOT0*(1-h) self term; P1 destination->1/h scaling plus NTOT1*(1-1/h) self term.',
 'Formal evenmoment net total-minus-transfer becomes h times its prior net value, before finite REAL32 rounding. This does not identify true absorption or certify actual branch.',
 'Final LIBDEN aggregates stored TRANC directly by true isotope density/alias/order and writes macro flag2. It need not regenerate TRANC from the final P1 columnsum.',
 'SIGS00 is a separately stored/updated vector; SIGW00 is sparse diagonal. Even corrected Source does not authorize forcing SIGS to the expanded column sum.',
 'Explicit anisotropic axial SPOT uses raw NTOT0/SIGW moments; radial closure keeps separately corrected native operator. Common P0 correction cancellation is only algebra, not full physical balance.',
 ],existing_META_limits=dict(material_SPH_factors_saved=False,material_SPH_independently_replayed=False,current_SOURCE_equals_original_actual_binary_compilation_proved=False,current_library_ALL_MF3_MF6_processed_multiplicity_proved=False),
 next_single_actual_verifiable_contract='After full native saved-byte evidence, Root-only bounded read/replay of each A then B final62-isotope microlib into all370x8 macro TRANC/NTOT0/NTOT1/all18 declared extra edits, all3 sparse transfer moments/SIGW/SIGS, and all32 fission components using true alias/mix/density/NESP/FISSIONINDEX/TIMESPER/flags; retain complete original records, missing None, order and REAL32 operation deltas. No new transport or synthesis ABSORPTION.',
 future_actual_input_pins=None,future_actual_checker_host_or_tool=None,actual_payload_read=False,actual_numerical_replay=False,actual_transport_launched=False,original_XSM_memory_bits_verified=False,reaction_multiplicity_verified=False,TRANC_semantics_actual_qualified=False,full_physical_neutron_balance_qualified=False,same_MG_unreduced_reference_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_accuracy_qualified=False,
 caps_unchanged=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0))
(P/'SOURCE_META_CONTRACT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,package=str(P),complete_finite_Source_META_inputs=len(pins),checks=report['check_count'],new_fact='post-TONE/SPH TRANC/event/transfer are differently transformed; finalmicro-to-macro contract is next actual check',no_candidate_API_guard_native_or_material_payload_execution=True),indent=2),flush=True)

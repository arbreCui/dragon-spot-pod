"""Bounded Source/META review. Never import reviewed APIs or read material payloads."""
import ast, hashlib, json, re, stat, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE_ROOT=Path('/Users/wen/dragon-5.1')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-current150-AB-full-rawrecord-transfer-v22-20261010')
SPEC=[
 ('LIBDEN.f',SOURCE_ROOT/'Dragon/src/LIBDEN.f',[(22,40),(99,129),(170,235),(666,705),(748,772),(835,916),(971,1013),(1062,1070)]),
 ('LIBMIX.f',SOURCE_ROOT/'Dragon/src/LIBMIX.f',[(64,75),(107,130)]),
 ('LIBNFI.f',SOURCE_ROOT/'Dragon/src/LIBNFI.f',[(24,33),(64,115),(170,190)]),
 ('TONDRV.f',SOURCE_ROOT/'Dragon/src/TONDRV.f',[(332,351)]),
 ('MACUPD.f',SOURCE_ROOT/'Dragon/src/MACUPD.f',[(235,260)]),
 ('MACNFI.f',SOURCE_ROOT/'Dragon/src/MACNFI.f',[(1,55)]),
 ('MAC.f',SOURCE_ROOT/'Dragon/src/MAC.f',[(1,60)]),
 ('lcm_c.c',SOURCE_ROOT/'Ganlib/src/lcm_c.c',[(2661,2709),(2740,2763),(3014,3104),(3342,3414)]),
 ('LCMAUX.f90',SOURCE_ROOT/'Ganlib/src/LCMAUX.f90',[(428,500)]),
 ('SectDmacrolib.tex',SOURCE_ROOT/'doc/IGE351/SectDmacrolib.tex',[(30,43),(148,158),(255,276),(386,412)]),
 ('SectDmicrolib.tex',SOURCE_ROOT/'doc/IGE351/SectDmicrolib.tex',[(90,98),(207,227),(979,1000)]),
 ('material_inputs.py',Path('/Users/wen/spot/validation/axial_material/material_inputs.py'),[(121,162),(169,192)]),
 ('native_records.py',SOURCE_ROOT/'Dragon/irena_core/colorset_rebuild_20260527/ce_compare/fullpitch_pnl_s30_b0_closure_v1_20260907/native_records.py',[(1,81)]),
 ('stream_records.py',SOURCE_ROOT/'Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/finegroup_acceptance/stream_records.py',[(1,108)])]
META=[(O/'ACTUAL_TRANSFER_REPORT.json','30326213d05531f8ce9871b77fb5197de32269fa97f7da12277f071860209412'),(O/'A/small_state_metadata.json','7df6aa620bed55ddd341bb7ef15c762f9ffd72ec467f92d549e59c3d8ede5e0f'),(O/'B/small_state_metadata.json','0457a7aaad107164e4a470eecb2c3603985d81078dc1a29bffbf401686a82be1'),(O/'A/full_required_field_contract.jsonl','95c2df0d00e5003056b14bb60bb39f58aee04e1ab720c42346cbb2fd75b6ba0b'),(O/'B/full_required_field_contract.jsonl','95c2df0d00e5003056b14bb60bb39f58aee04e1ab720c42346cbb2fd75b6ba0b')]
def identity(p):
 s=p.stat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p)
 if not stat.S_ISREG(before[2]): raise ValueError('not regular: '+str(p))
 raw=p.read_bytes(); after=identity(p)
 if before != after or len(raw)!=before[4]: raise ValueError('changed while reading: '+str(p))
 return raw,{'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before,'full_EOF_read':True,'before_after_exact':True}
def write(name,data):
 (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
checks=[]
def require(v,name):
 if type(v) is not bool or not v: raise ValueError(name)
 checks.append({'name':name,'pass':True})
source_pins=[]; texts={}; segments=[]
(ROOT/'full_source_text').mkdir(exist_ok=True)
for name,path,ranges in SPEC:
 raw,p=pin(path); source_pins.append(p)
 (ROOT/'full_source_text'/name).write_bytes(raw)
 text=raw.decode(); texts[name]=text
 if name.endswith('.py'): ast.parse(text,filename=str(path))
 lines=text.splitlines()
 for a,b in ranges:
  require(1<=a<=b<=len(lines),'valid Source segment '+name+':'+str(a))
  segments.append({'path':str(path),'sha256':p['sha256'],'start':a,'end':b,'text':'\n'.join(lines[a-1:b])})
for name,fragment in [
 ('LIBDEN.f',"CALL LCMPUT(IPLIB,'FISSIONINDEX',NBMIX*NFISSI,1,INDFIS)"),
 ('LIBDEN.f','IDATA(4)=NFISSI*NESP'),
 ('LIBDEN.f','ILONG=NBMIX*NFISSI*NESP'),
 ('LIBDEN.f','INDFIS(IBM,KFIS)=ISOT'),
 ('LIBDEN.f','IOF=(KFIS-1)*NBMIX*NESP+(ISP-1)*NBMIX+IBM'),
 ('LIBDEN.f',"CALL LCMGET(IPLIB,'CHI-LIMITS',IESP)"),
 ('LIBDEN.f','DO 610 LLL=IESP(ISP)+1,IESP(ISP+1)'),
 ('LIBDEN.f',"TEXT12='CHI--'//TEXT2//' '//NORD(IXSPER)"),
 ('LIBMIX.f','NBESP=ISTATE(16)'),
 ('LIBMIX.f','NESP=NBESP'),
 ('LIBMIX.f','CALL LIBDEN (IPLIB,NGROUP,NBISO,NBMIX,NL,NDEL,NESP'),
 ('LIBNFI.f','NFISSI=IDATA(4)/NESP'),
 ('LIBNFI.f','ELSE IF(ILONG.EQ.NFISSI*NBMIX)'),
 ('TONDRV.f','CALL LIBMIX(IPLIB,NBMIX,NGRO,NBISO,ISONAM,MIX,DEN,MASK,MASKL'),
 ('MACUPD.f',"CALL LCMPUT(IPMACR,'FISSIONINDEX',NBMIXF*NIFISF,1,NUMFN)"),
 ('material_inputs.py','MACRO := MICROLIB2 :: STEP UP MACROLIB'),
 ('material_inputs.py','MICROLIB2 := TONE: MICROLIB TRACK_T TRACK_T_f'),
 ('material_inputs.py','MACRO_OUT := MACRO'),
 ('lcm_c.c','lcmlen_c(&iplist, namt, &jlong, &itylcm);'),
 ('lcm_c.c','lcmnod_c(file, imode, idir, jlong, itylcm, iass);'),
 ('lcm_c.c','%16.8E'),
 ('lcm_c.c','%20.12E'),
 ('native_records.py','def decode(raw):'),
 ('native_records.py','records[path] = (kind, value)'),
 ('stream_records.py','select=lambda path, kind, count: True'),
 ('stream_records.py','records[path] = (kind, value)'),
 ('SectDmacrolib.tex','pointing to a component of record'),
 ('SectDmicrolib.tex','\\mathcal{S}^{m}_{16}'),
 ('SectDmicrolib.tex','{CHI-LIMITS\\blank{2}}{$G_{\\rm chi}+1$}')]:
 require(fragment in texts[name],'original Source formula '+name+': '+fragment)
meta_pins=[]; meta_data={}
for path,expected in META:
 raw,p=pin(path); require(p['sha256']==expected,'exact allowed META SHA '+str(path));meta_pins.append(p)
 if path.suffix=='.json':meta_data[str(path)]=json.loads(raw)
 else:
  rows=[json.loads(line) for line in raw.splitlines() if line]
  require(len(rows)==8515,'all8515 metadata contract rows '+str(path))
  fi=[r for r in rows if r['path']==['FISSIONINDEX']]
  require(len(fi)==1,'one root FISSIONINDEX '+str(path))
  require(fi[0]['present'] is True and fi[0]['actual_kind']==1 and fi[0]['actual_count']==64 and fi[0]['expected_count']==256 and fi[0]['gap_reasons']==['unexpected_actual_count'],'unchanged honest FISSIONINDEX gap '+str(path))
  gap=[r for r in rows if r['gap_reasons']]
  require(gap==fi,'FISSIONINDEX sole original contract gap '+str(path))
  fs=[r for r in rows if len(r['path'])==3 and r['path'][0]=='GROUP' and isinstance(r['path'][2],str) and (r['path'][2].startswith('NUSIGF') or r['path'][2].startswith('CHI'))]
  names={r['path'][2] for r in fs}
  require({'NUSIGF','CHI'}.issubset(names),'base fission rows included '+str(path))
  require(all(r['present'] is True and r['actual_kind']==2 and r['actual_count']==256 and not r['gap_reasons'] for r in fs),'all base and delayed expanded fission records count256 '+str(path))
  require(all(sum(r['path'][2]==name for r in fs)==370 for name in names),'all370 groups for every saved fission field '+str(path))
  meta_data[str(path)]={'all_contract_rows':len(rows),'FISSIONINDEX':fi[0],'only_gap_rows':gap,'all_fission_field_names':sorted(names),'all_fission_field_count_rows':len(fs),'every_fission_field_all370_count256':True}
for state in ('A','B'):
 d=meta_data[str(O/state/'small_state_metadata.json')]
 inv=d['full_inventory']; sc=d['scientific_contract_inventory']; compare=d['independent_full_reader_comparison']
 require(inv['records']==19619 and inv['numeric_values']==2264113,'saved complete record counts '+state)
 require(sc['actual_STATE_VECTOR'][:7]==[370,8,3,32,18,2,6],'saved STATE_VECTOR first7 '+state)
 require(compare['all_paths_types_order_values_floatbits_equal'] is True and compare['all_stream_records_retained'] is True,'saved two default reader full equality '+state)
 for key in ('original_LCM_memory_bit_identity_directly_verified','true_physical_loss_reaction_multiplicity_verified','transport_correction_semantics_qualified','future_solver_scientific_input_admitted'):
  require(sc[key] is False,'saved scientific unresolved '+state+'/'+key)
 require(sc['no_fields_filled_clipped_normalized_or_inferred'] is True,'no synthetic field repair '+state)
top_metadata=[]
for state in ('A','B'):
 path=Path('/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003')/state/'metadata.ascii'
 raw,p=pin(path); meta_pins.append(p)
 lines=raw.decode('ascii').splitlines(); observed={}
 for name,count in [('STATE-VECTOR',40),('CHI-LIMITS',5)]:
  hits=[]
  for i,line in enumerate(lines):
   if line.strip()!=name or i<1:continue
   header=re.fullmatch(r'->\s+1\s+12\s+1\s+'+str(count)+r'\s+<-\s*',lines[i-1])
   if header is None:continue
   values=[]; j=i+1
   while len(values)<count:
    require(j<len(lines) and not lines[j].startswith('->'),'complete authorized top metadata integer row '+state+'/'+name)
    values.extend(int(v) for v in lines[j].split());j+=1
   require(len(values)==count,'exact authorized integer count '+state+'/'+name)
   hits.append({'name':name,'header_line':i,'name_line':i+1,'last_payload_line':j,'kind':1,'count':count,'values':values,'actual_root_level':1})
  require(len(hits)==1,'unique top metadata named integer field '+state+'/'+name)
  observed[name]=hits[0]
 require(observed['STATE-VECTOR']['values']==[8,62,370,3,1,0,1,2,24,281,0,0,18,8,2,4,0,1,6,0,0,300,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],'actual full current top microlib STATE_VECTOR '+state)
 require(observed['CHI-LIMITS']['values']==[0,21,40,61,370],'actual complete CHI_LIMITS4 partitions '+state)
 top_metadata.append({'state':state,'pin':p,'only_decoded_metadata_names':['STATE-VECTOR','CHI-LIMITS'],'observed':observed,'isotopelist_or_xs_payload_read':False})
write('ACTUAL_TOP_MICROLIB_STATE16_CHI_LIMITS_ONLY_META.json',top_metadata)
report=meta_data[str(O/'ACTUAL_TRANSFER_REPORT.json')]
for key in ('scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','coupled_370group_reference_qualified','native_transport_executed','whole_combined_build_or_INPUT_qualified'):
 require(report[key] is False,'saved report honest scope '+key)
for p in source_pins+meta_pins:
 _,after=pin(Path(p['path']));require(after==p,'all Source/META full EOF before_after unchanged '+p['path'])
write('SOURCE_SEGMENTS.json',segments)
write('SOURCE_INPUT_FULL_PINS.json',source_pins)
write('ALLOWED_SAVED_META_FULL_PINS_AND_COUNTS.json',{'pins':meta_pins,'limited_derived_contract_counts':{k:v for k,v in meta_data.items() if k.endswith('.jsonl')}})
review={
 'schema':'FINITE_FISSIONINDEX_NATIVE_PRODUCER_SOURCE_AND_SAVED_COUNT_REVIEW_V1',
 'status':'SOURCE_META_PASS_NATIVE_LAYOUT_EXPLAINED_NO_PHYSICAL_ADMISSION',
 'source_only':True,'allowed_saved_META_only':True,'reviewed_APIs_imported_or_called':False,'material_payload_read_or_decoded':False,'numeric_business_run':False,'project_or_saved_results_modified':False,
 'source_input_count':len(source_pins),'allowed_saved_META_count':len(meta_pins),'checks':checks,'all_source_META_before_after_full_EOF_unchanged':True,
 'native_producer_equations':{'NESP':'microlib STATE-VECTOR(16), except0→1','NFISSI':'max local fissionable isotope slots per mixture','FISSIONINDEX':'Fortran INDFIS(NBMIX,NFISSI), stored count NBMIX*NFISSI, kind1','index_value':'microlib isotope ordinal ISOT, not expanded spectrum component ordinal','Macrolib_STATE_VECTOR_4':'NFISSI*NESP unless LSAME collapses to<=1','group_NUSIGF_CHI_and_delayed_count':'NBMIX*NFISSI*NESP unless LSAME collapses to NBMIX','expanded_component_0based':'component=local_slot*NESP+spectrum','index_flat_0based':'index=local_slot*NBMIX+mixture','group_fission_flat_0based':'index=(local_slot*NESP+spectrum)*NBMIX+mixture'},
 'current_saved_count_inference':{'saved_macrolib_first7':[370,8,3,32,18,2,6],'saved_FISSIONINDEX_count':64,'conditional_NFISSI':8,'conditional_NESP':4,'all370_base_and_delayed_NUSIGF_CHI_count256_retained':True,'conditional_explanation':'Within the observed LIBMIX/LIBDEN multi-spectrum production layout,64=8mixtures×8local isotope slots;32=8slots×4spectra. No256-entry FISSIONINDEX is required by this producer. This is not a global32-component lookup table. The generic MACUPD NBMIXF*NIFISF contract uses its own isotope-column parameter and cannot replace the LIBDEN NESP-dependent contract.'},
 'original_gap_unchanged':True,'actual_current_microlib_STATE16_and_CHI_LIMITS_observed_here':True,'actual_top_microlib_metadata':top_metadata,
 'remaining_necessary_evidence':['Top microlib saved META now independently shows STATE16=4 and root kind1 CHI-LIMITS5=[0,21,40,61,370]. Preserve/bind these exact fields to the same frozen current generation; this META/Source proof is not original LCM memory-bit evidence.','Bind actual FISSIONINDEX64 typed values against same microlib ISOTOPESUSED/ISOTOPERNAME, isotope mixture membership and zero-slot semantics. Do not invent a global32 map; retain all32 NUSIGF/CHI spectral components with the original flattening order.','Original LCM/XSM memory-bit equality remains unverified. Ganlib ASCII exporter prints REAL32 %16.8E and REAL64 %20.12E; two readers agreeing on the saved ASCII export proves only saved-export conversion consistency, not original LCM memory identity. A full binary/original-memory independent observation is still required for that separate claim.','NUSIGF is nu×fission cross section, not loss-only reaction rate. Complete ADDXSNAME reaction identity and true neutron-producing multiplicities for all relevant reactions (including n,2n) must be bound to the current material before physical balance.','Current CTRA APOL chain has stored transport correction flag2; LIBDEN copies and density-weights TRANC. A finite solver must independently honor the original total/scattering/TRANC conventions, three raw Legendre moments, sparse IJJ/NJJ/IPOS and every extra reaction; this Source review does not qualify such interpretation.'],
 'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'transfer_contract_changed_to_PASS':False}
write('REVIEW.json',review)
(ROOT/'REPORT.txt').write_text('Source/META only: authoritative LIBDEN distinguishes local isotope slots NFISSI from expanded fission components NFISSI*NESP.\nLIBDEN.f:1067 FISSIONINDEX is NBMIX*NFISSI kind1; LIBDEN.f:978/984 STATE4 is NFISSI*NESP; LIBDEN.f:902 group fission fields are NBMIX*NFISSI*NESP. INDFIS is microlib isotope ordinal (LIBDEN.f:703; LIBNFI.f:184).\nCurrent saved top microlib STATE16=4 and CHI-LIMITS=[0,21,40,61,370] explicitly confirm4 spectra. Source plus saved counts give NFISSI8 and NESP4:64 indices,32 components and256 values per group. Both A/B preserve all370 groups and all base/delayed fission fields. The expected256 FISSIONINDEX fixture conflicts with this producer layout, but this review does not edit it or grant qualification.\nBefore semantic closure, bind the actual microlib META lineage and index identity/mix/zero slots, then check original LCM memory bits, physical reaction multiplicities and transport-correction interpretation. All physical/native/AAA/ABA qualifications remain false.\nNo raw material payload, project API, guard or business operation was read/run. Exact Source references and full EOF/stat7 pins are in Source files and SOURCE_SEGMENTS.json.\n')
print(json.dumps({'package':str(ROOT),'checks':len(checks),'source_inputs':len(source_pins),'allowed_META':len(meta_pins),'status':review['status'],'review_sha256':hashlib.sha256((ROOT/'REVIEW.json').read_bytes()).hexdigest()}))

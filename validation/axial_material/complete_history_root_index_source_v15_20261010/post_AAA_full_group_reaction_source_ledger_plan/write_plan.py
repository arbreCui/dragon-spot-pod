"""Generate a finite scientific read-only next-check plan from saved metadata.
This script hashes only listed small source/report files; never XSM payloads.
"""
from pathlib import Path
import hashlib,json,os
D=Path('/private/tmp/axmat_refined_AAA_full_group_reaction_source_ledger_plan_20261010')
R=Path('/Users/wen/spot');A=R/'validation/artifacts'
P=A/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
O=A/'axial-material-qualified-AAA-white-trace-refined-observables-20261005'
meta=json.loads((D/'saved_directory_metadata.json').read_text())

def ident(s):return {k:getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}
def pin(p,role):
 before=ident(p.stat());
 if before['st_size']>2**21:raise ValueError('not a small source file: '+str(p))
 with p.open('rb') as f:
  fd_before=ident(os.fstat(f.fileno()));b=f.read();fd_after=ident(os.fstat(f.fileno()))
 after=ident(p.stat())
 if before!=fd_before or before!=fd_after or before!=after or len(b)!=before['st_size']:raise ValueError('source changed')
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'role':role,'path_7id_before':before,'fd_7id_before':fd_before,'fd_7id_after':fd_after,'path_7id_after':after}
files=[
 (P/'prepared.json','historical production prepared pointer and inputs'),
 (P/'AAA/run_status.json','historical VALID_MET / final map012 pointer'),
 (P/'AAA/map012/result.json','historical full stage output seal; XSM hashes from this manifest'),
 (P/'AAA/bootstrap/result.json','historical bootstrap full stage output seal'),
 (P/'AAA/map012/picard_axial.x2m','sealed historical executed deck: FLU -> SPOGBAL -> canonical state -> feedback'),
 (P/'AAA/map012/picard_radial.x2m','sealed historical candidate system assembly deck'),
 (P/'AAA/map012/check_one_map_xsm.log','historical independent fixed-space/layout/mirror/defect log'),
 (P/'AAA/map012/close_r64_returned.log','historical CLOSED/12 commit log'),
 (O/'protocol.json','historical export: explicit track/macro/map012 closed flux and seals'),
 (O/'export_receipt.json','historical complete immutable export receipt'),
 (O/'observables.summary.txt','historical 8x48x370 dimensions and all-group scalar/current checks'),
 (O/'observables.regions.csv','historical complete 384 fine-cell integrated observable values'),
 (O/'observables.faces.csv','historical complete 392 regional face-current values'),
 (A/'axial-material-AAA-white-trace-refined-closeout-20261005/REPORT.txt','actual independent AAA failure and missing full physical neutron balance statement'),
 (A/'axial-material-AAA-white-trace-refined-rate-flux-diagnostic-20261005/REPORT.txt','saved-mean factorization scope: not causal reaction/reduction separation'),
 (A/'axial-material-qualified-AB-admission-v2-20261004/material_snapshot_manifest.json','declared 32 fission components and material/data provenance, not reaction-transfer proof'),
 (A/'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json','original same-data MG transfer requirement / original physical scope'),
 (A/'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004/AAA/reference_contract.json','current CE comparison has energy_edges_ev null'),
 (R/'validation/axial_material/snapshot_control_preflight.py','existing little-endian XSM structural reader _XSM/_open_xsm; source only, never imported here'),
 (R/'validation/axial_material/qualified_snapshot_ingestion.py','existing list_handles record decoding helper; source only, never imported here'),
 (R/'validation/axial_material/audit_AAA_global_transverse_balance.py','existing independent saved-P0 replay design but hardcoded older 8x12 map004'),
 (R/'validation/axial_material/export_qualified_AAA_observables_white_trace_refined.py','existing genuine saved-MET exporter source and immutable input linkage'),
 (R/'validation/axial_material/export_observables.f90','historically pinned exporter source already computes nuSigmaF*FLUX64'),
 (R/'validation/axial_material/project_refined_observables.py','existing complete 4-to-1 conservative projection and single global normalization'),
 (R/'validation/iterative/close_r64_returned.f90','current source context for no-transport closure; current hash not a historical Dragon source attestation'),
 (R/'validation/iterative/check_one_map_xsm.f90','current source context: source is not independently checked by flux-layout predicate'),
 (R/'src/SPOR64_B2W.f90','current source context of whole-AX copy; not a historical executable full-source attestation'),
 (R/'src/FLU2DR64.f','current source context for final work-source REAL32 publication and guarded SIGS temporary source; not historical binary full-source proof'),
 (R/'src/SPOASM.f','current source context for saved candidate system operators'),
 (R/'src/SPOGBAL.f90','current source context: REAL32 FLUX/K/RADIAL-OP plus reconstructed P0 source, already existing'),
 (R/'src/SPOT_LEAKAGE.f90','current source context of fission/descending compressed off-group transfer formulas'),
 (D/'read_saved_directory_metadata.py','standard-library-only directory/state metadata reader actually run, no numeric payload read'),
]
pins=[pin(p,role) for p,role in files]
(D/'small_source_pins.json').write_text(json.dumps({'classification':'FRESH_FULL_SHA_7ID_OF_EXPLICIT_SMALL_SOURCES_ONLY','files':pins},indent=2)+'\n')
# Bound the source claims by actual executed/sealed metadata pointers.
prep=json.loads((P/'prepared.json').read_text());status=json.loads((P/'AAA/run_status.json').read_text());protocol=json.loads((O/'protocol.json').read_text());receipt=json.loads((O/'export_receipt.json').read_text())
assert prep['classification']=='PREPARED_NO_TRANSPORT'
assert status['cases']['AAA']['classification']=='VALID_MET' and status['cases']['AAA']['completed_maps']==12
assert status['cases']['AAA']['final_directory']==str(P/'AAA/map012')
assert receipt['classification']=='SAVED_MET_REAL64_OBSERVABLES_EXPORTED' and receipt['inputs_unchanged']
assert protocol['final_stage_seal']['sha256']==next(x['sha256'] for x in pins if x['path']==str(P/'AAA/map012/result.json'))
assert protocol['production_prepared']['sha256']==next(x['sha256'] for x in pins if x['path']==str(P/'prepared.json'))
for role in ['track','macro','closed_axial']:
 item=meta['archives'][role];assert protocol['source_inputs'][item['path']]==item['manifest_sha256']
arc=meta['archives'];assert arc['track']['state_vector'][0]==384 and arc['track']['state_vector'][5:8]==[8,48,3]
assert arc['track']['state_vector'][1]==1800 and arc['track']['state_vector'][10:12]==[1152,392]
assert arc['macro']['state_vector'][:4]==[370,24,3,32]
for role in ['macro','system']:assert len(arc[role]['all_group_directories'])==370
for key in ['NUSIGF','CHI','SCAT00','NJJS00','IJJS00','IPOS00','NTOT0','TRANC','NFTOT','NG','N2N','N3N','N4N','NA','NP','N2A','NNP','ND','NT','NX']:assert arc['macro']['group_field_presence'][key]['present']==370
for key in ['DRAGON-TXSC','DRAGON-S0XSC','RADIAL-OP64']:assert arc['system']['group_field_presence'][key]['present']==370
for role in ['closed_axial','candidate_axial']:
 assert arc[role]['FLUX64_type_length_counts']==[{'length_words':3600,'type':4,'count':370}]
 assert arc[role]['SOUR_type_length_counts']==[{'length_words':1800,'type':2,'count':370}]
 assert 'SOUR64' not in arc[role]['root_directory'] and 'SPOT-R64' not in arc[role]['root_directory']
assert arc['macro']['root_directory']['ENERGY'][1:]==[371,2]
assert arc['macro']['root_directory']['FISSIONINDEX'][1:]==[64,1]
plan={
 'classification':'SOURCE_ONLY_NEXT_DIAGNOSTIC_PLAN_WITH_SAVED_DIRECTORY_METADATA_VERIFIED',
 'not_executed':'No flux, cross-section, source, current, rate, residual or reaction-channel numeric payload was read or calculated. No business modules imported, transport/compile/fixture/API called, Root session accessed, project file written, huge history rehashed or resource tree scanned.',
 'objective':'Independently replay all 370-group physical source/transfer/closure terms on historical frozen refined AAA map012; distinguish saved work source, final-state source reconstruction, model closure and physical collision accounting. This is not merely repeating existing nuSigmaF*phi export.',
 'historical_scientific_state':{'AAA_MET':True,'maps':12,'fine_cells':384,'fine_faces':392,'axial_planes':49,'groups':370,'mixtures':24,'fission_components':32,'unknowns_per_group':1800,'original_observation_cells':96,'original_observation_planes':13,'independent_nufission_gate':'FAIL approximately 3.9525% > original 3%','AAA_accuracy_qualified':False,'ABA_admitted':False},
 'existing_coverage':[
  'export_observables.f90:67-107 already reads all FLUX64 groups, KEYFLX scalar values and LL4 regional current slice, NUSIGF and sums integrated flux/nu-fission/current. Repeating only that is an exporter check, not the new ledger.',
  'Executed map012 picard_axial.x2m:21 already calls SPOGBAL. Current SPOGBAL.f90:137-161 reads REAL32 FLUX/K and rebuilds source using SPOF00/SPOQ00; :279-325 uses REAL32 RADIAL-OP, corrected removal/selfscatter and face differences. Existing stored balance extrema do not contain the complete independently recomputed REAL64 per-group/cell ledger.',
  'check_one_map_xsm.f90:1244-1267 checks FLUX/optional FLUX64 layout, not an independent authoritative source equality gate.',
  'audit_AAA_global_transverse_balance.py:20-22,88 is old compensated map004/8x12, not refined 8x48 map012. Its :102-127 formula is a relevant read-only starting design only.',
 ],
 'inputs':[{ 'role':role,'path':item['path'],'size_bytes':item['path_7id_before']['st_size'],'sha256_from_frozen_stage_seal':item['manifest_sha256'],'fresh_full_payload_sha_performed_now':False,'metadata_7id_stable':True } for role,item in arc.items()],
 'record_extract_plan':[
  {'owner':'track','records':['STATE-VECTOR','MATCOD','KEYFLX','KEYFLX$ANIS','MAT1D','VOLUME','AREA2D','VOL1D'],'layout':'384 cells; 8 radial x48 axial, 3 snapshot zones; LL4=1152;392 current entries, NU=1800. Retain full unknown vector; scalar/currents extracted by stored indices, not guessed/rank reconstructed.'},
  {'owner':'macro','root':['STATE-VECTOR','ENERGY','FISSIONINDEX','VOLUME','ADDXSNAME-P0','GROUP'],'every_group':['NUSIGF','CHI','NJJS00','IJJS00','IPOS00','SCAT00','SIGS00','SIGW00','NTOT0','TRANC','NFTOT','NG','N2N','N3N','N4N','NA','NP','N2A','NNP','ND','NT','NX','CHECK00'],'layout':'ENERGY371 REAL32;FISSIONINDEX64 integer;NUSIGF/CHI768=24x32 REAL32. All named fields confirmed present in each of370 groups; no values/positivity/units/multiplicity were assessed by metadata-only read. Promote exact frozen REAL32 only at use; preserve all component ordering.'},
  {'owner':'system','root':['STATE-VECTOR','LINK.MACRO','LINK.TRACK','LINK.BASIS','SPOT-FIXB','SPOT-BTYPE','POD-RANK-G'],'every_group':['DRAGON-TXSC','DRAGON-S0XSC','RADIAL-OP','RADIAL-OP64','VOL2D','POD-BASIS','POD-NMODE'],'layout':'all370 group fields confirmed; TX25=0..24, S0=75=3x25, RADIAL-OP64 48words=24 REAL64=8x3.'},
  {'owner':'closed_axial','root':['STATE-VECTOR','SPOT-X-STATE','SPOT-X-EPOCH','SPOT-KEFF64','K-EFFECTIVE','FLUX64','FLUX','SOUR','SPOT-GBAL','SPOT-GBAL-MA','SPOT-MBAL'],'layout':'FLUX64 type4=1800 double each of370; FLUX/SOUR type2=1800 REAL32 each. Complete root metadata confirms no SOUR64 and no SPOT-R64 child in this axial archive.'},
 ],
 'source_semantics':{
  'saved_SOUR32':'Actual archived final work-source buffer projection; current FLU2DR64.f:669-685 constructs fission from old outer flux, :1160-1161 promotes final inner flux/source buffers, :1467-1468 applies common normalization, :1509-1513 writes FLUX64 but source only REAL32. Those code SHA values are current context; historical output type/presence is independently verified by directory metadata and seal. Historical Dragon binary full-source attestation is not inferred from current source.',
  'no_unconditional_equality':'Do not require or assert SOUR32 == round32(final-state rebuilt Q). It is a source work-buffer from iteration; final phi/k reconstruction has a different source epoch and may include a different same-group partition. Preserve/report the full scalar saved-source discrepancy and exact rounding/iteration qualifications.',
  'wrapper_qext64':'Current FLUSP64 (FLU2DR64.f:1628-1650) copies SUN to S2 and may apply guarded SIGS leakage correction before SPOF64. No axial final authoritative R64 S2/work source is present in the checked root; exact S2 bytes cannot be recovered from its REAL32 projection. Do not assume guarded B2 correction actually active without saved flags.',
  'radial_source_not_substitute':'Nested radial SPOT-R64/SOUR authority checked by B2W:724-797 is an indexed radial-plane payload, not the missing384-cell axial final R64 source. Do not substitute it in the axial equation.',
 },
 'equations':[
  'phi[g,i] = FLUX64[g][KEYFLX[i]-1]; J[g,r,z] = FLUX64[g][LL4+r*(NZ+1)+z], positive-z sign; g=1..370,i=all384,r=all8,z=all49faces.',
  'P[i,f] = sum_h NUSIGF[h,m(i),f] * phi[h,i], keeping all32 components and exact declared order.',
  'QF[g,i] = sum_f CHI[g,m(i),f]*P[i,f]/k64. Report sum_g CHI for every mixture/component; do not renormalize missing/nonunit spectra.',
  'QSoff[g,i] = sum_{h!=g} SCAT00[g <- h,m(i)]*phi[h,i], decoding 1-based IJJS00 descending NJJS00 entries at IPOS00; include source-group/offset proof and allzero rows.',
  'C[g,i] = V[i]*((Tcorr[g,m]-Sselfcorr[g,m])*phi[g,i]-QSoff[g,i]-QF[g,i]) + A[r]*(J[g,r,z+1]-J[g,r,z]); D[g,i] = V[i]*RADIAL-OP64[g,r,MAT1D[z]]*phi[g,i]; Rclosed=C+D. Store C,D,Rclosed per group/cell and global signed/absolute sums.',
  'Exact subtraction witness: sum(C)=sum(Rclosed)-sum(D), with justified floating-point summation bound; keep closure D as a reported term. A small Rclosed does not prove physical neutron conservation.',
  'Separately tabulate uncorrected NTOT0, full all-group SCAT00 including self, and transport correction terms. Net total-minus-neutron-transfer is not labelled physical absorption until every frozen reaction channel, multiplicity and transport correction has an explicit accounted contract; NX/other aggregate channels cannot be discarded.',
  'If channel multiplicity/meaning evidence is complete, report physical source+absorption+neutron-production-minus-loss+axial escape ledger without fitted closure. Otherwise return P0-accounting-complete / physical-absorption-not-qualified, not a guessed absorption formula.',
 ],
 'outputs_next_check':[
  'fresh_input_record_manifest.json: literal paths, full SHA7 before/after, root/group/list record count/type/length/offset and raw typed per-record digests, source epoch/units/ownership.',
  'compact little-endian raw arrays + layout JSON for all370x384 scalar/source/closure/collision terms and all370x8x49 face currents; save original full FLUX64 and SOUR32 buffer views or exact source digests where whole-array output exceeds cap. No CSV rounding as raw authority.',
  'per_group_cells_summary.json + small extremal CSV: signed/absolute/cell/global sums, source-buffer-vs-rebuilt-source diagnostic with explicit differing phase, correction/closure splits, chi sums, compressed transfer coverage and component ordering.',
  'export_replay_receipt.json: independently replay full384cell/392face old CSV and fullglobalnorm within explicit operation-count rounding bound; original conservative four-cell mapping and13plane observation view, no local normalization/rate fitting.',
  'physical_scope_and_missing_evidence.json: state whether channel/multiplicity/uncorrected absorption accounting is qualified; R64 work-source absence and current CE energy_edges_ev:null limitation; all AAA/ABA/scientific qualification flags remainfalse.',
  'true OwnRSS watchdog/typed Root terminal/fullstdoutstderr/archive namespace receipt. Structural COMPLETE diagnostic is distinct from a numerical near-zero balance or AAA precision PASS.',
 ],
 'rejection_and_scope_conditions':[
  'Any existing input seal/payload SHA mismatch, path/fd7ID drift, namespace mutation, file truncation/invalid XSM directory cycle/duplicate name/invalid offset must reject; fresh payload checks occur only during the later explicitly authorized bounded diagnostic.',
  'Require exact original8x48x3x370/24mixture/32component/1800unknown schema, full group list370, ENERGY371, complete384key/material map and392face current layout; invalid/missing key, overflow, component regrouping, omitted cell/group or snapped boundary must reject.',
  'Require all scalar flux positive and every parsed field finite, original positive geometry/k64; validate compressed scatter map counts/indices/coverage. Signed currents and physically permitted reaction/closure signs must retain original semantics, not be clipped.',
  'Missing required reaction/channel identity or neutron multiplicity evidence blocks a physical absorption claim, not proof of missing saved field. Record that limitation without inventing CE group spectra or microscopic transfer equivalence.',
  'No reuse of old map004 report as refined result; no transport, compile, basis change, rank selection, white-coefficient fit, thresholds relaxed, pergroup/percell normalization, dropped endpoint bin, inputcopy mutation, numerical retry, or change of original scientific criteria.',
  'Preserve inherited read-only diagnostic60s whole limit/512MiB ownRSS/1thread/1child/0retry; compact output ceiling64MiB is a proposed bounded supervisory envelope, not a historical ledger cap claim. Root must admit normalgenuine supervisor and complete dynamic resource scope96GiB/free8GiB before execute. If bounds fail, sealfailure/no retry in that namespace; no runtime proof existsnow.',
 ],
 'future_success_pins':{'diagnostic_declaration':None,'execution':None,'seal':None,'actual_terminal':None,'actual_watchdog':None,'independent_audit':None,'microscopic_raw_data_transfer':None,'same_data_unreduced_reference':None},
 'source_line_references':[
  {'path':str(R/'validation/axial_material/export_qualified_AAA_observables_white_trace_refined.py'),'lines':[17,35,42,48]},
  {'path':str(R/'validation/axial_material/export_observables.f90'),'lines':[35,46,67,89,101,106]},
  {'path':str(R/'validation/axial_material/audit_AAA_global_transverse_balance.py'),'lines':[20,22,63,65,88,102,107,110,119,130]},
  {'path':str(R/'src/SPOGBAL.f90'),'lines':[137,143,161,230,315,463]},
  {'path':str(R/'src/SPOT_LEAKAGE.f90'),'lines':[116,155,160,205,216,219]},
  {'path':str(R/'src/FLU2DR64.f'),'lines':[680,1160,1467,1509,1513,1628,1630,1645]},
  {'path':str(R/'src/SPOR64_B2W.f90'),'lines':[332,334,724,766]},
  {'path':str(R/'validation/iterative/check_one_map_xsm.f90'),'lines':[1244,1267]},
  {'path':str(A/'axial-material-AAA-white-trace-refined-closeout-20261005/REPORT.txt'),'lines':[14,24]},
 ],
 'source_pin_list':str(D/'small_source_pins.json'),'saved_directory_metadata':str(D/'saved_directory_metadata.json'),
 'scientific_accuracy_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'new_component_86_qualified':False,'Root_live_session_accessed':False,
}
(D/'INPUT_PLAN.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
txt='''冻结 refined AAA map012 全370群反应/源账本下一步计划（仅定位/计划；未计算）\n\n实际保存已核：8径向区×48轴向细格=384cell；8×49face=392；370群；24材料；32裂变分量；每群1800 unknown。\nbootstrap macro ENERGY371、FISSIONINDEX64；370群全部保存NUSIGF/CHI、P0 compressed scatter map/SCAT00、NTOT0/TRANC及现有核反应channel字段。candidate_system370群全部保存correctedTX/S0与RADIAL-OP64。\nclosed_axial保存370×1800 REAL64 FLUX64，以及REAL32 FLUX/SOUR；完整根目录确无SOUR64或SPOT-R64 axial authority。不能把径向plane的R64 SOUR当384cell轴向源。\n旧nativeSPOGBAL/νΣfΦ exporter已经存在；新工作是独立全字段、每群/每格源与碰撞账本、原始sourcebuffer解释、closure项分离和完整细网格账本，不是重复nuSigmaF*phi。\n\n必读原保存输入：\n'''+''.join(f"{role}: {item['path']}\n seal SHA={item['manifest_sha256']} （本次只metadata7ID稳定，未重hash数值payload）\n" for role,item in arc.items())+'''\n核算：QF=Σf χ_gmf (ΣhνΣf_hmf φ_hi)/k64；QSoff按NJJS/IJJS/IPOS下降群序。\nC=V[(Tcorr-Sselfcorr)φ-QSoff-QF]+A(Jright-Jleft)；D=V·RADIAL-OP64·φ；Rclosed=C+D。完整输出C/D/Rclosed；核sumC=sumRclosed-sumD，不删除D。完整uncorrectedNTOT0/allgrouptransfer/correction与所有reaction channels separately报告，未审明multiplicity/NX不得叫物理吸收。\n保存SOUR32是真实lastworksource的投影，不能默认等于最终φ/k重建的REAL64源；源的相位/roundoff/SIGS guarded校正分别记录。current native source哈希是context，不是假定20261005 Dragon二进制完整源码准入。\n\n输出：完整输入/record identities、compact raw+schema的全370×384源/碰撞/闭合项与370×8×49电流、full-cell/global/group摘要、源buffer差异、现有384cell/392face导出独立回放、固定4→1/原single globalnorm 96观察格、缺项/物理scope、真实监督及终端。预算不增加：继承saved-only60s、ownRSS512MiB、thread1/child1/retry0；64MiB compactoutput是拟议bounded envelope，不称旧ledger已声明的cap。Root正式准入normalgenuine supervisor及全资源96GiB/free8后才执行。\n\n拒绝：源pin/7ID/namespace漂移、XSM结构或压缩映射越界、漏群/漏格、材料/分量/群序变更、nonfinite或违反原positive geometry/k/scalarFlux规则、拟合/clip/renormalize/阈值改动、预算超限或旧结果借作本次结果。signedcurrents/允许的closure符号保留。物理channel合同缺失时阻断physicalabsorption信用；不能凭未找到文件宣称数据不存在。\n\n本次未读或计算任一flux/XS/source/current值；数值payload只核元数据和已有seal/export存证。所有新declaration/execution/seal/watchdog/independentaudit/same-MG未降阶reference pins均None，AAA/ABA/scientific/new86资格false。\n详细输入、字段、等式、条件、源行号与小文件freshSHA7见INPUT_PLAN.json/small_source_pins.json。\n'''
(D/'INPUT_PLAN.txt').write_text(txt)
print(json.dumps({'classification':plan['classification'],'directory':str(D),'small_sources':len(pins),'small_source_total_bytes':sum(p['size_bytes'] for p in pins),'metadata_archives':len(arc),'metadata_bytes_read':sum(x['metadata_bytes_read'] for x in arc.values()),'plan_sha256':hashlib.sha256((D/'INPUT_PLAN.json').read_bytes()).hexdigest(),'txt_sha256':hashlib.sha256((D/'INPUT_PLAN.txt').read_bytes()).hexdigest(),'source_pins_sha256':hashlib.sha256((D/'small_source_pins.json').read_bytes()).hexdigest(),'directory_metadata_sha256':hashlib.sha256((D/'saved_directory_metadata.json').read_bytes()).hexdigest(),'future_success_pins_all_none':all(v is None for v in plan['future_success_pins'].values())},indent=2))

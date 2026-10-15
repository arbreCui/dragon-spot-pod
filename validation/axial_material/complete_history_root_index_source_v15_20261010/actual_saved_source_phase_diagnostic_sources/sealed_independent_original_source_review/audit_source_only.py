from pathlib import Path
import ast,hashlib,json,os,time,collections
ROOT=Path('/Users/wen/spot')
PACKAGE=Path('/private/tmp/axmat_saved_source_phase_source_only_20261010_nx62ri4n')
OUT=Path(__file__).parent
EXPECTED='58d1cad3ed22b3d56f7db4d721ed3166cae04fd7d86e5c95f6c9df1532023fb9'
MANIFEST_EXPECTED='a99db7ea44374e9c86159f102aa7f32c7fcaff0b7311ba71db341caff417dece'
start=time.monotonic()
def identity(path):
 s=path.stat();return {k:getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}
def pin(path):
 b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'target_7id':identity(path)}
def unique(pairs):
 d={}
 for k,v in pairs:
  assert k not in d
  d[k]=v
 return d
def load(path):
 return json.loads(path.read_text(),object_pairs_hook=unique,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite metadata')))
def write(name,obj):
 (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
def segments(text):
 return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
source=PACKAGE/'complete_saved_S2_source_phase_consistency.UNREADY.py'
sp=pin(source);assert sp['sha256']==EXPECTED and sp['bytes']==290158
mp=pin(PACKAGE/'SOURCE_MANIFEST.json');assert mp['sha256']==MANIFEST_EXPECTED
manifest=load(PACKAGE/'SOURCE_MANIFEST.json')
assert set(manifest['members'])=={p.name for p in PACKAGE.iterdir() if p.is_file() and p.name!='SOURCE_MANIFEST.json'}
package_pins={}
for name,want in manifest['members'].items():
 actual=pin(PACKAGE/name);assert actual['sha256']==want['sha256'] and actual['bytes']==want['bytes'];package_pins[name]=actual
text=source.read_text();tree=ast.parse(text)
assign={}
for n in tree.body:
 if isinstance(n,ast.Assign):
  for target in n.targets:
   if isinstance(target,ast.Name):assign[target.id]=n.value
assert ast.literal_eval(assign['SOURCE_STATUS'])=='UNREADY'
assert ast.literal_eval(assign['WALL_SECONDS'])==60.0 and ast.literal_eval(assign['RSS_LIMIT_MIB'])==512.0
assert isinstance(assign['ARCHIVE_LIMIT_BYTES'],ast.BinOp)
assert ast.get_source_segment(text,assign['ARCHIVE_LIMIT_BYTES'])=='64*2**20'
assert ast.literal_eval(assign['THREADS'])==ast.literal_eval(assign['CHILDREN'])==1
assert ast.literal_eval(assign['RETRIES'])==0
inp=assign['INPUTS'];assert isinstance(inp,ast.Dict)
inputs={}
for kn,vn in zip(inp.keys,inp.values):
 key=ast.literal_eval(kn);assert key not in inputs and isinstance(vn,ast.Tuple) and len(vn.elts)==2
 path_expr,sha_expr=vn.elts
 assert isinstance(path_expr,ast.Call) and isinstance(path_expr.func,ast.Name) and path_expr.func.id=='Path' and len(path_expr.args)==1
 path=Path(ast.literal_eval(path_expr.args[0]));sha=ast.literal_eval(sha_expr)
 assert path.is_absolute() and len(sha)==64 and all(c in '0123456789abcdef' for c in sha)
 inputs[key]=(path,sha)
assert len(inputs)==1140
contract=load(PACKAGE/'input_contract.json');assert set(contract['inputs'])==set(inputs)
for k in ('future_actual_evaluator_pin','future_actual_host_pin','future_actual_output_pins','future_actual_terminal_pin'):
 assert contract[k] is None and manifest[k] is None
assert contract['numeric_payload_parsed'] is False
observed={};text_pins={};sizes=0;numeric_count=0
for role,(path,sha) in inputs.items():
 rec=contract['inputs'][role];assert rec['path']==str(path) and rec['expected_sha256']==sha
 actual=identity(path);assert actual==rec['observed_metadata_7id'];sizes+=actual['st_size']
 observed[role]={'path':str(path),'claimed_expected_sha256':sha,'fresh_observed_target_7id':actual,'binary_payload_read':False}
 assert rec['binary_numeric_payload_read_this_source_review'] is False
 if path.suffix in ('.json','.py','.f','.f90'):
  p=pin(path);assert p['sha256']==sha and rec['full_EOF_hash_performed_this_source_review'] is True;text_pins[role]=p
 else:
  assert path.suffix in ('.bin','.xsm') and rec['full_EOF_hash_performed_this_source_review'] is False;numeric_count+=1
assert sizes==96042876
for family in ('capture_source_','capture_return_','capture_field_'):
 assert {k for k in inputs if k.startswith(family)}=={family+f'{i:03d}' for i in range(1,371)}
assert 3+3*370==1113
# Original exact mature parser source segments, read as text only.
parser_path=inputs['parser_source'][0];capture_path=inputs['capture_evaluator_source'][0]
assert text_pins['parser_source']['sha256']=='4851d9151dfe5682a36f450fff8d0acb42c69865e177affe81c4b703119f7874'
assert text_pins['capture_evaluator_source']['sha256']=='cf402b628cf4c5095ffbc078f36a169624d42853e250248af23e3e37ac1775a2'
current=segments(text);old=segments(parser_path.read_text());captured=segments(capture_path.read_text());exact={}
for name in ('identity','check_time','fresh_hash','XSM','Output'):
 assert current[name]==old[name];exact[name]={'byte_exact':True,'origin_sha256':text_pins['parser_source']['sha256']}
assert current['unpack']==captured['unpack'];exact['unpack']={'byte_exact':True,'origin_sha256':text_pins['capture_evaluator_source']['sha256']}
# Rebind all selected binary SHA claims to immutable metadata only, not new binary EOF observations.
seal=load(inputs['capture_seal'][0]);raw=load(inputs['capture_raw_receipt'][0]);decl=load(inputs['capture_declaration'][0]);admit=load(inputs['capture_archival_admission'][0])
final=load(inputs['production_final_seal'][0]);capture_root=inputs['capture_seal'][0].parent
for role,(path,sha) in inputs.items():
 if role.startswith(('capture_source_','capture_return_','capture_field_')) or role in ('capture_published','capture_events','capture_pre_normal'):
  rel=str(path.relative_to(capture_root));assert seal['files'][rel]==raw['files'][rel]==sha
for role in ('production_closed_axial','production_candidate_axial','track'):
 path,sha=inputs[role];assert final['sha256'][path.name]==sha
assert raw['original_output_files']['candidate_axial.xsm']==inputs['capture_candidate_axial'][1]==inputs['production_candidate_axial'][1]
diag=load(inputs['diagnostic_manifest'][0])
for role in ('diagnostic_full_flux','diagnostic_full_source'):
 path,sha=inputs[role];assert diag['files'][path.name]['sha256']==sha
# True reversible archival insertion proof on entire source bytes, never evidence of complete original compilation identity.
inverse={}
for name,role,base in (('FLU2DR64.f','capture_sender_source','capture_sender_baseline'),('SPOT1P64.f90','capture_receiver_source',None)):
 patch=admit['patches'][name];candidate=inputs[role][0].read_text();assert patch['candidate_sha256']==inputs[role][1] and patch['native_expressions_changed'] is False
 changed=candidate
 for oldtext,newtext in reversed(patch['replacements']):
  assert changed.count(newtext)==1;changed=changed.replace(newtext,oldtext,1)
 h=hashlib.sha256(changed.encode()).hexdigest();assert h==patch['original_sha256']
 if base is not None:assert changed.encode()==inputs[base][0].read_bytes()
 inverse[name]={'whole_text_restored_sha256':h,'all_inverse_fragments_unique_once':True,'complete_original_compilation_source_identity_proved':False}
# Static exact scope assertions: AST/text inspection, no driver import/evaluation.
evaluate=current['evaluate'];events=current['events'];main=current['main'];eq=current['equal_words']
assert 'left.dtype==right.dtype and left.shape==right.shape and left.tobytes()==right.tobytes()' in eq
for fragment in ('for group in range(1,NG+1)',"equal_words(s2[:LL4],a['qext'].ravel(order='F')",'equal_words(returned,prenormal', 'equal_words(returned*normal,final','equal_words(s2*normal,source',"demoted=source.astype('<f4')","('FLUX64',2*NUN,4,'<f8',final)","('FLUX',NUN,2,'<f4',final.astype('<f4'))","('SOUR',NUN,2,'<f4',demoted)",'entry[1:]==(words,kind)',"diagflux.words('<f8',NUN)","diagsource.words('<f4',NUN)"):
 assert fragment in evaluate,fragment
for fragment in ('seq==len(records)+1','np.array_equal(active,np.flatnonzero(npsys)+1)','latest[active-1]=[seq,outer,inner]','calls[active-1]+=1','len(records)==136 and np.all(latest[:,1:]==[3,1])'):
 assert fragment in events,fragment
for fragment in ("np.array_equal(context[1:4],latest[group-1])",'context[6]==calls[group-1]',"equal_words(real[6:7],operands[:1]",'normal=operands[0]/operands[1]',"fields.words('<i4',8)","header[4:].tolist()==[466,326,7883,1490]", "a['flux'].ravel(order='F'),a['current'].ravel(order='F'),a['xnei'].ravel(order='F')"):
 assert fragment in evaluate,fragment
for name in ('reaction_multiplicity_contract_qualified','source_fission_scatter_partition_qualified','full_physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','same_MG_unreduced_reference_qualified','transport_launched','entire_original_compilation_source_byte_identity_proved'):
 assert "'"+name+"':False" in evaluate,name
assert "if SOURCE_STATUS!='READY'" in main and 'fresh_hash(path,start)' in main
assert "literal_7id_before" in main and "target_7id_before" in main and "literal_symlink_text" in main
assert not any(isinstance(n,ast.Assert) for n in ast.walk(tree))
# Fixed constants and planned array arithmetic; budget estimates only.
arrays={'raw_S2':370*1800*8,'published_source64':370*1800*8,'published_flux64':370*1800*8,'qext':370*1*3*48*8*8,'projected_source':370*3*48*1*8}
assert sum(arrays.values())==19820160
for role,(path,_) in inputs.items():assert identity(path)==observed[role]['fresh_observed_target_7id']
assert pin(source)==sp and pin(PACKAGE/'SOURCE_MANIFEST.json')==mp
report={'schema':'AXMAT_INDEPENDENT_SAVED_SOURCE_PHASE_DRIVER_SOURCE_REVIEW_V1','status':'PASS_SOURCE_ONLY_NO_RUNTIME_OR_PHYSICS_QUALIFICATION','scope':'AST, complete source/text/JSON read and input stat only; no candidate/helper import, no numeric payload reads, no transport','candidate':sp,'source_manifest':mp,'blocking_findings':[], 'inputs_count':len(inputs),'metadata_observed_input_bytes':sizes,'numeric_input_files_not_read':numeric_count,'selected_raw_capture_files':1113,'selected_binary_SHA_claims_rebound_to_fixed_JSON_manifests':True,'full_numeric_EOF_SHA_done_by_this_review':False,'mature_parser_exact_source_segments':exact,'capture_whole_text_inverse':inverse,'all_370_groups_1800_unknowns_384_cells_392_faces_three_moments_kept':True,'chronological_selection':'all 136 dispatches; fixed actual NGIND/NPSYS; per-group counts and last [outer3,inner1]; no metric selection','typed_word_equality':'dtype+shape+entire bytes, including signed zero; no added tolerance','normalization':'one original REAL64 AKEFF/FISOUR applied to all1800 returned and S2 words; same published operands bound to terminal and allthree XSM keff; native REAL32 demotion exactly compared','source_position_reviewed':'post-SIGS/pre-SPOF64 S2 capture; full return capture; post-convergence PRENORMAL before original common normalization; published after SOUR32 save','source_partition_qualified':False,'full_original_compilation_byte_identity_proved':False,'reaction_multiplicity_contract_qualified':False,'full_physical_neutron_balance_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'same_MG_unreduced_reference_qualified':False,'resource_plan_source_estimate_only':{'whole_seconds':60,'stage_seconds':60,'own_RSS_MiB':512,'archive_cap_bytes':64*2**20,'original_history_cap_bytes':96*2**30,'minfree_bytes':8*2**30,'threads':1,'children':1,'retries':0,'fixed_array_bytes':arrays,'fixed_array_total_bytes':sum(arrays.values()),'source_package_bytes':manifest['total_member_bytes']+mp['bytes'],'estimated_compact_total_bound_bytes':30*2**20,'remaining_headroom_under64MiB_after30MiB_sourceestimate':34*2**20,'own_RSS_estimate_MiB':150,'candidate_actual_RSS':None,'candidate_actual_wall_seconds':None,'host_source_output_receipts_must_be_jointly_counted_by_Root':True,'estimate_is_not_measured_feasibility_or_admission':True},'source_only_tool_wall_seconds':time.monotonic()-start,'required_actual_next_evidence':['Root READY exact source pin with only source admission change','one genuine OwnRSS host with original joint host/source/output budget and original history/free caps','fresh literal/target/fd7ID and EOF SHA before/after all1140 fixed inputs','actual complete-stream results plus output manifest, own RSS sample and strict integer EXIT0 with no live session','independent actual output byte review granting only narrow saved-work-RHS-phase identity'],'future_actual_evaluator_pin':None,'future_actual_host_pin':None,'future_actual_output_pins':None,'future_actual_terminal_pin':None}
write('REVIEW.json',report);write('SOURCE_PROOF.json',{'candidate':sp,'manifest':mp,'package_members':package_pins,'text_JSON_source_inputs_full_EOF_pins':text_pins,'numeric_inputs_stat_only_and_expected_SHA_claimed':observed,'all_metadata_7id_unchanged_after_review':True,'candidate_imported':False,'candidate_executed':False,'numeric_payload_read':False})
(OUT/'REPORT.txt').write_text('独立 SOURCE 审查通过：没有发现阻止一次受限保存态诊断的正确性问题。\n\n覆盖全部370群×1800 unknowns、384 cells、392 faces、3 moments；136 dispatch 按真实 NGIND/NPSYS 重建每群最后调用，没有按误差选样。post-SIGS S2 的源矩与 qext、原顺序 projection，完整 field flux/current/xnei 与 return/PRENORMAL，以及同一原 AKEFF/FISOUR 后的 published REAL64 flux/source，均以 dtype、shape 和全部字节相等为唯一合同。三 XSM 的完整 FLUX64/FLUX/SOUR 和既有全群诊断数组以原精度逐字核验，保留 signed zero，无新 tolerance。\n\n本次只读源码/JSON并 stat：候选没有 import/运行，全部numeric payload没有读。1,140输入共96,042,876 bytes来自本次 metadata身份观察；numeric SHA只向原sealed JSON重绑，没有伪称本次EOF读数。成熟parser六段原文逐字一致，两份Fortran全文逆转插入恢复原SHA，仍不能证明完整原编译源码身份。\n\n仅可在Root一次真实受限运行成功后授“原map012保存态工作RHS与源阶段的字一致”证据。构源分项/旧flux输入、完整编译链、反应multiplicity、完整物理balance、same-MG全阶参考、AAA和ABA均未qualified。\n\n预算估算：完整数组19,820,160 bytes；预计compact总计≤30MiB、OwnRSS约150MiB、60s内。此为SOURCE估算，不是实测；Root须把host+out+source归档和凭证共同算入原64MiB，并保持60s/512MiB/96GiB历史/8GiB空闲/1线程/1child/0retry。真实失败不得改门槛重跑。\n')
print(json.dumps({'status':report['status'],'review_directory':str(OUT),'review_sha256':pin(OUT/'REVIEW.json')['sha256'],'proof_sha256':pin(OUT/'SOURCE_PROOF.json')['sha256'],'inputs':len(inputs),'numeric_payload_read':False,'candidate_imported':False,'candidate_executed':False},indent=2))

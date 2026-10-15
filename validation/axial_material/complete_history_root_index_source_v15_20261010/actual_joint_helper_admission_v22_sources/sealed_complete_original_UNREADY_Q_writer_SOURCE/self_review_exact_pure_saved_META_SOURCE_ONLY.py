"""Stdlib AST/allowed saved-META review only; never runs or imports candidate."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).absolute().parent
P=Path('/private/tmp/axmat_v22_actual_pure_protocol_META_peer_20261010_ucrm3_bz')
FILES=[HERE/'write_actual_joint_helper_admission_v22.exact_pure_saved_META.UNREADY.py',HERE/'write_actual_joint_helper_admission_v22.UNREADY.py',HERE/'original_V21_joint_Q_writer_FULL_SOURCE.py',HERE/'FULL_WRITER_SOURCE_INVERSE.json',HERE/'EXACT_PURE_SAVED_META_FULL_SOURCE_INVERSE.json',HERE/'MINIMAL_COMPLETE_CANONICAL_PREP_SOURCE_ADAPTATION_PLAN.json',HERE/'EXACT_FUTURE_CANONICAL_GENUINE_PREP_SOURCE_LOCATIONS.json',P/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_REVIEW.json',P/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL.json',P/'ACTUAL_PURE_PROTOCOL_META_PEER_AUDIT_TOOL_RETURN.json',P/'ACTUAL_PURE_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json']
CHECKS=[]
def check(name,value,evidence=None):
 assert type(value)is bool;CHECKS.append(dict(name=name,pass_=value,evidence=evidence));CHECKS[-1]['pass']=CHECKS[-1].pop('pass_');assert value,name
def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];raw=p.read_bytes();t=p.lstat();z=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];assert a==z and len(raw)==a[4]
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)
before=[pin(p)for p in FILES];src=FILES[0].read_text();original=FILES[2].read_text();proof=json.loads(FILES[4].read_bytes());initialproof=json.loads(FILES[3].read_bytes());tree=ast.parse(src);oldtree=ast.parse(original)
check('complete exact-pure Source e692',before[0]['sha256']=='e6925e7720dd2cd213c24c0d4c35ddf2391d6e3ccbb5d7883819c037be0a54f4')
restored=src
for i,h in reversed(list(enumerate(proof['complete_finite_hunks']))):check('complete new exact-pure13 inverse '+str(i),restored.count(h['new'])==1);restored=restored.replace(h['new'],h['old'],1)
check('complete new byteinverse initial dc816',restored==FILES[1].read_text()and hashlib.sha256(restored.encode()).hexdigest()==proof['parent_sha256'])
parts=restored[len(initialproof['new_header_full_utf8']):].split(initialproof['new_helpers_full_utf8']+'\ndef main():\n    require_bound_saved_reviews()\n');check('old finite main wrapper single',len(parts)==2);prefix,body=parts;footer="\nif __name__ == '__main__':\n    main()\n";check('old main footer',body.endswith(footer));body=body[:-len(footer)];restored=prefix+''.join(line[4:]if line.strip()else line for line in body.splitlines(keepends=True))
for i,h in reversed(list(enumerate(initialproof['retarget_and_required_new_contract_hunks']))):check('all original41 inverse '+str(i),restored.count(h['new'])==1);restored=restored.replace(h['new'],h['old'],1)
check('complete chained whole byteinverse a732',restored==original)
check('complete chained whole ASTinverse a732',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(oldtree,include_attributes=False))
newdefs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};olddefs={n.name:n for n in oldtree.body if isinstance(n,ast.FunctionDef)}
for name,node in olddefs.items():check('whole original7 function byte+AST '+name,ast.dump(node,include_attributes=False)==ast.dump(newdefs[name],include_attributes=False)and ast.get_source_segment(original,node)==ast.get_source_segment(src,newdefs[name]))
oldadmission=next(n.value for n in oldtree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets));newadmission=next(n.value for n in newdefs['main'].body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets));ok=[k.value for k in oldadmission.keys];nk=[k.value for k in newadmission.keys]
check('all original complete Q topfields retained',set(ok)<=set(nk),ok);oldfresh=oldadmission.values[ok.index('complete_current_graph_fresh_verifier')];newfresh=newadmission.values[nk.index('complete_current_graph_fresh_verifier')];check('all original currentgraph Q fields retained',{k.value for k in oldfresh.keys}<={k.value for k in newfresh.keys})
globals_={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check('UNREADY blocks actual METAwriter',ast.literal_eval(globals_['WRITER_SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22')
check('fresh peer exact-field-shape future guard still None',ast.literal_eval(globals_['ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED'])is None)
for name in ast.literal_eval(globals_['REQUIRED_FUTURE_BINDING_FIELDS']):check('all unknown actual archive bindings None '+name,ast.literal_eval(globals_[name])is None)
check('main actual METAwriter guard first',isinstance(newdefs['main'].body[0],ast.Expr)and isinstance(newdefs['main'].body[0].value,ast.Call)and newdefs['main'].body[0].value.func.id=='require_bound_saved_reviews')
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.Assign,ast.If))or isinstance(n,ast.Expr)and isinstance(n.value,ast.Constant):continue
 check('no importtime actual METAcalls',False,ast.dump(n))
pure=json.loads(FILES[7].read_bytes());seal=json.loads(FILES[8].read_bytes());tool=json.loads(FILES[9].read_bytes());sealtool=json.loads(FILES[10].read_bytes())
check('pure actual complete new schema',pure['schema']=='INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1')
check('pure all1084 typed true hardblockers[]',pure['PASS']is True and pure['hard_blockers']==[]and type(pure['check_count'])is int and pure['check_count']==len(pure['checks'])==1084 and all(type(x['PASS'])is bool and x['PASS']is True for x in pure['checks']))
check('pure193 fullEOF rows117unique',len(pure['complete_full_EOF_reads'])==193 and len({x['path']for x in pure['complete_full_EOF_reads']})==117)
check('pure actual271? no fixed Sourcecrop',[(x['label'],x['regular_file_count'],len(x['symlinks']))for x in pure['complete_namespace_snapshots']]==[('D',61,0),('H',5,0),('O',33,2),('E_pre_summary',9,0)])
check('pure actual control counts4positive3negative2subtype2partial',[len(pure['original_and_new_complete_controls'][k])for k in('new_owner_positive_controls','new_owner_guard_rejections','new_owner_subtypes','new_owner_invalid_second_rejections')]==[4,3,2,2])
check('pure originalfixture37paired18codec61subtype2trace63379',[pure['original_and_new_complete_controls'][k]for k in('original_fixture_rejections','original_paired_fixture_rejection_cases','original_codec_rejections','original_subtype_controls','full_new_trace_records')]==[37,18,61,2,63379])
ledger=pure['archive_ledger_scope'];check('pure original vs conservative joint ledgers distinct honest',ledger['original_normal_guard_regular_file_bytes']==61013090 and ledger['conservative_META_extra_symlink_literal_bytes']==38 and ledger['Root_saved_META_total_DHO_bytes']==61013128 and 61013090+38==61013128<ledger['cap_bytes']==64*2**20)
check('pure newQ/fullfresh/science snapshot honest',pure['pure_protocol_saved_evidence_independently_reviewed']is True and pure['full_current_graph_verifier_qualified']is False and pure['new_Q']is None and pure['whole_build_INPUT_native_physics_AAA_ABA_goal_credit']is False)
check('pure actual bfea raw actual0closed',tool['chunk_id']=='bfea93'and type(tool['exit_code'])is int and tool['exit_code']==0 and'session_id'not in tool)
check('pure full actual seal schema and rawtool exact',seal['schema']=='INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL_V1'and seal['actual_peer_audit_tool_return']==tool and seal['actual_peer_closed']is True and type(seal['actual_peer_exit_code'])is int and seal['actual_peer_exit_code']==0)
check('pure actualseal28f447typed0closed',sealtool['closed']is True and sealtool['terminal_tool_return']['chunk_id']=='28f447'and type(sealtool['terminal_tool_return']['exit_code'])is int and sealtool['terminal_tool_return']['exit_code']==0 and'session_id'not in sealtool['terminal_tool_return'])
for key in ('private_owner_consume_controls','positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections','first_valid_slot_None_after_original_validate_and_append','owned_list_completely_cleared_after_success','complete_full_EOF_reads','complete_namespace_snapshots','original_normal_guard_regular_file_bytes','conservative_META_extra_symlink_literal_bytes','37112','37111','63379','175886','237767','62332','36776'):
 check('complete retained original and new scope '+key,key in src)
check('metadata exact type order floatbit comparator Source',"type(a) is not type(b)"in src and"list(a) == list(b)"in src and"struct.pack('>d', a) == struct.pack('>d', b)"in src)
plan=json.loads(FILES[6].read_bytes());check('complete canonical11/PREPhost11 unique anchors',len(plan['canonical_exact_anchors'])==len(plan['host_exact_11_atomic_anchors'])==11 and all(x['whole_source_occurrences']==1 for x in plan['canonical_exact_anchors']+plan['host_exact_11_atomic_anchors']))
check('exact 70 and all6future None',plan['original70definitions_bytes_and_math_to_remain_unchanged_except_require_ready_own_status_literal']is True and len(plan['six_future_business_pins'])==6 and all(x is None for x in plan['six_future_business_pins'].values()))
check('no businesscandidate or actualnewQ',plan['canonical_or_host_candidate_written']is False and plan['future_new_joint_helper_Q_sha256']is None)
for p in HERE.iterdir():
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));check('Source AST only '+p.name,True)
after=[pin(p)for p in FILES];check('all bounded fullSource/allowedMETA fullEOF SHA7ID beforeafter equal',before==after)
result={'schema':'V22_EXACT_PURE_SAVED_META_UNREADY_WRITER_SOURCE_SELF_REVIEW_V1','source_only':True,'status':'SOURCE_ONLY_PASS_EXPLICIT_UNREADY_FRESH_SAVED_META_ADAPTER_PENDING','all_checks_passed':True,'checks':CHECKS,'bounded_full_Source_META_pins_before':before,'bounded_full_Source_META_pins_after':after,'actual_new_helper_Q_created':False,'candidate_executed_or_imported':False,'Root_project_D_E_canonical_or_ART_written':False,'ART_payload_read_or_history_scanned':False,'remaining_required_Source_change':'Actual fresh saved-peer schema/fields must be supplied and independently reviewed, plus actual archived peer pins; existing guessed old fresh checks are unreachable due UNREADY status and None field-shape guard'}
with(HERE/'EXACT_PURE_SAVED_META_SOURCE_SELF_REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'source_only':True,'status':result['status'],'check_count':len(CHECKS),'report':pin(HERE/'EXACT_PURE_SAVED_META_SOURCE_SELF_REVIEW.json'),'candidate':before[0],'new_Q_created':False}))

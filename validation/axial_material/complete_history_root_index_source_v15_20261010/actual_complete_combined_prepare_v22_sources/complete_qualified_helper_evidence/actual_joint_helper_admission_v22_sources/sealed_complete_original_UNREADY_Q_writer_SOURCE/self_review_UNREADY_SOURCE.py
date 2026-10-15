"""Stdlib Source/allowed saved-META self review; do not import or run candidate."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).absolute().parent
R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
CHECKS=[]

def check(name,value,evidence=None):
 assert type(value)is bool
 CHECKS.append(dict(name=name,pass_=value,evidence=evidence));CHECKS[-1]['pass']=CHECKS[-1].pop('pass_')
 assert value,name

def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];raw=p.read_bytes();t=p.lstat();z=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];assert a==z and len(raw)==a[4]
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)

paths=[Path('/private/tmp/spot_v21_joint_helper_admission_root_meta_20261010.py'),R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py',B/'actual_complete_combined_prepare_v21_sources/sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/combined_prepare_host.py',B/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json',R/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',R/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py',B/'actual_complete_graph_helper_controls_v22_receipts/Root_actual_pure_protocol_summary.json',B/'actual_complete_graph_fresh_verifier_v22_receipts/Root_actual_fresh_verifier_summary.json',B/'actual_complete_graph_helper_controls_v22_receipts/Root_actual_pure_protocol_tool_terminal_return.json',B/'actual_complete_graph_fresh_verifier_v22_receipts/Root_actual_fresh_verifier_tool_terminal_return.json']
before=[pin(p)for p in paths]
expected={str(paths[0]):'a7324201063e968fcd7c9f7f0728722824b248bab065652de0d34985db5e6b22',str(paths[1]):'023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',str(paths[3]):'29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2',str(paths[4]):'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7',str(paths[5]):'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c',str(paths[6]):'f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4',str(paths[7]):'fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e',str(paths[8]):'12d8bbdef3cd59c2f9889d507cf8e5e646f37f4d7e0df1649381373c82100e78',str(paths[9]):'de3750d802a442329089c5301d36939bda610ddc88bc7770dbe0c0f7f65a76f4'}
for p in before:check('actual full EOF exact Source/META SHA '+p['path'],p['sha256']==expected.get(p['path'],p['sha256']),p)
source=(HERE/'write_actual_joint_helper_admission_v22.UNREADY.py').read_text();parent=(HERE/'original_V21_joint_Q_writer_FULL_SOURCE.py').read_text();proof=json.loads((HERE/'FULL_WRITER_SOURCE_INVERSE.json').read_bytes())
check('candidate fixed actual Source dc816',pin(HERE/'write_actual_joint_helper_admission_v22.UNREADY.py')['sha256']=='dc816f899d01623ed63a3cf421a4faa6bdb62ba1eac05972c1ff402e19d36217')
parsed=ast.parse(source);oldtree=ast.parse(parent)
check('complete parent fullsource copy actuala732',hashlib.sha256(parent.encode()).hexdigest()==expected[str(paths[0])])
parts=source[len(proof['new_header_full_utf8']):].split(proof['new_helpers_full_utf8']+'\ndef main():\n    require_bound_saved_reviews()\n')
check('one finite metadata block main wrapper',len(parts)==2)
prefix,body=parts;footer="\nif __name__ == '__main__':\n    main()\n";check('finite main footer exact',body.endswith(footer));body=body[:-len(footer)]
restored=prefix+''.join(line[4:]if line.strip()else line for line in body.splitlines(keepends=True))
check('finite41 retarget/additional contract hunks',len(proof['retarget_and_required_new_contract_hunks'])==41)
for i,h in reversed(list(enumerate(proof['retarget_and_required_new_contract_hunks']))):check('full source inverse unique hunk '+str(i),restored.count(h['new'])==1);restored=restored.replace(h['new'],h['old'],1)
check('whole writer fullbyte inverse exact a732',restored==parent)
check('whole writer fullAST inverse exact a732',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(oldtree,include_attributes=False))
olddefs={n.name:n for n in oldtree.body if isinstance(n,ast.FunctionDef)};newdefs={n.name:n for n in parsed.body if isinstance(n,ast.FunctionDef)}
for name,node in olddefs.items():check('all7 original definition Source AST '+name,ast.dump(node,include_attributes=False)==ast.dump(newdefs[name],include_attributes=False)and '\n'.join(parent.splitlines()[node.lineno-1:node.end_lineno])=='\n'.join(source.splitlines()[newdefs[name].lineno-1:newdefs[name].end_lineno]))
oldadmission=next(n.value for n in oldtree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets));newadmission=next(n.value for n in newdefs['main'].body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets))
oldkeys=[k.value for k in oldadmission.keys];newkeys=[k.value for k in newadmission.keys]
check('full original Root Q top-level field contract retained',set(oldkeys)<=set(newkeys),oldkeys)
oldfresh=oldadmission.values[oldkeys.index('complete_current_graph_fresh_verifier')];newfresh=newadmission.values[newkeys.index('complete_current_graph_fresh_verifier')]
check('full original fresh Q nested field contract retained',{k.value for k in oldfresh.keys}<={k.value for k in newfresh.keys})
values={n.targets[0].id:n.value for n in parsed.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check('explicit UNREADY status nonrunnable',values['WRITER_SOURCE_STATUS'].value=='UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22')
check('future actual saved-field-shapes not known/READY',values['ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED'].value is None)
for name in ast.literal_eval(values['REQUIRED_FUTURE_BINDING_FIELDS']):check('unknown future binding None '+name,values[name].value is None)
for key in ('original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation','63379','175886','237767','62332','36776','37112','37111','expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace','private_positive_controls','private_reject_controls'):check('full original protocol/fresh contract retained '+key,key in source)
for key in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections','first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved'):check('new complete private owner actual contract '+key,key in source)
for p,kind in [(paths[6],'PURE'),(paths[7],'FRESH')]:
 d=json.loads(p.read_bytes());check('actual new summary exact V22 schema '+kind,d['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1')
 check('summary closeout snapshot independent review false '+kind,d['independent_saved_actual_review_pass']is False)
 check('summary closeout snapshot future Q None '+kind,d['actual_new_helper_qualification_sha256']is None)
 check('snapshot false retained in writer Source '+kind,"value['independent_saved_actual_review_pass'] is False"in source and"value['actual_new_helper_qualification_sha256'] is None"in source)
 for k in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):check('snapshot truthful business/science false '+kind+'/'+k,d[k]is False)
for p,chunk in [(paths[8],'6f6847'),(paths[9],'57a6f5')]:
 d=json.loads(p.read_bytes());tr=d['terminal_tool_return'];check('actual Root genuine terminal stricttyped0/CLOSED '+chunk,d['closed']is True and d['actual_tool_terminal_return_observed']is True and d['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==0 and'session_id'not in tr and tr['chunk_id']==chunk)
plan=json.loads((HERE/'MINIMAL_COMPLETE_CANONICAL_PREP_SOURCE_ADAPTATION_PLAN.json').read_bytes())
check('exact70 original canonical definitions preserved Source plan',plan['canonical_actual_definition_count']==70)
check('all6 futurebusiness None unchanged',len(plan['six_future_business_pins'])==6 and all(v is None for v in plan['six_future_business_pins'].values()))
check('no business candidate or newQ generated',plan['new_runtime_candidate_authored']is False and plan['actual_new_helper_Q_path']is None and plan['actual_new_helper_Q_sha256']is None)
for p in sorted(HERE.iterdir()):
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));check('complete package Source AST parse only '+p.name,True)
after=[pin(p)for p in paths];check('all Source/allowedMETA complete EOF SHA7ID unchanged',before==after)
result=dict(schema='V22_COMPLETE_JOINT_ADMISSION_UNREADY_SOURCE_SELF_REVIEW_V1',status='SOURCE_ONLY_PASS_UNREADY_NO_Q',source_only=True,all_checks_passed=True,checks=CHECKS,actual_fixed_Source_and_META_before=before,actual_fixed_Source_and_META_after=after,candidate=pin(HERE/'write_actual_joint_helper_admission_v22.UNREADY.py'),oldQ_only_Source_parent_not_qualification_credit=True,original_writer_fullbyte_AST_inverse=True,actual_saved_review_field_shape_binding_completed=False,generated_writer_or_project_API_executed=False,ART_payload_read_or_history_scanned=False,actual_Q_created=False,new_runtime_candidate_authored=False)
with(HERE/'SOURCE_SELF_REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,status=result['status'],check_count=len(CHECKS),report=pin(HERE/'SOURCE_SELF_REVIEW.json'),candidate=result['candidate'],actual_Q_created=False),allow_nan=False))

"""Stdlib complete SOURCE+explicit small saved META review; no candidate execution."""
import ast
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
P=B/'actual_complete_graph_helper_controls_v22_receipts';F=B/'actual_complete_graph_fresh_verifier_v22_receipts'
PP=P/'sealed_independent_actual_original_pure_protocol_review';FP=F/'sealed_independent_actual_complete_fresh_verifier_review'
C=HERE/'write_actual_joint_helper_admission_v22.FINAL.UNREADY.py';O=HERE/'original_V21_joint_Q_writer_FULL_SOURCE.py'
PN=P/'Root_actual_pure_protocol_summary.json';FN=F/'Root_actual_fresh_verifier_summary.json'
PR=PP/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_REVIEW.json';FR=FP/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_REVIEW.json'
PS=PP/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL.json';FS=FP/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_SEAL.json'
PT=PP/'ACTUAL_PURE_PROTOCOL_META_PEER_AUDIT_TOOL_RETURN.json';FT=FP/'ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN.json'
PST=PP/'ACTUAL_PURE_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json';FST=FP/'ACTUAL_COMPLETE_FRESH_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json'
PC=P/'Root_actual_pure_protocol_saved_review_install_record.json';FC=F/'Root_actual_full_fresh_verifier_saved_review_install_record.json'
BR=B/'actual_complete_graph_helper_controls_v22_sources/sealed_full_qualification_ROOT_BOUND_SOURCE/ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json'
INPUTS=[C,O,PN,FN,PR,FR,PS,FS,PT,FT,PST,FST,PC,FC,BR]
CHECKS=[]
def check(name,value,evidence=None):
 assert type(value)is bool;CHECKS.append(dict(check=name,PASS=value,evidence=evidence));assert value,name
def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];b=p.read_bytes();t=p.lstat();z=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];assert a==z and len(b)==a[4]
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=a)
before=[pin(p)for p in INPUTS];src=C.read_text();old=O.read_text();restored=src
for name in ('FINAL_EXACT_SAVED_META_EXPECTED_SHA_FULL_SOURCE_INVERSE.json','EXACT_FRESH_SAVED_META_COMPLETE_FULL_SOURCE_INVERSE.json','EXACT_PURE_SAVED_META_FULL_SOURCE_INVERSE.json'):
 proof=json.loads((HERE/name).read_bytes());check('complete inverse candidate SHA '+name,hashlib.sha256(restored.encode()).hexdigest()==proof['candidate_sha256'])
 for i,h in reversed(list(enumerate(proof['complete_finite_hunks']))):check('full finite inverse '+name+'/'+str(i),restored.count(h['new'])==1);restored=restored.replace(h['new'],h['old'],1)
 check('full finite inverse parent bytes SHA '+name,hashlib.sha256(restored.encode()).hexdigest()==proof['parent_sha256'])
base=json.loads((HERE/'FULL_WRITER_SOURCE_INVERSE.json').read_bytes());check('base exact dc816',hashlib.sha256(restored.encode()).hexdigest()==base['candidate']['sha256']);parts=restored[len(base['new_header_full_utf8']):].split(base['new_helpers_full_utf8']+'\ndef main():\n    require_bound_saved_reviews()\n');check('main metadata wrapper exact',len(parts)==2);prefix,body=parts;footer="\nif __name__ == '__main__':\n    main()\n";check('main footer exact',body.endswith(footer));body=body[:-len(footer)];restored=prefix+''.join(line[4:]if line.strip()else line for line in body.splitlines(keepends=True))
for i,h in reversed(list(enumerate(base['retarget_and_required_new_contract_hunks']))):check('all original41 full Source inverse '+str(i),restored.count(h['new'])==1);restored=restored.replace(h['new'],h['old'],1)
check('entire final Source byteinverse a732',restored==old and hashlib.sha256(restored.encode()).hexdigest()=='a7324201063e968fcd7c9f7f0728722824b248bab065652de0d34985db5e6b22')
check('entire final Source ASTinverse a732',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
tree=ast.parse(src);ot=ast.parse(old);nf={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};of={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)}
for k,v in of.items():check('original7 function entire AST+bytes '+k,ast.dump(v,include_attributes=False)==ast.dump(nf[k],include_attributes=False)and ast.get_source_segment(old,v)==ast.get_source_segment(src,nf[k]))
oa=next(n.value for n in ot.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets));na=next(n.value for n in nf['main'].body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='admission'for t in n.targets));ok=[k.value for k in oa.keys];nk=[k.value for k in na.keys];check('complete old Q top contract fields allretained',set(ok)<=set(nk));ofs=oa.values[ok.index('complete_current_graph_fresh_verifier')];nfs=na.values[nk.index('complete_current_graph_fresh_verifier')];check('complete old fresh Q nested contract fields allretained',{k.value for k in ofs.keys}<={k.value for k in nfs.keys})
gg={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check('explicit UNREADY never creates Q',ast.literal_eval(gg['WRITER_SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22')
check('both exact new peer field shapes Source adapted',ast.literal_eval(gg['ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED'])is True)
for k in ast.literal_eval(gg['REQUIRED_FUTURE_BINDING_FIELDS']):check('all actual future Root bindings remain None '+k,ast.literal_eval(gg[k])is None)
known=ast.literal_eval(gg['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']);expected={'PURE_PEER_SHA256':before[4]['sha256'],'FRESH_PEER_SHA256':before[5]['sha256'],'PURE_PEER_SEAL_SHA256':before[6]['sha256'],'FRESH_PEER_SEAL_SHA256':before[7]['sha256'],'PURE_PEER_TOOL_SHA256':before[8]['sha256'],'FRESH_PEER_TOOL_SHA256':before[9]['sha256'],'PURE_PEER_SEAL_TOOL_SHA256':before[10]['sha256'],'FRESH_PEER_SEAL_TOOL_SHA256':before[11]['sha256']}
check('all8 new actual saved-META expectedSHA exact',known==expected)
check('first main action strong status/None Rootbind guard',isinstance(nf['main'].body[0],ast.Expr)and isinstance(nf['main'].body[0].value,ast.Call)and nf['main'].body[0].value.func.id=='require_bound_saved_reviews')
for k in ('pure','fresh'):
 d=json.loads((PN if k=='pure'else FN).read_bytes());check('exact two actual new V22 summary schema '+k,d['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1');check('snapshot review false/QNone retained '+k,d['independent_saved_actual_review_pass']is False and d['actual_new_helper_qualification_sha256']is None)
for name,path,schema,count in [('pure',PR,'INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1',1084),('fresh',FR,'INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1',686)]:
 d=json.loads(path.read_bytes());check('actual new savedpeer schema '+name,d['schema']==schema);check('complete typedtrue '+str(count)+' savedchecks '+name,d['PASS']is True and d['hard_blockers']==[]and type(d['check_count'])is int and d['check_count']==len(d['checks'])==count and all(type(x['PASS'])is bool and x['PASS']is True for x in d['checks']))
pr=json.loads(PR.read_bytes());fr=json.loads(FR.read_bytes());ps=json.loads(PS.read_bytes());fs=json.loads(FS.read_bytes());pt=json.loads(PT.read_bytes());ft=json.loads(FT.read_bytes());pst=json.loads(PST.read_bytes());fst=json.loads(FST.read_bytes())
check('new pure bfea93 raw tr strict0 no session',pt['chunk_id']=='bfea93'and type(pt['exit_code'])is int and pt['exit_code']==0 and'session_id'not in pt)
check('new fresh722af0 wrapped tr strict0closed',ft['closed']is True and ft['terminal_tool_return']['chunk_id']=='722af0'and type(ft['terminal_tool_return']['exit_code'])is int and ft['terminal_tool_return']['exit_code']==0 and'session_id'not in ft['terminal_tool_return'])
for name,seal,tr,tool,chunk in [('pure',ps,pt,pst,'28f447'),('fresh',fs,ft['terminal_tool_return'],fst,'407e5a')]:
 check('actual new seal audit exactlyfull raw '+name,seal['actual_peer_audit_tool_return']==tr and seal['actual_peer_closed']is True and type(seal['actual_peer_exit_code'])is int and seal['actual_peer_exit_code']==0)
 check('actual new seal tool strict0closed '+name,tool['closed']is True and tool['terminal_tool_return']['chunk_id']==chunk and type(tool['terminal_tool_return']['exit_code'])is int and tool['terminal_tool_return']['exit_code']==0 and'session_id'not in tool['terminal_tool_return'])
check('all27 fields and three fullgzips retained',len(fr['all27_return_fields'])==27 and len(fr['all_three_complete_gzip_pins'])==3 and fs['all27_fields_three_complete_gzip_streams_and37112_actual_records_retained']is True and all(x['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and x['no_fields_or_records_filtered']is True for x in fr['all_three_complete_gzip_pins'].values()))
check('fullfresh112reads41unique unchanged',len(fr['complete_full_EOF_reads'])==112 and len(fr['unique_complete_fresh_rechecked_input_pins'])==41 and fs['unique_explicit_Source_META_inputs_rechecked_at_seal']==41)
check('fullfresh actualprivate4positive3reject retained',len(fr['actual_private_trace_controls']['positive_controls'])==4 and len(fr['actual_private_trace_controls']['rejections'])==3 and fs['original_full_graph_private_trace4positive3reject_and_original_caps_kept']is True)
check('Root sourcebinding record actual5cdf fullpin',before[14]['sha256']=='5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3'and before[14]['identity']==[16777229,49400000,33188,1,16493,1791600978260704687,1791600978260713937])
ledger=fr['original_archive_full_HODE_scope'];check('fresh actualDHO and original fullHODE distinct',ledger['Root_saved_DHO_ledger_bytes']==1611101 and ledger['original_business_post_result_HODE_bytes']==1620310 and ledger['peer_current_full_HODE_bytes']==1664302 and ledger['Root_DHO_ledger_is_not_original_HODE_scope']is True and ledger['original_normal_guard_scope']==['H','O','D','E'])
check('sample and own peaks distinct truthful',fr['genuine_watchdog_sampled_peak_rss_mib']==345.390625 and fr['driver_own_peak_rss_mib']==355.1875 and fr['driver_own_peak_rss_bytes']==372441088)
check('all old/current physics scope honest savedpeer',fr['new_Q']is None and pr['new_Q']is None and fr['helper_metadata_qualification_receipt_created']is False and pr['full_current_graph_verifier_qualified']is False and all(fr[x]is False for x in ('complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')))
for path,want,n in [(PC,'ROOT_V22_ACTUAL_COMPLETE_PURE_SAVED_META_PEER_COPY_V1',10),(FC,'ROOT_V22_ACTUAL_COMPLETE_FRESH_SAVED_META_PEER_COPY_V1',11)]:
 d=json.loads(path.read_bytes());check('actual Root whole copiedpeer schema/count '+str(n),d['schema']==want and type(d['file_count'])is int and d['file_count']==len(d['copied_files'])==n and d['actual_new_helper_Q']is None)
 for key,row in d['copied_files'].items():
  check('complete actual Root peer copy SHA same '+key,row['original']['sha256']==row['copied']['sha256']and row['original']['size_bytes']==row['copied']['size_bytes']);check('actual Root peer copiedfile fullEOF SHA7ID '+key,pin(Path(row['copied']['path']))==row['copied'])
for key in ('validate_terminal_v22','validate_summary_v22','validate_private_owner_controls','exact_META','validate_pure_saved_review_v22','validate_pure_saved_seal_v22','validate_fresh_saved_review_v22','validate_fresh_saved_seal_v22'):check('new finite actual Sourcevalidator '+key,key in nf)
for value in ('60','600','1800','512','64 * 2**20','96 * 2**30','8 * 2**30','37112','37111','63379','175886','237767','62332','36776','owned_list_completely_cleared_after_success','first_valid_slot_None_after_original_validate_and_append','full_json_types_order_floatbits_and_values_retained','SOURCE33_and_all_fixed_inputs_before_after_unchanged','legacy_SOURCE33_key_is_compatibility_alias_not_V22_source_count'):
 check('entire original/new resource and scope retained '+value,value in src)
after=[pin(p)for p in INPUTS];check('all exact Source/savedMETA fullEOF SHA7ID stable beforeafter',before==after)
for p in sorted(HERE.iterdir()):
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));check('complete Source AST no execution '+p.name,True)
result=dict(schema='V22_COMPLETE_EXACT_ACTUAL_SAVED_META_Q_WRITER_UNREADY_SOURCE_SELF_REVIEW_V1',status='SOURCE_ONLY_PASS_COMPLETE_UNREADY_ACTUAL_ROOT_ARCHIVE_BINDINGS_REQUIRED',source_only=True,PASS=True,hard_blockers=[],check_count=len(CHECKS),checks=CHECKS,complete_bounded_Source_META_before=before,complete_bounded_Source_META_after=after,entire_original_writer_byte_AST_inverse=True,original7functions_bytes_AST_exact=True,full_Q_constructor_contract_retained=True,both_new_V22_saved_review_shapes_exact=True,actual_archived_bindings_not_activated=True,new_Q_created=False,candidate_writer_or_Project_API_executed=False,ART_graph_or_numeric_payload_read=False,Root_Project_canonical_D_E_written=False)
with(HERE/'COMPLETE_SOURCE_SELF_REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,status=result['status'],check_count=len(CHECKS),report=pin(HERE/'COMPLETE_SOURCE_SELF_REVIEW.json'),candidate=before[0],new_Q_created=False)))

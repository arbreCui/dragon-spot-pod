"""Independent bounded Source/explicit saved META audit. Does not execute target code."""
import ast,hashlib,json,math,stat,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
PACK=Path('/private/tmp/axmat_v22_joint_helper_Q_UNREADY_SOURCE_design_20261010_s3vgnwa3')
EXPECTED_MANIFEST='3fd6fe5c2922dbf041985c3aca05c1c501e9f7fafc384a663af9bfa3f405ac91'
EXPECTED_WRITER='59590a6f123d26519fd68e7f9042c44c9fb3e1c1c477470728b1765789efc444'
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
P=B/'actual_complete_graph_helper_controls_v22_receipts';F=B/'actual_complete_graph_fresh_verifier_v22_receipts'
PP=P/'sealed_independent_actual_original_pure_protocol_review';FP=F/'sealed_independent_actual_complete_fresh_verifier_review'
CHECKS=[];PINS={};BLOCKERS=[]
def check(name,v,evidence=None):
 if type(v)is not bool:raise TypeError(name)
 CHECKS.append({'check':name,'PASS':v,'evidence':evidence})
 if not v:BLOCKERS.append(name)
def must(name,v,evidence=None):
 check(name,v,evidence)
 if not v:raise ValueError(name)
def id7(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(p):
 p=Path(p);a=id7(p);must('regular explicit Source/META '+str(p),stat.S_ISREG(a[2]) and not p.is_symlink())
 h=hashlib.sha256();n=0
 with p.open('rb')as f:
  while True:
   b=f.read(1048576)
   if not b:break
   n+=len(b);h.update(b)
 must('complete EOF and stable stat7 '+str(p),n==a[4] and id7(p)==a)
 pin={'path':str(p),'sha256':h.hexdigest(),'size_bytes':n,'identity':a}
 if str(p)in PINS:must('same repeat full pin '+str(p),PINS[str(p)]==pin)
 PINS[str(p)]=pin;return pin
def pairs(items):
 out={}
 for k,v in items:
  if k in out:raise ValueError('duplicate META key '+k)
  out[k]=v
 return out
def bad(v):raise ValueError('nonfinite META '+v)
def read(p,sha=None):
 pin=fullpin(p)
 if sha is not None:must('exact declared SHA '+str(p),pin['sha256']==sha)
 d=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)
 must('JSON read stable '+str(p),id7(Path(p))==pin['identity'])
 return d
def exact(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return list(a)==list(b) and all(exact(a[k],b[k])for k in a)
 if type(a)in (list,tuple):return len(a)==len(b) and all(exact(x,y)for x,y in zip(a,b))
 if type(a)is float:return math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
 return a==b
def literal_globals(tree):
 d={}
 for n in tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:d[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
 return d
def assignment(nodes,name):return next(n.value for n in nodes if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
def dictkeys(node):return [k.value for k in node.keys]
def schema_and_closed(d,schema,chunk,init=None,session=None):
 must('actual terminal schema '+chunk,d['schema']==schema)
 must('actual terminal closed observed no repoll '+chunk,d['closed']is True and d['actual_tool_terminal_return_observed']is True and d['session_repolled_after_close']is False)
 t=d['terminal_tool_return'];must('actual strict integer0 no session '+chunk,t['chunk_id']==chunk and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t)
 if init is not None:must('actual own original session '+chunk,d['initial_tool_return']['chunk_id']==init and type(d['initial_tool_return']['session_id'])is int and d['initial_tool_return']['session_id']==session)
 must('actual elapsed finite typed '+chunk,type(t['wall_time_seconds'])in(int,float)and math.isfinite(t['wall_time_seconds'])and t['wall_time_seconds']>=0 and type(t['output'])is str)
 return t
manifest=read(PACK/'MANIFEST.json',EXPECTED_MANIFEST)
must('complete sealed30 members822475',type(manifest['members'])is dict and len(manifest['members'])==manifest['member_count_excluding_this_manifest']==30 and sum(x['size_bytes']for x in manifest['members'].values())==manifest['member_bytes_excluding_this_manifest']==822475)
members={}
for rel,entry in manifest['members'].items():
 q=PACK/rel;actual=fullpin(q);must('entire sealed member SHA7ID '+rel,actual==entry);members[rel]=q.read_bytes()
must('all31 sealed file names exact', {str(x.relative_to(PACK))for x in PACK.rglob('*')if x.is_file()}==set(members)|{'MANIFEST.json'})
pytrees={}
for rel,raw in members.items():
 if rel.endswith('.py'):pytrees[rel]=ast.parse(raw,filename=str(PACK/rel));check('whole Source AST parsed no execution '+rel,True)
text=members['write_actual_joint_helper_admission_v22.FINAL.UNREADY.py'].decode();tree=pytrees['write_actual_joint_helper_admission_v22.FINAL.UNREADY.py'];old=members['original_V21_joint_Q_writer_FULL_SOURCE.py'].decode();ot=pytrees['original_V21_joint_Q_writer_FULL_SOURCE.py']
must('fixed final writer42882 SHA59590a',len(text.encode())==42882 and hashlib.sha256(text.encode()).hexdigest()==EXPECTED_WRITER)
restored=text;inverse_counts=[]
for rel in ['FINAL_EXACT_SAVED_META_EXPECTED_SHA_FULL_SOURCE_INVERSE.json','EXACT_FRESH_SAVED_META_COMPLETE_FULL_SOURCE_INVERSE.json','EXACT_PURE_SAVED_META_FULL_SOURCE_INVERSE.json']:
 proof=json.loads(members[rel]);must('exact inverse initial SHA '+rel,hashlib.sha256(restored.encode()).hexdigest()==proof['candidate_sha256'])
 for i,h in reversed(list(enumerate(proof['complete_finite_hunks']))):
  must('unique exact full inverse hunk '+rel+'/'+str(i),restored.count(h['new'])==1)
  restored=restored.replace(h['new'],h['old'],1)
 must('exact inverse parent SHA '+rel,hashlib.sha256(restored.encode()).hexdigest()==proof['parent_sha256'])
 parent=Path(proof['parent_path']);must('exact inverse actual parent bytes '+rel,restored.encode()==members[parent.name])
 inverse_counts.append(len(proof['complete_finite_hunks']))
base=json.loads(members['FULL_WRITER_SOURCE_INVERSE.json']);must('inverse dc816 actual initial SHA',hashlib.sha256(restored.encode()).hexdigest()==base['candidate']['sha256'])
head=base['new_header_full_utf8'];helpers=base['new_helpers_full_utf8'];must('disclosed exact Source header',restored.startswith(head))
restored=restored[len(head):];split=helpers+'\ndef main():\n    require_bound_saved_reviews()\n';must('single disclosed helpers and main guard wrapper',restored.count(split)==1)
prefix,body=restored.split(split);footer="\nif __name__ == '__main__':\n    main()\n";must('exact disclosed main footer',body.endswith(footer));body=body[:-len(footer)]
must('only whole original block indentation',all(not line.strip()or line.startswith('    ')for line in body.splitlines()))
restored=prefix+''.join(line[4:]if line.strip()else line for line in body.splitlines(keepends=True))
for i,h in reversed(list(enumerate(base['retarget_and_required_new_contract_hunks']))):
 must('complete original41 unique inverse '+str(i),restored.count(h['new'])==1)
 restored=restored.replace(h['new'],h['old'],1)
must('entire final full byte inverse a732',restored==old and hashlib.sha256(restored.encode()).hexdigest()=='a7324201063e968fcd7c9f7f0728722824b248bab065652de0d34985db5e6b22')
must('entire full AST inverse a732',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ot,include_attributes=False))
actual_parent=fullpin(Path(base['parent']['path']));must('original actual Source a732 fullpin',actual_parent==base['parent']);must('original actual Source fullbytes copied',Path(base['parent']['path']).read_bytes()==old.encode())
nf={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};of={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)}
must('actual17 writer defs and original7',len(nf)==17 and len(of)==7)
for name,node in of.items():must('entire original function AST and bytes preserved '+name,ast.dump(node,include_attributes=False)==ast.dump(nf[name],include_attributes=False)and ast.get_source_segment(old,node)==ast.get_source_segment(text,nf[name]))
g=literal_globals(tree);required=g['REQUIRED_FUTURE_BINDING_FIELDS'];must('exact19 distinct required bindings',len(required)==len(set(required))==19)
for name in required:must('future Root binding None '+name,name in g and g[name]is None)
must('UNREADY strong first guard and optimized Python rejected',g['WRITER_SOURCE_STATUS']=='UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22' and ast.unparse(nf['main'].body[0])=='require_bound_saved_reviews()'and 'assert not sys.flags.optimize and not os.environ.get' in ast.get_source_segment(text,nf['require_bound_saved_reviews']))
must('no target business/helper/guard imports',all(n.module in {'pathlib'} for n in tree.body if isinstance(n,ast.ImportFrom)) and all(a.name in {'math','struct','os','sys','hashlib','json','stat'}for n in tree.body if isinstance(n,ast.Import)for a in n.names))
must('all META side effects inside main or functions except stdlib path/literal constructors',all(isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))or isinstance(n,ast.Expr)and isinstance(n.value,ast.Constant)or isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'" for n in tree.body))
must('exclusive new Q write Source retained',"with Q.open('x') as f:"in text and 'assert not Q.exists()'in text)
oa=assignment(ot.body,'admission');na=assignment(nf['main'].body,'admission');ok=dictkeys(oa);nk=dictkeys(na)
must('whole old Q constructor fields all retained',set(ok)<=set(nk) and len(nk)==len(set(nk)))
for field in ['full_protocol','original_caps','actual_measurement','complete_current_graph_fresh_verifier']:
 if field=='full_protocol':a=assignment(ot.body,field);b=assignment(nf['main'].body,field)
 elif field=='original_caps':a=assignment(ot.body,field);b=assignment(nf['main'].body,field)
 else:a=oa.values[ok.index(field)];b=na.values[nk.index(field)]
 must('complete old nested constructor retained '+field,set(dictkeys(a))<=set(dictkeys(b)))
 if field=='original_caps':must('whole original60 caps entire AST exact',ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))
falsekeys=['supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified']
for name in falsekeys:must('new Q business/physics flag literalFalse '+name,ast.literal_eval(na.values[nk.index(name)])is False)
refs={
 'pure_summary':(P/'Root_actual_pure_protocol_summary.json','f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4'),
 'fresh_summary':(F/'Root_actual_fresh_verifier_summary.json','fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e'),
 'pure_term':(P/'Root_actual_pure_protocol_tool_terminal_return.json','12d8bbdef3cd59c2f9889d507cf8e5e646f37f4d7e0df1649381373c82100e78'),
 'fresh_term':(F/'Root_actual_fresh_verifier_tool_terminal_return.json','de3750d802a442329089c5301d36939bda610ddc88bc7770dbe0c0f7f65a76f4'),
 'pure_peer':(PP/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_REVIEW.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['PURE_PEER_SHA256']),
 'pure_peer_tool':(PP/'ACTUAL_PURE_PROTOCOL_META_PEER_AUDIT_TOOL_RETURN.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['PURE_PEER_TOOL_SHA256']),
 'pure_peer_seal':(PP/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['PURE_PEER_SEAL_SHA256']),
 'pure_peer_seal_tool':(PP/'ACTUAL_PURE_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['PURE_PEER_SEAL_TOOL_SHA256']),
 'fresh_peer':(FP/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_REVIEW.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['FRESH_PEER_SHA256']),
 'fresh_peer_tool':(FP/'ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['FRESH_PEER_TOOL_SHA256']),
 'fresh_peer_seal':(FP/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_SEAL.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['FRESH_PEER_SEAL_SHA256']),
 'fresh_peer_seal_tool':(FP/'ACTUAL_COMPLETE_FRESH_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']['FRESH_PEER_SEAL_TOOL_SHA256']),
 'binding':(B/'actual_complete_graph_helper_controls_v22_sources/sealed_full_qualification_ROOT_BOUND_SOURCE/ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json','5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3'),
 'pure_report':(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010/ACTUAL_REPORT.json'),'68a4fe6ca874a767221cf850bc2b37c33f8143613a56061b15c46c947a7cb4f5'),
 'fresh_report':(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v22-20261010/ACTUAL_REPORT.json'),'bfd366a07fe897d210c61efc8c9aefdfa89add814ef210273ef97f2f10569976'),
 'pure_small':(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010/small_codec_and_rejection_controls.json'),None),
 'pure_fixture':(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010/small_fixture_controls.json'),None)}
docs={k:read(p,h)for k,(p,h)in refs.items()}
must('actual Root binding Source native7ID exact',PINS[str(refs['binding'][0])]['identity']==[16777229,49400000,33188,1,16493,1791600978260704687,1791600978260713937])
pt=schema_and_closed(docs['pure_term'],'ROOT_V22_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1','6f6847','86ab9d',74949)
ft=schema_and_closed(docs['fresh_term'],'ROOT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_TOOL_TERMINAL_RETURN_V1','57a6f5','55ef8e',29568)
for label,kind,whole,stage in [('pure_summary','PURE',60,60),('fresh_summary','FRESH',1800,600)]:
 d=docs[label];must('new actual summary exact schema/status '+kind,d['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1'and d['status']=='ACTUAL_EXIT0_CLOSED_COMPLETE_'+kind+'_CONTROLS_SAVED_REVIEW_REQUIRED')
 must('actual summary closed typedint0 '+kind,d['closed']is True and type(d['actual_Root_exit_code'])is int and d['actual_Root_exit_code']==0)
 must('snapshot peerFalse/QNone preserved '+kind,d['independent_saved_actual_review_pass']is False and d['actual_new_helper_qualification_sha256']is None)
 must('all Source before_after true and actualcounts typed '+kind,d['all_source_files_before_after_exact']is True and type(d['source_file_count'])is int and d['source_file_count']>0 and type(d['host_input_sources_and_original_helper_resource_factory_post_close_exact'])is int and d['host_input_sources_and_original_helper_resource_factory_post_close_exact']>0)
 must('real separate childstderr false/merged true '+kind,d['separate_child_stderr_capture_verified']is False and d['child_stdout_stderr_merge_is_original_normal_guard']is True)
 must('original caps exact '+kind,d['whole_seconds_cap']==whole and d['stage_seconds_cap']==stage and d['rss_mib_cap']==512 and d['archive_bytes_cap']==64*2**20 and d['history_bytes_cap']==96*2**30 and d['free_bytes_floor']==8*2**30 and d['threads']==d['children']==1 and d['retries']==0)
 for key,cap in [('whole_seconds',whole),('child_seconds',stage),('sampled_peak_rss_mib',512)]:must('new actual finite within cap '+kind+'/'+key,type(d[key])in(int,float)and math.isfinite(d[key])and 0<=d[key]<cap)
 for key in ['whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified']:must('actual summary scopeFalse '+kind+'/'+key,d[key]is False)
 for key in ['actual_external_Root_terminal','source_namespace_freeze','complete_namespace_manifest','actual_host_result','actual_control_report','actual_watchdog','actual_control_child_merged_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr']:
  entry=d[key];must('declared summary fullpin metadata shape '+kind+'/'+key,type(entry['identity'])is list and len(entry['identity'])==7 and all(type(v)is int for v in entry['identity'])and entry.get('size_bytes',entry['identity'][4])==entry['identity'][4]and len(entry['sha256'])==64)
pr=docs['pure_peer'];fr=docs['fresh_peer'];ps=docs['pure_peer_seal'];fs=docs['fresh_peer_seal'];p_report=docs['pure_report'];f_report=docs['fresh_report'];p_summary=docs['pure_summary'];f_summary=docs['fresh_summary']
for d,schema,count,name in [(pr,'INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1',1084,'pure'),(fr,'INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1',686,'fresh')]:
 must('actual savedpeer full schema '+name,d['schema']==schema)
 must('complete savedpeer typedtruechecks '+name,d['PASS']is True and d['hard_blockers']==[]and type(d['check_count'])is int and d['check_count']==len(d['checks'])==count and all(type(x['PASS'])is bool and x['PASS']is True for x in d['checks']))
 must('actual peer namespace 4labels '+name,[x['label']for x in d['complete_namespace_snapshots']]==['D','H','O','E_pre_summary'])
 must('actual peer no newQ '+name,d['new_Q']is None)
pure_raw=docs['pure_peer_tool'];fresh_raw=docs['fresh_peer_tool']['terminal_tool_return']
for raw,chunk in [(pure_raw,'bfea93'),(fresh_raw,'722af0')]:must('actual peer exact strict closed terminal '+chunk,raw['chunk_id']==chunk and type(raw['exit_code'])is int and raw['exit_code']==0 and 'session_id'not in raw)
must('fresh actualwrapped peer schema/closed',docs['fresh_peer_tool']['schema']=='INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN_V1'and docs['fresh_peer_tool']['closed']is True)
for s,t,a,chunk,schema in [(ps,docs['pure_peer_seal_tool'],pure_raw,'28f447','INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL_TOOL_RETURN_V1'),(fs,docs['fresh_peer_seal_tool'],fresh_raw,'407e5a','INDEPENDENT_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_META_PEER_SEAL_TOOL_RETURN_V1')]:
 must('actual peerseal exactaudit no selfcycle '+chunk,exact(s['actual_peer_audit_tool_return'],a)and s['actual_peer_closed']is True and type(s['actual_peer_exit_code'])is int and s['actual_peer_exit_code']==0)
 must('actual seal real terminal schema0closed '+chunk,t['schema']==schema and t['closed']is True and t['terminal_tool_return']['chunk_id']==chunk and type(t['terminal_tool_return']['exit_code'])is int and t['terminal_tool_return']['exit_code']==0 and 'session_id'not in t['terminal_tool_return'])
must('actual peer+summary references raw terminal type/order/floatbits exact',exact(pr['actual_Root_pure_tool_receipt'],docs['pure_term'])and exact(fr['actual_Root_terminal_tool_return'],ft)and fr['actual_Root_fresh_tool_receipt']==PINS[str(refs['fresh_term'][0])])
helper_actual=fullpin(Path(p_summary['installed_helper']['path']))
for label,d in [('pure',p_summary),('fresh',f_summary)]:
 ep=d['installed_helper'];must('same current helper cf0 normalized actualSource pin '+label,all(ep[k]==helper_actual[k]for k in ('path','sha256','identity'))and ep.get('size_bytes',ep.get('source_bytes'))==helper_actual['size_bytes']==148965 and helper_actual['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c')
must('actual fresh full report summary exact',exact(f_report,f_summary['complete_actual_report']))
must('original source61+13 counts not cropped to old33',p_summary['source_file_count']==61 and f_summary['source_file_count']==13 and "'complete_source_member_count': fresh['source_file_count']"in text and "'legacy_SOURCE33_key_is_compatibility_alias_not_V22_source_count': True"in text)
owner=p_report['private_owner_consume_controls'];must('owner actualreport/summary exact',exact(owner,p_summary['private_owner_consume_controls']))
must('owner correct schema/status',owner['schema']=='AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1'and owner['status']=='ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY')
for key,wanted in [('positive_controls',['default_list','default_tuple','explicit_False_list','owned_builtin_list_True']),('private_guard_rejections',['nonbool_consume','tuple_True','list_subclass_True']),('accepted_str_subclass_equivalence_controls',['plain_accepted_str','accepted_str_with_str_override']),('partial_invalid_second_owner_rejections',['invalid_second_owner_default','invalid_second_owner_owned_True'])]:must('owner complete orderedcontrols '+key,[x['case']for x in owner[key]]==wanted)
for row in owner['positive_controls']:
 must('owner fullnormalized retained '+row['case'],row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default']is True and exact(row['expected_complete_descriptor_signature'],row['actual_complete_descriptor_signature']))
 key='owned_list_completely_cleared_after_success'if row['case']=='owned_builtin_list_True'else 'caller_full_identity_type_order_value_attrs_floatbits_unchanged';must('owner correct ownership '+row['case'],row[key]is True)
for row in owner['private_guard_rejections']:must('owner full rejected unchanged '+row['case'],row['class']=='InputGraphError'and row['message']=='private owner consume needs a bool and an exclusively owned builtin list'and row['caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True)
for row in owner['accepted_str_subclass_equivalence_controls']:must('owner subtype complete equivalence '+row['case'],row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True and row['owned_list_completely_cleared_after_success']is True and row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default']is True and exact(row['expected_complete_descriptor_signature'],row['actual_complete_descriptor_signature']))
for key in ['first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created']:must('partial-owner original semantic receipt '+key,owner[key]is True)
must('partial invalidsecond exact errors',all(x['class']=='InputGraphError'and x['message']=='missing file owner'for x in owner['partial_invalid_second_owner_rejections']))
must('owner no actualQ/science receipt',owner['new_helper_qualification_created']is False and owner['business_or_science_qualification_created']is False)
oldmeta=p_report['full_old_saved_graph'];orig=oldmeta['complete_original_metadata'];counts=orig['complete_counts'];tr=p_report['full_new_creation_trace'];small=docs['pure_small'];fixture=docs['pure_fixture'];savedowner=pr['original_and_new_complete_controls']
must('all5 original stages ordered full', [x['stage']for x in p_report['stages']]==['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged'])
must('full old graph two entrances exact typeorderfloatbits',exact(orig,oldmeta['normal_strict_file_entrance_full_semantics_and_counts'])and exact(orig,oldmeta['normal_strict_payload_entrance_full_semantics_and_counts']))
must('complete old graph countscope exact',counts['canonical_files']==36776 and counts['requirements']==237767 and counts['read_trace_records']==62332 and exact(counts,savedowner['complete_old_graph_counts']))
must('all original codec/fixture rejects not omitted',len(small['rejections'])==61 and len(fixture['rejections'])==37 and len(fixture['complete_rejected_arguments'])==18 and fixture['producer_full_exact_values_types_order_floatbits']is True)
must('full63379 creation trace175886 attempts intact',tr['full_record_count']==63379 and tr['actual_attempt_count']==175886 and all(tr[k]is True for k in ['exact_full_roundtrip','persisted_full_trace_exact_order_type_floatbit_inverse','default_source_nonmutation']))
for key,actualkey in [('new_owner_positive_controls','positive_controls'),('new_owner_guard_rejections','private_guard_rejections'),('new_owner_subtypes','accepted_str_subclass_equivalence_controls'),('new_owner_invalid_second_rejections','partial_invalid_second_owner_rejections')]:must('saved peer owner proof full equality '+key,exact(savedowner[key],owner[actualkey]))
p_ledger=pr['archive_ledger_scope'];must('pure original ledger distinction complete',p_ledger['joint_scope']==['D','H','O']and p_ledger['original_normal_guard_regular_file_bytes']==61013090 and p_ledger['conservative_META_extra_symlink_literal_bytes']==38 and p_ledger['Root_saved_META_total_DHO_bytes']==p_summary['joint_source_host_out_bytes']==61013128 and p_ledger['cap_bytes']==64*2**20)
must('pure full EOF193 rows117 unique not truncation',len(pr['complete_full_EOF_reads'])==193 and len({x['path']for x in pr['complete_full_EOF_reads']})==117 and ps['all_unique_explicit_Source_META_inputs_second_complete_EOF_SHA7ID_unchanged']==117)
must('fresh full EOF112 rows41 unique sealed',len(fr['complete_full_EOF_reads'])==112 and len(fr['unique_complete_fresh_rechecked_input_pins'])==41 and fs['unique_explicit_Source_META_inputs_rechecked_at_seal']==41)
must('all27 fields complete ordered equality',len(fr['all27_return_fields'])==27 and exact(fr['all27_return_fields'],f_report['complete_return_fields_retained'])and fs['all27_fields_three_complete_gzip_streams_and37112_actual_records_retained']is True)
must('actual37112 fullread trace unfiltered',f_report['actual_complete_trace_counts']=={'records':37112,'attempts':37112,'canonical_files':37111,'external_graph_reads':1,'no_subprocess_reexecuted':True}and fr['unfiltered37112trace_complete_order_path_sequence_sha256']=='54e9a6fe108093c2f92d31c8c2c5e38e0cad153ee170eafc8e59c44fa6d99a30')
must('actual fresh graphcounts and privatecontrols full exact',exact(fr['complete_saved_graph_counts_and_fields'],f_report['independent_full_saved_graph_metadata'])and exact(fr['actual_private_trace_controls'],f_report['private_trace_controls']))
controls=fr['actual_private_trace_controls'];must('actual trace4positive3reject full scope', [x['case']for x in controls['positive_controls']]==['default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True']and [x['case']for x in controls['rejections']]==['nonbool_consume','tuple_True','list_subclass_True']and controls['augmented_records_are_not_claimed_as_actual_full_verifier_trace']is True and controls['old60pure_control_functions_not_changed']is True)
for row in controls['positive_controls']:must('trace full values retained '+row['case'],row['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd']is True and row['owned_list_completely_cleared'if row['case']=='probe_owned_builtin_list_True'else'caller_full_identity_type_order_value_floatbits_unchanged']is True)
for row in controls['rejections']:must('trace reject full unchanged '+row['case'],row['class_name']=='InputGraphError'and row['message']=='private trace consume needs a bool and an exclusively owned builtin list'and row['rejected']is True and row['caller_type_identity_nested_value_order_floatbits_unchanged']is True)
gz=fr['all_three_complete_gzip_pins'];must('3 complete gzip saved verifier no filtered records',list(gz)==['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace']and all(x['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and x['no_fields_or_records_filtered']is True for x in gz.values()))
must('expected actual gzip and uncompressed bytes hashes equal',gz['expected_complete_return_contract']['sha256']==gz['actual_complete_verifier_return']['sha256']and gz['expected_complete_return_contract']['uncompressed_JSON_sha256']==gz['actual_complete_verifier_return']['uncompressed_JSON_sha256']and gz['expected_complete_return_contract']['uncompressed_JSON_bytes']==gz['actual_complete_verifier_return']['uncompressed_JSON_bytes'])
for name,pin in gz.items():must('fullgzip reports same actual pin '+name,exact(pin,f_report[name]))
ledger=fr['original_archive_full_HODE_scope'];must('fresh full HODE originalclose and savedpeer scope distinct',ledger['original_normal_guard_scope']==['H','O','D','E']and ledger['Root_DHO_ledger_is_not_original_HODE_scope']is True and ledger['Root_saved_DHO_ledger_bytes']==1611101 and ledger['original_business_post_result_HODE_bytes']==1620310 and ledger['peer_current_full_HODE_bytes']==1664302)
must('genuine sample345.390625 and own355.1875 peaks distinct',fr['genuine_watchdog_sampled_peak_rss_mib']==f_summary['sampled_peak_rss_mib']==345.390625 and fr['driver_own_peak_rss_mib']==355.1875 and fr['driver_own_peak_rss_bytes']==372441088)
for name,d in [('purepeer',pr),('freshpeer',fr)]:must('savedpeer honest science onlyfalse '+name,d['new_Q']is None)
plan=json.loads(members['EXACT_FUTURE_CANONICAL_GENUINE_PREP_SOURCE_LOCATIONS.json']);minimal=json.loads(members['MINIMAL_COMPLETE_CANONICAL_PREP_SOURCE_ADAPTATION_PLAN.json'])
for name in ['canonical_parent','genuine_PREP_host_parent']:
 pin=fullpin(Path(plan[name]['path']));must('actual full Source parentplan '+name,pin==plan[name]and pin==minimal[name]);raw=Path(pin['path']).read_bytes();ast.parse(raw,filename=pin['path'])
 anchors=plan['canonical_exact_anchors'if name=='canonical_parent'else'host_exact_11_atomic_anchors'];must('all11 exact finite anchors '+name,len(anchors)==11)
 for row in anchors:must('source exact whole anchor '+name+'/'+str(row['line']),raw.decode().count(row['whole_exact_source_anchor'])==row['whole_source_occurrences']==1)
 if name=='canonical_parent':
  ptree=ast.parse(raw);must('all original70 canonical definitions actualSource',sum(isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))for x in ptree.body)==70)
  pg=literal_globals(ptree)
  for k in plan['six_future_business_pins']:must('all6 actual canonical business pins None '+k,pg[k]is None and plan['six_future_business_pins'][k]is None and minimal['six_future_business_pins'][k]is None)
 else:
  for token in ['512','600','1800','2*2**30','96*2**30','8*2**30']:
   check('genuine host original resource token retained '+token,token in raw.decode())
must('plan original caps1800/600/512/2GiB/history96/free8/1/1/0',minimal['business_caps']=={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'archive_bytes':2**31,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0})
must('plan no business candidates or fake future Q',minimal['actual_new_helper_Q_path']is None and minimal['actual_new_helper_Q_sha256']is None and minimal['new_runtime_candidate_authored']is False and plan['future_runtime_READY_source_sha256']is None and plan['future_new_joint_helper_Q_sha256']is None)
# Source shape audit: exact literal value[...] keys used by every newly added validator.
validator_docs={'validate_summary_v22':[p_summary,f_summary],'validate_private_owner_controls':[owner],'validate_pure_saved_review_v22':[pr],'validate_pure_saved_seal_v22':[ps],'validate_fresh_saved_review_v22':[fr],'validate_fresh_saved_seal_v22':[fs]}
for name,values in validator_docs.items():
 keys={n.slice.value for n in ast.walk(nf[name])if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='value'and isinstance(n.slice,ast.Constant)and isinstance(n.slice.value,str)}
 for d in values:must('all literal actual value keys exist '+name,keys<=set(d),sorted(keys))
# No input graph, material payload, decoded gzip, helper/API or target writer was opened/called.
startpins=list(PINS.values())
for pin in startpins:
 current=fullpin(Path(pin['path']));must('all finite Source/META inputs end fullEOF SHA7ID unchanged '+pin['path'],current==pin)
status='SOURCE_ONLY_PASS_UNREADY_TEMPLATE_REQUIRES_ACTUAL_ROOT_BINDING_REVIEW'if not BLOCKERS else'SOURCE_ONLY_BLOCKED'
result={'schema':'INDEPENDENT_V22_JOINT_HELPER_Q_WRITER_COMPLETE_SOURCE_META_REVIEW_V1','status':status,'PASS':not BLOCKERS,'source_only':True,'hard_blockers':BLOCKERS,'check_count':len(CHECKS),'checks':CHECKS,'qualified_Source_manifest_sha256':EXPECTED_MANIFEST,'qualified_UNREADY_writer_sha256':EXPECTED_WRITER,'full_input_pins':startpins,'full_inverse_hunk_counts':inverse_counts+[41],'original7functions_byte_AST_exact':True,'original_Q_constructor_contract_full_retained':True,'actual_writer_top_level_definition_count':17,'required_future_binding_count':19,'all19futurebindingsNone':True,'pure_actual_terminal':'6f6847','fresh_actual_terminal':'57a6f5','pure_saved_review_checks':1084,'fresh_saved_review_checks':686,'original_pure60caps_unchanged':True,'fresh1800whole600stage_caps_unchanged':True,'future_complete_PREP1800_600_512_2GiB_96GiB_free8_1_1_0_plan_unchanged':True,'reviewer_target_writer_or_helper_guard_API_executed':False,'graph_or_material_numeric_payload_read':False,'gzip_trace_or_result_payload_decompressed':False,'canonical_D_E_ART_Q_written':False,'new_Q':None,'whole_build_qualified':False,'whole_INPUT_admitted':False,'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False,'next_step':'Root may bind only the nineteen actual fields/status into a fresh Source derivative, retain complete inverse and actual Source tool return, then obtain independent bound-Source review before running the metadata writer.'}
(HERE/'REVIEW.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
(HERE/'REPORT.txt').write_text('SOURCE ONLY independent review of complete frozen V22 joint Q writer.\nStatus: '+status+'\nManifest3fd6/final59590a: all31 namespace files fullEOF SHA/stat7; all2/19/13/41 inverse plus disclosed header/helpers/main wrapper reconstruct originala732 byteexact/ASTexact; original7 functions and all old Q fields retained.\nActual nineteen Root bindings remain None, UNREADY guard runs before reads/writes; no Q created. Separate real pure6f6847/fresh57a6f5 terminals, two savedreview1084/686 and their own seal receipts bind new cf0 helper; oldQ29ac and old measurements not reused. Original5stage pure protocol, owner4/3/2/2, full27 current result/37112trace/3gzip saved evidence remain in contract.\nAll resource caps/scopes and false business/native/AAA/ABA/physical flags retained. Reviewer only read Source and explicit saved META, never executed target writer/API/guard/helper, decoded graph/gzip/material, or wrote project/D/E/ART/Q. Root bound Source remains a future independent review requirement.\n')
print(json.dumps({'package':str(HERE),'status':status,'checks':len(CHECKS),'hard_blockers':BLOCKERS,'source_META_inputs':len(startpins),'REVIEW_sha256':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest()}))

"""Bounded independent Source+literal saved META audit. Never executes target writer."""
import ast,hashlib,json,stat
from pathlib import Path
HERE=Path(__file__).resolve().parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_joint_helper_admission_v22_sources';E=B/'actual_joint_helper_admission_v22_receipts'
C=D/'write_actual_joint_helper_admission_v22.READY.py';R=D/'Root_actual_joint_Q_writer_Source_binding_record.json'
F=E/'Root_final_joint_Q_writer_SOURCE_freeze.json';T=E/'Root_actual_joint_Q_writer_Source_binding_tool_return.json'
CHECKS=[];PINS={}
def check(n,v):
 assert type(v)is bool;CHECKS.append({'check':n,'PASS':v});assert v,n
def id7(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=id7(p);check('regular Source/META '+str(p),stat.S_ISREG(a[2])and not p.is_symlink());h=hashlib.sha256();n=0
 with p.open('rb')as f:
  while True:
   b=f.read(1048576)
   if not b:break
   h.update(b);n+=len(b)
 check('full EOF stable exact7 '+str(p),n==a[4]and id7(p)==a)
 q={'path':str(p),'sha256':h.hexdigest(),'size_bytes':n,'identity':a}
 if str(p)in PINS:check('same repeated complete pin '+str(p),PINS[str(p)]==q)
 PINS[str(p)]=q;return q
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate META key '+k)
  d[k]=v
 return d
def bad(v):raise ValueError('nonfinite META '+v)
def read(p,sha=None):
 q=pin(p)
 if sha is not None:check('exact known SHA '+str(p),q['sha256']==sha)
 d=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad);check('JSON literal read7stable '+str(p),id7(Path(p))==q['identity']);return d
def globals_literal(tree):
 d={}
 for n in tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:d[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
 return d
freeze=read(F,'5d3c4276a6a98658a0c4ac6516cf2621fed299e3a294205bc8413ef83810a2f9')
record=read(R,'9909cc12367d8504bfd32e11914426c01b32f9f5dcc848d8a09aabaaf847150f')
receipt=read(T)
check('Source33files2dirs exact freeze',freeze['schema']=='ROOT_V22_FINAL_ACTUAL_JOINT_Q_WRITER_SOURCE_FREEZE_V1'and freeze['source_only']is True and freeze['file_count']==len(freeze['complete_files'])==33 and freeze['directory_count']==len(freeze['complete_directories'])==2 and freeze['no_Source_append_after_this_freeze']is True and freeze['Q_executed']is False and freeze['new_Q']is None)
for rel,expected in freeze['complete_files'].items():check('every frozen Source fullEOF SHA7ID '+rel,pin(D/rel)==expected)
for rel,expected in freeze['complete_directories'].items():check('every frozen directory stat7 '+rel,id7(D/rel)==expected)
observed={str(p.relative_to(D))for p in D.rglob('*')if p.is_file()};dirs={'.'}|{str(p.relative_to(D))for p in D.rglob('*')if p.is_dir()}
check('no frozen source members/directories added or removed',observed==set(freeze['complete_files'])and dirs==set(freeze['complete_directories']))
check('actual Source binding schema and scope',record['schema']=='ROOT_V22_ACTUAL_JOINT_HELPER_Q_WRITER_FINITE_SOURCE_BINDING_V1'and record['source_only']is True and record['actual_Q_created']is False and record['new_Q']is None and record['helper_guard_API_or_business_executed']is False and record['scientific_accuracy_qualified']is False and record['AAA_accuracy_qualified']is False and record['ABA_admitted']is False)
check('bound writer45738 SHA61d552 actualpin',pin(C)==record['bound_writer']and record['bound_writer']['sha256']=='61d552c4b2efe0334742c4d9ad1bf7cedd9558c49c66e9f51fdd25d611969b51'and record['bound_writer']['size_bytes']==45738)
oldpin=pin(Path(record['original_final_UNREADY_writer']['path']));check('original59590a fullpin stable',oldpin==record['original_final_UNREADY_writer']and oldpin['sha256']=='59590a6f123d26519fd68e7f9042c44c9fb3e1c1c477470728b1765789efc444')
old=Path(oldpin['path']).read_text();text=C.read_text();restored=text
check('exact20 unique global hunknames',len(record['finite_global_hunks'])==20 and len({h['name']for h in record['finite_global_hunks']})==20)
for h in reversed(record['finite_global_hunks']):
 check('unique whole global source hunk '+h['name'],restored.count(h['after'])==1 and h['after'].startswith(h['name']+' = ')and h['before'].startswith(h['name']+' = '))
 restored=restored.replace(h['after'],h['before'],1)
check('entire byteinverse20→59590a',restored==old and hashlib.sha256(restored.encode()).hexdigest()==oldpin['sha256'])
nt=ast.parse(text,filename=str(C));ot=ast.parse(old,filename=oldpin['path']);check('whole source ASTinverse20→59590a',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ot,include_attributes=False))
nf={n.name:n for n in nt.body if isinstance(n,ast.FunctionDef)};of={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)};check('all17 definitions no changes',len(nf)==len(of)==17 and set(nf)==set(of))
for name,n in of.items():check('whole function byte/AST exact '+name,ast.dump(n,include_attributes=False)==ast.dump(nf[name],include_attributes=False)and ast.get_source_segment(old,n)==ast.get_source_segment(text,nf[name]))
g=globals_literal(nt);og=globals_literal(ot);req=g['REQUIRED_FUTURE_BINDING_FIELDS'];check('19 requirements and only20 permitted global names',len(req)==len(set(req))==19 and set(h['name']for h in record['finite_global_hunks'])==set(req)|{'WRITER_SOURCE_STATUS'})
check('truthful ready literal guards unchanged17 functions',g['WRITER_SOURCE_STATUS']=='READY_ROOT_ACTUAL_SAVED_META_BOUND_V22'and ast.unparse(nf['main'].body[0])=='require_bound_saved_reviews()')
for name in req:
 if name.endswith('IDENTITY7'):check('native exact7 typedints '+name,type(g[name])is list and len(g[name])==7 and all(type(x)is int for x in g[name]))
 else:check('required actual binding nonemptystring '+name,type(g[name])is str and bool(g[name]))
for name in ('PP','FP'):check('original unused None retained '+name,g[name]is None and not any(isinstance(n,ast.Name)and n.id==name and isinstance(n.ctx,ast.Load)for n in ast.walk(nf['main'])))
check('8strong expected SHA dictionary unchanged',g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']==og['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S']and len(g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S'])==8)
for name,value in g['EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S'].items():check('Rootbound actual matches strong expected8 '+name,g[name]==value)
check('exact9 binding input map',set(record['exact_nine_binding_input_pins'])=={'PURE_PEER','PURE_PEER_TOOL','PURE_PEER_SEAL','PURE_PEER_SEAL_TOOL','FRESH_PEER','FRESH_PEER_TOOL','FRESH_PEER_SEAL','FRESH_PEER_SEAL_TOOL','FRESH_SOURCE_BINDING_RECORD'})
data={}
for name,expected in record['exact_nine_binding_input_pins'].items():
 check('actual nine fullEOF SHA7ID '+name,pin(Path(expected['path']))==expected)
 check('Source bound path/SHA routes '+name,g[name+'_PATH']==expected['path']and g[name+'_SHA256']==expected['sha256'])
 data[name]=read(Path(expected['path']),expected['sha256'])
check('binding5cdf native7ID exact',g['FRESH_SOURCE_BINDING_RECORD_SHA256']=='5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3'and g['FRESH_SOURCE_BINDING_RECORD_IDENTITY7']==record['exact_nine_binding_input_pins']['FRESH_SOURCE_BINDING_RECORD']['identity']==[16777229,49400000,33188,1,16493,1791600978260704687,1791600978260713937])
for name,schema,count in [('PURE_PEER','INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1',1084),('FRESH_PEER','INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1',686)]:
 d=data[name];check('actual exact savedpeer schema/checks '+name,d['schema']==schema and d['PASS']is True and d['hard_blockers']==[]and type(d['check_count'])is int and d['check_count']==len(d['checks'])==count and all(type(x['PASS'])is bool and x['PASS']is True for x in d['checks'])and d['new_Q']is None)
pt=data['PURE_PEER_TOOL'];ft=data['FRESH_PEER_TOOL']['terminal_tool_return']
for d,chunk in [(pt,'bfea93'),(ft,'722af0')]:check('actual two strict peerint0closed '+chunk,d['chunk_id']==chunk and type(d['exit_code'])is int and d['exit_code']==0 and 'session_id'not in d)
for name,a,chunk in [('PURE_PEER_SEAL',pt,'28f447'),('FRESH_PEER_SEAL',ft,'407e5a')]:
 d=data[name];check('actual saved seal rawaudit distinctbinding '+name,d['actual_peer_audit_tool_return']==a and d['actual_peer_closed']is True and type(d['actual_peer_exit_code'])is int and d['actual_peer_exit_code']==0 and d['new_Q']is None)
 t=data[name+'_TOOL'];tr=t['terminal_tool_return'];check('actual saved seal terminal exact '+chunk,t['closed']is True and tr['chunk_id']==chunk and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr)
check('peerpure complete117unique/fresh112full41unique and27fields',len({x['path']for x in data['PURE_PEER']['complete_full_EOF_reads']})==117 and len(data['FRESH_PEER']['complete_full_EOF_reads'])==112 and len(data['FRESH_PEER']['unique_complete_fresh_rechecked_input_pins'])==41 and len(data['FRESH_PEER']['all27_return_fields'])==27)
check('RootSource binding true118d6b integer0closed noSession',receipt['schema']=='ROOT_V22_ACTUAL_JOINT_HELPER_Q_WRITER_SOURCE_BINDING_TOOL_RETURN_V1'and receipt['source_only']is True and receipt['actual_tool_return_observed']is True and receipt['closed']is True and receipt['new_Q']is None and receipt['helper_guard_API_or_business_executed']is False and receipt['actual_tool_return']['chunk_id']=='118d6b'and type(receipt['actual_tool_return']['exit_code'])is int and receipt['actual_tool_return']['exit_code']==0 and 'session_id'not in receipt['actual_tool_return'])
out=json.loads(receipt['actual_tool_return']['output'],object_pairs_hook=pairs,parse_constant=bad)
check('actual Python terminal output fullpins sourcebinding no selfcycle',out['bound_writer']==record['bound_writer']and out['binding_record']==PINS[str(R)]and out['source_only']is True and out['complete_original_source_files_retained']==31 and out['function_count']==17 and out['global_hunks']==20 and out['new_Q']is None and out['helper_guard_business_executed']is False)
previous_pin=pin(Path(record['independent_source_review']['path']));check('priorSourceReview32e exact pin',previous_pin==record['independent_source_review']and previous_pin['sha256']=='32e93a0509a7dad751ee677161ddc07f380f9312ad13e3fc668f20d18ffc2ae8')
prev=read(Path(previous_pin['path']));check('reuse independent original721 full Source contract Source-only evidence',prev['PASS']is True and prev['hard_blockers']==[]and prev['check_count']==len(prev['checks'])==721 and prev['qualified_UNREADY_writer_sha256']==oldpin['sha256']and prev['qualified_Source_manifest_sha256']=='3fd6fe5c2922dbf041985c3aca05c1c501e9f7fafc384a663af9bfa3f405ac91'and prev['new_Q']is None and prev['reviewer_target_writer_or_helper_guard_API_executed']is False)
copy=D/'sealed_complete_original_UNREADY_Q_writer_SOURCE';om=read(copy/'MANIFEST.json','3fd6fe5c2922dbf041985c3aca05c1c501e9f7fafc384a663af9bfa3f405ac91')
check('all31 original Source copy exact namespace',set(str(p.relative_to(copy))for p in copy.rglob('*')if p.is_file())==set(om['members'])|{'MANIFEST.json'}and len(record['complete_original_source_package'])==31)
for name,expected in om['members'].items():
 actual=pin(copy/name);entry=record['complete_original_source_package'][name];check('full31 copy retains original byteSHA '+name,actual['sha256']==expected['sha256']and actual['size_bytes']==expected['size_bytes']and actual==entry['saved']and entry['original']==expected)
check('copied manifest exact preserved bytes fullpin',pin(copy/'MANIFEST.json')==record['complete_original_source_package']['MANIFEST.json']['saved']and record['complete_original_source_package']['MANIFEST.json']['original']['sha256']=='3fd6fe5c2922dbf041985c3aca05c1c501e9f7fafc384a663af9bfa3f405ac91')
check('allcaps/pure/fresh controls businessFalse inherit exact17 functions',all(x in text for x in ['64 * 2**20','96 * 2**30','8 * 2**30','1084','686','63379','175886','37112','37111','validate_private_owner_controls(owner_controls)',"'whole_build_qualified': False","'physical_balance_qualified': False"]))
q=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json';check('new Q observed not created at Source review time',not q.exists())
initial=list(PINS.values())
for expected in initial:check('all finite Source/META end wholeEOF7ID stable '+expected['path'],pin(Path(expected['path']))==expected)
for name,expected in freeze['complete_directories'].items():check('frozen2 directory7ID unchanged end '+name,id7(D/name)==expected)
status='SOURCE_PASS_BOUND_EXACT20_GLOBALS_READY_FOR_ROOT_STDLIB_META_ONLY'
review={'schema':'INDEPENDENT_V22_ACTUAL_BOUND_JOINT_Q_WRITER_SOURCE_REVIEW_V1','status':status,'PASS':True,'hard_blockers':[],'check_count':len(CHECKS),'checks':CHECKS,'source_only':True,'qualified_READY_writer_pin':record['bound_writer'],'qualified_SOURCE_binding_record_pin':PINS[str(R)],'qualified_SOURCE_freeze_pin':PINS[str(F)],'actual_Root_SOURCE_binding_tool_receipt_pin':PINS[str(T)],'full_Source_META_input_pins':initial,'complete_D_file_count':33,'complete_D_directory_count':2,'all_frozen_Source_before_after_exact':True,'whole20_global_byte_AST_inverse_to_59590a':True,'all17functions_wholebyte_AST_exact':True,'all9actualbindingpins_fullEOF_SHA7ID_verified':True,'all8strong_expectedSHA_bound':True,'actual5cdf_native7ID_verified':True,'reuse_independent_original_full721Source_contract':True,'target_writer_or_helper_guard_API_executed':False,'numeric_or_graph_or_material_payload_read':False,'Root_D_E_canonical_ART_or_Q_written':False,'new_Q':None,'whole_build_qualified':False,'whole_INPUT_admitted':False,'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False,'minor_nonblocking_note':'The module docstring is inherited byteexact from the UNREADY template; actual READY status and binding record explicitly identify activation. No doc hunk was authorized in the exact20-global binding contract.'}
(HERE/'REVIEW.json').write_text(json.dumps(review,indent=2,allow_nan=False)+'\n')
(HERE/'REPORT.txt').write_text(status+'\nActual61d552 READY Source and9909 binding record match Root118d6b strict0closed output. Complete D33files/2dirs exact freeze; copied original31files preserve3fd6 and59590a; all20 global bindings alone invert entire bytes/AST to59590a and all17 functions remain byte/ASTexact.\nNine actual saved input fullpins and eight expected hashes plus native5cdf7ID all exact. Original721 independent Source contract/pure1084/fresh686 schemas/caps remain untouched. Target writer never executed here, newQ absent at review instant, and all business/native/science qualifications false.\nMinor inherited docstring still says UNREADY; binding status and actualSource metadata are READY. This cosmetic inherited text does not alter function guard or the exact20-global contract.\n')
print(json.dumps({'package':str(HERE),'status':status,'checks':len(CHECKS),'Source_META_input_count':len(initial),'REVIEW_SHA':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest(),'READY_writer_SHA':record['bound_writer']['sha256'],'hard_blockers':[]}))

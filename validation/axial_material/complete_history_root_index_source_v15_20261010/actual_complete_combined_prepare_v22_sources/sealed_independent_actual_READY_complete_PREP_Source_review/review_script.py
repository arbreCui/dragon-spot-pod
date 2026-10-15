"""Finite actual bound SOURCE and saved META review; no target imports/calls."""
from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_v22_actual_Q_bound_complete_PREP_SOURCE_root_20261010_b89d2')
U=Path('/private/tmp/axmat_v22_complete_canonical_genuine_PREP_UNREADY_SOURCE_wngfraff')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_joint_helper_admission_v22b_receipts'
ART=Path('/Users/wen/spot/validation/artifacts')
HERE=Path(__file__).parent
checks=[];seen={}
def ck(name,ok):
 assert type(ok) is bool,name
 checks.append({'name':name,'PASS':ok});assert ok,name
def id7(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p,expected=None):
 p=Path(p);before=id7(p);ck('regular nonsymlink '+str(p),stat.S_ISREG(before[2]) and not p.is_symlink())
 raw=p.read_bytes();ck('fullEOF stable '+str(p),id7(p)==before)
 actual=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
 if expected is not None:ck('fullpin exact '+str(p),actual==expected)
 if str(p) in seen:ck('same observed pin '+str(p),seen[str(p)]==actual)
 seen[str(p)]=actual;return raw,actual
def read(p,expected=None):
 raw,item=full(p,expected);return json.loads(raw),item
def defs(text):
 return {n.name:n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assignment(tree,name):
 return next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def undo(text,edits,label):
 for edit in reversed(edits):
  ck('unique inverse hunk '+label+'/'+edit['label'],text.count(edit['new'])==1)
  text=text.replace(edit['new'],edit['old'],1)
 return text
m,mpin=read(P/'MANIFEST.json')
ck('fixed actual bound manifest',mpin['sha256']=='7e2711c180b11ed4d9181f944c8ccd948aebc463227c8ba22b5f7117a6a5c894')
ck('complete6members7files',m['member_count']==len(m['members'])==6 and {str(q.relative_to(P)) for q in P.rglob('*') if q.is_file()}==set(m['members'])|{'MANIFEST.json'})
for rel,item in m['members'].items():full(P/rel,item)
proof,proof_pin=read(P/'actual_READY_binding_complete_SOURCE_inverse.json')
result,result_pin=read(P/'SOURCE_binding_result.json')
receipt,receipt_pin=read(E/'Root_actual_Q_to_complete_PREP_Source_binding_tool_return.json')
ck('trueRoot binding receipt schema',receipt['schema']=='ROOT_ACTUAL_NEW_Q_TO_COMPLETE_PREP_SOURCE_BINDING_TOOL_RETURN_V1')
ck('trueRoot binding closed sourceonly',receipt['closed'] is True and receipt['observed_terminal'] is True and receipt['source_only'] is True)
tr=receipt['actual_tool_return'];ck('trueRoot a740d2 typed0 no session',tr['chunk_id']=='a740d2' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
actual_out=json.loads(tr['output'])
ck('trueRoot direct manifest pin exact',actual_out['manifest']==mpin)
ck('trueRoot project scientific flags false',receipt['project_business_or_numeric_executed'] is False and receipt['new_scientific_qualification_created'] is False and actual_out['executed_project'] is False)
Q,Qpin=read(proof['new_actual_Q']['path'],proof['new_actual_Q'])
ck('actual qualified Q fixed89d2',Qpin['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816')
ck('result actualQ fullpin exact',result['actual_Q']==Qpin and actual_out['actual_Q']==Qpin)
qcopy,_=full(P/'ACTUAL_NEW_JOINT_HELPER_Q.byte_exact.json',m['members']['ACTUAL_NEW_JOINT_HELPER_Q.byte_exact.json'])
qraw,_=full(Qpin['path'],Qpin);ck('Q copy complete byteexact original',qcopy==qraw)
ck('exact actualRoot CLI',receipt['actual_arguments']['cmd']==str(Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'))+' -B '+str(U/'bind_actual_Q_to_complete_PREP_SOURCE.py')+' '+Qpin['path']+' '+Qpin['sha256']+' '+str(P))
uf,ufpin=read(U/'MANIFEST.json');ck('prior UNREADY manifest fixed0000',ufpin['sha256']=='0000b8505b6ea35a149099fe9d0494532f26521bfa13b7de6c8236b297beb9c4')
oldproof,_=read(U/'COMPLETE_SOURCE_INVERSES.json');constants,_=read(U/'ROOT_BINDING_SOURCE_CONSTANTS.json')
expected_shas={'canonical':'09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e','host':'1be8cbf79ef14d7537d099d0a08d0c5ef755530c2652c58cfbb188c7e18bf051','writer':'348ae877f7c8e4c86f07cb4a49f96de97e11839ccb0858c5a602e3982a4ccba0'}
filenames={'canonical':'complete_combined_runtime.V22.READY_SOURCE.py','host':'combined_prepare_host.py','writer':'write_actual_prepare_terminal.py'}
bound={}
for name,count,oldcount in [('canonical',4,11),('host',4,13),('writer',3,14)]:
 raw,pin=full(P/filenames[name],m['members'][filenames[name]]);text=raw.decode();bound[name]=text
 ck('fixed actual candidateSHA '+name,pin['sha256']==expected_shas[name])
 field={'canonical':'READY_source','host':'genuine_PREP_host_Source','writer':'complete_PREP_metadata_writer_Source'}[name]
 ck('binding result direct actual fullpin '+name,result[field]==pin)
 row=proof['full_inverse'][name];edits=row['READY_to_UNREADY_edits']
 ck('exact actual READY hunk count '+name,len(edits)==count)
 unready_raw,_=full(U/(name+'.V22.UNREADY.full.py'),uf['members'][name+'.V22.UNREADY.full.py'])
 unready=unready_raw.decode();back=undo(text,edits,name+'/READY')
 ck('wholeREADY byteinverse to fixed UNREADY '+name,back==unready)
 ck('wholeREADY ASTinverse to fixed UNREADY '+name,ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(unready),include_attributes=False))
 nd,ud=defs(text),defs(unready);ck('all actual function names/order same '+name,list(nd)==list(ud))
 for fname,node in nd.items():
  ck('every bound function byteexact '+name+'/'+fname,ast.get_source_segment(text,node)==ast.get_source_segment(unready,ud[fname]))
  ck('every bound function ASTexact '+name+'/'+fname,ast.dump(node,include_attributes=False)==ast.dump(ud[fname],include_attributes=False))
 ck('old11/13/14 transforms exactly retained '+name,row['UNREADY_to_original_parent_edits']==oldproof['exact_finite_transforms'][name] and len(row['UNREADY_to_original_parent_edits'])==oldcount)
 original=undo(back,row['UNREADY_to_original_parent_edits'],name+'/parent')
 parent_raw,parent_pin=full(row['original_parent']['path'],row['original_parent'])
 ck('whole actual inverse original parent bytes '+name,original.encode()==parent_raw)
 ck('whole actual inverse original parent AST '+name,ast.dump(ast.parse(original),include_attributes=False)==ast.dump(ast.parse(parent_raw),include_attributes=False))
 ck('original parent proof fullpin unchanged '+name,parent_pin==oldproof['parent_sources'][name])
ct=ast.parse(bound['canonical']);ht=ast.parse(bound['host']);wt=ast.parse(bound['writer'])
ck('canonical70 complete definitions',len(defs(bound['canonical']))==70)
ck('canonicalREADY status exact original predicate',ast.literal_eval(assignment(ct,'DRAFT_STATUS'))=='READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
ck('canonical actual newQ SHA exact',ast.literal_eval(assignment(ct,'FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'))==Qpin['sha256'])
helpers=assignment(ct,'INPUT_HELPERS');gvalue=next(v for k,v in zip(helpers.keys,helpers.values) if ast.literal_eval(k)=='graph')
ck('canonical actualcf0 helperSHA exact',ast.literal_eval(gvalue.elts[1])==Q['helper']['sha256'])
ck('host actual canonicalSHA exact',ast.literal_eval(assignment(ht,'TARGET_SHA'))==expected_shas['canonical'])
ck('host actual QSHA exact',ast.literal_eval(assignment(ht,'ACTUAL_HELPER_Q_SHA'))==Qpin['sha256'])
qp=assignment(ht,'ACTUAL_HELPER_Q_PATH');ck('host exact actualQ logical path',isinstance(qp,ast.Call) and isinstance(qp.func,ast.Name) and qp.func.id=='Path' and ast.literal_eval(qp.args[0])==Qpin['path'])
ck('writer actual canonicalSHA exact',ast.literal_eval(assignment(wt,'FACTORY_SHA'))==expected_shas['canonical'])
ck('host ready status exact source guard',ast.literal_eval(assignment(ht,'SOURCE_BINDING_STATUS'))=='READY_V22_ACTUAL_Q_AND_TARGET_SOURCE_BOUND')
ck('writer ready status exact source guard',ast.literal_eval(assignment(wt,'SOURCE_BINDING_STATUS'))=='READY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND')
ck('Root output canonicalSHA exact',actual_out['complete_READY_source_sha256']==expected_shas['canonical'])
for k,v in proof['six_future_business_pins'].items():
 ck('all six business pins reallyNone '+k,v is None and result['all_future_business_pins'][k] is None and isinstance(assignment(ct,k),ast.Constant) and assignment(ct,k).value is None)
caps={'whole_seconds':1800,'phase_seconds':600,'rss_mib':512,'archive_bytes':2*2**30,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
ck('all original budgets no future cap relaxation',proof['original_complete_PREP_caps']==caps==constants['caps']==oldproof['original_complete_genuine_PREP_caps'])
ck('all complete original five stages unchanged',defs(bound['canonical'])['stage_labels'] and "return ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']" in ast.get_source_segment(bound['canonical'],defs(bound['canonical'])['stage_labels']))
ck('host original guardMRO strict resource/ownchild maintained',"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in bound['host'] and "helper.guard_admission(full)" in bound['host'] and "runner.execute(HOST/'run','prepare',command,STAGE_CAP)" in bound['host'] and "watch['own_child_only'] is not True" in bound['host'])
ck('host fullSource pins dynamic complete',"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]" in bound['host'] and "for entry in inputs+[hpin,rpin]" in bound['host'])
ck('host only four strict ART history roots',"resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)" in bound['host'])
ck('writer original source and full joint archive unchanged',"for root in (H,S,O,T,D,E)" in bound['writer'] and '+FACTORY.stat().st_size' in bound['writer'])
ck('writer actual genuineclosed0 before formal output unchanged',"type(observed.get('exit_code')) is not int" in bound['writer'] and "'session_id' in observed" in bound['writer'] and "if os.path.lexists" not in bound['writer'])
refs=[]
def collect(v):
 if type(v) is dict:
  if 'path' in v and 'sha256' in v and ('identity' in v or 'identity7' in v) and Path(v['path']).is_relative_to(ART):refs.append(v)
  for x in v.values():collect(x)
 elif type(v) is list:
  for x in v:collect(x)
collect(Q)
ck('all9 ART refs preserved full but not newly read',refs==proof['ART_references_preserved_not_read'] and len(refs)==9)
ck('all44 full input SourceMETA pins unique',len(proof['all_read_Source_and_saved_META_before_after_pins'])==len({x['path'] for x in proof['all_read_Source_and_saved_META_before_after_pins']})==44)
for item in proof['all_read_Source_and_saved_META_before_after_pins']:
 ck('actual binder never ART inputread '+item['path'],not Path(item['path']).is_relative_to(ART))
 full(item['path'],item)
ck('actual binder package22 complete inputscope included',{str(U/rel) for rel in uf['members']}|{str(U/'MANIFEST.json')} <= {x['path'] for x in proof['all_read_Source_and_saved_META_before_after_pins']})
retained={}
for dirname,reviewsha,count in [
 ('sealed_independent_actual_joint_helper_Q_saved_META_review','625e4deb8d0cc3637b7ef46e4189f3c00fafc3724777bc212b9cb9e8c18f0b96',1937),
 ('sealed_independent_complete_PREP_UNREADY_Source_review','eca3ef1134f4a4a456181b804e1618cca5b1673e4b85c62b2b938b0a00a5e844',576),
]:
 root=E/dirname;report,reportpin=read(root/'REVIEW.json');manifest,manifestpin=read(root/'MANIFEST.json')
 ck('actual retained original peer PASS '+dirname,report['PASS'] is True and report['check_count']==count and reportpin['sha256']==reviewsha)
 ck('complete retained original peer membership '+dirname,{str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}==set(manifest['members'])|{'MANIFEST.json','_actual_peer_seal_receipt.json'})
 for rel,original in manifest['members'].items():
  _,copy=full(root/rel)
  ck('whole peer retained bytes SHA '+dirname+'/'+rel,copy['sha256']==original['sha256'] and copy['size_bytes']==original['size_bytes'])
 seal,_=read(root/'_actual_peer_seal_receipt.json');tr=seal['terminal_tool_return']
 ck('actual retained peerseal strict0 closed '+dirname,seal['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
 retained[dirname]={'review':reportpin,'manifest':manifestpin}
for k in ['supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified']:ck('actualQ software scopefalse '+k,Q[k] is False)
ck('Source binding itself no installedbusiness/science claimed',proof['installed_or_executed'] is False and result['helper_guard_API_PREP_build_INPUT_native_or_numeric_executed'] is False and result['canonical_or_ART_or_Root_D_E_written'] is False and result['new_helper_qualification_created_by_this_Source_binder'] is False)
for path,item in list(seen.items()):full(path,item)
review={'schema':'INDEPENDENT_V22_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1','SOURCE_PASS':True,'PASS':True,'hard_blockers':[],'check_count':len(checks),'checks':checks,'actual_bound_manifest':mpin,'actual_Root_binding_tool_receipt':receipt_pin,'actual_full_Q_pin':Qpin,'all_explicit_Source_and_saved_META_input_fullpins':seen,'explicit_input_count':len(seen),'all7boundfiles_and_all44actualbinderinputs_fullEOF_SHA7ID_unchanged':True,'all4_4_3_READY_hunks_exact_inverse_to_fixed_UNREADY':True,'all70_1_7definitions_byte_AST_exact_to_UNREADY':True,'full11_13_14byte_ASTinverse_to_actual_original023_776_9dc':True,'all_original_caps':caps,'complete67oldinputs_two_fullphases_five_build_stages_preserved_by_whole_source_inverse':True,'all_six_future_business_pins_None':True,'actual_pure_and_fresh_source_and_Q_metadata_reviews_whole_retained':retained,'nine_ART_references_complete_unmodified_not_newly_read':refs,'candidate_helper_guard_binder_API_PREP_build_INPUT_native_or_numeric_executed_by_peer':False,'ART_graph_material_or_gzip_payload_read_or_decoded_by_peer':False,'project_canonical_D_E_ART_or_original_Source_modified_by_peer':False,'actual_new_PREP_build_INPUT_native_physics_AAA_ABA_or_goal_qualified':False}
(HERE/'REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
(HERE/'REPORT.txt').write_text('SOURCE_PASS only. ActualRoot binder a740d2 typed0closed; bound canonical09e539/host1be8cb/writer348ae8 fullpins exact.\nAll4/4/3 READY hunks restore fixedUNREADY, all70/1/7 definitions byte/AST exact; full11/13/14 inverses restore actual023abc/776bf/9dc original parents.\nActualQ89d2 whole bytecopy and actualRoot receipt match. Prior1937 savedQ and576 UNREADY reviews retained complete with real seals. All44 actualbinder Source/META inputs and bound7 files fullSHA7ID stable.\nOriginal1800/600/512/2GiB/96GiB/free8GiB/1/1/0 budgets, all67 oldinput shapes/two complete phases/five stages, genuine guard/MRO/fullSource namespace preserved. Six futurebusinesspins remainNone. NineART refs remain whole and were not opened by this review.\nNo binder/helper/guard/API/PREP/build/native/numeric was executed by reviewer. No project original file written and no PREP/build/INPUT/science success predicted. Root may only install exact accepted Source and perform its own genuine actual PREP.\n')
print(json.dumps({'package':str(HERE),'SOURCE_PASS':True,'check_count':len(checks),'input_count':len(seen),'REVIEW_sha256':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest(),'canonical_sha256':expected_shas['canonical'],'science_qualified':False}))


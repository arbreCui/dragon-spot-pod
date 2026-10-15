"""Independent bounded SOURCE/stdlib META only; no candidate/API calls."""
from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_v22_complete_canonical_genuine_PREP_UNREADY_SOURCE_wngfraff')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
HERE=Path(__file__).parent
checks=[];seen={};texts={}
def ck(name,ok):
 assert type(ok) is bool,name
 checks.append({'name':name,'PASS':ok});assert ok,name
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p,expected=None):
 p=Path(p);before=identity(p);ck('regular nonsymlink '+str(p),stat.S_ISREG(before[2]) and not p.is_symlink())
 raw=p.read_bytes();ck('full EOF stable '+str(p),identity(p)==before)
 item={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
 if expected is not None:ck('fullpin exact '+str(p),item==expected)
 if str(p) in seen:ck('same observed pin '+str(p),seen[str(p)]==item)
 seen[str(p)]=item;return raw,item
def read(p,expected=None):
 raw,item=full(p,expected);return json.loads(raw),item
def defs(text):
 return {n.name:n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assignment(tree,name):
 return next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def literals(node):
 return [n.value for n in ast.walk(node) if isinstance(n,ast.Constant)]
manifest,mpin=read(P/'MANIFEST.json')
ck('fixed author manifest SHA',mpin['sha256']=='0000b8505b6ea35a149099fe9d0494532f26521bfa13b7de6c8236b297beb9c4')
ck('complete21 members567519B',manifest['member_count']==len(manifest['members'])==21 and manifest['member_bytes']==sum(v['size_bytes'] for v in manifest['members'].values())==567519)
ck('complete22 filenames',set(str(q.relative_to(P)) for q in P.rglob('*') if q.is_file())==set(manifest['members'])|{'MANIFEST.json'})
for rel,item in manifest['members'].items():
 raw,_=full(P/rel,item)
 if rel.endswith('.py'):texts[rel]=raw.decode();ast.parse(raw)
proof,_=read(P/'COMPLETE_SOURCE_INVERSES.json')
constants,_=read(P/'ROOT_BINDING_SOURCE_CONSTANTS.json')
plan_raw,_=full(proof['plan_source']['path'],proof['plan_source'])
ck('complete exact plan retained',plan_raw==(P/'EXACT_PARENT_SOURCE_PLAN.full.json').read_bytes())
ck('all proof original unknown Q honest',proof['new_helper_Q_path'] is None and proof['new_helper_Q_sha256'] is None and constants['expected_Q_sha256'] is None)
caps={'whole_seconds':1800,'phase_seconds':600,'rss_mib':512,'archive_bytes':2*2**30,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
ck('complete original genuine caps',proof['original_complete_genuine_PREP_caps']==caps and constants['caps']==caps and manifest['original_genuine_caps']==caps)
transform_counts={}
for name,expected_count in [('canonical',11),('host',13),('writer',14)]:
 parent_raw,parent_pin=full(proof['parent_sources'][name]['path'],proof['parent_sources'][name])
 parent=texts[name+'.V21.parent.full.py'];candidate=texts[name+'.V22.UNREADY.full.py']
 ck('parent complete byte exact actual source '+name,parent.encode()==parent_raw)
 ck('constants actual parent pin exact '+name,constants['original_sources'][name]==parent_pin)
 edits=proof['exact_finite_transforms'][name];transform_counts[name]=len(edits)
 ck('exact finite transform count '+name,len(edits)==expected_count)
 current=parent
 for e in edits:
  ck('unique original anchor '+name+'/'+e['label'],current.count(e['old'])==1)
  current=current.replace(e['old'],e['new'],1)
 ck('complete forward exact candidate '+name,current==candidate)
 back=candidate
 for e in reversed(edits):
  ck('unique inverse anchor '+name+'/'+e['label'],back.count(e['new'])==1)
  back=back.replace(e['new'],e['old'],1)
 ck('complete byte inverse original '+name,back==parent)
 ck('complete AST inverse original '+name,ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
 old_defs,new_defs=defs(parent),defs(candidate)
 ck('all definition names order '+name,list(old_defs)==list(new_defs))
 for fname,node in old_defs.items():
  if name=='canonical' and fname=='require_ready':
   expected=ast.get_source_segment(parent,node).replace('READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
   ck('requireReady only ownV22 status literal',expected==ast.get_source_segment(candidate,new_defs[fname]))
  elif name=='canonical' or fname!='main':
   ck('original complete definition bytes '+name+'/'+fname,ast.get_source_segment(parent,node)==ast.get_source_segment(candidate,new_defs[fname]))
   ck('original complete definition AST '+name+'/'+fname,ast.dump(node,include_attributes=False)==ast.dump(new_defs[fname],include_attributes=False))
 if name=='canonical':
  ck('full70 and69 other definitions unchanged',len(new_defs)==70)
  tree=ast.parse(candidate)
  for key in proof['six_future_business_pins']:
   ck('canonical future business None '+key,isinstance(assignment(tree,key),ast.Constant) and assignment(tree,key).value is None)
  ck('UNREADY canonical status and futureQ None',ast.literal_eval(assignment(tree,'DRAFT_STATUS'))=='UNREADY_V22_COMPLETE_NEW_HELPER_ACTUAL_Q_UNBOUND' and ast.literal_eval(assignment(tree,'FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA')) is None)
  helpers=assignment(tree,'INPUT_HELPERS')
  graphvalue=next(v for k,v in zip(helpers.keys,helpers.values) if ast.literal_eval(k)=='graph')
  ck('unbound graph helper SHA None',isinstance(graphvalue,ast.Tuple) and ast.literal_eval(graphvalue.elts[1]) is None)
  ready=new_defs['require_ready'];ck('original requireReady helper andQ reject before inputs','nonzero_sha(INPUT_HELPERS' in ast.get_source_segment(candidate,ready) and 'nonzero_sha(FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA)' in ast.get_source_segment(candidate,ready))
 if name in ('host','writer'):
  tree=ast.parse(candidate);main=new_defs['main'];first=main.body[0]
  ck('UNREADY guard is first main statement '+name,isinstance(first,ast.If) and isinstance(first.body[0],ast.Raise))
  if name=='host':
   for key in ['TARGET_SHA','ACTUAL_HELPER_Q_PATH','ACTUAL_HELPER_Q_SHA']:ck('host unknown bound Source '+key,ast.literal_eval(assignment(tree,key)) is None)
   ck('host genuine guard MRO and budget statements retained','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)' in candidate and 'helper.guard_admission(full)' in candidate and 'runner.execute(HOST' in candidate)
   ck('host history roots only strict ART descendants',"resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)" in candidate)
   ck('host complete Source dynamic enumeration and beforeafter retained',"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]" in candidate and 'for entry in inputs+[hpin,rpin]' in candidate)
  else:
   ck('writer unknown FACTORY SHA None',ast.literal_eval(assignment(tree,'FACTORY_SHA')) is None)
   ck('writer genuineclosed0 before output retained',"type(observed.get('exit_code')) is not int" in candidate and "'session_id' in observed" in candidate and "T.mkdir()" in candidate)
   ck('writer full H/S/O/T/D/E+factory bytes retained',"for root in (H,S,O,T,D,E)" in candidate and '+FACTORY.stat().st_size' in candidate)
   ck('writer merged child actual external host stderr honesty',"separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False" in candidate)
binder=texts['bind_actual_Q_to_complete_PREP_SOURCE.py'];bt=ast.parse(binder);bdefs=defs(binder)
ck('fixed binder SHA',seen[str(P/'bind_actual_Q_to_complete_PREP_SOURCE.py')]['sha256']=='dd4c76e0abcf106d42fa11b2e1680d4254590bea06f5397e30de675e26df2958')
ck('binder20 full defs',len(bdefs)==20)
allowed={'argparse','ast','hashlib','json','math','os','pathlib','stat','struct','sys'}
for n in bt.body:
 if isinstance(n,ast.Import):ck('binder standard-library imports only',all(a.name in allowed for a in n.names))
 if isinstance(n,ast.ImportFrom):ck('binder standard-library from only',n.module in allowed)
ck('binder no exec eval dynamicimport subprocess calls',not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'exec','eval','compile','__import__'} for n in ast.walk(bt)))
ck('binder only reviewed Source TMP outputs',"output.is_relative_to(Path('/private/tmp')) and not os.path.lexists(output)" in binder and 'output.mkdir()' in binder and 'requires_Root_external_saved_Q_review_and_bound_Source_review_before_installation=True' in binder)
ck('binder disallows ART payload read',"assert not p.is_relative_to(ART)" in binder and 'ART_REFS.append(value);return value' in binder)
ck('binder strict duplicate/finite/order/floatbit contracts retained',"'duplicate JSON key'" in binder and "parse_constant=reject_constant" in binder and "struct.pack('!d',value)==struct.pack('!d',other)" in binder and 'list(value)==list(other)' in binder)
ck('binder preserves entire full Source member namespace',"inventory==sorted(list(package['members'])+['MANIFEST.json'])" in binder and "for rel,expected in package['members'].items()" in binder)
main=bdefs['main']
for var,count in [('ce',4),('he',4),('we',3)]:
 value=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==var for t in n.targets))
 ck('future READY exact finite edit count '+var,isinstance(value,ast.List) and len(value.elts)==count)
ck('future READY full function bytes retained',"definition_segments(text)==definition_segments(templates[name])" in binder)
ck('future full inverse to original all three parents',"parent=inverse(back,proof['exact_finite_transforms'][name])" in binder and "assert parent==actual_parent" in binder)
ck('future exact70/six unknownbusiness assertion',"assert len(definition_segments(canonical))==70" in binder and "for k in BUSINESS:assert isinstance(assignments[k],ast.Constant) and assignments[k].value is None" in binder)
public=ast.literal_eval(assignment(bt,'PUBLIC27'))
ck('full public27 fields present',len(public)==27)
meta=assignment(bt,'EXPECTED_META')
ck('13 fixed saved META Source routes',isinstance(meta,ast.Dict) and len(meta.keys)==13)
Qpath=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
Q,Qpin=read(Qpath)
ck('actualQ89d2 qualified independently',Qpin['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816')
Qreview_path=Path('/private/tmp/axmat_v22_actual_joint_Q_saved_META_independent_review_20261010_eh9240ki/REVIEW.json')
Qreview,Qreview_pin=read(Qreview_path)
ck('actual1937 independent Q META review PASS',Qreview_pin['sha256']=='625e4deb8d0cc3637b7ef46e4189f3c00fafc3724777bc212b9cb9e8c18f0b96' and Qreview['PASS'] is True and Qreview['check_count']==1937 and Qreview['actual_Q']==Qpin)
equal_owner_source=(B/'actual_joint_helper_admission_v22b_sources/write_actual_joint_helper_admission_v22b.READY.py')
owner_raw,_=full(equal_owner_source)
ownertext=owner_raw.decode();owner_node=defs(ownertext)['validate_private_owner_controls']
ck('binder owner controls entire validated method byteexact',ast.get_source_segment(binder,bdefs['validate_private_owner_controls'])==ast.get_source_segment(ownertext,owner_node))
f=Q['complete_current_graph_fresh_verifier']
ck('binder actual public27 exact',public==f['full_public_return_field_order'])
ck('binder qualified installed Source pin actual',ast.literal_eval(assignment(bt,'HELPER_SHA'))==Q['helper']['sha256'] and ast.literal_eval(assignment(bt,'HELPER_ID'))==Q['helper']['identity'])
full(proof['new_installed_helper_Source_only']['path'],proof['new_installed_helper_Source_only'])
expected_links={'pure_terminal':Q['actual_root_terminal'],'fresh_terminal':f['actual_root_terminal'],'pure_summary':Q['actual_controls_summary'],'fresh_summary':f['actual_controls_summary'],'pure_peer':Q['independent_actual_review'],'fresh_peer':f['independent_actual_review'],'pure_audit':Q['independent_actual_review_tool_return'],'fresh_audit':f['independent_actual_review_tool_return'],'pure_seal':Q['sealed_independent_pure_actual_review_manifest'],'fresh_seal':f['sealed_independent_actual_review_manifest'],'pure_seal_tool':Q['independent_pure_actual_review_seal_tool_return'],'fresh_seal_tool':f['independent_actual_review_seal_tool_return'],'source_binding':f['source_binding_record']}
for key,value in zip(meta.keys,meta.values):
 label=ast.literal_eval(key);ck('each fixed saved META digest aligns actualQ '+label,ast.literal_eval(value.elts[1])==expected_links[label]['sha256'])
 ck('fixed named saved META tuple '+label,isinstance(value,ast.Tuple) and len(value.elts)==2)
ck('both actual 0closed trial shape explicitly checked',"type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr" in binder and "'6f6847'" in binder and "'57a6f5'" in binder)
ck('actual1084/686 peer complete checksets retained',"1084),('fresh_peer'" in binder and "686))" in binder and "len(v['checks'])==count" in binder)
ck('full normalized3gzip joins all4 exact pin fields',"for field in ('path','sha256','identity','size_bytes')" in binder and "complete['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True" in binder and "complete['no_fields_or_records_filtered'] is True" in binder)
ck('all complete nested Source/META pin refs retained',"collect_full_references(q)" in binder and "for x in value.values():collect_full_references(x)" in binder)
sb,_=read(f['source_binding_record']['path'],f['source_binding_record'])
ck('binding shape actual5cdf matches future binder',sb['schema']=='AXMAT_V22_ROOT_ACTUAL_SOURCE_ONLY_QUALIFICATION_BINDING_INVERSES_V1' and sb['new_Q'] is None)
author_review,_=read(P/'FINAL_COMPLETE_SOURCE_SELF_REVIEW.json')
ck('actual author292 complete Source selfchecks',author_review['all_checks_passed'] is True and author_review['blockers']==[] and author_review['check_count']==len(author_review['checks'])==292)
author_receipt,_=read(P/'ACTUAL_SOURCE_FINAL_SELF_REVIEW_TOOL_TERMINAL_RETURN.json')
tr=author_receipt['terminal_tool_return'];ck('actual author8e9826 typed0closed',author_receipt['closed'] is True and tr['chunk_id']=='8e9826' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
seal_path=Path(str(P)+'_seal_receipt/ACTUAL_SOURCE_PACKAGE_SEAL_TOOL_TERMINAL_RETURN.json')
seal,seal_pin=read(seal_path);tr=seal['terminal_tool_return']
ck('actual authorseal23db29 typed0closed',seal['closed'] is True and seal['manifest_sha256']==mpin['sha256'] and tr['chunk_id']=='23db29' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
sealout=json.loads(tr['output']);ck('actual seal direct complete manifest pin',sealout['manifest']==mpin)
correction,_=read(P/'HONEST_SOURCE_SELF_REVIEW_CORRECTIONS_TOOL_RETURNS.json')
ck('two authorSource selfcheck errors retained',len(correction['failed_stdlib_checks'])==2 and [x['terminal_tool_return']['chunk_id'] for x in correction['failed_stdlib_checks']]==['4de9c5','31ea28'] and all(type(x['terminal_tool_return']['exit_code']) is int and x['terminal_tool_return']['exit_code']==1 for x in correction['failed_stdlib_checks']))
for p,expected in list(seen.items()):full(p,expected)
review={'schema':'INDEPENDENT_V22_COMPLETE_CANONICAL_GENUINE_PREP_UNREADY_SOURCE_REVIEW_V1','SOURCE_PASS':True,'PASS':True,'hard_blockers':[],'check_count':len(checks),'checks':checks,'author_package_manifest':mpin,'author_actual_seal_receipt':seal_pin,'all_explicit_complete_Source_and_small_META_fullpins':seen,'explicit_input_count':len(seen),'canonical70definitions_69exact_and_requireReady_only_statusliteral':True,'full_byte_AST_inverses':transform_counts,'future_READY_binding_hunks':{'canonical':4,'host':4,'writer':3},'all_original_caps':caps,'whole_67_old_input_shape_and_two_complete_phases_five_stages_unchanged_by_full_inverse':True,'all_six_future_business_success_pins_None':True,'real_Q_available_and_independently_saved_META_reviewed':Qpin,'actual_saved_Q_review':Qreview_pin,'binder_original20functions_only_stdlib_no_ART_read':True,'source_candidate_binder_guard_helper_API_PREP_build_INPUT_native_numeric_executed_by_peer':False,'actual_READY_candidates_produced_by_peer':False,'project_canonical_D_E_ART_or_author_sealed_Source_mutated':False,'actual_new_business_or_scientific_qualification':False}
(HERE/'REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
(HERE/'REPORT.txt').write_text('SOURCE_PASS only: full sealed22 author files and originalSource parents fully read and hash7ID verified twice.\nFull11/13/14 byte/AST inverses restore canonical023abc/genuinehost776bf/metadatawriter9dc. Full70 definitions retained;69 exact, require_ready only original own-version literal.\nUNREADY guard is before project load/META reads. Future4/4/3 Sourcebinding edits retain all function bytes, six businesspins stayNone.\nOriginal1800/600/512/2GiB/history96/free8/1/1/0, genuine619/705/productionMRO, complete Source inventory and physical/input scopes remain.\nActualQ89d2 now has independent1937 savedMETA PASS; binder fixed13 savedSource/META routes and complete3gzip join match its actual schemas. No binder/helper/guard/prepare/build/numeric execution, no ART payload read or project write. Root actual binding and new boundSource independent review remain required.\n')
print(json.dumps({'package':str(HERE),'SOURCE_PASS':True,'check_count':len(checks),'input_count':len(seen),'REVIEW_sha256':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest(),'candidate_binder_executed':False,'business_science_qualified':False}))


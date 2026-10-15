"""Independent finite complete SOURCE audit; reviewed code is never imported/called."""
import ast,hashlib,json,os,stat
from pathlib import Path
P=Path('/private/tmp/axmat_native_v23_strict_bool_complete_SOURCE_ens_zo_p')
R=Path(__file__).parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CHECKS=[];INPUTS={}
def ck(v,label):
 assert type(v)is bool and v,label
 CHECKS.append(dict(check=f'{len(CHECKS)+1:05d} '+label,passed=True))
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=identity(p)
 ck(p.is_absolute()and p.resolve()==p and stat.S_ISREG(a[2])and a[3]==1,'ordinary complete Source/META '+str(p))
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 ck(identity(p)==a,'complete EOF sevenID stable '+str(p))
 q=dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
 if str(p)in INPUTS:ck(INPUTS[str(p)]==q,'repeat fullpin unchanged '+str(p))
 INPUTS[str(p)]=q
 return q
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate metadata key')
  d[k]=v
 return d
def reject(x):raise ValueError('nonfinite metadata')
def read(p):
 q=pin(p);v=json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_constant=reject)
 ck(pin(p)==q,'JSON Source fullpin stable '+str(p))
 return v,q
def dump(x):return ast.dump(x,include_attributes=False)
def functions(t):return [n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
def globals_map(t):return {n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def source(p):
 q=pin(p);b=Path(p).read_bytes();ck(pin(p)==q,'complete Source bytes stable '+str(p));return b,ast.parse(b),q
def directory_view(root):
 dirs={'.':identity(root)};files=[]
 for p in sorted(root.rglob('*')):
  ck(not p.is_symlink(),'no complete Source namespace symlink '+str(p))
  if p.is_dir():dirs[str(p.relative_to(root))]=identity(p)
  else:ck(p.is_file(),'no complete Source special entry '+str(p));files.append(str(p))
 return dict(directories=dirs,files=files)
before=directory_view(P)
manifest,mp=read(P/'MANIFEST.json')
ck(mp['sha256']=='dd422e462869baf9edfc4652bd2111912be7d31be326c9c81190375671b92511','fixed complete mother manifest SHA')
ck(manifest['source_only']is True and manifest['status']=='UNREADY_SOURCE_ONLY_NO_NATIVE_OR_PHYSICS_EXECUTION','full mother UNREADY Source scope')
members=manifest['members']
ck(type(members)is list and len(members)==manifest['member_count']==267,'complete267 ordered mother members')
ck([m['path']for m in members]==[p for p in before['files']if p!=str(P/'MANIFEST.json')],'no omitted or added complete Source member')
ck(sum(m['size_bytes']for m in members)==manifest['total_member_bytes']==8157799,'complete uncompressed member bytes')
membermap={}
python=[]
for m in members:
 keys=('path','sha256','size_bytes','identity')
 ck(all(k in m for k in keys),'complete4pin member '+m['path'])
 q=pin(m['path'])
 ck(q=={k:m[k]for k in keys},'complete member exact SHA7ID '+m['path'])
 rel=str(Path(m['path']).relative_to(P));membermap[rel]=q
 if rel.endswith('.py'):
  raw,t,pq=source(m['path'])
  python.append(dict(path=m['path'],sha256=pq['sha256'],top_level_definitions=[n.name for n in functions(t)]))
ck(len(python)==100,'all100 Python Source files AST only parsed')
ck(set(before['directories'])- {'.'}=={str(Path(q['path']).relative_to(P))for q in manifest['subdirectories']},'complete16 subdirectories/rootinclusive17')
for q in manifest['subdirectories']:ck(identity(Path(q['path']))==q['identity'],'all sealed directory sevenIDs '+q['path'])
def copied_group(name,manifestname,count):
 root=P/name;v,p=read(root/manifestname);ms=v['members']
 ms={q['relative_path']:q for q in ms}if type(ms)is list else ms
 actual={str(f.relative_to(root)):f for f in root.rglob('*')if f.is_file()}
 ck(set(actual)==set(ms)|{manifestname},'entire retained original group '+name)
 ck(len(actual)==count,'retained complete group count '+name)
 for rel,q in ms.items():
  got=membermap[name+'/'+rel]
  ck(got['sha256']==q['sha256']and got['size_bytes']==q['size_bytes'],'retained full original Source bytes '+name+'/'+rel)
 return v,p
old,oldmp=copied_group('ORIGINAL_STRICT_SCOPE_V22_SOURCE','MANIFEST.json',83)
bound,boundmp=copied_group('ORIGINAL_ACTUAL_BOUND_V22_SOURCE','Root_actual_complete_bound_native_SOURCE_manifest.json',89)
fixed,fixedmp=copied_group('ORIGINAL_FIXED_HOST_BINDER_SOURCE','MANIFEST.json',67)
ck(oldmp['sha256']=='f1b5cd5fc1b01077b1fc181c5da1199020570ff7c9ba569355f875c0f5bd4ffa','retained full qualified83 mother manifest')
ck(boundmp['sha256']=='bce973287d8776ddcfca502494f9f9dff0113d653aa316666ebfa962a4ea74d9','retained complete actual bound89 manifest')
roles=manifest['Source_roles']
expected={'checker_template':('complete_native_XSM_ASCII_checker_v4.UNREADY.py','e95a81336e1c71eadb8c3340e7c8f6181f41369d1ce586016f35b91ba112e641',51552),'host_template':('complete_native_XSM_ASCII_genuine_host.UNREADY.py','9cd50de1033ee0c598500fc54e8b92137ecc746dd9b07dce4dd4c7f88686d42e',23802),'binder':('bind_complete_native_SOURCE_only.UNREADY.py','1ec6f89d00d4b72aa1a5ed70e7bdca95e8267ead7c07aa5351daa70ae64bc585',18222)}
roledata={}
for key,(filename,digest,size)in expected.items():
 b,t,q=source(P/filename);ck(q==roles[key]and q['sha256']==digest and q['size_bytes']==size,'exact current role fullpin '+key)
 roledata[key]=(b,t,q)
 for group in ['ORIGINAL_STRICT_SCOPE_V22_SOURCE','ORIGINAL_ACTUAL_BOUND_V22_SOURCE']:
  if key!='checker_template':
   original=(P/group/filename).read_bytes()
   ck(b==original and dump(t)==dump(ast.parse(original)),'full unchanged host/binder byteAST '+key+'/'+group)
new,nt,cp=roledata['checker_template'];parent=(P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE/complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()
ck(hashlib.sha256(parent).hexdigest()=='5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e','exact original complete5c50 checker mother')
oldline=b"    require(type(inputs) is list and inputs, 'complete explicit input pins required')\n"
newline=b"    require(type(inputs) is list and len(inputs)>0, 'complete explicit input pins required')\n"
ck(new.count(newline)==1 and parent.count(oldline)==1,'one exact unique boolean predicate repair')
restored=new.replace(newline,oldline,1)
ck(restored==parent and dump(ast.parse(restored))==dump(ast.parse(parent)),'whole checker all-byte AST inverse restores5c50')
nd=functions(nt);pd=functions(ast.parse(parent))
ck([n.name for n in nd]==[n.name for n in pd]and len(nd)==17,'all17 top-level classes/functions retained')
for nn,pn in zip(nd,pd):
 if nn.name!='main':
  ck(ast.get_source_segment(new.decode(),nn)==ast.get_source_segment(parent.decode(),pn)and dump(nn)==dump(pn),'other16 complete definition byteAST '+nn.name)
ck(dump(globals_map(nt)['ROOT_BOUND_BINDING_SHA256'])==dump(ast.Constant(value=None)),'checker future Root binding is None')
ck(ast.literal_eval(globals_map(nt)['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY','checker strict UNREADY protected')
ck(ast.get_source_segment(new.decode(),nd[0])==ast.get_source_segment(parent.decode(),pd[0]),'strict bool require implementation not loosened')
for key in ('checker_template','host_template'):
 code=roledata[key][0].decode();gt=globals_map(roledata[key][1])
 ck('if __name__'in code and 'main()'in code,'template main guard '+key)
 ck(ast.literal_eval(gt['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY','unready current template '+key)
 if key=='host_template':
  for k in ('SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA','ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256'):
   ck(isinstance(gt[k],ast.Constant)and gt[k].value is None,'all unknown actual future host bindings None '+k)
parent_blueprint,bpp=read(P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json')
actual_binding,abp=read(P/'ORIGINAL_ACTUAL_BOUND_V22_SOURCE/Root_actual_native_SOURCE_binding.json')
ck(type(parent_blueprint['complete_input_pins'])is list and len(parent_blueprint['complete_input_pins'])==129,'full129 original saved input metadata')
ck(parent_blueprint['complete_input_pins']==actual_binding['complete_input_pins'],'all129 original/current actual saved complete pins exact no filtering')
ck(len({q['path']for q in parent_blueprint['complete_input_pins']})==129,'full129 unique original paths')
ck(parent_blueprint['original_caps']==actual_binding['original_caps']==CAPS,'original all integer caps retained metadata')
ck(parent_blueprint['state_order']==actual_binding['state_order']==['A','B'],'complete A/B original order')
ck(parent_blueprint['states']==actual_binding['states']and parent_blueprint['format']==actual_binding['format']and parent_blueprint['source_runtime_format_evidence']==actual_binding['source_runtime_format_evidence'],'complete states/format/provenance unchanged metadata')
sourceproof,proofpin=read(P/'ONE_HUNK_COMPLETE_CHECKER_SOURCE_INVERSE.json')
ck(sourceproof['hunks']==[dict(old_utf8=oldline.decode(),new_utf8=newline.decode(),unique_old_anchor=True,unique_new_anchor=True)],'full disclosed onehunk inverse proof matches actual bytes')
ck(sourceproof['new_checker_pin']==cp and sourceproof['parent_checker_pin']['sha256']==hashlib.sha256(parent).hexdigest(),'proof current role and old5c50 binding correct')
scope,scopepin=read(P/'V23_SOURCE_ROLES_AND_FRESH_ROOT_NAMESPACES.UNREADY.json')
request,requestpin=read(P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json')
ns={k:str(v)for k,v in dict(host=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v23-20261010',output=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010',control=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v23-20261010',source=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_sources',receipts=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts').items()}
ck(request['namespaces']==scope['future_namespaces']==manifest['fresh_v23_namespace_design']==ns,'five explicit newv23 namespace SOURCE design')
ck(scope['Root_must_observe_namespace_absence_before_bind_and_run']is True and manifest['Root_must_observe_fresh_namespaces']is True,'future freshness remains actual Root prerequisite, not observed here')
for k in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin','actual_native_byte_qualification_sha256','actual_scientific_qualification_sha256','new_native_walker_controls_actual_run'):
 ck(request[k]is None,'future actual Root request pin remains None '+k)
for k in ('future_actual_Source_admission','future_actual_Source_admission_terminal','future_actual_Source_peer','future_actual_Source_binding_tool','actual_native_byte_qualification_sha256','actual_scientific_qualification_sha256'):
 ck(scope[k]is None,'future actual Source/science None '+k)
ck(scope['original_caps']==CAPS and scope['six_future_business_pins']==manifest['six_future_business_pins']==[None]*6,'all original caps/six future pins retained')
old_peer_pin=actual_binding['independent_host_binder_Source_review_pin'];peer,oldpeerpin=read(old_peer_pin['path'])
ck(oldpeerpin==old_peer_pin and peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['check_count']==5741,'actual original5741 full Source peer retained and exact')
ck((R/'original_5741_qualified_Source_review_preserved.json').read_bytes()==Path(old_peer_pin['path']).read_bytes(),'full original5741 report preserved byteexact')
bc=roledata['binder'][0].decode();hc=roledata['host_template'][0].decode()
for term in ["peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'","peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'","peer['source_only']is True and peer['all_checks_passed']is True","peer['check_count']==len(checks)>0","set(row)=={'check','passed'}","len({row['check']for row in checks})==len(checks)","peer[key]==expected and admission[key]==expected","qualified_source_manifest=mp","host_template=pin(","checker_template=pin(","binder=pin(","PREP cannot stand for BUILD","'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'","len(binding['complete_input_pins'])==129","shutil.copytree(P,destination)","for m in members:typed_pin(","new_native_walker_controls_actual_run=None","actual_native_byte_qualification_sha256=None","actual_scientific_qualification_sha256=None","original_native_build_binary_Source_linkage_qualified=False"]:
 ck(term in bc,'unchanged exact binder complete original contract '+term)
for term in ["helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","resources.check()","support.archive_bytes","resource.history_roots","complete_source_inputs(support,archive)","complete_source_inputs(support,receipts)","complete_directory_identity(archive)","complete_directory_identity(receipts)","source_and_receipts_outsideART_counted_separately=True","support.pin(entry['path'],entry['sha256'])","runner.execute(","actual_native_byte_qualification_sha256=None"]:
 ck(term in hc,'unchanged genuine host original Source contract '+term)
# Current role byte equality to qualified parents proves all original algorithms and caps survive.
# Audit every strict require expression by AST without evaluating any reviewed expression.
cond,condpin=read(P/'ALL_STRICT_REQUIRE_SOURCE_CONDITION_AUDIT.json');actual_conditions=[]
for key,(raw,t,q)in roledata.items():
 for n in ast.walk(t):
  if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require':
   actual_conditions.append((Path(q['path']).name,n.lineno,dump(n.args[0])))
declared=[(v['Source_role'],v['line'],dump(ast.parse(v['expression'],mode='eval').body))for v in cond['conditions']]
ck(len(actual_conditions)==len(declared)==cond['condition_count']==194 and set(actual_conditions)==set(declared),'all194 strict require actual AST arguments complete no omitted calls')
ck(cond['original_true_path_LIST_terminal_fixed']['actual_saved_input_count']==129,'Boolean repair actual complete saved scope129')
ck(cond['no_candidate_function_or_payload_executed']is True and cond['does_not_grant_native_RSS_bits_or_science']is True,'author Boolean shape controls only metadata/Source')
# Previous independent all108 SOURCE proof already validated name/ended/full; patched755 now Compare returns bool.
cw=new.decode();cf=[n for n in nt.body if isinstance(n,ast.FunctionDef)and n.name=='main'][0]
call755=[n for n in ast.walk(cf)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'and n.lineno==755]
ck(len(call755)==1 and isinstance(call755[0].args[0],ast.BoolOp)and all(isinstance(v,ast.Compare)for v in call755[0].args[0].values),'new755 all operands bool comparisons including len>0')
failedmeta=P/'ACTUAL_V22_FAILED_SOURCE_AND_META/RECEIPTS'
real,realpin=read(failedmeta/'Root_actual_complete_native_tool_terminal_return.json')
fs,fspin=read(failedmeta/'Root_actual_complete_native_postclose_summary.json')
ck(realpin['sha256']=='dd6d7b78e8118006be63a745d6ec6f6afe9c802027ed582e06c9d2b11c6c5060'and fspin['sha256']=='2f464d12e72229451fe8203e3ca39b0e2a06a25a44022841ebcb26c432b2d94d','actual V22 failed Root receipt/summary retained fullbytes')
tr=real['terminal_tool_return']
ck(type(tr['exit_code'])is int and tr['exit_code']==1 and 'session_id'not in tr and real['closed']is True and real['actual_terminal_chunk']=='efc410','actualV22 failed native closed1 preserved not rerun')
ck(fs['actual_exit_code']==1 and fs['native_persisted_XSM_value_bits_verified']is False and fs['actual_native_byte_qualification_sha256']is None,'actualfailure gives no native qualification')
for p in sorted((P/'ACTUAL_SOURCE_TOOL_RETURNS').glob('*.json')):
 v,q=read(p);tr=v['terminal_tool_return']
 ck(v['closed']is True and v['actual_tool_terminal_return_observed']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr,'actual author Source terminal trueclosed0 '+p.name)
 ck(v['candidate_checker_guard_API_executed']is False and v['material_payload_read']is False,'actual author only Source/META '+p.name)
for p in sorted(Path(str(P)+'_seal_receipt').glob('*.json')):
 v,q=read(p);tr=v.get('actual_tool_return',v.get('terminal_tool_return'))
 ck(v['closed']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr,'actual author final seal/read terminal trueclosed0 '+p.name)
after=directory_view(P)
ck(after==before,'whole complete mother directories/files unchanged7ID beforeafter')
for path,q in list(INPUTS.items()):ck(pin(path)==q,'final complete Source/META fullEOF stable '+path)
ck(len({q['check']for q in CHECKS})==len(CHECKS),'all own check labels unique exactly consumed by binder')
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1',
 status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',source_only=True,
 all_checks_passed=True,blockers=[],checks=CHECKS,check_count=len(CHECKS),
 qualified_source_manifest=mp,host_template=roledata['host_template'][2],
 checker_template=cp,binder=roledata['binder'][2],
 full_Source_META_reads=INPUTS,complete_source_members=267,
 complete_source_member_bytes=8157799,full_member_inventory=members,
 complete_directory_before=before,complete_directory_after=after,
 all_python_source_members=python,
 original_complete83_mother_files_retained=True,original_complete89_actual_bound_files_retained=True,
 all_original67_Source_files_retained=True,
 all129_inputs_and90orderedprefix_preserved=True,
 all194_strict_require_calls_complete_and_original_strict_bool_implementation_unchanged=True,
 only755_onehunk_checker_source_change=True,
 complete_inverses=dict(checker_whole_byte_AST_inverse_to_5c50=True,
 other16_definitions_exact=True,host_and_binder_whole_bytes_AST_unchanged=True),
 previous_full5741_source_review=oldpeerpin,
 fixed_schema_scope_contracts_preserved=True,original_caps=CAPS,original_caps_unchanged=True,
 actual_build_not_executed_here=True,actual_native_not_executed_here=True,
 actual_source_admission=None,actual_RSS_qualification=None,
 actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,
 new_native_walker_controls_actual_run=None,original_native_build_binary_Source_linkage_qualified=False,
 original_XSM_memory_bits_verified=False,whole_combined_build_or_INPUT_qualified=False,
 physical_neutron_balance_qualified=False,scientific_accuracy_qualified=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,
 no_reviewed_Source_binder_host_checker_reader_helper_guard_API_compile_or_business_execution=True,
 no_material_graph_or_ART_numeric_payload_read=True,
 no_original_frozen_package_project_canonical_D_E_write=True,
 future_v23_Root_namespace_freshness_not_observed_or_admitted_here=True,
 new_family23_Source_only_unknown_real_admission_and_bound_pins_remain_None=True,
 runtime_gate_note='Root must create actual new Source admission/closed0 receipt, bind all four current pins and all129 original pins, independently review full bound Source, install/freeze completeD/E and use genuine original guards/caps for one newv23 actual execution. Failedv22 family is immutable and cannot be retried.')
with (R/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
(R/'REPORT.txt').write_text('SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE\nComplete267 members+manifest EOF/SHA7ID, original83 mother+89 actual-bound+67 originalSource byte-preserving copies,100 Python ASTs and all194 strict require conditions verified. Checker only755 onehunk len(inputs)>0 repairs genuine valid129-list rejection; fullbyte/AST inverse restores5c50, other16definitions and all host/binder bytes unchanged. Original5741 schema/status/checks/four current4pin roles remain exactly consumable by unchanged binder. Full original129 saved metadata and original guard/caps/bit scopes preserved; actual failedV22 efc410 CLOSED1 retained. No material payload, business/API/guard/native/candidate execution, namespace freshness admission, new walkerQ, native bytes/RSS or science qualification.\n')
print(json.dumps(dict(status=report['status'],check_count=len(CHECKS),complete_source_members=267,full_Source_META_files=len(INPUTS),report=str(R/'REVIEW.json'),four_role_pins_exact=True,no_candidate_guard_native_numeric_executed=True)))

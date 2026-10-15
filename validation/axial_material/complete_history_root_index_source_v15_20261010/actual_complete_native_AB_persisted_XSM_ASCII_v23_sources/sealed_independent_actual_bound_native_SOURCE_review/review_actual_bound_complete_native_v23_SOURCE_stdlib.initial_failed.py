
# This auditor preserves the whole original 8133 reference protocol, adapting
# only the explicitly observed v23 Source family, counts and genuine tool schema.
# It imports no reviewed Source and never reads complete material payloads.
"""SOURCE / saved META only. No reviewed binder, host, checker, helper, guard or reader runs."""
from pathlib import Path
import ast,hashlib,json,os,stat,struct,shutil
P=Path('/private/tmp/axmat_complete_native_v23_actual_BOUND_SOURCE_ROOT_20261010_748877')
A=Path('/private/tmp/axmat_native_v23_strict_bool_complete_SOURCE_ens_zo_p')
OUT=Path('/private/tmp/axmat_native_v23_actual_BOUND_complete_independent_SOURCE_review_20261010_599a7s57')
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
checks=[];pins={};raw={};first={}
def check(k,v):
    assert type(v)is bool;checks.append(dict(check='B%05d: %s'%(len(checks)+1,k),passed=v))
    if not v:raise ValueError(k)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
    p=Path(p);s=p.lstat();i=identity(s)
    check('real singlelink SOURCE/META '+str(p),p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    with p.open('rb')as f:
        check('open actual7ID '+str(p),identity(os.fstat(f.fileno()))==i);b=f.read()
        check('fullEOF '+str(p),len(b)==s.st_size and f.read(1)==b'');check('afterfd actual7ID '+str(p),identity(os.fstat(f.fileno()))==i)
    check('afterpath actual7ID '+str(p),identity(p.lstat())==i)
    q=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
    if str(p)in first:check('SOURCE/META fullpin unchanged '+str(p),q==first[str(p)])
    else:first[str(p)]=q
    pins[str(p)]=q;return b
def typed_pin(p):
    return type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and len(p['sha256'])==64 and all(c in'0123456789abcdef'for c in p['sha256'])and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int and v>=0 for v in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes']
def fixed(p):check('META exact typed4pin '+str(p.get('path')),typed_pin(p));b=read(p['path']);check('META actual exact4pin '+p['path'],pins[p['path']]==p);return b
def exact(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return list(a)==list(b)and all(exact(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
    if type(a)is float:return struct.pack('>d',a)==struct.pack('>d',b)
    return a==b
mp=P/'Root_actual_complete_bound_native_SOURCE_manifest.json';m=json.loads(read(mp))
check('real bound Source manifest dfb327',pins[str(mp)]['sha256']=='dfb3278dcab1c9db3af8dd82edace64dd24373c550c0b7d75047135144670958')
check('actual274 files complete273plusmanifest',type(m['members'])is dict and m['member_count']==len(m['members'])==273 and m['original_complete_parent_member_count']==267)
check('actualSource schema honest scope',m['schema']=='ROOT_ACTUAL_COMPLETE_BOUND_NATIVE_SOURCE_FULL_MANIFEST_V1'and m['source_only']is True and m['actual_native_execution']is False and m['whole_build_INPUT_science_qualified']is False)
dirs={str(q):identity(q.lstat())for q in[P,*sorted(q for q in P.rglob('*')if q.is_dir())]}
check('all274 file inventory exact',sorted(q.relative_to(P).as_posix()for q in P.rglob('*')if q.is_file())==sorted([*m['members'],mp.name]))
check('all fullSource entries regular or directories noaliases',all(not q.is_symlink()and(stat.S_ISDIR(q.lstat().st_mode)or stat.S_ISREG(q.lstat().st_mode))for q in P.rglob('*')))
py=[]
for name,v in m['members'].items():
    check('actual member exactrelative '+name,v['path']==str(P/name));raw[name]=fixed(v)
    if name.endswith('.py'):ast.parse(raw[name]);py.append(name);check('whole actualSource ASTvalid '+name,True)
am=json.loads(read(A/'MANIFEST.json'));check('author actual268 completefixedsource',pins[str(A/'MANIFEST.json')]['sha256']=='dd422e462869baf9edfc4652bd2111912be7d31be326c9c81190375671b92511'and len(am['members'])==267)
for v in am['members']:
    original=fixed({k:v[k]for k in('path','sha256','size_bytes','identity')});check('all full268 parentSource byte copies '+v['relative_path'],original==raw[v['relative_path']])
check('whole original author manifest preserved',read(A/'MANIFEST.json')==raw['MANIFEST.json'])
binding_name='Root_actual_native_SOURCE_binding.json';host_name='Root_bound_complete_native_genuine_host.py';checker_name='Root_bound_complete_native_checker.py';record_name='Root_actual_complete_native_Source_binding_record.json';inv_name='Root_actual_complete_native_Source_binding_inverse.json'
b=json.loads(raw[binding_name]);rec=json.loads(raw[record_name]);inv=json.loads(raw[inv_name])
for n,sha in[(binding_name,'765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87'),(host_name,'90d4cf339eaa2aceb01e9736f65443351c64948ff96496b8d6a416dcf022f76f'),(checker_name,'9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'),(record_name,'505ec5800adb2793837a717e0d504a6e1d636620cc347cc97c870f66daa19c5d')]:check('Root bound exactbodySHA '+n,pins[str(P/n)]['sha256']==sha)
check('complete actualbinding record manifestpin',m['actual_Source_binding_record']==pins[str(P/record_name)])
check('all actualrecord bound outputs exact',all(v==pins[str(P/n)]for n,v in rec['bound_outputs'].items())and set(rec['bound_outputs'])=={binding_name,host_name,checker_name,inv_name})
check('actualrecord currentSource scope',rec['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_RECORD_V1'and rec['source_only']is True and rec['complete_parent_Source_members']==267 and rec['complete_original_input_pins_count']==129 and rec['all_original_input_pins_preserved_exact']is True)
definitions=lambda t:{n.name:n for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
fingerprint=lambda n:ast.dump(n,include_attributes=False)
reverses=[]
for family,new_name,old_name,key,count in[('host',host_name,'complete_native_XSM_ASCII_genuine_host.UNREADY.py','host_full_inverse',11),('checker',checker_name,'complete_native_XSM_ASCII_checker_v4.UNREADY.py','checker_full_inverse',2)]:
    old=raw[old_name];new=raw[new_name];hunks=inv[key];check(family+' fullglobals inversecount',len(hunks)==count)
    back=new.decode().splitlines(keepends=True)
    for h in sorted(hunks,key=lambda h:h['one_based_line'],reverse=True):
        at=h['one_based_line']-1;check(family+' exactnew boundglobal '+h['name'],back[at:at+len(h['new_full_lines'])]==h['new_full_lines']);back[at:at+len(h['new_full_lines'])]=h['old_full_lines']
    restored=''.join(back).encode();check(family+' entire source bytes reverse original',restored==old)
    check(family+' entire source AST reverse original',fingerprint(ast.parse(restored))==fingerprint(ast.parse(old)))
    od,nd=definitions(old),definitions(new);check(family+' complete definitions same inventory',set(od)==set(nd))
    for name in od:check(family+' definition complete byteASTunchanged '+name,fingerprint(od[name])==fingerprint(nd[name])and ast.get_source_segment(old.decode(),od[name])==ast.get_source_segment(new.decode(),nd[name]))
    def globals(t):return {n.targets[0].id:n for n in ast.parse(t).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    og,ng=globals(old),globals(new);changed=[name for name in og if fingerprint(og[name])!=fingerprint(ng[name])]
    check(family+' only exactbound globals changed',set(og)==set(ng)and set(changed)=={h['name']for h in hunks})
    reverses.append(dict(name=family,full_inverse=hunks,complete_definition_count=len(od),all_definition_bytes_AST_unchanged=True,actual_changed_globals=changed))
parent=json.loads(raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'])
for key in parent:check('whole original binding metadata types/order/bits preserved '+key,exact(parent[key],b[key]))
check('all129 declared pins full exacttyped unique preserved',len(b['complete_input_pins'])==129 and len({v['path']for v in b['complete_input_pins']})==129 and all(typed_pin(v)for v in b['complete_input_pins'])and exact(parent['complete_input_pins'],b['complete_input_pins']))
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
check('alloriginal genuinecaps exactinteger',b['original_caps']==rec['original_caps']==caps and all(type(v)is int for v in b['original_caps'].values()))
namespaces=b['namespaces'];check('all5 exact namespaces',set(namespaces)=={'host','output','control','source','receipts'}and exact(namespaces,rec['future_actual_namespaces']))
ns={k:Path(v)for k,v in namespaces.items()};check('allroots literalabsolute nonoverlap',all(v.is_absolute()and '..'not in v.parts for v in ns.values())and len(set(ns.values()))==5 and not any(a.is_relative_to(z)for a in ns.values()for z in ns.values()if a!=z))
check('HOC actualART descendants DE separate B',all(ns[k].is_relative_to(ART)and ns[k]!=ART for k in('host','output','control'))and all(ns[k].is_relative_to(BASE)and ns[k]!=BASE for k in('source','receipts')))
check('all5 jointroots exactorder',b['joint_archive_roots']==[namespaces[k]for k in('host','output','control','source','receipts')])
for k in('actual_native_byte_qualification_sha256','actual_scientific_qualification_sha256','new_native_walker_controls_actual_run'):check('future true native/science actualunknown '+k,b[k]is None and rec[k]is None)
check('historicalRAM/Sourcebinary link notadmitted',b['original_native_build_binary_Source_linkage_qualified']is False and rec['original_native_build_binary_Source_linkage_qualified']is False and b['all_science_flags_false']is True)
request=json.loads(fixed(rec['request']));check('actualrequest exactsha scope',rec['request']['sha256']=='42d2f2d903fde7515f3c312c5e2f3c49ed2744aecade896ca14ca5eb5d2c8c7f'and request['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_REQUEST_V1'and request['source_only']is True)
check('all5 actualrequest namespaces exact',exact(request['namespaces'],namespaces))
meta={}
for k in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin'):
    check('actualrequest entire trueMeta pin '+k,request[k]==b[k]);meta[k]=json.loads(fixed(b[k]))
adm=meta['source_admission_pin'];peer=meta['independent_host_binder_Source_review_pin'];source_truth=meta['actual_Root_Source_admission_tool_return_pin'];build_truth=meta['prior_actual_V22_build_tool_return_pin']
check('complete Source peer exactschema status',peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['all_checks_passed']is True and peer['blockers']==[])
check('fullpeer4528 unique typedpass scope',type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==4528 and len({q['check']for q in peer['checks']})==4528 and all(type(q)is dict and set(q)=={'check','passed'}and q['passed']is True for q in peer['checks']))
for i,q in enumerate(peer['checks']):check('inherited whole Source peer4528 [%05d] '%i+q['check'],q['passed'])
check('actualRoot admission exactscope',adm['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'and adm['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and adm['source_only']is True and adm['scientific_qualification_created']is False and adm['actual_native_byte_qualification_sha256']is None and adm['actual_scientific_qualification_sha256']is None)
contract=b['actual_author_Source_contract'];check('complete4 exact authorSource scope',set(contract)=={'qualified_source_manifest','host_template','checker_template','binder'}and exact(contract,rec['actual_author_Source_contract']))
for k,v in contract.items():fixed(v);check('true currentSource peer/admission contract '+k,adm[k]==peer[k]==v)
check('same actualarchived peer report fullpin',adm['independent_Source_review_pin']==b['independent_host_binder_Source_review_pin'])
for label,v,schema,exitcode,chunk in[('Source',source_truth,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1',0,'748877'),('BUILD',build_truth,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1',1,'65203e')]:
    t=v['terminal_tool_return'];check(label+' exactgenuine observed CLOSED typedterminal',v['schema']==schema and v['closed']is True and v['observed_terminal']is True and v['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==exitcode and 'session_id'not in t and v['actual_terminal_chunk']==t['chunk_id']==chunk)
check('actual BUILD original launch/session/closes retained',build_truth['initial_tool_return']['chunk_id']=='197727'and type(build_truth['initial_tool_return']['session_id'])is int and build_truth['initial_tool_return']['session_id']==70899 and build_truth['observations'][-1]==build_truth['terminal_tool_return'])
for k in('whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','goal_complete'):check('actual failedBUILD no promotion '+k,build_truth[k]is False)
stdout=json.loads(source_truth['terminal_tool_return']['output']);check('Source actualstdout admission fullpin coupled',stdout['source_only']is True and stdout['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'and stdout['source_admission_pin']==b['source_admission_pin'])
check('actualrecord retains whole actual Source/failedBUILD truth',exact(rec['actual_Source_admission_tool_truth'],source_truth)and exact(rec['prior_actual_closed_V22_build_tool_truth'],build_truth))
coupling=b['actual_Source_scope_coupling'];check('complete actualscope proof precise',exact(coupling,rec['actual_Source_scope_coupling'])and coupling['schema']=='ACTUAL_COMPLETE_NATIVE_SOURCE_SCOPE_COUPLING_V1'and coupling['all_four_actual_author_Source_fullpins_coupled']is True and coupling['Source_admission_actual_tool_output_fullpin_coupled']is True and coupling['PREP_is_not_BUILD']is True and coupling['independent_full_Source_checks_count']==4528 and coupling['actual_Source_admission']==b['source_admission_pin']and coupling['actual_independent_Source_review']==b['independent_host_binder_Source_review_pin']and coupling['actual_author_Source_contract']==contract)
tool=json.loads(fixed(m['actual_Root_Source_binding_tool_receipt']));t=tool['terminal_tool_return'];check('actualbinder truef73f14 typed0 CLOSED',tool['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1'and tool['source_only']is True and tool['closed']is True and tool['observed_terminal']is True and tool['session_repolled_after_close']is False and tool['actual_terminal_chunk']==t['chunk_id'] and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='f73f14'and 'session_id'not in t)
returned=json.loads(t['output']);check('actualbinder fulloutput record and four Sourcepins coupled',returned['source_only']is True and returned['status']=='ACTUAL_NATIVE_SOURCE_BOUND_ONLY_NOT_INSTALLED_OR_RUN'and returned['complete_original_input_pins']==129 and returned['binding_record']==pins[str(P/record_name)]and returned['bound_outputs']==rec['bound_outputs'])
host=raw[host_name].decode();checker=raw[checker_name].decode();ht=ast.parse(host);ct=ast.parse(checker)
def literal_globals(t):
    r={}
    for n in t.body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:r[n.targets[0].id]=ast.literal_eval(n.value)
            except(ValueError,TypeError):pass
    return r
hg=literal_globals(ht);cg=literal_globals(ct)
check('exact actualBOUND target/binding paths SHA',hg['TARGET']==str(ns['source']/checker_name)and hg['TARGET_SHA']==pins[str(P/checker_name)]['sha256']and hg['BINDING']==str(ns['source']/binding_name)and hg['BINDING_SHA']==pins[str(P/binding_name)]['sha256']and hg['SOURCE_ADMISSION_SHA']==b['source_admission_pin']['sha256']and cg['ROOT_BOUND_BINDING_SHA256']==hg['BINDING_SHA'])
for k in('ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256','PROTOCOL','PROTOCOL_SHA'):check('host all futurefalse sourceunknown '+k,hg[k]is None)
for k,v in hg['FALSE'].items():check('complete host science/historical RAM false '+k,v is False)
for label,anchor in [('original619guard','helper.guard_admission(full)'),('original705/38deMRO','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)'),('dynamic complete5ARTroots','[str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)]'),('whole129 beforehash',"for p in b['complete_input_pins']:inputs.append(recheck_full_pin(support,p))"),('allinputs afterhash','for entry in inputs+[hpin,rpin,*genuine_pins]:'),('allDE beforeafter frozen dirs','complete_directory_identity(receipts)==receipt_directories'),('full5jointcounts','support.archive_bytes(roots5)'),('real fullchild mergedlog','actual_merged_child_stdout_and_stderr'),('no invented childseparatestderr',"'child_separate_stderr_saved':False"),('allmacro19619',"macro['records']==19619"),('serialone no retry','len(runner.records)==1'),('save actual failed native loss honestly','actual_native_report_pin_if_saved=')]:check('actualBound original nativehost '+label,anchor in host)
check('checker fulljournal/db/spool/temp jointly counted',"for root in self.joint_roots:"in checker and "os.environ['SQLITE_TMPDIR'] = str(Path(path).parent)"in checker and 'PRAGMA cache_size=-8192'in checker and 'PRAGMA mmap_size=0'in checker and 'PRAGMA temp_store=FILE'in checker)
check('actualBinding root sourceonly notqualification',b['source_only']is True and b['scientific_qualification_created']is False and b['Root_only_actual_execution']is True)
for k in('actual_source_installed','actual_genuine_host_run','actual_native_success'):check('actualbound Source honest unknown runtime '+k,rec[k]is None)
for name,v in m['members'].items():fixed(v)
for k in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin'):fixed(b[k])
fixed(m['actual_Root_Source_binding_tool_receipt']);read(mp);check('completebound directory7ID beforeafter',dirs=={str(q):identity(q.lstat())for q in[P,*sorted(q for q in P.rglob('*')if q.is_dir())]})

old_reference=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_AB_persisted_XSM_ASCII_v22_sources/sealed_independent_actual_bound_native_SOURCE_review/REVIEW.json')
oldref=json.loads(read(old_reference));check('preserved original8133 bound reference schema',pins[str(old_reference)]['sha256']=='8f585b96311e4818c99cddad4fe6b8032a19787d06ffc88e9bd9d04aeeab231b' and oldref['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1' and oldref['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY' and oldref['all_checks_typed_true'] is True and oldref['blockers']==[] and oldref['check_count']==len(oldref['checks'])==8133)
check('new_source_does_not_reuse_old_actual_native_or_science_credit',b['actual_native_byte_qualification_sha256'] is None and b['actual_scientific_qualification_sha256'] is None)
checker_main=definitions(raw[checker_name])['main']
check('755_exact_bool_fix_in_bound_checker',"require(type(inputs) is list and len(inputs)>0, 'complete explicit input pins required')" in checker)
if any(n.name=='require' for n in definitions(raw[checker_name]).values()):
    req=definitions(raw[checker_name])['require'];check('strict_require_unchanged_exact_bool_gate',"type(value) is not bool" in ast.get_source_segment(checker,req))
check('originalv22_failed_native_retained_as_failure_not_priorBUILD',json.loads(raw['ACTUAL_V22_FAILED_SOURCE_AND_META/RECEIPTS/Root_actual_complete_native_tool_terminal_return.json'])['terminal_tool_return']['exit_code']==1)
check('manifest_full_newparent_Source_not_runtime',m['original_complete_parent_member_count']==267 and m['actual_native_execution'] is False)
check('actual_admission_source_contract_precisely_request_coupled',exact(request['Source_admission_contract'],adm) and exact(request['actual_Source_admission_tool_contract']['terminal_tool_return'],source_truth['terminal_tool_return']))
check('actual_source_receipt_output_three_direct_values_not_fabricated',exact(request['actual_Source_admission_tool_contract']['required_actual_terminal_output'],stdout))
check('prior_BUILD_complete_schema_EXIT1_not_v22nativefailure',b['prior_actual_V22_build_tool_return_pin']['sha256']=='7b66ecbcac1048e079b8197a7821e12761d05c55d4ff6603555c53d220f09d07' and build_truth['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
check('all27fbeadmission_scope_and_4528peer_pin_current',b['source_admission_pin']['sha256']=='27fbe88b45493ce20b29a69866ecbab57a04cb1e1097ac564c92fea4ad99bc3e' and b['independent_host_binder_Source_review_pin']['sha256']=='9521056f8efefaefcd282a64a103feb52b841492ebf639647a8d24656c90fb1b')
read(old_reference);check('old8133_reference_fullpin_beforeafter',pins[str(old_reference)]==first[str(old_reference)])

check('complete allchecks unique typedtrue',all(v['passed']is True for v in checks)and len({v['check']for v in checks})==len(checks))
report=dict(schema='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],checks=checks,check_count=len(checks),actual_bound_Source_manifest_pin=pins[str(mp)],actual_binding_pin=pins[str(P/binding_name)],actual_host_pin=pins[str(P/host_name)],actual_checker_pin=pins[str(P/checker_name)],actual_Root_binding_tool_receipt_pin=m['actual_Root_Source_binding_tool_receipt'],actual_binding_record_pin=pins[str(P/record_name)],actualSource274_fullinventory=m['members'],all274_files_beforeafter_fixed=True,complete_directory_before=dirs,complete_directory_after=dirs,actual_Root_request_pin=rec['request'],actual_Root_Source_admission_pin=b['source_admission_pin'],actual_Root_Source_admission_terminal_pin=b['actual_Root_Source_admission_tool_return_pin'],actual_failed_BUILD_CLOSED1_pin=b['prior_actual_V22_build_tool_return_pin'],actual_complete_archived4528_Source_peer_pin=b['independent_host_binder_Source_review_pin'],all268_original_source_files_byteexact=True,all129_input_declarations_type_order_bit_exact=True,actual129_material_payloads_freshly_hashed_here=False,complete_11plus2_global_inverse=reverses,all_host_checker_definitions_byte_AST_unchanged=True,original_caps=caps,all5jointroots=namespaces,complete_Source_META_reads=pins,all_python_Source_members=py,
    actual_helper_checker_nativehost_guard_API_binder_or_reader_executed_here=False,material_native_ASCII_graph_or_ART_numeric_payload_read_here=False,canonical_frozen_D_E_or_any_project_written_here=False,actual_genuine_native_run=None,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,new_native_walker_controls_actual_run=None,original_native_build_binary_Source_linkage_qualified=False,original_XSM_memory_bits_verified=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    runtime_gate_note='Root alone installs full reviewed Source and freezes D/E, rechecks full129 actual inputs/fresh HOC and all Source/guard pins, then runs one genuine native stage serially under original caps. Failed V22 BUILD CLOSED1 is retained honestly and does not grant build/INPUT/science. E must not change during the run: capture actual outer tools/output externally and save after genuine CLOSED; child real merged log/watch live in H and count under caps. No separate stderr is invented. Material losses remain actual failure; Source pass is not native/RSS/physics qualification.')

report['original8133_bound_review_reference_pin']=pins[str(old_reference)]
report['original8133_count_not_claimed_as_new_run']=True
report['actual_source_file_count_including_manifest']=274
report['original_parent_source_file_count_including_manifest']=268
report['whole_combined_build_qualified']=False
report['whole_combined_INPUT_admitted']=False
report['physical_balance_qualified']=False
report['scientific_accuracy_qualified']=False
report['all_original_bound_review_contract_scope_retained']=True
report['all_six_future_business_pins_still_None']=all(hg[k] is None for k in ('ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256','PROTOCOL','PROTOCOL_SHA'))

(OUT/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(checks),blockers=[],review_sha256=hashlib.sha256((OUT/'REVIEW.json').read_bytes()).hexdigest(),no_candidate_or_material_payload_executed=True),indent=2))

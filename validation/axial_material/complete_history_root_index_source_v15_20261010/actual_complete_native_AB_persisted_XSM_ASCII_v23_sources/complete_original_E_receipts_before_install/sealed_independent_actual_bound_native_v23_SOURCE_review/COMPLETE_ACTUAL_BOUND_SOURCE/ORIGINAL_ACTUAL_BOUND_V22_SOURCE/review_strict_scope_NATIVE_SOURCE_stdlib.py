"""Complete stdlib Source AST/hash review; no reviewed candidate is executed."""
import ast, difflib, hashlib, json, os, stat
from pathlib import Path
P=Path(__file__).resolve().parent
OLD=P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE'
ORIGINAL=Path('/private/tmp/axmat_complete_native_genuine_host_BINDER_UNREADY_SOURCE_20261010_pddg3kw5')
checks=[]
def check(name,v):
    if type(v)is not bool or not v:raise ValueError(name)
    checks.append(dict(check=name,passed=True))
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();check('regular typed Source file '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    with p.open('rb')as f:
        check('Source open7ID '+str(p),ident(os.fstat(f.fileno()))==ident(s))
        raw=f.read();check('Source EOF7ID '+str(p),ident(os.fstat(f.fileno()))==ident(s)and len(raw)==s.st_size)
    check('Source path7ID '+str(p),ident(p.lstat())==ident(s))
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s)),raw
def defs(raw):return{n.name:ast.dump(n,include_attributes=False)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def reverse(label,proof,original,new):
    a=original.decode().splitlines(keepends=True);b=new.decode().splitlines(keepends=True)
    changes=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal':changes.append(dict(tag=tag,original_zero_based_start=i,original_zero_based_end=j,derived_zero_based_start=k,derived_zero_based_end=l,original_full_lines=a[i:j],derived_full_lines=b[k:l]))
    check(label+' all independent full inverse hunks exact',proof['hunks']==changes)
    back=b[:]
    for h in reversed(changes):
        check(label+' full inverse hunk '+str(h['derived_zero_based_start']),back[h['derived_zero_based_start']:h['derived_zero_based_end']]==h['derived_full_lines'])
        back[h['derived_zero_based_start']:h['derived_zero_based_end']]=h['original_full_lines']
    check(label+' all parent Source bytes restore',''.join(back).encode()==original)
    aa,bb=defs(original),defs(new)
    check(label+' all parent topdefs retained',set(aa)<=set(bb))
    return dict(full_hunk_count=len(changes),unchanged_AST=[x for x in aa if aa[x]==bb[x]],changed_AST=[x for x in aa if aa[x]!=bb[x]],added_defs=sorted(set(bb)-set(aa)))
oldmanifest=json.loads((ORIGINAL/'MANIFEST.json').read_bytes())
check('known original fixed30958 complete manifest SHA',pin(ORIGINAL/'MANIFEST.json')[0]['sha256']=='30958ca0bf049fa02d9b205ed5b89fa07e62092be497df7fa97f2ce3ce00decf')
check('parent original67 full copied member paths',sorted(str(f.relative_to(OLD))for f in OLD.rglob('*')if f.is_file())==sorted(str(f.relative_to(ORIGINAL))for f in ORIGINAL.rglob('*')if f.is_file()))
for f in sorted(ORIGINAL.rglob('*')):
    if f.is_dir():continue
    actual,raw=pin(f);copy,copyraw=pin(OLD/f.relative_to(ORIGINAL))
    check('full original Source byte copy '+str(f),raw==copyraw)
    if f!=ORIGINAL/'MANIFEST.json':
        expected=next(m for m in oldmanifest['members']if m['path']==str(f))
        check('original unchanged complete30958 member fullpin '+str(f),actual=={k:expected[k]for k in actual})
original35=json.loads((OLD/'PARENT_NATIVE_SOURCE/ORIGINAL_SOURCE_PROVENANCE_PINS.json').read_bytes())['pins']
check('all original35 Source retained',len(original35)==35)
for expected in original35:
    actual,raw=pin(Path(expected['path']))
    check('original35 full original Source SHA7ID unchanged '+expected['path'],actual=={k:expected[k]for k in actual})
proof=json.loads((P/'STRICT_SCOPE_FULL_SOURCE_INVERSE_PROOF.json').read_bytes())
check('strict fullproof no execution',proof['source_only']is True and proof['no_candidate_execution']is True and proof['zero_based_line_ranges']is True)
review={}
for key,name in [('host','complete_native_XSM_ASCII_genuine_host.UNREADY.py'),('binder','bind_complete_native_SOURCE_only.UNREADY.py')]:
    oldpin,old=pin(OLD/name);newpin,new=pin(P/name)
    check(key+' derived fullpin proof',newpin==proof[key]['derived'])
    review[key]=reverse(key,proof[key],old,new)
check('host original7 functions AST unchanged',review['host']['unchanged_AST']==['require','strict_json','complete_source_inputs','observed_stage','typed_full_pin','recheck_full_pin','complete_directory_identity'])
check('host only prior/toolscope and main changed',review['host']['changed_AST']==['actual_closed_prior','main']and review['host']['added_defs']==['source_scope_contract'])
check('binder original6 functions AST unchanged',review['binder']['unchanged_AST']==['require','strict_json','identity','pin','typed_pin','bind_globals'])
check('binder only terminal and main changed',review['binder']['changed_AST']==['actual_terminal','main']and review['binder']['added_defs']==['source_scope_contract'])
checker=(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()
check('complete checker exact51KiB SHA unchanged',checker==(OLD/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()and hashlib.sha256(checker).hexdigest()=='5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e')
source_snapshot=[]
for f in sorted(P.rglob('*')):
    check('no Source package aliases '+str(f),not f.is_symlink())
    if f.is_file():
        actual,raw=pin(f);source_snapshot.append(actual)
        if f.suffix=='.py':check('all complete Source AST '+str(f),isinstance(ast.parse(raw,filename=str(f)),ast.Module))
host=(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py').read_text();binder=(P/'bind_complete_native_SOURCE_only.UNREADY.py').read_text()
for label,s in [('host',host),('binder',binder)]:
    for name,fragment in {
        'genuine Root observation closed':"value['closed']is True and value['observed_terminal']is True",
        'no postclose repoll':"value['session_repolled_after_close']is False",
        'actual schema bound family':"value['schema']==expected_schema",
        'actual same terminal chunk':"value['actual_terminal_chunk']==",
        'Build separate family':"ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1",
        'Source separate witness family':"ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1",
        'peer exact schema':"peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'",
        'peer software only':"peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'",
        'peer allchecks typed and no blockers':"peer['source_only']is True and peer['all_checks_passed']is True",
        'peer complete checks exactcount':"type(peer['check_count'])is int and peer['check_count']==len(checks)>0",
        'peer check duplicate forbid':"len({row['check']for row in checks})==len(checks)",
        'admission exact Source family':"admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'",
        'Source-only admission status':"admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'",
        'future native Q unknown':"admission['actual_native_byte_qualification_sha256']is None",
        'future scientific Q unknown':"admission['actual_scientific_qualification_sha256']is None",
        'full fourpin coupled':"peer[key]==expected and admission[key]==expected",
        'same peer report pin':"admission['independent_Source_review_pin']==request['independent_host_binder_Source_review_pin']",
        'actual admission tool output exact pin':"output['source_admission_pin']==request['source_admission_pin']",
        'actual admission tool output softwareonly':"output['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'",
    }.items():check(label+' strict scope '+name,fragment in s)
check('Source binder uses this actual manifest/template/body pins',all(x in binder for x in ("qualified_source_manifest=mp","host_template=pin(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py')","checker_template=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py')","binder=pin(Path(__file__).resolve())")))
check('Source binder coupling before any destination mutation',binder.index('scope_coupling=source_scope_contract(')<binder.index('shutil.copytree(P,destination)'))
check('Source binder checks all actualpins/coupling after',"all Source admission/peer coupling unchanged after Source binding"in binder)
check('actual source contract passed to bound runtime',"actual_author_Source_contract=expected_sources,actual_Source_scope_coupling=scope_coupling"in binder and "scope_coupling==b['actual_Source_scope_coupling']"in host)
check('host all fourSource actual full EOF pins',"for p in expected_sources.values():inputs.append(recheck_full_pin(support,p))"in host)
check('genuine guard/MRO entire import usage kept',all(fragment in host for fragment in ("support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')","helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","full.OwnRSSSerialExecutor(host,remaining,'COMPLETE_NATIVE_XSM_ASCII',resources)")))
check('one actual600 native stage only',host.count('runner.execute(')==1 and "runner.execute(host/'native_run','native_xsm_ascii',command,STAGE_CAP)"in host)
check('no runtime/process/environment overrides',all(x not in host for x in ('runner.env[','runner.env =','full.OwnRSSSerialExecutor=','full.OwnRSSSerialExecutor =','runner._process=','runner._process =')))
assign={n.targets[0].id:n.value for n in ast.parse(host).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check('native host UNREADY refuses execution',ast.literal_eval(assign['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY')
for name in ('SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA','ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256'):
    check('all futureRoot host namespace/pin/Q unknown '+name,ast.literal_eval(assign[name])is None)
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def static_constant(node):
    if isinstance(node,ast.Constant)and type(node.value)in(int,str):return node.value
    if isinstance(node,ast.Dict):return {static_constant(k):static_constant(v)for k,v in zip(node.keys,node.values)}
    if isinstance(node,ast.BinOp)and isinstance(node.op,(ast.Mult,ast.Pow)):
        a,b=static_constant(node.left),static_constant(node.right)
        check('caps arithmetic AST only bounded integer '+str(node.lineno)+':'+str(node.col_offset),type(a)is int and type(b)is int and 0<=a<=2**40 and 0<=b<=2**40 and (not isinstance(node.op,ast.Pow)or b<=40))
        return a*b if isinstance(node.op,ast.Mult)else a**b
    raise ValueError('nonconstant caps Source AST')
check('all original host caps exact',static_constant(assign['CAPS'])==CAPS)
blueprint=json.loads((OLD/'PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json').read_bytes())
check('all original129 inputs complete scope',len(blueprint['complete_input_pins'])==129 and len({p['path']for p in blueprint['complete_input_pins']})==129)
check('original complete blueprint caps unchanged',blueprint['original_caps']==CAPS and all(type(v)is int for v in blueprint['original_caps'].values()))
check('allSource129 before and after unchanged',"for p in b['complete_input_pins']:inputs.append(recheck_full_pin(support,p))"in host and "for entry in inputs+[hpin,rpin,*genuine_pins]:"in host)
check('complete D/E files and all directories freeze preserved',all(x in host for x in ('complete_source_inputs(support,archive)==source_inputs','complete_source_inputs(support,receipts)==receipt_inputs','complete_directory_identity(archive)==source_directories','complete_directory_identity(receipts)==receipt_directories')))
check('all output HOCDE2GiB counted',"roots5=(host,out,control,archive,receipts)"in host and "support.archive_bytes(roots5)"in host and "for root in self.joint_roots:"in checker.decode())
check('all originalmacro scope bit loss realfail',"macro['records']==19619"in host and "macro['physical_headers_including_all_closes']==19990"in host and "macro['numeric_components']==2264113"in host and 'actual_native_report_pin_if_saved='in host)
check('allmicro unchanged no scope narrowing',"for v in(macro,micro)"in host and 'new_native_walker_controls_actual_run=None'in host and 'original_native_build_binary_Source_linkage_qualified=False'in host)
check('binder onlystdlibSource no candidate exec',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in ('exec','eval','compile','__import__')for n in ast.walk(ast.parse(binder)))and all(x not in binder for x in ('importlib','runpy','subprocess')))
check('freshTMP fullSource binder no projectwrites',"destination.is_relative_to(Path('/private/tmp'))"in binder and 'shutil.copytree(P,destination)'in binder)
request=json.loads((P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())
check('all request4actual pins None',all(request[k]is None for k in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin')))
prep=json.loads((P/'ACTUAL_ROOT_PREP_RECEIPT_SHAPE_ONLY_NOT_BUILD.json').read_bytes())
check('real exact PREPcopy SHA566ef',hashlib.sha256((P/'ACTUAL_ROOT_PREP_RECEIPT_SHAPE_ONLY_NOT_BUILD.json').read_bytes()).hexdigest()=='566ef1b8647709212b9e1c603d2b6559f2920053c36ee7c4520d1dd0c410549e')
check('true observed_terminal not fictional observed',prep['closed']is True and prep['observed_terminal']is True and 'observed'not in prep and prep['session_repolled_after_close']is False and prep['actual_terminal_chunk']==prep['terminal_tool_return']['chunk_id']=='fc5201'and type(prep['terminal_tool_return']['exit_code'])is int and prep['terminal_tool_return']['exit_code']==0 and 'session_id'not in prep['terminal_tool_return'])
check('PREPSource shape only not BUILD',prep['schema']=='ROOT_V22_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1'and "PREP cannot authorize BUILD"in(P/'ROOT_EXECUTION_SEQUENCE_AND_REQUIRED_PINS.md').read_text())
for expected in source_snapshot:
    actual,_=pin(Path(expected['path']));check('complete Source unchanged across finite review '+expected['path'],actual==expected)
hostpin=pin(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py')[0]
checkerpin=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py')[0]
binderpin=pin(P/'bind_complete_native_SOURCE_only.UNREADY.py')[0]
report=dict(schema='STRICT_SCOPE_COMPLETE_NATIVE_GENUINE_HOST_BINDER_UNREADY_SOURCE_REVIEW_V1',source_only=True,status='AUTHOR_SOURCE_ONLY_STATIC_PASS_NOT_RUNTIME_OR_SCIENCE',all_checks_passed=True,blockers=[],checks=checks,check_count=len(checks),host_template=hostpin,checker_template=checkerpin,binder=binderpin,full_inverse_review=review,parent_fixed_Source_copied_files=67,all_original129_inputs_retained=True,all35originalSource_unchanged=True,complete_micro_and_macro_retained=True,original_caps=CAPS,no_candidate_helper_API_guard_compile_business_or_payload_execution=True,no_originalSource_project_ART_frozen_D_E_write=True,actual_source_admission=None,actual_prior_BUILD=None,actual_genuine_host=None,actual_native_success=None,actual_RSS_qualification=None,new_native_walker_controls_actual_run=None,original_native_build_binary_Source_linkage_qualified=False,original_XSM_memory_bits_verified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(P/'STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,check_count=report['check_count'],host_template=hostpin,checker_template=checkerpin,binder=binderpin,report=pin(P/'STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json')[0],inverse_review=review,no_candidate_execution=True),indent=2,allow_nan=False),flush=True)

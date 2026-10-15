"""Only standard-library SOURCE/META byte reads and AST analysis. No reviewed code runs."""
from pathlib import Path
import ast,difflib,hashlib,json,os,stat,shutil
P=Path('/private/tmp/axmat_native_host_BINDER_STRICT_SCOPE_UNREADY_SOURCE_20261010_gs2tnzvo')
OLD=Path('/private/tmp/axmat_complete_native_genuine_host_BINDER_UNREADY_SOURCE_20261010_pddg3kw5')
OUT=Path('/private/tmp/axmat_native_STRICT_SCOPE_complete_SOURCE_peer_l4us4hq0')
PREVIOUS=Path('/private/tmp/axmat_native_full_genuine_host_SOURCE_contract_peer_6ijwnmf5')
CHECKER_PEER=Path('/private/tmp/axmat_complete_native_XSM_ASCII_independent_SOURCE_review_wt06uxea')
checks=[];pins={};before={};raw={}
def check(label,value):
    if type(value)is not bool:raise TypeError(label)
    checks.append(dict(check='S%05d: %s'%(len(checks)+1,label),passed=value))
    if not value:raise ValueError(label)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
    p=Path(p);s=p.lstat();i=identity(s)
    check('real singlelink SOURCE/META '+str(p),p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    with p.open('rb')as f:
        check('opened exact7ID '+str(p),identity(os.fstat(f.fileno()))==i)
        b=f.read();check('complete EOF '+str(p),len(b)==s.st_size and f.read(1)==b'')
        check('opened final7ID '+str(p),identity(os.fstat(f.fileno()))==i)
    check('path final7ID '+str(p),identity(p.lstat())==i)
    pin=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
    if str(p)in before:check('actual full Source/META unchanged '+str(p),pin==before[str(p)])
    else:before[str(p)]=pin
    pins[str(p)]=pin;return b
def fullpin(v):return {k:v[k]for k in ('path','sha256','size_bytes','identity')}
def definitions(b):return {n.name:n for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def fingerprint(n):return ast.dump(n,include_attributes=False)
def inherit(p,sha,label,expected_count):
    report=json.loads(read(p));check(label+' report exact fixed full SHA',pins[str(p)]['sha256']==sha)
    check(label+' complete original typedchecks',report['check_count']==len(report['checks'])==expected_count and all(type(v)is dict and v['passed']is True for v in report['checks']))
    for i,v in enumerate(report['checks']):check(label+' full prior check %05d: %s'%(i,v['check']),v['passed'])
    return report
initial=inherit(PREVIOUS/'ORIGINAL_30958_SOURCE_REVIEW.json','a4adb4df059b1a4265621686cb1edab3cf8ce66dc8e3466b073b35570881ff18','complete original 30958',1727)
check('two genuine prior Source blockers preserved',len(initial['blockers'])==2 and initial['status']=='SOURCE_ONLY_BLOCKED_PENDING_STRICT_ROOT_META_SCOPE_BINDING')
checker_prior=inherit(CHECKER_PEER/'REVIEW.json','123729db69ab0f9851c5d2d6960dc2d63ad11b5db05935ce8e74418d534e7393','complete original native v3',1473)
manifest=json.loads(read(P/'MANIFEST.json'))
check('fixed full manifest f1b5',pins[str(P/'MANIFEST.json')]['sha256']=='f1b5cd5fc1b01077b1fc181c5da1199020570ff7c9ba569355f875c0f5bd4ffa')
members=manifest['members']
check('all82 members full bytes',len(members)==manifest['member_count']==82 and sum(v['size_bytes']for v in members)==manifest['total_member_bytes']==2206438)
actual_dirs={str(q):identity(q.lstat())for q in [P,*sorted(q for q in P.rglob('*')if q.is_dir())]}
check('complete frozen directories exact7ID',actual_dirs==manifest['directories'])
check('all full file names no omitted files',sorted(q.relative_to(P).as_posix()for q in P.rglob('*')if q.is_file())==sorted([v['relative_path']for v in members]+['MANIFEST.json']))
check('all package entries unaliased regular/directory',all(not q.is_symlink()and(stat.S_ISREG(q.lstat().st_mode)or stat.S_ISDIR(q.lstat().st_mode))for q in P.rglob('*')))
pyfiles=[]
for v in members:
    q=P/v['relative_path'];b=read(q);raw[v['relative_path']]=b
    check('every full member path/SHA/size7ID '+v['relative_path'],pins[str(q)]==fullpin(v))
    if q.suffix=='.py':ast.parse(b);pyfiles.append(v['relative_path']);check('whole Source AST parses '+v['relative_path'],True)
oldmanifest=json.loads(read(OLD/'MANIFEST.json'))
check('actual original30958 manifest fixed',pins[str(OLD/'MANIFEST.json')]['sha256']=='30958ca0bf049fa02d9b205ed5b89fa07e62092be497df7fa97f2ce3ce00decf')
check('all67 original files copied exactly',len(oldmanifest['members'])+1==manifest['parent_source_full_copy_count']==67)
for v in oldmanifest['members']:
    b=read(Path(v['path']));check('original fixed Source fullpin '+v['relative_path'],pins[v['path']]==fullpin(v))
    check('original whole Source byte copy '+v['relative_path'],b==raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/'+v['relative_path']])
check('full original manifest byte copy',read(OLD/'MANIFEST.json')==raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/MANIFEST.json'])
provenance=json.loads(raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ORIGINAL_SOURCE_PROVENANCE_PINS.json'])
originals=[]
for v in provenance['pins']:
    b=read(Path(v['path']));check('all35 original Source current exactpin '+v['path'],pins[v['path']]=={k:w for k,w in v.items()if k!='saved_source_path'})
    check('all original Source full bytes copied '+v['path'],b==raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/SOURCE_PROVENANCE/'+Path(v['saved_source_path']).name]);originals.append(pins[v['path']])
check('original provenance whole35',len(originals)==35)
proof=json.loads(raw['STRICT_SCOPE_FULL_SOURCE_INVERSE_PROOF.json']);reverses=[]
check('exact Source inverse full SHA',pins[str(P/'STRICT_SCOPE_FULL_SOURCE_INVERSE_PROOF.json')]['sha256']=='d4849192862d045b972f6d5ef2f75f7449f8a15fb4238b817111ffd4cbd44010')
for name,count,same,changed in [('host',6,7,['actual_closed_prior','main']),('binder',9,6,['actual_terminal','main'])]:
    v=proof[name];old=read(v['original']['path']);new=read(v['derived']['path'])
    check(name+' full proof pins true',pins[v['original']['path']]==v['original']and pins[v['derived']['path']]==v['derived'])
    ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);actual=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
        if tag!='equal':actual.append(dict(tag=tag,original_zero_based_start=a,original_zero_based_end=b,derived_zero_based_start=c,derived_zero_based_end=d,original_full_lines=ol[a:b],derived_full_lines=nl[c:d]))
    check(name+' all finite hunks exact',len(actual)==count and actual==v['hunks'])
    back=nl[:]
    for h in reversed(v['hunks']):
        a,b=h['derived_zero_based_start'],h['derived_zero_based_end'];check(name+' exact inverse hunk '+str(a),back[a:b]==h['derived_full_lines']);back[a:b]=h['original_full_lines']
    inverse=''.join(back).encode();check(name+' entire original bytes restored',inverse==old)
    check(name+' entire original AST restored',fingerprint(ast.parse(inverse))==fingerprint(ast.parse(old)))
    od,nd=definitions(old),definitions(new);unchanged=[k for k in od if fingerprint(od[k])==fingerprint(nd[k])]
    check(name+' every original definition retained',set(od)<=set(nd))
    check(name+' complete unchanged definitions',len(unchanged)==same)
    check(name+' complete changed and new definitions',[k for k in od if k not in unchanged]==changed and set(nd)-set(od)=={'source_scope_contract'})
    # Global AST statements other than definitions remain exactly original.
    globals_only=lambda b:[fingerprint(n)for n in ast.parse(b).body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    check(name+' every original global/import/cap unchanged',globals_only(old)==globals_only(new))
    reverses.append(dict(name=name,complete_full_inverse=v,original_definitions=list(od),candidate_definitions=list(nd),unchanged_AST=unchanged,changed_AST=changed,new_AST=['source_scope_contract']))
host=raw['complete_native_XSM_ASCII_genuine_host.UNREADY.py'].decode();binder=raw['bind_complete_native_SOURCE_only.UNREADY.py'].decode();checker=raw['complete_native_XSM_ASCII_checker_v4.UNREADY.py']
check('complete v4 checker exact51545 byte scope unchanged',checker==raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/complete_native_XSM_ASCII_checker_v4.UNREADY.py']and hashlib.sha256(checker).hexdigest()=='5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e')
hd,bd=definitions(host),definitions(binder)
normalized=ast.parse(ast.get_source_segment(host,hd['source_scope_contract']).replace('typed_full_pin(','typed_pin('))
check('same complete fourpin scope validator in host and binder',fingerprint(normalized.body[0])==fingerprint(bd['source_scope_contract']))
for family,source,fn in [('host',host,hd['actual_closed_prior']),('binder',binder,bd['actual_terminal'])]:
    text=ast.get_source_segment(source,fn)
    for label,anchor in [('closed exactbool',"value['closed']is True"),('actual observation exactbool',"value['observed_terminal']is True"),('never repoll exactbool',"value['session_repolled_after_close']is False"),('specificfamily',"value['schema']==expected_schema"),('exit exact integer',"type("+('actual'if family=='host'else'terminal')+"['exit_code'])is int"),('no live session',"'session_id'not in "+('actual'if family=='host'else'terminal')),('observed exact chunk',"value['actual_terminal_chunk']=="+('actual'if family=='host'else'terminal')+"['chunk_id']"),('Source0 / honest anybuildexit',"not zero or "+('actual'if family=='host'else'terminal')+"['exit_code']==0")]:
        check(family+' exact terminal '+label,anchor in text)
    check(family+' does not accept PREP as BUILD',"ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1"in source and "ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1"in source)
for family,source in [('host',host),('binder',binder)]:
    text=ast.get_source_segment(source,definitions(source)['source_scope_contract'])
    anchors=[('peer exact schema',"peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'"),('peer Sourceonly status',"peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'"),('allchecks typedPASS',"peer['all_checks_passed']is True"),('no blockers',"type(peer['blockers'])is list and peer['blockers']==[]"),('check_count exactint complete',"type(peer['check_count'])is int and peer['check_count']==len(checks)>0"),('full checks exactfields',"set(row)=={'check','passed'}"),('checks typedtrue',"row['passed']is True"),('checks unique',"len({row['check']for row in checks})==len(checks)"),('Sourceadmission exactschema',"admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'"),('Sourceadmission scopedstatus',"admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'"),('Sourceadmission no science',"admission['scientific_qualification_created']is False"),('unknown byteQ',"admission['actual_native_byte_qualification_sha256']is None"),('unknown scienceQ',"admission['actual_scientific_qualification_sha256']is None"),('all4 scopefullpins',"peer[key]==expected and admission[key]==expected"),('same full peerpin',"admission['independent_Source_review_pin']==request['independent_host_binder_Source_review_pin']"),('actual stdout JSON retained',"strict_json(source_truth['terminal_tool_return']['output'])"),('actual stdout scope',"output['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'"),('actual stdout admission fullpin',"output['source_admission_pin']==request['source_admission_pin']")]
    for label,anchor in anchors:check(family+' complete scope '+label,anchor in text)
    check(family+' four fullpins structurally typed before equality',('typed_full_pin(peer[key]);typed_full_pin(admission[key])'if family=='host'else'typed_pin(peer[key]);typed_pin(admission[key])')in text)
for label,anchor in [('wholeoriginal129',"len(binding['complete_input_pins'])==129"),('allSource fullcopy',"shutil.copytree(P,destination)"),('METAonly nooriginal materialread',"Binder never reads them; the genuine host and native checker hash all129"),('Source scope prebinding',"scope_coupling=source_scope_contract(request,expected_sources,source_truth)"),('Source scope afterbinding',"==scope_coupling,'all Source admission/peer coupling unchanged after Source binding'"),('actualbuild family afterbinding',"actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')"),('fulloriginal globals inverse',"all original Source bytes must restore"),('future freshonly',"all(not os.path.lexists(paths[key])for key in ('host','output','control','source'))")]:check('binder '+label,anchor in binder)
for label,anchor in [('genuine619 guard',"helper.guard_admission(full)"),('705/38de exact MRO',"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)"),('5121800600 originalcaps',"WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30"),('96history8free',"DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30"),('5 original ART scope',"[str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)]"),('full129 before',"for p in b['complete_input_pins']:inputs.append(recheck_full_pin(support,p))"),('fullall inputs after',"for entry in inputs+[hpin,rpin,*genuine_pins]:"),('HOCDE allroots',"roots5=(host,out,control,archive,receipts)"),('complete 5root before',"support.archive_bytes(roots5)<ARCHIVE_CAP"),('allSource E dirs beforeafter',"complete_directory_identity(receipts)==receipt_directories"),('one actual fullstage',"len(runner.records)==1"),('macrofull19619',"macro['records']==19619 and macro['physical_headers_including_all_closes']==19990 and macro['numeric_components']==2264113"),('allmicro nativebits physicalorder',"v['native_physical_preorder_equal_original_ASCII']is True"),('unexecuted protocolNone',"new_native_walker_controls_actual_run=None"),('no newQ',"actual_native_byte_qualification_sha256=None"),('binarylinkage honestfalse',"original_native_build_binary_Source_linkage_qualified=False"),('failure truthfulsavedfullreport',"actual_native_report_pin_if_saved=support.pin(saved)if saved.is_file()"),('Source scope preguard',"scope_coupling=source_scope_contract(b,expected_sources,source_truth)")]:check('whole genuinehost '+label,anchor in host)
tree=ast.parse(binder)
check('Root Sourcebinder noAPI/import reviewedSource/guard/run',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','exec_module','Popen','run')for n in ast.walk(tree)))
main=hd['main'];segments=[ast.get_source_segment(host,n)for n in main.body]
check('UNREADY prior any dynamic projectimport',next(i for i,v in enumerate(segments)if v.startswith('require(SOURCE_STATUS'))<next(i for i,v in enumerate(segments)if 'spec.loader.exec_module' in v))
check('exact four expectedSource keys host',"set(expected_sources)=={'qualified_source_manifest','host_template','checker_template','binder'}"in host)
check('binder expectedSource actualfresh pins',"qualified_source_manifest=mp"in binder and "binder=pin(Path(__file__).resolve())"in binder)
blueprint=json.loads(raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'])
parent=json.loads(raw['ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/SAVED_RAW_TRANSFER_PARENT_META.json'])
check('all129 unique and ordered90 oldprefix complete',len(blueprint['complete_input_pins'])==len({v['path']for v in blueprint['complete_input_pins']})==129 and len(parent['rawrecord_binding']['input_pins'])==90 and blueprint['complete_input_pins'][:90]==parent['rawrecord_binding']['input_pins'])
request=json.loads(raw['ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json'])
check('all4 future trueMETA pins None',all(request[k]is None for k in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin')))
check('future exact namespace5 all None',set(request['namespaces'])=={'host','output','control','source','receipts'}and all(v is None for v in request['namespaces'].values()))
check('futurebuild explicitschema notPREP',request['actual_prior_BUILD_tool_contract']['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'and request['actual_prior_BUILD_tool_contract']['PREP_cannot_substitute_BUILD']is True)
prep=json.loads(raw['ACTUAL_ROOT_PREP_RECEIPT_SHAPE_ONLY_NOT_BUILD.json'])
check('realPREP receipt kept shapeonly notBUILD',prep['schema']=='ROOT_V22_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1'and prep['closed']is True and prep['observed_terminal']is True and type(prep['terminal_tool_return']['exit_code'])is int and prep['terminal_tool_return']['exit_code']==0)
author=json.loads(raw['STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json'])
check('author1816 complete staticchecks actualtyped',author['check_count']==len(author['checks'])==1816 and author['all_checks_passed']is True and author['blockers']==[]and all(v['passed']is True for v in author['checks']))
seal_dir=Path(str(P)+'_seal_receipt');seal=json.loads(read(seal_dir/'actual_SOURCE_seal_tool_return.json'))
check('authorseal actualexact pinned receipt',pins[str(seal_dir/'actual_SOURCE_seal_tool_return.json')]['sha256']=='9e971457c1cfb8cdcf28343035da79c80eaa1e26d05c46af1dad72711d66acf4')
check('author actual seal typedzero no live session',type(seal['terminal_tool_return']['exit_code'])is int and seal['terminal_tool_return']['exit_code']==0 and 'session_id'not in seal['terminal_tool_return'])
post=json.loads(read(seal_dir/'actual_POST_SEAL_full_EOF_SHA7ID_confirmation_tool_return.json'))
check('actualpostseal typedzero no live session',type(post['terminal_tool_return']['exit_code'])is int and post['terminal_tool_return']['exit_code']==0 and 'session_id'not in post['terminal_tool_return'])
for v in members:read(v['path'])
for v in originals:read(v['path'])
for v in oldmanifest['members']:read(v['path'])
read(P/'MANIFEST.json');check('allcomplete fixed dirs beforeafter',actual_dirs=={str(q):identity(q.lstat())for q in [P,*sorted(q for q in P.rglob('*')if q.is_dir())]})
check('final complete independentchecklist unique',len({v['check']for v in checks})==len(checks))
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=True,blockers=[],checks=checks,check_count=len(checks),
    qualified_source_manifest=pins[str(P/'MANIFEST.json')],host_template=pins[str(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py')],checker_template=pins[str(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py')],binder=pins[str(P/'bind_complete_native_SOURCE_only.UNREADY.py')],
    full_Source_META_reads=pins,complete_source_members=82,complete_source_member_bytes=2206438,full_member_inventory=members,complete_directory_before=actual_dirs,complete_directory_after=actual_dirs,all_python_source_members=pyfiles,
    all_original67_Source_files_retained=True,all35originalSource_fullpins_rechecked=True,all129_inputs_and90orderedprefix_preserved=True,complete_inverses=reverses,
    prior_two_blockers_preserved=initial['blockers'],prior_two_blockers_resolved_only_by_source=True,previous_full1727_source_review=pins[str(PREVIOUS/'ORIGINAL_30958_SOURCE_REVIEW.json')],previous_full1473_checker_review=pins[str(CHECKER_PEER/'REVIEW.json')],
    fixed_schema_scope_contracts={'Source_admission':'ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1','Source_terminal':'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1','BUILD_terminal':'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'},
    original_caps=manifest['originalCaps'],original_caps_unchanged=True,actual_build_not_executed_here=True,actual_native_not_executed_here=True,actual_source_admission=None,actual_RSS_qualification=None,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,new_native_walker_controls_actual_run=None,
    original_native_build_binary_Source_linkage_qualified=False,original_XSM_memory_bits_verified=False,whole_combined_build_or_INPUT_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    no_reviewed_Source_binder_host_checker_reader_helper_guard_API_compile_or_business_execution=True,no_material_graph_or_ART_numeric_payload_read=True,no_original_frozen_package_project_canonical_D_E_write=True,
    runtime_gate_note='This is complete Source qualification only. Future actual Root Source admission and same-scope peer/fullpins, genuine observed CLOSED V22 BUILD receipt, bound Source review and all129 fresh hashes are still required. Any honest build exit is kept; PREP cannot replace BUILD. Controls for the new native walker remain unexecuted None. Original cap/guards must supervise the unique actual stage; all saved native/ASCII value/order/bit loss remains FAIL. No physical or historical-RAM qualification follows from persisted byte comparison.',
    retained_scope_note='All retained regular files under H/O/C/D/E including visible spool/database/journal count jointly. SQLite FILE temporary placement is O; actual transient storage, RSS, diskfree and guard operation are runtime evidence.')
(OUT/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
for name in('ORIGINAL_30958_SOURCE_REVIEW.json','review_frozen_initial_SOURCE_stdlib.py','ORIGINAL_30958_ACTUAL_REVIEW_TOOL_RETURNS.json'):shutil.copy2(PREVIOUS/name,OUT/name)
shutil.copy2(CHECKER_PEER/'REVIEW.json',OUT/'ORIGINAL_COMPLETE_CHECKER1473_SOURCE_REVIEW.json')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(checks),blockers=[],review_sha256=hashlib.sha256((OUT/'REVIEW.json').read_bytes()).hexdigest(),author_manifest_sha256=pins[str(P/'MANIFEST.json')]['sha256'],business_or_payload_executed=False),indent=2))

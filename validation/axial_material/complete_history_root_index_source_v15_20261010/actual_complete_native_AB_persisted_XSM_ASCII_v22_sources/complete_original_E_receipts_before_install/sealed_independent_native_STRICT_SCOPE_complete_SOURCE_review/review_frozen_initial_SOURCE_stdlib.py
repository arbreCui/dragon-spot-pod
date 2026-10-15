"""Static review of complete fixed source. No reviewed code is run or imported."""
from pathlib import Path
import ast,difflib,hashlib,json,os,stat
P=Path('/private/tmp/axmat_complete_native_genuine_host_BINDER_UNREADY_SOURCE_20261010_pddg3kw5')
OUT=Path('/private/tmp/axmat_native_full_genuine_host_SOURCE_contract_peer_6ijwnmf5')
PARENT=Path('/private/tmp/axmat_complete_native_XSM_ASCII_UNREADY_SOURCE_20261010_vs7f_ff8')
checks=[];pins={}
def check(k,v):
 assert type(v)is bool;checks.append(dict(check=k,passed=v))
 if not v:raise ValueError(k)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 s=p.lstat();i=identity(s);check('regular singlelink Source/META '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
 with p.open('rb')as f:
  check('actual open7ID '+str(p),identity(os.fstat(f.fileno()))==i)
  b=f.read();check('complete EOF '+str(p),len(b)==s.st_size and f.read(1)==b'')
  check('actual fdafter7ID '+str(p),identity(os.fstat(f.fileno()))==i)
 check('actual pathafter7ID '+str(p),identity(p.lstat())==i)
 pins[str(p)]=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
 return b
manifest=json.loads(read(P/'MANIFEST.json'))
check('whole fixed manifest30958',pins[str(P/'MANIFEST.json')]['sha256']=='30958ca0bf049fa02d9b205ed5b89fa07e62092be497df7fa97f2ce3ce00decf')
members=manifest['members'];check('all66 complete members',manifest['member_count']==len(members)==66 and manifest['member_bytes']==sum(v['size_bytes']for v in members)==1592530)
directories={str(q):identity(q.lstat())for q in [P,*[P/v for v in manifest['directories']]]}
check('complete declared directory inventory',sorted(q.relative_to(P).as_posix()for q in P.rglob('*')if q.is_dir())==manifest['directories'])
check('complete declared file inventory',sorted(q.relative_to(P).as_posix()for q in P.rglob('*')if q.is_file())==sorted([v['relative_path']for v in members]+['MANIFEST.json']))
asts=[];raw={}
for v in members:
 q=P/v['relative_path'];raw[v['relative_path']]=read(q)
 check('all complete member pins '+v['relative_path'],pins[str(q)]=={k:w for k,w in v.items()if k!='relative_path'})
 if q.suffix=='.py':ast.parse(raw[v['relative_path']]);asts.append(v['relative_path'])
parent=json.loads(read(PARENT/'MANIFEST.json'))
check('actual parent sealaccdf792 full',pins[str(PARENT/'MANIFEST.json')]['sha256']=='accdf792787276a941b73cdaccdc99f26972620e4a5d74f7b89528e6f377baa9')
for v in parent['members']:
 a=read(Path(v['path']));b=raw['PARENT_NATIVE_SOURCE/'+v['relative_path']]
 check('full parent pin unchanged '+v['relative_path'],pins[v['path']]=={k:w for k,w in v.items()if k!='relative_path'})
 check('all old parent bytes retained '+v['relative_path'],a==b)
check('entire old parent manifest retained',raw['PARENT_NATIVE_SOURCE/MANIFEST.json']==(PARENT/'MANIFEST.json').read_bytes())
provenance=json.loads(raw['PARENT_NATIVE_SOURCE/ORIGINAL_SOURCE_PROVENANCE_PINS.json'])
originals=[]
for v in provenance['pins']:
 b=read(Path(v['path']));check('actual all35 original Source fullpins '+v['path'],pins[v['path']]=={k:w for k,w in v.items()if k!='saved_source_path'})
 check('whole Source copied '+v['path'],b==(P/'PARENT_NATIVE_SOURCE/SOURCE_PROVENANCE'/Path(v['saved_source_path']).name).read_bytes());originals.append(pins[v['path']])
proof=json.loads(raw['COMPLETE_HOST_AND_V4_CHECKER_SOURCE_INVERSE_PROOF.json']);reverse=[]
for i,v in enumerate(proof['proofs']):
 old=read(Path(v['original_full_Source']['path']));new=read(Path(v['current_full_Source']['path']))
 check('original/source exact inverse pins '+str(i),pins[v['original_full_Source']['path']]==v['original_full_Source']and pins[v['current_full_Source']['path']]==v['current_full_Source'])
 oldlines=old.decode().splitlines(keepends=True);newlines=new.decode().splitlines(keepends=True)
 hs=v['full_line_hunks'];check('finite original fullhunks count '+str(i),len(hs)==(15 if i==0 else 6))
 rebuilt=[]
 for tag,a,b,c,d in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
  if tag!='equal':rebuilt.append(dict(old_begin_line_zero_based=a,old_end_exclusive_zero_based=b,new_begin_line_zero_based=c,new_end_exclusive_zero_based=d,old_full_lines=oldlines[a:b],new_full_lines=newlines[c:d]))
 check('independent every fullhunk '+str(i),rebuilt==hs)
 back=newlines[:]
 for h in reversed(hs):
  a,b=h['new_begin_line_zero_based'],h['new_end_exclusive_zero_based'];check('new inverse exacthunk '+str(i)+':'+str(a),back[a:b]==h['new_full_lines']);back[a:b]=h['old_full_lines']
 check('whole bytes reverse original '+str(i),''.join(back).encode()==old)
 check('whole AST reverse original '+str(i),ast.dump(ast.parse(''.join(back)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
 defs=lambda t:{n.name:n for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 od,nd=defs(old),defs(new);unchanged=[k for k in od if ast.dump(od[k],include_attributes=False)==ast.dump(nd[k],include_attributes=False)];changed=[k for k in od if k not in unchanged];added=sorted(set(nd)-set(od))
 check('alloriginal definitions preserved '+str(i),set(od)<=set(nd))
 check('all original unchanged AST ledger '+str(i),unchanged==v['unchanged_function_AST'])
 check('all original changed AST ledger '+str(i),changed==v['changed_function_AST'])
 check('all added functions disclosed '+str(i),added==v['added_functions'])
 reverse.append(dict(full_source_proof=v,actual_original_definition_count=len(od),actual_candidate_definition_count=len(nd)))
host=raw['complete_native_XSM_ASCII_genuine_host.UNREADY.py'].decode();checker=raw['complete_native_XSM_ASCII_checker_v4.UNREADY.py'].decode();binder=raw['bind_complete_native_SOURCE_only.UNREADY.py'].decode()
for name,source in [('HOST',host),('CHECKER',checker),('BINDER',binder)]:
 tree=ast.parse(source)
 check('Source '+name+' no subprocess/nativeAPI import',not any(isinstance(n,ast.Import)and any(a.name in ('subprocess','ctypes','ganlib')for a in n.names)for n in ast.walk(tree)))
 if name=='BINDER':check('Source binder noexecute watchedstage',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','run','exec_module','Popen')for n in ast.walk(tree)))
anchors=[
('original genuine619 guard',"helper.guard_admission(full)",host),
('original705/38de MRO',"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)",host),
('actual boundedbc4 source fullpin',"support.pin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA",host),
('whole1800 stage600 RSS512 joint2GiB',"WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30",host),
('original history96/free8 resource',"DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30",host),
('five original ART history streams',"[str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)]",host),
('all129 fullinput before',"for p in b['complete_input_pins']:inputs.append(recheck_full_pin(support,p))",host),
('all inputs Source guard after',"for entry in inputs+[hpin,rpin,*genuine_pins]:",host),
('complete D/E directories and inventories',"complete_directory_identity(receipts)==receipt_directories",host),
('alljoint before after final retainedspools db journal',"support.archive_bytes(roots5)",host),
('onlyone actualstage no replay',"len(runner.records)==1",host),
('all macrocounts19619/19990/2264113',"macro['records']==19619 and macro['physical_headers_including_all_closes']==19990 and macro['numeric_components']==2264113",host),
('physical order and completebit comparison',"v['native_physical_preorder_equal_original_ASCII']is True",host),
('unknown nativecontrols truthfulNone',"new_native_walker_controls_actual_run=None",host),
('nativebytequalification truthfulNone',"actual_native_byte_qualification_sha256=None",host),
('saveloss report pin honest',"actual_native_report_pin_if_saved=support.pin(saved)if saved.is_file()",host),
('every Source member inventoried binder',"files==[m['path']for m in members]",binder),
('all original129 remain binder',"len(binding['complete_input_pins'])==129",binder),
('boundglobal fullinverse checker+host',"all original Source bytes must restore",binder),
('future namespace Source freshness',"all(not os.path.lexists(paths[key])for key in ('host','output','control','source'))",binder),
('fullsourcecopy notfieldsfilter',"shutil.copytree(P,destination)",binder),
('SQLcache8MiB',"PRAGMA cache_size=-8192",checker),
('SQLmmap0',"PRAGMA mmap_size=0",checker),
('SQLFILEtempdeclaredO',"os.environ['SQLITE_TMPDIR'] = str(Path(path).parent)",checker),
('full runtime joint5 roots',"for root in self.joint_roots:",checker),
('unchanged full REAL64/CHAR/LOGICAL loss',"full evidence saved but at least one original native/ASCII value-bit mismatch; no tolerance or retry",checker),
]
for name,text,src in anchors:check(name,text in src)
blueprint=json.loads(raw['PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'])
check('all 129 exact original pins remain',len(blueprint['complete_input_pins'])==len({p['path']for p in blueprint['complete_input_pins']})==129)
actual_parent=json.loads(raw['PARENT_NATIVE_SOURCE/SAVED_RAW_TRANSFER_PARENT_META.json'])['rawrecord_binding']['input_pins']
check('whole90 original ordered prefix',len(actual_parent)==90 and blueprint['complete_input_pins'][:90]==actual_parent)
request=json.loads(raw['ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json'])
check('all request actualpins None',all(request[k]is None for k in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin')))
review=json.loads(raw['STATIC_COMPLETE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json'])
check('author488 finiteSource checks alltrue',review['all_static_checks_passed']is True and len(review['checks'])==review['check_count']==488 and all(v['passed']is True for v in review['checks']))
for v in members:read(Path(v['path']));check('fullauthor allmember afterunchanged '+v['relative_path'],pins[v['path']]=={k:w for k,w in v.items()if k!='relative_path'})
for v in originals:read(Path(v['path']));check('all35 actualoriginal afterunchanged '+v['path'],pins[v['path']]==v)
check('whole Source directory beforeafter',directories=={p:identity(Path(p).lstat())for p in directories})
read(P/'MANIFEST.json');check('author final manifest unchanged',pins[str(P/'MANIFEST.json')]['sha256']=='30958ca0bf049fa02d9b205ed5b89fa07e62092be497df7fa97f2ce3ce00decf')
blockers=[dict(id='Root_terminal_observation_wrapper_not_strictly_closed',locations=['binder:actual_terminal','host:actual_closed_prior'],
 detail='Requires terminal typed int/noSession but never checks actual Root observed CLOSED wrapper or build-specific scope. A PREP or unrelated Source receipt must not stand in for real V22 build closure.'),
 dict(id='Source_admission_and_peer_only_hashed_not_scope_bound',locations=['binder:main','host:main'],
 detail='Source admission and independent host/binder Source review are full-pin hashed but their schema/status/this-manifest/candidate-fullpin linkage is not validated. Admission actual tool output is not coupled to its actual admission file. Correct externally chosen metadata cannot replace explicit Source checks.')]
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_BLOCKED_PENDING_STRICT_ROOT_META_SCOPE_BINDING',
 source_only=True,all_nonblocker_checks_passed=True,checks=checks,check_count=len(checks),blockers=blockers,
 qualified_source_manifest=pins[str(P/'MANIFEST.json')],host_template=pins[str(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py')],checker_template=pins[str(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py')],binder=pins[str(P/'bind_complete_native_SOURCE_only.UNREADY.py')],
 whole_parent53files_and35originalSources_retained=True,all129inputs_and90orderedprefix_retained=True,
 complete_finite_inverse_proofs=reverse,full_Source_META_reads=pins,python_source_members=asts,
 no_reviewed_checker_binder_host_reader_helper_guard_API_compile_or_business_execution=True,no_material_numeric_payload_read=True,
 original_caps=[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0],original_native_build_binary_Source_linkage_qualified=False,
 actual_native_or_RSS_or_scientific_qualification=None,
 retained_scope_note='All retained regular files under H/O/C/D/E including visible spool/database/journal are jointly counted. SQLite FILE temporary placement is within O; actual transient storage, actual RSS and diskfree remain runtime evidence, not Source certification.')
(OUT/'ORIGINAL_30958_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,nonblocker_checks=len(checks),source_blockers=len(blockers),review_sha256=hashlib.sha256((OUT/'ORIGINAL_30958_SOURCE_REVIEW.json').read_bytes()).hexdigest(),business_executed=False),indent=2))

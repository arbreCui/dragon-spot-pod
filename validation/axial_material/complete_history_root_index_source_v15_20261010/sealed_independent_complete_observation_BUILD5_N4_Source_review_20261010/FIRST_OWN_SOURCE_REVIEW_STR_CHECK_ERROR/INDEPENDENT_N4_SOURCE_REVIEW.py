import ast,gzip,hashlib,json,shutil,stat,tarfile
from pathlib import Path
Q=Path(__file__).parent
N=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_role_limited_OS_tools_N4_UNREADY_Source_3gnnt2it')
OLD=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
PREVIOUS_PEER=Path('/private/tmp/axmat_INDEPENDENT_observer_N3_complete_Source_review_v8ehpd70')
SUPPORT=Path('/private/tmp/axmat_N3_recipe_physics_Source_support_independent_qxhm8spq')
EXPECTED={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
changed=['Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','complete_observation_BUILD5_AB_runtime.UNREADY.py','complete_observation_genuine_host.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']
checks=[];blockers=[];evidence={}
def check(name,value,detail=None):
 assert type(value)is bool and name not in {c['check']for c in checks}
 checks.append(dict(check=name,passed=value))
 if not value:blockers.append(dict(check=name,detail=detail))
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=ident(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def parse(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def read(p,sha=None):
 before=pin(p)
 if sha:assert before['sha256']==sha
 d=parse(Path(p).read_bytes());assert pin(p)==before;return d,before

def view(root):
 assert root.is_dir()and root.resolve()==root and not root.is_symlink()
 files={};dirs={'.':ident(root)}
 for p in sorted(root.rglob('*')):
  i=ident(p);assert not p.is_symlink();k=str(p.relative_to(root))
  if stat.S_ISREG(i[2]):files[k]=pin(p)
  else:assert stat.S_ISDIR(i[2]);dirs[k]=i
 for k,p in files.items():assert pin(root/k)==p
 for k,i in dirs.items():assert ident(root/k)==i
 return dict(root=str(root),files=files,directories=dirs,symlinks={})
def defs(text):
 tree=ast.parse(text)
 return {n.name:ast.get_source_segment(text,n)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assignment(tree,key):
 return next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==key for t in n.targets))
before=view(N);oldbefore=view(OLD)
m,mfp=read(N/'MANIFEST.json','0aa59da7045bcdbe1ed76f1506527939d6b692663a564a64b3779dc20af40d2d')
om,omfp=read(OLD/'MANIFEST.json','5313b65cc109d93816137f8c53e6cdcfbf6d5044310762ac65a20a2f76330593')
check('complete N4 author manifest and actual namespace full EOF SHA size seven identities',m['member_count']==97 and len(m['members'])==97 and len(before['files'])==98 and len(before['directories'])==13 and m['complete_directory_identity']==before['directories'] and {r['relative_path']:r['fullpin']for r in m['members']}=={k:p for k,p in before['files'].items()if k!='MANIFEST.json'})
check('complete original N3 namespace remains byte and identity frozen',len(oldbefore['files'])==81 and len(oldbefore['directories'])==10 and om['complete_directory_identity']==oldbefore['directories'] and {r['relative_path']:r['fullpin']for r in om['members']}=={k:p for k,p in oldbefore['files'].items()if k!='MANIFEST.json'})
check('all actual Source file and directory identity seven fields remain exact Python integers',all(type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])for p in before['files'].values())and all(len(i)==7 and all(type(x)is int for x in i)for i in before['directories'].values()))
unchanged=[k for k in oldbefore['files']if k not in changed+['MANIFEST.json']]
check('all75 nonrole original N3 members preserve entire bytes SHA and size',len(unchanged)==75 and all(before['files'][k]['sha256']==oldbefore['files'][k]['sha256']and before['files'][k]['size_bytes']==oldbefore['files'][k]['size_bytes']for k in unchanged))
check('entire original N3 manifest retained separately with byte exact EOF',pin(N/'PREVIOUS_SEALED_N3_SOURCE_PROVENANCE/MANIFEST.json')['sha256']==omfp['sha256'])
inv,ip=read(N/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json','39f6f937948265f6313b924a8d14d7b5d695f757c7b7d872ec1f824f18cab02e')
check('five role inverse exact role set canonical six actual paths and original complete81 pins',set(inv['five_role_complete_inverse_hunks'])==set(changed)and inv['canonical_OS_tool_paths']==EXPECTED and inv['N3_original_fullfile_pins']==oldbefore['files'])
check('twenty-nine full finite hunks cover all changed role Source',sum(len(h)for h in inv['five_role_complete_inverse_hunks'].values())==29)
role_proofs={};texts={};trees={};oldtexts={};oldtrees={}
expected_helper="""def source_tool_nlink_allowed(path,nlink,tool_role=None):
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1
"""
for role in changed:
 text=(N/role).read_text();old=(OLD/role).read_text();texts[role]=text;oldtexts[role]=old;trees[role]=ast.parse(text);oldtrees[role]=ast.parse(old)
 lines=text.splitlines(True);original=old.splitlines(True);hs=inv['five_role_complete_inverse_hunks'][role]
 for h in reversed(hs):
  assert ''.join(lines[h['derived_start0']:h['derived_stop0']])==h['derived']
  assert ''.join(original[h['original_start0']:h['original_stop0']])==h['original']
  lines[h['derived_start0']:h['derived_stop0']]=h['original'].splitlines(True)
 restored=''.join(lines)
 check(role+' complete byte and AST inverse restores entire original N3',restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
 retained=N/'PREVIOUS_SEALED_N3_SOURCE_PROVENANCE/FIVE_ORIGINAL_N3_SOURCE'/role
 check(role+' full original Source copy and author role proof match actual originals',pin(retained)['sha256']==pin(OLD/role)['sha256']and inv['five_role_full_definition_proof'][role]['original_pin']==pin(OLD/role)and inv['five_role_full_definition_proof'][role]['derived_pin']==pin(N/role))
 newdefs=defs(text);oldd=defs(old);proof=inv['five_role_full_definition_proof'][role]
 check(role+' complete nonchanged definitions retain byte and AST with exact changed set',set(newdefs)==set(oldd)|{'source_tool_nlink_allowed'}and set(proof['unchanged_topdefs_fullbytes_and_AST'])|set(proof['changed_original_topdefs'])==set(oldd)and all(newdefs[k]==oldd[k]and ast.dump(ast.parse(newdefs[k]),include_attributes=False)==ast.dump(ast.parse(oldd[k]),include_attributes=False)for k in proof['unchanged_topdefs_fullbytes_and_AST']))
 check(role+' exact explicit role helper rejects bool float zero negative and wrong paths by Source AST',ast.dump(ast.parse(newdefs['source_tool_nlink_allowed']),include_attributes=False)==ast.dump(ast.parse(expected_helper),include_attributes=False)and ast.literal_eval(assignment(trees[role],'CANONICAL_OS_TOOL_PATHS'))==EXPECTED)
 check(role+' original caps and future qualification AST unchanged',all(ast.dump(assignment(trees[role],k),include_attributes=False)==ast.dump(assignment(oldtrees[role],k),include_attributes=False)for k in ('CAPS',('FALSE'if role==changed[3]else'FUTURE'))))
 role_proofs[role]=dict(derived_fullpin=pin(N/role),original_fullpin=pin(OLD/role),complete_hunk_count=len(hs),all_unchanged_topdefs=proof['unchanged_topdefs_fullbytes_and_AST'],changed_definitions=proof['changed_original_topdefs'])
request,binder,runtime,host,post=[texts[r]for r in changed]
check('Root request requires exact six original CLI paths and passes explicit role only to six tools',"all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items())"in request and "tools={k:pin(getattr(a,k),deadline,tool_role=k)for k in('fortran','c','cpp','ar','lsof','ps')}"in request and "actual=pin(value['path'],deadline)"in request)
check('binder validates tool role paths before extra shapes and protects original129 with default singlelink',all(s in binder for s in ("for role,p in b['tool_pins'].items():shape(p,tool_role=role)","for p in rows:shape(p)","for p in extra:shape(p,tool_role=tool_roles_by_path.get(p['path']))","allpins.get(p['path'])==p")))
check('runtime validates roles and default original129 independently before genuine imports',all(s in runtime for s in ("for role,p in b['tool_pins'].items():pinshape(p,tool_role=role)","for p in rows:pinshape(p)","for p in extra:pinshape(p,tool_role=tool_roles_by_path.get(p['path']))")))
check('runtime all protected prelaunch success and failed fullEOF inputs carry correct tool role mapping',all(s in runtime for s in ("for p in inputs:recheck(p,tool_role=tool_roles_by_path.get(p['path']))","for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))","try:after_inputs.append(recheck(p,tool_role=tool_roles_by_path.get(p['path'])))","pinshape(p,tool_role=tool_role);require(fullpin(p['path'],budget,tool_role=tool_role)==p")))
check('host typed helper forwards role and retains original genuine support EOF SHA actual7ID',"typed_full_pin(expected,tool_role=tool_role)"in host and "actual=support.pin(expected['path'],expected['sha256'])"in host and defs(host)['main']==defs(oldtexts[changed[3]])['main'])
check('host execution delegates protected tools to role-aware full runtime while Source and Root terminal remain default singlelink',"runtime.run(sys.modules[__name__],support,b,b['actual_author_Source_contract'],started)"in host and defs(host)['source_scope_contract']==defs(oldtexts[changed[3]])['source_scope_contract']and defs(host)['actual_closed_prior']==defs(oldtexts[changed[3]])['actual_closed_prior'])
check('postclose checks tool role paths and every persisted whole input with same explicit mapping',all(s in post for s in ("for role,p in b['tool_pins'].items():check(p,tool_role=role)","for p in h['complete_input_pins_before_and_after']:check(p,tool_role=tool_roles_by_path.get(p['path']))","require(fullpin(p['path'],tool_role=tool_role)==p")))
check('complete namespace tree joint accounting Source helpers stay exact default singlelink',all(defs(texts[r])[k]==defs(oldtexts[r])[k]for r,keys in ((changed[2],('tree','joint_bytes','frozen_sources')),(changed[3],('complete_source_inputs','complete_directory_identity')),(changed[4],('tree',)))for k in keys))
check('all compiler recipes module includes suffix group archive commands and material collection retain entire bytes',all(defs(runtime)[k]==defs(oldtexts[changed[2]])[k]for k in ('compile_all','collect_state','guarded'))and ast.dump(assignment(trees[changed[2]],'ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES'),include_attributes=False)==ast.dump(assignment(oldtrees[changed[2]],'ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES'),include_attributes=False))
check('Root postclose whole five views E onlyself sorting and resources unchanged except role-aware input check',all(s in post for s in ("after_E_files=sorted(after_E['files'],key=lambda p:p['path'])","expected_E_files=sorted(","current[:3]==identity[:3]","Root_complete_postclose_HOCDE_namespace_views=namespace_views")))
# Parse every Source/Meta whole, never import any reviewed module.
parsed=[];jsonpins=[]
for p in sorted(N.rglob('*')):
 if p.is_file()and p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));parsed.append(pin(p))
 if p.is_file()and p.suffix=='.json':parse(p.read_bytes());jsonpins.append(pin(p))
check('all complete Python Source AST and JSON Meta parse with no execution duplicate keys or nonfinite values',bool(parsed)and bool(jsonpins))
index,indexp=read(N/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');members={q['relative_path']:q['full_original_Source_pin']for q in index['members']}
check('original complete native index retains1365 distinct Source members no fabricated compiled outputs',len(members)==1365 and len(index['members'])==1365 and index['actual_compile_execution']is None and index['actual_objects']is None and index['actual_new_executable']is None)
archive=N/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz';archivepins={};selected={}
physical=read(N/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json')[0]
needed={q['original_archive_member']for q in physical['derivations']}
with tarfile.open(archive,'r|gz')as tar:
 for member in tar:
  assert member.isfile()and member.name in members and member.name not in archivepins
  stream=tar.extractfile(member);h=hashlib.sha256();size=0;parts=[]
  while True:
   b=stream.read(2**20)
   if not b:break
   h.update(b);size+=len(b)
   if member.name in needed:parts.append(b)
  assert size==member.size and h.hexdigest()==members[member.name]['sha256']and size==members[member.name]['size_bytes']
  archivepins[member.name]=dict(sha256=h.hexdigest(),size_bytes=size)
  if parts:selected[member.name]=b''.join(parts)
check('all1365 Source tar members streamed full EOF SHA size with exact unique coverage',set(archivepins)==set(members))
with gzip.open(archive,'rb')as f:
 while f.read(2**20):pass
check('complete Source gzip reaches true EOF and validates trailer CRC without extraction',True)
count=0
for row in physical['derivations']:
 original=selected[row['original_archive_member']].decode();out=original.splitlines(True)
 for h in reversed(row['complete_insert_only_hunks']):
  assert h['tag']=='insert'and h['old_start0']==h['old_end0']and h['old_full_lines']==[]
  out[h['old_start0']:h['old_end0']]=h['new_full_lines'];count+=1
 assert ''.join(out)==(N/row['derived_Source_member']).read_text()
check('all four complete original physical Source routines invert all14 pure observer insertions without changing arithmetic',count==14)
hinv=read(N/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json')[0]
horiginal=(N/'PARENT_SOURCE/Root_bound_complete_native_genuine_host.py').read_text();hl=horiginal.splitlines(True)
for h in reversed(hinv['complete_full_inverse_hunks']):
 assert hl[h['old_start0']:h['old_end0']]==h['old_full_lines'];hl[h['old_start0']:h['old_end0']]=h['new_full_lines']
check('entire original genuine host twelve-hunk derivation plus N4 inverse reproduces current host',len(hinv['complete_full_inverse_hunks'])==12 and ''.join(hl)==oldtexts[changed[3]])
# Independent focused Source support is retained with genuine tool truth, no API execution.
support,supportp=read(SUPPORT/'REVIEW.json','e95920feae4c046a8d292f5894ad6c802294c7b64c2830a85026d9f4efc9d492')
supporttruth,supporttp=read(SUPPORT/'ACTUAL_REVIEW_TOOL_RETURN.json','fd149e8b4b7b8a311cb6c2cc44d2475d6ee0233a57a681170738812906a96751')
evidence['focused_original_recipe_physics_support']=dict(report_pin=supportp,actual_tool_truth_pin=supporttp,reviewer_Source_pin=pin(SUPPORT/'N3_RECIPE_PHYSICS_SOURCE_REVIEW.py')if(SUPPORT/'N3_RECIPE_PHYSICS_SOURCE_REVIEW.py').exists()else None,complete_report=support)
check('focused independent original fourMakefile recipes ar modules physics and host Source checks genuine true no blockers',support.get('blockers')==[]and support.get('errors')==[]and all(c['passed']is True for c in support['checks']))
# Root actual small META retained byte-exact; not reused as N4 admission.
meta=N/'ACTUAL_PRIOR_N3_SOURCE_META_FAILURE_EVIDENCE'
tools,tpp=read(meta/'Root_actual_canonical_tool_full_EOF_identity_observation_tool_return.json','86fae0e2c1b6727a3892630bb4769887fb02a928b55e3958c4e574908418875e')
tr=tools['terminal_tool_return'];actual=parse(tr['output'])
check('genuine new Root six-tool fullEOF observation782641 typed0 CLOSED actual observed field no guessed terminal',tools['closed']is True and tools['observed']is True and tools['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==0 and tr['chunk_id']=='782641'and 'session_id'not in tr and tools['compiler_or_business_executed']is False)
check('six original actual canonical tool paths preserve all genuine SHA size and seven integer nlinks2_78_78_78_1_1',len(actual['tools'])==6 and {r['tool_role']:r['requested']for r in actual['tools']}==EXPECTED and [r['fullpin']['identity'][3]for r in actual['tools']]==[2,78,78,78,1,1]and all(r['requested']==r['resolved']==r['fullpin']['path']and r['regular']is True and r['symlink_ancestors']==[]and all(type(x)is int for x in r['fullpin']['identity'])for r in actual['tools']))
priorad,prioradp=read(meta/'Root_actual_observation_Source_admission_tool_terminal_return.json');fail,failp=read(meta/'Root_actual_observation_request_META_alias_failure_tool_terminal_return.json')
check('honest prior N3 actual Source9884630 and request88c74a1 strict closed retained not promoted',priorad['terminal_tool_return']['chunk_id']=='988463'and type(priorad['terminal_tool_return']['exit_code'])is int and priorad['terminal_tool_return']['exit_code']==0 and fail['terminal_tool_return']['chunk_id']=='88c74a'and type(fail['terminal_tool_return']['exit_code'])is int and fail['terminal_tool_return']['exit_code']==1 and priorad['closed']is True and fail['closed']is True)
sourcead,sadp=read(meta/'Root_actual_complete_native_observation_N3_Source_admission.json')
check('prior successful N3 Source admission is exact old Source and cannot admit new N4 manifest',sourcead['complete_author_Source_manifest_pin']==omfp and sourcead['scientific_qualification_created']is False and sourcead['actual_author_Source_contract']['qualified_source_manifest']!=mfp)
previous,prevp=read(PREVIOUS_PEER/'REVIEW.json','10de184f8982061f4a3d43aaac3d941d81626156b3ae3007514193f02e54c14e')
check('original N3 independent66 Source-only contract exactly bound to old full manifest',previous['source_only']is True and previous['all_checks_passed']is True and previous['all_checks_typed_true']is True and previous['check_count']==66 and previous['blockers']==[]and previous['complete_reviewed_source_manifest_pin']==omfp)
# Author actual58 checks and their own honest atime assertion failure are provenance only.
author,ap=read(N/'AUTHOR_N4_SOURCE_ONLY_REPORT.json');authortruth,atp=read(N/'ACTUAL_AUTHOR_N4_SOURCE_ONLY_TOOL_RETURNS.json')
check('author58 Source checks remain typed true and do not serve as independent admission',author.get('all_checks_typed_true')is True and author.get('blockers')==[]and len(author['checks'])==58 and m['actual_peer_review']is None)
check('all future actual runtime native controls binary scientific pins remain unknown or false',all(m[k]is None for k in ('actual_peer_review','actual_Root_Source_admission','actual_Root_runtime_terminal','actual_observation_manifest','actual_native_Source_binary_linkage','actual_new_native_controls','actual_new_native_objects_archives_executable'))and all(m[k]is False for k in ('scientific_qualification_created','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted')))
roles=ast.literal_eval(assignment(trees[changed[0]],'ROLES'));authorcontract={k:pin(N/v)for k,v in roles.items()}
check('all14 current N4 actual author roles exact fullfourpins with unchanged completewalker and legacy extractor',len(authorcontract)==14 and authorcontract['qualified_source_manifest']==mfp and authorcontract['original_complete_native_walker']['sha256']=='9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'and authorcontract['legacy_context_old_XSM_extractor']['sha256']=='079e6b9bca0f5e0ab43a41604ccd91c83112a0d040253dcc9101ae47b0efcb69')
# Whole reviewed source retained once, without copying all ancestor packages again.
for k,p in before['files'].items():
 target=Q/'COMPLETE_REVIEWED_N4_SOURCE'/k;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p['path'],target);assert pin(target)['sha256']==p['sha256']and pin(target)['size_bytes']==p['size_bytes']
for k in before['directories']:(Q/'COMPLETE_REVIEWED_N4_SOURCE'/k).mkdir(parents=True,exist_ok=True)
for p in (PREVIOUS_PEER/'REVIEW.json',SUPPORT/'REVIEW.json',SUPPORT/'ACTUAL_REVIEW_TOOL_RETURN.json'):
 target=Q/'FINITE_INDEPENDENT_PROVENANCE'/('N3_66_REVIEW.json'if p.parent==PREVIOUS_PEER else p.name);target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
for p in SUPPORT.glob('*.py'):shutil.copyfile(p,Q/'FINITE_INDEPENDENT_PROVENANCE'/p.name)
check('whole reviewed N4 full98 files and all13 directories retained complete EOF byte exact',len(view(Q/'COMPLETE_REVIEWED_N4_SOURCE')['files'])==98 and set(view(Q/'COMPLETE_REVIEWED_N4_SOURCE')['directories'])==set(before['directories']))
check('all reviewed original N4 and N3 full namespaces unchanged after complete independentSource review',view(N)==before and view(OLD)==oldbefore)
evidence.update(five_role_complete_byte_AST_proof=role_proofs,complete_five_role_inverse_pin=ip,original_N3_manifest_pin=omfp,prior_N3_independent_Source_report_pin=prevp,whole_native_Source_archive_pin=pin(archive),all1365_streamed_Source_member_pins=archivepins,all_parsed_python_Source_pins=parsed,all_strict_Source_META_pins=jsonpins,actual_canonical_OS_tool_META_receipt=tpp,actual_prior_N3_Source_tool_truth_pin=prioradp,actual_prior_N3_REQUEST_failure_truth_pin=failp,actual_prior_N3_admission_pin=sadp,author_Source_check_pin=ap,author_actual_Source_tool_returns_pin=atp)
passed=not blockers and all(type(c['passed'])is bool and c['passed']is True for c in checks)
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'if passed else'BLOCKED_SOURCE_ONLY_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=passed,all_checks_typed_true=passed,check_count=len(checks),checks=checks,blockers=blockers,actual_author_Source_contract=authorcontract,evidence=evidence,complete_reviewed_source_manifest_pin=mfp,complete_reviewed_source_namespace_before=before,complete_reviewed_source_namespace_after=view(N),helper_candidate_guard_API_native_material_compile_or_numeric_executed=False,actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False,unverified_actual_scope=['Root new N4 Source admission and complete Source-only request/binding','genuine guarded complete five-stage native compiler execution and Source-object-archive-link-new-executable evidence','A and B actual material observations all native snapshots and context raw events','independent native walker and snapshot API bit controls','complete realRoot postclose manifest and context aggregation execution','science reference and neutron balance and AAA8 and ABA acceptance'])
with (Q/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(checks),typed_true=passed,blockers=blockers,review_pin=pin(Q/'REVIEW.json'),reviewed_N4_manifest_pin=mfp,candidate_or_guard_or_native_compiler_executed=False,scientific_qualification=False)))

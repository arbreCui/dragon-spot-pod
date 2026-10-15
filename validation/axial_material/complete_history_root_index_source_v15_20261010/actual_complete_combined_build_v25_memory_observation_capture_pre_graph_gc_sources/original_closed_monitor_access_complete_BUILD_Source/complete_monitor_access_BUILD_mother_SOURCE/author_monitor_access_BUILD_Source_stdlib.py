"""Own author Source work only: full bytes, static AST and exact namespace rows.
Never imports, compiles or invokes candidate/helper/guard/build/native APIs.
"""
from pathlib import Path
import ast,json,hashlib,stat,shutil,tempfile,difflib
U=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85');P=Path(tempfile.mkdtemp(prefix='axmat_v25_monitor_access_complete_BUILD_UNREADY_Source_',dir='/private/tmp'));checks=[]
def pin(p):
 s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not p.is_symlink()
 with p.open('rb')as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();assert before==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];return dict(path=str(p),sha256=d,size_bytes=s.st_size,identity=before)
def check(name,value):
 assert type(value)is bool and value,name;checks.append(dict(check=name,passed=True))
def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def inverse(text,rows):
 for row in reversed(rows):assert text.count(row['new'])==row['count'],row['label'];text=text.replace(row['new'],row['old'])
 return text
def literal(node):
 if isinstance(node,ast.Constant):return node.value
 if isinstance(node,ast.Name):return {'unknown_Source_Name':node.id}
 if isinstance(node,ast.List):return[literal(x)for x in node.elts]
 if isinstance(node,ast.Tuple):return tuple(literal(x)for x in node.elts)
 if isinstance(node,ast.Dict):return{literal(k):literal(v)for k,v in zip(node.keys,node.values)}
 return {'static_Source_AST_not_executed':ast.dump(node,include_attributes=False)}
def constants(text):
 return{n.targets[0].id:literal(n.value)for n in ast.parse(text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and(isinstance(n.value,(ast.Constant,ast.List,ast.Tuple,ast.Dict))or n.targets[0].id=='EXPECTED_COMMANDS')}
assert pin(U/'MANIFEST.json')['sha256']=='9e9a77669309071065c189ad02ee455709ca81db376de818825d99d8cf22f6e9';mf=json.loads((U/'MANIFEST.json').read_bytes());mother_pin=pin(U/'MANIFEST.json')
check('mother complete frozen39 files4dirs whole manifest actual SHA and all38 Source member fullEOF7ID exact',len(mf['members'])==38 and len(mf['directories'])==4 and all(pin(U/rel)==wanted for rel,wanted in mf['members'].items())and all(identity(U/rel)==wanted for rel,wanted in mf['directories'].items())and {str(q.relative_to(U))for q in U.rglob('*')if q.is_file()}==set(mf['members'])|{'MANIFEST.json'})
for p in U.iterdir():
 if p.is_dir():shutil.copytree(p,P/p.name,copy_function=shutil.copy2)
 else:shutil.copy2(p,P/p.name)
(P/'MANIFEST.json').rename(P/'ORIGINAL_FROZEN_MOTHER_SOURCE_MANIFEST.json')
mapping=[
 ('axial-material-complete-combined-prepare-host-v25-20261010','axial-material-complete-combined-prepare-host-v25-monitor-access-20261010'),
 ('axial-material-complete-combined-build-host-v25-20261010','axial-material-complete-combined-build-host-v25-monitor-access-20261010'),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010'),
 ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010'),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010'),
 ('actual_complete_combined_prepare_v25_sources','actual_complete_combined_prepare_v25_monitor_access_sources'),
 ('actual_complete_combined_prepare_v25_receipts','actual_complete_combined_prepare_v25_monitor_access_receipts'),
 ('actual_complete_combined_build_v25_sources','actual_complete_combined_build_v25_monitor_access_sources'),
 ('actual_complete_combined_build_v25_receipts','actual_complete_combined_build_v25_monitor_access_receipts'),
 ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py'),
]
names={'BUILD_binder':'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py','build_host':'host_and_postclose_templates/build_host.V25.UNREADY.full.py','build_writer':'host_and_postclose_templates/build_writer.V25.UNREADY.full.py'};edits={};originals={};fixed={}
for role,rel in names.items():
 text=(U/rel).read_text();originals[role]=text;rows=[]
 for old,new in mapping:
  count=text.count(old)
  if count:rows.append(dict(label='exact_v25_monitor_access_namespace_'+old,old=old,new=new,count=count));text=text.replace(old,new)
 assert inverse(text,rows)==originals[role];ast.parse(text);(P/rel).write_text(text);edits[role]=rows;fixed[role]=text
check('precise namespace transforms only exact10 named basenames in three BUILD files without global v25 V25 FAMILY schema replacement',all(inverse(fixed[role],edits[role])==originals[role]for role in names)and len(edits['BUILD_binder'])==7 and len(edits['build_host'])==7 and len(edits['build_writer'])==7)
proof=json.loads((U/'COMPLETE_SOURCE_INVERSES.json').read_bytes());original_proof=json.loads((U/'COMPLETE_SOURCE_INVERSES.json').read_bytes())
for role in('build_host','build_writer'):proof['exact_finite_transforms'][role].extend(edits[role])
(P/'COMPLETE_SOURCE_INVERSES.json').write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
for role in('canonical','prepare_host','prepare_writer','build_host','build_writer'):
 rel='canonical.V25.UNREADY.full.py'if role=='canonical'else'host_and_postclose_templates/'+role+'.V25.UNREADY.full.py';text=(P/rel).read_text();parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();restored=inverse(text,proof['exact_finite_transforms'][role]);check('complete '+role+' namespace plus existing Source inverse to ORIGINAL_PARENT_SOURCE byte AST equality',restored==parent and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
check('COMPLETE_SOURCE_INVERSES only appends seven namespace rows per BUILD role all other original rows keys values preserved',all(proof['exact_finite_transforms'][role]==original_proof['exact_finite_transforms'][role]+edits[role]for role in('build_host','build_writer'))and all(proof[k]==original_proof[k]for k in proof if k!='exact_finite_transforms')and all(proof['exact_finite_transforms'][role]==original_proof['exact_finite_transforms'][role]for role in('canonical','prepare_host','prepare_writer')))
bi=json.loads((P/'COMPLETE_SOURCE_BINDER_INVERSES.json').read_bytes())['roles']['BUILD_binder'];parent=(P/'ORIGINAL_PARENT_SOURCE/BUILD_binder.full.py').read_text();whole=bi['whole_exact_inverse'];check('full namespace binder inverse then original complete binder inverse equals actual72b196 ORIGINAL_PARENT Source',inverse(fixed['BUILD_binder'],edits['BUILD_binder'])==whole['new']and whole['old']==parent and hashlib.sha256(parent.encode()).hexdigest()==bi['parent_sha256']=='72b19614ca141555bfbe7ab70f74092cc5cc5407f8f69c530f2893ad5f0a315c')
changed=set(names.values())|{'COMPLETE_SOURCE_INVERSES.json'};unmodified=[]
for rel in mf['members']:
 if rel not in changed:assert(U/rel).read_bytes()==(P/rel).read_bytes();unmodified.append(rel)
check('all34 other original mother members remain full original bytes including canonical PREP binder PREP templates Q340owners and originalSource historical reports',len(unmodified)==34)
check('all exact named path anchors removed from three active BUILD Sources and every replacement covered by inverse rows',all(not any(old in text for old,new in mapping)for text in fixed.values()))
oldconst=constants(originals['build_host']);newconst=constants(fixed['build_host']);oldcommands=oldconst['EXPECTED_COMMANDS'];newcommands=newconst['EXPECTED_COMMANDS']
def route(x):
 if type(x)is list:return[route(v)for v in x]
 if type(x)is dict:return{k:route(v)for k,v in x.items()}
 if type(x)is str:
  for old,new in mapping:x=x.replace(old,new)
 return x
check('all original five complete compiler nm nm otool audit-build commands preserved argument order flags inputpaths and only exact outputexe canonical route changed',len(oldcommands)==len(newcommands)==5 and route(oldcommands)==newcommands and oldcommands[0][:-1]==newcommands[0][:-1]and oldcommands[1]==newcommands[1]and oldcommands[3][4:]==newcommands[3][4:]and oldcommands[4][2:]==newcommands[4][2:])
for role in names:
 oldc=constants(originals[role]);newc=constants(fixed[role]);check('all '+role+' future actual globals remain None and schema FAMILY original literals unchanged',{k:v for k,v in oldc.items()if k.startswith('FUTURE_')}=={k:v for k,v in newc.items()if k.startswith('FUTURE_')}and all(v is None for k,v in newc.items()if k.startswith('FUTURE_'))and all(oldc.get(k)==newc.get(k)for k in('FAMILY','SOURCE_BINDING_STATUS','SOURCE_DESIGN_STATUS','ACTUAL_HELPER_Q_PATH','ACTUAL_HELPER_Q_SCHEMA','ACTUAL_HELPER_Q_STATUS','INPUT_HELPERS')))
bt=ast.parse(fixed['BUILD_binder']);bo=ast.parse(originals['BUILD_binder']);olddefs={n.name:ast.get_source_segment(originals['BUILD_binder'],n)for n in bo.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};newdefs={n.name:ast.get_source_segment(fixed['BUILD_binder'],n)for n in bt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
check('all original full helper_Q functions Source3b admission c6 Qwriter saved48 retention and legacy controls definitions unchanged',all(newdefs[k]==v for k,v in olddefs.items()if k!='main')and set(newdefs)==set(olddefs))
check('original typed Root PREP CLOSED0 allcomplete namespace peer caps340 explicit owners and no unknown success bypass preserved by exact inverse',all(x in fixed['BUILD_binder']for x in("peer['actual_PREP_closed_EXIT0_verified']is True","len(ns)==5","source_verify_original_inverse(role,text,edits[role],proof)","all(type(s[k])is int and s[k]==v for k,v in zip(caps,expected_caps))","all Source/meta input unchanged".replace('all Source/meta','actual Source/meta'))))
# Complete proof of the four changed members, including lossless proof JSON
# itself; no Source is accepted through a tool-output excerpt.
derivations=[]
for rel in sorted(changed):
 old=(U/rel).read_bytes();new=(P/rel).read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
 for tag,i,j,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
  if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=j,new_start0=a,new_end0=b,old_full_lines=ol[i:j],new_full_lines=nl[a:b]))
 restored=list(nl)
 for h in reversed(hs):assert restored[h['new_start0']:h['new_end0']]==h['new_full_lines'];restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(restored).encode()==old;derivations.append(dict(relative_path=rel,original_fullpin=mf['members'][rel],derived_fullpin=pin(P/rel),full_byte_inverse_hunks=hs,whole_byte_inverse_equals_sealed_mother=True))
(P/'V25_MONITOR_ACCESS_EXACT_BUILD_NAMESPACE_FULL_BYTE_INVERSES.json').write_text(json.dumps(dict(schema='V25_MONITOR_ACCESS_COMPLETE_BUILD_NAMESPACE_FINITE_FULL_BYTE_INVERSE_V1',source_only=True,original_frozen_mother_manifest_pin=mother_pin,complete_changed_member_derivations=derivations,exact_namespace_transform_rows=edits,unchanged_original_mother_members=unmodified,all_other_original_members_byte_equal=True,original_full_parent_byte_AST_inverse=True,actual_Source_peer=None,actual_Root_Source_admission=None,actual_saved_closed_PREP_peer=None,actual_BUILD_Source_binding=None,actual_BUILD_terminal=None,actual_postclose_manifest=None,scientific_qualification_created=False),indent=2,allow_nan=False)+'\n')
route_meta=dict(schema='V25_MONITOR_ACCESS_COMPLETE_BUILD_ROOT_NEXT_ROUTE_SOURCE_ONLY_V1',source_only=True,active_scope='ONLY_BUILD_BINDER_AND_COMPLETE_BUILD_HOST_POSTCLOSE_WRITER_NAMESPACE_DERIVATIVE',retained_other_canonical_PREP_sources_are_original_mother_provenance_not_monitor_access_active_entrance=True,family_and_schemas_remain_original_V25=True,Root_steps=['Independent complete finite Source review of this original TMP package','Root finite Source-only admission of exact new MF and BUILD roles','Require real monitor-access PREP CLOSED0 persisted complete metadata and independent saved peer','Invoke this original sealed TMP BUILD binder with real exact PREP peer Q/canonical/writer/saved48/retention pins','Root freezes genuinely bound complete BUILD Sources to only new BUILD D/E and executes original whole five stages','Root actual CLOSED terminal then original complete postclose writer; retain actual success or failure evidence'],source_binder=str(P/names['BUILD_binder']),full_Build_host_template=str(P/names['build_host']),full_postclose_writer_template=str(P/names['build_writer']),exact_namespace_names={old:new for old,new in mapping},future_Root_BIND_argv=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(P/names['BUILD_binder']),'--saved-prep-peer-report','<actual persisted monitor-access PREP peer path>','--saved-prep-peer-report-sha256','<actual peer SHA>','--actual-Q-sha256','<actual new Q SHA>','--actual-canonical-sha256','<actual installed monitor-access C SHA>','--destination','<fresh private TMP bound BUILD Source dir>','--actual-new-Q-writer-terminal','<actual Root new Q writer terminal path>','--actual-new-Q-writer-terminal-sha256','<actual Root new Q terminal SHA>','--actual-Q-saved-peer','<actual saved48 review path>','--actual-Q-saved-peer-sha256','<actual saved48 SHA>','--actual-Q-saved-peer-retention','<actual full10members saved48 retention path>','--actual-Q-saved-peer-retention-sha256','<actual saved48 retention SHA>'],actual_Source_peer=None,actual_Root_Source_admission=None,actual_saved_closed_PREP_peer=None,actual_future_Q_and_external_proof_bound_pins=None,actual_BUILD_Source_binding=None,actual_BUILD_terminal=None,actual_postclose_manifest=None,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,candidate_helper_guard_API_compiler_or_numeric_executed=False)
(P/'ROOT_MONITOR_ACCESS_BUILD_NEXT_STEPS.UNREADY.json').write_text(json.dumps(route_meta,indent=2,allow_nan=False)+'\n')
shutil.copy2(__file__,P/'author_monitor_access_BUILD_Source_stdlib.py')
files=[q for q in sorted(P.rglob('*'))if q.is_file()];ast_files=[q for q in files if q.suffix=='.py']
for q in ast_files:ast.parse(q.read_bytes(),filename=str(q))
check('all complete new and retained Python Source files stdlib AST only parsed; no candidate import compile or execution',len(ast_files)>=24)
check('original mother full MF and every Source member7ID frozen unchanged after all own Source work',pin(U/'MANIFEST.json')==mother_pin and all(pin(U/rel)==wanted for rel,wanted in mf['members'].items())and all(identity(U/rel)==wanted for rel,wanted in mf['directories'].items()))
check('new complete namespace all ordinary single-link files and normal directories no aliases',all(not q.is_symlink()and(stat.S_ISDIR(q.lstat().st_mode)or(stat.S_ISREG(q.lstat().st_mode)and q.lstat().st_nlink==1))for q in[P,*P.rglob('*')]))
report=dict(schema='AUTHOR_FINITE_V25_MONITOR_ACCESS_COMPLETE_BUILD_NAMESPACE_SOURCE_CHECK_V1',status='AUTHOR_SOURCE_CHECKS_COMPLETE_UNREADY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,checks=checks,check_count=len(checks),all_checks_typed_true=True,blockers=[],whole_original_mother_members=38,complete_original_mother_manifest_pin=mother_pin,complete_changed_original_member_count=4,complete_unchanged_original_member_count=34,full_changed_member_inverse_hunk_count=sum(len(r['full_byte_inverse_hunks'])for r in derivations),complete_Python_Source_AST_files=len(ast_files),all_new_build_namespace_rows_and_full_original_parent_byte_AST_inverses=True,complete_full_Source_pins_before_seal=[pin(q)for q in files],no_candidate_helper_guard_API_compiler_or_numeric_executed=True,no_material_SQL_graph_trace_payload_read=True,no_project_Source_D_E_ART_write=True,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_saved_closed_PREP_peer=None,actual_BUILD_Source_binding=None,actual_BUILD_terminal=None,actual_postclose_manifest=None,scientific_qualification_created=False)
with(P/'AUTHOR_FINITE_MONITOR_ACCESS_BUILD_SOURCE_CHECK_UNREADY.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
Path('/private/tmp/axmat_v25_monitor_access_BUILD_author_current_path.txt').write_text(str(P)+'\n')
print(json.dumps(dict(status=report['status'],source_only=True,fresh_Source=str(P),check_count=len(checks),Source_AST_files=len(ast_files),changed_original_members=4,unchanged_original_members=34,complete_inverse_hunks=report['full_changed_member_inverse_hunk_count'],author_report_pin=pin(P/'AUTHOR_FINITE_MONITOR_ACCESS_BUILD_SOURCE_CHECK_UNREADY.json'),actual_native_BUILD_execution=None),allow_nan=False))

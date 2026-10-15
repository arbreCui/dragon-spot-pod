"""Static whole-source/inverse review; does not execute any reviewed source."""
from pathlib import Path
import ast,hashlib,json,os,stat
OUT=Path('/private/tmp/axmat_v22_fullbuild_Root_Source_binder_independent_review_05fs3v3d')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
R=Path('/Users/wen/spot');ART=R/'validation/artifacts';E=B/'actual_complete_combined_prepare_v22_receipts'
BINDER=Path('/private/tmp/spot_bind_v22_original_full_build_host_ROOT.py')
OLD=B/'actual_complete_combined_build_v21_sources/combined_build_host.py'
TARGET=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'
checks=[];reads={}
def check(k,v):
 assert type(v)is bool
 checks.append(dict(check=k,passed=v))
 if not v:raise ValueError(k)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 p=Path(p);s=p.lstat();i=identity(s)
 check('explicit Source/META regular '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
 with p.open('rb')as f:
  check('open seven-integer identity '+str(p),identity(os.fstat(f.fileno()))==i)
  b=f.read();check('complete EOF '+str(p),len(b)==s.st_size and f.read(1)==b'')
  check('fd unchanged '+str(p),identity(os.fstat(f.fileno()))==i)
 check('path unchanged '+str(p),identity(p.lstat())==i)
 reads[str(p)]=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
 return b
def load(p):return json.loads(read(p))
def constants(tree):
 d={}
 for n in tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:d[n.targets[0].id]=ast.literal_eval(n.value)
   except(ValueError,TypeError):pass
 return d
raw=read(BINDER);source=raw.decode();tree=ast.parse(raw)
check('original frozen Root binder44316f',reads[str(BINDER)]['sha256']=='44316f47416c5973c417a3ad07261cd1704bd091ebbb1f1a19ba9713ec7bf15a')
old=read(OLD);check('whole original host ebe99a',reads[str(OLD)]['sha256']=='ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196')
canonical=read(TARGET);check('actual fixed canonical09e539',reads[str(TARGET)]['sha256']=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e')
ctree=ast.parse(canonical);cvalues=constants(ctree)
check('actual canonical70 definitions',sum(isinstance(n,(ast.FunctionDef,ast.ClassDef))for n in ctree.body)==70)
check('canonical V22 source-ready literal',cvalues['DRAFT_STATUS']=='READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('all six future business pins remainNone',all(cvalues[k]is None for k in future))
summary=load(E/'Root_actual_complete_combined_prepare_summary.json')
namespace=load(E/'Root_actual_complete_prepare_namespace_manifest.json')
terminal=load(E/'Root_actual_prepare_tool_terminal_return.json')
check('actual PREP-only schema/status',summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
check('actual terminal closed integer0 no session',terminal['closed']is True and type(terminal['terminal_tool_return']['exit_code'])is int and terminal['terminal_tool_return']['exit_code']==0 and 'session_id'not in terminal['terminal_tool_return'])
check('Root summary terminal full pin actual',summary['actual_root_terminal']=={k:reads[str(E/'Root_actual_prepare_tool_terminal_return.json')][k]for k in ('path','sha256','identity')})
check('Root summary namespace full pin actual',summary['namespace_manifest']=={k:reads[str(E/'Root_actual_complete_prepare_namespace_manifest.json')][k]for k in ('path','sha256','identity')})
check('namespace canonical pin exact',namespace['canonical_factory']=={k:reads[str(TARGET)][k]for k in ('path','sha256','identity')})
Q=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json';q=load(Q)
check('true joint helperQ89d2 full pin',reads[str(Q)]['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816')
check('Q metadata-only status',q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V22')
HP=R/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py';read(HP)
check('new helpercf0 full SOURCE pin',reads[str(HP)]['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'and q['helper']==reads[str(HP)])
paths={
 'S':ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010',
 'O':ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010',
 'T':ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010',
}
for label,k,rel,root in [('declaration','actual_declaration','declaration.json','O'),('prep','formal_PREP_terminal','declaration_terminal_return.json','T'),('graph','actual_complete_input_graph','input_graph.json','O'),('trace','actual_complete_creation_trace','input_creation_python_open_trace.json','O')]:
 ref=summary[k]
 row=next(n for n in namespace['namespaces']if n['root']==str(paths[root]))['files'][rel]
 check('full immutable prepared output reference '+label,ref==row and ref['path']==str(paths[root]/rel)and len(ref['identity'])==7 and all(type(v)is int for v in ref['identity']))
declaration=summary['actual_declaration'];prep=summary['formal_PREP_terminal'];graph=summary['actual_complete_input_graph'];trace=summary['actual_complete_creation_trace']
changes=[
('axial-material-complete-combined-build-host-v21-20261010','axial-material-complete-combined-build-host-v22-20261010'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py',TARGET.name),
('023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',reads[str(TARGET)]['sha256']),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010',paths['S'].name),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010',paths['O'].name),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010',paths['T'].name),
('actual_complete_combined_build_v21_sources','actual_complete_combined_build_v22_sources'),
('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V21','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22_DECLARATION_V1'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_BUILD_SEAL_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22_BUILD_SEAL_V1'),
('AXMAT_V21_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1','AXMAT_V22_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1'),
('combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',HP.name),
('dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7',reads[str(HP)]['sha256']),
('Root_actual_complete_graph_private_verifier_helper_admission_v21.json',Q.name),
('29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2',reads[str(Q)]['sha256']),
('80d67cd194eed1d229e46cd5512df9ba4b00954e7f6e7b36dd8ea6902851d6af',declaration['sha256']),
('7e340a31596aa58518ebde4231bd3542554acb0a4ea1888f1df7ea14bec50dcf',prep['sha256']),
('d5622ad2b2661a336134cb97a2bbf113bfb76327a467149644e539a0009c2779',graph['sha256']),
('06fb0e5b3abe6efd38a0656e0b1e3572581ceab018825cd07be3f52683876244',trace['sha256']),
('actual_complete_combined_prepare_v21_receipts','actual_complete_combined_prepare_v22_receipts'),
('21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344',reads[str(E/'Root_actual_complete_combined_prepare_summary.json')]['sha256'])]
change_node=next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(v,ast.Name)and v.id=='changes'for v in n.targets))
check('all 21 original literal substitution anchors',len(change_node.elts)==21 and [ast.literal_eval(n.elts[0])for n in change_node.elts]==[c[0]for c in changes])
text=old.decode();ledger=[]
for before,after in changes:
 count=text.count(before);check('all parent literal occurrences '+before,count>0 and before!=after)
 text=text.replace(before,after);ledger.append(dict(before=before,after=after,count=count))
back=text
for c in reversed(ledger):
 check('unique full inverse literal '+c['after'],back.count(c['after'])==c['count'])
 back=back.replace(c['after'],c['before'])
check('complete byte inverse restores whole ebe99a host',back.encode()==old)
check('whole AST inverse restores parent',ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
newtree=ast.parse(text);values=constants(newtree)
check('original full five labels unchanged',values['EXPECTED_LABELS']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'])
check('all five commands retained',len(values['EXPECTED_COMMANDS'])==5)
check('original live stages metadata audit own command pins',values['EXPECTED_COMMANDS'][-1]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(TARGET),'audit-build','--sha256',declaration['sha256'],'--prep-sha256',prep['sha256']])
for label,anchor in [
 ('original1800/600/512/2GiB', 'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30'),
 ('all dynamic Sourcearchive members',"sorted(SOURCE_ARCHIVE.rglob('*'))"),
 ('original600 inner maximum',"iw['wall_cap_seconds']<=stage['wall_cap_seconds']<=600"),
 ('original5 supervised commands',"len(inner)!=5"),
 ('four original tails',"set(('result','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'))"),
 ('complete raw4tool outputs',"EXPECTED_LABELS[:4]"),
 ('complete OUT seal allmembers',"set(files)!=set(seal['files'])|{'seal.json'}"),
 ('original genuine MRO',"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)"),
 ('original dynamic96history/free8',"DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30"),
 ('entire HOST S O T Sourcearchive joint cap',"support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))"),
 ('post SOURCE input allunchanged',"for entry in inputs+[hpin,rpin]:"),
 ('genuine fresh no replay',"no prior build execution or build retry allowed"),
 ('wholeINPUT false',"whole_combined_INPUT_admitted=False"),
 ('sciencefalse',"native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False"),
 ]:check(label,anchor in text)
support=B/'actual_prepare_sources/prepare_cli_host_v15.py';sup=read(support);check('original normal support source fixed',reads[str(support)]['sha256']=='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7')
check('binder no helper guard API execution',not any(isinstance(n,ast.Import)and any(a.name.startswith(('importlib','ctypes'))for a in n.names)for n in ast.walk(tree)))
check('binder refuses allART reads',"not p.is_relative_to(ART)"in ast.get_source_segment(source,next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='read')))
check('binder validates source-only exact integer caps',"all(type(s[k]) is int and s[k]==v for k,v in zip(caps,wanted))"in source)
check('binder whole inverse assertion exists',"assert restored.encode()==old"in source)
check('binder never starts business',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','run','Popen','exec_module')for n in ast.walk(tree)))
for p,v in list(reads.items()):read(Path(p));check('whole explicit Source/META after unchanged '+p,reads[p]==v)
blocker=dict(id='saved_PREP_peer_not_bound_to_this_actual_PREP',source=str(BINDER),
 line=44,detail="Only PASS=True and empty hard_blockers are checked. Missing peer exact schema plus actual Root summary/terminal/namespace pin equality to current sp/tp/np. Correct externally chosen peer is operational evidence, not this Source hard predicate.")
report=dict(schema='INDEPENDENT_V22_ORIGINAL_FULL_BUILD_ROOT_BINDER_SOURCE_REVIEW_V1',source_only=True,
 status='ORIGINAL_DRAFT_SOURCE_BLOCKED_PENDING_EXACT_SAVED_PEER_BINDING',all_nonblocker_checks_passed=True,
 checks=checks,check_count=len(checks),blockers=[blocker],fixed_original_binder=reads[str(BINDER)],
 full_original_host=reads[str(OLD)],full_SOURCE_META_reads=reads,complete_21_changes=ledger,
 independent_static_expected_host_sha256=hashlib.sha256(text.encode()).hexdigest(),
 static_text_never_saved_as_bound_host=True,reviewed_generator_host_helper_guard_API_or_business_executed=False,
 ART_or_material_payload_read=False,actual_fullbuild_or_INPUT_or_science_qualified=False,
 required_actual_entrypoint='Root first validates exact saved peer, executes metadata-only binder with3argv into absent fresh TMP; independently reviews its actual source output; installs/freezes complete new D; prelaunch full inputs/aliases/resources; unique genuine host normal no-extra-argv run.',
 actual_caps=[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0])
(OUT/'ORIGINAL_DRAFT_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,checks=len(checks),source_blocker_count=1,expected_source_host_sha256=report['independent_static_expected_host_sha256'],review_sha256=hashlib.sha256((OUT/'ORIGINAL_DRAFT_REVIEW.json').read_bytes()).hexdigest(),business_executed=False),indent=2))

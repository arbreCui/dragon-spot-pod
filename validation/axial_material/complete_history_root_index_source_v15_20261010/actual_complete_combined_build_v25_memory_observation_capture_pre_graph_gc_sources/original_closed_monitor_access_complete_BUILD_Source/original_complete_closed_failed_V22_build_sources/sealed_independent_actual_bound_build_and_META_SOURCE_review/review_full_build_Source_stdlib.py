"""Finite independent Source/META inspection only; no reviewed module or API is executed."""
import ast,hashlib,json,math,pathlib,stat
R=pathlib.Path(__file__).parent
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_combined_prepare_v22_receipts'
P=pathlib.Path('/private/tmp/axmat_v22_actual_full_build_READY_SOURCE_root_20261010_b8ad01')
W=pathlib.Path('/private/tmp/spot_v22_complete_build_postclose_META_ROOT_SOURCE_20261010_6ed606')
PEER=E/'sealed_independent_v22c_full_build_actual_saved_peer_shape_Source_review'
checks=[];pins={}
def check(ok,label):
 if ok is not True:raise ValueError(label)
 checks.append(dict(check=label,passed=True))
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);i=identity(p)
 check(stat.S_ISREG(i[2]) and i[3]==1,'ordinary single-link '+str(p))
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 check(identity(p)==i,'full EOF stable '+str(p))
 q=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
 if str(p) in pins:check(pins[str(p)]==q,'repeated full pin unchanged '+str(p))
 else:pins[str(p)]=q
 return q
def verify(q,label):
 actual=pins.get(q['path']) or pin(q['path'])
 check(identity(pathlib.Path(q['path']))==actual['identity'],label+' live7ID')
 for k in ('path','sha256','size_bytes','identity'):
  if k in q:check(q[k]==actual[k],label+' '+k)
 return actual
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def read(p):
 p=pathlib.Path(p);pin(p)
 with p.open(encoding='utf8') as f:return json.load(f,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite')))
def package(root,sha,schema):
 m=read(root/'MANIFEST.json');check(pins[str(root/'MANIFEST.json')]['sha256']==sha,'actual fixed manifest '+str(root))
 check(m['schema']==schema and m['source_only'] is True,'complete Source package schema '+str(root))
 check(type(m['members']) is dict and m['member_count']==len(m['members'])==5,'actual Source package all five members')
 check({p.name for p in root.iterdir()}==set(m['members'])|{'MANIFEST.json'},'complete actual six files no extras '+str(root))
 for rel,q in m['members'].items():check(q['path']==str(root/rel),'manifest logical member path '+rel);verify(q,'complete Source member')
 return m
hm=package(P,'c8514275f297ac1344dfd3dd05d3b75a550516ef22ce568e33f4c868ada5bdae','ROOT_V22_ACTUAL_FULL_BUILD_SOURCE_BOUND_PACKAGE_MANIFEST_V1')
wm=package(W,'f0a11bc559fc21a04dcea470d4e4eaa321d2f7725745ed9d7c24f012e6ce2998','ROOT_V22_COMPLETE_BUILD_POSTCLOSE_META_WRITER_SOURCE_PACKAGE_V1')
check(hm['new_business_executed'] is False and wm['business_numeric_executed'] is False,'Source packages do not fabricate business')
host=(P/'combined_build_host.py').read_text();old=(P/'original_full_V21_build_host.byte_exact.py').read_text()
writer=(W/'write_actual_build_postclose_META.py').read_text();oldwriter=(W/'original_complete_V21_postclose_META_writer.byte_exact.py').read_text()
hp=pin(P/'combined_build_host.py');wp=pin(W/'write_actual_build_postclose_META.py')
check(hp['sha256']=='cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269' and hp['size_bytes']==18312,'true bound complete host')
check(wp['sha256']=='d246786b9f02b2b8f8024d2d4b8bf80a0de8e9eb6dff2ba801fd10c1f3d4b5b7' and wp['size_bytes']==37042,'true bound postclose metadata writer')
check(pins[str(P/'original_full_V21_build_host.byte_exact.py')]['sha256']=='ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196','actual full original V21 host')
proof=read(P/'Root_actual_full_build_Source_binding_inverse.json');wproof=read(W/'SOURCE_inverse.json')
def inverse(new,original,changes,count,label):
 check(len(changes)==count,label+' exact finite hunk count')
 forward=original
 for c in changes:
  before,after,n=c['before'],c['after'],c['count']
  check(type(n) is int and n>0 and forward.count(before)==n and before!=after,label+' exact forward literal count '+before)
  forward=forward.replace(before,after)
 check(forward==new,label+' whole exact forward bytes')
 back=new
 for c in reversed(changes):
  check(back.count(c['after'])==c['count'],label+' exact reverse literal count '+c['after'])
  back=back.replace(c['after'],c['before'])
 check(back==original,label+' full byte inverse restores original')
 check(ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False),label+' full AST inverse')
 for typ in (ast.If,ast.Assert,ast.Raise):
  a=[ast.dump(x,include_attributes=False) for x in ast.walk(ast.parse(back)) if isinstance(x,typ)]
  b=[ast.dump(x,include_attributes=False) for x in ast.walk(ast.parse(original)) if isinstance(x,typ)]
  check(a==b,label+' all original '+typ.__name__+' AST order/values preserved')
 return back
inverse(host,old,proof['finite_changes'],21,'full five-stage host')
inverse(writer,oldwriter,wproof['finite_hunks'],10,'full postclose writer')
verify(proof['complete_original_host'],'original host Source pin')
check(pathlib.Path(proof['complete_original_host']['path']).read_bytes()==(P/'original_full_V21_build_host.byte_exact.py').read_bytes(),'original V21 host complete Source retained')
verify(wproof['original'],'original full postclose writer pin')
check(pathlib.Path(wproof['original']['path']).read_bytes()==(W/'original_complete_V21_postclose_META_writer.byte_exact.py').read_bytes(),'original metadata writer full Source retained')
def defs(text):return {x.name:x for x in ast.parse(text).body if isinstance(x,ast.FunctionDef)}
newdefs=defs(writer);olddefs=defs(oldwriter)
check(list(newdefs)==list(olddefs) and len(newdefs)==21,'all21 full metadata writer definitions/order')
def segment(text,node):
 return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
changed=[name for name in newdefs if segment(writer,newdefs[name])!=segment(oldwriter,olddefs[name])]
check(changed==['compare_source_freeze','expected_commands','success_checks','main'],'only four functions have literal/comment retargets')
check(sum(segment(writer,newdefs[k])==segment(oldwriter,olddefs[k]) for k in newdefs)==17,'17 original metadata functions byteexact')
check(len(defs(host))==len(defs(old))==1 and list(defs(host))==['main'],'entire original host main preserved through inverse')
for tree,label,original in ((ast.parse(host),'host',old),(ast.parse(writer),'writer',oldwriter)):
 nodes=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom))]
 orig=[x for x in ast.parse(original).body if isinstance(x,(ast.Import,ast.ImportFrom))]
 check([ast.dump(x) for x in nodes]==[ast.dump(x) for x in orig],label+' all original imports preserved')
def constants(text):
 out={}
 for x in ast.parse(text).body:
  if isinstance(x,ast.Assign):
   for t in x.targets:
    if isinstance(t,ast.Name):
     try:out[t.id]=ast.literal_eval(x.value)
     except (ValueError,TypeError):pass
 return out
hc=constants(host);wc=constants(writer);bc=constants((P/'ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py').read_text())
labels=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
check(hc['EXPECTED_LABELS']==labels and wc['LABELS']==labels and len(hc['EXPECTED_COMMANDS'])==5,'all exact five stages/complete command arrays')
check("WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30" in host and 'WHOLE, STAGE, RSS, ARCHIVE, HISTORY, FREE = 1800, 600, 512, 2*2**30, 96*2**30, 8*2**30' in writer,'all original explicit caps unchanged')
for needle in ['resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)','helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','type(runner) is not full.OwnRSSSerialExecutor','children_at_once=1,retries=0','own_child_only','liveness_group_cleanup','FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY']:
 check(needle in host,'full genuine host guard retained '+needle)
for needle in ['len(inner)!=5','[s[\'command\'] for s in inner]!=EXPECTED_COMMANDS','raw[\'before_binary_identity_gates\'] is not True','inner_watches!=result[\'watchdogs\']','inner_watches[:-1]!=audit[\'previous_stage_watchdogs\']','seal[\'directories\']!=sorted(directories)','complete pinned inputs changed']:
 check(needle in host,'full host exact field/command/record control '+needle)
for needle in ['full_declared_physical_input_prelaunch_7ID_claimed=False','for path,sha in d[\'files\'].items()','unchanged_ordered_original_fixed_input_results=unchanged','full_declared_physical_input_finalpass_claimed=checks is not None','separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False','ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',"directories={'.':identity(root)}",'original ordered fixed inputs including repeats differ','actual_root_host_launchargs=actual[\'actual_launch_arguments\']','Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass=True','original_host_final_input_revalidation_observed=False']:
 check(needle in writer,'full postclose truthful complete control '+needle)
check(wc['HOST_SHA']==hp['sha256'] and wc['FACTORY_SHA']==hc['TARGET_SHA'] and wc['DECL_SHA']==hc['DECLARATION_SHA'] and wc['PREP_SHA']==hc['PREP_SHA'],'writer/host exact Source and PREP SHA interface')
rootreceipt=read(E/'Root_actual_v22c_full_build_Source_binding_tool_return.json')
authorreceipt=read(E/'Root_actual_build_postclose_META_Source_author_tool_return.json')
def closed(rec,chunk,label):
 q=rec['actual_tool_return']
 check(rec['closed'] is True and rec['observed_terminal'] is True and type(q['exit_code']) is int and q['exit_code']==0 and 'session_id' not in q,label+' actual strict CLOSED EXIT0')
 check(q['chunk_id']==chunk,label+' real Root tool chunk')
 return json.loads(q['output'])
actualgen=closed(rootreceipt,'6ed606','actual host Source binder')
actualauthor=closed(authorreceipt,'93894d','actual metadata Source author')
check(actualgen['manifest']==pins[str(P/'MANIFEST.json')] and actualgen['host']==hp and actualgen['finite_hunks']==21 and actualgen['project_executed'] is False,'actual Sourcegen complete output binds package')
check(rootreceipt['source_and_metadata_only'] is True and rootreceipt['new_numeric_execution'] is False and rootreceipt['whole_build_qualified'] is False,'actual Sourcegen metadata only scope')
for q in proof['all_source_inputs']:verify(q,'all actual Source binder inputs')
check(len(proof['all_source_inputs'])==9,'nine complete actual Source binder inputs')
check((P/'ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py').read_bytes()==pathlib.Path(proof['all_source_inputs'][-1]['path']).read_bytes(),'actual v22c binder full byteexact')
check(pins[str(P/'ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py')]['sha256']=='72b19614ca141555bfbe7ab70f74092cc5cc5407f8f69c530f2893ad5f0a315c','actual qualified binder SHA')
peer=read(P/'ACTUAL_SAVED_PREP_PEER.byte_exact.json')
verify(proof['actual_saved_PREP_peer'],'actual retained full savedPREP peer')
check((P/'ACTUAL_SAVED_PREP_PEER.byte_exact.json').read_bytes()==pathlib.Path(proof['actual_saved_PREP_peer']['path']).read_bytes(),'full actual PREP peer byteexact')
check(peer['schema']=='INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and peer['blockers']==[] and peer['actual_PREP_metadata_only'] is True and peer['all_checks_typed_true'] is True,'actual complete PREP peer exact contract')
check(peer['check_count']==10170==len(peer['checks']) and all(c['passed'] is True for c in peer['checks']),'all10170 actual savedPREP checks typed true')
for k,pk in [('actual_Root_PREP_summary_pin','actual_closed_PREP_summary'),('actual_Root_PREP_terminal_pin','actual_Root_closed_terminal'),('actual_complete_namespace_manifest_pin','actual_complete_NAMESPACE')]:
 check(peer[k]==proof[pk],'actual PREP peer full crosspin '+k);verify(peer[k],'real actual PREP independent fullpin')
summary=read(proof['actual_closed_PREP_summary']['path']);terminal=read(proof['actual_Root_closed_terminal']['path']);namespace=read(proof['actual_complete_NAMESPACE']['path'])
check(summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD' and terminal['closed'] is True and type(terminal['terminal_tool_return']['exit_code']) is int and terminal['terminal_tool_return']['exit_code']==0 and 'session_id' not in terminal['terminal_tool_return'],'same actual closed PREP')
check(len(namespace['namespaces'])==5 and namespace['no_build_or_native_credit'] is True,'same complete PREP five namespace scope')
ns={q['root']:q for q in namespace['namespaces']}
for label,q in proof['all_actual_output_references'].items():
 p=pathlib.Path(q['path']);check(ns[str(p.parent if label!='source_admission' else p.parent)]['files'][p.name]==q,'all actual PREP output reference fullpin '+label)
 # These large encoded graph/trace contents were fully hashed in the sealed10170 saved-META review; do not re-read them here.
 match=[r for r in peer['complete_full_EOF_input_pins'] if r['path']==q['path']]
 check(len(match)==1 and all(match[0][k]==q[k] for k in ('path','sha256','identity')),'reuse full EOF savedPREP output '+label)
dpath=proof['all_actual_output_references']['declaration']['path'];d=json.loads(pathlib.Path(dpath).read_text())
check(hc['EXPECTED_COMMANDS']==[d['production_link_command'],['/usr/bin/nm','-g',*d['actual_production_objects']],['/usr/bin/nm','-g',str(pathlib.Path(dpath).parent/'runtime/Dragon')],['/usr/bin/otool','-L',str(pathlib.Path(dpath).parent/'runtime/Dragon'),'/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-build-20261007/runtime/Dragon','/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/runtime/Dragon','/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon','/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/runtime/Dragon'],[d['python_command'],'/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py','audit-build','--sha256',hc['DECLARATION_SHA'],'--prep-sha256',hc['PREP_SHA']]],'all five host commands exactly current declaration and original canonical Source')
# Complete current declaration metadata is already fixed by saved PREP EOF proof; additionally pin only this explicit META.
pin(dpath)
support=B/'actual_prepare_sources/prepare_cli_host_v15.py'
check(pin(support)['sha256']==hc['SUPPORT_SHA'],'actual original normal support SOURCE')
genuine=[
 ('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
 ('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
 ('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),
 ('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
 ('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')]
for p,sha in genuine:check(pin(p)['sha256']==sha,'genuine619/705/38de/bc4/ebbb actual full Source '+p)
pm=read(PEER/'MANIFEST.json');pr=read(PEER/'REVIEW.json')
check(pins[str(PEER/'MANIFEST.json')]['sha256']=='4c7a8fd390684379de8a312ca1695ea939c7a432b7b0967e5555f463dfacf22b','retained qualified Source binder peer manifest')
check(pm['qualified_generator_sha256']==pins[str(P/'ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py')]['sha256'] and pm['actual_savedPREP_peer_sha256']==pins[str(P/'ACTUAL_SAVED_PREP_PEER.byte_exact.json')]['sha256'],'actual qualified Source binder scope')
for q in pm['members']:
 p=PEER/q['relative_path'];check(pin(p)['sha256']==q['sha256'] and pins[str(p)]['size_bytes']==q['size_bytes'],'complete retained Source peer member '+q['relative_path'])
check(pr['check_count']==403 and pr['PASS'] is True and pr['all_checks_passed'] is True and pr['blockers']==[],'retained403 plus original369 qualified Source peer')
sr=read(PEER/'_actual_peer_seal_receipt.json')
check(sr['closed'] is True and sr['actual_tool_terminal_return_observed'] is True and type(sr['terminal_tool_return']['exit_code']) is int and sr['terminal_tool_return']['exit_code']==0 and 'session_id' not in sr['terminal_tool_return'],'retained actual Source peer real CLOSED EXIT0 seal')
first=read(W/'FIRST_SOURCE_AUTHOR_FUNCTION_COMMENT_INVENTORY_FAILURE.json')
check(first['closed'] is True and first['observed_terminal'] is True and type(first['actual_tool_return']['exit_code']) is int and first['actual_tool_return']['exit_code']==1,'author0786a5 Source failure honestly retained')
canonical=pathlib.Path(proof['all_source_inputs'][1]['path']).read_text();cc=constants(canonical)
check(len(defs(canonical))==70 and cc['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==wc['Q_SHA'],'complete current70 canonical and actual newQ Source')
six=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
for name in six:check(cc[name] is None,'all six future business pins remain None '+name)
caps=[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0]
check(proof['original_caps']==wproof['original_caps']==caps,'all full host/writer proof original budgets')
initial=dict(pins)
for p,q in initial.items():check(pin(p)==q,'final full EOF SHA7ID unchanged '+p)
report=dict(schema='INDEPENDENT_V22_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],checks=checks,check_count=len(checks),actual_bound_build_host_pin=hp,actual_postclose_META_writer_pin=wp,actual_Root_Source_binding_tool_receipt_pin=pins[str(E/'Root_actual_v22c_full_build_Source_binding_tool_return.json')],qualified_actual_bound_Source_manifest_pin=pins[str(P/'MANIFEST.json')],qualified_postclose_META_Source_manifest_pin=pins[str(W/'MANIFEST.json')],actual_Root_postclose_META_Source_author_tool_receipt_pin=pins[str(E/'Root_actual_build_postclose_META_Source_author_tool_return.json')],complete_21_literal_host_inverse_to_original=True,complete_10_literal_writer_inverse_to_original=True,all21_writer_functions_retained=True,writer17functions_byteexact=True,all70_canonical_definitions_retained=True,all_original_five_stages_and_full_commands_retained=True,all_original_caps=caps,all_six_future_business_pins_None=True,actual_saved_PREP_10170_scope_and_three_pins_bound=True,complete_reviewed_Source_and_META_file_pins=list(pins.values()),large_encoded_graph_trace_read_from_saved_review_pin_proof_only=True,reviewer_imported_or_executed_reviewed_Source=False,reviewer_called_guard_or_API=False,new_business_or_numeric_execution=False,whole_combined_build_qualified=False,whole_combined_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,goal_complete=False,cleanup_performed=False,future_actual_root_terminal_required_fields=['closed','observed_after_actual_terminal_return','session_repolled_after_close','terminal_tool_return','exit_code','initial_tool_return','original_session_id','observations','record_producer','actual_launch_arguments'],future_actual_source_freeze_required_schema='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',future_source_directory_inventory_includes_dot=True,future_prelaunch_fixed_input_pins_preserve_full_host_order_and_duplicates=True,actual_successful_build_not_yet_observed=True)
(R/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(R/'REPORT.txt').write_text('PASS: actual bound five-stage build host and complete postclose metadata writer Source only.\n21 host literal changes and10 writer literal changes independently restore full originals byte-for-byte and AST; all original predicates/guards/commands preserved.\nAll21 metadata writer functions retained;17 byteexact; four have only family/binding literal or comment changes. True closed Root Source binder6ed606 and Source author93894d bind the fixed Source packages.\nActual saved PREP10170 complete checks and three real summary/terminal/namespace pins match; original five-stage scope and1800/600/512/2GiB/96GiB/free8/1/1/0 retained.\nFuture Root must create actual original typed terminal observations, BUILD freeze with dot directory7ID, and complete ordered input pins including repeats. Source writer must be installed before final D freeze.\nNo reviewer project/API/guard/business/numeric execution. No full build/whole INPUT/native/AAA/ABA/science qualification is assigned.\n')
print(json.dumps(dict(status=report['status'],check_count=len(checks),complete_Source_META_file_count=len(pins),host=hp,writer=wp,review=str(R/'REVIEW.json')),allow_nan=False))


"""Review actual saved failed-build evidence using stdlib only; never import/run project code."""
import ast,hashlib,json,math,os,pathlib,stat
R=pathlib.Path(__file__).parent
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010');ART=pathlib.Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_combined_build_v22_sources';E=B/'actual_complete_combined_build_v22_receipts'
H=ART/'axial-material-complete-combined-build-host-v22-20261010';S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010';T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010'
F=pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py')
checks=[];pins={}
def need(ok,label):
 if ok is not True:raise ValueError(label)
 checks.append(dict(check=label,passed=True))
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p):
 p=pathlib.Path(p);i=identity(p)
 need(stat.S_ISREG(i[2]) and i[3]==1,'regular single-link '+str(p))
 with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 need(i==identity(p),'complete EOF stable '+str(p))
 q=dict(path=str(p),sha256=d,size_bytes=i[4],identity=i)
 if str(p) in pins:need(pins[str(p)]==q,'repeat complete pin unchanged '+str(p))
 else:pins[str(p)]=q
 return q
def verify(q,label):
 v=pins.get(q['path']) or full(q['path'])
 need(identity(pathlib.Path(q['path']))==v['identity'],label+' live7ID')
 for k in ('path','sha256','size_bytes','identity'):
  if k in q:need(q[k]==v[k],label+' '+k)
 return v
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate metadata key')
  d[k]=v
 return d
def read(p):
 p=pathlib.Path(p);full(p)
 with p.open(encoding='utf8') as f:return json.load(f,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite metadata')))
def walk(root):
 files={};directories={'.':identity(root)};syms={}
 for folder,dirs,names in os.walk(root,followlinks=False):
  for name in dirs+names:
   p=pathlib.Path(folder)/name;rel=str(p.relative_to(root));i=identity(p)
   if stat.S_ISLNK(i[2]):syms[rel]=dict(identity=i,literal_target=os.readlink(p))
   elif stat.S_ISDIR(i[2]):directories[rel]=i
   elif stat.S_ISREG(i[2]):files[rel]=pins.get(str(p)) or full(p);need(identity(p)==files[rel]['identity'],'namespace current pin '+str(p))
   else:raise ValueError('nonordinary namespace')
  dirs[:]=[n for n in dirs if not (pathlib.Path(folder)/n).is_symlink()]
 return files,directories,syms
def finite(v,label):
 need(type(v) in (int,float) and math.isfinite(v),label+' finite typed')
expected={
 E/'Root_actual_build_tool_terminal_return.json':'7b66ecbcac1048e079b8197a7821e12761d05c55d4ff6603555c53d220f09d07',
 E/'Root_actual_failed_complete_combined_build_summary.json':'15fa2b3bf27ca8249cc5ddf94debd03da8c45b83e6d67566dcef1c58b46264a4',
 E/'Root_actual_failed_build_namespace_manifest.json':'8867aff897fd1c2ca28062c3a40ea7fabecc5fa5f7aa5fe5d295f4d5bb033719',
 E/'Root_prelaunch_complete_build_source_freeze.json':'3a5c324f7158af2216a5d6ee7aee53276e7de734676e19975be015cb42799715',
 E/'Root_final_prelaunch_source_input_and_reserve_check.json':'f32c7ad5ec83a058c2d95c671e5c213a17d1d38dad3c30de6ad43dcd9400e760',
 D/'combined_build_host.py':'cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269',
 D/'write_actual_build_postclose_META.py':'d246786b9f02b2b8f8024d2d4b8bf80a0de8e9eb6dff2ba801fd10c1f3d4b5b7',
 F:'09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'}
for p,sha in expected.items():need(full(p)['sha256']==sha,'actual fixed Root Source/META SHA '+str(p))
summary=read(E/'Root_actual_failed_complete_combined_build_summary.json');ns=read(E/'Root_actual_failed_build_namespace_manifest.json');root=read(E/'Root_actual_build_tool_terminal_return.json')
need(root['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1' and root['record_producer']=='root','actual Root failed build receipt schema')
need(root['closed'] is True and root['observed_terminal'] is True and root['observed_after_actual_terminal_return'] is True and root['session_repolled_after_close'] is False,'actual closed Root observation/no repoll')
tr=root['terminal_tool_return'];initial=root['initial_tool_return']
need(type(tr['exit_code']) is int and tr['exit_code']==1 and 'session_id' not in tr and tr['chunk_id']=='65203e','actual true failed terminal65203e EXIT1')
need(type(root['exit_code']) is int and root['exit_code']==tr['exit_code'] and root['original_session_id']==70899 and type(root['original_session_id']) is int and initial['session_id']==70899 and initial['chunk_id']=='197727' and 'exit_code' not in initial,'true original live launch70899')
closed_seen=False
for q in root['observations']:
 need(not closed_seen,'no observation after closed tool return')
 if 'session_id' in q:need(q['session_id']==70899,'only actual original session observation')
 if 'exit_code' in q:need(q==tr,'actual terminal observation byte-value equality');closed_seen=True
need(closed_seen and len(root['observations'])==3,'complete real observations include closure')
freeze=read(E/'Root_prelaunch_complete_build_source_freeze.json');pre=read(E/'Root_final_prelaunch_source_input_and_reserve_check.json')
need(freeze['schema']=='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and freeze['source_root']==str(D) and freeze['no_SOURCE_append_after_freeze'] is True,'fixed full build SOURCE freeze')
fd,dd,sd=walk(D)
need(len(fd)==freeze['actual_complete_SOURCE_file_count']==123 and len(dd)==12 and sd==freeze['symlinks']=={},'D123 files/12 root-inclusive directories complete')
need(set(fd)==set(freeze['complete_files']) and dd==freeze['complete_directories'],'all frozen SOURCE names/dirs7ID unchanged')
for rel,q in freeze['complete_files'].items():need(q['path']==str(D/rel),'frozen exact logical path '+rel);verify(q,'frozen full source')
need(pre['status']=='PRELAUNCH_PASS_NO_BUILD_EXECUTED' and pre['fixed_input_entries_count']==155 and len(pre['fixed_input_pins'])==155,'true historical prelaunch155 ordered inputs')
need(ns['ordered_original_fixed_input_expected_pins']==pre['fixed_input_pins'] and len(ns['unchanged_ordered_original_fixed_input_results'])==155 and ns['original_fixed_input_failures']==[],'actual unchanged155 complete expected/result scope')
for index,(expectedq,actualq) in enumerate(zip(pre['fixed_input_pins'],ns['unchanged_ordered_original_fixed_input_results'])):
 need(actualq['index']==index,'retain original ordered index '+str(index));v=verify(expectedq,'all155 original expected input');verify(actualq['pin'],'all155 actual postclose input')
 need({k:v[k] for k in ('path','sha256','identity')}==actualq['pin'],'actual unchanged result fullpin '+str(index))
# Independently reconstruct the host's complete original pin order, including duplicate SOURCE/TERMINAL entries.
seven=pre['fixed_input_pins'][:7]
sfiles=walk(S)[0];tfiles=walk(T)[0]
prepared_t={k:v for k,v in tfiles.items() if k in ['actual_child_merged_stdout_stderr.json','actual_external_host_stderr.txt','actual_external_host_stdout.json','actual_external_Root_tool_terminal.json','Root_actual_SOURCE_inventory.json','declaration_terminal_return.json']}
ordered=[q['path'] for q in seven]+sorted(q['path'] for q in fd.values())
ordered += [str(O/'declaration.json'),str(T/'declaration_terminal_return.json'),str(O/'input_graph.json'),str(O/'input_creation_python_open_trace.json')]
ordered += sorted(q['path'] for q in sfiles.values())+sorted(q['path'] for q in prepared_t.values())
ordered += [str(B/'actual_complete_combined_prepare_v22_receipts/Root_actual_prepare_tool_terminal_return.json'),str(B/'actual_complete_combined_prepare_v22_receipts/Root_actual_complete_combined_prepare_summary.json'),'/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py','/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py']
need(ordered==[q['path'] for q in pre['fixed_input_pins']] and len(prepared_t)==6,'entire host order7+D123+4+S11/T6+2+619/ebbb with duplicates')
need(ns['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_POSTCLOSE_FINITE_NAMESPACES_V1' and ns['mode']=='FAILED_BUILD_SAVED_METADATA_ONLY','failure-only full namespace scope')
need([q['root'] for q in ns['namespaces']]==[str(p) for p in (H,S,O,T,D,E)],'all H/S/O/T/D/E namespaces')
counts={}
laterE={'Root_actual_failed_build_namespace_manifest.json','Root_actual_failed_complete_combined_build_summary.json','Root_actual_failed_build_META_writer_tool_terminal_return.json'}
for view in ns['namespaces']:
 p=pathlib.Path(view['root']);files,dirs,syms=walk(p)
 need(view['present'] is True,'saved namespace actually present '+str(p))
 need(set(files)==set(view['files'])|(laterE if p==E else set()),'whole namespace exact file membership '+str(p))
 for rel,q in view['files'].items():need(q['path']==str(p/rel),'exact namespace member path '+rel);verify(q,'full namespace output')
 expected_dirs=view['directories']
 if p==E:
  need(ns['final_E_root_directory_identity_stability_claimed'] is False and set(dirs)==set(expected_dirs)=={'.'},'honest E root before three later appends')
 else:need(dirs==expected_dirs,'complete namespace dir7IDs '+str(p))
 need(syms==view['symlinks']=={},'complete namespace literal symlinks '+str(p))
 counts[str(p)]={'files':len(files),'root_inclusive_directories':len(dirs),'symlinks':len(syms)}
need([(q['files'],q['root_inclusive_directories']) for q in counts.values()]==[(5,4),(11,2),(11,6),(11,1),(123,12),(11,1)],'actual complete current namespace counts')
watch=read(H/'run/build.watchdog.json');failed=read(H/'failed_host_result.json');inner=read(O/'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22/stages.json')['stages']
hc={}
for n in ast.parse((D/'combined_build_host.py').read_text()).body:
 if isinstance(n,ast.Assign):
  for t in n.targets:
   if isinstance(t,ast.Name):
    try:hc[t.id]=ast.literal_eval(n.value)
    except (ValueError,TypeError):pass
command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(F),'run-build','--sha256',hc['DECLARATION_SHA'],'--prep-sha256',hc['PREP_SHA']]
need(watch['command']==command and type(watch['pid']) is int and watch['pid']==21587,'actual original canonical own child PID21587 and full command')
need(type(watch['returncode']) is int and watch['returncode']==-15 and watch['rss_cap_mib']==512 and watch['sampled_peak_rss_mib']==513.375 and watch['elapsed_seconds']==164.2412298329873,'actual own-child RSS failure sampled metrics')
for k in ['elapsed_seconds','sampled_peak_rss_mib','wall_cap_seconds']:finite(watch[k],'actual failed watch '+k)
need(watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')" and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and 0<watch['wall_cap_seconds']<=1800,'actual unchanged genuine RSS gate and cleanup')
need(failed['status']=='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY' and failed['error']==watch['limit_failure'] and len(failed['stage_records'])==1,'honest actual failed outer host')
outer=failed['stage_records'][0]
need(outer['label']=='run/build' and outer['status']=='FAILED' and outer['command']==command and 0<watch['wall_cap_seconds']<=outer['wall_cap_seconds']<=1800,'one genuine failed outer record')
need(len(inner)==2 and [q['label'] for q in inner]==['build/link','metadata/objects'] and [q['command'] for q in inner]==hc['EXPECTED_COMMANDS'][:2] and all(q['status']=='PASS' for q in inner),'only first2 of exact5 original commands actually passed')
for q in inner:
 raw=O/(q['label']+'.log');iw=read(raw.with_suffix('.watchdog.json'))
 need(full(raw)['sha256']==q['log_sha256'],'complete inner log SHA '+q['label'])
 need(iw['command']==q['command'] and type(iw['returncode']) is int and iw['returncode']==0 and iw['limit_failure'] is None and iw['rss_cap_mib']==512 and iw['own_child_only'] is True and iw['liveness_group_cleanup'] is True,'true bounded inner PASS '+q['label'])
 for k in ['elapsed_seconds','sampled_peak_rss_mib','wall_cap_seconds']:finite(iw[k],q['label']+' '+k)
 need(0<=iw['sampled_peak_rss_mib']<512 and 0<=iw['elapsed_seconds']<iw['wall_cap_seconds']<=q['wall_cap_seconds']<=600,'original inner600/512 retained '+q['label'])
for p in (H/'result.json',O/'seal.json',O/'driver_result.json',O/'raw_metadata_receipt.json',O/'audit/result.json',O/'audit/binary_identity.json',T/'terminal_return.json'):
 need(not os.path.lexists(p),'no successful complete build result '+str(p))
need(summary['status']=='ACTUAL_NONZERO_BUILD_NO_RETRY' and summary['actual_terminal_exit_code']==1 and summary['actual_tool_session_closed'] is True,'honest summary failed closed status')
need(summary['observed_partial_inner_stages']==inner and summary['observed_PASS_inner_stage_labels']==['build/link','metadata/objects'] and summary['observed_inner_stage_count']==2 and summary['completed_inner_stage_labels']==[],'partial2PASS distinct from complete-five qualification')
need(summary['observed_outer_watchdog_fields']=={k:watch[k] for k in summary['observed_outer_watchdog_fields']},'summary exact observed outer watch')
formal=read(summary['formal_build_terminal']['path'])
need(formal['schema']=='ROOT_V22_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1' and formal['status']==summary['status'] and formal['actual_tool_result']==tr and formal['returncode']==1 and formal['actual_root_host_launchargs']==root['actual_launch_arguments'],'failure formal receipt exact Root actual binding')
need(formal['actual_tool_terminal_return_observed'] is True and formal['record_written_after_actual_terminal_return'] is True and formal['successful_new_runtime_build_observed'] is False,'formal honest observed failure')
need(formal['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False,'truthful complete merged/outer stream labels')
for src,dst in [(H/'run/build.log',T/'actual_build_child_merged_stdout_stderr.json'),(E/'parent_stdout.log',T/'actual_build_external_host_stdout.json'),(E/'parent_stderr.log',T/'actual_build_external_host_stderr.txt'),(E/'Root_actual_build_tool_terminal_return.json',T/'actual_build_external_Root_tool_terminal.json')]:
 need(full(src)['sha256']==full(dst)['sha256'] and src.read_bytes()==dst.read_bytes(),'full exact original failed stream '+str(dst))
need(pins[str(E/'parent_stdout.log')]['size_bytes']==0 and b'own-child 512 MiB RSS cap reached' in (E/'parent_stderr.log').read_bytes(),'honest empty outer stdout and genuine failure outer stderr')
tailnames=['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']
need(all(k not in formal and k not in summary for k in tailnames) and pins[str(H/'run/build.log')]['size_bytes']==0,'four successful whole-return tails absent (NULL credit only), never forged')
wr=read(E/'Root_actual_failed_build_META_writer_tool_terminal_return.json');wtr=wr['actual_tool_return']
need(wr['closed'] is True and wr['observed_terminal'] is True and type(wtr['exit_code']) is int and wtr['exit_code']==0 and wtr['chunk_id']=='c48a3f' and 'session_id' not in wtr,'true failure-only metadata writer CLOSED EXIT0')
need('--mode failure-only' in wr['actual_arguments']['cmd'] and '--writer-sha256 '+pins[str(D/'write_actual_build_postclose_META.py')]['sha256'] in wr['actual_arguments']['cmd'] and wr['business_or_numeric_execution'] is False and wr['whole_build_INPUT_native_science_qualified'] is False,'actual prefrozen unchanged writer failure-only CLI and scope')
wout=json.loads(wtr['output'])
need(wout['status']==summary['status'] and wout['actual_tool_exit_code']==1 and wout['no_whole_INPUT_native_science_credit'] is True,'real writer actual output no build credit')
for k in ('namespace_manifest','summary'):verify(wout[k],'actual writer whole output pin')
for container,keys,label in [
 (root,['whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','goal_complete'],'Root receipt'),
 (summary,['original_five_build_stages_executed','all_five_build_stages_passed','whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved','mathematical_controls_newly_executed','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete','cleanup_performed','original_host_final_input_revalidation_observed','full_declared_physical_input_finalpass_claimed'],'summary'),
 (formal,['successful_new_runtime_build_observed','whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete','cleanup_performed','original_host_final_input_revalidation_observed','full_declared_physical_input_finalpass_claimed'],'formal')]:
 for k in keys:need(container[k] is False,'no successful scope credit '+label+' '+k)
need(summary['all_original_fixed_inputs_unchanged'] is True and summary['complete_SOURCE_unchanged'] is True and summary['original_fixed_input_entry_count']==155 and summary['full_SOURCE_file_count']==123,'honest saved155 postclose and frozen123 evidence')
need(summary['Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass'] is True and ns['full_declared_physical_input_postclose_pins']==[] and ns['full_declared_physical_input_prelaunch_7ID_claimed'] is False and ns['full_declared_physical_input_finalpass_claimed'] is False,'no failed host finalpass or all physical closure substituted')
caps={'whole_wall_cap_seconds':1800,'inner_stage_wall_cap_seconds':600,'rss_cap_mib':512,'joint_archive_cap_bytes':2*2**30,'history_cap_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
for x in (summary,formal):
 for k,v in caps.items():need(type(x[k]) is int and x[k]==v,'all original cap '+k)
resources=[pre['actual_genuine_history_resources'],outer['resource_before']]+[q[k] for q in inner for k in ('resource_before','resource_after')]
for q in resources:
 need(q['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and q['artifact_budget_bytes']==96*2**30 and q['min_free_bytes']==8*2**30,'original saved dynamic history96/free8')
 need(all(pathlib.Path(p).is_relative_to(ART) and pathlib.Path(p)!=ART for p in q['resource_roots']) and set(q['declared_resource_roots']).issubset(q['resource_roots']),'entire saved dynamic history strict ART roots')
 need(0<=q['artifact_bytes']<=96*2**30 and q['disk_free_bytes']>=8*2**30,'actual saved history/free resource pass')
need(pre['genuine_guard_original_MRO_verified'] is True and pre['complete_Root_extra_scope_ledger_does_not_modify_host_guard'] is True,'original genuine prelaunch MRO/guard unchanged')
for k in ['actual_Root_terminal','formal_build_terminal','namespace_manifest','actual_failed_host_result','actual_outer_watchdog','actual_partial_inner_stage_records']:verify(summary[k],'summary complete observed pin')
for k in ['actual_metadata_writer_source','actual_Root_terminal','complete_SOURCE_freeze','original_prelaunch_check','exact_formal_terminal']:verify(ns[k],'namespace provenance exact fullpin')
# Reuse the already independently sealed Source661 inverse qualification, with installed source bytes bound above.
sp=pathlib.Path('/private/tmp/axmat_v22_actual_full_build_bound_independent_SOURCE_review_20261010_tcjjkas9')
need(full(sp/'REVIEW.json')['sha256']=='5a664db961348c1edc6de608cccfef2a77b5fb1de935245ea63577a351e1bb5b','reuse exact completeSource661 report')
need(full(sp/'MANIFEST.json')['sha256']=='7c545ca1597568ada27f23cf9a126dc2cd9a34086a5c1e33d64757a9f14ca7a1','reuse sealedSource661 full manifest')
# Original writer's byte ledger conservatively adds its own Source after ROOTS already contain that Source.
base_bytes=sum(q['size_bytes'] for p in (H,S,O,T,D,E) for q in walk(p)[0].values())+pins[str(F)]['size_bytes']+pins[str(D/'write_actual_build_postclose_META.py')]['size_bytes']
historical=base_bytes-pins[str(E/'Root_actual_failed_build_META_writer_tool_terminal_return.json')]['size_bytes']
need(historical==summary['joint_archive_bytes_after_summary']==157670354 and summary['joint_archive_bytes_before_summary']+pins[str(E/'Root_actual_failed_complete_combined_build_summary.json')]['size_bytes']==historical,'independent exact whole original writer ledger (before later true writer receipt)')
need(base_bytes<2*2**30,'current full H/S/O/T/D/E+factory+conservative writer Source original2GiB')
# Full extra Root reserve scopes are bounded explicit Source/META namespaces, not a history scan.
extra_counts={};extra_bytes=0
for p in map(pathlib.Path,pre['complete_joint_scope_roots']):
 files,dirs,syms=walk(p);need(syms=={},'no omitted extra explicit Root ledger symlink '+str(p));extra_counts[str(p)]={'files':len(files),'root_inclusive_directories':len(dirs)};extra_bytes+=sum(q['size_bytes'] for q in files.values())
need(extra_bytes+pins[str(F)]['size_bytes']<2*2**30,'actual nine explicit Root reserve namespaces also below original2GiB')
initialpins=dict(pins)
for p,q in initialpins.items():need(full(p)==q,'final whole EOF SHA7ID unchanged '+p)
report=dict(schema='INDEPENDENT_V22_ACTUAL_FAILED_COMPLETE_BUILD_SAVED_SOURCE_META_REVIEW_V1',status='PASS_ACTUAL_FAILED_BUILD_EVIDENCE_ONLY',source_only_reviewer=True,stdlib_only=True,all_checks_typed_true=True,checks=checks,check_count=len(checks),blockers=[],actual_Root_failed_build_terminal_pin=pins[str(E/'Root_actual_build_tool_terminal_return.json')],actual_failure_only_META_writer_terminal_pin=pins[str(E/'Root_actual_failed_build_META_writer_tool_terminal_return.json')],actual_failed_build_summary_pin=pins[str(E/'Root_actual_failed_complete_combined_build_summary.json')],actual_failed_build_complete_namespace_pin=pins[str(E/'Root_actual_failed_build_namespace_manifest.json')],actual_frozen_host_Source_pin=pins[str(D/'combined_build_host.py')],actual_frozen_postclose_writer_Source_pin=pins[str(D/'write_actual_build_postclose_META.py')],actual_Root_exit_code=1,actual_Root_terminal_chunk='65203e',actual_Root_original_session=70899,actual_failure_only_writer_chunk='c48a3f',actual_failure_only_writer_exit_code=0,actual_outer_own_child={'pid':watch['pid'],'returncode':watch['returncode'],'elapsed_seconds':watch['elapsed_seconds'],'sampled_peak_rss_mib':watch['sampled_peak_rss_mib'],'rss_cap_mib':512,'cleanup':True},actual_partial_inner_PASS_labels=['build/link','metadata/objects'],actual_complete_five_stages_PASS=False,actual_original_input_entries=155,all155_original_input_pins_unchanged=True,frozen_SOURCE_file_count=123,frozen_SOURCE_root_inclusive_directory_count=12,namespace_counts=counts,complete_extra_Root_reserve_namespace_counts=extra_counts,historical_joint_bytes_after_summary=historical,current_writer_scope_joint_bytes=base_bytes,current_extra_Root_nine_namespace_bytes_plus_factory=extra_bytes+pins[str(F)]['size_bytes'],four_success_tail_fields_observed_absent=True,four_success_tail_qualification={k:None for k in tailnames},honest_failed_host_finalpass_unreached=True,all_complete_saved_Source_META_file_pins=list(pins.values()),reviewer_imported_or_called_project_helper_or_guard_API=False,reviewer_ran_business_or_numeric=False,numeric_payload_decoded=False,whole_combined_build_qualified=False,whole_combined_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,goal_complete=False,cleanup_performed=False)
(R/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(R/'REPORT.txt').write_text('PASS of actual saved FAILURE evidence only; V22 complete build failed the unchanged genuine512MiB own-child gate.\nRoot197727/session70899 ->65203e actual closed strict EXIT1; genuine child PID21587 return-15,164.2412298329873s/513.375MiB, own-child cleanup true. Only build/link and metadata/objects PASS(2/5); remaining three and all four final tail credits absent.\nPre-frozen complete Source writer d246 executed failure-only c48a3f actual closed EXIT0. Complete155 ordered original input pins full EOF unchanged; D123files/12 root-inclusive dirs freeze exact.\nAll H/S/O/T/D/E complete saved files/dirs and honest later E append shape verified. Child merged stream and actual outer stderr retained separately; no independent child stderr claimed. Original budgets/modes preserved.\nWriter full joint ledger157670354B after summary is verified; current ledger separately includes later genuine writer receipt. Root extra nine namespace reserve checked separately, without altering original guard.\nNo successful seal/driver/audit/terminal, no whole INPUT/native/AAA/ABA/physical balance qualification. Failed host final revalidation not reached; Root postclose155 pin check is not substituted for it. No reviewer API/helper/guard/business/numeric execution.\n')
print(json.dumps(dict(status=report['status'],check_count=len(checks),complete_saved_file_count=len(pins),Root_actual_failed_exit_code=1,metadata_writer_actual_exit_code=0,ordered_inputs=155,frozen_SOURCE_files=123,frozen_ROOT_inclusive_dirs=12,historical_joint_bytes=historical,current_joint_bytes=base_bytes,review=str(R/'REVIEW.json')),allow_nan=False))


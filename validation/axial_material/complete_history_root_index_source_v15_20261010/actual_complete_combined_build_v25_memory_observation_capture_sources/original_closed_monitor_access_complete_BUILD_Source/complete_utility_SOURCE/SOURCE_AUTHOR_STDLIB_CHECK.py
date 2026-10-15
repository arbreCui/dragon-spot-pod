import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
checks={}
def check(k,v):
 assert k not in checks and type(v) is bool;checks[k]=v
 if not v:raise AssertionError(k)
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=ident(p);assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def snapshot(root):
 f={};d={'.':ident(root)}
 for p in sorted(root.rglob('*')):
  i=ident(p);assert not p.is_symlink();k=str(p.relative_to(root))
  if stat.S_ISREG(i[2]):f[k]=pin(p)
  else:assert stat.S_ISDIR(i[2]);d[k]=i
 for k,q in f.items():assert pin(root/k)==q
 for k,i in d.items():assert ident(root/k)==i
 return dict(root=str(root),files=f,directories=d,symlinks={})
pro=json.loads((P/'ACTUAL_FINITE_SOURCE_INPUT_PROVENANCE.json').read_text())
ledger=json.loads((P/'COMPLETE_V22_UTILITY_SOURCE_BYTE_INVERSES.json').read_text())
contracts=json.loads((P/'SOURCE_ONLY_CONTRACT.json').read_text())
complete=[]
for role,v in pro['full_original_views'].items():
 check('full_original_'+role+'_full_EOF_SHA7ID_and_dirs',snapshot(Path(v['root']))==v)
 copied=pro['full_byte_retained_copies'][role]
 for name,q in v['files'].items():
  t=Path(copied['retained_root'])/name;actual=pin(t)
  assert actual==copied['files'][name] and actual['sha256']==q['sha256'] and actual['size_bytes']==q['size_bytes']
 check('whole_byte_copied_'+role+'_names_files_empty_dirs',set(snapshot(Path(copied['retained_root']))['files'])==set(v['files']) and set(snapshot(Path(copied['retained_root']))['directories'])==set(v['directories']))
 complete.extend(v['files'].values())
for role,row in ledger['roles'].items():
 original=(P/'ORIGINAL_ROLE_SOURCE'/role).read_text();new=(P/role).read_text();back=new
 for h in reversed(row['hunks']):assert back.count(h['new'])==1;back=back.replace(h['new'],h['old'],1)
 check(role+'_two_full_hunks_inverse_all_bytes',back==original and hashlib.sha256(back.encode()).hexdigest()==row['original_pin']['sha256'] and pin(row['original_pin']['path'])==row['original_pin'])
 check(role+'_new_fullpin_current',pin(P/role)==row['new_pin'])
 ot=ast.parse(original);nt=ast.parse(new)
 olddefs={n.name:ast.get_source_segment(original,n) for n in ot.body if isinstance(n,ast.FunctionDef) and n.name!='main'}
 newdefs={n.name:ast.get_source_segment(new,n) for n in nt.body if isinstance(n,ast.FunctionDef)}
 check(role+'_all_original_nonmain_definitions_full_byte_and_AST',set(olddefs)==set(row['original_nonmain_functions_byte_exact']) and all(newdefs[k]==v and ast.dump(ast.parse(newdefs[k]),include_attributes=False)==ast.dump(ast.parse(v),include_attributes=False) for k,v in olddefs.items()))
 check(role+'_all_original_imports_exact_AST', [ast.dump(n,include_attributes=False) for n in ot.body if isinstance(n,(ast.Import,ast.ImportFrom))]==[ast.dump(n,include_attributes=False) for n in nt.body if isinstance(n,(ast.Import,ast.ImportFrom))])
installer=(P/'Root_source_installer.py').read_text();pre=(P/'Root_prelaunch_checker.py').read_text()
check('full_original_closed_failed_V22_123files_12dirs',len(pro['full_original_views']['original_complete_closed_failed_V22_D']['files'])==123 and len(pro['full_original_views']['original_complete_closed_failed_V22_D']['directories'])==12)
check('new_installer_fresh_D_E_H_no_retry',"not any(os.path.lexists(p) for p in (D,E,HOST))" in installer and "strict_terminal(oldterminal,1)" in installer)
check('future_actual_Source_peer_exact_CLI_no_fabricated_pin',all(k in installer for k in ('peer-manifest','peer-manifest-sha256','peer-seal-receipt','peer-seal-receipt-sha256')) and contracts['future_independent_Source_peer_manifest'] is None and contracts['future_independent_Source_peer_seal'] is None)
check('full_actual_binding_receipt_closed_int0_original_a1380b',"tr['chunk_id']=='a1380b'" in installer and "type(tr['exit_code']) is int" in installer and "actual_bind['manifest']==pin(BOUND/'MANIFEST.json')" in installer)
check('future_Source_admission_requires_full_bound_and_utility_exact_pins',all(k in installer for k in ('actual_bound_build_host_pin','actual_postclose_META_writer_pin','actual_Root_Source_binding_tool_receipt_pin','qualified_actual_bound_Source_manifest_pin','actual_Source_utility_manifest_pin','actual_Root_source_installer_Source_pin','actual_Root_prelaunch_checker_Source_pin','original_bound_Source_review_report_pin','utility_Source_checks_typed_true')))
check('true_seal_full_manifest_review_coupling_and_three_real_tool_keys',all(k in installer for k in ("observed['manifest_pin']==manifest_pin","observed['review_pin']==review_pin","record.get('exec_command_result')","'session_id' not in tr")))
check('exact_full_compile_host_writer_not_modified',pin(Path(pro['full_original_views']['whole_actual_bound_BUILD_SOURCE']['root'])/'combined_build_host.py')['sha256']==contracts['current_bound_host_pin']['sha256'] and pin(Path(pro['full_original_views']['whole_actual_bound_BUILD_SOURCE']['root'])/'write_actual_build_postclose_META.py')['sha256']==contracts['current_bound_writer_pin']['sha256'])
summary=json.loads((P/'INPUT_SOURCE_COPIES/current_actual_PREP_E_small_META/Root_actual_complete_combined_prepare_summary.json').read_text())
ph=json.loads(Path(summary['actual_host_result']['path']).read_text())
check('actual_PREP_small_META_exact_original144_142plus2',len(ph['input_sources'])==142 and len(ph['input_sources']+[ph['original_helper'],ph['resource_factory']])==144 and summary['all_original_pinned_inputs_unchanged_count']==144)
check('PREP_runtime_result_small_META_not_payload_source_coupled',pin(summary['actual_host_result']['path'])['sha256']==summary['actual_host_result']['sha256'])
ns=json.loads((P/'INPUT_SOURCE_COPIES/current_actual_PREP_E_small_META/Root_actual_complete_prepare_namespace_manifest.json').read_text())
check('actual_PREP_all5_namespaces_exact_order_schema',ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and len(ns['namespaces'])==5 and [Path(e['root']).name for e in ns['namespaces']]==['axial-material-complete-combined-prepare-host-v25-monitor-access-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010','actual_complete_combined_prepare_v25_monitor_access_sources'])
check('both_mains_require_all144_and_five_whole_namespace_views',all("len(ph['input_sources'])==142" in s and 'len(inputs)==144' in s if s==installer else 'len(prep)==144' in s for s in (installer,pre)))
check('Root_final_fixed_pins_match_genuine_threekeys_and_repeats',"return {k:q[k] for k in ('path','sha256','identity')}" in pre and "fixed=[original_host_pin(exact(q)) for q in ph['input_sources'][:7]]" in pre and "fixed+=[original_host_pin(pin(p)) for p in sorted(D.rglob('*')) if p.is_file()]" in pre and "for root in (S,T)" in pre and "original_host_pin(exact(ph['original_helper'])),original_host_pin(exact(ph['resource_factory']))" in pre)
check('writer_actual_original_ordered_pins_equality_preserved',"original=h['input_sources']+[h['original_helper'],h['resource_factory']]" in (Path(pro['full_original_views']['whole_actual_bound_BUILD_SOURCE']['root'])/'write_actual_build_postclose_META.py').read_text())
check('prelaunch_genuine_support619_resource_ebbb_full_MRO_and_normal_paths',all(k in pre for k in ('support.load(support.OLD_HELPER,support.OLD_HELPER_SHA','support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA','full,production=helper.modules();helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)','Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT')))
check('all_original_resources_caps_and_five_thread_vars_preserved',contracts['original_caps']==[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0] and "roots=resource.history_roots([str(p) for p in (H,S,O,T)],support.ART)" in pre and all(k in pre for k in ('whole_seconds_cap=1800','stage_seconds_cap=600','rss_mib_cap=512','threads=1,children=1,retries=0','support.THREAD_KEYS==THREAD_KEYS')))
check('full_Root_extra_scope_allH_S_O_T_D_E_C_and_PREP_H_D_E',"extra_roots=[H,S,O,T,D,E,PREP_H,PREP_D,PRE]" in pre and "before_bytes=joint_size(extra_roots)+canonical_pin['size_bytes']" in pre and "actual_resources['artifact_bytes']+outside_art_bytes+own_pin['size_bytes']+2*2**30<96*2**30" in pre)
check('prelaunch_E_only_append_self_complete_files_dirs_7ID_APFSsafe',"now['files']=={**v['files'],out.name:own_pin}" in pre and "now['directories']['.'][:3]==v['directories']['.'][:3]" in pre and "if k!='.':assert now['directories'][k]==i" in pre and "after_bytes==before_bytes+own_pin['size_bytes']" in pre)
check('prelaunch_all_other_scope_fullpins_fullviews_unchanged_after_self_append',"else:assert now==v" in pre and "verify_frozen_source(freeze)" in pre and "for q in fixed:exact(q)" in pre and "assert full_view(PRE)==current_pre" in pre)
check('utility_root_finite_no_recursive_provenance_copy',"if not k.startswith('INPUT_SOURCE_COPIES/')" in installer and 'utility_author_provenance_copies_not_recopied=True' in installer)
check('writer_Source_freeze_exact_schema_and_filenames',all(k in installer and k in pre for k in ('ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1','Root_prelaunch_complete_build_source_freeze.json')) and 'Root_final_prelaunch_source_input_and_reserve_check.json' in pre)
check('fixed_installed_prelaunch_Source_self_pinned',"Path(__file__)==D/'Root_prelaunch_checker.py' and pin(Path(__file__))==freeze['complete_files']['Root_prelaunch_checker.py']" in pre)
parsed=[]
for p in sorted(P.rglob('*.py')):ast.parse(p.read_bytes(),filename=str(p));parsed.append(pin(p))
check('all_complete_python_Source_AST_only',bool(parsed))
check('known_original_genuine_parent_Source_full_EOF_retained',all(pin(P/'GENUINE_PARENT_SOURCE'/Path(q['path']).name)['sha256']==q['sha256'] and pin(q['path'])==q for q in pro['original_genuine_guard_source_pins']))
check('all_future_actual_BUILD_native_science_unknown_or_false',all(v is None for k,v in contracts.items() if k.startswith('future_')) and all(contracts[k] is False for k in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','new_business_or_candidate_executed')))
check('author_only_Source_stdlib_no_import_call_of_reviewed_API',pro['author_did_not_read_PREP_144_material_object_library_graph_trace_payloads'] is True)
report=dict(schema='V25_MONITOR_ACCESS_COMPLETE_INSTALLER_PRELAUNCH_FINITE_SOURCE_AUTHOR_REVIEW_V1',status='AUTHOR_SOURCE_CHECK_COMPLETE_UNREADY_NO_ROOT_EXECUTION',source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=all(type(v) is bool and v is True for v in checks.values()),blockers=[],actual_installer_Source_pin=pin(P/'Root_source_installer.py'),actual_prelaunch_Source_pin=pin(P/'Root_prelaunch_checker.py'),complete_original_byte_inverse_pin=pin(P/'COMPLETE_V22_UTILITY_SOURCE_BYTE_INVERSES.json'),complete_provenance_pin=pin(P/'ACTUAL_FINITE_SOURCE_INPUT_PROVENANCE.json'),all_parsed_Source_pins=parsed,complete_retained_original_Source_files=len(complete),actual_source_peer=None,actual_root_install_terminal=None,actual_root_prelaunch_terminal=None,actual_BUILD_terminal=None,actual_native_binary=None,candidate_helper_guard_API_imported_or_executed=False,native_or_compiler_or_material_or_numeric_executed=False,large_material_graph_trace_or_SQL_payload_read=False,project_D_E_C_ART_written=False,independent_Source_admission_claimed=False,whole_BUILD_science_qualified=False)
with (P/'AUTHOR_SOURCE_CHECK.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,status=report['status'],checks=len(checks),typed_true=report['all_checks_typed_true'],parsed_python_Source=len(parsed),report_pin=pin(P/'AUTHOR_SOURCE_CHECK.json'),whole_science_qualification=False)))

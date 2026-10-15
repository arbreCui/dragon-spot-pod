from pathlib import Path
import ast, hashlib, json, os, stat, tempfile

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
PREP = BASE/'actual_complete_combined_prepare_v25_monitor_access_sources'
BUILD = BASE/'actual_complete_combined_build_v25_monitor_access_sources'
CANONICAL = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py')
P = Path(tempfile.mkdtemp(prefix='axmat_V25_poststage_temporaries_complete_UNREADY_Source_', dir='/private/tmp'))
Q_SHA = 'c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
ROLE_PARENTS = {
 'canonical':CANONICAL,
 'prepare_host':PREP/'combined_prepare_host.py',
 'prepare_writer':PREP/'write_actual_prepare_terminal.py',
 'build_host':BUILD/'combined_build_host.py',
 'build_writer':BUILD/'write_actual_build_postclose_META.py',
 'prepare_binder':PREP/'sealed_complete_PREP_UNREADY_Source/bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py',
 'build_binder':BUILD/'complete_monitor_access_BUILD_mother_SOURCE/bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py',
}
ROLE_FILES = {
 'canonical':'canonical.V25.UNREADY.full.py',
 'prepare_host':'host_and_postclose_templates/prepare_host.V25.UNREADY.full.py',
 'prepare_writer':'host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py',
 'build_host':'host_and_postclose_templates/build_host.V25.UNREADY.full.py',
 'build_writer':'host_and_postclose_templates/build_writer.V25.UNREADY.full.py',
 'prepare_binder':'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py',
 'build_binder':'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py',
}
BUSINESS = ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
READ_PINS = {}
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1 and not p.is_symlink()
 raw=p.read_bytes();b=p.lstat();assert identity(a)==identity(b) and len(raw)==a.st_size
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(b))
def read(p):
 before=pin(p);raw=Path(p).read_bytes();assert pin(p)==before
 READ_PINS[str(p)]=before;return raw
def write(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw)
def dump(p,o):write(p,(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
def defs(text):return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assignments(text):return {n.targets[0].id:n for n in ast.parse(text).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def replace(text,rows,old,new,label):
 count=text.count(old);assert count>0 and old!=new,(label,count)
 rows.append(dict(label=label,old=old,new=new,count=count));return text.replace(old,new)
def assign(text,rows,name,value,label=None,tight=False):
 n=assignments(text)[name];old=ast.get_source_segment(text,n);new=name+('=' if tight else ' = ')+repr(value)
 if old==new:return text
 return replace(text,rows,old,new,label or 'unknown_'+name)
def inverse(text,rows):
 for r in reversed(rows):
  assert text.count(r['new'])==r['count'],r['label'];text=text.replace(r['new'],r['old'])
 return text

old_basename='prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py'
new_basename='prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
namespace_replacements = [(old_basename,new_basename),('v25-monitor-access-20261010','v25-poststage-temporaries-20261010'),('v25_monitor_access_sources','v25_poststage_temporaries_sources'),('v25_monitor_access_receipts','v25_poststage_temporaries_receipts')]
rows={role:[] for role in ROLE_PARENTS};parents={};texts={}
for role,path in ROLE_PARENTS.items():
 raw=read(path);text=raw.decode('utf-8');parents[role]=text
 write(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'),raw)
 for old,new in namespace_replacements:
  if old in text:text=replace(text,rows[role],old,new,'fresh_namespace_'+old)
 texts[role]=text
assert hashlib.sha256(parents['canonical'].encode()).hexdigest()=='643d1b5fcfada4c7ec13f8c5d4c01fb6a77529f51a109d73fac214952f849ef2'

role='canonical';text=texts[role]
anchor="            corrected_runtime=pin(OUT/'runtime/Dragon'),fresh_cold_AAA_required=True)"
text=replace(text,rows[role],anchor,anchor+'\n        del stages,audit,commands;gc.collect()','three_private_last_use_temporaries_only')
old_doc=ast.get_source_segment(text,ast.parse(text).body[0])
text=replace(text,rows[role],old_doc,repr('UNREADY complete V25 poststage-temporaries Source. Only the run_build last-use stages/audit/commands locals are released after all five complete stage/audit/watchdog checks. All original PREP, five-stage build, whole INPUT, physical and resource gates remain. Root must rebind the existing actual c6 helper-only Q/proofs and this new canonical Source, independently review/install, then freshly execute complete PREP and BUILD in disjoint namespaces. No new business or science success is provided; all six business pins remain None. RSS reduction is not predicted.'),'truthful_UNREADY_doc')
text=assign(text,rows[role],'DRAFT_STATUS','UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND')
for name in ('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA','FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN'):
 text=assign(text,rows[role],name,None)
for name in BUSINESS:assert assignments(text)[name].value.value is None
texts[role]=text
for role in ('prepare_host','prepare_writer','build_host','build_writer'):
 text=texts[role]
 for name in assignments(text):
  if name.startswith('FUTURE_V25_'):text=assign(text,rows[role],name,None,tight=True)
 ready={'prepare_host':'READY_V25_ACTUAL_Q_AND_TARGET_SOURCE_BOUND','prepare_writer':'READY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND','build_host':'READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND','build_writer':'READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND'}[role]
 unready=ready.replace('READY_','UNREADY_',1).replace('_BOUND','_UNBOUND')
 text=assign(text,rows[role],'SOURCE_BINDING_STATUS',unready,tight=True);texts[role]=text

# The original PREP binder has one harmless READY module-doc rewrite anchor.
# Retarget that anchor to this derivative's complete, truthful UNREADY doc, so
# its existing full-Q/proof reads and original body-preserving bind can operate.
role='prepare_binder';text=texts[role]
docline="repr('READY Source binding only for V25 complete sender/root-index flow. The new actual V25 full pure/fresh helper metadata Q and both Root terminal/saved peer/install proofs are read before project load. All original complete PREP, five-stage build, whole INPUT, physical and resource gates remain required. No new PREP/build/INPUT/native/science success is supplied by this binding; all six business pins remain None.')"
newdoc="repr('READY Source binding only for V25 poststage-temporaries complete sender/root-index flow. Existing actual c6 full pure/fresh helper metadata Q and all original Q terminal/saved peer/install proofs were re-read. All original complete PREP, five-stage build, whole INPUT, physical and resource gates remain required. This Source binding supplies no new PREP/build/INPUT/native/science success; all six business pins remain None. Private last-use local release does not predict RSS qualification.')"
text=replace(text,rows[role],docline,newdoc,'truthful_READY_binding_doc_only')
text=replace(text,rows[role],"'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'",repr(new_basename),'new_installed_canonical_output_basename')
texts[role]=text

checks=[]
def check(label,passed):
 assert type(passed) is bool and passed,label
 assert label not in {x['check'] for x in checks}
 checks.append(dict(check=label,passed=True))
for role,text in texts.items():
 restored=inverse(text,rows[role]);check(role+'_complete_byte_inverse',restored==parents[role])
 check(role+'_complete_AST_inverse',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parents[role]),include_attributes=False))
 check(role+'_all_top_definition_names_retained',list(defs(text))==list(defs(parents[role])))
 ast.parse(text);write(P/ROLE_FILES[role],text.encode())
 check(role+'_full_EOF_candidate_and_parent_saved',pin(P/ROLE_FILES[role])['sha256']==hashlib.sha256(text.encode()).hexdigest())

# Normalize only the explicit namespace literals for definition comparison.
for role in ('canonical','prepare_host','prepare_writer','build_host','build_writer'):
 normalized=texts[role]
 for old,new in reversed(namespace_replacements):normalized=normalized.replace(new,old)
 if role=='canonical':normalized=normalized.replace('\n        del stages,audit,commands;gc.collect()','')
 check(role+'_all_function_bodies_original_except_declared_namespace_and_last_use',defs(normalized)==defs(parents[role]))
run=next(n for n in ast.parse(texts['canonical']).body if isinstance(n,ast.FunctionDef)and n.name=='run_build')
oldrun=next(n for n in ast.parse(parents['canonical']).body if isinstance(n,ast.FunctionDef)and n.name=='run_build')
deletes=[n for n in ast.walk(run) if isinstance(n,ast.Delete)]
check('exactly_three_last_use_local_names',len(deletes)==1 and [n.id for n in deletes[0].targets]==['stages','audit','commands'])
check('new_release_after_full_watchdog_result_update_before_except_finally',deletes[0].lineno>next(n.lineno for n in ast.walk(run)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='result'and n.func.attr=='update'))
check('existing_gc_import_only',any(isinstance(n,ast.Import)and any(a.name=='gc' for a in n.names)for n in ast.parse(parents['canonical']).body))
for name in BUSINESS:check('canonical_'+name+'_None',isinstance(assignments(texts['canonical'])[name].value,ast.Constant)and assignments(texts['canonical'])[name].value.value is None)
for role in ('prepare_host','prepare_writer','build_host','build_writer'):
 slots={k:None for k,n in assignments(texts[role]).items()if k.startswith('FUTURE_V25_')}
 check(role+'_all_future_bindings_unknown',bool(slots)and all(isinstance(assignments(texts[role])[k].value,ast.Constant)and assignments(texts[role])[k].value.value is None for k in slots))
 check(role+'_first_main_guard_UNREADY',isinstance(next(n for n in ast.parse(texts[role]).body if isinstance(n,ast.FunctionDef)and n.name=='main').body[0],ast.If))
def statement_value(text,key):
 return next(n.value for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==key for target in n.targets for x in ast.walk(target)))
check('physical_and_resource_globals_unchanged',all(ast.dump(statement_value(texts['canonical'],k),include_attributes=False)==ast.dump(statement_value(parents['canonical'],k),include_attributes=False) for k in ('TOTAL_WALL','RESERVE','HISTORY_POLICY','THREAD_KEYS','INPUT_HELPERS','BODY_BINDING','PREFIX','FAMILY')))
check('actual_helper_SHA_3b_preserved','3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092' in texts['canonical'])
check('canonical_private_snapshot_consumers_preserved',texts['canonical'].count('snapshot(_consume=True)')==parents['canonical'].count('snapshot(_consume=True)')==3)

failure_paths={
 'Root_actual_failed_complete_combined_build_summary.json':BASE/'actual_complete_combined_build_v25_monitor_access_receipts/Root_actual_failed_complete_combined_build_summary.json',
 'Root_actual_build_tool_terminal_return.json':BASE/'actual_complete_combined_build_v25_monitor_access_receipts/Root_actual_build_tool_terminal_return.json',
 'Root_actual_build_metadata_writer_tool_terminal_return.json':BASE/'actual_complete_combined_build_v25_monitor_access_receipts/Root_actual_build_metadata_writer_tool_terminal_return.json',
 'build.watchdog.json':Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v25-monitor-access-20261010/run/build.watchdog.json'),
 'original_inner_five_stages.json':Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010/SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25/stages.json'),
 'original_audit_result.json':Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010/audit/result.json'),
}
failure={}
for name,path in failure_paths.items():
 raw=read(path);json.loads(raw);write(P/'ACTUAL_PRIOR_FAILED_BUILD_META'/name,raw);failure[name]=READ_PINS[str(path)]
summary=json.loads((P/'ACTUAL_PRIOR_FAILED_BUILD_META/Root_actual_failed_complete_combined_build_summary.json').read_bytes())
watch=json.loads((P/'ACTUAL_PRIOR_FAILED_BUILD_META/build.watchdog.json').read_bytes())
stages=json.loads((P/'ACTUAL_PRIOR_FAILED_BUILD_META/original_inner_five_stages.json').read_bytes())['stages']
check('prior_business_failure_kept_nonzero',summary['actual_terminal_exit_code']==1 and watch['returncode']==-15 and watch['sampled_peak_rss_mib']==512.578125)
check('actual_all_original_five_stages_PASS',len(stages)==5 and all(s['status']=='PASS'for s in stages))
check('actual_audit_PASS_not_misclassified',stages[-1]['label']=='audit/audit'and stages[-1]['elapsed_seconds']==48.33631362498272)
prior_truth=dict(actual_failure_pins=failure,actual_five_inner_stages_all_PASS=True,actual_audit_seconds=48.33631362498272,actual_whole_seconds=316.0239865001058,actual_whole_peak_rss_mib=512.578125,actual_whole_EXIT1=True,precise_peak_line_not_observed=True,driver_result_and_seal_not_generated=True,summary_original_formal_stage_flags=list((k,summary[k]) for k in ('original_five_build_stages_executed','all_five_build_stages_passed','completed_inner_stage_labels')),summary_observed_PASS_inner_stage_labels=summary['observed_PASS_inner_stage_labels'],formal_flags_not_used_to_deny_observed_inner_PASS=True,current_Q_already_actual_SHA=Q_SHA,new_PREP_or_BUILD_success=False,new_source_release_does_not_predict_RSS=True)
dump(P/'ACTUAL_PRIOR_FAILED_BUILD_META/FULL_ORIGINAL_FAILURE_SCOPE_AND_FIELD_DIFFERENCE.json',prior_truth)

# Keep only the six complete installation/prelaunch interface Sources; no
# transitive history or old Source/ART trees are copied into this small package.
utilities={'prepare_installer':PREP/'Root_complete_SOURCE_install_writer.py','prepare_prelaunch':PREP/'Root_complete_PREP_prelaunch.py','prepare_E_snapshot':PREP/'Root_complete_PREP_E_snapshot.py','prepare_namespace_author':PREP/'sealed_namespace_only_complete_PREP_Source/spot_derive_v25_monitor_access_complete_PREP_Source_ROOT.py','build_installer':BUILD/'Root_source_installer.py','build_prelaunch':BUILD/'Root_prelaunch_checker.py'}
utilitypins={}
for role,path in utilities.items():
 raw=read(path);ast.parse(raw);write(P/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(role+'.full.py'),raw);utilitypins[role]=READ_PINS[str(path)]

proof=dict(schema='COMPLETE_V25_POSTSTAGE_TEMPORARIES_SOURCE_INVERSE_V1',source_only=True,exact_finite_transforms=rows,parent_Source_pins={role:READ_PINS[str(path)]for role,path in ROLE_PARENTS.items()},role_filenames=ROLE_FILES,all_original_full_Source_preserved=True,canonical_business_change='Only del stages,audit,commands;gc.collect() after complete successful result.update; no field or record removed',all_physical_body_or_caps_changed=False,new_business_pins_unknown=True,known_current_helper_Q_SHA=Q_SHA,all_original_current_helper_Source_proofs_revalidated_by_Root_binders=True)
dump(P/'COMPLETE_SOURCE_INVERSES.json',proof)
namespaces=dict(canonical=str(Path('/Users/wen/spot/validation/axial_material')/new_basename),prepare_D=str(BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'),prepare_E=str(BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'),build_D=str(BASE/'actual_complete_combined_build_v25_poststage_temporaries_sources'),build_E=str(BASE/'actual_complete_combined_build_v25_poststage_temporaries_receipts'),prepare_H='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010',build_H='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v25-poststage-temporaries-20261010',S='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010',O='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010',T='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010')
for key,path in namespaces.items():check('new_'+key+'_namespace_absent_at_author_check',not os.path.lexists(path))
dump(P/'FUTURE_ROOT_BINDING_AND_NAMESPACE_CONTRACT.UNREADY.json',dict(source_only=True,status='UNREADY_ALL_NEW_BUSINESS_RESULTS_UNKNOWN',namespaces=namespaces,known_actual_helper_Q=dict(path=str(BASE/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'),sha256=Q_SHA,schema='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25',status='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25'),new_PREP_BUILD_result_pins={key:None for key in ('declaration','PREP_terminal','graph','trace','PREP_summary','BUILD_seal','BUILD_terminal','runtime','host_final_input_PASS')},new_actual_Source_binding_install_freeze_and_independent_peers={key:None for key in ('author_Source_peer','Root_PREP_binding','bound_PREP_Source_peer','PREP_install_and_freeze','PREP_saved_META_peer','Root_BUILD_binding','bound_BUILD_Source_peer','BUILD_install_and_freeze','BUILD_saved_META_peer')},original_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HSOTDE_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),original_install_interface_Source_pins=utilitypins,all_no_science_or_whole_INPUT_qualification=True))
steps='''Source-only author delivery; no candidate/guard/API/material execution.
1. Independent Source peer must review this exact manifest, all seven full roles and complete finite inverses. No self-author report is an independent admission.
2. Root truly runs the PREP Source binder in this package, only stdlib Source/META, with the existing c6 Q and the same actual Q writer terminal / saved48 report / saved48 retention full pins. Its CLI remains original: actual_Q_path actual_Q_sha256 fresh_TMP_output --actual-new-Q-writer-terminal PATH --actual-new-Q-writer-terminal-sha256 SHA --actual-Q-saved-peer PATH --actual-Q-saved-peer-sha256 SHA --actual-Q-saved-peer-retention PATH --actual-Q-saved-peer-retention-sha256 SHA. New bound Source needs independent byte/AST review.
3. Root prepares finite new installer/prelaunch/complete-E-snapshot Source from the complete ORIGINAL_ROOT_INSTALL_INTERFACES references. Retarget current canonical and all PREP/BUILD D/E/H/S/O/T literals to FUTURE_ROOT_BINDING_AND_NAMESPACE_CONTRACT.UNREADY.json; replace old namespace Source/peer/bound-manifest pins with exact new author/peer/bound pins, never old business success. Existing interface Sources are originals, not ready new installers. No new deployment utility is executed or falsely claimed complete here.
4. After independent Source admission, Root installs a new canonical at the fixed new path, complete new PREP D Source with original owned files/typed owners and actual freeze, and original prelaunch checks. All old namespaces stay frozen. Root requires the original monitor access permissions (/bin/ps); no guard/MRO/resource cap edit.
5. Root first genuinely executes the complete fresh PREP exactly once. Capture actual Root terminal with typed integer exit_code, observed terminal and closed/no-repoll truth, complete original streams/H/S/O/T/D/E. Only actual EXIT0 permits original prepare_writer and independent saved-PREP META review. New output pins remain None until this event.
6. Root then runs this package's complete BUILD Source binder --saved-prep-peer-report PATH --saved-prep-peer-report-sha256 SHA --actual-Q-sha256 c6... --actual-canonical-sha256 NEW --destination freshTMP and all six original new-Q proof CLI arguments from step2. It must read only the new PREP E/current canonical and actual independent new PREP outputs; old18a/fff/533/847/919 pins are not reused.
7. Independent bound BUILD Source review; Root installs/freezes a complete new BUILD D with actual PREP receipts/peer/source provenance and genuinely prelaunches. Then only Root executes the original complete five-stage BUILD with original tail/input checks, keeping 512/1800/600/2GiB/96GiB/8GiB/1/1/0. Preserve both failure and success evidence. Terminal chronology and E append semantics follow original full host/writer; do not append into frozen D, and never re-poll a closed session.
8. Only actual complete saved-result independent verification can establish new PREP/BUILD software evidence. Source PASS never supplies whole INPUT, native transport, physical balance, AAA or ABA credit. AAA remains7/8; ABA unstarted. No memory success is predicted.
'''
write(P/'ROOT_NEXT_STEPS.txt',steps.encode())
dump(P/'AUTHOR_SOURCE_ONLY_REPORT.json',dict(schema='AUTHOR_COMPLETE_V25_POSTSTAGE_TEMPORARIES_SOURCE_REVIEW_V1',status='AUTHOR_SOURCE_ONLY_COMPLETE_UNREADY_NO_EXECUTION',source_only=True,author_not_independent_peer=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],qualified_role_Source_pins={role:pin(P/rel)for role,rel in ROLE_FILES.items()},canonical_top_definition_count=len(defs(texts['canonical'])),only_success_path_new_business_body_statement='del stages,audit,commands;gc.collect()',prior_failure_scope=prior_truth,all_original_full_fields_records_guards_and_gates_retained=True,new_helper_Q_or_software_business_or_science_qualification=False,candidate_helper_guard_API_compile_native_material_numeric_executed=False,new_Source_install_executed=False))
write(P/'AUTHOR_EXECUTED_SOURCE.py',Path(__file__).read_bytes())
for path,wanted in READ_PINS.items():assert pin(path)==wanted
dump(P/'ALL_ORIGINAL_READ_SOURCE_AND_SMALL_META_PINS.json',dict(source_only=True,all_read_inputs_unchanged=True,full_read_input_pins=list(READ_PINS.values())))
print(json.dumps(dict(source_only=True,package=str(P),roles={role:pin(P/rel)for role,rel in ROLE_FILES.items()},report=pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json'),inverse=pin(P/'COMPLETE_SOURCE_INVERSES.json'),check_count=len(checks),candidate_helper_guard_API_compile_numeric_executed=False,original_inputs_unchanged=True)))

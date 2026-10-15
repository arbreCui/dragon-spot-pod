from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1
 raw=p.read_bytes();assert i7(a)==i7(p.lstat());return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i7(a))
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_bytes());report=json.loads((P/'AUTHOR_SOURCE_ONLY_REPORT.json').read_bytes());checks=[]
def check(k,v):
 assert type(v)is bool and v,k
 assert k not in[x['check']for x in checks]
 checks.append(dict(check=k,passed=True))
check('author_66_unique_exact_bool_checks_no_science',report['check_count']==66==len(report['checks']) and len({x['check']for x in report['checks']})==66 and all(type(x['passed'])is bool and x['passed']is True for x in report['checks'])and report['source_only']is True and report['author_not_independent_peer']is True and report['new_helper_Q_or_software_business_or_science_qualification']is False)
for role,rel in proof['role_filenames'].items():
 p=P/rel;text=p.read_text();ast.parse(text);original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
 for row in reversed(proof['exact_finite_transforms'][role]):
  assert type(row['count'])is int and row['count']>0 and text.count(row['new'])==row['count']
  text=text.replace(row['new'],row['old'])
 check(role+'_full_byte_AST_inverse_and_actual_pin',text==original and ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False)and pin(p)==report['qualified_role_Source_pins'][role])
canon=(P/'canonical.V25.UNREADY.full.py').read_text();tree=ast.parse(canon)
assign={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
business=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
check('canonical_six_new_business_slots_None',all(isinstance(assign[k],ast.Constant)and assign[k].value is None for k in business))
prep=(P/proof['role_filenames']['prepare_binder']).read_text();build=(P/proof['role_filenames']['build_binder']).read_text()
check('original_PREP_binder_canonical_replacement_anchors_match',"DRAFT_STATUS = 'UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND'"in canon and 'FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None'in canon and all(k+' = None'in canon for k in ('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN')))
check('PREP_binder_exact_new_output_basename',"'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'"in prep)
for role,expected in [('prepare_host','UNREADY_V25_ACTUAL_Q_AND_TARGET_SOURCE_UNBOUND'),('prepare_writer','UNREADY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_UNBOUND'),('build_host','UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'),('build_writer','UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND')]:
 text=(P/proof['role_filenames'][role]).read_text();t=ast.parse(text)
 slots={n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id.startswith('FUTURE_V25_')}
 check(role+'_original_binder_tight_None_and_status_anchors',bool(slots)and all(isinstance(v,ast.Constant)and v.value is None and k+'=None'in text for k,v in slots.items())and 'SOURCE_BINDING_STATUS='+repr(expected)in text)
run=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='run_build');delete=next(n for n in ast.walk(run)if isinstance(n,ast.Delete));update=next(n for n in run.body if isinstance(n,ast.Try)).body[-1]
check('release_after_complete_result_update_only',isinstance(update,ast.Expr)and isinstance(update.value,ast.Call)and isinstance(update.value.func,ast.Attribute)and isinstance(update.value.func.value,ast.Name)and update.value.func.value.id=='gc'and update.value.func.attr=='collect' and [n.id for n in delete.targets]==['stages','audit','commands'])
check('no_later_loads_of_released_locals',not any(isinstance(n,ast.Name)and isinstance(n.ctx,ast.Load)and n.id in('stages','audit','commands')and n.lineno>delete.lineno for n in ast.walk(run)))
check('original_BUILD_binding_requires_actual_new_PREP_peer',"E=BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'"in build and '--saved-prep-peer-report'in build and "actual_PREP_closed_EXIT0_verified"in build and 'helper_Q_admission()'in build)
check('no_old_namespace_in_seven_candidate_roles',all('v25-monitor-access-20261010'not in(P/rel).read_text()and'v25_monitor_access_sources'not in(P/rel).read_text()and'v25_monitor_access_receipts'not in(P/rel).read_text()and'combined_runtime_v25_monitor_access.py'not in(P/rel).read_text()for rel in proof['role_filenames'].values()))
inputs=json.loads((P/'ALL_ORIGINAL_READ_SOURCE_AND_SMALL_META_PINS.json').read_bytes())
check('all_parent_Source_and_actual_failure_meta_complete_unchanged',all(pin(row['path'])==row for row in inputs['full_read_input_pins']))
ns=json.loads((P/'FUTURE_ROOT_BINDING_AND_NAMESPACE_CONTRACT.UNREADY.json').read_bytes())
check('all_new_business_and_install_pins_unknown',all(v is None for v in ns['new_PREP_BUILD_result_pins'].values())and all(v is None for v in ns['new_actual_Source_binding_install_freeze_and_independent_peers'].values()))
print(json.dumps(dict(source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=True,blockers=[],author_report=pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json'),complete_inverse=pin(P/'COMPLETE_SOURCE_INVERSES.json'),candidate_guard_API_compile_numeric_executed=False)))

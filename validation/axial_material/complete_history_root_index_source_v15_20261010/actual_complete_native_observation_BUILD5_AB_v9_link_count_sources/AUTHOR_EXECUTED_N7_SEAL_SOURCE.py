from pathlib import Path
import ast,hashlib,json,stat
P=Path(__file__).resolve().parent
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not p.is_symlink();h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 assert identity(s)==identity(p.lstat());return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s))
report=P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json';r=json.loads(report.read_bytes())
assert r['source_only']is True and r['all_checks_typed_true']is True and r['blockers']==[]and type(r['check_count'])is int and r['check_count']==len(r['checks'])>0
assert all(type(c)is dict and set(c)=={'check','passed'}and type(c['check'])is str and c['passed']is True for c in r['checks'])and len({c['check']for c in r['checks']})==len(r['checks'])
tools=json.loads((P/'ACTUAL_AUTHOR_N7_COMPLETE_SOURCE_TOOL_RETURNS.json').read_bytes());last=tools['actual_tool_returns'][-1]['actual_tool_return'];assert type(last['exit_code'])is int and last['exit_code']==0 and 'session_id'not in last
assert json.loads(last['output'])['report_pin']==pin(report)
mf=P/'MANIFEST.json';assert not mf.exists();mf.write_text('{}\n')
members=[];dirs={}
for p in [P,*sorted(P.rglob('*'))]:
 s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
 if stat.S_ISDIR(s.st_mode):dirs[str(p)]=identity(s)
 elif p!=mf:members.append(dict(relative_path=str(p.relative_to(P)),fullpin=pin(p)))
value=dict(schema='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1',status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,members=members,member_count=len(members),full_file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,whole_original_native_Source_archive_members=1365,finite_necessary_full_Source_retention_only=True,author_finite_Source_check_pin=pin(report),finite_full_Source_fix_inverse_pin=pin(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json'),actual_author_Source_check_tool_returns_pin=pin(P/'ACTUAL_AUTHOR_N7_COMPLETE_SOURCE_TOOL_RETURNS.json'),original_frozen_N6_manifest_pin=r['original_N6_manifest_pin'],N6_complete_manifest_whole_byte_copy_pin=pin(P/'PREVIOUS_SEALED_N6_SOURCE_PROVENANCE/MANIFEST.json'),N7_changed_role_count=4,N7_failure_only_instrumentation_never_accepts_failed_monitor=True,N7_original_PS_lsof_argv_timeout_PID_selection_unchanged=True,N7_only_original_bounded_objects_wrapped_and_delegated=True,N7_no_successful_raw_scan_history_appended=True,N7_whole_regular_joint_disk_account_does_not_repair_failed_open_unlinked_scan=True,N7_all_original9caps_unchanged=True,N7_source_does_not_predict_storage_RSS_or_numerical_equality=True,N6_original_failed_lsof_raw=None,N6_original_failure_cause_unknown=True,N6_Source_admission_cannot_admit_N7=True,actual_peer_review=None,actual_Root_Source_admission=None,actual_Root_runtime_terminal=None,actual_observation_manifest=None,actual_native_Source_binary_linkage=None,actual_new_native_controls=None,actual_new_native_objects_archives_executable=None,actual_new_instrumented_monitor_controls=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
mf.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
assert {str(p):identity(p.lstat())for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}==dirs
assert all(pin(P/m['relative_path'])==m['fullpin']for m in members)
tree=ast.parse((P/'bind_complete_observation_SOURCE_only.UNREADY.py').read_text());roles=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ROLES'for x in n.targets));assert len(roles)==14
print(json.dumps(dict(status='SEALED_N7_FAILURE_ONLY_MONITOR_SOURCE_UNREADY_NO_EXECUTION',source_only=True,manifest_pin=pin(mf),report_pin=pin(report),member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),actual_author_Source_contract={k:pin(P/v)for k,v in roles.items()},actual_instrumented_monitor_controls=None,actual_N7_runtime_terminal=None,actual_scientific_qualification=None,candidate_or_helper_or_guard_or_API_or_native_or_material_executed=False),allow_nan=False))

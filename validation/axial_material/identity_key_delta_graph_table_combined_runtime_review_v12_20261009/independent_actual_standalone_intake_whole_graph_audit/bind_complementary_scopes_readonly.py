"""Small actual whole-INPUT scope binding; pure stdlib, no business execution."""
import hashlib,json,stat,time
from pathlib import Path
D=Path('/private/tmp/axmat_v12_actual_durable_whole_INPUT_graph_descriptor_independent_review_20261009')
S=Path('/private/tmp/axmat_v12_actual_intake_whole_body_source_independent_readonly_20261009')
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def read(p,sha):
 before=ident(p);raw=p.read_bytes();assert stat.S_ISREG(before[2]) and ident(p)==before and hashlib.sha256(raw).hexdigest()==sha
 return json.loads(raw),dict(path=str(p),sha256=sha,bytes=len(raw),seven_identity=before)
g,gp=read(D/'REPORT.json','ef70dccf43f5cc91341ff262eb991c78220ee8720f21702fd8280e327216a3eb')
s,sp=read(S/'REPORT.json','39b096153914a9f4e2ee205c70e084ff564564f243baeee876ef8d2767b56ce1')
gr,grp=read(D/'actual_readonly_tool_terminal_return.json','8daf251059c32289132ea8edbb973e3542ef3a1f452ca780535f2a272e243198')
sr,srp=read(S/'actual_readonly_tool_terminal_return.json','e6b88af007b383e6220fec5c9e462702ddc802476003bf836dadfd8bac2f00f9')
assert g['status']=='PASS_GRAPH_DESCRIPTOR_DURABLE_SCOPE_ONLY' and s['status']=='PASS_COMPLETE_ACTUAL_65_FIELD_BODY_AND_SOURCE_PROVENANCE_METADATA_ONLY'
for r in (gr,sr):
 assert type(r['returncode']) is int and r['returncode']==0
 assert type(r['actual_terminal_tool_result']['exit_code']) is int and r['actual_terminal_tool_result']['exit_code']==0
 assert 'session_id' not in r['actual_terminal_tool_result'] and r['record_written_after_actual_terminal_return'] is True
assert g['actual_Root_receipt']['sha256']==s['actual_root']['sha256']=='449d08d08cdfe7cb19eaf3a882312f8d6c21725011650289608e4bae601178bf'
assert g['whole_API_pin']['sha256']==s['actual_whole_API']['sha256']=='65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536'
root,rp=read(Path(s['actual_root']['path']),s['actual_root']['sha256'])
assert root['actual_tool']==dict(initial_chunk_id='3900c7',session_id=49432,terminal_chunk_id='bbe76b',exit_code=0)
assert type(root['actual_exit_code']) is int and root['actual_exit_code']==0 and root['record_written_after_actual_tool_return'] is True
observed={}
for p,v in s['observed_files'].items():assert ident(Path(p))==v['seven_identity'];observed[p]=v['seven_identity']
for p,v in g['all_small_full_SHA_pins'].items():assert ident(Path(p))==v['identity'];observed[p]=v['identity']
assert g['descriptor_count']==s['complete65_descriptor_union_count']==36804
assert g['alias_count']==s['complete_declaration_alias_count']==186
assert g['canonical_count']==36776 and g['namespace_count']==86 and g['absence_count']==449
assert g['graph_proof']['requirement_rows']==237767
assert len(s['full_65_field_provenance'])==s['whole_body_top_field_count']==65
assert all(v is True for v in s['checks'].values())
for k in ('business_imports_or_calls','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):
 assert g[k] is s[k] is False
r=dict(schema='AXMAT_V12_ACTUAL_WHOLE_INPUT_COMPLEMENTARY_FULL_SCOPE_BINDING_V1',status='PASS',
 scope='ACTUAL_COMPLETE_BOUND_RUNTIME_INPUT_ONLY_NO_COLD_NATIVE_AAA_ABA',
 graph_descriptor_namespace_resource_scope=gp,graph_actual_closed_tool_receipt=grp,
 whole65_seven_INPUT_V11_68_control_body_source_scope=sp,source_actual_closed_tool_receipt=sr,
 actual_Root_durable_receipt=rp,actual_host_tool=root['actual_tool'],
 whole_API_sha256=s['actual_whole_API']['sha256'],whole_API_bytes=s['actual_whole_API']['bytes'],
 durable_payload_files=9,durable_members=10,durable_payload_bytes=26415645,
 whole65_typed_order_and_floatbits_pass=True,seven_historical_INPUT_full_body_pass=True,
 actual_V11_trim_full_75_fields_and_30_counts_and_68_controls_pass=True,
 descriptor_files=36804,canonical_files=36776,complete_requirements=237767,namespaces=86,aliases=186,absence_inputs=449,
 declared_resource_roots=g['declared_resource_root_count'],current_dynamic_resource_roots=g['current_resource_root_count'],
 historical_bytes_freshly_read_by_actual_guarded_API_not_reexecuted_by_reviewers=True,
 independent_reviewers_business_phase_calls=0,historical_scientific_union_reread_by_reviewers=False,
 shared_source_and_witness_identity_pin_count=len(observed),fresh_identity_binding_sha256=hashlib.sha256(json.dumps(observed,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 original_API_512_MiB_stage_limit_satisfied=True,observed_API_peak_MiB=498.75,
 original_1800_600_512_one_thread_one_child_zero_retry_caps_unchanged=True,
 observed_whole_seconds=53.15720783296274,
 pure_graph_reviewer_failures_preserved=['failed_reader_stage_serialization_order','failed_reader_requirement_table_sort_boundary','failed_reader_trace_duplicate_assumption'],
 source_reviewer_failures_preserved=s['known_pure_reviewer_errors'],
 C_B_F_future_actual_cold_bindings_not_modified=True,project_written=False,files_deleted=0,
 cold_prepared=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
p=D/'combined_scope_binding.json';assert not p.exists();p.write_text(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(status='PASS',report=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))

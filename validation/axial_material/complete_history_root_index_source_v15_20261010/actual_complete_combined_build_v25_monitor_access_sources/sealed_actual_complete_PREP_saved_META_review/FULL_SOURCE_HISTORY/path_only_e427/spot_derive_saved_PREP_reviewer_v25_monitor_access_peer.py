"""Finite Source-only seven-directory derivation of frozen reviewer8843.
Never imports or runs the saved evidence reviewer or any project Source.
"""
import ast,hashlib,json,os,stat
from pathlib import Path
OLD=Path('/private/tmp/axmat_v25_complete_PREP_saved_META_reviewer_UNREADY_an2zkybe')
NEW=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_UNREADY_20261010')
mapping={
 'D':('actual_complete_combined_prepare_v25_sources','actual_complete_combined_prepare_v25_monitor_access_sources'),
 'E':('actual_complete_combined_prepare_v25_receipts','actual_complete_combined_prepare_v25_monitor_access_receipts'),
 'H':('axial-material-complete-combined-prepare-host-v25-20261010','axial-material-complete-combined-prepare-host-v25-monitor-access-20261010'),
 'S':('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010'),
 'O':('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010'),
 'T':('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010'),
 'C':('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py')}
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def statement(s,n):return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
def assigns(t):return {n.targets[0].id:n for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
p=OLD/'review_actual_complete_PREP_saved_META_stdlib.py';before=pin(p)
assert before['sha256']=='8843fac04cc3c6677bbd75687ac474d67616e2cdc23088c3ec1f0ae9d7ce0cb3'
old=p.read_text();ot=ast.parse(old);oa=assigns(ot);new=old;rows=[]
for name,(a,b) in mapping.items():
 s=statement(old,oa[name]);assert s.count(a)==1 and new.count(s)==1
 d=s.replace(a,b,1);new=new.replace(s,d,1);rows.append(dict(global_name=name,old_statement=s,new_statement=d,count=1))
nt=ast.parse(new);na=assigns(nt)
assert set(oa)==set(na) and {k for k in oa if ast.dump(oa[k],include_attributes=False)!=ast.dump(na[k],include_attributes=False)}==set(mapping)
recovered=new
for row in reversed(rows):
 assert recovered.count(row['new_statement'])==1
 recovered=recovered.replace(row['new_statement'],row['old_statement'],1)
assert recovered.encode()==old.encode() and ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ot,include_attributes=False)
defs=[n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))];nder=[n for n in nt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
assert len(defs)==len(nder) and all(statement(old,n)==statement(new,d) and ast.dump(n,include_attributes=False)==ast.dump(d,include_attributes=False) for n,d in zip(defs,nder))
inputp=OLD/'ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json';ip=pin(inputp);cfg=json.loads(inputp.read_bytes());keys=ast.literal_eval(oa['INPUT_KEYS'].value)
assert len(keys)==18 and all(cfg[k] is None for k in keys) and cfg['actual_terminal_chunks']=={'PREP':None,'metadata_writer':None} and cfg['later_E_files_after_writer_joint_sample'] is None
assert cfg['status']=='UNREADY_ROOT_COMPLETE_PREP_NOT_EXECUTED' and not os.path.lexists(NEW)
NEW.mkdir();out=NEW/p.name;out.write_text(new);saved=NEW/('original_'+p.name);saved.write_bytes(p.read_bytes())
assert pin(saved)['sha256']==before['sha256'] and pin(p)==before
(NEW/inputp.name).write_bytes(inputp.read_bytes());assert pin(inputp)==ip
seal=OLD/'seal_actual_complete_PREP_saved_META_review_stdlib.py';sp=pin(seal)
assert sp['sha256']=='6274b7a346809b3e8117bf4f8f2d7ce5febd272dc545f5dfb437a61f477c904c'
ast.parse(seal.read_text());(NEW/seal.name).write_bytes(seal.read_bytes());assert pin(seal)==sp
(NEW/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
checks=[dict(check=k,passed=True) for k in ('original8843_full_EOF_SHA7ID_unchanged','exact_seven_named_global_directory_assignments_only','complete_byte_inverse_to8843','complete_AST_inverse_to8843','all_original_function_class_bodies_byte_exact','all_Q_helper_case_caps_physics_stage_monitoring_schemas_credit_logic_unchanged','all18_actualpins_and_two_actualchunks_and_laterE_unknown_None','original_sealer6274_byte_exact_no_execution')]
v=dict(schema='INDEPENDENT_V25_MONITOR_ACCESS_SAVED_PREP_REVIEWER_SOURCE_DIRECTORY_INVERSE_V1',status='SOURCE_ONLY_DESIGN_READY_ACTUAL_PREP_NOT_EXECUTED',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],original_reviewer_pin=before,full_original_reviewer_copy=pin(saved),derived_reviewer_pin=pin(out),exact_seven_directory_statement_inverses=rows,full_byte_inverse_verified=True,full_AST_inverse_verified=True,original_definition_count=len(defs),all_function_class_bodies_full_byte_unchanged=True,original_sealer_pin=sp,derived_sealer_pin=pin(NEW/seal.name),all_actual_future_pins_remain_None=True,saved_PREP_reviewer_executed=False,candidate_helper_API_compiler_native_material_or_numeric_executed=False,actual_PREP_review_terminal=None,actual_PREP_PASS_report=None,actual_BUILD_terminal=None,whole_INPUT_or_BUILD_or_science_qualified=False)
write(NEW/'SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json',v)
(NEW/'ROOT_NEXT_STEPS.UNREADY.txt').write_text('Source-only new directory adaptation; do not execute until Root supplies genuine CLOSED int0 PREP and metadata writer, complete18 four-field actual pins, actual terminal chunks and exact later E files. Schema remains V25. All future actual values are None. Run review with --inputs ACTUAL_INPUTS --inputs-sha256 ACTUAL_SHA --output FRESH_PRIVATE_TMP. Preserve actual raw tool result as a string; only after successful actual review seal with the copied original sealer. This Source design creates no actual PREP/BUILD/science qualification.\n')
print(json.dumps(dict(source_only=True,status=v['status'],derived_reviewer_pin=pin(out),inverse_pin=pin(NEW/'SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json'),unready_inputs_pin=pin(NEW/inputp.name),check_count=len(checks),all_checks_typed_true=True,definition_count=len(defs),old8843_unchanged=pin(p)==before,actual_PREP_review_terminal=None,actual_PREP_PASS_report=None,candidate_numeric_or_saved_PREP_reviewer_executed=False)))

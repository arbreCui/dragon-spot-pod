import ast,hashlib,json,stat
from pathlib import Path
D=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009');ROOT=Path('/Users/wen/spot');PINS={}
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,sha):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])and p.resolve(strict=True)==p
 observed=hashlib.sha256(p.read_bytes()).hexdigest();assert observed==sha and identity(p)==before
 row=dict(path=str(p),sha256=sha,identity=before,bytes=before[3]);PINS[str(p)]=row;return row
def read(p,sha):
 row=pin(p,sha);d=json.loads(Path(p).read_text());assert identity(Path(p))==row['identity'];return d
G=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
proof=read(G/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
receipt=read(G/'actual_readonly_tool_return.json','34075c6b3c6f0e4197ab6e5ea93bd16b615ca25a3b38f6b57af87b6d8edaa1dd')
joint=read(G/'joint_scope_binding.json','f6d7fe1efff715350daa344d74ce40f1416089270d09347f0f1dca54e151fe91')
jointreceipt=read(G/'actual_joint_readonly_tool_return.json','38bfc4346fd806b05124998ec01ff5aea1832dbdff7374d0128e74a11b0db5f5')
assert proof['status']==joint['status']=='PASS'and joint['scientific_qualification']is False
assert receipt['actual_tool_result']==dict(initial_chunk_id='9a9803',session_id=71255,terminal_chunk_id='c050ac',exit_code=0,closed=True)
assert jointreceipt['actual_tool_result']==dict(chunk_id='208936',exit_code=0,closed=True)
work=Path(proof['actual_binding']['path']).parent
formal=ROOT/'validation/axial_material'
sources=[(work/'runtime/combined_cold_own_rss_host.py','dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7'),
 (work/'runtime/combined_cold_own_rss_controls.py','d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393'),
 (formal/'combined_cold_own_rss_host_physical_basis_own_pid_peak_20261008.py','dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7'),
 (formal/'combined_cold_own_rss_controls_own_pid_peak_20261008.py','d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393'),
 (formal/'cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py','ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b'),
 (work/'runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
 (work/'runtime/production_runner.py','67ae4ae465013fd7c7bd5ccb07c9d06c9b7e88dba9ba8481c7e4a506f15147bf')]
inventory={}
for p,sha in sources:
 pin(p,sha);text=p.read_text();tree=ast.parse(text)
 wanted={'control_namespace','control_archive_bytes','own_pid_peak_admission','controls_admission','fixture','watch_admission','run_controls','main','start_liveness_watchdog','finish_liveness_watchdog','terminate_group','process_group_exists'}
 defs={}
 for node in tree.body:
  if isinstance(node,ast.FunctionDef)and node.name in wanted:
   src=ast.get_source_segment(text,node);defs[node.name]=dict(first_line=node.lineno,full_source=src,source_sha256=hashlib.sha256(src.encode()).hexdigest())
  if isinstance(node,ast.ClassDef)and node.name in ('OwnRSSSerialExecutor','SerialExecutor'):
   for fn in node.body:
    if isinstance(fn,ast.FunctionDef)and fn.name in ('__init__','execute','_process'):
     src=ast.get_source_segment(text,fn);defs[node.name+'.'+fn.name]=dict(first_line=fn.lineno,full_source=src,source_sha256=hashlib.sha256(src.encode()).hexdigest())
 inventory[str(p)]=dict(source=PINS[str(p)],definitions=defs)
control_text=(work/'runtime/combined_cold_own_rss_controls.py').read_text()
assert "for mode in ('positive','oversize','short'):"in control_text
assert "value['own_pid_wait4_peak_rss_mib'] < 16"in control_text
assert 'OVERSIZE_BYTES = 576 * 2**20'in control_text
assert "executor = full.OwnRSSSerialExecutor(Path(b['work_root']),120,'binding_controls',resources)"in control_text
with(D/'complete_controls_boundary_source_inventory.json').open('x')as f:json.dump(inventory,f,indent=2);f.write('\n')
plan=dict(schema='AXMAT_V9_ACTUAL_CONTROLS_COMPLETE_GRAPH_OWNER_RESOURCE_POSTTERMINAL_SOURCE_PLAN_V1',status='SOURCE_SCOPE_PLAN_ONLY_WAITING_ROOT_TRUE_TERMINAL_AND_DURABLE_RECEIPT',
 known_binding=proof['actual_binding'],inherited_full_binding_graph_report=PINS[str(G/'REPORT.json')],inherited_graph_reader_true0=receipt['actual_tool_result'],inherited_complete_complementary_joint_report=PINS[str(G/'joint_scope_binding.json')],inherited_joint_true0=jointreceipt['actual_tool_result'],
 future_actual=dict(actual_Root_controls_closed_tool=None,actual_Root_controls_observer=None,actual_controls_seal=None,actual_controls_result=None,actual_controls_terminal_receipt=None,actual_reader_tool=None,actual_reader_report=None),
 work_root=str(work),controls_root=str(work/'binding_controls'),control_terminal_root=str(ROOT/'validation/artifacts/axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'),
 exact_actual_runtime_host=PINS[str(work/'runtime/combined_cold_own_rss_host.py')],exact_actual_runtime_controls=PINS[str(work/'runtime/combined_cold_own_rss_controls.py')],
 expected_success_control_namespace=dict(files=['claim.json','positive/execute.log','positive/execute.watchdog.json','oversize/execute.log','oversize/execute.watchdog.json','short/execute.log','short/execute.watchdog.json','stages.json','result.json','seal.json'],directories=['oversize','positive','short'],symlinks=[]),
 expected_success_stages=dict(order=['binding_controls/positive/execute','binding_controls/oversize/execute','binding_controls/short/execute'],statuses=['PASS','FAILED','PASS'],oversize_is_expected_original_RSS_rejection_not_whole_program_failure=True),
 whole_expected_ownerunion=dict(original_metadata_files=37339,full_binding_expected_files=37395,new_owner_expectations_at_controls='No mutation or backfill of binding.files; new control files have their independent exact seal. Explicit whole binding60.6MB SHA/identity remains immutable.',binding_selfpin_absent=True),
 full_graph_inheritance=dict(canonical_files=35647,canonical_bytes=35803098221,requirement_rows=235528,namespaces=86,aliases=186,absence_inputs=445,API_descriptor_files=35675,original_declared_roots=231,current_explicit_roots=236,complete_recent_dtype_layout_typed_owners_all_trace_body_and_whole65_original7_trim73_new7_preserved=True,new_35GB_read=False,fresh_all_canonical_and_mfiles_seven_field_identity_before_after_required=True),
 resources=dict(history_budget_bytes=96*2**30,min_free_bytes=8*2**30,control_archive_limit_bytes=64*2**20,control_reservation_bytes=64*2**20,whole_seconds=120,stage_seconds=60,rss_cap_mib=512,threads=1,children=1,retries=0,original_future_AAA_reserve_bytes=20971764748,dynamic_full_axial_family_union=True,old_resources_filecount_or_bytes_not_fixed_current_gate=True,new_controls_and_Root_terminal_count_freshly_in_live_roots=True,archive_exact_source_rule='sum all binding_controls regular payload bytes + pinned host bytes + pinned controls_source bytes + own_rss_binding bytes; independent CONTROL_TERMINAL excluded only from archive, included in complete history resources'),
 own_pid_peak_required=dict(contract='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1',positive_and_short='require all real fields; typed own wait4 observedTrue/pid exact/status terminal/exit0/raw integer finite Darwin bytes/kernel conversion exact/nonzero observed<512',short='real own wait4 kernel peak >=16MiB; no missing/None/default0 permitted',live_samples_zero='only when original count==0 and sampled==0 with genuine terminal wait4; no fabricated sample',oversize='actual own-PID sampled>=512 and return -15/-9/original RSS branch; all wait4 fields remain actual values or allNone if genuine unobserved, never invented',observed='max of actual sampled and actual kernel where present; missing positive/short kernel is a failure'),
 actual_postreview_gates=[
 'Wait Root typed genuine terminal0/CLOSED plus success recorder receipt; do not infer from files existence or poll half-written namespace.',
 'Fresh full hashes Root observer/terminal/rawstdout/stderr/seal/result/stages and all exact10 control payloads; actual namespace seal covers all9 previous files plus seal self exclusion.',
 'Every original SOURCE31/OUTPUTlocal43/prepared/binding and TERM9 byte pin/identity remains unchanged; only controls10 + separate Root terminal3 new artifacts allowed.',
 'Whole37395 independent expected map and391 actual module owners unchanged, no arbitrary current source SHA becomes expected; explicit sealed control files are additional endpoint scope.',
 'All canonical35647 recent truefullBYTE evidence + fresh7 identities beforeafter; complete m37339 and all typed235528 rows/ns86/aliases186/absence445 retained under immutable graph file.',
 'Complete runtime31/source namespace fixed; no generated directory alias or mutated controller/class/global/function overlay.',
 'Read complete actual raw3 logs; allocation-intent PID/mode/16 or576MiB exact; positive and short true completion marker; original own-PID RSS rejection exact oversize.',
 'Strict full watcher PID/command/status/time/samplecount/wait4 conversion/cleanup/short16 kernel and recorded no-live-group observation boundaries; no missing values filled.',
 'Four complete controls tail fields remain genuinely afterseal tail; elapsed<120, stage<=60, total archive<64MiB and original history96/free8.',
 'Live resource root membership beforeafter derived currently all236 explicit oldroots retained + dynamic union, CONTROL_TERMINAL now valid if root created; historical runtime filecount not frozen.',
 'Historical actual resource snapshots before Root terminal additions are source-time observations; compare declared policy/roots/caps and accounting timing, do not require equality to later current bytes.',
 'Fresh full resource metadata beforeafter stable, original futureAAA21GiB reservation gate separate from64MiB controls reservation retained.',
 'Complete result capabilities/sourceMRO/codehash actual identity and original constructor/helper cleanup source are independently peer reviewed, not re-executed by reader.',
 'If realRoot nonzero: record exact failure/partialnamespace; no success controls/seal/tail/science promotion, no retry.',
 'Only control-guard correctness evidence; no native Dragon/transport/assembly/solve/AAA/ABA credit, all subsequent prepared_cold/production outputs future until separate actual stages.'
 ],
 all_future_fields_None=True,new_control_output_or_stream_read=False,actual_controls_started_by_this_plan=False,business_or_graph_helper_imported=False,source_AST_only_no_exec_or_constructor=True,project_written=False,scientific_qualification=False,pins=PINS)
for p,row in PINS.items():assert identity(Path(p))==row['identity']
with(D/'PLAN.json').open('x')as f:json.dump(plan,f,indent=2);f.write('\n')
print(json.dumps(dict(status=plan['status'],source_files=len(sources),actual_controls_fields_None=True,controls_or_business_executed=False,plan_sha256=hashlib.sha256((D/'PLAN.json').read_bytes()).hexdigest()),sort_keys=True),flush=True)

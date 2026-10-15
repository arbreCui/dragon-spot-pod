"""Source/metadata contract only; importing this module does not run a build."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent;OUT=R/'validation/artifacts/axial-material-B-IO-build-qualification-20261015-v1'
IO=BASE.parent/'B_only_observer_IO_source_v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUTPUT_BOUND=32*2**20;SOURCE_BOUND=16*2**20
FALSE=dict(B_native_executed=False,B_observation_context_produced=False,compiled_IO_semantics_qualified=False,original_binary_qualified=False,historical_C_compiler_restored=False,original_compiled_archive_ABI_or_features_reconstructed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,system_compiler=None):
 q=Path(p['path']);s=q.lstat();fortran=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==p['identity'][3]==2
 system=p==system_compiler and q==Path('/Library/Developer/CommandLineTools/usr/bin/clang')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111)
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or fortran)and identity(s)==p['identity']and s.st_size==p['size_bytes']and(s.st_uid==os.getuid()or system),'exact frozen current7, only explicit existing compiler role may be system owned')
 return q
def current_metadata_role(p,plan):
 if p in plan['readonly_system_tool_metadata_pins']:
  q=Path(p['path']);s=q.lstat();need(q in(Path('/bin/ps'),Path('/usr/sbin/lsof'))and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111)and identity(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'only explicitly frozen readonly PS/lsof metadata roles')
 else:current(p,plan['C_compiler_pin'])
def pin_source(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(identity(os.fstat(f.fileno()))==identity(s),'opened Source/metadata7')
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b)
  need(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/metadata7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def metadata(p):
 current(p);need(p['size_bytes']<8*2**20,'metadata8MiB');raw=Path(p['path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata wholeSHA');v=json.loads(raw);current(p);return v
def source_module(p,name):
 need(pin_source(p['path'])==p,'whole Source fullPF');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def write_once(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'each Source metadata8MiB')
 need(sum(x.stat().st_size for x in BASE.rglob('*')if x.is_file()and not x.is_relative_to(OUT))+len(raw)<SOURCE_BOUND,'entire Source/metadata16MiB')
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def genuine(v,key,p,output_key,code=0):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine original closed typed return')
 need(json.loads(t['output'].strip().splitlines()[-1])[output_key]==p,'genuine return binds exact artifact PF')
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())
def admit_current_C_compiler_capture(plan):
 proof=metadata(plan['C_compiler_tool_full_pin_metadata']);tools=metadata(plan['C_compiler_tool_true_returns_pin'])
 need(proof['schema']=='ROOT_CURRENT_EXISTING_C_COMPILER_TOOL_BYTE_PIN_ONLY_V1'and proof['compiler_tool_pin']==plan['C_compiler_pin']and proof['compiler_executed']is False and proof['ABI_qualified']is False,'existing compiler bytes only, no inherited compile or ABI qualification')
 need(tools['schema']=='ROOT_CURRENT_C_COMPILER_PATH_AND_BYTE_PIN_TRUE_TOOL_RETURNS_V1'and tools['compiler_executed']is False and tools['ABI_qualified']is False,'genuine compiler path/byte capture metadata only')
 for key in('actual_path_lookup_return','actual_whole_byte_pin_return'):
  t=tools[key];need(type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'actual closed compiler lookup/byte-capture typed0')
 need(tools['actual_path_lookup_return']['output'].strip()==plan['C_compiler_pin']['path'],'genuine compiler entry path matches exact frozen current tool')
 captured=json.loads(tools['actual_whole_byte_pin_return']['output'].strip())
 need(captured['compiler_tool_pin']==plan['C_compiler_pin']and captured['metadata_pin']==plan['C_compiler_tool_full_pin_metadata'],'genuine blind byte capture binds exact tool and metadata PFs')
 current(plan['C_compiler_pin'],plan['C_compiler_pin'])
def admit_archive_and_plaintext_roles(plan):
 archived=metadata(plan['archive_control_plan_pin']);a=metadata(plan['archive_actual_post_pin']);at=metadata(plan['archive_actual_post_tools_pin']);ar=metadata(plan['archive_Root_tools_pin'])
 genuine(at,'actual_review_return',plan['archive_actual_post_pin'],'review_pin');genuine(ar,'actual_terminal_return',plan['archive_Host_report_pin'],'report_pin')
 need(a['schema']=='RECORDED_RESULT48_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and a['status']=='PASS_ACTUAL_ALL48_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_PLAINTEXT_RETAINED'and a['failure']is None and a['metadata_only']is True and a['actual_Root_tools_pin']==plan['archive_Root_tools_pin']and a['actual_Host_report_pin']==plan['archive_Host_report_pin']and a['execution_binding_pin']==plan['archive_control_plan_pin'],'actual48 byte archive Root0/post0 bound exactly, no decompression replay here')
 need(a['actual_Root_integer_exit_code']==a['actual_child_integer_exit_code']==0 and a['Root_actual_streamed_decompression_proofs_matched_original_fullPF']is True and len(a['ordered48_original_plain_full_pins'])==48 and a['ordered48_original_plain_full_pins']==archived['all48_plain_pins']==plan['historical48_plain_full_pins']and a['original_plain_bytes']==805236925,'historical complete48 operands remain fullPF bound')
 for p in a['ordered48_compressed_archive_full_pins']:current(p)
 latest_roots=metadata(plan['latest_complete_plan_pin'])['complete_joint_roots']
 need(len(a['ordered48_compressed_archive_full_pins'])==48 and archived['complete_joint_roots']==latest_roots[:len(archived['complete_joint_roots'])],'whole archive prefix preserved inside entire later prefix, not just its final count')
 need(plan['plain48_retirement_post_key_audit_completed']is True,'Root execution order requires genuine exact48 plaintext retirement/post0 before B build; no compiled-input dependency implied')
 keys=plan['plain48_actual_role_projection'];r=metadata(plan['plain48_retirement_receipt_pin']);rt=metadata(plan['plain48_retirement_Root_tools_pin']);p=metadata(plan['plain48_retirement_post_pin']);pt=metadata(plan['plain48_retirement_post_tools_pin'])
 genuine(rt,keys['Root_execution_return_field'],plan['plain48_retirement_receipt_pin'],keys['Root_execution_output_receipt_field']);genuine(pt,keys['post_return_field'],plan['plain48_retirement_post_pin'],keys['post_output_review_field'])
 released=r[keys['released_pins_field']];historical={x['path']:x for x in plan['historical48_plain_full_pins']}
 need(r['schema']==keys['receipt_schema']and r['status']==keys['receipt_success_status']and r['failure']is None and len(released)==len({x['path']for x in released})==48 and{x['path']:x for x in released}==historical and r[keys['released_bytes_field']]==805236925,'exact48 fullPF historical plaintext roles retired by genuine receipt only; no release-order assumption')
 need(p['schema']==keys['post_schema']and p['status']==keys['post_success_status']and p['failure']is None and p[keys['post_receipt_pin_field']]==plan['plain48_retirement_receipt_pin']and p[keys['post_Root_tools_pin_field']]==plan['plain48_retirement_Root_tools_pin'],'exact actual retirement post schema and role projection audited before freeze')
 retired={x['path']for x in plan['historical48_plain_full_pins']}
 need(len(retired)==48 and all(not os.path.lexists(x)for x in retired)and not retired&{x['path']for x in plan['compile_and_link_input_pins']},'48 absent historical result roles never relabelled as current compiled inputs')
 return dict(historical_plaintext_fullPFs_preserved=True,current_compiled_input_scope_unchanged=True,archive_byte_values_recomputed=False)
def commands(plan):
 old=metadata(plan['original75_build_report_pin']);planner=source_module(plan['IO_command_planner_Source_pin'],'B_IO_original_command_planner')
 result=planner.IO_build_commands(old,OUT/'sources',OUT/'sources/build',OUT/'sources/runtime/Dragon',plan['C_compiler_pin']['path'],plan['C_configuration'])
 for row in result['compile_commands'][1:]:
  i=row.index('-c');row[i:i]=['-include',str(OUT/'sources/B_IO_ABI_ASSERTIONS.h')]
 need(len(result['compile_commands'])==4 and result['original_explicit_object_count']==71 and result['new_explicit_object_count']==74 and len([p for p in result['link_command']if p.endswith('.a')])==4,'exact4compile+1link;74objects and4archives')
 return result
def admit_lifecycle(plan):
 need(plan['early14_actual_post_key_audit_completed']is True,'early14 actual0/post0 field audit mandatory; archive is not a data prerequisite')
 r=metadata(plan['early14_receipt_pin']);t=metadata(plan['early14_Root_tools_pin']);p=metadata(plan['early14_post_pin']);pt=metadata(plan['early14_post_tools_pin'])
 genuine(t,'actual_execution_return',plan['early14_receipt_pin'],'receipt_pin');genuine(pt,'actual_review_return',plan['early14_post_pin'],'review_pin')
 need(r['mode']=='execute'and r['status']=='RETIRED_EXACT_LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOLS_ONLY'and r['failure']is None and len(r['actual_released_pins'])==14 and r['actual_released_bytes']==149659264 and r['actual_released_pins']==plan['exact_early14_retired_pins']and all(not os.path.lexists(x['path'])for x in r['actual_released_pins']),'exact genuine early14 lifecycle only')
 need(p['schema']==plan['early14_post_schema']and p['status']==plan['early14_post_status']and p['failure']is None and p[plan['early14_post_receipt_field']]==plan['early14_receipt_pin']and p[plan['early14_post_tools_field']]==plan['early14_Root_tools_pin'],'actual separate post exact roles audited before Source freeze')
 latest=metadata(plan['latest_complete_plan_pin']);need(latest['complete_joint_roots']==plan['complete_joint_roots'][:-1]and plan['complete_joint_roots'][-1]==str(OUT),'entire exact latest admitted prefix plus one fresh whole owning build root; no fixed ordinal/count-only replacement')
 need(any(BASE.is_relative_to(Path(x))for x in latest['complete_joint_roots'])and str(OUT)==plan['planned_actual_output_root'],'Source already counted under FTOP and whole build/runtime/log/report counted once as final new root')
 if plan['intervening_archive_admission_pin']is not None:metadata(plan['intervening_archive_admission_pin'])
 admit_current_C_compiler_capture(plan);admit_archive_and_plaintext_roles(plan)
 return r

"""Formal independent Source review only: no import/compiler/compiled or science payload access."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent

def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
 r=q.read_bytes();s=q.lstat();return dict(path=str(q),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=ids(s))
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and all(type(x)is int for x in p['identity']),'exact current7 Python integerPF')
 return s
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'Source/report metadata8MiB only')
 with Path(p['path']).open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened Source/meta7');r=f.read();need(ids(os.fstat(f.fileno()))==p['identity'],'EOF Source/meta7')
 need(len(r)==p['size_bytes']and hashlib.sha256(r).hexdigest()==p['sha256'],'wholeSource/metaSHA');current(p);return r
def unique(rows):
 d={}
 for p in rows:need(p['path']not in d or d[p['path']]==p,'one exact PF per path');d[p['path']]=p
 return list(d.values())
def genuine(d,key,chunk,p,role):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and r['chunk_id']==chunk and type(r['exit_code'])is int and r['exit_code']==0 and not r.get('session_id')and json.loads(r['output'].strip().splitlines()[-1])[role]==p,'genuine typed0 exactstdoutPF')

def main():
 pa=pin(D/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');pr=pin(D/'SOURCE_REVIEW_READY.json');pg=pin(D/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
 need(pa['sha256']=='c5a1311ff3295430565e0af50a47864707ef6ac87de725a51c0b04ad3ead97bf'and pr['sha256']=='eacc3117611f11109939d41160a13b02774fdbc09b689f74273fbb4457c37253'and pg['sha256']=='1622e85223866d4dbd548894009b91192ccf208d7c8f646a55002c4a3dc6f477','exact Root frozen AUTHOR/READY/raw')
 author=json.loads(full(pa));ready=json.loads(full(pr));gen=json.loads(full(pg));genuine(gen,'actual_Source_preparation_return','0139ac',pr,'ready_pin');pp=ready['control_plan_pin'];plan=json.loads(full(pp))
 need(ready['complete_source_file_pins']==author['whole_Source_file_pins']and len(ready['complete_source_file_pins'])==28 and author['author_Source_writes_stopped_after_freeze']is True and author['historical_compiler_or_archive_ABI_reconstruction_qualified']is False,'exact frozen28 Source table/no qualification inheritance')
 selected=unique(ready['complete_source_file_pins']+ready['dependencies']+[pa,pr,pg,plan['original75_build_report_pin']]);raw={p['path']:full(p)for p in selected}
 for p in ready['complete_source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(raw[p['path']].decode(),filename=p['path'])
 need(plan['schema']=='B_IO_BUILD_QUALIFICATION_SOURCE_ONLY_PLAN_V1'and plan['source_only']is True and ready['source_only']is True and ready['Source_or_compiler_business_executed']is False,'Source-only current plan')
 latest=json.loads(raw[plan['latest_complete_plan_pin']['path']]);out=Path(plan['planned_actual_output_root'])
 need(plan['complete_joint_roots']==latest['complete_joint_roots']+[str(out)]and len(latest['complete_joint_roots'])==65 and len(plan['complete_joint_roots'])==66 and not os.path.lexists(out),'entire65 plus fresh owning66')
 need(plan['original_caps']==latest['original_caps']==ready['original_caps']and plan['bounded_new_output_reservation_bytes']==32*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['host_summary_hard_bound_bytes']==6*2**20 and plan['Source_only_current_cumulative_bytes_before_reservations']+48*2**20<2*2**30,'complete32+16 original caps reservation proof metadata')
 abi=raw[str(D/'B_IO_ABI_ASSERTIONS.h')].decode();need(all(x in abi for x in ['defined(__APPLE__)','defined(__LP64__)','sizeof(int)==4','sizeof(float)==4','sizeof(double)==8','sizeof(void*)==8','__ORDER_LITTLE_ENDIAN__','defined(HDF5_LIB)','defined(OPENMP)','defined(MPI)']),'forced private C ABI assertions')
 cfg=json.loads(raw[plan['configuration_header_Source_evidence_pin']['path']]);need(cfg['status']=='PASS_SOURCE_ONLY'and cfg['failure']is None and cfg['configuration_and_header_Source_pins']==plan['original_Ganlib_configuration_and_header_Source_pins']and len(cfg['configuration_and_header_Source_pins'])==8 and cfg['actual_active_nonHDF5_local_include_closure']==plan['active_nonHDF5_project_header_closure']and len(plan['active_nonHDF5_project_header_closure'])==5,'exact8 configSource/5 active localheaders')
 need(cfg['original_Ganlib_Makefile_Source_facts']['default_ccompiler_line44']=='gcc'and cfg['original_Ganlib_Makefile_Source_facts']['llvm1_ccompiler_line41']=='clang'and plan['explicit_new_clang_IO_compiler_route']is True and plan['historical_C_compiler_restored']is False and plan['original_compiled_archive_ABI_or_features_reconstructed']is False and plan['new_compiled_ABI_or_IO_semantics_qualified']is False,'original gcc/newclang route distinct/no historicalABI claim')
 compiler=plan['C_compiler_pin'];ct=json.loads(raw[plan['C_compiler_tool_true_returns_pin']['path']]);proof=json.loads(raw[plan['C_compiler_tool_full_pin_metadata']['path']])
 need(compiler['path']=='/Library/Developer/CommandLineTools/usr/bin/clang'and proof['compiler_tool_pin']==compiler and proof['compiler_executed']is False and proof['ABI_qualified']is False,'Rootcaptured exactclang metadata only')
 for key in ['actual_path_lookup_return','actual_whole_byte_pin_return']:need(type(ct[key]['exit_code'])is int and ct[key]['exit_code']==0 and not ct[key].get('session_id'),'genuine Root toolcapture0')
 cap=json.loads(ct['actual_whole_byte_pin_return']['output']);need(ct['actual_path_lookup_return']['output'].strip()==compiler['path']and cap['compiler_tool_pin']==compiler and cap['metadata_pin']==plan['C_compiler_tool_full_pin_metadata'],'exact Root compiler path+bytePF capture')
 st=current(compiler);need(st.st_uid==0 and st.st_nlink==1,'literal readonly UID0 compiler metadata role')
 compiled=plan['compile_and_link_input_pins'];sci=plan['original_SCI_current7_only_pins'];need(len(compiled)==180 and len(sci)==2 and sum(p['size_bytes']for p in sci)==979740136,'complete180 compiled roles and exact2 SCI library scope')
 old=json.loads(raw[plan['original75_build_report_pin']['path']]);oldcompile=next(r['command']for r in old['records']if r['label']=='build/compile_0');oldlink=next(r['command']for r in old['records']if r['label']=='build/link_Dragon');cmds=plan['exact_five_stage_commands'];need(len(cmds)==5 and all(r['status']=='PASS'for r in old['records']),'old75 actual link metadata and exact5newstages')
 need(sum(x.endswith('.o')for x in oldlink)==71 and sum(x.endswith('.a')for x in oldlink)==4 and sum(x.endswith('.o')for x in cmds[4])==74 and sum(x.endswith('.a')for x in cmds[4])==4,'old71+4/new74+4')
 inverse=list(cmds[4]);Cobjects=[cmds[i][-1]for i in (1,2,3)]
 for x in Cobjects:inverse.remove(x)
 inverse[inverse.index(cmds[0][-1])]=oldcompile[-1];inverse[-1]=oldlink[-1];need(inverse==oldlink,'whole original75 linkargv inverse only observerIO replacement plus3Coverrides')
 cc=list(cmds[0]);ob=str(Path(oldcompile[-1]).parent);nb=str(out/'sources/build')
 for i,arg in enumerate(cc):
  if arg in('-I'+nb,'-J'+nb):cc[i]=arg[:2]+ob
 cc[-3]=oldcompile[-3];cc[-1]=oldcompile[-1];need(cc==oldcompile,'whole original observer compile argv inverse')
 for row,name in zip(cmds[1:4],['cle2000_c','clemod_c','kdrdpr']):need(row[0]==compiler['path']and row[row.index('-include')+1]==str(out/'sources/B_IO_ABI_ASSERTIONS.h')and row[-3]==str(out/'sources'/(name+'.B_IO.UNREADY.c'))and row[-1]in Cobjects,'exact3C overrides/forcedABI header')
 for hook in ['LIBMIX.observe.UNREADY.o','LIBDEN.observe.UNREADY.o','TONDRV.context_observe.UNREADY.o','TONSPH.observe.UNREADY.o']:need(any(Path(x).name==hook for x in cmds[4])and any(Path(x).name==hook for x in oldlink),'original scientific hook object unchanged')
 retired=plan['historical48_plain_full_pins'];gz=plan['current48_compressed_archive_pins'];r=json.loads(raw[plan['plain48_retirement_receipt_pin']['path']]);rt=json.loads(raw[plan['plain48_retirement_Root_tools_pin']['path']]);post=json.loads(raw[plan['plain48_retirement_post_pin']['path']]);pt=json.loads(raw[plan['plain48_retirement_post_tools_pin']['path']]);keys=plan['plain48_actual_role_projection']
 genuine(rt,keys['Root_execution_return_field'],'e94abb',plan['plain48_retirement_receipt_pin'],keys['Root_execution_output_receipt_field']);genuine(pt,keys['post_return_field'],'0c0408',plan['plain48_retirement_post_pin'],keys['post_output_review_field'])
 need(r['schema']==keys['receipt_schema']and r['status']==keys['receipt_success_status']and r['failure']is None and r[keys['released_pins_field']]==retired and r[keys['released_bytes_field']]==805236925 and post['schema']==keys['post_schema']and post['status']==keys['post_success_status']and post['failure']is None and post[keys['post_receipt_pin_field']]==plan['plain48_retirement_receipt_pin']and post[keys['post_Root_tools_pin_field']]==plan['plain48_retirement_Root_tools_pin']and post['retained48_gzip_pins']==gz,'exact actual retirement/post0 roles')
 need(len(retired)==len(gz)==48 and sum(p['size_bytes']for p in gz)==68959717 and not {p['path']for p in retired}&{p['path']for p in compiled+plan['explicit_cumulative_metadata_file_pins']},'old48 are only historical/not compiled or live metadata roles')
 for p in retired+plan['exact_early14_retired_pins']:need(not os.path.lexists(p['path']),'exact retired48+14 absent')
 host=raw[ready['host_source_pin']['path']].decode();contract=raw[ready['contract_Source_pin']['path']].decode();publisher=raw[str(D/'publish_B_IO_build_CLI.UNREADY.py')].decode()
 for text in ["wp=m.OUT/(record['label']+'.watchdog.json')","lp=m.OUT/(record['label']+'.log')","runner.execute(m.OUT/'sources/build',label,cmd,600)","full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","claim_before_metadata_EOF_or_import_or_compiler=True","original hostSELF512/whole1800 from initial claim"]:need(text in host,'original guard/path binding '+text)
 need("review['status']=='PASS_SOURCE_ONLY_B_IO_BUILD_QUALIFICATION'"in publisher and "review['complete_source_file_pins']==ready['complete_source_file_pins']"in publisher and "review['control_plan_pin']==ready['control_plan_pin']"in publisher,'exact publisher review interface')
 for p in compiled+sci+gz+plan['explicit_cumulative_metadata_file_pins']+plan['readonly_system_tool_metadata_pins']:current(p)
 for p in selected:full(p)
 for p in compiled+sci+gz+plan['explicit_cumulative_metadata_file_pins']+[compiler]:current(p)
 report=dict(schema='INDEPENDENT_B_IO_BUILD_QUALIFICATION_FORMAL_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_B_IO_BUILD_QUALIFICATION',failure=None,source_only=True,control_plan_pin=pp,complete_source_file_pins=ready['complete_source_file_pins'],selected_Source_pins=selected,complete_Source_metadata_union_count=len(selected),Source_review_ready_pin=pr,Root_Source_generation_true_tools_pin=pg,author_Source_freeze_pin=pa,genuine_Root_Source_generation_integer_exit_code=0,complete_Source_metadata_fullEOF_SHA_current7_verified_twice=True,compiled_input_count=180,all180_compiled_inputs_current7_only_verified_twice=True,SCI_library_count=2,SCI_library_bytes=979740136,SCI_library_roles_current7_only_verified_twice=True,C_compiler_current7_only_verified_twice=True,Root_compiler_lookup_and_byte_capture_metadata_genuine0=True,original_Ganlib_configuration_Source_pins=plan['original_Ganlib_configuration_and_header_Source_pins'],active_local_header_closure=plan['active_nonHDF5_project_header_closure'],original_gcc_default_and_explicit_new_clang_route_distinct=True,historical_C_compiler_restored=False,original_compiled_archive_ABI_or_features_reconstructed=False,new_compiled_ABI_or_IO_semantics_qualified=False,system_C_headers_transitive_EOF_claimed=False,original75_link_argv_whole_inverse_verified=True,original_observer_compile_argv_whole_inverse_verified=True,original4_scientific_hook_objects_retained=True,original_link_object_count=71,new_link_object_count=74,archive_count=4,stage_count=5,original_guard_MRO_and_once_5stage600_watchlog_record_label_Source_verified=True,complete_joint_roots=plan['complete_joint_roots'],original_caps=plan['original_caps'],bounded_new_output_reservation_bytes=32*2**20,bounded_new_Source_metadata_reservation_bytes=16*2**20,actual48_retirement0_and_independent_post0_verified=True,historical48_fullPFs_not_current_relabelled=True,all48_current_archive_gzip_current7_only_verified_twice=True,all_prior_failure_artifacts_retained_by_exact_retirement_scope=True,reviewer_Source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),Source_generation_executed=False,publisher_executed=False,worker_or_helpers_imported=False,compiler_executed=False,native_executed=False,B_native_executed=False,B_observation_context_produced=False,business_executed=False,compiled_or_SCI_or_gzip_bodies_opened=False,compiled_or_SCI_or_gzip_SHA_recomputed=False,PS_executed=False,files_deleted=False,numerical_executed=False,physics_qualified=False,scientific_accuracy_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()

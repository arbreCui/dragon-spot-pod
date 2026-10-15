"""Independent Source/metadata/current7 audit. Never import a candidate or reader.

No compiler/native/helper/fixture, scientific file, object, archive or runtime
payload is read or executed. Mathematical functions are compared as Source text.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

D=Path(__file__).absolute().parent.parent
P=Path(__file__).absolute().parent
SYSTEM=[]
START=time.monotonic()
def need(v,m):
    if v is not True:raise RuntimeError(m)
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
    q=Path(p['path']);s=q.lstat()
    fc=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256')=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and s.st_nlink==p['identity'][3]==2
    need(q.is_absolute() and stat.S_ISREG(s.st_mode) and (s.st_nlink==1 or fc) and ids(s)==p['identity'] and s.st_size==p['size_bytes'] and not any(x.is_symlink()for x in(q,*q.parents)),'exact current7 '+str(q))
    need(s.st_uid==os.getuid()or(s.st_uid==0 and p in SYSTEM),'only exact frozen original system roles')
def full(q):
    q=Path(q);s=q.lstat();need(s.st_size<8*2**20 and stat.S_ISREG(s.st_mode),'named small Source/JSON only')
    a=q.read_bytes();b=q.read_bytes();need(a==b and ids(s)==ids(q.lstat()),'small whole bytes stable twice')
    p=dict(path=str(q),sha256=hashlib.sha256(a).hexdigest(),size_bytes=len(a),identity=ids(s));current(p);return p
def meta(p):
    need(Path(p['path']).suffix=='.json' and full(p['path'])==p,'exact bounded JSON metadata fullPF')
    return json.loads(Path(p['path']).read_text())
def genuine(t,key,p,field):
    v=t[key];need(t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0 and type(v['exit_code'])is int and v['exit_code']==0 and v.get('session_id')is None and json.loads(v['output'].strip().splitlines()[-1])[field]==p,'genuine original closed0 exact artifact')
def unique(rows):
    t={}
    for p in rows:
        if p['path']in t:need(t[p['path']]==p,'same path completePF')
        t[p['path']]=p
    return t
def scan(q):
    q=Path(q)
    if not q.exists():return 0
    total=0
    for e in os.scandir(q):
        s=e.stat(follow_symlinks=False);need(not stat.S_ISLNK(s.st_mode),'no owning scope alias')
        if stat.S_ISDIR(s.st_mode):total+=scan(e.path)
        elif stat.S_ISREG(s.st_mode):total+=s.st_size
    return total
def segment(text,name):
    n=next(n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name)
    return ast.get_source_segment(text,n)
def constants(text,name):
    n=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
    return ast.literal_eval(n.value)
def main():
    global SYSTEM
    pa=full(D/'AUTHOR_SOURCE_FREEZE.json');need(pa['sha256']=='3a52b687e342c98dd945837a381b54b59a26e05fcb3965cab9d39e91f846d6fc','final author freeze')
    a=meta(pa);pp=a['plan_pin'];need(pp['sha256']=='55612b1ddebc16533b7979e5fcc04cdd3efc5ef70ca20b627d52d521da31d9d2','exact final PLAN');p=meta(pp)
    need(a['source_only']is True and a['core_writing_stopped']is True and a['compiler_native_decoder_scientific_payload_or_compression_executed_by_author']is False and a['complete_source_file_pins']==p['complete_source_file_pins'] and len(p['complete_source_file_pins'])==5,'exact four Python plus deck freeze')
    texts={}
    for x in p['complete_source_file_pins']:
        need(full(x['path'])==x,'all five Source wholebytes');name=Path(x['path']).name;texts[name]=Path(x['path']).read_text()
        if name.endswith('.py'):ast.parse(texts[name])
    need(p['complete_source_file_pins']==[p[k]for k in('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','exact_PACK_deck_Source_pin')]and a['source_pin']==p['host_source_pin'],'all five role identities including deck')
    inverse=meta(a['positive_core_and_reader_whole_inverse_pin']);meta(a['static_scope_resource_evidence_pin'])
    launcher=texts['open_exact_three_cold_archives_then_exec_Dragon.UNREADY.py'];reader=texts['complete18_independent_PACK_readback.UNREADY.py'];host=texts['run_A1_B2_A3_complete18_PACK_readonly_FD_Root_only.UNREADY.py'];contract=texts['production_PACK_FD_Source_contract.UNREADY.py'];deck=texts['pack_exact_A1_B2_A3_readonly_FD.UNREADY.x2m']
    oldFD=meta_source=inverse['original_fixture_launcher_Source_pin'];need(full(oldFD['path'])==oldFD,'actual tested FD Source pin');oldFDtext=Path(oldFD['path']).read_text()
    for name in inverse['exact_whole_positive_core_functions']:need(segment(launcher,name)==segment(oldFDtext,name),'whole tested positive FD core '+name)
    oldReader=inverse['original_full_context_readback_Source_pin'];need(full(oldReader['path'])==oldReader,'original mathematical reader Source');oldReaderText=Path(oldReader['path']).read_text()
    need(len(inverse['whole_math_functions'])==9,'whole nine mathematical functions')
    for name in inverse['whole_math_functions']:need(segment(reader,name)==segment(oldReaderText,name),'whole original readback mathematics '+name)
    restored=reader
    for edit in reversed(inverse['PACK_to_original_full_file_reverse_edits']):
        i=edit['new_offset'];v=edit['new_exact'];need(restored[i:i+len(v)]==v,'exact inverse fragment');restored=restored[:i]+edit['original_exact']+restored[i+len(v):]
    need(restored==oldReaderText,'entire reader whole file inverse')
    need('def transfer_readback('not in reader and reader.count('READ_CHECK()')==2 and 'MAX_READ_BYTES=1024*1024'in reader and 'mmap'not in reader.replace('no mmap',''),'only complete PACK reader, bounded pread checks, no GLOBAL stage')
    fr=meta(p['FD_control_Root_report_pin']);ft=meta(p['FD_control_Root_tools_pin']);fp=meta(p['FD_control_actual_post_pin']);fpt=meta(p['FD_control_actual_post_tools_pin'])
    genuine(ft,p['FD_control_actual_Root_return_field'],p['FD_control_Root_report_pin'],'report_pin');genuine(fpt,'actual_review_return',p['FD_control_actual_post_pin'],'review_pin')
    need(fr['status']=='PASS_NONSCIENTIFIC_GNU_STARTUP_READONLY_FD_EXEC_CONTRACT_CONTROLS_ONLY' and fr['failure']is None and fr['actual_child_integer_exit_codes']==[0,0,71,1,1] and fp['status']=='PASS_ACTUAL_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_ROOT0_WITH_EXACT_NEGATIVE_CHILD_CODES_METADATA_ONLY' and fp['failure']is None and fp['actual_Root_integer_exit_code']==0 and fp['actual_child_integer_exit_codes']==[0,0,71,1,1] and fp['negative_original_FAILED_records_preserved']is True,'real five FD controls0/post0, negative FAILED preserved')
    need(fp['actual_Host_report_pin']==p['FD_control_Root_report_pin']and fp['actual_Root_tools_pin']==p['FD_control_Root_tools_pin'] and p['actual_FD_control_Root0_and_independent_post0_closed']is True,'four real FD closure roles')
    rp=meta(p['runtime_actual_post_pin']);rpt=meta(p['runtime_actual_post_tools_pin']);genuine(rpt,'actual_review_return',p['runtime_actual_post_pin'],'review_pin')
    need(rp['status']=='PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION' and rp['failure']is None and rp['actual_child_integer_exit_codes']==[0,0,0,0] and rp['actual_new_Dragon_pin']==p['runtime_pin'] and rp['actual_original_owned_runtime_Root_integer_exit_code']==1,'actual new complete71 runtime0/post0, historical Root1 retained')
    cat=meta(p['selected27_catalog_pin']);need(cat['producers']==p['producers'] and len(cat['producers'])==3 and cat['selected_readonly_role_count']==27 and cat['new_B_bearing_formal_configuration_or_GLOBAL_RCON_compatibility_proved']is False,'actual selected27 catalog only')
    need([(x['plane'],x['material'],x['expected_case'])for x in cat['producers']]==[(1,'A','R64WARM-A-V1 '),(2,'B','R64WARM-B-V1 '),(3,'A','R64-A3-WARM1 ')]and [x['archive']for x in cat['producers']]==p['ordered_three_real_archive_full_pins'] and len({tuple(x['identity'][:2])for x in p['ordered_three_real_archive_full_pins']})==3,'three genuine independent ordered A1/B2/A3 archives')
    need(constants(launcher,'EXPECTED_CATALOG_PIN')==p['selected27_catalog_pin']and constants(launcher,'EXPECTED_RUNTIME_PIN')==p['runtime_pin'],'literal catalog/runtime exactPF authority')
    need("catalog_role=p==EXPECTED_CATALOG_PIN"in launcher and "((catalog_role and len(raw)==73816)or(not catalog_role and len(raw)<65536))"in launcher and p['selected27_catalog_pin']['size_bytes']==73816,'only exact 73816 catalog exception, manifest bound64K unchanged')
    need("ap.add_argument('--manifest-pin',required=True)"in launcher and "choices="not in launcher and "a.case"not in launcher and launcher.count('os.execv(')==1 and 'subprocess'not in launcher and 'os.fork('not in launcher,'positive production entry only, samePID exec and no extra child')
    expectedDeck="XSM_FILE PACK :: FILE './initial_pack.xsm' ;\nXSM_FILE RCON1 :: FILE './plane1_rcon.xsm' ;\nXSM_FILE RCON2 :: FILE './plane2_rcon.xsm' ;\nXSM_FILE RCON3 :: FILE './plane3_rcon.xsm' ;\nXSM_FILE A1 :: FILE '/dev/fd/101' ;\nXSM_FILE B2 :: FILE '/dev/fd/102' ;\nXSM_FILE A3 :: FILE '/dev/fd/103' ;\nMODULE APACKX64: END: ;\nPACK RCON1 RCON2 RCON3 := APACKX64: A1 B2 A3 :: ;\nECHO \"ACTUAL-A1-B2-A3-COMPLETE18-PACK-ONLY\" ;\nEND: ; QUIT \"LIST\" .\n"
    need(deck==expectedDeck and p['fixed_readonly_fd_numbers']==[101,102,103],'exact deck four fresh outputs plus three readonly FD operands')
    need(p['whole18_tree_fields']==['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND']and p['readback_per_slice_max_bytes']==2**20 and p['independent_Root_readback_stage_seconds']==600 and p['complete_resource_scan_interval_seconds']==5 and p['last_full_scan_time_recorded_after_completion']is True,'whole six fields times three, original reader budget')
    for fragment in ("full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start)","runner.execute(m.OUT/'pack','produce_complete18_PACK_only',cmd,600", "watch['command']==cmd==record['command']", "receipt['PID']==receipt['process_group']==watch['pid']",'rb.READ_CHECK=checkpoint', 'len(packed)==18', 'complete_RCON_tree=rb.exact_tree(a,route,b,b.root)', "resources.check();last_scan=time.monotonic()", "time.monotonic()-readback_started<600", "native[1:]==saved[1:]==(2,4)", "wrapper['***HANDLE***'][1:]==(28,4)", 'explicit_external_metadata_bytes=extra', 'open_unlinked_bytes=sum(unlinked.values())'):
        need(fragment in host,'complete existing guardian and readback gate '+fragment)
    need(host.count('runner.execute(')==1 and "whole five Source files including PACK deck frozen"in host and host.index("with(BASE/'ROOT_CONTROL_EXECUTION_CLAIM.json').open('x')")<host.index('initial(ps)')<host.index('spec.loader.exec_module(m)'),'claim precedes imports/body/sole child and full5 Source verified')
    roots=p['complete_joint_roots'];out=Path(p['planned_actual_output_root']);need(len(roots)==len(set(roots))==86 and roots==fr['complete_joint_roots']+[str(out)]and not os.path.lexists(out)and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'whole85 plus single fresh PACK86')
    caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
    need(p['original_caps']==caps and p['bounded_new_output_reservation_bytes']==512*2**20 and p['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and p['output512MiB_is_conditional_stricter_hardbound']is True and p['apack18_complete_output_size_is_not_assumed_from_old_AAA_bytes']is True,'conditional512 output plus Source8 and all original caps')
    build=meta(p['original_guard_build_plan_pin']);SYSTEM=build['readonly_system_SDK_header_pins']+build['readonly_system_tool_metadata_pins']+[build['C_compiler_pin']]
    ledger=unique(p['explicit_cumulative_metadata_file_pins']);need(all(ledger[x['path']]==x for x in fp['all69_external_compile_toolchain_full_pins'])and len(fp['all69_external_compile_toolchain_full_pins'])==69,'all69 external roles still exact in full ledger')
    live=unique(list(ledger.values())+p['retained_current7_pins']+p['retained_archive_metadata_current7_pins']+p['retained_B2_current_epoch_readonly_pins']+p['selected31_current_epoch_readonly_pins']+[p['runtime_pin']])
    cold=[x['current_epoch_full_pin']for row in cat['producers']for x in row['selected_readonly_roles']];need(len(cold)==27 and all(live[x['path']]==x for x in cold),'all27 exact real cold roles retained in counted current7 tables')
    for x in live.values():current(x)
    failed=p['retained_failed_v1_current7_only_pins']+p['retained_failed_pool_archive_current7_only_pins'];need(len(failed)==15 and all(set(x)=={'path','size_bytes','identity'}for x in failed),'failed8+7 remain stat3 only')
    for x in failed:current(x)
    need(p['exact59_historical_absent_pins']==fp['exact59_historical_absent_pins']and len(p['exact59_historical_absent_pins'])==59,'exact59 latest historical roles')
    for x in p['exact59_historical_absent_pins']:need(not os.path.lexists(x['path']),'only known absent history')
    for k,v in p.items():
        if k.startswith('future_actual_'):need(v is None,'future PACK actual role remains NULL')
    for k in('GLOBAL_or_PROJECT_produced','all_transitive_inputs_recertified','new_B_formal13_compatible','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(p[k]is False,'no future qualification')
    need(p['scientific_input_copies_authorized']is False and p['scientific_symlink_or_hardlink_aliases_authorized']is False and p['compiler_or_runtime_rebuild_authorized']is False and p['only_positive_production_launcher']is True,'no copies/aliases/rebuild/negative production mode')
    ptmpl=full(D/'ROOT_REVIEWABLE_CLI_PENDING_GENUINE_SOURCE_PEER0.json');tmpl=meta(ptmpl);argv=tmpl['argv'];need(len(argv)==20 and argv[:11]==p['original_complete_ENV_Python_B_prefix']and argv[11]==p['host_source_pin']['path']and json.loads(argv[13])==p['host_source_pin']and json.loads(argv[15])==pp and argv[16:]==['--Source-review-pin','__GENUINE_INDEPENDENT_SOURCE_REVIEW_FULL_PIN__','--Source-review-tools-pin','__GENUINE_INDEPENDENT_SOURCE_REVIEW_TOOLS_FULL_PIN__']and tmpl['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact20 Root argv only two peer placeholders')
    joint=sum(scan(x)for x in roots);extra=sum(x['size_bytes']for x in ledger.values()if not any(Path(x['path']).is_relative_to(Path(r))for r in roots));need(joint+extra+512*2**20+8*2**20<2*2**30 and scan(D)+150000<8*2**20,'stat-only whole86 plus full512+8 fit; original runtime resource class still mandatory')
    for x in p['complete_source_file_pins']:need(full(x['path'])==x,'final whole5 Source stable twice')
    result=dict(schema='INDEPENDENT_SOURCE_ONLY_A1_B2_A3_PACK_ONLY_FD_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD',source_only=True,failure=None,executor_task_name='/root/b2_build_source_peer',source_pin=p['host_source_pin'],plan_pin=pp,complete_source_file_pins=p['complete_source_file_pins'],author_freeze_pin=pa,Root_CLI_template_pin=ptmpl,actual_FD_control_Root_report_pin=p['FD_control_Root_report_pin'],actual_FD_control_Root_tools_pin=p['FD_control_Root_tools_pin'],actual_FD_control_post_pin=p['FD_control_actual_post_pin'],actual_FD_control_post_tools_pin=p['FD_control_actual_post_tools_pin'],real_FD_child_codes=[0,0,71,1,1],negative_FD_FAILED_records_preserved=True,actual_runtime_post_pin=p['runtime_actual_post_pin'],exact_runtime_pin=p['runtime_pin'],whole_positive_FD_core_three_functions_unchanged=True,whole_nine_readback_math_functions_unchanged=True,whole_reader_full_file_inverse_verified=True,exact_catalog_73816_role_only_and_manifest64K_verified=True,all_five_sources_including_deck_verified_twice=True,planned_complete_tree_count=18,planned_independent_RCON_tree_count=3,all_six_fields_all_three_planes_preserved=True,strict_case_plane_epoch_full_type4_keff_and_mirror_Source_checked=True,Root_bounded_readback_original_SELF512_whole1800_stage600_hooks_verified=True,fullscan_timestamp_after_completion=True,same_PID_positive_only_launcher_and_original_OwnRSS_Source_checked=True,no_negative_modes_or_extra_child_in_production_launcher=True,all27_real_cold_roles_current7_verified_without_body_read=True,complete_joint_roots=roots,original_caps=caps,conditional_output_bound_bytes=512*2**20,own_Source_bound_bytes=8*2**20,all69_external_compile_toolchain_bytes=36068911,complete_explicit_metadata_role_count=len(ledger),exact_historical_absent_count=59,retained_failed_stat3_count=15,current_stat_only_joint_bytes=joint,current_exact_explicit_external_bytes=extra,original_runtime_resource_class_executed_by_reviewer=False,candidate_executed=False,helper_executed=False,compiler_executed=False,native_executed=False,scientific_payload_body_read=False,object_or_runtime_body_read=False,PACK_produced=False,GLOBAL_or_PROJECT_produced=False,all_transitive_inputs_recertified=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,elapsed_review_seconds=time.monotonic()-START)
    q=P/'REVIEW.json'
    with q.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=full(q))),flush=True)
if __name__=='__main__':main()

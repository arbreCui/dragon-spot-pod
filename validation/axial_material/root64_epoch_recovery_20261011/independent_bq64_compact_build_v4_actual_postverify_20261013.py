import os,stat,json,hashlib,shlex,shutil
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
D=R/'bq64_compact_expected_build_host_source_v4_20261013'
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4')
O=R/'independent_bq64_compact_build_v4_actual_postverify_20261013'
cache={};checks=[]
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in ('path','sha256','size_bytes','identity')}
def ck(ok,n):
 if not ok:raise AssertionError(n)
 checks.append(n)
def pin(path):
 p=Path(path);i=ids(p.lstat())
 if not stat.S_ISREG(i[2]):raise AssertionError('ordinary actual input/output')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  if ids(os.fstat(f.fileno()))!=i:raise AssertionError('open7')
  sha=hashlib.file_digest(f,'sha256').hexdigest()
  if ids(os.fstat(f.fileno()))!=i:raise AssertionError('EOF7')
 if ids(p.lstat())!=i:raise AssertionError('after7')
 row=dict(path=str(p),sha256=sha,size_bytes=i[4],identity=i);cache[str(p)]=row;return row
def same(p):
 p=norm(p);actual=cache.get(p['path'])or pin(p['path'])
 if actual!=p:raise AssertionError('full EOF exactPF '+p['path'])
def read(p):
 pf=pin(p);raw=Path(p).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=pf['sha256']or ids(Path(p).lstat())!=pf['identity']:raise AssertionError('JSON after7')
 return json.loads(raw),pf

a,ap=read(OUT/'Root_actual_build_only_summary.json');hf,hp=read(D/'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json');plan,pp=read(D/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json');cli,cp=read(D/'ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json');tools,tp=read(R/'ROOT_ACTUAL_COMPACT_BQ_BUILD_V4_TRUE_TOOL_RETURNS_20261013.json')
ck(ap['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f'and ap['size_bytes']==2333640,'actual build4 summary exact wholeEOF SHA/size')
ck(a['schema']=='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'and a['status']=='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'and a['failure']is None and a['after_check_error']is None and a['secondary_failures']==[],'actual successful build-only schema/status no failures')
terminal=tools['actual_terminal_return'];ck(type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal['chunk_id']=='c2d939'and tools['actual_initial_return']['session_id']==97263,'genuine original c2d939 integer EXIT0 after session97263')
ck(shlex.split(tools['exact_executed_command'])==cli['argv'],'actual executed environment/Python/3completePF externalargv exact CLI')
ck(tools['reader_control_qualified']is False and tools['physics_qualified']is False,'real terminal tool receipt does not promote reader/physics')
ck(norm(a['actual_host_Source_freeze_pin'])==hp and norm(a['actual_new_Source_freeze_pin'])==norm(hf['selected_new_Fortran_Source_freeze_pin'])and norm(a['actual_new_Source_pin'])==norm(hf['new_production_Fortran_Source_pin']),'actual productionSource/SF/ownHF pins exact frozen inputs')
for p in (a['actual_new_Source_pin'],a['actual_new_Source_freeze_pin'],a['actual_host_Source_freeze_pin']):same(p)
ck(len(a['records'])==2 and [x['label']for x in a['records']]==['build/compile_BOOTQ','build/link_Dragon']and all(x['status']=='PASS'for x in a['records']),'only actual BOOTQ compile1 and full70 link1 stages bothPASS')
source=plan['planned_new_Source_path'];newobj=str(OUT/'build/SPOR64_BOOTQ64.o');newexe=str(OUT/'runtime/Dragon');compiler=plan['original_compiler_pin']['path'];includes=['-I'+str(OUT/'build'),*plan['original_compile_include_arguments']]
expected_compile=[compiler,*plan['original_compile_flags'],*includes,'-J'+str(OUT/'build'),'-c',source,'-o',newobj]
oldpaths=[p['path']for p in plan['original_ordered70_input_pins']];newpaths=list(oldpaths);newpaths[40]=newobj
ck(a['records'][0]['command']==expected_compile and a['records'][1]['command']==[compiler,'-O2','-ffp-contract=off',*newpaths,'-o',newexe],'actual original compiler/flags/includes exact; only newSource compile and ordered70 link')
ck(a['actual_complete70_link_inputs']==newpaths and a['original_ordered70_input_pins']==plan['original_ordered70_input_pins']and a['replacement_zero_based_complete70_input_index']==40,'actual complete70 exact original69 paths with onlyslot40 replaced')
ck(a['original_nine_core_object_pins']==plan['original_nine_core_object_pins']and all(a[k]is True for k in ('original69_other_inputs_identical_and_retained','original_four_archives_identical_and_retained','original_eight_unchanged_core_objects_identical_and_retained','old_nine_objects_retained_as_historical_premise')),'original69/full original9 oldpremise/core8/fourarchives retained')
for p in plan['original_ordered70_input_pins']+plan['original_nine_core_object_pins']:same(p)
ck(len(a['fixed_current_pins'])==2566 and len(a['output_pins'])==10,'actual fixed2566 / output10 complete declaration counts')
fixed={p['path']:norm(p)for p in a['fixed_current_pins']};outputs={p['path']:norm(p)for p in a['output_pins']}
ck(all(fixed.get(p['path'])==norm(p)for p in hf['dependencies'])and fixed.get(hp['path'])==hp,'actual build fixed every HF2565 dependency plusownHF')
for p in a['fixed_current_pins']+a['output_pins']+a['owned_runtime_pins']:same(p)
ck(True,'all fixed2566/output10/owned4 actual fullEOF SHA and all7 preserved')
actual_files={str(p)for p in OUT.rglob('*')if p.is_file()}
ck(actual_files==set(outputs)|{ap['path']} and all(not p.is_symlink()for p in OUT.rglob('*')),'entire actual OUT inventory exactly10 outputs plusfull summary no aliases')
qpin=outputs[newobj];dpin=outputs[newexe]
ck(qpin['size_bytes']==198368 and qpin['sha256'].startswith('1118ab3d')and dpin['size_bytes']==10744200 and dpin['sha256'].startswith('403e0a35')and qpin['identity'][3]==dpin['identity'][3]==1,'new actual BOOTQ andDragon ordinary single-link fullPF')
watch_pins=[]
for record,claimed in zip(a['records'],a['actual_watchdog_checks']):
 log=OUT/(record['label']+'.log');watch=log.with_suffix('.watchdog.json');w,wp=read(watch);watch_pins.append(wp);lp=pin(log)
 ck(lp['sha256']==record['log_sha256']and claimed['path']==str(watch)and claimed['sha256']==wp['sha256'],'actual closed stage log/watch wholeSHA exact')
 ck(type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['command']==record['command']and w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600 and 0<=w['elapsed_seconds']<600 and 0<=w['sampled_peak_rss_mib']<512 and w['own_child_only']is True and w['liveness_group_cleanup']is True,'actual stagewatch integer0/original600/512/owncleanup')
ck(a['original_guard_class']=='OwnRSSSerialExecutor'and a['original_guard_MRO_unchanged']is True and type(a['SELF_peak_bytes'])is int and 0<=a['SELF_peak_bytes']<512*2**20 and 0<a['wall_seconds']<1800,'actual originalOwnRSS guard/MRO/SELF512/whole1800')
ck(a['original_caps']==plan['original_caps']==hf['original_caps']and a['Dragon_linked']is True and a['final_report_resource_check_passed']is True,'actual caps exact original and published complete report resourcecheck passed')
for snapshot in [a['resources_before'],a['resources_after'],a['resources_after_including_summary_bytes']]+[x[k]for x in a['records']for k in ('resource_before','resource_after')]:
 ck(snapshot['artifact_budget_bytes']==96*2**30 and snapshot['min_free_bytes']==8*2**30 and snapshot['disk_free_bytes']>=8*2**30 and snapshot['artifact_bytes']+20971764748+64*2**20<96*2**30 and snapshot['fresh_output']['artifact_budget_bytes']==2*2**30 and snapshot['fresh_output']['artifact_bytes']<=2*2**30,'actual resource snapshots original history96/free8/cold/meta/fresh2')
ck(all(a[k]is False for k in ('transport_executed','new_entry_controls_executed','new_reader_control_qualification','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete')),'actual compile/link only; reader/physics/AAA/ABA qualification remains false')
rootpaths=a['resources_after_including_summary_bytes']['resource_roots'];total=0;count=0;stack=list(map(Path,rootpaths))
while stack:
 p=stack.pop()
 try:fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 except FileNotFoundError:continue
 try:
  with os.scandir(fd)as entries:
   for e in entries:
    s=e.stat(follow_symlinks=False)
    if stat.S_ISDIR(s.st_mode):stack.append(p/e.name)
    elif stat.S_ISREG(s.st_mode):total+=s.st_size;count+=1
 finally:os.close(fd)
current_free=shutil.disk_usage(OUT).free;remaining=96*2**30-total-20971764748-64*2**20-2*2**30
ck(remaining>0 and current_free>=8*2**30,'independent current family history originalfullfresh2 reserve remainspositive/free8')
for p in cache.values():
 if ids(Path(p['path']).lstat())!=p['identity']:raise AssertionError('final all current7 '+p['path'])
report=dict(schema='INDEPENDENT_ACTUAL_COMPACT_BQ_BUILD_V4_READONLY_POSTVERIFY_V1',status='PASS_ACTUAL_COMPACT_BQ_BUILD_V4_COMPILE1_LINK70_CLOSED0_ONLY',failure=None,actual_build_report_pin=ap,actual_new_build_report_pin=ap,actual_build_true_tool_return_pin=tp,actual_new_BOOTQ_object_pin=qpin,actual_new_Dragon_pin=dpin,actual_Host_freeze_pin=hp,actual_build_PLAN_pin=pp,actual_build_CLI_pin=cp,actual_Source_freeze_pin=norm(a['actual_new_Source_freeze_pin']),actual_production_Source_pin=norm(a['actual_new_Source_pin']),actual_watchdog_pins=watch_pins,actual_genuine_terminal_integer_exit_code=terminal['exit_code'],actual_stage_count=2,actual_fixed_fullEOF_pin_count=2566,actual_output_fullEOF_pin_count=10,original69_core8_fourarchives_fullEOF_all7_unchanged=True,original_guards_caps_and_firstfailure_no_further_failures=True,actual_current_family_bytes=total,actual_current_family_regular_files=count,actual_current_free_bytes=current_free,actual_current_fullfresh2_original_reserve_remaining_bytes=remaining,readonly=True,source_only=False,Host_imported=False,Host_main_executed=False,compiler_executed_by_this_reviewer=False,numerical_executed=False,business_executed_by_this_reviewer=False,deletion_executed=False,released_targets_opened=False,reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,all_file_descriptors_closed=True,checks=checks)
O.mkdir();p=O/'REVIEW.json';p.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n');rp=pin(p)
print(json.dumps(dict(status=report['status'],failure=None,review_pin=rp,actual_build_report_pin=ap,actual_new_BOOTQ_object_pin=qpin,actual_new_Dragon_pin=dpin,actual_genuine_terminal_integer_exit_code=terminal['exit_code'],all_file_descriptors_closed=True),ensure_ascii=False))

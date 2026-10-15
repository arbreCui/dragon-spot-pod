import os,stat,json,hashlib,shlex
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v2')
D=R/'bq64_compact_expected_connected17_host_source_v2_20261013'
O=R/'independent_fresh17_compact_BQ_v2_actual_postverify_20261013'
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
 if actual!=p:raise AssertionError('fullPF '+p['path'])
def read(path):
 pf=pin(path);raw=Path(path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=pf['sha256']or ids(Path(path).lstat())!=pf['identity']:raise AssertionError('JSON after7')
 return json.loads(raw),pf

a,ap=read(OUT/'Root_actual_connected17_summary.json');hf,hp=read(D/'COMPLETE_FRESH17_NEW_BOOTQ_HOST_SOURCE_FREEZE.json');cli,cp=read(D/'ROOT_REVIEWABLE_EXACT_FRESH17_ARGV.json');t,tp=read(R/'ROOT_ACTUAL_FRESH17_V2_NEW_COMPACT_BQ_TRUE_TOOL_RETURNS_20261013.json');oracle,op=read(a['original_current17_oracle_pin']['path']);base,bp=read(a['actual_new_build70_report_pin']['path'])
ck(ap['sha256']=='7809453e0ebc8350ba3c4e8d47078795485527913f8b174e5c0817a0eba42cde'and ap['size_bytes']==9091563,'actual fresh17 summary exact fullEOF SHA/size')
ck(a['schema']=='ACTUAL_BQ64_COMPACT_EXPECTED_FRESH_CONNECTED17_COMPONENT_CONTROLS_V1'and a['status']=='ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY'and a['failure']is None and a['after_check_error']is None and a['secondary_failures']==[],'actual new17 successful closed0 component-only no errors')
tr=t['actual_terminal_return'];ck(type(tr['exit_code'])is int and tr['exit_code']==0 and tr['chunk_id']=='5adf13'and t['actual_initial_return']['session_id']==37513,'genuine real5adf13 originalinteger0 aftersession37513')
ck(shlex.split(t['exact_executed_command'])==cli['argv'],'actual executed CLI argv environment/Python/external3PF exact')
ck(norm(a['actual_host_Source_freeze_pin'])==hp and hp['sha256']=='88db202f3eebb22578b6f58a91050a41acaf0de35ba2e0718a5ba49a9deb3a89'and norm(hf['selected_actual_new_build70_report_pin'])==bp and bp['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f','actual fresh17 ownHF88db and sameactualnewbuild741')
ck(norm(a['genuine_production_new_BOOTQ_object_pin'])==next(norm(p)for p in base['output_pins']if p['path'].endswith('/SPOR64_BOOTQ64.o'))and a['genuine_production_new_BOOTQ_object_pin']['sha256']=='1118ab3d4b705d3732914aa2bd774919a173c24c20ff932cfd7650f35d51e574','same genuine newQ1118 complete actualPF')
same(a['genuine_production_new_BOOTQ_object_pin']);same(a['actual_current_control_source_pin']);ck(a['actual_current_control_source_pin']['sha256']=='1b782030e20d4a254052937fd37ff6ef0e145969604e6ef6d365957ea29a9af3','current actual originalfactory1b78 full sourceEOF unchanged')
for row in base['fixed_current_pins']+base['output_pins']:same(row)
for row in a['fixed_current_pins']+a['output_pins']:same(row)
fixed={p['path']:norm(p)for p in a['fixed_current_pins']};outputs={p['path']:norm(p)for p in a['output_pins']}
ck(len(fixed)==len(a['fixed_current_pins'])==2587 and len(outputs)==len(a['output_pins'])==47 and all(fixed.get(p['path'])==norm(p)for p in hf['dependencies'])and fixed[hp['path']]==hp,'actual completefixed2587/output47 and wholeHF2586 fullEOF SHA all7 preserved')
ck({str(p)for p in OUT.rglob('*')if p.is_file()}==set(outputs)|{ap['path']}and all(not p.is_symlink()for p in OUT.rglob('*')),'entire actualOUT exactly47 outputs plusfull summary; no aliases')
oldcompile=list(oracle['planned_compile_command']);oldout=oracle['planned_output_root'];newmain=str(OUT/'build/test_ROOT64_full_connected17.o');newexe=str(OUT/'build/full_connected17_unqualified');newq=a['genuine_production_new_BOOTQ_object_pin']['path']
at=next(i for i,v in enumerate(oldcompile)if v.startswith('-I'));oldcompile.insert(at,'-I'+str(Path(newq).parent));compile=[('-J'+str(OUT/'build'))if v=='-J'+oldout+'/build'else v for v in oldcompile];compile[-1]=newmain
oldlink=list(oracle['planned_link_command']);inputs=oldlink[3:-2];newinputs=list(inputs);newinputs[0]=newmain;newinputs[3]=newq;link=[*oldlink[:3],*newinputs,'-o',newexe];commands=[compile,link,*[[newexe,*x[1:]]for x in oracle['planned_run_commands']]]
ck(len(a['records'])==20 and [x['command']for x in a['records']]==commands and [x['label']for x in a['records']]==['build/control_'+str(i)for i in range(20)]and all(x['status']=='PASS'for x in a['records']),'all actual20 exact compile/link+18 original case-phase commands/pass/order')
ck([i for i,(x,y)in enumerate(zip(inputs,newinputs))if x!=y]==[0,3]and all(x in base['actual_complete70_link_inputs']for x in newinputs[1:]),'only controlmain andnewQ replace; other8 cores+4 archives sameactual70')
watchpins=[];casevalues=[]
for i,(record,claimed)in enumerate(zip(a['records'],a['actual_watchdog_checks'])):
 log=OUT/(record['label']+'.log');lp=pin(log);w,wp=read(log.with_suffix('.watchdog.json'));watchpins.append(wp)
 ck(lp['sha256']==record['log_sha256']and wp['path']==claimed['path']and wp['sha256']==claimed['sha256'],'actual stage'+str(i)+' complete logfile/watch SHA exact')
 ck(type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['command']==record['command']and w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600 and 0<=w['elapsed_seconds']<600 and 0<=w['sampled_peak_rss_mib']<512 and w['own_child_only']is True and w['liveness_group_cleanup']is True,'actual stage'+str(i)+' integer0/600/512/ownliveness cleanup')
 if i>=2:
  rows=[json.loads(s)for s in log.read_text().splitlines()];ck(len(rows)==2,'actual phase two terminalJSON rows only')
  assertion,counts=rows;command=record['command'];case=command[1];phase=command[2]if len(command)==3 else'single'
  ck(all(x['case']==case and x['phase']==phase for x in rows)and assertion['all_actual_assertions_completed']is True and assertion['synthetic_fixture']is True and all(assertion[k]is False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')),'actual phase exactcase/phase/assertions synthetic precise scope')
  decl=next(x for x in oracle['declared_case_oracles']if x['case']==case)
  for key,value in decl.items():
   if key.startswith(('expected_actual_','expected_explicit_')):
    observed=counts[key[9:]]
    if type(observed)is not int or observed!=value:raise AssertionError('exact original17 integer oracle '+case+' '+key)
  casevalues.append(dict(case=case,phase=phase,assertions=assertion,actual_statuses_and_call_counts=counts))
ck(casevalues==a['actual_cases']and len(casevalues)==18 and len({x['case']for x in casevalues})==17 and a['actual_logical_control_count']==17 and a['actual_run_phase_count']==18 and a['all17_original_names_exercised']is True and a['old_seventeen_PASS_inherited']is False,'actual18 raw logs/all integer status-count oracles equalactual17 summary; notoldPASS inherited')
e=a['actual_independent_host_coherent_refusal'];mf,mp=read(a['independent_coherent_baseline_manifest_pin']['path']);ck(mp==norm(a['independent_coherent_baseline_manifest_pin'])and mf['schema']=='INDEPENDENT_HOST_COHERENT_BASELINE_FULL_FILE_BINDING_V1'and norm(mf['actual_before_pin'])==norm(e['before']),'real coherentprepare baseline manifest wholeEOF exactbeforePF retained')
ck(e['actual_refused']is True and e['Fortran_internal_refusal_claimed']is False and e['actual_original_Host_gate']=='same_pin'and e['before']['path']==e['after']['path']and e['before']['sha256']!=e['after']['sha256']and e['before']['identity']!=e['after']['identity']and e['before']['identity'][:5]==e['after']['identity'][:5],'actual coherent samefile rewrite changes bytes/time; independent owning Host fullPF refusal only')
same(e['after']);ck('current fullEOF SHA/7ID differs:'in e['actual_refusal_error']and e['after']['path']in e['actual_refusal_error'],'real original same_pin refusal error names actualchanged file')
ck(fixed.get(mp['path'])==mp or outputs.get(mp['path'])==mp,'retained baseline manifest current outputPF protected')
ck(a['original_guard_class']=='OwnRSSSerialExecutor'and a['original_guard_MRO_unchanged']is True and type(a['SELF_peak_bytes'])is int and 0<=a['SELF_peak_bytes']<512*2**20 and 0<a['wall_seconds']<1800 and a['final_report_resource_check_passed']is True,'actual originalOwnRSS/MRO/SELF512/whole1800 complete summary resourcecheck')
for s in [a['resources_before'],a['resources_after'],a['resources_after_including_summary_bytes']]+[x[k]for x in a['records']for k in ('resource_before','resource_after')]:
 if not(s['artifact_budget_bytes']==96*2**30 and s['min_free_bytes']==8*2**30 and s['disk_free_bytes']>=8*2**30 and s['artifact_bytes']+20971764748+64*2**20<96*2**30 and s['fresh_output']['artifact_budget_bytes']==2*2**30 and s['fresh_output']['artifact_bytes']<=2*2**30):raise AssertionError('all actualcaps originalhistory96/free8/cold/meta/fresh2')
ck(True,'all actual resource stage/publication snapshots preserve original96/8/cold/meta/fresh2')
ck(a['other_eight_core_objects_and_original_oracles_unchanged']is True and all(a[k]is False for k in ('new_private_model_controls_qualified','new_extra_public_READ_controls_qualified','production_reader_admitted','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete')),'actualnew17 only syntheticprotocol; private/newpublic7/reader/physics/AAA qualification remainsfalse')
for p in cache.values():
 if ids(Path(p['path']).lstat())!=p['identity']:raise AssertionError('final all fullEOF/current7 '+p['path'])
report=dict(schema='INDEPENDENT_ACTUAL_FRESH17_NEW_COMPACT_BQ_V2_READONLY_POSTVERIFY_V1',status='PASS_ACTUAL_FRESH17_NEW_COMPACT_BQ_V2_20STAGES_17CONTROLS_18PHASES_CLOSED0_ONLY',failure=None,actual_fresh17_report_pin=ap,actual_fresh17_true_tool_return_pin=tp,actual_host_freeze_pin=hp,actual_cli_pin=cp,actual_new_build70_report_pin=bp,genuine_new_BOOTQ_object_pin=norm(a['genuine_production_new_BOOTQ_object_pin']),actual_current_original_factory_Source_pin=norm(a['actual_current_control_source_pin']),actual_current17_oracle_pin=op,actual_coherent_baseline_manifest_pin=mp,actual_coherent_rewritten_file_pin=norm(e['after']),historical_coherent_before_pin_not_current=norm(e['before']),actual_original_Host_coherent_refusal=e,actual_genuine_terminal_integer_exit_code=tr['exit_code'],actual_guarded_stage_count=20,actual_logical_control_count=17,actual_run_phase_count=18,actual_raw_integer_status_and_callcount_oracles_verified=True,actual_fixed_fullEOF_pin_count=2587,actual_output_fullEOF_pin_count=47,all_original_eight_core_and_archives_fullEOF_all7_unchanged=True,all_file_descriptors_closed=True,readonly=True,source_only=False,Host_imported=False,Host_main_executed=False,compiler_executed_by_this_reviewer=False,numerical_executed_by_this_reviewer=False,business_executed_by_this_reviewer=False,deletion_executed=False,released_or_deleted_stale_targets_opened=False,production_reader_admitted=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,checks=checks)
O.mkdir();p=O/'REVIEW.json';p.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n');rp=pin(p)
print(json.dumps(dict(status=report['status'],failure=None,review_pin=rp,actual_fresh17_report_pin=ap,actual_genuine_terminal_integer_exit_code=tr['exit_code'],all_file_descriptors_closed=True),ensure_ascii=False))

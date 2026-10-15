from pathlib import Path
import ast,hashlib,json,os,resource,stat,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';S=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_source_v2';A=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_v2_author_review_20261013';D=REC/'independent_single_pair_rank_type_v2_source_review_20261013';START=time.monotonic();checks=[];full={};bytes_read=0
def req(x,msg):
 assert type(x)is bool and x,msg;checks.append(msg)
 if time.monotonic()-START>=1800 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original independent source review whole1800/SELF512')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,expected=None):
 global bytes_read
 p=Path(p);before=identity(p.lstat());req(stat.S_ISREG(before[2])and before[0]==16777229,'ordinary currentDEV29 '+str(p))
 if expected is not None:req(before==expected['identity'],'all7 before '+str(p))
 if str(p)in full:
  q=full[str(p)];req(q['identity']==before and(expected is None or q==expected),'same currentPF cached after realEOF');return q
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  req(identity(os.fstat(fd))==before,'sameFD opened7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
  req(identity(os.fstat(fd))==before,'sameFD wholeEOF7')
 finally:os.close(fd)
 req(identity(p.lstat())==before and n==before[4],'pathEOF7 andsize')
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=before);req(expected is None or q==expected,'exact complete physicalPF '+str(p));full[str(p)]=q;bytes_read+=n;return q
def read(p):
 q=pin(p);b=Path(p).read_bytes();req(hashlib.sha256(b).hexdigest()==q['sha256']and identity(Path(p).lstat())==q['identity'],'complete savedJSON unchanged');return json.loads(b)
handoff=read(A/'FINAL_FROZEN_SOURCE_HANDOFF.json');req(pin(A/'FINAL_FROZEN_SOURCE_HANDOFF.json')['sha256']=='cdb6a3011c97e2262d1a69a75c68ebe07f745a029448dc052b9c8df8dc14da7a','author actual frozen handoff exact SHA')
for p in handoff['all_Source_tree_pins']+[handoff[k]for k in('CLI_pin','author_review_pin','host_freeze_pin')]:pin(p['path'],p)
hf=read(S/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json');req(pin(S/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json')['sha256']=='f7fd76012ce6a568157ff1781b90ec38986dc2c6384639d7a761ccc10462ee55','realv2HF exactSHA')
req(len(hf['dependencies'])==2811,'full2811 diagnosticdependencies')
for p in[hf['host_source']]+hf['source_files']+hf['dependencies']:pin(p['path'],p)
authority=read(S/'INPUT_AUTHORITY.json');plan=read(S/'PLAN_SOURCE_ONLY.json');inv=read(S/'COMPLETE_ORIGINAL_FRAGMENT_BYTE_INVERSE.json');cli=read(A/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json')
for p in[x['source_pin']for x in authority['inputs']]+[authority['old_raw_record_pin'],authority['old_stage_ledger_pin'],authority['exact_original_deck_pin'],inv['original_host_pin']]:pin(p['path'],p)
catalog_path=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json';catalog=read(catalog_path);req(len(catalog['rows'])==3040,'completecurrentcatalog3040')
for row in catalog['rows']:
 a=row['historical_pin'];b=row['current_pin'];req(a['identity'][0]in(16777234,16777229)and b['identity'][0]==16777229 and a['identity'][1:]==b['identity'][1:]and a['sha256']==b['sha256']and a['path']==b['path'],'onlydevicecatalogtransition');pin(b['path'],b)
compiler=dict(path='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15',sha256='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492',size_bytes=2648040,identity=[16777229,1171728,33133,2,2648040,1754637485000000000,1778162641926218060])
for q in full.values():req(q['identity'][3]==1 or q==compiler,'soleexactcompiler immutable_nlink2 role')
hostpath=Path(hf['host_source']['path']);host=hostpath.read_text();old=Path(inv['original_host_pin']['path']).read_text();tree=ast.parse(host);ot=ast.parse(old)
def fn(t,name):return next(n for n in ast.walk(t)if isinstance(n,ast.FunctionDef)and n.name==name)
def body(text,node):return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
Phase=next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources');oPhase=next(n for n in ot.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources')
req(body(host,Phase)==body(old,oPhase),'original completePhaseResources byteexact')
req(inv['original_PhaseResources_complete_text']==inv['diagnostic_PhaseResources_complete_text'],'savedPhase inversewholetext equal')
admission=inv['diagnostic_admission'];req(admission in host and inv['original_admission']in old,'savedcompleteadmission matches genuine Sourcebodies')
recovered=admission
for anchor,insert in inv['monitor_only_insertions']:
 req(recovered.count(anchor+insert)==1,'eachmonitorcheckpoint exactsinglecontext');recovered=recovered.replace(anchor+insert,anchor)
for a,b in inv['admission_exact_owner_replacements']:
 req(recovered.count(b)==1,'each exactownerliteral');recovered=recovered.replace(b,a)
req(recovered==inv['original_admission'],'alladmissionbytes inverseoriginal owner2+8checkpoints only')
for name in ('stable','retain','copy','clean_driver_scratch_before','stash_closed_driver_scratch'):
 a=body(old,fn(ot,name));b=body(host,fn(tree,name));normalized=''.join(('  '+line)if line.strip()else line for line in b.splitlines(keepends=True));req(normalized==a,'entire original nestedfunction onlyindent−2 '+name)
raw=read(authority['old_raw_record_pin']['path']);ledger=read(authority['old_stage_ledger_pin']['path']);req(len(raw['records'])==45 and ledger=={'stages':raw['records']},'true complete45 originalresource records')
req(raw['failure']=='RuntimeError: original SELF 512MiB cap'and raw['engineering_three_plane_closed0']is False and raw['actual_terminal']is None,'failedv11neverreclassified')
req(len(raw['fixed_current_pins'])==2643 and len(raw['owned_runtime_pins'])==163,'fulloriginalfixed2643+oldowned163')
for q in raw['fixed_current_pins']+raw['owned_runtime_pins']:pin(q['path'],q)
req(len(authority['inputs'])==12 and len({x['destination_name']for x in authority['inputs']})==12,'exact12unambiguous inputroles')
req(all(x['source_pin']in raw['owned_runtime_pins']for x in authority['inputs']),'allselected12actually retained oldcurrentowned inputs')
deck=Path(authority['exact_original_deck_pin']['path']).read_text();req(authority['expected_abort']=='SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.','exactexpectedabort')
req('RANK 1.0 EDIT 0'in deck and all(len(x.rstrip())<=120 for x in deck.splitlines()),'originalrank_typeCLE exactlinewidth')
req(sum(x['source_pin']['size_bytes']for x in authority['inputs'])==plan['base_input_bytes']==812951170,'actualfixedinputbytes')
req(plan['nonPROJECT_input_bytes']==63595218 and plan['nonPROJECT_planning_room_before_evidence_bytes']==128*2**20-63595218,'realplanning128 residual+PROJECT800; no caprelax')
req(plan['actual_new_stages']==1 and plan['unmodified_historical_prefix_count']==45 and plan['new_stage_index']==45,'old45historical/new1 contract')
req(hf['future_actual_report_pin']is None and plan['future_actual_report_pin']is None and cli['future_actual_report_pin']is None and handoff['actual_executed']is False,'no futurebusinessPF/prequalifiedstatus')
expected=read(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json')['mandatory_external_bindings'];req(hf['original_v11_external_bindings']==expected==cli['all_seven_original_external_bindings'],'all7unchanged realexternalreportfullPF')
argv=cli['argv'];flags={argv[i]:argv[i+1]for i in range(len(argv)-1)if argv[i].startswith('--')}
for name,q in expected.items():
 req(flags['--'+name+'-summary']==q['path']and flags['--'+name+'-sha256']==q['sha256']and json.loads(flags['--'+name+'-seven-id'])==q['identity'],'CLIexactoriginalexternal '+name);pin(q['path'],q)
req(flags['--diagnostic-freeze-summary']==handoff['host_freeze_pin']['path']and flags['--diagnostic-freeze-sha256']==handoff['host_freeze_pin']['sha256']and json.loads(flags['--diagnostic-freeze-seven-id'])==handoff['host_freeze_pin']['identity'],'CLIownrealHF exactSHAall7')
req(argv[:3]==['/usr/bin/env','-u','PYTHONOPTIMIZE']and '-B'in argv and all(k+'=1'in argv for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE')),'originalunprofiled1threadCLIenv')
main=fn(tree,'main');maintext=body(host,main);req(maintext.count('runner.execute(')==1 and not any(isinstance(n,ast.Call)and ast.unparse(n.func).endswith('_process')for n in ast.walk(main)),'soleoriginalexecute nosecondactororretry')
req("runner.execute(WORK,'pair_rank_type',[str(OUT/'runtime/Dragon')],600,deck=deck.name)"in maintext,'exactoneactualoriginalstage600')
req("runner.records=list(historical_raw['records']);historical_prefix_installed=True"in maintext and "runner.records[:45]!=historical_raw['records']"in maintext and "dumped!={'stages':runner.records}"in maintext,'shared historicalrowsunmodified appendonly1 original46serialized')
req("full.OwnRSSSerialExecutor.__bases__!=(full.SerialExecutor,)"in maintext and 'runner.resources is not resources'in maintext,'genuineparentbaseMRO/resources binding')
common=Path(REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py').read_text();req("full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)"in common and 'full,production=helper.modules()'in common,'actualCommon initialize validates production.SerialExecutor/paths so full.SerialExecutor bindinggenuine')
req("child_error!='RuntimeError: own-child stage failed; no retry'"in maintext and "record.get('error')!='own-child stage failed; no retry'"in maintext and "type(w['returncode'])is not int or w['returncode']!=1"in maintext,'preciserefusal genuineexit1recorderror')
req("text.count(authority['expected_abort'])!=1"in maintext and 'any(x in text for x in forbidden)'in maintext and 'no_positive_solver_or_seal_trace=True'in maintext,'singleexactabort pretransport noforbiddentraces')
req('created_OUT=False'in maintext and 'historical_prefix_installed=False'in maintext and 'OUT.mkdir();created_OUT=True'in maintext,'ownership created onlyafteractualmkdir; historyflagexplicit')
req(maintext.count('if created_OUT:')==2,'outputinventoryandpublicationbothownedonly')
created_ifs=[n for n in ast.walk(main)if isinstance(n,ast.If)and ast.unparse(n.test)=='created_OUT'];req(any(any(isinstance(q,ast.Call)and ast.unparse(q.func)=='os.open'for q in ast.walk(n))for n in created_ifs),'reportosopen beneathcreatedOUT gate')
req("new_actual_stage_count=0 if not historical_prefix_installed else len(runner.records)-45"in maintext,'noearlynegative newstagecount')
outer=next(n for n in main.body if isinstance(n,ast.Try));req(any('first_error=type(exc).__name__'in body(host,n)for n in outer.handlers),'primaryfailurecaptured outsidefinally')
finaltext=''.join(body(host,n)for n in outer.finalbody);req('first_error='not in finaltext,'finallyneverreassignsfirsterror')
req("resources.pending_publication_reserved_bytes=8*MI"in finaltext and "os.O_CREAT|os.O_EXCL|os.O_RDWR"in finaltext and "after_errors.append('after report write: '"in finaltext,'actual8MiBreserve+ownedexclusiveFD finalfailure path')
req("report['status']='SINGLE_PRETRANSPORT_DIAGNOSTIC_FAILED_EVIDENCE_RETAINED'"in finaltext and 'initial_id'in finaltext and 'stream.truncate(0)'in finaltext,'sameFD honestlatefailurepublication')
req('time.monotonic()-START>=1800'in finaltext and 'ru_maxrss>=512*MI'in finaltext and 'raise SystemExit(1)'in finaltext,'finalpostwriteoriginalwhole/SELFcaps+honestexit1')
req('old45_reexecuted=False'in maintext and 'old45_counted_as_new_PASS=False'in maintext and 'original_v11_closed50_succeeded=False'in maintext and 'engineering_qualified=False'in maintext,'no50orphysicsqualification')
req(not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('unlink','rmtree','remove')for n in ast.walk(tree)),'candidatehasnodatadeletion')
req(not any(isinstance(n,ast.Assign)and any(isinstance(t,ast.Attribute)and ast.unparse(t)in('resource.getrusage','full.OwnRSSSerialExecutor','production.SerialExecutor','runner.execute','resources.check')for t in n.targets)for n in ast.walk(tree)),'nopatchguards/classes/rusage/executor/resources')
req("ps=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())]"in host and 'resource.getrusage(resource.RUSAGE_SELF).ru_maxrss'in host and 'while not STOP.wait(.2)'in host,'realselfmonitor .2seconds nofakeresource')
output=Path(hf['own_future_output']);req(str(output)in host and str(output)==plan['planned_output']and not os.path.lexists(output),'freshactualdiagnosticOUT absent Sourceonly')
for p in S.iterdir():
 if p.is_file():pin(p)
for q in full.values():req(identity(Path(q['path']).lstat())==q['identity'],'all inputs all7 stable atfinal')
report=dict(schema='INDEPENDENT_COMPLETE_SINGLE_PAIR_RANK_TYPE_V2_SOURCE_ONLY_REVIEW_V1',status='SOURCE_ONLY_FINITE_REVIEW_PASS_READY_FOR_ROOT_AUTHORIZED_SINGLE_DIAGNOSTIC_ONLY',check_count=len(checks),unique_current_full_EOF_files=len(full),unique_current_full_EOF_bytes=bytes_read,all_verified_current_fullpins=list(full.values()),frozen_author_handoff_pin=pin(A/'FINAL_FROZEN_SOURCE_HANDOFF.json'),key_host_freeze_pin=pin(S/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json'),key_CLI_pin=pin(A/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json'),complete_original_ownership2_monitor8_admission_byteinverse_verified=True,all5original_nestedfunction_indentonly_wholeinverse_verified=True,original_PhaseResources_fullbyte_identical=True,all12readonly_inputs_currentfullPF=True,historical45_unmodified_only_new1_diagnostic=True,actual_original_MRO_Common_production_binding_verified=True,createdOUTownership_and_earlyfailure_count_guards_verified=True,primary_vs_after_errors_and_ownedFD_failurepublisher_verified=True,alloriginalcaps_currentpins_and_expectedexit1_oracle_verified=True,all_checks=checks,future_actual_business_report_pins_not_predicted=True,candidate_imported=False,guard_Dragon_or_numericbusiness_executed=False,cleanup_executed=False,Source_modified=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-START,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
D.mkdir()
with(D/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],checks=len(checks),unique_EOF=len(full),unique_bytes=bytes_read,SELF=report['SELF_peak_bytes'],wall=report['wall_seconds'],review_pin=pin(D/'REVIEW.json'))))

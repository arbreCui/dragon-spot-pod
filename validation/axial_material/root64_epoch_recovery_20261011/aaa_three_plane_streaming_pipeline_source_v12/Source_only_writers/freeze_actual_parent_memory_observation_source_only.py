"""Freeze actual Source only. No candidate import, compiler or business."""
import ast, copy, hashlib, json, os, resource, stat, time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'aaa_three_plane_streaming_pipeline_source_v11'
NEW=Path(__file__).absolute().parent.parent
START=time.monotonic();PINS={};CHECKS=[]
COMPILER=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
def need(ok,message):
    if not ok:raise RuntimeError(message)
    CHECKS.append(message)
def identity(path):
    s=Path(path).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);before=identity(path)
    need(stat.S_ISREG(before[2]) and not any(p.is_symlink()for p in(path,*path.parents)),'regular literal fullEOF Source/input')
    need(before[3]==1 or(path==COMPILER and before[3]==2),'owned1 or exact existing compiler2')
    with path.open('rb')as f:
        s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before,'opened all7 unchanged')
        digest=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(path),'fullEOF all7 unchanged')
    row=dict(path=str(path),sha256=digest,size_bytes=before[4],identity=before)
    need(str(path)not in PINS or PINS[str(path)]==row,'one unchanged fullpin per path');PINS[str(path)]=row
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-START>=1800:raise RuntimeError('original Source SELF512/whole1800')
    return row
def verify(row):need(pin(row['path'])==row,'actual current fullpin exactly selected')
def read(path):
    row=pin(path);raw=Path(path).read_bytes();need(hashlib.sha256(raw).hexdigest()==row['sha256']and identity(path)==row['identity'],'metadata currentEOF unchanged');return json.loads(raw),row
def save(path,raw):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def write(path,value):save(path,(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())

oldhf,oldhfp=read(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
oldcli,oldclip=read(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json')
need(len(oldhf['dependencies'])==308,'complete actual predecessor308 dependencies')
for row in oldhf['dependencies']+[oldhf['host_source']]+list(oldcli['mandatory_external_bindings'].values()):verify(row)
draft,draftpin=read(NEW/'UNFROZEN_EXACT_V11_TO_V12_OBSERVATION_DELTA_DRAFT.json')
oldhost=Path(oldhf['host_source']['path']).read_bytes();candidate=(NEW/'run_actual_three_plane_pipeline.py').read_bytes()
restored=candidate.decode()
for delta in reversed(draft['changes']):
    need(delta['count']==1 and restored.count(delta['new_block'])==1,'one exact authorized insertion block')
    restored=restored.replace(delta['new_block'],delta['old_block'],1)
need(restored.encode()==oldhost,'ENTIRE v11 host bytes inverse, no hidden change')
tree=ast.parse(candidate);oldtree=ast.parse(oldhost)
collect=lambda t:[n for n in ast.walk(t)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='gc'and n.func.attr=='collect']
need(len(collect(tree))==len(collect(oldtree))==1,'only original admission GC, no extra GC')
need(not any(isinstance(n,(ast.AsyncFunctionDef,ast.Await))for n in ast.walk(tree)),'main single thread no async observer')
need(not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('setrlimit','settrace','setprofile','Thread','reset_peak')for n in ast.walk(tree)),'no Thread profiling guard or peak patch')
need('self.late[-8:]'in candidate.decode()and 'len(raw)>8192'in candidate.decode(),'explicit bounded8 scalar late tail and8192 byte refusal')
need('except BaseException as original_late_exc:'in candidate.decode()and 'raise RuntimeError(failure or after_error)'in candidate.decode(),'existing primary wins over observer failure')
mapped_names={'actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90','DIRECT_ALIAS_ENTRY_BINDING.json','DECLARED_EXECUTION_INTERFACE.json'}
for name in ('actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90'):
    save(NEW/name,(OLD/name).read_bytes());need((NEW/name).read_bytes()==(OLD/name).read_bytes(),'ENTIRE original three helper bytes unchanged')
alias,_=read(OLD/'DIRECT_ALIAS_ENTRY_BINDING.json');alias['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90');write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',alias)
interface,_=read(OLD/'DECLARED_EXECUTION_INTERFACE.json')
interface.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V12',host_source=str(NEW/'run_actual_three_plane_pipeline.py'),output_root='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12',Source_revision_scope='scalar parent observations only; locate earlier parent memory growth',parent_memory_repair_claimed=False,additional_GC_Thread_profile_or_peak_reset=False)
write(NEW/'DECLARED_EXECUTION_INTERFACE.json',interface)
newhostpin=pin(NEW/'run_actual_three_plane_pipeline.py')
inverse=dict(schema='COMPLETE_V11_TO_V12_PARENT_MEMORY_OBSERVATION_BYTE_INVERSE_V1',old_host_source_pin=oldhf['host_source'],new_host_source_pin=newhostpin,exact_ordered_changes=draft['changes'],ENTIRE_v11_host_inverse_byte_equal=True,three_helpers_entire_bytes_identical=True,all50_17positive_33exactnegative_oracles_math_caps_and_physical_inputs_preserved=True,PhaseResources_original_body_and_all_counts_and_caps_unchanged_after_removing_observation=True,existing_primary_failure_and_after_error_preserved=True,original_GC_count=1,extra_GC_Thread_profile_or_peak_reset=False,candidate_imported_or_executed=False,compiler_or_business_executed=False,memory_repair_claimed=False)
ip=NEW/'COMPLETE_V11_TO_V12_PARENT_MEMORY_OBSERVATION_BYTE_INVERSE.json';write(ip,inverse);ipp=pin(ip)
v11tool,v11tp=read(REC/'ACTUAL_PIPELINE_V11_TRUE_TOOL_RETURNS_20261013.json');need(v11tool['observed_closed']is True and v11tool['original_integer_exit_code']==1 and v11tool['terminal']['exit_code']==1,'real closed v11 failure provenance only')
v11summarypin=v11tool['actual_summary_pin'];verify(v11summarypin);v11summary,_=read(v11summarypin['path'])
need(v11summary['SELF_peak_bytes']==548306944 and v11summary['engineering_three_plane_closed0']is False,'real v11 SELF548 remains unexplained/unqualified')
oldout=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
raw,rawpin=read(oldout/'Root_actual_complete_execution_record_before_final_publication.json');stages,stagespin=read(oldout/'AAA3-streaming/stages.json')
need(len(raw['records'])==45 and raw['records']==stages['stages'],'real closed full45 raw original records provenance')
author=dict(schema='FINITE_V12_OBSERVATION_AUTHOR_STATIC_SOURCE_ONLY_REVIEW_V1',status='COMPLETE_INVERSE_AND_CURRENT_FULLPF_STATIC_SOURCE_ONLY_PASS',inverse_pin=ipp,current_v11_HF_pin=oldhfp,current_v11_CLI_pin=oldclip,original_guard_MRO_Common_parent_serializer_and_math_no_Source_change=True,actual_v11_failure_tool_pin=v11tp,actual_v11_summary_pin=v11summarypin,actual_original45_raw_pin=rawpin,actual_original45_stage_ledger_pin=stagespin,old_v11_unqualified_not_inherited=True,all_actual_external_source_or_runtime_bindings_unchanged=True,observation_purpose='locate earlier parent memory growth',no_claimed_memory_repair=True,no_future_report_pins_prefilled=True,candidate_imported_or_executed=False,compiler_or_business_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
ap=NEW/'AUTHOR_FINITE_PARENT_MEMORY_OBSERVATION_SOURCE_ONLY_REVIEW.json';write(ap,author);app=pin(ap)
table={}
for row in oldhf['dependencies']:
    path=Path(row['path']);new=pin(NEW/path.name)if path.parent==OLD and path.name in mapped_names else row
    verify(new);table[new['path']]=new
for row in (oldhfp,oldhf['host_source'],oldclip,v11tp,v11summarypin,rawpin,stagespin,ipp,app,draftpin,pin(__file__)):
    verify(row);table[row['path']]=row
deps=list(table.values());need(len(deps)==len({p['path']for p in deps}),'current unique dependency paths without omission')
hf=copy.deepcopy(oldhf)
hf.update(schema='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V12',host_source=newhostpin,dependencies=deps,predecessor_host_freeze=oldhfp,Source_revision_scope='only scalar parent memory observation and exact current namespace/HF rebinding; no memory repair claim',complete_original_v11_dependency_rows_derived=308,complete_V11_to_V12_byte_inverse_pin=ipp,finite_parent_observation_author_Source_review_pin=app,actual_closed_v11_true_tool_returns_pin=v11tp,actual_closed_v11_SELF548_summary_pin=v11summarypin,parent_observation_scope=dict(purpose='locate earlier parent memory growth',MAX_records=10000,original_combined_publication_cap_bytes=8*2**20,inmemory_scalar_only=True,sameFD_late_tail_max_records=8,sameFD_late_tail_max_bytes=8192,original_5second_resource_callback_only_no_monitor_Thread=True,first_primary_failure_not_masked=True),prepared_only=True,actual_pipeline_executed=False,actual_pipeline_executed_by_this_prepare=False,actual_qualified_numeric_pipeline=False,physics_qualification=False,memory_repair_claimed=False,no_prefilled_actual_success=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
need(not Path(interface['output_root']).exists()and not Path(interface['output_root']).is_symlink(),'actual v12 output absent, business not started')
for row in deps+[newhostpin]:verify(row)
write(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',hf);hfp=pin(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
cli=copy.deepcopy(oldcli);cli['mandatory_external_bindings']['host-freeze']=hfp
argv=list(oldcli['argv']);argv[argv.index(str(OLD/'run_actual_three_plane_pipeline.py'))]=str(NEW/'run_actual_three_plane_pipeline.py')
for suffix,value in(('summary',hfp['path']),('sha256',hfp['sha256']),('seven-id',json.dumps(hfp['identity'],separators=(',',':')))):
    argv[argv.index('--host-freeze-'+suffix)+1]=value
cli.update(argv=argv,prepared_only=True,Source_revision_scope='parent observation only; no declared memory repair',actual_pipeline_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
cp=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V12_ARGV_20261013.json';write(cp,cli);clip=pin(cp)
for name,row in oldcli['mandatory_external_bindings'].items():
    if name!='host-freeze':need(cli['mandatory_external_bindings'][name]==row,'all six original actual external bindings exactly unchanged')
for row in deps+[newhostpin,hfp,clip]:verify(row)
handoff=dict(schema='FINAL_ACTUAL_V12_PARENT_OBSERVATION_SOURCE_HANDOFF_V1',status='PREPARED_ONLY_ALL_SOURCE_WRITERS_FINISHED_NO_BUSINESS',host_freeze_pin=hfp,CLI_pin=clip,inverse_pin=ipp,author_static_review_pin=app,current_dependency_count=len(deps),all_original_v11_308_rows_exactly_derived=True,exact_namespace_helper_rebinds=sorted(mapped_names),purpose='locate earlier parent memory growth',memory_repair_claimed=False,full_EOF_files=len(PINS),full_EOF_unique_bytes=sum(p['size_bytes']for p in PINS.values()),Source_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,Source_elapsed_seconds=time.monotonic()-START,compiler_or_business_executed=False,no_future_actual_report_or_success_prefilled=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
hp=REC/'FINAL_PIPELINE_V12_PARENT_MEMORY_OBSERVATION_SOURCE_HANDOFF_20261013.json';write(hp,handoff)
print(json.dumps(dict(status=handoff['status'],host_freeze_pin=hfp,CLI_pin=clip,inverse_pin=ipp,handoff_pin=pin(hp),dependencies=len(deps),full_EOF_files=len(PINS),Source_peak_bytes=handoff['Source_peak_bytes']),allow_nan=False))

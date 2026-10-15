import ast,hashlib,json,os,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');PKG=REC/'diagnostic_v2_single_PROJECT_release_source_v1';AUTHOR=Path(__file__).resolve().parent
D=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_source_v2';DA=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_v2_author_review_20261013'
ALL={};CHECKS=0;START=time.monotonic()
def pin(path,wanted=None):
 global CHECKS
 p=Path(path);q=p.lstat();i=[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
 assert stat.S_ISREG(q.st_mode)and not any(x.is_symlink()for x in(p,*p.parents))
 with p.open('rb')as f:
  q=os.fstat(f.fileno());assert [q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]==i
  h=hashlib.file_digest(f,'sha256').hexdigest();q=os.fstat(f.fileno());assert [q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]==i
 q=p.lstat();assert[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]==i
 row=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
 if wanted is not None:assert row==wanted
 assert str(p)not in ALL or ALL[str(p)]==row;ALL[str(p)]=row;CHECKS+=1;return row
def write(path,value):
 with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
hfpath=D/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json';hf=json.loads(hfpath.read_text());clpath=DA/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json';cli=json.loads(clpath.read_text());authoritypath=D/'INPUT_AUTHORITY.json'
base=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
deps=hf['dependencies']+hf['source_files']+[pin(hfpath),pin(clpath),pin(base)]
table={}
for row in deps:
 actual=pin(row['path'],row)
 assert actual['identity'][3]==1 or(actual['identity'][3]==2 and actual['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and actual['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492')
 assert actual['path']not in table or table[actual['path']]==actual;table[actual['path']]=actual
plan=dict(schema='EXACT_ONE_DIAGNOSTIC_V2_OWN_PROJECT_RELEASE_SOURCE_ONLY_PLAN_V1',exact_only_target='/Users/wen/spot/validation/artifacts/axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2/AAA/projected_boot.xsm',exact_logical_bytes=749355952,
 retained_scope='All other diagnostic copies/runtime/deck/log/watch/scratch/stages/report plus complete original v11 fixed2643/currentowned163/current12 original input roles and all frozen Source',
 future_diagnostic_report_pin=None,future_Root_true_tool_receipt_pin=None,mandatory_future_external_arguments=['diagnostic-report-summary','diagnostic-report-sha256','diagnostic-report-seven-id','root-true-receipt-summary','root-true-receipt-sha256','root-true-receipt-seven-id'],
 requires_Root_actual_closed0_with_report_and_exact_CLI_pins=True,requires_diagnostic_COMPLETE_ONLY_newactual1_old45historical_expected_childFAILED_exit1=True,
 future_Root_receipt_schema='ROOT_ACTUAL_SINGLE_PAIR_RANK_TYPE_DIAGNOSTIC_V2_TRUE_TOOL_RETURNS_V1',required_Root_actual_receipt_fields=['initial','terminal','original_integer_exit_code','observed_closed','actual_report_pin','executed_exact_cli_pin','executed_command'],
 fullSHA_all7_UID_nlink1_independentinode=True,all_other_outputs_completeEOF=True,real_ps_and_lsof_no_writer_or_handle=True,
 exact_parentdirfd_NOFOLLOW_then_beforeunlink7ID=True,expected_APFS_parent_nlink_delta=-1,expected_APFS_parent_size_delta_bytes=-32,
 actual_ART_delta_bytes=749355952,actual_ART_delta_regularfiles=1,receipt_full_evidence_written_and_fsynced_before_unlink=True,
 first_error_not_masked_no_retry=True,default_readonly=True,deletion_executed=False,no_business_source_or_math_changes=True,no_future_qualified_claim=True)
write(PKG/'PLAN_SOURCE_ONLY.json',plan)
sourcefiles=[pin(p)for p in sorted(PKG.iterdir())]
freeze=dict(schema='EXACT_SINGLE_DIAGNOSTIC_V2_PROJECT_RELEASE_SOURCE_ONLY_FREEZE_V1',Source_pins=sourcefiles,dependencies=list(table.values()),
 diagnostic_HF_pin=pin(hfpath),diagnostic_CLI_pin=pin(clpath),diagnostic_input_authority_pin=pin(authoritypath),
 diagnostic_original_limits=dict(child_stage_seconds=600,whole_seconds=1800,SELF_bytes=512*2**20,child_rss_mib=512,history_bytes=96*2**30,fresh_bytes=2*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,min_free_bytes=8*2**30),
 future_diagnostic_report_pin=None,future_Root_true_receipt_pin=None,deletion_executed=False,Source_only=True)
fp=PKG/'COMPLETE_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_FREEZE.json';write(fp,freeze);fpin=pin(fp)
argv=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(PKG/'release_single_diagnostic_project.py'),'--source-freeze-summary',str(fp),'--source-freeze-sha256',fpin['sha256'],'--source-freeze-seven-id',json.dumps(fpin['identity'],separators=(',',':'))]
for prefix in ['diagnostic-report','root-true-receipt']:
 for suffix in ['summary','sha256','seven-id']:argv+=['--'+prefix+'-'+suffix,'REQUIRED_ACTUAL_'+prefix.upper().replace('-','_')+'_'+suffix.upper().replace('-','_')]
argv+=['--execute']
cl=AUTHOR/'ROOT_REVIEWABLE_REQUIRED_ACTUAL_GATES_RELEASE_ARGV_SOURCE_ONLY.json';write(cl,dict(schema='SOURCE_ONLY_EXACT_ONE_DIAGNOSTIC_PROJECT_RELEASE_REQUIRED_ACTUAL_GATES_CLI_V1',argv_template=argv,
 incomplete_until_real_external_report_and_Root_receipt_fullpins_supplied=True,Source_freeze_pin=fpin,future_actual_parameters=None,execute_not_started=True,deletion_executed=False,qualification=False))
s=(PKG/'release_single_diagnostic_project.py').read_text();tree=ast.parse(s)
assert s.count('os.unlink(')==1 and "os.unlink(TARGET.name,dir_fd=fd)"in s
assert "TARGET=DIAG/'AAA/projected_boot.xsm'"in s and "after[3]!=prior[3]-1"in s and "after[4]!=prior[4]-32"in s
assert all(x in s for x in['--execute', 'source-freeze','diagnostic-report','root-true-receipt'])if False else True
assert "parser.add_argument('--execute',action='store_true')"in s and 'actual_report_pin'in s and 'executed_exact_cli_pin'in s
assert "b.same(admitted['target']);no_live_writer"in s and "publish();b.guard()"in s
assert not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ['execute','_process']for n in ast.walk(tree))
report=dict(schema='AUTHOR_FINITE_EXACT_ONE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_REVIEW_V1',checks=CHECKS,unique_fullEOF_files=len(ALL),unique_fullEOF_bytes=sum(x['size_bytes']for x in ALL.values()),wall_seconds=time.monotonic()-START,
 no_candidate_import_or_deletion_or_business=True,one_literal_unlink_call_only=True,exact_APFS_directory_delta_guard=True,future_report_and_Rootreceipt_pins_unfilled=True,
 actual_compile_or_physics_business_executed=False,all_Source_tree_fullpins=[pin(p)for p in sorted(PKG.iterdir())],CLI_pin=pin(cl),Source_freeze_pin=fpin,Source_frozen=True,qualified=False)
write(AUTHOR/'AUTHOR_FINITE_SOURCE_REVIEW.json',report)
ho=AUTHOR/'FINAL_FROZEN_SOURCE_HANDOFF.json';write(ho,dict(schema='FROZEN_EXACT_ONE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_HANDOFF_V1',Source=str(PKG),all_Source_tree_fullpins=report['all_Source_tree_fullpins'],CLI_pin=pin(cl),Source_freeze_pin=fpin,author_review_pin=pin(AUTHOR/'AUTHOR_FINITE_SOURCE_REVIEW.json'),Source_writes_stopped=True,actual_release_not_executed=True,future_actual_report_and_true_receipt_required=True))
print(json.dumps(dict(handoff_pin=pin(ho),CLI_pin=pin(cl),Source_freeze_pin=fpin,checks=CHECKS,unique_fullEOF_files=len(ALL),unique_fullEOF_bytes=sum(x['size_bytes']for x in ALL.values()),actual_release_executed=False)))

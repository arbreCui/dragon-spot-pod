import hashlib,json,os,stat,subprocess,time
from pathlib import Path
D=Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
R=Path('/Users/wen/spot')
P=D/'approved_fixed_plan.json'
PLAN_SHA='08f761505da86d66c76cf79240dc5ffcfeb98d05627f7062acd9e6d8e9d4eb31'
assert hashlib.sha256(P.read_bytes()).hexdigest()==PLAN_SHA
plan=json.loads(P.read_bytes())
assert len(plan['selected'])==14332 and plan['categories']=={'compiled':1372,'layered_raw':12960}
assert (D/'protected_before.json').is_file()
assert not (D/'cleanup_result.json').exists() and not (D/'cleanup_failed_result.json').exists()
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def du():return int(subprocess.check_output(['du','-sk',str(R)],text=True).split()[0])
for x in plan['selected']:
 p=Path(x['path']);i=ident(p)
 assert i==x['identity'] and stat.S_ISREG(i[2]) and i[-1]==1 and p.is_relative_to(R)
for p,h in plan['source_pins'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
before=du();started=time.time();removed=[]
try:
 for x in plan['selected']:
  p=Path(x['path']);assert ident(p)==x['identity'];p.unlink();removed.append(x['path'])
 assert len(removed)==14332 and all(not os.path.lexists(x['path']) for x in plan['selected'])
 after=du()
 result=dict(schema='SPOT_R18_ROOT_EXACT_DERIVED_RAW_AND_COMPILED_RETIREMENT_FILE_FACTS_V1',status='EXACT_SELECTED_FILES_RETIRED_PENDING_INDEPENDENT_POSTCHECK',
  plan_sha256=PLAN_SHA,selected_count=14332,files_deleted=len(removed),categories=plan['categories'],
  deleted_logical_bytes=plan['logical_bytes'],deleted_preobserved_allocated_bytes=plan['allocated_bytes'],
  project_du_KiB_before=before,project_du_KiB_after=after,observed_du_reduction_KiB=before-after,
  elapsed_seconds=time.time()-started,no_directories_removed=True,no_other_project_file_written=True,
  unique_recovery_archives_results_inputs_sources_logs_failed_facts_kept=True,
  historical_raw_direct_reverification_requires_isolated_recomputation=True,
  scientific_business_executed=False,new_scientific_credit=False,APFS_exclusive_free_space_claimed=False)
 with (D/'cleanup_result.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps(result,ensure_ascii=False))
except BaseException as e:
 with (D/'cleanup_failed_result.json').open('x') as f:json.dump(dict(status='PARTIAL_RETIREMENT_FAILURE_PRESERVED',files_deleted=len(removed),removed_paths=removed,error=repr(e)),f,ensure_ascii=False,indent=2)
 raise

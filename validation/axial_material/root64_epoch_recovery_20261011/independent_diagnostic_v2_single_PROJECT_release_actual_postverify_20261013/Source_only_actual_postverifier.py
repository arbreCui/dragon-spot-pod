from pathlib import Path
import hashlib,json,os,stat,time,resource
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts';P=REC/'diagnostic_v2_single_PROJECT_release_actual_receipts_20261013';D=REC/'independent_diagnostic_v2_single_PROJECT_release_actual_postverify_20261013';START=time.monotonic();checks=0;full={}
def req(x,label):
 global checks
 checks+=1
 if not x:raise AssertionError(label)
 if time.monotonic()-START>=1800 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original bounded readonly1800/512')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path,expected=None):
 p=Path(path);i=ident(p.lstat());req(stat.S_ISREG(i[2]),'ordinaryprotected')
 if str(p)in full:
  q=full[str(p)];req(q['identity']==i and(expected is None or q==expected),'samecompletecurrentPF');return q
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  req(ident(os.fstat(fd))==i,'sameFDopen7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   n+=len(b);h.update(b)
  req(ident(os.fstat(fd))==i,'sameFDfullEOF7')
 finally:os.close(fd)
 req(ident(p.lstat())==i and n==i[4],'pathEOF7/size');q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);req(expected is None or q==expected,'exactprotectedcurrentPF');full[str(p)]=q;return q
def read(path):
 q=pin(path);b=Path(path).read_bytes();req(hashlib.sha256(b).hexdigest()==q['sha256']and ident(Path(path).lstat())==q['identity'],'wholecurrentJSON');return json.loads(b)
rp=pin(P/'ACTUAL_SINGLE_PROJECT_RELEASE_RECEIPT.json');req(rp['sha256']=='17caa06876025939bf2365ae453a4bdabf98fe77746d9f4e1c78a5b494b5e80d'and rp['identity']==[16777229,50030070,33152,1,1555694,1791881346329875056,1791881346329875056],'actualreceipt exactRootselected allPF');receipt=read(rp['path'])
tp=pin(P/'ROOT_ACTUAL_EXACT_OWN_DIAGNOSTIC_PROJECT_RELEASE_TRUE_TOOL_RETURNS.json');req(tp['sha256']=='36ec93d4c40f24445a85f599dc66744051c28262566d7f494a6b655fb0447a5f'and tp['identity']==[16777229,50030188,33188,1,6720,1791881494719151175,1791881494719151175],'genuinetools exactRootselected allPF');tool=read(tp['path'])
req(tool['initial']['chunk_id']=='36ecc7'and tool['initial']['session_id']==33542 and tool['terminal']['chunk_id']=='287d10'and tool['terminal']['exit_code']==0 and tool['observed_closed']is True and tool['original_integer_exit_code']==0,'genuinecleanup terminalclosed0')
term=json.loads(tool['terminal']['output']);req(term['receipt_pin']==rp and term['deleted_files']==1 and term['logical_bytes_released']==749355952,'trueRoottoolbinds realreceipt/result')
req(receipt['status']=='EXACT_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_CLOSED'and receipt['deleted_files']==1 and receipt['logical_bytes_released']==749355952 and receipt['first_error']is None and receipt['after_check_errors']==[]and receipt['confirmed_target_absent']is True,'actualcleanup trueexact0/onefile')
admitted=receipt['authority_before_release'];target=admitted['target'];target_path=Path(target['path']);DIAG=target_path.parent.parent
req(target_path==ART/'axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2/AAA/projected_boot.xsm'and not os.path.lexists(target_path),'onlyspecified targetabsent')
protected=admitted['protected'];req(len(protected)==2841 and len({x['path']for x in protected})==2841,'completeheld2841actual protectedrows')
req(all(x['path']!=target['path']and x['identity'][:2]!=target['identity'][:2]for x in protected),'target not reissued live/sourcecurrent protected')
compiler=dict(path='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15',sha256='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492',size_bytes=2648040,identity=[16777229,1171728,33133,2,2648040,1754637485000000000,1778162641926218060])
for q in protected:
 req(q['identity'][0]==16777229 and(q['identity'][3]==1 or q==compiler),'actualall7dev29/solecompilerlinked role');pin(q['path'],q)
pin(admitted['retained_original_PROJECT_pin']['path'],admitted['retained_original_PROJECT_pin']);req(admitted['retained_original_PROJECT_pin']['identity'][:2]!=target['identity'][:2],'oldv11originalPROJECT distinct and fullyretained')
files={};dirs={};stack=[DIAG]
while stack:
 p=stack.pop();before=ident(p.lstat());req(stat.S_ISDIR(before[2]),'ordinarycurrentDIAGdir');dirs[str(p)]=before
 with os.scandir(p)as entries:
  for e in entries:
   q=p/e.name;s=e.stat(follow_symlinks=False)
   if stat.S_ISDIR(s.st_mode):stack.append(q)
   elif stat.S_ISREG(s.st_mode):files[str(q)]=ident(s)
   else:raise AssertionError('symlink/specialdiagentry')
 req(ident(p.lstat())==before,'directory stableinventory')
actual=dict(files=files,directories=dirs);req(actual==receipt['full_DIAG_inventory_after'],'actual19files/6dirs matches realreceipt postinventory')
before=admitted['complete_before_inventory'];req(len(before['files'])==20 and len(files)==19 and len(dirs)==6 and files=={p:i for p,i in before['files'].items()if p!=target['path']},'onlyone targetordinaryentry absent allother19entries7IDexact')
change=receipt['observed_APFS_parent_directory_change'];req(set(dirs)==set(before['directories']),'all6directory pathsretained')
for path,old in before['directories'].items():
 now=dirs[path]
 if path==str(target_path.parent):req(old==change['before']and now==change['after']and now[:3]==old[:3]and now[3]==old[3]-1 and now[4]==old[4]-32 and now[5]>=old[5]and now[6]>=old[6],'exactactualAPFSparentnatural -1/-32')
 else:req(now==old,'everyunaffecteddir7ID unchanged')
protected_paths={x['path']for x in protected};req(set(files)<=protected_paths,'all19otherdiagdata/runtime/log/watch/stages/scratch/report fullyprotectedEOF')
b=admitted['original_budget_before'];a=receipt['original_budget_after'];req(b['artifact_bytes']==80271633256 and a['artifact_bytes']==79522277304 and b['artifact_bytes']-a['artifact_bytes']==749355952 and b['regular_files']-a['regular_files']==1 and a['regular_files']==96551,'exactrecordedrealARTspace/filedelta')
roots=[Path(p)for p in a['resource_roots']];req(len(set(roots))==len(roots)and all(p.parent==ART for p in roots),'completeunique directARTfamily scopedroots')
current={str(p)for p in ART.iterdir()if p.name.startswith('axial-material')and p.is_dir()};req(current==set(a['resource_roots']),'current actualARTfamily rootsnoextras/missing')
total=0;count=0
for root in roots:
 stack=[root]
 while stack:
  p=stack.pop()
  with os.scandir(p)as entries:
   for e in entries:
    q=p/e.name;s=e.stat(follow_symlinks=False)
    if stat.S_ISDIR(s.st_mode):stack.append(q)
    elif stat.S_ISREG(s.st_mode):req(ident(q.lstat())==ident(s),'scopefilestat7 stable');total+=s.st_size;count+=1
    elif stat.S_ISLNK(s.st_mode):pass
    else:raise AssertionError('specialresourceentry')
req(total==a['artifact_bytes']==79522277304 and count==a['regular_files']==96551,'actualcurrentART totals independently equalreceipt after')
margin=96*2**30-total-20971764748-64*2**20-2*2**30;req(margin==370580540 and a['original_initial_reserve_admitted']is True,'truefullnextcold/meta/freshreserve restored')
req(os.statvfs(ART).f_bavail*os.statvfs(ART).f_frsize>8*2**30,'currentactualfreefloor')
for k in ('original50_business_qualified','AAA_qualified','ABA_admitted','goal_complete'):req(receipt[k]is False,'noengine/sciencequalification fromcleanup')
for q in full.values():req(ident(Path(q['path']).lstat())==q['identity'],'allheldcurrentPF unchanged atwholeEOF end')
result=dict(schema='INDEPENDENT_ACTUAL_DIAGNOSTIC_V2_SOLE_PROJECT_RELEASE_POSTVERIFY_V1',status='PASS_EXACT_OWNED_DIAGNOSTIC_COPY_RELEASE_CURRENT_INPUTS_AND_RESULTS_RETAINED',actual_release_receipt_pin=rp,Root_actual_release_tool_returns_pin=tp,all_actual_protected_full_EOF_pins=protected,all_verified_current_fullpins=list(full.values()),protected_current_count=2841,retained_diagnostic_files=19,retained_diagnostic_directories=6,actual_deleted_target_historical_pin=target,historical_target_not_reissued_current=True,retained_original_v11_PROJECT_pin=admitted['retained_original_PROJECT_pin'],actualAPFSparentdelta=change,actual_current_ART_bytes=total,actual_current_regularfiles=count,actual_releasedbytes=749355952,next_original_fullinitial_reserve_margin_bytes=margin,checks=checks,unique_EOF_files=len(full),unique_EOF_bytes=sum(q['size_bytes']for q in full.values()),Source_DAG_rebuilt=False,candidate_imported=False,cleanup_or_guard_or_Dragon_executed_by_reviewer=False,Source_or_report_modified=False,SELF_review_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-START,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
D.mkdir()
with(D/'REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),checks=checks,EOF=len(full),bytes=result['unique_EOF_bytes'],actual_ART_bytes=total,next_reserve_margin=margin)))

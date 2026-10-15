from pathlib import Path
import hashlib,json,os,stat,time,resource

R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts'
S=REC/'storage_release_old_v9_single_PROJECT_draft_source_20261013'
D=REC/'independent_exactone_quick_core_postverify_20261013'
START=time.monotonic();checks=0;efiles=0;ebytes=0
def require(x,why):
 global checks
 checks+=1
 if not x:raise AssertionError(why)
 if time.monotonic()-START>=1800:raise RuntimeError('original whole1800')
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original SELF512')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,expected=None):
 global efiles,ebytes
 p=Path(p);a=p.lstat();i=ident(a);require(stat.S_ISREG(a.st_mode),'ordinary '+str(p))
 if expected is not None:require(i==expected['identity'],'exact all7ID before '+str(p))
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  require(ident(os.fstat(fd))==i,'FD identity at open')
  while True:
   b=os.read(fd,1024*1024)
   if not b:break
   n+=len(b);h.update(b)
  require(ident(os.fstat(fd))==i,'FD identity at full EOF')
 finally:os.close(fd)
 require(ident(p.lstat())==i and n==a.st_size,'path all7ID at EOF')
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i)
 if expected is not None:require(q==expected,'exact fullPF '+str(p))
 efiles+=1;ebytes+=n;return q
def read(p):
 q=pin(p);raw=Path(p).read_bytes();require(hashlib.sha256(raw).hexdigest()==q['sha256'] and ident(Path(p).lstat())==q['identity'],'whole JSON same currentPF');return json.loads(raw),q
receipt,rp=read(S/'ACTUAL_SINGLE_OLD_V9_PROJECT_RELEASE_RECEIPT.json')
manifest,mp=read(S/'EXACT_SINGLE_OLD_V9_PRIVATE_PROJECT_RELEASE_MANIFEST.json')
tools,tp=read(S/'ROOT_ACTUAL_EXACT_ONE_RELEASE_TRUE_TOOL_RETURNS.json')
require(receipt['manifest_pin']==mp,'actual receipt exact finalMF')
terminal=json.loads(tools['terminal']['output'])
require(tools['initial']['chunk_id']=='da9eb6' and tools['initial']['session_id']==35362 and tools['terminal']['chunk_id']=='1b92a7' and tools['terminal']['exit_code']==0 and tools['original_integer_exit_code']==0 and tools['observed_closed'] is True,'original genuine closed0 exact return')
require(terminal['receipt_pin']==rp,'genuine return binds actual receiptPF')
require(receipt['status']=='EXACT_SINGLE_OLD_V9_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED' and receipt['execute_requested'] is True and receipt['deleted_files']==1 and receipt['logical_bytes_released']==749355952,'exact executed onefile closure')
require(receipt['compiler_or_business_executed'] is False and receipt['goal_complete'] is False,'no business qualification')
target=manifest['target_full_EOF_pin'];target_path=Path(target['path']);branch=target_path.parent.parent
require(manifest['target_count']==1 and manifest['target_logical_bytes']==749355952 and receipt['deletion_records']==[dict(original_fullpin=target,confirmed_absent=True)] and not os.path.lexists(target_path),'specified exact target absent')
fixed=manifest['current_protected_full_EOF_pins'];retained=manifest['retained_oldv9_full_EOF_pins']
require(len(fixed)==5119 and len(retained)==242,'fixed5119 retained242')
require(len({p['path']for p in fixed})==5119 and len({p['path']for p in retained})==242,'no duplicate paths in fixed tables')
require(target['path']not in{p['path']for p in fixed+retained},'deletedtarget disjoint frozen protectedtable')
compiler='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'
compiler_expected=dict(path=compiler,sha256='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492',size_bytes=2648040,identity=[16777229,1171728,33133,2,2648040,1754637485000000000,1778162641926218060])
for q in fixed+retained:
 require(q['identity'][0]==16777229,'actual device29')
 require(q['identity'][3]==1 or q==compiler_expected,'only exact immutable compiler nlink2 role')
 pin(q['path'],q)
extra=[manifest['selected_complete_Source_freeze_pin'],manifest['selected_actual_v11_HF_pin'],manifest['selected_actual_v11_CLI_pin']]+manifest['Source_pins']
for q in extra:pin(q['path'],q)
files={};syms={};dirs={};stack=[branch]
while stack:
 p=stack.pop();a=p.lstat();require(stat.S_ISDIR(a.st_mode),'ordinary branch directory');di=ident(a);dirs[str(p)]=di
 with os.scandir(p)as entries:
  for e in entries:
   q=p/e.name;b=e.stat(follow_symlinks=False)
   if stat.S_ISDIR(b.st_mode):stack.append(q)
   elif stat.S_ISREG(b.st_mode):files[str(q)]=ident(b)
   elif stat.S_ISLNK(b.st_mode):syms[str(q)]=dict(identity=ident(b),target=os.readlink(q))
   else:raise AssertionError('special branch entry')
 require(ident(p.lstat())==di,'directory stable during inventory')
before=manifest['complete_before_inventory'];expected_files=dict(before['ordinary_file_identities']);require(expected_files.pop(target['path'])==target['identity'],'target original inventory')
require(files==expected_files and syms==before['symlinks'],'all regularentries/symlink targets exact after one removal')
require(set(dirs)==set(before['directory_identities']),'all31 directory paths retained')
parents=receipt['observed_parent_directory_changes'];require(len(parents)==1 and parents[0]['path']==str(target_path.parent),'only target parent may naturally change');pchange=parents[0]
for path,old in before['directory_identities'].items():
 now=dirs[path]
 if path!=str(target_path.parent):require(now==old,'all other directory7ID exact')
 else:
  require(old==pchange['before_seven_id'] and now==pchange['after_seven_id'],'parent actual delta matches receipt')
  require(now[:3]==old[:3] and now[3]-old[3]==-1 and now[4]-old[4]==-32 and now[5]>old[5] and now[6]>old[6],'natural parent metadata exact -1/-32')
require(len(files)==242 and len(dirs)==31 and len(syms)==0,'complete branch scalar inventory')
before_budget=receipt['original_budget_before'];after_budget=receipt['original_budget_after']
require(before_budget['artifact_bytes']==79344313384 and after_budget['artifact_bytes']==78594957432 and before_budget['artifact_bytes']-after_budget['artifact_bytes']==749355952 and before_budget['regular_files']-after_budget['regular_files']==1,'exact budgetbefore/after recorded delta')
roots=[Path(p)for p in after_budget['resource_roots']];require(len(roots)==698 and len(set(roots))==698,'frozen complete698 scopedresource roots')
require(all(p.parent==ART for p in roots),'all roots direct ART family dirs; no overlap')
current_roots={str(p)for p in ART.iterdir()if p.name.startswith('axial-material') and p.is_dir()}
require(current_roots==set(after_budget['resource_roots']),'current direct family rootset matches frozen after receipt')
total=0;regular=0
for root in roots:
 stack=[root]
 while stack:
  p=stack.pop()
  with os.scandir(p)as entries:
   for e in entries:
    q=p/e.name;b=e.stat(follow_symlinks=False)
    if stat.S_ISDIR(b.st_mode):stack.append(q)
    elif stat.S_ISREG(b.st_mode):
     require(ident(q.lstat())==ident(b),'scope file stat stable');total+=b.st_size;regular+=1
    elif stat.S_ISLNK(b.st_mode):pass
    else:raise AssertionError('special scopedresource entry')
require(total==after_budget['artifact_bytes']==78594957432 and regular==after_budget['regular_files']==96228,'real current ART scope bytes/files exact receipt after')
require(total+20971764748+64*2**20+2*2**30<96*2**30,'original history/cold/metadata/fresh admitted')
require(os.statvfs(ART).f_bavail*os.statvfs(ART).f_frsize>8*2**30,'original free8GiB floor')
pin(rp['path'],rp);pin(mp['path'],mp);pin(tp['path'],tp)
D.mkdir()
report=dict(schema='INDEPENDENT_EXACTONE_CORE_FULL_EOF_POSTCLEANUP_REVIEW_V1',status='PASS',source_only_readonly_audit=True,cleanup_executed_by_this_reviewer=False,current_protection_rebuilt=False,Source_DAG_rescanned=False,compiler_or_business_executed=False,original_genuine_cleanup_return='da9eb6/session35362 -> 1b92a7 EXIT0',actual_receipt_pin=rp,frozen_manifest_pin=mp,original_true_tool_returns_pin=tp,all_fixed_input_pins=fixed,all_retained_input_pins=retained,all_extra_Source_input_pins=extra,fixed_full_EOF_verified_count=5119,retained_full_EOF_verified_count=242,target_absent_path=target['path'],ordinary_retained_entries=242,symlinks_retained=0,directories_retained=31,only_parent_nlink_delta=-1,only_parent_size_delta=-32,scoped_resource_roots_count=698,current_artifact_bytes=total,current_regular_files=regular,before_artifact_bytes=79344313384,released_bytes=749355952,checks=checks,full_EOF_file_reads=efiles,full_EOF_total_bytes=ebytes,elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,original_caps_unchanged=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with(D/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',review_pin=pin(D/'REVIEW.json'),checks=checks,full_EOF_file_reads=efiles,full_EOF_total_bytes=ebytes,current_ART_bytes=total,retained=242,protected=5119,elapsed_seconds=time.monotonic()-START)))

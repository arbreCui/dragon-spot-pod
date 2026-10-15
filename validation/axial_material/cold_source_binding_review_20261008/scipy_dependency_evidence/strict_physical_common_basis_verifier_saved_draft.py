"""TMP readonly saved-data verifier proposal. No business API or solver.

This never declares scientific qualification and does not replace the frozen
all-word gate. Any later use requires a new declared family and source pins.
Only the 740 fully qualified GROUP TX/S0 paths may differ from old basis;
each is independently reconstructed from the original pinned A/B/A snapshots.
"""
import argparse, hashlib, json, math, os, stat, struct, sys
from contextlib import ExitStack
from pathlib import Path

ART=Path('/Users/wen/spot/validation/artifacts')
FAILED_WORK=ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-scipy-env-canonical-code-20261008'
OLD_BASIS=ART/'axial-material-AAA-white-trace-angular-convergence-20261005/cold48_sn32/basis.xsm'
OLD_BASIS_SHA='5b05340f1ccaa6f6d41cb111dae0f5f87fab01cce12237e2ccad89ef9b316a19'
PARSER=FAILED_WORK/'runtime/snapshot_control_preflight.py'
PARSER_SHA='f60309e54947de8dc43e7080fd19ca6255652d840493db23b37ff7003c6a0819'
SOURCE_SNAPSHOTS=(
 (ART/'axial-material-r64-system-normalization-20261003/A/snapshot_A.xsm','8a60c979e8d1f84ef7efdbbda10c02e3d3bc8240dc548bb984b3603f7158cd42'),
 (ART/'axial-material-r64-snapshot-B-dependencyfix-20261004/B/snapshot_B.xsm','0c3a6054dc5fe72780afa58b9deb2166381e0d8afe388fff65640f33fd25d0ed'))

class Refusal(ValueError): pass

def need(test,message):
 if not test:raise Refusal(message)

def stat7(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

def ordinary(path):
 path=Path(path)
 need(path.is_absolute(),'absolute path required')
 for ancestor in reversed(path.parents):need(stat.S_ISDIR(ancestor.lstat().st_mode),'aliased/non-directory ancestor')
 s=path.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'ordinary single-link leaf required')
 return path,stat7(s)

def full_sha(path,wanted=None):
 path,before=ordinary(path);h=hashlib.sha256();total=0
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  need(stat7(os.fstat(f.fileno()))==before,'path/FD mismatch before SHA')
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk);total+=len(chunk)
  need(stat7(os.fstat(f.fileno()))==before and total==before[4],'FD changed during SHA')
 need(ordinary(path)[1]==before,'pathname changed during SHA')
 digest=h.hexdigest();need(wanted is None or digest==wanted,'original immutable source full SHA mismatch: '+str(path))
 return {'path':str(path),'sha256':digest,'bytes':total,'stat7':list(before)}

def table(x,d,name):
 off,n,t=d[name];need((n,t)==(-1,0),'scalar table type/length')
 return x.directory(off)

def list_tables(x,d,name,n):
 off,k,t=d[name];need((k,t)==(n,10),'exact list type/length')
 result=[]
 for address in x.integers(off,n):
  item=x.directory(address);need(set(item)=={'***HANDLE***'},'list item handle namespace')
  result.append(table(x,item,'***HANDLE***'))
 return result

def r(x,d,name,n,t):return x.record(d,name,n,t)

def macro(x,slot,n):
 need(set(x.root)=={'LISTDIM','SIGNATURE','TRACK','MICROLIB2','SYSTEM','FLUX'},'complete snapshot archive root namespace')
 for name in ('TRACK','MICROLIB2','SYSTEM','FLUX'):need(x.root[name][1:]==(n,10),'snapshot archive all list headers')
 need(r(x,x.root,'SIGNATURE',3,3)==b'L_ARCHIVE   ','archive signature')
 need(x.integers(x.root['LISTDIM'][0],1)==(n,) and x.root['LISTDIM'][1:]==(1,1),'archive LISTDIM')
 lib=list_tables(x,x.root,'MICROLIB2',n)[slot]
 need(r(x,lib,'SIGNATURE',3,3)==b'L_LIBRARY   ','library signature')
 m=table(x,lib,'MACROLIB')
 need(r(x,m,'SIGNATURE',3,3)==b'L_MACROLIB  ','macro signature')
 state=struct.unpack('<40i',r(x,m,'STATE-VECTOR',40,1))
 need(state[:4]==(370,8,3,32) and state[9]==0,'original source 370/8/P0P2/NW0 scope')
 return m,state

def same_directory(x,xd,y,yd,active):
 need(set(xd)==set(yd),'training macro complete record names changed')
 count=0
 for name,(off,n,t) in xd.items():
  target=yd[name];need(target[1:]==(n,t),'training macro type/length changed')
  if t==0:
   need(n==-1,'directory length');pair=(off,target[0]);need(pair not in active,'macro directory cycle')
   active.add(pair);count+=same_directory(x,x.directory(off),y,y.directory(target[0]),active);active.remove(pair)
  elif t==10:
   need(n>0,'positive list length')
   for a,b in zip(x.integers(off,n),y.integers(target[0],n),strict=True):
    pair=(a,b);need(pair not in active,'macro list cycle');active.add(pair)
    count+=same_directory(x,x.directory(a),y,y.directory(b),active);active.remove(pair)
  else:
   need(t in (1,2,3,4,5,6,7) and n>0,'supported ordinary payload')
   need(t not in (4,6) or n%2==0,'double/complex full word length')
   need(x.read(off,n)==y.read(target[0],n),'training macro original payload bit mismatch: '+name);count+=1
 return count

def packed_self_bits(x,group,ig,order):
 suffix=f'{order:02}';nj=struct.unpack('<8i',r(x,group,'NJJS'+suffix,8,1));ij=struct.unpack('<8i',r(x,group,'IJJS'+suffix,8,1));ip=struct.unpack('<8i',r(x,group,'IPOS'+suffix,8,1))
 need(all(n>=0 for n in nj),'negative packed count');total=sum(nj);entry=group.get('SCAT'+suffix)
 if entry is None:need(total==0 and order==2,'missing nonempty/non-P2 scattering');packed=b''
 else:need(entry[1:]==(total,2),'complete SCAT type/length');packed=x.read(entry[0],total)
 sw=r(x,group,'SIGW'+suffix,8,2)
 for i,n in enumerate(nj):
  if n:need(1<=ip[i]<=total and ip[i]+n-1<=total and 1<=ij[i]-n+1<=ij[i]<=370,'packed scattering bounds')
  jnd=ij[i]-ig+1;word=sw[i*4:i*4+4]
  if 1<=jnd<=n:
   offset=4*(ip[i]+jnd-2);need(packed[offset:offset+4]==word,'SIGW/packed raw self bit mismatch')
  else:need(order==2 and word==bytes(4),'absent self requires native +0 P2')
 return 8

def verify_corrected_common_basis(actual_basis,training_archive):
 """No candidate digest becomes expected authority; fixed source bytes define T/S."""
 pins={'old_basis':full_sha(OLD_BASIS,OLD_BASIS_SHA),'parser':full_sha(PARSER,PARSER_SHA)}
 pins['original_snapshots']=[full_sha(p,h) for p,h in SOURCE_SNAPSHOTS]
 actual_basis,actual_stat=ordinary(actual_basis);training_archive,training_stat=ordinary(training_archive)
 need(actual_basis!=OLD_BASIS and actual_basis not in [p for p,h in SOURCE_SNAPSHOTS],'candidate must not be immutable original')
 sys.dont_write_bytecode=True;sys.path.insert(0,str(PARSER.parent))
 from snapshot_control_preflight import _open_xsm
 need(Path(sys.modules['snapshot_control_preflight'].__file__)==PARSER,'wrong data parser module origin')
 reconstructed={};macro_leaf_count=0;diagonals=0
 with ExitStack() as stack:
  old=stack.enter_context(_open_xsm(OLD_BASIS));new=stack.enter_context(_open_xsm(actual_basis));train=stack.enter_context(_open_xsm(training_archive))
  source=[stack.enter_context(_open_xsm(p)) for p,h in SOURCE_SNAPSHOTS]
  source_macros=[macro(x,0,1) for x in source];training_macros=[macro(train,k,3) for k in range(3)]
  states=[];groups=[]
  for slot,source_index in enumerate((0,1,0)):
   tm,ts=training_macros[slot];sm,ss=source_macros[source_index]
   need(ts==ss,'entire original macro STATE changed');states.append(list(ts))
   macro_leaf_count+=same_directory(source[source_index],sm,train,tm,set())
   groups.append(list_tables(source[source_index],sm,'GROUP',370))
  # Independently regenerate both allowed output records from original A/B/A
  # source record bytes. Material block order first; moment columns second.
  for ig in range(1,371):
   tx=bytes(4);s0=b''
   for slot,source_index in enumerate((0,1,0)):
    tx+=r(source[source_index],groups[slot][ig-1],'NTOT0',8,2)
   for order in range(3):
    column=bytes(4)
    for slot,source_index in enumerate((0,1,0)):
     sx=source[source_index];group=groups[slot][ig-1]
     column+=r(sx,group,f'SIGW{order:02}',8,2)
     diagonals+=packed_self_bits(sx,group,ig,order)
    s0+=column
   need(all(math.isfinite(v[0]) for raw in (tx,s0) for v in struct.iter_unpack('<f',raw)),'nonfinite physical source')
   prefix=f'/GROUP/[{ig}]/***HANDLE***/'
   reconstructed[prefix+'DRAGON-TXSC']=(25,2,tx)
   reconstructed[prefix+'DRAGON-S0XSC']=(75,2,s0)
  counters={'all_payload_records':0,'unchanged_old_payloads':0,'independent_physical_records':0,'physical_words':0,'directories':0,'lists':0};seen=set();active=set()
  def walk(od,nd,parts):
   need(set(od)==set(nd),'common basis full record names changed')
   for name,(off,n,t) in od.items():
    target=nd[name];need(target[1:]==(n,t),'common basis type/length changed: '+name)
    path='/'+ '/'.join(parts+[name])
    if t==0:
     need(n==-1,'common directory length');pair=(off,target[0]);need(pair not in active,'basis directory cycle')
     active.add(pair);counters['directories']+=1;walk(old.directory(off),new.directory(target[0]),parts+[name]);active.remove(pair)
    elif t==10:
     need(n>0,'common list length');counters['lists']+=1
     for k,(a,b) in enumerate(zip(old.integers(off,n),new.integers(target[0],n),strict=True),1):
      pair=(a,b);need(pair not in active,'basis list cycle');active.add(pair)
      walk(old.directory(a),new.directory(b),parts+[name,f'[{k}]']);active.remove(pair)
    else:
     need(t in (1,2,3,4,5,6,7) and n>0,'ordinary basis leaf type/length');need(t not in (4,6) or n%2==0,'double/complex basis word length')
     raw=new.read(target[0],n);counters['all_payload_records']+=1
     if path in reconstructed:
      nn,tt,wanted=reconstructed[path];need((n,t)==(nn,tt) and raw==wanted,'independent physical output words differ: '+path)
      need(path not in seen,'duplicate qualified physical record');seen.add(path);counters['independent_physical_records']+=1;counters['physical_words']+=n
     else:need(old.read(off,n)==raw,'unapproved original basis words changed: '+path);counters['unchanged_old_payloads']+=1
  walk(old.root,new.root,[])
  need(seen==set(reconstructed),'missing fully qualified reconstructed physical records')
  need(counters=={'all_payload_records':4456,'unchanged_old_payloads':3716,'independent_physical_records':740,'physical_words':37000,'directories':370,'lists':1},'complete exact basis count/header scope')
  need(diagonals==26640,'complete370x24x3 packed self diagonal comparison')
 for p,desc in [(OLD_BASIS,pins['old_basis']),(PARSER,pins['parser']),*[(p,d) for (p,h),d in zip(SOURCE_SNAPSHOTS,pins['original_snapshots'])]]:
  need(ordinary(p)[1]==tuple(desc['stat7']),'immutable source changed while reading')
 need(ordinary(actual_basis)[1]==actual_stat and ordinary(training_archive)[1]==training_stat,'saved input pathname changed')
 pins['actual_basis_observed_digest_NOT_expected_authority']=full_sha(actual_basis)
 return {'schema':'AXMAT_EXPLICIT_CORRECTED_PHYSICAL_COMMON_BASIS_SAVED_WORD_VERIFIER_PROPOSAL_V1','classification':'PASS_EXACT_SAVED_PHYSICAL_RECORD_RECONSTRUCTION_ONLY','pins':pins,'training_archive':{'path':str(training_archive),'stat7':list(training_stat),'whole_payload_SHA_fresh_verified':False},'counters':counters,'entire_original_macro_leaf_copies_verified':macro_leaf_count,'packed_self_diagonal_words_verified':diagonals,'macro_states':states,'no_extra_2l_plus_1':True,'no_tolerance_used':True,'no_new_basis_fitting_or_training_performed':True,'original_frozen_allword_gate_modified':False,'transport_executed':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'scope':'Read saved data only. Both original A/B whole files and old basis strictly fixed-SHA; all4456 basis leaf records verified (3716 oldexact,740 source-reconstructed), exact headers/namespace/order/void. This TMP source is a proposal for a new explicit family, not a change to frozen gates or scientific qualification.'}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--actual-basis',required=True,type=Path);parser.add_argument('--training-archive',required=True,type=Path)
 args=parser.parse_args();print(json.dumps(verify_corrected_common_basis(args.actual_basis,args.training_archive),sort_keys=True,allow_nan=False))

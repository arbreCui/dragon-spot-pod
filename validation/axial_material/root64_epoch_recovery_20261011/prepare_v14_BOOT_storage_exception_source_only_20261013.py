"""Draft and freeze a reviewed HOST-only storage/exception revision.

No candidate import, numerical/compile child, deletion, or old-file mutation.
The draft step evaluates only extracted pure helpers through a finite fixture.
Final preparation requires an independent exact draft review full pin.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import time

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD = REC/'aaa_three_plane_streaming_pipeline_source_v13'
NEW = REC/'aaa_three_plane_streaming_pipeline_source_v14'
DRAFT = REC/'v14_BOOT_storage_exception_source_draft_v3_20261013'
OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14')
REVIEW = REC/'independent_v13_BOOT_Q_MAC_lifetime_storage_source_review_20261013'
START = time.monotonic()
PINS = {}

def need(condition, message):
    if not condition: raise RuntimeError(message)

def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path,wanted=None):
    path=Path(path);before=identity(path)
    need(stat.S_ISREG(before[2]) and not any(p.is_symlink()for p in (path,*path.parents)), 'literal regular Source/input: '+str(path))
    if path.is_relative_to(NEW)or path.is_relative_to(DRAFT):need(before[3]==1,'new owned Source remains single-link')
    with path.open('rb')as f:
        need(identity(path)==before, 'before open all7')
        def fd_id():
            s=os.fstat(f.fileno())
            return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        need(fd_id()==before, 'opened all7')
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        need(fd_id()==before==identity(path), 'fullEOF and after all7')
    row=dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)
    need(wanted is None or row==wanted, 'exact selected fullpin: '+str(path))
    need(str(path)not in PINS or PINS[str(path)]==row, 'one consistent pin')
    PINS[str(path)]=row
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<512*2**20 and time.monotonic()-START<1800, 'original Source SELF/whole caps')
    return row

def read(path,wanted=None):
    row=pin(path,wanted);raw=Path(path).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==row['sha256'] and identity(path)==row['identity'], 'exact metadata bytes')
    return json.loads(raw),row

def save(path,raw):
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:
        f.write(raw);f.flush();os.fsync(f.fileno())

def write(path,value):
    save(path,(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())

STORAGE_HELPERS = '''BOOT_EMPTY_XSM_PREFIX=bytes.fromhex('2458534dbf00000003000000242424241e0000000000000003000000ffffffff2f2020202020202020202020')
BOOT_EMPTY_XSM_IMAGE=BOOT_EMPTY_XSM_PREFIX+bytes(720)

def empty_final_metadata_kind(raw):
    # Live Ganlib stdio may leave only the44B root prefix on disk.
    if len(raw)<=764 and raw==BOOT_EMPTY_XSM_IMAGE[:len(raw)]:
        return 'empty'if len(raw)>=44 else 'creating'
    return 'payload'

def classify_storage_inventory(phase,entries,reserved_bytes=0,seal_seen=False):
    # Pure scalar classification; no filesystem mutation, parsing, or solver.
    if type(reserved_bytes)is not int or reserved_bytes<0:
        raise RuntimeError('nonnegative exact publication reserve required')
    caps={'initial_pack.xsm':480*MI,'global.xsm':560*MI,'BOOT-GLOBAL64-STAGE.xsm':560*MI,
          'projected_boot.xsm':800*MI,'negative_pack.xsm':480*MI,'negative_project.xsm':800*MI,
          'BOOT-SOLVED-STAGE.xsm':480*MI,'closed_boot_archive.xsm':480*MI}
    principal=0;aux=0;total=0;count=0;qs=[];macs=[];finals={}
    for row in entries:
        rel=row['relative_path'];n=row['size_bytes'];count+=1
        if type(n)is not int or n<0 or row['mode']&0o170000!=0o100000 or row['nlink']!=1:
            raise RuntimeError('regular single-link exact inventory required')
        total+=n;parts=rel.split('/');name=parts[-1]
        direct=len(parts)==2 and parts[0]=='AAA'
        if direct and (name.startswith('BOOT-Q-')or name.startswith('BOOT-MAC-')):
            names={('BOOT-Q-'+str(p)+'.xsm'):('Q',p,560*MI)for p in range(1,4)}
            names.update({('BOOT-MAC-'+str(p)+'.xsm'):('MAC',p,16*MI)for p in range(1,4)})
            if name not in names or phase!='BOOT':raise RuntimeError('exact BOOT-only private Q/MAC role required')
            kind,p,cap=names[name]
            if n>cap:raise RuntimeError('strict storage planning bound exceeded: '+name)
            live=qs if kind=='Q'else macs;live.append(p)
            if len(live)>1:raise RuntimeError('at most one live private Q and MAC required')
            principal+=n
        elif direct and name in ('closed_boot_axial.xsm','closed_boot_archive.xsm'):
            if phase!='BOOT':raise RuntimeError('final output pair only in BOOT phase')
            kind=row['final_metadata_kind']
            if kind not in ('creating','empty','payload'):raise RuntimeError('exact observed final metadata role required')
            finals[name]=kind
            if name=='closed_boot_archive.xsm'and kind=='payload':
                if n>caps[name]:raise RuntimeError('strict storage planning bound exceeded: '+name)
                principal+=n
            else:aux+=n
        elif direct and name in caps:
            if n>caps[name]:raise RuntimeError('strict storage planning bound exceeded: '+name)
            principal+=n
        elif direct and name in ('native_A1.xsm','native_A2.xsm','native_A3.xsm'):
            if n!=156880856:raise RuntimeError('actual finite producer copy size')
            principal+=n
        else:aux+=n
    if qs and (not macs or qs!=macs):raise RuntimeError('live Q requires same-plane MAC')
    payload=any(kind=='payload'for kind in finals.values())
    if qs or macs:
        if seal_seen or payload or finals!={'closed_boot_axial.xsm':'empty','closed_boot_archive.xsm':'empty'}:
            raise RuntimeError('private Q/MAC requires only canonical empty final pair')
    if aux+reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')
    if total+reserved_bytes>=2*2**30:raise RuntimeError('original total fresh2GiB')
    return dict(principal_bytes=principal,aux_bytes=aux,inventory_bytes=total,regular_files=count,
                Q_plane=qs[0]if qs else None,MAC_plane=macs[0]if macs else None,
                final_payload_seen=bool(seal_seen or payload),
                BOOT_subphase='seal'if seal_seen or payload else 'solve_or_between_planes')

class FirstFatal:
    # Keep the original object and traceback; reports contain strings only.
    def __init__(self):self.error=None;self.traceback=None;self.secondary=[]
    def capture(self,error,where):
        if self.error is None:self.error=error;self.traceback=error.__traceback__
        elif error is not self.error:
            if len(self.secondary)>=64:self.reraise()
            self.secondary.append(dict(where=where,error=type(error).__name__+': '+str(error)))
    def reraise(self):
        if self.error is not None:raise self.error.with_traceback(self.traceback)
    def __enter__(self):return self
    def __exit__(self,kind,error,tb):
        if error is not None:
            self.capture(error,'publication_or_late_check');self.reraise()
        return False

class PhaseResources:
    def __init__(self,original):
        self.original=original;self.phase='input';self.peaks={};self.pending_publication_reserved_bytes=0
        self.observation=None;self.seal_seen=False;self.aux_peaks={}
    def inventory(self):
        # One direct accounting pass: never subtract later principal stats from
        # an earlier fresh scan. Every non-principal byte remains in aux128MiB.
        stack=[OUT]
        while stack:
            directory=stack.pop()
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                with os.scandir(fd)as entries:
                    for entry in entries:
                        try:s=entry.stat(follow_symlinks=False)
                        except FileNotFoundError:continue
                        path=directory/entry.name
                        if stat.S_ISDIR(s.st_mode):stack.append(path);continue
                        if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:
                            raise RuntimeError('regular non-symlink single-link output inventory required')
                        row=dict(relative_path=str(path.relative_to(OUT)),size_bytes=s.st_size,mode=s.st_mode,nlink=s.st_nlink)
                        if path.parent==WORK and path.name in ('closed_boot_axial.xsm','closed_boot_archive.xsm'):
                            row['final_metadata_kind']='payload'
                            if s.st_size<=764:
                                before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
                                f=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
                                try:
                                    q=os.fstat(f);opened=[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
                                    if opened!=before:raise RuntimeError('live final metadata opened7ID changed')
                                    raw=os.pread(f,765,0);q=os.fstat(f)
                                    after=[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
                                    q=path.lstat();current=[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
                                    if after!=before or current!=before or len(raw)!=s.st_size:
                                        raise RuntimeError('live final metadata full7ID changed')
                                    row['final_metadata_kind']=empty_final_metadata_kind(raw)
                                finally:os.close(f)
                        yield row
            finally:os.close(fd)
    def check(self):
        if self.observation is not None:self.observation.checkpoint('phase.check.before',self.phase)
        try:
            r=self.original.check();fresh=r['fresh_output']['artifact_bytes']
            accounting=classify_storage_inventory(self.phase,self.inventory(),self.pending_publication_reserved_bytes,self.seal_seen)
            if self.phase=='BOOT':self.seal_seen=accounting['final_payload_seen']
            if fresh+self.pending_publication_reserved_bytes>=2*2**30:raise RuntimeError('original total fresh2GiB')
            self.peaks[self.phase]=max(self.peaks.get(self.phase,0),fresh,accounting['inventory_bytes'])
            self.aux_peaks[self.phase]=max(self.aux_peaks.get(self.phase,0),accounting['aux_bytes'])
            return dict(r,publication_reserved_bytes=self.pending_publication_reserved_bytes,actual_phase=self.phase,
                        observed_fresh_peak_bytes=self.peaks[self.phase],storage_inventory=accounting,
                        observed_aux_peak_bytes=self.aux_peaks[self.phase])
        finally:
            if self.observation is not None:self.observation.checkpoint('phase.check.after',self.phase)
'''

def changes(original):
    a=original.index('class PhaseResources:');b=original.index('\ndef main():',a)
    run_old=original[original.index('    def run(label,deck,marker=None):'):original.index('    def refuse(label,deck,message):')]
    run_new=run_old.replace('        error=None\n','').replace('        except BaseException as exc:error=exc\n','').replace('        if error is not None:raise error\n','')
    refusal=original[original.index('    def refuse(label,deck,message):'):original.index('    def cleanup(names,why,evidence):')]
    fixed=refusal.replace('error=None','error=None;error_tb=None').replace('except RuntimeError as exc:error=str(exc)','except RuntimeError as exc:error=exc;error_tb=exc.__traceback__')
    fixed=fixed.replace("        stash_closed_driver_scratch(label)\n",'')
    fixed=fixed.replace("        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')", "        if error is not None and str(error)!='own-child stage failed; no retry':raise error.with_traceback(error_tb)\n        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')")
    fixed=fixed.replace("if error!='own-child stage failed; no retry'", "if str(error)!='own-child stage failed; no retry'")
    fixed=fixed.replace('        cases.append(dict(case=label,expected_abort=message', '        stash_closed_driver_scratch(label)\n        cases.append(dict(case=label,expected_abort=message',1)
    pub=original[original.index('    # Complete unmodified original execution records'):original.index("\nif __name__=='__main__':main()")]
    pub_new=pub.replace("failure=failure,after_check_error=after_error,records=", "failure=failure,after_check_error=after_error,first_failure_secondary_errors=list(first.secondary),records=")
    pub_new=pub_new.replace("    except BaseException as exc:\n        observation.frozen=True", "    except BaseException as exc:\n        first.capture(exc,'journal_publication')\n        observation.frozen=True")
    pub_new=pub_new.replace("    except BaseException as exc:\n        if not isinstance(exc,ParentObservationFailure)", "    except BaseException as exc:\n        first.capture(exc,'publication_full_EOF')\n        if not isinstance(exc,ParentObservationFailure)")
    pub_new=pub_new.replace("    except BaseException as original_late_exc:\n", "    except BaseException as original_late_exc:\n        first.capture(original_late_exc,'late_resource_check')\n")
    for indent in ('        ','    '):
        pub_new=pub_new.replace(indent+"except BaseException as exc:\n"+indent+"    if observation.first_error is None:observation.first_error='late observation tail:",indent+"except BaseException as exc:\n"+indent+"    first.capture(exc,'late_observation_tail')\n"+indent+"    if observation.first_error is None:observation.first_error='late observation tail:")
    pub_new=pub_new.replace("        if isinstance(original_late_exc,ParentObservationFailure) and (failure is not None or after_error is not None):\n            raise RuntimeError(failure or after_error)\n        raise", "        first.reraise()")
    pub_new=pub_new.replace('        raise RuntimeError(failure or after_error)','        first.reraise()')
    pub_new=pub_new.replace("    if not closed:raise RuntimeError(failure or after_error or 'no actual terminal')", "    if not closed:\n        first.reraise()\n        raise RuntimeError('no actual terminal')")
    pub_new=pub_new.replace('    observation.require_healthy()','    first.reraise()\n    observation.require_healthy()')
    pub_new='    with first:\n'+''.join('    '+line if line.strip()else line for line in pub_new.splitlines(keepends=True))
    return [
      dict(old_block="axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13",new_block=OUT.name),
      dict(old_block='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V13',new_block='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V14'),
      dict(old_block=" 'BOOT':{'maximum_live':['PROJECT','private solved archive','closed final archive','remaining128MiB'],\n         'upper_bound_bytes':(800+480+480+128)*MI},",new_block=" 'BOOT_solve':{'maximum_live':['PROJECT','private solved archive','one same-plane Q','one MAC','remaining128MiB including empty final metadata'],\n               'upper_bound_bytes':(800+480+560+16+128)*MI},\n 'BOOT_seal':{'maximum_live':['PROJECT','private solved archive','closed final archive','remaining128MiB; Q/MAC absent'],\n              'upper_bound_bytes':(800+480+480+128)*MI},"),
      dict(old_block=original[a:b],new_block=STORAGE_HELPERS),
      dict(old_block='ledger=[];proofs=[];cases=[];failure=None;after_error=None;result=None',new_block='ledger=[];proofs=[];cases=[];failure=None;after_error=None;result=None;first=FirstFatal()'),
      dict(old_block=run_old,new_block=run_new),dict(old_block=refusal,new_block=fixed),
      dict(old_block="    except BaseException as exc:failure=type(exc).__name__+': '+str(exc)",new_block="    except BaseException as exc:\n        first.capture(exc,'execute_or_owned_proof');failure=type(exc).__name__+': '+str(exc)"),
      dict(old_block="        except BaseException as exc:after_error=type(exc).__name__+': '+str(exc);after=None",new_block="        except BaseException as exc:\n            first.capture(exc,'after_resource_check');after_error=type(exc).__name__+': '+str(exc);after=None"),
      dict(old_block=pub,new_block=pub_new)]

def candidate(old):
    raw=Path(old['host_source']['path']).read_bytes();original=raw.decode();cs=changes(original);text=original
    for row in cs:
        need(text.count(row['old_block'])==1,'one exact forward HOST block');text=text.replace(row['old_block'],row['new_block'],1)
    restored=text
    for row in reversed(cs):
        need(restored.count(row['new_block'])==1,'one exact reverse HOST block');restored=restored.replace(row['new_block'],row['old_block'],1)
    need(restored.encode()==raw,'entire original v13 HOST bytes restored');ast.parse(text)
    return text,cs

def fixtures(source):
    tree=ast.parse(source);names={'MI','BOOT_EMPTY_XSM_PREFIX','BOOT_EMPTY_XSM_IMAGE','empty_final_metadata_kind','classify_storage_inventory','FirstFatal'}
    selected=[n for n in tree.body if (isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name in names)or(isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id in names for t in n.targets))]
    need(len(selected)==6,'exact six pure helper nodes; candidate not imported')
    ns={};exec(compile(ast.Module(body=selected,type_ignores=[]),'<pure-v14-fixture-only>','exec'),ns)
    mi=2**20;classify=ns['classify_storage_inventory'];passed=[]
    def row(name,n=0,kind=None,mode=0o100600,nlink=1):
        r=dict(relative_path='AAA/'+name,size_bytes=n,mode=mode,nlink=nlink)
        if kind is not None:r['final_metadata_kind']=kind
        return r
    empty=[row('closed_boot_axial.xsm',44,'empty'),row('closed_boot_archive.xsm',44,'empty')]
    base=[row('projected_boot.xsm',800*mi),row('BOOT-SOLVED-STAGE.xsm',480*mi)]+empty
    def test(label,items,phase='BOOT',reserve=0,seal=False,refuse=False):
        try:r=classify(phase,items,reserve,seal)
        except RuntimeError:
            need(refuse,'unexpected pure fixture refusal:'+label);passed.append(label);return
        need(not refuse,'pure fixture unexpectedly admitted:'+label);passed.append(label);return r
    test('solve_exact1984MiB',base+[row('BOOT-Q-1.xsm',560*mi),row('BOOT-MAC-1.xsm',16*mi),row('log',128*mi-88)])
    for p in range(1,4):
        test('MAC_only_'+str(p),base+[row('BOOT-MAC-'+str(p)+'.xsm',16*mi)])
        test('same_plane_pair_'+str(p),base+[row('BOOT-Q-'+str(p)+'.xsm',560*mi),row('BOOT-MAC-'+str(p)+'.xsm',16*mi)])
    test('between_planes_none',base)
    test('prepare_final_absent',[row('projected_boot.xsm',800*mi)])
    test('prepare_final_zero',[row('closed_boot_axial.xsm',0,'creating'),row('closed_boot_archive.xsm',0,'creating')])
    for label,items,kw in [
      ('Q_only',base+[row('BOOT-Q-1.xsm')],{}),('two_Q',base+[row('BOOT-Q-1.xsm'),row('BOOT-Q-2.xsm')],{}),
      ('two_MAC',base+[row('BOOT-MAC-1.xsm'),row('BOOT-MAC-2.xsm')],{}),('mismatched_planes',base+[row('BOOT-Q-1.xsm'),row('BOOT-MAC-2.xsm')],{}),
      ('wrong_phase',base+[row('BOOT-MAC-1.xsm')],{'phase':'GLOBAL'}),('wrong_index',base+[row('BOOT-Q-4.xsm')],{}),
      ('Q_cap_plus1',base+[row('BOOT-Q-1.xsm',560*mi+1),row('BOOT-MAC-1.xsm')],{}),('MAC_cap_plus1',base+[row('BOOT-MAC-1.xsm',16*mi+1)],{}),
      ('aux_plus1',base+[row('log',128*mi-88+1)],{}),('reserve_plus1',base+[row('log',128*mi-88)],{'reserve':1}),
      ('payload_with_MAC',base[:-1]+[row('closed_boot_archive.xsm',1000,'payload'),row('BOOT-MAC-1.xsm')],{}),
      ('creating_with_MAC',base[:-1]+[row('closed_boot_archive.xsm',12,'creating'),row('BOOT-MAC-1.xsm')],{}),
      ('zero_final_with_MAC',base[:-1]+[row('closed_boot_archive.xsm',0,'creating'),row('BOOT-MAC-1.xsm')],{}),
      ('zero_final_with_Q_MAC',base[:-1]+[row('closed_boot_archive.xsm',0,'creating'),row('BOOT-MAC-1.xsm'),row('BOOT-Q-1.xsm')],{}),
      ('unknown_final_role',base[:-1]+[row('closed_boot_archive.xsm',44,'unknown')],{}),
      ('MAC_after_seal',base+[row('BOOT-MAC-1.xsm')],{'seal':True}),('wrong_file_type',[row('log',0,mode=0o120777)],{}),
      ('hardlink',[row('log',0,nlink=2)],{}),('total_exact2GiB',[row('projected_boot.xsm',800*mi),row('negative_project.xsm',800*mi),row('negative_pack.xsm',448*mi)],{})]:
        test(label,items,refuse=True,**kw)
    for name,cap in [('initial_pack.xsm',480),('global.xsm',560),('BOOT-GLOBAL64-STAGE.xsm',560),('projected_boot.xsm',800),('negative_pack.xsm',480),('negative_project.xsm',800),('BOOT-SOLVED-STAGE.xsm',480)]:
        test('original_principal_cap_'+name,[row(name,cap*mi)])
        test('original_principal_cap_plus1_'+name,[row(name,cap*mi+1)],refuse=True)
    test('final_archive_cap_plus1',[row('closed_boot_archive.xsm',480*mi+1,'payload')],refuse=True)
    r=test('seal_exact1888MiB',[row('projected_boot.xsm',800*mi),row('BOOT-SOLVED-STAGE.xsm',480*mi),row('closed_boot_archive.xsm',480*mi,'payload'),row('closed_boot_axial.xsm',128*mi,'payload')]);need(r['final_payload_seen'],'seal latch')
    test('context_same_basename_is_aux',[dict(relative_path='runtime/BOOT-Q-1.xsm',size_bytes=128*mi+1,mode=0o100600,nlink=1)],refuse=True)
    for n in [0,1,12,43,44,45,763,764]:
        need(ns['empty_final_metadata_kind'](ns['BOOT_EMPTY_XSM_IMAGE'][:n])==('creating'if n<44 else 'empty'),'canonical live metadata prefix');passed.append('empty_prefix_'+str(n))
    for raw in [ns['BOOT_EMPTY_XSM_IMAGE']+b'\0',b'bad',ns['BOOT_EMPTY_XSM_PREFIX'][:-1]+b'x']:
        need(ns['empty_final_metadata_kind'](raw)=='payload','noncanonical payload');passed.append('reject_noncanonical_'+str(len(raw)))
    class OriginalResource(RuntimeError):pass
    first=ns['FirstFatal']();primary=OriginalResource('original-cap');secondary=RuntimeError('later-archival')
    def original_origin():raise primary
    try:original_origin()
    except OriginalResource as exc:first.capture(exc,'execute');original_tb=exc.__traceback__
    first.capture(secondary,'after');need(first.error is primary and first.traceback is original_tb and len(first.secondary)==1,'first object tb retained')
    try:
        with first:raise RuntimeError('late-publication')
    except OriginalResource as exc:
        need(exc is primary and len(first.secondary)==2,'context preserves identity/class')
        names=[];tb=exc.__traceback__
        while tb:names.append(tb.tb_frame.f_code.co_name);tb=tb.tb_next
        need('original_origin'in names,'original traceback frame retained')
    else:need(False,'original error not reraised')
    passed.append('first_exception_identity_type_original_traceback_secondary_retained')
    return dict(schema='FINITE_V14_PURE_STORAGE_AND_EXCEPTION_BOUNDARIES_V1',status='PASS_PURE_HELPER_BOUNDARIES_ONLY',cases=passed,case_count=len(passed),candidate_imported=False,selected_pure_helpers_executed=True,compiler_or_numeric_child_started=False,full50_runtime_proven=False,AAA_qualified=False,ABA_admitted=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['draft','prepare'])
    for x in ('summary','sha256','seven-id'):p.add_argument('--independent-review-'+x)
    a=p.parse_args();old,oldpin=read(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');cli,clip=read(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V13_ARGV_20261013.json')
    need(len(old['dependencies'])==354,'exact original354 dependency rows')
    for row in old['dependencies']+[old['host_source']]+list(cli['mandatory_external_bindings'].values()):pin(row['path'],row)
    lifetime,lp=read(REVIEW/'REVIEW.json');lpp=pin(REVIEW/'ACTUAL_SOURCE_EOF_PINS.json');lpt=pin(REVIEW/'REPORT.txt')
    need(lifetime['status']=='CONDITIONAL_HOST_ONLY_FIX_FEASIBLE_NOT_EXECUTION_OR_QUALIFICATION','actual independent Source-only basis')
    text,cs=candidate(old)
    need(not NEW.exists()and not NEW.is_symlink()and not OUT.exists()and not OUT.is_symlink(),'fresh Source/business namespace')
    if a.mode=='draft':
        need(not DRAFT.exists()and not DRAFT.is_symlink(),'once-only draft namespace');DRAFT.mkdir()
        save(DRAFT/'run_actual_three_plane_pipeline.py',text.encode())
        for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):save(DRAFT/name,(OLD/name).read_bytes())
        write(DRAFT/'EXACT_ORDERED_HOST_CHANGES.json',dict(old_host_pin=old['host_source'],changes=cs,ENTIRE_v13_inverse_byte_equal=True,original354_dependencies_unchanged=True))
        fixture=fixtures(text);write(DRAFT/'FINITE_PURE_BOUNDARY_FIXTURE.json',fixture)
        write(DRAFT/'DRAFT_SOURCE_ONLY_HANDOFF.json',dict(schema='DRAFT_V14_HOST_STORAGE_EXCEPTION_SOURCE_ONLY_V1',status='UNFROZEN_REQUIRES_INDEPENDENT_EXACT_SOURCE_REVIEW',candidate_source_pin=pin(DRAFT/'run_actual_three_plane_pipeline.py'),fixture_pin=pin(DRAFT/'FINITE_PURE_BOUNDARY_FIXTURE.json'),changes_pin=pin(DRAFT/'EXACT_ORDERED_HOST_CHANGES.json'),preparer_pin=pin(__file__),predecessor_HF_pin=oldpin,original354_dependency_count=354,independent_lifetime_review_pin=lp,new_source_namespace=str(NEW),new_business_namespace=str(OUT),compiler_or_business_executed=False,final_manifest_frozen=False,AAA_qualified=False,ABA_admitted=False))
        print(json.dumps(dict(draft_handoff_pin=pin(DRAFT/'DRAFT_SOURCE_ONLY_HANDOFF.json'),fixture_pin=pin(DRAFT/'FINITE_PURE_BOUNDARY_FIXTURE.json'),candidate_source_pin=pin(DRAFT/'run_actual_three_plane_pipeline.py'),final_manifest_frozen=False)));return
    need(all(getattr(a,'independent_review_'+x.replace('-','_'))for x in ('summary','sha256','seven-id')),'explicit peer full pin mandatory')
    seven=json.loads(a.independent_review_seven_id);wanted=dict(path=a.independent_review_summary,sha256=a.independent_review_sha256,size_bytes=seven[4],identity=seven)
    peer,peerpin=read(wanted['path'],wanted);draft,dp=read(DRAFT/'DRAFT_SOURCE_ONLY_HANDOFF.json')
    need(peer.get('status')=='PASS_V14_SOURCE_ONLY_READY_FOR_PREPARATION'and not peer.get('failure'),'exact actual independent peer PASS')
    need(peer['draft_handoff_pin']==dp and peer['preparer_pin']==pin(__file__) and peer['candidate_source_pin']==pin(DRAFT/'run_actual_three_plane_pipeline.py'),'peer exact final draft Source')
    need(peer['fixture_pin']==pin(DRAFT/'FINITE_PURE_BOUNDARY_FIXTURE.json')and peer['changes_pin']==pin(DRAFT/'EXACT_ORDERED_HOST_CHANGES.json'),'peer exact finite proof and inverse changes')
    pt,ptp=read(Path(peerpin['path']).parent/'TRUE_TOOL_RETURNS.json')
    need(type(pt['original_integer_exit_code'])is int and pt['original_integer_exit_code']==0 and pt['observed_closed']is True and type(pt['genuine_actual_review_tool_return']['exit_code'])is int and pt['genuine_actual_review_tool_return']['exit_code']==0 and json.loads(pt['genuine_actual_review_tool_return']['output'])['review_pin']==peerpin,'genuine independent closed0 tool tied to exact peer review')
    need((DRAFT/'run_actual_three_plane_pipeline.py').read_bytes()==text.encode(),'final draft HOST exact bytes')
    need(draft['predecessor_HF_pin']==oldpin and draft['preparer_pin']==pin(__file__),'unchanged predecessor and reviewed preparer')
    NEW.mkdir();save(NEW/'run_actual_three_plane_pipeline.py',text.encode())
    for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):
        need((DRAFT/name).read_bytes()==(OLD/name).read_bytes(),'all three helper whole bytes unchanged');save(NEW/name,(OLD/name).read_bytes())
    alias,_=read(OLD/'DIRECT_ALIAS_ENTRY_BINDING.json');alias['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90');write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',alias)
    interface,_=read(OLD/'DECLARED_EXECUTION_INTERFACE.json');interface.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V14',host_source=str(NEW/'run_actual_three_plane_pipeline.py'),output_root=str(OUT),Source_revision_scope='HOST storage role accounting and first fatal exception fidelity only; original50 unchanged');write(NEW/'DECLARED_EXECUTION_INTERFACE.json',interface)
    hostpin=pin(NEW/'run_actual_three_plane_pipeline.py');inverse=dict(schema='COMPLETE_V13_TO_V14_BOOT_STORAGE_EXCEPTION_BYTE_INVERSE_V1',old_host_source_pin=old['host_source'],new_host_source_pin=hostpin,exact_ordered_changes=cs,ENTIRE_v13_HOST_inverse_byte_equal=True,three_helpers_whole_bytes_unchanged=True,original50_17positive_33negative_math_and_caps_unchanged=True,original354_dependency_rows=old['dependencies'],independent_Source_review_pin=peerpin,pure_fixture_pin=peer['fixture_pin'],actual_pipeline_executed=False,AAA_qualified=False,ABA_admitted=False)
    write(NEW/'COMPLETE_V13_TO_V14_BOOT_STORAGE_EXCEPTION_BYTE_INVERSE.json',inverse)
    local=[pin(x)for x in sorted(NEW.iterdir())];extra=[oldpin,old['host_source'],clip,lp,lpp,lpt,peerpin,ptp,dp,pin(__file__)]+[pin(x)for x in sorted(DRAFT.iterdir())]
    table={row['path']:row for row in old['dependencies']}
    for row in extra+local:
        need(row['path']not in table or table[row['path']]==row,'dependency exact pin has no conflict');table[row['path']]=row
    hf=copy.deepcopy(old);hf.update(schema='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V14',host_source=hostpin,dependencies=list(table.values()),predecessor_host_freeze=oldpin,Source_revision_scope=interface['Source_revision_scope'],complete_original_v13_dependency_rows_retained=354,complete_V13_to_V14_byte_inverse_pin=pin(NEW/'COMPLETE_V13_TO_V14_BOOT_STORAGE_EXCEPTION_BYTE_INVERSE.json'),independent_V14_Source_review_pin=peerpin,independent_V14_true_tool_returns_pin=ptp,independent_V13_Q_MAC_lifetime_review_pin=lp,finite_pure_boundary_fixture_pin=peer['fixture_pin'],finite_fixture_is_not_full50_runtime_proof=True,original_business_initial_fresh_reserve_bytes=2*2**30,prepared_only=True,actual_pipeline_executed=False,actual_pipeline_executed_by_this_prepare=False,actual_qualified_numeric_pipeline=False,physics_qualification=False,memory_repair_claimed=False,memory_repair_full_pipeline_proven=False,no_prefilled_actual_success=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    for row in hf['dependencies']+[hostpin]:pin(row['path'],row)
    write(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',hf);hp=pin(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
    freshcli=copy.deepcopy(cli);argv=list(cli['argv']);argv[argv.index(str(OLD/'run_actual_three_plane_pipeline.py'))]=str(NEW/'run_actual_three_plane_pipeline.py')
    for suffix,value in [('summary',hp['path']),('sha256',hp['sha256']),('seven-id',json.dumps(hp['identity'],separators=(',',':')))]:argv[argv.index('--host-freeze-'+suffix)+1]=value
    freshcli['mandatory_external_bindings']['host-freeze']=hp;freshcli.update(schema='ROOT_REVIEWABLE_EXACT_ACTUAL_PIPELINE_V14_BOOT_STORAGE_EXCEPTION_ARGV_V1',argv=argv,Source_revision_scope=hf['Source_revision_scope'],independent_V14_Source_review_pin=peerpin,actual_pipeline_executed=False,prepared_only=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    for key,row in cli['mandatory_external_bindings'].items():need(key=='host-freeze'or freshcli['mandatory_external_bindings'][key]==row,'six actual external parameters unchanged')
    cp=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V14_ARGV_20261013.json';write(cp,freshcli);cpp=pin(cp)
    hand=REC/'FINAL_PIPELINE_V14_BOOT_STORAGE_EXCEPTION_SOURCE_HANDOFF_20261013.json';write(hand,dict(schema='FINAL_V14_BOOT_STORAGE_EXCEPTION_SOURCE_ONLY_HANDOFF_V1',status='PREPARED_ONLY_REQUIRES_ROOT_AND_SPACE_ADMISSION',host_freeze_pin=hp,CLI_pin=cpp,inverse_pin=hf['complete_V13_to_V14_byte_inverse_pin'],peer_review_pin=peerpin,pure_fixture_pin=peer['fixture_pin'],dependencies=len(hf['dependencies']),original354_rows_retained=True,Source_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,actual_pipeline_executed=False,no_future_success_prefilled=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
    print(json.dumps(dict(handoff_pin=pin(hand),host_freeze_pin=hp,CLI_pin=cpp,dependency_count=len(hf['dependencies']),Source_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':main()

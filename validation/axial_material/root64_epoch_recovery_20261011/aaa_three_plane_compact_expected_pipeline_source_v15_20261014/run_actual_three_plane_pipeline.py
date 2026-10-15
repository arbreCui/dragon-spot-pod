#!/usr/bin/env python3
"""Actual three-plane operator, GLOBAL, projection and online BOOT under old limits.

Requires external full pins for three actual independent producer reports, the
actual new70 build, old current17, Fortran freeze and this complete Host freeze.
All large data objects stay XSM. Only owned, proved obsolete temporary copies may
be unlinked after closed child/watchdog and full independent whole-tree readback.
No implicit producer, rank default, retry, material change or physics certificate.
"""
import argparse
import gc
import importlib.util
import json
import os
import stat
import subprocess
from pathlib import Path
import shutil
import time
import actual_inputs_and_readback as data

R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
COMMON=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py')
spec=importlib.util.spec_from_file_location('pipeline_original_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
HERE=Path(__file__).resolve().parent
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261014-v15')
WORK=OUT/'AAA'
MI=2**20
ROOT_NAMES={'AX':'ax_current.xsm','AXTRACK':'axial_track.xsm','AXSYSTEM':'initial_system.xsm',
            'AXMACRO':'axial_macro.xsm','ARCHIVE':'initial_pack.xsm','RCON':'global_rcon.xsm'}
PREFIX='''XSM_FILE MACRO :: FILE './axial_macro.xsm' ;
XSM_FILE AXTRACK :: FILE './axial_track.xsm' ;
XSM_FILE BASIS :: FILE './basis.xsm' ;
XSM_FILE PACK :: FILE './initial_pack.xsm' ;
XSM_FILE GRCON :: FILE './global_rcon.xsm' ;
XSM_FILE RCON1 :: FILE './plane1_rcon.xsm' ;
XSM_FILE RCON2 :: FILE './plane2_rcon.xsm' ;
XSM_FILE RCON3 :: FILE './plane3_rcon.xsm' ;
'''
BOOT_PREFIX='''XSM_FILE PROJECT :: FILE './projected_boot.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE AXTRACK :: FILE './axial_track.xsm' ;
XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AXMACRO :: FILE './axial_macro.xsm' ;
XSM_FILE GRCON :: FILE './global_rcon.xsm' ;
SEQ_BINARY TRACK_f1 :: FILE './radial1.bin' ;
SEQ_BINARY TRACK_f2 :: FILE './radial2.bin' ;
SEQ_BINARY TRACK_f3 :: FILE './radial3.bin' ;
LINKED_LIST MICROLIB2 MACRO0 TRACK SYS1 SYS2 SYS3 ;
MODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 1 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS1 := ASM: MACRO0 TRACK TRACK_f1 PROJECT :: EDIT 0 ARM LK1D 1 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 2 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS2 := ASM: MACRO0 TRACK TRACK_f2 PROJECT :: EDIT 0 ARM LK1D 2 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 3 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS3 := ASM: MACRO0 TRACK TRACK_f3 PROJECT :: EDIT 0 ARM LK1D 3 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
'''

# Conditional physical file bounds are host planning gates, never measured peaks.
# Old fixed producer files/reports remain protected outside this fresh namespace.
STORAGE_FORECAST={
 'pack':{'maximum_live':['3 owned producer aliases','PACK','small independent context/runtime/metadata'],
         'upper_bound_bytes':3*156880856+(480+128)*MI},
 'initial_controls':{'maximum_live':['PACK','one private negative PACK','remaining128MiB'],
                     'upper_bound_bytes':(480+480+128)*MI},
 'GLOBAL':{'maximum_live':['PACK','private GLOBAL stage','GLOBAL','remaining128MiB'],
           'upper_bound_bytes':(480+560+560+128)*MI},
 'projection':{'maximum_live':['PACK','GLOBAL','one private PROJECT','remaining128MiB'],
               'upper_bound_bytes':(480+560+800+128)*MI},
 'retained_global_negative':{'maximum_live':['PROJECT','one private negative PROJECT','remaining128MiB'],
                            'upper_bound_bytes':(800+800+128)*MI},
 'BOOT_solve':{'maximum_live':['PROJECT','private solved archive','one same-plane Q','one MAC','compact expected SRC32MiB','expected MAC16MiB','remaining128MiB including empty final metadata'],
               'upper_bound_bytes':(800+480+560+16+32+16+128)*MI},
 'BOOT_seal':{'maximum_live':['PROJECT','private solved archive','closed final archive','remaining128MiB; Q/MAC absent'],
              'upper_bound_bytes':(800+480+480+128)*MI},
 'final_retained':{'maximum_live':['PROJECT retains entire independent GLOBAL/producer archive',
                                 'closed final archive','all final axial/context/runtime/log/proof files within128MiB'],
                   'upper_bound_bytes':(800+480+128)*MI},
 'all_forecasts_are_conditional_guard_bounds_not_actual_sizes':True,
 'fresh_original_cap_bytes':2*2**30,
 'whole_EOF_and_complete_tree_proof_required_before_each_temporary_release':True}
if any(row.get('upper_bound_bytes',0)>=2*2**30 for row in STORAGE_FORECAST.values()if isinstance(row,dict)):
    raise RuntimeError('storage Source forecasting must fit unchanged fresh2GiB')

def ext(args,prefix):
    return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))

def unique(rows):
    out={}
    for row in rows:
        if row['path']in out and out[row['path']]!=row:raise RuntimeError('inconsistent independent full pins')
        out[row['path']]=row
    return list(out.values())

class ParentObservationFailure(RuntimeError):
    pass

class ParentMemoryObservation:
    """Scalar observations only; no guard, Thread, GC or peak reset."""
    MAX_RECORDS=10000
    MAX_BYTES=8*2**20
    MAX_LATE_RECORDS=64
    def __init__(self,start):
        self.start=start;self.rows=[];self.late=[];self.first_error=None
        self.frozen=False;self.journal_pin=None;self.journal_bytes=0
        self.phase=lambda:'admission';self.stage=lambda:-1
    def checkpoint(self,status,phase=None):
        try:
            sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],
                                  capture_output=True,text=True,timeout=2)
            if sample.returncode!=0 or not sample.stdout.strip().isdigit():
                raise RuntimeError('true owning SELF RSS unavailable')
            row=dict(status=str(status),phase=str(self.phase() if phase is None else phase),
                     elapsed_seconds=time.monotonic()-self.start,
                     current_RSS_bytes=int(sample.stdout.strip())*1024,
                     SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
                     allocated_blocks=c.sys.getallocatedblocks(),gc_count=list(gc.get_count()),
                     stage_index=self.stage())
            if len(self.rows)+len(self.late)>=self.MAX_RECORDS:
                raise RuntimeError('parent observation maximum10000 scalar records reached')
            if len(row['status'])>96 or len(row['phase'])>96:
                raise RuntimeError('parent observation scalar status or phase exceeds96 characters')
            if self.frozen:
                if len(self.late)>=self.MAX_LATE_RECORDS:
                    raise RuntimeError('parent observation bounded64 late scalar records reached')
                self.late.append(row)
            else:self.rows.append(row)
        except BaseException as exc:
            if self.first_error is None:self.first_error=type(exc).__name__+': '+str(exc)[:256]
    def require_healthy(self):
        if self.first_error is not None:raise ParentObservationFailure(self.first_error)
    def freeze(self,path):
        if self.frozen or self.journal_pin is not None:
            raise RuntimeError('parent observation journal write once only')
        payload=dict(schema='ACTUAL_PARENT_MEMORY_CHECKPOINT_JOURNAL_V1',
                     purpose='locate earlier parent memory growth',records=self.rows,
                     first_observation_error=self.first_error,original_guard_and_math_unchanged=True,
                     memory_repair_claimed=False,AAA_qualified=False,ABA_admitted=False)
        self.journal_bytes=sum(len(chunk.encode('utf-8')) for chunk in
            json.JSONEncoder(indent=2,ensure_ascii=False,allow_nan=False).iterencode(payload))+1
        if self.journal_bytes>self.MAX_BYTES:
            if self.first_error is None:self.first_error='parent observation exceeds original8MiB publication'
            raise RuntimeError(self.first_error)
        self.frozen=True
        c.write(path,payload)
    def summary(self):
        return dict(purpose='locate earlier parent memory growth',journal_pin=self.journal_pin,
                    journal_bytes=self.journal_bytes,records=len(self.rows),maximum_records=self.MAX_RECORDS,
                    late_records=list(self.late),first_observation_error=self.first_error,
                    no_extra_GC_or_peak_reset_or_profiling_or_Thread=True,memory_repair_claimed=False)
    def same_fd_tail(self,status):
        self.checkpoint(status)
        payload=dict(schema='ACTUAL_PARENT_MEMORY_COMPACT_LATE_TAIL_V1',status=status,
                     late_records=self.late[-8:],total_late_records=len(self.late),first_observation_error=self.first_error,
                     journal_pin=self.journal_pin,original_exception_not_replaced=True,
                     memory_repair_claimed=False,AAA_qualified=False,ABA_admitted=False)
        raw=(json.dumps(payload,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n').encode()
        if len(raw)>8192:raise RuntimeError('parent observation sameFD late tail exceeds8192 bytes')
        offset=0
        while offset<len(raw):
            written=os.write(2,raw[offset:])
            if written<=0:raise RuntimeError('parent observation sameFD late tail write failed')
            offset+=written

BOOT_EMPTY_XSM_PREFIX=bytes.fromhex('2458534dbf00000003000000242424241e0000000000000003000000ffffffff2f2020202020202020202020')
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
    principal=0;aux=0;total=0;count=0;qs=[];macs=[];finals={};bq=[];seen_paths=set()
    for row in entries:
        rel=row['relative_path'];n=row['size_bytes'];count+=1
        if rel in seen_paths:raise RuntimeError('duplicate exact output inventory path')
        seen_paths.add(rel)
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
        elif name in ('BQ64-MAC-ST','BQ64-SRC-ST'):
            if not direct or phase!='BOOT':raise RuntimeError('literal BOOT-only expected BQ stage role required')
            cap=(16 if name=='BQ64-MAC-ST'else 32)*MI
            if n>cap:raise RuntimeError('strict compact expected storage planning bound exceeded: '+name)
            bq.append(name);principal+=n
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
    if bq:
        if set(bq)not in ({'BQ64-MAC-ST'},{'BQ64-MAC-ST','BQ64-SRC-ST'})or len(bq)!=len(set(bq))or len(qs)!=1 or macs!=qs:
            raise RuntimeError('expected BQ stages require unique same-plane outer Q/MAC and MAC-first/SRC-first-close lifetime')
        if seal_seen or payload or finals!={'closed_boot_axial.xsm':'empty','closed_boot_archive.xsm':'empty'}:
            raise RuntimeError('expected BQ stages require canonical empty final pair and no seal')
    if aux+reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')
    if total+reserved_bytes>=2*2**30:raise RuntimeError('original total fresh2GiB')
    return dict(principal_bytes=principal,aux_bytes=aux,inventory_bytes=total,regular_files=count,
                Q_plane=qs[0]if qs else None,MAC_plane=macs[0]if macs else None,
                expected_BQ_stage_names=sorted(bq),
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

# These admission routines read genuine completed prerequisites only. They do
# not execute a compiler/control, reuse an old-reader PASS, or grant physics.
def selected_pin(hf,key):
    row=hf.get(key)
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}:
        raise RuntimeError('exact actual selected prerequisite fullpin required: '+key)
    table={x['path']:x for x in unique(hf['dependencies'])}
    if table.get(row['path'])!=row:raise RuntimeError('selected actual prerequisite belongs to owning HF: '+key)
    return row

def read_selected(hf,key):
    chosen=selected_pin(hf,key)
    value,checked=c.read_bound_json_current(chosen['path'],chosen)
    if checked!=chosen:raise RuntimeError('selected current prerequisite fullpin: '+key)
    return value,chosen

def current_pin_table(rows):
    return {row['path']:row for row in unique(rows)}

def compact_log_rows(root,record):
    label=record['label']
    if not isinstance(label,str)or label.startswith('/')or any(x in ('','..','.')for x in label.split('/')):
        raise RuntimeError('exact owned prerequisite stage label')
    path=root/(label+'.log');pf=c.pin(path)
    if pf['sha256']!=record['log_sha256']:raise RuntimeError('closed prerequisite full log SHA')
    rows=[]
    with path.open('r',encoding='utf-8',errors='strict')as stream:
        for line in stream:
            if len(line)>65536:raise RuntimeError('bounded actual control JSON line')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                value=json.loads(line)
                if isinstance(value,dict):rows.append(value)
    c.same_pin(path,pf);return rows,pf

def exact_counter_oracles(actual,declared,prefixes):
    for key,value in declared.items():
        if key.startswith(prefixes):
            observed=actual.get(key[9:])
            if type(value)is not int or type(observed)is not int or observed!=value:
                raise RuntimeError('exact integer actual control status/call-count: '+key)

def admit_compact_build(args,hf,helper,cache,p_cache,old9):
    build,pbuild=ext(args,'new_build70')
    if pbuild!=selected_pin(hf,'selected_actual_new_build70_report_pin')or \
       build.get('schema')!='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'or \
       build.get('status')!='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
       [x['label'].rsplit('/',1)[-1]for x in build['records']]!=['compile_BOOTQ','link_Dragon']or \
       any(build.get(k)is not True for k in ('Dragon_linked','final_report_resource_check_passed',
         'original69_other_inputs_identical_and_retained','original_four_archives_identical_and_retained',
         'original_eight_unchanged_core_objects_identical_and_retained'))or \
       any(build.get(k)is not False for k in ('transport_executed','new_entry_controls_executed','new_reader_control_qualification')):
        raise RuntimeError('genuine closed2 compact BOOTQ build prerequisite')
    c.closed_report(build,helper,Path(pbuild['path']).parent,2)
    if build.get('secondary_failures')!=[]or any(build.get(k)is not False for k in c.scope()):
        raise RuntimeError('no secondary actual build failure or inherited physics scope')
    bhf,pbhf=read_selected(hf,'selected_new_build_Host_freeze_pin')
    sf,psf=read_selected(hf,'selected_new_Fortran_Source_freeze_pin')
    if bhf.get('schema')!='COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'or \
       any(bhf.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported_or_executed'))or \
       sf.get('schema')!='COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'or \
       sf.get('source_only')is not True or any(sf.get(k)is not False for k in ('compiled','numerical_executed'))or \
       bhf['selected_new_Fortran_Source_freeze_pin']!=psf or \
       bhf['selected_original_actual_complete70_report_pin']!=p_cache:
        raise RuntimeError('exact Source-only new build Host and compact Fortran authority')
    c.verify_rows(bhf['dependencies']);c.same_pin(bhf['host_source']['path'],bhf['host_source'])
    btable=current_pin_table(bhf['dependencies'])
    pp=bhf['build_plan_pin']
    if btable.get(pp['path'])!=pp:raise RuntimeError('exact owning newbuild plan dependency')
    plan,checked=c.read_bound_json_current(pp['path'],pp)
    if checked!=pp or plan.get('source_only')is not True or \
       any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed'))or \
       any(plan.get(k)is not None for k in ('actual_new_BOOTQ_object_pin','actual_new_Dragon_pin','actual_new_build_report_pin'))or \
       plan['original_actual_complete70_report_pin']!=p_cache:
        raise RuntimeError('frozen parameterized build plan does not predict actual results')
    caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,
      SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,retries=0,
      fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,filesystem_floor_bytes=8*2**30,
      original_cold_reserve_bytes=20971764748)
    if plan['original_caps']!=caps or bhf['original_caps']!=caps or build.get('original_caps')!=caps:
        raise RuntimeError('unchanged complete original newbuild caps')
    old70=plan['original_ordered70_input_pins']
    cache_table=current_pin_table(cache['fixed_current_pins']+cache['output_pins'])
    if old70!=build['original_ordered70_input_pins']or \
       [x['path']for x in old70]!=cache['actual_complete70_link_inputs']or \
       len(old70)!=70 or len({x['path']for x in old70})!=70 or \
       any(cache_table.get(x['path'])!=x for x in old70)or \
       plan['original_nine_core_object_pins']!=old9 or build['original_nine_core_object_pins']!=old9 or \
       len(old9)!=9 or old70[40]!=old9[5]or \
       build.get('replacement_zero_based_complete70_input_index')!=40 or \
       build.get('original_actual_complete70_report_pin')!=p_cache:
        raise RuntimeError('old69 inputs and exact core6/ordered70 index40 historical mapping')
    sf_rows=unique(sf['files']+sf['original_source_pins']+[sf['complete_byte_inverse_pin'],sf['control_plan_pin']])
    c.verify_rows(sf_rows)
    source=bhf['new_production_Fortran_Source_pin']
    if source not in sf['files']or build['actual_new_Source_pin']!=source:
        raise RuntimeError('one actual new compact BOOTQ Fortran Source')
    actual_table=current_pin_table(build['fixed_current_pins']+build['output_pins'])
    if any(actual_table.get(x['path'])!=x for x in (pbhf,psf,bhf['host_source'],pp,source))or \
       build['actual_host_Source_freeze_pin']!=pbhf or build['actual_new_Source_freeze_pin']!=psf:
        raise RuntimeError('newbuild own Host/SF/Source/plan exact fixed closure')
    root=Path(pbuild['path']).parent
    objects=[x for x in build['output_pins']if x['path']==str(root/'build/SPOR64_BOOTQ64.o')]
    dragons=[x for x in build['output_pins']if x['path']==str(root/'runtime/Dragon')]
    modules=[x for x in build['output_pins']if Path(x['path']).parent==root/'build'and Path(x['path']).suffix=='.mod']
    if len(objects)!=1 or len(dragons)!=1 or not modules or plan['planned_output_root']!=str(root):
        raise RuntimeError('genuine new object/module/Dragon exact output namespace')
    obj=objects[0];new70=list(old70);new70[40]=obj
    command=build['records'][0]['command'];old_command=cache['records'][0]['command']
    includes=['-I'+str(root/'build')]+plan['original_compile_include_arguments']
    expected_compile=[old_command[0],*c.FLAGS,*includes,'-J'+str(root/'build'),'-c',source['path'],'-o',obj['path']]
    expected_link=[old_command[0],'-O2','-ffp-contract=off',*[x['path']for x in new70],'-o',dragons[0]['path']]
    if command!=expected_compile or build['records'][1]['command']!=expected_link or \
       c.FLAGS!=plan['original_compile_flags']or old_command[0]!=plan['original_compiler_pin']['path']or \
       build['actual_complete70_link_inputs']!=[x['path']for x in new70]or \
       any(actual_table.get(x['path'])!=x for x in new70):
        raise RuntimeError('exact actual compact compile and one40-only ordered70 relink')
    c.verify_rows(new70)
    return dict(report=build,report_pin=pbuild,object_pin=obj,Dragon_pin=dragons[0],module_pins=modules,
      current70_pins=new70,source_pin=source,source_freeze_pin=psf,build_Host_freeze_pin=pbhf,
      fixed=unique([pbuild,pbhf,psf,bhf['host_source'],pp]+bhf['dependencies']+sf_rows+
        build['fixed_current_pins']+build['output_pins']),caps=caps)

def admit_control_host(hf,report,role,schema,selected_hf_key,compact):
    own,pown=read_selected(hf,selected_hf_key)
    if own.get('schema')!=schema or own.get('compiler_executed')is not False or \
       own.get('selected_new_build_Host_freeze_pin')!=compact['build_Host_freeze_pin']or \
       own.get('selected_new_Fortran_Source_freeze_pin')!=compact['source_freeze_pin']or \
       report.get('actual_host_Source_freeze_pin')!=pown:
        raise RuntimeError('exact actual '+role+' owning Host freeze')
    if role=='fresh17':
        if own.get('controls_executed')is not False:raise RuntimeError('Source-only fresh17 Host premise')
    elif own.get('numerical_executed')is not False:raise RuntimeError('Source-only control Host premise')
    c.same_pin(own['host_source']['path'],own['host_source']);c.verify_rows(own['dependencies'])
    table=current_pin_table(report['fixed_current_pins']);deps=current_pin_table(own['dependencies'])
    for x in (pown,own['host_source'],compact['build_Host_freeze_pin'],compact['source_freeze_pin']):
        if table.get(x['path'])!=x:raise RuntimeError('actual control fixed own-source provenance')
    for x in (compact['build_Host_freeze_pin'],compact['source_freeze_pin']):
        if deps.get(x['path'])!=x:raise RuntimeError('own Host explicit selected compact freezes')
    if report.get('actual_new_build70_report_pin')!=compact['report_pin']:
        raise RuntimeError('control actual newbuild report identity')
    if report.get('genuine_production_new_BOOTQ_object_pin'if role=='fresh17'else'actual_new_BOOTQ_object_pin')!=compact['object_pin']:
        raise RuntimeError('same genuine new BOOTQ object across all controls')
    return own,pown

def exact_public_pin(row,path):
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}or row['path']!=str(path):
        raise RuntimeError('exact public stale fullpin path and four fields')
    identity=row['identity']
    if not isinstance(identity,list)or len(identity)!=7 or any(type(x)is not int for x in identity)or \
       not stat.S_ISREG(identity[2])or identity[3]!=1 or type(row['size_bytes'])is not int or \
       row['size_bytes']<=0 or identity[4]!=row['size_bytes']or \
       not isinstance(row['sha256'],str)or len(row['sha256'])!=64 or \
       any(x not in '0123456789abcdef'for x in row['sha256']):
        raise RuntimeError('ordinary singlelink exact public stale historical/current fullpin')
    return row

def exact_public_live_pin(report,row,path):
    exact_public_pin(row,path)
    for key in ('output_pins','owned_runtime_pins'):
        if sum(x==row for x in report[key])!=1 or any(x['path']==str(path)and x!=row for x in report[key]):
            raise RuntimeError('exact current public stale file belongs to own output/owned closure')
    c.same_pin(path,row)
    return row

def exact_public_nulls(document,keys):
    if any(key not in document or document[key]is not None for key in keys):
        raise RuntimeError('explicit null public historical/failure/future fields required')

def admit_exact_public_stale_lifetimes(hf,own,plan,report,root,exe):
    stale=report['actual_stale_host_evidence']
    if len(stale)!=2 or {x['case']for x in stale}!={'public_read_stale_BQ_SRC','public_read_stale_BQ_MAC'}:
        raise RuntimeError('exact two independent stale private stage refusals')
    life_pin=own.get('selected_completed_first_SRC_bundle_lifetime_Source_plan_pin')
    if life_pin!=selected_pin(hf,'selected_completed_first_SRC_bundle_lifetime_Source_plan_pin')or \
       plan.get('completed_first_SRC_bundle_lifetime_Source_plan_pin')!=life_pin or \
       any(own.get(k)is not True for k in ('exact_completed_first_SRC_bundle_retirement_scope_only',
          'retired_bundle_is_historical_not_current_no_generic_missing_skip',
          'original_Fortran_math_7controls_9phases_11commands_unchanged')):
        raise RuntimeError('exact frozen first completed SRC lifetime authority')
    for rows in (own['dependencies'],report['fixed_current_pins']):
        if current_pin_table(rows).get(life_pin['path'])!=life_pin:
            raise RuntimeError('public ownHF and actualreport fixed lifetime Source plan')
    life,checked=c.read_bound_json_current(life_pin['path'],life_pin)
    if checked!=life_pin or life.get('schema')!='EXACT_PUBLIC_READ_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN_V1'or \
       life.get('source_only')is not True or life.get('exact_retirement_case')!='public_read_stale_BQ_SRC'or \
       life.get('exact_bundle_relative_path')!='public_read_stale_BQ_SRC/coherent_complete_context.xsm'or \
       life.get('unchanged_Fortran_Source_pin')!=report['actual_control_Source_pin']or \
       life.get('unchanged_public_Fortran_Source_freeze_pin')!=report['actual_Source_freeze_pin']or \
       any(type(life.get(k))is not int or life[k]!=v for k,v in (
          ('logical_controls',7),('phases',9),('total_guarded_stages',11),
          ('exact_expected_read_status',1),('exact_expected_control_calls',1),('exact_expected_baseline_calls',0),
          ('maximum_live_synthetic_context_bundles',1),('original_aux_bytes',128*MI),('pending_bytes',8*MI)))or \
       any(life.get(k)is not True for k in (
          'fsynced_intent_before_single_attempt','intent_parent_entry_fsync_before_unlink',
          'exact_APFS_creation_delta_nlink_plus1_size_plus32_and_times_monotonic',
          'owned_directory_fd_NOFOLLOW_UID_singlelink_full_identity',
          'only_exact_new_owned_completed_SRC_bundle_unlink_authorized',
          'truthful_attempted_returned_unlink_parent_fsync_receipt_before_close_or_any_after_check',
          'receipt_and_intent_retained_as_current_owned_metadata','only_retired_bundle_removed_from_current_owned_PFs',
          'original_before_and_after_completed_read_PFs_retained_as_historical_time_facts',
          'original_manifest_sentinel_both_logs_current_and_unchanged','second_MAC_bundle_retained_current_through_final_report',
          'no_sparse_compression_move_threshold_or_generic_missing_skip','no_retries','old_v5_output_unmodified',
          'Fortran_math_old17_phase_oracle_flags_firsterror_unchanged',
          'downstream_v15_only_SRC_exact_completed_retirement_proof_admission_required'))or \
       any(life.get(k)is not False for k in ('compiler_executed','numerical_executed','reader_qualified')):
        raise RuntimeError('original public lifetime Source plan without future success claims')
    exact_public_nulls(life,('future_actual_retirement_receipt_pin','future_actual_public7_report_pin'))
    retirements=report.get('actual_completed_bundle_retirements')
    if not isinstance(retirements,list)or len(retirements)!=1:
        raise RuntimeError('one genuine completed first SRC retirement event')
    for evidence in stale:
        name=evidence['case'];cwd=root/name
        before=exact_public_live_pin(report,evidence['actual_before_manifest_pin'],cwd/'Host_independent_stale_before_full_EOF_SHA_all7.json')
        value,checked=c.read_bound_json_current(before['path'],before)
        prepare_record=next(x for x in report['records']if x['command']==[exe,name,'prepare'])
        read_record=next(x for x in report['records']if x['command']==[exe,name,'read'])
        read_oracle=next(x for x in report['actual_control_results']if (x['case'],x['phase'])==(name,'read'))
        if prepare_record['status']!='PASS'or read_record['status']!='PASS'or \
           value.get('schema')!='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1'or value.get('case')!=name or \
           value.get('other_BQ_absent')is not True or value.get('genuine_prepare_child_closed0')is not True or \
           value.get('actual_prepare_record')!=prepare_record or evidence.get('actual_read_record')!=read_record:
            raise RuntimeError('two-phase stale baseline binds genuine completed prepare/read records')
        bundle=exact_public_pin(evidence['actual_bundle_before_pin'],cwd/'coherent_complete_context.xsm')
        selected='BQ64-SRC-ST'if name=='public_read_stale_BQ_SRC'else'BQ64-MAC-ST'
        sentinel=exact_public_live_pin(report,evidence['actual_stale_after_pin'],cwd/selected)
        if checked!=before or value['actual_bundle_pin']!=bundle or value['actual_stale_pin']!=evidence['actual_stale_before_pin']or \
           bundle!=evidence['actual_bundle_after_pin']or evidence['actual_stale_before_pin']!=sentinel or \
           any(evidence.get(k)is not True for k in ('actual_two_files_full_EOF_SHA_all7_unchanged',
              'actual_other_BQ_absent','genuine_read_child_closed0')):
            raise RuntimeError('real same-file fullEOF stale before/after facts remain unchanged')
        terminal=read_oracle['actual_terminal']
        if any(type(terminal.get(k))is not int or terminal[k]!=v for k,v in (
           ('actual_public_read_status',1),('actual_control_public_read_calls',1),('actual_baseline_public_read_calls',0))):
            raise RuntimeError('genuine public stale READ status/call-count oracle')
        other=cwd/('BQ64-MAC-ST'if name=='public_read_stale_BQ_SRC'else'BQ64-SRC-ST')
        if other.exists()or other.is_symlink():raise RuntimeError('other stale BQ stage remains absent')
        if name=='public_read_stale_BQ_MAC':
            if evidence.get('bundle_lifetime_status')!='CURRENT_RETAINED_AFTER_COMPLETED_READ'or \
               evidence.get('current_bundle_pin')!=bundle or 'actual_completed_bundle_retirement'in evidence:
                raise RuntimeError('second MAC complete fixture remains current and unretired')
            exact_public_live_pin(report,bundle,cwd/'coherent_complete_context.xsm')
            continue
        event=retirements[0]
        exact_public_nulls(evidence,('current_bundle_pin',))
        exact_public_nulls(event,('current_bundle_pin','post_receipt_failure'))
        if evidence.get('bundle_lifetime_status')!='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE'or \
           evidence.get('current_bundle_pin')is not None or evidence.get('actual_completed_bundle_retirement')!=event or \
           event.get('case')!=name or event.get('historical_bundle_before_pin')!=bundle or \
           event.get('historical_bundle_after_completed_read_pin')!=bundle or event.get('retirement_completed')is not True or \
           event.get('current_bundle_pin')is not None or event.get('post_receipt_failure')is not None or \
           event.get('secondary_operation_failures')!=[]:
            raise RuntimeError('sole SRC retirement event equals original completed READ evidence')
        for rows in (hf['dependencies'],own['dependencies'],report['fixed_current_pins'],report['output_pins'],report['owned_runtime_pins']):
            if any(x['path']==bundle['path']or x['identity'][:2]==bundle['identity'][:2]for x in rows):
                raise RuntimeError('retired exact SRC bundle has no current path or physical alias')
        if Path(bundle['path']).exists()or Path(bundle['path']).is_symlink():
            raise RuntimeError('only exact completed SRC bundle is absent')
        intent_pin=exact_public_live_pin(report,event['intent_pin'],cwd/'Host_completed_SRC_bundle_retirement_intent.json')
        receipt_pin=exact_public_live_pin(report,event['receipt_pin'],cwd/'Host_completed_SRC_bundle_retirement_receipt.json')
        intent,checked_intent=c.read_bound_json_current(intent_pin['path'],intent_pin)
        receipt,checked_receipt=c.read_bound_json_current(receipt_pin['path'],receipt_pin)
        exact_public_nulls(receipt,('current_bundle_pin','primary_operation_failure'))
        if checked_intent!=intent_pin or checked_receipt!=receipt_pin or receipt!=event['operation']or \
           intent.get('schema')!='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_INTENT_V1'or \
           receipt.get('schema')!='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_RECEIPT_V1'or \
           intent.get('case')!=name or receipt.get('case')!=name or receipt.get('actual_intent_pin')!=intent_pin:
            raise RuntimeError('actual fullEOF intent and returned receipt exactly match sole event')
        for document in (intent,receipt):
            if document.get('actual_before_manifest_pin')!=before or document.get('actual_stale_before_fullpin')!=sentinel or \
               document.get('actual_stale_after_fullpin')!=sentinel or document.get('actual_prepare_record')!=prepare_record or \
               document.get('actual_completed_read_record')!=read_record or document.get('actual_read_oracle')!=read_oracle or \
               any(document.get(k)is not True for k in ('other_BQ_absent','actual_before_equals_after_full_SHA_all7',
                  'no_retry','no_old_v5_file_targeted'))or document.get('physics_qualified')is not False or \
               type(document.get('target_uid'))is not int or document['target_uid']!=os.getuid():
                raise RuntimeError('strict intent/receipt bind original completed native records, fullpins and UID')
        if intent.get('exact_bundle_fullpin')!=bundle or intent.get('actual_bundle_after_completed_READ_fullpin')!=bundle or \
           intent.get('target_single_link_required')is not True or type(intent.get('current_owned_target_count'))is not int or \
           intent['current_owned_target_count']!=1 or intent.get('only_this_exact_bundle_may_be_unlinked')is not True or \
           receipt.get('exact_retired_bundle_fullpin')!=bundle or receipt.get('historical_completed_read_after_fullpin')!=bundle or \
           type(receipt.get('actual_retired_count'))is not int or receipt['actual_retired_count']!=1 or \
           receipt.get('current_bundle_pin')is not None or receipt.get('primary_operation_failure')is not None or \
           receipt.get('secondary_operation_failures')!=[]or \
           any(receipt.get(k)is not True for k in ('intent_parent_fsync_attempted','intent_parent_fsync_returned',
              'unlink_attempted','unlink_returned','parent_fsync_attempted','parent_fsync_returned',
              'target_absent_observed','removed_current_owned_fullpin','retirement_completed','retired_bundle_historical_only',
              'receipt_written_before_directory_close_and_any_later_check','directory_close_not_claimed_by_receipt')):
            raise RuntimeError('truthful sole completed unlink and both returned directory fsyncs, no failure/retry')
        before_intent=intent.get('parent_before_intent_identity');before_parent=receipt.get('parent_before_identity')
        after_parent=receipt.get('parent_after_identity')
        for identity in (before_intent,before_parent,after_parent):
            if not isinstance(identity,list)or len(identity)!=7 or any(type(x)is not int for x in identity)or not stat.S_ISDIR(identity[2]):
                raise RuntimeError('exact seven integer owned directory time-fact identities')
        if receipt.get('parent_before_intent_identity')!=before_intent or before_parent[:3]!=before_intent[:3]or \
           before_parent[3]!=before_intent[3]+1 or before_parent[4]!=before_intent[4]+32 or \
           before_parent[5]<before_intent[5]or before_parent[6]<before_intent[6]or \
           after_parent[:3]!=before_parent[:3]or after_parent[3]!=before_parent[3]-1 or \
           after_parent[4]!=before_parent[4]-32 or after_parent[5]<before_parent[5]or after_parent[6]<before_parent[6]:
            raise RuntimeError('exact APFS intent creation and sole unlink directory time-fact deltas')
        parent=cwd.lstat()
        if cwd.is_symlink()or not stat.S_ISDIR(parent.st_mode)or parent.st_uid!=os.getuid()or \
           [parent.st_dev,parent.st_ino,parent.st_mode]!=after_parent[:3]or \
           parent.st_nlink!=after_parent[3]+1 or parent.st_size!=after_parent[4]+32 or \
           parent.st_mtime_ns<after_parent[5]or parent.st_ctime_ns<after_parent[6]:
            raise RuntimeError('same owned SRC directory after sole retained receipt entry creation')
    return dict(sole_completed_SRC_bundle_retirement_admitted=True,retired_bundle_is_historical_only=True,
      MAC_bundle_retained_current=True,actual_completed_bundle_retirement=retirements[0],physics_qualified=False)

def admit_compact_controls(args,hf,helper,compact,old17,pold17):
    fixed=[];provenance={}
    oracle_pin=old17['actual_current_control_binding_pin']
    oracle,checked=c.read_bound_json_current(oracle_pin['path'],oracle_pin)
    if checked!=oracle_pin or oracle['source_pin']!=old17['actual_current_control_source_pin']or \
       oracle['source_pin']['sha256']!='1b782030e20d4a254052937fd37ff6ef0e145969604e6ef6d365957ea29a9af3':
        raise RuntimeError('unchanged original17 factory Source/oracle authority')
    specs=[('fresh17','fresh_seventeen','selected_actual_fresh17_report_pin',20,
      'ACTUAL_BQ64_COMPACT_EXPECTED_FRESH_CONNECTED17_COMPONENT_CONTROLS_V1',
      'ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY',
      'COMPLETE_BQ64_COMPACT_EXPECTED_CONNECTED17_HOST_SOURCE_ONLY_FREEZE_V1','selected_fresh17_Host_freeze_pin'),
     ('model','private_model','selected_actual_private_model_report_pin',3,
      'ACTUAL_BQ64_PRIVATE_GANLIB_MODEL_GUARDED_CONTROL_REPORT_V1',
      'ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY',
      'COMPLETE_BQ64_PRIVATE_GANLIB_MODEL_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1','selected_private_model_Host_freeze_pin'),
     ('public7','public_read_seven','selected_actual_public7_report_pin',11,
      'ACTUAL_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_GUARDED_CONTROL_REPORT_V1',
      'ACTUAL_SEVEN_GENUINE_PUBLIC_READ_CONTROLS_NINE_PHASES_CLOSED0_ONLY',
      'COMPLETE_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1','selected_public7_Host_freeze_pin')]
    for role,prefix,selected,count,schema,status,own_schema,own_key in specs:
        d,pd=ext(args,prefix);root=Path(pd['path']).parent
        if pd!=selected_pin(hf,selected)or d.get('schema')!=schema or d.get('status')!=status or \
           d.get('final_report_resource_check_passed')is not True or d.get('secondary_failures')!=[]:
            raise RuntimeError('genuine completed exact '+role+' control report')
        c.closed_report(d,helper,root,count)
        if any(d.get(k)is not False for k in c.scope()):raise RuntimeError('unqualified prerequisite scope must remain false')
        own,pown=admit_control_host(hf,d,role,own_schema,own_key,compact)
        if role=='fresh17':
            if d.get('actual_logical_control_count')!=17 or d.get('actual_run_phase_count')!=18 or \
               d.get('all17_original_names_exercised')is not True or d.get('old_seventeen_PASS_inherited')is not False or \
               d.get('other_eight_core_objects_and_original_oracles_unchanged')is not True or \
               any(d.get(k)is not False for k in ('new_private_model_controls_qualified','new_extra_public_READ_controls_qualified','production_reader_admitted'))or \
               d.get('original_current17_report_pin')!=pold17 or d.get('original_current17_oracle_pin')!=oracle_pin or \
               d.get('actual_current_control_source_pin')!=oracle['source_pin']or \
               own.get('selected_original17_report_pin')!=pold17 or \
               own.get('selected_actual_new_build70_report_pin')!=compact['report_pin']:
                raise RuntimeError('new actual17 scope and unchanged historical oracle Source')
            compile_cmd=list(oracle['planned_compile_command']);old_out=oracle['planned_output_root']
            include_at=next(i for i,x in enumerate(compile_cmd)if x.startswith('-I'))
            compile_cmd.insert(include_at,'-I'+str(Path(compact['object_pin']['path']).parent))
            compile_cmd=[('-J'+str(root/'build'))if x=='-J'+old_out+'/build'else x for x in compile_cmd]
            old_obj=compile_cmd[-1];new_obj=str(root/'build/test_ROOT64_full_connected17.o');compile_cmd[-1]=new_obj
            old_link=oracle['planned_link_command'];inputs=list(old_link[3:-2])
            if len(inputs)!=14 or inputs[0]!=old_obj or Path(inputs[3]).name!='SPOR64_BOOTQ64.o':
                raise RuntimeError('original current17 exact main0/BOOTQ3 link role')
            inputs[0]=new_obj;inputs[3]=compact['object_pin']['path'];exe=str(root/'build/full_connected17_unqualified')
            commands=[compile_cmd,[*old_link[:3],*inputs,'-o',exe]]+[[exe,*x[1:]]for x in oracle['planned_run_commands']]
            if [x['command']for x in d['records']]!=commands or len(commands)!=20 or \
               any(x not in compact['report']['actual_complete70_link_inputs']for x in inputs[1:])or len(d['actual_cases'])!=18:
                raise RuntimeError('genuine fresh20 commands and exact current9/fourarchives')
            for i,(record,case)in enumerate(zip(d['records'][2:],d['actual_cases'])):
                rows,lp=compact_log_rows(root,record);command=commands[i+2]
                name=command[1];phase=command[2]if len(command)==3 else'single'
                if len(rows)!=2 or rows!=[case['assertions'],case['actual_statuses_and_call_counts']]or \
                   (case['case'],case['phase'])!=(name,phase)or \
                   any((x.get('case'),x.get('phase'))!=(name,phase)for x in rows)or \
                   rows[0].get('all_actual_assertions_completed')is not True or rows[0].get('synthetic_fixture')is not True or \
                   any(rows[0].get(k)is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
                    raise RuntimeError('real fresh17 assertion/log case and unqualified scope')
                declared=next(x for x in oracle['declared_case_oracles']if x['case']==name)
                exact_counter_oracles(rows[1],declared,('expected_actual_','expected_explicit_'))
            refusal=d['actual_independent_host_coherent_refusal'];baseline=d['independent_coherent_baseline_manifest_pin']
            value,checked=c.read_bound_json_current(baseline['path'],baseline)
            if checked!=baseline or value['actual_before_pin']!=refusal['before']or \
               refusal.get('actual_refused')is not True or refusal.get('Fortran_internal_refusal_claimed')is not False or \
               refusal.get('actual_original_Host_gate')!='same_pin'or not isinstance(refusal.get('actual_refusal_error'),str)or \
               not refusal['actual_refusal_error']or refusal['before']['sha256']==refusal['after']['sha256']or \
               refusal['before']['identity']==refusal['after']['identity']:
                raise RuntimeError('real independent coherent immutable Host gate refusal')
            c.same_pin(refusal['after']['path'],refusal['after'])
        else:
            if d.get('logical_control_count')!=(1 if role=='model'else 7)or d.get('actual_run_phase_count')!=(1 if role=='model'else 9)or \
               d.get('old17_PASS_inherited')is not False or d.get('private_model_does_not_independently_qualify_public_reader')is not True or \
               any(d.get(k)is not False for k in ('new_reader_qualified','physics_qualified'))or \
               d.get('original_caps')!=compact['caps']or d.get('original_aux_cap_bytes')!=128*MI or \
               d.get('original_pending_metadata_bytes')!=8*MI or d.get('terminal_receipt_required_for_qualification')is not True:
                raise RuntimeError('separate model/public7 exact scope and original caps')
            plan_pin=own['control_host_plan_pin'];table=current_pin_table(own['dependencies'])
            if table.get(plan_pin['path'])!=plan_pin:raise RuntimeError('own frozen control plan')
            plan,checked=c.read_bound_json_current(plan_pin['path'],plan_pin)
            sfpin=d['actual_Source_freeze_pin'];sf,checked_sf=c.read_bound_json_current(sfpin['path'],sfpin)
            if checked!=plan_pin or checked_sf!=sfpin or d['actual_control_Source_pin']!=plan['control_Source_pin']or \
               sfpin!=plan['selected_control_Source_freeze_pin']or d['actual_control_Source_pin']not in sf['files']or \
               plan['selected_new_build_Host_freeze_pin']!=compact['build_Host_freeze_pin']or \
               plan['selected_new_Fortran_Source_freeze_pin']!=compact['source_freeze_pin']or \
               plan['planned_output_root']!=str(root)or plan['production_Source_pin']!=compact['source_pin']:
                raise RuntimeError('exact separate model/public control Source and frozenplan')
            if plan.get('source_only')is not True or any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported'))or \
               any(plan.get(k)is not None for k in ('future_actual_new_build70_report_pin','future_actual_control_object_pin','future_actual_control_executable_pin','future_actual_control_report_pin','future_actual_stale_manifests'))or \
               plan['kind']!=('model'if role=='model'else'public')or \
               plan['original_nine_core_pins']!=compact['report']['original_nine_core_object_pins']or \
               plan['original_nine_core_paths']!=[x['path']for x in plan['original_nine_core_pins']]or \
               plan['original_ordered70_paths']!=[x['path']for x in compact['report']['original_ordered70_input_pins']]or \
               plan['original_four_archive_paths']!=[x for x in compact['report']['actual_complete70_link_inputs']if x.endswith('.a')]or \
               plan['original_compile_flags']!=c.FLAGS or plan['original_caps']!=compact['caps']:
                raise RuntimeError('parameterized control plan exact original core/order/caps and futureNone')
            c.verify_rows(sf['files']+sf['original_source_pins']+sf.get('dependencies',[]))
            if (sfpin if role=='model'else sf['candidate_fortran_source_freeze_pin'])!=compact['source_freeze_pin']:
                raise RuntimeError('control SF selects same compact production Source')
            compiler=compact['report']['records'][0]['command'][0]
            includes=['-I'+str(root/'build'),'-I'+str(Path(compact['object_pin']['path']).parent),*plan['original_compile_include_arguments']]
            compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(root/'build'),'-c',plan['control_Source_pin']['path'],'-o',str(root/'build/control.o')]
            core=[] if role=='model'else list(plan['original_nine_core_paths'])
            if role=='public7':core[5]=compact['object_pin']['path']
            exe=str(root/'runtime/control_unqualified');link_cmd=[compiler,'-O2','-ffp-contract=off',str(root/'build/control.o'),*core,*plan['original_four_archive_paths'],'-o',exe]
            if d['records'][0]['command']!=compile_cmd or d['records'][1]['command']!=link_cmd or \
               d['actual_compile_command']!=compile_cmd or d['actual_link_command']!=link_cmd or \
               d['actual_link_core_paths']!=core or any(x not in compact['report']['actual_complete70_link_inputs']for x in core+plan['original_four_archive_paths']):
                raise RuntimeError('exact actual own control main/current production cores/archive commands')
            if role=='model':
                rows,lp=compact_log_rows(root,d['records'][2]);cases=d['actual_control_results']
                if d.get('actual_model_controls_passed')is not True or d.get('actual_seven_genuine_public_READ_controls_passed')is not False or \
                   d['records'][2]['command']!=[exe]or len(cases)!=1 or len(rows)!=1 or rows[0]!=cases[0]['actual_terminal']or \
                   rows[0].get('status')!='ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY'or type(rows[0].get('assertions'))is not int or rows[0]['assertions']!=36 or \
                   any(rows[0].get(k)is not False for k in ('physics_qualified','reader_qualified','AAA_qualified')):
                    raise RuntimeError('genuine private model assertions are not public qualification')
                models=cases[0]['actual_retained_model_file_pins'];c.verify_rows(models)
                if len(models)!=2 or [x['path']for x in models]!=[str(root/'model/C64-EXP'),str(root/'model/C64-ACT')]or \
                   models[0]['size_bytes']!=948232 or not models[0]['size_bytes']<models[1]['size_bytes']<=32*MI or \
                   models[0]['sha256']==models[1]['sha256']or any(x['identity'][3]!=1 for x in models):
                    raise RuntimeError('actual model compact948232 and complete retained independent files')
            else:
                phases=plan['planned_run_phases'];cases=d['actual_control_results'];stale=d['actual_stale_host_evidence']
                if d.get('actual_seven_genuine_public_READ_controls_passed')is not True or d.get('actual_model_controls_passed')is not False or \
                   len(phases)!=9 or len(cases)!=9 or len(stale)!=2:
                    raise RuntimeError('genuine7 public READ controls require9phases/two stale baselines')
                for declared,record,case in zip(phases,d['records'][2:],cases):
                    name,phase=declared['case'],declared['phase'];cmd=[exe,name]+([phase]if phase in ('prepare','read')else[])
                    rows,lp=compact_log_rows(root,record)
                    if record['command']!=cmd or len(rows)!=1 or rows[0]!=case['actual_terminal']or case['actual_log_pin']!=lp or \
                       rows[0].get('schema')!='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1'or \
                       (rows[0].get('case'),rows[0].get('phase'))!=(name,phase)or rows[0].get('all_actual_assertions_completed')is not True or \
                       rows[0].get('synthetic_fixture')is not True or any(rows[0].get(k)is not False for k in \
                        ('private_matcher_used_as_assertion_oracle','physics_qualified','reader_qualified','AAA_qualified','ABA_admitted')):
                        raise RuntimeError('real public READ log/oracle scope and phase')
                    exact_counter_oracles(rows[0],declared,('expected_',))
                admit_exact_public_stale_lifetimes(hf,own,plan,d,root,exe)
        fixed.extend([pd,pown,own['host_source']]+own['dependencies']+d['fixed_current_pins']+d['output_pins'])
        provenance[role]=dict(actual_report_pin=pd,actual_own_Host_freeze_pin=pown,
          exact_completed_record_count=count,old17_PASS_inherited=False,physics_qualified=False)
    return dict(fixed=unique(fixed),provenance=provenance)

def main():
    p=argparse.ArgumentParser()
    for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze','new-build70','fresh-seventeen','private-model','public-read-seven']:
        for suffix in ['summary','sha256','seven-id']:p.add_argument('--'+prefix+'-'+suffix,required=True)
    args=p.parse_args();start=time.monotonic()
    observation=ParentMemoryObservation(start);observation.checkpoint('main.started')
    hf,phf=ext(args,'host_freeze')
    if hf['schema']!='COMPLETE_ACTUAL_AAA3_COMPACT_EXPECTED_PIPELINE_HOST_SOURCE_FREEZE_V15' or \
       Path(hf['host_source']['path']).resolve()!=Path(__file__).resolve():
        raise RuntimeError('exact owning complete Host Source freeze')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    observation.checkpoint('admission.before_Common_initialize')
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    observation.checkpoint('admission.after_Common_initialize')
    if before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:
        raise RuntimeError('initial history96GiB reserves originalcold/metadata/fullfresh2GiB')
    observation.checkpoint('admission.before_build70')
    build,pbuild=ext(args,'build70')
    if pbuild!=hf['selected_actual_build70_report']:raise RuntimeError('exact external selected actual70 report pin required')
    if build['schema']!='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2' or \
       build['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       build['failure'] is not None or build['after_check_error'] is not None or \
       build['Dragon_linked'] is not True or len(build['records'])!=3 or \
       build['final_report_resource_check_passed']is not True or \
       build['old69_inputs_identical_and_retained'] is not True or \
       build['remaining68_original_inputs_identical_and_retained'] is not True or \
       build['old_nine_objects_identical_and_retained'] is not True or \
       [record['label'].rsplit('/',1)[-1]for record in build['records']]!=['compile_module','compile_driver','link_Dragon']:
        raise RuntimeError('actual cache-module/driver compile and complete70 link required')
    c.closed_report(build,helper,Path(pbuild['path']).parent,3)
    c.verify_rows(build['fixed_current_pins']);c.verify_rows(build['output_pins'])
    current69_pin=build['original_actual69_handle_lifetime_report_pin']
    current69,checked_current69_pin=c.load_json_exact(current69_pin['path'],current69_pin['sha256'],json.dumps(current69_pin['identity']))
    if checked_current69_pin!=current69_pin or \
       current69_pin!=hf['selected_original_actual69_handle_lifetime_report'] or \
       current69['schema']!='ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1' or \
       current69['status']!='ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       current69['failure'] is not None or current69['after_check_error'] is not None or \
       current69['Dragon_linked'] is not True or len(current69['records'])!=2 or \
       current69['remaining68_link_inputs_identical_and_retained'] is not True or \
       current69['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('separate actual native-handle complete69 two-stage premise required')
    c.closed_report(current69,helper,Path(current69_pin['path']).parent,2)
    c.verify_rows(current69['fixed_current_pins']);c.verify_rows(current69['output_pins'])
    original69_pin=build['original_actual69_v4_report_pin']
    original69,checked_original69_pin=c.load_json_exact(original69_pin['path'],original69_pin['sha256'],json.dumps(original69_pin['identity']))
    if checked_original69_pin!=original69_pin or \
       current69['original_actual69_v4_report_pin']!=original69_pin or \
       original69_pin!=hf['selected_original_actual69_v4_report'] or \
       original69['schema']!='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       original69['status']!='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       original69['failure'] is not None or original69['after_check_error'] is not None or \
       original69['Dragon_linked'] is not True or len(original69['records'])!=10:
        raise RuntimeError('original actual nine-alias complete69 ten-stage premise required')
    c.closed_report(original69,helper,Path(original69_pin['path']).parent,10)
    c.verify_rows(original69['fixed_current_pins']);c.verify_rows(original69['output_pins'])
    original69_link=original69['records'][-1]['command'][3:-2]
    current69_link=current69['records'][-1]['command'][3:-2]
    current70_link=build['records'][-1]['command'][3:-2]
    if len(original69_link)!=69 or len(current69_link)!=69 or \
       [i for i,(old_path,new_path)in enumerate(zip(original69_link,current69_link))if old_path!=new_path]!=[37] or \
       Path(original69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       Path(current69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o':
        raise RuntimeError('only actual native-driver object position37 changed in the separate complete69 premise')
    module_positions=[i for i,path in enumerate(current70_link)if Path(path).name=='SPOT1P64.o']
    first_archive=next(i for i,path in enumerate(current69_link)if path.endswith('.a'))
    if len(current70_link)!=70 or len(set(current70_link))!=70 or module_positions!=[first_archive] or \
       build['actual_complete70_link_inputs']!=current70_link or \
       build['replacement_zero_based_current69_input_index']!=37 or \
       build['module_insertion_current69_before_archive_index']!=first_archive or \
       [row['path']for row in build['original_current69_ordered_input_pins']]!=current69_link:
        raise RuntimeError('one genuine cache module inserted immediately before the original first archive')
    stripped70=current70_link[:first_archive]+current70_link[first_archive+1:]
    if [i for i,(old_path,new_path)in enumerate(zip(current69_link,stripped70))if old_path!=new_path]!=[37] or \
       Path(stripped70[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       [path for path in current70_link if path.endswith('.a')]!=[path for path in current69_link if path.endswith('.a')]:
        raise RuntimeError('removing the new cache helper and restoring only driver37 must recover exact original69 order')
    native_freeze_pin=hf['selected_native_exact_block_cache_source_freeze']
    native_sf,checked_native_freeze_pin=c.read_bound_json_current(native_freeze_pin['path'],native_freeze_pin)
    if checked_native_freeze_pin!=native_freeze_pin or build['actual_new_Source_freeze_pin']!=native_freeze_pin or \
       native_sf['schema']!='COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_ONLY_FREEZE_V1' or \
       native_sf['candidate_imported_or_executed']is not False or native_sf['compiled']is not False:
        raise RuntimeError('actual complete70 must bind the exact two-Fortran cache Source freeze')
    native_sf_rows=native_sf['files']+native_sf['original_source_pins']+native_sf['control_sources']+\
                   [native_sf['complete_byte_inverse_pin'],native_sf['control_plan_pin'],native_sf['logical_memory_key_contract_pin']]
    c.verify_rows(native_sf_rows)
    actual_new_sources=build['actual_new_Source_pins']
    if len(actual_new_sources)!=2 or \
       [Path(row['path']).name for row in actual_new_sources]!=['SPOT1P64.f90','SPOT_GLOBAL_NATIVE_DRIVER64.f'] or \
       any(row not in native_sf['files']for row in actual_new_sources) or \
       native_freeze_pin not in build['fixed_current_pins'] or \
       current69_pin not in build['fixed_current_pins'] or original69_pin not in build['fixed_current_pins']:
        raise RuntimeError('actual complete70 fixed pins must retain exact Sources and both genuine69 premises')
    c.verify_rows(build['original_current69_ordered_input_pins'])
    old9=binding['seventeen_required_same_production_object_pins']
    if len(old9)!=9 or any(row['path']not in current70_link for row in old9) or \
       any(row not in build['fixed_current_pins']for row in old9):
        raise RuntimeError('all original nine core objects remain exact current fixed inputs in complete70')
    cache_build=build;cache_build_pin=pbuild
    compact=admit_compact_build(args,hf,helper,cache_build,cache_build_pin,old9)
    build=compact['report'];pbuild=compact['report_pin']
    current70_link=build['actual_complete70_link_inputs']
    direct_binding_path=HERE/'DIRECT_ALIAS_ENTRY_BINDING.json'
    if not all(any(row['path']==str(HERE/name)for row in hf['dependencies'])
               for name in ['DIRECT_ALIAS_ENTRY_BINDING.json','direct_alias_entry_controls.f90']):
        raise RuntimeError('direct-entry binding and Fortran main must belong to the complete frozen Host Source')
    direct_probe_source_pin=next(row for row in hf['dependencies']
                                 if row['path']==str(HERE/'direct_alias_entry_controls.f90'))
    direct_binding_pin=next(row for row in hf['dependencies']if row['path']==str(direct_binding_path))
    direct_binding,checked_direct_binding_pin=c.read_bound_json_current(direct_binding_path,direct_binding_pin)
    if checked_direct_binding_pin!=direct_binding_pin:raise RuntimeError('exact current direct-entry binding fullpin')
    link_command=build['records'][-1]['command']
    direct_original_inputs=direct_binding['actual_original_ordered_70_link_inputs']
    removed_main=direct_binding['excluded_original_main_pin']
    if direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V2' or \
       direct_binding['selected_actual_build70_report_pin']!=pbuild or \
       direct_binding['actual_complete70_source_freeze_pin']!=compact['source_freeze_pin']or \
       direct_original_inputs!=compact['current70_pins']or \
       direct_binding['new_probe_source']!=str(HERE/'direct_alias_entry_controls.f90') or \
       direct_binding['only_main_object_replacement']is not True or \
       direct_binding['physics_qualification']is not False or \
       link_command[:3]!=[build['records'][0]['command'][0],'-O2','-ffp-contract=off'] or \
       link_command[-2:]!=['-o',next(row['path']for row in build['output_pins']if Path(row['path']).name=='Dragon')] or \
       link_command[3:-2]!=[row['path']for row in direct_original_inputs] or \
       len(direct_original_inputs)!=70 or \
       sum(Path(row['path']).suffix=='.o'for row in direct_original_inputs)!=66 or \
       sum(Path(row['path']).suffix=='.a'for row in direct_original_inputs)!=4 or \
       [row for row in direct_original_inputs if Path(row['path']).name=='DRAGON.o']!=[removed_main] or \
       direct_original_inputs[12]!=removed_main or \
       set(direct_binding['three_direct_control_modes'])!={'pack_original_alias','initial_contract_alias','view_system_alias'}:
        raise RuntimeError('exact actual ordered70 inputs with only original DRAGON main replacement required')
    c.verify_rows(direct_original_inputs)
    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    controls=admit_compact_controls(args,hf,helper,compact,seventeen,p17)
    compact_admission_provenance=dict(new_build70_report_pin=pbuild,new_BOOTQ_object_pin=compact['object_pin'],
      compact_Fortran_Source_freeze_pin=compact['source_freeze_pin'],new_build_Host_freeze_pin=compact['build_Host_freeze_pin'],
      actual_new_control_prerequisites=controls['provenance'],old17_is_historical_source_oracle_only=True,
      production_core_replacement_one_based_slot=6,complete70_replacement_zero_based_index=40,
      new_reader_prerequisites_genuinely_closed=True,physics_qualified=False)
    sf,psf=ext(args,'source_freeze')
    if psf!=hf['selected_fortran_freeze']:raise RuntimeError('exact external selected frozen Fortran Source required')
    if sf['schema']!='COMPLETE_NEW_FORTRAN_STORAGE_SOURCE_FROZEN_V1':raise RuntimeError('complete Fortran Source freeze')
    c.verify_rows(sf['files']);c.same_pin(sf['formal_and_actual_input_plan']['path'],sf['formal_and_actual_input_plan'])
    formal_plan_pin=next(row for row in hf['dependencies']if row['path']==str(data.PLAN))
    c.same_pin(data.PLAN,formal_plan_pin)
    plan,producer_fixed,producer_reports=data.validate_actual_producers(c,args)
    for row in producer_reports:c.closed_report(row,helper,Path(row['actual_output_pin']['path']).parent.parent,4)
    fixed=unique(fixed+compact['fixed']+controls['fixed']+[cache_build_pin]+cache_build['fixed_current_pins']+cache_build['output_pins']+
                 [phf,hf['host_source'],pbuild,p17,psf]+hf['dependencies']+sf['files']+
                 [sf['formal_and_actual_input_plan']]+producer_fixed+build['fixed_current_pins']+build['output_pins']+direct_original_inputs+
                 seventeen['fixed_current_pins']+seventeen['output_pins']+native_sf_rows+
                 [current69_pin,original69_pin]+current69['fixed_current_pins']+current69['output_pins']+
                 original69['fixed_current_pins']+original69['output_pins'])
    observation.checkpoint('admission.before_fixed_EOF')
    c.verify_rows(fixed)
    observation.checkpoint('admission.after_fixed_EOF')
    # Admission and full EOF checks are complete. Keep their immutable full pins,
    # the original ordered link command and the plan; close only unused JSONs.
    exe=dict(next(x for x in build['output_pins']if Path(x['path']).name=='Dragon'))
    compiler=build['records'][0]['command'][0]
    includes=tuple(x for x in build['records'][0]['command']if x.startswith('-I'))
    archives=tuple(x for x in build['records'][-1]['command']if x.endswith('.a'))
    bounded_sha256=binding['original_bounded']['sha256']
    del compact,controls,cache_build
    del build,current69,original69,seventeen,producer_reports,row,producer_fixed,sf,binding,native_sf
    del native_sf_rows,actual_new_sources,old9,original69_link,current69_link,current70_link,stripped70,module_positions
    gc.collect()
    observation.checkpoint('admission.after_original_GC')
    resources=PhaseResources(base_resources)
    resources.observation=observation;observation.phase=lambda:resources.phase
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir();WORK.mkdir();(OUT/'AAA3-streaming').mkdir()
    shutil.copy2(exe['path'],OUT/'runtime/Dragon');shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned=[c.pin(OUT/'runtime/Dragon'),c.pin(OUT/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=exe['sha256'] or owned[1]['sha256']!=bounded_sha256:
        raise RuntimeError('exact actual70 runtime and original bounded guard')
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA3-streaming',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise RuntimeError('genuine original supervisor')
    observation.stage=lambda:len(runner.records)-1
    observation.checkpoint('runtime.existing_runner_constructed')
    ledger=[];proofs=[];cases=[];failure=None;after_error=None;result=None;first=FirstFatal()
    new_storage_cases=[];lifecycle_cases=[];scratch_ledger=[];direct_alias_cases=[]
    direct_alias_build=None
    def stable():
        observation.checkpoint('stable.before',resources.phase)
        try:
            c.check_full_current(fixed,owned)
            observation.checkpoint('stable.after_full_current',resources.phase)
            resources.check()
            if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 elapsed cap')
        finally:observation.checkpoint('stable.after',resources.phase)
        observation.require_healthy()
    def retain(path):
        row=c.pin(path)
        if row['identity'][3]!=1 or any(tuple(row['identity'][:2])==tuple(x['identity'][:2])for x in fixed):
            raise RuntimeError('owned regular single-link distinct physical file required')
        if any(x['path']==row['path']for x in owned):raise RuntimeError('owned current file cannot be silently rebound')
        owned.append(row);return row
    def copy(row,name):
        target=WORK/name
        if target.exists()or target.is_symlink():raise RuntimeError('fresh owned alias only')
        c.same_pin(row['path'],row);shutil.copy2(row['path'],target);actual=retain(target)
        if actual['sha256']!=row['sha256']or actual['size_bytes']!=row['size_bytes']or actual['identity'][:2]==row['identity'][:2]:
            raise RuntimeError('complete exact copy with independent7ID')
        stable();return actual
    def release(name,why,evidence):
        target=WORK/name
        if target.parent!=WORK or target.name!=name or name not in [
          'native_A1.xsm','native_A2.xsm','native_A3.xsm','initial_pack.xsm','global.xsm',
          'negative_pack.xsm','negative_project.xsm','negative_system.xsm','negative_output.xsm',
          'negative_packout.xsm','negative_rcon1.xsm','negative_rcon2.xsm','negative_rcon3.xsm',
          'negative_ax.xsm','negative_archive.xsm','BOOT-SOLVED-STAGE.xsm']:
            raise RuntimeError('exact owned finite temporary release whitelist')
        row=c.pin(target)
        if row['identity'][3]!=1 or any(row['identity'][:2]==x['identity'][:2]for x in fixed):
            raise RuntimeError('release only independent regular single-link owned temporary')
        old=next((x for x in owned if x['path']==str(target)),None)
        if old is not None and row!=old:raise RuntimeError('owned readonly temporary changed before release')
        stable();target.unlink();owned[:]=[x for x in owned if x['path']!=str(target)]
        ledger.append(dict(released_full_pin=row,reason=why,complete_evidence=evidence,
                           exact_intermediate_XSM_raw_replay_retained=False,original_producer_files_retained=True))
        receipt=OUT/('Root_actual_private_release_'+str(len(ledger)).zfill(3)+'.json')
        c.write(receipt,ledger[-1]);retain(receipt);stable()
    def clean_driver_scratch_before():
        for name in ('_main001','_DUMMY'):
            target=WORK/name
            if target.exists()or target.is_symlink():
                raise RuntimeError('fresh actual CLE scratch paths required before each Dragon; no overwrite or retry')
    def stash_closed_driver_scratch(label):
        # Ganlib creates these only after the verified pre-launch absence. An
        # XABORT exit1 bypasses normal CLE teardown. Preserve exact raw bytes;
        # no deletion, no shared/producer object, no altered refusal oracle.
        if not label.replace('_','').isalnum():raise RuntimeError('finite literal driver label')
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());logpin=c.pin(lp);watchpin=c.pin(wp)
        if record['label']!='AAA/'+label or record['status']not in ('PASS','FAILED')or \
           w['command']!=record['command']or w['command']!=[str(OUT/'runtime/Dragon')]or \
           type(w.get('pid'))is not int or w['pid']<=0 or type(w['returncode'])is not int or \
           w['limit_failure']is not None or w['rss_cap_mib']!=512 or w['own_child_only']is not True or \
           w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or \
           not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('only genuine completed guarded Dragon permits scratch archival')
        if (record['status']=='PASS')!=(w['returncode']==0):raise RuntimeError('actual child closure status differs')
        receipt=dict(actual_stage_index=len(runner.records)-1,actual_stage_label=record['label'],
          actual_pid=w['pid'],actual_returncode=w['returncode'],actual_log_full_pin=logpin,
          actual_watchdog_full_pin=watchpin,exact_preserved_scratch_files=[],
          scratch_protocol_sources=hf['scratch_protocol_sources'],no_qualification_from_archival=True)
        folder=OUT/'cle_scratch_archive'/(str(len(runner.records)).zfill(3)+'_'+label)
        for name in ('_main001','_DUMMY'):
            source=WORK/name
            if not source.exists()and not source.is_symlink():continue
            before_pin=c.pin(source)
            if source.parent!=WORK or source.is_symlink()or before_pin['identity'][3]!=1 or \
               any(before_pin['identity'][:2]==row['identity'][:2]for row in fixed+owned):
                raise RuntimeError('scratch must be distinct exclusively owned regular single-link file')
            stable();folder.mkdir(parents=True,exist_ok=True)
            if folder.is_symlink()or folder.parent.is_symlink():raise RuntimeError('own scratch archive directories only')
            target=folder/name
            if target.exists()or target.is_symlink():raise RuntimeError('fresh archival target; no overwrite')
            c.same_pin(source,before_pin);source.rename(target);after_pin=retain(target)
            if after_pin['sha256']!=before_pin['sha256']or after_pin['size_bytes']!=before_pin['size_bytes']or \
               after_pin['identity'][:6]!=before_pin['identity'][:6]or source.exists()or source.is_symlink():
                raise RuntimeError('same physical scratch inode and complete raw bytes required after rename')
            receipt['exact_preserved_scratch_files'].append(dict(before_full_pin=before_pin,after_full_pin=after_pin,
              ctime_may_change_during_rename=True,exact_physical_raw_replay_retained=True))
            stable()
        clean_driver_scratch_before();scratch_ledger.append(receipt)
        rp=OUT/('Root_actual_closed_CLE_scratch_stash_'+str(len(runner.records)).zfill(3)+'.json')
        c.write(rp,receipt);retain(rp);stable()
    def run(label,deck,marker=None):
        f=WORK/(label+'.x2m');f.write_text(deck);retain(f);stable();clean_driver_scratch_before()
        observation.checkpoint('runner.before',resources.phase)
        try:
            runner.execute(WORK,label,[str(OUT/'runtime/Dragon')],600,marker=marker,deck=f.name)
        finally:observation.checkpoint('runner.after',resources.phase)
        stash_closed_driver_scratch(label)
        helper.check_watch(OUT,runner.records[-1]);stable()
    def refuse(label,deck,message):
        f=WORK/(label+'.x2m');f.write_text(deck);retain(f);stable();clean_driver_scratch_before();error=None;error_tb=None
        observation.checkpoint('runner.before',resources.phase)
        try:
            runner.execute(WORK,label,[str(OUT/'runtime/Dragon')],600,deck=f.name)
        except RuntimeError as exc:error=exc;error_tb=exc.__traceback__
        finally:observation.checkpoint('runner.after',resources.phase)
        if error is not None and str(error)!='own-child stage failed; no retry':raise error.with_traceback(error_tb)
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());text=lp.read_text()
        if str(error)!='own-child stage failed; no retry'or record['status']!='FAILED'or type(w['returncode'])is not int or w['returncode']!=1 or w['limit_failure']is not None:
            raise RuntimeError('only exact intended operator refusal can close this control')
        forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
          'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
          'SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
        if w['command']!=record['command'] or w['wall_cap_seconds']>record['wall_cap_seconds'] or \
           any(mark in text for mark in forbidden):raise RuntimeError('actual refusal command/cap or pre-kernel trace differs')
        if text.count(message)!=1 or w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('exact refusal reason and original child limits')
        stash_closed_driver_scratch(label)
        cases.append(dict(case=label,expected_abort=message,actual_exit_code=w['returncode'],actual_abort_message_exact=True,pre_transport_abort_at_frozen_validation_branch=True,
                          no_positive_solver_or_seal_trace=True,
                          actual_log_pin=c.pin(lp),actual_watchdog_pin=c.pin(wp),original_execution_record_index=len(runner.records)-1,
                          original_execution_record_label=record['label'],all_actual_assertions_completed=True))
        stable()
    def direct_refuse(label,message):
        # This actual child has its own main, so it never invokes CLE or creates
        # CLE scratch. Three target validation guards precede REDGET/material use.
        if direct_alias_build is None or label not in direct_binding['three_direct_control_modes']:
            raise RuntimeError('actual closed direct-entry executable and declared mode required')
        declared=direct_binding['three_direct_control_modes'][label]
        if declared['expected_abort']!=message or declared['material_payload_inspected']is not False or \
           declared['transport_executed']is not False:
            raise RuntimeError('exact structural entry scope and unmodified target refusal required')
        clean_driver_scratch_before();input_pins=[]
        for name in declared['actual_readonly_input_filenames']:
            path=WORK/name
            row=next((row for row in owned if row['path']==str(path)),None)
            if row is None:raise RuntimeError('direct control uses only current full pinned owned readonly inputs')
            c.same_pin(path,row);input_pins.append(row)
        if len({tuple(row['identity'][:2])for row in input_pins})!=len(input_pins):
            raise RuntimeError('actual input files remain physically distinct; only supplied c_ptr is deliberately repeated')
        for name in declared['fresh_private_output_filenames']:
            path=WORK/name
            if path.exists()or path.is_symlink():raise RuntimeError('fresh finite private direct-control outputs only')
        command=[str(OUT/'runtime/direct_alias_entry_controls'),label]
        stable();error=None;error_tb=None
        observation.checkpoint('runner.before',resources.phase)
        try:
            runner.execute(WORK,label,command,600)
        except RuntimeError as exc:error=exc;error_tb=exc.__traceback__
        finally:observation.checkpoint('runner.after',resources.phase)
        if error is not None and str(error)!='own-child stage failed; no retry':raise error.with_traceback(error_tb)
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());text=lp.read_text()
        clean_driver_scratch_before()
        forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
          'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
          'SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL',
          'kernel error','INCONSISTENT CALL','TARGET GUARD RETURNED']
        if str(error)!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           type(w.get('pid'))is not int or w['pid']<=0 or type(w['returncode'])is not int or w['returncode']!=1 or \
           w['limit_failure']is not None or w['command']!=command or record['command']!=command or \
           text.count('ACTUAL-AAA3-DIRECT-ALIAS-CONTROL: '+label)!=1 or text.count(message)!=1 or \
           any(mark in text for mark in forbidden)or \
           w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or \
           not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('only exact actual component direct-entry exit1 guard closes this structural control')
        for row in input_pins:c.same_pin(row['path'],row)
        case=dict(case=label,expected_abort=message,actual_exit_code=w['returncode'],actual_abort_message_exact=True,
          entry_invocation='ACTUAL_COMPONENT_DIRECT_CALL_WITH_DISTINCT_NAMES_AND_DUPLICATE_C_PTR',
          actual_component=declared['component'],actual_closed_build_evidence=direct_alias_build,
          declared_operand_construction=declared,actual_readonly_input_full_pins=input_pins,
          component_structural_guard_only=True,CLE_dispatch_executed=False,transport_executed=False,
          pre_transport_abort_at_frozen_validation_branch=True,no_positive_solver_or_seal_trace=True,
          actual_log_pin=c.pin(lp),actual_watchdog_pin=c.pin(wp),
          original_execution_record_index=len(runner.records)-1,original_execution_record_label=record['label'],
          all_actual_assertions_completed=True)
        cases.append(case);direct_alias_cases.append(label);stable()
    def cleanup(names,why,evidence):
        for name in names:
            if(WORK/name).exists():release(name,why,evidence)
    def storage_refuse(label,deck,message):
        refuse(label,deck,message);new_storage_cases.append(label)
    def writable_control(name):
        target=WORK/name;row=c.pin(target)
        if target.parent!=WORK or target.is_symlink()or row['identity'][3]!=1 or \
           any(row['identity'][:2]==x['identity'][:2]for x in fixed+owned if x['path']!=str(target)):
            raise RuntimeError('exclusive same-inode regular single-link private writable clone')
        owned[:]=[x for x in owned if x['path']!=str(target)];return row
    try:
        # Replace ONLY the main object in the original actual ordered70 link.
        # Every component/core/alias object and all four archives remain exact.
        resources.phase='direct_alias_probe_build'
        probe_obj=OUT/'build/direct_alias_entry_controls.o'
        probe_exe=OUT/'runtime/direct_alias_entry_controls'
        probe_compile=[compiler,*c.FLAGS,*includes,'-J'+str(OUT/'build'),'-c',
                       str(HERE/'direct_alias_entry_controls.f90'),'-o',str(probe_obj)]
        probe_inputs=[str(probe_obj)if row['path']==removed_main['path']else row['path']for row in direct_original_inputs]
        probe_link=[*link_command[:3],*probe_inputs,'-o',str(probe_exe)]
        if len(probe_inputs)!=70 or probe_inputs.count(str(probe_obj))!=1 or \
           any(actual!=original['path']for actual,original in zip(probe_inputs,direct_original_inputs)
               if original['path']!=removed_main['path']):
            raise RuntimeError('exact one-main-only ordered link replacement')
        direct_indices=[]
        for label,command in [('direct_alias_compile',probe_compile),('direct_alias_link',probe_link)]:
            stable();observation.checkpoint('runner.before',resources.phase)
            try:runner.execute(OUT/'build',label,command,600)
            finally:observation.checkpoint('runner.after',resources.phase)
            helper.check_watch(OUT,runner.records[-1]);direct_indices.append(len(runner.records)-1);stable()
        probe_obj_pin=retain(probe_obj);probe_exe_pin=retain(probe_exe)
        direct_alias_build=dict(actual_compile_link_record_indices=direct_indices,
          actual_new_main_frozen_source_pin=direct_probe_source_pin,
          actual_compile_command=probe_compile,actual_link_command=probe_link,
          original_ordered_70_inputs=direct_original_inputs,removed_original_main_pin=removed_main,
          actual_new_main_full_pin=probe_obj_pin,actual_new_executable_full_pin=probe_exe_pin,
          retained_original_component_and_archive_count=69,only_main_replaced=True,physics_qualification=False)
        # These copies are only access aliases. Reports and original producer pins
        # remain independent fixed inputs throughout every stage and publication.
        for i,row in enumerate(plan['producers'],1):
            copy(row['archive'],'native_A'+str(i)+'.xsm');copy(row['radial_binary_track'],'radial'+str(i)+'.bin')
        formal={Path(x['path']).name:x for x in plan['formal_inputs']}
        for original,name in [('initial_axial_track.xsm','axial_track.xsm'),('initial_axial_macrolib.xsm','axial_macro.xsm'),
                              ('basis_reference.xsm','basis.xsm'),('route_contract.xsm','global_rcon.xsm')]:copy(formal[original],name)
        packdeck=''.join('XSM_FILE '+n+' :: FILE \'./'+f+'\' ;\n'for n,f in [
          ('PACK','initial_pack.xsm'),('RCON1','plane1_rcon.xsm'),('RCON2','plane2_rcon.xsm'),('RCON3','plane3_rcon.xsm'),
          ('A1','native_A1.xsm'),('A2','native_A2.xsm'),('A3','native_A3.xsm')])
        packdeck+='MODULE APACKX64: END: ;\nPACK RCON1 RCON2 RCON3 := APACKX64: A1 A2 A3 :: ;\n'
        resources.phase='pack_controls'
        negpack=packdeck.replace('initial_pack.xsm','negative_packout.xsm').replace('plane1_rcon.xsm','negative_rcon1.xsm').replace('plane2_rcon.xsm','negative_rcon2.xsm').replace('plane3_rcon.xsm','negative_rcon3.xsm')
        for label,deck,message in [
          ('pack_missing_original',negpack.replace('A1 A2 A3 :: ;','A1 A2 :: ;'),'APACKX64: FOUR OUTPUTS AND THREE INDEPENDENT INPUTS REQUIRED.'),
          ('pack_memory_outputs',negpack.replace("XSM_FILE PACK :: FILE './negative_packout.xsm' ;",'LINKED_LIST PACK ;'),'APACKX64: STRICT FRESH XSM / READONLY XSM ORDER REQUIRED.'),
          ('pack_original_alias',None,'APACKX64: INDEPENDENT DISTINCT OPERANDS REQUIRED.'),
          ('pack_wrong_order',negpack.replace('A1 A2 A3 :: ;','A2 A1 A3 :: ;'),'APACKX64: OWN PLANE CASE REQUIRED.'),
          ('pack_no_fake_options',negpack.replace('A1 A2 A3 :: ;','A1 A2 A3 :: SYNTHETIC ;'),'APACKX64: NO SYNTHETIC PRODUCER OPTIONS ALLOWED.')]:
            if label=='pack_original_alias':
                direct_refuse(label,message);new_storage_cases.append(label)
            else:storage_refuse(label,deck+'END: ; QUIT "LIST" .\n',message)
            cleanup(['negative_packout.xsm','negative_rcon1.xsm','negative_rcon2.xsm','negative_rcon3.xsm'],
                    'unqualified pre-kernel APACK private outputs',cases[-1])
        resources.phase='pack';run('pack',packdeck+'ECHO "ACTUAL-AAA3-INDEPENDENT-PACK-COMPLETE" ;\nEND: ; QUIT "LIST" .\n','ACTUAL-AAA3-INDEPENDENT-PACK-COMPLETE')
        for n in ['initial_pack.xsm','plane1_rcon.xsm','plane2_rcon.xsm','plane3_rcon.xsm']:retain(WORK/n)
        packed=data.packed_readback(WORK/'initial_pack.xsm',plan);proofs.append(dict(stage='pack',actual_full_items=packed))
        c.write(OUT/'Root_actual_independent_three_plane_pack_readback.json',proofs[-1])
        for i in range(1,4):release('native_A'+str(i)+'.xsm','independent producer originals and complete18 packed trees retained',proofs[-1])
        # Compile only the bounded negative-input mutator; no Native/solver here.
        obj=OUT/'build/mutate_owned_control.o';mut=OUT/'runtime/mutate_owned_control'
        compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(OUT/'build'),'-c',str(HERE/'mutate_owned_control.f90'),'-o',str(obj)]
        for i,command in enumerate([compile_cmd,[compiler,'-O2','-ffp-contract=off',str(obj),*archives,'-o',str(mut)]]):
            stable();runner.execute(OUT/'build','mutator_'+str(i),command,600);helper.check_watch(OUT,runner.records[-1]);stable()
        retain(mut);retain(obj)
        resources.phase='initial_operator_controls'
        operands='MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2 RCON3'
        def initial(params='RANK 1 EDIT 0',ops=operands,pack='initial_pack.xsm',out='negative_system.xsm'):
            return PREFIX.replace('./initial_pack.xsm','./'+pack)+'XSM_FILE SYSOUT :: FILE \'./'+out+'\' ;\nMODULE SPOOPP64: END: ;\nSYSOUT := SPOOPP64: '+ops+' :: '+params+' ;\nEND: ; QUIT "LIST" .\n'
        for label,params,ops,message in [
          ('initial_missing_rank','EDIT 0',operands,'SPOOPP64: RANK MUST BE EXPLICIT, NO DEFAULT.'),
          ('initial_duplicate_rank','RANK 1 RANK 1',operands,'SPOOPP64: DUPLICATE RANK.'),
          ('initial_wrong_rank_type','RANK 1.0',operands,'SPOOPP64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('initial_zero_rank','RANK 0',operands,'SPOOPP64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('initial_missing_plane_contract','RANK 1','MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2','SPOOPP64: NINE FULL OPERANDS REQUIRED.'),
          ('initial_contract_alias',None,None,'SPOOPP64: CONTRACT OPERAND ALIAS.'),
          ('initial_wrong_plane_order','RANK 1','MACRO AXTRACK PACK BASIS GRCON RCON2 RCON1 RCON3','SPOASMP64: GENUINE COMPLETE NATIVE INPUT REQUIRED.')]:
            if label=='initial_contract_alias':direct_refuse(label,message)
            else:refuse(label,initial(params,ops),message)
            if(WORK/'negative_system.xsm').exists():release('negative_system.xsm','unqualified initial operator negative output',cases[-1])
        for mutation in ['missing_seal','wrong_case','wrong_plane','wrong_epoch','flux32','source32','LPOD_only']:
            copy(c.pin(WORK/'initial_pack.xsm'),'negative_pack.xsm')
            # Only this explicitly designated clone is writable during mutator.
            control_pin=c.pin(WORK/'negative_pack.xsm')
            if Path(control_pin['path']).parent!=WORK or not stat.S_ISREG(control_pin['identity'][2])or control_pin['identity'][3]!=1 or \
               any(control_pin['identity'][:2]==x['identity'][:2]for x in fixed+owned if x['path']!=control_pin['path']):
                raise RuntimeError('exclusive regular single-link private writable control clone')
            owned[:]=[x for x in owned if x['path']!=str(WORK/'negative_pack.xsm')]
            stable();runner.execute(WORK,'mutate_'+mutation,[str(mut),'negative_pack.xsm',mutation],600)
            helper.check_watch(OUT,runner.records[-1]);mutated=retain(WORK/'negative_pack.xsm')
            if mutated['identity'][:2]!=control_pin['identity'][:2]or mutated['sha256']==control_pin['sha256']:
                raise RuntimeError('actual declared mutation must change the same independent owned clone')
            stable()
            expected_message=('SPOASM: INVALID OFFLINE REAL64 SOURCE ITEM.'if mutation=='source32'else
                              'SPOASMP64: GENUINE COMPLETE NATIVE INPUT REQUIRED.')
            refuse('initial_'+mutation,initial(pack='negative_pack.xsm'),expected_message)
            if(WORK/'negative_system.xsm').exists():release('negative_system.xsm','unqualified initial operator negative output',cases[-1])
            release('negative_pack.xsm','one finite exact private control clone; original18 trees retained',cases[-1])
        run('initial_positive',initial(out='initial_system.xsm').replace('END: ; QUIT "LIST" .','ECHO "ACTUAL-AAA3-INITIAL-OPERATOR-COMPLETE" ;\nEND: ; QUIT "LIST" .'),
            'ACTUAL-AAA3-INITIAL-OPERATOR-COMPLETE');retain(WORK/'initial_system.xsm')
        resources.phase='GLOBAL'
        globaldeck=PREFIX+'''XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE GLOBAL :: FILE './global.xsm' ;
MODULE FLUGLOBAL64: END: ;
AX GLOBAL := FLUGLOBAL64: MACRO AXTRACK AXSYSTEM PACK GRCON ::
  EDIT -3 TYPE K B1 SIGS EXTE 500 5.00000000E-08 REBA OFF
  ACCE 3 0 UNKT 5.00000000E-08 THER 740 5.00000000E-08 ;
ECHO "ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE" ;
END: ; QUIT "LIST" .
'''
        run('global_positive',globaldeck,'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE')
        retain(WORK/'ax_current.xsm');retain(WORK/'global.xsm')
        resources.phase='projection'
        projectprefix=PREFIX+'''XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE GLOBAL :: FILE './global.xsm' ;
XSM_FILE PROJECT :: FILE './projected_boot.xsm' ;
MODULE BPROJX64: END: ;
'''
        # New single-private projection checks use actual independent full inputs.
        negproject=projectprefix.replace('projected_boot.xsm','negative_output.xsm')
        for label,params,head,message in [
          ('project_missing_rank','',negproject,'BPROJX64: MANDATORY UNIQUE RANK KEYWORD REQUIRED.'),
          ('project_rank_type','RANK 1.0',negproject,'BPROJX64: INTEGER RANK REQUIRED.'),
          ('project_zero_rank','RANK 0',negproject,'BPROJX64: RANK MUST BE EXACTLY ONE OR TWO.'),
          ('project_duplicate_rank','RANK 1 RANK 1',negproject,'BPROJX64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.'),
          ('project_case_rank_mismatch','RANK 2',negproject,'BPROJX64: COMPLETE PROJECTION ADMISSION OR COMMIT FAILED.'),
          ('project_memory_output','RANK 1',negproject.replace("XSM_FILE PROJECT :: FILE './negative_output.xsm' ;",'LINKED_LIST PROJECT ;'),'BPROJX64: PRIVATE XSM OUTPUT REQUIRED.')]:
            storage_refuse(label,head+'PROJECT := BPROJX64: GLOBAL AX AXTRACK AXSYSTEM MACRO PACK GRCON :: '+params+' ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_output.xsm'],'unqualified single-private projection control output',cases[-1])
        run('project_positive',projectprefix+'PROJECT := BPROJX64: GLOBAL AX AXTRACK AXSYSTEM MACRO PACK GRCON :: RANK 1 ;\n'
            +'ECHO "ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE" ;\nEND: ; QUIT "LIST" .\n','ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE')
        retain(WORK/'projected_boot.xsm')
        roots={n:WORK/f for n,f in ROOT_NAMES.items()}
        transferred=data.transfer_readback(WORK/'projected_boot.xsm',WORK/'global.xsm',WORK/'initial_pack.xsm',roots,plan)
        transferred=dict(stage='independent_complete_transfer',actual_tree_proof=transferred,
          project_full_pin=c.pin(WORK/'projected_boot.xsm'),global_full_pin=c.pin(WORK/'global.xsm'),pack_full_pin=c.pin(WORK/'initial_pack.xsm'))
        proofs.append(transferred);c.write(OUT/'Root_actual_complete_independent_transfer_readback.json',transferred)
        # Keep all original producer and formal inputs. Retained PROJECT contains
        # every original packed record and every old GLOBAL context/tree exactly.
        release('initial_pack.xsm','complete retained PROJECT/GLOBAL64/ARCHIVE matches independent originals',transferred)
        release('global.xsm','complete retained PROJECT/GLOBAL64 matches independent GLOBAL full tree',transferred)
        resources.phase='BOOT_storage_controls'
        # CLE requires actual defined systems before dispatching any component.
        # Reuse the complete positive BOOT recovery/ASM prefix for these guards.
        precheck=BOOT_PREFIX.replace('MODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;',
          'MODULE RECOVER: ASM: DELETE: SPOBVX64: SPOBOOX64: END: ;')+'''XSM_FILE AXOUT :: FILE './negative_ax.xsm' ;
XSM_FILE ARCOUT :: FILE './negative_archive.xsm' ;
'''
        viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON\n  SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'
        for label,head,ops,message in [
          ('view_missing_operand',precheck,viewops.rsplit(' ',1)[0],'SPOBVX64: EXACT FOURTEEN ORDERED OPERANDS REQUIRED.'),
          ('view_memory_output',precheck.replace("XSM_FILE AXOUT :: FILE './negative_ax.xsm' ;",'LINKED_LIST AXOUT ;'),viewops,'SPOBVX64: FRESH PRIVATE XSM OUTPUT PAIR REQUIRED.'),
          ('view_system_alias',None,None,'SPOBVX64: OPERAND ALIAS OR REPEATED NAME.')]:
            if label=='view_system_alias':
                direct_refuse(label,message);new_storage_cases.append(label)
            else:storage_refuse(label,head+'AXOUT ARCOUT := SPOBVX64: '+ops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_ax.xsm','negative_archive.xsm'],'unqualified pre-kernel view-pair outputs',cases[-1])
        for label,params,message in [
          ('pair_missing_rank','EDIT 0','SPOBOOX64: RANK HAS NO DEFAULT.'),
          ('pair_rank_type','RANK 1.0 EDIT 0','SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('pair_case_rank_mismatch','RANK 2 EDIT 0','SPOBOOX64: CASE RANK MISMATCH.')]:
            storage_refuse(label,precheck+'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: '+params+' ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_ax.xsm','negative_archive.xsm'],'unqualified pre-kernel complete BOOT pair outputs',cases[-1])
        if len(new_storage_cases)!=17 or len(set(new_storage_cases))!=17:raise RuntimeError('complete declared new17 strict-storage controls')
        copy(c.pin(WORK/'projected_boot.xsm'),'negative_project.xsm')
        before_mut=writable_control('negative_project.xsm');stable()
        runner.execute(WORK,'mutate_retained_global_case',[str(mut),'negative_project.xsm','global_case'],600)
        helper.check_watch(OUT,runner.records[-1]);changed=retain(WORK/'negative_project.xsm')
        if changed['identity'][:2]!=before_mut['identity'][:2]or changed['sha256']==before_mut['sha256']:
            raise RuntimeError('actual retained-global mutation is same private inode and differs')
        refuse('lifecycle_mutated_retained_global',precheck.replace('projected_boot.xsm','negative_project.xsm')+
          'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',
          'SPOBOOX64: GENUINE FULL PROJECTED-BOOT/E0 CONTEXT REQUIRED.')
        lifecycle_cases.append(cases[-1]['case'])
        cleanup(['negative_ax.xsm','negative_archive.xsm','negative_project.xsm'],'unqualified mutated retained GLOBAL complete control clone',cases[-1])
        c.write(WORK/'BOOT-SOLVED-STAGE.xsm',dict(unqualified_private_lifecycle_sentinel=True));retain(WORK/'BOOT-SOLVED-STAGE.xsm')
        sentinel=c.pin(WORK/'BOOT-SOLVED-STAGE.xsm')
        refuse('lifecycle_no_private_archive_overwrite',precheck+'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',
          'SPOBOOX64: PRIVATE ARCHIVE EXISTS; NO OVERWRITE.')
        c.same_pin(sentinel['path'],sentinel);lifecycle_cases.append(cases[-1]['case'])
        cleanup(['negative_ax.xsm','negative_archive.xsm','BOOT-SOLVED-STAGE.xsm'],'unchanged private sentinel; refusal before any kernel',cases[-1])
        if len(cases)!=33:raise RuntimeError('14 genuine operator +17 new storage +2 lifecycle refusals required')
        resources.phase='BOOT'
        bootdeck=BOOT_PREFIX+'''XSM_FILE AXOUT :: FILE './closed_boot_axial.xsm' ;
XSM_FILE ARCOUT :: FILE './closed_boot_archive.xsm' ;
AXOUT ARCOUT := SPOBVX64: PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON
  SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3 :: RANK 1 EDIT 0 ;
ECHO "ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE" ;
END: ; QUIT "LIST" .
'''
        # The independent proof above plus this unchanged full file pin is the
        # owning current-context authority for nested views, never self-comparison.
        stable();run('BOOT_positive',bootdeck,'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE')
        log=(WORK/'BOOT_positive.log').read_text()
        readbacks=[json.loads(line)for line in log.splitlines()if line.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"')]
        if len(readbacks)!=1 or readbacks[0]['status']!='PASS' or readbacks[0]['all_payload_bits_equal']is not True:
            raise RuntimeError('actual whole sealed-pair payload readback before private solved stage destruction')
        axpin=retain(WORK/'closed_boot_axial.xsm');arcpin=retain(WORK/'closed_boot_archive.xsm')
        result=data.final_readback(WORK/'closed_boot_axial.xsm',WORK/'closed_boot_archive.xsm')
        result=dict(actual_terminal=result,AX_full_pin=axpin,ARCHIVE_full_pin=arcpin,actual_Fortran_complete_copy_readback=readbacks[0])
        c.write(OUT/'Root_actual_complete_BOOT_terminal_readback.json',result);stable()
        if len(direct_alias_cases)!=3 or len(set(direct_alias_cases))!=3:
            raise RuntimeError('all three actual structural component alias guards required')
        if len(runner.records)!=50 or sum(x['status']=='PASS'for x in runner.records)!=17 or \
           sum(x['status']=='FAILED'for x in runner.records)!=33:
            raise RuntimeError('all50 genuine stages:17 success plus33 exact intended exit1 refusals')
    except BaseException as exc:
        first.capture(exc,'execute_or_owned_proof');failure=type(exc).__name__+': '+str(exc)
    finally:
        try:stable();after=resources.check()
        except BaseException as exc:
            first.capture(exc,'after_resource_check');after_error=type(exc).__name__+': '+str(exc);after=None
    with first:
        # Complete unmodified original execution records are written first. Only
        # this compact final receipt may claim engineering closed0 after raw-record
        # full-EOF readback and all original limits have genuinely passed.
        raw=dict(schema='ACTUAL_AAA3_COMPLETE_EXECUTION_PREPUBLICATION_RECORD_V1',
          failure=failure,after_check_error=after_error,first_failure_secondary_errors=list(first.secondary),records=runner.records,fixed_current_pins=fixed,
          owned_runtime_pins=owned,actual_operator_refusals=cases,actual_complete_readback_proofs=proofs,
          actual_direct_structural_alias_control_names=direct_alias_cases,actual_direct_alias_build=direct_alias_build,
          actual_terminal=result,actual_private_release_ledger=ledger,actual_closed_CLE_scratch_archival_ledger=scratch_ledger,
          private_release_ledger_scope='HOST_OWNED_UNLINK_ONLY',
          frozen_Fortran_internal_disposal=dict(names=['BOOT-MAC-1/2/3.xsm','BOOT-Q-1/2/3.xsm','BOOT-SOLVED-STAGE.xsm'],
             source='aaa_three_plane_streaming_source_v2/SPOBOOX64.f90',
             complete_logical_readback_before_disposal_required_by_frozen_source=True,
             actual_complete_copy_readback_seen=result is not None,
             independent_physical_EOF_pins_available=False,exact_raw_replay_retained=False),
          actual_compact_expected_reader_admission=compact_admission_provenance,
          compact_expected_internal_disposal=dict(names=['BQ64-SRC-ST','BQ64-MAC-ST'],
            source=hf['selected_new_Fortran_Source_freeze_pin'],private_READ_only=True,
            independent_physical_EOF_pins_available=False,exact_raw_replay_retained=False,physics_qualified=False),
          engineering_three_plane_closed0=False,
          current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),
          exact_publication_pending=True,**c.scope())
        rawpath=OUT/'Root_actual_complete_execution_record_before_final_publication.json'
        c.write(rawpath,raw);rawpin=retain(rawpath)
        observation.checkpoint('publication.before_journal',resources.phase)
        try:
            observation.freeze(OUT/'Root_actual_parent_memory_checkpoint_journal.json')
            observation.journal_pin=retain(OUT/'Root_actual_parent_memory_checkpoint_journal.json')
        except BaseException as exc:
            first.capture(exc,'journal_publication')
            observation.frozen=True
            if observation.first_error is None:
                observation.first_error='parent observation publication: '+type(exc).__name__+': '+str(exc)[:256]
        resources.pending_publication_reserved_bytes=8*MI
        try:
            stable();output_pins=[]
            for f in sorted(OUT.rglob('*')):
                if f.is_symlink():raise RuntimeError('current output inventory symlink forbidden')
                if f.is_file():output_pins.append(c.pin(f))
            c.verify_rows(output_pins);stable();after=resources.check()
        except BaseException as exc:
            first.capture(exc,'publication_full_EOF')
            if not isinstance(exc,ParentObservationFailure) or after_error is None:
                after_error=type(exc).__name__+': '+str(exc)
            output_pins=[];after=None
        closed=failure is None and after_error is None and result is not None and observation.first_error is None
        compact_records=[{k:v for k,v in record.items()if k not in ('resource_before','resource_after')}
                         for record in runner.records]
        report=dict(schema='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1',
          status='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'if closed else 'FAILED_UNQUALIFIED_NO_RETRY',
          output_pins=output_pins,physical_EOF_hashes_separate_from_logical_tree_digests=True,
          complete_unmodified_execution_records_pin=rawpin,actual_closed_CLE_scratch_archival_ledger=scratch_ledger,
          failure=failure,after_check_error=after_error,first_failure_secondary_errors=list(first.secondary),records=compact_records,fixed_current_pins=fixed,
          owned_runtime_pins=owned,actual_terminal=result,
          actual_direct_structural_alias_control_names=direct_alias_cases,actual_direct_alias_build=direct_alias_build,
          actual_operator_refusals=[{k:v for k,v in case.items()if k!='record'}for case in cases],
          actual_complete_readback_proofs=proofs,
          actual_private_release_ledger=[dict(released_full_pin=x['released_full_pin'],reason=x['reason'],
             complete_evidence_in_unmodified_execution_record=True,
             exact_intermediate_XSM_raw_replay_retained=False,original_producer_files_retained=True)for x in ledger],
          historical_released_pins_are_not_current_live_pins=True,private_release_ledger_scope='HOST_OWNED_UNLINK_ONLY',
          frozen_Fortran_internal_disposal=raw['frozen_Fortran_internal_disposal'],
          compact_expected_internal_disposal=raw['compact_expected_internal_disposal'],
          actual_compact_expected_reader_admission=compact_admission_provenance,angular_moments_status='UNKNOWN',
          actual_fresh_peaks_by_phase=resources.peaks,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
          original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,wall_seconds=time.monotonic()-start,
          resources_before=before,resources_after=after,engineering_three_plane_closed0=closed,
          independent_reference_physics_assessment_executed=False,
          all_new_storage_entry_controls_closed=closed and len(new_storage_cases)==17 and len(lifecycle_cases)==2,
          actual_new_storage_control_names=new_storage_cases,actual_negative_lifecycle_control_names=lifecycle_cases,
          storage_phase_maximum_simultaneous_inventory=STORAGE_FORECAST,
          final_publication_reserved_bytes=8*MI,
          current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),**c.scope())
        observation.checkpoint('publication.before_compact_report',resources.phase)
        report['parent_memory_observation']=observation.summary()
        final_size=sum(len(chunk.encode('utf-8'))for chunk in json.JSONEncoder(indent=2,ensure_ascii=False,
                        allow_nan=False).iterencode(report))+1
        if final_size>8*MI:raise RuntimeError('compact final publication exceeds independently guarded8MiB reserve')
        if final_size+observation.journal_bytes>8*MI:raise RuntimeError('parent observation plus final summary exceed original8MiB publication')
        c.write(OUT/'Root_actual_three_plane_engineering_summary.json',report)
        resources.pending_publication_reserved_bytes=0
        try:stable();resources.check()
        except BaseException as original_late_exc:
            first.capture(original_late_exc,'late_resource_check')
            try:observation.same_fd_tail('latefailed.after_compact_report')
            except BaseException as exc:
                first.capture(exc,'late_observation_tail')
                if observation.first_error is None:observation.first_error='late observation tail: '+type(exc).__name__+': '+str(exc)[:256]
            first.reraise()
        if failure is not None or after_error is not None:
            try:observation.same_fd_tail('original.failed.after_publication_checks')
            except BaseException as exc:
                first.capture(exc,'late_observation_tail')
                if observation.first_error is None:observation.first_error='late observation tail: '+type(exc).__name__+': '+str(exc)[:256]
            first.reraise()
        try:observation.same_fd_tail('final.after_original_publication_checks')
        except BaseException as exc:
            first.capture(exc,'late_observation_tail')
            if observation.first_error is None:observation.first_error='late observation tail: '+type(exc).__name__+': '+str(exc)[:256]
        first.reraise()
        observation.require_healthy()
        if not closed:
            first.reraise()
            raise RuntimeError('no actual terminal')

if __name__=='__main__':main()

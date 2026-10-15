#!/usr/bin/env python3
"""Guarded compile68/link70/one BOOT diagnostic. No GLOBAL/PROJECT/full50 rerun."""
import argparse,hashlib,importlib.util,json,os,shutil,stat,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).absolute().parent
PLAN=HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json'
OUT=R/'validation/artifacts/axial-material-new-one-BOOT-exact-status-diagnostic-20261014-v3'
WORK=OUT/'AAA'
COMMON=REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py'
COMMON_SHA='a5b774a6b62e229f8f6360a284354e2f0af8ff3860602b061de376b2624fc040'
MI=2**20
HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_EXACT_STATUS_DIAGNOSTIC_HOST_SOURCE_ONLY_FREEZE_V1'
SF_SCHEMA='COMPLETE_BOOT_EXACT_RETURN_STATUS_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'

BOOT_EMPTY_XSM_PREFIX=bytes.fromhex('2458534dbf00000003000000242424241e0000000000000003000000ffffffff2f2020202020202020202020')
BOOT_EMPTY_XSM_IMAGE=BOOT_EMPTY_XSM_PREFIX+bytes(720)
def load_common():
    def identity(s):
        return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    before = identity(COMMON.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('regular exact Common Source required')
    fd = os.open(COMMON,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != before:
            raise RuntimeError('Common opened7ID changed')
        with os.fdopen(fd,'rb') as stream:
            fd = None
            sha = hashlib.file_digest(stream,'sha256').hexdigest()
            if identity(os.fstat(stream.fileno())) != before:
                raise RuntimeError('Common EOF7ID changed')
    finally:
        if fd is not None:
            os.close(fd)
    if identity(COMMON.lstat()) != before or sha != COMMON_SHA:
        raise RuntimeError('Common fullEOF/after7ID/SHA differs')
    spec = importlib.util.spec_from_file_location('compact_bq_build_original_common',COMMON)
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    return c

def unique(rows):
    table = {}
    for row in rows:
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('inconsistent complete input pins')
        table[row['path']] = row
    return list(table.values())

def rewrite_summary(c,path,previous,data):
    if previous['identity'][3] != 1 or previous['path'] != str(path):
        raise RuntimeError('only owning single-link summary can be rewritten')
    c.same_pin(path,previous)
    fd = os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] != previous['identity']:
            raise RuntimeError('owned summary opened7ID changed')
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            fd = None
            stream.seek(0)
            stream.truncate(0)
            json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if fd is not None:
            os.close(fd)
    if c.identity(path)[:4] != previous['identity'][:4]:
        raise RuntimeError('own summary physical role changed')

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







def genuine_terminal(d,required):
    keys=[k for k in ('actual_terminal_return','actual_execute_return','actual_release_return')if k in d]
    if not keys or any(d[k]!=d[keys[0]]for k in keys):raise RuntimeError('one genuine terminal object, all named copies agree')
    a=d[keys[0]]
    if type(a['exit_code'])is not int or a['exit_code']!=required or a.get('session_id')is not None or d['observed_closed']is not True:raise RuntimeError('genuine closed integer Root terminal')
    return a

def make_commands(c,base,plan,source):
    old=list(base['actual_complete70_link_inputs']);last=base['records'][1]['command'];first=base['records'][0]['command']
    if len(old)!=70 or len(set(old))!=70 or last!=[first[0],'-O2','-ffp-contract=off',*old,'-o',plan['base_Dragon_pin']['path']]or \
       old!=[p['path']for p in plan['current_ordered70_input_pins']]or old[37]!=plan['retained_Driver37_pin']['path']or \
       old[40]!=plan['retained_BOOTQ40_pin']['path']or old[57]!=plan['retained_math57_pin']['path']or \
       Path(old[68]).name!='SPOBOOX64.o'or [p for p in old if p.endswith('.a')]!=[p['path']for p in plan['original_four_archive_pins']]:raise RuntimeError('exact current Driver2 ordered70/37/40/57/four archives')
    if c.FLAGS!=plan['original_compile_flags']or first[0]!=plan['original_compiler_pin']['path']or \
       [v for v in first if v.startswith('-I')]!=plan['original_compile_include_arguments']:raise RuntimeError('original exact compiler/flags/include order')
    obj=str(OUT/'build/SPOBOOX64.o');new=list(old);new[68]=obj
    if [i for i,(x,y)in enumerate(zip(old,new))if x!=y]!=[68]:raise RuntimeError('only object68 may be replaced')
    compile_cmd=[first[0],*c.FLAGS,'-I'+str(OUT/'build'),*plan['original_compile_include_arguments'],'-J'+str(OUT/'build'),'-c',source['path'],'-o',obj]
    link_cmd=[*last[:3],*new,'-o',str(OUT/'runtime/Dragon')]
    return [compile_cmd,link_cmd,[str(OUT/'runtime/Dragon')]],new

def read_BOOT_outcome(c,runner,expected_error,expected_tb):
    record=runner.records[-1];wp=c.pin(WORK/'BOOT_diagnostic.watchdog.json');lp=c.pin(WORK/'BOOT_diagnostic.log')
    w=json.loads(Path(wp['path']).read_text());text=Path(lp['path']).read_text();rows=[]
    for line in text.splitlines():
        if len(line)>65536:raise RuntimeError('bounded actual diagnostic JSON/log line')
        if line.strip().startswith('{')and line.strip().endswith('}'):
            row=json.loads(line)
            if isinstance(row,dict):rows.append(row)
    if w['command']!=record['command']or w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
       w['limit_failure']is not None or not 0<=w['sampled_peak_rss_mib']<512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or type(w['returncode'])is not int:raise RuntimeError('true own-child closed BOOT watch with unchanged caps')
    diagnostics=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_EXACT_FAILURE_STATUS_DIAGNOSTIC_V1']
    seals=[r for r in rows if r.get('schema')=='ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1']
    if w['returncode']==1:
        if expected_error is None or str(expected_error)!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           text.count('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')!=1 or len(diagnostics)!=1 or seals or 'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE'in text:raise RuntimeError('only exact original strict BOOT abort1 is diagnostic, never PASS')
        row=diagnostics[0]
        if type(row.get('boot_plane'))is not int or row['boot_plane']not in(1,2,3)or type(row.get('actual_return_status'))is not int or row['actual_return_status']not in range(1,8)or row.get('required_committed_status')!=8:raise RuntimeError('exact true failure plane/status1..7')
        return dict(kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY',actual_exit_code=1,actual_failed_record_preserved=True,actual_diagnostic=row,actual_log_pin=lp,actual_watchdog_pin=wp,original_expected_child_error_repr=repr(expected_error),original_expected_child_traceback_preserved=True,engineering_qualified=False),None
    if w['returncode']!=0 or expected_error is not None or record['status']!='PASS'or diagnostics or len(seals)!=1 or \
       seals[0].get('status')!='PASS'or seals[0].get('all_payload_bits_equal')is not True or seals[0].get('complete_lifecycle_checked')is not True or \
       (seals[0].get('groups'),seals[0].get('planes'),seals[0].get('epoch'))!=(370,3,0)or 'normal end of execution'not in text or 'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE'not in text:
        if expected_error is not None:raise expected_error.with_traceback(expected_tb)
        raise RuntimeError('actual status8 path requires original genuine full seal/readback, no promotion from missing diagnostic')
    return dict(kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0,actual_Fortran_complete_copy_readback=seals[0],actual_log_pin=lp,actual_watchdog_pin=wp,engineering_qualified=False),seals[0]

def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for prefix in ('driver-build','v16-failure','diag-source-freeze','host-freeze','literal3-release','literal3-Root-tools'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    a=p.parse_args();start=time.monotonic();c=load_common()
    def load(prefix):
        name=prefix.replace('-','_');return c.load_json_exact(getattr(a,name+'_summary'),getattr(a,name+'_sha256'),getattr(a,name+'_seven_id'))
    hf,phf=load('host-freeze');deps=unique(hf['dependencies']);dt={r['path']:r for r in deps}
    if hf['schema']!=HF_SCHEMA or hf['compiler_executed']is not False or hf['numerical_executed']is not False or hf['host_source']['path']!=str(Path(__file__).absolute()):raise RuntimeError('exact own Source-only diagnostic HF')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(deps)
    pp=hf['diagnostic_host_plan_pin'];plan=c.load_json_exact(pp['path'],pp['sha256'],json.dumps(pp['identity']))[0]
    if pp['path']!=str(PLAN)or dt.get(str(PLAN))!=pp or plan['source_only']is not True or plan['planned_output_root']!=str(OUT)or \
       any(plan[k]is not None for k in ('future_actual_object_pin','future_actual_Dragon_pin','future_actual_BOOT_report_pin')):raise RuntimeError('Source plan has no fake actuals or substituted output/input alias namespace')
    selected=('selected_Driver2_Host_freeze_pin','selected_diag_Fortran_Source_freeze_pin','selected_closed_v16_Host_freeze_pin','selected_closed_v16_Root_tool_pin','selected_closed_v16_actual_post_review_pin','selected_closed_v16_actual_post_tools_pin','selected_literal3_actual_release_pin','selected_literal3_actual_Root_tool_pin','selected_literal3_actual_post_review_pin','selected_literal3_actual_post_tools_pin')
    for k in selected:
        if not isinstance(hf[k],dict)or dt.get(hf[k]['path'])!=hf[k]:raise RuntimeError('all selected actual authorities in ownHF dependencies')
    base,pbase=load('driver-build');v16,pv16=load('v16-failure');sf,psf=load('diag-source-freeze');release,pr=load('literal3-release');rt,prt=load('literal3-Root-tools')
    if pbase!=plan['actual_Driver2_report_pin']or pv16!=plan['actual_closed_v16_report_pin']or pr!=hf['selected_literal3_actual_release_pin']or prt!=hf['selected_literal3_actual_Root_tool_pin']:raise RuntimeError('exact selected reports and real release authorities')
    genuine_terminal(rt,0)
    lpp=hf['selected_literal3_actual_post_review_pin'];lptp=hf['selected_literal3_actual_post_tools_pin']
    lpost=c.load_json_exact(lpp['path'],lpp['sha256'],json.dumps(lpp['identity']))[0];ltools=c.load_json_exact(lptp['path'],lptp['sha256'],json.dumps(lptp['identity']))[0];la=ltools['actual_review_return']
    if lpost['failure']is not None or lpost['actual_release_receipt_pin']!=pr or ltools['observed_closed']is not True or type(la['exit_code'])is not int or la['exit_code']!=0 or la.get('session_id')is not None or json.loads(la['output'].strip().splitlines()[-1])['review_pin']!=lpp:raise RuntimeError('genuine current literal3 post0 required before any compiler')
    if release['status']!='EXACT_LITERAL3_CLOSED_FAILED_V15_PRIVATE_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'or release['deleted_files']!=3 or release['logical_bytes_released']!=1504027360 or release['original_budget_after']['original_initial_reserve_admitted']is not True:raise RuntimeError('literal3 actualclosed0 release and original reserve required before diagnostic')
    for row in plan['released_only_old_v15_literal3_pins']:
        if os.path.lexists(row['path']):raise RuntimeError('exact retired old-v15 literal3 remain absent')
    if base['schema']!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'or base['status']!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or base['failure']is not None or base['after_check_error']is not None or base['Dragon_linked']is not True or base['final_report_resource_check_passed']is not True or base['actual_host_Source_freeze_pin']!=hf['selected_Driver2_Host_freeze_pin']:raise RuntimeError('genuine current Driver2 closedcompile/link runtime')
    post=c.load_json_exact(hf['selected_closed_v16_actual_post_review_pin']['path'],hf['selected_closed_v16_actual_post_review_pin']['sha256'],json.dumps(hf['selected_closed_v16_actual_post_review_pin']['identity']))[0]
    roottool=c.load_json_exact(hf['selected_closed_v16_Root_tool_pin']['path'],hf['selected_closed_v16_Root_tool_pin']['sha256'],json.dumps(hf['selected_closed_v16_Root_tool_pin']['identity']))[0];genuine_terminal(roottool,1)
    pt=c.load_json_exact(hf['selected_closed_v16_actual_post_tools_pin']['path'],hf['selected_closed_v16_actual_post_tools_pin']['sha256'],json.dumps(hf['selected_closed_v16_actual_post_tools_pin']['identity']))[0];pa=pt['actual_review_return']
    if pt['observed_closed']is not True or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or json.loads(pa['output'].strip().splitlines()[-1])['review_pin']!=hf['selected_closed_v16_actual_post_review_pin']or post['actual_report_pin']!=pv16 or post['actual_Host_freeze_pin']!=hf['selected_closed_v16_Host_freeze_pin']or post['actual_Root_true_tool_return_pin']!=hf['selected_closed_v16_Root_tool_pin']or post['actual_stage_count']!=50 or post['actual_positive_count']!=16 or post['actual_exact_refusal_count']!=33 or post['actual_unexpected_failed_record_indices']!=[49]or post['actual_engineering_three_plane_closed0']is not False:raise RuntimeError('genuine v16 failedBOOT-only context post0, not engineering')
    if v16['status']!='FAILED_UNQUALIFIED_NO_RETRY'or v16['engineering_three_plane_closed0']is not False or v16['failure']!=post['failure']or v16['actual_terminal']is not None:raise RuntimeError('closed v16 remains unqualified')
    if psf!=hf['selected_diag_Fortran_Source_freeze_pin']or psf['path']!=plan['selected_diag_Fortran_Source_freeze_path']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['public_subroutine_ABI_unchanged']is not True or sf['mathematics_conditions_thresholds_and_success_commit_order_unchanged']is not True or sf['failure_only_stdout_plane_and_status']is not True or sf['replacement_zero_based_link_index']!=68 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']or sf['selected_Driver2_Runtime_Host_freeze_pin']!=hf['selected_Driver2_Host_freeze_pin']or sf['selected_Driver2_actual_complete70_report_pin']!=pbase:raise RuntimeError('failure-only diagnostic Source, ABI/math/commit order unchanged')
    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['diagnostic_plan_pin']]);c.verify_rows(sfrows)
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748)
    if caps!=plan['original_caps']or any(binding[k]!=v for k,v in caps.items())or before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:raise RuntimeError('original caps and actual initial fullfresh2 reserve')
    c.closed_report(base,helper,Path(pbase['path']).parent,2)
    inputs=plan['owned_readonly_input_rows'];live={r['path']:r for r in unique(v16['fixed_current_pins']+v16['output_pins'])}
    if len(inputs)!=9 or len({r['owned_filename']for r in inputs})!=9 or any(live.get(r['target_pin']['path'])!=r['target_pin']for r in inputs):raise RuntimeError('nine exact actual readonly v16 inputs for ordinary own copies')
    planned,new70=make_commands(c,base,plan,sf['diagnostic_source_pin']);old70=plan['current_ordered70_input_pins'];old9=plan['current_nine_core_object_pins']
    fixed=unique(fixed+[phf,hf['host_source'],pp,pbase,pv16,psf,pr,prt]+deps+sfrows+base['fixed_current_pins']+base['output_pins']+v16['fixed_current_pins']+v16['output_pins']+old70+old9+[r['target_pin']for r in inputs]);c.verify_rows(fixed)
    OUT.mkdir();(OUT/'build').mkdir();(OUT/'runtime').mkdir();WORK.mkdir()
    (OUT/'one-BOOT-diagnostic').mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py');owned=[c.pin(OUT/'runtime/run_bounded_dragon.py')]
    copied=[]
    for row in inputs:
        source=row['target_pin'];target=WORK/row['owned_filename'];c.same_pin(source['path'],source)
        if target.exists()or target.is_symlink():raise RuntimeError('fresh ordinary input copy only')
        shutil.copy2(source['path'],target);new=c.pin(target);z=target.lstat()
        if new['sha256']!=source['sha256']or new['size_bytes']!=source['size_bytes']or new['identity'][:2]==source['identity'][:2]or not stat.S_ISREG(z.st_mode)or z.st_uid!=os.getuid()or z.st_nlink!=1:raise RuntimeError('exact sourceEOF/after7 and distinct owned same-byte copy UID/nlink1')
        c.same_pin(source['path'],source);owned.append(new);copied.append(dict(original_readonly_pin=source,owned_readonly_copy_pin=new))

    phase=PhaseResources(base_resources);phase.phase='build';resources=phase
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'one-BOOT-diagnostic',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('original OwnRSS supervisor/MRO/guard')
    deck=WORK/'BOOT_diagnostic.x2m';deck.write_text(plan['exact_BOOT_deck']);owned.append(c.pin(deck));first=FirstFatal();after=None;outcome=None;seal=None;watches=[]
    def check():
        c.check_full_current(fixed,owned)
        if not 0<time.monotonic()-start<1800:raise RuntimeError('original whole1800 includes final publication')
        return resources.check()
    try:
        for label,command in zip(('compile_BOOT_diagnostic','link_Dragon'),planned[:2]):
            check();runner.execute(OUT/'build',label,command,600);watches.append(helper.check_watch(OUT,runner.records[-1]))
            if label=='compile_BOOT_diagnostic':
                names=sorted(['SPOBOOX64.o','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json'])
                if sorted(p.name for p in (OUT/'build').iterdir())!=names:raise RuntimeError('one object+compile log/watch; no MODULE/other outputs')
                for name in names:
                    p=OUT/'build'/name;s=p.lstat()
                    if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or s.st_uid!=os.getuid():raise RuntimeError('ordinary compile outputs owned UID/nlink1')
                    c.pin(p)
                owned.append(c.pin(OUT/'build/SPOBOOX64.o'))
            else:owned.append(c.pin(OUT/'runtime/Dragon'))
            after=check()
        phase.phase='BOOT';check();expected=None;tb=None
        try:runner.execute(WORK,'BOOT_diagnostic',planned[2],600,deck=deck.name)
        except RuntimeError as exc:
            expected=exc;tb=exc.__traceback__;first.capture(exc,'actual_original_failed_BOOT_child')
        outcome,seal=read_BOOT_outcome(c,runner,expected,tb)
        if seal is not None:
            hp=plan['readonly_pair_helper_pin'];c.same_pin(hp['path'],hp);spec=importlib.util.spec_from_file_location('known_readonly_BOOT_pair_helper',hp['path']);data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
            terminal=data.final_readback(WORK/'closed_boot_axial.xsm',WORK/'closed_boot_archive.xsm');outcome['complete_terminal_readback']=terminal
            owned.extend(c.pin(WORK/n)for n in('closed_boot_axial.xsm','closed_boot_archive.xsm'))
        after=check();c.verify_rows(old70+old9)
    except BaseException as exc:first.capture(exc,'compile_link_or_single_BOOT')
    try:after=check()
    except BaseException as exc:first.capture(exc,'after_original_resource_check')
    good=first.error is None and outcome is not None and outcome['actual_exit_code']==0 and len(runner.records)==3 and [r['status']for r in runner.records[:2]]==['PASS','PASS']
    target=OUT/'Root_actual_one_BOOT_status_diagnostic_summary.json';summary=None
    try:
        phase.pending_publication_reserved_bytes=8*MI
        summary=dict(schema='ACTUAL_GUARDED_ONE_BOOT_RETURN_STATUS_DIAGNOSTIC_V1',status='ACTUAL_ONE_BOOT_ORIGINAL_SEAL_READBACK_CLOSED_ONLY'if good else'FAILED_DIAGNOSTIC_UNQUALIFIED',failure=None if first.error is None else repr(first.error),first_failure_secondary_errors=list(first.secondary),records=runner.records,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],owned_runtime_pins=owned,exact_owned_readonly_input_copy_proofs=copied,symlink_or_hardlink_input_aliases_used=False,old_v16_inputs_full_EOF_and_all7_preserved=True,actual_outcome=outcome,exact_failure_status_evidence_completed=outcome is not None and outcome['actual_exit_code']==1,actual_host_Source_freeze_pin=phf,actual_diagnostic_Fortran_Source_freeze_pin=psf,original_actual_Driver2_report_pin=pbase,actual_closed_v16_context_report_pin=pv16,required_literal3_actual_release_pin=pr,actual_commands=planned,actual_ordered70_link_inputs=new70,replacement_zero_based_link_index=68,other69_current_Driver37_BOOTQ40_math57_and_four_archives_unchanged=True,current_all9_core_objects_unchanged=True,actual_watchdog_checks=watches,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=caps,resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,full50_executed=False,GLOBAL_or_PROJECT_reexecuted=False,expected_child_failure_record_never_changed_to_PASS=True,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,physics_qualified=False,goal_complete=False)
        c.write(target,summary);phase.pending_publication_reserved_bytes=0;summary['resources_after_including_summary_bytes']=check();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check()
    except BaseException as exc:
        first.capture(exc,'summary_publication_or_final_check')
        try:
            if summary is not None:
                summary.update(status='FAILED_DIAGNOSTIC_UNQUALIFIED',failure=repr(first.error),first_failure_secondary_errors=list(first.secondary),final_report_resource_check_passed=False)
                if target.exists():rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as later:first.capture(later,'failed_summary_publication')
    first.reraise()
    if not good:raise RuntimeError('incomplete guarded three-stage diagnostic; no retry')

if __name__=='__main__':main()

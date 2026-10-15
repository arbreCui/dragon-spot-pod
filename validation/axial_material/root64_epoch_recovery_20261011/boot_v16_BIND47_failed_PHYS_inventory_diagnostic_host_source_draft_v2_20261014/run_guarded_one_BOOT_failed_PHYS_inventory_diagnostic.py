#!/usr/bin/env python3
"""Source draft: guarded compile47/link70/one BOOT explicit BIND return diagnostic. No GLOBAL/PROJECT/full50 rerun."""
import argparse,hashlib,importlib.util,json,os,shutil,stat,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).absolute().parent
PLAN=HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json'
OUT=R/'validation/artifacts/axial-material-new-one-BOOT-failed-PHYS-group-inventory-diagnostic-20261014-v1'
WORK=OUT/'AAA'
COMMON=REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py'
COMMON_SHA='a5b774a6b62e229f8f6360a284354e2f0af8ff3860602b061de376b2624fc040'
MI=2**20
HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC_HOST_SOURCE_ONLY_FREEZE_V1'
SF_SCHEMA='COMPLETE_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'

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

def core_pin(row):
    return {k:row[k]for k in ('path','sha256','size_bytes','identity')}

def retained_current_rows(rows,retired):
    # Only the five literal prior complete pins may become historical. Never skip missing files.
    table={r['path']:core_pin(r)for r in retired}
    result=[]
    for row in rows:
        if row['path']in table:
            if core_pin(row)!=table[row['path']]:raise RuntimeError('historical retired body pin changed or substituted')
        else:result.append(row)
    return unique(result)

def make_commands(c,base,plan,source):
    old=list(base['actual_ordered70_link_inputs']);first=base['records'][0]['command'];last=base['records'][1]['command']
    if len(old)!=70 or len(set(old))!=70 or last!=[first[0],'-O2','-ffp-contract=off',*old,'-o',plan['base_Dragon_pin']['path']]or \
       old!=[p['path']for p in plan['current_ordered70_input_pins']]or old[37]!=plan['retained_Driver37_pin']['path']or \
       old[40]!=plan['retained_BOOTQ40_pin']['path']or old[57]!=plan['retained_math57_pin']['path']or \
       old[68]!=plan['retained_actual_prior_BOXX68_pin']['path']or old[49]!=plan['retained_actual_prior_BOOTB49_pin']['path']or Path(old[47]).name!='SPOR64_BOOT_BIND64.o'or \
       [p for p in old if p.endswith('.a')]!=[p['path']for p in plan['original_four_archive_pins']]:raise RuntimeError('exact actual diag4 ordered70/37/40/49/57/68/four archives')
    if c.FLAGS!=plan['original_compile_flags']or first[0]!=plan['original_compiler_pin']['path']or \
       [v for v in first if v.startswith('-I')]!=plan['original_compile_include_arguments']:raise RuntimeError('original exact compiler/flags/include order')
    obj=str(OUT/'build/SPOR64_BOOT_BIND64.o');new=list(old);new[47]=obj
    if [i for i,(x,y)in enumerate(zip(old,new))if x!=y]!=[47]:raise RuntimeError('only object47 may be replaced')
    compile_cmd=[first[0],*c.FLAGS,'-I'+str(OUT/'build'),*plan['original_compile_include_arguments'],'-J'+str(OUT/'build'),'-c',source['path'],'-o',obj]
    link_cmd=[*last[:3],*new,'-o',str(OUT/'runtime/Dragon')]
    return [compile_cmd,link_cmd,[str(OUT/'runtime/Dragon')]],new

def parse_BIND_return_chain(rows,plan):
    events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1']
    mapping={r['predicate_id']:r for r in plan['exact_BIND_original_return_mapping']}
    response_sites=[m['original_return_source_line']for m in mapping.values()if m['scope']=='SYSTEM_PAYLOAD_IS_VALID'and 'RESPONSE_GROUP_IS_EXACT('in m['original_condition_statement_complete']]
    if response_sites!=[168]:raise RuntimeError('actual original82 Source maps RESPONSE call to SYSTEM168, not NTOT finite173')
    finite_sites=[m['original_return_source_line']for m in mapping.values()if m['scope']=='RESPONSE_GROUP_IS_EXACT'and 'FINITE_REAL32_RECORD('in m['original_condition_statement_complete']]
    if finite_sites!=[240,245,247,248,249]:raise RuntimeError('actual original82 Source finite-record RESPONSE callsites')
    counts={'SPOR64_BOOT_BIND64_READ':0,'SYSTEM_PAYLOAD_IS_VALID':0,'RESPONSE_GROUP_IS_EXACT':0,'FINITE_REAL32_RECORD':0}
    order={'FINITE_REAL32_RECORD':0,'RESPONSE_GROUP_IS_EXACT':1,'SYSTEM_PAYLOAD_IS_VALID':2,'SPOR64_BOOT_BIND64_READ':3}
    for e in events:
        scope=e.get('scope');m=mapping.get(e.get('predicate_id'))
        if scope not in counts or m is None or m['scope']!=scope or type(e.get('original_return_source_line'))is not int or e['original_return_source_line']!=m['original_return_source_line']or type(e.get('actual_boolean_status_integer'))is not int or e['actual_boolean_status_integer']!=0:raise RuntimeError('exact original BIND scope/predicate/line/false0')
        counts[scope]+=1
        if counts[scope]>1:raise RuntimeError('each failed BIND scope has at most one actual event')
    if not events or counts['SPOR64_BOOT_BIND64_READ']!=1 or events[-1]['scope']!='SPOR64_BOOT_BIND64_READ'or [order[e['scope']]for e in events]!=sorted(order[e['scope']]for e in events):raise RuntimeError('nested callee-to-caller BIND chain ending READ exactly once')
    by={e['scope']:e for e in events};read=by['SPOR64_BOOT_BIND64_READ']
    if read['original_return_source_line']!=97:
        if len(events)!=1:raise RuntimeError('non97 READ cannot have SYSTEM/RESPONSE/FINITE events')
    else:
        if counts['SYSTEM_PAYLOAD_IS_VALID']!=1:raise RuntimeError('READ97 requires original SYSTEM failed explicit return')
        system=by['SYSTEM_PAYLOAD_IS_VALID']
        if system['original_return_source_line']==response_sites[0]:
            if counts['RESPONSE_GROUP_IS_EXACT']!=1:raise RuntimeError('SYSTEM168 requires failed RESPONSE child')
        elif counts['RESPONSE_GROUP_IS_EXACT']or counts['FINITE_REAL32_RECORD']:raise RuntimeError('only SYSTEM168 can have RESPONSE/FINITE chain')
        if counts['FINITE_REAL32_RECORD']:
            if counts['RESPONSE_GROUP_IS_EXACT']!=1 or by['RESPONSE_GROUP_IS_EXACT']['original_return_source_line']not in finite_sites:raise RuntimeError('FINITE child only at original RESPONSE finite-record guards')
    # FINITE implicit finite-false has no new exit/event; RESPONSE-first remains valid.
    return events

def parse_failed_PHYS_inventory(rows,chain,outer):
    schema='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1'
    events=[r for r in rows if r.get('schema')==schema]
    by={e['scope']:e for e in chain};system=by.get('SYSTEM_PAYLOAD_IS_VALID');response=by.get('RESPONSE_GROUP_IS_EXACT')
    called=system is not None and system['original_return_source_line']==168
    callers=[e for e in events if e.get('event')=='caller'];headers=[e for e in events if e.get('event')!='caller']
    def integer(d,k):
        if type(d.get(k))is not int:raise RuntimeError('actual header integer only '+k)
        return d[k]
    caller=None
    if called:
        if len(callers)!=1:raise RuntimeError('original SYSTEM168 requires one actual group/plane caller')
        caller=callers[0]
        if set(caller)!={'schema','event','original_return_source_line','group_index','plane_index'}or integer(caller,'original_return_source_line')!=168 or not 1<=integer(caller,'group_index')<=370 or integer(caller,'plane_index')!=outer['boot_plane']:raise RuntimeError('exact original caller168/group1..370/actual outer plane')
        if not rows.index(system)<rows.index(caller)<rows.index(by['SPOR64_BOOT_BIND64_READ']):raise RuntimeError('actual SYSTEM168 then caller then READ97')
    elif events:raise RuntimeError('inventory/caller events only on actual SYSTEM168 RESPONSE failure path')
    expected=response is not None and response['original_return_source_line']==236
    if not expected:
        if headers:raise RuntimeError('failed PHYS inventory headers only after actual RESPONSE236')
        return dict(actual_inventory_header_events_observed=False,actual_complete_header_inventory_observed=False,actual_caller=caller)
    if not called or len(headers)<2 or headers[0].get('event')!='begin'or headers[-1].get('event')!='end'or any(e.get('event')!='record'for e in headers[1:-1]):raise RuntimeError('one bounded actual PHYS begin/ordered records/end sequence')
    begin=headers[0];end=headers[-1];records=headers[1:-1]
    if set(begin)!={'schema','event','original_return_source_line','maximum_records','expected_schema','expected_count','associated_integer','empty_integer','object_length','memory_integer'}or integer(begin,'original_return_source_line')!=236 or integer(begin,'maximum_records')!=64 or begin['expected_schema']!='SCHEMA_RESPONSE_GROUP_PHYS'or integer(begin,'expected_count')!=15 or any(integer(begin,k)not in(0,1)for k in('associated_integer','empty_integer','memory_integer')):raise RuntimeError('exact actual PHYS15 header64 and observed preflight flags')
    integer(begin,'object_length')
    if set(end)!={'schema','event','original_return_source_line','record_count','complete_integer','truncated_integer'}or integer(end,'original_return_source_line')!=236 or integer(end,'record_count')!=len(records)or not 0<=len(records)<=64 or any(integer(end,k)not in(0,1)for k in('complete_integer','truncated_integer')):raise RuntimeError('exact observed bounded count/complete/truncated flags')
    names=[]
    for i,e in enumerate(records,1):
        if set(e)!={'schema','event','ordinal','name_bytes_hex','length','type'}or integer(e,'ordinal')!=i:raise RuntimeError('exact consecutive actual header record ordinals')
        name=e.get('name_bytes_hex')
        if not isinstance(name,str)or len(name)!=24 or any(c not in'0123456789ABCDEF'for c in name)or bytes.fromhex(name)==b' '*12 or name in names:raise RuntimeError('exact unique all12 name bytes24uppercasehex, no display-name normalization')
        if integer(e,'length')< -1:raise RuntimeError('actual LCMLEN header extent')
        integer(e,'type');names.append(name)
    if end['truncated_integer']==1 and(len(records)!=64 or end['complete_integer']!=0):raise RuntimeError('actual truncation64 cannot be complete')
    complete=end['complete_integer']==1 and end['truncated_integer']==0
    if complete and(begin['associated_integer']!=1 or begin['object_length']!=-1 or(begin['empty_integer']==1 and records)or(begin['empty_integer']==0 and not records)):raise RuntimeError('complete actual header inventory requires observed ordinary directory preflight and consistent empty/count')
    if not rows.index(response)<rows.index(begin)or not rows.index(end)<rows.index(system)or [rows.index(e)for e in headers]!=sorted(rows.index(e)for e in headers):raise RuntimeError('RESPONSE236 then begin/records/end then SYSTEM168; no deck or reordered evidence')
    if any(not rows.index(begin)<rows.index(e)<rows.index(end)for e in records):raise RuntimeError('every actual record is inside unique inventory block')
    return dict(actual_inventory_header_events_observed=True,actual_complete_header_inventory_observed=complete,actual_inventory_begin=begin,actual_inventory_records=records,actual_inventory_end=end,actual_caller=caller,actual_record_payload_not_read_or_dumped=True,actual_partial_or_truncated_never_admitted_as_complete=not complete)

def read_BOOT_outcome(c,runner,expected_error,expected_tb,plan):
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
    predicates=[r for r in rows if r.get('schema')=='ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1']
    completed=[line for line in text.splitlines()if line.strip()=='ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE']
    bind_events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1']
    inventory_events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1']
    if w['returncode']==1:
        if expected_error is None or str(expected_error)!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           text.count('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')!=1 or len(diagnostics)!=1 or seals or completed or len(predicates)!=1:raise RuntimeError('only exact original strict BOOT abort1 is diagnostic, never PASS')
        row=diagnostics[0]
        if type(row.get('boot_plane'))is not int or row['boot_plane']not in(1,2,3)or type(row.get('actual_return_status'))is not int or row['actual_return_status']!=1 or type(row.get('required_committed_status'))is not int or row['required_committed_status']!=8:raise RuntimeError('exact true failure plane/status1/required8')
        predicate=predicates[0];line=predicate.get('original_return_source_line')
        if type(line)is not int or line!=466 or predicate.get('predicate_id')!='BOOTB_INGRESS_RETURN_L0466'or type(predicate.get('actual_return_status'))is not int or predicate['actual_return_status']!=1:raise RuntimeError('original BOOTB466 status1 after failed BIND READ')
        chain=parse_BIND_return_chain(rows,plan)
        inventory=parse_failed_PHYS_inventory(rows,chain,row)
        if any(rows.index(e)>=rows.index(predicate)for e in chain):raise RuntimeError('all BIND nested events must precede BOOTB466')
        if rows.index(predicate)>=rows.index(row):raise RuntimeError('first-admission predicate JSON must precede actual outer BOOT status JSON')
        return dict(kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY',actual_exit_code=1,actual_failed_record_preserved=True,actual_diagnostic=row,actual_first_admission_predicate=predicate,actual_BIND_failed_return_chain=chain,actual_BIND_first_explicit_return=chain[0],actual_failed_PHYS_group_inventory=inventory,actual_log_pin=lp,actual_watchdog_pin=wp,original_expected_child_error_repr=repr(expected_error),original_expected_child_traceback_preserved=True,engineering_qualified=False),None
    if w['returncode']!=0 or expected_error is not None or record['status']!='PASS'or diagnostics or predicates or bind_events or inventory_events or len(seals)!=1 or \
       seals[0].get('status')!='PASS'or seals[0].get('all_payload_bits_equal')is not True or seals[0].get('complete_lifecycle_checked')is not True or \
       (seals[0].get('groups'),seals[0].get('planes'),seals[0].get('epoch'))!=(370,3,0)or 'normal end of execution'not in text or len(completed)!=1:
        if expected_error is not None:raise expected_error.with_traceback(expected_tb)
        raise RuntimeError('actual status8 path requires original genuine full seal/readback, no promotion from missing diagnostic')
    return dict(kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0,actual_Fortran_complete_copy_readback=seals[0],actual_log_pin=lp,actual_watchdog_pin=wp,engineering_qualified=False),seals[0]

def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for prefix in ('prior-probe-failure','bind-source-freeze','host-freeze','exact3-release','exact3-Root-tools'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    a=p.parse_args();start=time.monotonic();c=load_common()
    def load(prefix):
        name=prefix.replace('-','_');return c.load_json_exact(getattr(a,name+'_summary'),getattr(a,name+'_sha256'),getattr(a,name+'_seven_id'))
    hf,phf=load('host-freeze');deps=unique(hf['dependencies']);dt={r['path']:r for r in deps}
    if hf['schema']!=HF_SCHEMA or hf['compiler_executed']is not False or hf['numerical_executed']is not False or hf['host_source']['path']!=str(Path(__file__).absolute()):raise RuntimeError('exact own Source-only first-predicate HF')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(deps)
    pp=hf['diagnostic_host_plan_pin'];plan=c.load_json_exact(pp['path'],pp['sha256'],json.dumps(pp['identity']))[0]
    if pp['path']!=str(PLAN)or dt.get(str(PLAN))!=pp or plan['source_only']is not True or plan['planned_output_root']!=str(OUT)or plan['runtime_authorities_complete']is not True or \
       any(plan[k]is not None for k in ('future_actual_object_pin','future_actual_mod_pin','future_actual_Dragon_pin','future_actual_BOOT_report_pin')):raise RuntimeError('draft is not executable: all real retirement/HF authorities required, no fake actuals')
    selected=('selected_prior_probe_Host_freeze_pin','selected_bind_Fortran_Source_freeze_pin','selected_prior_probe_Root_tool_pin','selected_prior_probe_actual_post_review_pin','selected_prior_probe_actual_post_tools_pin','selected_closed_v16_Host_freeze_pin','selected_closed_v16_Root_tool_pin','selected_closed_v16_actual_post_review_pin','selected_closed_v16_actual_post_tools_pin','selected_exact3_actual_release_pin','selected_exact3_actual_Root_tool_pin','selected_exact3_actual_post_review_pin','selected_exact3_actual_post_tools_pin','selected_exact3_actual_manifest_pin')
    for k in selected:
        if not isinstance(hf[k],dict)or dt.get(hf[k]['path'])!=hf[k]:raise RuntimeError('all selected real authorities in ownHF dependencies')
    base,pbase=load('prior-probe-failure');sf,psf=load('bind-source-freeze');release,pr=load('exact3-release');rt,prt=load('exact3-Root-tools')
    if pbase!=plan['actual_prior_probe_report_pin']or psf!=plan['selected_bind_Fortran_Source_freeze_pin']or pr!=hf['selected_exact3_actual_release_pin']or prt!=hf['selected_exact3_actual_Root_tool_pin']:raise RuntimeError('exact reports/SF/retirement authorities')
    for k in ('selected_exact3_actual_release_pin','selected_exact3_actual_Root_tool_pin','selected_exact3_actual_post_review_pin','selected_exact3_actual_post_tools_pin','selected_exact3_actual_manifest_pin'):
        if plan[k]!=hf[k]:raise RuntimeError('draft pending retirement fields must be replaced by exact genuine actual PFs in final plan')
    genuine_terminal(rt,0)
    lpp=hf['selected_exact3_actual_post_review_pin'];lptp=hf['selected_exact3_actual_post_tools_pin'];mp=hf['selected_exact3_actual_manifest_pin']
    lpost=c.load_json_exact(lpp['path'],lpp['sha256'],json.dumps(lpp['identity']))[0];ltools=c.load_json_exact(lptp['path'],lptp['sha256'],json.dumps(lptp['identity']))[0];la=ltools['actual_review_return']
    mf=c.load_json_exact(mp['path'],mp['sha256'],json.dumps(mp['identity']))[0];retired=plan['exact_historical_retired_private_body_pins']
    if len(retired)!=3 or len({r['path']for r in retired})!=3 or sum(r['size_bytes']for r in retired)!=1277838584 or mf['target_full_EOF_pins']!=retired or release['manifest_pin']!=mp:raise RuntimeError('only five exact retired complete prior pins, no scope expansion')
    if lpost['failure']is not None or not lpost['status'].startswith('PASS')or lpost['actual_release_receipt_pin']!=pr or lpost['actual_Root_true_tool_pin']!=prt or lpost['actual_manifest_pin']!=mp or ltools['observed_closed']is not True or type(la['exit_code'])is not int or la['exit_code']!=0 or la.get('session_id')is not None or json.loads(la['output'].strip().splitlines()[-1])['review_pin']!=lpp:raise RuntimeError('genuine exact5 independent release post0 before any compiler')
    rr=release['deletion_records']
    if release['schema']!=plan['selected_exact3_release_schema']or release['status']!=plan['selected_exact3_release_status']or release['execute_requested']is not True or release['deleted_files']!=3 or release['logical_bytes_released']!=1277838584 or release['original_budget_after']['original_initial_reserve_admitted']is not True or len(rr)!=3 or [r['original_fullpin']for r in rr]!=retired or any(r['actual_unlink_returned']is not True or r['target_directory_fsync_attempted']is not True or r['target_directory_fsync_returned']is not True or r['confirmed_absent']is not True for r in rr):raise RuntimeError('genuine exact5 truthful unlink/fsync/current reserve receipt required')
    for row in retired:
        if os.path.lexists(row['path']):raise RuntimeError('exact retired private body must remain absent')
    if any(r['path']in {x['path']for x in retired}for r in deps):raise RuntimeError('no exact retired body may also be promoted into current ownHF dependencies')
    postp=hf['selected_prior_probe_actual_post_review_pin'];toolp=hf['selected_prior_probe_actual_post_tools_pin']
    post=c.load_json_exact(postp['path'],postp['sha256'],json.dumps(postp['identity']))[0];pt=c.load_json_exact(toolp['path'],toolp['sha256'],json.dumps(toolp['identity']))[0];pa=pt['actual_review_return']
    rootp=hf['selected_prior_probe_Root_tool_pin'];roottool=c.load_json_exact(rootp['path'],rootp['sha256'],json.dumps(rootp['identity']))[0];genuine_terminal(roottool,1)
    if pt['observed_closed']is not True or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or json.loads(pa['output'].strip().splitlines()[-1])['review_pin']!=postp or post['verification_failure']is not None or post['actual_report_pin']!=pbase or post['actual_Host_freeze_pin']!=hf['selected_prior_probe_Host_freeze_pin']or post['actual_Root_true_tool_return_pin']!=rootp or post['actual_stage_count']!=3 or post['actual_stage_statuses']!=['PASS','PASS','FAILED']or post['actual_BOOT_plane']!=1 or post['actual_BOOT_return_status']!=1 or post['all_three_watches_closed_without_limit_failure']is not True or post['actual_original_first_failure_object_traceback_preserved']is not True or post['engineering_qualified']is not False or post['actual_unique_first_admission_predicate']['original_return_source_line']!=466:raise RuntimeError('real closed diag4 predicate-unknown failure1 and independent post0 only')
    if post['schema']!='INDEPENDENT_BIND47_EXPLICIT_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_BIND47_EXPLICIT_RETURN_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_unique_BIND_failed_return_chain']!=plan['actual_prior_failed_BIND_chain']or post['known_sealed_summary_metadata_discrepancy']['original_source_or_sealed_report_modified']is not False:raise RuntimeError('genuine prior RESP236/SYSTEM168/READ97/BOOTB466 failure facts and transparent parser defect')
    if base['schema']!='ACTUAL_GUARDED_ONE_BOOT_BIND47_EXPLICIT_RETURN_DIAGNOSTIC_V1'or base['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or base['failure']!=post['actual_summary_failure']or base['actual_outcome']is not None or base['actual_host_Source_freeze_pin']!=hf['selected_prior_probe_Host_freeze_pin']or base['full50_executed']is not False or base['engineering_qualified']is not False:raise RuntimeError('sealed actual prior parser metadata defect stays original and unqualified')
    if psf!=hf['selected_bind_Fortran_Source_freeze_pin']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['replacement_zero_based_link_index']!=47 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']:raise RuntimeError('exact failure-only BIND Source freeze and object47')
    for flag in plan['required_BIND_Source_freeze_true_flags']:
        if sf[flag]is not True:raise RuntimeError('BIND whole original ABI/conditions/math/statement order obligations')
    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['diagnostic_plan_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)
    sp=sf['control_plan_pin'];sourceplan=c.load_json_exact(sp['path'],sp['sha256'],json.dumps(sp['identity']))[0]
    if sp!=plan['failed_PHYS_inventory_Source_plan_pin']or sourceplan['failed_source_SITE']!=236 or sourceplan['failed_caller_SITE']!=168 or sourceplan['inventory_event_schema']!='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1'or sourceplan['maximum_actual_inventory_records']!=64 or sourceplan['actual_record_content_not_read_or_dumped']is not True or sourceplan['native_schema_gate_not_changed']is not True:raise RuntimeError('actual frozen header-only64 diagnostic Source contract, unchanged original native inventory gate')
    v16pin=plan['actual_closed_v16_report_pin'];v16=c.load_json_exact(v16pin['path'],v16pin['sha256'],json.dumps(v16pin['identity']))[0];pv16=v16pin
    for name in ('selected_prior_probe_Host_freeze_pin','selected_closed_v16_Host_freeze_pin'):
        h=hf[name];oldhf=c.load_json_exact(h['path'],h['sha256'],json.dumps(h['identity']))[0]
        if any(dt.get(r['path'])!=r for r in retained_current_rows(oldhf['dependencies'],retired)):raise RuntimeError('all unretired original dependencies remain exact current ownHF rows')
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748)
    if caps!=plan['original_caps']or any(binding[k]!=v for k,v in caps.items())or before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:raise RuntimeError('original caps and actual initial fullfresh2 reserve')
    inputs=plan['owned_readonly_input_rows'];live={r['path']:r for r in retained_current_rows(base['fixed_current_pins']+base['output_pins'],retired)}
    if len(inputs)!=9 or len({r['owned_filename']for r in inputs})!=9 or any(live.get(r['target_pin']['path'])!=r['target_pin']for r in inputs):raise RuntimeError('nine exact retained actual diag4 readonly copies for new ordinary own copies')
    c.verify_rows(plan['retained_original_v16_nine_input_pins'])
    planned,new70=make_commands(c,base,plan,sf['diagnostic_source_pin']);old70=plan['current_ordered70_input_pins'];old9=plan['current_nine_core_object_pins']
    fixed=unique(retained_current_rows(fixed+[phf,hf['host_source'],pp,pbase,pv16,psf,pr,prt]+deps+sfrows+base['fixed_current_pins']+base['output_pins']+old70+old9+[r['target_pin']for r in inputs]+plan['retained_original_v16_nine_input_pins']+[plan['selected_original_BIND_module_pin']],retired));c.verify_rows(fixed)
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
    deck=WORK/'BOOT_diagnostic.x2m';deck.write_text(plan['exact_BOOT_deck']);owned.append(c.pin(deck));first=FirstFatal();after=None;outcome=None;seal=None;watches=[];actual_preservation_verified=False
    def check():
        nonlocal actual_preservation_verified
        actual_preservation_verified=False
        c.check_full_current(fixed,owned);c.verify_rows(old70+old9)
        if not 0<time.monotonic()-start<1800:raise RuntimeError('original whole1800 includes final publication')
        result=resources.check();actual_preservation_verified=True
        return result
    try:
        for label,command in zip(('compile_BOOT_diagnostic','link_Dragon'),planned[:2]):
            check();runner.execute(OUT/'build',label,command,600);watches.append(helper.check_watch(OUT,runner.records[-1]))
            if label=='compile_BOOT_diagnostic':
                names=sorted(['SPOR64_BOOT_BIND64.o','spor64_boot_bind64.mod','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json'])
                if sorted(p.name for p in (OUT/'build').iterdir())!=names:raise RuntimeError('one object+exact same-ABI module+compile log/watch; no other outputs')
                for name in names:
                    p=OUT/'build'/name;s=p.lstat()
                    if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or s.st_uid!=os.getuid():raise RuntimeError('ordinary compile outputs owned UID/nlink1')
                    c.pin(p)
                oldmod=plan['selected_original_BIND_module_pin'];c.same_pin(oldmod['path'],oldmod);newmod=c.pin(OUT/'build/spor64_boot_bind64.mod')
                if newmod['sha256']!=oldmod['sha256']or newmod['size_bytes']!=oldmod['size_bytes']:raise RuntimeError('new module public ABI must be exactly same whole bytes as selected old module')
                c.same_pin(oldmod['path'],oldmod);owned.extend([c.pin(OUT/'build/SPOR64_BOOT_BIND64.o'),newmod])
            else:
                if sorted(p.name for p in(OUT/'build').iterdir())!=sorted(['SPOR64_BOOT_BIND64.o','spor64_boot_bind64.mod','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json','link_Dragon.log','link_Dragon.watchdog.json']):raise RuntimeError('exact six closed build files only')
                owned.append(c.pin(OUT/'runtime/Dragon'))
            after=check()
        phase.phase='BOOT';check();expected=None;tb=None
        try:runner.execute(WORK,'BOOT_diagnostic',planned[2],600,deck=deck.name)
        except RuntimeError as exc:
            expected=exc;tb=exc.__traceback__;first.capture(exc,'actual_original_failed_BOOT_child')
        outcome,seal=read_BOOT_outcome(c,runner,expected,tb,plan)
        if seal is not None:
            hp=plan['readonly_pair_helper_pin'];c.same_pin(hp['path'],hp);spec=importlib.util.spec_from_file_location('known_readonly_BOOT_pair_helper',hp['path']);data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
            terminal=data.final_readback(WORK/'closed_boot_axial.xsm',WORK/'closed_boot_archive.xsm');outcome['complete_terminal_readback']=terminal
            owned.extend(c.pin(WORK/n)for n in('closed_boot_axial.xsm','closed_boot_archive.xsm'))
        after=check()
    except BaseException as exc:first.capture(exc,'compile_link_or_single_BOOT')
    try:after=check()
    except BaseException as exc:first.capture(exc,'after_original_resource_check')
    good=first.error is None and outcome is not None and outcome['actual_exit_code']==0 and len(runner.records)==3 and [r['status']for r in runner.records[:2]]==['PASS','PASS']
    target=OUT/'Root_actual_one_BOOT_status_diagnostic_summary.json';summary=None
    try:
        phase.pending_publication_reserved_bytes=8*MI
        summary=dict(schema='ACTUAL_GUARDED_ONE_BOOT_BIND47_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_V1',status='ACTUAL_ONE_BOOT_ORIGINAL_SEAL_READBACK_CLOSED_ONLY'if good else'FAILED_DIAGNOSTIC_UNQUALIFIED',failure=None if first.error is None else repr(first.error),first_failure_secondary_errors=list(first.secondary),records=runner.records,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],owned_runtime_pins=owned,exact_owned_readonly_input_copy_proofs=copied,symlink_or_hardlink_input_aliases_used=False,retained_original9_old_diag4_eight_prior_probe_eight_latest_probe_nine_input_sources_full_EOF_and_all7_preserved=actual_preservation_verified,actual_outcome=outcome,exact_failure_status_evidence_completed=outcome is not None and outcome['actual_exit_code']==1,actual_complete_failed_PHYS_header_inventory_observed=outcome is not None and outcome['actual_exit_code']==1 and outcome['actual_failed_PHYS_group_inventory']['actual_complete_header_inventory_observed']is True,actual_host_Source_freeze_pin=phf,actual_diagnostic_Fortran_Source_freeze_pin=psf,original_actual_prior_probe_report_pin=pbase,actual_closed_v16_context_report_pin=pv16,required_exact5_actual_release_pin=pr,historical_retired_exact_private_body_pins=retired,actual_retirement_manifest_pin=mp,actual_commands=planned,actual_ordered70_link_inputs=new70,replacement_zero_based_link_index=47,other69_current_Driver37_BOOTQ40_math57_and_four_archives_unchanged=actual_preservation_verified,current_all9_core_objects_unchanged=actual_preservation_verified,actual_watchdog_checks=watches,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=caps,resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,full50_executed=False,GLOBAL_or_PROJECT_reexecuted=False,expected_child_failure_record_never_changed_to_PASS=True,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,physics_qualified=False,goal_complete=False)
        c.write(target,summary);phase.pending_publication_reserved_bytes=0;summary['resources_after_including_summary_bytes']=check();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check()
    except BaseException as exc:
        actual_preservation_verified=False
        first.capture(exc,'summary_publication_or_final_check')
        try:
            if summary is not None:
                summary.update(status='FAILED_DIAGNOSTIC_UNQUALIFIED',failure=repr(first.error),first_failure_secondary_errors=list(first.secondary),final_report_resource_check_passed=False,retained_original9_old_diag4_eight_prior_probe_eight_latest_probe_nine_input_sources_full_EOF_and_all7_preserved=actual_preservation_verified,other69_current_Driver37_BOOTQ40_math57_and_four_archives_unchanged=actual_preservation_verified,current_all9_core_objects_unchanged=actual_preservation_verified)
                if target.exists():rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as later:first.capture(later,'failed_summary_publication')
    first.reraise()
    if not good:raise RuntimeError('incomplete guarded three-stage diagnostic; no retry')

if __name__=='__main__':main()

"""UNREADY whole original helper methods; Root only may read saved B operands.
No main, import-time IO, compiler, native stage or Source preparation.
"""
import hashlib,importlib.util,json,os,sqlite3,stat,sys
from pathlib import Path

def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current7(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and identity(s)==p['identity'],'literal ordinary frozen current7')
 require(s.st_nlink==1,'single-link ordinary data/Source role');return s

def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m

def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v

def small_saved_input(descriptor,out,budget,adapter):
 sqlpin=descriptor['paired_SQLite_pin'];poolpin=descriptor['paired_original_pool_pin'];current7(sqlpin);current7(poolpin)
 sf=os.open(sqlpin['path'],os.O_RDONLY|os.O_NOFOLLOW);pf=os.open(poolpin['path'],os.O_RDONLY|os.O_NOFOLLOW);db=None
 try:
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'opened SQL/pool full7')
  os.environ['SQLITE_TMPDIR']=str(out)
  db=sqlite3.connect(Path(sqlpin['path']).as_uri()+'?mode=ro&immutable=1',uri=True)
  db.execute('PRAGMA query_only=ON');db.execute('PRAGMA cache_size=-8192');db.execute('PRAGMA mmap_size=0');db.execute('PRAGMA temp_store=FILE')
  db.set_progress_handler(lambda:(budget(),0)[1],1000)
  require(tuple(r[1]for r in db.execute('PRAGMA table_info(records)'))==adapter.SQL_COLUMNS,'original saved native SQLite schema')
  validator=object.__new__(adapter.SavedNativeInput);validator.pool_pin=poolpin
  records=[];payloads=[]
  for path,count in [(('ENERGY',),371)]+[(('MACROLIB','GROUP',g,'OVERV'),8)for g in range(1,371)]:
   budget();key=adapter.path_key(path);result=db.execute('SELECT row FROM records WHERE key=?',(key,)).fetchone();require(result is not None,'exact current record path')
   row=adapter.strict_json(result[0]);validator.validate_row(row)
   require(row['path']==list(path)and row['kind']==2 and row['declared_count']==count and row['original_word_count']==count,'exact current REAL32 record shape')
   begin=row['native_payload_begin_byte'];size=row['native_payload_end_byte']-begin
   require(size==count*4,'whole bounded record bytes');raw=os.pread(pf,size,begin)
   require(len(raw)==size and hashlib.sha256(raw).hexdigest()==row['native_payload_sha256'],'actual complete tiny record hash')
   records.append(row);payloads.append(raw)
  require(sum(map(len,payloads))==1484+370*8*4,'exact 13324 payload bytes, no XSM tree decode')
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'after bounded inputs7')
  current7(sqlpin);current7(poolpin)
  energy=out/'ENERGY371_original_words.bin';expected=out/'OVERV370x8_original_words.bin'
  for target,raw in[(energy,payloads[0]),(expected,b''.join(payloads[1:]))]:
   with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
  return dict(energy_path=str(energy),expected_path=str(expected),actual_original_record_metadata=records,actual_payload_bytes_read=13324,complete_SQLite_or_pool_body_EOF_repeated=False,original_XSM_opened=False)
 finally:
  if db is not None:db.close()
  os.close(pf);os.close(sf)

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

def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:
            raise RuntimeError('inconsistent complete PF for same input path')
        table[row['path']]=row
    return list(table.values())

def safe_repr(error):
    try:return repr(error)
    except BaseException:return '<exception repr unavailable>'

def log_rows(c,root,record):
    path=root/(record['label']+'.log')
    pf=c.pin(path)
    if pf['sha256']!=record['log_sha256']:raise RuntimeError('actual closed stage full log SHA')
    rows=[]
    with path.open('r',encoding='utf-8',errors='strict')as stream:
        for line in stream:
            if len(line)>65536:raise RuntimeError('control JSON/log line bound')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                value=json.loads(line)
                if isinstance(value,dict):rows.append(value)
    c.same_pin(path,pf)
    return rows,pf

from pathlib import Path
import collections
import hashlib
import json
import os
import stat
import time

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
OUT=Path('/private/tmp/spot_ninth_storage_build_cache_independent_review_20261009')
GRAPH=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/input_graph.json'
COLD=Path('/private/tmp/spot_eighth_storage_independent_source_review_20261009/current_cold_dynamic_protected_files.json')
INDEX=ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'
CRIT=ROOT/'validation/storage_cleanup_fifth_20261009/critical_source_scope_scan.json'

def read(p,want):
    raw=Path(p).read_bytes();h=hashlib.sha256(raw).hexdigest();assert h==want,(str(p),h);return json.loads(raw),dict(path=str(p),sha256=h,size=len(raw))

def allstrings(d):
    if isinstance(d,str):yield d
    elif isinstance(d,dict):
        for k,v in d.items():yield from allstrings(k);yield from allstrings(v)
    elif isinstance(d,list):
        for v in d:yield from allstrings(v)

def under(p,r):return p==r or p.startswith(r.rstrip('/')+'/')

def main():
    started=time.monotonic()
    graph,gp=read(GRAPH,'242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
    cold,cp=read(COLD,'11f9f07e92ca6c11ccb90ed4bf58b9d98a0e726bf2893a40e457c32edbc9e161')
    old,op=read(INDEX,'30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
    crit,crp=read(CRIT,'10843bbf7fa7c1eb4dfbc55c089d1044e3112296d6bef5a6219b2e81df643407')
    graphpaths={s for s in allstrings(graph) if s.startswith('/')}
    canonical={r['path'] for r in graph['canonical_files']}
    ns={r[k] for r in graph['namespaces'] for k in ('root','canonical_root')}
    aliasdirs={r[k] for r in graph['aliases'] for k in ('path','target') if r['kind']=='directory'}
    oldfiles=set(old['protected_files']);olddirs=set(old['protected_directories']);oldtargets=set(old['inbound_alias_targets'])
    coldpaths={r['path'] for r in cold['current_cold_dynamic_protected_files']}
    critical=crit['critical_roots_excluded_wholesale']
    dirs=list(ns|aliasdirs|olddirs|set(critical))
    allrows=[];links=[];errors=[];cache_dirs=[]
    for base,dirnames,names in os.walk(ROOT,followlinks=False):
        for n in dirnames+names:
            p=Path(base)/n
            try:
                s=p.lstat()
                if stat.S_ISLNK(s.st_mode):
                    links.append(dict(path=str(p),text=os.readlink(p),target=str(p.resolve()),is_directory=p.is_dir()));continue
                if stat.S_ISDIR(s.st_mode):
                    if n in ('node_modules','__pycache__','.cache','.pytest_cache','.mypy_cache','.ruff_cache','.npm','.venv','CMakeFiles'):
                        cache_dirs.append(str(p))
                    continue
                if not stat.S_ISREG(s.st_mode):continue
                rel=p.relative_to(ROOT)
                row=dict(path=str(p),relative=str(rel),size=s.st_size,allocated_bytes=s.st_blocks*512,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink],family=rel.parts[2] if len(rel.parts)>2 and rel.parts[:2]==('validation','artifacts') else rel.parts[0])
                suffix=p.suffix.lower()
                kind=None
                if suffix in ('.o','.a','.so','.dylib','.mod','.smod','.obj','.dll','.exe'):kind=suffix
                elif suffix in ('.tar','.tgz','.zip','.gz','.bz2','.xz','.7z'):kind='archive'+suffix
                elif '.git'==rel.parts[0]:kind='git_metadata_or_object'
                elif any(under(str(p),s) for s in cache_dirs):kind='cache'
                elif s.st_mode & 0o111 and suffix not in ('.py','.sh','.pl','.rb','.f','.f90','.c','.h','.md','.txt','.x2m'):
                    with p.open('rb') as f:magic=f.read(4)
                    if magic in (b'\xcf\xfa\xed\xfe',b'\xce\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xfe\xed\xfa\xce',b'\xca\xfe\xba\xbe',b'\x7fELF'):kind='executable_binary'
                if kind:row['kind']=kind;allrows.append(row)
            except OSError as e:errors.append(dict(path=str(p),error=repr(e)))
    targetfiles={l['target'] for l in links if not l['is_directory']}
    targetdirs={l['target'] for l in links if l['is_directory']}
    def protection(row):
        p=row['path'];flags=dict(current_graph_literal=p in graphpaths,current_canonical=p in canonical,current_namespace_or_directory_alias=any(under(p,r) for r in ns|aliasdirs),current_cold_dynamic=p in coldpaths,old_protected_file=p in oldfiles,old_protected_directory=any(under(p,r) for r in olddirs),old_alias_target=p in oldtargets,critical_root=any(under(p,r) for r in critical),project_inbound_symlink=p in targetfiles or any(under(p,r) for r in targetdirs),primary_build=any(under(p,str(ROOT/r)) for r in ('lib','Ganlib/lib','src','.git')))
        return flags
    grouped=collections.defaultdict(lambda:dict(files=0,logical_bytes=0,allocated_bytes=0,protected_files=0,protected_allocated_bytes=0,unprotected_files=0,unprotected_allocated_bytes=0))
    families=collections.defaultdict(lambda:dict(files=0,allocated_bytes=0,unprotected_files=0,unprotected_allocated_bytes=0))
    unprotected=[]
    for row in allrows:
        flags=protection(row);row['protection']=flags;row['protected']=any(flags.values())
        k=grouped[row['kind']];k['files']+=1;k['logical_bytes']+=row['size'];k['allocated_bytes']+=row['allocated_bytes']
        f=families[row['family']];f['files']+=1;f['allocated_bytes']+=row['allocated_bytes']
        if row['protected']:k['protected_files']+=1;k['protected_allocated_bytes']+=row['allocated_bytes']
        else:
            k['unprotected_files']+=1;k['unprotected_allocated_bytes']+=row['allocated_bytes'];f['unprotected_files']+=1;f['unprotected_allocated_bytes']+=row['allocated_bytes'];unprotected.append(row)
    # Original prior cleanup manifests and restore utilities are evidence; never alter them.
    previous=[]
    for base in sorted((ROOT/'validation').glob('storage_cleanup*')):
        if not base.is_dir():continue
        for p in base.iterdir():
            if p.is_file() and not p.is_symlink() and (p.suffix=='.py' and 'restore' in p.name or p.suffix=='.json' and any(s in p.name for s in ('manifest','cleanup_result','preflight'))):
                raw=p.read_bytes();previous.append(dict(path=str(p),size=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    data=dict(status='READ_ONLY_BUILD_CACHE_METADATA_SCREEN_NOT_DELETION_APPROVAL',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),graph=gp,current_graph_counts=dict(canonical_files=len(canonical),namespaces=len(ns)//2 if False else len(graph['namespaces']),aliases=len(graph['aliases']),live_resource_roots=len(graph['live_resource_roots'])),current_cold_dynamic=cp,current_cold_protected_count=len(coldpaths),old_index=op,critical_scopes=crp,project_symlinks=len(links),stat_errors=errors,classes=dict(grouped),families=dict(sorted(families.items(),key=lambda v:-v[1]['unprotected_allocated_bytes'])),cache_directories=cache_dirs,prior_cleanup_evidence_pins=previous,all_build_cache_file_metadata=allrows,unprotected_candidates=unprotected,files_deleted=0,business_API_imported=False,PREP_or_RUN_executed=False,formal_or_ART_write=False,elapsed_seconds=time.monotonic()-started)
    target=OUT/'build_cache_metadata_screen.json'
    with target.open('x') as stream:json.dump(data,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status=data['status'],path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),classes=dict(grouped),largest_unprotected_families=list(data['families'].items())[:12],cache_directories=cache_dirs[:15],cache_directory_count=len(cache_dirs),stat_errors=len(errors),symlinks=len(links),elapsed_seconds=data['elapsed_seconds'])))

if __name__=='__main__':main()

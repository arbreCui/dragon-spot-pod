from pathlib import Path
import ast,collections,hashlib,json,os,stat,time
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=ROOT/'validation/storage_cleanup_eighth_20261009'
OUT=Path('/private/tmp/spot_eighth_cleanup_independent_source_review_20261009')
MANIFEST_SHA='dcc76b4a6f6cdacd52edcaf004d206d64018f0d7b72b4f9e303e1aacf8529e8a'
PREFLIGHT_SHA='450db036dff5b651a7b1a72d98217b7320023cea8ff5688f220e33a95a719f26'
SOURCE_SHA='be4e2c1e3a5c5bf2856a8d7bf5fa5e8620506d64b3779b57a2360d0e8d6a9f65'
FRESH={}; START=time.monotonic()
if not __debug__:raise ValueError('optimized independent safety review refused')
def need(v,msg):
    if not v:raise ValueError(msg)
def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,wanted=None,keep=False):
    p=Path(p);k=str(p)
    if k in FRESH:
        r=FRESH[k];need(wanted is None or r['sha256']==wanted,'cached SHA mismatch '+k)
        return r,p.read_bytes() if keep else None
    a=identity(p);need(stat.S_ISREG(a[2]),'not regular '+k)
    h=hashlib.sha256();parts=[]
    with p.open('rb') as stream:
        fs=os.fstat(stream.fileno());need([fs.st_dev,fs.st_ino]==a[:2],'open inode mismatch '+k)
        while block:=stream.read(4*1024**2):
            h.update(block)
            if keep:parts.append(block)
    need(identity(p)==a,'file changed during full read '+k)
    r=dict(path=k,identity=a,size=a[3],sha256=h.hexdigest())
    need(wanted is None or r['sha256']==wanted,'full SHA mismatch '+k)
    FRESH[k]=r;return r,b''.join(parts) if keep else None
def expected(r):
    value,_=pin(r['path'],r['sha256'])
    need(value['identity']==r['identity'] and value['size']==r['size'],'identity/size mismatch '+r['path'])
    return value
def load(p,wanted=None):
    r,b=pin(p,wanted,True)
    def pairs(rows):
        d={}
        for k,v in rows:need(k not in d,'duplicate JSON key '+str(p));d[k]=v
        return d
    v=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite JSON')))
    return r,v
def inventory(excluded):
    h=hashlib.sha256();count=collections.Counter()
    for dp,dn,fn in os.walk(ROOT,followlinks=False):
        dn[:]=sorted(n for n in dn if Path(dp)/n!=BASE)
        for n in sorted(dn+fn):
            p=Path(dp)/n
            if str(p) in excluded:continue
            s=p.lstat();relative=str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):row=[relative,identity(p),os.readlink(p)];count['symlinks']+=1
            elif stat.S_ISDIR(s.st_mode):row=[relative,'directory'];count['directories']+=1
            elif stat.S_ISREG(s.st_mode):row=[relative,identity(p)];count['regular_files']+=1
            else:raise ValueError('nonordinary project object '+str(p))
            h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    return dict(sha256=h.hexdigest(),**dict(count))
def links(selected):
    rows=[]
    for dp,dn,fn in os.walk(ROOT,followlinks=False):
        for n in dn+fn:
            p=Path(dp)/n
            if p.is_symlink():
                a=identity(p);raw=os.readlink(p);target=p.resolve(strict=False);need(identity(p)==a,'link changed')
                need(not any(Path(q)==target or Path(q).is_relative_to(target) for q in selected),'inbound link to candidate '+str(p))
                rows.append([str(p),raw,str(target)])
    return dict(count=len(rows),sha256=hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest())
def abswalk(v,found):
    if isinstance(v,dict):
        for k,x in v.items():abswalk(k,found);abswalk(x,found)
    elif isinstance(v,list):
        for x in v:abswalk(x,found)
    elif isinstance(v,str) and v.startswith('/'):found.add(v)
def save(n,v):
    p=OUT/n
    with p.open('x')as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size}
def main():
    mp,m=load(BASE/'manifest.json',MANIFEST_SHA)
    pp,pf=load(BASE/'preflight.json',PREFLIGHT_SHA)
    rvpin,rv=load(BASE/'independent_preflight_review.json','1aeae74ddae9bda4e749ba39850c500c16ab8313bbcdd2ee17abba1431ad8daf')
    ap,actual=load(BASE/'cleanup_result.json','170ff40befd04a6c47fdae49bbd2f667569cf8dcd0007e9d5518b1640f5448e8')
    tp,terminal=load(BASE/'cleanup_terminal_observation.json','fba675db602eb690e8fc3bcdcdb12218fa0445d4d93bf9ecd1063b6946991908')
    lp,raw=pin(BASE/'retirement_ledger.jsonl','eb12e21a5d35221c363e92b284df30e0178f366b5f84eec081f894ea11fdf8ad',True)
    ledger=[json.loads(line)for line in raw.decode().splitlines()]
    source,_=pin(BASE/'cleanup_exact_files.py',SOURCE_SHA)
    need(m['cleanup_source_sha256']==SOURCE_SHA,'actual cleanup source changed')
    need(rv['status']=='PASS' and rv['manifest_sha256']==mp['sha256'] and rv['preflight_sha256']==pp['sha256'],'independent preflight contract')
    need(actual['status']=='PASS' and actual['manifest_sha256']==mp['sha256'] and actual['preflight_sha256']==pp['sha256'] and actual['independent_preflight_sha256']==rvpin['sha256'],'actual result identity chain')
    need(actual['solver_or_API_executed'] is False and actual['new_scientific_credit'] is False,'actual cleanup credit/scope changed')
    need(terminal['exit_code']==0 and terminal['closed'] is True and terminal['initial_chunk_id']=='471f35' and terminal['terminal_chunk_id']=='7058d5','actual Root tool not true closed exit 0')
    need(terminal['manifest_sha256']==actual['manifest_sha256'] and terminal['actual_stdout_status']=='PASS' and terminal['deleted_files']==13 and terminal['deleted_allocated_bytes']==423231488 and terminal['solver_or_API_executed'] is False and terminal['new_scientific_credit'] is False,'actual Root terminal scope/identity mismatch')
    need(terminal['cleanup_result_sha256']==ap['sha256'],'actual Root result terminal pin mismatch')
    selected={c['path']for c in m['candidates']};need(len(selected)==m['exact_count']==len(ledger)==actual['deleted_files']==13,'actual exact count mismatch')
    need(actual['deleted_logical_bytes']==m['logical_bytes']==423204200 and actual['deleted_allocated_bytes']==m['allocated_bytes']==423231488,'actual bytes mismatch')
    for c,row,pinned in zip(m['candidates'],ledger,pf['verified_candidates']):
        need(row['deleted'] is True and row['category']==c['category'],'ledger deletion category mismatch')
        need(all(row[k]==pinned[k]==c[k]for k in ('path','identity','size','sha256')),'ledger/preflight/fullmanifest mismatch')
        p=Path(c['path']);need(not os.path.lexists(p),'deleted candidate still exists')
        need(p.parent.resolve(strict=True)==p.parent and p.is_relative_to(ART),'deleted canonical parent changed')
    need({r['path']for r in ledger}==selected,'actual ledger paths mismatch')
    before=inventory(selected);need(before==pf['preservation_baseline']==rv['preservation_baseline_after']==actual['nonselected_before']==actual['nonselected_after'],'actual nonselected baseline changed')
    link_before=links(selected);need(link_before==pf['symlink_screen']==actual['symlink_check_after'] and link_before['count']==687,'actual links changed')
    proof_records=[expected(r)for r in m['source_and_review_pins']];primaries=[expected(r)for r in m['retained_primaries']]
    need(len(proof_records)==392 and len(primaries)==12 and primaries==pf['verified_primaries'],'actual retained source/primary mismatch')
    gp=expected(m['graph_pin']);ip=expected(m['old_index_pin']);_,g=load(gp['path'],gp['sha256']);_,idx=load(ip['path'],ip['sha256'])
    absolute=set();abswalk(g,absolute)
    directories=set(x['canonical_root']for x in g['namespaces'])|set(x['target']for x in g['aliases']if x['kind']in('dir','directory'))|set(idx['protected_directories'])|set(m['critical_roots'])
    protected=absolute|set(idx['protected_files'])|set(idx['inbound_alias_targets'])|set(m['current_cold_extra_protected_files'])
    need(not selected&protected and not any(p==d or p.startswith(d+'/')for p in selected for d in directories),'actual preserved closure intersection')
    need(len(g['canonical_files'])==35646 and len(g['requirements']['rows'])==235528 and len(g['namespaces'])==86 and len(g['aliases'])==186 and len(g['live_resource_roots'])==225 and len(m['critical_roots'])==88,'actual full scopes changed')
    proof=m['current_cold_dynamic_proof'];expected(proof['report']);expected(proof['extra_holds_report']);_,cold=load(proof['report']['path'],proof['report']['sha256']);_,holds=load(proof['extra_holds_report']['path'],proof['extra_holds_report']['sha256'])
    coldpaths={r['path']for r in cold['current_cold_dynamic_protected_files']};holdpaths={r['path']for k in ('selected','holds','archive_holds')for r in holds[k]}
    need(len(coldpaths)==6194 and len(holdpaths)==85 and set(m['current_cold_extra_protected_files'])==coldpaths|holdpaths and len(coldpaths|holdpaths)==6248,'actual additional cold strict proof union changed')
    need(not selected&(coldpaths|holdpaths) and len(holds['selected'])==42 and len(holds['holds'])==2 and len(holds['archive_holds'])==41,'actual HOLD overlap')
    # These held files were already completely hashed among the 392 source pins.
    need(all(os.path.lexists(p)for p in holdpaths),'an explicit HOLD path disappeared')
    after=inventory(selected);link_after=links(selected)
    need(before==after and link_before==link_after,'actual postdelete review window changed preserved baseline or links')
    need(all(not os.path.lexists(p)for p in selected),'candidate reappeared during actual review')
    for r in FRESH.values():need(identity(r['path'])==r['identity'],'retained bytes identity changed by review end '+r['path'])
    records=save('actual_postdelete_independent_full_sha_records.json',list(FRESH.values()))
    report=dict(schema='SPOT_EIGHTH_INDEPENDENT_ACTUAL_POSTDELETE_REVIEW_V1',status='PASS',manifest_sha256=mp['sha256'],preflight_sha256=pp['sha256'],independent_preflight_sha256=rvpin['sha256'],actual_cleanup_result_sha256=ap['sha256'],actual_Root_terminal_sha256=tp['sha256'],retirement_ledger_sha256=lp['sha256'],cleanup_source_sha256=source['sha256'],Root_actual_true_exit_0_closed=True,exact_deleted_files=13,deleted_logical_bytes=423204200,deleted_allocated_bytes=423231488,all_exact_ledger_rows_match_original_manifest_and_preflight_and_actual_absence=True,all_deleted_canonical_parents_retained=True,independent_fresh_full_SHA_files=len(FRESH),independent_fresh_full_SHA_bytes=sum(r['size']for r in FRESH.values()),retained_primary_full_SHA_count=12,retained_source_and_proof_full_SHA_count=392,all_retained_source_and_primary_bytes_and_identities_unchanged=True,nonselected_before=before,nonselected_after=after,all_nonselected_unchanged_and_equal_Root_preflight=True,all_project_symlinks_before=link_before,all_project_symlinks_after=link_after,current_closure=dict(canonical_files=35646,logical_requirements=235528,namespaces=86,aliases=186,live_resource_roots=225,critical_roots=88,old_protected_files=len(idx['protected_files']),current_cold_dynamic_paths=6194,all_cold_plus_HOLD_paths=6248,candidate_intersections=[]),all_42_material_seed_2_unsealed_and_41_archives_still_HOLD_and_present=True,full_fresh_records_pin=records,historical_whole_replay_and_complete_seal_restore_required=True,root_reported_capacity_before=actual['capacity_before'],root_reported_capacity_after=actual['capacity_after'],APFS_disk_free_change_claimed=False,independent_files_deleted=0,independent_restore_executed=False,business_import_API_native_solver_PREP_RUN_executed=False,formal_or_ART_written=False,new_RSS_or_scientific_credit=False,elapsed_seconds=time.monotonic()-START)
    saved=save('independent_actual_postdelete_review.json',report)
    print(json.dumps(dict(status='PASS',report=saved['path'],sha256=saved['sha256'],fresh_full_SHA_files=len(FRESH),fresh_full_SHA_bytes=report['independent_fresh_full_SHA_bytes'],verified_actual_deleted_files=13,nonselected_unchanged=True,all_12_primaries_392_proofs_unchanged=True,all_extra_cold_6248_protected_paths_preserved=True,independent_files_deleted=0,elapsed_seconds=report['elapsed_seconds'])),flush=True)
if __name__=='__main__':main()

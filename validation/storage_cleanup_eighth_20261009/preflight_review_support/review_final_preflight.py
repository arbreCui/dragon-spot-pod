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
    mp,m=load(BASE/'manifest.json',MANIFEST_SHA);pp,pf=load(BASE/'preflight.json',PREFLIGHT_SHA)
    terminal,tr=load(BASE/'preflight_terminal_observation.json','b50d64c7ec226e4a5610c44be9de85d5b9ccbe23196e1c230704e0b7e16f946d')
    source,_=pin(BASE/'cleanup_exact_files.py',SOURCE_SHA)
    need(m['cleanup_source_sha256']==SOURCE_SHA,'manifest source pin')
    need(m['status'].startswith('READY') or m['status'].startswith('PASS') or m['status'].startswith('ROOT'),'unexpected manifest status')
    need(pf['status']=='PASS' and pf['manifest_sha256']==mp['sha256'] and pf['files_deleted']==0 and pf['solver_or_API_executed'] is False,'Root preflight contract')
    selected={c['path'] for c in m['candidates']}
    need(len(selected)==len(m['candidates'])==m['exact_count']==13,'final exact 13 set')
    need(len(m['retained_primaries'])==12 and len(m['source_and_review_pins'])==392,'final source/primary counts')
    need(sum(c['size'] for c in m['candidates'])==m['logical_bytes']==423204200,'logical total')
    need(sum(c['allocated_bytes'] for c in m['candidates'])==m['allocated_bytes']==423231488,'allocated total')
    need(not selected & {r['path'] for r in m['source_and_review_pins']+m['retained_primaries']},'deleted path in retained proof/primary')
    before=inventory(selected);need(before==pf['preservation_baseline'],'nonselected baseline differs from true Root preflight')
    link_before=links(selected);need(link_before==pf['symlink_screen'] and link_before['count']==687,'full link inventory mismatch')
    source_records=[expected(r)for r in m['source_and_review_pins']]
    primary_records=[expected(r)for r in m['retained_primaries']]
    need(primary_records==pf['verified_primaries'],'Root primary pins mismatch')
    primaries={r['path']:r for r in primary_records};actual=[]
    for c in m['candidates']:
        p=Path(c['path']);need(p.is_absolute() and str(p)==c['path'] and '..' not in p.parts and p.is_relative_to(ART) and p.parent.resolve(strict=True)==p.parent,'noncanonical candidate')
        r=expected(c);need(r['identity'][-1]==1 and not p.is_symlink(),'linked candidate')
        need(p.stat().st_blocks*512==c['allocated_bytes'],'allocated blocks changed')
        need(c['category']=='EXACT_DUPLICATE_OLD_WORK_COPY' and c['historical_whole_replay_restore_required'] is True,'candidate scope/restore limitation')
        primary=primaries[c['retained_primary']];need(primary['path']!=r['path'] and primary['size']==r['size'] and primary['sha256']==r['sha256'],'whole bytes not exact primary')
        need(Path(primary['path']).parent.resolve(strict=True)==Path(primary['path']).parent and primary['identity'][-1]==1,'primary endpoint unsafe')
        actual.append(r)
    need(actual==pf['verified_candidates'],'fresh candidate set differs from Root preflight')
    gp=expected(m['graph_pin']);ip=expected(m['old_index_pin']);_,g=load(gp['path'],gp['sha256']);_,idx=load(ip['path'],ip['sha256'])
    need(gp['sha256']=='9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68','wrong current frozen V7 graph')
    need(ip['sha256']=='30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86','wrong current old index')
    absolute=set();abswalk(g,absolute)
    directories=set(x['canonical_root'] for x in g['namespaces'])|set(x['target']for x in g['aliases']if x['kind']in('dir','directory'))|set(idx['protected_directories'])|set(m['critical_roots'])
    protected=absolute|set(idx['protected_files'])|set(idx['inbound_alias_targets'])|set(m['current_cold_extra_protected_files'])
    for p in selected:need(p not in protected and not any(p==d or p.startswith(d+'/')for d in directories),'current dependency closure intersection '+p)
    need(len(g['canonical_files'])==35646 and len(g['requirements']['rows'])==235528 and len(g['namespaces'])==86 and len(g['aliases'])==186 and len(g['live_resource_roots'])==225 and len(m['critical_roots'])==88,'complete frozen V7 original scopes/counts')
    proof=m['current_cold_dynamic_proof'];expected(proof['report']);expected(proof['extra_holds_report'])
    _,d=load(proof['report']['path'],proof['report']['sha256']);_,material=load(proof['extra_holds_report']['path'],proof['extra_holds_report']['sha256'])
    need(d['status']=='HOLD_ALL_42_MATERIAL_SEED_CANDIDATES_CURRENT_COLD_DYNAMIC_DEPENDENCY' and not d['approved_deletion_paths'],'cold HOLD report contract')
    need(len(d['source_pins_and_actual_function_definitions'])==6 and len(d['actual_pinned_metadata'])==23,'cold proof source/metadata count')
    bound={r['path']:r for r in m['source_and_review_pins']}
    for r in [proof['report'],proof['extra_holds_report']]+d['source_pins_and_actual_function_definitions']+d['actual_pinned_metadata']:
        need(r['path'] in bound and all(bound[r['path']][k]==r[k]for k in ('sha256','size','identity')),'cold proof not fully retained pinned '+r['path']);expected(r)
    for r in d['source_pins_and_actual_function_definitions']:
        _,raw=pin(r['path'],r['sha256'],True);text=raw.decode();tree=ast.parse(text);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
        for fn in r['definitions']:
            node=defs[fn['name']];segment=ast.get_source_segment(text,node)
            need(node.lineno==fn['line'] and node.end_lineno==fn['end_line'] and segment==fn['source'] and hashlib.sha256(segment.encode()).hexdigest()==fn['source_sha256'],'cold source function proof mismatch')
    # Independently rebuild the dynamic metadata path->digest union. No business imports/calls.
    dyn={}
    def add(path,wanted):
        path=str(path);need(path.startswith('/'),'nonabsolute protected descriptor')
        need(path not in dyn or dyn[path]==wanted,'conflicting actual metadata SHA '+path);dyn[path]=wanted
    def readmeta(p,wanted=None):
        need(str(p) in bound,'derived cold metadata not retained pinned '+str(p));return load(p,wanted)[1]
    base=ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007';old=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
    parent_intersections=[];held_material={r['path']for r in material['selected']}
    for directory in (base,old):
        prepared=readmeta(directory/'prepared.json');
        for item in prepared['inputs'].values():add(item['path'],item['sha256'])
        item=prepared['inputs']['material_results'];receipt=readmeta(item['path'],item['sha256'])
        for key in ('producer_runtime','receiver_source'):add(receipt[key]['path'],receipt[key]['sha256'])
        hits=set();protocol_hits=set()
        for state in receipt['states'].values():
            for item in state.values():
                if isinstance(item,dict)and {'path','sha256'}<=set(item):add(item['path'],item['sha256'])
            item=state['execution'];execution=readmeta(item['path'],item['sha256'])
            for p,w in execution['files'].items():add(p,w)
            hits |= held_material & set(execution['files'])
            item=state['snapshot_run_status'];run=readmeta(item['path'],item['sha256']);archive_dir=Path(state['archive']['path']).parent
            for name,w in run['outputs'].items():add(archive_dir/name,w)
            item=state['audit_status'];audit=readmeta(item['path'],item['sha256']);audit_dir=Path(item['path']).parent
            add(audit_dir/'protocol.json',audit['protocol_sha256']);protocol=readmeta(audit_dir/'protocol.json',audit['protocol_sha256'])
            for p,w in protocol['files'].items():add(p,w)
            protocol_hits |= held_material & set(protocol['files'])
            for name,w in audit['outputs'].items():add(audit_dir/name,w)
        variant=readmeta(directory/'runtime/conditional_white_receiver_variant.json')
        for p,w in variant['files'].items():add(p,w)
        parent_intersections.append(dict(parent=str(directory),material_execution_intersection=len(hits),material_protocol_intersection=len(protocol_hits)))
    old_prepared=readmeta(old/'prepared.json');original_manifest=readmeta(old_prepared['inputs']['material_manifest']['path'])
    def descriptors(v):
        if isinstance(v,dict):
            if isinstance(v.get('path'),str)and v['path'].startswith('/')and isinstance(v.get('sha256'),str):add(v['path'],v['sha256'])
            for item in v.values():descriptors(item)
        elif isinstance(v,list):
            for item in v:descriptors(item)
    descriptors(original_manifest)
    saved_dyn={r['path']:r['sha256'] for r in d['current_cold_dynamic_protected_files']}
    need(dyn==saved_dyn and len(dyn)==6194,'independently derived full cold dynamic metadata union mismatch')
    hold={r['path']for k in ('selected','holds','archive_holds')for r in material[k]}
    need(len(material['selected'])==42 and len(material['holds'])==2 and len(material['archive_holds'])==41 and len(hold)==85,'all explicit HOLD counts')
    need(set(m['current_cold_extra_protected_files'])==set(dyn)|hold and len(set(m['current_cold_extra_protected_files']))==6248,'final cold strict exclusion union mismatch')
    need(len(held_material & set(dyn))==31 and not selected&(hold|set(dyn)),'selected intersects real cold or hold scope')
    _,replay=load(BASE/'replay/candidate_exact_restoration_mapping.json','86794a1613ce9efeb29bf046c9794a9cad168506b76eefd692558d9a8c73dbde')
    _,compiled=load(BASE/'compiled/exact_compiled_candidates.json')
    replay_set={r['path']for r in replay['candidates']};compiled_set={r['path']for r in compiled['candidates']}
    need(len(replay_set)==10 and len(compiled_set)==3 and selected==replay_set|compiled_set,'final 13 is not precise admitted candidate author union')
    overlap_pin,_=pin(BASE/'inventory/prior_seven_overlap_screen.json');_,overlap=load(overlap_pin['path']);
    _,restore=load(BASE/'restore_default_list_verification.json')
    after=inventory(selected);link_after=links(selected)
    need(after==before and after==pf['preservation_baseline'] and link_after==link_before,'review window changed nonselected/link baseline')
    for r in FRESH.values():need(identity(r['path'])==r['identity'],'full read identity changed at review end '+r['path'])
    closure_counts=dict(canonical_files=35646,logical_requirements=235528,namespaces=86,aliases=186,live_resource_roots=225,old_protected_files=len(idx['protected_files']),critical_roots=88,all_absolute_graph_strings=len(absolute),dynamic_cold_paths=6194,all_extra_cold_and_hold_paths=6248,candidate_intersections=[])
    record=save('independent_full_fresh_sha_records.json',list(FRESH.values()))
    report=dict(schema='SPOT_EIGHTH_INDEPENDENT_FULL_FRESH_PREFLIGHT_REVIEW_V1',status='PASS',manifest_sha256=mp['sha256'],preflight_sha256=pp['sha256'],cleanup_source_sha256=source['sha256'],actual_Root_preflight_terminal_pin=terminal,exact_candidate_count=13,track_work_copy_count=10,compiled_work_copy_count=3,retained_primary_count=12,source_and_review_pin_count=392,independent_fresh_full_sha_files=len(FRESH),independent_fresh_full_sha_bytes=sum(r['size']for r in FRESH.values()),all_candidates_and_primaries_exact_fresh_SHA_identity_and_regular_singlelink=True,all_retained_proof_bytes_and_identities_fresh=True,preservation_baseline_before=before,preservation_baseline_after=after,all_nonselected_unchanged_and_equal_true_Root_preflight=True,all_project_symlinks_before=link_before,all_project_symlinks_after=link_after,current_closure=closure_counts,independently_rebuilt_cold_source_metadata_protected_union_exact=True,parent_material_intersections=parent_intersections,all_42_material_seeds_2_unsealed_41_archives_HOLD=True,all_dynamic_source_and_metadata_proofs_exactly_bound_to_manifest=True,original_historical_documents_manifests_logs_sources_and_results_retained=True,historical_whole_replay_and_seal_limitation='Historical complete copied-input audits, whole original manifests or replay naming any retired path require exact restoration first. Original evidence remains unchanged; missing historical paths are not passed as live runtime compatibility.',full_sha_records_pin=record,files_deleted=0,restore_executed=False,business_import_API_constructor_native_solver_PREP_RUN_executed=False,formal_or_ART_written=False,new_RSS_or_scientific_credit=False,actual_cleanup_result_sha256=None,elapsed_seconds=time.monotonic()-START)
    saved=save('independent_preflight_review.json',report)
    print(json.dumps(dict(status='PASS',report=saved['path'],sha256=saved['sha256'],manifest_sha256=mp['sha256'],preflight_sha256=pp['sha256'],fresh_full_sha_files=len(FRESH),fresh_full_sha_bytes=report['independent_fresh_full_sha_bytes'],candidate_count=13,full_nonselected_baseline_unchanged=True,cold_dynamic_protected_union=6194,extra_all_holds_union=6248,files_deleted=0,elapsed_seconds=report['elapsed_seconds'])),flush=True)
if __name__=='__main__':main()

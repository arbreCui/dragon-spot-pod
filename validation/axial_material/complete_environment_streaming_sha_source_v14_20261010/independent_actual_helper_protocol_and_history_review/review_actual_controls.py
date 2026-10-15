"""Read authenticated source and existing control evidence; never load helper."""
from pathlib import Path
from collections import Counter
import ast, hashlib, json, math, os, stat, struct, time

D=Path('/private/tmp/axmat_v14_actual_helper_controls_independent_review_20261010')
P=Path('/Users/wen/spot'); A=P/'validation/artifacts'; V=P/'validation/axial_material'
S=V/'complete_environment_streaming_sha_source_v14_20261010'
H=A/'axial-material-complete-environment-streaming-sha-helper-only-host-v14-20261010'
C=A/'axial-material-complete-environment-streaming-sha-helper-only-controls-v14-20261010'
HH=A/'axial-material-complete-environment-streaming-sha-helper-only-host-v14-historical-read-20261010'
HC=A/'axial-material-complete-environment-streaming-sha-helper-only-controls-v14-historical-read-20261010'
pins={}
def identity(p):
    x=Path(p).lstat(); return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p,want=None,ident=None):
    p=Path(p); before=identity(p); assert stat.S_ISREG(before[2]),str(p)
    value=sha(p); assert identity(p)==before,str(p)
    if want is not None:assert value==want,(str(p),value,want)
    if ident is not None:assert before==ident,(str(p),before,ident)
    rec={'path':str(p),'sha256':value,'identity':before};pins[str(p)]=rec;return rec
def unique(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate JSON field')
        d[k]=v
    return d
def read(p,want=None):
    pin(p,want);return json.loads(Path(p).read_text(),object_pairs_hook=unique,
        parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def exact(a,b):
    assert type(a) is type(b),(type(a),type(b))
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:exact(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):exact(x,y)
    elif isinstance(a,float):assert struct.pack('>d',a)==struct.pack('>d',b)
    else:assert a==b,(a,b)
def namespace(root):
    result={}
    for parent,dirs,files in os.walk(root,followlinks=False):
        for name in sorted(dirs+files):
            p=Path(parent)/name;key=str(p.relative_to(root));i=identity(p)
            kind='link' if stat.S_ISLNK(i[2]) else 'dir' if stat.S_ISDIR(i[2]) else 'file' if stat.S_ISREG(i[2]) else 'other'
            assert kind!='other'
            result[key]={'kind':kind,'identity':i}
            if kind=='link':result[key]['readlink']=os.readlink(p)
    return result
def inverse(source,edits):
    text=source
    for e in reversed(edits):
        assert text.count(e['new'])==e['count']
        text=text.replace(e['new'],e['old'])
    return text
def defs(text):
    a=ast.parse(text);return [(n.name,ast.get_source_segment(text,n)) for n in ast.walk(a)
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
started=time.monotonic()
ns_before={str(r):namespace(r) for r in (S,H,C,HH,HC)}
root=read(S/'actual_helper_control_receipts/Root_actual_helper_controls_tool_terminal_return.json',
    '5914404602b0797a8365f3781a7fc278519fca6facc7fd195ce6b70fd3e0bb94')
assert root['schema']=='AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1'
assert root['action']=='fixtures' and root['initial_session_id']==21373
assert root['session_closed'] is True
assert root['call_history'][0]['chunk_id']=='9fe32f' and root['terminal_result']['chunk_id']=='9c9d85'
assert type(root['terminal_result']['exit_code']) is int and root['terminal_result']['exit_code']==0
exact(root['call_history'][-1],root['terminal_result'])
for k in ('stdout','stderr'):pin(root[k]['path'],root[k]['sha256']);assert identity(root[k]['path'])[4]==root[k]['size_bytes']
assert root['stderr']['size_bytes']==0
host=read(H/'result.json','3f0515b181169da0253661f7a6ac706819b4eaa62ad89e28e592dba07c9626ec')
out=read(C/'result.json','002467a8fe0fc4ae9246563c1902c02d44ba1d57ea61c7882255a01592b37440')
raw=read(C/'raw_preservation_manifest.json')
bound=read(S/'actual_control_sources/exact_source_binding_inverse.json')
helper=Path(bound['helper']['path']);pin(helper,bound['helper']['sha256'])
assert bound['helper']['sha256']==root['source_helper_sha256']=='839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
proof=read(bound['source_patch_proof']['path'],bound['source_patch_proof']['sha256'])
parent=Path(proof['parent_helper']['path']);pin(parent,proof['parent_helper']['sha256'])
assert inverse(helper.read_text(),proof['edits'])==parent.read_text()
olddefs=dict(defs(parent.read_text())); newdefs=dict(defs(helper.read_text()))
assert len(olddefs)==34
assert [n for n in olddefs if olddefs[n]!=newdefs[n]]==['digest']
source_inverse={}
for k in ('driver','host'):
    d=bound[k];p=Path(d['bound_source']['path']);q=Path(d['source_unready']['path'])
    pin(p,d['bound_source']['sha256']);pin(q,d['source_unready']['sha256'])
    assert inverse(p.read_text(),d['edits'])==q.read_text()
    assert defs(p.read_text())==defs(q.read_text())
    source_inverse[k]={'complete_inverse':True,'definitions_byteexact':len(defs(p.read_text()))}
for row in host['input_sources']+[host['original_helper'],host['resource_factory']]:pin(row['path'],row['sha256'],row['identity'])
for k in ('actual_full_merged_stdout_stderr','actual_child_result','actual_watchdog'):
    row=host[k];pin(row['path'],row['sha256'],row['identity'])
pin(out['source']['path'],out['source']['sha256'],out['source']['identity'])
pin(H/'runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
root_stdout=read(root['stdout']['path']);assert root_stdout['status']==host['status']=='PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST'
assert root_stdout['action']==host['action']=='fixtures'
row=root_stdout['host_result'];pin(row['path'],row['sha256'],row['identity'])
assert root_stdout['actual_external_Root_terminal_still_required'] is True
watch=read(H/'run/controls.watchdog.json');exact(watch,host['watchdog'])
assert type(watch['returncode']) is int and watch['returncode']==0 and type(watch['pid']) is int and watch['pid']==70564
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['limit_failure'] is None
assert watch['rss_cap_mib']==512 and 0<watch['wall_cap_seconds']<=120
assert watch['sampled_peak_rss_mib']==0.0
assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']
expectedcmd=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(S/'actual_control_sources/helper_only_controls.py'),'--action','fixtures','--out',str(C)]
exact(watch['command'],expectedcmd);exact(host['actual_command'],expectedcmd)
journal=read(H/'HELPER_ONLY_CONTROLS/stages.json');exact(journal['stages'],host['stage_records']);assert len(journal['stages'])==1
stage=journal['stages'][0];assert stage['label']=='run/controls' and stage['status']=='PASS'
exact(stage['command'],expectedcmd);assert stage['log_sha256']==sha(H/'run/controls.log')
assert watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=120
assert watch['elapsed_seconds']<=stage['elapsed_seconds']<stage['wall_cap_seconds']
child_stdout=read(H/'run/controls.log');assert child_stdout['status']==out['status']=='PASS_HELPER_PROTOCOL_ONLY'
assert child_stdout['action']==out['action']=='fixtures' and child_stdout['result_sha256']==sha(C/'result.json')
assert child_stdout['Root_actual_child_terminal_required_before_admission'] is True
for k,v in {'whole_wall_cap_seconds':120,'rss_cap_mib':512,'archive_cap_bytes':64*2**20,'threads':1,'children_at_once':1,'retries':0}.items():exact(host[k],v)
assert 0<host['whole_elapsed_seconds']<120 and 0<out['elapsed_seconds']<watch['elapsed_seconds']
assert host['whole_archive_bytes']<64*2**20
exact(out['Root_external_watchdog_required'],{'wall_seconds':120,'rss_mib':512,'children_at_once':1,'retries':0,'threads':1})
assert out['archive_cap_bytes']==64*2**20
for obj in (host,out,root):
    for key in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert obj[key] is False
for key in ('supervisor_class_or_MRO_modified','failed_V13_audit_reexecuted','numerical_component_or_transport_executed'):assert host[key] is False
assert out['numeric_component_stage_count_increment']==0 and out['numerical_controls_compiler_or_API_invoked'] is False
assert raw['component_native_AAA_ABA_credit'] is False and raw['original86_stage_count_increment']==0

names=['independent_SHA_empty_boundaries_multiblock_tail','forced_positive_short_reads','invalid_stream_counts_and_premature_EOF','same_literal_declared_owner_and_inventory','identical_SHA_distinct_files_and_hardlink_literals','allowed_relative_links_multihop_and_symlink_dotdot','original_relative_path_in_explicit_context','same_literal_conflicting_expected_SHA','missing_file_and_badalias_files_first_order','whole_original_namespace_unexpected_member','same_SHA_alias_retarget_before_duplicate','late_unhashed_native_alias_retarget','during_stream_truncate','during_stream_replace','during_stream_rewrite','late_identity_change_at_context_exit','success_and_exception_scope_reset','nested_scope_rejected_parent_stays_valid','wrong_thread_access_rejected','default_outside_context_fresh','preserved_namespace_link_word_change']
assert [g['name'] for g in out['groups']]==names
expectedfiles={'result.json','raw_preservation_manifest.json'}
expecteddirs=set(names);expectedlinks={}
def entries(name,files=(),dirs=(),links=None):
    expectedfiles.add(name+'/case_result.json')
    expectedfiles.update(name+'/'+x for x in files);expecteddirs.update(name+'/'+x for x in dirs)
    for k,v in (links or {}).items():expectedlinks[name+'/'+k]=v
entries(names[0],['input_'+str(i)+'.bin' for i in range(6)])
entries(names[1],['input.bin']);entries(names[2],[x+'.bin' for x in ['bool','none','negative','too_large','premature_zero']])
entries(names[3],['namespace/input.bin'],['namespace'])
entries(names[4],['first.bin','second.bin','hardlink.bin'])
entries(names[5],['other/input.bin'],['other','other/nested'],{'one.link':'other/input.bin','two.link':'one.link','dir.link':'other/nested'})
entries(names[6],['input.bin'],links={'relative.link':'input.bin'})
entries(names[7],['input.bin']);entries(names[8])
entries(names[9],['namespace/input.bin','namespace/extra.bin'],['namespace'])
entries(names[10],['first.bin','second.bin'],links={'alias.link':'second.bin'})
entries(names[11],['first.bin','second.bin'],links={'unhashed_native.link':'second.bin'})
for n in names[12:20]:entries(n,['input.bin'])
entries(names[20],['namespace/input.bin'],['namespace'],{'namespace/link':'missing.bin'})
actual=ns_before[str(C)]
assert {k for k,r in actual.items() if r['kind']=='file'}==expectedfiles
assert {k for k,r in actual.items() if r['kind']=='dir'}==expecteddirs
assert {k:r['readlink'] for k,r in actual.items() if r['kind']=='link'}==expectedlinks
assert set(raw['files'])==expectedfiles-{'raw_preservation_manifest.json'}
for rel,wanted in raw['files'].items():pin(C/rel,wanted)
assert set(ns_before[str(H)])=={'runtime','run','HELPER_ONLY_CONTROLS','runtime/run_bounded_dragon.py','run/controls.log','run/controls.watchdog.json','HELPER_ONLY_CONTROLS/stages.json','result.json'}
for rel,item in ns_before[str(S)].items():
    if item['kind']=='file':pin(S/rel)
assert all(x['kind']!='link' for x in ns_before[str(S)].values())

def oracle(size,marker=0,patch=None):
    h=hashlib.sha256();chunk=bytes((i*73+marker)%256 for i in range(65536));offset=0
    while offset<size:
        b=chunk[:min(size-offset,len(chunk))]
        if patch is not None:
            pos,word=patch;lo=max(offset,pos);hi=min(offset+len(b),pos+len(word))
            if lo<hi:b=b[:lo-offset]+word[lo-pos:hi-pos]+b[hi-offset:]
        h.update(b);offset+=len(b)
    return h.hexdigest()
G={g['name']:g for g in out['groups']}
for g in out['groups']:
    assert g['status']=='PASS_HELPER_PROTOCOL_ONLY'
    exact(read(C/g['name']/'case_result.json'),g)
    for e in g['actual_new_helper_open_stream_events']:
        for k in ('readinto_calls','positive_reads','bytecount','opened_fd_size'):assert type(e[k]) is int and e[k]>=0
        assert type(e['EOF_observed']) is bool and len(e['fd_identity_before'])==7
        assert e['readinto_calls']>=e['positive_reads']
sizes=[0,1,4194303,4194304,4194305,8388625]
for i,(r,e,size) in enumerate(zip(G[names[0]]['result'],G[names[0]]['actual_new_helper_open_stream_events'],sizes)):
    assert r['size']==e['bytecount']==e['opened_fd_size']==size
    assert r['oracle_sha256']==r['actual_sha256']==oracle(size,i)==sha(C/names[0]/('input_'+str(i)+'.bin'))
    assert e['EOF_observed'] and e['positive_reads']==math.ceil(size/4194304) and e['readinto_calls']==e['positive_reads']+1
q=G[names[1]];e=q['actual_new_helper_open_stream_events'][0]
assert q['result']['oracle_sha256']==oracle(10003)==sha(C/names[1]/'input.bin')
assert e['positive_reads']==1429 and e['readinto_calls']==1430 and e['bytecount']==10003 and e['EOF_observed']
bad=G[names[2]];assert [r['token'] for r in bad['result']]==['bool','none','negative','too_large','premature_zero']
for i,(r,e) in enumerate(zip(bad['result'],bad['actual_new_helper_open_stream_events'])):
    assert r['rejection']['type']=='ValueError'
    assert r['rejection']['message']==('full-content readinto returned an invalid byte count' if i<4 else 'complete EOF byte count or descriptor/path/alias identities drifted')
    assert e['bytecount']==(0 if i<4 else 7) and not e['EOF_observed']
assert G[names[3]]['result']=={'actual_full_reads':1,'expected_SHA_owner_checks':2,'original_complete_environment_predicates':True}
assert len(G[names[3]]['actual_new_helper_open_stream_events'])==1
assert G[names[4]]['result']['oracle_sha256']==oracle(1025)
x=identity(C/names[4]/'first.bin');y=identity(C/names[4]/'hardlink.bin');z=identity(C/names[4]/'second.bin')
assert x[0:2]==y[0:2] and x[3]==y[3]==2 and x[1]!=z[1] and z[3]==1
assert len(G[names[4]]['actual_new_helper_open_stream_events'])==3
assert G[names[5]]['result']['oracle_sha256']==oracle(1225) and len(G[names[5]]['actual_new_helper_open_stream_events'])==4
for literal in G[names[5]]['result']['literal_paths']:assert sha(literal)==oracle(1225)
assert G[names[6]]['result']['oracle_sha256']==oracle(1441)
assert len(G[names[6]]['actual_new_helper_open_stream_events'])==1 and G[names[6]]['actual_new_helper_open_stream_events'][0]['literal']=='relative.link'
rejections={7:'missing or changed declared file:',8:'missing or changed declared file:',9:'preserved predecessor namespace or hash changed:',10:'same-call literal identity drift forbids digest reuse',11:'complete declared native alias changed before environment exit',12:'complete EOF byte count or descriptor/path/alias identities drifted',13:'complete EOF byte count or descriptor/path/alias identities drifted',14:'complete EOF byte count or descriptor/path/alias identities drifted',15:'complete hashed input identity changed before environment exit',17:'nested or concurrent environment digest scopes are forbidden',18:'one unchanged-thread/cwd environment digest scope required',20:'preserved predecessor namespace or hash changed:'}
for i,message in rejections.items():
    r=G[names[i]]['result'];r=r.get('rejection',r)
    assert r['type']=='ValueError' and message in r['message']
assert len(G[names[7]]['actual_new_helper_open_stream_events'])==1
assert not G[names[8]]['actual_new_helper_open_stream_events']
assert not G[names[11]]['actual_new_helper_open_stream_events'] and G[names[11]]['result']['alias_had_no_digest_owner'] is True
assert sha(C/names[12]/'input.bin')==oracle(3)
assert sha(C/names[13]/'input.bin')==oracle(10003,1)
assert sha(C/names[14]/'input.bin')==oracle(10003,patch=(500,b'changed'))
exact(G[names[16]]['result'],{'fresh_scope_full_reads':4,'original_exception_preserved':True,'private_retained_buffer_and_memo_empty':True})
assert len(G[names[16]]['actual_new_helper_open_stream_events'])==4
assert not G[names[18]]['actual_new_helper_open_stream_events']
assert G[names[19]]['result']['oracle_before']==oracle(257)
assert G[names[19]]['result']['oracle_after']==oracle(257,patch=(0,b'changed'))==sha(C/names[19]/'input.bin')
assert G[names[19]]['result']['default_no_context_fresh'] is True
assert not G[names[19]]['actual_new_helper_open_stream_events']
assert not (C/names[8]/'absent.bin').exists() and not (C/names[8]/'also_missing.link').exists()
assert (C/names[20]/'namespace/link').is_symlink() and not (C/names[20]/'namespace/link').exists()

# Authenticate original live-own-PID guard proof and genuine direct parent MRO.
full=Path(host['input_sources'][3]['path']);fulltext=full.read_text();fullast=ast.parse(fulltext)
cls=next(n for n in fullast.body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
assert [ast.unparse(b) for b in cls.bases]==['SerialExecutor']
oldtext=parent.read_text();oldast=ast.parse(oldtext)
guard=next(n for n in oldast.body if isinstance(n,ast.FunctionDef) and n.name=='guard_admission')
guardtext=ast.get_source_segment(oldtext,guard)
assert 'class_text(FULL_SOURCE) != class_text(tested)' in guardtext
guardfolder=A/'axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard'
guarddata=read(guardfolder/'guard_controls.json','ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454')
tested=guardfolder/'tested_driver_source.py';pin(tested,guarddata['source_sha256'])
testedtext=tested.read_text();testedcls=next(n for n in ast.parse(testedtext).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
assert ast.get_source_segment(fulltext,cls)==ast.get_source_segment(testedtext,testedcls)
for rel,wanted in guarddata['control_files'].items():pin(guardfolder/rel,wanted)
assert guarddata['positive_child_completed'] is True and guarddata['actual_oversize_child_rejected'] is True
assert guarddata['terminated_own_child_not_live'] is True and guarddata['rss_cap_mib']==512
resourceparents=[(V/'prepare_qualified_AB_rank1_cache_production.py','92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'),(V/'prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')]
for p,w in resourceparents:pin(p,w)
for snap in [host['resources_before'],stage['resource_before'],stage['resource_after'],host['resources_after']]:
    assert snap['min_free_bytes']==8*2**30 and snap['artifact_budget_bytes']==96*2**30
    assert snap['artifact_bytes']<96*2**30 and snap['disk_free_bytes']>=8*2**30
    assert snap['declared_resource_roots']==snap['resource_roots']==host['resource_roots']
    assert snap['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
    for key in ('case_spec','resource_addendum'):
        r=snap['resource_scope_contract'][key];pin(r['path'],r['sha256'])
assert host['resources_before']['artifact_bytes']+64*2**20<96*2**30
assert host['resources_before']['disk_free_bytes']-64*2**20>=8*2**30
roots=sorted({str(p) for p in A.glob('axial-material-*')}|{str(H),str(C)})
assert set(host['resource_roots']).issubset(roots) and len(host['resource_roots'])==270
resource_meta={};n=total=0
for literal in roots:
    r=Path(literal);assert r.parent==A and not r.is_symlink()
    if not r.exists():continue
    for directory,dirs,files in os.walk(r,followlinks=False):
        for name in dirs+files:
            p=Path(directory)/name;i=identity(p);resource_meta[str(p)]=i
            if stat.S_ISREG(i[2]):total+=i[4];n+=1
assert total<96*2**30 and os.statvfs(A).f_bavail*os.statvfs(A).f_frsize>=8*2**30
assert roots==sorted({str(p) for p in A.glob('axial-material-*')}|{str(H),str(C)})
resource_meta_after={}
for literal in roots:
    r=Path(literal)
    if not r.exists():continue
    for directory,dirs,files in os.walk(r,followlinks=False):
        for name in dirs+files:resource_meta_after[str(Path(directory)/name)]=identity(Path(directory)/name)
assert resource_meta_after==resource_meta
# A separate actual whole old->new environment read, not a second helper run.
hr=read(S/'actual_historical_environment_read_receipts/Root_actual_historical_environment_read_tool_terminal_return.json','3f4ca6d6a6e6e4a657dddc73c09e916dba0fa5e765bca424df242d6e04141fad')
assert hr['action']=='historical-environment' and hr['session_closed'] is True
assert hr['initial_session_id']==46623 and hr['call_history'][0]['chunk_id']=='3b9149'
assert hr['terminal_result']['chunk_id']=='667c7b' and type(hr['terminal_result']['exit_code']) is int and hr['terminal_result']['exit_code']==0
exact(hr['call_history'][-1],hr['terminal_result'])
for key in ('stdout','stderr'):pin(hr[key]['path'],hr[key]['sha256']);assert identity(hr[key]['path'])[4]==hr[key]['size_bytes']
assert hr['stderr']['size_bytes']==0
hh=read(HH/'result.json','2e70836c4dd7ead9b8b9979591c0241884fb82081076e680b6752be834f7f18f')
hc=read(HC/'result.json','5a1a82598476a1bd7df63e0c09eedf2ff6e2b89211cc12d4f6d16f37872a17a5')
hm=read(HC/'raw_preservation_manifest.json');assert hm['files']=={'result.json':sha(HC/'result.json')}
assert hm['component_native_AAA_ABA_credit'] is False and hm['original86_stage_count_increment']==0
hw=read(HH/'run/controls.watchdog.json');exact(hw,hh['watchdog'])
hcmd=expectedcmd.copy();hcmd[-3]='historical-environment';hcmd[-1]=str(HC)
exact(hw['command'],hcmd);exact(hh['actual_command'],hcmd)
assert type(hw['returncode']) is int and hw['returncode']==0
assert hw['own_child_only'] is True and hw['liveness_group_cleanup'] is True and hw['limit_failure'] is None
assert hw['rss_cap_mib']==512 and hw['sampled_peak_rss_mib']==135.28125
assert 0<hw['elapsed_seconds']<hw['wall_cap_seconds']<=120
hj=read(HH/'HELPER_ONLY_CONTROLS/stages.json');exact(hj['stages'],hh['stage_records']);assert len(hj['stages'])==1
hs=hj['stages'][0];assert hs['status']=='PASS' and hs['label']=='run/controls' and hs['log_sha256']==sha(HH/'run/controls.log')
exact(hs['command'],hcmd)
hlt=read(HH/'run/controls.log');assert hlt['status']==hc['status']=='BOTH_COMPLETE_ENVIRONMENT_PREDICATES_RETURNED'
assert hlt['result_sha256']==sha(HC/'result.json') and hlt['action']=='historical-environment'
hst=read(hr['stdout']['path']);assert hst['status']==hh['status']=='PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST'
for x in (hst['host_result'],hh['actual_full_merged_stdout_stderr'],hh['actual_child_result'],hh['actual_watchdog'],hh['original_helper'],hh['resource_factory'],hc['source'],hc['original619_source'],hc['declaration'],*hh['input_sources']):pin(x['path'],x['sha256'],x['identity'])
pin(HH/'runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
assert set(ns_before[str(HC)])=={'result.json','raw_preservation_manifest.json'}
assert set(ns_before[str(HH)])==set(ns_before[str(H)])
for k,v in {'whole_wall_cap_seconds':120,'rss_cap_mib':512,'archive_cap_bytes':64*2**20,'threads':1,'children_at_once':1,'retries':0}.items():exact(hh[k],v)
assert 0<hh['whole_elapsed_seconds']<120 and hh['whole_archive_bytes']<64*2**20
assert 0<hc['elapsed_seconds']<hw['elapsed_seconds'] and hc['numerical_controls_compiler_or_API_invoked'] is False
for key in ('supervisor_class_or_MRO_modified','failed_V13_audit_reexecuted','numerical_component_or_transport_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert hh[key] is False
for key in ('old_helper_globals_unmodified','helper_only_observer_overhead_not_removed','not_V13_failed_audit_reexecution','not_component_or_native_or_AAA_qualification','new_all_streams_EOF_and_total_size_equal'):assert hc[key] is True
for snap in [hh['resources_before'],hs['resource_before'],hs['resource_after'],hh['resources_after']]:
    assert snap['min_free_bytes']==8*2**30 and snap['artifact_budget_bytes']==96*2**30
    assert snap['artifact_bytes']<96*2**30 and snap['disk_free_bytes']>=8*2**30
    assert snap['declared_resource_roots']==snap['resource_roots']==hh['resource_roots']==roots
declaration=read(hc['declaration']['path'],hc['declaration']['sha256'])
fields=['files','preserved_predecessors','build_python_executable','native_library_aliases','numerical_loader_environment']
assert hc['exact_environment_input_fields']==fields and hc['original_preserved_namespace_count']==len(declaration['preserved_predecessors'])==8
expectedcounter=Counter(list(declaration['files']))
for pred in declaration['preserved_predecessors']:
    expectedcounter.update(str(Path(pred['root'])/rel) for rel in pred['inventory']['files'])
old_events=hc['old_actual_FD_full_EOF_stream_observations'];new_events=hc['new_actual_FD_full_EOF_stream_observations']
assert len(old_events)==25213 and len(new_events)==13588
oldpaths=[x['path'] for x in old_events];assert Counter(oldpaths)==expectedcounter
assert [x['literal'] for x in new_events]==list(dict.fromkeys(oldpaths))
historyids={}
for e in old_events:
    for k in ('initial_tell','final_tell','actual_complete_bytes','opened_fd_size','readinto_calls'):assert type(e[k]) is int and e[k]>=0
    assert e['initial_tell']==0 and e['final_tell']==e['actual_complete_bytes']==e['opened_fd_size']
    assert e['readinto_calls']>=1
for e in new_events:
    i=identity(e['literal']);assert i==e['fd_identity_before'];historyids[e['literal']]=i
    assert e['EOF_observed'] is True and e['bytecount']==e['opened_fd_size']
    assert e['readinto_calls']==e['positive_reads']+1
    assert e['positive_reads']==math.ceil(e['opened_fd_size']/4194304)
    assert Path(e['literal']).stat().st_size==e['opened_fd_size']
assert sum(x['actual_complete_bytes'] for x in old_events)==hc['old_actual_full_byte_volume']==28562424798
assert sum(x['bytecount'] for x in new_events)==hc['new_actual_full_byte_volume']==27794515455
for p,i in historyids.items():assert identity(p)==i
assert hc['old_elapsed_seconds_including_profile']==15.705013833998237
assert hc['new_elapsed_seconds_including_open_probe']==15.68816187500488
history_summary={'actual_Root_terminal_chunk':'667c7b','actual_Root_exit_code':0,'session_closed':True,'old_streams':len(old_events),'new_streams':len(new_events),'old_full_bytes':hc['old_actual_full_byte_volume'],'new_full_bytes':hc['new_actual_full_byte_volume'],'removed_duplicate_full_bytes':767909343,'whole_environment_fields_and_all_expected_literal_occurrences':True,'new_unique_literal_order_matches_old_first_occurrences':True,'full_EOF_size_and_current_7identity_before_after':True,'identity_set_fingerprint':hashlib.sha256(json.dumps(historyids,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'old_seconds_with_profile':hc['old_elapsed_seconds_including_profile'],'new_seconds_with_probe':hc['new_elapsed_seconds_including_open_probe'],'watch_sample_peak_mib':hw['sampled_peak_rss_mib'],'whole_host_seconds':hh['whole_elapsed_seconds'],'archive_at_host_tail_bytes':hh['whole_archive_bytes'],'elapsed_difference_seconds':hc['old_elapsed_seconds_including_profile']-hc['new_elapsed_seconds_including_open_probe'],'interpretation':'No material elapsed improvement demonstrated in this instrumented old->new run. This does not admit full86 or remedy the failed V13 final audit.'}
for row in list(pins.values()):assert identity(row['path'])==row['identity'] and sha(row['path'])==row['sha256']
assert {str(r):namespace(r) for r in (S,H,C,HH,HC)}==ns_before
currentarchive=sum(i['identity'][4] for r in (H,C) for i in ns_before[str(r)].values() if i['kind']=='file')
assert currentarchive==host['whole_archive_bytes']+identity(H/'result.json')[4]
evidence={'schema':'AXMAT_V14_ACTUAL_HELPER_ONLY_CONTROL_FULL_READONLY_EVIDENCE_V1','full_fresh_file_pins':list(pins.values()),'namespace_before_after':ns_before,'source_inverse':source_inverse,'complete_helper_inverse_to_619':True,'33_original_helper_functions_byteexact':True,'all_21_cases_independent_protocol_checks':names,'historical_environment_summary':history_summary,'resource_metadata_current':{'roots':roots,'regular_files':n,'logical_bytes':total,'metadata_entry_count':len(resource_meta),'stable_before_after':True,'metadata_fingerprint_sha256':hashlib.sha256(json.dumps(resource_meta,sort_keys=True,separators=(',',':')).encode()).hexdigest()},'actual_root':root,'actual_watchdog':watch,'actual_stage':stage,'oracle_method':'Independent hashlib on complete retained actual raw files plus deterministic byte generator; no helper function loaded or replayed.'}
(D/'EVIDENCE.json').write_text(json.dumps(evidence,indent=2,allow_nan=False)+'\n')
report={'schema':'AXMAT_V14_ACTUAL_HELPER_ONLY_CONTROL_INDEPENDENT_REVIEW_V1','status':'PASS_HELPER_PROTOCOL_ONLY','actual_root_exit_code':0,'actual_root_session_closed':True,'actual_root_terminal_chunk':'9c9d85','groups':21,'complete_source_inverse_and_bound_driver':True,'all_fixture_and_case_files_fresh_full_SHA':True,'complete_namespace_files_links_directories':True,'original_genuine_MRO_guard_and_dynamic_resources':True,'whole_elapsed_seconds':host['whole_elapsed_seconds'],'child_elapsed_seconds':watch['elapsed_seconds'],'driver_elapsed_seconds':out['elapsed_seconds'],'archive_at_host_tail_bytes':host['whole_archive_bytes'],'archive_current_after_host_result_bytes':currentarchive,'sampled_peak_rss_mib_as_recorded':0.0,'RSS_interpretation':'The original short-child watchdog recorded no positive RSS sample. 0.0 is not a measured process peak and supplies no RSS-reduction or native-512MiB success credit.','actual_positive_RSS_sample_observed':False,'historical_environment_action_executed_by_Root':True,'historical_environment_summary':history_summary,'historical_big_bytes_re_read_by_this_review':False,'full_86_component_admitted':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'helper_loaded_or_called_by_this_review':False,'fixtures_or_controls_rerun':False,'project_written':False,'Root_polled':False,'fresh_full_pin_count':len(pins),'scope_limit':'Authenticates actual control evidence and source guards; private buffer/lock cleanup results originate from the frozen executed control driver, rather than a second helper execution. Full86/native remain unqualified.','readonly_review_elapsed_seconds':time.monotonic()-started,'evidence':{'path':str(D/'EVIDENCE.json'),'sha256':sha(D/'EVIDENCE.json')}}
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('独立实际控制审查：PASS_HELPER_PROTOCOL_ONLY\n21项原始控制、完整SHA/EOF、别名/命名空间/拒绝顺序、清理记录、原监督器来源、120秒/512MiB/单子进程/零重试及全资源门均通过有限独审。\n实际整段11.091秒；原watch采样峰0.0没有捕获短进程正RSS样本，不能解释为真实RSS峰0，也不能授予86阶段组件/native/AAA/ABA资格。\n本审查只读现存证据，未导入helper、重跑控制或写项目。\n')
print(json.dumps({'status':report['status'],'REPORT_sha256':sha(D/'REPORT.json'),'EVIDENCE_sha256':sha(D/'EVIDENCE.json'),'full_pins':len(pins),'groups':21,'resource_roots':len(roots)},indent=2))

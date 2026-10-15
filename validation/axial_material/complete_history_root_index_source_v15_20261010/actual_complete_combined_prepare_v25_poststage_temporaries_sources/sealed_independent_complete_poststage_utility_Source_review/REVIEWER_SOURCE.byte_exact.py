"""Independent finite complete V25 utility Source review; no candidate execution."""
import ast,difflib,hashlib,json,os,stat,sys,tempfile
from pathlib import Path
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
PREP=Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')
BOUNDPEER=Path('/private/tmp/axmat_V25_actual_poststage_PREP_bound_Source_independent_l0vys9jh')
F=Path(tempfile.mkdtemp(prefix='axmat_INDEPENDENT_V25_poststage_finite_utilities_V3_Source_',dir='/private/tmp'))
checks=[];errors=[];inputs={};inverse_details={};owners={};definitions={};roles={}
def ck(name,value):
    if any(c['check']==name for c in checks):raise ValueError('duplicate independent check')
    ok=type(value) is bool and value is True;checks.append(dict(check=name,passed=ok))
    if not ok:raise ValueError(name)
def ident(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p)
    if not(p.is_absolute() and not any(x.is_symlink() for x in(p,*p.parents)) and stat.S_ISREG(a[2]) and a[3]==1):raise ValueError('ordinary Source/META required '+str(p))
    with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=a:raise ValueError('Source EOF identity changed '+str(p))
    q=dict(path=str(p),sha256=d,size_bytes=a[4],identity=a)
    if str(p) in inputs and inputs[str(p)]!=q:raise ValueError('same Source input changed')
    inputs[str(p)]=q;return q
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate Source/META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def load(p):
    q=pin(p);v=strict(Path(p).read_bytes())
    if pin(p)!=q:raise ValueError('parse changed Source')
    return v
def view(root):
    root=Path(root);ds={'.':ident(root)};fs={}
    if root.is_symlink() or not root.is_dir():raise ValueError('ordinary Source root')
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));i=ident(p)
        if stat.S_ISDIR(i[2]):ds[rel]=i
        elif stat.S_ISREG(i[2]):fs[rel]=pin(p)
        else:raise ValueError('nonordinary Source namespace')
    if ident(root)!=ds['.']:raise ValueError('Source root changed')
    return dict(root=str(root),files=fs,directories=ds,symlinks={})
def package(mp,sha):
    mp=Path(mp);m=load(mp);v=view(mp.parent)
    if pin(mp)['sha256']!=sha or m['source_only'] is not True:raise ValueError('actual full Source manifest')
    members=m['members']
    if type(members) is list:members={r['relative_path']:r.get('fullpin',r) for r in members}
    if type(members) is not dict or len(members)!=m['member_count'] or set(v['files'])!=set(members)|{'MANIFEST.json'} or v['directories']!=m['directories']:raise ValueError('whole package exact member/directory view')
    if any(v['files'][rel]!={k:q[k] for k in('path','sha256','size_bytes','identity')} for rel,q in members.items()):raise ValueError('full Source manifest byte/7ID mismatch')
    return m,v
def defs(raw):
    s=raw.decode();t=ast.parse(s);nodes=sorted((n for n in ast.walk(t) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))),key=lambda n:(n.lineno,n.col_offset))
    return [(type(n).__name__,n.name,ast.dump(n,include_attributes=False),ast.get_source_segment(s,n)) for n in nodes]
def literal(n):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='dict' and not n.args:return {k.arg:literal(k.value) for k in n.keywords}
    if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Mult,ast.Pow)):
        a,b=literal(n.left),literal(n.right)
        if type(a) is not int or type(b) is not int or a<0 or b<0 or a>2**40 or b>(40 if isinstance(n.op,ast.Pow) else 2**40):raise ValueError('bounded Source literal')
        return a*b if isinstance(n.op,ast.Mult) else a**b
    return ast.literal_eval(n)
def constants(raw):
    c={}
    for n in ast.parse(raw).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:c[n.targets[0].id]=literal(n.value)
            except(ValueError,TypeError):pass
    return c
def receipt(path,chunk):
    w=load(path);t=w.get('terminal_tool_return',w.get('actual_tool_return',w.get('exec_command_result')))
    if not(w['closed'] is True and w['observed_terminal'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and t['chunk_id']==chunk and w.get('session_repolled_after_close',False) is False):raise ValueError('genuine closed strict0 terminal '+chunk)
    return w,strict(t['output'])
def copy(p,rel):
    p=Path(p);q=pin(p);dst=F/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    with p.open('rb') as src,dst.open('xb') as out:
        while True:
            block=src.read(2**20)
            if not block:break
            out.write(block)
    d=pin(dst)
    if pin(p)!=q or(d['sha256'],d['size_bytes'])!=(q['sha256'],q['size_bytes']):raise ValueError('lossless finite Source copy')
try:
    before=view(U);m,uv=package(U/'MANIFEST.json','4aafddfd6b13372dba48823c9e5a9ca7ee2f1ccfe28875acf0e7c48dfa5aabe2')
    ck('whole24files2dirs utility original Source manifest fullEOF7ID exact',uv==before and len(uv['files'])==24 and len(uv['directories'])==2 and m['member_count']==23)
    raws={str(p.relative_to(U)):p.read_bytes() for p in U.rglob('*.py')}
    for rel,raw in raws.items():ast.parse(raw);definitions[rel]=[dict(kind=x[0],name=x[1]) for x in defs(raw)]
    ck('all17 complete Python Source AST every definition occurrence inspected',len(raws)==17 and len(definitions)==17)
    c=load(U/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json');inv=load(U/'COMPLETE_SIX_INTERFACE_SOURCE_BYTE_AST_INVERSES.json');ar=load(U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json');integration=load(U/'FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json')
    names=('Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_complete_PREP_E_snapshot.py','Root_prepare_poststage_REQUEST.Source_META_only.py','Root_source_installer.py','Root_prelaunch_checker.py','Root_poststage_Source_META_contract.py')
    roles={name:pin(U/name) for name in names}
    ck('seven exact actual utility role full4pins match manifest author and integration',set(m['role_Source_names'])==set(names) and roles==ar['role_Source_pins']==integration['qualified_role_Source_pins'])
    allinverse=True;allnonmain=True;hunkcount=0
    for role,r in inv['roles'].items():
        old=Path(r['complete_original_Source_copy']['path']).read_bytes();new=Path(r['derived_Source']['path']).read_bytes();lines=new.decode().splitlines(keepends=True)
        if pin(r['complete_original_Source_copy']['path'])!=r['complete_original_Source_copy'] or pin(r['derived_Source']['path'])!=r['derived_Source'] or pin(r['original_Source']['path'])!=r['original_Source'] or Path(r['original_Source']['path']).read_bytes()!=old:raise ValueError('actual original finite interface Source pin')
        for h in reversed(r['finite_hunks']):
            if ''.join(lines[h['derived_start']:h['derived_end']])!=h['derived_text']:raise ValueError('entire precise finite inverse hunk')
            lines[h['derived_start']:h['derived_end']]=h['original_text'].splitlines(keepends=True);hunkcount+=1
        restored=''.join(lines).encode();allinverse&=restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
        a=defs(old);b=defs(new);exceptions={'full_PREP','check_PREP','main'}
        allnonmain&=[d for d in a if d[1] not in exceptions]==[d for d in b if d[1] not in exceptions]
        if role=='build_installer':
            original=next(d[3] for d in a if d[1]=='full_PREP');derived=next(d[3] for d in b if d[1]=='full_PREP')
            allnonmain&=original.replace("assert len(ph['input_sources'])==142","scope.prepare_input_scope(ph,summary)").replace("assert len(inputs)==144 and summary['all_original_pinned_inputs_unchanged_count']==144","assert len(inputs)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(inputs)")==derived
        if role=='build_prelaunch':
            original=next(d[3] for d in a if d[1]=='check_PREP');derived=next(d[3] for d in b if d[1]=='check_PREP')
            allnonmain&=original.replace("assert len(ph['input_sources'])==142 and len(prep)==144 and summary['all_original_pinned_inputs_unchanged_count']==144","scope.prepare_input_scope(ph,summary)\n    assert len(prep)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(prep)")==derived
        inverse_details[role]=dict(original=r['original_Source'],complete_original_copy=r['complete_original_Source_copy'],derived=r['derived_Source'],hunks=len(r['finite_hunks']),original_complete_definition_occurrences=[dict(kind=d[0],name=d[1]) for d in a],derived_complete_definition_occurrences=[dict(kind=d[0],name=d[1]) for d in b])
    ck('all six complete interface Source fullbyte AST inverses and40 exact hunks',len(inv['roles'])==6 and hunkcount==40 and allinverse)
    ck('all complete nonmain definitions byte AST preserved with only exact full_PREP check_PREP dynamic count contract',allnonmain)
    for phase,o in c['complete_old_frozen_Source_owners'].items():
        f=load(o['freeze']['path']);v=view(o['root']);dirs=f['complete_directories']
        if phase=='PREP':dirs={'.':f['source_root_identity'],**dirs}
        if pin(o['freeze']['path'])!=o['freeze'] or v['files']!=f['complete_files'] or v['files']!=o['complete_files'] or v['directories']!=dirs or v['directories']!=o['complete_directories'] or len(v['files'])!=o['original_file_count'] or len(v['directories'])!=o['original_directory_count_including_root']:raise ValueError('all complete old frozen Source owner identity preserved')
        owners[phase]=v
    ck('all463 actual old Source owners fullEOF4pins no dropped path full frozen directory identity',len(owners['PREP']['files'])==135 and len(owners['BUILD']['files'])==328 and len(owners['PREP']['directories'])==12 and len(owners['BUILD']['directories'])==38 and c['all_original_physical_Source_owners_retained_without_reduction'] is True)
    ck('all463 old owner records strict fullfourkeys exact7int size path rooted',all(set(q)=={'path','sha256','size_bytes','identity'} and type(q['size_bytes']) is int and all(type(i) is int for i in q['identity']) and len(q['identity'])==7 and Path(q['path'])==Path(v['root'])/rel for v in owners.values() for rel,q in v['files'].items()))
    oldhost=load(c['original_closed_PREP_host_META_pin']['path']);oldcanonical=pin(c['original_canonical_Source_pin']['path'])
    ck('original closed PREP sevenprefix 142inputs plus2 exact old144 retained as provenance',pin(c['original_closed_PREP_host_META_pin']['path'])==c['original_closed_PREP_host_META_pin'] and oldcanonical==c['original_canonical_Source_pin'] and len(oldhost['input_sources'])==142 and len(oldhost['input_sources']+[oldhost['original_helper'],oldhost['resource_factory']])==144 and [{k:q[k]for k in('path','sha256','identity')}for q in c['original_host_prefix_seven_input_pins']]==oldhost['input_sources'][:7])
    for q in c['original_host_prefix_seven_input_pins']:
        observed=pin(q['path'])
        if {k:observed[k] for k in q}!=q or set(q)!={'path','sha256','identity'}:raise ValueError('actual original ordered prefix Source/META pin')
    bm,bv=package(PREP/'MANIFEST.json','531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef')
    bw,bo=receipt(c['actual_new_PREP_Source_binding_terminal']['path'],'91304c')
    boundroles=dict(canonical=pin(PREP/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'),prepare_host=pin(PREP/'combined_prepare_host.py'),prepare_writer=pin(PREP/'write_actual_prepare_terminal.py'))
    ck('actual91304c strict0 binding full sixfile PREP Source manifest and all three actual role fullpins',len(bv['files'])==6 and pin(PREP/'MANIFEST.json')==c['actual_new_PREP_bound_Source_manifest']==bo['manifest'] and pin(c['actual_new_PREP_Source_binding_terminal']['path'])==c['actual_new_PREP_Source_binding_terminal'] and bo['canonical']==boundroles['canonical'] and bo['host']==boundroles['prepare_host'] and bo['writer']==boundroles['prepare_writer'] and bo['business_or_science_executed'] is False)
    pm,pv=package(BOUNDPEER/'MANIFEST.json','00c3c8c6341164f646e14fca5086baa41997f44d4ef96a5843604b252d78fa2d');pr=load(BOUNDPEER/'REVIEW.json');ps,po=receipt(Path(str(BOUNDPEER)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','abe78c')
    ck('actual24check boundPREP peer exact real schema fields and genuine seal coupling',pr['schema']=='INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1' and pr['status']=='PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED' and pr['source_only'] is True and pr['all_checks_typed_true'] is True and pr['check_count']==24 and len(pr['checks'])==24 and all(type(x['passed']) is bool and x['passed'] is True for x in pr['checks']) and pr['blockers']==[] and pr['actual_complete_bound_Source_manifest_pin']==pin(PREP/'MANIFEST.json') and pr['actual_ready_role_Source_pins']==boundroles and po['manifest_pin']==pin(BOUNDPEER/'MANIFEST.json') and po['review_pin']==pin(BOUNDPEER/'REVIEW.json'))
    am,av=package(c['author_manifest']['path'],c['author_manifest']['sha256']);apm,apv=package(c['author_peer_manifest']['path'],c['author_peer_manifest']['sha256']);apr=load(Path(c['author_peer_manifest']['path']).parent/'REVIEW.json')
    ck('complete seven-role physical parent Source author and658 peer actual fullEOF qualification unchanged',pin(c['author_manifest']['path'])==c['author_manifest'] and pin(c['author_peer_manifest']['path'])==c['author_peer_manifest'] and apr['schema']=='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1' and apr['status']=='PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION' and apr['check_count']==658 and apr['all_checks_typed_true'] is True and apr['blockers']==[] and apr['qualified_complete_Source_manifest_pin']==c['author_manifest'] and apr['qualified_role_Source_pins']==c['seven_author_role_Source_pins'])
    for role,q in c['seven_author_role_Source_pins'].items():
        if pin(q['path'])!=q:raise ValueError('complete actual seven-parent Source pin')
        ast.parse(Path(q['path']).read_bytes())
    ck('all seven author role Source complete AST fullEOF pins matched actual658peer',True)
    core=raws['Root_poststage_Source_META_contract.py'].decode();source_install=raws['Root_complete_SOURCE_install_writer.py'].decode();prep_launch=raws['Root_complete_PREP_prelaunch.py'].decode();build_install=raws['Root_source_installer.py'].decode();build_launch=raws['Root_prelaunch_checker.py'].decode();snapshot=raws['Root_complete_PREP_E_snapshot.py'].decode();cc=constants(raws['Root_poststage_Source_META_contract.py'])
    caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HSOTDE_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children=1,retries=0)
    ck('all9 original exactint caps no guard budget increase or retry change',cc['CAPS']==caps and all(type(v) is int for v in cc['CAPS'].values()) and 'resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)' in prep_launch and 'resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)' in build_launch and 'rss_mib_cap=512' in build_launch and 'rss_mib=512' in prep_launch)
    unknown=('future_actual_Source_utility_peer','future_bound_PREP_Source_peer','future_saved_new_PREP_META_peer','future_actual_bound_BUILD_Source_manifest','future_actual_BUILD_Source_binding_terminal','future_bound_BUILD_Source_peer','actual_new_PREP_business_pins','actual_new_BUILD_business_pins')
    ck('all futurebusiness Source peer BUILD and savedPREP pins unknown no fabricated observed success',all(c[k] is None for k in unknown) and all(q is None for q in cc['NEW_BUSINESS_PINS'].values()) and c['whole_INPUT_native_or_science_qualified'] is False and c['Source_install_or_prelaunch_executed'] is False)
    ck('strict utility peer report7 actual roles exact owner manifest and true toolseal consumption','INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1' in core and 'PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION' in core and "r['qualified_complete_utility_manifest_pin']==up" in core and "r['qualified_role_Source_pins']==expected" in core and "observed['manifest_pin']==mpin and observed['review_pin']==rp" in core)
    ck('real boundPREP schema status fields compatible all three roles and root913 manifest fixed','INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1' in core and 'PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED' in core and "r['actual_complete_bound_Source_manifest_pin']==bp and r['actual_ready_role_Source_pins']==roles" in core and "tr['chunk_id']=='91304c'" in core and cc['PREP_BOUND_SHA']=='531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef')
    ck('request complete closed actual Source owner facts no None-filter and newBUILD realPREP facts mandatory',"author=author_facts();utility=utility_facts(Path(__file__).parent,a);bound=bound_facts(a.phase,a);parent=parent_facts(a.phase)" in core and "facts=prep_facts(a) if a.phase=='BUILD' else None" in core and "all(getattr(a,k.replace('-','_')) is None for k in business) if a.phase=='PREP' else all(getattr(a,k.replace('-','_')) is not None for k in business)" in core and "assert d['author']==author_facts()" in core and "assert f==prep_facts(a)" in core)
    ck('Source-only contract stdlib imports and no project import business API subprocess calls',all((isinstance(n,ast.Import) and all(a.name in ('argparse','ast','hashlib','json','os','stat','sys') for a in n.names)) or (isinstance(n,ast.ImportFrom) and n.module=='pathlib') for n in ast.parse(raws['Root_poststage_Source_META_contract.py']).body if isinstance(n,(ast.Import,ast.ImportFrom))) and all(x not in core for x in('subprocess.','spec_from_file_location','exec_module','guard_admission(','run-build','importlib.')))
    ck('PREP installation fresh namespace whole seven views copied allutilityroles Sourcefreeze fullnoappend',"for prefix,v in source_views:" in source_install and source_install.count("('original_closed_monitor_access_complete_PREP_Source',")==1 and len(ast.literal_eval(next(n.value for n in ast.parse(source_install).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='NAMES')))==4 and 'for role,q in request[\'utility\'][\'roles\'].items()' in source_install and "assert inventory(D)==frozen" in source_install and "all(not os.path.lexists(p) for p in (D,E,C,*(ART/n for n in NAMES)))" in source_install)
    ck('complete installed owner records verify whole original full view and every saved Source byte',"assert view(original['root'])==original" in core and "for rel,q in original['files'].items():" in core and "(saved['sha256'],saved['size_bytes'])==(q['sha256'],q['size_bytes'])" in core and "set(v['files'])==set(members)|{'MANIFEST.json'}" in core)
    ck('ordered PREP inputscope equals originalhost sevenprefix plus every full newD sorted and2 originals',"expected=expected_prefix+[host_pin(v['files'][k]) for k in sorted(v['files'])]" in core and "ph['input_sources']==expected" in core and 'total=len(expected)+2' in core and "summary['all_original_pinned_inputs_unchanged_count']==total" in core and "expected_host_inputs=exact_prefix+[scope.host_pin(frozen['complete_files'][k]) for k in sorted(frozen['complete_files'])]" in prep_launch and "[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]" in Path(boundroles['prepare_host']['path']).read_text())
    ck('original PREP prelaunch support guards helper resource genuine MRO and11 prerequisites unchanged','helper.guard_admission(full)' in prep_launch and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)' in prep_launch and "qt['chunk_id']=='94520a'" in prep_launch and "qp['check_count']==48" in prep_launch and "inputs.extend([qwriterpin,qpeerpin,qretentionpin])" in prep_launch and "assert pin(support_path)==support_pin" in prep_launch)
    ck('PREP E snapshot captures all actual files directories root at snapshot only freshTMP output','for folder,dnames,names in os.walk(E,followlinks=False):' in snapshot and 'second==ns and secondroot==rootid' in snapshot and 'E_root_is_not_claimed_unchanged_after_genuine_future_appends=True' in snapshot and "out.is_relative_to(Path('/private/tmp'))" in snapshot)
    ck('BUILD six complete copy owners whole newPREP Source keeps full author utility peer once',"copy_roles=[('original_closed_monitor_access_complete_BUILD_Source'" in build_install and "('complete_actual_poststage_PREP_Source',prep['complete_new_PREP_Source'])" in build_install and "('complete_actual_PREP_receipts_before_build',prep['current_complete_PREP_E'])" in build_install and "for prefix,v in copy_roles:copy_view(v,prefix)" in build_install and "assert snapshot(Path(v['root']))==v" in build_install and "no_SOURCE_append_after_freeze=True" in build_install)
    ck('BUILD fixed ordered inputs exact genuine host construction includes repeats allD S T and originals',"fixed=[original_host_pin(exact(q)) for q in ph['input_sources'][:7]]" in build_launch and "fixed+=[original_host_pin(pin(p)) for p in sorted(D.rglob('*')) if p.is_file()]" in build_launch and "for root in (S,T) for p in sorted(root.rglob('*')) if p.is_file()]" in build_launch and "original_host_pin(exact(ph['original_helper'])),original_host_pin(exact(ph['resource_factory']))" in build_launch and "for q in fixed:exact(q)" in build_launch and "inputs += [support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]" in Path(c['seven_author_role_Source_pins']['build_host']['path']).read_text())
    ck('BUILD completeRoot H S O T D E C pluscurrentPREP H D E caps outsideART history Eappend accounted',"extra_roots=[H,S,O,T,D,E,PREP_H,PREP_D,PRE]" in build_launch and 'before_bytes<2*2**30' in build_launch and 'outside_art_bytes+own_pin[\'size_bytes\']+2*2**30<96*2**30' in build_launch and "now['files']=={**v['files'],out.name:own_pin}" in build_launch and "now['directories']['.'][:3]==v['directories']['.'][:3]" in build_launch and "if k!='.':assert now['directories'][k]==i" in build_launch and "else:assert now==v" in build_launch)
    ck('bothprelaunch exact original environment Python five threads no optimization profile frozen self','OMP_NUM_THREADS' in prep_launch and 'NUMEXPR_NUM_THREADS' in prep_launch and 'not sys.flags.optimize' in prep_launch and 'sys.getprofile() is None' in prep_launch and 'not sys.flags.optimize' in build_launch and "support.THREAD_KEYS==THREAD_KEYS" in build_launch and "pin(Path(__file__))==freeze['complete_files']['Root_prelaunch_checker.py']" in build_launch and "pin(Path(__file__))==frozen['complete_files']['Root_complete_PREP_prelaunch.py']" in prep_launch)
    wt=load(U/'ACTUAL_AUTHOR_AND_SOURCE_CHECK_TOOL_RETURNS.json')
    for key,chunk,rpath in [('author','f2b2a4','AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json'),('source_integration_check','2e1935','FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json')]:
        t=wt[key]['actual_tool_return'];o=strict(t['output'])
        if type(t['exit_code']) is not int or t['exit_code']!=0 or 'session_id' in t or t['chunk_id']!=chunk or o.get('author_report',o.get('report'))!=pin(U/rpath):raise ValueError('genuine author tool coupling')
    sw,so=receipt(Path(str(U)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','77abc2');pw,po=receipt(Path(str(U)+'_seal_receipt')/'ACTUAL_SOURCE_POSTSEAL_TOOL_RETURN.json','1d9bb0')
    ck('actual author buildSourcecheck seal postseal four CLOSED0 full Source manifest coupling',so['manifest_pin']==po['manifest_pin']==pin(U/'MANIFEST.json') and so['review_pin']==po['review_pin']==pin(U/'FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json') and so['complete_files']==po['complete_files']==24 and so['complete_py_AST_count']==po['complete_py_AST_count']==17 and po['all_full_EOF_SHA7ID_unchanged'] is True and wt['closed'] is True and wt['observed_terminal'] is True)
    ck('whole original utility and boundPREP Source immutable after independent full checks',view(U)==before and view(PREP)==bv and view(BOUNDPEER)==pv and all(view(v['root'])==v for v in owners.values()))
    for rel in before['files']:copy(U/rel,'COMPLETE_REVIEWED_UTILITY_SOURCE/'+rel)
    for rel in bv['files']:copy(PREP/rel,'COMPLETE_ACTUAL_BOUND_PREP_SOURCE/'+rel)
    for n in ('MANIFEST.json','REVIEW.json'):copy(BOUNDPEER/n,'EXACT_ACTUAL_BOUND_PREP_PEER/'+n)
    copy(Path(str(BOUNDPEER)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','EXACT_ACTUAL_BOUND_PREP_PEER/ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')
    for n in ('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_SOURCE_POSTSEAL_TOOL_RETURN.json'):copy(Path(str(U)+'_seal_receipt')/n,'ACTUAL_AUTHOR_TOOL_TRUTH/'+n)
    for phase,o in c['complete_old_frozen_Source_owners'].items():copy(o['freeze']['path'],'FINITE_ORIGINAL_OWNER_FREEZES/'+phase+'_freeze.byte_exact.json')
    first=Path('/private/tmp/axmat_INDEPENDENT_V25_poststage_finite_utilities_V3_Source_s6vlhnhi')
    for n in ('REVIEW.json','REVIEWER_SOURCE.byte_exact.py','ACTUAL_OWN_PREFIX_SHAPE_CHECK_FAILURE_TOOL_RETURN.json'):copy(first/n,'OWN_ORIGINAL_HOST_THREE_KEY_PREFIX_CHECK_ERROR/'+n)
    copy(Path('/private/tmp/spot_V25_own_original_host_prefix_shape_review_finite_inverse_20261010.json'),'OWN_ORIGINAL_HOST_THREE_KEY_PREFIX_CHECK_ERROR/COMPLETE_OWN_REVIEWER_FIX_INVERSE.json')
    ck('finite full reviewed24utility6boundSource retained losslessly no physical payload or large history clone',len(list((F/'COMPLETE_REVIEWED_UTILITY_SOURCE').rglob('*.py')))==17 and all(pin(F/'COMPLETE_REVIEWED_UTILITY_SOURCE'/rel)['sha256']==q['sha256'] for rel,q in before['files'].items()) and all(pin(F/'COMPLETE_ACTUAL_BOUND_PREP_SOURCE'/rel)['sha256']==q['sha256'] for rel,q in bv['files'].items()))
except Exception as ex:errors.append(dict(type=type(ex).__name__,message=str(ex)))
blockers=[c['check'] for c in checks if c['passed'] is not True]+[e['message'] for e in errors]
report=dict(schema='INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1',status='PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION' if not blockers else 'BLOCKED_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_NO_EXECUTION',source_only=True,all_checks_typed_true=not blockers,all_checks_passed=not blockers,check_count=len(checks),checks=checks,blockers=blockers,errors=errors,qualified_complete_utility_manifest_pin=inputs.get(str(U/'MANIFEST.json')),qualified_role_Source_pins=roles,complete_reviewed_utility_original_fullview=before if 'before' in globals() else None,complete_original_owned_Source_views=owners,actual_original_owned_file_count=sum(len(v['files']) for v in owners.values()),actual_all463_original_owned_Source_full_EOF_read=True if len(owners)==2 else False,complete_six_interface_Source_inverse_details=inverse_details,complete_definition_occurrence_inventory=definitions,complete_Source_and_small_META_input_pins=inputs,actual_bound_PREP_manifest_pin=inputs.get(str(PREP/'MANIFEST.json')),actual_bound_PREP_Source_only_peer_manifest_pin=inputs.get(str(BOUNDPEER/'MANIFEST.json')),actual_91304c_binding_only=True,future_new_PREP_business_result=None,future_saved_new_PREP_peer=None,future_actual_bound_BUILD_manifest=None,future_BUILD_terminal=None,actual_Source_installation=None,actual_prelaunch_execution=None,actual_native_execution=None,actual_scientific_qualification=None,no_utility_candidate_binder_helper_guard_API_compile_material_numeric_or_Rootwriter_execution=True,no_graph_trace_gzip_material_library_or_DB_payload_read=True,no_project_or_frozen_Source_or_progress_mutation=True,whole_build_INPUT_RSS_native_science_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with(F/'REVIEW.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with(F/'REVIEWER_SOURCE.byte_exact.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps(dict(status=report['status'],source_only=True,review_pin=pin(F/'REVIEW.json'),reviewer_Source_pin=pin(F/'REVIEWER_SOURCE.byte_exact.py'),check_count=len(checks),blockers=blockers,actual_utility_candidate_or_business_execution=False)),flush=True)
sys.exit(0 if not blockers else 1)

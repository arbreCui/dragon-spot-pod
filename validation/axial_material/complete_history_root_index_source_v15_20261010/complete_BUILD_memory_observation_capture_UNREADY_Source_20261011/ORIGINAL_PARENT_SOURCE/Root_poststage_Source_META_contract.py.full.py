"""Finite V25 poststage Source/META contract. No project imports or business calls."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
A=R/'validation/artifacts'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
PD=B/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'
PE=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
BD=B/'actual_complete_combined_build_v25_poststage_temporaries_sources'
BE=B/'actual_complete_combined_build_v25_poststage_temporaries_receipts'
PH=A/'axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010'
BH=A/'axial-material-complete-combined-build-host-v25-poststage-temporaries-20261010'
S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010'
O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010'
T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010'
AUTHOR=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
AUTHOR_SHA='9085afa282c04c927118323d101c9d23ffce51ebcdd2f2ddda7e4b8d0500d6bd'
AUTHOR_PEER=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_Source_independent_V2_20261010')
AUTHOR_PEER_SHA='6e1627dae76811f4f2c845a10520c5fb5decee9adcbd0b5f03359c800b4b4367'
AUTHOR_PEER_SEAL=Path(str(AUTHOR_PEER)+'_seal_receipt/ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')
AUTHOR_PEER_SEAL_SHA='64cfd24fbcb261e24e889d4254719bf6c21c5a4dc1580d658db2eb3dbd4783e3'
PREP_BOUND=Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')
PREP_BOUND_SHA='531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef'
PREP_BINDING=B/'Root_actual_V25_poststage_PREP_Source_binding_tool_terminal_return.json'
PREP_BINDING_SHA='c3cb0eb7ec35e33f83f64bd0f2f2adcddb35eb4112fab4a686b7353345cb39c2'
Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
QSHA='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
HELPER=R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
HELPER_SHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
SUPPORT=B/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
UTILITY_ROLES=('Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_complete_PREP_E_snapshot.py','Root_prepare_poststage_REQUEST.Source_META_only.py','Root_source_installer.py','Root_prelaunch_checker.py','Root_poststage_Source_META_contract.py')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HSOTDE_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0)
REQUEST_SCHEMA='ROOT_V25_POSTSTAGE_FINITE_ACTUAL_SOURCE_META_INSTALL_REQUEST_V1'
NEW_BUSINESS_PINS=dict(declaration=None,PREP_terminal=None,graph=None,trace=None,PREP_summary=None,BUILD_seal=None,BUILD_terminal=None,runtime=None,host_final_input_PASS=None)

def identity(p):
    v=Path(p).lstat();return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]
def sha_value(s):
    assert type(s) is str and len(s)==64 and s!='0'*64 and all(c in '0123456789abcdef' for c in s)
    return s
def pin(p):
    p=Path(p);i=identity(p)
    assert p.is_absolute() and p.resolve()==p and all(type(n) is int for n in i) and len(i)==7
    assert stat.S_ISREG(i[2]) and i[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def exact(q):
    assert type(q) is dict and set(q) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'})
    sha_value(q['sha256']);assert type(q['identity']) is list and len(q['identity'])==7 and all(type(i) is int for i in q['identity'])
    if 'size_bytes' in q:assert type(q['size_bytes']) is int and q['size_bytes']>=0
    p=pin(q['path']);assert {k:p[k] for k in q}==q
    return p
def read(p,sha=None):
    q=pin(p)
    if sha is not None:assert q['sha256']==sha_value(sha)
    d=json.loads(Path(p).read_bytes());assert pin(p)==q
    return d,q
def view(root):
    root=Path(root);assert root.is_absolute() and root.resolve()==root and root.is_dir() and not root.is_symlink()
    files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink();i=identity(p);rel=str(p.relative_to(root))
        if stat.S_ISREG(i[2]):files[rel]=pin(p)
        else:assert stat.S_ISDIR(i[2]);dirs[rel]=i
    assert dirs['.']==identity(root)
    for rel,q in files.items():assert pin(root/rel)==q
    for rel,i in dirs.items():assert identity(root/rel)==i
    return dict(root=str(root),files=files,directories=dirs,symlinks={})
def package(mp,sha):
    mp=Path(mp);assert mp.name=='MANIFEST.json'
    m,p=read(mp,sha);v=view(mp.parent);members=m['members']
    if type(members) is list:members={q['relative_path']:q for q in members}
    assert type(members) is dict and type(m['member_count']) is int and len(members)==m['member_count'] and m['source_only'] is True
    assert set(v['files'])==set(members)|{'MANIFEST.json'} and m['directories']==v['directories']
    assert all(type(i) is list and len(i)==7 and all(type(n) is int for n in i) for i in m['directories'].values())
    for rel,q in members.items():
        assert Path(q['path'])==mp.parent/rel and v['files'][rel]=={k:q[k] for k in ('path','sha256','size_bytes','identity')}
        exact({k:q[k] for k in ('path','sha256','size_bytes','identity')})
    return m,p,v
def terminal(path,sha):
    d,p=read(path,sha);assert d['closed'] is True and d['observed_terminal'] is True
    t=d.get('terminal_tool_return',d.get('actual_tool_return',d.get('exec_command_result')))
    assert type(t) is dict and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
    assert d.get('session_repolled_after_close',False) is False
    return d,p,t
def peer(mp,sha,seal,seal_sha,schema,status):
    m,mpin,v=package(mp,sha);r,rp=read(Path(mp).parent/'REVIEW.json')
    assert r['schema']==schema and r['status']==status and r['source_only'] is True
    assert r['all_checks_typed_true'] is True and r['blockers']==[] and type(r['checks']) is list and r['checks']
    assert all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
    sd,sp,tr=terminal(seal,seal_sha);observed=json.loads(tr['output'])
    assert observed['manifest_pin']==mpin and observed['review_pin']==rp
    return dict(manifest=mpin,view=v,review=rp,seal=sp),r
def contract():
    return read(Path(__file__).parent/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json')[0]
def author_facts():
    am,ap,av=package(AUTHOR/'MANIFEST.json',AUTHOR_SHA)
    pp,r=peer(AUTHOR_PEER/'MANIFEST.json',AUTHOR_PEER_SHA,AUTHOR_PEER_SEAL,AUTHOR_PEER_SEAL_SHA,'INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1','PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION')
    assert r['qualified_complete_Source_manifest_pin']==ap and r['check_count']==658
    expected=contract()['seven_author_role_Source_pins']
    assert r['qualified_role_Source_pins']==expected
    for q in expected.values():exact(q)
    return dict(manifest=ap,view=av,peer=pp)
def parent_facts(phase):
    c=contract()['complete_old_frozen_Source_owners'][phase];f,fp=read(c['freeze']['path'],c['freeze']['sha256']);assert fp==c['freeze']
    v=view(Path(c['root']));assert f['source_root']==c['root'] and f['symlinks']=={} and f['no_SOURCE_append_after_freeze'] is True
    dirs=f['complete_directories']
    if phase=='PREP':dirs={'.':f['source_root_identity'],**dirs}
    assert v['files']==f['complete_files'] and v['directories']==dirs
    assert v['files']==c['complete_files'] and v['directories']==c['complete_directories']
    assert len(v['files'])==c['original_file_count'] and len(v['directories'])==c['original_directory_count_including_root']
    return dict(freeze=fp,view=v)
def utility_facts(root,a):
    um,up,uv=package(Path(root)/'MANIFEST.json',a.utility_manifest_sha256)
    pp,r=peer(a.utility_peer_manifest,a.utility_peer_manifest_sha256,a.utility_peer_seal,a.utility_peer_seal_sha256,'INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1','PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION')
    assert r['qualified_complete_utility_manifest_pin']==up
    expected={name:uv['files'][name] for name in UTILITY_ROLES}
    assert r['qualified_role_Source_pins']==expected and set(expected)==set(UTILITY_ROLES)
    return dict(manifest=up,view=uv,peer=pp,roles=expected)
def bound_facts(phase,a):
    bm,bp,bv=package(a.bound_manifest,a.bound_manifest_sha256);root=Path(a.bound_manifest).parent
    bd,bip,tr=terminal(a.binding_terminal,a.binding_terminal_sha256);actual=json.loads(tr['output'])
    assert bd['source_only'] is True and actual['manifest']==bp and actual.get('business_or_science_executed',False) is False
    if phase=='PREP':
        assert root==PREP_BOUND and bp['sha256']==PREP_BOUND_SHA and bip['path']==str(PREP_BINDING) and bip['sha256']==PREP_BINDING_SHA and tr['chunk_id']=='91304c'
        roles={'canonical':pin(root/C.name),'prepare_host':pin(root/'combined_prepare_host.py'),'prepare_writer':pin(root/'write_actual_prepare_terminal.py')}
        assert (roles['canonical']['sha256'],roles['prepare_host']['sha256'],roles['prepare_writer']['sha256'])==('6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649','9475d42436aa242e834d8388ee018d3217f8b0bf2326d2384258b3c50b610e0c','e5144866b187ead27dab8b3441d0dcce9dd2c53f94429d22300daec0873d53f0')
        assert actual['canonical']==roles['canonical'] and actual['host']==roles['prepare_host'] and actual['writer']==roles['prepare_writer'] and actual['actual_Q']['sha256']==QSHA
        pp,r=peer(a.bound_peer_manifest,a.bound_peer_manifest_sha256,a.bound_peer_seal,a.bound_peer_seal_sha256,'INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1','PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED')
        assert r['actual_complete_bound_Source_manifest_pin']==bp and r['actual_ready_role_Source_pins']==roles
    else:
        assert root.is_relative_to(Path('/private/tmp')) and root!=PREP_BOUND
        roles={'build_host':pin(root/'combined_build_host.py'),'build_writer':pin(root/'write_actual_build_postclose_META.py')}
        assert actual['host']==roles['build_host'] and actual['writer']==roles['build_writer']
        pp,r=peer(a.bound_peer_manifest,a.bound_peer_manifest_sha256,a.bound_peer_seal,a.bound_peer_seal_sha256,'INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1','PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY')
        expected={'qualified_actual_bound_Source_manifest_pin':bp,'actual_bound_build_host_pin':roles['build_host'],'actual_postclose_META_writer_pin':roles['build_writer'],'actual_Root_Source_binding_tool_receipt_pin':bip}
        for field,q in expected.items():assert r[field]==q
    return dict(manifest=bp,view=bv,roles=roles,binding_terminal=bip,peer=pp)
def host_pin(q):
    return {k:q[k] for k in ('path','sha256','identity')}
def literal_values(path):
    tree=ast.parse(Path(path).read_bytes());values={}
    for n in tree.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:values[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return values
def prepare_input_scope(ph,summary):
    f,fp=read(PE/'Root_prelaunch_complete_source_freeze.json');v=view(PD)
    assert f['schema']=='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1' and f['source_root']==str(PD) and f['symlinks']=={} and f['no_SOURCE_append_after_freeze'] is True
    assert v['files']==f['complete_files'] and v['directories']=={'.':f['source_root_identity'],**f['complete_directories']} and pin(C)==f['canonical_factory']
    assert type(f['file_count']) is int and f['file_count']==len(v['files'])
    install,ip=read(PD/'Root_actual_complete_SOURCE_install_record.json')
    expected_prefix=install['exact_original_host_prefix_seven_input_pins']
    assert len(expected_prefix)==7 and len({q['path'] for q in expected_prefix})==7
    expected=expected_prefix+[host_pin(v['files'][k]) for k in sorted(v['files'])]
    assert ph['input_sources']==expected and len({q['path'] for q in expected})==len(expected)
    assert all(set(q)=={'path','sha256','identity'} for q in expected)
    for q in expected+[ph['original_helper'],ph['resource_factory']]:exact(q)
    total=len(expected)+2
    assert type(summary['all_original_pinned_inputs_unchanged_count']) is int and summary['all_original_pinned_inputs_unchanged_count']==total
    return dict(freeze=fp,complete_Source_file_count=len(v['files']),original_parent_Source_count=135,ordered_input_count=len(expected),protected_input_count=total,old142_144_counts_are_provenance_only=True)
def prep_facts(a):
    summary,sp=read(PE/'Root_actual_complete_combined_prepare_summary.json',a.prep_summary_sha256)
    assert summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
    ns,np=read(PE/'Root_actual_complete_prepare_namespace_manifest.json',a.prep_namespace_sha256);assert exact(summary['namespace_manifest'])==np
    assert ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and [Path(v['root']) for v in ns['namespaces']]==[PH,S,O,T,PD]
    for saved in ns['namespaces']:
        current=view(saved['root']);assert saved['symlinks']=={} and set(current['files'])==set(saved['files'])
        for q in saved['files'].values():exact(q)
        assert {k:i for k,i in current['directories'].items() if k!='.'}=={q['path']:q['identity'] for q in saved['directories']}
    ph,hp=read(summary['actual_host_result']['path'],summary['actual_host_result']['sha256']);exact(summary['actual_host_result']);scope=prepare_input_scope(ph,summary)
    tp=terminal(PE/'Root_actual_prepare_tool_terminal_return.json',a.prep_terminal_sha256)[1]
    wp=terminal(PE/'Root_actual_prepare_metadata_writer_tool_terminal_return.json',a.prep_writer_terminal_sha256)[1]
    assert exact(summary['actual_root_terminal'])==tp
    pp,r=peer(a.saved_prep_peer_manifest,a.saved_prep_peer_manifest_sha256,a.saved_prep_peer_seal,a.saved_prep_peer_seal_sha256,'INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1','PASS_ACTUAL_COMPLETE_PREP_ONLY')
    for field,q in [('actual_Root_PREP_summary_pin',sp),('actual_Root_PREP_terminal_pin',tp),('actual_complete_namespace_manifest_pin',np)]:assert r[field]==q
    for field,path in [('actual_declaration',O/'declaration.json'),('formal_PREP_terminal',T/'declaration_terminal_return.json'),('actual_complete_input_graph',O/'input_graph.json'),('actual_complete_creation_trace',O/'input_creation_python_open_trace.json')]:assert exact(summary[field])['path']==str(path)
    assert pin(C)['sha256']=='6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649'
    return dict(summary=sp,namespace=np,host_result=hp,terminal=tp,writer_terminal=wp,peer=pp,input_scope=scope,current_complete_PREP_E=view(PE),complete_new_PREP_Source=view(PD))
def write(p,d):
    with Path(p).open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def request_main():
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    ap=argparse.ArgumentParser();ap.add_argument('--phase',required=True,choices=('PREP','BUILD'));ap.add_argument('--fresh-TMP-output',required=True)
    keys=('utility-manifest-sha256','utility-peer-manifest','utility-peer-manifest-sha256','utility-peer-seal','utility-peer-seal-sha256','bound-manifest','bound-manifest-sha256','binding-terminal','binding-terminal-sha256','bound-peer-manifest','bound-peer-manifest-sha256','bound-peer-seal','bound-peer-seal-sha256')
    for key in keys:ap.add_argument('--'+key,required=True)
    business=('prep-summary-sha256','prep-namespace-sha256','prep-terminal-sha256','prep-writer-terminal-sha256','saved-prep-peer-manifest','saved-prep-peer-manifest-sha256','saved-prep-peer-seal','saved-prep-peer-seal-sha256')
    for key in business:ap.add_argument('--'+key)
    a=ap.parse_args();out=Path(a.fresh_TMP_output);assert out.is_absolute() and out.parent.resolve()==out.parent and out.is_relative_to(Path('/private/tmp')) and not os.path.lexists(out)
    assert all(getattr(a,k.replace('-','_')) is None for k in business) if a.phase=='PREP' else all(getattr(a,k.replace('-','_')) is not None for k in business)
    author=author_facts();utility=utility_facts(Path(__file__).parent,a);bound=bound_facts(a.phase,a);parent=parent_facts(a.phase)
    qp=pin(Q);hp=pin(HELPER);assert qp['sha256']==QSHA and hp['sha256']==HELPER_SHA
    old_c=exact(contract()['original_canonical_Source_pin'])
    facts=prep_facts(a) if a.phase=='BUILD' else None
    record=dict(schema=REQUEST_SCHEMA,status='ACTUAL_SOURCE_FACTS_BOUND_NO_INSTALL_OR_BUSINESS',phase=a.phase,source_only=True,author=author,utility=utility,bound=bound,parent=parent,actual_helper_Q=qp,installed_helper=hp,original_canonical_Source=old_c,actual_new_PREP=facts,new_business_results=(NEW_BUSINESS_PINS if a.phase=='PREP' else {**NEW_BUSINESS_PINS,'PREP_summary':facts['summary'],'PREP_terminal':facts['terminal']}),original_caps=CAPS,whole_build_INPUT_native_or_science_qualified=False,installation_executed=False)
    write(out,record);print(json.dumps(dict(request=pin(out),phase=a.phase,source_only=True,business_or_science_executed=False)))
def load_request(path,sha,phase):
    d,p=read(path,sha);assert d['schema']==REQUEST_SCHEMA and d['phase']==phase and d['source_only'] is True and d['original_caps']==CAPS and d['installation_executed'] is False and d['whole_build_INPUT_native_or_science_qualified'] is False
    assert d['author']==author_facts()
    u=d['utility'];b=d['bound']
    a=argparse.Namespace(utility_manifest_sha256=u['manifest']['sha256'],utility_peer_manifest=u['peer']['manifest']['path'],utility_peer_manifest_sha256=u['peer']['manifest']['sha256'],utility_peer_seal=u['peer']['seal']['path'],utility_peer_seal_sha256=u['peer']['seal']['sha256'],bound_manifest=b['manifest']['path'],bound_manifest_sha256=b['manifest']['sha256'],binding_terminal=b['binding_terminal']['path'],binding_terminal_sha256=b['binding_terminal']['sha256'],bound_peer_manifest=b['peer']['manifest']['path'],bound_peer_manifest_sha256=b['peer']['manifest']['sha256'],bound_peer_seal=b['peer']['seal']['path'],bound_peer_seal_sha256=b['peer']['seal']['sha256'])
    assert u==utility_facts(Path(u['view']['root']),a) and b==bound_facts(phase,a)
    assert d['parent']==parent_facts(phase) and exact(d['actual_helper_Q'])==pin(Q) and d['actual_helper_Q']['sha256']==QSHA and exact(d['installed_helper'])['sha256']==HELPER_SHA
    assert exact(d['original_canonical_Source'])==exact(contract()['original_canonical_Source_pin'])
    terminal(d['bound']['binding_terminal']['path'],d['bound']['binding_terminal']['sha256'])
    if phase=='PREP':assert d['actual_new_PREP'] is None and d['new_business_results']==NEW_BUSINESS_PINS and d['bound']['manifest']['sha256']==PREP_BOUND_SHA
    else:
        f=d['actual_new_PREP'];assert type(f) is dict and f['current_complete_PREP_E']==view(PE) and f['complete_new_PREP_Source']==view(PD)
        a.prep_summary_sha256=f['summary']['sha256'];a.prep_namespace_sha256=f['namespace']['sha256'];a.prep_terminal_sha256=f['terminal']['sha256'];a.prep_writer_terminal_sha256=f['writer_terminal']['sha256']
        a.saved_prep_peer_manifest=f['peer']['manifest']['path'];a.saved_prep_peer_manifest_sha256=f['peer']['manifest']['sha256'];a.saved_prep_peer_seal=f['peer']['seal']['path'];a.saved_prep_peer_seal_sha256=f['peer']['seal']['sha256']
        assert f==prep_facts(a) and d['new_business_results']=={**NEW_BUSINESS_PINS,'PREP_summary':f['summary'],'PREP_terminal':f['terminal']}
    return d,p
def installed_request(root,phase):
    name='Root_actual_complete_SOURCE_install_record.json' if phase=='PREP' else 'Root_complete_SOURCE_install_record.json'
    i,ip=read(Path(root)/name);d,p=load_request(Path(root)/'Root_actual_Source_META_install_request.byte_exact.json',i['actual_request']['sha256'],phase)
    assert i['installed_request']==p and i['actual_request']['sha256']==p['sha256']
    for owner in i['complete_Source_owner_copies']:
        original=owner['original'];prefix=owner['destination_prefix'];assert view(original['root'])==original
        for rel,q in original['files'].items():
            saved=pin(Path(root)/prefix/rel);assert (saved['sha256'],saved['size_bytes'])==(q['sha256'],q['size_bytes'])
    return d,i
def original_prefix_seven(bound_roles):
    # Complete saved original host prefix is provenance; only canonical slot points to the new Source.
    original=contract()['original_host_prefix_seven_input_pins']
    assert len(original)==7 and original[0]['path']==str(SUPPORT) and original[5]['path']==str(HELPER) and original[6]['path']==str(Q)
    expected=[exact(q) if i!=1 else pin(C) for i,q in enumerate(original)]
    assert expected[0]['sha256']==SUPPORT_SHA and expected[1]['sha256']==bound_roles['canonical']['sha256']
    assert expected[2]['sha256']=='cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447' and expected[3]['sha256']=='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206' and expected[4]['sha256']=='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
    assert len({q['path'] for q in expected})==7
    return [host_pin(q) for q in expected]

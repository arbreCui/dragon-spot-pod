import hashlib,importlib.util,json,os,shutil,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010';A=R/'validation/artifacts'
D=B/'actual_complete_combined_build_v22_sources';E=B/'actual_complete_combined_build_v22_receipts';PRE=B/'actual_complete_combined_prepare_v22_receipts'
H=A/'axial-material-complete-combined-build-host-v22-20261010';S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010';O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010';T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010'
def ident(p):
    v=p.lstat();return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]
def pin(p,wanted=None):
    p=Path(p);before=ident(p);assert p.resolve()==p and stat.S_ISREG(before[2]) and before[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert ident(p)==before
    q=dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
    if wanted:assert q['sha256']==wanted
    return q
def exact(q):
    c=pin(q['path']);assert {k:c[k] for k in q}==q;return c
def read(p,sha=None):
    q=pin(p,sha);d=json.loads(p.read_text());assert pin(p)==q;return d,q
def joint_size(roots):
    total=0
    for root in roots:
        if not root.exists():continue
        assert root.is_dir() and not root.is_symlink()
        for p in root.rglob('*'):
            assert not p.is_symlink()
            if p.is_file():total+=p.lstat().st_size
    return total
def main():
    assert len(sys.argv)==1 and not sys.flags.optimize and sys.getprofile() is None
    freeze_file=E/'Root_prelaunch_complete_build_source_freeze.json';freeze,freeze_pin=read(freeze_file)
    assert freeze['schema']=='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and freeze['source_root']==str(D)
    assert freeze['symlinks']=={} and freeze['no_SOURCE_append_after_freeze'] is True
    assert set(str(f.relative_to(D)) for f in D.rglob('*') if f.is_file())==set(freeze['complete_files'])
    assert not any(f.is_symlink() for f in D.rglob('*'))
    for q in freeze['complete_files'].values():exact(q)
    dirs={'.':ident(D),**{str(p.relative_to(D)):ident(p) for p in D.rglob('*') if p.is_dir()}}
    assert dirs==freeze['complete_directories']
    summary,summary_pin=read(PRE/'Root_actual_complete_combined_prepare_summary.json','0b4ef19900921de593d5979283fd65c779a8df857ee1c6204d4e7b7951f4a306')
    nsfile=Path(summary['namespace_manifest']['path']);nspin=exact(summary['namespace_manifest']);ns=json.loads(nsfile.read_text())
    for entry in ns['namespaces']:
        root=Path(entry['root']);assert set(str(f.relative_to(root)) for f in root.rglob('*') if f.is_file())==set(entry['files'])
        assert not any(f.is_symlink() for f in root.rglob('*'))
        for q in entry['files'].values():exact(q)
        current_dirs={str(p.relative_to(root)):ident(p) for p in root.rglob('*') if p.is_dir()}
        assert current_dirs=={q['path']:q['identity'] for q in entry['directories']}
    phfile=Path(summary['actual_host_result']['path']);exact(summary['actual_host_result']);ph=json.loads(phfile.read_text())
    prep_inputs=ph['input_sources']+[ph['original_helper'],ph['resource_factory']];assert len(prep_inputs)==313
    for q in prep_inputs:exact(q)
    fixed=[exact(q) for q in ph['input_sources'][:7]]
    fixed+=[pin(p) for p in sorted(D.rglob('*')) if p.is_file()]
    fixed+=[exact(summary['actual_declaration']),exact(summary['formal_PREP_terminal']),exact(summary['actual_complete_input_graph']),exact(summary['actual_complete_creation_trace'])]
    fixed+=[pin(p) for root in (S,T) for p in sorted(root.rglob('*')) if p.is_file()]
    fixed+=[exact(summary['actual_root_terminal']),summary_pin,exact(ph['original_helper']),exact(ph['resource_factory'])]
    host_pin=pin(D/'combined_build_host.py','cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269')
    assert not os.path.lexists(H)
    for rel in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','audit/binary_identity.json','audit/result.json','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22/stages.json','runtime/Dragon'):assert not os.path.lexists(O/rel)
    support_path=Path(fixed[0]['path']);assert fixed[0]['sha256']=='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
    spec=importlib.util.spec_from_file_location('Root_v22_complete_build_prelaunch_original_support',support_path)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    assert Path(sys.executable).resolve()==support.PYTHON and all(os.environ.get(k)=='1' for k in support.THREAD_KEYS)
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'Root_v22_build_prelaunch_genuine619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'Root_v22_build_prelaunch_genuine_ebbb')
    full,production=helper.modules();helper.guard_admission(full)
    assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
    assert Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
    assert {k:fixed[-2][k] for k in hpin}==hpin and {k:fixed[-1][k] for k in rpin}==rpin
    roots=resource.history_roots([str(p) for p in (H,S,O,T)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    actual_resources=resources.check()
    assert actual_resources['artifact_bytes']+2*2**30<96*2**30 and actual_resources['disk_free_bytes']-2*2**30>=8*2**30
    extra_roots=[H,S,O,T,D,E,A/'axial-material-complete-combined-prepare-host-v22-20261010',B/'actual_complete_combined_prepare_v22_sources',PRE]
    canonical=Path(fixed[1]['path']);before_bytes=joint_size(extra_roots)+canonical.stat().st_size
    assert before_bytes<2*2**30
    q=dict(schema='ROOT_V22_COMPLETE_BUILD_FINAL_PRELAUNCH_SOURCE_INPUT_RESERVE_CHECK_V1',status='PRELAUNCH_PASS_NO_BUILD_EXECUTED',fixed_input_pins=fixed,fixed_input_entries_count=len(fixed),source_freeze=freeze_pin,complete_SOURCE_files=freeze['complete_files'],complete_SOURCE_directories=freeze['complete_directories'],prepared_namespace_manifest=nspin,actual_PREP_summary=summary_pin,canonical_factory=fixed[1],normal_host=host_pin,genuine_guard_original_MRO_verified=True,actual_genuine_history_resources=actual_resources,complete_joint_scope_roots=[str(p) for p in extra_roots],complete_joint_bytes_before_prelaunch_record=before_bytes,original_host_joint_scope_is_H_S_O_T_D=True,complete_Root_extra_scope_ledger_does_not_modify_host_guard=True,whole_seconds_cap=1800,stage_seconds_cap=600,rss_mib_cap=512,joint_archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0,HOST_fresh=True,all_new_build_outputs_absent=True,all_original313_PREP_inputs_unchanged=True,all_prepared_namespaces_unchanged=True,SOURCE_frozen_no_append=True,numeric_or_build_executed=False)
    out=E/'Root_final_prelaunch_source_input_and_reserve_check.json'
    with out.open('x') as f:json.dump(q,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    assert joint_size(extra_roots)+canonical.stat().st_size<2*2**30
    for q in fixed:exact(q)
    print(json.dumps(dict(status='PRELAUNCH_PASS_NO_BUILD_EXECUTED',complete_Source_files=len(freeze['complete_files']),fixed_input_entries=len(fixed),preflight=pin(out),actual_history_bytes=actual_resources['artifact_bytes'],free_bytes=actual_resources['disk_free_bytes'],complete_joint_bytes=joint_size(extra_roots)+canonical.stat().st_size,new_build_or_numeric_executed=False)))
if __name__=='__main__':main()

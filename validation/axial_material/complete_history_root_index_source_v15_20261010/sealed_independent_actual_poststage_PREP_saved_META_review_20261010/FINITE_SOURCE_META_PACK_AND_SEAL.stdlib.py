"""Finite Source/small-META retention and one seal/postseal. No business calls."""
import hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_V25_actual_poststage_PREP_saved_Source_META_independent_ATTEMPT1_20261010')
S=Path(str(F)+'_seal_receipt')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010')
T=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010')
A=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010')
def ident(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p)
    if not(p.is_absolute() and not any(x.is_symlink() for x in(p,*p.parents)) and stat.S_ISREG(a[2]) and a[3]==1):raise ValueError('ordinary Source/META')
    if p.name in('input_graph.json','input_creation_python_open_trace.json') or p.suffix in('.gz','.xsm','.db','.sqlite','.so','.o','.a'):raise ValueError('physical or graph trace payload read forbidden')
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=a:raise ValueError('Source META full EOF7ID changed')
    return dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def load(p):
    q=pin(p);d=strict(Path(p).read_bytes())
    if pin(p)!=q:raise ValueError('Source META parse changed')
    return d
def view(root,exclude=()):
    root=Path(root);fs={};ds={'.':ident(root)}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));i=ident(p)
        if stat.S_ISDIR(i[2]):ds[rel]=i
        elif stat.S_ISREG(i[2]):
            if rel not in exclude:fs[rel]=pin(p)
        else:raise ValueError('ordinary Source namespace only')
    return dict(files=fs,directories=ds)
def copy(p,name):
    p=Path(p);q=pin(p);dst=F/name;dst.parent.mkdir(parents=True,exist_ok=True)
    with p.open('rb') as a,dst.open('xb') as b:
        while True:
            block=a.read(2**20)
            if not block:break
            b.write(block)
    result=pin(dst)
    if pin(p)!=q or (result['sha256'],result['size_bytes'])!=(q['sha256'],q['size_bytes']):raise ValueError('lossless finite Source/META retention')
    return dict(original=q,saved=result)
def validate():
    r=load(F/'REVIEW.json');cs=r['checks']
    if not(r['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and r['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and r['source_only'] is True and r['all_checks_typed_true'] is True and r['check_count']==len(cs)==31 and len({q['check'] for q in cs})==31 and all(type(q['passed']) is bool and q['passed'] is True for q in cs) and r['blockers']==[] and r['actual_PREP_closed_EXIT0_verified'] is True and r['actual_metadata_writer_closed_EXIT0_verified'] is True and r['actual_PREP_metadata_only'] is True and r['all_complete_scope_verified'] is True):raise ValueError('actual independent PREP-only review contract')
    for path,q in r['full_EOF_Source_and_small_META_pins'].items():
        if pin(path)!=q:raise ValueError('all original Source/small META EOF changed')
    for path,q in r['Root_actual_full_EOF_business_payload_pins_verified_current7ID_only'].items():
        if ident(path)!=q['identity']:raise ValueError('Root observed business file7ID changed')
    for name in('actual_Root_PREP_summary_pin','actual_Root_PREP_terminal_pin','actual_complete_namespace_manifest_pin'):
        if pin(r[name]['path'])!=r[name]:raise ValueError('three actual saved endpoints changed')
    w=load(F/'ACTUAL_INDEPENDENT_SAVED_META_REVIEW_TOOL_RETURN.json');t=w['terminal_tool_return'];o=strict(t['output'])
    if not(w['closed'] is True and w['observed_terminal'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and t['chunk_id']=='736ff8' and o['review_pin']==pin(F/'REVIEW.json') and o['check_count']==31):raise ValueError('real review tool coupling')
    return r
def emit(v):print(json.dumps(v,allow_nan=False),flush=True)
def main():
    mode=sys.argv[1];r=validate()
    if mode=='retain':
        cfg=load(r['actual_review_input_contract_pin']['path']);paths={Path(r['actual_review_input_contract_pin']['path'])}
        for v in cfg.values():
            if type(v) is dict and set(v)=={'path','sha256','size_bytes','identity'}:paths.add(Path(v['path']))
        paths.update(E.iterdir())
        paths.update((H/'result.json',H/'run/prepare.watchdog.json',H/'run/prepare.log',H/'COMBINED_PREPARATION/stages.json',O/'declaration.json',A/'source_admission.json',T/'declaration_terminal_return.json',T/'Root_actual_SOURCE_inventory.json'))
        paths.update(T/name for name in('actual_child_merged_stdout_stderr.json','actual_external_host_stderr.txt','actual_external_host_stdout.json','actual_external_Root_tool_terminal.json'))
        ledger={str(p):copy(p,'FINITE_ACTUAL_SOURCE_META_COPIES/'+str(n).zfill(3)+'_'+p.name) for n,p in enumerate(sorted(paths,key=str))}
        for p,name in [(Path('/private/tmp/spot_V25_poststage_saved_PREP_Source_META_independent_UNREADY_reviewer_20261010.py'),'ORIGINAL_COMPLETE_UNREADY_REVIEWER_Source.py'),(Path('/private/tmp/spot_V25_poststage_saved_PREP_independent_complete_current_contract_Source_inverse_20261010.json'),'COMPLETE_NINE_HUNK_CURRENT_CONTRACT_SOURCE_INVERSE.json'),(Path('/private/tmp/axmat_v25_monitor_access_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_ORIGINAL_STAGE_STORAGE_20261010/REVIEWER_EXECUTED_SOURCE.py'),'ORIGINAL_21204_SAVED_PREP_REVIEWER.complete_Source.py')]:copy(p,'FINITE_REVIEWER_SOURCE_PROVENANCE/'+name)
        with(F/'COMPLETE_FINITE_ACTUAL_SOURCE_META_RETENTION.json').open('x') as f:json.dump(dict(schema='FINITE_ACTUAL_POSTSTAGE_PREP_SOURCE_SMALL_META_RETENTION_V1',source_only=True,unique_original_Source_META_count=len(ledger),complete_current_E_files=8,copies=ledger,graph_trace_gzip_material_or_native_payload_copied=False,actual_old_history_cloned=False),f,indent=2);f.write('\n')
        emit(dict(source_only=True,actual_finite_copy_count=len(ledger),ledger_pin=pin(F/'COMPLETE_FINITE_ACTUAL_SOURCE_META_RETENTION.json'),no_business_payload_read_or_copied=True))
    elif mode=='seal':
        with(F/'MANIFEST.json').open('xb') as f:
            v=view(F,('MANIFEST.json',));m=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_SOURCE_META_REVIEW_MANIFEST_V1',source_only=True,status='SEALED_ACTUAL_COMPLETE_PREP_ONLY_NO_BUILD_NATIVE_SCIENCE_CREDIT',members=v['files'],directories=v['directories'],member_count=len(v['files']),file_count_including_manifest=len(v['files'])+1,directory_count=len(v['directories']),review_pin=pin(F/'REVIEW.json'),actual_review_tool_truth_pin=pin(F/'ACTUAL_INDEPENDENT_SAVED_META_REVIEW_TOOL_RETURN.json'),check_count=31,blockers=[],actual_Root_PREP_summary_pin=r['actual_Root_PREP_summary_pin'],actual_Root_PREP_terminal_pin=r['actual_Root_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=r['actual_complete_namespace_manifest_pin'],whole_BUILD_INPUT_native_RSS_science_qualified=False)
            f.write((json.dumps(m,indent=2,allow_nan=False)+'\n').encode())
        if view(F,('MANIFEST.json',))!=v:raise ValueError('seal changed finite Source/Meta member or directory')
        emit(dict(source_only=True,manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=31,blockers=[],actual_Root_PREP_summary_pin=r['actual_Root_PREP_summary_pin'],actual_Root_PREP_terminal_pin=r['actual_Root_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=r['actual_complete_namespace_manifest_pin'],new_business_or_science_execution=False))
    elif mode=='postseal':
        m=load(F/'MANIFEST.json');mp=pin(F/'MANIFEST.json');v=view(F,('MANIFEST.json',))
        if m['members']!=v['files'] or m['directories']!=v['directories'] or m['member_count']!=len(v['files']):raise ValueError('complete finite Source META postseal')
        w=load(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');t=w['terminal_tool_return'];o=strict(t['output'])
        if not(w['closed'] is True and w['observed_terminal'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and o['manifest_pin']==mp and o['review_pin']==pin(F/'REVIEW.json')):raise ValueError('real Source META seal tool coupling')
        proof=dict(schema='INDEPENDENT_ACTUAL_POSTSTAGE_PREP_FULL_SOURCE_META_POSTSEAL_VERIFICATION_V1',source_only=True,manifest_pin=mp,review_pin=pin(F/'REVIEW.json'),actual_Source_seal_tool_truth_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=31,blockers=[],all_finite_member_names_full_EOF_SHA_size_7ID_and_directories_unchanged=True,original_Source_small_META_full_EOF_unchanged=True,Root_observed_business_file7ID_unchanged_no_payload_EOF_read=True,new_business_or_science_execution=False)
        path=S/'FULL_SOURCE_META_POSTSEAL_VERIFICATION.json'
        with path.open('x') as f:json.dump(proof,f,indent=2);f.write('\n')
        if pin(F/'MANIFEST.json')!=mp or view(F,('MANIFEST.json',))!=v:raise ValueError('postseal mutated frozen Source META')
        emit(dict(source_only=True,manifest_pin=mp,review_pin=pin(F/'REVIEW.json'),verification_pin=pin(path),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=31,blockers=[],new_business_or_science_execution=False))
    else:raise ValueError('one explicit finite retention seal or postseal mode')
if __name__=='__main__':main()

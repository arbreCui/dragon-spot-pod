"""Finite private review seal; Source/META EOF, business file7ID only."""
import hashlib,json,os,stat,sys
from pathlib import Path
D=Path('/private/tmp/axmat_P4_ACTUAL_PREP_SAVED_Source_META_INDEPENDENT_56olj6zv');S=D.with_name(D.name+'_seal_receipt')
def ident(p):
    t=Path(p).lstat();return[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
def full(p,allow_package=True):
    p=Path(p);a=ident(p);assert p.resolve()==p and stat.S_ISREG(a[2])and a[3]==1 and a[4]<=16*2**20
    assert p.name not in ('input_graph.json','input_creation_python_open_trace.json')and p.suffix not in ('.gz','.xsm','.sqlite','.db','.h5','.hdf5','.so','.a','.o')and not p.name.startswith('draglib')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        t=os.fstat(fd);assert[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==a;b=b''
        while True:
            c=os.read(fd,min(65536,16*2**20+1-len(b)))
            if not c:break
            b+=c;assert len(b)<=16*2**20
        t=os.fstat(fd);assert len(b)==a[4]and os.read(fd,1)==b''and[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==a and ident(p)==a
    finally:os.close(fd)
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=a)
def write(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    return full(p)[1]
def inventory():
    files={};dirs={}
    for root,sub,names in os.walk(D,followlinks=False):
        root=Path(root);dirs[str(root.relative_to(D))]=ident(root)
        for q in sub:assert not(root/q).is_symlink()
        for name in names:
            p=root/name
            if p.name=='MANIFEST.json'and p.parent==D:continue
            files[str(p.relative_to(D))]=full(p)[1]
    return files,dirs
def verify():
    mp=full(D/'MANIFEST.json')[1];m=json.loads(full(D/'MANIFEST.json')[0]);files,dirs=inventory();assert files==m['members']and dirs==m['directories']
    report_pin=full(D/'attempt2_output/REVIEW.json')[1];r=json.loads(full(D/'attempt2_output/REVIEW.json')[0]);assert r['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'and r['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'and r['source_only']is True and r['all_checks_typed_true']is True and r['check_count']==len(r['checks'])==31 and r['blockers']==[]
    assert len({c['check']for c in r['checks']})==31 and all(set(c)=={'check','passed'}and type(c['passed'])is bool and c['passed']is True for c in r['checks'])
    raw=json.loads(full(D/'ACTUAL_ATTEMPT2_REVIEW_TOOL_RETURN.json')[0]);t=raw['terminal_tool_return'];assert raw['closed']is True and raw['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==raw['actual_terminal_chunk']=='faf1b5'and json.loads(t['output'])['review_pin']==report_pin
    failed=json.loads(full(D/'ACTUAL_ATTEMPT1_REVIEW_TOOL_RETURN.json')[0]);assert failed['terminal_tool_return']['exit_code']==1 and failed['actual_terminal_chunk']=='01ec54'and(D/'attempt1_output/FAILED_ATTEMPT.json').is_file()and(D/'attempt1_output/REVIEWER_FAILED_ATTEMPT_SOURCE.py').is_file()
    for p,q in r['full_EOF_Source_and_small_META_pins'].items():assert full(p)[1]==q
    for p,q in r['Root_actual_full_EOF_business_payload_pins_verified_current7ID_only'].items():assert ident(p)==q['identity']and stat.S_ISREG(q['identity'][2])and q['identity'][3]==1 and q['identity'][4]==q['size_bytes']
    namespace_shapes={}
    for root,wanted in r['complete_namespace_counts'].items():
        paths=list(Path(root).rglob('*'));actual=dict(files=sum(stat.S_ISREG(p.lstat().st_mode)for p in paths),directories=sum(stat.S_ISDIR(p.lstat().st_mode)for p in paths));assert actual==wanted and not any(p.is_symlink()for p in paths);namespace_shapes[root]=actual
    for k in('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):assert r[k]is False
    assert r['graph_trace_gzip_native_material_or_DB_payload_read']is False and r['new_reviewer_business_or_API_execution']is False
    metrics=r['metrics'];assert metrics['current_joint_bytes']==metrics['historical_joint_bytes']+metrics['writer_own_summary_after_sample_bytes']+metrics['external_later_E_append_bytes']==164076988 and metrics['current_joint_bytes']<2*2**30
    return dict(manifest_pin=mp,review_pin=report_pin,actual_review_tool_pin=full(D/'ACTUAL_ATTEMPT2_REVIEW_TOOL_RETURN.json')[1],Source_only=True,all31_checks_typed_true=True,blockers=[],review_status=r['status'],complete_review_member_pins=files,complete_review_directory_7ID=dirs,review_file_count=len(files)+1,review_directory_count=len(dirs),actual_review_chunk='faf1b5',actual_review_exit_code=0,complete_Source_META_EOF_pin_count=len(r['full_EOF_Source_and_small_META_pins']),Root_payload_7ID_only_count=len(r['Root_actual_full_EOF_business_payload_pins_verified_current7ID_only']),complete_Source_AST_count=len(r['complete_definition_occurrence_counts']),current_protected_inputs=r['complete_actual_input_entries'],complete_namespace_counts=namespace_shapes,metrics=metrics,actual_Root_PREP_summary_pin=r['actual_Root_PREP_summary_pin'],actual_Root_PREP_terminal_pin=r['actual_Root_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=r['actual_complete_namespace_manifest_pin'],failed_first_attempt_real_raw_and_full_source_retained=True,no_candidate_API_or_business_execution=True)
mode=sys.argv[1]
if mode=='seal':
    assert not os.path.lexists(D/'MANIFEST.json')and not os.path.lexists(S)
    fd=os.open(D/'MANIFEST.json',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o644);os.close(fd);files,dirs=inventory()
    with(D/'MANIFEST.json').open('w')as f:json.dump(dict(schema='INDEPENDENT_ACTUAL_P4_COMPLETE_PREP_SAVED_SOURCE_META_REVIEW_PACKAGE_V1',source_only=True,status='PASS_ACTUAL_COMPLETE_PREP_ONLY',member_count=len(files),members=files,directories=dirs),f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    v=verify();S.mkdir();sp=write(S/'SEAL_REPORT.json',dict(schema='TRUE_SIBLING_INDEPENDENT_ACTUAL_P4_SAVED_PREP_REVIEW_SEAL_V1',all_integrity_checks_typed_true=True,**v))
    print(json.dumps(dict(status='SEALED_PASS_ACTUAL_COMPLETE_PREP_ONLY',source_only=True,manifest_pin=v['manifest_pin'],review_pin=v['review_pin'],seal_report_pin=sp,review_file_count=v['review_file_count'],review_directory_count=v['review_directory_count'],actual_review_chunk='faf1b5',actual_review_exit_code=0,all31_checks_typed_true=True,candidate_or_API_or_business_executed=False),sort_keys=True))
elif mode=='post':
    sp=full(S/'SEAL_REPORT.json')[1];old=json.loads(full(S/'SEAL_REPORT.json')[0]);v=verify();assert all(old[k]==x for k,x in v.items())and full(S/'SEAL_REPORT.json')[1]==sp
    pp=write(S/'POSTSEAL_REPORT.json',dict(schema='COMPLETE_FULL_EOF_INDEPENDENT_ACTUAL_P4_SAVED_PREP_REVIEW_POSTSEAL_V1',all_integrity_checks_typed_true=True,true_sibling_seal_report_pin=sp,**v))
    print(json.dumps(dict(status='POSTSEAL_COMPLETE_FULL_EOF_PASS_ACTUAL_COMPLETE_PREP_ONLY',source_only=True,manifest_pin=v['manifest_pin'],review_pin=v['review_pin'],seal_report_pin=sp,postseal_report_pin=pp,review_file_count=v['review_file_count'],review_directory_count=v['review_directory_count'],all31_checks_typed_true=True,actual_review_chunk='faf1b5',actual_review_exit_code=0,candidate_or_API_or_business_executed=False),sort_keys=True))
else:raise ValueError('unknown finite private seal mode')

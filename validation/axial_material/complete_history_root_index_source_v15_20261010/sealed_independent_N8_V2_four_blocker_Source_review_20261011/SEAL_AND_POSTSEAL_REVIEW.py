"""Seal this independent Source-only current pass review; never execute candidate."""
import hashlib,json,os,stat,sys
from pathlib import Path
D=Path('/private/tmp/axmat_N8_V2_four_blocker_INDEPENDENT_review_4prv7dk5')
S=D.with_name(D.name+'_seal_receipt')
def identity(t):return [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
def read(p):
    p=Path(p);before=identity(p.lstat());assert p.resolve()==p and stat.S_ISREG(before[2])and before[3]==1 and 0<=before[4]<=4*2**20
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        assert identity(os.fstat(fd))==before;raw=b''
        while True:
            part=os.read(fd,min(65536,4*2**20+1-len(raw)))
            if not part:break
            raw+=part;assert len(raw)<=4*2**20
        assert len(raw)==before[4]and os.read(fd,1)==b''and identity(os.fstat(fd))==before and identity(p.lstat())==before
    finally:os.close(fd)
    return raw,dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
def write_new(p,v):
    with p.open('x')as stream:json.dump(v,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    return read(p)[1]
def inventory():
    files={};dirs={}
    for root,subs,names in os.walk(D,followlinks=False):
        root=Path(root);dirs[str(root)]=identity(root.lstat())
        for sub in subs:assert not(root/sub).is_symlink()
        for name in names:
            p=root/name
            if p==D/'MANIFEST.json':continue
            files[str(p.relative_to(D))]=read(p)[1]
    return files,dirs
def candidate_recheck(result):
    pins=result['all_complete_source_member_pins'];root=Path(result['candidate_manifest_pin']['path']).parent;actual={}
    for rel,wanted in pins.items():
        got=read(root/rel)[1];assert got==wanted;actual[rel]=got
    dirs={str(Path(rootdir)):identity(Path(rootdir).lstat())for rootdir in result['complete_source_directory_7ID']}
    assert dirs==result['complete_source_directory_7ID']
    names={str(p.relative_to(root))for p in root.rglob('*')if p.is_file()};assert names==set(pins)
    return dict(candidate_manifest_pin=pins['MANIFEST.json'],candidate_complete_file_count=len(actual),candidate_complete_directory_count=len(dirs),all_full_EOF_SHA_size_descriptor_path_7ID_unchanged=True)
def verify():
    raw,mp=read(D/'MANIFEST.json');m=json.loads(raw);files,dirs=inventory();assert files==m['members']and dirs==m['directories']
    report=json.loads(read(D/'REVIEW.json')[0]);assert report['source_only']is True and report['all_checks_passed']is True and report['all_checks_typed_true']is True and report['blockers']==[] and report['check_count']==len(report['checks'])==154 and all(c['passed']is True for c in report['checks'])
    assert len({c['check']for c in report['checks']})==154 and all(set(c)=={'check','passed'}and type(c['passed'])is bool for c in report['checks'])
    truth=json.loads(read(D/'ACTUAL_INDEPENDENT_SOURCE_VERDICT_TOOL_RETURN.json')[0]);terminal=truth['terminal_tool_return'];assert truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and truth['actual_terminal_chunk']==terminal['chunk_id']=='54cfe9'
    output=json.loads(terminal['output']);assert output['review_pin']==read(D/'REVIEW.json')[1]and output['all_checks_passed']is True and output['blocker_count']==0
    result=json.loads(read(D/'COMPLETE_ALL_SOURCE_EOF_AST_RETENTION_NATIVE_ARCHIVE_AND_INVERSE_RESULTS.json')[0]);c=candidate_recheck(result)
    return dict(manifest_pin=mp,report_pin=read(D/'REVIEW.json')[1],actual_Source_verdict_tool_return_pin=read(D/'ACTUAL_INDEPENDENT_SOURCE_VERDICT_TOOL_RETURN.json')[1],review_complete_file_count=len(files)+1,review_complete_directory_count=len(dirs),complete_member_pins=files,complete_directory_7ID=dirs,actual_Source_verdict_exit_code=0,actual_Source_verdict_chunk='54cfe9',all_checks_passed=True,check_count=154,passed_check_count=154,blocker_count=0,actual_author_Source_contract=report['actual_author_Source_contract'],**c)
mode=sys.argv[1]
if mode=='seal':
    assert not os.path.lexists(D/'MANIFEST.json')and not os.path.lexists(S)
    fd=os.open(D/'MANIFEST.json',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o644);os.close(fd)
    files,dirs=inventory();manifest=dict(schema='INDEPENDENT_N8_COMPLETE_SOURCE_REVIEW_SEALED_MANIFEST_V1',source_only=True,status='SEALED_REAL_PASSED_SOURCE_REVIEW_NOT_RUNTIME_OR_SCIENCE',members=files,directories=dirs)
    with (D/'MANIFEST.json').open('w')as stream:json.dump(manifest,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    verified=verify();S.mkdir();pin=write_new(S/'SEAL_REPORT.json',dict(schema='ACTUAL_INDEPENDENT_N8_SOURCE_REVIEW_TRUE_SIBLING_SEAL_V1',status='INTEGRITY_PASS_SOURCE_VERDICT_REMAINS_REAL_PASS',source_only=True,all_integrity_checks_typed_true=True,**verified))
    print(json.dumps(dict(status='TRUE_SIBLING_SEAL_INTEGRITY_PASS_SOURCE_REAL_PASS_RETAINED',source_only=True,manifest_pin=verified['manifest_pin'],report_pin=verified['report_pin'],seal_report_pin=pin,review_complete_files=verified['review_complete_file_count'],review_complete_directories=verified['review_complete_directory_count'],actual_Source_verdict_chunk='54cfe9',actual_Source_verdict_exit_code=0,candidate_or_API_or_business_executed=False),sort_keys=True))
elif mode=='post':
    before=read(S/'SEAL_REPORT.json')[1];seal=json.loads(read(S/'SEAL_REPORT.json')[0]);verified=verify();assert all(seal[k]==v for k,v in verified.items());assert read(S/'SEAL_REPORT.json')[1]==before
    pin=write_new(S/'POSTSEAL_REPORT.json',dict(schema='ACTUAL_INDEPENDENT_N8_COMPLETE_SOURCE_REVIEW_POSTSEAL_V1',status='COMPLETE_FULL_EOF_POSTSEAL_INTEGRITY_PASS_SOURCE_VERDICT_REMAINS_REAL_PASS',source_only=True,all_integrity_checks_typed_true=True,true_sibling_seal_report_pin=before,**verified))
    print(json.dumps(dict(status='COMPLETE_FULL_EOF_POSTSEAL_INTEGRITY_PASS_SOURCE_REAL_PASS_RETAINED',source_only=True,manifest_pin=verified['manifest_pin'],report_pin=verified['report_pin'],seal_report_pin=before,postseal_report_pin=pin,review_complete_files=verified['review_complete_file_count'],review_complete_directories=verified['review_complete_directory_count'],candidate_complete_files=verified['candidate_complete_file_count'],candidate_complete_directories=verified['candidate_complete_directory_count'],actual_Source_verdict_chunk='54cfe9',actual_Source_verdict_exit_code=0,candidate_or_API_or_business_executed=False),sort_keys=True))
else:raise ValueError('unknown finite review seal mode')

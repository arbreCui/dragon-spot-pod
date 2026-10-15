"""Seal only this independent saved SOURCE review; stdlib, no business calls."""
import hashlib
import json
from pathlib import Path
import stat

B=Path(__file__).absolute().parent

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    a=identity(p);raw=p.read_bytes();z=identity(p)
    if a!=z or len(raw)!=a[4]or not stat.S_ISREG(a[2])or a[3]!=1:raise ValueError('source7ID/fullEOF changed')
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)

def tree(p):
    f=[];d=[]
    for q in sorted(p.rglob('*')):
        s=q.lstat()
        if stat.S_ISDIR(s.st_mode):d.append(dict(path=str(q),identity=identity(q)))
        elif stat.S_ISREG(s.st_mode)and s.st_nlink==1:f.append(pin(q))
        else:raise ValueError('unexpected Source namespace member')
    return dict(root=str(p),root_identity=identity(p),directories=d,files=f)

report=json.loads((B/'REVIEW.json').read_bytes())
if report['schema']!='INDEPENDENT_CURRENT150_AB_FULL_RAWRECORD_BINDING_HOST_SOURCE_REVIEW_V1'or report['status']!='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'or report['all_checks_passed']is not True or report['blockers']!=[]or len(report['checks'])!=430 or not all(type(r)is dict and r['pass']is True for r in report['checks']):raise ValueError('exact complete independent SOURCE report required')
if pin(B/'REVIEW.json')['sha256']!='85514d32a0052678f72f7fc23b9f1729eeca7b7a44ee5912da467408f42d3e2d':raise ValueError('final Source review changed')
before=report['complete_derivative_source_namespace_before']
if tree(Path(before['root']))!=before:raise ValueError('sealed author SOURCE full namespace changed since independent review')
terminal=json.loads((B/'actual_SOURCE_review_tool_terminal_return.json').read_bytes());tr=terminal['terminal_tool_return']
if terminal['closed']is not True or terminal['source_only']is not True or terminal['actual_tool_terminal_return_observed']is not True or type(tr['exit_code'])is not int or tr['exit_code']!=0 or 'session_id'in tr or terminal['review_sha256']!=pin(B/'REVIEW.json')['sha256']:raise ValueError('real exact typed0 SOURCE terminal required')
files=[pin(q)for q in sorted(B.iterdir())if q.is_file()]
for row in files:row['relative_path']=Path(row['path']).name
manifest=dict(schema='INDEPENDENT_CURRENT150_AB_COMPLETE_RAWRECORD_SOURCE_REVIEW_SEAL_V1',source_only=True,status=report['status'],all_checks_passed=True,check_count=430,review=pin(B/'REVIEW.json'),actual_SOURCE_review_terminal=pin(B/'actual_SOURCE_review_tool_terminal_return.json'),qualified_source_manifest_sha256=report['qualified_source_manifest_sha256'],complete_qualified_source_namespace_unchanged=True,files=files,file_count=len(files),total_file_bytes=sum(x['size_bytes']for x in files),actual_transfer_qualification_sha256=None,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
target=B/'MANIFEST.json'
with target.open('x')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
if tree(Path(before['root']))!=before:raise ValueError('author sealed namespace changed during Source seal')
print(json.dumps(dict(source_only=True,status=report['status'],manifest=pin(target),file_count=len(files),check_count=430,actual_review_chunk=tr['chunk_id'],reviewed_API_or_business_executed=False),allow_nan=False))

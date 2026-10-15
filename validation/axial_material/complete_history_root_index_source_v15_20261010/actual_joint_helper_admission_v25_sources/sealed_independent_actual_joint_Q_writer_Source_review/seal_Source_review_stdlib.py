"""Only seals this finite Source review; never executes reviewed Source."""
import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).parent
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p)
    if not stat.S_ISREG(before[2]):raise ValueError('ordinary review file')
    h=hashlib.sha256()
    with p.open('rb')as f:
        while b:=f.read(1024*1024):h.update(b)
    if identity(p)!=before:raise ValueError('changed review input')
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
r=json.loads((P/'REVIEW.json').read_bytes());t=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_RETURNS.json').read_bytes())
if r['source_only']is not True or r['all_checks_typed_true']is not True or r['blockers']!=[] or type(r['check_count'])is not int or r['check_count']!=65 or len(r['checks'])!=65 or len({x['check']for x in r['checks']})!=65 or not all(type(x['passed'])is bool and x['passed']is True for x in r['checks']):raise ValueError('Source review contract')
a=t['actual_success_tool_return']
if type(a['exit_code'])is not int or a['exit_code']!=0 or 'session_id'in a or a['chunk_id']!='03e988':raise ValueError('genuine completed review tool required')
out=json.loads(a['output'])
if out['review_pin']!=pin(P/'REVIEW.json')or out['check_count']!=65 or out['source_only']is not True:raise ValueError('actual review output coupling')
if pin(Path(r['qualified_Root_writer_Source_pin']['path']))!=r['qualified_Root_writer_Source_pin']:raise ValueError('Root writer changed')
if pin(P/'REVIEWED_ROOT_V25_JOINT_Qwriter_SOURCE.py')!=r['reviewed_Source_copy_pin']:raise ValueError('Source copy changed')
manifest=P/'MANIFEST.json'
with manifest.open('xb'):pass
files={str(p.relative_to(P)):pin(p)for p in sorted(P.rglob('*'))if p.is_file()and p!=manifest}
dirs={'.':identity(P),**{str(p.relative_to(P)):identity(p)for p in sorted(P.rglob('*'))if p.is_dir()}}
d=dict(schema='INDEPENDENT_ROOT_V25_JOINT_Q_WRITER_SOURCE_REVIEW_MANIFEST_V1',source_only=True,review_status=r['status'],check_count=65,complete_members=files,complete_directories=dirs,member_count=len(files),complete_member_bytes=sum(v['size_bytes']for v in files.values()),manifest_self_excluded=True,no_qualification_created=True,reviewed_writer_executed=False)
with manifest.open('w')as f:json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
for rel,v in files.items():
    if pin(P/rel)!=v:raise ValueError('member changed during seal')
if identity(P)!=dirs['.']:raise ValueError('seal directory changed')
print(json.dumps(dict(status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION',source_only=True,manifest_pin=pin(manifest),review_pin=pin(P/'REVIEW.json'),writer_pin=r['qualified_Root_writer_Source_pin'],check_count=65,member_count=len(files),candidate_or_writer_API_or_numeric_executed=False)))

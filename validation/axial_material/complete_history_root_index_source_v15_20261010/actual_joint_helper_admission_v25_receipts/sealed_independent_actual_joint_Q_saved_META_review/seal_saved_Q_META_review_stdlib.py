"""Seals only this saved helper Q metadata review; no candidate execution."""
import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).parent
def identity(p):
    s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p)
    if not stat.S_ISREG(before[2]):raise ValueError('regular finite Source/META')
    h=hashlib.sha256()
    with p.open('rb')as f:
        while b:=f.read(1024*1024):h.update(b)
    if identity(p)!=before:raise ValueError('changed input')
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
r=json.loads((P/'REVIEW.json').read_bytes());t=json.loads((P/'ACTUAL_SAVED_Q_META_REVIEW_TOOL_RETURNS.json').read_bytes());a=t['actual_success_tool_return']
if r['schema']!='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1'or r['status']!='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY'or r['source_only']is not True or r['all_checks_typed_true']is not True or r['blockers']!=[]or type(r['check_count'])is not int or r['check_count']!=len(r['checks'])!=48:raise ValueError('savedQ finite report contract')
if len(r['checks'])!=48 or len({x['check']for x in r['checks']})!=48 or not all(type(x['passed'])is bool and x['passed']is True for x in r['checks']):raise ValueError('48 typedchecks')
if type(a['exit_code'])is not int or a['exit_code']!=0 or a['chunk_id']!='17e611'or 'session_id'in a:raise ValueError('genuine actualreview closed0')
actual=json.loads(a['output'])
if actual['review_pin']!=pin(P/'REVIEW.json')or actual['check_count']!=48:raise ValueError('actual reviewpin coupling')
for name in ['Root_actual_Q_pin','Root_actual_Q_writer_terminal_pin','Root_actual_Q_writer_Source_pin']:
    if pin(Path(r[name]['path']))!=r[name]:raise ValueError('Root actual source/Q/proof changed')
manifest=P/'MANIFEST.json'
with manifest.open('xb'):pass
files={str(p.relative_to(P)):pin(p)for p in sorted(P.rglob('*'))if p.is_file()and p!=manifest};dirs={'.':identity(P),**{str(p.relative_to(P)):identity(p)for p in sorted(P.rglob('*'))if p.is_dir()}}
m=dict(schema='INDEPENDENT_V25_SAVED_JOINT_HELPER_Q_META_REVIEW_MANIFEST_V1',source_only=True,status=r['status'],check_count=48,complete_members=files,complete_directories=dirs,member_count=len(files),complete_member_bytes=sum(x['size_bytes']for x in files.values()),manifest_self_excluded=True,no_new_qualification_created=True,helper_only_saved_qualification_verified=True,candidate_helper_writer_guard_API_or_numeric_executed=False)
with manifest.open('w')as f:json.dump(m,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
if identity(P)!=dirs['.']or any(pin(P/rel)!=v for rel,v in files.items()):raise ValueError('sealed namespace changed')
print(json.dumps(dict(status='SEALED_PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY',source_only=True,manifest_pin=pin(manifest),review_pin=pin(P/'REVIEW.json'),check_count=48,member_count=len(files),complete_member_bytes=m['complete_member_bytes'],Root_actual_Q_pin=r['Root_actual_Q_pin'],whole_build_qualified=False,whole_INPUT_admitted=False,AAA_accuracy_qualified=False,ABA_admitted=False)))

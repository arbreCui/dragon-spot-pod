from pathlib import Path
import hashlib,json,stat

HERE=Path(__file__).parent
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p):
 before=identity(p);assert stat.S_ISREG(before[2]) and not p.is_symlink()
 h=hashlib.sha256()
 with p.open('rb') as f:
  while part:=f.read(1024*1024):h.update(part)
 assert identity(p)==before
 return {'path':str(p),'sha256':h.hexdigest(),'size_bytes':before[4],'identity':before}
r=json.loads((HERE/'REVIEW.json').read_bytes());t=json.loads((HERE/'actual_SOURCE_audit_tool_returns.json').read_bytes())
assert r['PASS'] is True and r['SOURCE_PASS'] is True and r['check_count']==571 and all(c['PASS'] is True for c in r['checks'])
assert t['actual_audit_tool_return']['chunk_id']=='722a0d' and type(t['actual_audit_tool_return']['exit_code']) is int and t['actual_audit_tool_return']['exit_code']==0 and 'session_id' not in t['actual_audit_tool_return']
members={str(p.relative_to(HERE)):full(p) for p in sorted(HERE.rglob('*')) if p.is_file()}
assert set(members)=={'REVIEW.json','REPORT.txt','review_script.py','actual_SOURCE_audit_tool_returns.json','seal_script.py'}
for expected in r['complete_full_EOF_Source_META_inputs'].values():assert full(Path(expected['path']))==expected
assert r['REVIEW_sha256'] if 'REVIEW_sha256' in r else True
manifest={'schema':'INDEPENDENT_V22B_FINITE_SELF_CAPTURE_SOURCE_REVIEW_SEALED_MANIFEST_V1','SOURCE_PASS':True,'member_count':len(members),'member_bytes':sum(p['size_bytes'] for p in members.values()),'members':members,'complete46SourceMETAinputs_second_EOF_SHA7ID_unchanged':True,'actual_audit_tool_return':t['actual_audit_tool_return'],'writer_executed':False,'new_Q':None,'science_qualified':False}
(HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'review_package':str(HERE),'manifest_pin':full(HERE/'MANIFEST.json'),'review_pin':full(HERE/'REVIEW.json'),'SOURCE_PASS':True,'check_count':571,'all46inputs_second_EOF_unchanged':True,'new_Q':None}))

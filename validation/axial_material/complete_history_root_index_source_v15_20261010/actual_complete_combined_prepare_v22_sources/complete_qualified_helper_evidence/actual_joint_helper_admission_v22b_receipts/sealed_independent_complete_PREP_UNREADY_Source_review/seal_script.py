from pathlib import Path
import json,hashlib,stat
P=Path(__file__).parent
def pin(p):
 s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert stat.S_ISREG(s.st_mode) and not p.is_symlink();h=hashlib.sha256()
 with p.open('rb') as f:
  while c:=f.read(1024*1024):h.update(c)
 ss=p.lstat();assert i==[ss.st_dev,ss.st_ino,ss.st_mode,ss.st_nlink,ss.st_size,ss.st_mtime_ns,ss.st_ctime_ns]
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=i)
r=json.loads((P/'REVIEW.json').read_bytes());t=json.loads((P/'actual_SOURCE_review_tool_returns.json').read_bytes())
assert r['SOURCE_PASS'] is True and r['check_count']==576 and all(c['PASS'] is True for c in r['checks'])
assert t['actual_audit_tool_return']['chunk_id']=='0bdb92' and type(t['actual_audit_tool_return']['exit_code']) is int and t['actual_audit_tool_return']['exit_code']==0 and 'session_id' not in t['actual_audit_tool_return']
for expected in r['all_explicit_complete_Source_and_small_META_fullpins'].values():assert pin(Path(expected['path']))==expected
members={str(p.relative_to(P)):pin(p) for p in sorted(P.rglob('*')) if p.is_file()};assert len(members)==5
m={'schema':'INDEPENDENT_V22_COMPLETE_CANONICAL_GENUINE_PREP_UNREADY_SOURCE_REVIEW_SEALED_MANIFEST_V1','SOURCE_PASS':True,'members':members,'member_count':len(members),'member_bytes':sum(x['size_bytes'] for x in members.values()),'all32explicit_Source_META_inputs_third_fullEOF_SHA7ID_unchanged':True,'actual_audit_tool_return':t['actual_audit_tool_return'],'candidate_binder_executed':False,'business_science_qualified':False}
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'package':str(P),'manifest':pin(P/'MANIFEST.json'),'review':pin(P/'REVIEW.json'),'SOURCE_PASS':True,'check_count':576,'input_count':32,'candidate_binder_executed':False}))


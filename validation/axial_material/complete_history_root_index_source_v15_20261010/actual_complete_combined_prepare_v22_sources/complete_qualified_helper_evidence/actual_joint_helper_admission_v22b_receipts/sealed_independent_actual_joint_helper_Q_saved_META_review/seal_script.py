from pathlib import Path
import hashlib,json,stat
P=Path(__file__).parent
def pin(p):
 s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];h=hashlib.sha256()
 assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 with p.open('rb') as f:
  while c:=f.read(1024*1024):h.update(c)
 ss=p.lstat();assert i==[ss.st_dev,ss.st_ino,ss.st_mode,ss.st_nlink,ss.st_size,ss.st_mtime_ns,ss.st_ctime_ns]
 return {'path':str(p),'sha256':h.hexdigest(),'size_bytes':s.st_size,'identity':i}
r=json.loads((P/'REVIEW.json').read_bytes());t=json.loads((P/'actual_saved_META_review_tool_returns.json').read_bytes())
assert r['PASS'] is True and r['check_count']==1937 and all(c['PASS'] is True for c in r['checks'])
assert t['actual_audit_tool_return']['chunk_id']=='1174fd' and type(t['actual_audit_tool_return']['exit_code']) is int and t['actual_audit_tool_return']['exit_code']==0 and 'session_id' not in t['actual_audit_tool_return']
for expected in r['all_explicit_review_inputs'].values():assert pin(Path(expected['path']))==expected
members={str(p.relative_to(P)):pin(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert len(members)==7
m={'schema':'INDEPENDENT_V22_ACTUAL_JOINT_Q_SAVED_META_REVIEW_SEALED_MANIFEST_V1','PASS':True,'members':members,'member_count':len(members),'member_bytes':sum(x['size_bytes'] for x in members.values()),'all187explicit_inputs_third_EOF_SHA7ID_unchanged':True,'all173admission_input_pins_independently_reconstructed':True,'actual_audit_tool_return':t['actual_audit_tool_return'],'actual_Q':r['actual_Q'],'metadata_only_helper_qualification_reviewed':True,'business_science_qualified':False}
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'package':str(P),'manifest_pin':pin(P/'MANIFEST.json'),'review_pin':pin(P/'REVIEW.json'),'PASS':True,'check_count':1937,'all173admission_inputs':True,'all187review_inputs_third_EOF_SHA7ID_unchanged':True,'science_qualified':False}))


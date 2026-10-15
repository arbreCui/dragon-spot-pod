"""Stdlib SOURCE seal only; no candidate import/compile/evaluation/execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import tarfile

P=Path(__file__).resolve().parent
S=P.with_name(P.name+'_seal_receipt')
EXPECTED={
 'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py':'5fc7f972a8d2c9877375de495fdc502546e0f7ba1702b3c7725d45e50fb30707',
 'complete_observed_old_post_final_XSM_extractor.UNREADY.py':'079e6b9bca0f5e0ab43a41604ccd91c83112a0d040253dcc9101ae47b0efcb69',
 'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py':'5dc8e1743df62bc26dfb6270062f9c23924e23eaedf8e42a2fbd033be47d49af'}
def require(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'unaliased Source/META')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'open Source7ID')
  raw=f.read();require(identity(os.fstat(f.fileno()))==identity(s),'fullEOF Source7ID')
 require(identity(p.lstat())==identity(s),'path Source7ID')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s)),raw
def inventory(root,exclude_manifest=False):
 files=[];dirs=[]
 for p in [root,*sorted(root.rglob('*'))]:
  s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'Source no symlink')
  rel=str(p.relative_to(root))
  if stat.S_ISDIR(s.st_mode):dirs.append(dict(path=str(p),relative_path=rel,identity=identity(s)))
  elif not(exclude_manifest and rel=='MANIFEST.json'):
   q,_=pin(p);files.append(dict(relative_path=rel,**q))
 return files,dirs
def compare_original(view):
 f,d=inventory(Path(view['root']))
 require({x['relative_path']:{k:x[k]for k in('path','sha256','size_bytes','identity')}for x in f}==view['files'],'all original parent files unchanged')
 require({x['relative_path']:x['identity']for x in d}==view['directories'],'all original parent directories unchanged')
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

review=json.loads((P/'AUTHOR_FINITE_COMPLETE_SOURCE_REVIEW.json').read_bytes())
require(review['status']=='AUTHOR_STATIC_SOURCE_CHECKS_COMPLETE_NOT_INDEPENDENT_ADMISSION'and review['source_only']is True,'author honest scope')
require(type(review['check_count'])is int and review['check_count']==len(review['checks'])==49 and all(type(x['passed'])is bool and x['passed']is True for x in review['checks']),'all49 exact typed author checks')
require(all(review[k]is None for k in('actual_candidate_execution','actual_independent_review','actual_binding','new_Q'))and review['scientific_qualification_created']is False,'all unknown actual author fields remain None')
inverse=json.loads((P/'COMPLETE_SIX_HUNK_SOURCE_INVERSE_AND_DEFINITION_PROOF.json').read_bytes())
require(len(inverse['derivations'])==3 and sum(len(x['complete_zero_based_hunks'])for x in inverse['derivations'])==6,'three roles six finite hunks')
archives=json.loads((P/'COMPLETE_ORIGINAL_SOURCE_PEER_AND_TRUE_SEAL_LOSSLESS_ARCHIVES.json').read_bytes())
original=archives['before']['original']
for role,sha in EXPECTED.items():
 q,raw=pin(P/role);require(q['sha256']==sha and q==review['changed_roles'][role],'fixed candidate fullpin')
 item=next(x for x in inverse['derivations']if x['candidate']==role)
 require(item['candidate_pin']==q,'full inverse candidatepin')
 lines=raw.decode().splitlines(keepends=True)
 for h in reversed(item['complete_zero_based_hunks']):
  require(lines[h['new_start0']:h['new_end0']]==h['new_full_lines'],'whole inverse candidate hunk')
  lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
 restored=''.join(lines).encode();original_raw=Path(item['original_pin']['path']).read_bytes()
 require(restored==original_raw and hashlib.sha256(restored).hexdigest()==item['original_pin']['sha256'],'exact original complete Source inverse')
 a,b=ast.parse(original_raw),ast.parse(raw)
 require([ast.dump(n,include_attributes=False)for n in a.body if isinstance(n,(ast.Assign,ast.AnnAssign))]==[ast.dump(n,include_attributes=False)for n in b.body if isinstance(n,(ast.Assign,ast.AnnAssign))],'all original globals caps physics unknown pins unchanged')
 require(item['candidate_definition_count']==item['original_definition_count'],'original definitions count retained')
same=[r for r in original['files']if r!='MANIFEST.json'and r not in EXPECTED]
require(len(same)==191 and all(pin(P/r)[0]['sha256']==original['files'][r]['sha256']and pin(P/r)[0]['size_bytes']==original['files'][r]['size_bytes']for r in same),'all191 other original Source members unchanged')
require((P/'ORIGINAL_COMPLETE_SOURCE_MANIFEST.json').read_bytes()==Path(original['files']['MANIFEST.json']['path']).read_bytes(),'original whole outer manifest preserved exact')
require(archives['before']==archives['after'],'author original beforeafter full inventory match')
for a in archives['archives']:
 require(pin(Path(a['archive_pin']['path']))[0]==a['archive_pin'],'whole Source archivepin fixed')
 seenf={};seend=[]
 with tarfile.open(a['archive_pin']['path'],'r:gz')as tar:
  for m in tar:
   require(m.name not in seenf and m.name not in seend,'unique archive member')
   if m.isdir():seend.append(m.name);continue
   require(m.isfile(),'archive no links/special')
   f=tar.extractfile(m);n=0;h=hashlib.sha256()
   while True:
    chunk=f.read(2**20)
    if not chunk:break
    n+=len(chunk);h.update(chunk)
   seenf[m.name]=dict(sha256=h.hexdigest(),size_bytes=n)
 view=a['original_inventory']
 require(set(seenf)==set(view['files'])and set(seend)==set(view['directories'])and all(seenf[n]=={k:x[k]for k in('sha256','size_bytes')}for n,x in view['files'].items()),'complete lossless archive files dirs manifests EOF SHA')
 compare_original(view)
actual=json.loads((P/'ACTUAL_FINITE_AUTHOR_SOURCE_TOOL_RETURN.json').read_bytes())
t=actual['terminal_tool_return']
require(actual['source_only']is True and actual['closed']is True and actual['actual_tool_terminal_return_observed']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']=='160d41','genuine closed0 Source author witness')
prior_review=json.loads((P/'ORIGINAL_AUTHOR_FINITE_REVIEW_BEFORE_LABEL_CORRECTION.json').read_bytes())
require(json.loads(t['output'])['review']['sha256']==hashlib.sha256((P/'ORIGINAL_AUTHOR_FINITE_REVIEW_BEFORE_LABEL_CORRECTION.json').read_bytes()).hexdigest(),'original author actual output pin preserved before label-only precision correction')
require(prior_review['changed_roles']==review['changed_roles'],'label-only correction did not alter Source candidates')
S.mkdir(exist_ok=False)
manifest=P/'MANIFEST.json'
with manifest.open('xb')as f:f.write(b'')
members,dirs=inventory(P,True)
obj=dict(schema='COMPLETE_CONTEXT_SIX_BLOCKER_FINITE_UNREADY_SOURCE_MANIFEST_V1',source_only=True,status='UNREADY_AUTHOR_FINITE_CORRECTIONS_REQUIRE_INDEPENDENT_REVIEW',root=str(P),member_count=len(members),total_member_bytes=sum(x['size_bytes']for x in members),members=members,directory_count=len(dirs),directories=dirs,author_review_pin=pin(P/'AUTHOR_FINITE_COMPLETE_SOURCE_REVIEW.json')[0],changed_roles={n:pin(P/n)[0]for n in EXPECTED},complete_original194_plus_manifest_preserved=True,complete_original_blocked_peer_and_true_seal_preserved=True,only_six_runtime_Source_hunks=True,actual_independent_review=None,actual_binding=None,new_Q=None,scientific_qualification_created=False)
save(manifest,obj)
again,again_dirs=inventory(P,True)
require(members==again and dirs==again_dirs,'all member and directory fullEOF SHA7ID after actual manifest seal')
mp=pin(manifest)[0]
seal=dict(schema='ACTUAL_COMPLETE_CONTEXT_FINITE_CORRECTION_SOURCE_SEAL_V1',source_only=True,manifest_pin=mp,member_count=len(members),total_member_bytes=obj['total_member_bytes'],directory_count=len(dirs),all_member_full_EOF_SHA7ID_unchanged=True,all_directory_7ID_unchanged=True,author_review_pin=obj['author_review_pin'],changed_roles=obj['changed_roles'],actual_independent_review=None,new_Q=None,scientific_qualification_created=False)
save(S/'SOURCE_SEAL.json',seal)
print(json.dumps(seal,ensure_ascii=False,allow_nan=False),flush=True)

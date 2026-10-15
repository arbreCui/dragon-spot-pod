import ast,difflib,hashlib,io,json,os,stat,tarfile
from pathlib import Path
P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4');D=Path('/private/tmp/axmat_N8_COMPLETE_INDEPENDENT_Source_review_36g28ueh')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
pins={};raws={};objects={};trees={};external={}
def read(p):
 p=Path(p);before=ident(p.lstat());assert p.resolve()==p and stat.S_ISREG(before[2]) and before[3]==1 and 0<=before[4]<=4*2**20
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  assert ident(os.fstat(fd))==before;b=b''
  while True:
   c=os.read(fd,min(65536,4*2**20+1-len(b)))
   if not c:break
   b+=c;assert len(b)<=4*2**20
  assert len(b)==before[4] and os.read(fd,1)==b'' and ident(os.fstat(fd))==before and ident(p.lstat())==before
 finally:os.close(fd)
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before)
b,mp=read(P/'MANIFEST.json');m=parse(b);pins['MANIFEST.json']=mp;raws['MANIFEST.json']=b
assert mp['sha256']=='81d83891b2ee213a45de57868e71667633ae4a126f1cb8603f299d23d2e9bde6' and mp['size_bytes']==152666
wanted={q['relative_path']:q['fullpin'] for q in m['members']};assert len(wanted)==len(m['members'])==239
names=[];dirs={}
for root,sub,n in os.walk(P,followlinks=False):
 root=Path(root);dirs[str(root)]=ident(root.lstat())
 for s in sub:assert not (root/s).is_symlink()
 for s in n:names.append(str((root/s).relative_to(P)))
assert set(names)==set(wanted)|{'MANIFEST.json'} and len(names)==240 and dirs==m['directories'] and len(dirs)==29
for rel,q in sorted(wanted.items()):
 b,actual=read(P/rel);assert actual==q;pins[rel]=actual;raws[rel]=b
 if rel.endswith('.py'):trees[rel]=ast.parse(b,filename=str(P/rel),type_comments=True)
 elif rel.endswith('.json'):objects[rel]=parse(b)
assert len(trees)==96 and sum(q['size_bytes'] for q in pins.values())==10697989
for p in sorted(P.with_name(P.name+'_seal_receipt').iterdir()):
 b,q=read(p);external[p.name]=q
 if p.suffix=='.json':parse(b)
retain=objects['COMPLETE_ORIGINAL_N7_MEMBER_RETENTION.Source_META.json'];b,q=read(retain['mother_manifest_pin']['path']);assert q==retain['mother_manifest_pin'];mother=parse(b);external['original_N7_manifest']=q
mothermembers={row['relative_path']:row['fullpin'] for row in mother['members']} if isinstance(mother['members'],list) else mother['members']
assert len(retain['members'])==len(mothermembers)==181
retention_results=[]
for row in retain['members']:
 old=row['mother_original_fullpin'];cur=row['actual_complete_retained_original_fullpin'];rel=row['relative_path']
 assert old==mothermembers[rel];currentrel=str(Path(cur['path']).relative_to(P));assert pins[currentrel]==cur and cur['sha256']==old['sha256'] and cur['size_bytes']==old['size_bytes']
 derivative=row['actual_current_derivative_fullpin']
 if derivative is not None:assert pins[str(Path(derivative['path']).relative_to(P))]==derivative
 retention_results.append(dict(original_member=rel,original_fullpin=old,current_retained_fullpin=cur,current_derivative_fullpin=derivative,original_whole_bytes_retained=True))
inv=objects['COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json'];role_inverses={};independent={};diff=[]
for row in inv['roles']:
 rel=row['role_basename'];assert row['new_complete_Source_pin']==pins[rel]
 oldrow=next(r for r in retention_results if r['original_member']==rel);oldrel=str(Path(oldrow['current_retained_fullpin']['path']).relative_to(P));old=raws[oldrel].decode();current=raws[rel].decode();lines=current.splitlines(keepends=True)
 for h in reversed(row['hunks']):
  start=h['new_start_line0'];end=h['new_end_line0'];assert ''.join(lines[start:end])==h['new_text'];lines[start:end]=h['old_text'].splitlines(keepends=True)
 recovered=''.join(lines);assert recovered==old and ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(trees[oldrel],include_attributes=False)
 a=old.splitlines(keepends=True);z=current.splitlines(keepends=True);ops=[t for t in difflib.SequenceMatcher(None,a,z,autojunk=False).get_opcodes() if t[0]!='equal'];rebuild=z[:]
 for tag,i,j,k,l in reversed(ops):rebuild[k:l]=a[i:j]
 assert ''.join(rebuild)==old
 independent[rel]=[dict(tag=tag,original_lines0=[i,j],current_lines0=[k,l],old=''.join(a[i:j]),new=''.join(z[k:l]))for tag,i,j,k,l in ops]
 diff.append('ROLE '+rel+'\n'+''.join(difflib.unified_diff(a,z,fromfile=oldrel,tofile=rel)))
 role_inverses[rel]=dict(current_fullpin=pins[rel],retained_parent_fullpin=pins[oldrel],whole_original_byte_AST_inverse=True,author_hunks=len(row['hunks']),independent_hunks=len(ops),independent_full_diff_reverse=True)
# Whole native Source archive content, no extraction, build, or native API.
index=objects['COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json'];nativewanted={x['relative_path']:x['full_original_Source_pin'] for x in index['members']};assert len(nativewanted)==len(index['members'])==1365
archive=tarfile.open(fileobj=io.BytesIO(raws['COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz']),mode='r:gz');members=archive.getmembers();assert len(members)==1365 and {x.name for x in members}==set(nativewanted)
native_results={};total=0
for member in members:
 assert member.isfile() and not Path(member.name).is_absolute() and '..' not in Path(member.name).parts and member.size==nativewanted[member.name]['size_bytes'] and member.size<=200000
 stream=archive.extractfile(member);b=stream.read(member.size+1);assert len(b)==member.size and stream.read(1)==b'';stream.close();h=hashlib.sha256(b).hexdigest();assert h==nativewanted[member.name]['sha256'];total+=len(b)
 native_results[member.name]=dict(sha256=h,size_bytes=len(b),full_original_Source_pin=nativewanted[member.name],complete_archive_Source_EOF_verified=True)
archive.close();assert total==12545229
contract={role:pins[rel] for role,rel in m['required_author_Source_roles'].items()};assert len(contract)==21 and contract['qualified_source_manifest']==mp
scope=objects['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'];assert scope['required_author_Source_roles']==m['required_author_Source_roles']
result=dict(source_only=True,all240_files_full_EOF_SHA_7ID=True,all29_directories_full_7ID=True,all96_Python_full_AST=True,strict_JSON_count=len(objects)+1,all_complete_source_member_pins=pins,complete_source_directory_7ID=dirs,candidate_manifest_pin=mp,actual_author_Source_contract=contract,original181_N7_whole_bytes_retention=retention_results,complete4role_original_whole_byte_AST_inverses=role_inverses,native1365_Source_archive_complete_member_results=native_results,native_total_original_Source_bytes=total,actual_sibling_receipt_pins=external,candidate_guard_API_control_PS_lsof_wait_poll_compile_material_numeric_executed=False)
(D/'COMPLETE_ALL_SOURCE_EOF_AST_RETENTION_NATIVE_ARCHIVE_AND_INVERSE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(D/'INDEPENDENT_COMPLETE_FOUR_ROLE_WHOLE_SOURCE_INVERSE.json').write_text(json.dumps(dict(source_only=True,independently_derived_full_current_to_retained_N7_source=True,roles=independent),indent=2)+'\n')
(D/'INDEPENDENT_ALL_FOUR_WHOLE_SOURCE_DIFFS.txt').write_text('\n\n'.join(diff))
print(json.dumps(dict(source_only=True,manifest_pin=mp,complete_files=240,complete_dirs=29,full_Python_AST=96,all_JSON_strict=len(objects)+1,original_N7_Source_bytes_retained=181,all_current_four_whole_original_byte_AST_inverses=True,native_archive_Source_members=1365,native_archive_complete_Source_bytes=total,author_Source_contract_fullpins=21,candidate_or_API_or_business_executed=False),sort_keys=True))

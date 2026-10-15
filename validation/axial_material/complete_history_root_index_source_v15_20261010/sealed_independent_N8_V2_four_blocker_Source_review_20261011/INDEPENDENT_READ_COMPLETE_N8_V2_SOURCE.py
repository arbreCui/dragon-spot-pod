"""Independent finite Source read. Never imports or executes candidate roles."""
import ast,difflib,hashlib,io,json,os,stat,tarfile
from pathlib import Path
P=Path('/private/tmp/axmat_N8_four_blocker_minimal_complete_UNREADY_Source_ekd9i0c_')
OLD=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
D=Path('/private/tmp/axmat_N8_V2_four_blocker_INDEPENDENT_review_4prv7dk5')
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
assert mp['sha256']=='cdaed7cd53d2b22ec3891a7f82064eea9505ae974f8ac284e6d76fe5ae7ae267' and mp['size_bytes']==187186
assert m['schema']=='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1'
wanted={q['relative_path']:q['fullpin'] for q in m['members']};assert len(wanted)==len(m['members'])==287
names=[];dirs={}
for root,sub,n in os.walk(P,followlinks=False):
 root=Path(root);dirs[str(root)]=ident(root.lstat())
 for s in sub:assert not (root/s).is_symlink()
 for s in n:names.append(str((root/s).relative_to(P)))
assert set(names)==set(wanted)|{'MANIFEST.json'} and len(names)==288 and dirs==m['directories'] and len(dirs)==33
for rel,q in sorted(wanted.items()):
 b,actual=read(P/rel);assert actual==q;pins[rel]=actual;raws[rel]=b
 if rel.endswith('.py'):trees[rel]=ast.parse(b,filename=str(P/rel),type_comments=True)
 elif rel.endswith('.json'):objects[rel]=parse(b)
assert len(trees)==113 and sum(q['size_bytes'] for q in pins.values())==14124000
siblings={}
for p in sorted(P.with_name(P.name+'_seal_receipt').iterdir()):
 b,q=read(p);external[p.name]=q
 if p.suffix=='.json':siblings[p.name]=parse(b)
assert external['ACTUAL_SOURCE_SEAL_TOOL_RETURN.json']['sha256']=='9df69b8ca798714be5d0864e672800387ee2fee0c74f250debf655ffcfafa8d1'
assert external['ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json']['sha256']=='f474f22686d1c72713e54fe040b0523a3384c0d43afd7a76561b6fb13b37d4a4'
for name in('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'):
 w=siblings[name];t=w['terminal_tool_return'];assert type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and w['closed']is True and w['observed_terminal']is True and w['session_repolled_after_close']is False and w['actual_terminal_chunk']==t['chunk_id']
# Whole sealed N8 parent and original N7 retained transitive Source, never payloads.
revision=objects['CURRENT_N8_V2_SOURCE_REVISION_CONTRACT.UNREADY.json'];b,q=read(OLD/'MANIFEST.json');oldm=parse(b);assert q==revision['parent_manifest_pin'];external['original_N8_manifest']=q
oldwanted={r['relative_path']:r['fullpin']for r in oldm['members']};assert len(oldwanted)==239
oldnames=[];olddirs={};oldraw={};oldpins={}
for root,sub,files in os.walk(OLD,followlinks=False):
 root=Path(root);olddirs[str(root)]=ident(root.lstat())
 for s in sub:assert not (root/s).is_symlink()
 oldnames.extend(str((root/s).relative_to(OLD))for s in files)
assert olddirs==oldm['directories']and set(oldnames)==set(oldwanted)|{'MANIFEST.json'}
changed=set(revision['changed_complete_Source_roles']);assert len(changed)==8
n8retained=[]
for rel,expected in sorted(oldwanted.items()):
 raw,q=read(OLD/rel);assert q==expected;oldraw[rel]=raw;oldpins[rel]=q
 if rel in changed:
  backup='PREVIOUS_SEALED_N8_FOUR_BLOCKER_FAILURE_PROVENANCE/ORIGINAL_COMPLETE_CHANGED_ROLE_SOURCE/'+rel
  assert raws[backup]==raw;retained_pin=pins[backup]
 else:assert raws[rel]==raw;retained_pin=pins[rel]
 n8retained.append(dict(original_member=rel,original_fullpin=q,current_retained_fullpin=retained_pin,original_whole_bytes_retained=True))
retain=objects['COMPLETE_ORIGINAL_N7_MEMBER_RETENTION.Source_META.json'];b,q=read(retain['mother_manifest_pin']['path']);assert q==retain['mother_manifest_pin'];mother=parse(b);external['original_N7_manifest']=q
mothermembers={row['relative_path']:row['fullpin'] for row in mother['members']} if isinstance(mother['members'],list) else mother['members'];assert len(retain['members'])==len(mothermembers)==181
retention_results=[]
for row in retain['members']:
 old=row['mother_original_fullpin'];rel=row['relative_path'];assert old==mothermembers[rel];raw,actual=read(old['path']);assert actual==old
 parentretained=row['actual_complete_retained_original_fullpin'];currentrel=str(Path(parentretained['path']).relative_to(OLD));assert oldpins[currentrel]==parentretained and raws[currentrel]==raw
 derivative=row['actual_current_derivative_fullpin'];current_derivative=None
 if derivative is not None:
  derrel=str(Path(derivative['path']).relative_to(OLD));assert oldpins[derrel]==derivative;current_derivative=pins[derrel]
 retention_results.append(dict(original_member=rel,original_fullpin=old,current_retained_fullpin=pins[currentrel],current_derivative_fullpin=current_derivative,original_whole_bytes_retained=True))
# Actual current inverses, not retained historical proof rows.
def inverse_result(inv,expected_count,resolve_old):
 results={};independent={};diff=[]
 assert len(inv['roles'])==expected_count
 for row in inv['roles']:
  rel=row['role_basename'];assert row['new_complete_Source_pin']==pins[rel];old,oldpin,oldlabel=resolve_old(row);current=raws[rel].decode();lines=current.splitlines(keepends=True)
  for h in reversed(row['hunks']):
   start=h['new_start_line0'];end=h['new_end_line0'];assert ''.join(lines[start:end])==h['new_text'];lines[start:end]=h['old_text'].splitlines(keepends=True)
  recovered=''.join(lines);assert recovered==old
  if rel.endswith('.py'):assert ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
  else:assert parse(recovered)==parse(old)
  a=old.splitlines(keepends=True);z=current.splitlines(keepends=True);ops=[t for t in difflib.SequenceMatcher(None,a,z,autojunk=False).get_opcodes()if t[0]!='equal'];rebuild=z[:]
  for tag,i,j,k,l in reversed(ops):rebuild[k:l]=a[i:j]
  assert ''.join(rebuild)==old
  independent[rel]=[dict(tag=tag,original_lines0=[i,j],current_lines0=[k,l],old=''.join(a[i:j]),new=''.join(z[k:l]))for tag,i,j,k,l in ops]
  diff.append('ROLE '+rel+'\n'+''.join(difflib.unified_diff(a,z,fromfile=oldlabel,tofile=rel)))
  results[rel]=dict(current_fullpin=pins[rel],retained_parent_fullpin=oldpin,whole_original_byte_AST_inverse=True,author_hunks=len(row['hunks']),independent_hunks=len(ops),independent_full_diff_reverse=True)
 return results,independent,diff
inv8=objects['COMPLETE_N8_V2_ALL_CHANGED_ROLE_BYTE_AST_INVERSE.json'];assert set(r['role_basename']for r in inv8['roles'])==changed
assert pins['COMPLETE_N8_V2_ALL_CHANGED_ROLE_BYTE_AST_INVERSE.json']['sha256']=='a6e3e6a19f0231a8b81bd147c82d2775fb86e994478995be41cdbdacb893f530'
def resolve_n8(row):
 rel=row['role_basename'];backup=str(Path(row['retained_original_fullpin']['path']).relative_to(P));assert oldpins[rel]==row['parent_original_fullpin']and pins[backup]==row['retained_original_fullpin']and raws[backup]==oldraw[rel]
 return raws[backup].decode(),pins[backup],backup
n8inverses,ind8,diff8=inverse_result(inv8,8,resolve_n8)
inv4=objects['COMPLETE_N8_V2_CURRENT_FOUR_ROLE_TO_N7_BYTE_AST_INVERSE.json'];assert pins['COMPLETE_N8_V2_CURRENT_FOUR_ROLE_TO_N7_BYTE_AST_INVERSE.json']['sha256']=='985ac98b83dceec9f7421b7107eab177fb4263d20506cb6b8a218198cc294f00'
def resolve_n7(row):
 rel=row['role_basename'];record=next(r for r in retention_results if r['original_member']==rel);assert record['original_fullpin']==row['parent_original_fullpin'];oldpin=record['current_retained_fullpin'];oldlabel=str(Path(oldpin['path']).relative_to(P))
 return raws[oldlabel].decode(),oldpin,oldlabel
role_inverses,ind4,diff4=inverse_result(inv4,4,resolve_n7)
# Every original archive member read to EOF, SHA checked, no extraction/build.
index=objects['COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json'];nativewanted={x['relative_path']:x['full_original_Source_pin']for x in index['members']};assert len(nativewanted)==len(index['members'])==1365
archive=tarfile.open(fileobj=io.BytesIO(raws['COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz']),mode='r:gz');members=archive.getmembers();assert len(members)==1365 and {x.name for x in members}==set(nativewanted)
native_results={};total=0
for member in members:
 assert member.isfile()and not Path(member.name).is_absolute()and '..'not in Path(member.name).parts and member.size==nativewanted[member.name]['size_bytes']and member.size<=200000
 stream=archive.extractfile(member);b=stream.read(member.size+1);assert len(b)==member.size and stream.read(1)==b'';stream.close();h=hashlib.sha256(b).hexdigest();assert h==nativewanted[member.name]['sha256'];total+=len(b)
 native_results[member.name]=dict(sha256=h,size_bytes=len(b),full_original_Source_pin=nativewanted[member.name],complete_archive_Source_EOF_verified=True)
archive.close();assert total==12545229
contract={role:pins[rel]for role,rel in m['required_author_Source_roles'].items()};assert len(contract)==21 and contract['qualified_source_manifest']==mp
scope=objects['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'];assert scope['required_author_Source_roles']==m['required_author_Source_roles']==revision['required_complete_author_Source_roles'];assert contract==siblings['DELIVERY.json']['actual_author_Source_contract']
assert {k:v for k,v in contract.items()if k!='qualified_source_manifest'}==revision['current_role_Source_pins_before_manifest']
failed=Path(revision['actual_failed_independent_report_pin']['path']);failedraw,failedpin=read(failed);assert failedpin==revision['actual_failed_independent_report_pin'];failedreview=parse(failedraw);assert failedreview['status']=='SOURCE_ONLY_FAIL_BLOCKED_NO_EXECUTION_OR_SCIENCE'and failedreview['check_count']==102 and sum(c['passed']is True for c in failedreview['checks'])==98 and len(failedreview['blockers'])==4
for k in('actual_failed_independent_Source_verdict_tool_pin','actual_failed_independent_manifest_pin','actual_failed_independent_seal_pin','actual_failed_independent_postseal_pin'):
 raw,q=read(revision[k]['path']);assert q==revision[k]
 if k.endswith('verdict_tool_pin'):t=parse(raw)['terminal_tool_return'];assert type(t['exit_code'])is int and t['exit_code']==1 and 'session_id'not in t
result=dict(source_only=True,all288_files_full_EOF_SHA_7ID=True,all33_directories_full_7ID=True,all113_Python_full_AST=True,strict_JSON_count=len(objects)+1,all_complete_source_member_pins=pins,complete_source_directory_7ID=dirs,candidate_manifest_pin=mp,actual_author_Source_contract=contract,original239_N8_whole_bytes_retention=n8retained,original181_N7_whole_bytes_retention=retention_results,complete8role_to_N8_whole_byte_AST_inverses=n8inverses,complete4role_original_whole_byte_AST_inverses=role_inverses,native1365_Source_archive_complete_member_results=native_results,native_total_original_Source_bytes=total,actual_sibling_receipt_pins=external,actual_failed_independent_review_pin=failedpin,candidate_guard_API_control_PS_lsof_wait_poll_compile_material_numeric_executed=False)
(D/'COMPLETE_ALL_SOURCE_EOF_AST_RETENTION_NATIVE_ARCHIVE_AND_INVERSE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(D/'INDEPENDENT_COMPLETE_EIGHT_AND_FOUR_ROLE_WHOLE_SOURCE_INVERSES.json').write_text(json.dumps(dict(source_only=True,independently_derived_current_to_N8=ind8,independently_derived_current_to_N7=ind4),indent=2)+'\n')
(D/'INDEPENDENT_ALL_EIGHT_AND_FOUR_WHOLE_SOURCE_DIFFS.txt').write_text('\n\n'.join(diff8+diff4))
print(json.dumps(dict(source_only=True,manifest_pin=mp,complete_files=288,complete_dirs=33,full_Python_AST=113,all_JSON_strict=len(objects)+1,original_N8_Source_bytes_retained=239,original_N7_Source_bytes_retained=181,all_current_eight_and_four_whole_original_byte_AST_inverses=True,native_archive_Source_members=1365,native_archive_complete_Source_bytes=total,author_Source_contract_fullpins=21,candidate_or_API_or_business_executed=False),sort_keys=True))

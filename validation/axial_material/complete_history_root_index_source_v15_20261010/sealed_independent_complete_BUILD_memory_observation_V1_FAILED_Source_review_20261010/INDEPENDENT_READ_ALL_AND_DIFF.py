import ast,difflib,hashlib,json,os,stat
from pathlib import Path
P=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
D=Path('/private/tmp/axmat_V25_memory_observation_INDEPENDENT_review_ZgGEhb')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def reject_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
pins={}; texts={}; objects={}; trees={}
def read(p):
 before=ident(p.lstat());assert stat.S_ISREG(before[2]) and before[3]==1
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ident(os.fstat(fd))==before
  b=b''
  while True:
   c=os.read(fd,65536)
   if not c:break
   b+=c
  assert os.read(fd,1)==b'' and len(b)==before[4] and ident(os.fstat(fd))==before and ident(p.lstat())==before
 finally:os.close(fd)
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before)
b,m=read(P/'MANIFEST.json');mf=json.loads(b,object_pairs_hook=reject_pairs);pins['MANIFEST.json']=m
actual_files=[];actual_dirs=[]
for root,dirs,files in os.walk(P,followlinks=False):
 root=Path(root);actual_dirs.append(str(root.relative_to(P)))
 for dirname in dirs:assert not (root/dirname).is_symlink()
 for name in files:actual_files.append(str((root/name).relative_to(P)))
assert set(actual_files)==set(mf['members'])|{'MANIFEST.json'} and len(actual_files)==68
assert set(actual_dirs)==set(mf['directories']) and len(actual_dirs)==6
for rel in actual_dirs:assert ident((P/rel).lstat())==mf['directories'][rel]
for rel in sorted(mf['members']):
 b,q=read(P/rel);assert q==mf['members'][rel];pins[rel]=q
 t=b.decode('utf-8');texts[rel]=t
 if rel.endswith('.py'):trees[rel]=ast.parse(t,filename=str(P/rel),type_comments=True)
 elif rel.endswith('.json'):objects[rel]=json.loads(t,object_pairs_hook=reject_pairs)
assert m['sha256']=='fff5b15ae51888bd3ff310597a44ce2381ecdd0f2bb858ee12c4c0395f6385bc' and m['size_bytes']==36168
assert sum(q['size_bytes'] for rel,q in pins.items() if rel!='MANIFEST.json')==3925987
external={}
for p in sorted(P.with_name(P.name+'_seal_receipt').iterdir()):
 b,q=read(p);external[p.name]=q
 if p.suffix=='.py':ast.parse(b.decode(),filename=str(p),type_comments=True)
 elif p.suffix=='.json':json.loads(b,object_pairs_hook=reject_pairs)
rootmeta=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_Python_resource_dependency_and_waitid_capability_Source_META.json')
b,q=read(rootmeta);external['actual_Root_resource_dependency_Source_META']=q;json.loads(b,object_pairs_hook=reject_pairs)
inv=objects['COMPLETE_SOURCE_INVERSES.json'];roles=inv['role_current_paths'];assert len(roles)==14
role_results={};diffs=[];independent_inverse={}
for role,rel in roles.items():
 oldrel='ORIGINAL_PARENT_SOURCE/'+(role+'.full.py' if role.endswith('.py') else role+'.full.py')
 old=texts[oldrel];new=texts[rel]
 expected=inv['original_parent_fullpins'][role];assert hashlib.sha256(old.encode()).hexdigest()==expected['sha256'] and len(old.encode())==expected['size_bytes']
 restored=new
 for patch in reversed(inv['exact_finite_transforms'][role]):
  assert type(patch['count']) is int and patch['count']>0 and restored.count(patch['new'])==patch['count'],(role,patch['label'],'reverse_count')
  restored=restored.replace(patch['new'],patch['old'])
 assert restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(trees[oldrel],include_attributes=False)
 normalized=old.replace('v25-poststage-temporaries','v25-memory-observation').replace('v25_poststage_temporaries','v25_memory_observation')
 sm=difflib.SequenceMatcher(None,normalized.splitlines(keepends=True),new.splitlines(keepends=True),autojunk=False)
 opcodes=[x for x in sm.get_opcodes() if x[0]!='equal'];a=normalized.splitlines(keepends=True);z=new.splitlines(keepends=True)
 rebuild=z[:];patches=[]
 for tag,i,j,k,l in reversed(opcodes):rebuild[k:l]=a[i:j]
 assert ''.join(rebuild)==normalized
 for tag,i,j,k,l in opcodes:patches.append(dict(tag=tag,original_lines=[i+1,j],candidate_lines=[k+1,l],old=''.join(a[i:j]),new=''.join(z[k:l])))
 independent_inverse[role]=patches
 diffs.append('ROLE '+role+'\n'+''.join(difflib.unified_diff(a,z,fromfile=oldrel,tofile=rel,n=3)))
 def defs(tree):return {(type(n).__name__,n.name,n.lineno):ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
 od=defs(ast.parse(normalized));nd=defs(trees[rel]);na={}
 for key,value in nd.items():na.setdefault((key[0],key[1]),[]).append(value)
 unchanged=[];changed=[]
 for key,value in od.items():
  (unchanged if value in na.get((key[0],key[1]),[]) else changed).append(dict(kind=key[0],name=key[1],original_line=key[2]))
 role_results[role]=dict(candidate_pin=pins[rel],parent_copy_pin=pins[oldrel],parent_advertised_pin=expected,full_inverse_byte_equal=True,full_inverse_AST_equal=True,independent_diff_inverse_equal=True,independent_hunk_count=len(opcodes),unchanged_original_definitions=unchanged,changed_original_definitions=changed,original_definition_count=len(od),candidate_definition_count=len(nd))
(D/'INDEPENDENT_ALL_14_ROLE_DIFFS.txt').write_text('\n\n'.join(diffs))
(D/'INDEPENDENT_WHOLE_SOURCE_INVERSES.json').write_text(json.dumps(dict(source_only=True,independently_derived_from_full_source=True,namespace_normalization_only=['v25-poststage-temporaries -> v25-memory-observation','v25_poststage_temporaries -> v25_memory_observation'],roles=independent_inverse),indent=2,ensure_ascii=False)+'\n')
result=dict(source_only=True,manifest_pin=m,all_68_files_EOF_SHA_7ID_verified=True,all_6_directory_7ID_verified=True,python_AST_count=len(trees),json_count=len(objects)+1,complete_members=pins,external_small_receipt_pins=external,role_results=role_results,candidate_or_business_executed=False)
(D/'COMPLETE_READ_AND_INVERSE_RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(source_only=True,manifest_pin=m,complete_files=len(pins),complete_dirs=len(actual_dirs),python_AST_count=len(trees),json_count=len(objects)+1,roles=len(roles),all_complete_EOF_SHA_7ID_and_inverses=True,diff_bytes=(D/'INDEPENDENT_ALL_14_ROLE_DIFFS.txt').stat().st_size,changed_definitions={r:[v['name'] for v in q['changed_original_definitions']] for r,q in role_results.items()},candidate_or_business_executed=False),sort_keys=True))

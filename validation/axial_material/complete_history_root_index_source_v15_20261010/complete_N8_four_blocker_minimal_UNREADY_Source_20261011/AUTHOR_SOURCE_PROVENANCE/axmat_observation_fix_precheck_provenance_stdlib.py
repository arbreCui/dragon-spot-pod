from pathlib import Path
import ast,json,hashlib,difflib,shutil
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_four_contract_finite_UNREADY_Source_fix_vz42_t14');O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
q=P/'complete_observation_BUILD5_AB_runtime.UNREADY.py';s=q.read_text();old="module_copy_pins=[]\n        if recipe['module_copy']:\n            modules=native/recipe['lib_module']\n            for p in folder.glob('*.mod'):"
new="module_copy_pins=[]\n        if recipe['module_copy']:\n            modules=native/recipe['lib_module'];generated_modules=list(folder.glob('*.mod'))\n            require(component!='Utilib'or bool(generated_modules),'original Utilib unguarded cp *.mod requires actual modules')\n            for p in generated_modules:"
assert s.count(old)==1;s=s.replace(old,new);ast.parse(s);q.write_text(s)
q=P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json';j=json.loads(q.read_bytes());proof=[]
for previous in j['source_derivations']:
 name=previous['source_member'];old=(O/name).read_bytes();new=(P/name).read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
 for tag,i,k,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
  if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=k,new_start0=a,new_end0=b,old_full_lines=ol[i:k],new_full_lines=nl[a:b]))
 inv=list(nl)
 for h in reversed(hs):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(inv).encode()==old
 proof.append(dict(source_member=name,original_sha256=hashlib.sha256(old).hexdigest(),fixed_sha256=hashlib.sha256(new).hexdigest(),complete_full_inverse_hunks=hs,whole_Source_inverse_to_original_frozen_member_equal=True))
j['source_derivations']=proof;q.write_text(json.dumps(j,indent=2)+'\n')
d=P/'AUTHOR_SOURCE_PROVENANCE';d.mkdir()
for p in('/private/tmp/axmat_observation_four_contract_Source_fix_author_stdlib.py','/private/tmp/axmat_observation_final_four_blocker_fix_finish_stdlib.py',__file__):
 shutil.copy2(p,d/Path(p).name)
print(json.dumps(dict(status='ALL_FOUR_TRUE_SOURCE_FIXES_READY_FOR_FINAL_AUTHOR_SOURCE_CHECK_ONLY',changed_original_members=len(proof),full_byte_inverse_hunks=sum(len(r['complete_full_inverse_hunks'])for r in proof),actual_native_execution=None)))

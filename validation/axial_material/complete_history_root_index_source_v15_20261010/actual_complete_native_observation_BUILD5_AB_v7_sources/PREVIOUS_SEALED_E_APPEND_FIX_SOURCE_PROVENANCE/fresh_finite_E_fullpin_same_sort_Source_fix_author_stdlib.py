from pathlib import Path
import json,hashlib,ast,difflib,shutil,tempfile
N=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_append_dir_identity_finite_UNREADY_Source_fix_kn1wol83');O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq');P=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_',dir='/private/tmp'))
for p in N.iterdir():
 if p.is_dir():shutil.copytree(p,P/p.name,copy_function=shutil.copy2)
 else:shutil.copy2(p,P/p.name)
d=P/'PREVIOUS_SEALED_E_APPEND_FIX_SOURCE_PROVENANCE';d.mkdir()
for name in('MANIFEST.json','AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json','ACTUAL_AUTHOR_FIXED_SOURCE_CHECK_TOOL_RETURNS.json'):(P/name).rename(d/name)
for name in('AUTHOR_COMPLETE_SOURCE_SEAL_REPORT.json','ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','FULL_SOURCE_POSTSEAL_VERIFICATION.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'):shutil.copy2(Path(str(N)+'_seal_receipt')/name,d/('TRUE_SIBLING_'+name))
shutil.copy2(N/'Root_observation_postclose_META_writer.UNREADY.py',d/'PREVIOUS_FULL_ROOT_POSTCLOSE_SOURCE.py')
q=P/'Root_observation_postclose_META_writer.UNREADY.py';old=q.read_text();a="after_views['receipts']['files']==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])";b="sorted(after_views['receipts']['files'],key=lambda p:p['path'])==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])";assert old.count(a)==1;new=old.replace(a,b);ast.parse(new);q.write_text(new)
q=P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json';j=json.loads(q.read_text().replace(str(N),str(P)));j['postclose_E_fullpin_compare_sort']='Both actual after-E fullpin list and complete expected original-E plus own-manifest fullpin list use exact same full-string path key for comparison. Original tree fullpin views retain original Path traversal order. No snapshot, event, native record or physics ordering changed.';q.write_text(json.dumps(j,indent=2)+'\n')
q=P/'author_fixed_finite_complete_Source_check_stdlib_only.py';s=q.read_text().replace(str(N),str(P));needle="report=dict(schema='AUTHOR_FINITE_COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_SOURCE_CHECK_V1'";s=s.replace(needle,"check('postclose E actual and expected complete fullpins share exact full string path sort key without changing original tree or snapshot order',\"sorted(after_views['receipts']['files'],key=lambda p:p['path'])==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])\"in post)\n"+needle);ast.parse(s);q.write_text(s)
q=P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json';j=json.loads(q.read_bytes());proof=[]
for r in j['source_derivations']:
 name=r['source_member'];old=(O/name).read_bytes();new=(P/name).read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
 for tag,i,k,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
  if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=k,new_start0=a,new_end0=b,old_full_lines=ol[i:k],new_full_lines=nl[a:b]))
 inv=list(nl)
 for h in reversed(hs):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(inv).encode()==old;proof.append(dict(source_member=name,original_sha256=hashlib.sha256(old).hexdigest(),fixed_sha256=hashlib.sha256(new).hexdigest(),complete_full_inverse_hunks=hs,whole_Source_inverse_to_original_frozen_member_equal=True))
j.update(source_derivations=proof,E_postclose_actual_expected_complete_fullpin_same_path_sort_Source_correction=True,previous_sealed_E_append_manifest_sha256='864fd7b9c1640a547cd636574b944eb89f4715cd22cea12f30e77f1de71f86d1');q.write_text(json.dumps(j,indent=2)+'\n')
old=(N/'Root_observation_postclose_META_writer.UNREADY.py').read_bytes();new=(P/'Root_observation_postclose_META_writer.UNREADY.py').read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
for tag,i,k,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
 if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=k,new_start0=a,new_end0=b,old_full_lines=ol[i:k],new_full_lines=nl[a:b]))
inv=list(nl)
for h in reversed(hs):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
assert ''.join(inv).encode()==old and len(hs)==1
paths=[Path('/a/file.json'),Path('/a-.json')];ordering=dict(Path_component_order=[str(p)for p in sorted(paths)],full_string_order=sorted(map(str,paths)));assert ordering['Path_component_order']!=ordering['full_string_order']
(d/'FULL_ROOT_POSTCLOSE_SINGLE_HUNK_SAME_SORT_SOURCE_INVERSE.json').write_text(json.dumps(dict(source_only=True,original_full_Source_sha256=hashlib.sha256(old).hexdigest(),corrected_full_Source_sha256=hashlib.sha256(new).hexdigest(),whole_byte_inverse_hunks=hs,whole_inverse_equals_previous_sealed_complete_Source=True,pure_stdlib_no_fixture_Path_sort_metadata=ordering,independent_author_reported_sort_reproduction_true_terminal_chunk='1938da',actual_new_independent_Source_review=None,actual_Root_Source_admission=None,actual_runtime=None,scientific_qualification_created=False),indent=2)+'\n')
shutil.copy2(__file__,d/'fresh_finite_E_fullpin_same_sort_Source_fix_author_stdlib.py');Path('/private/tmp/axmat_observation_E_fullpin_sort_fix_author_current_path.txt').write_text(str(P)+'\n')
print(json.dumps(dict(status='FRESH_SOURCE_ONLY_E_ACTUAL_EXPECTED_FULLPIN_SAME_SORT_FIX_UNSEALED',fresh_Source=str(P),complete_postclose_delta_hunks=1,original_MF_still_immutable=True,actual_new_native_execution=None)))

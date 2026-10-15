from pathlib import Path
import json,hashlib,ast,difflib,shutil,tempfile
N=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_four_contract_finite_UNREADY_Source_fix_vz42_t14');O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
P=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_BUILD5_AB_E_append_dir_identity_finite_UNREADY_Source_fix_',dir='/private/tmp'))
for p in N.iterdir():
 if p.is_dir():shutil.copytree(p,P/p.name,copy_function=shutil.copy2)
 else:shutil.copy2(p,P/p.name)
d=P/'PREVIOUS_SEALED_FIX_SOURCE_PROVENANCE';d.mkdir()
for name in('MANIFEST.json','AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json','ACTUAL_AUTHOR_FIXED_SOURCE_CHECK_TOOL_RETURNS.json'):
 (P/name).rename(d/name)
for name in('AUTHOR_COMPLETE_SOURCE_SEAL_REPORT.json','ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','FULL_SOURCE_POSTSEAL_VERIFICATION.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'):
 shutil.copy2(Path(str(N)+'_seal_receipt')/name,d/('TRUE_SIBLING_'+name))
shutil.copy2(N/'Root_observation_postclose_META_writer.UNREADY.py',d/'PREVIOUS_FULL_ROOT_POSTCLOSE_SOURCE.py')
q=P/'Root_observation_postclose_META_writer.UNREADY.py';old=q.read_text();assert old.count("current[:4]==identity[:4]")==1;new=old.replace("current[:4]==identity[:4]","current[:3]==identity[:3]").replace("only E own append directory stat timestamps/size may change","only E own append directory nlink/size/timestamps may change; dev/inode/mode stay identical");ast.parse(new);q.write_text(new)
q=P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json';raw=q.read_text().replace(str(N),str(P));j=json.loads(raw);j['postclose_E_append_parent_directory_identity_contract']='Darwin/APFS append may change directory st_nlink/size/mtime/ctime; dev/inode/mode remain exactly stable. E exact files gain own manifest only, complete directory set unchanged, all other E dirs full7ID unchanged. H/O/C/D views stay exact.';q.write_text(json.dumps(j,indent=2)+'\n')
q=P/'author_fixed_finite_complete_Source_check_stdlib_only.py';s=q.read_text().replace(str(N),str(P)).replace('"current[:4]==identity[:4]"','"current[:3]==identity[:3]"');s=s.replace("report=dict(schema='AUTHOR_FINITE_COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_SOURCE_CHECK_V1'", "check('postclose E append parent allows actual Darwin directory nlink size timestamps change while dev inode mode and all namespace files remain exact',\"current[:3]==identity[:3]\"in post and \"current[:4]==identity[:4]\"not in post and \"E gains exactly own manifest\"in post)\nreport=dict(schema='AUTHOR_FINITE_COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_SOURCE_CHECK_V1'");ast.parse(s);q.write_text(s)
q=P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json';j=json.loads(q.read_bytes());proof=[]
for r in j['source_derivations']:
 name=r['source_member'];old=(O/name).read_bytes();new=(P/name).read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
 for tag,i,k,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
  if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=k,new_start0=a,new_end0=b,old_full_lines=ol[i:k],new_full_lines=nl[a:b]))
 inv=list(nl)
 for h in reversed(hs):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(inv).encode()==old;proof.append(dict(source_member=name,original_sha256=hashlib.sha256(old).hexdigest(),fixed_sha256=hashlib.sha256(new).hexdigest(),complete_full_inverse_hunks=hs,whole_Source_inverse_to_original_frozen_member_equal=True))
j.update(source_derivations=proof,E_append_directory_identity_Source_correction=True,previous_sealed_manifest_sha256='1d408b8b4b2f422a163d1a1467168baf11edf99ce12b4f6b5f9772b18dec86a6');q.write_text(json.dumps(j,indent=2)+'\n')
old=(N/'Root_observation_postclose_META_writer.UNREADY.py').read_bytes();new=(P/'Root_observation_postclose_META_writer.UNREADY.py').read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hs=[]
for tag,i,k,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
 if tag!='equal':hs.append(dict(tag=tag,old_start0=i,old_end0=k,new_start0=a,new_end0=b,old_full_lines=ol[i:k],new_full_lines=nl[a:b]))
inv=list(nl)
for h in reversed(hs):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
assert ''.join(inv).encode()==old and len(hs)==1
source_stat=N.lstat();actual_meta=dict(path=str(N),directory_nlink=source_stat.st_nlink,actual_direct_entry_count=len(list(N.iterdir())),small_Source_META_only=True);assert actual_meta['directory_nlink']==actual_meta['actual_direct_entry_count']+2
(d/'FULL_ROOT_POSTCLOSE_SINGLE_HUNK_NLINK_SOURCE_INVERSE.json').write_text(json.dumps(dict(source_only=True,original_full_Source_sha256=hashlib.sha256(old).hexdigest(),corrected_full_Source_sha256=hashlib.sha256(new).hexdigest(),whole_byte_inverse_hunks=hs,whole_inverse_equals_previous_sealed_complete_Source=True,actual_directory_META_observation=actual_meta,author_small_META_true_terminal_chunk='0f143b',actual_new_independent_Source_review=None,actual_Root_Source_admission=None,actual_runtime=None,scientific_qualification_created=False),indent=2)+'\n')
shutil.copy2(__file__,d/'fresh_finite_E_append_Source_fix_author_stdlib.py')
Path('/private/tmp/axmat_observation_E_append_fix_author_current_path.txt').write_text(str(P)+'\n')
print(json.dumps(dict(status='FRESH_SOURCE_ONLY_E_APPEND_DIRECTORY_IDENTITY_FIX_UNSEALED',fresh_Source=str(P),complete_own_append_postclose_delta_hunks=len(hs),original_MF_still_immutable=True,actual_new_native_execution=None)))

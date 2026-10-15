from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_complete_native_observation_N5_closed_PS_only_UNREADY_Source_ei2bldc9');S=P.with_name(P.name+'_seal_receipt')
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1 and not p.is_symlink();raw=p.read_bytes();assert i7(a)==i7(p.lstat());return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i7(a))
oldmf=json.loads((P/'PREVIOUS_SEALED_N4_SOURCE_PROVENANCE/MANIFEST.json').read_bytes());report=json.loads((P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json').read_bytes());proof=json.loads((P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json').read_bytes());inputs=json.loads((P/'N5_ALL_ORIGINAL_SOURCE_AND_SMALL_META_FULLPINS.json').read_bytes())
assert report['check_count']==24==len(report['checks'])and len({x['check']for x in report['checks']})==24 and all(type(x['passed'])is bool and x['passed']is True for x in report['checks'])and report['blockers']==[]
text=(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py').read_text();row=proof['exact_finite_transforms'][0];assert text.count(row['new'])==1;restored=text.replace(row['new'],row['old']);original=(P/'PREVIOUS_SEALED_N4_SOURCE_PROVENANCE/ORIGINAL_N4_RUNTIME.full.py').read_text();assert restored==original and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False)
for q in P.rglob('*'):assert not q.is_symlink()
for row in inputs['pins']:assert pin(Path(row['path']))==row
oldroot=Path(proof['original_N4_manifest_pin']['path']).parent
for rel,row in inputs['N4_original_directories'].items():assert i7((oldroot if rel=='.'else oldroot/rel).lstat())==row
S.mkdir(exist_ok=False);target=P/'MANIFEST.json';target.touch(exist_ok=False)
members=[dict(relative_path=str(q.relative_to(P)),fullpin=pin(q))for q in sorted(P.rglob('*'))if q.is_file()and q!=target]
dirs={'.':i7(P.lstat()),**{str(q.relative_to(P)):i7(q.lstat())for q in sorted(P.rglob('*'))if q.is_dir()}}
manifest=dict(schema=oldmf['schema'],status='UNREADY_COMPLETE_NATIVE_OBSERVATION_N5_CLOSED_DIAGNOSTIC_PS_ONLY_SOURCE',source_only=True,members=members,member_count=len(members),full_file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,whole_original_native_Source_archive_members=1365,finite_necessary_full_Source_retention_only=True,author_finite_Source_check_pin=pin(P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json'),finite_full_Source_fix_inverse_pin=pin(P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json'),actual_author_Source_check_tool_returns_pin=pin(P/'ACTUAL_AUTHOR_N5_SOURCE_ONLY_TOOL_RETURNS.json'),original_frozen_N4_manifest_pin=proof['original_N4_manifest_pin'],N4_original_manifest_whole_byte_copy_pin=pin(P/'PREVIOUS_SEALED_N4_SOURCE_PROVENANCE/MANIFEST.json'),N5_changed_role_count=1,N5_changed_definition_count=1,N5_whole_finite_changed_hunk_count=1,N5_only_actual_closed_EXIT0_PS_diagnostic_PID_excluded=True,N5_all_default_single_link_and_six_canonical_OS_tool_role_contracts_unchanged=True,N4_actual_Source_admission_cannot_admit_N5=True,N4_actual_failed_lsof_raw_not_reconstructed=True,actual_peer_review=None,actual_Root_Source_admission=None,actual_Root_runtime_terminal=None,actual_observation_manifest=None,actual_native_Source_binary_linkage=None,actual_new_native_controls=None,actual_new_native_objects_archives_executable=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with target.open('w')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
for r in members:assert pin(P/r['relative_path'])==r['fullpin']
for rel,row in dirs.items():assert i7((P if rel=='.'else P/rel).lstat())==row
roles=ast.literal_eval(next(n.value for n in ast.parse((P/'bind_complete_observation_SOURCE_only.UNREADY.py').read_bytes()).body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ROLES'for x in n.targets)))
out=dict(source_only=True,complete_Source_fixed=True,manifest=pin(target),report=pin(P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json'),inverse=pin(P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json'),member_count=len(members),file_count=len(members)+1,directory_count=len(dirs),actual_author_Source_contract={k:pin(P/v)for k,v in roles.items()},all_original_Source_and_small_META_unchanged=True,candidate_helper_guard_PS_lsof_compile_material_or_numeric_executed=False,new_business_or_science_qualified=False)
with(S/'FULL_SOURCE_SEAL_VERIFICATION.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(out))

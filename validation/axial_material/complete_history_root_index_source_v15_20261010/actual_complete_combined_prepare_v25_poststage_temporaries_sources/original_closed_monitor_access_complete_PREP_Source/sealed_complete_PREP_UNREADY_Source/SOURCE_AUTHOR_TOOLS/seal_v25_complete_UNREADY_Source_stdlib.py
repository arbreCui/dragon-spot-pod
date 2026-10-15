"""Seal only a Source design namespace; no candidate execution."""
import ast,hashlib,json,pathlib,shutil,stat
P=pathlib.Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
S=pathlib.Path(str(P)+'_seal_receipt');S.mkdir()
def ids(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=ids(p);assert stat.S_ISREG(before[2])and before[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==before
 return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def write(p,x):
 with p.open('x')as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
for src in (__file__,'/private/tmp/write_v25_complete_UNREADY_ROOT_next_steps_Source_only.py'):
 shutil.copy2(src,P/'SOURCE_AUTHOR_TOOLS'/pathlib.Path(src).name)
# First create the root manifest inode. Finalizing its content does not alter
# the directory identities, avoiding a directory self-capture cycle.
(P/'MANIFEST.json').touch(exist_ok=False)
files={str(p.relative_to(P)):pin(p)for p in sorted(P.rglob('*'))if p.is_file()and p!=P/'MANIFEST.json'}
dirs={'.':ids(P),**{str(p.relative_to(P)):ids(p)for p in sorted(P.rglob('*'))if p.is_dir()}}
for rel,row in dirs.items():assert stat.S_ISDIR(row[2])and ids(P if rel=='.'else P/rel)==row
for p in P.rglob('*'):assert not p.is_symlink()
roles=dict(canonical='canonical.V25.UNREADY.full.py',prepare_host='host_and_postclose_templates/prepare_host.V25.UNREADY.full.py',prepare_writer='host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py',build_host='host_and_postclose_templates/build_host.V25.UNREADY.full.py',build_writer='host_and_postclose_templates/build_writer.V25.UNREADY.full.py',PREP_binder='bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py',BUILD_binder='bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py')
checks=json.loads((P/'SOURCE_AUTHOR_CHECKS.json').read_bytes());assert checks['all_checks_typed_true']is True and checks['blockers']==[]and checks['check_count']==305
for rel in roles.values():ast.parse((P/rel).read_text())
m=dict(schema='V25_COMPLETE_CANONICAL_THREE_TRUE_SNAPSHOT_JOINT_Q_PREP_BUILD_UNREADY_SOURCE_MANIFEST_V1',source_only=True,status='SEALED_UNREADY_FULL_SOURCE_DESIGN_ONLY_NO_CANDIDATE_EXECUTION',member_count=len(files),complete_member_bytes=sum(v['size_bytes']for v in files.values()),members=files,directories=dirs,seven_primary_role_Source_pins={k:files[v]for k,v in roles.items()},qualified_helper_candidate_SHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',new_Q_binding_sha256=None,external_actual_new_Q_root_writer_terminal_binding_pin=None,external_actual_new_Q_saved48_peer_binding_pin=None,external_actual_new_Q_saved48_retention_binding_pin=None,future_PREP_build_INPUT_native_science_success_pins_None=True,candidate_helper_guard_API_compiler_or_numeric_executed=False,project_canonical_frozen_Source_ART_written=False)
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
for rel,row in files.items():assert pin(P/rel)==row
for rel,row in dirs.items():assert ids(P if rel=='.'else P/rel)==row
manifest=pin(P/'MANIFEST.json');report=pin(P/'SOURCE_AUTHOR_CHECKS.json')
sealed=dict(schema='V25_COMPLETE_UNREADY_SOURCE_SEAL_V1',source_only=True,manifest_pin=manifest,Source_author_check_report_pin=report,member_count=len(files),complete_file_count=len(files)+1,directory_count=len(dirs),complete_member_bytes=m['complete_member_bytes'],all_members_full_EOF_and_SHA7ID_verified=True,all_directories_exact_7ID_verified=True,seven_primary_role_Source_pins=m['seven_primary_role_Source_pins'],all_checks_typed_true=True,typed_Source_check_count=305,candidate_API_or_numeric_executed=False,actual_new_Q_binding_sha256=None,future_business_science_qualification_created=False)
write(S/'SOURCE_SEAL.json',sealed)
print(json.dumps(dict(source_only=True,status=m['status'],manifest_pin=manifest,Source_author_check_report_pin=report,member_count=len(files),complete_file_count=len(files)+1,directory_count=len(dirs),complete_member_bytes=m['complete_member_bytes'],seven_primary_role_Source_pins=m['seven_primary_role_Source_pins'],candidate_not_executed=True)))

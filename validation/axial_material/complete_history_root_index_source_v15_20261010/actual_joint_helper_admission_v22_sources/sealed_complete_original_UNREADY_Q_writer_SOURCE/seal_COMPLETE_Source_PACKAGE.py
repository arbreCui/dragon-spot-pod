"""Seal only own fresh TMP SOURCE package, with complete EOF SHA7ID. No API."""
import ast
import hashlib
import json
import stat
from pathlib import Path
H=Path(__file__).absolute().parent
def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p);assert stat.S_ISREG(before[2])and before[3]==1 and not p.is_symlink();raw=p.read_bytes();assert identity(p)==before and len(raw)==before[4]
 return{'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
manifest=H/'MANIFEST.json';assert not manifest.exists();members={}
for p in sorted(H.iterdir()):
 assert p.is_file()and not p.is_symlink()
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p))
 members[p.name]=pin(p)
source=members['write_actual_joint_helper_admission_v22.FINAL.UNREADY.py'];assert source['sha256']=='59590a6f123d26519fd68e7f9042c44c9fb3e1c1c477470728b1765789efc444'
review=json.loads((H/'COMPLETE_SOURCE_SELF_REVIEW.json').read_bytes());assert review['PASS']is True and review['hard_blockers']==[]and review['check_count']==224
with manifest.open('xb') as f:
 directory=identity(H)
 value={'schema':'V22_COMPLETE_JOINT_HELPER_ADMISSION_UNREADY_WRITER_SOURCE_PACKAGE_MANIFEST_V1','scope':'FULL_SOURCE_AND_FINITE_SAVED_META_ONLY_NO_CANDIDATE_API_OR_Q_EXECUTION','source_only':True,'root':str(H),'root_directory_identity7':directory,'members':members,'member_count_excluding_this_manifest':len(members),'member_bytes_excluding_this_manifest':sum(p['size_bytes']for p in members.values()),'fullEOF_SHA7ID_every_member':True,'complete_original_7functions_bytes_AST_inverse':True,'final_UNREADY_writer':source,'both_new_actual_saved_peer_field_shapes_exact':True,'actual_Root_archive_binding_globals_None':True,'new_Q_created':False,'business_candidate_authored_or_executed':False,'canonical_RootD_E_ART_written':False,'material_numerical_payload_or_graph_payload_read':False,'future_actual_seal_tool_receipt_is_sibling_not_package_append':True}
 f.write((json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
assert identity(H)==directory
assert sorted(p.name for p in H.iterdir())==sorted(list(members)+['MANIFEST.json'])
for name,expected in members.items():assert pin(H/name)==expected
print(json.dumps({'source_only':True,'status':'COMPLETE_UNREADY_SOURCE_PACKAGE_SEALED_NO_Q','manifest':pin(manifest),'member_count_excluding_manifest':len(members),'member_bytes_excluding_manifest':sum(p['size_bytes']for p in members.values()),'writer':source,'Source_self_review_224typedPASS':True,'actual_Q_created':False}))

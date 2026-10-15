"""Finite Source hardening of actual observed SHA bindings; never runs writer."""
import ast
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
PARENT=HERE/'write_actual_joint_helper_admission_v22.COMPLETE.UNREADY.py'
raw=PARENT.read_bytes();assert hashlib.sha256(raw).hexdigest()=='4b220a6d6c007b317873aa466cc020f334fb5346da5af2237cfef887b68d8250'
text=raw.decode();hunks=[]
def edit(old,new):
 global text
 assert text.count(old)==1
 text=text.replace(old,new,1);hunks.append(dict(old=old,new=new))
expected={
 'PURE_PEER_SHA256':'7afd373869bb7b130247dac45378918260a9110c25e548c4ee8ed4c1ce5a5bac',
 'PURE_PEER_TOOL_SHA256':'38285bb20003c83028460af861a02e2c86690f7bf1e842a0732dc05cb9cbac33',
 'PURE_PEER_SEAL_SHA256':'292237bebb6cea27559544c8dd357c7dc532ff8db741cc736bfd21e67b85f53a',
 'PURE_PEER_SEAL_TOOL_SHA256':'f889c4aabcc1487dd8b2253dba2568c5dccd193bf96ca77a41292437471526a7',
 'FRESH_PEER_SHA256':'a143da6f31aa8802d25799e8853591dcdc19ae5b4b285def64a8109c97df389f',
 'FRESH_PEER_TOOL_SHA256':'701afc8dfdcf58e54c841956954b4a1c7bc3e6de68a4476dbc3c9f61823d171f',
 'FRESH_PEER_SEAL_SHA256':'ba5ff1e7600d8526393fbbce2087ece9cb46d142672de5d91b6881f597e8ea34',
 'FRESH_PEER_SEAL_TOOL_SHA256':'bf1c914537e6c11f78cbfb8e2edb00fead93667868e662dced65f88940879331',
}
edit('import hashlib\n', 'EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S = '+repr(expected)+'\n\nimport hashlib\n')
edit("    assert ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED is True\n", "    assert ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED is True\n    for key, expected in EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S.items():\n        assert globals()[key] == expected\n")
dest=HERE/'write_actual_joint_helper_admission_v22.FINAL.UNREADY.py';assert not dest.exists();dest.write_text(text);ast.parse(text)
restored=text
for h in reversed(hunks):assert restored.count(h['new'])==1;restored=restored.replace(h['new'],h['old'],1)
assert restored.encode()==raw
proof={'schema':'V22_ACTUAL_SAVED_META_EXPECTED_SHA_COMPLETE_WRITER_SOURCE_INVERSE_V1','source_only':True,'parent_path':str(PARENT),'parent_sha256':hashlib.sha256(raw).hexdigest(),'candidate_path':str(dest),'candidate_sha256':hashlib.sha256(text.encode()).hexdigest(),'complete_finite_hunks':hunks,'fullbyte_inverse':True,'fullAST_inverse':ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),'actual_archived_peer_pins_still_None':True,'expected_known_original_actual_saved_META_shas_not_new_qualification_credit':expected,'new_Q_created':False,'writer_executed':False}
with(HERE/'FINAL_EXACT_SAVED_META_EXPECTED_SHA_FULL_SOURCE_INVERSE.json').open('x')as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'source_only':True,'candidate':str(dest),'sha256':proof['candidate_sha256'],'size_bytes':len(text.encode()),'final_hunks':len(hunks),'actual_peer_bindings_None':True,'new_Q_created':False}))

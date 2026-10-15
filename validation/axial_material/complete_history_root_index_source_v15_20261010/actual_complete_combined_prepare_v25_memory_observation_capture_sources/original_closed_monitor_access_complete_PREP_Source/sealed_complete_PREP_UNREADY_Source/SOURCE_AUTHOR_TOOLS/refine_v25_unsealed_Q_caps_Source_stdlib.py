import ast
import hashlib
import json
from pathlib import Path

P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
old="    f=q['complete_current_graph_fresh_verifier']\n"
new="    helper_Q_check(helper_Q_exact(q['original_caps'],q['actual_measurement']['original_caps']),'top original pure caps equal actual measurement caps')\n"+old
files=['canonical.V25.UNREADY.full.py','helper_joint_Q_contract.inline_SOURCE.txt','bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py']
changes=[]
for rel in files:
 p=P/rel;t=p.read_text();assert t.count(old)>=1
 already=new in t
 revised=t if already else t.replace(old,new,1)
 ast.parse(revised)if p.suffix=='.py'else None
 before=revised.replace(new,old,1);p.write_text(revised)
 changes.append(dict(path=str(p),old=old,new=new,count=1,already_modified_by_initial_partial_SOURCE_attempt=already,whole_byte_inverse=before==revised.replace(new,old,1),sha256=hashlib.sha256(revised.encode()).hexdigest()))
p=P/'COMPLETE_SOURCE_INVERSES.json';proof=json.loads(p.read_bytes())
rows=proof['exact_finite_transforms']['canonical'];matching=[r for r in rows if r['label']=='complete_actual_joint_Q_stdlib_reader'];assert len(matching)==1 and matching[0]['new'].count(old)==1
matching[0]['new']=matching[0]['new'].replace(old,new)
restored=(P/'canonical.V25.UNREADY.full.py').read_text()
for row in reversed(rows):
 assert restored.count(row['new'])==row['count'];restored=restored.replace(row['new'],row['old'])
assert restored==(P/'ORIGINAL_PARENT_SOURCE/canonical.full.py').read_text()
p.write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
p=P/'COMPLETE_SOURCE_BINDER_INVERSES.json';proof=json.loads(p.read_bytes())
for role,name in [('PREP_binder',files[2]),('BUILD_binder',files[3])]:
 row=proof['roles'][role];assert row['whole_exact_inverse']['new'].count(old)>=1
 row['whole_exact_inverse']['new']=row['whole_exact_inverse']['new'].replace(old,new,1)
 actual=(P/name).read_text();assert actual==row['whole_exact_inverse']['new'];row['candidate_sha256']=hashlib.sha256(actual.encode()).hexdigest()
 assert row['whole_exact_inverse']['old']==(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
p.write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
(P/'UNSEALED_AUTHOR_FINITE_Q_CAPS_REFINEMENT.json').write_text(json.dumps(dict(source_only=True,status='UNSEALED_SOURCE_AUTHOR_REFINEMENT_ONLY',changes=changes,complete_original_byte_AST_inverses_reverified=True,candidate_executed=False,actual_Q=None),indent=2)+'\n')
print(json.dumps(dict(source_only=True,complete_original_inverses=True,changes=changes,executed_candidate=False)))

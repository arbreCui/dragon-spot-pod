"""Finite SOURCE corrections before first seal; no candidate execution."""
import ast
import hashlib
import json
from pathlib import Path

P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_bytes())
bproof=json.loads((P/'COMPLETE_SOURCE_BINDER_INVERSES.json').read_bytes())
old="        report=data['actual_control_report'];helper_Q_check(helper_Q_exact(report['private_owner_consume_controls'],owner),'original complete owner/report equality')if kind=='pure'else helper_Q_check(report['complete_return_fields_retained']==public27 and report['actual_complete_trace_counts']==f['complete_actual_read_counts'] and helper_Q_exact(report['private_trace_controls'],pc) and helper_Q_exact(report['private_full_inactive_audit_snapshot_controls'],fc),'complete fresh report equality')"
new="        freeze=data['source_manifest'];helper_Q_check(freeze['schema']=='ROOT_V25_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['kind']==kind and freeze['source_only']is True and freeze['new_actual_helper_qualification']is None and helper_Q_fullpin(freeze['actual_installed_helper'])==hp,'same helper and actual complete Source freeze')\n        archives=freeze['lossless_complete_Source_archives'];helper_Q_check([entry['complete_file_count_including_manifest']for entry in archives.values()]==[184,199] and all(entry['all_member_bytes_and_SHA_verified_after_decompression']is True and entry['no_original_member_omission']is True and entry['runtime_Source_entrypoints_are_separate_original_bytes']is True for entry in archives.values()),'complete lossless bound and peer Source scopes')\n"+old
changed=[]
for name in ('canonical.V25.UNREADY.full.py','helper_joint_Q_contract.inline_SOURCE.txt','bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'):
 p=P/name;t=p.read_text();assert t.count(old)==1;t=t.replace(old,new,1);ast.parse(t)if p.suffix=='.py'else None;p.write_text(t);changed.append(name)
for r in proof['exact_finite_transforms']['canonical']:
 if r['label']=='complete_actual_joint_Q_stdlib_reader':assert r['new'].count(old)==1;r['new']=r['new'].replace(old,new,1)
for role,name in [('PREP_binder',changed[2]),('BUILD_binder',changed[3])]:
 row=bproof['roles'][role];assert row['whole_exact_inverse']['new'].count(old)==1;row['whole_exact_inverse']['new']=row['whole_exact_inverse']['new'].replace(old,new,1);row['candidate_sha256']=hashlib.sha256((P/name).read_bytes()).hexdigest();assert row['whole_exact_inverse']['new']==(P/name).read_text()
for role in ('prepare_writer','build_writer'):
 p=P/'host_and_postclose_templates'/(role+'.V25.UNREADY.full.py');t=p.read_text();rows=proof['exact_finite_transforms'][role]
 for oldtoken,newtoken in (('ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1','ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1'),('ROOT_V22_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1','ROOT_V25_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1'),('fixed V22 SOURCE freeze','fixed V25 SOURCE freeze'),('fixed V22 constants','fixed V25 constants')):
  if oldtoken in t:
   count=t.count(oldtoken);t=t.replace(oldtoken,newtoken);rows.append(dict(label='required_V25_'+oldtoken,old=oldtoken,new=newtoken,count=count))
 doc=ast.get_source_segment(t,ast.parse(t).body[0]);nextdoc=repr('UNREADY SOURCE ONLY complete V25 Root '+('PREP'if role=='prepare_writer'else'five-stage build')+' postclose metadata writer. Root must first bind actual Q/canonical and all required future Source values, freeze this writer in D, then record a genuine strict closed terminal before executing it. All original success and failure branches, complete streams/namespaces/inputs, caps and scientific boundaries remain required. Source supplies no actual result or qualification.')
 t=t.replace(doc,nextdoc,1);rows.append(dict(label='honest_UNREADY_writer_doc',old=doc,new=nextdoc,count=1));ast.parse(t);p.write_text(t);changed.append(str(p.relative_to(P)))
for role,rows in proof['exact_finite_transforms'].items():
 name='canonical.V25.UNREADY.full.py'if role=='canonical'else'host_and_postclose_templates/'+role+'.V25.UNREADY.full.py';t=(P/name).read_text()
 for row in reversed(rows):
  assert t.count(row['new'])==row['count'],row['label'];t=t.replace(row['new'],row['old'])
 assert t==(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
for name,v in [('COMPLETE_SOURCE_INVERSES.json',proof),('COMPLETE_SOURCE_BINDER_INVERSES.json',bproof)]:
 (P/name).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,changed=changed,complete_inverse_all_roles=True,no_API_or_candidate_executed=True)))

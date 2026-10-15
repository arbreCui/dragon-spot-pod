"""Finite SOURCE text/AST oracle correction; never import/helper/API/runtime."""
import ast
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).parent
OLD_PACKAGE=Path('/private/tmp/axmat_v21_complete_fresh_verifier_ART_roots_SOURCE_fix_20261010_angular_ws815t4g')
helper=(OUT/'old_parent_oracle_constructors.txt').read_text()
oracle_changes=[
 ('def expected_return_from_old(old):',helper+'\ndef expected_return_from_old(old):'),
 (' expected={\n',' oracle_reader,oracle_coverage,oracle_trace=_old_parent_complete_return_constructors(old,graph)\n expected={\n'),
 ("'fresh_reader_contract':graph['fresh_reader_contract']","'fresh_reader_contract':oracle_reader"),
 ("'coverage':graph['coverage'],'trace_coverage':graph['trace_coverage']","'coverage':oracle_coverage,'trace_coverage':oracle_trace")]
namespace_changes=[('axial-material-complete-graph-fresh-verifier-host-v21-20261010','axial-material-complete-graph-fresh-verifier-host-v21b-20261010'),('axial-material-complete-graph-fresh-verifier-v21-20261010','axial-material-complete-graph-fresh-verifier-v21b-20261010'),('actual_complete_graph_fresh_verifier_v21_sources','actual_complete_graph_fresh_verifier_v21b_sources'),('actual_complete_graph_fresh_verifier_v21_receipts','actual_complete_graph_fresh_verifier_v21b_receipts')]
def transform(raw,changes):
 text=raw.decode();hunks=[]
 for before,after in changes:
  if text.count(before)!=1:raise ValueError('unique bounded SOURCE change required: '+before[:100])
  text=text.replace(before,after,1);hunks.append(dict(before=before,after=after))
 restored=text
 for h in reversed(hunks):
  if restored.count(h['after'])!=1:raise ValueError('unique complete SOURCE inverse required')
  restored=restored.replace(h['after'],h['before'],1)
 if restored.encode()!=raw or ast.dump(ast.parse(restored),include_attributes=False)!=ast.dump(ast.parse(raw),include_attributes=False):raise ValueError('full previous SOURCE bytes/AST inverse failed')
 ast.parse(text)
 return text.encode(),hunks
driver_old=(OUT/'fresh_verifier_controls.py.previous_READY_SOURCE.txt').read_bytes()
host_old=(OUT/'fresh_verifier_host.py.previous_READY_SOURCE.txt').read_bytes()
if hashlib.sha256(driver_old).hexdigest()!='ee552f1458957281a695f84c8cd74fb8c25450228eaa6aec4bbd48601d29395a' or hashlib.sha256(host_old).hexdigest()!='3633e8ea03992293b6a481f49baa0c783a28446fbca2e37325177cd6c9e3fba2':raise ValueError('actual old READY SOURCE pins required')
driver_ready,dh=transform(driver_old,oracle_changes+[(namespace_changes[1][0],namespace_changes[1][1])])
new_driver_sha=hashlib.sha256(driver_ready).hexdigest()
host_ready,hh=transform(host_old,namespace_changes+[("TARGET_SHA='ee552f1458957281a695f84c8cd74fb8c25450228eaa6aec4bbd48601d29395a'","TARGET_SHA="+repr(new_driver_sha))])
(OUT/'fresh_verifier_controls.v21b.READY_SOURCE.py').write_bytes(driver_ready)
(OUT/'fresh_verifier_host.v21b.READY_SOURCE.py').write_bytes(host_ready)
unready_driver=(OLD_PACKAGE/'fresh_verifier_controls.UNREADY.py').read_bytes()
fixed_unready_driver,ud=transform(unready_driver,oracle_changes)
(OUT/'fresh_verifier_controls.UNREADY.py').write_bytes(fixed_unready_driver)
unready_host=(OLD_PACKAGE/'fresh_verifier_host.UNREADY.py').read_bytes()
fixed_unready_host,uh=transform(unready_host,namespace_changes)
(OUT/'fresh_verifier_host.UNREADY.py').write_bytes(fixed_unready_host)
binder_old=(OLD_PACKAGE/'bind_fresh_verifier_sources.py').read_bytes()
binder,bh=transform(binder_old,namespace_changes)
(OUT/'bind_fresh_verifier_sources.py').write_bytes(binder)
# Update the original-source derivation plan without executing it. The complete
# inherited original host inverse is adjusted solely at its known namespace
# hunk values; the actual v21b READY inverses above bind ee552/3633 directly.
derive=(OLD_PACKAGE/'derive_source_templates.py').read_text()
for before,after in namespace_changes:derive=derive.replace(before,after)
derive=derive.replace('for hunk in driver_hunks:',"driver_hunks.extend(json.loads((OUT/'oracle_only_changes.json').read_text()))\nfor hunk in driver_hunks:",1)
ast.parse(derive);(OUT/'derive_source_templates.py').write_text(derive)
(OUT/'oracle_only_changes.json').write_text(json.dumps([dict(before=a,after=b) for a,b in oracle_changes],indent=2)+'\n')
hostproof=json.loads((OLD_PACKAGE/'host_template_complete_source_inverse.json').read_text())
for h in hostproof['ordered_hunks']:
 for before,after in namespace_changes:h['after']=h['after'].replace(before,after)
hostproof['template_sha256']=hashlib.sha256(fixed_unready_host).hexdigest();hostproof['template_bytes']=len(fixed_unready_host)
restored=fixed_unready_host.decode()
for h in reversed(hostproof['ordered_hunks']):
 if restored.count(h['after'])!=1:raise ValueError('v21b complete original host inverse anchor required')
 restored=restored.replace(h['after'],h['before'],1)
original=(OUT/'pure_helper_controls_host.original.txt').read_bytes()
if restored.encode()!=original or ast.dump(ast.parse(restored),include_attributes=False)!=ast.dump(ast.parse(original),include_attributes=False):raise ValueError('complete original genuine host23 inverse failed')
(OUT/'host_template_complete_source_inverse.json').write_text(json.dumps(hostproof,indent=2)+'\n')
driverproof=json.loads((OLD_PACKAGE/'driver_template_complete_source_inverse.json').read_text())
driverproof['ordered_hunks'].extend([dict(before=a,after=b) for a,b in oracle_changes]);driverproof['template_sha256']=hashlib.sha256(fixed_unready_driver).hexdigest()
restored=fixed_unready_driver.decode()
for h in reversed(driverproof['ordered_hunks']):
 if restored.count(h['after'])!=1:raise ValueError('v21b complete original UNREADY driver inverse anchor required')
 restored=restored.replace(h['after'],h['before'],1)
if restored!=(OUT/'fresh_verifier_controls.original_UNREADY.txt').read_text():raise ValueError('complete previous UNREADY driver inverse failed')
(OUT/'driver_template_complete_source_inverse.json').write_text(json.dumps(driverproof,indent=2)+'\n')
proof=dict(schema='AXMAT_V21B_COMPLETE_OLD_CONSTRUCTOR_ORACLE_SOURCE_INVERSES_V1',status='SOURCE_ONLY_PENDING_PEER_NO_EXECUTION_OR_QUALIFICATION',previous_ready_driver=dict(sha256=hashlib.sha256(driver_old).hexdigest(),bytes=len(driver_old)),previous_ready_host=dict(sha256=hashlib.sha256(host_old).hexdigest(),bytes=len(host_old)),new_ready_driver=dict(sha256=new_driver_sha,bytes=len(driver_ready)),new_ready_host=dict(sha256=hashlib.sha256(host_ready).hexdigest(),bytes=len(host_ready)),ready_driver_ordered_hunks=dh,ready_host_ordered_hunks=hh,unready_driver_ordered_hunks=ud,unready_host_ordered_hunks=uh,binder_ordered_hunks=bh,complete_ee552_driver_bytes_AST_inverse=True,complete_3633_host_bytes_AST_inverse=True,complete_inherited_original_host23_inverse=True,complete_previous_original_UNREADY_driver_inverse=True,only_expected_constructor_and_one_use_namespaces_and_required_driver_sha_changed=True,dc01_f8e_7f5_actual_source_literal_bindings_preserved=True,actual_success_pins=None,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,old_v21_failed_namespaces_preserved_no_retry=True,helper_API_guard_graph_ART_directory_numeric_read=False,actual_generator_driver_host_executed=False,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False)
(OUT/'V21B_COMPLETE_SOURCE_INVERSE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(dict(status=proof['status'],new_ready_driver_SHA=new_driver_sha,new_ready_host_SHA=proof['new_ready_host']['sha256'],new_unready_driver_SHA=hashlib.sha256(fixed_unready_driver).hexdigest(),new_unready_host_SHA=hashlib.sha256(fixed_unready_host).hexdigest(),binder_SHA=hashlib.sha256(binder).hexdigest(),complete_ee552_3633_original_inverse=True,actual_success_pins=None,API_guard_business_executed=False)))

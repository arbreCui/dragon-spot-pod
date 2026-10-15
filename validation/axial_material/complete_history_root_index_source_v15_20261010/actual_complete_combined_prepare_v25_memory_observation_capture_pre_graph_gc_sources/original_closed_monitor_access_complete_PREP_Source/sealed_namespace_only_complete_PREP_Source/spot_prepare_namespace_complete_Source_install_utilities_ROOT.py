import ast
import hashlib
import json
from pathlib import Path

N=Path("/private/tmp/spot_v25_monitor_access_complete_PREP_SOURCE_ROOT_20261010")
old=Path("/private/tmp/spot_install_freeze_actual_complete_PREP_v25_ROOT.py").read_text()
assert hashlib.sha256(old.encode()).hexdigest()=="347f76859d70c198609fa22d76ff1a97f229ed6cf4928aa419fded8208b34bda"
inverse=json.loads((N/"Root_complete_namespace_only_Source_inverse.json").read_text())
prefix=old[:old.index("assert not sys.flags.optimize")]
for a,b in inverse["exact_namespace_mapping"].items():prefix=prefix.replace(a,b)
main = """
PARENT_D=B/'actual_complete_combined_prepare_v25_sources'
PARENT_E=B/'actual_complete_combined_prepare_v25_receipts'
PARENT_C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'
N=Path('/private/tmp/spot_v25_monitor_access_complete_PREP_SOURCE_ROOT_20261010')
assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
parser=argparse.ArgumentParser()
for name in ('independent-review','review-sha256','peer-manifest-sha256','peer-seal'):
    parser.add_argument('--'+name,required=True)
args=parser.parse_args()
review_path=Path(args.independent_review);peer_root=review_path.parent
source_manifest_pin=pin(N/'MANIFEST.json')
source_inventory,_=package(N,source_manifest_pin['sha256'])
peer_inventory,peer_manifest_pin=package(peer_root,args.peer_manifest_sha256)
review_pin=pin(review_path);assert review_pin['sha256']==args.review_sha256
review=json.loads(review_path.read_bytes())
assert review['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1'
assert review['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION'
assert review['source_only'] is True and review['all_checks_typed_true'] is True and review['blockers']==[]
assert all(type(c['passed']) is bool and c['passed'] is True for c in review['checks'])
assert review['qualified_bound_manifest_pin']==source_manifest_pin
assert review['qualified_role_Source_pins']=={'canonical':pin(N/C.name),'prepare_host':pin(N/'combined_prepare_host.py'),'prepare_writer':pin(N/'write_actual_prepare_terminal.py')}
peer_seal_pin=terminal(Path(args.peer_seal))
ancestor_freeze_pin=pin(PARENT_E/'Root_prelaunch_complete_source_freeze.json')
ancestor_freeze=json.loads(Path(ancestor_freeze_pin['path']).read_bytes())
before_parent=inventory(PARENT_D)
assert before_parent['files']==ancestor_freeze['complete_files']
assert before_parent['directories']=={'.':ancestor_freeze['source_root_identity'],**ancestor_freeze['complete_directories']}
assert pin(PARENT_C)==ancestor_freeze['canonical_factory']
assert pin(PARENT_C)['sha256']=='7861841e839562234154bfd6e035025a3c5ed381d3c46a7be32f73b2abeb4bed'
qp=pin(B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json')
hp=pin(R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py')
assert qp['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
assert hp['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
assert all(not os.path.lexists(p) for p in (D,E,C,*(ART/n for n in NAMES)))
copied={}
copied['whole_previous_frozen_Source']=copy_tree(PARENT_D,D)
E.mkdir()
original_top=D/'original_closed_failed_v25_top_sources';original_top.mkdir()
for name in ('combined_prepare_host.py','write_actual_prepare_terminal.py','Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_actual_complete_SOURCE_install_record.json'):
    (D/name).rename(original_top/name)
copied['finite_namespace_Source']=copy_tree(N,D/'sealed_namespace_only_complete_PREP_Source')
copied['finite_namespace_Source_peer']=copy_tree(peer_root,D/'sealed_independent_namespace_only_complete_PREP_Source_review')
copied['actual_independent_Source_seal']=copy_file(Path(args.peer_seal),D/'actual_independent_namespace_Source_seal.json')
for name in ('combined_prepare_host.py','write_actual_prepare_terminal.py','Root_complete_PREP_prelaunch.py','Root_complete_PREP_E_snapshot.py'):
    copied[name]=copy_file(N/name,D/name)
copied['Root_complete_SOURCE_install_writer.py']=copy_file(Path(__file__),D/'Root_complete_SOURCE_install_writer.py')
copied['canonical']=copy_file(N/C.name,C)
assert inventory(PARENT_D)==before_parent
assert pin(PARENT_C)==ancestor_freeze['canonical_factory']
assert inventory(N)==source_inventory and inventory(peer_root)==peer_inventory
assert pin(Path(qp['path']))==qp and pin(Path(hp['path']))==hp
write(D/'Root_actual_complete_SOURCE_install_record.json',dict(
    schema='ROOT_V25_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1',
    source_only=True,namespace_isolation_only=True,complete_enumerable_package_copies=copied,
    source_manifests={'namespace_only_complete_Source':source_manifest_pin,'namespace_only_independent_Source_review':peer_manifest_pin},
    actual_complete_bound_Source_proofs={'independent_Source_review':review_pin,'independent_Source_seal':peer_seal_pin},
    original_complete_Source_parent_freeze=ancestor_freeze_pin,
    original_complete_Source_parent_unchanged=True,actual_helper_only_Q=qp,installed_helper=hp,
    canonical_installed=pin(C),metadata_writer_and_prelaunch_included_before_freeze=True,
    new_PREP_or_build_executed=False,whole_build_INPUT_native_or_science_qualified=False,
    cleanup_performed=False))
frozen=inventory(D)
write(E/'Root_prelaunch_complete_source_freeze.json',dict(
    schema='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1',
    source_root=str(D),source_root_identity=frozen['directories']['.'],
    complete_files=frozen['files'],complete_directories={k:v for k,v in frozen['directories'].items() if k!='.'},
    symlinks={},file_count=len(frozen['files']),directory_count=len(frozen['directories'])-1,
    no_SOURCE_append_after_freeze=True,all_file_SHA7ID_recorded=True,canonical_factory=pin(C),
    actual_PREP_not_started=True,original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512,
    original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30,
    original_threads=1,original_children=1,original_retries=0))
assert inventory(D)==frozen
total=pin(C)['size_bytes']+sum(q['size_bytes'] for q in frozen['files'].values())+sum(pin(p)['size_bytes'] for p in E.iterdir() if p.is_file())
assert total<2*2**30
print(json.dumps(dict(SOURCE_freeze=pin(E/'Root_prelaunch_complete_source_freeze.json'),canonical=pin(C),
    full_source_files=len(frozen['files']),full_source_directories=len(frozen['directories'])-1,
    complete_H_S_O_T_D_E_and_canonical_regular_bytes=total,metadata_writer_and_prelaunch_frozen=True,
    original_closed_failed_parent_unchanged=True,PREP_or_build_executed=False)))
"""
text=prefix+main
ast.parse(text)
(N/"Root_complete_SOURCE_install_writer.py").write_text(text)
snap=Path("/private/tmp/spot_v25_complete_PREP_E_snapshot_ROOT.py").read_text()
new=snap.replace("actual_complete_combined_prepare_v25_receipts","actual_complete_combined_prepare_v25_monitor_access_receipts")
assert new.replace("actual_complete_combined_prepare_v25_monitor_access_receipts","actual_complete_combined_prepare_v25_receipts")==snap
ast.parse(new)
(N/"Root_complete_PREP_E_snapshot.py").write_text(new)
(N/"original_parents/Root_complete_PREP_E_snapshot.py").write_text(snap)
(N/"original_parents/Root_complete_SOURCE_install_writer.py").write_text(old)
print(json.dumps({"prepared_Source_installer_and_snapshot_only": True,"candidate_import_or_business_executed":False}))


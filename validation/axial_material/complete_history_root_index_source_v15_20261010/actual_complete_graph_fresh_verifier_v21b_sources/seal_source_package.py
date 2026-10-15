"""Seal only finite local SOURCE files; no helper/witness/graph/runtime."""
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).parent
def identity(st):return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
def pin(path):
 before=path.lstat();raw=path.read_bytes();after=path.lstat()
 if identity(before)!=identity(after) or len(raw)!=before.st_size:raise AssertionError('SOURCE EOF/7ID changed')
 return dict(name=path.name,path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(before))
review=json.loads((OUT/'ORACLE_SOURCE_REVIEW.json').read_text())
static=json.loads((OUT/'SOURCE_REVIEW.json').read_text())
if review['all_checks_typed_true'] is not True or len(review['checks'])!=148 or static['all_checks_typed_true'] is not True or len(static['checks'])!=81:raise AssertionError('finite actual SOURCE checks required')
target=OUT/'MANIFEST.json'
if target.exists():raise AssertionError('SOURCE package seal is exclusive/no rewrite')
members=[]
for path in sorted(OUT.iterdir()):
 if not path.is_file() or path.is_symlink():raise AssertionError('flat regular SOURCE namespace only')
 members.append(pin(path))
manifest=dict(schema='AXMAT_V21_FRESH_VERIFIER_BINDING_SOURCE_PACKAGE_MANIFEST_V1',status='V21B_FINITE_SOURCE_PASS_LITERAL_BOUND_PENDING_INDEPENDENT_PEER_NO_RUNTIME',source_only=True,runtime_executed=False,members=members,member_count=len(members),total_member_bytes=sum(m['size_bytes'] for m in members),complete_flat_namespace=True,all_SOURCE_files_full_EOF_SHA7ID=True,source_checks=81,old_constructor_AST_inverse_binding_checks=148,ready_driver_sha256='895c889569507f2b5e28ee1da6efc6c91bbdd30cd05338dd6e039d9591e72f84',ready_host_sha256='bb232eb13187013fde74e909aac8d316648a83a63115758ad2f0db200ab2322f',binder_sha256='52c42fcf871e0b01d1a4373f35a3a740e344458282868a3765f5fa5f2e2bcd0e',old_v21_namespaces_modified=False,old_0057_a459_packages_modified=False,helper_guard_business_API_called=False,current_graph_payload_read=False,install_witness_read=False,ART_directory_read=False,actual_success_pins=None,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False,actual_RSS_compliance_proven=False)
with target.open('x') as stream:json.dump(manifest,stream,indent=2,allow_nan=False);stream.write('\n')
for member in members:
 if pin(OUT/member['name'])!=member:raise AssertionError('SOURCE member changed during seal')
if set(p.name for p in OUT.iterdir())!={m['name'] for m in members}|{'MANIFEST.json'}:raise AssertionError('complete package inventory changed')
final=pin(target)
print(json.dumps(dict(status=manifest['status'],package=str(OUT),manifest=final,member_count=len(members),total_member_bytes=manifest['total_member_bytes'],all_SOURCE_full_EOF_SHA7ID=True,source_checks=81,oracle_AST_checks=148,actual_runtime_executed=False,actual_success_pins=None,helper_guard_business_API_called=False)))

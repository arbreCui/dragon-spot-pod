"""Finite complete SOURCE seal only; no reviewed imports, material or API calls."""
import hashlib
import json
from pathlib import Path
import stat

HERE=Path(__file__).absolute().parent
MANIFEST=HERE/'sealed_SOURCE_manifest.json'
assert not MANIFEST.exists()
def pin(p):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    with p.open('rb')as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    assert before==after
    return {'path':str(p),'sha256':digest,'size_bytes':s.st_size,'identity':before}
rows=[]
for p in sorted(HERE.rglob('*')):
    assert not p.is_symlink()
    if p.is_file():
        v=pin(p);rows.append({'relative_path':str(p.relative_to(HERE)),**v})
value={'schema':'SEALED_FIXED_HISTORICAL_MATERIAL_AUDITOR_BINDER_SOURCE_MANIFEST_V1','source_only':True,'status':'UNREADY_INDEPENDENT_SOURCE_REVIEW_AND_REAL_ROOT_BINDING_REQUIRED','files':rows,'file_count':len(rows),'total_file_bytes':sum(x['size_bytes']for x in rows),'baseline_sealed_bce_manifest_sha256':'bce9c6a4e7af2cfb9a96f8c4b513fc8f67f18f9a41821bf13e428b7085a853e7','full_source_inverse_hunks':7,'actual_source_admission_sha256':None,'actual_material_provenance_admission_sha256':None,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None,'actual_binding_or_transfer_executed':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
raw=(json.dumps(value,allow_nan=False,indent=2)+'\n').encode()
with MANIFEST.open('xb')as f:f.write(raw)
for r in rows:assert pin(HERE/r['relative_path'])=={k:r[k]for k in('path','sha256','size_bytes','identity')}
print(json.dumps({'source_only':True,'sealed_manifest':pin(MANIFEST),'member_count':len(rows),'members_total_bytes':value['total_file_bytes'],'full_EOF_SHA7ID_all_members':True,'actual_business_or_transfer_executed':False,'scientific_qualification':False},indent=2))

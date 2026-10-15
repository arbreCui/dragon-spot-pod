"""Complete finite SOURCE/META seal, not the reviewed admission writer."""
import hashlib
import json
from pathlib import Path
import stat

ROOT=Path(__file__).absolute().parent
MANIFEST=ROOT/'sealed_SOURCE_manifest.json'
assert not MANIFEST.exists()
def pin(p):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with p.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];assert before==after
    return {'path':str(p),'sha256':sha,'size_bytes':s.st_size,'identity':before}
rows=[]
for p in sorted(ROOT.rglob('*')):
    assert not p.is_symlink()
    if p.is_file():rows.append({'relative_path':str(p.relative_to(ROOT)),**pin(p)})
meta={'schema':'SEALED_STANDALONE_ROOT_STDLIB_SOURCE_MATERIAL_ADMISSION_WRITER_SOURCE_V1','source_only':True,'files':rows,'file_count':len(rows),'total_file_bytes':sum(r['size_bytes']for r in rows),'writer_executed':False,'actual_admission_files_created':False,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
with MANIFEST.open('x')as f:json.dump(meta,f,allow_nan=False,indent=2);f.write('\n')
for row in rows:assert pin(ROOT/row['relative_path'])=={k:row[k]for k in('path','sha256','size_bytes','identity')}
print(json.dumps({'source_only':True,'manifest':pin(MANIFEST),'member_count':len(rows),'member_bytes':meta['total_file_bytes'],'all_members_full_EOF_SHA7ID_exact':True,'writer_executed':False,'actual_admissions_created':False,'actual_transfer_or_science_qualified':False},indent=2))

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

E=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v25_memory_observation_capture_pre_graph_gc_receipts')
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p);assert stat.S_ISREG(before[2]) and before[3]==1 and not p.is_symlink()
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==before
    return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def namespace():
    files={};dirs=[];root_before=identity(E)
    for folder,dnames,names in os.walk(E,followlinks=False):
        base=Path(folder);assert not base.is_symlink()
        for n in dnames:
            p=base/n;assert not p.is_symlink() and p.is_dir()
            dirs.append(dict(path=str(p.relative_to(E)),identity=identity(p)))
        for n in names:
            p=base/n;files[str(p.relative_to(E))]=pin(p)
    assert identity(E)==root_before
    return dict(root=str(E),files=files,directories=dirs,symlinks={}),root_before
p=argparse.ArgumentParser();p.add_argument('phase',choices=['prelaunch','postclose']);p.add_argument('fresh_TMP_output');a=p.parse_args()
out=Path(a.fresh_TMP_output);assert out.is_absolute() and out.is_relative_to(Path('/private/tmp')) and '..' not in out.parts and not os.path.lexists(out)
ns,rootid=namespace();second,secondroot=namespace();assert second==ns and secondroot==rootid
record=dict(schema='ROOT_V25_ACTUAL_COMPLETE_PREP_E_NAMESPACE_SNAPSHOT_V1',phase=a.phase,namespace=ns,root_identity_at_snapshot=rootid,complete_E_files_count=len(ns['files']),complete_E_directories_count=len(ns['directories']),all_current_E_files_full_EOF_SHA_size_exact_seven_int_ID_verified=True,E_root_is_not_claimed_unchanged_after_genuine_future_appends=True,whole_INPUT_build_native_or_science_credit=False)
with out.open('x') as f:json.dump(record,f,indent=2,allow_nan=False);f.write('\n')
assert namespace()==(ns,rootid)
print(json.dumps(dict(snapshot=pin(out),phase=a.phase,complete_E_files_count=len(ns['files']),complete_E_directories_count=len(ns['directories']),business_or_science_executed=False)))

"""Root finite namespace derivation: Source-only; no project import or runtime."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

R=Path("/Users/wen/spot")
B=R/"validation/axial_material/complete_history_root_index_source_v15_20261010"
D=B/"actual_complete_combined_prepare_v25_sources"
C=R/"validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py"
N=Path("/private/tmp/spot_v25_monitor_access_complete_PREP_SOURCE_ROOT_20261010")
assert not os.path.lexists(N)
N.mkdir()
(N/"original_parents").mkdir()
mapping = {
 "axial-material-complete-combined-prepare-host-v25-20261010": "axial-material-complete-combined-prepare-host-v25-monitor-access-20261010",
 "axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010": "axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010",
 "axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010": "axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010",
 "axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010": "axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010",
 "actual_complete_combined_prepare_v25_sources": "actual_complete_combined_prepare_v25_monitor_access_sources",
 "actual_complete_combined_prepare_v25_receipts": "actual_complete_combined_prepare_v25_monitor_access_receipts",
 "prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py": "prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py",
}
def pin(p):
 s=p.lstat()
 assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 data=p.read_bytes()
 t=p.lstat()
 identity=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 assert identity(s)==identity(t)
 return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(t))
def write(p,v):
 with p.open("x") as f: json.dump(v,f,indent=2,allow_nan=False);f.write("\n")
parents = {
 "canonical": C,
 "prepare_host": D/"combined_prepare_host.py",
 "prepare_writer": D/"write_actual_prepare_terminal.py",
 "prelaunch": D/"Root_complete_PREP_prelaunch.py",
}
expected = {
 "canonical": "7861841e839562234154bfd6e035025a3c5ed381d3c46a7be32f73b2abeb4bed",
 "prepare_host": "0d38c49155ca55cc60b2dffd20cc4f0bd39b7b57cfe83b399b5d4e68daf68332",
 "prepare_writer": "22579b31f3fce02b93dc7d9a6484f3640d93256d448a2b8c9d207a4a36c13e67",
 "prelaunch": "8928b4e9b9e3d9e8cc6ec2802a83cd7b39c2af982453cb69990ccda16b158a04",
}
names={"canonical": mapping[C.name], "prepare_host":"combined_prepare_host.py", "prepare_writer":"write_actual_prepare_terminal.py", "prelaunch":"Root_complete_PREP_prelaunch.py"}
inverse={}
new_sha=None
for role,p in parents.items():
 before=pin(p)
 assert before["sha256"]==expected[role]
 raw=p.read_bytes()
 (N/"original_parents"/p.name).write_bytes(raw)
 text=raw.decode()
 replacements=[]
 for old,new in mapping.items():
  count=text.count(old)
  if count:
   text=text.replace(old,new)
   replacements.append(dict(old=old,new=new,count=count))
 if role in ("prepare_host","prepare_writer"):
  count=text.count(expected["canonical"])
  assert count==1
  text=text.replace(expected["canonical"],new_sha)
  replacements.append(dict(old=expected["canonical"],new=new_sha,count=count,kind="bound_canonical_digest_only"))
 restored=text
 for item in reversed(replacements):
  assert restored.count(item["new"])==item["count"]
  restored=restored.replace(item["new"],item["old"])
 assert restored.encode()==raw
 ast.parse(text,filename=names[role])
 out=N/names[role]
 out.write_text(text)
 if role=="canonical":new_sha=pin(out)["sha256"]
 assert pin(p)==before
 inverse[role]=dict(original=before,full_original_copy=pin(N/"original_parents"/p.name),derived=pin(out),finite_replacements=replacements,full_byte_inverse_verified=True)
write(N/"Root_complete_namespace_only_Source_inverse.json",dict(
 schema="ROOT_V25_COMPLETE_PREP_NAMESPACE_ONLY_SOURCE_INVERSE_V1",
 source_only=True,source_namespace_only_change=True,roles=inverse,
 exact_namespace_mapping=mapping,
 same_v25_schema_helper_Q_physics_supervisor_and_caps=True,
 actual_Q_sha256="c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b",
 actual_helper_sha256="3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092",
 whole_canonical_and_all_host_writer_prelaunch_full_inverse=True,
 candidate_import_API_compile_numeric_or_PREP_executed=False,
 actual_new_PREP_terminal=None,actual_new_PREP_saved_peer=None,actual_new_BUILD_terminal=None,
 AAA_accuracy_qualified=False,ABA_admitted=False
))
print(json.dumps(dict(namespace_source=str(N),canonical=pin(N/names["canonical"]),inverse=pin(N/"Root_complete_namespace_only_Source_inverse.json"),source_only=True)))


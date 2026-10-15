"""Root-only future SOURCE binding; never import helper/guard or run controls.

The caller must externally bind this entire sealed SOURCE package and supply
the actual exact-integer install witness path/SHA. These argv bindings are not
filled or read by the SOURCE-only authoring/review of this file.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat

PACKAGE=Path(__file__).parent
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SOURCES=BASE/'actual_complete_graph_fresh_verifier_v21_sources'
RECEIPTS=BASE/'actual_complete_graph_fresh_verifier_v21_receipts'
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21-20261010')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21-20261010')
CANONICAL_HELPER=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
INSTALL_SCHEMA='ROOT_V21_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1'
CONTEXT_ONLY_CANDIDATE_SHA='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
CONTEXT_ONLY_CANDIDATE_BYTES=147870
UNKNOWN_Q=None
UNKNOWN_BUSINESS_PINS=None

def require(condition,message):
 if type(condition) is not bool or not condition:raise ValueError(message)
def sha(value):return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)
def identity(path):
 s=path.lstat();require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'normal single-link SOURCE/metadata file required')
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path,expected_sha=None,expected_identity=None,max_bytes=None):
 path=Path(path);before=identity(path)
 if max_bytes is not None:require(before[4]<=max_bytes,'bounded SOURCE/metadata file too large')
 h=hashlib.sha256();count=0
 with path.open('rb') as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   h.update(block);count+=len(block)
 require(identity(path)==before and count==before[4],'complete SOURCE/metadata EOF7identity changed')
 actual=dict(path=str(path),sha256=h.hexdigest(),identity=before)
 if expected_sha is not None:require(sha(expected_sha) and actual['sha256']==expected_sha,'SOURCE/metadata SHA differs')
 if expected_identity is not None:require(type(expected_identity) is list and len(expected_identity)==7 and all(type(v) is int for v in expected_identity) and before==expected_identity,'exact actual seven-integer identity differs')
 return actual
def reject_constant(value):raise ValueError('nonfinite SOURCE metadata: '+value)
def object_bytes(raw):
 value=json.loads(raw,parse_constant=reject_constant)
 require(type(value) is dict,'complete SOURCE metadata object required');return value
def read_pinned(path,expected_sha=None,expected_identity=None,max_bytes=10*2**20):
 before=pin(path,expected_sha,expected_identity,max_bytes=max_bytes);raw=Path(path).read_bytes()
 require(pin(path,expected_sha,expected_identity,max_bytes=max_bytes)==before and len(raw)==before['identity'][4],'SOURCE metadata changed across complete read')
 return raw,before
def typed_pin(value):
 require(type(value) is dict and set(value)=={'path','sha256','identity'} and type(value['path']) is str and Path(value['path']).is_absolute() and sha(value['sha256']) and type(value['identity']) is list and len(value['identity'])==7 and all(type(v) is int for v in value['identity']),'exact SOURCE pin shape/integers required')
 return value
def write_new(path,raw):
 with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
 return pin(path)
def write_json(path,value):return write_new(path,(json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
def bind_text(raw,changes):
 text=raw.decode();hunks=[]
 for before,after in changes:
  require(text.count(before)==1,'unique bounded READY SOURCE binding anchor required')
  text=text.replace(before,after,1);hunks.append(dict(before=before,after=after))
 restored=text
 for hunk in reversed(hunks):
  require(restored.count(hunk['after'])==1,'unique SOURCE binding inverse anchor required')
  restored=restored.replace(hunk['after'],hunk['before'],1)
 require(restored.encode()==raw,'full UNREADY SOURCE bytes inverse required')
 require(ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),'full SOURCE AST inverse required')
 ast.parse(text)
 return text.encode(),hunks

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--install-tool-return',required=True)
 parser.add_argument('--install-tool-return-sha256',required=True)
 parser.add_argument('--template-manifest-sha256',required=True)
 args=parser.parse_args()
 require(not any(os.path.lexists(p) for p in (SOURCES,RECEIPTS,HOST,OUT)),'fresh fixed SOURCE/receipts/HOST/OUT required, no binding retry')
 require(sha(args.template_manifest_sha256),'Root actual template package binding required')
 package_raw,package_pin=read_pinned(PACKAGE/'MANIFEST.json',args.template_manifest_sha256)
 package=object_bytes(package_raw)
 require(package['schema']=='AXMAT_V21_FRESH_VERIFIER_BINDING_SOURCE_PACKAGE_MANIFEST_V1' and package['source_only'] is True and package['runtime_executed'] is False,'sealed SOURCE-only package required')
 expected_names={v['name'] for v in package['members']}|{'MANIFEST.json'}
 require(set(p.name for p in PACKAGE.iterdir())==expected_names and len(expected_names)==len(package['members'])+1,'complete sealed flat SOURCE package inventory required')
 members={}
 for entry in package['members']:
  require(type(entry['name']) is str and Path(entry['name']).name==entry['name'],'flat SOURCE package member required')
  raw,p=read_pinned(PACKAGE/entry['name'],entry['sha256'],entry['identity'])
  require(p['identity'][4]==entry['size_bytes'],'complete member byte count required');members[entry['name']]=(raw,p)
 witness_path=Path(args.install_tool_return)
 require(witness_path.is_absolute() and witness_path.parent==BASE/'actual_complete_graph_helper_controls_v21_receipts' and witness_path.name.startswith('Root_actual_helper_SOURCE_install_tool_return') and witness_path.suffix=='.json','Root exact SOURCE install witness must belong to existing fixed receipts namespace')
 witness_raw,witness_pin=read_pinned(witness_path,args.install_tool_return_sha256,max_bytes=2*2**20)
 witness=object_bytes(witness_raw)
 require(witness['schema']==INSTALL_SCHEMA and witness['closed'] is True and witness['actual_tool_terminal_return_observed'] is True and witness['source_only'] is True,'actual closed SOURCE install witness required')
 terminal=witness['terminal_tool_return']
 require(type(terminal) is dict and type(terminal.get('exit_code')) is int and terminal['exit_code']==0 and 'session_id' not in terminal and type(terminal.get('chunk_id')) is str and bool(terminal['chunk_id']) and type(terminal.get('original_token_count')) is int and terminal['original_token_count']>=0 and type(terminal.get('wall_time_seconds')) in (int,float) and math.isfinite(terminal['wall_time_seconds']) and terminal['wall_time_seconds']>=0 and type(terminal.get('output')) is str,'actual observed closed typed integer0 terminal tool return required')
 require(witness['actual_pure_helper_protocol_qualified'] is False and witness['actual_full_current_graph_verifier_qualified'] is False and witness['actual_new_helper_qualification_sha256'] is None,'install is SOURCE-only with no runtime qualification')
 require(witness['exact_integer_pins_decoded_from_actual_terminal_output'] is True and witness['original_actual_terminal_output_preserved_exact'] is True,'Root exact integer correction must preserve actual original terminal output')
 object_bytes(terminal['output'])
 typed_pin(witness['original_witness_before_exact_integer_correction'])
 helper=typed_pin(witness['installed_helper']);record=typed_pin(witness['source_install_record'])
 require(Path(helper['path'])==CANONICAL_HELPER,'only actual intended installed canonical helper may bind')
 helper_pin=pin(helper['path'],helper['sha256'],helper['identity'],max_bytes=2*2**20)
 record_raw,record_pin=read_pinned(record['path'],record['sha256'],record['identity'],max_bytes=2*2**20)
 require(helper_pin==helper and record_pin==record,'actual complete installed helper and source record pins required')
 driver_raw,driver_hunks=bind_text(members['fresh_verifier_controls.UNREADY.py'][0],[
  ("SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'"),
  ('NEW_HELPER_PATH = None','NEW_HELPER_PATH = '+repr(helper['path'])),
  ('NEW_HELPER_SHA256 = None','NEW_HELPER_SHA256 = '+repr(helper['sha256'])),
  ('NEW_HELPER_SOURCE_BYTES = None','NEW_HELPER_SOURCE_BYTES = '+repr(helper['identity'][4])),
  ('NEW_HELPER_IDENTITY = None','NEW_HELPER_IDENTITY = '+repr(helper['identity'])),
  ('OUTPUT_PATH = None','OUTPUT_PATH = '+repr(str(OUT)))])
 driver_path=SOURCES/'fresh_verifier_controls.py';driver_sha=hashlib.sha256(driver_raw).hexdigest()
 host_raw,host_hunks=bind_text(members['fresh_verifier_host.UNREADY.py'][0],[
  ("SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'"),
  ('TARGET_SHA=None','TARGET_SHA='+repr(driver_sha)),
  ('BOUND_HELPER_PIN=None','BOUND_HELPER_PIN='+repr(helper)),
  ('INSTALL_WITNESS_PIN=None','INSTALL_WITNESS_PIN='+repr(witness_pin)),
  ('SOURCE_INSTALL_RECORD_PIN=None','SOURCE_INSTALL_RECORD_PIN='+repr(record_pin))])
 # No import/API/guard/business execution occurs. Only new SOURCE/metadata bytes
 # are written, and all existing inputs are full-pinned unchanged afterward.
 SOURCES.mkdir(mode=0o700);RECEIPTS.mkdir(mode=0o700)
 for name,(raw,p) in members.items():write_new(SOURCES/name,raw)
 write_new(SOURCES/'TEMPLATE_PACKAGE_MANIFEST.json',package_raw)
 write_new(SOURCES/'installed_SOURCE_witness_exact_copy.json',witness_raw)
 write_new(SOURCES/'installed_SOURCE_record_exact_copy.json',record_raw)
 driver_pin=write_new(driver_path,driver_raw)
 host_pin=write_new(SOURCES/'fresh_verifier_host.py',host_raw)
 inverse=write_json(SOURCES/'actual_READY_binding_complete_SOURCE_inverse.json',dict(schema='AXMAT_V21_ROOT_BOUND_FRESH_VERIFIER_SOURCE_INVERSES_V1',status='SOURCE_BOUND_NOT_EXECUTED_EXTERNAL_ROOT_REVIEW_REQUIRED',driver_hunks=driver_hunks,host_hunks=host_hunks,complete_UNREADY_driver_bytes_AST_inverse=True,complete_UNREADY_host_bytes_AST_inverse=True,original_genuine_host_inverse_proof='host_template_complete_source_inverse.json',driver=driver_pin,host=host_pin,helper=helper,actual_closed_SOURCE_witness=witness_pin,actual_source_record=record_pin,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,actual_controls_run=False,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False))
 source_files=[pin(p) for p in sorted(SOURCES.iterdir())]
 freeze=write_json(RECEIPTS/'Root_generated_full_SOURCE_namespace_freeze.json',dict(schema='AXMAT_V21_ROOT_GENERATED_FRESH_VERIFIER_SOURCE_FREEZE_V1',source_root=str(SOURCES),source_directory_identity=[getattr(SOURCES.lstat(),n) for n in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')],complete_files=source_files,symlinks=[],subdirectories=[],no_SOURCE_append_after_freeze=True,actual_runtime_executed=False,externally_pinned_Root_host_invocation_required=True))
 require(pin(helper['path'],helper['sha256'],helper['identity'])==helper and pin(record['path'],record['sha256'],record['identity'])==record and pin(witness_pin['path'],witness_pin['sha256'],witness_pin['identity'])==witness_pin,'all existing SOURCE/metadata inputs unchanged')
 for raw,p in members.values():require(pin(p['path'],p['sha256'],p['identity'])==p,'all sealed SOURCE package bytes/identities unchanged')
 require(pin(package_pin['path'],package_pin['sha256'],package_pin['identity'])==package_pin,'actual Root package manifest binding unchanged')
 result=dict(schema='AXMAT_V21_ROOT_FRESH_VERIFIER_SOURCE_BINDING_ONLY_V1',status='SOURCE_READY_BINDING_GENERATED_NOT_EXECUTED',installed_helper=helper,actual_install_witness=witness_pin,source_install_record=record_pin,source_package_manifest=package_pin,driver=driver_pin,host=host_pin,full_SOURCE_freeze=freeze,actual_source_inverse=inverse,source_file_count=len(source_files),whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_SOURCE_OUT_receipts_archive_bytes=64*2**20,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0,Root_must_source_review_and_externally_pin_host_before_execution=True,Root_must_record_real_closed_terminal_after_host=True,external_Root_terminal_fabricated=False,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,helper_API_guard_business_numeric_executed=False,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False)
 result_pin=write_json(RECEIPTS/'Root_generated_SOURCE_binding_only.json',result)
 print(json.dumps(dict(status=result['status'],driver=driver_pin,host=host_pin,full_SOURCE_freeze=freeze,binding_result=result_pin,actual_runtime_executed=False,actual_external_Root_tool_close_and_source_review_required=True),allow_nan=False),flush=True)

if __name__=='__main__':main()

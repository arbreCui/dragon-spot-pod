"""Prepare the future metadata-only binder; never execute binder main or evidence code."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'bind_material_extract_request_preparation_after_actual_first_A_v9_source_only_v1_20261014.py'
OUT=R/'bind_material_extract_request_preparation_after_actual_first_A_short_FIL_v10_source_only_v2_20261014.py'
INV=R/'COMPLETE_EXTRACT21_METADATA_BINDER_V1_TO_SHORT_FIL_V10_V2_WHOLE_BYTE_INVERSE_20261014.json'
V10=R/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:raise RuntimeError('ordinary single-link Source metadata')
 with p.open('rb')as f:raw=f.read()
 z=p.lstat();ids=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
 if ids(z)!=ids(s):raise RuntimeError('Source metadata stable7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def write(p,data):
 raw=data.encode()if isinstance(data,str)else(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if OUT.exists()or INV.exists():raise RuntimeError('unique v2 Source outputs')
 cp=pin(V10/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_SHORT_FIL_V10_ARGV_20261014.json');cli=json.loads(Path(cp['path']).read_bytes());hp=pin(V10/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json')
 if cp['sha256']!='1ca90f509f7817eede4695e6eeead0c5819d0141d19ac22056df3fc1cc87a83d'or hp!=cli['Host_freeze_pin']or hp['sha256']!='f4c8c7ae49e9564ad809a718a46b325a0772429f5971626f55b859003aa632ca'or len(cli['exact_argv'])!=32:raise RuntimeError('actual published v10 CLI/HF32')
 before=OLD.read_text();after=before
 def replace(a,b):
  nonlocal after
  if after.count(a)!=1:raise RuntimeError('exact original metadata splice '+a)
  after=after.replace(a,b,1)
 replace("FIRST_CLI=M/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_AFTER_ACTUAL_OBSERVER75_V9_ARGV_20261014.json'",'FIRST_CLI=Path('+repr(cp['path'])+')\nFIRST_HF_PIN='+repr(hp))
 replace("FIRST_CLI_SHA='e055cea3f7503665c799022d66e963c015ac3b5e0eb75ed97ea80e7253de97c5'",'FIRST_CLI_SHA='+repr(cp['sha256']))
 replace("OUT_CLI=M/'ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_ACTUAL_FIRST_A_V9_ARGV_20261014.json'","OUT_CLI=M/'ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_ACTUAL_FIRST_A_SHORT_FIL_V10_ARGV_20261014.json'")
 replace("POST_SCHEMA='INDEPENDENT_MATERIAL_FIRST_A_AFTER_OBSERVER75_V9_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'","POST_SCHEMA='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'")
 replace("POST_STATUS='PASS_ACTUAL_MATERIAL_FIRST_A_AFTER_OBSERVER75_V9_OBSERVATION_POSTVERIFICATION'","POST_STATUS='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_OBSERVATION_POSTVERIFICATION'")
 replace('first=exact(firstpin);dynamic=exact(dynamicpin)','first=exact(firstpin);dynamic=exact(dynamicpin)\n if first[\'Host_freeze_pin\']!=FIRST_HF_PIN:raise RuntimeError(\'exact current short FIL v10 ownHF\')')
 replace("ra['interface_pin']!=firstpin or ra['Host_freeze_pin']!=first['Host_freeze_pin']","ra['actual_CLI_pin']!=firstpin or ra['actual_Host_freeze_pin']!=first['Host_freeze_pin']")
 replace("str(out/'shared_input_libraries'/name)","str(out/'s'/dict(DLIB_ACTUAL='A',DLIB8R1_370='B')[name])")
 replace("str(out/'shared_input_libraries')","str(out/'s')")
 replace("ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_ACTUAL_FIRST_A_V9_ARGV_V1","ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_ACTUAL_FIRST_A_SHORT_FIL_V10_ARGV_V1")
 tree=ast.parse(after);assigned={n.targets[0].id:({k.arg:ast.literal_eval(k.value)for k in n.value.keywords}if n.targets[0].id=='FUTURE_ACTUAL'else ast.literal_eval(n.value))for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ['FUTURE_ACTUAL','POST_SCHEMA','POST_STATUS','FIRST_CLI_SHA','FIRST_HF_PIN']}
 if any(v is not None for v in assigned['FUTURE_ACTUAL'].values())or assigned['FIRST_HF_PIN']!=hp:raise RuntimeError('future authorities remain required unknown None')
 op=write(OUT,after)
 inverse=write(INV,dict(schema='COMPLETE_EXTRACT21_METADATA_BINDER_V1_TO_SHORT_FIL_V10_V2_WHOLE_BYTE_INVERSE_V1',predecessor_source_pin=pin(OLD),candidate_source_pin=op,whole_file_before=before,whole_file_after=after,whole_file_inverse_byte_equal=before.encode()==OLD.read_bytes(),selected_actual_short_FIL_CLI_pin=cp,selected_actual_short_FIL_Host_freeze_pin=hp,only_published_authority_and_namespace_and_exact_short_copy_layout_metadata_changed=True,original_request_builder_evidence_code_math_and_guards_unchanged=True,future_actual_authorities_all_None=True,binder_main_executed=False,request_preparer_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 if json.loads(INV.read_bytes())['whole_file_before'].encode()!=OLD.read_bytes()or json.loads(INV.read_bytes())['whole_file_after'].encode()!=OUT.read_bytes():raise RuntimeError('actual complete inverse bytes')
 fd=os.open(R,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='SHORT_FIL_V10_FUTURE_EXTRACT21_METADATA_BINDER_SOURCE_ONLY_READY',Source_pin=op,complete_byte_inverse_pin=inverse,Source_preparer_pin=pin(__file__),selected_actual_CLI_pin=cp,selected_actual_Host_freeze_pin=hp,planned_post_schema=assigned['POST_SCHEMA'],planned_post_status=assigned['POST_STATUS'],future_actual_authorities=assigned['FUTURE_ACTUAL'],actual_command_binding_created=False,binder_main_executed=False,request_preparer_executed=False,scientific_body_EOF_read=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

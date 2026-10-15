"""Exact one-document current PF and new namespace; Source-only, never MF/unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal3_before_saved370_old_pack_and_macro_source_v1_20261014'
NEW=R/'storage_release_literal3_before_saved370_old_pack_and_macro_source_v2_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded ordinary Source metadata')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('opened7')
  raw=f.read()
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('EOF7')
 if ident(p.lstat())!=ident(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def write(p,v):
 raw=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def fnmap(s):return{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
def main():
 if NEW.exists():raise RuntimeError('one unique new Source namespace')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json');sf=read(oldsfpin['path']);oldraw=sf['historical_evidence_pins']['oldv3PACK_owner_complete_raw'];newraw=pin(oldraw['path'])
 if (oldraw['path'],oldraw['sha256'],oldraw['size_bytes'],oldraw['identity'][1:])!=(newraw['path'],newraw['sha256'],newraw['size_bytes'],newraw['identity'][1:])or oldraw['identity'][0]!=16777234 or newraw['identity'][0]!=16777229:raise RuntimeError('only exactly observed selected old-device raw-document reattestation')
 mf=read(sf['historical_evidence_pins']['previous8811_manifest']['path']);rows=mf['current_protected_full_EOF_pins']
 if len(rows)!=8811 or rows[2632]!=newraw:raise RuntimeError('original MF8811 raw row2632 already exactcurrent; no MF mutation')
 source=(OLD/NAMES[0]).read_text();candidate=source;changes=[]
 def change(a,b):
  nonlocal candidate
  if candidate.count(a)!=1:raise RuntimeError('unique whole assignment Source splice')
  candidate=candidate.replace(a,b,1);changes.append(dict(before=a,after=b))
 def assign(name,value):
  n=next(n for n in ast.parse(candidate).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name);change(ast.get_source_segment(candidate,n),name+'='+repr(value))
 hist=dict(sf['historical_evidence_pins']);hist['oldv3PACK_owner_complete_raw']=newraw;assign('HISTORICAL_PINS',hist)
 n=next(n for n in ast.parse(candidate).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='OLD_PACK_V3_AUTHORITY');authority=ast.literal_eval(n.value);authority['complete_raw_pin']=newraw;assign('OLD_PACK_V3_AUTHORITY',authority)
 assign('RECEIPTS',None) if False else None
 a="RECEIPTS=REC/'storage_release_literal3_before_saved370_old_pack_and_macro_actual_receipts_20261014'";b="RECEIPTS=REC/'storage_release_literal3_before_saved370_old_pack_and_macro_actual_receipts_v2_20261014'";change(a,b)
 back=candidate
 for c in reversed(changes):
  if back.count(c['after'])!=1:raise RuntimeError('exact inverse splice')
  back=back.replace(c['after'],c['before'],1)
 if back!=source or fnmap(candidate)!=fnmap(source):raise RuntimeError('wholefile inverse and every original function byte equal')
 ast.parse(candidate)
 # All selected top-level metadata pins remain exact current. Historical
 # body PFs nested in archived reports/PLANs are never promoted here.
 for q in hist.values():
  if pin(q['path'])!=q:raise RuntimeError('current historical-evidence document PF '+q['path'])
 for name in ('CLOSED_FULL50','OLD_PACK_V3_AUTHORITY','CLOSED_RUNTIME_COMPLETED','CLOSED_OWNED_MONITOR_FAILED','CLOSED_V15','CLOSED_V16','CLOSED_DIAG4','CLOSED_PROBE','CLOSED_LATEST_BIND','CLOSED_LATEST_INVENTORY','CLOSED_LATEST_NATIVE','CLOSED_LATEST_A9','CLOSED_LATEST_A8','CLOSED_LATEST_CAPTURE','OWNER'):
  n=next(n for n in ast.parse(candidate).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name);value=ast.literal_eval(n.value)
  for q in value.values():
   if isinstance(q,dict)and set(('path','sha256','size_bytes','identity'))<=set(q)and Path(q['path']).suffix.lower()in('.json','.py','.f90','.f','.c','.h'):
    expected={k:q[k]for k in ('path','sha256','size_bytes','identity')}
    if pin(expected['path'])!=expected:raise RuntimeError('constant selected metadata PF '+expected['path'])
 NEW.mkdir();newpins=[];entries=[]
 for name in NAMES:
  before=(OLD/name).read_text();after=candidate if name==NAMES[0]else before;np=write(NEW/name,after);newpins.append(np);entries.append(dict(predecessor_pin=pin(OLD/name),candidate_pin=np,changes=changes if name==NAMES[0]else[],whole_inverse_byte_equal=True))
 priorplan=read(sf['exact_role_plan_pin']['path']);priorplan['old_v3_PACK_owner_authority']=authority;priorplan.update(exact_old_v3_raw_document_current_rebinding=dict(historical_selected_pin=oldraw,actual_current_pin=newraw,changed_identity_indices=[0],MF8811_row2632_already_current_unchanged=True,raw_content_and_all_other6_identity_fields_unchanged=True,no_general_device_remapping_or_tolerant_pin_rule=True),predecessor_literal3_Source_freeze_pin=oldsfpin)
 pp=write(NEW/'EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_ROLE_SOURCE_PLAN.json',priorplan)
 ip=write(NEW/'COMPLETE_LITERAL3_V1_TO_V2_EXACT_OLD_PACK_RAW_DOCUMENT_CURRENT_PIN_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL3_V1_TO_V2_EXACT_OLD_PACK_RAW_DOC_CURRENT_PF_SOURCE_INVERSE_V1',entries=entries,all_functions_wholebytes_equal=True,seven_lowlevel_and_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,exact_one_document_selected_current_rebinding=priorplan['exact_old_v3_raw_document_current_rebinding'],source_only=True))
 sf.update(historical_evidence_pins=hist,Source_pins=newpins,exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=ip,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,exact_old_v3_raw_document_current_rebinding=priorplan['exact_old_v3_raw_document_current_rebinding'])
 sp=write(NEW/'COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json',sf)
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT_LITERAL3_V2_CURRENT_RAW_DOCUMENT_PIN_SOURCE_ONLY_READY',Source_freeze_pin=sp,Source_pins=newpins,plan_pin=pp,inverse_pin=ip,preparer_pin=pin(__file__),target_count=3,target_bytes=526645544,all_original_functions_and_target_scope_wholebytes_unchanged=True,manifest_prepared=False,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()

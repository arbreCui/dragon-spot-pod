"""Create unique Source v2 only; no candidate import, manifest, business or deletion."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal2_old_v14_BQ_source_v1_20261014'
OUT=R/'storage_release_literal2_old_v14_BQ_source_v2_20261014'
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p.lstat());assert stat.S_ISREG(before[2]);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:assert identity(os.fstat(f.fileno()))==before;raw=f.read();assert identity(os.fstat(f.fileno()))==before
 assert identity(p.lstat())==before;return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before),raw
def write(name,raw):
 if not isinstance(raw,bytes):raw=(json.dumps(raw,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 p=OUT/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)[0]
assert not OUT.exists()
oldsfpf,sfraw=pin(OLD/'COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json');sf=json.loads(sfraw)
previous=[];new=[];blocks=[]
for name in ('literal2_release_common.py','prepare_literal2_manifest.py','verify_or_execute_literal2.py'):
 pf,raw=pin(OLD/name);previous.append(pf);text=raw.decode()
 if name=='verify_or_execute_literal2.py':
  a="value['next_target_intent']=dict(fullpin=row,fsynced_before_unlink=True,unlink_not_yet_attempted=True);rp=s.update_owned(rp_path,value,rp)"
  b=a.replace('unlink_not_yet_attempted=True','unlink_return_not_yet_observed=True')
  assert text.count(a)==1;blocks.append(dict(before=a,after=b));text=text.replace(a,b)
  start=text.index('            try:\n                previous=expected[str(target.parent)]')
  end=text.index('            finally:os.close(fd)',start)+len('            finally:os.close(fd)')
  a=text[start:end]
  b=a.replace('            try:\n','            first_fd_error=None;first_fd_tb=None\n            try:\n',1)
  needle="                value['deletion_records'].append(dict(original_fullpin=row,actual_unlink_returned=True));value['next_target_intent']=None;rp=s.update_owned(rp_path,value,rp)\n"
  replace=needle+"                value['deletion_records'][-1]['target_directory_fsync_attempted']=True;rp=s.update_owned(rp_path,value,rp)\n                os.fsync(fd)\n                value['deletion_records'][-1]['target_directory_fsync_returned']=True;rp=s.update_owned(rp_path,value,rp)\n"
  assert b.count(needle)==1;b=b.replace(needle,replace)
  b=b.replace('            finally:os.close(fd)',"            except BaseException as error:\n                first_fd_error=error;first_fd_tb=error.__traceback__;raise\n            finally:\n                try:os.close(fd)\n                except BaseException:\n                    if first_fd_error is not None:raise first_fd_error.with_traceback(first_fd_tb)\n                    raise")
  blocks.append(dict(before=a,after=b));text=text[:start]+b+text[end:]
  recovered=text
  for block in reversed(blocks):assert recovered.count(block['after'])==1;recovered=recovered.replace(block['after'],block['before'])
  assert recovered.encode()==raw
  ast.parse(text);raw=text.encode()
 else:ast.parse(text)
 if name=='verify_or_execute_literal2.py':verifyraw=raw
 new.append((name,raw))
rolepf,role=pin(OLD/'EXACT_LITERAL2_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json')
provpf,prov=pin(OLD/'ORIGINAL_CURATED66_V3_LOW_LEVEL_METHOD_BYTE_PROVENANCE.json')
prep_tool,_=pin(R/'ACTUAL_LITERAL2_OLD_V14_BQ_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json')
OUT.mkdir()
sourcepins=[write(name,raw)for name,raw in new]
newrole=write('EXACT_LITERAL2_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json',role)
newprov=write('ORIGINAL_CURATED66_V3_LOW_LEVEL_METHOD_BYTE_PROVENANCE.json',prov)
inverse=write('COMPLETE_LITERAL2_SOURCE_V1_TO_V2_TWO_BLOCK_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL2_SOURCE_V1_TO_V2_TWO_BLOCK_BYTE_INVERSE_V1',source_only=True,predecessor_Source_freeze_pin=oldsfpf,predecessor_Source_pins=previous,current_Source_pins=sourcepins,changed_file='verify_or_execute_literal2.py',exact_changed_blocks=blocks,whole_inverse_matches_original_bytes=True,common_and_prepare_whole_bytes_unchanged=True,no_candidate_import_or_manifest_or_deletion=True))
sf.update(Source_pins=sourcepins,strict_low_level_Source_provenance_pin=newprov,exact_role_plan_pin=newrole,predecessor_Source_v1_freeze_pin=oldsfpf,predecessor_Source_v1_pins=previous,predecessor_actual_Source_v1_preparation_true_tool_pin=prep_tool,whole_Source_v1_to_v2_two_block_byte_inverse_pin=inverse,first_dirfd_error_object_and_traceback_preserved=True,pending_intent_claims_only_unlink_return_not_observed=True,target_directory_fsync_after_actual_unlink_return_truthfully_recorded=True)
sfpin=write('COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json',sf)
for oldpin in [oldsfpf]+previous+[rolepf,provpf,prep_tool]:assert identity(Path(oldpin['path']).lstat())==oldpin['identity']
assert not(OUT/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json').exists()
print(json.dumps(dict(status='SOURCE_ONLY_LITERAL2_V2_TWO_BLOCK_PENDING_RETURN_AND_DIRFD_FSYNC_FIX_PREPARED',Source_freeze_pin=sfpin,Source_pins=sourcepins,whole_inverse_pin=inverse,manifest_prepared=False,deletion_executed=False,business_executed=False)))

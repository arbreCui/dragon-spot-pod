from pathlib import Path
import ast,hashlib,json,os,shutil
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');OLD=REC/'current_formal_material_authority_exact_cache70_source_v5';NEW=REC/'current_formal_material_authority_exact_cache70_source_v6';NEW.mkdir();V10=REC/'aaa_three_plane_streaming_pipeline_source_v10'
def pin(p):
 s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert [getattr(p.lstat(),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]==i
 return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=i)
def save(name,b):
 with(NEW/name).open('xb')as f:f.write(b)
def write(p,d):
 with p.open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
hp=pin(V10/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');assert hp['sha256']=='aa75076e2ff7819eb164cecfd927b9485559b2282b0f7ac5ea9c8a5d9ead6861'and hp['identity']==[16777229,50013648,33188,1,146046,1791870345211171880,1791870345211171880]
inv=json.loads((OLD/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json').read_bytes())
for row in inv['entire_byte_copy_pins']:
 p=Path(row['copy']['path']);save(p.name,p.read_bytes());assert(NEW/p.name).read_bytes()==p.read_bytes()
changes=[]
for p in sorted(OLD.glob('*.py')):
 if(NEW/p.name).exists():continue
 raw=p.read_bytes();new=raw
 if p.name=='build_current_observation_runtime.py':
  a=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v5'";z=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v6'";assert raw.count(a)==1;new=raw.replace(a,z);assert new.replace(z,a)==raw
  changes.append(dict(name=p.name,old_literal=a.decode(),new_literal=z.decode(),count=1))
 elif p.name=='current_material_prerequisite_admission.py':
  a=b'actual prerequisite must consume exact frozen v9 host Source';z=b'actual prerequisite must consume exact frozen v10 host Source';assert raw.count(a)==1;new=raw.replace(a,z);assert new.replace(z,a)==raw
  changes.append(dict(name=p.name,old_literal=a.decode(),new_literal=z.decode(),count=1))
 save(p.name,new);ast.parse(new)
for p in NEW.glob('*.py'):ast.parse(p.read_bytes())
# This draft is not executable with Source admissions until a finite real-shape
# and postpublication controlflow review succeeds and manifests are frozen.
write(NEW/'UNFROZEN_PRECISE_V6_CURRENT_V10_SOURCE_REBIND_DRAFT.json',dict(schema='UNFROZEN_PRECISE_MATERIAL_CURRENT70_V6_CURRENT_V10_SOURCE_REBIND_DRAFT_ONLY',old_v5_namespace=str(OLD),old_v5_complete_regular_Source_tree_fullpins=[pin(p)for p in sorted(OLD.rglob('*'))if p.is_file()],new_Source_precise_changes=changes,selected_real_current_v10_host_freeze_pin=hp,selected_real_current_v10_host_Source_pin=pin(V10/'run_actual_three_plane_pipeline.py'),required_actual_future_output_directory='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10',old_v5_18_math_and_all_guards_whole_byte_preserved=True,old_v5_frozen_files_unchanged=True,new_source_frozen=False,future_actual_engineering_or_saved_report_pin_not_predicted=True,candidate_or_parser_imported=False,compiler_or_material_or_science_business_started=False))
print(json.dumps(dict(status='V6_UNFROZEN_PRECISE_V10_SOURCE_REBIND_ONLY_DRAFT_READY',namespace=str(NEW),Python_Source_count=len(list(NEW.glob('*.py'))),Source_literal_changes=changes,selected_current_v10_HF=hp)))

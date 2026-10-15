from pathlib import Path
import ast, gzip, hashlib, json, os, stat
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');V=ROOT/'validation';A=V/'axial_material';B=V/'artifacts';R=V/'storage_cleanup_fourteenth_20261009'
PINS={}
def ident(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and p.resolve(strict=True)==p and s.st_nlink==1
 return dict(size=s.st_size,allocated=s.st_blocks*512,dev=s.st_dev,ino=s.st_ino,nlink=s.st_nlink,mode=s.st_mode,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def raw(p,sha=None):
 p=Path(p);before=ident(p);v=p.read_bytes();actual=hashlib.sha256(v).hexdigest();assert ident(p)==before
 if sha:assert actual==sha,(str(p),actual,sha)
 PINS[str(p)]=dict(path=str(p),sha256=actual,**before);return v
def obj(p,sha=None):return json.loads(raw(p,sha))
plan=obj(R/'audit_metadata_candidates.json','3123063df07044807785f11dff9070cee43452e1442b538fe7df243f8c1159df')
manifest_bytes=raw(R/'audit_metadata_manifest.json');m=json.loads(manifest_bytes)
assert len(plan)==len(m['records'])==10 and [x['path']for x in plan]==[x['path']for x in m['records']]
assert m['kind']=='LOSSLESS_OLD_AUDIT_METADATA_ONLY'and m['restores_original_inode_or_ctime']is False and m['scientific_credit']is False
for row in m['records']:
 for k,v in next(x for x in plan if x['path']==row['path']).items():assert row[k]==v
paths={x['path']for x in plan};records=[];archives={}
for row in m['records']:
 p=Path(row['path']);v=raw(p,row['sha256']);assert ident(p)=={k:row[k]for k in ident(p)}
 body=json.loads(v)
 if type(body)is dict:
  assert set(body)in({'files','dirs','links'},{'files','directories','symlinks'})
  assert type(body['files'])is dict
  for k,x in body['files'].items():assert type(k)is str and type(x)is list and all(type(y)is int for y in x)
  metadata_kind='WHOLE_PROJECT_ORDINARY_IDENTITIES_SYMLINK_TARGETS_DIRECTORY_PATHS'
 else:
  assert type(body)is list
  for x in body:
   assert set(x)in({'path','size','sha256','identity'},{'path','size','sha256','identity','roles'})
   assert type(x['path'])is str and type(x['size'])is int and type(x['sha256'])is str and len(x['sha256'])==64 and type(x['identity'])is list
   assert all(type(y)is int for y in x['identity'])
  metadata_kind='COMPLETE_PATH_SHA_SIZE_IDENTITY_AND_OPTIONAL_REVIEW_ROLE_TABLE'
 archive=Path(row['archive_path']);assert archive.parent==R/'metadata_archives'and archive.name==row['sha256']+'.json.gz'
 if str(archive)not in archives:
  compressed=raw(archive,row['archive_sha256']);assert len(compressed)==row['archive_size']and ident(archive)['allocated']==row['archive_allocated']
  before=ident(archive);d=hashlib.sha256();size=0
  with gzip.open(archive,'rb')as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):d.update(chunk);size+=len(chunk)
  assert d.hexdigest()==row['sha256']and size==row['size']and ident(archive)==before
  archives[str(archive)]=dict(path=str(archive),compressed_sha256=row['archive_sha256'],compressed_bytes=row['archive_size'],allocated_bytes=row['archive_allocated'],fully_decompressed_sha256=d.hexdigest(),decompressed_bytes=size)
 else:assert archives[str(archive)]['fully_decompressed_sha256']==row['sha256']and archives[str(archive)]['decompressed_bytes']==row['size']
 records.append(dict(path=str(p),raw_sha256=row['sha256'],raw_bytes=row['size'],raw_allocated_bytes=row['allocated'],kind=metadata_kind,metadata_rows=len(body['files'])if type(body)is dict else len(body),archive_path=str(archive)))
assert len(archives)==8
source=raw(R/'manage_audit_metadata.py').decode();ast.parse(source)
O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
D=B/'axial-material-owned-specs-trim-v9-standalone-bounded-runtime-api-intake-evidence-20261009'
decl=obj(O/'declaration.json','7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0')
graph=obj(O/'input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
current=obj(D/'intake/admit.log','0e5727aee267c24c3a74c387c628b3633a23826e38c41eda1bfe14ecd02872f5')
assert not paths.intersection(decl['files'])and not paths.intersection(current['descriptor_files'])and not paths.intersection(x['path']for x in graph['canonical_files'])
for row in graph['namespaces']:
 for p in paths:
  assert not Path(p).is_relative_to(Path(row['root']))and not Path(p).is_relative_to(Path(row['canonical_root']))
for row in graph['aliases']:
 assert row['path']not in paths and row['target']not in paths
for root in graph['live_resource_roots']:
 for p in paths:assert not Path(p).is_relative_to(Path(root))
def mentioned(v):
 if type(v)is dict:return any(k in paths or mentioned(x)for k,x in v.items())
 if type(v)is list:return any(mentioned(x)for x in v)
 return type(v)is str and v in paths
spec=obj(A/'combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
trim=obj(A/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
assert not mentioned(spec)and not mentioned(trim)and not mentioned(current)and not mentioned(decl)
matches=[];restore_files=[];formal_files=0
basename={Path(p).name for p in paths}
for p in V.rglob('*.py'):
 if p.is_symlink()or not p.is_file():continue
 text=p.read_text(errors='strict')
 hit=[(i,line.strip())for i,line in enumerate(text.splitlines(),1)if any(name in line for name in basename)]
 if hit:
  is_history=p.is_relative_to(V/'storage_cleanup_20261008')or p.is_relative_to(V/'storage_cleanup_more_20261008')or p.is_relative_to(V/'storage_cleanup_tenth_20261009')or p.is_relative_to(V/'storage_cleanup_eleventh_20261009')or p.is_relative_to(R)
  assert is_history,(str(p),hit[:3])
  raw(p);matches.append(dict(path=str(p),matches=[dict(line=i,text=s)for i,s in hit]))
 if p.name.startswith('restore')and p.is_relative_to(V):
  restore_files.append(dict(path=str(p),matching_candidate_literal=any(path in text for path in paths),matching_basename=[n for n in basename if n in text]))
 if p.is_relative_to(A):formal_files+=1
assert all(not x['matching_candidate_literal']and not x['matching_basename']for x in restore_files)
assert not (R/'audit_metadata_retirement_result.json').exists()
for p,row in PINS.items():assert ident(Path(p))=={k:row[k]for k in ident(Path(p))}
report=dict(status='PASS_ARCHIVE_CONTENT_AND_CURRENT_DEPENDENCY_SCOPE_ONLY_AWAIT_FINAL_MANAGEMENT_SOURCE',schema='SPOT_R14_METADATA_ARCHIVES_DEPENDENCY_INDEPENDENT_REVIEW_V1',candidate_count=10,unique_archives=8,manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),plan_sha256='3123063df07044807785f11dff9070cee43452e1442b538fe7df243f8c1159df',source_sha256=hashlib.sha256(source.encode()).hexdigest(),raw_original_logical_bytes=sum(x['raw_bytes']for x in records),raw_original_allocated_bytes=sum(x['raw_allocated_bytes']for x in records),unique_archive_logical_bytes=sum(x['compressed_bytes']for x in archives.values()),unique_archive_allocated_bytes=sum(x['allocated_bytes']for x in archives.values()),all10_originals_still_present_fullSHA_identity_stable=True,all8_gzip_fully_decompressed_fullSHA_size_equal=True,all_candidates_only_pure_metadata_tables_not_scientific_arrays=True,current_graph_canonical35647_namespace86_alias186_and_resource231_path_exclusion=True,current_POST_descriptor35675_and_whole7_2cad_trim73_fed209_full_literal_exclusion=True,all_formal_axial_material_py_examined=formal_files,only_historical_closed_cleanup_or_review_and_newR14_management_source_refs=True,old_source_matches=matches,restore_tool_source_checks=restore_files,candidates=records,archives=list(archives.values()),all_fullread_pins=list(PINS.values()),final_source_review=None,delete_permit=None,actual_retire_tool=None,old_reader_rule='Before reading original historical tables restore exactly matching JSON bytes from permanent R14 archives. Old source/report/seal facts stay unchanged; old inode/ctime cannot be recovered and old whole-project historical snapshots are not asserted current again.',permanent_archives_and_manifest_must_remain=True,formal_ART_written=False,business_or_manage_retire_restore_pack_executed=False,files_deleted=False,scientific_or_native_RSS_credit=False,limits=['Canonical numeric35GB contents are not reread; only already-admitted saved graph metadata and whole actual INPUT/immutable source descriptors are checked for these ten exact storage paths.','Source approval is pending small preservation fixes; this content/dependency PASS alone is not permission to retire.'])
with (H/'archive_and_dependency_review.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],report_sha256=hashlib.sha256((H/'archive_and_dependency_review.json').read_bytes()).hexdigest(),originals=10,archives=8,logical_raw=report['raw_original_logical_bytes'],logical_gzip=report['unique_archive_logical_bytes'],no_business=True)),flush=True)

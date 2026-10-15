import errno,hashlib,json,os,stat,time
from pathlib import Path,PurePosixPath
ROOT=Path('/Users/wen/spot');T=Path('/private/tmp/spot_storage_twelfth_actual_postcleanup_independent_review_20261009');START=time.monotonic()
G=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
data=G.read_bytes();assert hashlib.sha256(data).hexdigest()=='0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3';g=json.loads(data)
base=(T/'REPORT.json').read_bytes();assert hashlib.sha256(base).hexdigest()=='2cc22473372cf6a38e2ec7cb24a72756e34ae10c0dcce83d23620daf799d26e8';assert json.loads(base)['status']=='PASS'
aliases={}
for x in g['aliases']:
 assert x['path']not in aliases;aliases[x['path']]=x
assert len(aliases)==186
for ns in g['namespaces']:
 for n,x in ns['symlinks'].items():
  p=str(Path(ns['root'])/n);v=dict(x,path=p)
  if p in aliases:assert aliases[p]==v
  else:aliases[p]=v
assert len(aliases)==186

def sig(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def resolve(path,kind=None,stack=()):
 assert path.startswith('/')and '..'not in PurePosixPath(path).parts and len(stack)<64
 current='/';parts=PurePosixPath(path).parts[1:];info=None
 for i,part in enumerate(parts):
  candidate=os.path.join(current,part);info=os.lstat(candidate)
  if stat.S_ISLNK(info.st_mode):
   assert candidate in aliases and candidate not in stack
   expected=aliases[candidate];raw=os.readlink(candidate);assert raw==expected['text']
   target=raw if os.path.isabs(raw)else os.path.join(os.path.dirname(candidate),raw)
   current=resolve(os.path.normpath(target),expected['kind'],stack+(candidate,));assert current==expected['target'];info=None
  else:current=candidate
  if i<len(parts)-1:
   if info is None:info=os.lstat(current)
   assert stat.S_ISDIR(info.st_mode)
 if not parts or info is None:info=os.lstat(current)
 assert not stat.S_ISLNK(info.st_mode)
 if kind=='file':assert stat.S_ISREG(info.st_mode)
 if kind=='directory':assert stat.S_ISDIR(info.st_mode)
 return current

def scan_namespace(ns):
 canonical=resolve(ns['root'],'directory');assert canonical==ns['canonical_root'];files=set();dirs=set();links={};pending=[(canonical,'')]
 while pending:
  absolute,relative=pending.pop();before=os.lstat(absolute);assert stat.S_ISDIR(before.st_mode)
  with os.scandir(absolute)as it:entries=list(it)
  for entry in entries:
   rel=entry.name if not relative else relative+'/'+entry.name;s=entry.stat(follow_symlinks=False)
   if stat.S_ISREG(s.st_mode):files.add(rel)
   elif stat.S_ISLNK(s.st_mode):links[rel]=os.readlink(entry.path)
   elif stat.S_ISDIR(s.st_mode):dirs.add(rel);pending.append((entry.path,rel))
   else:raise AssertionError(entry.path)
  assert sig(before)==sig(os.lstat(absolute))
 assert files==set(ns['files']),ns['root'];assert dirs==set(ns['directories']),ns['root'];assert links=={n:v['text']for n,v in ns['symlinks'].items()},ns['root']
 assert resolve(ns['root'],'directory')==canonical
 for n,v in ns['symlinks'].items():assert resolve(str(Path(ns['root'])/n),v['kind'])==v['target']
 return [ns['root'],len(files),len(dirs),len(links)]

def fdidentity(s):return dict(device=s.st_dev,inode=s.st_ino,mode=s.st_mode,rdev=s.st_rdev,major=os.major(s.st_rdev),minor=os.minor(s.st_rdev))
def absence(path):
 current='/';s=os.lstat(current);assert stat.S_ISDIR(s.st_mode);anc=[dict(literal_component='/',canonical_path='/',identity=fdidentity(s))];parts=PurePosixPath(path).parts[1:]
 for i,part in enumerate(parts):
  candidate=os.path.join(current,part);literal='/'+ '/'.join(parts[:i+1])
  try:s=os.lstat(candidate)
  except OSError as e:
   assert e.errno==errno.ENOENT
   return dict(schema='AXMAT_COMBINED_RUNTIME_DECLARED_INPUT_ABSENCE_OBSERVATION_V1',path=path,canonical_absent_path=os.path.join(candidate,*parts[i+1:]),first_missing_component=candidate,missing_errno=errno.ENOENT,existing_ancestors=anc,regular_input_bytes=0,scope='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION',observation='EXACT_DECLARED_ENOENT_ONLY')
  assert i<len(parts)-1
  if stat.S_ISLNK(s.st_mode):assert candidate in aliases and aliases[candidate]['kind']=='directory';current=resolve(candidate,'directory');s=os.lstat(current)
  else:assert stat.S_ISDIR(s.st_mode);current=candidate
  assert stat.S_ISDIR(s.st_mode)and not stat.S_ISLNK(s.st_mode);anc.append(dict(literal_component=literal,canonical_path=current,identity=fdidentity(s)))
 raise AssertionError('declared absent path exists:'+path)

assert len(g['namespaces'])==86 and len(g['absence_inputs'])==445
phase_digests=[]
for stage in ('before','after'):
 ns=[scan_namespace(x)for x in g['namespaces']]
 for x in g['aliases']:assert resolve(x['path'],x['kind'])==x['target']
 observations={p:absence(p)for p in sorted(g['absence_inputs'])};assert observations==g['absence_observations']
 digest=hashlib.sha256(json.dumps([ns,observations],sort_keys=True,separators=(',',':')).encode()).hexdigest();phase_digests.append(digest)
assert phase_digests[0]==phase_digests[1]
R9=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
R9overlap=[x['root']for x in g['namespaces']if str(R9)==x['root']or str(R9).startswith(x['root']+'/')or x['root'].startswith(str(R9)+'/')]
assert R9overlap==[]
assert hashlib.sha256(G.read_bytes()).hexdigest()=='0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
report=dict(schema='SPOT_TWELFTH_POST_CURRENT_GRAPH_NAMESPACE_ALIAS_ABSENCE_METADATA_SUPPLEMENT_V1',status='PASS',scope='FRESH_NAMESPACE_ALIAS_ABSENCE_METADATA_ONLY_NOT_SECOND_35GB_FRESH_BYTE_PASS',base_actual_post_report_sha256=hashlib.sha256(base).hexdigest(),current_graph_sha256=hashlib.sha256(data).hexdigest(),all86_exhaustive_namespace_files_links_dirs_exact_before_after=True,all186_explicit_literal_alias_targets_kinds_exact_before_after=True,all445_exact_ENOENT_ancestors_and_first_missing_component_observations_equal_before_after=True,phase_observation_digests=phase_digests,namespace_observations=ns,R9_review_archive_overlaps_exhaustive_namespace_roots=R9overlap,R9_new_pre_cleanup_full_PREP_archiving_not_cache_mutation=True,current_input_byte_SHA_read_credit_not_repeated=True,whole_fresh_graph_byte_PASS_claimed_by_this_supplement=False,no_business_import_or_API_or_PREP_RUN_or_cleaner_or_restore=True,no_formal_ART_write_or_delete=True,elapsed_seconds=time.monotonic()-START)
with (T/'current_graph_metadata_supplement.json').open('x')as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',namespaces=86,aliases=186,absences=445,R9ns_overlap=0,report_sha256=hashlib.sha256((T/'current_graph_metadata_supplement.json').read_bytes()).hexdigest(),elapsed_seconds=report['elapsed_seconds'])))

import argparse, collections, hashlib, json, os, shutil, stat, subprocess, time
from pathlib import Path
from datetime import datetime, timezone
if not __debug__:
 raise RuntimeError('Cleanup safety gates require Python optimization to be disabled')
ROOT=Path('/Users/wen/spot');OUT=ROOT/'validation/storage_cleanup_ninth_20261009'
def safe_art_path(raw):
 p=Path(raw)
 if not p.is_absolute() or str(p)!=raw or '..' in p.parts or not p.is_relative_to(ROOT/'validation/artifacts') or p.parent.resolve(strict=True)!=p.parent:
  raise ValueError('Noncanonical artifact path: '+raw)
 return p
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p):
 p=Path(p);a=identity(p);assert stat.S_ISREG(a[2]),str(p);h=hashlib.sha256()
 with p.open('rb') as f:
  assert [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino]==a[:2]
  while b:=f.read(4*1024**2):h.update(b)
 assert identity(p)==a,str(p)
 return dict(path=str(p),identity=a,sha256=h.hexdigest(),size=a[3])
def write(name,value):
 p=OUT/name
 with p.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 return pin(p)
def inventory(excluded):
 h=hashlib.sha256();counts=collections.Counter()
 for dp,dn,fn in os.walk(ROOT,followlinks=False):
  dn[:]=sorted(n for n in dn if Path(dp)/n!=OUT)
  for n in sorted(dn+fn):
   p=Path(dp)/n
   if str(p) in excluded:continue
   s=p.lstat();relative=str(p.relative_to(ROOT))
   if stat.S_ISLNK(s.st_mode):row=[relative,identity(p),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISDIR(s.st_mode):row=[relative,'directory'];counts['directories']+=1
   elif stat.S_ISREG(s.st_mode):row=[relative,identity(p)];counts['regular_files']+=1
   else:raise ValueError(str(p))
   h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),**dict(counts))
def links(selected):
 rows=[]
 for dp,dn,fn in os.walk(ROOT,followlinks=False):
  for n in dn+fn:
   p=Path(dp)/n
   if p.is_symlink():
    target=p.resolve(strict=False)
    assert not any(Path(q)==target or Path(q).is_relative_to(target) for q in selected),(str(p),str(target))
    rows.append([str(p),os.readlink(p),str(target)])
 return dict(count=len(rows),sha256=hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest())
def capacity():return dict(project_allocated_bytes=int(subprocess.check_output(['/usr/bin/du','-k','-s',str(ROOT)],text=True).split()[0])*1024,disk_free_bytes=shutil.disk_usage(ROOT).free)
def expected(record):
 p=pin(record['path'])
 assert p['identity']==record['identity'] and p['sha256']==record['sha256'] and p['size']==record['size'],record['path']
 return p
def closure(m,selected):
 gp=expected(m['graph_pin']);ip=expected(m['old_index_pin'])
 graph=json.loads(Path(gp['path']).read_text());index=json.loads(Path(ip['path']).read_text());absolute=set()
 def walk(value):
  if isinstance(value,dict):
   for k,v in value.items():walk(k);walk(v)
  elif isinstance(value,list):
   for v in value:walk(v)
  elif isinstance(value,str) and value.startswith('/'):absolute.add(value)
 walk(graph)
 directories=set(x['canonical_root'] for x in graph['namespaces'])|set(x['target'] for x in graph['aliases'] if x['kind'] in ('directory','dir'))|set(index['protected_directories'])|set(m['critical_roots'])
 files=absolute|set(index['protected_files'])|set(index['inbound_alias_targets'])
 files |= set(m['current_cold_extra_protected_files'])
 for p in selected:
  assert p not in files and not any(p==d or p.startswith(d+'/') for d in directories),p
 return dict(canonical_files=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),live_resource_roots=len(graph['live_resource_roots']),old_protected_files=len(index['protected_files']),critical_roots=len(m['critical_roots']),candidate_intersections=[])
def verify_candidates(m):
 out=[];retained={p['path']:p for p in m['retained_primaries']}
 for c in m['candidates']:
  p=safe_art_path(c['path']);assert not p.is_symlink()
  fresh=expected(c);assert fresh['identity'][-1]==1
  assert p.stat().st_blocks*512==c['allocated_bytes']
  if c['category']=='EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR':
   assert c['restoration_recipe_sha256']==pin(OUT/'tar/candidate.json')['sha256']
   proc=subprocess.run(['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(OUT/'restore_retired_tar.py')],check=True,capture_output=True,text=True)
   proof=json.loads(proc.stdout);assert proof['status']=='PASS' and proof['restored'] is False and proof['archive_sha256']==fresh['sha256']
  elif c['category']=='TERMINAL_OLD_INTERMEDIATE_PAYLOAD':
   relative=p.relative_to(ROOT/'validation/artifacts')
   allowed_map=(relative.parts[0]=='axial-material-production-qualified-AB-compensated-20261004' and relative.parts[1]=='AAA' and relative.parts[2] in ('map001','map002','map003') and len(relative.parts)==4 and relative.name in ('candidate_radial.xsm','candidate_snapshots.xsm','projected_proposal.xsm'))
   allowed_tape=(relative.parts[0] in ('d4a-final-four-fuel-temperature-run-20261002','d4a-remaining-fuel-temperature-run-20261001','d4a-remaining-temperature-run-20261001') and relative.name=='tape30' and relative.parent.name in ('pendf','groupr'))
   assert allowed_map or allowed_tape,str(p)
   proof=c['historical_payload_proof'];historic=pin(proof['path']);assert historic['sha256']==proof['sha256']
   record=json.loads(Path(proof['path']).read_text())
   if proof['format']=='JSON_SHA256_MAP':
    assert allowed_map and record['classification']=='SEALED_STAGE_OUTPUTS' and proof['key']==p.name
    assert Path(proof['path'])==p.parent/'result.json' and record['sha256'][proof['key']]==fresh['sha256']
   elif proof['format']=='NJOY_RECEIPT_OUTPUT':
    assert allowed_tape and Path(proof['path'])==p.parent/'receipt.json'
    assert type(record['returncode']) is int and record['returncode']==0 and record['output_sha256']==fresh['sha256']
    seal=pin(proof['result_manifest_path']);assert seal['sha256']==proof['result_manifest_sha256']
    entries={line.split('  ',1)[1]:line.split('  ',1)[0] for line in Path(proof['result_manifest_path']).read_text().splitlines() if line}
    owner=Path(proof['result_manifest_path']).parent
    assert owner==ROOT/'validation/artifacts'/relative.parts[0] and entries[str(p.relative_to(owner))]==fresh['sha256']
   else:raise ValueError('unrecognized historical payload proof')
  else:
   primary=retained[c['retained_primary']]
   assert primary['sha256']==fresh['sha256'] and primary['size']==fresh['size'] and primary['path']!=fresh['path']
  out.append(fresh)
 return out
def main():
 start=time.monotonic();parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['preflight','apply']);parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--preflight-sha256');parser.add_argument('--independent-sha256');args=parser.parse_args()
 mp=pin(OUT/'manifest.json');assert mp['sha256']==args.manifest_sha256
 m=json.loads((OUT/'manifest.json').read_text());selected={c['path'] for c in m['candidates']}
 assert len(selected)==len(m['candidates'])==m['exact_count'] and 0<len(selected)<=2000
 assert not selected & {p['path'] for p in m['retained_primaries']}
 assert sum(c['allocated_bytes'] for c in m['candidates'])==m['allocated_bytes']
 assert sum(c['size'] for c in m['candidates'])==m['logical_bytes']
 assert pin(Path(__file__))['sha256']==m['cleanup_source_sha256']
 for c in m['candidates']:assert c['category'] in ('EXACT_DUPLICATE_OLD_WORK_COPY','EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR','TERMINAL_OLD_INTERMEDIATE_PAYLOAD')
 for p in m['source_and_review_pins']:expected(p)
 kept=[expected(p) for p in m['retained_primaries']]
 close=closure(m,selected);link=links(selected)
 if args.mode=='preflight':
  before=inventory(selected);candidates=verify_candidates(m);after=inventory(selected);assert before==after
  value=dict(schema='SPOT_NINTH_ROOT_FRESH_EXACT_CONTENT_PREFLIGHT_V1',status='PASS',utc=datetime.now(timezone.utc).isoformat(),manifest_sha256=mp['sha256'],verified_candidates=candidates,verified_primaries=kept,preservation_baseline=before,symlink_screen=link,current_closure=close,capacity=capacity(),files_deleted=0,solver_or_API_executed=False)
  result=write('preflight.json',value)
  print(json.dumps(dict(status='PASS',mode='preflight',report=result['path'],sha256=result['sha256'],candidates=len(candidates),allocated_gib=m['allocated_bytes']/2**30,baseline=before)));return
 assert args.preflight_sha256 and args.independent_sha256
 pp=pin(OUT/'preflight.json');assert pp['sha256']==args.preflight_sha256
 rp=pin(OUT/'independent_preflight_review.json');assert rp['sha256']==args.independent_sha256
 pf=json.loads((OUT/'preflight.json').read_text());rv=json.loads((OUT/'independent_preflight_review.json').read_text())
 assert pf['status']=='PASS' and rv['status']=='PASS' and rv['manifest_sha256']==mp['sha256'] and rv['preflight_sha256']==pp['sha256']
 assert pf['manifest_sha256']==mp['sha256']
 assert not (OUT/'cleanup_result.json').exists() and not (OUT/'retirement_ledger.jsonl').exists()
 baseline=inventory(selected);assert baseline==pf['preservation_baseline']
 actual=verify_candidates(m);assert actual==pf['verified_candidates']
 before=capacity()
 with (OUT/'retirement_ledger.jsonl').open('x') as ledger:
  for c,fresh in zip(m['candidates'],actual):
   p=safe_art_path(c['path']);assert identity(p)==fresh['identity']
   p.unlink()
   ledger.write(json.dumps(dict(**fresh,category=c['category'],deleted=True),separators=(',',':'))+'\n');ledger.flush();os.fsync(ledger.fileno())
 assert all(not Path(q).exists() and not Path(q).is_symlink() for q in selected)
 after_inventory=inventory(selected);assert after_inventory==baseline
 assert links(selected)==link
 for p in m['retained_primaries']+m['source_and_review_pins']+[m['graph_pin'],m['old_index_pin']]:expected(p)
 result=dict(schema='SPOT_NINTH_ACTUAL_EXACT_OLD_WORK_RETIREMENT_V1',status='PASS',utc=datetime.now(timezone.utc).isoformat(),manifest_sha256=mp['sha256'],preflight_sha256=pp['sha256'],independent_preflight_sha256=rp['sha256'],deleted_files=len(selected),deleted_logical_bytes=m['logical_bytes'],deleted_allocated_bytes=m['allocated_bytes'],capacity_before=before,capacity_after=capacity(),nonselected_before=baseline,nonselected_after=after_inventory,symlink_check_after=link,all_retained_primaries_and_source_review_bytes_unchanged=True,solver_or_API_executed=False,new_scientific_credit=False,elapsed_seconds=time.monotonic()-start)
 saved=write('cleanup_result.json',result)
 print(json.dumps(dict(status='PASS',mode='apply',report=saved['path'],sha256=saved['sha256'],deleted_files=len(selected),deleted_allocated_gib=m['allocated_bytes']/2**30,project_after_gib=result['capacity_after']['project_allocated_bytes']/2**30,nonselected_unchanged=True)))
if __name__=='__main__':main()

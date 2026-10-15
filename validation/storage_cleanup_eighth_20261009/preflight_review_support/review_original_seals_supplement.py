from pathlib import Path
import json,hashlib,re,os,stat
root=Path('/Users/wen/spot'); b=root/'validation/storage_cleanup_eighth_20261009';out=Path('/private/tmp/spot_eighth_cleanup_independent_source_review_20261009');m=json.loads((b/'manifest.json').read_text());r=json.loads((b/'replay/candidate_exact_restoration_mapping.json').read_text());c=json.loads((b/'compiled/exact_compiled_candidates.json').read_text());bound={x['path']:x for x in m['source_and_review_pins']};fresh={}
def content(p):
 p=Path(p);s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink];assert stat.S_ISREG(a[2]);raw=p.read_bytes();s=p.lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==a;h=hashlib.sha256(raw).hexdigest();fresh[str(p)]={'path':str(p),'identity':a,'size':len(raw),'sha256':h};return raw.decode()
def exact_entry(p,wanted,declared):
 text=content(p);rp=bound[str(p)];assert fresh[str(p)]['sha256']==rp['sha256'] and fresh[str(p)]['identity']==rp['identity'];hits=[]
 for n,line in enumerate(text.splitlines(),1):
  mt=re.fullmatch(r'([0-9a-f]{64})\s+(.+)',line)
  if mt and mt[1]==wanted:
   name=mt[2].lstrip('*'); path=Path(name) if name.startswith('/')else(root/name if name.startswith('validation/')else Path(p).parent/name)
   if os.path.normpath(str(path))==declared:hits.append(n)
 assert hits,(p,declared);return hits
checks=[]
for row in r['candidates']:
 for k,path in [('candidate_original_seal_entries',row['path']),('primary_original_seal_entries',row['restoration_primary']['path'])]:
  seals=row[k];assert seals
  for s in seals:
   assert s['entry_sha256']==row['sha256'] and s['canonical_declared_path']==path
   assert s['line'] in exact_entry(s['manifest'],row['sha256'],path)
   checks.append({'candidate':row['path'],'role':k,'manifest':s['manifest'],'line':s['line'],'exact_original_path_and_SHA_entry':True})
proof=c['original_proofs'];df='df83931c4ba0e5f5a7dfa534438967536a71d82e62e77ba4fc6bcb2e8f19f84a';dv='2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db'
p=Path(proof['gmres_original_installed_executable_SHA']['path']);text=content(p);assert text.strip()==df+'  bin/Darwin_arm64/Dragon';assert str(p)in bound;assert '/source/bin/Darwin_arm64/Dragon' in m['candidates'][10]['retained_primary']
make=content(proof['gmres_local_link_then_install_copy_source']['path']);assert 'Dragon: libDragon.a DRAGON.o $(bin)/ sub-make\n' in make and '\tcp $@ $(bin)/$@\n' in make
receipt=content(proof['gmres_original_build_receipt']['path']);assert 'bin/Darwin_arm64/Dragon\t'+df in receipt
exact_entry(proof['observables_original_result_manifest']['path'],dv,m['candidates'][11]['path'])
exact_entry(proof['picard_original_result_manifest']['path'],dv,m['candidates'][12]['path'])
exact_entry(proof['release_original_manifest']['path'],dv,m['candidates'][11]['retained_primary'])
for p,v in fresh.items():
 if p in bound:assert all(v[k]==bound[p][k]for k in ('sha256','identity','size'))
t=json.loads(content(b/'preflight_terminal_observation.json'));assert t['exit_code']==0 and t['closed'] is True and t['actual_stdout_status']=='PASS' and t['initial_chunk_id']=='d5a6fb' and t['terminal_chunk_id']=='9c6ead' and t['manifest_sha256']=='dcc76b4a6f6cdacd52edcaf004d206d64018f0d7b72b4f9e303e1aacf8529e8a' and t['preflight_sha256']=='450db036dff5b651a7b1a72d98217b7320023cea8ff5688f220e33a95a719f26' and t['source_sha256']==m['cleanup_source_sha256'] and t['files_deleted']==0 and t['solver_or_API_executed'] is False
v=json.loads(content(b/'restore_default_list_verification.json'));assert v['status']=='PASS_DEFAULT_LIST_NO_RESTORE' and v['actual_subprocess_exit_code']==0 and v['exact_rows']==13 and v['restore_or_deletion_executed'] is False and v['source_sha256']=='53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd'
pf=out/'independent_preflight_review.json';rep={'status':'PASS_SUPPLEMENT_ORIGINAL_SEALS_AND_ACTUAL_TOOL_RETURN_SEMANTICS','independent_full_preflight_review_sha256':hashlib.sha256(pf.read_bytes()).hexdigest(),'manifest_sha256':t['manifest_sha256'],'preflight_sha256':t['preflight_sha256'],'root_actual_preflight_true_exit_0_closed':True,'default_restore_actual_subprocess_0_list_13_no_restore':True,'native_replay_original_exact_path_seal_entries_checked':checks,'native_original_seal_entry_count':len(checks),'compiled_original_manifest_exact_path_and_SHA_entries_checked':3,'gmres_makefile_Dragon_target_cp_automatic_variable_install_and_original_bin_receipt_checked':True,'gmres_source_build_target_has_no_own_seal_row_and_fresh_whole_source_bin_equality_is_restoration_evidence_only':True,'fresh_source_and_seal_pins':list(fresh.values()),'files_deleted':0,'restore_executed':False,'business_import_API_PREP_RUN_solver_executed':False,'formal_or_ART_written':False};p=out/'original_seals_and_true_tool_return_supplement.json'
with p.open('x')as f:json.dump(rep,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':rep['status'],'report':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_exact_original_seal_entries':len(checks),'compiled_original_sealed_paths':3,'fresh_seal_and_source_files':len(fresh)}))

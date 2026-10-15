"""Exact36 fixed-plan byte/identity check only; no business, no deletion."""
import hashlib,json,os,stat,time
from pathlib import Path
D=Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009')
ROOTPLAN=Path('/private/tmp/spot_storage_nineteenth_root_20261009/fixed_candidate_plan.json')
SHA='b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
PINS={};START=time.monotonic()
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,wanted):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])and p.resolve(strict=True)==p
 h=hashlib.sha256()
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
  while block:=f.read(4*2**20):h.update(block)
 assert identity(p)==before and h.hexdigest()==wanted,str(p)
 PINS[str(p)]=dict(path=str(p),identity=before,bytes=before[3],sha256=wanted);return PINS[str(p)]
def read(p,wanted):pin(p,wanted);return json.loads(Path(p).read_bytes())
plan=read(ROOTPLAN,SHA)
before=read(D/'REPORT.json','0473a770f97ecd65ef066aef12729478932d784c7aa4f22e42b138e46491e960')
assert before['status']=='CURRENT_INDEX_EXCLUDED_PENDING_GLOBAL_LINK_RESTORE_AND_ORIGINAL_SOURCE_REVIEW'
regular={r['path']:r for r in before['proposed_regular18']};links={r['path']:r for r in before['proposed_related_symlink18']}
assert {r['path']for r in plan['regular']}==set(regular)and {r['path']for r in plan['symlinks']}==set(links)
for row in plan['regular']:
 old=regular[row['path']];assert row['identity']==old['identity']and row['sha256']==old['original_expected_SHA256']
 assert row['original_stage_seal']==old['original_seal']['path']and row['original_stage_seal_sha256']==old['original_seal']['sha256']
 seal=read(row['original_stage_seal'],row['original_stage_seal_sha256'])
 assert seal['classification']=='SEALED_STAGE_OUTPUTS'and seal['sha256']['closed_snapshots.xsm']==row['sha256']
 assert identity(row['path'])==row['identity'];pin(row['path'],row['sha256'])
 assert identity(row['path'])==row['identity']and row['identity'][6]==1
for row in plan['symlinks']:
 old=links[row['path']];assert row['identity']==old['identity']and row['link_text']==old['literal_link_text']and row['target']==old['target']
 p=Path(row['path']);assert stat.S_ISLNK(p.lstat().st_mode)and identity(p)==row['identity']and os.readlink(p)==row['link_text']and str(p.resolve(strict=True))==row['target']
assert plan['logical_bytes']==sum(row['identity'][3]for row in plan['regular'])==4283202816
assert plan['allocated_bytes']==sum(row['allocated_bytes']for row in plan['regular'])==4283228160
assert plan['old_historical_seals_not_asserted_complete']is True
assert plan['all_existing_bootstrap_last_two_maps_and_other_results_kept']is True
for row in before['preserve_last_three_closed_snapshots']:assert identity(row['path'])==row['identity']
for p,row in PINS.items():assert identity(p)==row['identity']
report=dict(schema='SPOT_R19_EXACT36_EARLY_MAP_FIXED_PLAN_INDEPENDENT_FULLSHA_REVIEW_V1',status='PASS_BYTE_AND_CURRENT_INDEX_SCOPE_PENDING_COMPLEMENTARY_DEPENDENCY',
 fixed_plan=PINS[str(ROOTPLAN)],current_dependency_report=PINS[str(D/'REPORT.json')],regular_count=18,related_symlink_count=18,
 fresh_candidate_fullSHA_original_SEALED_STAGE_OUTPUTS_equal=True,fresh_candidate_fullSHA_bytes=4283202816,
 full_candidate_seven_identity_before_after_equal=True,related_symlink_literal_identity_and_target_exact=True,
 current37395_canon35647_ns86_alias186_absence445_exact_excluded=True,last_three_closed_states_unchanged=True,
 original_historical_full_seal_reverification_not_claimed=True,
 remaining_approval_scopes=['Current actual native dynamic snapshot producer read path','Prior restore-master exclusion','Root genuine global incoming-symlinks preflight'],
 files_deleted=0,project_written=False,business_executed=False,old35GB_rehashed=False,scientific_credit=False,
 exact_fullSHA_pins=PINS,elapsed_seconds=time.monotonic()-START)
p=D/'EXACT_FIXED_PLAN_FULLSHA_REPORT.json'
with p.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(status=report['status'],report=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),regular_count=18,symlink_count=18,elapsed_seconds=report['elapsed_seconds'])))

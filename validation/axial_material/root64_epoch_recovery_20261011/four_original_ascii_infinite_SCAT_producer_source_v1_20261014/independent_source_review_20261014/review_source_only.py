"""Independent frozen Source/metadata review; no science payload reads or calls."""
import ast, hashlib, json, os, stat, time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
 fresh_bytes=2147483648, history_bytes=103079215104,
 cold_reserve_bytes=20971764748, metadata_reserve_bytes=67108864,
 free_floor_bytes=8589934592, threads=1, children_at_once=1, retries=0)
FLAGS = ('business_executed','numerical_executed','compiler_executed','files_deleted')
PHYSICS = ('physics_qualified','scientific_accuracy_qualified',
 'complete_reaction_authority_qualified','physical_neutron_balance_qualified',
 'unreduced_reference_qualified','finite18_replayed','temperature_interpolation_replayed',
 'current_SPH_MASK_context_applied','AAA_qualified','ABA_admitted','goal_complete')
READY = dict(path=str(BASE/'SOURCE_REVIEW_READY.json'),
 sha256='f5a91cbe557a5c88bfd5850400528ececf3841d15d8821b5d356e51e4987eab2',
 size_bytes=178200, identity=[16777229,50396951,33188,1,178200,1791993797801749969,1791993797801749969])
GEN = dict(path=str(BASE/'ACTUAL_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json'),
 sha256='4833aca485c2dd60bcf3affcf6f7136f8f94a1caec44f8e7c858562cdecb2459',
 size_bytes=1431, identity=[16777229,50397031,33188,1,1431,1791993855270108924,1791993855270108924])

def require(ok, text):
 if type(ok) is not bool or not ok: raise RuntimeError(text)
def identity(s):
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'},'exact fullPF schema')
 q=Path(p['path']);s=q.lstat()
 role=(str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'
       and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'
       and p['identity'][3]==2)
 require(q.is_absolute() and not any(x.is_symlink() for x in (q,*q.parents))
   and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if role else 1)
   and identity(s)==p['identity'] and s.st_size==p['size_bytes'],'exact current7/fullPF '+str(q))
def whole(p):
 current(p); require(p['size_bytes']<8*2**20,'only bounded Source/metadata complete SHA')
 q=Path(p['path'])
 with q.open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened metadata7')
  raw=f.read();require(identity(os.fstat(f.fileno()))==p['identity'],'metadata EOF7')
 require(len(raw)==p['size_bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],'full Source/metadata SHA '+str(q))
 current(p); return raw
def pin(q):
 q=Path(q);s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(p):return json.loads(whole(p))
def function_bytes(raw, name):
 text=raw.decode(); tree=ast.parse(text);lines=text.splitlines(keepends=True)
 matches=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
 require(len(matches)==1,'one exact Source definition '+name);n=matches[0]
 return ''.join(lines[n.lineno-1:n.end_lineno]).rstrip('\n').encode()
def inverse(p):
 a=whole(p['original_full_pin']);b=whole(p['candidate_full_pin']);out=bytearray();at=0
 for e in p['edit_map']:
  i,j,k,l=[e[x] for x in ('original_begin_byte','original_end_byte','candidate_begin_byte','candidate_end_byte')]
  require(a[i:j]==bytes.fromhex(e['original_bytes_hex']) and b[k:l]==bytes.fromhex(e['candidate_bytes_hex']) and at<=k,'actual inverse byte slices')
  out.extend(b[at:k]);out.extend(a[i:j]);at=l
 out.extend(b[at:]);require(bytes(out)==a and hashlib.sha256(out).hexdigest()==p['whole_original_reconstructed_sha256'] and p['complete_inverse_reconstructed_original'] is True,'complete original whole byte reconstruction')

def main():
 started=time.monotonic();selected=[];failure=None;facts={}
 try:
  ready=read(READY);gen=read(GEN)
  require(ready['source_only'] is True and ready['actual_business_started'] is False
    and ready['Root_final_publication_executed'] is False and ready['scientific_payload_read'] is False
    and all(ready[k] is False for k in FLAGS+PHYSICS),'Source-only false qualifiers')
  selected=ready['selected_Source_pins']+[READY,GEN]
  require(ready['selected_Source_pins']==ready['dependencies'] and len(ready['dependencies'])==191
    and len({p['path'] for p in selected})==193,'exact191 dependencies plus ready/generation')
  for p in selected:whole(p)
  ret=gen['actual_Source_preparation_return']
  require(gen['observed_closed'] is True and type(gen['original_integer_exit_code']) is int and gen['original_integer_exit_code']==0
    and type(ret['exit_code']) is int and ret['exit_code']==0 and ret.get('session_id') is None
    and type(ret['output']) is str,'genuine Source preparation typedclosed0')
  receipt=json.loads(ret['output'].strip().splitlines()[-1])
  require(receipt['ready_pin']==READY and receipt['status']=='FOUR_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_PREPARATION_ONLY'
    and all(receipt[k] is False for k in FLAGS+PHYSICS),'original generation stdout binds frozen ready')
  plan=read(ready['control_plan_pin']);prior=read(plan['selected_prior45_plan_pin']);old=read(plan['selected_original_ASCII_plan_pin'])
  roots=plan['complete_joint_roots']
  require(plan['source_only'] is True and all(plan[k] is False for k in FLAGS+PHYSICS)
    and plan['original_caps']==ready['original_caps']==prior['original_caps']==old['original_caps']==CAPS,'original exact caps and false scope')
  require(len(roots)==len(set(roots))==47 and roots==prior['complete_joint_roots']+[str(BASE),plan['planned_actual_output_root']]
    and len(prior['complete_joint_roots'])==45 and prior['complete_joint_roots'][:44]==old['complete_joint_roots']
    and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'original45/44 prefix plus Source/output47')
  require(len(plan['explicit_cumulative_metadata_file_pins'])==179
    and all(p in ready['dependencies'] for p in plan['explicit_cumulative_metadata_file_pins']),'all179 metadata fullpins protected')
  require(not Path(plan['planned_actual_output_root']).exists()
    and all(not (BASE/n).exists() for n in ('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')),'no business or premature final publication')
  proof=read(plan['original_whole_math_inverse_proof_pin'])
  require(proof['source_only'] is True and proof['scientific_payload_read'] is False
    and all(proof[k] is False for k in FLAGS+PHYSICS),'original Source-only inverse proof')
  for c in proof['whole_original_source_copies']:
   a=whole(c['original_full_pin']);b=whole(c['whole_unchanged_copy_full_pin']);require(a==b,'six whole original Source copies unchanged')
  scalar=whole(plan['original_scalar_helper_source_copy_pin']);dragr=whole(proof['actual_original_producer_dragr_Source_full_pin'])
  require(hashlib.sha256(dragr).hexdigest()=='047ed05e54c54aad2681ce1796bec72f47a0118a2d80295d0d9929e4e42381ac','actual producer original dragr Source')
  for row in proof['original_scalar_functions_called_unchanged']:
   raw=function_bytes(scalar,row['name']);require(raw==bytes.fromhex(row['original_complete_definition_bytes_hex']) and hashlib.sha256(raw).hexdigest()==row['original_complete_definition_sha256'] and row['called_unchanged'] is True,'seven unchanged scalar definitions')
  for row in proof['whole_original_math_source_blocks']:
   raw=dragr[row['begin_byte']:row['end_byte']];require(raw==bytes.fromhex(row['original_statement_bytes_hex']) and hashlib.sha256(raw).hexdigest()==row['sha256'],'whole drasc/fmatr/limits/drahd exact bytes')
  worker=whole(next(p for p in ready['complete_source_file_pins'] if Path(p['path']).name=='compare_four_original_ascii_infinite_SCAT.py'))
  host=whole(ready['host_source_pin']);writer=whole(ready['final_publisher_Source_pin'])
  for row in proof['minimal_infinite_P0_adapter_source_statements']:
   raw=worker[row['begin_byte']:row['end_byte']];require(raw==bytes.fromhex(row['bytes_hex']) and hashlib.sha256(raw).hexdigest()==row['sha256'],'literal compact P0/packing/energy adapter byte slices')
  inverse(proof['host_complete_byte_inverse']);inverse(proof['publisher_complete_byte_inverse'])
  for raw in (worker,host,writer):ast.parse(raw)
  wt=worker.decode();ht=host.decode();pub=writer.decode()
  for text in ("MTS=(2,5,16,17,28,37,*range(51,92))", "ngther=min(ngther,igrest)", "if ig==370:break", "reverse=True", "total[first:,:]+=value[first:,:]", "total[first:,:]-=value[first:,:]", "for mt in MTS:", "total+=value", "scalar.packed(total,False,(0,0),total)", "payload[::active['nl']*active['nz']]", "matrix(section);return value[0,0],flux[0,0]", "struct.pack('<f',actual)", "all exact actual sections/grids and eightT replay", "whole original ASCII EOF SHA/size", "whole compressed primary EOF SHA/size", "require(exact,'actual original infinite P0 packed mismatch retained; no retry')"):
   require(text in wt,'reviewed infinite-only original order/source guard '+text)
  require('math.fsum(' not in wt and '.sum(' not in wt and 'subprocess' not in wt,'no reduced diagnostic sum/native call substituted')
  require("len(roots)==47" in ht and "600" in ht and 'OwnRSSSerialExecutor' in ht
    and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)' in ht
    and "runner.execute(stage,'four_original_ASCII_32T_infinite_P0_SCAT',cmd,600)" in ht
    and "len(runner.records)==1" in ht,'same original owning actual class/MRO onechild600')
  originals=[c for c in proof['whole_original_source_copies'] if Path(c['whole_unchanged_copy_full_pin']['path']).name=='original_guard_host.py']
  require(len(originals)==1,'one original host copy');oldht=whole(originals[0]['whole_unchanged_copy_full_pin']).decode()
  start=' class Resources:';end=' resources=Resources();'
  require(ht[ht.index(start):ht.index(end)]==oldht[oldht.index(start):oldht.index(end)],'whole original Resources methods unchanged')
  require("peer['source_only']is True" in pub and "peer['status'].startswith('PASS')" in pub
    and "peer['failure']is None" in pub and "all(contains(peer,p)for p in selected)" in pub
    and "type(t['exit_code'])is int and t['exit_code']==0" in pub
    and "gd['ready_pin']==pready" in pub and "not any(os.path.lexists(q)for q in targets)" in pub
    and "len(prefix)==11" in pub and "'--source-freeze-summary'" in pub
    and "'--host-freeze-summary'" in pub,'Root-only once writer true roletriple/selected scope/CLI24')
  require(len(ready['original_complete_ENV_Python_B_prefix'])==11 and ready['original_complete_ENV_Python_B_prefix'][-1]=='-B','whole original ENV Python -B prefix')
  sci=plan['actual_current_SCI1_pin'];current(sci)
  require(sci['sha256']=='e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc' and sci['size_bytes']==210627112,'original current SCI1 fullpin only; no payload reread')
  evidence=read(plan['actual_original_ASCII_evidence_pin']);post=read(plan['actual_original_ASCII_independent_post_pin']);tools=read(plan['actual_original_ASCII_independent_post_tools_pin'])
  require(evidence['status']=='ACTUAL_ALL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY'
    and post['status'].startswith('PASS') and post['failure'] is None
    and post['actual_original_decompressed_payload_bytes']==284814387
    and tools['observed_closed'] is True and type(tools['actual_review_return']['exit_code']) is int
    and tools['actual_review_return']['exit_code']==0
    and json.loads(tools['actual_review_return']['output'])['review_pin']==plan['actual_original_ASCII_independent_post_pin'],'actual four original fullEOF independent post context')
  require([r['nuclide'] for r in plan['inputs']]==['Am241','Pu238','Pu239','Pu240'] and plan['inputs']!=[], 'exact four original nucleus order')
  cohorts=[]
  for row, ex in zip(plan['inputs'],evidence['actual_extractions']):
   inv=read(row['actual_complete_inventory_pin']);current(row['gzip_primary_current_full_pin'])
   require(row['actual_complete_inventory_pin']==ex['complete_inventory_pin']
     and row['historical_original_ASCII_sha256']==inv['actual_decompressed_SHA256']==ex['actual_decompressed_SHA256']
     and inv['current_gzip_primary_full_pin']==row['gzip_primary_current_full_pin']
     and inv['original_ASCII_fullEOF_validated'] is True,'same genuine source bodies already independently verified')
   grids=inv['original8_MF1_grids'];require(len(grids)==8 and len({g['temperature_K'] for g in grids})==8,'all8 actual grids')
   require(row['original_ipflag']==0 and row['original_nimpo_unit']==29 and row['original_nexpo_unit']==30
     and row['original_drahd_existing_ENERGY_REAL32_branch'] is True and row['original_thermal_cutoff_eV']==4.0,'exact original imported ENERGY branch/cutoff/pfflag0')
   deck=whole(row['historical_proof']['actual_DRAGR_deck_pin']).decode()
   require('-21 -23 -25 0 0  29  30 0 1 0 1/' in deck and '4.000000 /' in deck,'literal original two-pass high DRAGR deck')
   seq=[];dims=set();all_dims=set();thermals=[]
   for s in inv['actual_sections']:
    if not seq or seq[-1]!=s['temperature_K']:seq.append(s['temperature_K'])
    all_dims.add((s['nl'],s['nz']))
    if s['mf']==6:dims.add((s['nl'],s['nz']))
    if s['mf']==6 and s['mt']==221:thermals.append(s)
   require(seq==[g['temperature_K'] for g in grids] and dims<={(1,10),(2,1),(2,10)}
     and len(thermals)==8 and {s['temperature_K'] for s in thermals}==set(seq)
     and all(s['nl']==2 and s['nz']==1 and 370 in s['incident_groups_present'] for s in thermals),'actual oneT order/3 allowed dimensions/thermal221 eachT sentinel')
   require(set(row['all_actual_MF6_MTs'])=={s['mt'] for s in inv['actual_sections'] if s['mf']==6} and 18 in row['all_actual_MF6_MTs'],'complete actual MF6 inventory including fission separately')
   cohorts.append(dict(nuclide=row['nuclide'],actual_temperature_count=8,actual_sections=len(inv['actual_sections']),actual_MF6_dimension_pairs=sorted(dims),actual_all_MF_dimension_pairs=sorted(all_dims),thermal221_sections=8,original_nimpo29_imported_REAL32_ENERGY_branch=True))
  retirement=read(plan['actual_precise_retirement_receipt_pin'])
  require(retirement['mode']=='execute' and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'
    and retirement['failure'] is None and retirement['actual_released_bytes']==405417320
    and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4
    and all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']),'original exact retirement edge only')
  total=0
  for root in roots:
   p=Path(root)
   if not p.exists():continue
   for q in p.rglob('*'):
    s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'cumulative roots no aliases')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
  outer=sum(p['size_bytes'] for p in plan['explicit_cumulative_metadata_file_pins'] if not any(Path(p['path']).is_relative_to(Path(r)) for r in roots))
  require(total+outer<2*2**30,'actual all47 roots plus explicit outer metadata below original2GiB')
  facts=dict(actual_cohorts=cohorts,whole_source_and_metadata_fullpin_count=193,
    science_file_current7_only_pins=[sci]+[r['gzip_primary_current_full_pin'] for r in plan['inputs']],
    complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],
    observed_cumulative_root_bytes=total,observed_explicit_outer_metadata_bytes=outer,
    observed_total_cumulative_bytes=total+outer,original_caps=CAPS,
    exact_original47_MT_order=True,actual_thermal221_first_then_elastic_infinite_subtraction=True,
    ngther_scan_original370_sentinel_only=True,original_imported_REAL32_ENERGY_cutoff_branch=True,
    unchanged_scalar_matrix_and_infinite_packed_functions=True,original_P0_z0_projection_only=True,
    true_original_generation_ready_fullPF_bound=True,original_guard_class_MRO_and_Resources_methods_retained=True,
    one_child_noRetry_Root_only_oncepublisher_roletriple_reviewed=True,
    minimum_infinite_only_SCOPE_no_finite_tail_execution=True)
  for p in selected:whole(p)
 except BaseException as exc:failure=repr(exc)
 report=dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_ONLY_REVIEW_V1',
  status='PASS_FROZEN_FOUR_ORIGINAL_ASCII_32T_INFINITE_P0_SOURCE_ONLY' if failure is None else 'FAIL_FROZEN_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_ONLY',
  source_only=True,failure=failure,selected_Source_pins=selected,selected_Source_only_ready_pin=READY,
  genuine_Source_generation_true_tools_pin=GEN,audit_source_pin=pin(Path(__file__)),
  scientific_payload_read=False,gzip_decompressed_by_peer=False,SCI_payload_read_by_peer=False,
  candidate_imported_or_executed_by_peer=False,Source_final_freezes_published_by_peer=False,
  **{k:False for k in FLAGS+PHYSICS},**facts,elapsed_seconds=time.monotonic()-started)
 target=OUT/'REVIEW.json'
 with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),source_only=True,**{k:False for k in FLAGS+PHYSICS})),flush=True)
 require(failure is None,'independent Source review retained actual failure: '+str(failure))

if __name__=='__main__':main()

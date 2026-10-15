"""Independent frozen all34 Source and small-metadata review; no science bodies."""
import ast, hashlib, json, os, re, stat, time
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
TOP=BASE.parent
OUT=Path(__file__).resolve().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FLAGS=('business_executed','numerical_executed','compiler_executed','files_deleted')
PHYSICS=('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','physical_neutron_balance_qualified','unreduced_reference_qualified','finite18_replayed','temperature_interpolation_replayed','current_SPH_MASK_context_applied','AAA_qualified','ABA_admitted','goal_complete')
READY=dict(path=str(BASE/'SOURCE_REVIEW_READY.json'),sha256='36a65580fb92472e52297b970f0028db4219e83f6191d295c94da967d05f01da',size_bytes=275213,identity=[16777229,50401810,33188,1,275213,1791996515912599559,1791996515912599559])
GEN=dict(path=str(BASE/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json'),sha256='c75d439741d6de3c1815d1a4dbabe80c70cc4dee664622284c891a480a2dd8a5',size_bytes=1255,identity=[16777229,50401880,33188,1,1255,1791996533229091187,1791996533229091187])
FUEL={'Am241','Pu238','Pu239','Pu240','Pu241','Pu242','U235','U238'}
MO={'Mo92','Mo94','Mo95','Mo96','Mo97','Mo98','Mo100'}
SCIENCE=set()

def require(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'} and type(p['path']) is str and type(p['sha256']) is str and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']) and type(p['size_bytes']) is int and type(p['identity']) is list and len(p['identity'])==7 and all(type(v) is int for v in p['identity']) and p['identity'][4]==p['size_bytes'],'strict complete fullPF schema')
 q=Path(p['path']);s=q.lstat();compiler=(str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2)
 require(q.is_absolute() and not any(a.is_symlink() for a in(q,*q.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and identity(s)==p['identity'] and s.st_size==p['size_bytes'],'exact ordinary current7 '+str(q))
def whole(p):
 current(p);require(p['path'] not in SCIENCE and p['size_bytes']<8*2**20,'bounded Source/metadata only, no science body')
 with Path(p['path']).open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened Source/metadata7');raw=f.read();require(identity(os.fstat(f.fileno()))==p['identity'],'EOF Source/metadata7')
 require(len(raw)==p['size_bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole Source/metadata SHA '+p['path']);current(p);return raw
def pin(q):
 q=Path(q);s=q.lstat();require(str(q) not in SCIENCE and s.st_size<8*2**20,'only bounded review metadata pin');raw=q.read_bytes();p=dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(p):return json.loads(whole(p))
def false_scope(v):require(all(v[k] is False for k in FLAGS+PHYSICS),'execution and science qualifiers false')
def function_bytes(raw,name):
 text=raw.decode();nodes=[n for n in ast.walk(ast.parse(text)) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name];require(len(nodes)==1,'one complete helper '+name);n=nodes[0];return ''.join(text.splitlines(keepends=True)[n.lineno-1:n.end_lineno]).rstrip('\n').encode()
def inverse(v):
 a=whole(v['original_full_pin']);b=whole(v['candidate_full_pin']);out=bytearray();at=0
 for e in v['edit_map']:
  i,j,k,l=[e[x] for x in('original_begin_byte','original_end_byte','candidate_begin_byte','candidate_end_byte')]
  require(at<=k and a[i:j]==bytes.fromhex(e['original_bytes_hex']) and b[k:l]==bytes.fromhex(e['candidate_bytes_hex']),'actual complete inverse slices');out.extend(b[at:k]);out.extend(a[i:j]);at=l
 out.extend(b[at:]);require(bytes(out)==a and hashlib.sha256(out).hexdigest()==v['whole_original_reconstructed_sha256'] and v['complete_inverse_reconstructed_original'] is True,'complete inverse reconstructs whole original')
def deck(row):
 hp=row['historical_proof'];gp=hp.get('actual_GROUPR_deck_pin',hp.get('original_GROUPR_deck_pin'));dp=hp.get('actual_DRAGR_deck_pin',hp.get('original_DRAGR_deck_pin'));g=[s.strip() for s in whole(gp).decode().splitlines() if s.strip()];d=[s.strip() for s in whole(dp).decode().splitlines() if s.strip()];i=g.index('groupr');card=[int(v) for v in g[i+2].split()];at=i+3
 while g[at].startswith("'"):at+=1
 chunks=[]
 while True:
  chunks.append(g[at]);at+=1
  if '/' in chunks[-1]:break
 temps=[float(x) for x in ' '.join(chunks).split('/')[0].split()];dc=[int(v) for v in d[d.index('dragr')+1].split('/')[0].split()];matches=[s for s in d if s.split()[:2]==[str(card[0]),row['nuclide']]]
 require(len(matches)==1 and matches[0].endswith('/'),'unique complete original material card');material=matches[0].split('/')[0].split();require(len(material)==3,'three original material fields');nbesp=int(material[2]);fuel=row['nuclide'] in FUEL;mo=row['nuclide'] in MO
 require(card[0]==row['mat'] and len(temps)==card[5] and temps==row['original_source_deck_temperatures_K'] and card[6]==row['original_expected_nz'],'original GROUPR MAT/native T/NZ exact')
 require(nbesp==row['original_DRAGR_NBESP']==(4 if fuel else 0) and matches[0]==row['original_DRAGR_material_card_ascii'],'original NBESP4 fuel or NBESP0 others retained')
 require(len(dc)==11 and dc[5]==row['original_nimpo_unit']==(29 if fuel else 0) and dc[6]==row['original_nexpo_unit']==30 and dc[7]==row['original_ipflag']==(1 if mo else 0) and row['original_drahd_existing_ENERGY_REAL32_branch'] is fuel and row['original_thermal_cutoff_eV']==4.0 and '4.000000 /' in d,'exact original producer units/precision/collapse/cutoff')
 require(row['original_expected_nz']==(10 if fuel or row['nuclide'] in {'Cr52','Fe56'} else 1),'actual MF1 expected width1 or10')
 if mo:require(temps==[293.0,550.0,900.0,1200.0,2000.0],'original Mo five temperatures')
 return dict(nuclide=row['nuclide'],SCI_role=row['SCI_role'],actual_deck_temperature_count=len(temps),original_expected_nz=card[6],original_NBESP=nbesp,original_nimpo_unit=dc[5],original_ipflag=dc[7],original_GROUPR_deck_pin=gp,original_DRAGR_deck_pin=dp)

def main():
 started=time.monotonic();failure=None;facts={};selected=[]
 try:
  ready=read(READY);gen=read(GEN);plan=read(ready['control_plan_pin']);SCIENCE.update([plan['actual_current_SCI1_pin']['path'],plan['actual_current_SCI2_pin']['path']]+[r['current_original_input_full_pin']['path'] for r in plan['inputs']])
  require(ready['source_only'] is True and ready['actual_business_started'] is False and ready['Root_final_publication_executed'] is False and ready['scientific_payload_read'] is False,'frozen Source-only ready');false_scope(ready);false_scope(plan)
  selected=ready['selected_Source_pins']+[READY,GEN];require(ready['selected_Source_pins']==ready['dependencies'] and len(ready['dependencies'])==307 and len(selected)==309 and len({p['path'] for p in selected})==309,'all307 selected dependencies plus frozen READY and genuine GEN')
  for p in selected:whole(p)
  ret=gen['actual_Source_preparation_return'];require(gen['observed_closed'] is True and type(gen['original_integer_exit_code']) is int and gen['original_integer_exit_code']==0 and type(ret['exit_code']) is int and ret['exit_code']==0 and ret.get('session_id') is None and type(ret['output']) is str,'genuine original generation typed closed0');receipt=json.loads(ret['output'].strip().splitlines()[-1]);require(receipt['status']=='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_PREPARATION_ONLY' and receipt['ready_pin']==READY,'exact genuine generation stdout READY fullPF');false_scope(receipt)
  prior=read(plan['selected_prior47_plan_pin']);roots=plan['complete_joint_roots'];require(plan['source_only'] is True and plan['original_caps']==ready['original_caps']==prior['original_caps']==CAPS,'exact retained original caps');require(len(roots)==len(set(roots))==49 and roots==prior['complete_joint_roots']+[str(TOP),plan['planned_actual_output_root']] and len(prior['complete_joint_roots'])==47 and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'exact original47 prefix plus TOP/output49')
  require(all(p in ready['dependencies'] for p in plan['explicit_cumulative_metadata_file_pins']) and not Path(plan['planned_actual_output_root']).exists() and all(not (BASE/n).exists() for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')),'complete explicit metadata and no business or premature final publication')
  proof=read(plan['original_whole_math_inverse_proof_pin']);require(proof['source_only'] is True and proof['scientific_payload_read'] is False,'Source-only original math proof');false_scope(proof)
  for c in proof['whole_original_source_copies']:require(whole(c['original_full_pin'])==whole(c['whole_unchanged_copy_full_pin']),'six original whole Source copies unchanged')
  scalar=whole(plan['original_scalar_helper_source_copy_pin']);dragr=whole(proof['actual_original_producer_dragr_Source_full_pin']);require(hashlib.sha256(dragr).hexdigest()=='047ed05e54c54aad2681ce1796bec72f47a0118a2d80295d0d9929e4e42381ac' and len(dragr)==123030,'whole original actual producer dragr')
  for row in proof['original_scalar_functions_called_unchanged']:
   raw=function_bytes(scalar,row['name']);require(raw==bytes.fromhex(row['original_complete_definition_bytes_hex']) and hashlib.sha256(raw).hexdigest()==row['original_complete_definition_sha256'] and row['called_unchanged'] is True,'unchanged scalar parser/matrix/packing helper')
  for row in proof['whole_original_math_source_blocks']:
   raw=dragr[row['begin_byte']:row['end_byte']];require(raw==bytes.fromhex(row['original_statement_bytes_hex']) and hashlib.sha256(raw).hexdigest()==row['sha256'],'whole original drasc/fmatr/energy/limits Source block')
  for k in('host_complete_byte_inverse','publisher_complete_byte_inverse','worker_complete_byte_inverse'):inverse(proof[k])
  for p in proof['Mo_original_producer_Source_and_historic_log_pins']:whole(p)
  require(proof['original_SCI_raw_max_words']==262144 and proof['BoundedSCI_new_leaf_extension_literal_names']==['SCAT00','NJJS00','IJJS00'] and proof['no_original_finite_tail_branch_called'] is True,'original typed raw bound and infinite-only roles')
  sources={Path(p['path']).name:whole(p) for p in ready['complete_source_file_pins'] if p['path'].endswith('.py')}
  for raw in sources.values():ast.parse(raw)
  worker=sources['compare_all34_original_ascii_infinite_SCAT.py'].decode();host=sources['run_guarded_all34_original_ascii_infinite_SCAT.py'].decode();pub=sources['write_once_Root_all34_original_ascii_infinite_SCAT_SF_HF_CLI.py'].decode();prep=sources['prepare_all34_original_ascii_infinite_SCAT_Source.py'].decode()
  snippets=("MTS=(2,5,16,17,28,37,*range(51,92))","cutoff_energy=energy['values']if row['original_drahd_existing_ENERGY_REAL32_branch']else grid['ascending_energy_eV'][::-1]","cutoff_energy[1:370]","first_thermal=next((mt for mt in sections if 221<=mt<=250),None)","if ig==370:break","ngther=min(ngther,igrest)","reverse=True","total[first:,:]+=value[first:,:]","total[first:,:]-=value[first:,:]","for mt in MTS:","total+=value","for incident in range(370):","dgar=0.0","for outgoing in range(370):dgar=dgar+float(total[incident,outgoing])","total[incident,:]=0.0;total[incident,incident]=dgar","scalar.packed(total,False,(0,0),total)","payload[::active['nl']*active['nz']]","matrix(section);return value[0,0],flux[0,0]","grid_nz==row['original_expected_nz']and 1<=grid_nz<=30","npl==1+grid_nz+ng+1+ngg+1","nz in(1,grid_nz)","nt=len(row['original_source_deck_temperatures_K'])","whole original ASCII EOF SHA/size","whole compressed primary EOF SHA/size","for role in('SCI1','SCI2'):","require(exact,'actual original infinite P0 packed mismatch retained; no retry')")
  for s in snippets:require(s in worker,'concrete original arithmetic/parser Source statement '+s)
  require('math.fsum(' not in worker and '.sum(' not in worker and 'subprocess' not in worker and 'thermals == [221]' not in worker,'no substituted reduction, engine launch, or universal thermal221 assumption')
  mts=dragr.decode().split('integer,save,dimension(maxmat) :: mtlist=',1)[1].split('(/',1)[1].split('/)',1)[0];require(tuple(int(x) for x in re.findall(r'\d+',mts))==(2,5,16,17,28,37,*range(51,92)),'exact original47 MT order')
  bounded=whole(plan['original_bounded_SCI_helpers_copy_pin']).decode();require('0<=n<=262144' in bounded,'original bounded SCI raw method unchanged')
  original_host=whole(proof['host_complete_byte_inverse']['original_full_pin']).decode();start=' class Resources:';end=' resources=Resources();';require(host[host.index(start):host.index(end)]==original_host[original_host.index(start):original_host.index(end)],'whole original Resources methods unchanged')
  for s in("full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","len(roots)==49","for p in fixed:current7(p);c.same_pin(p['path'],p)","SCI1_and_SCI2_whole_PF_verified_by_original_parent_before_child=True","runner.execute(stage,'all34_original_ASCII_234T_infinite_P0_SCAT',cmd,600)","len(runner.records)==1"):
   require(s in host,'original guard class, full SCI preverification, onechild600 Source '+s)
  for s in("selected=ready['selected_Source_pins']+[pready,pg]","all(contains(peer,p)for p in selected)","peer['source_only']is True","peer['status'].startswith('PASS')","peer['failure']is None","type(t['exit_code'])is int and t['exit_code']==0","gd['ready_pin']==pready","not any(os.path.lexists(q)for q in targets)","Path(p).open('x')","len(prefix)==11","'--source-freeze-summary'","'--host-freeze-summary'"):
   require(s in pub,'Root-only once Source publisher reviewed concrete guard '+s)
  require('subprocess' not in pub and 'material_cards=' in prep and 'original_DRAGR_NBESP=nbesp' in prep and 'scientific payload not read' in prep,'corrected material-card semantics and Source-only preparation/publication')
  require(len(ready['original_complete_ENV_Python_B_prefix'])==11 and ready['original_complete_ENV_Python_B_prefix'][-1]=='-B','retained exact ENV/Python/-B prefix')
  author_pin=pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=read(author_pin);derive_pin=author['source_derivation_pin'];derive=read(derive_pin)
  for p in author['whole_Source_file_pins']+author['preserved_original_source_and_author_freeze_pins']+derive['failed_original_source_pins']:whole(p)
  inverse(derive['prepare_complete_byte_inverse']);failed=read(derive['retained_genuine_first_source_preparation_failure_pin']);require(type(failed['exit_code']) is int and failed['exit_code']==1 and failed.get('session_id') is None and 'same original MAT/name/cutoff deck' in failed['output'] and derive['three_worker_host_oncewriter_sources_whole_unchanged'] is True,'original failed Source/freeze/true failure preserved; correction only before business')
  summary=read(plan['prior_four_actual_summary_pin']);post=read(plan['prior_four_actual_post_pin']);posttools=read(plan['prior_four_actual_post_tools_pin']);oldactual=read(post['Root_actual_runtime_true_tools_pin']);require(post['status'].startswith('PASS') and post['failure'] is None and post['actual_Root_report_pin']==plan['prior_four_actual_summary_pin'] and post['actual_original_compared_words']==1926639 and post['actual_bit_word_mismatches']==0 and summary['failure'] is None,'actual first4 independent post and1926639 zero mismatch words')
  require(posttools['observed_closed'] is True and type(posttools['actual_review_return']['exit_code']) is int and posttools['actual_review_return']['exit_code']==0 and json.loads(posttools['actual_review_return']['output'])['review_pin']==plan['prior_four_actual_post_pin'] and oldactual['observed_closed'] is True and type(oldactual['actual_terminal_return']['exit_code']) is int and oldactual['actual_terminal_return']['exit_code']==0 and json.loads(oldactual['actual_terminal_return']['output'])['report_pin']==plan['prior_four_actual_summary_pin'],'genuine first4 Root and independent post typed0 tool bindings')
  findings=read(plan['actual_original_SCI1_nuclide_route_context_pin']);routes=findings['complete_actual_source_library_isotope_NX_inventory'];sci1=plan['actual_current_SCI1_pin'];sci2=plan['actual_current_SCI2_pin'];current(sci1);current(sci2);require(sci1['sha256']=='e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc' and sci1['size_bytes']==210627112 and sci2['sha256']=='66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9' and sci2['size_bytes']==769113024,'both exact retained SCI roles, current7 only')
  sci1refs={q['reference'] for r in routes if r['library_pin']['sha256']==sci1['sha256'] for q in r['actual_refs']};sci2refs={q['reference'] for r in routes if r['library_pin']['sha256']==sci2['sha256'] for q in r['actual_refs']};rows=plan['inputs'];require(len(rows)==34 and len({r['nuclide'] for r in rows})==34 and {r['nuclide'] for r in rows if r['SCI_role']=='SCI1'}==sci1refs and len(sci1refs)==27 and 'C12' not in sci1refs and {r['nuclide'] for r in rows if r['SCI_role']=='SCI2'}==sci2refs==MO,'exact actual27 SCI1 excluding C12 and seven SCI2 routes')
  cohorts=[deck(row) for row in rows];require(sum(r['actual_deck_temperature_count'] for r in cohorts)==234 and sum(r['actual_deck_temperature_count'] for r in cohorts if r['SCI_role']=='SCI1')==199 and sum(r['original_nimpo_unit']==29 for r in cohorts)==8 and sum(r['original_nimpo_unit']==0 and r['SCI_role']=='SCI1' for r in cohorts)==19 and plan['expected_nuclides']==34 and plan['expected_temperature_records']==234 and plan['expected_leaf_records']==702 and plan['original_decompressed_payload_expected_bytes']==sum(r['original_ASCII_expected_size_bytes'] for r in rows)==746505396,'exact original all34 nativeT/precision routes and bytes')
  preparation=read(plan['SCI1_original_preparation_pin']);source_rows={r['nuclide']:r for r in preparation['sources']};mo=read(plan['Root_current_Mo_input_full_PF_capture_pin']);mot=read(plan['Root_current_Mo_input_full_PF_capture_tools_pin']);require(type(mot['exit_code']) is int and mot['exit_code']==0 and mot.get('session_id') is None and json.loads(mot['output'])['input_capture_pin']==plan['Root_current_Mo_input_full_PF_capture_pin'] and mo['SCI2_payload_read'] is False and mo['original_SCI2_retained_pin_current7_only']==sci2,'genuine Root current Mo fullEOF capture, no invented historical receipt')
  archive=direct=0
  for row in rows:
   p=row['current_original_input_full_pin'];current(p);hp=row['historical_proof'];require(row['original_ASCII_expected_sha256']==p['sha256'] or row['input_encoding']=='gzip','direct original input expected full SHA')
   if row['SCI_role']=='SCI2':
    hits=[r for r in mo['actual_original_ASCII_current_full_pins'] if r['nuclide']==row['nuclide']];require(len(hits)==1 and hits[0]['current_original_ASCII_full_pin']==p and hits[0]['whole_original_ASCII_EOF_hash_measured_now'] is True and hp['historical_original_ASCII_PF_not_invented'] is True,'current Mo capture exact source role');continue
   gr=read(hp['actual_GROUPR_receipt_pin']);dr=read(hp['actual_DRAGR_receipt_pin']);require(type(gr['returncode']) is int and gr['returncode']==0 and gr['output_sha256']==row['original_ASCII_expected_sha256'] and type(dr['returncode']) is int and dr['returncode']==0 and dr['output_sha256']==source_rows[row['nuclide']]['sha256'],'historic GROUPR/DRAGR output/source binding')
   if row['input_encoding']=='gzip':
    archive+=1;manifest=read(hp['round9_manifest_pin']);backups=read(hp['round9_backups_pin']);c=manifest['candidates'][hp['round9_candidate_index']];hits=[r for r in backups['records'] if r['original']['path']==c['path']];require(len(hits)==1,'one exact historic archived input');h=hits[0];b=c['compressed_backup'];require(c['sha256']==h['original']['sha256']==row['original_ASCII_expected_sha256'] and c['size']==h['original']['size']==row['original_ASCII_expected_size_bytes'] and h['verified_decompressed']==dict(size=c['size'],sha256=c['sha256']) and b['path']==h['backup']['path']==p['path'] and b['sha256']==h['backup']['sha256']==p['sha256'] and b['size']==h['backup']['size']==p['size_bytes'] and not os.path.lexists(c['path']),'complete round9 historic verified decode/current compressed PF binding')
    hashes=read(hp['actual_DRAGR_input_hashes_pin']);dp=Path(hp['actual_DRAGR_deck_pin']['path']);require(hashes[str(dp.parent/'tape24')]==c['sha256'],'actual archived original ASCII was DRAGR input')
   else:
    direct+=1;staged=read(hp['actual_staged_inputs_pin']);dp=Path(hp['actual_DRAGR_deck_pin']['path']);gp=hp['actual_GROUPR_deck_pin'];require(staged[str(dp)]==hp['actual_DRAGR_deck_pin']['sha256'] and staged[gp['path']]==gp['sha256'] and staged[str(dp.parent/'tape24')]==gr['output_sha256'],'direct Fe56/light original deck and ASCII staged receipts')
   if row.get('actual_complete_inventory_pin'):
    inv=read(row['actual_complete_inventory_pin']);require(inv['original_ASCII_fullEOF_validated'] is True and inv['current_gzip_primary_full_pin']==p and inv['actual_decompressed_SHA256']==row['original_ASCII_expected_sha256'] and len(inv['original8_MF1_grids'])==8,'first4 exact prior fullEOF inventories retained')
  require(archive==23 and direct==4,'archived23/direct4 exact SCI1 input roles')
  retirement=read(plan['actual_precise_retirement_receipt_pin']);require(retirement['mode']=='execute' and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and retirement['failure'] is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4 and all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']),'only exact original four retired spool roles absent')
  require(plan['all_known_output_document_count']==12 and len(plan['all_known_output_document_pins'])==12 and all(p in plan['explicit_cumulative_metadata_file_pins'] for p in plan['all_known_output_document_pins']),'all known six old metadata plus six output documents explicitly counted')
  total=0
  for root in roots:
   q=Path(root)
   if not q.exists():continue
   for p in q.rglob('*'):
    s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no joint namespace alias')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
  outer=sum(p['size_bytes'] for p in plan['explicit_cumulative_metadata_file_pins'] if not any(Path(p['path']).is_relative_to(Path(r)) for r in roots));require(total+outer<2*2**30,'all49 roots plus external explicit metadata below original2GiB')
  facts=dict(actual_original_deck_cohorts=cohorts,whole_source_and_metadata_fullpin_count=309,selected_dependency_count=307,science_file_current7_only_pins=[sci1,sci2]+[r['current_original_input_full_pin'] for r in rows],complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],observed_cumulative_root_bytes=total,observed_explicit_outer_metadata_bytes=outer,observed_total_cumulative_bytes=total+outer,original_caps=CAPS,original_failed_source_and_freeze_preservation_checked=True,corrected_v2_author_freeze_pin=author_pin,corrected_v2_source_derivation_pin=derive_pin,actual_native_temperature_records=234,actual_SCI1_temperature_records=199,actual_SCI2_temperature_records=35,actual_expected_original_ASCII_bytes=746505396,original_MF1_NZ1_or10_and_NPL373plusNZ_from_decks=True,original_energy_route_nimpo0_binary64_nimpo29_REAL32=True,original_ipflag1_outgoing1to370_sequential_sum_then_zero_and_diagonal=True,original47_MT_order_and_P0z0_projection_retained=True,original_first_thermal370_sentinel_scan_distinct_from_fmatr=True,thermal_MTs_selected_from_actual_sections_without_universal221_assumption=True,unchanged_original_scalar_matrix_and_infinite_packed_functions=True,original_raw_typed_SCI_bound262144_retained=True,archived23_historical_receipt_lossless_metadata_verified=True,direct4_actual_receipt_and_staged_lineage_verified=True,Mo_current_fullEOF_capture_historical_PF_not_invented=True,prior_first4_32T96leaves1926639words_zero_mismatch_context_verified=True,original_guard_MRO_Resources_caps_and_onechild600_noRetry_retained=True,Root_only_once_publisher_requires_all_selected_READY_and_GEN_fullpins=True,true_original_generation_stdout_READY_fullPF_verified=True)
  for p in selected:whole(p)
  whole(author_pin);whole(derive_pin)
 except BaseException as exc:failure=repr(exc)
 report=dict(schema='INDEPENDENT_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_ONLY_REVIEW_V1',status='PASS_FROZEN_ALL34_ORIGINAL_ASCII_234T_INFINITE_P0_SOURCE_ONLY' if failure is None else 'FAIL_FROZEN_ALL34_ORIGINAL_ASCII_INFINITE_P0_SOURCE_ONLY',source_only=True,failure=failure,selected_Source_pins=selected,selected_Source_only_ready_pin=READY,genuine_Source_generation_true_tools_pin=GEN,audit_source_pin=pin(Path(__file__)),scientific_payload_read=False,gzip_decompressed_by_peer=False,SCI_payload_read_by_peer=False,candidate_imported_or_executed_by_peer=False,Source_final_freezes_published_by_peer=False,historical_machine_bit_replay=False,original_XSM_memory_bits_verified=False,full_reference_qualified=False,**{k:False for k in FLAGS+PHYSICS},**facts,elapsed_seconds=time.monotonic()-started)
 target=OUT/'REVIEW.json'
 with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),source_only=True,**{k:False for k in FLAGS+PHYSICS})),flush=True)
 require(failure is None,'independent Source review retained actual failure: '+str(failure))

if __name__=='__main__':main()

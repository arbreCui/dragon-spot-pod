"""Independent frozen Source and bounded-metadata audit. No candidate imports."""
import ast
import hashlib
import json
import os
import resource
import stat
import sys
import time
from pathlib import Path

BASE = Path(__file__).absolute().parents[1]
TOP = BASE.parent
R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
PRIOR = REC/'current_all34_original_ASCII_infinite_SCAT_producer_source_v1_20261015/v2'
OUT = R/'validation/artifacts/axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v1'
HERE = Path(__file__).absolute().parent
REVIEW = HERE/'REVIEW.json'
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512, fresh_bytes=2147483648,
            history_bytes=103079215104, cold_reserve_bytes=20971764748,
            metadata_reserve_bytes=67108864, free_floor_bytes=8589934592,
            threads=1, children_at_once=1, retries=0)
LARGE = (
 R/'validation/artifacts/axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',
 R/'validation/artifacts/axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')
FALSE = dict(business_executed=False, numerical_executed=False, compiler_executed=False,
 files_deleted=False, physics_qualified=False, scientific_accuracy_qualified=False,
 complete_reaction_authority_qualified=False, physical_neutron_balance_qualified=False,
 unreduced_reference_qualified=False, full_reference_qualified=False,
 finite18_replayed=False, temperature_interpolation_replayed=False,
 current_SPH_MASK_context_applied=False, AAA_qualified=False, ABA_admitted=False,
 goal_complete=False, historical_machine_bit_replay=False,
 original_XSM_memory_bits_verified=False)
START = time.monotonic()
CHECKS = []
HASHED = {}
SCI_STAT = []

def require(ok, message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)

def ident(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def complete(p):
    require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'}, 'complete PF keys')
    require(type(p['path']) is str and Path(p['path']).is_absolute(), 'literal absolute PF')
    require(type(p['sha256']) is str and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']), 'SHA256 PF')
    require(type(p['size_bytes']) is int and p['size_bytes']>=0 and type(p['identity']) is list and len(p['identity'])==7 and all(type(v) is int for v in p['identity']) and p['identity'][4]==p['size_bytes'], 'typed size/seven identity PF')

def current(p):
    complete(p)
    q = Path(p['path'])
    s = q.lstat()
    compiler = (q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15') and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and s.st_nlink==2 and p['identity'][3]==2)
    require(not any(v.is_symlink() for v in (q,*q.parents)) and stat.S_ISREG(s.st_mode) and (s.st_nlink==1 or compiler) and ident(s)==p['identity'], 'exact ordinary current7: '+str(q))

def allowed(q, size):
    permitted = q.suffix in ('.py','.f90','.json','.jsonl','.txt','.make','.in','.sha256','.log') or q.name.startswith(('file_data_gendf_','file_data_dendf_'))
    require(permitted and not q.name.startswith('tape') and q.name not in ('SCI1','SCI2'), 'Source/bounded metadata read role: '+str(q))
    require(size < (64*2**20 if q in LARGE else 8*2**20), 'exact-role metadata bound: '+str(q))

def pin(q):
    q = Path(q)
    s = q.lstat()
    p = dict(path=str(q),sha256='0'*64,size_bytes=s.st_size,identity=ident(s))
    current(p)
    allowed(q,s.st_size)
    with q.open('rb') as stream:
        require(ident(os.fstat(stream.fileno()))==p['identity'], 'opened Source/metadata7')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require(ident(os.fstat(stream.fileno()))==p['identity'], 'EOF Source/metadata7')
    p['sha256']=digest
    current(p)
    HASHED[str(q)]=p
    return p

def verify(p):
    current(p)
    require(pin(p['path'])==p, 'whole Source/metadata SHA/size/current7: '+p['path'])

def read(p):
    verify(p)
    value=json.loads(Path(p['path']).read_bytes())
    current(p)
    return value

def get(q):
    p=pin(q)
    return read(p),p

def text_source(p):
    verify(p)
    require(Path(p['path']).suffix in ('.py','.f90','.in'), 'Source text role')
    return Path(p['path']).read_text()

def false_flags(v, names=FALSE):
    require(all(v[k] is False for k in names if k in v), 'false qualification/execution flags')

def contains(v,p):
    return v==p or type(v) is dict and any(contains(x,p) for x in v.values()) or type(v) is list and any(contains(x,p) for x in v)

def check(name):
    CHECKS.append(name)

def tools_closed(v, role, expected_pin, expected_key):
    t=v[role]
    require(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code']==0 and type(t['exit_code']) is int and t['exit_code']==0 and t.get('session_id') is None and type(t['output']) is str, 'genuine original closed0 '+role)
    d=json.loads(t['output'].strip().splitlines()[-1])
    require(d[expected_key]==expected_pin, 'typed original stdout exact fullPF '+role)
    return d

def exact_source_history(author):
    for k,v in author.items():
        if k.startswith('preserved_original_'):
            for p in v: verify(p)
        elif k.startswith('root_precise_'):
            verify(v)
    v1=(TOP/'prepare_eight_fuel_finite18_SCAT_Source.py').read_text()
    v2=(TOP/'v2/prepare_eight_fuel_finite18_SCAT_Source.py').read_text()
    old=" p=pin(p);require(p['size_bytes']<8*2**20,'bounded metadata');v=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same metadata');return v,p"
    new=" p=pin(p);large_roles=(ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json');limit=64*2**20 if Path(p['path'])in large_roles else 8*2**20;require(p['size_bytes']<limit,'bounded metadata exact upstream report role');v=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same metadata');return v,p"
    roots_old="roots=prior['complete_joint_roots']+[str(BASE),str(OUT)]"
    roots_new="roots=prior['complete_joint_roots']+[str(TOP),str(OUT)]"
    require(v1.count(old)==1 and v1.count(roots_old)==1 and v1.replace(old,new,1).replace(roots_old,roots_new,1)==v2, 'v2 exactly two metadata/root Source changes')
    for n in ('compare_eight_fuel_finite18_SCAT.py','run_guarded_eight_fuel_finite18_SCAT.py','write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py'):
        require((TOP/n).read_bytes()==(TOP/'v2'/n).read_bytes(), 'v1-v2 whole runtime Source equality')
    w2=(TOP/'v2/compare_eight_fuel_finite18_SCAT.py').read_bytes()
    w3=(TOP/'v3/compare_eight_fuel_finite18_SCAT.py').read_bytes()
    a=b'actual_inventory_section_indexes_one_based=section_indexes,'
    b=b'actual_inventory_section_indexes_one_based=list(section_indexes),'
    require(w2.count(a)==1 and w2.replace(a,b,1)==w3, 'v3 exactly returned metadata list copy')
    for n in ('prepare_eight_fuel_finite18_SCAT_Source.py','run_guarded_eight_fuel_finite18_SCAT.py','write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py'):
        require((TOP/'v2'/n).read_bytes()==(TOP/'v3'/n).read_bytes(), 'v2-v3 other three Source whole equality')
    p3=(TOP/'v3/prepare_eight_fuel_finite18_SCAT_Source.py').read_bytes()
    p4=(BASE/'prepare_eight_fuel_finite18_SCAT_Source.py').read_bytes()
    for n in (b'REVIEW.json',b'TRUE_TOOL_RETURNS.json'):
        old=b'actual_postverify_20261015/'+n
        new=b'actual_postverify_20261015/corrected_metadata_assessment_v2/'+n
        require(p3.count(old)==1, 'one exact old post metadata path')
        p3=p3.replace(old,new,1)
    require(p3==p4, 'v4 exactly two final post metadata paths')
    for n in ('compare_eight_fuel_finite18_SCAT.py','run_guarded_eight_fuel_finite18_SCAT.py','write_once_Root_eight_fuel_finite18_SCAT_SF_HF_CLI.py'):
        require((TOP/'v3'/n).read_bytes()==(BASE/n).read_bytes(), 'v3-v4 other three Source whole equality')
    check('All frozen v1-v4 Source fullPFs preserved; exact role-bound, ledger-root, metadata-list-copy, and final-post-path changes only')

def deck(row):
    proof=row['historical_proof']
    g=text_source(proof['actual_GROUPR_deck_pin'])
    d=text_source(proof['actual_DRAGR_deck_pin'])
    gl=[s.strip() for s in g.splitlines() if s.strip()]
    i=gl.index('groupr');card=[int(v) for v in gl[i+2].split()]
    require(card[0]==row['mat'] and card[5:7]==[8,10], 'original GROUPR material/NZ10/8T deck')
    i+=3
    while gl[i].startswith("'"): i+=1
    grids=[]
    for _ in range(2):
        vals=[]
        while True:
            part=gl[i];vals.extend(float(v) for v in part.split('/')[0].split());i+=1
            if '/' in part:break
        grids.append(vals)
    temperatures,sigma=grids
    require(temperatures==row['original_source_deck_temperatures_K'] and len(temperatures)==8 and len(sigma)==10 and sigma[0]==1e10 and all(x>y for x,y in zip(sigma,sigma[1:])), 'native lane temperatures/dilution Source cards')
    mf6_cards=[s.split('/')[0].split() for s in gl if s.startswith('6 ')]
    thermal_cards=[c for c in mf6_cards if len(c)==2 and 221<=int(c[1])<=250]
    require(len(thermal_cards)==8 and all(c==['6','221'] for c in thermal_cards), 'original only free-gas thermal MF6 deck')
    dl=[s.strip() for s in d.splitlines() if s.strip()]
    i=dl.index('dragr');dc=[int(v) for v in dl[i+1].split('/')[0].split()]
    require(len(dc)==11 and dc[5]==(0 if row['lane']=='low' else 29) and dc[6:8]==[30,0], 'original nimpo/nexpo/ipflag deck')
    material=row['original_DRAGR_material_card_ascii']
    require(material in dl and material.split('/')[0].split()==[str(row['mat']),row['nuclide'],'4'], 'original MAT/name/NBESP4 deck')
    i=dl.index(material)+1;require(dl[i].startswith("'"), 'original material label');i+=1
    fission=[]
    while True:
        part=dl[i];fission.extend(float(v) for v in part.split('/')[0].split());i+=1
        if '/' in part:break
    bounds=[float(v) for v in dl[i].split('/')[0].split()]
    require(len(fission)==5 and bounds==row['original_selfshielding_energy_bounds_eV'] and float(dl[i+1].split('/')[0])==row['original_thermal_cutoff_eV']==4.0, 'fission card skipped exactly; selfshielding/thermal source bounds')
    return dict(nuclide=row['nuclide'],lane=row['lane'],mat=row['mat'],temperatures_K=temperatures,finite_sigma0_source_cards=sigma[1:],original_thermal_MF6_MT=221,NBESP=4,ipflag=0,nimpo=dc[5],nexpo=30,cutoff_eV=4.0,selfshielding_bounds_eV=bounds)

def audit():
    ready,pr=get(BASE/'SOURCE_REVIEW_READY.json')
    require(pr['sha256']=='3cffd1e76e0b36cb7c7cd3adc342ee1c95780ec50d3eed14e66c8f102a97c529' and pr['size_bytes']==347181, 'selected Root v4 READY fullPF')
    require(ready['schema']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_REVIEW_READY_V1' and ready['source_only'] is True and ready['actual_business_started'] is False and ready['Root_final_publication_executed'] is False and ready['scientific_payload_read'] is False, 'actual frozen READY Source-only roles')
    false_flags(ready)
    require(ready['original_caps']==CAPS and len(ready['selected_Source_pins'])==388 and ready['selected_Source_pins']==ready['dependencies'], 'selected388 exact complete Source scope')
    for p in ready['selected_Source_pins']: verify(p)
    generation,pg=get(BASE/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
    require(pg['sha256']=='4e1f5bc6f62d86d4cf990eaf94cc3c7c0e2940dc9624139933001b9078c5beaf' and pg['size_bytes']==1234, 'selected real Root generation fullPF')
    gd=tools_closed(generation,'actual_Source_preparation_return',pr,'ready_pin')
    require(gd['status']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_PREPARATION_ONLY', 'genuine Source-only generation status')
    false_flags(gd)
    check('All selected388 bounded Source/metadata fullPFs and real Root generation/READY exact fullPF checked')
    plan=read(ready['control_plan_pin']);require(plan['schema']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_ONLY_PLAN_V1' and plan['original_caps']==CAPS, 'selected Source-only plan caps')
    false_flags(plan)
    prior=read(plan['selected_prior49_plan_pin'])
    roots=plan['complete_joint_roots']
    require(len(prior['complete_joint_roots'])==49 and roots==prior['complete_joint_roots']+[str(TOP),str(OUT)] and len(roots)==len(set(roots))==51 and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b), 'all prior49 exact prefix plus entire TOP and OUT roots')
    require(plan['planned_actual_output_root']==str(OUT) and not os.path.lexists(OUT) and not any(os.path.lexists(BASE/n) for n in ('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')), 'unexecuted fresh finite target and no premature publication')
    author=read(plan['author_Pre_Root_generation_Source_freeze_pin'])
    require(plan['author_Pre_Root_generation_Source_freeze_pin']['sha256']=='46c7161286241acbbcb30d64dfe5983143c71d7fdf244d1392ebac0bf1646c53' and plan['author_Pre_Root_generation_Source_freeze_pin']['size_bytes']==13677 and author['Source_files_frozen_before_Root_generation'] is True and author['Source_preparation_executed_by_author'] is False and author['Source_publication_executed_by_author'] is False, 'final Root v4 pre-generation Source freeze')
    for p in author['whole_Source_file_pins']: verify(p)
    false_flags(author)
    exact_source_history(author)
    proof=read(plan['original_whole_math_inverse_proof_pin'])
    require(proof['schema']=='EIGHT_FUEL_FINITE18_ORIGINAL_SCAT_MATH_WHOLE_SOURCE_AND_MINIMAL_INVERSE_V1' and len(proof['whole_original_source_copies'])==6, 'six original whole Source copies')
    false_flags(proof)
    for row in proof['whole_original_source_copies']:
        a=row['original_full_pin'];b=row['whole_unchanged_copy_full_pin'];verify(a);verify(b)
        require(Path(a['path']).read_bytes()==Path(b['path']).read_bytes(), 'whole original unchanged Source copy')
    actual=proof['actual_original_producer_dragr_Source_full_pin'];verify(actual)
    dragr=(BASE/'original_dragr.f90').read_bytes()
    require(dragr==Path(actual['path']).read_bytes() and actual['sha256']=='047ed05e54c54aad2681ce1796bec72f47a0118a2d80295d0d9929e4e42381ac', 'whole actual original dragr Source')
    for k in ('host_complete_byte_inverse','worker_complete_byte_inverse','publisher_complete_byte_inverse'):
        inv=proof[k];verify(inv['original_full_pin']);verify(inv['candidate_full_pin'])
        a=Path(inv['original_full_pin']['path']).read_bytes();b=Path(inv['candidate_full_pin']['path']).read_bytes()
        for e in sorted(inv['edit_map'],key=lambda v:v['candidate_begin_byte'],reverse=True):
            ob=bytes.fromhex(e['original_bytes_hex']);cb=bytes.fromhex(e['candidate_bytes_hex'])
            require(a[e['original_begin_byte']:e['original_end_byte']]==ob and b[e['candidate_begin_byte']:e['candidate_end_byte']]==cb, 'complete inverse exact retained edit intervals')
            b=b[:e['candidate_begin_byte']]+ob+b[e['candidate_end_byte']:]
        require(b==a and hashlib.sha256(b).hexdigest()==inv['whole_original_reconstructed_sha256'] and inv['complete_inverse_reconstructed_original'] is True, 'whole original byte inverse')
    for e in proof['whole_original_math_source_blocks']+[proof['whole_original_dramat_source_block']]:
        raw=dragr[e['begin_byte']:e['end_byte']]
        require(raw==bytes.fromhex(e['original_statement_bytes_hex']) and hashlib.sha256(raw).hexdigest()==e['sha256'], 'whole original Fortran math block exact bytes')
    scalar=text_source(plan['original_scalar_helper_source_copy_pin'])
    tree=ast.parse(scalar)
    defs={n.name:ast.get_source_segment(scalar,n).encode() for n in tree.body if isinstance(n,ast.FunctionDef)}
    for f in proof['original_scalar_functions_called_unchanged']:
        raw=defs[f['name']]
        require(raw==bytes.fromhex(f['original_complete_definition_bytes_hex']) and hashlib.sha256(raw).hexdigest()==f['original_complete_definition_sha256'] and f['called_unchanged'] is True, 'whole original scalar function exact Source')
    require(hashlib.sha256(defs['matrix']).hexdigest()=='ce657825b91ea0a9d87d3c2b0753bd9f000b8c0efdae1eed6839f0b626fa6a6b' and hashlib.sha256(defs['packed']).hexdigest()=='1406c189739199fb60bc0db71af061a6f2721604487d8cd2896ed8aeb86edb63', 'independently inspected original fmatr/packed functions')
    for token in ('support_factor = float(np.float32(1e-6))','tail_factor = float(np.float32(1e-8))',"stored = np.asarray(stored,dtype='f4')",'limit = tail_factor*float(np.abs(stored).max())',"np.abs(stored).astype('f8') >= limit"):
        require(scalar.count(token)==1, 'original support/REAL32-garmax/suffix-tail precision')
    require(scalar.index("stored = np.asarray(stored,dtype='f4')")<scalar.index('limit = tail_factor*float(np.abs(stored).max())'), 'REAL32 cast before original garmax')
    worker=(BASE/'compare_eight_fuel_finite18_SCAT.py').read_bytes()
    for e in proof['minimal_finite_P0_allNZ_adapter_source_statements']:
        raw=worker[e['begin_byte']:e['end_byte']]
        require(raw==bytes.fromhex(e['bytes_hex']) and hashlib.sha256(raw).hexdigest()==e['sha256'] and worker.count(raw)==1, 'exact finite P0 allNZ adapter Source statement')
    w=worker.decode()
    for token in ("MTS=(2,5,16,17,28,37,*range(51,92))", "payload[::active['nl']]",'value,flux=scalar.matrix(section);return value[:,0],flux[:,0]',"ratio=flux[z].copy();nonzero=flux[0]!=0;ratio[nonzero]/=flux[0,nonzero];value=total[z]*ratio[:,None]-total[0]",'njjs,ijjs,scat=scalar.packed(value,True,(igres0,igres1),total[0])',"thermals=sorted((mt for mt in sections if 221<=mt<=250),reverse=True)","cutoff_energy=energy['values']if row['original_drahd_existing_ENERGY_REAL32_branch']else grid['ascending_energy_eV'][::-1]",'for ig in range(371,1,-1):',"dhits=[i for i,v in enumerate(dilutions)if struct.pack('<f',v)==dword]",'actual_inventory_section_indexes_one_based=list(section_indexes)'):
        require(w.count(token)==1, 'independent finite mathematical/routing Source inspection: '+token)
    require(b'iglast(il)=igres1+1' in dragr and proof['original_finite_support_and_suffix_tail_called_unchanged'] is True and proof['no_original_finite_tail_branch_called'] is False and proof['low_lane_own_infinite_and_elasticflux_reference_preserved'] is True and proof['original_REAL32_DILUTION_word_selects_original_SUBMAT'] is True, 'finite original support/tail/selfshielding and own-lane routes')
    for p in ready['complete_source_file_pins']:
        if Path(p['path']).suffix=='.py':ast.parse(text_source(p),filename=p['path'])
    check('Whole original Source copies, complete byte inverses, original drasc/fmatr/math blocks, and unchanged exact scalar matrix/packing precision verified without import or numerical replay')
    manifest,pm=get(R/'validation/storage_cleanup_ninth_20261009/manifest.json')
    backups,pb=get(R/'validation/storage_cleanup_ninth_20261009/packed_material_intermediate_backups.json')
    require(pm['sha256']=='e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8' and pb['sha256']=='d5834da3209265f9d0f4ad571f4da0c8a570558cfe39b7120750f5dad156aec9' and backups['status']=='PASS', 'exact round9 whole backup metadata')
    indices=dict(Am241=(203,201),Pu238=(210,208),Pu239=(217,215),Pu240=(224,222),Pu241=(178,176),Pu242=(185,183),U235=(192,190),U238=(199,197))
    inputs=plan['inputs'];require(len(inputs)==16 and {(v['nuclide'],v['lane']) for v in inputs}=={(n,l) for n in indices for l in ('low','high')}, 'exact eight original low/high routes')
    routes=[]
    for row in inputs:
        require(row['SCI_role']=='SCI1' and row['input_encoding']=='gzip' and row['original_expected_nz']==10 and row['original_DRAGR_NBESP']==4 and row['original_ipflag']==0 and row['original_nexpo_unit']==30 and row['original_nimpo_unit']==(0 if row['lane']=='low' else 29) and row['original_drahd_existing_ENERGY_REAL32_branch'] is (row['lane']=='high'), 'plan exact original scientific route flags')
        p=row['current_original_input_full_pin'];current(p);SCI_STAT.append(p)
        i=indices[row['nuclide']][0 if row['lane']=='low' else 1];c=manifest['candidates'][i]
        require(row['historical_proof']['round9_candidate_index']==i and c['sha256']==row['original_ASCII_expected_sha256'] and c['size']==row['original_ASCII_expected_size_bytes'] and c['compressed_backup']['path']==p['path'] and c['compressed_backup']['sha256']==p['sha256'] and c['compressed_backup']['size']==p['size_bytes'], 'original archival route pins without archive-body read')
        matches=[v for v in backups['records'] if v['original']['path']==c['path']]
        require(len(matches)==1 and matches[0]['verified_decompressed']==dict(size=c['size'],sha256=c['sha256']), 'retained original whole decompressed EOF proof')
        h=row['historical_proof'];gr=read(h['actual_GROUPR_receipt_pin']);dr=read(h['actual_DRAGR_receipt_pin']);ih=read(h['actual_DRAGR_input_hashes_pin']);dp=Path(h['actual_DRAGR_deck_pin']['path'])
        require(gr['returncode']==0 and gr['output_sha256']==c['sha256'] and dr['returncode']==0 and ih[str(dp.parent/'tape24')]==c['sha256'] and ih[str(dp)]==h['actual_DRAGR_deck_pin']['sha256'], 'original successful GROUPR/DRAGR source lineage')
        if row['lane']=='high':
            old=next(v for v in prior['inputs'] if v['nuclide']==row['nuclide'])
            low=next(v for v in inputs if v['nuclide']==row['nuclide'] and v['lane']=='low')
            low_receipt=read(low['historical_proof']['actual_DRAGR_receipt_pin'])
            require(p==old['current_original_input_full_pin'] and ih[str(dp.parent/'tape29')]==low_receipt['output_sha256'], 'same actual all34 high input and imported own low output Source lineage')
        comparison=read(h['retained_prior_finite_source_comparison_pin'])
        require(comparison['nuclide']==row['nuclide'] and comparison['status']=='DIRECT_TEMPERATURE_REFERENCE_COMPLETE' and len(comparison['finite_weighted_tables'])==144 and comparison['low_replay']['status']=='GENDF_TO_STORED_SCATTER_EXACT' and comparison['high_or_single_replay']['status']=='GENDF_TO_STORED_SCATTER_EXACT', 'retained historical context only')
        routes.append(deck(row))
    require(sum(v['original_ASCII_expected_size_bytes'] for v in inputs)==plan['original_decompressed_payload_expected_bytes']==1156737672 and sum(v['current_original_input_full_pin']['size_bytes'] for v in inputs)==plan['original_compressed_payload_expected_bytes']==276016193, 'exact sixteen original archive sizes')
    expected=dict(expected_nuclides=8,expected_archives=16,expected_temperature_records=64,expected_archive_temperature_records=128,expected_finite_dilution_nodes=1152,expected_leaf_records=3456)
    require(all(plan[k]==v for k,v in expected.items()), 'eight fuels x eight T x eighteen finite points x three leaf targets')
    for k in ('actual_current_SCI1_pin','actual_current_SCI2_pin'):current(plan[k]);SCI_STAT.append(plan[k])
    require(plan['actual_current_SCI1_pin']==prior['actual_current_SCI1_pin'], 'same current original SCI1 fullPF metadata')
    check('Sixteen exact original lane archives bound by metadata; NBESP4/ipflag0/thermal221 and original own-lane ENERGY/flux routes checked from native decks; all science files current7 only')
    host=text_source(ready['host_source_pin']);oldhost=(PRIOR/'run_guarded_all34_original_ascii_infinite_SCAT.py').read_text()
    start=' class Resources:';end=' resources=Resources();'
    require(host[host.index(start):host.index(end)]==oldhost[oldhost.index(start):oldhost.index(end)], 'whole original Resources methods unchanged')
    for token in ('runner.execute(stage,\'eight_fuel_64T_finite18_P0_SCAT\',cmd,600)',"require(len(runner.records)==1 and runner.records[0]['status']=='PASS'",'1800-(time.monotonic()-start)',"full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","full.OwnRSSSerialExecutor(out",'512*2**20',"'fresh control namespace; no retry'"):
        require(token in host, 'unchanged original serial ownership/time/RSS/noRetry controls')
    require('len(roots)==51' in w and 'now-self.started<600 and peak<512*2**20' in w and "total+sum(unlinked.values())<2*2**30" in w, 'child cap exact Source control')
    prior_cli=read(pin(PRIOR/'FINAL_ROOT_REVIEWABLE_CLI.json'))
    prefix=ready['original_complete_ENV_Python_B_prefix']
    require(prefix==prior_cli['argv'][:11] and len(prefix)==11 and prefix[0]=='/usr/bin/env' and prefix[1:3]==['-u','PYTHONOPTIMIZE'] and prefix[-1]=='-B' and all(v in prefix for v in ('PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1')), 'same original exact Python/env/no-write/singlethread prefix')
    pub=text_source(ready['final_publisher_Source_pin'])
    for token in ("type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None", "type(gt['exit_code'])is int and gt['exit_code']==0 and gt.get('session_id')is None", "gd['ready_pin']==pready", "not any(os.path.lexists(q)for q in targets)", "selected=ready['selected_Source_pins']+[pready,pg]"):
        require(token in pub, 'once Root final publication binds genuine peer/generation tools and exact READY')
    require('runner.execute' not in pub and 'subprocess' not in pub, 'publisher only Source/metadata writes')
    total=0;files=0
    for root in map(Path,roots):
        if not root.exists():continue
        for p in root.rglob('*'):
            s=p.lstat();require(not stat.S_ISLNK(s.st_mode), 'no alias in joint metadata ledger')
            if stat.S_ISREG(s.st_mode):total+=s.st_size;files+=1
    extra=0;nodes=set()
    for p in plan['explicit_cumulative_metadata_file_pins']:
        current(p);node=tuple(p['identity'][:2]);require(node not in nodes, 'distinct physical explicit metadata nodes');nodes.add(node)
        if not any(Path(p['path']).is_relative_to(Path(root)) for root in roots):extra+=p['size_bytes']
    require(total+extra<2*2**30, 'current stat-only cumulative Source+retained roots below unchanged2GiB')
    check('Exact unchanged original Resources, owning OwnRSS/Serial MRO, one child, noRetry, 512MiB/600s/1800s/2GiB controls and all49+TOP+OUT51 roots verified')
    post=read(plan['prior_all34_actual_post_pin']);posttools=read(plan['prior_all34_actual_post_tools_pin'])
    require(post['status']=='PASS_ACTUAL_ALL34_ASCII_234T_702_10741939_INFINITE_P0_WORDS_WITH_METADATA_INDEX_LIMITATION' and post['failure'] is None and post['metadata_only'] is True and post['all_metadata_fields_correct_claimed'] is False and type(post['metadata_index_field_limitation']) is dict and all(contains(post,plan[k]) for k in ('prior_all34_actual_summary_pin','prior_all34_actual_evidence_pin','prior_all34_actual_true_tools_pin')), 'actual sole corrected all34 post pin and truthful metadata-index limitation')
    false_flags(post)
    tools_closed(posttools,'actual_review_return',plan['prior_all34_actual_post_pin'],'review_pin')
    actualtools=read(plan['prior_all34_actual_true_tools_pin'])
    tools_closed(actualtools,'actual_terminal_return',plan['prior_all34_actual_summary_pin'],'report_pin')
    retirement=read(plan['actual_precise_retirement_receipt_pin'])
    require(retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1' and retirement['mode']=='execute' and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and retirement['failure'] is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4, 'same exact prior retained retirement only')
    for p in retirement['actual_released_pins']:require(not os.path.lexists(p['path']), 'only old four precise retired roles absent')
    check('Actual all34 closed0 and sole corrected metadata post bind exact fullPFs; original metadata index limitation retained; retirement metadata unchanged; no broader qualification')
    selected=ready['selected_Source_pins']+[pr,pg]
    for p in selected:current(p)
    for p in SCI_STAT:current(p)
    elapsed=time.monotonic()-START;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    require(elapsed<600 and peak<512*2**20, 'independent audit own time/RSS bounded')
    return dict(selected_Source_pins=selected,Source_ready_pin=pr,Root_generation_true_tools_pin=pg,
      control_plan_pin=ready['control_plan_pin'],final_author_freeze_pin=plan['author_Pre_Root_generation_Source_freeze_pin'],
      complete_hash_checked_Source_metadata_pins=list(HASHED.values()),science_files_current7_only=SCI_STAT,
      original_native_deck_routes=routes,expected_scope_counts=expected,original_caps=CAPS,
      complete_joint_roots=roots,stat_only_joint_files=files,stat_only_joint_bytes=total,
      stat_only_explicit_outer_metadata_bytes=extra,stat_only_cumulative_bytes=total+extra,
      prior_all34_actual_post_pin=plan['prior_all34_actual_post_pin'],
      prior_all34_truthful_metadata_index_limitation=post['metadata_index_field_limitation'],
      finite_metadata_index_copy_corrected=True,exact_original_scalar_matrix_function_sha256=hashlib.sha256(defs['matrix']).hexdigest(),
      exact_original_scalar_packed_function_sha256=hashlib.sha256(defs['packed']).hexdigest(),
      elapsed_seconds=elapsed,auditor_SELF_peak_bytes=peak)

def main():
    require(not os.path.lexists(REVIEW), 'once independent Source review report, preserve failures')
    result=dict(schema='INDEPENDENT_EIGHT_FUEL_FINITE18_SCAT_FROZEN_SOURCE_REVIEW_V1',
      status='FAIL_INDEPENDENT_FROZEN_SOURCE_REVIEW',failure=None,source_only=True,
      scientific_payload_read=False,gzip_payload_read=False,SCI_payload_read=False,
      original_ASCII_payload_read=False,candidate_imported=False,sciencebody_imported_or_executed=False,
      Source_preparation_executed_by_peer=False,Source_publication_executed_by_peer=False,
      business_rerun_by_peer=False,matrix_math_recomputed_by_peer=False,native_engines_started_by_peer=0,
      scope='Frozen finite18 P0 producer Source eligibility only; no actual finite replay, SPH/material/full-reference physics or AAA/ABA qualification',**FALSE)
    error=None
    try:
        result.update(audit());result['status']='PASS_INDEPENDENT_EIGHT_FUEL_FINITE18_P0_FROZEN_SOURCE_ONLY'
    except BaseException as e:
        error=e;result['failure']=repr(e)
    result['checks_completed']=CHECKS
    result['audit_source_pin']=pin(Path(__file__).absolute())
    with REVIEW.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=pin(REVIEW),**FALSE)),flush=True)
    if error is not None:raise error

if __name__=='__main__':main()

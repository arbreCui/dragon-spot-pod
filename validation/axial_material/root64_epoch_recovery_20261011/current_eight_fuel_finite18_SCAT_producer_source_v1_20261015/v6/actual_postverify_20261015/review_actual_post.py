"""Sole finite P0 actual-run metadata audit. Never read original science bodies."""
import argparse
import hashlib
import json
import math
import os
import resource
import shlex
import stat
import struct
import sys
import time
from pathlib import Path

BASE=Path(__file__).absolute().parents[1]
HERE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts/axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,
 history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,
 free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FLAGS=('business_executed','numerical_executed','compiler_executed','files_deleted')
QUALIFIERS=('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified',
 'physical_neutron_balance_qualified','unreduced_reference_qualified','finite18_replayed',
 'temperature_interpolation_replayed','current_SPH_MASK_context_applied','AAA_qualified','ABA_admitted','goal_complete')
MTS=[2,5,16,17,28,37,*range(51,92)]
SCIENCE=set()
CHECKS=[]

def require(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p):
    require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'} and type(p['path']) is str and type(p['sha256']) is str and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']) and type(p['size_bytes']) is int and type(p['identity']) is list and len(p['identity'])==7 and all(type(v) is int for v in p['identity']) and p['identity'][4]==p['size_bytes'], 'complete typed fullPF')
    q=Path(p['path']);s=q.lstat()
    compiler=(q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15') and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2)
    require(q.is_absolute() and not any(v.is_symlink() for v in(q,*q.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and identity(s)==p['identity'], 'exact immutable current7: '+str(q))

def permitted(q,size):
    require(str(q) not in SCIENCE and q.name not in ('SCI1','SCI2') and q.suffix not in ('.gz','.npy','.npz') and not q.name.startswith('tape'), 'original science-body read prohibited: '+str(q))
    require(q.is_relative_to(ART) or q.suffix in ('.py','.json','.jsonl','.txt','.in','.f90','.log','.sha256','.make') or q.name.startswith(('file_data_gendf_','file_data_dendf_')), 'new actual output or Source/metadata only')
    require(size<(64*2**20 if q.is_relative_to(ART) else 8*2**20), 'bounded actual output/metadata')

def pin(q):
    q=Path(q);s=q.lstat();permitted(q,s.st_size)
    p=dict(path=str(q),sha256='0'*64,size_bytes=s.st_size,identity=identity(s));current(p)
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno()))==p['identity'], 'opened metadata7')
        p['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
        require(identity(os.fstat(f.fileno()))==p['identity'], 'whole metadata EOF7')
    current(p);return p

def whole(p):
    current(p);q=Path(p['path']);permitted(q,p['size_bytes'])
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno()))==p['identity'], 'opened actual metadata7')
        raw=f.read();require(identity(os.fstat(f.fileno()))==p['identity'], 'whole actual metadata EOF7')
    require(len(raw)==p['size_bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'], 'actual output fullEOF SHA/size')
    current(p);return raw

def read(p):return json.loads(whole(p))
def get(q):
    p=pin(q);return read(p),p
def hash_text(v):
    return type(v) is str and len(v)==64 and all(c in '0123456789abcdef' for c in v)
def fword(v):return struct.pack('<f',v)
def fvalue(v):return struct.unpack('<f',fword(v))[0]
def false_qual(v):require(all(v[k] is False for k in QUALIFIERS+('full_reference_qualified','historical_machine_bit_replay','original_XSM_memory_bits_verified')), 'producer evidence only; broad qualifications false')
def true_return(v,key,p,stdout_key):
    r=v[key]
    require(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code']==0 and type(r['exit_code']) is int and r['exit_code']==0 and r.get('session_id') is None and type(r['output']) is str and json.loads(r['output'].strip().splitlines()[-1])[stdout_key]==p, 'genuine original typed closed0/stdout exact fullPF')
def unique(rows):
    out={}
    for p in rows:
        if p['path'] in out:require(out[p['path']]==p, 'one literal path consistent fullPF')
        out[p['path']]=p
    return list(out.values())
def check(name):CHECKS.append(name)
def budget(start):
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    require(peak<512*2**20 and time.monotonic()-start<600, 'bounded metadata post-auditor SELF512/600s')
    return peak

def source_sigma(row):
    p=row['historical_proof']['actual_GROUPR_deck_pin'];raw=whole(p);lines=[s.strip() for s in raw.decode().splitlines() if s.strip()]
    i=lines.index('groupr')+3
    while lines[i].startswith("'"):i+=1
    cards=[]
    for _ in range(2):
        values=[]
        while True:
            part=lines[i];values.extend(float(v) for v in part.split('/')[0].split());i+=1
            if '/' in part:break
        cards.append(values)
    require(cards[0]==row['original_source_deck_temperatures_K'] and len(cards[1])==10 and cards[1][0]==1e10, 'same native original Source deck temperatures and dilution cards')
    return cards[1][1:]

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def compact_resources(value):
    result={k:v for k,v in value.items() if k not in ('original_history','complete_joint')}
    for role in ('original_history','complete_joint'):
        original=value[role];selected={k:v for k,v in original.items() if k not in ('resource_roots','declared_resource_roots','resource_scope_contract')}
        for key in ('resource_roots','declared_resource_roots','resource_scope_contract'):
            if key in original:
                selected[key+'_sha256']=canonical_sha(original[key])
                if isinstance(original[key],(list,dict)):selected[key+'_count']=len(original[key])
        result[role]=selected
    return result

def compact_record(value):
    result=dict(value)
    for key in ('resource_before','resource_after'):
        if isinstance(result.get(key),dict):result[key]=compact_resources(result[key])
    return result

def inspect(args,start):
    seven=json.loads(args.root_tools_seven_id)
    pRootTools=dict(path=args.root_tools_summary,sha256=args.root_tools_sha256,size_bytes=seven[4],identity=seven)
    tools=read(pRootTools);terminal=tools['actual_terminal_return'];H=json.loads(terminal['output'].strip().splitlines()[-1])['report_pin']
    require(H['path']==str(ART/'Root_actual_eight_fuel_finite18_SCAT_summary.json'), 'exact literal owning finite report role')
    true_return(tools,'actual_terminal_return',H,'report_pin')
    h=read(H)
    require(h['schema']=='ACTUAL_EIGHT_FUEL_FINITE18_SCAT_GUARDED_REPORT_V1' and h['status']=='ACTUAL_EIGHT_FUEL_64T_FINITE18_P0_WORDS_CLOSED0_ONLY' and h['failure'] is None and h['secondary_failures']==[] and h['final_report_resource_check_passed'] is True and h['original_guard_MRO_unchanged'] is True and h['original_caps']==CAPS and h['native_engines_started']==0 and h['original_ASCII_files_written']==0, 'actual sole finite owning guarded report success')
    false_qual(h)
    sf=read(h['source_freeze_pin']);hf=read(h['host_freeze_pin']);plan=read(sf['control_plan_pin'])
    science_pins=[plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[r['current_original_input_full_pin'] for r in plan['inputs']]
    SCIENCE.update(p['path'] for p in science_pins)
    for p in science_pins:current(p)
    require(h['source_freeze_pin']==pin(BASE/'FINAL_SOURCE_FREEZE.json') and h['host_freeze_pin']==pin(BASE/'FINAL_HOST_FREEZE.json') and hf['selected_source_freeze_pin']==h['source_freeze_pin'] and sf['original_caps']==hf['original_caps']==plan['original_caps']==CAPS, 'exact published owning Source freezes and plan')
    pub,pPub=get(BASE/'FINAL_PUBLICATION_RECEIPT.json');pubtools,pPubTools=get(BASE/'ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json')
    require(type(pubtools['exit_code']) is int and pubtools['exit_code']==0 and pubtools.get('session_id') is None and json.loads(pubtools['output'].strip().splitlines()[-1])['receipt_pin']==pPub and pub['final_source_freeze_pin']==h['source_freeze_pin'] and pub['final_host_freeze_pin']==h['host_freeze_pin'], 'genuine original once Source publication0')
    proof=pub['peer_and_generation_proof'];peer=read(proof['peer_review_pin']);peert=read(proof['peer_true_tools_pin']);gen=read(proof['Source_generation_true_tools_pin']);ready=read(proof['selected_Source_only_ready_pin'])
    require(peer['status']=='PASS_INDEPENDENT_V6_EIGHT_SERIAL_FUEL_FINITE18_P0_FROZEN_SOURCE_ONLY' and peer['failure'] is None and peer['source_only'] is True and peer['scientific_payload_read'] is False and peer['original_stage_ledger_field_exact_path']=='gendf-stage/stages.json' and ready['control_plan_pin']==sf['control_plan_pin'] and sf['Root_same_round_peer_and_generation_proof']==hf['Root_same_round_peer_and_generation_proof']==proof, 'exact same-round independent Source/generation proof and metadata-copy correction')
    true_return(peert,'actual_review_return',proof['peer_review_pin'],'review_pin');true_return(gen,'actual_Source_preparation_return',proof['selected_Source_only_ready_pin'],'ready_pin')
    light,pLight=get(BASE/'ROOT_FINAL_LIGHT_REVIEW_20261015.json');lighttools,pLightTools=get(BASE/'ROOT_FINAL_LIGHT_TRUE_TOOL_RETURN_20261015.json')
    require(type(lighttools['exit_code']) is int and lighttools['exit_code']==0 and lighttools.get('session_id') is None and json.loads(lighttools['output'].strip().splitlines()[0])['review_pin']==pLight and light['status']=='PASS_FINAL_SAME_ROUND_SOURCE_METADATA_CLI24_OUTPUT_ABSENT' and light['failure'] is None and light['source_only'] is True and light['source_freeze_pin']==h['source_freeze_pin'] and light['host_freeze_pin']==h['host_freeze_pin'] and light['same_round_proof']==proof and light['original_caps']==CAPS, 'genuine Root final LIGHT0 exact Source proof')
    argv,pArgv=get(BASE/'ROOT_EXACT_ACTUAL24_ARGV.json');cli=read(pub['final_CLI_pin'])
    require(shlex.split(lighttools['output'].strip().splitlines()[1])==argv and argv==cli['argv']==shlex.split(tools['exact_executed_command']) and len(argv)==24 and argv[:11]==ready['original_complete_ENV_Python_B_prefix'] and argv[11]==hf['host_source_pin']['path'] and light['final_CLI_pin']==pub['final_CLI_pin'], 'exact actual executed CLI24 and published pins')
    check('Real Root actual closed0; exact CLI24, frozen Source/generation/peer/publication and final LIGHT original typed tool returns')
    outputs=h['complete_output_pins']+[H]
    actual_paths={str(p) for p in ART.rglob('*') if p.is_file()}
    require(len(outputs)==len({p['path'] for p in outputs}) and actual_paths=={p['path'] for p in outputs}, 'complete dynamic actual output inventory')
    for p in outputs:
        require(Path(p['path']).is_relative_to(ART), 'only new actual output role');whole(p)
    fixed=h['fixed_current_pins'];require(len(fixed)==len({p['path'] for p in fixed}), 'unique complete actual fixed pins')
    required=unique(hf['dependencies']+[h['source_freeze_pin'],h['host_freeze_pin'],hf['host_source_pin'],plan['actual_current_SCI1_pin']]+[r['current_original_input_full_pin'] for r in plan['inputs']])
    require(all(p in fixed for p in required), 'every original declared Source/science input in owning fixed inventory')
    for p in fixed:current(p)
    fixed_digest=hashlib.sha256(json.dumps(fixed,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    child=h['actual_child_receipt'];E=child['report_pin'];e=read(E)
    require(e==h['actual_evidence'] and e['schema']=='ACTUAL_EIGHT_FUEL_FINITE18_SCAT_PRODUCER_COMPARISON_V1' and e['status']==child['status']=='EIGHT_FUEL_64T_FINITE18_P0_RAW_WORDS_EQUAL' and e['source_freeze_pin']==h['source_freeze_pin'] and e['control_plan_pin']==sf['control_plan_pin'] and e['actual_current_SCI1_pin']==plan['actual_current_SCI1_pin'] and e['original_caps']==CAPS and e['eight_fuel_finite18_P0_producer_raw_words_replayed'] is True and e['native_engines_started']==e['original_inputs_written']==e['original_ASCII_files_written']==e['dense_field_spool_files_written']==0, 'actual child finite P0 evidence only, exact owning Source and current SCI1 metadata')
    false_qual(e)
    expected={'compared_original_archives':16,'compared_unique_nuclides':8,'compared_temperature_records':64,'compared_archive_temperature_records':128,'compared_finite_dilution_nodes':1152,'compared_original_leaf_records':3456}
    require(all(e[k]==v for k,v in expected.items()), 'exact finite producer target coverage counters')
    binding=read(e['execution_binding_pin'])
    require(binding['schema']=='EIGHT_FUEL_FINITE18_SCAT_EXECUTION_BINDING_V1' and binding['source_freeze_pin']==h['source_freeze_pin'] and binding['control_plan_pin']==sf['control_plan_pin'] and binding['SCI1_whole_PF_verified_by_original_parent_before_child'] is True and binding['complete_joint_roots']==plan['complete_joint_roots'] and binding['explicit_cumulative_metadata_file_pins']==hf['explicit_cumulative_metadata_file_pins'] and binding['original_caps']==CAPS and binding['output_directory']==str(ART/'inventories'), 'exact actual binding and SCI1 parent whole-PF preverification')
    false_qual(binding)
    names=plan['execution_nuclides'];require(names==['Am241','Pu238','Pu239','Pu240','Pu241','Pu242','U235','U238'], 'exact8 selected names')
    require(e['aggregation_metadata_only'] is True and e['compared_completed_child_reports']==8 and child['metadata_aggregate_of_eight_original_closed_child_reports'] is True and len(h['records'])==len(h['actual_watchdog_checks'])==len(h['actual_child_receipts'])==8, 'all8 actual closed reports before whole qualification')
    pStages=h['original_stage_ledger_pin'];require(pStages is not None and pStages['path']==str(ART/'gendf-stage/stages.json'), 'exact original full stage ledger path')
    stages=read(pStages);require(len(stages['stages'])==8 and [compact_record(v) for v in stages['stages']]==h['records'], 'eight full original records equal compact Host records')
    part_values=[];watch_pins=[];log_pins=[];part_pins=[];watch_values=[]
    require(len(e['original_completed_child_report_pins'])==8, 'all eight original part pins')
    for index,(stage,fullstage,receipt,nuclide) in enumerate(zip(h['records'],stages['stages'],h['actual_child_receipts'],names)):
        require(stage['status']=='PASS' and 0<stage['wall_cap_seconds']<=600 and stage['command'][-2:]==['--nuclide',nuclide], 'original one serial stage cap bound to selected name')
        if index:require(fullstage['started_unix']>=stages['stages'][index-1]['started_unix']+stages['stages'][index-1]['elapsed_seconds'], 'own children originally serial without overlap')
        watch,pWatch=get(ART/(stage['label']+'.watchdog.json'))
        require(watch['command']==stage['command'] and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['rss_cap_mib']==512 and watch['sampled_peak_rss_mib']<512 and 0<watch['wall_cap_seconds']<=stage['wall_cap_seconds'] and watch['elapsed_seconds']<watch['wall_cap_seconds'] and h['actual_watchdog_checks'][index]['path']==pWatch['path'] and h['actual_watchdog_checks'][index]['sha256']==pWatch['sha256'], 'each actual own-child watchdog512/600-or-remaining and closed0')
        cmd=stage['command'];require(len(cmd)==9 and cmd[0]==ready['original_complete_ENV_Python_B_prefix'][-2] and cmd[1]=='-B' and cmd[2]==str(BASE/'compare_eight_fuel_finite18_SCAT.py') and cmd[3]=='--binding-pin' and json.loads(cmd[4])==e['execution_binding_pin'] and cmd[5]=='--expected-parent-pid' and int(cmd[6])>0 and cmd[7:] == ['--nuclide',nuclide], 'each actual worker Source/binding/owning parent/name exact')
        pLog=pin(ART/(stage['label']+'.log'));raw=whole(pLog);require(pLog['sha256']==stage['log_sha256'] and len(raw.splitlines())==1 and json.loads(raw)==receipt, 'each original complete child stdout receipt')
        pPart=receipt['report_pin'];require(pPart==e['original_completed_child_report_pins'][index] and pPart['path']==str(ART/'inventories'/('ACTUAL_'+nuclide+'_FINITE18_SCAT_EVIDENCE.json')), 'each complete pinned part literal role')
        part=read(pPart)
        require(part['schema']=='ACTUAL_SINGLE_FUEL_FINITE18_SCAT_PRODUCER_COMPARISON_V1' and part['nuclide']==receipt['nuclide']==nuclide and part['status']==receipt['status']=='SINGLE_FUEL_8T_FINITE18_P0_RAW_WORDS_EQUAL' and part['execution_binding_pin']==e['execution_binding_pin'] and part['control_plan_pin']==e['control_plan_pin'] and part['source_freeze_pin']==e['source_freeze_pin'] and part['actual_current_SCI1_pin']==plan['actual_current_SCI1_pin'] and part['single_fuel_finite18_P0_producer_raw_words_replayed'] is True and part['original_caps']==CAPS, 'all eight genuine original single-fuel closed reports exact binding')
        require((part['compared_original_archives'],part['compared_unique_nuclides'],part['compared_temperature_records'],part['compared_archive_temperature_records'],part['compared_finite_dilution_nodes'],part['compared_original_leaf_records'])==(2,1,8,16,144,432), 'each original part2archive/8nativeT/16laneT/144node/432leaf coverage')
        require(part['original_SCI_ENERGY_leaf']['name']=='ENERGY' and part['original_SCI_ENERGY_leaf']['kind']==2 and part['original_SCI_ENERGY_leaf']['words']==371 and hash_text(part['original_SCI_ENERGY_raw_sha256']) and part['selective_SCI_read_bytes']>0, 'each exact SCI1 ENERGY/selective-read metadata')
        false_qual(part);part_values.append(part);part_pins.append(pPart);watch_pins.append(pWatch);log_pins.append(pLog);watch_values.append(watch)
    require([r for part in part_values for r in part['actual_extractions']]==e['actual_extractions'] and len({p['path'] for p in part_pins})==8 and len({s['label'] for s in h['records']})==8, 'whole aggregate exactly equals eight persisted original parts, unique labels/pins')
    require(len({json.dumps(p['original_SCI_ENERGY_leaf'],sort_keys=True) for p in part_values})==len({p['original_SCI_ENERGY_raw_sha256'] for p in part_values})==1, 'all eight parts same exact current SCI1 ENERGY role/hash')
    check('Every new output fullEOF SHA/current7 first pass, fixed inputs current7 first pass, one actual binding/stage/watchdog/log and child evidence')
    rows=plan['inputs'];results=e['actual_extractions']
    require([(v['nuclide'],v['lane']) for v in results]==[(v['nuclide'],v['lane']) for v in rows] and len(results)==16 and len({v['nuclide'] for v in rows})==8, 'all16 original archives and eight nuclides exact original order')
    sigma_cards={(v['nuclide'],v['lane']):source_sigma(v) for v in rows}
    dilation_maps={}
    for n in {v['nuclide'] for v in rows}:
        vals=[fvalue(v) for l in ('low','high') for v in sigma_cards[n,l]]
        require(len(vals)==len(set(vals))==18 and all(math.isfinite(v) and v>0 for v in vals), 'original two-lane Source cards produce exact18 unique REAL32 words')
        dilation_maps[n]={fword(v).hex():i+1 for i,v in enumerate(sorted(vals))}
    total_words=total_leaves=total_t=total_bytes=total_nodes=0
    native=set();node_stamps=set();cohorts=[];members=[];pairs={};selected_count=0
    for r,row in zip(results,rows):
        p=row['current_original_input_full_pin'];current(p)
        require(r['nuclide']==row['nuclide'] and r['lane']==row['lane'] and r['SCI_role']==row['SCI_role']=='SCI1' and r['input_encoding']==row['input_encoding']=='gzip' and r['current_original_input_full_pin']==p and r['actual_original_ASCII_EOF_SHA256']==row['original_ASCII_expected_sha256'] and r['actual_decompressed_bytes']==row['original_ASCII_expected_size_bytes'] and r['actual_compressed_EOF_SHA256']==p['sha256'] and r['actual_complete_inventory_pin']==row.get('actual_complete_inventory_pin') and r['original_formatter_already_applied'] is True and r['second_quantization_performed'] is False and r['Mo_historical_input_PF_invented'] is False, 'exact original own lane and whole EOF reported digests, no peer science reread')
        false_qual(r)
        ts=r['temperature_comparisons'];nt=len(row['original_source_deck_temperatures_K'])
        require(nt==len(ts)==8 and [fword(q['actual_original_ASCII_temperature_K']) for q in ts]==[fword(v) for v in row['original_source_deck_temperatures_K']], 'all8 original native temperature REAL32 mappings per lane')
        ledger=r['actual_MF3_MF6_compact_inventory']
        require(len(ledger)==r['all_actual_MF3_MF6_sections_verified'] and [s['section_index_one_based'] for s in ledger]==list(range(1,len(ledger)+1)), 'complete ordered compact MF3/MF6 reaction ledger')
        stamps=set()
        for s in ledger:
            stamp=(s['mf'],s['mt'],s['temperature_K'])
            require(stamp not in stamps and s['mat']==row['mat'] and s['mf'] in(3,6) and 1<=s['nl']<=8 and s['nz'] in(1,10) and s['energy_groups']==370 and any(s['temperature_K']==q['actual_original_ASCII_temperature_K'] for q in ts), 'unique actual reaction/T/original dimensions')
            stamps.add(stamp);mask=bytes.fromhex(s['incident_present_mask_hex'])
            require(len(mask)==370 and all(v in(0,1) for v in mask) and type(s['spectrum_LIST_present']) is bool and s['LIST_records']==sum(mask)+int(s['spectrum_LIST_present']) and hash_text(s['section_header_sha256']) and hash_text(s['LIST_dimension_sequence_sha256']), 'all incident/spectrum LIST counts/dimension digests complete')
        require(r['actual_MF6_MTs']==sorted({s['mt'] for s in ledger if s['mf']==6}), 'all actual MF6 families retained including outside strict47')
        archive_words=0
        for q in ts:
            T=q['actual_original_ASCII_temperature_K'];word=fword(T).hex();at=[s for s in ledger if s['temperature_K']==T and s['mf']==6];mts={s['mt'] for s in at};elastic=[s for s in at if s['mt']==2]
            require(len(elastic)==1 and elastic[0]['nz']==10, 'one original actual elastic10 per lane/nativeT')
            thermals=sorted((mt for mt in mts if 221<=mt<=250),reverse=True)
            indices=[s['section_index_one_based'] for s in at if s['mt'] in MTS or 221<=s['mt']<=250]
            require(q['actual_inventory_section_indexes_one_based']==indices and indices and q['nuclide']==row['nuclide'] and q['lane']==row['lane'] and q['mat']==row['mat'] and q['original_strict47_MTs']==MTS and q['actual_used_strict47_MTs']==[v for v in MTS if v in mts] and q['actual_thermal_MTs_descending']==thermals and q['actual_MF6_MTs_outside_strict47_and_thermal']==[s['mt'] for s in at if s['mt'] not in MTS and not 221<=s['mt']<=250], 'correct copied selected indices exactly match retained ledger; strict47/dynamic thermal metadata')
            selected_count+=1
            require(q['original_MF1_grid_index_one_based']==len([v for v in ts if v['original_MF1_grid_index_one_based']<=q['original_MF1_grid_index_one_based']]) and q['selected_temperature_raw32_hex']==word and q['original_SCI_SUBTMP'].startswith('SUBTMP') and len(q['original_SCI_SUBTMP'])==10 and 1<=int(q['original_SCI_SUBTMP'][6:])<=8 and q['original_temperature_leaf']['name']=='TEMPERATURE' and q['original_temperature_leaf']['kind']==2 and q['original_temperature_leaf']['words']==8 and hash_text(q['original_temperature_leaf_raw_sha256']), 'actual temperature leaf and exact native SUBTMP word metadata')
            require(row['original_ipflag']==0 and row['original_DRAGR_NBESP']==4 and q['original_ENERGY_cutoff_branch']==('existing_REAL32_promoted' if row['lane']=='high' else 'new_GENDF_binary64') and q['original_selfshielding_energy_bounds_eV']==row['original_selfshielding_energy_bounds_eV'] and 1<=q['original_igres0']<=q['original_igres1']<=370 and 0<=q['original_ngther']<=q['original_igrest']<=369 and (bool(thermals) or q['original_ngther']==0) and q['actual_elastic_NL']==elastic[0]['nl'] and q['actual_elastic_NZ']==10 and q['exact_finite18_lane_P0_raw_words_equal'] is True and q['compact_P0_all_original10_dilutions_LIST_only'] is True and q['no_dense_field_spool'] is True, 'exact original own-lane precision/thermal/selfshielding/P0 scope')
            require(hash_text(q['original_lane_own_infinite_reference_binary64_sha256']) and hash_text(q['original_lane_own_elastic_infinite_flux_binary64_sha256']), 'retained own original lane infinity and elastic-flux digests')
            false_qual(q)
            dleaf=q['original_dilution_leaf']
            require(dleaf['name']=='DILUTION' and dleaf['kind']==2 and dleaf['words']==18 and hash_text(q['original_dilution_leaf_raw_sha256']), 'original exact18 DILUTION leaf metadata')
            targets=q['finite_comparisons'];require(len(targets)==9, 'original nine finite columns per lane/nativeT')
            target_words=[];submats=[]
            for z,v in enumerate(targets,1):
                dword=fword(v['original_sigma0_barn_binary64']).hex();expected_word=fword(sigma_cards[row['nuclide'],row['lane']][z-1]).hex();di=dilation_maps[row['nuclide']][dword]
                require(v['original_GENDF_dilution_index_zero_based']==z and v['selected_dilution_raw32_hex']==dword==expected_word==fword(v['SCI_dilution_REAL32']).hex() and v['original_SCI_SUBMAT']=='SUBMAT'+format(di,'04d') and v['exact_finite_P0_three_leaf_raw_words_equal'] is True, 'native original dilution column exactREAL32 mapped to ascending18 SUBMAT; no assumed lane offset')
                stamp=(row['nuclide'],word,dword);require(stamp not in node_stamps, 'every current finite target unique across original lanes');node_stamps.add(stamp);target_words.append(dword);submats.append(v['original_SCI_SUBMAT'])
                require(set(v['comparisons'])=={'SCAT00','NJJS00','IJJS00'}, 'exact three finite P0 leaf roles')
                for name,c in v['comparisons'].items():
                    leaf=c['original_leaf'];limit=370*370 if name=='SCAT00' else 370
                    require(leaf['name']==name and leaf['words']==c['original_words']==c['replayed_words'] and leaf['kind']==c['original_kind']==(2 if name=='SCAT00' else 1) and type(leaf['offset_words']) is int and c['original_byte_offset']==4*leaf['offset_words'] and 0<c['original_words']<=limit and 0<=c['original_byte_offset'] and c['original_byte_offset']+4*c['original_words']<=plan['actual_current_SCI1_pin']['size_bytes'] and (name=='SCAT00' or leaf['words']==370) and hash_text(c['original_raw_sha256']) and c['original_raw_sha256']==c['replayed_raw_sha256'] and c['exact_raw_words_equal'] is True and type(c['mismatching_raw_words']) is int and c['mismatching_raw_words']==0 and c['bounded_mismatch_samples']==[], 'all3456 original/replayed leaf hashes/types/counts/offsets and exact zero mismatches')
                    archive_words+=c['original_words'];total_leaves+=1
                total_nodes+=1
            require(len(set(target_words))==len(set(submats))==9, 'nine unique actual lane finite targets')
            native.add((row['nuclide'],word));key=(row['nuclide'],word);pairs.setdefault(key,{})[row['lane']]=q
            members.append(dict(nuclide=row['nuclide'],lane=row['lane'],temperature_K=T,temperature_raw32_hex=word,original_SUBTMP=q['original_SCI_SUBTMP'],corrected_selected_section_indexes=indices,selected_dilution_raw32_hex=target_words,original_SUBMATs=submats,own_original_infinite_reference_binary64_sha256=q['original_lane_own_infinite_reference_binary64_sha256'],own_original_elastic_infinite_flux_binary64_sha256=q['original_lane_own_elastic_infinite_flux_binary64_sha256'],reference_provenance='same original lane own total[0]/elastic flux[0] as frozen reviewed producer Source; metadata audit does not recompute matrix arithmetic'))
        total_words+=archive_words;total_t+=nt;total_bytes+=r['actual_decompressed_bytes']
        cohorts.append(dict(nuclide=row['nuclide'],lane=row['lane'],temperature_records=nt,finite_nodes=9*nt,target_leaf_records=27*nt,original_words=archive_words,word_mismatches=0,original_ASCII_bytes=r['actual_decompressed_bytes'],actual_MF3_MF6_sections=len(ledger),original_nimpo_unit=row['original_nimpo_unit'],original_ipflag=row['original_ipflag']))
    require(total_t==128 and len(native)==64 and len(pairs)==64 and total_nodes==len(node_stamps)==1152 and total_leaves==3456 and selected_count==128 and total_words>0 and total_bytes==plan['original_decompressed_payload_expected_bytes']==1156737672, 'actual16archives/8nuclides/64nativeT/128laneT/1152nodes/3456leaf/source bytes closure')
    for (n,word),lanes in pairs.items():
        require(set(lanes)=={'low','high'}, 'each native nuclide/T has both original lanes')
        low=lanes['low'];high=lanes['high']
        require(low['original_SCI_SUBTMP']==high['original_SCI_SUBTMP'] and low['original_temperature_leaf']==high['original_temperature_leaf'] and low['original_temperature_leaf_raw_sha256']==high['original_temperature_leaf_raw_sha256'] and low['original_dilution_leaf']==high['original_dilution_leaf'] and low['original_dilution_leaf_raw_sha256']==high['original_dilution_leaf_raw_sha256'], 'both original lanes address identical current nativeT and DILUTION leaf')
        observed={v['selected_dilution_raw32_hex'] for q in (low,high) for v in q['finite_comparisons']}
        require(observed==set(dilation_maps[n]) and {v['original_SCI_SUBMAT'] for q in (low,high) for v in q['finite_comparisons']}=={'SUBMAT'+format(i,'04d') for i in range(1,19)}, 'all18 exact dilution words and all18 ascending SUBMAT membership per nativeT')
    require(e['selective_SCI_read_bytes']==sum(p['selective_SCI_read_bytes'] for p in part_values) and e['selective_SCI_directory_extents']==sum(p['selective_SCI_directory_extents'] for p in part_values), 'exact metadata aggregate selective SCI counters from all eight original reports')
    check('Exact16 archive EOF metadata, eight fuels/64nativeT/128laneT/1152unique finite nodes/3456 exact leaf hashes and zero word mismatches; own-lane references, all18REAL32 membership and all128 copied section-index lists verified')
    roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))==52 and roots[-1]==str(ART) and str(BASE.parent) in roots, 'exact original prior51 plus freshOUT52 including preserved failed output')
    for k in ('resources_before','resources_after','resources_after_including_summary_bytes'):
        res=h[k];j=res['complete_joint'];hist=res['original_history']
        require(j['resource_roots_count']==52 and j['resource_roots_sha256']==canonical_sha(roots) and j['artifact_budget_bytes']==2*2**30 and hist['artifact_budget_bytes']==96*2**30 and res['host_SELF_peak_bytes']<512*2**20 and res['whole_elapsed_seconds']<1800 and j['artifact_bytes']+res['explicit_external_metadata_bytes']+res['host_open_unlinked_bytes']<2*2**30 and hist['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']<96*2**30 and j['disk_free_bytes']-CAPS['cold_reserve_bytes']-2*2**30>=8*2**30, 'all actual original before/after/report-inclusive resource caps')
    require(h['resources_before']['original_history']['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']+2*2**30<96*2**30 and h['wall_seconds']<1800, 'fullfresh original initial history reservation and whole wall cap')
    current_total=0
    for root in map(Path,roots):
        if not root.exists():continue
        for p in root.rglob('*'):
            s=p.lstat();require(not stat.S_ISLNK(s.st_mode), 'all52 namespace no aliases')
            if stat.S_ISREG(s.st_mode):current_total+=s.st_size
    outer=0
    for p in hf['explicit_cumulative_metadata_file_pins']:
        current(p)
        if not any(Path(p['path']).is_relative_to(Path(root)) for root in roots):outer+=p['size_bytes']
    require(current_total+outer<2*2**30, 'current all52 plus explicit metadata below unchanged2GiB')
    retirement=read(h['actual_precise_retirement_receipt_pin'])
    require(h['actual_precise_retirement_receipt_pin']==plan['actual_precise_retirement_receipt_pin']==proof['actual_precise_retirement_receipt_pin'] and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and retirement['failure'] is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4 and all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']), 'same only exact prior four retired roles absent; no peer deletion')
    old_tools=read(plan['prior_finite_failed_Root_true_tools_pin']);old_report=read(plan['prior_finite_failed_Root_report_pin']);old_facts=read(plan['prior_finite_failure_facts_review_pin'])
    require(old_tools['observed_closed'] is True and type(old_tools['original_integer_exit_code']) is int and old_tools['original_integer_exit_code']==1 and type(old_tools['actual_terminal_return']['exit_code']) is int and old_tools['actual_terminal_return']['exit_code']==1 and old_report['status']=='FAILED_EIGHT_FUEL_FINITE18_SCAT_NO_RETRY' and old_report['actual_evidence'] is None and old_facts['original_Root_integer_exit_code']==1 and old_facts['actual_original_finite_P0_equality_unknown'] is True and old_facts['actual_failed_pipeline_reclassified_as_success'] is False, 'old v4 failed pipeline remains failed and unqualified')
    author=read(plan['author_Pre_Root_generation_Source_freeze_pin'])
    preserved=plan['preserved_finite_v1_v2_v3_v4_Source_pins']+plan['retained_frozen_v5_source_metadata_pins']
    for p in preserved:current(p)
    for k,v in author.items():
        if k.startswith('preserved_original_'):
            for p in v:current(p);preserved.append(p)
        elif k.startswith('root_precise_'):current(v);preserved.append(v)
    for p in fixed:current(p)
    for p in science_pins:current(p)
    for p in outputs:whole(p)
    require(read(H)==h and read(E)==e and all(read(p)==part for p,part in zip(part_pins,part_values)), 'same immutable Host/aggregate/all8parts after second whole output/fullPF verification')
    peak=budget(start)
    check('Original600/512MiB/1800s/2GiB actual resource caps; all52 roots; preserved Source versions; fixedcurrent7 twice and every new output EOF fullPF twice')
    return dict(Root_actual_runtime_true_tools_pin=pRootTools,actual_Root_report_pin=H,actual_child_evidence_pin=E,
      actual_execution_binding_pin=e['execution_binding_pin'],actual_watchdog_pins=watch_pins,actual_stage_ledger_pin=pStages,
      actual_child_log_pins=log_pins,actual_single_fuel_report_pins=part_pins,all_actual_output_full_pins=outputs,original_source_review_pin=proof['peer_review_pin'],
      original_source_review_tools_pin=proof['peer_true_tools_pin'],original_generation_tools_pin=proof['Source_generation_true_tools_pin'],
      actual_Root_publication_receipt_pin=pPub,actual_Root_publication_tools_pin=pPubTools,
      necessary_Root_final_LIGHT_review_pin=pLight,necessary_Root_final_LIGHT_tools_pin=pLightTools,
      exact_actual24_argv_pin=pArgv,actual_original_archives=16,actual_unique_nuclides=8,
      actual_native_temperature_records=64,actual_archive_temperature_records=128,actual_finite_nodes=1152,
      actual_original_closed_single_fuel_reports=8,actual_target_leaf_records=3456,actual_original_compared_words=total_words,actual_bit_word_mismatches=0,
      actual_cohort_summaries=cohorts,actual_original_ASCII_total_bytes=total_bytes,
      actual_selective_SCI_bytes=e['selective_SCI_read_bytes'],science_files_dual_current7_only_pins=science_pins,actual_fixed_input_current7_count=len(fixed),
      actual_fixed_input_dual_current7_checks=True,original_fixed_input_fullpin_inventory_SHA256=fixed_digest,
      all_new_output_bytes_independently_dual_EOF_current7_checked=True,
      correct_metadata_index_lists_checked_from_complete_retained_ledger=True,correct_metadata_index_list_records=128,
      own_lane_reference_and_dilution_membership_records=members,all18_REAL32_dilution_words_and_SUBMATs_verified_each_nativeT=True,
      Source_own_lane_infinite_and_elasticflux_routing_preverified=True,actual_retained_compact_reaction_ledger_consistency_checked=True,
      preserved_original_Source_version_and_correction_pins=unique(preserved),original_caps=CAPS,
      actual_watchdog_sampled_peak_rss_mib=max(v['sampled_peak_rss_mib'] for v in watch_values),actual_whole_wall_seconds=h['wall_seconds'],
      complete_joint_roots=roots,actual_current_joint_root_bytes=current_total,actual_current_explicit_outer_metadata_bytes=outer,
      actual_current_cumulative_bytes=current_total+outer,post_auditor_SELF_peak_bytes=peak)

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for suffix in ('summary','sha256','seven-id'):ap.add_argument('--root-tools-'+suffix,required=True)
    args=ap.parse_args();start=time.monotonic();failure=None;facts={}
    target=HERE/'REVIEW.json';require(not os.path.lexists(target), 'once sole post report; preserve any original failed review')
    try:facts=inspect(args,start)
    except BaseException as e:failure=repr(e)
    report=dict(schema='INDEPENDENT_EIGHT_SERIAL_FUEL_FINITE18_SCAT_ACTUAL_RUNTIME_METADATA_POSTVERIFY_V1',
      status='PASS_ACTUAL_EIGHT_FUEL_64T_128LANET_1152NODES_3456_FINITE_P0_LEAF_WORDS' if failure is None else 'FAIL_ACTUAL_EIGHT_FUEL_FINITE18_P0_METADATA_POSTVERIFY',
      failure=failure,metadata_only=True,audit_source_pin=pin(Path(__file__).absolute()),
      gzip_payload_read_by_peer=False,SCI_payload_read_by_peer=False,original_ASCII_payload_read_by_peer=False,
      sciencebody_imported_or_executed=False,business_rerun_by_peer=False,native_engines_started_by_peer=0,
      matrix_math_recomputed_by_peer=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,
      original_XSM_memory_bits_verified=False,full_reference_qualified=False,
      scope='Current eight SCI1 fuel nuclides only: all64 original nativeT, both16 original archives/128laneT, all1152 finite nodes, P0 SCAT00 NJJS00 IJJS00 producer words. Broad finite18/operator/material/reaction/temperature interpolation/SPH/MASK/physics/full-reference/AAA/ABA remain unqualified.',
      **{k:False for k in FLAGS+QUALIFIERS},**facts,checks_completed=CHECKS,elapsed_seconds=time.monotonic()-start)
    with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=report['status'],review_pin=pin(target),**{k:False for k in FLAGS+QUALIFIERS})),flush=True)
    require(failure is None, 'sole actual post retained failure: '+str(failure))

if __name__=='__main__':main()

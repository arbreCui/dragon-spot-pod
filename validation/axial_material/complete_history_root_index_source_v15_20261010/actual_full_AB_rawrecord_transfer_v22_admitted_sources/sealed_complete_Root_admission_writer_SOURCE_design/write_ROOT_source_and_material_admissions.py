"""Standalone Root stdlib SOURCE/material admission writer. SOURCE design only.

It streams full SHA7ID reads and small original META; it never calls the binder,
reader, native engine, guard or business API. Real prior70a7c1 and independent7f50bb
tool returns prove prerequisites directly. Its own future writer return is never
used as those prerequisites. It preserves all54 current logical source pins, old54
expected hashes, all82 prechecked full inputs, all124 ordered temperatures and the
entire original precheck. Writing admissions does not perform or qualify transfer,
protocol controls, XSM bits, multiplicity, native transport or scientific accuracy.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import struct
import sys

ROOT = Path('/Users/wen/spot')
BASE = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = ROOT/'validation/artifacts'
MATERIAL = ART/'axial-material-inputs-20261003'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
HERE = Path('/private/tmp/axmat_rawrecord_fixed_historical_auditor_retention_SOURCE_20261010_tl856qp8')
CAPS = {'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
KNOWN_WRAPPER_SHA = '098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116'
OLD_MANIFEST_SHA = 'f862d822da445bb7674e246c985dc1c8e4caed1f5fcc68e7ace4e791a955d97c'
OLD_PEER_SEAL_SHA = '8058f908bbc8d6e3eae8b997d9a7707640cddfc610c3c508621f8cb232e51b35'
# This is one fixed historical SOURCE retention, never a general hash fallback.
MATERIAL_AUDITOR_ORIGINAL = ROOT/'validation/axial_material/material_audit.py'
MATERIAL_AUDITOR_RETAINED = ART/'axial-material-tools-20261003/material_audit_used_for_ab.py'
MATERIAL_AUDITOR_RETENTION_RECORD = ART/'axial-material-tools-20261003/material_audit_implementation_retention.json'
MATERIAL_AUDITOR_OLD_SHA = '90659465a03f6b9464df5a7780aabbce06aeb8c0bbfb746c3dc40eda1b6afed5'
MATERIAL_AUDITOR_CURRENT_SHA = 'cb461b94ae61917da63e813e3dae2261d8f48a20834b15b42d0cad9fe0b8ddc9'
MATERIAL_AUDITOR_RETENTION_RECORD_SHA = '1e5cc9cc2edba850080c61dbad8a71e7e76551dc920c8a0fb844017a3b8c5697'
MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA = 'e1755e33f677ad3ded8e5722d76f1abe4dd0d5db8610d015348ca25074b20ba8'
READERS = {
 'native_records':(Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/fullpitch_pnl_s30_b0_closure_v1_20260907/native_records.py'),'67fe414c25f5867e80cc0509c9951522253e572b92998c83c6b32a254c59342b'),
 'stream_records':(Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/finegroup_acceptance/stream_records.py'),'dc2d4e5f6cfa6b6d312669f44db98df5873d049707672bb166b26719fad2df0f')}
UNKNOWN_ACTUAL_TRANSFER_QUALIFICATION_SHA256 = None
UNKNOWN_REACTION_MULTIPLICITY_QUALIFICATION_SHA256 = None
UNKNOWN_SCIENTIFIC_REFERENCE_SHA256 = None
FALSE = {'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False}

SOURCE_STATUS = 'SOURCE_DESIGN_READY_REAL_ROOT_PREREQUISITES_REQUIRED_NOT_EXECUTED'
PRECHECK_PATH = BASE/'actual_full_AB_rawrecord_transfer_v22_receipts/Root_actual_complete_current150_AB_material_provenance_precheck.json'
PRECHECK_SHA = '689fd702c8cdc530c8be8398c1e7e18857cc09b88e534fc36e16134cb6f1e7a7'
PRECHECK_TERMINAL_PATH = BASE/'actual_full_AB_rawrecord_transfer_v22_receipts/Root_actual_complete_AB_material_provenance_precheck_tool_terminal_return.json'
PRECHECK_TERMINAL_SHA = 'efe5854af938d40d7973b14aae9dc0547a850f094e4e71052dfdf760d7cf4590'
SOURCE_MANIFEST_SHA = '641682743ba9f411dd5d09eae4c2df8c3dcce8178f325cc42da71dd1f84f9b4d'
BINDER_SHA = '52b8665a6505c0965f3af5c9f42fa440a9dd6df2dcbca1d1f00e3146472fe58f'
PEER_ROOT = Path('/private/tmp/axmat_full_AB_rawrecord_independent_SOURCE_review_20261010_gjmmbjxj')
PEER_REVIEW_SHA = '85514d32a0052678f72f7fc23b9f1729eeca7b7a44ee5912da467408f42d3e2d'
PEER_MANIFEST_SHA = '73dfb77ca4eeedad5a87735752bd3f98799be61dd7900827844ce28aecff35d2'

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)


def ordinary(path,directory=False):
    require(type(path)is Path or isinstance(path,Path),'Path required')
    require(path.is_absolute()and '..'not in path.parts,'absolute no-traversal path required')
    for parent in [*reversed(path.parents),path]:require(not stat.S_ISLNK(parent.lstat().st_mode),'no path alias allowed')
    s=path.lstat();require(stat.S_ISDIR(s.st_mode)if directory else stat.S_ISREG(s.st_mode)and s.st_nlink==1,'ordinary single-link SOURCE/input required')


def pin(path,wanted=None):
    path=Path(path);ordinary(path);s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    require(before==after and(wanted is None or sha==wanted),'complete EOF SHA7ID mismatch')
    return {'path':str(path),'sha256':sha,'size_bytes':s.st_size,'identity':before}


def actual_pin(value):
    require(type(value)is dict and set(value)=={'path','sha256','size_bytes','identity'},'actual whole pin fields required')
    require(type(value['sha256'])is str and len(value['sha256'])==64 and all(c in '0123456789abcdef'for c in value['sha256'])and value['sha256']!='0'*64,'actual nonzero SHA required')
    require(type(value['size_bytes'])is int and value['size_bytes']>=0 and type(value['identity'])is list and len(value['identity'])==7 and all(type(x)is int for x in value['identity'])and value['identity'][4]==value['size_bytes'],'exact7 Python integers required')
    require(pin(value['path'])==value,'real current wholeEOF SHA7ID must equal Root receipt')
    return value


def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:require(key not in result,'duplicate metadata key');result[key]=value
        return result
    def reject(value):raise ValueError('nonfinite metadata '+value)
    result=json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)
    def finite(value):
        if type(value)is dict:return all(finite(x)for x in value.values())
        if type(value)is list:return all(finite(x)for x in value)
        return type(value)is not float or math.isfinite(value)
    require(finite(result),'all metadata floats finite');return result


def read_meta(entry,limit=64*2**20):
    actual_pin(entry);require(entry['size_bytes']<=limit,'predeclared bounded complete metadata file required')
    raw=Path(entry['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'complete metadata read SHA required')
    result=strict_json(raw);actual_pin(entry);return result


def write_new(path,value):
    raw=(json.dumps(value,allow_nan=False,ensure_ascii=True,indent=2)+'\n').encode()
    require(len(raw)<=2*2**20,'small whole SOURCE binding metadata bound')
    with path.open('xb')as f:f.write(raw)


def closed_source_return(value):
    require(type(value)is dict and value.get('closed')is True and value.get('actual_tool_terminal_return_observed')is True,'real externally observed closed SOURCE terminal required')
    tr=value.get('terminal_tool_return');require(type(tr)is dict and type(tr.get('exit_code'))is int and tr['exit_code']==0 and 'session_id'not in tr,'actual typedint0 terminal; no live session')
    require(type(tr.get('chunk_id'))is str and bool(tr['chunk_id'])and type(tr.get('output'))is str,'actual full tool output preserved')
    require(type(tr.get('wall_time_seconds'))in(int,float)and not isinstance(tr['wall_time_seconds'],bool)and math.isfinite(tr['wall_time_seconds'])and tr['wall_time_seconds']>=0,'finite actual SOURCE tool time')


def historical_material_auditor_retention(value,protected,audit_entries):
    """Hash/read SOURCE and small retained metadata only; never run the auditor."""
    row=value['historical_material_source_retention']
    require(type(row)is dict and set(row)=={'schema','resolution_kind','original_path','original_expected_sha256','current_original_source','retained_source','retention_record','full_source_inverse_proof'},'one complete explicit historical SOURCE resolution required')
    require(row['schema']=='ROOT_ACTUAL_FIXED_MATERIAL_AUDITOR_HISTORICAL_RETENTION_V1'and row['resolution_kind']=='historical_exact_source_retention','fixed historical SOURCE resolution schema')
    require(row['original_path']==str(MATERIAL_AUDITOR_ORIGINAL)and row['original_expected_sha256']==MATERIAL_AUDITOR_OLD_SHA and protected[str(MATERIAL_AUDITOR_ORIGINAL)]==MATERIAL_AUDITOR_OLD_SHA,'one fixed logical original path and old producerSHA only')
    current=actual_pin(row['current_original_source']);retained=actual_pin(row['retained_source']);record_pin=actual_pin(row['retention_record']);proof_pin=actual_pin(row['full_source_inverse_proof'])
    require(Path(current['path'])==MATERIAL_AUDITOR_ORIGINAL and current['sha256']==MATERIAL_AUDITOR_CURRENT_SHA and current['size_bytes']==18948,'current original source has real current cb461 pin, never original906')
    require(Path(retained['path'])==MATERIAL_AUDITOR_RETAINED and retained['sha256']==MATERIAL_AUDITOR_OLD_SHA and retained['size_bytes']==18947,'complete genuine retained original906 source required')
    require(Path(record_pin['path'])==MATERIAL_AUDITOR_RETENTION_RECORD and record_pin['sha256']==MATERIAL_AUDITOR_RETENTION_RECORD_SHA and record_pin['size_bytes']==1222,'original complete retention mapping fixed SHA')
    require(Path(proof_pin['path'])==HERE/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json'and proof_pin['sha256']==MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA,'independently SOURCE-reviewed complete one-hunk proof in this new package')
    record=read_meta(record_pin);proof=read_meta(proof_pin)
    require(record['schema_version']==1 and record['status']=='EXACT_MATERIAL_AUDITOR_RETAINED'and record['mapping']==[{'original_path':str(MATERIAL_AUDITOR_ORIGINAL),'original_sha256':MATERIAL_AUDITOR_OLD_SHA,'retained_path':str(MATERIAL_AUDITOR_RETAINED),'retained_sha256':MATERIAL_AUDITOR_OLD_SHA}],'whole original retention origin mapping unchanged')
    require(record['current_reader_path']==str(MATERIAL_AUDITOR_ORIGINAL)and record['current_reader_sha256']==MATERIAL_AUDITOR_CURRENT_SHA and record['audit_json_modified']is False,'original current-source disclosure and unmodified audit receipts required')
    require(type(record['audit_receipts'])is dict and record['audit_receipts']=={audit_entries[s]['path']:audit_entries[s]['sha256']for s in('A','B')},'both entire unchanged original A/B audit receipt hashes')
    require(proof['schema']=='MATERIAL_AUDITOR_COMPLETE_ONE_HUNK_SOURCE_INVERSE_V1'and proof['source_only']is True and proof['original_path']==str(MATERIAL_AUDITOR_ORIGINAL)and proof['original_expected_sha256']==MATERIAL_AUDITOR_OLD_SHA and proof['current_expected_sha256']==MATERIAL_AUDITOR_CURRENT_SHA,'full SOURCE-only inverse provenance required')
    require(proof['pins']=={'current_original_source':current,'retained_source':retained,'retention_record':record_pin,'A_audit':audit_entries['A'],'B_audit':audit_entries['B']},'full source/mapping/audit exact SHA7ID proof bindings')
    for name in('full_current_inverse_equals_retained_bytes','full_inverse_AST_equals_original','all_other_seven_definitions_source_and_AST_exact','all_non_definition_AST_exact','MATERIAL_branch_before_changed_snapshot_line_returns','terminal_default_stage_MATERIAL','analyze_terminal_two_positional_args_no_stage_override'):require(proof[name]is True,'complete Source inverse condition '+name)
    for name in('audit_json_modified','retained_source_executed','actual_transfer_qualified','original_XSM_memory_bits_verified','reaction_multiplicity_verified','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):require(proof[name]is False,'retention proof has no execution/science permission '+name)
    require(type(proof['definition_count'])is int and proof['definition_count']==8,'all eight original auditor definitions retained')
    require(current['size_bytes']<=2*2**20 and retained['size_bytes']<=2*2**20,'bounded full SOURCE reads only')
    current_raw=Path(current['path']).read_bytes();retained_raw=Path(retained['path']).read_bytes()
    require(hashlib.sha256(current_raw).hexdigest()==MATERIAL_AUDITOR_CURRENT_SHA and hashlib.sha256(retained_raw).hexdigest()==MATERIAL_AUDITOR_OLD_SHA,'full SOURCE content SHA before inverse proof')
    old_line="    require(all(modules.count(m) == 1 for m in ('SALT:', 'MCCG:', 'ASM:', 'FLU:')), 'snapshot native module count')"
    new_line="    require(all(modules.count(m) == 1 for m in ('SALT:', 'MCCGT:', 'ASM:', 'FLU:')), 'snapshot native module count')"
    old=retained_raw.decode('utf-8');new=current_raw.decode('utf-8')
    require(proof['full_hunk']=={'old':old_line,'new':new_line}and old.count(old_line)==new.count(new_line)==1 and new.replace(new_line,old_line,1)==old,'one and only complete source byte inverse')
    ot=ast.parse(old);nt=ast.parse(new)
    require(ast.dump(ast.parse(new.replace(new_line,old_line,1)),include_attributes=False)==ast.dump(ot,include_attributes=False),'full inverse AST equals entire old source')
    od={n.name:n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))};nd={n.name:n for n in nt.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
    require(list(od)==list(nd)==['sha','fuel_densities','names','resolve_isotope_rows','metadata_check','terminal','analyze','main'],'all exact original auditor definition names and order')
    ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True)
    for name in od:
        if name!='terminal':require(ast.dump(od[name],include_attributes=False)==ast.dump(nd[name],include_attributes=False)and ''.join(ol[od[name].lineno-1:od[name].end_lineno])==''.join(nl[nd[name].lineno-1:nd[name].end_lineno]),'every other full auditor function bytes and AST unchanged')
    require([ast.dump(n,include_attributes=False)for n in ot.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]==[ast.dump(n,include_attributes=False)for n in nt.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))],'all auditor globals/imports AST unchanged')
    terminal=od['terminal'];material_test=ast.dump(ast.parse("stage == 'MATERIAL'",mode='eval').body,include_attributes=False)
    branches=[n for n in terminal.body if isinstance(n,ast.If)and ast.dump(n.test,include_attributes=False)==material_test]
    require(len(branches)==1 and isinstance(branches[0].body[-1],ast.Return)and isinstance(terminal.args.defaults[-1],ast.Constant)and terminal.args.defaults[-1].value=='MATERIAL','MATERIAL source branch returns before changed SNAPSHOT check')
    calls=[n for n in ast.walk(od['analyze'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='terminal']
    require(len(calls)==1 and len(calls[0].args)==2 and calls[0].keywords==[],'unchanged analyze uses only default MATERIAL terminal scope')
    for p in(current,retained,record_pin,proof_pin):actual_pin(p)
    return row,[current,retained,record_pin,proof_pin]


def validate_source_value(value):
    require(value['schema']=='ROOT_ACTUAL_COMPLETE_RAWRECORD_SOURCE_ONLY_ADMISSION_V1'and value['source_only']is True,'new real Root SOURCE admission schema')
    require(value['actual_protocol_qualified']is False and value['actual_full_rawrecord_transfer_qualified']is False and value['scientific_accuracy_qualified']is False and value['physical_neutron_balance_qualified']is False and value['AAA_accuracy_qualified']is False and value['ABA_admitted']is False,'Source admission cannot predeclare runtime/science success')
    manifest_pin=actual_pin(value['source_design_manifest']);require(Path(manifest_pin['path'])==HERE/'sealed_SOURCE_manifest.json','this fresh full SOURCE package only')
    manifest=read_meta(manifest_pin);require(type(manifest['files'])is list and manifest['source_only']is True,'complete frozen new source namespace required')
    source_files={row['relative_path']:row for row in manifest['files']}
    require(len(source_files)==len(manifest['files']),'all source namespace names unique')
    require(pin(HERE/'ORIGINAL_UNREADY_PACKAGE/sealed_SOURCE_manifest.json',OLD_MANIFEST_SHA)['sha256']==OLD_MANIFEST_SHA and pin(HERE/'ORIGINAL_SOURCE_PEER/SOURCE_PEER_SEAL.json',OLD_PEER_SEAL_SHA)['sha256']==OLD_PEER_SEAL_SHA,'old full rawrecord SOURCE and independent peer preserved')
    for row in manifest['files']:
        require(type(row['relative_path'])is str and row['relative_path']and not Path(row['relative_path']).is_absolute()and '..'not in Path(row['relative_path']).parts,'source manifest confined relative path')
        current=pin(HERE/row['relative_path']);require(current['sha256']==row['sha256']and current['size_bytes']==row['size_bytes']and current['identity']==row['identity'],'complete new source file exact pin')
    review_entry=actual_pin(value['independent_source_review']);review=read_meta(review_entry)
    require(review['schema']=='INDEPENDENT_CURRENT150_AB_FULL_RAWRECORD_BINDING_HOST_SOURCE_REVIEW_V1'and review['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and review['all_checks_passed']is True and review['blockers']==[],'actual independent new Source peer PASS needed')
    checks=review['checks'];require(type(checks)is list and bool(checks)and all(type(r)is dict and r.get('pass')is True for r in checks),'complete typedtrue peer Source checks')
    require(review['qualified_source_manifest_sha256']==manifest_pin['sha256']and review['qualified_generator_sha256']==pin(HERE/'generate_ROOT_actual_rawrecord_binding.py')['sha256']and review['qualified_original_wrapper_sha256']==KNOWN_WRAPPER_SHA,'new exact binder/wrapper qualification')
    require(review['qualified_host_template_sha256']==pin(HERE/'full_AB_rawrecord_genuine_host_UNREADY.py')['sha256']and review['qualified_protocol_source_sha256']==pin(HERE/'full_rawrecord_protocol_controls_UNREADY.py')['sha256'],'new exact host/protocol Source qualification')
    terminal_entry=actual_pin(value['independent_source_terminal']);terminal=read_meta(terminal_entry);closed_source_return(terminal)
    require(terminal['source_only']is True and terminal['review_sha256']==review_entry['sha256'],'actual closed peer terminal binds exact saved review')
    return value,[manifest_pin,review_entry,terminal_entry],manifest


def validate_material_value(value):
    require(value['schema']=='ROOT_ACTUAL_CURRENT150_AB_MATERIAL_PROVENANCE_BINDING_ADMISSION_V1'and value['source_only']is True,'real material provenance admission metadata required')
    closed_source_return(value)
    for key in ('same_current_geometry_temperatures_composition_verified','protected_material_source_maps_complete','no_material_decoder_or_native_engine_called'):require(value[key]is True,key)
    for key in ('scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','original_XSM_memory_bits_verified','reaction_multiplicity_verified'):require(value[key]is False,key+' remains false')
    require(value['actual_transfer_qualification_sha256']is None and value['actual_scientific_reference_sha256']is None,'unknown future scientific/runtime pins remain None')
    p={k:actual_pin(value[k])for k in ('case_spec','material_inputs','material_results','python')}
    require(Path(p['case_spec']['path'])==ROOT/'validation/axial_material/case_spec.json'and Path(p['material_inputs']['path'])==MATERIAL/'material_inputs.json'and Path(p['material_results']['path'])==MATERIAL/'material_results.json'and Path(p['python']['path'])==PYTHON,'exact original Source/metadata/Python paths')
    case=read_meta(p['case_spec']);inputs=read_meta(p['material_inputs']);results=read_meta(p['material_results'])
    require(results['inputs_manifest_sha256']==p['material_inputs']['sha256']and results['physical_accuracy_accepted']is False,'real saved material result binds full original input manifest and limits')
    geo=case['geometry'];mat=case['materials'];cfg=inputs['config'];igeo=inputs['geometry']
    require(geo['radial_regions']==igeo['regions']==8 and geo['physical_z_edges_cm']==[0,50,100,150]and geo['radial_boundary']=='white isotropic albedo one, NOT specular reflection'and geo['axial_boundary']=='vacuum at both ends','current finite150 boundaries and8 original regions')
    require(geo['radii_inner_to_outer_cm']==igeo['radii_cm']==[.11,.308712,.381084,.412536,.4225,.435,.485]and geo['hex_edge_cm']==igeo['hex_side_cm']==.61776479,'same current radial geometry')
    require(mat['temperature_C_in_every_zone']=={'fuel_and_hole':750,'clad_and_gap':620,'sodium':475}and mat['kelvin_offset']==273.15 and(cfg['fuel_C'],cfg['clad_C'],cfg['sodium_C'])==(750.,620.,475.),'current same-temperature A/B target')
    require(mat['A']['rnr_cc_p_Pu']==cfg['pu_A']==.21 and mat['A']['rnr_cc_p_U']==cfg['u_A']==.79 and mat['B']['rnr_cc_p_Pu']==cfg['pu_B']==.2436 and mat['B']['rnr_cc_p_U']==cfg['u_B']==.7564,'actual declared A/B composition metadata')
    require(case['cases']==inputs['cases']=={'AAA':['A','A','A'],'ABA':['A','B','A']}and inputs['fission_components_expected']==32 and inputs['material_entries_expected']==62,'unreduced current case/material inventories')
    targets=case['predeclared_decisions']['shape_targets'];require(targets['normalized_nu_fission_max_relative_difference_in_fuel_bins']==.03 and targets['fission_normalized_scalar_flux_volume_weighted_relative_l2_max']==.01,'original scientific3%/1% thresholds preserved')
    require(case['reference']['normalization']=='one global integrated nu-fission normalization; no per-layer or per-group scaling','original global normalization preserved')
    provenance=[]
    for row in inputs['source_files'].values():provenance.append(pin(row['path'],row['sha256']))
    for relative,wanted in inputs['generated_sha256'].items():
        require(type(relative)is str and not Path(relative).is_absolute()and '..'not in Path(relative).parts,'original generated input confined path');provenance.append(pin(MATERIAL/relative,wanted))
    audit_entries={s:actual_pin(value['material_audits'][s])for s in ('A','B')}
    macro_entries={s:actual_pin(value['macro_inputs'][s])for s in ('A','B')}
    protected={}
    for state in ('A','B'):
        audit_entry=audit_entries[state];require(Path(audit_entry['path'])==MATERIAL/state/'material_audit.json'and audit_entry['sha256']==results['states'][state]['material_audit_sha256'],'actual A/B audit binds producer result')
        require(Path(macro_entries[state]['path'])==MATERIAL/state/'macro.ascii','original full A/B macro path')
        audit=read_meta(audit_entry);r=results['states'][state]
        require(audit['state']==state and audit['status']=='PIN_MATERIAL_DATA_CHECKED_WITH_DECLARED_SPH_REPLAY_LIMIT'and audit['production_accuracy_accepted']is False and audit['native_engines_started']==0,'original honest audited material scope')
        require((audit['mixtures'],audit['microscopic_entries'],audit['fission_components'])==(8,62,32)and(r['groups'],r['regions'],r['fission_components'],r['snapshots'])==(370,8,32,1),'original full370/8/32 material metadata')
        rows=audit['microscopic'];require(type(rows)is list and len(rows)==62 and [row['index']for row in rows]==list(range(1,63))and{row['mixture']for row in rows}==set(range(1,9)),'complete ordered62 audited isotope rows')
        for row in rows:
            mix=row['mixture'];c=475. if mix==1 else 620. if mix in (2,3)else 750.
            expected=struct.unpack('<f',struct.pack('<f',c+273.15))[0]
            require(type(row['temperature_K'])in(int,float)and not isinstance(row['temperature_K'],bool)and math.isfinite(row['temperature_K'])and struct.pack('<d',float(row['temperature_K']))==struct.pack('<d',expected),'each original audited mixture has declared REAL32 Kelvin bits')
        require(audit['source_sha256'][macro_entries[state]['path']]==macro_entries[state]['sha256'],'real macroSHA from actual audit; no guessed archiveSHA')
        for path,sha in audit['source_sha256'].items():
            require(path not in protected or protected[path]==sha,'shared protected sourceSHA unchanged');protected[path]=sha
        require(type(audit['limits'])is list and bool(audit['limits'])and{row['order']for row in audit['macroscopic']}=={0,1},'retain original SPH/P1 limits; no auditedP2 claim')
    expected=value['protected_material_source_expected_sha256'];require(type(expected)is dict and len(expected)==len(protected)==54 and expected==protected,'complete original54 logical producerSHA map retained verbatim')
    history,history_pins=historical_material_auditor_retention(value,protected,audit_entries)
    declared=value['protected_material_source_pins'];require(type(declared)is list and len(declared)==len(protected)and{r['path']for r in declared}==set(protected),'complete union of original A/B protected sources required')
    for row in declared:
        actual_pin(row)
        if row['path']==str(MATERIAL_AUDITOR_ORIGINAL):require(row==history['current_original_source']and row['sha256']==MATERIAL_AUDITOR_CURRENT_SHA and protected[row['path']]==MATERIAL_AUDITOR_OLD_SHA,'only fixed original906/currentcb461 historical SOURCE exception; real current pin preserved')
        else:require(row['sha256']==protected[row['path']],'all other53 actual original inputs must match producerSHA; no general retention fallback')
        provenance.append(row)
    # Full SHA reads above are not parser calls and do not certify XSM in-memory
    # field bits, physical loss/reaction multiplicity or a coupled reference.
    return value,[*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance,*history_pins],macro_entries,p['python']


def peer_namespace():
    seal_pin=pin(PEER_ROOT/'MANIFEST.json',PEER_MANIFEST_SHA);seal=read_meta(seal_pin)
    require(seal['schema']=='INDEPENDENT_CURRENT150_AB_COMPLETE_RAWRECORD_SOURCE_REVIEW_SEAL_V1'and seal['source_only']is True and seal['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and seal['all_checks_passed']is True,'real sealed independent430 Source review')
    require(type(seal['check_count'])is int and seal['check_count']==430 and seal['qualified_source_manifest_sha256']==SOURCE_MANIFEST_SHA and seal['complete_qualified_source_namespace_unchanged']is True,'full new qualified Source scope')
    rows=seal['files'];require(type(rows)is list and len(rows)==seal['file_count']==10,'all10 independent Source archive files preserved')
    seen=set();pins=[]
    for row in rows:
        relative=row['relative_path'];require(type(relative)is str and relative and not Path(relative).is_absolute()and '..'not in Path(relative).parts and relative not in seen,'complete confined unique peer namespace')
        seen.add(relative);entry=pin(PEER_ROOT/relative)
        require(entry['sha256']==row['sha256']and entry['size_bytes']==row['size_bytes']and entry['identity']==row['identity'],'actual full peer archive SHA7ID');pins.append(entry)
    require(sum(r['size_bytes']for r in rows)==seal['total_file_bytes'],'complete peer namespace bytes')
    review_pin=pin(PEER_ROOT/'REVIEW.json',PEER_REVIEW_SHA);terminal_pin=pin(PEER_ROOT/'actual_SOURCE_review_tool_terminal_return.json')
    require(actual_pin(seal['review'])==review_pin and actual_pin(seal['actual_SOURCE_review_terminal'])==terminal_pin,'independent seal binds exact review and real terminal')
    terminal=read_meta(terminal_pin);closed_source_return(terminal)
    require(terminal['source_only']is True and terminal['review_sha256']==PEER_REVIEW_SHA and terminal['terminal_tool_return']['chunk_id']=='7f50bb','real prior independent Source terminal direct7f50bb')
    return review_pin,terminal_pin,[seal_pin,*pins]

def complete_precheck():
    report_pin=pin(PRECHECK_PATH,PRECHECK_SHA);report=read_meta(report_pin)
    terminal_pin=pin(PRECHECK_TERMINAL_PATH,PRECHECK_TERMINAL_SHA);terminal=read_meta(terminal_pin);closed_source_return(terminal)
    require(terminal['schema']=='ROOT_V22_ACTUAL_COMPLETE_CURRENT150_AB_MATERIAL_PROVENANCE_PRECHECK_TOOL_RETURN_V1'and terminal['source_only']is True and terminal['no_material_decoder_or_native_engine_called']is True,'real Root material Source/META receipt')
    require(terminal['terminal_tool_return']['chunk_id']=='70a7c1'and terminal['precheck_report_sha256']==PRECHECK_SHA,'direct actual prior70a7c1 binds full689fd report, not this writer')
    for name in('scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):require(terminal[name]is False,'Root precheck is not science')
    require(terminal['actual_transfer_qualification_sha256']is None and terminal['independent_coupled_reference_sha256']is None,'Root precheck has no transfer/reference success pins')
    require(report['schema']=='ROOT_ACTUAL_CURRENT150_AB_MATERIAL_PROVENANCE_PRECHECK_V1'and report['status']=='ACTUAL_FULL_EOF_META_WITH_ONE_EXACT_HISTORICAL_SOURCE_RETENTION_NO_TRANSFER_OR_SCIENCE'and report['source_only']is True,'complete real material precheck scope')
    checks=report['checks'];require(type(checks)is list and len(checks)==322 and all(type(r)is dict and r.get('pass')is True for r in checks),'entire322 Root precheck checks retained')
    for name in('same_current_geometry_temperatures_composition_verified','protected_material_source_maps_complete','no_material_decoder_or_native_engine_called','all54_original_logical_Source_entries_preserved'):require(report[name]is True,'complete material precheck condition '+name)
    require(report['all_current_Source_bytes_equal_generation_time']is False,'honest one historicalSource/current difference remains explicit')
    protected=report['protected_material_source_pins'];full=report['complete_all_unique_source_pins'];generated=report['source_and_generated_provenance_pins'];temperatures=report['all124_ordered_temperature_rows']
    require(type(protected)is list and len(protected)==54 and len({r['path']for r in protected})==54,'all54 current logical fullpins')
    require(type(full)is list and len(full)==82 and len({r['path']for r in full})==82,'all82 original unique complete input fullpins')
    require(type(generated)is list and len(generated)==20 and len({r['path']for r in generated})==20,'entire8Source plus12generated provenance')
    require(type(temperatures)is list and len(temperatures)==124,'all124 ordered original isotope temperature rows')
    unique={p['path']:actual_pin(p)for p in full}
    for p in [*protected,*generated,*[report[k]for k in('case_spec','material_inputs','material_results','python')],*report['material_audits'].values(),*report['macro_inputs'].values()]:require(unique[p['path']]==p,'every material/protected/generated pin belongs to full82 original union')
    history=report['historical_exact_SOURCE_retention']
    require(history['logical_original_path']==str(MATERIAL_AUDITOR_ORIGINAL)and history['original_expected_sha256']==MATERIAL_AUDITOR_OLD_SHA and history['only_snapshot_module_name_changed']is True and history['whole_source_inverse_equals_retained']is True and history['no_material_decoder_or_native_engine_called']is True and history['old_audit_JSON_modified']is False,'original fixed exact Source retention disclosed in whole report')
    for name in('current_source_pin','retained_source_pin','retention_record_pin'):require(unique[history[name]['path']]==history[name],'complete82 includes all real historical/current/retention input pins')
    expected=history['complete_original_Source_map'];require(type(expected)is dict and len(expected)==54 and set(expected)=={r['path']for r in protected},'complete old54 producerSHA map remains intact')
    audit_union={};alltemps=[]
    for state in('A','B'):
        audit=read_meta(report['material_audits'][state])
        for path,wanted in audit['source_sha256'].items():require(path not in audit_union or audit_union[path]==wanted,'original shared source hashes equal');audit_union[path]=wanted
        for row in audit['microscopic']:
            mix=row['mixture'];c=475. if mix==1 else 620. if mix in(2,3)else 750.
            b32=struct.pack('<f',c+273.15);temperature=struct.unpack('<f',b32)[0]
            require(type(row['temperature_K'])in(int,float)and not isinstance(row['temperature_K'],bool)and math.isfinite(row['temperature_K'])and struct.pack('<d',float(row['temperature_K']))==struct.pack('<d',temperature),'every actual audited temperature bits')
            alltemps.append({'state':state,'index':row['index'],'mixture':mix,'audited_temperature_K':row['temperature_K'],'audited_parser64_bits':struct.pack('<d',float(row['temperature_K'])).hex(),'declared_float32_Kelvin_bits':b32.hex()})
    require(expected==audit_union and len(audit_union)==54,'full original protected map reconstructed from both unchanged actual audit JSONs')
    require(temperatures==alltemps and [r['state']for r in temperatures]==['A']*62+['B']*62 and [r['index']for r in temperatures]==list(range(1,63))*2,'complete124 original ordered temperature values/types/bitstrings unchanged')
    for p in protected:
        wanted=expected[p['path']]
        if p['path']==str(MATERIAL_AUDITOR_ORIGINAL):require(wanted==MATERIAL_AUDITOR_OLD_SHA and p==history['current_source_pin']and p['sha256']==MATERIAL_AUDITOR_CURRENT_SHA,'one fixed historical906/currentcb exception only')
        else:require(p['sha256']==wanted,'other53 real original paths equal producerSHA')
    return report,terminal,[report_pin,terminal_pin,*full]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',required=True);args=parser.parse_args()
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None,'unoptimized unprofiled stdlib Root metadata writer')
    require(Path(sys.executable).resolve()==PYTHON,'Root uses original actual material Python')
    output=Path(args.output_dir);require(output.is_absolute()and '..'not in output.parts and output.is_relative_to(BASE)and output!=BASE and not os.path.lexists(output),'fresh one-use admission metadata directory under original B')
    ordinary(output.parent,directory=True)
    require(pin(HERE/'sealed_SOURCE_manifest.json',SOURCE_MANIFEST_SHA)['sha256']==SOURCE_MANIFEST_SHA and pin(HERE/'generate_ROOT_actual_rawrecord_binding.py',BINDER_SHA)['sha256']==BINDER_SHA,'exact new derivative641682/binder52b866 only')
    review_pin,peer_terminal_pin,peer_pins=peer_namespace()
    source={'schema':'ROOT_ACTUAL_COMPLETE_RAWRECORD_SOURCE_ONLY_ADMISSION_V1','source_only':True,'source_design_manifest':pin(HERE/'sealed_SOURCE_manifest.json',SOURCE_MANIFEST_SHA),'independent_source_review':review_pin,'independent_source_terminal':peer_terminal_pin,'independent_source_seal':peer_pins[0],**FALSE,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None}
    _,source_pins,_=validate_source_value(source)
    report,root_terminal,material_pins=complete_precheck()
    history=report['historical_exact_SOURCE_retention']
    material={**report,'schema':'ROOT_ACTUAL_CURRENT150_AB_MATERIAL_PROVENANCE_BINDING_ADMISSION_V1','status':'REAL_PREREQUISITE_SOURCE_META_ADMISSION_NOT_TRANSFER_OR_SCIENCE','closed':root_terminal['closed'],'actual_tool_terminal_return_observed':root_terminal['actual_tool_terminal_return_observed'],'terminal_tool_return':root_terminal['terminal_tool_return'],'original_actual_precheck_terminal':material_pins[1],'original_actual_precheck_report':material_pins[0],'complete_original_precheck_report':report,'protected_material_source_expected_sha256':history['complete_original_Source_map'],'historical_material_source_retention':{'schema':'ROOT_ACTUAL_FIXED_MATERIAL_AUDITOR_HISTORICAL_RETENTION_V1','resolution_kind':'historical_exact_source_retention','original_path':history['logical_original_path'],'original_expected_sha256':history['original_expected_sha256'],'current_original_source':history['current_source_pin'],'retained_source':history['retained_source_pin'],'retention_record':history['retention_record_pin'],'full_source_inverse_proof':pin(HERE/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json',MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA)},**FALSE,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None}
    _,contract_material_pins,_,_=validate_material_value(material)
    allpins={p['path']:p for p in[*peer_pins,*source_pins,*material_pins,*contract_material_pins]}
    for p in allpins.values():actual_pin(p)
    # No output directory/file exists until every real prerequisite and full scope
    # has been verified. Neither admission uses this writer's future terminal.
    output.mkdir()
    sp=output/'Root_actual_rawrecord_SOURCE_admission.json';mp=output/'Root_actual_current150_AB_material_provenance_admission.json'
    write_new(sp,source);write_new(mp,material)
    summary={'schema':'ROOT_ACTUAL_CURRENT150_AB_STDLIB_SOURCE_MATERIAL_ADMISSION_WRITER_REPORT_V1','source_only':True,'source_admission':pin(sp),'material_provenance_admission':pin(mp),'original_actual_material_precheck_report':material_pins[0],'original_actual_material_precheck_terminal':material_pins[1],'original_actual_independent_Source_review':review_pin,'original_actual_independent_Source_terminal':peer_terminal_pin,'complete_input_pins':list(allpins.values()),'protected_current_logical_count':54,'original_expected_source_count':54,'complete_original_precheck_unique_inputs':82,'complete_original_source_generated_inputs':20,'complete_original_temperature_rows':124,'complete_original_precheck_checks':322,'complete_independent_Source_checks':430,'current_all_equal_generation':False,'fixed_historical_Source_exception_count':1,'other53_original_source_hashes_equal':True,'original_genuine_host_caps':CAPS,'preconditions_proven_by_prior_real_tool_returns_not_writer_self_return':True,'no_binder_reader_guard_helper_business_or_native_API_called':True,'no_material_numeric_payload_decoded':True,**FALSE,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None}
    write_new(output/'Root_actual_rawrecord_admission_writer_report.json',summary)
    for p in allpins.values():actual_pin(p)
    print(json.dumps({'schema':'ROOT_ACTUAL_CURRENT150_AB_ADMISSION_WRITER_RETURN_V1','source_only':True,'source_admission':summary['source_admission'],'material_provenance_admission':summary['material_provenance_admission'],'writer_report':pin(output/'Root_actual_rawrecord_admission_writer_report.json'),'direct_actual_prerequisite_chunks':['70a7c1','7f50bb'],'protected_current_logical_count':54,'complete_original_unique_input_count':82,'complete_original_temperature_row_count':124,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None,**FALSE},allow_nan=False),flush=True)

if __name__=='__main__':main()

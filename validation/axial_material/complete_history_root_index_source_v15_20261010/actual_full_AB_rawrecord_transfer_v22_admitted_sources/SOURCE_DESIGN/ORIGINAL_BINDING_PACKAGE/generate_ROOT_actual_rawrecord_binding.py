"""Root-only future SOURCE binder, never a transfer/parser/guard executor.

This file is authored and reviewed as text only. Its future main requires real
closed SOURCE and material-provenance receipts supplied by Root. It hashes the
original files without decoding material data, binds the known original two
readers, and creates one fresh D/E SOURCE namespace. No reviewed API is imported.
READY is SOURCE readiness only. All actual transfer/science success pins stay
None. The binding intentionally excludes READY-wrapper SHA to avoid a hash cycle;
the unchanged genuine host independently pins the final READY-wrapper SHA.
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
HERE = Path(__file__).absolute().parent
CAPS = {'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
KNOWN_WRAPPER_SHA = '098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116'
OLD_MANIFEST_SHA = 'f862d822da445bb7674e246c985dc1c8e4caed1f5fcc68e7ace4e791a955d97c'
OLD_PEER_SEAL_SHA = '8058f908bbc8d6e3eae8b997d9a7707640cddfc610c3c508621f8cb232e51b35'
READERS = {
 'native_records':(Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/fullpitch_pnl_s30_b0_closure_v1_20260907/native_records.py'),'67fe414c25f5867e80cc0509c9951522253e572b92998c83c6b32a254c59342b'),
 'stream_records':(Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/finegroup_acceptance/stream_records.py'),'dc2d4e5f6cfa6b6d312669f44db98df5873d049707672bb166b26719fad2df0f')}
UNKNOWN_ACTUAL_TRANSFER_QUALIFICATION_SHA256 = None
UNKNOWN_REACTION_MULTIPLICITY_QUALIFICATION_SHA256 = None
UNKNOWN_SCIENTIFIC_REFERENCE_SHA256 = None
FALSE = {'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False}

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

def source_admission(entry):
    value=read_meta(entry);require(value['schema']=='ROOT_ACTUAL_COMPLETE_RAWRECORD_SOURCE_ONLY_ADMISSION_V1'and value['source_only']is True,'new real Root SOURCE admission schema')
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
    require(review['qualified_source_manifest_sha256']==manifest_pin['sha256']and review['qualified_generator_sha256']==pin(Path(__file__).absolute())['sha256']and review['qualified_original_wrapper_sha256']==KNOWN_WRAPPER_SHA,'new exact binder/wrapper qualification')
    require(review['qualified_host_template_sha256']==pin(HERE/'full_AB_rawrecord_genuine_host_UNREADY.py')['sha256']and review['qualified_protocol_source_sha256']==pin(HERE/'full_rawrecord_protocol_controls_UNREADY.py')['sha256'],'new exact host/protocol Source qualification')
    terminal_entry=actual_pin(value['independent_source_terminal']);terminal=read_meta(terminal_entry);closed_source_return(terminal)
    require(terminal['source_only']is True and terminal['review_sha256']==review_entry['sha256'],'actual closed peer terminal binds exact saved review')
    return value,[entry,manifest_pin,review_entry,terminal_entry],manifest

def material_admission(entry):
    value=read_meta(entry);require(value['schema']=='ROOT_ACTUAL_CURRENT150_AB_MATERIAL_PROVENANCE_BINDING_ADMISSION_V1'and value['source_only']is True,'real material provenance admission metadata required')
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
    declared=value['protected_material_source_pins'];require(type(declared)is list and len(declared)==len(protected)and{r['path']for r in declared}==set(protected),'complete union of original A/B protected sources required')
    for row in declared:actual_pin(row);require(row['sha256']==protected[row['path']],'all actual protected original inputs match full source maps');provenance.append(row)
    # Full SHA reads above are not parser calls and do not certify XSM in-memory
    # field bits, physical loss/reaction multiplicity or a coupled reference.
    return value,[entry,*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance],macro_entries,p['python']

def retarget(text,hunks):
    for old,new in hunks:require(text.count(old)==1,'single exact Source retarget hunk');text=text.replace(old,new,1)
    inverse=text
    for old,new in reversed(hunks):require(inverse.count(new)==1,'single exact inverse Source hunk');inverse=inverse.replace(new,old,1)
    return text,inverse

def functions(text):
    return {n.name:ast.dump(n,include_attributes=False)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source-admission','source-admission-sha256','material-provenance-admission','material-provenance-admission-sha256','source-dir','receipts-dir','host-dir','transfer-dir','protocol-dir'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args()
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None,'unoptimized unprofiled Root SOURCE binding')
    source_entry=pin(args.source_admission,args.source_admission_sha256);material_entry=pin(args.material_provenance_admission,args.material_provenance_admission_sha256)
    source,source_pins,manifest=source_admission(source_entry)
    material,material_pins,macro_pins,python_pin=material_admission(material_entry)
    require(Path(sys.executable).resolve()==PYTHON,'real original pinned Python for future SOURCE binder')
    d,e=Path(args.source_dir),Path(args.receipts_dir);h,o,c=Path(args.host_dir),Path(args.transfer_dir),Path(args.protocol_dir)
    require(d.is_absolute()and e.is_absolute()and d.is_relative_to(BASE)and e.is_relative_to(BASE)and d!=BASE and e!=BASE,'new Source/receipt namespaces beneath original B')
    require(all(p.is_absolute()and p.is_relative_to(ART)and p!=ART for p in(h,o,c)),'only genuine ART descendants are history roots')
    require(len({str(p)for p in(d,e,h,o,c)})==5 and all('..'not in p.parts and not os.path.lexists(p)for p in(d,e,h,o,c)),'one-use separate new D/E/H/O/control namespaces; no retry')
    for p in(d,e,h,o,c):ordinary(p.parent,directory=True)
    # No directory or generated Source exists before all real admissions/pins.
    readers={name:pin(path,sha)for name,(path,sha)in READERS.items()}
    binding={'schema':'ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1','source_only':True,'scientific_qualification_created':False,'source_qualification_sha256':source_entry['sha256'],'source_admission':source_entry,'material_provenance_admission':material_entry,'original_caps':CAPS,'inputs':macro_pins,'readers':readers,'python':python_pin,'public_reader_calls':['native_records.decode(raw_bytes)','stream_records.decode_stream(binary_iterator)'],'full_default_retention':True,'source_manifest':source['source_design_manifest'],'input_pins':list({p['path']:p for p in[*source_pins,*material_pins,*readers.values()]}.values()),'namespaces':{'source':str(d),'receipts':str(e),'host':str(h),'transfer':str(o),'protocol':str(c)},'source_ready_not_runtime_or_science':True,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None,**FALSE}
    d.mkdir();e.mkdir()
    design=d/'SOURCE_DESIGN';design.mkdir()
    for row in manifest['files']:
        origin=HERE/row['relative_path'];dest=design/row['relative_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(origin,dest);require(pin(dest)['sha256']==row['sha256'],'full unfiltered SOURCE copy')
    shutil.copyfile(HERE/'sealed_SOURCE_manifest.json',design/'sealed_SOURCE_manifest.json')
    evidence=d/'ROOT_BINDING_EVIDENCE';evidence.mkdir()
    preserved=[('source_admission.json',source_entry),('material_provenance_admission.json',material_entry),('independent_source_review.json',source['independent_source_review']),('independent_source_terminal.json',source['independent_source_terminal']),('case_spec.json',material['case_spec']),('material_inputs.json',material['material_inputs']),('material_results.json',material['material_results']),('A_material_audit.json',material['material_audits']['A']),('B_material_audit.json',material['material_audits']['B'])]
    for name,entry in preserved:
        shutil.copyfile(entry['path'],evidence/name);require(pin(evidence/name)['sha256']==entry['sha256'],'complete Root SOURCE/material metadata evidence byteexact preservation')
    bp=d/'Root_actual_rawrecord_SOURCE_binding.json';write_new(bp,binding);bpin=pin(bp)
    raw=(HERE/'ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py').read_text();require(hashlib.sha256(raw.encode()).hexdigest()==KNOWN_WRAPPER_SHA,'unchanged full original wrapper')
    wrapper_hunks=[("SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_ROOT_TRUE_BINDING_AND_GENUINE_SUPERVISOR_REQUIRED'","SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'"),("SOURCE_QUALIFICATION_SHA256 = None",'SOURCE_QUALIFICATION_SHA256 = '+repr(source_entry['sha256'])),("ACTUAL_ROOT_BINDING_RECEIPT_SHA256 = None",'ACTUAL_ROOT_BINDING_RECEIPT_SHA256 = '+repr(bpin['sha256']))]
    ready,inverse=retarget(raw,wrapper_hunks);require(inverse==raw and functions(ready)==functions(raw),'all original wrapper functions/caps/data/control Source unchanged')
    target=d/'transfer_full_AB_rawrecord_READY.py';target.write_text(ready);target_pin=pin(target)
    protocol_raw=(HERE/'full_rawrecord_protocol_controls_UNREADY.py').read_text();protocol_hunks=[("SOURCE_STATUS='UNREADY_SOURCE_ONLY_ROOT_ACTUAL_BINDING_REQUIRED'","SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'")]
    protocol_ready,protocol_inverse=retarget(protocol_raw,protocol_hunks);require(protocol_inverse==protocol_raw and functions(protocol_ready)==functions(protocol_raw),'all protocol fixtures/rejects/full fields unchanged')
    protocol=d/'full_rawrecord_protocol_controls_READY.py';protocol.write_text(protocol_ready);protocol_pin=pin(protocol)
    host_raw=(HERE/'full_AB_rawrecord_genuine_host_UNREADY.py').read_text()
    replacements={'SOURCE_STATUS':"'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'",'SOURCE_ARCHIVE':repr(str(d)),'RECEIPTS':repr(str(e)),'HOST':repr(str(h)),'OUT':repr(str(o)),'CONTROL':repr(str(c)),'TARGET':repr(str(target)),'TARGET_SHA':repr(target_pin['sha256']),'PROTOCOL':repr(str(protocol)),'PROTOCOL_SHA':repr(protocol_pin['sha256']),'BINDING':repr(str(bp)),'BINDING_SHA':repr(bpin['sha256']),'SOURCE_ADMISSION_SHA':repr(source_entry['sha256'])}
    host_hunks=[(key+' = None',key+' = '+value)for key,value in replacements.items()]
    host_ready,host_inverse=retarget(host_raw,host_hunks);require(host_inverse==host_raw and functions(host_ready)==functions(host_raw),'all genuinehost functions/guards/caps byte/AST inverse')
    host=d/'full_AB_rawrecord_genuine_host_READY.py';host.write_text(host_ready);host_pin=pin(host)
    for p in binding['input_pins']:actual_pin(p)
    proof={'schema':'ROOT_ACTUAL_RAWRECORD_READY_SOURCE_BINDING_INVERSE_V1','source_only':True,'binding':bpin,'ready_wrapper':target_pin,'ready_protocol':protocol_pin,'ready_genuine_host':host_pin,'wrapper_three_global_hunks':wrapper_hunks,'protocol_one_status_hunk':protocol_hunks,'host_global_only_hunks':host_hunks,'all_original_function_AST_unchanged':True,'all_three_full_byte_inverses_equal_original':True,'wrapper_original_sha256':KNOWN_WRAPPER_SHA,'wrapper_ready_sha_not_in_binding_to_avoid_cycle':True,'genuine_host_pins_ready_wrapper_externally':True,'all_actual_success_pins_remain_None':True,**FALSE}
    write_new(d/'READY_SOURCE_binding_inverse.json',proof)
    write_new(d/'READY_SOURCE_installation_inventory.json',{'schema':'ROOT_ACTUAL_RAWRECORD_READY_SOURCE_INSTALLATION_INVENTORY_V1','source_only':True,'files':[pin(p)for p in sorted(d.rglob('*'))if p.is_file()],'fresh_namespace_paths':binding['namespaces'],'complete_SOURCE_tree_must_be_Root_frozen_before_execution':True,**FALSE})
    print(json.dumps({'schema':'ROOT_ACTUAL_RAWRECORD_READY_SOURCE_BINDING_RETURN_V1','source_only':True,'binding':bpin,'ready_wrapper':target_pin,'ready_protocol':protocol_pin,'ready_genuine_host':host_pin,'source_dir':str(d),'receipts_dir':str(e),'future_host_command':[str(PYTHON),'-B',str(host)],'actual_transfer_qualification_sha256':None,'no_reader_helper_guard_or_business_API_called':True,**FALSE},allow_nan=False),flush=True)

if __name__=='__main__':main()

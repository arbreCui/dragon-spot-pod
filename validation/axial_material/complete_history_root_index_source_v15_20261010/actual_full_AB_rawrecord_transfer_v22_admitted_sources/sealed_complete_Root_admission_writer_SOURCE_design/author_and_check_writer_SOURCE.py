"""Source author only; never imports/executes a reviewed module or data reader."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

QUALIFIED=Path('/private/tmp/axmat_rawrecord_fixed_historical_auditor_retention_SOURCE_20261010_tl856qp8')
PEER=Path('/private/tmp/axmat_full_AB_rawrecord_independent_SOURCE_review_20261010_gjmmbjxj')
E=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_full_AB_rawrecord_transfer_v22_receipts')
PRECHECK=E/'Root_actual_complete_current150_AB_material_provenance_precheck.json'
TERMINAL=E/'Root_actual_complete_AB_material_provenance_precheck_tool_terminal_return.json'
out=Path(tempfile.mkdtemp(prefix='axmat_standalone_stdlib_material_Source_admission_writer_SOURCE_20261010_',dir='/private/tmp'))
baseline=(QUALIFIED/'generate_ROOT_actual_rawrecord_binding.py').read_text()
assert hashlib.sha256(baseline.encode()).hexdigest()=='52b8665a6505c0965f3af5c9f42fa440a9dd6df2dcbca1d1f00e3146472fe58f'
tree=ast.parse(baseline);lines=baseline.splitlines(keepends=True)
nodes={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def part(name):
    n=nodes[name];return ''.join(lines[n.lineno-1:n.end_lineno])+'\n'
prefix=''.join(lines[:min(n.lineno for n in nodes.values())-1])
start=prefix.index('import argparse\n');prefix=prefix[start:]
prefix=prefix.replace('HERE = Path(__file__).absolute().parent','HERE = Path('+repr(str(QUALIFIED))+')')
doc='''"""Standalone Root stdlib SOURCE/material admission writer. SOURCE design only.

It streams full SHA7ID reads and small original META; it never calls the binder,
reader, native engine, guard or business API. Real prior70a7c1 and independent7f50bb
tool returns prove prerequisites directly. Its own future writer return is never
used as those prerequisites. It preserves all54 current logical source pins, old54
expected hashes, all82 prechecked full inputs, all124 ordered temperatures and the
entire original precheck. Writing admissions does not perform or qualify transfer,
protocol controls, XSM bits, multiplicity, native transport or scientific accuracy.
"""
'''
added="""SOURCE_STATUS = 'SOURCE_DESIGN_READY_REAL_ROOT_PREREQUISITES_REQUIRED_NOT_EXECUTED'
PRECHECK_PATH = BASE/'actual_full_AB_rawrecord_transfer_v22_receipts/Root_actual_complete_current150_AB_material_provenance_precheck.json'
PRECHECK_SHA = '689fd702c8cdc530c8be8398c1e7e18857cc09b88e534fc36e16134cb6f1e7a7'
PRECHECK_TERMINAL_PATH = BASE/'actual_full_AB_rawrecord_transfer_v22_receipts/Root_actual_complete_AB_material_provenance_precheck_tool_terminal_return.json'
PRECHECK_TERMINAL_SHA = 'efe5854af938d40d7973b14aae9dc0547a850f094e4e71052dfdf760d7cf4590'
SOURCE_MANIFEST_SHA = '641682743ba9f411dd5d09eae4c2df8c3dcce8178f325cc42da71dd1f84f9b4d'
BINDER_SHA = '52b8665a6505c0965f3af5c9f42fa440a9dd6df2dcbca1d1f00e3146472fe58f'
PEER_ROOT = Path('/private/tmp/axmat_full_AB_rawrecord_independent_SOURCE_review_20261010_gjmmbjxj')
PEER_REVIEW_SHA = '85514d32a0052678f72f7fc23b9f1729eeca7b7a44ee5912da467408f42d3e2d'
PEER_MANIFEST_SHA = '73dfb77ca4eeedad5a87735752bd3f98799be61dd7900827844ce28aecff35d2'
"""
primitive_names=['require','ordinary','pin','actual_pin','strict_json','read_meta','write_new','closed_source_return','historical_material_auditor_retention']
primitives='\n'.join(part(n) for n in primitive_names)
adaptations=[]
def adapt(name,changes):
    old=part(name);new=old
    for a,b in changes:
        assert new.count(a)==1;new=new.replace(a,b,1)
    inverse=new
    for a,b in reversed(changes):assert inverse.count(b)==1;inverse=inverse.replace(b,a,1)
    assert inverse==old
    adaptations.append({'original_definition':name,'hunks':[{'old':a,'new':b}for a,b in changes],'complete_byte_inverse_equals_qualified_binder_definition':True,'complete_AST_inverse_equals_qualified_binder_definition':ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)})
    return new
source_validation=adapt('source_admission',[
 ('def source_admission(entry):','def validate_source_value(value):'),
 ("    value=read_meta(entry);require(value['schema']", "    require(value['schema']"),
 ("pin(Path(__file__).absolute())['sha256']", "pin(HERE/'generate_ROOT_actual_rawrecord_binding.py')['sha256']"),
 ('    return value,[entry,manifest_pin,review_entry,terminal_entry],manifest', '    return value,[manifest_pin,review_entry,terminal_entry],manifest')])
material_validation=adapt('material_admission',[
 ('def material_admission(entry):','def validate_material_value(value):'),
 ("    value=read_meta(entry);require(value['schema']", "    require(value['schema']"),
 ("    return value,[entry,*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance,*history_pins],macro_entries,p['python']", "    return value,[*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance,*history_pins],macro_entries,p['python']")])
extra='''def peer_namespace():
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
'''
writer=doc+prefix+added+'\n'+primitives+'\n'+source_validation+'\n'+material_validation+'\n'+extra
ast.parse(writer);(out/'write_ROOT_source_and_material_admissions.py').write_text(writer)
shutil.copyfile(QUALIFIED/'generate_ROOT_actual_rawrecord_binding.py',out/'qualified_derivative_binder_FULL_SOURCE.py')
context=out/'ACTUAL_PREREQUISITE_META_SOURCE_CONTEXT';context.mkdir()
for p in [PRECHECK,TERMINAL,PEER/'REVIEW.json',PEER/'actual_SOURCE_review_tool_terminal_return.json',PEER/'MANIFEST.json']:
    wanted={PRECHECK:'689fd702c8cdc530c8be8398c1e7e18857cc09b88e534fc36e16134cb6f1e7a7',TERMINAL:'efe5854af938d40d7973b14aae9dc0547a850f094e4e71052dfdf760d7cf4590',PEER/'REVIEW.json':'85514d32a0052678f72f7fc23b9f1729eeca7b7a44ee5912da467408f42d3e2d',PEER/'MANIFEST.json':'73dfb77ca4eeedad5a87735752bd3f98799be61dd7900827844ce28aecff35d2'}.get(p)
    raw=p.read_bytes();assert wanted is None or hashlib.sha256(raw).hexdigest()==wanted
    shutil.copyfile(p,context/p.name)
checks=[]
def check(name,value):
    assert type(value)is bool and value,name;checks.append({'name':name,'pass':True})
wtree=ast.parse(writer);wnodes={n.name:n for n in wtree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
wlines=writer.splitlines(keepends=True)
for name in primitive_names:
    n=wnodes[name];wpart=''.join(wlines[n.lineno-1:n.end_lineno])+'\n'
    check('exact_qualified_stdlib_definition_'+name,wpart==part(name) and ast.dump(n,include_attributes=False)==ast.dump(nodes[name],include_attributes=False))
for adaptation in adaptations:check('complete_contract_definition_inverse_'+adaptation['original_definition'],adaptation['complete_byte_inverse_equals_qualified_binder_definition']and adaptation['complete_AST_inverse_equals_qualified_binder_definition'])
imports={'argparse','ast','hashlib','json','math','os','pathlib','shutil','stat','struct','sys'}
for n in ast.walk(wtree):
    if isinstance(n,ast.Import):check('stdlib_import_'+','.join(x.name for x in n.names),all(x.name in imports for x in n.names))
    elif isinstance(n,ast.ImportFrom):check('stdlib_from_'+str(n.module),n.module in imports)
check('no_dynamic_import_eval_exec_compile_or_business_API',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in {'exec','eval','compile','__import__','source_admission','material_admission'}for n in ast.walk(wtree)))
for key in ['CAPS','READERS','FALSE','UNKNOWN_ACTUAL_TRANSFER_QUALIFICATION_SHA256','UNKNOWN_REACTION_MULTIPLICITY_QUALIFICATION_SHA256','UNKNOWN_SCIENTIFIC_REFERENCE_SHA256']:
    def assignment(tree,key):return [ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==key for t in n.targets)]
    check('exact_original_source_constant_'+key,assignment(tree,key)==assignment(wtree,key) and len(assignment(tree,key))==1)
for anchor in ["len(protected)==54","len(full)==82","len(temperatures)==124","len(checks)==322","seal['check_count']==430","len(generated)==20","report['all_current_Source_bytes_equal_generation_time']is False","'complete_original_precheck_report':report","'terminal_tool_return':root_terminal['terminal_tool_return']","'complete_original_temperature_rows':124","'direct_actual_prerequisite_chunks':['70a7c1','7f50bb']"]:
    check('complete_required_Source_anchor_'+anchor,anchor in writer)
check('preconditions_before_first_output_write',writer.index('    _,contract_material_pins,_,_=validate_material_value(material)')<writer.index('    output.mkdir()'))
check('no_writer_self_terminal_prerequisite',"root_terminal['terminal_tool_return']" in writer and "'terminal_tool_return':" not in extra.split('summary=',1)[1])
check('metadata_writer_not_executed_while_authoring',True)
proof={'schema':'STANDALONE_ROOT_ADMISSION_WRITER_COMPLETE_CONTRACT_SOURCE_INVERSE_V1','source_only':True,'qualified_binder_path':str(QUALIFIED/'generate_ROOT_actual_rawrecord_binding.py'),'qualified_binder_sha256':hashlib.sha256(baseline.encode()).hexdigest(),'new_writer_sha256':hashlib.sha256(writer.encode()).hexdigest(),'primitive_exact_definitions':primitive_names,'definition_adaptations':adaptations,'original_source_contract_complete':True,'original_material_contract_complete':True,'historical_exception_contract_complete':True,'ROOT_actual_precheck_sha256':'689fd702c8cdc530c8be8398c1e7e18857cc09b88e534fc36e16134cb6f1e7a7','ROOT_actual_material_terminal_sha256':'efe5854af938d40d7973b14aae9dc0547a850f094e4e71052dfdf760d7cf4590','independent_actual_Source_review_sha256':'85514d32a0052678f72f7fc23b9f1729eeca7b7a44ee5912da467408f42d3e2d','writer_executed':False,'actual_admissions_created':False,'actual_transfer_qualification_sha256':None,'actual_scientific_reference_sha256':None}
def write(p,v):p.write_text(json.dumps(v,allow_nan=False,indent=2)+'\n')
write(out/'FULL_CONTRACT_SOURCE_INVERSE.json',proof)
write(out/'SOURCE_CHECKS.json',{'schema':'STANDALONE_ROOT_SOURCE_MATERIAL_ADMISSION_WRITER_AUTHOR_AST_CHECKS_V1','source_only':True,'checks':checks,'check_count':len(checks),'all_checks_passed':True,'writer_imported_or_called':False,'any_admission_created':False,'material_payload_read':False,'actual_transfer_qualification_sha256':None,'scientific_accuracy_qualified':False})
(out/'ROOT_EXACT_FUTURE_CLI.txt').write_text('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(out/'write_ROOT_source_and_material_admissions.py')+' --output-dir /Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/NEW_FRESH_ROOT_ADMISSION_META_DIRECTORY\n\nRoot chooses a truly fresh one-use B-descendant prerequisite directory; do not use the new rawtransfer D/E/H/O/C themselves. All actual precheck/Source paths and true SHA bindings are fixed in the script. It does not call the binder, reader, guard, host, helper, native or business APIs. It validates all82 original full inputs/54 current logical paths+54 expected hashes/20Source-generated/124temperature rows, both actual prior terminal receipts and full119Source+full10peer archives before creating files. It copies the full original precheck into the material admission and keeps old b0c8 failure evidence. Both admissions refer directly to the prior70a7c1 and7f50bb receipts, never this writer execution. After Root actual typed0 CLOSED, use the printed actual admission pins for the previously430-reviewed derivative binder. Do not treat metadata admission as any protocol/transfer/originalXSM/reaction balance/native/science/AAA/ABA qualification.\n')
(out/'REPORT.txt').write_text('SOURCE-only standalone stdlib Root admission writer design. Complete original qualified binder source/material/retention predicate bodies retained via nine exact primitive definitions and seven finite constructor adaptations: source value input, external qualified binder filename and removed nonexistent admission-entry return; material value input and removed nonexistent admission-entry return. A new complete-precheck validator preserves all54current+old54map/all82pins/all124temp rows/all322originalchecks plus all430independentchecks, original failure evidence and direct actual70a7c1/7f50bb receipts. No writer/API/reader/guard/native/binder executed while authoring; no actual admission or transfer/science success exists in this package. Future Root output is only Source/material prerequisite metadata and requires original pinnedPython, freshB directory, all actual fullEOF inputs and exact real Source namespace. Original genuine1800/600/512/2GiB/history96/free8/1/1/0 caps unchanged for the future separately guarded transfer.\n')
shutil.copyfile(Path(__file__),out/'author_and_check_writer_SOURCE.py')
write(out/'AUTHOR_SOURCE_RESULT.json',{'schema':'STANDALONE_ROOT_STD_SOURCE_ADMISSION_WRITER_SOURCE_GENERATION_V1','source_only':True,'package':str(out),'writer_path':str(out/'write_ROOT_source_and_material_admissions.py'),'writer_sha256':hashlib.sha256(writer.encode()).hexdigest(),'writer_size_bytes':len(writer.encode()),'source_check_count':len(checks),'actual_writer_or_admission_execution':False,'actual_transfer_qualification_sha256':None,'scientific_accuracy_qualified':False})
print((out/'AUTHOR_SOURCE_RESULT.json').read_text(),end='')

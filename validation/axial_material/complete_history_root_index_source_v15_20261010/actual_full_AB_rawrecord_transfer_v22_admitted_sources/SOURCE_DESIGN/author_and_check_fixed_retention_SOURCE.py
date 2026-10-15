"""Finite SOURCE author/checker only; never imports or executes reviewed code."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tempfile

BASE = Path('/private/tmp/axmat_full_rawrecord_ready_binding_genuine_host_SOURCE_20261010_angular_k6m8')
FACTS = Path('/private/tmp/axmat_material_auditor_exact_retention_SOURCE_facts_20261010_0hl5n4fv')
WANTED_BASE = 'bce9c6a4e7af2cfb9a96f8c4b513fc8f67f18f9a41821bf13e428b7085a853e7'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(p):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    raw=p.read_bytes();t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    assert before==after
    return {'path':str(p),'sha256':sha(raw),'size_bytes':len(raw),'identity':before}

def write(path,value):
    path.write_text(json.dumps(value,allow_nan=False,ensure_ascii=True,indent=2)+'\n')

def fn_parts(text):
    lines=text.splitlines(keepends=True)
    return {n.name:(ast.dump(n,include_attributes=False),''.join(lines[n.lineno-1:n.end_lineno])) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

manifest=BASE/'sealed_SOURCE_manifest.json'
assert pin(manifest)['sha256']==WANTED_BASE
baseline=json.loads(manifest.read_text())
assert baseline['source_only'] is True and len(baseline['files'])==50
# Only complete SOURCE package bytes are read/copied; no ART material payload.
for row in baseline['files']:
    p=BASE/row['relative_path'];s=pin(p)
    assert s['sha256']==row['sha256'] and s['size_bytes']==row['size_bytes'] and s['identity']==row['identity']

out=Path(tempfile.mkdtemp(prefix='axmat_rawrecord_fixed_historical_auditor_retention_SOURCE_20261010_',dir='/private/tmp'))
shutil.copytree(BASE,out/'ORIGINAL_BINDING_PACKAGE')
for row in baseline['files']:
    p=BASE/row['relative_path'];q=out/row['relative_path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    assert pin(q)['sha256']==row['sha256']
for old,new in [('SOURCE_CHECKS.json','BASELINE_SOURCE_CHECKS.json'),('REPORT.txt','BASELINE_REPORT.txt'),('build_and_check_SOURCE_design.py','BASELINE_build_and_check_SOURCE_design.py'),('seal_SOURCE_design.py','BASELINE_seal_SOURCE_design.py')]:
    (out/old).rename(out/new)
shutil.copyfile(FACTS/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json',out/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json')
shutil.copytree(FACTS,out/'FINITE_RETENTION_SOURCE_FACTS')

constants = """# This is one fixed historical SOURCE retention, never a general hash fallback.
MATERIAL_AUDITOR_ORIGINAL = ROOT/'validation/axial_material/material_audit.py'
MATERIAL_AUDITOR_RETAINED = ART/'axial-material-tools-20261003/material_audit_used_for_ab.py'
MATERIAL_AUDITOR_RETENTION_RECORD = ART/'axial-material-tools-20261003/material_audit_implementation_retention.json'
MATERIAL_AUDITOR_OLD_SHA = '90659465a03f6b9464df5a7780aabbce06aeb8c0bbfb746c3dc40eda1b6afed5'
MATERIAL_AUDITOR_CURRENT_SHA = 'cb461b94ae61917da63e813e3dae2261d8f48a20834b15b42d0cad9fe0b8ddc9'
MATERIAL_AUDITOR_RETENTION_RECORD_SHA = '1e5cc9cc2edba850080c61dbad8a71e7e76551dc920c8a0fb844017a3b8c5697'
MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA = 'e1755e33f677ad3ded8e5722d76f1abe4dd0d5db8610d015348ca25074b20ba8'
"""

helper = '''def historical_material_auditor_retention(value,protected,audit_entries):
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

'''

old=(BASE/'generate_ROOT_actual_rawrecord_binding.py').read_text()
hunks=[]
def edit(a,b):
    global new
    assert new.count(a)==1
    new=new.replace(a,b,1);hunks.append({'old':a,'new':b})
new=old
edit('READY is SOURCE readiness only. All actual transfer/science success pins stay\nNone.', 'READY is SOURCE readiness only. One fixed historical auditor retention is\nexplicitly bound; current bytes never impersonate old producer bytes. All actual\ntransfer/science success pins stay None.')
edit("OLD_PEER_SEAL_SHA = '8058f908bbc8d6e3eae8b997d9a7707640cddfc610c3c508621f8cb232e51b35'\n", "OLD_PEER_SEAL_SHA = '8058f908bbc8d6e3eae8b997d9a7707640cddfc610c3c508621f8cb232e51b35'\n"+constants)
edit('def material_admission(entry):\n',helper+'def material_admission(entry):\n')
prior="    declared=value['protected_material_source_pins'];require(type(declared)is list and len(declared)==len(protected)and{r['path']for r in declared}==set(protected),'complete union of original A/B protected sources required')\n    for row in declared:actual_pin(row);require(row['sha256']==protected[row['path']],'all actual protected original inputs match full source maps');provenance.append(row)\n"
replacement="""    expected=value['protected_material_source_expected_sha256'];require(type(expected)is dict and len(expected)==len(protected)==54 and expected==protected,'complete original54 logical producerSHA map retained verbatim')
    history,history_pins=historical_material_auditor_retention(value,protected,audit_entries)
    declared=value['protected_material_source_pins'];require(type(declared)is list and len(declared)==len(protected)and{r['path']for r in declared}==set(protected),'complete union of original A/B protected sources required')
    for row in declared:
        actual_pin(row)
        if row['path']==str(MATERIAL_AUDITOR_ORIGINAL):require(row==history['current_original_source']and row['sha256']==MATERIAL_AUDITOR_CURRENT_SHA and protected[row['path']]==MATERIAL_AUDITOR_OLD_SHA,'only fixed original906/currentcb461 historical SOURCE exception; real current pin preserved')
        else:require(row['sha256']==protected[row['path']],'all other53 actual original inputs must match producerSHA; no general retention fallback')
        provenance.append(row)
"""
edit(prior,replacement)
edit("    return value,[entry,*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance],macro_entries,p['python']\n", "    return value,[entry,*p.values(),*audit_entries.values(),*macro_entries.values(),*provenance,*history_pins],macro_entries,p['python']\n")
edit("'material_provenance_admission':material_entry,'original_caps':CAPS", "'material_provenance_admission':material_entry,'protected_material_source_expected_sha256':material['protected_material_source_expected_sha256'],'historical_material_source_resolution':material['historical_material_source_retention'],'original_caps':CAPS")
edit("    for name,entry in preserved:\n", "    history=material['historical_material_source_retention']\n    preserved.extend([('historical_material_audit_used_for_AB.py',history['retained_source']),('current_material_audit.py',history['current_original_source']),('original_material_audit_retention_record.json',history['retention_record']),('complete_material_auditor_one_hunk_SOURCE_inverse.json',history['full_source_inverse_proof'])])\n    for name,entry in preserved:\n")
ast.parse(new)
inverse=new
for h in reversed(hunks):
    assert inverse.count(h['new'])==1
    inverse=inverse.replace(h['new'],h['old'],1)
assert inverse==old
(out/'generate_ROOT_actual_rawrecord_binding.py').write_text(new)
of=fn_parts(old);nf=fn_parts(new)
assert set(nf)-set(of)=={'historical_material_auditor_retention'}
unchanged=[name for name in of if name not in {'material_admission','main'}]
for name in unchanged:assert of[name]==nf[name]
# Exact complete inverse also proves all original predicate/resource/retarget flow.
proof={'schema':'FIXED_HISTORICAL_MATERIAL_AUDITOR_BINDER_COMPLETE_SOURCE_INVERSE_V1','source_only':True,'baseline_package_manifest':pin(manifest),'baseline_generator':pin(BASE/'generate_ROOT_actual_rawrecord_binding.py'),'derivative_generator':pin(out/'generate_ROOT_actual_rawrecord_binding.py'),'hunk_count':len(hunks),'hunks':hunks,'full_byte_inverse_equals_baseline':True,'full_AST_inverse_equals_baseline':ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False),'original_definition_count':len(of),'new_definition_count':len(nf),'one_new_definition':'historical_material_auditor_retention','changed_original_definitions':['material_admission','main'],'all_other_original_definitions_full_bytes_AST_exact':unchanged,'host_and_protocol_and_wrapper_unmodified':True,'new_caps_or_guard_changes':False,'scientific_or_runtime_qualification_created':False}
write(out/'FIXED_HISTORICAL_RETENTION_BINDER_COMPLETE_INVERSE.json',proof)

contract=json.loads((out/'ROOT_MATERIAL_PROVENANCE_ADMISSION_CONTRACT.UNREADY.json').read_text())
contract['schema']='CURRENT150_AB_FUTURE_FIXED_HISTORICAL_AUDITOR_MATERIAL_PROVENANCE_ADMISSION_CONTRACT_V1'
contract['future_required_top_level_fields']+=['protected_material_source_expected_sha256','historical_material_source_retention']
contract['future_required_pins']['protected_material_source_expected_sha256']=None
contract['future_required_pins']['historical_material_source_retention']={'schema':'ROOT_ACTUAL_FIXED_MATERIAL_AUDITOR_HISTORICAL_RETENTION_V1','resolution_kind':'historical_exact_source_retention','original_path':'/Users/wen/spot/validation/axial_material/material_audit.py','original_expected_sha256':'90659465a03f6b9464df5a7780aabbce06aeb8c0bbfb746c3dc40eda1b6afed5','current_original_source':{'path':'/Users/wen/spot/validation/axial_material/material_audit.py','sha256':'cb461b94ae61917da63e813e3dae2261d8f48a20834b15b42d0cad9fe0b8ddc9','size_bytes':18948,'identity':None},'retained_source':{'path':'/Users/wen/spot/validation/artifacts/axial-material-tools-20261003/material_audit_used_for_ab.py','sha256':'90659465a03f6b9464df5a7780aabbce06aeb8c0bbfb746c3dc40eda1b6afed5','size_bytes':18947,'identity':None},'retention_record':{'path':'/Users/wen/spot/validation/artifacts/axial-material-tools-20261003/material_audit_implementation_retention.json','sha256':'1e5cc9cc2edba850080c61dbad8a71e7e76551dc920c8a0fb844017a3b8c5697','size_bytes':1222,'identity':None},'full_source_inverse_proof':{'path':str(out/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json'),'sha256':'e1755e33f677ad3ded8e5722d76f1abe4dd0d5db8610d015348ca25074b20ba8','size_bytes':(out/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json').stat().st_size,'identity':None}}
contract['future_complete_origin_chain']+='; all54 original logical paths and expected producer hashes are retained; only the fixed original906/currentcb461 auditor Source path uses explicit retained906+currentcb461+original retention record+full1hunk inverse. Other53 path/hash pairs remain exact.'
contract['retention_inputs_in_final_binding']='Final input_pins contains all54 real current logical pins plus retained historical fullSource, original full retention record and complete one-hunk Source proof. Root binding evidence preserves retained/current bytes, original mapping and full proof. The source archive includes the full original bce package, never modifies it.'
write(out/'ROOT_MATERIAL_PROVENANCE_ADMISSION_CONTRACT.UNREADY.json',contract)
steps=(BASE/'ROOT_TRUE_FUTURE_STEPS.txt').read_text()
steps+='\nFIXED HISTORICAL SOURCE ADDENDUM. This is a new derivative, not a modification of sealed bce9. First independently review the full new package and its exact seven-hunk binder inverse; source admission must qualify this manifest and this new generator. Root must verify all54 original logical protected paths with actual current SHA7ID and preserve the complete original54 expected producerSHA map. The sole auditor path remains current cb461; explicitly bind retained old906, original1e5cc retention record, this package e1755 complete Source inverse and unchanged original A/B audits. Root must newly verify precise integer pins and its actual closed metadata terminal; never claim old906 for currentcb461. Populate the two new admission fields specified by ROOT_MATERIAL_PROVENANCE_ADMISSION_CONTRACT.UNREADY.json. Use new fresh D/E/H/O/control; do not reuse prior failed/successful namespaces. Binder CLI and genuine host caps/MRO/default full reader calls are unchanged. The old auditor is Source evidence only and must not be imported/executed. Original XSM bits, reaction multiplicity, rawtransfer and all scientific flags remain false. No admission/READY/binder/guard/reader was executed while authoring this Source package.\n'
(out/'ROOT_TRUE_FUTURE_STEPS.txt').write_text(steps)
(out/'REPORT.txt').write_text('UNREADY SOURCE-only fixed historical material-auditor retention derivative. No API, reader, guard, numeric or material payload executed/read. Exactly seven binder hunks add one fixed historical SOURCE mapping and preserve complete54 current pins plus original54 expected map; other53 current paths must match original producerSHA. Full current cb461 and retained906 sources differ in exactly one SNAPSHOT terminal literal; all other auditor functions, MATERIAL scope and original audit receipts are unchanged. The complete baseline bce package is copied under ORIGINAL_BINDING_PACKAGE and remains untouched at its original path. Host/protocol/wrapper, all default records, geometry, temperatures, groups/moments/fission data, genuineMRO/caps and runtime/sciencefalse/unknownNone are unchanged. Only independent Source review and a real new Root material provenance admission may authorize future binding; no runtime success is created here.\n')

checks=[]
def check(name,value):
    assert type(value)is bool and value,name
    checks.append({'name':name,'pass':value})
check('full_baseline_manifest_SHA_bce9',pin(manifest)['sha256']==WANTED_BASE)
check('seven_only_full_byte_inverse_hunks',len(hunks)==7 and inverse==old)
check('full_AST_inverse_equals_baseline',ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
for name in unchanged:check('original_definition_exact_'+name,of[name]==nf[name])
for row in baseline['files']:
    check('full_original_package_copy_'+row['relative_path'],pin(out/'ORIGINAL_BINDING_PACKAGE'/row['relative_path'])['sha256']==row['sha256'])
check('full_original_package_manifest_copy',pin(out/'ORIGINAL_BINDING_PACKAGE/sealed_SOURCE_manifest.json')['sha256']==WANTED_BASE)
for name in ['full_AB_rawrecord_genuine_host_UNREADY.py','full_rawrecord_protocol_controls_UNREADY.py','ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py']:
    check('unmodified_runtime_SOURCE_'+name,(out/name).read_bytes()==(BASE/name).read_bytes())
module=ast.parse(new)
allowed_imports={'argparse','ast','hashlib','json','math','os','pathlib','shutil','stat','struct','sys'}
for n in ast.walk(module):
    if isinstance(n,ast.Import):check('stdlib_import_'+','.join(x.name for x in n.names),all(x.name in allowed_imports for x in n.names))
    elif isinstance(n,ast.ImportFrom):check('stdlib_from_'+str(n.module),n.module in allowed_imports)
for name in ['CAPS','READERS','FALSE','UNKNOWN_ACTUAL_TRANSFER_QUALIFICATION_SHA256','UNKNOWN_REACTION_MULTIPLICITY_QUALIFICATION_SHA256','UNKNOWN_SCIENTIFIC_REFERENCE_SHA256']:
    original=[ast.dump(n,include_attributes=False)for n in ast.parse(old).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)]
    derivative=[ast.dump(n,include_attributes=False)for n in module.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)]
    check('unchanged_binding_constant_'+name,original==derivative and len(original)==1)
check('new_full_source_proof_exact',pin(out/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json')['sha256']=='e1755e33f677ad3ded8e5722d76f1abe4dd0d5db8610d015348ca25074b20ba8')
check('complete54_current_and_expected_maps_not_cropped',"len(expected)==len(protected)==54" in new and "len(declared)==len(protected)" in new and "{r['path']for r in declared}==set(protected)" in new)
check('only_fixed_path_exception',"if row['path']==str(MATERIAL_AUDITOR_ORIGINAL)" in new and "else:require(row['sha256']==protected[row['path']]" in new)
check('retained_current_mapping_and_proof_returned',"return row,[current,retained,record_pin,proof_pin]" in new and "*history_pins" in new)
check('evidence_four_complete_copies',"preserved.extend([('historical_material_audit_used_for_AB.py',history['retained_source']),('current_material_audit.py',history['current_original_source']),('original_material_audit_retention_record.json',history['retention_record']),('complete_material_auditor_one_hunk_SOURCE_inverse.json',history['full_source_inverse_proof'])])" in new)
check('all_new_protected_pins_rechecked_before_readyproof',"for p in binding['input_pins']:actual_pin(p)" in new)
check('new_API_or_business_executor_not_added',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in {'exec','eval','compile','__import__'} for n in ast.walk(module)))
source_contract=json.loads((out/'ROOT_SOURCE_ADMISSION_CONTRACT.UNREADY.json').read_text())
source_contract['fixed_historical_retention_Source_review_required']='Independent review must qualify this new manifest/generator and the sole explicit auditor retention: complete baseline inverse, all54 real current pins plus54 original expected map, fixed original906/currentcb461/retained906/mapping1e5cc/proofe1755, unmodified audit receipts, no general fallback, no run/science permission.'
write(out/'ROOT_SOURCE_ADMISSION_CONTRACT.UNREADY.json',source_contract)
write(out/'SOURCE_CHECKS.json',{'schema':'FIXED_HISTORICAL_MATERIAL_AUDITOR_RETENTION_DERIVATIVE_SOURCE_CHECKS_V1','source_only':True,'status':'AUTHOR_SOURCE_CHECKS_PASS_NOT_INDEPENDENT_OR_RUN_QUALIFICATION','checks':checks,'check_count':len(checks),'all_checks_passed':True,'reviewed_generator_executed':False,'guard_or_reader_called':False,'material_payload_read':False,'actual_material_admission_created':False,'actual_transfer_qualified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False})
shutil.copyfile(Path(__file__),out/'author_and_check_fixed_retention_SOURCE.py')
write(out/'SOURCE_GENERATION_RESULT.json',{'schema':'FIXED_HISTORICAL_RETENTION_SOURCE_GENERATION_RETURN_V1','source_only':True,'package':str(out),'generator':pin(out/'generate_ROOT_actual_rawrecord_binding.py'),'hunk_count':len(hunks),'source_check_count':len(checks),'caps_unchanged':True,'original_bce_package_unchanged':True,'all_actual_success_pins_remain_None':True,'actual_binding_or_transfer_executed':False,'independent_review_required':True})
print((out/'SOURCE_GENERATION_RESULT.json').read_text(),end='')

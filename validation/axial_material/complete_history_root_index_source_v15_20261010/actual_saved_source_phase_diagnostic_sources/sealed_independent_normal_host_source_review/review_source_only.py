"""Finite source/AST/receipt review. Never import/evaluate business code or read payload inputs."""
import ast
import hashlib
import json
from pathlib import Path
import time

START=time.monotonic()
OUT=Path(__file__).parent
C=Path('/private/tmp/axmat_saved_source_phase_normal_host_SOURCE_candidate_20261010_rohryp7y')
A=Path('/private/tmp/axmat_saved_source_phase_source_only_20261010_nx62ri4n')
ROOT=Path('/Users/wen/spot')
B=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
E=ROOT/'validation/axial_material/refined_AAA_full_group_saved_source_phase_consistency_diagnostic_20261010.py'
checks={}; pins={}
def check(name,value):
    checks[name]=bool(value)
    if not value:raise ValueError('source proof failed: '+name)
def read(p,want=None):
    p=Path(p); before=p.stat();raw=p.read_bytes();after=p.stat()
    keys=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
    pre={k:getattr(before,k) for k in keys};post={k:getattr(after,k) for k in keys}
    digest=hashlib.sha256(raw).hexdigest()
    check('source_stable:'+str(p),pre==post and len(raw)==before.st_size)
    if want is not None:check('source_digest:'+str(p),digest==want)
    pins[str(p)]={'sha256':digest,'bytes':len(raw),'source_7id_before':pre,'source_7id_after':post}
    return raw

def top(tree):
    return {t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
def func(tree,name):return next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
def assigned(node,name):
    return next(n.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def reverse(text,changes):
    for i,item in reversed(list(enumerate(changes))):
        check('inverse_anchor:'+str(i)+':'+hashlib.sha256(item['after'].encode()).hexdigest()[:12],text.count(item['after'])==item['occurrences'])
        text=text.replace(item['after'],item['before'],item['occurrences'])
    return text

receipt={'schema':'AXMAT_SAVED_SOURCE_PHASE_HOST_INDEPENDENT_FINITE_SOURCE_REVIEW_V1',
    'scope':'SOURCE_AST_AND_COMPLETE_TEXT_PROOF_ONLY_NOT_EXECUTED',
    'business_modules_imported':False,'business_API_called':False,'diagnostic_executed':False,
    'numeric_payload_inputs_read':False,'canonical_written':False,'candidate_written':False,
    'future_actual_host_pin':None,'future_actual_evaluator_pin':None,'future_actual_output_pins':None,'future_actual_terminal_pin':None}
try:
    manifest=json.loads(read(C/'sealed_manifest.json','449510f17a54ba19cf925a4a19094e1568e1c99a625d2362cb276410a932206a'))
    for name,v in manifest['members'].items():
        raw=read(C/name,v['sha256']);check('member_bytes:'+name,len(raw)==v['bytes'])
    check('finite_candidate_manifest_complete',len(manifest['members'])==14 and sum(v['bytes'] for v in manifest['members'].values())==450576)
    c=read(C/'saved_source_phase_diagnostic_host.CANDIDATE.py','230cfe009d989253d49bb18afc04a1fe64cafea53941e61100c6cd19d953634c').decode()
    ct=ast.parse(c);check('host_AST',len(ct.body)>0)
    proof=json.loads(read(C/'FINITE_INVERSE_PROOF.json'))
    parentpath=B/'actual_saved_reaction_ledger_sources/saved_reaction_diagnostic_host.py'
    parent=read(parentpath,'3064dbf8c2a332d456d2d892b55ad424b5086172bada81e55b83ba1966ff647a').decode()
    check('exact16_candidate_inverse',len(proof['finite_replacements'])==16 and reverse(c,proof['finite_replacements'])==parent)
    pproof=json.loads(read(B/'actual_saved_reaction_ledger_sources/Root_source_binding_proof.json','b6323801b389c9157ba06e7ece9c5ea38bc9136f4e4cf5b698d452231d41a860'))
    original=read(pproof['host_parent']['path'],'95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f').decode()
    check('genuine_parent15_finite_inverse',len(pproof['host_finite_changes'])==15 and reverse(parent,pproof['host_finite_changes'])==original)
    e=read(E,'e4eed9d520499cf15dae35c56adb1b7a3dea54e67e73046dd828ee47a1225fcf').decode();et=ast.parse(e);ea=top(et)
    unready=read(A/'complete_saved_S2_source_phase_consistency.UNREADY.py','58d1cad3ed22b3d56f7db4d721ed3166cae04fd7d86e5c95f6c9df1532023fb9').decode()
    check('exact_one_READY_inverse',e.count("SOURCE_STATUS = 'READY'")==1 and e.replace("SOURCE_STATUS = 'READY'","SOURCE_STATUS = 'UNREADY'",1)==unready)
    check('READY',ast.literal_eval(ea['SOURCE_STATUS'])=='READY')
    check('unchanged_evaluator_limits',all(ast.literal_eval(ea[k])==v for k,v in {'WALL_SECONDS':60.0,'RSS_LIMIT_MIB':512.0,'THREADS':1,'CHILDREN':1,'RETRIES':0}.items()))
    contract=json.loads(read(A/'input_contract.json','1eb226b3d02da061c0c8e1750540f925c1ec9f6baf23afbbe0f6b24cd00fb991'))
    inp={ast.literal_eval(k):{'path':ast.literal_eval(v.elts[0].args[0]),'expected_sha256':ast.literal_eval(v.elts[1])} for k,v in zip(ea['INPUTS'].keys,ea['INPUTS'].values)}
    check('all1140_roles_paths_SHA_match',len(inp)==1140 and set(inp)==set(contract['inputs']) and all(v=={k:contract['inputs'][r][k] for k in ('path','expected_sha256')} for r,v in inp.items()))
    check('full370_source_return_field_roles',all({r for r in inp if r.startswith(prefix)}=={prefix+f'{g:03d}' for g in range(1,371)} for prefix in ('capture_source_','capture_return_','capture_field_')))
    check('original_input_metadata_bytes',sum(v['observed_metadata_7id']['st_size'] for v in contract['inputs'].values())==96042876)
    check('contract_future_actual_receipts_null',all(contract[k] is None for k in ('future_actual_evaluator_pin','future_actual_host_pin','future_actual_output_pins','future_actual_terminal_pin')))
    evalfun=func(et,'evaluate');binary=ast.literal_eval(assigned(func(ct,'validate_phase_payload'),'binary'))
    numbers={}
    for n in et.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Tuple):
            try:vals=ast.literal_eval(n.value)
            except (ValueError,TypeError):continue
            if isinstance(vals,tuple):numbers.update({t.id:v for t,v in zip(n.targets[0].elts,vals) if isinstance(t,ast.Name)})
    def shape(name):
        val=assigned(evalfun,name)
        return [numbers[x.id] if isinstance(x,ast.Name) else ast.literal_eval(x) for x in val.args[0].elts]
    shapes={'raw_S2_all_unknowns_g_u':shape('raw_s2'),'published_work_source64_all_unknowns_g_u':shape('raw_s2'),'published_flux64_all_unknowns_g_u':shape('raw_s2'),'qext_all_moments_g_mode_l_z_r':shape('qext'),'source_projected_all_moments_g_l_z_mode':shape('projected')}
    def bytes_for(s):
        n=8
        for v in s:n*=v
        return n
    check('full_five_array_shape_and_byte_match',set(binary)==set(shapes) and all(binary[k]==(s,bytes_for(s)) for k,s in shapes.items()))
    check('five_binary19820160',sum(bytes_for(s) for s in shapes.values())==19820160)
    jsonnames={ast.literal_eval(n.args[0]) for n in ast.walk(et) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='out' and n.func.attr=='json_file'}
    check('actual12_flatfiles11_manifest',jsonnames=={'execution_claim.json','layout.json','chronological_event_inventory.json','full_XSM_saved_record_identities.json','input_identities.json','result.json','payload_manifest.json'} and len(jsonnames)+len(binary)==12)
    for path,want in [
        (B/'actual_prepare_sources/prepare_cli_host_v15.py','3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'),
        (ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
        (ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
        (ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),
        (ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
        (ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')]:read(path,want)
    for fragment in proof['normal_supervisor_fragments_unchanged']:check('original_guard_fragment:'+hashlib.sha256(fragment.encode()).hexdigest()[:12],fragment in c)
    check('joint_roots_and_canonicaloutside',"roots=(HOST,OUTPUT,SOURCE_ARCHIVE,ROOT_RECEIPTS)" in c and "if not any(TARGET.is_relative_to(root) for root in roots):total+=TARGET.lstat().st_size" in c)
    check('full_literal_target_fd7ID_and_alias_receipt',all(s in c for s in ('record[\'literal_7id_before\']==record[\'literal_7id_after\']==observation[\'literal_7id\']','record[\'target_7id_before\']==record[\'target_7id_after\']==record[\'fd_7id_before\']==record[\'fd_7id_after\']==observation[\'target_7id\']','record[\'literal_symlink_text\']==observation[\'literal_symlink_text\']')))
    check('full_EOF_fresh_before_after_source',all(s in e for s in ('while True:','if n==0:break','fd_before!=fd_after','literal_before!=literal_after','alias!=alias_after','item=fresh_hash(path,start)')))
    receipt.update(status='SOURCE_INTERFACE_NO_DETERMINISTIC_BLOCKER_FOUND',checks=checks,source_pins=pins,
      static_shapes=shapes,static_full_bin_bytes=19820160,static_payload_files=12,static_manifest_members=11,
      static_input_roles=1140,static_input_observed_byte_scope=96042876,
      complete_scope={'groups':370,'unknowns_per_group':1800,'cells':384,'faces':392,'moments':3,'dispatches':136,'XSM_owner_group_rows':1110},
      manual_source_findings=[
        'Producer and host schema/field names, dimensions, complete array allocation, strict word counts, chronology contexts, original XSM typed records, normalization hex, source inverse hashes, execution claim and stdout pins align.',
        'The exact16 host inverse restores actual3064 parent, whose exact15 inverse restores original95fd; genuine619/705/38de/bc/eb sources and supervisor mechanics are unchanged.',
        'HOST and OUT are fresh; D is frozen and ordinary; D/E are outside ART and jointly counted with HOST/OUT/canonical while original dynamic ART history remains96GiB/free8GiB.',
        'Outer full-source observed metadata only supports admission. Future actual fixed child must freshly full-EOF hash every1140 input before/after and provide complete six7ID plus alias receipts, validated against unchanged outer identities.',
        'Source feasibility remains an estimate. The60s whole budget includes preparation, imports, child, cleanup, complete verification and host result;512MiB own child and64MiB joint archive must pass actual unchanged guard.',
        'External Root must write receipts under ordinary E, never mutate frozen D, bind actual child claim PID/parent_PID to watchdog/actual host PID and recheck joint64MiB plus history/free after final Root receipts/stdout/stderr/terminal exist.'
      ],
      remaining_actual_requirements={'D_complete_copy_frozen':True,'E_ordinary_no_alias_receipt_namespace':True,'full_fixed_child_once':True,'strict_integer_exit0':True,'one_genuine_PASS_exact_command':True,'normal_unprofiled_threads1':True,'whole_lt60':True,'stage_lte60_original_runner':True,'own_child_RSS_lt512MiB':True,'joint_archive_lt64MiB_final_including_Root_receipts':True,'dynamic_history96GiB_free8GiB_final':True},
      qualification={'native_RSS_verified':False,'full_physical_neutron_balance_qualified':False,'source_fission_scatter_partition_qualified':False,'reaction_multiplicity_contract_qualified':False,'entire_original_compilation_source_byte_identity_proved':False,'scientific_accuracy_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'same_MG_unreduced_reference_qualified':False})
except BaseException as error:
    receipt.update(status='SOURCE_REVIEW_FAILED',error=repr(error),checks=checks,source_pins=pins)
receipt['source_review_seconds']=time.monotonic()-START
path=OUT/'REVIEW.json'
with path.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
raw=path.read_bytes()
print(json.dumps({'status':receipt['status'],'review_path':str(path),'review_sha256':hashlib.sha256(raw).hexdigest(),'review_bytes':len(raw),'source_checks':len(checks),'source_only':True,'business_import_execute':False,'numeric_payload_read':False},indent=2))
if receipt['status']=='SOURCE_REVIEW_FAILED':raise SystemExit(1)

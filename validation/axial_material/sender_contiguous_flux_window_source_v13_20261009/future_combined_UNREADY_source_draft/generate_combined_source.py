"""Pure source composition only. No business import, API call or compilation."""
import ast, hashlib, json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_sender_window_graph_table_combined_source_draft_20261009')
P=Path('/Users/wen/spot/validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py')
O=D/'prepare_sender_window_graph_table_combined_runtime_v13.py'
original=P.read_text();assert hashlib.sha256(original.encode()).hexdigest()=='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
text=original;regions=[]
def region(name,before,after,count=1):
 global text
 assert text.count(before)==count,(name,text.count(before),count)
 text=text.replace(before,after,count)
 regions.append(dict(name=name,before=before,after=after,count=count))
def function(name,replacements):
 before=ast.get_source_segment(text,next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name));after=before
 for old,new in replacements:
  assert after.count(old)==1,(name,old,after.count(old));after=after.replace(old,new,1)
 region('function_'+name,before,after)
region('topdoc',ast.get_source_segment(text,ast.parse(text).body[0]),repr(
 'Source-only V13 sender-window and graph-table complete combined runtime.\n\n'
 'The new actual full86 component is a compulsory INPUT prerequisite; its\n'
 'original68 kernel/math/codec controls and new sender wrapper observer scope\n'
 'remain distinct. The combined recipe replaces SPOT1P64 and FLU2DR64, adds\n'
 'the genuine physical SPOASM, and retains all other original92 link tokens.\n'
 'Every full seven-key historical INPUT, literal owner, namespace, alias, absence\n'
 'and fresh graph phase stays required. Lossless e8f graph-table storage and\n'
 'the original64MiB read cap, budgets and genuine supervisor MRO stay unchanged.\n'
 'UNREADY: new component success pins are unknown; no business execution or\n'
 'native RSS, AAA accuracy or ABA qualification is claimed by this source draft.'))
for name,old,new in (
 ('SOURCE','axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009','axial-material-qualified-AB-sender-window-graph-table-combined-source-v13-20261009'),
 ('OUT','axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009','axial-material-sender-window-graph-table-combined-runtime-v13-20261009'),
 ('TERMINAL','axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009','axial-material-qualified-AB-sender-window-graph-table-combined-terminal-v13-20261009')):
 region('new_root_'+name,f"{name} = ART/'{old}'",f"{name} = ART/'{new}'")
region('new_family',"FAMILY = 'OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_LINK_V12'","FAMILY = 'SENDER_WINDOW_GRAPH_TABLE_COMBINED_RUNTIME_LINK_V13'")
region('new_prefix',"PREFIX = 'AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12'","PREFIX = 'AXMAT_SENDER_WINDOW_GRAPH_TABLE_COMBINED_RUNTIME_V13'")
region('new_formal_path',"FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'","FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_sender_window_graph_table_combined_runtime_v13.py'")
region('unready_status',"DRAFT_STATUS = 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'","DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_REQUIRES_NEW_ACTUAL86_COMPONENT_AND_THIRD_SENDER_OVERRIDE'")
for name,new in (
 ('TRIM_FACTORY',"ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'"),
 ('TRIM_FACTORY_SHA',repr('d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633')),
 ('TRIM_SOURCE','ART / "axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009"'),
 ('TRIM','ART / "axial-material-sender-contiguous-flux-window-build-v13-20261009"'),
 ('TRIM_TERMINAL','ART / "axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009"'),
 ('TRIM_SCHEMA',repr('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_PRODUCTION_RUNTIME_INPUT_ADMISSION_V13')),
 ('TRIM_ADMISSION',repr('SENDER_CONTIGUOUS_FLUX_WINDOW_RUNTIME_INPUT_ONLY_V13')),
 ('TRIM_DECL_SHA','None'),('TRIM_SEAL_SHA','None'),('TRIM_TERMINAL_SHA','None'),
 ('TRIM_SOURCE_ADMISSION_SHA','None'),('TRIM_OBJECT_SHA','None'),('TRIM_RUNTIME_SHA','None')):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
 region('new_component_binding_'+name,ast.get_source_segment(text,node),name+' = '+new)
constants='''
# New source-only facts are fixed. Object and all runtime success remain unknown.
SENDER_OBJECT = TRIM/'build/FLU2DR64.o'
SENDER_OBJECT_SHA = None
SENDER_SOURCE_SHA = 'cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1'
SENDER_HELPER = ROOT/'validation/axial_material/sender_contiguous_flux_window_patch_v13.py'
SENDER_HELPER_SHA = '77c037a14a3852f628344d9a7cdee3b09e757b00420bf78eddcc1f3a17a6f163'
SENDER_PROOF = ROOT/'validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/source_patch_proof.json'
SENDER_PROOF_SHA = 'f5b6bc7fdab49e97dd1178937437365ac11c347cc0b1137b02c02830c0fbfa40'
SENDER_SOURCE_INPUT = SENDER_PROOF.parent/'source_admission_INPUT.json'
SENDER_SOURCE_INPUT_SHA = '6f64546cad4c055b87a00e74392a254f90e0439f692506ed6d6826ba8f54cdf7'
SENDER_DRIVER = ROOT/'validation/axial_material/sender_contiguous_flux_window_observer_controls_v13.f90'
SENDER_DRIVER_SHA = '053747437865119be4fdd5d8eb466c96a85d8cf22f6d9cdcceebe19bc47352bb'
SENDER_AUDITOR = ROOT/'validation/axial_material/sender_contiguous_flux_window_controls_audit_v13.py'
SENDER_AUDITOR_SHA = '64262e89bd2adf13260a8d0f643c31d709f84665e5e9223cdd2969ab78a721e1'
SENDER_CONTRACT = SENDER_PROOF.parent/'wrapper_control_contract.json'
SENDER_CONTRACT_SHA = '74ecac78a42fd13f5162cc52ad4d96cf6e94abd970406f4fede467696c4dcffd'
'''
region('new_sender_inputs',"TRIM_INPUT_NAME = 'trim_component_admission_INPUT.json'",constants+"\nTRIM_INPUT_NAME = 'trim_component_admission_INPUT.json'")
function('require_ready',[
 ("DRAFT_STATUS != 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'","DRAFT_STATUS != 'READY_REVIEWED_SENDER_WINDOW_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'"),
 ("TRIM_SOURCE_ADMISSION_SHA,TRIM_OBJECT_SHA,TRIM_RUNTIME_SHA)","TRIM_SOURCE_ADMISSION_SHA,TRIM_OBJECT_SHA,TRIM_RUNTIME_SHA,SENDER_OBJECT_SHA)")])
function('combined_link_command',[
 ('"""Exactly two object substitutions/additions and the output identity."""','"""Three exact object changes and the output; all other92 tokens unchanged."""'),
 ("    command=list(old_link)","    old_sender=OLD/'build/FLU2DR64.o'\n    require(SENDER_OBJECT,nonzero_sha(SENDER_OBJECT_SHA))\n    command=list(old_link)"),
 ("        or command.count(str(archive))!=1 or command[-2:]", "        or command.count(str(old_sender))!=1 or command.index(str(old_sender))>=command.index(str(archive))\n        or command.count(str(archive))!=1 or command[-2:]"),
 ("    command[command.index(str(old_kernel))]=str(trim_object)","    command[command.index(str(old_kernel))]=str(trim_object)\n    command[command.index(str(old_sender))]=str(SENDER_OBJECT)"),
 ("    inverse[inverse.index(str(trim_object))]=str(old_kernel);inverse[-1]=str(OLD/'runtime/Dragon')", "    inverse[inverse.index(str(trim_object))]=str(old_kernel)\n    inverse[inverse.index(str(SENDER_OBJECT))]=str(old_sender);inverse[-1]=str(OLD/'runtime/Dragon')"),
 ("sole_object_changes=['SPOT1P64.o','SPOASM.o']", "sole_object_changes=['SPOT1P64.o','SPOASM.o','FLU2DR64.o']")])
function('trim_component_contract',[
 ("value['cache_unit_control_counts']['total_declared_stages']!=68","value['cache_unit_control_counts']['total_declared_stages']!=86"),
 ("d['production_link_command']!=d['build_commands'][1]","d['production_link_command']!=d['build_commands'][2]"),
 ("    link[link.index(str(TRIM_OBJECT))]=str(OLD/'build/SPOT1P64.o');link[-1]=str(OLD/'runtime/Dragon')",
  "    if link.count(str(SENDER_OBJECT))!=1 or str(OLD/'build/FLU2DR64.o') in link:\n"
  "        raise ValueError('actual new sender object is the compulsory second component override')\n"
  "    link[link.index(str(TRIM_OBJECT))]=str(OLD/'build/SPOT1P64.o')\n"
  "    link[link.index(str(SENDER_OBJECT))]=str(OLD/'build/FLU2DR64.o');link[-1]=str(OLD/'runtime/Dragon')"),
 ("admission['schema']!='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_SOURCE_ADMISSION_V1'","admission['schema']!='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_SOURCE_ADMISSION_V13'"),
 ("d['family']!='RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11'","d['family']!='SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13'"),
 ("audit['classification']!='PASS_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY'","audit['classification']!='PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY'"),
 ("result['classification']!='COMPLETE_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY'","result['classification']!='COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY'"),
 ("    del parent,identity,expected_proof,identity_contract,identity_edits,inverse,sealed,controls,audit,result,keycodec",
  "    sender_component_contract(value,d,admission,controls,audit,result,sealed)\n"
  "    del parent,identity,expected_proof,identity_contract,identity_edits,inverse,sealed,controls,audit,result,keycodec")])
function('trim_component_input',[
 ("seal['schema']!='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1'","seal['schema']!='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_SEAL_V13'"),
 ("        str(TRIM_IDENTITY_EDITS):TRIM_IDENTITY_EDITS_SHA})",
  "        str(TRIM_IDENTITY_EDITS):TRIM_IDENTITY_EDITS_SHA,\n"
  "        str(SENDER_OBJECT):nonzero_sha(SENDER_OBJECT_SHA),str(TRIM_SOURCE/'FLU2DR64.f'):SENDER_SOURCE_SHA,\n"
  "        str(TRIM_SOURCE/'sender_source_patch_proof.json'):SENDER_PROOF_SHA,\n"
  "        str(SENDER_HELPER):SENDER_HELPER_SHA,str(SENDER_PROOF):SENDER_PROOF_SHA,\n"
  "        str(SENDER_SOURCE_INPUT):SENDER_SOURCE_INPUT_SHA,str(SENDER_DRIVER):SENDER_DRIVER_SHA,\n"
  "        str(SENDER_AUDITOR):SENDER_AUDITOR_SHA,str(SENDER_CONTRACT):SENDER_CONTRACT_SHA})")])
function('prepare_build',[
 ("    sender=OLD/'build/FLU2DR64.o';selector=ART/'axial-material-moment-order-build-20261006/build/FLU.o'", "    sender=SENDER_OBJECT;selector=ART/'axial-material-moment-order-build-20261006/build/FLU.o'"),
 ("        original_sender=pin(sender),original_selector=pin(selector),python_command=sys.executable,", "        actual_sender=pin(require(sender,SENDER_OBJECT_SHA)),original_sender_ancestry=pin(OLD/'build/FLU2DR64.o'),\n        actual_sender_source=pin(require(TRIM_SOURCE/'FLU2DR64.f',SENDER_SOURCE_SHA)),\n        actual_sender_source_proof=pin(require(TRIM_SOURCE/'sender_source_patch_proof.json',SENDER_PROOF_SHA)),\n        original_selector=pin(selector),python_command=sys.executable,")])
function('declaration_admission',[
 ("    if d['production_link_command']!=link or d['link_inverse']!=inverse:raise ValueError('original-token link differs')", "    if d['production_link_command']!=link or d['link_inverse']!=inverse:raise ValueError('original-token link differs')\n"
  "    selector=ART/'axial-material-moment-order-build-20261006/build/FLU.o'\n"
  "    if (d['actual_production_objects']!=list(map(str,[TRIM_OBJECT,PHYSICAL_OBJECT,SENDER_OBJECT,selector]))\n"
  "        or d['actual_sender']!=dict(path=str(SENDER_OBJECT),sha256=nonzero_sha(SENDER_OBJECT_SHA))\n"
  "        or d['original_sender_ancestry']!=pin(OLD/'build/FLU2DR64.o')\n"
  "        or d['actual_sender_source']!=dict(path=str(TRIM_SOURCE/'FLU2DR64.f'),sha256=SENDER_SOURCE_SHA)\n"
  "        or d['actual_sender_source_proof']!=dict(path=str(TRIM_SOURCE/'sender_source_patch_proof.json'),sha256=SENDER_PROOF_SHA)):\n"
  "        raise ValueError('new actual sender/source/proof and original selector identities differ')")])
function('binary_audit',[
 ("    required={paths[0]:'_spot1p64_',paths[1]:'_spoasm_',paths[2]:'_flu2dr64_',paths[3]:'_flu_'}", "    required=[(paths[0],'_spot1p64_'),(paths[1],'_spoasm_'),(paths[2],'_flu2dr64_'),\n        (paths[2],'_flusp64_'),(paths[3],'_flu_')]"),
 ("    for path,name in required.items():", "    for path,name in required:"),
 ("    for row in executable:", "    if sum(row['name']=='_spof64_' and row['kind'].upper()=='T' for row in executable)!=1:\n        raise ValueError('unchanged real archive SPOF64 definition required')\n    for row in executable:"),
 ("'dense_cache_mod','physical_unit'", "'dense_cache_mod','physical_unit','flusp64_reference','flusp64_window_observer','sender_window_controls'"),
 ("sole_object_changes=['SPOT1P64.o','SPOASM.o']", "sole_object_changes=['SPOT1P64.o','SPOASM.o','FLU2DR64.o']"),
 ("        actual_object_definitions=definitions,actual_runtime=pin(OUT/'runtime/Dragon'),dependencies=deps,", "        actual_object_definitions=definitions,actual_runtime=pin(OUT/'runtime/Dragon'),dependencies=deps,\n        actual_sender=pin(require(SENDER_OBJECT,SENDER_OBJECT_SHA)),\n        actual_sender_source=pin(require(TRIM_SOURCE/'FLU2DR64.f',SENDER_SOURCE_SHA)),\n        actual_sender_source_proof=pin(require(TRIM_SOURCE/'sender_source_patch_proof.json',SENDER_PROOF_SHA)),")])
function('production_admission',[
 ("compiled_trim_kernel=pin(TRIM_OBJECT),inherited_compiled_dedup_kernel=pin(DEDUP_OBJECT),compiled_physical_assembly=pin(PHYSICAL_OBJECT),", "compiled_trim_kernel=pin(TRIM_OBJECT),inherited_compiled_dedup_kernel=pin(DEDUP_OBJECT),compiled_physical_assembly=pin(PHYSICAL_OBJECT),\n        compiled_sender=pin(require(SENDER_OBJECT,SENDER_OBJECT_SHA)),compiled_sender_source=pin(require(TRIM_SOURCE/'FLU2DR64.f',SENDER_SOURCE_SHA)),\n        sender_source_proof=pin(require(TRIM_SOURCE/'sender_source_patch_proof.json',SENDER_PROOF_SHA)),"),
 ("sole_object_changes=['SPOT1P64.o','SPOASM.o']", "sole_object_changes=['SPOT1P64.o','SPOASM.o','FLU2DR64.o']"),
 ("        retained_cache_mathematics_and_rhs_order_unchanged=True,observer_objects_linked=False,", "        retained_cache_mathematics_and_rhs_order_unchanged=True,observer_objects_linked=False,\n        sender_output_storage_window_changed=True,corrected_sender_transport_math_retained=True,\n        sender_window_controls_passed=trim_body['sender_window_controls_passed'],\n        original_68_control_counts=trim_body['original_68_control_counts'],\n        sender_window_control_counts=trim_body['sender_window_control_counts'],\n        sender_wrapper_observer_real_SPOT_credit=0,")])
function('current_new_owned_paths',[
 ("        str(TRIM_TERMINAL/'terminal_return.json')]", "        str(TRIM_TERMINAL/'terminal_return.json'),str(SENDER_OBJECT),str(TRIM_SOURCE/'FLU2DR64.f'),\n        str(TRIM_SOURCE/'sender_source_patch_proof.json'),str(SENDER_HELPER),str(SENDER_PROOF),str(SENDER_SOURCE_INPUT),\n        str(SENDER_DRIVER),str(SENDER_AUDITOR),str(SENDER_CONTRACT)]")])

# Complete sender scope is fixed source text; it is never called here.
G=Path('/private/tmp/axmat_v13_combined_sender_component_gate_draft_20261009/sender_component_contract.function.py')
gate=G.read_text()
assert hashlib.sha256(gate.encode()).hexdigest()=='0de38027fcf124013d4e1f833b50b67d56f825d29975c17cbe801d2c8821b003'
gate_function=ast.get_source_segment(gate,next(n for n in ast.parse(gate).body if isinstance(n,ast.FunctionDef)and n.name=='sender_component_contract'))
region('new_separate_sender_component_contract','\ndef trim_component_contract(value,d,admission):',
       '\n'+gate_function+'\n\n\ndef trim_component_contract(value,d,admission):')
def save():
 ast.parse(text);inverse=text
 for e in reversed(regions):
  assert inverse.count(e['after'])==e['count'],e['name'];inverse=inverse.replace(e['after'],e['before'],e['count'])
 assert inverse==original
 O.write_text(text);(D/'composition_regions.json').write_text(json.dumps(regions,indent=2)+'\n')
 print(json.dumps(dict(status='COMPLETE_COMBINED_SOURCE_UNREADY',candidate_sha256=hashlib.sha256(text.encode()).hexdigest(),regions=len(regions),whole_inverse_byteexact=True,business_executed=False)))
if __name__=='__main__':save()

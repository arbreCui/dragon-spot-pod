"""Finite SOURCE adaptation of the frozen fdd V18 design; no business or live ART."""
import ast
import hashlib
import json
from pathlib import Path

D=Path(__file__).parent
P=Path('/private/tmp/axmat_v18_complete_combined_build_host_source_design_20261010/generate_build_host.py')
OLD_SHA='fdd14188d7d1657d31fc6bce27697b55c00b9c6f4fa8cb159890cace4c04ad54'
old=P.read_text()
assert hashlib.sha256(old.encode()).hexdigest()==OLD_SHA
text=old
edits=[]
def replace(before,after,count=1):
    global text
    assert text.count(before)==count,before[:110]
    text=text.replace(before,after)
    edits.append(dict(old=before,new=after,occurrences=count))
replace("    raise ValueError('UNREADY: V18 PREP actually failed; no V18 build host may be bound or generated. A reviewed fresh family and real closed successful PREP are required.')\n","    # Only the pinned real Root closed-success summary below can enable metadata-only host generation.\n")
replace('5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240','34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b')
# SOURCE family retarget only: every old V17 immutable prerequisite remains untouched.
replace('v18','v19',text.count('v18'))
replace('V18','V19',text.count('V18'))
replace('DRAFT_STATUS = \'UNREADY_FROZEN_V19_FAILED_PREP_NO_BUILD_BINDING_ALLOWED\'',
"DRAFT_STATUS = 'UNREADY_SOURCE_TEMPLATE_AWAIT_REAL_ROOT_V19_CLOSED_SUCCESSFUL_PREP'")
replace("return data, dict(path=str(path),sha256=actual,identity=fields(last),size_bytes=len(data))",
"return data, dict(path=str(path),sha256=actual,identity=fields(last))")
start=text.index('def output_reference(');end=text.index('def write_new(',start)
replace(text[start:end],"""def output_reference(ref, expected_path):
    if set(ref) != {'path','sha256','identity'} or ref['path'] != expected_path:
        raise ValueError('complete actual Root writer output pin required')
    if re.fullmatch('[0-9a-f]{64}',ref['sha256']) is None or not isinstance(ref['identity'],list) or len(ref['identity'])!=7:
        raise ValueError('actual Root output hash and seven identity fields required')
    if any(type(x) is not int for x in ref['identity']):
        raise ValueError('actual Root output pins must be typed')
    if ref['identity'][4] <= 0 or ref['identity'][3]!=1 or not stat.S_ISREG(ref['identity'][2]):
        raise ValueError('ordinary complete actual output metadata required')
    return ref

""")
replace("if s['schema']!='AXMAT_V19_ROOT_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' or s['status']!='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_FULL_BUILD_INPUT_NATIVE_PENDING':",
"if s['schema']!='ROOT_V19_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' or s['status']!='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD':")
start=text.index("    if terminal['record_producer']");end=text.index("    for key in (",start)
replace(text[start:end],"""    if terminal['closed'] is not True or type(tr.get('exit_code')) is not int or tr['exit_code']!=0 or 'session_id' in tr:
        raise ValueError('real Root typed EXIT0 closed terminal required')
    if terminal.get('exit_code',0)!=0 or terminal.get('session_repolled_after_close',False) is not False:
        raise ValueError('Root successful closed terminal with no repoll required')
    if s['Root_actual_terminal']!=s['actual_root_terminal']:
        raise ValueError('Root terminal aliases must be the same complete actual pin')
    cap_keys=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries')
    if tuple(s[k] for k in cap_keys)!=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0):
        raise ValueError('all original complete PREP caps required')
    if s['original_caps_preserved'] is not True or not 0<=s['sampled_peak_rss_mib']<512 or not 0<s['child_seconds']<=600 or not s['child_seconds']<=s['whole_seconds']<1800 or not 0<s['joint_archive_bytes']<2*2**30:
        raise ValueError('actual original bounded PREP metadata required')
""")
replace("if namespace['schema']!='AXMAT_V19_ROOT_ACTUAL_PREPARE_NAMESPACE_FREEZE_V1' or namespace['recorded_after_actual_exit0_closed'] is not True or namespace['original_archive_cap_bytes']!=2*2**30 or namespace['archive_bytes']!=s['archive_bytes']:",
"if namespace['schema']!='ROOT_V19_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' or namespace['no_build_or_native_credit'] is not True:")
replace("'actual_prep_terminal':output_reference(ns[TERMINAL]['files']['declaration_terminal_return.json'],TERMINAL+'/declaration_terminal_return.json')",
"'actual_prep_terminal':output_reference(s['formal_PREP_terminal'],TERMINAL+'/declaration_terminal_return.json')")
replace("recorded_sources = {p['path']:p for p in namespace['input_full_sha7id']}\n    if recorded_sources[str(TARGET)]!=sources[-1]:",
"recorded_sources = {p['path']:p for p in namespace['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']}\n    if recorded_sources[str(TARGET)]!=sources[-1] or namespace['canonical_factory']!=sources[-1]:")
replace("    if len(ns)!=len(namespace['namespaces']):\n        raise ValueError('unique complete namespace records required')",
"""    expected_roots={ART+'axial-material-complete-combined-prepare-host-v19-20261010',SOURCE,OUT,TERMINAL,str(BASE/'actual_complete_combined_prepare_v19_sources')}
    if len(ns)!=len(namespace['namespaces']) or set(ns)!=expected_roots:
        raise ValueError('all five complete actual H/S/O/T/D namespaces required')""")
# Preserve the old immutable source plan and genuine host exactly after finite substitutions.
inverse=text
for e in reversed(edits):
    assert inverse.count(e['new'])==e['occurrences'],(e['old'][:100],e['new'][:100],e['occurrences'],inverse.count(e['new']))
    inverse=inverse.replace(e['new'],e['old'])
assert inverse==old
compile(text,str(D/'generate_build_host.py'),'exec')
with (D/'generate_build_host.py').open('x') as f:f.write(text)
proof=dict(schema='AXMAT_V19_BUILD_GENERATOR_FINITE_SOURCE_INVERSE_TO_FDD_V18_V1',
status='SOURCE_TEMPLATE_ONLY_ACTUAL_CLOSED_PREP_BINDING_NOT_EXECUTED',
parent_path=str(P),parent_sha256=OLD_SHA,new_generator_path=str(D/'generate_build_host.py'),
new_generator_sha256=hashlib.sha256(text.encode()).hexdigest(),
edits=edits,finite_change_count=len(edits),whole_byte_inverse_exact_to_fdd=True,
actual_Root_V19_metadata_writer='/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v19_receipts/write_actual_prepare_terminal.py',
actual_closed_PREP_summary_sha256=None,actual_V19_four_output_pins=None,
business_host_generated=False,actual_binding_branch_executed=False,
project_or_ART_written=False,business_or_numeric_executed=False)
with (D/'generator_source_inverse_proof.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,generator=proof['new_generator_path'],generator_sha256=proof['new_generator_sha256'],
finite_change_count=len(edits),whole_inverse_exact=True,actual_binding_branch_executed=False,business_host_generated=False)))

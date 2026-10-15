"""Independent finite SOURCE/META audit. Reviewed code is never imported or called."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).parent
ORIGINAL=P/'original_source_gap_preserved'
WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT_v2.py')
INSTALLER=Path('/private/tmp/spot_install_v22_complete_native_ROOT_v2.py')
OLD_WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT.py')
OLD_INSTALLER=Path('/private/tmp/spot_install_v22_complete_native_ROOT.py')
HOST=Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf/Root_bound_complete_native_genuine_host.py')
SUPPORT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
CHECKS=[]
INPUTS={}
def identity(path):
    s=path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    before=identity(path)
    assert path.is_absolute() and path.resolve()==path and stat.S_ISREG(before[2]) and before[3]==1
    with path.open('rb') as stream:
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    assert identity(path)==before
    return dict(path=str(path),sha256=digest,size_bytes=before[4],identity=before)
def check(value,label):
    assert value,label
    CHECKS.append(dict(check=label,passed=True))
def read_source(path):
    before=pin(path)
    data=path.read_bytes()
    check(pin(path)==before,'full EOF SHA7ID stable '+str(path))
    INPUTS[str(path)]=before
    return data.decode(),before,ast.parse(data)
def functions(tree):
    return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
def segment(source,node):
    return ast.get_source_segment(source,node)
def dump(tree):
    return ast.dump(tree,include_attributes=False)
def single_replace(source,before,after,label):
    check(source.count(before)==1,'unique inverse anchor '+label)
    return source.replace(before,after,1)
def required(text,terms,prefix):
    for term in terms:
        check(term in text,prefix+term)
def real_tool(path):
    d=json.loads(path.read_text())
    tr=d['actual_tool_return']
    check(d['closed'] is True and d['observed_terminal'] is True,'actual observed closed '+path.name)
    check(type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr,'real typed exit0/noSession '+path.name)
    check(type(tr['chunk_id']) is str and type(tr['output']) is str,'raw real tool fields '+path.name)
    return d

w,wp,wt=read_source(WRITER)
i,ip,it=read_source(INSTALLER)
ow,owp,owt=read_source(OLD_WRITER)
oi,oip,oit=read_source(OLD_INSTALLER)
hs,hp,ht=read_source(HOST)
ss,sp,st=read_source(SUPPORT)
for value,expected,size,label in [
    (wp,'dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc',8213,'v2 writer'),
    (ip,'4c26224d590f3fe389dddb3581b3fa1e39da34f42a720526da11c8a9eeb44aa9',5429,'v2 installer'),
    (owp,'5f302e44a094c20682e1708f3cd714f4e7bedf7da12de1c775ccca7b8338ea5b',8100,'original writer'),
    (oip,'355081f5464a4f9a6588673bb5e3b692457f53aba2a958f8b3d1d5ee95224506',5426,'original installer'),
    (sp,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7',11458,'genuine support')]:
    check(value['sha256']==expected and value['size_bytes']==size,'fixed complete Source '+label)
check((P/'writer_v2_SOURCE.py').read_bytes()==WRITER.read_bytes(),'full v2 writer copied')
check((P/'installer_v2_SOURCE.py').read_bytes()==INSTALLER.read_bytes(),'full v2 installer copied')
check((ORIGINAL/'original_5f302e_writer_SOURCE.py').read_bytes()==OLD_WRITER.read_bytes(),'full original writer retained exact')
check((ORIGINAL/'original_355081_installer_SOURCE.py').read_bytes()==OLD_INSTALLER.read_bytes(),'full original installer retained exact')

writer_hunks=[
    ("report,report_pin=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')",
     "report,_=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')"),
    ("        assert {k:report_pin[k] for k in ('path','sha256','identity')}==host['actual_native']['report']\n",'')]
reverse_w=w
for n,(before,after) in enumerate(writer_hunks):
    reverse_w=single_replace(reverse_w,before,after,'writer '+str(n+1))
check(reverse_w==ow,'writer all-byte inverse restores complete original')
check(dump(ast.parse(reverse_w))==dump(owt),'writer whole AST inverse exact original')
installer_hunks=[
    ("WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT_v2.py')","WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT.py')"),
    ("WRITER_SHA='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc'","WRITER_SHA='5f302e44a094c20682e1708f3cd714f4e7bedf7da12de1c775ccca7b8338ea5b'")]
reverse_i=i
for n,(before,after) in enumerate(installer_hunks):
    reverse_i=single_replace(reverse_i,before,after,'installer '+str(n+1))
check(reverse_i==oi,'installer all-byte inverse restores complete original')
check(dump(ast.parse(reverse_i))==dump(oit),'installer whole AST inverse exact original')
wf=functions(wt);owf=functions(owt);inf=functions(it);oinf=functions(oit)
check(list(wf)==list(owf)==['identity','pin','snapshot','read','write','bytes_in','main'],'all seven writer definitions retained')
for name in wf:
    if name!='main':
        check(segment(w,wf[name])==segment(ow,owf[name]),'writer definition byteexact '+name)
        check(dump(wf[name])==dump(owf[name]),'writer definition ASTexact '+name)
check(list(inf)==list(oinf)==['main'],'installer main definition retained')
check(segment(i,inf['main'])==segment(oi,oinf['main']),'installer complete main byteexact')
check(dump(inf['main'])==dump(oinf['main']),'installer complete main ASTexact')

success=[n for n in wf['main'].body if isinstance(n,ast.If) and ast.get_source_segment(w,n.test)=="tr['exit_code']==0"]
check(len(success)==1,'one original successful Root terminal branch')
sb=success[0].body
newassert=[n for n in sb if isinstance(n,ast.Assert) and "host['actual_native']['report']" in segment(w,n)]
check(len(newassert)==1,'one success actual report pin comparison')
test=newassert[0].test
check(isinstance(test,ast.Compare) and len(test.ops)==1 and isinstance(test.ops[0],ast.Eq),'exact equality compares actual saved report')
check(isinstance(test.left,ast.DictComp),'only three primitive pin fields projected from full report pin')
check(ast.literal_eval(test.left.generators[0].iter)==('path','sha256','identity'),'exact producer path SHA sevenID field order')
check(segment(w,test.left.key)=='k' and segment(w,test.left.value)=="report_pin[k]",'actual read pin directly supplies compared values')
check(segment(w,test.comparators[0])=="host['actual_native']['report']", 'direct genuine actual stage report pin target')
check(sb.index(newassert[0])>0 and segment(w,sb[0]).startswith('assert host is not None and report is not None and watch is not None'),'report success present guard before actual pin comparison')
check(segment(w,sb[-1])=='success=True','success only after all original evidence/cap guards')
check(w.index("report,report_pin=read(")<w.index("if tr['exit_code']==0:"),'report pin acquired before success branch')
check("host['actual_native']['report']" not in ow,'original missing crosspin gap retained honestly')
support_pin=functions(st)['pin']
support_return=[n for n in support_pin.body if isinstance(n,ast.Return)]
check(len(support_return)==1 and isinstance(support_return[0].value,ast.Dict),'actual genuine support pin producer is dict')
check([ast.literal_eval(n) for n in support_return[0].value.keys]==['path','sha256','identity'],'actual genuine stage pin has exactly compared three keys')
required(segment(ss,support_pin),["hashlib.file_digest(stream, 'sha256')","identity(path) != before"],'genuine pin fullhash stability ')
required(hs,["'report':support.pin(report_path)","returned['report']['sha256']==support.pin(report_path)['sha256']","returned['report']['identity']==support.pin(report_path)['identity']","actual_native=stage"],'genuine host direct actual report provenance ')

required(w,[
    "type(tr['exit_code']) is int","'session_id' not in tr","receipt['closed'] is True",
    "receipt['observed_terminal'] is True","receipt['session_repolled_after_close'] is False",
    "receipt['actual_terminal_chunk']==tr['chunk_id']",
    "assert snapshot(D)==pre['complete_D_frozen']",
    "current_E['files'][k]==q",
    "pre['native_executed'] is False",
    "snapshot(p) for p in (H,O,C,D,E)",
    "with p.open('x')",
    "allow_nan=False",
    "native_persisted_XSM_value_bits_verified=success",
    "all_complete_A_B_scopes_retained_and_verified=success",
    "actual_native_byte_qualification_sha256=None",
    "original_XSM_memory_bits_verified=False",
    "original_native_build_binary_Source_linkage_qualified=False",
    "new_native_walker_controls_actual_run=None",
    "physical_neutron_balance_qualified=False",
    "scientific_accuracy_qualified=False",
    "AAA_accuracy_qualified=False",
    "ABA_admitted=False",
    "goal_complete=False",
    "outer_tool_output_scope='ACTUAL_EXEC_COMMAND_MERGED_EXTERNAL_HOST_STDOUT_STDERR'",
    "separate_external_host_stderr_saved=False",
    "independent_external_host_stderr_empty_verified=False",
    "E_directory_identity_after_postclose_appends_claimed_unchanged=False",
    "new_numeric_execution_by_writer=False",
    "cleanup_performed=False",
], 'complete unchanged writer contract ')
required(w,[
    "whole_seconds=1800","stage_seconds=600","rss_mib=512",
    "joint_archive_bytes=2*2**30","history_bytes=96*2**30",
    "free_floor_bytes=8*2**30","threads=1","children_at_once=1","retries=0",
    "host['original_caps']==CAPS and report['original_caps']==CAPS",
    "[r['state'] for r in report['states']]==['A','B']",
    "(19619,19990,2264113)",
    "('complete_MACROLIB','complete_MICROLIB')",
    "all_persisted_native_value_bits_equal_ASCII",
    "native_physical_preorder_equal_original_ASCII",
    "all_complete_orders_preserved_on_disk",
    "host['actual_native']['watchdog']==watch",
    "watch['sampled_peak_rss_mib']<512",
    "watch['wall_cap_seconds']<=600",
    "host['whole_seconds']<1800",
    "len(host['stage_records'])==1",
    "bytes_in(final)<2*2**30",
],'complete original caps/data scopes ')
for tree,label,allowed in [(wt,'writer',{'argparse','hashlib','json','os','stat','pathlib'}),(it,'installer',{'argparse','hashlib','importlib.util','json','os','shutil','sys','pathlib'})]:
    imports=[]
    for node in tree.body:
        if isinstance(node,ast.Import):imports.extend(n.name for n in node.names)
        if isinstance(node,ast.ImportFrom):imports.append(node.module)
    check(set(imports)<=allowed,label+' only standard module imports')
    check(not any(isinstance(n,(ast.Import,ast.ImportFrom)) for f in functions(tree).values() for n in ast.walk(f)),label+' no project imports inside functions')
    for word in ('subprocess','exec_command','run_stage','Popen','ctypes'):
        check(word not in (w if label=='writer' else i),label+' no candidate guard or native call '+word)
    check("if __name__=='__main__':main()" in (w if label=='writer' else i),label+' main protected at import')
required(i,[
    "spec_from_file_location('Root_native_metadata_functions_only',WRITER)",
    "not any(os.path.lexists(p) for p in (m.D,m.H,m.O,m.C))",
    "len(original['files'])==89",
    "set(original['files'])==set(manifest['members'])",
    "peer['files'][k][key]",
    "review['all_checks_typed_true'] is True",
    "review['blockers']==[]",
    "type(tr['exit_code']) is int and tr['exit_code']==0",
    "meta_review['writer_pin']==m.pin(WRITER)",
    "for k,q in view['files'].items()",
    "m.pin(p)['sha256']==q['sha256']",
    "m.pin(p)['size_bytes']==q['size_bytes']",
    "m.snapshot(Path(view['root']))==view",
    "copy_view(before_E,Path('complete_original_E_receipts_before_install'))",
    "Root_native_postclose_META_writer.py",
    "Root_native_Source_installer.py",
    "frozen=m.snapshot(m.D);assert m.snapshot(m.E)==before_E",
    "all_original_input_pins_preserved_129=True",
    "actual_native_byte_qualification_sha256=None",
    "scientific_accuracy_qualified=False",
    "no_D_append_after_freeze=True",
    "actual_native_not_executed=True"
], 'complete unchanged install/freeze contract ')
old=json.loads((ORIGINAL/'REVIEW.json').read_text())
check(old['status']=='SOURCE_BLOCKED_EXACT_REPORT_PIN_BINDING_GAP' and len(old['blockers'])==1,'original real SOURCE blocker preserved')
check(old['writer_pin']==owp and old['installer_pin']==oip and old['limited_genuine_host_Source_pin']==hp,'original reported pins match unchanged full source')
check(old['check_count']==15 and all(type(r['passed']) is bool and r['passed'] is True for r in old['checks']),'original finite fifteen source checks retained')
tools={}
for path in sorted(P.glob('actual_*_tool_return.json')):
    tools[path.name]=real_tool(path)
check(tools['actual_original_Source_review_tool_return.json']['actual_tool_return']['chunk_id']=='5d3ef2','original actual review terminal 5d3ef2 retained')
check('SOURCE_BLOCKED_EXACT_REPORT_PIN_BINDING_GAP' in tools['actual_original_Source_review_tool_return.json']['actual_tool_return']['output'],'original blocker tool output preserved')
for path,value in INPUTS.items():check(pin(Path(path))==value,'final complete source sevenID unchanged '+path)
proof=dict(schema='INDEPENDENT_ROOT_NATIVE_POSTCLOSE_META_V2_FINITE_SOURCE_INVERSE_V1',
    writer_hunks=[dict(new=a,old=b) for a,b in writer_hunks],
    installer_hunks=[dict(new=a,old=b) for a,b in installer_hunks],
    writer_whole_byte_AST_inverse_exact_original=True,installer_whole_byte_AST_inverse_exact_original=True,
    original_source_gap_preserved=True,only_report_read_pin_retention_and_threefield_success_binding_added=True,
    original_all_cap_data_bit_flag_guards_unchanged=True,
    genuine_guard_classes_MRO_not_modified=True,
    numeric_candidate_guard_or_native_execution=False)
(P/'SOURCE_INVERSE_PROOF.json').write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
report=dict(schema='INDEPENDENT_ROOT_NATIVE_POSTCLOSE_METADATA_V2_SOURCE_REVIEW_V1',
    status='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY',
    all_checks_typed_true=True,blockers=[],check_count=len(CHECKS),checks=CHECKS,
    writer_pin=wp,installer_pin=ip,original_writer_pin=owp,original_installer_pin=oip,
    limited_genuine_host_Source_pin=hp,actual_genuine_report_pin_producer_Source_pin=sp,
    complete_reviewed_input_pins=INPUTS,source_only=True,
    original_single_gap_retained_and_fixed_by_exact_report_pin_binding=True,
    original_native_bound_89_Source_not_reaudited=True,
    installer_complete_original_bound89_and_source_peer_and_META_peer_and_original_E_copy_preserved=True,
    original_root_scope_caps_and_two_states_bit_evidence_conditions_preserved=True,
    installer_writer_source_installed_before_D_freeze=True,
    reviewer_imported_or_executed_candidate=False,
    reviewer_guard_or_native_or_numeric_executed=False,
    material_payload_read_or_decoded=False,
    canonical_ART_frozen_D_E_modified=False,
    actual_native_run_started_by_reviewer=False,
    actual_native_byte_qualification_sha256=None,
    original_XSM_memory_bits_verified=False,
    original_native_build_binary_Source_linkage_qualified=False,
    new_native_walker_controls_actual_run=None,
    whole_combined_build_qualified=False,
    whole_combined_INPUT_admitted=False,native_RSS_verified=False,
    physical_neutron_balance_qualified=False,scientific_accuracy_qualified=False,
    AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,
    future_saved_NATIVE_review_requires_real_Root_typed_CLOSED_terminal=True,
    actual_directory_empty_metadata_from_original_bounded_read_retained_only=True)
(P/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(P/'REPORT.txt').write_text(
    'PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY\n'
    'V2 writer dcdfbe2e/8213 B: exactly two source changes retain the full report read pin and bind path/SHA256/7ID to genuine host actual_native.report before success. Genuine support pin returns exactly these three fields.\n'
    'V2 installer 4c26224d/5429 B: only writer path and SHA literals retargeted. Writer all-byte/AST inverse and installer all-byte/AST inverse restore original 5f302e/355081; six writer metadata definitions and full installer main byteexact. Complete originals and original one-gap review/tool results are preserved.\n'
    'Original A/B complete micro/macro evidence scopes, true Root terminal gates, D/E input preservation, install-before-freeze, full source copy, 1800/600/512/2GiB/96GiB/free8/1child/1thread/0retry and false science/unknown native qualification remain unchanged. No 89-file source replay or payload/history scan.\n'
    'Only reviewer-owned standard-library SOURCE text/AST/hash/META audit executed. No candidate, installer, guard, native, decoder, numerical program, canonical/ART/frozen D/E write, or new native qualification. Root has not acquired native execution or scientific credit from this Source review.\n')
(P/'writer_v2.diff').write_text(''.join(difflib.unified_diff(ow.splitlines(True),w.splitlines(True),fromfile=str(OLD_WRITER),tofile=str(WRITER))))
(P/'installer_v2.diff').write_text(''.join(difflib.unified_diff(oi.splitlines(True),i.splitlines(True),fromfile=str(OLD_INSTALLER),tofile=str(INSTALLER))))
(P/'genuine_report_pin_producer_SOURCE.txt').write_text('SOURCE '+str(SUPPORT)+'\n'+segment(ss,support_pin)+'\n')
(P/'limited_genuine_host_report_binding_SOURCE.txt').write_text(
    'SOURCE '+str(HOST)+'\n'+segment(hs,functions(ht)['observed_stage'])+'\n'+
    '\n'.join(line for line in hs.splitlines() if 'actual_native=stage' in line)+'\n')
print(json.dumps(dict(status=report['status'],check_count=len(CHECKS),writer=wp,installer=ip,report=str(P/'REVIEW.json'),no_candidate_guard_native_numeric_executed=True)))


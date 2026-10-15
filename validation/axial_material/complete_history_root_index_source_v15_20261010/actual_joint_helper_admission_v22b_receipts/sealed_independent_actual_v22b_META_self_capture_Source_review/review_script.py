"""Bounded independent stdlib SOURCE/META audit; never imports reviewed code."""
from pathlib import Path
import ast, hashlib, json, os, stat, sys

B = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D = B / 'actual_joint_helper_admission_v22b_sources'
E = B / 'actual_joint_helper_admission_v22b_receipts'
OLD_D = B / 'actual_joint_helper_admission_v22_sources'
HERE = Path(__file__).parent
checks, observed = [], {}

def check(name, ok):
    assert type(ok) is bool, name
    checks.append({'name': name, 'PASS': ok})
    assert ok, name

def id7(p):
    s = p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def full(p, expected=None):
    p = Path(p); before = id7(p)
    check('regular nonsymlink '+str(p), stat.S_ISREG(before[2]) and not p.is_symlink())
    h = hashlib.sha256(); data = bytearray()
    with p.open('rb') as stream:
        while True:
            part = stream.read(1024*1024)
            if not part: break
            h.update(part); data.extend(part)
    check('full EOF identity unchanged '+str(p), id7(p) == before)
    actual = {'path':str(p),'sha256':h.hexdigest(),'size_bytes':len(data),'identity':before}
    if expected is not None:
        check('full pin equal '+str(p), actual == expected)
    if str(p) in observed: check('same input full pin '+str(p), observed[str(p)] == actual)
    observed[str(p)] = actual
    return bytes(data), actual

def read(p, expected=None):
    raw, actual = full(p, expected)
    def pairs(items):
        result = {}
        for key,value in items:
            assert key not in result
            result[key] = value
        return result
    def bad(value): raise ValueError(value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad),actual

old_path = OLD_D / 'write_actual_joint_helper_admission_v22.READY.py'
new_path = D / 'write_actual_joint_helper_admission_v22b.READY.py'
proof_path = D / 'Root_actual_v22b_META_self_capture_SOURCE_inverse.json'
freeze_path = E / 'Root_final_v22b_META_writer_Source_freeze.json'
receipt_path = E / 'Root_actual_v22b_META_self_capture_Source_correction_tool_return.json'
proof, proof_pin = read(proof_path)
freeze, freeze_pin = read(freeze_path)
receipt, receipt_pin = read(receipt_path)
check('proof schema',proof['schema']=='ROOT_V22B_FINITE_SAVED_META_SELF_CAPTURE_SOURCE_CORRECTION_V1')
check('freeze schema',freeze['schema']=='ROOT_V22B_FINITE_META_WRITER_SOURCE_FREEZE_V1')
check('receipt schema',receipt['schema']=='ROOT_V22B_ACTUAL_FINITE_META_SELF_CAPTURE_SOURCE_CORRECTION_TOOL_RETURN_V1')
check('fixed proof SHA',proof_pin['sha256']=='4451424dd0d678a3363a8926e8b8d8a9e870a2c87c7b0b88773b6469726e8f0b')
check('fixed freeze SHA',freeze_pin['sha256']=='7c6ac56a7f4f54699721d12ed93edfa138f786e4e134f1bccf0d6168bfa094e6')
old_raw, old_pin = full(old_path,proof['parent'])
new_raw, new_pin = full(new_path,proof['candidate'])
check('fixed old writer SHA',old_pin['sha256']=='61d552c4b2efe0334742c4d9ad1bf7cedd9558c49c66e9f51fdd25d611969b51')
check('fixed corrected writer SHA',new_pin['sha256']=='a9fefd704170ce12cb68f329e75e3b4a015f665f7e8637abf1bb697437aa1c35')
old, new = old_raw.decode(),new_raw.decode()
check('exact two declared hunks',len(proof['hunks'])==2 and [x['mode'] for x in proof['hunks']]==['pure','fresh'])
undo = new
for hunk in reversed(proof['hunks']):
    check('unique new hunk '+hunk['mode'],undo.count(hunk['after'])==1)
    undo = undo.replace(hunk['after'],hunk['before'],1)
check('whole byte inverse exact old writer',undo.encode()==old_raw)
check('whole AST inverse exact old writer',ast.dump(ast.parse(undo),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
ot,nt = ast.parse(old),ast.parse(new)
of = {x.name:x for x in ot.body if isinstance(x,ast.FunctionDef)}
nf = {x.name:x for x in nt.body if isinstance(x,ast.FunctionDef)}
check('all 17 function names and order retained',list(of)==list(nf) and len(nf)==17)
changed = {'validate_pure_saved_review_v22','validate_fresh_saved_review_v22'}
for name in of:
    if name not in changed:
        check('untouched function bytes '+name,ast.get_source_segment(old,of[name])==ast.get_source_segment(new,nf[name]))
        check('untouched function AST '+name,ast.dump(of[name],include_attributes=False)==ast.dump(nf[name],include_attributes=False))
check('all globals imports doc and top-level main guard unchanged',ast.dump(ast.Module(body=[x for x in ot.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]),include_attributes=False)==ast.dump(ast.Module(body=[x for x in nt.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]),include_attributes=False))
check('no reviewed Source imported or executed',all(x.module in ('pathlib',) for x in nt.body if isinstance(x,ast.ImportFrom)) and all(a.name in ('math','struct','os','sys','hashlib','json','stat') for x in nt.body if isinstance(x,ast.Import) for a in x.names))

expected_maps = {
 'pure': {'Root_actual_pure_protocol_namespace_manifest.json':'Root_namespace_manifest_pin','Root_actual_pure_protocol_summary.json':'Root_summary_pin'},
 'fresh': {'Root_actual_fresh_verifier_namespace_manifest.json':'Root_namespace_manifest_pin','Root_actual_fresh_verifier_summary.json':'Root_summary_pin'},
}
shape_summary = {}
for kind,function_name,files_key,root_variable,expected_root in (
 ('pure','validate_pure_saved_review_v22','regular_files','P',B/'actual_complete_graph_helper_controls_v22_receipts'),
 ('fresh','validate_fresh_saved_review_v22','complete_regular_files','E',B/'actual_complete_graph_fresh_verifier_v22_receipts'),
):
    source = ast.get_source_segment(new,nf[function_name])
    expected_block = (
        '        self_capture = {\n' +
        ''.join('            '+repr(k)+': '+repr(v)+',\n' for k,v in expected_maps[kind].items()) +
        '        }\n' +
        "        null_names = {name for name, entry in snapshot['"+files_key+"'].items() if entry is None}\n" +
        "        if snapshot['label'] == 'E_pre_summary':\n" +
        "            assert snapshot['root'] == str("+root_variable+") and null_names == set(self_capture)\n" +
        '        else:\n            assert not null_names\n' +
        "        for name, entry in snapshot['"+files_key+"'].items():\n" +
        '            if entry is None:\n' +
        "                assert snapshot['label'] == 'E_pre_summary' and name in self_capture\n" +
        '                post_capture_pin = value[self_capture[name]]\n' +
        "                assert Path(post_capture_pin['path']) == Path(snapshot['root']) / name\n" +
        '                verify(post_capture_pin)\n' +
        '            else:\n                verify(entry)\n')
    check('independently specified complete resolution block '+kind,source.count(expected_block)==1)
    hunk = next(x for x in proof['hunks'] if x['mode']==kind)
    check('declared correction equals independent exact block '+kind,hunk['after']==expected_block)
    restored = source.replace(expected_block,hunk['before'],1)
    check('changed validator all original bytes retained '+kind,restored==ast.get_source_segment(old,of[function_name]))
    peer,peer_pin = read(proof['actual_saved_shapes'][kind]['path'],proof['actual_saved_shapes'][kind])
    check('original actual snapshot labels '+kind,[x['label'] for x in peer['complete_namespace_snapshots']]==['D','H','O','E_pre_summary'])
    rows=[]
    for snapshot in peer['complete_namespace_snapshots']:
        entries = snapshot[files_key]
        nulls = {name for name,value in entries.items() if value is None}
        check('complete original count '+kind+'/'+snapshot['label'],type(snapshot['regular_file_count']) is int and snapshot['regular_file_count']==len(entries))
        check('complete directory count '+kind+'/'+snapshot['label'],type(snapshot['directory_count']) is int and snapshot['directory_count']==len(snapshot['directories']))
        if snapshot['label']=='E_pre_summary':
            check('exact saved E root '+kind,snapshot['root']==str(expected_root))
            check('exact two reserved nulls '+kind,nulls==set(expected_maps[kind]))
        else:
            check('all other snapshots no null '+kind,not nulls)
        for name,entry in entries.items():
            if entry is None:
                post = peer[expected_maps[kind][name]]
                check('postcapture exact root/name '+kind+'/'+name,Path(post['path'])==Path(snapshot['root'])/name)
                check('postcapture full pin shape '+kind+'/'+name,type(post) is dict and type(post['identity']) is list and len(post['identity'])==7 and all(type(i) is int for i in post['identity']) and type(post['size_bytes']) is int and post['size_bytes']==post['identity'][4])
                full(post['path'],post)
            else:
                check('nonnull full pin shape '+kind+'/'+snapshot['label']+'/'+name,type(entry) is dict and type(entry['identity']) is list and len(entry['identity'])==7 and all(type(i) is int for i in entry['identity']) and type(entry['sha256']) is str and len(entry['sha256'])==64)
        rows.append({'label':snapshot['label'],'root':snapshot['root'],'regular_file_count':len(entries),'directory_count':len(snapshot['directories']),'actual_null_names':sorted(nulls),'each_null_resolved_by_verified_complete_postcapture_pin':True})
    shape_summary[kind] = rows

check('closed actual correction receipt',receipt['closed'] is True and receipt['actual_tool_return_observed'] is True and receipt['source_only'] is True)
tr = receipt['actual_tool_return']
check('actual correction typed0 no session',tr['chunk_id']=='d58c34' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
actual_output = json.loads(tr['output'])
check('actual receipt exact corrected writer pin',actual_output['corrected_writer']==new_pin)
check('actual receipt exact inverse record pin',actual_output['Source_record']==proof_pin)
check('actual receipt 2 hunks 17 functions no Q no business',actual_output['hunks']==2 and actual_output['function_count']==17 and actual_output['all_original_constructor_and_caps_retained'] is True and actual_output['new_Q'] is None and actual_output['business_executed'] is False)
failure,failure_pin = read(proof['actual_metadata_writer_failure']['path'],proof['actual_metadata_writer_failure'])
check('actual prior metadata failure preserved',failure['schema']=='ROOT_V22_ACTUAL_JOINT_HELPER_META_WRITER_FAILED_TOOL_RETURN_V1' and failure['closed'] is True and failure['new_Q_created'] is False and failure['helper_guard_or_numeric_business_executed'] is False)
check('actual prior writer typed1 no session',failure['actual_tool_return']['chunk_id']=='c8c7d5' and type(failure['actual_tool_return']['exit_code']) is int and failure['actual_tool_return']['exit_code']==1 and 'session_id' not in failure['actual_tool_return'])
check('complete new SOURCE namespace two files one dir',freeze['file_count']==2 and freeze['directory_count']==1 and set(freeze['complete_files'])=={new_path.name,proof_path.name} and set(freeze['complete_directories'])=={'.'})
check('exact new namespace file membership',{str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}==set(freeze['complete_files']))
check('exact new namespace directory membership',{'.'}|{str(p.relative_to(D)) for p in D.rglob('*') if p.is_dir()}==set(freeze['complete_directories']))
for rel,expected in freeze['complete_files'].items():full(D/rel,expected)
for rel,expected in freeze['complete_directories'].items():check('new source directory id7 '+rel,id7(D/rel)==expected)

old_freeze,_ = read(B/'actual_joint_helper_admission_v22_receipts/Root_final_joint_Q_writer_SOURCE_freeze.json')
check('original frozen D33/2 complete shape',old_freeze['file_count']==33 and old_freeze['directory_count']==2)
check('old namespace membership unchanged',{str(p.relative_to(OLD_D)) for p in OLD_D.rglob('*') if p.is_file()}==set(old_freeze['complete_files']))
for rel,expected in old_freeze['complete_files'].items():full(OLD_D/rel,expected)
for rel,expected in old_freeze['complete_directories'].items():check('old source directory id7 '+rel,id7(OLD_D/rel)==expected)

prior=Path('/private/tmp/axmat_v22_READY_joint_Q_writer_BOUND_independent_SOURCE_review_20261010__pyafi5h/REVIEW.json')
prior_review,prior_pin=read(prior)
check('prior bound review reused with candid discovered omission',prior_pin['sha256']=='2d642ac5f33668da8e8d274d8d16bbe4a838cf495f5332c11d0210d75d37d0c1')
check('prior reviewed contract 616 count',prior_review['check_count']==616)
check('Q still not created',not (B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json').exists())
for path,expected in list(observed.items()):full(path,expected)
for rel,expected in freeze['complete_directories'].items():check('final new directory identity '+rel,id7(D/rel)==expected)
for rel,expected in old_freeze['complete_directories'].items():check('final old directory identity '+rel,id7(OLD_D/rel)==expected)

review = {
 'schema':'INDEPENDENT_V22B_FINITE_SELF_CAPTURE_META_WRITER_SOURCE_REVIEW_V1',
 'SOURCE_PASS':True,'PASS':True,'hard_blockers':[],'check_count':len(checks),'checks':checks,
 'corrected_writer':new_pin,'source_inverse_record':proof_pin,'actual_Root_correction_tool_receipt':receipt_pin,
 'actual_saved_meta_shape_resolution':shape_summary,'complete_full_EOF_Source_META_inputs':observed,
 'complete_input_count':len(observed),'whole_two_hunk_byte_and_AST_inverse_to_actual61d552':True,
 'fifteen_other_functions_and_all_globals_main_constructor_caps_unchanged':True,
 'four_exact_self_capture_nulls_verified_using_same_peer_postcapture_fullpin':True,
 'every_other_null_strictly_rejected_by_independently_specified_AST':True,
 'old_frozen33files2dirs_fully_reverified_unchanged':True,
 'previous_static_review_missed_self_capture_null_records':True,
 'actual_previous_writer_failure_receipt':failure_pin,
 'prior_bound_SOURCE_review_reused_only_for_unchanged_contract':prior_pin,
 'new_Q':None,'writer_or_validator_or_helper_guard_API_business_numeric_executed_by_peer':False,
 'project_canonical_D_E_ART_or_original_Source_modified_by_peer':False,
 'large_graph_material_numeric_or_gzip_payload_read_or_decoded':False,
 'actual_new_writer_execution_success_qualified':False,
 'helper_qualification_Q_created_by_this_review':False,
 'whole_build_INPUT_native_physics_AAA_ABA_or_goal_qualification':False,
}
(HERE/'REVIEW.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(HERE/'REPORT.txt').write_text('SOURCE_PASS only. Corrected writer a9fefd; exact two-hunk inverse to actual 61d552.\nAll 17 function names, other 15 full functions, globals/main/constructor/caps retained.\nPure and fresh E_pre_summary each have exactly two self-capture null records; each is resolved by the same peer postcapture full pin at exact root/name. No field is skipped. Other nulls reject.\nPrior c8c7d5 actual writer failure and earlier static-review omission are preserved candidly. Old frozen D33/2 unchanged; new D2/1 unchanged.\nNo writer, validator, helper, guard, business or numerical call was made. No graph/material/gzip payload was read. No new Q or physical/scientific qualification was created.\n')
print(json.dumps({'review_package':str(HERE),'SOURCE_PASS':True,'check_count':len(checks),'input_count':len(observed),'REVIEW_sha256':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest(),'writer_sha256':new_pin['sha256'],'new_Q':None}))

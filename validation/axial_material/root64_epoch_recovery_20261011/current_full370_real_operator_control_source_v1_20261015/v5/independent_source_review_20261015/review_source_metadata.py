"""Independent bounded Source/metadata review; never import candidate modules.

Eleven scientific extraction JSONs and all live scientific/binary inputs are
current7-only. Their original complete pins remain evidence, not new EOF claims.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

sys.dont_write_bytecode = True
R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
ART = R/'validation/artifacts'
BASE = REC/'current_full370_real_operator_control_source_v1_20261015/v5'
HERE = Path(__file__).absolute().parent
TOP = BASE.parent
CORE = REC/'full370_unreduced_eigen_reference_source_v2'
CAP = REC/'current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015'
OUT = ART/'axial-material-current-full370-real-operator-control-20261015-v3'
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
    fresh_bytes=2147483648, history_bytes=103079215104,
    cold_reserve_bytes=20971764748, metadata_reserve_bytes=67108864,
    free_floor_bytes=8589934592, threads=1, children_at_once=1, retries=0)
FALSE = dict(physics_qualified=False, complete_reaction_authority_qualified=False,
    full_reference_qualified=False, formal_H150_NZ48_full_controls_qualified=False,
    scientific_accuracy_qualified=False, AAA_qualified=False, ABA_admitted=False,
    goal_complete=False, formal_SN32_equivalence_claimed=False,
    stored_native_REAL32_temperature_selection_qualified=False)
EXTRACT = ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence'
EXCEPTIONS = {str(EXTRACT/(n+'_actual_saved_MT5_P0.json')) for n in
    ('U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55')}
RETIRED = {str(ART/'axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence/A1'/n)
    for n in ('original_archive_index.sqlite','original_words.bin')}
LARGE = {str(ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1'/n)
    for n in ('Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',
              'inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')}
LARGE.update(str(ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2'/n)
    for n in ('Root_actual_eight_fuel_finite18_SCAT_summary.json',
              'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json'))
STARTED = time.monotonic()

def need(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)

def limits():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    need(peak < 512*2**20 and time.monotonic()-STARTED < 600, 'bounded reviewer SELF512/stage600')

def ident(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def strict(raw):
    def pairs(items):
        d = {}
        for k,v in items:
            need(k not in d, 'duplicate JSON key')
            d[k] = v
        return d
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x:
        (_ for _ in ()).throw(ValueError('nonfinite JSON '+x)))

def current(p):
    need(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'}, 'complete Python fullPF schema')
    need(type(p['size_bytes']) is int and type(p['identity']) is list and len(p['identity'])==7
        and all(type(x) is int for x in p['identity']), 'typed fullPF size/identity')
    q = Path(p['path'])
    need(q.is_absolute() and '..' not in q.parts and str(q) not in RETIRED, 'literal live path, no retired spool')
    need(not any(x.is_symlink() for x in (q,*q.parents)), 'no path alias')
    s = q.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and ident(s)==p['identity']
        and s.st_size==p['size_bytes'], 'exact ordinary current7 '+str(q))
    limits()
    return q

def eof(p):
    q = current(p)
    need(str(q) not in EXCEPTIONS, 'scientific extraction document must remain current7-only')
    need(p['size_bytes'] < (64*2**20 if str(q) in LARGE else 8*2**20), 'exact-role metadata/Source read cap')
    h = hashlib.sha256(); n = 0
    with q.open('rb') as f:
        need(ident(os.fstat(f.fileno()))==p['identity'], 'opened fullPF7')
        while True:
            limits(); raw = f.read(2**20)
            if not raw: break
            h.update(raw); n += len(raw)
        need(ident(os.fstat(f.fileno()))==p['identity'], 'EOF opened7')
    current(p)
    need(n==p['size_bytes'] and h.hexdigest()==p['sha256'], 'fullEOF/SHA '+str(q))

def fresh_pin(q):
    s = q.lstat(); p = dict(path=str(q),sha256='',size_bytes=s.st_size,identity=ident(s))
    current(p); h = hashlib.sha256()
    with q.open('rb') as f:
        for raw in iter(lambda:f.read(2**20),b''): h.update(raw); limits()
    current(p); p['sha256'] = h.hexdigest()
    return p

def read(p):
    eof(p)
    value = strict(Path(p['path']).read_bytes())
    current(p)
    return value

def unique(rows):
    d = {}
    for p in rows:
        need(p['path'] not in d or d[p['path']]==p, 'one complete selected fullPF per path')
        d[p['path']] = p
    return list(d.values())

def contains(value, wanted):
    return value==wanted or (type(value) is dict and any(contains(x,wanted) for x in value.values())) or (
        type(value) is list and any(contains(x,wanted) for x in value))

def closed(tools,key,pin,label):
    r = tools[key]
    need(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int
        and tools['original_integer_exit_code']==0 and type(r['exit_code']) is int
        and r['exit_code']==0 and r.get('session_id') is None, 'genuine typed0 terminal')
    need(strict(r['output'].strip().splitlines()[-1])[label]==pin, 'terminal exact output pin')

def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--reviewer-freeze-pin',required=True)
    args = ap.parse_args()
    freeze_pin = strict(args.reviewer_freeze_pin); freeze = read(freeze_pin)
    need(freeze['schema']=='INDEPENDENT_FULL370_V5_REVIEWER_SOURCE_ONLY_FREEZE_V1'
        and freeze['reviewer_not_yet_executed'] is True, 'frozen read-only reviewer Source')
    eof(freeze['reviewer_source_pin'])
    need(freeze['reviewer_source_pin']['path']==str(Path(__file__).absolute()), 'reviewer Source path')
    ready_pin = freeze['ready_pin']; gen_pin = freeze['generation_tools_pin']
    ready = read(ready_pin); gen = read(gen_pin); plan = read(ready['plan_pin'])
    author = read(ready['author_source_freeze_pin']); inverse = read(ready['original_Source_inverse_proof_pin'])
    need(ready_pin['sha256']=='b576247e10521d70413dcfc4eef7e685635f127176dc501f1a9ddd9b2da64112'
        and ready_pin['size_bytes']==259102, 'exact actual same-round READY')
    closed(gen,'actual_Source_preparation_return',ready_pin,'ready_pin')
    need(ready['schema']=='FULL370_REAL_OPERATOR_CONTROL_SOURCE_REVIEW_READY_V1'
        and plan['schema']=='FULL370_REAL_CURRENT_MATERIAL_OPERATOR_CONTROL_SOURCE_ONLY_PLAN_V1'
        and ready['source_only'] is True and ready['source_preparation_only'] is True, 'Source-only same-round schemas')
    need(author['source_only'] is True and author['author_writes_stopped'] is True
        and author['source_preparation_executed'] is False, 'preserved author freeze')
    selected = unique([ready_pin,ready['plan_pin'],ready['author_source_freeze_pin'],ready['worker_source_pin'],
        ready['host_source_pin'],ready['original_Source_inverse_proof_pin']]+ready['selected_Source_and_metadata_pins']+[gen_pin])
    science = plan['scientific_input_current7_pins']; library = plan['actual_kernel_library_pin']
    need(len(science)==6 and {p['path'] for p in science}=={plan[k]['path'] for k in
        ('observed_final55_SQLite_pin','observed_final55_pool_pin','current_original_radial_track_pin',
         'current_axial_track_pin','compact_native_vector_pin','current_original_A1_native_archive_pin')}, 'exact six scientific live roles')
    binary_paths = {p['path'] for p in science+[library]}
    union = unique(selected+plan['source_dependency_pins']+plan['explicit_cumulative_metadata_file_pins']
        +plan['complete_kernel_source_pins']+[r['pin'] for r in plan['explicit_import_bindings']])
    need(EXCEPTIONS.issubset({p['path'] for p in union}) and not RETIRED.intersection(p['path'] for p in union), 'complete eleven exceptions; old pair excluded')
    records = []
    for p in union:
        if p['path'] in EXCEPTIONS or p['path'] in binary_paths:
            current(p); records.append(dict(full_pin=p,verification='CURRENT7_ONLY_TWICE_NO_BODY_OPEN_OR_HASH'))
        else:
            eof(p); records.append(dict(full_pin=p,verification='FULL_EOF_SHA_AND_CURRENT7_TWICE'))
    roots = plan['complete_joint_roots']
    need(len(roots)==57 and roots[:-1]==plan['inherited_complete_joint_roots'] and len(roots[:-1])==56
        and roots[-1:]==[str(OUT)] and str(TOP) in roots[:-1] and len(set(roots))==57
        and all(not Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b), 'inherited failed56/new57 disjoint ledger without reset')
    need(plan['planned_actual_output_root']==str(OUT) and not os.path.lexists(OUT), 'fresh unexecuted control OUT')
    need(plan['original_caps']==CAPS and plan['new_control_reserved_bytes']==291566880
        and plan['whole_white_cache_payload_bytes']==260858880
        and sum(plan['control_reservation_components'].values())==291566880, 'unchanged caps/cache/output reserve')
    need(plan['physical_checks']=={'primitive':1e-10,'cell':1e-10,'global':1e-10,'geometry':5e-12,'represented_width':5e-12,'white':5e-12}
        and plan['offset_order']==32 and plan['working_group_chunk']==1
        and plan['boundary_model']=='GEOMETRIC_LAYER_LOCAL_WHITE', 'original unfitted physical ceilings')
    for obj in (ready,plan,author,inverse):
        for k in FALSE:
            if k in obj: need(obj[k] is False, 'Source cannot grant '+k)
    need(plan['actual_control_report_pin'] is None and plan['protected_formal_case_or_inputs_rewritten'] is False
        and plan['current_SPH_MASK_context_applied'] is False and plan['temperature_interpolation_replayed'] is False, 'component-only current raw totals')
    for p in science+[library]: current(p)
    cap = plan['compact_capture_prerequisite_pins']; ret = plan['literal2_retirement_prerequisite_pins']
    ch = read(cap['host']); cc = read(cap['child']); cp = read(cap['post'])
    need(ch['schema']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_GUARDED_REPORT_V1'
        and ch['status']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_26R4_104B_CLOSED0_ONLY'
        and ch['failure'] is None and ch.get('after_check_error') is None and ch['secondary_failures']==[]
        and len(ch['records'])==1 and ch['records'][0]['status']=='PASS'
        and ch['final_report_resource_check_passed'] is True and ch['actual_evidence']==cc, 'actual narrow capture host/child')
    need(cc['schema']=='ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE_V1'
        and cc['status']=='A1_NATIVE_26_REAL32_WORDS_104B_CAPTURE_CLOSED0_ONLY'
        and cc['compact_vector_full_pin']==plan['compact_native_vector_pin']
        and cc['captured_original_record_count']==4 and cc['captured_REAL32_words']==26
        and cc['captured_bytes']==104 and cc['original_small_vectors_called_unchanged'] is True, 'actual four-record104B scope')
    for r,(name,n,at) in zip(cc['native_vector_record_descriptors'],
            [('XMU$MCCG',4,0),('ZMU$MCCG',4,16),('WZMU$MCCG',4,32),('V$MCCG',14,48)]):
        need(r['name']==name and r['path']==['TRACK',1,name] and r['kind']==2 and r['words']==n
            and r['offset_bytes']==at and r['captured_bytes']==4*n and r['captured_word_encoding']=='little_endian_REAL32'
            and r['native_payload_sha256']==r['captured_payload_sha256']==r['original_native_row']['native_payload_sha256'], 'exact captured original descriptors')
    need(len(cc['native_vector_record_descriptors'])==4, 'exact four vector descriptors')
    closed(read(cap['root_tools']),'actual_terminal_return',cap['host'],'report_pin')
    need(cp['schema']==plan['capture_post_schema'] and cp['status']==plan['capture_post_status']
        and cp['status'].startswith('PASS') and cp['failure'] is None
        and all(contains(cp,cap[k]) for k in ('host','child','root_tools')), 'actual capture independent post')
    closed(read(cap['post_tools']),'actual_review_return',cap['post'],'review_pin')
    rr = read(ret['receipt']); rp = read(ret['post']); targets = [cc['original_A1_SQLite_pin'],cc['original_A1_pool_pin']]
    need(rr['schema']=='LITERAL2_COMPLETED_A1_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'
        and rr['mode']=='execute' and rr['status']=='RETIRED_EXACT_LITERAL2_COMPLETED_A1_COMPARE_SPOOLS_ONLY'
        and rr['failure'] is None and rr['exact_target_pins']==targets and rr['actual_released_pins']==targets
        and rr['actual_released_bytes']==202708660 and rr['files_deleted'] is True
        and {p['path'] for p in targets}==RETIRED and all(not os.path.lexists(p['path']) for p in targets), 'actual exact literal2 retirement')
    for k,p in [('capture_host_pin',cap['host']),('capture_child_pin',cap['child']),('capture_post_pin',cap['post']),
        ('capture_root_tools_pin',cap['root_tools']),('capture_post_tools_pin',cap['post_tools']),('compact_vector_full_pin',plan['compact_native_vector_pin'])]:
        need(rr[k]==p, 'same actual capture/retirement chain')
    need(rr['complete_joint_roots']==plan['capture_retirement_complete_joint_roots'] and rr['fresh_ps_lsof_checks_passed'] is True, 'actual same54 retirement process proof')
    closed(read(ret['root_tools']),'actual_terminal_return',ret['receipt'],'receipt_pin')
    need(rp['schema']=='INDEPENDENT_ACTUAL_LITERAL2_A1_RETIREMENT_METADATA_POSTVERIFY_V1'
        and rp['schema']==plan['retirement_post_schema'] and rp['status']==plan['retirement_post_status']
        and rp['status']=='PASS_ACTUAL_EXACT_LITERAL2_A1_RETIREMENT_202708660B_METADATA_ONLY'
        and rp['failure'] is None and all(contains(rp,p) for p in (ret['receipt'],ret['root_tools'],cap['post'],plan['compact_native_vector_pin'])), 'actual corrected retirement independent post')
    closed(read(ret['post_tools']),'actual_review_return',ret['post'],'review_pin')
    for obj in (ch,cc,cp,rr,rp):
        for k in ('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'):
            if k in obj: need(obj[k] is False, 'prerequisite narrow scope')
    need(Path(cap['post']['path']).is_relative_to(CAP/'v2/actual_capture_postverify_20261015/corrected_process_access_v2')
        and Path(ret['post']['path']).is_relative_to(CAP/'v4/actual_retirement_postverify_20261015/corrected_current7_schema_v2'), 'actual corrected own routing')
    kernel = read(plan['actual_kernel_origin_pin']); build = read(plan['actual_kernel_build_report_pin'])
    need(kernel['schema']=='ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN_V1'
        and kernel['library_pin']==library and kernel['complete_source_pins']==plan['complete_kernel_source_pins']
        and kernel['actual_build_report_pin']==plan['actual_kernel_build_report_pin'] and kernel['original_caps']==CAPS
        and build['failure'] is None and build.get('after_check_error') is None
        and all(r['status']=='PASS' for r in build['records'])
        and kernel['actual_command'] in [r['command'] for r in build['records']], 'actual existing kernel Origin/build only')
    compiler = kernel['compiler_pin']
    need(compiler['path']=='/usr/bin/clang++' and compiler['identity'][3]==78, 'system compiler role preserved inside origin, no ordinary-data rule')
    source_text = {}
    for p in author['source_pins']:
        raw = Path(p['path']).read_bytes(); ast.parse(raw,filename=p['path']); source_text[Path(p['path']).name] = raw
    operator = source_text['current_formal_full370_ray_operator.py']
    need(operator==Path(plan['original_mathematical_operator_Source_pin']['path']).read_bytes()
        and plan['mathematical_operator_Source_copy_pin']['sha256']=='731b921e0c5f64955c0f4b358b03bfbd70e88f7c1eeaf644c7ff275517ef02f5', 'whole unchanged operator')
    worker = source_text['run_full370_real_operator_control.py']; old = (TOP/'run_full370_real_operator_control.py').read_bytes()
    v4worker=(TOP/'v4/run_full370_real_operator_control.py').read_bytes()
    restored=worker
    need(len(author['worker_restore_to_v4_replacements'])==6, 'exact six Source-only lifetime/diagnostic replacement blocks')
    for edit in author['worker_restore_to_v4_replacements']:
        candidate=bytes.fromhex(edit['candidate_bytes_hex']); original=bytes.fromhex(edit['original_bytes_hex'])
        need(restored.count(candidate)==1, 'exact single Source block for inverse')
        restored=restored.replace(candidate,original,1)
    need(restored==v4worker, 'complete lifetime/diagnostic inverse restores whole v4 worker')
    i=old.index(b'    angles,angle_rows=helpers.small_vectors('); j=old.index(b'    support=sys.modules',i)
    a=restored.index(b'    # New actual capture preserves'); b=restored.index(b'    support=sys.modules',a)
    need(restored[:a]+old[i:j]+restored[b:]==old and restored==(TOP/'v2/run_full370_real_operator_control.py').read_bytes(), 'compact-input-only whole worker inverse to original v1')
    def definition(raw,name):
        text=raw.decode('utf-8'); tree=ast.parse(text)
        return next(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    need(all(definition(worker,n)==definition(v4worker,n) for n in ('require','digest','relative','fixture')), 'four numeric/fixture functions whole bytes unchanged')
    need(inverse['whole_v5_to_v4_lifetime_and_diagnostic_inverse'] is True
        and inverse['numeric_control_functions_whole_equal'] is True, 'actual inverse proof metadata agrees')
    text=worker.decode('utf-8')
    for token in ('original_budget=helpers.Budget()', 'started=original_budget.started',
        'return self.inner.started', 'try:return self.inner.check()',
        'original_class.__bases__==(object,)', 'self.failure_checkpoint_attempted=True',
        "with self.path.open('xb')", "len(raw)<=8192", 'ORIGINAL_BUDGET_CHECK_INVOCATIONS_ONLY_NOT_NATIVE_ACTIONS'):
        need(token in text, 'original Budget delegate/checkpoint Source contract')
    need(text.count('try:return self.inner.check()')==1 and text.count('helpers.Budget()')==1
        and 'self.inner.started=' not in text and 'self.inner.check=' not in text,
        'one original Budget; no original check or clock mutation')
    diagnostic=next(n for n in ast.parse(text).body if isinstance(n,ast.ClassDef) and n.name=='BoundedBudgetDiagnostic')
    checker=next(n for n in diagnostic.body if isinstance(n,ast.FunctionDef) and n.name=='check')
    original_try=next(n for n in checker.body if isinstance(n,ast.Try))
    need(isinstance(original_try.body[0],ast.Return) and len(original_try.handlers)==1
        and isinstance(original_try.handlers[0].body[-1],ast.Raise)
        and original_try.handlers[0].body[-1].exc is None, 'original check unconditionally delegated; original exception bare-reraised')
    need(not any(isinstance(n,(ast.For,ast.While)) for n in ast.walk(checker)), 'no diagnostic throttle loop')
    need(text.index("budget.set_phase('SOURCE_POSITIVITY')") < text.index('source_min>0')
        < text.index('validated_fixture_digest=digest(coefficient)') < text.index('del coefficient,q')
        < text.index('operator.prepare_white()') < text.index("budget.set_phase('SOURCE_RECREATE')")
        < text.index("digest(coefficient)==validated_fixture_digest") < text.index('operator.apply(coefficient)'),
        'original positivity/parity before white, digest retained, release and identical recreation before apply')
    need(plan['bounded_original_Budget_failure_checkpoint_maximum_bytes']==8192
        and plan['budget_diagnostic_count_scope']=='CHECK_INVOCATIONS_ONLY_NOT_NATIVE_ACTIONS'
        and plan['no_Runtime_or_RSS_fit_inferred'] is True and author['runtime_or_RSS_fit_proved'] is False,
        'diagnostics cannot grant runtime fit or native action counts')
    need(Path(inverse['whole_original_v6_helper_copy_pin']['path']).read_bytes()
        ==Path(inverse['whole_original_v6_helper_provenance_pin']['path']).read_bytes(), 'whole original helper copy')
    tree=ast.parse(worker); calls=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
    need(calls.count('prepare_white')==1 and calls.count('apply')==1, 'one preparation/one apply literal Source calls')
    for token in (b'11364',b'363648',b'181824',b'source_min>0',b'fixture()',b'authority.KernelBinding',
                  b'unfitted_physical_white_relative64',b'signed=np.stack([-end[0],end[1]])',b'NO49FACE_PROFILE'):
        need(token in worker, 'complete original fixture/coverage/white/two-end Source assertion')
    guard=source_text['run_guarded_full370_real_operator_control.py']
    for token in (b'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)',b'runner.execute(',b',command,600)',
                  b'peak<512*2**20',b'time.monotonic()-started<1800',b"len(runner.records)==1",b"len(roots)==57"):
        need(token in guard, 'original owning guard/caps/one child Source')
    writer=source_text['write_once_full370_real_operator_control_SF_HF_CLI.py']
    for token in (b"receipt.open('xb')",b"old['argv'][:11]",b'len(argv)==24',b"'actual_Source_preparation_return'",b"'actual_review_return'",b'FAILED_ONCE_SOURCE_PUBLICATION_NO_RETRY'):
        need(token in writer, 'once Source publication/GEN/peer0/original24 recipe')
    prior_pins=plan['prior_fullv4_failed_evidence_pins']
    prior_map={p['path']:p for p in prior_pins}
    prior_base=TOP/'v4'; prior_out=ART/'axial-material-current-full370-real-operator-control-20261015-v2'
    def prior_doc(q):return read(prior_map[str(q)])
    prior_plan=read(plan['prior_fullv4_failed_plan_pin'])
    need(roots[:-1]==prior_plan['complete_joint_roots'] and plan['capture_retirement_complete_joint_roots']==rr['complete_joint_roots']
        and len(plan['capture_retirement_complete_joint_roots'])==54 and plan['prior_fullv4_original_Root_exit_code']==1,
        'no reset: capture54 retained inside original failed56 then fresh57')
    prior_root=prior_doc(prior_base/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json'); prior_terminal=prior_root['actual_terminal_return']
    need(prior_root['observed_closed'] is True and type(prior_root['original_integer_exit_code']) is int
        and prior_root['original_integer_exit_code']==1 and type(prior_terminal['exit_code']) is int
        and prior_terminal['exit_code']==1 and prior_terminal.get('session_id') is None, 'original actual Root1 preserved')
    prior_host_pin=prior_map[str(prior_out/'Root_actual_full370_real_operator_control_summary.json')]
    prior_host=read(prior_host_pin); prior_watch=prior_doc(prior_out/'control/full370_real_operator.watchdog.json')
    need(prior_host['status']=='ACTUAL_FULL370_REAL_OPERATOR_CONTROL_FAILED_UNQUALIFIED'
        and len(prior_host['records'])==1 and prior_host['records'][0]['status']=='FAILED'
        and prior_host['actual_control_results'] is None and prior_host['final_report_resource_check_passed'] is True
        and prior_host['after_check_error'] is None and prior_watch['returncode']==1
        and prior_watch['limit_failure'] is None and prior_watch['liveness_group_cleanup'] is True,
        'original failed child1/watchdog facts, no actual0 conversion')
    need(prior_doc(prior_out/'operator-control/stages.json')['stages']==prior_host['records']
        and 'original childSELF512/stage600' in Path(prior_map[str(prior_out/'control/full370_real_operator.log')]['path']).read_text(),
        'original failed stage and child guard log retained')
    need(not os.path.lexists(prior_out/'control/ACTUAL_FULL370_REAL_OPERATOR_CONTROL.json')
        and not any(p.is_file() for p in (prior_out/'control/white_cache').glob('*')), 'prior child report/cache still absent')
    facts_pin=plan['prior_fullv4_failure_facts_post_pin']; facts=read(facts_pin)
    facts_tools=prior_doc(prior_base/'actual_failure_metadata_assessment_20261015/TRUE_TOOL_RETURNS.json')
    closed(facts_tools,'actual_review_return',facts_pin,'review_pin')
    need(facts['status']=='PASS_FAILURE_FACTS_ONLY' and facts['actual_Root_original_integer_exit_code']==1
        and facts['actual_child_original_integer_exit_code']==1 and facts['actual_host_report_pin']==prior_host_pin
        and facts['actual_Root_true_tools_pin']==prior_map[str(prior_base/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')], 'failure assessment0 asserts failure facts only')
    prior_ready_pin=prior_map[str(prior_base/'SOURCE_REVIEW_READY.json')]
    closed(prior_doc(prior_base/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json'),'actual_Source_preparation_return',prior_ready_pin,'ready_pin')
    prior_sf=prior_doc(prior_base/'COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE.json')
    closed(read(prior_sf['same_round_Source_tools_pin']),'actual_review_return',prior_sf['same_round_Source_review_pin'],'review_pin')
    prior_receipt=prior_doc(prior_base/'FINAL_PUBLICATION_RECEIPT.json')
    closed(prior_doc(prior_base/'ROOT_FINAL_PUBLICATION_TRUE_TOOL_RETURNS.json'),'actual_publication_return',prior_receipt['CLI_pin'],'CLI_pin')
    light=prior_doc(prior_base/'ROOT_FINAL_LIGHT_REVIEW_20261015.json'); light_tools=prior_doc(prior_base/'ROOT_FINAL_LIGHT_TRUE_TOOL_RETURNS_20261015.json')
    light_return=light_tools['actual_light_return']
    need(light['status'].startswith('PASS') and light['failure'] is None and light_tools['observed_closed'] is True
        and type(light_tools['original_integer_exit_code']) is int and light_tools['original_integer_exit_code']==0
        and type(light_return['exit_code']) is int and light_return['exit_code']==0 and light_return.get('session_id') is None
        and strict(light_return['output'])['status']==light['status'], 'original LIGHT0 status-only return preserved')
    for p in prior_pins:need(p in union, 'complete original failure history in selected union')
    for p in union:
        if p['path'] not in EXCEPTIONS and p['path'] not in binary_paths:eof(p)
        else:current(p)
    for p in union+science+[library]: current(p)
    need(not os.path.lexists(OUT), 'output remains absent at review completion')
    hashed=[r['full_pin'] for r in records if r['verification']=='FULL_EOF_SHA_AND_CURRENT7_TWICE']
    report=dict(schema='INDEPENDENT_FULL370_REAL_OPERATOR_V5_SOURCE_METADATA_REVIEW_V1',
        status='PASS_SOURCE_METADATA_SCOPE_WITH_SCIENTIFIC_DOCUMENT_CURRENT7_ONLY',failure=None,
        metadata_only=True,source_only=True,reviewer_source_freeze_pin=freeze_pin,reviewer_source_pin=freeze['reviewer_source_pin'],
        actual_ready_pin=ready_pin,actual_plan_pin=ready['plan_pin'],actual_generation_tools_pin=gen_pin,
        source_preparation_actual_integer_exit_code=0,selected_source_and_metadata_full_pins=selected,
        complete_source_metadata_and_live_pin_union=union,complete_union_verification_records=records,
        selected_source_metadata_pin_count=len(selected),complete_union_pin_count=len(union),
        fullEOF_Source_report_metadata_pin_count=len(hashed),eleven_scientific_extraction_document_pins=[p for p in union if p['path'] in EXCEPTIONS],
        scientific_extraction_document_count=11,scientific_extraction_documents_current7_verified_twice=True,
        scientific_extraction_document_bodies_opened_hashed_or_decoded=False,
        actual_parent_current_science_input_fullPF_authority_retained=True,
        all_selected_pins_new_fullEOF_claimed=False,scientific_input_current7_pins=science,
        scientific_input_current7_verified_twice=True,existing_kernel_library_current7_only_pin=library,
        kernel_library_body_opened_or_hashed=False,actual_kernel_origin_pin=plan['actual_kernel_origin_pin'],
        actual_kernel_build_report_pin=plan['actual_kernel_build_report_pin'],compiler_pin_retained_as_origin_metadata=compiler,
        complete_kernel_source_pins=plan['complete_kernel_source_pins'],compact_capture_prerequisite_pins=cap,literal2_retirement_prerequisite_pins=ret,
        whole_operator_bytes_equal_original=True,compact_input_only_whole_worker_reverse_equals_original=True,
        whole_original_small_vectors_helper_copy_equal=True,six_Source_AST_only_syntax_passed=True,
        direct_existing_KernelBinding_only=True,original_24_argument_once_publication_recipe_retained=True,
        original_caps=CAPS,complete_joint_roots=roots,full_control_reserved_bytes=291566880,
        fresh_runtime_capacity_qualified=False,runtime_or_SELF_RSS_fit_proved=False,planned_actual_output_root=str(OUT),
        planned_actual_output_root_absent=True,complete_original_tracks=11364,actions_per_group_sweep=181824,
        apply_action_calls=363648,groups=370,axial_cells=48,retained_moments=9,prepare_white_Source_calls=1,apply_Source_calls=1,
        independent_source_angular_positivity_assertion_retained=True,signed_current_scope='TWO_END_FACES_ONLY_NO49FACE_PROFILE',
        physical_checks=plan['physical_checks'],unfitted_physical_white_global_ceiling=1e-10,
        original_failures_and_frozen_v1_v2_v3_v4_preserved=True, prior_fullv4_Root_integer_exit_code=1, prior_fullv4_child_integer_exit_code=1, prior_fullv4_failure_facts_post_integer_exit_code=0, whole_v5_to_v4_worker_inverse_verified=True, numeric_control_functions_whole_equal=True, original_Budget_check_delegated_every_time=True, original_Budget_started_not_reset=True, bounded_failure_checkpoint_maximum_bytes=8192, fixture_recreated_full_digest_equality_assertion_retained=True, diagnostic_count_scope='CHECK_INVOCATIONS_NOT_NATIVE_ACTIONS',business_executed=False,numerical_executed=False,
        native_executed=False,compiler_executed=False,files_deleted=False,candidate_Source_or_helpers_imported=False,
        scientific_body_opened_hashed_or_decoded=False,reviewer_elapsed_seconds=time.monotonic()-STARTED,**FALSE)
    target=HERE/'REVIEW.json'
    with target.open('x') as f: json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    rp=fresh_pin(target)
    for p in union+science+[library]: current(p)
    print(json.dumps(dict(status=report['status'],review_pin=rp,business_executed=False,numerical_executed=False,
        native_executed=False,compiler_executed=False,files_deleted=False,**FALSE)),flush=True)

if __name__=='__main__':
    main()

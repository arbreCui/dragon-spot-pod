"""Exact five closed nonfinal old intermediates; Source only, no MF or unlink."""
import ast
import importlib.util
import json
import os
import stat
from pathlib import Path

R = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD = R / 'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014'
OUT = R / 'storage_release_literal5_closed_old_map007011_source_v1_20261014'
OLDLABEL = 'LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE'
LABEL = 'LITERAL5_CLOSED_OLD_MAP007011'
spec = importlib.util.spec_from_file_location('original_source_helpers_for_exact_five', R / 'prepare_literal2_old_map005006_before_aggregate_source_only_v2_20261014.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
pin, read, write, identity = h.pin, h.read, h.write, h.identity


def main():
    if OUT.exists():
        raise RuntimeError('fresh exact Source namespace')
    source = (OLD / h.h.NAMES[0]).read_text()
    current = source
    changes = []

    def node(name):
        matches = [n for n in ast.parse(current).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name]
        if len(matches) != 1:
            raise RuntimeError('one exact assignment ' + name)
        return matches[0]

    def const(name):
        return ast.literal_eval(node(name).value)

    def change(old, new):
        nonlocal current
        if current.count(old) != 1:
            raise RuntimeError('one precise Source splice')
        current = current.replace(old, new, 1)
        changes.append(dict(before=old, after=new))

    def assign(name, value):
        change(ast.get_source_segment(current, node(name)), name + '=' + repr(value))

    def fn(name):
        return ast.get_source_segment(current, next(n for n in ast.parse(current).body if isinstance(n, ast.FunctionDef) and n.name == name))

    oldsfpin = pin(OLD / 'COMPLETE_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_SOURCE_FREEZE.json')
    sf = read(oldsfpin)
    mfpin = pin(OLD / 'EXACT_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_MANIFEST.json')
    mother = read(mfpin)
    rows = mother['current_protected_full_EOF_pins']
    if len(rows) != 9771 or len(mother['target_full_EOF_pins']) != 2:
        raise RuntimeError('real mother9771 and original exact2 declarations')
    previous_targets = mother['target_full_EOF_pins']
    postpin = pin(R / 'independent_literal2_old_map005006_before_aggregate_actual_exact_release_postverify_20261014/REVIEW.json')
    toolpin = pin(Path(postpin['path']).parent / 'TRUE_TOOL_RETURNS.json')
    post = read(postpin)
    receiptpin = post['actual_release_receipt_pin']
    receipt = read(receiptpin)
    if receipt['deleted_files'] != 2 or receipt['logical_bytes_released'] != 463397752 or any(os.path.lexists(p['path']) for p in previous_targets):
        raise RuntimeError('actual exact2 gone, not missing-current relaxation')
    oma = dict(const('OLD_MAP_AUTHORITY'))
    root = Path(oma['run_status_pin']['path']).parent
    targets, results = [], []
    for number in range(7, 12):
        path = root / ('map' + format(number, '03d')) / 'projected_proposal.xsm'
        s = path.lstat()
        rp = pin(path.parent / 'result.json')
        value = read(rp)
        sha = value['sha256']['projected_proposal.xsm']
        if s.st_uid != os.getuid() or s.st_nlink != 1 or not stat.S_ISREG(s.st_mode) or s.st_size != 231698876 or value['classification'] != 'SEALED_STAGE_OUTPUTS':
            raise RuntimeError('exact old ordinary intermediate with sealed SHA')
        targets.append(dict(path=str(path), sha256=sha, size_bytes=s.st_size, identity=identity(s)))
        results.append(rp)
    targetpaths = {p['path'] for p in targets}
    if targetpaths & {p['path'] for p in rows} or len(targetpaths) != 5 or len({tuple(p['identity'][:2]) for p in targets}) != 5:
        raise RuntimeError('five distinct noncurrent targets disjoint mother9771')
    before = h.inventory([Path(p['path']).parent for p in targets])
    oma['target_result_pins'] = results
    hist = dict(const('HISTORICAL_PINS'))
    hist.update(previous9771_manifest=mfpin, previous_exact2_Source_freeze=oldsfpin,
                completed_exact2_post=postpin, completed_exact2_post_tools=toolpin,
                completed_exact2_receipt=receiptpin, completed_exact2_Root_tools=post['actual_Root_true_tool_pin'])
    for i, p in enumerate(results):
        hist['map007011_result_' + str(i)] = p
    aggregate_path = Path('/Users/wen/spot/validation/artifacts/axial-material-current-first-A-complete-aggregate-eight-roots-20261014-v1/Root_actual_current_material_evidence_summary.json')
    aggregate_pin = pin(aggregate_path)
    aggregate = read(aggregate_pin)
    aggregate_raw_pin = pin(R / 'ROOT_ACTUAL_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_TRUE_TOOL_RETURNS_20261014.json')
    hist.update(actual_first_aggregate_report=aggregate_pin, actual_first_aggregate_Root_tools=aggregate_raw_pin)
    for name, value in [('HISTORICAL_PINS', hist), ('TARGET_SELECTED_PINS', targets), ('HISTORICAL_TARGET_INDICES', []), ('BASELINE_OWNED_INVENTORIES', before), ('OWNER_FILE_COUNT', len(before['ordinary_file_identities'])), ('OWNER_DIRECTORY_COUNT', len(before['directory_identities'])), ('BYTES', 1158494380), ('OLD_MAP_AUTHORITY', oma)]:
        assign(name, value)
    change(ast.get_source_segment(current, node('BRANCHES')), 'BRANCHES=[' + ','.join('Path(' + repr(str(Path(p['path']).parent)) + ')' for p in targets) + ']')
    change(ast.get_source_segment(current, node('RECEIPTS')), "RECEIPTS=REC/'storage_release_literal5_closed_old_map007011_actual_receipts_20261014'\nCOMPLETED_EXACT2_MAP_RETIREMENT=" + repr(dict(post_pin=postpin, post_tools_pin=toolpin, receipt_pin=receiptpin, Root_tools_pin=post['actual_Root_true_tool_pin'], original_target_pins=previous_targets)) + '\nCLOSED_FIRST_AGGREGATE=' + repr(dict(report_pin=aggregate_pin, Root_tools_pin=aggregate_raw_pin)))
    assign('SF', "__placeholder__")
    change("SF='__placeholder__'", "SF=PKG/'COMPLETE_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_FREEZE.json'")
    change(ast.get_source_segment(current, node('FINAL')), "FINAL=PKG/'EXACT_LITERAL5_CLOSED_OLD_MAP007011_MANIFEST.json'")
    f = fn('source_gate')
    change(f, f.replace(OLDLABEL, LABEL).replace('len(TARGETS)!=2', 'len(TARGETS)!=5').replace('len(TARGET_PATHS)!=2', 'len(TARGET_PATHS)!=5'))
    f = fn('disjoint')
    change(f, f.replace('len(TARGETS)!=2', 'len(TARGETS)!=5').replace('len(TARGET_PATHS)!=2', 'len(TARGET_PATHS)!=5').replace("len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=2", "len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=5"))
    f = fn('current_protection')
    z = f.replace("HISTORICAL_PINS['previous9626_manifest']", "HISTORICAL_PINS['previous9771_manifest']")
    a = " if len(rows)!=9626 or HISTORICAL_TARGET_INDICES!=[5948,5949]or [b.norm(rows[i])for i in HISTORICAL_TARGET_INDICES]!=RELEASED_A10_LIBRARY_PINS or {p['path']for p in rows}&TARGET_PATHS:raise RuntimeError('exact mother9626 releasedlibrary2 history and noncurrent map2')"
    b = " if len(rows)!=9771 or HISTORICAL_TARGET_INDICES!=[]or {p['path']for p in rows}&(TARGET_PATHS|{p['path']for p in COMPLETED_EXACT2_MAP_RETIREMENT['original_target_pins']}):raise RuntimeError('all mother9771 current rows preserved; old exact2 only historical declarations')"
    if a not in z:
        raise RuntimeError('one mother-row role gate')
    z = z.replace(a, b, 1).replace('all_previous9626_rows_', 'all_previous9771_rows_').replace(" if len(table)!=9624:raise RuntimeError('all other9624 mother rows kept')", " if len(table)!=9771:raise RuntimeError('all9771 mother current rows kept')")
    z = z.replace("len(retained)!=OWNER_FILE_COUNT-2", "len(retained)!=OWNER_FILE_COUNT-5").replace('all_other_map005006_files_kept', 'all_other_map007011_files_kept').replace('only two selected intermediate files retired', 'only five selected intermediate files retired')
    insert = " for q in ROLE_KEEP_PINS:add(q,'all_original_scientific9_current')"
    extra = " d=read(CLOSED_FIRST_AGGREGATE['report_pin'])\n for q in list(CLOSED_FIRST_AGGREGATE.values())+d['fixed_current_pins']+d['complete_output_pins']:add(q,'all_actual_first_aggregate_outputs_retained_no_math_qualification')\n for q in [COMPLETED_EXACT2_MAP_RETIREMENT[k]for k in('post_pin','post_tools_pin','receipt_pin','Root_tools_pin')]:add(q,'actual_exact2_release_documents_retained')\n"
    if insert not in z:
        raise RuntimeError('one aggregate current preservation insertion')
    z = z.replace(insert, extra + insert, 1)
    z = z.replace('previous_protected_count=9626,exact_previous_MF_indices_migrated_to_history=[5948,5949],all_other9624_PF_rows_data_retained=True', 'previous_protected_count=9771,exact_previous_MF_indices_migrated_to_history=[],all9771_PF_rows_data_retained=True,exact_already_released_map005006_historical_declarations=[dict(original_body_pin=q,current_pin=None)for q in COMPLETED_EXACT2_MAP_RETIREMENT[\'original_target_pins\']]')
    z = z.replace('explicit_exact2_historical_body_declarations', 'explicit_exact5_historical_body_declarations').replace('EXACT_TWO_CLOSED_OLD_MAP005006_INTERMEDIATES_HISTORICAL', 'EXACT_FIVE_CLOSED_OLD_MAP007011_INTERMEDIATES_HISTORICAL')
    change(f, z)
    additional = '''def completed_exact2_and_first_aggregate_proof():
 c=COMPLETED_EXACT2_MAP_RETIREMENT;p=read(c['post_pin']);t=read(c['post_tools_pin']);r=read(c['receipt_pin']);rt=read(c['Root_tools_pin'])
 if p['schema']!='INDEPENDENT_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_EXACT_RELEASE_POSTVERIFICATION'or p['failure']is not None or p['actual_release_receipt_pin']!=c['receipt_pin']or p['actual_Root_true_tool_pin']!=c['Root_tools_pin']or any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','deletion_executed_by_reviewer')):raise RuntimeError('strict true exact2 release independent post')
 for key in('actual_review_return','actual_postverification_return'):
  q=t[key]
  if type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or b.norm(json.loads(q['output'].strip().splitlines()[-1])['review_pin'])!=c['post_pin']:raise RuntimeError('exact2 genuine independent post0')
 if rt['observed_closed']is not True or type(rt['original_integer_exit_code'])is not int or rt['original_integer_exit_code']!=0 or r['deleted_files']!=2 or r['logical_bytes_released']!=463397752 or any(os.path.lexists(q['path'])for q in c['original_target_pins']):raise RuntimeError('exact2 actual terminal release, historical targets only')
 a=CLOSED_FIRST_AGGREGATE;d=read(a['report_pin']);t=read(a['Root_tools_pin'])
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or d['operation']!='aggregate'or d['failure']is not None or d['after_check_error']is not None or d['actual_intentional_exit2_normal_closure']is not True or len(d['complete_output_pins'])!=13:raise RuntimeError('actual first aggregate closed evidence only; all outputs retained')
 return dict(completed_exact2_retirement=c,first_actual_aggregate=a,physics_qualified=False)
'''
    change(fn('closed_proofs'), fn('closed_proofs').replace('current_completion_and_extraction_closed_proof()]', 'current_completion_and_extraction_closed_proof(),completed_exact2_and_first_aggregate_proof()]') + '\n\n' + additional.rstrip())
    funcs = lambda s: {n.name: ast.get_source_segment(s, n) for n in ast.parse(s).body if isinstance(n, ast.FunctionDef)}
    low = ['_base', 'external', 'inventory', 'receipt_pin', 'update_owned', 'budget', 'review_gate']
    if any(funcs(source)[n] != funcs(current)[n] for n in low) or 's.st_nlink!=1' not in fn('disjoint'):
        raise RuntimeError('seven low methods and real single-link guard unchanged')
    ast.parse(current)
    others = []
    for name in h.h.NAMES[1:]:
        a = (OLD / name).read_text()
        z = a.replace(OLDLABEL, LABEL).replace('target_count=2', 'target_count=5').replace("m['target_count']!=2", "m['target_count']!=5").replace("before['regular_files']-after['regular_files']!=2", "before['regular_files']-after['regular_files']!=5").replace('deleted_files=2', 'deleted_files=5')
        ast.parse(z)
        others.append((name, a, z))
    a, z = others[1][1:]
    start = '                os.unlink(target.name,dir_fd=fd)'
    end = "        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)"
    if a[a.index(start):a.index(end)] != z[z.index(start):z.index(end)] or "after['original_initial_reserve_admitted']is not True" not in z:
        raise RuntimeError('original unlink/truth-receipt/dirfsync/FirstFailure and full actual reserve unchanged')
    OUT.mkdir()
    write(OUT / h.h.NAMES[0], current)
    for name, _, z in others:
        write(OUT / name, z)
    plan = write(OUT / 'EXACT_LITERAL5_CLOSED_OLD_MAP007011_ROLE_SOURCE_PLAN.json', dict(schema='EXACT_LITERAL5_CLOSED_OLD_MAP007011_ROLE_SOURCE_PLAN_V1', source_only=True, target_count=5, target_bytes=1158494380, literal5_fullpins=targets, mother9771_manifest_pin=mfpin, all9771_mother_rows_kept=True, no_current_MF_rows_retired=True, completed_exact2_maps_only_historical=previous_targets, complete_owner_inventory=before, owner_file_count=len(before['ordinary_file_identities']), owner_directory_count=len(before['directory_identities']), retained_other_file_count=len(before['ordinary_file_identities'])-5, first_actual_aggregate_outputs_retained=True, actual_first_aggregate_report_pin=aggregate_pin, original_caps=sf['original_caps'], future_actual_manifest_pin=None, future_actual_release_receipt_pin=None, compiler_executed=False, numerical_executed=False, business_executed=False, deletion_executed=False))
    entries = [dict(predecessor_pin=pin(OLD / h.h.NAMES[0]), candidate_pin=pin(OUT / h.h.NAMES[0]), changes=changes)] + [dict(predecessor_pin=pin(OLD / n), candidate_pin=pin(OUT / n), changes=[dict(before=a, after=z)]) for n, a, z in others]
    for e in entries:
        back = Path(e['candidate_pin']['path']).read_text()
        for c in reversed(e['changes']):
            if back.count(c['after']) != 1:
                raise RuntimeError('one reverse exact splice')
            back = back.replace(c['after'], c['before'], 1)
        if back.encode() != Path(e['predecessor_pin']['path']).read_bytes():
            raise RuntimeError('complete three-file wholebyte inverse')
    inverse = write(OUT / 'COMPLETE_EXACT2_TO_EXACT5_OLD_MAP007011_WHOLE_BYTE_INVERSE.json', dict(schema='COMPLETE_EXACT2_TO_EXACT5_OLD_MAP007011_WHOLE_BYTE_INVERSE_V1', entries=entries, seven_lowlevel_methods_wholebytes_equal=low, unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_equal=True, actor_actual_after_fullfresh2True_original=True, source_only=True))
    sf.update(schema='COMPLETE_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_ONLY_FREEZE_V1', literal11_fullpins=targets, literal2_fullpins=targets, literal5_fullpins=targets, target_count=5, target_bytes=1158494380, historical_evidence_pins=hist, closed_old_map_authority=oma, Source_pins=[pin(OUT / n) for n in h.h.NAMES], exact_role_plan_pin=plan, strict_low_level_Source_provenance_pin=inverse, Source_preparer_pin=pin(__file__), predecessor_Source_freeze_pin=oldsfpin, future_actual_manifest_pin=None, future_actual_release_receipt_pin=None, future_original_current_fullfresh2_budget_admission=None)
    sfpin = write(OUT / 'COMPLETE_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_FREEZE.json', sf)
    print(json.dumps(dict(status='EXACT5_CLOSED_OLD_MAP007011_SOURCE_ONLY_READY_NO_MF_NO_DELETE', Source_freeze_pin=sfpin, Source_pins=sf['Source_pins'], plan_pin=plan, inverse_pin=inverse, target_count=5, target_bytes=1158494380, business_executed=False, compiler_executed=False, numerical_executed=False, deletion_executed=False)))


if __name__ == '__main__':
    main()

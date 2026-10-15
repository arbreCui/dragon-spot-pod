import ast
import hashlib
import json
import stat
from pathlib import Path

NEW = Path('/private/tmp/axmat_v25_monitor_access_complete_BUILD_UNREADY_Source_j8g_s3id')
OLD = Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
DEST = Path('/private/tmp/spot_ROOT_independent_v25_monitor_access_BUILD_namespace_Source_review_20261010')
CHANGED = {'COMPLETE_SOURCE_INVERSES.json', 'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py', 'host_and_postclose_templates/build_host.V25.UNREADY.full.py', 'host_and_postclose_templates/build_writer.V25.UNREADY.full.py'}
checks = []
pins = {}

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def read(path):
    before = identity(path)
    assert stat.S_ISREG(before[2]) and not path.is_symlink(), path
    b = path.read_bytes()
    assert identity(path) == before and len(b) == before[4], path
    pin = dict(path=str(path), sha256=hashlib.sha256(b).hexdigest(), size_bytes=len(b), identity=before)
    if str(path) in pins: assert pins[str(path)] == pin
    pins[str(path)] = pin
    return b, pin

def check(label, value):
    assert type(value) is bool and value is True, label
    checks.append(dict(label=label, passed=value))

def document(path):
    b, pin = read(path)
    return json.loads(b), pin

def package(root):
    m, mp = document(root/'MANIFEST.json')
    check(str(root)+' exact complete file names', {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} == set(m['members'])|{'MANIFEST.json'})
    check(str(root)+' exact complete directory names', {'.'}|{str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir()} == set(m['directories']))
    for k, wanted in m['directories'].items(): check('whole directory identity '+str(root/k), identity(root if k=='.' else root/k) == wanted)
    for k, wanted in m['members'].items(): check('whole member EOF SHA size 7ID '+str(root/k), read(root/k)[1] == wanted)
    return m, mp

def reverse_hunks(data, rows):
    lines = data.decode().splitlines(keepends=True)
    for h in reversed(rows):
        start, end = h['new_start0'], h['new_end0']
        assert lines[start:end] == h['new_full_lines']
        lines[start:end] = h['old_full_lines']
    return ''.join(lines).encode()

def reverse_rows(text, rows):
    for row in reversed(rows):
        assert text.count(row['new']) == row['count'], row['label']
        text = text.replace(row['new'], row['old'])
    return text

def main():
    assert not DEST.exists()
    old, oldpin = package(OLD)
    new, newpin = package(NEW)
    check('known old complete frozen manifest digest', oldpin['sha256']=='9e9a77669309071065c189ad02ee455709ca81db376de818825d99d8cf22f6e9')
    check('known new complete frozen manifest digest', newpin['sha256']=='8c99844e51761cbf00013f260d647b34fa34919e8db7b655a4340f11e6c6b4d7')
    check('exact complete original and new package sizes', len(old['members'])==38 and len(new['members'])==44 and len(old['directories'])==len(new['directories'])==4)
    check('unchanged manifest schema protocol family', new['schema']==old['schema'])
    inv, invpin = document(NEW/'V25_MONITOR_ACCESS_EXACT_BUILD_NAMESPACE_FULL_BYTE_INVERSES.json')
    check('exact mother provenance four pin', inv['original_frozen_mother_manifest_pin']==oldpin==new['original_sealed_mother_manifest_pin'])
    rows = inv['exact_namespace_transform_rows']
    role_names = {'BUILD_binder':'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py','build_host':'host_and_postclose_templates/build_host.V25.UNREADY.full.py','build_writer':'host_and_postclose_templates/build_writer.V25.UNREADY.full.py'}
    route, routepin = document(NEW/'ROOT_MONITOR_ACCESS_BUILD_NEXT_STEPS.UNREADY.json')
    namespace = route['exact_namespace_names']
    check('exact three route roles seven replacements each', set(rows)==set(role_names) and all(len(x)==7 for x in rows.values()))
    for role, name in role_names.items():
        before = read(OLD/name)[0].decode()
        expected = before
        for row in rows[role]:
            check('strict exact route '+role+' '+row['old'], namespace.get(row['old'])==row['new'] and row['count']>0 and expected.count(row['old'])==row['count'])
            expected = expected.replace(row['old'],row['new'])
        now = read(NEW/name)[0].decode()
        check('whole expected route bytes '+role, expected == now)
        restored = reverse_rows(now, rows[role])
        check('whole mother byte and AST inverse '+role, restored == before and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(before),include_attributes=False))
    derivations=inv['complete_changed_member_derivations']
    check('exact four changed original members', {x['relative_path'] for x in derivations}==CHANGED and len(derivations)==4)
    for d in derivations:
        name=d['relative_path']
        after, ap=read(NEW/name); before,bp=read(OLD/name)
        check('true Source derivation pins '+name, d['original_fullpin']==bp and d['derived_fullpin']==ap)
        check('whole finite hunk byte inverse '+name, reverse_hunks(after,d['full_byte_inverse_hunks'])==before)
    unchanged=set(old['members'])-CHANGED
    check('exact 34 original preserved members', len(unchanged)==34 and set(inv['unchanged_original_mother_members'])==unchanged)
    for name in sorted(unchanged): check('original whole bytes preserved '+name, read(NEW/name)[0]==read(OLD/name)[0])
    proof, proofpin=document(NEW/'COMPLETE_SOURCE_INVERSES.json')
    oldproof, oldproofpin=document(OLD/'COMPLETE_SOURCE_INVERSES.json')
    expected=json.loads(json.dumps(oldproof))
    for role in ('build_host','build_writer'): expected['exact_finite_transforms'][role].extend(rows[role])
    check('only two original full inverse rows extended', proof==expected)
    for role in ('canonical','prepare_host','prepare_writer','build_host','build_writer'):
        name='canonical.V25.UNREADY.full.py' if role=='canonical' else 'host_and_postclose_templates/'+role+'.V25.UNREADY.full.py'
        restored=reverse_rows(read(NEW/name)[0].decode(),proof['exact_finite_transforms'][role])
        parent=read(NEW/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))[0].decode()
        check('full original physics cap guard Source bytes and AST '+role, restored==parent and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
    check('new future business proof absence', all(proof['six_future_business_pins'][x] is None for x in proof['six_future_business_pins']) and proof['actual_new_Q'] is None and proof['project_API_or_numeric_executed'] is False)
    for role in ('build_host','build_writer'):
        text=read(NEW/role_names[role])[0].decode(); tree=ast.parse(text)
        names={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
        check('all future build assignments unknown '+role, all(isinstance(v,ast.Constant) and v.value is None for k,v in names.items() if k.startswith('FUTURE_')))
    for name in new['members']:
        if name.endswith('.py'):
            b=read(NEW/name)[0]; ast.parse(b); compile(b,str(NEW/name),'exec')
            check('Source syntax only '+name,True)
    for key in ('actual_independent_Source_review','actual_Root_Source_admission','actual_saved_closed_PREP_peer','actual_BUILD_Source_binding','actual_BUILD_terminal','actual_postclose_manifest'): check('future current Source only '+key,new[key] is None)
    check('no execution science or input qualification',new['source_only'] is True and new['candidate_helper_guard_API_compiler_or_numeric_executed'] is False and new['whole_build_INPUT_native_science_qualified'] is False)
    for path, wanted in tuple(pins.items()): check('all Source inputs unchanged postread '+path,read(Path(path))[1]==wanted)
    DEST.mkdir()
    (DEST/'REVIEWER_Source_stdlib_only.py').write_bytes(Path(__file__).read_bytes())
    (DEST/'REVIEWED_COMPLETE_NEW_SOURCE_MANIFEST.json').write_bytes((NEW/'MANIFEST.json').read_bytes())
    (DEST/'REVIEWED_COMPLETE_ORIGINAL_MOTHER_MANIFEST.json').write_bytes((OLD/'MANIFEST.json').read_bytes())
    report=dict(schema='INDEPENDENT_V25_MONITOR_ACCESS_COMPLETE_BUILD_NAMESPACE_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',source_only=True,complete_new_Source_manifest_pin=newpin,complete_original_mother_manifest_pin=oldpin,exact_namespace_full_byte_inverse_pin=invpin,complete_Source_inverse_pin=proofpin,check_count=len(checks),checks=checks,all_checks_typed_true=True,blockers=[],exact_three_active_BUILD_Source_pins={k:read(NEW/v)[1] for k,v in role_names.items()},all_Source_META_input_pins=list(pins.values()),whole_five_stage_commands_flags_inputs_order_caps_MRO_helper_Q_physics_byte_preserved=True,candidate_helper_guard_API_compiler_or_numeric_executed=False,actual_saved_closed_PREP_peer=None,actual_BUILD_Source_binding=None,actual_BUILD_terminal=None,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False)
    (DEST/'REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=report['status'],check_count=len(checks),review_pin=read(DEST/'REVIEW.json')[1],source_only=True,candidate_or_business_executed=False)))

if __name__=='__main__': main()

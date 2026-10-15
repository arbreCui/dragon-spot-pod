"""Generate/inspect SOURCE text only; never import or execute candidate code."""
from pathlib import Path
import ast
import base64
import hashlib
import json
import shutil

P = Path(__file__).parent
HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py')
CANONICAL = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py')
OLD_PROPOSAL = Path('/private/tmp/axmat_v22_failedbuild_inactive_audit_SOURCE_lastuse_7ecicdjv')
HELPER_SHA = 'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
CANONICAL_SHA = '09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
OLD_MANIFEST_SHA = '00373bffbeaeef7aecabf48ea66e494283e69885f848d1fd78806fc1cf64efef'
CANDIDATE_NAME = 'combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume.UNREADY.py'

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(path):
    before = identity(path)
    raw = path.read_bytes()
    after = identity(path)
    assert before == after and len(raw) == before[4]
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw), 'identity': before}

def write(name, value):
    dest = P / name
    assert not dest.exists()
    dest.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')

def dump(node):
    return ast.dump(node, include_attributes=False)

def defs(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

def text_of(source, node):
    return ''.join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])

before_pins = {str(f): pin(f) for f in (HELPER, CANONICAL, OLD_PROPOSAL/'MANIFEST.json')}
assert before_pins[str(HELPER)]['sha256'] == HELPER_SHA
assert before_pins[str(CANONICAL)]['sha256'] == CANONICAL_SHA
assert before_pins[str(OLD_PROPOSAL/'MANIFEST.json')]['sha256'] == OLD_MANIFEST_SHA
old_manifest = json.loads((OLD_PROPOSAL/'MANIFEST.json').read_bytes())
old_members_before = {}
for entry in old_manifest['members']:
    f = OLD_PROPOSAL / entry['relative_path']
    actual = pin(f)
    assert actual == {k: entry[k] for k in ('path', 'sha256', 'size_bytes', 'identity')}
    old_members_before[str(f)] = actual
    dest = P / 'ORIGINAL_SEALED_LAST_USE_PROPOSAL' / entry['relative_path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f, dest)
shutil.copyfile(OLD_PROPOSAL/'MANIFEST.json', P/'ORIGINAL_SEALED_LAST_USE_PROPOSAL'/'MANIFEST.json')
parent_raw = HELPER.read_bytes()
parent = parent_raw.decode('utf-8')
canonical_raw = CANONICAL.read_bytes()
canonical = canonical_raw.decode('utf-8')
(P/'ORIGINAL_cf0_COMPLETE_HELPER.py').write_bytes(parent_raw)
(P/'ORIGINAL_09e_COMPLETE_CANONICAL.py').write_bytes(canonical_raw)

old_start = '''    def snapshot(self):
        _require(not self._active, "end the read-open audit phase before freezing its trace")
'''
new_start = '''    def snapshot(self, *, _consume=False):
        # Private True is reserved for a fresh, exclusively owned audit whose
        # inactive snapshot is its last use. Default preserves all audit state.
        # Ownership beyond this object's builtin map is the caller's contract;
        # no reference-count, allocator, cache or caller-frame test is used.
        _require(type(_consume) is bool,
                 "private read-open snapshot consume flag must be an exact bool")
        _require(not self._active, "end the read-open audit phase before freezing its trace")
        if _consume:
            _require(type(self) is ReadOpenAudit and type(self._records) is dict
                     and self._active is False and self._recording is False
                     and all(trace is not self for trace in _ACTIVE_TRACES),
                     "private read-open snapshot consume requires an owned inactive builtin audit")
'''
old_return = '''        return {"schema": TRACE_SCHEMA, "coverage": "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY",
                "records": _json_clone(records),
                "subprocess_records": _json_clone(self._subprocess_records),
                "unique_records": len(self._records),
                "actual_read_open_attempts": sum(value["attempt_count"] for value in self._records.values()),
                "record_storage": "EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS",
                "success_of_open_attempt_is_not_observed": True,
                "native_libc_HDF5_loader_and_directory_stat_are_not_traced": True}
'''
private_return = '''        if _consume:
            # Normalization above traversed every original record/role. Capture
            # both original complete counts before their owned map's last use.
            # Clearing ends the serialized keys and original dictionaries; the
            # full normalized list and all nested data remain for the same clone.
            # A later clone error is not transactional in this private mode.
            unique_records = len(self._records)
            actual_read_open_attempts = sum(value["attempt_count"] for value in self._records.values())
            self._records.clear()
            return {"schema": TRACE_SCHEMA, "coverage": "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY",
                    "records": _json_clone(records),
                    "subprocess_records": _json_clone(self._subprocess_records),
                    "unique_records": unique_records,
                    "actual_read_open_attempts": actual_read_open_attempts,
                    "record_storage": "EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS",
                    "success_of_open_attempt_is_not_observed": True,
                    "native_libc_HDF5_loader_and_directory_stat_are_not_traced": True}
'''
edits = [(old_start, new_start), (old_return, private_return + old_return)]
candidate = parent
inverse_edits = []
for index, (old, new) in enumerate(edits):
    assert candidate.count(old) == 1
    candidate = candidate.replace(old, new, 1)
    inverse_edits.append({'index': index, 'old_utf8': old, 'new_utf8': new,
                          'old_base64': base64.b64encode(old.encode()).decode(),
                          'new_base64': base64.b64encode(new.encode()).decode()})
candidate_file = P / CANDIDATE_NAME
candidate_file.write_text(candidate)
restored = candidate
for edit in reversed(inverse_edits):
    assert restored.count(edit['new_utf8']) == 1
    restored = restored.replace(edit['new_utf8'], edit['old_utf8'], 1)
assert restored.encode() == parent_raw
pt, ct, rt = ast.parse(parent), ast.parse(candidate), ast.parse(restored)
pc = defs(pt)['ReadOpenAudit']
cc = defs(ct)['ReadOpenAudit']
pm = {n.name:n for n in pc.body if isinstance(n,ast.FunctionDef)}
cm = {n.name:n for n in cc.body if isinstance(n,ast.FunctionDef)}
ps, cs = pm['snapshot'], cm['snapshot']
checks = []
def check(name, condition, evidence=None):
    value = bool(condition)
    checks.append({'name':name,'pass':value,'evidence':evidence})
    assert value, name

check('full_bytes_inverse_to_cf0', restored.encode() == parent_raw, HELPER_SHA)
check('full_AST_inverse_to_cf0', dump(rt) == dump(pt))
check('complete_definition_order_and_count_81', list(defs(pt)) == list(defs(ct)) and len(defs(pt)) == 81)
for name, old in defs(pt).items():
    if name != 'ReadOpenAudit':
        check('unchanged_complete_definition_'+name,
              text_of(parent,old) == text_of(candidate,defs(ct)[name]) and dump(old) == dump(defs(ct)[name]))
for name in ('__init__','__enter__','__exit__'):
    check('unchanged_audit_method_'+name,text_of(parent,pm[name]) == text_of(candidate,cm[name]) and dump(pm[name]) == dump(cm[name]))
check('unchanged_all_module_nondefinition_AST',
      [dump(n) for n in pt.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))] ==
      [dump(n) for n in ct.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))])
check('only_keyword_private_flag_added', cs.args.posonlyargs == ps.args.posonlyargs and
      [dump(n) for n in cs.args.args] == [dump(n) for n in ps.args.args] and
      cs.args.vararg is None and cs.args.kwarg is None and len(cs.args.kwonlyargs) == 1 and
      cs.args.kwonlyargs[0].arg == '_consume' and
      type(cs.args.kw_defaults[0].value) is bool and cs.args.kw_defaults[0].value is False)
check('original_inactive_guard_preserved',dump(ps.body[0]) == dump(cs.body[1]))
check('original_complete_records_initialization_preserved',dump(ps.body[1]) == dump(cs.body[3]))
check('original_complete_normalization_all_roles_AST_and_bytes',dump(ps.body[2]) == dump(cs.body[4]) and
      text_of(parent,ps.body[2]) == text_of(candidate,cs.body[4]))
check('default_original_complete_return_AST_and_bytes',dump(ps.body[3]) == dump(cs.body[6]) and
      text_of(parent,ps.body[3]) == text_of(candidate,cs.body[6]))
private = cs.body[5]
check('private_branch_controlled_only_by_consume',isinstance(private,ast.If) and dump(private.test)==dump(ast.Name(id='_consume',ctx=ast.Load())) and not private.orelse)
check('private_original_unique_count_expression',dump(private.body[0].value)==dump(ps.body[3].value.values[4]))
check('private_original_attempt_total_expression',dump(private.body[1].value)==dump(ps.body[3].value.values[5]))
check('private_clear_only_record_map_after_both_counts',ast.unparse(private.body[2]) == 'self._records.clear()' and
      sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='clear' for x in ast.walk(cs))==1)
original_keys = [key.value for key in ps.body[3].value.keys]
new_keys = [key.value for key in private.body[3].value.keys]
check('all_nine_snapshot_fields_and_original_order', original_keys==new_keys and len(new_keys)==9,new_keys)
for i,key in enumerate(original_keys):
    if key not in ('unique_records','actual_read_open_attempts'):
        check('private_complete_snapshot_expression_'+key,
              dump(ps.body[3].value.values[i])==dump(private.body[3].value.values[i]))
check('private_return_uses_full_original_count_scalars',
      ast.unparse(private.body[3].value.values[4])=='unique_records' and
      ast.unparse(private.body[3].value.values[5])=='actual_read_open_attempts')
check('both_original_full_clone_calls_same_private_order',
      [ast.unparse(x) for x in ast.walk(private.body[3]) if isinstance(x,ast.Call)] ==
      ['_json_clone(records)','_json_clone(self._subprocess_records)'])
check('private_flag_is_exact_bool_guard',
      ast.unparse(cs.body[0].value.args[0])=='type(_consume) is bool')
check('private_owner_guard_exact_class_builtin_map_inactive_not_recording_not_hook_member',
      ast.unparse(cs.body[2].body[0].value.args[0])==
      'type(self) is ReadOpenAudit and type(self._records) is dict and (self._active is False) and (self._recording is False) and all((trace is not self for trace in _ACTIVE_TRACES))')
vf=defs(pt)['verify_graph']
vr=[x for x in ast.walk(vf) if isinstance(x,ast.Return)]
fields=[key.value for key in vr[0].value.keys]
check('all_27_verifier_return_fields_unchanged',len(vr)==1 and len(fields)==27 and
      text_of(parent,vf)==text_of(candidate,defs(ct)['verify_graph']),fields)

canon_tree=ast.parse(canonical)
callers=[]
for fn in canon_tree.body:
    if not isinstance(fn,ast.FunctionDef):continue
    calls=[x for x in ast.walk(fn) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='snapshot']
    if not calls:continue
    refs=sorted([{'line':x.lineno,'context':type(x.ctx).__name__} for x in ast.walk(fn) if isinstance(x,ast.Name) and x.id=='audit'],key=lambda x:x['line'])
    callers.append({'function':fn.name,'complete_source':text_of(canonical,fn),'snapshot_calls':[{'line':x.lineno,'expression':ast.unparse(x)}for x in calls],'audit_name_references':refs})
    check('three_local_refs_no_alias_or_export_'+fn.name,
          len(refs)==3 and [x['context'] for x in refs]==['Store','Load','Del'] and len(calls)==1 and
          ast.unparse(calls[0])=='audit.snapshot()')
check('all_three_local_snapshot_callers_enumerated',[x['function']for x in callers]==
      ['record_actual_trim_component','create_complete_input_graph','complete_input_phase'])
phase=defs(canon_tree)['complete_input_phase']
withs=[x for x in ast.walk(phase) if isinstance(x,ast.With)]
check('complete_phase_audit_fresh_local_with_owner',len(withs)==1 and
      ast.unparse(withs[0].items[0].context_expr)=='g.ReadOpenAudit()' and
      ast.unparse(withs[0].items[0].optional_vars)=='audit')
check('verifier_gets_no_audit_object',
      ast.unparse(withs[0].body[0].value)=="g.verify_graph(d['input_graph']['path'], expected_sha256=d['input_graph']['sha256'], phase=phase)")
check('audit_global_deactivation_precedes_snapshot',
      '        _ACTIVE_TRACES.remove(self)\n        self._active = False\n        return False\n' in text_of(parent,pm['__exit__']))
check('no_existing_helper_snapshot_callers',not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='snapshot' for x in ast.walk(pt)))
check('canonical_whole_source_unmodified',(P/'ORIGINAL_09e_COMPLETE_CANONICAL.py').read_bytes()==canonical_raw)
call_site_old='    trace=audit.snapshot();graph_path=d[\'input_graph\'][\'path\']\n'
call_site_new='    trace=audit.snapshot(_consume=True);graph_path=d[\'input_graph\'][\'path\']\n'
check('future_single_call_site_anchor_unique_only_full_phase',canonical.count(call_site_old)==1 and
      call_site_old in text_of(canonical,phase))
original_phase_calls=[ast.unparse(x)for x in ast.walk(phase)if isinstance(x,ast.Call)]
matrix=[
 {'object':'inactive local audit._records','creator':'ReadOpenAudit.__init__ and _open_audit','original_retention':'complete serialized dedup JSON keys + original complete record dicts','last_use':'full original normalization traversal, original len, original sum','private_release':'clear after normalization and both original counts, before unchanged full normalized/subprocess clone','scope_proof':'fresh local context, __exit__ removes global identity, no object alias/export among these bounded Source callers','no_global_ownership_claim':True},
 {'object':'snapshot local complete normalized records','creator':'unchanged dict(value) + original roles association, every row appended','survives_private_clear':True,'last_use':'unchanged full _json_clone(records)','no_filter_or_consumption_of_normalized_records':True},
 {'object':'audit._subprocess_records/_popen_commands/_popen_objects','last_use':'original role lookup and complete subprocess clone; audit deletion by caller','candidate_clears_or_changes':False},
 {'object':'complete returned nine-field trace','last_use':'original complete_input_phase unique path, attempt, external graph read checks; complete content digest','candidate_trims_or_changes':False},
 {'object':'full verify_graph result/27 fields and input graph','last_use':'all original fresh whole-graph verifier/current phase checks','candidate_changes':False},
 {'object':'full run_build declaration','last_use':'remaining environment phases/commands and finally/final gates','candidate_changes':False},
]
future={name:None for name in ('installed_new_helper_pin','new_Source_install_tool_witness','new_original_complete_pure_protocol_terminal','new_complete_current_graph_fresh_terminal','new_pure_saved_review','new_fresh_saved_review','new_joint_helper_Q','new_canonical_READY_runtime','new_prepare_terminal','new_complete_build_seal','new_complete_build_terminal','new_whole_INPUT_admission','new_native_AAA','new_native_ABA')}
controls=[
 {'scope':'retain original complete genuine pure protocol','required':'all existing positive/negative controls incl owner/trace private controls, full fixtures, stdout/stderr/watchdog/MRO and original 60s/512MiB/64MiB caps; no removal'},
 {'scope':'new private positive full equivalence','required':'fresh inactive exact audit: default and consume compare all nine fields, every nested type/key order/float bit, full row/roles/subprocess order; original caller inputs not reused between branch runs'},
 {'scope':'new private duplicate/empty coverage','required':'duplicate actual open counts, empty builtin map, every complete record preserved and count equality; consume clears map only and default map unchanged; no promised empty result after a second consume'},
 {'scope':'new private real subprocess controls','required':'all original actual Popen/descriptor identity/role tests stay; default/consume full equivalence incl roles and attempt counts; no forged native trace coverage'},
 {'scope':'new private rejects','required':'exact bool only: None/0/1/string; active audit; audit class subclass; non-builtin record map/dict subclass; _recording not False or stale identity still in active list; rejects before mutation'},
 {'scope':'private failure semantics','required':'normalization errors before clear leave input; clone failure after clear may have consumed private input, explicitly test/report no transactional promise or returned qualification'},
 {'scope':'complete current graph fresh verification','required':'full original graph and all 27 verification return fields/type/order/float bits; all 37111 inputs plus external graph = 37112 actual opens; complete unsieved gzip/trace streams and original 4positive/3reject controls; new consume snapshot integrated by pure driver Source without business run'},
 {'scope':'new admission','required':'two genuine original normal-host CLOSED0 terminals, complete saved independent reviews and actual new Source install binding; new joint Q only after both passes; old cf0 Q89 cannot qualify changed helper'},
]
after_pins={str(f):pin(f) for f in (HELPER,CANONICAL,OLD_PROPOSAL/'MANIFEST.json')}
check('all_fixed_original_Source_and_sealed_proposal_pins_unchanged',before_pins==after_pins)
for path,before in old_members_before.items():
    check('sealed_old_proposal_member_unchanged_'+Path(path).name,pin(Path(path))==before)
proof={'schema':'COMPLETE_HELPER_PRIVATE_INACTIVE_AUDIT_EXACT_SOURCE_INVERSE_V1','source_only':True,
       'parent_helper_pin':before_pins[str(HELPER)],'candidate_pin':pin(candidate_file),'hunks':inverse_edits,
       'full_bytes_inverse':True,'full_AST_inverse':True,'complete_definition_count':81,
       'other_top_definitions_complete_bytes_AST_unchanged':80,'unchanged_audit_methods':['__init__','__enter__','__exit__'],
       'default_original_normalization_and_return_complete_bytes_AST':True,
       'default_additions':'exact bool private flag check and two False branch tests only; original guard/normalization/return same',
       'private_changes_disclosed':'keyword flag + exact owner/inactive guard; full original len/sum before clear and full clones rather than in later return; private state consumed on later clone error',
       'full_original_call_AST_order_for_private_mode_unchanged':False,'canonical_modified':False,
       'new_qualification_required':True,'all_new_helper_qualification_pins':future,'six_future_business_pins':[None]*6}
write('EXACT_COMPLETE_SOURCE_INVERSE.json',proof)
write('LOCAL_CALLER_ALIAS_LAST_USE_AND_RETURN_EVIDENCE.json',{
       'schema':'COMPLETE_HELPER_INACTIVE_AUDIT_FINITE_SOURCE_OWNERSHIP_EVIDENCE_V1','source_only':True,
       'bounded_Source_scope':[before_pins[str(HELPER)],before_pins[str(CANONICAL)]],
       'all_local_snapshot_callers':callers,'complete_original_ReadOpenAudit':text_of(parent,pc),
       'complete_original_open_audit':text_of(parent,defs(pt)['_open_audit']),
       'complete_original_json_clone':text_of(parent,defs(pt)['_json_clone']),
       'complete_original_verify_graph':text_of(parent,vf),'all27_return_fields':fields,'all9_snapshot_fields':original_keys,
       'complete_original_phase_call_AST_order':original_phase_calls,'last_use_matrix':matrix,
       'future_canonical_call_site_source_only_not_applied':{'old':call_site_old,'new':call_site_new,'only_after_new_Q':True},
       'Source_can_prove_local_ownership_only':'No claim about arbitrary external public caller aliases. Private True explicitly transfers this record map at its final use; the exact local canonical caller is proven, defaults remain non-destructive.',
       'actual_peak_line_or_new_RSS_observed':False,'RSS_or_PASS_prediction':None})
write('REQUIRED_NEW_FULL_PROTOCOL_AND_FRESH_QUALIFICATION.json',{
       'schema':'COMPLETE_HELPER_PRIVATE_INACTIVE_AUDIT_REQUIRED_FUTURE_QUALIFICATION_V1','source_only':True,
       'status':'UNREADY_REQUIRES_NEW_GENUINE_PURE_AND_COMPLETE_FRESH_ADMISSION','controls':controls,
       'future_actual_pins':future,'six_future_business_pins':[None]*6,'old_helper_or_Q_credit_inherited':False,
       'original_caps_changed':False,'full_input_graph_or_trace_scope_changed':False,
       'future_scope_counts_are_original_contract_not_observations':{'canonical_inputs':37111,'actual_opens_including_graph':37112,'public_verifier_fields':27},
       'business_native_RAM_AAA_ABA_physics_qualified':False})
write('SOURCE_SELF_REVIEW.json',{'schema':'COMPLETE_HELPER_PRIVATE_INACTIVE_AUDIT_SOURCE_SELF_REVIEW_V1',
       'status':'PASS_COMPLETE_SOURCE_ONLY_UNREADY_NEW_HELPER','source_only':True,'checks':checks,
       'check_count':len(checks),'all_checks_typed_true':all(x['pass'] is True for x in checks),'blockers':[],
       'parent_Source_pins_before':before_pins,'parent_Source_pins_after':after_pins,
       'candidate_pin':pin(candidate_file),'candidate_or_helper_executed':False,'numeric_or_ART_payload_read':False,
       'project_canonical_D_E_changed':False,'new_actual_qualification':None,'six_future_business_pins':[None]*6})
(P/'REPORT.md').write_text('''This complete SOURCE candidate changes only ReadOpenAudit.snapshot with two explicit inverse hunks. The original 81 top-level definitions remain; all other 80 definitions, all globals, public verify_graph and its 27 return fields remain byte exact. The default snapshot preserves the original inactive guard, complete normalization and nine-field return, with an added exact-bool private flag check. No current helper, canonical, frozen namespace or cap was modified.

The proven local caller is complete_input_phase: its audit is fresh, removed from the active registry at context exit, has no alias/export in this bounded SOURCE, is read only by snapshot, then deleted after the complete path/attempt checks and trace digest. The other two local callers keep the default. No arbitrary external caller ownership is claimed. The candidate is not wired into canonical.

Private True requires an exact inactive ReadOpenAudit and builtin record map, no recording and no remaining active-registry identity. After every original row and subprocess-role normalization completes, it calculates both complete original counts, clears the old owned map and its serialized dedup keys, then performs the same two complete clones and returns all nine original fields in their original order. The complete normalized rows remain. Private count computation necessarily moves before clone; its full Call AST order is not identical. A clone failure after clear may leave private state consumed; this mode makes no transactional promise.

This is SOURCE only, UNREADY for admission. It is neither a measured peak-line cause nor a prediction that the next build passes. Root must independently review SOURCE, install a fresh helper, run the original full genuine pure protocol plus new private controls and complete current-graph fresh verification, independently review both complete saved results, then create a new joint Q. All new actual pins and six future business pins are None. Old cf0/Q89 remain unchanged and grant no credit to this changed helper. Full input/record/trace/role/namespace scope and original resources are preserved.
''')
print(json.dumps({'source_only':True,'status':'SOURCE_ONLY_COMPLETE_HELPER_UNREADY','package':str(P),
                  'candidate':pin(candidate_file),'inverse':pin(P/'EXACT_COMPLETE_SOURCE_INVERSE.json'),
                  'report':pin(P/'SOURCE_SELF_REVIEW.json'),'check_count':len(checks),
                  'candidate_executed':False,'new_Q':None},separators=(',',':')))

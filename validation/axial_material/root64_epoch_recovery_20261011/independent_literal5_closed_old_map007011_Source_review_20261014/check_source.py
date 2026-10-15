from pathlib import Path
import ast, copy, hashlib, importlib.util, json, os, stat, sys
sys.dont_write_bytecode = True
R = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P = R / 'storage_release_literal5_closed_old_map007011_source_v1_20261014'
D = Path(__file__).parent

def ids(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<64*2**20
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s)
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))

def load(p):
    if isinstance(p,dict):
        assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())

def seven(p):
    q=Path(p['path']);s=q.lstat()
    assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes'],str(q)

def fn(t,n):
    return next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==n)

assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
sfp=pin(P/'COMPLETE_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_FREEZE.json');sf=load(sfp)
assert sfp['sha256'].startswith('d352990f') and sfp['size_bytes']==370179
plan=load(sf['exact_role_plan_pin']);iv=load(sf['strict_low_level_Source_provenance_pin'])
assert sf['exact_role_plan_pin']['sha256'].startswith('230e7599') and sf['exact_role_plan_pin']['size_bytes']==56124
assert sf['strict_low_level_Source_provenance_pin']['sha256'].startswith('cab59500') and sf['strict_low_level_Source_provenance_pin']['size_bytes']==594418
assert sf['source_only'] is True and sf['manifest_prepared'] is False and sf['deletion_executed'] is False and sf['compiler_or_business_executed'] is False
assert sf['target_count']==plan['target_count']==5 and sf['target_bytes']==plan['target_bytes']==1158494380
assert sf['original_caps']==plan['original_caps'] and sf['original_caps']['SELF_mib']==512 and sf['original_caps']['stage_seconds']==600 and sf['original_caps']['whole_seconds']==1800 and sf['original_caps']['fresh_bytes']==2147483648
code={};oldcode={};trees={};oldtrees={}
assert len(iv['entries'])==3 and iv['source_only'] is True
for e in iv['entries']:
    candidate=e['candidate_pin'];pred=e['predecessor_pin']
    assert pin(candidate['path'])==candidate and pin(pred['path'])==pred
    ct=Path(candidate['path']).read_text();pt=Path(pred['path']).read_text();rev=ct
    for change in reversed(e['changes']):
        assert rev.count(change['after'])==1;rev=rev.replace(change['after'],change['before'])
    assert rev.encode()==Path(pred['path']).read_bytes()
    name=Path(candidate['path']).name;code[name]=ct;oldcode[name]=pt;trees[name]=ast.parse(ct);oldtrees[name]=ast.parse(pt)
assert {e['candidate_pin']['path'] for e in iv['entries']}=={p['path'] for p in sf['Source_pins']}
common='literal11_release_common.py';actor='verify_or_execute_literal11.py'
assert iv['seven_lowlevel_methods_wholebytes_equal']==['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
for name in iv['seven_lowlevel_methods_wholebytes_equal']:
    assert ast.get_source_segment(code[common],fn(trees[common],name)).encode()==ast.get_source_segment(oldcode[common],fn(oldtrees[common],name)).encode()
def unlinkloop(t):
    return next(n for n in ast.walk(t) if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [v.id for v in n.target.elts]==['target','row'])
assert ast.get_source_segment(code[actor],unlinkloop(trees[actor])).encode()==ast.get_source_segment(oldcode[actor],unlinkloop(oldtrees[actor])).encode()
assert iv['unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_equal'] is True and iv['actor_actual_after_fullfresh2True_original'] is True
assert "after['original_initial_reserve_admitted']is not True" in code[actor] and "before['regular_files']-after['regular_files']!=5" in code[actor]
assert 'predicted_margin_after_future' not in code[actor]
spec=importlib.util.spec_from_file_location('independent_literal5_old_map007011_source_only',P/common)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
gate=m.source_gate(sfp);proofs=m.closed_proofs()
assert gate['Source_pins']==sf['Source_pins'] and isinstance(proofs,list) and len(proofs)==21
assert m.TARGET_SELECTED_PINS==sf['literal5_fullpins']==plan['literal5_fullpins'] and len(m.TARGETS)==len(m.TARGET_PATHS)==5 and m.BYTES==1158494380
assert [Path(p['path']).parent.name for p in m.TARGET_SELECTED_PINS]==['map007','map008','map009','map010','map011']
assert m.PENDING_A10_LIBRARY_PINS==[] and sf['pending_A10_library_pins']==[]
mother=load(plan['mother9771_manifest_pin']);mr=mother['current_protected_full_EOF_pins']
assert len(mr)==9771 and m.HISTORICAL_TARGET_INDICES==[] and plan['all9771_mother_rows_kept'] is True and plan['no_current_MF_rows_retired'] is True
oldmaps=m.COMPLETED_EXACT2_MAP_RETIREMENT['original_target_pins']
assert oldmaps==mother['target_full_EOF_pins']==plan['completed_exact2_maps_only_historical']
assert [Path(p['path']).parent.name for p in oldmaps]==['map005','map006'] and all(not os.path.lexists(p['path']) for p in oldmaps)
assert not ({p['path'] for p in mr}&(m.TARGET_PATHS|{p['path'] for p in oldmaps}))
assert m.COMPLETED_EXACT2_MAP_RETIREMENT['post_pin']['sha256'].startswith('d80a') and m.COMPLETED_EXACT2_MAP_RETIREMENT['post_tools_pin']['sha256'].startswith('8320')
assert len(m.ROLE_KEEP_PINS)==9
before=plan['complete_owner_inventory']
assert len(before['ordinary_file_identities'])==m.OWNER_FILE_COUNT==plan['owner_file_count']==115
assert len(before['directory_identities'])==m.OWNER_DIRECTORY_COUNT==plan['owner_directory_count']==5
assert plan['retained_other_file_count']==110 and m.inventory()==before
for path,decl in before['symlinks'].items():
    assert ids(Path(path).lstat())==decl['identity'] and os.readlink(path)==decl['target']
for p in m.TARGET_SELECTED_PINS:
    seven(p);s=Path(p['path']).lstat();assert s.st_uid==os.getuid() and s.st_nlink==1
assert len({tuple(p['identity'][:2]) for p in m.TARGET_SELECTED_PINS})==5 and len({p['sha256'] for p in m.TARGET_SELECTED_PINS})==5
assert sum(p['size_bytes'] for p in m.TARGET_SELECTED_PINS)==1158494380
disjoint=fn(trees[common],'disjoint');test=disjoint.body[0].test;scope=dict(vars(m))
assert eval(compile(ast.Expression(test),'real_count_guard','eval'),scope) is False
bad=dict(scope);bad['TARGETS']=list(m.TARGETS)[:4]
assert eval(compile(ast.Expression(test),'missing_target_guard','eval'),bad) is True
bad=dict(scope);collision=copy.deepcopy(m.TARGET_SELECTED_PINS);collision[1]['identity'][:2]=collision[0]['identity'][:2];bad['TARGET_SELECTED_PINS']=collision
assert eval(compile(ast.Expression(test),'equal_size_duplicate_guard','eval'),bad) is True
assert 's.st_nlink!=1' in ast.get_source_segment(code[common],disjoint)
# Run only the actual metadata add body; never call payload-reading current_protection.
protection=fn(trees[common],'current_protection');addnode=next(n for n in protection.body if isinstance(n,ast.FunctionDef) and n.name=='add')
ns=dict(vars(m));ns.update(retired={p['path']:p for p in m.RELEASED_A10_LIBRARY_PINS},historical=[],table={},roles={},cache={})
expected_rows={}
def add_expected(p):
    assert p['path'] not in expected_rows or expected_rows[p['path']]==p
    expected_rows[p['path']]=p
for p in mr:
    add_expected(p)
def current_meta_pin(path):
    p=expected_rows[str(path)];seven(p);return p
ns['pin']=current_meta_pin
exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(addnode)],type_ignores=[])),'<actual_Source_metadata_add_only>','exec'),ns)
for i,p in enumerate(mr):
    ns['add'](p,'all_previous9771_rows_'+str(i))
assert len(ns['table'])==9771 and not ns['historical'] and all(ns['table'][p['path']]==p for p in mr)
for p in m.ROLE_KEEP_PINS:
    add_expected(p);ns['add'](p,'original_scientific9')
agg=load(m.CLOSED_FIRST_AGGREGATE['report_pin'])
assert plan['actual_first_aggregate_report_pin']==m.CLOSED_FIRST_AGGREGATE['report_pin'] and plan['first_actual_aggregate_outputs_retained'] is True
assert len(agg['complete_output_pins'])==13 and agg['failure'] is None and agg['after_check_error'] is None
agg_rows=list(m.CLOSED_FIRST_AGGREGATE.values())+agg['fixed_current_pins']+agg['complete_output_pins']
for p in agg_rows:
    add_expected(p);ns['add'](p,'all_first_actual_aggregate')
capture=load(m.A10_CAPTURE_AUTHORITY['report_pin']);post=load(m.A10_CAPTURE_AUTHORITY['post_pin']);hf=load(m.A10_CAPTURE_AUTHORITY['HF_pin'])
capture_rows=list(m.A10_CAPTURE_AUTHORITY.values())+hf['dependencies']+capture['fixed_current_pins']+capture['output_pins']+capture['owned_input_copy_pins']+post['actual_scene_full_EOF_pins']+post['actual_original_library_input_pins']
for p in capture_rows:
    if p['path'] not in ns['retired']:
        add_expected(p)
    ns['add'](p,'original_capture_only_exact_released_library2_historical')
protected_extraction_outputs=[]
for c in [m.CLOSED_A10_COMPLETION,m.CLOSED_EXTRACTION]:
    host=load(c['report_pin']);outputs=host['output_pins'] if c is m.CLOSED_A10_COMPLETION else host['complete_output_pins']
    if c is m.CLOSED_EXTRACTION:
        assert len(outputs)==46;protected_extraction_outputs=outputs+[c['report_pin']]
    for p in list(c.values())+host['fixed_current_pins']+outputs:
        add_expected(p);ns['add'](p,'all_current_completion_and_extraction')
assert len(protected_extraction_outputs)==47
for p in m.RELEASED_A10_LIBRARY_PINS:
    assert not os.path.lexists(p['path'])
    bad=dict(p);bad['sha256']='0'*64
    try:
        ns['add'](bad,'wrong_historical_SHA');raise AssertionError('wrong historical PF accepted')
    except RuntimeError:
        pass
assert not ({p['path'] for p in oldmaps}&set(ns['table'])) and not (m.TARGET_PATHS&set(ns['table']))
assert not ({tuple(p['identity'][:2]) for p in m.TARGET_SELECTED_PINS}&{tuple(p['identity'][:2]) for p in ns['table'].values()})
required=sf['Source_pins']+[sf['exact_role_plan_pin'],sf['strict_low_level_Source_provenance_pin'],sf['Source_preparer_pin'],sf['original_resource_factory_pin'],sfp,plan['mother9771_manifest_pin']]
assert len(required)==9 and len({p['path'] for p in required})==9
for _ in range(2):
    for p in required+m.TARGET_SELECTED_PINS+m.ROLE_KEEP_PINS+list(ns['table'].values()):
        seven(p)
assert m.inventory()==before
for k,v in sf.items():
    if k.startswith('future_'):
        assert v is None
result=dict(schema='INDEPENDENT_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_REVIEW_V1',status='PASS_LITERAL5_CLOSED_OLD_MAP007011_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,
    Source_freeze_pin=sfp,Source_pins=sf['Source_pins'],plan_pin=sf['exact_role_plan_pin'],inverse_pin=sf['strict_low_level_Source_provenance_pin'],Source_preparer_pin=sf['Source_preparer_pin'],original_resource_factory_pin=sf['original_resource_factory_pin'],source_required_fullpins=required,
    actual_pure_Source_gate_and_closed_proof_count=len(proofs),three_complete_Source_inverses_verified=True,seven_lowlevel_methods_wholebytes_unchanged=True,unlink_truthreceipt_dirfsync_FirstFailure_wholebytes_unchanged=True,actor_after_actual_fullfresh2True_required=True,
    actual_mother9771_manifest_pin=plan['mother9771_manifest_pin'],all9771_rows_exact_data_preserved_by_actual_add_metadata_block=True,current_MF_rows_retired=0,exact_already_released_map005006_only_historical=True,exact_released_map005006_historical_pins=oldmaps,exact_map005006_genuine_closed_release_authority=m.COMPLETED_EXACT2_MAP_RETIREMENT,
    target_count=5,target_logical_bytes=1158494380,target_fullpins=m.TARGET_SELECTED_PINS,target_UID_regular_singlelink_nonsymlink_current7_verified_twice=True,real_countguard_false_missingtarget_and_equal_size_duplicate_node_negative_rejected=True,owner_before_file_count=115,owner_directory_count=5,owner_symlink_count=len(before['symlinks']),retained_other_file_count=110,ordinary_files_and_symlinks_inventory_current=True,retained110_fullEOF_PFs_reserved_for_later_actual_MF=True,
    actual_first_aggregate_report_pin=m.CLOSED_FIRST_AGGREGATE['report_pin'],actual_first_aggregate_all13_outputs_and_host_retained=True,actual_completion_and_capture_preserved=True,actual_extraction47_outputs_and_host_protected=True,original_science9_fullpins=m.ROLE_KEEP_PINS,original_science9_and_final_map012_archives_docs_successful_pairs_current70_build75_liveTMP_preserved=True,
    no_generic_missing_pin_skip=True,no_recursive_historical_body_promotion=True,actual_add_block_wrong_historical_SHA_rejected=True,Source_and_metadata_only_no_target_or_science_body_EOF=True,current_protection_full_payload_reader_not_called=True,current_runtime_budget_admission_not_issued=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,reviewer_source_pin=pin(__file__),physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as out:
    json.dump(result,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),Source_freeze_pin=sfp,actual_closed_proof_count=len(proofs),target_count=5,target_bytes=1158494380,mother_current_row_count=9771,current_MF_rows_retired=0)),flush=True)

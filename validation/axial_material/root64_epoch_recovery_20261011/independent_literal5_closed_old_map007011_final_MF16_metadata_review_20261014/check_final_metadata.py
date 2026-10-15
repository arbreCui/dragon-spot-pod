from pathlib import Path
import hashlib, json, os, shlex, stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'storage_release_literal5_closed_old_map007011_source_v1_20261014'
D=Path(__file__).parent
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def seven(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes'],str(q)
def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<64*2**20
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
    if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())
def genuine(t):
    assert t['observed_closed'] is True and type(t['original_integer_exit_code']) is int and t['original_integer_exit_code']==0
    z=t['actual_terminal_return'];assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
    return json.loads(z['output'].strip().splitlines()[-1])
assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
mp=pin(P/'EXACT_LITERAL5_CLOSED_OLD_MAP007011_MANIFEST.json');m=load(mp)
assert mp['sha256']=='76af050507ddc17f27d33c2922c034131890b93dd8c151abf77ed1655f1d7483' and mp['size_bytes']==9209825
mtp=pin(R/'ROOT_LITERAL5_OLD_MAP007011_MANIFEST_TRUE_TOOL_RETURNS_20261014.json');mt=load(mtp);mr=genuine(mt)
assert mt['actual_initial_return']['chunk_id']=='8b4b6e' and mt['actual_terminal_return']['chunk_id']=='d7b9d4'
assert mr['manifest_pin']==mp and mr['protected_count']==9914 and mr['retained_other_count']==110 and mr['target_bytes']==1158494380 and mr['deletion_executed'] is False
rp=pin(R/'storage_release_literal5_closed_old_map007011_actual_receipts_20261014/READONLY_EXACT_LITERAL5_CLOSED_OLD_MAP007011_OLD_PRIVATE_VERIFICATION_RECEIPT.json');receipt=load(rp)
assert rp['sha256']=='74ba4b94048655bf93a7548d189a9ebb91ed3cdfa200c5a7af8ca119b8d9f259' and rp['size_bytes']==189267
rtp=pin(R/'ROOT_LITERAL5_OLD_MAP007011_READONLY_TRUE_TOOL_RETURNS_20261014.json');rt=load(rtp);rr=genuine(rt)
assert rt['actual_initial_return']['chunk_id']=='fb499f' and rt['actual_initial_return']['session_id']==24835 and rt['actual_terminal_return']['chunk_id']=='ac375a'
assert rr['receipt_pin']==rp and rr['deletion_executed'] is False
assert receipt['manifest_pin']==mp and receipt['execute_requested'] is False and receipt['deletion_records']==[] and receipt['next_target_intent'] is None and receipt['compiler_or_business_executed'] is False
assert receipt['status']=='READONLY_LITERAL2_ALL_CURRENT_EOF_VERIFIED'
ap=pin(R/'ROOT_EXACT_LITERAL5_OLD_MAP007011_READONLY_AND_EXECUTE_ARGV_20261014.json');a=load(ap)
assert a['manifest_pin']==mp and len(a['readonly_argv'])==16 and len(a['execute_argv'])==17
assert shlex.split(a['readonly_command'])==a['readonly_argv'] and shlex.split(a['execute_command'])==a['execute_argv']
assert a['execute_argv']==a['readonly_argv']+['--execute'] and a['execute_argv'].count('--execute')==1
assert rt['exact_executed_command']==a['readonly_command'] and '--execute' not in a['readonly_argv']
assert a['readonly_argv'][-4:]==['--manifest-sha256',mp['sha256'],'--manifest-seven-id',json.dumps(mp['identity'],separators=(',',':'))]
assert m['schema']=='ROOT_EXACT_LITERAL_LITERAL5_CLOSED_OLD_MAP007011_OLD_PRIVATE_RELEASE_MANIFEST_V1' and m['draft_only'] is False and m['action_executed'] is False
assert m['target_count']==5 and m['target_logical_bytes']==1158494380 and m['compiler_or_business_executed'] is False
sfp=m['selected_Source_freeze_pin'];sf=load(sfp);plan=load(sf['exact_role_plan_pin'])
assert sfp['sha256']=='d352990f47e9c673c9868bfc0e90c4cbf00dc76ae43c1d670d7515944540c099' and sf['source_only'] is True
assert m['Source_pins']==sf['Source_pins'] and len(m['Source_pins'])==3
reviews=m['selected_literal11_Source_reviews'];assert len(reviews)==2 and [v[0] for v in reviews]==['root','independent']
for who,p,t in reviews:
    review=load(p);tools=load(t);z=tools['actual_review_return']
    assert review['Source_freeze_pin']==sfp and review['failure'] is None
    if who=='independent':assert review['source_only'] is True
    for k in ['business_executed','compiler_executed','numerical_executed']:assert review[k] is False
    assert review['deletion_executed' if who=='root' else 'files_deleted'] is False
    assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
    assert tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==0
    assert json.loads(z['output'].strip().splitlines()[-1])['review_pin']==p
independent=load(reviews[1][1]);assert independent['actual_pure_Source_gate_and_closed_proof_count']==21 and independent['current_MF_rows_retired']==0
cmd=shlex.split(mt['exact_executed_command']);assert len(cmd)==42 and cmd[11]==str(P/'prepare_literal11_manifest.py')
selected=[('source-freeze',sfp),('root-source-review',reviews[0][1]),('root-source-tools',reviews[0][2]),('independent-source-review',reviews[1][1]),('independent-source-tools',reviews[1][2])]
assert cmd[12:]==[token for name,p in selected for token in ['--'+name+'-summary',p['path'],'--'+name+'-sha256',p['sha256'],'--'+name+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]]
protected=m['current_protected_full_EOF_pins'];table={p['path']:p for p in protected}
assert len(protected)==len(table)==9914
for p in protected:seven(p)
mother=load(plan['mother9771_manifest_pin']);rows=mother['current_protected_full_EOF_pins'];assert len(rows)==9771
assert all(table[p['path']]==p for p in rows)
dag=m['Source_DAG_provenance'];assert dag['previous_protected_count']==9771 and dag['exact_previous_MF_indices_migrated_to_history']==[] and dag['all9771_PF_rows_data_retained'] is True
assert dag['no_generic_missing_pin_skip'] is True and dag['no_recursive_historical_PF_body_promotion'] is True
targets=m['target_full_EOF_pins'];assert targets==sf['literal5_fullpins']==plan['literal5_fullpins'] and len(targets)==5
assert [Path(p['path']).parent.name for p in targets]==['map007','map008','map009','map010','map011']
assert sum(p['size_bytes'] for p in targets)==1158494380 and len({tuple(p['identity'][:2]) for p in targets})==5
for p in targets:
    seven(p);s=Path(p['path']).lstat();assert s.st_uid==os.getuid() and s.st_nlink==1
assert not ({p['path'] for p in targets}&set(table)) and not ({tuple(p['identity'][:2]) for p in targets}&{tuple(p['identity'][:2]) for p in protected})
retained=m['retained_all_other_v15_files_full_EOF_pins'];assert len(retained)==110 and len({p['path'] for p in retained})==110
assert all(table[p['path']]==p for p in retained)
inventory=m['complete_before_inventory'];assert inventory==plan['complete_owner_inventory']==dag['current_target_owner_complete_inventory']
assert len(inventory['ordinary_file_identities'])==115 and len(inventory['directory_identities'])==5 and len(inventory['symlinks'])==35
assert set(inventory['ordinary_file_identities'])=={p['path'] for p in targets+retained}
for p in targets+retained:assert inventory['ordinary_file_identities'][p['path']]==p['identity']
for path,identity in inventory['ordinary_file_identities'].items():assert ids(Path(path).lstat())==identity
for path,identity in inventory['directory_identities'].items():
    p=Path(path);s=p.lstat();assert stat.S_ISDIR(s.st_mode) and not p.is_symlink() and ids(s)==identity
    assert set(str(p/x) for x in os.listdir(p))=={q for q in list(inventory['ordinary_file_identities'])+list(inventory['symlinks']) if str(Path(q).parent)==path}
for path,v in inventory['symlinks'].items():assert ids(Path(path).lstat())==v['identity'] and os.readlink(path)==v['target']
science=independent['original_science9_fullpins'];assert len(science)==9 and all(table[p['path']]==p for p in science)
aggpin=independent['actual_first_aggregate_report_pin'];agg=load(aggpin);assert len(agg['complete_output_pins'])==13
assert all(table[p['path']]==p for p in agg['complete_output_pins']+[aggpin])
ex=sf['actual_extraction_authority'];eh=load(ex['report_pin']);assert len(eh['complete_output_pins'])==46
assert all(table[p['path']]==p for p in eh['complete_output_pins']+[ex['report_pin']])
released_libraries={p['path']:p for p in sf['released_A10_library_pins']}
assert len(released_libraries)==2
historical_libraries=dag['exact_already_released_A10_library_historical_declarations']
assert all(q['current_pin'] is None and q['original_body_pin']==released_libraries[q['original_body_pin']['path']] for q in historical_libraries)
for authority in [sf['actual_A10_capture_authority'],sf['actual_A10_completion_authority']]:
    host=load(authority['report_pin']);assert table[authority['report_pin']['path']]==authority['report_pin']
    for p in host['output_pins']:
        if authority is sf['actual_A10_capture_authority'] and p['path'] in released_libraries:
            assert p==released_libraries[p['path']] and not os.path.lexists(p['path']) and p['path'] not in table
            assert any(q['original_body_pin']==p for q in historical_libraries)
        else:assert table[p['path']]==p
old=independent['exact_released_map005006_historical_pins'];assert all(not os.path.lexists(p['path']) and p['path'] not in table for p in old)
assert [q['original_body_pin'] for q in dag['exact_already_released_map005006_historical_declarations']]==old
assert all(q['current_pin'] is None for q in dag['exact_already_released_map005006_historical_declarations'])
assert len(m['actual_closed_failed_v14_v15_v16_owner_proofs'])==21 and dag['retained_other_file_count']==110
for p in protected+targets+[mp,mtp,rp,rtp,ap,sfp]+sf['Source_pins']+[v for _,p,t in reviews for v in [p,t]]:seven(p)
result=dict(schema='INDEPENDENT_LITERAL5_CLOSED_OLD_MAP007011_FINAL_MF16_METADATA_REVIEW_V1',status='PASS_LITERAL5_CLOSED_OLD_MAP007011_ACTUAL_MF16_METADATA_FINAL_LIGHT',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,
    Source_freeze_pin=sfp,actual_manifest_pin=mp,actual_manifest_true_tool_pin=mtp,actual_readonly_receipt_pin=rp,actual_readonly_true_tool_pin=rtp,actual_readonly16_execute17_argv_pin=ap,actual_Source_review_authorities=reviews,reviewer_source_pin=pin(__file__),
    actual_manifest_Root_integer_exit_code=mt['original_integer_exit_code'],actual_readonly_Root_integer_exit_code=rt['original_integer_exit_code'],actual_manifest42_and_readonly16_and_future_execute17_argv_verified=True,complete_current_protected_count=9914,all9914_current7_verified_twice=True,all9771_mother_current_rows_preserved=True,current_MF_rows_retired=0,
    target_count=5,target_logical_bytes=1158494380,target_UID_link1_current7_physical_and_path_disjoint_verified=True,owner_file_count=115,owner_directory_count=5,owner_symlink_count=35,retained_other_file_count=110,all110_retained_relationships_exact=True,complete_current_owner_inventory_unchanged=True,
    original_science9_protected=True,actual_first_aggregate13_plus_host_protected=True,actual_extraction46_plus_host_protected=True,actual_capture_and_completion_protected=True,exact_released_old_map005006_historical_only=True,actual_manifest_and_readonly_full_EOF_producing_returns_genuine=True,target_or_scientific_payload_EOF_repeated=False,no_new_gate_layer=True,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),actual_manifest_pin=mp,actual_readonly_receipt_pin=rp,complete_current_protected_count=9914,target_count=5)),flush=True)

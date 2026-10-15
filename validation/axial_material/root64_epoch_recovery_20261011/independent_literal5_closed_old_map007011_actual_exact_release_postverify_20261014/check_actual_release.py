from pathlib import Path
import hashlib, importlib.util, json, os, shlex, stat, sys
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'storage_release_literal5_closed_old_map007011_source_v1_20261014'
D=Path(__file__).parent
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def seven(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes'],str(q)
def pin(p,maximum=64*2**20):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<=maximum
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
    if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())
assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
mp=pin(P/'EXACT_LITERAL5_CLOSED_OLD_MAP007011_MANIFEST.json');m=load(mp)
assert mp['sha256']=='76af050507ddc17f27d33c2922c034131890b93dd8c151abf77ed1655f1d7483'
ap=pin(R/'ROOT_EXACT_LITERAL5_OLD_MAP007011_READONLY_AND_EXECUTE_ARGV_20261014.json');argv=load(ap)
assert argv['manifest_pin']==mp and len(argv['execute_argv'])==17 and argv['execute_argv']==argv['readonly_argv']+['--execute']
assert shlex.split(argv['execute_command'])==argv['execute_argv'] and argv['execute_argv'].count('--execute')==1
tp=pin(R/'ROOT_LITERAL5_OLD_MAP007011_ACTUAL_EXECUTE_TRUE_TOOL_RETURNS_20261014.json');tools=load(tp)
assert tools['actual_initial_return']['chunk_id']=='ec617f' and tools['actual_initial_return']['session_id']==17269
z=tools['actual_terminal_return'];assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
assert tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==0
assert tools['exact_executed_command']==argv['execute_command']
closed=json.loads(z['output'].strip().splitlines()[-1]);rp=closed['receipt_pin'];receipt=load(rp)
assert rp['path']==str(R/'storage_release_literal5_closed_old_map007011_actual_receipts_20261014/ACTUAL_EXACT_LITERAL5_CLOSED_OLD_MAP007011_OLD_PRIVATE_RELEASE_RECEIPT.json')
assert receipt['schema']=='ACTUAL_EXACT_LITERAL5_CLOSED_OLD_MAP007011_OLD_PRIVATE_RELEASE_RECEIPT_V1'
assert receipt['status']==closed['status']=='EXACT_LITERAL5_CLOSED_OLD_MAP007011_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'
assert receipt['manifest_pin']==mp and receipt['execute_requested'] is True and receipt['compiler_or_business_executed'] is False
assert receipt['deleted_files']==closed['deleted_files']==5 and receipt['logical_bytes_released']==closed['logical_bytes_released']==1158494380
assert closed['original_initial_reserve_admitted'] is True and receipt['next_target_intent'] is None and 'first_error' not in receipt
targets=m['target_full_EOF_pins'];targetpaths={p['path'] for p in targets};assert len(targets)==len(targetpaths)==5
assert len(receipt['deletion_records'])==5
for p,record in zip(targets,receipt['deletion_records']):
    assert record['original_fullpin']==p and not os.path.lexists(p['path'])
    for k in ['actual_unlink_returned','target_directory_fsync_attempted','target_directory_fsync_returned','confirmed_absent']:assert record[k] is True
    assert record['parent_before_seven_id']==m['complete_before_inventory']['directory_identities'][str(Path(p['path']).parent)]
assert sum(p['size_bytes'] for p in targets)==1158494380
protected=m['current_protected_full_EOF_pins'];table={p['path']:p for p in protected};assert len(protected)==len(table)==9914
for p in protected:seven(p)
retained=m['retained_all_other_v15_files_full_EOF_pins'];assert len(retained)==110 and all(table[p['path']]==p for p in retained)
for p in retained:assert pin(p['path'],2*2**30)==p
before=m['complete_before_inventory'];assert len(before['ordinary_file_identities'])==115 and len(before['directory_identities'])==5 and len(before['symlinks'])==35
assert set(before['ordinary_file_identities'])==targetpaths|{p['path'] for p in retained}
changes=receipt['affected_parent_changes'];assert len(changes)==5
byparent={c['path']:c for c in changes};assert len(byparent)==5 and set(byparent)==set(before['directory_identities'])
current_files={};current_links={}
for path,old in before['directory_identities'].items():
    p=Path(path);s=p.lstat();now=ids(s);c=byparent[path]
    assert stat.S_ISDIR(s.st_mode) and not p.is_symlink() and c['before']==old and c['after']==now
    assert c['removed_children']==1 and c['nlink_delta']==-1 and c['size_delta']==-32
    assert now[:3]==old[:3] and now[3]==old[3]-1 and now[4]==old[4]-32 and now[5]>=old[5] and now[6]>=old[6]
    for child in p.iterdir():
        s=child.lstat()
        if stat.S_ISREG(s.st_mode):current_files[str(child)]=ids(s)
        elif stat.S_ISLNK(s.st_mode):current_links[str(child)]=dict(identity=ids(s),target=os.readlink(child))
        else:raise AssertionError('unexpected owner entry '+str(child))
assert current_files=={p:i for p,i in before['ordinary_file_identities'].items() if p not in targetpaths}
assert len(current_files)==110 and current_links==before['symlinks'] and len(current_links)==35
for p,record in zip(targets,receipt['deletion_records']):assert record['parent_after_seven_id']==byparent[str(Path(p['path']).parent)]['after']
bfr=receipt['original_budget_before'];aft=receipt['original_budget_after']
assert bfr['artifact_bytes']-aft['artifact_bytes']==1158494380 and bfr['regular_files']-aft['regular_files']==5 and aft['original_initial_reserve_admitted'] is True
assert aft['remaining_after_original_initial_reserves_bytes']>0
sfpin=m['selected_Source_freeze_pin'];sf=load(sfpin);plan=load(sf['exact_role_plan_pin']);mother=load(plan['mother9771_manifest_pin'])
assert len(mother['current_protected_full_EOF_pins'])==9771 and all(table[p['path']]==p for p in mother['current_protected_full_EOF_pins'])
dag=m['Source_DAG_provenance'];assert dag['all9771_PF_rows_data_retained'] is True and dag['exact_previous_MF_indices_migrated_to_history']==[]
ind=next(p for who,p,t in m['selected_literal11_Source_reviews'] if who=='independent');source=load(ind)
assert source['Source_freeze_pin']==sfpin and source['failure'] is None and source['source_only'] is True
science=source['original_science9_fullpins'];assert len(science)==9 and all(table[p['path']]==p for p in science)
agp=source['actual_first_aggregate_report_pin'];ag=load(agp)
assert len(ag['complete_output_pins'])==13 and all(table[p['path']]==p for p in ag['complete_output_pins']+[agp])
ex=sf['actual_extraction_authority'];eh=load(ex['report_pin'])
assert len(eh['complete_output_pins'])==46 and all(table[p['path']]==p for p in eh['complete_output_pins']+[ex['report_pin']])
assert receipt['all_other_v15_science_and_current_success_failed_public_outputs_retained'] is True and receipt['only_old_private_exact_path_replay_lost'] is True
assert not (targetpaths&set(table))
# Original resource factory metadata only; no target, scientific payload, or native tree decoding.
spec=importlib.util.spec_from_file_location('independent_literal5_release_original_factory_only',P/'literal11_release_common.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
current=s.budget()
assert current['original_initial_reserve_admitted'] is True and current['remaining_after_original_initial_reserves_bytes']>0
assert current['original_cold_reserve_bytes']==sf['original_caps']['cold_reserve_bytes'] and current['metadata_reserve_bytes']==sf['original_caps']['metadata_reserve_bytes'] and current['initial_fresh_reserve_bytes']==sf['original_caps']['fresh_bytes']
assert current['artifact_budget_bytes']==sf['original_caps']['history_bytes'] and current['min_free_bytes']==sf['original_caps']['free_floor_bytes']
assert s.inventory()==dict(ordinary_file_identities=current_files,directory_identities={path:c['after'] for path,c in byparent.items()},symlinks=current_links)
assert s.inventory([s.V12_OUT])==dag['current_v12_complete_inventory']
for p in protected+[mp,ap,tp,rp,sfpin,ind]+sf['Source_pins']:seven(p)
assert all(not os.path.lexists(p['path']) for p in targets)
result=dict(schema='INDEPENDENT_LITERAL5_CLOSED_OLD_MAP007011_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1',status='PASS_ACTUAL_LITERAL5_CLOSED_OLD_MAP007011_EXACT_RELEASE_POSTVERIFICATION',failure=None,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed_by_reviewer=False,files_deleted_by_reviewer=False,
    Source_freeze_pin=sfpin,actual_manifest_pin=mp,actual_Root_true_tool_pin=tp,actual_Root_argv_pin=ap,actual_release_receipt_pin=rp,actual_independent_Source_review_pin=ind,reviewer_source_pin=pin(__file__),actual_Root_integer_exit_code=tools['original_integer_exit_code'],actual_release_Root17_genuine_closed_no_retry=True,
    complete_current_protected_count=9914,all9914_current7_verified_twice=True,all9771_mother_current_rows_preserved=True,current_MF_rows_retired=0,actual_deleted_files=5,actual_logical_bytes_released=1158494380,all5_targets_currently_absent=True,all5_original_unlink_truthreceipt_dirfsync_and_FirstFailure_proof_preserved=True,
    retained_other_file_count=110,all110_retained_full_EOF_SHA_and7_verified=True,actual_owner_regular_files_before=115,actual_owner_regular_files_after=110,actual_owner_directories_retained=5,actual_owner_symlinks_retained=35,actual_affected_parent_changes=changes,all_original_science9_current=True,actual_first_aggregate13_plus_host_current=True,actual_extraction46_plus_host_current=True,current_v12_metadata_inventory_unchanged=True,
    actual_original_resource_delta_bytes=bfr['artifact_bytes']-aft['artifact_bytes'],actual_original_resource_delta_files=bfr['regular_files']-aft['regular_files'],actual_after_original_factory_fullfresh2_admitted=True,actual_current_original_factory=current,actual_current_original_factory_fullfresh2_admitted=True,
    scientific_payload_EOF_repeated=False,native_or_SQLite_scientific_trees_redecoded=False,only_required110_retained_owner_files_read_to_EOF=True,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),actual_release_receipt_pin=rp,actual_Root_integer_exit_code=tools['original_integer_exit_code'],actual_deleted_files=5,actual_logical_bytes_released=1158494380,actual_current_original_factory_fullfresh2_admitted=current['original_initial_reserve_admitted'],actual_current_remaining_after_original_initial_reserves_bytes=current['remaining_after_original_initial_reserves_bytes'])),flush=True)

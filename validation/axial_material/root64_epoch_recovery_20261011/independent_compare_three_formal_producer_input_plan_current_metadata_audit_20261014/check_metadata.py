from pathlib import Path
import collections, hashlib, json, os, stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
D=Path(__file__).parent
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<64*2**20
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
    if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())
def current(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes']
def genuine(tools,expected):
    assert tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==0
    z=tools['actual_review_return'];assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
    assert json.loads(z['output'].strip().splitlines()[-1])['review_pin']==expected
assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
planpin=pin(R/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json');plan=load(planpin)
assert planpin['sha256']=='3948281d4f69755af3b1ab2ee8d14fa6ab444e2450db17adc51e21be7aedffab' and planpin['size_bytes']==14155
assert plan['schema']=='AAA3_FORMAL_RANK1_AND_ACTUAL_INDEPENDENT_PRODUCER_INPUT_PLAN_V1' and len(plan['formal_inputs'])==13 and len(plan['producers'])==3
sfpin=pin(R/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014/COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json');sf=load(sfpin)
catalogpin=next(p for p in sf['complete_source_file_pins'] if Path(p['path']).name=='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json');catalog=load(catalogpin)
bindingpin=next(p for p in sf['complete_source_file_pins'] if Path(p['path']).name=='CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json');binding=load(bindingpin)
assert binding['current_mount_full_identity_catalog_pin']==catalogpin
assert catalog['schema']=='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1' and catalog['status']=='ACTUAL_CURRENT_MOUNT_COMPLETE_PF_CATALOG_CLOSED0_ONLY' and catalog['current_data_identity_qualified'] is True and catalog['mandatory_failures']==[]
assert catalog['post_release_role_reconciliation']['all_retained_PF_all7_SHA_fullEOF_reverified'] is True
assert catalog['post_literal3_old_pack_role_reconciliation']['inherited_predecessor_complete_EOF_attestation_preserved'] is True
catrows={}
for row in catalog['rows']:
    p=row['current_pin'];assert p['path'] not in catrows or catrows[p['path']]==p;catrows[p['path']]=p
mfpin=pin(R/'storage_release_literal5_closed_old_map007011_source_v1_20261014/EXACT_LITERAL5_CLOSED_OLD_MAP007011_MANIFEST.json');mf=load(mfpin)
assert mfpin['sha256']=='76af050507ddc17f27d33c2922c034131890b93dd8c151abf77ed1655f1d7483' and len(mf['current_protected_full_EOF_pins'])==9914
mfrows={p['path']:p for p in mf['current_protected_full_EOF_pins']};assert len(mfrows)==9914
postpin=pin(R/'independent_literal5_closed_old_map007011_actual_exact_release_postverify_20261014/REVIEW.json');post=load(postpin)
posttoolspin=pin(Path(postpin['path']).parent/'TRUE_TOOL_RETURNS.json');pt=load(posttoolspin);genuine(pt,postpin)
assert postpin['sha256']=='11ed3dc3ef128a21842baa2733b5d98e346ec527ba3ae9362173efecf245cead' and posttoolspin['sha256']=='aaa2e8fe4e90fe241f2b04bff829d75a689dc13d8d1580b35420072c6a74ac65'
assert post['failure'] is None and post['actual_manifest_pin']==mfpin and post['complete_current_protected_count']==9914 and post['all9914_current7_verified_twice'] is True
assert post['all110_retained_full_EOF_SHA_and7_verified'] is True and post['actual_release_Root17_genuine_closed_no_retry'] is True
declarations=[];reports=[]
for i,p in enumerate(plan['formal_inputs']):declarations.append(('formal_inputs',p))
for producer in plan['producers']:
    plane=producer['plane'];rp=producer['report'];actual=pin(rp['path'])
    assert actual['path']==rp['path'] and actual['sha256']==rp['sha256'] and actual['size_bytes']==rp['size_bytes'] and actual['identity'][1:]==rp['identity'][1:]
    reports.append(actual);host=load(actual)
    for key in ['report','archive','radial_binary_track']:declarations.append((f'producer{plane}_{key}',producer[key]))
    for p in host['fixed_current_pins']:declarations.append((f'producer{plane}_fixed_current_pins',p))
stats={};unique={};issues=[]
for role,p in declarations:
    q=Path(p['path'])
    try:s=q.lstat()
    except FileNotFoundError:
        issues.append(dict(role=role,path=p['path'],classification='ABSENT'));stats.setdefault(role,collections.Counter())['ABSENT']+=1;continue
    actual=ids(s)
    classification='EXACT_DEV34_TO29_ONLY' if p['identity'][0]==16777234 and actual[0]==16777229 and actual[1:]==p['identity'][1:] and s.st_size==p['size_bytes'] and stat.S_ISREG(s.st_mode) and not q.is_symlink() else 'NON_DEV_ONLY_CHANGE'
    stats.setdefault(role,collections.Counter())[classification]+=1
    if classification!='EXACT_DEV34_TO29_ONLY':issues.append(dict(role=role,path=p['path'],classification=classification,historical_identity=p['identity'],actual_identity=actual))
    assert p['path'] not in unique or unique[p['path']]['historical_pin']==p
    if p['path'] not in unique:unique[p['path']]=dict(historical_pin=p,actual_identity=actual,roles=collections.Counter())
    unique[p['path']]['roles'][role]+=1
assert len(declarations)==23607 and len(unique)==2345 and not issues
rebinding=[];catalog_covered=mf_covered=0;missing_eof=[]
for path,item in sorted(unique.items()):
    p=item['historical_pin'];c=catrows.get(path);m=mfrows.get(path)
    def exact(candidate):return candidate is not None and candidate['path']==p['path'] and candidate['sha256']==p['sha256'] and candidate['size_bytes']==p['size_bytes'] and candidate['identity']==item['actual_identity'] and candidate['identity'][1:]==p['identity'][1:]
    catgood=exact(c);mfgood=exact(m);catalog_covered+=int(catgood);mf_covered+=int(mfgood)
    if not (catgood or mfgood):missing_eof.append(dict(path=path,size_bytes=p['size_bytes'],original_sha256=p['sha256']))
    assert catgood and mfgood,path
    current(c);current(m)
    rebinding.append(dict(historical_pin=p,canonical_current_full_EOF_pin=c,changed_identity_indices=[0],exact_source_catalog_match=True,exact_latest_MF9914_match=True,declaration_role_counts=dict(item['roles']),declaration_occurrences=sum(item['roles'].values())))
assert catalog_covered==mf_covered==2345 and missing_eof==[]
for row in rebinding:current(row['canonical_current_full_EOF_pin'])
for p in [planpin,sfpin,catalogpin,bindingpin,mfpin,postpin,posttoolspin]+reports:current(p)
result=dict(schema='INDEPENDENT_COMPARE_THREE_FORMAL_PRODUCER_INPUT_CURRENT_METADATA_AUDIT_V1',status='PASS_COMPARE_THREE_FORMAL_PRODUCER_INPUT_EXACT_CURRENT_METADATA_AUDIT',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,formal_plan_or_projection_written=False,
    actual_original_plan_pin=planpin,actual_source_freeze_pin=sfpin,actual_current_catalog_pin=catalogpin,actual_current_binding_pin=bindingpin,actual_latest_MF9914_pin=mfpin,actual_latest_MF_release_post_pin=postpin,actual_latest_MF_release_post_tools_pin=posttoolspin,actual_producer_report_current_fullpins=reports,reviewer_source_pin=pin(__file__),
    actual_plan_schema=plan['schema'],formal_input_count=13,producer_count=3,producer_fixed_pin_declaration_counts=[4731,9427,9427],category_classification_counts={k:dict(v)for k,v in stats.items()},total_pin_declarations=23607,distinct_physical_path_pin_count=2345,
    absent_paths=[],non_dev_only_changed_paths=[],nonregular_paths=[],inconsistent_duplicate_pin_declarations=[],current_identity_verified_twice=True,only_exact16777234_to16777229_change_allowed=True,all_other6_identity_fields_and_SHA_and_size_preserved=True,
    current_full_EOF_catalog_exact_match_count=catalog_covered,current_latest_MF9914_exact_match_count=mf_covered,current_full_EOF_provenance_complete=True,additional_specific_large_EOF_needed=[],exact_rebinding_enumeration=rebinding,
    large_scientific_payload_or_native_tree_EOF_read_by_reviewer=False,producer_report_metadata_only_EOF_verified=True,no_generic_device_rule_or_missing_skip=True,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),distinct_exact_rebinding_paths=2345,total_pin_declarations=23607,current_catalog_exact_matches=2345,current_MF9914_exact_matches=2345,absent=0,non_dev_only_changes=0,additional_large_EOF_needed=0)),flush=True)

from pathlib import Path
import ast,json,hashlib,difflib
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_four_contract_finite_UNREADY_Source_fix_vz42_t14')
O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
q=P/'complete_observation_BUILD5_AB_runtime.UNREADY.py';s=q.read_text()
assert s.count('snapshots.append(dict(event=event,role=role,root_prefix=[],input_pin=snapshot))')==1
s=s.replace('snapshots.append(dict(event=event,role=role,root_prefix=[],input_pin=snapshot))',"snapshots.append(dict(event=event,role=role,root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB'],input_pin=snapshot))")
s=s.replace("[dict(item,root_prefix=[]if item['role']=='final-complete-micro'else['MACROLIB'])for item in snapshots]","[dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])for item in snapshots]")
ast.parse(s);q.write_text(s)
q=P/'Root_observation_postclose_META_writer.UNREADY.py';s=q.read_text()
s=s.replace("for p in row['complete_state_snapshot_inputs']:require(p['root_prefix']==[],'all real observer snapshot physical roots are native XSM root');check(p['input_pin'])", "for p in row['complete_state_snapshot_inputs']:\n            require(set(p)=={'event','role','root_prefix','logical_prefix','input_pin'}and p['root_prefix']==[]and p['logical_prefix']==([]if p['role']=='final-complete-micro'else['MACROLIB']),'explicit native root[] and original pool logical prefix');check(p['input_pin'])")
s=s.replace("[dict(p,root_prefix=[]if p['role']=='final-complete-micro'else['MACROLIB'])for p in row['complete_state_snapshot_inputs']]", "[dict(event=p['event'],role=p['role'],root_prefix=p['logical_prefix'],input_pin=p['input_pin'])for p in row['complete_state_snapshot_inputs']]")
old="roots=[Path(b['namespaces'][k])for k in('host','output','control','source','receipts')];total=sum(q.stat().st_size for root in roots for q in root.rglob('*')if q.is_file());require(total<2*2**30,'complete actual postclose joint archive before receipt')"
new="namespace_keys=('host','output','control','source','receipts');roots=[Path(b['namespaces'][k])for k in namespace_keys]"
assert s.count(old)==1;s=s.replace(old,new)
old="out=Path(a.output);require(out.is_absolute()and out.parent.is_dir()and not os.path.lexists(out)and out.is_relative_to(es),'fresh postclose META within E after the genuine child closure')"
new=old+"""
    # Full EOF views cover every regular file, not only known Source/build/event
    # pins. E is deliberately captured before appending this manifest; a JSON
    # manifest cannot contain its own complete hash/identity recursively.
    namespace_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}
    require(namespace_views['source']==h['complete_Source_D_freeze']and namespace_views['receipts']==h['complete_receipt_E_freeze'],'complete D remains frozen; complete E captured before this single append')
    total=sum(p['size_bytes']for view in namespace_views.values()for p in view['files']);outside=sum(p['size_bytes']for key in('source','receipts')for p in namespace_views[key]['files'])
    require(total<2*2**30 and resource_before['artifact_bytes']+outside<96*2**30,'all complete namespace fullpins counted before append')
"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("Root_postclose_external_Source_D_receipt_E_bytes=outside,Root_postclose_coverage_contract", "Root_postclose_external_Source_D_receipt_E_bytes=outside,Root_complete_postclose_HOCDE_namespace_views=namespace_views,Root_complete_postclose_HOCDE_namespace_view_contract=dict(schema='ROOT_COMPLETE_HOCDE_POSTCLOSE_FULL_EOF_VIEWS_BEFORE_OWN_E_APPEND_V1',namespace_order=list(namespace_keys),all_directories_and_regular_files_saved=True,all_regular_file_full_EOF_sha256_size_and_7_identity_saved=True,E_view_before_this_manifest_append=True,this_manifest_not_self_pinned_in_its_content=True,this_manifest_actual_fullpin_is_in_actual_Root_stdout=True,this_manifest_append_counts_in_joint_history_free_caps=True,D_namespace_never_appended=True),Root_postclose_coverage_contract")
old="write_new(out,result);resource_after=resource_checker.check();outside_after=sum(q.stat().st_size for root in roots[3:]for q in root.rglob('*')if q.is_file());require(resource_after['artifact_bytes']+outside_after<96*2**30,'postclose receipt itself counts in history96GiB/free8GiB');require(sum(q.stat().st_size for root in roots for q in root.rglob('*')if q.is_file())<2*2**30,'postclose receipt itself counts in joint archive')"
new="""write_new(out,result)
    # Re-read all five complete views after the append. H/O/C/D must be byte
    # and identity stable. E may gain exactly this new receipt and only its
    # containing directory metadata may change. No D Source is appended.
    after_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys};out_pin=fullpin(out)
    require(all(after_views[key]==namespace_views[key]for key in namespace_keys[:-1]),'postclose H/O/C/D full views unchanged across own E append')
    require(after_views['receipts']['files']==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])and set(after_views['receipts']['directories'])==set(namespace_views['receipts']['directories']),'E gains exactly own manifest with complete full EOF pin and no extra directory')
    for directory,identity in namespace_views['receipts']['directories'].items():
        current=after_views['receipts']['directories'][directory]
        require((current[:4]==identity[:4])if directory==str(out.parent)else current==identity,'only E own append directory stat timestamps/size may change')
    resource_after=resource_checker.check();outside_after=sum(p['size_bytes']for key in('source','receipts')for p in after_views[key]['files']);joint_after=sum(p['size_bytes']for view in after_views.values()for p in view['files'])
    require(resource_after['artifact_bytes']+outside_after<96*2**30,'postclose receipt itself counts in history96GiB/free8GiB');require(joint_after<2*2**30,'postclose receipt itself counts in joint archive')"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("actual_observation_manifest_pin=fullpin(out),raw_observation_manifest_pin", "actual_observation_manifest_pin=out_pin,Root_postclose_complete_namespace_views_saved_before_own_E_append=True,Root_postclose_joint_HOCDE_bytes_including_own_manifest=joint_after,Root_postclose_original_dynamic_history_resource_after=resource_after,Root_postclose_external_Source_D_receipt_E_bytes_including_own_manifest=outside_after,raw_observation_manifest_pin")
ast.parse(s);q.write_text(s)
q=P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json';j=json.loads(q.read_bytes());j['steps'][5]['complete_state_snapshot_inputs']='Use exact legacy_context_source_snapshot_request_rows from new postclose manifest for the existing admitted V2 Source request: its root_prefix equals canonical logical_prefix and is only an emitted pool path, never native directory lookup. Canonical complete_state_snapshot_inputs explicitly stores five fields event/role/root_prefix=[]/logical_prefix/input_pin.';j['postclose_complete_namespace_views']='Root_complete_postclose_HOCDE_namespace_views includes all five actual directory and regular-file full EOF 7-ID views. E is captured before this manifest append; actual Root stdout pins this manifest and reports caps including its own bytes. D is never appended.';j['true_original_Source_blockers_fixed']=['per_component_original_compiler_flags','original_suffix_group_archive_object_order','original_per_component_module_include_namespace','full_actual_postclose_five_namespace_views'];j['snapshot_prefix_clarification_is_not_an_old_execution_blocker']=True;q.write_text(json.dumps(j,indent=2)+'\n')
proof=[]
for name in('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json','ROOT_OBSERVATION_SOURCE_REQUEST_TEMPLATE.UNREADY.json','ROOT_OBSERVATION_SOURCE_ADMISSION_TEMPLATE.UNREADY.json','ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json'):
 old=(O/name).read_bytes();new=(P/name).read_bytes();ol=old.decode().splitlines(keepends=True);nl=new.decode().splitlines(keepends=True);hunks=[]
 for tag,i,j,a,b in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
  if tag!='equal':hunks.append(dict(tag=tag,old_start0=i,old_end0=j,new_start0=a,new_end0=b,old_full_lines=ol[i:j],new_full_lines=nl[a:b]))
 inv=list(nl)
 for h in reversed(hunks):assert inv[h['new_start0']:h['new_end0']]==h['new_full_lines'];inv[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(inv).encode()==old
 proof.append(dict(source_member=name,original_sha256=hashlib.sha256(old).hexdigest(),fixed_sha256=hashlib.sha256(new).hexdigest(),complete_full_inverse_hunks=hunks,whole_Source_inverse_to_original_frozen_member_equal=True))
q=P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json';j=json.loads(q.read_bytes());j.update(source_derivations=proof,true_blockers=['per_component_original_compiler_flags','original_suffix_group_archive_object_order','original_per_component_module_include_namespace','full_actual_postclose_five_namespace_views'],nonblocking_clarifications=['explicit_physical_native_root_and_logical_pool_prefix_legacy_exact4_mapping'],snapshot_prefix_old_runtime_failure_claim_withdrawn=True);q.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(status='FINAL_FOUR_TRUE_BLOCKERS_AND_NONBLOCKING_PREFIX_CLARIFICATION_WRITTEN_UNSEALED_SOURCE_ONLY',changed_original_members=len(proof),whole_byte_inverse_hunks=sum(len(p['complete_full_inverse_hunks'])for p in proof),all_original_physical_observer_and_native_archive_Source_unchanged=True,actual_execution=None)))

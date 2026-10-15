import hashlib,json,pathlib
D=pathlib.Path('/private/tmp/spot_storage_review_eighteenth_graph_20261009');R=pathlib.Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
def pin(p):
    before=p.lstat();b=p.read_bytes();after=p.lstat()
    ids=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    assert ids(before)==ids(after)
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'identity':ids(before)}
receipt=json.loads((D/'actual_post_retirement_tool_return.json').read_bytes())
assert receipt['actual_tool_result']=={'initial_chunk_id':'931783','session_id':15391,'terminal_chunk_id':'b58f51','exit_code':0,'closed':True}
assert pin(pathlib.Path(receipt['report']['path']))==receipt['report']
for name in ('executed_source','stdout','stderr','text_report'):assert pin(pathlib.Path(receipt[name]['path']))==receipt[name]
failure={'schema':'SPOT_R18_SMALL_POST_BINDING_REVIEWER_FAILURE_OBSERVATION_V1','status':'REVIEWER_ASSERTION_FAILURE_PRESERVED','actual_tool_result':{'chunk_id':'83e206','exit_code':1,'closed':True},'executed_as_heredoc':True,'executed_source':pin(D/'first_post_small_binding_83e206_exit1_executed_source.py.txt'),'observed_tool_output':'Traceback (most recent call last):\n  File "<stdin>", line 10, in <module>\nAssertionError\n','cause':'Reviewer incorrectly named Root count keys symlinks/directories. Actual preserved schema keys are symlink/directory_paths. Core actual post reader had already genuinely exited0; no business failure or retry occurred.','project_written':False,'business_executed':False}
fp=D/'first_post_small_binding_83e206_exit1_tool_return.json'
with fp.open('x')as f:json.dump(failure,f,indent=2);f.write('\n')
a=json.loads((R/'protected_before.json').read_bytes());b=json.loads((R/'protected_after.json').read_bytes())
assert a['counts']==b['counts']=={'regular':160363,'symlink':687,'directory_paths':7058}
assert a['metadata_identity_sha256']==b['metadata_identity_sha256'] and a['document_sha256']==b['document_sha256']
assert len(a['document_sha256'])==10 and a['fixed_plan_sha256']==b['fixed_plan_sha256']=='08f761505da86d66c76cf79240dc5ffcfeb98d05627f7062acd9e6d8e9d4eb31'
output={'schema':'SPOT_R18_ACTUAL_POST_RETIREMENT_FINAL_SMALL_EVIDENCE_BINDING_V1','status':'PASS','independent_graph_retained_post_report':receipt['report'],'independent_true_reader_receipt':pin(D/'actual_post_retirement_tool_return.json'),'Root_protected_before':pin(R/'protected_before.json'),'Root_protected_after':pin(R/'protected_after.json'),'Root_protected_after_true_tool_as_observed_by_Root':{'initial_chunk_id':'b37a8f','session_id':29496,'terminal_chunk_id':'fd3e7d','exit_code':0,'closed':True},'Root_whole_other_files_metadata_identity_equal':True,'Root_original_README_progress_R9_ten_fullSHA_equal':True,'whole_protected_counts':a['counts'],'preserved_reviewer_only_small_binding_failure':pin(fp),'original_audit_evidence_not_rewritten':True,'new_scientific_credit':False,'only_TMP_written':True}
p=D/'ACTUAL_POST_RETIREMENT_FINAL_BINDING.json'
with p.open('x')as f:json.dump(output,f,indent=2);f.write('\n')
names=('review_actual_post_retirement_readonly.py','actual_post_retirement.stdout','actual_post_retirement.stderr','ACTUAL_POST_RETIREMENT_REPORT.json','ACTUAL_POST_RETIREMENT_REPORT.txt','actual_post_retirement_tool_return.json','first_post_small_binding_83e206_exit1_executed_source.py.txt','first_post_small_binding_83e206_exit1_tool_return.json','finalize_actual_post_small_binding_readonly.py','ACTUAL_POST_RETIREMENT_FINAL_BINDING.json')
manifest={'schema':'SPOT_R18_ACTUAL_POST_RETIREMENT_SMALL_EVIDENCE_LIST_V1','status':'PASS','files':[pin(D/n)for n in names],'only_TMP_written':True}
mp=D/'actual_post_small_evidence_manifest.json'
with mp.open('x')as f:json.dump(manifest,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','report':receipt['report'],'receipt':pin(D/'actual_post_retirement_tool_return.json'),'binding':pin(p),'manifest':pin(mp)}))

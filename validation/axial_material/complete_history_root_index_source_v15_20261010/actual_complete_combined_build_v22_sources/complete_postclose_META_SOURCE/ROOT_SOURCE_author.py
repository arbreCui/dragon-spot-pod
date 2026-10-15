from pathlib import Path
import ast, hashlib, json

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
OLD=B/'actual_complete_combined_build_v21_receipts/sealed_postclose_failure_META_SOURCE_design/write_actual_build_postclose_META.py'
DEST=Path('/private/tmp/spot_v22_complete_build_postclose_META_ROOT_SOURCE_20261010_6ed606')
def pin(p):
    s=p.lstat();raw=p.read_bytes();t=p.lstat()
    ids=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    assert ids(s)==ids(t) and not p.is_symlink()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':ids(s)}
assert not DEST.exists()
orig=OLD.read_bytes();text=orig.decode();rows=[]
changes=[
('V21','V22'),('v21','v22'),
('023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5','09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'),
('ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196','cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269'),
('80d67cd194eed1d229e46cd5512df9ba4b00954e7f6e7b36dd8ea6902851d6af','8ad01e54e6ed89911c56d1fe04284e5f39f81ebe0ae9aa060253b9378df346b1'),
('7e340a31596aa58518ebde4231bd3542554acb0a4ea1888f1df7ea14bec50dcf','96ff567a30a451af02767c153ce8f0213c9f5b6e7330eb48b1ca9c69a992b61c'),
('combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py','combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py'),
('dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7','cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'),
('Root_actual_complete_graph_private_verifier_helper_admission_v22.json','Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'),
('29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2','89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816')]
for before,after in changes:
    count=text.count(before);assert count>0
    text=text.replace(before,after);rows.append({'before':before,'after':after,'count':count})
restored=text
for row in reversed(rows):
    assert restored.count(row['after'])==row['count']
    restored=restored.replace(row['after'],row['before'])
assert restored.encode()==orig
compile(text,'write_actual_build_postclose_META.py','exec')
def funcs(raw):
    return {n.name:ast.get_source_segment(raw.decode(),n) for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
oldfunc=funcs(orig);newfunc=funcs(text.encode());assert oldfunc.keys()==newfunc.keys()
unchanged=[k for k in oldfunc if oldfunc[k]==newfunc[k]]
changed=[k for k in oldfunc if oldfunc[k]!=newfunc[k]]
assert changed==['compare_source_freeze','expected_commands','success_checks','main'],changed
for name in changed:
    candidate=oldfunc[name]
    for before,after in changes:candidate=candidate.replace(before,after)
    assert candidate==newfunc[name]
DEST.mkdir()
(DEST/'write_actual_build_postclose_META.py').write_text(text)
(DEST/'original_complete_V21_postclose_META_writer.byte_exact.py').write_bytes(orig)
(DEST/'ROOT_SOURCE_author.py').write_bytes(Path(__file__).read_bytes())
first={'schema':'ROOT_METADATA_SOURCE_AUTHOR_FIRST_ASSERTION_ATTEMPT_V1','actual_tool_return':{'chunk_id':'0786a5','wall_time_seconds':0.000006958,'exit_code':1,'original_token_count':23,'output':'Traceback (most recent call last):\n  File "<stdin>", line 25, in <module>\nAssertionError\n'},'closed':True,'observed_terminal':True,'failure':'Source-only function-text delta inventory omitted expected_commands comment literal; actual four family-literal-only functions, no destination created','business_numeric_executed':False}
(DEST/'FIRST_SOURCE_AUTHOR_FUNCTION_COMMENT_INVENTORY_FAILURE.json').write_text(json.dumps(first,indent=2)+'\n')
proof={'schema':'ROOT_V22_COMPLETE_BUILD_POSTCLOSE_META_WRITER_SOURCE_INVERSE_V1','source_only':True,'original':pin(OLD),'actual_source':pin(DEST/'write_actual_build_postclose_META.py'),'finite_hunks':rows,'whole_byte_inverse_to_original':True,'full_original_functions':len(oldfunc),'byte_exact_functions':unchanged,'only_family_literal_changed_functions':changed,'original_complete_success_and_failure_modes_retained':True,'original_caps':[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0],'project_or_guard_API_executed':False,'numeric_executed':False,'whole_INPUT_native_science_qualified':False}
(DEST/'SOURCE_inverse.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
members={p.name:pin(p) for p in sorted(DEST.iterdir())}
(DEST/'MANIFEST.json').write_text(json.dumps({'schema':'ROOT_V22_COMPLETE_BUILD_POSTCLOSE_META_WRITER_SOURCE_PACKAGE_V1','source_only':True,'members':members,'member_count':len(members),'business_numeric_executed':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'manifest':pin(DEST/'MANIFEST.json'),'writer':pin(DEST/'write_actual_build_postclose_META.py'),'original_writer':pin(OLD),'finite_hunks':len(rows),'full_functions':len(oldfunc),'byte_exact_functions':len(unchanged),'family_literal_changed_functions':changed,'business_numeric_executed':False}))

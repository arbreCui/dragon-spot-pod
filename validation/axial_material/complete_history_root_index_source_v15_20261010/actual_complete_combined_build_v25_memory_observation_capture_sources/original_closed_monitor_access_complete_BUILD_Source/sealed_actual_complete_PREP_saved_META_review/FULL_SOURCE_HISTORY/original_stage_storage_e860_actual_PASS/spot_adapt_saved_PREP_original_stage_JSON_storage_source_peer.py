"""Source-only original stage dump_json sort_keys storage mirror adapter."""
import ast,hashlib,json,os,stat
from pathlib import Path
OLD=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_CLOSED_RECEIPTS_SOURCE_UNREADY_20261010')
NEW=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ORIGINAL_STAGE_JSON_STORAGE_SOURCE_UNREADY_20261010')
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def segment(s,n):return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
p=OLD/'review_actual_complete_PREP_saved_META_stdlib.py';op=pin(p);assert op['sha256']=='200fb2289b377b85915548a740d8d43e6717469852e4ce4cc243d81d82041710'
old=p.read_text()
a="    need(type(stages) is list and len(stages)==1 and exact(stages,h['stage_records']),'one complete saved PREP stage')\n"
b="""    stage_writer_text,stage_writer_tree=source(ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py')
    dump_node=next(n for n in stage_writer_tree.body if isinstance(n,ast.FunctionDef) and n.name=='dump_json')
    need(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='json' and n.func.attr=='dumps' and any(k.arg=='sort_keys' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords) for n in ast.walk(dump_node)),'original production stage metadata writer uses complete recursive sort_keys storage')
    stored_host_stages=strict_bytes(json.dumps(h['stage_records'],sort_keys=True,allow_nan=False))
    need(type(stages) is list and len(stages)==1 and exact(stages,stored_host_stages),'one complete saved PREP stage exact original storage mapping order types sequences and float bits')
"""
assert old.count(a)==1;new=old.replace(a,b,1);nt=ast.parse(new);ot=ast.parse(old)
assert new.count(b)==1 and new.replace(b,a,1)==old and ast.dump(ast.parse(new.replace(b,a,1)),include_attributes=False)==ast.dump(ot,include_attributes=False)
od={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)};nd={n.name:n for n in nt.body if isinstance(n,ast.FunctionDef)}
assert set(od)==set(nd) and len(od)==24 and all(segment(new,nd[k])==segment(old,v) for k,v in od.items() if k!='review')
assert segment(new,nd['review']).replace(b,a,1)==segment(old,od['review'])
assert all(ast.dump(n,include_attributes=False)==ast.dump(m,include_attributes=False) for n,m in zip([x for x in ot.body if not isinstance(x,ast.FunctionDef)],[x for x in nt.body if not isinstance(x,ast.FunctionDef)]))
assert not os.path.lexists(NEW);NEW.mkdir();out=NEW/p.name;out.write_text(new)
(NEW/('original_'+p.name)).write_bytes(p.read_bytes());assert pin(p)==op
for n in ('ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json','seal_actual_complete_PREP_saved_META_review_stdlib.py','COMPLETE_HISTORICAL_TRANSFER_CURRENT_RETENTION_SOURCE_INVERSE.json','SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json','ACTUAL_WRITER_RECEIPT_BASENAME_SOURCE_INVERSE.json','ACTUAL_CLOSED_RECEIPTS_COMPLETE_SOURCE_CONTRACT_INVERSE.json'):
 q=OLD/n;qp=pin(q);(NEW/n).write_bytes(q.read_bytes());assert pin(q)==qp
(NEW/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
checks=[dict(check=k,passed=True) for k in ('complete_original200_Source_EOF_unchanged','only_stage_metadata_writer_defined_sort_keys_mirror_block','original_exact_type_mapping_order_sequence_floatbit_comparator_unchanged','all23_other_original_functions_full_byte_unchanged','all_original_globals_Q_helper_physics_thresholds_caps_MRO_andcredit_unchanged','whole_byte_and_AST_inverse200','no_saved_reviewer_or_candidate_executed_by_Source_author')]
v=dict(schema='INDEPENDENT_V25_SAVED_PREP_ORIGINAL_STAGE_SORT_KEYS_STORAGE_SOURCE_INVERSE_V1',status='SOURCE_ONLY_ORIGINAL_STAGE_STORAGE_READY_ACTUAL_SAVED_REVIEW_NOT_EXECUTED',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],original_reviewer_pin=op,derived_reviewer_pin=pin(out),full_original_copy_pin=pin(NEW/('original_'+p.name)),complete_byte_inverse=True,complete_AST_inverse=True,one_exact_finite_replacement=dict(old=a,new=b,count=1),original_exact_comparator_unchanged=True,candidate_helper_API_compiler_native_material_numeric_or_saved_PREP_reviewer_executed=False,actual_saved_PREP_review_terminal=None,actual_saved_PREP_PASS_report=None,whole_INPUT_BUILD_native_RSS_physics_AAA_ABA_qualified=False)
write(NEW/'ORIGINAL_STAGE_SORT_KEYS_COMPLETE_SOURCE_INVERSE.json',v)
print(json.dumps(dict(source_only=True,reviewer_pin=pin(out),inverse_pin=pin(NEW/'ORIGINAL_STAGE_SORT_KEYS_COMPLETE_SOURCE_INVERSE.json'),check_count=len(checks),all_checks_typed_true=True,saved_PREP_reviewer_executed=False)))

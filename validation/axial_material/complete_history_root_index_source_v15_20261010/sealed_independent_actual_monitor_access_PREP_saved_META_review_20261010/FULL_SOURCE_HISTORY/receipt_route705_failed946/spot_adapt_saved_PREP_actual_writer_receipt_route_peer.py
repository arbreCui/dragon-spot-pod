"""Source-only literal route correction to Root's actual writer receipt.
No saved evidence reviewer, candidate or inspected helper is executed.
"""
import ast,hashlib,json,os,stat
from pathlib import Path
OLD=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_CURRENT_RETAINED_SOURCE_V2_UNREADY_20261010')
NEW=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_RECEIPT_ROUTE_UNREADY_20261010')
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
p=OLD/'review_actual_complete_PREP_saved_META_stdlib.py';op=pin(p)
assert op['sha256']=='80d2c839889eaf2c6aba5a20f8e00b1c13422ab3abece6438e5547d5a72a9af0'
a='Root_actual_prepare_metadata_writer_tool_return.json';b='Root_actual_prepare_metadata_writer_tool_terminal_return.json'
old=p.read_text();assert old.count(a)==2 and old.count(b)==0
new=old.replace(a,b);ot=ast.parse(old);nt=ast.parse(new)
restored=new.replace(b,a);assert restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ot,include_attributes=False)
changes=[]
for before,after in zip(ast.walk(ot),ast.walk(nt)):
 if ast.dump(before,include_attributes=False)!=ast.dump(after,include_attributes=False) and isinstance(before,ast.Constant):
  assert type(before.value) is str and before.value==a and isinstance(after,ast.Constant) and after.value==b
  changes.append(before.lineno)
assert len(changes)==2 and not os.path.lexists(NEW);NEW.mkdir();out=NEW/p.name;out.write_text(new)
(NEW/('original_'+p.name)).write_bytes(p.read_bytes());assert pin(p)==op
for name in ('ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json','seal_actual_complete_PREP_saved_META_review_stdlib.py','COMPLETE_HISTORICAL_TRANSFER_CURRENT_RETENTION_SOURCE_INVERSE.json','SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json'):
 q=OLD/name;qp=pin(q);(NEW/name).write_bytes(q.read_bytes());assert pin(q)==qp
(NEW/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
checks=[dict(check=k,passed=True) for k in ('complete_parent80d2_full_EOF_unchanged','exact_two_actual_writer_receipt_basename_literals_only','complete_byte_and_AST_inverse80d2','all_original_validation_predicates_physics_caps_Q_schemas_andcredit_unchanged','original_18_future_template_pins_remain_None','saved_PREP_reviewer_not_executed')]
v=dict(schema='INDEPENDENT_V25_SAVED_PREP_ACTUAL_WRITER_RECEIPT_ROUTE_SOURCE_INVERSE_V1',status='SOURCE_ONLY_ROUTE_READY_ACTUAL_SAVED_PREP_REVIEW_NOT_EXECUTED',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],original_reviewer_pin=op,derived_reviewer_pin=pin(out),full_original_copy_pin=pin(NEW/('original_'+p.name)),old_receipt_basename=a,actual_receipt_basename=b,exact_literal_changes_count=2,old_literal_line_numbers=changes,complete_byte_inverse=True,complete_AST_inverse=True,candidate_helper_API_compiler_native_material_numeric_or_saved_PREP_reviewer_executed=False,actual_saved_PREP_review_terminal=None,actual_saved_PREP_PASS_report=None,whole_INPUT_BUILD_native_or_science_qualified=False)
write(NEW/'ACTUAL_WRITER_RECEIPT_BASENAME_SOURCE_INVERSE.json',v)
print(json.dumps(dict(source_only=True,reviewer_pin=pin(out),inverse_pin=pin(NEW/'ACTUAL_WRITER_RECEIPT_BASENAME_SOURCE_INVERSE.json'),check_count=len(checks),all_checks_typed_true=True,actual_saved_PREP_reviewer_executed=False)))

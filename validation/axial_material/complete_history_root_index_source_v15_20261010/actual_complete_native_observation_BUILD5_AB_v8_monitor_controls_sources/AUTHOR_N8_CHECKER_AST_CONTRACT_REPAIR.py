"""Repair an author checker AST comparison, without candidate imports/execution."""
import ast
from pathlib import Path
import shutil

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
path=P/'AUTHOR_N8_FINAL_SOURCE_CHECKER.py'
backup=P/'AUTHOR_DRAFT_ERRORS/author_checker_before_AST_contract_compare_repair.Source.py'
shutil.copy2(path,backup)
text=path.read_text()
old="assigns={n.targets[0].id:ast.literal_eval(n.value)for n in rt.body"
new="assigns={n.targets[0].id:ast.dump(n.value,include_attributes=False)for n in rt.body"
assert text.count(old)==1;text=text.replace(old,new,1)
old="oldassign={n.targets[0].id:ast.literal_eval(n.value)for n in mother.body"
new="oldassign={n.targets[0].id:ast.dump(n.value,include_attributes=False)for n in mother.body"
assert text.count(old)==1;text=text.replace(old,new,1)
ast.parse(text);path.write_text(text)
print('{"status":"AUTHOR_CHECKER_AST_COMPARE_REPAIR_SOURCE_ONLY","candidate_execution":false}')

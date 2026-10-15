"""Final author-only Source refinement and AST/byte verification. No candidate execution."""
from pathlib import Path
import ast,hashlib,json,stat,sys
P=Path(sys.argv[1])
assert P.is_relative_to(Path('/private/tmp')) and P.name=='axmat_V25_complete_BUILD_memory_observation_V2_finite_UNREADY_Source_919_qh5t'
V1=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes();assert ident(q.lstat())==ident(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s))
def dump(n):return ast.dump(n,include_attributes=False)
def save(name,x):
    q=P/name;assert not q.exists();q.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n');return pin(q)
checks=[]
def check(name,test,detail=None):
    assert type(test) is bool
    checks.append(dict(check=name,passed=test,evidence=detail))
    assert test,name
old_manifest=json.loads((V1/'MANIFEST.json').read_text())
before={rel:pin(V1/rel) for rel in old_manifest['members']}
parent_pin=pin(V1/'MANIFEST.json')
dirs={str(q.relative_to(V1)):ident(q.lstat()) for q in [V1]+sorted(V1.rglob('*')) if q.is_dir()}
initial=json.loads((P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2.json').read_text())
initial_inverse=json.loads((P/'V2_COMPLETE_THREE_ROLE_SIX_FUNCTION_WHOLE_SOURCE_INVERSES.json').read_text())
roles={role:row['relative_path'] for role,row in initial_inverse['roles'].items()}
changed={'prepare_host','build_host','build_writer'}
for role in changed:
    q=P/roles[role];text=q.read_text()
    check(role+'_initial_buffered_descriptor_anchor_exactly_two',text.count("os.fdopen(fd,'rb',closefd=False)")==2)
    # Final Source refinement is confined to the same two changed diagnostic functions.
    q.write_text(text.replace("os.fdopen(fd,'rb',closefd=False)","os.fdopen(fd,'rb',buffering=0,closefd=False)"))
proof={}
for role,rel in roles.items():
    old=(V1/rel).read_text();current=(P/rel).read_text()
    ot=ast.parse(old);ct=ast.parse(current)
    old_defs=[n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    new_defs=[n for n in ct.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    changes=[];restored=current
    check(role+'_all_definitions_in_original_occurrence_order',[(type(n).__name__,n.name) for n in old_defs]==[(type(n).__name__,n.name) for n in new_defs])
    for a,b in zip(old_defs,new_defs):
        old_s=ast.get_source_segment(old,a)+'\n';new_s=ast.get_source_segment(current,b)+'\n'
        if old_s!=new_s:
            check(role+'_'+a.name+'_changed_only_allowed_diagnostic_function',role in changed and a.name in ('memory_diagnostic_pin','memory_diagnostic_rows'))
            changes.append(dict(function=a.name,old=old_s,new=new_s,exact_occurrences=1))
    for h in reversed(changes):
        assert restored.count(h['new'])==1
        restored=restored.replace(h['new'],h['old'],1)
    check(role+'_whole_fullbyte_inverse_to_original_V1',restored.encode()==old.encode())
    check(role+'_whole_AST_inverse_to_original_V1',dump(ast.parse(restored))==dump(ot))
    check(role+'_only_two_changed_or_entire_byteexact', [h['function'] for h in changes]==(['memory_diagnostic_pin','memory_diagnostic_rows'] if role in changed else []))
    mask_old=ast.parse(old);mask_new=ast.parse(current)
    if role in changed:
        mask_old.body=[n for n in mask_old.body if not isinstance(n,ast.FunctionDef) or n.name not in ('memory_diagnostic_pin','memory_diagnostic_rows')]
        mask_new.body=[n for n in mask_new.body if not isinstance(n,ast.FunctionDef) or n.name not in ('memory_diagnostic_pin','memory_diagnostic_rows')]
    check(role+'_all_other_full_module_AST_byte_equivalent',dump(mask_old)==dump(mask_new))
    if role in changed:
        defs={n.name:n for n in ct.body if isinstance(n,ast.FunctionDef)}
        f=ast.get_source_segment(current,defs['memory_diagnostic_pin']);g=ast.get_source_segment(current,defs['memory_diagnostic_rows'])
        check(role+'_preopen_lstat_regular_singlelink_size_le_1MiB',f.index('not 0<=s.st_size<=bound')<f.index('fd=os.open') and 'bound!=1048576' in f and 'not stat.S_ISREG(s.st_mode)' in f and 's.st_nlink!=1' in f)
        check(role+'_no_follow_nonblock_and_unbuffered_one_maxplusone_read',f.count("os.fdopen(fd,'rb',buffering=0,closefd=False)")==1 and f.count('stream.read(bound+1)')==1 and 'os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK' in f and 'iter(' not in f)
        check(role+'_full_7ID_same_descriptor_path_and_actual_size',f.count('os.fstat(fd)')==2 and 'opened_ident!=ident' in f and 'finished_ident!=ident' in f and 'after!=ident' in f and 'len(raw)>bound or len(raw)!=ident[4]' in f)
        check(role+'_full_bounded_SHA_and_original_four_field_pin','sha256=hashlib.sha256(raw).hexdigest(),size_bytes=ident[4],identity=ident' in f)
        check(role+'_parser_stat_regular_before_same_no_follow_descriptor',g.index('current=path.lstat()')<g.index('fd=os.open') and 'current_ident!=before[\'identity\']' in g and 'opened_ident!=before[\'identity\']' in g)
        check(role+'_parser_exact_one_unbuffered_total_maxplusone_read',g.count("os.fdopen(fd,'rb',buffering=0,closefd=False)")==1 and g.count("stream.read(contract['max_bytes']+1)")==1 and "len(raw)>contract['max_bytes'] or len(raw)!=before['size_bytes']" in g)
        check(role+'_parser_all_bytes_SHA_descriptor_path_7ID_protected',g.count('os.fstat(fd)')==2 and "finished_ident!=before['identity']" in g and "hashlib.sha256(raw).hexdigest()!=before['sha256']" in g and 'after!=before' in g)
        handlers=[n for n in ast.walk(defs['memory_diagnostic_rows']) if isinstance(n,ast.ExceptHandler)]
        check(role+'_only_validation_errors_caught_failure_success_reraises',[dump(h.type) for h in handlers]==[dump(ast.parse('(ValueError, TypeError, KeyError, OverflowError)',mode='eval').body)] and '        if success:raise\n' in g)
        check(role+'_OSError_KeyboardInterrupt_SystemExit_and_BaseException_not_caught',not any(isinstance(n,ast.Name) and n.id in ('OSError','KeyboardInterrupt','SystemExit','BaseException') for h in handlers for n in ast.walk(h.type)))
        check(role+'_both_descriptors_close_in_finally',sum(isinstance(n,ast.Try) and any(isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Attribute) and x.value.func.attr=='close' for x in n.finalbody) for n in ast.walk(defs['memory_diagnostic_pin']))==1 and sum(isinstance(n,ast.Try) and any(isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Attribute) and x.value.func.attr=='close' for x in n.finalbody) for n in ast.walk(defs['memory_diagnostic_rows']))==1)
    old_None={n.targets[0].id for n in ot.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    new_None={n.targets[0].id for n in ct.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    check(role+'_future_None_slots_unchanged',old_None==new_None)
    proof[role]=dict(relative_path=rel,parent_V1_pin=before[rel],current_V2_pin=pin(P/rel),whole_byte_and_AST_inverse=True,definition_count=len(new_defs),all_original_future_None_globals=sorted(new_None),exact_finite_transforms=changes)
unmodified={rel:pin(P/rel) for rel in before if rel not in {roles[r] for r in changed}}
check('all_64_unmodified_V1_members_full_complete_bytes',len(unmodified)==64 and all(q['sha256']==before[rel]['sha256'] and q['size_bytes']==before[rel]['size_bytes'] for rel,q in unmodified.items()))
check('original_V1_actual_full_manifest_bytes_retained', (P/'V1_SOURCE_PROVENANCE/ORIGINAL_V1_COMPLETE_MANIFEST.byte_exact.json').read_bytes()==(V1/'MANIFEST.json').read_bytes())
count=0
for q in sorted(P.rglob('*.py')):ast.parse(q.read_text());count+=1
check('all_52_current_full_Source_texts_AST_parsed_no_exec',count==52)
check('original_V1_full_EOF_SHA_7ID_before_after_unchanged',{rel:pin(V1/rel) for rel in before}==before and pin(V1/'MANIFEST.json')==parent_pin)
check('original_V1_all_full_directory_identities_unchanged',{str(q.relative_to(V1)):ident(q.lstat()) for q in [V1]+sorted(V1.rglob('*')) if q.is_dir()}==dirs)
prov=json.loads((P/'V2_ACTUAL_V1_FAILED_REVIEW_AND_ORIGINAL_SOURCE_FULLPIN_PROVENANCE.json').read_text())
check('genuine_V1_FAIL_report_and_terminal_exact_current_fullpins',pin(prov['actual_failed_V1_review']['path'])==prov['actual_failed_V1_review'] and pin(prov['actual_failed_V1_review_terminal']['path'])==prov['actual_failed_V1_review_terminal'] and prov['V1_is_failed_not_V2_admission'] is True)
inverse=save('V2_FINAL_COMPLETE_THREE_ROLE_SIX_FUNCTION_WHOLE_SOURCE_INVERSES.json',dict(schema='V25_BUILD_MEMORY_OBSERVATION_V2_FINAL_FINITE_WHOLE_BYTE_AST_INVERSE_V1',source_only=True,parent_manifest_pin=parent_pin,roles=proof,unchanged_V1_member_fullpins=unmodified,exact_changed_roles=sorted(changed),exact_changed_functions=['memory_diagnostic_pin','memory_diagnostic_rows'],hunk_count=6,unbuffered_descriptor_reads=True))
source_roles=['canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer']
report=dict(schema='AUTHOR_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_V2_FINAL_FINITE_SOURCE_ONLY_REPORT_V1',status='UNREADY_SOURCE_ONLY_FINITE_V2_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW',source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=all(x['passed'] is True for x in checks),blockers=[],qualified_role_Source_pins={r:pin(P/roles[r]) for r in source_roles},qualified_utility_Source_pins={r:pin(P/roles[r]) for r in roles if r not in source_roles},parent_V1_manifest_pin=parent_pin,actual_failed_V1_review_pin=prov['actual_failed_V1_review'],complete_inverse_pin=inverse,actual_fullpin_provenance=pin(P/'V2_ACTUAL_V1_FAILED_REVIEW_AND_ORIGINAL_SOURCE_FULLPIN_PROVENANCE.json'),initial_author_report_pin=pin(P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2.json'),initial_2399f6_actual_tool_return=pin(P/'ACTUAL_AUTHOR_V2_INITIAL_SOURCE_TOOL_RETURN.json'),initial_buffered_Source_report_is_intermediate_not_current_final=True,exact_changed_roles=sorted(changed),exact_changed_functions=['memory_diagnostic_pin','memory_diagnostic_rows'],exact_hunk_count=6,unchanged_V1_member_count=64,future_environment_witness=None,future_business_pins=None,all_candidate_API_helper_guard_resource_numeric_or_business_executed=False,project_or_ART_or_original_packages_written=False,diagnostic_RUNTIME_controls_executed=False,whole_INPUT_build_RSS_native_or_science_qualified=False,limitations=initial['remaining_actual_limits'])
rp=save('AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2_FINAL.json',report)
print(json.dumps(dict(source_only=True,check_count=len(checks),all_checks_typed_true=True,current_final_report_pin=rp,current_final_inverse_pin=inverse,roles=report['qualified_role_Source_pins'],candidate_or_business_executed=False),ensure_ascii=False))


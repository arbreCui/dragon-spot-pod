"""Author-only finite Source derivative; never imports or executes any candidate."""
from pathlib import Path
import ast
import hashlib
import json
import os
import shutil
import stat
import sys

PARENT=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
FAILED=Path('/private/tmp/axmat_V25_memory_observation_INDEPENDENT_review_ZgGEhb')
PARENT_SHA='fff5b15ae51888bd3ff310597a44ce2381ecdd0f2bb858ee12c4c0395f6385bc'
FAILED_SHA='4c449f9154596ffe071e30d535c0f817c82ad5088bcc151090164d0d8c967189'
FAILED_MANIFEST_SHA='8743e7408650050deef1cd1018f13c0753a25e0a6ae676ee8b3e4fd927dc5bf8'
P=Path(sys.argv[1])
assert P.is_dir() and P.is_relative_to(Path('/private/tmp')) and P!=PARENT
CHECKS=[]
def check(name,value,evidence=None):
    assert type(value) is bool
    CHECKS.append(dict(check=name,passed=value,evidence=evidence))
    if not value:raise AssertionError(name)
def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);s=path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not path.is_symlink()
    raw=path.read_bytes()
    assert identity(path.lstat())==identity(s) and len(raw)==s.st_size
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def write(name,value):
    q=P/name
    assert not q.exists()
    q.parent.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n'
    q.write_bytes(raw)
    return pin(q)
def dump(node):return ast.dump(node,include_attributes=False)
def definition_rows(text):
    return [(n.name,type(n).__name__,ast.get_source_segment(text,n),dump(n)) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]

parent_manifest_pin=pin(PARENT/'MANIFEST.json')
check('actual_V1_complete_manifest_exact_SHA',parent_manifest_pin['sha256']==PARENT_SHA)
manifest=json.loads((PARENT/'MANIFEST.json').read_text())
check('actual_V1_member_count',type(manifest['member_count']) is int and manifest['member_count']==67 and len(manifest['members'])==67)
before={name:pin(PARENT/name) for name in manifest['members']}
check('actual_V1_all_67_members_full_EOF_exact_7ID',before==manifest['members'])
check('actual_V1_full_file_set',set(str(q.relative_to(PARENT)) for q in PARENT.rglob('*') if q.is_file())==set(before)|{'MANIFEST.json'})
old_dirs={str(q.relative_to(PARENT)):identity(q.lstat()) for q in [PARENT]+sorted(PARENT.rglob('*')) if q.is_dir()}
failed_pin=pin(FAILED/'REVIEW.json')
failed_manifest_pin=pin(FAILED/'MANIFEST.json')
check('genuine_failed_independent_V1_report_and_manifest_SHA',failed_pin['sha256']==FAILED_SHA and failed_manifest_pin['sha256']==FAILED_MANIFEST_SHA)
failed=json.loads((FAILED/'REVIEW.json').read_text())
check('V1_failed_scope_not_relabelled_PASS',failed['check_count']==121 and failed['all_checks_typed_true'] is False and len(failed['blockers'])==2 and sum(x['passed'] is True for x in failed['checks'])==115)
failed_tool_pin=pin(FAILED/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json')
failed_tool=json.loads((FAILED/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json').read_text())
terminal=failed_tool['terminal_tool_return']
check('V1_genuine_46e34b_closed_int1_retained',failed_tool['closed'] is True and failed_tool['observed_terminal'] is True and failed_tool['session_repolled_after_close'] is False and failed_tool['actual_terminal_chunk']=='46e34b' and type(terminal['exit_code']) is int and terminal['exit_code']==1 and 'session_id' not in terminal and terminal['chunk_id']=='46e34b')
actual_failed=json.loads(terminal['output'])
check('V1_raw_actual_scope_121_115_six_false',actual_failed['check_count']==121 and actual_failed['passed_count']==115 and len(actual_failed['failed_checks'])==6)

# Every original member is retained in place; only three current role texts are changed.
for name in before:
    q=P/name
    check_name=None
    assert not q.exists()
    q.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(PARENT/name,q)
write('V1_SOURCE_PROVENANCE/ORIGINAL_V1_COMPLETE_MANIFEST.byte_exact.json',manifest)
# Preserve the literal manifest byte stream, not a reserialization.
provenance=P/'V1_SOURCE_PROVENANCE/ORIGINAL_V1_COMPLETE_MANIFEST.byte_exact.json'
provenance.write_bytes((PARENT/'MANIFEST.json').read_bytes())
check('V1_manifest_full_literal_bytes_retained',provenance.read_bytes()==(PARENT/'MANIFEST.json').read_bytes())

previous=json.loads((PARENT/'COMPLETE_SOURCE_INVERSES.json').read_text())
roles=previous['role_current_paths']
check('all_original_14_roles_preserved',len(roles)==14)
changed={'prepare_host','build_host','build_writer'}
new_pin="""def memory_diagnostic_pin(path):
    path=Path(path);s=path.lstat()
    ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if path.is_symlink() or not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('ordinary single-link diagnostic required')
    bound=BUILD_MEMORY_DIAGNOSTIC_CONTRACT['max_bytes']
    if type(bound) is not int or bound!=1048576 or type(s.st_size) is not int or not 0<=s.st_size<=bound:raise ValueError('diagnostic pre-open size exceeds reserved byte bound')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        opened=os.fstat(fd);opened_ident=[opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns]
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink!=1 or opened_ident!=ident:raise ValueError('diagnostic no-follow descriptor differs from pre-open identity')
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(bound+1)
        if len(raw)>bound or len(raw)!=ident[4]:raise ValueError('diagnostic bounded full EOF bytes differ from exact stat size')
        finished=os.fstat(fd);finished_ident=[finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns]
        if finished_ident!=ident:raise ValueError('diagnostic descriptor changed during bounded full EOF pin')
    finally:
        os.close(fd)
    s=path.lstat();after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if after!=ident:raise ValueError('full EOF diagnostic changed during pin')
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=ident[4],identity=ident)
"""
old_read="""        if before['size_bytes']>contract['max_bytes']:raise ValueError('diagnostic exceeds reserved byte bound')
        with path.open('rb') as stream:raw=stream.read(contract['max_bytes']+1)
        if len(raw)!=before['size_bytes']:raise ValueError('diagnostic bounded read differs from full pin')
"""
new_read="""        if type(before['size_bytes']) is not int or not 0<=before['size_bytes']<=contract['max_bytes']:raise ValueError('diagnostic exceeds reserved byte bound')
        current=path.lstat();current_ident=[current.st_dev,current.st_ino,current.st_mode,current.st_nlink,current.st_size,current.st_mtime_ns,current.st_ctime_ns]
        if path.is_symlink() or not stat.S_ISREG(current.st_mode) or current.st_nlink!=1 or current_ident!=before['identity']:raise ValueError('diagnostic pre-open parser identity changed')
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        try:
            opened=os.fstat(fd);opened_ident=[opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns]
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink!=1 or opened_ident!=before['identity']:raise ValueError('diagnostic parser no-follow descriptor identity changed')
            with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(contract['max_bytes']+1)
            if len(raw)>contract['max_bytes'] or len(raw)!=before['size_bytes']:raise ValueError('diagnostic bounded read differs from full pin')
            finished=os.fstat(fd);finished_ident=[finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns]
            if finished_ident!=before['identity']:raise ValueError('diagnostic parser descriptor changed during read')
        finally:
            os.close(fd)
        current=path.lstat();current_ident=[current.st_dev,current.st_ino,current.st_mode,current.st_nlink,current.st_size,current.st_mtime_ns,current.st_ctime_ns]
        if current_ident!=before['identity'] or hashlib.sha256(raw).hexdigest()!=before['sha256']:raise ValueError('diagnostic parser full SHA or exact identity changed')
"""
proof={}
for role,rel in roles.items():
    old=(PARENT/rel).read_text()
    text=old
    transforms=[]
    if role in changed:
        tree=ast.parse(old)
        functions={n.name:ast.get_source_segment(old,n)+'\n' for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('memory_diagnostic_pin','memory_diagnostic_rows')}
        check(role+'_original_two_named_functions_complete',set(functions)=={'memory_diagnostic_pin','memory_diagnostic_rows'})
        check(role+'_original_parser_read_anchor_exact_once',functions['memory_diagnostic_rows'].count(old_read)==1)
        check(role+'_original_BaseException_anchor_exact_once',functions['memory_diagnostic_rows'].count('    except BaseException as error:\n')==1)
        new_rows=functions['memory_diagnostic_rows'].replace(old_read,new_read).replace('    except BaseException as error:\n','    except (ValueError, TypeError, KeyError, OverflowError) as error:\n')
        for name,replacement in [('memory_diagnostic_pin',new_pin),('memory_diagnostic_rows',new_rows)]:
            original=functions[name]
            check(role+'_'+name+'_whole_transform_single_occurrence',text.count(original)==1)
            text=text.replace(original,replacement,1)
            transforms.append(dict(function=name,old=original,new=replacement,exact_occurrences=1))
        (P/rel).write_text(text)
    restored=text
    for transform in reversed(transforms):
        check(role+'_'+transform['function']+'_inverse_single_occurrence',restored.count(transform['new'])==1)
        restored=restored.replace(transform['new'],transform['old'],1)
    check(role+'_whole_byte_inverse',restored.encode()==old.encode())
    check(role+'_whole_AST_inverse',dump(ast.parse(restored))==dump(ast.parse(old)))
    old_rows=definition_rows(old);new_rows=definition_rows(text)
    check(role+'_all_definition_occurrences_names_and_types_preserved',[(x[0],x[1]) for x in old_rows]==[(x[0],x[1]) for x in new_rows])
    unchanged=[a==b for a,b in zip(old_rows,new_rows) if a[0] not in ('memory_diagnostic_pin','memory_diagnostic_rows') or role not in changed]
    check(role+'_all_other_definition_bytes_and_AST_preserved',all(unchanged))
    check(role+'_exact_changed_definitions', [a[0] for a,b in zip(old_rows,new_rows) if a!=b]==(['memory_diagnostic_pin','memory_diagnostic_rows'] if role in changed else []))
    if role in changed:
        parsed=ast.parse(text)
        defs={n.name:n for n in parsed.body if isinstance(n,ast.FunctionDef)}
        pin_node=defs['memory_diagnostic_pin'];row_node=defs['memory_diagnostic_rows']
        pin_text=ast.get_source_segment(text,pin_node);row_text=ast.get_source_segment(text,row_node)
        check(role+'_pin_preopen_strict_1MiB_bound',pin_text.index('not 0<=s.st_size<=bound')<pin_text.index('fd=os.open'))
        check(role+'_descriptor_read_total_maxbytes_plus_one_only',pin_text.count('stream.read(bound+1)')==1 and 'iter(' not in pin_text)
        check(role+'_descriptor_regular_singlelink_exact_identity_before_after',pin_text.count('os.fstat(fd)')==2 and 'opened_ident!=ident' in pin_text and 'finished_ident!=ident' in pin_text and 'after!=ident' in pin_text)
        check(role+'_pin_actualbytes_full_SHA_exact_stat', 'len(raw)>bound or len(raw)!=ident[4]' in pin_text and 'sha256=hashlib.sha256(raw).hexdigest()' in pin_text)
        check(role+'_parser_no_follow_total_bound_and_fullSHA',row_text.count('stream.read(contract[\'max_bytes\']+1)')==1 and 'hashlib.sha256(raw).hexdigest()!=before[\'sha256\']' in row_text and 'os.O_NOFOLLOW|os.O_NONBLOCK' in row_text)
        handlers=[n for n in ast.walk(row_node) if isinstance(n,ast.ExceptHandler)]
        check(role+'_only_explicit_validation_exception_handler',[dump(n.type) for n in handlers]==[dump(ast.parse('(ValueError, TypeError, KeyError, OverflowError)',mode='eval').body)])
        check(role+'_no_OSError_or_BaseException_or_interrupt_catch',not any(isinstance(n,ast.Name) and n.id in ('OSError','BaseException','KeyboardInterrupt','SystemExit') for n in ast.walk(row_node)))
        check(role+'_original_success_raise_preserved','        if success:raise\n' in row_text)
    proof[role]=dict(relative_path=rel,original_V1_role_pin=before[rel],current_V2_role_pin=pin(P/rel),whole_byte_inverse_verified=True,whole_AST_inverse_verified=True,definition_occurrence_count=len(new_rows),exact_finite_transforms=transforms)
unmodified={name:pin(P/name) for name in before if name not in {roles[x] for x in changed}}
check('all_other_64_V1_members_complete_bytes_preserved',all(p['sha256']==before[name]['sha256'] and p['size_bytes']==before[name]['size_bytes'] for name,p in unmodified.items()) and len(unmodified)==64)
check('canonical_full_bytes_and_AST_entirely_unchanged',pin(P/roles['canonical'])['sha256']==before[roles['canonical']]['sha256'])
check('both_binders_and_all_seven_utilities_entirely_unchanged',all(pin(P/roles[r])['sha256']==before[roles[r]]['sha256'] for r in roles if r not in changed))
for role,rel in roles.items():
    source=(P/rel).read_text()
    # This parses literal None state only and does not evaluate any candidate expression.
    original_none={n.targets[0].id:None for n in ast.parse((PARENT/rel).read_text()).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    current_none={n.targets[0].id:None for n in ast.parse(source).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    check(role+'_all_future_None_slots_unchanged',current_none==original_none)
    proof[role]['all_original_None_globals']=sorted(current_none)
source_ast_count=0
for q in sorted(P.rglob('*.py')):
    ast.parse(q.read_text());source_ast_count+=1
check('all_complete_Source_files_AST_only_parse',source_ast_count==51)
after={name:pin(PARENT/name) for name in before}
check('V1_original_67_members_and_manifest_exact_beforeafter',before==after and pin(PARENT/'MANIFEST.json')==parent_manifest_pin)
check('V1_original_all_directory_full_7ID_beforeafter',old_dirs=={str(q.relative_to(PARENT)):identity(q.lstat()) for q in [PARENT]+sorted(PARENT.rglob('*')) if q.is_dir()})
check('failed_V1_independent_review_proofs_exact_beforeafter',pin(FAILED/'REVIEW.json')==failed_pin and pin(FAILED/'MANIFEST.json')==failed_manifest_pin and pin(FAILED/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json')==failed_tool_pin)
inverse_pin=write('V2_COMPLETE_THREE_ROLE_SIX_FUNCTION_WHOLE_SOURCE_INVERSES.json',dict(schema='V25_BUILD_MEMORY_OBSERVATION_V2_FINITE_WHOLE_BYTE_AST_INVERSE_V1',source_only=True,parent_manifest_pin=parent_manifest_pin,roles=proof,unchanged_V1_member_fullpins=unmodified,exact_changed_roles=sorted(changed),exact_changed_functions=['memory_diagnostic_pin','memory_diagnostic_rows'],hunk_count=6,all_inverse_checks_typed_true=True))
lineage_pin=write('V2_ACTUAL_V1_FAILED_REVIEW_AND_ORIGINAL_SOURCE_FULLPIN_PROVENANCE.json',dict(schema='V25_MEMORY_OBSERVATION_V2_ACTUAL_V1_FAILED_SOURCE_PROVENANCE_V1',source_only=True,original_V1_complete_manifest=parent_manifest_pin,original_V1_author_report=pin(PARENT/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT.json'),original_V1_seal=pin(Path(str(PARENT)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),original_V1_postseal=pin(Path(str(PARENT)+'_seal_receipt')/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'),actual_failed_V1_review=failed_pin,actual_failed_V1_review_manifest=failed_manifest_pin,actual_failed_V1_review_terminal=failed_tool_pin,actual_failed_V1_terminal_wrapper=failed_tool,failed_V1_blockers=failed['blockers'],V1_is_failed_not_V2_admission=True,complete_V1_member_pins=before))
source_role_keys=['canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer']
report=dict(schema='AUTHOR_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_V2_FINITE_SOURCE_ONLY_REPORT_V1',status='UNREADY_SOURCE_ONLY_FINITE_V2_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW',source_only=True,check_count=len(CHECKS),checks=CHECKS,all_checks_typed_true=all(x['passed'] is True for x in CHECKS),blockers=[],qualified_role_Source_pins={r:pin(P/roles[r]) for r in source_role_keys},qualified_utility_Source_pins={r:pin(P/roles[r]) for r in roles if r not in source_role_keys},parent_V1_manifest_pin=parent_manifest_pin,actual_failed_V1_review_pin=failed_pin,complete_inverse_pin=inverse_pin,actual_fullpin_provenance=lineage_pin,exact_changed_roles=sorted(changed),exact_changed_functions=['memory_diagnostic_pin','memory_diagnostic_rows'],exact_hunk_count=6,unchanged_V1_member_count=64,original_all_14_roles=True,future_environment_witness=None,future_business_pins=None,all_candidate_API_helper_guard_resource_numeric_or_business_executed=False,project_or_ART_or_original_packages_written=False,diagnostic_RUNTIME_controls_executed=False,whole_INPUT_build_RSS_native_or_science_qualified=False,remaining_actual_limits=['Independent Source review and real new binding/install/PREP/BUILD remain required.','V1 genuine Source failure remains failure; current author checks do not turn it into PASS.','Root actual environment witness may be bound later; no future fact is silently populated.','Only format ValueError/TypeError/KeyError/OverflowError may be saved as INVALID_DIAGNOSTIC on failure; OSError and control exceptions propagate.','All original canonical finally ordering, graph reads, snapshots, helper/Q, physical commands and nine caps remain byte exact.'])
report_pin=write('AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2.json',report)
q=P/'ROOT_V2_NEXT_STEPS.txt'
q.write_text('UNREADY V2 Source only. This package replaces only complete memory_diagnostic_pin/rows functions in prepare_host, build_host and build_writer. All 14 actual Source interfaces and 64 other V1 members are preserved. V1 FAILED review remains literal provenance, never admission.\n1. Root obtains one new independent whole V2 Source review under unchanged INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json, coupling this actual MANIFEST and all current 7 role + 7 utility fullpins.\n2. Use unchanged ROOT_NEXT_STEPS.txt and environment witness contract. Root binds true existing Q c6/helper3b/proofs and its actual environment witness through complete current PREP binder into fresh TMP; independent bound review follows. Do not treat old V1 author checks, failed review or old business runs as new qualification.\n3. Root actual install/freeze/PREP then BUILD binding/install/prelaunch and one complete BUILD. Future business pins remain None here; original 1800/600/512MiB/2GiB/96GiB/8GiB/1thread/1child/0retry, all inputs and physical commands remain unchanged.\n4. Current three pin/readers stat-check ordinary single-link <=1MiB before open; no-follow nonblocking regular descriptor retains exact full7ID, bounded max_bytes+1 total read and full SHA. Failure saves validation errors only; I/O/control exceptions propagate. No candidate or resource runtime controls have been executed by the author.\n')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(CHECKS),all_checks_typed_true=report['all_checks_typed_true'],report_pin=report_pin,inverse_pin=inverse_pin,actual_V1_failed_provenance=lineage_pin,package=str(P),role_pins=report['qualified_role_Source_pins'],utility_role_count=len(report['qualified_utility_Source_pins']),candidate_or_business_executed=False),ensure_ascii=False))


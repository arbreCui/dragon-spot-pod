"""Namespace-only capture recovery Source author. No candidate/binder/runtime execution."""
from pathlib import Path
import ast,copy,hashlib,json,shutil,stat,sys
P=Path(sys.argv[1])
P3=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_V3_actual_consumer_UNREADY_Source_nl8d0t72')
F=Path('/private/tmp/axmat_V25_memory_observation_V3_INDEPENDENT_review_2FVRNl')
FS=Path(str(F)+'_seal_receipt')
REPLACEMENTS=[('v25_memory_observation','v25_memory_observation_capture'),('v25-memory-observation','v25-memory-observation-capture')]
checks=[]
def check(label,value,evidence=None):
    assert type(value) is bool
    checks.append(dict(check=label,passed=value,evidence=evidence))
    if not value:raise AssertionError(label)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes();assert identity(q.lstat())==identity(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def write(name,x):
    q=P/name;assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n');return pin(q)
def ast_dump(n):return ast.dump(n,include_attributes=False)
def definitions(text):
    return [(n.name,ast.get_source_segment(text,n),ast_dump(n)) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def inverse(text,rows):
    counts=[]
    for row in reversed(rows):
        actual=text.count(row['new'])
        if actual!=row['count']:raise ValueError('author text inverse anchor '+row['label'])
        counts.append(dict(label=row['label'],actual=actual,expected=row['count']))
        text=text.replace(row['new'],row['old'])
    return text,counts
assert P.is_dir() and P.is_relative_to(Path('/private/tmp')) and P!=P3
p3mp=pin(P3/'MANIFEST.json')
check('actual_fixed_P3_manifest_exact_SHA',p3mp['sha256']=='ef360cd59c6e3f9851eee17bd9173382f9c526de4d9fd9ec81e4fd737c814837')
m=json.loads((P3/'MANIFEST.json').read_text())
before={rel:pin(P3/rel) for rel in m['members']}
check('all_actual_P3_89_members_full_EOF_SHA_size_7ID',before==m['members'] and len(before)==89)
dirs={str(q.relative_to(P3)):identity(q.lstat()) for q in [P3]+sorted(P3.rglob('*')) if q.is_dir()}
check('all_actual_P3_directories_exact',dirs==m['directories'])
delivery=json.loads((FS/'DELIVERY_INDEX.json').read_text())
fp=pin(F/'REVIEW.json');fm=pin(F/'MANIFEST.json')
check('original_P3_independent_source_only_review_and_manifest_exact',fp['sha256']=='6e5b323ba3a2028c2963262bfe71f33651dfcc5ba2e88bc47ecb3668f2855375' and fm['sha256']=='4c430af18d9ce09168cad49e4b70b393c139eee7496f777c213ac09f1c53f2b0')
fr=json.loads((F/'REVIEW.json').read_text())
check('original_P3_independent_186_scope_is_lineage_only',fr['source_only'] is True and fr['all_checks_typed_true'] is True and fr['check_count']==186 and len(fr['checks'])==186 and fr['blockers']==[] and fr['qualified_complete_Source_manifest_pin']==p3mp)
peerterm=pin(F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json')
for label,q,chunk in [('review',peerterm,'d393d8'),('seal',pin(FS/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),'9eba3c'),('postseal',pin(FS/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'),'269334')]:
    t=json.loads(Path(q['path']).read_text());r=t['terminal_tool_return']
    check('actual_parent_Source_'+label+'_strict_CLOSED0',t['closed'] is True and t['observed_terminal'] is True and t['session_repolled_after_close'] is False and type(r['exit_code']) is int and r['exit_code']==0 and r['chunk_id']==chunk and 'session_id' not in r)
# All historical P3 members are retained once; only current roles and necessary active metadata change.
for rel in before:
    q=P/rel;assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P3/rel,q)
q=P/'CAPTURE_P3_PROVENANCE/ORIGINAL_P3_COMPLETE_MANIFEST.byte_exact.json';q.parent.mkdir();q.write_bytes((P3/'MANIFEST.json').read_bytes())
old_raw=(P3/'COMPLETE_SOURCE_INVERSES.json').read_bytes();old_proof=json.loads(old_raw);proof=copy.deepcopy(old_proof);roles=proof['role_current_paths']
check('original_14_actual_consumer_role_paths_complete',len(roles)==14 and set(roles)==set(proof['exact_finite_transforms'])==set(proof['definitions_by_role']))
role_proof={};total_namespace_hunks=0
for role,rel in roles.items():
    parent=(P3/rel).read_text();current=parent;rows=[]
    for old,new in REPLACEMENTS:
        count=current.count(old)
        check(role+'_'+old+'_new_capture_namespace_was_absent',current.count(new)==0)
        if count:
            rows.append(dict(label='capture_namespace_only_'+old,old=old,new=new,count=count))
            current=current.replace(old,new)
    (P/rel).write_text(current)
    # These are appended to the exact JSON consumed by both actual binders.
    proof['exact_finite_transforms'][role].extend(rows);total_namespace_hunks+=len(rows)
    recovered,counts=inverse(current,rows)
    check(role+'_whole_namespace_only_byte_inverse_to_actual_P3',recovered.encode()==parent.encode())
    check(role+'_whole_namespace_only_AST_inverse_to_actual_P3',ast_dump(ast.parse(recovered))==ast_dump(ast.parse(parent)))
    original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
    restored,all_counts=inverse(current,proof['exact_finite_transforms'][role])
    check(role+'_actual_consumed_complete_chain_whole_byte_inverse',restored==original)
    check(role+'_actual_consumed_complete_chain_whole_AST_inverse',ast_dump(ast.parse(restored))==ast_dump(ast.parse(original)))
    original_defs=definitions(original);current_defs=definitions(current)
    filtered=[d for d in current_defs if d[0] in {r[0] for r in original_defs}]
    check(role+'_all_original_definition_occurrences_preserved',len(filtered)==len(original_defs) and [r[0] for r in filtered]==[r[0] for r in original_defs])
    proof['definitions_by_role'][role]=dict(original_count=len(original_defs),new_count=len(current_defs),unchanged_original_definition_occurrences=[dict(name=a[0],occurrence=i,whole_bytes_and_AST_unchanged=(a==b)) for i,(a,b) in enumerate(zip(original_defs,filtered))])
    old_None={n.targets[0].id for n in ast.parse(parent).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    new_None={n.targets[0].id for n in ast.parse(current).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant) and n.value.value is None}
    check(role+'_all_original_None_future_globals_retained',new_None==old_None)
    check(role+'_only_two_allowed_namespace_tokens_changed',current==parent.replace(REPLACEMENTS[0][0],REPLACEMENTS[0][1]).replace(REPLACEMENTS[1][0],REPLACEMENTS[1][1]))
    check(role+'_all_live_namespace_uses_capture_route',all(old not in current.replace(new,'') for old,new in REPLACEMENTS))
    role_proof[role]=dict(relative_path=rel,actual_P3_role_pin=before[rel],current_capture_role_pin=pin(P/rel),namespace_finite_transforms=rows,actual_inverse_anchor_counts=all_counts,whole_byte_and_AST_inverse_to_P3_and_original_parent=True,all_future_None_globals=sorted(new_None))
(P/'COMPLETE_SOURCE_INVERSES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
active_proof=pin(P/'COMPLETE_SOURCE_INVERSES.json')
check('actual_consumed_proof_schema_and_currentpaths_unchanged',proof['schema']==old_proof['schema'] and proof['role_current_paths']==old_proof['role_current_paths'] and proof['original_parent_fullpins']==old_proof['original_parent_fullpins'])
restored_proof=copy.deepcopy(proof)
for role,row in role_proof.items():
    if row['namespace_finite_transforms']:
        restored_proof['exact_finite_transforms'][role]=restored_proof['exact_finite_transforms'][role][:-len(row['namespace_finite_transforms'])]
restored_proof['definitions_by_role']=old_proof['definitions_by_role']
check('whole_actual_proof_JSON_inverse_to_P3_bytes',(json.dumps(restored_proof,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()==old_raw)
contract_rel='utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json'
old_contract_raw=(P3/contract_rel).read_bytes();old_contract=json.loads(old_contract_raw);contract=copy.deepcopy(old_contract)
for key,value in contract['namespaces'].items():
    for old,new in REPLACEMENTS:value=value.replace(old,new)
    contract['namespaces'][key]=value
(P/contract_rel).write_text(json.dumps(contract,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
check('fixed_utility_contract_only_namespace_map_changed',all(contract[k]==old_contract[k] for k in contract if k!='namespaces'))
restore_contract=copy.deepcopy(contract);restore_contract['namespaces']=old_contract['namespaces']
check('whole_fixed_contract_JSON_byte_inverse_to_P3',(json.dumps(restore_contract,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()==old_contract_raw)
check('all_old_463_Source_owners_and_Q_original_context_retained',contract['complete_old_frozen_Source_owners']==old_contract['complete_old_frozen_Source_owners'] and contract['original_host_prefix_seven_input_pins']==old_contract['original_host_prefix_seven_input_pins'])
consumers={}
for binder in ('prepare_binder','build_binder'):
    text=(P/roles[binder]).read_text();defs={n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)};main=ast.get_source_segment(text,defs['main'])
    check(binder+'_actual_main_consumes_updated_fixed_inverse_file',main.count("proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json')")==1)
    check(binder+'_actual_source_verify_keeps_exact_originalParent_contract',"source_inverse(source_inverse(text,ready_rows),proof['exact_finite_transforms'][role])" in ast.get_source_segment(text,defs['source_verify_original_inverse']))
    template_roles=('canonical','prepare_host','prepare_writer') if binder=='prepare_binder' else ('build_host','build_writer')
    for role in template_roles:
        restored,counts=inverse((P/roles[role]).read_text(),proof['exact_finite_transforms'][role])
        original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
        check(binder+'_'+role+'_actual_template_whole_byte_AST_inverse',restored==original and ast_dump(ast.parse(restored))==ast_dump(ast.parse(original)))
    consumers[binder]=dict(actual_current_binder_pin=pin(P/roles[binder]),actual_consumed_proof_pin=active_proof,template_roles=list(template_roles),actual_READY_binding_or_candidate_execution=False)
prepare_binder=(P/roles['prepare_binder']).read_text()
check('actual_PREP_binder_output_canonical_capture_basename',"'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py'" in prepare_binder)
check('actual_BUILD_binder_fixed_installed_canonical_capture_route','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py' in (P/roles['build_binder']).read_text())
canonical=(P/roles['canonical']).read_text();canonical_parent=(P3/roles['canonical']).read_text()
check('original_empty_stderr_PREP_admission_gate_retained',"if terminal_file(e['full_stderr']['path'],e['full_stderr']['sha256']).stat().st_size!=0:" in canonical and canonical.replace(REPLACEMENTS[0][1],REPLACEMENTS[0][0]).replace(REPLACEMENTS[1][1],REPLACEMENTS[1][0])==canonical_parent)
writer=(P/roles['prepare_writer']).read_text()
check('original_real_separate_parent_stderr_contract_not_relaxed',"(E/'parent_stderr.log').stat().st_size!=0" in writer and "separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False" in writer)
modified={roles[role] for role,row in role_proof.items() if row['namespace_finite_transforms']}|{'COMPLETE_SOURCE_INVERSES.json',contract_rel}
retained={rel:pin(P/rel) for rel in before if rel not in modified}
check('all_other_P3_history_members_literal_bytes_retained',all(q['sha256']==before[rel]['sha256'] and q['size_bytes']==before[rel]['size_bytes'] for rel,q in retained.items()))
ast_count=0
for q in P.rglob('*.py'):ast.parse(q.read_text());ast_count+=1
check('all_current_56_full_Source_AST_only_parsed',ast_count==56)
check('original_P3_complete_source_manifest_members_dirs_unchanged',pin(P3/'MANIFEST.json')==p3mp and before=={rel:pin(P3/rel) for rel in before} and dirs=={str(q.relative_to(P3)):identity(q.lstat()) for q in [P3]+sorted(P3.rglob('*')) if q.is_dir()})
check('original_P3_independent_review_proof_unchanged',pin(F/'REVIEW.json')==fp and pin(F/'MANIFEST.json')==fm and pin(F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json')==peerterm)
lineage=write('CAPTURE_ACTUAL_P3_PARENT_SOURCE_AND_PEER_FULLPIN_PROVENANCE.json',dict(schema='V25_MEMORY_OBSERVATION_CAPTURE_PARENT_PROVENANCE_SOURCE_ONLY_V1',source_only=True,P3_manifest=p3mp,P3_independent_source_review=fp,P3_independent_source_review_manifest=fm,P3_true_review_terminal=peerterm,P3_true_seal=pin(FS/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),P3_true_postseal=pin(FS/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'),P3_delivery_index=pin(FS/'DELIVERY_INDEX.json'),P3_qualification_is_lineage_not_capture_admission=True,all_original_P3_member_fullpins=before,all_original_P3_directory_identities=dirs,new_actual_CAPTURE_env_business_peers_and_results=None))
inverse_pin=write('CAPTURE_NAMESPACE_COMPLETE_14_ROLE_BYTE_AST_AND_JSON_INVERSES.json',dict(schema='V25_MEMORY_OBSERVATION_CAPTURE_NAMESPACE_ONLY_WHOLE_INVERSE_V1',source_only=True,exact_namespace_pairs=REPLACEMENTS,exact_namespace_hunk_count=total_namespace_hunks,roles=role_proof,actual_consumer_proof_pin=active_proof,actual_consumer_proof_parent_pin=before['COMPLETE_SOURCE_INVERSES.json'],original_P3_definition_metadata=old_proof['definitions_by_role'],current_capture_definition_metadata=proof['definitions_by_role'],updated_fixed_contract_pin=pin(P/contract_rel),original_fixed_contract_pin=before[contract_rel],original_contract_namespace_map=old_contract['namespaces'],current_capture_namespace_map=contract['namespaces'],whole_Source_and_JSON_inverses_verified=True,all_unmodified_P3_members=retained,all_actual_binder_consumer_static_results=consumers))
source_roles=['canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer']
report=dict(schema='AUTHOR_V25_MEMORY_OBSERVATION_CAPTURE_NAMESPACE_ONLY_SOURCE_REPORT_V1',status='UNREADY_NAMESPACE_ONLY_SOURCE_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW_AND_ROOT_BINDING',source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=all(c['passed'] is True for c in checks),blockers=[],qualified_role_Source_pins={r:pin(P/roles[r]) for r in source_roles},qualified_utility_Source_pins={r:pin(P/roles[r]) for r in roles if r not in source_roles},actual_consumed_complete_inverse_pin=active_proof,complete_namespace_inverse_pin=inverse_pin,actual_parent_provenance_pin=lineage,exact_namespace_pairs=REPLACEMENTS,exact_namespace_hunk_count=total_namespace_hunks,actual_capture_namespaces=contract['namespaces'],unmodified_P3_member_count=len(retained),all_original_history_kept=True,old_P3_qualification_is_lineage_only=True,all_actual_future_environment_business_or_Source_qualification_pins=None,Root_real_external_stdout_and_stderr_capture_required=True,original_empty_external_stderr_gate_not_relaxed=True,candidate_BINDER_API_guard_resource_helper_material_numeric_or_business_executed=False,project_ART_old_Source_frozenD_or_old_results_written=False,whole_INPUT_BUILD_RSS_native_or_science_qualified=False)
rp=write('AUTHOR_CAPTURE_NAMESPACE_ONLY_SOURCE_REPORT.json',report)
(P/'ROOT_CAPTURE_NEXT_STEPS.txt').write_text("""UNREADY capture namespace-only Source. No binder, candidate, guard, resource API or business execution here.
1. Obtain a new independent Source review coupled to this MANIFEST and current seven role + seven utility fullpins. P3 Source qualification and old real PREP are lineage only.
2. Root runs the same PREP Source binder with actual Q path/c6 SHA/fresh TMP; unchanged mandatory flags:
 --actual-new-Q-writer-terminal PATH --actual-new-Q-writer-terminal-sha256 SHA
 --actual-Q-saved-peer PATH --actual-Q-saved-peer-sha256 SHA
 --actual-Q-saved-peer-retention PATH --actual-Q-saved-peer-retention-sha256 SHA
 --actual-diagnostic-resource-environment-witness PATH --actual-diagnostic-resource-environment-witness-sha256 SHA
All true proof values come from Root; this Source fills no future business/environment result. New canonical basename:
 prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py
3. Root uses unchanged complete utilities with new actual manifest/peer/bound pins to install/freeze/prelaunch in capture namespaces. The utility fixed namespace map is in current report. Original B/history/date20261010, Q/helper, physics, empty-stderr gate, caps and MRO remain unchanged.
4. Before the one new genuine PREP launch, use two actual external shell redirections, not combined tool output and never invented empty files:
 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B NEW_CAPTURE_PREP_D/combined_prepare_host.py > NEW_CAPTURE_PREP_E/parent_stdout.log 2> NEW_CAPTURE_PREP_E/parent_stderr.log
Root must set NEW_CAPTURE_PREP_D/E to the fixed actual capture paths, confirm neither stream file already exists, and preserve the real terminal separately. Native executor child capture remains original merged stdout/stderr; these redirections only supply genuine separate external Root host streams. Do not claim separate child stderr.
5. On genuine closed exit0, retain real terminal and both full streams, use the original writer and full namespace/saved-result review. Never synthesize missing stderr or re-run old namespaces. Then actual new PREP proof feeds unchanged BUILD binder and current BUILD interfaces; Root BUILD also captures actual external streams separately. No old PREP success is a new capture declaration/terminal/result pin.
6. Nine original caps and all complete inputs/5stages/two graph reads/trace/physical commands remain. No RSS improvement or scientific qualification is predicted.
""")
print(json.dumps(dict(source_only=True,check_count=len(checks),all_checks_typed_true=True,current_author_report_pin=rp,current_actual_consumed_complete_inverse_pin=active_proof,current_complete_namespace_inverse_pin=inverse_pin,all_current_role_count=14,namespace_hunks=total_namespace_hunks,candidate_or_business_executed=False),ensure_ascii=False))

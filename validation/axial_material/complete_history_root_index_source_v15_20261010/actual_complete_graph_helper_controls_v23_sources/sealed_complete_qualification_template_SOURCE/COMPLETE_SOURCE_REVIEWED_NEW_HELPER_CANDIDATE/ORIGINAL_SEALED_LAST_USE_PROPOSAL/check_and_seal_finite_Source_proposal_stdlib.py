from pathlib import Path
import ast,hashlib,json,os,stat
P=Path('/private/tmp/axmat_v22_failedbuild_inactive_audit_SOURCE_lastuse_7ecicdjv')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with p.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==identity(s);b=f.read();assert len(b)==s.st_size and f.read(1)==b'';assert identity(os.fstat(f.fileno()))==identity(s)
    assert identity(p.lstat())==identity(s)
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
e=json.loads((P/'FULL_SOURCE_EVIDENCE.json').read_bytes());r=json.loads((P/'SINGLE_FINITE_SOURCE_PROPOSAL.json').read_bytes());checks=[]
def check(k,v):assert type(v)is bool and v;checks.append(dict(check=k,passed=v))
for row in e['original_source_copies']:
    p=Path(row['path']);copy=Path(row['copy_path']);check('exact full Source pin '+str(p),pin(p)=={k:row[k]for k in('path','sha256','size_bytes','identity')})
    check('whole Source byte copy '+str(p),p.read_bytes()==copy.read_bytes());check('whole Source AST copy '+str(p),ast.dump(ast.parse(p.read_bytes()),include_attributes=False)==ast.dump(ast.parse(copy.read_bytes()),include_attributes=False))
    check('complete definitions '+str(p),len([n for n in ast.parse(copy.read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))])==row['complete_definition_count'])
canonical=(P/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py').read_text();helper=(P/'combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py').read_text()
for k,a in [('audit full copied records','record = dict(value)'),('audit complete source map','for value in self._records.values():'),('whole original records clone','"records": _json_clone(records)'),('original unique count','"unique_records": len(self._records)'),('original total attempts','sum(value["attempt_count"] for value in self._records.values())'),('audit stored full JSON keys','key = _canonical_json(value)')]:check(k,a in helper)
for k,a in [('full fresh audit','with g.ReadOpenAudit()as audit:'),('wholeverify no newfake','verified=g.verify_graph('),('full original snapshot','trace=audit.snapshot();'),('full trace digest','trace_digest=g._content_digest(trace);'),('only later audit deletion','del trace,audit,regular,graph_reads'),('whole second freshgraph','graph=g.strict_json(d[\'input_graph\'][\'path\'],d[\'input_graph\'][\'sha256\'])'),('whole original all4 phase loops',"zip(stage_labels()[:4],commands[:4])")]:check(k,a in canonical)
check('future sixNone and newQ unknown',r['future_business_pins']==[None]*6 and r['required_future_qualification']['new_joint_helper_Q']is None)
check('no predictedPASS and no actualpeakline',r['RSS_cause_or_next_PASS_prediction']is None and r['actual_limit_trigger_line_observed']is False)
check('private countcall timing explicitly disclosed',bool(r['single_proposed_change']['original_call_order_not_falsely_claimed']))
out=dict(schema='FINITE_INACTIVE_AUDIT_LAST_USE_SOURCE_ONLY_SELF_REVIEW_V1',source_only=True,all_checks_passed=True,checks=checks,check_count=len(checks),source_parent_pins=e['original_source_copies'],only_proposal_no_generated_runtime_candidate=True,no_reviewed_code_or_API_guard_business_payload_execution=True)
(P/'SOURCE_SELF_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');m=P/'MANIFEST.json';assert not m.exists();m.write_text('{}\n');members=[dict(relative_path=q.relative_to(P).as_posix(),**pin(q))for q in sorted(P.iterdir())if q.is_file()and q!=m];di=identity(P.lstat());manifest=dict(schema='FINITE_COMPLETE_BUILD_INACTIVE_AUDIT_SOURCE_PROPOSAL_SEAL_V1',source_only=True,status='SOURCE_PROPOSAL_ONLY_NO_CANDIDATE_OR_QUALIFICATION',members=members,member_count=len(members),directory_identity=di)
m.write_text(json.dumps(manifest,indent=2)+'\n');assert identity(P.lstat())==di
for v in members:assert pin(Path(v['path']))=={k:v[k]for k in('path','sha256','size_bytes','identity')}
print(json.dumps(dict(source_only=True,check_count=len(checks),manifest=pin(m),proposal=pin(P/'SINGLE_FINITE_SOURCE_PROPOSAL.json'),no_reviewed_code_or_business_execution=True),indent=2))

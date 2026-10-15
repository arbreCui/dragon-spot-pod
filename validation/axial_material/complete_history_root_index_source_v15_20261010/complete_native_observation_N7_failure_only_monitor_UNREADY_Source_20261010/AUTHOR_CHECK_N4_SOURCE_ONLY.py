"""Author's static Source/AST/whole-byte audit only; never execute a candidate."""
from pathlib import Path
import ast
import hashlib
import json
import stat
import tarfile

N=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_role_limited_OS_tools_N4_UNREADY_Source_3gnnt2it')
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
FILES=['Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','complete_observation_BUILD5_AB_runtime.UNREADY.py','complete_observation_genuine_host.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']
TOOLS={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
checks=[]

def check(name,value):
    assert type(value)is bool and value,name
    assert name not in {c['check']for c in checks}
    checks.append(dict(check=name,passed=value))

def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1
    with p.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    b=p.lstat();assert [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]==[b.st_dev,b.st_ino,b.st_mode,b.st_nlink,b.st_size,b.st_mtime_ns,b.st_ctime_ns]
    return dict(path=str(p),sha256=sha,size_bytes=b.st_size,identity=[b.st_dev,b.st_ino,b.st_mode,b.st_nlink,b.st_size,b.st_mtime_ns,b.st_ctime_ns])

def info(raw):
    lines=raw.decode().splitlines(keepends=True);t=ast.parse(raw)
    return t,{n.name:(ast.dump(n,include_attributes=False),''.join(lines[n.lineno-1:n.end_lineno]))for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def globals_AST(tree):
    return [ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.Assign,ast.AnnAssign))and not (isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='CANONICAL_OS_TOOL_PATHS')]

def literal_role_map(tree):
    return next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='CANONICAL_OS_TOOL_PATHS')

def main():
    ledger=json.loads((N/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json').read_bytes());before=ledger['N3_original_fullfile_pins'];changed={}
    check('original N3 manifest exact family SHA',pin(P/'MANIFEST.json')['sha256']=='5313b65cc109d93816137f8c53e6cdcfbf6d5044310762ac65a20a2f76330593')
    check('complete original81 Source fullpins unchanged',before=={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()})
    check('original N3 manifest retained as full original bytes',(N/'PREVIOUS_SEALED_N3_SOURCE_PROVENANCE/MANIFEST.json').read_bytes()==(P/'MANIFEST.json').read_bytes())
    check('all75 original nonchanged members remain whole bytes',all((N/rel).read_bytes()==(P/rel).read_bytes()for rel in before if rel not in {*FILES,'MANIFEST.json'}))
    helper_dumps=[];unchanged_defs=0;hunks_count=0
    allowed={FILES[0]:{'pin','main'},FILES[1]:{'pin','shape','main'},FILES[2]:{'fullpin','pinshape','recheck','validate_request','run'},FILES[3]:{'typed_full_pin','recheck_full_pin'},FILES[4]:{'fullpin','check','main'}}
    for name in FILES:
        raw=(N/name).read_bytes();parent=(P/name).read_bytes();ot,od=info(parent);nt,nd=info(raw);hunks=ledger['five_role_complete_inverse_hunks'][name];restored=raw.decode().splitlines(keepends=True)
        for h in reversed(hunks):
            assert ''.join(restored[h['derived_start0']:h['derived_stop0']])==h['derived']
            restored[h['derived_start0']:h['derived_stop0']]=h['original'].splitlines(keepends=True)
        recovered=''.join(restored).encode();check(name+' fullbyte/AST inverse to original N3',recovered==parent and ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ot,include_attributes=False));hunks_count+=len(hunks)
        check(name+' whole original defs remain, only specified defs changed',set(od)<=set(nd)and {k for k in od if od[k]!=nd[k]}==allowed[name]and set(nd)-set(od)=={'source_tool_nlink_allowed'})
        check(name+' all other defs fullbytes and AST exact',all(od[k]==nd[k]for k in od if k not in allowed[name]));unchanged_defs+=len(od)-len(allowed[name])
        check(name+' all original global AST including physics/caps/unknown unchanged',globals_AST(ot)==globals_AST(nt))
        check(name+' exact same six canonical OS tool roles',literal_role_map(nt)==TOOLS)
        helper=next(n for n in nt.body if isinstance(n,ast.FunctionDef)and n.name=='source_tool_nlink_allowed');helper_dumps.append(ast.dump(helper,include_attributes=False))
        check(name+' explicit optionalNone tool role only and typed positive nlink Source',ast.literal_eval(helper.args.defaults[-1])is None and "if tool_role is None:return type(nlink)is int and nlink==1"in nd[helper.name][1]and "type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS"in nd[helper.name][1]and "str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1"in nd[helper.name][1])
        check(name+' all prior nlink-checked routines default singlelink',all(ast.literal_eval(n.args.defaults[-1])is None for n in nt.body if isinstance(n,ast.FunctionDef)and n.name in allowed[name]-{'main','validate_request','run'}))
        changed[name]=pin(N/name)
    check('same nlink predicate AST in all5roles',len(set(helper_dumps))==1)
    check('finite whole5role29hunks',hunks_count==29)
    runtime=(N/FILES[2]).read_text();binder=(N/FILES[1]).read_text();preparer=(N/FILES[0]).read_text();post=(N/FILES[4]).read_text();host=(N/FILES[3]).read_text()
    check('request exact six original CLIpaths; only tools explicit roles',"all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items())"in preparer and "pin(getattr(a,k),deadline,tool_role=k)"in preparer and "actual=pin(value['path'],deadline)"in preparer)
    check('binder original129 defaults; only dedicated extra tool role mapping',"for p in rows:shape(p)"in binder and "for p in extra:shape(p,tool_role=tool_roles_by_path.get(p['path']))"in binder and "for role,p in b['tool_pins'].items():shape(p,tool_role=role)"in binder)
    check('runtime original129/seed/author defaults; explicit actual tool roles',"for p in rows:pinshape(p)"in runtime and "for p in extra:pinshape(p,tool_role=tool_roles_by_path.get(p['path']))"in runtime and "pinshape(row['input_pin']);require(allpins"in runtime and "for p in expected.values():recheck(p)"in runtime)
    check('runtime complete inputs before/after/failure actual tool roles',all(s in runtime for s in ["for p in inputs:recheck(p,tool_role=tool_roles_by_path.get(p['path']))","for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))","try:after_inputs.append(recheck(p,tool_role=tool_roles_by_path.get(p['path'])))"]))
    check('host typed check passes declared role, original support wholeEOF remains',"typed_full_pin(expected,tool_role=tool_role)"in host and "actual=support.pin(expected['path'],expected['sha256'])"in host)
    check('postclose complete tool/fullinput roles; rest defaults',"for role,p in b['tool_pins'].items():check(p,tool_role=role)"in post and "for p in h['complete_input_pins_before_and_after']:check(p,tool_role=tool_roles_by_path.get(p['path']))"in post and "fullpin(p['path'],tool_role=tool_role)==p"in post)
    oi=json.loads((N/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());members={row['relative_path']:row for row in oi['members']};count=0
    with tarfile.open(N/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as t:
        for row in t:
            assert row.isfile()and row.name in members
            stream=t.extractfile(row);sha=hashlib.sha256();size=0
            while True:
                b=stream.read(2**20)
                if not b:break
                sha.update(b);size+=len(b)
            stream.close();wanted=members[row.name]['full_original_Source_pin'];assert row.size==size==wanted['size_bytes']and sha.hexdigest()==wanted['sha256'];count+=1
    check('whole1365 native compile Source archive retained fullEOF CRC/index SHA',count==1365==len(members))
    evidence=N/'ACTUAL_PRIOR_N3_SOURCE_META_FAILURE_EVIDENCE';ad=json.loads((evidence/'Root_actual_observation_Source_admission_tool_terminal_return.json').read_bytes());fail=json.loads((evidence/'Root_actual_observation_request_META_alias_failure_tool_terminal_return.json').read_bytes())
    check('real prior988463 Source admission0 remains N3only',ad['closed']is True and ad['observed_terminal']is True and ad['actual_terminal_chunk']=='988463'and type(ad['terminal_tool_return']['exit_code'])is int and ad['terminal_tool_return']['exit_code']==0 and 'session_id'not in ad['terminal_tool_return'])
    check('real request88c74a1 preserved no build/material execution',fail['closed']is True and fail['observed_terminal']is True and fail['actual_terminal_chunk']=='88c74a'and type(fail['terminal_tool_return']['exit_code'])is int and fail['terminal_tool_return']['exit_code']==1 and fail['actual_build_or_material_execution']is False and 'actual Root full regular singlelink pin'in fail['terminal_tool_return']['output'])
    for row in ledger['actual_prior_N3_Source_META_evidence']:
        check('prior actual Source META fullbytes '+Path(row['original_pin']['path']).name,Path(row['original_pin']['path']).read_bytes()==Path(row['copied_pin']['path']).read_bytes()and pin(Path(row['original_pin']['path']))==row['original_pin'])
    stat_receipt=evidence/'Root_actual_canonical_tool_full_EOF_identity_observation_tool_return.json'
    check('actual Root782641 wholeEOF tool identity observation present; no fabricated9261c9',stat_receipt.is_file())
    sr=json.loads(stat_receipt.read_bytes());st=sr['terminal_tool_return'];check('actual Root782641 read-only typed0closed preserved',sr['schema']=='ROOT_ACTUAL_CANONICAL_TOOL_FULL_EOF_IDENTITY_TOOL_RETURN_V1'and sr['source_only']is True and sr['closed']is True and sr['observed']is True and sr['session_repolled_after_close']is False and sr['compiler_or_business_executed']is False and st['chunk_id']=='782641'and type(st['exit_code'])is int and st['exit_code']==0 and 'session_id'not in st)
    actual_tools=json.loads(st['output']);rows=actual_tools['tools'];check('actual six original paths and real nlinks2/78/78/78/1/1 preserved',actual_tools['source_only']is True and actual_tools['compiler_or_business_executed']is False and [r['tool_role']for r in rows]==list(TOOLS)and all(r['requested']==r['resolved']==r['fullpin']['path']==TOOLS[r['tool_role']]and r['regular']is True and r['symlink_ancestors']==[]and len(r['fullpin']['identity'])==7 and all(type(v)is int for v in r['fullpin']['identity'])for r in rows)and [r['fullpin']['identity'][3]for r in rows]==[2,78,78,78,1,1])
    check('original Source wholefullpins remain unchanged after audit',before=={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()})
    (N/'AUTHOR_CHECK_N4_SOURCE_ONLY.py').write_bytes(Path(__file__).read_bytes())
    report=dict(schema='AUTHOR_COMPLETE_N4_ROLE_LIMITED_OS_TOOL_NLINK_SOURCE_REVIEW_V1',status='UNREADY_AUTHOR_SOURCE_CHECKS_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,check_count=len(checks),all_checks_typed_true=True,checks=checks,blockers=[],canonical_OS_tool_paths=TOOLS,five_changed_Source_pins=changed,finite_hunk_count=hunks_count,unchanged_original_topdef_count=unchanged_defs,original_compile_Source_archive_members=count,original_N3_manifest_pin=pin(P/'MANIFEST.json'),full_inverse_pin=pin(N/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json'),actual_Root_N4_Source_admission=None,actual_independent_N4_Source_review=None,actual_Root_N4_runtime_terminal=None,actual_build_or_material_execution=False,scientific_qualification_created=False)
    out=N/'AUTHOR_N4_SOURCE_ONLY_REPORT.json';out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=report['status'],source_only=True,report_pin=pin(out),check_count=len(checks),five_Source_pins=changed,original_compile_Source_archive_members=count,candidate_guard_API_compile_native_or_material_executed=False),allow_nan=False))

if __name__=='__main__':main()

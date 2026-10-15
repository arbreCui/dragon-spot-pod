"""Pure text/AST draft generation. No helper loading or fixture creation."""
from pathlib import Path
import ast,hashlib,json,stat
D=Path('/private/tmp/axmat_v14b_manual_alias_helper_controls_source_only_20261010')
P=Path('/private/tmp/axmat_v14_complete_environment_streaming_helper_controls_source_only_20261010/helper_only_controls.UNREADY.py')
H=Path('/private/tmp/axmat_v14b_manual_file_alias_streaming_sha_helper_source_draft_20261010/complete_environment_streaming_sha_helper_v14b.py')
O=D/'helper_only_controls_v14b.UNREADY.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(p):
 x=p.lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
before={str(p):ident(p) for p in (P,H)}
assert sha(P)=='4d630833ea330264f48aecf37b45183296716d906c6a74a15a113295b83513f9'
assert sha(H)=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
original=P.read_text();text=original;regions=[]
def edit(name,old,new,count=1):
 global text
 assert text.count(old)==count and old!=new
 text=text.replace(old,new,count);regions.append({'name':name,'old':old,'new':new,'count':count})
edit('source_only_documentation','SOURCE-ONLY. Root must bind reviewed canonical helper SHA before execution.','SOURCE-ONLY V14b. Root must bind reviewed canonical helper SHA before execution.')
edit('additional_stdlib_errno_import','import argparse\nimport hashlib','import argparse\nimport errno\nimport hashlib')
edit('new_canonical_helper_path',"HELPER=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14.py')", "HELPER=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14b.py')")
edit('new_exclusive_namespace_prefix',"OUT_PREFIX='axial-material-complete-environment-streaming-sha-helper-only-controls-v14-'", "OUT_PREFIX='axial-material-complete-environment-streaming-sha-helper-only-controls-v14b-'")
alias_old="""        assert len(probe.events)==4
        return {'oracle_sha256':want,'literal_paths':[str(x) for x in [p,first,second,spelling]],'separate_full_reads':4,'dotdot_OS_semantics_retained':True}"""
alias_new="""        assert len(probe.events)==4
        # Original four literal streams remain complete and distinct.
        extra=[]
        third=folder/'three.link';third.symlink_to(second.name)
        assert sha(third)==want
        with module.complete_environment_digest_context({}):
            actual=module.digest(third);assert actual==want
            snapshot=module._ENV_STREAM_ACTIVE_CONTEXT['memo'][str(third)]['snapshot']
            assert [item[0] for item in snapshot['alias_hops']]==[str(third),str(second),str(first)]
            hops=snapshot['alias_hops']
        context_cleared(module)
        assert probe.events[-1]['bytecount']==1225 and probe.events[-1]['EOF_observed']
        extra.append({'case':'legal_three_link_chain','literal':str(third),
            'independent_full_SHA_oracle':sha(third),'actual_SHA':actual,'alias_hops':hops})
        repeated=directory/'..'/'..'/'dir.link'/'..'/'input.bin'
        assert sha(repeated)==want
        with module.complete_environment_digest_context({}):
            actual=module.digest(repeated);assert actual==want
            snapshot=module._ENV_STREAM_ACTIVE_CONTEXT['memo'][str(repeated)]['snapshot']
            assert [item[0] for item in snapshot['alias_hops']]==[str(directory),str(directory)]
            hops=snapshot['alias_hops']
        context_cleared(module)
        assert probe.events[-1]['bytecount']==1225 and probe.events[-1]['EOF_observed']
        extra.append({'case':'legal_completed_directory_link_repeat_after_dotdot','literal':str(repeated),
            'independent_full_SHA_oracle':sha(repeated),'actual_SHA':actual,'alias_hops':hops,
            'completed_link_revisited_twice':True})
        selflink=folder/'self_cycle.link';selflink.symlink_to(selflink.name)
        a=folder/'mutual_a.link';b=folder/'mutual_b.link';a.symlink_to(b.name);b.symlink_to(a.name)
        growing=folder/'growing_cycle.link';growing.symlink_to(growing.name+'/padding')
        def independent_OS_cycle(path):
            try:sha(path)
            except OSError as error:
                assert error.errno==errno.ELOOP,(type(error).__name__,error.errno,str(error))
                return {'type':type(error).__name__,'errno':error.errno,'message':str(error)}
            raise AssertionError('independent genuine OS full-open cycle unexpectedly accepted')
        for name,path in [('self_cycle',selflink),('mutual_cycle',a),('growing_cycle',growing)]:
            original_open_rejection=independent_OS_cycle(path)
            count_before=len(probe.events)
            def attempt():
                with module.complete_environment_digest_context({}):module.digest(path)
            rejection=reject(attempt,'cyclic active literal alias expansion')
            context_cleared(module)
            assert len(probe.events)==count_before
            extra.append({'case':name,'literal':str(path),'independent_original_OS_full_open_rejection':original_open_rejection,
                'new_manual_walk_rejection':rejection,'no_partial_file_stream_or_SHA_accepted':True,
                'context_buffer_memo_lock_reset':True})
        assert len(probe.events)==6
        return {'oracle_sha256':want,'literal_paths':[str(x) for x in [p,first,second,spelling]],
            'separate_full_reads':4,'dotdot_OS_semantics_retained':True,'additional_v14b_alias_cases':extra,
            'actual_total_complete_alias_streams':6,'original_four_literal_checks_preserved':True}"""
edit('only_alias_group_five_new_subcases',alias_old,alias_new)
tree=ast.parse(text)
inverse=text
for e in reversed(regions):
 assert inverse.count(e['new'])==e['count'];inverse=inverse.replace(e['new'],e['old'],e['count'])
assert inverse==original
def scopes(t):
 d={}
 def visit(n,parents):
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
   key=parents+(n.name,);d[key]=ast.get_source_segment(t,n);parents=key
  for c in ast.iter_child_nodes(n):visit(c,parents)
 visit(ast.parse(t),());return d
oldscope=scopes(original);newscope=scopes(text)
changed=[list(k) for k,v in oldscope.items() if newscope[k]!=v]
assert changed==[['fixture_controls'],['fixture_controls','aliases']]
assert set(newscope)-set(oldscope)=={('fixture_controls','aliases','independent_OS_cycle'),('fixture_controls','aliases','attempt')}
for name in ('historical_environment_comparison','load_canonical','main','NewHelperOpenProbe','RealFDProbe','context_cleared','sha'):
 assert newscope[(name,)]==oldscope[(name,)]
run_calls=[n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='run' and n.args and isinstance(n.args[0],ast.Constant)]
assert len(run_calls)==18
values={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
assert ast.literal_eval(values['HELPER_SHA256']) is None
assert ast.literal_eval(values['STATUS']).startswith('UNREADY')
assert ast.literal_eval(values['MAX_ARCHIVE_BYTES'].left)==64
assert all(ident(p)==before[str(p)] for p in (P,H))
with O.open('x') as f:f.write(text)
proof={'schema':'AXMAT_V14B_HELPER_ONLY_CONTROL_DRIVER_COMPLETE_SOURCE_INVERSE_V1','status':'UNREADY_SOURCE_ONLY','parent':{'path':str(P),'sha256':sha(P)},'candidate':{'path':str(O),'sha256':sha(O)},'regions':regions,'complete_inverse':True,'original_all_definitions':len(oldscope),'candidate_all_definitions':len(newscope),'changed_original_definition_scopes':changed,'all_other_original_definitions_byteexact':True,'canonical_helper_final_sha256':None,'control_root':None,'host_root':None,'actual_control_exit':None}
(D/'COMPLETE_SOURCE_INVERSE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
contract={'schema':'AXMAT_V14B_HELPER_ONLY_CONTROL_SOURCE_CONTRACT_V1','groups':21,'original_literal_group_names':run_calls,'original_mutation_group_names':['during_stream_truncate','during_stream_replace','during_stream_rewrite'],'only_modified_group':'allowed_relative_links_multihop_and_symlink_dotdot','original_four_alias_cases_kept':True,'additional_alias_subcases':['legal_three_link_chain','legal_completed_directory_link_repeat_after_dotdot','self_cycle','mutual_cycle','growing_cycle'],'complete_valid_stream_count_in_alias_group':6,'cycles_have_zero_new_file_streams':True,'oracle':'independent original stdlib file_digest on real OS-opened file; cycle errno.ELOOP from original OS open','canonical_helper':'/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14b.py','canonical_helper_sha256':None,'new_out_prefix':'axial-material-complete-environment-streaming-sha-helper-only-controls-v14b-','original_Darwin_helper_ROOT_binding_must_remain_canonical':True,'optional_history_environment_body_byteexact':True,'whole_wall_seconds':120,'own_child_rss_mib':512,'archive_bytes':64*2**20,'children':1,'threads':1,'retries':0,'full_history_GiB':96,'free_floor_GiB':8,'new_genuine_host_and_Root_actual_receipt_still_required':True,'actual_result':None,'fixture_executed':False,'performance_executed':False,'component_or_native_AAA_ABA_credit':False}
(D/'CONTROL_CONTRACT.json').write_text(json.dumps(contract,indent=2)+'\n')
report={'schema':'AXMAT_V14B_HELPER_ONLY_CONTROL_DRIVER_SOURCE_DRAFT_REVIEW_V1','status':'UNREADY_SOURCE_ONLY','driver_sha256':sha(O),'original_driver_sha256':sha(P),'complete_inverse_regions':len(regions),'original_all_definition_count':len(oldscope),'candidate_all_definition_count':len(newscope),'changed_original_scopes':changed,'original21groups_kept':True,'alias_group_new_subcases':5,'all_other_original_support_and_optional_history_exact':True,'helper_final_SHA_None':True,'actual_controls_and_performance_None':True,'source_identity_before_after':before,'source_helper_future_candidate_sha256':sha(H),'business_imports_or_calls':False,'fixture_creation_or_execution':False,'project_written':False,'full86_native_AAA_ABA_qualification':False,'proof_sha256':sha(D/'COMPLETE_SOURCE_INVERSE_PROOF.json'),'contract_sha256':sha(D/'CONTROL_CONTRACT.json')}
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('H14b helper-only控制草稿已生成，UNREADY，未运行。原21组完整保留，仅aliases组新增合法3link、同dirlink target结束后dotdot再访、self/mutual/growing循环；合法路径独立标准库完整SHA，循环独立原OS ELOOP，拒绝后无partialstream及context清理。\n新canonical v14b、helperSHA None、新v14b OUT前缀；历史old619/DECL/完整environment动作逐字保留，原120/512/64MiB/单子进程/零重试及96/free8不改。不授原86数学控制/提速/native/AAA/ABA。\n')
print(json.dumps({'status':report['status'],'driver':str(O),'driver_sha256':sha(O),'REPORT_sha256':sha(D/'REPORT.json'),'source_inverse_sha256':report['proof_sha256'],'contract_sha256':report['contract_sha256'],'original_definitions':len(oldscope),'candidate_definitions':len(newscope)},indent=2))

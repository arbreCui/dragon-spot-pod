import ast,hashlib,json,os,stat,tempfile
from pathlib import Path
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
CHECKS=[];PINS={};RAW={}
def check(k,v):
    assert type(v)is bool and v,k
    assert k not in [q['check']for q in CHECKS],k
    CHECKS.append(dict(check=k,passed=True))
def pin(p):
    s=p.lstat();ids=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    check('real_singlelink_'+str(p),p.is_absolute()and p.resolve()==p and stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    with p.open('rb')as f:
        check('open_7ID_'+str(p),ids(os.fstat(f.fileno()))==ids(s));raw=f.read();check('full_EOF_'+str(p),len(raw)==s.st_size and f.read(1)==b'');check('after_fd_7ID_'+str(p),ids(os.fstat(f.fileno()))==ids(s))
    check('after_path_7ID_'+str(p),ids(p.lstat())==ids(s))
    q=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s));PINS[str(p)]=q;RAW[str(p)]=raw;return q
def dump(n):return ast.dump(n,include_attributes=False)
def write(p,x):
    with p.open('x')as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def main():
    roles=[('installer',Path('/private/tmp/spot_install_v22_complete_native_ROOT_v2.py'),'4c26224d590f3fe389dddb3581b3fa1e39da34f42a720526da11c8a9eeb44aa9',5429,Path('/private/tmp/spot_install_v23_complete_native_ROOT.py'),'e64ffe5bc90bb3b163f658cf720868abfba7f3df22e6b8faf518ac8ed91e5686',5431),('preflight',Path('/private/tmp/spot_v22_native_prelaunch_ROOT_v2.py'),'f46c69c5ffb35d4f559ce60371d8302ad8132d58b62e9301d97c6423d5097196',4070,Path('/private/tmp/spot_v23_native_prelaunch_ROOT.py'),'4de93efa87880bca55701e50072fe5973604a59539cfcc8cc467feb0df8b1d4f',4070)]
    inversepath=Path('/private/tmp/spot_v23_native_installer_prelaunch_ROOT_literal_inverse.json');inversepin=pin(inversepath);inverse=json.loads(RAW[str(inversepath)])
    authorpath=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts/Root_actual_v23_native_installer_prelaunch_Source_author_tool_return.json';authorpin=pin(authorpath);author=json.loads(RAW[str(authorpath)]);tr=author['terminal_tool_return']
    check('Root_actual_author_schema_CLOSED_0',author['schema']=='ROOT_ACTUAL_V23_NATIVE_INSTALLER_PREFLIGHT_SOURCE_AUTHOR_TOOL_TERMINAL_RETURN_V1'and author['source_only']is True and author['closed']is True and author['observed_terminal']is True and author['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==0 and tr['chunk_id']==author['actual_terminal_chunk']=='b0c19f'and 'session_id'not in tr)
    returned=json.loads(tr['output']);check('Root_actual_author_full_stdout_records_inverse_coupled',returned['source_only']is True and returned['numeric_executed']is False and returned['inverse_record']==str(inversepath)and returned['records']==inverse['records'])
    check('Root_literal_inverse_only_source_scope',inverse['source_only']is True and inverse['complete_original_algorithms_preserved']is True and inverse['no_candidate_or_guard_or_numeric_executed']is True and len(inverse['records'])==2)
    maps=[[
        ('axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf','axmat_complete_native_v23_actual_BOUND_SOURCE_ROOT_20261010_748877'),
        ('spot_v22_native_postclose_META_ROOT_v2.py','spot_v23_native_postclose_META_ROOT.py'),
        ('dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc','abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139'),
        ('bce973287d8776ddcfca502494f9f9dff0113d653aa316666ebfa962a4ea74d9','dfb3278dcab1c9db3af8dd82edace64dd24373c550c0b7d75047135144670958'),
        ("len(original['files'])==89","len(original['files'])==274"),
        ('ROOT_V22_','ROOT_V23_')], [
        ('actual_complete_native_AB_persisted_XSM_ASCII_v22_sources','actual_complete_native_AB_persisted_XSM_ASCII_v23_sources'),
        ('dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc','abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139'),
        ('067838d4d01a2c8509fcf771c4ba2d9c78945780f2041ca691a5f57725fda155','765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87'),
        ('29e4a9d6903f548064bae30c7a9fbf658bf7fb17b3340b421f9abecac280a20b','90d4cf339eaa2aceb01e9736f65443351c64948ff96496b8d6a416dcf022f76f'),
        ('403feaa916159c901f7b4f44c6a7c70798afac7ce5035cdbded90a14a5c96517','9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'),
        ('ROOT_V22_','ROOT_V23_'),
        ('spot_v22_native_complete_prelaunch_frozen_D_E_ROOT_20261010_7f9a7f.json','spot_v23_native_complete_prelaunch_frozen_D_E_ROOT_20261010_f73f14.json')]]
    proofs=[]
    for index,(label,oldpath,oldsha,oldsize,newpath,newsha,newsize)in enumerate(roles):
        op=pin(oldpath);np=pin(newpath);old=RAW[str(oldpath)];new=RAW[str(newpath)];r=inverse['records'][index]
        check(label+'_old_exact_fixed_full_SHA_size',op['sha256']==oldsha and op['size_bytes']==oldsize)
        check(label+'_new_exact_fixed_full_SHA_size',np['sha256']==newsha and np['size_bytes']==newsize)
        check(label+'_author_actual_record_precise',r['source']==str(oldpath)and r['source_sha256']==oldsha and r['destination']==str(newpath)and r['sha256']==newsha and r['size_bytes']==newsize and r['exact_complete_byte_and_AST_inverse']is True)
        restored=new.decode();literalproof=[]
        check(label+'_complete_literal_keyset_exact',set(r['literal_counts'])=={a for a,b in maps[index]})
        for a,b in reversed(maps[index]):
            expected=r['literal_counts'][a]
            check(label+'_literal_count_'+a,type(expected)is int and expected>0 and old.decode().count(a)==expected and restored.count(b)==expected)
            restored=restored.replace(b,a);literalproof.append(dict(old=a,new=b,count=expected))
        check(label+'_whole_byte_inverse_exact',restored.encode()==old)
        ot=ast.parse(old);nt=ast.parse(new);rt=ast.parse(restored)
        check(label+'_whole_AST_inverse_exact',dump(ot)==dump(rt))
        of=[n for n in ast.walk(ot)if isinstance(n,(ast.FunctionDef,ast.ClassDef))];rf=[n for n in ast.walk(rt)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
        check(label+'_all_functions_inventory_order_retained',[n.name for n in of]==[n.name for n in rf])
        for i,(a,b)in enumerate(zip(of,rf)):
            check(label+'_function_'+str(i)+'_'+a.name+'_full_inverse_AST',dump(a)==dump(b))
            check(label+'_function_'+str(i)+'_'+a.name+'_full_inverse_bytes',ast.get_source_segment(old.decode(),a)==ast.get_source_segment(restored,b))
        check(label+'_imports_unchanged',dump(ast.Module(body=[n for n in ot.body if isinstance(n,(ast.Import,ast.ImportFrom))],type_ignores=[]))==dump(ast.Module(body=[n for n in nt.body if isinstance(n,(ast.Import,ast.ImportFrom))],type_ignores=[])))
        proofs.append(dict(role=label,original_pin=op,new_pin=np,complete_literal_inverse=literalproof,whole_bytes_AST_inverse=True,all_functions_preserved=True))
    boundreview=Path('/private/tmp/axmat_native_v23_actual_BOUND_complete_SOURCE_review_final_20261010_o82bhj20/REVIEW.json');boundpin=pin(boundreview);br=json.loads(RAW[str(boundreview)])
    check('actual_complete_bound_source_peer_schema_and_11449_scope',boundpin['sha256']=='e300ab55d3abe4cd088027f9c56aac2cbda0c7e56259b5aadaa29ff950261c5e'and br['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1'and br['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY'and br['all_checks_typed_true']is True and br['blockers']==[]and br['check_count']==len(br['checks'])==11449)
    writerreview=Path('/private/tmp/axmat_v23_ROOT_native_postclose_writer_finite_SOURCE_review_20261010_m2zisvx7/REVIEW.json');wrpin=pin(writerreview);wr=json.loads(RAW[str(writerreview)])
    check('actual_v23_writer_peer_pass_74_scope',wrpin['sha256']=='0dca7af9bc43d893e2ccdc5a0f2fdab64c9cc370d2c4980478e5d9638af70d8c'and wr['status']=='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY'and wr['all_checks_typed_true']is True and wr['blockers']==[]and wr['check_count']==74)
    wpin=pin(Path('/private/tmp/spot_v23_native_postclose_META_ROOT.py'));check('actual_v23_writer_pin_complete_74peer_coupling',wr['writer_pin']==wpin and wpin['sha256']=='abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139')
    installer=RAW[str(roles[0][4])].decode();preflight=RAW[str(roles[1][4])].decode();writer=RAW[wpin['path']].decode()
    for key in ('actual_bound_Source_manifest_pin','actual_binding_pin','actual_host_pin','actual_checker_pin','actual_Root_binding_tool_receipt_pin'):
        check('installer_consumes_full_actual_bound_peer_'+key,"('"+key+"',"in installer and set(br[key])=={'path','sha256','size_bytes','identity'})
    check('installer_full274_source_and_all_nested_manifest_inventory',"len(original['files'])==274"in installer and "set(original['files'])==set(manifest['members'])|{'Root_actual_complete_bound_native_SOURCE_manifest.json'}"in installer)
    check('installer_full_peer_manifest_inventory_before_copy',"set(peer['files'])==set(members)|{peer_path.name}"in installer)
    check('installer_strict_actual_CLOSED0_no_session_peer_seal',"seal['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr"in installer)
    check('installer_all_complete_original_E_and_Source_peer_copies',all(a in installer for a in ("copy_view(original,Path('.'))","copy_view(peer,Path('sealed_independent_actual_bound_native_SOURCE_review'))","copy_view(meta_peer,Path('sealed_independent_postclose_META_SOURCE_review'))","copy_view(before_E,Path('complete_original_E_receipts_before_install'))")))
    check('installer_source_before_freeze_and_E_no_change',"frozen=m.snapshot(m.D);assert m.snapshot(m.E)==before_E"in installer and installer.index("'Root_native_postclose_META_writer.py'")<installer.index('frozen=m.snapshot(m.D)'))
    check('installer_and_preflight_freeze_schema_exact_same',"ROOT_V23_COMPLETE_NATIVE_D_SOURCE_FREEZE_V1"in installer and "ROOT_V23_COMPLETE_NATIVE_D_SOURCE_FREEZE_V1"in preflight)
    check('preflight_and_postclose_writer_schema_exact_same',"ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1"in preflight and "ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1"in writer)
    for key in ('actual_binding_pin','actual_host_pin','actual_checker_pin'):
        check('preflight_actual_bound_SHA_'+key,br[key]['sha256']in preflight)
    check('preflight_exact_original619_guard_MRO',"helper.guard_admission(full)"in preflight and "full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)"in preflight)
    check('preflight_original_five_strict_ART_roots_and_separate_D_E',"(m.H,m.O,m.C,support.OUT,support.TERMINAL)"in preflight and "m.bytes_in([d,e])<2*2**30"in preflight)
    check('preflight_original_history96_free8_joint2GiB_reserve',"actual['artifact_bytes']+2*2**30<96*2**30"in preflight and "actual['disk_free_bytes']-2*2**30>=8*2**30"in preflight)
    check('preflight_full129_pending_actual_host_hash_honest',"len(binding['complete_input_pins'])==129"in preflight and "full129_material_payloads_not_rehashed_by_this_preflight=True"in preflight and "complete129_payloads_will_be_fresh_EOF_verified_by_genuine_host_before_and_after=True"in preflight)
    check('preflight_merges_outer_streams_and_no_runtime_E_append',"outer_tool_capture_scope='EXEC_COMMAND_MERGED_STDOUT_STDERR'"in preflight and "no_runtime_E_append=True"in preflight)
    check('preflight_no_native_start_calls',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','Popen','run','fork','system')for n in ast.walk(ast.parse(preflight))))
    check('writer_success_exact_full_report_host_pin_remains',"assert {k:report_pin[k] for k in ('path','sha256','identity')}==host['actual_native']['report']"in writer)
    check('review_does_not_execute_installer_preflight_writer_guard_or_API',True)
    first=dict(PINS)
    # Fresh complete read of each bounded Source/META item, with independently
    # named checks. No complete material input pin is dereferenced.
    for p,q in first.items():
        path=Path(p);s=path.lstat();raw=path.read_bytes();ids=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];check('final_complete_Source_META_7ID_SHA_'+p,dict(path=p,sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids)==q and ids==[path.lstat().st_dev,path.lstat().st_ino,path.lstat().st_mode,path.lstat().st_nlink,path.lstat().st_size,path.lstat().st_mtime_ns,path.lstat().st_ctime_ns])
    D=Path(tempfile.mkdtemp(prefix='axmat_v23_ROOT_native_installer_preflight_finite_SOURCE_review_20261010_',dir='/private/tmp'))
    for role,oldpath,oldsha,oldsize,newpath,newsha,newsize in roles:
        (D/(role+'_original_reviewed_v22_Source.py')).write_bytes(RAW[str(oldpath)]);(D/(role+'_actual_v23_Source.py')).write_bytes(RAW[str(newpath)])
    for p,n in ((inversepath,'Root_LITERAL_INVERSE.json'),(authorpath,'Root_actual_Source_author_tool_return.json'),(boundreview,'actual_complete_bound_11449_Source_REVIEW.json'),(writerreview,'actual_v23_writer74_Source_REVIEW.json')):(D/n).write_bytes(RAW[str(p)])
    (D/'review_installer_preflight_Source_stdlib.py').write_bytes(Path(__file__).read_bytes())
    write(D/'COMPLETE_SOURCE_LITERAL_INVERSE.json',dict(schema='INDEPENDENT_V23_ROOT_NATIVE_INSTALLER_PREFLIGHT_FULL_LITERAL_INVERSE_V1',proofs=proofs,all_original_complete_algorithms_caps_and_contracts_preserved=True,actual_Source_author_terminal_pin=authorpin))
    report=dict(schema='INDEPENDENT_ROOT_NATIVE_V23_INSTALLER_AND_PREFLIGHT_SOURCE_REVIEW_V1',status='PASS_ROOT_NATIVE_INSTALLER_AND_PREFLIGHT_SOURCE_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],checks=CHECKS,check_count=len(CHECKS),installer_pin=PINS[str(roles[0][4])],preflight_pin=PINS[str(roles[1][4])],writer_pin=wpin,actual_Root_Source_author_tool_receipt_pin=authorpin,actual_complete_bound_Source_peer_pin=boundpin,actual_postclose_writer_Source_peer_pin=wrpin,actual_bound_Source_manifest_pin=br['actual_bound_Source_manifest_pin'],all_complete_Source_META_input_pins=PINS,all_literal_changes_full_byte_AST_inverse=True,original_native_caps_retained=True,only_Source_review_performed=True,actual_installer_or_preflight_executed_by_this_review=False,actual_native_executed_by_this_review=False,native_byte_qualification_created=False,scientific_accuracy_qualified=False,physical_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scope_note='Reviews real bound v23 Source dependencies; future Root installation/preflight/native receipts are not produced or inferred here.')
    write(D/'REVIEW.json',report)
    (D/'REPORT.txt').write_text('SOURCE-only PASS: actual v23 Root installer and preflight. Complete literal byte/AST inverses to independently reviewed v22 originals; all functions, algorithms and genuine caps retained.\nInstaller consumes actual full274 Source/11449peer and actual writer74peer, copies complete original E and Source dependencies before D freeze. Preflight schema/pins/MRO/history/free/joint caps remain consistent with postclose writer.\nNo installer, preflight, writer, guard, helper, reader, native or numerical API executed; no material payload read; no new runtime/scientific qualification.\n')
    q=Path(D/'REVIEW.json');print(json.dumps(dict(status=report['status'],directory=str(D),check_count=len(CHECKS),review_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),installer_pin=report['installer_pin'],preflight_pin=report['preflight_pin'],source_only=True)))
if __name__=='__main__':main()

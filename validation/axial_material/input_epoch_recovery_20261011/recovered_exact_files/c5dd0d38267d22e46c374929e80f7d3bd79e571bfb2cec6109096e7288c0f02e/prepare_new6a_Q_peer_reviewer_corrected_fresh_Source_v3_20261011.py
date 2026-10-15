import pathlib,json,hashlib,os,stat,ast,tempfile
OLD=pathlib.Path('/private/tmp/SPOT_NEW6A_Q_INDEPENDENT_ACTUAL_RESULT_REVIEW_SOURCE_ONLY_hrup15t7');NEW=pathlib.Path(tempfile.mkdtemp(prefix='SPOT_NEW6A_Q_INDEPENDENT_REVIEW_COMPLETE_FRESH_SOURCE_ONLY_',dir='/private/tmp'));M=json.loads((OLD/'FINAL_SOURCE_ONLY_MANIFEST.json').read_bytes());S=pathlib.Path(M['reviewer_Source']['path']).read_text()
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);a=p.lstat();h=hashlib.sha256();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
 with p.open('rb') as f:
  assert ids(os.fstat(f.fileno()))==ids(a)
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
  assert ids(os.fstat(f.fileno()))==ids(a)
 assert ids(p.lstat())==ids(a);return dict(path=str(p),size_bytes=a.st_size,sha256=h.hexdigest(),identity=ids(a))
fresh=[pin(p) for p in ['/private/tmp/Root_corrected_new6a_Q_v3_actual_tool_returns_20261011.json','/private/tmp/prepare_new6a_Q_independent_actual_saved_review_Source_v1_20261011.py','/private/tmp/prepare_new6a_Q_independent_actual_saved_review_Source_v2_20261011.py','/private/tmp/new6a_Q_peer_review_Source_prepare_v2_inverse_20261011.json','/private/tmp/new6a_Q_peer_reviewer_Source_v2_actual_schema_preflight_20261011.json',__file__]]
add='\n_PEER_CURRENT_FRESH_PINS='+repr(fresh)+'\n_PEER_SOURCE_ROOTS=[Path('+repr(str(OLD))+'),Path(__file__).parent]\n_PEER_SOURCE_FREEZE=None\n'+'''
def complete_peer_account(reserve):
    global _PEER_SOURCE_FREEZE
    original=account(reserve)
    ns=[]
    for root in _PEER_SOURCE_ROOTS:
        ck(root.is_dir() and not root.is_symlink(),'peer complete ordinary Source namespace')
        paths=sorted(root.rglob('*'),key=str);dirs=[];files=[]
        for p in [root,*paths]:
            s=p.lstat();ck(not stat.S_ISLNK(s.st_mode),'peer Source no aliases')
            if stat.S_ISDIR(s.st_mode):dirs.append(dict(path=str(p),identity=identity(s)))
            else:files.append(pin(p));verify(files[-1])
        ck(paths==sorted(root.rglob('*'),key=str),'peer Source full pathset unchanged')
        ns.append(dict(root=str(root),directories=dirs,files=files))
    if _PEER_SOURCE_FREEZE is None:_PEER_SOURCE_FREEZE=ns
    else:ck(ns==_PEER_SOURCE_FREEZE,'peer full Source namespace frozen beforeafter')
    for p in _PEER_CURRENT_FRESH_PINS:verify(p)
    rows=[*after['complete_joint_roots_inode_once'],dict(path=str(out))]+[dict(path=str(root)) for root in _PEER_SOURCE_ROOTS]+[dict(path=p['path']) for p in _PEER_CURRENT_FRESH_PINS]
    seen=set();total=0
    for row in rows:
        p=Path(row['path'])
        if not p.exists():ck(not p.is_symlink(),'peer future output not dangling');continue
        s=p.lstat();ck(not stat.S_ISLNK(s.st_mode),'peer joint no aliases')
        members=sorted(p.rglob('*'),key=str) if stat.S_ISDIR(s.st_mode) else [p]
        for m in members:
            ms=m.lstat();ck(not stat.S_ISLNK(ms.st_mode),'peer joint member no aliases')
            if stat.S_ISDIR(ms.st_mode):continue
            ck(stat.S_ISREG(ms.st_mode) and ms.st_nlink==1,'peer inode-once ordinary file')
            key=(ms.st_dev,ms.st_ino)
            if key not in seen:seen.add(key);total+=ms.st_size
    ck(total+reserve<2*2**30,'peer complete actual Qfamily Source fresh files output joint2GiB')
    free={str(root):int(os.statvfs(root).f_bavail)*int(os.statvfs(root).f_frsize) for root in _PEER_SOURCE_ROOTS}
    ck(min([*free.values(),*(int(os.statvfs(Path(p['path']).parent).f_bavail)*int(os.statvfs(Path(p['path']).parent).f_frsize) for p in _PEER_CURRENT_FRESH_PINS)])-reserve>=8*2**30,'all actual peer TMP source/file free8GiB reserved')
    return dict(original_resource_return=original,complete_peer_joint_bytes=total,reserved_bytes=reserve,complete_peer_Source_namespaces=ns,explicit_current_peer_fresh_input_pins=_PEER_CURRENT_FRESH_PINS,tmp_free_bytes=free,original_joint2_history96_free8_and_wholephysics_limits_unchanged=True)
'''
changes=[]
def rep(a,b):
 global S
 assert S.count(a)==1,(a[:150],S.count(a));S=S.replace(a,b,1);changes.append(dict(before=a,after=b))
rep('CHECKS=[];INPUTS={}',add+'\nCHECKS=[];INPUTS={}')
rep('original_before=account(4*2**20);checkpoint()','original_before=complete_peer_account(4*2**20);checkpoint()')
rep('original_after=account(1024*1024);finalcheck=checkpoint()','''original_after=complete_peer_account(1024*1024);finalcheck=checkpoint()
resource_witness=dict(schema='SPOT_ACTUAL_NEW6A_Q_INDEPENDENT_SAVED_REVIEW_RESOURCE_WITNESS_V1',actual_metadata_Q=QPIN,actual_saved_review=reviewpin,actual_independent_review_Source=selfpin,resources_before=original_before,resources_after_review_before_resource_witness=original_after,actual_checkpoint_after_review=finalcheck,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)
with (out/'ACTUAL_RESOURCE_WITNESS.json').open('x') as f:json.dump(resource_witness,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\\n');f.flush();os.fsync(f.fileno())
resource_witness_pin=pin(out/'ACTUAL_RESOURCE_WITNESS.json')
ck(resource_witness_pin['size_bytes']<1024*1024,'peer resourcewitness fits original1MiB reservation')
peer_final_account=complete_peer_account(0);peer_final_checkpoint=checkpoint()''')
rep("actual_original_after_resource_summary=dict(joint_bytes=original_after['joint_bytes'],history_including_external_DE_bytes=original_after['history_including_external_DE_bytes'],reserved_bytes=original_after['reserved_bytes']),actual_final_checkpoint=finalcheck","actual_peer_resource_witness=resource_witness_pin,actual_final_peer_complete_joint_bytes=peer_final_account['complete_peer_joint_bytes'],actual_original_after_resource_summary=dict(joint_bytes=peer_final_account['original_resource_return']['joint_bytes'],history_including_external_DE_bytes=peer_final_account['original_resource_return']['history_including_external_DE_bytes'],reserved_bytes=peer_final_account['reserved_bytes']),actual_final_checkpoint=peer_final_checkpoint")
ast.parse(S);p=NEW/'REVIEW_ACTUAL_NEW6A_METADATA_Q_AFTER_REAL_WRITER_CLOSED0.py';p.write_text(S);sp=pin(p)
r=S
for c in reversed(changes):assert r.count(c['after'])==1;r=r.replace(c['after'],c['before'],1)
assert r.encode()==pathlib.Path(M['reviewer_Source']['path']).read_bytes()
man=dict(status='SOURCE_ONLY_FULL235_ACTUAL_Q_INDEPENDENT_REVIEW_WITH_COMPLETE_PEER_FRESH_BUDGET_PENDING_ROOT',reviewer_Source=sp,original_Source= M['reviewer_Source'],original_Source_manifest=pin(OLD/'FINAL_SOURCE_ONLY_MANIFEST.json'),original_resource_prefix_Source=M['old_original_resource_prefix_Source'],original_resource_prefix_full_inverse_sha256=M['original_resource_prefix_full_inverse_sha256'],original_resource_prefix_joint_account_functions_unchanged=True,whole_inverse_to_original24k_reviewer_byte_exact=True,Source_forward_changes=changes,complete_peer_fresh_external_input_pins=fresh,complete_original_and_new_peer_Source_roots=[str(OLD),str(NEW)],unchanged_metadata_contract_Source=M['metadata_contract_Source'],actual_closed_writer_tools_pin=pin(M['expected_real_writer_tool_file']),actual235_Q_and_resourcewitness_known=True,actual_complete_declared_input_union235_preflight=pin('/private/tmp/new6a_Q_peer_reviewer_Source_v2_actual_schema_preflight_20261011.json'),actual_peer_REVIEW_and_resourcewitness_not_created=True,original_thread1_600s_512MiB_joint2GiB_history96_free8_fiveguards_DE_preserved=True,Source_only=True,reviewer_writer_factory_Native_or_PS_executed=False,helper_numeric_or_fullgraph_business_api_executed=False,no_whole_INPUT_science_or_BOOT_qualification_created=True,preparation_Source=pin(__file__))
mp=NEW/'FINAL_SOURCE_ONLY_MANIFEST.json';mp.write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'Source_root':str(NEW),'Source':sp,'manifest':pin(mp),'Source_only':True,'reviewer_writer_factory_Native_or_PS_executed':False}))

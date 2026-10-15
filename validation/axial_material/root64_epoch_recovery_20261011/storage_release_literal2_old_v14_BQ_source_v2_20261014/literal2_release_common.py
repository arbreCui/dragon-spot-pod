"""Literal2 old failedv14 private BQ files only; default readonly, no retry."""
import ast,hashlib,importlib.util,json,os,stat,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';PKG=Path(__file__).absolute().parent
BASE_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py', 'sha256': 'b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d', 'size_bytes': 18001, 'identity': [16777229, 49980314, 33188, 1, 18001, 1791847138307427020, 1791847138307427020]}
CAPS={'SELF_mib': 512, 'whole_seconds': 1800, 'stage_seconds': 600, 'threads': 1, 'children_at_once': 1, 'fresh_bytes': 2147483648, 'history_bytes': 103079215104, 'free_floor_bytes': 8589934592, 'cold_reserve_bytes': 20971764748, 'metadata_reserve_bytes': 67108864}
HISTORICAL_PINS={'previous_curated66_Source_freeze': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/storage_release_curated66_old_private_copies_source_v3_20261013/COMPLETE_CURATED66_OLD_PRIVATE_RELEASE_SOURCE_FREEZE.json', 'sha256': 'ad95f9f9a2e1a94f5070bb6c335621b1b4b95c6543af6d1dbe9637c73fc1412d', 'size_bytes': 43297, 'identity': [16777229, 50066022, 33188, 1, 43297, 1791901316139267628, 1791901316139267628]}, 'previous7030_manifest': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/storage_release_curated66_old_private_copies_source_v3_20261013/EXACT_CURATED66_OLD_PRIVATE_RELEASE_MANIFEST.json', 'sha256': '938c685869b5fd6e9e0e8579be66c8de9eb1a45bae9afb3695a3e3eb57db014f', 'size_bytes': 6559455, 'identity': [16777229, 50066432, 33188, 1, 6559455, 1791901724326175083, 1791901724326175083]}, 'completed_actual_curated66_release': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/storage_release_curated66_old_private_copies_actual_receipts_20261013/ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT.json', 'sha256': '114d2fd0f13c1af1396823cbba0c4b693130361092ed83ad4ecb6ca2849aadda', 'size_bytes': 436781, 'identity': [16777229, 50067069, 33188, 1, 436781, 1791902421754037345, 1791902421754037345]}, 'completed_independent_curated66_postreview': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_curated66_actual_postrelease_review_20261013/REVIEW.json', 'sha256': 'ab1fcf77e4668111c4f596cde66e36fe5433500daeec535a4bddd6652ccdb62e', 'size_bytes': 3949938, 'identity': [16777229, 50067397, 33188, 1, 3949938, 1791902708212398512, 1791902708212398512]}, 'completed_independent_curated66_post_tools': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_curated66_actual_postrelease_review_20261013/TRUE_TOOL_RETURNS.json', 'sha256': 'e16e552573491e2087fc4d9345aa49d850bdb4ede5535f9bae4769377f4f50cb', 'size_bytes': 1304, 'identity': [16777229, 50067411, 33188, 1, 1304, 1791902733530484372, 1791902733530484372]}, 'literal2_source_survey': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_literal2_failed_v14_BQ_storage_role_survey_20261013/REVIEW.json', 'sha256': 'af96d430d4862b0d89138f483db2ec7c4d3456dd1ff0bafe6b049cff533a5832', 'size_bytes': 11384, 'identity': [16777229, 50072090, 33188, 1, 11384, 1791907091509031567, 1791907091509031567]}, 'literal2_source_survey_tools': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_literal2_failed_v14_BQ_storage_role_survey_20261013/TRUE_TOOL_RETURNS.json', 'sha256': '604f72ea5322fbc651bfb25e0a44d1890c3324cccc104a42016a03aba827c14b', 'size_bytes': 1205, 'identity': [16777229, 50072117, 33188, 1, 1205, 1791907129077568128, 1791907129077568128]}}
CURRENT_SELECTIONS=[{'role': 'build4', 'Host_freeze_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_compact_expected_build_host_source_v4_20261013/COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json', 'sha256': '38ad77ba82cf38acf45f1ecaf2ccbaaf12d230c78e75e114adde4fa0a77645b7', 'size_bytes': 979332, 'identity': [16777229, 50069102, 33188, 1, 979332, 1791904380243951068, 1791904380243951068]}, 'actual_report_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4/Root_actual_build_only_summary.json', 'sha256': '74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f', 'size_bytes': 2333640, 'identity': [16777229, 50069280, 33188, 1, 2333640, 1791904584137298133, 1791904584137298133]}, 'exact_cli_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_compact_expected_build_host_source_v4_20261013/ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json', 'sha256': '35ca85ab88f6060bce789a473c66e932c8ebe0ef5d3902dea0516e1e8ce9a1ca', 'size_bytes': 3585, 'identity': [16777229, 50069103, 33188, 1, 3585, 1791904380244772903, 1791904380244772903]}, 'actual_output_root': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4', 'actual_status': 'ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY', 'actual_failure': None, 'expected_dependency_count': 2565, 'actual_fixed_count': 2566, 'actual_output_count': 10}, {'role': 'fresh17', 'Host_freeze_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_compact_expected_connected17_host_source_v2_20261013/COMPLETE_FRESH17_NEW_BOOTQ_HOST_SOURCE_FREEZE.json', 'sha256': '88db202f3eebb22578b6f58a91050a41acaf0de35ba2e0718a5ba49a9deb3a89', 'size_bytes': 989284, 'identity': [16777229, 50069665, 33188, 1, 989284, 1791904983281321230, 1791904983281321230]}, 'actual_report_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v2/Root_actual_connected17_summary.json', 'sha256': '7809453e0ebc8350ba3c4e8d47078795485527913f8b174e5c0817a0eba42cde', 'size_bytes': 9091563, 'identity': [16777229, 50070314, 33188, 1, 9091563, 1791905563527882236, 1791905563527882236]}, 'exact_cli_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_compact_expected_connected17_host_source_v2_20261013/ROOT_REVIEWABLE_EXACT_FRESH17_ARGV.json', 'sha256': '460b18aad776bc2e6827efb54e30b3bb71069daa13796fc333b7a930d610a67e', 'size_bytes': 3349, 'identity': [16777229, 50069666, 33188, 1, 3349, 1791904983282238774, 1791904983282238774]}, 'actual_output_root': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v2', 'actual_status': 'ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY', 'actual_failure': None, 'expected_dependency_count': 2586, 'actual_fixed_count': 2587, 'actual_output_count': 47}, {'role': 'model5', 'Host_freeze_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_private_GANLIB_model_control_host_source_v5_20261013/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json', 'sha256': '04d05551c688cee59e421a3f5e2cba9ff1a45905bd4333b1392c2ed60617c269', 'size_bytes': 999296, 'identity': [16777229, 50071438, 33188, 1, 999296, 1791906654616283603, 1791906654616283603]}, 'actual_report_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5/Root_actual_control_summary.json', 'sha256': 'a7724f8d8c9d334cd75a2c2e088269645385ef46d059af74ee9accff1c6b74f1', 'size_bytes': 2693213, 'identity': [16777229, 50072317, 33188, 1, 2693213, 1791907269514309368, 1791907269514309368]}, 'exact_cli_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bq64_private_GANLIB_model_control_host_source_v5_20261013/ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json', 'sha256': '726ab8016bbf6b2c8f8a3eff774c8f382bbb8aebeaf7d4030d082bdbaee97d8a', 'size_bytes': 4906, 'identity': [16777229, 50071439, 33188, 1, 4906, 1791906654619314526, 1791906654619314526]}, 'actual_output_root': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5', 'actual_status': 'ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY', 'actual_failure': None, 'expected_dependency_count': 2597, 'actual_fixed_count': 2610, 'actual_output_count': 14}, {'role': 'public5_failed', 'Host_freeze_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/public_read_compact_bq_admission_control_host_source_v5_20261013/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json', 'sha256': 'ddfdd1f10faf646541f6f13b174b71ad6f0d431da0edb3d96a232dd430603345', 'size_bytes': 1005274, 'identity': [16777229, 50071440, 33188, 1, 1005274, 1791906654652667684, 1791906654652667684]}, 'actual_report_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/Root_actual_control_summary.json', 'sha256': 'c60ae9b8eb0b410fd286e0b93e11dc110b029f69d5a3240b4b23184895d1652e', 'size_bytes': 5377582, 'identity': [16777229, 50072524, 33188, 1, 5377582, 1791907360247363139, 1791907360247363139]}, 'exact_cli_pin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/public_read_compact_bq_admission_control_host_source_v5_20261013/ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json', 'sha256': '0820b4b931772a966ae4fb5b168758bb475befbbddcc61da72b6000d411fa112', 'size_bytes': 5001, 'identity': [16777229, 50071441, 33188, 1, 5001, 1791906654653461102, 1791906654653461102]}, 'actual_output_root': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5', 'actual_status': 'ACTUAL_CONTROL_FAILED_UNQUALIFIED', 'actual_failure': "RuntimeError('original remaining runtime/context/log/meta storage planning bound128MiB')", 'expected_dependency_count': 2609, 'actual_fixed_count': 2622, 'actual_output_count': 30}]
OWNER={'root': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14', 'summary_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/Root_actual_three_plane_engineering_summary.json', 'sha256': '6d2757e8aa984c5154b75128f0f568a307149cd4056241bf1a9713968820d903', 'size_bytes': 1827141, 'identity': [16777229, 50056722, 33188, 1, 1827141, 1791895780743395721, 1791895780743395721]}, 'complete_raw_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/Root_actual_complete_execution_record_before_final_publication.json', 'sha256': '59c17b3eabb3edef83e1a16ad840e1bd080d4aeaae983b0610edd971b6d7ba6a', 'size_bytes': 14543455, 'identity': [16777229, 50056720, 33188, 1, 14543455, 1791895779257535093, 1791895779257535093]}, 'stages_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/AAA3-streaming/stages.json', 'sha256': '788df0657a7305b70e5268d0683c9f6a0ba4049f6c239a5b784deaefb3317a33', 'size_bytes': 12408760, 'identity': [16777229, 50056719, 33188, 1, 12408760, 1791895777776914314, 1791895777777114815]}, 'last_watchdog_pin': {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/AAA/BOOT_positive.watchdog.json', 'sha256': '66917617ece3752795bfc6204bd62ceab22103ae6b4fbdd31ac08f10bdd17370', 'size_bytes': 496, 'identity': [16777229, 50056718, 33188, 1, 496, 1791895777714993295, 1791895777714993295]}, 'actual_failure': 'RuntimeError: remaining runtime/context/log/meta storage planning bound128MiB', 'actual_record_count': 50, 'actual_last_child_integer_returncode': -15, 'engineering_closed0': False, 'AAA_qualified': False}
TARGET_SELECTED_PINS=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/AAA/BQ64-MAC-ST', 'sha256': 'e333a14457c777f676490c3961244419354b4129e78aa49eb691eec46142af13', 'size_bytes': 9893580, 'identity': [16777229, 50056699, 33152, 1, 9893580, 1791895775554590434, 1791895775554590434]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14/AAA/BQ64-SRC-ST', 'sha256': 'd1aca3f5929dcf765c765795e35f2ad55baa9e0fdc9404e650462cc612cb2a4d', 'size_bytes': 518589052, 'identity': [16777229, 50056700, 33152, 1, 518589052, 1791895775774856970, 1791895775774856970]}]
PUBLIC5_FAILED_BUNDLES=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/public_read_stale_BQ_MAC/coherent_complete_context.xsm', 'sha256': '2ba7398987f21ce747691ca5d635a374e5793ce7f2dbad2a30b1bb827d4c9061', 'size_bytes': 100163528, 'identity': [16777229, 50072511, 33152, 1, 100163528, 1791907356383958366, 1791907356383958366]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/public_read_stale_BQ_SRC/coherent_complete_context.xsm', 'sha256': '2ba7398987f21ce747691ca5d635a374e5793ce7f2dbad2a30b1bb827d4c9061', 'size_bytes': 100163528, 'identity': [16777229, 50072481, 33152, 1, 100163528, 1791907347722299725, 1791907347722299725]}]
BRANCHES=[Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14')]
V14_OUT=BRANCHES[0]
V12_OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12')
TARGETS=[Path(r['path'])for r in TARGET_SELECTED_PINS];TARGET_PATHS={str(p)for p in TARGETS};BYTES=528482632
SOURCE_NAMES=('literal2_release_common.py','prepare_literal2_manifest.py','verify_or_execute_literal2.py')
SF=PKG/'COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json';FINAL=PKG/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json';RECEIPTS=REC/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014'

def _base():
    p=Path(BASE_PIN['path']);a=p.lstat();ident=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(a.st_mode)or ident(a)!=BASE_PIN['identity']:raise RuntimeError('original immutable helper all7')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if ident(os.fstat(f.fileno()))!=ident(a):raise RuntimeError('helper FD changed')
        h=hashlib.file_digest(f,'sha256').hexdigest()
        if ident(os.fstat(f.fileno()))!=ident(a):raise RuntimeError('helper EOF changed')
    if ident(p.lstat())!=ident(a)or h!=BASE_PIN['sha256']:raise RuntimeError('original helper bytes changed')
    spec=importlib.util.spec_from_file_location('immutable_curated66_readonly_helpers',p);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);return b
b=_base();pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new

def external(path,sha,seven):
    r=pin(path)
    if r['sha256']!=sha or r['identity']!=json.loads(seven):raise RuntimeError('exact external SHA/all7 required')
    return r

def inventory(roots=BRANCHES):
    files={};dirs={};links={};stack=list(roots)
    while stack:
        p=stack.pop();b.ancestors(p);before=p.lstat()
        if not stat.S_ISDIR(before.st_mode):raise RuntimeError('ordinary owner directory')
        dirs[str(p)]=identity(before);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=identity(before):raise RuntimeError('directory changed at open')
            with os.scandir(fd)as entries:
                for e in entries:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('special old namespace entry')
            if identity(os.fstat(fd))!=identity(before):raise RuntimeError('directory changed during inventory')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)

def receipt_pin(p):
    p=Path(p);b.ancestors(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1 or s.st_size>64*2**20:raise RuntimeError('bounded own exclusive receipt')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('receipt FD changed')
        h=hashlib.file_digest(f,'sha256').hexdigest()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('receipt EOF changed')
    if identity(p.lstat())!=identity(s):raise RuntimeError('receipt path changed')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))

def update_owned(p,v,old):
    if receipt_pin(p)!=old:raise RuntimeError('same receipt all7/EOF changed')
    raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>64*2**20:raise RuntimeError('receipt64MiB cap')
    fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
    with os.fdopen(fd,'r+b')as f:
        before=identity(os.fstat(f.fileno()))
        if before!=old['identity']or before[3]!=1 or p.lstat().st_uid!=os.getuid():raise RuntimeError('same owned receipt FD before update')
        f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno());after=identity(os.fstat(f.fileno()))
        if after!=identity(p.lstat())or after[:4]!=before[:4]:raise RuntimeError('same receipt inode/mode/link after fsync')
    return receipt_pin(p)

def budget():
    f=read(pin(SF));same(f['original_resource_factory_pin']);return b.budget()


def source_gate(sfpin):
    if sfpin['path']!=str(SF):raise RuntimeError('exact literal2 Source namespace')
    f=read(sfpin)
    if f['schema']!='COMPLETE_LITERAL2_OLD_FAILED_V14_PRIVATE_BQ_RELEASE_SOURCE_ONLY_FREEZE_V1'or f['source_only']is not True or f['manifest_prepared']is not False or f['deletion_executed']is not False or f['compiler_or_business_executed']is not False or f['original_caps']!=CAPS or f['literal2_fullpins']!=TARGET_SELECTED_PINS or f['historical_evidence_pins']!=HISTORICAL_PINS or f['current_actual_selections']!=CURRENT_SELECTIONS or f['literal_failed_owner_proof']!=OWNER:raise RuntimeError('exact immutable2 Source scope/caps/roles')
    if [p['path']for p in f['Source_pins']]!=[str(PKG/n)for n in SOURCE_NAMES]:raise RuntimeError('three exact Source files')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values()):same(p)
    same(f['original_resource_factory_pin'])
    if f['original_resource_factory_pin']['path']!=str(b.FACTORY):raise RuntimeError('original exact resource factory')
    survey=read(HISTORICAL_PINS['literal2_source_survey']);tool=read(HISTORICAL_PINS['literal2_source_survey_tools']);closed=tool['actual_review_return']
    if type(closed['exit_code'])is not int or closed['exit_code']!=0 or closed.get('session_id')is not None or b.norm(json.loads(closed['output'].strip().splitlines()[-1])['review_pin'])!=HISTORICAL_PINS['literal2_source_survey']or survey['failure']is not None or survey['exact_literal_target_count']!=2 or survey['total_logical_bytes']!=BYTES:raise RuntimeError('real literal2 source survey0')
    return f

def review_gate(sfpin,reviewpin,toolpin):
    d=read(reviewpin);t=read(toolpin);a=t.get('actual_review_return')
    if d.get('Source_freeze_pin')!=sfpin or d.get('failure')is not None or d.get('business_executed')is not False or t.get('observed_closed')is not True or type(t.get('original_integer_exit_code'))is not int or t['original_integer_exit_code']!=0 or not isinstance(a,dict)or type(a.get('exit_code'))is not int or a['exit_code']!=0 or a.get('session_id')is not None or b.norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=reviewpin:raise RuntimeError('genuine exact owning Source review0')

def closed_proofs():
    s=read(OWNER['summary_pin']);raw=read(OWNER['complete_raw_pin']);stages=read(OWNER['stages_pin']);w=read(OWNER['last_watchdog_pin'])
    compact=lambda rs:[{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in rs]
    if s['failure']!=OWNER['actual_failure']or s['engineering_three_plane_closed0']is not False or s['actual_terminal']is not None or s['AAA_qualified']is not False or compact(s['records'])!=compact(raw['records'])or stages!={'stages':raw['records']}or len(s['records'])!=OWNER['actual_record_count']or type(w['returncode'])is not int or w['returncode']!=OWNER['actual_last_child_integer_returncode']or w['own_child_only']is not True or w['liveness_group_cleanup']is not True:raise RuntimeError('exact actual failed-unqualified v14 owner closed proof')
    return [OWNER]

def disjoint(protected):
    if len(TARGETS)!=2 or len(TARGET_PATHS)!=2 or sum(p['size_bytes']for p in TARGET_SELECTED_PINS)!=BYTES or len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=2:raise RuntimeError('exact2 paths/physicalnodes/bytes')
    paths={p['path']for p in protected};nodes={tuple(p['identity'][:2])for p in protected}
    for path,p in zip(TARGETS,TARGET_SELECTED_PINS):
        b.ancestors(path);s=path.lstat()
        if str(path)!=p['path']or identity(s)!=p['identity']or s.st_uid!=os.getuid()or s.st_nlink!=1 or not stat.S_ISREG(s.st_mode)or str(path)in paths or tuple(p['identity'][:2])in nodes:raise RuntimeError('owned literal2 UID/all7/nlink1/nonsymlink/disjoint')
        same(p)

def current_protection(sfpin,reviews):
    f=source_gate(sfpin);old=read(HISTORICAL_PINS['previous7030_manifest']);done=read(HISTORICAL_PINS['completed_actual_curated66_release']);post=read(HISTORICAL_PINS['completed_independent_curated66_postreview']);table={};roles={};cache={}
    if done['status']!='EXACT_CURATED66_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'or done['deleted_files']!=66 or done['logical_bytes_released']!=1751559764 or done['manifest_pin']!=HISTORICAL_PINS['previous7030_manifest']or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_actual_curated66_release']:raise RuntimeError('immutable completed curated66 historical facts')
    oldrows=old['current_protected_full_EOF_pins']
    if len(oldrows)!=7030 or [oldrows[i]for i in (4166,4167)]!=TARGET_SELECTED_PINS or {p['path']for p in oldrows}&TARGET_PATHS!=TARGET_PATHS:raise RuntimeError('only exact2 prior7030 historical protected declarations')
    def add(p,role):
        p=b.norm(p);path=p['path'];actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or path in TARGET_PATHS or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected exactPF changed or aliases target')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):
        if i not in(4166,4167):add(p,'original7028_protected_every_other_row_retained')
    before=inventory();oldinv=old['Source_DAG_provenance']['current_v14_complete_inventory']
    if before!=oldinv or len(before['ordinary_file_identities'])!=299 or before['symlinks']:raise RuntimeError('whole latestfailedv14 original299/36 inventory changed')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:
            actual=pin(path);add(actual,'all_other297_v14_Q1_MAC1_PROJECT_science_results_logs_summary_sources_retained');retained.append(actual)
    current12=inventory([V12_OUT])
    if current12!=old['Source_DAG_provenance']['current_v12_complete_inventory']:raise RuntimeError('entire v12 namespace changed')
    for selected in CURRENT_SELECTIONS:
        hf=read(selected['Host_freeze_pin']);a=read(selected['actual_report_pin']);cli=read(selected['exact_cli_pin'])
        if len(hf['dependencies'])!=selected['expected_dependency_count']or len(a['fixed_current_pins'])!=selected['actual_fixed_count']or len(a['output_pins'])!=selected['actual_output_count']or a['status']!=selected['actual_status']or a['failure']!=selected['actual_failure']or a['actual_host_Source_freeze_pin']!=selected['Host_freeze_pin']:raise RuntimeError('exact current selected Host/actual report pins and role counts/status')
        if selected['role']=='public5_failed'and(a['status']!='ACTUAL_CONTROL_FAILED_UNQUALIFIED'or a['actual_seven_genuine_public_READ_controls_passed']is not False):raise RuntimeError('failed public5 scene is retained unqualified evidence')
        rows=[selected['Host_freeze_pin'],selected['actual_report_pin'],selected['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']
        # Only direct current PF lists are live. Nested historical JSON is never promoted.
        for p in rows:add(p,'current_'+selected['role']+'_entire_HF_ownHost_actual_fixed_output_summary_retained')
        actual_inventory=inventory([Path(selected['actual_output_root'])])
        if set(actual_inventory['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{selected['actual_report_pin']['path']}or actual_inventory['symlinks']:raise RuntimeError('full selected actual output scene contains unregistered/aliased file')
        for p in PUBLIC5_FAILED_BUNDLES:
            if selected['role']=='public5_failed':same(p)
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin]:add(p,'own_Source_and_completed_historical_metadata_retained_as_files')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_actual_source0');add(t,who+'_actual_source0_tools')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=7030,only_two_original_indices_migrated_to_historical=[4166,4167],all_original_other7028_PF_rows_data_retained=True,historical_original7030_and_v14_299_attestation_not_rewritten=True,current_v14_complete_inventory=before,current_v12_complete_inventory=current12,protected_all_current_success_and_failed_public5_actual_outputs=True,old_nested_JSON_historical_PF_not_live_dependencies=True),retained,before

def writer_gate(protected):
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],capture_output=True,text=True,timeout=20)
    if proc.returncode!=0 or proc.stderr.strip():raise RuntimeError('real process metadata unavailable')
    owners=[str(REC/('aaa_three_plane_streaming_pipeline_source_v'+str(v))/'run_actual_three_plane_pipeline.py')for v in range(1,16)]+[p['path']for p in protected if Path(p['path']).suffix=='.py'and any(w in Path(p['path']).name for w in('run_','prepare_','finalize_','freeze_','write_'))]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)!=2 or int(fields[0])==os.getpid():continue
        command=fields[1]
        if int(fields[0])==os.getppid()and Path(command.split(None,1)[0]).name in('zsh','bash','sh')and str(Path(sys.argv[0]).absolute())in command:continue
        if any(p in command for p in owners+[str(PKG)])or(str(ART)in command and('/runtime/Dragon'in command or'run_bounded_dragon.py'in command)):raise RuntimeError('active protected writer or owned business')
    for branch in BRANCHES+[V12_OUT]+[Path(s['actual_output_root'])for s in CURRENT_SELECTIONS]:
        opened=subprocess.run(['/usr/sbin/lsof','-nP','+D',str(branch)],capture_output=True,text=True,timeout=30)
        if opened.returncode not in(0,1)or opened.stdout.strip()or opened.stderr.strip():raise RuntimeError('protected/target namespace open handle or real lsof unavailable')
    guard()

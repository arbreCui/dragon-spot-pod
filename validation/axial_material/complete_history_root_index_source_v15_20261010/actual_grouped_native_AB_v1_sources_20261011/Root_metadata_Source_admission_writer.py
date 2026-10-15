"""Root-only future metadata writer; never import or execute candidate modules.

Authoring this file creates no gate, READY Source or project namespace. Only a
later explicit Root CLI invocation may create fresh D/E metadata after real
closed sixteen controls and their actual reviews. E stays empty for the real
independent full-binding prelaunch review. H/O/C stay absent. The only project
import permitted here is the genuine fixed training disk resource guard.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import stat
import sys
import time

SOURCE_STATUS = 'SOURCE_ONLY_ROOT_METADATA_WRITER_NO_NATIVE_CANDIDATE_EXECUTION'
READY_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
ROOT = Path('/Users/wen/spot')
BASE = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = ROOT/'validation/artifacts'
OLD_D = BASE/'actual_original_grouped16_tiny_controls_v3_sources_20261011'
OLD_E = BASE/'actual_original_grouped16_tiny_controls_v3_receipts_20261011'
OLD_H = ART/'axial-material-original-grouped16-tiny-controls-v3-20261011-host'
OLD_C = ART/'axial-material-original-grouped16-tiny-controls-v3-20261011-control'
D = BASE/'actual_grouped_native_AB_v1_sources_20261011'
E = BASE/'actual_grouped_native_AB_v1_receipts_20261011'
NAMESPACES = dict(host=str(ART/'axial-material-grouped-native-AB-v1-20261011-host'),
    output=str(ART/'axial-material-grouped-native-AB-v1-20261011-output'),
    control=str(ART/'axial-material-grouped-native-AB-v1-20261011-control'),
    source=str(D),receipts=str(E))
REVIEW_TARGET = E/'INDEPENDENT_COMPLETE_NATIVE_AB_SOURCE_REVIEW.json'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
    'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
POLICY = 'FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,
    history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FUTURE = dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,
    actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,
    scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,
    AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,
    complete_context_aggregation_qualified=False)
WORKFLOW = Path('/private/tmp/Root_grouped_native_AB_workflow_v4_Source_7wklnsa1/full_native_grouped_AB_workflow.UNREADY.py')
WORKFLOW_SHA = 'cd1842ec55d6f5d78ae5cffa876d03706e1c5ecc6c2c9f534a86d41d2eee7a1e'
LAUNCHER = Path('/private/tmp/Root_grouped_native_AB_launcher_v3_Source_pm6ha7qa/full_native_grouped_AB_launcher.UNREADY.py')
LAUNCHER_SHA = '904181dd30fdb09dfaa11fbb9848e02099278ace6289b00972bde16d2d1564de'
LATEST_REVIEW = Path('/private/tmp/axmat_full_Native_AB_independent_prelaunch_reviewer_Source_nj11cw97/LATEST_WORKFLOW_V4_CLI_V3_SOURCE_REVIEW.txt')
LATEST_REVIEW_SHA = '771dc7f1f2343b0ad0208959386909f868d8cea99d2398201dc987aad0b3fa25'
BATCH_SHA = 'ef35a10a289b99b02cd9136dbcdeed8732c02fe07e495d0af16aec27444720b7'
CONTRACT_SHA = 'cac8532a9477824d7f68252196c74f86aaa4c06e12301836fa31976d0505f8cb'
ADAPTER_SHA = 'd18ce676d776b674429d0c3e976466f5ab417ef4439f16f47aadef6a7ce9f50d'
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
REQUIRED_CASES = ['positive-mini-libraries','preexisting-original-object',
    'preexisting-default-pp-object','preexisting-pp-source','case-basename-collision',
    'mixed-flags','mixed-cwd','mixed-component','unmet-dependency-preflight',
    'unmet-dependency-planner','source-pin-mutation','pp-default-original-collision',
    'closed-driver-missing-object','closed-driver-extra-object',
    'closed-driver-source-mutation','second-input-syntax-error']
PAYLOAD_ROLES = dict(native_Source_archive='COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz',
    native_Source_index='COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json',
    LIBMIX_observation='OBSERVATION_SOURCE/LIBMIX.observe.UNREADY.f',
    LIBDEN_observation='OBSERVATION_SOURCE/LIBDEN.observe.UNREADY.f',
    TONDRV_observation='OBSERVATION_SOURCE/TONDRV.context_observe.UNREADY.f',
    TONSPH_observation='OBSERVATION_SOURCE/TONSPH.observe.UNREADY.f',
    observer_module='OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90')
GUARD_SOURCES = {
    'run_real64_common_rank2_training.py':'f88ab14f9c54093af8dfc66e0585069af825997286d722fa4766c046acea66fa',
    'production_inputs.py':'92bf4e8955fda48e9547cc29afb7aad7cc262ba91ffbd536cb94df02d735346e',
    'production_runner.py':'f34915c9cf5c2392704817b201f97fbe11c12505b7b4870087693d4af8968d20',
    'qualify_refined_AAA_layered_full.py':'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6',
    'moment_order_complete_history_resource_trie_20261010.py':'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022',
}


def require(value,message):
    if type(value) is not bool or not value:raise ValueError(message)


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def read_json(raw):
    def pairs(items):
        out={}
        for key,value in items:
            require(key not in out,'no duplicate META key');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))


def pin(path,budget,positive_links=False):
    budget();path=Path(path);before=identity(path.lstat())
    require(path.is_absolute() and '..' not in path.parts
        and all(not p.is_symlink() for p in (path,*path.parents))
        and stat.S_ISREG(before[2]) and (before[3]>=1 if positive_links else before[3]==1),
        'ordinary complete nonalias file and explicitly preserved original link rule')
    digest=hashlib.sha256();count=0
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno()))==before,'true opened Source/META identity')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            count+=len(raw);digest.update(raw)
        require(identity(os.fstat(stream.fileno()))==before,'true complete EOF identity')
    require(identity(path.lstat())==before and count==before[4],'full EOF/path/size held')
    budget();return dict(path=str(path),sha256=digest.hexdigest(),size_bytes=count,identity=before)


def shape(p):
    require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'}
        and type(p['path']) is str and Path(p['path']).is_absolute()
        and type(p['sha256']) is str and len(p['sha256'])==64
        and all(c in '0123456789abcdef' for c in p['sha256'])
        and type(p['size_bytes']) is int and p['size_bytes']>=0
        and type(p['identity']) is list and len(p['identity'])==7
        and all(type(v) is int and v>=0 for v in p['identity'])
        and p['identity'][4]==p['size_bytes'],'exact integer full EOF SHA/size/seven ID pin')


def recheck(p,budget,positive_paths=()):
    shape(p);require(pin(p['path'],budget,p['path'] in positive_paths)==p,'whole actual pin held: '+p['path'])


def raw(p,budget,positive_paths=()):
    recheck(p,budget,positive_paths)
    with Path(p['path']).open('rb') as stream:
        require(identity(os.fstat(stream.fileno()))==p['identity'],'full-read FD identity')
        data=stream.read()
        require(identity(os.fstat(stream.fileno()))==p['identity'],'full-read EOF FD identity')
    require(len(data)==p['size_bytes'] and hashlib.sha256(data).hexdigest()==p['sha256'],
        'complete real bytes, never reconstructed output')
    recheck(p,budget,positive_paths);return data


def meta(p,budget,positive_paths=()):return read_json(raw(p,budget,positive_paths))


def fixed(path,sha,budget,size=None):
    p=pin(path,budget);require(p['sha256']==sha and (size is None or p['size_bytes']==size),'fixed complete original Source/META')
    return p


def tree(root,budget):
    files=[];directories={};root=Path(root)
    for path in (root,*sorted(root.rglob('*'))):
        budget();s=path.lstat();require(not stat.S_ISLNK(s.st_mode),'no D/E aliases')
        if stat.S_ISDIR(s.st_mode):directories[str(path)]=identity(s)
        else:files.append(pin(path,budget))
    return dict(files=files,directories=directories)


def static_value(source,name):
    nodes=[n for n in ast.parse(source).body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    require(len(nodes)==1,'one real Source literal declaration: '+name)
    value=nodes[0].value
    if isinstance(value,ast.Call):
        require(isinstance(value.func,ast.Name) and value.func.id=='dict'
            and not value.args and all(k.arg is not None for k in value.keywords),'only literal keyword dict')
        return {k.arg:ast.literal_eval(k.value) for k in value.keywords}
    return ast.literal_eval(value)


def write_new(path,data,budget):
    budget();path=Path(path)
    require(not os.path.lexists(path) and all(not p.is_symlink() for p in path.parents),'fresh exact metadata/Source destination')
    with path.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
    return pin(path,budget)


def write_meta(path,value,budget):
    return write_new(path,(json.dumps(value,indent=2,allow_nan=False)+'\n').encode(),budget)


def copy_source(origin,dest,budget):
    data=raw(origin,budget);result=write_new(dest,data,budget)
    require(result['sha256']==origin['sha256'] and result['size_bytes']==origin['size_bytes'],
        'complete Source copied with unchanged bytes and independent actual new pin')
    recheck(origin,budget);return result


def ready_source(origin,parent_dest,ready_dest,budget):
    source=raw(origin,budget);nodes=[n for n in ast.parse(source).body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='SOURCE_STATUS' for t in n.targets)]
    require(len(nodes)==1 and ast.literal_eval(nodes[0].value)=='UNREADY_SOURCE_ONLY',
        'one actual top-level UNREADY status assignment in frozen production Source')
    lines=source.splitlines(keepends=True);old=b"SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'"
    marker=("SOURCE_STATUS = '"+READY_STATUS+"'").encode();i=nodes[0].lineno-1
    require(lines[i].strip()==old and lines[i].count(old)==1,'exact one-line readiness assignment')
    lines[i]=lines[i].replace(old,marker,1);ready=b''.join(lines)
    require(ready.count(marker)==1 and ready.replace(marker,old,1)==source,
        'whole immutable READY inverse differs only in the actual status literal')
    ast.parse(ready)
    parent=write_new(parent_dest,source,budget);result=write_new(ready_dest,ready,budget)
    recheck(origin,budget)
    return parent,result,dict(original_UNREADY_Source_pin=origin,copied_UNREADY_Source_pin=parent,
        immutable_READY_Source_pin=result,actual_top_level_assignment_only=True,
        whole_inverse_bytes_equal_original=True,READY_is_not_runtime_or_scientific_qualification=True)


def main():
    started=time.monotonic()
    def budget():require(time.monotonic()-started<CAPS['whole_seconds'],'whole original1800 includes metadata, full EOF reads and final resource closure')
    cli=argparse.ArgumentParser()
    cli.add_argument('--Root-metadata-source-admission-only',required=True,action='store_true')
    cli.add_argument('--latest-independent-workflow-CLI-source-review',required=True)
    cli.add_argument('--latest-independent-workflow-CLI-source-review-sha256',required=True)
    args=cli.parse_args();budget()
    require(args.Root_metadata_source_admission_only and not sys.flags.optimize
        and not os.environ.get('PYTHONOPTIMIZE') and sys.gettrace() is None and sys.getprofile() is None
        and all(os.environ.get(k)=='1' for k in THREAD_KEYS)
        and Path(sys.executable).resolve()==PYTHON and platform.system()=='Darwin'
        and platform.machine()=='arm64','explicit Root metadata action under canonical original environment')
    require(not any(os.path.lexists(p) for p in NAMESPACES.values()),'all five new namespaces absent; no retry or replacement')
    self_pin=pin(Path(__file__).absolute(),budget)
    old_binding_pin=fixed(OLD_D/'Root_original_grouped16_tiny_controls_Source_binding.json',
        'd69653a7481dc9bf9b0b26666c859341d818682f7ad20c7cecbdc2004bee1724',budget,34882)
    old=meta(old_binding_pin,budget)
    # Exact old binding SHA is independently checked against the actual facts
    # below. An author must never manufacture a new old-input pin.
    facts_pin=fixed(OLD_H/'ACTUAL_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS.json',
        '8302377338391a6f186cd6d2b606fc5b5e481ec6bb61e9bd265e9fe6e65b38ca',budget,6695398)
    facts=meta(facts_pin,budget)
    require(facts['new_Source_binding_pin']==old_binding_pin and old['schema']=='ROOT_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_SOURCE_BINDING_V2'
        and old['original_caps']==facts['original_caps']==CAPS
        and all(type(v) is int for v in old['original_caps'].values())
        and old['source_only'] is True and old['Root_only_actual_execution'] is True
        and old['actual_execution'] is None and old['policy']==POLICY
        and old['old_controls_qualification_inherited'] is False,'actual frozen V3 tiny contract and typed original caps')
    positive_paths={p['path'] for p in old['tool_pins'].values()}|{old['actual_stdlib_subprocess_Source_pin']['path']}
    protected=[self_pin,old_binding_pin,facts_pin,*facts['complete_protected_input_pins'],
        old['actual_stdlib_subprocess_Source_pin'],*old['tool_pins'].values()]
    for p in protected:recheck(p,budget,positive_paths)
    require(tree(OLD_D,budget)==facts['complete_D_freeze'] and tree(OLD_E,budget)==facts['complete_E_freeze'],
        'whole original V3 D/E kept unchanged')
    qualified_D=Path(old['fresh_controls_Source_binding_pin']['path']).parent
    qualified_E=BASE/'actual_single_preappend_monitor_controls_approved_env_receipts_20261011'
    require(tree(qualified_D,budget)==facts['preserved_qualified_controls_D_freeze']
        and tree(qualified_E,budget)==facts['preserved_qualified_controls_E_freeze'],
        'same genuine actual ten-control Source/independent-receipts whole freezes held')
    review_pin=fixed(OLD_H/'SAVED_RESULT_REVIEW.txt','5109008302279e701a07c830068feca3776aa20ae8c1327909db740abad5c47f',budget,9637)
    saved_review=raw(review_pin,budget).decode('utf-8')
    require('PASS_FINITE_GROUPED_TINY_CONTROL_COMPOSITION_ONLY' in saved_review and 'blockers=[]' in saved_review,
        'actual complete independent saved-result review, finite controls only')
    prelaunch_pin=facts['independent_Source_prelaunch_review_pin'];recheck(prelaunch_pin,budget)
    report_pin=fixed(OLD_H/'REPORT.txt','7c04f5342142d35afbbd562f330c1d52fb6ff8a9ce85f4453810e279745c8fe9',budget,4190)
    capture_pin=fixed(OLD_C/'actual_Root_tool_terminal.json','a7c3d79d445ea057d51495d1e15cf740e8e14cc87ffdd3d1a3d0ac93e253920e',budget)
    capture=meta(capture_pin,budget);actual=capture['actual_final_tool_return']
    require(capture['schema']=='ROOT_GENUINE_GROUPED16_TINY_CONTROLS_TOOL_AND_COMPLETE_CAPTURE_V1'
        and capture['actual_terminal_closed'] is True and capture['complete_original_stdout_available'] is True
        and capture['captured_streams_reconstructed'] is False and capture['raw_output_truncation_preserved'] is False
        and capture['stdout_and_stderr_redirected_to_fresh_files_before_launch'] is True
        and capture['files_copied_only_after_actual_terminal_closed'] is True
        and type(actual['exit_code']) is int and actual['exit_code']==0 and actual['chunk_id']=='bf09e2'
        and actual['output']=='' and 'session_id' not in actual,'real original redirected CLOSED0 tool preserved unmodified')
    stdout_pin=capture['actual_stdout_file_pin'];stderr_pin=capture['actual_stderr_file_pin']
    redirect_pin=capture['actual_redirected_tool_receipt_pin']
    for p in (stdout_pin,stderr_pin,redirect_pin):recheck(p,budget)
    stdout=meta(stdout_pin,budget);redirect=meta(redirect_pin,budget)
    require(stdout['actual_facts_pin']==facts_pin and stderr_pin['size_bytes']==0
        and redirect['actual_final_tool_return']==actual and redirect['actual_terminal_closed'] is True
        and redirect['fresh_redirect_paths_checked_before_launch'] is True and redirect['shell_noclobber_enforced'] is True,
        'complete true stdout facts and original raw prelaunch redirect receipt coupled')
    close_pin=fixed(OLD_C/'Root_current_closeout.json','b573c0301c408b989b112c86109d6de8f8626dbc277a1a789c255f9711660ce2',budget)
    close=meta(close_pin,budget)
    require(close['all_recorded_PIDs_and_groups_currently_absent'] is True
        and close['actual_saved_facts_pin']==facts_pin and close['no_business_rerun'] is True
        and close['no_process_cleanup_performed'] is True,'existing real current-closeout observation only, no new PS claim')
    require(facts['schema']=='ACTUAL_ORIGINAL_GROUPED_DIRECT_DRIVER_TINY_CONTROLS_FACTS_V2'
        and facts['source_only'] is False
        and facts['direct_driver_batch_Source_pin']==old['direct_driver_batch_Source_pin']
        and facts['adapter_Source_pin']==old['adapter_Source_pin']
        and facts['tool_pins']==old['tool_pins']
        and facts['original_stdlib_Source_pin']==old['actual_stdlib_subprocess_Source_pin']
        and facts['original21_author_Source_contract']==old['original21_author_Source_contract']
        and facts['fresh_monitor_controls_RESULT_pin']==old['fresh_controls_saved_RESULT_pin']
        and facts['fresh_monitor_controls_independent_saved_review_pin']==old['fresh_controls_independent_saved_review_pin']
        and [r['case_id'] for r in facts['actual_all_sixteen_grouped_controls']]==REQUIRED_CASES
        and all(r['expected_outcome_observed'] is True for r in facts['actual_all_sixteen_grouped_controls'])
        and old['control_execution_order']==facts['actual_grouped_control_manifest']['order']==REQUIRED_CASES
        and old['planned_control_manifest']==facts['actual_grouped_control_manifest']
        and facts['actual_python_business_controller_used'] is False
        and [r['status'] for r in facts['actual_stage_records']]==['PASS']*5+['FAILED']*4
        and facts['actual_retry_count']==0 and facts['old_controls_qualification_inherited'] is False
        and len(facts['actual_owner_state']['owners'])==58 and facts['actual_owner_state']['unknown']==[]
        and facts['actual_monitor_evidence']['additional_recording_errors']==[]
        and facts['actual_monitor_evidence']['unpersisted_complete_events']==[]
        and facts['actual_saved_monitor_timing']['fatal_count']==0,'all sixteen actual controls and genuine retained failures')
    for key in ('full_Native_build_qualified','actual_AB_material_context_qualified','full_reference_qualified',
        'scientific_qualification_created','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','ABA_started','native_RSS_qualified'):
        require(facts[key] is False,'no expanded control qualification: '+key)
    journal_pin=facts['actual_saved_monitor_timing']['complete_journal_pin'];recheck(journal_pin,budget)
    workflow_pin=fixed(WORKFLOW,WORKFLOW_SHA,budget,38470);launcher_pin=fixed(LAUNCHER,LAUNCHER_SHA,budget,15795)
    require(old['probe_entry_Source_pin']['sha256']==CONTRACT_SHA
        and old['direct_driver_batch_Source_pin']['sha256']==BATCH_SHA
        and old['adapter_Source_pin']['sha256']==ADAPTER_SHA and old['support_Source_pin']['sha256']==SUPPORT_SHA,
        'same genuine tested cac/ef35 and unchanged d18/public support')
    require(args.latest_independent_workflow_CLI_source_review==str(LATEST_REVIEW)
        and args.latest_independent_workflow_CLI_source_review_sha256==LATEST_REVIEW_SHA,
        'explicit exact latest real independent Source review, not a synthetic replacement')
    static_review_pin=fixed(LATEST_REVIEW,LATEST_REVIEW_SHA,budget,6623)
    source_review=raw(static_review_pin,budget).decode('utf-8')
    require('PASS_SOURCE_ONLY_LATEST_WORKFLOW_V4_CLI_V3_INTERFACE_DELTA' in source_review
        and any(s in source_review for s in ('blockers=[]','Blockers: []','Blockers []'))
        and WORKFLOW_SHA in source_review and LAUNCHER_SHA in source_review,
        'actual latest independent V4/CLI V3 Source review exists; never inherit old Source review')
    protected.extend([review_pin,prelaunch_pin,report_pin,capture_pin,stdout_pin,stderr_pin,redirect_pin,close_pin,
        journal_pin,workflow_pin,launcher_pin,static_review_pin])
    author=old['original21_author_Source_contract'];require(type(author) is dict and len(author)==21,'all original21 Source roles')
    manifest=meta(author['qualified_source_manifest'],budget);members=manifest['members']
    require(len(members)==306 and manifest['member_count']==306 and manifest['source_only'] is True
        and len({r['relative_path'] for r in members})==306,'full original manifest306 unique members')
    indexed={r['relative_path']:r['fullpin'] for r in members}
    require(set(manifest['required_author_Source_roles'])==set(author),'all21 original role declarations preserved without omission')
    for role,relative in manifest['required_author_Source_roles'].items():
        require(role in author and (role=='qualified_source_manifest' or indexed[relative]==author[role]),
            'all21 exact original manifest role mappings')
    anchors={k:manifest[k] for k in ('parent_manifest_pin','current_revision_contract_pin','current_full_inverse_pin',
        'actual_author_report_pin','actual_author_Source_check_tool_return_pin')}
    protected.extend(anchors.values())
    for row in members:recheck(row['fullpin'],budget);protected.append(row['fullpin'])
    for p in author.values():recheck(p,budget);protected.append(p)
    seed=meta(author['original_material_seed_contract'],budget)
    require(seed['schema']=='ORIGINAL129_COMPLETE_MATERIAL_SEED_SOURCE_META_CONTRACT_V1'
        and seed['source_only'] is True and len(seed['original129_input_pins'])==129
        and len({p['path'] for p in seed['original129_input_pins']})==129
        and list(seed['states'])==['A','B'] and set(seed['libraries'])=={'DLIB_ACTUAL','DLIB8R1_370'},
        'original whole129, A/B original seeds and two unchanged physical libraries')
    original129=seed['original129_input_pins']
    for p in original129:recheck(p,budget,positive_paths);protected.append(p)
    recheck(seed['material_original_provenance_pin'],budget);protected.append(seed['material_original_provenance_pin'])
    adapter_raw=raw(old['adapter_Source_pin'],budget)
    require(static_value(adapter_raw,'FUTURE')==FUTURE,'original ten future fields unchanged')
    layout=static_value(adapter_raw,'SHARED_INPUT_LIBRARY_LAYOUT')
    require(layout['seed_destination_order']==['material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'],
        'original shared library exact seed role order')
    libraries={}
    for name,witness in seed['libraries'].items():
        # Genuine complete stream to EOF, bounded memory; no copied library,
        # virtual fullpin or use of generation SHA as an observed current pin.
        p=fixed(witness['path'],witness['generation_sha256'],budget)
        libraries[name]=p;protected.append(p)
    states={}
    for state in ('A','B'):
        rows=[]
        for name in layout['seed_destination_order']:
            p=libraries[name] if name in libraries else seed['states'][state][name]
            recheck(p,budget);protected.append(p);rows.append(dict(destination=name,input_pin=p))
        states[state]=dict(native_stage_inputs=rows,original_material_deck_pin=rows[0]['input_pin'])
    original_payload={role:indexed[relative] for role,relative in PAYLOAD_ROLES.items()}
    require(original_payload['native_Source_archive']==author['native_Source_archive']
        and original_payload['native_Source_index']==author['native_Source_index']
        and original_payload['observer_module']==author['observer_module'],'all seven original payload anchors')
    index=meta(author['native_Source_index'],budget)
    require(index['schema']=='COMPLETE_ORIGINAL_MATERIAL_NATIVE_COMPILE_SOURCE_INDEX_V1'
        and len(index['members'])==1365 and len({r['relative_path'] for r in index['members']})==1365,
        'complete original1365 native archive index, no reduced compile payload')
    # Only the unchanged genuine training disk guards may be imported. Candidate
    # runtime/contract/workflow/batch/launcher are parsed or copied, never loaded.
    guard_pins=[fixed(ROOT/'validation/axial_material'/name,sha,budget) for name,sha in GUARD_SOURCES.items()]
    protected.extend(guard_pins);sys.dont_write_bytecode=True
    sys.path.insert(0,str(ROOT/'validation/axial_material'))
    require('run_real64_common_rank2_training' not in sys.modules,'fresh original training guard import')
    from run_real64_common_rank2_training import TrainingResources
    for p in guard_pins:
        recheck(p,budget);name=Path(p['path']).stem
        require(name in sys.modules and Path(sys.modules[name].__file__).resolve()==Path(p['path']),
            'genuine imported disk guard Source path held')
    resources=TrainingResources(Path(NAMESPACES['host']),tuple(Path(NAMESPACES[k]) for k in ('output','control')))
    def disk_census(reserve):
        budget()
        for p in guard_pins:recheck(p,budget)
        q=resources.check();budget();seen=set();external=0
        for root in (D,E):
            if not os.path.lexists(root):continue
            for path in root.rglob('*'):
                budget();s=path.lstat();require(not stat.S_ISLNK(s.st_mode),'actual new external D/E has no aliases')
                if stat.S_ISDIR(s.st_mode):continue
                require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'ordinary independent external metadata')
                key=(s.st_dev,s.st_ino);require(key not in seen,'external D/E counted once');seen.add(key);external+=s.st_size
        joint=q['fresh_output']['artifact_bytes']+external
        history=q['complete_history']['artifact_bytes']+external;free=q['fresh_output']['disk_free_bytes']
        require(joint+reserve<CAPS['joint_archive_bytes'] and history+reserve<=CAPS['history_bytes']
            and free-reserve>=CAPS['free_floor_bytes'],'original joint/history/free caps including actual external D/E and reserved next write')
        for p in guard_pins:recheck(p,budget)
        return dict(complete_original_training_resource_observation=q,actual_new_external_D_E_bytes=external,
            actual_joint_HOCDE_bytes=joint,actual_history_plus_external_DE_bytes=history,
            actual_free_bytes=free,reserved_next_metadata_bytes=reserve,
            no_process_or_open_unlinked_census_claimed=True)
    reserve=16*2**20;before=disk_census(reserve)
    require(not any(os.path.lexists(p) for p in NAMESPACES.values()),'all new namespaces still absent before exclusive metadata writes')
    D.mkdir();E.mkdir();(D/'OBSERVATION_SOURCE').mkdir()
    new_payload={role:copy_source(p,D/PAYLOAD_ROLES[role],budget) for role,p in original_payload.items()}
    group_parent,group_ready,gproof=ready_source(old['direct_driver_batch_Source_pin'],D/'full_native_original_grouped_direct_driver_batch.UNREADY.py',D/'full_native_original_grouped_direct_driver_batch.READY.py',budget)
    work_parent,work_ready,wproof=ready_source(workflow_pin,D/'full_native_grouped_AB_workflow.UNREADY.py',D/'full_native_grouped_AB_workflow.READY.py',budget)
    host_parent,host_ready,hproof=ready_source(launcher_pin,D/'full_native_grouped_AB_launcher.UNREADY.py',D/'full_native_grouped_AB_launcher.READY.py',budget)
    creator_copy=copy_source(self_pin,D/'Root_metadata_Source_admission_writer.py',budget)
    inverse_pin=write_meta(D/'THREE_IMMUTABLE_READY_SOURCE_FULL_INVERSES.json',dict(schema='ROOT_THREE_IMMUTABLE_READY_SOURCE_INVERSES_V1',
        source_only=True,actual_runtime_status_monkeypatched=False,whole_Source_inverses=[gproof,wproof,hproof],
        candidate_modules_imported=False,Native_or_scientific_execution=False),budget)
    wrapper_pin=write_meta(D/'GENUINE_GROUPED16_bf09e2_CLOSED0_TYPED_TOOL_RETURN.json',dict(
        schema='ROOT_GENUINE_ORIGINAL_GROUPED16_SAVED_TYPED_CLOSED_TOOL_WRAPPER_V1',source_only=False,
        closed=True,observed_terminal=True,actual_terminal_chunk=actual['chunk_id'],terminal_tool_return=copy.deepcopy(actual),
        original_complete_capture_receipt_pin=capture_pin,original_raw_redirected_tool_receipt_pin=redirect_pin,
        original_complete_stdout_pin=stdout_pin,original_complete_stderr_pin=stderr_pin,
        copied_saved_terminal_only=True,new_business_execution=False,actual_streams_reconstructed=False),budget)
    gate_pin=write_meta(D/'ACTUAL_SIXTEEN_GROUPED_CONTROLS_SAVED_ADMISSION_GATE.json',dict(
        schema='ROOT_GROUPED_DIRECT_COMPILER_SAVED_CONTROLS_V1',source_only=False,
        all_required_controls_passed=True,blockers=[],original_caps=CAPS,
        tested_UNREADY_Source_pin=old['direct_driver_batch_Source_pin'],actual_entry_Source_pin=old['probe_entry_Source_pin'],
        required_case_ids=REQUIRED_CASES,full_Native_build_qualified=False,scientific_qualification_created=False,
        actual_facts_pin=facts_pin,actual_closed_zero_tool_return_pin=wrapper_pin,actual_current_closeout_pin=close_pin,
        independent_saved_result_review_pin=review_pin,actual_complete_stdout_pin=stdout_pin,
        actual_complete_stderr_pin=stderr_pin,actual_capture_tool_receipt_pin=capture_pin,
        actual_controls_Source_binding_pin=old_binding_pin,actual_controls_Source_review_pin=prelaunch_pin,
        actual_saved_REPORT_pin=report_pin,old_monitors_not_inherited_as_new_execution=True),budget)
    b={key:copy.deepcopy(old[key]) for key in ('source_only','Root_only_actual_execution','policy','original_caps',
        'actual_execution','old_controls_qualification_inherited','direct_driver_batch_Source_pin','support_Source_pin',
        'adapter_Source_pin','fresh_controls_Source_binding_pin','original_N9_controls_Source_binding_pin',
        'original21_author_Source_contract','owner_helper_Source_pin','actual_stdlib_subprocess_Source_pin','tool_pins',
        'fresh_controls_saved_RESULT_pin','fresh_controls_independent_saved_review_pin','genuine_guard_Source_pins')}
    b.update(FUTURE)
    b.update(schema='ROOT_GROUPED_COMPLETE_NATIVE_AB_SOURCE_BINDING_V1',
        execution_scope='ROOT_COMPLETE_GROUPED_NATIVE_BUILD_AND_A_THEN_B_CONTEXT_EVIDENCE_ONLY',namespaces=NAMESPACES,
        full_host_Source_pin=host_ready,full_host_UNREADY_Source_pin=host_parent,
        full_workflow_Source_pin=work_ready,full_workflow_UNREADY_Source_pin=work_parent,
        contract_entry_Source_pin=old['probe_entry_Source_pin'],grouped_READY_Source_pin=group_ready,
        grouped_tested_UNREADY_Source_pin=old['direct_driver_batch_Source_pin'],
        grouped_UNREADY_local_parent_copy_Source_pin=group_parent,actual_grouped_controls_gate_pin=gate_pin,
        grouped_controls_required_case_ids=REQUIRED_CASES,original129_input_pins=original129,
        original_native_payload_pins=original_payload,native_payload_pins=new_payload,state_order=['A','B'],
        build_stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],SPOT_AXMAT_OBSERVATION='ADMITTED_SOURCE_ONLY',
        material_input_layout=layout,states=states,actual_Root_current_library_fullpins=libraries,
        actual_original16_control_Source_binding_pin=old_binding_pin,
        actual_original16_control_Source_review_pin=prelaunch_pin,
        actual_latest_workflow_CLI_static_Source_review_pin=static_review_pin,
        original_author_manifest_anchors=anchors,original_author_manifest_complete_members=members,
        original_author_manifest_directory_declarations=manifest['directories'],
        original_material_provenance_pin=seed['material_original_provenance_pin'],
        immutable_READY_full_inverse_proof_pin=inverse_pin,Root_metadata_creator_original_Source_pin=self_pin,
        Root_metadata_creator_copied_Source_pin=creator_copy,
        original_UNREADY_workflow_Source_pin=workflow_pin,original_UNREADY_launcher_Source_pin=launcher_pin,
        independent_full_prelaunch_review_required_path=str(REVIEW_TARGET),
        actual_independent_full_prelaunch_review=None,full_Native_build_qualified=False,
        actual_AB_material_context_qualified=False,full_reference_qualified=False,scientific_qualification_created=False,
        ABA_started=False,native_RSS_qualified=False)
    binding_pin=write_meta(D/'Root_complete_grouped_native_AB_Source_binding.json',b,budget)
    inventory_pin=write_meta(D/'COMPLETE_NEW_SOURCE_PRE_RECEIPT_FILE_INVENTORY.json',dict(
        schema='ROOT_COMPLETE_GROUPED_NATIVE_AB_SOURCE_PRE_RECEIPT_INVENTORY_V1',source_only=True,
        new_Source_binding_pin=binding_pin,actual_files=[pin(p,budget) for p in sorted(D.rglob('*')) if p.is_file()],
        original21_roles_preserved=True,original129_complete_pins_preserved=True,
        actual_independent_full_prelaunch_review=None,expected_review_path=str(REVIEW_TARGET)),budget)
    require(tree(OLD_D,budget)==facts['complete_D_freeze'] and tree(OLD_E,budget)==facts['complete_E_freeze'],
        'all prior frozen D/E unchanged after new Source writes')
    require(tree(qualified_D,budget)==facts['preserved_qualified_controls_D_freeze']
        and tree(qualified_E,budget)==facts['preserved_qualified_controls_E_freeze'],
        'all original actual ten-control D/E still held after new Source writes')
    # Deduplicate only equal declarations; all complete bytes are re-read. The
    # two genuine large libraries are streamed, never retained whole in RAM.
    dedup={}
    for p in protected:
        require(p['path'] not in dedup or dedup[p['path']]==p,'all duplicate input declarations equal');dedup[p['path']]=p
    for p in dedup.values():recheck(p,budget,positive_paths)
    require(not list(E.iterdir()) and not any(os.path.lexists(NAMESPACES[k]) for k in ('host','output','control')),
        'E genuinely empty and HOC still absent; independent review and all business remain pending')
    before_receipt=disk_census(262144)
    receipt_pin=write_meta(D/'Root_metadata_only_Source_admission_resource_receipt.json',dict(
        schema='ROOT_COMPLETE_GROUPED_NATIVE_AB_METADATA_SOURCE_ADMISSION_RESOURCE_RECEIPT_V1',
        status='ACTUAL_METADATA_ONLY_SOURCE_BINDING_CREATED_INDEPENDENT_FULL_PRELAUNCH_REVIEW_PENDING',
        source_only=True,new_Source_binding_pin=binding_pin,original_caps=CAPS,
        actual_original16_gate_pin=gate_pin,actual_TYPED_original_CLOSED0_wrapper_pin=wrapper_pin,
        actual_complete_new_Source_pre_receipt_inventory_pin=inventory_pin,
        original_training_guard_Source_pins=guard_pins,resources_before_new_D_E_writes=before,
        resources_after_Source_documents_before_own_receipt=before_receipt,
        actual_candidate_module_imported=False,actual_training_disk_guard_imported=True,
        actual_Native_or_material_or_scientific_execution=False,actual_business_rerun=False,
        actual_new_OS_PS_lsof_sampling=False,actual_new_HOC_created=False,actual_E_empty=True,
        actual_independent_full_prelaunch_review_created=False,expected_review_path=str(REVIEW_TARGET),
        metadata_receipt_future_tool_return_reserved_bytes=65536,scientific_qualification_created=False),budget)
    after=disk_census(65536)
    for p in (self_pin,binding_pin,gate_pin,wrapper_pin,inverse_pin,inventory_pin,receipt_pin,
        group_parent,group_ready,work_parent,work_ready,host_parent,host_ready,*guard_pins):recheck(p,budget)
    require(not list(E.iterdir()) and not any(os.path.lexists(NAMESPACES[k]) for k in ('host','output','control')),
        'final complete Source preparation never creates review or HOC')
    budget()
    print(json.dumps(dict(status='ROOT_METADATA_ONLY_COMPLETE_SOURCE_BINDING_CREATED_REQUIRES_INDEPENDENT_FULL_PRELAUNCH_REVIEW',
        new_Source_binding_pin=binding_pin,new_Source_directory=str(D),new_empty_receipts_directory=str(E),
        expected_independent_full_prelaunch_review_path=str(REVIEW_TARGET),actual_complete_D_freeze=tree(D,budget),
        actual_empty_E_freeze=tree(E,budget),actual_post_own_append_original_disk_resources=after,
        Root_metadata_resource_receipt_pin=receipt_pin,actual_gate_pin=gate_pin,actual_TYPED_tool_wrapper_pin=wrapper_pin,
        actual_whole_seconds=time.monotonic()-started,actual_candidate_import=False,
        actual_Native_or_material_or_scientific_execution=False,actual_independent_full_review=None,
        actual_HOC_created=False,original_caps=CAPS,**FUTURE),allow_nan=False),flush=True)
    budget()


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Current-case full raw/context evidence, using intact original implementations.

This new entry does not change or invoke any old UNREADY main. It accepts an
explicit full-file request and a separately frozen complete Source package.
Extraction/reconstruction are evidence-only: complete evidence exits 2, and
actual malformed/incomplete execution exits 1. Neither code means physics PASS.
Every old, intermediate and final observation remains present. No SPH factor,
MASK, old MACROLIB, six missing moments or reaction multiplicity is invented.
"""
import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import resource
import stat
import sys
import time

BASE=Path(__file__).absolute().parent
COMMON=BASE.parent/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/guarded_warm_A_common.py'
_cs=importlib.util.spec_from_file_location('current_evidence_explicit_mount',COMMON)
c=importlib.util.module_from_spec(_cs);_cs.loader.exec_module(c)
COMPILER_EXACT_ROLE_PIN={'path': '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', 'sha256': '0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492', 'size_bytes': 2648040, 'identity': [16777229, 1171728, 33133, 2, 2648040, 1754637485000000000, 1778162641926218060]}
CASE_SHA='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
  joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,
  threads=1,children_at_once=1,retries=0)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,
  historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,
  TRANC_semantics_qualified=False,physical_neutron_balance_qualified=False,
  coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,
  AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False)


def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)


def strict(raw):
    def pairs(items):
        value={}
        for key,item in items:
            require(key not in value,'duplicate metadata key '+key);value[key]=item
        return value
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:
      (_ for _ in ()).throw(ValueError('nonfinite metadata '+x)))


def identity(s):
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path,budget):
    path=Path(path)
    require(path.is_absolute()and'..'not in path.parts,'literal absolute file path')
    require(not any(p.is_symlink()for p in(path,*path.parents)),'file and ancestor aliases forbidden')
    before=path.lstat();require(stat.S_ISREG(before.st_mode)and(before.st_nlink==1 or(str(path)==COMPILER_EXACT_ROLE_PIN['path']and identity(before)==COMPILER_EXACT_ROLE_PIN['identity'])),
      'regular single-link file or exact immutable compiler role')
    h=hashlib.sha256();size=0
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==identity(before),'opened full7ID')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            h.update(raw);size+=len(raw)
        require(identity(os.fstat(stream.fileno()))==identity(before),'fullEOF descriptor identity')
    require(size==before.st_size and identity(path.lstat())==identity(before),'fullEOF path identity')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=size,identity=identity(before))


def check(expected,budget):
    require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact four-field full pin')
    require(type(expected['path'])is str and type(expected['sha256'])is str and
      re.fullmatch('[0-9a-f]{64}',expected['sha256'])is not None and type(expected['size_bytes'])is int and
      expected['size_bytes']>=0 and type(expected['identity'])is list and len(expected['identity'])==7 and
      all(type(n)is int and n>=0 for n in expected['identity'])and
      (expected['identity'][3]==1 or expected==COMPILER_EXACT_ROLE_PIN)and expected['identity'][4]==expected['size_bytes'],'strict typed SHA/size/7ID and exact immutable compiler role')
    require(pin(expected['path'],budget)==expected,'fullEOF SHA/7ID differs '+expected['path'])
    return expected


def read(expected,budget):
    check(expected,budget);value,actual=c.read_bound_json_current(expected['path'],expected);require(actual==expected,'exact current metadata fullpin');check(expected,budget);return value


def write(path,value):
    with Path(path).open('x')as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())


class Budget:
    def __init__(self,roots):
        self.start=time.monotonic();self.last=0.0
        require(type(roots)is list and len(roots)>=5 and len(set(roots))==len(roots)and
          all(type(s)is str and Path(s).is_absolute()for s in roots),'all original five plus previous-stage evidence namespaces')
        self.roots=[Path(s)for s in roots]
        require(not any(a.is_relative_to(b)for a in self.roots for b in self.roots if a!=b),'disjoint evidence namespaces')
    def check(self):
        now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform!='darwin':peak*=1024
        require(now-self.start<600 and peak<512*2**20,'unchanged child stage600/SELF512')
        if now-self.last<0.25:return
        self.last=now;total=0
        for root in self.roots:
            if not root.exists():continue
            for p in root.rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no evidence namespace alias')
                if stat.S_ISREG(s.st_mode):total+=s.st_size
        unlinked={}
        for fd in os.listdir('/dev/fd'):
            try:s=os.fstat(int(fd))
            except(ValueError,OSError):continue
            if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
        require(total+sum(unlinked.values())<2*2**30,'unchanged joint fresh2GiB including SQLite/open-unlinked')


def module(name,filename,source_table,budget):
    path=BASE/filename;require(str(path)in source_table,'complete executing dependency pin')
    check(source_table[str(path)],budget)
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    check(source_table[str(path)],budget);return value


def admit_owning_stage(report_pin,label,command,budget):
    """Exact real successful producer stage, not a copied status label."""
    value=read(report_pin,budget)
    historical_terminal=(report_pin,value['schema'])in (({'path': '/Users/wen/spot/validation/artifacts/axial-material-new-REAL64-native-warm-A-20261012-v3/Root_actual_single_plane_warm_A_summary.json', 'sha256': '9823afc6fcab9da82ee11b2c2a3478d82be1fc081012c66cfec090c27db8d262', 'size_bytes': 3526183, 'identity': [16777229, 49775045, 33188, 1, 3526183, 1791743369388144123, 1791743369388144123]}, 'ACTUAL_CURRENT_SINGLE_PLANE_WARM_A_NATIVE_PRODUCER_ROOT_V1'), ({'path': '/Users/wen/spot/validation/artifacts/axial-material-new-REAL64-native-warm-A2-20261012-v1/Root_actual_single_plane_warm_A2_summary.json', 'sha256': 'f1f6fff5e23279545dddf18753f461c30f4175d13c1942fddf328f15b30bd82a', 'size_bytes': 5290034, 'identity': [16777229, 49787488, 33188, 1, 5290034, 1791751712212451946, 1791751712212451946]}, 'ACTUAL_CURRENT_SINGLE_PLANE_WARM_A2_NATIVE_PRODUCER_ROOT_V1'), ({'path': '/Users/wen/spot/validation/artifacts/axial-material-new-REAL64-native-warm-A3-20261012-v1/Root_actual_single_plane_warm_A3_summary.json', 'sha256': '2f9003f4730d0a40b988bbf3e08fe66a6a494aedc5c546a3ab6a8ae2dbf0ae1b', 'size_bytes': 5294296, 'identity': [16777229, 49788718, 33188, 1, 5294296, 1791751957538262051, 1791751957538262051]}, 'ACTUAL_CURRENT_SINGLE_PLANE_WARM_A3_NATIVE_PRODUCER_ROOT_V1'))
    if historical_terminal:
        require('after_check_error'not in value,'exact historical producer terminal field absence, never invented None')
    else:
        require(value['after_check_error']is None,'actual producer host after-check terminal')
    require(value['failure']is None,'actual producer host terminal')
    matches=[r for r in value['records']if r['label']==label]
    require(len(matches)==1 and matches[0]['status']=='PASS'and matches[0]['command']==command,'exact actual producer command')
    record=matches[0];root=Path(report_pin['path']).parent
    wanted=root/(label+'.watchdog.json');actual=pin(wanted,budget)
    rows=[p for p in value['actual_watchdog_checks']if p['path']==str(wanted)]
    require(len(rows)==1 and rows[0]['sha256']==actual['sha256'],'actual watchdog whole-file authority')
    watch=strict(wanted.read_bytes())
    require(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and
      watch['command']==command and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and
      type(watch['rss_cap_mib'])is int and watch['rss_cap_mib']==512 and
      0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and
      0<=watch['sampled_peak_rss_mib']<512,'real producer watchdog/caps/exit0')
    require(type(value['SELF_peak_bytes'])is int and value['SELF_peak_bytes']<512*2**20 and
      0<value['wall_seconds']<1800,'owning original SELF/whole limits')
    log=root/(label+'.log');require(pin(log,budget)['sha256']==record['log_sha256'],'actual complete producer log')
    return value


def source_admission(request,budget):
    sf=read(request['complete_source_freeze_pin'],budget)
    require(sf['schema']=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and
      sf['candidate_executed']is False,'separate complete current evidence Source freeze')
    table={}
    for p in sf['complete_source_file_pins']:
        check(p,budget);require(p['path']not in table,'complete Source path unique');table[p['path']]=p
    require(str(Path(__file__).absolute())in table,'complete own executing Source')
    require(request['current_case_spec_pin']['sha256']==CASE_SHA,'current fbe336 case, not old ac3e')
    case=read(request['current_case_spec_pin'],budget)
    require(case['basis']['requested_rank']==1 and case['cases']['AAA']==['A','A','A']and
      case['production']['groups']==370 and case['production']['fission_components']==32 and
      case['geometry']['physical_z_edges_cm']==[0,50,100,150],'same formal rank1/370/32/H150/AAA authority')
    require(request['original_caps']==CAPS and all(type(v)is int for v in request['original_caps'].values()),'original strict caps')
    fixed=request['complete_input_pins'];table_inputs={}
    for p in fixed:
        check(p,budget)
        require(p['path']not in table_inputs,'all current inputs unique');table_inputs[p['path']]=p
    for p in(request['current_case_spec_pin'],request['complete_source_freeze_pin']):
        require(table_inputs.get(p['path'])==p,'actual request authority in complete fixed inputs')
    return table,fixed


def extract(request,output,budget,source_table):
    native=module('current_full_native_snapshot_extractor','complete_observed_old_post_final_XSM_extractor.UNREADY.py',source_table,budget.check)
    contexts=module('current_full_actual_context_extractor','extract_actual_complete_context_with_SPH_decisions.UNREADY.py',source_table,budget.check)
    manifest_pin=request['actual_observation_manifest_pin'];manifest=read(manifest_pin,budget.check)
    require(manifest['schema']=='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1'and
      manifest['current_case_spec_pin']==request['current_case_spec_pin']and manifest['state_order']==['A']and
      manifest['observation_scope']=='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',
      'actual current complete observation manifest')
    states={};context_states={};all_files=[]
    for state in manifest['state_order']:
        s=manifest['states'][state]
        admit_owning_stage(s['actual_owning_report_pin'],s['actual_stage_label'],s['actual_command'],budget.check)
        for p in s['physical_input_pins']+s['complete_observed_file_pins']:
            check(p,budget.check);all_files.append(p)
        directory=Path(s['actual_cwd'])
        eventpins=s['complete_context_pins'];expectedfiles={p['path']for p in s['complete_observed_file_pins']}
        actualfiles={str(p)for p in directory.iterdir()if p.name.startswith('axobs-')}
        require(actualfiles==expectedfiles,'full observer directory must match manifest, no dropped extra event/snapshot')
        require(eventpins and len({p['path']for p in eventpins})==len(eventpins),'all actual contexts unique')
        folder=output/state;folder.mkdir();previous=0;events=[];snapshots=[]
        with(folder/'all_context_words.jsonl').open('x')as words:
            for p in eventpins:
                require(p in s['complete_observed_file_pins'],'each actual context protected')
                event=contexts.extract_event(p,words,budget.check)
                require(event['event']==previous+1 and Path(p['path']).name=='axobs-'+str(event['event']).zfill(6)+'.context.bin',
                  'exact consecutive unrenumbered original event order')
                previous=event['event'];events.append(event)
        require(events[-1]['label']=='TONDRV_FINAL_AFTER_SHIBA','complete actual TONDRV end')
        bypath={p['path']:p for p in s['complete_observed_file_pins']}
        allowed={p['path']for p in eventpins}
        macro_present=False
        roles={'LIBMIX_BEFORE':'oldmacro-pre-LIBMIX','LIBDEN_OLD_CONTEXT':'oldmacro-LIBDEN',
               'LIBMIX_AFTER':'postmacro-LIBMIX','TONDRV_FINAL_AFTER_SHIBA':'final-complete-micro'}
        for event in events:
            if event['label']=='LIBMIX_BEFORE':
                d=event['dimensions'];macro_present=d['MACRO_LENGTH']==-1 and d['MACRO_KIND']==0
                require(macro_present or d['MACRO_LENGTH']==0,'actual absence branch must be explicit')
            role=roles.get(event['label'])
            if role is None or(role in('oldmacro-pre-LIBMIX','oldmacro-LIBDEN')and not macro_present):continue
            name='axobs-'+str(event['event']).zfill(6)+'-'+role+'.xsm';path=str(directory/name)
            require(path in bypath,'complete actual snapshot missing '+name);allowed.add(path)
            item=dict(event=event['event'],role=role,root_prefix=[]if role=='final-complete-micro'else['MACROLIB'],input_pin=bypath[path])
            out=folder/(str(event['event']).zfill(6)+'_'+role);out.mkdir()
            rows=native.DiskRecords(out/'complete_native_original_path_index.sqlite')
            try:
                with Path(path).open('rb')as stream,(out/'complete_native_physical_directory_slots.jsonl').open('x')as physical,\
                  (out/'complete_native_original_value_bytes.bin').open('xb')as pool:
                    require(identity(os.fstat(stream.fileno()))==item['input_pin']['identity'],'actual opened snapshot full7ID')
                    tree=native.XSM(native.ReadOnlyFileBytes(stream),physical,pool,budget,rows)
                    tree.walk_table(tree.root,tuple(item['root_prefix']),());rows.checkpoint()
                    with(out/'complete_native_logical_record_inventory.jsonl').open('x')as inventory:
                        for row in rows.iter_rows():budget.check();native.line_json(inventory,row)
                    with(out/'complete_native_xsmnxt_export_record_order.jsonl').open('x')as api:
                        for row in rows.iter_rows(api=True):budget.check();native.line_json(api,row)
                    result=dict(state=state,**item,complete_records=len(rows),complete_directories=tree.directory_count,
                      complete_extents=tree.extent_count,all_original_types_counts_words_and_physical_API_orders_saved=True,
                      ASCII_used_or_invented=False,original_RAM_bits_qualified=False,new_qualification_sha256=None)
                    require(identity(os.fstat(stream.fileno()))==item['input_pin']['identity'],'snapshot full read identity')
            finally:rows.close()
            check(item['input_pin'],budget.check)
            result['paired_SQLite_pin']=pin(out/'complete_native_original_path_index.sqlite',budget.check)
            result['paired_original_pool_pin']=pin(out/'complete_native_original_value_bytes.bin',budget.check)
            result['all_output_file_pins']=[pin(p,budget.check)for p in sorted(out.rglob('*'))if p.is_file()]
            snapshots.append(result)
        require(allowed==expectedfiles,'every observed file assigned its original role, never filtered')
        states[state]=snapshots;context_states[state]=events
    report=dict(schema='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1',
      status='ACTUAL_CURRENT_COMPLETE_CONTEXT_AND_RAW_SNAPSHOT_EVIDENCE_ONLY_EXIT2',
      current_case_spec_pin=request['current_case_spec_pin'],actual_observation_manifest_pin=manifest_pin,
      actual_child_PID=os.getpid(),actual_parent_PID=os.getppid(),states=states,context_states=context_states,
      state_order=['A'],observation_scope='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',
      all_complete_state_scope_retained=True,all_handles_closed_between_snapshots=True,
      all_observed_native_tree_words_and_orders_preserved=True,original_caps=CAPS,
      complete_actual_observation_input_pins=all_files,complete_aggregation_qualified=False,
      complete_final_construction_qualified=False,new_qualification_sha256=None,**FALSE)
    path=output/'ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_REPORT.json';write(path,report)
    return path


def aggregate(request,output,budget,source_table):
    engine=module('current_original_complete_aggregation','complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',source_table,budget.check)
    adapter=module('current_original_saved_native_adapter','saved_native_data_access_adapter.UNREADY.py',source_table,budget.check)
    require(engine.ORIGINAL_CAPS==adapter.ORIGINAL_CAPS==CAPS,'intact original complete aggregation caps')
    binding=request['aggregation_binding']
    require(binding['state_order']==['A']and set(binding['states'])=={'A'}and
      set(binding['actual_context_states'])=={'A'}and binding['Source_route']==dict(ITSTMP=0,historical_call_proved=False),
      'same complete A-only nonperturbation Source route; no claimed B history')
    # The actual extraction coverage contract is a separate Root-reviewed file.
    # Its independent review is neither created nor replaced by this wrapper.
    for state in binding['state_order']:
        a=binding['actual_context_states'][state]
        review=read(request['actual_extraction_independent_review_pin'],budget.check)
        coverage=read(a['actual_extraction_coverage_contract_pin'],budget.check)
        require(review['actual_extraction_report_pin']==a['actual_extraction_report_pin']and
          review['actual_observation_manifest_pin']==a['actual_observation_manifest_pin']and
          review['complete_context_pins']==a['complete_context_pins']and
          review['all_snapshot_pairs']==a['all_snapshot_pairs']and
          coverage['independent_actual_review_pin']==request['actual_extraction_independent_review_pin']and
          review['all_original_snapshot_and_context_pins_verified']is True,
          'separate actual complete saved extraction review')
    states=[];error=None
    try:
        for state in binding['state_order']:
            states.append(engine.context_state_check(adapter,binding,state,output,budget.check))
    except BaseException as e:error=repr(e)
    report=dict(schema='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1',
      status='ACTUAL_CURRENT_COMPLETE_ORIGINAL_MATH_CONSTRUCTION_EVIDENCE_ONLY_EXIT2'if error is None else'ACTUAL_CURRENT_CONSTRUCTION_FAILED',
      current_case_spec_pin=request['current_case_spec_pin'],original_caps=CAPS,states=states,error=error,
      complete_source_freeze_pin=request['complete_source_freeze_pin'],
      actual_extraction_independent_review_pin=request['actual_extraction_independent_review_pin'],
      state_order=['A'],observation_scope='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',
      all_complete_state_scope_retained=len(states)==1,complete_final_construction_qualified=False,
      new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,**FALSE)
    path=output/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json';write(path,report)
    require(error is None,'complete construction execution failed '+str(error))
    return path


def compare_raw_macro(request,output,budget,source_table):
    """Every macro path/type/count/word, using original order and raw bytes.

    Observer final micro has MACROLIB at its root. Each real native archive has
    a MICROLIB2 list item; only that exact item is selected from the archive,
    while the entire original archive remains externally pinned.
    """
    native=module('current_raw_macro_full_walker','complete_observed_old_post_final_XSM_extractor.UNREADY.py',source_table,budget.check)
    adapter=module('current_raw_macro_saved_adapter','saved_native_data_access_adapter.UNREADY.py',source_table,budget.check)
    pair=request['observed_final_A_pair'];check(pair['sqlite_pin'],budget.check);check(pair['native_pool_pin'],budget.check)
    temp=output/'sqlite_temp';temp.mkdir()
    saved=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget.check)
    reports=[]
    try:
        producers=request['actual_native_producers']
        require(len(producers)==3 and[ p['plane']for p in producers]==[1,2,3], 'three genuinely independent plane archives')
        for producer in producers:
            expected=producer['archive_pin'];check(expected,budget.check)
            admit_owning_stage(producer['actual_report_pin'],producer['actual_solve_label'],producer['actual_solve_command'],budget.check)
            folder=output/('A'+str(producer['plane']));folder.mkdir()
            rows=native.DiskRecords(folder/'original_archive_index.sqlite')
            try:
                with Path(expected['path']).open('rb')as stream,(folder/'physical.jsonl').open('x')as physical,\
                  (folder/'original_words.bin').open('xb')as pool:
                    tree=native.XSM(native.ReadOnlyFileBytes(stream),physical,pool,budget,rows)
                    # Full archive walk preserves every unrelated container too.
                    tree.walk();pool.flush()
                    handle=rows.get(('MICROLIB2',1))
                    require(handle is not None and handle['kind']==0,'real archive MICROLIB2 list1 directory')
                    rows.checkpoint();rawpool=adapter.SavedNativeInput(pin(folder/'original_archive_index.sqlite',budget.check),
                        pin(folder/'original_words.bin',budget.check),temp,budget.check)
                    try:
                        def under(source,prefix):
                            for value in source.iter_all():
                                if tuple(value['record']['path'][:len(prefix)])==prefix:yield value
                        left=under(saved,('MACROLIB',));right=under(rawpool,('MICROLIB2',1,'MACROLIB'))
                        count=words=mismatches=0
                        with(folder/'complete_macro_comparison.jsonl').open('x')as detail:
                            for a,b in itertools.zip_longest(left,right):
                                budget.check();ar=None if a is None else a['record'];br=None if b is None else b['record']
                                meta=ar is not None and br is not None and ar['path']==['MACROLIB']+br['path'][3:]and \
                                  ar['path_types']==['str']+br['path_types'][3:]and \
                                  all(ar[k]==br[k]for k in('kind','declared_count','original_word_count'))
                                actualwords=0;wordmismatch=0
                                lhs=()if ar is None else saved.iter_raw(ar);rhs=()if br is None else rawpool.iter_raw(br)
                                for aa,bb in itertools.zip_longest(lhs,rhs,fillvalue=b''):
                                    actualwords+=max(len(aa),len(bb))//4
                                    if aa!=bb:
                                        wordmismatch+=sum(aa[i:i+4]!=bb[i:i+4]for i in range(0,max(len(aa),len(bb)),4))
                                count+=1;words+=actualwords;mismatches+=wordmismatch+int(not meta)
                                native.line_json(detail,dict(observation_record=ar,archive_record=br,
                                  original_words=actualwords,metadata_equal=meta,raw_word_mismatches=wordmismatch,
                                  all_available_original_payloads_fully_read=True))
                    finally:rawpool.close()
            finally:rows.close()
            check(expected,budget.check)
            reports.append(dict(plane=producer['plane'],archive_pin=expected,compared_all_macro_records=count,
              compared_original_payload_words=words,raw_word_mismatches=mismatches,
              full_original_scope_retained=True,all_output_pins=[pin(p,budget.check)for p in sorted(folder.rglob('*'))if p.is_file()]))
    finally:saved.close()
    report=dict(schema='ACTUAL_CURRENT_OBSERVED_A_TO_THREE_NATIVE_RAW_MACRO_COMPARISON_V1',
      current_case_spec_pin=request['current_case_spec_pin'],observed_final_A_pair=pair,comparisons=reports,
      whole_archive_producer_seals_not_relabelled=True,all_raw_word_mismatches=sum(r['raw_word_mismatches']for r in reports),**FALSE)
    path=output/'ACTUAL_THREE_CURRENT_RAW_MACRO_COMPARISONS.json';write(path,report);return path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('operation',choices=['extract','aggregate','compare-three'])
    parser.add_argument('--request-pin',required=True);parser.add_argument('--output-dir',required=True)
    parser.add_argument('--expected-parent-pid',required=True,type=int);args=parser.parse_args()
    require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None,
      'actual owning parent, unprofiled unoptimized child')
    require(all(os.environ.get(k)=='1'for k in THREADS),'original one-thread environment')
    expected=strict(args.request_pin);request=read(expected,lambda:None)
    require(request['schema']=='CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'and
      request['operation']==args.operation,'complete current explicit operation request')
    output=Path(args.output_dir)
    require(output.is_absolute()and str(output)==request['output_directory']and not os.path.lexists(output),'fresh exact output zero retry')
    budget=Budget(request['joint_archive_roots']);require(output in budget.roots,'output counted in fresh joint evidence')
    source_table,fixed=source_admission(request,budget.check);output.mkdir()
    operation={'extract':extract,'aggregate':aggregate,'compare-three':compare_raw_macro}[args.operation]
    report=operation(request,output,budget,source_table)
    for p in fixed:check(p,budget.check)
    for p in source_table.values():check(p,budget.check)
    check(expected,budget.check);budget.check()
    print(json.dumps(dict(status='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2',report=pin(report,budget.check),**FALSE),allow_nan=False),flush=True)
    raise SystemExit(2)


if __name__=='__main__':main()

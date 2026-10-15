#!/usr/bin/env python3
"""Actual three-plane operator, GLOBAL, projection and online BOOT under old limits.

Requires external full pins for three actual independent producer reports, the
actual new70 build, old current17, Fortran freeze and this complete Host freeze.
All large data objects stay XSM. Only owned, proved obsolete temporary copies may
be unlinked after closed child/watchdog and full independent whole-tree readback.
No implicit producer, rank default, retry, material change or physics certificate.
"""
import argparse
import importlib.util
import json
import os
import stat
from pathlib import Path
import shutil
import time
import actual_inputs_and_readback as data

R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'
spec=importlib.util.spec_from_file_location('pipeline_original_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
HERE=Path(__file__).resolve().parent
OUT=c.ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'
WORK=OUT/'AAA'
MI=2**20
ROOT_NAMES={'AX':'ax_current.xsm','AXTRACK':'axial_track.xsm','AXSYSTEM':'initial_system.xsm',
            'AXMACRO':'axial_macro.xsm','ARCHIVE':'initial_pack.xsm','RCON':'global_rcon.xsm'}
PREFIX='''XSM_FILE MACRO :: FILE './axial_macro.xsm' ;
XSM_FILE AXTRACK :: FILE './axial_track.xsm' ;
XSM_FILE BASIS :: FILE './basis.xsm' ;
XSM_FILE PACK :: FILE './initial_pack.xsm' ;
XSM_FILE GRCON :: FILE './global_rcon.xsm' ;
XSM_FILE RCON1 :: FILE './plane1_rcon.xsm' ;
XSM_FILE RCON2 :: FILE './plane2_rcon.xsm' ;
XSM_FILE RCON3 :: FILE './plane3_rcon.xsm' ;
'''
BOOT_PREFIX='''XSM_FILE PROJECT :: FILE './projected_boot.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE AXTRACK :: FILE './axial_track.xsm' ;
XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AXMACRO :: FILE './axial_macro.xsm' ;
XSM_FILE GRCON :: FILE './global_rcon.xsm' ;
SEQ_BINARY TRACK_f1 :: FILE './radial1.bin' ;
SEQ_BINARY TRACK_f2 :: FILE './radial2.bin' ;
SEQ_BINARY TRACK_f3 :: FILE './radial3.bin' ;
LINKED_LIST MICROLIB2 MACRO0 TRACK SYS1 SYS2 SYS3 ;
MODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 1 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS1 := ASM: MACRO0 TRACK TRACK_f1 PROJECT :: EDIT 0 ARM LK1D 1 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 2 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS2 := ASM: MACRO0 TRACK TRACK_f2 PROJECT :: EDIT 0 ARM LK1D 2 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
MICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 3 EDIT 0 ;
MACRO0 := MICROLIB2 ;
MICROLIB2 := DELETE: MICROLIB2 ;
SYS3 := ASM: MACRO0 TRACK TRACK_f3 PROJECT :: EDIT 0 ARM LK1D 3 ;
MACRO0 TRACK := DELETE: MACRO0 TRACK ;
'''

# Conditional physical file bounds are host planning gates, never measured peaks.
# Old fixed producer files/reports remain protected outside this fresh namespace.
STORAGE_FORECAST={
 'pack':{'maximum_live':['3 owned producer aliases','PACK','small independent context/runtime/metadata'],
         'upper_bound_bytes':3*156880856+(480+128)*MI},
 'initial_controls':{'maximum_live':['PACK','one private negative PACK','remaining128MiB'],
                     'upper_bound_bytes':(480+480+128)*MI},
 'GLOBAL':{'maximum_live':['PACK','private GLOBAL stage','GLOBAL','remaining128MiB'],
           'upper_bound_bytes':(480+560+560+128)*MI},
 'projection':{'maximum_live':['PACK','GLOBAL','one private PROJECT','remaining128MiB'],
               'upper_bound_bytes':(480+560+800+128)*MI},
 'retained_global_negative':{'maximum_live':['PROJECT','one private negative PROJECT','remaining128MiB'],
                            'upper_bound_bytes':(800+800+128)*MI},
 'BOOT':{'maximum_live':['PROJECT','private solved archive','closed final archive','remaining128MiB'],
         'upper_bound_bytes':(800+480+480+128)*MI},
 'final_retained':{'maximum_live':['PROJECT retains entire independent GLOBAL/producer archive',
                                 'closed final archive','all final axial/context/runtime/log/proof files within128MiB'],
                   'upper_bound_bytes':(800+480+128)*MI},
 'all_forecasts_are_conditional_guard_bounds_not_actual_sizes':True,
 'fresh_original_cap_bytes':2*2**30,
 'whole_EOF_and_complete_tree_proof_required_before_each_temporary_release':True}
if any(row.get('upper_bound_bytes',0)>=2*2**30 for row in STORAGE_FORECAST.values()if isinstance(row,dict)):
    raise RuntimeError('storage Source forecasting must fit unchanged fresh2GiB')

def ext(args,prefix):
    return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))

def unique(rows):
    out={}
    for row in rows:
        if row['path']in out and out[row['path']]!=row:raise RuntimeError('inconsistent independent full pins')
        out[row['path']]=row
    return list(out.values())

class PhaseResources:
    def __init__(self,original):self.original=original;self.phase='input';self.peaks={};self.pending_publication_reserved_bytes=0
    def check(self):
        r=self.original.check();fresh=r['fresh_output']['artifact_bytes']
        caps={'initial_pack.xsm':480*MI,'global.xsm':560*MI,'BOOT-GLOBAL64-STAGE.xsm':560*MI,
              'projected_boot.xsm':800*MI,'negative_pack.xsm':480*MI,'negative_project.xsm':800*MI,
              'BOOT-SOLVED-STAGE.xsm':480*MI,'closed_boot_archive.xsm':480*MI}
        main=0
        for name,cap in caps.items():
            p=WORK/name
            if p.exists():
                n=p.stat().st_size
                if n>cap:raise RuntimeError('strict storage planning bound exceeded: '+name)
                main+=n
        # Input producer aliases are deliberately finite, owned phase copies.
        for i in range(1,4):
            p=WORK/('native_A'+str(i)+'.xsm')
            if p.exists():
                if p.stat().st_size!=156880856:raise RuntimeError('actual finite producer copy size')
                main+=p.stat().st_size
        if fresh-main+self.pending_publication_reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')
        if fresh+self.pending_publication_reserved_bytes>=2*2**30:raise RuntimeError('original total fresh2GiB')
        self.peaks[self.phase]=max(self.peaks.get(self.phase,0),fresh)
        return dict(r,publication_reserved_bytes=self.pending_publication_reserved_bytes,actual_phase=self.phase,observed_fresh_peak_bytes=self.peaks[self.phase])

def main():
    p=argparse.ArgumentParser()
    for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze']:
        for suffix in ['summary','sha256','seven-id']:p.add_argument('--'+prefix+'-'+suffix,required=True)
    args=p.parse_args();start=time.monotonic()
    hf,phf=ext(args,'host_freeze')
    if hf['schema']!='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V9' or \
       Path(hf['host_source']['path']).resolve()!=Path(__file__).resolve():
        raise RuntimeError('exact owning complete Host Source freeze')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    if before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:
        raise RuntimeError('initial history96GiB reserves originalcold/metadata/fullfresh2GiB')
    build,pbuild=ext(args,'build70')
    if pbuild!=hf['selected_actual_build70_report']:raise RuntimeError('exact external selected actual70 report pin required')
    if build['schema']!='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2' or \
       build['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       build['failure'] is not None or build['after_check_error'] is not None or \
       build['Dragon_linked'] is not True or len(build['records'])!=3 or \
       build['final_report_resource_check_passed']is not True or \
       build['old69_inputs_identical_and_retained'] is not True or \
       build['remaining68_original_inputs_identical_and_retained'] is not True or \
       build['old_nine_objects_identical_and_retained'] is not True or \
       [record['label'].rsplit('/',1)[-1]for record in build['records']]!=['compile_module','compile_driver','link_Dragon']:
        raise RuntimeError('actual cache-module/driver compile and complete70 link required')
    c.closed_report(build,helper,Path(pbuild['path']).parent,3)
    c.verify_rows(build['fixed_current_pins']);c.verify_rows(build['output_pins'])
    current69_pin=build['original_actual69_handle_lifetime_report_pin']
    current69,checked_current69_pin=c.load_json_exact(current69_pin['path'],current69_pin['sha256'],json.dumps(current69_pin['identity']))
    if checked_current69_pin!=current69_pin or \
       current69_pin!=hf['selected_original_actual69_handle_lifetime_report'] or \
       current69['schema']!='ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1' or \
       current69['status']!='ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       current69['failure'] is not None or current69['after_check_error'] is not None or \
       current69['Dragon_linked'] is not True or len(current69['records'])!=2 or \
       current69['remaining68_link_inputs_identical_and_retained'] is not True or \
       current69['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('separate actual native-handle complete69 two-stage premise required')
    c.closed_report(current69,helper,Path(current69_pin['path']).parent,2)
    c.verify_rows(current69['fixed_current_pins']);c.verify_rows(current69['output_pins'])
    original69_pin=build['original_actual69_v4_report_pin']
    original69,checked_original69_pin=c.load_json_exact(original69_pin['path'],original69_pin['sha256'],json.dumps(original69_pin['identity']))
    if checked_original69_pin!=original69_pin or \
       current69['original_actual69_v4_report_pin']!=original69_pin or \
       original69_pin!=hf['selected_original_actual69_v4_report'] or \
       original69['schema']!='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       original69['status']!='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       original69['failure'] is not None or original69['after_check_error'] is not None or \
       original69['Dragon_linked'] is not True or len(original69['records'])!=10:
        raise RuntimeError('original actual nine-alias complete69 ten-stage premise required')
    c.closed_report(original69,helper,Path(original69_pin['path']).parent,10)
    c.verify_rows(original69['fixed_current_pins']);c.verify_rows(original69['output_pins'])
    original69_link=original69['records'][-1]['command'][3:-2]
    current69_link=current69['records'][-1]['command'][3:-2]
    current70_link=build['records'][-1]['command'][3:-2]
    if len(original69_link)!=69 or len(current69_link)!=69 or \
       [i for i,(old_path,new_path)in enumerate(zip(original69_link,current69_link))if old_path!=new_path]!=[37] or \
       Path(original69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       Path(current69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o':
        raise RuntimeError('only actual native-driver object position37 changed in the separate complete69 premise')
    module_positions=[i for i,path in enumerate(current70_link)if Path(path).name=='SPOT1P64.o']
    first_archive=next(i for i,path in enumerate(current69_link)if path.endswith('.a'))
    if len(current70_link)!=70 or len(set(current70_link))!=70 or module_positions!=[first_archive] or \
       build['actual_complete70_link_inputs']!=current70_link or \
       build['replacement_zero_based_current69_input_index']!=37 or \
       build['module_insertion_current69_before_archive_index']!=first_archive or \
       [row['path']for row in build['original_current69_ordered_input_pins']]!=current69_link:
        raise RuntimeError('one genuine cache module inserted immediately before the original first archive')
    stripped70=current70_link[:first_archive]+current70_link[first_archive+1:]
    if [i for i,(old_path,new_path)in enumerate(zip(current69_link,stripped70))if old_path!=new_path]!=[37] or \
       Path(stripped70[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       [path for path in current70_link if path.endswith('.a')]!=[path for path in current69_link if path.endswith('.a')]:
        raise RuntimeError('removing the new cache helper and restoring only driver37 must recover exact original69 order')
    native_freeze_pin=hf['selected_native_exact_block_cache_source_freeze']
    native_sf,checked_native_freeze_pin=c.read_bound_json_current(native_freeze_pin['path'],native_freeze_pin)
    if checked_native_freeze_pin!=native_freeze_pin or build['actual_new_Source_freeze_pin']!=native_freeze_pin or \
       native_sf['schema']!='COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_ONLY_FREEZE_V1' or \
       native_sf['candidate_imported_or_executed']is not False or native_sf['compiled']is not False:
        raise RuntimeError('actual complete70 must bind the exact two-Fortran cache Source freeze')
    native_sf_rows=native_sf['files']+native_sf['original_source_pins']+native_sf['control_sources']+\
                   [native_sf['complete_byte_inverse_pin'],native_sf['control_plan_pin'],native_sf['logical_memory_key_contract_pin']]
    c.verify_rows(native_sf_rows)
    actual_new_sources=build['actual_new_Source_pins']
    if len(actual_new_sources)!=2 or \
       [Path(row['path']).name for row in actual_new_sources]!=['SPOT1P64.f90','SPOT_GLOBAL_NATIVE_DRIVER64.f'] or \
       any(row not in native_sf['files']for row in actual_new_sources) or \
       native_freeze_pin not in build['fixed_current_pins'] or \
       current69_pin not in build['fixed_current_pins'] or original69_pin not in build['fixed_current_pins']:
        raise RuntimeError('actual complete70 fixed pins must retain exact Sources and both genuine69 premises')
    c.verify_rows(build['original_current69_ordered_input_pins'])
    old9=binding['seventeen_required_same_production_object_pins']
    if len(old9)!=9 or any(row['path']not in current70_link for row in old9) or \
       any(row not in build['fixed_current_pins']for row in old9):
        raise RuntimeError('all original nine core objects remain exact current fixed inputs in complete70')
    direct_binding_path=HERE/'DIRECT_ALIAS_ENTRY_BINDING.json'
    if not all(any(row['path']==str(HERE/name)for row in hf['dependencies'])
               for name in ['DIRECT_ALIAS_ENTRY_BINDING.json','direct_alias_entry_controls.f90']):
        raise RuntimeError('direct-entry binding and Fortran main must belong to the complete frozen Host Source')
    direct_probe_source_pin=next(row for row in hf['dependencies']
                                 if row['path']==str(HERE/'direct_alias_entry_controls.f90'))
    direct_binding_pin=next(row for row in hf['dependencies']if row['path']==str(direct_binding_path))
    direct_binding,checked_direct_binding_pin=c.read_bound_json_current(direct_binding_path,direct_binding_pin)
    if checked_direct_binding_pin!=direct_binding_pin:raise RuntimeError('exact current direct-entry binding fullpin')
    link_command=build['records'][-1]['command']
    direct_original_inputs=direct_binding['actual_original_ordered_70_link_inputs']
    removed_main=direct_binding['excluded_original_main_pin']
    if direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V2' or \
       direct_binding['selected_actual_build70_report_pin']!=pbuild or \
       direct_binding['new_probe_source']!=str(HERE/'direct_alias_entry_controls.f90') or \
       direct_binding['only_main_object_replacement']is not True or \
       direct_binding['physics_qualification']is not False or \
       link_command[:3]!=[build['records'][0]['command'][0],'-O2','-ffp-contract=off'] or \
       link_command[-2:]!=['-o',next(row['path']for row in build['output_pins']if Path(row['path']).name=='Dragon')] or \
       link_command[3:-2]!=[row['path']for row in direct_original_inputs] or \
       len(direct_original_inputs)!=70 or \
       sum(Path(row['path']).suffix=='.o'for row in direct_original_inputs)!=66 or \
       sum(Path(row['path']).suffix=='.a'for row in direct_original_inputs)!=4 or \
       [row for row in direct_original_inputs if Path(row['path']).name=='DRAGON.o']!=[removed_main] or \
       direct_original_inputs[12]!=removed_main or \
       set(direct_binding['three_direct_control_modes'])!={'pack_original_alias','initial_contract_alias','view_system_alias'}:
        raise RuntimeError('exact actual ordered70 inputs with only original DRAGON main replacement required')
    c.verify_rows(direct_original_inputs)
    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    sf,psf=ext(args,'source_freeze')
    if psf!=hf['selected_fortran_freeze']:raise RuntimeError('exact external selected frozen Fortran Source required')
    if sf['schema']!='COMPLETE_NEW_FORTRAN_STORAGE_SOURCE_FROZEN_V1':raise RuntimeError('complete Fortran Source freeze')
    c.verify_rows(sf['files']);c.same_pin(sf['formal_and_actual_input_plan']['path'],sf['formal_and_actual_input_plan'])
    formal_plan_pin=next(row for row in hf['dependencies']if row['path']==str(data.PLAN))
    c.same_pin(data.PLAN,formal_plan_pin)
    plan,producer_fixed,producer_reports=data.validate_actual_producers(c,args)
    for row in producer_reports:c.closed_report(row,helper,Path(row['actual_output_pin']['path']).parent.parent,4)
    fixed=unique(fixed+[phf,hf['host_source'],pbuild,p17,psf]+hf['dependencies']+sf['files']+
                 [sf['formal_and_actual_input_plan']]+producer_fixed+build['fixed_current_pins']+build['output_pins']+direct_original_inputs+
                 seventeen['fixed_current_pins']+seventeen['output_pins']+native_sf_rows+
                 [current69_pin,original69_pin]+current69['fixed_current_pins']+current69['output_pins']+
                 original69['fixed_current_pins']+original69['output_pins'])
    c.verify_rows(fixed)
    resources=PhaseResources(base_resources)
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir();WORK.mkdir();(OUT/'AAA3-streaming').mkdir()
    exe=next(x for x in build['output_pins']if Path(x['path']).name=='Dragon')
    shutil.copy2(exe['path'],OUT/'runtime/Dragon');shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned=[c.pin(OUT/'runtime/Dragon'),c.pin(OUT/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=exe['sha256'] or owned[1]['sha256']!=binding['original_bounded']['sha256']:
        raise RuntimeError('exact actual70 runtime and original bounded guard')
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA3-streaming',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise RuntimeError('genuine original supervisor')
    ledger=[];proofs=[];cases=[];failure=None;after_error=None;result=None
    new_storage_cases=[];lifecycle_cases=[];scratch_ledger=[];direct_alias_cases=[]
    direct_alias_build=None
    def stable():
        c.check_full_current(fixed,owned);resources.check()
        if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 elapsed cap')
    def retain(path):
        row=c.pin(path)
        if row['identity'][3]!=1 or any(tuple(row['identity'][:2])==tuple(x['identity'][:2])for x in fixed):
            raise RuntimeError('owned regular single-link distinct physical file required')
        if any(x['path']==row['path']for x in owned):raise RuntimeError('owned current file cannot be silently rebound')
        owned.append(row);return row
    def copy(row,name):
        target=WORK/name
        if target.exists()or target.is_symlink():raise RuntimeError('fresh owned alias only')
        c.same_pin(row['path'],row);shutil.copy2(row['path'],target);actual=retain(target)
        if actual['sha256']!=row['sha256']or actual['size_bytes']!=row['size_bytes']or actual['identity'][:2]==row['identity'][:2]:
            raise RuntimeError('complete exact copy with independent7ID')
        stable();return actual
    def release(name,why,evidence):
        target=WORK/name
        if target.parent!=WORK or target.name!=name or name not in [
          'native_A1.xsm','native_A2.xsm','native_A3.xsm','initial_pack.xsm','global.xsm',
          'negative_pack.xsm','negative_project.xsm','negative_system.xsm','negative_output.xsm',
          'negative_packout.xsm','negative_rcon1.xsm','negative_rcon2.xsm','negative_rcon3.xsm',
          'negative_ax.xsm','negative_archive.xsm','BOOT-SOLVED-STAGE.xsm']:
            raise RuntimeError('exact owned finite temporary release whitelist')
        row=c.pin(target)
        if row['identity'][3]!=1 or any(row['identity'][:2]==x['identity'][:2]for x in fixed):
            raise RuntimeError('release only independent regular single-link owned temporary')
        old=next((x for x in owned if x['path']==str(target)),None)
        if old is not None and row!=old:raise RuntimeError('owned readonly temporary changed before release')
        stable();target.unlink();owned[:]=[x for x in owned if x['path']!=str(target)]
        ledger.append(dict(released_full_pin=row,reason=why,complete_evidence=evidence,
                           exact_intermediate_XSM_raw_replay_retained=False,original_producer_files_retained=True))
        receipt=OUT/('Root_actual_private_release_'+str(len(ledger)).zfill(3)+'.json')
        c.write(receipt,ledger[-1]);retain(receipt);stable()
    def clean_driver_scratch_before():
        for name in ('_main001','_DUMMY'):
            target=WORK/name
            if target.exists()or target.is_symlink():
                raise RuntimeError('fresh actual CLE scratch paths required before each Dragon; no overwrite or retry')
    def stash_closed_driver_scratch(label):
        # Ganlib creates these only after the verified pre-launch absence. An
        # XABORT exit1 bypasses normal CLE teardown. Preserve exact raw bytes;
        # no deletion, no shared/producer object, no altered refusal oracle.
        if not label.replace('_','').isalnum():raise RuntimeError('finite literal driver label')
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());logpin=c.pin(lp);watchpin=c.pin(wp)
        if record['label']!='AAA/'+label or record['status']not in ('PASS','FAILED')or \
           w['command']!=record['command']or w['command']!=[str(OUT/'runtime/Dragon')]or \
           type(w.get('pid'))is not int or w['pid']<=0 or type(w['returncode'])is not int or \
           w['limit_failure']is not None or w['rss_cap_mib']!=512 or w['own_child_only']is not True or \
           w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or \
           not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('only genuine completed guarded Dragon permits scratch archival')
        if (record['status']=='PASS')!=(w['returncode']==0):raise RuntimeError('actual child closure status differs')
        receipt=dict(actual_stage_index=len(runner.records)-1,actual_stage_label=record['label'],
          actual_pid=w['pid'],actual_returncode=w['returncode'],actual_log_full_pin=logpin,
          actual_watchdog_full_pin=watchpin,exact_preserved_scratch_files=[],
          scratch_protocol_sources=hf['scratch_protocol_sources'],no_qualification_from_archival=True)
        folder=OUT/'cle_scratch_archive'/(str(len(runner.records)).zfill(3)+'_'+label)
        for name in ('_main001','_DUMMY'):
            source=WORK/name
            if not source.exists()and not source.is_symlink():continue
            before_pin=c.pin(source)
            if source.parent!=WORK or source.is_symlink()or before_pin['identity'][3]!=1 or \
               any(before_pin['identity'][:2]==row['identity'][:2]for row in fixed+owned):
                raise RuntimeError('scratch must be distinct exclusively owned regular single-link file')
            stable();folder.mkdir(parents=True,exist_ok=True)
            if folder.is_symlink()or folder.parent.is_symlink():raise RuntimeError('own scratch archive directories only')
            target=folder/name
            if target.exists()or target.is_symlink():raise RuntimeError('fresh archival target; no overwrite')
            c.same_pin(source,before_pin);source.rename(target);after_pin=retain(target)
            if after_pin['sha256']!=before_pin['sha256']or after_pin['size_bytes']!=before_pin['size_bytes']or \
               after_pin['identity'][:6]!=before_pin['identity'][:6]or source.exists()or source.is_symlink():
                raise RuntimeError('same physical scratch inode and complete raw bytes required after rename')
            receipt['exact_preserved_scratch_files'].append(dict(before_full_pin=before_pin,after_full_pin=after_pin,
              ctime_may_change_during_rename=True,exact_physical_raw_replay_retained=True))
            stable()
        clean_driver_scratch_before();scratch_ledger.append(receipt)
        rp=OUT/('Root_actual_closed_CLE_scratch_stash_'+str(len(runner.records)).zfill(3)+'.json')
        c.write(rp,receipt);retain(rp);stable()
    def run(label,deck,marker=None):
        f=WORK/(label+'.x2m');f.write_text(deck);retain(f);stable();clean_driver_scratch_before()
        error=None
        try:runner.execute(WORK,label,[str(OUT/'runtime/Dragon')],600,marker=marker,deck=f.name)
        except BaseException as exc:error=exc
        stash_closed_driver_scratch(label)
        if error is not None:raise error
        helper.check_watch(OUT,runner.records[-1]);stable()
    def refuse(label,deck,message):
        f=WORK/(label+'.x2m');f.write_text(deck);retain(f);stable();clean_driver_scratch_before();error=None
        try:runner.execute(WORK,label,[str(OUT/'runtime/Dragon')],600,deck=f.name)
        except RuntimeError as exc:error=str(exc)
        stash_closed_driver_scratch(label)
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());text=lp.read_text()
        if error!='own-child stage failed; no retry'or record['status']!='FAILED'or type(w['returncode'])is not int or w['returncode']!=1 or w['limit_failure']is not None:
            raise RuntimeError('only exact intended operator refusal can close this control')
        forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
          'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
          'SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
        if w['command']!=record['command'] or w['wall_cap_seconds']>record['wall_cap_seconds'] or \
           any(mark in text for mark in forbidden):raise RuntimeError('actual refusal command/cap or pre-kernel trace differs')
        if text.count(message)!=1 or w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('exact refusal reason and original child limits')
        cases.append(dict(case=label,expected_abort=message,actual_exit_code=w['returncode'],actual_abort_message_exact=True,pre_transport_abort_at_frozen_validation_branch=True,
                          no_positive_solver_or_seal_trace=True,
                          actual_log_pin=c.pin(lp),actual_watchdog_pin=c.pin(wp),original_execution_record_index=len(runner.records)-1,
                          original_execution_record_label=record['label'],all_actual_assertions_completed=True))
        stable()
    def direct_refuse(label,message):
        # This actual child has its own main, so it never invokes CLE or creates
        # CLE scratch. Three target validation guards precede REDGET/material use.
        if direct_alias_build is None or label not in direct_binding['three_direct_control_modes']:
            raise RuntimeError('actual closed direct-entry executable and declared mode required')
        declared=direct_binding['three_direct_control_modes'][label]
        if declared['expected_abort']!=message or declared['material_payload_inspected']is not False or \
           declared['transport_executed']is not False:
            raise RuntimeError('exact structural entry scope and unmodified target refusal required')
        clean_driver_scratch_before();input_pins=[]
        for name in declared['actual_readonly_input_filenames']:
            path=WORK/name
            row=next((row for row in owned if row['path']==str(path)),None)
            if row is None:raise RuntimeError('direct control uses only current full pinned owned readonly inputs')
            c.same_pin(path,row);input_pins.append(row)
        if len({tuple(row['identity'][:2])for row in input_pins})!=len(input_pins):
            raise RuntimeError('actual input files remain physically distinct; only supplied c_ptr is deliberately repeated')
        for name in declared['fresh_private_output_filenames']:
            path=WORK/name
            if path.exists()or path.is_symlink():raise RuntimeError('fresh finite private direct-control outputs only')
        command=[str(OUT/'runtime/direct_alias_entry_controls'),label]
        stable();error=None
        try:runner.execute(WORK,label,command,600)
        except RuntimeError as exc:error=str(exc)
        record=runner.records[-1];wp=WORK/(label+'.watchdog.json');lp=WORK/(label+'.log')
        w=json.loads(wp.read_text());text=lp.read_text()
        clean_driver_scratch_before()
        forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
          'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
          'SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL',
          'kernel error','INCONSISTENT CALL','TARGET GUARD RETURNED']
        if error!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           type(w.get('pid'))is not int or w['pid']<=0 or type(w['returncode'])is not int or w['returncode']!=1 or \
           w['limit_failure']is not None or w['command']!=command or record['command']!=command or \
           text.count('ACTUAL-AAA3-DIRECT-ALIAS-CONTROL: '+label)!=1 or text.count(message)!=1 or \
           any(mark in text for mark in forbidden)or \
           w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
           not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or \
           not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('only exact actual component direct-entry exit1 guard closes this structural control')
        for row in input_pins:c.same_pin(row['path'],row)
        case=dict(case=label,expected_abort=message,actual_exit_code=w['returncode'],actual_abort_message_exact=True,
          entry_invocation='ACTUAL_COMPONENT_DIRECT_CALL_WITH_DISTINCT_NAMES_AND_DUPLICATE_C_PTR',
          actual_component=declared['component'],actual_closed_build_evidence=direct_alias_build,
          declared_operand_construction=declared,actual_readonly_input_full_pins=input_pins,
          component_structural_guard_only=True,CLE_dispatch_executed=False,transport_executed=False,
          pre_transport_abort_at_frozen_validation_branch=True,no_positive_solver_or_seal_trace=True,
          actual_log_pin=c.pin(lp),actual_watchdog_pin=c.pin(wp),
          original_execution_record_index=len(runner.records)-1,original_execution_record_label=record['label'],
          all_actual_assertions_completed=True)
        cases.append(case);direct_alias_cases.append(label);stable()
    def cleanup(names,why,evidence):
        for name in names:
            if(WORK/name).exists():release(name,why,evidence)
    def storage_refuse(label,deck,message):
        refuse(label,deck,message);new_storage_cases.append(label)
    def writable_control(name):
        target=WORK/name;row=c.pin(target)
        if target.parent!=WORK or target.is_symlink()or row['identity'][3]!=1 or \
           any(row['identity'][:2]==x['identity'][:2]for x in fixed+owned if x['path']!=str(target)):
            raise RuntimeError('exclusive same-inode regular single-link private writable clone')
        owned[:]=[x for x in owned if x['path']!=str(target)];return row
    try:
        # Replace ONLY the main object in the original actual ordered70 link.
        # Every component/core/alias object and all four archives remain exact.
        resources.phase='direct_alias_probe_build'
        compiler=build['records'][0]['command'][0]
        includes=[x for x in build['records'][0]['command']if x.startswith('-I')]
        probe_obj=OUT/'build/direct_alias_entry_controls.o'
        probe_exe=OUT/'runtime/direct_alias_entry_controls'
        probe_compile=[compiler,*c.FLAGS,*includes,'-J'+str(OUT/'build'),'-c',
                       str(HERE/'direct_alias_entry_controls.f90'),'-o',str(probe_obj)]
        probe_inputs=[str(probe_obj)if row['path']==removed_main['path']else row['path']for row in direct_original_inputs]
        probe_link=[*link_command[:3],*probe_inputs,'-o',str(probe_exe)]
        if len(probe_inputs)!=70 or probe_inputs.count(str(probe_obj))!=1 or \
           any(actual!=original['path']for actual,original in zip(probe_inputs,direct_original_inputs)
               if original['path']!=removed_main['path']):
            raise RuntimeError('exact one-main-only ordered link replacement')
        direct_indices=[]
        for label,command in [('direct_alias_compile',probe_compile),('direct_alias_link',probe_link)]:
            stable();runner.execute(OUT/'build',label,command,600)
            helper.check_watch(OUT,runner.records[-1]);direct_indices.append(len(runner.records)-1);stable()
        probe_obj_pin=retain(probe_obj);probe_exe_pin=retain(probe_exe)
        direct_alias_build=dict(actual_compile_link_record_indices=direct_indices,
          actual_new_main_frozen_source_pin=direct_probe_source_pin,
          actual_compile_command=probe_compile,actual_link_command=probe_link,
          original_ordered_70_inputs=direct_original_inputs,removed_original_main_pin=removed_main,
          actual_new_main_full_pin=probe_obj_pin,actual_new_executable_full_pin=probe_exe_pin,
          retained_original_component_and_archive_count=69,only_main_replaced=True,physics_qualification=False)
        # These copies are only access aliases. Reports and original producer pins
        # remain independent fixed inputs throughout every stage and publication.
        for i,row in enumerate(plan['producers'],1):
            copy(row['archive'],'native_A'+str(i)+'.xsm');copy(row['radial_binary_track'],'radial'+str(i)+'.bin')
        formal={Path(x['path']).name:x for x in plan['formal_inputs']}
        for original,name in [('initial_axial_track.xsm','axial_track.xsm'),('initial_axial_macrolib.xsm','axial_macro.xsm'),
                              ('basis_reference.xsm','basis.xsm'),('route_contract.xsm','global_rcon.xsm')]:copy(formal[original],name)
        packdeck=''.join('XSM_FILE '+n+' :: FILE \'./'+f+'\' ;\n'for n,f in [
          ('PACK','initial_pack.xsm'),('RCON1','plane1_rcon.xsm'),('RCON2','plane2_rcon.xsm'),('RCON3','plane3_rcon.xsm'),
          ('A1','native_A1.xsm'),('A2','native_A2.xsm'),('A3','native_A3.xsm')])
        packdeck+='MODULE APACKX64: END: ;\nPACK RCON1 RCON2 RCON3 := APACKX64: A1 A2 A3 :: ;\n'
        resources.phase='pack_controls'
        negpack=packdeck.replace('initial_pack.xsm','negative_packout.xsm').replace('plane1_rcon.xsm','negative_rcon1.xsm').replace('plane2_rcon.xsm','negative_rcon2.xsm').replace('plane3_rcon.xsm','negative_rcon3.xsm')
        for label,deck,message in [
          ('pack_missing_original',negpack.replace('A1 A2 A3 :: ;','A1 A2 :: ;'),'APACKX64: FOUR OUTPUTS AND THREE INDEPENDENT INPUTS REQUIRED.'),
          ('pack_memory_outputs',negpack.replace("XSM_FILE PACK :: FILE './negative_packout.xsm' ;",'LINKED_LIST PACK ;'),'APACKX64: STRICT FRESH XSM / READONLY XSM ORDER REQUIRED.'),
          ('pack_original_alias',None,'APACKX64: INDEPENDENT DISTINCT OPERANDS REQUIRED.'),
          ('pack_wrong_order',negpack.replace('A1 A2 A3 :: ;','A2 A1 A3 :: ;'),'APACKX64: OWN PLANE CASE REQUIRED.'),
          ('pack_no_fake_options',negpack.replace('A1 A2 A3 :: ;','A1 A2 A3 :: SYNTHETIC ;'),'APACKX64: NO SYNTHETIC PRODUCER OPTIONS ALLOWED.')]:
            if label=='pack_original_alias':
                direct_refuse(label,message);new_storage_cases.append(label)
            else:storage_refuse(label,deck+'END: ; QUIT "LIST" .\n',message)
            cleanup(['negative_packout.xsm','negative_rcon1.xsm','negative_rcon2.xsm','negative_rcon3.xsm'],
                    'unqualified pre-kernel APACK private outputs',cases[-1])
        resources.phase='pack';run('pack',packdeck+'ECHO "ACTUAL-AAA3-INDEPENDENT-PACK-COMPLETE" ;\nEND: ; QUIT "LIST" .\n','ACTUAL-AAA3-INDEPENDENT-PACK-COMPLETE')
        for n in ['initial_pack.xsm','plane1_rcon.xsm','plane2_rcon.xsm','plane3_rcon.xsm']:retain(WORK/n)
        packed=data.packed_readback(WORK/'initial_pack.xsm',plan);proofs.append(dict(stage='pack',actual_full_items=packed))
        c.write(OUT/'Root_actual_independent_three_plane_pack_readback.json',proofs[-1])
        for i in range(1,4):release('native_A'+str(i)+'.xsm','independent producer originals and complete18 packed trees retained',proofs[-1])
        # Compile only the bounded negative-input mutator; no Native/solver here.
        cmd=build['records'][0]['command'];compiler=cmd[0]
        includes=[x for x in cmd if x.startswith('-I')]
        obj=OUT/'build/mutate_owned_control.o';mut=OUT/'runtime/mutate_owned_control'
        compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(OUT/'build'),'-c',str(HERE/'mutate_owned_control.f90'),'-o',str(obj)]
        archives=[x for x in build['records'][-1]['command']if x.endswith('.a')]
        for i,command in enumerate([compile_cmd,[compiler,'-O2','-ffp-contract=off',str(obj),*archives,'-o',str(mut)]]):
            stable();runner.execute(OUT/'build','mutator_'+str(i),command,600);helper.check_watch(OUT,runner.records[-1]);stable()
        retain(mut);retain(obj)
        resources.phase='initial_operator_controls'
        operands='MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2 RCON3'
        def initial(params='RANK 1 EDIT 0',ops=operands,pack='initial_pack.xsm',out='negative_system.xsm'):
            return PREFIX.replace('./initial_pack.xsm','./'+pack)+'XSM_FILE SYSOUT :: FILE \'./'+out+'\' ;\nMODULE SPOOPP64: END: ;\nSYSOUT := SPOOPP64: '+ops+' :: '+params+' ;\nEND: ; QUIT "LIST" .\n'
        for label,params,ops,message in [
          ('initial_missing_rank','EDIT 0',operands,'SPOOPP64: RANK MUST BE EXPLICIT, NO DEFAULT.'),
          ('initial_duplicate_rank','RANK 1 RANK 1',operands,'SPOOPP64: DUPLICATE RANK.'),
          ('initial_wrong_rank_type','RANK 1.0',operands,'SPOOPP64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('initial_zero_rank','RANK 0',operands,'SPOOPP64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('initial_missing_plane_contract','RANK 1','MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2','SPOOPP64: NINE FULL OPERANDS REQUIRED.'),
          ('initial_contract_alias',None,None,'SPOOPP64: CONTRACT OPERAND ALIAS.'),
          ('initial_wrong_plane_order','RANK 1','MACRO AXTRACK PACK BASIS GRCON RCON2 RCON1 RCON3','SPOASMP64: GENUINE COMPLETE NATIVE INPUT REQUIRED.')]:
            if label=='initial_contract_alias':direct_refuse(label,message)
            else:refuse(label,initial(params,ops),message)
            if(WORK/'negative_system.xsm').exists():release('negative_system.xsm','unqualified initial operator negative output',cases[-1])
        for mutation in ['missing_seal','wrong_case','wrong_plane','wrong_epoch','flux32','source32','LPOD_only']:
            copy(c.pin(WORK/'initial_pack.xsm'),'negative_pack.xsm')
            # Only this explicitly designated clone is writable during mutator.
            control_pin=c.pin(WORK/'negative_pack.xsm')
            if Path(control_pin['path']).parent!=WORK or not stat.S_ISREG(control_pin['identity'][2])or control_pin['identity'][3]!=1 or \
               any(control_pin['identity'][:2]==x['identity'][:2]for x in fixed+owned if x['path']!=control_pin['path']):
                raise RuntimeError('exclusive regular single-link private writable control clone')
            owned[:]=[x for x in owned if x['path']!=str(WORK/'negative_pack.xsm')]
            stable();runner.execute(WORK,'mutate_'+mutation,[str(mut),'negative_pack.xsm',mutation],600)
            helper.check_watch(OUT,runner.records[-1]);mutated=retain(WORK/'negative_pack.xsm')
            if mutated['identity'][:2]!=control_pin['identity'][:2]or mutated['sha256']==control_pin['sha256']:
                raise RuntimeError('actual declared mutation must change the same independent owned clone')
            stable()
            expected_message=('SPOASM: INVALID OFFLINE REAL64 SOURCE ITEM.'if mutation=='source32'else
                              'SPOASMP64: GENUINE COMPLETE NATIVE INPUT REQUIRED.')
            refuse('initial_'+mutation,initial(pack='negative_pack.xsm'),expected_message)
            if(WORK/'negative_system.xsm').exists():release('negative_system.xsm','unqualified initial operator negative output',cases[-1])
            release('negative_pack.xsm','one finite exact private control clone; original18 trees retained',cases[-1])
        run('initial_positive',initial(out='initial_system.xsm').replace('END: ; QUIT "LIST" .','ECHO "ACTUAL-AAA3-INITIAL-OPERATOR-COMPLETE" ;\nEND: ; QUIT "LIST" .'),
            'ACTUAL-AAA3-INITIAL-OPERATOR-COMPLETE');retain(WORK/'initial_system.xsm')
        resources.phase='GLOBAL'
        globaldeck=PREFIX+'''XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE GLOBAL :: FILE './global.xsm' ;
MODULE FLUGLOBAL64: END: ;
AX GLOBAL := FLUGLOBAL64: MACRO AXTRACK AXSYSTEM PACK GRCON ::
  EDIT -3 TYPE K B1 SIGS EXTE 500 5.00000000E-08 REBA OFF
  ACCE 3 0 UNKT 5.00000000E-08 THER 740 5.00000000E-08 ;
ECHO "ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE" ;
END: ; QUIT "LIST" .
'''
        run('global_positive',globaldeck,'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE')
        retain(WORK/'ax_current.xsm');retain(WORK/'global.xsm')
        resources.phase='projection'
        projectprefix=PREFIX+'''XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;
XSM_FILE AX :: FILE './ax_current.xsm' ;
XSM_FILE GLOBAL :: FILE './global.xsm' ;
XSM_FILE PROJECT :: FILE './projected_boot.xsm' ;
MODULE BPROJX64: END: ;
'''
        # New single-private projection checks use actual independent full inputs.
        negproject=projectprefix.replace('projected_boot.xsm','negative_output.xsm')
        for label,params,head,message in [
          ('project_missing_rank','',negproject,'BPROJX64: MANDATORY UNIQUE RANK KEYWORD REQUIRED.'),
          ('project_rank_type','RANK 1.0',negproject,'BPROJX64: INTEGER RANK REQUIRED.'),
          ('project_zero_rank','RANK 0',negproject,'BPROJX64: RANK MUST BE EXACTLY ONE OR TWO.'),
          ('project_duplicate_rank','RANK 1 RANK 1',negproject,'BPROJX64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.'),
          ('project_case_rank_mismatch','RANK 2',negproject,'BPROJX64: COMPLETE PROJECTION ADMISSION OR COMMIT FAILED.'),
          ('project_memory_output','RANK 1',negproject.replace("XSM_FILE PROJECT :: FILE './negative_output.xsm' ;",'LINKED_LIST PROJECT ;'),'BPROJX64: PRIVATE XSM OUTPUT REQUIRED.')]:
            storage_refuse(label,head+'PROJECT := BPROJX64: GLOBAL AX AXTRACK AXSYSTEM MACRO PACK GRCON :: '+params+' ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_output.xsm'],'unqualified single-private projection control output',cases[-1])
        run('project_positive',projectprefix+'PROJECT := BPROJX64: GLOBAL AX AXTRACK AXSYSTEM MACRO PACK GRCON :: RANK 1 ;\n'
            +'ECHO "ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE" ;\nEND: ; QUIT "LIST" .\n','ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE')
        retain(WORK/'projected_boot.xsm')
        roots={n:WORK/f for n,f in ROOT_NAMES.items()}
        transferred=data.transfer_readback(WORK/'projected_boot.xsm',WORK/'global.xsm',WORK/'initial_pack.xsm',roots,plan)
        transferred=dict(stage='independent_complete_transfer',actual_tree_proof=transferred,
          project_full_pin=c.pin(WORK/'projected_boot.xsm'),global_full_pin=c.pin(WORK/'global.xsm'),pack_full_pin=c.pin(WORK/'initial_pack.xsm'))
        proofs.append(transferred);c.write(OUT/'Root_actual_complete_independent_transfer_readback.json',transferred)
        # Keep all original producer and formal inputs. Retained PROJECT contains
        # every original packed record and every old GLOBAL context/tree exactly.
        release('initial_pack.xsm','complete retained PROJECT/GLOBAL64/ARCHIVE matches independent originals',transferred)
        release('global.xsm','complete retained PROJECT/GLOBAL64 matches independent GLOBAL full tree',transferred)
        resources.phase='BOOT_storage_controls'
        # CLE requires actual defined systems before dispatching any component.
        # Reuse the complete positive BOOT recovery/ASM prefix for these guards.
        precheck=BOOT_PREFIX.replace('MODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;',
          'MODULE RECOVER: ASM: DELETE: SPOBVX64: SPOBOOX64: END: ;')+'''XSM_FILE AXOUT :: FILE './negative_ax.xsm' ;
XSM_FILE ARCOUT :: FILE './negative_archive.xsm' ;
'''
        viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'
        for label,head,ops,message in [
          ('view_missing_operand',precheck,viewops.rsplit(' ',1)[0],'SPOBVX64: EXACT FOURTEEN ORDERED OPERANDS REQUIRED.'),
          ('view_memory_output',precheck.replace("XSM_FILE AXOUT :: FILE './negative_ax.xsm' ;",'LINKED_LIST AXOUT ;'),viewops,'SPOBVX64: FRESH PRIVATE XSM OUTPUT PAIR REQUIRED.'),
          ('view_system_alias',None,None,'SPOBVX64: OPERAND ALIAS OR REPEATED NAME.')]:
            if label=='view_system_alias':
                direct_refuse(label,message);new_storage_cases.append(label)
            else:storage_refuse(label,head+'AXOUT ARCOUT := SPOBVX64: '+ops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_ax.xsm','negative_archive.xsm'],'unqualified pre-kernel view-pair outputs',cases[-1])
        for label,params,message in [
          ('pair_missing_rank','EDIT 0','SPOBOOX64: RANK HAS NO DEFAULT.'),
          ('pair_rank_type','RANK 1.0 EDIT 0','SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.'),
          ('pair_case_rank_mismatch','RANK 2 EDIT 0','SPOBOOX64: CASE RANK MISMATCH.')]:
            storage_refuse(label,precheck+'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: '+params+' ;\nEND: ; QUIT "LIST" .\n',message)
            cleanup(['negative_ax.xsm','negative_archive.xsm'],'unqualified pre-kernel complete BOOT pair outputs',cases[-1])
        if len(new_storage_cases)!=17 or len(set(new_storage_cases))!=17:raise RuntimeError('complete declared new17 strict-storage controls')
        copy(c.pin(WORK/'projected_boot.xsm'),'negative_project.xsm')
        before_mut=writable_control('negative_project.xsm');stable()
        runner.execute(WORK,'mutate_retained_global_case',[str(mut),'negative_project.xsm','global_case'],600)
        helper.check_watch(OUT,runner.records[-1]);changed=retain(WORK/'negative_project.xsm')
        if changed['identity'][:2]!=before_mut['identity'][:2]or changed['sha256']==before_mut['sha256']:
            raise RuntimeError('actual retained-global mutation is same private inode and differs')
        refuse('lifecycle_mutated_retained_global',precheck.replace('projected_boot.xsm','negative_project.xsm')+
          'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',
          'SPOBOOX64: GENUINE FULL PROJECTED-BOOT/E0 CONTEXT REQUIRED.')
        lifecycle_cases.append(cases[-1]['case'])
        cleanup(['negative_ax.xsm','negative_archive.xsm','negative_project.xsm'],'unqualified mutated retained GLOBAL complete control clone',cases[-1])
        c.write(WORK/'BOOT-SOLVED-STAGE.xsm',dict(unqualified_private_lifecycle_sentinel=True));retain(WORK/'BOOT-SOLVED-STAGE.xsm')
        sentinel=c.pin(WORK/'BOOT-SOLVED-STAGE.xsm')
        refuse('lifecycle_no_private_archive_overwrite',precheck+'AXOUT ARCOUT := SPOBVX64: '+viewops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n',
          'SPOBOOX64: PRIVATE ARCHIVE EXISTS; NO OVERWRITE.')
        c.same_pin(sentinel['path'],sentinel);lifecycle_cases.append(cases[-1]['case'])
        cleanup(['negative_ax.xsm','negative_archive.xsm','BOOT-SOLVED-STAGE.xsm'],'unchanged private sentinel; refusal before any kernel',cases[-1])
        if len(cases)!=33:raise RuntimeError('14 genuine operator +17 new storage +2 lifecycle refusals required')
        resources.phase='BOOT'
        bootdeck=BOOT_PREFIX+'''XSM_FILE AXOUT :: FILE './closed_boot_axial.xsm' ;
XSM_FILE ARCOUT :: FILE './closed_boot_archive.xsm' ;
AXOUT ARCOUT := SPOBVX64: PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON
  SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3 :: RANK 1 EDIT 0 ;
ECHO "ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE" ;
END: ; QUIT "LIST" .
'''
        # The independent proof above plus this unchanged full file pin is the
        # owning current-context authority for nested views, never self-comparison.
        stable();run('BOOT_positive',bootdeck,'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE')
        log=(WORK/'BOOT_positive.log').read_text()
        readbacks=[json.loads(line)for line in log.splitlines()if line.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"')]
        if len(readbacks)!=1 or readbacks[0]['status']!='PASS' or readbacks[0]['all_payload_bits_equal']is not True:
            raise RuntimeError('actual whole sealed-pair payload readback before private solved stage destruction')
        axpin=retain(WORK/'closed_boot_axial.xsm');arcpin=retain(WORK/'closed_boot_archive.xsm')
        result=data.final_readback(WORK/'closed_boot_axial.xsm',WORK/'closed_boot_archive.xsm')
        result=dict(actual_terminal=result,AX_full_pin=axpin,ARCHIVE_full_pin=arcpin,actual_Fortran_complete_copy_readback=readbacks[0])
        c.write(OUT/'Root_actual_complete_BOOT_terminal_readback.json',result);stable()
        if len(direct_alias_cases)!=3 or len(set(direct_alias_cases))!=3:
            raise RuntimeError('all three actual structural component alias guards required')
        if len(runner.records)!=50 or sum(x['status']=='PASS'for x in runner.records)!=17 or \
           sum(x['status']=='FAILED'for x in runner.records)!=33:
            raise RuntimeError('all50 genuine stages:17 success plus33 exact intended exit1 refusals')
    except BaseException as exc:failure=type(exc).__name__+': '+str(exc)
    finally:
        try:stable();after=resources.check()
        except BaseException as exc:after_error=type(exc).__name__+': '+str(exc);after=None
    # Complete unmodified original execution records are written first. Only
    # this compact final receipt may claim engineering closed0 after raw-record
    # full-EOF readback and all original limits have genuinely passed.
    raw=dict(schema='ACTUAL_AAA3_COMPLETE_EXECUTION_PREPUBLICATION_RECORD_V1',
      failure=failure,after_check_error=after_error,records=runner.records,fixed_current_pins=fixed,
      owned_runtime_pins=owned,actual_operator_refusals=cases,actual_complete_readback_proofs=proofs,
      actual_direct_structural_alias_control_names=direct_alias_cases,actual_direct_alias_build=direct_alias_build,
      actual_terminal=result,actual_private_release_ledger=ledger,actual_closed_CLE_scratch_archival_ledger=scratch_ledger,
      private_release_ledger_scope='HOST_OWNED_UNLINK_ONLY',
      frozen_Fortran_internal_disposal=dict(names=['BOOT-MAC-1/2/3.xsm','BOOT-Q-1/2/3.xsm','BOOT-SOLVED-STAGE.xsm'],
         source='aaa_three_plane_streaming_source_v2/SPOBOOX64.f90',
         complete_logical_readback_before_disposal_required_by_frozen_source=True,
         actual_complete_copy_readback_seen=result is not None,
         independent_physical_EOF_pins_available=False,exact_raw_replay_retained=False),
      engineering_three_plane_closed0=False,
      current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),
      exact_publication_pending=True,**c.scope())
    rawpath=OUT/'Root_actual_complete_execution_record_before_final_publication.json'
    c.write(rawpath,raw);rawpin=retain(rawpath)
    resources.pending_publication_reserved_bytes=8*MI
    try:
        stable();output_pins=[]
        for f in sorted(OUT.rglob('*')):
            if f.is_symlink():raise RuntimeError('current output inventory symlink forbidden')
            if f.is_file():output_pins.append(c.pin(f))
        c.verify_rows(output_pins);stable();after=resources.check()
    except BaseException as exc:
        after_error=type(exc).__name__+': '+str(exc);output_pins=[];after=None
    closed=failure is None and after_error is None and result is not None
    compact_records=[{k:v for k,v in record.items()if k not in ('resource_before','resource_after')}
                     for record in runner.records]
    report=dict(schema='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1',
      status='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'if closed else 'FAILED_UNQUALIFIED_NO_RETRY',
      output_pins=output_pins,physical_EOF_hashes_separate_from_logical_tree_digests=True,
      complete_unmodified_execution_records_pin=rawpin,actual_closed_CLE_scratch_archival_ledger=scratch_ledger,
      failure=failure,after_check_error=after_error,records=compact_records,fixed_current_pins=fixed,
      owned_runtime_pins=owned,actual_terminal=result,
      actual_direct_structural_alias_control_names=direct_alias_cases,actual_direct_alias_build=direct_alias_build,
      actual_operator_refusals=[{k:v for k,v in case.items()if k!='record'}for case in cases],
      actual_complete_readback_proofs=proofs,
      actual_private_release_ledger=[dict(released_full_pin=x['released_full_pin'],reason=x['reason'],
         complete_evidence_in_unmodified_execution_record=True,
         exact_intermediate_XSM_raw_replay_retained=False,original_producer_files_retained=True)for x in ledger],
      historical_released_pins_are_not_current_live_pins=True,private_release_ledger_scope='HOST_OWNED_UNLINK_ONLY',
      frozen_Fortran_internal_disposal=raw['frozen_Fortran_internal_disposal'],angular_moments_status='UNKNOWN',
      actual_fresh_peaks_by_phase=resources.peaks,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,wall_seconds=time.monotonic()-start,
      resources_before=before,resources_after=after,engineering_three_plane_closed0=closed,
      independent_reference_physics_assessment_executed=False,
      all_new_storage_entry_controls_closed=closed and len(new_storage_cases)==17 and len(lifecycle_cases)==2,
      actual_new_storage_control_names=new_storage_cases,actual_negative_lifecycle_control_names=lifecycle_cases,
      storage_phase_maximum_simultaneous_inventory=STORAGE_FORECAST,
      final_publication_reserved_bytes=8*MI,
      current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),**c.scope())
    final_size=sum(len(chunk.encode('utf-8'))for chunk in json.JSONEncoder(indent=2,ensure_ascii=False,
                    allow_nan=False).iterencode(report))+1
    if final_size>8*MI:raise RuntimeError('compact final publication exceeds independently guarded8MiB reserve')
    c.write(OUT/'Root_actual_three_plane_engineering_summary.json',report)
    resources.pending_publication_reserved_bytes=0
    stable();resources.check()
    if not closed:raise RuntimeError(failure or after_error or 'no actual terminal')

if __name__=='__main__':main()

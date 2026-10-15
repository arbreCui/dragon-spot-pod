#!/usr/bin/env python3
"""Current genuine CLE refusals and readonly carrier/loader controls. No transport.

The positive FLUNAT64 solve is the later, separately admitted warm-A main case.
Each declared refusal exits before any driver/kernel call, on the actual Dragon.
No XABORT shim, retry, altered original guard, or inherited old17 PASS.
"""
import argparse
import json
from pathlib import Path
import time
import guarded_warm_A_common as c

OUT=c.ART/'axial-material-current-warm-A-CLE-entry-controls-20261012'
POSITIVE='''XSM_FILE CASE_OUT :: FILE './case_output.xsm' ;
LINKED_LIST RCONTRACT BOOT_BIND ARCH_CTL ;
MODULE AXNCASE64: BACKUP: END: ;
RCONTRACT BOOT_BIND := AXNCASE64: :: ;
ARCH_CTL := BACKUP: RCONTRACT :: LIST 1 ITEM 1 ;
ARCH_CTL := BACKUP: ARCH_CTL BOOT_BIND :: ITEM 1 ;
CASE_OUT := ARCH_CTL ;
ECHO "WARM-A-CURRENT-CASE-CLE-COMPLETE" ;
END: ; QUIT "LIST" .
'''
AX_PREFIX='LINKED_LIST RCONTRACT BOOT_BIND ;\nMODULE AXNCASE64: END: ;\n'
FLU_PREFIX='''XSM_FILE SEED_IN :: FILE '../../inputs/snapshot_A.xsm' ;
XSM_FILE CASE_IN :: FILE '../case_positive/case_output.xsm' ;
LINKED_LIST SEEDSET CASESET FLUX TRACK SYSTEM MICROLIB2 RCONTRACT BOOT_BIND WRONG_BIND ;
MODULE RECOVER: AXNCASE64: FLUNAT64: ERASE: END: ;
SEEDSET := SEED_IN ;
TRACK := RECOVER: SEEDSET :: ITEM 1 ;
SYSTEM := RECOVER: SEEDSET :: ITEM 1 ;
MICROLIB2 := RECOVER: SEEDSET :: ITEM 1 ;
FLUX := RECOVER: SEEDSET :: ITEM 1 ;
RCONTRACT BOOT_BIND := AXNCASE64: :: ;
'''
PARAMS='EDIT 0 TYPE K EXTE 500 2.50000000E-07 UNKT 2.50000000E-07 THER 2.50000000E-07 REBA INIT ON'

def controls():
    rows=[]
    def ax(name,line,message,prefix=AX_PREFIX):
        rows.append(dict(case=name,deck=prefix+line+'\nEND: ; QUIT "LIST" .\n',expected_abort=message))
    ax('axncase_wrong_count','RCONTRACT := AXNCASE64: :: ;','AXNCASE64: TWO FRESH CASE OUTPUTS REQUIRED.')
    ax('axncase_wrong_output_order','BOOT_BIND RCONTRACT := AXNCASE64: :: ;','AXNCASE64: EXACT FRESH MEMORY OUTPUT ORDER REQUIRED.')
    ax('axncase_wrong_output_media','RCONTRACT BOOT_BIND := AXNCASE64: :: ;',
       'AXNCASE64: EXACT FRESH MEMORY OUTPUT ORDER REQUIRED.',
       "XSM_FILE RCONTRACT :: FILE './wrong_output.xsm' ;\nLINKED_LIST BOOT_BIND ;\nMODULE AXNCASE64: END: ;\n")
    ax('axncase_disallowed_keyword','RCONTRACT BOOT_BIND := AXNCASE64: :: RANK 1 ;',
       'AXNCASE64: ONLY THE DECLARED CASE IS ALLOWED.')
    def flu(name,message,operands='RCONTRACT BOOT_BIND',params=PARAMS,prefix=FLU_PREFIX):
        rows.append(dict(case=name,deck=prefix+'FLUX := FLUNAT64: FLUX SYSTEM MICROLIB2 TRACK '+operands+' ::\n '+params+' ;\nEND: ; QUIT "LIST" .\n',expected_abort=message))
    flu('flunat64_missing_bind','FLUNAT64: MATERIAL/CONTRACT/BOOT_BIND REQUIRED.',operands='RCONTRACT')
    flu('flunat64_missing_contract','FLUNAT64: MATERIAL/CONTRACT/BOOT_BIND REQUIRED.',operands='BOOT_BIND')
    flu('flunat64_wrong_bind_name','FLUNAT64: NAMED READ-ONLY BOOT_BIND REQUIRED.',
        operands='RCONTRACT WRONG_BIND',prefix=FLU_PREFIX+'WRONG_BIND := BOOT_BIND ;\n')
    flu('flunat64_init_off','FLUNAT64: ORIGINAL NATIVE MCCG WARM TYPE K ROUTE REQUIRED.',params=PARAMS.replace('INIT ON','INIT OFF'))
    flu('flunat64_reba_off','FLUNAT64: ORIGINAL NATIVE MCCG WARM TYPE K ROUTE REQUIRED.',params=PARAMS.replace('REBA INIT','REBA OFF INIT'))
    flu('flunat64_mismatched_contract_eps','FLUNAT64: ORIGINAL NATIVE CONTROLS DIFFER FROM CONTRACT.',
        params=PARAMS.replace('2.50000000E-07','2.50001000E-07'))
    empty_prefix=FLU_PREFIX+'BOOT_BIND := ERASE: BOOT_BIND ;\n'
    flu('flunat64_empty_bind','FLU: INVALID RHS SIGNATURE RECORD.',prefix=empty_prefix)
    empty_prefix=FLU_PREFIX+'RCONTRACT := ERASE: RCONTRACT ;\n'
    flu('flunat64_empty_contract','FLU: INVALID RHS SIGNATURE RECORD.',prefix=empty_prefix)
    return rows

def expect_abort(runner,folder,row,fixed,owned):
    c.check_full_current(fixed,owned)
    error=None
    try:runner.execute(folder,'refusal',[str(OUT/'runtime/Dragon')],600,deck='control.x2m')
    except RuntimeError as caught:error=str(caught)
    record=runner.records[-1]
    watch_path=folder/'refusal.watchdog.json';w=json.loads(watch_path.read_text())
    text=(folder/'refusal.log').read_text(errors='strict')
    if error!='own-child stage failed; no retry' or record['status']!='FAILED':
        raise RuntimeError('declared refusal must be actual nonzero exit, no other failure accepted')
    if type(w['returncode']) is not int or w['returncode']==0 or w['limit_failure'] is not None:
        raise RuntimeError('actual exit refusal, without wall/RSS/disk/liveness failure')
    if w['command']!=record['command'] or w['rss_cap_mib']!=512 or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True:
        raise RuntimeError('unchanged real own-child guard receipt')
    if not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:
        raise RuntimeError('actual original refusal limits')
    if text.count(row['expected_abort'])!=1 or 'WARM-A-CURRENT-CASE-CLE-COMPLETE' in text:
        raise RuntimeError('exact intended current XABORT must be the unique terminal reason')
    if any(token in text for token in ('ROOT64-NEW-WARM-A-NATIVE-COMPLETE','FLUX SOLUTION DOOR','native terminal publication')):
        raise RuntimeError('no solver/kernel or producer terminal permitted in entry refusal')
    c.check_full_current(fixed,owned)
    return dict(case=row['case'],expected_abort=row['expected_abort'],actual_exit_code=w['returncode'],
       actual_abort_message_exact=True,all_actual_assertions_completed=True,transport_executed=False,
       record=record,actual_log_pin=c.pin(folder/'refusal.log'),actual_watchdog_pin=c.pin(watch_path))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seventeen-summary',required=True)
    parser.add_argument('--seventeen-sha256',required=True);parser.add_argument('--seventeen-seven-id',required=True)
    args=parser.parse_args();start=time.monotonic()
    binding,fixed,support,helper,full,resources,before=c.initialize(OUT,start)
    seventeen,seventeen_pin=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    fixed+=[seventeen_pin]+seventeen['fixed_current_pins']+seventeen['output_pins']
    runner,owned=c.create_runtime(OUT,start,support,full,resources,binding,'WARM_A_ENTRY_CONTROLS')
    (OUT/'inputs').mkdir();(OUT/'cases').mkdir()
    seed=next(x for x in binding['physical_inputs'] if x['role']=='readonly_seed_archive')['pin']
    import shutil
    shutil.copy2(seed['path'],OUT/'inputs/snapshot_A.xsm');seed_copy=c.pin(OUT/'inputs/snapshot_A.xsm')
    if seed_copy['sha256']!=seed['sha256'] or seed_copy['identity']==seed['identity']:raise RuntimeError('actual owned control seed exact/new7ID')
    owned.append(seed_copy)
    commands=c.probe_commands(OUT,binding);cases=[];success=[];failure=None
    c.write(OUT/'Root_current_entry_controls_binding.json',dict(fixed_current_pins=fixed,owned_runtime_pins=owned,
      actual_probe_commands=commands,declared_controls=controls(),positive_case_deck=POSITIVE,scope='current CLE/carrier prekernel refusal controls only'))
    try:
        for index,command in enumerate(commands):
            c.check_full_current(fixed,owned);runner.execute(OUT/'build','compile_'+str(index),command,600)
            helper.check_watch(OUT,runner.records[-1])
        probe_pin=c.pin(OUT/'runtime/verify_native_A_archive64');owned.append(probe_pin)
        folder=OUT/'cases/case_positive';folder.mkdir();(folder/'control.x2m').write_text(POSITIVE)
        owned.append(c.pin(folder/'control.x2m'))
        runner.execute(folder,'case_positive',[str(OUT/'runtime/Dragon')],600,marker='WARM-A-CURRENT-CASE-CLE-COMPLETE',deck='control.x2m')
        helper.check_watch(OUT,runner.records[-1]);case_archive=c.pin(folder/'case_output.xsm');owned.append(case_archive)
        runner.execute(folder,'case_readback',[probe_pin['path'],'case','case_output.xsm'],600)
        helper.check_watch(OUT,runner.records[-1]);row=json.loads((folder/'case_readback.log').read_text())
        if row.get('all_actual_assertions_completed') is not True or row.get('case_name')!='R64WARM-A-V1 ':
            raise RuntimeError('actual padded case/CLE complete readonly roundtrip')
        success.append(row)
        runner.execute(OUT/'inputs','loader_controls',[probe_pin['path'],'loader_controls','snapshot_A.xsm'],600)
        helper.check_watch(OUT,runner.records[-1]);row=json.loads((OUT/'inputs/loader_controls.log').read_text())
        if row.get('actual_loader_calls')!=8 or row.get('actual_refusals')!=7 or row.get('all_actual_assertions_completed') is not True:
            raise RuntimeError('actual loader all370 baseline plus seven exact refusals')
        success.append(row)
        for row in controls():
            folder=OUT/'cases'/row['case'];folder.mkdir();(folder/'control.x2m').write_text(row['deck']);owned.append(c.pin(folder/'control.x2m'))
            cases.append(expect_abort(runner,folder,row,fixed,owned))
        c.check_full_current(fixed,owned);after=resources.check()
        if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 cap')
    except BaseException as error:
        failure=repr(error);after=None
    report=dict(schema='ACTUAL_CURRENT_WARM_A_CLE_ENTRY_CONTROLS_ROOT_V1',
       status='ACTUAL_CURRENT_WARM_A_CLE_ENTRY_CONTROLS_CLOSED0_ONLY' if failure is None else 'FAILED_CURRENT_WARM_A_ENTRY_CONTROLS_NO_RETRY',
       failure=failure,after_check_error=None,records=runner.records,fixed_current_pins=fixed,owned_runtime_pins=owned,
       actual_refusal_cases=cases,actual_positive_readbacks=success,declared_control_oracles=controls(),
       original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
       SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,
       output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],resources_before=before,resources_after=after,
       transport_executed=False,physical_producer_qualified=False,old_seventeen_PASS_inherited=False,**c.scope())
    c.write(OUT/'Root_actual_entry_controls_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))
    return 0 if failure is None else 1
if __name__=='__main__':raise SystemExit(main())

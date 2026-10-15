#!/usr/bin/env python3
"""One owned plane1/e0 actual warm solve, strictly after complete actual controls.

No full runtime rebuild, retry, threshold relaxation, three-plane/GLOBAL/rank or
online BOOT certificate. The new readonly probe is separately compiled and linked
under the original guard, then validates the complete actual output archive.
"""
import argparse
import json
from pathlib import Path
import shutil
import time
import guarded_warm_A_common as c
import run_current_warm_A_entry_controls as entry

OUT=c.ART/'axial-material-new-REAL64-native-warm-A-20261012-v2'

def covered_saved_controls(binding,helper):
    core_path=Path(binding['actual_core83_report']['path']);ingress_path=Path(binding['actual_AB_ingress_report']['path'])
    c.same_pin(core_path,binding['actual_core83_report']);c.same_pin(ingress_path,binding['actual_AB_ingress_report'])
    core=json.loads(core_path.read_text());ingress=json.loads(ingress_path.read_text())
    if core['status']!='ACTUAL_83_CORE_CONTROLS_CLOSED0_ONLY' or ingress['status']!='ACTUAL_AB_WARM_INGRESS_CLOSED0_ONLY':
        raise RuntimeError('actual corresponding saved control PASS required')
    c.closed_report(core,helper,core_path.parent,3);c.closed_report(ingress,helper,ingress_path.parent,4)
    s=core['actual_control_summary']
    if (s['control_count'],s['explicit_publish_calls'],s['explicit_read_calls'],s['explicit_import_calls'])!=(83,32,52,55):
        raise RuntimeError('full actual83 exact scope/call counts')
    if len(core['actual_cases'])!=83 or any(r.get('all_actual_assertions_completed') is not True for r in core['actual_cases']):
        raise RuntimeError('actual all83 Source assertions')
    for mapping in binding['covered_existing_control_source_and_object_applicability']:
        table={p['path']:p for p in (core if mapping['report']=='core83' else ingress)['fixed_current_pins']}
        if mapping['pin']['path'] not in table or table[mapping['pin']['path']]!=mapping['pin']:
            raise RuntimeError('actual corresponding complete Source/object applicability differs')
        c.same_pin(mapping['pin']['path'],mapping['pin'])
    for mapping in binding['actual_covered_Source_object_compile_origins']:
        row=mapping['actual_compile_origin_report'];c.same_pin(row['path'],row)
        origin=json.loads(Path(row['path']).read_text())
        c.closed_report(origin,helper,Path(row['path']).parent,len(origin['records']))
        if mapping['actual_compile_record'] not in origin['records']:raise RuntimeError('actual covered compile Source/object command')
        c.same_pin(mapping['source_pin']['path'],mapping['source_pin']);c.same_pin(mapping['object_pin']['path'],mapping['object_pin'])
    if ingress.get('actual_A_B_archives_readonly') is not True or ingress.get('external_input_full_EOF_SHA_and_7ID_stable') is not True:
        raise RuntimeError('actual physical typed A/B ingress scope')
    if [row['case']for row in ingress['actual_cases']]!=['A','B']:
        raise RuntimeError('both actual physical typed ingress cases')
    for row in ingress['actual_cases']:
        if row.get('status')!='PASS' or row.get('native_flux_bits_equal') is not True or row.get('native_keff_bits_equal') is not True or row.get('flux_values')!=5180:
            raise RuntimeError('actual full370 typed seed input bit equality')
    return core,ingress

def admit_entry(path,sha,seven,binding,helper):
    d,p=c.load_json_exact(path,sha,seven)
    if d['schema']!='ACTUAL_CURRENT_WARM_A_CLE_ENTRY_CONTROLS_ROOT_V1' or d['status']!='ACTUAL_CURRENT_WARM_A_CLE_ENTRY_CONTROLS_CLOSED0_ONLY' or d['failure'] is not None or d['after_check_error'] is not None:
        raise RuntimeError('actual declared current CLE entry controls required')
    c.verify_rows(d['fixed_current_pins']);c.verify_rows(d['owned_runtime_pins']);c.verify_rows(d['output_pins'])
    if d['original_guard_class']!='OwnRSSSerialExecutor' or d['original_guard_MRO_unchanged'] is not True or not 0<d['wall_seconds']<1800 or not 0<=d['SELF_peak_bytes']<512*2**20:
        raise RuntimeError('actual route original guard/caps')
    expected=entry.controls()
    if d['declared_control_oracles']!=expected or len(d['records'])!=5+len(expected) or len(d['actual_refusal_cases'])!=len(expected):
        raise RuntimeError('complete current Source declared route oracles')
    for record in d['records'][:5]:
        if record['status']!='PASS':raise RuntimeError('actual positive entry/probe stages')
        helper.check_watch(Path(path).parent,record)
    for row,wanted,record in zip(d['actual_refusal_cases'],expected,d['records'][5:]):
        if row['case']!=wanted['case'] or row['expected_abort']!=wanted['expected_abort'] or row['actual_abort_message_exact'] is not True or row['all_actual_assertions_completed'] is not True or row['transport_executed'] is not False:
            raise RuntimeError('actual exact intended prekernel refusal')
        if row['record']!=record or record['status']!='FAILED':raise RuntimeError('actual refusal stage')
        w=json.loads(Path(row['actual_watchdog_pin']['path']).read_text());log=Path(row['actual_log_pin']['path']).read_text()
        if w['command']!=record['command'] or w['returncode']!=row['actual_exit_code'] or type(w['returncode']) is not int or w['returncode']==0 or w['limit_failure'] is not None:
            raise RuntimeError('actual controlled exit; resource/runtime failures cannot be PASS')
        if w['rss_cap_mib']!=512 or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('actual refusal original wall/RSS/liveness caps')
        if log.count(wanted['expected_abort'])!=1:raise RuntimeError('actual intended unique XABORT')
    if len(d['actual_positive_readbacks'])!=2 or any(r['all_actual_assertions_completed'] is not True for r in d['actual_positive_readbacks']):
        raise RuntimeError('complete case and loader actual readbacks')
    if d['actual_positive_readbacks'][0]['case_name']!='R64WARM-A-V1 ' or d['actual_positive_readbacks'][1]['actual_loader_calls']!=8 or d['actual_positive_readbacks'][1]['actual_refusals']!=7:
        raise RuntimeError('actual exact name and complete typed ingress refusal counts')
    pins={r['path']:r for r in d['fixed_current_pins']}
    for r in binding['fixed_current_pins']:
        if pins.get(r['path'])!=r:raise RuntimeError('entry controls whole current runtime/Source applicability')
    if d['transport_executed'] is not False or d['physical_producer_qualified'] is not False:
        raise RuntimeError('entry control scope')
    return d,p

def main():
    parser=argparse.ArgumentParser()
    for prefix in ('seventeen','entry-controls'):
        parser.add_argument('--'+prefix+'-summary',required=True)
        parser.add_argument('--'+prefix+'-sha256',required=True)
        parser.add_argument('--'+prefix+'-seven-id',required=True)
    args=parser.parse_args();start=time.monotonic()
    binding,fixed,support,helper,full,resources,before=c.initialize(OUT,start)
    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    core,ingress=covered_saved_controls(binding,helper)
    route,proute=admit_entry(args.entry_controls_summary,args.entry_controls_sha256,args.entry_controls_seven_id,binding,helper)
    fixed+=[p17,proute]+seventeen['fixed_current_pins']+seventeen['output_pins']+route['fixed_current_pins']+route['output_pins']
    # Every prerequisite finishes before this new namespace or any child exists.
    runner,owned=c.create_runtime(OUT,start,support,full,resources,binding,'A')
    copies=[]
    for row in binding['physical_inputs']:
        if row['role']=='readonly_rays_reference':continue
        source=row['pin'];destination=OUT/'A'/Path(source['path']).name
        shutil.copy2(source['path'],destination);new=c.pin(destination)
        if new['sha256']!=source['sha256'] or new['size_bytes']!=source['size_bytes'] or new['identity']==source['identity']:
            raise RuntimeError('whole original bytes with fresh owned7ID')
        copies.append(dict(role=row['role'],original=source,owned=new));owned.append(new)
    deck=OUT/'A/ROOT64_NEW_WARM_A_20261011.x2m';shutil.copy2(binding['exact_warm_deck']['path'],deck)
    owned.append(c.pin(deck))
    if owned[-1]['sha256']!=binding['exact_warm_deck']['sha256']:raise RuntimeError('whole original warm deck bytes')
    rays=OUT/'A/radial_track.bin';archive=OUT/'A/new_native_A.xsm'
    if rays.exists() or rays.is_symlink() or archive.exists() or archive.is_symlink():raise RuntimeError('SALT binary track and native output both initially absent')
    commands=c.probe_commands(OUT,binding)+[[str(OUT/'runtime/Dragon')],[str(OUT/'runtime/verify_native_A_archive64'),'native','new_native_A.xsm']]
    c.write(OUT/'Root_current_warm_A_binding.json',dict(fixed_current_pins=fixed,actual_commands=commands,
      owned_readonly_inputs=copies,owned_runtime_pins=owned,stdin_deck=c.pin(deck),
      SALT_binary_track_role='fresh actual output, may mutate only during the solver child; fullEOF pin after terminal',
      independently_owned_prerequisites=[p17,proute],original_stage600_whole1800_SELFchild512MiB=True,**c.scope()))
    failure=None;terminal=None;output_after_solve=None;final_rays=None;watchdogs=[];after=None
    try:
        for index,command in enumerate(commands[:2]):
            c.check_full_current(fixed,owned);runner.execute(OUT/'build','compile_'+str(index),command,600)
            watchdogs.append(helper.check_watch(OUT,runner.records[-1]))
        owned.append(c.pin(OUT/'runtime/verify_native_A_archive64'))
        c.check_full_current(fixed,owned)
        runner.execute(OUT/'A','solve',commands[2],600,marker='ROOT64-NEW-WARM-A-NATIVE-COMPLETE',deck=deck.name)
        watchdogs.append(helper.check_watch(OUT,runner.records[-1]))
        c.check_full_current(fixed,owned)
        output_after_solve=c.pin(archive);final_rays=c.pin(rays)
        reference=next(x['pin']for x in binding['physical_inputs']if x['role']=='readonly_rays_reference')
        if final_rays['sha256']!=reference['sha256'] or final_rays['size_bytes']!=reference['size_bytes']:
            raise RuntimeError('actual SALT complete binary differs from retained exact geometry/rays reference')
        c.write(OUT/'Host_actual_producer_terminal_output_fullEOF_binding.json',dict(schema='OWNING_WARM_A_ACTUAL_PRODUCER_FULLFILE_TERMINAL_BINDING_V1',
          actual_solver_record=runner.records[-1],actual_watchdog=watchdogs[-1],actual_output_pin=output_after_solve,
          actual_SALT_binary_track_pin=final_rays,readonly_original_rays_reference=reference,
          independent_full_Source_tool_input_pins=fixed,internal_ROOT_REF_is_not_external_authority=True,**c.scope()))
        runner.execute(OUT/'A','native_readback',commands[3],600)
        watchdogs.append(helper.check_watch(OUT,runner.records[-1]))
        c.same_pin(archive,output_after_solve);c.same_pin(rays,final_rays);c.check_full_current(fixed,owned)
        terminal=json.loads((OUT/'A/native_readback.log').read_text())
        if terminal['schema']!='ACTUAL_NEW_WARM_A_COMPLETE_NATIVE_TERMINAL_READBACK_V1' or terminal['status']!='PASS' or (terminal['plane'],terminal['epoch'],terminal['groups'],terminal['unknowns'])!=(1,0,370,14):
            raise RuntimeError('actual strict full physical Native readback')
        if any(terminal[k] is not True for k in ('all370_ROOT_FLUX64_FLUX64_REF_bits_equal','full_source64_type4_finite_and_exact_mirror','archive_read_only','strict_terminal_gate_passed')) or terminal['full_native_read_status']!=3:
            raise RuntimeError('full actual native terminal, no mirror promotion')
        if any(terminal[k] is not False for k in c.scope()):raise RuntimeError('single-plane producer scope remains bounded')
        after=resources.check()
        if time.monotonic()-start>=1800:raise RuntimeError('original whole1800 cap')
    except BaseException as error:
        failure=repr(error)
        try:after=resources.check()
        except BaseException:pass
    report=dict(schema='ACTUAL_CURRENT_SINGLE_PLANE_WARM_A_NATIVE_PRODUCER_ROOT_V1',
      status='ACTUAL_SINGLE_PLANE1_E0_WARM_A_NATIVE_PRODUCER_CLOSED0_ONLY' if failure is None else 'FAILED_WARM_A_NATIVE_PRODUCER_NO_RETRY',
      failure=failure,records=runner.records,fixed_current_pins=fixed,owned_runtime_pins=owned,
      actual_output_pin=output_after_solve,actual_SALT_binary_track_pin=final_rays,actual_native_terminal=terminal,
      actual_watchdog_checks=watchdogs,resources_before=before,resources_after=after,
      original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,
      output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],
      transport_executed=any(r['label']=='A/solve' for r in runner.records),single_plane_native_producer_closed=failure is None,
      all3_original_native_producer_inputs_qualified=False,old_wholeInput_or_Q_inherited=False,**c.scope())
    c.write(OUT/'Root_actual_single_plane_warm_A_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))
    return 0 if failure is None else 1
if __name__=='__main__':raise SystemExit(main())

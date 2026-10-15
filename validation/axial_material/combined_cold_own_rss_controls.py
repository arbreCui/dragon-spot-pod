"""Two actual isolated own-child controls for a new canonical controller.

Source preparation alone grants no PASS. The reviewed future factory supplies
all real input pins. Root must actually run this program, retain complete
stdout/stderr, and write the independent exit-zero terminal witness afterward.
This program starts no Dragon, transport, assembly, or linear solve.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ENTRY_STARTED = time.monotonic()
sys.dont_write_bytecode = True
POSITIVE_MARKER = 'POSITIVE_NEW_CANONICAL_OWN_CHILD_CONTROL_COMPLETE'
OVERSIZE_REASON = 'own-child 512 MiB RSS cap reached'
OVERSIZE_BYTES = 576 * 2**20


def write_once(path, value):
    with Path(path).open('x') as out:
        json.dump(value, out, sort_keys=True, indent=2, allow_nan=False)
        out.write('\n')


def fixture(mode):
    """Real control child; its OS RSS must be sampled by the genuine guard."""
    if mode not in ('positive', 'oversize'):
        raise ValueError('one fixed genuine positive or oversize control command required')
    nbytes = 16 * 2**20 if mode == 'positive' else OVERSIZE_BYTES
    print(json.dumps(dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,
                          pid=os.getpid(),requested_bytes=nbytes)),flush=True)
    payload = bytearray(nbytes)
    for offset in range(0, nbytes, 4096):
        payload[offset] = 1
    if mode == 'positive':
        time.sleep(.8)
        if payload[0] != 1 or payload[-4096] != 1:
            raise ValueError('actual touched small control allocation differs')
        print(POSITIVE_MARKER,flush=True)
    else:
        print('ACTUAL_OVERSIZE_ALLOCATION_TOUCHED_WAITING_FOR_ORIGINAL_RSS_GUARD',flush=True)
        time.sleep(65)
        raise RuntimeError('oversize child returned without original RSS rejection')


def watch_admission(host, path, command, stage, mode):
    value = host.strict_json(path)
    if (value['command'] != command or stage['command'] != command
            or value['own_child_only'] is not True or value['liveness_group_cleanup'] is not True
            or value['rss_cap_mib'] != 512 or type(value['pid']) is not int or value['pid'] <= 0
            or not 0 < value['wall_cap_seconds'] <= stage['wall_cap_seconds'] <= 60
            or not 0 <= value['elapsed_seconds'] < value['wall_cap_seconds']
            or type(value['sampled_peak_rss_mib']) not in (int,float)):
        raise ValueError('actual stage-bound original own-child guard evidence required')
    if mode == 'positive':
        if (stage['status'] != 'PASS' or value['returncode'] != 0 or value['limit_failure'] is not None
                or not 0 < value['sampled_peak_rss_mib'] < 512):
            raise ValueError('actual positive child must complete under the original RSS cap')
        host.require(path.parent/'execute.log', stage['log_sha256'])
    elif (stage['status'] != 'FAILED' or value['returncode'] not in (-15,-9)
            or value['limit_failure'] != "RuntimeError('"+OVERSIZE_REASON+"')"
            or value['sampled_peak_rss_mib'] < 512 or stage['error'] != OVERSIZE_REASON):
        raise ValueError('actual touched oversized child must be rejected by the original RSS branch')
    return value


def run_controls(binding, binding_sha):
    started = ENTRY_STARTED
    # Import normally from the reviewed copied runtime. No class/global alias
    # is installed and no existing module binding is replaced.
    import combined_cold_own_rss_host as host
    descriptor = dict(path=str(binding),sha256=binding_sha)
    c, full, b = host.bind_controller(descriptor)
    if str(Path(__file__).resolve()) != b['controls_source']['path']:
        raise ValueError('execute the actual source-bound copied control script')
    roots = b['resource_info']['resource_roots']
    if type(roots) is not list or any(type(p) is not str for p in roots):
        raise ValueError('actual declared history roots must retain original string ABI')
    # Use the actual unchanged cold controller callsite and its real lazy
    # factory class, not a separately created class from the same source.
    resources = c.resource_monitor(b['resource_info'])
    resource_source = host.resource_provenance(resources,c,b)
    before = resources.check()
    if (before['artifact_bytes'] + 64*2**20 > 96*2**30
            or before['disk_free_bytes'] - 64*2**20 < 8*2**30):
        raise ValueError('actual original control reservation no longer fits')
    root = Path(b['work_root'])/'binding_controls'
    if os.path.lexists(root):
        raise ValueError('permanent exclusive actual new binding-control attempt already exists')
    root.mkdir()
    write_once(root/'claim.json',dict(schema=host.CONTROL_SCHEMA,pid=os.getpid(),binding=descriptor,
                                    started_unix=time.time(),retries=0,scientific_qualification=False))
    executor = full.OwnRSSSerialExecutor(Path(b['work_root']),120,'binding_controls',resources)
    executor.deadline = min(executor.deadline,started+120)
    if (executor.records != [] or executor.bounded.__file__ != b['bounded_helper']['path']
            or host.digest(host.require(executor.bounded.__file__)) != host.BOUNDED_SHA):
        raise ValueError('real inherited constructor did not load its original pinned local helper')
    bounded_identity = host.bounded_helper_provenance(executor,b)
    observations = []
    try:
        for mode in ('positive','oversize'):
            directory = root/mode
            directory.mkdir()
            command = [b['producer_environment']['executable'],b['controls_source']['path'],'fixture',mode]
            unexpected = None
            try:
                text = executor.execute(directory,'execute',command,60,
                                        POSITIVE_MARKER if mode=='positive' else None)
                if mode=='oversize':
                    raise ValueError('oversize command returned without original RSS cap rejection')
                if POSITIVE_MARKER not in text.splitlines():
                    raise ValueError('actual positive control marker missing')
            except RuntimeError as error:
                if mode!='oversize' or str(error)!=OVERSIZE_REASON:
                    raise
                unexpected = str(error)
            stage = executor.records[-1]
            watch_path = directory/'execute.watchdog.json'
            watch = watch_admission(host,watch_path,command,stage,mode)
            # This is an actual no-signal liveness observation after the
            # original bounded group cleanup, not a static True assertion.
            if executor.bounded.process_group_exists(watch['pid']):
                raise ValueError('actual controlled own group remains live after original cleanup')
            log_path = directory/'execute.log'
            lines = host.require(log_path).read_text().splitlines()
            if not lines:
                raise ValueError('retain actual raw child allocation intent')
            allocation = json.loads(lines[0])
            expected_bytes = 16*2**20 if mode=='positive' else OVERSIZE_BYTES
            if allocation != dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,
                                  pid=watch['pid'],requested_bytes=expected_bytes):
                raise ValueError('actual child PID/allocation command identity differs')
            observations.append(dict(mode=mode,command=command,watch=watch,watchdog=host.pin(watch_path),
                                     raw_log=host.pin(log_path),actual_group_no_longer_live=True,
                                     actual_expected_rejection=unexpected))
        source_identity = host.source_mro_proof(c,full,b)
        host.binding_admission(descriptor)
        host.resource_provenance(resources,c,b)
        snapshot = resources.check()
        if time.monotonic()-started >= 120 or host.control_archive_bytes(b) >= 64*2**20:
            raise ValueError('actual complete binding-control reservation/time exhausted')
        result = dict(schema=host.CONTROL_SCHEMA,classification='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY',
            binding=descriptor,caps=host.CAPS,positive_completed=True,actual_oversize_rejected=True,
            own_children_no_longer_live=True,source_identity=source_identity,actual_resource_class=resource_source,
            actual_bounded_helper=bounded_identity,
            observations=observations,actual_resource_snapshot=snapshot,elapsed_before_closeout=time.monotonic()-started,
            scientific_qualification=False,Dragon_started=False,transport_started=False,
            new_assembly_or_linear_solve=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        write_once(root/'result.json',result)
        namespace = host.control_namespace(root)
        write_once(root/'seal.json',dict(schema=host.SEAL_SCHEMA,files=namespace['files'],
                                      namespace_directories=namespace['directories']))
        host.binding_admission(descriptor)
        actual_resources = resources.check()
        elapsed = time.monotonic()-started
        actual_bytes = host.control_archive_bytes(b)
        if elapsed >= 120 or actual_bytes >= 64*2**20:
            raise ValueError('actual all-closeout original control caps exceeded')
        return dict(result=result,actual_tail_check='PASS',actual_elapsed_seconds=elapsed,
                    actual_archive_bytes=actual_bytes,actual_resources=actual_resources)
    except BaseException as error:
        write_once(root/'failure.json',dict(schema=host.CONTROL_SCHEMA,classification='FAILED_NEW_BINDING_CONTROLS_NO_RETRY',
            error=repr(error),scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,
            actual_elapsed_seconds=time.monotonic()-started))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command',required=True)
    child = subs.add_parser('fixture');child.add_argument('mode',choices=('positive','oversize'))
    run = subs.add_parser('run-controls')
    run.add_argument('--binding',type=Path,required=True);run.add_argument('--binding-sha256',required=True)
    args = parser.parse_args()
    if args.command == 'fixture':
        fixture(args.mode)
    else:
        print(json.dumps(run_controls(args.binding,args.binding_sha256),sort_keys=True,indent=2,allow_nan=False))


if __name__ == '__main__':
    main()

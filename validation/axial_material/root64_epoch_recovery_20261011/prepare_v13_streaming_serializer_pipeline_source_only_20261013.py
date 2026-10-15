"""Freeze the original fifty-stage pipeline with the reviewed serializer bundle.

Source preparation only: no import of candidate code, compiler, or business child.
All predecessor dependencies remain real, immutable historical authorities.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import time

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD = REC/'aaa_three_plane_streaming_pipeline_source_v12'
NEW = REC/'aaa_three_plane_streaming_pipeline_source_v13'
BUNDLE = REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'
OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13')
START = time.monotonic()
PINS = {}

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def identity(path):
    s = Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path, wanted=None):
    path = Path(path); before = identity(path)
    need(stat.S_ISREG(before[2]) and not any(p.is_symlink() for p in (path,*path.parents)), 'literal regular Source/input')
    with path.open('rb') as f:
        s = os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before, 'opened all7')
        sha = hashlib.file_digest(f,'sha256').hexdigest(); s = os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before == identity(path), 'fullEOF and after all7')
    result = dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)
    need(wanted is None or result == wanted, 'exact selected fullpin: '+str(path))
    need(str(path) not in PINS or PINS[str(path)] == result, 'one consistent pin')
    PINS[str(path)] = result
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 512*2**20 and time.monotonic()-START < 1800, 'original Source SELF/whole caps')
    return result

def read(path, wanted=None):
    p = pin(path,wanted); raw = Path(path).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == p['sha256'] and identity(path) == p['identity'], 'exact metadata read')
    return json.loads(raw),p

def save(path, raw):
    fd = os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())

def write(path, value):
    save(path,(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--independent-review-summary',required=True)
    p.add_argument('--independent-review-sha256',required=True)
    p.add_argument('--independent-review-seven-id',required=True)
    p.add_argument('--independent-review-status',required=True)
    a = p.parse_args()
    seven = json.loads(a.independent_review_seven_id)
    wanted = dict(path=a.independent_review_summary,sha256=a.independent_review_sha256,size_bytes=seven[4],identity=seven)
    peer,peerpin = read(wanted['path'],wanted)
    need(peer.get('status') == a.independent_review_status == 'PASS_FROZEN_SOURCE_AND_TWO_ACTUAL_FINITE_PROOFS_ONLY_READY_FOR_V13_SOURCE_PREPARATION' and not peer.get('failure'), 'exact actual independent finite PASS')
    bundle,bp = read(BUNDLE/'COMPLETE_SERIALIZER_BUNDLE_SOURCE_FREEZE.json')
    need(bp['sha256'] == '986cc915dc026f85b35101d3716969e47b643ee31b0b115f75d40efd4baa7194', 'actual final serializer freeze')
    need(bundle['source_writers_stopped'] and bundle['source_rebound_serializer_only'] and bundle['all45_original_complete_JSON_bytes_equal'] and bundle['finite_guard_dummy_closed0'], 'closed finite Source proof')
    need(bundle['memory_repair_full_pipeline_proven'] is False and bundle['complete_business_initial_fresh_reserve_bytes'] == 2*2**30, 'finite does not qualify original business')
    need(peer['source_freeze_pin'] == bp and peer['selected_derived_source_pins'] == bundle['selected_derived_source_pins'], 'peer actually reviewed this entire selected bundle')
    need(peer['actual_canonical_report_pin'] == bundle['closed_actual_finite_report_pins']['canonical'] and peer['actual_guard_report_pin'] == bundle['closed_actual_finite_report_pins']['guard'], 'peer exact two actual proofs')
    need(peer['actual_two_process_true_tool_returns_pin'] == bundle['actual_true_tool_returns_pin'] and peer['actual_finite_argv_pin'] == bundle['actual_finite_argv_pin'], 'peer exact actual exits and commands')
    pt,ptp = read(Path(peerpin['path']).parent/'TRUE_TOOL_RETURNS.json')
    need(pt['original_integer_exit_code'] == 0 and type(pt['original_integer_exit_code']) is int and pt['observed_closed'] is True and pt['genuine_actual_review_tool_return']['exit_code'] == 0 and json.loads(pt['genuine_actual_review_tool_return']['output'])['review_pin'] == peerpin, 'genuine independent closed0 tied to this exact review')
    old,oldpin = read(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
    need(oldpin == bundle['original_v12_host_source_freeze_pin'] and old['dependencies'] == bundle['original_v12_dependencies_as_unchanged_authority_and_provenance'], 'entire original319 dependencies unchanged')
    cli,clip = read(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V12_ARGV_20261013.json')
    for row in old['dependencies']+[old['host_source']]+list(cli['mandatory_external_bindings'].values()):
        pin(row['path'],row)
    extra = [bp,peerpin,ptp,oldpin,old['host_source'],clip,bundle['complete_byte_inverse_pin'],bundle['actual_true_tool_returns_pin'],bundle['actual_finite_argv_pin'],bundle['final_report_pin']]
    extra += list(bundle['selected_derived_source_pins'].values())+bundle['original_source_lineage_pins']+list(bundle['closed_actual_finite_report_pins'].values())+bundle['finite_fixture_source_and_first_failure_pins']+bundle['historical_v12_failure_and_root_source_review_pins']
    for row in extra:
        pin(row['path'],row)
    need(not NEW.exists() and not NEW.is_symlink() and not OUT.exists() and not OUT.is_symlink(), 'fresh immutable Source and business namespaces')
    original = Path(old['host_source']['path']).read_text()
    changes = [
        dict(old_block="COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'",new_block='COMMON=Path('+repr(bundle['selected_derived_source_pins']['common']['path'])+')'),
        dict(old_block="OUT=c.ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12'",new_block='OUT=Path('+repr(str(OUT))+')'),
        dict(old_block='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V12',new_block='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V13')]
    candidate = original
    for change in changes:
        need(candidate.count(change['old_block']) == 1, 'one exact integration literal')
        candidate = candidate.replace(change['old_block'],change['new_block'],1)
    restored = candidate
    for change in reversed(changes):
        need(restored.count(change['new_block']) == 1, 'one reverse integration literal')
        restored = restored.replace(change['new_block'],change['old_block'],1)
    need(restored == original, 'entire v12 HOST byte inverse')
    ast.parse(candidate)
    NEW.mkdir()
    save(NEW/'run_actual_three_plane_pipeline.py',candidate.encode())
    for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):
        save(NEW/name,(OLD/name).read_bytes())
    alias,_ = read(OLD/'DIRECT_ALIAS_ENTRY_BINDING.json')
    need(alias['new_probe_source'] == str(OLD/'direct_alias_entry_controls.f90'), 'original actual alias Source')
    alias['new_probe_source'] = str(NEW/'direct_alias_entry_controls.f90')
    write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',alias)
    interface,_ = read(OLD/'DECLARED_EXECUTION_INTERFACE.json')
    interface.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V13',host_source=str(NEW/'run_actual_three_plane_pipeline.py'),output_root=str(OUT),Source_revision_scope='selected streaming complete-ledger serializer bundle only; original50 unchanged',parent_memory_repair_claimed=False)
    write(NEW/'DECLARED_EXECUTION_INTERFACE.json',interface)
    hostpin = pin(NEW/'run_actual_three_plane_pipeline.py')
    inverse = dict(schema='COMPLETE_V12_TO_V13_STREAMING_SERIALIZER_INTEGRATION_BYTE_INVERSE_V1',old_host_source_pin=old['host_source'],new_host_source_pin=hostpin,exact_ordered_changes=changes,ENTIRE_v12_host_inverse_byte_equal=True,three_helpers_whole_bytes_unchanged=True,source_rebound_serializer_only=True,original50_17positive_33negative_math_and_caps_unchanged=True,original_business_initial_fresh_reserve_bytes=2*2**30,serializer_bundle_pin=bp,independent_finite_review_pin=peerpin,actual_pipeline_executed=False,memory_repair_proven=False)
    write(NEW/'COMPLETE_V12_TO_V13_SERIALIZER_BUNDLE_INTEGRATION_BYTE_INVERSE.json',inverse)
    local = [pin(x) for x in sorted(NEW.iterdir())]
    table = {row['path']:row for row in old['dependencies']}
    for row in extra+local+[pin(__file__)]:
        need(row['path'] not in table or table[row['path']] == row, 'new unique dependency has no conflict')
        table[row['path']] = row
    hf = copy.deepcopy(old)
    hf.update(schema='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V13',host_source=hostpin,dependencies=list(table.values()),predecessor_host_freeze=oldpin,Source_revision_scope='only complete ledger serializer through honestly selected derived four-source import bundle; original50 retained',source_rebound_serializer_only=True,selected_serializer_bundle_pin=bp,selected_derived_guard_source_pins=bundle['selected_derived_source_pins'],original_Common_freeze_and_Bind_are_unchanged_science_authority_not_new_Source_freeze=True,complete_original_v12_dependency_rows_retained=len(old['dependencies']),complete_V12_to_V13_byte_inverse_pin=pin(NEW/'COMPLETE_V12_TO_V13_SERIALIZER_BUNDLE_INTEGRATION_BYTE_INVERSE.json'),independent_closed_finite_bundle_review_pin=peerpin,original_business_initial_fresh_reserve_bytes=2*2**30,prepared_only=True,actual_pipeline_executed=False,actual_pipeline_executed_by_this_prepare=False,actual_qualified_numeric_pipeline=False,physics_qualification=False,memory_repair_claimed=False,memory_repair_full_pipeline_proven=False,no_prefilled_actual_success=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    for row in hf['dependencies']+[hostpin]:
        pin(row['path'],row)
    write(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',hf); hp = pin(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
    freshcli = copy.deepcopy(cli)
    argv = list(cli['argv']); argv[argv.index(str(OLD/'run_actual_three_plane_pipeline.py'))] = str(NEW/'run_actual_three_plane_pipeline.py')
    for suffix,value in [('summary',hp['path']),('sha256',hp['sha256']),('seven-id',json.dumps(hp['identity'],separators=(',',':')))]:
        argv[argv.index('--host-freeze-'+suffix)+1] = value
    freshcli['mandatory_external_bindings']['host-freeze'] = hp
    freshcli.update(schema='ROOT_REVIEWABLE_EXACT_ACTUAL_PIPELINE_V13_STREAMING_SERIALIZER_BUNDLE_ARGV_V1',argv=argv,Source_revision_scope=hf['Source_revision_scope'],serializer_bundle_pin=bp,independent_closed_finite_bundle_review_pin=peerpin,actual_pipeline_executed=False,prepared_only=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    for key,row in cli['mandatory_external_bindings'].items():
        need(key == 'host-freeze' or freshcli['mandatory_external_bindings'][key] == row, 'all six actual external parameters unchanged')
    cp = REC/'ROOT_EXACT_ACTUAL_PIPELINE_V13_ARGV_20261013.json'; write(cp,freshcli); cpp = pin(cp)
    handoff = dict(schema='FINAL_V13_STREAMING_SERIALIZER_BUNDLE_SOURCE_ONLY_HANDOFF_V1',status='PREPARED_ONLY_REQUIRES_ROOT_AND_PEER_SOURCE_REVIEW_AND_SPACE_ADMISSION',host_freeze_pin=hp,CLI_pin=cpp,inverse_pin=hf['complete_V12_to_V13_byte_inverse_pin'],serializer_bundle_pin=bp,independent_finite_review_pin=peerpin,dependencies=len(hf['dependencies']),fullEOF_files=len(PINS),Source_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,actual_pipeline_executed=False,no_future_success_prefilled=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    hand = REC/'FINAL_PIPELINE_V13_STREAMING_SERIALIZER_SOURCE_HANDOFF_20261013.json'; write(hand,handoff)
    print(json.dumps(dict(handoff_pin=pin(hand),host_freeze_pin=hp,CLI_pin=cpp,dependency_count=len(hf['dependencies']),Source_peak_bytes=handoff['Source_peak_bytes']),allow_nan=False))

if __name__ == '__main__':
    main()

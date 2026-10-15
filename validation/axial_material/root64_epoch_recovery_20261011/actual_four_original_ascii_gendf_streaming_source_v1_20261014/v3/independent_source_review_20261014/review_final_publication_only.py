"""Read-only final Source publication integration review; no science execution."""
import json
import os
import shutil
import stat
from pathlib import Path
from review_source_only import BASE, CAPS, FLAGS, current, full, new, pin, read, require


def main():
    ready_pin = pin(BASE / 'SOURCE_REVIEW_READY.json')
    ready = read(ready_pin)
    review_pin = pin(BASE / 'independent_source_review_20261014/REVIEW.json')
    review_tools_pin = pin(BASE / 'independent_source_review_20261014/ACTUAL_REVIEW_TRUE_TOOL_RETURNS.json')
    generation_pin = pin(BASE / 'ACTUAL_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
    original_review = read(review_pin)
    for p in original_review['original_dynamic_guard_Source_pins'] + original_review['original_live_guard_admission_full_pins']:
        full(p)
    p_sf = pin(BASE / 'FINAL_SOURCE_FREEZE.json')
    p_hf = pin(BASE / 'FINAL_HOST_FREEZE.json')
    p_cli = pin(BASE / 'FINAL_ROOT_REVIEWABLE_CLI.json')
    p_receipt = pin(BASE / 'FINAL_PUBLICATION_RECEIPT.json')
    sf, hf, cli, receipt = [read(p) for p in (p_sf, p_hf, p_cli, p_receipt)]
    plan = read(ready['control_plan_pin'])
    require(sf['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_SOURCE_ONLY_FREEZE_V1'
            and hf['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_HOST_SOURCE_ONLY_FREEZE_V1'
            and cli['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_REVIEWABLE_CLI_SOURCE_ONLY_V1'
            and receipt['schema'] == 'ROOT_ONCE_FOUR_ORIGINAL_ASCII_SOURCE_PUBLICATION_ONLY_V1', 'exact final schemas')
    require(sf['source_only'] is True and hf['source_only'] is True
            and sf['candidate_executed'] is False and hf['candidate_executed'] is False
            and all(d[k] is False for d in (sf, hf, cli, receipt) for k in FLAGS), 'final Source-only false flags')
    expected_proof = dict(actual_precise_retirement_receipt_pin=plan['actual_precise_retirement_receipt_pin'],
                          peer_review_pin=review_pin, peer_true_tools_pin=review_tools_pin,
                          Source_generation_true_tools_pin=generation_pin, selected_Source_only_ready_pin=ready_pin,
                          root_same_round_Source_only_publication=True, business_executed=False,
                          compiler_executed=False, numerical_executed=False, files_deleted=False)
    require(sf['Root_same_round_peer_and_generation_proof'] == hf['Root_same_round_peer_and_generation_proof']
            == cli['Root_same_round_peer_and_generation_proof'] == receipt['peer_and_generation_proof'] == expected_proof,
            'same exact peer/generation/retirement/ready fullPF integration')
    require(sf['control_plan_pin'] == ready['control_plan_pin']
            and sf['complete_source_file_pins'] == ready['complete_source_file_pins'] + [ready_pin]
            and hf['selected_source_freeze_pin'] == p_sf
            and hf['host_source_pin'] == ready['host_source_pin']
            and sf['original_caps'] == hf['original_caps'] == CAPS
            and cli['source_freeze_pin'] == p_sf and cli['host_freeze_pin'] == p_hf
            and receipt['final_source_freeze_pin'] == p_sf and receipt['final_host_freeze_pin'] == p_hf
            and receipt['final_CLI_pin'] == p_cli, 'final SF/HF/CLI receipt exactPF bindings')
    require(receipt['selected_Source_pins'] == ready['selected_Source_pins'] + [ready_pin, generation_pin], 'all same selected original SourcePF')
    for p in ready['dependencies'] + sf['complete_source_file_pins'] + hf['dependencies'] + hf['explicit_cumulative_metadata_file_pins']:
        full(p)
    required_tail = [ready['host_source_pin']['path'], '--source-freeze-summary', p_sf['path'], '--source-freeze-sha256',
                     p_sf['sha256'], '--source-freeze-seven-id', json.dumps(p_sf['identity'], separators=(',', ':')),
                     '--host-freeze-summary', p_hf['path'], '--host-freeze-sha256', p_hf['sha256'], '--host-freeze-seven-id',
                     json.dumps(p_hf['identity'], separators=(',', ':'))]
    require(cli['argv'] == ready['original_complete_ENV_Python_B_prefix'] + required_tail
            and cli['planned_actual_output_root'] == plan['planned_actual_output_root'], 'exact reviewable once host argv')
    actual_argv_pin = pin(BASE / 'ROOT_EXACT_ACTUAL24_ARGV.json')
    require(read(actual_argv_pin) == cli['argv'] and len(cli['argv']) == 24, 'Root retained exact original24 argv')
    publication_tools_pin = pin(BASE / 'ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json')
    publication_tools = read(publication_tools_pin)
    pt = publication_tools['actual_publication_return']
    require(type(pt['exit_code']) is int and pt['exit_code'] == 0 and pt.get('session_id') is None
            and json.loads(pt['output'].strip().splitlines()[-1])['receipt_pin'] == p_receipt,
            'actual Root final once publication typed closed0 stdout exactPF')
    require(not os.path.lexists(plan['planned_actual_output_root']), 'once actual business OUT still absent')
    def scan(roots):
        total = count = 0
        stack = [Path(q) for q in roots]
        while stack:
            q = stack.pop()
            require(not any(p.is_symlink() for p in (q, *q.parents)), 'no root/ancestor alias')
            try:
                fd = os.open(q, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            except FileNotFoundError:
                continue
            try:
                with os.scandir(fd) as entries:
                    for e in entries:
                        try:
                            s = e.stat(follow_symlinks=False)
                        except FileNotFoundError:
                            continue
                        if stat.S_ISDIR(s.st_mode):
                            stack.append(q / e.name)
                        elif stat.S_ISREG(s.st_mode):
                            total += s.st_size
                            count += 1
            finally:
                os.close(fd)
        return dict(artifact_bytes=total, regular_files=count)
    joint = scan(plan['complete_joint_roots'])
    extra = sum(p['size_bytes'] for p in hf['explicit_cumulative_metadata_file_pins']
                if not any(Path(p['path']).is_relative_to(Path(q)) for q in plan['complete_joint_roots']))
    artifact_root = Path('/Users/wen/spot/validation/artifacts')
    history_roots = sorted(set(str(p) for p in artifact_root.glob('axial-material-*')) | {plan['planned_actual_output_root']})
    history = scan(history_roots)
    free = shutil.disk_usage(artifact_root).free
    require(joint['artifact_bytes'] + extra < CAPS['fresh_bytes']
            and history['artifact_bytes'] + CAPS['cold_reserve_bytes'] + CAPS['metadata_reserve_bytes'] + CAPS['fresh_bytes'] < CAPS['history_bytes']
            and free - CAPS['cold_reserve_bytes'] - CAPS['fresh_bytes'] >= CAPS['free_floor_bytes'],
            'current43 joint2GiB, original dynamic axial history96GiB, cold/meta/fresh reserve and free8GiB')
    tools = read(review_tools_pin)
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int
            and tools['original_integer_exit_code'] == 0
            and type(tools['actual_review_return']['exit_code']) is int and tools['actual_review_return']['exit_code'] == 0
            and tools['actual_review_return'].get('session_id') is None
            and json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin'] == review_pin,
            'retained actual peer closed0/stdout same reviewPF')
    for row in plan['inputs']:
        current(row['gzip_primary_current_full_pin'])
    target = BASE / 'independent_source_review_20261014/FINAL_PUBLICATION_LIGHT_REVIEW.json'
    result = dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_FINAL_PUBLICATION_METADATA_REVIEW_V1',
                  status='PASS_FINAL_SOURCE_PUBLICATION_LIGHT_FULL_EOF_CURRENT7_EXACT_ARGV',
                  source_only=True, failure=None, final_source_freeze_pin=p_sf, final_host_freeze_pin=p_hf,
                  final_CLI_pin=p_cli, Root_publication_receipt_pin=p_receipt,
                  peer_generation_retirement_ready_proof=expected_proof,
                  selected_Source_pins=receipt['selected_Source_pins'],
                  original_caps=CAPS, complete_joint_roots=plan['complete_joint_roots'],
                  final_argv=cli['argv'], final_dependency_count=len(hf['dependencies']),
                  final_explicit_cumulative_metadata_count=len(hf['explicit_cumulative_metadata_file_pins']),
                  Root_actual_publication_tools_pin=publication_tools_pin, Root_exact_actual24_argv_pin=actual_argv_pin,
                  current_complete_joint_stat_snapshot=joint, explicit_external_metadata_bytes=extra,
                  current_original_dynamic_history_stat_snapshot=history, current_filesystem_free_bytes=free,
                  actual_business_output_namespace_absent=True,
                  full_EOF_current7_metadata_and_Source_verified=True,
                  gzip_payload_read=False, sciencebody_imported_or_executed=False, **FLAGS)
    new(target, result)
    print(json.dumps(dict(status=result['status'], review_pin=pin(target), **FLAGS)), flush=True)


if __name__ == '__main__':
    main()

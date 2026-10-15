"""Read-only qualification of the isolated normalized REAL64 A snapshot."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from analyze_r64_snapshot import analyze as analyze_snapshot
from analyze_r64_tracking_moments import analyze as analyze_moments
from analyze_r64_trace import analyze as analyze_trace
from check_r64_audit_rejections import check as check_snapshot_rejections
from check_r64_normalization_rejections import check as check_normalization_rejections
from production_runner import ROOT, check_dragon_log

ART = ROOT / 'validation/artifacts'
TRIALS = {
    'inactive_link': ('pjj64', '72c31825bbdb3f80e4a807c9850ee6f6bd9bffc2a365652289c841a49616020f'),
    'checked_psj_rejection': ('pjj64-linkfix', '4cb96506a56e440846943ed45d3518e644d4f5e9aebba011f50d9783a10a7b1b'),
    'checked_ilu_rejection': ('pjj64-workspacefix', 'abac10504412c0e506e6c6181fbc658d4aca838fb8f901ce0a77631e2e802548'),
    'pjj64_only': ('pjj64-ilufix', '2e4413bf91a583501ded51df9f1e5fb3b20ad46c08dd722ce234e1ae0e515aba'),
    'matched_coefficients': ('kernel-consistency', 'f79713e8de00a50c3d6fceb808e10413b0d544fdfb20a0f1b72bc4bf17760751'),
    'readonly_track_rejection': ('track-normalization', 'b4e7d76b2c85f9c08724d31d0f52c49ad1422c28f7fb6bf17aa2d71c03812bfe'),
    'normalized': ('system-normalization', '1795608b8ab463955311cf3c340d5ec7d9054cf658af5b4e7c80a132cbee61b4'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify():
    from verify_r64_snapshot_diagnostics import verify as verify_previous
    previous = verify_previous()
    require(previous['classification'] == 'R64_SNAPSHOT_DIAGNOSTICS_VERIFIED', 'prior diagnostics changed')
    require(not previous['snapshot_A_binary64_qualified'], 'historical failed audit changed')
    seal = ART / 'axial-material-r64-progress-20261003/checkpoint.sha256'
    require(digest(seal) == '983375ad62e00f867fc4c878606b8ac4df7b79e6861bdb7862780957cb3e1e7b', 'historical seal changed')
    for line in seal.read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require(digest(seal.parent / name) == wanted, 'historical checkpoint file changed: ' + name)
    evidence = {str(seal): digest(seal)}
    runs = {}
    wall = 0.0
    common = previous['material_geometry_and_track_identical']
    for label, (stem, wanted) in TRIALS.items():
        work = ART / ('axial-material-r64-' + stem + '-20261003')
        require(digest(work / 'execution.json') == wanted, 'execution changed: ' + label)
        manifest = json.loads((work / 'execution.json').read_text())
        require(manifest['wall_seconds'] == 600 and manifest['automatic_retries'] == 0, 'budget changed')
        for name, expected in manifest['files'].items():
            require(digest(Path(name)) == expected, 'frozen input changed: ' + name)
        status = json.loads((work / 'run_status.json').read_text())
        require(status['frozen_inputs_unchanged'] and not status['scientific_accuracy_accepted'], 'run scope changed')
        for name, expected in status['outputs'].items():
            require(digest(work / 'A' / name) == expected, 'output changed: ' + label + '/' + name)
        require({name: digest(work / 'A' / name) for name in common} == common, 'physical input or track differs')
        wall += status['elapsed_seconds']
        log = (work / 'A/solve.log').read_text()
        run = dict(classification=status['classification'], elapsed_seconds=status['elapsed_seconds'])
        rejected = {
            'checked_psj_rejection': "actual argument 'psj' is not allocated",
            'checked_ilu_rejection': "actual argument 'lucf' is not allocated",
            'readonly_track_rejection': "THE OBJECT 'TRACK' IS OPEN IN READ-ONLY MODE",
        }
        if label in rejected:
            require(status['classification'] == 'FAILED_NO_RETRY' and rejected[label] in log, 'rejection changed')
            require(not (work / 'A/snapshot_A.xsm').exists(), 'rejection published snapshot')
        else:
            require(status['classification'] == 'R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT', 'snapshot did not complete')
            check_dragon_log(log, 'AXMAT-SNAPSHOT-A-COMPLETE')
            trace = analyze_trace(log)
            require(trace['strict_terminal_marker'] and trace['snapshot_marker_count'] == 1, 'terminal changed')
            require(not trace['incomplete_final_radial_call'], 'incomplete radial call')
            require(trace['maximum_printed_inner_residual'] <= 2.5000005e-10, 'radial work target not met')
            run['trace'] = trace
            audit = work / 'audit_initialized'
            audited = json.loads((audit / 'run_status.json').read_text())
            require(audited['frozen_inputs_unchanged'], 'audit input changed')
            require(digest(audit / 'protocol.json') == audited['protocol_sha256'], 'audit protocol changed')
            for name, expected in json.loads((audit / 'protocol.json').read_text())['files'].items():
                require(digest(Path(name)) == expected, 'audit frozen input changed: ' + name)
            for name, expected in audited['outputs'].items():
                require(digest(audit / name) == expected, 'audit output changed: ' + name)
            wall += audited['elapsed_seconds']
            if label == 'inactive_link':
                require(audited['classification'] == 'AUDIT_FAILED_NO_RETRY', 'missing-record rejection changed')
                require('record mismatch: PJJ64$MCCG' in (audit / 'audit.log').read_text(), 'inactive link falsely accepted')
                require(digest(work / 'A/snapshot_A.xsm') ==
                    digest(ART / 'axial-material-r64-rebalance-inputfix-20261003/A/snapshot_A.xsm'), 'inactive candidate changed')
                run['scientific_pjj_contrast_usable'] = False
            else:
                measured = analyze_snapshot(audit / 'audit.bin')
                require(measured == json.loads((audit / 'observations.json').read_text()), 'terminal analysis differs')
                expected = 'R64_SNAPSHOT_TERMINAL_AUDIT_PASS' if label == 'normalized' else 'R64_SNAPSHOT_TERMINAL_AUDIT_FAIL'
                require(measured['classification'] == audited['classification'] == expected, 'audit outcome differs')
                require(audited['snapshot_qualified'] == (label == 'normalized'), 'qualification scope differs')
                pjj = (audit / 'pjj.bin').read_bytes()
                require(len(pjj) == 35528 and np.frombuffer(pjj, '<i4', 2).tolist() == [8, 370], 'bad PJJ export')
                authority = np.frombuffer(pjj, '<f8', 2960, 8)
                mirror = np.frombuffer(pjj, '<f4', 2960, 23688)
                require(np.isfinite(authority).all() and np.all(authority >= 0), 'invalid PJJ authority')
                require(np.array_equal(authority.astype('<f4').view('<u4'), mirror.view('<u4')), 'PJJ mirror differs')
                run['terminal_audit'] = {k: v for k, v in measured.items() if k != 'groups'}
                run['failing_groups'] = [g['group'] for g in measured['groups'] if g['full_image_defect'] >= measured['terminal_threshold']]
            for p in audit.iterdir():
                if p.is_file():
                    evidence[str(p)] = digest(p)
        for p in (work / 'execution.json', work / 'protocol.json', work / 'run_status.json', work / 'A/solve.log'):
            evidence[str(p)] = digest(p)
        runs[label] = run
    final = ART / 'axial-material-r64-system-normalization-20261003'
    audit = final / 'audit_initialized'
    moments_dir = final / 'tracking_moments'
    for stem in ('kernel-consistency', 'system-normalization'):
        p = ART / ('axial-material-r64-' + stem + '-20261003') / 'tracking_moments'
        status = json.loads((p / 'run_status.json').read_text())
        require(status['frozen_inputs_unchanged'], 'tracking export changed')
        require(digest(p / 'protocol.json') == status['protocol_sha256'], 'tracking export protocol changed')
        for name, wanted in json.loads((p / 'protocol.json').read_text())['files'].items():
            require(digest(Path(name)) == wanted, 'tracking export input changed')
        for name, wanted in status['outputs'].items():
            require(digest(p / name) == wanted, 'tracking export output changed')
        for path in p.iterdir():
            if path.is_file():
                evidence[str(path)] = digest(path)
    require(digest(moments_dir / 'moments.bin') ==
        '05b6d362ebc70630110b8b81b577b930ab33136ef647f6dc7df043eeacce6a89', 'quadrature/geometry owner changed')
    normalization = analyze_moments(final / 'A/radial_track.bin', moments_dir / 'moments.bin', audit / 'volume64.bin')
    require(normalization == json.loads((audit / 'volume_normalization_check.json').read_text()), 'normalization replay differs')
    negatives = check_snapshot_rejections(audit / 'audit.bin')
    require(negatives == json.loads((audit / 'negative_controls.json').read_text()), 'snapshot rejections differ')
    normalization_negatives = check_normalization_rejections(final / 'A/radial_track.bin', moments_dir / 'moments.bin', audit / 'volume64.bin')
    require(normalization_negatives == json.loads((audit / 'normalization_negative_controls.json').read_text()), 'normalization rejections differ')
    commands = json.loads((final / 'protocol.json').read_text())['build_commands']
    link = next(c for c in commands if c[c.index('-o') + 1] == str(final / 'runtime/Dragon'))
    require(all(link.count(str(final / 'build' / name)) == 1 for name in ('MCGASM.o', 'MCGFST.o', 'MCGDSCA.o')), 'new object omitted')
    require("CALL LCMPUT(IPTRK,'AXMAT-V64'" not in (final / 'build/MCGASM.f').read_text(), 'read-only TRACK mutated')
    require(digest(ROOT / 'bin/Darwin_arm64/Dragon') == '2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db', 'canonical runtime changed')
    source_dir = Path(__file__).parent
    for name in ('verify_r64_normalized_snapshot.py', 'analyze_r64_tracking_moments.py', 'check_r64_normalization_rejections.py'):
        evidence[str(source_dir / name)] = digest(source_dir / name)
    return dict(classification='R64_SNAPSHOT_A_QUALIFIED_OFFLINE_ONLY',
        snapshot_A_binary64_qualified=True, production_qualified=False, aaa_qualified=False,
        aba_started=False, new_ce_accuracy_accepted=False, shared_solver_modified=False,
        prior_failures_and_sealed_checkpoint_preserved=True,
        material_geometry_track_and_quadrature_unchanged=True, physical_inputs=common,
        producer_runtime_sha256=digest(final / 'runtime/Dragon'),
        snapshot_sha256=digest(final / 'A/snapshot_A.xsm'),
        terminal_audit=runs['normalized']['terminal_audit'], normalization=normalization,
        analyzer_negative_controls=negatives, normalization_negative_controls=normalization_negatives,
        runs=runs, new_numerical_wall_seconds_including_rejections=wall,
        total_numerical_wall_seconds=previous['numerical_wall_seconds_including_cleanup'] + wall,
        evidence=evidence,
        limits=['Offline infinite-pin A qualification only; original outer/bare-image gates unchanged.',
            'Existing REBA and 100x tighter radial/thermal work targets remain part of this numerical method.',
            'Matched source-isolation coefficients and track-derived binary64 normalization change numerical coefficient construction, not solely storage precision.',
            'Canonical and coupled production runtimes were not replaced; binary32 mirrors are not certified inner terminals.',
            'B snapshot, explicit producer/ingestion receipts and qualified AAA precede ABA.',
            'Independent coupled reference admission and original D4 CE accuracy remain outstanding.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('runs', 'evidence')}, indent=2))


if __name__ == '__main__':
    main()

"""Read-only replay of the October 3 snapshot residual investigation."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

from analyze_true_residual import analyze

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / 'validation/artifacts'
EXPERIMENTS = {
    'original': ('axial-material-true-residual-probe-20261003', 'ea43f8e16ed9b0dcef0f3b94442f30838a3caaa04e370a9be449c40ebefb23d3'),
    'rhs64': ('axial-material-moc-rhs64-20261003', '075508e12672f6510e21004a0318c9ded178d7754e88977fa57c67975db4b97c'),
    'homogeneous': ('axial-material-moc-homogeneous-20261003', '4579198c38dce1dbbf68f47157293ac05b2c28c3aecd972cab6fbb7e60c86a8f'),
    'homogeneous_single_round': ('axial-material-moc-homogeneous-single-round-20261003', '48ace95ffb553e500ba68dfdce63db669d64a7d72b4e05a6dc9fd5045bfc003c'),
    'verified_restarts': ('axial-material-moc-verified-20261003', '602c763226cb6c88e94ee0386ab4bbcb4b469843286ca90a05398f2fff9764cc'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_manifest(work, expected):
    path = work / 'execution.json'
    require(digest(path) == expected, 'execution identity: ' + str(work))
    manifest = json.loads(path.read_text())
    for name, wanted in manifest['files'].items():
        require(digest(Path(name)) == wanted, 'frozen file changed: ' + name)
    return manifest


def verify():
    require(digest(ROOT / 'src/MCGMRE.f') == 'f29c0325f2dce3a9c2a9bedc9d5b803154445e5b9c1a8382f8c930827c26b7a6', 'shared MCGMRE source changed')
    matrix, evidence, common_inputs, common_source = [], {}, None, None
    total_seconds = 0.0
    for variant, (folder, expected) in EXPERIMENTS.items():
        work = ARTIFACTS / folder
        manifest = check_manifest(work, expected)
        status = json.loads((work / 'run_status.json').read_text())
        require(status['classification'] == 'POSTUPDATE_RESIDUAL_OBSERVATIONS_COMPLETE', 'incomplete probe')
        require(status['frozen_inputs_unchanged'] and not status['snapshot_qualified'], 'wrong probe scope')
        log = work / 'A/probe.log'
        require(digest(log) == status['log_sha256'], 'log changed')
        text = log.read_text()
        recomputed = analyze(text)
        saved = json.loads((work / 'independent_observations.json').read_text())
        for key, value in recomputed.items():
            require(saved[key] == value, 'saved observation differs: ' + key)
        inputs = {name:digest(work / 'A' / name) for name in ('material.xsm', 'geometry.dat', 'snapshot.x2m')}
        sources = []
        for line in text.splitlines():
            if not line.startswith('AXMAT-VECTOR '):
                continue
            fields = line.split()
            sources.append((int(fields[1]), int(fields[2]), float(fields[3])))
            flux = float(fields[4])
            require(struct.unpack('f', struct.pack('f', flux))[0] == flux, 'returned flux not binary32')
        if common_inputs is None:
            common_inputs, common_source = inputs, sources
        require(inputs == common_inputs and sources == common_source, 'contrast input/source differs')
        require(not (work / 'A/snapshot_A.xsm').exists(), 'unexpected snapshot')
        total_seconds += status['elapsed_seconds']
        matrix.append(dict(variant=variant, reported_pass_count=saved['estimated_pass_count'],
            true_pass_count=saved['true_pass_count'], false_acceptance_count=saved['false_acceptance_count'],
            maximum_true_residual=saved['maximum_true_residual'], median_true_residual=saved['median_true_residual'],
            repeat_max_absolute_difference=saved['repeat_max_absolute_difference'],
            returned_vector_gate='PASS' if saved['true_pass_count'] == 370 else 'FAIL',
            snapshot_qualified=False, elapsed_seconds=status['elapsed_seconds']))
        for name in ('execution.json', 'protocol.json', 'run_status.json', 'A/probe.log', 'independent_observations.json', 'build/MCGMRE_probe.f'):
            evidence[str(work / name)] = digest(work / name)
    trace = ARTIFACTS / 'axial-material-snapshot-trace-20261003'
    check_manifest(trace, 'cd0d7ae957c3c293d561b2a8c5fc77d8d26eae855d38874f7d38701c32765ba6')
    trace_status = json.loads((trace / 'run_status.json').read_text())
    require(trace_status['classification'] == 'DIAGNOSTIC_TIME_LIMIT', 'unexpected trace terminal')
    observations = json.loads((trace / 'observations.json').read_text())
    from analyze_snapshot_trace import analyze as analyze_trace
    trace_recomputed = analyze_trace((trace / 'A/snapshot.log').read_text())
    for key, value in trace_recomputed.items():
        require(observations[key] == value, 'trace observation changed: ' + key)
    require(not observations['parser_errors'], 'trace parser error')
    original = json.loads((ARTIFACTS / EXPERIMENTS['original'][0] / 'independent_observations.json').read_text())
    first_groups = observations['calls'][0]['groups']
    require(len(first_groups) == 370, 'incomplete original first call')
    for native, probe in zip(first_groups, original['rows']):
        require(native['group'] == probe['group'] and native['iterations'] == probe['iterations'], 'first-call group/iteration differs')
        require(math.isclose(native['reported_accuracy'], probe['estimated'], rel_tol=5.01e-5), 'first-call printed estimate differs')
    total_seconds += trace_status['stages'][0]['elapsed_seconds']
    for name in ('execution.json', 'run_status.json', 'observations.json', 'A/snapshot.log'):
        evidence[str(trace / name)] = digest(trace / name)
    old = ARTIFACTS / 'axial-material-closeout-20261003'
    require(digest(old / 'result.sha256') == '8c287eb982001e97f5e53b738f9b37338dca95ff88bf30b9e7ef90f0dafa9359', 'prior seal changed')
    for line in (old / 'result.sha256').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require(digest(old / name) == wanted, 'prior closeout file changed')
    return dict(classification='DIAGNOSTIC_EVIDENCE_VERIFIED_PRODUCTION_GATES_NOT_MET',
        scientific_objective_achieved=False, shared_solver_modified=False,
        snapshot_qualified=False, aaa_qualified=False, aba_started=False, formal_ce_started=False,
        variants=matrix, common_inputs=common_inputs, source_vectors_equal=True,
        original_first_call_printed_iteration_and_estimate_match=True,
        trace=dict(started_calls=observations['all_started_calls'],
            calls_with_summaries=observations['calls_with_group_summaries'],
            group_records=observations['group_summaries'],
            reported_above_epsi=len(observations['printed_group_residuals_above_epsi']),
            max_reported_group_iterations=observations['maximum_reported_group_iterations'],
            minimum_printed_outer_flux_change=observations['minimum_printed_outer_flux_change'],
            last_outer=observations['outer'][-1]),
        numerical_wall_seconds_including_trace_cleanup=total_seconds,
        prior_closeout_seal_unchanged=True, evidence=evidence,
        scope='Observation integrity and same-input arithmetic contrasts. No proof of a unique outer-stagnation cause or a hard precision floor. No snapshot, coupled convergence, rank accuracy, CE accuracy or release acceptance.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'evidence'}, indent=2))


if __name__ == '__main__':
    main()

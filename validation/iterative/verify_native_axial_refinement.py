#!/usr/bin/env python3
"""Verify refinement replay and isolation from ten prior sealed artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

PRIOR=['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
       'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
       'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
       'exchange-pod-projection-20260928','native-radial-response-20260928',
       'native-multigroup-pod-20260928','native-axial-coupling-20260928']


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    counts=dict(byte_identical_analysis_files=0,exactly_equal_arrays=0,protected_files=0,
                source_inputs=0,prior_manifest_entries=0,prior_artifacts=len(PRIOR))
    for path in sorted((a/'analysis').iterdir()):
        other=a/'replay/analysis'/path.name
        assert digest(path)==digest(other),f'replay mismatch: {path.name}'
        counts['byte_identical_analysis_files']+=1
        if path.suffix=='.npz':
            x=np.load(path);y=np.load(other);assert x.files==y.files
            for name in x.files:
                np.testing.assert_array_equal(x[name],y[name]);counts['exactly_equal_arrays']+=1
    for manifest,key in [('protected_inputs_before.json','protected_files'),('inputs.json','source_inputs')]:
        for filename,expected in json.loads((a/manifest).read_text()).items():
            assert digest(root/filename)==expected,f'protected/source input changed: {filename}'
            counts[key]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected,path=line.split(maxsplit=1)
            assert digest(folder/path)==expected,f'prior evidence changed: {name}/{path}'
            counts['prior_manifest_entries']+=1
    for source in (a/'build').glob('*.py'):
        assert digest(source)==digest(root/'validation/iterative'/source.name),f'archived source differs: {source.name}'
    for label in ['source_tests','archived_tests']:
        report=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 12 tests' in report and '\nOK\n' in report and 'skipped=' not in report
    result=json.loads((a/'analysis/result.json').read_text())
    assert result['mesh_gate_passed'] is False
    assert len(result['meshes'])==7
    assert all(r['negative_scalar_count']==0 for r in result['meshes'])
    assert all(r['failed_gates']==['nonpositive_outgoing_angles'] for r in result['meshes'] if r['cells']>=4)
    source=json.loads((a/'analysis/source_audit.json').read_text())
    assert source[-1]['vacuum_negative_outflow_count']==2178
    assert all(r['negative_outflow_with_negative_attenuation_count']==0 for r in source)
    counts.update(source_tests=12,archived_tests=12,all_verification_checks_passed=True,
                  physical_refinement_admission=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

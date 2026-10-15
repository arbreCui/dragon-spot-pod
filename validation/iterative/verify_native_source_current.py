#!/usr/bin/env python3
"""Verify the signed audit, exact replay, and eleven prior evidence seals."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

PRIOR=['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
       'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
       'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
       'exchange-pod-projection-20260928','native-radial-response-20260928',
       'native-multigroup-pod-20260928','native-axial-coupling-20260928',
       'native-axial-refinement-20260928']


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    counts=dict(byte_identical_analysis_files=0,exactly_equal_arrays=0,protected_files=0,
                source_inputs=0,prior_manifest_entries=0,prior_artifacts=len(PRIOR))
    for path in sorted((a/'analysis').iterdir()):
        target=a/'replay/analysis'/path.name
        assert digest(path)==digest(target),f'replay mismatch: {path.name}'
        counts['byte_identical_analysis_files']+=1
        if path.suffix=='.npz':
            x=np.load(path);y=np.load(target);assert x.files==y.files
            for name in x.files:
                np.testing.assert_array_equal(x[name],y[name]);counts['exactly_equal_arrays']+=1
    for manifest,key in [('protected_inputs_before.json','protected_files'),('inputs.json','source_inputs')]:
        for filename,expected in json.loads((a/manifest).read_text()).items():
            assert digest(root/filename)==expected,f'protected/source input changed: {filename}'
            counts[key]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected,filename=line.split(maxsplit=1)
            assert digest(folder/filename)==expected,f'older artifact changed: {name}/{filename}'
            counts['prior_manifest_entries']+=1
    for source in (a/'build').glob('*.py'):
        assert digest(source)==digest(root/'validation/iterative'/source.name),source.name
    for label in ['source_tests','archived_tests']:
        output=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 8 tests' in output and '\nOK\n' in output and 'skipped=' not in output
    result=json.loads((a/'analysis/result.json').read_text())
    assert result['identity_checks_passed']
    assert result['groups_with_significant_positive_offdiagonal_inverse']==370
    assert result['groups_with_certified_negative_propagation']==370
    rows=json.loads((a/'analysis/generator_audit.json').read_text())
    for r in rows:
        w=r['certified_witness']
        assert w['exponential_entry']<=w['exponential_upper_bound']+1e-16<0
        assert w['implicit_entry']<=w['implicit_upper_bound']+1e-16<0
    for n in [1,2,4,8,16,32,64]:
        fields=np.load(a/f'analysis/current_{n}.npz')
        assert np.all(fields['native_replayed_field']>=0)
    response=np.load(a/'inputs/operator_fields.npz')['response']
    counts['raw_response_negative_entries_retained']=int(np.sum(response<0))
    counts['raw_response_negative_groups']=int(np.sum(np.any(response<0,axis=(1,2))))
    counts.update(source_tests=8,archived_tests=8,all_verification_checks_passed=True,
                  new_coupled_reference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

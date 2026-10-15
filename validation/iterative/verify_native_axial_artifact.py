#!/usr/bin/env python3
"""Read-only replay and lineage verification; writes one new receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

PRIOR = ['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
         'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
         'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
         'exchange-pod-projection-20260928','native-radial-response-20260928',
         'native-multigroup-pod-20260928']


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    counts={'byte_identical_analysis_files':0,'exactly_equal_arrays':0,'protected_files':0,
            'source_inputs':0,'prior_manifest_entries':0,'prior_artifacts':len(PRIOR)}
    for path in sorted((a/'analysis').iterdir()):
        target=a/'replay/analysis'/path.name
        assert target.is_file(),f'missing replay: {target}'
        assert digest(path)==digest(target),f'replay bytes changed: {path}'
        counts['byte_identical_analysis_files']+=1
        if path.suffix=='.npz':
            x=np.load(path);y=np.load(target);assert x.files==y.files
            for key in x.files:
                np.testing.assert_array_equal(x[key],y[key]);counts['exactly_equal_arrays']+=1
    for filename,counter in [('protected_inputs_before.json','protected_files'),('inputs.json','source_inputs')]:
        baseline=json.loads((a/filename).read_text())
        for name,expected in baseline.items():
            assert digest(root/name)==expected,f'protected/source input changed: {name}'
            counts[counter]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected,filename=line.split(maxsplit=1)
            assert digest(folder/filename)==expected,f'prior artifact changed: {name}/{filename}'
            counts['prior_manifest_entries']+=1
    for source in (a/'build').glob('*.py'):
        assert digest(source)==digest(root/'validation/iterative'/source.name),f'archived source differs: {source}'
    assert digest(a/'build/export_native_fission.f90')==digest(root/'validation/iterative/export_native_fission.f90')
    for label in ('source_tests','archived_tests'):
        text=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 10 tests' in text and '\nOK\n' in text and 'skipped=' not in text
    counts.update(source_tests=10,archived_tests=10,all_checks_passed=True)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

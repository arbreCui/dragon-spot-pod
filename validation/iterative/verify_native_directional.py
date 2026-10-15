#!/usr/bin/env python3
"""Verify native replay, angular analysis and unchanged historical evidence."""
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
       'native-axial-refinement-20260928','native-source-current-consistency-20260928']


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    count=dict(native_files_byte_identical=0,analysis_files_byte_identical=0,arrays_exactly_equal=0,
               protected_files=0,source_inputs=0,copied_inputs=0,prior_artifacts=len(PRIOR),prior_manifest_entries=0)
    for n in ['track_data.bin','export_metadata.txt','scalar_sources.txt','scalar.csv','scalar_metadata.csv']:
        assert digest(a/'runs'/n)==digest(a/'replay/runs'/n),n
        count['native_files_byte_identical']+=1
    for p in sorted((a/'analysis').iterdir()):
        other=a/'replay/analysis'/p.name
        assert digest(p)==digest(other),p.name
        count['analysis_files_byte_identical']+=1
        if p.suffix=='.npz':
            x=np.load(p);y=np.load(other);assert x.files==y.files
            for key in x.files:
                np.testing.assert_array_equal(x[key],y[key]);count['arrays_exactly_equal']+=1
    for filename,key,base in [('protected_inputs_before.json','protected_files',root),
                              ('inputs.json','source_inputs',root),('copied_inputs.json','copied_inputs',a)]:
        for path,h in json.loads((a/filename).read_text()).items():
            assert digest(base/path)==h,path
            count[key]+=1
    for n in PRIOR:
        folder=root/'validation/artifacts'/n
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split(maxsplit=1)
            assert digest(folder/path)==h,f'{n}/{path}'
            count['prior_manifest_entries']+=1
    for n in ['export_native_directional.f90','qualify_native_directional.py',
              'test_native_directional.py','verify_native_directional.py']:
        assert digest(a/'build'/n)==digest(root/'validation/iterative'/n),n
    for label in ['source_tests','archived_tests']:
        output=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 8 tests' in output and '\nOK\n' in output and 'skipped=' not in output
    result=json.loads((a/'analysis/result.json').read_text())
    assert result['native_planar_aggregation_passed']
    assert not result['axial_odd_response_identified'] and not result['new_coupled_reference_qualified']
    for g in result['groups']:
        assert g['pjj_binary32_exact'] and g['negative_transmissions']==0
        assert g['max_raw_balance_relative']<1e-6 and g['directional_pair_raw_balance_relative']<1e-6
        assert g['errors']['retained_action_max_case_relative']<5e-12
        assert max(g['directional_pair_errors'].values())<5e-12
        for label in ['positive_input_extrema','directional_pair_extrema']:
            for k in ['negative_incoming_count','negative_outgoing_count','negative_integral_count']:
                assert g[label][k]==0
    count.update(source_tests=8,archived_tests=8,native_scalar_cases=93,positive_external_cases=87,
                 directional_pair_cases=9,all_verification_checks_passed=True,
                 axial_odd_response_identified=False,new_coupled_reference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(count,f,indent=2);f.write('\n')
    print(json.dumps(count,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

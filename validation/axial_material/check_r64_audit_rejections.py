"""Calibrate the serialized-terminal analyzer with deliberately corrupted exports."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import numpy as np

from analyze_r64_snapshot import analyze


def check(source):
    original=analyze(source)
    data=source.read_bytes()
    # A synthetic identity image calibrates only the acceptance checker.
    # It is explicitly not evidence that the real transport image passed.
    identity=bytearray(data)
    identity[-14*370*8:]=data[124:124+14*370*8]
    control=bytes(identity)
    variants={}
    changed=bytearray(control)
    fresh=np.frombuffer(changed,dtype='<f8',count=14*370,offset=len(changed)-14*370*8)
    fresh*=1.01
    variants['wrong_fresh_image']=bytes(changed)
    changed=bytearray(control)
    struct.pack_into('<d',changed,20,struct.unpack_from('<d',data,20)[0]*1.01)
    variants['wrong_keff']=bytes(changed)
    changed=bytearray(control)
    struct.pack_into('<d',changed,124,float('nan'))
    variants['nonfinite_flux']=bytes(changed)
    variants['truncated_export']=control[:-8]
    results={}
    with tempfile.TemporaryDirectory(prefix='spot-r64-audit-',dir='/private/tmp') as directory:
        positive=Path(directory)/'synthetic_identity.bin';positive.write_bytes(control)
        if analyze(positive)['classification']!='R64_SNAPSHOT_TERMINAL_AUDIT_PASS':
            raise AssertionError('synthetic identity control failed')
        for name,payload in variants.items():
            p=Path(directory)/(name+'.bin');p.write_bytes(payload)
            try:
                result=analyze(p)
            except ValueError as error:
                results[name]=dict(rejected=True,reason=str(error))
            else:
                if result['classification']!='R64_SNAPSHOT_TERMINAL_AUDIT_FAIL':
                    raise AssertionError(name+' was falsely accepted')
                results[name]=dict(rejected=True,failed_checks=[key for key,value in result['checks'].items() if not value])
    return dict(classification='SERIALIZED_AUDIT_NEGATIVE_CONTROLS_PASS',
        source_export_sha256=hashlib.sha256(data).hexdigest(),original_classification=original['classification'],
        positive_control_pass=True,positive_control_kind='Synthetic identity image only; not a numerical transport PASS.',
        snapshot_qualified=False,controls=results)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();result=check(args.export)
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()

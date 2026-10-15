"""Read the sealed MET state through the existing saved REAL64 native exporter."""
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT,DiskResources,SerialExecutor,dump_json,require_file,sha256,verify_sealed_directory
from qualified_snapshot_ingestion import descriptor


def main():
    art=ROOT/'validation/artifacts'
    production=art/'axial-material-production-qualified-AB-compensated-20261004'
    prepared=json.loads(require_file(production/'prepared.json','2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7').read_text())
    status_path=production/'AAA/run_status.json'
    status=json.loads(status_path.read_text())
    if status['classification']!='WAITING_REFERENCE' or status['cases']['AAA']['classification']!='VALID_MET':
        raise ValueError('independently checked fixed point required before reference observables')
    final=Path(status['cases']['AAA']['final_directory'])
    verify_sealed_directory(final)
    bootstrap=production/'AAA/bootstrap'
    verify_sealed_directory(bootstrap)
    tools=art/'axial-material-tools-20261003'
    exporter=require_file(tools/'export_observables','81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524',True)
    require_file(ROOT/'validation/axial_material/export_observables.f90','fdfb6204a9661a38ba120387311136e0eba2959d54bd0bac6b594723b586ee35')
    out=art/'axial-material-qualified-AAA-observables-20261004'
    out.mkdir(exist_ok=False)
    (out/'AAA').mkdir();(out/'runtime').mkdir()
    bounded=production/'runtime/run_bounded_dragon.py'
    shutil.copy2(bounded,out/'runtime/run_bounded_dragon.py')
    inputs={'track.xsm':bootstrap/'initial_axial_track.xsm','axial.xsm':final/'closed_axial.xsm',
            'macro.xsm':bootstrap/'initial_axial_macrolib.xsm'}
    for name,path in inputs.items():(out/name).symlink_to(path)
    pins={str(path):sha256(path) for path in inputs.values()}
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())
    spec=json.loads(Path(prepared['case_spec']['path']).read_text())
    resources=DiskResources(art,roots,8*2**30,spec['resource_caps']['new_case_artifact_budget_GiB']*2**30)
    protocol=dict(schema='AXMAT_SAVED_MET_REAL64_OBSERVABLE_EXPORT_V1',
        production_prepared=descriptor(production/'prepared.json'),AAA_status=descriptor(status_path),
        final_stage_seal=descriptor(final/'result.json'),exporter=descriptor(exporter),
        exporter_source=descriptor(ROOT/'validation/axial_material/export_observables.f90'),
        bounded_runner=descriptor(out/'runtime/run_bounded_dragon.py'),source_inputs=pins,
        wall_seconds=60,threads=1,retries=0,resource_roots=roots)
    dump_json(out/'protocol.json',protocol)
    runner=SerialExecutor(out,60,'AAA',resources)
    with (out/'export.log').open('xb') as log:
        runner._process([str(exporter),'track.xsm','axial.xsm','macro.xsm','observables'],out,subprocess.DEVNULL,log,60)
    if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in (out/'export.log').read_text().splitlines()):
        raise ValueError('native read-only exporter did not complete')
    for path,wanted in pins.items():require_file(Path(path),wanted)
    verify_sealed_directory(final);verify_sealed_directory(bootstrap)
    dump_json(out/'export_receipt.json',dict(classification='SAVED_MET_REAL64_OBSERVABLES_EXPORTED',
        protocol=descriptor(out/'protocol.json'),inputs_unchanged=True,
        outputs={p.name:sha256(p) for p in out.glob('observables.*')},
        independent_accuracy_qualified=False,resources=resources.check()))
    print(json.dumps(descriptor(out/'export_receipt.json'),indent=2))


if __name__=='__main__':main()

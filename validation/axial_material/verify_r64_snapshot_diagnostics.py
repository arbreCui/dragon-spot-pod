"""Read-only replay of the declared binary64 snapshot investigation."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from analyze_r64_snapshot import analyze as analyze_export
from analyze_r64_snapshot_probe import analyze as analyze_probe
from analyze_r64_trace import analyze as analyze_trace
from production_runner import check_dragon_log

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'validation/artifacts'
EXPERIMENTS={
 'first_call':('axial-material-r64-first-call-20261003','56f2187a292241568977cf0543c1a641359e4a7d60efc92387ec1c8560eb9e61'),
 'cold':('axial-material-r64-snapshot-A-20261003','2fd06e51dbb80006658ef91b34aa5e7f6b5ed9d9265d5a3cd10493666f802b75'),
 'warm_input_rejected':('axial-material-r64-snapshot-A-warm-20261003','7c6406376c49656a02bd539ad4c229abcc1e6084cc5770b250d5e11fe21f8e69'),
 'warm':('axial-material-r64-snapshot-A-warm-inputfix-20261003','6beef5bd97e804ef4e05fffbff0b7df590132ce289497a8350d885b11acb82bd'),
 'inner_polish':('axial-material-r64-inner-polish-20261003','6cc3b721c6c473eef6bd9a8eabe0cbc69922227b0dd786990140135954354540'),
 'thermal_polish':('axial-material-r64-thermal-polish-20261003','5625e3f442e4b82df04907bfcf23876f34df2007359c2d6994a5a2aacef5b00e'),
 'rebalance_input_rejected':('axial-material-r64-rebalance-20261003','2b3ed05441066c02145ea7bdfd1e23af94a45db06266adc52a9e2ce683a913bc'),
 'rebalance':('axial-material-r64-rebalance-inputfix-20261003','5b62c23869f5d75105ff6a6cdf3c35bd2cd547ba93f47fc335c9c4bc3488be00'),
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(condition,message):
    if not condition:
        raise ValueError(message)


def verify():
    from verify_residual_diagnostics import verify as verify_previous
    previous=verify_previous()
    require(previous['classification']=='DIAGNOSTIC_EVIDENCE_VERIFIED_PRODUCTION_GATES_NOT_MET','prior evidence changed')
    evidence={};runs={};common=None;wall=0.0
    for label,(folder,wanted) in EXPERIMENTS.items():
        work=ART/folder
        require(digest(work/'execution.json')==wanted,'execution changed: '+label)
        manifest=json.loads((work/'execution.json').read_text())
        for name,expected in manifest['files'].items():
            require(digest(Path(name))==expected,'frozen input changed: '+name)
        status=json.loads((work/'run_status.json').read_text())
        require(status['frozen_inputs_unchanged'] and not status['scientific_accuracy_accepted'],'run scope/identity failure')
        for name,expected in status['outputs'].items():
            require(digest(work/'A'/name)==expected,'run output changed: '+label+'/'+name)
        inputs={name:digest(work/'A'/name) for name in ('material.xsm','geometry.dat','radial_track.bin')}
        if common is None:
            common=inputs
        require(inputs==common,'physics/track input differs: '+label)
        wall+=status['elapsed_seconds']
        log=(work/'A/solve.log').read_text()
        run=dict(classification=status['classification'],elapsed_seconds=status['elapsed_seconds'])
        if label=='first_call':
            measured=analyze_probe(log)
            saved=json.loads((work/'independent_observations.json').read_text())
            require(all(saved[k]==v for k,v in measured.items()),'probe observations differ')
            run.update({k:v for k,v in measured.items() if k!='rows'})
            old=(ART/'axial-material-true-residual-probe-20261003/A/probe.log').read_text()
            def sources(text,prefix):
                return [tuple([int(p[1]),int(p[2]),float(p[3])]) for line in text.splitlines() if line.startswith(prefix) for p in [line.split()]]
            require(sources(old,'AXMAT-VECTOR ')==sources(log,'AXMAT-R64-VECTOR '),'original native and REAL64 source differs')
        elif label in ('warm_input_rejected','rebalance_input_rejected'):
            marker='LINKED_LIST *FLUX* ALREADY EXISTS' if label=='warm_input_rejected' else 'FLUGPI: READ ERROR - ILLEGAL KEYWORD ON'
            require(marker in log and 'MCCGF64-CENSUS' not in log,'input rejection differs')
            require(not (work/'A/snapshot_A.xsm').exists(),'rejected deck published snapshot')
        else:
            observed=analyze_trace(log)
            run.update({k:v for k,v in observed.items() if k!='outer'})
            if label in ('cold','warm','inner_polish','thermal_polish'):
                require('TimeoutExpired' in status['error'],'expected bounded stop')
                require(not (work/'A/snapshot_A.xsm').exists() and observed['snapshot_marker_count']==0,'timeout published snapshot')
            else:
                require(status['classification']=='R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT','polish did not complete')
                check_dragon_log(log,'AXMAT-SNAPSHOT-A-COMPLETE')
                require(observed['strict_terminal_marker'] and observed['snapshot_marker_count']==1 and not observed['incomplete_final_radial_call'],'missing strict terminal')
                for key in ('EEXT','EUNK','EINR'):
                    lines=[x for x in log.splitlines() if x.startswith(' FLU2DR-TERM') and key+'=' in x]
                    require(len(lines)==1,'missing or duplicate terminal '+key)
                    value=float(re.search(r'\b'+key+r'=\s*([+\-\d.E]+)',lines[0]).group(1))
                    require(0<=value<2.5e-7,'unconverged strict terminal '+key)
                    run[key]=value
                require(observed['maximum_printed_inner_residual']<=2.5000005e-10,'polished target not met')
        runs[label]=run
        for p in (work/'execution.json',work/'protocol.json',work/'run_status.json',work/'A/solve.log'):
            evidence[str(p)]=digest(p)
    work=ART/EXPERIMENTS['rebalance'][0]
    audit=work/'audit_initialized'
    status=json.loads((audit/'run_status.json').read_text())
    require(status['frozen_inputs_unchanged'],'audit mutated inputs')
    require(digest(audit/'protocol.json')==status['protocol_sha256'],'audit protocol changed')
    protocol=json.loads((audit/'protocol.json').read_text())
    for name,wanted in protocol['files'].items():
        require(digest(Path(name))==wanted,'audit input changed: '+name)
    for name,wanted in status['outputs'].items():
        require(digest(audit/name)==wanted,'audit output changed: '+name)
    measured=analyze_export(audit/'audit.bin')
    require(measured==json.loads((audit/'observations.json').read_text()),'saved-terminal analysis differs')
    require(measured['classification']==status['classification'],'audit classification differs')
    wall+=status['elapsed_seconds']
    from analyze_r64_rebalance_gap import diagnose
    gap=diagnose(audit/'audit.bin')
    require(gap==json.loads((audit/'rebalance_gap.json').read_text()),'rebalance diagnostic differs')
    from check_r64_audit_rejections import check as check_negatives
    negatives=check_negatives(audit/'audit.bin')
    require(negatives==json.loads((audit/'negative_controls.json').read_text()),'audit rejection controls differ')
    rejected_audit=work/'audit'
    rejected_status=json.loads((rejected_audit/'run_status.json').read_text())
    require(rejected_status['classification']=='INPUT_IDENTITY_FAILURE' and 'nonpositive state' in rejected_status['error'],'initial checker failure differs')
    wall+=rejected_status['elapsed_seconds']
    for p in rejected_audit.iterdir():
        if p.is_file():
            evidence[str(p)]=digest(p)
    for p in audit.iterdir():
        if p.is_file():
            evidence[str(p)]=digest(p)
    previous_seal=ART/'axial-material-residual-closeout-20261003/result.sha256'
    require(digest(previous_seal)=='7eb14d009d457c926876190eb0019d53f27f7b2d65c8c8ed8512e57a5f3bfd0d','previous seal differs')
    for line in previous_seal.read_text().splitlines():
        wanted,name=line.split('  ',1)
        require(digest(previous_seal.parent/name)==wanted,'previous report changed: '+name)
    qualified=status['snapshot_qualified'] and all(measured['checks'].values())
    return dict(classification='R64_SNAPSHOT_DIAGNOSTICS_VERIFIED',snapshot_A_binary64_qualified=qualified,
        production_qualified=False,aaa_qualified=False,aba_started=False,new_ce_accuracy_accepted=False,
        shared_solver_modified=False,prior_evidence_unchanged=True,original_source_vectors_identical=True,
        material_geometry_and_track_identical=common,runs=runs,
        terminal_audit={k:v for k,v in measured.items() if k!='groups'},
        rebalance_diagnostic=gap,analyzer_negative_controls=negatives,
        numerical_wall_seconds_including_cleanup=wall,evidence=evidence,
        limits=['Isolated offline A snapshot only; no new production runtime promotion.',
                'Initial REBA OFF contrasts stopped; the final candidate restores native rebalancing through FLUBAL64 and retains 100x stricter within-group/multigroup work targets. These are numerical changes, not solely a precision change.',
                'The legacy binary32 mirror is not certified at the original radial tolerance.',
                'B-state regeneration and explicit audited snapshot-producer/ingestion checks must precede qualified AAA and ABA execution; legacy BOOT currently uses the binary32 mirror only as an initial guess.',
                'Original D4 CE accuracy failure remains unresolved.'])


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('evidence','runs')},indent=2))


if __name__=='__main__':
    main()

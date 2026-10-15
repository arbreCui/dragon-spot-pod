"""Prepare unchanged independent CE inputs; launch no transport."""
import json
from pathlib import Path
import shutil

from production_runner import ROOT, dump_json, require_file, sha256
from qualified_snapshot_ingestion import descriptor
from reference_statistics import predeclared_rules
from compare_balance_symmetry import predeclared_rules as balance_rules


def main():
    art=ROOT/'validation/artifacts'
    source=art/'axial-material-ce-rank1-20261003'
    production=art/'axial-material-production-qualified-AB-compensated-20261004'
    prepared=json.loads(require_file(production/'prepared.json',
        '2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7').read_text())
    common=json.loads((source/'frozen_execution_common.json').read_text())
    for path,wanted in common['files'].items():require_file(Path(path),wanted)
    spec_path=Path(prepared['case_spec']['path'])
    new_spec=json.loads(spec_path.read_text())
    old_spec=json.loads(Path(common['case_spec']['path']).read_text())
    for field in ('geometry','materials','cases','reference'):
        if new_spec[field]!=old_spec[field]:raise ValueError('independent physical/reference input changed')
    out=art/'axial-material-ce-qualified-AB-compensated-20261004'
    out.mkdir(exist_ok=False)
    (out/'runtime').mkdir()
    for name in ('ce_execution.py','production_runner.py','production_inputs.py'):
        shutil.copy2(source/'runtime'/name,out/'runtime'/name)
    reuse={}
    for case in ('AAA','ABA'):
        folder=out/case;folder.mkdir()
        for name in ('materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json'):
            shutil.copy2(source/case/name,folder/name)
            reuse[str(folder/name)]=dict(source=descriptor(source/case/name),sha256=sha256(folder/name))
    addendum=json.loads((ROOT/'validation/axial_material/case_spec_rank1_moc_precision_resource_addendum.json').read_text())
    addendum.update(case_spec_sha256=prepared['case_spec']['sha256'],
        parent_resource_addendum=descriptor(ROOT/'validation/axial_material/case_spec_rank1_moc_precision_resource_addendum.json'),
        scope='Reuse the previously justified bounded 5400-second CE cap with identical sample counts, seeds and original gates. No formal CE transport has started for this new experiment.')
    dump_json(out/'resource_addendum.json',addendum)
    dump_json(out/'statistical_rules.json',predeclared_rules(spec_path))
    dump_json(out/'balance_symmetry_rules.json',balance_rules(spec_path))
    dump_json(out/'input_reuse_receipt.json',dict(classification='IDENTICAL_INDEPENDENT_PHYSICAL_XML_AND_CONTRACT_REUSED',
        case_spec=prepared['case_spec'],production_prepared=descriptor(production/'prepared.json'),files=reuse,
        production_qualified=False,formal_CE_started=False))
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())
    for case in ('AAA','ABA'):
        folder=out/case
        contract=dict(common,case_spec=prepared['case_spec'],resource_roots=roots,
            resource_addendum=str(out/'resource_addendum.json'),
            scope='Launch only after the same case has a valid independently checked SPOT fixed point; ABA additionally requires full independent AAA qualification.')
        files=dict(common['files'])
        files.update({str(p):sha256(p) for p in out.rglob('*') if p.is_file()})
        for p in (spec_path,Path(prepared['rank_addendum']['path']),production/'prepared.json',Path(__file__).resolve()):
            files[str(p)]=sha256(p)
        contract['files']=files
        dump_json(folder/'execution.json',contract)
    print(json.dumps(dict(classification='PREPARED_CE_NO_TRANSPORT',
        AAA=descriptor(out/'AAA/execution.json'),ABA=descriptor(out/'ABA/execution.json')),indent=2))


if __name__=='__main__':main()

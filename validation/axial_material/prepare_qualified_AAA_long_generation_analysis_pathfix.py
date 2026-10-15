"""Preserve rejected pre-transport collector paths; freeze corrected copies."""
import importlib.util
import json
from pathlib import Path
import time

from prepare_qualified_AAA_ce_long_generations import ROOT, OUT, digest, pin, verify, write_new, once


def main():
    if (OUT / 'AAA/run_claim.json').exists():
        raise ValueError('cannot change collection preparation after formal transport')
    old_path=OUT / 'analysis_collection_declaration.json'
    old=json.loads(old_path.read_text());verify(old['files'])
    runtime=OUT / 'runtime'
    names=('assess_qualified_AAA_reference_long_generations','run_qualified_AAA_reference_analysis_long_generations')
    corrected=[]
    for name in names:
        text=(runtime / (name+'.py')).read_text()
        text=once(text,'ROOT = Path(__file__).resolve().parents[2]','ROOT = Path(__file__).resolve().parents[4]')
        if name.startswith('run_'):
            text=once(text,names[0]+'.py',names[0]+'_v2.py')
            if text.count('analysis_collection_declaration.json')!=2:
                raise ValueError('unexpected driver declaration reference count')
            text=text.replace('analysis_collection_declaration.json','analysis_collection_declaration_v2.json')
        path=runtime / (name+'_v2.py')
        with path.open('x') as stream:stream.write(text)
        spec=importlib.util.spec_from_file_location(name+'_path_check',path)
        item=importlib.util.module_from_spec(spec);spec.loader.exec_module(item)
        if item.ROOT!=ROOT:
            raise ValueError('corrected runtime project root does not match actual checkout')
        corrected.append(path)
    write_new(OUT / 'analysis_preparation_path_rejection.json',dict(classification='PRE_TRANSPORT_ANALYSIS_PATHS_REJECTED',
        original_declaration=pin(old_path),native_formal_started=False,native_results_changed=False,
        reason='Copied collector and driver moved from validation/axial_material to artifacts/<attempt>/runtime; their unchanged parents[2] resolved artifacts as project root. Found before any formal claim or analysis execution.',
        correction='New v2 copies use parents[4], with actual imported ROOT checked against this checkout. Statistics, current comparisons, sampling, thresholds and native inputs unchanged; old copies preserved.'))
    files=dict(old['files'])
    files.update({str(p.resolve()):digest(p) for p in [*corrected,Path(__file__).resolve(),old_path,OUT / 'analysis_preparation_path_rejection.json']})
    new=dict(old,declared_unix=time.time(),files=files,previous_preparation=pin(old_path),
        path_rejection=pin(OUT / 'analysis_preparation_path_rejection.json'),
        actual_driver=pin(corrected[1]),actual_collector=pin(corrected[0]),
        change='Runtime root path depth and v2 collection references only; checked before formal transport.')
    write_new(OUT / 'analysis_collection_declaration_v2.json',new)
    print(json.dumps(dict(driver=pin(corrected[1]),collector=pin(corrected[0]),
        declaration=pin(OUT / 'analysis_collection_declaration_v2.json')),indent=2))


if __name__=='__main__':main()

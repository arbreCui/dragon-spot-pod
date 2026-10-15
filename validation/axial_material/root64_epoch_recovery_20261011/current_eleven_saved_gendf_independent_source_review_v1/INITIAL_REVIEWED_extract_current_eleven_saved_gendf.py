#!/usr/bin/env python3
"""One bounded read of all eleven preserved nonzero-NX GENDF inputs.

The unchanged parser retains all370 P0 entries, explicit presence masks and
temperature/dilution/energy grids. Its fsum reductions are diagnostic evidence;
this child does not replay DRAGR packed words, apply TONE/SPH/MASK or qualify a
reaction model. It never invokes a native engine or writes any original input.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import re
import stat
import sys
import time

CASE='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
  history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
  free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(DRAGR_packed_raw_words_replayed=False,current_SPH_MASK_context_applied=False,
  three_current_raw_MACRO_comparisons_performed=False,complete_reaction_authority_qualified=False,
  physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,
  scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')


def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)


def strict(raw):
    def pairs(items):
        value={}
        for key,item in items:require(key not in value,'duplicate key');value[key]=item
        return value
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:
      (_ for _ in ()).throw(ValueError('nonfinite metadata '+x)))


def identity(s):
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path,budget):
    path=Path(path);require(path.is_absolute()and'..'not in path.parts,'literal absolute file')
    require(not any(p.is_symlink()for p in(path,*path.parents)),'no file or ancestor aliases')
    before=path.lstat();require(stat.S_ISREG(before.st_mode)and before.st_nlink==1,'regular single-link input')
    h=hashlib.sha256();total=0
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==identity(before),'open full7ID')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            total+=len(raw);h.update(raw)
        require(identity(os.fstat(stream.fileno()))==identity(before),'EOF full7ID')
    require(total==before.st_size and identity(path.lstat())==identity(before),'after full7ID')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=total,identity=identity(before))


def check(expected,budget):
    require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact four-field pin')
    require(type(expected['path'])is str and type(expected['sha256'])is str and
      re.fullmatch('[0-9a-f]{64}',expected['sha256'])is not None and
      type(expected['size_bytes'])is int and expected['size_bytes']>=0 and
      type(expected['identity'])is list and len(expected['identity'])==7 and
      all(type(x)is int and x>=0 for x in expected['identity'])and
      expected['identity'][3]==1 and expected['identity'][4]==expected['size_bytes'],
      'strict types/full SHA/size/seven identity fields')
    require(pin(expected['path'],budget)==expected,'fullEOF SHA/7ID changed')


def read(expected,budget):
    check(expected,budget);value=strict(Path(expected['path']).read_bytes());check(expected,budget);return value


def write(path,value):
    with Path(path).open('x')as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())


class Budget:
    def __init__(self,roots):
        require(type(roots)is list and len(roots)==5 and len(set(roots))==5,'all five disjoint joint roles')
        self.roots=[Path(p)for p in roots]
        require(all(p.is_absolute()for p in self.roots)and
          not any(a.is_relative_to(b)for a in self.roots for b in self.roots if a!=b),'literal disjoint joint roots')
        self.started=time.monotonic();self.last=0.0
    def check(self):
        now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform!='darwin':peak*=1024
        require(now-self.started<600 and peak<512*2**20,'original child600/SELF512')
        if now-self.last<0.25:return
        self.last=now;total=0
        for root in self.roots:
            if not root.exists():continue
            for p in root.rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no joint namespace alias')
                if stat.S_ISREG(s.st_mode):total+=s.st_size
        unlinked={}
        for fd in os.listdir('/dev/fd'):
            try:s=os.fstat(int(fd))
            except(ValueError,OSError):continue
            if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
        require(total+sum(unlinked.values())<2*2**30,'original shared fresh2GiB including previous capture/open-unlinked')


def main():
    p=argparse.ArgumentParser();p.add_argument('--binding-pin',required=True)
    p.add_argument('--expected-parent-pid',type=int,required=True);args=p.parse_args()
    require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None,
      'real owning parent and unprofiled unoptimized child')
    require(all(os.environ.get(k)=='1'for k in THREADS),'original single thread')
    expected=strict(args.binding_pin);binding=read(expected,lambda:None)
    require(binding['schema']=='CURRENT_ELEVEN_SAVED_GENDF_EXPLICIT_EXECUTION_BINDING_V1'and
      binding['original_caps']==CAPS and binding['requested_mts']==[5],'complete current MT5 extraction-only binding')
    budget=Budget(binding['joint_archive_roots']);budget.check()
    sf=read(binding['source_freeze_pin'],budget.check)
    require(sf['schema']=='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_V1'and
      sf['candidate_executed']is False,'explicit immutable complete Source package')
    table={p['path']:p for p in sf['complete_source_file_pins']}
    require(len(table)==len(sf['complete_source_file_pins'])and str(Path(__file__).absolute())in table,
      'whole actual child Source unique and protected')
    for row in table.values():check(row,budget.check)
    plan=read(binding['selected_genDF_source_plan_pin'],budget.check)
    require(sf['selected_genDF_source_plan_pin']==binding['selected_genDF_source_plan_pin']and
      plan['current_formal_case_sha256']==CASE and plan['extractor_executed']is False and
      plan['schema']=='READONLY_CURRENT_NONZERO_NX_GENDF_SOURCE_PLAN_V1','same eleven current physical input plan')
    require(binding['current_case_spec_pin']['sha256']==CASE,'formal current case, no historical replacement')
    check(binding['current_case_spec_pin'],budget.check)
    rows=plan['inputs'];names=[r['nuclide']for r in rows]
    require(len(rows)==11 and len(set(names))==11 and names==plan['actual_nonzero_NX_unique_references']and
      set(names)=={'U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55'},
      'exact all eleven currently nonzero-NX references, no selected omission')
    parser_pin=plan['source_pin'];require(table.get(parser_pin['path'])==parser_pin,'actual whole unchanged parser Source')
    check(parser_pin,budget.check)
    spec=importlib.util.spec_from_file_location('current_saved_binary_gendf_parser',parser_pin['path'])
    parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser);check(parser_pin,budget.check)
    for row in binding['fixed_current_pins']:check(row,budget.check)
    out=Path(binding['output_directory']);require(out in budget.roots and not os.path.lexists(out),'fresh child output, once')
    out.mkdir();results=[]
    for row in rows:
        budget.check();value=parser.extract(row['preserved_binary_GENDf_input_pin'],row['mat'],[5],budget.check)
        require(value['energy_groups']==370 and value['requested_mts']==[5]and
          value['input_pin']==row['preserved_binary_GENDf_input_pin']and
          value['DRAGR_packed_raw_words_replayed']is False and
          value['complete_reaction_authority_qualified']is False,'only actual unchanged parser extraction, no authority claim')
        target=out/(row['nuclide']+'_actual_saved_MT5_P0.json');write(target,value)
        results.append(dict(nuclide=row['nuclide'],mat=row['mat'],input_pin=value['input_pin'],
          actual_complete_extraction_pin=pin(target,budget.check),actual_whole_file_records=value['whole_file_records'],
          actual_sections=len(value['actual_P0_sections']),actual_grid_count=len(value['original_full_MF1_temperature_dilution_energy_grids'])))
        del value
    for row in binding['fixed_current_pins']:check(row,budget.check)
    for row in table.values():check(row,budget.check)
    check(expected,budget.check);budget.check()
    report=out/'ACTUAL_ELEVEN_SAVED_GENDF_EXTRACTION_EVIDENCE.json'
    write(report,dict(schema='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_EXTRACTION_EVIDENCE_V1',
      status='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY',current_case_spec_pin=binding['current_case_spec_pin'],
      actual_material_observation_report_pin=binding['actual_material_observation_report_pin'],
      source_freeze_pin=binding['source_freeze_pin'],selected_genDF_source_plan_pin=binding['selected_genDF_source_plan_pin'],
      execution_binding_pin=expected,actual_extractions=results,original_caps=CAPS,
      original_parser_math_unchanged=True,all370_P0_entries_masks_and_actual_grids_retained=True,
      native_engines_started=0,original_input_or_library_writes=0,**FALSE))
    print(json.dumps(dict(status='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY',report=pin(report,budget.check),**FALSE),allow_nan=False),flush=True)


if __name__=='__main__':main()

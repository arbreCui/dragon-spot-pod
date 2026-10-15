#!/usr/bin/env python3
"""Future Root child exec route; same PID, unchanged original watchdog.

Root's original bounded runner starts this process in an owned stage under the
new B output root. This process verifies metadata/current7 and replaces itself
with the separately built native executable in the original SCI library cwd.
It does not fork, launch a monitor, copy a library or read any SCI body.
This UNREADY Source is not executable admission.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import importlib.util

THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)

def identity(s):
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read_control(expected):
    path=Path(expected['path'])
    require(path.is_absolute()and not any(p.is_symlink()for p in(path,*path.parents)),
      'literal control role')
    before=path.lstat()
    require(stat.S_ISREG(before.st_mode)and before.st_nlink==1 and
      before.st_size<=2**20 and identity(before)==expected['identity'],'bounded control current7')
    with path.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==expected['identity'],'opened control current7')
        raw=f.read();require(identity(os.fstat(f.fileno()))==expected['identity'],'closed control current7')
    require(len(raw)==expected['size_bytes']and hashlib.sha256(raw).hexdigest()==expected['sha256']and
      identity(path.lstat())==expected['identity'],'exact Source/control fullEOF PF')
    return raw

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--binding-pin',required=True)
    parser.add_argument('--expected-parent-pid',required=True,type=int)
    args=parser.parse_args()
    require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and
      sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),
      'one original Root parent, one thread, no profile/optimized checks')
    binding_pin=json.loads(args.binding_pin)
    binding=json.loads(read_control(binding_pin))
    require(binding['actual_Root_PID']==args.expected_parent_pid and
      binding['business_admission_complete']is True and binding['entry_mode']=='Root'and
      binding['new_IO_build_and_publication_closed0']is True,
      'real separately admitted Root execution/new IO build, never draft admission')
    source_pins=binding['execution_Source_pins']
    table={p['path']:p for p in source_pins}
    require(len(table)==len(source_pins)and str(Path(__file__).absolute())in table,
      'full exact executing Source table')
    for pin in source_pins:read_control(pin)
    helper_path=Path(__file__).absolute().parent/'B_original_input_binding.UNREADY.py'
    require(str(helper_path)in table,'explicit B binding Source pin')
    spec=importlib.util.spec_from_file_location('explicit_original_B_binding',helper_path)
    route=importlib.util.module_from_spec(spec);spec.loader.exec_module(route)
    read_control(table[str(helper_path)])
    seed_pin=binding['original_v10_seed_plan_pin']
    seed=json.loads(read_control(seed_pin))
    route.validate_B_binding(binding,seed,seed_pin)
    require(binding['derived_B_material_deck_pin']['path']in table and
      binding['derived_B_material_deck_pin']==table[binding['derived_B_material_deck_pin']['path']],
      'exact derived original B deck with four IO-only literal replacements')
    runtime=binding['new_IO_runtime_pin'];route.current_only(runtime)
    oldcwd=Path(binding['actual_native_cwd']);out=Path(binding['actual_observation_directory'])
    require(out.is_dir()and not any(p.is_symlink()for p in(out,*out.parents))and
      out.lstat().st_uid==os.getuid()and Path.cwd().is_relative_to(out),
      'unchanged watchdog starts in owned output stage; native cwd differs explicitly')
    require(route.snapshot_old_cwd_current7()==binding['all_old_cwd_entries_current7_before_child'],
      'all old cwd names/7IDs bound before sole child')
    for path in out.iterdir():
        name=path.name
        require(name not in route.PRODUCT_NAMES and not name.startswith(('axobs-','_'))and
          not name.endswith(('.o2m','.l2m'))and name!='TRACK_T_f',
          'no existing native output/cache/scratch; no retry')
    claim=json.loads(read_control(binding['exclusive_Root_claim_pin']))
    require(claim['Root_PID']==args.expected_parent_pid and claim['output_root']==str(out),
      'exclusive actual Root ownership already acquired before child')
    env=dict(os.environ);env['SPOT_AXMAT_OBSERVATION']='ADMITTED_SOURCE_ONLY'
    env['SPOT_AXMAT_OBSERVATION_DIRECTORY']=binding['io_component']
    os.chdir(oldcwd)
    # Exec preserves the exact original watchdog's one owned child PID/group.
    # Root retains stdout/stderr in the original owned stage log descriptor.
    os.execve(runtime['path'],[runtime['path']],env)

if __name__=='__main__':main()

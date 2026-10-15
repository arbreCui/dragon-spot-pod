"""UNREADY IO build command plan; never invokes a compiler or subprocess.

The original actual75 link argv is authoritative. Replace only the observer
module object's path, keep every other original object/archive in order, and
add exactly three IO-only C overrides before the first archive. This increases
the explicit link object count by3; it is not the original75 runtime. A new
genuine bounded build and independent qualification are still required.
"""
from pathlib import Path

def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)

def IO_build_commands(actual75_report,Source_directory,new_build_directory,
                      new_runtime_path,exact_C_compiler_path,C_configuration):
    source=Path(Source_directory);build=Path(new_build_directory)
    require(build.is_relative_to(source)and Path(new_runtime_path).is_relative_to(source),
      'new build/runtime nested under already counted Source top, no hidden new output root')
    require(C_configuration==dict(architecture='arm64',platform='Darwin',
      hdf5=False,openmp=False,mpi=False,preprocessor=['-DLinux','-DUnix']),
      'separately verified original Ganlib C ABI/configuration, no guessed HDF5/OpenMP mode')
    rows=actual75_report['records']
    compile_rows=[r for r in rows if r['label']=='build/compile_0']
    links=[r for r in rows if r['label']=='build/link_Dragon']
    require(len(compile_rows)==len(links)==1 and all(r['status']=='PASS'for r in rows),
      'exact genuine actual75 compiler/link metadata')
    original_compile=compile_rows[0]['command'];old_object=original_compile[-1]
    command=list(original_compile)
    original_build=str(Path(old_object).parent)
    for i,arg in enumerate(command):
        if arg in ('-I'+original_build,'-J'+original_build):command[i]=arg[:2]+str(build)
    require(command[-4]=='-c'and command[-2]=='-o','original exact observer compile argv suffix')
    command[-3]=str(source/'AXMAT_CONTEXT_OBSERVATION_MOD.B_IO.UNREADY.f90')
    command[-1]=str(build/'AXMAT_CONTEXT_OBSERVATION_MOD.B_IO.UNREADY.o')
    compiles=[command];C_objects=[]
    # Flags are the original Darwin-arm64 Ganlib Makefile C rule. No make or
    # whole archive rebuild is run, and no scientific C/Fortran API is changed.
    for name in ('cle2000_c','clemod_c','kdrdpr'):
        obj=str(build/(name+'.B_IO.UNREADY.o'));C_objects.append(obj)
        compiles.append([exact_C_compiler_path,'-Wall','-fPIC','-DLinux','-DUnix',
          '-O2','-march=native','-ffp-contract=off','-g',
          '-I/Users/wen/spot/Ganlib/src','-I'+str(source),
          '-c',str(source/(name+'.B_IO.UNREADY.c')),'-o',obj])
    original_link=links[0]['command'];require(original_link.count(old_object)==1,
      'one exact original observer module object slot')
    link=list(original_link);link[link.index(old_object)]=command[-1]
    archive_indices=[i for i,p in enumerate(link)if p.endswith('.a')]
    require(len(archive_indices)==4,'original four archive order intact')
    first=archive_indices[0];link[first:first]=C_objects
    require(link[-2]=='-o','exact original output argv suffix');link[-1]=str(new_runtime_path)
    restored=list(link)
    for p in C_objects:restored.remove(p)
    restored[restored.index(command[-1])]=old_object;restored[-1]=original_link[-1]
    require(restored==original_link,'whole original link argv inverse equality')
    return dict(compile_commands=compiles,link_command=link,
      original75_link_command=original_link,original75_link_argv_inverse_equal=True,
      new_explicit_C_override_object_count=3,
      original_explicit_object_count=sum(p.endswith('.o')for p in original_link),
      new_explicit_object_count=sum(p.endswith('.o')for p in link),
      whole_Ganlib_archive_rebuild_required_by_plan=False,
      actual_new_build_required=True,actual_new_build_executed=False)

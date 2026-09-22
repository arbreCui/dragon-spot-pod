#!/usr/bin/env python3
"""Short saved-current arithmetic tests; no transport or physics acceptance."""
import argparse
import csv
import hashlib
from pathlib import Path
import platform
import subprocess
import tempfile

FLAGS = ("-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror "
         "-Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math").split()
REJECTIONS = {
    'zero_denominator': 'ZERO DENOMINATOR',
    'bad_key': 'SCALAR FLUX INDEX OUT OF RANGE',
    'bad_type': 'FLUX64 ITEM MUST BE NUNK REAL64 VALUES',
    'nan_field': 'NONFINITE FLUX64 FIELD',
}

FIXTURE = r"""
program fixture
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value,ieee_quiet_nan
  implicit none
  integer,parameter :: nr=132,nz=3,ng=370,nu=2772,l4=1188,l5=528
  type(c_ptr) :: track,axial,fl64,fl32
  integer :: state(40),key(nr*nz),mapping(nz),i,f,g,p,k
  real(real32) :: area(nr),height(nz),volume(nr*nz)
  real(real64) :: u(nu),leak(ng*nz),phi(nz),jface(nz+1),num,den
  character(len=32) :: mode
  call get_command_argument(1,mode)
  call LCMOP(track,'track.xsm',0,2,0)
  call LCMPTC(track,'SIGNATURE',12,'L_TRACK     ')
  call LCMPTC(track,'TRACK-TYPE',12,'SPOT        ')
  state=0
  state(1)=nr*nz; state(2)=nu; state(6)=nr; state(7)=nz
  state(8)=nz; state(11)=l4; state(12)=l5
  call LCMPUT(track,'STATE-VECTOR',40,1,state)
  key=[(nr*nz+1-i,i=1,nr*nz)]
  if(mode=='bad_key') key(1)=nu+1
  mapping=[3,1,2]
  area=2.0_real32
  height=[2.0_real32,4.0_real32,8.0_real32]
  do i=1,nr
    do f=1,nz
      volume((i-1)*nz+f)=area(i)*height(f)
    enddo
  enddo
  call LCMPUT(track,'KEYFLX',nr*nz,1,key)
  call LCMPUT(track,'MAT1D',nz,1,mapping)
  call LCMPUT(track,'AREA2D',nr,2,area)
  call LCMPUT(track,'VOL1D',nz,2,height)
  call LCMPUT(track,'VOLUME',nr*nz,2,volume)
  call LCMPUT(track,'NCODE',2,1,[1,1])
  call LCMPUT(track,'ZCODE',2,2,[0.0_real32,0.0_real32])
  call LCMCL(track,1)

  call LCMOP(axial,'axial.xsm',0,2,0)
  call LCMPTC(axial,'SIGNATURE',12,'L_FLUX      ')
  state=0
  state(1)=ng; state(2)=nu
  call LCMPUT(axial,'STATE-VECTOR',40,1,state)
  call LCMPUT(axial,'KEYFLX',nr*nz,1,key)
  call LCMPUT(axial,'SPOT-KEFF64',1,4,1.25_real64)
  call LCMPUT(axial,'K-EFFECTIVE',1,2,1.25_real32)
  call LCMPUT(axial,'SPOT-X-EPOCH',1,1,8)
  call LCMPTC(axial,'SPOT-X-STATE',12,'CLOSED      ')
  fl64=LCMLID(axial,'FLUX64',ng)
  fl32=LCMLID(axial,'FLUX',ng)
  do g=1,ng
    phi=[2.0_real64,4.0_real64,8.0_real64]
    if(mode=='zero_denominator') phi(2)=0.0_real64
    jface=[-3.0_real64,-1.0_real64,2.0_real64,6.0_real64]
    if(g==2) jface=-jface
    if(g==3) jface(4)=jface(4)+2.0_real64**(-30)
    u=0.0_real64
    do i=1,nr
      do f=1,nz
        k=nr*nz+1-((i-1)*nz+f)
        u(k)=phi(f)
      enddo
      u(l4+(i-1)*(nz+1)+1:l4+i*(nz+1))=jface
    enddo
    if(mode=='nan_field'.and.g==1) u(l4+1)=ieee_value(0.0_real64,ieee_quiet_nan)
    if(mode=='bad_type'.and.g==1) then
      call LCMPDL(fl64,g,nu,2,real(u,real32))
    else
      call LCMPDL(fl64,g,nu,4,u)
    endif
    call LCMPDL(fl32,g,nu,2,real(u,real32))
    do f=1,nz
      p=mapping(f)
      num=0.0_real64
      den=0.0_real64
      do i=1,nr
        num=num+2.0_real64*(jface(f+1)-jface(f))
        den=den+2.0_real64*real(height(f),real64)*phi(f)
      enddo
      leak((p-1)*ng+g)=0.0_real64
      if(den/=0.0_real64) leak((p-1)*ng+g)=num/den
    enddo
  enddo
  if(mode=='changed_saved') leak(1)=leak(1)+0.125_real64
  call LCMPUT(axial,'SPOT-X-L',nz*ng,4,leak)
  call LCMCL(axial,1)
end program fixture
"""


def run(command, cwd, check=True):
    return subprocess.run(list(map(str, command)), cwd=cwd, timeout=10,
                          capture_output=True, text=True, check=check)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def expected(floor, group):
    currents = [-3.0, -1.0, 2.0, 6.0]
    if group == 2:
        currents = [-v for v in currents]
    if group == 3:
        currents[3] += 2.0**-30
    low = high = num = den = 0.0
    for _ in range(132):
        low += 2.0 * currents[floor - 1]
        high += 2.0 * currents[floor]
        num += 2.0 * (currents[floor] - currents[floor - 1])
        den += 2.0 * (2.0, 4.0, 8.0)[floor - 1]**2
    return dict(low_current=low, high_current=high, numerator=num,
                denominator=den, recomputed_leak=num/den)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    ganlib = here.parents[1] / 'Ganlib/lib' / f'{platform.system()}_{platform.machine()}'
    with tempfile.TemporaryDirectory(prefix='d4a-current-test-') as temporary:
        work = Path(temporary)
        host = args.host.resolve() if args.host else work / 'diagnose'
        if not args.host:
            run(['gfortran', *FLAGS, '-I', ganlib/'modules',
                 here/'diagnose_d4a_axial_current.f90', ganlib/'libGanlib.a',
                 '-lstdc++', '-o', host], work)
        source = work / 'fixture.f90'
        source.write_text(FIXTURE)
        fixture = work / 'fixture'
        run(['gfortran', *FLAGS, '-I', ganlib/'modules', source,
             ganlib/'libGanlib.a', '-lstdc++', '-o', fixture], work)
        for mode in ('good', 'changed_saved', 'zero_denominator',
                     'bad_key', 'bad_type', 'nan_field'):
            case = work / mode
            case.mkdir()
            run([fixture, mode], case)
            inputs = [case/'track.xsm', case/'axial.xsm']
            before = [hashlib.sha256(p.read_bytes()).digest() for p in inputs]
            result = run([host, 'track.xsm', 'axial.xsm', 'current.csv'], case, check=False)
            require(before == [hashlib.sha256(p.read_bytes()).digest() for p in inputs],
                    f'{mode}: source mutation')
            output = case/'current.csv'
            if mode not in ('good', 'changed_saved'):
                require(result.returncode != 0 and REJECTIONS[mode] in result.stderr,
                        f'{mode}: expected rejection absent: {result.stdout}{result.stderr}')
                require(not output.exists(), f'{mode}: published partial output')
                print(f'{mode}: rejected; inputs unchanged')
                continue
            require(result.returncode == 0, result.stdout+result.stderr)
            with output.open() as stream:
                rows = list(csv.DictReader(stream))
            require(len(rows) == 1110, 'wrong row count')
            require(sorted((int(r['plane']), int(r['group'])) for r in rows) ==
                    [(f,g) for f in range(1,4) for g in range(1,371)], 'wrong row coverage')
            for row in rows:
                floor, group = int(row['plane']), int(row['group'])
                require(int(row['snapshot']) == (3,1,2)[floor-1], 'mapping ignored')
                wanted = expected(floor, group)
                for name, value in wanted.items():
                    require(float(row[name]) == value, f'{name} mismatch: {row}')
                changed = mode == 'changed_saved' and floor == 2 and group == 1
                require(float(row['saved_leak']) == wanted['recomputed_leak'] + (0.125 if changed else 0),
                        'saved value was not retained')
                require(int(row['bitwise_equal']) == int(not changed), 'mismatch report incorrect')
                floors = [expected(f, group) for f in (1, 2, 3)]
                group_n = 0.0
                for f in floors:
                    group_n += f['numerator']
                bottom, top = -floors[0]['low_current'], floors[2]['high_current']
                require(float(row['group_numerator']) == group_n, 'group integral mismatch')
                require(float(row['bottom_outflow']) == bottom and
                        float(row['top_outflow']) == top, 'outward sign mismatch')
                require(float(row['telescoping_difference']) == group_n-(bottom+top),
                        'telescoping mismatch')
                for boundary in ('bottom', 'top'):
                    require(int(row[f'{boundary}_negative_outflow_regions']) == (132 if group == 2 else 0),
                            'negative boundary flow was hidden')
                require(int(row['nonpositive_flux_regions']) == 0, 'wrong positive flux count')
            # The group-3 perturbation vanishes in REAL32 but must survive here.
            special = next(r for r in rows if int(r['plane']) == 3 and int(r['group']) == 3)
            require(float(special['recomputed_leak']) != 0.0625, 'lost REAL64 current authority')
            previous = output.read_bytes()
            retry = run([host, 'track.xsm', 'axial.xsm', 'current.csv'], case, check=False)
            require(retry.returncode != 0 and output.read_bytes() == previous, 'overwrite allowed')
            print(f'{mode}: 1110 exact rows; permuted mapping; signed currents; REAL64 detail retained')
    print('D4A AXIAL CURRENT SYNTHETIC CHECKS COMPLETE; NO PHYSICS ACCEPTANCE')


if __name__ == '__main__':
    main()

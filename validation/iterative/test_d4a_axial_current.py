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
    'bad_mat1d': 'THREE CONTIGUOUS EQUAL CELL BLOCKS',
    'duplicate_snapshot': 'EACH SNAPSHOT IN EXACTLY ONE CELL BLOCK',
    'bad_snapshot': 'MAT1D',
    'bad_dimensions': 'INCONSISTENT D4-A TRACK/AXIAL DIMENSIONS',
}

FIXTURE = r"""
program fixture
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value,ieee_quiet_nan
  implicit none
  integer,parameter :: nr=132,ns=3,ng=370
  type(c_ptr) :: track,axial,fl64,fl32
  integer :: state(40),i,f,g,p,k,nz,nu,l4,l5,q,ios
  integer :: permutation(ns)=[3,1,2]
  integer,allocatable :: key(:),mapping(:),stored_mapping(:)
  real(real32) :: area(nr)
  real(real32),allocatable :: height(:),volume(:)
  real(real64) :: leak(ng*ns),num(ns),den(ns)
  real(real64),allocatable :: u(:),phi(:),jface(:)
  character(len=32) :: mode,argument
  call get_command_argument(1,mode)
  call get_command_argument(2,argument)
  read(argument,*,iostat=ios) nz
  if(ios/=0) error stop 'INVALID CELL COUNT.'
  if(nz/=3.and.nz/=6.and.nz/=12) error stop 'UNSUPPORTED FIXTURE CELL COUNT.'
  l4=3*nr*nz
  l5=nr*(nz+1)
  nu=l4+l5+8*nr
  allocate(key(nr*nz),mapping(nz),stored_mapping(nz),height(nz),volume(nr*nz))
  allocate(u(nu),phi(nz),jface(nz+1))
  call LCMOP(track,'track.xsm',0,2,0)
  call LCMPTC(track,'SIGNATURE',12,'L_TRACK     ')
  call LCMPTC(track,'TRACK-TYPE',12,'SPOT        ')
  state=0
  state(1)=nr*nz; state(2)=nu; state(6)=nr; state(7)=nz
  state(8)=ns; state(11)=l4; state(12)=l5
  if(mode=='bad_dimensions') state(8)=4
  call LCMPUT(track,'STATE-VECTOR',40,1,state)
  key=[(nr*nz+1-i,i=1,nr*nz)]
  if(mode=='bad_key') key(1)=nu+1
  do f=1,nz
    q=1+(f-1)/(nz/ns)
    mapping(f)=permutation(q)
  enddo
  stored_mapping=mapping
  if(mode=='bad_mat1d') stored_mapping(nz/ns)=1
  if(mode=='duplicate_snapshot') stored_mapping(nz/ns+1:2*nz/ns)=3
  if(mode=='bad_snapshot') stored_mapping(2*nz/ns+1:)=4
  area=2.0_real32
  do f=1,nz
    height(f)=real(f+1,real32)
  enddo
  if(nz==3) height=[2.0_real32,4.0_real32,8.0_real32]
  do i=1,nr
    do f=1,nz
      volume((i-1)*nz+f)=area(i)*height(f)
    enddo
  enddo
  call LCMPUT(track,'KEYFLX',nr*nz,1,key)
  call LCMPUT(track,'MAT1D',nz,1,stored_mapping)
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
    do f=1,nz
      phi(f)=real(2*f+1,real64)
    enddo
    if(nz==3) phi=[2.0_real64,4.0_real64,8.0_real64]
    if(mode=='zero_denominator') phi(nz/ns+1:2*nz/ns)=0.0_real64
    if(mode=='negative_flux') phi(nz/ns+1:2*nz/ns)=-phi(nz/ns+1:2*nz/ns)
    do f=1,nz+1
      jface(f)=real(f*(f+1)/2-4,real64)
    enddo
    if(g==2) jface=-jface
    if(g==3) jface(nz+1)=jface(nz+1)+2.0_real64**(-30)
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
    num=0.0_real64
    den=0.0_real64
    do f=1,nz
      p=mapping(f)
      do i=1,nr
        num(p)=num(p)+2.0_real64*(jface(f+1)-jface(f))
        den(p)=den(p)+2.0_real64*real(height(f),real64)*phi(f)
      enddo
    enddo
    do p=1,ns
      leak((p-1)*ng+g)=0.0_real64
      if(den(p)/=0.0_real64) leak((p-1)*ng+g)=num(p)/den(p)
    enddo
  enddo
  if(mode=='changed_saved') leak(1)=leak(1)+0.125_real64
  call LCMPUT(axial,'SPOT-X-L',ns*ng,4,leak)
  call LCMCL(axial,1)
end program fixture
"""


def run(command, cwd, check=True):
    return subprocess.run(list(map(str, command)), cwd=cwd, timeout=10,
                          capture_output=True, text=True, check=check)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def expected(floor, group, ncell=3, mode='good'):
    currents = [float(f*(f+1)//2 - 4) for f in range(1, ncell+2)]
    heights = [float(f+1) for f in range(1, ncell+1)]
    fluxes = [float(2*f+1) for f in range(1, ncell+1)]
    if ncell == 3:
        heights = fluxes = [2.0, 4.0, 8.0]
    cells_per_zone = ncell // 3
    first, last = (floor-1)*cells_per_zone, floor*cells_per_zone
    if mode == 'negative_flux':
        fluxes = [(-v if cells_per_zone <= i < 2*cells_per_zone else v)
                  for i, v in enumerate(fluxes)]
    if group == 2:
        currents = [-v for v in currents]
    if group == 3:
        currents[-1] += 2.0**-30
    low = high = num = den = 0.0
    for _ in range(132):
        low += 2.0 * currents[first]
        high += 2.0 * currents[last]
    for cell in range(first, last):
        for _ in range(132):
            num += 2.0 * (currents[cell+1] - currents[cell])
            den += 2.0 * heights[cell] * fluxes[cell]
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
        cases = [('good', 'good', 3), ('good6', 'good', 6), ('good12', 'good', 12),
                 ('changed_saved', 'changed_saved', 3),
                 ('changed_saved12', 'changed_saved', 12),
                 ('negative_flux12', 'negative_flux', 12)]
        cases.extend((mode, mode, 3) for mode in
                     ('zero_denominator', 'bad_key', 'bad_type', 'nan_field'))
        cases.extend((mode+'12', mode, 12) for mode in
                     ('zero_denominator', 'bad_mat1d', 'duplicate_snapshot',
                      'bad_snapshot', 'bad_dimensions'))
        for label, mode, ncell in cases:
            case = work / label
            case.mkdir()
            run([fixture, mode, ncell], case)
            inputs = [case/'track.xsm', case/'axial.xsm']
            before = [hashlib.sha256(p.read_bytes()).digest() for p in inputs]
            result = run([host, 'track.xsm', 'axial.xsm', 'current.csv'], case, check=False)
            require(before == [hashlib.sha256(p.read_bytes()).digest() for p in inputs],
                    f'{mode}: source mutation')
            output = case/'current.csv'
            if mode not in ('good', 'changed_saved', 'negative_flux'):
                require(result.returncode != 0 and REJECTIONS[mode] in result.stderr,
                        f'{mode}: expected rejection absent: {result.stdout}{result.stderr}')
                require(not output.exists(), f'{mode}: published partial output')
                print(f'{label}: rejected; inputs unchanged')
                continue
            require(result.returncode == 0, result.stdout+result.stderr)
            with output.open() as stream:
                rows = list(csv.DictReader(stream))
            require(len(rows) == 1110, 'wrong row count')
            require(sorted((int(r['plane']), int(r['group'])) for r in rows) ==
                    [(f,g) for f in range(1,4) for g in range(1,371)], 'wrong row coverage')
            reference = {(f, g): expected(f, g, ncell, mode)
                         for f in (1, 2, 3) for g in range(1, 371)}
            for row in rows:
                floor, group = int(row['plane']), int(row['group'])
                require(int(row['snapshot']) == (3,1,2)[floor-1], 'mapping ignored')
                wanted = reference[floor, group]
                for name, value in wanted.items():
                    require(float(row[name]) == value, f'{name} mismatch: {row}')
                changed = mode == 'changed_saved' and floor == 2 and group == 1
                require(float(row['saved_leak']) == wanted['recomputed_leak'] + (0.125 if changed else 0),
                        'saved value was not retained')
                require(int(row['bitwise_equal']) == int(not changed), 'mismatch report incorrect')
                require(float(row['leak_difference']) ==
                        wanted['recomputed_leak']-float(row['saved_leak']), 'wrong signed leak difference')
                require(float(row['face_integral_difference']) ==
                        wanted['high_current']-wanted['low_current']-wanted['numerator'],
                        'wrong face integral arithmetic')
                floors = [reference[f, group] for f in (1, 2, 3)]
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
                negative_count = 132*(ncell//3) if mode == 'negative_flux' and floor == 2 else 0
                require(int(row['nonpositive_flux_regions']) == negative_count,
                        'nonpositive cell-region flux was hidden')
            # The group-3 perturbation vanishes in REAL32 but must survive here.
            special = next(r for r in rows if int(r['plane']) == 3 and int(r['group']) == 3)
            require(float(special['recomputed_leak']) != reference[3, 1]['recomputed_leak'],
                    'lost REAL64 current authority')
            previous = output.read_bytes()
            retry = run([host, 'track.xsm', 'axial.xsm', 'current.csv'], case, check=False)
            require(retry.returncode != 0 and output.read_bytes() == previous, 'overwrite allowed')
            print(f'{label}: {ncell} cells -> 1110 exact rows; permuted mapping; signed currents; REAL64 detail retained')
    print('D4A AXIAL CURRENT SYNTHETIC CHECKS COMPLETE; NO PHYSICS ACCEPTANCE')


if __name__ == '__main__':
    main()

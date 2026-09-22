program test_d4a_region_rates
  ! Small synthetic fixture writer for export_d4a_region_rates; no transport.
  ! Run in an empty temporary directory. Each selected case writes three XSMs.
  ! The good case has NFIS=2, nontrivial KEYFLX, and an intentionally different
  ! FLUX64: these expose a wrong NUSIGF stride or an illicit FLUX64 substitution.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32,real64
  use, intrinsic :: ieee_arithmetic, only : ieee_value,ieee_quiet_nan
  implicit none
  integer, parameter :: nreg=396,nradial=132,nfloor=3,ngrp=370,nmix=18,nfis=2
  type(c_ptr) :: flux,track,macro,groups,groups64,item
  integer :: state(40),mat(nreg),key(nreg),i,f,r,g,j,mode_status
  real(real32) :: volume(nreg),field(nreg),nufis(nmix*nfis)
  real(real64) :: field64(nreg),nufis64(nmix*nfis)
  character(len=32) :: mode
  logical :: exists

  if (command_argument_count() /= 1) error stop 'ONE FIXTURE CASE REQUIRED.'
  call get_command_argument(1,mode,status=mode_status)
  if (mode_status /= 0) error stop 'INVALID CASE ARGUMENT.'
  select case(trim(mode))
  case('good','bad_key','duplicate_key','bad_material','bad_volume','nan_flux','flux64_type', &
       'nusigf_shape','nusigf_type','extra_fissile','missing_fissile','bad_dimensions')
  case default
    error stop 'UNKNOWN FIXTURE CASE.'
  end select
  inquire(file='flux.xsm',exist=exists)
  if (exists) error stop 'FIXTURE FILE ALREADY EXISTS.'
  inquire(file='track.xsm',exist=exists)
  if (exists) error stop 'FIXTURE FILE ALREADY EXISTS.'
  inquire(file='macro.xsm',exist=exists)
  if (exists) error stop 'FIXTURE FILE ALREADY EXISTS.'

  do r=1,nradial
    do f=1,nfloor
      i=(r-1)*nfloor+f
      mat(i)=2+(f-1)*6
      if (r <= 25) mat(i)=4+(f-1)*6
      key(i)=nreg+1-i
      volume(i)=real(r+f,real32)
    enddo
  enddo
  if (mode == 'bad_key') key(1)=nreg+1
  if (mode == 'duplicate_key') key(2)=key(1)
  if (mode == 'bad_material') mat(2)=8
  if (mode == 'bad_volume') volume(1)=-1.0_real32
  call LCMOP(track,'track.xsm',0,2,0)
  call LCMPTC(track,'SIGNATURE',12,'L_TRACK     ')
  call LCMPTC(track,'TRACK-TYPE',12,'SPOT        ')
  state=0
  state(1)=nreg
  state(2)=nreg
  state(4)=nmix
  state(6)=nradial
  state(7)=nfloor
  state(8)=nfloor
  if (mode == 'bad_dimensions') state(6)=nradial-1
  call LCMPUT(track,'STATE-VECTOR',40,1,state)
  call LCMPUT(track,'MATCOD',nreg,1,mat)
  call LCMPUT(track,'KEYFLX',nreg,1,key)
  call LCMPUT(track,'MAT1D',nfloor,1,[1,2,3])
  call LCMPUT(track,'VOLUME',nreg,2,volume)
  call LCMCL(track,1)

  call LCMOP(flux,'flux.xsm',0,2,0)
  call LCMPTC(flux,'SIGNATURE',12,'L_FLUX      ')
  state=0
  state(1)=ngrp
  state(2)=nreg
  call LCMPUT(flux,'STATE-VECTOR',40,1,state)
  groups=LCMLID(flux,'FLUX',ngrp)
  groups64=LCMLID(flux,'FLUX64',ngrp)
  do g=1,ngrp
    do i=1,nreg
      field(i)=real(g+nreg+1-i,real32)
    enddo
    if (mode == 'nan_flux' .and. g == 1) field(1)=ieee_value(1.0_real32,ieee_quiet_nan)
    field64=2.0_real64*real(field,real64)
    if (mode == 'flux64_type' .and. g == 1) then
      call LCMPDL(groups,g,nreg,4,field64)
    else
      call LCMPDL(groups,g,nreg,2,field)
    endif
    call LCMPDL(groups64,g,nreg,4,field64)
  enddo
  call LCMCL(flux,1)

  call LCMOP(macro,'macro.xsm',0,2,0)
  call LCMPTC(macro,'SIGNATURE',12,'L_MACROLIB  ')
  state=0
  state(1)=ngrp
  state(2)=nmix
  state(4)=nfis
  call LCMPUT(macro,'STATE-VECTOR',40,1,state)
  groups=LCMLID(macro,'GROUP',ngrp)
  do g=1,ngrp
    item=LCMDIL(groups,g)
    nufis=0.0_real32
    do f=1,nfloor
      j=4+(f-1)*6
      nufis(j)=real(g+f,real32)
      nufis(nmix+j)=real(2*g+f,real32)
      if (mode == 'missing_fissile' .and. f == 3) then
        nufis(j)=0.0_real32
        nufis(nmix+j)=0.0_real32
      endif
      if (mode == 'extra_fissile') nufis(j-2)=1.0_real32
    enddo
    if (mode == 'nusigf_shape' .and. g == 1) then
      call LCMPUT(item,'NUSIGF',nmix,2,nufis(:nmix))
    else if (mode == 'nusigf_type' .and. g == 1) then
      nufis64=real(nufis,real64)
      call LCMPUT(item,'NUSIGF',nmix*nfis,4,nufis64)
    else
      call LCMPUT(item,'NUSIGF',nmix*nfis,2,nufis)
    endif
  enddo
  call LCMCL(macro,1)
  write(*,'(A,A)') 'SYNTHETIC FIXTURE CREATED: ',trim(mode)
end program test_d4a_region_rates

program TEST_B2E_CURRENT_ADMISSION
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32
  use B2E_NOOP_PROBES
  use SPOR64_B2B, only : SPOR64_B2B_ADMISSION_FAILED, &
      SPOR64_B2B_INGRESS
  implicit none

  integer, parameter :: NENTRY=6, NMAT=8
  character(len=12) :: hentry(NENTRY)
  character(len=1024) :: scenario, flux_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: ientry(NENTRY), jentry(NENTRY), imerg(NMAT)
  integer :: length, record_type, status
  integer(int64) :: cutoff_visit64
  real(real32) :: eps32
  logical :: rec, limerg
  type(c_ptr) :: flux, macro, track, system, source, fresh
  type(c_ptr) :: kentry(NENTRY)
  type(FIL_file), target :: fake_track

  if (command_argument_count() /= 6) &
    error stop 'expected scenario plus five XSM paths'
  call get_command_argument(1,scenario)
  call get_command_argument(2,flux_path)
  call get_command_argument(3,macro_path)
  call get_command_argument(4,track_path)
  call get_command_argument(5,system_path)
  call get_command_argument(6,source_path)

  call LCMOP(flux,trim(flux_path),2,2,0)
  call LCMOP(macro,trim(macro_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call LCMOP(system,trim(system_path),2,2,0)
  call LCMOP(source,trim(source_path),2,2,0)
  if (.not. all([c_associated(flux),c_associated(macro), &
      c_associated(track),c_associated(system),c_associated(source)])) &
    error stop 'read-only XSM open failed'

  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  hentry=[character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
      'SYSTEM','FSOURCE']
  ientry=[2,2,2,3,2,2]
  jentry=[1,2,2,2,2,2]
  kentry=[flux,macro,track,c_loc(fake_track),system,source]
  imerg=1
  rec=.true.
  limerg=.false.
  eps32=transfer(int(z'348637bd',int32),eps32)

  select case(trim(scenario))
  case('real-restart','sour-free-restart')
    continue
  case('fresh-create')
    call LCMOP(fresh,'B2E-FRESH',0,1,0)
    if (.not. c_associated(fresh)) error stop 'fresh output create failed'
    ientry(1)=1
    jentry(1)=0
    kentry(1)=fresh
    rec=.false.
    limerg=.true.
  case default
    error stop 'unknown B2E scenario'
  end select

  call B2E_RESET_PROBES()
  call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
      0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
      rec,0,limerg,370,8,8,32,1,2,1,.false.,.true., &
      status,cutoff_visit64)
  if (status /= SPOR64_B2B_ADMISSION_FAILED) &
    error stop 'current blocked topology unexpectedly admitted'
  if (xdrta2_calls /= 0 .or. core_calls /= 0 .or. publisher_calls /= 0) &
    error stop 'blocked topology crossed the post-admission boundary'
  if (trim(scenario) == 'fresh-create') then
    if (spomoc_calls /= 0) error stop 'fresh output passed early topology guards'
    call LCMLEN(fresh,'SIGNATURE',length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      error stop 'fresh output mutated on rejection'
    call LCMCL(fresh,2)
  else
    if (spomoc_calls /= 1) error stop 'real restart did not reach schema guards'
  end if
  if (cutoff_visit64 /= 0_int64) error stop 'blocked topology visited cutoff'

  call LCMCL(source,1)
  call LCMCL(system,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(flux,1)
  write(*,'(A,1X,A)') 'B2E CURRENT-ADMISSION BLOCKED PASS',trim(scenario)
end program TEST_B2E_CURRENT_ADMISSION

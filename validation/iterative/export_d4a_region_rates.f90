program export_d4a_region_rates
  ! Read-only diagnostic: no transport and no convergence/acceptance decision.
  ! Input FLUX is deliberately the REAL32 mirror used by SPORATE, not FLUX64.
  ! Only SPORATE is called from the existing Dragon library, for a direct
  ! printout comparison; all archive access is through GANLIB read-only XSM.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64,real32,real64,error_unit
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40,nradial=132,nfloor=3,nreg=396,nmix=18
  integer, parameter :: nsnap=3,nbase=6,nfuel=25,max_xsm_path=72
  type(c_ptr) :: objects(3),jpflux,jpmacro,kpmacro
  character(len=1024) :: paths(4)
  character(len=12) :: names(3)=['AX_FLUX     ','AX_TRACK    ','AX_MACRO    ']
  integer :: iflux(nstate),itrack(nstate),imacro(nstate)
  integer :: mat(nreg),keyflx(nreg),mat1d(nfloor),ngrp,nunk,nfis
  integer :: i,igr,ireg,ibm,ifis,ifloor,isnap,radial,ilong,itylcm,out,ios
  real(real32) :: volume(nreg)
  real(real32), allocatable :: unknown(:),nufis(:)
  real(real64) :: rate(nsnap),region_rate(nreg),nusigf,total_rate,contribution
  logical :: fissile(nmix),fuel_radial(nradial),exists

  if (command_argument_count() /= 4) call fail( &
    'USAGE: export_d4a_region_rates FLUX_XSM TRACK_XSM MACROLIB_XSM OUTPUT_CSV')
  do i=1,4
    call get_command_argument(i,paths(i),status=ios)
    if (ios /= 0 .or. len_trim(paths(i)) == 0) call fail('INVALID PATH ARGUMENT.')
    if (i <= 3) then
      if (len_trim(paths(i)) > max_xsm_path) &
        call fail('XSM PATH EXCEEDS 72 CHARACTERS; USE SHORT READ-ONLY SYMLINKS.')
      inquire(file=trim(paths(i)),exist=exists)
      if (.not.exists) call fail('INPUT XSM DOES NOT EXIST: '//trim(paths(i)))
    endif
  enddo
  inquire(file=trim(paths(4)),exist=exists)
  if (exists) call fail('OUTPUT CSV ALREADY EXISTS; REFUSING TO OVERWRITE.')
  do i=1,3
    call LCMOP(objects(i),trim(paths(i)),2,2,0)
    call require_record(objects(i),'STATE-VECTOR',nstate,1)
  enddo
  call require_character(objects(1),'SIGNATURE','L_FLUX')
  call require_character(objects(2),'SIGNATURE','L_TRACK')
  call require_character(objects(2),'TRACK-TYPE','SPOT')
  call require_character(objects(3),'SIGNATURE','L_MACROLIB')
  call LCMGET(objects(1),'STATE-VECTOR',iflux)
  call LCMGET(objects(2),'STATE-VECTOR',itrack)
  call LCMGET(objects(3),'STATE-VECTOR',imacro)
  ngrp=iflux(1)
  nunk=itrack(2)
  nfis=imacro(4)
  if (ngrp /= 370 .or. imacro(1) /= ngrp .or. nunk <= 0 .or. &
      iflux(2) /= nunk .or. itrack(1) /= nreg .or. itrack(4) /= nmix .or. &
      itrack(6) /= nradial .or. itrack(7) /= nfloor .or. &
      itrack(8) /= nsnap .or. imacro(2) /= nmix) &
    call fail('INCONSISTENT D4-A FLUX/TRACK/MACROLIB DIMENSIONS.')
  if (nfis <= 0 .or. int(nfis,int64)*nmix > huge(nfis)) call fail('INVALID NFIS.')

  call require_record(objects(2),'MATCOD',nreg,1)
  call require_record(objects(2),'KEYFLX',nreg,1)
  call require_record(objects(2),'VOLUME',nreg,2)
  call require_record(objects(2),'MAT1D',nfloor,1)
  call LCMGET(objects(2),'MATCOD',mat)
  call LCMGET(objects(2),'KEYFLX',keyflx)
  call LCMGET(objects(2),'VOLUME',volume)
  call LCMGET(objects(2),'MAT1D',mat1d)
  if (any(mat1d /= [1,2,3])) call fail('D4-A FLOOR/SNAPSHOT MAP MUST BE 1,2,3.')
  if (any(mat < 1) .or. any(mat > nmix)) call fail('MATCOD INDEX OUT OF RANGE.')
  if (any(keyflx < 1) .or. any(keyflx > nunk)) call fail('KEYFLX INDEX OUT OF RANGE.')
  do i=1,nreg
    if (any(keyflx(:i-1) == keyflx(i))) call fail('DUPLICATE REGION KEYFLX INDEX.')
  enddo
  if (any(.not.ieee_is_finite(volume)) .or. any(volume <= 0.0_real32)) &
    call fail('VOLUME MUST BE FINITE AND POSITIVE IN ALL 396 REGIONS.')
  do radial=1,nradial
    ibm=mat((radial-1)*nfloor+1)
    if (ibm < 1 .or. ibm > nbase) call fail('INVALID FIRST-FLOOR BASE MATERIAL.')
    do ifloor=1,nfloor
      ireg=(radial-1)*nfloor+ifloor
      if (mat(ireg) /= ibm+(mat1d(ifloor)-1)*nbase) &
        call fail('INCONSISTENT SIX-MATERIAL SNAPSHOT OFFSETS.')
    enddo
  enddo

  allocate(unknown(nunk),nufis(nmix*nfis))
  call require_record(objects(1),'FLUX',ngrp,10)
  call require_record(objects(3),'GROUP',ngrp,10)
  jpflux=LCMGID(objects(1),'FLUX')
  jpmacro=LCMGID(objects(3),'GROUP')
  rate=0.0_real64
  region_rate=0.0_real64
  fissile=.false.
  ! Preserve SPORATE's igr -> ireg -> ifis order and floor accumulation.
  do igr=1,ngrp
    call LCMLEL(jpflux,igr,ilong,itylcm)
    if (ilong /= nunk .or. itylcm /= 2) &
      call fail('FLUX MUST CONTAIN NUNK REAL32 VALUES PER GROUP (NO FLUX64 FALLBACK).')
    call LCMGDL(jpflux,igr,unknown)
    if (any(.not.ieee_is_finite(unknown))) call fail('NON-FINITE FLUX UNKNOWN.')
    if (any(unknown(keyflx) <= 0.0_real32)) &
      call fail('REGION FLUX MUST BE POSITIVE IN ALL 396 REGIONS.')
    call LCMLEL(jpmacro,igr,ilong,itylcm)
    if (itylcm /= 0) call fail('MACROLIB GROUP ITEM MUST BE A DIRECTORY.')
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'NUSIGF',ilong,itylcm)
    if (ilong == 0) cycle
    if (ilong /= nmix*nfis .or. itylcm /= 2) &
      call fail('NUSIGF MUST BE REAL32 WITH MIXTURE-FASTEST NMIX*NFIS LAYOUT.')
    call LCMGET(kpmacro,'NUSIGF',nufis)
    if (any(.not.ieee_is_finite(nufis)) .or. any(nufis < 0.0_real32)) &
      call fail('NUSIGF MUST BE FINITE AND NONNEGATIVE.')
    ! D4-A's six-material snapshot layout assigns fuel to 4, 10, and 16.
    ! Check every mixture/component, including any mixture absent from MATCOD.
    do ibm=1,nmix
      if (mod(ibm-1,nbase)+1 == 4) cycle
      do ifis=1,nfis
        if (nufis((ifis-1)*nmix+ibm) /= 0.0_real32) &
          call fail('NONFUEL MATERIAL HAS NONZERO NUSIGF; FUEL MUST BE 4,10,16.')
      enddo
    enddo
    do ireg=1,nreg
      ibm=mat(ireg)
      ifloor=mod(ireg-1,nfloor)+1
      isnap=mat1d(ifloor)
      nusigf=0.0_real64
      do ifis=1,nfis
        nusigf=nusigf+real(nufis((ifis-1)*nmix+ibm),real64)
      enddo
      if (nusigf > 0.0_real64) fissile(ibm)=.true.
      contribution=real(volume(ireg),real64)* &
        real(unknown(keyflx(ireg)),real64)*nusigf
      rate(isnap)=rate(isnap)+contribution
      region_rate(ireg)=region_rate(ireg)+contribution
    enddo
  enddo
  total_rate=0.0_real64
  do isnap=1,nsnap
    total_rate=total_rate+rate(isnap)
  enddo
  if (.not.ieee_is_finite(total_rate) .or. total_rate <= 0.0_real64 .or. &
      any(.not.ieee_is_finite(region_rate))) call fail('INVALID INTEGRATED RATE.')
  if (.not.all(fissile([4,10,16]))) call fail('FISSILE MATERIALS MUST INCLUDE 4,10,16.')
  do radial=1,nradial
    fuel_radial(radial)=fissile(mat((radial-1)*nfloor+1))
    do ifloor=1,nfloor
      ireg=(radial-1)*nfloor+ifloor
      if (fissile(mat(ireg)) .neqv. fuel_radial(radial)) &
        call fail('FISSILE REGION SUPPORT DIFFERS BETWEEN FLOORS.')
      if (fuel_radial(radial)) then
        if (region_rate(ireg) <= 0.0_real64) call fail('NONPOSITIVE FUEL REGION RATE.')
      else
        if (region_rate(ireg) /= 0.0_real64) call fail('NONFUEL REGION HAS NONZERO RATE.')
      endif
    enddo
  enddo
  if (count(fuel_radial) /= nfuel) call fail('EXPECTED EXACTLY 25 FUEL RADIAL REGIONS.')

  write(*,'(A)') 'D4A-REGION DIAGNOSTIC_ONLY; NO CONVERGENCE OR FINAL ACCEPTANCE CLAIM'
  write(*,'(A)') 'D4A-REGION FLUX_PRECISION=REAL32 ACCUMULATION=REAL64'
  write(*,'(A)') 'D4A-REGION FISSILE_MATERIALS=4,10,16; OTHER NUSIGF COMPONENTS=0'
  write(*,'(A,I0,A,I0)') 'D4A-REGION CHECKED_REGIONS=',nreg,' EXPORTED_FUEL_REGIONS=',nfuel*nfloor
  write(*,'(A,ES24.16E3)') 'D4A-REGION GLOBAL_NU_FISSION_RATE ',total_rate
  write(*,'(A,1P,3E16.8)') 'D4A-REGION NU-FISSION-FRACTIONS ',rate/total_rate
  call SPORATE(3,names,[2,2,2],[2,2,2],objects)

  open(newunit=out,file=trim(paths(4)),status='new',action='write',iostat=ios)
  if (ios /= 0) call fail('CANNOT CREATE OUTPUT CSV.')
  write(out,'(A)') 'radial_region,floor,material,volume,nu_fission_rate,global_fraction'
  do radial=1,nradial
    if (.not.fuel_radial(radial)) cycle
    do ifloor=1,nfloor
      ireg=(radial-1)*nfloor+ifloor
      write(out,'(I0,2(A,I0),3(A,ES24.16E3))',iostat=ios) &
        radial,',',ifloor,',',mat(ireg),',',real(volume(ireg),real64), &
        ',',region_rate(ireg),',',region_rate(ireg)/total_rate
      if (ios /= 0) call fail('CSV WRITE FAILED.')
    enddo
  enddo
  close(out,iostat=ios)
  if (ios /= 0) call fail('CSV CLOSE FAILED.')
  do i=3,1,-1
    call LCMCL(objects(i),1)
  enddo

contains

  subroutine require_record(ptr,name,length_expected,type_expected)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    integer, intent(in) :: length_expected,type_expected
    integer :: length_actual,type_actual
    call LCMLEN(ptr,name,length_actual,type_actual)
    if (length_actual /= length_expected .or. type_actual /= type_expected) &
      call fail('INVALID RECORD LENGTH/TYPE: '//trim(name))
  end subroutine require_record

  subroutine require_character(ptr,name,expected)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,expected
    character(len=12) :: value
    call require_record(ptr,name,3,3)
    call LCMGTC(ptr,name,12,value)
    if (value /= expected) call fail('INVALID CHARACTER RECORD: '//trim(name))
  end subroutine require_character

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(error_unit,'(A)') 'D4A-REGION ERROR: '//trim(message)
    error stop 1
  end subroutine fail

end program export_d4a_region_rates

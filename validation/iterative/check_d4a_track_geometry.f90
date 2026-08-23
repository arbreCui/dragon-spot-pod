program check_d4a_track_geometry
  ! Independent GANLIB-only check of the real D4-A geometry TRACK.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,real32
  implicit none

  integer, parameter :: nstate=40,nreg=132,nmat=6,nsurf=12,nunk=144
  integer, parameter :: ncode=6
  integer(int32), parameter :: mccg_epsi_bits=int(z'3727c5ac',int32)
  integer, parameter :: max_path=72
  type(c_ptr) :: track
  character(len=1024) :: path
  character(len=12) :: signature,track_type
  integer :: state(nstate),mccg_state(nstate)
  integer :: matcod(nreg),keyflx(nreg),keyflx_anis(nreg)
  integer :: keycur(nsurf),nzon(nunk),icode(ncode),bc(nsurf)
  real(real32) :: volume(nreg),v_mccg(nunk),albedo(ncode),real_param(4)
  logical :: seen(nunk)
  integer :: i

  if (command_argument_count() /= 1) &
    call fail('EXPECTED ONE TRACK XSM PATH.')
  call get_command_argument(1,path)
  if ((len_trim(path) == 0).or.(len_trim(path) > max_path)) &
    call fail('XSM PATH IS EMPTY OR EXCEEDS THE GANLIB LIMIT.')

  call LCMOP(track,trim(path),2,2,0)
  call require_record(track,'SIGNATURE',3,3)
  call require_record(track,'TRACK-TYPE',3,3)
  call LCMGTC(track,'SIGNATURE',12,signature)
  call LCMGTC(track,'TRACK-TYPE',12,track_type)
  if (signature /= 'L_TRACK') call fail('L_TRACK SIGNATURE EXPECTED.')
  if (track_type /= 'MCCG') call fail('MCCG TRACK TYPE EXPECTED.')

  call require_record(track,'STATE-VECTOR',nstate,1)
  call require_record(track,'MCCG-STATE',nstate,1)
  call require_record(track,'REAL-PARAM',4,2)
  call LCMGET(track,'STATE-VECTOR',state)
  call LCMGET(track,'MCCG-STATE',mccg_state)
  call LCMGET(track,'REAL-PARAM',real_param)
  if ((state(1) /= nreg).or.(state(2) /= nunk).or. &
      (state(3) /= 1).or.(state(4) /= nmat).or. &
      (state(5) /= nsurf).or.(state(6) /= 1)) &
    call fail('D4-A STATE(1:6) IS NOT (132,144,1,6,12,1).')
  if (mccg_state(19) /= 1 .or. mccg_state(20) /= 1) &
    call fail('ISOTROPIC MCCG UNKNOWN LAYOUT EXPECTED.')
  if (any(.not.ieee_is_finite(real_param))) &
    call fail('NON-FINITE MCCG REAL-PARAM.')
  if (transfer(real_param(1),0_int32) /= mccg_epsi_bits .or. &
      any(transfer(real_param(2:4),0_int32,3) /= 0_int32)) &
    call fail('MCCG REAL-PARAM DOES NOT MATCH THE PRODUCTION CONTRACT.')

  call require_record(track,'MATCOD',nreg,1)
  call require_record(track,'VOLUME',nreg,2)
  call require_record(track,'KEYFLX',nreg,1)
  call require_record(track,'KEYFLX$ANIS',nreg,1)
  call require_record(track,'V$MCCG',nunk,2)
  call require_record(track,'NZON$MCCG',nunk,1)
  call require_record(track,'KEYCUR$MCCG',nsurf,1)
  call require_record(track,'ICODE',ncode,1)
  call require_record(track,'ALBEDO',ncode,2)
  call require_record(track,'BC-REFL+TRAN',nsurf,1)

  call LCMGET(track,'MATCOD',matcod)
  call LCMGET(track,'VOLUME',volume)
  call LCMGET(track,'KEYFLX',keyflx)
  call LCMGET(track,'KEYFLX$ANIS',keyflx_anis)
  call LCMGET(track,'V$MCCG',v_mccg)
  call LCMGET(track,'NZON$MCCG',nzon)
  call LCMGET(track,'KEYCUR$MCCG',keycur)
  call LCMGET(track,'ICODE',icode)
  call LCMGET(track,'ALBEDO',albedo)
  call LCMGET(track,'BC-REFL+TRAN',bc)

  if (any(matcod < 1).or.any(matcod > nmat)) &
    call fail('MATCOD IS OUTSIDE THE SIX-MEDIUM D4-A GEOMETRY.')
  if (any(nzon(:nreg) /= matcod)) &
    call fail('MCCG REGION CODES DO NOT MATCH MATCOD.')
  if (any(nzon(nreg+1:) >= 0).or. &
      any(abs(nzon(nreg+1:)) > ncode)) &
    call fail('MCCG SURFACE CODES ARE NOT SIX-SLOT BOUNDARY CODES.')
  if (any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0_real32)) &
    call fail('INVALID REGION VOLUMES.')
  if (any(.not.ieee_is_finite(v_mccg)).or.any(v_mccg <= 0.0_real32)) &
    call fail('INVALID MCCG REGION/SURFACE MEASURES.')
  if (any(.not.ieee_is_finite(albedo))) call fail('NON-FINITE ALBEDO.')
  if (any(bc < 1).or.any(bc > nsurf)) &
    call fail('INVALID 12-SURFACE REFLECTION/TRANSMISSION MAP.')

  seen=.false.
  do i=1,nreg
    if ((keyflx(i) < 1).or.(keyflx(i) > nunk)) &
      call fail('KEYFLX INDEX OUT OF RANGE.')
    if (keyflx_anis(i) /= keyflx(i)) &
      call fail('ISOTROPIC KEYFLX RECORDS DIFFER.')
    if (seen(keyflx(i))) call fail('DUPLICATE REGION UNKNOWN INDEX.')
    seen(keyflx(i))=.true.
  enddo
  do i=1,nsurf
    if ((keycur(i) < 1).or.(keycur(i) > nunk)) &
      call fail('KEYCUR INDEX OUT OF RANGE.')
    if (seen(keycur(i))) call fail('DUPLICATE SURFACE UNKNOWN INDEX.')
    seen(keycur(i))=.true.
  enddo
  if (.not.all(seen)) call fail('REGION/SURFACE KEYS DO NOT COVER NUNK.')

  call LCMCL(track,1)
  write(*,'(A)') &
    'D4A-TRACK TUPLE NREG=132 NMAT=6 NSURF=12 NUNK=144 NCODE=6 EPSI=1E-5'
  write(*,'(A)') &
    'D4A-TRACK LENGTHS MATCOD=132 VOLUME=132 V$MCCG=144 ' // &
    'NZON$MCCG=144 KEYFLX=132 KEYCUR$MCCG=12 ICODE=6 ALBEDO=6 BC=12'
  write(*,'(A)') 'D4A-TRACK GEOMETRY-ONLY PASS'

contains

  subroutine require_record(ptr,name,length_expected,type_expected)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    integer, intent(in) :: length_expected,type_expected
    integer :: length_actual,type_actual
    character(len=160) :: message
    call LCMLEN(ptr,name,length_actual,type_actual)
    if ((length_actual /= length_expected).or. &
        (type_actual /= type_expected)) then
      write(message,'(A,A,A,I0,A,I0,A,I0,A,I0)') &
        'RECORD ',trim(name),' EXPECTED LENGTH/TYPE ',length_expected,'/', &
        type_expected,' FOUND ',length_actual,'/',type_actual
      call fail(trim(message))
    endif
  end subroutine require_record

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(*,'(A,A)') 'D4A-TRACK GEOMETRY-ONLY FAIL: ',trim(message)
    error stop 1
  end subroutine fail

end program check_d4a_track_geometry

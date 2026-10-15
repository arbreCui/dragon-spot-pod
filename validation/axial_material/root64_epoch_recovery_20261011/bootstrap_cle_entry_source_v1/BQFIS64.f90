! NEW SOURCE: standard CLE entry for the complete bootstrap QFISS64 path.
! Ordered operands: MACRO_OUT SOURCE_OUT PROJECTED GLOBAL64 AX AXTRACK
!                   AXSYSTEM AXMACRO ARCHIVE RCON.
! Syntax is exactly :: PLANE 1 ;, :: PLANE 2 ; or :: PLANE 3 ;.
subroutine BQFIS64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated
  use, intrinsic :: iso_fortran_env, only: real64
  use SPOR64_VERIFY, only: EMPTY_ROOT
  use SPOR64_BOOTQ64_V2, only: SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_READ, &
      SPOR64_BOOTQ64_COMMITTED,SPOR64_BOOTQ64_LOADED
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  integer :: i,j,object_length,plane_index,status,token_type,token_integer
  real :: token_real
  double precision :: token_double
  real(real64), allocatable :: verified_q64(:,:)
  real(real64) :: verified_rho64
  character(len=12) :: token_text,object_directory
  character(len=72) :: object_file
  logical :: object_empty,is_lcm

  if(nentry/=10) call XABORT('BQFIS64: EXACT TEN ORDERED OPERANDS REQUIRED.')
  if(any((ientry/=1).and.(ientry/=2))) &
      call XABORT('BQFIS64: ONLY LCM/XSM OPERANDS ALLOWED.')
  if(any(jentry(1:2)/=0).or.any(jentry(3:10)/=2)) &
      call XABORT('BQFIS64: TWO FRESH OUTPUTS AND EIGHT READONLY INPUTS REQUIRED.')
  do i=1,nentry
    if(.not.c_associated(kentry(i))) call XABORT('BQFIS64: NULL OPERAND.')
    if(len_trim(hentry(i))==0) call XABORT('BQFIS64: EMPTY CLE OBJECT NAME.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
          call XABORT('BQFIS64: OPERAND ALIAS OR REPEATED CLE NAME.')
    enddo
    call LCMINF(kentry(i),object_file,object_directory,object_empty,object_length,is_lcm)
    if(object_length/=-1.or.trim(object_directory)/='/') &
        call XABORT('BQFIS64: ROOT DIRECTORY OPERANDS REQUIRED.')
    if((ientry(i)==1).neqv.is_lcm) &
        call XABORT('BQFIS64: CLE STORAGE DESCRIPTOR MISMATCH.')
  enddo
  do i=1,2
    if(.not.EMPTY_ROOT(kentry(i))) call XABORT('BQFIS64: OUTPUT MUST BE EMPTY.')
  enddo

  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/='PLANE') &
      call XABORT('BQFIS64: MANDATORY UNIQUE PLANE KEYWORD REQUIRED.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=1) call XABORT('BQFIS64: INTEGER PLANE REQUIRED.')
  plane_index=token_integer
  if(plane_index<1.or.plane_index>3) &
      call XABORT('BQFIS64: PLANE MUST BE ONE THROUGH THREE.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('BQFIS64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.')

  ! Full PROJECTED-BOOT/e0 admission precedes every output mutation.
  ! All 370 groups and 32 fission slots use the frozen original formula.
  ! The full selected macrolib is cloned; only NUSIGF physical records
  ! are cleared. DSOUR32 is a mirror of the actual type-4 QFISS authority.
  call SPOR64_BOOTQ64_BUILD(kentry(3),kentry(4),kentry(5),kentry(6), &
      kentry(7),kentry(8),kentry(9),kentry(10),plane_index, &
      kentry(1),kentry(2),status)
  if(status/=SPOR64_BOOTQ64_COMMITTED) &
      call XABORT('BQFIS64: COMPLETE QFISS ADMISSION OR COMMIT FAILED.')

  ! Actual independent recomputation and full-tree comparison, not metadata.
  ! A committed output whose complete readback fails is never returned.
  call SPOR64_BOOTQ64_READ(kentry(3),kentry(4),kentry(5),kentry(6), &
      kentry(7),kentry(8),kentry(9),kentry(10),plane_index, &
      kentry(1),kentry(2),verified_q64,verified_rho64,status)
  if(status/=SPOR64_BOOTQ64_LOADED) &
      call XABORT('BQFIS64: COMMITTED OUTPUT COMPLETE READBACK FAILED.')
  if(.not.allocated(verified_q64)) &
      call XABORT('BQFIS64: REAL64 READBACK ARRAY MISSING.')
  if(size(verified_q64,1)<=0.or.size(verified_q64,2)/=370) &
      call XABORT('BQFIS64: REAL64 READBACK SHAPE MISMATCH.')
  deallocate(verified_q64)
end subroutine BQFIS64

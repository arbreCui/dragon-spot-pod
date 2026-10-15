! NEW SOURCE: standard CLE entry for the complete bootstrap projection.
! Ordered operands: PROJECTED_OUT GLOBAL64 AX AXTRACK AXSYSTEM AXMACRO ARCHIVE RCON.
! Syntax is exactly :: RANK 1 ; or :: RANK 2 ;. No default or rank fallback.
subroutine BPROJX64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated
  use SPOR64_XSM_STORE64, only: EMPTY_XSM_ROOT
  use SPOR64_BOOT_PROJECTX64, only: SPOR64_BOOT_PROJECT_ARCHIVE, &
      SPOR64_BOOT_PROJECT_COMMITTED
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  integer :: i,j,object_length,requested_rank,status,token_type,token_integer
  real :: token_real
  double precision :: token_double
  character(len=12) :: token_text,object_directory
  character(len=72) :: object_file
  logical :: object_empty,is_lcm

  if(nentry/=8) call XABORT('BPROJX64: EXACT EIGHT ORDERED OPERANDS REQUIRED.')
  if(any((ientry/=1).and.(ientry/=2))) &
      call XABORT('BPROJX64: ONLY LCM/XSM OPERANDS ALLOWED.')
  if(jentry(1)/=0.or.any(jentry(2:8)/=2)) &
      call XABORT('BPROJX64: FRESH OUTPUT AND SEVEN READONLY INPUTS REQUIRED.')
  do i=1,nentry
    if(.not.c_associated(kentry(i))) call XABORT('BPROJX64: NULL OPERAND.')
    if(len_trim(hentry(i))==0) call XABORT('BPROJX64: EMPTY CLE OBJECT NAME.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
          call XABORT('BPROJX64: OPERAND ALIAS OR REPEATED CLE NAME.')
    enddo
    call LCMINF(kentry(i),object_file,object_directory,object_empty,object_length,is_lcm)
    if(object_length/=-1.or.trim(object_directory)/='/') &
        call XABORT('BPROJX64: ROOT DIRECTORY OPERANDS REQUIRED.')
    if((ientry(i)==1).neqv.is_lcm) &
        call XABORT('BPROJX64: CLE STORAGE DESCRIPTOR MISMATCH.')
  enddo
  if(ientry(1)/=2) call XABORT('BPROJX64: PRIVATE XSM OUTPUT REQUIRED.')
  if(.not.EMPTY_XSM_ROOT(kentry(1))) call XABORT('BPROJX64: OUTPUT MUST BE EMPTY.')

  ! Consume exactly one keyword, one integer and the terminating semicolon.
  ! The independent host binds this explicit rank to the frozen owning case.
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/='RANK') &
      call XABORT('BPROJX64: MANDATORY UNIQUE RANK KEYWORD REQUIRED.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=1) call XABORT('BPROJX64: INTEGER RANK REQUIRED.')
  requested_rank=token_integer
  if(requested_rank/=1.and.requested_rank/=2) &
      call XABORT('BPROJX64: RANK MUST BE EXACTLY ONE OR TWO.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('BPROJX64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.')

  ! The callee checks GLOBAL64 against all six independent physical inputs,
  ! recomputes the full canonical state and checks every requested rank.
  ! It publishes only PROJECTED-BOOT/e0, commits EPOCH last, and performs
  ! complete caller-output readback. This is not a transport or SVD gate.
  call SPOR64_BOOT_PROJECT_ARCHIVE(kentry(1),kentry(2),kentry(3),kentry(4), &
      kentry(5),kentry(6),kentry(7),kentry(8),requested_rank,status)
  if(status/=SPOR64_BOOT_PROJECT_COMMITTED) &
      call XABORT('BPROJX64: COMPLETE PROJECTION ADMISSION OR COMMIT FAILED.')
end subroutine BPROJX64

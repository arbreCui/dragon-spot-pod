! NEW SOURCE. This entry imports a native ROOT64 seed after full admission.
! It does not modify the original BOOT routine or select a REAL32 fallback.
subroutine SPOBOOT64(nentry,hentry,ientry,jentry,kentry)
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use GANLIB
  use SPOR64_BOOT64, only : ROOT64_IMPORTED, SPOR64_BOOT64_IMPORT_NATIVE
  use SPOR64_VERIFY, only : CHARACTER_RECORD_MATCHES, EXACT_INVENTORY, RECORD_MATCHES
  implicit none
  integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  character(len=12), parameter :: names(7) = &
      ['FLUX        ','FLUX_OLD    ','TRACK       ','SYSTEM      ', &
       'MICROLIB2   ','RCONTRACT   ','BOOT_BIND   ']
  character(len=12), parameter :: bind_names(3) = &
      ['SIGNATURE   ','PLANE       ','EPOCH       ']
  integer :: plane, epoch, status, i, token_type, token_integer
  real :: token_real
  double precision :: token_double
  character(len=4) :: token_text

  if (nentry /= 7) call XABORT('SPOBOOT64: SEVEN ENTRIES REQUIRED.')
  if (any(hentry /= names)) call XABORT('SPOBOOT64: ENTRY ORDER CHANGED.')
  if (ientry(1) /= 1 .or. jentry(1) /= 0) &
      call XABORT('SPOBOOT64: FRESH MEMORY OUTPUT REQUIRED.')
  if (any((ientry(2:7) /= 1).and.(ientry(2:7) /= 2))) &
      call XABORT('SPOBOOT64: LCM INPUTS REQUIRED.')
  if (any(jentry(2:7) /= 2)) call XABORT('SPOBOOT64: READONLY INPUTS REQUIRED.')
  do i = 1, nentry
    if (.not. c_associated(kentry(i))) call XABORT('SPOBOOT64: NULL ENTRY.')
  end do
  if (.not. EXACT_INVENTORY(kentry(7),bind_names)) &
      call XABORT('SPOBOOT64: INDEPENDENT BINDING INVENTORY REQUIRED.')
  if (.not. CHARACTER_RECORD_MATCHES(kentry(7),'SIGNATURE',3,12,'L_BOOTBIND')) &
      call XABORT('SPOBOOT64: INDEPENDENT BINDING SIGNATURE REQUIRED.')
  if (.not. RECORD_MATCHES(kentry(7),'PLANE',1,1)) &
      call XABORT('SPOBOOT64: PLANE RECORD REQUIRED.')
  if (.not. RECORD_MATCHES(kentry(7),'EPOCH',1,1)) &
      call XABORT('SPOBOOT64: EPOCH RECORD REQUIRED.')
  call LCMGET(kentry(7),'PLANE',plane)
  call LCMGET(kentry(7),'EPOCH',epoch)
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if (token_type /= 3 .or. token_text /= ';') &
      call XABORT('SPOBOOT64: ONLY TERMINATING SEMICOLON IS ALLOWED.')
  call SPOR64_BOOT64_IMPORT_NATIVE(kentry(1),kentry(2),kentry(3), &
      kentry(4),kentry(5),kentry(6),plane,epoch,status)
  if (status /= ROOT64_IMPORTED) call XABORT('SPOBOOT64: ROOT64 ADMISSION FAILED.')
end subroutine SPOBOOT64

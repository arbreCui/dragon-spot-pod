! NEW SOURCE: independent constants for ROOT64_NEW_WARM_A3_20261012.
! Creates case operands only. It never certifies a solve or an epoch closure.
subroutine AXNCASEA364(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: int32,real32
  use SPOR64_VERIFY, only: EMPTY_MEMORY_ROOT,EXACT_INVENTORY, &
      CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  character(len=12), parameter :: names(2)=['RCONTRACT   ','BOOT_BIND   ']
  character(len=12), parameter :: route_names(6)= &
      ['SIGNATURE   ','CASE-NAME   ','EPS-TERMINAL','FLU-CAPS    ', &
       'FLU-ACCE    ','FLU-OPTION  ']
  character(len=12), parameter :: bind_names(3)= &
      ['SIGNATURE   ','PLANE       ','EPOCH       ']
  character(len=12), parameter :: case12='R64-A3-WARM1 '
  real(real32), parameter :: eps(3)=[2.5e-7_real32,5.0e-8_real32,2.5e-8_real32]
  integer, parameter :: caps(2)=[500,740],acce(2)=[3,3],plane=3,epoch=0
  type(SPOR64_ROUTE_CONTRACT) :: contract
  logical :: loaded
  integer :: i,token_type,token_integer,read_plane,read_epoch
  real :: token_real
  double precision :: token_double
  character(len=4) :: token_text
  if(nentry/=2) call XABORT('AXNCASEA364: TWO FRESH CASE OUTPUTS REQUIRED.')
  if(any(hentry/=names).or.any(ientry/=1).or.any(jentry/=0)) &
      call XABORT('AXNCASEA364: EXACT FRESH MEMORY OUTPUT ORDER REQUIRED.')
  do i=1,2
    if(.not.c_associated(kentry(i))) call XABORT('AXNCASEA364: NULL OUTPUT.')
    if(.not.EMPTY_MEMORY_ROOT(kentry(i))) call XABORT('AXNCASEA364: OUTPUT NOT EMPTY.')
  enddo
  if(c_associated(kentry(1),kentry(2))) call XABORT('AXNCASEA364: OUTPUT ALIAS.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('AXNCASEA364: ONLY THE DECLARED CASE IS ALLOWED.')
  ! Same mandatory LCM ABI as the retained independent RCONTRACT builder.
  call LCMPTC(kentry(1),'SIGNATURE',12,'L_RCONTRACT ')
  call LCMPTC(kentry(1),'CASE-NAME',12,case12)
  call LCMPUT(kentry(1),'EPS-TERMINAL',3,2,eps)
  call LCMPUT(kentry(1),'FLU-CAPS',2,1,caps)
  call LCMPUT(kentry(1),'FLU-ACCE',2,1,acce)
  call LCMPTC(kentry(1),'FLU-OPTION',4,'B0  ')
  call LCMPTC(kentry(2),'SIGNATURE',12,'L_BOOTBIND  ')
  call LCMPUT(kentry(2),'PLANE',1,1,plane)
  call LCMPUT(kentry(2),'EPOCH',1,1,epoch)
  ! Structural/bit checks prove only the case declaration was constructed.
  call SPOR64_RCONTRACT_LOAD(kentry(1),contract,loaded)
  if(.not.loaded) call XABORT('AXNCASEA364: DECLARATION LOAD REFUSED.')
  if(.not.EXACT_INVENTORY(kentry(1),route_names).or. &
      .not.EXACT_INVENTORY(kentry(2),bind_names)) &
      call XABORT('AXNCASEA364: INCOMPLETE DECLARATION INVENTORY.')
  if(contract%case_name/=case12.or. &
      contract%eps_radial_bits/=transfer(eps(1),0_int32).or. &
      contract%eps_axial_bits/=transfer(eps(2),0_int32).or. &
      contract%eps_mccg_bits/=transfer(eps(3),0_int32).or. &
      contract%flu_maxout/=caps(1).or.contract%flu_maxinr/=caps(2).or. &
      contract%flu_acce_free/=acce(1).or.contract%flu_acce_accel/=acce(2).or. &
      contract%flu_option/='B0  ') call XABORT('AXNCASEA364: CASE BITS MISMATCH.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(2),'SIGNATURE',3,12,'L_BOOTBIND').or. &
      .not.RECORD_MATCHES(kentry(2),'PLANE',1,1).or. &
      .not.RECORD_MATCHES(kentry(2),'EPOCH',1,1)) &
      call XABORT('AXNCASEA364: BINDING TYPE/SHAPE MISMATCH.')
  call LCMGET(kentry(2),'PLANE',read_plane)
  call LCMGET(kentry(2),'EPOCH',read_epoch)
  if(read_plane/=plane.or.read_epoch/=epoch) call XABORT('AXNCASEA364: BINDING BITS MISMATCH.')
end subroutine AXNCASEA364

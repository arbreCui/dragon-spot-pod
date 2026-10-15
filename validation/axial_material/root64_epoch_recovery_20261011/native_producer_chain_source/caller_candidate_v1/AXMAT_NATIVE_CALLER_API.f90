module AXMAT_NATIVE_CALLER_API
  ! NEW SOURCE: explicit interface of the complete isolated FLUDRVN64.
  ! Real native terminal arrays are returned to FLUNAT64 for publication
  ! only after all original FLU checks and complete headers have finished.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only : int32,real32,real64
  implicit none
  private
  integer, parameter :: kind_guard=1/merge(1,0, &
    kind(1)==int32.and.kind(1.0)==real32.and.kind(0.0d0)==real64.and.dp==real64)
  public :: FLUDRVN64
  interface
    subroutine FLUDRVN64(iprt,ipflux,iptrk,ipmacr,ipsou,iftrak,ipsys, &
        iphase,itpij,cxdoor,itranc,title,b2,initfl,lforw,leaksw,irebal, &
        ngrp,nmat,nifis,nanis,nlf,nlin,nfunl,option,nun,maxinr,epsinr, &
        maxout,epsunk,epsout,ifritr,iacitr,itypec,ileak,nreg,nsout, &
        matcod,keyflx,vol,refkef,nmerg,imerg,imcaud,lr64,lnative, &
        terminal_flux64,terminal_source64,terminal_keff64,terminal_resid64, &
        terminal_counters,terminal_inner_state,terminal_valid)
      import :: c_ptr,real32,real64
      type(c_ptr) :: ipflux,iptrk,ipmacr,ipsou,ipsys
      character(len=12) :: cxdoor
      character(len=72) :: title
      character(len=4) :: option
      integer :: iprt,iftrak,iphase,itpij,itranc,initfl,irebal,ngrp,nmat,nifis
      integer :: nanis,nlf,nlin,nfunl,nun,maxinr,maxout,ifritr,iacitr,itypec
      integer :: ileak,nreg,nsout,matcod(nreg),keyflx(nreg,nlin,nfunl)
      integer :: nmerg,imerg(nmat),imcaud
      real(real32) :: epsunk,epsinr,epsout,b2(4),vol(nreg)
      real(real64) :: refkef
      logical :: lforw,leaksw,lr64
      logical, intent(in) :: lnative
      real(real64), allocatable, intent(out) :: terminal_flux64(:,:),terminal_source64(:,:)
      real(real64), intent(out) :: terminal_keff64,terminal_resid64(3)
      integer, intent(out) :: terminal_counters(2),terminal_inner_state
      logical, intent(out) :: terminal_valid
    end subroutine FLUDRVN64
  end interface
end module AXMAT_NATIVE_CALLER_API

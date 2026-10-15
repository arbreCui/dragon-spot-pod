module SPOT_GLOBAL_TYPED_DRIVER_API
  ! Complete typed-driver ABI only; no caller, solve or seal is executed here.
  ! Original TYPE3 B1HOM64 precision boundary remains explicit in the manifest.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  implicit none
  private
  integer, parameter :: kind_guard=1/merge(1,0, &
    kind(1)==int32.and.kind(1.0)==real32.and.kind(0.0d0)==real64.and.dp==real64)
  public :: SPOT_GLOBAL_TYPED_DRIVER64
  interface
    subroutine SPOT_GLOBAL_TYPED_DRIVER64(iprt,ipmacr,ipflux,ipsys,iptrk,ipflup,ipsou, &
        igpt,iftrak,cxdoor,title,nunkno,nreg,nsout,nanis,nlf,nlin,nfunl, &
        ngrp,nmat,nifis,lforw,leaksw,maxinr,epsinr,maxout,epsunk,epsout, &
        ncptl,ncpta,itypec,iphase,itpij,ileak,option,refkef,matcod, &
        keyflx,vol,xstrc,xsdia,xsnuf,xschi,lrebal,initfl,nmerg,imerg, &
        initial_flux64,terminal_flux64,terminal_source64,terminal_keff64, &
        terminal_resid64,terminal_counters,terminal_inner_state,terminal_valid)
      import :: c_ptr,real32,real64
      type(c_ptr) :: ipmacr,ipflux,ipsys,iptrk,ipflup,ipsou
      integer :: iprt,igpt,iftrak,nunkno,nreg,nsout,nanis,nlf,nlin,nfunl
      integer :: ngrp,nmat,nifis,maxinr,maxout,ncptl,ncpta,itypec,iphase,itpij
      integer :: ileak,initfl,nmerg,matcod(nreg),keyflx(nreg,nlin,nfunl),imerg(nmat)
      real(real32) :: epsinr,epsunk,epsout,vol(nreg),xstrc(0:nmat,ngrp)
      real(real32) :: xsdia(0:nmat,0:nanis,ngrp),xsnuf(0:nmat,nifis,ngrp)
      real(real32) :: xschi(0:nmat,nifis,ngrp)
      character(len=12) :: cxdoor
      character(len=72) :: title
      character(len=4) :: option
      logical :: lforw,leaksw,lrebal
      real(real64) :: refkef
      real(real64), intent(in) :: initial_flux64(nunkno,ngrp)
      real(real64), intent(out) :: terminal_flux64(nunkno,ngrp)
      real(real64), intent(out) :: terminal_source64(nunkno,ngrp),terminal_keff64
      real(real64), intent(out) :: terminal_resid64(3)
      integer, intent(out) :: terminal_counters(2),terminal_inner_state
      logical, intent(out) :: terminal_valid
    end subroutine SPOT_GLOBAL_TYPED_DRIVER64
  end interface
end module SPOT_GLOBAL_TYPED_DRIVER_API

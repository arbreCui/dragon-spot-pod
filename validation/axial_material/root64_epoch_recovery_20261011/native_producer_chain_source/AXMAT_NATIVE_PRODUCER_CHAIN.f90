module AXMAT_NATIVE_PRODUCER_CHAIN
  ! NEW SOURCE: strict typed ingress and post-FLUDRV publication helpers.
  ! No transport is performed here. The explicit interface below refers to
  ! the complete transformed native kernel in AXMAT_CONTINUOUS_DRIVER64.f.
  ! A host must independently bind every input/context full EOF SHA and 7ID.
  ! Loading an old terminal as a warm guess grants no old qualification.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_BOOT64, only : SPOR64_BOOT64_PUBLISH_NATIVE, ROOT64_REFUSED
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT, SPOR64_RCONTRACT_LOAD
  implicit none
  private
  integer, parameter :: nstate=40, required_groups=370, required_unknowns=14
  integer, parameter :: kind_guard=1/merge(1,0, &
    kind(1)==int32.and.kind(1.0)==real32.and.kind(0.0d0)==real64.and.dp==real64)
  integer, parameter, public :: AXMAT_SEED64_REFUSED=0, AXMAT_SEED64_LOADED=1
  public :: AXMAT_CONTINUOUS_DRIVER64, AXMAT_LOAD_WARM_NATIVE64
  public :: AXMAT_PUBLISH_REAL_TERMINAL64

  interface
    subroutine AXMAT_CONTINUOUS_DRIVER64(iprt,ipmacr,ipflux,ipsys,iptrk,ipflup,ipsou, &
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
    end subroutine AXMAT_CONTINUOUS_DRIVER64
  end interface

contains

  subroutine AXMAT_LOAD_WARM_NATIVE64(ipseed,nunknown,ngroup,initial_flux64,seed_keff64,status)
    ! ipseed is the recovered L_FLUX object, not the containing archive.
    ! Every native FLUX64 and SOUR64 item is read in full, with bit-exact
    ! demotion mirrors. Only FLUX64 provides the numerical initial guess.
    ! The independent external byte pin must establish which archive this
    ! came from and that its complete track/material/system match this run.
    type(c_ptr), intent(in) :: ipseed
    integer, intent(in) :: nunknown,ngroup
    real(real64), allocatable, intent(out) :: initial_flux64(:,:)
    real(real64), intent(out) :: seed_keff64
    integer, intent(out) :: status
    integer :: state(nstate),group,allocation_status
    real(real64), allocatable :: candidate(:,:),source64(:)
    real(real32), allocatable :: mirror(:)
    real(real64) :: keff64
    real(real32) :: keff32
    type(c_ptr) :: flux64,flux32,sour64,sour32
    character(len=12) :: signature
    logical :: pair_valid

    status=AXMAT_SEED64_REFUSED
    seed_keff64=0.0_real64
    if (.not.c_associated(ipseed)) return
    if (ngroup/=required_groups.or.nunknown/=required_unknowns) return
    if (.not.record_matches(ipseed,'SIGNATURE',3,3)) return
    call LCMGTC(ipseed,'SIGNATURE',12,signature)
    if (signature/='L_FLUX') return
    if (.not.record_matches(ipseed,'STATE-VECTOR',nstate,1)) return
    call LCMGET(ipseed,'STATE-VECTOR',state)
    if (state(1)/=ngroup.or.state(2)/=nunknown.or.state(3)/=1.or.state(6)/=2) return
    if (.not.record_matches(ipseed,'SPOT-KEFF64',1,4)) return
    if (.not.record_matches(ipseed,'K-EFFECTIVE',1,2)) return
    call LCMGET(ipseed,'SPOT-KEFF64',keff64)
    call LCMGET(ipseed,'K-EFFECTIVE',keff32)
    if (.not.ieee_is_finite(keff64).or.keff64<=0.0_real64) return
    if (.not.ieee_is_finite(keff32).or.keff32<=0.0_real32) return
    if (transfer(real(keff64,real32),0_int32)/=transfer(keff32,0_int32)) return
    if (.not.record_matches(ipseed,'FLUX64',ngroup,10)) return
    if (.not.record_matches(ipseed,'FLUX',ngroup,10)) return
    if (.not.record_matches(ipseed,'SOUR64',ngroup,10)) return
    if (.not.record_matches(ipseed,'SOUR',ngroup,10)) return
    flux64=LCMGID(ipseed,'FLUX64')
    flux32=LCMGID(ipseed,'FLUX')
    sour64=LCMGID(ipseed,'SOUR64')
    sour32=LCMGID(ipseed,'SOUR')
    allocate(candidate(nunknown,ngroup),source64(nunknown),mirror(nunknown),stat=allocation_status)
    if (allocation_status/=0) return
    do group=1,ngroup
      call read_exact_pair(flux64,flux32,group,candidate(:,group),mirror,pair_valid)
      if (.not.pair_valid) return
      call read_exact_pair(sour64,sour32,group,source64,mirror,pair_valid)
      if (.not.pair_valid) return
    enddo
    call move_alloc(candidate,initial_flux64)
    seed_keff64=keff64
    status=AXMAT_SEED64_LOADED
  end subroutine AXMAT_LOAD_WARM_NATIVE64

  subroutine AXMAT_PUBLISH_REAL_TERMINAL64(ipflux,iptrack,ipsystem,ipmaterial, &
      ipcontract,plane,epoch,terminal_flux64,terminal_source64,terminal_keff64, &
      terminal_resid64,terminal_counters,terminal_inner_state,terminal_valid,status)
    ! Called by the real owning caller only after the complete FLUDRV
    ! STATE-VECTOR/EPS-CONVERGE/KEYFLX/OPTION and FLU signature/links exist.
    ! These arrays must be direct outputs from AXMAT_CONTINUOUS_DRIVER64.
    ! A separate host admission pins the strict-run Source, inputs and output;
    ! no caller-supplied Boolean or internal copy can replace that proof.
    type(c_ptr), intent(in) :: ipflux,iptrack,ipsystem,ipmaterial,ipcontract
    integer, intent(in) :: plane,epoch,terminal_counters(2),terminal_inner_state
    real(real64), intent(in) :: terminal_flux64(:,:),terminal_source64(:,:)
    real(real64), intent(in) :: terminal_keff64,terminal_resid64(3)
    logical, intent(in) :: terminal_valid
    integer, intent(out) :: status
    type(c_ptr) :: sources,mirrors
    real(real64), allocatable :: saved64(:)
    real(real32), allocatable :: mirror32(:)
    real(real32) :: actual_mccg_control(4)
    type(SPOR64_ROUTE_CONTRACT) :: contract
    integer :: group,nunknown,allocation_status
    logical :: pair_valid,contract_loaded

    status=ROOT64_REFUSED
    if (.not.terminal_valid.or..not.c_associated(ipflux)) return
    if (size(terminal_flux64,2)/=required_groups) return
    nunknown=size(terminal_flux64,1)
    if (nunknown/=required_unknowns) return
    if (any(shape(terminal_source64)/=shape(terminal_flux64))) return
    if (.not.all(ieee_is_finite(terminal_flux64))) return
    if (.not.all(ieee_is_finite(terminal_source64))) return
    ! The retained real AXMAT_MCCG_DOOR64 uses this exact TRACK cutoff.
    ! A historical route contract with eps_mccg=1e-5 cannot silently label
    ! a solve actually performed with 2.5e-8 as that old whole-input case.
    call SPOR64_RCONTRACT_LOAD(ipcontract,contract,contract_loaded)
    if (.not.contract_loaded) return
    if (.not.record_matches(iptrack,'REAL-PARAM',4,2)) return
    call LCMGET(iptrack,'REAL-PARAM',actual_mccg_control)
    if (.not.all(ieee_is_finite(actual_mccg_control))) return
    if (actual_mccg_control(1)/=2.5e-8_real32) return
    if (any(actual_mccg_control(2:4)/=0.0_real32)) return
    if (transfer(actual_mccg_control(1),0_int32)/=contract%eps_mccg_bits) return
    if (.not.record_matches(ipflux,'SOUR64',required_groups,10)) return
    if (.not.record_matches(ipflux,'SOUR',required_groups,10)) return
    sources=LCMGID(ipflux,'SOUR64')
    mirrors=LCMGID(ipflux,'SOUR')
    allocate(saved64(nunknown),mirror32(nunknown),stat=allocation_status)
    if (allocation_status/=0) return
    do group=1,required_groups
      call read_exact_pair(sources,mirrors,group,saved64,mirror32,pair_valid)
      if (.not.pair_valid) return
      if (.not.same64(saved64,terminal_source64(:,group))) return
    enddo
    call SPOR64_BOOT64_PUBLISH_NATIVE(ipflux,iptrack,ipsystem,ipmaterial,ipcontract, &
      plane,epoch,terminal_flux64,terminal_keff64,terminal_resid64, &
      terminal_counters(1),terminal_counters(2),terminal_inner_state,status)
  end subroutine AXMAT_PUBLISH_REAL_TERMINAL64

  subroutine read_exact_pair(native,mirror,group,values,mirror_values,valid)
    type(c_ptr), intent(in) :: native,mirror
    integer, intent(in) :: group
    real(real64), intent(out) :: values(:)
    real(real32), intent(out) :: mirror_values(:)
    logical, intent(out) :: valid
    integer :: length,type_code,index
    valid=.false.
    if (.not.c_associated(native).or..not.c_associated(mirror)) return
    if (size(values)/=size(mirror_values)) return
    call LCMLEL(native,group,length,type_code)
    if (length/=size(values).or.type_code/=4) return
    call LCMLEL(mirror,group,length,type_code)
    if (length/=size(values).or.type_code/=2) return
    call LCMGDL(native,group,values)
    call LCMGDL(mirror,group,mirror_values)
    if (.not.all(ieee_is_finite(values)).or..not.all(ieee_is_finite(mirror_values))) return
    if (.not.all(ieee_is_finite(real(values,real32)))) return
    do index=1,size(values)
      if (transfer(real(values(index),real32),0_int32)/=transfer(mirror_values(index),0_int32)) return
    enddo
    valid=.true.
  end subroutine read_exact_pair

  logical function record_matches(object,name,length,type_code)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type
    record_matches=.false.
    if (.not.c_associated(object)) return
    call LCMLEN(object,name,actual_length,actual_type)
    record_matches=actual_length==length.and.actual_type==type_code
  end function record_matches

  logical function same64(left,right)
    real(real64), intent(in) :: left(:),right(:)
    same64=.false.
    if (size(left)/=size(right)) return
    same64=all(transfer(left,0_int64,size(left))==transfer(right,0_int64,size(right)))
  end function same64
end module AXMAT_NATIVE_PRODUCER_CHAIN

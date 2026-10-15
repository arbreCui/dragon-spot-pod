module SPOR64_BOOT_BIND64
  ! Full current PROJECTED-BOOT/e0 context and physical frozen-Q binding.
  ! Stored labels/tree consistency do not replace the owning host's actual
  ! complete external file SHA/7ID and actual tool terminal pins.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only:int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only:ieee_is_finite
  use SPOR64_BOOT_CONTEXT64_V2,only:SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOTQ64_V2,only:SPOR64_BOOTQ64_READ,SPOR64_BOOTQ64_LOADED
  use SPOR64_BOOT64,only:SPOR64_BOOT64_SAME_TREE
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY,only:ABSENT_RECORD,CHARACTER_RECORD_MATCHES, &
      EXACT_INVENTORY,LIST_ITEM_IS_DIRECTORY,RECORD_MATCHES,SAME_REAL32_BITS
  use SPOR64_SCHEMA,only:SCHEMA_RESPONSE_GROUP,SCHEMA_RESPONSE_GROUP_P3, &
      SCHEMA_RESPONSE_GROUP_PHYS,SCHEMA_RESPONSE_GROUP_PHYS_P3, &
      SCHEMA_CANDIDATE_SYSTEM_ROOT,SCHEMA_CANDIDATE_SYSTEM_ROOT_L1RAW
  implicit none
  private
  integer,parameter::NSTATE=40,NGRP=370,NSNAP=3
  public::SPOR64_BOOT_BIND64_READ
contains
  subroutine SPOR64_BOOT_BIND64_READ(ipprojected,ipglobal,ipax, &
      ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract,requested_rank, &
      plane_index,ipseed,iptrack,ipsystem,ipmacro,ipsource, &
      initial_flux64,fixed_source64,leak1d64,ok)
    type(c_ptr),intent(in)::ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem
    type(c_ptr),intent(in)::ipaxmacro,iparchive,ipcontract
    type(c_ptr),intent(in)::ipseed,iptrack,ipsystem,ipmacro,ipsource
    integer,intent(in)::requested_rank,plane_index
    real(real64),intent(out)::initial_flux64(:,:),fixed_source64(:,:),leak1d64(:)
    logical,intent(out)::ok
    type(SPOR64_ROUTE_CONTRACT)::contract
    type(c_ptr)::tracks,fluxes,expected_seed,expected_track,roots,native,groups
    integer::rank(NGRP),state(NSTATE),mccg(NSTATE),pflag,g,n,t,nreg,nunk,nmat
    integer::status
    real(real64)::rho
    real(real64),allocatable::q64(:,:),phi(:)
    real(real32)::leak32(NGRP)
    logical::valid
    ok=.false.;initial_flux64=0.0_real64;fixed_source64=0.0_real64;leak1d64=0.0_real64
    if(requested_rank<=0.or.plane_index<1.or.plane_index>NSNAP)return
    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,contract,valid)
    if(.not.valid)return
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-RANK',NGRP,1))return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    if(any(rank/=requested_rank))return
    tracks=LCMGID(ipprojected,'TRACK');fluxes=LCMGID(ipprojected,'FLUX')
    expected_track=LCMGIL(tracks,plane_index);expected_seed=LCMGIL(fluxes,plane_index)
    if(.not.SPOR64_BOOT64_SAME_TREE(iptrack,expected_track))return
    if(.not.SPOR64_BOOT64_SAME_TREE(ipseed,expected_seed))return
    call LCMGET(iptrack,'STATE-VECTOR',state)
    nreg=state(1);nunk=state(2);nmat=state(4)
    if(nreg<=0.or.nunk<=nreg.or.nmat<=0)return
    if(any(shape(initial_flux64)/=[nunk,NGRP]))return
    if(any(shape(fixed_source64)/=[nunk,NGRP]).or.size(leak1d64)/=NGRP)return
    call SPOR64_BOOTQ64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
        ipmacro,ipsource,q64,rho,status)
    if(status/=SPOR64_BOOTQ64_LOADED)return
    if(.not.allocated(q64))return
    if(any(shape(q64)/=[nunk,NGRP]))return
    if(any(.not.ieee_is_finite(q64)).or.any(q64<0.0_real64))return
    fixed_source64=q64
    if(.not.RECORD_MATCHES(ipseed,'ROOT-FLUX64',NGRP,10))return
    roots=LCMGID(ipseed,'ROOT-FLUX64')
    native=LCMGID(LCMGID(ipseed,'SPOT-R64'),'FLUX')
    allocate(phi(nunk))
    do g=1,NGRP
      call LCMLEL(roots,g,n,t)
      if(n/=nunk.or.t/=4)return
      call LCMGDL(roots,g,initial_flux64(:,g))
      call LCMLEL(native,g,n,t)
      if(n/=nunk.or.t/=4)return
      call LCMGDL(native,g,phi)
      if(any(.not.ieee_is_finite(initial_flux64(:,g))))return
      if(any(transfer(phi,[0_int64],nunk)/= &
          transfer(initial_flux64(:,g),[0_int64],nunk)))return
    enddo
    if(.not.RECORD_MATCHES(ipseed,'LEAK1D64',NGRP,4))return
    call LCMGET(ipseed,'LEAK1D64',leak1d64)
    if(any(.not.ieee_is_finite(leak1d64)))return
    call LCMGET(ipseed,'SPOT-LEAK1D',leak32)
    if(any(transfer(leak32,[0_int32],NGRP)/= &
        transfer(real(leak1d64,real32),[0_int32],NGRP)))return
    ! Real fresh ASM result only; no forged ASSEMBLED/e0 lifecycle wrapper.
    if(.not.CANDIDATE_SYSTEM_ROOT_IS_EXACT(ipsystem))return
    if(.not.RECORD_MATCHES(ipsystem,'SPOT-L1-RAW',1,1))return
    call LCMGET(ipsystem,'SPOT-L1-RAW',pflag)
    if(pflag/=1)return
    if(.not.ABSENT_RECORD(ipsystem,'SPOT-R64'))return
    if(.not.ABSENT_RECORD(ipsystem,'B2I-SENT').or. &
        .not.ABSENT_RECORD(ipsystem,'B2I-DEEP'))return
    if(.not.RECORD_MATCHES(iptrack,'MCCG-STATE',NSTATE,1))return
    call LCMGET(iptrack,'MCCG-STATE',mccg)
    if(.not.SYSTEM_PAYLOAD_IS_VALID(ipsystem,ipmacro,leak32,plane_index, &
        .true.,nreg,nmat,nunk,state(5),mccg(6),mccg(10),mccg(17)))return
    ok=.true.
  end subroutine SPOR64_BOOT_BIND64_READ
  logical function SYSTEM_PAYLOAD_IS_VALID(ipsystem,ipmacro,leakage, &
      plane,unreduced,nreg,nmat,nunkno,nsurf,lc,paca,lc0)
    type(c_ptr), intent(in) :: ipsystem, ipmacro
    real(real32), intent(in) :: leakage(NGRP)
    integer, intent(in) :: plane, nreg, nmat, nunkno, nsurf, lc
    integer, intent(in) :: paca, lc0
    logical, intent(in) :: unreduced

    integer :: state(NSTATE), expected_state(NSTATE)
    integer :: snapshot, ig, im, ilong, itylcm, allocation_status
    real(real32), allocatable :: ntot32(:), sigw32(:), tranc32(:)
    real(real32) :: candidate_leakage32(NGRP)
    real(real32), allocatable :: tx32(:), sphys32(:), sused32(:)
    real(real32), allocatable :: expected_tx32(:)
    real(real32), allocatable :: expected_sphys32(:)
    real(real32), allocatable :: expected_sused32(:)
    type(c_ptr) :: macro_groups, system_groups, macro_group, system_group

    SYSTEM_PAYLOAD_IS_VALID = .false.
    if (nreg <= 0 .or. nmat <= 0 .or. nunkno <= 0 .or. &
        nsurf <= 0 .or. lc <= 0) return
    if (paca /= 3 .and. paca /= 4) return
    if ((paca == 3 .and. lc0 <= 0) .or. &
        (paca == 4 .and. lc0 /= 0)) return
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) return
    if (.not. c_associated(ipsystem)) return
    if (.not. c_associated(ipmacro)) return
    if (plane < 1 .or. plane > NSNAP) return
    if (.not. all(ieee_is_finite(leakage))) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'SIGNATURE',3,12, &
        'L_PIJ')) return
    if (.not. RECORD_MATCHES(ipsystem,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipsystem,'STATE-VECTOR',state)
    expected_state = &
        [1,1,1,0,1,1,4,NGRP,nunkno,nmat,1,0,0,0, &
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if (any(state /= expected_state)) return
    allocate(ntot32(nmat),sigw32(nmat),tranc32(nmat), &
        tx32(0:nmat),sphys32(0:nmat),sused32(0:nmat), &
        expected_tx32(0:nmat),expected_sphys32(0:nmat), &
        expected_sused32(0:nmat),stat=allocation_status)
    if (allocation_status /= 0) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-L1-SNAP',1,1)) return
    call LCMGET(ipsystem,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= plane) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(ipsystem,'SPOT-LEAK1D',candidate_leakage32)
    if (.not. all(ieee_is_finite(candidate_leakage32))) return
    if (.not. SAME_REAL32_BITS(candidate_leakage32,leakage)) return
    if (.not. RECORD_MATCHES(ipsystem,'GROUP',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipmacro,'GROUP',NGRP,10)) return
    system_groups = LCMGID(ipsystem,'GROUP')
    macro_groups = LCMGID(ipmacro,'GROUP')
    if (.not. c_associated(system_groups)) return
    if (.not. c_associated(macro_groups)) return

    do ig = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(system_groups,ig)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(macro_groups,ig)) return
      system_group = LCMGIL(system_groups,ig)
      macro_group = LCMGIL(macro_groups,ig)
      if (.not. c_associated(system_group)) return
      if (.not. c_associated(macro_group)) return
      if (.not. RESPONSE_GROUP_IS_EXACT(system_group,nreg,nmat, &
          nunkno,nsurf,lc,paca,lc0)) return
      if (.not. RECORD_MATCHES(macro_group,'NTOT0',nmat,2)) return
      if (.not. RECORD_MATCHES(macro_group,'SIGW00',nmat,2)) return
      call LCMGET(macro_group,'NTOT0',ntot32)
      call LCMGET(macro_group,'SIGW00',sigw32)
      if (.not. all(ieee_is_finite(ntot32))) return
      if (.not. all(ieee_is_finite(sigw32))) return
      call LCMLEN(macro_group,'TRANC',ilong,itylcm)
      if (ilong /= nmat .or. itylcm /= 2) return
      call LCMGET(macro_group,'TRANC',tranc32)
      if (.not. all(ieee_is_finite(tranc32))) return

      call LCMGET(system_group,'DRAGON-TXSC',tx32)
      call LCMGET(system_group,'SPOT-S0-PHYS',sphys32)
      call LCMGET(system_group,'DRAGON-S0XSC',sused32)
      expected_tx32 = +0.0_real32
      expected_sphys32 = +0.0_real32
      expected_sused32 = +0.0_real32
      if (unreduced) then
        ! REAL64 leakage mode: the stored self-scattering is the
        ! physical one; the reduction is applied in the solver core.
        expected_sused32(0) = expected_sphys32(0)
      else
        expected_sused32(0) = expected_sphys32(0)-leakage(ig)
      end if
      do im = 1, nmat
        expected_tx32(im) = ntot32(im)
        expected_sphys32(im) = sigw32(im)
        expected_tx32(im) = expected_tx32(im)-tranc32(im)
        expected_sphys32(im) = expected_sphys32(im)-tranc32(im)
        if (unreduced) then
          expected_sused32(im) = expected_sphys32(im)
        else
          expected_sused32(im) = expected_sphys32(im)-leakage(ig)
        end if
      end do
      if (.not. all(ieee_is_finite(expected_tx32))) return
      if (.not. all(ieee_is_finite(expected_sphys32))) return
      if (.not. all(ieee_is_finite(expected_sused32))) return
      if (.not. SAME_REAL32_BITS(tx32,expected_tx32)) return
      if (.not. SAME_REAL32_BITS(sphys32,expected_sphys32)) return
      if (.not. SAME_REAL32_BITS(sused32,expected_sused32)) return
    end do
    SYSTEM_PAYLOAD_IS_VALID = .true.
  end function SYSTEM_PAYLOAD_IS_VALID


  logical function RESPONSE_GROUP_IS_EXACT(group,nreg,nmat,nunkno, &
      nsurf,lc,paca,lc0)
    type(c_ptr), intent(in) :: group
    integer, intent(in) :: nreg, nmat, nunkno, nsurf, lc, paca, lc0

    integer :: response_lengths(size(SCHEMA_RESPONSE_GROUP)), i

    RESPONSE_GROUP_IS_EXACT = .false.
    if (nreg <= 0 .or. nmat <= 0 .or. nunkno <= 0 .or. &
        nsurf <= 0 .or. lc <= 0) return
    if (paca /= 3 .and. paca /= 4) return
    if ((paca == 3 .and. lc0 <= 0) .or. &
        (paca == 4 .and. lc0 /= 0)) return
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) return
    response_lengths = &
        [lc,nunkno,lc,nunkno,nreg,nreg,nreg,nreg,nreg,nreg,nreg, &
         nunkno]
    if (paca == 3) then
      if (.not. EXACT_INVENTORY(group, &
          SCHEMA_RESPONSE_GROUP_PHYS_P3)) return
    else
      if (.not. EXACT_INVENTORY(group,SCHEMA_RESPONSE_GROUP_PHYS)) return
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)
      if (.not. FINITE_REAL32_RECORD(group,SCHEMA_RESPONSE_GROUP(i), &
          response_lengths(i))) return
    end do
    if (paca == 3) then
      if (.not. FINITE_REAL32_RECORD(group, &
          SCHEMA_RESPONSE_GROUP_P3(size(SCHEMA_RESPONSE_GROUP_P3)), &
          lc0)) return
    end if
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-TXSC',nmat+1)) return
    if (.not. FINITE_REAL32_RECORD(group,'SPOT-S0-PHYS',nmat+1)) return
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-S0XSC',nmat+1)) return
    if (.not. ABSENT_RECORD(group,'FUNKNO$USS')) return
    RESPONSE_GROUP_IS_EXACT = .true.
  end function RESPONSE_GROUP_IS_EXACT


  logical function FINITE_REAL32_RECORD(root,name,expected_length)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length
    real(real32), allocatable :: values(:)
    integer :: allocation_status

    FINITE_REAL32_RECORD = .false.
    if (.not. RECORD_MATCHES(root,name,expected_length,2)) return
    allocate(values(expected_length),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(root,name,values)
    FINITE_REAL32_RECORD = all(ieee_is_finite(values))
  end function FINITE_REAL32_RECORD


  logical function CANDIDATE_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CANDIDATE_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_CANDIDATE_SYSTEM_ROOT_L1RAW) &
        .or. EXACT_INVENTORY(iplist,SCHEMA_CANDIDATE_SYSTEM_ROOT)
  end function CANDIDATE_SYSTEM_ROOT_IS_EXACT
end module SPOR64_BOOT_BIND64

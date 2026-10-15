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
    if(requested_rank<=0.or.plane_index<1.or.plane_index>NSNAP)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0041",'// &
        '"original_return_source_line":41,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,contract,valid)
    if(.not.valid)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0044",'// &
        '"original_return_source_line":44,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-RANK',NGRP,1))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0045",'// &
        '"original_return_source_line":45,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    if(any(rank/=requested_rank))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0047",'// &
        '"original_return_source_line":47,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    tracks=LCMGID(ipprojected,'TRACK');fluxes=LCMGID(ipprojected,'FLUX')
    expected_track=LCMGIL(tracks,plane_index);expected_seed=LCMGIL(fluxes,plane_index)
    if(.not.SPOR64_BOOT64_SAME_TREE(iptrack,expected_track))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0050",'// &
        '"original_return_source_line":50,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.SPOR64_BOOT64_SAME_TREE(ipseed,expected_seed))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0051",'// &
        '"original_return_source_line":51,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(iptrack,'STATE-VECTOR',state)
    nreg=state(1);nunk=state(2);nmat=state(4)
    if(nreg<=0.or.nunk<=nreg.or.nmat<=0)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0054",'// &
        '"original_return_source_line":54,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(any(shape(initial_flux64)/=[nunk,NGRP]))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0055",'// &
        '"original_return_source_line":55,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(any(shape(fixed_source64)/=[nunk,NGRP]).or.size(leak1d64)/=NGRP)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0056",'// &
        '"original_return_source_line":56,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call SPOR64_BOOTQ64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
        ipmacro,ipsource,q64,rho,status)
    if(status/=SPOR64_BOOTQ64_LOADED)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0060",'// &
        '"original_return_source_line":60,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.allocated(q64))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0061",'// &
        '"original_return_source_line":61,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(any(shape(q64)/=[nunk,NGRP]))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0062",'// &
        '"original_return_source_line":62,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(any(.not.ieee_is_finite(q64)).or.any(q64<0.0_real64))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0063",'// &
        '"original_return_source_line":63,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    fixed_source64=q64
    if(.not.RECORD_MATCHES(ipseed,'ROOT-FLUX64',NGRP,10))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0065",'// &
        '"original_return_source_line":65,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    roots=LCMGID(ipseed,'ROOT-FLUX64')
    native=LCMGID(LCMGID(ipseed,'SPOT-R64'),'FLUX')
    allocate(phi(nunk))
    do g=1,NGRP
      call LCMLEL(roots,g,n,t)
      if(n/=nunk.or.t/=4)then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SPOR64_BOOT_BIND64_READ",'// &
          '"predicate_id":"BIND64_READ_RETURN_L0071",'// &
          '"original_return_source_line":71,"actual_boolean_status_integer":', &
          merge(1,0,ok),'}'
        flush(6)
        return
      endif
      call LCMGDL(roots,g,initial_flux64(:,g))
      call LCMLEL(native,g,n,t)
      if(n/=nunk.or.t/=4)then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SPOR64_BOOT_BIND64_READ",'// &
          '"predicate_id":"BIND64_READ_RETURN_L0074",'// &
          '"original_return_source_line":74,"actual_boolean_status_integer":', &
          merge(1,0,ok),'}'
        flush(6)
        return
      endif
      call LCMGDL(native,g,phi)
      if(any(.not.ieee_is_finite(initial_flux64(:,g))))then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SPOR64_BOOT_BIND64_READ",'// &
          '"predicate_id":"BIND64_READ_RETURN_L0076",'// &
          '"original_return_source_line":76,"actual_boolean_status_integer":', &
          merge(1,0,ok),'}'
        flush(6)
        return
      endif
      if(any(transfer(phi,[0_int64],nunk)/= &
          transfer(initial_flux64(:,g),[0_int64],nunk)))then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SPOR64_BOOT_BIND64_READ",'// &
          '"predicate_id":"BIND64_READ_RETURN_L0078",'// &
          '"original_return_source_line":78,"actual_boolean_status_integer":', &
          merge(1,0,ok),'}'
        flush(6)
        return
      endif
    enddo
    if(.not.RECORD_MATCHES(ipseed,'LEAK1D64',NGRP,4))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0080",'// &
        '"original_return_source_line":80,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'LEAK1D64',leak1d64)
    if(any(.not.ieee_is_finite(leak1d64)))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0082",'// &
        '"original_return_source_line":82,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'SPOT-LEAK1D',leak32)
    if(any(transfer(leak32,[0_int32],NGRP)/= &
        transfer(real(leak1d64,real32),[0_int32],NGRP)))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0085",'// &
        '"original_return_source_line":85,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    ! Real fresh ASM result only; no forged ASSEMBLED/e0 lifecycle wrapper.
    if(.not.CANDIDATE_SYSTEM_ROOT_IS_EXACT(ipsystem))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0087",'// &
        '"original_return_source_line":87,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.RECORD_MATCHES(ipsystem,'SPOT-L1-RAW',1,1))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0088",'// &
        '"original_return_source_line":88,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(ipsystem,'SPOT-L1-RAW',pflag)
    if(pflag/=1)then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0090",'// &
        '"original_return_source_line":90,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.ABSENT_RECORD(ipsystem,'SPOT-R64'))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0091",'// &
        '"original_return_source_line":91,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.ABSENT_RECORD(ipsystem,'B2I-SENT').or. &
        .not.ABSENT_RECORD(ipsystem,'B2I-DEEP'))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0093",'// &
        '"original_return_source_line":93,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    if(.not.RECORD_MATCHES(iptrack,'MCCG-STATE',NSTATE,1))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0094",'// &
        '"original_return_source_line":94,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
    call LCMGET(iptrack,'MCCG-STATE',mccg)
    if(.not.SYSTEM_PAYLOAD_IS_VALID(ipsystem,ipmacro,leak32,plane_index, &
        .true.,nreg,nmat,nunk,state(5),mccg(6),mccg(10),mccg(17)))then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SPOR64_BOOT_BIND64_READ",'// &
        '"predicate_id":"BIND64_READ_RETURN_L0097",'// &
        '"original_return_source_line":97,"actual_boolean_status_integer":', &
        merge(1,0,ok),'}'
      flush(6)
      return
    endif
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
        nsurf <= 0 .or. lc <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0120",'// &
        '"original_return_source_line":120,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (paca /= 3 .and. paca /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0121",'// &
        '"original_return_source_line":121,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if ((paca == 3 .and. lc0 <= 0) .or. &
        (paca == 4 .and. lc0 /= 0)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0123",'// &
        '"original_return_source_line":123,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0124",'// &
        '"original_return_source_line":124,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. c_associated(ipsystem)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0125",'// &
        '"original_return_source_line":125,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. c_associated(ipmacro)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0126",'// &
        '"original_return_source_line":126,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (plane < 1 .or. plane > NSNAP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0127",'// &
        '"original_return_source_line":127,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. all(ieee_is_finite(leakage))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0128",'// &
        '"original_return_source_line":128,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'SIGNATURE',3,12, &
        'L_PIJ')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0130",'// &
        '"original_return_source_line":130,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsystem,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0131",'// &
        '"original_return_source_line":131,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    call LCMGET(ipsystem,'STATE-VECTOR',state)
    expected_state = &
        [1,1,1,0,1,1,4,NGRP,nunkno,nmat,1,0,0,0, &
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if (any(state /= expected_state)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0136",'// &
        '"original_return_source_line":136,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    allocate(ntot32(nmat),sigw32(nmat),tranc32(nmat), &
        tx32(0:nmat),sphys32(0:nmat),sused32(0:nmat), &
        expected_tx32(0:nmat),expected_sphys32(0:nmat), &
        expected_sused32(0:nmat),stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0141",'// &
        '"original_return_source_line":141,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.MACRO',3,12, &
        'MACRO0')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0143",'// &
        '"original_return_source_line":143,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.TRACK',3,12, &
        'TRACK')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0145",'// &
        '"original_return_source_line":145,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-L1-SNAP',1,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0146",'// &
        '"original_return_source_line":146,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    call LCMGET(ipsystem,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= plane) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0148",'// &
        '"original_return_source_line":148,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-LEAK1D',NGRP,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0149",'// &
        '"original_return_source_line":149,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    call LCMGET(ipsystem,'SPOT-LEAK1D',candidate_leakage32)
    if (.not. all(ieee_is_finite(candidate_leakage32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0151",'// &
        '"original_return_source_line":151,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. SAME_REAL32_BITS(candidate_leakage32,leakage)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0152",'// &
        '"original_return_source_line":152,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsystem,'GROUP',NGRP,10)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0153",'// &
        '"original_return_source_line":153,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipmacro,'GROUP',NGRP,10)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0154",'// &
        '"original_return_source_line":154,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    system_groups = LCMGID(ipsystem,'GROUP')
    macro_groups = LCMGID(ipmacro,'GROUP')
    if (.not. c_associated(system_groups)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0157",'// &
        '"original_return_source_line":157,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif
    if (.not. c_associated(macro_groups)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
        '"predicate_id":"BIND64_SYSTEM_RETURN_L0158",'// &
        '"original_return_source_line":158,"actual_boolean_status_integer":', &
        merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
      flush(6)
      return
    endif

    do ig = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(system_groups,ig)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0161",'// &
          '"original_return_source_line":161,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. LIST_ITEM_IS_DIRECTORY(macro_groups,ig)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0162",'// &
          '"original_return_source_line":162,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      system_group = LCMGIL(system_groups,ig)
      macro_group = LCMGIL(macro_groups,ig)
      if (.not. c_associated(system_group)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0165",'// &
          '"original_return_source_line":165,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. c_associated(macro_group)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0166",'// &
          '"original_return_source_line":166,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. RESPONSE_GROUP_IS_EXACT(system_group,nreg,nmat, &
          nunkno,nsurf,lc,paca,lc0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0168",'// &
          '"original_return_source_line":168,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        write(6,'(A,I0,A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
          '"event":"caller","original_return_source_line":168,"group_index":', &
          ig,',"plane_index":',plane,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(macro_group,'NTOT0',nmat,2)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0169",'// &
          '"original_return_source_line":169,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(macro_group,'SIGW00',nmat,2)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0170",'// &
          '"original_return_source_line":170,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      call LCMGET(macro_group,'NTOT0',ntot32)
      call LCMGET(macro_group,'SIGW00',sigw32)
      if (.not. all(ieee_is_finite(ntot32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0173",'// &
          '"original_return_source_line":173,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. all(ieee_is_finite(sigw32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0174",'// &
          '"original_return_source_line":174,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      call LCMLEN(macro_group,'TRANC',ilong,itylcm)
      if (ilong /= nmat .or. itylcm /= 2) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0176",'// &
          '"original_return_source_line":176,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      call LCMGET(macro_group,'TRANC',tranc32)
      if (.not. all(ieee_is_finite(tranc32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0178",'// &
          '"original_return_source_line":178,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif

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
      if (.not. all(ieee_is_finite(expected_tx32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0204",'// &
          '"original_return_source_line":204,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. all(ieee_is_finite(expected_sphys32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0205",'// &
          '"original_return_source_line":205,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. all(ieee_is_finite(expected_sused32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0206",'// &
          '"original_return_source_line":206,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. SAME_REAL32_BITS(tx32,expected_tx32)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0207",'// &
          '"original_return_source_line":207,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. SAME_REAL32_BITS(sphys32,expected_sphys32)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0208",'// &
          '"original_return_source_line":208,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
      if (.not. SAME_REAL32_BITS(sused32,expected_sused32)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SYSTEM_PAYLOAD_IS_VALID",'// &
          '"predicate_id":"BIND64_SYSTEM_RETURN_L0209",'// &
          '"original_return_source_line":209,"actual_boolean_status_integer":', &
          merge(1,0,SYSTEM_PAYLOAD_IS_VALID),'}'
        flush(6)
        return
      endif
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
        nsurf <= 0 .or. lc <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0224",'// &
        '"original_return_source_line":224,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if (paca /= 3 .and. paca /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0225",'// &
        '"original_return_source_line":225,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if ((paca == 3 .and. lc0 <= 0) .or. &
        (paca == 4 .and. lc0 /= 0)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0227",'// &
        '"original_return_source_line":227,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0228",'// &
        '"original_return_source_line":228,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    response_lengths = &
        [lc,nunkno,lc,nunkno,nreg,nreg,nreg,nreg,nreg,nreg,nreg, &
         nunkno]
    if (paca == 3) then
      if (.not. EXACT_INVENTORY(group, &
          SCHEMA_RESPONSE_GROUP_PHYS_P3)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
          '"predicate_id":"BIND64_RESPONSE_RETURN_L0234",'// &
          '"original_return_source_line":234,"actual_boolean_status_integer":', &
          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        return
      endif
    else
      if (.not. EXACT_INVENTORY(group,SCHEMA_RESPONSE_GROUP_PHYS)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
          '"predicate_id":"BIND64_RESPONSE_RETURN_L0236",'// &
          '"original_return_source_line":236,"actual_boolean_status_integer":', &
          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        block
          character(len=72) :: diag_file
          character(len=12) :: diag_object,diag_name,diag_first
          character(len=24) :: diag_name_hex
          integer :: diag_length,diag_type,diag_count,diag_j,diag_object_length
          logical :: diag_empty,diag_lcm,diag_associated,diag_complete,diag_truncated
          diag_file=' ';diag_object=' ';diag_name=' ';diag_first=' '
          diag_object_length=0;diag_empty=.false.;diag_lcm=.false.
          diag_count=0;diag_complete=.false.;diag_truncated=.false.
          diag_associated=c_associated(group)
          if(diag_associated)then
            call LCMINF(group,diag_file,diag_object,diag_empty,diag_object_length,diag_lcm)
          endif
          write(6,'(A,I0,A,I0,A,I0,A,I0,A)') &
            '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
            '"event":"begin","original_return_source_line":236,"maximum_records":64,'// &
            '"expected_schema":"SCHEMA_RESPONSE_GROUP_PHYS","expected_count":15,'// &
            '"associated_integer":',merge(1,0,diag_associated), &
            ',"empty_integer":',merge(1,0,diag_empty), &
            ',"object_length":',diag_object_length, &
            ',"memory_integer":',merge(1,0,diag_lcm),'}'
          if(diag_associated.and.diag_object_length==-1)then
            if(diag_empty)then
              diag_complete=.true.
            else
              call LCMNXT(group,diag_name)
              if(diag_name/=' ')then
                diag_first=diag_name
                do
                  diag_count=diag_count+1
                  call LCMLEN(group,diag_name,diag_length,diag_type)
                  do diag_j=1,12
                    write(diag_name_hex(2*diag_j-1:2*diag_j),'(Z2.2)') &
                      iachar(diag_name(diag_j:diag_j))
                  enddo
                  write(6,'(A,I0,A,A,A,I0,A,I0,A)') &
                    '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
                    '"event":"record","ordinal":',diag_count, &
                    ',"name_bytes_hex":"',diag_name_hex,'","length":',diag_length, &
                    ',"type":',diag_type,'}'
                  call LCMNXT(group,diag_name)
                  if(diag_name==diag_first)then
                    diag_complete=.true.
                    exit
                  endif
                  if(diag_count==64)then
                    diag_truncated=.true.
                    exit
                  endif
                  if(diag_name==' ')exit
                enddo
              endif
            endif
          endif
          write(6,'(A,I0,A,I0,A,I0,A)') &
            '{"schema":"ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1",'// &
            '"event":"end","original_return_source_line":236,"record_count":',diag_count, &
            ',"complete_integer":',merge(1,0,diag_complete), &
            ',"truncated_integer":',merge(1,0,diag_truncated),'}'
          flush(6)
        end block
        return
      endif
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)
      if (.not. FINITE_REAL32_RECORD(group,SCHEMA_RESPONSE_GROUP(i), &
          response_lengths(i))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
          '"predicate_id":"BIND64_RESPONSE_RETURN_L0240",'// &
          '"original_return_source_line":240,"actual_boolean_status_integer":', &
          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        return
      endif
    end do
    if (paca == 3) then
      if (.not. FINITE_REAL32_RECORD(group, &
          SCHEMA_RESPONSE_GROUP_P3(size(SCHEMA_RESPONSE_GROUP_P3)), &
          lc0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
          '"predicate_id":"BIND64_RESPONSE_RETURN_L0245",'// &
          '"original_return_source_line":245,"actual_boolean_status_integer":', &
          merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
        flush(6)
        return
      endif
    end if
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-TXSC',nmat+1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0247",'// &
        '"original_return_source_line":247,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if (.not. FINITE_REAL32_RECORD(group,'SPOT-S0-PHYS',nmat+1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0248",'// &
        '"original_return_source_line":248,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-S0XSC',nmat+1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0249",'// &
        '"original_return_source_line":249,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    if (.not. ABSENT_RECORD(group,'FUNKNO$USS')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"RESPONSE_GROUP_IS_EXACT",'// &
        '"predicate_id":"BIND64_RESPONSE_RETURN_L0250",'// &
        '"original_return_source_line":250,"actual_boolean_status_integer":', &
        merge(1,0,RESPONSE_GROUP_IS_EXACT),'}'
      flush(6)
      return
    endif
    RESPONSE_GROUP_IS_EXACT = .true.
  end function RESPONSE_GROUP_IS_EXACT


  logical function FINITE_REAL32_RECORD(root,name,expected_length)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length
    real(real32), allocatable :: values(:)
    integer :: allocation_status

    FINITE_REAL32_RECORD = .false.
    if (.not. RECORD_MATCHES(root,name,expected_length,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FINITE_REAL32_RECORD",'// &
        '"predicate_id":"BIND64_FINITE_RETURN_L0263",'// &
        '"original_return_source_line":263,"actual_boolean_status_integer":', &
        merge(1,0,FINITE_REAL32_RECORD),'}'
      flush(6)
      return
    endif
    allocate(values(expected_length),stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FINITE_REAL32_RECORD",'// &
        '"predicate_id":"BIND64_FINITE_RETURN_L0265",'// &
        '"original_return_source_line":265,"actual_boolean_status_integer":', &
        merge(1,0,FINITE_REAL32_RECORD),'}'
      flush(6)
      return
    endif
    call LCMGET(root,name,values)
    FINITE_REAL32_RECORD = all(ieee_is_finite(values))
  end function FINITE_REAL32_RECORD


  logical function CANDIDATE_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CANDIDATE_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_CANDIDATE_SYSTEM_ROOT_L1RAW) &
        .or. EXACT_INVENTORY(iplist,SCHEMA_CANDIDATE_SYSTEM_ROOT)
  end function CANDIDATE_SYSTEM_ROOT_IS_EXACT
end module SPOR64_BOOT_BIND64

module SPOR64_BOOT_CONTEXT64_V2
  ! NEW bootstrap ABI; no old PROJECTED/e>0 or ROOT64 producer seal is relaxed.
  ! Full trees bind supplied independent contexts. Coherent rewrites still need
  ! independent host full-file SHA/7ID rejection and a genuine producer call.
  use, intrinsic :: iso_c_binding, only : c_ptr,c_associated
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : RECORD_MATCHES,CHARACTER_RECORD_MATCHES, &
      EXACT_INVENTORY,LIST_ITEM_IS_DIRECTORY
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  use SPOR64_BOOT64, only : SPOR64_BOOT64_SAME_TREE
  use SPOR64_BOOT_CANONICAL64_V2, only : SPOR64_BOOT_CANONICAL64_CHECK
  implicit none
  private
  integer, parameter :: NGRP=370,EXPECTED_NPLANE=3,NSTATE=40
  integer, parameter :: kind_guard=1/merge(1,0, &
      kind(1)==int32.and.kind(1.0)==real32.and.dp==real64)
  character(len=12), parameter, public :: BOOT_GLOBAL_NAMES(21) = &
      ['SIGNATURE   ','VERSION     ','NPLANE      ','EPOCH       ', &
       'ROLE        ','STATE       ','CASE        ','KEFF64      ', &
       'RHO64       ','NORM64      ','RESIDUALS   ','COUNTERS    ', &
       'INNER-STATE ','CAPS        ','TERM-EPS    ','AX          ', &
       'AXTRACK     ','AXSYSTEM    ','AXMACRO     ','ARCHIVE     ', &
       'RCON        ']
  character(len=12), parameter, public :: BOOT_ARCHIVE_NAMES(8) = &
      ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
       'MICROLIB2   ','FLUX        ','SPOT-R64    ','GLOBAL64    ']
  character(len=12), parameter :: BOOT_ROOT_AUTH_NAMES(4) = &
      ['RHO         ','NPLANE      ','STATE       ','EPOCH       ']
  character(len=12), parameter, public :: BOOT_PLANE_NAMES(16) = &
      ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
       'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
       'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ', &
       'LEAK1D64    ','ROOT-FLUX64 ','VOLUME64    ','WEIGHT64    ']
  character(len=12), parameter, public :: BOOT_PLANE_AUTH_NAMES(5) = &
      ['RHO         ','FLUX        ','STATE       ','EPOCH       ', &
       'PLANE       ']
  character(len=12), parameter, public :: BOOT_SOURCE_NAMES(8) = &
      ['SIGNATURE   ','STATE-VECTOR','SPOT-FROZEN ','SPOT-KEFF   ', &
       'SPOT-QINT   ','DSOUR       ','SPOT-R64    ','ROOT-QFISS64']
  character(len=12), parameter, public :: BOOT_SOURCE_AUTH_NAMES(8) = &
      ['RHO         ','PLANE       ','STATE       ','QFISS       ', &
       'EPOCH       ','NORM        ','GLOBAL64    ','SEED        ']
  public :: SPOR64_BOOT_CONTEXT64_READ,SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK
contains
  subroutine SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(ipglobal,ipax, &
      ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract,contract,ok)
    type(c_ptr), intent(in) :: ipglobal,ipax,ipaxtrack
    type(c_ptr), intent(in) :: ipaxsystem,ipaxmacro,iparchive,ipcontract
    type(SPOR64_ROUTE_CONTRACT), intent(out) :: contract
    logical, intent(out) :: ok
    type(c_ptr) :: expected(6),child,root_auth,tracks,libraries,fluxes
    type(c_ptr) :: archive_tracks,archive_libraries,archive_fluxes
    type(c_ptr) :: plane,plane_track,seed,auth,native,roots,mirrors,old_native
    type(c_ptr) :: ax_source,ax_source32
    character(len=12), parameter :: names(6) = &
        ['AX          ','AXTRACK     ','AXSYSTEM    ','AXMACRO     ', &
         'ARCHIVE     ','RCON        ']
    integer :: i,j,g,p,nreg,nunk,nmode,ncoef,istat,nsnap
    integer :: version,epoch,nplane,inner_state,plane_number,archive_nplane
    integer :: ax_state(NSTATE),ax_track_state(NSTATE),track_state(NSTATE)
    integer :: caps(2),counter(2),dims(4),state(NSTATE),old_state(NSTATE)
    integer, allocatable :: rank(:),offset(:),boff(:),key(:),imerge(:),keycur(:),keyanis(:)
    logical, allocatable :: seen(:)
    integer :: length,type_code,index_a,index_b
    real(real32) :: eps32(5)
    real(real32), allocatable :: basis(:),mirror(:),vol32(:),leak32(:)
    real(real64) :: keff,rho,norm,value,source_value,volume_sum
    real(real64) :: residual(3),limits(3),leak(3*NGRP),actual_rho
    real(real64), allocatable :: coordinates(:),values(:),reference(:)
    real(real64), allocatable :: old_values(:),volume(:),weight(:),saved(:)
    logical :: valid

    ok=.false.
    expected=[ipax,ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract]
    if (.not.c_associated(ipglobal)) return
    do i=1,size(expected)
      if (.not.c_associated(expected(i))) return
      if (c_associated(ipglobal,expected(i))) return
      do j=1,i-1
        if (c_associated(expected(i),expected(j))) return
      enddo
    enddo
    call SPOR64_RCONTRACT_LOAD(ipcontract,contract,valid)
    if (.not.valid) return
    call SPOR64_BOOT_CANONICAL64_CHECK(ipax,ipaxtrack,ipaxsystem,ipaxmacro,valid)
    if (.not.valid) return
    if (.not.EXACT_INVENTORY(ipglobal,BOOT_GLOBAL_NAMES)) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'SIGNATURE',3,12,'L_GLOBAL64')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'ROLE',3,12,'GLOBAL-K64')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'STATE',3,12,'GLOBAL-DONE')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'CASE',3,12,contract%case_name)) return
    if (.not.RECORD_MATCHES(ipglobal,'VERSION',1,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'NPLANE',1,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'EPOCH',1,1)) return
    call LCMGET(ipglobal,'VERSION',version)
    call LCMGET(ipglobal,'NPLANE',nplane)
    call LCMGET(ipglobal,'EPOCH',epoch)
    if (version /= 1.or.nplane /= EXPECTED_NPLANE.or.epoch /= 0) return
    do i=1,size(expected)
      if (.not.RECORD_MATCHES(ipglobal,names(i),-1,0)) return
      child=LCMGID(ipglobal,names(i))
      if (.not.SPOR64_BOOT64_SAME_TREE(child,expected(i))) return
    enddo
    if (.not.RECORD_MATCHES(ipglobal,'KEFF64',1,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'RHO64',1,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'NORM64',1,4)) return
    call LCMGET(ipglobal,'KEFF64',keff)
    call LCMGET(ipglobal,'RHO64',rho)
    call LCMGET(ipglobal,'NORM64',norm)
    if (.not.ieee_is_finite(keff).or.keff <= 0.0_real64) return
    if (.not.ieee_is_finite(rho).or.rho <= 0.0_real64) return
    if (.not.ieee_is_finite(norm).or.norm <= 0.0_real64) return
    if (transfer(rho,0_int64) /= transfer(1.0_real64/keff,0_int64)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-KEFF',keff)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-RHO',rho)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-NORM',norm)) return
    if (.not.RECORD_MATCHES(ipglobal,'RESIDUALS',3,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'TERM-EPS',3,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'COUNTERS',2,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'CAPS',2,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'INNER-STATE',1,1)) return
    if (.not.RECORD_MATCHES(ipax,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipglobal,'RESIDUALS',residual)
    call LCMGET(ipglobal,'TERM-EPS',limits)
    call LCMGET(ipglobal,'COUNTERS',counter)
    call LCMGET(ipglobal,'CAPS',caps)
    call LCMGET(ipglobal,'INNER-STATE',inner_state)
    call LCMGET(ipax,'EPS-CONVERGE',eps32)
    call LCMGET(ipax,'STATE-VECTOR',ax_state)
    call LCMGET(ipaxtrack,'STATE-VECTOR',ax_track_state)
    ! Original production TYPE K B1 SIGS becomes ITYPEC=3 in FLUGPI.
    if (ax_state(3) /= 1.or.ax_state(6) /= 3.or.ax_state(7) /= 3) return
    if (ax_state(10) /= 0) return
    if (.not.CHARACTER_RECORD_MATCHES(ipax,'OPTION',1,4,'B1')) return
    if (contract%flu_option /= 'B0') return
    if (.not.all(ieee_is_finite(eps32))) return
    if (any(transfer(eps32(1:3),0_int32,3) /= contract%eps_axial_bits)) return
    if (any(transfer(eps32(4:5),0_int32,2) /= 0_int32)) return
    if (.not.SAME64(limits,real(eps32(3:1:-1),real64))) return
    if (.not.all(ieee_is_finite(residual)).or.any(residual < 0.0_real64)) return
    if (any(residual >= limits)) return
    if (any(caps /= [ax_state(12),ax_state(11)])) return
    if (any(counter < [2,1]).or.any(counter > caps).or.inner_state /= 1) return
    if (ax_track_state(8) /= EXPECTED_NPLANE) return
    if (.not.RECORD_MATCHES(ipax,'SOUR64',NGRP,10)) return
    if (.not.RECORD_MATCHES(ipax,'SOUR',NGRP,10)) return
    ax_source=LCMGID(ipax,'SOUR64')
    ax_source32=LCMGID(ipax,'SOUR')
    allocate(values(ax_state(2)),mirror(ax_state(2)),stat=istat)
    if (istat /= 0) return
    do g=1,NGRP
      if (.not.ITEM_MATCH(ax_source,g,ax_state(2),4)) return
      if (.not.ITEM_MATCH(ax_source32,g,ax_state(2),2)) return
      call LCMGDL(ax_source,g,values)
      call LCMGDL(ax_source32,g,mirror)
      if (.not.all(ieee_is_finite(values))) return
      if (.not.all(ieee_is_finite(mirror))) return
      if (.not.SAME32(mirror,real(values,real32))) return
    enddo
    deallocate(values,mirror)

    ok=.true.
  end subroutine SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK

  subroutine SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax, &
      ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract,contract,ok)
    type(c_ptr), intent(in) :: ipprojected,ipglobal,ipax,ipaxtrack
    type(c_ptr), intent(in) :: ipaxsystem,ipaxmacro,iparchive,ipcontract
    type(SPOR64_ROUTE_CONTRACT), intent(out) :: contract
    logical, intent(out) :: ok
    type(c_ptr) :: expected(6),child,root_auth,tracks,libraries,fluxes
    type(c_ptr) :: archive_tracks,archive_libraries,archive_fluxes
    type(c_ptr) :: plane,plane_track,seed,auth,native,roots,mirrors,old_native
    type(c_ptr) :: ax_source,ax_source32
    character(len=12), parameter :: names(6) = &
        ['AX          ','AXTRACK     ','AXSYSTEM    ','AXMACRO     ', &
         'ARCHIVE     ','RCON        ']
    integer :: i,j,g,p,nreg,nunk,nmode,ncoef,istat,nsnap
    integer :: version,epoch,nplane,inner_state,plane_number,archive_nplane
    integer :: ax_state(NSTATE),ax_track_state(NSTATE),track_state(NSTATE)
    integer :: caps(2),counter(2),dims(4),state(NSTATE),old_state(NSTATE)
    integer, allocatable :: rank(:),offset(:),boff(:),key(:),imerge(:),keycur(:),keyanis(:)
    logical, allocatable :: seen(:)
    integer :: length,type_code,index_a,index_b
    real(real32) :: eps32(5)
    real(real32), allocatable :: basis(:),mirror(:),vol32(:),leak32(:)
    real(real64) :: keff,rho,norm,value,source_value,volume_sum
    real(real64) :: residual(3),limits(3),leak(3*NGRP),actual_rho
    real(real64), allocatable :: coordinates(:),values(:),reference(:)
    real(real64), allocatable :: old_values(:),volume(:),weight(:),saved(:)
    logical :: valid

    ok=.false.
    expected=[ipax,ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract]
    if (.not.c_associated(ipprojected).or..not.c_associated(ipglobal)) return
    do i=1,size(expected)
      if (.not.c_associated(expected(i))) return
      if (c_associated(ipprojected,expected(i))) return
      if (c_associated(ipglobal,expected(i))) return
      do j=1,i-1
        if (c_associated(expected(i),expected(j))) return
      enddo
    enddo
    if (c_associated(ipprojected,ipglobal)) return
    call SPOR64_RCONTRACT_LOAD(ipcontract,contract,valid)
    if (.not.valid) return
    call SPOR64_BOOT_CANONICAL64_CHECK(ipax,ipaxtrack,ipaxsystem,ipaxmacro,valid)
    if (.not.valid) return
    if (.not.EXACT_INVENTORY(ipglobal,BOOT_GLOBAL_NAMES)) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'SIGNATURE',3,12,'L_GLOBAL64')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'ROLE',3,12,'GLOBAL-K64')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'STATE',3,12,'GLOBAL-DONE')) return
    if (.not.CHARACTER_RECORD_MATCHES(ipglobal,'CASE',3,12,contract%case_name)) return
    if (.not.RECORD_MATCHES(ipglobal,'VERSION',1,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'NPLANE',1,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'EPOCH',1,1)) return
    call LCMGET(ipglobal,'VERSION',version)
    call LCMGET(ipglobal,'NPLANE',nplane)
    call LCMGET(ipglobal,'EPOCH',epoch)
    if (version /= 1.or.nplane /= EXPECTED_NPLANE.or.epoch /= 0) return
    do i=1,size(expected)
      if (.not.RECORD_MATCHES(ipglobal,names(i),-1,0)) return
      child=LCMGID(ipglobal,names(i))
      if (.not.SPOR64_BOOT64_SAME_TREE(child,expected(i))) return
    enddo
    if (.not.RECORD_MATCHES(ipglobal,'KEFF64',1,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'RHO64',1,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'NORM64',1,4)) return
    call LCMGET(ipglobal,'KEFF64',keff)
    call LCMGET(ipglobal,'RHO64',rho)
    call LCMGET(ipglobal,'NORM64',norm)
    if (.not.ieee_is_finite(keff).or.keff <= 0.0_real64) return
    if (.not.ieee_is_finite(rho).or.rho <= 0.0_real64) return
    if (.not.ieee_is_finite(norm).or.norm <= 0.0_real64) return
    if (transfer(rho,0_int64) /= transfer(1.0_real64/keff,0_int64)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-KEFF',keff)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-RHO',rho)) return
    if (.not.SCALAR_MATCH(ipax,'SPOT-X-NORM',norm)) return
    if (.not.RECORD_MATCHES(ipglobal,'RESIDUALS',3,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'TERM-EPS',3,4)) return
    if (.not.RECORD_MATCHES(ipglobal,'COUNTERS',2,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'CAPS',2,1)) return
    if (.not.RECORD_MATCHES(ipglobal,'INNER-STATE',1,1)) return
    if (.not.RECORD_MATCHES(ipax,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipglobal,'RESIDUALS',residual)
    call LCMGET(ipglobal,'TERM-EPS',limits)
    call LCMGET(ipglobal,'COUNTERS',counter)
    call LCMGET(ipglobal,'CAPS',caps)
    call LCMGET(ipglobal,'INNER-STATE',inner_state)
    call LCMGET(ipax,'EPS-CONVERGE',eps32)
    call LCMGET(ipax,'STATE-VECTOR',ax_state)
    call LCMGET(ipaxtrack,'STATE-VECTOR',ax_track_state)
    ! Original production TYPE K B1 SIGS becomes ITYPEC=3 in FLUGPI.
    if (ax_state(3) /= 1.or.ax_state(6) /= 3.or.ax_state(7) /= 3) return
    if (ax_state(10) /= 0) return
    if (.not.CHARACTER_RECORD_MATCHES(ipax,'OPTION',1,4,'B1')) return
    if (contract%flu_option /= 'B0') return
    if (.not.all(ieee_is_finite(eps32))) return
    if (any(transfer(eps32(1:3),0_int32,3) /= contract%eps_axial_bits)) return
    if (any(transfer(eps32(4:5),0_int32,2) /= 0_int32)) return
    if (.not.SAME64(limits,real(eps32(3:1:-1),real64))) return
    if (.not.all(ieee_is_finite(residual)).or.any(residual < 0.0_real64)) return
    if (any(residual >= limits)) return
    if (any(caps /= [ax_state(12),ax_state(11)])) return
    if (any(counter < [2,1]).or.any(counter > caps).or.inner_state /= 1) return
    if (ax_track_state(8) /= EXPECTED_NPLANE) return
    if (.not.RECORD_MATCHES(ipax,'SOUR64',NGRP,10)) return
    if (.not.RECORD_MATCHES(ipax,'SOUR',NGRP,10)) return
    ax_source=LCMGID(ipax,'SOUR64')
    ax_source32=LCMGID(ipax,'SOUR')
    allocate(values(ax_state(2)),mirror(ax_state(2)),stat=istat)
    if (istat /= 0) return
    do g=1,NGRP
      if (.not.ITEM_MATCH(ax_source,g,ax_state(2),4)) return
      if (.not.ITEM_MATCH(ax_source32,g,ax_state(2),2)) return
      call LCMGDL(ax_source,g,values)
      call LCMGDL(ax_source32,g,mirror)
      if (.not.all(ieee_is_finite(values))) return
      if (.not.all(ieee_is_finite(mirror))) return
      if (.not.SAME32(mirror,real(values,real32))) return
    enddo
    deallocate(values,mirror)

    ! One global/canonical authority is shared by all three projected seeds.
    if (.not.EXACT_INVENTORY(ipprojected,BOOT_ARCHIVE_NAMES)) return
    if (.not.CHARACTER_RECORD_MATCHES(ipprojected,'SIGNATURE',3,12,'L_ARCHIVE')) return
    if (.not.RECORD_MATCHES(ipprojected,'LISTDIM',1,1)) return
    call LCMGET(ipprojected,'LISTDIM',nplane)
    if (nplane /= EXPECTED_NPLANE) return
    if (.not.SCALAR_MATCH(ipprojected,'SPOT-ITER-K',keff)) return
    if (.not.RECORD_MATCHES(ipprojected,'GLOBAL64',-1,0)) return
    child=LCMGID(ipprojected,'GLOBAL64')
    if (.not.SPOR64_BOOT64_SAME_TREE(child,ipglobal)) return
    if (.not.RECORD_MATCHES(ipprojected,'SPOT-R64',-1,0)) return
    root_auth=LCMGID(ipprojected,'SPOT-R64')
    if (.not.EXACT_INVENTORY(root_auth,BOOT_ROOT_AUTH_NAMES)) return
    if (.not.CHARACTER_RECORD_MATCHES(root_auth,'STATE',4,16,'PROJECTED-BOOT')) return
    if (.not.SCALAR_MATCH(root_auth,'RHO',rho)) return
    if (.not.RECORD_MATCHES(root_auth,'NPLANE',1,1)) return
    if (.not.RECORD_MATCHES(root_auth,'EPOCH',1,1)) return
    call LCMGET(root_auth,'NPLANE',nplane)
    call LCMGET(root_auth,'EPOCH',epoch)
    if (nplane /= EXPECTED_NPLANE.or.epoch /= 0) return
    if (.not.CHARACTER_RECORD_MATCHES(iparchive,'SIGNATURE',3,12,'L_ARCHIVE')) return
    if (.not.RECORD_MATCHES(iparchive,'LISTDIM',1,1)) return
    call LCMGET(iparchive,'LISTDIM',archive_nplane)
    if (archive_nplane /= EXPECTED_NPLANE) return
    do i=1,2
      if (i == 1) then
        if (.not.RECORD_MATCHES(ipprojected,'TRACK',EXPECTED_NPLANE,10)) return
        if (.not.RECORD_MATCHES(iparchive,'TRACK',EXPECTED_NPLANE,10)) return
        child=LCMGID(ipprojected,'TRACK')
        archive_tracks=LCMGID(iparchive,'TRACK')
        do p=1,EXPECTED_NPLANE
          if (.not.LIST_ITEM_IS_DIRECTORY(child,p)) return
          if (.not.LIST_ITEM_IS_DIRECTORY(archive_tracks,p)) return
          plane=LCMGIL(child,p)
          seed=LCMGIL(archive_tracks,p)
          if (.not.SPOR64_BOOT64_SAME_TREE(plane,seed)) return
        enddo
      else
        if (.not.RECORD_MATCHES(ipprojected,'MICROLIB2',EXPECTED_NPLANE,10)) return
        if (.not.RECORD_MATCHES(iparchive,'MICROLIB2',EXPECTED_NPLANE,10)) return
        child=LCMGID(ipprojected,'MICROLIB2')
        archive_libraries=LCMGID(iparchive,'MICROLIB2')
        do p=1,EXPECTED_NPLANE
          if (.not.LIST_ITEM_IS_DIRECTORY(child,p)) return
          if (.not.LIST_ITEM_IS_DIRECTORY(archive_libraries,p)) return
          plane=LCMGIL(child,p)
          seed=LCMGIL(archive_libraries,p)
          if (.not.SPOR64_BOOT64_SAME_TREE(plane,seed)) return
        enddo
      endif
    enddo
    if (.not.RECORD_MATCHES(ipprojected,'FLUX',EXPECTED_NPLANE,10)) return
    if (.not.RECORD_MATCHES(iparchive,'FLUX',EXPECTED_NPLANE,10)) return
    tracks=LCMGID(ipprojected,'TRACK')
    libraries=LCMGID(ipprojected,'MICROLIB2')
    fluxes=LCMGID(ipprojected,'FLUX')
    archive_fluxes=LCMGID(iparchive,'FLUX')
    ! CANONICAL64_CHECK already recomputed and bit-checked every field below.
    call LCMGET(ipax,'SPOT-X-DIMS',dims)
    nsnap=dims(3)
    ncoef=dims(4)
    allocate(rank(NGRP),offset(NGRP+1),boff(NGRP+1),coordinates(ncoef),stat=istat)
    if (istat /= 0) return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    call LCMGET(ipax,'SPOT-X-OFF',offset)
    call LCMGET(ipax,'SPOT-X-BOFF',boff)
    allocate(basis(boff(NGRP+1)),stat=istat)
    if (istat /= 0) return
    call LCMGET(ipax,'SPOT-X-A',coordinates)
    call LCMGET(ipax,'SPOT-X-BASIS',basis)
    call LCMGET(ipax,'SPOT-X-L',leak)
    do p=1,EXPECTED_NPLANE
      if (.not.LIST_ITEM_IS_DIRECTORY(tracks,p)) return
      if (.not.LIST_ITEM_IS_DIRECTORY(libraries,p)) return
      if (.not.LIST_ITEM_IS_DIRECTORY(fluxes,p)) return
      if (.not.LIST_ITEM_IS_DIRECTORY(archive_fluxes,p)) return
      plane=LCMGIL(fluxes,p)
      plane_track=LCMGIL(tracks,p)
      seed=LCMGIL(archive_fluxes,p)
      if (.not.RECORD_MATCHES(plane_track,'STATE-VECTOR',NSTATE,1)) return
      call LCMGET(plane_track,'STATE-VECTOR',track_state)
      nreg=track_state(1)
      nunk=track_state(2)
      if (nreg /= ax_track_state(6).or.nreg <= 0.or.nunk <= nreg) return
      if (track_state(3) /= 1.or.track_state(6) /= 1) return
      if (track_state(4) <= 0.or.track_state(5) <= 0) return
      if (int(nunk,int64) /= int(nreg,int64)+int(track_state(5),int64)) return
      if (.not.EXACT_INVENTORY(plane,BOOT_PLANE_NAMES)) return
      if (.not.CHARACTER_RECORD_MATCHES(plane,'SIGNATURE',3,12,'L_FLUX')) return
      if (.not.RECORD_MATCHES(plane,'STATE-VECTOR',NSTATE,1)) return
      call LCMGET(plane,'STATE-VECTOR',state)
      if (any(state(1:7) /= [NGRP,nunk,1,0,0,0,0])) return
      if (state(8) /= contract%flu_acce_free.or.state(9) /= contract%flu_acce_accel) return
      if (state(10) /= 1.or.state(11) /= contract%flu_maxinr.or.state(12) /= contract%flu_maxout) return
      if (any(state(13:16) /= 0).or.state(17) /= track_state(4).or.state(18) /= 1) return
      if (any(state(19:NSTATE) /= 0)) return
      if (.not.RECORD_MATCHES(plane,'EPS-CONVERGE',5,2)) return
      call LCMGET(plane,'EPS-CONVERGE',eps32)
      if (any(transfer(eps32(1:3),0_int32,3) /= contract%eps_radial_bits)) return
      if (any(transfer(eps32(4:5),0_int32,2) /= 0_int32)) return
      if (.not.RECORD_MATCHES(plane,'KEYFLX',nreg,1)) return
      if (.not.RECORD_MATCHES(plane_track,'KEYFLX',nreg,1)) return
      if (.not.RECORD_MATCHES(plane_track,'KEYFLX$ANIS',nreg,1)) return
      if (.not.RECORD_MATCHES(plane_track,'KEYCUR$MCCG',track_state(5),1)) return
      if (.not.RECORD_MATCHES(plane_track,'VOLUME',nreg,2)) return
      if (.not.RECORD_MATCHES(plane,'VOLUME64',nreg,4)) return
      if (.not.RECORD_MATCHES(plane,'WEIGHT64',nreg,4)) return
      if (.not.RECORD_MATCHES(plane,'IMERGE-LEAK',track_state(4),1)) return
      if (.not.CHARACTER_RECORD_MATCHES(plane,'OPTION',1,4,contract%flu_option)) return
      if (.not.CHARACTER_RECORD_MATCHES(plane,'LINK.MACRO',3,12,'MACRO0')) return
      if (.not.CHARACTER_RECORD_MATCHES(plane,'LINK.TRACK',3,12,'TRACK')) return
      if (.not.CHARACTER_RECORD_MATCHES(plane,'LINK.SYSTEM',3,12,'SYSTEM')) return
      allocate(key(nreg),imerge(nreg),vol32(nreg),volume(nreg),weight(nreg),saved(nreg),stat=istat)
      if (istat /= 0) return
      call LCMGET(plane_track,'KEYFLX',key)
      call LCMGET(plane,'KEYFLX',imerge)
      if (any(key /= imerge).or.any(key < 1).or.any(key > nunk)) return
      allocate(keyanis(nreg),keycur(track_state(5)),seen(nunk),stat=istat)
      if (istat /= 0) return
      call LCMGET(plane_track,'KEYFLX$ANIS',keyanis)
      call LCMGET(plane_track,'KEYCUR$MCCG',keycur)
      if (any(key /= keyanis).or.any(keycur < 1).or.any(keycur > nunk)) return
      seen=.false.
      do i=1,nreg
        if (seen(key(i))) return
        seen(key(i))=.true.
      enddo
      do i=1,size(keycur)
        if (seen(keycur(i))) return
        seen(keycur(i))=.true.
      enddo
      if (.not.all(seen)) return
      deallocate(imerge)
      allocate(imerge(track_state(4)),stat=istat)
      if (istat /= 0) return
      call LCMGET(plane,'IMERGE-LEAK',imerge)
      if (any(imerge /= 1)) return
      call LCMGET(plane_track,'VOLUME',vol32)
      if (.not.all(ieee_is_finite(vol32)).or.any(vol32 <= 0.0_real32)) return
      volume=real(vol32,real64)
      volume_sum=sum(volume)
      if (.not.ieee_is_finite(volume_sum).or.volume_sum <= 0.0_real64) return
      weight=volume/volume_sum
      call LCMGET(plane,'VOLUME64',saved)
      if (.not.SAME64(saved,volume)) return
      call LCMGET(plane,'WEIGHT64',saved)
      if (.not.SAME64(saved,weight)) return
      if (.not.RECORD_MATCHES(plane,'SPOT-R64',-1,0)) return
      auth=LCMGID(plane,'SPOT-R64')
      if (.not.EXACT_INVENTORY(auth,BOOT_PLANE_AUTH_NAMES)) return
      if (.not.CHARACTER_RECORD_MATCHES(auth,'STATE',4,16,'PROJECTED-BOOT')) return
      if (.not.SCALAR_MATCH(auth,'RHO',rho)) return
      if (.not.RECORD_MATCHES(auth,'PLANE',1,1)) return
      if (.not.RECORD_MATCHES(auth,'EPOCH',1,1)) return
      call LCMGET(auth,'PLANE',plane_number)
      call LCMGET(auth,'EPOCH',epoch)
      if (plane_number /= p.or.epoch /= 0) return
      if (.not.RECORD_MATCHES(auth,'FLUX',NGRP,10)) return
      if (.not.RECORD_MATCHES(plane,'ROOT-FLUX64',NGRP,10)) return
      if (.not.RECORD_MATCHES(plane,'FLUX',NGRP,10)) return
      if (.not.RECORD_MATCHES(seed,'FLUX64',NGRP,10)) return
      if (.not.RECORD_MATCHES(seed,'STATE-VECTOR',NSTATE,1)) return
      call LCMGET(seed,'STATE-VECTOR',old_state)
      if (old_state(1) /= NGRP.or.old_state(2) /= nunk) return
      native=LCMGID(auth,'FLUX')
      roots=LCMGID(plane,'ROOT-FLUX64')
      mirrors=LCMGID(plane,'FLUX')
      old_native=LCMGID(seed,'FLUX64')
      allocate(values(nunk),reference(nunk),old_values(nunk),mirror(nunk),leak32(NGRP),stat=istat)
      if (istat /= 0) return
      if (.not.RECORD_MATCHES(plane,'LEAK1D64',NGRP,4)) return
      if (.not.RECORD_MATCHES(plane,'SPOT-LEAK1D',NGRP,2)) return
      deallocate(saved)
      allocate(saved(NGRP),stat=istat)
      if (istat /= 0) return
      call LCMGET(plane,'LEAK1D64',saved)
      if (.not.SAME64(saved,leak((p-1)*NGRP+1:p*NGRP))) return
      call LCMGET(plane,'SPOT-LEAK1D',leak32)
      if (.not.SAME32(leak32,real(saved,real32))) return
      do g=1,NGRP
        if (.not.ITEM_MATCH(native,g,nunk,4)) return
        if (.not.ITEM_MATCH(roots,g,nunk,4)) return
        if (.not.ITEM_MATCH(mirrors,g,nunk,2)) return
        if (.not.ITEM_MATCH(old_native,g,nunk,4)) return
        call LCMGDL(native,g,values)
        call LCMGDL(roots,g,reference)
        call LCMGDL(mirrors,g,mirror)
        call LCMGDL(old_native,g,old_values)
        if (.not.all(ieee_is_finite(values)).or..not.all(ieee_is_finite(old_values))) return
        if (.not.all(ieee_is_finite(mirror))) return
        if (.not.SAME64(values,reference)) return
        if (.not.SAME32(mirror,real(values,real32))) return
        nmode=rank(g)
        ! Exactly the original SPOPROJ64 FIXB scalar contraction, no extra norm.
        reference=old_values
        do i=1,nreg
          value=0.0_real64
          do j=1,nmode
            index_a=offset(g)+(p-1)*nmode+j
            index_b=boff(g)+(j-1)*nreg+i
            value=value+real(basis(index_b),real64)*coordinates(index_a)
          enddo
          if (.not.ieee_is_finite(value).or.value <= 0.0_real64) return
          reference(key(i))=value
        enddo
        if (.not.SAME64(values,reference)) return
      enddo
      deallocate(leak32,mirror,old_values,reference,values,saved,weight,volume,vol32,imerge,key)
      deallocate(seen,keycur,keyanis)
    enddo
    ok=.true.
  end subroutine SPOR64_BOOT_CONTEXT64_READ

  logical function SCALAR_MATCH(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected
    real(real64) :: actual
    SCALAR_MATCH=.false.
    if (.not.RECORD_MATCHES(object,name,1,4)) return
    call LCMGET(object,name,actual)
    SCALAR_MATCH=transfer(actual,0_int64)==transfer(expected,0_int64)
  end function SCALAR_MATCH
  logical function ITEM_MATCH(list,index,length,type_code)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index,length,type_code
    integer :: actual_length,actual_type
    ITEM_MATCH=.false.
    if (.not.c_associated(list)) return
    call LCMLEL(list,index,actual_length,actual_type)
    ITEM_MATCH=actual_length==length.and.actual_type==type_code
  end function ITEM_MATCH
  logical function SAME64(left,right)
    real(real64), intent(in) :: left(:),right(:)
    SAME64=.false.
    if (size(left) /= size(right)) return
    SAME64=all(transfer(left,0_int64,size(left))==transfer(right,0_int64,size(right)))
  end function SAME64
  logical function SAME32(left,right)
    real(real32), intent(in) :: left(:),right(:)
    SAME32=.false.
    if (size(left) /= size(right)) return
    SAME32=all(transfer(left,0_int32,size(left))==transfer(right,0_int32,size(right)))
  end function SAME32
end module SPOR64_BOOT_CONTEXT64_V2

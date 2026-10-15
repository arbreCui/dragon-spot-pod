module SPOR64_BOOT64
  ! NEW SOURCE, current epoch. This is not a recovery of SHA 5f88b893.
  ! A typed serialization boundary, not a transport or physics certificate.
  ! The native caller and immutable context files must be independently pinned
  ! by the host. The producer entry is called only at the genuine strict native
  ! terminal branch. This module neither solves nor fabricates that branch.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_MEMORY_ROOT, EXACT_INVENTORY, RECORD_MATCHES
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT, SPOR64_RCONTRACT_LOAD
  implicit none
  private

  integer, parameter, public :: ROOT64_REFUSED = 1
  integer, parameter, public :: ROOT64_PUBLISHED = 2
  integer, parameter, public :: ROOT64_LOADED = 3
  integer, parameter, public :: ROOT64_IMPORTED = 4
  integer, parameter :: NGRP = 370, NSTATE = 40, NIFIS = 32
  integer, parameter :: MAX_DEPTH = 64, MAX_NODES = 2000000
  integer, parameter :: MAX_RECORD_WORDS = 16777216
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1) == int32 .and. kind(1.0) == real32 .and. kind(0.0d0) == real64)
  character(len=12), parameter :: SEAL_NAMES(20) = &
      ['SIGNATURE   ','VERSION     ','STATE       ','ROLE        ', &
       'DIMS        ','PLANE       ','EPOCH       ','CASE        ', &
       'KEFF64      ','GATE64      ','LIMIT64     ','TERM-INT    ', &
       'TRACK       ','SYSTEM      ','MATERIAL    ','RCONTRACT   ', &
       'VOLUME64    ','WEIGHT64    ','MATCOD      ','KEYFLX      ']

  public :: SPOR64_BOOT64_PUBLISH_NATIVE, SPOR64_BOOT64_READ_NATIVE
  public :: SPOR64_BOOT64_IMPORT_NATIVE, SPOR64_BOOT64_SAME_TREE

contains

  ! Publish the existing native REAL64 terminal image, preserving every bit.
  ! terminal_flux is cross-checked against the driver's existing FLUX64 list.
  ! The three residuals and terminal counters are actual native values; the
  ! host must independently verify that this call is on its strict PASS branch.
  subroutine SPOR64_BOOT64_PUBLISH_NATIVE(ipflux,iptrack,ipsystem, &
      ipmaterial,ipcontract,plane,epoch,terminal_flux,keff64, &
      residual64,outer_step,inner_step,inner_state,status)
    type(c_ptr), intent(in) :: ipflux, iptrack, ipsystem, ipmaterial, ipcontract
    integer, intent(in) :: plane, epoch, outer_step, inner_step, inner_state
    real(real64), intent(in) :: terminal_flux(:,:), keff64, residual64(3)
    integer, intent(out) :: status
    type(SPOR64_ROUTE_CONTRACT) :: contract
    integer :: dims(4), term_int(3), group, allocation_status
    integer, allocatable :: key(:), material_code(:)
    real(real64), allocatable :: volume64(:), weight64(:), saved64(:)
    real(real32), allocatable :: mirror32(:)
    real(real32) :: keff32
    real(real64) :: limits64(3), saved_keff64
    type(c_ptr) :: existing, mirrors, roots, seal, reference, child
    logical :: valid

    status = ROOT64_REFUSED
    if (plane < 1 .or. plane > 3 .or. epoch < 0) return
    call READ_CONTEXT(iptrack,ipsystem,ipmaterial,ipcontract, &
        dims,key,material_code,volume64,weight64,contract,valid)
    if (.not. valid) return
    if (any(shape(terminal_flux) /= [dims(2),NGRP])) return
    if (.not. all(ieee_is_finite(terminal_flux))) return
    if (.not. ieee_is_finite(keff64) .or. keff64 <= 0.0_real64) return
    if (.not. all(ieee_is_finite(residual64))) return
    if (any(residual64 < 0.0_real64)) return
    limits64 = real(transfer(contract%eps_radial_bits,0.0_real32),real64)
    if (any(residual64 >= limits64)) return
    if (outer_step < 2 .or. outer_step > contract%flu_maxout) return
    if (inner_step < 1 .or. inner_step > contract%flu_maxinr) return
    if (inner_state /= 1) return
    if (.not. FLUX_HEADER_VALID(ipflux,dims,key,contract)) return
    if (.not. ABSENT_RECORD(ipflux,'ROOT-FLUX64')) return
    if (.not. ABSENT_RECORD(ipflux,'ROOT64-SEAL')) return
    if (.not. ABSENT_RECORD(ipflux,'SPOT-R64')) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX64',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'SPOT-KEFF64',1,4)) return
    if (.not. RECORD_MATCHES(ipflux,'K-EFFECTIVE',1,2)) return
    call LCMGET(ipflux,'SPOT-KEFF64',saved_keff64)
    call LCMGET(ipflux,'K-EFFECTIVE',keff32)
    if (transfer(saved_keff64,0_int64) /= transfer(keff64,0_int64)) return
    if (.not. ieee_is_finite(real(keff64,real32))) return
    if (transfer(keff32,0_int32) /= transfer(real(keff64,real32),0_int32)) return
    existing = LCMGID(ipflux,'FLUX64')
    mirrors = LCMGID(ipflux,'FLUX')
    allocate(saved64(dims(2)),mirror32(dims(2)),stat=allocation_status)
    if (allocation_status /= 0) return
    do group = 1, NGRP
      if (.not. LIST_RECORD_MATCHES(existing,group,dims(2),4)) return
      if (.not. LIST_RECORD_MATCHES(mirrors,group,dims(2),2)) return
      call LCMGDL(existing,group,saved64)
      call LCMGDL(mirrors,group,mirror32)
      if (.not. SAME64(saved64,terminal_flux(:,group))) return
      if (.not. all(ieee_is_finite(real(saved64,real32)))) return
      if (.not. SAME32(mirror32,real(saved64,real32))) return
      if (any(saved64(key) <= 0.0_real64)) return
    end do
    ! All refusals above precede mutation. ROOT64-SEAL/STATE is written last.
    roots = LCMLID(ipflux,'ROOT-FLUX64',NGRP)
    do group = 1, NGRP
      call LCMPDL(roots,group,dims(2),4,terminal_flux(:,group))
    end do
    seal = LCMDID(ipflux,'ROOT64-SEAL')
    call LCMPTC(seal,'SIGNATURE',12,'L_ROOT64    ')
    call LCMPUT(seal,'VERSION',1,1,1)
    call LCMPTC(seal,'ROLE',12,'NATIVE-K64  ')
    call LCMPUT(seal,'DIMS',4,1,dims)
    call LCMPUT(seal,'PLANE',1,1,plane)
    call LCMPUT(seal,'EPOCH',1,1,epoch)
    call LCMPTC(seal,'CASE',12,contract%case_name)
    call LCMPUT(seal,'KEFF64',1,4,keff64)
    call LCMPUT(seal,'GATE64',3,4,residual64)
    call LCMPUT(seal,'LIMIT64',3,4,limits64)
    term_int = [outer_step,inner_step,inner_state]
    call LCMPUT(seal,'TERM-INT',3,1,term_int)
    call LCMPUT(seal,'VOLUME64',dims(3),4,volume64)
    call LCMPUT(seal,'WEIGHT64',dims(3),4,weight64)
    call LCMPUT(seal,'MATCOD',dims(3),1,material_code)
    call LCMPUT(seal,'KEYFLX',dims(3),1,key)
    child = LCMDID(seal,'TRACK')
    call LCMEQU(iptrack,child)
    child = LCMDID(seal,'SYSTEM')
    call LCMEQU(ipsystem,child)
    child = LCMDID(seal,'MATERIAL')
    call LCMEQU(ipmaterial,child)
    child = LCMDID(seal,'RCONTRACT')
    call LCMEQU(ipcontract,child)
    ! This is an internal consistency copy, not an independent witness or
    ! terminal solve. The original host's separate full-file SHA/7ID binding
    ! must reject coherent edits to all copies before this native read.
    reference = LCMLID(seal,'ROOT-REF64',NGRP)
    do group = 1, NGRP
      call LCMPDL(reference,group,dims(2),4,terminal_flux(:,group))
    end do
    call LCMPTC(seal,'STATE',12,'PRODUCED    ')
    status = ROOT64_PUBLISHED
  end subroutine SPOR64_BOOT64_PUBLISH_NATIVE


  ! The only accepted numerical authority is ROOT-FLUX64, type 4 throughout.
  ! FLUX/FLUX64 are checked mirrors; neither supplies missing authority.
  subroutine SPOR64_BOOT64_READ_NATIVE(ipflux,iptrack,ipsystem, &
      ipmaterial,ipcontract,plane,epoch,flux64,status)
    type(c_ptr), intent(in) :: ipflux, iptrack, ipsystem, ipmaterial, ipcontract
    integer, intent(in) :: plane, epoch
    real(real64), allocatable, intent(out) :: flux64(:,:)
    integer, intent(out) :: status
    type(SPOR64_ROUTE_CONTRACT) :: contract
    integer :: dims(4), saved_dims(4), saved_plane, saved_epoch, version
    integer :: term_int(3), group, allocation_status
    integer, allocatable :: key(:), material_code(:), saved_int(:)
    real(real64), allocatable :: volume64(:), weight64(:), saved64(:)
    real(real64), allocatable :: reference64(:), native64(:), staged(:,:)
    real(real32), allocatable :: mirror32(:)
    real(real64) :: keff64, native_keff64, residual64(3), limits64(3)
    real(real64) :: expected_limits(3)
    real(real32) :: keff32
    type(c_ptr) :: seal, root_list, reference, mirrors, native_list, child
    logical :: valid
    character(len=12) :: all_names(21)

    status = ROOT64_REFUSED
    if (plane < 1 .or. plane > 3 .or. epoch < 0) return
    call READ_CONTEXT(iptrack,ipsystem,ipmaterial,ipcontract, &
        dims,key,material_code,volume64,weight64,contract,valid)
    if (.not. valid) return
    if (.not. FLUX_HEADER_VALID(ipflux,dims,key,contract)) return
    if (.not. ABSENT_RECORD(ipflux,'SPOT-R64')) return
    if (.not. RECORD_MATCHES(ipflux,'ROOT64-SEAL',-1,0)) return
    seal = LCMGID(ipflux,'ROOT64-SEAL')
    all_names(1:20) = SEAL_NAMES
    all_names(21) = 'ROOT-REF64'
    if (.not. EXACT_INVENTORY(seal,all_names)) return
    if (.not. CHARACTER_RECORD_MATCHES(seal,'SIGNATURE',3,12,'L_ROOT64')) return
    if (.not. CHARACTER_RECORD_MATCHES(seal,'STATE',3,12,'PRODUCED')) return
    if (.not. CHARACTER_RECORD_MATCHES(seal,'ROLE',3,12,'NATIVE-K64')) return
    if (.not. CHARACTER_RECORD_MATCHES(seal,'CASE',3,12,contract%case_name)) return
    if (.not. RECORD_MATCHES(seal,'VERSION',1,1)) return
    if (.not. RECORD_MATCHES(seal,'DIMS',4,1)) return
    if (.not. RECORD_MATCHES(seal,'PLANE',1,1)) return
    if (.not. RECORD_MATCHES(seal,'EPOCH',1,1)) return
    call LCMGET(seal,'VERSION',version)
    call LCMGET(seal,'DIMS',saved_dims)
    call LCMGET(seal,'PLANE',saved_plane)
    call LCMGET(seal,'EPOCH',saved_epoch)
    if (version /= 1 .or. any(saved_dims /= dims)) return
    if (saved_plane /= plane .or. saved_epoch /= epoch) return
    if (.not. RECORD_MATCHES(seal,'TERM-INT',3,1)) return
    if (.not. RECORD_MATCHES(seal,'GATE64',3,4)) return
    if (.not. RECORD_MATCHES(seal,'LIMIT64',3,4)) return
    call LCMGET(seal,'TERM-INT',term_int)
    call LCMGET(seal,'GATE64',residual64)
    call LCMGET(seal,'LIMIT64',limits64)
    expected_limits = real(transfer(contract%eps_radial_bits,0.0_real32),real64)
    if (.not. SAME64(limits64,expected_limits)) return
    if (.not. all(ieee_is_finite(residual64))) return
    if (any(residual64 < 0.0_real64) .or. any(residual64 >= limits64)) return
    if (term_int(1) < 2 .or. term_int(1) > contract%flu_maxout) return
    if (term_int(2) < 1 .or. term_int(2) > contract%flu_maxinr) return
    if (term_int(3) /= 1) return
    if (.not. RECORD_MATCHES(seal,'KEFF64',1,4)) return
    if (.not. RECORD_MATCHES(ipflux,'SPOT-KEFF64',1,4)) return
    if (.not. RECORD_MATCHES(ipflux,'K-EFFECTIVE',1,2)) return
    call LCMGET(seal,'KEFF64',keff64)
    call LCMGET(ipflux,'SPOT-KEFF64',native_keff64)
    call LCMGET(ipflux,'K-EFFECTIVE',keff32)
    if (.not. ieee_is_finite(keff64) .or. keff64 <= 0.0_real64) return
    if (transfer(keff64,0_int64) /= transfer(native_keff64,0_int64)) return
    if (.not. ieee_is_finite(real(keff64,real32))) return
    if (transfer(keff32,0_int32) /= transfer(real(keff64,real32),0_int32)) return
    if (.not. RECORD_MATCHES(seal,'TRACK',-1,0)) return
    if (.not. RECORD_MATCHES(seal,'SYSTEM',-1,0)) return
    if (.not. RECORD_MATCHES(seal,'MATERIAL',-1,0)) return
    if (.not. RECORD_MATCHES(seal,'RCONTRACT',-1,0)) return
    child = LCMGID(seal,'TRACK')
    if (.not. SPOR64_BOOT64_SAME_TREE(child,iptrack)) return
    child = LCMGID(seal,'SYSTEM')
    if (.not. SPOR64_BOOT64_SAME_TREE(child,ipsystem)) return
    child = LCMGID(seal,'MATERIAL')
    if (.not. SPOR64_BOOT64_SAME_TREE(child,ipmaterial)) return
    child = LCMGID(seal,'RCONTRACT')
    if (.not. SPOR64_BOOT64_SAME_TREE(child,ipcontract)) return
    allocate(saved_int(dims(3)),saved64(max(dims(2),dims(3))), &
        reference64(dims(2)),native64(dims(2)),mirror32(dims(2)), &
        staged(dims(2),NGRP),stat=allocation_status)
    if (allocation_status /= 0) return
    if (.not. RECORD_MATCHES(seal,'KEYFLX',dims(3),1)) return
    if (.not. RECORD_MATCHES(seal,'MATCOD',dims(3),1)) return
    if (.not. RECORD_MATCHES(seal,'VOLUME64',dims(3),4)) return
    if (.not. RECORD_MATCHES(seal,'WEIGHT64',dims(3),4)) return
    call LCMGET(seal,'KEYFLX',saved_int)
    if (any(saved_int /= key)) return
    call LCMGET(seal,'MATCOD',saved_int)
    if (any(saved_int /= material_code)) return
    call LCMGET(seal,'VOLUME64',saved64(1:dims(3)))
    if (.not. SAME64(saved64(1:dims(3)),volume64)) return
    call LCMGET(seal,'WEIGHT64',saved64(1:dims(3)))
    if (.not. SAME64(saved64(1:dims(3)),weight64)) return
    if (.not. RECORD_MATCHES(ipflux,'ROOT-FLUX64',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX64',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(seal,'ROOT-REF64',NGRP,10)) return
    root_list = LCMGID(ipflux,'ROOT-FLUX64')
    reference = LCMGID(seal,'ROOT-REF64')
    native_list = LCMGID(ipflux,'FLUX64')
    mirrors = LCMGID(ipflux,'FLUX')
    do group = 1, NGRP
      if (.not. LIST_RECORD_MATCHES(root_list,group,dims(2),4)) return
      if (.not. LIST_RECORD_MATCHES(reference,group,dims(2),4)) return
      if (.not. LIST_RECORD_MATCHES(native_list,group,dims(2),4)) return
      if (.not. LIST_RECORD_MATCHES(mirrors,group,dims(2),2)) return
      call LCMGDL(root_list,group,staged(:,group))
      call LCMGDL(reference,group,reference64)
      call LCMGDL(native_list,group,native64)
      call LCMGDL(mirrors,group,mirror32)
      if (.not. all(ieee_is_finite(staged(:,group)))) return
      if (.not. SAME64(staged(:,group),reference64)) return
      if (.not. SAME64(staged(:,group),native64)) return
      if (.not. all(ieee_is_finite(real(staged(:,group),real32)))) return
      if (.not. SAME32(mirror32,real(staged(:,group),real32))) return
      if (any(staged(key,group) <= 0.0_real64)) return
    end do
    call move_alloc(staged,flux64)
    status = ROOT64_LOADED
  end subroutine SPOR64_BOOT64_READ_NATIVE


  subroutine SPOR64_BOOT64_IMPORT_NATIVE(ipout,ipflux,iptrack,ipsystem, &
      ipmaterial,ipcontract,plane,epoch,status)
    type(c_ptr), intent(in) :: ipout, ipflux, iptrack, ipsystem, ipmaterial, ipcontract
    integer, intent(in) :: plane, epoch
    integer, intent(out) :: status
    real(real64), allocatable :: flux64(:,:)
    integer :: read_status
    status = ROOT64_REFUSED
    if (.not. EMPTY_MEMORY_ROOT(ipout)) return
    if (c_associated(ipout,ipflux) .or. c_associated(ipout,iptrack)) return
    if (c_associated(ipout,ipsystem) .or. c_associated(ipout,ipmaterial)) return
    if (c_associated(ipout,ipcontract)) return
    call SPOR64_BOOT64_READ_NATIVE(ipflux,iptrack,ipsystem,ipmaterial, &
        ipcontract,plane,epoch,flux64,read_status)
    if (read_status /= ROOT64_LOADED) return
    call LCMEQU(ipflux,ipout)
    status = ROOT64_IMPORTED
  end subroutine SPOR64_BOOT64_IMPORT_NATIVE


  subroutine READ_CONTEXT(iptrack,ipsystem,ipmaterial,ipcontract, &
      dims,key,material_code,volume64,weight64,contract,valid)
    type(c_ptr), intent(in) :: iptrack, ipsystem, ipmaterial, ipcontract
    integer, intent(out) :: dims(4)
    integer, allocatable, intent(out) :: key(:), material_code(:)
    real(real64), allocatable, intent(out) :: volume64(:), weight64(:)
    type(SPOR64_ROUTE_CONTRACT), intent(out) :: contract
    logical, intent(out) :: valid
    integer :: track_state(NSTATE), system_state(NSTATE), macro_state(NSTATE)
    integer :: nreg, nunk, nmat, nsurface, allocation_status, i
    integer, allocatable :: keycur(:)
    logical, allocatable :: seen(:)
    real(real32), allocatable :: volume32(:)
    real(real64) :: volume_sum
    type(c_ptr) :: macro
    logical :: loaded
    valid = .false.
    dims = 0
    if (.not. c_associated(iptrack) .or. .not. c_associated(ipsystem)) return
    if (.not. c_associated(ipmaterial) .or. .not. c_associated(ipcontract)) return
    if (.not. CHARACTER_RECORD_MATCHES(iptrack,'SIGNATURE',3,12,'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(iptrack,'TRACK-TYPE',3,12,'MCCG')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'SIGNATURE',3,12,'L_PIJ')) return
    call SPOR64_RCONTRACT_LOAD(ipcontract,contract,loaded)
    if (.not. loaded) return
    if (.not. RECORD_MATCHES(iptrack,'STATE-VECTOR',NSTATE,1)) return
    if (.not. RECORD_MATCHES(ipsystem,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(iptrack,'STATE-VECTOR',track_state)
    call LCMGET(ipsystem,'STATE-VECTOR',system_state)
    nreg = track_state(1)
    nunk = track_state(2)
    nmat = track_state(4)
    nsurface = track_state(5)
    if (nreg <= 0 .or. nunk <= 0 .or. nmat <= 0 .or. nsurface <= 0) return
    if (int(nreg,int64)+int(nsurface,int64) /= int(nunk,int64)) return
    if (track_state(3) /= 1 .or. track_state(6) /= 1) return
    if (system_state(8) /= NGRP .or. system_state(9) /= nunk) return
    if (system_state(10) /= nmat) return
    if (CHARACTER_RECORD_MATCHES(ipmaterial,'SIGNATURE',3,12,'L_MACROLIB')) then
      macro = ipmaterial
    else
      if (.not. CHARACTER_RECORD_MATCHES(ipmaterial,'SIGNATURE',3,12,'L_LIBRARY')) return
      if (.not. RECORD_MATCHES(ipmaterial,'MACROLIB',-1,0)) return
      macro = LCMGID(ipmaterial,'MACROLIB')
    end if
    if (.not. RECORD_MATCHES(macro,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(macro,'STATE-VECTOR',macro_state)
    if (macro_state(1) /= NGRP .or. macro_state(2) /= nmat) return
    if (macro_state(3) /= 3 .or. macro_state(4) /= NIFIS) return
    if (.not. RECORD_MATCHES(iptrack,'KEYFLX$ANIS',nreg,1)) return
    if (.not. RECORD_MATCHES(iptrack,'KEYCUR$MCCG',nsurface,1)) return
    if (.not. RECORD_MATCHES(iptrack,'MATCOD',nreg,1)) return
    if (.not. RECORD_MATCHES(iptrack,'VOLUME',nreg,2)) return
    allocate(key(nreg),keycur(nsurface),material_code(nreg),volume32(nreg), &
        volume64(nreg),weight64(nreg),seen(nunk),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(iptrack,'KEYFLX$ANIS',key)
    call LCMGET(iptrack,'KEYCUR$MCCG',keycur)
    call LCMGET(iptrack,'MATCOD',material_code)
    call LCMGET(iptrack,'VOLUME',volume32)
    if (any(key < 1) .or. any(key > nunk)) return
    if (any(keycur < 1) .or. any(keycur > nunk)) return
    if (any(material_code < 1) .or. any(material_code > nmat)) return
    seen = .false.
    do i = 1, nreg
      if (seen(key(i))) return
      seen(key(i)) = .true.
    end do
    do i = 1, nsurface
      if (seen(keycur(i))) return
      seen(keycur(i)) = .true.
    end do
    if (.not. all(seen)) return
    if (.not. all(ieee_is_finite(volume32))) return
    if (any(volume32 <= 0.0_real32)) return
    volume64 = real(volume32,real64)
    volume_sum = sum(volume64)
    if (.not. ieee_is_finite(volume_sum) .or. volume_sum <= 0.0_real64) return
    weight64 = volume64/volume_sum
    if (.not. all(ieee_is_finite(weight64)) .or. any(weight64 <= 0.0_real64)) return
    dims = [NGRP,nunk,nreg,nmat]
    valid = .true.
  end subroutine READ_CONTEXT


  logical function FLUX_HEADER_VALID(ipflux,dims,key,contract)
    type(c_ptr), intent(in) :: ipflux
    integer, intent(in) :: dims(4), key(:)
    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract
    integer :: flux_state(NSTATE), saved_key(size(key))
    real(real32) :: eps32(5)
    FLUX_HEADER_VALID = .false.
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'SIGNATURE',3,12,'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipflux,'STATE-VECTOR',NSTATE,1)) return
    if (.not. RECORD_MATCHES(ipflux,'KEYFLX',dims(3),1)) return
    if (.not. RECORD_MATCHES(ipflux,'EPS-CONVERGE',5,2)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'OPTION',1,4,contract%flu_option)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.TRACK',3,12,'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.SYSTEM',3,12,'SYSTEM')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.MACRO',3,12,'MICROLIB2') .and. &
        .not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.MACRO',3,12,'MACRO0')) return
    call LCMGET(ipflux,'STATE-VECTOR',flux_state)
    call LCMGET(ipflux,'KEYFLX',saved_key)
    call LCMGET(ipflux,'EPS-CONVERGE',eps32)
    if (flux_state(1) /= NGRP .or. flux_state(2) /= dims(2)) return
    if (flux_state(3) /= 1 .or. flux_state(17) /= dims(4)) return
    if (flux_state(4) /= 0 .or. flux_state(5) /= 0) return
    if (flux_state(6) /= 2) return
    if (flux_state(7) /= 0) return
    if (flux_state(8) /= contract%flu_acce_free) return
    if (flux_state(9) /= contract%flu_acce_accel) return
    if (flux_state(10) /= 0 .and. flux_state(10) /= 1) return
    if (flux_state(11) /= contract%flu_maxinr) return
    if (flux_state(12) /= contract%flu_maxout) return
    if (flux_state(18) /= 1) return
    if (any(saved_key /= key)) return
    if (.not. all(ieee_is_finite(eps32))) return
    if (any(transfer(eps32(1:3),[0_int32,0_int32,0_int32]) /= contract%eps_radial_bits)) return
    if (any(abs(eps32(4:5)) > 0.0_real32)) return
    FLUX_HEADER_VALID = .true.
  end function FLUX_HEADER_VALID


  logical function SAME64(left,right)
    real(real64), intent(in) :: left(:), right(:)
    SAME64 = .false.
    if (size(left) /= size(right)) return
    SAME64 = all(transfer(left,0_int64,size(left)) == transfer(right,0_int64,size(right)))
  end function SAME64

  logical function SAME32(left,right)
    real(real32), intent(in) :: left(:), right(:)
    SAME32 = .false.
    if (size(left) /= size(right)) return
    SAME32 = all(transfer(left,0_int32,size(left)) == transfer(right,0_int32,size(right)))
  end function SAME32

  logical function LIST_RECORD_MATCHES(object,index,length,type_code)
    type(c_ptr), intent(in) :: object
    integer, intent(in) :: index, length, type_code
    integer :: actual_length, actual_type
    LIST_RECORD_MATCHES = .false.
    if (.not. c_associated(object)) return
    call LCMLEL(object,index,actual_length,actual_type)
    LIST_RECORD_MATCHES = actual_length == length .and. actual_type == type_code
  end function LIST_RECORD_MATCHES


  ! Full context comparison, including names, types, lengths, all directories,
  ! all list indices and raw stored words. Floating signed zero is preserved.
  ! No field subset, numeric tolerance, traversal-order assumption or repair.
  logical function SPOR64_BOOT64_SAME_TREE(left,right)
    type(c_ptr), intent(in) :: left, right
    integer :: nodes
    nodes = 0
    SPOR64_BOOT64_SAME_TREE = SAME_DIRECTORY(left,right,0,nodes)
  end function SPOR64_BOOT64_SAME_TREE

  recursive logical function SAME_DIRECTORY(left,right,depth,nodes) result(equal)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: depth
    integer, intent(inout) :: nodes
    character(len=72) :: file_name
    character(len=12) :: object_name, item_name, first_name
    integer :: left_extent, right_extent, count_left, count_right
    integer :: length_left, type_left, length_right, type_right
    logical :: left_empty, right_empty, medium
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    call LCMINF(left,file_name,object_name,left_empty,left_extent,medium)
    call LCMINF(right,file_name,object_name,right_empty,right_extent,medium)
    if (left_extent /= -1 .or. right_extent /= -1) return
    if (left_empty .neqv. right_empty) return
    if (left_empty) then
      equal = .true.
      return
    end if
    item_name = ' '
    call LCMNXT(left,item_name)
    first_name = item_name
    count_left = 0
    do
      nodes = nodes+1
      count_left = count_left+1
      if (nodes > MAX_NODES .or. item_name == ' ') return
      call LCMLEN(left,item_name,length_left,type_left)
      call LCMLEN(right,item_name,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        if (.not. SAME_DIRECTORY(child_left,child_right,depth+1,nodes)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        if (.not. SAME_LIST(child_left,child_right,length_left,depth+1,nodes)) return
      else
        if (.not. SAME_RECORD(left,right,item_name,0,length_left,type_left)) return
      end if
      call LCMNXT(left,item_name)
      if (item_name == first_name) exit
    end do
    item_name = ' '
    call LCMNXT(right,item_name)
    first_name = item_name
    count_right = 0
    do
      count_right = count_right+1
      if (count_right > MAX_NODES .or. item_name == ' ') return
      call LCMNXT(right,item_name)
      if (item_name == first_name) exit
    end do
    equal = count_left == count_right
  end function SAME_DIRECTORY

  recursive logical function SAME_LIST(left,right,extent,depth,nodes) result(equal)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: extent, depth
    integer, intent(inout) :: nodes
    integer :: index, length_left, type_left, length_right, type_right
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH .or. extent <= 0) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    do index = 1, extent
      nodes = nodes+1
      if (nodes > MAX_NODES) return
      call LCMLEL(left,index,length_left,type_left)
      call LCMLEL(right,index,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 99 .and. length_left == 0) cycle
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. SAME_DIRECTORY(child_left,child_right,depth+1,nodes)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. SAME_LIST(child_left,child_right,length_left,depth+1,nodes)) return
      else
        if (.not. SAME_RECORD(left,right,' ',index,length_left,type_left)) return
      end if
    end do
    equal = .true.
  end function SAME_LIST

  logical function SAME_RECORD(left,right,name,index,length,type_code)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: index, length, type_code
    integer(int64) :: words64
    integer :: words, allocation_status
    integer, allocatable :: left_bits(:), right_bits(:)
    SAME_RECORD = .false.
    if (length <= 0 .or. type_code < 1 .or. type_code > 6) return
    words64 = int(length,int64)
    if (type_code == 4 .or. type_code == 6) words64 = 2_int64*words64
    if (words64 > int(MAX_RECORD_WORDS,int64)) return
    words = int(words64)
    allocate(left_bits(words),right_bits(words),stat=allocation_status)
    if (allocation_status /= 0) return
    ! GANLIB's GET wrappers copy raw words without coercion. The allocated
    ! buffer is two int32 words per REAL64/complex value, one for other types.
    if (index == 0) then
      call LCMGET(left,name,left_bits)
      call LCMGET(right,name,right_bits)
    else
      call LCMGDL(left,index,left_bits)
      call LCMGDL(right,index,right_bits)
    end if
    SAME_RECORD = all(left_bits == right_bits)
  end function SAME_RECORD

end module SPOR64_BOOT64

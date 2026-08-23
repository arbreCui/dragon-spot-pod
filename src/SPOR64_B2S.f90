module SPOR64_B2S
  ! Drives the three radial solves of one step and hands the
  ! result to B2R.
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32
  use GANLIB
  use SPOR64_B2B, only : SPOR64_B2B_CONT, SPOR64_B2B_INGRESS
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED
  use SPOR64_B2O, only : SPOR64_B2O_SEALED, &
      SPOR64_B2O_SEAL_CONT_PAIR
  use SPOR64_B2R, only : SPOR64_B2R_RETURNED, SPOR64_B2R_COLLECT
  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT, LIST_ITEM_IS_DIRECTORY, &
      RECORD_MATCHES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2S_DISABLED = 0
  integer, parameter, public :: SPOR64_B2S_FAILED = 1
  integer, parameter, public :: SPOR64_B2S_RETURNED = 2

  integer, parameter :: NSNAP = 3
  integer, parameter :: NSTATE = 40
  integer, parameter :: NENTRY = 7
  integer, parameter :: NGRP = 370
  integer, parameter :: NIFIS = 32
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  integer, parameter :: kind_guard = 1 / merge(1,0,kind(1.0) == real32)

  public :: SPOR64_B2S_HOST_BRIDGE

contains

  subroutine SPOR64_B2S_HOST_BRIDGE(ipout,ipassembled,ipmacros, &
      ipsources,iptrack_file,status,cutoff_by_plane,enable)
    type(c_ptr), intent(in) :: ipout, ipassembled
    type(c_ptr), intent(in) :: ipmacros(NSNAP), ipsources(NSNAP)
    type(c_ptr), intent(in) :: iptrack_file
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_by_plane(NSNAP)
    logical, intent(in), optional :: enable

    character(len=12), parameter :: hentry(NENTRY) = &
        [character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
         'SYSTEM','FSOURCE','FLUX_OLD']
    integer :: ientry(NENTRY), jentry(NENTRY)
    integer, allocatable :: imerg(:)
    integer :: slot_for_plane(NSNAP), source_plane(NSNAP)
    integer :: plane, slot, seal_status, radial_status, collect_status
    integer :: nreg, nmat, nunkno, nsurf, plane_nsurf, allocation_status
    integer :: track_state(NSTATE)
    real(real32) :: frozen_tol32
    type(c_ptr) :: tracks, track
    type(c_ptr) :: sealed_seed(NSNAP), sealed_system(NSNAP)
    type(c_ptr) :: solved_by_plane(NSNAP), kentry(NENTRY)

    status = SPOR64_B2S_DISABLED
    cutoff_by_plane = 0_int64

    ! Execution routing is deliberately default-off.  The disabled call does
    ! not inspect an object, create scratch storage, or enter B2O/B2B/B2R.
    if (.not. present(enable)) return
    if (.not. enable) return
    status = SPOR64_B2S_FAILED

    ! The ABI accepts no loose plane, RHO, k, epoch, tolerance, relaxation,
    ! or caller-produced SOLVED object.  MACRO0 and FROZEN-QFIS are the two
    ! products supplied by the preceding B2N boundary; their sibling history
    ! is not independently encoded by the present object schemas.
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipassembled)) return
    if (.not. c_associated(iptrack_file)) return
    if (c_associated(ipout,ipassembled)) return
    do slot = 1, NSNAP
      if (.not. c_associated(ipmacros(slot))) return
      if (.not. c_associated(ipsources(slot))) return
      if (c_associated(ipout,ipmacros(slot))) return
      if (c_associated(ipout,ipsources(slot))) return
      if (c_associated(ipassembled,ipmacros(slot))) return
      if (c_associated(ipassembled,ipsources(slot))) return
    end do
    do slot = 1, NSNAP-1
      do plane = slot+1, NSNAP
        if (c_associated(ipsources(slot),ipsources(plane))) return
      end do
    end do
    do slot = 1, NSNAP
      do plane = 1, NSNAP
        if (c_associated(ipmacros(slot),ipsources(plane))) return
      end do
    end do
    if (.not. EMPTY_MEMORY_ROOT(ipout)) return

    ! The ASSEMBLED TRACK list is the sole geometry authority for this host
    ! bridge.  Establish one common runtime tuple before creating any private
    ! object or entering a radial solve.
    if (.not. RECORD_MATCHES(ipassembled,'TRACK',NSNAP,10)) return
    tracks = LCMGID(ipassembled,'TRACK')
    if (.not. c_associated(tracks)) return
    do plane = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,plane)) return
      track = LCMGIL(tracks,plane)
      if (.not. c_associated(track)) return
      if (.not. RECORD_MATCHES(track,'STATE-VECTOR',NSTATE,1)) return
      call LCMGET(track,'STATE-VECTOR',track_state)
      plane_nsurf = track_state(5)
      if (track_state(3) /= 1 .or. plane_nsurf <= 0) return
      if (track_state(6) /= 1) return
      if (plane == 1) then
        nreg = track_state(1)
        nunkno = track_state(2)
        nmat = track_state(4)
        nsurf = plane_nsurf
        if (nreg <= 0 .or. nunkno <= 0 .or. nmat <= 0) return
        if (int(nunkno,int64) /= &
            int(nreg,int64)+int(nsurf,int64)) return
      else
        if (track_state(1) /= nreg .or. track_state(2) /= nunkno) return
        if (track_state(4) /= nmat .or. plane_nsurf /= nsurf) return
      end if
      if (.not. RECORD_MATCHES(track,'V$MCCG',nunkno,2)) return
      if (.not. RECORD_MATCHES(track,'NZON$MCCG',nunkno,1)) return
      if (.not. RECORD_MATCHES(track,'KEYCUR$MCCG',nsurf,1)) return
      if (.not. RECORD_MATCHES(track,'MATCOD',nreg,1)) return
      if (.not. RECORD_MATCHES(track,'KEYFLX$ANIS',nreg,1)) return
    end do
    allocate(imerg(nmat),stat=allocation_status)
    if (allocation_status /= 0) return

    sealed_seed = c_null_ptr
    sealed_system = c_null_ptr
    solved_by_plane = c_null_ptr
    do slot = 1, NSNAP
      call OPEN_PRIVATE(sealed_seed(slot),'B2S-SEED',slot)
      call OPEN_PRIVATE(sealed_system(slot),'B2S-SYS',slot)
      call OPEN_PRIVATE(solved_by_plane(slot),'B2S-SOLV',slot)
    end do

    ! Seal all three tuples before the first radial call.  Duplicate or
    ! missing labels therefore fail without spending a transport solve.
    slot_for_plane = 0
    source_plane = 0
    do slot = 1, NSNAP
      call SPOR64_B2O_SEAL_CONT_PAIR(ipassembled,ipsources(slot), &
          sealed_seed(slot),sealed_system(slot),seal_status)
      if (seal_status /= SPOR64_B2O_SEALED) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if
      if (.not. READ_SEALED_PLANE(sealed_seed(slot),source_plane(slot))) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if
      plane = source_plane(slot)
      if (slot_for_plane(plane) /= 0) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if
      slot_for_plane(plane) = slot
    end do
    if (any(slot_for_plane == 0)) then
      call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
      return
    end if

    frozen_tol32 = transfer(FROZEN_TOL_BITS,0.0_real32)
    imerg = 1
    jentry = [0,2,2,2,2,2,2]

    ! Canonical plane order makes the three diagnostic cutoff counts
    ! unambiguous.  They are neither summed nor used in any acceptance rule.
    do plane = 1, NSNAP
      slot = slot_for_plane(plane)
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,plane)) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if
      track = LCMGIL(tracks,plane)
      if (.not. c_associated(track)) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if

      ientry = [1,LCM_STORAGE_KIND(ipmacros(slot)), &
          LCM_STORAGE_KIND(track),3,1,LCM_STORAGE_KIND(ipsources(slot)),1]
      kentry = [solved_by_plane(plane),ipmacros(slot),track, &
          iptrack_file,sealed_system(slot),ipsources(slot),sealed_seed(slot)]
      call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
          0,500,740,frozen_tol32,frozen_tol32,frozen_tol32,1,3,3, &
          'B0  ',0,1,1,imerg,0,.false.,0,.true.,NGRP,nreg,nmat, &
          NIFIS,1,2,1,.false.,.true.,SPOR64_B2B_CONT,radial_status, &
          cutoff_by_plane(plane))
      if (radial_status /= SPOR64_B2C_HOST_COMMITTED) then
        call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
        return
      end if
    end do

    ! The caller cannot substitute detached SOLVED objects: these three
    ! objects are still live from the immediately preceding B2B calls.
    call SPOR64_B2R_COLLECT(ipout,ipassembled,solved_by_plane, &
        ipsources,collect_status)
    if (collect_status == SPOR64_B2R_RETURNED) status = SPOR64_B2S_RETURNED
    call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)
  end subroutine SPOR64_B2S_HOST_BRIDGE


  subroutine OPEN_PRIVATE(stage,prefix,index)
    type(c_ptr), intent(out) :: stage
    character(len=*), intent(in) :: prefix
    integer, intent(in) :: index
    character(len=12) :: name

    write(name,'(A,I1)') trim(prefix),index
    call LCMOP(stage,name,0,1,0)
    if (.not. c_associated(stage)) &
      call XABORT('SPOR64_B2S: PRIVATE LCM CREATION FAILED.')
  end subroutine OPEN_PRIVATE


  subroutine CLOSE_PRIVATE(seeds,systems,solved)
    type(c_ptr), intent(inout) :: seeds(NSNAP), systems(NSNAP)
    type(c_ptr), intent(inout) :: solved(NSNAP)
    integer :: slot

    do slot = 1, NSNAP
      if (c_associated(solved(slot))) call LCMCL(solved(slot),2)
      if (c_associated(systems(slot))) call LCMCL(systems(slot),2)
      if (c_associated(seeds(slot))) call LCMCL(seeds(slot),2)
      solved(slot) = c_null_ptr
      systems(slot) = c_null_ptr
      seeds(slot) = c_null_ptr
    end do
  end subroutine CLOSE_PRIVATE


  logical function READ_SEALED_PLANE(seed,plane)
    type(c_ptr), intent(in) :: seed
    integer, intent(out) :: plane
    type(c_ptr) :: authority

    READ_SEALED_PLANE = .false.
    plane = 0
    if (.not. RECORD_MATCHES(seed,'SPOT-R64',-1,0)) return
    authority = LCMGID(seed,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. RECORD_MATCHES(authority,'PLANE',1,1)) return
    call LCMGET(authority,'PLANE',plane)
    if (plane < 1 .or. plane > NSNAP) return
    READ_SEALED_PLANE = .true.
  end function READ_SEALED_PLANE


  integer function LCM_STORAGE_KIND(owner)
    type(c_ptr), intent(in) :: owner
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call LCMINF(owner,object_file,object_name,empty,object_length,is_lcm)
    if (is_lcm) then
      LCM_STORAGE_KIND = 1
    else
      LCM_STORAGE_KIND = 2
    end if
  end function LCM_STORAGE_KIND
end module SPOR64_B2S

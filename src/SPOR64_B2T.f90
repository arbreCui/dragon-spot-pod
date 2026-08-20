module SPOR64_B2T
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use GANLIB
  use SPOR64_B2K, only : SPOR64_B2K_ARCHIVE_ASSEMBLED, &
      SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE
  use SPOR64_B2N, only : SPOR64_B2N_COMMITTED, SPOR64_B2N_BUILD
  use SPOR64_B2S, only : SPOR64_B2S_RETURNED, &
      SPOR64_B2S_HOST_BRIDGE
  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT
  implicit none
  private

  integer, parameter, public :: SPOR64_B2T_DISABLED = 0
  integer, parameter, public :: SPOR64_B2T_FAILED = 1
  integer, parameter, public :: SPOR64_B2T_RETURNED = 2

  integer, parameter :: NSNAP = 3

  public :: SPOR64_B2T_HOST_STEP

contains

  subroutine SPOR64_B2T_HOST_STEP(ipout,ipprojected,ipsystems, &
      iptrack_file,status,cutoff_by_plane,enable)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(NSNAP), iptrack_file
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_by_plane(NSNAP)
    logical, intent(in), optional :: enable

    integer :: plane, other, assemble_status, source_status, bridge_status
    type(c_ptr) :: assembled
    type(c_ptr) :: macros(NSNAP), sources(NSNAP)

    status = SPOR64_B2T_DISABLED
    cutoff_by_plane = 0_int64

    ! The complete ownership boundary is deliberately default-off.  The
    ! disabled call performs no association test, LCM access, scratch-object
    ! creation, B2K/B2N source build, or B2S radial bridge call.
    if (.not. present(enable)) return
    if (.not. enable) return
    status = SPOR64_B2T_FAILED

    ! One PROJECTED archive is the common parent of both the assembled
    ! operator archive and all three frozen-source pairs.  The public ABI has
    ! no detached ASSEMBLED, MACRO0, FSOURCE, SOLVED, plane, RHO, eigenvalue,
    ! epoch, tolerance, or relaxation input.
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipprojected)) return
    if (.not. c_associated(iptrack_file)) return
    if (c_associated(ipout,ipprojected)) return
    if (c_associated(ipout,iptrack_file)) return
    if (c_associated(ipprojected,iptrack_file)) return
    do plane = 1, NSNAP
      if (.not. c_associated(ipsystems(plane))) return
      if (c_associated(ipout,ipsystems(plane))) return
      if (c_associated(ipprojected,ipsystems(plane))) return
      if (c_associated(iptrack_file,ipsystems(plane))) return
    end do
    do plane = 1, NSNAP-1
      do other = plane+1, NSNAP
        if (c_associated(ipsystems(plane),ipsystems(other))) return
      end do
    end do
    if (.not. EMPTY_MEMORY_ROOT(ipout)) return

    assembled = c_null_ptr
    macros = c_null_ptr
    sources = c_null_ptr
    call OPEN_PRIVATE(assembled,'B2T-ASMB',0)
    do plane = 1, NSNAP
      call OPEN_PRIVATE(macros(plane),'B2T-MAC',plane)
      call OPEN_PRIVATE(sources(plane),'B2T-SRC',plane)
    end do

    ! B2K first binds the three supplied candidate SYSTEM objects to the one
    ! PROJECTED parent and creates a private ASSEMBLED archive.  Historical
    ! proof that the candidates came from same-call host ASM remains the
    ! responsibility of the future outer host boundary.
    call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(assembled,ipprojected, &
        ipsystems,assemble_status)
    if (assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) then
      call CLOSE_PRIVATE(assembled,macros,sources)
      return
    end if

    ! B2N owns both members of each pair.  All three pairs remain private and
    ! live until B2S consumes them; no caller can substitute a detached macro
    ! or source after the build.
    do plane = 1, NSNAP
      call SPOR64_B2N_BUILD(ipprojected,plane,macros(plane), &
          sources(plane),source_status)
      if (source_status /= SPOR64_B2N_COMMITTED) then
        call CLOSE_PRIVATE(assembled,macros,sources)
        return
      end if
    end do

    ! B2S performs B2O(3) -> B2B CONT(3) -> B2R(1).  TRACK_f remains an
    ! external file handle; its identity is deliberately an outer-host receipt
    ! concern and is not inferred from the symbolic LINK.FTRACK record.
    call SPOR64_B2S_HOST_BRIDGE(ipout,assembled,macros,sources, &
        iptrack_file,bridge_status,cutoff_by_plane,.true.)
    if (bridge_status == SPOR64_B2S_RETURNED) &
      status = SPOR64_B2T_RETURNED
    call CLOSE_PRIVATE(assembled,macros,sources)
  end subroutine SPOR64_B2T_HOST_STEP


  subroutine OPEN_PRIVATE(stage,prefix,index)
    type(c_ptr), intent(out) :: stage
    character(len=*), intent(in) :: prefix
    integer, intent(in) :: index
    character(len=12) :: name

    write(name,'(A,I1)') trim(prefix),index
    call LCMOP(stage,name,0,1,0)
    if (.not. c_associated(stage)) &
      call XABORT('SPOR64_B2T: PRIVATE LCM CREATION FAILED.')
  end subroutine OPEN_PRIVATE


  subroutine CLOSE_PRIVATE(assembled,macros,sources)
    type(c_ptr), intent(inout) :: assembled
    type(c_ptr), intent(inout) :: macros(NSNAP), sources(NSNAP)
    integer :: plane

    do plane = 1, NSNAP
      if (c_associated(sources(plane))) call LCMCL(sources(plane),2)
      if (c_associated(macros(plane))) call LCMCL(macros(plane),2)
      sources(plane) = c_null_ptr
      macros(plane) = c_null_ptr
    end do
    if (c_associated(assembled)) call LCMCL(assembled,2)
    assembled = c_null_ptr
  end subroutine CLOSE_PRIVATE
end module SPOR64_B2T

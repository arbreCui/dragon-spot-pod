module B2T_CONTENT_CAPTURE_PROBES
  implicit none
  private

  integer, parameter, public :: B2T_CONTENT_NSNAP = 3
  integer, parameter, public :: B2T_CONTENT_PATH_LENGTH = 1024
  integer, public, save :: b2t_content_b2k_calls = 0
  integer, public, save :: b2t_content_b2s_calls = 0
  integer, public, save :: b2t_content_evidence_writes = 0
  logical, public, save :: b2t_content_configured = .false.
  character(len=B2T_CONTENT_PATH_LENGTH), public, save :: &
      b2t_content_macro_paths(B2T_CONTENT_NSNAP) = ' '
  character(len=B2T_CONTENT_PATH_LENGTH), public, save :: &
      b2t_content_source_paths(B2T_CONTENT_NSNAP) = ' '

  public :: B2T_CONTENT_CONFIGURE

contains

  subroutine B2T_CONTENT_CONFIGURE(macro1,source1,macro2,source2, &
      macro3,source3)
    character(len=*), intent(in) :: macro1, source1, macro2, source2
    character(len=*), intent(in) :: macro3, source3

    if (len_trim(macro1) == 0 .or. len_trim(source1) == 0 .or. &
        len_trim(macro2) == 0 .or. len_trim(source2) == 0 .or. &
        len_trim(macro3) == 0 .or. len_trim(source3) == 0) &
      error stop 'B2T content evidence path is empty'
    if (max(len_trim(macro1),len_trim(source1),len_trim(macro2), &
        len_trim(source2),len_trim(macro3),len_trim(source3)) > &
        B2T_CONTENT_PATH_LENGTH) &
      error stop 'B2T content evidence path is too long'

    b2t_content_macro_paths = [character(len=B2T_CONTENT_PATH_LENGTH) :: &
        trim(macro1),trim(macro2),trim(macro3)]
    b2t_content_source_paths = [character(len=B2T_CONTENT_PATH_LENGTH) :: &
        trim(source1),trim(source2),trim(source3)]
    b2t_content_b2k_calls = 0
    b2t_content_b2s_calls = 0
    b2t_content_evidence_writes = 0
    b2t_content_configured = .true.
  end subroutine B2T_CONTENT_CONFIGURE

end module B2T_CONTENT_CAPTURE_PROBES


module SPOR64_B2K
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use B2T_CONTENT_CAPTURE_PROBES, only : B2T_CONTENT_NSNAP, &
      b2t_content_b2k_calls, b2t_content_configured
  implicit none
  private

  integer, parameter, public :: SPOR64_B2K_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2K_ARCHIVE_ASSEMBLED = 2

  public :: SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE

contains

  subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(ipout,ipprojected, &
      ipsystems,status)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(B2T_CONTENT_NSNAP)
    integer, intent(out) :: status

    integer :: marker, plane

    status = SPOR64_B2K_PREFLIGHT_FAILED
    if (.not. b2t_content_configured) return
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipprojected)) return
    do plane = 1, B2T_CONTENT_NSNAP
      if (.not. c_associated(ipsystems(plane))) return
    end do

    b2t_content_b2k_calls = b2t_content_b2k_calls + 1
    marker = 1
    call LCMPUT(ipout,'B2T-CONTENT',1,1,marker)
    status = SPOR64_B2K_ARCHIVE_ASSEMBLED
  end subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE

end module SPOR64_B2K


module SPOR64_B2S
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use B2T_CONTENT_CAPTURE_PROBES, only : B2T_CONTENT_NSNAP, &
      b2t_content_b2s_calls, b2t_content_configured, &
      b2t_content_evidence_writes, b2t_content_macro_paths, &
      b2t_content_source_paths
  implicit none
  private

  integer, parameter, public :: SPOR64_B2S_DISABLED = 0
  integer, parameter, public :: SPOR64_B2S_FAILED = 1
  integer, parameter, public :: SPOR64_B2S_RETURNED = 2

  public :: SPOR64_B2S_HOST_BRIDGE

contains

  subroutine SPOR64_B2S_HOST_BRIDGE(ipout,ipassembled,ipmacros, &
      ipsources,iptrack_file,status,cutoff_by_plane,enable)
    type(c_ptr), intent(in) :: ipout, ipassembled
    type(c_ptr), intent(in) :: ipmacros(B2T_CONTENT_NSNAP)
    type(c_ptr), intent(in) :: ipsources(B2T_CONTENT_NSNAP)
    type(c_ptr), intent(in) :: iptrack_file
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_by_plane(B2T_CONTENT_NSNAP)
    logical, intent(in), optional :: enable

    integer :: marker, plane

    status = SPOR64_B2S_DISABLED
    cutoff_by_plane = 0_int64
    if (.not. present(enable)) return
    if (.not. enable) return
    status = SPOR64_B2S_FAILED

    if (.not. b2t_content_configured) return
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipassembled)) return
    if (.not. c_associated(iptrack_file)) return
    call REQUIRE_RECORD(ipassembled,'B2T-CONTENT',1,1)
    call LCMGET(ipassembled,'B2T-CONTENT',marker)
    if (marker /= 1) return
    do plane = 1, B2T_CONTENT_NSNAP
      if (.not. c_associated(ipmacros(plane))) return
      if (.not. c_associated(ipsources(plane))) return
    end do

    b2t_content_b2s_calls = b2t_content_b2s_calls + 1
    do plane = 1, B2T_CONTENT_NSNAP
      call COPY_TO_NEW_XSM(ipmacros(plane), &
          trim(b2t_content_macro_paths(plane)))
      b2t_content_evidence_writes = b2t_content_evidence_writes + 1
      call COPY_TO_NEW_XSM(ipsources(plane), &
          trim(b2t_content_source_paths(plane)))
      b2t_content_evidence_writes = b2t_content_evidence_writes + 1
    end do
    status = SPOR64_B2S_RETURNED
  end subroutine SPOR64_B2S_HOST_BRIDGE


  subroutine COPY_TO_NEW_XSM(source,path)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: path

    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, exists, is_lcm
    type(c_ptr) :: evidence

    inquire(file=trim(path),exist=exists)
    if (exists) error stop 'B2T content evidence path already exists'
    call LCMOP(evidence,trim(path),0,2,0)
    if (.not. c_associated(evidence)) &
      error stop 'B2T content evidence creation failed'
    call LCMINF(evidence,object_file,object_name,empty,object_length,is_lcm)
    if (is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') &
      error stop 'B2T content evidence XSM is not fresh'
    call LCMEQU(source,evidence)
    call LCMCL(evidence,1)
  end subroutine COPY_TO_NEW_XSM


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
      error stop 'B2T content stub record schema differs'
  end subroutine REQUIRE_RECORD

end module SPOR64_B2S

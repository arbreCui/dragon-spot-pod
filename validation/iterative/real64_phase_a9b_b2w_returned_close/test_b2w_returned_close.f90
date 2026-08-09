program TEST_B2W_RETURNED_CLOSE
  use GANLIB
  use B2W_FIXTURE_SUPPORT
  use B2W_SPOLEAK_PROBES, only : RESET_SPOLEAK_PROBES, &
      redget_calls, redput_calls, returned_error_bits
  use SPOR64_B2W, only : SPOR64_B2W_CLOSE, &
      SPOR64_B2W_PREFLIGHT_FAILED, SPOR64_B2W_CLOSED
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  implicit none

  integer, parameter :: NREJECTION=25
  integer :: status, rejection_count
  character(len=1024) :: ax_input_path, feedback_input_path
  character(len=1024) :: ax_output_path, archive_output_path
  character(len=12) :: hentry(3)
  integer :: ientry(3), jentry(3)
  type(c_ptr) :: kentry(3), ax, feedback, axtrack
  type(c_ptr) :: axout, archiveout

  interface
    subroutine SPOLEAK(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOLEAK
  end interface

  if (command_argument_count() /= 4) error stop &
    'expected AX input, feedback input, closed AX, and closed archive paths'
  call get_command_argument(1,ax_input_path)
  call get_command_argument(2,feedback_input_path)
  call get_command_argument(3,ax_output_path)
  call get_command_argument(4,archive_output_path)
  call REQUIRE_FRESH_PATH(ax_input_path)
  call REQUIRE_FRESH_PATH(feedback_input_path)
  call REQUIRE_FRESH_PATH(ax_output_path)
  call REQUIRE_FRESH_PATH(archive_output_path)

  call BUILD_AX(ax)
  call BUILD_AX_TRACK(axtrack)
  call BUILD_FEEDBACK_BEFORE_SPOLEAK(feedback)

  hentry=[character(len=12) :: 'FEEDBACK','AX','AXTRACK']
  ientry=[1,1,1]
  jentry=[1,2,2]
  kentry=[feedback,ax,axtrack]
  call RESET_SPOLEAK_PROBES()
  call SPOLEAK(3,hentry,ientry,jentry,kentry)
  if (redget_calls /= 2 .or. redput_calls /= 1) &
    error stop 'real SPOLEAK parser-call inventory differs'
  if (returned_error_bits /= transfer(0.5_real32,0_int32)) &
    error stop 'real SPOLEAK returned error bits differ'

  call VERIFY_AX_INPUT(ax)
  call VERIFY_FEEDBACK_INPUT(feedback)
  rejection_count=0
  call RUN_REJECTION_SET(ax,feedback,rejection_count)
  if (rejection_count /= NREJECTION) &
    error stop 'B2W rejection inventory differs'
  call VERIFY_AX_INPUT(ax)
  call VERIFY_FEEDBACK_INPUT(feedback)

  call OPEN_FRESH('AX-OUTPUT',axout)
  call OPEN_FRESH('ARCHIVE-OUTPUT',archiveout)
  call SPOR64_B2W_CLOSE(axout,archiveout,ax,feedback,status)
  if (status /= SPOR64_B2W_CLOSED) &
    error stop 'canonical B2W close was rejected'
  call VERIFY_OUTPUTS(axout,archiveout,ax,feedback)
  call VERIFY_AX_INPUT(ax)
  call VERIFY_FEEDBACK_INPUT(feedback)

  call WRITE_XSM(ax,ax_input_path)
  call WRITE_XSM(feedback,feedback_input_path)
  call WRITE_XSM(axout,ax_output_path)
  call WRITE_XSM(archiveout,archive_output_path)

  call LCMCL(archiveout,2)
  call LCMCL(axout,2)
  call LCMCL(axtrack,2)
  call LCMCL(feedback,2)
  call LCMCL(ax,2)

  write(*,'(A)') 'B2W RETURNED-CLOSE SYNTHETIC PASS'
  write(*,'(A)') 'B2W REAL-SPOLEAK-CALLS=1 REDGET=2 REDPUT=1'
  write(*,'(A,I0,A,I0)') 'B2W CLOSES=1 REJECTIONS=',rejection_count, &
      ' ZERO-WRITE=',rejection_count
  write(*,'(A)') 'B2W RHO0-RETAINED=3 RHO1-ROOT=1 AX=CLOSED/1'
  write(*,'(A)') 'B2W ROOT-INPUT=EXACT9 ROOT-OUTPUT=EXACT8 L1ERR=DROPPED'
  write(*,'(A)') 'B2W DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0'

contains

  subroutine RUN_REJECTION_SET(input_ax,input_feedback,count)
    type(c_ptr), intent(in) :: input_ax, input_feedback
    integer, intent(inout) :: count
    integer :: offsets(NGRP+1), epoch, marker, ip
    real(real32) :: value32, values32(NUNK), leakage32(NGRP)
    real(real64) :: value64, leakage64(NGRP*NSNAP)
    type(c_ptr) :: bad_ax, bad_feedback, authority, fluxes, child
    type(c_ptr) :: payload, outer, inner, alias, other

    call CLONE_ROOT(input_ax,'BAD-AX-RHO',bad_ax)
    call LCMGET(bad_ax,'SPOT-X-RHO',value64)
    value64=nearest(value64,+1.0_real64)
    call LCMPUT(bad_ax,'SPOT-X-RHO',1,4,value64)
    call EXPECT_REJECTION(bad_ax,input_feedback,count)
    call LCMCL(bad_ax,2)

    call CLONE_ROOT(input_ax,'BAD-AX-LAYOUT',bad_ax)
    call LCMGET(bad_ax,'SPOT-X-OFF',offsets)
    offsets(2)=offsets(2)+1
    call LCMPUT(bad_ax,'SPOT-X-OFF',NGRP+1,1,offsets)
    call EXPECT_REJECTION(bad_ax,input_feedback,count)
    call LCMCL(bad_ax,2)

    call CLONE_ROOT(input_ax,'BAD-AX-NAN',bad_ax)
    value64=ieee_value(0.0_real64,ieee_quiet_nan)
    call LCMPUT(bad_ax,'SPOT-X-GERR',1,4,value64)
    call EXPECT_REJECTION(bad_ax,input_feedback,count)
    call LCMCL(bad_ax,2)

    call CLONE_ROOT(input_feedback,'BAD-ROOT-SCHEMA',bad_feedback)
    marker=7
    call LCMPUT(bad_feedback,'EXTRA',1,1,marker)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-ROOT-STATE',bad_feedback)
    authority=LCMGID(bad_feedback,'SPOT-R64')
    call PUT_CHARACTER(authority,'STATE',12,'CLOSED')
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-ROOT-EPOCH',bad_feedback)
    authority=LCMGID(bad_feedback,'SPOT-R64')
    epoch=2
    call LCMPUT(authority,'EPOCH',1,1,epoch)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-ROOT-K',bad_feedback)
    call LCMGET(bad_feedback,'SPOT-ITER-K',value64)
    value64=nearest(value64,+1.0_real64)
    call LCMPUT(bad_feedback,'SPOT-ITER-K',1,4,value64)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-LEAK',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,2)
    call LCMGET(child,'SPOT-LEAK1D',leakage32)
    leakage32(17)=nearest(leakage32(17),+1.0_real32)
    call LCMPUT(child,'SPOT-LEAK1D',NGRP,2,leakage32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-L1-NEG',bad_feedback)
    value32=-0.5_real32
    call LCMPUT(bad_feedback,'SPOT-L1-ERR',1,2,value32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-L1-NAN',bad_feedback)
    value32=ieee_value(0.0_real32,ieee_quiet_nan)
    call LCMPUT(bad_feedback,'SPOT-L1-ERR',1,2,value32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-L1-WRONG',bad_feedback)
    value32=nearest(0.5_real32,+1.0_real32)
    call LCMPUT(bad_feedback,'SPOT-L1-ERR',1,2,value32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-SYSTEM-L0',bad_feedback)
    fluxes=LCMGID(bad_feedback,'SYSTEM')
    child=LCMGIL(fluxes,1)
    call LCMGET(child,'SPOT-LEAK1D',leakage32)
    leakage32(1)=2.0_real32
    call LCMPUT(child,'SPOT-LEAK1D',NGRP,2,leakage32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-SYSTEM-RHO',bad_feedback)
    fluxes=LCMGID(bad_feedback,'SYSTEM')
    child=LCMGIL(fluxes,2)
    authority=LCMGID(child,'SPOT-R64')
    value64=nearest(RHO0_VALUE(),+1.0_real64)
    call LCMPUT(authority,'RHO',1,4,value64)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-CHILD-RHO',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,2)
    authority=LCMGID(child,'SPOT-R64')
    value64=nearest(RHO0_VALUE(),+1.0_real64)
    call LCMPUT(authority,'RHO',1,4,value64)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-CHILD-STATE',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,1)
    authority=LCMGID(child,'SPOT-R64')
    call PUT_CHARACTER(authority,'STATE',12,'RETURNED')
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-CHILD-EPOCH',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,3)
    authority=LCMGID(child,'SPOT-R64')
    call LCMPUT(authority,'EPOCH',1,1,2)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-QFISS',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,1)
    authority=LCMGID(child,'SPOT-R64')
    call LCMDEL(authority,'QFISS')
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-FLUX-MIRROR',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,2)
    payload=LCMGID(child,'FLUX')
    call LCMGDL(payload,1,values32)
    values32(1)=nearest(values32(1),+1.0_real32)
    call LCMPDL(payload,1,NUNK,2,values32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-PLANE',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,3)
    authority=LCMGID(child,'SPOT-R64')
    call LCMPUT(authority,'PLANE',1,1,3)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-FS-K-PLANE',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,2)
    value32=nearest(K0_VALUE(),+1.0_real32)
    call LCMPUT(child,'SPOT-FS-K',1,2,value32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-FS-K-RHO',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    value32=nearest(K0_VALUE(),+1.0_real32)
    do ip=1,NSNAP
      child=LCMGIL(fluxes,ip)
      call LCMPUT(child,'SPOT-FS-K',1,2,value32)
    end do
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_feedback,'BAD-Q-MIRROR',bad_feedback)
    fluxes=LCMGID(bad_feedback,'FLUX')
    child=LCMGIL(fluxes,3)
    outer=LCMGID(child,'SPOT-QFISS')
    inner=LCMGIL(outer,1)
    call LCMGDL(inner,1,values32)
    values32(2)=nearest(values32(2),+1.0_real32)
    call LCMPDL(inner,1,NUNK,2,values32)
    call EXPECT_REJECTION(input_ax,bad_feedback,count)
    call LCMCL(bad_feedback,2)

    call CLONE_ROOT(input_ax,'BAD-AX-LEAK-NAN',bad_ax)
    call LCMGET(bad_ax,'SPOT-X-L',leakage64)
    leakage64(1)=ieee_value(0.0_real64,ieee_quiet_nan)
    call LCMPUT(bad_ax,'SPOT-X-L',NGRP*NSNAP,4,leakage64)
    call EXPECT_REJECTION(bad_ax,input_feedback,count)
    call LCMCL(bad_ax,2)

    call OPEN_FRESH('ALIASED-OUTPUT',alias)
    call SPOR64_B2W_CLOSE(alias,alias,input_ax,input_feedback,status)
    if (status /= SPOR64_B2W_PREFLIGHT_FAILED .or. .not. EMPTY_ROOT(alias)) &
      error stop 'aliased output rejection wrote data'
    call LCMCL(alias,2)
    count=count+1

    call OPEN_FRESH('NONFRESH-AXOUT',alias)
    call OPEN_FRESH('NONFRESH-AROUT',other)
    marker=271828
    call LCMPUT(alias,'SENTINEL',1,1,marker)
    call SPOR64_B2W_CLOSE(alias,other,input_ax,input_feedback,status)
    if (status /= SPOR64_B2W_PREFLIGHT_FAILED) &
      error stop 'nonfresh output was accepted'
    call REQUIRE_ONLY_SENTINEL(alias,marker)
    if (.not. EMPTY_ROOT(other)) &
      error stop 'nonfresh rejection wrote its peer output'
    call LCMCL(other,2)
    call LCMCL(alias,2)
    count=count+1

    call VERIFY_AX_INPUT(input_ax)
    call VERIFY_FEEDBACK_INPUT(input_feedback)
  end subroutine RUN_REJECTION_SET


  subroutine EXPECT_REJECTION(input_ax,input_feedback,count)
    type(c_ptr), intent(in) :: input_ax, input_feedback
    integer, intent(inout) :: count
    integer :: local_status
    type(c_ptr) :: rejected_ax, rejected_archive

    call OPEN_FRESH('REJECTED-AX',rejected_ax)
    call OPEN_FRESH('REJECTED-ARCHIVE',rejected_archive)
    call SPOR64_B2W_CLOSE(rejected_ax,rejected_archive,input_ax, &
        input_feedback,local_status)
    if (local_status /= SPOR64_B2W_PREFLIGHT_FAILED) &
      error stop 'malformed B2W input was accepted'
    if (.not. EMPTY_ROOT(rejected_ax) .or. &
        .not. EMPTY_ROOT(rejected_archive)) &
      error stop 'rejected B2W call wrote an output'
    call LCMCL(rejected_archive,2)
    call LCMCL(rejected_ax,2)
    count=count+1
  end subroutine EXPECT_REJECTION


  subroutine VERIFY_OUTPUTS(output_ax,output_archive,input_ax,input_feedback)
    type(c_ptr), intent(in) :: output_ax, output_archive
    type(c_ptr), intent(in) :: input_ax, input_feedback
    character(len=12), parameter :: archive_names(8)=[ &
        character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
        'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
    character(len=12), parameter :: authority_names(4)=[ &
        character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
    integer :: ip, ig, marker, value
    real(real32) :: found32(NUNK), expected32(NUNK)
    real(real64) :: found64(NUNK), expected64(NUNK)
    type(c_ptr) :: stripped_ax, in_list, out_list, in_item, out_item
    type(c_ptr) :: in_deep, out_deep, authority, payload, outer, inner

    if (c_associated(output_ax,input_ax) .or. &
        c_associated(output_archive,input_feedback) .or. &
        c_associated(output_ax,output_archive)) &
      error stop 'successful B2W output aliases another root'
    call REQUIRE_CHARACTER(output_ax,'SPOT-X-STATE',12,'CLOSED')
    call REQUIRE_INTEGER(output_ax,'SPOT-X-EPOCH',1)
    call CLONE_ROOT(output_ax,'STRIPPED-AX',stripped_ax)
    call LCMDEL(stripped_ax,'SPOT-X-STATE')
    call LCMDEL(stripped_ax,'SPOT-X-EPOCH')
    call VERIFY_AX_INPUT(stripped_ax)
    call LCMCL(stripped_ax,2)
    in_list=LCMGID(input_ax,'FLUX')
    out_list=LCMGID(output_ax,'FLUX')
    if (c_associated(in_list,out_list)) &
      error stop 'closed AX FLUX list is not a deep copy'

    call REQUIRE_EXACT_INVENTORY(output_archive,archive_names, &
        'closed archive root')
    call REQUIRE_CHARACTER(output_archive,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_INTEGER(output_archive,'LISTDIM',NSNAP)
    call REQUIRE_REAL64_BITS(output_archive,'SPOT-ITER-K', &
        real(K1_VALUE(),real64))
    call REQUIRE_ABSENT(output_archive,'SPOT-L1-ERR')
    authority=LCMGID(output_archive,'SPOT-R64')
    call REQUIRE_EXACT_INVENTORY(authority,authority_names, &
        'closed archive authority')
    call REQUIRE_REAL64_BITS(authority,'RHO',RHO1_VALUE())
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER(authority,'STATE',12,'CLOSED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)

    call VERIFY_LIST_COPY(input_feedback,output_archive,'TRACK',1)
    call VERIFY_LIST_COPY(input_feedback,output_archive,'MICROLIB2',2)
    call VERIFY_LIST_COPY(input_feedback,output_archive,'SYSTEM',3)
    call VERIFY_LIST_COPY(input_feedback,output_archive,'FLUX',4)

    in_list=LCMGID(input_feedback,'FLUX')
    out_list=LCMGID(output_archive,'FLUX')
    do ip=1,NSNAP
      in_item=LCMGIL(in_list,ip)
      out_item=LCMGIL(out_list,ip)
      call REQUIRE_CHARACTER(out_item,'SIGNATURE',12,'L_FLUX')
      call REQUIRE_REAL32_BITS(out_item,'SPOT-FS-K',K0_VALUE())
      authority=LCMGID(out_item,'SPOT-R64')
      call REQUIRE_REAL64_BITS(authority,'RHO',RHO0_VALUE())
      call REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
      call REQUIRE_INTEGER(authority,'EPOCH',1)
      call REQUIRE_ABSENT(authority,'PLANE')
      payload=LCMGID(authority,'FLUX')
      do ig=1,NGRP
        call EXPECTED_VECTOR64(1,ip,ig,expected64)
        call LCMGDL(payload,ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          error stop 'closed archive authority FLUX differs'
        expected32=real(expected64,real32)
        call LCMGDL(LCMGID(out_item,'FLUX'),ig,found32)
        if (any(BITS32(found32) /= BITS32(expected32))) &
          error stop 'closed archive FLUX mirror differs'
        call EXPECTED_VECTOR64(2,ip,ig,expected64)
        call LCMGDL(LCMGID(authority,'SOUR'),ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          error stop 'closed archive authority SOUR differs'
        call EXPECTED_VECTOR64(3,ip,ig,expected64)
        call LCMGDL(LCMGID(authority,'QFISS'),ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          error stop 'closed archive authority QFISS differs'
        outer=LCMGID(out_item,'SPOT-QFISS')
        inner=LCMGIL(outer,1)
        call LCMGDL(inner,ig,found32)
        expected32=real(expected64,real32)
        if (any(BITS32(found32) /= BITS32(expected32))) &
          error stop 'closed archive QFISS mirror differs'
      end do
      if (c_associated(in_item,out_item)) &
        error stop 'closed FLUX child aliases feedback child'
    end do

    in_list=LCMGID(input_feedback,'TRACK')
    out_list=LCMGID(output_archive,'TRACK')
    do ip=1,NSNAP
      in_item=LCMGIL(in_list,ip)
      out_item=LCMGIL(out_list,ip)
      marker=1000+ip
      call REQUIRE_INTEGER(out_item,'B2W-ID',marker)
      in_deep=LCMGID(in_item,'B2W-DEEP')
      out_deep=LCMGID(out_item,'B2W-DEEP')
      if (c_associated(in_deep,out_deep)) &
        error stop 'nested TRACK directory aliases input'
      call LCMGET(out_deep,'VALUE',value)
      if (value /= marker) error stop 'nested TRACK value differs'
    end do
  end subroutine VERIFY_OUTPUTS


  subroutine VERIFY_LIST_COPY(input_root,output_root,name,kind_id)
    type(c_ptr), intent(in) :: input_root, output_root
    character(len=*), intent(in) :: name
    integer, intent(in) :: kind_id
    integer :: ip, ig, found, expected
    real(real32) :: input_leak(NGRP), output_leak(NGRP)
    type(c_ptr) :: input_list, output_list, input_item, output_item
    type(c_ptr) :: input_deep, output_deep, input_groups, output_groups
    type(c_ptr) :: input_group, output_group

    input_list=LCMGID(input_root,name)
    output_list=LCMGID(output_root,name)
    if (c_associated(input_list,output_list)) &
      error stop 'closed archive list aliases feedback list'
    do ip=1,NSNAP
      input_item=LCMGIL(input_list,ip)
      output_item=LCMGIL(output_list,ip)
      if (c_associated(input_item,output_item)) &
        error stop 'closed archive child aliases feedback child'
      select case(kind_id)
      case(1,2)
        input_deep=LCMGID(input_item,'B2W-DEEP')
        output_deep=LCMGID(output_item,'B2W-DEEP')
        if (c_associated(input_deep,output_deep)) &
          error stop 'closed archive nested directory aliases input'
        call LCMGET(input_deep,'VALUE',expected)
        call LCMGET(output_deep,'VALUE',found)
        if (found /= expected) error stop 'deep-copy sentinel differs'
      case(3)
        call LCMGET(input_item,'SPOT-LEAK1D',input_leak)
        call LCMGET(output_item,'SPOT-LEAK1D',output_leak)
        if (any(BITS32(input_leak) /= BITS32(output_leak))) &
          error stop 'SYSTEM copy differs'
        input_groups=LCMGID(input_item,'GROUP')
        output_groups=LCMGID(output_item,'GROUP')
        if (c_associated(input_groups,output_groups)) &
          error stop 'SYSTEM GROUP list aliases input'
        do ig=1,NGRP
          input_group=LCMGIL(input_groups,ig)
          output_group=LCMGIL(output_groups,ig)
          if (c_associated(input_group,output_group)) &
            error stop 'SYSTEM GROUP child aliases input'
          call LCMGET(input_group,'B2W-WITNESS',expected)
          call LCMGET(output_group,'B2W-WITNESS',found)
          if (found /= expected) error stop 'SYSTEM witness differs'
        end do
      case(4)
        continue
      case default
        error stop 'unknown four-list kind'
      end select
    end do
  end subroutine VERIFY_LIST_COPY


  subroutine REQUIRE_ONLY_SENTINEL(root,expected)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected
    character(len=12), parameter :: names(1)=[character(len=12) :: &
        'SENTINEL']

    call REQUIRE_EXACT_INVENTORY(root,names,'nonfresh output')
    call REQUIRE_INTEGER(root,'SENTINEL',expected)
  end subroutine REQUIRE_ONLY_SENTINEL


  subroutine REQUIRE_FRESH_PATH(path)
    character(len=*), intent(in) :: path
    logical :: exists
    inquire(file=trim(path),exist=exists)
    if (exists) error stop 'evidence path already exists'
  end subroutine REQUIRE_FRESH_PATH


  subroutine WRITE_XSM(source,path)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: path
    type(c_ptr) :: target

    call LCMOP(target,trim(path),0,2,0)
    if (.not. c_associated(target)) error stop 'XSM evidence create failed'
    call LCMEQU(source,target)
    call LCMCL(target,1)
  end subroutine WRITE_XSM

end program TEST_B2W_RETURNED_CLOSE

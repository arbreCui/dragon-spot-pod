module B2K_FIXTURE_SUPPORT
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_B2J, only : SPOR64_B2J_ARCHIVE_PROJECTED, &
      SPOR64_B2J_PROJECT_ARCHIVE
  use B2J_FIXTURE_SUPPORT
  implicit none
  private

  integer, parameter, public :: B2K_NACA=5
  integer, parameter, public :: B2K_NPJJ=7
  integer, parameter, public :: B2K_NGROUP_RECORDS=15
  integer, parameter, public :: B2K_NXS_FAMILIES=3
  integer, parameter, public :: B2K_NSYSMIX=B2J_NMAT+1
  integer, parameter, public :: B2K_RESTORED_XS_BITS = &
      B2J_NSNAP*B2J_NGRP*B2J_NMAT*3

  public :: B2K_BUILD_FRESH_SYSTEMS
  public :: B2K_CLOSE_SYSTEMS
  public :: B2K_PREPARE_PROJECTED_INPUT
  public :: B2K_REQUIRE_FORMULA_WITNESS
  public :: B2K_VERIFY_CANDIDATE_FORMULAS
  public :: B2K_VERIFY_POST_COMMIT_INDEPENDENCE
  public :: B2K_VERIFY_SYSTEM_DEEP_COPY

contains

  subroutine B2K_PREPARE_PROJECTED_INPUT(axial_base,archive_base, &
      axial_track_base,axial_closed,archive_closed,projected, &
      b2c_calls,b2i_calls,b2j_calls,restored_xs_bits)
    type(c_ptr), intent(in) :: axial_base, archive_base, axial_track_base
    type(c_ptr), intent(out) :: axial_closed, archive_closed, projected
    integer, intent(out) :: b2c_calls, b2i_calls, b2j_calls
    integer, intent(out) :: restored_xs_bits
    integer :: status

    call B2J_BUILD_CLOSED_PAIR(axial_base,archive_base,axial_track_base, &
        axial_closed,archive_closed,b2c_calls,b2i_calls)
    call RESTORE_REAL_MACROLIB_XS(archive_base,archive_closed, &
        restored_xs_bits)

    call LCMOP(projected,'B2K-PROJ',0,1,0)
    call B2J_REQUIRE_ASSOCIATED(projected,'B2k projected archive')
    call B2J_REQUIRE_EMPTY_ROOT(projected)
    b2j_calls=1
    call SPOR64_B2J_PROJECT_ARCHIVE(projected,axial_closed, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
      error stop 'production B2J rejected the restored real inputs'
    call B2J_REQUIRE_CHARACTER(LCMGID(projected,'SPOT-R64'), &
        'STATE',12,'PROJECTED')
  end subroutine B2K_PREPARE_PROJECTED_INPUT


  subroutine RESTORE_REAL_MACROLIB_XS(real_archive,closed_archive, &
      bit_checks)
    type(c_ptr), intent(in) :: real_archive, closed_archive
    integer, intent(out) :: bit_checks
    character(len=12), parameter :: names(3) = &
        [character(len=12) :: 'NTOT0','SIGW00','TRANC']
    integer :: ip, ig, ix
    real(real32) :: source32(B2J_NMAT), restored32(B2J_NMAT)
    type(c_ptr) :: real_libraries, closed_libraries
    type(c_ptr) :: real_library, closed_library
    type(c_ptr) :: real_macro, closed_macro
    type(c_ptr) :: real_groups, closed_groups
    type(c_ptr) :: real_group, closed_group

    real_libraries=LCMGID(real_archive,'MICROLIB2')
    closed_libraries=LCMGID(closed_archive,'MICROLIB2')
    call B2J_REQUIRE_ASSOCIATED(real_libraries,'real MICROLIB2 list')
    call B2J_REQUIRE_ASSOCIATED(closed_libraries,'closed MICROLIB2 list')
    bit_checks=0
    do ip=1,B2J_NSNAP
      call B2J_REQUIRE_DIRECTORY_ITEM(real_libraries,ip)
      call B2J_REQUIRE_DIRECTORY_ITEM(closed_libraries,ip)
      real_library=LCMGIL(real_libraries,ip)
      closed_library=LCMGIL(closed_libraries,ip)
      real_macro=LCMGID(real_library,'MACROLIB')
      closed_macro=LCMGID(closed_library,'MACROLIB')
      real_groups=LCMGID(real_macro,'GROUP')
      closed_groups=LCMGID(closed_macro,'GROUP')
      do ig=1,B2J_NGRP
        call B2J_REQUIRE_DIRECTORY_ITEM(real_groups,ig)
        call B2J_REQUIRE_DIRECTORY_ITEM(closed_groups,ig)
        real_group=LCMGIL(real_groups,ig)
        closed_group=LCMGIL(closed_groups,ig)
        do ix=1,size(names)
          call B2J_REQUIRE_RECORD(real_group,names(ix),B2J_NMAT,2)
          call LCMGET(real_group,names(ix),source32)
          if (.not. all(ieee_is_finite(source32))) &
            error stop 'real MACROLIB formula input is nonfinite'
          call LCMPUT(closed_group,names(ix),B2J_NMAT,2,source32)
          call LCMGET(closed_group,names(ix),restored32)
          if (any(B2J_BITS32(source32) /= B2J_BITS32(restored32))) &
            error stop 'restored MACROLIB formula bits differ'
          bit_checks=bit_checks+B2J_NMAT
        end do
      end do
    end do
    if (bit_checks /= B2K_RESTORED_XS_BITS) &
      error stop 'restored MACROLIB check inventory differs'
  end subroutine RESTORE_REAL_MACROLIB_XS


  subroutine B2K_BUILD_FRESH_SYSTEMS(projected,systems)
    type(c_ptr), intent(in) :: projected
    type(c_ptr), intent(out) :: systems(B2J_NSNAP)
    character(len=12) :: name
    integer :: ip

    call B2J_REQUIRE_CHARACTER(LCMGID(projected,'SPOT-R64'), &
        'STATE',12,'PROJECTED')
    call B2J_REQUIRE_ABSENT(projected,'SYSTEM')
    do ip=1,B2J_NSNAP
      write(name,'("B2K-SYS",I2.2)') ip
      call LCMOP(systems(ip),name,0,1,0)
      call B2J_REQUIRE_ASSOCIATED(systems(ip),'fresh SYSTEM candidate')
      call B2J_REQUIRE_EMPTY_ROOT(systems(ip))
      call BUILD_ONE_FRESH_SYSTEM(projected,systems(ip),ip)
    end do
  end subroutine B2K_BUILD_FRESH_SYSTEMS


  subroutine BUILD_ONE_FRESH_SYSTEM(projected,system,ip)
    type(c_ptr), intent(in) :: projected, system
    integer, intent(in) :: ip
    character(len=12) :: signature, link_macro, link_track
    integer :: state(B2J_NSTATE), ig
    real(real32) :: leakage32(B2J_NGRP)
    type(c_ptr) :: fluxes, plane, libraries, library, macro, macro_groups
    type(c_ptr) :: system_groups, macro_group, system_group

    signature='L_PIJ'
    link_macro='MACRO0'
    link_track='TRACK'
    state=0
    state([1,2,3,5,6,11])=1
    state(7)=4
    state(8)=B2J_NGRP
    state(9)=B2J_NUNKNO
    state(10)=B2J_NMAT

    fluxes=LCMGID(projected,'FLUX')
    call B2J_REQUIRE_DIRECTORY_ITEM(fluxes,ip)
    plane=LCMGIL(fluxes,ip)
    call B2J_REQUIRE_RECORD(plane,'SPOT-LEAK1D',B2J_NGRP,2)
    call LCMGET(plane,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) &
      error stop 'projected plane leakage is nonfinite'

    libraries=LCMGID(projected,'MICROLIB2')
    call B2J_REQUIRE_DIRECTORY_ITEM(libraries,ip)
    library=LCMGIL(libraries,ip)
    macro=LCMGID(library,'MACROLIB')
    macro_groups=LCMGID(macro,'GROUP')

    call LCMPTC(system,'SIGNATURE',12,signature)
    call LCMPTC(system,'LINK.MACRO',12,link_macro)
    call LCMPTC(system,'LINK.TRACK',12,link_track)
    call LCMPUT(system,'STATE-VECTOR',B2J_NSTATE,1,state)
    call LCMPUT(system,'SPOT-LEAK1D',B2J_NGRP,2,leakage32)
    call LCMPUT(system,'SPOT-L1-SNAP',1,1,ip)
    system_groups=LCMLID(system,'GROUP',B2J_NGRP)
    call B2J_REQUIRE_ASSOCIATED(system_groups,'fresh SYSTEM groups')
    do ig=1,B2J_NGRP
      call B2J_REQUIRE_DIRECTORY_ITEM(macro_groups,ig)
      macro_group=LCMGIL(macro_groups,ig)
      system_group=LCMDIL(system_groups,ig)
      call B2J_REQUIRE_ASSOCIATED(system_group,'fresh SYSTEM group')
      call BUILD_FRESH_GROUP(macro_group,system_group,leakage32(ig),ip,ig)
    end do

    call B2J_REQUIRE_ABSENT(system,'SPOT-R64')
    call B2J_REQUIRE_ABSENT(system,'B2I-SENT')
    call B2J_REQUIRE_ABSENT(system,'B2I-DEEP')
    call B2J_REQUIRE_EXACT_INVENTORY(system, &
        [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
         'STATE-VECTOR','SPOT-LEAK1D','SPOT-L1-SNAP','GROUP'])
  end subroutine BUILD_ONE_FRESH_SYSTEM


  subroutine BUILD_FRESH_GROUP(macro_group,system_group,leakage32,ip,ig)
    type(c_ptr), intent(in) :: macro_group, system_group
    real(real32), intent(in) :: leakage32
    integer, intent(in) :: ip, ig
    integer :: im
    real(real32) :: ntot0(B2J_NMAT), sigw00(B2J_NMAT)
    real(real32) :: tranc(B2J_NMAT)
    real(real32) :: txsc(0:B2J_NMAT), s0phys(0:B2J_NMAT)
    real(real32) :: s0used(0:B2J_NMAT)
    real(real32) :: r14(14), r32(32), r8(8)

    call B2J_REQUIRE_RECORD(macro_group,'NTOT0',B2J_NMAT,2)
    call B2J_REQUIRE_RECORD(macro_group,'SIGW00',B2J_NMAT,2)
    call B2J_REQUIRE_RECORD(macro_group,'TRANC',B2J_NMAT,2)
    call LCMGET(macro_group,'NTOT0',ntot0)
    call LCMGET(macro_group,'SIGW00',sigw00)
    call LCMGET(macro_group,'TRANC',tranc)
    if (.not. all(ieee_is_finite(ntot0)) .or. &
        .not. all(ieee_is_finite(sigw00)) .or. &
        .not. all(ieee_is_finite(tranc)) .or. &
        .not. ieee_is_finite(leakage32)) &
      error stop 'fresh SYSTEM formula input is nonfinite'

    txsc(0)=+0.0_real32
    s0phys(0)=+0.0_real32
    s0used(0)=s0phys(0)-leakage32
    do im=1,B2J_NMAT
      txsc(im)=ntot0(im)-tranc(im)
      s0phys(im)=sigw00(im)-tranc(im)
      s0used(im)=s0phys(im)-leakage32
    end do
    if (.not. all(ieee_is_finite(txsc)) .or. &
        .not. all(ieee_is_finite(s0phys)) .or. &
        .not. all(ieee_is_finite(s0used))) &
      error stop 'fresh SYSTEM formula result is nonfinite'

    call FILL_RESPONSE(r14,ip,ig,1)
    call LCMPUT(system_group,'DIAGF$MCCG',14,2,r14)
    call FILL_RESPONSE(r32,ip,ig,2)
    call LCMPUT(system_group,'CF$MCCG',32,2,r32)
    call FILL_RESPONSE(r14,ip,ig,3)
    call LCMPUT(system_group,'ILUDF$MCCG',14,2,r14)
    call FILL_RESPONSE(r32,ip,ig,4)
    call LCMPUT(system_group,'CQ$MCCG',32,2,r32)
    call FILL_RESPONSE(r14,ip,ig,5)
    call LCMPUT(system_group,'DIAGQ$MCCG',14,2,r14)
    call FILL_RESPONSE(r8,ip,ig,6)
    call LCMPUT(system_group,'PJJ$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,7)
    call LCMPUT(system_group,'PJJX$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,8)
    call LCMPUT(system_group,'PJJY$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,9)
    call LCMPUT(system_group,'PJJZ$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,10)
    call LCMPUT(system_group,'PJJXI$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,11)
    call LCMPUT(system_group,'PJJYI$MCCG',8,2,r8)
    call FILL_RESPONSE(r8,ip,ig,12)
    call LCMPUT(system_group,'PJJZI$MCCG',8,2,r8)
    call LCMPUT(system_group,'DRAGON-TXSC',B2K_NSYSMIX,2,txsc)
    call LCMPUT(system_group,'SPOT-S0-PHYS',B2K_NSYSMIX,2,s0phys)
    call LCMPUT(system_group,'DRAGON-S0XSC',B2K_NSYSMIX,2,s0used)
  end subroutine BUILD_FRESH_GROUP


  subroutine FILL_RESPONSE(values,ip,ig,family)
    real(real32), intent(out) :: values(:)
    integer, intent(in) :: ip, ig, family
    integer :: i

    do i=1,size(values)
      values(i)=real(ip,real32)+scale(real(ig,real32),-10)+ &
          scale(real(family,real32),-14)+scale(real(i,real32),-20)
    end do
  end subroutine FILL_RESPONSE


  subroutine B2K_VERIFY_CANDIDATE_FORMULAS(projected,systems, &
      leakage_checks,txsc_checks,s0phys_checks,s0used_checks)
    type(c_ptr), intent(in) :: projected
    type(c_ptr), intent(in) :: systems(B2J_NSNAP)
    integer, intent(out) :: leakage_checks, txsc_checks
    integer, intent(out) :: s0phys_checks, s0used_checks
    integer :: ip, ig, im, snapshot
    real(real32) :: plane_leak(B2J_NGRP), system_leak(B2J_NGRP)
    real(real32) :: ntot0(B2J_NMAT), sigw00(B2J_NMAT)
    real(real32) :: tranc(B2J_NMAT)
    real(real32) :: txsc(0:B2J_NMAT), s0phys(0:B2J_NMAT)
    real(real32) :: s0used(0:B2J_NMAT), expected32
    type(c_ptr) :: fluxes, plane, libraries, library, macro, macro_groups
    type(c_ptr) :: system_groups, macro_group, system_group

    leakage_checks=0
    txsc_checks=0
    s0phys_checks=0
    s0used_checks=0
    fluxes=LCMGID(projected,'FLUX')
    libraries=LCMGID(projected,'MICROLIB2')
    do ip=1,B2J_NSNAP
      plane=LCMGIL(fluxes,ip)
      call LCMGET(plane,'SPOT-LEAK1D',plane_leak)
      call B2J_REQUIRE_RECORD(systems(ip),'SPOT-LEAK1D',B2J_NGRP,2)
      call B2J_REQUIRE_RECORD(systems(ip),'SPOT-L1-SNAP',1,1)
      call LCMGET(systems(ip),'SPOT-LEAK1D',system_leak)
      call LCMGET(systems(ip),'SPOT-L1-SNAP',snapshot)
      if (snapshot /= ip) error stop 'fresh SYSTEM plane index differs'
      do ig=1,B2J_NGRP
        if (B2J_BITS32(system_leak(ig)) /= B2J_BITS32(plane_leak(ig))) &
          error stop 'fresh SYSTEM leakage bits differ'
        leakage_checks=leakage_checks+1
      end do

      library=LCMGIL(libraries,ip)
      macro=LCMGID(library,'MACROLIB')
      macro_groups=LCMGID(macro,'GROUP')
      system_groups=LCMGID(systems(ip),'GROUP')
      do ig=1,B2J_NGRP
        macro_group=LCMGIL(macro_groups,ig)
        system_group=LCMGIL(system_groups,ig)
        call LCMGET(macro_group,'NTOT0',ntot0)
        call LCMGET(macro_group,'SIGW00',sigw00)
        call LCMGET(macro_group,'TRANC',tranc)
        call LCMGET(system_group,'DRAGON-TXSC',txsc)
        call LCMGET(system_group,'SPOT-S0-PHYS',s0phys)
        call LCMGET(system_group,'DRAGON-S0XSC',s0used)

        expected32=+0.0_real32-plane_leak(ig)
        if (B2J_BITS32(txsc(0)) /= B2J_BITS32(+0.0_real32) .or. &
            B2J_BITS32(s0phys(0)) /= B2J_BITS32(+0.0_real32) .or. &
            B2J_BITS32(s0used(0)) /= B2J_BITS32(expected32)) &
          error stop 'fresh SYSTEM zero mixture slot differs'
        txsc_checks=txsc_checks+1
        s0phys_checks=s0phys_checks+1
        s0used_checks=s0used_checks+1
        do im=1,B2J_NMAT
          expected32=ntot0(im)-tranc(im)
          if (B2J_BITS32(txsc(im)) /= B2J_BITS32(expected32)) &
            error stop 'fresh SYSTEM TXSC formula bits differ'
          txsc_checks=txsc_checks+1
          expected32=sigw00(im)-tranc(im)
          if (B2J_BITS32(s0phys(im)) /= B2J_BITS32(expected32)) &
            error stop 'fresh SYSTEM S0PHYS formula bits differ'
          s0phys_checks=s0phys_checks+1
          expected32=expected32-plane_leak(ig)
          if (B2J_BITS32(s0used(im)) /= B2J_BITS32(expected32)) &
            error stop 'fresh SYSTEM S0USED formula bits differ'
          s0used_checks=s0used_checks+1
        end do
      end do
    end do
  end subroutine B2K_VERIFY_CANDIDATE_FORMULAS


  subroutine B2K_REQUIRE_FORMULA_WITNESS()
    real(real32), volatile :: x, y, z, first, ordered, grouped
    integer(int32) :: bits

    x=transfer(int(z'3d000000',int32),x)
    y=transfer(int(z'3c000000',int32),y)
    z=transfer(int(z'3c000001',int32),z)
    first=x-y
    ordered=first-z
    grouped=y+z
    grouped=x-grouped
    bits=transfer(ordered,bits)
    if (bits /= int(z'3c7fffff',int32)) &
      error stop 'ordered binary32 formula witness differs'
    bits=transfer(grouped,bits)
    if (bits /= int(z'3c800000',int32)) &
      error stop 'reassociated binary32 formula witness differs'
    if (B2J_BITS32(ordered) == B2J_BITS32(grouped)) &
      error stop 'binary32 formula witness does not discriminate order'
  end subroutine B2K_REQUIRE_FORMULA_WITNESS


  subroutine B2K_VERIFY_SYSTEM_DEEP_COPY(candidate,output,expected_plane, &
      response_bit_checks)
    type(c_ptr), intent(in) :: candidate, output
    integer, intent(in) :: expected_plane
    integer, intent(inout) :: response_bit_checks
    integer :: ig, snapshot
    type(c_ptr) :: input_groups, output_groups
    type(c_ptr) :: input_group, output_group

    call B2J_REQUIRE_DISTINCT(candidate,output,'complete SYSTEM root')
    call B2J_COMPARE_CHARACTER_RECORD(candidate,output,'SIGNATURE',12)
    call B2J_COMPARE_CHARACTER_RECORD(candidate,output,'LINK.MACRO',12)
    call B2J_COMPARE_CHARACTER_RECORD(candidate,output,'LINK.TRACK',12)
    call B2J_COMPARE_INTEGER_RECORD(candidate,output,'STATE-VECTOR')
    call B2J_COMPARE_REAL32_RECORD(candidate,output,'SPOT-LEAK1D')
    call B2J_COMPARE_INTEGER_RECORD(candidate,output,'SPOT-L1-SNAP')
    call LCMGET(output,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= expected_plane) &
      error stop 'deep-copied SYSTEM plane index differs'
    call B2J_REQUIRE_EXACT_INVENTORY(candidate, &
        [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
         'STATE-VECTOR','SPOT-LEAK1D','SPOT-L1-SNAP','GROUP'])
    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
         'STATE-VECTOR','SPOT-LEAK1D','SPOT-L1-SNAP','GROUP','SPOT-R64'])

    input_groups=LCMGID(candidate,'GROUP')
    output_groups=LCMGID(output,'GROUP')
    call B2J_REQUIRE_DISTINCT(input_groups,output_groups,'SYSTEM GROUP list')
    do ig=1,B2J_NGRP
      input_group=LCMGIL(input_groups,ig)
      output_group=LCMGIL(output_groups,ig)
      call B2J_REQUIRE_DISTINCT(input_group,output_group,'SYSTEM group')
      call COMPARE_GROUP_RECORDS(input_group,output_group,response_bit_checks)
    end do
  end subroutine B2K_VERIFY_SYSTEM_DEEP_COPY


  subroutine B2K_VERIFY_POST_COMMIT_INDEPENDENCE(candidate,output,witnesses)
    type(c_ptr), intent(in) :: candidate, output
    integer, intent(out) :: witnesses
    character(len=12), parameter :: names(15) = &
        [character(len=12) :: 'DIAGF$MCCG','CF$MCCG','ILUDF$MCCG', &
         'CQ$MCCG','DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
         'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG', &
         'DRAGON-TXSC','SPOT-S0-PHYS','DRAGON-S0XSC']
    integer :: i, length, record_type
    real(real32), allocatable :: original(:), changed(:), committed(:)
    type(c_ptr) :: candidate_group, output_group

    candidate_group=LCMGIL(LCMGID(candidate,'GROUP'),1)
    output_group=LCMGIL(LCMGID(output,'GROUP'),1)
    call B2J_REQUIRE_DISTINCT(candidate_group,output_group, &
        'post-commit SYSTEM group')
    witnesses=0
    do i=1,size(names)
      call LCMLEN(candidate_group,names(i),length,record_type)
      if (length < 1 .or. record_type /= 2) &
        error stop 'post-commit witness schema differs'
      allocate(original(length),changed(length),committed(length))
      call LCMGET(candidate_group,names(i),original)
      call LCMGET(output_group,names(i),committed)
      if (any(B2J_BITS32(original) /= B2J_BITS32(committed))) &
        error stop 'pre-mutation committed SYSTEM bits differ'
      changed=original
      changed(1)=nearest(changed(1),1.0_real32)
      call LCMPUT(candidate_group,names(i),length,2,changed)
      call LCMGET(output_group,names(i),committed)
      if (any(B2J_BITS32(original) /= B2J_BITS32(committed))) &
        error stop 'committed SYSTEM aliases candidate mutation'
      call LCMPUT(candidate_group,names(i),length,2,original)
      call LCMGET(candidate_group,names(i),changed)
      if (any(B2J_BITS32(original) /= B2J_BITS32(changed))) &
        error stop 'candidate witness restoration differs'
      witnesses=witnesses+1
      deallocate(original,changed,committed)
    end do
  end subroutine B2K_VERIFY_POST_COMMIT_INDEPENDENCE


  subroutine COMPARE_GROUP_RECORDS(input,output,response_bit_checks)
    type(c_ptr), intent(in) :: input, output
    integer, intent(inout) :: response_bit_checks
    character(len=12), parameter :: response_names(12) = &
        [character(len=12) :: 'DIAGF$MCCG','CF$MCCG','ILUDF$MCCG', &
         'CQ$MCCG','DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
         'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG']
    integer :: i, length, record_type

    call B2J_REQUIRE_EXACT_INVENTORY(input, &
        [character(len=12) :: response_names, 'DRAGON-TXSC', &
         'SPOT-S0-PHYS','DRAGON-S0XSC'])
    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: response_names, 'DRAGON-TXSC', &
         'SPOT-S0-PHYS','DRAGON-S0XSC'])
    do i=1,size(response_names)
      call LCMLEN(input,response_names(i),length,record_type)
      if (length < 1 .or. record_type /= 2) &
        error stop 'fresh response schema differs'
      call B2J_COMPARE_REAL32_RECORD(input,output,response_names(i))
      response_bit_checks=response_bit_checks+length
    end do
    call B2J_COMPARE_REAL32_RECORD(input,output,'DRAGON-TXSC')
    call B2J_COMPARE_REAL32_RECORD(input,output,'SPOT-S0-PHYS')
    call B2J_COMPARE_REAL32_RECORD(input,output,'DRAGON-S0XSC')
  end subroutine COMPARE_GROUP_RECORDS


  subroutine B2K_CLOSE_SYSTEMS(systems)
    type(c_ptr), intent(inout) :: systems(B2J_NSNAP)
    integer :: ip

    do ip=B2J_NSNAP,1,-1
      call LCMCL(systems(ip),2)
    end do
  end subroutine B2K_CLOSE_SYSTEMS

end module B2K_FIXTURE_SUPPORT

module SPOR64_B2O
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  implicit none
  private

  integer, parameter, public :: SPOR64_B2O_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2O_SEALED = 2

  integer, parameter :: NSNAP = 3
  integer, parameter :: NGRP = 370
  integer, parameter :: CONT_EPOCH = 1
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2O_SEAL_CONT_PAIR

contains

  subroutine SPOR64_B2O_SEAL_CONT_PAIR(ipassembled,ipsource, &
      ipseed_out,ipsystem_out,status)
    type(c_ptr), intent(in) :: ipassembled, ipsource
    type(c_ptr), intent(in) :: ipseed_out, ipsystem_out
    integer, intent(out) :: status

    integer :: nplane, root_epoch, source_epoch
    integer :: seed_epoch, system_epoch, system_plane
    integer(int64) :: expected64
    real(real32) :: seed_leakage32(NGRP), system_leakage32(NGRP)
    real(real64) :: iter_keff64, root_rho64, source_rho64
    real(real64) :: seed_rho64, system_rho64
    type(c_ptr) :: root_authority, source_authority
    type(c_ptr) :: fluxes, systems, input_seed, input_system
    type(c_ptr) :: seed_authority, system_authority
    type(c_ptr) :: output_seed_authority, output_system_authority

    status = SPOR64_B2O_PREFLIGHT_FAILED

    ! The committed source authority owns the archive-item plane.  This ABI
    ! accepts no independent caller plane, RHO, or epoch scalar.
    if (.not. c_associated(ipassembled)) return
    if (.not. c_associated(ipsource)) return
    if (.not. c_associated(ipseed_out)) return
    if (.not. c_associated(ipsystem_out)) return
    if (c_associated(ipassembled,ipsource)) return
    if (c_associated(ipassembled,ipseed_out)) return
    if (c_associated(ipassembled,ipsystem_out)) return
    if (c_associated(ipsource,ipseed_out)) return
    if (c_associated(ipsource,ipsystem_out)) return
    if (c_associated(ipseed_out,ipsystem_out)) return
    if (.not. EMPTY_LCM_ROOT(ipseed_out)) return
    if (.not. EMPTY_LCM_ROOT(ipsystem_out)) return

    if (.not. ASSEMBLED_ROOT_IS_EXACT(ipassembled)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipassembled,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipassembled,'LISTDIM',1,1)) return
    if (.not. RECORD_MATCHES(ipassembled,'SPOT-ITER-K',1,4)) return
    if (.not. RECORD_MATCHES(ipassembled,'SPOT-R64',-1,0)) return
    call LCMGET(ipassembled,'LISTDIM',nplane)
    call LCMGET(ipassembled,'SPOT-ITER-K',iter_keff64)
    if (nplane /= NSNAP) return
    if (.not. ieee_is_finite(iter_keff64)) return
    if (iter_keff64 <= +0.0_real64) return
    root_authority = LCMGID(ipassembled,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',root_rho64)
    call LCMGET(root_authority,'NPLANE',nplane)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(root_rho64)) return
    if (root_rho64 <= +0.0_real64) return
    if (nplane /= NSNAP) return
    if (root_epoch /= CONT_EPOCH) return
    expected64 = transfer(1.0_real64/iter_keff64,0_int64)
    if (transfer(root_rho64,0_int64) /= expected64) return

    if (.not. RECORD_MATCHES(ipsource,'SPOT-R64',-1,0)) return
    source_authority = LCMGID(ipsource,'SPOT-R64')
    if (.not. c_associated(source_authority)) return
    if (.not. SOURCE_AUTHORITY_IS_EXACT(source_authority)) return
    if (.not. RECORD_MATCHES(source_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(source_authority,'PLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(source_authority,'STATE',3,12, &
        'FROZEN-QFIS')) return
    if (.not. RECORD_MATCHES(source_authority,'QFISS',NGRP,10)) return
    if (.not. RECORD_MATCHES(source_authority,'EPOCH',1,1)) return
    call LCMGET(source_authority,'RHO',source_rho64)
    call LCMGET(source_authority,'PLANE',nplane)
    call LCMGET(source_authority,'EPOCH',source_epoch)
    if (.not. ieee_is_finite(source_rho64)) return
    if (source_rho64 <= +0.0_real64) return
    if (transfer(source_rho64,0_int64) /= &
        transfer(root_rho64,0_int64)) return
    if (nplane < 1 .or. nplane > NSNAP) return
    if (source_epoch /= root_epoch) return

    if (.not. RECORD_MATCHES(ipassembled,'FLUX',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipassembled,'SYSTEM',NSNAP,10)) return
    fluxes = LCMGID(ipassembled,'FLUX')
    systems = LCMGID(ipassembled,'SYSTEM')
    if (.not. c_associated(fluxes)) return
    if (.not. c_associated(systems)) return
    if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,nplane)) return
    if (.not. LIST_ITEM_IS_DIRECTORY(systems,nplane)) return
    input_seed = LCMGIL(fluxes,nplane)
    input_system = LCMGIL(systems,nplane)
    if (.not. c_associated(input_seed)) return
    if (.not. c_associated(input_system)) return

    if (.not. PROJECTED_SEED_ROOT_IS_EXACT(input_seed)) return
    if (.not. RECORD_MATCHES(input_seed,'SPOT-R64',-1,0)) return
    if (.not. RECORD_MATCHES(input_seed,'SPOT-LEAK1D',NGRP,2)) return
    seed_authority = LCMGID(input_seed,'SPOT-R64')
    if (.not. c_associated(seed_authority)) return
    if (.not. INPUT_SEED_AUTHORITY_IS_EXACT(seed_authority)) return
    if (.not. RECORD_MATCHES(seed_authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(seed_authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(seed_authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(seed_authority,'EPOCH',1,1)) return
    call LCMGET(seed_authority,'RHO',seed_rho64)
    call LCMGET(seed_authority,'EPOCH',seed_epoch)
    call LCMGET(input_seed,'SPOT-LEAK1D',seed_leakage32)
    if (.not. ieee_is_finite(seed_rho64)) return
    if (seed_rho64 <= +0.0_real64) return
    if (transfer(seed_rho64,0_int64) /= &
        transfer(root_rho64,0_int64)) return
    if (seed_epoch /= root_epoch) return
    if (.not. all(ieee_is_finite(seed_leakage32))) return

    if (.not. ASSEMBLED_SYSTEM_ROOT_IS_EXACT(input_system)) return
    if (.not. RECORD_MATCHES(input_system,'SPOT-R64',-1,0)) return
    if (.not. RECORD_MATCHES(input_system,'SPOT-L1-SNAP',1,1)) return
    if (.not. RECORD_MATCHES(input_system,'SPOT-LEAK1D',NGRP,2)) return
    system_authority = LCMGID(input_system,'SPOT-R64')
    if (.not. c_associated(system_authority)) return
    if (.not. SYSTEM_AUTHORITY_IS_EXACT(system_authority)) return
    if (.not. RECORD_MATCHES(system_authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(system_authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(system_authority,'EPOCH',1,1)) return
    call LCMGET(system_authority,'RHO',system_rho64)
    call LCMGET(system_authority,'EPOCH',system_epoch)
    call LCMGET(input_system,'SPOT-L1-SNAP',system_plane)
    call LCMGET(input_system,'SPOT-LEAK1D',system_leakage32)
    if (.not. ieee_is_finite(system_rho64)) return
    if (system_rho64 <= +0.0_real64) return
    if (transfer(system_rho64,0_int64) /= &
        transfer(root_rho64,0_int64)) return
    if (system_epoch /= root_epoch) return
    if (system_plane /= nplane) return
    if (.not. all(ieee_is_finite(system_leakage32))) return
    if (.not. SAME_REAL32_BITS(seed_leakage32,system_leakage32)) return

    ! Repeat freshness immediately before the first caller-visible mutation.
    if (.not. EMPTY_LCM_ROOT(ipseed_out)) return
    if (.not. EMPTY_LCM_ROOT(ipsystem_out)) return

    call LCMEQU(input_seed,ipseed_out)
    output_seed_authority = LCMGID(ipseed_out,'SPOT-R64')
    if (.not. c_associated(output_seed_authority)) &
        call XABORT('SPOR64_B2O: COPIED SEED AUTHORITY MISSING.')
    call LCMPUT(output_seed_authority,'PLANE',1,1,nplane)
    ! Rewriting EPOCH makes it the final seed-authority commit mutation.
    call LCMPUT(output_seed_authority,'EPOCH',1,1,root_epoch)

    call LCMEQU(input_system,ipsystem_out)
    output_system_authority = LCMGID(ipsystem_out,'SPOT-R64')
    if (.not. c_associated(output_system_authority)) &
        call XABORT('SPOR64_B2O: COPIED SYSTEM AUTHORITY MISSING.')
    ! Rewriting EPOCH makes it the final system-authority commit mutation.
    call LCMPUT(output_system_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_B2O_SEALED
  end subroutine SPOR64_B2O_SEAL_CONT_PAIR


  logical function EMPTY_LCM_ROOT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    EMPTY_LCM_ROOT = .false.
    if (.not. c_associated(iplist)) return
    call LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)
    EMPTY_LCM_ROOT = is_lcm .and. empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_LCM_ROOT


  logical function RECORD_MATCHES(iplist,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type

    RECORD_MATCHES = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    RECORD_MATCHES = actual_length == expected_length .and. &
        actual_type == expected_type
  end function RECORD_MATCHES


  logical function LIST_ITEM_IS_DIRECTORY(iplist,index)
    type(c_ptr), intent(in) :: iplist
    integer, intent(in) :: index
    integer :: actual_length, actual_type

    LIST_ITEM_IS_DIRECTORY = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEL(iplist,index,actual_length,actual_type)
    LIST_ITEM_IS_DIRECTORY = actual_length == -1 .and. actual_type == 0
  end function LIST_ITEM_IS_DIRECTORY


  logical function CHARACTER_RECORD_MATCHES(iplist,name,expected_words, &
      character_count,expected_value)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name, expected_value
    integer, intent(in) :: expected_words, character_count
    character(len=72) :: value

    CHARACTER_RECORD_MATCHES = .false.
    if (character_count < 1 .or. character_count > len(value)) return
    if (.not. RECORD_MATCHES(iplist,name,expected_words,3)) return
    value = ' '
    call LCMGTC(iplist,name,character_count,value)
    CHARACTER_RECORD_MATCHES = value(1:character_count) == expected_value
  end function CHARACTER_RECORD_MATCHES


  logical function SAME_REAL32_BITS(left,right)
    real(real32), intent(in) :: left(:), right(:)

    SAME_REAL32_BITS = size(left) == size(right)
    if (SAME_REAL32_BITS) SAME_REAL32_BITS = all( &
        transfer(left,0_int32,size(left)) == &
        transfer(right,0_int32,size(right)))
  end function SAME_REAL32_BITS


  logical function ASSEMBLED_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(8) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
         'MICROLIB2   ','SYSTEM      ','FLUX        ','SPOT-R64    ']
    ASSEMBLED_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function ASSEMBLED_ROOT_IS_EXACT


  logical function ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(4) = &
        ['RHO         ','NPLANE      ','STATE       ','EPOCH       ']
    ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function ROOT_AUTHORITY_IS_EXACT


  logical function SOURCE_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(5) = &
        ['RHO         ','PLANE       ','STATE       ','QFISS       ', &
         'EPOCH       ']
    SOURCE_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function SOURCE_AUTHORITY_IS_EXACT


  logical function PROJECTED_SEED_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(12) = &
        ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
         'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ']
    PROJECTED_SEED_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function PROJECTED_SEED_ROOT_IS_EXACT


  logical function INPUT_SEED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(4) = &
        ['RHO         ','FLUX        ','STATE       ','EPOCH       ']
    INPUT_SEED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function INPUT_SEED_AUTHORITY_IS_EXACT


  logical function ASSEMBLED_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(8) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-R64    ']
    ASSEMBLED_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function ASSEMBLED_SYSTEM_ROOT_IS_EXACT


  logical function SYSTEM_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(3) = &
        ['RHO         ','STATE       ','EPOCH       ']
    SYSTEM_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function SYSTEM_AUTHORITY_IS_EXACT


  logical function EXACT_INVENTORY(iplist,expected_names)
    type(c_ptr), intent(in) :: iplist
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, item_name
    integer :: count, i, allocation_status
    logical, allocatable :: found(:)

    EXACT_INVENTORY = .false.
    if (.not. c_associated(iplist)) return
    allocate(found(size(expected_names)),stat=allocation_status)
    if (allocation_status /= 0) return
    found = .false.
    item_name = ' '
    call LCMNXT(iplist,item_name)
    if (item_name == ' ') return
    first_name = item_name
    count = 0
    do
      count = count+1
      if (count > size(expected_names)) return
      do i = 1, size(expected_names)
        if (item_name == expected_names(i)) exit
      end do
      if (i > size(expected_names)) return
      if (found(i)) return
      found(i) = .true.
      call LCMNXT(iplist,item_name)
      if (item_name == first_name) exit
    end do
    EXACT_INVENTORY = count == size(expected_names) .and. all(found)
  end function EXACT_INVENTORY

end module SPOR64_B2O

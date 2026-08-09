program CHECK_B2W_RETURNED_CLOSE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NGRP=370, NSNAP=3, NUNK=14, NREG=8
  integer :: authority_checks, mirror_checks, deep_copies
  integer :: leakage_checks, system_group_checks
  character(len=1024) :: ax_input_path, feedback_path
  character(len=1024) :: ax_output_path, archive_path
  type(c_ptr) :: ax_input, feedback, ax_output, archive

  if (command_argument_count() /= 4) error stop &
    'expected AX input, feedback input, closed AX, and closed archive paths'
  call get_command_argument(1,ax_input_path)
  call get_command_argument(2,feedback_path)
  call get_command_argument(3,ax_output_path)
  call get_command_argument(4,archive_path)
  call OPEN_READ_ONLY(ax_input_path,ax_input)
  call OPEN_READ_ONLY(feedback_path,feedback)
  call OPEN_READ_ONLY(ax_output_path,ax_output)
  call OPEN_READ_ONLY(archive_path,archive)

  if (c_associated(ax_input,feedback) .or. &
      c_associated(ax_input,ax_output) .or. &
      c_associated(ax_input,archive) .or. &
      c_associated(feedback,ax_output) .or. &
      c_associated(feedback,archive) .or. &
      c_associated(ax_output,archive)) &
    error stop 'posterior roots are not distinct'

  authority_checks=0
  mirror_checks=0
  deep_copies=0
  leakage_checks=0
  system_group_checks=0
  call VERIFY_AX_PAIR(ax_input,ax_output)
  call VERIFY_ARCHIVE_PAIR(feedback,archive,ax_input)

  if (authority_checks /= 3*NSNAP*NGRP*NUNK) &
    error stop 'authority check inventory differs'
  if (mirror_checks /= 3*NSNAP*NGRP*NUNK) &
    error stop 'mirror check inventory differs'
  if (deep_copies /= 4*NSNAP) error stop 'deep-copy inventory differs'
  if (leakage_checks /= NSNAP*NGRP) &
    error stop 'leakage check inventory differs'
  if (system_group_checks /= NSNAP*NGRP) &
    error stop 'SYSTEM group inventory differs'

  call LCMCL(archive,1)
  call LCMCL(ax_output,1)
  call LCMCL(feedback,1)
  call LCMCL(ax_input,1)

  write(*,'(A)') 'B2W RETURNED-CLOSE POSTERIOR PASS'
  write(*,'(A)') 'B2W AX=UNSEALED->CLOSED/1 ARCHIVE=RETURNED/1->CLOSED/1'
  write(*,'(A,I0,A,I0)') 'B2W AUTHORITY64-BITS=',authority_checks, &
      ' MIRROR32-BITS=',mirror_checks
  write(*,'(A,I0,A,I0)') 'B2W LEAKAGE-PROMOTIONS=',leakage_checks, &
      ' SYSTEM-L0-GROUPS=',system_group_checks
  write(*,'(A,I0)') 'B2W FOUR-LIST-DEEP-COPIES=',deep_copies
  write(*,'(A)') 'B2W RHO0=RETAINED RHO1=RECIPROCAL K/L=BITWISE L1ERR=ABSENT'

contains

  subroutine VERIFY_AX_PAIR(input,output)
    type(c_ptr), intent(in) :: input, output
    integer :: ig, epoch
    real(real32) :: k32, in32(NUNK), out32(NUNK)
    real(real64) :: rho, input_leak(NGRP*NSNAP)
    real(real64) :: output_leak(NGRP*NSNAP)
    type(c_ptr) :: input_flux, output_flux

    call REQUIRE_CHARACTER(input,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_ABSENT(input,'SPOT-X-STATE')
    call REQUIRE_ABSENT(input,'SPOT-X-EPOCH')
    call REQUIRE_CHARACTER(output,'SPOT-X-STATE',12,'CLOSED')
    call REQUIRE_INTEGER(output,'SPOT-X-EPOCH',1)
    call LCMGET(output,'SPOT-X-EPOCH',epoch)
    if (epoch /= 1) error stop 'closed AX epoch differs'

    call COMPARE_CHARACTER(input,output,'SIGNATURE',12)
    call COMPARE_CHARACTER(input,output,'SPOT-X-NID',12)
    call COMPARE_CHARACTER(input,output,'SPOT-X-BTYP',12)
    call COMPARE_INTEGER(input,output,'STATE-VECTOR')
    call COMPARE_INTEGER(input,output,'SPOT-X-DIMS')
    call COMPARE_INTEGER(input,output,'SPOT-X-FIXB')
    call COMPARE_INTEGER(input,output,'SPOT-X-RANK')
    call COMPARE_INTEGER(input,output,'SPOT-X-OFF')
    call COMPARE_INTEGER(input,output,'SPOT-X-GOFF')
    call COMPARE_INTEGER(input,output,'SPOT-X-BOFF')
    call COMPARE_REAL32(input,output,'SPOT-X-BASIS')
    call COMPARE_REAL32(input,output,'K-EFFECTIVE')
    call COMPARE_REAL64(input,output,'SPOT-X-A')
    call COMPARE_REAL64(input,output,'SPOT-X-GRAM')
    call COMPARE_REAL64(input,output,'SPOT-X-RHO')
    call COMPARE_REAL64(input,output,'SPOT-X-L')
    call COMPARE_REAL64(input,output,'SPOT-X-H')
    call COMPARE_REAL64(input,output,'SPOT-X-NORM')
    call COMPARE_REAL64(input,output,'SPOT-X-PERP')
    call COMPARE_REAL64(input,output,'SPOT-X-GERR')

    call LCMGET(input,'K-EFFECTIVE',k32)
    call LCMGET(input,'SPOT-X-RHO',rho)
    if (.not. ieee_is_finite(k32) .or. .not. ieee_is_finite(rho)) &
      error stop 'AX K/RHO is nonfinite'
    if (BITS64(rho) /= BITS64(1.0_real64/real(k32,real64))) &
      error stop 'AX RHO reciprocal bits differ'
    call LCMGET(input,'SPOT-X-L',input_leak)
    call LCMGET(output,'SPOT-X-L',output_leak)
    if (any(BITS64(input_leak) /= BITS64(output_leak))) &
      error stop 'closed AX leakage bits differ'

    input_flux=LCMGID(input,'FLUX')
    output_flux=LCMGID(output,'FLUX')
    call REQUIRE_DISTINCT(input_flux,output_flux,'AX FLUX list')
    do ig=1,NGRP
      call LCMGDL(input_flux,ig,in32)
      call LCMGDL(output_flux,ig,out32)
      if (any(BITS32(in32) /= BITS32(out32))) &
        error stop 'closed AX ordinary FLUX differs'
    end do
  end subroutine VERIFY_AX_PAIR


  subroutine VERIFY_ARCHIVE_PAIR(input,output,ax)
    type(c_ptr), intent(in) :: input, output, ax
    character(len=12), parameter :: input_names(9)=[ &
        character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
        'SPOT-L1-ERR','TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
    character(len=12), parameter :: output_names(8)=[ &
        character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
        'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
    character(len=12), parameter :: returned_names(3)=[ &
        character(len=12) :: 'NPLANE','STATE','EPOCH']
    character(len=12), parameter :: closed_names(4)=[ &
        character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
    integer :: ip
    integer(int32) :: first_k_bits
    integer(int64) :: first_rho_bits
    real(real32) :: k32, l1err
    real(real64) :: iter_k, rho1
    type(c_ptr) :: input_authority, output_authority

    call REQUIRE_EXACT(input,input_names,'feedback root')
    call REQUIRE_EXACT(output,output_names,'closed archive root')
    call REQUIRE_CHARACTER(input,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_INTEGER(input,'LISTDIM',NSNAP)
    call REQUIRE_INTEGER(output,'LISTDIM',NSNAP)
    call COMPARE_REAL64(input,output,'SPOT-ITER-K')
    call REQUIRE_ABSENT(output,'SPOT-L1-ERR')
    call LCMGET(input,'SPOT-L1-ERR',l1err)
    if (.not. ieee_is_finite(l1err) .or. l1err < 0.0_real32) &
      error stop 'feedback L1 error is invalid'
    call VERIFY_L1_ERROR(input,l1err)
    call LCMGET(ax,'K-EFFECTIVE',k32)
    call LCMGET(input,'SPOT-ITER-K',iter_k)
    if (BITS64(iter_k) /= BITS64(real(k32,real64))) &
      error stop 'feedback/AX K bits differ'

    input_authority=LCMGID(input,'SPOT-R64')
    output_authority=LCMGID(output,'SPOT-R64')
    call REQUIRE_EXACT(input_authority,returned_names, &
        'returned root authority')
    call REQUIRE_EXACT(output_authority,closed_names, &
        'closed root authority')
    call REQUIRE_CHARACTER(input_authority,'STATE',12,'RETURNED')
    call REQUIRE_CHARACTER(output_authority,'STATE',12,'CLOSED')
    call REQUIRE_INTEGER(input_authority,'NPLANE',NSNAP)
    call REQUIRE_INTEGER(output_authority,'NPLANE',NSNAP)
    call REQUIRE_INTEGER(input_authority,'EPOCH',1)
    call REQUIRE_INTEGER(output_authority,'EPOCH',1)
    call REQUIRE_ABSENT(input_authority,'RHO')
    call LCMGET(output_authority,'RHO',rho1)
    if (BITS64(rho1) /= BITS64(1.0_real64/real(k32,real64))) &
      error stop 'closed root RHO reciprocal bits differ'

    call VERIFY_SIMPLE_LIST(input,output,'TRACK',1)
    call VERIFY_SIMPLE_LIST(input,output,'MICROLIB2',2)
    call VERIFY_SYSTEM_LIST(input,output)
    first_k_bits=0_int32
    first_rho_bits=0_int64
    do ip=1,NSNAP
      call VERIFY_FLUX_CHILD(input,output,ax,ip,rho1, &
          first_k_bits,first_rho_bits)
    end do
  end subroutine VERIFY_ARCHIVE_PAIR


  subroutine VERIFY_L1_ERROR(root,stored_error)
    type(c_ptr), intent(in) :: root
    real(real32), intent(in) :: stored_error
    integer :: ip
    real(real32) :: system_l0(NGRP), returned_l1(NGRP), recomputed
    type(c_ptr) :: systems, fluxes, system, flux

    systems=LCMGID(root,'SYSTEM')
    fluxes=LCMGID(root,'FLUX')
    recomputed=0.0_real32
    do ip=1,NSNAP
      system=LCMGIL(systems,ip)
      flux=LCMGIL(fluxes,ip)
      call LCMGET(system,'SPOT-LEAK1D',system_l0)
      call LCMGET(flux,'SPOT-LEAK1D',returned_l1)
      if (.not. all(ieee_is_finite(system_l0)) .or. &
          .not. all(ieee_is_finite(returned_l1))) &
        error stop 'L0/L1 leakage is nonfinite'
      recomputed=max(recomputed,maxval(abs(returned_l1-system_l0)))
    end do
    if (BITS32(recomputed) /= BITS32(stored_error)) &
      error stop 'SPOT-L1-ERR does not equal direct L1-L0 maximum'
  end subroutine VERIFY_L1_ERROR


  subroutine VERIFY_SIMPLE_LIST(input,output,name,kind_id)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer, intent(in) :: kind_id
    integer :: ip, expected, found, key_in(NREG), key_out(NREG)
    type(c_ptr) :: ilist, olist, ichild, ochild, ideep, odeep

    ilist=LCMGID(input,name)
    olist=LCMGID(output,name)
    call REQUIRE_DISTINCT(ilist,olist,trim(name)//' list')
    do ip=1,NSNAP
      ichild=LCMGIL(ilist,ip)
      ochild=LCMGIL(olist,ip)
      call REQUIRE_DISTINCT(ichild,ochild,trim(name)//' child')
      if (kind_id == 1) then
        call REQUIRE_CHARACTER(ochild,'SIGNATURE',12,'L_TRACK')
        call LCMGET(ichild,'KEYFLX',key_in)
        call LCMGET(ochild,'KEYFLX',key_out)
        if (any(key_in /= key_out)) error stop 'TRACK key copy differs'
        expected=1000+ip
      else
        call REQUIRE_CHARACTER(ochild,'SIGNATURE',12,'L_LIBRARY')
        expected=2000+ip
      end if
      call REQUIRE_INTEGER(ichild,'B2W-ID',expected)
      call REQUIRE_INTEGER(ochild,'B2W-ID',expected)
      ideep=LCMGID(ichild,'B2W-DEEP')
      odeep=LCMGID(ochild,'B2W-DEEP')
      call REQUIRE_DISTINCT(ideep,odeep,trim(name)//' nested directory')
      call LCMGET(odeep,'VALUE',found)
      if (found /= expected) error stop 'nested copy value differs'
      deep_copies=deep_copies+1
    end do
  end subroutine VERIFY_SIMPLE_LIST


  subroutine VERIFY_SYSTEM_LIST(input,output)
    type(c_ptr), intent(in) :: input, output
    integer :: ip, ig, input_witness, output_witness
    real(real32) :: input_leak(NGRP), output_leak(NGRP)
    type(c_ptr) :: ilist, olist, ichild, ochild
    type(c_ptr) :: igroups, ogroups, iitem, oitem

    ilist=LCMGID(input,'SYSTEM')
    olist=LCMGID(output,'SYSTEM')
    call REQUIRE_DISTINCT(ilist,olist,'SYSTEM list')
    do ip=1,NSNAP
      ichild=LCMGIL(ilist,ip)
      ochild=LCMGIL(olist,ip)
      call REQUIRE_DISTINCT(ichild,ochild,'SYSTEM child')
      call COMPARE_CHARACTER(ichild,ochild,'SIGNATURE',12)
      call COMPARE_CHARACTER(ichild,ochild,'LINK.MACRO',12)
      call COMPARE_CHARACTER(ichild,ochild,'LINK.TRACK',12)
      call COMPARE_INTEGER(ichild,ochild,'STATE-VECTOR')
      call COMPARE_INTEGER(ichild,ochild,'SPOT-L1-SNAP')
      call LCMGET(ichild,'SPOT-LEAK1D',input_leak)
      call LCMGET(ochild,'SPOT-LEAK1D',output_leak)
      if (any(BITS32(input_leak) /= BITS32(output_leak))) &
        error stop 'SYSTEM L0 copy differs'
      igroups=LCMGID(ichild,'GROUP')
      ogroups=LCMGID(ochild,'GROUP')
      call REQUIRE_DISTINCT(igroups,ogroups,'SYSTEM GROUP list')
      do ig=1,NGRP
        iitem=LCMGIL(igroups,ig)
        oitem=LCMGIL(ogroups,ig)
        call REQUIRE_DISTINCT(iitem,oitem,'SYSTEM GROUP child')
        call LCMGET(iitem,'B2W-WITNESS',input_witness)
        call LCMGET(oitem,'B2W-WITNESS',output_witness)
        if (input_witness /= output_witness) &
          error stop 'SYSTEM group witness differs'
        system_group_checks=system_group_checks+1
      end do
      deep_copies=deep_copies+1
    end do
  end subroutine VERIFY_SYSTEM_LIST


  subroutine VERIFY_FLUX_CHILD(input,output,ax,plane,rho1, &
      first_k_bits,first_rho_bits)
    type(c_ptr), intent(in) :: input, output, ax
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho1
    integer(int32), intent(inout) :: first_k_bits
    integer(int64), intent(inout) :: first_rho_bits
    character(len=12), parameter :: child_names(16)=[ &
        character(len=12) :: 'SPOT-R64','FLUX','SOUR','SIGNATURE', &
        'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
        'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D', &
        'SPOT-FS-EQN','SPOT-FS-K','SPOT-QFISS']
    character(len=12), parameter :: authority_names(6)=[ &
        character(len=12) :: 'RHO','FLUX','SOUR','QFISS','STATE','EPOCH']
    integer :: ig, field
    integer(int32) :: k_bits
    integer(int64) :: rho_bits
    real(real32) :: k0, input_leak(NGRP), output_leak(NGRP)
    real(real32) :: input32(NUNK), output32(NUNK), projected32(NUNK)
    real(real64) :: rho0, ax_leak(NGRP*NSNAP)
    real(real64) :: input64(NUNK), output64(NUNK)
    type(c_ptr) :: ilist, olist, ichild, ochild, iauth, oauth
    type(c_ptr) :: imirror, omirror, iauthority, oauthority
    type(c_ptr) :: iouter, oouter, iinner, oinner

    ilist=LCMGID(input,'FLUX')
    olist=LCMGID(output,'FLUX')
    ichild=LCMGIL(ilist,plane)
    ochild=LCMGIL(olist,plane)
    call REQUIRE_DISTINCT(ichild,ochild,'FLUX child')
    call REQUIRE_EXACT(ichild,child_names,'feedback FLUX child')
    call REQUIRE_EXACT(ochild,child_names,'closed FLUX child')
    call COMPARE_CHARACTER(ichild,ochild,'SIGNATURE',12)
    call COMPARE_CHARACTER(ichild,ochild,'OPTION',4)
    call COMPARE_CHARACTER(ichild,ochild,'LINK.MACRO',12)
    call COMPARE_CHARACTER(ichild,ochild,'LINK.TRACK',12)
    call COMPARE_CHARACTER(ichild,ochild,'LINK.SYSTEM',12)
    call COMPARE_INTEGER(ichild,ochild,'STATE-VECTOR')
    call COMPARE_INTEGER(ichild,ochild,'IMERGE-LEAK')
    call COMPARE_INTEGER(ichild,ochild,'KEYFLX')
    call COMPARE_INTEGER(ichild,ochild,'SPOT-FS-EQN')
    call COMPARE_REAL32(ichild,ochild,'EPS-CONVERGE')
    call COMPARE_REAL32(ichild,ochild,'SPOT-FS-K')
    call LCMGET(ichild,'SPOT-FS-K',k0)
    k_bits=BITS32(k0)
    call LCMGET(ichild,'SPOT-LEAK1D',input_leak)
    call LCMGET(ochild,'SPOT-LEAK1D',output_leak)
    if (any(BITS32(input_leak) /= BITS32(output_leak))) &
      error stop 'returned leakage copy differs'
    call LCMGET(ax,'SPOT-X-L',ax_leak)
    do ig=1,NGRP
      if (BITS64(ax_leak((plane-1)*NGRP+ig)) /= &
          BITS64(real(input_leak(ig),real64))) &
        error stop 'AX/feedback leakage promotion differs'
      leakage_checks=leakage_checks+1
    end do

    iauth=LCMGID(ichild,'SPOT-R64')
    oauth=LCMGID(ochild,'SPOT-R64')
    call REQUIRE_DISTINCT(iauth,oauth,'FLUX authority')
    call REQUIRE_EXACT(iauth,authority_names,'feedback child authority')
    call REQUIRE_EXACT(oauth,authority_names,'closed child authority')
    call REQUIRE_CHARACTER(iauth,'STATE',12,'SOLVED')
    call REQUIRE_CHARACTER(oauth,'STATE',12,'SOLVED')
    call REQUIRE_INTEGER(iauth,'EPOCH',1)
    call REQUIRE_INTEGER(oauth,'EPOCH',1)
    call REQUIRE_ABSENT(iauth,'PLANE')
    call REQUIRE_ABSENT(oauth,'PLANE')
    call LCMGET(iauth,'RHO',rho0)
    rho_bits=BITS64(rho0)
    if (rho_bits /= BITS64(1.0_real64/real(k0,real64))) &
      error stop 'child RHO reciprocal bits differ'
    if (rho_bits == BITS64(rho1)) error stop 'rho0 equals rho1'
    call REQUIRE_REAL64_BITS(oauth,'RHO',rho0)
    if (plane == 1) then
      first_k_bits=k_bits
      first_rho_bits=rho_bits
    else if (k_bits /= first_k_bits .or. rho_bits /= first_rho_bits) then
      error stop 'cross-plane K/RHO bits differ'
    end if

    do field=1,3
      select case(field)
      case(1)
        imirror=LCMGID(ichild,'FLUX')
        omirror=LCMGID(ochild,'FLUX')
        iauthority=LCMGID(iauth,'FLUX')
        oauthority=LCMGID(oauth,'FLUX')
      case(2)
        imirror=LCMGID(ichild,'SOUR')
        omirror=LCMGID(ochild,'SOUR')
        iauthority=LCMGID(iauth,'SOUR')
        oauthority=LCMGID(oauth,'SOUR')
      case(3)
        iouter=LCMGID(ichild,'SPOT-QFISS')
        oouter=LCMGID(ochild,'SPOT-QFISS')
        call REQUIRE_DISTINCT(iouter,oouter,'QFISS outer list')
        iinner=LCMGIL(iouter,1)
        oinner=LCMGIL(oouter,1)
        imirror=iinner
        omirror=oinner
        iauthority=LCMGID(iauth,'QFISS')
        oauthority=LCMGID(oauth,'QFISS')
      end select
      call REQUIRE_DISTINCT(imirror,omirror,'REAL32 mirror list')
      call REQUIRE_DISTINCT(iauthority,oauthority,'REAL64 authority list')
      do ig=1,NGRP
        call LCMGDL(imirror,ig,input32)
        call LCMGDL(omirror,ig,output32)
        call LCMGDL(iauthority,ig,input64)
        call LCMGDL(oauthority,ig,output64)
        if (any(BITS64(input64) /= BITS64(output64))) &
          error stop 'authority payload copy differs'
        authority_checks=authority_checks+NUNK
        if (any(BITS32(input32) /= BITS32(output32))) &
          error stop 'mirror payload copy differs'
        projected32=real(output64,real32)
        if (any(BITS32(output32) /= BITS32(projected32))) &
          error stop 'authority/mirror projection differs'
        mirror_checks=mirror_checks+NUNK
      end do
    end do
    deep_copies=deep_copies+1
  end subroutine VERIFY_FLUX_CHILD


  subroutine OPEN_READ_ONLY(path,root)
    character(len=*), intent(in) :: path
    type(c_ptr), intent(out) :: root
    call LCMOP(root,trim(path),2,2,0)
    if (.not. c_associated(root)) error stop 'read-only XSM open failed'
  end subroutine OPEN_READ_ONLY


  subroutine REQUIRE_DISTINCT(left,right,label)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: label
    if (.not. c_associated(left) .or. .not. c_associated(right)) &
      call FAIL(trim(label)//' is missing')
    if (c_associated(left,right)) call FAIL(trim(label)//' aliases input')
  end subroutine REQUIRE_DISTINCT


  subroutine REQUIRE_RECORD(root,name,length,record_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: length, record_type
    integer :: found_length, found_type
    call LCMLEN(root,name,found_length,found_type)
    if (found_length /= length .or. found_type /= record_type) &
      call FAIL(trim(name)//' schema differs')
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type
    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      call FAIL(trim(name)//' is unexpectedly present')
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_INTEGER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found
    call REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) call FAIL(trim(name)//' value differs')
  end subroutine REQUIRE_INTEGER


  subroutine REQUIRE_REAL64_BITS(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected
    real(real64) :: found
    call REQUIRE_RECORD(root,name,1,4)
    call LCMGET(root,name,found)
    if (BITS64(found) /= BITS64(expected)) &
      call FAIL(trim(name)//' REAL64 bits differ')
  end subroutine REQUIRE_REAL64_BITS


  subroutine REQUIRE_CHARACTER(root,name,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=72) :: found
    call REQUIRE_RECORD(root,name,(count+3)/4,3)
    found=' '
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= expected) &
      call FAIL(trim(name)//' character value differs')
  end subroutine REQUIRE_CHARACTER


  subroutine COMPARE_CHARACTER(input,output,name,count)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer, intent(in) :: count
    character(len=72) :: left, right
    call REQUIRE_RECORD(input,name,(count+3)/4,3)
    call REQUIRE_RECORD(output,name,(count+3)/4,3)
    left=' '
    right=' '
    call LCMGTC(input,name,count,left)
    call LCMGTC(output,name,count,right)
    if (left(1:count) /= right(1:count)) &
      call FAIL(trim(name)//' copied character differs')
  end subroutine COMPARE_CHARACTER


  subroutine COMPARE_INTEGER(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: ilen, itype, olen, otype
    integer, allocatable :: left(:), right(:)
    call LCMLEN(input,name,ilen,itype)
    call LCMLEN(output,name,olen,otype)
    if (ilen < 1 .or. itype /= 1 .or. olen /= ilen .or. otype /= 1) &
      call FAIL(trim(name)//' integer schema differs')
    allocate(left(ilen),right(ilen))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(left /= right)) call FAIL(trim(name)//' integer copy differs')
  end subroutine COMPARE_INTEGER


  subroutine COMPARE_REAL32(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: ilen, itype, olen, otype
    real(real32), allocatable :: left(:), right(:)
    call LCMLEN(input,name,ilen,itype)
    call LCMLEN(output,name,olen,otype)
    if (ilen < 1 .or. itype /= 2 .or. olen /= ilen .or. otype /= 2) &
      call FAIL(trim(name)//' REAL32 schema differs')
    allocate(left(ilen),right(ilen))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(BITS32(left) /= BITS32(right))) &
      call FAIL(trim(name)//' REAL32 copy differs')
  end subroutine COMPARE_REAL32


  subroutine COMPARE_REAL64(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: ilen, itype, olen, otype
    real(real64), allocatable :: left(:), right(:)
    call LCMLEN(input,name,ilen,itype)
    call LCMLEN(output,name,olen,otype)
    if (ilen < 1 .or. itype /= 4 .or. olen /= ilen .or. otype /= 4) &
      call FAIL(trim(name)//' REAL64 schema differs')
    allocate(left(ilen),right(ilen))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(BITS64(left) /= BITS64(right))) &
      call FAIL(trim(name)//' REAL64 copy differs')
  end subroutine COMPARE_REAL64


  subroutine REQUIRE_EXACT(root,names,label)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: names(:)
    character(len=*), intent(in) :: label
    character(len=72) :: object_file
    character(len=12) :: object_name, first_name, item_name
    integer :: object_length, count, i
    logical :: empty, memory_backed
    logical, allocatable :: seen(:)
    if (.not. c_associated(root)) call FAIL(trim(label)//' is missing')
    call LCMINF(root,object_file,object_name,empty,object_length, &
        memory_backed)
    if (empty .or. object_length /= -1) &
      call FAIL(trim(label)//' is empty or a list')
    allocate(seen(size(names)))
    seen=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    first_name=item_name
    count=0
    do
      count=count+1
      do i=1,size(names)
        if (item_name == names(i)) exit
      end do
      if (i > size(names) .or. count > size(names)) &
        call FAIL(trim(label)//' has an extra record')
      if (seen(i)) call FAIL(trim(label)//' has a duplicate record')
      seen(i)=.true.
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= size(names) .or. .not. all(seen)) &
      call FAIL(trim(label)//' inventory differs')
  end subroutine REQUIRE_EXACT


  subroutine FAIL(message)
    character(len=*), intent(in) :: message
    write(*,'(A)') 'B2W POSTERIOR FAILURE: '//trim(message)
    error stop 'B2W independent posterior failed'
  end subroutine FAIL


  elemental integer(int32) function BITS32(value)
    real(real32), intent(in) :: value
    BITS32=transfer(value,0_int32)
  end function BITS32


  elemental integer(int64) function BITS64(value)
    real(real64), intent(in) :: value
    BITS64=transfer(value,0_int64)
  end function BITS64

end program CHECK_B2W_RETURNED_CLOSE

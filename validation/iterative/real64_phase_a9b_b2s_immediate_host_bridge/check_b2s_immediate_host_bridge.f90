program CHECK_B2S_IMMEDIATE_HOST_BRIDGE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  implicit none

  integer, parameter :: NSNAP=3, NGRP=370, NUNK=14, NREG=8
  integer, parameter :: NSTATE=40, NMAT=8
  character(len=1024) :: output_path
  integer :: plane, r64_flux_bits, r64_source_bits, r64_qfiss_bits
  integer :: r32_flux_bits, r32_source_bits, r32_qfiss_bits
  integer :: track_copies, library_copies, system_copies
  integer :: child_plane_absences, terminal_witnesses
  integer :: key(NREG), reference_key(NREG)
  real(real32) :: leakage(NGRP), reference_leakage(NGRP)
  real(real64) :: k64, rho64
  type(c_ptr) :: output, authority, tracks, libraries, systems, fluxes

  if (command_argument_count() /= 1) &
    error stop 'expected one RETURNED XSM path'
  call get_command_argument(1,output_path)
  k64=nearest(1.0_real64,-1.0_real64)
  rho64=1.0_real64/k64

  call LCMOP(output,trim(output_path),2,2,0)
  call REQUIRE_ASSOCIATED(output,'RETURNED XSM')
  call REQUIRE_EXACT(output,[character(len=12) :: &
      'SIGNATURE','LISTDIM','TRACK','MICROLIB2','SYSTEM','FLUX', &
      'SPOT-R64'])
  call REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_ARCHIVE')
  call REQUIRE_INTEGER(output,'LISTDIM',NSNAP)
  call REQUIRE_ABSENT(output,'RHO')
  call REQUIRE_ABSENT(output,'SPOT-ITER-K')
  call REQUIRE_ABSENT(output,'AX_NEXT')
  call REQUIRE_ABSENT(output,'AX-NEXT')
  call REQUIRE_ABSENT(output,'CLOSED')

  authority=LCMGID(output,'SPOT-R64')
  call REQUIRE_ASSOCIATED(authority,'RETURNED root authority')
  call REQUIRE_EXACT(authority,[character(len=12) :: &
      'NPLANE','STATE','EPOCH'])
  call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
  call REQUIRE_CHARACTER(authority,'STATE',12,'RETURNED')
  call REQUIRE_INTEGER(authority,'EPOCH',1)
  call REQUIRE_ABSENT(authority,'RHO')
  call REQUIRE_ABSENT(authority,'SPOT-ITER-K')

  call REQUIRE_RECORD(output,'TRACK',NSNAP,10)
  call REQUIRE_RECORD(output,'MICROLIB2',NSNAP,10)
  call REQUIRE_RECORD(output,'SYSTEM',NSNAP,10)
  call REQUIRE_RECORD(output,'FLUX',NSNAP,10)
  tracks=LCMGID(output,'TRACK')
  libraries=LCMGID(output,'MICROLIB2')
  systems=LCMGID(output,'SYSTEM')
  fluxes=LCMGID(output,'FLUX')
  if (.not. all([c_associated(tracks),c_associated(libraries), &
      c_associated(systems),c_associated(fluxes)])) &
    error stop 'RETURNED archive list missing'

  r64_flux_bits=0
  r64_source_bits=0
  r64_qfiss_bits=0
  r32_flux_bits=0
  r32_source_bits=0
  r32_qfiss_bits=0
  track_copies=0
  library_copies=0
  system_copies=0
  child_plane_absences=0
  terminal_witnesses=0
  reference_key=0
  reference_leakage=0.0_real32
  do plane=1,NSNAP
    call REQUIRE_DIRECTORY_ITEM(tracks,plane)
    call REQUIRE_DIRECTORY_ITEM(libraries,plane)
    call REQUIRE_DIRECTORY_ITEM(systems,plane)
    call REQUIRE_DIRECTORY_ITEM(fluxes,plane)
    call VERIFY_TRACK(LCMGIL(tracks,plane),plane,key)
    if (plane == 1) then
      reference_key=key
    else if (any(key /= reference_key)) then
      error stop 'TRACK copies do not preserve one common KEYFLX payload'
    end if
    track_copies=track_copies+1
    call VERIFY_LIBRARY(LCMGIL(libraries,plane),plane)
    library_copies=library_copies+1
    call VERIFY_SYSTEM(LCMGIL(systems,plane),plane,rho64,leakage)
    if (plane == 1) then
      reference_leakage=leakage
    else if (any(transfer(leakage,0_int32,NGRP) /= &
        transfer(reference_leakage,0_int32,NGRP))) then
      error stop 'SYSTEM copies do not preserve one leakage payload'
    end if
    system_copies=system_copies+1
    call VERIFY_CHILD(LCMGIL(fluxes,plane),plane,k64,rho64,key, &
        leakage,r64_flux_bits,r64_source_bits,r64_qfiss_bits, &
        r32_flux_bits,r32_source_bits,r32_qfiss_bits, &
        child_plane_absences,terminal_witnesses)
  end do

  if (r64_flux_bits /= NSNAP*NGRP*NUNK .or. &
      r64_source_bits /= NSNAP*NGRP*NUNK .or. &
      r64_qfiss_bits /= NSNAP*NGRP*NUNK) &
    error stop 'REAL64 posterior inventory differs'
  if (r32_flux_bits /= NSNAP*NGRP*NUNK .or. &
      r32_source_bits /= NSNAP*NGRP*NUNK .or. &
      r32_qfiss_bits /= NSNAP*NGRP*NUNK) &
    error stop 'REAL32 posterior inventory differs'
  if (track_copies /= NSNAP .or. library_copies /= NSNAP .or. &
      system_copies /= NSNAP) &
    error stop 'same-index copy inventory differs'
  if (child_plane_absences /= NSNAP) &
    error stop 'archive child PLANE absence inventory differs'
  if (terminal_witnesses /= 2*NSNAP*NGRP*NUNK) &
    error stop 'terminal REAL64 witness inventory differs'

  call LCMCL(output,1)
  write(*,'(A)') 'B2S IMMEDIATE-HOST-BRIDGE POSTERIOR PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2S R64-FLUX-BITS=',r64_flux_bits, &
      ' R64-SOUR-BITS=',r64_source_bits,' R64-QFISS-BITS=',r64_qfiss_bits
  write(*,'(A,I0,A,I0,A,I0)') 'B2S R32-FLUX-BITS=',r32_flux_bits, &
      ' R32-SOUR-BITS=',r32_source_bits,' R32-QFISS-BITS=',r32_qfiss_bits
  write(*,'(A,I0,A,I0,A,I0)') 'B2S TRACK-COPIES=',track_copies, &
      ' MICROLIB2-COPIES=',library_copies,' SYSTEM-COPIES=',system_copies
  write(*,'(A,I0,A,I0)') 'B2S CHILD-PLANE-ABSENCES=', &
      child_plane_absences,' TERMINAL-LOWBIT-WITNESSES=',terminal_witnesses
  write(*,'(A)') 'B2S ROOT-RHO=ABSENT ROOT-K=ABSENT AX-NEXT=ABSENT CLOSED=ABSENT'

contains

  subroutine VERIFY_TRACK(track,plane,key)
    type(c_ptr), intent(in) :: track
    integer, intent(in) :: plane
    integer, intent(out) :: key(NREG)
    integer :: anis(NREG), i
    logical :: seen(NUNK)

    call REQUIRE_ASSOCIATED(track,'returned TRACK item')
    call REQUIRE_CHARACTER(track,'SIGNATURE',12,'L_TRACK')
    call REQUIRE_INTEGER(track,'B2S-PLANE',plane)
    call REQUIRE_RECORD(track,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
    call LCMGET(track,'KEYFLX',key)
    call LCMGET(track,'KEYFLX$ANIS',anis)
    if (any(key /= anis)) error stop 'returned TRACK key records differ'
    seen=.false.
    do i=1,NREG
      if (key(i) < 1 .or. key(i) > NUNK) &
        error stop 'returned TRACK key is outside the scalar unknowns'
      if (seen(key(i))) error stop 'returned TRACK key is duplicated'
      seen(key(i))=.true.
    end do
  end subroutine VERIFY_TRACK


  subroutine VERIFY_LIBRARY(library,plane)
    type(c_ptr), intent(in) :: library
    integer, intent(in) :: plane
    type(c_ptr) :: macrolib

    call REQUIRE_ASSOCIATED(library,'returned MICROLIB2 item')
    call REQUIRE_CHARACTER(library,'SIGNATURE',12,'L_LIBRARY')
    call REQUIRE_INTEGER(library,'B2S-PLANE',plane)
    call REQUIRE_RECORD(library,'MACROLIB',-1,0)
    macrolib=LCMGID(library,'MACROLIB')
    call REQUIRE_ASSOCIATED(macrolib,'returned MICROLIB2 MACROLIB')
    call REQUIRE_CHARACTER(macrolib,'SIGNATURE',12,'L_MACROLIB')
  end subroutine VERIFY_LIBRARY


  subroutine VERIFY_SYSTEM(system,plane,rho_value,leakage)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho_value
    real(real32), intent(out) :: leakage(NGRP)
    integer :: state(NSTATE), g
    real(real64) :: found_rho
    type(c_ptr) :: groups, group, system_authority

    call REQUIRE_ASSOCIATED(system,'returned SYSTEM item')
    call REQUIRE_EXACT(system,[character(len=12) :: &
        'SIGNATURE','LINK.MACRO','LINK.TRACK','STATE-VECTOR', &
        'SPOT-LEAK1D','SPOT-L1-SNAP','GROUP','SPOT-R64'])
    call REQUIRE_CHARACTER(system,'SIGNATURE',12,'L_PIJ')
    call REQUIRE_CHARACTER(system,'LINK.MACRO',12,'MACRO0')
    call REQUIRE_CHARACTER(system,'LINK.TRACK',12,'TRACK')
    call REQUIRE_INTEGER(system,'SPOT-L1-SNAP',plane)
    call REQUIRE_RECORD(system,'STATE-VECTOR',NSTATE,1)
    call LCMGET(system,'STATE-VECTOR',state)
    if (any(state(1:14) /= &
        [1,1,1,0,1,1,4,NGRP,NUNK,NMAT,1,0,0,0])) &
      error stop 'returned SYSTEM leading state differs'
    if (any(state(15:NSTATE) /= 0)) &
      error stop 'returned SYSTEM trailing state differs'
    call REQUIRE_RECORD(system,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(system,'SPOT-LEAK1D',leakage)
    call REQUIRE_RECORD(system,'GROUP',NGRP,10)
    groups=LCMGID(system,'GROUP')
    call REQUIRE_ASSOCIATED(groups,'returned SYSTEM GROUP list')
    do g=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(groups,g)
      group=LCMGIL(groups,g)
      call REQUIRE_ASSOCIATED(group,'returned SYSTEM GROUP item')
    end do
    system_authority=LCMGID(system,'SPOT-R64')
    call REQUIRE_ASSOCIATED(system_authority,'returned SYSTEM authority')
    call REQUIRE_EXACT(system_authority,[character(len=12) :: &
        'RHO','STATE','EPOCH'])
    call REQUIRE_CHARACTER(system_authority,'STATE',12,'ASSEMBLED')
    call REQUIRE_INTEGER(system_authority,'EPOCH',1)
    call REQUIRE_RECORD(system_authority,'RHO',1,4)
    call LCMGET(system_authority,'RHO',found_rho)
    if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
      error stop 'returned SYSTEM RHO differs'
  end subroutine VERIFY_SYSTEM


  subroutine VERIFY_CHILD(child,plane,k_value,rho_value,key,leakage, &
      n_r64_flux,n_r64_source,n_r64_qfiss,n_r32_flux,n_r32_source, &
      n_r32_qfiss,n_plane_absent,n_terminal_witness)
    type(c_ptr), intent(in) :: child
    integer, intent(in) :: plane, key(NREG)
    real(real64), intent(in) :: k_value, rho_value
    real(real32), intent(in) :: leakage(NGRP)
    integer, intent(inout) :: n_r64_flux, n_r64_source, n_r64_qfiss
    integer, intent(inout) :: n_r32_flux, n_r32_source, n_r32_qfiss
    integer, intent(inout) :: n_plane_absent, n_terminal_witness
    integer :: g, found_key(NREG), state(NSTATE), imerge(NMAT)
    integer(int32) :: eps_bits(5)
    real(real32) :: k32, found_k32, found_leakage(NGRP), eps(5)
    real(real32) :: found32(NUNK), expected32(NUNK)
    real(real64) :: found64(NUNK), expected64(NUNK), qfiss64(NUNK)
    real(real64) :: found_rho
    type(c_ptr) :: child_authority, aflux, asour, aqfiss
    type(c_ptr) :: mflux, msour, qouter, qinner

    call REQUIRE_ASSOCIATED(child,'returned SOLVED child')
    call REQUIRE_EXACT(child,[character(len=12) :: &
        'SPOT-R64','FLUX','SOUR','SIGNATURE','STATE-VECTOR', &
        'EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION','LINK.MACRO', &
        'LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D','SPOT-FS-EQN', &
        'SPOT-FS-K','SPOT-QFISS'])
    call REQUIRE_CHARACTER(child,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_CHARACTER(child,'OPTION',4,'B0  ')
    call REQUIRE_CHARACTER(child,'LINK.MACRO',12,'MACRO0')
    call REQUIRE_CHARACTER(child,'LINK.TRACK',12,'TRACK')
    call REQUIRE_CHARACTER(child,'LINK.SYSTEM',12,'SYSTEM')
    call REQUIRE_RECORD(child,'STATE-VECTOR',NSTATE,1)
    call LCMGET(child,'STATE-VECTOR',state)
    if (any(state(1:18) /= &
        [NGRP,NUNK,1,0,0,0,0,3,3,1,740,500,0,0,0,0,NMAT,1])) &
      error stop 'returned SOLVED leading state differs'
    if (any(state(19:NSTATE) /= 0)) &
      error stop 'returned SOLVED trailing state differs'
    call REQUIRE_RECORD(child,'EPS-CONVERGE',5,2)
    call LCMGET(child,'EPS-CONVERGE',eps)
    eps_bits=transfer(eps,0_int32,5)
    if (any(eps_bits(1:3) /= int(z'348637bd',int32)) .or. &
        any(eps_bits(4:5) /= 0_int32)) &
      error stop 'returned SOLVED tolerance bits differ'
    call REQUIRE_RECORD(child,'IMERGE-LEAK',NMAT,1)
    call LCMGET(child,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) error stop 'returned SOLVED merge map differs'
    call REQUIRE_RECORD(child,'KEYFLX',NREG,1)
    call LCMGET(child,'KEYFLX',found_key)
    if (any(found_key /= key)) &
      error stop 'returned SOLVED key is not bound to its TRACK index'
    call REQUIRE_RECORD(child,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(child,'SPOT-LEAK1D',found_leakage)
    if (any(transfer(found_leakage,0_int32,NGRP) /= &
        transfer(leakage,0_int32,NGRP))) &
      error stop 'returned SOLVED leakage is not bound to its SYSTEM index'

    child_authority=LCMGID(child,'SPOT-R64')
    call REQUIRE_ASSOCIATED(child_authority,'returned child authority')
    call REQUIRE_EXACT(child_authority,[character(len=12) :: &
        'RHO','FLUX','SOUR','QFISS','STATE','EPOCH'])
    call REQUIRE_ABSENT(child_authority,'PLANE')
    n_plane_absent=n_plane_absent+1
    call REQUIRE_CHARACTER(child_authority,'STATE',12,'SOLVED')
    call REQUIRE_INTEGER(child_authority,'EPOCH',1)
    call REQUIRE_RECORD(child_authority,'RHO',1,4)
    call LCMGET(child_authority,'RHO',found_rho)
    if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
      error stop 'returned child inherited RHO differs'

    call REQUIRE_INTEGER(child,'SPOT-FS-EQN',1)
    call REQUIRE_RECORD(child,'SPOT-FS-K',1,2)
    call LCMGET(child,'SPOT-FS-K',found_k32)
    k32=real(k_value,real32)
    if (transfer(found_k32,0_int32) /= transfer(k32,0_int32)) &
      error stop 'returned child fixed-source K differs'
    call REQUIRE_RECORD(child,'SPOT-QFISS',1,10)
    qouter=LCMGID(child,'SPOT-QFISS')
    call REQUIRE_ASSOCIATED(qouter,'returned SPOT-QFISS outer')
    call REQUIRE_LIST_ELEMENT(qouter,1,NGRP,10)
    qinner=LCMGIL(qouter,1)
    call REQUIRE_ASSOCIATED(qinner,'returned SPOT-QFISS inner')

    call REQUIRE_RECORD(child_authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(child_authority,'SOUR',NGRP,10)
    call REQUIRE_RECORD(child_authority,'QFISS',NGRP,10)
    call REQUIRE_RECORD(child,'FLUX',NGRP,10)
    call REQUIRE_RECORD(child,'SOUR',NGRP,10)
    aflux=LCMGID(child_authority,'FLUX')
    asour=LCMGID(child_authority,'SOUR')
    aqfiss=LCMGID(child_authority,'QFISS')
    mflux=LCMGID(child,'FLUX')
    msour=LCMGID(child,'SOUR')
    do g=1,NGRP
      call REQUIRE_LIST_ELEMENT(aflux,g,NUNK,4)
      call EXPECTED_VECTOR64(1,plane,g,expected64)
      call LCMGDL(aflux,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(expected64,0_int64,NUNK))) &
        error stop 'returned type-4 terminal FLUX bits differ'
      n_r64_flux=n_r64_flux+NUNK
      expected32=real(expected64,real32)
      if (any(transfer(expected64,0_int64,NUNK) == transfer( &
          real(expected32,real64),0_int64,NUNK))) &
        error stop 'terminal FLUX oracle lacks REAL64-only bits'
      n_terminal_witness=n_terminal_witness+NUNK
      call REQUIRE_LIST_ELEMENT(mflux,g,NUNK,2)
      call LCMGDL(mflux,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'returned type-2 terminal FLUX bits differ'
      n_r32_flux=n_r32_flux+NUNK

      call REQUIRE_LIST_ELEMENT(asour,g,NUNK,4)
      call EXPECTED_VECTOR64(2,plane,g,expected64)
      call LCMGDL(asour,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(expected64,0_int64,NUNK))) &
        error stop 'returned type-4 terminal SOUR bits differ'
      n_r64_source=n_r64_source+NUNK
      expected32=real(expected64,real32)
      if (any(transfer(expected64,0_int64,NUNK) == transfer( &
          real(expected32,real64),0_int64,NUNK))) &
        error stop 'terminal SOUR oracle lacks REAL64-only bits'
      n_terminal_witness=n_terminal_witness+NUNK
      call REQUIRE_LIST_ELEMENT(msour,g,NUNK,2)
      call LCMGDL(msour,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'returned type-2 terminal SOUR bits differ'
      n_r32_source=n_r32_source+NUNK

      call REQUIRE_LIST_ELEMENT(aqfiss,g,NUNK,4)
      call EXPECTED_VECTOR64(3,plane,g,qfiss64)
      call LCMGDL(aqfiss,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(qfiss64,0_int64,NUNK))) &
        error stop 'returned label-bound type-4 QFISS bits differ'
      n_r64_qfiss=n_r64_qfiss+NUNK
      expected32=real(qfiss64,real32)
      call REQUIRE_LIST_ELEMENT(qinner,g,NUNK,2)
      call LCMGDL(qinner,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'returned label-bound type-2 QFISS bits differ'
      n_r32_qfiss=n_r32_qfiss+NUNK
    end do
  end subroutine VERIFY_CHILD


  subroutine EXPECTED_VECTOR64(field,plane,group,values)
    integer, intent(in) :: field, plane, group
    real(real64), intent(out) :: values(NUNK)
    integer :: i
    real(real64) :: base

    do i=1,NUNK
      select case(field)
      case(1)
        base=16384.0_real64+1024.0_real64*real(plane,real64)+ &
            real(31*group+i,real64)/16.0_real64
      case(2)
        base=32768.0_real64+2048.0_real64*real(plane,real64)+ &
            real(37*group+3*i,real64)/16.0_real64
      case(3)
        base=4096.0_real64+256.0_real64*real(plane,real64)+ &
            2.0_real64*real(group,real64)+real(i,real64)/16.0_real64
      case default
        error stop 'unknown posterior field'
      end select
      values(i)=base+real(plane,real64)*spacing(base)
    end do
  end subroutine EXPECTED_VECTOR64


  subroutine REQUIRE_ASSOCIATED(ptr,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: label
    if (.not. c_associated(ptr)) call FAIL(trim(label)//' missing')
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type
    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= expected_length .or. actual_type /= expected_type) &
      call FAIL(trim(name)//' schema differs')
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_LIST_ELEMENT(list,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index, expected_length, expected_type
    integer :: actual_length, actual_type
    call LCMLEL(list,index,actual_length,actual_type)
    if (actual_length /= expected_length .or. actual_type /= expected_type) &
      error stop 'list element schema differs'
  end subroutine REQUIRE_LIST_ELEMENT


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    call REQUIRE_LIST_ELEMENT(list,index,-1,0)
  end subroutine REQUIRE_DIRECTORY_ITEM


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type
    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= 0) call FAIL(trim(name)//' unexpectedly present')
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


  subroutine REQUIRE_CHARACTER(root,name,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=72) :: found
    integer :: words
    words=(count+3)/4
    call REQUIRE_RECORD(root,name,words,3)
    found=' '
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= expected) &
      call FAIL(trim(name)//' character value differs')
  end subroutine REQUIRE_CHARACTER


  subroutine REQUIRE_EXACT(root,expected_names)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: expected_names(:)
    character(len=72) :: object_file
    character(len=12) :: object_name, first_name, item_name
    logical :: empty, is_lcm, found(size(expected_names))
    integer :: count, i, object_length

    call REQUIRE_ASSOCIATED(root,'exact-inventory root')
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (empty .or. object_length /= -1) &
      error stop 'exact inventory owner is not a nonempty directory'
    found=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'exact inventory is empty'
    first_name=item_name
    count=0
    do
      count=count+1
      if (count > size(expected_names)) &
        error stop 'exact inventory has extra records'
      do i=1,size(expected_names)
        if (item_name == expected_names(i)) exit
      end do
      if (i > size(expected_names)) &
        error stop 'exact inventory has an unknown record'
      if (found(i)) error stop 'exact inventory record repeated'
      found(i)=.true.
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= size(expected_names) .or. .not. all(found)) &
      error stop 'exact inventory is incomplete'
  end subroutine REQUIRE_EXACT


  subroutine FAIL(message)
    character(len=*), intent(in) :: message
    write(*,'(A)') 'B2S POSTERIOR FAILURE: '//trim(message)
    error stop 'B2S independent posterior failed'
  end subroutine FAIL

end program CHECK_B2S_IMMEDIATE_HOST_BRIDGE

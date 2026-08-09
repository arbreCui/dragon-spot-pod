program CHECK_B2Y_REAL_CLOSE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NSTATE=40, NGRP=370, NSNAP=3
  integer, parameter :: NREG=8, NUNKNO=14, NMAT=8, NIFIS=32
  integer(int32), parameter :: FROZEN_TOL_BITS=int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64=real(huge(0.0_real32),real64)
  integer, parameter :: TRACK_STATE_EXPECTED(NSTATE) = &
      [NREG,NUNKNO,1,NMAT,6,1,4,0,0,0,48,1,-1,4,1,2, &
       165,100000,11364,96,96,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: MACRO_STATE_EXPECTED(NSTATE) = &
      [NGRP,NMAT,3,NIFIS,18,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0, &
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  character(len=12), parameter :: RETURNED_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','TRACK', &
       'MICROLIB2','SYSTEM','FLUX','SPOT-R64']
  character(len=12), parameter :: CLOSED_ROOT_NAMES(8) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
       'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
  character(len=12), parameter :: RETURN_AUTHORITY_NAMES(3) = &
      [character(len=12) :: 'NPLANE','STATE','EPOCH']
  character(len=12), parameter :: CLOSED_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
  character(len=12), parameter :: CHILD_NAMES(16) = &
      [character(len=12) :: 'SPOT-R64','FLUX','SOUR','SIGNATURE', &
       'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
       'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D', &
       'SPOT-FS-EQN','SPOT-FS-K','SPOT-QFISS']
  character(len=12), parameter :: CHILD_AUTHORITY_NAMES(6) = &
      [character(len=12) :: 'RHO','FLUX','SOUR','QFISS','STATE','EPOCH']
  character(len=12), parameter :: SYSTEM_ROOT_NAMES(8) = &
      [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
       'STATE-VECTOR','SPOT-LEAK1D','SPOT-L1-SNAP','GROUP','SPOT-R64']
  character(len=12), parameter :: SYSTEM_AUTHORITY_NAMES(3) = &
      [character(len=12) :: 'RHO','STATE','EPOCH']
  character(len=12), parameter :: GROUP_NAMES(15) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
       'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG', &
       'DRAGON-TXSC','SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG']
  character(len=12), parameter :: RESPONSE_NAMES(12) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
       'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG', &
       'DIAGF$MCCG']
  integer, parameter :: RESPONSE_LENGTHS(12) = &
      [32,14,32,14,8,8,8,8,8,8,8,14]

  character(len=1024) :: returned_path, ax_path, archive_path
  integer :: ip, input_r64, input_r32, closed_r64, closed_r32
  integer :: input_q64, input_q32, closed_q64, closed_q32
  integer :: q64_preserved, q32_preserved
  integer :: l0_bindings, system_l0_preserved, l1_promotions
  integer :: system_groups, rank_one_groups, axial_coefficients
  integer :: archive_children
  integer(int64) :: copied_records, copied_words
  integer(int32) :: first_k_bits
  integer(int64) :: first_rho_bits
  integer :: keyflx(NREG)
  real(real32) :: old_k32, closed_k32
  real(real32) :: old_l0(NGRP), system_l0(NGRP), closed_system_l0(NGRP)
  real(real32) :: new_l1(NGRP)
  real(real64) :: old_rho64, closed_rho64, axial_l1(NGRP*NSNAP)
  type(c_ptr) :: returned, ax_closed, archive_closed
  type(c_ptr) :: rtracks, rlibraries, rsystems, rfluxes
  type(c_ptr) :: atracks, alibraries, asystems, afluxes
  type(c_ptr) :: rtrack, rlibrary, rsystem, rchild
  type(c_ptr) :: asystem, achild

  if (command_argument_count() /= 3) &
      error stop 'expected RETURNED, AX_CLOSED, and ARCH_CLOSED XSM paths'
  call get_command_argument(1,returned_path)
  call get_command_argument(2,ax_path)
  call get_command_argument(3,archive_path)
  if (len_trim(returned_path) == 0 .or. len_trim(ax_path) == 0 .or. &
      len_trim(archive_path) == 0) error stop 'empty XSM path is forbidden'

  call OPEN_READ_ONLY(returned_path,returned)
  call OPEN_READ_ONLY(ax_path,ax_closed)
  call OPEN_READ_ONLY(archive_path,archive_closed)
  call REQUIRE_DISTINCT(returned,ax_closed,'RETURNED/AX roots')
  call REQUIRE_DISTINCT(returned,archive_closed,'RETURNED/archive roots')
  call REQUIRE_DISTINCT(ax_closed,archive_closed,'AX/archive roots')

  call VERIFY_RETURNED_ROOT(returned)
  call VERIFY_CLOSED_AX(ax_closed,closed_k32,closed_rho64,axial_l1, &
      rank_one_groups,axial_coefficients)
  call VERIFY_CLOSED_ROOT(archive_closed,closed_k32,closed_rho64)

  rtracks=LCMGID(returned,'TRACK')
  rlibraries=LCMGID(returned,'MICROLIB2')
  rsystems=LCMGID(returned,'SYSTEM')
  rfluxes=LCMGID(returned,'FLUX')
  atracks=LCMGID(archive_closed,'TRACK')
  alibraries=LCMGID(archive_closed,'MICROLIB2')
  asystems=LCMGID(archive_closed,'SYSTEM')
  afluxes=LCMGID(archive_closed,'FLUX')
  call REQUIRE_ASSOCIATED(rtracks,'RETURNED TRACK list')
  call REQUIRE_ASSOCIATED(rlibraries,'RETURNED MICROLIB2 list')
  call REQUIRE_ASSOCIATED(rsystems,'RETURNED SYSTEM list')
  call REQUIRE_ASSOCIATED(rfluxes,'RETURNED FLUX list')
  call REQUIRE_ASSOCIATED(atracks,'closed TRACK list')
  call REQUIRE_ASSOCIATED(alibraries,'closed MICROLIB2 list')
  call REQUIRE_ASSOCIATED(asystems,'closed SYSTEM list')
  call REQUIRE_ASSOCIATED(afluxes,'closed FLUX list')
  call REQUIRE_DISTINCT(rtracks,atracks,'TRACK lists')
  call REQUIRE_DISTINCT(rlibraries,alibraries,'MICROLIB2 lists')
  call REQUIRE_DISTINCT(rsystems,asystems,'SYSTEM lists')
  call REQUIRE_DISTINCT(rfluxes,afluxes,'FLUX lists')

  copied_records=0_int64
  copied_words=0_int64
  call COMPARE_LIST(rtracks,atracks,NSNAP,copied_records,copied_words)
  call COMPARE_LIST(rlibraries,alibraries,NSNAP,copied_records,copied_words)
  call COMPARE_LIST(rsystems,asystems,NSNAP,copied_records,copied_words)

  input_r64=0
  input_r32=0
  closed_r64=0
  closed_r32=0
  input_q64=0
  input_q32=0
  closed_q64=0
  closed_q32=0
  q64_preserved=0
  q32_preserved=0
  l0_bindings=0
  system_l0_preserved=0
  l1_promotions=0
  system_groups=0
  archive_children=0
  first_k_bits=0_int32
  first_rho_bits=0_int64

  do ip=1,NSNAP
    call REQUIRE_DIRECTORY_ITEM(rtracks,ip)
    call REQUIRE_DIRECTORY_ITEM(rlibraries,ip)
    call REQUIRE_DIRECTORY_ITEM(rsystems,ip)
    call REQUIRE_DIRECTORY_ITEM(rfluxes,ip)
    call REQUIRE_DIRECTORY_ITEM(asystems,ip)
    call REQUIRE_DIRECTORY_ITEM(afluxes,ip)
    rtrack=LCMGIL(rtracks,ip)
    rlibrary=LCMGIL(rlibraries,ip)
    rsystem=LCMGIL(rsystems,ip)
    rchild=LCMGIL(rfluxes,ip)
    asystem=LCMGIL(asystems,ip)
    achild=LCMGIL(afluxes,ip)
    call REQUIRE_DISTINCT(rsystem,asystem,'same-index SYSTEM children')
    call REQUIRE_DISTINCT(rchild,achild,'same-index FLUX children')

    call VERIFY_TRACK(rtrack,keyflx)
    call VERIFY_LIBRARY(rlibrary)
    call VERIFY_CHILD(rchild,keyflx,old_rho64,old_k32,old_l0, &
        input_r64,input_r32,input_q64,input_q32)
    call VERIFY_SYSTEM(rsystem,ip,old_rho64,system_l0,system_groups)
    if (any(BITS32(old_l0) /= BITS32(system_l0))) &
        call FAIL('RETURNED child L0 differs from same-index SYSTEM L0')
    l0_bindings=l0_bindings+NGRP

    call VERIFY_CHILD(achild,keyflx,old_rho64,old_k32,new_l1, &
        closed_r64,closed_r32,closed_q64,closed_q32)
    call COMPARE_CHILD_EXCEPT_LEAKAGE(rchild,achild,copied_records,copied_words)
    q64_preserved=q64_preserved+NGRP*NUNKNO
    q32_preserved=q32_preserved+NGRP*NUNKNO

    call LCMGET(asystem,'SPOT-LEAK1D',closed_system_l0)
    if (any(BITS32(system_l0) /= BITS32(closed_system_l0))) &
        call FAIL('closed SYSTEM did not preserve lagged L0')
    system_l0_preserved=system_l0_preserved+NGRP
    if (.not. all(ieee_is_finite(new_l1))) &
        call FAIL('closed child L1 is nonfinite')
    if (any(BITS64(axial_l1((ip-1)*NGRP+1:ip*NGRP)) /= &
        BITS64(real(new_l1,real64)))) &
        call FAIL('closed child L1 is not the exact AX leakage promotion')
    l1_promotions=l1_promotions+NGRP

    if (ip == 1) then
      first_k_bits=BITS32(old_k32)
      first_rho_bits=BITS64(old_rho64)
    else if (BITS32(old_k32) /= first_k_bits .or. &
        BITS64(old_rho64) /= first_rho_bits) then
      call FAIL('returned radial K/RHO differs across planes')
    end if
    archive_children=archive_children+4
  end do

  call LCMCL(archive_closed,1)
  call LCMCL(ax_closed,1)
  call LCMCL(returned,1)

  if (input_r64 /= 3*NSNAP*NGRP*NUNKNO .or. &
      closed_r64 /= 3*NSNAP*NGRP*NUNKNO) &
      call FAIL('REAL64 authority census differs')
  if (input_r32 /= input_r64 .or. closed_r32 /= closed_r64) &
      call FAIL('REAL32 mirror census differs')
  if (input_q64 /= NSNAP*NGRP*NUNKNO .or. input_q32 /= input_q64 .or. &
      closed_q64 /= input_q64 .or. closed_q32 /= input_q64) &
      call FAIL('QFISS inventory census differs')
  if (q64_preserved /= NSNAP*NGRP*NUNKNO .or. &
      q32_preserved /= NSNAP*NGRP*NUNKNO) &
      call FAIL('QFISS preservation census differs')
  if (l0_bindings /= NSNAP*NGRP .or. &
      system_l0_preserved /= NSNAP*NGRP .or. &
      l1_promotions /= NSNAP*NGRP) call FAIL('leakage census differs')
  if (system_groups /= NSNAP*NGRP) call FAIL('SYSTEM group census differs')
  if (rank_one_groups /= NGRP .or. axial_coefficients /= NSNAP*NGRP) &
      call FAIL('rank-one axial census differs')
  if (archive_children /= 4*NSNAP) call FAIL('archive child census differs')
  if (copied_records <= 0_int64 .or. copied_words <= 0_int64) &
      call FAIL('recursive copy census is empty')

  write(*,'(A)') 'B2Y REAL RETURNED-CLOSE POSTERIOR PASS'
  write(*,'(A)') 'B2Y ROOT=RETURNED/1->CLOSED/1 AX=CLOSED/1 PLANES=3'
  write(*,'(A,I0,A,I0)') 'B2Y RETURNED-R64=',input_r64, &
      ' RETURNED-R32=',input_r32
  write(*,'(A,I0,A,I0)') 'B2Y CLOSED-R64=',closed_r64, &
      ' CLOSED-R32=',closed_r32
  write(*,'(A,I0,A,I0)') 'B2Y QFISS64-PRESERVED=',q64_preserved, &
      ' QFISS32-PRESERVED=',q32_preserved
  write(*,'(A,I0,A,I0,A,I0)') 'B2Y L0-CHILD-SYSTEM=',l0_bindings, &
      ' SYSTEM-L0-PRESERVED=',system_l0_preserved, &
      ' L1-AX-PROMOTIONS=',l1_promotions
  write(*,'(A,I0,A,I0,A,I0)') 'B2Y AX-RANK1-GROUPS=',rank_one_groups, &
      ' AX-COEFFICIENTS=',axial_coefficients, &
      ' ARCHIVE-CHILDREN=',archive_children
  write(*,'(A)') &
      'B2Y READ-ONLY=3 GANLIB/UTILIB-ONLY=YES PICARD-CONVERGENCE=NOT-EVALUATED'

contains

  subroutine VERIFY_RETURNED_ROOT(root)
    type(c_ptr), intent(in) :: root
    type(c_ptr) :: authority

    call REQUIRE_EXACT(root,RETURNED_ROOT_NAMES)
    call REQUIRE_CHARACTER12(root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_INTEGER(root,'LISTDIM',NSNAP)
    call REQUIRE_RECORD(root,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(root,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(root,'SYSTEM',NSNAP,10)
    call REQUIRE_RECORD(root,'FLUX',NSNAP,10)
    call REQUIRE_RECORD(root,'SPOT-R64',-1,0)
    call REQUIRE_ABSENT(root,'SPOT-ITER-K')
    call REQUIRE_ABSENT(root,'SPOT-L1-ERR')
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'RETURNED root authority')
    call REQUIRE_EXACT(authority,RETURN_AUTHORITY_NAMES)
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER12(authority,'STATE','RETURNED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_ABSENT(authority,'RHO')
  end subroutine VERIFY_RETURNED_ROOT


  subroutine VERIFY_CLOSED_ROOT(root,keff32,rho64)
    type(c_ptr), intent(in) :: root
    real(real32), intent(in) :: keff32
    real(real64), intent(in) :: rho64
    real(real64) :: found_keff, found_rho
    type(c_ptr) :: authority

    call REQUIRE_EXACT(root,CLOSED_ROOT_NAMES)
    call REQUIRE_CHARACTER12(root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_INTEGER(root,'LISTDIM',NSNAP)
    call REQUIRE_RECORD(root,'SPOT-ITER-K',1,4)
    call REQUIRE_RECORD(root,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(root,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(root,'SYSTEM',NSNAP,10)
    call REQUIRE_RECORD(root,'FLUX',NSNAP,10)
    call REQUIRE_RECORD(root,'SPOT-R64',-1,0)
    call REQUIRE_ABSENT(root,'SPOT-L1-ERR')
    call LCMGET(root,'SPOT-ITER-K',found_keff)
    if (.not. ieee_is_finite(found_keff) .or. &
        BITS64(found_keff) /= BITS64(real(keff32,real64))) &
        call FAIL('closed archive K differs from closed AX K')
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'closed root authority')
    call REQUIRE_EXACT(authority,CLOSED_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER12(authority,'STATE','CLOSED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',found_rho)
    if (.not. ieee_is_finite(found_rho) .or. &
        BITS64(found_rho) /= BITS64(rho64)) &
        call FAIL('closed archive RHO differs from closed AX RHO')
  end subroutine VERIFY_CLOSED_ROOT


  subroutine VERIFY_CLOSED_AX(root,keff32,rho64,leakage64, &
      rank_groups,ncoefficients)
    type(c_ptr), intent(in) :: root
    real(real32), intent(out) :: keff32
    real(real64), intent(out) :: rho64, leakage64(NGRP*NSNAP)
    integer, intent(out) :: rank_groups, ncoefficients
    integer :: state(NSTATE), dims(4), rank(NGRP)
    integer :: offset(NGRP+1), gram_offset(NGRP+1), basis_offset(NGRP+1)
    integer :: ig, total_gram, total_basis
    real(real32), allocatable :: basis32(:)
    real(real32), allocatable :: ordinary_flux(:)
    real(real64), allocatable :: coordinates64(:), gram64(:)
    real(real64) :: height64(NSNAP), norm64
    real(real64) :: offspace64(NGRP*NSNAP), gram_error64
    type(c_ptr) :: fluxes

    call REQUIRE_CHARACTER12(root,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(root,'STATE-VECTOR',NSTATE,1)
    call LCMGET(root,'STATE-VECTOR',state)
    if (state(1) /= NGRP .or. state(2) <= 0) &
        call FAIL('closed AX STATE-VECTOR differs')
    call REQUIRE_RECORD(root,'K-EFFECTIVE',1,2)
    call LCMGET(root,'K-EFFECTIVE',keff32)
    if (.not. ieee_is_finite(keff32) .or. keff32 <= +0.0_real32) &
        call FAIL('closed AX K is invalid')
    call REQUIRE_CHARACTER12(root,'SPOT-X-STATE','CLOSED')
    call REQUIRE_INTEGER(root,'SPOT-X-EPOCH',1)
    call REQUIRE_RECORD(root,'FLUX',NGRP,10)
    fluxes=LCMGID(root,'FLUX')
    call REQUIRE_ASSOCIATED(fluxes,'closed AX ordinary FLUX')
    allocate(ordinary_flux(state(2)))
    do ig=1,NGRP
      call REQUIRE_LIST_RECORD(fluxes,ig,state(2),2)
      call LCMGDL(fluxes,ig,ordinary_flux)
      if (.not. all(ieee_is_finite(ordinary_flux))) &
          call FAIL('closed AX ordinary FLUX is nonfinite')
    end do

    call REQUIRE_RECORD(root,'SPOT-X-DIMS',4,1)
    call LCMGET(root,'SPOT-X-DIMS',dims)
    if (any(dims /= [1,NGRP,NSNAP,NGRP*NSNAP])) &
        call FAIL('closed AX SPOT-X-DIMS differs')
    ncoefficients=dims(4)
    call REQUIRE_INTEGER(root,'SPOT-X-FIXB',1)
    call REQUIRE_CHARACTER12(root,'SPOT-X-NID','NUFISS-UNIT')
    call REQUIRE_CHARACTER12(root,'SPOT-X-BTYP','POD-FIXED')
    call REQUIRE_RECORD(root,'SPOT-X-RANK',NGRP,1)
    call REQUIRE_RECORD(root,'SPOT-X-OFF',NGRP+1,1)
    call REQUIRE_RECORD(root,'SPOT-X-GOFF',NGRP+1,1)
    call REQUIRE_RECORD(root,'SPOT-X-BOFF',NGRP+1,1)
    call LCMGET(root,'SPOT-X-RANK',rank)
    call LCMGET(root,'SPOT-X-OFF',offset)
    call LCMGET(root,'SPOT-X-GOFF',gram_offset)
    call LCMGET(root,'SPOT-X-BOFF',basis_offset)
    if (any(rank /= 1)) call FAIL('closed AX is not rank one')
    rank_groups=count(rank == 1)
    do ig=1,NGRP+1
      if (offset(ig) /= (ig-1)*NSNAP .or. &
          gram_offset(ig) /= ig-1 .or. &
          basis_offset(ig) /= (ig-1)*NREG) &
          call FAIL('closed AX packed offsets differ')
    end do
    total_gram=gram_offset(NGRP+1)
    total_basis=basis_offset(NGRP+1)
    call REQUIRE_RECORD(root,'SPOT-X-A',ncoefficients,4)
    call REQUIRE_RECORD(root,'SPOT-X-GRAM',total_gram,4)
    call REQUIRE_RECORD(root,'SPOT-X-BASIS',total_basis,2)
    call REQUIRE_RECORD(root,'SPOT-X-RHO',1,4)
    call REQUIRE_RECORD(root,'SPOT-X-L',NGRP*NSNAP,4)
    call REQUIRE_RECORD(root,'SPOT-X-H',NSNAP,4)
    call REQUIRE_RECORD(root,'SPOT-X-NORM',1,4)
    call REQUIRE_RECORD(root,'SPOT-X-PERP',NGRP*NSNAP,4)
    call REQUIRE_RECORD(root,'SPOT-X-GERR',1,4)
    allocate(basis32(total_basis),coordinates64(ncoefficients), &
        gram64(total_gram))
    call LCMGET(root,'SPOT-X-BASIS',basis32)
    call LCMGET(root,'SPOT-X-A',coordinates64)
    call LCMGET(root,'SPOT-X-GRAM',gram64)
    call LCMGET(root,'SPOT-X-RHO',rho64)
    call LCMGET(root,'SPOT-X-L',leakage64)
    call LCMGET(root,'SPOT-X-H',height64)
    call LCMGET(root,'SPOT-X-NORM',norm64)
    call LCMGET(root,'SPOT-X-PERP',offspace64)
    call LCMGET(root,'SPOT-X-GERR',gram_error64)
    if (.not. all(ieee_is_finite(basis32)) .or. &
        .not. all(ieee_is_finite(coordinates64)) .or. &
        .not. all(ieee_is_finite(gram64)) .or. &
        .not. all(ieee_is_finite(leakage64)) .or. &
        .not. all(ieee_is_finite(height64)) .or. &
        .not. all(ieee_is_finite(offspace64))) &
        call FAIL('closed AX canonical array is nonfinite')
    if (any(height64 <= +0.0_real64) .or. &
        any(offspace64 < +0.0_real64)) &
        call FAIL('closed AX height/off-space value is invalid')
    if (.not. ieee_is_finite(norm64) .or. norm64 <= +0.0_real64 .or. &
        .not. ieee_is_finite(gram_error64) .or. gram_error64 < +0.0_real64) &
        call FAIL('closed AX norm/Gram error is invalid')
    if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64 .or. &
        BITS64(rho64) /= BITS64(1.0_real64/real(keff32,real64))) &
        call FAIL('closed AX RHO/K reciprocal differs')
  end subroutine VERIFY_CLOSED_AX


  subroutine VERIFY_TRACK(track,key)
    type(c_ptr), intent(in) :: track
    integer, intent(out) :: key(NREG)
    integer :: state(NSTATE), key_anis(NREG), ir
    logical :: seen(NUNKNO)

    call REQUIRE_CHARACTER12(track,'SIGNATURE','L_TRACK')
    call REQUIRE_RECORD(track,'STATE-VECTOR',NSTATE,1)
    call LCMGET(track,'STATE-VECTOR',state)
    if (any(state /= TRACK_STATE_EXPECTED)) call FAIL('TRACK state differs')
    call REQUIRE_RECORD(track,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
    call LCMGET(track,'KEYFLX',key)
    call LCMGET(track,'KEYFLX$ANIS',key_anis)
    if (any(key /= key_anis)) call FAIL('TRACK KEYFLX aliases differ')
    seen=.false.
    do ir=1,NREG
      if (key(ir) < 1 .or. key(ir) > NUNKNO .or. seen(key(ir))) &
          call FAIL('TRACK KEYFLX map is invalid')
      seen(key(ir))=.true.
    end do
  end subroutine VERIFY_TRACK


  subroutine VERIFY_LIBRARY(library)
    type(c_ptr), intent(in) :: library
    integer :: state(NSTATE), macro_state(NSTATE)
    type(c_ptr) :: macro

    call REQUIRE_CHARACTER12(library,'SIGNATURE','L_LIBRARY')
    call REQUIRE_RECORD(library,'STATE-VECTOR',NSTATE,1)
    call LCMGET(library,'STATE-VECTOR',state)
    if (state(1) /= NMAT .or. state(2) <= 0 .or. &
        state(3) /= NGRP .or. state(4) /= 3) &
        call FAIL('MICROLIB2 state differs')
    call REQUIRE_RECORD(library,'MACROLIB',-1,0)
    macro=LCMGID(library,'MACROLIB')
    call REQUIRE_ASSOCIATED(macro,'MICROLIB2 MACROLIB')
    call REQUIRE_CHARACTER12(macro,'SIGNATURE','L_MACROLIB')
    call REQUIRE_RECORD(macro,'STATE-VECTOR',NSTATE,1)
    call LCMGET(macro,'STATE-VECTOR',macro_state)
    if (any(macro_state /= MACRO_STATE_EXPECTED)) &
        call FAIL('MICROLIB2 MACROLIB state differs')
    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
  end subroutine VERIFY_LIBRARY


  subroutine VERIFY_SYSTEM(system,plane,rho64,leakage32,group_count)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho64
    real(real32), intent(out) :: leakage32(NGRP)
    integer, intent(inout) :: group_count
    integer :: state(NSTATE), expected_state(NSTATE), ig, i
    real(real32), allocatable :: values(:)
    real(real64) :: found_rho
    type(c_ptr) :: authority, groups, group

    call REQUIRE_EXACT(system,SYSTEM_ROOT_NAMES)
    call REQUIRE_CHARACTER12(system,'SIGNATURE','L_PIJ')
    call REQUIRE_CHARACTER12(system,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(system,'LINK.TRACK','TRACK')
    call REQUIRE_RECORD(system,'STATE-VECTOR',NSTATE,1)
    call LCMGET(system,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:14)=[1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0]
    if (any(state /= expected_state)) call FAIL('SYSTEM state differs')
    call REQUIRE_INTEGER(system,'SPOT-L1-SNAP',plane)
    call REQUIRE_RECORD(system,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(system,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) &
        call FAIL('SYSTEM L0 is nonfinite')
    call REQUIRE_RECORD(system,'SPOT-R64',-1,0)
    authority=LCMGID(system,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SYSTEM authority')
    call REQUIRE_EXACT(authority,SYSTEM_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','ASSEMBLED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',found_rho)
    if (.not. ieee_is_finite(found_rho) .or. &
        BITS64(found_rho) /= BITS64(rho64)) &
        call FAIL('SYSTEM RHO differs from child RHO')
    call REQUIRE_RECORD(system,'GROUP',NGRP,10)
    groups=LCMGID(system,'GROUP')
    call REQUIRE_ASSOCIATED(groups,'SYSTEM GROUP list')
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(groups,ig)
      group=LCMGIL(groups,ig)
      call REQUIRE_EXACT(group,GROUP_NAMES)
      do i=1,size(RESPONSE_NAMES)
        call REQUIRE_RECORD(group,RESPONSE_NAMES(i),RESPONSE_LENGTHS(i),2)
        allocate(values(RESPONSE_LENGTHS(i)))
        call LCMGET(group,RESPONSE_NAMES(i),values)
        if (.not. all(ieee_is_finite(values))) &
            call FAIL('SYSTEM response is nonfinite')
        deallocate(values)
      end do
      do i=1,3
        select case(i)
        case(1)
          call VERIFY_REAL32_RECORD(group,'DRAGON-TXSC',NMAT+1)
        case(2)
          call VERIFY_REAL32_RECORD(group,'SPOT-S0-PHYS',NMAT+1)
        case(3)
          call VERIFY_REAL32_RECORD(group,'DRAGON-S0XSC',NMAT+1)
        end select
      end do
      group_count=group_count+1
    end do
  end subroutine VERIFY_SYSTEM


  subroutine VERIFY_CHILD(child,expected_key,rho64,keff32,leakage32, &
      n64,n32,nq64,nq32)
    type(c_ptr), intent(in) :: child
    integer, intent(in) :: expected_key(NREG)
    real(real64), intent(out) :: rho64
    real(real32), intent(out) :: keff32, leakage32(NGRP)
    integer, intent(inout) :: n64, n32, nq64, nq32
    integer :: state(NSTATE), expected_state(NSTATE), key(NREG), imerge(NMAT)
    integer :: epoch, marker, ig, field
    integer(int32) :: eps_bits(5)
    real(real32) :: eps32(5), mirror32(NUNKNO)
    real(real64) :: authority64(NUNKNO)
    type(c_ptr) :: authority, authority_list, mirror_list
    type(c_ptr) :: qouter, qinner

    call REQUIRE_EXACT(child,CHILD_NAMES)
    call REQUIRE_CHARACTER12(child,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(child,'STATE-VECTOR',NSTATE,1)
    call LCMGET(child,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:18)=[NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1]
    if (any(state /= expected_state)) call FAIL('SOLVED child state differs')
    call REQUIRE_RECORD(child,'EPS-CONVERGE',5,2)
    call LCMGET(child,'EPS-CONVERGE',eps32)
    if (.not. all(ieee_is_finite(eps32))) &
        call FAIL('SOLVED tolerance is nonfinite')
    eps_bits=transfer(eps32,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS) .or. &
        any(eps_bits(4:5) /= 0_int32)) &
        call FAIL('SOLVED tolerance bits differ')
    call REQUIRE_RECORD(child,'IMERGE-LEAK',NMAT,1)
    call LCMGET(child,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) call FAIL('SOLVED IMERGE-LEAK differs')
    call REQUIRE_RECORD(child,'KEYFLX',NREG,1)
    call LCMGET(child,'KEYFLX',key)
    if (any(key /= expected_key)) call FAIL('SOLVED KEYFLX differs from TRACK')
    call REQUIRE_CHARACTER_N(child,'OPTION',1,4,'B0  ')
    call REQUIRE_CHARACTER12(child,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(child,'LINK.TRACK','TRACK')
    call REQUIRE_CHARACTER12(child,'LINK.SYSTEM','SYSTEM')
    call REQUIRE_INTEGER(child,'SPOT-FS-EQN',1)
    call REQUIRE_RECORD(child,'SPOT-FS-K',1,2)
    call LCMGET(child,'SPOT-FS-EQN',marker)
    call LCMGET(child,'SPOT-FS-K',keff32)
    if (marker /= 1 .or. .not. ieee_is_finite(keff32) .or. &
        keff32 <= +0.0_real32) call FAIL('SOLVED source/K marker differs')
    call REQUIRE_RECORD(child,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(child,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) &
        call FAIL('SOLVED child leakage is nonfinite')

    call REQUIRE_RECORD(child,'SPOT-R64',-1,0)
    authority=LCMGID(child,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SOLVED child authority')
    call REQUIRE_EXACT(authority,CHILD_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','SOLVED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_ABSENT(authority,'PLANE')
    call LCMGET(authority,'RHO',rho64)
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= 1 .or. .not. ieee_is_finite(rho64) .or. &
        rho64 <= +0.0_real64 .or. &
        BITS64(rho64) /= BITS64(1.0_real64/real(keff32,real64))) &
        call FAIL('SOLVED child RHO/K authority differs')

    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(authority,'SOUR',NGRP,10)
    call REQUIRE_RECORD(authority,'QFISS',NGRP,10)
    call REQUIRE_RECORD(child,'FLUX',NGRP,10)
    call REQUIRE_RECORD(child,'SOUR',NGRP,10)
    call REQUIRE_RECORD(child,'SPOT-QFISS',1,10)
    qouter=LCMGID(child,'SPOT-QFISS')
    call REQUIRE_ASSOCIATED(qouter,'SOLVED QFISS outer list')
    call REQUIRE_LIST_RECORD(qouter,1,NGRP,10)
    qinner=LCMGIL(qouter,1)
    call REQUIRE_ASSOCIATED(qinner,'SOLVED QFISS inner list')
    do field=1,3
      select case(field)
      case(1)
        authority_list=LCMGID(authority,'FLUX')
        mirror_list=LCMGID(child,'FLUX')
      case(2)
        authority_list=LCMGID(authority,'SOUR')
        mirror_list=LCMGID(child,'SOUR')
      case(3)
        authority_list=LCMGID(authority,'QFISS')
        mirror_list=qinner
      end select
      call REQUIRE_ASSOCIATED(authority_list,'SOLVED REAL64 field list')
      call REQUIRE_ASSOCIATED(mirror_list,'SOLVED REAL32 field list')
      do ig=1,NGRP
        call REQUIRE_LIST_RECORD(authority_list,ig,NUNKNO,4)
        call REQUIRE_LIST_RECORD(mirror_list,ig,NUNKNO,2)
        call LCMGDL(authority_list,ig,authority64)
        call LCMGDL(mirror_list,ig,mirror32)
        call VERIFY_REAL64_MIRROR(authority64,mirror32)
        if (field == 3 .and. any(authority64 < +0.0_real64)) &
            call FAIL('SOLVED QFISS is negative')
        n64=n64+NUNKNO
        n32=n32+NUNKNO
        if (field == 3) then
          nq64=nq64+NUNKNO
          nq32=nq32+NUNKNO
        end if
      end do
    end do
  end subroutine VERIFY_CHILD


  subroutine COMPARE_CHILD_EXCEPT_LEAKAGE(input,output,record_count,word_count)
    type(c_ptr), intent(in) :: input, output
    integer(int64), intent(inout) :: record_count, word_count
    character(len=12), parameter :: copied_names(11) = &
        [character(len=12) :: 'SIGNATURE','STATE-VECTOR','EPS-CONVERGE', &
         'IMERGE-LEAK','KEYFLX','OPTION','LINK.MACRO','LINK.TRACK', &
         'LINK.SYSTEM','SPOT-FS-EQN','SPOT-FS-K']
    integer :: i
    type(c_ptr) :: left, right

    do i=1,size(copied_names)
      call COMPARE_NAMED_AUTO(input,output,copied_names(i), &
          record_count,word_count)
    end do
    left=LCMGID(input,'SPOT-R64')
    right=LCMGID(output,'SPOT-R64')
    call REQUIRE_DISTINCT(left,right,'child SPOT-R64 authorities')
    call COMPARE_DICTIONARY(left,right,record_count,word_count)
    left=LCMGID(input,'FLUX')
    right=LCMGID(output,'FLUX')
    call REQUIRE_DISTINCT(left,right,'child FLUX mirrors')
    call COMPARE_LIST(left,right,NGRP,record_count,word_count)
    left=LCMGID(input,'SOUR')
    right=LCMGID(output,'SOUR')
    call REQUIRE_DISTINCT(left,right,'child SOUR mirrors')
    call COMPARE_LIST(left,right,NGRP,record_count,word_count)
    left=LCMGID(input,'SPOT-QFISS')
    right=LCMGID(output,'SPOT-QFISS')
    call REQUIRE_DISTINCT(left,right,'child QFISS mirrors')
    call COMPARE_LIST(left,right,1,record_count,word_count)
  end subroutine COMPARE_CHILD_EXCEPT_LEAKAGE


  subroutine VERIFY_REAL64_MIRROR(authority,mirror)
    real(real64), intent(in) :: authority(:)
    real(real32), intent(in) :: mirror(:)
    if (size(authority) /= size(mirror)) call FAIL('mirror extent differs')
    if (.not. all(ieee_is_finite(authority)) .or. &
        .not. all(ieee_is_finite(mirror))) &
        call FAIL('REAL64 authority or REAL32 mirror is nonfinite')
    if (any(abs(authority) > REAL32_MAX64)) &
        call FAIL('REAL64 authority exceeds REAL32 mirror range')
    if (any(BITS32(mirror) /= BITS32(real(authority,real32)))) &
        call FAIL('REAL64 authority/REAL32 mirror projection differs')
  end subroutine VERIFY_REAL64_MIRROR


  subroutine VERIFY_REAL32_RECORD(root,name,length)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: length
    real(real32), allocatable :: values(:)
    call REQUIRE_RECORD(root,name,length,2)
    allocate(values(length))
    call LCMGET(root,name,values)
    if (.not. all(ieee_is_finite(values))) &
        call FAIL(trim(name)//' contains a nonfinite value')
  end subroutine VERIFY_REAL32_RECORD


  recursive subroutine COMPARE_DICTIONARY(left,right,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer(int64), intent(inout) :: record_count, word_count
    character(len=12) :: first_name, name
    integer :: left_count, right_count, left_length, right_length
    integer :: left_type, right_type
    type(c_ptr) :: left_child, right_child

    call COUNT_DICTIONARY_NAMES(left,left_count)
    call COUNT_DICTIONARY_NAMES(right,right_count)
    if (left_count /= right_count) call FAIL('copied directory count differs')
    if (left_count == 0) return
    name=' '
    call LCMNXT(left,name)
    first_name=name
    do
      call LCMLEN(left,name,left_length,left_type)
      call LCMLEN(right,name,right_length,right_type)
      if (left_length /= right_length .or. left_type /= right_type) &
          call FAIL('copied named schema differs')
      select case(left_type)
      case(0)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied dictionary')
        call REQUIRE_ASSOCIATED(right_child,'right copied dictionary')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied list')
        call REQUIRE_ASSOCIATED(right_child,'right copied list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count,word_count)
      case default
        call COMPARE_NAMED_PAYLOAD(left,right,name,left_length,left_type, &
            record_count,word_count)
      end select
      call LCMNXT(left,name)
      if (name == first_name) exit
    end do
  end subroutine COMPARE_DICTIONARY


  recursive subroutine COMPARE_LIST(left,right,length,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: length
    integer(int64), intent(inout) :: record_count, word_count
    integer :: index, left_length, right_length, left_type, right_type
    type(c_ptr) :: left_child, right_child

    do index=1,length
      call LCMLEL(left,index,left_length,left_type)
      call LCMLEL(right,index,right_length,right_type)
      if (left_length /= right_length .or. left_type /= right_type) &
          call FAIL('copied list schema differs')
      select case(left_type)
      case(0)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left copied list directory')
        call REQUIRE_ASSOCIATED(right_child,'right copied list directory')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left nested list')
        call REQUIRE_ASSOCIATED(right_child,'right nested list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count,word_count)
      case default
        call COMPARE_LIST_PAYLOAD(left,right,index,left_length,left_type, &
            record_count,word_count)
      end select
    end do
  end subroutine COMPARE_LIST


  subroutine COMPARE_NAMED_AUTO(left,right,name,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer(int64), intent(inout) :: record_count, word_count
    integer :: left_length, right_length, left_type, right_type
    call LCMLEN(left,name,left_length,left_type)
    call LCMLEN(right,name,right_length,right_type)
    if (left_length /= right_length .or. left_type /= right_type .or. &
        left_type == 0 .or. left_type == 10 .or. left_type == 99) &
        call FAIL(trim(name)//' copied scalar schema differs')
    call COMPARE_NAMED_PAYLOAD(left,right,name,left_length,left_type, &
        record_count,word_count)
  end subroutine COMPARE_NAMED_AUTO


  subroutine COMPARE_NAMED_PAYLOAD(left,right,name,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: length, record_type
    integer(int64), intent(inout) :: record_count, word_count
    integer, allocatable :: il(:), ir(:)
    real(real32), allocatable :: rl(:), rr(:)
    real(real64), allocatable :: dl(:), dr(:)
    logical, allocatable :: ll(:), lr(:)
    complex(real32), allocatable :: cl(:), cr(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(il(length),ir(length))
      call LCMGET(left,name,il)
      call LCMGET(right,name,ir)
      if (any(il /= ir)) call FAIL('copied integer/character bits differ')
      word_count=word_count+length
    case(2)
      allocate(rl(length),rr(length))
      call LCMGET(left,name,rl)
      call LCMGET(right,name,rr)
      if (any(BITS32(rl) /= BITS32(rr))) call FAIL('copied REAL32 bits differ')
      word_count=word_count+length
    case(4)
      allocate(dl(length),dr(length))
      call LCMGET(left,name,dl)
      call LCMGET(right,name,dr)
      if (any(BITS64(dl) /= BITS64(dr))) call FAIL('copied REAL64 bits differ')
      word_count=word_count+2_int64*length
    case(5)
      allocate(ll(length),lr(length))
      call LCMGET(left,name,ll)
      call LCMGET(right,name,lr)
      if (any(transfer(ll,0_int32,length) /= transfer(lr,0_int32,length))) &
          call FAIL('copied logical bits differ')
      word_count=word_count+length
    case(6)
      allocate(cl(length),cr(length))
      call LCMGET(left,name,cl)
      call LCMGET(right,name,cr)
      if (any(transfer(cl,0_int32,2*length) /= &
          transfer(cr,0_int32,2*length))) &
          call FAIL('copied complex bits differ')
      word_count=word_count+2_int64*length
    case default
      call FAIL('unsupported copied GANLIB record type')
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_NAMED_PAYLOAD


  subroutine COMPARE_LIST_PAYLOAD(left,right,index,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: index, length, record_type
    integer(int64), intent(inout) :: record_count, word_count
    integer, allocatable :: il(:), ir(:)
    real(real32), allocatable :: rl(:), rr(:)
    real(real64), allocatable :: dl(:), dr(:)
    logical, allocatable :: ll(:), lr(:)
    complex(real32), allocatable :: cl(:), cr(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(il(length),ir(length))
      call LCMGDL(left,index,il)
      call LCMGDL(right,index,ir)
      if (any(il /= ir)) call FAIL('copied list integer/character bits differ')
      word_count=word_count+length
    case(2)
      allocate(rl(length),rr(length))
      call LCMGDL(left,index,rl)
      call LCMGDL(right,index,rr)
      if (any(BITS32(rl) /= BITS32(rr))) &
          call FAIL('copied list REAL32 bits differ')
      word_count=word_count+length
    case(4)
      allocate(dl(length),dr(length))
      call LCMGDL(left,index,dl)
      call LCMGDL(right,index,dr)
      if (any(BITS64(dl) /= BITS64(dr))) &
          call FAIL('copied list REAL64 bits differ')
      word_count=word_count+2_int64*length
    case(5)
      allocate(ll(length),lr(length))
      call LCMGDL(left,index,ll)
      call LCMGDL(right,index,lr)
      if (any(transfer(ll,0_int32,length) /= transfer(lr,0_int32,length))) &
          call FAIL('copied list logical bits differ')
      word_count=word_count+length
    case(6)
      allocate(cl(length),cr(length))
      call LCMGDL(left,index,cl)
      call LCMGDL(right,index,cr)
      if (any(transfer(cl,0_int32,2*length) /= &
          transfer(cr,0_int32,2*length))) &
          call FAIL('copied list complex bits differ')
      word_count=word_count+2_int64*length
    case default
      call FAIL('unsupported copied GANLIB list record type')
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_LIST_PAYLOAD


  subroutine COUNT_DICTIONARY_NAMES(root,result_count)
    type(c_ptr), intent(in) :: root
    integer, intent(out) :: result_count
    character(len=12) :: first_name, name
    result_count=0
    name=' '
    call LCMNXT(root,name)
    if (name == ' ') return
    first_name=name
    do
      result_count=result_count+1
      call LCMNXT(root,name)
      if (name == first_name) exit
    end do
  end subroutine COUNT_DICTIONARY_NAMES


  subroutine REQUIRE_EXACT(root,expected_names)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, name
    logical :: found(size(expected_names))
    integer :: count_names, index

    call REQUIRE_ASSOCIATED(root,'exact-inventory owner')
    found=.false.
    name=' '
    call LCMNXT(root,name)
    if (name == ' ') call FAIL('exact inventory is empty')
    first_name=name
    count_names=0
    do
      count_names=count_names+1
      if (count_names > size(expected_names)) &
          call FAIL('exact inventory has extras')
      do index=1,size(expected_names)
        if (name == expected_names(index)) exit
      end do
      if (index > size(expected_names) .or. found(index)) &
          call FAIL('exact inventory has an unknown/duplicate entry')
      found(index)=.true.
      call LCMNXT(root,name)
      if (name == first_name) exit
    end do
    if (count_names /= size(expected_names) .or. .not. all(found)) &
        call FAIL('exact inventory is incomplete')
  end subroutine REQUIRE_EXACT


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type
    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        call FAIL(trim(name)//' schema differs')
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_LIST_RECORD(list,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index, expected_length, expected_type
    integer :: length, record_type
    call LCMLEL(list,index,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        call FAIL('list item schema differs')
  end subroutine REQUIRE_LIST_RECORD


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    call REQUIRE_LIST_RECORD(list,index,-1,0)
  end subroutine REQUIRE_DIRECTORY_ITEM


  subroutine REQUIRE_INTEGER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found
    call REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) call FAIL(trim(name)//' value differs')
  end subroutine REQUIRE_INTEGER


  subroutine REQUIRE_CHARACTER12(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    call REQUIRE_CHARACTER_N(root,name,3,12,expected)
  end subroutine REQUIRE_CHARACTER12


  subroutine REQUIRE_CHARACTER_N(root,name,expected_words,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: expected_words, count
    character(len=72) :: found, padded
    call REQUIRE_RECORD(root,name,expected_words,3)
    found=' '
    padded=' '
    padded=expected
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= padded(1:count)) &
        call FAIL(trim(name)//' character value differs')
  end subroutine REQUIRE_CHARACTER_N


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type
    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
        call FAIL(trim(name)//' is unexpectedly present')
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_ASSOCIATED(pointer,label)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: label
    if (.not. c_associated(pointer)) call FAIL(trim(label)//' is absent')
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_DISTINCT(left,right,label)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: label
    call REQUIRE_ASSOCIATED(left,trim(label)//' left')
    call REQUIRE_ASSOCIATED(right,trim(label)//' right')
    if (c_associated(left,right)) call FAIL(trim(label)//' alias')
  end subroutine REQUIRE_DISTINCT


  subroutine OPEN_READ_ONLY(path,root)
    character(len=*), intent(in) :: path
    type(c_ptr), intent(out) :: root
    call LCMOP(root,trim(path),2,2,0)
    call REQUIRE_ASSOCIATED(root,'read-only XSM root')
  end subroutine OPEN_READ_ONLY


  pure elemental integer(int32) function BITS32(value)
    real(real32), intent(in) :: value
    BITS32=transfer(value,0_int32)
  end function BITS32


  pure elemental integer(int64) function BITS64(value)
    real(real64), intent(in) :: value
    BITS64=transfer(value,0_int64)
  end function BITS64


  subroutine FAIL(message)
    character(len=*), intent(in) :: message
    write(*,'(A)') 'B2Y POSTERIOR FAILURE: '//trim(message)
    error stop 'B2Y real close posterior rejected'
  end subroutine FAIL

end program CHECK_B2Y_REAL_CLOSE

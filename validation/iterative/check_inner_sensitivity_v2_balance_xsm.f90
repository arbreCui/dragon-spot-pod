program check_inner_sensitivity_v2_balance_xsm
  ! Independent Ganlib-only replay of the Stage-4v2 axial physics balance.
  !
  !   check_v2_balance TRACK MACROLIB SYSTEM STATE
  !
  ! The checker reconstructs the physical multigroup source from the final
  ! flux and immutable material data.  It does not read SPOT-GBAL records and
  ! does not link or call any SPOT/Dragon production routine.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: ngroup=370
  integer, parameter :: nunknown=1992
  integer, parameter :: nregion=480
  integer, parameter :: nradial=8
  integer, parameter :: nfloor=60
  integer, parameter :: nsnapshot=3
  integer, parameter :: nmixture=24
  integer, parameter :: nfission=32
  integer, parameter :: max_path=72

  character(len=1024) :: path(4)
  type(c_ptr) :: track,macro,system,state
  type(c_ptr) :: fluxes,macro_groups,system_groups
  type(c_ptr) :: macro_group,system_group
  character(len=12) :: signature,track_type
  character(len=96) :: owner
  integer :: track_state(nstate),macro_state(nstate)
  integer :: system_state(nstate),flux_state(nstate)
  integer :: mat(nregion),keyflx(nregion),mat1d(nfloor)
  integer :: rank_root(ngroup)
  integer :: njjs(nmixture,ngroup),ijjs(nmixture,ngroup)
  integer :: ipos(nmixture,ngroup),scat_length(ngroup)
  integer :: arg,g,jg,i,f,r,ibm,ifis,jnd,index0
  integer :: ll4,ll5,nmix,nfis,nmode,nreg_value,nsnap_value
  integer :: found_length,found_type,max_scat
  real(real32) :: volume(nregion),dz(nfloor),area(nradial)
  real(real32) :: volume2d(nradial),keff
  real(real32) :: phi(nunknown,ngroup)
  real(real32) :: tx(0:nmixture,ngroup),s0(0:nmixture,ngroup)
  real(real32) :: radial(nradial,nsnapshot,ngroup)
  real(real32) :: basis(nradial,ngroup)
  real(real32) :: chi(nmixture,nfission,ngroup)
  real(real32) :: nufis(nmixture,nfission,ngroup)
  real(real32), allocatable :: scat(:,:),s0_all(:)
  real(real32) :: qphysical(nregion,ngroup)
  real(real64) :: fission_prod(nregion,nfission)
  real(real64) :: production,source,cell,cell_balance,cell_scale
  real(real64) :: left_current,right_current,cell_integral,axial
  real(real64) :: residual,scale,total_res,total_scale
  real(real64) :: modal_residual(nfloor),modal_scale(nfloor)
  real(real32) :: global_balance,group_balance,galerkin_balance
  real(real32) :: stored_global,stored_group,stored_galerkin
  real(real32) :: ratio,min_scalar
  real(real64) :: expected_volume,volume_bound
  logical :: legacy_anchor

  if ((command_argument_count() /= 4).and. &
      (command_argument_count() /= 5)) call fail( &
    'FOUR XSM ARGUMENTS AND OPTIONAL LEGACY-ANCHOR EXPECTED.')
  do arg=1,4
    call get_command_argument(arg,path(arg))
    if (len_trim(path(arg)) == 0) call fail('EMPTY XSM PATH.')
    if (len_trim(path(arg)) > max_path) &
      call fail('XSM PATH EXCEEDS GANLIB LIMIT.')
  enddo
  legacy_anchor=command_argument_count() == 5
  if (legacy_anchor) then
    call get_command_argument(5,owner)
    if (trim(owner) /= 'LEGACY-ANCHOR') &
      call fail('UNKNOWN OPTIONAL MODE.')
  endif

  call LCMOP(track,trim(path(1)),2,2,0)
  call require_record(track,'SIGNATURE',3,3,'TRACK')
  call require_record(track,'TRACK-TYPE',3,3,'TRACK')
  call LCMGTC(track,'SIGNATURE',12,signature)
  call LCMGTC(track,'TRACK-TYPE',12,track_type)
  if ((signature /= 'L_TRACK').or.(track_type /= 'SPOT')) &
    call fail('SPOT L_TRACK EXPECTED.')
  call require_record(track,'STATE-VECTOR',nstate,1,'TRACK')
  call LCMGET(track,'STATE-VECTOR',track_state)
  ll4=track_state(11)
  ll5=track_state(12)
  if ((track_state(1) /= nregion).or. &
      (track_state(2) /= nunknown).or. &
      (track_state(6) /= nradial).or. &
      (track_state(7) /= nfloor).or. &
      (track_state(8) /= nsnapshot).or. &
      (nregion /= nradial*nfloor).or. &
      (ll5 /= nradial*(nfloor+1)).or. &
      (ll4+ll5 > nunknown)) call fail('TRACK DIMENSIONS CHANGED.')
  call require_record(track,'MATCOD',nregion,1,'TRACK')
  call require_record(track,'KEYFLX',nregion,1,'TRACK')
  call require_record(track,'MAT1D',nfloor,1,'TRACK')
  call require_record(track,'VOLUME',nregion,2,'TRACK')
  call require_record(track,'VOL1D',nfloor,2,'TRACK')
  call require_record(track,'AREA2D',nradial,2,'TRACK')
  call LCMGET(track,'MATCOD',mat)
  call LCMGET(track,'KEYFLX',keyflx)
  call LCMGET(track,'MAT1D',mat1d)
  call LCMGET(track,'VOLUME',volume)
  call LCMGET(track,'VOL1D',dz)
  call LCMGET(track,'AREA2D',area)
  if (any(mat < 1).or.any(mat > nmixture).or. &
      any(keyflx < 1).or.any(keyflx > nunknown).or. &
      any(mat1d < 1).or.any(mat1d > nsnapshot).or. &
      any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0_real32).or. &
      any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0_real32).or. &
      any(.not.ieee_is_finite(area)).or.any(area <= 0.0_real32)) &
    call fail('INVALID TRACK GEOMETRY.')
  do i=1,nradial
    do f=1,nfloor
      r=(i-1)*nfloor+f
      expected_volume=real(area(i),real64)*real(dz(f),real64)
      volume_bound=0.5_real64*real(spacing(volume(r)),real64)
      if (abs(real(volume(r),real64)-expected_volume) > volume_bound) &
        call fail('EXTRUDED VOLUME FAILS HALF-ULP IDENTITY.')
    enddo
  enddo

  call LCMOP(state,trim(path(4)),2,2,0)
  call require_record(state,'SIGNATURE',3,3,'STATE')
  call LCMGTC(state,'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call fail('STATE L_FLUX EXPECTED.')
  call require_record(state,'STATE-VECTOR',nstate,1,'STATE')
  call LCMGET(state,'STATE-VECTOR',flux_state)
  if ((flux_state(1) /= ngroup).or.(flux_state(2) /= nunknown)) &
    call fail('STATE DIMENSIONS CHANGED.')
  call require_record(state,'K-EFFECTIVE',1,2,'STATE')
  call LCMGET(state,'K-EFFECTIVE',keff)
  if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0_real32)) &
    call fail('INVALID K-EFFECTIVE.')
  if (legacy_anchor) then
    call require_record(state,'SPOT-GBAL',1,2,'LEGACY STATE')
    call require_record(state,'SPOT-GBAL-MA',1,2,'LEGACY STATE')
    call require_record(state,'SPOT-MBAL',1,2,'LEGACY STATE')
    call LCMGET(state,'SPOT-GBAL',stored_global)
    call LCMGET(state,'SPOT-GBAL-MA',stored_group)
    call LCMGET(state,'SPOT-MBAL',stored_galerkin)
  endif
  call require_record(state,'FLUX',ngroup,10,'STATE')
  fluxes=LCMGID(state,'FLUX')
  do g=1,ngroup
    write(owner,'(A,I0)') 'STATE FLUX GROUP ',g
    call require_list_item(fluxes,g,nunknown,2,trim(owner))
    call LCMGDL(fluxes,g,phi(:,g))
  enddo
  if (any(.not.ieee_is_finite(phi))) call fail('NON-FINITE RAW FLUX.')
  min_scalar=huge(min_scalar)
  do g=1,ngroup
    do r=1,nregion
      min_scalar=min(min_scalar,phi(keyflx(r),g))
    enddo
  enddo
  if ((.not.ieee_is_finite(min_scalar)).or. &
      (min_scalar <= 0.0_real32)) call fail('NONPOSITIVE SCALAR FLUX.')

  call LCMOP(macro,trim(path(2)),2,2,0)
  call require_record(macro,'SIGNATURE',3,3,'MACROLIB')
  call LCMGTC(macro,'SIGNATURE',12,signature)
  if (signature /= 'L_MACROLIB') call fail('L_MACROLIB EXPECTED.')
  call require_record(macro,'STATE-VECTOR',nstate,1,'MACROLIB')
  call LCMGET(macro,'STATE-VECTOR',macro_state)
  nmix=macro_state(2)
  nfis=macro_state(4)
  if ((macro_state(1) /= ngroup).or.(nmix /= nmixture).or. &
      (nfis /= nfission)) call fail('MACROLIB DIMENSIONS CHANGED.')
  call require_record(macro,'GROUP',ngroup,10,'MACROLIB')
  macro_groups=LCMGID(macro,'GROUP')
  max_scat=0
  do g=1,ngroup
    call require_directory_item(macro_groups,g,'MACROLIB GROUP')
    macro_group=LCMGIL(macro_groups,g)
    call LCMLEN(macro_group,'SCAT00',found_length,found_type)
    if ((found_length <= 0).or.(found_type /= 2)) &
      call fail('INVALID SCAT00 RECORD.')
    scat_length(g)=found_length
    max_scat=max(max_scat,found_length)
  enddo
  allocate(scat(max_scat,ngroup))
  scat=0.0_real32
  do g=1,ngroup
    write(owner,'(A,I0)') 'MACROLIB GROUP ',g
    macro_group=LCMGIL(macro_groups,g)
    call require_record(macro_group,'CHI',nmix*nfis,2,trim(owner))
    call require_record(macro_group,'NUSIGF',nmix*nfis,2,trim(owner))
    call require_record(macro_group,'NJJS00',nmix,1,trim(owner))
    call require_record(macro_group,'IJJS00',nmix,1,trim(owner))
    call require_record(macro_group,'IPOS00',nmix,1,trim(owner))
    call LCMGET(macro_group,'CHI',chi(:,:,g))
    call LCMGET(macro_group,'NUSIGF',nufis(:,:,g))
    call LCMGET(macro_group,'NJJS00',njjs(:,g))
    call LCMGET(macro_group,'IJJS00',ijjs(:,g))
    call LCMGET(macro_group,'IPOS00',ipos(:,g))
    call LCMGET(macro_group,'SCAT00',scat(1:scat_length(g),g))
  enddo
  if (any(.not.ieee_is_finite(chi)).or. &
      any(.not.ieee_is_finite(nufis)).or. &
      any(.not.ieee_is_finite(scat))) call fail('NON-FINITE MACROLIB.')

  call LCMOP(system,trim(path(3)),2,2,0)
  call require_record(system,'SIGNATURE',3,3,'SYSTEM')
  call LCMGTC(system,'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call fail('SYSTEM L_PIJ EXPECTED.')
  call require_record(system,'STATE-VECTOR',nstate,1,'SYSTEM')
  call LCMGET(system,'STATE-VECTOR',system_state)
  if ((system_state(8) /= ngroup).or. &
      (system_state(9) /= nunknown).or. &
      (system_state(10) /= nmix).or.(system_state(14) /= 1)) &
    call fail('SYSTEM DIMENSIONS OR RANK CHANGED.')
  call require_record(system,'POD-RANK-G',ngroup,1,'SYSTEM')
  call LCMGET(system,'POD-RANK-G',rank_root)
  if (any(rank_root /= 1)) call fail('SYSTEM IS NOT RANK ONE.')
  call require_record(system,'GROUP',ngroup,10,'SYSTEM')
  system_groups=LCMGID(system,'GROUP')
  do g=1,ngroup
    write(owner,'(A,I0)') 'SYSTEM GROUP ',g
    call require_directory_item(system_groups,g,trim(owner))
    system_group=LCMGIL(system_groups,g)
    call require_record(system_group,'DRAGON-TXSC',nmix+1,2,trim(owner))
    call LCMLEN(system_group,'DRAGON-S0XSC', &
      found_length,found_type)
    if ((found_length < nmix+1).or.(found_type /= 2).or. &
        (mod(found_length,nmix+1) /= 0)) call fail('INVALID SYSTEM S0.')
    allocate(s0_all(found_length))
    call LCMGET(system_group,'DRAGON-TXSC',tx(:,g))
    call LCMGET(system_group,'DRAGON-S0XSC',s0_all)
    s0(:,g)=s0_all(1:nmix+1)
    deallocate(s0_all)
    call require_record(system_group,'NREG2D',1,1,trim(owner))
    call require_record(system_group,'NSNAP',1,1,trim(owner))
    call require_record(system_group,'POD-NMODE',1,1,trim(owner))
    call LCMGET(system_group,'NREG2D',nreg_value)
    call LCMGET(system_group,'NSNAP',nsnap_value)
    call LCMGET(system_group,'POD-NMODE',nmode)
    if ((nreg_value /= nradial).or.(nsnap_value /= nsnapshot).or. &
        (nmode /= 1)) call fail('INVALID SYSTEM POD DIMENSIONS.')
    call require_record(system_group,'VOL2D',nradial,2,trim(owner))
    call require_record(system_group,'RADIAL-OP', &
      nradial*nsnapshot,2,trim(owner))
    call require_record(system_group,'POD-BASIS',nradial,2,trim(owner))
    call LCMGET(system_group,'VOL2D',volume2d)
    call LCMGET(system_group,'RADIAL-OP',radial(:,:,g))
    call LCMGET(system_group,'POD-BASIS',basis(:,g))
    if (any(real32_bits(volume2d) /= real32_bits(area))) &
      call fail('VOL2D AND AREA2D DIFFER BITWISE.')
  enddo
  if (any(.not.ieee_is_finite(tx)).or. &
      any(.not.ieee_is_finite(s0)).or. &
      any(.not.ieee_is_finite(radial)).or. &
      any(.not.ieee_is_finite(basis))) call fail('NON-FINITE SYSTEM DATA.')

  fission_prod=0.0_real64
  do r=1,nregion
    ibm=mat(r)
    do ifis=1,nfis
      production=0.0_real64
      do jg=1,ngroup
        production=production+ &
          real(nufis(ibm,ifis,jg),real64)* &
          real(phi(keyflx(r),jg),real64)
      enddo
      fission_prod(r,ifis)=production
    enddo
  enddo
  qphysical=0.0_real32
  do g=1,ngroup
    do r=1,nregion
      ibm=mat(r)
      source=0.0_real64
      do ifis=1,nfis
        source=source+real(chi(ibm,ifis,g),real64)* &
          fission_prod(r,ifis)/real(keff,real64)
      enddo
      if (njjs(ibm,g) < 0) call fail('NEGATIVE NJJS00.')
      jg=ijjs(ibm,g)
      do jnd=1,njjs(ibm,g)
        index0=ipos(ibm,g)+jnd-1
        if ((jg < 1).or.(jg > ngroup).or.(index0 < 1).or. &
            (index0 > scat_length(g))) call fail('SCATTER MAP OVERFLOW.')
        if (jg /= g) source=source+ &
          real(scat(index0,g),real64)*real(phi(keyflx(r),jg),real64)
        jg=jg-1
      enddo
      qphysical(r,g)=real(source,real32)
    enddo
  enddo
  if (any(.not.ieee_is_finite(fission_prod)).or. &
      any(.not.ieee_is_finite(qphysical))) &
    call fail('NON-FINITE REBUILT PHYSICAL SOURCE.')

  total_res=0.0_real64
  total_scale=0.0_real64
  group_balance=0.0_real32
  galerkin_balance=0.0_real32
  do g=1,ngroup
    cell_integral=0.0_real64
    scale=0.0_real64
    modal_residual=0.0_real64
    modal_scale=0.0_real64
    do i=1,nradial
      do f=1,nfloor
        r=(i-1)*nfloor+f
        ibm=mat(r)
        cell=(real(tx(ibm,g),real64)-real(s0(ibm,g),real64)+ &
          real(radial(i,mat1d(f),g),real64))* &
          real(phi(keyflx(r),g),real64)-real(qphysical(r,g),real64)
        left_current=real( &
          phi(ll4+(i-1)*(nfloor+1)+f,g),real64)
        right_current=real( &
          phi(ll4+(i-1)*(nfloor+1)+f+1,g),real64)
        cell_balance=real(volume(r),real64)*cell+ &
          real(area(i),real64)*(right_current-left_current)
        cell_scale=real(volume(r),real64)*( &
          abs(real(tx(ibm,g),real64)*real(phi(keyflx(r),g),real64))+ &
          abs(real(s0(ibm,g),real64)*real(phi(keyflx(r),g),real64))+ &
          abs(real(radial(i,mat1d(f),g),real64)* &
          real(phi(keyflx(r),g),real64))+ &
          abs(real(qphysical(r,g),real64)))+ &
          real(area(i),real64)*(abs(left_current)+abs(right_current))
        modal_residual(f)=modal_residual(f)+ &
          real(basis(i,g),real64)*cell_balance
        modal_scale(f)=modal_scale(f)+ &
          abs(real(basis(i,g),real64))*cell_scale
        cell_integral=cell_integral+real(volume(r),real64)*cell
        scale=scale+real(volume(r),real64)*( &
          abs(real(tx(ibm,g),real64)*real(phi(keyflx(r),g),real64))+ &
          abs(real(s0(ibm,g),real64)*real(phi(keyflx(r),g),real64))+ &
          abs(real(radial(i,mat1d(f),g),real64)* &
          real(phi(keyflx(r),g),real64))+ &
          abs(real(qphysical(r,g),real64)))
      enddo
    enddo
    axial=0.0_real64
    do i=1,nradial
      axial=axial+real(area(i),real64)*( &
        real(phi(ll4+(i-1)*(nfloor+1)+nfloor+1,g),real64)- &
        real(phi(ll4+(i-1)*(nfloor+1)+1,g),real64))
    enddo
    residual=cell_integral+axial
    scale=scale+abs(axial)
    if ((.not.ieee_is_finite(residual)).or. &
        (.not.ieee_is_finite(scale)).or.(scale <= 0.0_real64)) &
      call fail('INVALID GROUP BALANCE.')
    ratio=real(abs(residual)/scale,real32)
    group_balance=max(group_balance,ratio)
    total_res=total_res+residual
    total_scale=total_scale+scale
    do f=1,nfloor
      if (modal_scale(f) > 0.0_real64) then
        ratio=real(abs(modal_residual(f))/modal_scale(f),real32)
      else if (modal_residual(f) == 0.0_real64) then
        ratio=0.0_real32
      else
        call fail('ZERO GALERKIN SCALE WITH NONZERO RESIDUAL.')
      endif
      galerkin_balance=max(galerkin_balance,ratio)
    enddo
  enddo
  if ((.not.ieee_is_finite(total_res)).or. &
      (.not.ieee_is_finite(total_scale)).or.(total_scale <= 0.0_real64)) &
    call fail('INVALID GLOBAL BALANCE.')
  global_balance=real(abs(total_res)/total_scale,real32)
  if ((.not.ieee_is_finite(global_balance)).or. &
      (.not.ieee_is_finite(group_balance)).or. &
      (.not.ieee_is_finite(galerkin_balance)).or. &
      btest(real32_bits(global_balance),31).or. &
      btest(real32_bits(group_balance),31).or. &
      btest(real32_bits(galerkin_balance),31)) &
    call fail('INVALID NORMALIZED BALANCE DIAGNOSTIC.')
  if (legacy_anchor) then
    if ((real32_bits(global_balance) /= real32_bits(stored_global)).or. &
        (real32_bits(group_balance) /= real32_bits(stored_group)).or. &
        (real32_bits(galerkin_balance) /= real32_bits(stored_galerkin))) &
      call fail('LEGACY BALANCE ANCHOR DIFFERS BITWISE.')
  endif

  write(6,'(A,1X,Z8.8)') &
    'INNER-SENSITIVITY-V2 POSITIVE-SCALAR MIN-BITS', &
    real32_bits(min_scalar)
  write(6,'(A)') 'INNER-SENSITIVITY-V2 PHYSICAL-SOURCE REBUILT'
  write(6,'(A,3(1X,Z8.8))') &
    'INNER-SENSITIVITY-V2 BALANCE GLOBAL/GROUP/GALERKIN-BITS', &
    real32_bits(global_balance),real32_bits(group_balance), &
    real32_bits(galerkin_balance)
  if (legacy_anchor) &
    write(6,'(A)') 'INNER-SENSITIVITY-V2 LEGACY-ANCHOR BITWISE PASS'
  write(6,'(A)') 'INNER-SENSITIVITY-V2 BALANCE-XSM COMPLETE'

  deallocate(scat)
  call LCMCL(system,1)
  call LCMCL(macro,1)
  call LCMCL(state,1)
  call LCMCL(track,1)

contains

  subroutine require_record(ptr,name,length_expected,type_expected,owner0)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner0
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner0)//' INVALID RECORD', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('RECORD CONTRACT FAILURE.')
    endif
  end subroutine require_record


  subroutine require_directory_item(list_ptr,index0,owner0)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner0
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= -1).or.(type_found /= 0)) &
      call fail(trim(owner0)//' IS NOT A DIRECTORY.')
  end subroutine require_directory_item


  subroutine require_list_item(list_ptr,index0,length_expected, &
      type_expected,owner0)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: owner0
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) call fail( &
        trim(owner0)//' HAS INVALID LIST ITEM.')
  end subroutine require_list_item


  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'INNER-SENSITIVITY-V2 BALANCE-XSM ERROR: '// &
      trim(message)
    error stop 2
  end subroutine fail

end program check_inner_sensitivity_v2_balance_xsm

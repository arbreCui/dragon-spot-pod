!DECK SPOGBAL
subroutine SPOGBAL(nentry,hentry,ientry,jentry,kentry)
  ! Audit the volume-integrated multigroup SPOT transport balance.
  use GANLIB
  use SPOT_LEAKAGE, only : SPOF00,SPOQ00
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate),isystem(nstate)
  integer :: ngrp,nunk,nreg,nreg2d,nfloor,nsnap,nmix,nfis,ll4,ll5,nmode
  integer :: igr,i,ifloor,ireg,isnap,ibm,iunk,ilong,itylcm
  integer :: nnonpositive,worst_group,worst_region,group_min_region
  integer :: global_min_group,global_min_region,dominant_negative_group
  integer :: max_negative_abs_group,max_negative_abs_region
  integer :: max_negative_rel_group,max_negative_rel_region
  integer :: worst_balance_group
  integer :: max_abs_balance_group
  integer :: a,modal_worst_group,modal_worst_mode,modal_worst_floor
  integer :: nscat
  integer :: indic,nitma
  integer :: imacro(nstate)
  integer, allocatable :: mat(:),keyflx(:),mat1d(:)
  integer, allocatable :: njjs(:),ijjs(:),ipos(:)
  real, allocatable :: volume(:),dz(:),area(:),phi(:)
  real, allocatable :: phi_all(:,:),regflux(:,:),qfinal(:)
  double precision, allocatable :: fisprod(:,:)
  real, allocatable :: chi(:,:),nusigf(:,:,:),scat(:)
  real, allocatable :: tx(:),s0all(:),radial(:,:),basis(:,:)
  real :: group_max,global_res,flott,global_phi_min,global_phi_max
  real :: group_phi_min,group_phi_scale,worst_ratio,ratio,signed_group
  real :: worst_balance_signed,worst_balance_weight
  real :: max_abs_balance_norm,sum_abs_balance_norm
  real :: negative_mass_fraction,worst_group_mass_fraction
  real :: worst_group_negative_fraction
  real :: dominant_negative_mass_fraction
  real :: dominant_negative_group_weight,dominant_negative_group_fraction
  real :: max_negative_cell_abs_norm,max_negative_cell_relative
  real :: global_min_cell_relative
  real :: telescope_error_norm
  real :: modal_max,modal_ratio,modal_worst_signed
  real :: keff
  double precision :: residual,scale,axial,cell,total_res,total_scale
  double precision :: cell_integral,worst_cell_integral,worst_axial
  double precision :: worst_balance_scale
  double precision :: max_abs_balance_residual,max_abs_balance_scale
  double precision :: sum_abs_balance_residual
  double precision :: total_phi_mass,negative_phi_mass,group_phi_mass
  double precision :: group_negative_mass,worst_phi_mass,worst_phi_negative
  double precision :: worst_min_contribution
  double precision :: dominant_negative_mass,dominant_negative_group_mass
  double precision :: cell_balance,cell_balance_scale,left_current,right_current
  double precision :: cell_balance_sum,telescope_error_sum
  double precision :: max_negative_cell_abs
  double precision :: global_min_cell_residual,global_min_cell_scale
  double precision, allocatable :: modal_residual(:,:),modal_scale(:,:)
  double precision :: dflott,expected_volume,volume_bound
  character(len=4) :: text4
  character(len=12) :: signature,track_type
  type(c_ptr) :: jpflux,jpsystem,kpsystem,jpmacro,kpmacro

  if (nentry /= 4) call XABORT('SPOGBAL: FOUR ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOGBAL: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 1).or.any(jentry(2:4) /= 2)) &
    call XABORT('SPOGBAL: MODIFIABLE FLUX AND THREE INPUTS EXPECTED.')
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') &
    call XABORT('SPOGBAL: INVALID FLUX '//trim(hentry(1))//'.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPOGBAL: L_TRACK EXPECTED.')
  call LCMGTC(kentry(2),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') call XABORT('SPOGBAL: SPOT TRACK EXPECTED.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call XABORT('SPOGBAL: L_PIJ EXPECTED.')
  call LCMGTC(kentry(4),'SIGNATURE',12,signature)
  if (signature /= 'L_MACROLIB') &
    call XABORT('SPOGBAL: L_MACROLIB EXPECTED.')

  call LCMGET(kentry(1),'STATE-VECTOR',iflux)
  call LCMGET(kentry(2),'STATE-VECTOR',itrack)
  call LCMGET(kentry(3),'STATE-VECTOR',isystem)
  call LCMGET(kentry(4),'STATE-VECTOR',imacro)
  ngrp=iflux(1)
  nunk=iflux(2)
  nreg=itrack(1)
  nreg2d=itrack(6)
  nfloor=itrack(7)
  nsnap=itrack(8)
  ll4=itrack(11)
  ll5=itrack(12)
  nmix=isystem(10)
  nfis=imacro(4)
  if ((ngrp /= isystem(8)).or.(nunk /= itrack(2)).or. &
      (nunk /= isystem(9)).or.(nreg /= nreg2d*nfloor).or. &
      (ll5 /= nreg2d*(nfloor+1)).or.(ll4+ll5 > nunk).or. &
      (ngrp /= imacro(1)).or.(nmix /= imacro(2)).or. &
      (nmix <= 0).or.(nfis <= 0).or.(nsnap <= 0)) &
    call XABORT('SPOGBAL: INCONSISTENT DIMENSIONS.')
  allocate(mat(nreg),keyflx(nreg),mat1d(nfloor))
  allocate(volume(nreg),dz(nfloor),area(nreg2d),phi(nunk))
  allocate(phi_all(nunk,ngrp),regflux(nreg,ngrp),qfinal(nreg))
  allocate(fisprod(nreg,nfis))
  allocate(chi(nmix,nfis),nusigf(nmix,nfis,ngrp))
  allocate(njjs(nmix),ijjs(nmix),ipos(nmix))
  allocate(tx(0:nmix))
  call LCMLEN(kentry(2),'AREA2D',ilong,itylcm)
  if ((ilong /= nreg2d).or.(itylcm /= 2)) &
    call XABORT('SPOGBAL: INVALID AREA2D RECORD.')
  call LCMGET(kentry(2),'MATCOD',mat)
  call LCMGET(kentry(2),'KEYFLX',keyflx)
  call LCMGET(kentry(2),'MAT1D',mat1d)
  call LCMGET(kentry(2),'VOLUME',volume)
  call LCMGET(kentry(2),'VOL1D',dz)
  call LCMGET(kentry(2),'AREA2D',area)
  if (any(mat1d < 1).or.any(mat1d > nsnap)) &
    call XABORT('SPOGBAL: INVALID FLOOR MAP.')
  if (any(.not.ieee_is_finite(area)).or.any(area <= 0.0)) &
    call XABORT('SPOGBAL: NON-FINITE OR NONPOSITIVE AREA2D.')
  if (any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0).or. &
      any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0)) &
    call XABORT('SPOGBAL: INVALID EXTRUDED GEOMETRY.')
  do i=1,nreg2d
    do ifloor=1,nfloor
      ireg=(i-1)*nfloor+ifloor
      expected_volume=dble(area(i))*dble(dz(ifloor))
      volume_bound=0.5d0*dble(spacing(volume(ireg)))
      if (abs(dble(volume(ireg))-expected_volume) > volume_bound) &
        call XABORT('SPOGBAL: INCONSISTENT EXTRUDED VOLUME.')
    enddo
  enddo

  jpflux=LCMGID(kentry(1),'FLUX')
  jpsystem=LCMGID(kentry(3),'GROUP')
  jpmacro=LCMGID(kentry(4),'GROUP')
  call LCMLEN(kentry(1),'K-EFFECTIVE',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 2)) &
    call XABORT('SPOGBAL: INVALID FINAL EIGENVALUE RECORD.')
  call LCMGET(kentry(1),'K-EFFECTIVE',keff)
  if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0)) &
    call XABORT('SPOGBAL: INVALID FINAL EIGENVALUE.')
  do igr=1,ngrp
    call LCMGDL(jpflux,igr,phi_all(1,igr))
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'NUSIGF',ilong,itylcm)
    if ((ilong /= nmix*nfis).or.(itylcm /= 2)) &
      call XABORT('SPOGBAL: INVALID NUSIGF RECORD.')
    call LCMGET(kpmacro,'NUSIGF',nusigf(1,1,igr))
  enddo
  regflux=0.0
  do ireg=1,nreg
    iunk=keyflx(ireg)
    if ((mat(ireg) <= 0).or.(iunk <= 0)) cycle
    if (iunk > nunk) call XABORT('SPOGBAL: FLUX KEY OVERFLOW.')
    regflux(ireg,:)=phi_all(iunk,:)
  enddo
  call SPOF00(nreg,ngrp,nmix,nfis,mat,regflux,nusigf,fisprod)
  group_max=0.0
  total_res=0.0d0
  total_scale=0.0d0
  global_phi_min=huge(global_phi_min)
  global_phi_max=-huge(global_phi_max)
  global_min_group=0
  global_min_region=0
  worst_ratio=huge(worst_ratio)
  nnonpositive=0
  worst_group=0
  worst_region=0
  total_phi_mass=0.0d0
  negative_phi_mass=0.0d0
  worst_phi_mass=0.0d0
  worst_phi_negative=0.0d0
  worst_min_contribution=0.0d0
  dominant_negative_group=0
  dominant_negative_mass=0.0d0
  dominant_negative_group_mass=0.0d0
  max_negative_abs_group=0
  max_negative_abs_region=0
  max_negative_rel_group=0
  max_negative_rel_region=0
  max_negative_cell_abs=0.0d0
  max_negative_cell_relative=0.0
  global_min_cell_residual=0.0d0
  global_min_cell_scale=-1.0d0
  worst_balance_group=0
  worst_balance_signed=0.0
  worst_cell_integral=0.0d0
  worst_axial=0.0d0
  worst_balance_scale=0.0d0
  max_abs_balance_group=0
  max_abs_balance_residual=0.0d0
  max_abs_balance_scale=0.0d0
  sum_abs_balance_residual=0.0d0
  telescope_error_sum=0.0d0
  modal_max=0.0
  modal_worst_signed=0.0
  modal_worst_group=0
  modal_worst_mode=0
  modal_worst_floor=0
  modal_ratio=0.0
  do igr=1,ngrp
    phi=phi_all(:,igr)
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'CHI',ilong,itylcm)
    if ((ilong /= nmix*nfis).or.(itylcm /= 2)) &
      call XABORT('SPOGBAL: INVALID CHI RECORD.')
    call LCMGET(kpmacro,'CHI',chi)
    call LCMLEN(kpmacro,'NJJS00',ilong,itylcm)
    if ((ilong /= nmix).or.(itylcm /= 1)) &
      call XABORT('SPOGBAL: INVALID NJJS00 RECORD.')
    call LCMGET(kpmacro,'NJJS00',njjs)
    call LCMLEN(kpmacro,'IJJS00',ilong,itylcm)
    if ((ilong /= nmix).or.(itylcm /= 1)) &
      call XABORT('SPOGBAL: INVALID IJJS00 RECORD.')
    call LCMGET(kpmacro,'IJJS00',ijjs)
    call LCMLEN(kpmacro,'IPOS00',ilong,itylcm)
    if ((ilong /= nmix).or.(itylcm /= 1)) &
      call XABORT('SPOGBAL: INVALID IPOS00 RECORD.')
    call LCMGET(kpmacro,'IPOS00',ipos)
    call LCMLEN(kpmacro,'SCAT00',nscat,itylcm)
    if ((nscat <= 0).or.(itylcm /= 2)) &
      call XABORT('SPOGBAL: INVALID SCAT00 RECORD.')
    allocate(scat(nscat))
    call LCMGET(kpmacro,'SCAT00',scat)
    call SPOQ00(nreg,ngrp,nmix,nfis,igr,mat,regflux,keff, &
      njjs,ijjs,ipos,scat,chi,nusigf,qfinal,fisprod)
    deallocate(scat)
    group_phi_min=huge(group_phi_min)
    group_phi_scale=0.0
    group_min_region=0
    group_phi_mass=0.0d0
    group_negative_mass=0.0d0
    do ireg=1,nreg
      iunk=keyflx(ireg)
      if ((mat(ireg) <= 0).or.(iunk <= 0)) cycle
      if (phi(iunk) < group_phi_min) then
        group_phi_min=phi(iunk)
        group_min_region=ireg
      endif
      group_phi_scale=max(group_phi_scale,abs(phi(iunk)))
      if (phi(iunk) < global_phi_min) then
        global_phi_min=phi(iunk)
        global_min_group=igr
        global_min_region=ireg
      endif
      global_phi_max=max(global_phi_max,phi(iunk))
      group_phi_mass=group_phi_mass+dble(volume(ireg))* &
        abs(dble(phi(iunk)))
      if (phi(iunk) <= 0.0) then
        nnonpositive=nnonpositive+1
        group_negative_mass=group_negative_mass+dble(volume(ireg))* &
          abs(dble(phi(iunk)))
      endif
    enddo
    total_phi_mass=total_phi_mass+group_phi_mass
    negative_phi_mass=negative_phi_mass+group_negative_mass
    if ((dominant_negative_group == 0).or. &
        (group_negative_mass > dominant_negative_mass)) then
      dominant_negative_group=igr
      dominant_negative_mass=group_negative_mass
      dominant_negative_group_mass=group_phi_mass
    endif
    if (group_phi_scale <= 0.0.or.group_min_region == 0) &
      call XABORT('SPOGBAL: INVALID GROUP FLUX SCALE.')
    ratio=group_phi_min/group_phi_scale
    if (ratio < worst_ratio) then
      worst_ratio=ratio
      worst_group=igr
      worst_region=group_min_region
      worst_phi_mass=group_phi_mass
      worst_phi_negative=group_negative_mass
      worst_min_contribution=dble(volume(group_min_region))* &
        abs(dble(phi(keyflx(group_min_region))))
    endif
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMLEN(kpsystem,'DRAGON-TXSC',ilong,itylcm)
    if ((ilong /= nmix+1).or.(itylcm /= 2)) &
      call XABORT('SPOGBAL: INVALID TXSC RECORD.')
    call LCMGET(kpsystem,'DRAGON-TXSC',tx)
    call LCMLEN(kpsystem,'DRAGON-S0XSC',ilong,itylcm)
    if ((itylcm /= 2).or.(ilong < nmix+1).or. &
        (mod(ilong,nmix+1) /= 0)) &
      call XABORT('SPOGBAL: INVALID S0 LENGTH.')
    call LCMGET(kpsystem,'POD-NMODE',nmode)
    if ((nmode <= 0).or.(nmode > nreg2d)) &
      call XABORT('SPOGBAL: INVALID POD MODE COUNT.')
    allocate(s0all(ilong),radial(nreg2d,nsnap),basis(nreg2d,nmode))
    allocate(modal_residual(nmode,nfloor),modal_scale(nmode,nfloor))
    call LCMGET(kpsystem,'DRAGON-S0XSC',s0all)
    call LCMLEN(kpsystem,'RADIAL-OP',ilong,itylcm)
    if (ilong /= nreg2d*nsnap) &
      call XABORT('SPOGBAL: INVALID RADIAL OPERATOR.')
    call LCMGET(kpsystem,'RADIAL-OP',radial)
    call LCMLEN(kpsystem,'POD-BASIS',ilong,itylcm)
    if (ilong /= nreg2d*nmode) &
      call XABORT('SPOGBAL: INVALID POD BASIS.')
    call LCMGET(kpsystem,'POD-BASIS',basis)

    residual=0.0d0
    scale=0.0d0
    cell_balance_sum=0.0d0
    modal_residual=0.0d0
    modal_scale=0.0d0
    do i=1,nreg2d
      do ifloor=1,nfloor
        ireg=(i-1)*nfloor+ifloor
        ibm=mat(ireg)
        iunk=keyflx(ireg)
        isnap=mat1d(ifloor)
        if ((ibm <= 0).or.(iunk <= 0)) cycle
        cell=(dble(tx(ibm))-dble(s0all(ibm+1))+ &
          dble(radial(i,isnap)))*dble(phi(iunk))-dble(qfinal(ireg))
        left_current=dble(phi(ll4+(i-1)*(nfloor+1)+ifloor))
        right_current=dble(phi(ll4+(i-1)*(nfloor+1)+ifloor+1))
        cell_balance=dble(volume(ireg))*cell+dble(area(i))* &
          (right_current-left_current)
        cell_balance_scale=dble(volume(ireg))*( &
          abs(dble(tx(ibm))*dble(phi(iunk)))+ &
          abs(dble(s0all(ibm+1))*dble(phi(iunk)))+ &
          abs(dble(radial(i,isnap))*dble(phi(iunk)))+ &
          abs(dble(qfinal(ireg))))+dble(area(i))* &
          (abs(left_current)+abs(right_current))
        do a=1,nmode
          modal_residual(a,ifloor)=modal_residual(a,ifloor)+ &
            dble(basis(i,a))*cell_balance
          modal_scale(a,ifloor)=modal_scale(a,ifloor)+ &
            abs(dble(basis(i,a)))*cell_balance_scale
        enddo
        if (phi(iunk) <= 0.0) then
          if ((max_negative_abs_group == 0).or. &
              (abs(cell_balance) > max_negative_cell_abs)) then
            max_negative_cell_abs=abs(cell_balance)
            max_negative_abs_group=igr
            max_negative_abs_region=ireg
          endif
          if (cell_balance_scale > 0.0d0) then
            ratio=real(abs(cell_balance)/cell_balance_scale)
            if ((max_negative_rel_group == 0).or. &
                (ratio > max_negative_cell_relative)) then
              max_negative_cell_relative=ratio
              max_negative_rel_group=igr
              max_negative_rel_region=ireg
            endif
          endif
        endif
        if ((igr == global_min_group).and. &
            (ireg == global_min_region)) then
          global_min_cell_residual=cell_balance
          global_min_cell_scale=cell_balance_scale
        endif
        cell_balance_sum=cell_balance_sum+cell_balance
        residual=residual+dble(volume(ireg))*cell
        scale=scale+dble(volume(ireg))*( &
          abs(dble(tx(ibm))*dble(phi(iunk)))+ &
          abs(dble(s0all(ibm+1))*dble(phi(iunk)))+ &
          abs(dble(radial(i,isnap))*dble(phi(iunk)))+ &
          abs(dble(qfinal(ireg))))
      enddo
    enddo
    cell_integral=residual
    axial=0.0d0
    do i=1,nreg2d
      axial=axial+dble(area(i))*( &
        dble(phi(ll4+(i-1)*(nfloor+1)+nfloor+1))- &
        dble(phi(ll4+(i-1)*(nfloor+1)+1)))
    enddo
    residual=residual+axial
    telescope_error_sum=telescope_error_sum+abs(cell_balance_sum-residual)
    scale=scale+abs(axial)
    if (scale > 0.0d0) then
      signed_group=real(residual/scale)
      if ((worst_balance_group == 0).or. &
          (abs(signed_group) > group_max)) then
        group_max=abs(signed_group)
        worst_balance_group=igr
        worst_balance_signed=signed_group
        worst_cell_integral=cell_integral
        worst_axial=axial
        worst_balance_scale=scale
      endif
      if ((max_abs_balance_group == 0).or. &
          (abs(residual) > max_abs_balance_residual)) then
        max_abs_balance_group=igr
        max_abs_balance_residual=abs(residual)
        max_abs_balance_scale=scale
      endif
    endif
    total_res=total_res+residual
    total_scale=total_scale+scale
    sum_abs_balance_residual=sum_abs_balance_residual+abs(residual)
    do ifloor=1,nfloor
      do a=1,nmode
        if (modal_scale(a,ifloor) > 0.0d0) then
          modal_ratio=real(abs(modal_residual(a,ifloor))/ &
            modal_scale(a,ifloor))
        else if (modal_residual(a,ifloor) == 0.0d0) then
          modal_ratio=0.0
        else
          call XABORT('SPOGBAL: ZERO GALERKIN BALANCE SCALE.')
        endif
        if ((modal_worst_group == 0).or.(modal_ratio > modal_max)) then
          modal_max=modal_ratio
          modal_worst_group=igr
          modal_worst_mode=a
          modal_worst_floor=ifloor
          if (modal_scale(a,ifloor) > 0.0d0) then
            modal_worst_signed=real(modal_residual(a,ifloor)/ &
              modal_scale(a,ifloor))
          else
            modal_worst_signed=0.0
          endif
        endif
      enddo
    enddo
    deallocate(modal_scale,modal_residual,basis,radial,s0all)
  enddo
  if (total_scale <= 0.0d0) call XABORT('SPOGBAL: ZERO BALANCE SCALE.')
  if (total_phi_mass <= 0.0d0) call XABORT('SPOGBAL: ZERO FLUX MASS.')
  if ((global_min_group <= 0).or.(global_min_region <= 0)) &
    call XABORT('SPOGBAL: GLOBAL FLUX MINIMUM WAS NOT LOCATED.')
  if (global_min_cell_scale < 0.0d0) &
    call XABORT('SPOGBAL: GLOBAL-MINIMUM CELL WAS NOT AUDITED.')
  if (worst_phi_mass < worst_min_contribution) &
    call XABORT('SPOGBAL: INCONSISTENT WORST-GROUP FLUX MASS.')
  if (dominant_negative_group_mass < dominant_negative_mass) &
    call XABORT('SPOGBAL: INCONSISTENT NEGATIVE-GROUP FLUX MASS.')
  global_res=real(abs(total_res)/total_scale)
  worst_balance_weight=real(worst_balance_scale/total_scale)
  max_abs_balance_norm=real(max_abs_balance_residual/total_scale)
  sum_abs_balance_norm=real(sum_abs_balance_residual/total_scale)
  telescope_error_norm=real(telescope_error_sum/total_scale)
  max_negative_cell_abs_norm=real(max_negative_cell_abs/total_scale)
  if (global_min_cell_scale > 0.0d0) then
    global_min_cell_relative= &
      real(abs(global_min_cell_residual)/global_min_cell_scale)
  else
    global_min_cell_relative=0.0
  endif
  negative_mass_fraction=real(negative_phi_mass/total_phi_mass)
  worst_group_mass_fraction=real(worst_phi_mass/total_phi_mass)
  if (worst_phi_mass > 0.0d0) then
    worst_group_negative_fraction=real(worst_phi_negative/worst_phi_mass)
  else
    worst_group_negative_fraction=0.0
  endif
  dominant_negative_mass_fraction=real(dominant_negative_mass/total_phi_mass)
  dominant_negative_group_weight= &
    real(dominant_negative_group_mass/total_phi_mass)
  if (dominant_negative_group_mass > 0.0d0) then
    dominant_negative_group_fraction= &
      real(dominant_negative_mass/dominant_negative_group_mass)
  else
    dominant_negative_group_fraction=0.0
  endif
  if (.not.ieee_is_finite(group_max).or. &
      .not.ieee_is_finite(global_res).or. &
      .not.ieee_is_finite(modal_max)) &
    call XABORT('SPOGBAL: NON-FINITE BALANCE.')
  call LCMPUT(kentry(1),'SPOT-GBAL',1,2,global_res)
  call LCMPUT(kentry(1),'SPOT-GBAL-MAX',1,2,group_max)
  call LCMPUT(kentry(1),'SPOT-GB-GRP',1,1,worst_balance_group)
  call LCMPUT(kentry(1),'SPOT-GB-ABS',1,2,max_abs_balance_norm)
  call LCMPUT(kentry(1),'SPOT-GB-AGRP',1,1,max_abs_balance_group)
  call LCMPUT(kentry(1),'SPOT-GB-SUM',1,2,sum_abs_balance_norm)
  call LCMPUT(kentry(1),'SPOT-GB-TEL',1,2,telescope_error_norm)
  call LCMPUT(kentry(1),'SPOT-MBAL',1,2,modal_max)
  call LCMPUT(kentry(1),'SPOT-MB-GRP',1,1,modal_worst_group)
  call LCMPUT(kentry(1),'SPOT-MB-MOD',1,1,modal_worst_mode)
  call LCMPUT(kentry(1),'SPOT-MB-FLR',1,1,modal_worst_floor)
  call LCMPUT(kentry(1),'SPOT-PHI-MIN',1,2,global_phi_min)
  call LCMPUT(kentry(1),'SPOT-PHI-MAX',1,2,global_phi_max)
  call LCMPUT(kentry(1),'SPOT-PHI-RAT',1,2,worst_ratio)
  call LCMPUT(kentry(1),'SPOT-PHI-NON',1,1,nnonpositive)
  call LCMPUT(kentry(1),'SPOT-PHI-GRP',1,1,worst_group)
  call LCMPUT(kentry(1),'SPOT-PHI-REG',1,1,worst_region)
  call LCMPUT(kentry(1),'SPOT-PHI-MGR',1,1,global_min_group)
  call LCMPUT(kentry(1),'SPOT-PHI-MRG',1,1,global_min_region)
  call LCMPUT(kentry(1),'SPOT-NEG-MAS',1,2,negative_mass_fraction)
  call LCMPUT(kentry(1),'SPOT-WG-MAS',1,2,worst_group_mass_fraction)
  call LCMPUT(kentry(1),'SPOT-WG-NEG',1,2,worst_group_negative_fraction)
  call LCMPUT(kentry(1),'SPOT-NG-GRP',1,1,dominant_negative_group)
  call LCMPUT(kentry(1),'SPOT-NG-MAS',1,2,dominant_negative_mass_fraction)
  call LCMPUT(kentry(1),'SPOT-NG-WGT',1,2,dominant_negative_group_weight)
  call LCMPUT(kentry(1),'SPOT-NG-FRC',1,2,dominant_negative_group_fraction)
  call LCMPUT(kentry(1),'SPOT-NC-ABS',1,2,max_negative_cell_abs_norm)
  call LCMPUT(kentry(1),'SPOT-NC-REL',1,2,max_negative_cell_relative)
  call LCMPUT(kentry(1),'SPOT-NC-AGR',1,1,max_negative_abs_group)
  call LCMPUT(kentry(1),'SPOT-NC-ARE',1,1,max_negative_abs_region)
  call LCMPUT(kentry(1),'SPOT-NC-RGR',1,1,max_negative_rel_group)
  call LCMPUT(kentry(1),'SPOT-NC-RRE',1,1,max_negative_rel_region)
  call LCMPUT(kentry(1),'SPOT-MC-RES',1,4,global_min_cell_residual)
  call LCMPUT(kentry(1),'SPOT-MC-SCL',1,4,global_min_cell_scale)
  call LCMPUT(kentry(1),'SPOT-MC-REL',1,2,global_min_cell_relative)
  write(6,'(A,1P,2E13.5)') 'SPOGBAL GLOBAL/MAX-GROUP ', &
    global_res,group_max
  write(6,'(A,3I8,1P,2E13.5)') &
    'SPOGBAL GALERKIN-MAX G/M/F SIGNED/RATIO ', &
    modal_worst_group,modal_worst_mode,modal_worst_floor, &
    modal_worst_signed,modal_max
  write(6,'(A,I6,1P,5E13.5)') &
    'SPOGBAL WORST-GROUP SIGNED/CELL/AXIAL/SCALE/WEIGHT ', &
    worst_balance_group,worst_balance_signed,real(worst_cell_integral), &
    real(worst_axial),real(worst_balance_scale),worst_balance_weight
  write(6,'(A,I6,1P,3E13.5)') &
    'SPOGBAL MAX-ABS-GROUP RES/TOTAL-SCALE/GROUP-SCALE ', &
    max_abs_balance_group,real(max_abs_balance_residual), &
    max_abs_balance_norm,real(max_abs_balance_scale)
  write(6,'(A,1P,2E13.5)') &
    'SPOGBAL SUM-ABS-GROUP/TOTAL-SCALE ', &
    real(sum_abs_balance_residual),sum_abs_balance_norm
  write(6,'(A,1P,2E13.5)') &
    'SPOGBAL CELL-TELESCOPE/TOTAL-SCALE ', &
    real(telescope_error_sum),telescope_error_norm
  write(6,'(A,1P,3E13.5,0P,3I8)') &
    'SPOGBAL PHI MIN/MAX/WORST-RATIO NONPOS/WORST-G/WORST-R ', &
    global_phi_min,global_phi_max,worst_ratio,nnonpositive,worst_group, &
    worst_region
  write(6,'(A,1P,E13.5,0P,2I8)') &
    'SPOGBAL PHI GLOBAL-MIN G/R ',global_phi_min,global_min_group, &
    global_min_region
  write(6,'(A,1P,3E13.5)') &
    'SPOGBAL PHI NEG-MASS/WORST-GROUP-MASS/WORST-GROUP-NEG ', &
    negative_mass_fraction,worst_group_mass_fraction, &
    worst_group_negative_fraction
  write(6,'(A,I6,1P,3E13.5)') &
    'SPOGBAL PHI DOM-NEG G/NEG-MASS/GROUP-MASS/GROUP-NEG ', &
    dominant_negative_group,dominant_negative_mass_fraction, &
    dominant_negative_group_weight,dominant_negative_group_fraction
  write(6,'(A,1P,3E13.5,0P,2I8)') &
    'SPOGBAL PHI MIN-CELL RES/SCALE/REL G/R ', &
    real(global_min_cell_residual),real(global_min_cell_scale), &
    global_min_cell_relative,global_min_group,global_min_region
  write(6,'(A,1P,2E13.5,0P,4I8)') &
    'SPOGBAL PHI NONPOS-CELL MAX-ABS/TOTAL MAX-REL AG/AR/RG/RR ', &
    max_negative_cell_abs_norm,max_negative_cell_relative, &
    max_negative_abs_group,max_negative_abs_region, &
    max_negative_rel_group,max_negative_rel_region

  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOGBAL: ; CHARACTER EXPECTED.')
  deallocate(ipos,ijjs,njjs,nusigf,chi,fisprod,qfinal,regflux,phi_all)
  deallocate(tx,phi,area,dz,volume,mat1d,keyflx,mat)
end subroutine SPOGBAL

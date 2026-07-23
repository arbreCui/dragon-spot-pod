!DECK SPOFSRC
subroutine SPOFSRC(nentry,hentry,ientry,jentry,kentry)
  ! Build one frozen-fission source for a radial 2D Picard step:
  !
  !   q_g(r) = chi_g(r) sum_h nuSigma_f,h(r) phi_h^old(r) / k_global.
  !
  ! The first output is a temporary macrolib with NUSIGF set to zero.
  ! This prevents TYPE S from adding a second, live fission source.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: indic,nitma,igr,jgr,ireg,ibm,ifis,ilong,itylcm
  integer :: ngrp,nmix,nfis,nreg,nunk
  integer :: imacro(nstate),itrack(nstate),iflux(nstate),isource(nstate)
  integer, allocatable :: mat(:),keyflx(:),keyall(:)
  real :: flott,keff,fis
  real, allocatable :: volume(:),unknown(:,:),source(:,:)
  real, allocatable :: chi(:,:,:),nufis(:,:,:),zeros(:),qint(:)
  double precision :: dflott
  character(len=4) :: text4
  character(len=12) :: signature
  type(c_ptr) :: ipmacro,jpmacro,kpmacro,jpflux,jpsource,kpsource

  if (nentry /= 5) call XABORT('SPOFSRC: FIVE ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOFSRC: LCM ENTRIES EXPECTED.')
  if (any(jentry(1:2) /= 0) .or. any(jentry(3:5) /= 2)) &
    call XABORT('SPOFSRC: TWO NEW OUTPUTS AND THREE INPUTS EXPECTED.')

  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature == 'L_LIBRARY') then
    ipmacro=LCMGID(kentry(3),'MACROLIB')
  else if (signature == 'L_MACROLIB') then
    ipmacro=kentry(3)
  else
    call XABORT('SPOFSRC: INVALID MACROLIB '//trim(hentry(3))//'.')
  endif
  call LCMGTC(kentry(4),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPOFSRC: L_TRACK EXPECTED.')
  call LCMGTC(kentry(5),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOFSRC: L_FLUX EXPECTED.')

  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= 'KEFF')) &
    call XABORT('SPOFSRC: KEFF KEYWORD EXPECTED.')
  call REDGET(indic,nitma,keff,text4,dflott)
  if ((indic /= 2).or.(keff <= 0.0).or.(.not.ieee_is_finite(keff))) &
    call XABORT('SPOFSRC: POSITIVE FINITE KEFF EXPECTED.')
  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOFSRC: ; CHARACTER EXPECTED.')

  call LCMGET(ipmacro,'STATE-VECTOR',imacro)
  call LCMGET(kentry(4),'STATE-VECTOR',itrack)
  call LCMGET(kentry(5),'STATE-VECTOR',iflux)
  ngrp=imacro(1)
  nmix=imacro(2)
  nfis=imacro(4)
  nreg=itrack(1)
  nunk=itrack(2)
  if ((ngrp <= 0).or.(nmix <= 0).or.(nfis <= 0).or.(nreg <= 0) &
      .or.(nunk <= 0)) call XABORT('SPOFSRC: INVALID DIMENSIONS.')
  if ((iflux(1) /= ngrp).or.(iflux(2) /= nunk)) &
    call XABORT('SPOFSRC: INCONSISTENT FLUX DIMENSIONS.')

  call LCMLEN(kentry(4),'KEYFLX$ANIS',ilong,itylcm)
  if (ilong < nreg) call XABORT('SPOFSRC: INVALID KEYFLX LENGTH.')
  allocate(mat(nreg),keyflx(nreg),keyall(ilong),volume(nreg))
  allocate(unknown(nunk,ngrp),source(nunk,ngrp))
  allocate(chi(nmix,nfis,ngrp),nufis(nmix,nfis,ngrp))
  allocate(zeros(nmix*nfis),qint(ngrp))
  call LCMGET(kentry(4),'MATCOD',mat)
  call LCMGET(kentry(4),'VOLUME',volume)
  call LCMGET(kentry(4),'KEYFLX$ANIS',keyall)
  keyflx=keyall(:nreg)
  jpflux=LCMGID(kentry(5),'FLUX')
  do igr=1,ngrp
    call LCMGDL(jpflux,igr,unknown(:,igr))
  enddo

  jpmacro=LCMGID(ipmacro,'GROUP')
  do igr=1,ngrp
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'CHI',ilong,itylcm)
    if (ilong /= nmix*nfis) call XABORT('SPOFSRC: INVALID CHI LENGTH.')
    call LCMLEN(kpmacro,'NUSIGF',ilong,itylcm)
    if (ilong /= nmix*nfis) &
      call XABORT('SPOFSRC: INVALID NUSIGF LENGTH.')
    call LCMGET(kpmacro,'CHI',chi(:,:,igr))
    call LCMGET(kpmacro,'NUSIGF',nufis(:,:,igr))
  enddo

  source=0.0
  qint=0.0
  do ireg=1,nreg
    ibm=mat(ireg)
    if ((ibm <= 0).or.(keyflx(ireg) <= 0)) cycle
    if (ibm > nmix .or. keyflx(ireg) > nunk) &
      call XABORT('SPOFSRC: REGION MAP OVERFLOW.')
    do ifis=1,nfis
      fis=0.0
      do jgr=1,ngrp
        fis=fis+nufis(ibm,ifis,jgr)*unknown(keyflx(ireg),jgr)
      enddo
      do igr=1,ngrp
        source(keyflx(ireg),igr)=source(keyflx(ireg),igr)+ &
          chi(ibm,ifis,igr)*fis/keff
      enddo
    enddo
    do igr=1,ngrp
      qint(igr)=qint(igr)+volume(ireg)*source(keyflx(ireg),igr)
    enddo
  enddo
  if (any(.not.ieee_is_finite(source)) .or. sum(qint) <= 0.0) &
    call XABORT('SPOFSRC: INVALID FROZEN FISSION SOURCE.')

  ! Copy every macrolib record, changing only NUSIGF in the temporary copy.
  call LCMEQU(ipmacro,kentry(1))
  zeros=0.0
  jpmacro=LCMGID(kentry(1),'GROUP')
  do igr=1,ngrp
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMPUT(kpmacro,'NUSIGF',nmix*nfis,2,zeros)
  enddo
  call LCMPUT(kentry(1),'SPOT-FROZEN',1,1,(/1/))
  call LCMPUT(kentry(1),'SPOT-KEFF',1,2,keff)

  signature='L_SOURCE'
  call LCMPTC(kentry(2),'SIGNATURE',12,signature)
  isource=0
  isource(1)=ngrp
  isource(2)=nunk
  isource(3)=1
  call LCMPUT(kentry(2),'STATE-VECTOR',nstate,1,isource)
  call LCMPUT(kentry(2),'SPOT-FROZEN',1,1,(/1/))
  call LCMPUT(kentry(2),'SPOT-KEFF',1,2,keff)
  call LCMPUT(kentry(2),'SPOT-QINT',ngrp,2,qint)
  jpsource=LCMLID(kentry(2),'DSOUR',1)
  kpsource=LCMLIL(jpsource,1,ngrp)
  do igr=1,ngrp
    call LCMPDL(kpsource,igr,nunk,2,source(:,igr))
  enddo
  write(6,'(A,1P,4E13.5)') 'SPOFSRC KEFF/QSUM/QMIN/QMAX ',keff, &
    sum(qint),minval(source),maxval(source)

  deallocate(qint,zeros,nufis,chi,source,unknown,volume,keyall,keyflx,mat)
end subroutine SPOFSRC


!DECK SPOFCHK
subroutine SPOFCHK(nentry,hentry,ientry,jentry,kentry)
  ! Audit one frozen-fission radial solve against its old flux.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate),isystem(nstate)
  integer :: ngrp,nreg,nunk,nmix,igr,ireg,ibm,iunk,ilong,itylcm
  integer :: indic,nitma
  integer, allocatable :: mat(:),keyflx(:),keyall(:)
  real, allocatable :: volume(:),phi(:),old(:),sour(:),leak(:),qint(:)
  real, allocatable :: qfrozen(:)
  real, allocatable :: tx(:),s0(:)
  real :: rel_l2,max_rel,rbal_max,min_phi,qsum,flott,source_keff
  double precision :: dnum,dden,dmax,dref,rbal,rscale,dflott
  character(len=4) :: text4
  character(len=12) :: signature
  type(c_ptr) :: jpflux,jpold,jpsour,jpsystem,kpsystem
  type(c_ptr) :: jpfsrc,kpfsrc,jpqfrozen,kpqfrozen

  if (nentry /= 5) call XABORT('SPOFCHK: FIVE ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOFCHK: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 1).or.any(jentry(2:5) /= 2)) &
    call XABORT('SPOFCHK: MODIFIABLE FLUX AND FOUR INPUTS EXPECTED.')
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') &
    call XABORT('SPOFCHK: INVALID FLUX '//trim(hentry(1))//'.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOFCHK: REFERENCE FLUX EXPECTED.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPOFCHK: L_TRACK EXPECTED.')
  call LCMGTC(kentry(4),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call XABORT('SPOFCHK: L_PIJ EXPECTED.')
  call LCMGTC(kentry(5),'SIGNATURE',12,signature)
  if (signature /= 'L_SOURCE') call XABORT('SPOFCHK: L_SOURCE EXPECTED.')

  call LCMGET(kentry(1),'STATE-VECTOR',iflux)
  call LCMGET(kentry(3),'STATE-VECTOR',itrack)
  call LCMGET(kentry(4),'STATE-VECTOR',isystem)
  ngrp=iflux(1)
  nunk=iflux(2)
  nreg=itrack(1)
  nmix=isystem(10)
  if ((ngrp /= isystem(8)).or.(nunk /= itrack(2)).or. &
      (nunk /= isystem(9)).or.(nmix <= 0)) &
    call XABORT('SPOFCHK: INCONSISTENT DIMENSIONS.')

  call LCMLEN(kentry(3),'KEYFLX$ANIS',ilong,itylcm)
  if (ilong < nreg) call XABORT('SPOFCHK: INVALID KEYFLX LENGTH.')
  allocate(mat(nreg),keyflx(nreg),keyall(ilong),volume(nreg))
  allocate(phi(nunk),old(nunk),sour(nunk),leak(ngrp),qint(ngrp))
  allocate(qfrozen(nunk))
  allocate(tx(0:nmix),s0(0:nmix))
  call LCMGET(kentry(3),'MATCOD',mat)
  call LCMGET(kentry(3),'VOLUME',volume)
  call LCMGET(kentry(3),'KEYFLX$ANIS',keyall)
  keyflx=keyall(:nreg)
  call LCMLEN(kentry(1),'SPOT-LEAK1D',ilong,itylcm)
  if (ilong == ngrp) then
    call LCMGET(kentry(1),'SPOT-LEAK1D',leak)
  else if (ilong == 0) then
    leak=0.0
  else
    call XABORT('SPOFCHK: INVALID LEAK1D LENGTH.')
  endif
  call LCMLEN(kentry(5),'SPOT-QINT',ilong,itylcm)
  if (ilong /= ngrp) call XABORT('SPOFCHK: INVALID QINT LENGTH.')
  call LCMGET(kentry(5),'SPOT-QINT',qint)
  call LCMLEN(kentry(5),'SPOT-KEFF',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 2)) &
    call XABORT('SPOFCHK: INVALID FROZEN-SOURCE KEFF.')
  call LCMGET(kentry(5),'SPOT-KEFF',source_keff)
  if ((.not.ieee_is_finite(source_keff)).or.(source_keff <= 0.0)) &
    call XABORT('SPOFCHK: NONPOSITIVE FROZEN-SOURCE KEFF.')
  call LCMLEN(kentry(5),'DSOUR',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 10)) &
    call XABORT('SPOFCHK: INVALID FROZEN FISSION SOURCE LIST.')
  jpfsrc=LCMGID(kentry(5),'DSOUR')
  kpfsrc=LCMGIL(jpfsrc,1)
  jpqfrozen=LCMLID(kentry(1),'SPOT-QFISS',1)
  kpqfrozen=LCMLIL(jpqfrozen,1,ngrp)

  jpflux=LCMGID(kentry(1),'FLUX')
  jpold=LCMGID(kentry(2),'FLUX')
  jpsour=LCMGID(kentry(1),'SOUR')
  jpsystem=LCMGID(kentry(4),'GROUP')
  dnum=0.0d0
  dden=0.0d0
  dmax=0.0d0
  dref=0.0d0
  rbal_max=0.0
  min_phi=huge(min_phi)
  do igr=1,ngrp
    call LCMLEL(kpfsrc,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 2)) &
      call XABORT('SPOFCHK: INVALID FROZEN FISSION SOURCE ITEM.')
    call LCMGDL(kpfsrc,igr,qfrozen)
    if (any(.not.ieee_is_finite(qfrozen))) &
      call XABORT('SPOFCHK: NON-FINITE FROZEN FISSION SOURCE.')
    call LCMPDL(kpqfrozen,igr,nunk,2,qfrozen)
    call LCMGDL(jpflux,igr,phi)
    call LCMGDL(jpold,igr,old)
    call LCMGDL(jpsour,igr,sour)
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMGET(kpsystem,'DRAGON-TXSC',tx)
    call LCMLEN(kpsystem,'SPOT-S0-PHYS',ilong,itylcm)
    if (ilong /= nmix+1) call XABORT('SPOFCHK: PHYSICAL S0 EXPECTED.')
    call LCMGET(kpsystem,'SPOT-S0-PHYS',s0)
    rbal=0.0d0
    rscale=0.0d0
    do ireg=1,nreg
      ibm=mat(ireg)
      iunk=keyflx(ireg)
      if ((ibm <= 0).or.(iunk <= 0)) cycle
      dnum=dnum+dble(volume(ireg))*dble(phi(iunk)-old(iunk))**2
      dden=dden+dble(volume(ireg))*dble(old(iunk))**2
      dmax=max(dmax,abs(dble(phi(iunk)-old(iunk))))
      dref=max(dref,abs(dble(old(iunk))))
      min_phi=min(min_phi,phi(iunk))
      rbal=rbal+dble(volume(ireg))*(-dble(tx(ibm)*phi(iunk))+ &
        dble(s0(ibm)*phi(iunk))+dble(sour(iunk))- &
        dble(leak(igr)*phi(iunk)))
      rscale=rscale+dble(volume(ireg))*(abs(dble(tx(ibm)*phi(iunk)))+ &
        abs(dble(s0(ibm)*phi(iunk)))+abs(dble(sour(iunk)))+ &
        abs(dble(leak(igr)*phi(iunk))))
    enddo
    if (rscale > 0.0d0) rbal_max=max(rbal_max,real(abs(rbal)/rscale))
  enddo
  if (dden <= 0.0d0 .or. dref <= 0.0d0) &
    call XABORT('SPOFCHK: INVALID REFERENCE NORM.')
  rel_l2=real(sqrt(dnum/dden))
  max_rel=real(dmax/dref)
  qsum=sum(qint)
  if (.not.ieee_is_finite(rel_l2) .or. .not.ieee_is_finite(rbal_max) &
      .or. .not.ieee_is_finite(min_phi) .or. min_phi <= 0.0) &
    call XABORT('SPOFCHK: INVALID FIXED-SOURCE SOLUTION.')
  call LCMPUT(kentry(1),'SPOT-FS-L2',1,2,rel_l2)
  call LCMPUT(kentry(1),'SPOT-FS-MAX',1,2,max_rel)
  call LCMPUT(kentry(1),'SPOT-FS-RBAL',1,2,rbal_max)
  call LCMPUT(kentry(1),'SPOT-FS-MIN',1,2,min_phi)
  call LCMPUT(kentry(1),'SPOT-FS-QSUM',1,2,qsum)
  call LCMPUT(kentry(1),'SPOT-FS-EQN',1,1,(/1/))
  call LCMPUT(kentry(1),'SPOT-FS-K',1,2,source_keff)
  write(6,'(A,1P,5E13.5)') 'SPOFCHK L2/MAX/RBAL/MIN/QSUM ',rel_l2, &
    max_rel,rbal_max,min_phi,qsum

  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOFCHK: ; CHARACTER EXPECTED.')

  deallocate(s0,tx,qfrozen,qint,leak,sour,old,phi)
  deallocate(volume,keyall,keyflx,mat)
end subroutine SPOFCHK

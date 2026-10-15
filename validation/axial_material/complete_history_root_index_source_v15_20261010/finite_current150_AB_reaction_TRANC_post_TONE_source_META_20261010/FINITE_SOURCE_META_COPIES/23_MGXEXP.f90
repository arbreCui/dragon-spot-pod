!DECK MGXEXP
subroutine MGXEXP(nentry,hentry,ientry,jentry,kentry)
  ! Export a multigroup macrolib to solver-neutral ASCII. Multiple
  ! fission spectra remain separate so an independent solver can rebuild
  ! the exact group-to-group fission production matrix.
  use GANLIB
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: indic,nitma,lout,ngrp,nmix,nanis,nfis,nleg,norder
  integer :: igr,ibm,ifis,il,jnd,jgr,ilong,itylcm
  integer :: istate(nstate)
  real :: flott,value
  double precision :: dflott
  character(len=4) :: text4
  character(len=12) :: hsign
  character(len=2) :: cm
  type(c_ptr) :: ipmac,jpmac,kpmac
  integer, allocatable :: ijj(:),njj(:),ipos(:)
  real, allocatable :: energy(:),total(:),sigs(:),absorption(:)
  real, allocatable :: excess_multiplicity(:),work(:),xscat(:)
  real, allocatable :: nufis(:,:),chi(:,:)

  if (nentry /= 2) call XABORT('MGXEXP: TWO ENTRIES EXPECTED.')
  if (ientry(1) /= 4) call XABORT('MGXEXP: ASCII OUTPUT EXPECTED.')
  if (jentry(1) == 2) call XABORT('MGXEXP: OUTPUT IS READ-ONLY.')
  lout=FILUNIT(kentry(1))
  if ((ientry(2) /= 1).and.(ientry(2) /= 2)) &
    call XABORT('MGXEXP: MACROLIB INPUT EXPECTED.')
  if (jentry(2) /= 2) call XABORT('MGXEXP: READ-ONLY INPUT EXPECTED.')
  call LCMGTC(kentry(2),'SIGNATURE',12,hsign)
  if (hsign /= 'L_MACROLIB') &
    call XABORT('MGXEXP: L_MACROLIB INPUT EXPECTED.')

  ipmac=kentry(2)
  call LCMGET(ipmac,'STATE-VECTOR',istate)
  ngrp=istate(1)
  nmix=istate(2)
  nanis=istate(3)
  nfis=istate(4)
  if ((ngrp <= 0).or.(nmix <= 0).or.(nanis <= 0)) &
    call XABORT('MGXEXP: INVALID MACROLIB DIMENSIONS.')

  nleg=nanis
  do
    call REDGET(indic,nitma,flott,text4,dflott)
    if (indic /= 3) call XABORT('MGXEXP: KEYWORD EXPECTED.')
    if (text4 == 'PN') then
      call REDGET(indic,norder,flott,text4,dflott)
      if (indic /= 1) call XABORT('MGXEXP: PN ORDER EXPECTED.')
      if (norder < 0) call XABORT('MGXEXP: NEGATIVE PN ORDER.')
      nleg=min(nanis,norder+1)
    else if (text4 == ';') then
      exit
    else
      call XABORT('MGXEXP: INVALID KEYWORD.')
    endif
  enddo

  allocate(energy(ngrp+1),total(ngrp),sigs(ngrp),absorption(ngrp))
  allocate(excess_multiplicity(ngrp))
  allocate(work(max(nmix,nmix*max(1,nfis))))
  allocate(nufis(max(1,nfis),ngrp),chi(max(1,nfis),ngrp))
  allocate(ijj(nmix),njj(nmix),ipos(nmix))

  call LCMGET(ipmac,'ENERGY',energy)
  write(lout,'(A)') 'MGXEXP 1'
  write(lout,'(A,4I8)') 'DIM ',ngrp,nmix,nleg,nfis
  write(lout,'(A)') 'ENERGY_EV_DESCENDING'
  write(lout,100) energy
  jpmac=LCMGID(ipmac,'GROUP')

  do ibm=1,nmix
    total=0.0
    sigs=0.0
    absorption=0.0
    excess_multiplicity=0.0
    nufis=0.0
    chi=0.0

    do igr=1,ngrp
      kpmac=LCMGIL(jpmac,igr)
      call LCMGET(kpmac,'NTOT0',work)
      total(igr)=work(ibm)
      call LCMLEN(kpmac,'SIGS00',ilong,itylcm)
      if (ilong > 0) then
        call LCMGET(kpmac,'SIGS00',work)
        sigs(igr)=work(ibm)
      endif
      absorption(igr)=total(igr)-sigs(igr)

      call LCMLEN(kpmac,'N2N',ilong,itylcm)
      if (ilong > 0) then
        call LCMGET(kpmac,'N2N',work)
        excess_multiplicity(igr)=excess_multiplicity(igr)+work(ibm)
      endif
      call LCMLEN(kpmac,'N3N',ilong,itylcm)
      if (ilong > 0) then
        call LCMGET(kpmac,'N3N',work)
        excess_multiplicity(igr)=excess_multiplicity(igr)+2.0*work(ibm)
      endif
      call LCMLEN(kpmac,'N4N',ilong,itylcm)
      if (ilong > 0) then
        call LCMGET(kpmac,'N4N',work)
        excess_multiplicity(igr)=excess_multiplicity(igr)+3.0*work(ibm)
      endif
      absorption(igr)=absorption(igr)+excess_multiplicity(igr)

      if (nfis > 0) then
        call LCMLEN(kpmac,'NUSIGF',ilong,itylcm)
        if (ilong > 0) then
          call LCMGET(kpmac,'NUSIGF',work)
          do ifis=1,nfis
            nufis(ifis,igr)=work((ifis-1)*nmix+ibm)
          enddo
        endif
        call LCMLEN(kpmac,'CHI',ilong,itylcm)
        if (ilong > 0) then
          call LCMGET(kpmac,'CHI',work)
          do ifis=1,nfis
            chi(ifis,igr)=work((ifis-1)*nmix+ibm)
          enddo
        endif
      endif
    enddo

    write(lout,'(A,I8)') 'MATERIAL ',ibm
    write(lout,'(A)') 'TOTAL'
    write(lout,100) total
    write(lout,'(A)') 'ABSORPTION'
    write(lout,100) absorption
    write(lout,'(A)') 'SCATTER_SUM'
    write(lout,100) sigs
    write(lout,'(A)') 'EXCESS_MULTIPLICITY'
    write(lout,100) excess_multiplicity
    do ifis=1,nfis
      write(lout,'(A,I8)') 'FISSION_COMPONENT ',ifis
      write(lout,'(A)') 'NU_SIGF'
      write(lout,100) nufis(ifis,:)
      write(lout,'(A)') 'CHI'
      write(lout,100) chi(ifis,:)
    enddo

    ! A group directory is a destination group. Its compressed JGR index
    ! identifies source groups. Raw Legendre moments are exported; the
    ! independent solver applies its own (2*l+1) angular convention.
    do il=0,nleg-1
      write(cm,'(I2.2)') il
      write(lout,'(A,I8)') 'SCATTER ',il
      do igr=1,ngrp
        kpmac=LCMGIL(jpmac,igr)
        call LCMGET(kpmac,'IJJS'//cm,ijj)
        call LCMGET(kpmac,'NJJS'//cm,njj)
        call LCMGET(kpmac,'IPOS'//cm,ipos)
        call LCMLEN(kpmac,'SCAT'//cm,ilong,itylcm)
        if (ilong <= 0) cycle
        allocate(xscat(ilong))
        call LCMGET(kpmac,'SCAT'//cm,xscat)
        do jnd=1,njj(ibm)
          jgr=ijj(ibm)-jnd+1
          value=xscat(ipos(ibm)+jnd-1)
          if (value /= 0.0) write(lout,110) jgr,igr,value
        enddo
        deallocate(xscat)
      enddo
      write(lout,'(A)') 'END_SCATTER'
    enddo
    write(lout,'(A)') 'END_MATERIAL'
  enddo

  write(lout,'(A)') 'END_MGXEXP'
  deallocate(ipos,njj,ijj,chi,nufis,work,excess_multiplicity)
  deallocate(absorption,sigs,total,energy)
  return
100 format(1P,4E24.16)
110 format(2I8,1P,E24.16)
end subroutine MGXEXP

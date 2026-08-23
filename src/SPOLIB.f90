!DECK SPOLIB
subroutine SPOLIB(nentry,hentry,ientry,jentry,kentry)
  ! Build the SPOT multitemperature macrolib by lossless block copying.
  ! No homogenization or spectrum remapping is performed: mixture block k
  ! is copied directly from snapshot k.
  use GANLIB
  implicit none

  integer, intent(in) :: nentry
  integer, intent(in) :: ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer, parameter :: nstate=40
  integer :: indic,nitma,isnap,igr,nsnap,nmix2d,nmix,nfis,ngrp
  integer :: itylcm
  integer :: istate(nstate),iref(nstate)
  real :: flott
  double precision :: dflott
  character(len=4) :: text4
  character(len=12) :: hsign
  type(c_ptr) :: ipout,ipsnap,jarchive,karchive
  type(c_ptr), allocatable :: src(:),groups(:)

  if (nentry < 2) call XABORT('SPOLIB: INPUT LIBRARIES EXPECTED.')
  if ((ientry(1) /= 1).and.(ientry(1) /= 2)) &
    call XABORT('SPOLIB: LCM OUTPUT EXPECTED.')
  if (jentry(1) /= 0) call XABORT('SPOLIB: NEW OUTPUT EXPECTED.')
  ipout=kentry(1)
  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 10).and.((indic /= 3).or.(text4 /= ';'))) &
    call XABORT('SPOLIB: NO INPUT DATA EXPECTED.')

  do isnap=2,nentry
    if ((ientry(isnap) /= 1).and.(ientry(isnap) /= 2)) &
      call XABORT('SPOLIB: LCM INPUT EXPECTED.')
    if (jentry(isnap) /= 2) &
      call XABORT('SPOLIB: READ-ONLY INPUT EXPECTED.')
  enddo

  ipsnap=kentry(2)
  call LCMGTC(ipsnap,'SIGNATURE',12,hsign)
  if (hsign == 'L_ARCHIVE') then
    if (nentry /= 2) &
      call XABORT('SPOLIB: ARCHIVE MUST BE THE ONLY INPUT.')
    call LCMGET(ipsnap,'LISTDIM',nsnap)
    if (nsnap <= 0) call XABORT('SPOLIB: EMPTY SNAPSHOT ARCHIVE.')
    allocate(src(nsnap),groups(nsnap))
    jarchive=LCMGID(ipsnap,'MICROLIB2')
    do isnap=1,nsnap
      karchive=LCMGIL(jarchive,isnap)
      call LCMGTC(karchive,'SIGNATURE',12,hsign)
      if (hsign /= 'L_LIBRARY') &
        call XABORT('SPOLIB: SNAPSHOT MICROLIB EXPECTED.')
      src(isnap)=LCMGID(karchive,'MACROLIB')
    enddo
  else
    nsnap=nentry-1
    allocate(src(nsnap),groups(nsnap))
    do isnap=1,nsnap
      call LCMGTC(kentry(isnap+1),'SIGNATURE',12,hsign)
      if (hsign == 'L_MACROLIB') then
        src(isnap)=kentry(isnap+1)
      else if (hsign == 'L_LIBRARY') then
        src(isnap)=LCMGID(kentry(isnap+1),'MACROLIB')
      else
        call XABORT('SPOLIB: MACROLIB OR MICROLIB EXPECTED.')
      endif
    enddo
  endif

  nmix2d=0
  nfis=0
  ngrp=0
  do isnap=1,nsnap
    call LCMGET(src(isnap),'STATE-VECTOR',istate)
    if (isnap == 1) then
      iref=istate
      ngrp=istate(1)
      nmix2d=istate(2)
      nfis=istate(4)
    else
      if (istate(1) /= ngrp) call XABORT('SPOLIB: GROUP MISMATCH.')
      if (istate(2) /= nmix2d) call XABORT('SPOLIB: MIXTURE MISMATCH.')
      if (istate(3) /= iref(3)) call XABORT('SPOLIB: ANISOTROPY MISMATCH.')
      if (istate(4) /= nfis) call XABORT('SPOLIB: FISSION MISMATCH.')
    endif
  enddo
  if ((ngrp <= 0).or.(nmix2d <= 0)) &
    call XABORT('SPOLIB: INVALID SOURCE MACROLIB.')

  ! Clone metadata and directory structure from snapshot 1, then expand all
  ! mixture-indexed records into disjoint snapshot blocks.
  call LCMEQU(src(1),ipout)
  call SPOCPD(src,ipout,nsnap,nmix2d,nfis)
  nmix=nmix2d*nsnap
  iref(2)=nmix
  call LCMPUT(ipout,'STATE-VECTOR',nstate,1,iref)

  do isnap=1,nsnap
    groups(isnap)=LCMGID(src(isnap),'GROUP')
  enddo
  do igr=1,ngrp
    do isnap=1,nsnap
      groups(isnap)=LCMGIL(LCMGID(src(isnap),'GROUP'),igr)
    enddo
    call SPOCPD(groups,LCMGIL(LCMGID(ipout,'GROUP'),igr), &
                nsnap,nmix2d,nfis)
  enddo

  call LCMLEN(ipout,'STATE-VECTOR',nitma,itylcm)
  if (nitma /= nstate) call XABORT('SPOLIB: INVALID OUTPUT STATE.')
  deallocate(groups,src)
end subroutine SPOLIB


subroutine SPOCPD(src,dst,nsrc,nmix0,nfis)
  ! Copy one LCM directory while expanding material-indexed records.
  use GANLIB
  implicit none

  integer, intent(in) :: nsrc,nmix0,nfis
  type(c_ptr), intent(in) :: src(nsrc),dst

  integer :: ilong,itype,isrc,i,j,nmix,nout,lscat,offset
  integer :: ilong2,itype2
  character(len=12) :: name,first,scatname
  integer, allocatable :: iold(:),inew(:)
  real, allocatable :: rold(:),rnew(:)

  nmix=nmix0*nsrc
  name=' '
  call LCMNXT(src(1),name)
  first=name
  do
    call LCMLEN(src(1),name,ilong,itype)
    if ((ilong > 0).and.((itype == 1).or.(itype == 2))) then
      if ((name(1:4) == 'SCAT').and.(itype == 2)) then
        nout=0
        do isrc=1,nsrc
          call LCMLEN(src(isrc),name,ilong2,itype2)
          if (itype2 /= 2) call XABORT('SPOCPD: SCAT TYPE MISMATCH.')
          nout=nout+ilong2
        enddo
        allocate(rnew(nout))
        offset=0
        do isrc=1,nsrc
          call LCMLEN(src(isrc),name,ilong2,itype2)
          if (ilong2 > 0) then
            allocate(rold(ilong2))
            call LCMGET(src(isrc),name,rold)
            rnew(offset+1:offset+ilong2)=rold
            deallocate(rold)
          endif
          offset=offset+ilong2
        enddo
        call LCMPUT(dst,name,nout,2,rnew)
        deallocate(rnew)
      else if ((name(1:4) == 'IPOS').and.(itype == 1).and. &
               (ilong == nmix0)) then
        allocate(inew(nmix),iold(nmix0))
        scatname='SCAT'//name(5:12)
        offset=0
        do isrc=1,nsrc
          call LCMGET(src(isrc),name,iold)
          do i=1,nmix0
            j=(isrc-1)*nmix0+i
            if (iold(i) > 0) then
              inew(j)=iold(i)+offset
            else
              inew(j)=iold(i)
            endif
          enddo
          call LCMLEN(src(isrc),scatname,lscat,itype2)
          offset=offset+lscat
        enddo
        call LCMPUT(dst,name,nmix,1,inew)
        deallocate(iold,inew)
      else if (ilong == nmix0) then
        if (itype == 1) then
          allocate(inew(nmix),iold(nmix0))
          do isrc=1,nsrc
            call LCMGET(src(isrc),name,iold)
            inew((isrc-1)*nmix0+1:isrc*nmix0)=iold
          enddo
          call LCMPUT(dst,name,nmix,1,inew)
          deallocate(iold,inew)
        else
          allocate(rnew(nmix),rold(nmix0))
          do isrc=1,nsrc
            call LCMGET(src(isrc),name,rold)
            rnew((isrc-1)*nmix0+1:isrc*nmix0)=rold
          enddo
          call LCMPUT(dst,name,nmix,2,rnew)
          deallocate(rold,rnew)
        endif
      else if ((nfis > 0).and.(ilong == nmix0*nfis)) then
        nout=nmix*nfis
        if (itype == 1) then
          allocate(inew(nout),iold(ilong))
          do isrc=1,nsrc
            call LCMGET(src(isrc),name,iold)
            do j=1,nfis
              do i=1,nmix0
                inew((j-1)*nmix+(isrc-1)*nmix0+i)= &
                  iold((j-1)*nmix0+i)
              enddo
            enddo
          enddo
          call LCMPUT(dst,name,nout,1,inew)
          deallocate(iold,inew)
        else
          allocate(rnew(nout),rold(ilong))
          do isrc=1,nsrc
            call LCMGET(src(isrc),name,rold)
            do j=1,nfis
              do i=1,nmix0
                rnew((j-1)*nmix+(isrc-1)*nmix0+i)= &
                  rold((j-1)*nmix0+i)
              enddo
            enddo
          enddo
          call LCMPUT(dst,name,nout,2,rnew)
          deallocate(rold,rnew)
        endif
      endif
    endif
    call LCMNXT(src(1),name)
    if (name == first) exit
  enddo
end subroutine SPOCPD

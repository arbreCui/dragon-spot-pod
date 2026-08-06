module SPOR64_B2B
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOMOC_AUDIT, only : SPOMOC_ACTIVE
  use SPOR64_A9, only : FLU2DR64_CORE
  use SPOR64_B2C, only : SPOR64_B2C_PUBLISH
  implicit none
  private

  integer, parameter, public :: SPOR64_B2B_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2B_CORE_FAILED = 2
  integer, parameter, public :: SPOR64_B2B_NOT_ACCEPTED = 3
  integer, parameter, public :: SPOR64_B2B_ACCEPTED_UNPUBLISHED = 4

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NMAT = 8
  integer, parameter :: NIFIS = 32
  integer, parameter :: NUNKNO = 14
  integer, parameter :: NSOUT = 6
  integer, parameter :: MACRO_STORED_COMPONENTS = 3
  integer, parameter :: TRACK_ACTIVE_COMPONENTS = 1
  integer, parameter :: MAX_SCAT = NMAT*NGRP
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  integer(int32), parameter :: MCCG_EPSI_BITS = int(z'3727c5ac',int32)
  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2B_INGRESS

  interface
    subroutine XDRTA2()
    end subroutine XDRTA2
  end interface

contains

  subroutine SPOR64_B2B_INGRESS(nentry,hentry,ientry,jentry,kentry, &
      itypec,maxout,maxinr,epsout32,epsunk32,epsinr32,irebal,ifritr, &
      iacitr,coptio,ileak,initfl,nmerg,imerg,iprint,rec,imcaud,limerg, &
      ngrp_host,nreg_host,nmat_host,nifis_host,itpij_host,itranc_host, &
      iphase_host,leaksw_host,lforw_host,status,cutoff_visit64)
    integer, intent(in) :: nentry
    character(len=12), intent(in) :: hentry(:)
    integer, intent(in) :: ientry(:), jentry(:)
    type(c_ptr), intent(in) :: kentry(:)
    integer, intent(in) :: itypec, maxout, maxinr, irebal, ifritr
    integer, intent(in) :: iacitr, ileak, initfl, nmerg, imerg(:)
    integer, intent(in) :: iprint, imcaud
    real(real32), intent(in) :: epsout32, epsunk32, epsinr32
    character(len=4), intent(in) :: coptio
    logical, intent(in) :: rec, limerg
    integer, intent(in) :: ngrp_host, nreg_host, nmat_host, nifis_host
    integer, intent(in) :: itpij_host, itranc_host, iphase_host
    logical, intent(in) :: leaksw_host, lforw_host
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_visit64

    character(len=72) :: title, output_file
    character(len=12) :: output_name
    integer :: flux_state(NSTATE), macro_state(NSTATE)
    integer :: system_state(NSTATE), track_state(NSTATE)
    integer :: mccg_state(NSTATE), source_state(NSTATE)
    integer :: imerge_stage(NMAT), matcod(NREG), keyflx_base1(NREG)
    integer :: seed_keyflx(NREG)
    integer :: keycur(NSOUT), nzon(NUNKNO), matalb_surface(NSOUT)
    integer :: njj_stage(NMAT), ijj_stage(NMAT), ipos_stage(NMAT)
    integer :: njj_off(NMAT,NGRP), ijj_off(NMAT,NGRP)
    integer :: ipos_off(NMAT,NGRP), nscat_off(NGRP)
    integer :: frozen_flag, iftrak, ig, ibm, ir, ilong, itylcm
    integer :: allocation_status
    integer :: last_position
    integer(int32) :: volume_bits, track_volume_bits
    logical :: admission_complete, accepted, core_ok
    logical :: output_empty, output_lcm
    logical :: seen_unknown(NUNKNO)
    real(real32) :: eps_stage32(5), real_param32(4)
    real(real32) :: macro_keff32, source_keff32
    real(real32) :: vol32(NREG), volume_track32(NUNKNO)
    real(real32) :: albedo32(NSOUT), surfac32(NSOUT)
    real(real32) :: leak1d_input32(NGRP), seed_leak1d32(NGRP), qint32(NGRP)
    real(real32) :: flux_stage32(NUNKNO), source_stage32(NUNKNO)
    real(real32) :: nusigf_stage32(NMAT*NIFIS)
    real(real32) :: xstrc32(0:NMAT,NGRP)
    real(real32) :: xsdia0_32(0:NMAT,NGRP)
    real(real32), allocatable :: scat_stage32(:)
    real(real32), allocatable :: scat_off32(:,:)
    real(real64) :: fixed_source64(NUNKNO,NGRP)
    real(real64) :: initial_flux64(NUNKNO,NGRP)
    real(real64) :: terminal_flux64(NUNKNO,NGRP)
    real(real64) :: terminal_source64(NUNKNO,NGRP)
    real(real64) :: xcsou1
    type(c_ptr) :: ipflux, ipseed, ipmacr, iptrk, ipsys, ipsou
    type(c_ptr) :: jpflux, jpmacr, jpsys, jpsource, kpsource
    type(c_ptr) :: kpmacr, kpsys

    status = SPOR64_B2B_ADMISSION_FAILED
    cutoff_visit64 = 0_int64
    admission_complete = .false.

    if (nentry /= 7) return
    if (size(hentry) /= nentry .or. size(ientry) /= nentry) return
    if (size(jentry) /= nentry .or. size(kentry) /= nentry) return
    if (size(imerg) /= NMAT) return
    if (hentry(1) /= 'FLUX') return
    if (hentry(2) /= 'MACRO0') return
    if (hentry(3) /= 'TRACK') return
    if (hentry(4) /= 'TRACK_f') return
    if (hentry(5) /= 'SYSTEM') return
    if (hentry(6) /= 'FSOURCE') return
    if (hentry(7) /= 'FLUX_OLD') return
    if (ientry(1) /= 1) return
    if (.not. LCM_ENTRY_KIND(ientry(2))) return
    if (.not. LCM_ENTRY_KIND(ientry(3))) return
    if (ientry(4) /= 3) return
    if (.not. LCM_ENTRY_KIND(ientry(5))) return
    if (.not. LCM_ENTRY_KIND(ientry(6))) return
    if (.not. LCM_ENTRY_KIND(ientry(7))) return
    if (jentry(1) /= 0) return
    if (any(jentry(2:7) /= 2)) return
    do ir = 1, 7
      if (.not. c_associated(kentry(ir))) return
    end do

    ipflux = kentry(1)
    ipmacr = kentry(2)
    iptrk = kentry(3)
    ipsys = kentry(5)
    ipsou = kentry(6)
    ipseed = kentry(7)
    do ir = 2, 7
      if (c_associated(ipflux,kentry(ir))) return
    end do
    iftrak = FILUNIT(kentry(4))
    if (iftrak <= 0) return

    call LCMINF(ipflux,output_file,output_name,output_empty,ilong,output_lcm)
    if (.not. output_lcm .or. ilong /= -1 .or. .not. output_empty) return
    if (trim(output_name) /= '/') return
    if (rec .or. .not. limerg) return
    if (itypec /= 0 .or. maxout /= 500 .or. maxinr /= 740) return
    if (irebal /= 1 .or. ifritr /= 3 .or. iacitr /= 3) return
    if (coptio /= 'B0  ') return
    if (ileak /= 0 .or. initfl /= 1 .or. nmerg /= 1) return
    if (any(imerg /= 1)) return
    if (transfer(epsout32,0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(epsunk32,0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(epsinr32,0_int32) /= FROZEN_TOL_BITS) return
    if (imcaud /= 0 .or. SPOMOC_ACTIVE()) return
    if (ngrp_host /= NGRP .or. nreg_host /= NREG) return
    if (nmat_host /= NMAT .or. nifis_host /= NIFIS) return
    if (itpij_host /= 1 .or. itranc_host /= 2) return
    if (iphase_host /= 1 .or. leaksw_host .or. .not. lforw_host) return

    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipmacr,'SIGNATURE',3,12, &
        'L_MACROLIB')) return
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'SIGNATURE',3,12, &
        'L_PIJ')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsou,'SIGNATURE',3,12, &
        'L_SOURCE')) return

    if (.not. ABSENT_RECORD(ipseed,'B2  HETE')) return
    if (.not. ABSENT_RECORD(ipseed,'B2  B1HOM')) return
    if (.not. ABSENT_RECORD(ipseed,'SPOT-R64')) return
    if (.not. ABSENT_RECORD(ipseed,'AFLUX')) return
    if (.not. ABSENT_RECORD(ipseed,'DFLUX')) return
    if (.not. ABSENT_RECORD(ipseed,'ADFLUX')) return
    if (.not. RECORD_MATCHES(ipseed,'KEYFLX',NREG,1)) return
    call LCMGET(ipseed,'KEYFLX',seed_keyflx)
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'OPTION',1,4,'B0  ')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(ipseed,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(ipseed,'SPOT-LEAK1D',seed_leak1d32)
    if (.not. all(ieee_is_finite(seed_leak1d32))) return
    if (.not. RECORD_MATCHES(ipseed,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipseed,'STATE-VECTOR',flux_state)
    if (flux_state(1) /= NGRP .or. flux_state(2) /= NUNKNO) return
    if (flux_state(3) /= 1) return
    if (flux_state(4) /= 0 .or. flux_state(5) /= 0) return
    if (flux_state(6) /= 0 .or. flux_state(7) /= 0) return
    if (flux_state(8) /= 3 .or. flux_state(9) /= 3) return
    if (flux_state(10) /= 1 .or. flux_state(17) /= NMAT) return
    if (flux_state(11) /= 740 .or. flux_state(12) /= 500) return
    if (flux_state(18) /= 1) return
    if (.not. RECORD_MATCHES(ipseed,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipseed,'EPS-CONVERGE',eps_stage32)
    if (.not. all(ieee_is_finite(eps_stage32))) return
    if (transfer(eps_stage32(1),0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(eps_stage32(2),0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(eps_stage32(3),0_int32) /= FROZEN_TOL_BITS) return
    if (abs(eps_stage32(4)) > 0.0_real32) return
    if (abs(eps_stage32(5)) > 0.0_real32) return
    if (.not. RECORD_MATCHES(ipseed,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(ipseed,'IMERGE-LEAK',imerge_stage)
    if (any(imerge_stage /= 1)) return

    if (.not. RECORD_MATCHES(ipmacr,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipmacr,'STATE-VECTOR',macro_state)
    if (macro_state(1) /= NGRP .or. macro_state(2) /= NMAT) return
    if (macro_state(3) /= MACRO_STORED_COMPONENTS .or. &
        macro_state(4) /= NIFIS) return
    if (macro_state(6) /= 2 .or. macro_state(13) /= 0) return
    if (.not. RECORD_MATCHES(ipmacr,'SPOT-FROZEN',1,1)) return
    call LCMGET(ipmacr,'SPOT-FROZEN',frozen_flag)
    if (frozen_flag /= 1) return
    if (.not. RECORD_MATCHES(ipmacr,'SPOT-KEFF',1,2)) return
    call LCMGET(ipmacr,'SPOT-KEFF',macro_keff32)
    if (.not. ieee_is_finite(macro_keff32)) return
    if (macro_keff32 <= 0.0_real32) return

    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. RECORD_MATCHES(ipsys,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipsys,'STATE-VECTOR',system_state)
    if (any(system_state(1:14) /= &
        [1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0])) return
    if (.not. RECORD_MATCHES(ipsys,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(ipsys,'SPOT-LEAK1D',leak1d_input32)
    if (.not. all(ieee_is_finite(leak1d_input32))) return

    if (.not. RECORD_MATCHES(iptrk,'TITLE',18,3)) return
    title = ' '
    call LCMGTC(iptrk,'TITLE',72,title)
    if (title /= 'SAL TRACKING') return
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'TRACK-TYPE',3,12, &
        'MCCG')) return
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'LINK.FTRACK',3,12, &
        'TRACK_f')) return
    if (.not. RECORD_MATCHES(iptrk,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(iptrk,'STATE-VECTOR',track_state)
    if (track_state(1) /= NREG .or. track_state(2) /= NUNKNO) return
    if (track_state(3) /= 1 .or. track_state(4) /= NMAT) return
    if (track_state(5) /= NSOUT .or. &
        track_state(6) /= TRACK_ACTIVE_COMPONENTS) return
    if (track_state(9) /= 0 .or. track_state(14) /= 4) return
    if (track_state(16) /= 2 .or. track_state(22) /= 1) return
    if (track_state(27) /= 0 .or. track_state(39) /= 0) return
    if (track_state(40) /= 0) return
    if (.not. RECORD_MATCHES(iptrk,'MCCG-STATE',NSTATE,1)) return
    call LCMGET(iptrk,'MCCG-STATE',mccg_state)
    if (mccg_state(2) /= 4 .or. mccg_state(3) /= 10) return
    if (mccg_state(4) /= 0 .or. mccg_state(5) /= 17) return
    if (mccg_state(6) /= 32 .or. mccg_state(7) /= 80) return
    if (mccg_state(8) /= 0 .or. mccg_state(9) /= 0) return
    if (mccg_state(10) /= 4 .or. mccg_state(12) /= 0) return
    if (mccg_state(13) /= 20 .or. mccg_state(15) /= 1) return
    if (mccg_state(16) /= 1 .or. mccg_state(18) /= 0) return
    if (mccg_state(19) /= 1 .or. mccg_state(20) /= 1) return
    if (.not. RECORD_MATCHES(iptrk,'REAL-PARAM',4,2)) return
    call LCMGET(iptrk,'REAL-PARAM',real_param32)
    if (.not. all(ieee_is_finite(real_param32))) return
    if (transfer(real_param32(1),0_int32) /= MCCG_EPSI_BITS) return
    if (any(abs(real_param32(2:4)) > 0.0_real32)) return

    if (.not. RECORD_MATCHES(iptrk,'MATCOD',NREG,1)) return
    call LCMGET(iptrk,'MATCOD',matcod)
    if (.not. RECORD_MATCHES(iptrk,'VOLUME',NREG,2)) return
    call LCMGET(iptrk,'VOLUME',vol32)
    if (.not. RECORD_MATCHES(iptrk,'KEYFLX$ANIS',NREG,1)) return
    call LCMGET(iptrk,'KEYFLX$ANIS',keyflx_base1)
    if (any(seed_keyflx /= keyflx_base1)) return
    if (.not. RECORD_MATCHES(iptrk,'KEYCUR$MCCG',NSOUT,1)) return
    call LCMGET(iptrk,'KEYCUR$MCCG',keycur)
    if (.not. RECORD_MATCHES(iptrk,'NZON$MCCG',NUNKNO,1)) return
    call LCMGET(iptrk,'NZON$MCCG',nzon)
    if (.not. RECORD_MATCHES(iptrk,'V$MCCG',NUNKNO,2)) return
    call LCMGET(iptrk,'V$MCCG',volume_track32)
    if (.not. RECORD_MATCHES(iptrk,'ALBEDO',NSOUT,2)) return
    call LCMGET(iptrk,'ALBEDO',albedo32)

    if (any(matcod < 1) .or. any(matcod > NMAT)) return
    if (any(nzon(1:NREG) /= matcod)) return
    if (any(nzon(NREG+1:) < -NSOUT)) return
    if (any(nzon(NREG+1:) > -1)) return
    if (.not. all(ieee_is_finite(vol32))) return
    if (.not. all(ieee_is_finite(volume_track32))) return
    if (any(vol32 <= 0.0_real32)) return
    if (any(volume_track32 <= 0.0_real32)) return
    do ir = 1, NREG
      volume_bits = transfer(vol32(ir),0_int32)
      track_volume_bits = transfer(volume_track32(ir),0_int32)
      if (volume_bits /= track_volume_bits) return
    end do
    if (.not. all(ieee_is_finite(albedo32))) return
    matalb_surface = nzon(NREG+1:NUNKNO)
    surfac32 = volume_track32(NREG+1:NUNKNO)

    seen_unknown = .false.
    do ir = 1, NREG
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > NUNKNO) return
      if (seen_unknown(keyflx_base1(ir))) return
      seen_unknown(keyflx_base1(ir)) = .true.
    end do
    do ir = 1, NSOUT
      if (keycur(ir) < 1 .or. keycur(ir) > NUNKNO) return
      if (seen_unknown(keycur(ir))) return
      seen_unknown(keycur(ir)) = .true.
    end do
    if (.not. all(seen_unknown)) return

    if (.not. ABSENT_RECORD(ipsou,'NORM-FS')) return
    if (.not. ABSENT_RECORD(ipsou,'NBS')) return
    if (.not. RECORD_MATCHES(ipsou,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipsou,'STATE-VECTOR',source_state)
    if (source_state(1) /= NGRP .or. source_state(2) /= NUNKNO) return
    if (source_state(3) /= 1) return
    if (any(source_state(4:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(ipsou,'SPOT-FROZEN',1,1)) return
    call LCMGET(ipsou,'SPOT-FROZEN',frozen_flag)
    if (frozen_flag /= 1) return
    if (.not. RECORD_MATCHES(ipsou,'SPOT-KEFF',1,2)) return
    call LCMGET(ipsou,'SPOT-KEFF',source_keff32)
    if (.not. ieee_is_finite(source_keff32)) return
    if (source_keff32 <= 0.0_real32) return
    if (transfer(source_keff32,0_int32) /= &
        transfer(macro_keff32,0_int32)) return
    if (.not. RECORD_MATCHES(ipsou,'SPOT-QINT',NGRP,2)) return
    call LCMGET(ipsou,'SPOT-QINT',qint32)
    if (.not. all(ieee_is_finite(qint32))) return

    if (.not. RECORD_MATCHES(ipseed,'FLUX',NGRP,10)) return
    jpflux = LCMGID(ipseed,'FLUX')
    if (.not. c_associated(jpflux)) return
    initial_flux64 = +0.0_real64
    do ig = 1, NGRP
      call LCMLEL(jpflux,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 2) return
      call LCMGDL(jpflux,ig,flux_stage32)
      if (.not. all(ieee_is_finite(flux_stage32))) return
      initial_flux64(:,ig) = real(flux_stage32,real64)
    end do

    if (.not. RECORD_MATCHES(ipsou,'DSOUR',1,10)) return
    jpsource = LCMGID(ipsou,'DSOUR')
    if (.not. c_associated(jpsource)) return
    call LCMLEL(jpsource,1,ilong,itylcm)
    if (ilong /= NGRP .or. itylcm /= 10) return
    kpsource = LCMGIL(jpsource,1)
    if (.not. c_associated(kpsource)) return
    fixed_source64 = +0.0_real64
    do ig = 1, NGRP
      call LCMLEL(kpsource,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 2) return
      call LCMGDL(kpsource,ig,source_stage32)
      if (.not. all(ieee_is_finite(source_stage32))) return
      if (any(source_stage32 < 0.0_real32)) return
      fixed_source64(:,ig) = real(source_stage32,real64)
    end do

    xcsou1 = +0.0_real64
    do ir = 1, NREG
      xcsou1 = xcsou1 + fixed_source64(keyflx_base1(ir),1) * &
          real(vol32(ir),real64)
    end do
    if (.not. ieee_is_finite(xcsou1) .or. xcsou1 <= 0.0_real64) return

    if (.not. RECORD_MATCHES(ipmacr,'GROUP',NGRP,10)) return
    jpmacr = LCMGID(ipmacr,'GROUP')
    if (.not. c_associated(jpmacr)) return
    allocate(scat_off32(MAX_SCAT,NGRP),stat=allocation_status)
    if (allocation_status /= 0) return
    scat_off32 = +0.0_real32
    njj_off = 0
    ijj_off = 0
    ipos_off = 0
    nscat_off = 0
    do ig = 1, NGRP
      kpmacr = LCMGIL(jpmacr,ig)
      if (.not. c_associated(kpmacr)) return
      if (.not. RECORD_MATCHES(kpmacr,'NJJS01',NMAT,1)) return
      if (.not. RECORD_MATCHES(kpmacr,'NJJS02',NMAT,1)) return
      if (.not. RECORD_MATCHES(kpmacr,'NUSIGF',NMAT*NIFIS,2)) return
      call LCMGET(kpmacr,'NUSIGF',nusigf_stage32)
      if (.not. all(ieee_is_finite(nusigf_stage32))) return
      if (any(abs(nusigf_stage32) > 0.0_real32)) return
      if (.not. RECORD_MATCHES(kpmacr,'NJJS00',NMAT,1)) return
      call LCMGET(kpmacr,'NJJS00',njj_stage)
      if (.not. RECORD_MATCHES(kpmacr,'IJJS00',NMAT,1)) return
      call LCMGET(kpmacr,'IJJS00',ijj_stage)
      if (.not. RECORD_MATCHES(kpmacr,'IPOS00',NMAT,1)) return
      call LCMGET(kpmacr,'IPOS00',ipos_stage)
      call LCMLEN(kpmacr,'SCAT00',ilong,itylcm)
      if (ilong < 0 .or. ilong > MAX_SCAT .or. itylcm /= 2) return
      if (ilong > 0) then
        allocate(scat_stage32(ilong),stat=allocation_status)
        if (allocation_status /= 0) return
        call LCMGET(kpmacr,'SCAT00',scat_stage32)
        if (.not. all(ieee_is_finite(scat_stage32))) return
      end if
      do ibm = 1, NMAT
        if (njj_stage(ibm) < 0) return
        if (njj_stage(ibm) == 0) cycle
        if (ipos_stage(ibm) < 1) return
        last_position = ipos_stage(ibm) + njj_stage(ibm) - 1
        if (last_position > ilong) return
        if (ijj_stage(ibm) < 1 .or. ijj_stage(ibm) > NGRP) return
        if (ijj_stage(ibm)-njj_stage(ibm)+1 < 1) return
      end do
      njj_off(:,ig) = njj_stage
      ijj_off(:,ig) = ijj_stage
      ipos_off(:,ig) = ipos_stage
      nscat_off(ig) = ilong
      if (ilong > 0) then
        scat_off32(1:ilong,ig) = scat_stage32
        deallocate(scat_stage32)
      end if
    end do

    if (.not. RECORD_MATCHES(ipsys,'GROUP',NGRP,10)) return
    jpsys = LCMGID(ipsys,'GROUP')
    if (.not. c_associated(jpsys)) return
    xstrc32 = +0.0_real32
    xsdia0_32 = +0.0_real32
    do ig = 1, NGRP
      kpsys = LCMGIL(jpsys,ig)
      if (.not. c_associated(kpsys)) return
      if (.not. RECORD_MATCHES(kpsys,'DRAGON-TXSC',NMAT+1,2)) return
      call LCMGET(kpsys,'DRAGON-TXSC',xstrc32(:,ig))
      if (.not. all(ieee_is_finite(xstrc32(:,ig)))) return
      if (.not. RECORD_MATCHES(kpsys,'DRAGON-S0XSC',NMAT+1,2)) return
      call LCMGET(kpsys,'DRAGON-S0XSC',xsdia0_32(:,ig))
      if (.not. all(ieee_is_finite(xsdia0_32(:,ig)))) return
      xsdia0_32(0,ig) = +0.0_real32
      call LCMLEN(kpsys,'FUNKNO$USS',ilong,itylcm)
      if (ilong /= 0 .or. itylcm /= 99) return
    end do

    admission_complete = .true.
    if (.not. admission_complete) return
    call XDRTA2
    call FLU2DR64_CORE(jpsys,iptrk,iftrak,iprint,title, &
        keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
        matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
        nscat_off,scat_off32,fixed_source64,initial_flux64, &
        real(epsinr32,real64),real(epsunk32,real64), &
        real(epsout32,real64),terminal_flux64,terminal_source64, &
        cutoff_visit64,accepted,core_ok)

    if (.not. core_ok) then
      status = SPOR64_B2B_CORE_FAILED
    else if (.not. accepted) then
      status = SPOR64_B2B_NOT_ACCEPTED
    else
      status = SPOR64_B2B_ACCEPTED_UNPUBLISHED
      call SPOR64_B2C_PUBLISH(ipflux,SPOR64_B2B_ACCEPTED_UNPUBLISHED, &
          terminal_flux64,terminal_source64,keyflx_base1,nmerg,imerg, &
          leak1d_input32,epsout32,epsunk32,epsinr32,coptio, &
          hentry(2),hentry(3),hentry(5),status)
    end if
  end subroutine SPOR64_B2B_INGRESS


  logical function LCM_ENTRY_KIND(kind_value)
    integer, intent(in) :: kind_value

    LCM_ENTRY_KIND = kind_value == 1 .or. kind_value == 2
  end function LCM_ENTRY_KIND


  logical function RECORD_MATCHES(iplist,name,expected_length, &
      expected_type)
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


  logical function ABSENT_RECORD(iplist,name)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type

    ABSENT_RECORD = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    ABSENT_RECORD = actual_length == 0 .and. actual_type == 99
  end function ABSENT_RECORD

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

end module SPOR64_B2B

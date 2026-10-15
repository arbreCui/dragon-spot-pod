module SPOR64_BOOTB64
  ! One radial fixed-source solve: admission, the REAL64 core
  ! call, publication.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOMOC_AUDIT, only : SPOMOC_ACTIVE
  use SPOR64_A9, only : FLU2DR64_CORE
  use SPOR64_BOOT_BIND64, only : SPOR64_BOOT_BIND64_READ
  use SPOR64_BOOTC64, only : SPOR64_BOOTC64_PUBLISH, SPOR64_BOOTC64_PUBLISH_CONT
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EXACT_INVENTORY, RECORD_MATCHES, SAME_REAL32_BITS
  use SPOR64_SCHEMA, only : SCHEMA_PLANE_SEED_AUTHORITY, &
      SCHEMA_SOURCE_AUTHORITY, SCHEMA_SYSTEM_AUTHORITY
  implicit none
  private

  integer, parameter, public :: SPOR64_BOOTB64_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_BOOTB64_CORE_FAILED = 2
  integer, parameter, public :: SPOR64_BOOTB64_NOT_ACCEPTED = 3
  integer, parameter, public :: SPOR64_BOOTB64_ACCEPTED_UNPUBLISHED = 4
  integer, parameter, public :: SPOR64_BOOTB64_BOOT = 1
  integer, parameter, public :: SPOR64_BOOTB64_CONT = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NIFIS = 32
  integer, parameter :: NALBEDO = 6
  integer, parameter :: MACRO_STORED_COMPONENTS = 3
  integer, parameter :: TRACK_ACTIVE_COMPONENTS = 1
  ! Axial lineage terminal of the r64dp route (solver_eps = 5.0E-8 in
  ! REAL32).  Seeds projected from dp-era axial states carry this value
  ! in EPS-CONVERGE(1:3) and IREBAL=0 (REBA OFF) in their state vector.
  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_BOOTB64_INGRESS

  interface
    subroutine XDRTA2()
    end subroutine XDRTA2
  end interface

contains

  subroutine SPOR64_BOOTB64_INGRESS(nentry,hentry,ientry,jentry,kentry, &
      itypec,maxout,maxinr,epsout32,epsunk32,epsinr32,irebal,ifritr, &
      iacitr,coptio,ileak,initfl,nmerg,imerg,iprint,rec,imcaud,limerg, &
      ngrp_host,nreg_host,nmat_host,nifis_host,itpij_host,itranc_host, &
      iphase_host,leaksw_host,lforw_host,r64_mode,contract,status, &
      cutoff_visit64,ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem, &
      ipaxmacro,iparchive,ipcontract,requested_rank,boot_plane)
    integer, intent(in) :: nentry
    character(len=12), intent(in) :: hentry(:)
    integer, intent(in) :: ientry(:), jentry(:)
    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract
    type(c_ptr), intent(in) :: kentry(:)
    type(c_ptr), intent(in) :: ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem
    type(c_ptr), intent(in) :: ipaxmacro,iparchive,ipcontract
    integer, intent(in) :: requested_rank,boot_plane
    logical :: boot_bound
    integer, intent(in) :: itypec, maxout, maxinr, irebal, ifritr
    integer, intent(in) :: iacitr, ileak, initfl, nmerg, imerg(:)
    integer, intent(in) :: iprint, imcaud, r64_mode
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
    integer, allocatable :: imerge_stage(:), matcod(:), keyflx_base1(:)
    integer, allocatable :: seed_keyflx(:), nzon(:)
    integer, allocatable :: keycur(:), matalb_surface(:)
    integer, allocatable :: njj_stage(:), ijj_stage(:), ipos_stage(:)
    integer, allocatable :: njj_off(:,:), ijj_off(:,:), ipos_off(:,:)
    integer :: nscat_off(NGRP)
    integer :: frozen_flag, iftrak, ig, ibm, ir, ilong, itylcm
    integer :: allocation_status
    integer :: last_position, nreg, nmat, nsou, nunkno, nlong, max_scat
    integer :: plane_index
    integer :: lc0, paca
    integer(int32) :: volume_bits, track_volume_bits
    logical :: admission_complete, accepted, core_ok
    logical :: output_empty, output_lcm
    logical, allocatable :: seen_unknown(:)
    real(real32) :: eps_stage32(5), real_param32(4)
    real(real32) :: macro_keff32, source_keff32
    real(real32), allocatable :: vol32(:), volume_track32(:), surfac32(:)
    real(real32) :: albedo32(NALBEDO)
    real(real32) :: leak1d_input32(NGRP), seed_leak1d32(NGRP), qint32(NGRP)
    real(real32), allocatable :: ilucf_stage32(:), s0phys_stage32(:)
    real(real64) :: leak1d64(NGRP)
    logical :: have_leak1d64
    real(real32), allocatable :: flux_stage32(:), source_stage32(:)
    real(real32), allocatable :: nusigf_stage32(:)
    real(real32), allocatable :: xstrc32(:,:), xsdia0_32(:,:)
    real(real32), allocatable :: scat_stage32(:)
    real(real32), allocatable :: scat_off32(:,:)
    real(real64), allocatable :: fixed_source64(:,:), initial_flux64(:,:)
    real(real64), allocatable :: terminal_flux64(:,:), terminal_source64(:,:)
    real(real64) :: xcsou1
    type(c_ptr) :: ipflux, ipseed, ipmacr, iptrk, ipsys, ipsou
    type(c_ptr) :: seed_authority, source_authority
    type(c_ptr) :: jpflux, jpmacr, jpsys, jpsource, kpsource
    type(c_ptr) :: kpmacr, kpsys

    status = SPOR64_BOOTB64_ADMISSION_FAILED
    cutoff_visit64 = 0_int64
    admission_complete = .false.

    if (r64_mode /= SPOR64_BOOTB64_BOOT) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0121","original_return_source_line":121,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (requested_rank <= 0 .or. boot_plane < 1 .or. boot_plane > 3) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0122","original_return_source_line":122,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (ngrp_host /= NGRP .or. nreg_host <= 0 .or. nmat_host <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0123","original_return_source_line":123,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (nifis_host /= NIFIS) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0124","original_return_source_line":124,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (int(nmat_host,int64)*int(NGRP,int64) > &
        int(huge(max_scat),int64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0126","original_return_source_line":126,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    nreg = nreg_host
    nmat = nmat_host
    if (nentry /= 7) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0129","original_return_source_line":129,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (size(hentry) /= nentry .or. size(ientry) /= nentry) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0130","original_return_source_line":130,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (size(jentry) /= nentry .or. size(kentry) /= nentry) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0131","original_return_source_line":131,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (size(imerg) /= nmat) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0132","original_return_source_line":132,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(1) /= 'FLUX') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0133","original_return_source_line":133,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(2) /= 'MACRO0') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0134","original_return_source_line":134,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(3) /= 'TRACK') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0135","original_return_source_line":135,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(4) /= 'TRACK_f') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0136","original_return_source_line":136,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(5) /= 'SYSTEM') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0137","original_return_source_line":137,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(6) /= 'FSOURCE') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0138","original_return_source_line":138,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (hentry(7) /= 'FLUX_OLD') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0139","original_return_source_line":139,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (ientry(1) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0140","original_return_source_line":140,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. LCM_ENTRY_KIND(ientry(2))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0141","original_return_source_line":141,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. LCM_ENTRY_KIND(ientry(3))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0142","original_return_source_line":142,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (ientry(4) /= 3) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0143","original_return_source_line":143,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. LCM_ENTRY_KIND(ientry(5))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0144","original_return_source_line":144,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. LCM_ENTRY_KIND(ientry(6))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0145","original_return_source_line":145,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. LCM_ENTRY_KIND(ientry(7))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0146","original_return_source_line":146,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (jentry(1) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0147","original_return_source_line":147,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(jentry(2:7) /= 2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0148","original_return_source_line":148,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    do ir = 1, 7
      if (.not. c_associated(kentry(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0150","original_return_source_line":150,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end do

    ipflux = kentry(1)
    ipmacr = kentry(2)
    iptrk = kentry(3)
    ipsys = kentry(5)
    ipsou = kentry(6)
    ipseed = kentry(7)
    do ir = 2, 7
      if (c_associated(ipflux,kentry(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0160","original_return_source_line":160,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end do
    iftrak = FILUNIT(kentry(4))
    if (iftrak <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0163","original_return_source_line":163,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    call LCMINF(ipflux,output_file,output_name,output_empty,ilong,output_lcm)
    if (.not. output_lcm .or. ilong /= -1 .or. .not. output_empty) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0166","original_return_source_line":166,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (trim(output_name) /= '/') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0167","original_return_source_line":167,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (rec .or. .not. limerg) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0168","original_return_source_line":168,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (itypec /= 0 .or. maxout /= contract%flu_maxout .or. &
        maxinr /= contract%flu_maxinr) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0170","original_return_source_line":170,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (irebal /= 1 .or. ifritr /= contract%flu_acce_free .or. &
        iacitr /= contract%flu_acce_accel) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0172","original_return_source_line":172,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (coptio /= contract%flu_option) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0173","original_return_source_line":173,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (ileak /= 0 .or. initfl /= 1 .or. nmerg /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0174","original_return_source_line":174,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(imerg /= 1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0175","original_return_source_line":175,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(epsout32,0_int32) /= contract%eps_radial_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0176","original_return_source_line":176,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(epsunk32,0_int32) /= contract%eps_radial_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0177","original_return_source_line":177,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(epsinr32,0_int32) /= contract%eps_radial_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0178","original_return_source_line":178,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (imcaud /= 0 .or. SPOMOC_ACTIVE()) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0179","original_return_source_line":179,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (itpij_host /= 1 .or. itranc_host /= 2) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0180","original_return_source_line":180,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (iphase_host /= 1 .or. leaksw_host .or. .not. lforw_host) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0181","original_return_source_line":181,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'SIGNATURE',3,12, &
        'L_FLUX')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0184","original_return_source_line":184,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipmacr,'SIGNATURE',3,12, &
        'L_MACROLIB')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0186","original_return_source_line":186,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'SIGNATURE',3,12, &
        'L_TRACK')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0188","original_return_source_line":188,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'SIGNATURE',3,12, &
        'L_PIJ')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0190","original_return_source_line":190,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsou,'SIGNATURE',3,12, &
        'L_SOURCE')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0192","original_return_source_line":192,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    ! TRACK is the sole geometry-dimension authority.  Host counts and every
    ! other object below must agree with this immutable state record.
    if (.not. RECORD_MATCHES(iptrk,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0196","original_return_source_line":196,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'STATE-VECTOR',track_state)
    nreg = track_state(1)
    nunkno = track_state(2)
    nmat = track_state(4)
    nsou = track_state(5)
    if (nreg /= nreg_host .or. nunkno <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0202","original_return_source_line":202,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (track_state(3) /= 1 .or. nmat /= nmat_host) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0203","original_return_source_line":203,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (nsou <= 0 .or. track_state(6) /= TRACK_ACTIVE_COMPONENTS) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0204","original_return_source_line":204,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsou,int64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0205","original_return_source_line":205,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    ! The stored tracking payload must independently confirm the state-vector
    ! dimensions before any geometry-sized allocation or read is attempted.
    call LCMLEN(iptrk,'V$MCCG',nlong,itylcm)
    if (nlong /= nunkno .or. itylcm /= 2) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0210","original_return_source_line":210,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMLEN(iptrk,'NZON$MCCG',ilong,itylcm)
    if (ilong /= nlong .or. itylcm /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0212","original_return_source_line":212,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMLEN(iptrk,'KEYCUR$MCCG',ilong,itylcm)
    if (ilong /= nsou .or. itylcm /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0214","original_return_source_line":214,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    max_scat = nmat*NGRP
    allocate(imerge_stage(nmat),matcod(nreg),keyflx_base1(nreg), &
        seed_keyflx(nreg),keycur(nsou),matalb_surface(nsou), &
        surfac32(nsou),vol32(nreg),njj_stage(nmat),ijj_stage(nmat), &
        ipos_stage(nmat),njj_off(nmat,NGRP),ijj_off(nmat,NGRP), &
        ipos_off(nmat,NGRP),nusigf_stage32(nmat*NIFIS), &
        s0phys_stage32(nmat+1),xstrc32(0:nmat,NGRP), &
        xsdia0_32(0:nmat,NGRP),nzon(nlong),volume_track32(nlong), &
        seen_unknown(nunkno), &
        flux_stage32(nunkno),source_stage32(nunkno), &
        fixed_source64(nunkno,NGRP),initial_flux64(nunkno,NGRP), &
        terminal_flux64(nunkno,NGRP),terminal_source64(nunkno,NGRP), &
        stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0229","original_return_source_line":229,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. ABSENT_RECORD(ipseed,'B2  HETE')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0231","original_return_source_line":231,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. ABSENT_RECORD(ipseed,'B2  B1HOM')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0232","original_return_source_line":232,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (r64_mode == SPOR64_BOOTB64_BOOT) then
      if (.not. RECORD_MATCHES(ipseed,'SPOT-R64',-1,0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0234","original_return_source_line":234,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(ipsou,'SPOT-R64',-1,0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0235","original_return_source_line":235,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    else
      if (.not. RECORD_MATCHES(ipseed,'SPOT-R64',-1,0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0237","original_return_source_line":237,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(ipsou,'SPOT-R64',-1,0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0238","original_return_source_line":238,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end if
    if (.not. ABSENT_RECORD(ipseed,'AFLUX')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0240","original_return_source_line":240,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. ABSENT_RECORD(ipseed,'DFLUX')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0241","original_return_source_line":241,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. ABSENT_RECORD(ipseed,'ADFLUX')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0242","original_return_source_line":242,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipseed,'KEYFLX',nreg,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0243","original_return_source_line":243,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'KEYFLX',seed_keyflx)
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'OPTION',1,4, &
        contract%flu_option)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0246","original_return_source_line":246,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (r64_mode == SPOR64_BOOTB64_BOOT) then
      if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.MACRO',3,12, &
          'MACRO0') .and. &
          .not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.MACRO',3,12, &
          'MICROLIB2')) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0251","original_return_source_line":251,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    else
      if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.MACRO',3,12, &
          'MACRO0')) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0254","original_return_source_line":254,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end if
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.TRACK',3,12, &
        'TRACK')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0257","original_return_source_line":257,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.SYSTEM',3,12, &
        'SYSTEM')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0259","original_return_source_line":259,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipseed,'SPOT-LEAK1D',NGRP,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0260","original_return_source_line":260,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'SPOT-LEAK1D',seed_leak1d32)
    if (.not. all(ieee_is_finite(seed_leak1d32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0262","original_return_source_line":262,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    ! Presence-gated REAL64 leakage authority on the projected seed.
    ! When present, the REAL32 record must be its exact bitwise demote
    ! mirror and the assembled system must be UNREDUCED (verified in
    ! the group loop below); the reduction is then applied in REAL64
    ! inside the solver core.
    call LCMLEN(ipseed,'LEAK1D64',ilong,itylcm)
    have_leak1d64 = (ilong == NGRP .and. itylcm == 4)
    if (ilong /= 0 .and. .not. have_leak1d64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0270","original_return_source_line":270,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    leak1d64 = 0.0_real64
    if (have_leak1d64) then
      call LCMGET(ipseed,'LEAK1D64',leak1d64)
      if (.not. all(ieee_is_finite(leak1d64))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0274","original_return_source_line":274,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      do ig = 1, NGRP
        if (transfer(seed_leak1d32(ig),0_int32) /= &
            transfer(real(leak1d64(ig),real32),0_int32)) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0277","original_return_source_line":277,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
      end do
    end if
    if (.not. have_leak1d64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0280","original_return_source_line":280,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipseed,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0281","original_return_source_line":281,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'STATE-VECTOR',flux_state)
    if (flux_state(1) /= NGRP .or. flux_state(2) /= nunkno) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0283","original_return_source_line":283,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(3) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0284","original_return_source_line":284,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(4) /= 0 .or. flux_state(5) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0285","original_return_source_line":285,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (r64_mode == SPOR64_BOOTB64_BOOT) then
      ! A raw TYPE-K snapshot is admitted only as the numerical initial
      ! iterate of this TYPE-S BOOT solve.  The host equation above remains
      ! ITYPEC=0 and the independently frozen FSOURCE remains authoritative.
      if (flux_state(6) /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0290","original_return_source_line":290,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    else
      if (flux_state(6) /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0292","original_return_source_line":292,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end if
    if (flux_state(7) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0294","original_return_source_line":294,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(8) /= contract%flu_acce_free .or. &
        flux_state(9) /= contract%flu_acce_accel) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0296","original_return_source_line":296,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(10) /= 1 .and. flux_state(10) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0297","original_return_source_line":297,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(17) /= nmat) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0298","original_return_source_line":298,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(11) /= contract%flu_maxinr .or. &
        flux_state(12) /= contract%flu_maxout) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0300","original_return_source_line":300,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (flux_state(18) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0301","original_return_source_line":301,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipseed,'EPS-CONVERGE',5,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0302","original_return_source_line":302,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'EPS-CONVERGE',eps_stage32)
    if (.not. all(ieee_is_finite(eps_stage32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0304","original_return_source_line":304,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(eps_stage32(1),0_int32) /= contract%eps_radial_bits &
        .and. transfer(eps_stage32(1),0_int32) /= &
        contract%eps_axial_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0307","original_return_source_line":307,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(eps_stage32(2),0_int32) /= &
        transfer(eps_stage32(1),0_int32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0309","original_return_source_line":309,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(eps_stage32(3),0_int32) /= &
        transfer(eps_stage32(1),0_int32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0311","original_return_source_line":311,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (abs(eps_stage32(4)) > 0.0_real32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0312","original_return_source_line":312,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (abs(eps_stage32(5)) > 0.0_real32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0313","original_return_source_line":313,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipseed,'IMERGE-LEAK',nmat,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0314","original_return_source_line":314,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipseed,'IMERGE-LEAK',imerge_stage)
    if (any(imerge_stage /= 1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0316","original_return_source_line":316,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. RECORD_MATCHES(ipmacr,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0318","original_return_source_line":318,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipmacr,'STATE-VECTOR',macro_state)
    if (macro_state(1) /= NGRP .or. macro_state(2) /= nmat) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0320","original_return_source_line":320,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (macro_state(3) /= MACRO_STORED_COMPONENTS .or. &
        macro_state(4) /= NIFIS) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0322","original_return_source_line":322,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (macro_state(6) /= 2 .or. macro_state(13) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0323","original_return_source_line":323,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipmacr,'SPOT-FROZEN',1,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0324","original_return_source_line":324,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipmacr,'SPOT-FROZEN',frozen_flag)
    if (frozen_flag /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0326","original_return_source_line":326,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipmacr,'SPOT-KEFF',1,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0327","original_return_source_line":327,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipmacr,'SPOT-KEFF',macro_keff32)
    if (.not. ieee_is_finite(macro_keff32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0329","original_return_source_line":329,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (macro_keff32 <= 0.0_real32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0330","original_return_source_line":330,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'LINK.MACRO',3,12, &
        'MACRO0')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0333","original_return_source_line":333,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(ipsys,'LINK.TRACK',3,12, &
        'TRACK')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0335","original_return_source_line":335,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsys,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0336","original_return_source_line":336,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsys,'STATE-VECTOR',system_state)
    if (any(system_state(1:14) /= &
        [1,1,1,0,1,1,4,NGRP,nunkno,nmat,1,0,0,0])) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0339","original_return_source_line":339,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsys,'SPOT-LEAK1D',NGRP,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0340","original_return_source_line":340,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsys,'SPOT-LEAK1D',leak1d_input32)
    if (.not. all(ieee_is_finite(leak1d_input32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0342","original_return_source_line":342,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. RECORD_MATCHES(iptrk,'TITLE',18,3)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0344","original_return_source_line":344,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    title = ' '
    call LCMGTC(iptrk,'TITLE',72,title)
    if (title /= 'SAL TRACKING') then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0347","original_return_source_line":347,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'TRACK-TYPE',3,12, &
        'MCCG')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0349","original_return_source_line":349,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. CHARACTER_RECORD_MATCHES(iptrk,'LINK.FTRACK',3,12, &
        'TRACK_f')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0351","original_return_source_line":351,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (track_state(9) /= 0 .or. track_state(14) /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0352","original_return_source_line":352,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (track_state(16) /= 2 .or. track_state(22) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0353","original_return_source_line":353,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (track_state(27) < 0 .or. track_state(39) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0354","original_return_source_line":354,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (track_state(40) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0355","original_return_source_line":355,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(iptrk,'MCCG-STATE',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0356","original_return_source_line":356,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'MCCG-STATE',mccg_state)
    if (mccg_state(2) /= 4 .or. mccg_state(3) /= 10) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0358","original_return_source_line":358,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(4) /= 0 .or. mccg_state(5) <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0359","original_return_source_line":359,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(6) <= 0 .or. mccg_state(7) /= 80) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0360","original_return_source_line":360,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(8) /= 0 .or. mccg_state(9) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0361","original_return_source_line":361,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    paca = mccg_state(10)
    lc0 = mccg_state(17)
    if (paca /= 3 .and. paca /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0364","original_return_source_line":364,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(12) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0365","original_return_source_line":365,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (paca == 3) then
      if (lc0 <= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0367","original_return_source_line":367,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(iptrk,'IM0$MCCG',nlong+1,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0368","original_return_source_line":368,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(iptrk,'MCU0$MCCG',lc0,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0369","original_return_source_line":369,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      allocate(ilucf_stage32(lc0),stat=allocation_status)
      if (allocation_status /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0371","original_return_source_line":371,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    else
      if (lc0 /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0373","original_return_source_line":373,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. ABSENT_RECORD(iptrk,'IM0$MCCG')) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0374","original_return_source_line":374,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. ABSENT_RECORD(iptrk,'MCU0$MCCG')) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0375","original_return_source_line":375,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end if
    if (mccg_state(13) /= 20 .or. mccg_state(15) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0377","original_return_source_line":377,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(16) /= 1 .or. mccg_state(18) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0378","original_return_source_line":378,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (mccg_state(19) /= 1 .or. mccg_state(20) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0379","original_return_source_line":379,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(iptrk,'REAL-PARAM',4,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0380","original_return_source_line":380,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'REAL-PARAM',real_param32)
    if (.not. all(ieee_is_finite(real_param32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0382","original_return_source_line":382,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(real_param32(1),0_int32) /= &
        contract%eps_mccg_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0384","original_return_source_line":384,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(abs(real_param32(2:4)) > 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0385","original_return_source_line":385,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. RECORD_MATCHES(iptrk,'MATCOD',nreg,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0387","original_return_source_line":387,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'MATCOD',matcod)
    if (.not. RECORD_MATCHES(iptrk,'VOLUME',nreg,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0389","original_return_source_line":389,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'VOLUME',vol32)
    if (.not. RECORD_MATCHES(iptrk,'KEYFLX$ANIS',nreg,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0391","original_return_source_line":391,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'KEYFLX$ANIS',keyflx_base1)
    if (any(seed_keyflx /= keyflx_base1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0393","original_return_source_line":393,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(iptrk,'KEYCUR$MCCG',nsou,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0394","original_return_source_line":394,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'KEYCUR$MCCG',keycur)
    if (.not. RECORD_MATCHES(iptrk,'NZON$MCCG',nlong,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0396","original_return_source_line":396,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'NZON$MCCG',nzon)
    if (.not. RECORD_MATCHES(iptrk,'V$MCCG',nlong,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0398","original_return_source_line":398,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'V$MCCG',volume_track32)
    if (.not. RECORD_MATCHES(iptrk,'ALBEDO',NALBEDO,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0400","original_return_source_line":400,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(iptrk,'ALBEDO',albedo32)

    if (any(matcod < 1) .or. any(matcod > nmat)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0403","original_return_source_line":403,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(nzon(1:nreg) /= matcod)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0404","original_return_source_line":404,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(nzon(nreg+1:nlong) < -NALBEDO)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0405","original_return_source_line":405,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(nzon(nreg+1:nlong) > -1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0406","original_return_source_line":406,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. all(ieee_is_finite(vol32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0407","original_return_source_line":407,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. all(ieee_is_finite(volume_track32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0408","original_return_source_line":408,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(vol32 <= 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0409","original_return_source_line":409,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(volume_track32 <= 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0410","original_return_source_line":410,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    do ir = 1, nreg
      volume_bits = transfer(vol32(ir),0_int32)
      track_volume_bits = transfer(volume_track32(ir),0_int32)
      if (volume_bits /= track_volume_bits) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0414","original_return_source_line":414,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end do
    if (.not. all(ieee_is_finite(albedo32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0416","original_return_source_line":416,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    matalb_surface = nzon(nreg+1:nlong)
    surfac32 = volume_track32(nreg+1:nlong)

    seen_unknown = .false.
    do ir = 1, nreg
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > nunkno) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0422","original_return_source_line":422,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (seen_unknown(keyflx_base1(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0423","original_return_source_line":423,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      seen_unknown(keyflx_base1(ir)) = .true.
    end do
    do ir = 1, nsou
      if (keycur(ir) < 1 .or. keycur(ir) > nunkno) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0427","original_return_source_line":427,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (seen_unknown(keycur(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0428","original_return_source_line":428,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      seen_unknown(keycur(ir)) = .true.
    end do
    if (.not. all(seen_unknown)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0431","original_return_source_line":431,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. ABSENT_RECORD(ipsou,'NORM-FS')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0433","original_return_source_line":433,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. ABSENT_RECORD(ipsou,'NBS')) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0434","original_return_source_line":434,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsou,'STATE-VECTOR',NSTATE,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0435","original_return_source_line":435,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsou,'STATE-VECTOR',source_state)
    if (source_state(1) /= NGRP .or. source_state(2) /= nunkno) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0437","original_return_source_line":437,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (source_state(3) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0438","original_return_source_line":438,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (any(source_state(4:NSTATE) /= 0)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0439","original_return_source_line":439,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsou,'SPOT-FROZEN',1,1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0440","original_return_source_line":440,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsou,'SPOT-FROZEN',frozen_flag)
    if (frozen_flag /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0442","original_return_source_line":442,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsou,'SPOT-KEFF',1,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0443","original_return_source_line":443,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsou,'SPOT-KEFF',source_keff32)
    if (.not. ieee_is_finite(source_keff32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0445","original_return_source_line":445,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (source_keff32 <= 0.0_real32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0446","original_return_source_line":446,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (transfer(source_keff32,0_int32) /= &
        transfer(macro_keff32,0_int32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0448","original_return_source_line":448,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (.not. RECORD_MATCHES(ipsou,'SPOT-QINT',NGRP,2)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0449","original_return_source_line":449,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    call LCMGET(ipsou,'SPOT-QINT',qint32)
    if (.not. all(ieee_is_finite(qint32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0451","original_return_source_line":451,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    ! CONT may cross the transport boundary only when its three committed
    ! authorities satisfy one exact projected-source-system predicate set at
    ! the required local stage label.  This is not a global lineage claim. The
    ! comparison is exact: no tolerance, fitted coefficient, or repair path
    ! is available.  BOOT deliberately retains its one-time legacy ingress.
    if (r64_mode == SPOR64_BOOTB64_CONT) then
      if (.not. CONT_LIFECYCLE_IS_BOUND(ipseed,ipsou,ipsys, &
          seed_leak1d32,leak1d_input32)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0460","original_return_source_line":460,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end if

    call SPOR64_BOOT_BIND64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,requested_rank,boot_plane, &
        ipseed,iptrk,ipsys,ipmacr,ipsou,initial_flux64,fixed_source64,leak1d64,boot_bound)
    if (.not. boot_bound) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0466","original_return_source_line":466,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    xcsou1 = +0.0_real64
    do ir = 1, nreg
      xcsou1 = xcsou1 + fixed_source64(keyflx_base1(ir),1) * &
          real(vol32(ir),real64)
    end do
    if (.not. ieee_is_finite(xcsou1) .or. xcsou1 <= 0.0_real64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0473","original_return_source_line":473,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif

    if (.not. RECORD_MATCHES(ipmacr,'GROUP',NGRP,10)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0475","original_return_source_line":475,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    jpmacr = LCMGID(ipmacr,'GROUP')
    if (.not. c_associated(jpmacr)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0477","original_return_source_line":477,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    allocate(scat_off32(max_scat,NGRP),stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0479","original_return_source_line":479,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    scat_off32 = +0.0_real32
    njj_off = 0
    ijj_off = 0
    ipos_off = 0
    nscat_off = 0
    do ig = 1, NGRP
      kpmacr = LCMGIL(jpmacr,ig)
      if (.not. c_associated(kpmacr)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0487","original_return_source_line":487,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpmacr,'NJJS01',nmat,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0488","original_return_source_line":488,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpmacr,'NJJS02',nmat,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0489","original_return_source_line":489,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpmacr,'NUSIGF',nmat*NIFIS,2)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0490","original_return_source_line":490,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpmacr,'NUSIGF',nusigf_stage32)
      if (.not. all(ieee_is_finite(nusigf_stage32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0492","original_return_source_line":492,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (any(abs(nusigf_stage32) > 0.0_real32)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0493","original_return_source_line":493,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpmacr,'NJJS00',nmat,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0494","original_return_source_line":494,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpmacr,'NJJS00',njj_stage)
      if (.not. RECORD_MATCHES(kpmacr,'IJJS00',nmat,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0496","original_return_source_line":496,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpmacr,'IJJS00',ijj_stage)
      if (.not. RECORD_MATCHES(kpmacr,'IPOS00',nmat,1)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0498","original_return_source_line":498,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpmacr,'IPOS00',ipos_stage)
      call LCMLEN(kpmacr,'SCAT00',ilong,itylcm)
      if (ilong < 0 .or. ilong > max_scat .or. itylcm /= 2) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0501","original_return_source_line":501,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (ilong > 0) then
        allocate(scat_stage32(ilong),stat=allocation_status)
        if (allocation_status /= 0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0504","original_return_source_line":504,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        call LCMGET(kpmacr,'SCAT00',scat_stage32)
        if (.not. all(ieee_is_finite(scat_stage32))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0506","original_return_source_line":506,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
      end if
      do ibm = 1, nmat
        if (njj_stage(ibm) < 0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0509","original_return_source_line":509,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        if (njj_stage(ibm) == 0) cycle
        if (ipos_stage(ibm) < 1) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0511","original_return_source_line":511,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        last_position = ipos_stage(ibm) + njj_stage(ibm) - 1
        if (last_position > ilong) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0513","original_return_source_line":513,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        if (ijj_stage(ibm) < 1 .or. ijj_stage(ibm) > NGRP) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0514","original_return_source_line":514,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        if (ijj_stage(ibm)-njj_stage(ibm)+1 < 1) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0515","original_return_source_line":515,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
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

    if (.not. RECORD_MATCHES(ipsys,'GROUP',NGRP,10)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0527","original_return_source_line":527,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    jpsys = LCMGID(ipsys,'GROUP')
    if (.not. c_associated(jpsys)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0529","original_return_source_line":529,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    xstrc32 = +0.0_real32
    xsdia0_32 = +0.0_real32
    do ig = 1, NGRP
      kpsys = LCMGIL(jpsys,ig)
      if (.not. c_associated(kpsys)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0534","original_return_source_line":534,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpsys,'DRAGON-TXSC',nmat+1,2)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0535","original_return_source_line":535,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpsys,'DRAGON-TXSC',xstrc32(:,ig))
      if (.not. all(ieee_is_finite(xstrc32(:,ig)))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0537","original_return_source_line":537,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (.not. RECORD_MATCHES(kpsys,'DRAGON-S0XSC',nmat+1,2)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0538","original_return_source_line":538,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      call LCMGET(kpsys,'DRAGON-S0XSC',xsdia0_32(:,ig))
      if (.not. all(ieee_is_finite(xsdia0_32(:,ig)))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0540","original_return_source_line":540,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
      if (paca == 3) then
        if (.not. RECORD_MATCHES(kpsys,'ILUCF$MCCG',lc0,2)) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0542","original_return_source_line":542,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        call LCMGET(kpsys,'ILUCF$MCCG',ilucf_stage32)
        if (.not. all(ieee_is_finite(ilucf_stage32))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0544","original_return_source_line":544,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
      else
        if (.not. ABSENT_RECORD(kpsys,'ILUCF$MCCG')) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0546","original_return_source_line":546,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
      end if
      if (have_leak1d64) then
        ! REAL64 leakage mode: the system must be UNREDUCED, i.e. the
        ! stored self-scattering must be bitwise the physical one.
        if (.not. RECORD_MATCHES(kpsys,'SPOT-S0-PHYS',nmat+1,2)) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
            '"predicate_id":"BOOTB_INGRESS_RETURN_L0551","original_return_source_line":551,'// &
            '"actual_return_status":',status,'}'
          flush(6)
          return
        endif
        call LCMGET(kpsys,'SPOT-S0-PHYS',s0phys_stage32)
        do ibm = 1, nmat
          if (transfer(xsdia0_32(ibm,ig),0_int32) /= &
              transfer(s0phys_stage32(ibm+1),0_int32)) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
              '"predicate_id":"BOOTB_INGRESS_RETURN_L0555","original_return_source_line":555,'// &
              '"actual_return_status":',status,'}'
            flush(6)
            return
          endif
        end do
      end if
      xsdia0_32(0,ig) = +0.0_real32
      call LCMLEN(kpsys,'FUNKNO$USS',ilong,itylcm)
      if (ilong /= 0 .or. itylcm /= 99) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
          '"predicate_id":"BOOTB_INGRESS_RETURN_L0560","original_return_source_line":560,'// &
          '"actual_return_status":',status,'}'
        flush(6)
        return
      endif
    end do

    admission_complete = .true.
    if (.not. admission_complete) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1",'// &
        '"predicate_id":"BOOTB_INGRESS_RETURN_L0564","original_return_source_line":564,'// &
        '"actual_return_status":',status,'}'
      flush(6)
      return
    endif
    if (r64_mode == SPOR64_BOOTB64_CONT) then
      call LCMGET(ipsys,'SPOT-L1-SNAP',plane_index)
      write(6,'(A,I0)') ' SPOR64_BOOTB64-CENSUS: PLANE=', plane_index
      flush(6)
    end if
    call XDRTA2
    call FLU2DR64_CORE(jpsys,iptrk,iftrak,iprint,title, &
        keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
        matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
        nscat_off,scat_off32,fixed_source64,initial_flux64, &
        leak1d64,real(epsinr32,real64),real(epsunk32,real64), &
        real(epsout32,real64),contract,terminal_flux64, &
        terminal_source64, &
        cutoff_visit64,accepted,core_ok)

    if (.not. core_ok) then
      status = SPOR64_BOOTB64_CORE_FAILED
    else if (.not. accepted) then
      status = SPOR64_BOOTB64_NOT_ACCEPTED
    else
      status = SPOR64_BOOTB64_ACCEPTED_UNPUBLISHED
      if (r64_mode == SPOR64_BOOTB64_CONT) then
        call SPOR64_BOOTC64_PUBLISH_CONT(ipflux,ipseed, &
            SPOR64_BOOTB64_ACCEPTED_UNPUBLISHED,terminal_flux64, &
            terminal_source64,keyflx_base1,nmerg,imerg,leak1d_input32, &
            leak1d64,epsout32,epsunk32,epsinr32,coptio,hentry(2), &
            hentry(3),hentry(5),contract,status)
      else
        call SPOR64_BOOTC64_PUBLISH(ipflux,SPOR64_BOOTB64_ACCEPTED_UNPUBLISHED, &
            terminal_flux64,terminal_source64,keyflx_base1,nmerg,imerg, &
            leak1d_input32,leak1d64,epsout32,epsunk32,epsinr32,coptio, &
            hentry(2),hentry(3),hentry(5),contract,status)
      end if
    end if
  end subroutine SPOR64_BOOTB64_INGRESS


  logical function CONT_LIFECYCLE_IS_BOUND(ipseed,ipsource,ipsystem, &
      seed_leakage,system_leakage)
    type(c_ptr), intent(in) :: ipseed, ipsource, ipsystem
    real(real32), intent(in) :: seed_leakage(:), system_leakage(:)

    integer, parameter :: NPLANE = 3
    integer :: seed_epoch, source_epoch, system_epoch
    integer :: seed_plane, source_plane, system_plane
    real(real64) :: seed_rho64, source_rho64, system_rho64
    type(c_ptr) :: seed_authority, source_authority, system_authority

    CONT_LIFECYCLE_IS_BOUND = .false.
    if (.not. c_associated(ipseed)) return
    if (.not. c_associated(ipsource)) return
    if (.not. c_associated(ipsystem)) return
    if (size(seed_leakage) /= NGRP) return
    if (size(system_leakage) /= NGRP) return

    if (.not. RECORD_MATCHES(ipseed,'SPOT-R64',-1,0)) return
    if (.not. RECORD_MATCHES(ipsource,'SPOT-R64',-1,0)) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-R64',-1,0)) return
    seed_authority = LCMGID(ipseed,'SPOT-R64')
    source_authority = LCMGID(ipsource,'SPOT-R64')
    system_authority = LCMGID(ipsystem,'SPOT-R64')
    if (.not. c_associated(seed_authority)) return
    if (.not. c_associated(source_authority)) return
    if (.not. c_associated(system_authority)) return
    if (.not. CONT_SEED_AUTHORITY_IS_EXACT(seed_authority)) return
    if (.not. CONT_SOURCE_AUTHORITY_IS_EXACT(source_authority)) return
    if (.not. CONT_SYSTEM_AUTHORITY_IS_EXACT(system_authority)) return

    if (.not. RECORD_MATCHES(seed_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(seed_authority,'PLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(seed_authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(seed_authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(source_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(source_authority,'PLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(source_authority,'STATE',3,12, &
        'FROZEN-QFIS')) return
    if (.not. RECORD_MATCHES(source_authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(system_authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(system_authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(system_authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-L1-SNAP',1,1)) return

    call LCMGET(seed_authority,'RHO',seed_rho64)
    call LCMGET(seed_authority,'PLANE',seed_plane)
    call LCMGET(seed_authority,'EPOCH',seed_epoch)
    call LCMGET(source_authority,'RHO',source_rho64)
    call LCMGET(source_authority,'PLANE',source_plane)
    call LCMGET(source_authority,'EPOCH',source_epoch)
    call LCMGET(system_authority,'RHO',system_rho64)
    call LCMGET(system_authority,'EPOCH',system_epoch)
    call LCMGET(ipsystem,'SPOT-L1-SNAP',system_plane)

    if (.not. ieee_is_finite(seed_rho64)) return
    if (.not. ieee_is_finite(source_rho64)) return
    if (.not. ieee_is_finite(system_rho64)) return
    if (seed_rho64 <= +0.0_real64) return
    if (source_rho64 <= +0.0_real64) return
    if (system_rho64 <= +0.0_real64) return
    if (transfer(seed_rho64,0_int64) /= &
        transfer(source_rho64,0_int64)) return
    if (transfer(seed_rho64,0_int64) /= &
        transfer(system_rho64,0_int64)) return
    ! The continuation epoch is dynamic: the three authorities must
    ! agree exactly among themselves; no fixed epoch is pinned.
    if (seed_epoch < 1) return
    if (source_epoch /= seed_epoch) return
    if (system_epoch /= seed_epoch) return
    if (source_plane < 1 .or. source_plane > NPLANE) return
    if (seed_plane /= source_plane) return
    if (system_plane /= source_plane) return
    if (.not. SAME_REAL32_BITS(seed_leakage,system_leakage)) return

    CONT_LIFECYCLE_IS_BOUND = .true.
  end function CONT_LIFECYCLE_IS_BOUND


  logical function LCM_ENTRY_KIND(kind_value)
    integer, intent(in) :: kind_value

    LCM_ENTRY_KIND = kind_value == 1 .or. kind_value == 2
  end function LCM_ENTRY_KIND
  logical function CONT_SEED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CONT_SEED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_PLANE_SEED_AUTHORITY)
  end function CONT_SEED_AUTHORITY_IS_EXACT


  logical function CONT_SOURCE_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CONT_SOURCE_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOURCE_AUTHORITY)
  end function CONT_SOURCE_AUTHORITY_IS_EXACT


  logical function CONT_SYSTEM_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CONT_SYSTEM_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_AUTHORITY)
  end function CONT_SYSTEM_AUTHORITY_IS_EXACT
end module SPOR64_BOOTB64

program test_b2h_runtime_geometry
  ! No-transport projection test.  The pin case locks the existing record
  ! arithmetic; the manufactured D4-A tuple proves runtime sizing only.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use GANLIB
  use SPOR64_B2H, only : SPOR64_B2H_PROJECTED_COMMITTED, &
      SPOR64_B2H_PROJECT
  implicit none

  call run_case(8,8,6)
  call run_case(132,6,12)
  write(*,'(A)') &
      'B2H RUNTIME-GEOMETRY PASS: pin and D4-A (132,144,12) tuple projection only.'

contains

  subroutine run_case(nreg,nmat,nsurf)
    integer, intent(in) :: nreg, nmat, nsurf
    integer, parameter :: ngrp=370, ncode=6, nstate=40
    integer(int32), parameter :: tol_bits=int(z'348637bd',int32)
    integer :: nunkno, ig, ir, status, ilong, itylcm
    integer :: state(nstate), keyflx(nreg), keycur(nsurf)
    integer :: nzon(nreg+nsurf), imerge(nmat), found_state(nstate)
    real(real32) :: track_volume(nreg+nsurf), eps(5), leakage(ngrp)
    real(real64) :: rho64, phi(nreg+nsurf), projected(nreg,ngrp)
    real(real64) :: found64(nreg+nsurf)
    real(real32) :: found32(nreg+nsurf)
    character(len=12) :: name, text12
    character(len=4) :: option
    type(c_ptr) :: track, seed, output, authority
    type(c_ptr) :: flux, source, output_flux, legacy_flux

    nunkno = nreg+nsurf
    write(name,'("B2H-T",I3.3)') nreg
    call LCMOP(track,trim(name),0,1,0)
    if (.not. c_associated(track)) error stop 'TRACK CREATE'
    write(name,'("B2H-S",I3.3)') nreg
    call LCMOP(seed,trim(name),0,1,0)
    if (.not. c_associated(seed)) error stop 'SEED CREATE'
    write(name,'("B2H-O",I3.3)') nreg
    call LCMOP(output,trim(name),0,1,0)
    if (.not. c_associated(output)) error stop 'OUTPUT CREATE'

    text12 = 'L_TRACK'
    call LCMPTC(track,'SIGNATURE',12,text12)
    state = 0
    state(1:6) = [nreg,nunkno,1,nmat,nsurf,1]
    call LCMPUT(track,'STATE-VECTOR',nstate,1,state)
    track_volume = 1.0_real32
    nzon = 1
    do ir = 1, nreg
      keyflx(ir) = ir
    end do
    do ir = 1, nsurf
      keycur(ir) = nreg+ir
      nzon(nreg+ir) = -(1+mod(ir-1,ncode))
    end do
    call LCMPUT(track,'V$MCCG',nunkno,2,track_volume)
    call LCMPUT(track,'NZON$MCCG',nunkno,1,nzon)
    call LCMPUT(track,'KEYCUR$MCCG',nsurf,1,keycur)
    call LCMPUT(track,'KEYFLX$ANIS',nreg,1,keyflx)

    text12 = 'L_FLUX'
    call LCMPTC(seed,'SIGNATURE',12,text12)
    state = 0
    state(1:3) = [ngrp,nunkno,1]
    state(8:12) = [3,3,1,740,500]
    state(17:18) = [nmat,1]
    call LCMPUT(seed,'STATE-VECTOR',nstate,1,state)
    eps = 0.0_real32
    eps(1:3) = transfer(tol_bits,0.0_real32)
    imerge = 1
    leakage = 0.0_real32
    call LCMPUT(seed,'EPS-CONVERGE',5,2,eps)
    call LCMPUT(seed,'IMERGE-LEAK',nmat,1,imerge)
    call LCMPUT(seed,'KEYFLX',nreg,1,keyflx)
    option = 'B0  '
    call LCMPTC(seed,'OPTION',4,option)
    text12 = 'MACRO0'
    call LCMPTC(seed,'LINK.MACRO',12,text12)
    text12 = 'TRACK'
    call LCMPTC(seed,'LINK.TRACK',12,text12)
    text12 = 'SYSTEM'
    call LCMPTC(seed,'LINK.SYSTEM',12,text12)
    call LCMPUT(seed,'SPOT-LEAK1D',ngrp,2,leakage)

    authority = LCMDID(seed,'SPOT-R64')
    text12 = 'SOLVED'
    call LCMPTC(authority,'STATE',12,text12)
    call LCMPUT(authority,'EPOCH',1,1,7)
    rho64 = 0.75_real64
    call LCMPUT(authority,'RHO',1,4,rho64)
    flux = LCMLID(authority,'FLUX',ngrp)
    source = LCMLID(authority,'SOUR',ngrp)
    do ig = 1, ngrp
      do ir = 1, nunkno
        phi(ir) = 1.0_real64 + real(ir+ig,real64)*1.0e-8_real64
      end do
      call LCMPDL(flux,ig,nunkno,4,phi)
      call LCMPDL(source,ig,nunkno,4,phi)
      do ir = 1, nreg
        projected(ir,ig) = 2.0_real64 + &
            real(2*ir+ig,real64)*1.0e-8_real64
      end do
    end do

    call SPOR64_B2H_PROJECT(output,seed,track,projected,rho64,status)
    if (status /= SPOR64_B2H_PROJECTED_COMMITTED) &
      error stop 'VALID RUNTIME CASE REJECTED'
    call LCMGET(output,'STATE-VECTOR',found_state)
    if (found_state(2) /= nunkno .or. found_state(17) /= nmat) &
      error stop 'OUTPUT STATE EXTENTS'
    call LCMLEN(output,'IMERGE-LEAK',ilong,itylcm)
    if (ilong /= nmat .or. itylcm /= 1) error stop 'IMERGE EXTENT'
    call LCMLEN(output,'KEYFLX',ilong,itylcm)
    if (ilong /= nreg .or. itylcm /= 1) error stop 'KEYFLX EXTENT'
    authority = LCMGID(output,'SPOT-R64')
    output_flux = LCMGID(authority,'FLUX')
    legacy_flux = LCMGID(output,'FLUX')
    do ig = 1, ngrp
      call LCMLEL(output_flux,ig,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 4) error stop 'R64 EXTENT'
      call LCMLEL(legacy_flux,ig,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 2) error stop 'R32 EXTENT'
      call LCMGDL(output_flux,ig,found64)
      call LCMGDL(legacy_flux,ig,found32)
      do ir = 1, nunkno
        if (transfer(found32(ir),0_int32) /= &
            transfer(real(found64(ir),real32),0_int32)) &
          error stop 'PROJECTED MIRROR'
      end do
      do ir = 1, nreg
        if (transfer(found64(ir),0_int64) /= &
            transfer(projected(ir,ig),0_int64)) &
          error stop 'PROJECTED VALUE'
      end do
      do ir = nreg+1, nunkno
        phi(ir) = 1.0_real64 + real(ir+ig,real64)*1.0e-8_real64
        if (transfer(found64(ir),0_int64) /= transfer(phi(ir),0_int64)) &
          error stop 'SURFACE VALUE NOT PRESERVED'
      end do
    end do

    call LCMCL(output,2)
    call LCMCL(seed,2)
    call LCMCL(track,2)
  end subroutine run_case

end program test_b2h_runtime_geometry

program test_radial_closure
  use, intrinsic :: iso_fortran_env, only : error_unit
  use SPOT_LEAKAGE, only : SPOLE2,SPOF00,SPOQ00,SPOQFS
  implicit none
  integer, parameter :: nr=2
  integer :: failures
  real :: area(nr),total(nr),scatter0(nr),phi(nr),source(nr)
  real :: expected(nr),radial(nr),radial_scaled(nr),radial_zero(nr)
  real :: balance
  integer, parameter :: ng=3,nmix=2,nfis=2
  integer :: matq(nr),njjs(nmix),ijjs(nmix),ipos(nmix)
  real :: phiq(nr,ng),scat(5),chi(nmix,nfis)
  real :: nusigf(nmix,nfis,ng),qtotal(nr),q_k4(nr)
  real :: q_precomputed(nr),qfrozen(nr),q_fixed_source(nr)
  double precision :: fisprod(nr,nfis)
  real :: removal(nr),lagged_source(nr),trial(nr)

  failures=0
  area=[2.0,1.0]
  total=[1.0,0.8]
  scatter0=[0.3,0.2]
  phi=[2.0,4.0]
  expected=[0.1,-0.1]

  ! Offline snapshots contain no imposed axial leakage.  Construct a source
  ! whose scalar balance has the prescribed radial current divergence.
  source=phi*(expected+total-scatter0)
  radial=SPOLE2(total,scatter0,source,phi,0.0)
  call assert_close('radial closure region 1',radial(1),expected(1), &
                    2.0e-7,failures)
  call assert_close('radial closure region 2',radial(2),expected(2), &
                    2.0e-7,failures)
  call assert_true('positive closure denotes radial loss', &
                   radial(1) > 0.0,failures)
  call assert_true('negative closure denotes radial gain', &
                   radial(2) < 0.0,failures)

  balance=sum(area*phi*radial)
  call assert_close('reflective radial integral balance',balance,0.0, &
                    5.0e-7,failures)

  radial_scaled=SPOLE2(total,scatter0,3.0*source,3.0*phi,0.0)
  call assert_true('radial closure is flux-normalization invariant', &
                   maxval(abs(radial_scaled-radial)) < 2.0e-7,failures)

  radial_zero=SPOLE2(total,scatter0,phi*(total-scatter0),phi,0.0)
  call assert_true('zero radial-divergence limit', &
                   maxval(abs(radial_zero)) < 2.0e-7,failures)

  ! Hand calculation for target group 2.  Mix 1 has compressed entries
  ! g=3,2,1 and mix 2 has g=2,1.  The self-scattering entries (g=2)
  ! must not enter qtotal.
  matq=[1,2]
  phiq=reshape([2.0,7.0,3.0,11.0,5.0,13.0],shape(phiq))
  njjs=[3,2]
  ijjs=[3,2]
  ipos=[1,4]
  scat=[0.1,0.2,0.3,0.4,0.5]
  chi=reshape([0.25,0.5,0.1,0.2],shape(chi))
  nusigf=0.0
  nusigf(1,1,:)=[0.2,0.4,0.6]
  nusigf(1,2,:)=[0.1,0.0,0.2]
  nusigf(2,1,:)=[0.01,0.02,0.03]
  nusigf(2,2,:)=[0.04,0.05,0.06]
  call SPOQ00(nr,ng,nmix,nfis,2,matq,phiq,2.0,njjs,ijjs,ipos, &
              scat,chi,nusigf,qtotal)
  call assert_close('P0 final source region 1',qtotal(1),1.735, &
                    3.0e-7,failures)
  call assert_close('P0 final source region 2',qtotal(2),3.831, &
                    5.0e-7,failures)
  call assert_true('P0 compressed map excludes self scattering', &
                   abs(qtotal(1)-(1.735+0.2*3.0)) > 0.5,failures)
  call SPOF00(nr,ng,nmix,nfis,matq,phiq,nusigf,fisprod)
  call SPOQ00(nr,ng,nmix,nfis,2,matq,phiq,2.0,njjs,ijjs,ipos, &
              scat,chi,nusigf,q_precomputed,fisprod)
  call assert_true('precomputed fission path is bit identical', &
                   all(q_precomputed == qtotal),failures)

  ! An online radial update must keep the fission source formed from the
  ! preceding restricted axial field. Only off-group scattering is rebuilt
  ! from the final radial field.
  qfrozen=[0.7,1.2]
  call SPOQFS(nr,ng,nmix,2,matq,phiq,njjs,ijjs,ipos,scat, &
              qfrozen,q_fixed_source)
  call assert_close('fixed-source RHS region 1',q_fixed_source(1),1.8, &
                    3.0e-7,failures)
  call assert_close('fixed-source RHS region 2',q_fixed_source(2),4.7, &
                    5.0e-7,failures)
  call assert_true('fixed fission is not replaced by final-field fission', &
                   maxval(abs(q_fixed_source-qtotal)) > 0.5,failures)

  ! The accepted source must use the final eigenvalue.  Doubling k leaves
  ! off-group scattering unchanged and halves only the fission contribution.
  call SPOQ00(nr,ng,nmix,nfis,2,matq,phiq,4.0,njjs,ijjs,ipos, &
              scat,chi,nusigf,q_k4)
  call assert_close('P0 final-k dependence region 1',q_k4(1),1.4175, &
                    3.0e-7,failures)
  call assert_close('P0 final-k dependence region 2',q_k4(2),3.6655, &
                    5.0e-7,failures)

  ! A synthetic Galerkin balance closes with q_final by construction.  A
  ! distinct saved/lagged work source does not, so it cannot be substituted
  ! into an acceptance residual.
  removal=qtotal/phiq(:,2)
  trial=[0.6,0.8]
  lagged_source=qtotal+[0.1,-0.05]
  call assert_close('q_final Galerkin closure', &
                    sum(trial*(removal*phiq(:,2)-qtotal)),0.0, &
                    2.0e-7,failures)
  call assert_true('lagged work source is not an acceptance source', &
                   abs(sum(trial*(removal*phiq(:,2)-lagged_source))) > &
                   1.0e-3,failures)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'RADIAL CLOSURE TEST FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a)') &
    'RADIAL CLOSURE PASS: physical P0 source, signs, normalization, balance.'

contains
  subroutine assert_close(label,value,expected_value,tolerance,failures)
    character(*), intent(in) :: label
    real, intent(in) :: value,expected_value,tolerance
    integer, intent(inout) :: failures
    call assert_true(label,abs(value-expected_value) <= tolerance,failures)
  end subroutine assert_close

  subroutine assert_true(label,condition,failures)
    character(*), intent(in) :: label
    logical, intent(in) :: condition
    integer, intent(inout) :: failures
    if (condition) then
      write(*,'(a)') 'PASS: '//label
    else
      write(error_unit,'(a)') 'FAIL: '//label
      failures=failures+1
    endif
  end subroutine assert_true
end program test_radial_closure

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT

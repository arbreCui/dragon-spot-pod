!
!-----------------------------------------------------------------------
!
!Purpose:
! POD-based constraint-preserving compression of the radial leakage
! matrix L^{2D} for the SPOT (Synthesis Proper Orthogonal Decomposition)
! method, VARIANT III': POD on the volume-weighted PURE-RADIAL leakage
! current density
!     Y'_{i,k} := V_i * ( L^{2D}_{i,k} + L^{1D}_k ) * phi^k_i.
!
! Why Y' and not Y = V*L2D*phi (the original Variant III variable):
! from the SPOASM assembly
!     L^{2D}_{i,k} = -Sigma_t + Sigma_s0 - L^{1D}_k + Q_i/phi_i,
! the converged 2D MOC snapshot balance gives
!     1^T Y[:,k] = - L^{1D}_{g,k} * sum_i V_i phi^k_i,
! which vanishes ONLY when L1D = 0, i.e. only at the first outer
! iteration. (Measured in d3_sanity.log: |1^T Y| jumps from ~1e-11
! at ASM call 1 to ~1e-4 at calls 2-3.) The shifted variable Y'
! removes the known axial-leakage share, so its column sums equal the
! pure 2D radial balance and stay at the assembly-rounding level
! (single-precision DB2 assembly in SPOASM plus the 2D MOC
! convergence residual) at EVERY outer iteration, instead of growing
! with L1D. The zero-column-sum property is inherited by all
! left singular vectors with nonzero singular value (elementary
! column-space property of the SVD), hence ANY filtered reconstruction
! built from those vectors preserves the constraint exactly.
!
! Algorithm:
!   1. Build Y'_{i,k} = V_i * ( L^{2D}_{i,k} + L^{1D}_k ) * phi^k_i.
!   2. Pre-verify  | 1^T Y'[:,k] |_inf < tol * |Y'|_F.
!   3. Standard thin SVD (unweighted): Y' = U Sigma V^T.
!   4. Tikhonov filter factors instead of a hard rank cutoff:
!         f_a = sigma_a^2 / ( sigma_a^2 + (eps_pod*sigma_1)^2 ),
!      so f_a ~ 1 for sigma_a >> eps*sigma_1 and f_a ~ 0 below it,
!      with f = 1/2 exactly at the old cutoff sigma_a = eps*sigma_1.
!      The map Y' -> tilde Y' is then Lipschitz in the data: a 1-ulp
!      perturbation of the spectrum (e.g. FMA/SIMD reordering) can no
!      longer flip a whole rank and move k by O(1 pcm), which the old
!      strict-inequality cutoff did (see README, -O3 note).
!      RANK_MAX > 0 remains a hard cap (f_a = 0 for a > RANK_MAX).
!   5. Filtered reconstruction: tilde Y' = sum_a f_a sigma_a u_a v_a^T.
!   6. Recover (S1: hard floor on phi):
!         tilde L^{2D}_{i,k} = tilde Y'_{i,k}/(V_i phi^k_i) - L^{1D}_k
!                                                   if phi^k_i >= phi_min
!         tilde L^{2D}_{i,k} = L^{2D}_{i,k}         otherwise.
!   7. Post-verify the constraint on V*(tilde L2D + L1D)*phi.
!      Note: cells taken through the S1 opt-out keep their original
!      (unfiltered) value, so the post residual is measured, not
!      asserted; it is machine-precision when no cell hits the floor.
!
! Computational complexity: O(N^2 K) per group when N >= K, dominated by
! ALSVDF. Energy-group loop is the natural parallelisation axis.
! ALSVDF (Golub-Reinsch) is retained deliberately: the per-group
! matrices are tiny (N_region x N_snap), and the former compiler
! sensitivity lived in the hard cutoff, not in the SVD itself.
!
!Copyright:
! Copyright (C) 2026 Ecole Polytechnique de Montreal.
!
!Author(s): B. Cui, Polytechnique Montreal (variant III', POD on the
!           volume-weighted pure-radial leakage current density), based
!           on the SPOT framework by A. Hebert.
!
!Parameters: input
! NREG2D    number of radial regions per snapshot (= N).
! NSNAP     number of snapshots (= K).
! PHI       array of snapshot zero-th Legendre fluxes,
!           PHI(I,K) = phi^K_I for radial region I, snapshot K.
! VOL       array of region volumes, VOL(I) = V_I for I=1..NREG2D.
! XL1D      per-snapshot axial leakage cross sections for this group,
!           XL1D(K) = L^{1D}_{g,K}. Zero at the first outer iteration.
! EPS_POD   relative filter tolerance (f=1/2 at sigma = eps*sigma_1).
!           <= 0 disables filtering; with RANK_MAX <= 0 or
!           RANK_MAX >= NSNAP the write-back is skipped entirely, so
!           DB2 leaves the routine bit-identical and the full-rank
!           control mode is exactly reproducible (only the spectrum
!           diagnostics are computed).
! RANK_MAX  explicit hard rank cap. 0 means automatic from EPS_POD only.
! PHI_MIN   hard floor on phi for safe recovery (S1 stabilisation).
!           0 means no floor (always do the reverse division).
! IMPX      print verbosity.
! IGR       energy-group index for diagnostics.
!
!Parameters: input/output
! DB2       DOUBLE PRECISION matrix, DB2(K,I), the radial leakage
!           cross sections L^{2D}_{i,k} for one energy group. Filtered
!           in place.
!
!Parameters: output
! RANK_USED  effective rank: number of modes with f_a > 1/2, i.e.
!            sigma_a > eps_pod*sigma_1, capped by RANK_MAX (1..NSNAP).
!            Reported for diagnostics; reconstruction uses the smooth
!            filter factors, not this integer.
! SIG_OUT    array of size min(NREG2D,NSNAP), the singular spectrum
!            of Y' (sorted descending).
! ERR_PRE    DOUBLE PRECISION, max | 1^T Y'[:,k] | / |Y'|_F before SVD.
!            Diagnoses the pure 2D radial balance of the snapshots;
!            bounded by the single-precision DB2 assembly rounding
!            (SPOASM) and the 2D MOC convergence residual, at every
!            outer iteration.
! ERR_POST   DOUBLE PRECISION, max | 1^T tildeY'[:,k] | / |tildeY'|_F
!            after filtering, measured on V*(tilde L2D + L1D)*phi.
!
!-----------------------------------------------------------------------
!
subroutine SPOPOD(NREG2D, NSNAP, DB2, PHI, VOL, XL1D, &
                  EPS_POD, RANK_MAX, PHI_MIN,          &
                  RANK_USED, SIG_OUT,                  &
                  ERR_PRE, ERR_POST,                   &
                  IMPX, IGR)
   implicit none
   integer, parameter :: dp = kind(1.0d0)
   integer, parameter :: IUNOUT = 6
   !----
   ! subroutine arguments
   !----
   integer, intent(in)            :: NREG2D, NSNAP, RANK_MAX, IMPX, IGR
   real,    intent(in)            :: EPS_POD, PHI_MIN
   double precision, intent(inout):: DB2(NSNAP, NREG2D)
   real,    intent(in)            :: PHI(NREG2D, NSNAP)
   real,    intent(in)            :: VOL(NREG2D)
   real,    intent(in)            :: XL1D(NSNAP)
   integer, intent(out)           :: RANK_USED
   double precision, intent(out)  :: SIG_OUT(*)
   double precision, intent(out)  :: ERR_PRE, ERR_POST
   !----
   ! local variables
   !----
   integer  :: M, N, ialpha, k, i
   double precision :: tol, smax, frob_full, frob_kept
   double precision :: ynorm_F, ymax, vphi, ysum_k, dnoise, fw
   logical  :: lexact
   double precision, allocatable :: Y(:,:), Yw(:,:), V(:,:), W(:), F(:)
   double precision, allocatable :: Ytilde(:,:)
   external :: ALSVDF
   !
   M = NREG2D
   N = NSNAP
   RANK_USED = N
   ERR_PRE  = 0.0d0
   ERR_POST = 0.0d0
   ! Always zero the full N-length output spectrum (callers like SPOASM
   ! write back NSNAP entries regardless of how many were used internally).
   ! Otherwise the M<N skip path or zero-spectrum branch leaves callers
   ! reading uninitialised tail.
   if (N > 0) SIG_OUT(1:N) = 0.0d0
   if (M <= 0 .or. N <= 0) return
   !
   !----
   ! Step 1: build Y'_{i,k} = V_i * ( L^{2D}_{i,k} + L^{1D}_k ) * phi^k_i
   !----
   allocate(Y(M, N))
   ynorm_F = 0.0d0
   ymax    = 0.0d0
   do i = 1, M
      do k = 1, N
         vphi = real(VOL(i), dp) * real(PHI(i, k), dp)
         Y(i, k) = vphi * (DB2(k, i) + real(XL1D(k), dp))
         ynorm_F = ynorm_F + Y(i, k)**2
         if (abs(Y(i,k)) > ymax) ymax = abs(Y(i,k))
      end do
   end do
   ynorm_F = sqrt(ynorm_F)
   !
   !----
   ! Step 2: pre-verify column-zero-sum (pure 2D radial balance)
   !----
   ERR_PRE = 0.0d0
   do k = 1, N
      ysum_k = 0.0d0
      do i = 1, M
         ysum_k = ysum_k + Y(i, k)
      end do
      if (abs(ysum_k) > ERR_PRE) ERR_PRE = abs(ysum_k)
   end do
   if (ynorm_F > 0.0d0) ERR_PRE = ERR_PRE / ynorm_F
   !
   ! Decide whether to actually do POD
   if (EPS_POD <= 0.0 .and. RANK_MAX <= 0) then
      ! POD disabled. Still report constraint violation if asked.
      RANK_USED = N
      ERR_POST  = ERR_PRE
      if (IMPX >= 2) then
         write(IUNOUT,'(A,I4,A,1P,E11.4)') &
           ' SPOPOD: group', IGR, &
           '  POD disabled, constraint residual=', ERR_PRE
      end if
      deallocate(Y)
      return
   end if
   !
   ! ALSVDF requires M >= N (tall-skinny). When M < N, no meaningful
   ! POD compression exists (rank cannot exceed M), skip silently.
   if (M < N) then
      RANK_USED = M
      ERR_POST  = ERR_PRE
      if (IMPX >= 1) then
         write(IUNOUT,'(A,I4,A,I0,A,I0,A)') &
           ' SPOPOD: group', IGR, &
           '  skipped (NREG2D=', M, ' < NSNAP=', N, ')'
      end if
      deallocate(Y)
      return
   end if
   !
   !----
   ! Step 3: Plan A -- direct unweighted SVD on Y'.
   !
   ! Earlier draft pre-multiplied by sqrt(V) ("V-weighted SVD") in
   ! the hope of recovering a V-inner-product-optimal basis. But Y'
   ! itself already contains the V_i factor, so the resulting Yw
   ! effectively carried V_i^{3/2} and minimised the ill-motivated
   ! functional sum_i V_i^3 (.)^2. Plan A drops that extra layer.
   !
   ! Constraint preservation does NOT require V-weighting: starting
   ! from 1^T Y'[:,k]=0, the column-zero-sum subspace invariance
   ! directly gives 1^T tildeY'[:,k]=0 for any reconstruction built
   ! from the left singular vectors with nonzero singular value.
   ! The SVD here minimises the Euclidean Frobenius norm, which is
   ! the V^2 phi^2 weighted L^2 of (L2D + L1D); this is a defensible
   ! choice because V phi is the natural "neutron volume" and the
   ! quantity we ultimately want to filter is the leakage CURRENT
   ! density, not the cross-section L itself.
   !----
   allocate(Yw(M, N), V(N, N), W(N), F(N))
   do k = 1, N
      do i = 1, M
         Yw(i, k) = Y(i, k)
      end do
   end do
   !
   !----
   ! Step 4: thin SVD via ALSVDF.  Y' = U * diag(W) * V^T
   ! On exit, ALSVDF returns U overwriting Yw, W sorted descending,
   ! V is N x N right singular vectors.
   !----
   call ALSVDF(Yw, M, N, M, N, W, V)
   !
   do ialpha = 1, N
      SIG_OUT(ialpha) = W(ialpha)
   end do
   !
   !----
   ! Step 5: Tikhonov filter factors + reported effective rank
   !----
   smax = W(1)
   if (smax <= 0.0d0) then
      ! Zero spectrum: nothing to filter, leave DB2 unchanged.
      RANK_USED = N
      if (IMPX >= 1) then
         write(IUNOUT,'(A,I4,A,I3,A,1P,E11.4,A)') &
           ' SPOPOD: group', IGR, &
           '  zero singular spectrum (N=', N, &
           ', smax=', smax, '), POD inactive'
      end if
      deallocate(F, Yw, V, W, Y)
      return
   end if
   !
   if (EPS_POD > 0.0) then
      tol = real(EPS_POD, dp) * smax
      do ialpha = 1, N
         F(ialpha) = W(ialpha)**2 / (W(ialpha)**2 + tol**2)
      end do
   else
      tol = 0.0d0
      F(1:N) = 1.0d0
   end if
   if (RANK_MAX > 0) then
      do ialpha = RANK_MAX + 1, N
         F(ialpha) = 0.0d0
      end do
   end if
   !
   ! Reported effective rank keeps the old semantics: number of modes
   ! above the f = 1/2 point (sigma > eps*sigma_1), capped by RANK_MAX.
   RANK_USED = 0
   do ialpha = 1, N
      if (W(ialpha) > tol) RANK_USED = ialpha
   end do
   if (RANK_MAX > 0) RANK_USED = min(RANK_USED, RANK_MAX)
   RANK_USED = max(RANK_USED, 1)
   !
   ! Exact fast path: no filtering requested (eps<=0) and no active
   ! rank cap. Steps 6-7 are then skipped so DB2 stays bit-identical
   ! to its input (see comment there).
   lexact = (EPS_POD <= 0.0) .and. (RANK_MAX <= 0 .or. RANK_MAX >= N)
   !
   ! Frobenius energy retained (diagnostic, filter-weighted)
   frob_full = 0.0d0
   frob_kept = 0.0d0
   do ialpha = 1, N
      frob_full = frob_full + W(ialpha)**2
      frob_kept = frob_kept + (F(ialpha) * W(ialpha))**2
   end do
   !
   if (IMPX >= 1) then
      ! RANK_USED >= 1 guaranteed here so W(RANK_USED) is safe.
      write(IUNOUT,'(A,I4,A,I3,A,I3,A,1P,E11.4,A,E11.4,A,0P,F7.4)') &
        ' SPOPOD: group', IGR, '  rank=', RANK_USED, '/', N, &
        '  s1=', smax, '  s_r/s_1=', &
        W(RANK_USED) / max(smax, 1.0d-30), &
        '  energy=', sqrt(frob_kept / max(frob_full, 1.0d-30))
      if (IMPX >= 2) then
         write(IUNOUT,'(A,12(1P,E11.3))') ' SPOPOD: spectrum', &
           (W(ialpha), ialpha = 1, N)
         write(IUNOUT,'(A,12(0P,F11.7))') ' SPOPOD: filters ', &
           (F(ialpha), ialpha = 1, N)
         write(IUNOUT,'(A,1P,E11.4)') &
           ' SPOPOD: pre-SVD constraint residual = ', ERR_PRE
      end if
   end if
   !
   !----
   ! Steps 6-7: filtered reconstruction tilde Y' = sum_a f_a sigma_a
   ! u_a v_a^T, then recovery tilde L^{2D} = tilde Y'/(V phi) - L1D
   ! with S1 stabilisation.
   ! Both steps are skipped entirely on the exact fast path: a
   ! reconstruct-and-divide round trip (even with all f_a = 1) would
   ! perturb DB2 at ulp level, and the stated purpose of the fast
   ! path is bit-identical reproduction of the control mode. The SVD
   ! above still runs for the spectrum diagnostics.
   !----
   if (.not. lexact) then
      allocate(Ytilde(M, N))
      do k = 1, N
         do i = 1, M
            Ytilde(i, k) = 0.0d0
            do ialpha = 1, N
               fw = F(ialpha) * W(ialpha)
               if (fw == 0.0d0) cycle
               Ytilde(i, k) = Ytilde(i, k) &
                            + Yw(i, ialpha) * fw * V(k, ialpha)
            end do
         end do
      end do
      ! Recovery. Use STRICT inequality phi > effective_floor to
      ! avoid 1/0 when both PHI and PHI_MIN are zero. The effective
      ! floor combines the user's PHI_MIN with a hard internal lower
      ! bound (tiny() of the kind) so that even PHI_MIN=0 gives at
      ! least machine-epsilon protection.
      block
        real :: effective_floor
        effective_floor = max(PHI_MIN, 100.0 * tiny(1.0))
        do k = 1, N
           do i = 1, M
              if (PHI(i, k) > effective_floor .and. VOL(i) > 0.0) then
                 DB2(k, i) = Ytilde(i, k) / (real(VOL(i), dp) * real(PHI(i, k), dp)) &
                           - real(XL1D(k), dp)
              end if
              ! else: keep DB2(k, i) unchanged (S1: low-flux opt-out)
           end do
        end do
      end block
      deallocate(Ytilde)
   end if
   !
   !----
   ! Step 8: post-verify constraint on V*(tilde L2D + L1D)*phi
   !----
   ERR_POST = 0.0d0
   ynorm_F  = 0.0d0
   do k = 1, N
      ysum_k = 0.0d0
      do i = 1, M
         dnoise = real(VOL(i), dp) * (DB2(k, i) + real(XL1D(k), dp)) &
                * real(PHI(i, k), dp)
         ynorm_F = ynorm_F + dnoise**2
         ysum_k  = ysum_k  + dnoise
      end do
      if (abs(ysum_k) > ERR_POST) ERR_POST = abs(ysum_k)
   end do
   ynorm_F = sqrt(ynorm_F)
   if (ynorm_F > 0.0d0) ERR_POST = ERR_POST / ynorm_F
   !
   if (IMPX >= 2) then
      write(IUNOUT,'(A,1P,E11.4)') &
        ' SPOPOD: post-SVD constraint residual = ', ERR_POST
   end if
   !
   deallocate(F, W, V, Yw, Y)
   return
end subroutine SPOPOD

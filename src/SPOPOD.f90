!
!-----------------------------------------------------------------------
!
!Purpose:
! POD-based constraint-preserving compression of the radial leakage
! matrix L^{2D} for the SPOT (Synthesis Proper Orthogonal Decomposition)
! method, VARIANT III: POD on the volume-weighted leakage current density
!     Y_{i,k} := V_i * L^{2D}_{i,k} * phi^k_i.
!
! The fundamental-mode constraint of SPOT is
!     sum_i V_i * L^{2D}_{i,k} * phi^k_i = 0   for each snapshot k,
! which writes 1^T Y[:,k] = 0 in matrix form. Theorem 1 (Cui 2026)
! shows that the standard thin-SVD rank-r truncation of Y preserves
! this column-zero-sum property exactly at any rank, and the recovered
! tilde L^{2D} = tilde Y / (V phi) therefore satisfies the
! fundamental-mode constraint exactly. Variant III is the
! constraint-preserving POD applied to SPOT.
!
! Algorithm:
!   1. Build Y_{i,k} = V_i * L^{2D}_{i,k} * phi^k_i.
!   2. Pre-verify  | 1^T Y[:,k] |_inf < tol * |Y|_F.
!   3. Standard thin SVD (unweighted): Y = U Sigma V^T.
!   4. Choose rank r from eps_pod (sigma_r/sigma_1 relative threshold)
!      and rank_max (explicit cap).
!   5. Truncate: tilde Y = sum_{a<=r} sigma_a u_a v_a^T.
!   6. Recover (S1: hard floor on phi):
!         tilde L^{2D}_{i,k} = tilde Y_{i,k} / (V_i phi^k_i)  if phi^k_i >= phi_min
!         tilde L^{2D}_{i,k} = L^{2D}_{i,k}                   otherwise.
!   7. Post-verify constraint at machine precision.
!
! Computational complexity: O(N^2 K) per group when N >= K, dominated by
! ALSVDF. Energy-group loop is the natural parallelisation axis.
!
!Copyright:
! Copyright (C) 2026 Ecole Polytechnique de Montreal.
!
!Author(s): B. Cui, Polytechnique Montreal (variant III, POD on weighted
!           leakage current density), based on the SPOT framework by
!           A. Hebert.
!
!Parameters: input
! NREG2D    number of radial regions per snapshot (= N).
! NSNAP     number of snapshots (= K).
! PHI       array of snapshot zero-th Legendre fluxes,
!           PHI(I,K) = phi^K_I for radial region I, snapshot K.
! VOL       array of region volumes, VOL(I) = V_I for I=1..NREG2D.
! EPS_POD   relative truncation tolerance (sigma_r/sigma_1 cutoff).
!           <= 0 disables POD (the matrix is left untouched, but the
!           singular spectrum is still computed when IMPX >= 2).
! RANK_MAX  explicit rank cap. 0 means automatic from EPS_POD only.
! PHI_MIN   hard floor on phi for safe recovery (S1 stabilisation).
!           0 means no floor (always do tilde L = tilde Y / (V phi)).
! IMPX      print verbosity.
! IGR       energy-group index for diagnostics.
!
!Parameters: input/output
! DB2       DOUBLE PRECISION matrix, DB2(K,I), the radial leakage
!           cross sections L^{2D}_{i,k} for one energy group. Rank
!           truncation rewrites this in place.
!
!Parameters: output
! RANK_USED  effective rank actually retained (1..min(NREG2D,NSNAP)).
! SIG_OUT    array of size min(NREG2D,NSNAP), the singular spectrum
!            of the V-weighted matrix Y^{(W)} (sorted descending).
! ERR_PRE    DOUBLE PRECISION, max | 1^T Y[:,k] | / |Y|_F before SVD.
!            Diagnoses whether the input radial fluxes already satisfy
!            the fundamental-mode constraint (machine-precision when
!            B1 critical search is converged).
! ERR_POST   DOUBLE PRECISION, max | 1^T tildeY[:,k] | / |tildeY|_F after SVD.
!            Should be at machine-precision (theorem 4.2 of spot_v3.pdf).
!
!-----------------------------------------------------------------------
!
subroutine SPOPOD(NREG2D, NSNAP, DB2, PHI, VOL, &
                  EPS_POD, RANK_MAX, PHI_MIN,    &
                  RANK_USED, SIG_OUT,            &
                  ERR_PRE, ERR_POST,             &
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
   integer, intent(out)           :: RANK_USED
   double precision, intent(out)  :: SIG_OUT(*)
   double precision, intent(out)  :: ERR_PRE, ERR_POST
   !----
   ! local variables
   !----
   integer  :: M, N, ialpha, k, i
   double precision :: tol, smax, frob_full, frob_kept
   double precision :: ynorm_F, ymax, vphi, ysum_k, dnoise
   double precision, allocatable :: Y(:,:), Yw(:,:), V(:,:), W(:)
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
   ! Step 1: build Y_{i,k} = V_i * L^{2D}_{i,k} * phi^k_i
   !----
   allocate(Y(M, N))
   ynorm_F = 0.0d0
   ymax    = 0.0d0
   do i = 1, M
      do k = 1, N
         vphi = real(VOL(i), dp) * real(PHI(i, k), dp)
         Y(i, k) = vphi * DB2(k, i)
         ynorm_F = ynorm_F + Y(i, k)**2
         if (abs(Y(i,k)) > ymax) ymax = abs(Y(i,k))
      end do
   end do
   ynorm_F = sqrt(ynorm_F)
   !
   !----
   ! Step 2: pre-verify column-zero-sum (fundamental-mode constraint)
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
   ! Step 3: Plan A -- direct unweighted SVD on Y.
   !
   ! Earlier draft pre-multiplied Y by sqrt(V) ("V-weighted SVD") in
   ! the hope of recovering a V-inner-product-optimal basis. But Y
   ! itself already contains the V_i factor (Y = V*L*phi), so the
   ! resulting Yw effectively carried V_i^{3/2} and minimised the
   ! ill-motivated functional sum_i V_i^3 (L*phi)^2. Plan A drops
   ! that extra layer.
   !
   ! Constraint preservation (Theorem 4.2 of spot_v3.pdf) does NOT
   ! require V-weighting: starting from 1^T Y[:,k]=0, Lemma 4.1
   ! (column-zero-sum subspace invariance) directly gives
   ! 1^T tildeY[:,k]=0 for any rank truncation of the unweighted SVD
   ! Y = U Sigma V^T. The SVD here minimises the Euclidean Frobenius
   ! norm ||Y - tildeY||_F^2 = sum_{i,k} (V_i L_{i,k} phi_i^k)^2,
   ! which is V^2 phi^2 weighted L^2 of L; this is a defensible
   ! choice because V phi is the natural "neutron volume" and the
   ! quantity we ultimately want to filter is the leakage CURRENT
   ! density, not the cross-section L itself.
   !----
   allocate(Yw(M, N), V(N, N), W(N))
   do k = 1, N
      do i = 1, M
         Yw(i, k) = Y(i, k)
      end do
   end do
   !
   !----
   ! Step 4: thin SVD via ALSVDF.  Y = U * diag(W) * V^T
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
   ! Step 5: rank selection
   !----
   smax = W(1)
   if (smax <= 0.0d0) then
      ! Zero spectrum: nothing to truncate, leave DB2 unchanged.
      ! Diagnostic printout below uses ratios so guard against W(0).
      RANK_USED = N
      if (IMPX >= 1) then
         write(IUNOUT,'(A,I4,A,I3,A,1P,E11.4,A)') &
           ' SPOPOD: group', IGR, &
           '  zero singular spectrum (N=', N, &
           ', smax=', smax, '), POD inactive'
      end if
      deallocate(Yw, V, W, Y)
      return
   else
      tol = max(real(EPS_POD, dp), 0.0d0) * smax
      RANK_USED = 0
      do ialpha = 1, N
         if (W(ialpha) > tol) RANK_USED = ialpha
      end do
      if (RANK_MAX > 0) RANK_USED = min(RANK_USED, RANK_MAX)
      RANK_USED = max(RANK_USED, 1)
   end if
   !
   ! Frobenius energy retained (diagnostic)
   frob_full = 0.0d0
   frob_kept = 0.0d0
   do ialpha = 1, N
      frob_full = frob_full + W(ialpha)**2
      if (ialpha <= RANK_USED) frob_kept = frob_kept + W(ialpha)**2
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
         write(IUNOUT,'(A,1P,E11.4)') &
           ' SPOPOD: pre-SVD constraint residual = ', ERR_PRE
      end if
   end if
   !
   !----
   ! Step 6: truncate to rank r.
   ! Plan A unweighted SVD gives directly tilde Y = U[:,:r] diag(W[1:r]) V[:,:r]^T.
   !----
   allocate(Ytilde(M, N))
   if (RANK_USED < N) then
      do k = 1, N
         do i = 1, M
            Ytilde(i, k) = 0.0d0
            do ialpha = 1, RANK_USED
               Ytilde(i, k) = Ytilde(i, k) &
                            + Yw(i, ialpha) * W(ialpha) * V(k, ialpha)
            end do
         end do
      end do
   else
      ! Full rank: tilde Y = Y exactly (up to roundoff)
      do k = 1, N
         do i = 1, M
            Ytilde(i, k) = Y(i, k)
         end do
      end do
   end if
   !
   !----
   ! Step 7: recover tilde L^{2D} with S1 stabilisation.
   ! Use STRICT inequality phi > effective_floor to avoid 1/0 when both
   ! PHI and PHI_MIN are zero. The effective floor combines the user's
   ! PHI_MIN with a hard internal lower bound (tiny() of the kind) so
   ! that even PHI_MIN=0 gives at least machine-epsilon protection.
   !----
   block
     real :: effective_floor
     effective_floor = max(PHI_MIN, 100.0 * tiny(1.0))
     do k = 1, N
        do i = 1, M
           if (PHI(i, k) > effective_floor .and. VOL(i) > 0.0) then
              DB2(k, i) = Ytilde(i, k) / (real(VOL(i), dp) * real(PHI(i, k), dp))
           end if
           ! else: keep DB2(k, i) unchanged (S1: low-flux opt-out)
        end do
     end do
   end block
   !
   !----
   ! Step 8: post-verify constraint on tilde L^{2D}
   !----
   ERR_POST = 0.0d0
   ynorm_F  = 0.0d0
   do k = 1, N
      ysum_k = 0.0d0
      do i = 1, M
         dnoise = real(VOL(i), dp) * DB2(k, i) * real(PHI(i, k), dp)
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
   deallocate(Ytilde, W, V, Yw, Y)
   return
end subroutine SPOPOD

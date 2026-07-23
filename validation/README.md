# SPOT validation

The active target is the self-consistent fixed-space Galerkin–SPOD method in
`SPOT_doc/rederivation.md`.

The published validation tree is intentionally small:

| Directory | Purpose |
|---|---|
| `level1/` | weighted POD algebra |
| `level2/` | radial fixed-operator and source closure |
| `iterative/` | fixed-basis state, source, replay, and one-map contracts |

The new validation order is:

1. freeze the fixed-space equations and source identity;
2. test radial source/closure algebra and leakage signs;
3. define and independently replay the complete state
   \(x=(a,1/k,L)\);
4. validate one corrected map evaluation;
5. compare production and tighter inner controls from the same input;
6. qualify direct Picard convergence;
7. repeat discretization studies;
8. compare only the accepted iterative solution with an independent 3D
   reference.

No long continuation is authorized merely because an earlier trajectory
ended at a prescribed iteration count.

## Current stop point

The online branch preserves

\[
q_{\rm FS}=F(Ba)/k+S_{\rm off}(u_\perp)
\]

and constructs `RADIAL-OP` from that same source. The offline POD package is
then reused bit for bit while the live response changes. The canonical state
uses the production binary32 restriction, and explicit `SPOPROJ FIXB`
reconstructs the feedback as \(Ba\).

The independent no-transport fixture passes. The next unresolved gate is one
complete corrected transport map \(x_1=G(x_0)\); no new iterative convergence
claim exists yet.

## Commands that remain valid

Run the inherited and new short algebra/contracts with

```sh
sh validation/run_fast.sh
```

Run the no-transport LCM fixture with a Dragon executable built from the
current sources:

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
  sh validation/iterative/run_stage0_runtime.sh
```

The runtime fixture also requires the six local seed files listed in
`validation/iterative/seed.sha256`. They are deliberately excluded from Git
because they total about 258 MB; set `SEED_DIR` if they are stored elsewhere.

The full active protocol is
`SPOT_doc/validation_plan.md`. These commands qualify implementation plumbing
only. They do not qualify one transport map or iterative convergence.

# D4-A 650 C TONE gate

## Result

`PASS_TONE650_NO_SNAPSHOT`.

One corrected D4-A material state was run at fuel/cladding/sodium
temperatures `(650,620,475) C`.  The gate contains only
`LIB -> SALT(TISO=50,MERGMIX) -> TONE`; it does not contain the production
`MCCGT`, `ASM` or `FLU` chain and creates no snapshot or XSM archive.

The single run used the unchanged TONE terminal
`MXIT=20, EPS=1.0e-5, TRAN PIJ` and gave

```text
CONVERGENCE REACHED AT TONE ITERATION = 4  ERROR = 4.453E-06
MODULE TONE: TIME SPENT = 326.000 s
normal end of execution for dragon 5
```

The iteration-cap warning is absent.  The independently checked log contains
one TONE module and zero MCCGT, ASM, FLU or snapshot markers.  The bounded
runner had a fixed 1500 s wall limit, one attempt and no retry; the limit is a
process-safety terminal and does not enter the physical equations.

## Reproducibility

The retained local artifact is
`validation/artifacts/d4a-tone650-gate-20260824/`.
Both its result manifest and executed-input manifest pass `sha256sum -c`.
The main hashes are:

- result log: `1c5436b7d518bcc3420eb9ef8f82a2ede0477a37ee3630294bec7d78d58cfdbe`;
- gate procedure: `87bd90b0bf81c8048435e7e8ff7fe4e552384f0cfd372195cfbb3a00be2ebd48`;
- gate deck: `806ff83c7b9e6442009b3be04d474d68a1d83ccefb33d121fdc06ec90b0b8d44`;
- Dragon executable: `c47d2a8d7b61f7e5e19680be49cdd3d2a0b1267e08a76fc1c3d25e43f31fcc28`;
- SHEM-370 DLIB: `66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9`.

Before execution, the gate's executable material construction and TONE block
were independently compared with `SpotD4Snap` and matched exactly.  The
repository input manifest now freezes the gate files as well.

## Meaning

This closes only the corrected 650 C self-shielding prerequisite.  It permits
the separately bounded three-state snapshot campaign to be attempted.  It is
not a radial-flux result, a POD basis, a 2D/1D iteration, a convergence result
or an independent accuracy validation.

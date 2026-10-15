# Bounded storage for the complete selected native-track pilot

The [native-track pilot contract](native_oblique_track_pilot_contract.md)
remains the scientific scope. Its first preflight selects eleven paths and
16,896 configurations, within the memory/time estimates, but the diagnostic
expansion has a 26.42-GiB primary uncompressed bound. Only about 5.8 GiB is
available on the shared volume. Preserve that attempt as storage-blocked;
do not run its full diagnostic expansion or remove unrelated project files.

The compact continuation preserves exactly the selected paths, all four
polar nodes, both axial signs, both planar orientations, physical reflections,
groups 51/61/98, heights 1/20 cm, axial grids 1/2/4/8, orders 8/16, complete
cell/boundary source coordinates, matched native input controls and all gates.
Its 16-column batching changes no mathematics or source coordinates.

## Lossless assembled fields and reconstructible primitive diagnostics

Store every cell-integrated response and one copy of the current on each
physical radial/axial face, for every source column. Neighboring contributions
must be bitwise equal before sharing storage; otherwise preserve the failure
without packing it. Inactive side entries are exactly zero. This is a
lossless representation of the full assembled response, not a projection.

Store each ray's entry data, its ordered piece endpoints, physical cell ids
and exit sides in a compressed geometry layout. Use exact float64 endpoints
and checked unsigned integer indices. Reconstruct piece starts, lengths,
travel order and incidence only by exact original identities. Packing and
unpacking must recover the full geometric and response arrays bit for bit.

Every primitive and source column is still evaluated. Preserve per-input
minimum amplitudes/integrals, maximum normalized primitive defects and the
complete worst primitive witness (input column, piece identity, incoming,
outgoing, integral, signed defect and scale). Preserve matched endpoint
defects/scales and all aggregate raw fields needed to recompute cell/global
and shared-face ledgers. Full per-piece/per-input trace tensors are regenerated
from immutable geometry, source coordinates and the archived algorithm;
they are not materialized in this compact archive. Describe this diagnostic
storage choice separately from the lossless assembled response encoding.

Retain original 1D reference fields, exact native baseline data, source-cell
mapping and native angular weights. Regional fields and weighted moment
contributions must reconstruct exactly from the complete segment responses.
No selected-ray normalizer may be fitted to whole-native measures.

## Storage and independent replay

Freeze a conservative byte bound before response computation. Include full
primary output, one fresh replay process at a time, input/source copies,
metadata overhead and at least 1 GiB remaining for other work. Keep the
512-MiB/600-second limits and one numerical thread for each process.
Stop before a new process if the free-space reserve cannot be maintained.

Run the replay from real copied inputs and sources in a fresh directory.
For each completed replay process, compare every output byte with the primary
file, then write a receipt containing all hashes and sizes. Only after all
comparisons pass may that replay process's duplicate NPZ files be discarded.
Retain its result JSON, logs, resources and receipt; retain every primary
field. Any mismatch keeps its replay files for diagnosis and stops the run.
The replay must cover the full case matrix, not selected witnesses.

Archive the original preflight, compact plan, packing tests, complete primary
fields, full replay receipts and an independent raw-ledger audit. Seal the
completed artifact. Storage success admits no scientific result by itself.
Qualification remains limited to the selected paths; whole-native geometry,
common radial white return, native mesh convergence and the coupled
eigenreference remain separate future gates.

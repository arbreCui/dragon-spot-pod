"""Actual original supervisor, new disposable TMP child, no numerical program."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
STARTED = time.monotonic()
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
FACTORY = ROOT / 'validation/axial_material/prepare_combined_physical_dedup_file_snapshot_runtime_build.py'
FACTORY_SHA = 'bf4692a57209ace55e22f85c6e9ffabf80850dcb1b610348e7dc97b74a80040c'
BASE = Path('/private/tmp/combined-runtime-declared-union-readonly-measurement-20261007')
CHILD = Path('/private/tmp/combined_runtime_declared_union_readonly_measurement_20261007.py')
CHILD_SHA = '0f9e9778782abd8c6d61f8d0a038d573ae3bcea77c1ad806e3bb4b4a17ec9244'
assert hashlib.sha256(FACTORY.read_bytes()).hexdigest() == FACTORY_SHA
assert hashlib.sha256(CHILD.read_bytes()).hexdigest() == CHILD_SHA
assert not os.path.lexists(BASE)
spec = importlib.util.spec_from_file_location('actual_combined_runtime_declared_union_supervisor_provider', FACTORY)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
# Genuine module/source/MRO/immutable guard and live resource APIs, not any
# component production admission. Existing FAILED SOURCE/OUT is never written.
b, h, full, c = m.modules()
assert full.OwnRSSSerialExecutor.__bases__ == (c.SerialExecutor,)
resources = m.resources_for([str(p) for p in b.history_roots([], ART)], c.ResourceFailure)
before = resources.check()
BASE.mkdir()
(BASE / 'runtime').mkdir()
(BASE / 'measurement').mkdir()
(BASE / 'READONLY_DECLARED_UNION').mkdir()
shutil.copy2(m.require(m.BOUNDED, m.BOUNDED_SHA), BASE / 'runtime/run_bounded_dragon.py')
assert m.digest(BASE / 'runtime/run_bounded_dragon.py') == m.BOUNDED_SHA
runner = full.OwnRSSSerialExecutor(BASE, 1800-(time.monotonic()-STARTED), 'READONLY_DECLARED_UNION', resources)
assert runner.bounded.__file__ == str(BASE / 'runtime/run_bounded_dragon.py')
command = [sys.executable, str(CHILD)]
runner.execute(BASE / 'measurement', 'complete_declared_union', command, 600,
               'AXMAT-COMBINED-DECLARED-UNION-READ-ONLY-MEASURED')
after = resources.check()
elapsed = time.monotonic()-STARTED
assert elapsed < 1800
print(json.dumps(dict(schema='AXMAT_COMBINED_DECLARED_UNION_ACTUAL_SUPERVISION_MEASUREMENT_V1',
    supervisor_source=m.pin(Path(full.__file__).resolve()), parent_class_source=m.pin(Path(c.__file__).resolve()),
    bounded_helper=m.pin(BASE / 'runtime/run_bounded_dragon.py'),
    actual_command=command, stage_records=runner.records,
    resources_before=before, resources_after=after, whole_elapsed_seconds=elapsed,
    original_total_wall_seconds=1800, original_stage_wall_seconds=600, original_RSS_cap_mib=512,
    thread_count=1, children_at_once=1, retries=0,
    numeric_program_or_component_API_executed=False, scientific_qualification_created=False,
    measurement_output_root=str(BASE)), allow_nan=False), flush=True)

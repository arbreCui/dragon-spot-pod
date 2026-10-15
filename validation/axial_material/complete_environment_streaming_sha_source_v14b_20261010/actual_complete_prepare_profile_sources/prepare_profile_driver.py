"""Passive timing around one unchanged canonical V14b prepare-build CLI.

This executes preparation, not compilation, transport or scientific admission.
All canonical and predecessor gates execute normally; no callable is replaced.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import stat
import sys
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
TARGET = ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
TARGET_SHA = '4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
OLD_RECEIPT = ROOT / 'validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/actual_component_execution_receipts/Root_actual_prepare_tool_return.json'
OLD_RECEIPT_SHA = 'd69437dc3f3df2fc8b36adb7c3077410e6d3052e153d4568ea7e0b52ac856f82'
PROFILE_OUT = ART / 'axial-material-complete-prepare-profile-v14b-20261010'
PROFILE_PREFIX = str(ROOT / 'validation/axial_material') + '/'
FORBIDDEN_FACTORY = str(ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
NAMES = frozenset(('prepare_build', 'predecessor_admission', 'failed_capture_admission',
    'memory_predecessor_admission', 'failed_memory_capture_admission', 'source_inputs',
    'patch_admission', 'sender_source_admission', 'sender_control_contract',
    'stream_environment_helper_source_admission', 'complete_archive_forecast',
    'production_cache_shape_forecast', 'modules', 'guard_admission', 'environment',
    'production_admission', 'declaration_admission', 'capture_admission', 'control_audit',
    'memory_controls_audit', 'inventory', 'check', 'archive_bytes', 'resource_admission',
    'verify_inventory', 'validate_history_roots', 'history_roots', 'digest', 'verify'))

def pin(path, wanted=None):
    path = Path(path)
    a = path.lstat()
    identity = [a.st_dev, a.st_ino, a.st_mode, a.st_nlink, a.st_size, a.st_mtime_ns, a.st_ctime_ns]
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('regular pinned source required')
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    after = [b.st_dev, b.st_ino, b.st_mode, b.st_nlink, b.st_size, b.st_mtime_ns, b.st_ctime_ns]
    if identity != after or (wanted is not None and value != wanted):
        raise ValueError('pinned source changed: ' + str(path))
    return dict(path=str(path), sha256=value, identity=identity)

class PassiveProfile:
    """Selected Python spans; time includes profiling and ordinary I/O overhead."""
    def __init__(self):
        self.cache = {}
        self.stack = []
        self.active = {}
        self.stats = {}
        self.spans = []
        self.forbidden = []

    def observe(self, frame, event, arg):
        if event not in ('call', 'return'):
            return
        code = frame.f_code
        selected = self.cache.get(code)
        if selected is None:
            filename = code.co_filename
            in_scope = filename.startswith(PROFILE_PREFIX)
            selected = in_scope and code.co_name in NAMES
            self.cache[code] = selected
        # A failed old factory may be read as immutable bytes, never executed.
        if event == 'call' and code.co_filename == FORBIDDEN_FACTORY:
            self.forbidden.append([code.co_filename, code.co_name, code.co_firstlineno])
            raise ValueError('old failed V13 factory execution forbidden')
        if not selected:
            return
        now = time.perf_counter()
        key = (code.co_filename, code.co_firstlineno, code.co_name)
        if event == 'call':
            row = self.stats.setdefault(key, dict(calls=0, returns=0, inclusive_seconds=0., exclusive_selected_seconds=0.))
            row['calls'] += 1
            item = [id(frame), key, now, 0.]
            self.active[id(frame)] = item
            self.stack.append(item)
        else:
            item = self.active.pop(id(frame), None)
            if item is None or not self.stack or self.stack[-1] is not item:
                raise ValueError('passive selected profile stack mismatch')
            self.stack.pop()
            elapsed = now - item[2]
            row = self.stats[key]
            row['returns'] += 1
            row['inclusive_seconds'] += elapsed
            row['exclusive_selected_seconds'] += elapsed - item[3]
            if self.stack:
                self.stack[-1][3] += elapsed
            if code.co_name != 'digest':
                self.spans.append(dict(file=key[0], line=key[1], name=key[2],
                    started_perf_counter=item[2], inclusive_seconds=elapsed,
                    exclusive_selected_seconds=elapsed-item[3]))

    def result(self):
        return dict(rows=[dict(file=k[0], line=k[1], name=k[2], **v) for k,v in sorted(self.stats.items())],
            spans=self.spans, open_selected_frames=len(self.stack), forbidden_calls=self.forbidden,
            profiler_cleared=sys.getprofile() is None, timing_includes_profile_overhead=True,
            exclusive_is_relative_to_selected_python_spans_only=True,
            sha_or_guard_calls_skipped=False, callable_or_class_replaced=False)

def main():
    if len(sys.argv) != 1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
        raise ValueError('fixed nonoptimized preparation wrapper required')
    before = [pin(TARGET, TARGET_SHA), pin(OLD_RECEIPT, OLD_RECEIPT_SHA)]
    receipt = json.loads(OLD_RECEIPT.read_text())
    if receipt['terminal']['exit_code'] != 0 or receipt['session_closed'] is not True:
        raise ValueError('closed original preparation receipt required')
    argv = list(receipt['input']['argv'])
    if len(argv) != 23 or argv[2] != 'prepare-build':
        raise ValueError('original ten preparation arguments required')
    argv[1] = str(TARGET)
    if not PROFILE_OUT.is_dir() or os.path.lexists(PROFILE_OUT / 'child_profile.json'):
        raise ValueError('Root-created fresh profiling namespace required; no retry')
    original_argv = sys.argv
    profile = PassiveProfile()
    started = time.monotonic()
    failure = None
    try:
        sys.argv = argv[1:]
        sys.setprofile(profile.observe)
        runpy.run_path(str(TARGET), run_name='__main__')
    except BaseException as error:
        failure = repr(error)
        raise
    finally:
        sys.setprofile(None)
        sys.argv = original_argv
        after = [pin(TARGET, TARGET_SHA), pin(OLD_RECEIPT, OLD_RECEIPT_SHA)]
        if before != after:
            raise ValueError('preparation source changed during actual call')
        value = dict(schema='AXMAT_V14B_ACTUAL_COMPLETE_PREPARE_PASSIVE_PROFILE_V1',
            status='COMPLETE_PREPARE_RETURNED' if failure is None else 'PREPARE_FAILED_NO_RETRY',
            actual_canonical_argv=argv, complete_source_pins_before=before,
            complete_source_pins_after=after, failure=failure,
            actual_child_elapsed_seconds=time.monotonic()-started, profile=profile.result(),
            compilation_or_transport_launched=False, full86_executed=False,
            native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False)
        with (PROFILE_OUT / 'child_profile.json').open('x') as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.write('\n')

if __name__ == '__main__':
    main()

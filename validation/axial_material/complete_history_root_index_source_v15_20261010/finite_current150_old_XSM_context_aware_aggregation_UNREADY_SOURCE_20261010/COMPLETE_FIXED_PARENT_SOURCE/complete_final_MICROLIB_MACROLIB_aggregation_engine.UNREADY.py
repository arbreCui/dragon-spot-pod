"""UNREADY Source: complete saved final-micro construction comparison.

This program is NOT imported or executed by its author. Root must bind this
Source, the unchanged saved-native adapter, actual persisted-native evidence,
independent Source review and genuine host before execution. No native, project,
transport, helper or guard API is imported by this child. Unknown history never
becomes an old input or a success qualification. Full original coverage remains
on disk even when a field producer or arithmetic model fails.
"""
import argparse
from array import array
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sqlite3
import stat
import struct
import sys
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
SOURCE_BINDING_SHA256 = None
BOUND_ADAPTER_PIN = None
ORIGINAL_CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
    joint_archive_bytes=2*2**30, history_bytes=96*2**30,
    free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
GROUPS, MIXES, ISOTOPES, MOMENTS, EXTRAS = 370, 8, 62, 3, 18
SLOTS, SPECTRA, COMPONENTS, DELAYED = 8, 4, 32, 6
SUFFIXES = ('    ', ' LIN', ' QUA')
FALSE = dict(original_XSM_memory_bits_verified=False,
    original_native_build_binary_Source_linkage_qualified=False,
    historical_LIBDEN_machine_arithmetic_replayed=False,
    reaction_multiplicity_verified=False, physical_neutron_balance_qualified=False,
    scientific_accuracy_qualified=False, AAA_accuracy_qualified=False,
    ABA_admitted=False, coupled_370group_reference_qualified=False,
    native_transport_executed=False, whole_combined_build_or_INPUT_qualified=False,
    genuine_supervisor_watch_verified_here=False)
PIN_KEYS = {'path', 'sha256', 'size_bytes', 'identity'}


def require(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def typed_pin(value):
    require(type(value) is dict and set(value) == PIN_KEYS, 'four-field full pin')
    require(type(value['path']) is str and Path(value['path']).is_absolute(), 'absolute pin')
    require(type(value['sha256']) is str and len(value['sha256']) == 64 and
            all(c in '0123456789abcdef' for c in value['sha256']), 'full lowercase SHA256')
    require(type(value['size_bytes']) is int and value['size_bytes'] >= 0 and
            type(value['identity']) is list and len(value['identity']) == 7 and
            all(type(x) is int and x >= 0 for x in value['identity']) and
            value['identity'][3] == 1 and value['identity'][4] == value['size_bytes'],
            'exact typed size and seven identities')


def full_pin(path, budget):
    path = Path(path)
    require(path.is_absolute(), 'absolute real file required')
    for p in (path, *path.parents):
        require(not stat.S_ISLNK(p.lstat().st_mode), 'input/output symlink alias forbidden')
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'single-link regular file')
    digest = hashlib.sha256()
    total = 0
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == identity(before), 'opened inode differs')
        while True:
            budget()
            raw = stream.read(2**20)
            if not raw:
                break
            digest.update(raw)
            total += len(raw)
        require(identity(os.fstat(stream.fileno())) == identity(before), 'file changed at EOF')
    require(identity(path.lstat()) == identity(before) and total == before.st_size,
            'full EOF input changed')
    return dict(path=str(path), sha256=digest.hexdigest(), size_bytes=total,
                identity=identity(before))


def check_pin(expected, budget):
    typed_pin(expected)
    actual = full_pin(expected['path'], budget)
    require(actual == expected, 'full input pin changed: '+expected['path'])
    return actual


def write_new(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=True, allow_nan=False, indent=2)
        stream.write('\n')


def make_array(raw, signed=False):
    result = array('i' if signed else 'I')
    require(result.itemsize == 4, 'four-byte native integer array required')
    result.frombytes(raw)
    if sys.byteorder != 'little':
        result.byteswap()
    return result


def bytes_array(values, signed=False):
    result = array('i' if signed else 'I', values)
    if sys.byteorder != 'little':
        result.byteswap()
    return result.tobytes()


class Binary32Model:
    """Exact integer RN-even operations; model remains separate from compilation.

    Binary32 finite inputs are decoded to signed integer ratios. No binary64 sum
    or one final cast stands in for isotope-ordered operations. Each call rounds
    independently; NaN/Inf and division by zero remain honest model failures.
    sqrt32 compares the exact square of the midpoint. FMA is never assumed.
    """
    def __init__(self):
        self.operations = dict(add=0, multiply=0, divide=0, sqrt=0)
        self.underflow_to_zero = 0
        self.overflow_to_infinity = 0

    @staticmethod
    def ratio(bits):
        require(type(bits) is int and 0 <= bits < 2**32, 'exact original binary32 bits')
        exponent = (bits >> 23) & 255
        require(exponent != 255, 'nonfinite REAL32 is not replaced or normalized')
        fraction = bits & 0x7fffff
        significand = fraction if exponent == 0 else fraction | 0x800000
        power = -149 if exponent == 0 else exponent-150
        numerator, denominator = (significand << power, 1) if power >= 0 else (significand, 1 << -power)
        return (-numerator if bits >> 31 else numerator), denominator

    @staticmethod
    def floor_log2(numerator, denominator):
        exponent = numerator.bit_length()-denominator.bit_length()
        if (numerator < denominator << exponent) if exponent >= 0 else (numerator << -exponent < denominator):
            exponent -= 1
        return exponent

    def pack_ratio(self, numerator, denominator, zero_sign=0):
        require(type(numerator) is int and type(denominator) is int and denominator > 0,
                'exact finite integer ratio')
        if numerator == 0:
            return zero_sign << 31
        sign = int(numerator < 0)
        numerator = abs(numerator)
        exponent = self.floor_log2(numerator, denominator)
        quantum = max(exponent-23, -149)
        n, d = (numerator, denominator << quantum) if quantum >= 0 else (numerator << -quantum, denominator)
        integer, remainder = divmod(n, d)
        if 2*remainder > d or (2*remainder == d and integer & 1):
            integer += 1
        if integer == 0:
            self.underflow_to_zero += 1
            return sign << 31
        if exponent < -126:
            return (sign << 31) | integer
        if integer == 1 << 24:
            exponent += 1
            integer >>= 1
        if exponent > 127:
            self.overflow_to_infinity += 1
            raise ValueError('REAL32 model overflow: no infinity is silently accepted')
        return (sign << 31) | ((exponent+127) << 23) | (integer & 0x7fffff)

    def add(self, a, b):
        self.operations['add'] += 1
        an, ad = self.ratio(a); bn, bd = self.ratio(b)
        return self.pack_ratio(an*bd+bn*ad, ad*bd, int(a == b == 0x80000000))

    def multiply(self, a, b):
        self.operations['multiply'] += 1
        an, ad = self.ratio(a); bn, bd = self.ratio(b)
        return self.pack_ratio(an*bn, ad*bd, (a ^ b) >> 31)

    def divide(self, a, b):
        self.operations['divide'] += 1
        an, ad = self.ratio(a); bn, bd = self.ratio(b)
        require(bn != 0, 'REAL32 division by zero is retained as model failure')
        n, d = an*bd, ad*bn
        if d < 0:
            n, d = -n, -d
        return self.pack_ratio(n, d, (a ^ b) >> 31)

    def sqrt(self, a):
        self.operations['sqrt'] += 1
        numerator, denominator = self.ratio(a)
        require(numerator >= 0, 'negative REAL32 square root')
        if numerator == 0:
            return a
        exponent = self.floor_log2(numerator, denominator)//2
        quantum = max(exponent-23, -149)
        n, d = (numerator, denominator << (2*quantum)) if quantum >= 0 else (numerator << (-2*quantum), denominator)
        integer = math.isqrt(n//d)
        midpoint = d*(2*integer+1)**2
        if 4*n > midpoint or (4*n == midpoint and integer & 1):
            integer += 1
        return self.pack_ratio(integer << quantum, 1) if quantum >= 0 else self.pack_ratio(integer, 1 << -quantum)

    def f64_to32(self, value):
        require(type(value) is float and math.isfinite(value), 'finite binary64 diagnostic only')
        n, d = value.as_integer_ratio()
        return self.pack_ratio(n, d, int(math.copysign(1.0, value) < 0))

    @staticmethod
    def nonzero(bits):
        Binary32Model.ratio(bits)
        return bool(bits & 0x7fffffff)


class DiskEvidence:
    """All source records and comparisons on disk; no whole Python path map."""
    def __init__(self, root, saved, budget, state):
        self.root, self.saved, self.budget, self.state = root, saved, budget, state
        self.coverage = (root/'complete_original_coverage.jsonl').open('x', encoding='ascii')
        self.fields = (root/'complete_field_comparisons.jsonl').open('x', encoding='ascii')
        self.mismatches = (root/'all_numeric_mismatches.jsonl').open('x', encoding='ascii')
        self.events = (root/'all_presence_branch_and_missing.jsonl').open('x', encoding='ascii')
        self.expected = (root/'complete_model_expected_bytes.bin').open('xb')
        self.db = sqlite3.connect(str(root/'coverage_decisions.sqlite'))
        self.db.execute('PRAGMA cache_size=-8192')
        self.db.execute('PRAGMA mmap_size=0')
        self.db.execute('PRAGMA temp_store=FILE')
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('CREATE TABLE decisions(key TEXT PRIMARY KEY, producer TEXT NOT NULL, outcome TEXT NOT NULL)')
        self.records = self.macro_records = self.comparisons = self.compared_elements = 0
        self.mismatch_elements = self.issues = 0
        self.phase_results = []
        self.producer_counts = {}

    def line(self, stream, value):
        self.budget()
        stream.write(json.dumps(value, separators=(',', ':'), allow_nan=False)+'\n')

    def event(self, category, **facts):
        self.line(self.events, dict(category=category, **facts))
        if category in ('REQUIRED_OPERAND_MISSING', 'PHASE_FAILED', 'UNSUPPORTED_SOURCE_BRANCH', 'SOURCE_CONTEXT_NOT_SAVED'):
            self.issues += 1

    def decision(self, path, producer, outcome):
        key = json.dumps(list(path), ensure_ascii=True, separators=(',', ':'))
        self.db.execute('INSERT OR REPLACE INTO decisions VALUES(?,?,?)', (key, producer, outcome))

    def inventory(self):
        """Full original micro+macro EOF payload hashes and all order evidence."""
        for original in self.saved.iter_all():
            row = original['record']
            for raw in self.saved.iter_raw(row):
                del raw
            self.records += 1
            self.macro_records += int(row['path'][:1] == ['MACROLIB'])
            self.line(self.coverage, original)
        require(self.macro_records == 19619, 'all original 19619 macro records retained')
        self.event('COMPLETE_ORIGINAL_COVERAGE', all_records=self.records,
                   macro_records=self.macro_records, raw_type_order_span_hash_preserved=True)

    def compare(self, path, kind, expected, producer, eligibility):
        """Every expected element saved; every differing element remains on disk."""
        row = self.saved.row(path)
        require(type(eligibility) is dict, 'explicit final/history eligibility')
        self.comparisons += 1
        offset = self.expected.tell()
        raw = expected if type(expected) is bytes else bytes_array(expected, kind == 1)
        self.expected.write(raw)
        expected_count = len(raw)//4
        expect_sha = hashlib.sha256(raw).hexdigest()
        base = dict(path=list(path), producer=producer, expected_type=kind,
            expected_count=expected_count, expected_pool_begin=offset,
            expected_pool_end=offset+len(raw), expected_sha256=expect_sha,
            actual_original_record=row, eligibility=eligibility)
        if row is None or row['kind'] != kind or row['declared_count'] != expected_count:
            self.event('REQUIRED_OPERAND_MISSING', path=list(path), producer=producer,
                reason='actual output absent/type/count differs', original_record=row)
            self.line(self.fields, dict(**base, outcome='OUTPUT_PRESENCE_TYPE_COUNT_FAIL'))
            self.decision(path, producer, 'OUTPUT_PRESENCE_TYPE_COUNT_FAIL')
            return False
        original = b''.join(self.saved.iter_raw(row))
        require(len(original) <= 2**20 and len(raw) <= 2**20, 'one bounded output record required')
        mismatches = 0
        for index in range(expected_count):
            self.compared_elements += 1
            wanted, actual = raw[4*index:4*index+4], original[4*index:4*index+4]
            if wanted == actual:
                continue
            mismatches += 1
            self.mismatch_elements += 1
            detail = dict(path=list(path), producer=producer, element_zero_based=index,
                expected_bits_hex=wanted.hex(), actual_bits_hex=actual.hex(), eligibility=eligibility)
            if kind == 2:
                ev, av = struct.unpack('<f', wanted)[0], struct.unpack('<f', actual)[0]
                eb, ab = struct.unpack('<I', wanted)[0], struct.unpack('<I', actual)[0]
                def ordered(bits):
                    return (~bits & 0xffffffff) if bits >> 31 else bits | 0x80000000
                detail.update(expected_finite=math.isfinite(ev), actual_finite=math.isfinite(av),
                    expected_binary64=ev if math.isfinite(ev) else None,
                    actual_binary64=av if math.isfinite(av) else None,
                    ULP_distance=abs(ordered(eb)-ordered(ab)),
                    absolute_delta=abs(av-ev) if math.isfinite(ev) and math.isfinite(av) else None,
                    opposite_sign=bool((ab ^ eb) >> 31))
            self.line(self.mismatches, detail)
        outcome = 'MODEL_BITS_MATCH' if mismatches == 0 else 'MODEL_BITS_MISMATCH'
        self.line(self.fields, dict(**base, outcome=outcome, differing_elements=mismatches,
            full_native_output_order_retained=True, historical_machine_bit_qualification=False))
        self.decision(path, producer, outcome)
        return mismatches == 0

    def complete_decisions(self):
        """Every original record has a classification; unknown producers fail full scope."""
        stream = (self.root/'complete_producer_coverage.jsonl').open('x', encoding='ascii')
        unknown_macro = 0
        try:
            for original in self.saved.iter_all():
                row = original['record']; path = row['path']
                key = json.dumps(path, ensure_ascii=True, separators=(',', ':'))
                decision = self.db.execute('SELECT producer,outcome FROM decisions WHERE key=?', (key,)).fetchone()
                if decision is None:
                    if row['kind'] in (0, 10, 99):
                        producer, outcome = 'ORIGINAL_CONTAINER_OR_EMPTY', 'ALL_TYPE_ORDER_AND_EMPTY_RETAINED'
                    elif path[:1] != ['MACROLIB']:
                        producer, outcome = 'ORIGINAL_MICRO_INPUT', 'FULL_ORIGINAL_INPUT_RETAINED'
                    else:
                        producer, outcome = 'ORIGINAL_PRESENT_NO_PROVED_AGGREGATION_RULE', 'UNQUALIFIED_NOT_DROPPED'
                        unknown_macro += 1
                else:
                    producer, outcome = decision
                self.producer_counts[producer] = self.producer_counts.get(producer, 0)+1
                self.line(stream, dict(original=original, producer=producer, outcome=outcome))
        finally:
            stream.close()
        return unknown_macro

    def compare_known_components(self, path, actual, expected, known, mask_bit, eligibility, producer):
        """One complete field report, exact known pairs and every mismatch.

        Unknown actual values remain in their original complete pool/span; no
        fabricated expectation is inserted for them. A compact disk pair stream
        prevents repeating a full native-row descriptor for each component.
        """
        self.comparisons += 1
        begin = self.expected.tell()
        compared = mismatches = 0
        for index, mask in enumerate(known):
            if not mask & mask_bit:
                continue
            self.budget()
            bits = expected[index]
            self.expected.write(struct.pack('<II', index, bits))
            self.compared_elements += 1
            compared += 1
            if bits != actual[index]:
                self.mismatch_elements += 1
                mismatches += 1
                ev, av = struct.unpack('<f', struct.pack('<I', bits))[0], struct.unpack('<f', struct.pack('<I', actual[index]))[0]
                self.line(self.mismatches, dict(path=list(path), producer=producer,
                    element_zero_based=index, expected_bits_hex=struct.pack('<I',bits).hex(),
                    actual_bits_hex=struct.pack('<I',actual[index]).hex(),
                    expected_binary64=ev if math.isfinite(ev) else None,
                    actual_binary64=av if math.isfinite(av) else None,
                    absolute_delta=abs(av-ev) if math.isfinite(ev) and math.isfinite(av) else None,
                    known_mask=mask, eligibility=eligibility))
        self.line(self.fields, dict(path=list(path), producer=producer,
            actual_original_record=self.saved.row(path), original_component_count=len(actual),
            known_component_mask_hex=bytes(known).hex(), mask_bit=mask_bit,
            expected_pool_begin=begin, expected_pool_end=self.expected.tell(),
            expected_pool_format='little_endian_u32_index_u32_expected_bits_pairs',
            compared_known_components=compared, differing_known_components=mismatches,
            unknown_original_components_preserved=len(actual)-compared,
            outcome='FULL_FIELD_RETAINED_KNOWN_COMPONENTS_COMPARED_UNKNOWN_UNQUALIFIED',
            eligibility=eligibility))

    def close(self):
        self.db.commit()
        self.db.close()
        for stream in (self.coverage, self.fields, self.mismatches, self.events, self.expected):
            stream.close()


class CompleteConstruction:
    def __init__(self, saved, evidence, context, route):
        self.saved, self.evidence, self.context, self.route = saved, evidence, context, route
        self.fp = Binary32Model()
        self.aliases = context['complete62_LIBIPS_aliases_one_based']
        self.mix = self.vector(('ISOTOPESMIX',), 1, ISOTOPES)
        self.density = self.vector(('ISOTOPESDENS',), 2, ISOTOPES)
        self.root_state = self.vector(('STATE-VECTOR',), 1, 40)
        self.macro_state = self.vector(('MACROLIB','STATE-VECTOR'), 1, 40)
        self.chi_limits = self.vector(('CHI-LIMITS',), 1, SPECTRA+1)
        require(self.chi_limits[0] == 0 and self.chi_limits[-1] == GROUPS and
                all(a < b for a,b in zip(self.chi_limits, self.chi_limits[1:])), 'full actual CHI-LIMITS')
        self.indfis = self.vector(('MACROLIB','FISSIONINDEX'), 1, MIXES*SLOTS)
        require(all(0 <= x <= ISOTOPES for x in self.indfis), 'complete64 FISSIONINDEX bounds')
        require(self.root_state[5] == 0 and self.root_state[25] == 0,
                'actual forward / no companion route; unsupported branches not guessed')
        particle = self.saved.row(('PARTICLE',))
        if particle is not None:
            require(particle['kind']==3 and particle['declared_count']>=1,
                    'original particle character type/count')
            first = self.saved.range_bytes(particle,0,1)
            require(first in (b'N',b' '),'charged-particle/Sternheimer producer unsupported, never guessed')
        # Actual V23 root STATE27=1 is permitted: LIBDEN Sternheimer arithmetic
        # is additionally conditional on HPRT1 B/C and is inert for neutrons.
        self.extra_names = [bytes.fromhex(x).decode('ascii') for x in context['original_18_extra_name_bytes_hex']]
        require(len(self.extra_names) == EXTRAS, 'all declared18 names, no reaction-selection')
        self.model_eligibility = dict(final_micro_constructed_independently=True,
            all370_groups_and8_mixes_requested=True, density_order='original62_no_dedup',
            model='MODEL_SEPARATE_ROUND32', historical_old_macro_available=False,
            historical_tracking_MASK_proved=False, historical_branch_proved=False,
            historical_SPHand_compiled_link_proved=False)
        self.nxs, self.timfact = self.perturbation()
        self.scalar_presence = {}
        self.overv_fallback_expected = None
        self.full_scattering_math_items = 0
        self.fission_mapping_validated = False
        self.delayed_zero_components_context_known = False
        self.diffusion_old_flag = None
        self.evidence.event('SOURCE_CONTEXT_NOT_SAVED', missing=['pre_call_MACROLIB','TONDRV actual tracking MAT',
            'last_call MASK/MASKL and old timestamp','historical SPH factors and actual compiled arithmetic linkage'],
            full_final_construction_model_continues=True, invented_old_macro=False,
            assumed_SPH_one=False, assumed_all_actual_MASK_true=False)

    def vector(self, path, kind, count, required=True):
        row = self.saved.row(path)
        if row is None:
            if required:
                self.evidence.event('REQUIRED_OPERAND_MISSING', path=list(path), expected_type=kind, expected_count=count)
                raise ValueError('required operand absent '+repr(path))
            self.evidence.event('ORIGINAL_ABSENCE_SOURCE_OPTIONAL', path=list(path))
            return None
        require(row['kind'] == kind and row['declared_count'] == count and
                row['native_payload_end_byte']-row['native_payload_begin_byte'] <= 2**20,
                'original operand type/count differs '+repr(path))
        raw = b''.join(self.saved.iter_raw(row))
        if kind == 3:
            return raw
        require(kind in (1,2), 'no raw type coercion')
        result = make_array(raw, kind == 1)
        if kind == 2:
            for bits in result:
                self.fp.ratio(bits)
        return result

    def micro_path(self, isotope, name, suffix='    '):
        require(type(isotope) is int and 1 <= isotope <= ISOTOPES, 'all original isotope slots')
        key = (name.ljust(8)+suffix).rstrip(' ')
        return ('ISOTOPESLIST', self.aliases[isotope-1], key)

    def micro(self, isotope, name, kind=2, count=GROUPS, suffix='    ', required=True):
        path = self.micro_path(isotope, name, suffix)
        self.evidence.event('ISOTOPE_OPERAND_PRESENCE', isotope=isotope, alias=self.aliases[isotope-1],
            own_mix=self.mix[isotope-1], own_density_bits_hex=struct.pack('<I',self.density[isotope-1]).hex(),
            path=list(path), present=self.saved.row(path) is not None)
        return self.vector(path, kind, count, required)

    @staticmethod
    def macro_path(group, name):
        return ('MACROLIB','GROUP',group,name.rstrip(' '))

    def compare_groups(self, name, matrix, producer, eligibility=None):
        for group in range(1, GROUPS+1):
            self.evidence.compare(self.macro_path(group,name), 2,
                array('I', (matrix[(group-1)*MIXES+m] for m in range(MIXES))),
                producer, self.model_eligibility if eligibility is None else eligibility)

    def perturbation(self):
        require(type(self.route) is dict and self.route['schema'] == 'ROOT_BOUND_FINAL_TONE_LIBMIX_SOURCE_ROUTE_V1'
                and self.route['ITSTMP'] == 0 and type(self.route['ITSTMP']) is int
                and self.route['historical_call_proved'] is False,
                'explicit Source route is not fabricated actual call history')
        times = self.saved.row(('TIMESPER',))
        if times is not None and 2 <= times['declared_count'] <= 6:
            raise ValueError('LIBDEN135: perturbation forbidden on this original TONE route; no TIMFCT override')
        return 1, 0

    def scalar(self):
        names = ('NTOT0','NTOT1','STRD','H-FACTOR','C-FACTOR','OVERV','TRANC')
        accum = {name:array('I',[0])*(GROUPS*MIXES) for name in names}
        present = {name:False for name in names}
        for mix in range(1,MIXES+1):
            total_density = 0
            for isotope in range(1,ISOTOPES+1):
                density = self.density[isotope-1]
                if self.mix[isotope-1] != mix or not self.fp.nonzero(density):
                    self.evidence.event('SOURCE_SCALAR_ISOTOPE_SKIP', mix=mix,isotope=isotope,
                        reason='own_mix_or_original_zero_density')
                    continue
                total_density = self.fp.add(total_density,density)
                for suffix in SUFFIXES[:self.nxs]:
                    for name in names:
                        required = name == 'NTOT0' or (name == 'TRANC' and self.root_state[4] != 0)
                        if name == 'TRANC' and self.root_state[4] == 0:
                            continue
                        values = self.micro(isotope,name,suffix=suffix,required=required)
                        if values is None:
                            continue
                        present[name] = True
                        for group, bits in enumerate(values):
                            index = group*MIXES+mix-1
                            accum[name][index] = self.fp.add(accum[name][index], self.fp.multiply(bits,density))
                    density = self.fp.multiply(density,self.timfact)
            if present['OVERV']:
                for group in range(GROUPS):
                    index = group*MIXES+mix-1
                    if self.fp.nonzero(accum['OVERV'][index]):
                        accum['OVERV'][index] = self.fp.divide(accum['OVERV'][index],total_density)
        self.scalar_presence = present
        extra_overwrites = {name.rstrip(' ') for name in self.extra_names
            if name[:2]!='NW' and name.rstrip(' ')!='TRANC' and name[:3]not in('BST','CST') and name[:8]!='H-FACTOR'}
        for name in names:
            if not present[name]:
                self.evidence.event('SOURCE_NO_OUTPUT_IF_ALL_ABSENT',field=name)
                continue
            if name == 'STRD':
                # Conditional LDIFF comes from old macro STATE9. Neither final
                # STATE9 nor present STRD proves the pre-call LDIFF selection.
                for i,bits in enumerate(accum[name]):
                    if self.fp.nonzero(bits):
                        accum[name][i] = self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,bits))
                output = 'DIFF'
                eligibility = dict(self.model_eligibility, pre_call_LDIFF_unknown=True)
            else:
                output, eligibility = name, self.model_eligibility
            if output in extra_overwrites:
                self.evidence.event('SOURCE_INTERMEDIATE_SCALAR_EXTRA_MAY_OVERWRITE',field=output,
                    final_extra_producer_compared_later=True,old_extra_EXIST_unknown=True)
                continue
            self.compare_groups(output,accum[name],'LIBDEN_SCALAR_'+name,eligibility)
        if not present['OVERV']:
            energy = self.vector(('ENERGY',),2,GROUPS+1)
            if not self.fp.nonzero(energy[-1]):
                energy[-1] = self.fp.f64_to32(1e-5)
            sqfmas = math.sqrt(2.0e4*1.60217653e-19/1.67492728e-27)
            expected = array('I',[0])*(GROUPS*MIXES)
            for group in range(GROUPS):
                average = self.fp.sqrt(self.fp.multiply(energy[group],energy[group+1]))
                square_root32 = self.fp.sqrt(average)
                sqv = struct.unpack('<f',struct.pack('<I',square_root32))[0]
                require(sqv != 0.0, 'OVERV fallback zero energy')
                value = self.fp.f64_to32(1.0/(float(sqv)*sqfmas))
                for mix in range(MIXES):
                    expected[group*MIXES+mix] = value
            # The fallback is after the extra edit loop in LIBDEN, and thus
            # does overwrite a declared OVERV extra when LOVERV is false.
            self.overv_fallback_expected = expected

    def overv_fallback(self):
        if self.overv_fallback_expected is not None:
            self.compare_groups('OVERV',self.overv_fallback_expected,
                'LIBDEN_OVERV_FALLBACK_XDRCST_SOURCE_CONSTANTS',
                dict(self.model_eligibility, double_sqrt_and_libm_historical_bits_unproved=True))
            self.overv_fallback_expected = None

    def extras(self):
        for ordinal,name in enumerate(self.extra_names,1):
            actual_name = name.rstrip(' ')
            if name[:2] == 'NW' or actual_name == 'TRANC' or name[:3] in ('BST','CST') or name[:8] == 'H-FACTOR':
                self.evidence.event('DECLARED_EXTRA_SPECIAL_PRODUCER',declared_ordinal=ordinal,
                    complete8byte_name_hex=name.encode('ascii').hex(),name=actual_name,
                    scope_retained=True, not_a_density_sum=True)
                continue
            expected = array('I',[0])*(GROUPS*MIXES)
            exists = False
            for mix in range(1,MIXES+1):
                for isotope in range(1,ISOTOPES+1):
                    density = self.density[isotope-1]
                    if self.mix[isotope-1] != mix or not self.fp.nonzero(density):
                        continue
                    for suffix in SUFFIXES[:self.nxs]:
                        values = self.micro(isotope,name,suffix=suffix,required=False)
                        if values is None:
                            self.evidence.event('LIBDEN_EXTRA_GOTO720',isotope=isotope,name=actual_name,
                                suffix=suffix,later_suffixes_not_read=True,density_not_advanced=True)
                            break
                        exists = True
                        for group,bits in enumerate(values):
                            index = group*MIXES+mix-1
                            expected[index] = self.fp.add(expected[index],self.fp.multiply(bits,density))
                        density = self.fp.multiply(density,self.timfact)
            if exists:
                if actual_name == 'OVERV' and not self.scalar_presence.get('OVERV', False):
                    self.evidence.event('SOURCE_INTERMEDIATE_EXTRA_OVERV_OVERWRITTEN_BY_FALLBACK',
                        declared_ordinal=ordinal, complete8byte_name_hex=name.encode('ascii').hex(),
                        intermediate_density_sum_saved=False, final_fallback_compared=True)
                    continue
                self.compare_groups(actual_name,expected,'LIBDEN_DECLARED_EXTRA_'+str(ordinal),
                    dict(self.model_eligibility, original_declared_name_hex=name.encode('ascii').hex(),
                         old_macro_EXIST_unknown=True))
            else:
                self.evidence.event('SOURCE_NO_FRESH_EXTRA_WRITE',declared_ordinal=ordinal,
                    complete8byte_name_hex=name.encode('ascii').hex(), old_macro_EXIST_unknown=True)

    def scattering(self):
        for moment in range(MOMENTS):
            cm = f'{moment:02d}'
            check = array('I',[0])*(GROUPS*MIXES)
            for dest_begin in range(0,GROUPS,50):
                width = min(50,GROUPS-dest_begin)
                gaff = array('I',[0])*(MIXES*GROUPS*width)
                sigs = array('I',[0])*(MIXES*width)
                for isotope in range(1,ISOTOPES+1):
                    density = self.density[isotope-1]
                    if not self.fp.nonzero(density):
                        continue
                    mix = self.mix[isotope-1]-1
                    fact = 0x3f800000
                    for suffix in SUFFIXES[:self.nxs]:
                        sigma = self.micro(isotope,'SIGS'+cm,suffix=suffix,required=False)
                        if sigma is None:
                            fact = self.fp.multiply(fact,self.timfact)
                            continue
                        njj = self.micro(isotope,'NJJS'+cm,1,suffix=suffix)
                        ijj = self.micro(isotope,'IJJS'+cm,1,suffix=suffix)
                        require(all(0 <= n <= GROUPS and (n == 0 or n <= j <= GROUPS)
                            for n,j in zip(njj,ijj)), 'full microscopic sparse bounds')
                        count = sum(njj)
                        scat = self.micro(isotope,'SCAT'+cm,count=count,suffix=suffix)
                        cursor = sum(njj[:dest_begin])
                        for block in range(width):
                            dest = dest_begin+block
                            sigs[block*MIXES+mix] = self.fp.add(sigs[block*MIXES+mix],
                                self.fp.multiply(sigma[dest],density))
                            for source in range(ijj[dest]-1,ijj[dest]-njj[dest]-1,-1):
                                index = (block*MIXES+mix)*GROUPS+source
                                t1 = self.fp.multiply(scat[cursor],density)
                                t2 = self.fp.multiply(t1,fact)
                                gaff[index] = self.fp.add(gaff[index],t2)
                                cursor += 1
                        require(cursor == sum(njj[:dest_begin+width]), 'all micro sparse payload components accounted')
                        fact = self.fp.multiply(fact,self.timfact)
                for block in range(width):
                    dest = dest_begin+block
                    p = self.macro_path(dest+1,'SIGS'+cm)
                    self.evidence.compare(p,2,sigs[block*MIXES:(block+1)*MIXES],
                        'LIBDEN_SIGS_INDEPENDENT_OF_SCAT_SUM',self.model_eligibility)
                    output = array('I'); nvec=array('i'); ivec=array('i'); pos=array('i'); selfvec=array('I')
                    # Every mathematical source cell, including proven sparse
                    # initialized zeros, gets a complete domain digest. No
                    # absent SCAT record is converted to such a zero cell.
                    domain_digest = hashlib.sha256()
                    for mix in range(MIXES):
                        offset = (block*MIXES+mix)*GROUPS
                        domain = gaff[offset:offset+GROUPS]
                        domain_digest.update(bytes_array(domain))
                        self.full_scattering_math_items += GROUPS
                        active = [i for i,bits in enumerate(domain) if self.fp.nonzero(bits)]
                        low = min([dest,*active]); high = max([dest,*active])
                        pos.append(len(output)+1); nvec.append(high-low+1); ivec.append(high+1)
                        for source in range(high,low-1,-1):
                            bits=domain[source]
                            output.append(bits)
                            index=source*MIXES+mix
                            check[index]=self.fp.add(check[index],bits)
                        selfvec.append(domain[dest])
                    self.evidence.event('FULL_SCATTERING_DOMAIN',moment=moment,destination_one_based=dest+1,
                        mixes=MIXES,sources=GROUPS, mathematical_domain_sha256=domain_digest.hexdigest(),
                        native_padding_not_normalized=True, historical_LOGL_not_proved=True)
                    for name,kind,values in (('SCAT'+cm,2,output),('NJJS'+cm,1,nvec),
                            ('IJJS'+cm,1,ivec),('IPOS'+cm,1,pos),('SIGW'+cm,2,selfvec)):
                        self.evidence.compare(self.macro_path(dest+1,name),kind,values,
                            'LIBDEN_COMPRESSED_SCAT_'+name,self.model_eligibility)
                del gaff,sigs
            self.compare_groups('CHECK'+cm,check,'LIBDEN_CHECK_DESTINATION_ORDER_SOURCE_SUM')
        require(self.full_scattering_math_items == GROUPS*GROUPS*MIXES*MOMENTS,
                'all370x370x8x3 mathematical cells retained')

    def fission(self):
        # Reconstructing fresh slot allocation would ignore original old64.
        # The actual final map is checked, used as input and explicitly never
        # compared to itself as a historical slot-allocation proof.
        mapped = set()
        for slot in range(SLOTS):
            for mix in range(MIXES):
                isotope=self.indfis[slot*MIXES+mix]
                if isotope == 0:
                    self.evidence.event('ORIGINAL_EMPTY_FISSION_SLOT',slot=slot+1,mix=mix+1)
                    continue
                require(self.mix[isotope-1] == mix+1,'original fission slot isotope/mix mismatch')
                require((mix,isotope) not in mapped,'same isotope duplicated in actual fission slots')
                mapped.add((mix,isotope))
                nuf=self.micro(isotope,'NUSIGF')
                chi=self.micro(isotope,'CHI--01')
                require(any(self.fp.ratio(x)[0] > 0 for x in chi),'mapped isotope has no positive CHI--01')
                self.evidence.event('ACTUAL64_FISSION_INDEX_BINDING',slot=slot+1,mix=mix+1,
                    isotope=isotope,alias=self.aliases[isotope-1],own_density_bits_hex=struct.pack('<I',self.density[isotope-1]).hex(),
                    actual_native_value=self.indfis[slot*MIXES+mix],historical_slot_allocation_proved=False)
        for isotope in range(1,ISOTOPES+1):
            nuf=self.micro(isotope,'NUSIGF',required=False)
            chi=self.micro(isotope,'CHI--01',required=False)
            if nuf is not None and chi is not None and any(self.fp.ratio(x)[0] > 0 for x in chi):
                require((self.mix[isotope-1]-1,isotope) in mapped,'all actual fissile isotopes must appear in map')
        self.fission_mapping_validated=True
        self.evidence.decision(('MACROLIB','FISSIONINDEX'),'ORIGINAL64_MAPPING_CONSISTENCY',
            'ACTUAL_ISOTOPE_MIX_BINDING_ONLY_NOT_HISTORICAL_ALLOCATION')
        for delayed in range(DELAYED+1):
            nus=array('I',[0])*(GROUPS*MIXES*COMPONENTS)
            chis=array('I',[0])*(GROUPS*MIXES*COMPONENTS)
            known=array('B',[0])*(MIXES*COMPONENTS)
            for spectrum in range(SPECTRA):
                for slot in range(SLOTS):
                    for mix in range(MIXES):
                        isotope=self.indfis[slot*MIXES+mix]
                        index=(slot*SPECTRA+spectrum)*MIXES+mix
                        if isotope == 0 or (delayed and spectrum != 0):
                            self.evidence.event('FISSION_INITIAL_OR_OLD_CONTEXT_UNKNOWN',delayed=delayed,
                                spectrum=spectrum+1,slot=slot+1,mix=mix+1,
                                exact_source_condition='KFIS.GT.NFISS0*NESP',
                                original_component_preserved=True,zero_not_asserted=True)
                            continue
                        den=self.density[isotope-1]
                        for ix,suffix in enumerate(SUFFIXES[:self.nxs]):
                            if delayed:
                                last=self.micro(isotope,f'NUSIGF{DELAYED:02d}',suffix=suffix,required=False)
                                values=None if last is None else self.micro(isotope,f'NUSIGF{delayed:02d}',suffix=suffix)
                                last_chi=self.micro(isotope,f'CHI{DELAYED:02d}',suffix=suffix,required=False)
                                chi_values=None if last_chi is None or ix != 0 else self.micro(isotope,f'CHI{delayed:02d}',suffix=suffix)
                            else:
                                values=self.micro(isotope,'NUSIGF',suffix=suffix)
                                chi_values=self.micro(isotope,f'CHI--{spectrum+1:02d}',suffix=suffix,required=False) if ix == 0 else None
                            if values is not None:
                                begin,end=(0,GROUPS) if delayed else (self.chi_limits[spectrum],self.chi_limits[spectrum+1])
                                for group in range(begin,end):
                                    loc=group*MIXES*COMPONENTS+index
                                    nus[loc]=self.fp.add(nus[loc],self.fp.multiply(values[group],den))
                                known[index]|=1
                            if chi_values is not None:
                                for group,bits in enumerate(chi_values):
                                    chis[group*MIXES*COMPONENTS+index]=bits
                                known[index]|=2
                            den=self.fp.multiply(den,self.timfact)
            nus_name='NUSIGF' if delayed == 0 else f'NUSIGF{delayed:02d}'
            chi_name='CHI' if delayed == 0 else f'CHI{delayed:02d}'
            # Unknown entries use no fabricated expectation. Native bytes for
            # all256 components remain in coverage and full field span hashes;
            # known-entry masks are persisted separately and full scope fails.
            for group in range(GROUPS):
                for name,values,bit in ((nus_name,nus,1),(chi_name,chis,2)):
                    actual=self.vector(self.macro_path(group+1,name),2,MIXES*COMPONENTS)
                    self.evidence.compare_known_components(self.macro_path(group+1,name),actual,
                        values[group*MIXES*COMPONENTS:(group+1)*MIXES*COMPONENTS],known,bit,
                        self.model_eligibility,'LIBDEN_PROMPT_AND_ALL6_DELAYED_FULL256')
                    self.evidence.decision(self.macro_path(group+1,name),
                        'LIBDEN_PROMPT_AND_ALL6_DELAYED_FULL256',
                        'KNOWN_COMPONENTS_COMPARED_ALL_UNKNOWN_ORIGINAL_COMPONENTS_RETAINED')
                    self.evidence.event('FULL256_COMPONENT_KNOWN_MASK',path=list(self.macro_path(group+1,name)),
                        known_mask_hex=bytes(known).hex(),all256_original_bits_preserved=True,
                        unknown_components_not_filled_or_qualified=True)
            del nus,chis,known
        self.lambdas()

    def lambdas(self):
        actual=self.vector(('MACROLIB','LAMBDA-D'),2,DELAYED*SLOTS)
        expected=array('I',[0])*(DELAYED*SLOTS)
        known=[False]*SLOTS
        for slot in range(SLOTS):
            for mix in range(MIXES):
                isotope=self.indfis[slot*MIXES+mix]
                if not isotope:
                    continue
                values=self.micro(isotope,'LAMBDA-D',count=DELAYED,required=False)
                if values is not None:
                    expected[slot*DELAYED:(slot+1)*DELAYED]=values
                    known[slot]=True
                    self.evidence.event('LAMBDA_SLOT_LAST_WRITE',slot=slot+1,mix_loop=mix+1,isotope=isotope,
                        density_not_used=True,layout='NDEL6 x NFISSI8; not mix table')
        known_mask = array('B',(3 if known[index//DELAYED] else 0 for index in range(DELAYED*SLOTS)))
        self.evidence.compare_known_components(('MACROLIB','LAMBDA-D'),actual,expected,
            known_mask,1,self.model_eligibility,'LIBDEN_LAMBDA48_SLOT_LAST_MIX_WRITE')
        self.evidence.decision(('MACROLIB','LAMBDA-D'),'LIBDEN_LAMBDA48_SLOT_LAST_MIX_WRITE',
            'KNOWN_SLOTS_COMPARED_UNKNOWN_OLD_VALUES_NOT_ZERO_FILLED')

    def metadata(self):
        for name in ('ADDXSNAME-P0','PARTICLE-NGR','PARTICLE-MC2'):
            row=self.saved.row((name,))
            if row is None:
                self.evidence.event('ORIGINAL_METADATA_ABSENCE',name=name)
                continue
            raw=b''.join(self.saved.iter_raw(row))
            self.evidence.compare(('MACROLIB',name),row['kind'],raw,
                'LIBDEN_DIRECT_COPY_'+name,self.model_eligibility)
        for name in ('PARTICLE','PARTICLE-NAM'):
            if self.saved.row((name,)) is not None:
                self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field=name,
                    reason='LCMGTC length1 followed by LCMPTC length1 is a character projection, not raw word copy',
                    original_full_words_retained=True,character_padding_arithmetic_not_guessed=True)
        energy=self.vector(('ENERGY',),2,GROUPS+1)
        if not self.fp.nonzero(energy[-1]):
            energy[-1]=self.fp.f64_to32(1e-5)
        self.evidence.compare(('MACROLIB','ENERGY'),2,energy,'LIBDEN_ENERGY_FRESH_ONLY',
            dict(self.model_eligibility,old_macro_energy_copy_branch_unknown=True))
        signature=self.saved.row(('MACROLIB','SIGNATURE'))
        require(signature is not None and signature['kind']==3,'original macro signature required')
        self.evidence.compare(('MACROLIB','SIGNATURE'),3,b'L_MACROLIB  ',
            'LIBDEN_SIGNATURE_LITERAL',self.model_eligibility)
        volumes=self.vector(('ISOTOPESVOL',),2,ISOTOPES,required=False)
        current=self.vector(('MIXTURESVOL',),2,MIXES,required=False)
        expected=None
        if volumes is not None:
            expected=array('I',[0])*MIXES
            for isotope in range(ISOTOPES):
                expected[self.mix[isotope]-1]=volumes[isotope]
            self.evidence.compare(('MIXTURESVOL',),2,expected,
                'LIBDEN_ISOTOPESVOL_LAST_WRITE',self.model_eligibility)
        elif current is not None:
            expected=current
            self.evidence.event('ORIGINAL_MIXTURESVOL_USED_WITHOUT_ISOTOPESVOL',
                not_independent_volume_production_proof=True)
        if expected is not None:
            self.evidence.compare(('MACROLIB','VOLUME'),2,expected,'LIBDEN_VOLUME_COPY',self.model_eligibility)
            for moment,name in ((0,'NWT0'),(1,'NWT1')):
                flux=array('I',[0])*(GROUPS*MIXES); any_present=False
                for isotope in range(1,ISOTOPES+1):
                    row = self.saved.row(self.micro_path(isotope,name))
                    if row is not None and row['declared_count'] != GROUPS:
                        self.evidence.event('SOURCE_INTEGRATED_FLUX_ILONG_NOT_NGROUP_SKIP',
                            isotope=isotope, field=name, original_record=row,
                            original_count_retained=True, skipped_like_LIBDEN=True)
                        continue
                    values=self.micro(isotope,name,required=False)
                    if values is None:
                        continue
                    any_present=True; mix=self.mix[isotope-1]-1
                    for group,bits in enumerate(values):
                        flux[group*MIXES+mix]=self.fp.multiply(bits,expected[mix])
                    self.evidence.event('INTEGRATED_FLUX_LAST_WRITE',field=name,isotope=isotope,
                        own_mix=mix+1,not_density_sum=True)
                if any_present:
                    self.compare_groups('FLUX-INTG' if moment==0 else 'FLUX-INTG-P1',flux,
                        'LIBDEN_'+name+'_LAST_WRITE_TIMES_VOLUME')
        # STATE/TIMESTAMP contain pre-call maxima/OLDTIM. Actual values and
        # SHIBA state are fully retained, but never copied back as expectations.
        for name in ('STATE-VECTOR','TIMESTAMP','SPH'):
            path=('MACROLIB',name)
            if self.saved.row(path) is not None:
                self.evidence.decision(path,'LIBDEN_HISTORICAL_CONTEXT_DEPENDENT_METADATA',
                    'ORIGINAL_PRESENT_HISTORY_UNPROVED_NO_FINAL_SELF_PROOF')
        self.evidence.event('STATE40_KNOWN_CURRENT_SCOPE',actual_macro_state=list(self.macro_state),
            expected_scope=[GROUPS,MIXES,MOMENTS,COMPONENTS],actual_root_state=list(self.root_state),
            SPH_presence_does_not_prove_factor_or_branch=True, historical_timestamp_not_synthesized=True)


def state_check(adapter, binding, state, output, budget):
    source=binding['states'][state]
    root=output/state;root.mkdir();temp=root/'sqlite_file_temp';temp.mkdir()
    saved=adapter.SavedNativeInput(source['sqlite_pin'],source['native_pool_pin'],temp,budget)
    evidence=None
    state_report=None
    try:
        evidence=DiskEvidence(root,saved,budget,state)
        evidence.inventory()
        context=adapter.capture_complete_fixed_context(saved)
        write_new(root/'ACTUAL_COMPLETE_FIXED_CONTEXT.json',context)
        model=CompleteConstruction(saved,evidence,context,binding['Source_route'])
        for label in ('scattering','scalar','fission','extras','overv_fallback','metadata'):
            try:
                getattr(model,label)()
                evidence.phase_results.append(dict(phase=label,computation_finished=True))
            except Exception as error:
                evidence.event('PHASE_FAILED',phase=label,error=repr(error),
                    remaining_original_coverage_not_removed=True)
                evidence.phase_results.append(dict(phase=label,computation_finished=False,error=repr(error)))
        unknown=evidence.complete_decisions()
        state_report=dict(state=state,all_original_records=evidence.records,
            complete_MACROLIB_records=evidence.macro_records, original_scope=[370,8,3,32,64,62,18,6,48],
            complete_source_field_comparisons=evidence.comparisons,
            compared_known_elements=evidence.compared_elements,
            all_mismatching_elements=evidence.mismatch_elements, all_context_or_operand_issues=evidence.issues,
            unknown_macro_producers=unknown,phase_results=evidence.phase_results,
            all_original_native_records_and_bytes_preserved=True,
            all_complete_orders_preserved=True,all_missing_fields_not_zero_filled=True,
            expected_binary32_model='MODEL_SEPARATE_ROUND32',
            binary32_model_operations=model.fp.operations,
            binary32_model_underflow_to_zero=model.fp.underflow_to_zero,
            binary32_model_overflow_to_infinity=model.fp.overflow_to_infinity,
            mathematical_scattering_domain_computed=model.full_scattering_math_items,
            expected_full_scattering_domain=370*370*8*3,
            actual64_isotope_mix_mapping_checked=model.fission_mapping_validated,
            complete_final_construction_qualified=False,
            historical_old_macro_proved=False,historical_actual_tracking_MASK_proved=False,
            historical_SPHand_compiled_arithmetic_proved=False,
            known_component_matching_does_not_qualify_unknown_delayed_or_inherited_fields=True,
            full_output_scope_retained_even_on_failure=True,**FALSE)
    finally:
        if evidence is not None:
            evidence.close()
        saved.close()
    require(state_report is not None,'full state report unavailable; no fabricated completion')
    # Both handles are closed before pins/report and before state B may open.
    files=[full_pin(p,budget)for p in sorted(root.rglob('*'))if p.is_file()]
    state_report['complete_output_file_pins']=files
    state_report['all_state_databases_and_pool_closed_before_next_state']=True
    write_new(root/'ACTUAL_COMPLETE_STATE_CONSTRUCTION_REPORT.json',state_report)
    return state_report


def main():
    started=time.monotonic()
    require(SOURCE_STATUS=='READY_ROOT_BOUND_SOURCE_ONLY'and type(SOURCE_BINDING_SHA256)is str
            and len(SOURCE_BINDING_SHA256)==64
            and BOUND_ADAPTER_PIN is not None,'UNREADY refuses import, payload read or output writes')
    require(not sys.flags.optimize and sys.getprofile() is None,'original unprofiled execution')
    require(all(os.environ.get(k)=='1'for k in
        ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')),
        'original single-thread child environment')
    parser=argparse.ArgumentParser()
    parser.add_argument('--binding',required=True)
    parser.add_argument('--binding-sha256',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--expected-parent-pid',required=True,type=int)
    args=parser.parse_args()
    require(os.getppid()==args.expected_parent_pid,'actual genuine host PID binding')
    output=Path(args.output_dir).absolute()
    require(not output.exists() and output.is_absolute(),'fresh complete output, zero retry')
    binding_path=Path(args.binding).absolute()
    last_archive_check = [0.0]
    archive_roots = [output]
    def budget():
        require(time.monotonic()-started<ORIGINAL_CAPS['stage_seconds'],'original600 stage budget')
        now=time.monotonic()
        if now-last_archive_check[0]>=0.25:
            last_archive_check[0]=now
            total=0
            for archive_root in archive_roots:
                if not archive_root.exists():continue
                for p in archive_root.rglob('*'):
                    s=p.lstat()
                    require(not stat.S_ISLNK(s.st_mode),'no joint output symlink escape')
                    if stat.S_ISREG(s.st_mode):total+=s.st_size
            # SQLite FILE temp sorts may unlink their names while still open.
            # Count those actual regular own-child descriptors separately;
            # every linked journal/DB/spool is already in the five namespaces.
            unlinked={}
            for fd_text in os.listdir('/dev/fd'):
                try:
                    fd=int(fd_text);s=os.fstat(fd)
                except (ValueError,OSError):
                    continue
                if stat.S_ISREG(s.st_mode)and s.st_nlink==0:
                    unlinked[(s.st_dev,s.st_ino)]=s.st_size
            total+=sum(unlinked.values())
            require(total<ORIGINAL_CAPS['joint_archive_bytes'],'full H/O/C/D/E plus open unlinked SQLite FILE temp bytes')
    binding_pin=full_pin(binding_path,budget)
    require(args.binding_sha256==SOURCE_BINDING_SHA256==binding_pin['sha256'],
            'bound actual Root binding bytes; actual installed7ID observed, never guessed')
    binding=strict_json(binding_path.read_bytes())
    require(binding['schema']=='ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1'
            and binding['source_only']is True and binding['Root_only_actual_execution']is True
            and binding['new_aggregation_qualification_sha256']is None
            and binding['actual_scientific_qualification_sha256']is None,'actual Source-only binding')
    require(type(binding['original_caps'])is dict and set(binding['original_caps'])==set(ORIGINAL_CAPS)
            and all(type(x)is int for x in binding['original_caps'].values())
            and binding['original_caps']==ORIGINAL_CAPS,'all original strict integer caps')
    require(binding['state_order']==['A','B']and set(binding['states'])=={'A','B'},'complete serial A then B')
    require(binding['namespaces']['output']==str(output),'actual owned output binding')
    require(type(binding['joint_archive_roots'])is list and len(binding['joint_archive_roots'])==5
            and binding['joint_archive_roots']==[binding['namespaces'][k]for k in('host','output','control','source','receipts')],
            'same complete original five-root budget')
    archive_roots[:]=[Path(p)for p in binding['joint_archive_roots']]
    complete_pins=binding['complete_input_pins']
    require(type(complete_pins)is list and len(complete_pins)>=129
            and len({p['path']for p in complete_pins})==len(complete_pins),'all original129 plus actual evidence inputs')
    for pin in complete_pins:check_pin(pin,budget)
    check_pin(BOUND_ADAPTER_PIN,budget)
    require(binding['saved_native_adapter_pin']==BOUND_ADAPTER_PIN,'same full saved-native adapter Source')
    spec=importlib.util.spec_from_file_location('root_bound_saved_native_adapter',BOUND_ADAPTER_PIN['path'])
    adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
    require(adapter.ORIGINAL_CAPS==ORIGINAL_CAPS,'adapter original caps')
    output.mkdir()
    states=[]
    error=None
    try:
        for state in ('A','B'):
            # state_check closes both SQLite and paired pool in its finally.
            states.append(state_check(adapter,binding,state,output,budget))
        for pin in complete_pins:check_pin(pin,budget)
        check_pin(binding_pin,budget);check_pin(BOUND_ADAPTER_PIN,budget)
    except BaseException as failure:
        error=repr(failure)
    report=dict(schema='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1',
        status='COMPLETE_ORIGINAL_SCOPE_RETAINED_CONSTRUCTION_INCOMPLETE_NO_QUALIFICATION',
        actual_child_PID=os.getpid(),actual_parent_PID=os.getppid(),source_binding=binding_pin,
        original_caps=ORIGINAL_CAPS, states=states, error=error,
        input_sources=complete_pins,whole_child_seconds=time.monotonic()-started,
        all_complete_state_scope_retained=len(states)==2,
        complete_final_construction_qualified=False,new_aggregation_qualification_sha256=None,
        actual_scientific_qualification_sha256=None,
        historical_context_missing_is_not_silently_supplied=True, **FALSE)
    report_path=output/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
    write_new(report_path,report)
    print(json.dumps(dict(status=report['status'],report=full_pin(report_path,lambda:None)),
        allow_nan=False),flush=True)
    # This complete source candidate has known unresolved historical/context
    # producers. Matching supported fields cannot yield a fabricated EXIT0 Q.
    raise SystemExit(2 if error is None else 1)


if __name__=='__main__':main()

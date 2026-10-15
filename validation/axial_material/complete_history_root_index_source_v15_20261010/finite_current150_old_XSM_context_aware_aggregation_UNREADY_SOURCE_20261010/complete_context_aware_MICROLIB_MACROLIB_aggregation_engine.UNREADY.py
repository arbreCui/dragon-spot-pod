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


"""Insertion-only Source fragment. Not importable in isolation or executed.

Uses original complete saved-native adapter and Binary32Model. Root must save
the actual observer stream and every old/post/final XSM first. None of those
future values/pins are supplied by this author. All record scopes remain full.
"""

class ObservedContext:
    """Full context words streamed to disk; MAT membership alone stays in RAM."""
    def __init__(self, pins, budget, evidence):
        require(type(pins)is list and pins,'actual full context list required')
        self.events=[];self.budget=budget;self.evidence=evidence
        previous=0;last_libmix=0;pending=[]
        for expected in pins:
            check_pin(expected,budget)
            with Path(expected['path']).open('rb')as stream:
                def take(size):
                    require(type(size)is int and 0<=size<=2**20,'bounded original context read')
                    budget();raw=stream.read(size)
                    require(len(raw)==size,'actual context truncation');return raw
                require(take(8)==b'AXOBSCTX','actual original observer magic')
                version,event,libmix,length=struct.unpack('<4i',take(16))
                require(version==2 and event==previous+1 and libmix>=0 and 1<=length<=256,
                    'all original consecutive events, no hidden prefix or sorting')
                previous=event;label=take(length).decode('ascii')
                fields={};dimensions={}
                def field(name,count,real=False,dimension=False,mat=False):
                    require(type(count)is int and count>=0,'all actual context field count')
                    require(mat or count<=65536,'bounded non-MAT actual context field')
                    begin=stream.tell();digest=hashlib.sha256();values=array('I'if real else'i')
                    membership=set()
                    for start in range(0,count,4096):
                        raw=take(4*min(4096,count-start));digest.update(raw)
                        chunk=make_array(raw,not real)
                        if mat:
                            require(all(0<=x<=MIXES for x in chunk),'full actual MAT region mix bounds')
                            membership.update(chunk)
                        else:values.extend(chunk)
                        evidence.event('FULL_ORIGINAL_CONTEXT_WORDS',event=event,libmix=libmix,label=label,
                            field=name,original_type='REAL32'if real else'INTEGER32',original_count=count,
                            element_begin0=start,full_original_bytes_hex=raw.hex())
                    evidence.event('FULL_ORIGINAL_CONTEXT_FIELD_EOF',event=event,label=label,field=name,
                        span_begin=begin,span_end=stream.tell(),original_count=count,
                        complete_original_SHA256=digest.hexdigest())
                    fields[name]=membership if mat else values
                    if dimension:dimensions.update(zip(name.split(','),values))
                if label=='LIBMIX_BEFORE':
                    field('NBMIX,NGROUP,NBISO,ITSTMP',4,dimension=True)
                    require(tuple(dimensions[k]for k in('NBMIX','NGROUP','NBISO'))==(8,370,62),'full LIBMIX scope')
                    field('ROOT_STATE40',40);field('MIX',62);field('DEN',62,True);field('TMPDAY',3,True)
                    field('MACRO_LENGTH,MACRO_KIND',2,dimension=True);field('MASK',8);field('MASKL',370)
                    field('MIXTURESVOL_LENGTH,MIXTURESVOL_KIND',2,dimension=True)
                    if dimensions['MIXTURESVOL_LENGTH']>0:
                        require(dimensions['MIXTURESVOL_LENGTH']==8 and dimensions['MIXTURESVOL_KIND']==2,'full observed root volume type/count')
                        field('ROOT_MIXTURESVOL_BEFORE',8,True)
                elif label=='LIBDEN_OLD_CONTEXT':
                    field('NBMIX,NGROUP,NBISO,NL,NDEL,NESP,NED,ITRANC,MAXNFI,NPART,ITSTMP,STERN,NFISSI',13,dimension=True)
                    require(tuple(dimensions[k]for k in('NBMIX','NGROUP','NBISO','NL','NDEL','NESP','NED'))==
                        (8,370,62,3,6,4,18),'all original construction dimensions')
                    field('TMPDAY',3,True);field('LSAME,MASKK,LALL,LDIFF',4);field('MASK',8);field('MASKL',370)
                elif label=='LIBDEN_BEFORE_FISSION_SLOT_MUTATION':
                    field('NBMIX,MAXNFI,NFISS0,NFISSI',4,dimension=True)
                    require(dimensions['NBMIX']==8 and 0<=dimensions['NFISS0']==dimensions['NFISSI']<=dimensions['MAXNFI']<=62,
                        'complete defined original pre-mutation extent')
                    field('INDFIS_DEFINED_PRE_MUTATION',8*dimensions['NFISSI'])
                elif label=='TONDRV_AFTER_REAL_MAT_ELIMINATION':
                    field('NREG,NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPROB,IGRMIN,IGRMAX',9,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370)and dimensions['NREG']>0,
                        'complete actual tracking scope')
                    field('MAT',dimensions['NREG'],mat=True);field('MIX',62);field('LSHI',62);field('DEN',62,True)
                elif label=='TONDRV_ACTUAL_FINAL_LIBMIX_MASK':
                    field('NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPHASE,NRES2,ITSTMP',8,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370),'full mask scope')
                    field('LSHI',62);field('LSHI2',62);field('TMPDAY',3,True);field('MASK',8);field('MASKL',370)
                elif label=='TONSPH_BEFORE_ACTUAL_TONCMI':
                    field('NBM,NBISO,NGRO,INRS,ITRANC,IGRMIN,IGRMAX',7,dimension=True)
                    require(tuple(dimensions[k]for k in('NBM','NBISO','NGRO'))==(8,62,370),'all actual SPH factors')
                    field('MASKI',62);field('SPH',8*370,True)
                elif label=='TONDRV_ACTUAL_SPH_CALL_DECISION':
                    field('NBISO,NBMIX,NGRO,INRS,NBNRS,NRES2,KSPH',7,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370),'full Source SPH decision scope')
                    field('LSHI2',62)
                elif label not in('LIBMIX_AFTER','TONDRV_FINAL_AFTER_SHIBA'):
                    raise ValueError('unhandled original event, never skipped '+label)
                require(stream.read(1)==b'','complete context EOF, no omitted extra word')
                for name in('MASK','MASKL','MASKI','LSAME,MASKK,LALL,LDIFF'):
                    if name in fields:require(all(x in(0,1)for x in fields[name]),'actual logical merge words exact0/1')
                current=dict(event=event,libmix=libmix,label=label,fields=fields,dimensions=dimensions,input=expected)
                if label=='LIBMIX_BEFORE':
                    require(not pending and libmix==last_libmix+1,'full consecutive original LIBMIX begin')
                    last_libmix=libmix;pending=[current]
                    self.events=[e for e in self.events if e['label']not in
                        ('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER')]
                elif label in('LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'):
                    sequence=('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER')
                    require(pending and libmix==last_libmix and label==sequence[len(pending)],'all Source call phases in exact original order')
                    pending.append(current)
                    if label=='LIBMIX_AFTER':
                        evidence.event('FULL_ACTUAL_CALL_CONTEXT',libmix=libmix,event_numbers=[e['event']for e in pending]);pending=[]
                elif label=='TONDRV_AFTER_REAL_MAT_ELIMINATION':
                    require(not pending,'no hidden incomplete preceding original call')
                    self.events=[]
                self.events.append(current)
            check_pin(expected,budget)
        require(not pending,'no incomplete original call at complete EOF')
        self.full_original_event_count=previous
        require(self.events[-1]['label']=='TONDRV_FINAL_AFTER_SHIBA','complete observer end required')
        # Retain every event, but select the genuinely final completed LIBMIX.
        calls={};last_begin=0
        for e in self.events:
            if e['label']=='LIBMIX_BEFORE':
                last_begin=e['libmix'];calls[last_begin]=[e]
            elif e['label']in('LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'):
                require(e['libmix']in calls,'call context without original LIBMIX begin')
                calls[e['libmix']].append(e)
        require(calls,'actual complete LIBMIX calls required')
        for number,events in calls.items():
            labels=[e['label']for e in events]
            require(labels==['LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'],
                'full current MXS call context, no incomplete call treated as complete')
            evidence.event('FULL_ACTUAL_CALL_CONTEXT',libmix=number,event_numbers=[e['event']for e in events])
        self.before,self.old,self.fission,self.after=calls[last_begin]
        track=[e for e in self.events if e['label']=='TONDRV_AFTER_REAL_MAT_ELIMINATION'and e['event']<self.before['event']]
        masks=[e for e in self.events if e['label']=='TONDRV_ACTUAL_FINAL_LIBMIX_MASK'and e['event']<self.before['event']]
        require(track and masks,'real MAT and final-mask events required, no inferred ones')
        self.track,self.mask=track[-1],masks[-1]
        t,m,b,o=self.track['fields'],self.mask['fields'],self.before['fields'],self.old['fields']
        require(b['MIX']==t['MIX'] and b['DEN']==t['DEN'],'same actual mix/density in call and tracking')
        require(b['MASK']==m['MASK']==o['MASK']and b['MASKL']==m['MASKL']==o['MASKL'],'actual complete masks agree')
        require(all(t['LSHI'][i]==0 for i in range(ISOTOPES)if t['MIX'][i]not in t['MAT']),
            'Source TONDRV MAT-eliminated isotope flags remain zero')
        expected_mask=array('i',(int(any(b['MIX'][i]==mix and m['LSHI'][i]>0 for i in range(ISOTOPES)))for mix in range(1,9)))
        lo,hi=self.track['dimensions']['IGRMIN'],self.track['dimensions']['IGRMAX']
        require(1<=lo<=hi<=GROUPS and expected_mask==b['MASK']and
            b['MASKL']==array('i',(int(lo<=g<=hi)for g in range(1,GROUPS+1))),
            'Source exact MAT/LSHI/group-range mask derivation, never MASK=true default')
        require(self.mask['dimensions']['ITSTMP']==self.before['dimensions']['ITSTMP']==self.old['dimensions']['ITSTMP']==0,
            'current actual no-perturbation call route')
        # All earlier calls/events remain saved. Validate this final TONDRV's
        # actual decision list after its initial final-mask event.
        sph=[e for e in self.events if e['label']=='TONSPH_BEFORE_ACTUAL_TONCMI'and
            self.track['event']<e['event']<self.before['event']]
        for e in sph:
            require(self.track['dimensions']['KSPH']==1,'actual SPH branch is KSPH1')
            for bits in e['fields']['SPH']:Binary32Model.ratio(bits)
            evidence.event('ACTUAL_FULL_SPH_CAPTURE_RETAINED',event=e['event'],all2960_factor_words=True,
                factors_assumed_one=False,previous_history_reconstructed=False)
        decisions=[e for e in self.events if e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'and
            self.track['event']<e['event']<self.before['event']]
        ksph=self.track['dimensions']['KSPH']
        if ksph==1:
            nres=self.mask['dimensions']['NRES2']
            require(type(nres)is int and 0<=nres<=ISOTOPES and
                [e['dimensions']['INRS']for e in decisions]==list(range(1,nres+1)),
                'every actual Source INRS decision required, no omitted false branch')
            require(all(e['dimensions']['KSPH']==1 and e['dimensions']['NRES2']==nres
                and e['dimensions']['NBNRS']>=0 for e in decisions),'actual SPH branch dimensions')
            selected=[e['dimensions']['INRS']for e in decisions if e['dimensions']['NBNRS']>1]
            require([e['dimensions']['INRS']for e in sph]==selected,'one full actual SPH factor event per true Source decision')
            require(all(e['fields']['LSHI2']==self.mask['fields']['LSHI2']for e in decisions),
                'all original SPH call-selection isotope flags unchanged')
        else:require(not decisions and not sph,'Source non-KSPH1 branch contains no SPH calls')
        self.complete_sph_call_selection_proved=True
        evidence.event('COMPLETE_ACTUAL_SPH_SELECTION',KSPH=ksph,all_original_decision_events=[e['event']for e in decisions],
            all_original_factor_events=[e['event']for e in sph],factors_assumed_one=False)


class ContextAwareConstruction(CompleteConstruction):
    """Final construction with actual old state; never a historical float replay."""
    def __init__(self,saved,evidence,context,route,observed,old_saved,pre_saved,post_saved):
        self.saved,self.evidence,self.context,self.route=saved,evidence,context,route
        self.observed,self.old_saved,self.pre_saved,self.post_saved=observed,old_saved,pre_saved,post_saved
        self.fp=Binary32Model();self.aliases=context['complete62_LIBIPS_aliases_one_based']
        self.mix=self.vector(('ISOTOPESMIX',),1,62);self.density=self.vector(('ISOTOPESDENS',),2,62)
        self.root_state=self.vector(('STATE-VECTOR',),1,40);self.macro_state=self.vector(('MACROLIB','STATE-VECTOR'),1,40)
        self.chi_limits=self.vector(('CHI-LIMITS',),1,5)
        require(self.chi_limits[0]==0 and self.chi_limits[-1]==370 and all(a<b for a,b in zip(self.chi_limits,self.chi_limits[1:])),
            'all original CHI-LIMITS')
        b,o,f=observed.before,observed.old,observed.fission
        require(self.mix==b['fields']['MIX']and self.density==b['fields']['DEN']and self.root_state==b['fields']['ROOT_STATE40'],
            'same final micro operands and actual last LIBMIX state')
        self.mask=b['fields']['MASK'];self.maskl=b['fields']['MASKL']
        self.lsame,self.maskk,self.lall,self.ldiff=(bool(x)for x in o['fields']['LSAME,MASKK,LALL,LDIFF'])
        require(not self.lsame and self.root_state[5]==0 and self.root_state[25]==0 and
            o['dimensions']['NPART']==0,'current complete32/256 neutron route, other branch remains unsupported')
        particle=saved.row(('PARTICLE',))
        if particle is not None:require(particle['kind']==3 and saved.range_bytes(particle,0,1)in(b'N',b' '),'actual neutron particle')
        require(self.maskk==(old_saved is not None)==(pre_saved is not None),'actual oldmacro presence matches observed MASKK')
        self.old_state=self.old_vector(('MACROLIB','STATE-VECTOR'),1,40)if self.maskk else None
        self.nbm0=self.old_state[1]if self.maskk else 0
        self.nfiss0=f['dimensions']['NFISS0'];require(self.nfiss0==o['dimensions']['NFISSI'],'actual NFISS0 matches pre-mutation context')
        require(self.ldiff==(self.old_state[8]==1 if self.maskk else True)and
            self.lall==(8>self.nbm0 if self.maskk else False),'old STATE9/LALL exact Source branch')
        if self.maskk:
            require(self.old_state[0]==370 and 0<self.nbm0<=8 and self.old_state[3]//4==self.nfiss0 and
                (self.old_state[5]==2 or o['dimensions']['ITRANC']<=0),'original old scope/transport conditions')
            self.same_snapshots(pre_saved,old_saved,'ACTUAL_PRE_LIBMIX_VS_PRE_LIBDEN_MACRO')
        self.same_snapshots(post_saved,saved,'ACTUAL_LAST_POST_LIBMIX_VS_FINAL_MICRO_MACRO')
        self.extra_names=[bytes.fromhex(x).decode('ascii')for x in context['original_18_extra_name_bytes_hex']]
        require(len(self.extra_names)==18,'all eighteen declared edits')
        self.model_eligibility=dict(final_micro_constructed_independently=True,all370_groups_and8_mixes_requested=True,
            density_order='original62_no_dedup',model='MODEL_SEPARATE_ROUND32',actual_old_macro_available=self.maskk,
            actual_tracking_MASK_proved=True,actual_branch_proved=True,actual_full_SPHand_compiled_link_proved=False,
            historical_machine_float_replay=False)
        self.nxs,self.timfact=1,0
        times=saved.row(('TIMESPER',))
        require(times is None or not 2<=times['declared_count']<=6,'actual ITSTMP0 forbids Source perturbation')
        self.scalar_presence={};self.scalar_intermediate={};self.overv_fallback_expected=None;self.full_scattering_math_items=0
        self.fission_mapping_validated=False;self.delayed_zero_components_context_known=False;self.diffusion_old_flag=self.ldiff
        self.indfis=array('i',f['fields']['INDFIS_DEFINED_PRE_MUTATION']);self.nfissi=self.nfiss0
        require(len(self.indfis)==8*self.nfiss0 and all(0<=x<=62 for x in self.indfis),'all original defined INDFIS')
        self.validate_old_indfis()
        self.reserved=set()
        for g in range(1,371):
            for name in('NTOT0','NTOT1','DIFF','H-FACTOR','C-FACTOR','OVERV','TRANC',*self.extra_names,
                    'NUSIGF','CHI',*(f'NUSIGF{d:02d}'for d in range(1,7)),*(f'CHI{d:02d}'for d in range(1,7)),
                    *(stem+f'{m:02d}'for m in range(3)for stem in('SCAT','SIGS','SIGW','NJJS','IJJS','IPOS','CHECK')),
                    'FLUX-INTG','FLUX-INTG-P1'):
                self.reserved.add(self.macro_path(g,name))
        self.reserved.update(('MACROLIB',n)for n in('STATE-VECTOR','TIMESTAMP','FISSIONINDEX','LAMBDA-D','ENERGY',
            'SIGNATURE','ADDXSNAME-P0','VOLUME','PARTICLE','PARTICLE-NAM','PARTICLE-NGR','PARTICLE-MC2'))

    def selected(self,mix):return bool(self.mask[mix-1])or not self.maskk
    def group_selected(self,group):return bool(self.maskl[group-1])or self.lall

    def old_vector(self,path,kind,count=None,required=True):
        row=None if self.old_saved is None else self.old_saved.row(path)
        if row is None:
            require(not required,'required original old operand missing '+repr(path));return None
        require(row['kind']==kind and(count is None or row['declared_count']==count)and row['original_word_count']*4<=2**20,
            'original old type/count, no coercion '+repr(path))
        raw=b''.join(self.old_saved.iter_raw(row))
        return raw if kind==3 else make_array(raw,kind==1)

    def old_mix_vector(self,path,required=True):
        v=self.old_vector(path,2,required=required)
        if v is None:return array('I',[0])*8
        require(len(v)<=8,'old vector larger than Source GAF slice')
        return v+array('I',[0])*(8-len(v))

    def compare_raw_sources(self,left,right,path,producer):
        a,b=left.row(path),right.row(path)
        require(a is not None and b is not None and a['kind']==b['kind']and a['declared_count']==b['declared_count']and
            a['original_word_count']==b['original_word_count'],'full snapshot type/count/presence differs '+repr(path))
        count=0
        for raw in left.iter_raw(a):count+=len(raw)
        for raw in right.iter_raw(b):count-=len(raw)
        require(count==0 and a['native_payload_sha256']==b['native_payload_sha256'],'complete original snapshot byte mismatch')
        self.evidence.event('COMPLETE_SNAPSHOT_RECORD_COUPLING',path=list(path),producer=producer,
            left_original=a,right_original=b,all_original_bits_checked=True)

    def same_snapshots(self,left,right,producer):
        require(left is not None and right is not None,'complete original snapshot pair required')
        nleft=nright=0
        for item in left.iter_all():
            row=item['record']
            if row['path'][:1]!=['MACROLIB']or row['path']==['MACROLIB']:continue
            nleft+=1;self.compare_raw_sources(left,right,tuple(row['path']),producer)
        for item in right.iter_all():
            row=item['record']
            if row['path'][:1]!=['MACROLIB']or row['path']==['MACROLIB']:continue
            nright+=1;require(left.row(tuple(row['path']))is not None,'new unexpected original macro record')
        require(nleft==nright,'all macro container/empty/field scope matches')
        def order(source):
            for item in source.iter_all():
                row=item['record']
                if row['path'][:1]==['MACROLIB']and row['path']!=['MACROLIB']:
                    yield row['path'],row['path_types'],row['kind'],row['declared_count']
        for a,b in zip(order(left),order(right)):require(a==b,'full original physical path/key/type/count order')
        self.evidence.event('COMPLETE_SNAPSHOT_ORDER_COUPLING',producer=producer,complete_records=nleft,
            macro_only_XSM_root_labels_no_fake_root_record=True,API_rotation_order_not_normalized=True)

    def inherit(self,path,producer='LIBDEN_ORIGINAL_OLD_RECORD_NOT_WRITTEN'):
        old=None if self.old_saved is None else self.old_saved.row(path)
        actual=self.saved.row(path)
        if old is None:
            if actual is not None and actual['kind']not in(0,10,99):
                self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='no Source write and no actual old value')
            return
        require(actual is not None and old['kind']==actual['kind']and old['declared_count']==actual['declared_count']and
            old['original_word_count']==actual['original_word_count'],'actual inherited presence/type/count changed')
        begin=self.evidence.expected.tell();mismatch=0;total=0
        for raw in self.old_saved.iter_raw(old):
            self.evidence.expected.write(raw);total+=len(raw)
        for raw in self.saved.iter_raw(actual):del raw
        # Full original EOF digests are validated by both iter_raw operations.
        # A differing digest is a genuine complete-record mismatch, never PASS.
        if old['native_payload_sha256']!=actual['native_payload_sha256']:
            mismatch=1;self.evidence.mismatch_elements+=1
            self.evidence.line(self.evidence.mismatches,dict(path=list(path),producer=producer,
                mismatch_unit='complete_original_record_SHA256',old_record=old,actual_record=actual))
        self.evidence.comparisons+=1
        self.evidence.line(self.evidence.fields,dict(path=list(path),producer=producer,actual_original_record=actual,
            expected_original_record=old,expected_pool_begin=begin,expected_pool_end=begin+total,
            outcome='ORIGINAL_OLD_BITS_MATCH'if not mismatch else'ORIGINAL_OLD_BITS_MISMATCH'))
        self.evidence.decision(path,producer,'ORIGINAL_OLD_BITS_MATCH'if not mismatch else'ORIGINAL_OLD_BITS_MISMATCH')

    def validate_old_indfis(self):
        expected=array('i',[0])*(8*self.nfiss0)
        row=None if not self.maskk else self.old_saved.row(('MACROLIB','FISSIONINDEX'))
        if row is not None:
            original=self.old_vector(('MACROLIB','FISSIONINDEX'),1)
            require(len(original)<=8*self.nfiss0,'Source rejects excessive original old FISSIONINDEX')
            if len(original)==8*self.nfiss0:expected=original
            else:
                require(len(original)>=self.nbm0*self.nfiss0,'Source old-index short read would use undefined words')
                for slot in range(self.nfiss0):
                    expected[slot*8:slot*8+self.nbm0]=original[slot*self.nbm0:(slot+1)*self.nbm0]
        require(expected==self.indfis,'actual observed pre-mutation INDFIS from original old map/Source zeros')

    def scalar(self):
        names=('NTOT0','NTOT1','STRD','H-FACTOR','C-FACTOR','OVERV','TRANC')
        accum={n:array('I',[0])*(370*8)for n in names};present={n:False for n in names}
        present['NTOT0']=True;present['TRANC']=self.observed.old['dimensions']['ITRANC']!=0
        for mix in range(1,9):
            if not self.selected(mix):continue
            total=0
            for isotope in range(1,63):
                den=self.density[isotope-1]
                if self.mix[isotope-1]!=mix or not self.fp.nonzero(den):continue
                total=self.fp.add(total,den)
                for suffix in SUFFIXES[:self.nxs]:
                    for name in names:
                        if(name=='STRD'and not self.ldiff)or(name=='TRANC'and not present['TRANC']):continue
                        values=self.micro(isotope,name,suffix=suffix,required=name in('NTOT0','TRANC'))
                        if values is None:continue
                        present[name]=True
                        for g,bits in enumerate(values):
                            k=g*8+mix-1;accum[name][k]=self.fp.add(accum[name][k],self.fp.multiply(bits,den))
                    den=self.fp.multiply(den,self.timfact)
            if present['OVERV']:
                for g in range(370):
                    k=g*8+mix-1
                    if self.fp.nonzero(accum['OVERV'][k]):accum['OVERV'][k]=self.fp.divide(accum['OVERV'][k],total)
        self.scalar_presence=present
        ordinary={n.rstrip(' ')for n in self.extra_names if n[:2]!='NW'and n.rstrip(' ')!='TRANC'and n[:3]not in('BST','CST')and n[:8]!='H-FACTOR'}
        for name in names:
            output='DIFF'if name=='STRD'else name
            if present[name]:self.scalar_intermediate[output]=array('I',[0])*(370*8)
            for g in range(1,371):
                path=self.macro_path(g,output)
                if not present[name]or not self.group_selected(g):
                    if output not in ordinary and not(output=='OVERV'and not present['OVERV']):self.inherit(path)
                    continue
                v=accum[name][(g-1)*8:g*8]
                if self.maskk:
                    old=self.old_mix_vector(path,required=name!='H-FACTOR')
                    for m in range(8):
                        if not self.mask[m]:
                            v[m]=self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,old[m]))if name=='STRD'else old[m]
                if name=='STRD':
                    for m,bits in enumerate(v):
                        if self.fp.nonzero(bits):v[m]=self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,bits))
                self.scalar_intermediate[output][(g-1)*8:g*8]=v
                if output not in ordinary:self.evidence.compare(path,2,v,'LIBDEN_SCALAR_ACTUAL_CONTEXT_'+name,self.model_eligibility)
        if not present['OVERV']:
            energy=self.vector(('ENERGY',),2,371)
            if not self.fp.nonzero(energy[-1]):energy[-1]=self.fp.f64_to32(1e-5)
            sqfmas=math.sqrt(2.0e4*1.60217653e-19/1.67492728e-27);expected=array('I',[0])*(370*8)
            for g in range(370):
                average=self.fp.sqrt(self.fp.multiply(energy[g],energy[g+1]));root=self.fp.sqrt(average)
                value=struct.unpack('<f',struct.pack('<I',root))[0]
                require(value!=0,'actual OVERV fallback nonzero energy')
                for m in range(8):expected[g*8+m]=self.fp.f64_to32(1.0/(value*sqfmas))
            self.overv_fallback_expected=expected
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',
                original_all370x8_words_compared=True,historical_machine_bit_replay=False)

    def extras(self):
        for ordinal,name in enumerate(self.extra_names,1):
            out=name.rstrip(' ')
            if name[:2]=='NW'or out=='TRANC'or name[:3]in('BST','CST')or name[:8]=='H-FACTOR':
                self.evidence.event('DECLARED_EXTRA_SPECIAL_PRODUCER',declared_ordinal=ordinal,full_name_hex=name.encode('ascii').hex())
                if name[:2]!='NW'and out not in('TRANC','H-FACTOR'):
                    for g in range(1,371):self.inherit(self.macro_path(g,out))
                continue
            values=array('I',[0])*(370*8);exists=False
            for mix in range(1,9):
                if not self.selected(mix):continue
                for isotope in range(1,63):
                    den=self.density[isotope-1]
                    if self.mix[isotope-1]!=mix or not self.fp.nonzero(den):continue
                    for suffix in SUFFIXES[:self.nxs]:
                        v=self.micro(isotope,name,suffix=suffix,required=False)
                        if v is None:
                            self.evidence.event('ACTUAL_CONTEXT_EXTRA_GOTO720',isotope=isotope,ordinal=ordinal,suffix=suffix);break
                        exists=True
                        for g,bits in enumerate(v):
                            k=g*8+mix-1;values[k]=self.fp.add(values[k],self.fp.multiply(bits,den))
                        den=self.fp.multiply(den,self.timfact)
            for g in range(1,371):
                path=self.macro_path(g,out)
                if out=='OVERV'and not self.scalar_presence.get('OVERV',False):continue
                if not self.group_selected(g):self.inherit(path);continue
                old=self.old_vector(path,2,required=False)if self.maskk else None
                if old is not None:exists=True
                if not exists:
                    if out in self.scalar_intermediate:
                        self.evidence.compare(path,2,self.scalar_intermediate[out][(g-1)*8:g*8],
                            'LIBDEN_SCALAR_RETAINED_EXTRA_EXIST_FALSE',self.model_eligibility)
                    else:self.inherit(path)
                    continue
                current=values[(g-1)*8:g*8]
                inherited=self.old_mix_vector(path,False)
                for m in range(8):
                    if self.maskk and not self.mask[m]:current[m]=inherited[m]
                self.evidence.compare(path,2,current,'LIBDEN_EXTRA_'+str(ordinal)+'_ACTUAL_EXIST_ORDER',self.model_eligibility)

    def scattering(self):
        for moment in range(3):
            cm=f'{moment:02d}';check=array('I',[0])*(370*8)
            for start in range(0,370,50):
                width=min(50,370-start);gaf=array('I',[0])*(8*370*width);sigs=array('I',[0])*(8*width)
                for isotope in range(1,63):
                    den=self.density[isotope-1];mix=self.mix[isotope-1]-1
                    if not self.fp.nonzero(den):continue
                    fact=0x3f800000
                    for suffix in SUFFIXES[:self.nxs]:
                        sigma=self.micro(isotope,'SIGS'+cm,suffix=suffix,required=False)
                        if sigma is not None:
                            njj=self.micro(isotope,'NJJS'+cm,1,suffix=suffix);ijj=self.micro(isotope,'IJJS'+cm,1,suffix=suffix)
                            require(all(0<=n<=370 and(n==0 or n<=j<=370)for n,j in zip(njj,ijj)),'complete micro sparse bounds')
                            scat=self.micro(isotope,'SCAT'+cm,count=sum(njj),suffix=suffix)
                            cursor=sum(njj[:start])
                            for block in range(width):
                                dest=start+block
                                if self.selected(mix+1):sigs[block*8+mix]=self.fp.add(sigs[block*8+mix],self.fp.multiply(sigma[dest],den))
                                for src in range(ijj[dest]-1,ijj[dest]-njj[dest]-1,-1):
                                    if self.selected(mix+1):
                                        k=(block*8+mix)*370+src
                                        gaf[k]=self.fp.add(gaf[k],self.fp.multiply(self.fp.multiply(scat[cursor],den),fact))
                                    cursor+=1
                            require(cursor==sum(njj[:start+width]),'all sparse micro words consumed in source order')
                        fact=self.fp.multiply(fact,self.timfact)
                for block in range(width):
                    dest=start+block;g=dest+1;path=self.macro_path(g,'SIGS'+cm)
                    if self.group_selected(g):
                        v=sigs[block*8:(block+1)*8]
                        if self.maskk:
                            old=self.old_mix_vector(path,required=moment==0)
                            for m in range(8):
                                if not self.mask[m]:v[m]=old[m]
                        self.evidence.compare(path,2,v,'LIBDEN_SIGS_ACTUAL_MASK_INHERIT',self.model_eligibility)
                    else:self.inherit(path)
                    # Source LOGL is evaluated on new GAF before restoring old SCAT.
                    logl=self.group_selected(g)or any(self.maskl[src]and self.fp.nonzero(gaf[(block*8+m)*370+src])
                        for m in range(8)for src in range(370))
                    names=('SCAT'+cm,'NJJS'+cm,'IJJS'+cm,'IPOS'+cm,'SIGW'+cm)
                    if logl and self.maskk:
                        old=self.old_vector(self.macro_path(g,'SCAT'+cm),2,required=moment==0)
                        if old is not None:
                            nj=self.old_vector(self.macro_path(g,'NJJS'+cm),1);ij=self.old_vector(self.macro_path(g,'IJJS'+cm),1)
                            pos=self.old_vector(self.macro_path(g,'IPOS'+cm),1)
                            require(len(nj)==len(ij)==len(pos)<=8,'complete original old scatter layout')
                            for m in range(8):
                                if self.mask[m]or m>=len(pos)or pos[m]==-99:continue
                                require(0<=nj[m]<=370 and(nj[m]==0 or nj[m]<=ij[m]<=370)and
                                    1<=pos[m]and pos[m]-1+nj[m]<=len(old),'complete old sparse span')
                                for j,src in enumerate(range(ij[m]-1,ij[m]-nj[m]-1,-1)):
                                    gaf[(block*8+m)*370+src]=old[pos[m]-1+j]
                    output=array('I');nj=array('i');ij=array('i');pos=array('i');sigw=array('I');digest=hashlib.sha256()
                    for m in range(8):
                        domain=gaf[(block*8+m)*370:(block*8+m+1)*370];digest.update(bytes_array(domain))
                        self.full_scattering_math_items+=370
                        if not logl:continue
                        active=[i for i,b in enumerate(domain)if self.fp.nonzero(b)];lo=min([dest,*active]);hi=max([dest,*active])
                        pos.append(len(output)+1);nj.append(hi-lo+1);ij.append(hi+1)
                        for src in range(hi,lo-1,-1):
                            output.append(domain[src]);k=src*8+m;check[k]=self.fp.add(check[k],domain[src])
                        sigw.append(domain[dest])
                    self.evidence.event('FULL_ACTUAL_CONTEXT_SCATTER_DOMAIN',moment=moment,destination_one_based=g,
                        all8x370_domain_SHA256=digest.hexdigest(),Source_LOGL=logl,old_inheritance_applied_after_LOGL=True)
                    if logl:
                        for name,kind,v in zip(names,(2,1,1,1,2),(output,nj,ij,pos,sigw)):
                            self.evidence.compare(self.macro_path(g,name),kind,v,'LIBDEN_SCAT_ACTUAL_LOGL_OLD_MASK',self.model_eligibility)
                    else:
                        for name in names:self.inherit(self.macro_path(g,name))
                del gaf,sigs
            for g in range(1,371):
                path=self.macro_path(g,'CHECK'+cm)
                if self.group_selected(g):self.evidence.compare(path,2,check[(g-1)*8:g*8],'LIBDEN_CHECK_ACTUAL_DESTINATION_WRITE_ORDER',self.model_eligibility)
                else:self.inherit(path)
        require(self.full_scattering_math_items==370*370*8*3,'full original scatter mathematical scope')

    def fission(self):
        # Reconstruct every original allocation step, including zero-density isotopes.
        for isotope in range(1,63):
            mix=self.mix[isotope-1]-1
            if not self.selected(mix+1):continue
            nuf=self.saved.row(self.micro_path(isotope,'NUSIGF'));chi=self.saved.row(self.micro_path(isotope,'CHI--01'))
            if nuf is None or chi is None or nuf['declared_count']<=0 or chi['declared_count']<=0:continue
            values=self.micro(isotope,'CHI--01')
            if not any(self.fp.ratio(x)[0]>0 for x in values):continue
            chosen=next((s for s in range(self.nfissi)if self.indfis[s*8+mix]in(0,isotope)),None)
            if chosen is None:
                chosen=self.nfissi;self.nfissi+=1;require(self.nfissi<=self.observed.old['dimensions']['MAXNFI'],'actual Source MAXNFI')
                self.indfis.extend([0]*8)
            self.indfis[chosen*8+mix]=isotope
            self.evidence.event('ACTUAL_OLD_CONTEXT_FISSION_SLOT_ALLOCATION',isotope=isotope,mix=mix+1,slot=chosen+1,
                actual_density_bits=int(self.density[isotope-1]),density_zero_not_filtered=True)
        require(self.nfissi==8,'complete original32 components/64 index scope, no reduced target')
        self.evidence.compare(('MACROLIB','FISSIONINDEX'),1,self.indfis,'LIBDEN_ORIGINAL_OLD64_SLOT_ALLOCATION',self.model_eligibility)
        self.fission_mapping_validated=True
        for delayed in range(7):
            nn='NUSIGF'if delayed==0 else f'NUSIGF{delayed:02d}';cn='CHI'if delayed==0 else f'CHI{delayed:02d}'
            for g in range(1,371):
                if not self.group_selected(g):self.inherit(self.macro_path(g,nn));self.inherit(self.macro_path(g,cn));continue
                nus=array('I',[0])*256;chis=array('I',[0])*256;known=array('B',[0])*256
                if self.nfiss0>0:
                    # LIBDEN465 explicitly initializes the WHOLE MAXNFI*NESP
                    # slice before copying old components, including new slots.
                    known=array('B',[3])*256
                    oldn=self.old_vector(self.macro_path(g,nn),2,required=delayed==0)
                    oldc=self.old_vector(self.macro_path(g,cn),2,required=delayed==0 or oldn is not None)
                    if oldn is not None:
                        require(oldc is not None and len(oldn)==len(oldc)==self.nbm0*self.nfiss0*4,'complete old fission component count')
                        for c in range(self.nfiss0*4):
                            nus[c*8:c*8+self.nbm0]=oldn[c*self.nbm0:(c+1)*self.nbm0]
                            chis[c*8:c*8+self.nbm0]=oldc[c*self.nbm0:(c+1)*self.nbm0]
                for spectrum in range(4):
                    for slot in range(8):
                        for mix in range(8):
                            isotope=self.indfis[slot*8+mix];k=(slot*4+spectrum)*8+mix
                            if slot+1>self.nfiss0*4 or(isotope and self.selected(mix+1)):
                                nus[k]=chis[k]=0;known[k]=3
                            if not isotope or not self.selected(mix+1):continue
                            den=self.density[isotope-1]
                            for ix,suffix in enumerate(SUFFIXES[:self.nxs]):
                                if delayed and spectrum==0:
                                    last=self.saved.row(self.micro_path(isotope,'NUSIGF06',suffix))
                                    values=None if last is None or last['declared_count']<=0 else self.micro(isotope,nn,suffix=suffix)
                                    lastchi=self.saved.row(self.micro_path(isotope,'CHI06',suffix))
                                    cv=None if ix or lastchi is None or lastchi['declared_count']<=0 else self.micro(isotope,cn,suffix=suffix)
                                elif delayed:values=cv=None
                                else:
                                    values=self.micro(isotope,'NUSIGF',suffix=suffix)
                                    crow=self.saved.row(self.micro_path(isotope,f'CHI--{spectrum+1:02d}',suffix))
                                    cv=self.micro(isotope,f'CHI--{spectrum+1:02d}',suffix=suffix)if ix==0 and crow is not None and crow['declared_count']==370 else None
                                if values is not None and(delayed or self.chi_limits[spectrum]<g<=self.chi_limits[spectrum+1]):
                                    if known[k]&1:nus[k]=self.fp.add(nus[k],self.fp.multiply(values[g-1],den))
                                if cv is not None:chis[k]=cv[g-1];known[k]|=2
                                den=self.fp.multiply(den,self.timfact)
                for name,v,bit in((nn,nus,1),(cn,chis,2)):
                    path=self.macro_path(g,name)
                    if all(k&bit for k in known):self.evidence.compare(path,2,v,'LIBDEN_OLD_INIT_PROMPT_ALL6_DELAYED256',self.model_eligibility)
                    else:
                        actual=self.vector(path,2,256)
                        self.evidence.compare_known_components(path,actual,v,known,bit,self.model_eligibility,'LIBDEN_OLD_INIT_UNDEFINED_COMPONENTS')
                        self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='original Source initialization does not define every component')
        self.lambdas()

    def lambdas(self):
        expected=array('I',[0])*48;known=array('B',[0])*48
        if self.nfiss0>0:
            old=self.old_vector(('MACROLIB','LAMBDA-D'),2,required=False)
            if old is None:known[:6]=array('B',[1])*6
            else:
                require(len(old)<=48,'old Lambda Source extent')
                expected[:len(old)]=old;known[:len(old)]=array('B',[1])*len(old)
        for slot in range(self.nfiss0,8):known[slot*6:(slot+1)*6]=array('B',[1])*6
        for slot in range(8):
            for mix in range(8):
                isotope=self.indfis[slot*8+mix]
                if not isotope or not self.selected(mix+1):continue
                v=self.micro(isotope,'LAMBDA-D',count=6,required=False)
                if v is not None:
                    expected[slot*6:(slot+1)*6]=v;known[slot*6:(slot+1)*6]=array('B',[1])*6
                    self.evidence.event('LAMBDA_ACTUAL_CONTEXT_LAST_WRITE',slot=slot+1,mix=mix+1,isotope=isotope)
        path=('MACROLIB','LAMBDA-D')
        if all(known):self.evidence.compare(path,2,expected,'LIBDEN_LAMBDA48_ACTUAL_OLD_INITIALIZATION_LAST_WRITE',self.model_eligibility)
        else:
            self.evidence.compare_known_components(path,self.vector(path,2,48),expected,known,1,self.model_eligibility,'LIBDEN_LAMBDA_UNDEFINED_OLD_SLOTS')
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='Source initializes only missing old Lambda slot1; other old slots undefined')

    def metadata(self):
        for name in('ADDXSNAME-P0','PARTICLE-NGR','PARTICLE-MC2'):
            row=self.saved.row((name,))
            if row is None:continue
            self.evidence.compare(('MACROLIB',name),row['kind'],b''.join(self.saved.iter_raw(row)),
                'LIBDEN_DIRECT_COPY_ACTUAL_CONTEXT_'+name,self.model_eligibility)
        for name in('PARTICLE','PARTICLE-NAM'):
            if self.saved.row((name,))is not None:
                self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field=name,reason='LCMPTC one-character machine padding requires compiled control; no raw-copy substitution')
        energy=self.vector(('ENERGY',),2,371)
        if not self.fp.nonzero(energy[-1]):energy[-1]=self.fp.f64_to32(1e-5)
        if self.maskk:
            self.inherit(('MACROLIB','ENERGY'));self.inherit(('MACROLIB','SIGNATURE'))
            state=array('i',self.old_state);state[1]=max(self.nbm0,8);state[2]=max(state[2],3);state[3]=32;state[4]=max(state[4],18)
        else:
            state=array('i',[0])*40;state[:5]=array('i',[370,8,3,32,18])
            self.evidence.compare(('MACROLIB','ENERGY'),2,energy,'LIBDEN_FRESH_ONLY_ENERGY',self.model_eligibility)
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='SIGNATURE',reason='fresh LCMPTC twelve-character Source-machine padding not runtime qualified')
        itranc=self.observed.old['dimensions']['ITRANC'];state[5]=2 if itranc else 0;state[6]=6;state[7]=0
        state[8]=int(self.scalar_presence.get('STRD',False));state[9]=int(self.scalar_presence.get('NTOT1',False));state[10:]=array('i',[0])*30
        if self.old_saved is not None and self.old_saved.row(('MACROLIB','SPH'))is not None:state[13]=1
        self.evidence.compare(('MACROLIB','STATE-VECTOR'),1,state,'LIBDEN_OLD_STATE40_MAXIMA_ACTUAL_FLAGS',self.model_eligibility)
        before=self.observed.before['fields']['TMPDAY'];actual=self.observed.old['fields']['TMPDAY'];expected=array('I',before)
        if self.maskk:
            timestamp=self.old_vector(('MACROLIB','TIMESTAMP'),2,required=False)
            if timestamp is not None and 0<len(timestamp)<=3:
                if len(timestamp)!=3:
                    self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='TIMESTAMP',reason='LCMGET short old timestamp leaves uninitialized OLDTIM tail')
                else:expected=timestamp
        require(expected==actual,'LIBMIX actual old timestamp overwrite, no final self proof')
        self.evidence.compare(('MACROLIB','TIMESTAMP'),2,actual,'LIBMIX_OLD_TIMESTAMP_LIBDEN_WRITE',self.model_eligibility)
        volumes=self.vector(('ISOTOPESVOL',),2,62,required=False)
        if volumes is not None:
            v=array('I',[0])*8
            for i in range(62):v[self.mix[i]-1]=volumes[i]
            self.evidence.compare(('MIXTURESVOL',),2,v,'LIBDEN_LAST_ISOTOPE_VOLUME',self.model_eligibility)
        else:
            v=self.observed.before['fields'].get('ROOT_MIXTURESVOL_BEFORE')
            if v is not None:self.evidence.compare(('MIXTURESVOL',),2,v,'LIBDEN_ACTUAL_PRECALL_ROOT_VOLUME_UNCHANGED',self.model_eligibility)
        if v is not None:
            self.evidence.compare(('MACROLIB','VOLUME'),2,v,'LIBDEN_VOLUME_COPY_ACTUAL_CONTEXT',self.model_eligibility)
            for name,out in(('NWT0','FLUX-INTG'),('NWT1','FLUX-INTG-P1')):
                flux=array('I',[0])*(370*8);any_present=False
                for isotope in range(1,63):
                    row=self.saved.row(self.micro_path(isotope,name))
                    if row is None or row['declared_count']!=370:
                        self.evidence.event('FULL_ORIGINAL_FLUX_PRESENCE_COUNT',isotope=isotope,name=name,original=row);continue
                    values=self.micro(isotope,name);any_present=True;mix=self.mix[isotope-1]-1
                    for g,bits in enumerate(values):flux[g*8+mix]=self.fp.multiply(bits,v[mix])
                    self.evidence.event('FULL_ACTUAL_FLUX_LAST_WRITE',isotope=isotope,mix=mix+1,field=name,density_not_used=True)
                for g in range(1,371):
                    path=self.macro_path(g,out)
                    if any_present:self.evidence.compare(path,2,flux[(g-1)*8:g*8],'LIBDEN_FLUX_LAST_WRITE_ALL_GROUPS',self.model_eligibility)
                    else:self.inherit(path)
        else:
            self.inherit(('MACROLIB','VOLUME'))
            for g in range(1,371):
                for out in('FLUX-INTG','FLUX-INTG-P1'):self.inherit(self.macro_path(g,out))
        # Every genuinely unmodified old field is compared from OLD, including
        # full SPH words. Potential producers reserved above are never silently
        # inherited after a phase error or an unsupported computation.
        if self.maskk:
            for item in self.old_saved.iter_all():
                row=item['record'];path=tuple(row['path'])
                if path[:1]==('MACROLIB',)and row['kind']not in(0,10,99)and path not in self.reserved:self.inherit(path)
        self.evidence.event('COMPLETE_CONTEXT_MODEL_BOUNDARY',all_original_scope_retained=True,
            historical_LIBDEN_machine_float_replay=False,compiled_Source_binary_link_qualified=False,
            actual_old_macro_input=self.maskk,actual_STATE9=self.ldiff,actual_tracking_MASK_proved=True,
            SPH_one_never_assumed=True,actual_complete_SPH_selection= self.observed.complete_sph_call_selection_proved)

"""Root-only context aggregation entry, insertion-only Source fragment."""
def context_state_check(adapter,binding,state,output,budget):
    source=binding['states'][state];root=output/state;root.mkdir();temp=root/'sqlite_file_temp';temp.mkdir()
    saved=adapter.SavedNativeInput(source['sqlite_pin'],source['native_pool_pin'],temp,budget)
    opened=[];evidence=None;state_report=None
    try:
        evidence=DiskEvidence(root,saved,budget,state);evidence.inventory()
        context=adapter.capture_complete_fixed_context(saved);write_new(root/'ACTUAL_COMPLETE_FIXED_CONTEXT.json',context)
        actual=binding['actual_context_states'][state]
        require(type(actual)is dict and set(actual)=={'complete_context_pins','all_snapshot_pairs','actual_extraction_report_pin',
            'actual_observation_manifest_pin','selected_last_libmix_number','actual_extraction_coverage_contract_pin'},
            'full actual context contract, no final-state substituted history')
        for key in('actual_extraction_report_pin','actual_observation_manifest_pin','actual_extraction_coverage_contract_pin'):
            check_pin(actual[key],budget)
        observed=ObservedContext(actual['complete_context_pins'],budget,evidence)
        require(type(actual['selected_last_libmix_number'])is int and
            actual['selected_last_libmix_number']==observed.before['libmix'],'actual final completed call, no arbitrary selection')
        # Protect every saved old/post/final snapshot, not just the last call.
        # Root coverage META supplies same exact all-snapshot list as the
        # genuine closed extraction; it cannot be a Source-only assertion.
        cov=strict_json(Path(actual['actual_extraction_coverage_contract_pin']['path']).read_bytes())
        require(cov['schema']=='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1'and
            cov['all_original_snapshot_pairs_saved']is True and cov['actual_extraction_report_pin']==actual['actual_extraction_report_pin']and
            cov['actual_observation_manifest_pin']==actual['actual_observation_manifest_pin']and
            cov['states'][state]['all_snapshot_pairs']==actual['all_snapshot_pairs']and
            cov['states'][state]['complete_context_pins']==actual['complete_context_pins']and
            cov['actual_closed_extraction_receipt_independently_reviewed']is True and cov['new_qualification_sha256']is None,
            'same genuine complete saved snapshot/context coverage, no raw Q transplant')
        report=strict_json(Path(actual['actual_extraction_report_pin']['path']).read_bytes())
        require(report['schema']=='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'and
            report['all_complete_state_scope_retained']is True,'actual complete Root extraction report')
        expected=report['states'][state];pairs=actual['all_snapshot_pairs']
        require(type(pairs)is list and len(pairs)==len(expected),'all genuine snapshot pairs retained')
        selected={};previous=0
        for pair,record in zip(pairs,expected):
            require(set(pair)=={'event','role','root_prefix','input_pin','sqlite_pin','native_pool_pin'}and
                type(pair['event'])is int and pair['event']>=previous and
                all(pair[k]==record[k]for k in('event','role','root_prefix','input_pin'))and
                pair['sqlite_pin']==record['paired_SQLite_pin']and pair['native_pool_pin']==record['paired_original_pool_pin'],
                'every original complete pair exactly bound to genuine report, no sorting or replacement')
            previous=pair['event']
            for k in('input_pin','sqlite_pin','native_pool_pin'):check_pin(pair[k],budget)
            extract=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget)
            try:
                n=0
                for item in extract.iter_all():
                    for raw in extract.iter_raw(item['record']):del raw
                    n+=1;evidence.event('FULL_ORIGINAL_OBSERVED_SNAPSHOT_RECORD',event=pair['event'],role=pair['role'],original=item)
                require(n==record['complete_records'],'complete actual snapshot EOF count')
            finally:extract.close()
            key=(pair['event'],pair['role'])
            require(key not in selected,'duplicate genuine original snapshot')
            # Keep only small Source pins, never an in-memory whole path tree.
            selected[key]=pair
        final_pair=selected.get((observed.events[-1]['event'],'final-complete-micro'))
        require(final_pair is not None and final_pair['sqlite_pin']==source['sqlite_pin']and
            final_pair['native_pool_pin']==source['native_pool_pin'],
            'same genuinely observed final full micro used for all62 operands, no unrelated V23 pool substitution')
        def open_pair(event,role,required=True):
            pair=selected.get((event,role))
            require(pair is not None or not required,'actual necessary snapshot missing '+role)
            if pair is None:return None
            item=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget);opened.append(item);return item
        maskk=bool(observed.old['fields']['LSAME,MASKK,LALL,LDIFF'][1])
        old=open_pair(observed.old['event'],'oldmacro-LIBDEN',maskk)
        pre=open_pair(observed.before['event'],'oldmacro-pre-LIBMIX',maskk)
        post=open_pair(observed.after['event'],'postmacro-LIBMIX')
        model=ContextAwareConstruction(saved,evidence,context,binding['Source_route'],observed,old,pre,post)
        for phase in('scattering','scalar','fission','extras','overv_fallback','metadata'):
            try:getattr(model,phase)();evidence.phase_results.append(dict(phase=phase,computation_finished=True))
            except Exception as error:
                evidence.event('PHASE_FAILED',phase=phase,error=repr(error),complete_original_scope_retained=True)
                evidence.phase_results.append(dict(phase=phase,computation_finished=False,error=repr(error)))
        unknown=evidence.complete_decisions()
        state_report=dict(state=state,all_original_records=evidence.records,complete_MACROLIB_records=evidence.macro_records,
            original_scope=[370,8,3,32,64,62,18,6,48],complete_source_field_comparisons=evidence.comparisons,
            compared_known_elements=evidence.compared_elements,all_mismatching_elements=evidence.mismatch_elements,
            all_context_or_operand_issues=evidence.issues,unknown_macro_producers=unknown,phase_results=evidence.phase_results,
            all_original_native_records_and_bytes_preserved=True,all_complete_orders_preserved=True,
            all_missing_fields_not_zero_filled=True,expected_binary32_model='MODEL_SEPARATE_ROUND32',
            binary32_model_operations=model.fp.operations,binary32_model_underflow_to_zero=model.fp.underflow_to_zero,
            binary32_model_overflow_to_infinity=model.fp.overflow_to_infinity,
            mathematical_scattering_domain_computed=model.full_scattering_math_items,expected_full_scattering_domain=370*370*8*3,
            actual64_isotope_mix_mapping_checked=model.fission_mapping_validated,
            actual_old_MACROLIB_snapshots_used=maskk,actual_STATE9_initialization_checked=True,actual_NFISS0_INDFIS_checked=True,
            actual_MAT_MASK_derivation_checked=True,actual_complete_SPH_branch_selection_checked=observed.complete_sph_call_selection_proved,
            original_context_event_count=len(actual['complete_context_pins']),all_original_snapshot_count=len(pairs),
            complete_final_construction_qualified=False,historical_old_macro_proved=False,
            historical_actual_tracking_MASK_proved=False,historical_SPHand_compiled_arithmetic_proved=False,
            instrumented_actual_context_is_not_recovered_original_history=True,
            known_component_matching_does_not_qualify_unknown_delayed_or_inherited_fields=True,
            full_output_scope_retained_even_on_failure=True,**FALSE)
    except Exception as error:
        if evidence is not None:
            evidence.event('PHASE_FAILED',phase='context_admission_or_initialization',error=repr(error),complete_original_scope_retained=True)
            unknown=evidence.complete_decisions()
            state_report=dict(state=state,all_original_records=evidence.records,complete_MACROLIB_records=evidence.macro_records,
                original_scope=[370,8,3,32,64,62,18,6,48],error=repr(error),unknown_macro_producers=unknown,
                all_context_or_operand_issues=evidence.issues,all_mismatching_elements=evidence.mismatch_elements,
                all_original_native_records_and_bytes_preserved=True,complete_final_construction_qualified=False,
                full_output_scope_retained_even_on_failure=True,all_missing_fields_not_zero_filled=True,**FALSE)
        else:raise
    finally:
        for item in reversed(opened):item.close()
        if evidence is not None:evidence.close()
        saved.close()
    require(state_report is not None,'no fabricated state result')
    state_report['complete_output_file_pins']=[full_pin(p,budget)for p in sorted(root.rglob('*'))if p.is_file()]
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
    require(binding['schema']=='ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_MICRO_MACRO_BINDING_V2'
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
            states.append(context_state_check(adapter,binding,state,output,budget))
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
        historical_context_missing_is_not_silently_supplied=True,genuine_supervisor_watch_verified_here=False, **FALSE)
    report_path=output/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
    write_new(report_path,report)
    print(json.dumps(dict(status=report['status'],report=full_pin(report_path,lambda:None)),
        allow_nan=False),flush=True)
    # This complete source candidate has known unresolved historical/context
    # producers. Matching supported fields cannot yield a fabricated EXIT0 Q.
    raise SystemExit(2 if error is None else 1)


if __name__=='__main__':main()

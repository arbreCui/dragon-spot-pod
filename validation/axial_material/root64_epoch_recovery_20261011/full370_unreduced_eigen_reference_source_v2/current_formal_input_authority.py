"""Concrete current-file/array binding, without a true-returning callback.

This is a declared terminal-MACROLIB mathematical input route, not a nuclear
data qualification. Missing current context production is an explicit required
operation. A saved report label cannot stand in for raw records or call history.
"""
from pathlib import Path
from dataclasses import asdict
import hashlib
import json
import os
import re
import stat
import numpy as np
from snapshot_control_preflight import _open_xsm
from terminal_AB_and_current_track_inputs import (
    terminal_material_from_snapshot, native_track_inventory, array)
from native_full_angular_p2 import angular_states_from_native
from full370_unreduced_eigen import (Controls, ReferenceFailure,
    ReferenceUnready, FORMAL_CASE_SHA, NR, NZ, NG, NF, NMOM)

CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
            fresh_bytes=2*2**30, history_bytes=96*2**30,
            cold_reserve_bytes=20971764748, metadata_reserve_bytes=64*2**20,
            free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ReferenceFailure('duplicate authority key '+key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda value:
        (_ for _ in ()).throw(ReferenceFailure('nonfinite authority '+value)))


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path, budget=None):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ReferenceFailure('literal absolute authority path')
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ReferenceFailure('authority path alias '+str(item))
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ReferenceFailure('regular single-link authority input '+str(path))
    digest = hashlib.sha256(); count = 0
    with path.open('rb') as stream:
        if identity(os.fstat(stream.fileno())) != identity(before):
            raise ReferenceFailure('opened authority identity')
        while True:
            if budget is not None:
                budget.check()
            raw = stream.read(2**20)
            if not raw:
                break
            count += len(raw); digest.update(raw)
        if identity(os.fstat(stream.fileno())) != identity(before):
            raise ReferenceFailure('fullEOF authority identity')
    if count != before.st_size or identity(path.lstat()) != identity(before):
        raise ReferenceFailure('authority changed during whole-file read')
    return dict(path=str(path), sha256=digest.hexdigest(),
                size_bytes=count, identity=identity(before))


def recheck(expected, budget=None):
    if (type(expected) is not dict or set(expected) !=
            {'path','sha256','size_bytes','identity'} or
            type(expected['sha256']) is not str or
            re.fullmatch('[0-9a-f]{64}', expected['sha256']) is None or
            type(expected['size_bytes']) is not int or
            type(expected['identity']) is not list or len(expected['identity']) != 7 or
            any(type(value) is not int for value in expected['identity'])):
        raise ReferenceFailure('exact typed complete authority pin')
    if pin(expected['path'], budget) != expected:
        raise ReferenceFailure('authority fullEOF/SHA/7ID changed '+expected['path'])
    return expected


def read(expected, budget=None):
    recheck(expected, budget)
    result = strict_json(Path(expected['path']).read_bytes())
    recheck(expected, budget)
    return result


def array_digest(value):
    value = np.asarray(value)
    if value.dtype.hasobject:
        raise ReferenceFailure('object arrays cannot bind numerical input')
    return dict(shape=list(value.shape), dtype=value.dtype.str,
                sha256=hashlib.sha256(value.tobytes(order='C')).hexdigest())


def complete_value_digest(value):
    """Stream all typed ray metadata into one hash without a second ray tree."""
    digest=hashlib.sha256()
    def emit(tag,payload=b''):
        digest.update(str(len(tag)).encode()+b':'+tag+
                      str(len(payload)).encode()+b':'+payload)
    def walk(item):
        if isinstance(item,np.ndarray):
            emit(b'ndarray',json.dumps(array_digest(item),sort_keys=True).encode())
        elif type(item)is dict:
            if not all(type(key)is str for key in item):
                raise ReferenceFailure('typed original ray metadata keys')
            emit(b'dict',str(len(item)).encode())
            for key in sorted(item):emit(b'key',key.encode());walk(item[key])
        elif type(item)in(list,tuple):
            emit(type(item).__name__.encode(),str(len(item)).encode())
            for child in item:walk(child)
        elif type(item)is bytes:
            emit(b'bytes',str(len(item)).encode()+b':'+hashlib.sha256(item).digest())
        elif item is None:
            emit(b'NoneType')
        elif type(item)is str:
            emit(b'str',item.encode())
        elif type(item)in(int,float,bool)or isinstance(item,np.generic):
            emit(b'scalar',json.dumps(array_digest(item),sort_keys=True).encode())
        else:
            raise ReferenceFailure('unsupported original ray metadata type')
    walk(value)
    return dict(kind='complete_typed_tree',sha256=digest.hexdigest())


def complete_states_digest(states):
    fields=('keys','directions','streaming_directions','harmonics','xmu','zmu',
            'wzmu','native_in_plane','azimuth_count')
    return {key:complete_value_digest(getattr(states,key)) for key in fields}


def complete_model_digest(model):
    fields=('material_ids','scatter64','nusigf64','chi64','total64','volume64',
            'stored_surface64','tranc64','formal_SN32_U','formal_SN32_W','formal_SN32_PL')
    return dict(arrays={key:array_digest(model[key]) for key in fields},
                events=complete_value_digest(model['events64']),
                rays=complete_value_digest(model['rays']),
                states=complete_states_digest(model['states']))


def actual_success_report(expected, budget=None):
    report = read(expected, budget)
    if report.get('failure') is not None or report.get('after_check_error') is not None:
        raise ReferenceUnready('actual owning host failed, no inherited admission')
    records = report.get('records')
    if type(records) is not list or not records:
        raise ReferenceUnready('actual nonempty owning records')
    for record in records:
        if record['status'] != 'PASS':
            raise ReferenceUnready('this component requires actual successful stages')
        watch_path = Path(expected['path']).parent/(record['label']+'.watchdog.json')
        wanted_watch = next((row for row in report.get('actual_watchdog_checks',[])
                             if row['path'] == str(watch_path)), None)
        if wanted_watch is None or pin(watch_path,budget)['sha256'] != wanted_watch['sha256']:
            raise ReferenceUnready('actual summary must bind the exact watchdog bytes')
        watch = strict_json(watch_path.read_bytes())
        if (type(watch['returncode']) is not int or watch['returncode'] != 0 or
            watch['limit_failure'] is not None or watch['command'] != record['command'] or
            watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or
            not 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= 600 or
            watch['rss_cap_mib'] != 512 or not 0 <= watch['sampled_peak_rss_mib'] < 512):
            raise ReferenceUnready('actual successful component watchdog differs')
    return report


class KernelBinding:
    """Concrete compiled-library origin; future actual pins are passed explicitly.

    The manifest must come from the actual compiling host, not this Source.
    Binding compilation is not claiming new H150/48/370 kernel controls passed.
    The separate current controls report is required by FormalBinding below.
    """
    def __init__(self, origin_pin, budget):
        self.origin_pin = origin_pin; self.budget = budget
        origin = read(origin_pin, budget)
        if origin['schema'] != 'ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN_V1':
            raise ReferenceUnready('explicit actual current kernel build origin')
        self.library_pin = origin['library_pin']
        self.source_pins = origin['complete_source_pins']
        self.report_pin = origin['actual_build_report_pin']
        if (type(self.source_pins) is not list or not self.source_pins or
            len({p['path'] for p in self.source_pins}) != len(self.source_pins) or
            origin['original_caps'] != CAPS):
            raise ReferenceUnready('complete unique kernel origins/original caps')
        actual = actual_success_report(self.report_pin, budget)
        if origin['actual_command'] not in [row['command'] for row in actual['records']]:
            raise ReferenceUnready('compiler command is absent from actual records')
        for item in self.source_pins:
            recheck(item, budget)
        own_source = Path(__file__).with_name('current_full370_white_accumulate.cpp')
        if pin(own_source, budget) not in self.source_pins:
            raise ReferenceUnready('current complete accumulator Source origin')
        self.verify(self.library_pin['path'])

    def verify(self, library):
        if str(Path(library)) != self.library_pin['path']:
            raise ReferenceFailure('library differs from actual origin')
        recheck(self.origin_pin, self.budget); recheck(self.report_pin, self.budget)
        recheck(self.library_pin, self.budget)
        for item in self.source_pins:
            recheck(item, self.budget)


class FormalBinding:
    def __init__(self, input_plan_pin, material_lineage_pin, kernel_control_pin, budget):
        self.plan_pin = input_plan_pin; self.budget = budget
        self.plan = read(input_plan_pin, budget)
        if self.plan['schema'] != 'CURRENT_FORMAL_FULL370_UNREDUCED_INPUT_PLAN_V1':
            raise ReferenceUnready('current fixed Source input plan')
        original = read(self.plan['protected_formal_and_producer_plan_pin'], budget)
        self.protected = original
        self.fixed = original['formal_inputs'] + [
            value for row in original['producers']
            for value in (row['report'],row['archive'],row['radial_binary_track'])]
        self.fixed += self.plan['additional_current_input_pins']
        by_path = {}
        for item in self.fixed:
            if item['path'] in by_path and item != by_path[item['path']]:
                raise ReferenceFailure('ambiguous current fullfile input')
            by_path[item['path']] = item
        self.fixed = list(by_path.values())
        for item in self.fixed:
            recheck(item, budget)
        case_pin = self.plan['current_case_spec_pin']
        if case_pin['sha256'] != FORMAL_CASE_SHA or case_pin not in self.fixed:
            raise ReferenceUnready('formal current CASE fbe336, not old ac3e')
        case = read(case_pin, budget)
        prepared = read(self.plan['current_prepared_pin'], budget)
        cfg = prepared['production_config']
        if (case['basis']['requested_rank'] != 1 or cfg != original['formal_configuration'] or
            cfg['cells_per_zone'] != 16 or cfg['sn'] != 32 or
            cfg['zone_height_cm'] != 50.0 or cfg['rank'] != 1 or
            case['cases']['AAA'] != ['A','A','A'] or
            case['geometry']['physical_z_edges_cm'] != [0,50,100,150] or
            case['production']['groups'] != NG or case['production']['fission_components'] != NF):
            raise ReferenceUnready('complete current formal H150/48/SN32/rank1/AAA context')
        # Numerical candidate controls derive directly from current frozen case.
        # The one global integral is roundoff-checked using the original strict
        # transport arithmetic ceiling. This is declared BEFORE any execution.
        self.controls = Controls(max_outer=cfg['maxout'], max_inner=cfg['maxinr'],
            inner_relative=cfg['eps_mccg'], flux_relative=cfg['eps_axial'],
            keff_relative=cfg['eps_axial'], eigen_relative=cfg['eps_axial'],
            normalization_absolute=self.plan['physical_checks']['global'])
        if self.plan['full_reference_controls'] != asdict(self.controls):
            raise ReferenceUnready('Source controls differ from exact current-case derivation')
        # These receipts are actual independently produced data. No empty or
        # future value, old META-only success, or internal coherent labels pass.
        self.lineage_pin = material_lineage_pin
        self.kernel_control_pin = kernel_control_pin
        self.lineage = read(material_lineage_pin, budget)
        self.kernel_controls = read(kernel_control_pin, budget)
        self._admit_lineage()
        self._admit_kernel_controls()
        self.digest = None

    def _admit_lineage(self):
        value = self.lineage
        if (value['schema'] != 'ACTUAL_CURRENT_FORMAL_FULL370_MATERIAL_LINEAGE_V1' or
            value['current_case_spec_pin'] != self.plan['current_case_spec_pin'] or
            value['current_producer_archive_pins'] != [r['archive'] for r in self.protected['producers']] or
            value['all370_raw_macro_word_comparisons'] != 3 or
            value['all_raw_word_mismatches'] != 0 or
            value['all_six_required_phases_finished'] is not True or
            value['all_context_or_operand_issues'] != 0 or
            value['all_necessary_reference_producers_known'] is not True or
            value['captured_actual_full_SPH_selection'] is not True or
            value['captured_actual_MASK_and_oldmacro'] is not True or
            value['actual_reaction_multiplicity_source_coverage_complete'] is not True):
            raise ReferenceUnready('current raw transfer/context/reaction producer incomplete')
        for key in ('actual_observation_report_pin','actual_extraction_report_pin',
                    'actual_aggregation_report_pin','actual_multiplicity_report_pin',
                    'independent_saved_production_review_pin'):
            recheck(value[key], self.budget)
        # Complete raw evidence is mandatory, and itself bound into this object.
        if not value['complete_actual_evidence_pins']:
            raise ReferenceUnready('raw evidence cannot be replaced by a result label')
        for item in value['complete_actual_evidence_pins']:
            recheck(item, self.budget)

    def _admit_kernel_controls(self):
        value = self.kernel_controls
        if (value['schema'] != 'ACTUAL_CURRENT_FULL370_NDIM3_KERNEL_CONTROLS_V1' or
            value['current_case_spec_pin'] != self.plan['current_case_spec_pin'] or
            value['offset_order'] != self.plan['offset_order'] or
            value['boundary_model'] != self.plan['boundary_model'] or
            value['physical_checks'] != self.plan['physical_checks'] or
            value['complete_original_tracks'] != 11364 or
            value['actions_per_group_sweep'] != 181824 or
            value['groups'] != NG or value['axial_cells'] != NZ or
            value['retained_moments'] != NMOM or value['all_actual_controls_passed'] is not True or
            value['original_caps'] != CAPS or value['full_reference_qualified'] is not False):
            raise ReferenceUnready('new formal kernel controls pending, no helper inheritance')
        for item in value['complete_actual_evidence_pins']:
            recheck(item, self.budget)
        recheck(value['independent_saved_control_review_pin'], self.budget)

    def load_model(self):
        materials = []
        for row in self.protected['producers']:
            report = actual_success_report(row['report'], self.budget)
            if len(report['records']) != 4 or report['actual_native_terminal'] != row['native_readback']:
                raise ReferenceUnready('own actual single-plane producer/readback contract')
            materials.append(terminal_material_from_snapshot(row['archive']))
        first = materials[0]
        # Each plane is an independent physical product, not a copied/relabelled
        # archive. Raw mathematical arrays/contexts must nevertheless agree for
        # AAA. Equality is computed here rather than inferred from filenames.
        for other in materials[1:]:
            for field in ('total_f4','raw_scatter_f4','nusigf_f4','chi_f4','tranc_f4',
                          'sigs_f4','sigw_f4','energy_f4','fission_index','chi_limits'):
                if array_digest(first[field]) != array_digest(other[field]):
                    raise ReferenceFailure('AAA independent plane field differs '+field)
            for field in first['micro_context_fields']:
                if array_digest(first['micro_context_fields'][field]) != array_digest(other['micro_context_fields'][field]):
                    raise ReferenceFailure('current isotope temperature/density/mix differs')
            if first['macro_record_identity'].keys() != other['macro_record_identity'].keys():
                raise ReferenceFailure('complete raw record name scope differs')
            for name, descriptor in first['macro_record_identity'].items():
                if descriptor.get('sha256') != other['macro_record_identity'][name].get('sha256'):
                    raise ReferenceFailure('complete raw macro payload differs '+name)
        for row, material in zip(self.protected['producers'],materials):
            for name, coverage in material['compressed_payload_coverage'].items():
                if np.any(coverage['count'] > 1) or np.any(coverage['unaddressed_values'] != 0):
                    raise ReferenceUnready('original compressed nonzero padding/duplicate requires explicit producer evidence '+name)
            if material['track']['MATCOD'].tolist() != list(range(1,9)):
                raise ReferenceUnready('original radial region/material identity')
        rays = native_track_inventory(self.protected['producers'][0]['radial_binary_track'])
        states = angular_states_from_native(first['track']['XMU$MCCG'].astype('d'),
            first['track']['ZMU$MCCG'].astype('d'), first['track']['WZMU$MCCG'].astype('d'),
            rays['azimuth_xy'][:,0],rays['azimuth_xy'][:,1])
        with _open_xsm(self.plan['current_axial_track_pin']['path']) as archive:
            directory = archive.root
            state,_ = array(archive,directory,'STATE-VECTOR','<i4',40)
            if (state[0] != NR*NZ or state[5] != NR or state[6] != NZ or
                state[7] != 3 or state[14] != 32):
                raise ReferenceUnready('actual formal SPOT48/SN32 geometry')
            area,_=array(archive,directory,'AREA2D','<f4',NR)
            dz,_=array(archive,directory,'VOL1D','<f4',NZ)
            mat1d,_=array(archive,directory,'MAT1D','<i4',NZ)
            volume,_=array(archive,directory,'VOLUME','<f4',NR*NZ)
            ncode,_=array(archive,directory,'NCODE','<i4',2)
            u,_=array(archive,directory,'U','<f4',32)
            w,_=array(archive,directory,'W','<f4',32)
            pl,_=array(archive,directory,'PL','<f4',3*32)
        if (not np.array_equal(mat1d,np.repeat([1,2,3],16)) or
            not np.array_equal(dz,np.full(NZ,np.float32(150.0/NZ))) or
            np.any(area <= 0) or np.any(volume <= 0) or np.any(ncode != 1)):
            raise ReferenceUnready('exact current zones/grid/vacuum physical data')
        expected = area.astype('d')[:,None]*dz.astype('d')[None,:]
        volume = volume.reshape(NR,NZ)
        if np.any(np.abs(volume.astype('d')-expected) > np.spacing(volume).astype('d')/2):
            raise ReferenceFailure('actual VOLUME exact original half-ULP extrusion check')
        model=dict(material_ids=np.repeat(np.arange(NR)[:,None],NZ,axis=1),
            scatter64=first['raw_scatter_f4'].astype('d'),
            nusigf64=first['nusigf_f4'].astype('d'),chi64=first['chi_f4'].astype('d'),
            total64=np.repeat(first['total_f4'].astype('d')[:,None,:],NZ,axis=1),
            volume64=volume.astype('d'),
            stored_surface64=np.repeat(first['track']['V$MCCG'][8:].astype('d')[:,None],NZ,axis=1)*dz,
            tranc64=first['tranc_f4'].astype('d'),events64={k:v.astype('d') for k,v in first['events_f4'].items()},
            formal_SN32_U=u,formal_SN32_W=w,formal_SN32_PL=pl,
            rays=rays,states=states,binding=self)
        self.digest=complete_model_digest(model)
        self.verify_model(model,self.controls)
        return model

    def verify_model(self,model,controls):
        if self.digest is None or asdict(controls) != asdict(self.controls):
            raise ReferenceUnready('actual loaded current model and derived controls')
        recheck(self.plan_pin,self.budget);recheck(self.lineage_pin,self.budget)
        recheck(self.kernel_control_pin,self.budget)
        for item in self.fixed:
            recheck(item,self.budget)
        if complete_model_digest(model) != self.digest:
            raise ReferenceFailure('bound complete material/rays/states/formal U/W/PL input changed')
        self._admit_lineage();self._admit_kernel_controls()


    def verify_operator(self,model,operator):
        from current_formal_full370_ray_operator import WholeRayOperator
        if type(operator) is not WholeRayOperator or self.digest is None:
            raise ReferenceUnready('concrete full current ray operator and loaded model')
        if (array_digest(operator.total) != self.digest['arrays']['total64'] or
            array_digest(operator.volume) != self.digest['arrays']['volume64'] or
            array_digest(operator.stored_surface) != self.digest['arrays']['stored_surface64'] or
            complete_value_digest(operator.ray_inventory) != self.digest['rays'] or
            complete_value_digest(operator.rays) != complete_value_digest(model['rays']['tracks']) or
            complete_states_digest(operator.states) != self.digest['states']):
            raise ReferenceFailure('actual operator material/volume/surface/rays/angular fields differ from bound model')
        if (operator.order != self.plan['offset_order'] or
            operator.chunk != self.plan['working_group_chunk'] or
            operator.boundary_model != self.plan['boundary_model'] or
            operator.checks != self.plan['physical_checks']):
            raise ReferenceUnready('actual operator original order/white model/checks differ from current plan')
        binding=operator.kernel_binding
        if (self.kernel_controls['actual_kernel_origin_pin'] != binding.origin_pin or
            self.kernel_controls['actual_kernel_library_pin'] != binding.library_pin or
            self.kernel_controls['actual_kernel_build_report_pin'] != binding.report_pin or
            self.kernel_controls['complete_kernel_source_pins'] != binding.source_pins):
            raise ReferenceUnready('actual operator library/complete Source origin differs from real kernel controls')
        binding.verify(operator.library)


def independent_full_angular_initial_guess(states):
    """Integrate an independently declared positive isotropic angular ansatz.

    All1536 states are evaluated. The six absent observed moments are never
    read. Zero odd values, if produced by actual symmetric quadrature sums,
    arise from this independent initial guess, not completion of missing data.
    No initialized higher moment is described as a measured native terminal.
    """
    moments = np.zeros(NMOM); mass = 0.0
    for index,key in enumerate(states.keys):
        weight = float(states.wzmu[key[0]]*states.zmu[key[0]]/(4*states.azimuth_count))
        moments += weight*states.harmonics[index]; mass += weight
    if not np.isfinite(mass) or mass <= 0 or not np.isfinite(moments).all():
        raise ReferenceFailure('independent complete angular initial ansatz')
    # One angular initial-guess amplitude, before the one global nu-fission
    # normalization in the eigeniteration. This is not a fitted transport weight.
    moments /= mass
    return np.broadcast_to(moments,(NR,NZ,NG,NMOM)).copy()

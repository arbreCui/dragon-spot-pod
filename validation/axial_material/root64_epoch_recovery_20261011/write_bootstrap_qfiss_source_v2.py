"""Source-only v2: preserve actual axial B1/SIGS and separate radial B0 route."""
from pathlib import Path
import hashlib, json, time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
V1=REC/'bootstrap_qfiss_source_v1'
V2=REC/'bootstrap_qfiss_source_v2'
V2.mkdir(exist_ok=True)
(V2/'original_exact_v1').mkdir(exist_ok=True)
started=time.monotonic()

def pin(path):
    path=Path(path); stat=path.stat()
    return {'path':str(path),'bytes':stat.st_size,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'seven_id':[stat.st_dev,stat.st_ino,stat.st_mode,stat.st_nlink,
                        stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns]}

v1_manifest=json.loads((V1/'SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json').read_text())
protected=v1_manifest['source_pins']
assert all(pin(p['path'])==p for p in protected)

# Independently check emitted v1 against complete saved original byte inverses.
inverse_results=[]
for name in ['SPOR64_BOOT_CANONICAL64.f90','SPOR64_BOOTQ64.f90']:
    proof=json.loads((V1/(name+'.exact_local_byte_inverse.json')).read_text())
    data=(V1/name).read_text()
    for c in reversed(proof['changes']):
        at=c['offset_before']
        assert data[at:at+len(c['new'])]==c['new']
        data=data[:at]+c['old']+data[at+len(c['new']):]
    assert hashlib.sha256(data.encode()).hexdigest()==proof['original_sha256']
    assert data==Path(proof['original_input']['path']).read_text()
    inverse_results.append({'new_source':pin(V1/name),'complete_byte_inverse':True,
                            'original_input':proof['original_input']})

original_q=(ROOT/'src/SPOR64_B2N.f90').read_text()
new_q=(V1/'SPOR64_BOOTQ64.f90').read_text()
def segment(source,start,stop):
    begin=source.index(start); end=source.index(stop,begin)
    return source[begin:end]
fission_start='    q64 = +0.0_real64\n'
integral_start='    qint64 = +0.0_real64\n'
fission_old=segment(original_q,fission_start,integral_start)
fission_new=segment(new_q,fission_start,integral_start)
assert fission_old==fission_new
integral_stop='    if (.not. all(ieee_is_finite(qint64))) return'
integral_old=segment(original_q,integral_start,integral_stop)
integral_new=segment(new_q,integral_start,integral_stop)
assert integral_old.replace('real(volume32(ir),real64)','volume64(ir)')==integral_new
original_can=(REC/'continuous_chain_source/SPOSTATE64.f90').read_text()
new_can=(V1/'SPOR64_BOOT_CANONICAL64.f90').read_text()
norm_start='  ! One global nu-fission-production normalization.\n'
leak_start='  ! Reconstruct the original signed leakage from the same REAL64 field.\n'
basis_start='  ! Recover the fixed radial basis layout.\n'
old_norm=segment(original_can,norm_start,leak_start)
new_norm=segment(new_can,norm_start,leak_start)
expected_norm=old_norm.replace('if (ilong == 0) cycle','if (ilong == 0) return')
expected_norm=expected_norm.replace("call XABORT('SPOSTATE64: INVALID NUSIGF RECORD.')",'return')
expected_norm=expected_norm.replace("call XABORT('SPOSTATE64: NON-FINITE NUSIGF.')",'return')
expected_norm=expected_norm.replace("call XABORT('SPOSTATE64: NONPOSITIVE GLOBAL NU-FISSION NORMALIZATION.')",'return')
assert expected_norm==new_norm
old_leak=segment(original_can,leak_start,basis_start)
new_leak=segment(new_can,leak_start,basis_start)
assert old_leak.replace("call XABORT('SPOSTATE64: NON-FINITE LEAKAGE STATE.')",'return')==new_leak
formula={'status':'BYTE_ONLY_FORMULA_EVIDENCE_NO_NUMERICAL_EXECUTION',
         'complete_original_byte_inverses':inverse_results,
         'entire_original_region_slot_h_g_qfiss_loop_byte_identical':True,
         'qfiss_loop_sha256':hashlib.sha256(fission_new.encode()).hexdigest(),
         'volume_integral_only_operand_spelling_changed':True,
         'volume64_bit_checked_equal_to_original_promoted_geometry':True,
         'global_normalization_arithmetic_preserved':True,
         'normalization_guard_only_change':'all370 NUSIGF records mandatory; ordinary refusal',
         'full_signed_face_current_leakage_arithmetic_preserved':True,
         'no_formula_calculated_during_evidence_generation':True}
(V1/'FORMULA_SEGMENT_BYTE_EVIDENCE.json').write_text(json.dumps(formula,indent=2)+'\n')
(V1/'SOURCE_ONLY_WRITER_ACTUAL_TOOL_RETURN.json').write_text(json.dumps({
    'schema':'ACTUAL_SOURCE_ONLY_WRITER_RECEIPT',
    'actual_tool':'tools.exec_command', 'actual_chunk_id':'51c8ac', 'actual_exit_code':0,
    'actual_writer_self_seconds':0.002959790999739198,
    'actual_source_pins':protected,
    'compile_or_Native_run':False,
    'later_source_review_status':'UNREADY_GLOBAL_ROUTE_CONTRACT_V1_REJECTS_ACTUAL_B1_SIGS',
    'reported_by_root':'v1 requires TYPE2/B0 but original global is TYPE3/B1 SIGS',
    'v1_source_remains_frozen_unchanged':True,
    'qualified':False},indent=2)+'\n')
(V1/'V1_FROZEN_UNREADY_GLOBAL_ROUTE_REVIEW.txt').write_text(
    'Frozen v1 Source is unready for the real global route. Original production_inputs.py '
    'uses TYPE K B1 SIGS REBA OFF; FLUGPI.f converts ITYPEC=2 to3 for an explicit '
    'buckling option. Global OPTION B1 is independent of radial RCON OPTION B0. '
    'Root found this before compile/runtime. v1 strict counter>=caps also exceeds '
    'the original terminal branch policy; a valid EPS-converged at-cap iterate may '
    'be rejected. v2 corrects both in a new namespace. No v1 Source was changed.\n')

class Transform:
    def __init__(self,data): self.original=data; self.data=data; self.changes=[]
    def replace_all(self,old,new,label,count):
        assert self.data.count(old)==count,(label,self.data.count(old))
        for index in range(count):
            at=self.data.index(old)
            self.changes.append({'label':label,'offset_before':at,'old':old,'new':new})
            self.data=self.data[:at]+new+self.data[at+len(old):]
    def finish(self,name):
        undo=self.data
        for c in reversed(self.changes):
            at=c['offset_before']; assert undo[at:at+len(c['new'])]==c['new']
            undo=undo[:at]+c['old']+undo[at+len(c['new']):]
        assert undo==self.original
        (V2/name).write_text(self.data)
        (V2/'original_exact_v1'/name).write_text(self.original)
        (V2/(name+'.v1_exact_local_byte_inverse.json')).write_text(json.dumps({
            'original_v1_source':pin(V1/name),'v2_source':pin(V2/name),
            'original_v1_complete_byte_inverse':True,'changes':self.changes},indent=2)+'\n')

names=['SPOR64_BOOT_CANONICAL64.f90','SPOR64_BOOT_CONTEXT64.f90','SPOR64_BOOTQ64.f90']
for name in names:
    t=Transform((V1/name).read_text())
    module=name[:-4]
    t.replace_all('module '+module+'\n','module '+module+'_V2\n','independent v2 module namespace',2)
    if name=='SPOR64_BOOT_CONTEXT64.f90':
        t.replace_all('use SPOR64_BOOT_CANONICAL64, only',
                      'use SPOR64_BOOT_CANONICAL64_V2, only','use actual complete v2 canonical module',1)
        t.replace_all('    if (ax_state(3) /= 1.or.ax_state(6) /= 2) return',
                      '    ! Original production TYPE K B1 SIGS becomes ITYPEC=3 in FLUGPI.\n'
                      '    if (ax_state(3) /= 1.or.ax_state(6) /= 3.or.ax_state(7) /= 3) return\n'
                      '    if (ax_state(10) /= 0) return',
                      'actual original global B1 SIGS route / REBA OFF',2)
        t.replace_all("    if (.not.CHARACTER_RECORD_MATCHES(ipax,'OPTION',1,4,contract%flu_option)) return",
                      "    if (.not.CHARACTER_RECORD_MATCHES(ipax,'OPTION',1,4,'B1')) return\n"
                      "    if (contract%flu_option /= 'B0') return",
                      'separate explicit global B1 and radial RCON B0',2)
        t.replace_all('any(counter >= caps)','any(counter > caps)',
                      'retain original inclusive iteration-cap bound and strict EPS',2)
    if name=='SPOR64_BOOTQ64.f90':
        t.replace_all('use SPOR64_BOOT_CONTEXT64, only',
                      'use SPOR64_BOOT_CONTEXT64_V2, only','use actual complete v2 ingress',1)
    t.finish(name)

deps=v1_manifest['actual_dependency_pins']
deps=deps+[pin(ROOT/'validation/axial_material/production_inputs.py'),
           pin(ROOT/'src/FLUGPI.f'),pin(ROOT/'src/FLUDRV.f'),
           pin(REC/'global_native64_dependency_source_v2/driver_source/SPOT_GLOBAL_NATIVE_DRIVER64.f'),
           pin(ROOT/'Ganlib/lib/Darwin_arm64/modules/ganlib.mod'),
           pin(ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a'),
           pin(ROOT/'lib/Darwin_arm64/libDragon.a')]
manifest={'status':'NEW_SOURCE_ONLY_V2_TRUE_GLOBAL_B1_SIGS_NOT_COMPILED_NOT_RUN',
          'source_pins':[pin(V2/name) for name in names],
          'protected_v1_before':protected,'protected_v1_after':[pin(p['path']) for p in protected],
          'actual_dependency_pins':deps,'writer_pin':pin(Path(__file__)),
          'public_procedure_ABI_names_and_parameters_unchanged':True,
          'modules':['SPOR64_BOOT_CANONICAL64_V2','SPOR64_BOOT_CONTEXT64_V2','SPOR64_BOOTQ64_V2'],
          'global_route':{'ITYPEC':3,'ILEAK_SIGS':3,'OPTION':'B1','REBA':0,
                          'source':'complete original production_inputs.py _axial_solve + FLUGPI'},
          'radial_RCON_route':{'OPTION':'B0','loaded_true_contract':True},
          'iteration_cap_policy':'>=min and <=MAX; exact original strict residual/inner-state gate unchanged',
          'science_formula_and_original_preflight_unchanged_from_full_v1':True,
          'original_17_controls_passed':False,'global_actual_runtime_wired':False,
          'bootstrap_actual_runtime_wired':False,'AAA_qualified':False,'ABA_started':False,
          'opaque_old_archive_source_to_object_mapping_proved':False,
          'host_full_SHA_seven_ID_external_pins_required':True}
assert manifest['protected_v1_after']==protected
(V2/'SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json').write_text(json.dumps(manifest,indent=2)+'\n')
(V2/'FORMULA_SEGMENT_BYTE_EVIDENCE.json').write_text(json.dumps(formula,indent=2)+'\n')
v2doc=(V1/'ABI_FORMULA_EVIDENCE_AND_REMAINING_CALLER.txt').read_text()
v2doc=v2doc.replace('QFISS64 v1, 2026-10-11','QFISS64 v2, 2026-10-12')
v2doc=v2doc.replace('module SPOR64_BOOT_CANONICAL64\n','module SPOR64_BOOT_CANONICAL64_V2\n')
v2doc=v2doc.replace('module SPOR64_BOOT_CONTEXT64\n','module SPOR64_BOOT_CONTEXT64_V2\n')
v2doc=v2doc.replace('module SPOR64_BOOTQ64\n','module SPOR64_BOOTQ64_V2\n')
v2doc=v2doc.replace('and strictly below the declared caps','and at or below the original declared caps')
v2doc=v2doc.replace(' AX TYPE-K header has STATE[3]=1 and STATE[6]=2 and OPTION matches RCON.',
                     ' AX original B1/SIGS header has STATE[3]=1, STATE[6]=3, STATE[7]=3,\n'
                     " STATE[10]=0 (REBA OFF), OPTION='B1'. The radial RCON remains OPTION='B0'.")
v2doc += ('\nV2 route correction is Source-only, before any compile/runtime. The complete '
          'v1 Sources remain frozen. New modules have suffix _V2; public procedure '
          'names/arguments remain unchanged. Complete v1 inverse proofs are retained '
          'and new v1-to-v2 inverse proofs preserve the same full mathematics.\n')
(V2/'ABI_FORMULA_EVIDENCE_AND_REMAINING_CALLER.txt').write_text(v2doc)
long_lines=[]
for name in names:
    for number,line in enumerate((V2/name).read_text().splitlines(),1):
        if len(line)>132: long_lines.append([name,number,len(line)])
assert not long_lines,long_lines
print(json.dumps({'status':manifest['status'],
                  'source_writer_self_seconds':time.monotonic()-started,
                  'source_pins':manifest['source_pins'],
                  'protected_v1_unchanged':True,'long_lines':long_lines},indent=2))

"""Independent finite read-only Source review. No candidate imports or execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE = REC/'saved_full370_terminal_audit_host_source_v2'
OUT = Path(__file__).resolve().parent
started = time.monotonic()
checks = []

def require(condition, name):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p = Path(p)
    before = identity(p)
    require(stat.S_ISREG(before[2]), 'regular:'+str(p))
    with p.open('rb') as f:
        s = os.fstat(f.fileno())
        opened = [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        require(opened == before, 'opened7ID:'+str(p))
        sha = hashlib.file_digest(f,'sha256').hexdigest()
        s = os.fstat(f.fileno())
        after = [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        require(after == before == identity(p), 'fullEOF7ID:'+str(p))
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)

def load(name):
    return json.loads((BASE/name).read_text())

binding = load('CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
mapping = load('COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json')
sf = load('COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json')
hf = load('COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json')
cli = load('ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json')
inverse = load('COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json')
original = json.loads(Path(binding['original_v1_binding_current_pin']['path']).read_text())
manifest = load('ACTUAL_INPUT_PIN_PLAN_UNRUN.json')
old_manifest = json.loads(Path(sf['original_manifest_current_pin']['path']).read_text())
host = Path(hf['host_pin']['path']).read_text()
science = Path(sf['source_pin']['path']).read_text()
host_ast = ast.parse(host)
science_ast = ast.parse(science)

require(len(binding['fixed_current_pins']) == 3315, '3315 fixed current pins')
require(len({p['path'] for p in binding['fixed_current_pins']}) == 3315, '3315 unique fixed current paths')
require(len(original['fixed_current_pins']) == 3305, '3305 original fixed pins')
require(len(mapping['rows']) == 3301 and not mapping['errors'], '3301 explicit current mapping and no errors')
require(len(mapping['historical_non_live_declarations']) == 4, 'four explicitly historical missing Source origins')
require(len(binding['science_original_input_pins']) == len(manifest['inputs']) == 1129, '1129 complete science inputs')
require(sum(p['size_bytes'] for p in binding['science_original_input_pins']) == 102109901, 'complete science input bytes')

current = []
historical = []
for row in mapping['rows']:
    old, now = row['historical_pin'], row['current_pin']
    require((old['path'],old['sha256'],old['size_bytes'],old['identity'][1:]) ==
            (now['path'],now['sha256'],now['size_bytes'],now['identity'][1:]), 'six unchanged fields and SHA:'+now['path'])
    require(old['identity'][0] in (16777234,16777229) and now['identity'][0] == 16777229, 'explicit actual mount transition:'+now['path'])
    require(now in binding['fixed_current_pins'], 'old live mandatory retained:'+now['path'])
    current.append(now)
    historical.append(old)

known_missing = {
    'ACTUAL_INPUT_PIN_PLAN_UNRUN.json', 'PARSER_SOURCE_PROOF.json',
    'SCIENTIFIC_REVIEW_AND_SOURCE_ONLY_HANDOFF.txt', 'audit_saved_terminal_source_all370.py',
}
require({Path(d['historical_pin']['path']).name for d in mapping['historical_non_live_declarations']} == known_missing, 'exact four missing historical Source-origin names')
for declaration in mapping['historical_non_live_declarations']:
    old = declaration['historical_pin']
    require(Path(old['path']).parent == Path('/private/tmp/SPOT_AAA_full370_terminal_source_UNRUN_20261012'), 'exact historical TMP origin parent')
    require(not os.path.lexists(old['path']), 'actual historical Source origin absent:'+old['path'])
    require(declaration['current_pin'] is None and declaration['in_scientific_1129_inputs'] is False and declaration['original_v1_mandatory'] is True, 'explicit no fake current PF:'+old['path'])
    require(old['path'] not in manifest['inputs'] and old['path'] not in {p['path'] for p in binding['fixed_current_pins']}, 'not scientific or current mandatory input:'+old['path'])
    historical.append(old)
require(sorted(historical,key=lambda p:p['path']) == sorted(original['fixed_current_pins'],key=lambda p:p['path']), 'all original3305 declarations exactly accounted')
require(binding['historical_non_live_Source_origins'] == mapping['historical_non_live_declarations'], 'binding maps exact historical classifications')
require(all(p in current for p in binding['science_original_input_pins']), 'all science inputs in original genuine live mapping')
require(manifest['inputs'] == old_manifest['inputs'], '1129 original science path SHA pairs exact')
require({p['path']:p['sha256'] for p in binding['science_original_input_pins']} == manifest['inputs'], '1129 science complete declaration correspondence')
require(Path(sf['source_pin']['path']).read_bytes() == Path(sf['original_science_current_pin']['path']).read_bytes(), 'science full bytes identical to preserved v1')
rebound = json.loads(Path(sf['original_manifest_current_pin']['path']).read_text())
rebound['source']['path'] = sf['source_pin']['path']
require(rebound == manifest, 'manifest semantic change only self Source path')
rebind = inverse['manifest_only_literal_rebind']
require(Path(sf['science_manifest_pin']['path']).read_text().replace(rebind['new_literal'],rebind['old_literal'],1) == Path(sf['original_manifest_current_pin']['path']).read_text(), 'manifest exact inverse complete bytes')
old_host = Path(inverse['original_host_current_pin']['path']).read_text()
for change in inverse['complete_host_literal_changes']:
    require(old_host.count(change['old_literal']) == change['literal_count'] == 1, 'one original host literal:'+change['label'])
    old_host = old_host.replace(change['old_literal'],change['new_literal'],1)
require(old_host == host, 'entire host inverse reconstructs exactly six scoped edits')
require(hf['schema'] == 'COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V2', 'exact host Source freeze schema')
require(hf['input_binding_pin']['path'] == str(BASE/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'), 'host exact current binding path')

live_pins = binding['fixed_current_pins'] + hf['fixed_source_files'] + [cli['Source_freeze_pin'], sf['original_science_current_pin'], sf['original_manifest_current_pin'], inverse['original_host_current_pin'], binding['original_v1_binding_current_pin']]
unique = {}
for expected in live_pins:
    p = expected['path']
    require(p not in unique or unique[p] == expected, 'no conflicting complete current pin:'+p)
    unique[p] = expected
for path, expected in unique.items():
    require(pin(path) == expected, 'current actual fullEOF exact SHA/7ID:'+path)
require(pin(BASE/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json')['sha256'] == 'dd332c394874abbb8c80a4e7b976af034e0cd8461ff5e8b551bbbab98d12386d', 'Root CLI frozen bytes')

expected_argv = ['env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hf['host_pin']['path'],'--freeze-sha256',cli['Source_freeze_pin']['sha256'],'--freeze-seven-id',json.dumps(cli['Source_freeze_pin']['identity'],separators=(',',':'))]
require(cli['argv'] == expected_argv, 'exact canonical frozen host CLI')
require(not os.path.lexists(cli['planned_actual_ART_output']) and not os.path.lexists(cli['planned_actual_TMP_output']), 'both true fresh actual execution namespaces absent')

for literal in ["history=factory.DynamicHistoryResources(ART,factory.history_roots([str(OUT)],ART),8*2**30,96*2**30,production.ResourceFailure)","fresh=production.DiskResources(ART,[str(OUT)],8*2**30,2*2**30)","runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA_SAVED_AUDIT',resources)","runner.execute(OUT/'AAA_SAVED_AUDIT','saved_terminal_source_all370',command,600)","resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20", "h['artifact_bytes']+tb+20971764748+64*2**20>=96*2**30", "f['artifact_bytes']+tb>=2*2**30", "free-20971764748-2*2**30<8*2**30", "before['combined_history_bytes']+20971764748+64*2**20+2*2**30>=96*2**30", "resources.check()", "replace_just_created_owned_report(summary,summary_pin,report)"]:
    require(literal in host, 'reviewed original guard/cap literal:'+literal)
for literal in ["os.open(p,os.O_RDWR|os.O_NOFOLLOW)","hashlib.file_digest(f,'sha256').hexdigest()!=wanted['sha256']", "p!=OUT/'Root_actual_saved_full370_diagnostic_summary.json'", "s.st_nlink!=1", "f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())", "return 0 if failure is None else 1"]:
    require(literal in host, 'same-fd owned late-failure boundary:'+literal)
for field in ('full_neutron_balance_qualified','full_eigen_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'):
    require(sf[field] is False, 'science freeze no unsupported qualification:'+field)
for field in ('AAA_qualified','ABA_admitted','goal_complete'):
    require(hf[field] is False, 'host freeze no unsupported qualification:'+field)
require("sys.addaudithook(no_launch)" in science and "LAUNCH_ATTEMPTS.append(event);raise RuntimeError" in science, 'science rejects child launches')
require("UNKNOWN_SIX_TRANSVERSE_OR_MIXED_MOMENTS_NOT_OBSERVED; no zero completion, no fitted/angular reconstruction" in science, 'six unknown moments never reconstructed or qualified')
require("known_NDIM3_R_indices_0based':[0,2,6]" in science and "unknown_NDIM3_R_indices_0based':[1,3,4,5,7,8]" in science, 'exact observed and unobserved axes')
require("NG,NUN,NZ,NA,NR,NL,NMAT,NF=370,1800,48,32,8,3,24,32" in science, 'all370 and32 fission components fixed dimensions')
require("raw_allgroup_scatter_source=all_scatter" in science and "raw_diagonal_minus_SIGW=selfraw-sigw" in science, 'signed complete scatter and diagonal differences retained')
require("native_DD_saved_source_defect=dd_native" in science and "native_DD_final_source_defect=dd_final" in science, 'native and reconstructed final source residuals distinct')
require("UNKNOWN; saved-minus-final difference is not thereby a bug proof" in science, 'historical arithmetic/source phase unknown no fabricated cause proof')

report = dict(
    schema='INDEPENDENT_SAVED_FULL370_V2_FINITE_RUNTIME_SCOPE_SOURCE_REVIEW_20261013',
    status='SOURCE_REVIEW_PASS_CONDITIONAL_ON_ROOT_TRUE_BOOT_AND_ACTUAL_GUARDED_TERMINAL',
    checks=len(checks), failed_checks=[], fullEOF_unique_inputs=len(unique),
    fullEOF_unique_input_bytes=sum(p['size_bytes'] for p in unique.values()),
    fixed_current_binding_count=3315, original_fixed_declarations=3305,
    genuine_live_original_mandatory=3301, historical_nonlive_Source_only_origins=4,
    complete_scientific_inputs=1129, complete_scientific_input_bytes=102109901,
    science_full_bytes_unchanged=True, complete_host_inverse_six_scoped_edits=True,
    complete_original_guard_Source_MRO_and_caps_preserved=True,
    approved_interpretation_of_historical_classification='Four absent prior TMP Source-generation origins retain original historical PF. They are excluded only from the new current execution mandatory list, not from historical provenance, and are not scientific inputs. This is a new explicit current declaration; old historical stages were not rerun.',
    scientific_scope='All370 historical saved terminal axial P0/P1/P2 only; all32 fission terms and signed complete scatter retained. Six unobserved NDIM3 moments remain UNKNOWN. No coupled reference, AAA physics accuracy or ABA admission.',
    runtime_requirements=['Root must independently prove true three-plane GLOBAL and online BOOT aggregate closed0 before this diagnostic', 'Exact frozen CLI plus original stage600/whole1800/SELF and own child512MiB/one thread/one science child/no retry', 'Initial full2GiB and cold20971764748+metadata64MiB history96GiB reservation and free8GiB on both filesystems must actually pass', 'Actual canonical child watcher, final reports and retained scientific files must be reviewed with true external terminal closed0'],
    thread_scope='Canonical native library environment and single Python main thread are enforced; the unchanged original OwnRSS guard measures actual own child RSS. It does not itself provide a native thread census or kernel hard RSS cap, and this review claims neither.',
    actual_candidate_imported_or_executed=False, compiler_or_transport_executed=False,
    upstream_three_plane_or_BOOT_qualification_granted=False,
    full_neutron_balance_qualified=False, full_eigen_reference_qualified=False,
    AAA_qualified=False, ABA_admitted=False, goal_complete=False,
    current_host_pin=hf['host_pin'], current_host_Source_freeze_pin=cli['Source_freeze_pin'],
    current_science_Source_freeze_pin=cli['selected_actual_science_source_freeze_pin'],
    current_binding_pin=cli['input_binding_pin'], current_mapping_pin=cli['current_mapping_pin'],
    current_actual_frozen_CLI_pin=pin(BASE/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json'),
    review_elapsed_seconds=time.monotonic()-started,
    review_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
)
path = OUT/'REVIEW.json'
with path.open('x') as f:
    json.dump(report,f,indent=2,allow_nan=False)
    f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],checks=report['checks'],unique_fullEOF_inputs=report['fullEOF_unique_inputs'],unique_fullEOF_bytes=report['fullEOF_unique_input_bytes'],report_pin=pin(path),candidate_imported_or_executed=False),allow_nan=False))

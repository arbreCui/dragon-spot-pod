"""Finish finite author Source documentation/provenance; no candidate execution."""
import ast
import hashlib
import json
from pathlib import Path
import shutil

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')

def pin(path):
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();assert [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before
    return dict(path=str(path),sha256=sha,size_bytes=s.st_size,identity=before)

def write(path,value):
    with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def main():
    evidence=P/'CURRENT_ROOT_ENVIRONMENT_SOURCE_META';evidence.mkdir()
    original_stdlib=Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/subprocess.py')
    sp=pin(original_stdlib);assert sp['sha256']=='85d29b2bf0249f5436838298c9a60ee93508b1102e9ac43b001f8a7e7ae8f375'and sp['size_bytes']==88747
    ast.parse(original_stdlib.read_bytes());target=evidence/'COMPLETE_ORIGINAL_PYTHON_3_12_SUBPROCESS_SOURCE.py';shutil.copy2(original_stdlib,target);assert target.read_bytes()==original_stdlib.read_bytes()
    current=B/'Root_actual_Python_resource_dependency_and_waitid_capability_Source_META.json';cp=pin(current)
    assert cp['sha256']=='a22507c0289c2be4f52d034b77671b48f9ebce128f56a2b478b22f1ac51a7f98'and cp['size_bytes']==1397
    copied=evidence/current.name;shutil.copy2(current,copied);assert copied.read_bytes()==current.read_bytes()
    write(evidence/'COMPLETE_ORIGINAL_STDLIB_AND_ACTUAL_ROOT_CAPABILITY_BYTE_RETENTION.json',dict(schema='N8_COMPLETE_ORIGINAL_STDLIB_AND_CURRENT_ROOT_SOURCE_META_RETENTION_V1',source_only=True,actual_original_stdlib_subprocess_Source_pin=sp,actual_retained_complete_stdlib_Source_pin=pin(target),actual_current_Root_capability_META_original_pin=cp,actual_retained_current_Root_capability_META_pin=pin(copied),Root_actual_capability_terminal_chunk='2f89e2',waitid_callable_in_exact_current_Root_environment=False,waitid_constants_are_not_API_support=True,waitid_or_ctypes_or_new_native_platform_alternative_used=False,actual_current_author_API_or_control_execution=False,future_Root_stdlib_Source_witness=None,future_actual_monitor_controls_qualification=None))
    contract=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())
    protocol=json.loads((P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes())
    write(P/'EXPECTED_N8_FUTURE_ROOT_SOURCE_AND_CONTROLS_BINDING.UNREADY.json',dict(schema='N8_COMPLETE_SOURCE_AND_ACTUAL_MONITOR_CONTROLS_FUTURE_ROOT_INTERFACE_V1',status='UNREADY_SOURCE_ONLY_NOT_ADMITTED_BOUND_EXECUTED_OR_QUALIFIED',source_only=True,required_complete_author_Source_roles=contract['required_author_Source_roles'],required_complete_author_Source_role_count=21,required_independent_Source_review_schema=contract['required_review_schema'],required_independent_Source_review_status=contract['required_pass_status'],actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_controls_Source_binding=None,actual_independent_bound_controls_Source_prelaunch_review=None,actual_complete_controls_manifest=None,actual_Root_complete_controls_tool_terminal=None,actual_independent_saved_controls_review=None,actual_monitor_controls_qualification=None,actual_Root_monitor_qualification_tool_terminal=None,actual_business_request=None,actual_business_bound_Source=None,actual_business_native_AB_terminal=None,actual_scientific_qualification=None,new_owner_instrumentation=['exact genuine start_liveness_watchdog delegate wrapper captures original business Popen/sessionPGID and watchdog Popen','per exact original Popen instance _internal_poll delegates original method with one original locked waitpid callback','per exact original Popen instance _try_wait normal wait body records actual original waitpid; ECHILD/permissions non-OSError unknown refusal','one current canonical fullPS pid/ppid/pgid/stat union; closed leader singlePID exclusion after actual owned WIFEXITED/WIFSIGNALED wait','controls-only real transition hook after original watchdog start and realPS; production hooks always None'],original_guard_classes_MRO_global_wait_APIs_and_Source_unchanged=True,first_live_census_acceptance_gate_added_by_author_then_removed=True,original_scope_basis=protocol['original_contract_and_added_gate_correction'],all_original_caps=protocol['original_caps'],all_actual_OS_control_outcomes=None,source_controls_plan_is_not_an_actual_monitor_qualification=True,old_actual_OS_failures_are_finite_unchanged_guard_regression_not_new_monitor_execution=True,canonical_OS_nonzero_timeout_oversize_or_EPERM_is_not_manufactured=True,remaining_limits=protocol['accurate_remaining_limits'],scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False))
    text='''N8 fresh complete Source, UNREADY. No controls, process APIs, guard, compiler,
native/material/numeric operation was executed by the author. The 1598-check
author result is Source/AST/full EOF evidence, not independent review or runtime
qualification. Original181 members, all14 Source owners, native1365 members,
physics/inverses/seeds/shared libraries/recipes/guard bytes/caps are retained.
Seven additional explicit Source owners make21. All future actual facts are None.

Original scope basis and finite correction:
N7 joint_bytes lines205-212 form the current host parent-chain closure; it does
not require a first live census for every business PID. The preserved genuine
OwnRSSSerialExecutor._process starts original Popen with start_new_session=True,
then original watchdog captures process.pid as group. Its first poll may already
be0, after which final resources.check still runs. The author's added first-live-
census prerequisite was removed. The real early-exit control now requires exact
original owned wait0/reap and a complete currentPS union; excludes only the closed
leader singlePID; keeps host/watchdog/current samePGID/any captured descendants.
ECHILD, wrong exact owner/frame, and later current reuse of a closed PID remain
refusals. No lsof nonzero is accepted. Unknown current observations are not PASS.
Historical unobserved escaped ancestry is not reconstructed or added as a user gate.

Root sequence (all paths/SHA/7ID must come from actual immutable saved facts):
1. Different-author complete Source review, common schema/status in the required
scope contract, actual_author_Source_contract exact21 fullpins including MF.
Root derives and separately reviews a strict Source-admission writer for this
fixed package/21 roles, executes only it, and saves its actual CLOSED0 terminal.
No N7 admission/runtime result or old controls qualification is reused for N8.
2. Root saves actual six canonical tool pins and exact subprocess Source witness
schema ROOT_ACTUAL_N8_PYTHON_SUBPROCESS_SOURCE_AND_WAIT_OWNER_WITNESS_V1,
source_only=True, actual_wait_poll_signal_or_control_execution=False. The current
Python lacks callable waitid; constants do not support a waitid route. No ctypes
or native replacement is provided. Complete original subprocess Source is saved.
3. Source binder CLI:
python3.12 -B N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py
 --source-manifest-sha256 <actual MF SHA>
 --independent-Source-review <actual independent Source REVIEW.json>
 --Source-admission <actual Root Source admission META>
 --actual-Source-admission-terminal <actual CLOSED0 Root admission wrapper>
 --actual-tool-pins-meta <actual {tool_pins: six real fullpins} META>
 --actual-stdlib-Source-witness <actual Source-only subprocess witness>
 --output-source-dir <B>/actual_complete_native_observation_BUILD5_AB_v8_monitor_controls_sources
 --receipts <B>/actual_complete_native_observation_BUILD5_AB_v8_monitor_controls_receipts
<B> is /Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010.
E exists before Source binding; D is fresh. Binder copies the whole Source package,
creates true binding, bound driver and full3-global inverse. Root saves actual
CLOSED0 source binding wrapper schema ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1.
Then a different-author full actual-bound Source prelaunch review is mandatory.
All Source/receipt E files required by driver exist before its first freeze.
4. Each actual genuine control is one fresh fixed H/O/C namespace from the binding:
python3.12 -B <D>/Root_bound_N8_genuine_monitor_controls_driver.py
 --case-id <one exact protocol CASE_ID>
 --actual-source-binding-terminal <actual Source-binding CLOSED0 wrapper>
 --independent-bound-control-Source-prelaunch-review <actual prelaunch review>
Keep the original one-thread environment, whole1800/stage600/RSS512, joint2GiB,
history96GiB/free8GiB, business children1/retries0. Do not re-run failed namespaces.
Use actual controls Source, actual private fixtures and the same production factory/
owner helper under genuine original runner; no synthetic PS/lsof/EPERM qualification.
Case01 includes real wait0 before any business census as a positive case. Case04
requires real nonzero7 to preserve original stage failure. Case06 records actual
external reaping/ECHILD and wrong ownership refusal. Current live and reparented
descendant FD/group scope is covered by actual private fork cases. Private8MiB
output is labelled private output only; no canonical tool oversize/EPERM is claimed.
5. After actual case tool close, Root records strict full currentPS4cols showing
actual PID/PPID/PGID targets absent, actual original resource/history/free closure,
each real tool terminal, and the full Source D/receipt E frozen snapshot. These
postclose files go under that case H/O/C, never append frozen D/E. This confirms
current absence only; original historical cleanupTrue is never backfilled.
6. Source/small-META assembler CLI for each actual case:
python3.12 -B N8_Root_controls_postclose_META.UNREADY.py --mode case
 --binding <actual Source binding> --facts <actual driver facts>
 --case-terminal <actual Root case CLOSED0 wrapper>
 --current-group-closure <actual strict current group/PS META>
 --current-group-terminal <its actual Root CLOSED0 wrapper>
 --postclose-resources <actual original resource factory META>
 --postclose-resource-terminal <its actual Root CLOSED0 wrapper>
 --output <counted case C>/Root_actual_case_postclose.json
Required schema/fields are explicit in Source and protocol. It does not run PS,
lsof, resource APIs, candidates or guards, and cannot invent missing actual facts.
7. Assemble all12 in exact order, with refreshed actual all-controls resource
META/terminal (joint union of all12 H/O/C and shared D/E once), then actual Root
manifest tool close, independent full saved-controls review, and Q:
--mode manifest --binding <binding> --case-final <case01 postclose> ...
 --case-final <case12 postclose> --controls-postclose-resources <actual union META>
 --controls-postclose-resource-terminal <actual union CLOSED0 wrapper>
 --output <case12 C>/ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST.json
--mode qualification --binding <binding> --manifest <actual immutable manifest>
 --controls-terminal <actual complete-controls CLOSED0 wrapper>
 --independent-saved-review <actual independent saved controls review>
 --controls-postclose-resources <refreshed actual union META>
 --controls-postclose-resource-terminal <actual refreshed union CLOSED0 wrapper>
 --output <case12 C>/Root_actual_N8_monitor_controls_qualification.json
Root separately saves Q writer's actual CLOSED0 wrapper. Own and each later receipt
append remain counted within original caps. Q grants only actual monitor controls.
8. Only actual Q plus Q real terminal permit original request/binder/runtime action.
Request's new required CLI flags are --monitor-controls-qualification <actual Q>
and --monitor-controls-qualification-terminal <actual Q CLOSED0 wrapper>; all
original request flags, original129+Source/tool inputs, library fullEOF, whole
five original build groups and A/B seed/material observation ordering remain.
New business fixed namespace is v8, not monitor-controls or any old v7 namespace.
Fresh actual request/bind + complete actual-bound Source prelaunch are still needed.
Source-only author/independent PASS does not establish live disk/RSS/native/science.
'''
    with (P/'N8_ROOT_NEXT_STEPS_SOURCE_ONLY.txt').open('x')as f:f.write(text)
    print(json.dumps(dict(status='AUTHOR_COMPLETE_N8_FINAL_SOURCE_AND_ROOT_INTERFACE_WRITTEN_UNREADY',source_only=True,actual_waitid_API_callable_in_existing_Root_witness=False,actual_candidate_or_controls_or_API_execution=False),allow_nan=False))

if __name__=='__main__':main()

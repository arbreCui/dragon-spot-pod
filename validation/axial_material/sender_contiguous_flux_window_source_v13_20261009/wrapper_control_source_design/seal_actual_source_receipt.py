"""Seal the already observed source-only tool return; no compiler/business."""
from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v13_flusp64_window_wrapper_control_source_draft_20261009')
def fullpin(p):
    s=p.stat();b=p.read_bytes();t=p.stat()
    fields=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    assert tuple(getattr(s,x) for x in fields)==tuple(getattr(t,x) for x in fields)
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),
            'identity':{x:getattr(t,x) for x in fields}}
assert (D/'source_design.stderr').read_bytes()==b''
data=json.loads((D/'source_design.stdout').read_bytes())
assert fullpin(D/'REPORT.json')['sha256']==data['status']
assert fullpin(D/'CONTROL_CONTRACT.json')['sha256']==data['contract_sha256']
assert fullpin(D/'flusp64_window_observer_controls.UNREADY.f90')['sha256']==data['driver_sha256']
receipt={'schema':'AXMAT_ACTUAL_SOURCE_ONLY_TOOL_TERMINAL_RETURN_V1',
 'actual_tool_result':{'chunk_id':'753414','wall_time_seconds':0.000007292,'exit_code':0,'original_token_count':0,'output':''},
 'tool_state':'CLOSED','returncode_type':'int','actually_executed':'STDlib seal_source_design.py only',
 'stdout':fullpin(D/'source_design.stdout'),'stderr':fullpin(D/'source_design.stderr'),
 'source_report':fullpin(D/'REPORT.json'),'compiled_or_ran_Fortran':False,'business_imported_or_called':False,
 'project_written':False,'Root_handle_polled':False,'actual_controls':None,'actual_RSS':None}
with (D/'actual_readonly_tool_return.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
with (D/'HANDOFF.txt').open('x') as f:
 f.write('SOURCE ONLY UNREADY: Root sole compile/runner; original68controls unchanged.\n')
 f.write('Actual source-only generator753414 returned integer0 CLOSED; streams retained.\n')
 f.write('14 mandatory modes and all raw/namespace/EOF counts are CONTROL_CONTRACT.json.\n')
 f.write('No actual source-wrapper control, numerical solve, RSS qualification or native/AAA/ABA credit.\n')
 f.write('Source-only original reference extraction is a single routine-name inverse.\n')
 f.write('Production link uses actual fullsender object + real GANLIB, SPOF observer only in this test.\n')
 f.write('Root writes independent audit_sender_controls(controls_root,contract); no auditor run here.\n')
 f.write('Direct failed FUN may be partially written; retain no-retry failure semantics.\n')
files=[fullpin(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest={'schema':'AXMAT_V13_SENDER_WINDOW_SOURCE_DESIGN_EVIDENCE_MANIFEST_V1','status':'SOURCE_ONLY_UNREADY',
          'files':files,'actual_source_terminal':{'chunk_id':'753414','exit_code':0,'state':'CLOSED'},
          'compiled_or_controls_run':False,'project_written':False}
with (D/'EVIDENCE_MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
print(json.dumps({'report':fullpin(D/'REPORT.json'),'receipt':fullpin(D/'actual_readonly_tool_return.json'),
                 'evidence_manifest':fullpin(D/'EVIDENCE_MANIFEST.json'),'reference_unit':fullpin(D/'FLUSP64_REFERENCE.f')},separators=(',',':')))

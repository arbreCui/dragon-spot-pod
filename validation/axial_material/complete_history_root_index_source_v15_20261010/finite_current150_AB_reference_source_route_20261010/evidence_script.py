"""Bounded SOURCE/small-META references only; no project API/helper/guard import."""
import hashlib
import json
from pathlib import Path
import stat
import time

ROOT=Path('/Users/wen/spot')
OUT=Path(__file__).parent
FILES=[
 'validation/axial_material/complete_history_root_index_source_v15_20261010/CURRENT_SCIENTIFIC_GAPS.txt',
 'validation/axial_material/case_spec.json',
 'validation/axial_material/material_inputs.py',
 'validation/axial_material/material_audit.py',
 'validation/axial_material/material_interface.txt',
 'validation/axial_material/prepare_qualified_AB_production.py',
 'validation/axial_material/production_inputs.py',
 'validation/axial_material/audit_r64_snapshot.f90',
 'validation/iterative/native_layered_full_action.py',
 'validation/iterative/native_layered_transport.py',
 'src/MGXEXP.f90','src/SPOPHYS.f90','src/SPOT1P64.f90','src/SPOASM.f','src/FLU2DR64.f',
 'validation/d4_reference/export_map8_macrolib.x2m',
 'validation/d4_reference/audit_mgxexp.py',
 'validation/artifacts/axial-material-inputs-20261003/material_results.json',
 'validation/artifacts/axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005/AAA/reference_assessment.json']
ANCHORS={
 'src/MGXEXP.f90':['nleg=min(nanis,norder+1)','absorption(igr)=total(igr)-sigs(igr)','N2N','Raw Legendre moments'],
 'src/SPOPHYS.f90':['diagnostic full physical radial','call LCMEQU','basis_new(i,i)','RADIAL-OP'],
 'src/SPOT1P64.f90':['ONLY CONSTANT DIAMOND','diagonal_basis=nmode == nreg2d','radial2d(i,isnap)','mn(n,l)='],
 'validation/axial_material/production_inputs.py':['if self.rank > 2','ALLG DIAM 0 SN','SPOD {config.rank} FIXB'],
 'validation/axial_material/material_inputs.py':['MACRO_OUT := MACRO','ANIS 3','nfis 32','self.fuel_C'],
 'validation/axial_material/material_audit.py':['(370, 8, 3, 32)','for order in (0, 1)','No SPH factor record'],
 'validation/iterative/native_layered_full_action.py':['def solve_white','def main','[51,61,98]']}

def ident(path):
 s=path.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

refs={}
for rel in FILES:
 path=ROOT/rel;before=ident(path)
 if not stat.S_ISREG(before[2]) or before[4]>1000000:raise ValueError('bounded regular SOURCE/small META only: '+rel)
 raw=path.read_bytes();after=ident(path)
 if before!=after or len(raw)!=before[4]:raise ValueError('reference changed across complete read: '+rel)
 text=raw.decode();lines=text.splitlines()
 refs[rel]=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before,complete_SOURCE_or_small_META_read=True,matched_anchors={anchor:[i+1 for i,line in enumerate(lines) if anchor in line] for anchor in ANCHORS.get(rel,[])})
materials=ROOT/'validation/artifacts/axial-material-inputs-20261003'
payload_metadata={}
for state in ('A','B'):
 for name in ('material.xsm','macro.ascii'):
  path=materials/state/name;before=ident(path)
  if not stat.S_ISREG(before[2]):raise ValueError('missing current saved material payload: '+str(path))
  payload_metadata[str(path)]=dict(identity=before,size_bytes=before[4],payload_opened=False,payload_SHA_not_freshly_verified=True)
review=dict(schema='AXMAT_CURRENT150_SAME_T_AB_UNREDUCED_REFERENCE_BOUNDED_SOURCE_ROUTE_V1',status='SOURCE_ROUTE_IDENTIFIED_NOT_IMPLEMENTED_NOT_EXECUTED_NOT_QUALIFIED',created_unix=time.time(),source_reference_count=len(refs),project_import=False,project_API_or_helper_or_guard_called=False,numeric_or_business_executed=False,full_payload_read=False,history_rescanned=False,saved_source_phase_diagnostic_reverified=False,canonical_or_saved_evidence_modified=False,raw_material_payloads_only_stat_metadata=True,science_thresholds_changed=False,source_references=refs,current_saved_material_payload_stat_metadata=payload_metadata,report_sha256=hashlib.sha256((OUT/'REPORT.txt').read_bytes()).hexdigest(),entry_findings=dict(current_raw_complete_material_export_exists_in_SOURCE=True,generic_MGXEXP_PN2_3moment_32fission_export_exists_in_SOURCE=True,MGXEXP_complete_transport_reaction_contract=False,current_complete_independent_coupled_reference_ready=False,SPOPHYS_same_model_full8_coordinate_control_exists_in_SOURCE=True,SPOPHYS_independent_closure_truth=False),qualification=dict(full_MG_data_transfer=False,current_unreduced_coupled_reference=False,physical_neutron_balance=False,AAA_accuracy=False,ABA_admitted=False,new_build=False,whole_INPUT=False,native=False,goal_complete=False))
(OUT/'REVIEW.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(status=review['status'],references=len(refs),output=str(OUT),report_sha256=review['report_sha256'],numeric_or_business_executed=False)))

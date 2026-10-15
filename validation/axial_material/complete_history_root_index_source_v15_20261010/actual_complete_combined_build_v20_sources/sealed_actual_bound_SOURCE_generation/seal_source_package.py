"""Seal finite SOURCE design; never bind Root PREP metadata or run any project API."""
import ast
import hashlib
import json
from pathlib import Path
import stat

DEST=Path(__file__).parent
NORMAL19=Path('/private/tmp/axmat_v19_normal_PREP_host_source_binding_20261010')

def pin(path, expected=None):
    path=Path(path)
    if '/validation/artifacts/' in str(path) or not path.is_absolute() or path.resolve()!=path:
        raise ValueError('ordinary SOURCE only; never ART')
    a=path.lstat()
    if not stat.S_ISREG(a.st_mode) or a.st_nlink!=1:raise ValueError('unique regular SOURCE required')
    data=path.read_bytes(); b=path.lstat()
    identity=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    digest=hashlib.sha256(data).hexdigest()
    if identity(a)!=identity(b) or len(data)!=b.st_size or (expected is not None and digest!=expected):
        raise ValueError('complete fresh SOURCE SHA7ID mismatch')
    return data,dict(path=str(path),sha256=digest,identity=identity(b))

def write_new(path, value):
    data=value if isinstance(value,bytes) else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(data)

def main():
    data,generator=pin(DEST/'generate_build_host.py','c8cf1a7c0a3e60c4cfb2edfc88e496e9fedccb25330c11c5bbb7421d23c52f72')
    parent,parent_pin=pin(DEST/'frozen_parent_generate_build_host_v19.py','dc48a3c47804359ba483bab74da31df3cd5aebad0a2935c994211ebd76293d39')
    proof_data,proof_pin=pin(DEST/'Root_finite_build_generator_source_inverse.json','e25cf0306bb39a69de28bea17fd8beab7512d4e58f959b22354cef5399699939')
    proof=json.loads(proof_data); backward=data.decode()
    for change in reversed(proof['changes']):
        if backward.count(change['after'])!=change['count']:raise ValueError('exact finite inverse count required')
        backward=backward.replace(change['after'],change['before'])
    if backward.encode()!=parent:raise ValueError('entire dc48 parent exact inverse required')
    design_data,design_pin=pin(DEST/'SOURCE_DESIGN_REPORT.json','176358e269ed236d52462e8acb35a0877abb1ff3517c3d50435d2317aa56774f')
    design=json.loads(design_data)
    if design['host_generated'] is not False or design['business_executed'] is not False or design['fixed_retarget_count']!=11 or design['closed_actual_binding_retarget_count']!=6:
        raise ValueError('unbound complete original SOURCE design required')
    if not all(design[key] is None for key in ('actual_V20_declaration_sha256','actual_V20_prep_terminal_sha256','actual_V20_Root_prepare_summary_sha256','actual_V20_complete_graph_sha256','actual_V20_creation_trace_sha256')):
        raise ValueError('all future actual PREP pins must remain None')
    if (DEST/'combined_build_host.py').exists() or (DEST/'Root_finite_build_host_source_inverse.json').exists():
        raise ValueError('future binding branch must not run')
    source_chain=design['original_thirteen_change_proof']
    if source_chain['finite_change_count']!=13 or source_chain['host_sha256']!='cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9' or source_chain['parent_sha256']!='37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3':
        raise ValueError('complete original cf2c thirteen-change source chain required')
    normal,normal_pin=pin(NORMAL19/'combined_prepare_host.py','f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580')
    normal_proof,normal_proof_pin=pin(NORMAL19/'full_host_ancestry_inverse_proof.json','2ab2bd271400bc53bfd94414ed5cea6c3c69016797b25ad17a8133fb8d7479fe')
    # Preserve the already qualified whole proof without broadening the current SOURCE review.
    write_new(DEST/'reused_original_normal_v19_prepare_host.py',normal)
    write_new(DEST/'reused_original_normal_v19_complete_ancestry_proof.json',normal_proof)
    actual_data,actual_pin=pin(DEST/'actual_source_design_tool_returns.json')
    actual=json.loads(actual_data)
    if any(type(x.get('exit_code')) is not int or x['exit_code']!=0 or 'session_id' in x for x in actual['source_only_tools']):
        raise ValueError('actual typed SOURCE-only tools must be closed EXIT0')
    for name in ('generate_build_host.py','adapt_frozen_v19_generator_SOURCE_ONLY.py','seal_source_package.py','actual_writer_v19_SOURCE.py','actual_writer_v20_SOURCE.py'):
        source,_=pin(DEST/name); ast.parse(source.decode()); compile(source.decode(),str(DEST/name),'exec')
    report=dict(schema='AXMAT_V20_COMPLETE_BUILD_GENERATOR_SOURCE_PACKAGE_REPORT_V1',status='UNREADY_SOURCE_TEMPLATE_AWAIT_REAL_ROOT_V20_PREP_CLOSED_SUCCESS',generator=generator,finite_generator_inverse=proof_pin,source_design=design_pin,actual_SOURCE_tools=actual_pin,full_inverse_dc48=True,frozen_cf2c_thirteen_change_inverse_to_37d_verified_by_source_only_check=True,original_normal_v19_f5c_source=normal_pin,reused_qualified_f5c_complete_ancestry_proof=normal_proof_pin,source_history_not_reaudited=True,actual_writer20_source=proof['actual_writer20_source'],actual_writer19_source=proof['actual_writer19_source'],complete_actual_writer_inverse_af0c_to_7c69=True,actual_writer_fields_compatible=True,writer_binding_location=proof['writer_binding_location'],canonical_v20_SOURCE_sha256=proof['canonical_v20_SOURCE_sha256'],future_real_summary_path='/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v20_receipts/Root_actual_complete_combined_prepare_summary.json',future_real_summary_sha256=None,future_actual_declaration_sha256=None,future_actual_formal_PREP_terminal_sha256=None,future_actual_complete_input_graph_sha256=None,future_actual_complete_creation_trace_sha256=None,future_actual_Root_PREP_terminal_sha256=None,metadata_binding_parameter_count=2,full_five_stages=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'],all_four_metadata_tools_seal_and_full_tails_retained=True,genuine_guard_and_MRO_unchanged=True,outer_seconds=1800,inner_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0,archive_scope=['HOST','SOURCE','OUT','TERMINAL','new_SOURCE_ARCHIVE'],host_generated=False,binding_branch_executed=False,business_executed=False,API_or_helper_or_guard_called=False,ART_read_or_written=False,numeric_payload_read=False,new_BUILD_success_qualified=False,whole_combined_INPUT_admitted=False,native_executed=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False)
    write_new(DEST/'REPORT.json',report)
    members=[]
    for p in sorted(DEST.iterdir()):
        if not p.is_file() or p.name=='sealed_manifest.json':raise ValueError('exact ordinary fresh SOURCE package required')
        _,ref=pin(p); members.append(ref)
    for ref in members:
        _,again=pin(ref['path'],ref['sha256'])
        if ref!=again:raise ValueError('all complete SOURCE member pins remain unchanged')
    manifest=dict(schema='AXMAT_V20_COMPLETE_BUILD_SOURCE_ONLY_SEALED_MANIFEST_V1',status=report['status'],root=str(DEST),members=members,all_complete_member_SHA7ID_before_after_exact=True,host_generated=False,binding_branch_executed=False,business_executed=False,ART_read_or_written=False,numeric_payload_read=False,actual_PREP_success_claimed=False,new_BUILD_success_qualified=False)
    manifest_path=DEST/'sealed_manifest.json'; write_new(manifest_path,manifest)
    _,manifest_pin=pin(manifest_path)
    print(json.dumps(dict(status=report['status'],manifest=manifest_pin,member_count=len(members),generator_sha256=generator['sha256'],report_sha256=hashlib.sha256((DEST/'REPORT.json').read_bytes()).hexdigest(),host_generated=False,binding_branch_executed=False,business_executed=False)))

if __name__=='__main__':main()

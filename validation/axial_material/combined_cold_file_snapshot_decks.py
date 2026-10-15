"""Pure INPUT-only file-SNAP complete-deck permutations for the original 844 cold case.

No file operations, project imports, solver invocation, resource admission or
qualification occur here. The caller must use freshly generated original
write_inputs decks and apply changes before c.prepare seals local_files.
Both complete original decks are hard-pinned. Each copy and SNAP storage-medium
change has a separate whole-deck inverse and def/use proof. The independent XSM
work file is created only by the future native case, not by this pure helper.
Actual 512MiB fitness for bootstrap/combined cold is unproved.
"""
import hashlib
import re
from collections.abc import Mapping

PRODUCTION_INPUTS_SHA256='9af09bc87f6a0b10081370a2bbd46a23cf649a8ef74cf3851f3df5d2a01fea5c'
WRITE_INPUTS_DEFINITION_SHA256='00687ead9434bf4ad8c79afdf2de783b479de48b8211dc06d660849764fa5ddb'
SPECS={
    'bootstrap_axial.x2m':dict(
        original_sha256='13a43842e6fe32ea1568e476715f5ca3a0b44c7dbab5744d7667b9cc956e893e',
        copy=b'SNAP := SNAP_IN ;\n',source_symbol='SNAP_IN',
        old_successor=b'AX_CURRENT := FLU: MACROLIB3 TRACK_AX SYSTEM_NEXT ::\n',
        after=b'AX_CURRENT := SPOSTATE: AX_CURRENT TRACK_AX SYSTEM_NEXT MACROLIB3 :: ;\n',
        immediately_after_module='SPOSTATE',
        module_order=['FLU','SPOGBAL','SPOSTATE','SPOLEAK']),
    'picard_axial.x2m':dict(
        original_sha256='0849ed24c071fde68957c32956b55dae619a8801c3e64a38e0a7a03c703b5cc4',
        copy=b'SNAP := RADIAL_IN ;\n',source_symbol='RADIAL_IN',
        old_successor=b'AX_CURRENT := PARENT_AX ;\n',
        after=b'AX_CURRENT := SPOXCONV: AX_CURRENT PARENT_AX :: ;\n',
        immediately_after_module='SPOXCONV',
        module_order=['FLU','SPOGBAL','SPOSTATE','SPOXCONV','SPOLEAK'])}
FIRST_USE=b'SNAP := SPOLEAK: SNAP AX_CURRENT TRACK_AX :: >>leak_change<< ;\n'
ORIGINAL_SNAPSHOT_DECLARATION=b'LINKED_LIST SNAP AX_CURRENT ;\n'
FILE_SNAPSHOT_DECLARATION=(b"XSM_FILE SNAP :: FILE './radial_snapshot_work.xsm' ;\n"
                           b'LINKED_LIST AX_CURRENT ;\n')
WORKING_SNAPSHOT_NAME='radial_snapshot_work.xsm'


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _scientific_statements(raw):
    result=[]
    for statement in raw.split(b';'):
        match=re.search(rb'(?m)^([^\n]*:=\s*(FLU|SPOGBAL|SPOSTATE|SPOXCONV|SPOLEAK):)',statement)
        if match:result.append((match.group(2).decode('ascii'),statement[match.start():]+b';'))
    return result


def _defer_complete_deck(original,name):
    if type(original) is not bytes or name not in SPECS:
        raise ValueError('one complete original immutable byte deck is required')
    spec=SPECS[name]
    if _digest(original)!=spec['original_sha256']:
        raise ValueError('original frozen deck bytes changed')
    copy,successor,after=spec['copy'],spec['old_successor'],spec['after']
    declaration=ORIGINAL_SNAPSHOT_DECLARATION
    for exact in (copy,successor,after,FIRST_USE,declaration):
        if original.count(exact)!=1:
            raise ValueError('single complete definition and first-use anchors required')
    if copy+successor not in original or after+FIRST_USE not in original:
        raise ValueError('complete original snapshot copy/call ordering differs')
    start=original.index(copy);end=original.index(FIRST_USE)
    if not start<end or re.search(rb'\b(?:SNAP|'+spec['source_symbol'].encode('ascii')+rb')\b',original[start+len(copy):end]):
        raise ValueError('a snapshot or source object has an earlier use or modification')
    scientific=_scientific_statements(original)
    if [name for name,_ in scientific]!=spec['module_order']:
        raise ValueError('complete original scientific modules/parameters/order required')
    deferred=original.replace(copy,b'',1).replace(after,after+copy,1)
    if WORKING_SNAPSHOT_NAME.encode('ascii') in original:
        raise ValueError('independent work filename already appears in original deck')
    transformed=deferred.replace(declaration,FILE_SNAPSHOT_DECLARATION,1)
    if (transformed.count(FILE_SNAPSHOT_DECLARATION)!=1 or declaration in transformed
        or transformed.count(WORKING_SNAPSHOT_NAME.encode('ascii'))!=1
        or len(re.findall(rb'(?m)^(?:LINKED_LIST|XSM_FILE)\s+SNAP\b',transformed))!=1):
        raise ValueError('exact sole independent file SNAP declaration required')
    regions=[dict(before=copy.decode('ascii'),after=''),
             dict(before=after.decode('ascii'),after=(after+copy).decode('ascii')),
             dict(before=declaration.decode('ascii'),after=FILE_SNAPSHOT_DECLARATION.decode('ascii'))]
    recovered_deferred=transformed.replace(FILE_SNAPSHOT_DECLARATION,declaration,1)
    if recovered_deferred!=deferred:
        raise ValueError('storage-medium inverse does not recover complete deferred deck')
    recovered=recovered_deferred.replace(after+copy,after,1).replace(successor,copy+successor,1)
    if recovered!=original or transformed.count(copy)!=1 or after+copy+FIRST_USE not in transformed:
        raise ValueError('independent full-deck inverse or actual first use differs')
    if _scientific_statements(transformed)!=scientific:
        raise ValueError('scientific call body/argument order changed')
    return transformed,dict(schema='AXMAT_COMBINED_COLD_FILE_SNAPSHOT_COMPLETE_DECK_INPUT_V1',
        classification='DECK_INPUT_ONLY_NO_NATIVE_OR_SCIENTIFIC_CREDIT',deck_name=name,
        original_sha256=_digest(original),deferred_sha256=_digest(transformed),
        prior_linked_list_deferred_sha256=_digest(deferred),
        candidate_file_snapshot_sha256=_digest(transformed),
        whole_deck_bytes=len(original),candidate_whole_deck_bytes=len(transformed),
        whole_deck_inverse_byte_exact=True,storage_medium_inverse_byte_exact=True,
        sole_SNAP_storage_medium='XSM_FILE',independent_working_snapshot_name=WORKING_SNAPSHOT_NAME,
        working_snapshot_not_an_input_or_candidate_output_alias=True,
        complete_working_snapshot_bytes_must_enter_native_stage_namespace_and_storage=True,
        original_and_deferred_single_copy=True,source_object=spec['source_symbol'],
        no_snapshot_or_source_reference_between_original_copy_and_first_SPOLEAK=True,
        immediately_after_module=spec['immediately_after_module'],first_consumer='SPOLEAK',
        all_scientific_statements_in_original_order_byte_exact=True,
        scientific_modules=list(spec['module_order']),pure_statement_regions=regions,
        inverse_operations=[dict(remove=FILE_SNAPSHOT_DECLARATION.decode('ascii'),restore=declaration.decode('ascii')),
                            dict(remove=(after+copy).decode('ascii'),restore=after.decode('ascii')),
                            dict(remove=successor.decode('ascii'),restore=(copy+successor).decode('ascii'))],
        original_write_inputs_function_changed=False,original_Fortran_arithmetic_changed=False,
        logical_snapshot_cache_co_residence_avoided=True,
        actual_native_RSS_under_512MiB_proved=False,predicted_RSS_saving_claimed=False,
        prior_failed_peak_cause_claimed=False,bootstrap_or_map_solve_executed=False,
        AAA_accuracy_qualified=False,ABA_admitted=False)


def defer_bootstrap_snapshot_deck(original):
    return _defer_complete_deck(original,'bootstrap_axial.x2m')


def defer_picard_snapshot_deck(original):
    return _defer_complete_deck(original,'picard_axial.x2m')


def defer_freshly_generated_axial_decks(original_decks):
    """Return changed bytes; the caller owns fresh-directory writes/inventory.

    The complete map is returned, preserving every other deck byte. There is no
    automatic directory traversal or inferred input/source allowance.
    """
    if not isinstance(original_decks,Mapping) or not set(SPECS).issubset(original_decks):
        raise ValueError('both original generated axial decks must be supplied explicitly')
    if any(type(name) is not str or type(raw) is not bytes for name,raw in original_decks.items()):
        raise ValueError('literal deck names and complete raw byte values required')
    candidate=dict(original_decks);proofs={}
    for name in SPECS:
        candidate[name],proofs[name]=_defer_complete_deck(original_decks[name],name)
    for name in set(original_decks)-set(SPECS):
        if candidate[name]!=original_decks[name]:raise ValueError('another generated deck changed')
    return candidate,dict(schema='AXMAT_COMBINED_COLD_TWO_FILE_SNAPSHOT_DECK_INPUTS_V1',
        classification='DECK_INPUT_ONLY_NO_NATIVE_OR_SCIENTIFIC_CREDIT',independent_deck_inverses=proofs,
        original_production_inputs_source_sha256=PRODUCTION_INPUTS_SHA256,
        original_write_inputs_function_source_sha256=WRITE_INPUTS_DEFINITION_SHA256,
        only_two_complete_copy_statements_moved=True,
        only_two_SNAP_declarations_use_independent_XSM_files=True,
        independent_working_snapshot_name=WORKING_SNAPSHOT_NAME,
        all_other_generated_deck_bytes_unchanged=True,
        actual_bootstrap_RSS_or_mathematical_output_credit=False,
        actual_cfb_map012_capture_credit_not_inherited=True,
        actual_file_snapshot_map012_capture_credit_not_inherited=True,
        original_budgets=dict(total_seconds=43200,axial_seconds=4200,bootstrap_axial_seconds=4200,
            bootstrap_radial_seconds=600,radial_seconds=300,setup_seconds=120,host_seconds=120,max_maps=100),
        scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False)

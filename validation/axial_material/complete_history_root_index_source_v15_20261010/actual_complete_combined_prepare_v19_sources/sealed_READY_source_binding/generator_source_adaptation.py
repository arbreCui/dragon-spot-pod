"""Strict finite SOURCE-only inverse adaptation of the frozen V18 READY binding generator."""
import ast
import hashlib
import json
from pathlib import Path

D=Path(__file__).parent
P=Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010/source_binding_generator.py')
OLD_SHA='4d54cc988d47918017bdabcf082918bf528cf0ef2a94000a7a082cec68989f0f'
old=P.read_text()
assert hashlib.sha256(old.encode()).hexdigest()==OLD_SHA
text=old
edits=[]
def replace(before,after,count=1):
    global text
    assert text.count(before)==count,before[:120]
    text=text.replace(before,after)
    edits.append(dict(old=before,new=after,occurrences=count))
replace("U=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/next_complete_combined_v18_source_only_review/sealed_complete_UNREADY_candidate/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py')",
"U=Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py')")
replace("P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')",
"P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')")
replace("D=Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010')",
"D=Path('/private/tmp/axmat_v19_complete_combined_READY_source_binding_20261010')")
replace("R=U.parent.parent/'sealed_independent_source_review/REVIEW.json'\nM=U.parent.parent/'sealed_independent_source_review/sealed_manifest.json'",
"R=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/next_complete_combined_v18_source_only_review/sealed_independent_source_review/REVIEW.json')\nM=R.parent/'sealed_manifest.json'")
replace("RP=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')",
"RP=Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')\nI18=Path('/private/tmp/axmat_v18_complete_combined_full_phase_last_use_source_only_20261010/source_inverse_proof.json')\nR17=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')")
replace("inputs=[U,I,P,Q,G,S,R,M,RP,I17,O]","inputs=[U,I,P,Q,G,S,R,M,RP,I17,O,I18,R17]")
replace("assert before[0]['sha256']=='ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'",
"assert before[0]['sha256']=='585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50'")
replace("assert before[1]['sha256']=='920d4cef7d96e8f0737a82f9e5cad8feb7b7c3387324dc128b66f1c45908f0e4'",
"assert before[1]['sha256']=='c3927b04791aa00115f1ad661f6113de6992d5a93f165a3c8ea58586dccd6595'")
replace("assert before[2]['sha256']=='feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'",
"assert before[2]['sha256']=='5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240'")
replace("source_review['candidate_sha256']==before[0]['sha256']",
"source_review['candidate_sha256']=='ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'")
old_doc='READY source-bound V18 complete sender/root-index whole-phase caller last-use revision. The exact bcd order-preserved helper and d490 Root pure-metadata admission remain qualified INPUT-only prerequisites. Original V15 complete86 component success and source pins are retained as complete INPUT evidence. All original whole historical bodies, fresh EOF phases, full graph traces, aliases, namespaces, current predicates, failure-length checks, five build stages, physics and budgets remain required. The added same-SHA whole specs reread and all ecfd function bodies remain unchanged. Failed V17 build grants no successful combined/native/science evidence. This new V18 family has not executed prepare/build/whole INPUT/native/AAA/ABA; all six future business success pins remain None.'
new_doc='READY source-bound V19 complete sender/root-index PREP caller last-use candidate for final independent SOURCE review before installation. All 585e function bodies remain unchanged, including original complete PREP checks and V18 full INPUT phase corrections. Qualified bcd/d490 pure metadata protocol and actual V15 complete86 component remain original INPUT prerequisites. Complete historical seven-key bodies, graph scope, trace, nine coverage categories, fresh EOF reads, aliases, namespaces, physics and original budgets remain required. Actual V18 PREP failed above512 MiB and supplies no successful declaration, graph, build, INPUT or science credit. This V19 family has not executed any business or scientific validation; all six future combined/native success pins remain None. Root must pass the final independent SOURCE review before installation and fresh bounded PREP.'
replace(repr(old_doc),repr(new_doc))
replace('UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED','UNREADY_SOURCE_ONLY_V19_PREP_CALLER_LAST_USE_REVIEW_REQUIRED',2)
replace('READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY',2)
replace('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py',3)
# The P canonical path must remain V18; the prior replacement affects compile and output only because P used earlier an exact replacement.
replace("P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')",
"P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')")
replace("for layer in (read(RP),read(I17)):","for layer in (read(RP),read(I18),read(R17),read(I17)):")
replace('AXMAT_V18_READY_COMBINED_TWO_SOURCE_BINDINGS_INVERSE_V1','AXMAT_V19_READY_COMBINED_TWO_SOURCE_BINDINGS_INVERSE_V1')
replace('AXMAT_V18_COMPLETE_COMBINED_READY_SOURCE_BINDING_REPORT_V1','AXMAT_V19_COMPLETE_COMBINED_READY_SOURCE_BINDING_REPORT_V1')
replace("'independent_V18_source_review':before[6]","'independent_prior_V18_source_review':before[6],'independent_V19_source_review':None,'independent_V19_source_review_completed':False",2)
replace('all_70_function_class_definitions_byteexact_to_UNREADY_ecfd','all_70_function_class_definitions_byteexact_to_UNREADY_585e')
replace('READY_complete_inverse_to_ecfd_exact','READY_complete_inverse_to_585e_exact')
replace('complete_ancestry_inverse_chain_ecfd_feeb_82_0ea_exact','complete_ancestry_inverse_chain_585e_5c4b_ecfd_feeb_82_0ea_exact')
replace('no new V18 production graph, combined build/INPUT or native/AAA/ABA','no new V19 production graph, combined build/INPUT or native/AAA/ABA')
replace('existing require_ready V18 READY string','existing require_ready V19 READY string')
replace('all_function_bodies_exact_to_ecfd','all_function_bodies_exact_to_585e')
replace('source_inverse_chain_READY_ecfd_feeb_82_0ea_exact','source_inverse_chain_READY_585e_5c4b_ecfd_feeb_82_0ea_exact')
replace('fresh_V18_SOURCE_OUT_TERMINAL_HOST_namespaces_unchanged_from_UNREADY','fresh_V19_SOURCE_OUT_TERMINAL_HOST_namespaces_unchanged_from_UNREADY')
replace('Root review and install the exact READY candidate at its V18 FORMAL_FACTORY, retain this source inverse and actual prerequisite Q bindings, then independently execute a fresh original bounded V18 prepare once; success requires the observed new artifacts and terminal.',
'Root must complete the final independent V19 SOURCE review before installation. Only then install the exact READY candidate at its V19 FORMAL_FACTORY, retain this inverse and actual prerequisite Q bindings, and execute a fresh original bounded V19 PREP once; success requires observed new artifacts and closed terminal.')
replace('inverse_ecfd_feeb_82_0ea_exact','inverse_585e_5c4b_ecfd_feeb_82_0ea_exact')
inverse=text
for e in reversed(edits):
    assert inverse.count(e['new'])==e['occurrences'],e['new'][:100]
    inverse=inverse.replace(e['new'],e['old'])
assert inverse==old
compile(text,str(D/'generate_READY_binding.py'),'exec')
new=D/'generate_READY_binding.py'
with new.open('x') as f:f.write(text)
proof=dict(schema='AXMAT_V19_READY_GENERATOR_FINITE_INVERSE_TO_V18_V1',parent_path=str(P),parent_sha256=OLD_SHA,new_generator_path=str(new),new_generator_sha256=hashlib.sha256(text.encode()).hexdigest(),edits=edits,finite_change_count=len(edits),full_inverse_exact=True,source_compile_only=True,business_executed=False,project_or_ART_written=False)
with (D/'READY_generator_finite_inverse_proof.json').open('x') as f:json.dump(proof,f,indent=2);f.write('\n')
print(json.dumps(dict(source_only=True,generator=str(new),generator_sha256=proof['new_generator_sha256'],finite_change_count=len(edits),full_inverse_exact=True,business_executed=False)))

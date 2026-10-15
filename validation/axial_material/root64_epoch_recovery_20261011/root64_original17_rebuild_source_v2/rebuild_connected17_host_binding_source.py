from pathlib import Path
import hashlib
import json
import ast

HERE=Path(__file__).resolve().parent
OLD=HERE.with_name('root64_original17_rebuild_source_v1')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p.stat());b=p.read_bytes();z=ident(p.stat());assert a==z
    return dict(path=str(p),size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),identity=a)
def save(name,data):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb')as f:f.write(data.encode()if isinstance(data,str)else data)
    return pin(p)
original=OLD/'prepare_full_connected17_binding_and_host.py'
original_pin=pin(original);old=original.read_text();text=old;changes=[]
def splice(before,after):
    global text
    assert text.count(before)==1,(before[:100],text.count(before))
    text=text.replace(before,after,1);changes.append([before,after])
before=text
text=text.replace('test_ROOT64_full_connected17_v1','test_ROOT64_full_connected17_v2')
text=text.replace('axial-material-new-ROOT64-full-connected17-controls-20261012',
                  'axial-material-new-ROOT64-full-connected17-controls-v2-20261012')
text=text.replace('CURRENT_COMPLETE_ROOT64_CONNECTED17_FIXED_SOURCE_ORACLE_AND_COMMAND_BINDING_V1',
                  'CURRENT_COMPLETE_ROOT64_CONNECTED17_FIXED_SOURCE_ORACLE_AND_COMMAND_BINDING_V2')
text=text.replace('ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V1',
                  'ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V2')
changes.append([before,text])
splice('80a38a86e467e0b6595f28001e191ec56fe7143fd25e6000bcbb4e4fb038d312',
       '28e229ff6d1eb3d9f0b4d3ee0c1e96b207d5b1d417876f2f2653947bade45273')
splice("    PACKAGE/'COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json',",
'''    PACKAGE/'COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json',
    PACKAGE/'EXACT_UNFROZEN_V1_TO_V2_SOURCE_WRITER_DERIVATION.json',
    PACKAGE/'generate_full_connected17_source.py',
    PACKAGE/'rebuild_consumed_archive_admission_source.py',
    PACKAGE/'rebuild_connected17_host_binding_source.py',
''')
splice(" 'delete actual Native ROOT64-SEAL',", " 'delete actual consumed ARCHIVE/FLUX plane3 ROOT64-SEAL; owning admission must refuse before QBUILD and return no product',")
splice(" 'Native ROOT-FLUX64 group370 is written type2 instead of type4',",
       " 'actual consumed ARCHIVE/FLUX plane3 ROOT-FLUX64 group370 is type2 instead oftype4; owning Native admission refuses',")
splice(" 'Native FLUX32 mirror group370 region1 changes by one binary32 ulp',",
       " 'actual consumed ARCHIVE/FLUX plane3 FLUX32 mirror group370 region1 changes by one binary32 ulp; owning Native admission refuses',")
splice("    qr=3 if i in (1,17)else(0 if i in (3,4,5)else 1)",
       "    qr=3 if i in (1,17)else 1")
splice("        assertion_boundary='independent_host_full_EOF_SHA_seven_ID'if i==17 else 'actual_complete_module_calls',",
'''        assertion_boundary=('independent_host_full_EOF_SHA_seven_ID'if i==17 else
            'owning_connected_Native_admission_before_QBUILD_READ'if i in (3,4,5,15)else
            'actual_complete_module_calls'),''')
splice("        expected_explicit_q_read_calls=9 if i==17 else(6 if i==1 else(3 if i in (3,4,5)else 4)),",
       "        expected_explicit_q_read_calls=9 if i==17 else(6 if i==1 else(3 if i in (3,4,5,15)else 4)),")
splice("        expected_explicit_native_publish_calls=1,\n        require_refused_QBUILD_products_empty=upstream,",
'''        expected_explicit_native_publish_calls=4,
        expected_actual_archive_native_read_calls=51 if i==17 else(39 if i==1 else(
            33 if upstream or i in (3,4,5)else(28 if i==15 else 30))),
        expected_actual_archive_native_gate_calls=17 if i==17 else(13 if i==1 else(
            11 if upstream or i in (3,4,5)else 10)),
        expected_actual_archive_native_last_status=1 if i in (3,4,5,15)else 3,
        expected_actual_connected_q_build_calls=4 if upstream or i in (3,4,5)else 3,
        expected_actual_connected_q_read_calls=9 if i==17 else(6 if i==1 else 4),
        require_refused_QBUILD_products_empty=upstream or i in (3,4,5),''')
splice("        all32_NUSIGF_slots_nonzero=True,requested_rank=1,",
'''        all32_NUSIGF_slots_nonzero=True,requested_rank=1,
        archive_full_SYSTEM_list=True,consumed_archive_native_plane_identities=[1,2,3],
        archive_Native_PUBLISH_before_GLOBAL_PROJECT_Q=True,
        owning_archive_Native_gate_before_all_QBUILD_QREAD=True,
        frozen_Context_Q_internal_Native_or_external_auth_contract=False,''')
splice("                        'explicit_q_build_calls','explicit_q_read_calls','explicit_native_publish_calls'):",
'''                        'explicit_q_build_calls','explicit_q_read_calls','explicit_native_publish_calls',
                        'actual_archive_native_read_calls','actual_archive_native_gate_calls',
                        'actual_archive_native_last_status','actual_connected_q_build_calls',
                        'actual_connected_q_read_calls'):''')
splice('''Full positive path actually calls CAN WRITE, GLOBAL PUBLISH, PROJECT ARCHIVE,
all3plane QBUILD/QREAD and Native PUBLISH/READ/IMPORT. Synthetic values exercise
''','''Full positive path publishes each actual ARCHIVE/FLUX plane independently with
its real same-index TRACK/SYSTEM/MICROLIB2, RCON, plane=p/e0 before GLOBAL. The
owning connected caller actually Native READs all three consumed archive leaves
before GLOBAL, PROJECT, every QBUILD and QREAD; full XSM reopen uses the same gate.
CAN WRITE, GLOBAL PUBLISH, PROJECT ARCHIVE, all3plane QBUILD/QREAD and the retained
independent Native PUBLISH/READ/IMPORT are actual calls. Negative3/4/5 mutate the
consumed archive plane3, not the independent radial sibling; owning QBUILD refuses
and fresh outputs stay empty, then owning QREAD refuses with no loaded authority.
Frozen Context/Q modules do not themselves claim Native seal or external fullfile
authentication. The explicit owning gate is new test/caller Source, not hidden
qualification of an unchanged production caller. Synthetic values exercise
''')
ast.parse(text)
inverse=text
for before,after in reversed(changes):
    assert inverse.count(after)==1
    inverse=inverse.replace(after,before,1)
assert inverse==old
newpin=save('prepare_full_connected17_binding_and_host.py',text)
retained=save('unqualified_v1_exact_writer/prepare_full_connected17_binding_and_host.py',old)
save('EXACT_UNFROZEN_V1_TO_V2_BINDING_WRITER_DERIVATION.json',json.dumps(dict(
    original=original_pin,retained=retained,new=newpin,literal_changes=changes,
    complete_inverse_matches=True,old_v1_archive_lineage_incomplete=True,
    compiler_or_native_executed=False),indent=2)+'\n')
print(json.dumps(dict(new_host_binding_writer=newpin,original_v1_writer_unchanged=pin(original)==original_pin,
    complete_inverse=True,compiler_or_native_executed=False)))

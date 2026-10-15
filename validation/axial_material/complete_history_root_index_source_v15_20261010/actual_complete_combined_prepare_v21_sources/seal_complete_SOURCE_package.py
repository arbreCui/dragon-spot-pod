"""Complete fresh TMP SOURCE seal, including genuine postclose metadata-writer SOURCE."""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

BASE=Path('/private/tmp/axmat_v21_COMPLETE_READY_runtime_genuine_PREP_closed_metadata_SOURCE_20261010_syx41')
MANIFEST=BASE/'sealed_complete_SOURCE_manifest.json'


def identity(st):
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]


def read_source(path):
    before=path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or path.resolve()!=path:
        raise ValueError('Regular non-symlink singlelink SOURCE file required')
    with path.open('rb') as stream:
        if identity(os.fstat(stream.fileno()))!=identity(before):
            raise ValueError('SOURCE changed before reading')
        data=stream.read()
        if identity(os.fstat(stream.fileno()))!=identity(before):
            raise ValueError('SOURCE changed during full reading')
    if identity(path.lstat())!=identity(before) or len(data)!=before.st_size:
        raise ValueError('SOURCE full EOF SHA7ID changed')
    return data,dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),
                     size_bytes=len(data),identity=identity(before))


def inventory():
    files=[];directories=[]
    for folder,dirs,names in os.walk(BASE,followlinks=False):
        folder=Path(folder)
        if not stat.S_ISDIR(folder.lstat().st_mode):
            raise ValueError('Regular SOURCE directory required')
        directories.append(str(folder.relative_to(BASE)))
        for name in dirs:
            if not stat.S_ISDIR((folder/name).lstat().st_mode):
                raise ValueError('No symlink SOURCE directory permitted')
        for name in names:
            path=folder/name
            if path!=MANIFEST:files.append(path)
    return sorted(files),sorted(directories)


def main():
    if MANIFEST.exists():raise ValueError('Only one fresh complete SOURCE seal permitted')
    if BASE.resolve()!=BASE or BASE.parent!=Path('/private/tmp'):
        raise ValueError('Only this fixed TMP SOURCE package may be sealed')
    writer_root=BASE/'metadata_writer_SOURCE_binding'
    report=json.loads((writer_root/'SOURCE_REVIEW.json').read_bytes())
    proof=json.loads((writer_root/'full_metadata_writer_SOURCE_inverse.json').read_bytes())
    if report['all_checks_typed_true'] is not True or report['blockers']!=[]:
        raise ValueError('Writer SOURCE review did not pass')
    if any(check['value'] is not True for check in report['checks']):
        raise ValueError('Each writer SOURCE check must be exact bool true')
    writer,writer_pin=read_source(writer_root/'write_actual_prepare_terminal.py')
    if writer_pin!=proof['candidate'] or writer_pin['sha256']!='9dc8823bb3c5433d5cac464720e3f8d8da3d631ac0b4eaaef2d6f3bb83ba866d':
        raise ValueError('Fixed metadata writer SOURCE differs')
    original,original_pin=read_source(writer_root/'original_metadata_writer_full_SOURCE.txt')
    if original_pin['sha256']!='af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539':
        raise ValueError('Full original writer SOURCE differs')
    restored=writer.decode()
    if len(proof['complete_forward_hunks'])!=12:
        raise ValueError('Writer SOURCE finite retarget scope differs')
    for hunk in reversed(proof['complete_forward_hunks']):
        if restored.count(hunk['new'])!=1:raise ValueError('Unique full writer inverse required')
        restored=restored.replace(hunk['new'],hunk['old'],1)
    if restored.encode()!=original or ast.dump(ast.parse(restored),include_attributes=False)!=ast.dump(ast.parse(original.decode()),include_attributes=False):
        raise ValueError('Full writer byte or AST inverse differs')
    retained=BASE/'sealed_READY_runtime_and_PREP_binding'
    old_manifest_bytes,old_manifest_pin=read_source(retained/'sealed_SOURCE_manifest.json')
    if old_manifest_pin['sha256']!='5b8653db81265f06eddbe6e9fb9e66c59dacbb8608537a69b4ca58244cbf30d3':
        raise ValueError('Original complete READY SOURCE seal was not retained exact')
    old_manifest=json.loads(old_manifest_bytes)
    expected_retained=set(old_manifest['full_member_inventory'])|{'sealed_SOURCE_manifest.json'}
    actual_retained={str(path.relative_to(retained)) for path in retained.rglob('*') if path.is_file()}
    if expected_retained!=actual_retained:
        raise ValueError('Full original READY SOURCE archive member inventory differs')
    for relative,old_pin in old_manifest['full_member_inventory'].items():
        _,copied_pin=read_source(retained/relative)
        expected_copy=report['complete_original_SOURCE_members_and_copy_pins'][relative]['copy']
        if copied_pin!=expected_copy or copied_pin['sha256']!=old_pin['sha256'] or copied_pin['size_bytes']!=old_pin['size_bytes']:
            raise ValueError('Complete original READY SOURCE member bytes or new copy identity changed')
    fixed={
      'sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py':'023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',
      'sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/combined_prepare_host.py':'776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405',
      'metadata_writer_SOURCE_binding/write_actual_prepare_terminal.py':'9dc8823bb3c5433d5cac464720e3f8d8da3d631ac0b4eaaef2d6f3bb83ba866d',
    }
    files_before,dirs_before=inventory()
    before={str(path.relative_to(BASE)):read_source(path)[1] for path in files_before}
    if any(before[relative]['sha256']!=sha for relative,sha in fixed.items()):
        raise ValueError('Fixed complete SOURCE candidate bytes differ')
    files_after,dirs_after=inventory()
    after={str(path.relative_to(BASE)):read_source(path)[1] for path in files_after}
    if before!=after or dirs_before!=dirs_after:
        raise ValueError('Whole SOURCE namespace or EOF SHA7ID changed before sealing')
    document={
      'schema':'AXMAT_V21_COMPLETE_READY_RUNTIME_GENUINE_PREP_POSTCLOSE_METADATA_SOURCE_SEAL_V1',
      'status':'SEALED_COMPLETE_SOURCE_READY_UNINSTALLED_NO_ACTUAL_PREP_OR_BUILD_CREDIT',
      'package_path':str(BASE),'members_excluding_this_manifest':len(before),
      'bytes_excluding_this_manifest':sum(pin['size_bytes'] for pin in before.values()),
      'full_file_inventory':before,'full_directory_relative_paths':dirs_before,
      'all_full_EOF_SHA256_exact7ID_before_after_unchanged':True,
      'original_sealed_READY_package_all_members_retained_byteexact':True,
      'runtime_4hunk_full_inverse_and_all70_definition_bytes_retained':True,
      'genuine_normal_PREP_host_11hunk_full_inverse_original_caps_retained':True,
      'postclose_metadata_writer_12hunk_full_byte_and_AST_inverse_to_af0c':True,
      'postclose_metadata_writer_all7_definition_complete_inverses_and_original_Call_If_Raise_Assert_Return_retained':True,
      'writer_source_checks':len(report['checks']),
      'writer_SOURCE_generation_actual_tool_chunk':'edd798',
      'writer_SOURCE_generation_exact_integer_exit_code':0,
      'fixed_actual_helper_joint_Q_SHA':'29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2',
      'original_business_caps_and_complete_input_graph_trace_source_namespace_scope_unchanged':True,
      'six_unknown_future_business_pins_all_None':True,
      'metadata_writer_requires_future_true_typed_EXIT0_closed_genuine_PREP':True,
      'metadata_writer_must_be_archived_before_D_freeze':True,
      'SOURCE_check_failures_preserved_without_business_execution':True,
      'API_guard_business_executed':False,'metadata_writer_executed':False,
      'ART_graph_numeric_payload_read':False,'canonical_or_frozen_namespace_written':False,
      'installed':False,'actual_PREP_build_INPUT_native_AAA_ABA_success_claimed':False,
    }
    with MANIFEST.open('x') as stream:
        json.dump(document,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n')
    _,manifest_pin=read_source(MANIFEST)
    final_files,final_dirs=inventory()
    final={str(path.relative_to(BASE)):read_source(path)[1] for path in final_files}
    if before!=final or dirs_before!=final_dirs or read_source(MANIFEST)[1]!=manifest_pin:
        raise ValueError('Complete SOURCE seal changed after creation')
    print(json.dumps({'status':document['status'],'manifest':manifest_pin,
                      'members':len(before),'member_bytes':document['bytes_excluding_this_manifest'],
                      'writer_checks':len(report['checks']),
                      'all_full_EOF_SHA7ID_before_after_exact':True,
                      'API_guard_business_executed':False,'writer_executed':False,'installed':False}))


if __name__=='__main__':main()

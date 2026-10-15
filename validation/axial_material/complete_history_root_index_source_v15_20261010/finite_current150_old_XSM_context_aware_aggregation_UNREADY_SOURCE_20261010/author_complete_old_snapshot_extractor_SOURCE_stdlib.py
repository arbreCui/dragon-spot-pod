"""Derive only Source; no XSM/native/helper/candidate execution."""
import ast,difflib,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
source=P/'COMPLETE_FIXED_PARENT_SOURCE/FINITE_ACTUAL_NATIVE_V23_SOURCE_META/Root_bound_complete_native_checker.py'
old=source.read_text();new=old
new=new.replace("SOURCE_STATUS = 'ROOT_BOUND_SOURCE_ONLY_NOT_QUALIFIED'","SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'")
new=new.replace("ROOT_BOUND_BINDING_SHA256 = '765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87'","ROOT_BOUND_BINDING_SHA256 = None")
anchor="        require(total < CAPS['joint_archive_bytes'], 'full joint H/O/C/D/E exceeds original2GiB')\n"
assert new.count(anchor)==1
new=new.replace(anchor,"""        unlinked={}
        for name in os.listdir('/dev/fd'):
            try:s=os.fstat(int(name))
            except (ValueError,OSError):continue
            if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[(s.st_dev,s.st_ino)]=s.st_size
        total+=sum(unlinked.values())
"""+anchor)
new=new[:new.index('def main():')]+r'''def main():
    import sys
    require(SOURCE_STATUS=='READY_ROOT_BOUND_SOURCE_ONLY'and type(ROOT_BOUND_BINDING_SHA256)is str,
            'UNREADY complete old-XSM Source refuses payload read or writes')
    require(not sys.flags.optimize and sys.getprofile()is None,'original unprofiled child')
    require(all(os.environ.get(k)=='1'for k in
        ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')),
        'original complete single-thread environment')
    parser=argparse.ArgumentParser()
    parser.add_argument('--binding',required=True)
    parser.add_argument('--binding-sha256',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--expected-parent-pid',required=True,type=int)
    args=parser.parse_args()
    require(os.getppid()==args.expected_parent_pid,'actual unchanged genuine parent PID')
    binding_pin=pin(Path(args.binding).absolute())
    require(binding_pin['sha256']==args.binding_sha256==ROOT_BOUND_BINDING_SHA256,'actual Root old-XSM binding bytes')
    binding=strict_json(Path(args.binding).read_bytes())
    require(binding['schema']=='ROOT_ACTUAL_COMPLETE_OBSERVATION_XSM_EXTRACTION_BINDING_V1'and
            binding['Root_only_actual_execution']is True and binding['new_qualification_sha256']is None,
            'new exact extraction family, no qualification transplanted')
    require(type(binding['original_caps'])is dict and set(binding['original_caps'])==set(CAPS)and
            all(type(x)is int for x in binding['original_caps'].values())and binding['original_caps']==CAPS,
            'all original typed caps')
    require(binding['state_order']==['A','B']and set(binding['complete_state_snapshot_inputs'])=={'A','B'},'full serial states')
    output=Path(args.output_dir).absolute()
    require(not os.path.lexists(output),'fresh complete snapshot extraction, no retry')
    budget=Budget(output,binding['joint_archive_roots'])
    exact_pin(binding['actual_observation_manifest_pin'])
    exact_pin(binding['independent_observation_Source_admission_pin'])
    all_inputs=binding['original129_input_pins']+binding['additional_actual_observation_input_pins']
    require(len(binding['original129_input_pins'])==129 and len({p['path']for p in all_inputs})==len(all_inputs),
            'full original129 preserved plus all actual observation inputs')
    for p in all_inputs:budget.check();exact_pin(p)
    output.mkdir();sqltemp=output/'sqlite_file_temp';sqltemp.mkdir()
    os.environ['SQLITE_TMPDIR']=str(sqltemp)
    states={};errors=[]
    for state in ('A','B'):
        state_folder=output/state;state_folder.mkdir();reports=[]
        inputs=binding['complete_state_snapshot_inputs'][state]
        require(type(inputs)is list and inputs,'complete observed snapshot list')
        previous=0
        for item in inputs:
            require(type(item)is dict and set(item)=={'event','role','root_prefix','input_pin'}and
                type(item['event'])is int and item['event']>=previous and type(item['role'])is str,
                'all original event-order snapshots, no selection or sorting')
            previous=item['event'];prefix=item['root_prefix']
            require((item['role']in('oldmacro-pre-LIBMIX','oldmacro-LIBDEN','postmacro-LIBMIX')and prefix==['MACROLIB'])or
                (item['role']=='final-complete-micro'and prefix==[]),'exact observer complete tree prefix, no invented root node')
            pin_shape(item['input_pin']);require(item['input_pin']in all_inputs,'each entire actual XSM protected')
            exact_pin(item['input_pin']);budget.check()
            folder=state_folder/(str(item['event']).zfill(6)+'_'+item['role']);folder.mkdir()
            rows=DiskRecords(folder/'complete_native_original_path_index.sqlite')
            snapshot=None
            try:
                with Path(item['input_pin']['path']).open('rb')as src,\
                    (folder/'complete_native_physical_directory_slots.jsonl').open('x')as physical,\
                    (folder/'complete_native_original_value_bytes.bin').open('xb')as pool:
                    require(identity(os.fstat(src.fileno()))==item['input_pin']['identity'],'actual opened snapshot7ID')
                    native=XSM(ReadOnlyFileBytes(src),physical,pool,budget,rows)
                    # Observer macro-only XSM root is already its MACROLIB.
                    # Prefix labels actual provenance; no fake root row/value.
                    native.walk_table(native.root,tuple(prefix),());rows.checkpoint()
                    records=len(rows)
                    with(folder/'complete_native_logical_record_inventory.jsonl').open('x')as index:
                        for row in rows.iter_rows():budget.check();line_json(index,row)
                    with(folder/'complete_native_xsmnxt_export_record_order.jsonl').open('x')as api:
                        for row in rows.iter_rows(api=True):budget.check();line_json(api,row)
                    require(identity(os.fstat(src.fileno()))==item['input_pin']['identity'],'actual snapshot unchanged at full traversal')
                    snapshot=dict(state=state,event=item['event'],role=item['role'],root_prefix=prefix,
                        input_pin=item['input_pin'],complete_records=records,complete_directories=native.directory_count,
                        complete_extents=native.extent_count,all_original_types_counts_words_and_physical_API_orders_saved=True,
                        ASCII_used_or_invented=False,original_RAM_bits_qualified=False,new_qualification_sha256=None)
            finally:rows.close()
            exact_pin(item['input_pin']);budget.check()
            require(snapshot is not None,'complete snapshot extraction missing, no fake completion')
            snapshot['paired_SQLite_pin']=pin(folder/'complete_native_original_path_index.sqlite')
            snapshot['paired_original_pool_pin']=pin(folder/'complete_native_original_value_bytes.bin')
            snapshot['all_output_file_pins']=[pin(p)for p in sorted(folder.rglob('*'))if p.is_file()]
            reports.append(snapshot)
        # Every XSM fd/pool/index is closed before next snapshot/state.
        states[state]=reports
    for p in all_inputs:budget.check();exact_pin(p)
    exact_pin(binding_pin);budget.check()
    report=dict(schema='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1',
        actual_child_PID=os.getpid(),actual_parent_PID=os.getppid(),states=states,original_caps=CAPS,
        input_sources=all_inputs,all_complete_state_scope_retained=True,all_handles_closed_before_B=True,
        all_observed_native_tree_words_and_orders_preserved=True,genuine_supervisor_watch_verified_here=False,
        complete_aggregation_qualified=False,new_qualification_sha256=None,**FALSE)
    path=output/'ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_REPORT.json'
    with path.open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status='ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_EVIDENCE_ONLY',report=pin(path)),allow_nan=False),flush=True)
    # Source only until complete new malformed/fullprefix/resource controls and
    # actual Root CLOSED receipt independently qualify this new extraction.
    raise SystemExit(2)


if __name__=='__main__':main()
'''
ast.parse(new)
a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
h=[dict(tag=t,old_start0=i,old_end0=j,new_start0=k,new_end0=l,old_full_lines=a[i:j],new_full_lines=b[k:l])for t,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()if t!='equal']
back=b[:]
for x in reversed(h):
    assert back[x['new_start0']:x['new_end0']]==x['new_full_lines'];back[x['new_start0']:x['new_end0']]=x['old_full_lines']
assert ''.join(back)==old
(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py').write_text(new)
(P/'COMPLETE_V23_OLD_XSM_EXTRACTION_SOURCE_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_V23_OLD_XSM_EXTRACTION_SOURCE_FULL_INVERSE_V1',source_only=True,
    original_source=str(source),original_SHA256=hashlib.sha256(old.encode()).hexdigest(),candidate_SHA256=hashlib.sha256(new.encode()).hexdigest(),
    complete_zero_based_hunks=h,all_original_V23_Source_bytes_restored=True,
    all_original_XSM_ReadOnlyFileBytes_DiskRecords_classes_bytes_AST_unchanged=True,only_Budget_adds_unlinked_bytes=True,
    actual_old_XSM_extraction=None,actual_new_controls=None,new_qualification=None),indent=2)+'\n')
print(json.dumps(dict(source_only=True,full_inverse_hunks=len(h),old_XSM_Source_SHA256=hashlib.sha256(new.encode()).hexdigest(),candidate_executed=False)))

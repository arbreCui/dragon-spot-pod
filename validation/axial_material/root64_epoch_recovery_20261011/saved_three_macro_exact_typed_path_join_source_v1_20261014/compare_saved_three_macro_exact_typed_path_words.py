"""One bounded comparison of existing typed SQLite indices and original byte pools."""
import argparse,hashlib,importlib.util,itertools,json,os,sys
from pathlib import Path
BASE=Path(__file__).absolute().parent
from current_material_lineage_evidence import Budget,admit_owning_stage,check,pin,read,require,strict,FALSE
import saved_native_data_access_adapter as adapter
def current7(expected):
 p=Path(expected['path']);s=p.lstat();require(not any(a.is_symlink()for a in(p,*p.parents))and[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==expected['identity'],'original physical archive current7 only; no new decode')
def under(saved,prefix):
 for value in saved.iter_all():
  if tuple(value['record']['path'][:len(prefix)])==prefix:yield value
def keys(saved,prefix):
 result=set()
 for value in under(saved,prefix):
  original=value['record']['path'];canonical=original if prefix==('MACROLIB',)else original[2:]
  require(canonical[:1]==['MACROLIB'],'only exact native MICROLIB2,1,MACROLIB prefix normalized')
  key=adapter.path_key(canonical);require(key not in result,'unique canonical typed path, no record overwritten');result.add(key)
 return result
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);args=ap.parse_args()
 require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None,'genuine owning parent/unprofiled unoptimized child')
 require(all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'original single thread')
 bindingpin=strict(args.binding_pin);binding=read(bindingpin,lambda:None)
 require(binding['schema']=='ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_BINDING_V1','one exact saved-pair operation')
 budget=Budget(binding['joint_archive_roots'],binding['explicit_cumulative_metadata_file_pins']);budget.check()
 for p in binding['source_file_pins']:check(p,budget.check)
 out=Path(binding['child_output_directory']);require(out.is_dir()and not any(out.iterdir()),'fresh owned comparison subdirectory')
 temp=out/'sqlite_temp';temp.mkdir();pair=binding['observed_pair']
 saved=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget.check);reports=[]
 try:
  observed_keys=keys(saved,('MACROLIB',));require(len(observed_keys)==binding['expected_macro_record_count'],'all original19620 records including typed root')
  for plane,row in enumerate(binding['native_pairs'],1):
   require(row['plane']==plane,'original three plane order');producer=binding['original_native_producers'][plane-1]
   require(row['archive_pin']==producer['archive_pin'],'same original physical producer')
   current7(row['archive_pin']);admit_owning_stage(producer['actual_report_pin'],producer['actual_solve_label'],producer['actual_solve_command'],budget.check)
   native=adapter.SavedNativeInput(row['sqlite_pin'],row['native_pool_pin'],temp,budget.check)
   try:
    native_keys=keys(native,('MICROLIB2',1,'MACROLIB'))
    require(native_keys==observed_keys,'complete bidirectional typed path inventories, no dropped or invented record')
    count=words=word_mismatches=metadata_mismatches=0;detail=out/('A'+str(plane)+'_canonical_macro_comparison.jsonl')
    with detail.open('x')as output:
     # Preserve the observed API/physical order; lookup does not sort either archive.
     for value in under(saved,('MACROLIB',)):
      budget.check();a=value['record'];right_path=['MICROLIB2',1]+a['path'];b=native.row(right_path)
      require(b is not None,'exact typed native path lookup')
      right_info=native.db.execute('SELECT ordinal,api_key FROM records WHERE key=?',(adapter.path_key(right_path),)).fetchone();require(right_info is not None,'original native physical/API ordinal retained')
      meta=a['path_types']==b['path_types'][2:]and all(a[k]==b[k]for k in('kind','declared_count','original_word_count'))
      nwords=ndiff=0
      for aa,bb in itertools.zip_longest(saved.iter_raw(a),native.iter_raw(b),fillvalue=b''):
       budget.check();nwords+=max(len(aa),len(bb))//4
       ndiff+=sum(aa[i:i+4]!=bb[i:i+4]for i in range(0,max(len(aa),len(bb)),4))
      count+=1;words+=nwords;word_mismatches+=ndiff;metadata_mismatches+=int(not meta)
      item=dict(canonical_path=a['path'],kind=a['kind'],declared_count=a['declared_count'],original_word_count=a['original_word_count'],metadata_equal=meta,raw_word_mismatches=ndiff,compared_words=nwords,observation_payload_SHA=a['native_payload_sha256'],archive_payload_SHA=b['native_payload_sha256'],original_observation_ordinal=value['physical_ordinal'],original_observation_api_key=value['api_key'],original_archive_ordinal=right_info[0],original_archive_api_key=right_info[1])
      output.write(json.dumps(item,separators=(',',':'),allow_nan=False)+'\n')
     output.flush();os.fsync(output.fileno())
    require(count==len(observed_keys)==len(native_keys),'all records compared once, including root')
    current7(row['archive_pin']);reports.append(dict(plane=plane,compared_all_macro_records=count,compared_original_payload_words=words,raw_word_mismatches=word_mismatches,metadata_mismatches=metadata_mismatches,path_sets_equal=True,all_original_records_and_typed_root_preserved=True,original_archive_not_redecoded=True,original_orders_not_sorted_or_rewritten=True,detail_pin=pin(detail,budget.check),native_sqlite_pin=row['sqlite_pin'],native_pool_pin=row['native_pool_pin']))
   finally:native.close()
 finally:saved.close()
 report=out/'ACTUAL_SAVED_THREE_MACRO_CANONICAL_PATH_COMPARISONS.json'
 value=dict(schema='ACTUAL_SAVED_THREE_MACRO_CANONICAL_PATH_RAW_WORD_COMPARISON_V1',original_failed_compare_authority_pins=binding['original_failed_compare_authority_pins'],original_Root_exit_code_retained=1,original_positional_mismatch_report_not_modified=True,observed_pair=pair,comparisons=reports,all_raw_word_mismatches=sum(r['raw_word_mismatches']for r in reports),all_metadata_mismatches=sum(r['metadata_mismatches']for r in reports),all_three_original_producer_seals_preserved=True,comparison_contract='EXACT_TYPED_FULL_PATH_KIND_COUNT_WORDS_AND_ALL_RAW_BYTES',**FALSE)
 with report.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 check(bindingpin,budget.check);budget.check();print(json.dumps(dict(status='ACTUAL_SAVED_THREE_TYPED_PATH_COMPARISONS_CLOSED_ONLY_EXIT2',report=pin(report,budget.check),**FALSE)),flush=True);raise SystemExit(2)
if __name__=='__main__':main()

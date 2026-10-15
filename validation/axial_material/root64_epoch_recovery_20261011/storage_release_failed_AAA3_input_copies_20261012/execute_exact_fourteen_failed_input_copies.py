"""Exact closed-failure copied input release; original inputs/results retained."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE=Path(__file__).resolve().parent
COMMON=REC/'storage_release_20261012/storage_release_common.py'
spec=importlib.util.spec_from_file_location('original_exact_release_guards',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
NAMES=['axial_macro.xsm','axial_track.xsm','basis.xsm','global_rcon.xsm',
       'native_A1.xsm','native_A2.xsm','native_A3.xsm']
BRANCHES=[ROOT/'validation/artifacts'/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v)
          for v in ['v1','v2']]
EXPECTED_BYTES=998914456
MANIFEST=PACKAGE/'EXACT_14_CANDIDATE_MANIFEST_FROZEN_V3_PROTECTED.json'
RECEIPT=PACKAGE/'ACTUAL_EXACT_FOURTEEN_RELEASE_EXECUTION_RECEIPT.json'

def inventory():
    out=[]
    for branch in BRANCHES:
        files={};links={};dirs={};stack=[branch]
        while stack:
            p=stack.pop();c.ancestors(p);s=p.lstat()
            if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary closed branch directory required')
            dirs[str(p)]=c.identity(s)
            fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                with os.scandir(fd)as entries:
                    for entry in entries:
                        q=p/entry.name;s=entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(s.st_mode):stack.append(q)
                        elif stat.S_ISREG(s.st_mode):files[str(q)]=c.identity(s)
                        elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=c.identity(s),target=os.readlink(q))
                        else:raise RuntimeError('unexpected special file in closed failed branch')
            finally:os.close(fd)
            c.guard()
        out.append(dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--manifest-seven-id',required=True);args=ap.parse_args()
    mr=c.pin(MANIFEST)
    if mr['sha256']!=args.manifest_sha256 or mr['identity']!=json.loads(args.manifest_seven_id):
        raise RuntimeError('Root selected complete durable manifest SHA and exact7ID required')
    m=c.read_pinned_json(mr)
    if m['schema']!='INDEPENDENT_EXACT_14_CLOSED_AAA3_FAILED_INPUT_COPY_CANDIDATE_MANIFEST_FROZEN_V3_PROTECTED_V2' or \
       m['action_executed']is not False or m['unlink_executed']is not False or \
       m['target_count']!=14 or m['total_target_logical_bytes']!=EXPECTED_BYTES:
        raise RuntimeError('exact unexecuted closed-failure copied-input manifest required')
    expected=sorted(str(b/'AAA'/n)for b in BRANCHES for n in NAMES)
    targets=m['target_full_EOF_pins'];kept=m['retained_ordinary_file_full_EOF_pins']
    if sorted(x['path']for x in targets)!=expected or sum(x['size_bytes']for x in targets)!=EXPECTED_BYTES:
        raise RuntimeError('only the literal fourteen copied input XSM files are authorized')
    protected=m['current_frozen_original_and_producer_protected_full_EOF_pins']
    extra=m['closed_failure_report_pins']+m['true_terminal_receipt_pins']+m['source_protection_helper_pins']
    for row in targets+kept+protected+extra:c.same(row)
    if inventory()!=m['complete_closed_before_inventories']:
        raise RuntimeError('complete closed failed branches changed before Root release')
    protected_paths={x['path']for x in protected};protected_ids={tuple(x['identity'][:2])for x in protected}
    for row in targets:
        if row['path']in protected_paths or tuple(row['identity'][:2])in protected_ids or \
           not stat.S_ISREG(row['identity'][2])or row['identity'][3]!=1:
            raise RuntimeError('target intersects current/frozen dependencies or is not a single-link file')
    for prov in m['original_source_input_provenance']:
        c.same(prov['original_input_full_pin'])
        if prov['original_input_full_pin']['sha256']!=prov['candidate_full_pin']['sha256']:
            raise RuntimeError('candidate must be a complete byte-identical failed copy of retained original input')
    reports=[c.read_pinned_json(x)for x in m['closed_failure_report_pins']]
    if [len(x['records'])for x in reports]!=[2,3]or \
       any(x['status']!='FAILED_UNQUALIFIED_NO_RETRY'or x['failure']is None or x['actual_terminal']is not None
           for x in reports):raise RuntimeError('both actual failures must remain closed without positive terminal')
    if RECEIPT.exists()or RECEIPT.with_suffix('.pending').exists():raise RuntimeError('no receipt overwrite or automatic deletion retry')
    before=c.budget();source=c.pin(Path(__file__));common=c.pin(COMMON)
    r=dict(schema='ROOT_EXACT_FOURTEEN_CLOSED_AAA3_FAILED_INPUT_COPY_RELEASE_ACTUAL_V1',
           manifest_pin=mr,execution_Source_pin=source,original_guard_Source_pin=common,
           original_budget_before=before,started_unix=time.time(),status='EXECUTING',deletion_records=[],
           all_full_EOF_preflight_verified=True,original_caps_unchanged=True,scientific_computation_started=False,
           retained_original_input_and_result_docs=True,current_frozen_v3_dependency_closure_disjoint=True)
    c.write_new(RECEIPT,r)
    try:
        for row in targets:
            c.same(row);p=Path(row['path']);fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if c.identity(os.stat(p.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:
                    raise RuntimeError('target changed immediately before exact unlink')
                os.unlink(p.name,dir_fd=fd)
            finally:os.close(fd)
            if os.path.lexists(p):raise RuntimeError('target reappeared after unlink')
            r['deletion_records'].append(dict(original_full_EOF_pin=row,confirmed_absent=True,
                action='UNLINK_EXACT_FROZEN_ORDINARY_FAILED_INPUT_COPY',unix=time.time()))
            c.update_owned_receipt(RECEIPT,r)
        for row in kept+protected+extra+[mr,source,common]:c.same(row)
        after_inventory=inventory();names={x['path']for x in targets}
        for before_i,after_i,branch in zip(m['complete_closed_before_inventories'],after_inventory,BRANCHES):
            if after_i['ordinary_file_identities']!={p:i for p,i in before_i['ordinary_file_identities'].items()if p not in names}or \
               after_i['symlinks']!=before_i['symlinks']or \
               set(after_i['directory_identities'])!=set(before_i['directory_identities']):
                raise RuntimeError('unexpected retained branch inventory change')
            for p,i in before_i['directory_identities'].items():
                observed=after_i['directory_identities'][p]
                if p==str(branch/'AAA'):
                    if observed[:4]!=i[:4]:raise RuntimeError('parent directory identity changed beyond natural unlink timestamps')
                elif observed!=i:raise RuntimeError('untouched directory identity changed')
        after=c.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=EXPECTED_BYTES or before['regular_files']-after['regular_files']!=14:
            raise RuntimeError('logical history changed beyond exact14; no concurrent artifact writer permitted')
        r.update(status='EXACT_FOURTEEN_FAILED_INPUT_COPY_RELEASE_AND_RETENTION_VERIFIED',
                 deleted_file_count=14,logical_bytes_released=EXPECTED_BYTES,original_budget_after=after,
                 retained_other_closed_files_full_EOF_count=len(kept),current_dependency_full_EOF_count=len(protected),
                 all_retained_files_full_EOF_SHA_and7ID_unchanged=True,
                 parent_directory_unlink_timestamp_changes_only=True,completed_unix=time.time(),
                 goal_complete=False,pipeline_or_physical_qualification=False)
    except BaseException as exc:
        r.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(exc),completed_unix=time.time())
        c.update_owned_receipt(RECEIPT,r);raise
    c.update_owned_receipt(RECEIPT,r)
    print(json.dumps(dict(status=r['status'],deleted_files=14,logical_bytes_released=EXPECTED_BYTES,
                         receipt_pin=c.pin(RECEIPT),initial_reserve_admitted=after['original_initial_reserve_admitted'],
                         remaining_after_original_initial_reserves_bytes=after['remaining_after_original_initial_reserves_bytes'])))

if __name__=='__main__':main()

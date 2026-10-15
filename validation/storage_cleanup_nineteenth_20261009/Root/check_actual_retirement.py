from pathlib import Path
import json, runpy, subprocess, os

OUT = Path('/private/tmp/spot_storage_nineteenth_root_20261009')
review = runpy.run_path(str(OUT / 'prepare_review.py'), run_name='pure_metadata_helpers_only')
sha, identity, inventory = review['sha'], review['identity'], review['inventory']

def main():
    plan = json.loads((OUT / 'fixed_candidate_plan.json').read_text())
    result = json.loads((OUT / 'cleanup_result.json').read_text())
    before = json.loads((OUT / 'protected_before.json').read_text())
    assert sha(OUT/'fixed_candidate_plan.json') == result['plan_sha256'] == before['candidate_plan_sha256']
    assert result['status'] == 'COMPLETE_EXACT_18_EARLY_STATES_AND_18_DEPENDENT_LINKS_RETIREMENT'
    assert result['deleted_regular'] == [x['path'] for x in plan['regular']]
    assert result['deleted_symlinks'] == [x['path'] for x in plan['symlinks']]
    selected = {x['path'] for x in plan['regular'] + plan['symlinks']}
    for s in selected:
        assert not os.path.lexists(s), ('selected path still exists', s)
    after = inventory(selected)
    assert after['counts'] == before['counts'] and after['fingerprints'] == before['fingerprints'], 'unselected project remainder changed'
    for key in ['current_binding', 'current_graph']:
        pin = plan[key]
        assert sha(Path(pin['path'])) == pin['sha256']
    for s, digest in {**before['control_document_pins'], **plan['stage_documents']}.items():
        assert sha(Path(s)) == digest
    for x in plan['kept_last_three_closed_and_last_two_parent_links']:
        p = Path(x['path'])
        assert identity(p) == x['identity']
        if 'sha256' in x:
            assert sha(p) == x['sha256']
        else:
            assert os.readlink(p) == x['link_text'] and str(p.resolve()) == x['target'] and p.resolve().is_file()
    after['control_document_pins'] = before['control_document_pins']
    after['du_kib'] = int(subprocess.check_output(['du', '-sk', str(review['ROOT'])], text=True).split()[0])
    (OUT/'protected_after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2)+'\n')
    report = {'status': 'PASS_EXACT_DELETION_WHOLE_REMAINDER_AND_FINAL_STATE_PRESERVATION', 'deleted_regular': 18, 'deleted_symlinks': 18, 'protected_counts': after['counts'], 'whole_protected_fingerprints_same': True, 'current_binding_and_graph_bytes_same': True, 'stage_and_control_documents_whole_sha_same': True, 'last_three_closed_and_last_two_parent_links_same_and_valid': True, 'before_du_kib': before['du_kib'], 'after_du_kib': after['du_kib'], 'measured_decrease_gib': (before['du_kib']-after['du_kib'])/2**20, 'selected_original_allocated_gib': plan['allocated_bytes']/2**30, 'project_scientific_source_inputs_thresholds_progress_modified': False, 'business_executed': False, 'scientific_qualification': False}
    (OUT/'postcheck_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()

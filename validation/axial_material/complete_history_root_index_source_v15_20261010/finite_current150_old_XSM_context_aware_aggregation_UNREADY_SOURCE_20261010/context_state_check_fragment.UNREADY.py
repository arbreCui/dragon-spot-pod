"""Root-only context aggregation entry, insertion-only Source fragment."""
def context_state_check(adapter,binding,state,output,budget):
    source=binding['states'][state];root=output/state;root.mkdir();temp=root/'sqlite_file_temp';temp.mkdir()
    saved=adapter.SavedNativeInput(source['sqlite_pin'],source['native_pool_pin'],temp,budget)
    opened=[];evidence=None;state_report=None
    try:
        evidence=DiskEvidence(root,saved,budget,state);evidence.inventory()
        context=adapter.capture_complete_fixed_context(saved);write_new(root/'ACTUAL_COMPLETE_FIXED_CONTEXT.json',context)
        actual=binding['actual_context_states'][state]
        require(type(actual)is dict and set(actual)=={'complete_context_pins','all_snapshot_pairs','actual_extraction_report_pin',
            'actual_observation_manifest_pin','selected_last_libmix_number','actual_extraction_coverage_contract_pin'},
            'full actual context contract, no final-state substituted history')
        for key in('actual_extraction_report_pin','actual_observation_manifest_pin','actual_extraction_coverage_contract_pin'):
            check_pin(actual[key],budget)
        observed=ObservedContext(actual['complete_context_pins'],budget,evidence)
        require(type(actual['selected_last_libmix_number'])is int and
            actual['selected_last_libmix_number']==observed.before['libmix'],'actual final completed call, no arbitrary selection')
        # Protect every saved old/post/final snapshot, not just the last call.
        # Root coverage META supplies same exact all-snapshot list as the
        # genuine closed extraction; it cannot be a Source-only assertion.
        cov=strict_json(Path(actual['actual_extraction_coverage_contract_pin']['path']).read_bytes())
        require(cov['schema']=='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1'and
            cov['all_original_snapshot_pairs_saved']is True and cov['actual_extraction_report_pin']==actual['actual_extraction_report_pin']and
            cov['actual_observation_manifest_pin']==actual['actual_observation_manifest_pin']and
            cov['states'][state]['all_snapshot_pairs']==actual['all_snapshot_pairs']and
            cov['states'][state]['complete_context_pins']==actual['complete_context_pins']and
            cov['actual_closed_extraction_receipt_independently_reviewed']is True and cov['new_qualification_sha256']is None,
            'same genuine complete saved snapshot/context coverage, no raw Q transplant')
        report=strict_json(Path(actual['actual_extraction_report_pin']['path']).read_bytes())
        require(report['schema']=='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'and
            report['all_complete_state_scope_retained']is True,'actual complete Root extraction report')
        expected=report['states'][state];pairs=actual['all_snapshot_pairs']
        require(type(pairs)is list and len(pairs)==len(expected),'all genuine snapshot pairs retained')
        selected={};previous=0
        for pair,record in zip(pairs,expected):
            require(set(pair)=={'event','role','root_prefix','input_pin','sqlite_pin','native_pool_pin'}and
                type(pair['event'])is int and pair['event']>=previous and
                all(pair[k]==record[k]for k in('event','role','root_prefix','input_pin'))and
                pair['sqlite_pin']==record['paired_SQLite_pin']and pair['native_pool_pin']==record['paired_original_pool_pin'],
                'every original complete pair exactly bound to genuine report, no sorting or replacement')
            previous=pair['event']
            for k in('input_pin','sqlite_pin','native_pool_pin'):check_pin(pair[k],budget)
            extract=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget)
            try:
                n=0
                for item in extract.iter_all():
                    for raw in extract.iter_raw(item['record']):del raw
                    n+=1;evidence.event('FULL_ORIGINAL_OBSERVED_SNAPSHOT_RECORD',event=pair['event'],role=pair['role'],original=item)
                require(n==record['complete_records'],'complete actual snapshot EOF count')
            finally:extract.close()
            key=(pair['event'],pair['role'])
            require(key not in selected,'duplicate genuine original snapshot')
            # Keep only small Source pins, never an in-memory whole path tree.
            selected[key]=pair
        final_pair=selected.get((observed.events[-1]['event'],'final-complete-micro'))
        require(final_pair is not None and final_pair['sqlite_pin']==source['sqlite_pin']and
            final_pair['native_pool_pin']==source['native_pool_pin'],
            'same genuinely observed final full micro used for all62 operands, no unrelated V23 pool substitution')
        def open_pair(event,role,required=True):
            pair=selected.get((event,role))
            require(pair is not None or not required,'actual necessary snapshot missing '+role)
            if pair is None:return None
            item=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget);opened.append(item);return item
        maskk=bool(observed.old['fields']['LSAME,MASKK,LALL,LDIFF'][1])
        old=open_pair(observed.old['event'],'oldmacro-LIBDEN',maskk)
        pre=open_pair(observed.before['event'],'oldmacro-pre-LIBMIX',maskk)
        post=open_pair(observed.after['event'],'postmacro-LIBMIX')
        model=ContextAwareConstruction(saved,evidence,context,binding['Source_route'],observed,old,pre,post)
        for phase in('scattering','scalar','fission','extras','overv_fallback','metadata'):
            try:getattr(model,phase)();evidence.phase_results.append(dict(phase=phase,computation_finished=True))
            except Exception as error:
                evidence.event('PHASE_FAILED',phase=phase,error=repr(error),complete_original_scope_retained=True)
                evidence.phase_results.append(dict(phase=phase,computation_finished=False,error=repr(error)))
        unknown=evidence.complete_decisions()
        state_report=dict(state=state,all_original_records=evidence.records,complete_MACROLIB_records=evidence.macro_records,
            original_scope=[370,8,3,32,64,62,18,6,48],complete_source_field_comparisons=evidence.comparisons,
            compared_known_elements=evidence.compared_elements,all_mismatching_elements=evidence.mismatch_elements,
            all_context_or_operand_issues=evidence.issues,unknown_macro_producers=unknown,phase_results=evidence.phase_results,
            all_original_native_records_and_bytes_preserved=True,all_complete_orders_preserved=True,
            all_missing_fields_not_zero_filled=True,expected_binary32_model='MODEL_SEPARATE_ROUND32',
            binary32_model_operations=model.fp.operations,binary32_model_underflow_to_zero=model.fp.underflow_to_zero,
            binary32_model_overflow_to_infinity=model.fp.overflow_to_infinity,
            mathematical_scattering_domain_computed=model.full_scattering_math_items,expected_full_scattering_domain=370*370*8*3,
            actual64_isotope_mix_mapping_checked=model.fission_mapping_validated,
            actual_old_MACROLIB_snapshots_used=maskk,actual_STATE9_initialization_checked=True,actual_NFISS0_INDFIS_checked=True,
            actual_MAT_MASK_derivation_checked=True,actual_complete_SPH_branch_selection_checked=observed.complete_sph_call_selection_proved,
            original_context_event_count=len(actual['complete_context_pins']),all_original_snapshot_count=len(pairs),
            complete_final_construction_qualified=False,historical_old_macro_proved=False,
            historical_actual_tracking_MASK_proved=False,historical_SPHand_compiled_arithmetic_proved=False,
            instrumented_actual_context_is_not_recovered_original_history=True,
            known_component_matching_does_not_qualify_unknown_delayed_or_inherited_fields=True,
            full_output_scope_retained_even_on_failure=True,**FALSE)
    except Exception as error:
        if evidence is not None:
            evidence.event('PHASE_FAILED',phase='context_admission_or_initialization',error=repr(error),complete_original_scope_retained=True)
            unknown=evidence.complete_decisions()
            state_report=dict(state=state,all_original_records=evidence.records,complete_MACROLIB_records=evidence.macro_records,
                original_scope=[370,8,3,32,64,62,18,6,48],error=repr(error),unknown_macro_producers=unknown,
                all_context_or_operand_issues=evidence.issues,all_mismatching_elements=evidence.mismatch_elements,
                all_original_native_records_and_bytes_preserved=True,complete_final_construction_qualified=False,
                full_output_scope_retained_even_on_failure=True,all_missing_fields_not_zero_filled=True,**FALSE)
        else:raise
    finally:
        for item in reversed(opened):item.close()
        if evidence is not None:evidence.close()
        saved.close()
    require(state_report is not None,'no fabricated state result')
    state_report['complete_output_file_pins']=[full_pin(p,budget)for p in sorted(root.rglob('*'))if p.is_file()]
    state_report['all_state_databases_and_pool_closed_before_next_state']=True
    write_new(root/'ACTUAL_COMPLETE_STATE_CONSTRUCTION_REPORT.json',state_report)
    return state_report

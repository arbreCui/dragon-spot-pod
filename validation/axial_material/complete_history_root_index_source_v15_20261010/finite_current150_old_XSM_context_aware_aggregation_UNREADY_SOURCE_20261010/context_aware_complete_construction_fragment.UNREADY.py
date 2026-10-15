"""Insertion-only Source fragment. Not importable in isolation or executed.

Uses original complete saved-native adapter and Binary32Model. Root must save
the actual observer stream and every old/post/final XSM first. None of those
future values/pins are supplied by this author. All record scopes remain full.
"""

class ObservedContext:
    """Full context words streamed to disk; MAT membership alone stays in RAM."""
    def __init__(self, pins, budget, evidence):
        require(type(pins)is list and pins,'actual full context list required')
        self.events=[];self.budget=budget;self.evidence=evidence
        previous=0;last_libmix=0;pending=[]
        for expected in pins:
            check_pin(expected,budget)
            with Path(expected['path']).open('rb')as stream:
                def take(size):
                    require(type(size)is int and 0<=size<=2**20,'bounded original context read')
                    budget();raw=stream.read(size)
                    require(len(raw)==size,'actual context truncation');return raw
                require(take(8)==b'AXOBSCTX','actual original observer magic')
                version,event,libmix,length=struct.unpack('<4i',take(16))
                require(version==2 and event==previous+1 and libmix>=0 and 1<=length<=256,
                    'all original consecutive events, no hidden prefix or sorting')
                previous=event;label=take(length).decode('ascii')
                fields={};dimensions={}
                def field(name,count,real=False,dimension=False,mat=False):
                    require(type(count)is int and count>=0,'all actual context field count')
                    require(mat or count<=65536,'bounded non-MAT actual context field')
                    begin=stream.tell();digest=hashlib.sha256();values=array('I'if real else'i')
                    membership=set()
                    for start in range(0,count,4096):
                        raw=take(4*min(4096,count-start));digest.update(raw)
                        chunk=make_array(raw,not real)
                        if mat:
                            require(all(0<=x<=MIXES for x in chunk),'full actual MAT region mix bounds')
                            membership.update(chunk)
                        else:values.extend(chunk)
                        evidence.event('FULL_ORIGINAL_CONTEXT_WORDS',event=event,libmix=libmix,label=label,
                            field=name,original_type='REAL32'if real else'INTEGER32',original_count=count,
                            element_begin0=start,full_original_bytes_hex=raw.hex())
                    evidence.event('FULL_ORIGINAL_CONTEXT_FIELD_EOF',event=event,label=label,field=name,
                        span_begin=begin,span_end=stream.tell(),original_count=count,
                        complete_original_SHA256=digest.hexdigest())
                    fields[name]=membership if mat else values
                    if dimension:dimensions.update(zip(name.split(','),values))
                if label=='LIBMIX_BEFORE':
                    field('NBMIX,NGROUP,NBISO,ITSTMP',4,dimension=True)
                    require(tuple(dimensions[k]for k in('NBMIX','NGROUP','NBISO'))==(8,370,62),'full LIBMIX scope')
                    field('ROOT_STATE40',40);field('MIX',62);field('DEN',62,True);field('TMPDAY',3,True)
                    field('MACRO_LENGTH,MACRO_KIND',2,dimension=True);field('MASK',8);field('MASKL',370)
                    field('MIXTURESVOL_LENGTH,MIXTURESVOL_KIND',2,dimension=True)
                    if dimensions['MIXTURESVOL_LENGTH']>0:
                        require(dimensions['MIXTURESVOL_LENGTH']==8 and dimensions['MIXTURESVOL_KIND']==2,'full observed root volume type/count')
                        field('ROOT_MIXTURESVOL_BEFORE',8,True)
                elif label=='LIBDEN_OLD_CONTEXT':
                    field('NBMIX,NGROUP,NBISO,NL,NDEL,NESP,NED,ITRANC,MAXNFI,NPART,ITSTMP,STERN,NFISSI',13,dimension=True)
                    require(tuple(dimensions[k]for k in('NBMIX','NGROUP','NBISO','NL','NDEL','NESP','NED'))==
                        (8,370,62,3,6,4,18),'all original construction dimensions')
                    field('TMPDAY',3,True);field('LSAME,MASKK,LALL,LDIFF',4);field('MASK',8);field('MASKL',370)
                elif label=='LIBDEN_BEFORE_FISSION_SLOT_MUTATION':
                    field('NBMIX,MAXNFI,NFISS0,NFISSI',4,dimension=True)
                    require(dimensions['NBMIX']==8 and 0<=dimensions['NFISS0']==dimensions['NFISSI']<=dimensions['MAXNFI']<=62,
                        'complete defined original pre-mutation extent')
                    field('INDFIS_DEFINED_PRE_MUTATION',8*dimensions['NFISSI'])
                elif label=='TONDRV_AFTER_REAL_MAT_ELIMINATION':
                    field('NREG,NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPROB,IGRMIN,IGRMAX',9,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370)and dimensions['NREG']>0,
                        'complete actual tracking scope')
                    field('MAT',dimensions['NREG'],mat=True);field('MIX',62);field('LSHI',62);field('DEN',62,True)
                elif label=='TONDRV_ACTUAL_FINAL_LIBMIX_MASK':
                    field('NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPHASE,NRES2,ITSTMP',8,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370),'full mask scope')
                    field('LSHI',62);field('LSHI2',62);field('TMPDAY',3,True);field('MASK',8);field('MASKL',370)
                elif label=='TONSPH_BEFORE_ACTUAL_TONCMI':
                    field('NBM,NBISO,NGRO,INRS,ITRANC,IGRMIN,IGRMAX',7,dimension=True)
                    require(tuple(dimensions[k]for k in('NBM','NBISO','NGRO'))==(8,62,370),'all actual SPH factors')
                    field('MASKI',62);field('SPH',8*370,True)
                elif label=='TONDRV_ACTUAL_SPH_CALL_DECISION':
                    field('NBISO,NBMIX,NGRO,INRS,NBNRS,NRES2,KSPH',7,dimension=True)
                    require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370),'full Source SPH decision scope')
                    field('LSHI2',62)
                elif label not in('LIBMIX_AFTER','TONDRV_FINAL_AFTER_SHIBA'):
                    raise ValueError('unhandled original event, never skipped '+label)
                require(stream.read(1)==b'','complete context EOF, no omitted extra word')
                for name in('MASK','MASKL','MASKI','LSAME,MASKK,LALL,LDIFF'):
                    if name in fields:require(all(x in(0,1)for x in fields[name]),'actual logical merge words exact0/1')
                current=dict(event=event,libmix=libmix,label=label,fields=fields,dimensions=dimensions,input=expected)
                if label=='LIBMIX_BEFORE':
                    require(not pending and libmix==last_libmix+1,'full consecutive original LIBMIX begin')
                    last_libmix=libmix;pending=[current]
                    self.events=[e for e in self.events if e['label']not in
                        ('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER')]
                elif label in('LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'):
                    sequence=('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER')
                    require(pending and libmix==last_libmix and label==sequence[len(pending)],'all Source call phases in exact original order')
                    pending.append(current)
                    if label=='LIBMIX_AFTER':
                        evidence.event('FULL_ACTUAL_CALL_CONTEXT',libmix=libmix,event_numbers=[e['event']for e in pending]);pending=[]
                elif label=='TONDRV_AFTER_REAL_MAT_ELIMINATION':
                    require(not pending,'no hidden incomplete preceding original call')
                    self.events=[]
                self.events.append(current)
            check_pin(expected,budget)
        require(not pending,'no incomplete original call at complete EOF')
        self.full_original_event_count=previous
        require(self.events[-1]['label']=='TONDRV_FINAL_AFTER_SHIBA','complete observer end required')
        # Retain every event, but select the genuinely final completed LIBMIX.
        calls={};last_begin=0
        for e in self.events:
            if e['label']=='LIBMIX_BEFORE':
                last_begin=e['libmix'];calls[last_begin]=[e]
            elif e['label']in('LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'):
                require(e['libmix']in calls,'call context without original LIBMIX begin')
                calls[e['libmix']].append(e)
        require(calls,'actual complete LIBMIX calls required')
        for number,events in calls.items():
            labels=[e['label']for e in events]
            require(labels==['LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER'],
                'full current MXS call context, no incomplete call treated as complete')
            evidence.event('FULL_ACTUAL_CALL_CONTEXT',libmix=number,event_numbers=[e['event']for e in events])
        self.before,self.old,self.fission,self.after=calls[last_begin]
        track=[e for e in self.events if e['label']=='TONDRV_AFTER_REAL_MAT_ELIMINATION'and e['event']<self.before['event']]
        masks=[e for e in self.events if e['label']=='TONDRV_ACTUAL_FINAL_LIBMIX_MASK'and e['event']<self.before['event']]
        require(track and masks,'real MAT and final-mask events required, no inferred ones')
        self.track,self.mask=track[-1],masks[-1]
        t,m,b,o=self.track['fields'],self.mask['fields'],self.before['fields'],self.old['fields']
        require(b['MIX']==t['MIX'] and b['DEN']==t['DEN'],'same actual mix/density in call and tracking')
        require(b['MASK']==m['MASK']==o['MASK']and b['MASKL']==m['MASKL']==o['MASKL'],'actual complete masks agree')
        require(all(t['LSHI'][i]==0 for i in range(ISOTOPES)if t['MIX'][i]not in t['MAT']),
            'Source TONDRV MAT-eliminated isotope flags remain zero')
        expected_mask=array('i',(int(any(b['MIX'][i]==mix and m['LSHI'][i]>0 for i in range(ISOTOPES)))for mix in range(1,9)))
        lo,hi=self.track['dimensions']['IGRMIN'],self.track['dimensions']['IGRMAX']
        require(1<=lo<=hi<=GROUPS and expected_mask==b['MASK']and
            b['MASKL']==array('i',(int(lo<=g<=hi)for g in range(1,GROUPS+1))),
            'Source exact MAT/LSHI/group-range mask derivation, never MASK=true default')
        require(self.mask['dimensions']['ITSTMP']==self.before['dimensions']['ITSTMP']==self.old['dimensions']['ITSTMP']==0,
            'current actual no-perturbation call route')
        # All earlier calls/events remain saved. Validate this final TONDRV's
        # actual decision list after its initial final-mask event.
        sph=[e for e in self.events if e['label']=='TONSPH_BEFORE_ACTUAL_TONCMI'and
            self.track['event']<e['event']<self.before['event']]
        for e in sph:
            require(self.track['dimensions']['KSPH']==1,'actual SPH branch is KSPH1')
            for bits in e['fields']['SPH']:Binary32Model.ratio(bits)
            evidence.event('ACTUAL_FULL_SPH_CAPTURE_RETAINED',event=e['event'],all2960_factor_words=True,
                factors_assumed_one=False,previous_history_reconstructed=False)
        decisions=[e for e in self.events if e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'and
            self.track['event']<e['event']<self.before['event']]
        ksph=self.track['dimensions']['KSPH']
        if ksph==1:
            nres=self.mask['dimensions']['NRES2']
            require(type(nres)is int and 0<=nres<=ISOTOPES and
                [e['dimensions']['INRS']for e in decisions]==list(range(1,nres+1)),
                'every actual Source INRS decision required, no omitted false branch')
            require(all(e['dimensions']['KSPH']==1 and e['dimensions']['NRES2']==nres
                and e['dimensions']['NBNRS']>=0 for e in decisions),'actual SPH branch dimensions')
            selected=[e['dimensions']['INRS']for e in decisions if e['dimensions']['NBNRS']>1]
            require([e['dimensions']['INRS']for e in sph]==selected,'one full actual SPH factor event per true Source decision')
            require(all(e['fields']['LSHI2']==self.mask['fields']['LSHI2']for e in decisions),
                'all original SPH call-selection isotope flags unchanged')
        else:require(not decisions and not sph,'Source non-KSPH1 branch contains no SPH calls')
        self.complete_sph_call_selection_proved=True
        evidence.event('COMPLETE_ACTUAL_SPH_SELECTION',KSPH=ksph,all_original_decision_events=[e['event']for e in decisions],
            all_original_factor_events=[e['event']for e in sph],factors_assumed_one=False)


class ContextAwareConstruction(CompleteConstruction):
    """Final construction with actual old state; never a historical float replay."""
    def __init__(self,saved,evidence,context,route,observed,old_saved,pre_saved,post_saved):
        self.saved,self.evidence,self.context,self.route=saved,evidence,context,route
        self.observed,self.old_saved,self.pre_saved,self.post_saved=observed,old_saved,pre_saved,post_saved
        self.fp=Binary32Model();self.aliases=context['complete62_LIBIPS_aliases_one_based']
        self.mix=self.vector(('ISOTOPESMIX',),1,62);self.density=self.vector(('ISOTOPESDENS',),2,62)
        self.root_state=self.vector(('STATE-VECTOR',),1,40);self.macro_state=self.vector(('MACROLIB','STATE-VECTOR'),1,40)
        self.chi_limits=self.vector(('CHI-LIMITS',),1,5)
        require(self.chi_limits[0]==0 and self.chi_limits[-1]==370 and all(a<b for a,b in zip(self.chi_limits,self.chi_limits[1:])),
            'all original CHI-LIMITS')
        b,o,f=observed.before,observed.old,observed.fission
        require(self.mix==b['fields']['MIX']and self.density==b['fields']['DEN']and self.root_state==b['fields']['ROOT_STATE40'],
            'same final micro operands and actual last LIBMIX state')
        self.mask=b['fields']['MASK'];self.maskl=b['fields']['MASKL']
        self.lsame,self.maskk,self.lall,self.ldiff=(bool(x)for x in o['fields']['LSAME,MASKK,LALL,LDIFF'])
        require(not self.lsame and self.root_state[5]==0 and self.root_state[25]==0 and
            o['dimensions']['NPART']==0,'current complete32/256 neutron route, other branch remains unsupported')
        particle=saved.row(('PARTICLE',))
        if particle is not None:require(particle['kind']==3 and saved.range_bytes(particle,0,1)in(b'N',b' '),'actual neutron particle')
        require(self.maskk==(old_saved is not None)==(pre_saved is not None),'actual oldmacro presence matches observed MASKK')
        self.old_state=self.old_vector(('MACROLIB','STATE-VECTOR'),1,40)if self.maskk else None
        self.nbm0=self.old_state[1]if self.maskk else 0
        self.nfiss0=f['dimensions']['NFISS0'];require(self.nfiss0==o['dimensions']['NFISSI'],'actual NFISS0 matches pre-mutation context')
        require(self.ldiff==(self.old_state[8]==1 if self.maskk else True)and
            self.lall==(8>self.nbm0 if self.maskk else False),'old STATE9/LALL exact Source branch')
        if self.maskk:
            require(self.old_state[0]==370 and 0<self.nbm0<=8 and self.old_state[3]//4==self.nfiss0 and
                (self.old_state[5]==2 or o['dimensions']['ITRANC']<=0),'original old scope/transport conditions')
            self.same_snapshots(pre_saved,old_saved,'ACTUAL_PRE_LIBMIX_VS_PRE_LIBDEN_MACRO')
        self.same_snapshots(post_saved,saved,'ACTUAL_LAST_POST_LIBMIX_VS_FINAL_MICRO_MACRO')
        self.extra_names=[bytes.fromhex(x).decode('ascii')for x in context['original_18_extra_name_bytes_hex']]
        require(len(self.extra_names)==18,'all eighteen declared edits')
        self.model_eligibility=dict(final_micro_constructed_independently=True,all370_groups_and8_mixes_requested=True,
            density_order='original62_no_dedup',model='MODEL_SEPARATE_ROUND32',actual_old_macro_available=self.maskk,
            actual_tracking_MASK_proved=True,actual_branch_proved=True,actual_full_SPHand_compiled_link_proved=False,
            historical_machine_float_replay=False)
        self.nxs,self.timfact=1,0
        times=saved.row(('TIMESPER',))
        require(times is None or not 2<=times['declared_count']<=6,'actual ITSTMP0 forbids Source perturbation')
        self.scalar_presence={};self.scalar_intermediate={};self.overv_fallback_expected=None;self.full_scattering_math_items=0
        self.fission_mapping_validated=False;self.delayed_zero_components_context_known=False;self.diffusion_old_flag=self.ldiff
        self.indfis=array('i',f['fields']['INDFIS_DEFINED_PRE_MUTATION']);self.nfissi=self.nfiss0
        require(len(self.indfis)==8*self.nfiss0 and all(0<=x<=62 for x in self.indfis),'all original defined INDFIS')
        self.validate_old_indfis()
        self.reserved=set()
        for g in range(1,371):
            for name in('NTOT0','NTOT1','DIFF','H-FACTOR','C-FACTOR','OVERV','TRANC',*self.extra_names,
                    'NUSIGF','CHI',*(f'NUSIGF{d:02d}'for d in range(1,7)),*(f'CHI{d:02d}'for d in range(1,7)),
                    *(stem+f'{m:02d}'for m in range(3)for stem in('SCAT','SIGS','SIGW','NJJS','IJJS','IPOS','CHECK')),
                    'FLUX-INTG','FLUX-INTG-P1'):
                self.reserved.add(self.macro_path(g,name))
        self.reserved.update(('MACROLIB',n)for n in('STATE-VECTOR','TIMESTAMP','FISSIONINDEX','LAMBDA-D','ENERGY',
            'SIGNATURE','ADDXSNAME-P0','VOLUME','PARTICLE','PARTICLE-NAM','PARTICLE-NGR','PARTICLE-MC2'))

    def selected(self,mix):return bool(self.mask[mix-1])or not self.maskk
    def group_selected(self,group):return bool(self.maskl[group-1])or self.lall

    def old_vector(self,path,kind,count=None,required=True):
        row=None if self.old_saved is None else self.old_saved.row(path)
        if row is None:
            require(not required,'required original old operand missing '+repr(path));return None
        require(row['kind']==kind and(count is None or row['declared_count']==count)and row['original_word_count']*4<=2**20,
            'original old type/count, no coercion '+repr(path))
        raw=b''.join(self.old_saved.iter_raw(row))
        return raw if kind==3 else make_array(raw,kind==1)

    def old_mix_vector(self,path,required=True):
        v=self.old_vector(path,2,required=required)
        if v is None:return array('I',[0])*8
        require(len(v)<=8,'old vector larger than Source GAF slice')
        return v+array('I',[0])*(8-len(v))

    def compare_raw_sources(self,left,right,path,producer):
        a,b=left.row(path),right.row(path)
        require(a is not None and b is not None and a['kind']==b['kind']and a['declared_count']==b['declared_count']and
            a['original_word_count']==b['original_word_count'],'full snapshot type/count/presence differs '+repr(path))
        count=0
        for raw in left.iter_raw(a):count+=len(raw)
        for raw in right.iter_raw(b):count-=len(raw)
        require(count==0 and a['native_payload_sha256']==b['native_payload_sha256'],'complete original snapshot byte mismatch')
        self.evidence.event('COMPLETE_SNAPSHOT_RECORD_COUPLING',path=list(path),producer=producer,
            left_original=a,right_original=b,all_original_bits_checked=True)

    def same_snapshots(self,left,right,producer):
        require(left is not None and right is not None,'complete original snapshot pair required')
        nleft=nright=0
        for item in left.iter_all():
            row=item['record']
            if row['path'][:1]!=['MACROLIB']or row['path']==['MACROLIB']:continue
            nleft+=1;self.compare_raw_sources(left,right,tuple(row['path']),producer)
        for item in right.iter_all():
            row=item['record']
            if row['path'][:1]!=['MACROLIB']or row['path']==['MACROLIB']:continue
            nright+=1;require(left.row(tuple(row['path']))is not None,'new unexpected original macro record')
        require(nleft==nright,'all macro container/empty/field scope matches')
        def order(source):
            for item in source.iter_all():
                row=item['record']
                if row['path'][:1]==['MACROLIB']and row['path']!=['MACROLIB']:
                    yield row['path'],row['path_types'],row['kind'],row['declared_count']
        for a,b in zip(order(left),order(right)):require(a==b,'full original physical path/key/type/count order')
        self.evidence.event('COMPLETE_SNAPSHOT_ORDER_COUPLING',producer=producer,complete_records=nleft,
            macro_only_XSM_root_labels_no_fake_root_record=True,API_rotation_order_not_normalized=True)

    def inherit(self,path,producer='LIBDEN_ORIGINAL_OLD_RECORD_NOT_WRITTEN'):
        old=None if self.old_saved is None else self.old_saved.row(path)
        actual=self.saved.row(path)
        if old is None:
            if actual is not None and actual['kind']not in(0,10,99):
                self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='no Source write and no actual old value')
            return
        require(actual is not None and old['kind']==actual['kind']and old['declared_count']==actual['declared_count']and
            old['original_word_count']==actual['original_word_count'],'actual inherited presence/type/count changed')
        begin=self.evidence.expected.tell();mismatch=0;total=0
        for raw in self.old_saved.iter_raw(old):
            self.evidence.expected.write(raw);total+=len(raw)
        for raw in self.saved.iter_raw(actual):del raw
        # Full original EOF digests are validated by both iter_raw operations.
        # A differing digest is a genuine complete-record mismatch, never PASS.
        if old['native_payload_sha256']!=actual['native_payload_sha256']:
            mismatch=1;self.evidence.mismatch_elements+=1
            self.evidence.line(self.evidence.mismatches,dict(path=list(path),producer=producer,
                mismatch_unit='complete_original_record_SHA256',old_record=old,actual_record=actual))
        self.evidence.comparisons+=1
        self.evidence.line(self.evidence.fields,dict(path=list(path),producer=producer,actual_original_record=actual,
            expected_original_record=old,expected_pool_begin=begin,expected_pool_end=begin+total,
            outcome='ORIGINAL_OLD_BITS_MATCH'if not mismatch else'ORIGINAL_OLD_BITS_MISMATCH'))
        self.evidence.decision(path,producer,'ORIGINAL_OLD_BITS_MATCH'if not mismatch else'ORIGINAL_OLD_BITS_MISMATCH')

    def validate_old_indfis(self):
        expected=array('i',[0])*(8*self.nfiss0)
        row=None if not self.maskk else self.old_saved.row(('MACROLIB','FISSIONINDEX'))
        if row is not None:
            original=self.old_vector(('MACROLIB','FISSIONINDEX'),1)
            require(len(original)<=8*self.nfiss0,'Source rejects excessive original old FISSIONINDEX')
            if len(original)==8*self.nfiss0:expected=original
            else:
                require(len(original)>=self.nbm0*self.nfiss0,'Source old-index short read would use undefined words')
                for slot in range(self.nfiss0):
                    expected[slot*8:slot*8+self.nbm0]=original[slot*self.nbm0:(slot+1)*self.nbm0]
        require(expected==self.indfis,'actual observed pre-mutation INDFIS from original old map/Source zeros')

    def scalar(self):
        names=('NTOT0','NTOT1','STRD','H-FACTOR','C-FACTOR','OVERV','TRANC')
        accum={n:array('I',[0])*(370*8)for n in names};present={n:False for n in names}
        present['NTOT0']=True;present['TRANC']=self.observed.old['dimensions']['ITRANC']!=0
        for mix in range(1,9):
            if not self.selected(mix):continue
            total=0
            for isotope in range(1,63):
                den=self.density[isotope-1]
                if self.mix[isotope-1]!=mix or not self.fp.nonzero(den):continue
                total=self.fp.add(total,den)
                for suffix in SUFFIXES[:self.nxs]:
                    for name in names:
                        if(name=='STRD'and not self.ldiff)or(name=='TRANC'and not present['TRANC']):continue
                        values=self.micro(isotope,name,suffix=suffix,required=name in('NTOT0','TRANC'))
                        if values is None:continue
                        present[name]=True
                        for g,bits in enumerate(values):
                            k=g*8+mix-1;accum[name][k]=self.fp.add(accum[name][k],self.fp.multiply(bits,den))
                    den=self.fp.multiply(den,self.timfact)
            if present['OVERV']:
                for g in range(370):
                    k=g*8+mix-1
                    if self.fp.nonzero(accum['OVERV'][k]):accum['OVERV'][k]=self.fp.divide(accum['OVERV'][k],total)
        self.scalar_presence=present
        ordinary={n.rstrip(' ')for n in self.extra_names if n[:2]!='NW'and n.rstrip(' ')!='TRANC'and n[:3]not in('BST','CST')and n[:8]!='H-FACTOR'}
        for name in names:
            output='DIFF'if name=='STRD'else name
            if present[name]:self.scalar_intermediate[output]=array('I',[0])*(370*8)
            for g in range(1,371):
                path=self.macro_path(g,output)
                if not present[name]or not self.group_selected(g):
                    if output not in ordinary and not(output=='OVERV'and not present['OVERV']):self.inherit(path)
                    continue
                v=accum[name][(g-1)*8:g*8]
                if self.maskk:
                    old=self.old_mix_vector(path,required=name!='H-FACTOR')
                    for m in range(8):
                        if not self.mask[m]:
                            v[m]=self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,old[m]))if name=='STRD'else old[m]
                if name=='STRD':
                    for m,bits in enumerate(v):
                        if self.fp.nonzero(bits):v[m]=self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,bits))
                self.scalar_intermediate[output][(g-1)*8:g*8]=v
                if output not in ordinary:self.evidence.compare(path,2,v,'LIBDEN_SCALAR_ACTUAL_CONTEXT_'+name,self.model_eligibility)
        if not present['OVERV']:
            energy=self.vector(('ENERGY',),2,371)
            if not self.fp.nonzero(energy[-1]):energy[-1]=self.fp.f64_to32(1e-5)
            sqfmas=math.sqrt(2.0e4*1.60217653e-19/1.67492728e-27);expected=array('I',[0])*(370*8)
            for g in range(370):
                average=self.fp.sqrt(self.fp.multiply(energy[g],energy[g+1]));root=self.fp.sqrt(average)
                value=struct.unpack('<f',struct.pack('<I',root))[0]
                require(value!=0,'actual OVERV fallback nonzero energy')
                for m in range(8):expected[g*8+m]=self.fp.f64_to32(1.0/(value*sqfmas))
            self.overv_fallback_expected=expected
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',
                original_all370x8_words_compared=True,historical_machine_bit_replay=False)

    def extras(self):
        for ordinal,name in enumerate(self.extra_names,1):
            out=name.rstrip(' ')
            if name[:2]=='NW'or out=='TRANC'or name[:3]in('BST','CST')or name[:8]=='H-FACTOR':
                self.evidence.event('DECLARED_EXTRA_SPECIAL_PRODUCER',declared_ordinal=ordinal,full_name_hex=name.encode('ascii').hex())
                if name[:2]!='NW'and out not in('TRANC','H-FACTOR'):
                    for g in range(1,371):self.inherit(self.macro_path(g,out))
                continue
            values=array('I',[0])*(370*8);exists=False
            for mix in range(1,9):
                if not self.selected(mix):continue
                for isotope in range(1,63):
                    den=self.density[isotope-1]
                    if self.mix[isotope-1]!=mix or not self.fp.nonzero(den):continue
                    for suffix in SUFFIXES[:self.nxs]:
                        v=self.micro(isotope,name,suffix=suffix,required=False)
                        if v is None:
                            self.evidence.event('ACTUAL_CONTEXT_EXTRA_GOTO720',isotope=isotope,ordinal=ordinal,suffix=suffix);break
                        exists=True
                        for g,bits in enumerate(v):
                            k=g*8+mix-1;values[k]=self.fp.add(values[k],self.fp.multiply(bits,den))
                        den=self.fp.multiply(den,self.timfact)
            for g in range(1,371):
                path=self.macro_path(g,out)
                if out=='OVERV'and not self.scalar_presence.get('OVERV',False):continue
                if not self.group_selected(g):self.inherit(path);continue
                old=self.old_vector(path,2,required=False)if self.maskk else None
                if old is not None:exists=True
                if not exists:
                    if out in self.scalar_intermediate:
                        self.evidence.compare(path,2,self.scalar_intermediate[out][(g-1)*8:g*8],
                            'LIBDEN_SCALAR_RETAINED_EXTRA_EXIST_FALSE',self.model_eligibility)
                    else:self.inherit(path)
                    continue
                current=values[(g-1)*8:g*8]
                inherited=self.old_mix_vector(path,False)
                for m in range(8):
                    if self.maskk and not self.mask[m]:current[m]=inherited[m]
                self.evidence.compare(path,2,current,'LIBDEN_EXTRA_'+str(ordinal)+'_ACTUAL_EXIST_ORDER',self.model_eligibility)

    def scattering(self):
        for moment in range(3):
            cm=f'{moment:02d}';check=array('I',[0])*(370*8)
            for start in range(0,370,50):
                width=min(50,370-start);gaf=array('I',[0])*(8*370*width);sigs=array('I',[0])*(8*width)
                for isotope in range(1,63):
                    den=self.density[isotope-1];mix=self.mix[isotope-1]-1
                    if not self.fp.nonzero(den):continue
                    fact=0x3f800000
                    for suffix in SUFFIXES[:self.nxs]:
                        sigma=self.micro(isotope,'SIGS'+cm,suffix=suffix,required=False)
                        if sigma is not None:
                            njj=self.micro(isotope,'NJJS'+cm,1,suffix=suffix);ijj=self.micro(isotope,'IJJS'+cm,1,suffix=suffix)
                            require(all(0<=n<=370 and(n==0 or n<=j<=370)for n,j in zip(njj,ijj)),'complete micro sparse bounds')
                            scat=self.micro(isotope,'SCAT'+cm,count=sum(njj),suffix=suffix)
                            cursor=sum(njj[:start])
                            for block in range(width):
                                dest=start+block
                                if self.selected(mix+1):sigs[block*8+mix]=self.fp.add(sigs[block*8+mix],self.fp.multiply(sigma[dest],den))
                                for src in range(ijj[dest]-1,ijj[dest]-njj[dest]-1,-1):
                                    if self.selected(mix+1):
                                        k=(block*8+mix)*370+src
                                        gaf[k]=self.fp.add(gaf[k],self.fp.multiply(self.fp.multiply(scat[cursor],den),fact))
                                    cursor+=1
                            require(cursor==sum(njj[:start+width]),'all sparse micro words consumed in source order')
                        fact=self.fp.multiply(fact,self.timfact)
                for block in range(width):
                    dest=start+block;g=dest+1;path=self.macro_path(g,'SIGS'+cm)
                    if self.group_selected(g):
                        v=sigs[block*8:(block+1)*8]
                        if self.maskk:
                            old=self.old_mix_vector(path,required=moment==0)
                            for m in range(8):
                                if not self.mask[m]:v[m]=old[m]
                        self.evidence.compare(path,2,v,'LIBDEN_SIGS_ACTUAL_MASK_INHERIT',self.model_eligibility)
                    else:self.inherit(path)
                    # Source LOGL is evaluated on new GAF before restoring old SCAT.
                    logl=self.group_selected(g)or any(self.maskl[src]and self.fp.nonzero(gaf[(block*8+m)*370+src])
                        for m in range(8)for src in range(370))
                    names=('SCAT'+cm,'NJJS'+cm,'IJJS'+cm,'IPOS'+cm,'SIGW'+cm)
                    if logl and self.maskk:
                        old=self.old_vector(self.macro_path(g,'SCAT'+cm),2,required=moment==0)
                        if old is not None:
                            nj=self.old_vector(self.macro_path(g,'NJJS'+cm),1);ij=self.old_vector(self.macro_path(g,'IJJS'+cm),1)
                            pos=self.old_vector(self.macro_path(g,'IPOS'+cm),1)
                            require(len(nj)==len(ij)==len(pos)<=8,'complete original old scatter layout')
                            for m in range(8):
                                if self.mask[m]or m>=len(pos)or pos[m]==-99:continue
                                require(0<=nj[m]<=370 and(nj[m]==0 or nj[m]<=ij[m]<=370)and
                                    1<=pos[m]and pos[m]-1+nj[m]<=len(old),'complete old sparse span')
                                for j,src in enumerate(range(ij[m]-1,ij[m]-nj[m]-1,-1)):
                                    gaf[(block*8+m)*370+src]=old[pos[m]-1+j]
                    output=array('I');nj=array('i');ij=array('i');pos=array('i');sigw=array('I');digest=hashlib.sha256()
                    for m in range(8):
                        domain=gaf[(block*8+m)*370:(block*8+m+1)*370];digest.update(bytes_array(domain))
                        self.full_scattering_math_items+=370
                        if not logl:continue
                        active=[i for i,b in enumerate(domain)if self.fp.nonzero(b)];lo=min([dest,*active]);hi=max([dest,*active])
                        pos.append(len(output)+1);nj.append(hi-lo+1);ij.append(hi+1)
                        for src in range(hi,lo-1,-1):
                            output.append(domain[src]);k=src*8+m;check[k]=self.fp.add(check[k],domain[src])
                        sigw.append(domain[dest])
                    self.evidence.event('FULL_ACTUAL_CONTEXT_SCATTER_DOMAIN',moment=moment,destination_one_based=g,
                        all8x370_domain_SHA256=digest.hexdigest(),Source_LOGL=logl,old_inheritance_applied_after_LOGL=True)
                    if logl:
                        for name,kind,v in zip(names,(2,1,1,1,2),(output,nj,ij,pos,sigw)):
                            self.evidence.compare(self.macro_path(g,name),kind,v,'LIBDEN_SCAT_ACTUAL_LOGL_OLD_MASK',self.model_eligibility)
                    else:
                        for name in names:self.inherit(self.macro_path(g,name))
                del gaf,sigs
            for g in range(1,371):
                path=self.macro_path(g,'CHECK'+cm)
                if self.group_selected(g):self.evidence.compare(path,2,check[(g-1)*8:g*8],'LIBDEN_CHECK_ACTUAL_DESTINATION_WRITE_ORDER',self.model_eligibility)
                else:self.inherit(path)
        require(self.full_scattering_math_items==370*370*8*3,'full original scatter mathematical scope')

    def fission(self):
        # Reconstruct every original allocation step, including zero-density isotopes.
        for isotope in range(1,63):
            mix=self.mix[isotope-1]-1
            if not self.selected(mix+1):continue
            nuf=self.saved.row(self.micro_path(isotope,'NUSIGF'));chi=self.saved.row(self.micro_path(isotope,'CHI--01'))
            if nuf is None or chi is None or nuf['declared_count']<=0 or chi['declared_count']<=0:continue
            values=self.micro(isotope,'CHI--01')
            if not any(self.fp.ratio(x)[0]>0 for x in values):continue
            chosen=next((s for s in range(self.nfissi)if self.indfis[s*8+mix]in(0,isotope)),None)
            if chosen is None:
                chosen=self.nfissi;self.nfissi+=1;require(self.nfissi<=self.observed.old['dimensions']['MAXNFI'],'actual Source MAXNFI')
                self.indfis.extend([0]*8)
            self.indfis[chosen*8+mix]=isotope
            self.evidence.event('ACTUAL_OLD_CONTEXT_FISSION_SLOT_ALLOCATION',isotope=isotope,mix=mix+1,slot=chosen+1,
                actual_density_bits=int(self.density[isotope-1]),density_zero_not_filtered=True)
        require(self.nfissi==8,'complete original32 components/64 index scope, no reduced target')
        self.evidence.compare(('MACROLIB','FISSIONINDEX'),1,self.indfis,'LIBDEN_ORIGINAL_OLD64_SLOT_ALLOCATION',self.model_eligibility)
        self.fission_mapping_validated=True
        for delayed in range(7):
            nn='NUSIGF'if delayed==0 else f'NUSIGF{delayed:02d}';cn='CHI'if delayed==0 else f'CHI{delayed:02d}'
            for g in range(1,371):
                if not self.group_selected(g):self.inherit(self.macro_path(g,nn));self.inherit(self.macro_path(g,cn));continue
                nus=array('I',[0])*256;chis=array('I',[0])*256;known=array('B',[0])*256
                if self.nfiss0>0:
                    # LIBDEN465 explicitly initializes the WHOLE MAXNFI*NESP
                    # slice before copying old components, including new slots.
                    known=array('B',[3])*256
                    oldn=self.old_vector(self.macro_path(g,nn),2,required=delayed==0)
                    oldc=self.old_vector(self.macro_path(g,cn),2,required=delayed==0 or oldn is not None)
                    if oldn is not None:
                        require(oldc is not None and len(oldn)==len(oldc)==self.nbm0*self.nfiss0*4,'complete old fission component count')
                        for c in range(self.nfiss0*4):
                            nus[c*8:c*8+self.nbm0]=oldn[c*self.nbm0:(c+1)*self.nbm0]
                            chis[c*8:c*8+self.nbm0]=oldc[c*self.nbm0:(c+1)*self.nbm0]
                for spectrum in range(4):
                    for slot in range(8):
                        for mix in range(8):
                            isotope=self.indfis[slot*8+mix];k=(slot*4+spectrum)*8+mix
                            if slot+1>self.nfiss0*4 or(isotope and self.selected(mix+1)):
                                nus[k]=chis[k]=0;known[k]=3
                            if not isotope or not self.selected(mix+1):continue
                            den=self.density[isotope-1]
                            for ix,suffix in enumerate(SUFFIXES[:self.nxs]):
                                if delayed and spectrum==0:
                                    last=self.saved.row(self.micro_path(isotope,'NUSIGF06',suffix))
                                    values=None if last is None or last['declared_count']<=0 else self.micro(isotope,nn,suffix=suffix)
                                    lastchi=self.saved.row(self.micro_path(isotope,'CHI06',suffix))
                                    cv=None if ix or lastchi is None or lastchi['declared_count']<=0 else self.micro(isotope,cn,suffix=suffix)
                                elif delayed:values=cv=None
                                else:
                                    values=self.micro(isotope,'NUSIGF',suffix=suffix)
                                    crow=self.saved.row(self.micro_path(isotope,f'CHI--{spectrum+1:02d}',suffix))
                                    cv=self.micro(isotope,f'CHI--{spectrum+1:02d}',suffix=suffix)if ix==0 and crow is not None and crow['declared_count']==370 else None
                                if values is not None and(delayed or self.chi_limits[spectrum]<g<=self.chi_limits[spectrum+1]):
                                    if known[k]&1:nus[k]=self.fp.add(nus[k],self.fp.multiply(values[g-1],den))
                                if cv is not None:chis[k]=cv[g-1];known[k]|=2
                                den=self.fp.multiply(den,self.timfact)
                for name,v,bit in((nn,nus,1),(cn,chis,2)):
                    path=self.macro_path(g,name)
                    if all(k&bit for k in known):self.evidence.compare(path,2,v,'LIBDEN_OLD_INIT_PROMPT_ALL6_DELAYED256',self.model_eligibility)
                    else:
                        actual=self.vector(path,2,256)
                        self.evidence.compare_known_components(path,actual,v,known,bit,self.model_eligibility,'LIBDEN_OLD_INIT_UNDEFINED_COMPONENTS')
                        self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='original Source initialization does not define every component')
        self.lambdas()

    def lambdas(self):
        expected=array('I',[0])*48;known=array('B',[0])*48
        if self.nfiss0>0:
            old=self.old_vector(('MACROLIB','LAMBDA-D'),2,required=False)
            if old is None:known[:6]=array('B',[1])*6
            else:
                require(len(old)<=48,'old Lambda Source extent')
                expected[:len(old)]=old;known[:len(old)]=array('B',[1])*len(old)
        for slot in range(self.nfiss0,8):known[slot*6:(slot+1)*6]=array('B',[1])*6
        for slot in range(8):
            for mix in range(8):
                isotope=self.indfis[slot*8+mix]
                if not isotope or not self.selected(mix+1):continue
                v=self.micro(isotope,'LAMBDA-D',count=6,required=False)
                if v is not None:
                    expected[slot*6:(slot+1)*6]=v;known[slot*6:(slot+1)*6]=array('B',[1])*6
                    self.evidence.event('LAMBDA_ACTUAL_CONTEXT_LAST_WRITE',slot=slot+1,mix=mix+1,isotope=isotope)
        path=('MACROLIB','LAMBDA-D')
        if all(known):self.evidence.compare(path,2,expected,'LIBDEN_LAMBDA48_ACTUAL_OLD_INITIALIZATION_LAST_WRITE',self.model_eligibility)
        else:
            self.evidence.compare_known_components(path,self.vector(path,2,48),expected,known,1,self.model_eligibility,'LIBDEN_LAMBDA_UNDEFINED_OLD_SLOTS')
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',path=list(path),reason='Source initializes only missing old Lambda slot1; other old slots undefined')

    def metadata(self):
        for name in('ADDXSNAME-P0','PARTICLE-NGR','PARTICLE-MC2'):
            row=self.saved.row((name,))
            if row is None:continue
            self.evidence.compare(('MACROLIB',name),row['kind'],b''.join(self.saved.iter_raw(row)),
                'LIBDEN_DIRECT_COPY_ACTUAL_CONTEXT_'+name,self.model_eligibility)
        for name in('PARTICLE','PARTICLE-NAM'):
            if self.saved.row((name,))is not None:
                self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field=name,reason='LCMPTC one-character machine padding requires compiled control; no raw-copy substitution')
        energy=self.vector(('ENERGY',),2,371)
        if not self.fp.nonzero(energy[-1]):energy[-1]=self.fp.f64_to32(1e-5)
        if self.maskk:
            self.inherit(('MACROLIB','ENERGY'));self.inherit(('MACROLIB','SIGNATURE'))
            state=array('i',self.old_state);state[1]=max(self.nbm0,8);state[2]=max(state[2],3);state[3]=32;state[4]=max(state[4],18)
        else:
            state=array('i',[0])*40;state[:5]=array('i',[370,8,3,32,18])
            self.evidence.compare(('MACROLIB','ENERGY'),2,energy,'LIBDEN_FRESH_ONLY_ENERGY',self.model_eligibility)
            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='SIGNATURE',reason='fresh LCMPTC twelve-character Source-machine padding not runtime qualified')
        itranc=self.observed.old['dimensions']['ITRANC'];state[5]=2 if itranc else 0;state[6]=6;state[7]=0
        state[8]=int(self.scalar_presence.get('STRD',False));state[9]=int(self.scalar_presence.get('NTOT1',False));state[10:]=array('i',[0])*30
        if self.old_saved is not None and self.old_saved.row(('MACROLIB','SPH'))is not None:state[13]=1
        self.evidence.compare(('MACROLIB','STATE-VECTOR'),1,state,'LIBDEN_OLD_STATE40_MAXIMA_ACTUAL_FLAGS',self.model_eligibility)
        before=self.observed.before['fields']['TMPDAY'];actual=self.observed.old['fields']['TMPDAY'];expected=array('I',before)
        if self.maskk:
            timestamp=self.old_vector(('MACROLIB','TIMESTAMP'),2,required=False)
            if timestamp is not None and 0<len(timestamp)<=3:
                if len(timestamp)!=3:
                    self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='TIMESTAMP',reason='LCMGET short old timestamp leaves uninitialized OLDTIM tail')
                else:expected=timestamp
        require(expected==actual,'LIBMIX actual old timestamp overwrite, no final self proof')
        self.evidence.compare(('MACROLIB','TIMESTAMP'),2,actual,'LIBMIX_OLD_TIMESTAMP_LIBDEN_WRITE',self.model_eligibility)
        volumes=self.vector(('ISOTOPESVOL',),2,62,required=False)
        if volumes is not None:
            v=array('I',[0])*8
            for i in range(62):v[self.mix[i]-1]=volumes[i]
            self.evidence.compare(('MIXTURESVOL',),2,v,'LIBDEN_LAST_ISOTOPE_VOLUME',self.model_eligibility)
        else:
            v=self.observed.before['fields'].get('ROOT_MIXTURESVOL_BEFORE')
            if v is not None:self.evidence.compare(('MIXTURESVOL',),2,v,'LIBDEN_ACTUAL_PRECALL_ROOT_VOLUME_UNCHANGED',self.model_eligibility)
        if v is not None:
            self.evidence.compare(('MACROLIB','VOLUME'),2,v,'LIBDEN_VOLUME_COPY_ACTUAL_CONTEXT',self.model_eligibility)
            for name,out in(('NWT0','FLUX-INTG'),('NWT1','FLUX-INTG-P1')):
                flux=array('I',[0])*(370*8);any_present=False
                for isotope in range(1,63):
                    row=self.saved.row(self.micro_path(isotope,name))
                    if row is None or row['declared_count']!=370:
                        self.evidence.event('FULL_ORIGINAL_FLUX_PRESENCE_COUNT',isotope=isotope,name=name,original=row);continue
                    values=self.micro(isotope,name);any_present=True;mix=self.mix[isotope-1]-1
                    for g,bits in enumerate(values):flux[g*8+mix]=self.fp.multiply(bits,v[mix])
                    self.evidence.event('FULL_ACTUAL_FLUX_LAST_WRITE',isotope=isotope,mix=mix+1,field=name,density_not_used=True)
                for g in range(1,371):
                    path=self.macro_path(g,out)
                    if any_present:self.evidence.compare(path,2,flux[(g-1)*8:g*8],'LIBDEN_FLUX_LAST_WRITE_ALL_GROUPS',self.model_eligibility)
                    else:self.inherit(path)
        else:
            self.inherit(('MACROLIB','VOLUME'))
            for g in range(1,371):
                for out in('FLUX-INTG','FLUX-INTG-P1'):self.inherit(self.macro_path(g,out))
        # Every genuinely unmodified old field is compared from OLD, including
        # full SPH words. Potential producers reserved above are never silently
        # inherited after a phase error or an unsupported computation.
        if self.maskk:
            for item in self.old_saved.iter_all():
                row=item['record'];path=tuple(row['path'])
                if path[:1]==('MACROLIB',)and row['kind']not in(0,10,99)and path not in self.reserved:self.inherit(path)
        self.evidence.event('COMPLETE_CONTEXT_MODEL_BOUNDARY',all_original_scope_retained=True,
            historical_LIBDEN_machine_float_replay=False,compiled_Source_binary_link_qualified=False,
            actual_old_macro_input=self.maskk,actual_STATE9=self.ldiff,actual_tracking_MASK_proved=True,
            SPH_one_never_assumed=True,actual_complete_SPH_selection= self.observed.complete_sph_call_selection_proved)

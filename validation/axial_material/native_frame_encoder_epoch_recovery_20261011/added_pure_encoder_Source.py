def complete_frame_self_accounted_UTF8(event,account,budget):
    """Encode each complete payload value once; solve only the size integer.

    The caller owns this freshly returned account, which has just been inserted
    at the one top-level diagnostic key. JSON key/value fragments retain the
    standard encoder's exact insertion order, separators, UTF8, float spelling,
    and nonfinite refusal. No original resource or clock method is called here
    except the same caller's budget. No frame field or payload is discarded.
    """
    require(event['actual_diagnostic_write_byte_account_before']is account
        and type(account['additional_record_bytes'])is int
        and account['additional_record_bytes']>=0,'owned diagnostic byte-size integer')
    budget()
    parts=[b'{'];slot=None
    for ordinal,(key,value)in enumerate(event.items()):
        budget()
        if ordinal:parts.append(b', ')
        if key!='actual_diagnostic_write_byte_account_before':
            parts.append(json.dumps({key:value},ensure_ascii=False,
                allow_nan=False)[1:-1].encode('utf-8'))
            continue
        # Isolate this exact owned integer structurally; no text search, marker,
        # collision assumption, full-event re-encoding, or payload truncation.
        pair=json.dumps({key:None},ensure_ascii=False,allow_nan=False)[1:-1]
        parts.append(pair[:-4].encode('utf-8'));parts.append(b'{')
        for inner_ordinal,(inner_key,inner_value)in enumerate(account.items()):
            budget()
            if inner_ordinal:parts.append(b', ')
            if inner_key=='additional_record_bytes':
                pair=json.dumps({inner_key:0},ensure_ascii=False,
                    allow_nan=False)[1:-1]
                parts.append(pair[:-1].encode('utf-8'))
                slot=len(parts);parts.append(b'')
            else:
                parts.append(json.dumps({inner_key:inner_value},ensure_ascii=False,
                    allow_nan=False)[1:-1].encode('utf-8'))
        parts.append(b'}')
    parts.append(b'}\n')
    require(slot is not None,'one complete owned diagnostic byte-size slot')
    base=sum(map(len,parts))
    size=base+len(str(account['additional_record_bytes']))
    for serialization in range(8):
        budget()
        next_size=base+len(str(size))
        if next_size==size:break
        size=next_size
    else:raise ValueError('complete exact byte-length fixed point did not stabilize')
    budget()
    account['additional_record_bytes']=size
    parts[slot]=str(size).encode('ascii')
    raw=b''.join(parts)
    require(len(raw)==size,'complete exact self-accounted JSON-line byte length')
    budget();return raw


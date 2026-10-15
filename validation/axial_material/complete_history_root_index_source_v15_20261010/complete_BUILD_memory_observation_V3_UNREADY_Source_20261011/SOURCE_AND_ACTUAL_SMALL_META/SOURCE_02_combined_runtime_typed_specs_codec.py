"""Lossless metadata encoding only; no filesystem/PASS or hash-cache semantics.

Every original owner and its map iteration order remains a separate row.
Namespace file maps share representation only when their full ordered contents
are equal. This does not merge namespaces, owners, paths or payload reads.
"""
SCHEMA = 'AXMAT_COMBINED_RUNTIME_LOSSLESS_TYPED_INPUT_METADATA_ENCODING_V1'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pack_specs(specs):
    need(isinstance(specs, dict) and 'owners' in specs and 'namespace_specs' in specs, 'typed specs required')
    pins = []
    pin_indices = {}

    def index(path, sha):
        token = (path, sha)
        if token not in pin_indices:
            pin_indices[token] = len(pins)
            pins.append([path, sha])
        return pin_indices[token]

    rows = []
    for owner in specs['owners']:
        need(set(owner) == {'owner', 'category', 'expected_files'}, 'only original normalized owner shape supported')
        need(isinstance(owner['expected_files'], dict), 'owner full expected map required')
        rows.append([owner['owner'], owner['category'],
                     [index(path, sha) for path, sha in owner['expected_files'].items()]])
    pools = []
    pool_indices = {}
    namespaces = []
    for namespace in specs['namespace_specs']:
        need(isinstance(namespace, dict) and isinstance(namespace.get('files'), dict), 'original namespace required')
        # Ordered literal expected pins, with no resolution, stat or current SHA.
        ids = tuple(index(path, sha) for path, sha in namespace['files'].items())
        if ids not in pool_indices:
            pool_indices[ids] = len(pools)
            pools.append(list(ids))
        record = {key: value for key, value in namespace.items() if key != 'files'}
        need('files_pool' not in record, 'reserved encoding field conflict')
        record['files_pool'] = pool_indices[ids]
        namespaces.append(record)
    return dict(schema=SCHEMA, scope='LOSSLESS_METADATA_REPRESENTATION_ONLY',
        metadata={key: value for key, value in specs.items() if key not in ('owners', 'namespace_specs')},
        expected_pin_symbols=pins, original_owner_rows=rows,
        namespace_file_map_pools=pools, original_namespace_rows=namespaces,
        all_logical_owner_rows_retained=True, no_expected_map_or_namespace_union=True,
        filesystem_or_payload_observation_created=False, science_or_live_resource_credit_created=False)


def unpack_specs(value):
    need(isinstance(value, dict) and set(value) == {'schema', 'scope', 'metadata',
        'expected_pin_symbols', 'original_owner_rows', 'namespace_file_map_pools', 'original_namespace_rows',
        'all_logical_owner_rows_retained', 'no_expected_map_or_namespace_union',
        'filesystem_or_payload_observation_created', 'science_or_live_resource_credit_created'}, 'encoding fields differ')
    need(value['schema'] == SCHEMA and value['scope'] == 'LOSSLESS_METADATA_REPRESENTATION_ONLY', 'encoding contract changed')
    need(value['all_logical_owner_rows_retained'] is True and value['no_expected_map_or_namespace_union'] is True
         and value['filesystem_or_payload_observation_created'] is False
         and value['science_or_live_resource_credit_created'] is False, 'encoding scope changed')
    pins = value['expected_pin_symbols']
    need(isinstance(pins, list), 'pin symbol list required')
    for pair in pins:
        need(isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, str) for v in pair), 'literal expected pair required')
    need(len({tuple(v) for v in pins}) == len(pins), 'duplicate pin symbols')

    def full_map(ids):
        need(isinstance(ids, list) and all(type(i) is int and 0 <= i < len(pins) for i in ids), 'invalid pin symbol index')
        need(len({pins[i][0] for i in ids}) == len(ids), 'duplicate original expected path')
        return {pins[i][0]: pins[i][1] for i in ids}

    owners = []
    need(isinstance(value['original_owner_rows'], list), 'owner row list required')
    for row in value['original_owner_rows']:
        need(isinstance(row, list) and len(row) == 3 and isinstance(row[0], str) and isinstance(row[1], str), 'invalid owner row')
        owners.append(dict(owner=row[0], category=row[1], expected_files=full_map(row[2])))
    pools = value['namespace_file_map_pools']
    need(isinstance(pools, list), 'namespace pool list required')
    need(len({tuple(v) for v in pools if isinstance(v, list)}) == len(pools), 'duplicate or invalid namespace pool')
    maps = [full_map(ids) for ids in pools]
    namespaces = []
    need(isinstance(value['original_namespace_rows'], list), 'namespace row list required')
    for row in value['original_namespace_rows']:
        need(isinstance(row, dict) and 'files_pool' in row and 'files' not in row, 'invalid namespace row')
        i = row['files_pool']
        need(type(i) is int and 0 <= i < len(maps), 'invalid namespace pool index')
        namespace = {key: item for key, item in row.items() if key != 'files_pool'}
        # Sharing this immutable expected-map representation grants no mutable
        # caller permission. Copy the map; every namespace remains a full row.
        namespace['files'] = dict(maps[i])
        namespaces.append(namespace)
    metadata = value['metadata']
    need(isinstance(metadata, dict) and 'owners' not in metadata and 'namespace_specs' not in metadata, 'metadata shape differs')
    result = dict(metadata, owners=owners, namespace_specs=namespaces)
    need(pack_specs(result) == value, 'noncanonical encoding, unused symbols, altered rows or pools')
    return result

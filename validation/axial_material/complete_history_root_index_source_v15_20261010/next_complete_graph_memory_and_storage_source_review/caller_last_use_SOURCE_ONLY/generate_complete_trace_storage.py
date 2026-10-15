"""Source-only complete canonical-file/trace storage helper. No API execution."""
import ast
import hashlib
import json
from pathlib import Path

OUT=Path('/private/tmp/axmat_v15_complete_wire_and_trace_table_source_only_20261010')
OUT.mkdir(exist_ok=False)
P=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py')
FRESH=Path(__file__).parent/'fresh_complete_wire_helper.UNREADY.py'
parent=P.read_text();fresh=FRESH.read_text()
assert hashlib.sha256(parent.encode()).hexdigest()=='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
assert fresh.startswith(parent)
def sha(data):return hashlib.sha256(data).hexdigest()
def ident(p):
    s=p.lstat();return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size_bytes=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def pin(p):
    a=ident(p);b=p.read_bytes();z=ident(p);assert a==z
    return dict(path=str(p),sha256=sha(b),size_bytes=len(b),identity=a)
def funcs(text):
    ls=text.splitlines(keepends=True)
    return {n.name:''.join(ls[n.lineno-1:n.end_lineno])for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
def write(name,data):
    with (OUT/name).open('xb')as f:f.write(data)
def doc(name,v):write(name,(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
inputpins=[pin(P),pin(FRESH)]
add=r'''

COMPLETE_GRAPH_TRACE_TABLE_SOURCE_STATUS = "UNREADY_SOURCE_ONLY_NO_RUNTIME_QUALIFICATION"
COMPLETE_GRAPH_TRACE_TABLE_STORAGE_SCHEMA = "AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1"
READ_TRACE_RECORD_TABLE_STORAGE_SCHEMA = "AXMAT_COMPLETE_READ_TRACE_ORDERED_RECORD_AND_STRING_TABLE_V1"


def _trace_storage_nonstring_json(value):
    """Validate non-string cells without copying any nested JSON container."""
    _require(type(value) is not str, "trace cell disagrees with string type discriminator")
    pending = [value]
    while pending:
        part = pending.pop()
        kind = type(part)
        if kind is dict:
            _require(all(type(key) is str for key in part), "trace nested JSON object keys must be strings")
            pending.extend(part.values())
        elif kind is list:
            pending.extend(part)
        elif kind is int:
            str(part)  # same decimal conversion limit as original JSON
        elif kind is float:
            _require(math.isfinite(part), "trace nested JSON values must be finite")
        else:
            _require(kind in (str, bool, type(None)), "trace cells must preserve builtin JSON types")


def _encode_read_trace_record_table(records):
    """Lossless ordered fields plus tagged scalar string interning; no mutation."""
    _require(type(records) is list, "complete trace records must be a list")
    for record in records:
        _require(type(record) is dict and all(type(key) is str for key in record),
                 "complete trace record must be a builtin JSON object")
    columns = sorted({key for record in records for key in record})
    column_ids = {key: index for index, key in enumerate(columns)}
    layouts, layout_ids, strings, string_ids, rows = [], {}, [], {}, []
    for record in records:
        signature = tuple((column_ids[key], type(value) is str) for key, value in record.items())
        if signature not in layout_ids:
            layout_ids[signature] = len(layouts)
            layouts.append([[column, string_type] for column, string_type in signature])
        cells = []
        for value in record.values():
            if type(value) is str:
                if value not in string_ids:
                    string_ids[value] = len(strings)
                    strings.append(value)
                cells.append(string_ids[value])
            else:
                _trace_storage_nonstring_json(value)
                cells.append(value)
        rows.append([layout_ids[signature], *cells])
    return {"schema": READ_TRACE_RECORD_TABLE_STORAGE_SCHEMA, "columns": columns,
            "layouts": layouts, "strings": strings, "row_count": len(records), "rows": rows}


def _decode_read_trace_record_table(table, *, _consume=False):
    """Decode all fields/types/order; privately release only a new parsed table."""
    _require(type(_consume) is bool, "invalid private trace storage consume flag")
    _require(type(table) is dict and set(table) == {"schema", "columns", "layouts", "strings", "row_count", "rows"}
             and table.get("schema") == READ_TRACE_RECORD_TABLE_STORAGE_SCHEMA,
             "invalid complete trace table header")
    columns, layouts, strings, rows = table["columns"], table["layouts"], table["strings"], table["rows"]
    _require(type(columns) is list and all(type(key) is str for key in columns)
             and columns == sorted(set(columns)), "invalid trace storage columns")
    _require(type(strings) is list and all(type(value) is str for value in strings)
             and len(strings) == len(set(strings)), "invalid trace storage string table")
    _require(type(layouts) is list and type(rows) is list
             and type(table["row_count"]) is int and table["row_count"] >= 0
             and table["row_count"] == len(rows), "invalid complete trace row count")
    signatures = set()
    for layout in layouts:
        _require(type(layout) is list, "invalid trace storage layout")
        seen = set()
        for field in layout:
            _require(type(field) is list and len(field) == 2 and type(field[0]) is int
                     and 0 <= field[0] < len(columns) and type(field[1]) is bool,
                     "invalid trace storage field/type discriminator")
            _require(field[0] not in seen, "duplicate trace layout field")
            seen.add(field[0])
        signature = tuple((field[0], field[1]) for field in layout)
        _require(signature not in signatures, "duplicate trace storage layout")
        signatures.add(signature)
    result, used_layouts, used_strings, used_columns = [], set(), set(), set()
    for index, row in enumerate(rows):
        _require(type(row) is list and row and type(row[0]) is int
                 and 0 <= row[0] < len(layouts), "invalid trace storage row/layout index")
        lid = row[0]
        if lid not in used_layouts:
            _require(lid == len(used_layouts), "trace layouts not in first-occurrence order")
            used_layouts.add(lid)
        layout = layouts[lid]
        _require(len(row) == 1 + len(layout), "invalid trace storage row field count")
        record = {}
        for position, (column, string_type) in enumerate(layout, 1):
            value = row[position]
            if string_type:
                _require(type(value) is int and 0 <= value < len(strings), "invalid trace storage string index")
                if value not in used_strings:
                    _require(value == len(used_strings), "trace strings not in first-occurrence order")
                    used_strings.add(value)
                value = strings[value]
            else:
                _trace_storage_nonstring_json(value)
            record[columns[column]] = value
            used_columns.add(column)
        result.append(record)
        if _consume:
            rows[index] = None
    _require(len(used_layouts) == len(layouts) and len(used_strings) == len(strings)
             and len(used_columns) == len(columns), "unused trace storage symbols or layouts")
    if _consume:
        rows.clear()
        layouts.clear()
        strings.clear()
        columns.clear()
    if result:
        del row, record, layout
    del rows, layouts, strings, columns
    return result


def encode_complete_graph_table_storage(graph):
    """Borrow every original graph value; table only canonical pins and trace."""
    canonical = encode_canonical_file_table_storage(graph)
    view = canonical["graph"]
    trace = view.get("read_trace")
    _require(type(trace) is dict and type(trace.get("records")) is list,
             "complete graph trace descriptor required for storage")
    stored_trace = dict(trace)
    stored_trace["records"] = _encode_read_trace_record_table(trace["records"])
    view["read_trace"] = stored_trace
    return {"schema": COMPLETE_GRAPH_TRACE_TABLE_STORAGE_SCHEMA, "graph": view}


def decode_complete_graph_table_storage(storage, *, _consume=False):
    """Inverse full canonical pins plus trace; original content SHA is binding."""
    _require(type(_consume) is bool, "invalid private complete graph storage consume flag")
    _require(type(storage) is dict and set(storage) == {"schema", "graph"}
             and storage.get("schema") == COMPLETE_GRAPH_TRACE_TABLE_STORAGE_SCHEMA,
             "invalid complete graph trace storage header")
    graph = storage["graph"]
    _require(type(graph) is dict and graph.get("schema") == WIRE_GRAPH_SCHEMA
             and graph.get("scope") == INPUT_SCOPE,
             "invalid original decoded graph schema/scope")
    table = graph.get("canonical_files")
    _require(type(table) is dict and set(table) == {"columns", "rows"}
             and type(table["columns"]) is list
             and table["columns"] == list(CANONICAL_FILE_TABLE_STORAGE_COLUMNS)
             and type(table["rows"]) is list,
             "invalid canonical-file table header/columns")
    pins = []
    rows = table["rows"]
    for index, row in enumerate(rows):
        values = _canonical_file_storage_values(row)
        pins.append({key: value for key, value in zip(CANONICAL_FILE_TABLE_STORAGE_COLUMNS, values)})
        if _consume:
            rows[index] = None
    if _consume:
        rows.clear()
    del rows
    if pins:
        del row, values
    trace = graph.get("read_trace")
    _require(type(trace) is dict and "records" in trace, "invalid complete graph trace descriptor")
    records = _decode_read_trace_record_table(trace["records"], _consume=_consume)
    restored_trace = dict(trace)
    restored_trace["records"] = records
    restored = dict(graph)
    restored["canonical_files"] = pins
    restored["read_trace"] = restored_trace
    _require(_sha(restored.get("content_sha256")) == _content_digest(restored),
             "decoded complete graph content changed")
    return restored
'''
candidate=fresh+add
edits=[]
old='    if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:\n        return decode_canonical_file_table_storage(result, _consume=True)\n    return result'
new='    if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:\n        return decode_canonical_file_table_storage(result, _consume=True)\n    if type(result) is dict and result.get("schema") == COMPLETE_GRAPH_TRACE_TABLE_STORAGE_SCHEMA:\n        return decode_complete_graph_table_storage(result, _consume=True)\n    return result'
assert candidate.count(old)==2
candidate=candidate.replace(old,new)
edits=[dict(old=old,new=new,occurrences=2)]
compile(candidate,'complete_graph_wire_trace_tables.UNREADY.py','exec')
reverse=candidate
assert reverse.endswith(add)
reverse=reverse[:-len(add)]
assert reverse.count(new)==2
reverse=reverse.replace(new,old)
assert reverse==fresh
assert fresh[:len(parent)]==parent
oldfuncs=funcs(parent);newfuncs=funcs(candidate)
changed={'strict_json','_parse_strict_json_payload'}
assert all(newfuncs[n]==v for n,v in oldfuncs.items() if n not in changed)
assert all(newfuncs[n].replace(new,old)==oldfuncs[n]for n in changed)
assert [pin(P),pin(FRESH)]==inputpins
path='complete_input_graph_fresh_wire_canonical_and_trace_tables.UNREADY.py'
write(path,candidate.encode())
doc('source_complete_inverse_proof.json',dict(schema='AXMAT_COMPLETE_GRAPH_TRACE_TABLE_FRESH_WIRE_SOURCE_INVERSE_V1',
    status='UNREADY_SOURCE_ONLY',parent=inputpins[0],intermediate=inputpins[1],
    parent_complete_inverse_exact=True,append_only_fresh_producer_region=True,append_only_codec_region=True,
    parser_edits=edits,all_other_parent_function_and_class_segments_byteexact=len(oldfuncs)-2,
    originals_unchanged=sorted(set(oldfuncs)-changed),syntax_compile_without_exec=True,
    new_api_names=['create_fresh_complete_wire_graph','encode_complete_graph_table_storage','decode_complete_graph_table_storage'],
    MAX_JSON_BYTES=67108864,read_trace_or_owners_or_requirement_rows_filtered=False))
doc('REPORT.json',dict(schema='AXMAT_COMPLETE_GRAPH_FRESH_WIRE_AND_FULL_TRACE_STORAGE_SOURCE_PLAN_V1',
    status='UNREADY_SOURCE_ONLY',helper=pin(OUT/path),parents=inputpins,
    fresh_api='create_fresh_complete_wire_graph',storage_encoder='encode_complete_graph_table_storage',
    decoder='decode_complete_graph_table_storage',new_storage_schema='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1',
    complete_graph_scope_preserved=True,original_semantic_and_wire_content_digest_preserved_by_design=True,
    trace_table=dict(columns='sorted unique whole union of original record keys',
       layouts='first occurrence ordered [column id, exact bool string discriminator] pairs',
       strings='first occurrence unique complete original top-level string scalars including path/cwd/empty strings',
       rows='layout id followed by every original field value or strictly non-bool string index',
       missing_vs_null_distinct=True,original_field_insertion_order_preserved=True,
       duplicate_records_and_attempt_count_preserved=True,nested_descriptor_JSON_borrowed_without_change=True,
       subprocess_records_and_all_other_trace_fields_borrowed_without_change=True,
       strict_full_row_count_exact_shape_indexes_used_symbols_and_first_occurrence_guards=True),
    ownership=dict(default_encode_or_decode_does_not_mutate_inputs=True,
       owned_consume_only_new_parsed_container=True,consume_releases_completed_rows_and_tables=True,
       ordinary_JSON_and_old_storage_wrapper_paths_same=True,
       unchanged_public_graph_create_verify_wire_encode_and_consumer_functions=True),
    root_model_only=dict(full_new_trace_records=63379,full_new_trace_bytes=35211756,
       prior_graph_trace_records=62332,prior_graph_trace_bytes=29667957,old_trace_replaced_graph_model_bytes=72102742,
       actual_V15_graph_created=False,new_encoded_bytes=None,new_decoded_equivalence_tested=False),
    required_next_root_owned_pure_controls=['full saved graph/whole new trace model table size below original64MiB',
       'all complete original decoded values/types/order/floatbits/wirecontent/legacysemantic and duplicate records',
       'default nonmutation and both strict owned decode entrance release/error controls',
       'missing vs null/string vs integer vs bool, bad column/layout/row/string indexes and noncanonical unused/order symbols',
       'fresh complete producer original public full accepted graph semantics and new guard error order'],
    pure_source_compile_only=True,helper_imported_or_called=False,fixtures_or_business_executed=False,
    project_written=False,new_GRAPH_BUILD_INPUT_NATIVE_AAA_ABA_or_RSS_credit=False,
    budgets_unchanged=dict(json_read_bytes=67108864,rss_mib=512,children=1,retries=0)))
write('REPORT.txt',('完整 trace 的透明表编码源码草稿；没有截记录或提取子集。\n'
    '顶层 record 使用全部列名、顺序布局、严格字符串标签和全字符串表，保留缺失/null、所有类型、字段与行顺序、重复、attempts。嵌套 descriptor 与 subprocess 原值保留。\n'
    '原 create_graph/encode_graph_wire/verify_graph/phase/math/resource/consumer 逐字保留；仅两严格 JSON wrapper 添加新 schema 解码路由。独立 fresh producer 使用完整原 phase 与 coverage/trace 门。\n'
    '默认 pure encode/decode 不修改调用者；私有 consume 只用于 fresh parsed document，逐行释放后清空表；新图 wire 与旧 legacy digest 保留。\n'
    '所有输出 UNREADY；只做 AST/compile-source，不执行 helper、fixture 或业务。实际体积、完整 roundtrip 与 RSS 尚未验证；Root 后续受限纯元数据控制为必需。原64MiB/512MiB门不改。\n').encode())
print(json.dumps(dict(status='UNREADY_SOURCE_ONLY',helper=pin(OUT/path),proof=pin(OUT/'source_complete_inverse_proof.json'),report=pin(OUT/'REPORT.json')),separators=(',',':')))

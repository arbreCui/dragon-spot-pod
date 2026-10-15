from pathlib import Path
import json
O=Path('/Users/wen/spot/validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-20261010')
manifest=json.loads((O/'payload_manifest.json').read_text())
payload_paths={p.name:p for p in O.iterdir() if p.is_file()}
assert set(payload_paths)==set(manifest['files'])|{'payload_manifest.json'}

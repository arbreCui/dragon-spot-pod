"""Source-only reproducible region replay; never imports or calls the candidate."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser()
p.add_argument('--out',required=True)
a=p.parse_args()
q=Path(__file__).parent/'source_finite_inverse_839.json'
proof=json.loads(q.read_text())
source=Path(proof['parent']['path']).read_bytes()
assert hashlib.sha256(source).hexdigest()==proof['parent']['sha256']
s=source.decode()
for e in proof['regions']:
 assert s.count(e['old'])==e['count']
 s=s.replace(e['old'],e['new'],e['count'])
assert hashlib.sha256(s.encode()).hexdigest()==proof['candidate']['sha256']
out=Path(a.out)
assert out.is_absolute() and str(out).startswith('/private/tmp/') and not out.exists()
with out.open('x') as f:f.write(s)
print(hashlib.sha256(out.read_bytes()).hexdigest())

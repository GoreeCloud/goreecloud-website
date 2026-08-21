from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'blog'
required = ['index.html','style.css','site.js','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing blog site files: {missing}')
index = (SITE/'index.html').read_text()
headers = (SITE/'_headers').read_text()
for marker in ['GoreeCloud Blog','Building an owned cloud, one layer at a time.','GoreeCloud is becoming a software ecosystem','Everkeep','Glaze UI','Homelab']:
    if marker not in index:
        raise SystemExit(f'Missing required blog marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden blog runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Blog CSP is not fail-closed enough')
print('GoreeCloud Blog site validation passed.')

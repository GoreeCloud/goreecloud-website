from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'archive'
required = ['index.html','style.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing archive site files: {missing}')
index = (SITE/'index.html').read_text()
headers = (SITE/'_headers').read_text()
for marker in [
    'GoreeCloud Archive',
    'Preserving the evolution of GoreeCloud.',
    'Archive policy',
    'Public history is curated, not mirrored.',
    'Development evidence era · August 24, 2026',
    'Fold identity and the first persistent Drive milestone land',
    'Search advances through RC #09 validation',
    '50.2-rc.2 source line',
]:
    if marker not in index:
        raise SystemExit(f'Missing required archive marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden archive runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Archive CSP is not fail-closed enough')
print('GoreeCloud Archive site validation passed.')

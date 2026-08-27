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
    'Native application mandate · August 24, 2026',
    'Source-control independence · August 25, 2026',
    'Historical direction: self-hosted Gitea as the planned permanent authority',
    'superseded on August 27, 2026',
    'Platform refresh · August 27, 2026',
    '53 repositories: 39 public and 14 private',
    'Glaze UI 1.5.0 becomes the current Stable baseline',
    'GoreeCloud Code becomes the first-party source-control product',
    'Forgejo becomes the initial replaceable infrastructure foundation',
    'Public Center model · August 27, 2026',
    'Design Center',
    'Privacy Center',
    'Security Center',
    'Continuity Center',
    'Mesh Center',
]:
    if marker not in index:
        raise SystemExit(f'Missing required archive marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden archive runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Archive CSP is not fail-closed enough')
print('GoreeCloud Archive site validation passed.')
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'archive'
required = ['index.html','style.css','glaze-v1.1.0.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing archive site files: {missing}')

index = (SITE/'index.html').read_text(encoding='utf-8')
error_page = (SITE/'404.html').read_text(encoding='utf-8')
css = (SITE/'glaze-v1.1.0.css').read_text(encoding='utf-8')
headers = (SITE/'_headers').read_text(encoding='utf-8')

for marker in [
    'GoreeCloud Archive',
    'Preserving the evolution of GoreeCloud.',
    'Public history is curated, not mirrored.',
    'Native application mandate · August 24, 2026',
    'Historical direction: self-hosted Gitea as the planned permanent authority',
    'superseded on August 27, 2026',
    '53 repositories: 39 public and 14 private',
    'Glaze UI 2.0.0 becomes the Stable baseline of that period',
    'At that point Glaze UI 2.1 remained Candidate',
    '56 repositories: 40 public and 16 private',
    'GoreeCloud Identity expands the substantive platform model to six systems',
    'Facet becomes the current official Glaze UI identity',
    'Glaze UI 2.1.0 becomes the Stable target of that period',
    'reviewed state of that date',
    'Current web baseline · September 4, 2026',
    'GLAZE UI V1.1 becomes the Stable target for a 13-destination public ecosystem',
    'GLAZE UI V1.1 / 1.1.0',
    '13 destinations across nine repositories',
    'Manager’s public information surface',
    'Mesh Center',
    'Identity Center',
]:
    if marker not in index:
        raise SystemExit(f'Missing required archive marker: {marker}')

for page_name, page in [('index',index),('404',error_page)]:
    for marker in ['data-glaze-version="1.1"','name="goreecloud-glaze-ui" content="1.1.0"','data-glaze-ui="1.1.0"','glaze-v1.1.0.css','glaze-canvas']:
        if marker not in page:
            raise SystemExit(f'{page_name} missing GLAZE UI V1.1 marker: {marker}')
    for stale in ['data-glaze-ui="1.5.0"','data-glaze-ui="2.0.0"','data-glaze-ui="2.1.0"','data-glaze-ui="2.2.0"']:
        if stale in page:
            raise SystemExit(f'{page_name} still activates a superseded Glaze UI bundle')

for marker in [
    'GLAZE UI V1.1 / 1.1.0 Stable consumer integration',
    '15cc76d2bcd4065552dc31c77145b63f34d9e7b2',
    '--glz1-target-shell: 48px',
    '--glz1-target-assisted: 56px',
    '--glz11-deep-teal:',
    'prefers-reduced-motion',
    'prefers-reduced-transparency',
    'prefers-contrast: more',
    'forced-colors: active',
]:
    if marker not in css:
        raise SystemExit(f'Missing Archive GLAZE UI V1.1 web-layer marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden archive runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Archive CSP is not fail-closed enough')

print('GoreeCloud Archive historical sequence and current GLAZE UI V1.1 portfolio validation passed.')

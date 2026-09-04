from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'blog'
required = ['index.html','style.css','site.js','glaze-v1.1.0.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing blog site files: {missing}')

index = (SITE/'index.html').read_text(encoding='utf-8')
error_page = (SITE/'404.html').read_text(encoding='utf-8')
css = (SITE/'glaze-v1.1.0.css').read_text(encoding='utf-8')
headers = (SITE/'_headers').read_text(encoding='utf-8')

for marker in [
    'GoreeCloud Blog',
    'Building an owned cloud, one layer at a time.',
    'current connected GoreeCloud source inventory spans 57 repositories: 40 public and 17 private',
    'GoreeCloud Index',
    'Forgejo is the initial replaceable infrastructure foundation',
    'GLAZE UI V1.1 is the current Stable production target',
    'GLAZE UI V1.1 / 1.1.0 is the current Stable GoreeCloud design-system baseline',
    'deep and mineral teal',
    '48px standard targets',
    '56px Touch Assistance',
    'Facet is the current official Glaze UI identity',
    'GoreeCloud Identity',
    'Design Center',
    'Privacy Center',
    'Security Center',
    'Continuity Center',
    'Mesh Center',
    'Identity Center',
    'September 4, 2026',
]:
    if marker not in index:
        raise SystemExit(f'Missing required blog marker: {marker}')

for stale in [
    'Glaze UI 2.1 is the current Stable production target',
    'Glaze UI 2.1.0 is the current Stable GoreeCloud design-system baseline',
    'Glaze UI 2.1 remains Candidate',
    'Glaze UI 2.0 is the current Stable production target',
    'the five substantive platform systems',
    'Fold identity is the canonical Glaze UI mark',
]:
    if stale in index:
        raise SystemExit(f'Stale Blog content remains: {stale}')

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
    '--glz11-soft-aqua:',
    'prefers-reduced-motion',
    'prefers-reduced-transparency',
    'prefers-contrast: more',
    'forced-colors: active',
]:
    if marker not in css:
        raise SystemExit(f'Missing Blog GLAZE UI V1.1 web-layer marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden blog runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Blog CSP is not fail-closed enough')
print('GoreeCloud Blog current portfolio, six-system model, Facet identity, and GLAZE UI V1.1 validation passed.')

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'blog'
required = ['index.html','style.css','site.js','glaze-ui-2.2.0.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing blog site files: {missing}')

index = (SITE/'index.html').read_text(encoding='utf-8')
error_page = (SITE/'404.html').read_text(encoding='utf-8')
css = (SITE/'glaze-ui-2.2.0.css').read_text(encoding='utf-8')
headers = (SITE/'_headers').read_text(encoding='utf-8')

for marker in [
    'GoreeCloud Blog',
    'Building an owned cloud, one layer at a time.',
    'GoreeCloud’s public platform model moves to evidence-backed conformance',
    'Glaze UI 2.2.0 is the current Stable design-system baseline',
    'seven Integral Platform Systems',
    'GoreeCloud Manager',
    'GoreeCloud Code replaces the idea of a forge as the product boundary',
    'Forgejo is the initial replaceable infrastructure foundation',
    'Documents, Messenger, Gateway, Quill, File Manager, Maps, and App Store broaden the native portfolio',
    'Glaze UI 2.2 is the current Stable production target',
    'Solid where users read. Glazed where users interact.',
    'one dominant Glaze panel',
    'historical rollback baseline',
    'repository-local acceptance',
    'Facet is the current official Glaze UI identity',
    'Identity joins the public platform model',
    'GoreeCloud Identity',
    'Historical direction: self-hosted Gitea as the planned permanent authority',
    'superseded August 27, 2026',
    'Design Center',
    'Privacy Center',
    'Security Center',
    'Continuity Center',
    'Mesh Center',
    'Identity Center',
    'Management Center',
    'September 2, 2026',
]:
    if marker not in index:
        raise SystemExit(f'Missing required blog marker: {marker}')

for stale in [
    'current connected GoreeCloud source inventory still spans 56 repositories',
    'Glaze UI 2.1 remains Candidate',
    'Glaze UI 2.0 is the current Stable production target',
    'Glaze UI 2.1 is the current Stable production target',
    'Glaze UI 2.1.0 is the current Stable GoreeCloud design-system baseline',
    'the five substantive platform systems',
    'The six substantive platform systems are',
    'Fold identity is the canonical Glaze UI mark',
    'Fold becomes the official visual identity',
]:
    if stale in index:
        raise SystemExit(f'Stale Blog content remains: {stale}')

for page_name, page in [('index',index),('404',error_page)]:
    for marker in ['name="goreecloud-glaze-ui" content="2.2.0"','data-glaze-ui="2.2.0"','glaze-canvas']:
        if marker not in page:
            raise SystemExit(f'{page_name} missing Glaze UI 2.2 marker: {marker}')
    for stale in ['data-glaze-ui="1.5.0"','data-glaze-ui="2.0.0"','data-glaze-ui="2.1.0"','glaze-ui-2.1.0.css']:
        if stale in page:
            raise SystemExit(f'{page_name} still activates a superseded Glaze UI bundle')

for marker in [
    'Glaze UI 2.2.0 Stable consumer integration',
    '6731098b28dd0393faa878c70d989a221d714a20',
    'Solid where users read. Glazed where users interact.',
    '--glaze-touch-min: 48px',
    '--glaze-touch-assisted: 56px',
    'data-glaze-density="compact"',
    'data-glaze-performance="reduced"',
    'data-glaze-large-text="true"',
    '--glaze-system-panel-budget: 1',
    'prefers-reduced-motion',
    'prefers-reduced-transparency',
    'prefers-contrast: more',
    'forced-colors: active',
]:
    if marker not in css:
        raise SystemExit(f'Missing Blog Glaze UI 2.2 web-layer marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden blog runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Blog CSP is not fail-closed enough')
print('GoreeCloud Blog current platform model, seven Integral Platform Systems, Facet identity, and Glaze UI 2.2 validation passed.')
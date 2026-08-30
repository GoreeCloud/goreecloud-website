from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'archive'
required = ['index.html','style.css','glaze-ui-2.0.0.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing archive site files: {missing}')

index = (SITE/'index.html').read_text(encoding='utf-8')
error_page = (SITE/'404.html').read_text(encoding='utf-8')
css = (SITE/'glaze-ui-2.0.0.css').read_text(encoding='utf-8')
headers = (SITE/'_headers').read_text(encoding='utf-8')

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
    'Glaze UI 2.0.0 becomes the current Stable baseline',
    'Glaze UI 2.1 remains Candidate',
    'GoreeCloud Code becomes the first-party source-control product',
    'Forgejo becomes the initial replaceable infrastructure foundation',
    'Public Center model · August 27, 2026',
    'Portfolio reconciliation · August 29, 2026',
    '56 repositories: 40 public and 16 private',
    'GoreeCloud Identity expands the substantive platform model to six systems',
    'Facet becomes the current official Glaze UI identity',
    'GoreeCloud File Manager',
    'GoreeCloud Maps',
    'GoreeCloud App Store',
    'Design Center',
    'Privacy Center',
    'Security Center',
    'Continuity Center',
    'Mesh Center',
    'Identity Center',
]:
    if marker not in index:
        raise SystemExit(f'Missing required archive marker: {marker}')

for page_name, page in [('index',index),('404',error_page)]:
    for marker in ['name="goreecloud-glaze-ui" content="2.0.0"','data-glaze-ui="2.0.0"','glaze-canvas']:
        if marker not in page:
            raise SystemExit(f'{page_name} missing Glaze UI 2.0 marker: {marker}')
    if 'data-glaze-ui="1.5.0"' in page:
        raise SystemExit(f'{page_name} still activates Glaze UI 1.5')

for marker in ['Glaze UI 2.0.0 Stable integration','ff3fff4306bd53ea9c0715a7c0d64265bb038617','prefers-reduced-motion','prefers-reduced-transparency','forced-colors']:
    if marker not in css:
        raise SystemExit(f'Missing Archive Glaze UI 2.0 web-layer marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden archive runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Archive CSP is not fail-closed enough')

print('GoreeCloud Archive historical sequence and current Glaze UI 2.0 portfolio validation passed.')

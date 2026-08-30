from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'sites' / 'blog'
required = ['index.html','style.css','site.js','glaze-ui-2.0.0.css','_headers','404.html','README.md']
missing = [name for name in required if not (SITE / name).is_file()]
if missing:
    raise SystemExit(f'Missing blog site files: {missing}')
index = (SITE/'index.html').read_text()
error_page = (SITE/'404.html').read_text()
css = (SITE/'glaze-ui-2.0.0.css').read_text()
headers = (SITE/'_headers').read_text()
for marker in [
    'GoreeCloud Blog',
    'Building an owned cloud, one layer at a time.',
    'GoreeCloud’s public platform map catches up with the software',
    '53 repositories: 39 public and 14 private',
    'GoreeCloud Code replaces the idea of a forge as the product boundary',
    'Forgejo is the initial replaceable infrastructure foundation',
    'Documents, Messenger, Gateway, and Quill broaden the native portfolio',
    'Glaze UI 2.0 is the current Stable production target',
    'Glaze UI 2.0.0 is now the current Stable GoreeCloud design-system baseline',
    'Historical direction: self-hosted Gitea as the planned permanent authority',
    'superseded August 27, 2026',
    'Design Center',
    'Privacy Center',
    'Security Center',
    'Continuity Center',
    'Mesh Center',
    'GoreeCloud is becoming a software ecosystem',
    'August 24, 2026',
    'August 29, 2026',
]:
    if marker not in index:
        raise SystemExit(f'Missing required blog marker: {marker}')
for page_name,page in [('index',index),('404',error_page)]:
    for marker in ['name="goreecloud-glaze-ui" content="2.0.0"','data-glaze-ui="2.0.0"','glaze-canvas']:
        if marker not in page: raise SystemExit(f'{page_name} missing Glaze UI 2.0 marker: {marker}')
    if 'data-glaze-ui="1.5.0"' in page: raise SystemExit(f'{page_name} still activates Glaze UI 1.5')
for marker in ['Glaze UI 2.0.0 Stable integration','ff3fff4306bd53ea9c0715a7c0d64265bb038617','prefers-reduced-motion','prefers-reduced-transparency','forced-colors']:
    if marker not in css: raise SystemExit(f'Missing Blog Glaze UI 2.0 web-layer marker: {marker}')
for forbidden in ['google-analytics','googletagmanager','fonts.googleapis.com','http://']:
    if forbidden in index.lower():
        raise SystemExit(f'Forbidden blog runtime dependency: {forbidden}')
if "default-src 'self'" not in headers or "connect-src 'none'" not in headers:
    raise SystemExit('Blog CSP is not fail-closed enough')
print('GoreeCloud Blog Glaze UI 2.0 site validation passed.')
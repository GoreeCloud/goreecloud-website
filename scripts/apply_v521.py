#!/usr/bin/env python3
"""Apply the one-time GoreeCloud Website v5.21 public-asset hardening migration."""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def platform_anchor(text: str, href: str, aria: str, mark: str, img_src: str, img_alt: str, width: str = "38", height: str = "38", extra_class: str = "") -> str:
    classes = "platform-logo-link" + (f" {extra_class}" if extra_class else "")
    old = (
        f'<a class="{classes}" href="{href}" target="_blank" rel="noopener noreferrer" aria-label="{aria}">\n'
        f'                <img src="{img_src}" alt="{img_alt}" width="{width}" height="{height}" loading="lazy" decoding="async">\n'
        f'              </a>'
    )
    new = (
        f'<a class="platform-logo-link platform-native-mark" href="{href}" target="_blank" rel="noopener noreferrer" aria-label="{aria}">{mark}</a>'
    )
    return replace_once(text, old, new, f"platform mark {mark}")


def main() -> None:
    index = read("index.html")
    index = platform_anchor(index, "https://www.proxmox.com", "Proxmox official website", "PX", "assets/platform/proxmox.svg", "Proxmox logo")
    index = platform_anchor(index, "https://www.debian.org/", "Debian official website", "DE", "assets/platform/debian.svg", "Debian logo")
    index = platform_anchor(index, "https://www.docker.com/", "Docker official website", "DK", "assets/platform/docker.svg", "Docker logo")
    index = platform_anchor(index, "https://netbird.io/", "NetBird official website", "NB", "assets/platform/netbird.svg", "NetBird logo", "42", "31", "netbird")
    index = platform_anchor(index, "https://adguard.com/adguard-home/overview.html", "AdGuard Home official website", "AG", "assets/platform/adguard-home.svg", "AdGuard Home logo")
    index = platform_anchor(index, "https://caddyserver.com/", "Caddy official website", "CA", "assets/platform/caddy.svg", "Caddy logo")
    index = platform_anchor(index, "https://github.com/henrygd/beszel", "Beszel official repository", "BZ", "assets/platform/beszel.svg", "Beszel logo")
    index = platform_anchor(index, "https://github.com/louislam/uptime-kuma", "Uptime Kuma official repository", "UK", "assets/platform/uptime-kuma.svg", "Uptime Kuma logo")
    index = replace_once(
        index,
        '<a class="platform-logo-link" href="https://github.com/GoreeCloud/goreecloud-monitor" target="_blank" rel="noopener noreferrer" aria-label="GoreeCloud Monitor public repository">\n                <span class="platform-native-mark" aria-hidden="true">GM</span>\n              </a>',
        '<a class="platform-logo-link platform-native-mark" href="https://github.com/GoreeCloud/goreecloud-monitor" target="_blank" rel="noopener noreferrer" aria-label="GoreeCloud Monitor public repository">GM</a>',
        "GoreeCloud Monitor mark",
    )
    index = replace_once(
        index,
        '<a class="platform-logo-link" href="https://github.com/GoreeCloud/goreecloud-search" target="_blank" rel="noopener noreferrer" aria-label="GoreeCloud Search public repository">\n                <span class="platform-native-mark" aria-hidden="true">GS</span>\n              </a>',
        '<a class="platform-logo-link platform-native-mark" href="https://github.com/GoreeCloud/goreecloud-search" target="_blank" rel="noopener noreferrer" aria-label="GoreeCloud Search public repository">GS</a>',
        "GoreeCloud Search mark",
    )
    index = replace_once(
        index,
        '<p class="platform-legal">Third-party logos identify their respective technologies and remain the property of their respective owners. This is a representative public foundation, not a complete infrastructure inventory.</p>',
        '<p class="platform-legal">Technology names identify their respective projects; outbound links lead to official project sites or repositories. GoreeCloud uses neutral Glaze UI letter marks instead of third-party logo artwork. This is a representative public foundation, not a complete infrastructure inventory.</p>',
        "platform legal note",
    )
    write("index.html", index)

    css = read("css/platform.css")
    css = replace_once(
        css,
        '\n.platform-logo-link img {\n  width: 38px;\n  height: 38px;\n  display: block;\n  object-fit: contain;\n}\n\n.platform-logo-link.netbird img {\n  width: 42px;\n  height: auto;\n}\n',
        '\n',
        "retired platform image CSS",
    )
    write("css/platform.css", css)

    build = read("scripts/build_public_site.py")
    old_assets = '''# Only artwork intentionally required by the current public experience.\n# Family-service cards use GoreeCloud Glaze UI monograms instead of deploying\n# third-party service-logo artwork. The remaining third-party graphics are the\n# explicitly reviewed platform marks shown in the platform-foundation section.\nPUBLIC_ASSET_FILES = (\n    "assets/favicon.svg",\n    "assets/goreecloud-icon.png",\n    "assets/social-preview.png",\n    "assets/platform/adguard-home.svg",\n    "assets/platform/beszel.svg",\n    "assets/platform/caddy.svg",\n    "assets/platform/debian.svg",\n    "assets/platform/docker.svg",\n    "assets/platform/netbird.svg",\n    "assets/platform/ntfy.svg",\n    "assets/platform/proxmox.svg",\n    "assets/platform/searxng.svg",\n    "assets/platform/uptime-kuma.svg",\n)'''
    new_assets = '''# Only GoreeCloud-owned identity/presentation artwork is deployable.\n# Third-party technologies are identified with neutral Glaze UI letter marks and\n# descriptive names/links rather than redistributing project logo artwork.\nPUBLIC_ASSET_FILES = (\n    "assets/favicon.svg",\n    "assets/goreecloud-icon.png",\n    "assets/social-preview.png",\n)'''
    build = replace_once(build, old_assets, new_assets, "public asset allowlist")
    write("scripts/build_public_site.py", build)

    inventory = '''# GoreeCloud Website Public Asset Inventory\n\n## Purpose\n\nThis repository document records the artwork that is intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-asset, and repository-publication review tracked in issue #5.\n\nThis inventory is **not a license grant**. The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`, and CI requires the deployable artwork boundary to remain GoreeCloud-owned and explicitly allowlisted.\n\n## Review status\n\nStatus: **Deployable artwork reduced to GoreeCloud-owned identity and presentation assets; third-party artwork removed from the public artifact**\n\nVersion 5.21.0 removes the remaining third-party platform logo files from the `dist/` allowlist and replaces the homepage platform-logo presentation with neutral Glaze UI letter marks. Technology names and outbound links remain for descriptive identification, but the browser no longer downloads or displays third-party project logo artwork from this repository.\n\nThis change removes the remaining deployable third-party-artwork provenance/trademark review from the website publication surface. It does **not** declare third-party names or marks to be GoreeCloud property, does not alter the Apache-2.0 source-license boundary, and does not by itself authorize publishing the private repository or its history.\n\n## GoreeCloud identity artwork\n\n| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |\n| --- | --- | --- | --- |\n| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `1e578573f8f753f0d51e616284546b42f67012da` |\n| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `5ae9000d1404239ef362f42f109e3d7de3557d38` |\n| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; editorial/brand rights remain separately controlled | `64aaf437835b31a8473292487cf57366bb58c4fa` |\n\n## Third-party artwork publication boundary\n\nNo path under `assets/platform/` or `assets/services/` is included in the current `PUBLIC_ASSET_FILES` allowlist. The homepage uses text/letter marks for platform technologies and family services instead of third-party logos.\n\nThird-party SVG files may remain in the private repository as historical or reference material while issue #5 remains open. Repository presence does not make those files deployable, approved for redistribution, or covered by the Apache-2.0 source grant. The isolated `dist/` build is the publication boundary.\n\n## Integrity and regression controls\n\n- `scripts/build_public_site.py` explicitly allowlists only the three GoreeCloud-owned public artwork files above.\n- `scripts/validate_public_assets.py` rejects any deployable `assets/platform/` or `assets/services/` path and rejects third-party artwork references from the homepage platform surface.\n- `tests/test_public_asset_boundary.py` protects the exact artwork allowlist and neutral-mark contract.\n- `scripts/validate_build_artifact.py` proves that only allowlisted files enter the isolated `dist/` artifact.\n- `scripts/verify_remote_deployment.py` compares deployed bytes against the exact reviewed source/artifact after merge.\n\n## Deliberate boundaries\n\n- Technology and project names remain descriptive references to their respective projects.\n- Official outbound project links remain links; they do not load third-party render resources into the GoreeCloud page.\n- The Apache-2.0 source license applies to the approved source-code boundary and does not automatically license GoreeCloud branding or third-party marks.\n- GoreeCloud identity artwork may use different reuse terms from source code.\n- Adding any new public artwork requires updating `PUBLIC_ASSET_FILES`, this inventory, and the creative-asset validator in the same reviewed change.\n- Repository-only historical/reference artwork remains outside the deployment artifact unless explicitly reviewed and allowlisted.\n\n## Publication gate\n\nIssue #5 remains open only for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. A successful CI run or this reduction of the public artwork surface does not authorize a repository visibility change.\n'''
    write("docs/public-asset-inventory.md", inventory)

    validator = '''#!/usr/bin/env python3\n"""Fail closed on GoreeCloud website public creative-asset boundaries."""\n\nfrom __future__ import annotations\n\nfrom html.parser import HTMLParser\nfrom pathlib import Path\nimport sys\n\nROOT = Path(__file__).resolve().parents[1]\nSCRIPTS = ROOT / "scripts"\nif str(SCRIPTS) not in sys.path:\n    sys.path.insert(0, str(SCRIPTS))\n\nfrom build_public_site import PUBLIC_ASSET_FILES  # noqa: E402\n\nEXPECTED_ASSETS = (\n    "assets/favicon.svg",\n    "assets/goreecloud-icon.png",\n    "assets/social-preview.png",\n)\nFORBIDDEN_PREFIXES = ("assets/platform/", "assets/services/")\nEXPECTED_PLATFORM_MARKS = {"PX", "DE", "DK", "NB", "AG", "CA", "GN", "BZ", "UK", "GM", "GS"}\n\n\nclass PlatformParser(HTMLParser):\n    def __init__(self) -> None:\n        super().__init__(convert_charrefs=True)\n        self.in_platform = False\n        self.platform_depth = 0\n        self.third_party_images: list[str] = []\n        self.marks: list[str] = []\n        self._capture_mark = False\n\n    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:\n        attrs = {key: value or "" for key, value in attrs_list}\n        if tag == "section" and attrs.get("id") == "platform":\n            self.in_platform = True\n            self.platform_depth = 1\n            return\n        if self.in_platform and tag == "section":\n            self.platform_depth += 1\n        if not self.in_platform:\n            return\n        if tag == "img":\n            src = attrs.get("src", "")\n            if src.startswith(FORBIDDEN_PREFIXES):\n                self.third_party_images.append(src)\n        classes = set(attrs.get("class", "").split())\n        if tag in {"a", "span"} and "platform-native-mark" in classes:\n            self._capture_mark = True\n\n    def handle_endtag(self, tag: str) -> None:\n        if self._capture_mark and tag in {"a", "span"}:\n            self._capture_mark = False\n        if self.in_platform and tag == "section":\n            self.platform_depth -= 1\n            if self.platform_depth <= 0:\n                self.in_platform = False\n\n    def handle_data(self, data: str) -> None:\n        if self.in_platform and self._capture_mark:\n            value = data.strip()\n            if value:\n                self.marks.append(value)\n\n\ndef main() -> int:\n    errors: list[str] = []\n    if tuple(PUBLIC_ASSET_FILES) != EXPECTED_ASSETS:\n        errors.append(f"PUBLIC_ASSET_FILES must remain exactly {EXPECTED_ASSETS!r}; found {tuple(PUBLIC_ASSET_FILES)!r}.")\n\n    for path in PUBLIC_ASSET_FILES:\n        if path.startswith(FORBIDDEN_PREFIXES):\n            errors.append(f"Third-party artwork must not be deployable: {path}")\n\n    index = (ROOT / "index.html").read_text(encoding="utf-8")\n    parser = PlatformParser()\n    parser.feed(index)\n    if parser.third_party_images:\n        errors.append(f"Platform section still references third-party artwork: {sorted(parser.third_party_images)!r}")\n    if set(parser.marks) != EXPECTED_PLATFORM_MARKS:\n        errors.append(f"Platform neutral marks drifted: expected {sorted(EXPECTED_PLATFORM_MARKS)!r}, found {sorted(set(parser.marks))!r}.")\n\n    inventory = (ROOT / "docs/public-asset-inventory.md").read_text(encoding="utf-8")\n    for marker in (\n        "third-party artwork removed from the public artifact",\n        "No path under `assets/platform/` or `assets/services/` is included",\n        "final human reachable-history/contextual-disclosure review",\n    ):\n        if marker not in inventory:\n            errors.append(f"Public asset inventory is missing required boundary text: {marker!r}")\n\n    if errors:\n        print("Public creative-asset validation failed:")\n        for error in errors:\n            print(f"  - {error}")\n        return 1\n    print("Public creative-asset validation passed: only GoreeCloud-owned artwork is deployable.")\n    return 0\n\n\nif __name__ == "__main__":\n    sys.exit(main())\n'''
    write("scripts/validate_public_assets.py", validator)

    tests = '''#!/usr/bin/env python3\n"""Regression tests for the GoreeCloud public creative-asset boundary."""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\nimport sys\nimport unittest\n\nROOT = Path(__file__).resolve().parents[1]\nSCRIPTS = ROOT / "scripts"\nif str(SCRIPTS) not in sys.path:\n    sys.path.insert(0, str(SCRIPTS))\n\nfrom build_public_site import PUBLIC_ASSET_FILES  # noqa: E402\n\n\nclass PublicAssetBoundaryTests(unittest.TestCase):\n    def test_only_goreecloud_owned_artwork_is_deployable(self) -> None:\n        self.assertEqual(\n            tuple(PUBLIC_ASSET_FILES),\n            ("assets/favicon.svg", "assets/goreecloud-icon.png", "assets/social-preview.png"),\n        )\n\n    def test_third_party_asset_directories_are_not_deployable(self) -> None:\n        self.assertFalse(any(path.startswith("assets/platform/") for path in PUBLIC_ASSET_FILES))\n        self.assertFalse(any(path.startswith("assets/services/") for path in PUBLIC_ASSET_FILES))\n\n    def test_homepage_does_not_reference_third_party_artwork(self) -> None:\n        index = (ROOT / "index.html").read_text(encoding="utf-8")\n        self.assertNotIn("assets/platform/", index)\n        self.assertNotIn("assets/services/", index)\n        self.assertIn("neutral Glaze UI letter marks instead of third-party logo artwork", index)\n\n\nif __name__ == "__main__":\n    unittest.main()\n'''
    write("tests/test_public_asset_boundary.py", tests)

    workflow = read(".github/workflows/validate.yml")
    workflow = replace_once(
        workflow,
        '      - name: Validate source license\n        run: python scripts/validate_license.py\n\n      - name: Validate GoreeCloud governance readiness',
        '      - name: Validate source license\n        run: python scripts/validate_license.py\n\n      - name: Validate public creative-asset boundary\n        run: python scripts/validate_public_assets.py\n\n      - name: Validate GoreeCloud governance readiness',
        "creative asset CI gate",
    )
    write(".github/workflows/validate.yml", workflow)

    readme = read("README.md")
    readme = replace_once(
        readme,
        'Current website package: **v5.20.0 — repository portfolio reconciliation, metadata hardening, and ancillary-page request optimization**',
        'Current website package: **v5.21.0 — third-party artwork elimination and platform identity hardening**',
        "README version",
    )
    readme = replace_once(readme, '- locally hosted images and project artwork;', '- locally hosted GoreeCloud identity and presentation artwork;', "README artwork role")
    readme = replace_once(
        readme,
        'The v5.20.0 release also links the already-deployed local web manifest and dual SVG/PNG favicon identity from every human-facing page, completes Open Graph/Twitter metadata for the public repository directory, and enforces page-specific stylesheet/script request ceilings. Privacy and security pages now load only the shared styles they actually use. These are static presentation and delivery improvements; they do not add browser telemetry, a service worker, a backend, or new network requests.',
        'The v5.21.0 release removes all third-party platform/service artwork from the deployable `dist/` allowlist. The platform foundation now uses neutral Glaze UI letter marks while retaining descriptive technology names and official outbound links. A dedicated validator and regression suite reject any future `assets/platform/` or `assets/services/` publication without an explicit reviewed boundary change. This reduces payload, browser asset requests, and creative-rights exposure without adding telemetry, remote resources, a service worker, or a backend.',
        "README release summary",
    )
    readme = replace_once(
        readme,
        'Issue #5 remains open for the remaining third-party platform-mark review, the final human repository-history/contextual review, and the explicit repository visibility/publication decision. Passing CI does not itself authorize a repository visibility change or a creative-rights decision.',
        'Issue #5 remains open for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. The v5.21.0 public artifact no longer contains third-party logo artwork, but passing CI still does not authorize a repository visibility change or a creative-rights/publication decision.',
        "README issue boundary",
    )
    readme = replace_once(
        readme,
        'The 5.20.0 candidate preserves the site\'s established visual identity and exact Glaze UI 1.1 contract, plus the 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections.',
        'The 5.21.0 candidate preserves the site\'s established visual identity and exact Glaze UI 1.1 contract, plus the 5.20.0 repository/metadata hardening, 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections.',
        "README Glaze release reference",
    )
    readme = replace_once(
        readme,
        '- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;\n',
        '- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;\n- `python scripts/validate_public_assets.py` — reject third-party artwork from the deployable allowlist and homepage platform surface;\n',
        "README tooling",
    )
    write("README.md", readme)

    baseline = read("docs/stability-baseline.md")
    baseline = replace_once(baseline, 'The repository-defined release version is **5.20.0**.', 'The repository-defined release version is **5.21.0**.', "baseline version")
    start = baseline.index("## 5.20.0 scope")
    end = baseline.index("## Glaze UI 1.1 stable-release boundary")
    scope = '''## 5.21.0 scope\n\nVersion 5.21.0 removes third-party artwork from the deployable website artifact and hardens the platform-identity boundary while preserving the production-verified v5.20 repository portfolio, metadata, Glaze UI 1.1, privacy, security, runtime-status, and isolated-publication contracts.\n\nThe release:\n\n- removes all ten `assets/platform/*.svg` paths from `PUBLIC_ASSET_FILES`, leaving only the GoreeCloud favicon, application icon, and social preview as deployable artwork;\n- replaces visible Proxmox, Debian, Docker, NetBird, AdGuard Home, Caddy, Beszel, and Uptime Kuma logos with neutral Glaze UI letter marks while preserving descriptive names and official outbound project links;\n- simplifies GoreeCloud Monitor and Search platform marks to the same single-frame Glaze UI mark pattern;\n- retains historical/reference third-party SVG files only in the private repository and outside `dist/`;\n- adds `scripts/validate_public_assets.py` and `tests/test_public_asset_boundary.py` so third-party artwork cannot silently re-enter the deployed allowlist or homepage platform surface;\n- adds the creative-asset validator to the exact-head CI workflow before governance/deployment acceptance;\n- updates `docs/public-asset-inventory.md` so the remaining issue #5 gate is the final human reachable-history/contextual-disclosure review and explicit repository publication decision, not deployable third-party logo provenance;\n- reduces public file count and artifact bytes without raising any HTML, CSS, JavaScript, image, request, or total-artifact ceiling;\n- preserves the authenticated **30 repository / 23 public / 7 private / 11 group** portfolio authority from v5.20.0;\n- preserves the exact Glaze UI 1.1.0 conformance pin at `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`;\n- preserves the Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma runtime-status boundaries;\n- preserves Wardveil Security reporting, `security@goreecloud.com`, the self-only browser-origin model, `connect-src 'none'`, and telemetry-free operation;\n- preserves the exact allowlisted Cloudflare `dist/` publication model and exact branch-preview/production deployment verification requirement.\n\n'''
    baseline = baseline[:start] + scope + baseline[end:]
    baseline = baseline.replace("The v5.20.0 portfolio and metadata release does not add authentication", "The v5.21.0 platform-identity release does not add authentication")
    baseline = replace_once(
        baseline,
        'The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.',
        'The open creative-rights and source-publication review remains authoritative for repository visibility decisions. The public artifact no longer deploys third-party logo artwork, but the final human reachable-history/contextual-disclosure review and explicit publication decision are not bypassed by a successful stable release.',
        "baseline publication boundary",
    )
    write("docs/stability-baseline.md", baseline)

    stability_tests = read("tests/test_stability_baseline.py")
    stability_tests = replace_once(stability_tests, '            "Third-party platform-mark review",', '            "final human reachable-history/contextual-disclosure review",', "stability test publication marker")
    write("tests/test_stability_baseline.py", stability_tests)

    write("VERSION", "5.21.0\n")

    print("Applied GoreeCloud Website v5.21.0 platform identity hardening migration.")


if __name__ == "__main__":
    main()

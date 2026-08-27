# GoreeCloud Website Icon Identity Audit

Date: 2026-08-27

The GoreeCloud Suite homepage must display the reviewed canonical application artwork recorded in `docs/suite-portfolio.json`.

Each Suite entry records its authoritative GoreeCloud repository, source artwork path, reviewed source ref, website icon path, and expected Git blob identity. `scripts/validate_suite_portfolio.py` verifies that the website copy matches the reviewed repository-owned artwork before publication.

The canonical product identity is intended to remain the same across supported web/PWA, desktop/Linux, Android, future iOS, GoreeCloud Manager, repository, release, documentation, notification, installer, update, and recovery surfaces. Platform-specific masking, padding, raster sizes, formats, adaptive layers, monochrome variants, or other required derivatives may differ while preserving the same underlying product identity.

Third-party infrastructure and roadmap technologies are different: their cards use the official or otherwise authorized identity of the external product when that third party is being represented. Those assets are referential and are not GoreeCloud application identities.

A product may still be in development before every client package consumes every required derivative. Full visual production acceptance requires supported release targets to reference or reproducibly derive the approved canonical identity.

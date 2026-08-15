# GoreeCloud Gallery Android Build Carrier

## Role and Purpose

This branch is an isolated build carrier for GoreeCloud Gallery Android APK development and acceptance testing. It is intentionally separated from the GoreeCloud public website `main` branch and does not define or modify the production website deployment.

GoreeCloud Gallery is an offline-first GoreeCloud-maintained fork based on Fossify Gallery. The application package is `com.goreecloud.gallery`.

## Exact Upstream Baseline

The build is reproducible from pinned source revisions:

- Fossify Gallery 1.13.1: `b28299dc33821eee8d108a9880ce87876cf31443`
- Fossify Commons 6.1.5: `acfd352df1a1852d17a5f77def8b7ad6e522a5b6`

The workflow checks out those exact commits in detached state before applying GoreeCloud changes.

## Patch Architecture

GoreeCloud changes are maintained as deterministic, fail-closed source transformations:

1. `build_goreecloud_gallery.py` — gc.1 foundation, package identity, GoreeCloud branding, Glaze palette, launcher identity, offline boundary, and license notice.
2. `build_goreecloud_gallery_gc2.py` — local Commons composite build, palette/system-theme correction, launcher aliases, and first fork-boundary fixes.
3. `build_goreecloud_gallery_gc3.py` — real-device identity corrections, Compose counterfeit-warning boundary, canonical launcher behavior, and Glaze app-bar surfaces.
4. `build_goreecloud_gallery_gc4.py` — rounded Glaze Settings cards and refined popup/dialog geometry.
5. `build_goreecloud_gallery_gc5.py` — legacy non-Compose counterfeit-warning removal, popup contrast correction, rounded folder/media thumbnail defaults, and stronger release-readiness validation.

Each patch script verifies the exact expected upstream source shape and terminates instead of silently applying an incomplete transformation when the baseline changes.

## Glaze UI Requirements

GoreeCloud Gallery uses Glaze UI as its shared visual and interaction language. The Android implementation emphasizes:

- rounded containers and media surfaces;
- layered light and dark surfaces;
- restrained elevation and border depth;
- readable, explicit popup/dialog contrast;
- polished controls and touch-friendly spacing;
- GoreeCloud-controlled launcher and product identity;
- system-aware light/dark behavior without depending on Material You color extraction;
- accessibility and legibility over decorative effects.

## Privacy and Network Boundary

GoreeCloud Gallery is intended to operate entirely against local Android media/storage APIs. The GoreeCloud patchset does not add analytics, advertising, cloud accounts, remote APIs, tracking, or `android.permission.INTERNET`.

The build workflow validates that the packaged application does not request the Internet permission.

Android's storage-management permissions are separate from network access and are retained only where required for local gallery file-management functionality.

## Build and Validation

The gc.5 workflow performs the following gates before publishing an artifact:

- exact upstream revision verification;
- deterministic patch validation;
- `git diff --check` for Gallery and Commons changes;
- source-level counterfeit-warning scan;
- rounded-thumbnail default assertions;
- popup contrast-selection assertion;
- Android unit tests;
- Android lint;
- FOSS debug APK compilation;
- application-ID verification when `apkanalyzer` is available;
- packaged permission verification for absence of `android.permission.INTERNET`;
- inspection of every packaged `classes*.dex` file for removed Fossify counterfeit-warning text;
- GoreeCloud notice verification;
- GNU GPL license preservation;
- SHA-256 generation;
- GitHub Actions artifact upload.

A successful build artifact is an acceptance candidate, not automatically a production release. Real-device acceptance remains required for visual behavior, storage permissions, installation/upgrade behavior, media operations, light/dark appearance, accessibility, and destructive file-operation safety.

## Release Model

Current APKs are development-signed acceptance builds intended for direct sideloading. A stable GoreeCloud Gallery release should use a controlled long-lived signing identity so upgrades can be installed predictably without uninstalling prior releases.

Before stable promotion, verify at minimum:

- no upstream counterfeit or promotional branding appears in normal use;
- GoreeCloud identity is consistent across launcher, installer, About, Settings, dialogs, and secondary surfaces;
- folder and media thumbnails default to rounded Glaze geometry;
- overflow menus are readable in System, Light, Dark, White, Black & White, and supported Custom themes;
- file browsing, viewing, editing, copy/move/delete, recycle bin, hidden/excluded items, favorites, video playback, and import/export settings behave correctly;
- Android storage permission flows are understandable and do not request network access;
- upgrade/rollback behavior is documented;
- licensing and source attribution remain available;
- real-device acceptance evidence is recorded.

## Repository Direction

This build carrier is deliberately isolated and suitable for current APK iteration. Before declaring GoreeCloud Gallery a long-term stable GoreeCloud-maintained application, its source/build history should be evaluated for migration into a dedicated GoreeCloud Gallery repository so application development is not permanently coupled to the public website repository.

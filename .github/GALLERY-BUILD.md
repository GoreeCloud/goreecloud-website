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
5. `build_goreecloud_gallery_gc5.py` — legacy non-Compose counterfeit-warning removal, popup contrast correction, rounded folder/media thumbnail defaults, API-qualified navigation-bar appearance resources, and stronger release-readiness validation.
6. `build_goreecloud_gallery_gc6.py` — removes square thumbnail controls and square rendering preferences from the GoreeCloud product surface, hard-enforces rounded folder/media thumbnails, and attempts the first MaterialToolbar action-overflow correction through application theme resources.
7. `build_goreecloud_gallery_gc7.py` — corrects the remaining real-device toolbar overflow defect at the actual owner path: Fossify Commons `MySearchMenu`. It assigns an explicit GoreeCloud light/dark popup theme to the embedded `MaterialToolbar` during construction and whenever search-bar colors refresh, with GoreeCloud-owned popup surfaces and text appearances.

Each patch script verifies the exact expected upstream source shape and terminates instead of silently applying an incomplete transformation when the baseline changes.

## Glaze UI Requirements

GoreeCloud Gallery uses Glaze UI as its shared visual and interaction language. The Android implementation emphasizes:

- rounded containers and media surfaces;
- rounded thumbnail presentation as a GoreeCloud product rule rather than an optional square/rounded mode;
- layered light and dark surfaces;
- restrained elevation and border depth;
- readable, explicit popup/dialog contrast;
- polished controls and touch-friendly spacing;
- GoreeCloud-controlled launcher and product identity;
- system-aware light/dark behavior without depending on Material You color extraction;
- accessibility and legibility over decorative effects.

Square thumbnail controls are intentionally not exposed in GoreeCloud Gallery. Media grid thumbnails, folder thumbnails, and imported or legacy thumbnail-style preferences must resolve to the rounded GoreeCloud presentation. Thumbnail spacing, folder-count presentation, folder-title limits, media duration/file-type badges, and favorite markers remain configurable where supported.

Toolbar overflow menus are also a Glaze-controlled surface. A light GoreeCloud screen must not display a dark inherited popup, and popup foreground/background colors must always remain mutually readable. The `MySearchMenu` toolbar therefore owns an explicit popup-theme contract rather than relying on the upstream Commons default.

## Privacy and Network Boundary

GoreeCloud Gallery is intended to operate entirely against local Android media/storage APIs. The GoreeCloud patchset does not add analytics, advertising, cloud accounts, remote APIs, tracking, or `android.permission.INTERNET`.

The build workflow validates that the packaged application does not request the Internet permission.

Android's storage-management permissions are separate from network access and are retained only where required for local gallery file-management functionality. Because full local file-management capability is security-sensitive, real-device acceptance must verify that the permission request is understandable, expected for the documented feature set, and not broader than the accepted product requirement.

## Build and Validation

The gc.7 workflow performs the following gates before publishing an artifact:

- exact upstream revision verification;
- deterministic gc.1 through gc.7 patch validation;
- `git diff --check` for Gallery and Commons changes;
- source-level counterfeit-warning scan;
- forced rounded-thumbnail configuration assertions;
- assertions that the crop-to-square Settings row, file rounded/square toggle, and folder square/rounded selector are absent;
- assertion that `MySearchMenu` selects GoreeCloud popup themes directly from the effective background luminance;
- assertion that the embedded `MaterialToolbar` has a construction-time GoreeCloud popup theme before menu inflation;
- explicit light/dark popup-widget, popup-text, list-view, foreground, and background resource assertions;
- Android unit-test task execution;
- Android lint;
- FOSS debug APK compilation;
- application-ID verification when `apkanalyzer` is available;
- packaged permission verification for absence of `android.permission.INTERNET`;
- inspection of every packaged `classes*.dex` file for removed Fossify counterfeit-warning text;
- GoreeCloud notice verification;
- GNU GPL license preservation;
- SHA-256 generation;
- GitHub Actions artifact upload.

The earlier gc.5 validation run identified and forced correction of an API-compatibility defect inherited from the first Glaze theme patch: `android:windowLightNavigationBar` is isolated to API-27-qualified resources while the application continues to support its API 26 minimum.

Real-device gc.6 acceptance then established two different outcomes. The no-square-thumbnail work behaved as intended on the visible Settings surface and rounded thumbnails rendered correctly. Standard dialogs such as column count, media filtering, and sorting were also readable. However, the three-dot overflow menu on both the main folder screen and an opened media folder remained a dark navy surface with very dark text.

Inspection of the pinned source identified the remaining boundary: the affected top bar is not a generic activity dialog or standalone popup. `activity_main.xml` hosts Fossify Commons `MySearchMenu`; `MySearchMenu` inflates `menu_search.xml`; and that layout creates its own `MaterialToolbar`. The upstream Commons base theme defaults its action-overflow menu to a dark style. Application-level gc.6 overrides were therefore insufficient to guarantee the popup context used by this embedded toolbar on the tested device.

gc.7 moves the correction to that actual owner path. The toolbar now receives a GoreeCloud `ThemeOverlay.AppCompat.Light` or `ThemeOverlay.AppCompat.Dark` popup context directly. The light theme owns a `#F7F8FC` rounded surface with `#14213D` primary text; the dark theme owns a `#171C29` rounded surface with `#F5F7FC` primary text. The selected popup theme is set while `MySearchMenu` is constructed and is refreshed whenever the top-bar colors update.

A successful build artifact is an acceptance candidate, not automatically a production release. Real-device acceptance remains required for visual behavior, storage permissions, installation/upgrade behavior, media operations, light/dark appearance, accessibility, and destructive file-operation safety.

## Known Readiness Debt

The following items remain deliberate pre-stable-release work rather than being hidden by a successful APK build:

- The upstream `testFossDebugUnitTest` task currently reports `NO-SOURCE`; the workflow executes the unit-test gate, but there are not yet GoreeCloud-specific automated application tests. Stable development should add targeted tests for fork-owned behavior where practical.
- Android lint passes against the upstream lint baseline and still reports non-blocking warnings, including deprecated Android/Gradle APIs and other inherited technical debt. GoreeCloud-specific new lint errors are not accepted, but upstream debt should be reviewed during future baseline synchronization rather than silently expanded.
- The upstream Android build currently emits deprecation warnings for Jetifier and Gradle behavior that will require attention before future Android Gradle Plugin/Gradle major-version upgrades.
- GitHub Actions runner deprecation notices for pinned workflow actions should be addressed during CI maintenance without weakening reproducibility.
- Current acceptance APKs rely on the Android debug-signing path. Stable GoreeCloud distribution requires a controlled, long-lived signing identity stored through approved secret handling rather than committed to source control.
- Real-device acceptance remains required for the gc.7 direct `MySearchMenu` overflow correction, the deeper file/folder thumbnail-option dialogs, forced rounded behavior with existing preferences, storage permission flow, and core file operations.

These limitations do not invalidate an acceptance APK, but they prevent treating a successful CI build alone as evidence of stable production readiness.

## Release Model

Current APKs are acceptance builds intended for direct sideloading. A stable GoreeCloud Gallery release should use a controlled long-lived signing identity so upgrades can be installed predictably without uninstalling prior releases.

Before stable promotion, verify at minimum:

- no upstream counterfeit or promotional branding appears in normal use;
- GoreeCloud identity is consistent across launcher, installer, About, Settings, dialogs, and secondary surfaces;
- square thumbnail controls are absent and folder/media thumbnails remain rounded even when legacy or imported preferences previously selected square behavior;
- toolbar overflow menus are readable on the main folders screen and inside media folders in both light and dark Glaze presentation;
- file browsing, viewing, editing, copy/move/delete, recycle bin, hidden/excluded items, favorites, video playback, and import/export settings behave correctly;
- Android storage permission flows are understandable and do not request network access;
- upgrade/rollback behavior is documented;
- licensing and source attribution remain available;
- real-device acceptance evidence is recorded.

## Repository Direction

This build carrier is deliberately isolated and suitable for current APK iteration. Before declaring GoreeCloud Gallery a long-term stable GoreeCloud-maintained application, its source/build history should be evaluated for migration into a dedicated GoreeCloud Gallery repository so application development is not permanently coupled to the public website repository.

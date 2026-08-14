/* GoreeCloud public website — early appearance and application identity initialization.
 *
 * This tiny self-hosted script runs before stylesheets so an explicit Light or Dark
 * preference can be applied before the first paint. System mode requires no stored value.
 * It also publishes the local web app manifest without introducing an inline-script CSP exception.
 */

(() => {
  const THEME_STORAGE_KEY = 'goreecloud-theme';
  const MANIFEST_HREF = '/site.webmanifest';
  const THEME_COLORS = {
    dark: '#07111f',
    light: '#f4f7fb',
  };
  const root = document.documentElement;

  function ensureManifestLink() {
    if (document.querySelector('link[rel~="manifest"]')) return;

    const manifest = document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = MANIFEST_HREF;
    document.head.append(manifest);
  }

  function updateThemeColors(mode) {
    document.querySelectorAll('meta[name="theme-color"][data-theme-color]').forEach((meta) => {
      const scheme = meta.dataset.themeColor;
      meta.content = mode === 'light' || mode === 'dark'
        ? THEME_COLORS[mode]
        : THEME_COLORS[scheme] ?? meta.content;
    });
  }

  ensureManifestLink();

  try {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    if (savedTheme === 'light' || savedTheme === 'dark') {
      root.dataset.theme = savedTheme;
      updateThemeColors(savedTheme);
    } else if (savedTheme) {
      localStorage.removeItem(THEME_STORAGE_KEY);
    }
  } catch {
    // Follow the operating-system appearance when browser storage is unavailable.
  }
})();

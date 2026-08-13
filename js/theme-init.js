/* GoreeCloud public website — early appearance initialization.
 *
 * This tiny self-hosted script runs before stylesheets so an explicit Light or Dark
 * preference can be applied before the first paint. System mode requires no stored value.
 */

(() => {
  const THEME_STORAGE_KEY = 'goreecloud-theme';
  const THEME_COLORS = {
    dark: '#07111f',
    light: '#f4f7fb',
  };
  const root = document.documentElement;

  function updateThemeColors(mode) {
    document.querySelectorAll('meta[name="theme-color"][data-theme-color]').forEach((meta) => {
      const scheme = meta.dataset.themeColor;
      meta.content = mode === 'light' || mode === 'dark'
        ? THEME_COLORS[mode]
        : THEME_COLORS[scheme] ?? meta.content;
    });
  }

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

/* GoreeCloud public website — appearance, navigation, and small progressive enhancements. */

const THEME_STORAGE_KEY = 'goreecloud-theme';
const THEME_MODES = ['system', 'light', 'dark'];
const THEME_COLORS = {
  dark: '#07111f',
  light: '#f4f7fb',
};
const root = document.documentElement;
const themeToggle = document.querySelector('.theme-toggle');
const themeIcon = document.querySelector('.theme-toggle-icon');
const themeLabel = document.querySelector('.theme-toggle-label');
const colorScheme = window.matchMedia('(prefers-color-scheme: light)');

root.dataset.js = 'true';
if (themeToggle) themeToggle.hidden = false;

function getThemeMode() {
  const explicitTheme = root.dataset.theme;
  return explicitTheme === 'light' || explicitTheme === 'dark' ? explicitTheme : 'system';
}

function updateThemeColors(mode) {
  document.querySelectorAll('meta[name="theme-color"][data-theme-color]').forEach((meta) => {
    const scheme = meta.dataset.themeColor;
    meta.content = mode === 'light' || mode === 'dark'
      ? THEME_COLORS[mode]
      : THEME_COLORS[scheme] ?? meta.content;
  });
}

function updateThemeControl() {
  if (!themeToggle || !themeIcon || !themeLabel) return;

  const currentMode = getThemeMode();
  const currentIndex = THEME_MODES.indexOf(currentMode);
  const nextMode = THEME_MODES[(currentIndex + 1) % THEME_MODES.length];
  const currentLabel = currentMode[0].toUpperCase() + currentMode.slice(1);
  const nextLabel = nextMode[0].toUpperCase() + nextMode.slice(1);
  const accessibleLabel = `Appearance: ${currentLabel}. Activate for ${nextLabel} mode.`;

  themeToggle.dataset.themeMode = currentMode;
  themeIcon.textContent = currentMode === 'system' ? '◐' : currentMode === 'light' ? '☀' : '☾';
  themeToggle.setAttribute('aria-label', accessibleLabel);
  themeToggle.setAttribute('title', accessibleLabel);
  themeLabel.textContent = accessibleLabel;
}

function setThemeMode(mode, { persist = true } = {}) {
  if (!THEME_MODES.includes(mode)) return;

  if (mode === 'system') {
    delete root.dataset.theme;
  } else {
    root.dataset.theme = mode;
  }

  updateThemeColors(mode);

  if (persist) {
    try {
      if (mode === 'system') {
        localStorage.removeItem(THEME_STORAGE_KEY);
      } else {
        localStorage.setItem(THEME_STORAGE_KEY, mode);
      }
    } catch {
      // The site remains fully usable when browser storage is unavailable.
    }
  }

  updateThemeControl();
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

updateThemeControl();

themeToggle?.addEventListener('click', () => {
  const currentIndex = THEME_MODES.indexOf(getThemeMode());
  const nextMode = THEME_MODES[(currentIndex + 1) % THEME_MODES.length];
  setThemeMode(nextMode);
});

colorScheme.addEventListener?.('change', () => {
  if (getThemeMode() === 'system') {
    updateThemeColors('system');
    updateThemeControl();
  }
});

const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const desktopNavigation = window.matchMedia('(min-width: 721px)');

function closeNavigation({ restoreFocus = false } = {}) {
  if (!navToggle || !nav) return;
  nav.classList.remove('open');
  navToggle.setAttribute('aria-expanded', 'false');
  if (restoreFocus) navToggle.focus();
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => closeNavigation());
  });

  document.addEventListener('click', (event) => {
    if (!nav.classList.contains('open')) return;
    if (nav.contains(event.target) || navToggle.contains(event.target)) return;
    closeNavigation();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeNavigation({ restoreFocus: true });
    }
  });

  desktopNavigation.addEventListener?.('change', (event) => {
    if (event.matches) closeNavigation();
  });
}

const sectionLinks = nav
  ? Array.from(nav.querySelectorAll('a[href^="#"]')).filter((link) => link.hash.length > 1)
  : [];
const sectionEntries = sectionLinks
  .map((link) => ({ link, section: document.getElementById(link.hash.slice(1)) }))
  .filter(({ section }) => section);
let navigationFrame = null;

function updateActiveNavigation() {
  navigationFrame = null;
  if (!sectionEntries.length) return;

  const headerHeight = document.querySelector('.site-header')?.offsetHeight ?? 0;
  const marker = window.scrollY + headerHeight + Math.min(window.innerHeight * 0.18, 140);
  let activeId = '';

  for (const { section } of sectionEntries) {
    if (section.offsetTop <= marker) activeId = section.id;
  }

  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
    activeId = sectionEntries.at(-1)?.section.id ?? activeId;
  }

  for (const { link, section } of sectionEntries) {
    if (section.id === activeId) {
      link.setAttribute('aria-current', 'location');
    } else {
      link.removeAttribute('aria-current');
    }
  }
}

function scheduleActiveNavigationUpdate() {
  if (navigationFrame !== null) return;
  navigationFrame = window.requestAnimationFrame(updateActiveNavigation);
}

if (sectionEntries.length) {
  updateActiveNavigation();
  window.addEventListener('scroll', scheduleActiveNavigationUpdate, { passive: true });
  window.addEventListener('resize', scheduleActiveNavigationUpdate);
}

const year = document.getElementById('year');
if (year) {
  year.textContent = new Date().getFullYear();
}

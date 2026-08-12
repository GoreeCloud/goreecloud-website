/* GoreeCloud public website — navigation, appearance, and small progressive enhancements. */

const THEME_STORAGE_KEY = 'goreecloud-theme';
const root = document.documentElement;
const themeToggle = document.querySelector('.theme-toggle');
const themeIcon = document.querySelector('.theme-toggle-icon');
const themeLabel = document.querySelector('.theme-toggle-label');
const colorScheme = window.matchMedia('(prefers-color-scheme: light)');

function getEffectiveTheme() {
  const explicitTheme = root.dataset.theme;
  if (explicitTheme === 'light' || explicitTheme === 'dark') {
    return explicitTheme;
  }
  return colorScheme.matches ? 'light' : 'dark';
}

function updateThemeControl() {
  if (!themeToggle || !themeIcon || !themeLabel) return;

  const currentTheme = getEffectiveTheme();
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  const nextThemeLabel = `Switch to ${nextTheme} theme`;

  themeIcon.textContent = currentTheme === 'dark' ? '☀' : '☾';
  themeToggle.setAttribute('aria-label', nextThemeLabel);
  themeToggle.setAttribute('title', nextThemeLabel);
  themeLabel.textContent = nextThemeLabel;
}

function setTheme(theme) {
  root.dataset.theme = theme;
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch {
    // The site remains fully usable when browser storage is unavailable.
  }
  updateThemeControl();
}

try {
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  if (savedTheme === 'light' || savedTheme === 'dark') {
    root.dataset.theme = savedTheme;
  }
} catch {
  // Follow the operating-system appearance when browser storage is unavailable.
}

updateThemeControl();

themeToggle?.addEventListener('click', () => {
  setTheme(getEffectiveTheme() === 'dark' ? 'light' : 'dark');
});

colorScheme.addEventListener?.('change', () => {
  if (!root.dataset.theme) updateThemeControl();
});

const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');

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
}

const year = document.getElementById('year');
if (year) {
  year.textContent = new Date().getFullYear();
}

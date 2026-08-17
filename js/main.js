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

if (!document.querySelector('link[href="css/repositories.css"]')) {
  const repositoryStyles = document.createElement('link');
  repositoryStyles.rel = 'stylesheet';
  repositoryStyles.href = 'css/repositories.css';
  document.head.append(repositoryStyles);
}

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
const navToggleLabel = navToggle?.querySelector('.sr-only');
const nav = document.querySelector('.site-nav');
const desktopNavigation = window.matchMedia('(min-width: 721px)');

if (nav && location.pathname.endsWith('/') || location.pathname.endsWith('/index.html')) {
  const projectLink = nav.querySelector('a[href="#development"]');
  if (projectLink && !nav.querySelector('a[href="repositories.html"]')) {
    const repositoryLink = document.createElement('a');
    repositoryLink.href = 'repositories.html';
    repositoryLink.textContent = 'Repositories';
    projectLink.insertAdjacentElement('afterend', repositoryLink);
  }
}

function updateNavigationControl(open) {
  if (!navToggle) return;
  navToggle.setAttribute('aria-expanded', String(open));
  if (navToggleLabel) navToggleLabel.textContent = open ? 'Close navigation' : 'Open navigation';
}

function closeNavigation({ restoreFocus = false } = {}) {
  if (!navToggle || !nav) return;
  nav.classList.remove('open');
  updateNavigationControl(false);
  if (restoreFocus) navToggle.focus();
}

if (navToggle && nav) {
  updateNavigationControl(nav.classList.contains('open'));

  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    updateNavigationControl(open);
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

const developmentSection = document.getElementById('development');
if (developmentSection && !document.getElementById('repositories')) {
  const repositorySection = document.createElement('section');
  repositorySection.id = 'repositories';
  repositorySection.className = 'section repository-teaser';
  repositorySection.innerHTML = `
    <div class="container repository-teaser-grid">
      <div class="repository-teaser-copy">
        <p class="eyebrow">GitHub repositories</p>
        <h2>Source code is part of the platform.</h2>
        <p>GoreeCloud currently maintains 20 repositories spanning Glaze UI, native applications, maintained forks, browser integrations, monitoring, search, feeds, media, security, and the public website. The dedicated directory explains each repository's purpose and role.</p>
        <div class="repository-teaser-actions">
          <a class="button primary" href="repositories.html">Explore all repositories</a>
          <a class="button secondary" href="https://github.com/GoreeCloud" target="_blank" rel="noopener noreferrer">Open GitHub profile</a>
        </div>
      </div>
      <div class="repository-teaser-stats" aria-label="Repository portfolio summary">
        <div><strong>20</strong><span>current repositories</span></div>
        <div><strong>16</strong><span>public repositories</span></div>
        <div><strong>4</strong><span>private repositories</span></div>
        <div><strong>9</strong><span>functional groups</span></div>
      </div>
    </div>`;
  developmentSection.insertAdjacentElement('afterend', repositorySection);
}

const year = document.getElementById('year');
if (year) {
  year.textContent = new Date().getFullYear();
}

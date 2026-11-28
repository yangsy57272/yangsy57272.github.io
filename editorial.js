const dialog = document.querySelector('.search-dialog');
const trigger = document.querySelector('[data-search]');
const input = document.querySelector('#site-search');
const results = [...document.querySelectorAll('.search-results a')];
const empty = document.querySelector('.search-empty');

function filterResults() {
  const words = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let count = 0;
  for (const link of results) {
    const haystack = `${link.textContent} ${link.dataset.keywords}`.toLocaleLowerCase();
    const matches = words.every(word => haystack.includes(word));
    link.parentElement.hidden = !matches;
    if (matches) count++;
  }
  empty.hidden = count > 0;
}

let previousFocus;
function openSearch() {
  previousFocus = document.activeElement;
  input.value = '';
  filterResults();
  dialog.showModal();
  input.focus();
}

if (typeof dialog.showModal === 'function') {
  trigger.hidden = false;
  trigger.addEventListener('click', openSearch);
  dialog.querySelector('[data-close-search]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    if (previousFocus instanceof HTMLElement) previousFocus.focus({preventScroll: true});
  });
  input.addEventListener('input', filterResults);
  dialog.addEventListener('keydown', event => {
    const visible = results.filter(link => !link.parentElement.hidden);
    const index = visible.indexOf(document.activeElement);
    if (event.target === input && event.key === 'Enter' && visible.length) {
      event.preventDefault();
      visible[0].click();
      return;
    }
    if (!visible.length || (event.target !== input && index === -1)) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      if (event.key === 'ArrowDown') visible[(index + 1) % visible.length].focus();
      else if (index === 0) input.focus();
      else visible[index < 0 ? visible.length - 1 : index - 1].focus();
    }
  });
  for (const link of results) link.addEventListener('click', () => dialog.close());
  document.addEventListener('keydown', event => {
    if (event.defaultPrevented || event.altKey || event.isComposing || event.repeat) return;
    const typing = event.target instanceof HTMLElement &&
      (event.target.isContentEditable || event.target.matches('input, textarea, select'));
    const shortcut = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k';
    if (shortcut || (event.key === '/' && !typing && !event.ctrlKey && !event.metaKey)) {
      event.preventDefault();
      if (dialog.open) dialog.close();
      else openSearch();
    }
  });
}

function routeHomeFragment() {
  const routes = {
    '#about': 'about.html',
    '#contact': 'about.html#contact',
    '#research': '#work',
    '#photo-teaser': 'studio.html',
    '#music': 'studio.html#music',
    '#playground': 'playground.html',
    '#hero': '#main',
  };
  const hash = window.location.hash;
  if (!hash || document.getElementById(hash.slice(1))) return;
  window.location.replace(Object.hasOwn(routes, hash) ? routes[hash] : 'archive.html' + hash);
}

if (document.querySelector('.hero')) {
  routeHomeFragment();
  window.addEventListener('hashchange', routeHomeFragment);
}

const players = [...document.querySelectorAll('.studio-section audio, .studio-section video')];
for (const player of players) {
  player.addEventListener('play', () => {
    for (const other of players) if (other !== player && !other.paused) other.pause();
  });
}

const frameControls = document.querySelector('.frame-controls');
if (frameControls) {
  const frames = [...document.querySelectorAll('[data-artwork]')];
  const views = [...frameControls.querySelectorAll('[data-art-view]')];
  frameControls.hidden = false;
  for (const view of views) {
    view.addEventListener('click', () => {
      for (const button of views) button.setAttribute('aria-pressed', String(view === button));
      for (const frame of frames) frame.hidden = frame.dataset.artwork !== view.dataset.artView;
    });
  }
}

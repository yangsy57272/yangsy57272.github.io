/* Small pointer responses: light, tactile, and respectful of reduced motion. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const precisePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduced || !precisePointer) return;

  const halo = document.createElement('span');
  halo.className = 'pointer-halo';
  halo.setAttribute('aria-hidden', 'true');
  document.body.append(halo);
  let frame = 0, pointerX = -400, pointerY = -400;
  document.addEventListener('pointermove', event => {
    pointerX = event.clientX; pointerY = event.clientY;
    document.body.classList.add('pointer-active');
    if (frame) return;
    frame = requestAnimationFrame(() => {
      halo.style.setProperty('--pointer-x', pointerX + 'px');
      halo.style.setProperty('--pointer-y', pointerY + 'px');
      frame = 0;
    });
  }, { passive: true });
  document.documentElement.addEventListener('mouseleave', () => document.body.classList.remove('pointer-active'));
  document.addEventListener('pointerdown', () => halo.classList.add('is-down'));
  document.addEventListener('pointerup', () => halo.classList.remove('is-down'));

  const surfaces = document.querySelectorAll([
    '.song-card', '.research-card', '.growth-foundation', '.growth-track-compact',
    '.activity-card', '.edu-card', '.curiosity-choice', '.photo-frame', '.hero-print'
  ].join(','));
  surfaces.forEach(surface => {
    surface.classList.add('reactive-surface');
    const sheen = document.createElement('span');
    sheen.className = 'reactive-sheen';
    sheen.setAttribute('aria-hidden', 'true');
    surface.prepend(sheen);
    surface.addEventListener('pointermove', event => {
      const box = surface.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width;
      const y = (event.clientY - box.top) / box.height;
      surface.style.setProperty('--surface-x', (x * 100) + '%');
      surface.style.setProperty('--surface-y', (y * 100) + '%');
      surface.style.setProperty('--tilt-x', ((.5 - y) * 2.2) + 'deg');
      surface.style.setProperty('--tilt-y', ((x - .5) * 2.2) + 'deg');
    }, { passive: true });
    surface.addEventListener('pointerleave', () => {
      surface.style.setProperty('--tilt-x', '0deg');
      surface.style.setProperty('--tilt-y', '0deg');
    });
  });

  document.querySelectorAll('a, button').forEach(control => {
    if (control.closest('nav') || control.classList.contains('lb-btn')) return;
    control.classList.add('magnetic');
    control.addEventListener('pointermove', event => {
      const box = control.getBoundingClientRect();
      control.style.setProperty('--pull-x', ((event.clientX - box.left - box.width / 2) * .055) + 'px');
      control.style.setProperty('--pull-y', ((event.clientY - box.top - box.height / 2) * .08) + 'px');
    }, { passive: true });
    control.addEventListener('pointerleave', () => {
      control.style.setProperty('--pull-x', '0px');
      control.style.setProperty('--pull-y', '0px');
    });
  });

  document.addEventListener('click', event => {
    if (!event.target.closest('.sticker-shortcuts a,.section-sticker,.record-sticker,.song-symbol')) return;
    const ring = document.createElement('span');
    ring.className = 'ink-ripple';
    ring.style.left = event.clientX + 'px';
    ring.style.top = event.clientY + 'px';
    document.body.append(ring);
    ring.addEventListener('animationend', () => ring.remove(), { once: true });
  });
})();

/* Pointer depth and quiet entrances; the page remains complete without JavaScript. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return;

  if ('IntersectionObserver' in window) {
    const subjects = document.querySelectorAll([
      '#about .section-title', '#curiosity .section-title', '#photo-teaser .teaser-copy',
      '#music .section-title', '#education .section-title', '#achievements .section-title',
      '#research .section-title', '#activities .section-title', '#skills .section-title',
      '#contact .section-title', '.album-intro .section-title'
    ].join(','));
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('atelier-visible');
        observer.unobserve(entry.target);
      }
    }, { threshold: .08, rootMargin: '0px 0px -5% 0px' });
    subjects.forEach(subject => {
      subject.classList.add('atelier-rise');
      observer.observe(subject);
    });
  }

  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const stages = document.querySelectorAll('#hero, #photo-teaser, #photo-hero');
  for (const stage of stages) {
    let frame = 0;
    let x = 0;
    let y = 0;
    const render = () => {
      frame = 0;
      stage.style.setProperty('--art-x', `${(x * 22).toFixed(1)}px`);
      stage.style.setProperty('--art-y', `${(y * 18).toFixed(1)}px`);
      stage.style.setProperty('--art-x-mid', `${(x * 12).toFixed(1)}px`);
      stage.style.setProperty('--art-y-mid', `${(y * 13).toFixed(1)}px`);
      stage.style.setProperty('--art-x-small', `${(x * 7).toFixed(1)}px`);
      stage.style.setProperty('--art-y-small', `${(y * 6).toFixed(1)}px`);
      stage.style.setProperty('--art-x-back', `${(x * -10).toFixed(1)}px`);
      stage.style.setProperty('--art-y-back', `${(y * -9).toFixed(1)}px`);
    };
    stage.addEventListener('pointermove', event => {
      const box = stage.getBoundingClientRect();
      x = Math.max(-1, Math.min(1, (event.clientX - box.left) / box.width * 2 - 1));
      y = Math.max(-1, Math.min(1, (event.clientY - box.top) / box.height * 2 - 1));
      if (!frame) frame = requestAnimationFrame(render);
    }, { passive: true });
    stage.addEventListener('pointerleave', () => {
      x = 0; y = 0;
      if (!frame) frame = requestAnimationFrame(render);
    });
  }
})();

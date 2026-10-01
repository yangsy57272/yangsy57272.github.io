(() => {
  const story = document.getElementById('chapters');
  if (!story) return;
  const stage = story.querySelector('.chapter-stage');
  const steps = [...story.querySelectorAll('.chapter-step')];
  const visuals = [...story.querySelectorAll('.chapter-visual')];
  const controls = [...story.querySelectorAll('[data-chapter-jump]')];
  const paths = [...story.querySelectorAll('.chapter-drawing path')];
  const count = story.querySelector('.chapter-count');
  const note = story.querySelector('.chapter-scroll-note');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const lengths = paths.map(path => {
    const length = path.getTotalLength();
    path.style.strokeDasharray = `${length} ${length}`;
    return length;
  });
  let scheduled = false;
  let active = -1;
  story.classList.add('is-enhanced');

  function update() {
    scheduled = false;
    const rect = story.getBoundingClientRect();
    const stepHeight = rect.height / steps.length;
    const position = Math.max(0, Math.min(steps.length - 1, -rect.top / stepHeight));
    const next = Math.min(steps.length - 1, Math.max(0, Math.round(position)));
    if (next !== active) {
      active = next;
      steps.forEach((step, i) => step.classList.toggle('is-active', i === active));
      controls.forEach((button, i) => {
        if (i === active) button.setAttribute('aria-current', 'step');
        else button.removeAttribute('aria-current');
      });
      count.textContent = `${String(active + 1).padStart(2, '0')} / ${String(steps.length).padStart(2, '0')}`;
      note.textContent = active === steps.length - 1 ? 'Keep exploring ↓' : 'Scroll to follow the story ↓';
      [active, Math.min(active + 1, visuals.length - 1)].forEach(i => {
        visuals[i].querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
      });
    }
    visuals.forEach((visual, i) => {
      const opacity = reduced ? (i === active ? 1 : 0) : Math.max(0, 1 - Math.abs(position - i));
      visual.style.opacity = opacity.toFixed(3);
      visual.style.setProperty('--scene-scale', (1.035 + Math.max(0, 1 - Math.abs(position - i)) * -.027).toFixed(3));
    });
    const progress = position / Math.max(1, steps.length - 1);
    stage.style.setProperty('--chapter-progress', `${(progress * 100).toFixed(1)}%`);
    stage.style.setProperty('--light-opacity', (0.8 - progress * 0.42).toFixed(2));
    stage.style.setProperty('--light-scale', (1 + Math.sin(progress * Math.PI) * .25).toFixed(2));
    paths.forEach((path, i) => {
      path.style.strokeDashoffset = String(lengths[i] * (0.72 - progress * 0.66));
    });
  }
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  }
  addEventListener('scroll', schedule, { passive:true });
  addEventListener('resize', schedule, { passive:true });
  controls.forEach((button, index) => button.addEventListener('click', () => {
    const target = steps[index];
    scrollTo({ top:scrollY + target.getBoundingClientRect().top, behavior:reduced ? 'auto' : 'smooth' });
  }));
  if (!reduced && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    stage.addEventListener('pointermove', event => {
      const box = stage.getBoundingClientRect();
      const x = (event.clientX / box.width - .5) * 16;
      const y = ((event.clientY - box.top) / box.height - .5) * 16;
      stage.style.setProperty('--scene-x', `${x.toFixed(1)}px`);
      stage.style.setProperty('--scene-y', `${y.toFixed(1)}px`);
    }, { passive:true });
    stage.addEventListener('pointerleave', () => {
      stage.style.setProperty('--scene-x', '0px');
      stage.style.setProperty('--scene-y', '0px');
    });
  }
  update();
})();

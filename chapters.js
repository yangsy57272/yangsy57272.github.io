(() => {
  const story = document.getElementById('chapters');
  if (!story) return;

  const stage = story.querySelector('.chapter-stage');
  const steps = [...story.querySelectorAll('.chapter-step')];
  const visuals = [...story.querySelectorAll('.chapter-visual')];
  const controls = [...story.querySelectorAll('[data-chapter-jump]')];
  const count = story.querySelector('.chapter-count');
  const scrollNote = story.querySelector('.chapter-scroll-note');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let active = -1;
  let scheduled = false;

  story.classList.add('is-enhanced');

  function activate(index) {
    if (index === active) return;
    active = index;
    steps.forEach((step, i) => step.classList.toggle('is-active', i === index));
    visuals.forEach((visual, i) => visual.classList.toggle('is-active', i === index));
    controls.forEach((control, i) => {
      if (i === index) control.setAttribute('aria-current', 'step');
      else control.removeAttribute('aria-current');
    });
    count.textContent = `${String(index + 1).padStart(2, '0')} / ${String(steps.length).padStart(2, '0')}`;
    scrollNote.textContent = index === steps.length - 1 ? 'Keep exploring ↓' : 'Scroll to turn the page ↓';
  }

  function update() {
    scheduled = false;
    const viewportMidpoint = innerHeight * 0.53;
    let nearest = 0;
    let nearestDistance = Infinity;
    steps.forEach((step, index) => {
      const box = step.getBoundingClientRect();
      const distance = Math.abs((box.top + box.bottom) / 2 - viewportMidpoint);
      if (distance < nearestDistance) { nearestDistance = distance; nearest = index; }
    });
    activate(nearest);
    const rect = story.getBoundingClientRect();
    const scrollable = Math.max(1, rect.height - innerHeight);
    const progress = Math.min(1, Math.max(0, -rect.top / scrollable));
    stage.style.setProperty('--chapter-progress', `${Math.round(progress * 100)}%`);
  }

  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  }

  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule, { passive: true });
  controls.forEach((control, index) => control.addEventListener('click', () => {
    steps[index].scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    activate(index);
  }));

  if (!reducedMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    stage.addEventListener('pointermove', event => {
      const box = stage.getBoundingClientRect();
      stage.style.setProperty('--chapter-pointer-x', `${((event.clientX - box.left) / box.width * 100).toFixed(1)}%`);
      stage.style.setProperty('--chapter-pointer-y', `${((event.clientY - box.top) / box.height * 100).toFixed(1)}%`);
      stage.style.setProperty('--chapter-drift-x', `${((event.clientX - box.left) / box.width - .5) * -12}px`);
      stage.style.setProperty('--chapter-drift-y', `${((event.clientY - box.top) / box.height - .5) * -12}px`);
    }, { passive: true });
    stage.addEventListener('pointerleave', () => {
      stage.style.setProperty('--chapter-drift-x', '0px');
      stage.style.setProperty('--chapter-drift-y', '0px');
    });
  }

  update();
})();

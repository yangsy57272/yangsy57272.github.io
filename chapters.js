(() => {
  const story = document.getElementById('chapters');
  if (!story) return;

  const stage = story.querySelector('.chapter-stage');
  const steps = [...story.querySelectorAll('.chapter-step')];
  const visuals = [...story.querySelectorAll('.chapter-visual')];
  const controls = [...story.querySelectorAll('[data-chapter-jump]')];
  const count = story.querySelector('.chapter-count');
  const scrollNote = story.querySelector('.chapter-scroll-note');
  const revealButton = story.querySelector('.chapter-reveal-button');
  const revealLabel = story.querySelector('.chapter-reveal-label');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let active = -1;
  let scheduled = false;
  let transitionTimer;
  const touchLensFocus = [['34%', '33%'], ['67%', '39%'], ['58%', '35%']];

  function positionTouchLens(index) {
    const [x, y] = touchLensFocus[index];
    stage.style.setProperty('--chapter-pointer-x', x);
    stage.style.setProperty('--chapter-pointer-y', y);
  }

  story.classList.add('is-enhanced');

  function activate(index) {
    if (index === active) return;
    [index, index + 1].forEach(i => {
      const photo = visuals[i]?.querySelector('img');
      if (photo) photo.loading = 'eager';
    });
    clearTimeout(transitionTimer);
    visuals.forEach(visual => visual.classList.remove('is-leaving'));
    if (active >= 0) visuals[active].classList.add('is-leaving');
    active = index;
    steps.forEach((step, i) => step.classList.toggle('is-active', i === index));
    visuals.forEach((visual, i) => visual.classList.toggle('is-active', i === index));
    controls.forEach((control, i) => {
      if (i === index) control.setAttribute('aria-current', 'step');
      else control.removeAttribute('aria-current');
    });
    count.textContent = `${String(index + 1).padStart(2, '0')} / ${String(steps.length).padStart(2, '0')}`;
    scrollNote.textContent = index === steps.length - 1 ? 'Keep exploring ↓' : 'Scroll to turn the page ↓';
    if (revealButton.getAttribute('aria-pressed') === 'true' && innerWidth <= 760) positionTouchLens(index);
    transitionTimer = setTimeout(() => visuals.forEach(visual => visual.classList.remove('is-leaving')), reducedMotion ? 0 : 950);
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
    const activeBox = steps[nearest].getBoundingClientRect();
    const chapterProgress = Math.min(1, Math.max(0, (viewportMidpoint - activeBox.top) / activeBox.height));
    stage.style.setProperty('--chapter-pan-y', `${((chapterProgress - .5) * -32).toFixed(1)}px`);
  }

  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  }

  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule, { passive: true });
  controls.forEach((control, index) => control.addEventListener('click', () => {
    scrollTo({ top: scrollY + steps[index].getBoundingClientRect().top, behavior: reducedMotion ? 'auto' : 'smooth' });
    activate(index);
  }));

  revealButton.addEventListener('click', () => {
    const revealed = !stage.classList.contains('is-peeking');
    stage.classList.toggle('is-peeking', revealed);
    positionTouchLens(Math.max(0, active));
    revealButton.setAttribute('aria-pressed', String(revealed));
    revealLabel.textContent = revealed ? 'Hide the lens' : 'Reveal the photo';
  });

  if (!reducedMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    stage.addEventListener('pointermove', event => {
      if (innerWidth <= 760) return;
      if (event.target.closest('.chapter-controls')) {
        stage.classList.remove('is-peeking');
        return;
      }
      const box = stage.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width;
      stage.classList.toggle('is-peeking', x >= .48);
      stage.style.setProperty('--chapter-pointer-x', `${(Math.max(.61, Math.min(.84, x)) * 100).toFixed(1)}%`);
      stage.style.setProperty('--chapter-pointer-y', `${((event.clientY - box.top) / box.height * 100).toFixed(1)}%`);
      stage.style.setProperty('--chapter-drift-x', `${(x - .5) * -12}px`);
      stage.style.setProperty('--chapter-drift-y', `${((event.clientY - box.top) / box.height - .5) * -12}px`);
    }, { passive: true });
    stage.addEventListener('pointerleave', () => {
      stage.classList.remove('is-peeking');
      stage.style.setProperty('--chapter-drift-x', '0px');
      stage.style.setProperty('--chapter-drift-y', '0px');
    });
  }

  update();
})();

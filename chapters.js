(() => {
  const video = document.getElementById('story-film');
  if (!video) return;
  const start = document.querySelector('.film-start');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let loaded = false;
  let visible = false;
  let manuallyPaused = false;
  let automaticPause = false;
  function load() {
    if (loaded) return;
    loaded = true;
    const source = video.querySelector('source');
    source.src = source.dataset.src;
    video.load();
  }
  function play() {
    load();
    video.play().catch(() => { start.hidden = false; });
  }
  start.addEventListener('click', () => { manuallyPaused = false; play(); });
  video.addEventListener('play', () => { start.hidden = true; manuallyPaused = false; });
  video.addEventListener('pause', () => {
    if (!automaticPause && visible && !document.hidden) manuallyPaused = true;
    automaticPause = false;
  });
  function suspend() {
    if (!video.paused) { automaticPause = true; video.pause(); }
  }
  const observer = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    if (visible && !reduced.matches && !manuallyPaused && !document.hidden) play();
    else if (!visible) suspend();
  }, { threshold:.3 });
  observer.observe(video);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) suspend();
    else if (visible && !reduced.matches && !manuallyPaused) play();
  });
  reduced.addEventListener('change', () => { if (reduced.matches) suspend(); });
  video.addEventListener('error', () => { start.hidden = true; });

  const dialog = document.getElementById('life-lightbox');
  let opener;
  document.querySelectorAll('[data-life-photo]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button;
      const img = dialog.querySelector('img');
      img.src = `assets/life/${button.dataset.lifePhoto}.webp`;
      img.alt = button.querySelector('img').alt;
      dialog.querySelector('figcaption').textContent = button.dataset.caption;
      dialog.showModal();
    });
  });
  dialog.querySelector('.life-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { if (opener) opener.focus(); });
})();

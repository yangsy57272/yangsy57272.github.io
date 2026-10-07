(() => {
  const video = document.getElementById('story-film');
  if (!video) return;
  const start = document.querySelector('.film-start');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const films = {
    activities: {src:'assets/films/a-world-of-connections-real-activities.mp4',poster:'assets/activities/thematic-story-01.jpg',description:'My projects, workshops, writing, teamwork and service — in 2 minutes 24 seconds.',label:'A world of connections: sixteen activities with real photos, labeled illustrations and golden animation'},
    art: {src:'assets/films/the-spark-art-film.mp4',poster:'assets/films/the-spark-art-poster.jpg',description:'An imagined world, inspired by my robotics photographs.',label:'The robot and me: an illustrated film of a spark, a blueprint, rotating connections, and a shared workshop'},
  };
  document.querySelectorAll('[data-film]').forEach(button => {
    button.addEventListener('click', () => {
      const film = films[button.dataset.film];
      suspend();
      video.poster = film.poster;
      video.setAttribute('aria-label', film.label);
      video.querySelector('source').dataset.src = film.src;
      document.getElementById('film-description').textContent = film.description;
      document.getElementById('film-download').href = film.src;
      document.querySelectorAll('[data-film]').forEach(b => b.setAttribute('aria-pressed',String(b === button)));
      loaded = false; manuallyPaused = false; start.hidden = false;
      play();
    });
  });
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

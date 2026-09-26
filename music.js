/* One audio stream per page, shared by the song cards and photo viewer. */
(() => {
  const tracks = [
    { id: 'rap', title: 'Song 01 · Rap', file: 'song-01-rap.mp3' },
    { id: 'time-machine', title: 'Time Machine · Country', file: 'time-machine.mp3' },
    { id: 'folk', title: 'Song 03 · 中文民谣', file: 'song-03-folk.mp3' }
  ];
  const roots = [...document.querySelectorAll('[data-music-player]')];
  if (!roots.length) return;
  const audio = document.createElement('audio');
  audio.preload = 'none';
  audio.volume = 0.35;
  audio.id = 'wendy-audio';
  document.body.append(audio);
  let current = document.body.classList.contains('gallery-with-music') ? 1 : 0;
  let state = 'Ready when you are';
  let request = 0;
  roots.forEach((root, i) => {
    root.innerHTML = `<div class="music-player-label"><span aria-hidden="true">♫</span> <span>Wendy’s songbook</span></div>
      <button class="music-toggle" type="button" aria-label="Play music">Play music</button>
      <label class="track-picker"><span class="music-sr">Choose a song</span><select aria-label="Choose a song">${tracks.map((t,j)=>`<option value="${j}">${t.title}</option>`).join('')}</select></label>
      <button class="music-next" type="button" aria-label="Next song">↠</button>
      <label class="music-volume">Volume <input type="range" min="0" max="100" step="1" value="35" aria-label="Music volume"></label>
      <div class="music-timeline"><span class="music-time">0:00</span><input type="range" min="0" max="100" value="0" step="0.1" aria-label="Song position" disabled><span class="music-duration">—</span></div>
      <p class="music-status" role="status">Ready when you are</p>`;
    root.querySelector('.music-toggle').addEventListener('click', toggle);
    root.querySelector('select').addEventListener('change', e => choose(Number(e.target.value), !audio.paused));
    root.querySelector('.music-next').addEventListener('click', () => choose((current + 1) % tracks.length, !audio.paused));
    root.querySelector('.music-volume input').addEventListener('input', e => { audio.volume = Number(e.target.value) / 100; sync(); });
    root.querySelector('.music-timeline input').addEventListener('input', e => {
      if (Number.isFinite(audio.duration)) audio.currentTime = Number(e.target.value) / 100 * audio.duration;
    });
  });
  function clock(seconds) { return Number.isFinite(seconds) ? Math.floor(seconds / 60) + ':' + String(Math.floor(seconds % 60)).padStart(2, '0') : '—'; }
  function sync() {
    const playing = !audio.paused;
    roots.forEach(root => {
      const toggle = root.querySelector('.music-toggle');
      toggle.textContent = playing ? 'Pause music' : 'Play music';
      toggle.setAttribute('aria-label', playing ? 'Pause music' : 'Play music');
      root.classList.toggle('is-playing', playing);
      root.querySelector('select').value = String(current);
      root.querySelector('.music-volume input').value = String(Math.round(audio.volume * 100));
      const status = root.querySelector('.music-status');
      if (status.textContent !== state) status.textContent = state;
    });
    document.querySelectorAll('[data-play-track]').forEach(btn => {
      const active = btn.dataset.playTrack === tracks[current].id && playing;
      btn.textContent = active ? 'Pause song Ⅱ' : 'Play song ▷';
      btn.setAttribute('aria-label', (active ? 'Pause ' : 'Play ') + tracks.find(t=>t.id===btn.dataset.playTrack).title);
      btn.closest('.song-card').classList.toggle('is-playing', active);
    });
  }
  function progress() {
    roots.forEach(root => {
      root.querySelector('.music-time').textContent = clock(audio.currentTime);
      root.querySelector('.music-duration').textContent = clock(audio.duration);
      const slider = root.querySelector('.music-timeline input');
      slider.disabled = !Number.isFinite(audio.duration) || audio.duration <= 0;
      slider.value = slider.disabled ? '0' : String(audio.currentTime / audio.duration * 100);
      slider.setAttribute('aria-valuetext', clock(audio.currentTime) + ' of ' + clock(audio.duration));
    });
  }
  async function play() {
    const token = ++request;
    if (!audio.getAttribute('src')) audio.src = 'assets/music/' + tracks[current].file;
    state = 'Loading your soundtrack…'; sync();
    try { await audio.play(); }
    catch (error) {
      if (token !== request || error.name === 'AbortError') return;
      state = error.name === 'NotAllowedError' ? 'Press Play music to start listening.' : 'Unable to play this track. Press Play to retry, or choose another song.';
      sync();
    }
  }
  function toggle() {
    if (audio.paused) { if (audio.error) audio.load(); play(); }
    else { ++request; audio.pause(); }
  }
  function choose(index, resume) {
    ++request;
    audio.pause(); current = index;
    audio.src = 'assets/music/' + tracks[current].file;
    state = 'Ready when you are'; progress(); sync();
    if (resume) play();
  }
  document.querySelectorAll('[data-play-track]').forEach(btn => btn.addEventListener('click', () => {
    const index = tracks.findIndex(t => t.id === btn.dataset.playTrack);
    if (index === current) toggle(); else choose(index, true);
  }));
  audio.addEventListener('playing', () => { state = 'Now playing · ' + tracks[current].title; sync(); });
  audio.addEventListener('pause', () => { state = 'Paused · ' + tracks[current].title; sync(); });
  audio.addEventListener('waiting', () => { state = 'Loading your soundtrack…'; sync(); });
  audio.addEventListener('error', () => { state = 'This track could not load. Press Play to retry, or choose another song.'; sync(); });
  audio.addEventListener('ended', () => choose((current + 1) % tracks.length, true));
  audio.addEventListener('timeupdate', progress);
  audio.addEventListener('loadedmetadata', progress);
  sync();
})();

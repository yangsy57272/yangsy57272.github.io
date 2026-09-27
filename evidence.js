(() => {
  const viewer = document.getElementById('evidence-viewer');
  if (!viewer) return;

  const image = viewer.querySelector('figure img');
  const caption = viewer.querySelector('figcaption');
  const closeButton = viewer.querySelector('.evidence-close');
  const previousButton = viewer.querySelector('.evidence-prev');
  const nextButton = viewer.querySelector('.evidence-next');
  let items = [];
  let activeIndex = 0;
  let returnFocus = null;

  function collectItems(button) {
    const rail = button.closest('[data-evidence-group]');
    return rail ? [...rail.querySelectorAll('.evidence-shot')] : [button];
  }

  function show(index) {
    if (!items.length) return;
    activeIndex = (index + items.length) % items.length;
    const item = items[activeIndex];
    image.src = item.dataset.full;
    image.alt = item.querySelector('img')?.alt || '';
    caption.textContent = item.dataset.caption || '';

    [items[(activeIndex + 1) % items.length], items[(activeIndex - 1 + items.length) % items.length]]
      .forEach(neighbor => {
        if (!neighbor) return;
        const preload = new Image();
        preload.src = neighbor.dataset.full;
      });
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('.evidence-shot');
    if (!button) return;
    items = collectItems(button);
    activeIndex = items.indexOf(button);
    returnFocus = button;
    show(activeIndex);
    viewer.showModal();
  });

  function closeViewer() {
    viewer.close();
  }

  viewer.addEventListener('close', () => {
    image.removeAttribute('src');
    returnFocus?.focus({ preventScroll: true });
  });

  closeButton.addEventListener('click', closeViewer);
  previousButton.addEventListener('click', () => show(activeIndex - 1));
  nextButton.addEventListener('click', () => show(activeIndex + 1));
  viewer.addEventListener('click', event => {
    const box = viewer.getBoundingClientRect();
    const inside = event.clientX >= box.left && event.clientX <= box.right && event.clientY >= box.top && event.clientY <= box.bottom;
    if (!inside) closeViewer();
  });
  viewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(activeIndex - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(activeIndex + 1); }
  });
})();

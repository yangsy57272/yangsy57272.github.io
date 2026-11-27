const ROWS = 3;
const COLS = 5;
const GOAL = 6;
const SVG = 'http://www.w3.org/2000/svg';

function collinear(a, b, c) {
  return (b.col - a.col) * (c.row - a.row) === (c.col - a.col) * (b.row - a.row);
}

function conflictingLines(points) {
  const lines = [];
  for (let a = 0; a < points.length - 2; a++) {
    for (let b = a + 1; b < points.length - 1; b++) {
      for (let c = b + 1; c < points.length; c++) {
        if (collinear(points[a], points[b], points[c])) lines.push([points[a], points[b], points[c]]);
      }
    }
  }
  return lines;
}

const board = document.querySelector('.board');
const status = document.querySelector('.board-status');
const controls = document.querySelector('.puzzle-controls');
const undo = controls.querySelector('[data-undo]');
const reset = controls.querySelector('[data-reset]');
const selected = new Set();
const history = [];
const points = Array.from({length: ROWS * COLS}, (_, index) => ({
  index, row: Math.floor(index / COLS), col: index % COLS,
}));
const cells = points.map(point => {
  const cell = document.createElement('button');
  cell.type = 'button';
  cell.tabIndex = point.index === 0 ? 0 : -1;
  cell.setAttribute('aria-label', `Row ${point.row + 1}, column ${point.col + 1}`);
  cell.addEventListener('click', () => {
    moveFocus(point.index);
    history.push([...selected]);
    if (selected.has(point.index)) selected.delete(point.index);
    else selected.add(point.index);
    render();
  });
  return cell;
});
const overlay = document.createElementNS(SVG, 'svg');
overlay.setAttribute('viewBox', `0 0 ${COLS} ${ROWS}`);
overlay.setAttribute('preserveAspectRatio', 'none');
overlay.setAttribute('aria-hidden', 'true');
board.append(...cells, overlay);

let focusIndex = 0;
function moveFocus(index) {
  cells[focusIndex].tabIndex = -1;
  focusIndex = index;
  cells[index].tabIndex = 0;
  cells[index].focus({preventScroll: true});
}

function render() {
  const lines = conflictingLines(points.filter(point => selected.has(point.index)));
  const conflicted = new Set(lines.flatMap(line => line.map(point => point.index)));
  overlay.replaceChildren(...lines.map(([from, , to]) => {
    const line = document.createElementNS(SVG, 'line');
    line.setAttribute('x1', from.col + .5);
    line.setAttribute('y1', from.row + .5);
    line.setAttribute('x2', to.col + .5);
    line.setAttribute('y2', to.row + .5);
    return line;
  }));
  points.forEach(({index, row, col}) => {
    cells[index].setAttribute('aria-pressed', String(selected.has(index)));
    cells[index].setAttribute('aria-label', `Row ${row + 1}, column ${col + 1}${conflicted.has(index) ? ', on a conflicting line' : ''}`);
    cells[index].classList.toggle('conflicted', conflicted.has(index));
  });
  if (lines.length) {
    const coordinates = lines[0].map(point => `row ${point.row + 1} column ${point.col + 1}`);
    status.textContent = `${selected.size} placed. Conflict: ${coordinates.join(', ')} line up.`;
  } else if (selected.size === GOAL) {
    status.textContent = 'Solved! Six points, with no three on a line.';
  } else {
    status.textContent = `${selected.size} of ${GOAL} points placed.`;
  }
  undo.disabled = !history.length;
  reset.disabled = !selected.size;
  if ((document.activeElement === undo && undo.disabled) || (document.activeElement === reset && reset.disabled)) {
    if (!undo.disabled) undo.focus();
    else moveFocus(focusIndex);
  }
}

board.addEventListener('keydown', event => {
  const {row, col} = points[focusIndex];
  const directions = {
    ArrowLeft: [0, -1], ArrowRight: [0, 1], ArrowUp: [-1, 0], ArrowDown: [1, 0],
  };
  if (!Object.hasOwn(directions, event.key)) return;
  event.preventDefault();
  const [dy, dx] = directions[event.key];
  const nextRow = row + dy;
  const nextCol = col + dx;
  if (nextRow >= 0 && nextRow < ROWS && nextCol >= 0 && nextCol < COLS) {
    moveFocus(nextRow * COLS + nextCol);
  }
});

undo.addEventListener('click', () => {
  const previous = history.pop();
  selected.clear();
  previous.forEach(index => selected.add(index));
  render();
});
reset.addEventListener('click', () => {
  history.push([...selected]);
  selected.clear();
  render();
});

document.querySelector('.board-help').hidden = false;
controls.hidden = false;
render();

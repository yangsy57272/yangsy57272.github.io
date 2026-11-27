# Shiyi Yang · Personal website

A portfolio and notebook for mathematics, physical prototypes, writing, photography, songwriting, and small interactive experiments.

## Preview

Clone the repository and run these commands from its root.

```bash
python3 -m http.server 8000
```

Open [the local homepage](http://localhost:8000/). The checked-in HTML is ready to serve directly. GitHub Pages serves the root of the `main` branch.

## Editing the site

- Edit `site_src/projects.py` for selected project summaries, case studies, and resource links. Each project entry drives its homepage card and case-study page.
- Edit `site_src/build.py` for the homepage, About, Notes, Studio, Playground, Now, navigation, search entries, and page metadata. Run `python3 site_src/build.py` after changes and include the updated HTML and sitemap in the same commit. The generator uses Python 3.9+ and the standard library.
- Edit `editorial.css` for typography, color, components, and breakpoints. `editorial.js` handles quick search, old homepage links, and keeping Studio playback to one active item. `puzzle.js` provides the no-three-in-a-line board.
- Edit `archive.html` for the original notebook, supporting project evidence, awards, sticker stories, and the debate, math, and camera experiments. Bookmarks to those sections on the former homepage still resolve.
- Edit `photography.html` and `activity-film.html` directly for the full gallery and activity journal. Gallery images use thumbnails with separate full-size files, and media files in Studio load on demand.

Use `/` or `Ctrl/⌘ K` for search. The archive’s search also indexes awards and their filters. On the puzzle board, use arrow keys to move, Enter or Space to toggle a point, and Tab to reach Undo and Clear board.

## Credits

Instrument Serif and Space Grotesk are bundled under the SIL Open Font License. The license files are in `assets/fonts/`. The Citrus Circuits logo in the sticker story is the official team mark from [Citrus Circuits](https://www.citruscircuits.org/).

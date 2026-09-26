# Shiyi Yang (Wendy) — Personal Website

Personal portfolio of **Shiyi Yang (Wendy)** — national debate champion, AIME qualifier,
2× FRC regional champion, and HIMCM global finalist (Top 4%). IB Class of 2027,
Shanghai Pinghe Bilingual School.

**Live site:** https://yangsy57272.github.io/

## Highlights

- Interactive constellation animation in the hero (responds to your mouse; click to add stars)
- "Follow a question" interactive story paths connecting debate, engineering, and photography
- Quick-search command palette — press `/` or `Ctrl/⌘ K` to jump to any section, award or PDF
- "Year by year" dot timeline of every award, linked to the filters and cards
- Playground: debate-motion generator with prep timer, AIME-style math sprint,
  and an exposure-triangle camera simulator from my photography workshop
- Photography gallery with reserved image space, immediate photo display, slideshow, swipe, filmstrip,
  shareable photo links (`photography.html#photo-DSC05866`) and a sticky album bar
- Typewriter headline cycling through key achievements
- Animated count-up statistics and staggered scroll-reveal throughout
- Filterable awards gallery (29 awards across 6 categories)
- Full HiMCM Finalist certificate and 26-page competition paper included as PDFs
- Zero dependencies — one HTML file, works anywhere

## Structure

```
index.html                        the main site (HTML + CSS + JS, no build step)
photography.html                  photography gallery (4 collections, 72 photos)
assets/photos/                    gallery images
assets/photography-workshop.pdf   workshop deck
assets/HiMCM-2025-Certificate.pdf HiMCM Finalist certificate
assets/HiMCM-2025-Paper.pdf       HiMCM 2025 competition paper
deploy.sh                         one-command deploy to GitHub Pages
```

## Deploy to GitHub Pages

```bash
brew install gh        # if not already installed
gh auth login          # log in to your GitHub account (one time)
./deploy.sh            # creates the repo, pushes, enables Pages
```

The script deploys to `<username>.github.io` (your root site) by default.
To use a different repo name: `./deploy.sh my-website` → the site appears at
`https://<username>.github.io/my-website/`.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Personal notebook design

The homepage uses `personal.css` for its warm paper, sage and rust palette, illustrated sticker shortcuts, personal stories, and compact academic records. Photography uses `gallery.css`, journal/contact-sheet layouts, collection covers, and a keyboard-accessible lightbox. The gallery retains all 72 original photos.

### Asset credit

`assets/stickers/citrus-circuits.png` is the official Citrus Circuits team mark from [citruscircuits.org](https://www.citruscircuits.org/), used to identify the FRC 1678 pit-sticker memory. It is presented on a paper sticker; it is not a scan of Wendy’s physical sticker. The team mark remains in its original colors. Other small illustrations are original SVG artwork.

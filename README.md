# Shiyi Yang (Wendy) — Personal Website

Personal portfolio of **Shiyi Yang (Wendy)** — national debate champion, AIME qualifier,
2× FRC regional champion, and HIMCM global finalist (Top 4%). IB Class of 2027,
Shanghai Pinghe Bilingual School.

**Live site:** https://\_\_GITHUB\_USERNAME\_\_.github.io/

## Highlights

- Interactive constellation animation in the hero (responds to your mouse)
- Typewriter headline cycling through key achievements
- Animated count-up statistics and staggered scroll-reveal throughout
- Filterable awards gallery (29 awards across 6 categories)
- Full HiMCM Finalist certificate and 26-page competition paper included as PDFs
- Zero dependencies — one HTML file, works anywhere

## Structure

```
index.html                        the entire site (HTML + CSS + JS, no build step)
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

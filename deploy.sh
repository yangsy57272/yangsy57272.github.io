#!/usr/bin/env bash
# One-command deploy to GitHub Pages.
# Usage: ./deploy.sh [repo-name]   (default: <your-username>.github.io)
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI not found. Install it first:  brew install gh"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "You are not logged in to GitHub yet — a browser window will open."
  gh auth login --web --git-protocol https
fi

GH_USER=$(gh api user -q .login)
REPO="${1:-$GH_USER.github.io}"

# Fill in the GitHub username placeholders in the site
if grep -q "__GITHUB_USERNAME__" index.html README.md 2>/dev/null; then
  sed -i '' "s/__GITHUB_USERNAME__/$GH_USER/g" index.html README.md
  git add -A
  git commit -m "Point GitHub links at $GH_USER"
fi

git branch -M main

if gh repo view "$GH_USER/$REPO" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$GH_USER/$REPO.git"
  git push -u origin main
else
  gh repo create "$REPO" --public --source=. --remote=origin --push \
    --description "Personal website of Shiyi Yang (Wendy)"
fi

# Enable GitHub Pages (main branch, root folder); ignore error if already enabled
gh api -X POST "repos/$GH_USER/$REPO/pages" \
  -f 'source[branch]=main' -f 'source[path]=/' >/dev/null 2>&1 || true

if [ "$REPO" = "$GH_USER.github.io" ]; then
  URL="https://$GH_USER.github.io/"
else
  URL="https://$GH_USER.github.io/$REPO/"
fi

echo ""
echo "  Deployed! Your site will be live in about a minute at:"
echo "  $URL"
echo ""
echo "  Share that link with anyone."

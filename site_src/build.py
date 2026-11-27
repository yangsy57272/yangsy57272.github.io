"""Build the editorial pages in place for GitHub Pages. Python 3, no dependencies."""

from html import escape
from pathlib import Path
from textwrap import dedent
from xml.etree.ElementTree import Element, SubElement, indent, tostring

from projects import PROJECTS

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://yangsy57272.github.io/'
NAME = 'Shiyi Yang'
BUILT_ROUTES = []
NAV = [('Work', 'index.html#work'), ('Notes', 'notes.html'), ('Studio', 'studio.html'),
       ('Playground', 'playground.html'), ('About', 'about.html')]
PAGES = [
    ('Selected work', 'index.html#work', 'ScentSense HiMCM Greenvolt portfolio projects'),
    ('Notes & writing', 'notes.html', 'Barbie John Locke essay argument'),
    ('Photography, music & films', 'studio.html', 'studio photo song video sound'),
    ('HiMCM 2024 paper (PDF)', 'assets/HiMCM-2024-Paper.pdf', 'computing environmental model'),
    ('HiMCM 2025 paper (PDF)', 'assets/HiMCM-2025-Paper.pdf', 'building evacuation simulation'),
    ('No-three-in-a-line paper (PDF)', 'assets/No-Three-In-Line.pdf', 'combinatorics geometry'),
    ('Photography gallery', 'photography.html', 'Istanbul Shanghai gallery lightbox'),
    ('About Wendy', 'about.html', 'biography laptop stickers red flower contact email'),
    ('Now', 'now.html', 'current working questions'),
    ('Playground', 'playground.html', 'puzzles math games'),
    ('No-three-in-a-line puzzle', 'playground.html#no-three-puzzle', 'geometry dots puzzle'),
    ('Debate prep, math sprint & exposure lab', 'archive.html#playground', 'camera stopwatch games'),
    ('Films & activity journal', 'archive.html#chapters', 'connections art film documentary'),
    ('Original notebook & awards', 'archive.html#achievements', 'archive growth honors activities awards'),
    ('The little things', 'archive.html#curiosity', 'stickers citrus circuits flower plums café'),
    ('Contact', 'about.html#contact', 'email GitHub'),
]
PAGES += [(p['title'], p['slug'] + '.html', p['category'] + ' ' + p['premise']) for p in PROJECTS]


def link_list(links):
    return '<ul class="text-links">' + ''.join(
        f'<li><a href="{href}">{escape(label)}</a></li>' for label, href in links
    ) + '</ul>'


def page(filename, title, description, body, *, active='', image='assets/life/behind-the-camera.webp', css=''):
    url = SITE + ('' if filename == 'index.html' else filename)
    BUILT_ROUTES.append(url)
    page_title = f'{title} | {NAME}'
    current = ' aria-current="page"'
    nav = ''.join(f'<a href="{href}"{current if label == active else ""}>{label}</a>'
                  for label, href in NAV)
    commands = ''.join(f'<li><a href="{href}" data-keywords="{escape(keywords, quote=True)}">{escape(label)}</a></li>'
                       for label, href, keywords in PAGES)
    html = f'''<!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{escape(page_title)}</title>
      <meta name="description" content="{escape(description, quote=True)}">
      <meta name="theme-color" content="#eeeee7">
      <link rel="canonical" href="{url}">
      <meta property="og:type" content="website">
      <meta property="og:site_name" content="{NAME}">
      <meta property="og:title" content="{escape(page_title, quote=True)}">
      <meta property="og:description" content="{escape(description, quote=True)}">
      <meta property="og:url" content="{url}">
      <meta property="og:image" content="{SITE}{image}">
      <meta name="twitter:card" content="summary_large_image">
      <link rel="icon" href="assets/editorial-mark.svg" type="image/svg+xml">
      <link rel="preload" href="assets/fonts/instrument-serif.woff2" as="font" type="font/woff2" crossorigin>
      <link rel="stylesheet" href="editorial.css">
      <script src="editorial.js" defer></script>
      {css}
    </head>
    <body>
      <a class="skip" href="#main">Skip to content</a>
      <header class="site-head">
        <div class="wrap mast">
          <a class="wordmark" href="index.html">{NAME}<span>.</span></a>
          <nav aria-label="Main navigation">{nav}</nav>
          <button class="search-button" type="button" data-search hidden><span>Search</span> <kbd>/</kbd></button>
        </div>
      </header>
      <main id="main" tabindex="-1">{body}</main>
      <footer class="site-foot">
        <div class="wrap foot-layout">
          <a class="wordmark" href="index.html">{NAME}<span>.</span></a>
          <nav aria-label="Elsewhere">
            <a href="now.html">Now</a><a href="archive.html">Archive</a>
            <a href="about.html#contact">Contact</a><a href="https://github.com/yangsy57272">GitHub</a>
          </nav>
        </div>
      </footer>
      <dialog class="search-dialog" aria-labelledby="search-title">
        <div class="search-head"><h2 id="search-title">Search the site</h2><button type="button" data-close-search>Close</button></div>
        <label class="sr-only" for="site-search">Filter pages and projects</label>
        <input id="site-search" type="search" placeholder="Find a project, note, or experiment…" autocomplete="off" autofocus>
        <p class="search-empty" role="status" hidden>No matching pages.</p>
        <ul class="search-results">{commands}</ul>
        <p class="search-help">Use the arrow keys to browse, Enter to open, or Esc to close.</p>
      </dialog>
    </body>
    </html>
    '''
    (ROOT / filename).write_text(dedent(html), encoding='utf-8')


def intro(label, title, body):
    return f'''<header class="wrap page-intro"><p class="eyebrow">{label}</p>
      <h1>{title}</h1><p class="lede">{body}</p></header>'''


def project_card(p):
    visual = (f'<div class="work-art {p["style"]}"><img src="{p["image"]}" alt="" loading="lazy" decoding="async"></div>')
    if p['style'] == 'grid-study':
        visual = '''<div class="work-art grid-study" aria-hidden="true">
          <span class="plot-axis">y</span><span class="plot-axis plot-axis-x">x</span><span class="plot-line"></span>
          <i style="--x:1;--y:1"></i><i style="--x:3;--y:1"></i><i style="--x:2;--y:2"></i>
          <i style="--x:4;--y:2"></i><i style="--x:4;--y:3"></i><i style="--x:5;--y:3"></i></div>'''
    return f'''<article class="work-card"><a href="{p['slug']}.html">
      {visual}
      <div class="work-copy"><p class="eyebrow">{p['category']}</p>
      <h3>{escape(p['title'])}</h3><p>{escape(p['premise'])}</p>
      <span class="read-case" aria-hidden="true">Read case study</span></div></a></article>'''


def home():
    work = ''.join(project_card(p) for p in PROJECTS)
    return f'''
    <section class="wrap hero">
      <div class="hero-copy">
        <p class="eyebrow"><span class="eyebrow-mark" aria-hidden="true"></span> Shiyi Yang / Wendy</p>
        <h1>Proofs, prototypes<br class="hero-break"> <em>&amp; passing moments.</em></h1>
        <p class="lede">I’m a student in Shanghai. I work through questions in mathematics, build physical prototypes, and keep a camera close by.</p>
        <div class="hero-links"><a class="action" href="#work">Explore my work</a><a class="plain-link" href="about.html">A little about me</a></div>
      </div>
      <figure class="hero-frame">
        <div class="hero-image"><img src="assets/life/behind-the-camera.webp" alt="Wendy photographing the action from the stands" width="1182" height="666" fetchpriority="high">
          <span class="viewfinder" aria-hidden="true"></span>
        </div>
        <figcaption><span>Behind the camera</span><a href="studio.html">Visit the studio</a></figcaption>
      </figure>
    </section>
    <section class="wrap work" id="work" aria-labelledby="work-heading">
      <div class="section-head"><h2 id="work-heading">Selected work</h2><a href="archive.html#research">Full project archive</a></div>
      <div class="work-grid">{work}</div>
    </section>
    <section class="wrap field-section" aria-labelledby="field-heading">
      <div class="field-copy"><p class="eyebrow">The notebook</p><h2 id="field-heading">Pages I keep open.</h2>
        <p>A laptop with more than thirty stickers. Half-formed arguments. Photos from between robotics matches.</p></div>
      <div class="field-links">
        <a href="notes.html"><strong>Notes &amp; writing</strong><span>Arguments that took a few drafts.</span></a>
        <a href="studio.html"><strong>The studio</strong><span>Photographs, songwriting and two films.</span></a>
        <a href="playground.html"><strong>Playground</strong><span>Try a proof with your hands.</span></a>
        <a href="now.html"><strong>Now</strong><span>Questions I’ve left open.</span></a>
      </div>
    </section>'''


def case_study(p):
    sections = ''.join(f'<section><h2>{escape(title)}</h2><p>{escape(copy)}</p></section>'
                       for title, copy in p['sections'])
    return intro(p['category'], escape(p['title']), escape(p['premise'])) + f'''
      <article class="wrap case-layout">
        <figure class="case-figure {p['style']}"><img src="{p['image']}" alt="{escape(p['alt'], quote=True)}" fetchpriority="high">
        <figcaption>{escape(p['evidence'])}</figcaption></figure>
        <div class="case-text">{sections}
          <section class="resources"><h2>Project material</h2>{link_list(p['links'])}</section>
          <a class="plain-link" href="index.html#work">All selected work</a>
        </div>
      </article>'''


def about():
    return intro('About', 'Hi, I’m <em>Wendy.</em>', 'I’m Shiyi Yang, a student in Shanghai. I build things, write songs, debate, and carry a camera.') + '''
    <div class="wrap story-layout">
      <figure class="case-figure"><img src="assets/life/match-day.webp" alt="Wendy cheering with friends at a robotics competition" width="724" height="1086">
        <figcaption>In the stands at a robotics competition</figcaption></figure>
      <div class="prose">
        <section><h2>Leaving the screen open</h2>
          <p>I used to sit at the back of the classroom so nobody could read an idea before I was ready to share it. A conversation with my dad about a poem by Du Fu helped. He heard my reading and offered his own. I could take his seriously and still keep mine.</p>
          <blockquote>“Being heard does not mean being overwritten.”</blockquote>
        </section>
        <section id="stickers"><h2>The laptop stickers</h2>
          <p>There are more than thirty stickers on my laptop. Some are peeling. I keep them anyway: a small red flower, a Citrus Circuits sticker, a reminder to leave the gap in a proof showing.</p>
          <p>The red flower came from a student who asked the same grammar question three times. I used to count the lessons I had finished. She remembered whether she could ask again.</p>
          <a class="plain-link" href="archive.html#curiosity">Open the sticker stories</a>
        </section>
        <section id="contact"><h2>Leave a little note.</h2>
          <p>A photograph, a half-formed idea, or something you’re making — I’d love to hear about it.</p>
          <div class="inline-links"><a href="mailto:yangsy.2009@outlook.com">Email me</a><a href="https://github.com/yangsy57272">GitHub</a></div>
        </section>
      </div>
    </div>'''


def notes():
    return intro('Notes &amp; writing', 'Thinking on <em>paper.</em>', 'A place for essays, arguments I kept revising, and the stories behind the work.') + '''
    <div class="wrap reading-list">
      <article><p class="eyebrow">Film criticism / Extended essay</p><h2>Barbie, irony &amp; the things we’re sold</h2>
        <p>How can a film question consumer culture while making its own brand more appealing? I followed that tension through Barbie Land, Gloria’s monologue and Ken’s Kendom.</p>
        <a href="assets/Barbie-Extended-Essay.pdf">Read the essay (PDF)</a><a href="archive.html#barbie">Browse the page previews</a></article>
      <article><p class="eyebrow">Ethics / Essay reflection</p><h2>Should we be polite to ChatGPT?</h2>
        <p>For the 2026 John Locke Essay Prize, I looked at why people say “please” to AI. I revised the argument around a separate question: whether we owe it politeness.</p>
        <a href="archive.html#writing">Read the reflection</a></article>
      <article><p class="eyebrow">Activity journal</p><h2>Learning to edit someone else’s words</h2>
        <p>At PHocus, I went from contributing articles to editing and running workshops. I used to start with the edit I wanted to make. Now I start by asking what the writer was trying to say.</p>
        <a href="activity-film.html#phocus">Read the PHocus story</a></article>
    </div>'''


def studio():
    return intro('Photography / Music / Film', 'The <em>studio.</em>', 'Istanbul between robotics matches, songs about distance, and the people who show up on both sides of the camera.') + '''
    <section class="wrap studio-section"><div class="section-head"><h2>Photography</h2><a href="photography.html">Open the full gallery</a></div>
      <div class="contact-sheet">
        <a href="photography.html#photo-DSC05866"><img src="assets/thumbs/city/DSC05866.webp" alt="Hagia Sophia" loading="lazy"><span>Hagia Sophia</span></a>
        <a href="photography.html#photo-DSC07053"><img src="assets/thumbs/city/DSC07053.webp" alt="Galata Tower seen from the water" loading="lazy"><span>Galata Tower</span></a>
        <a href="photography.html#photo-DSC08102"><img src="assets/thumbs/gongqing/DSC08102.webp" alt="A meadow of poppies" loading="lazy"><span>Poppy Afternoon</span></a>
      </div>
    </section>
    <section class="wrap studio-section" id="music"><div class="section-head"><h2>Songwriting</h2><a href="archive.html#music">Open the songbook</a></div>
      <div class="studio-songs">
        <article><p class="eyebrow">Rap / Identity</p><h3>Song 01</h3><p>Hearing your own voice through everyone else’s expectations.</p><audio controls preload="none" aria-label="Song 01" src="assets/music/song-01-rap.mp3"></audio></article>
        <article><p class="eyebrow">Country / Distance</p><h3>Time Machine</h3><p>Trying to build a time machine out of memories, with a friend across an ocean.</p><audio controls preload="none" aria-label="Time Machine" src="assets/music/time-machine.mp3"></audio></article>
        <article><p class="eyebrow">Folk / Family</p><h3>Song 03</h3><p>Old photographs, a lake outside the family home, and things left unsaid.</p><audio controls preload="none" aria-label="Song 03" src="assets/music/song-03-folk.mp3"></audio></article>
      </div>
    </section>
    <section class="wrap studio-section" id="films"><div class="section-head"><h2>Films</h2><a href="activity-film.html">Read the activity journal</a></div>
      <div class="studio-films">
        <figure><video controls muted playsinline preload="none" poster="assets/activities/thematic-story-01.jpg" src="assets/films/a-world-of-connections-real-activities.mp4" aria-label="A world of connections"></video><figcaption>A world of connections · 2:24 · Silent film</figcaption></figure>
        <figure><video controls muted playsinline preload="none" poster="assets/films/the-spark-art-poster.jpg" src="assets/films/the-spark-art-film.mp4" aria-label="The Spark art film"></video><figcaption>The Spark · 0:28 · Silent art film</figcaption><details><summary>Read the visual description</summary><p>An inventor and a competition robot reach toward a golden gyroscope. The workshop fades into glowing blueprint lines. The last scene gathers the team around a workbench lit by the same small spark.</p></details></figure>
      </div>
    </section>'''


def playground():
    return intro('Playground', 'Try the <em>question.</em>', 'A proof you can play, a debate clock, a math sprint, and the manual controls of a camera.') + '''
    <section class="wrap puzzle" id="no-three-puzzle" aria-labelledby="puzzle-title">
      <div class="puzzle-copy"><p class="eyebrow">Combinatorial geometry</p><h2 id="puzzle-title">No three in a line</h2>
        <p>Place six points on the grid without letting any straight line pass through three. Select a point again to remove it.</p>
        <details><summary>Show a hint</summary><p>Each row can hold at most two points. For a diagonal through all three rows, check whether the middle column is halfway between the other two.</p></details>
        <a href="no-three-in-a-line.html">Read the case study</a>
      </div>
      <div class="puzzle-interface">
        <div class="board" role="group" aria-label="Three-row, five-column puzzle" aria-describedby="board-help"></div>
        <noscript><p>Enable JavaScript to play the grid puzzle. The case study explains the rules and proof.</p></noscript>
        <p class="board-help" id="board-help" hidden>Use arrow keys to move and Enter or Space to place a point.</p>
        <p class="board-status" role="status" aria-live="polite"></p>
        <div class="puzzle-controls" hidden><button type="button" data-undo>Undo</button><button type="button" data-reset>Clear board</button></div>
      </div>
    </section>
    <section class="wrap studio-section"><div class="section-head"><h2>More experiments</h2></div>
      <div class="reading-list compact">
        <article><h3>Debate prep</h3><p>Draw a motion, pick a side, and start the clock.</p><a href="archive.html#playground">Open the debate clock</a></article>
        <article><h3>Math sprint</h3><p>Try four short competition-style problems.</p><a href="archive.html#pg-math">Open the math sprint</a></article>
        <article><h3>Exposure lab</h3><p>Adjust aperture, shutter speed and ISO to balance an exposure.</p><a href="archive.html#pg-lens">Open the exposure lab</a></article>
      </div>
    </section>'''


def now():
    return intro('Now', 'Open <em>questions.</em>', 'Questions I carried forward from the work in this notebook.') + '''
    <div class="wrap reading-list">
      <article><h2>When should a model ask?</h2><p>After the ScentSense demonstration, I wanted visitors to have a way to correct a label or choose a scent for themselves.</p><a href="scentsense.html">ScentSense</a></article>
      <article><h2>How will the rig behave in waves?</h2><p>A wave-tank test would help us see how the Greenvolt Spark prototype behaves in more realistic conditions.</p><a href="greenvolt-spark.html">Greenvolt Spark</a></article>
      <article><h2>What changes when a door opens?</h2><p>Our sweep model kept smoke behavior fixed when a door opened. I’d like to see how opening one changes who gets reached first.</p><a href="himcm.html">HiMCM</a></article>
    </div>'''


def build():
    BUILT_ROUTES.clear()
    page('index.html', 'Proofs, prototypes & passing moments', 'The personal website of Shiyi Yang (Wendy). Explore mathematics research, engineering prototypes, writing, photography, songs and interactive experiments.', home())
    page('about.html', 'About Wendy', 'Shiyi Yang on cameras, laptop stickers and getting comfortable sharing unfinished ideas.', about(), active='About', image='assets/life/match-day.webp')
    page('notes.html', 'Notes & writing', 'Essays and reflections by Shiyi Yang on film, AI etiquette and editing.', notes(), active='Notes')
    page('studio.html', 'Photography, music & films', 'Photographs, songs and short films by Shiyi Yang.', studio(), active='Studio', image='assets/thumbs/city/DSC05866.webp')
    page('playground.html', 'Playground', 'Play a no-three-in-a-line puzzle and explore debate, competition math and photography experiments.', playground(), active='Playground', image='assets/evidence/no-three-grid-transform.jpg', css='<script src="puzzle.js" type="module"></script>')
    page('now.html', 'Now', 'Open questions from Shiyi Yang’s work in engineering and mathematical modeling.', now())
    for project in PROJECTS:
        page(project['slug'] + '.html', project['title'], project['premise'], case_study(project), image=project['image'])
    sitemap = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in BUILT_ROUTES + [SITE + path for path in ('archive.html', 'photography.html', 'activity-film.html')]:
        SubElement(SubElement(sitemap, 'url'), 'loc').text = url
    indent(sitemap)
    (ROOT / 'sitemap.xml').write_bytes(tostring(sitemap, encoding='utf-8', xml_declaration=True) + b'\n')


if __name__ == '__main__':
    build()

#!/usr/bin/env python3
"""
Static-site generator for this Obsidian vault.

Flow it supports:
  edit notes in Obsidian  ->  git push (raw Obsidian format)  ->
  GitHub Action runs this script  ->  ./public is deployed to GitHub Pages.

It converts Obsidian-flavored Markdown (wikilinks, image embeds, LaTeX,
fenced code) into a small, themed static site. Source notes are never modified.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from urllib.parse import quote
from dataclasses import dataclass, field
from pathlib import Path

import markdown as md

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
ASSETS = OUT / "assets"

SITE_TITLE = "Подготовка в магистратуру ИУ5"
SITE_SUBTITLE = "Конспекты и разборы задач для вступительного экзамена"

# Folders / files that are not content.
IGNORE_DIRS = {".git", ".obsidian", ".github", "scripts", "public", "node_modules"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

# Per-subject presentation metadata (matched by the subject's index-note name).
SUBJECT_META = {
    "Алгебра логики": {"emoji": "🧮", "order": 1},
    "Базы данных": {"emoji": "🗄️", "order": 2},
    "Сети": {"emoji": "🌐", "order": 4},
    "ВЕБ": {"emoji": "🎨", "order": 5},
    "Машинное обучение": {"emoji": "🤖", "order": 6},
}

# --------------------------------------------------------------------------- #
# Slugs / transliteration
# --------------------------------------------------------------------------- #

_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "",
    "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def translit(text: str) -> str:
    out = []
    for ch in text.lower():
        out.append(_TRANSLIT.get(ch, ch))
    return "".join(out)


def slugify(text: str) -> str:
    s = translit(text.strip())
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "page"


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Note:
    src: Path                 # source .md path
    title: str                # display title (filename without extension)
    key: str                  # normalized lookup key for wikilinks
    out_path: Path            # output .html path
    is_index: bool = False
    subject: "Subject | None" = None


@dataclass
class Subject:
    name: str                 # e.g. "Алгебра логики"
    folder: Path
    slug: str
    emoji: str
    order: int
    index: "Note | None" = None
    tasks: list[Note] = field(default_factory=list)

    @property
    def out_dir(self) -> Path:
        return OUT / self.slug

    @property
    def landing_url_note(self) -> "Note | None":
        return self.index or (self.tasks[0] if self.tasks else None)


def norm_key(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().lower()


def note_number(title: str) -> tuple[int, str]:
    m = re.match(r"\s*(\d+)", title)
    return (int(m.group(1)) if m else 999, title.lower())


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #

def discover() -> tuple[list[Subject], dict[str, Note], dict[str, str]]:
    subjects: list[Subject] = []
    note_by_key: dict[str, Note] = {}
    image_by_name: dict[str, str] = {}   # filename -> output url path (site-root relative)

    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name in IGNORE_DIRS:
            continue
        md_files = [p for p in folder.glob("*.md")]
        if not md_files:
            continue

        subject_name = re.sub(r"\s*\(task.*?\)\s*$", "", folder.name).strip()
        meta = SUBJECT_META.get(subject_name, {})
        subject = Subject(
            name=subject_name,
            folder=folder,
            slug=slugify(subject_name),
            emoji=meta.get("emoji", "📘"),
            order=meta.get("order", 99),
        )

        index_key = norm_key(subject_name)
        used_slugs: set[str] = set()
        for p in md_files:
            title = p.stem
            is_index = norm_key(title) == index_key
            if is_index:
                out_path = subject.out_dir / "index.html"
            else:
                base = slugify(title)
                slug = base
                i = 2
                while slug in used_slugs:
                    slug = f"{base}-{i}"
                    i += 1
                used_slugs.add(slug)
                out_path = subject.out_dir / f"{slug}.html"

            note = Note(
                src=p, title=title, key=norm_key(title),
                out_path=out_path, is_index=is_index, subject=subject,
            )
            note_by_key[note.key] = note
            if is_index:
                subject.index = note
            else:
                subject.tasks.append(note)

        subject.tasks.sort(key=lambda n: note_number(n.title))

        # Register images in this subject's image/ folder.
        img_dir = folder / "image"
        if img_dir.is_dir():
            for img in img_dir.iterdir():
                if img.suffix.lower() in IMAGE_EXTS:
                    image_by_name[img.name] = f"{subject.slug}/image/{img.name}"

        subjects.append(subject)

    subjects.sort(key=lambda s: (s.order, s.name))
    return subjects, note_by_key, image_by_name


# --------------------------------------------------------------------------- #
# Markdown / Obsidian conversion
# --------------------------------------------------------------------------- #

CODE_SPLIT = re.compile(r"(?s)(```.*?```)")
BLOCK_MATH = re.compile(r"(?s)\$\$(.+?)\$\$")
INLINE_MATH = re.compile(r"\$([^\n$]+?)\$")
EMBED = re.compile(r"!\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")
WIKILINK = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")


def relurl(from_dir: Path, to_site_rel: str) -> str:
    """Relative URL from a page's output dir to a site-root-relative path."""
    target = OUT / to_site_rel
    return os.path.relpath(target, start=from_dir).replace(os.sep, "/")


def convert(text: str, page: Note, note_by_key, image_by_name) -> tuple[str, str]:
    """Return (html, plaintext-for-search)."""
    page_dir = page.out_path.parent
    math_store: list[str] = []

    def stash_math(m: re.Match, display: bool) -> str:
        idx = len(math_store)
        raw = f"$$\n{m.group(1).strip()}\n$$" if display else f"${m.group(1).strip()}$"
        math_store.append(raw)
        return f"MZ{idx}ZM"

    def repl_embed(m: re.Match) -> str:
        name = m.group(1).strip()
        opt = (m.group(2) or "").strip()
        if Path(name).suffix.lower() in IMAGE_EXTS:
            site_rel = image_by_name.get(name)
            if not site_rel:
                return f'<span class="missing">🖼 {html.escape(name)}</span>'
            url = quote(relurl(page_dir, site_rel))
            style = ""
            if opt.isdigit():
                style = f' style="width:{opt}px"'
            alt = html.escape(name)
            return (f'<a class="imglink" href="{url}" data-lightbox>'
                    f'<img class="note-img" src="{url}" alt="{alt}" loading="lazy"{style}></a>')
        # Non-image embed -> link to the note.
        target = note_by_key.get(norm_key(name))
        if target:
            href = relurl(page_dir, str(target.out_path.relative_to(OUT)))
            return f'<a class="wikilink" href="{href}">{html.escape(opt or name)}</a>'
        return f'<span class="missing">{html.escape(name)}</span>'

    def repl_wikilink(m: re.Match) -> str:
        name = m.group(1).strip()
        alias = (m.group(2) or "").strip()
        label = alias or name
        target = note_by_key.get(norm_key(name))
        if target:
            href = relurl(page_dir, str(target.out_path.relative_to(OUT)))
            return f"[{label}]({href})"
        return f'<span class="missing">{html.escape(label)}</span>'

    # Process only outside fenced code blocks.
    parts = CODE_SPLIT.split(text)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        seg = BLOCK_MATH.sub(lambda m: stash_math(m, True), seg)
        seg = INLINE_MATH.sub(lambda m: stash_math(m, False), seg)
        seg = EMBED.sub(repl_embed, seg)
        seg = WIKILINK.sub(repl_wikilink, seg)
        parts[i] = seg
    text = "".join(parts)

    html_body = md.markdown(
        text,
        extensions=["extra", "sane_lists", "nl2br", "attr_list"],
        output_format="html5",
    )

    # Restore math (raw) for client-side KaTeX rendering.
    def restore(m: re.Match) -> str:
        return math_store[int(m.group(1))]

    html_body = re.sub(r"MZ(\d+)ZM", restore, html_body)

    # Search plaintext: strip tags + math.
    plain = re.sub(r"MZ\d+ZM", " ", "".join(parts))
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    return html_body, plain


# --------------------------------------------------------------------------- #
# HTML templates
# --------------------------------------------------------------------------- #

def root_prefix(page_dir: Path) -> str:
    rel = os.path.relpath(OUT, start=page_dir).replace(os.sep, "/")
    return "" if rel == "." else rel + "/"


def head(page_dir: Path, title: str, desc: str) -> str:
    a = relurl(page_dir, "assets/style.css")
    app = relurl(page_dir, "assets/app.js")
    root = root_prefix(page_dir)
    return f"""<!doctype html>
<html lang="ru" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<script>window.SITE_ROOT="{root}";(function(){{try{{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<link id="hl-light" rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
<link id="hl-dark" rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css" disabled>
<link rel="stylesheet" href="{a}">
<script defer src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script defer src="{app}"></script>
</head>"""


def theme_button() -> str:
    return ('<button class="icon-btn" id="theme-toggle" aria-label="Тема" title="Сменить тему">'
            '<span class="i-sun">☀️</span><span class="i-moon">🌙</span></button>')


def sidebar(subjects: list[Subject], page: Note | None, page_dir: Path) -> str:
    home = relurl(page_dir, "index.html")
    items = []
    for s in subjects:
        s_note = s.landing_url_note
        s_href = relurl(page_dir, str(s_note.out_path.relative_to(OUT))) if s_note else "#"
        active_sub = page is not None and page.subject is s
        children = []
        for t in s.tasks:
            t_href = relurl(page_dir, str(t.out_path.relative_to(OUT)))
            cls = "active" if page is t else ""
            children.append(f'<li><a class="{cls}" href="{t_href}">{html.escape(t.title)}</a></li>')
        idx_cls = "active" if (page is not None and page.is_index and page.subject is s) else ""
        open_attr = " open" if active_sub else ""
        items.append(
            f'<details class="nav-subject"{open_attr}>'
            f'<summary><span class="nav-emoji">{s.emoji}</span>'
            f'<span class="nav-name">{html.escape(s.name)}</span></summary>'
            f'<ul><li><a class="{idx_cls}" href="{s_href}">Обзор</a></li>'
            f'{"".join(children)}</ul></details>'
        )
    return f"""<aside class="sidebar" id="sidebar">
  <a class="brand" href="{home}"><span class="brand-mark">ИУ5</span>
    <span class="brand-text">Подготовка<br>к магистратуре</span></a>
  <button class="search-open" id="search-open">🔎 Поиск<span class="kbd">/</span></button>
  <nav class="nav">{"".join(items)}</nav>
  <div class="sidebar-foot"><a href="{home}">← На главную</a></div>
</aside>"""


def topbar(crumbs: list[tuple[str, str]]) -> str:
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if href and i < len(crumbs) - 1:
            parts.append(f'<a href="{href}">{html.escape(label)}</a>')
        else:
            parts.append(f'<span>{html.escape(label)}</span>')
    crumb_html = '<span class="sep">/</span>'.join(parts)
    return f"""<header class="topbar">
  <button class="icon-btn menu-btn" id="menu-btn" aria-label="Меню">☰</button>
  <nav class="crumbs">{crumb_html}</nav>
  <div class="spacer"></div>
  {theme_button()}
</header>"""


def page_shell(subjects, page: Note, body_html, page_dir, title, desc, crumbs) -> str:
    return f"""{head(page_dir, title, desc)}
<body>
<div class="layout">
{sidebar(subjects, page, page_dir)}
<div class="main">
{topbar(crumbs)}
<main class="content">
{body_html}
</main>
<footer class="page-foot">
  <p>Собрано из Obsidian-заметок · обновляется автоматически при <code>git push</code></p>
</footer>
</div>
</div>
{search_modal()}
</body></html>"""


def search_modal() -> str:
    return """<div class="search-modal" id="search-modal" hidden>
  <div class="search-box">
    <input type="text" id="search-input" placeholder="Искать по конспектам…" autocomplete="off">
    <ul id="search-results"></ul>
    <div class="search-hint">Enter — перейти · Esc — закрыть</div>
  </div>
</div>"""


# --------------------------------------------------------------------------- #
# Landing page
# --------------------------------------------------------------------------- #

def parse_scores() -> dict[str, str]:
    scores: dict[str, str] = {}
    readme = ROOT / "README.md"
    if readme.exists():
        for m in re.finditer(r"\[\[([^\]]+?)\]\][^\n(]*\((\d+)\s*балл", readme.read_text(encoding="utf-8")):
            scores[norm_key(m.group(1))] = m.group(2)
    return scores


def render_landing(subjects, note_by_key, image_by_name):
    scores = parse_scores()
    page_dir = OUT
    cards = []
    for s in subjects:
        note = s.landing_url_note
        href = relurl(page_dir, str(note.out_path.relative_to(OUT))) if note else "#"
        count = len(s.tasks)
        score = scores.get(norm_key(s.name))
        badge = f'<span class="badge">{score} баллов</span>' if score else ""
        meta = f"{count} " + plural(count, "задача", "задачи", "задач")
        cards.append(
            f'<a class="card" href="{href}">'
            f'<div class="card-emoji">{s.emoji}</div>'
            f'<div class="card-body"><h3>{html.escape(s.name)}</h3>'
            f'<p class="card-meta">{meta}</p></div>{badge}'
            f'<span class="card-arrow">→</span></a>'
        )

    total_notes = sum(len(s.tasks) for s in subjects)
    body = f"""<section class="hero">
  <div class="hero-badge">Экзамен ИУ5 · МГТУ им. Баумана</div>
  <h1>{html.escape(SITE_TITLE)}</h1>
  <p class="lead">{html.escape(SITE_SUBTITLE)}. Разборы типовых задач, формулы
     и готовые решения по каждому блоку экзамена.</p>
  <div class="hero-stats">
    <div><b>{len(subjects)}</b><span>предметов</span></div>
    <div><b>{total_notes}</b><span>разборов задач</span></div>
    <div><b>∞</b><span>попыток понять</span></div>
  </div>
</section>
<section class="cards">{"".join(cards)}</section>"""

    html_doc = f"""{head(page_dir, SITE_TITLE, SITE_SUBTITLE)}
<body class="landing">
<div class="layout">
{sidebar(subjects, None, page_dir)}
<div class="main">
{topbar([(SITE_TITLE, "")])}
<main class="content wide">
{body}
</main>
<footer class="page-foot">
  <p>Конспекты в Obsidian → GitHub → эта страница. Правки появляются автоматически.</p>
</footer>
</div>
</div>
{search_modal()}
</body></html>"""
    (OUT / "index.html").write_text(html_doc, encoding="utf-8")


def plural(n, one, few, many):
    n = abs(n) % 100
    n1 = n % 10
    if 11 <= n <= 14:
        return many
    if n1 == 1:
        return one
    if 2 <= n1 <= 4:
        return few
    return many


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    ASSETS.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    subjects, note_by_key, image_by_name = discover()

    # Copy images.
    for s in subjects:
        img_dir = s.folder / "image"
        if img_dir.is_dir():
            dest = s.out_dir / "image"
            dest.mkdir(parents=True, exist_ok=True)
            for img in img_dir.iterdir():
                if img.suffix.lower() in IMAGE_EXTS:
                    shutil.copy2(img, dest / img.name)

    search_index = []

    for s in subjects:
        notes = ([s.index] if s.index else []) + s.tasks
        for note in notes:
            text = note.src.read_text(encoding="utf-8")
            body_html, plain = convert(text, note, note_by_key, image_by_name)
            page_dir = note.out_path.parent
            s_note = s.landing_url_note
            s_href = relurl(page_dir, str(s_note.out_path.relative_to(OUT))) if s_note else "#"
            home = relurl(page_dir, "index.html")
            crumbs = [("Главная", home), (s.name, s_href)]
            if not note.is_index:
                crumbs.append((note.title, ""))

            title_html = (f'<div class="note-head"><span class="note-emoji">{s.emoji}</span>'
                          f'<h1>{html.escape(note.title if not note.is_index else s.name)}</h1></div>')
            article = f'<article class="note">{title_html}{body_html}</article>'
            # subject-level "next tasks" list on the overview page
            if note.is_index and s.tasks:
                links = "".join(
                    f'<a href="{relurl(page_dir, str(t.out_path.relative_to(OUT)))}">'
                    f'<span>{html.escape(t.title)}</span><em>→</em></a>'
                    for t in s.tasks
                )
                article += f'<section class="tasklist"><h2>Разборы задач</h2>{links}</section>'

            doc = page_shell(
                subjects, note, article, page_dir,
                title=f"{note.title} · {SITE_TITLE}" if not note.is_index else f"{s.name} · {SITE_TITLE}",
                desc=SITE_SUBTITLE, crumbs=crumbs,
            )
            note.out_path.parent.mkdir(parents=True, exist_ok=True)
            note.out_path.write_text(doc, encoding="utf-8")

            search_index.append({
                "title": note.title if not note.is_index else f"{s.name} (обзор)",
                "subject": s.name,
                "url": str(note.out_path.relative_to(OUT)).replace(os.sep, "/"),
                "text": plain[:600],
            })

    render_landing(subjects, note_by_key, image_by_name)

    (OUT / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8")

    write_assets()
    print(f"Built {len(search_index)} pages for {len(subjects)} subjects -> {OUT}")


def write_assets():
    (ASSETS / "style.css").write_text(CSS, encoding="utf-8")
    (ASSETS / "app.js").write_text(JS, encoding="utf-8")


# CSS / JS are defined in a sibling module to keep this file readable.
from site_assets import CSS, JS  # noqa: E402


if __name__ == "__main__":
    build()

# Сборка сайта из Obsidian-заметок

Этот каталог превращает заметки vault в статический сайт для GitHub Pages.
Исходные `.md`-файлы **не изменяются** — сборка читает их и генерирует `../public`.

## Как это работает (флоу)

```
правки в Obsidian  →  git push (сырой формат)  →  GitHub Action  →  GitHub Pages
```

- `.github/workflows/deploy.yml` запускается на каждый push в `main`.
- Ставит `markdown`, запускает `build_site.py`, публикует `public/` в Pages.
- Pages включается автоматически при первом запуске (`enablement: true`).

Сайт: **https://bmaks9.github.io/master/**

## Что поддерживается

- `[[вики-ссылки]]` и `[[ссылка|подпись]]`
- эмбеды картинок `![[image.png]]` и `![[image.png|ширина]]`
- LaTeX `$$...$$` и `$...$` (KaTeX)
- блоки кода с подсветкой (highlight.js)
- тёмная/светлая тема, поиск (`/`), лайтбокс для картинок

## Локальный предпросмотр

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install markdown
python scripts/build_site.py
python -m http.server -d public 8000   # → http://localhost:8000
```

## Добавить новый предмет

Создайте папку с заметками как обычно в Obsidian. Чтобы задать эмодзи и порядок
на главной, добавьте предмет в `SUBJECT_META` в `build_site.py` (необязательно —
без этого будет эмодзи по умолчанию 📘).

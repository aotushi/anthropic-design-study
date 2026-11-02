# HTML edition maintenance

The Chinese and English chapters are the content source. `scripts/build_html.py` renders both editions into `html/`, adds navigation and search, and builds an interactive evidence explorer from the recorded samples and pattern taxonomy.

The reading interface uses warm paper backgrounds, dark ink, a muted rust accent, system serif headings, and system sans-serif body text. This interface has its own typography; the study's original screenshots show the observed Anthropic fonts. No external font service or runtime network request is needed for reading or search.

- Desktop: persistent chapter navigation, a central reading column, and section links. On wide screens the section links use a side column; smaller screens use an expandable contents list.
- Narrow screens: a collapsible chapter menu, single-column content, and horizontally scrollable tables.
- Interaction: language links keep the current chapter; search finds chapter sections; figures open in a keyboard-accessible dialog; the explorer compares pages and filters patterns.
- Print: navigation and controls are removed, expandable gallery items are opened, and content is laid out for paper.

## Build and verify

1. Install `requirements-docs.txt` with Python's package installer.
2. Run `python scripts/build_html.py`.
3. Run `python scripts/validate.py` and `python scripts/validate_html.py`.
4. Preview with `python -m http.server 8765 --bind 127.0.0.1`, then open `http://127.0.0.1:8765/html/en/index.html`.
5. Install `requirements-test.txt` and run `python scripts/test_html.py` with Chrome available. The script starts and stops its own local server. Use `--channel chromium` in CI after installing Playwright's Chromium. Use `--base-url https://aotushi.github.io/anthropic-design-study` to check the published edition.

The generated HTML is committed so a downloaded repository can be opened directly at `html/zh/index.html` or `html/en/index.html`. Search data is embedded locally; no server is required for the downloaded edition. English is the default README and site entrance; `README.zh-CN.md` is the Chinese overview. `README.en.md` remains as a compatibility link.

GitHub Pages serves the same files from the `main` branch at `/`, with `.nojekyll` preserving the static output. Its publishing configuration follows the [GitHub Pages API documentation](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site). The document workflow rebuilds the HTML, checks that the committed output matches, validates both editions, and exercises the browser flows.

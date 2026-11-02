# HTML edition maintenance

The Chinese and English chapters are the content source. `scripts/build_html.py` renders both editions into `html/`, adds navigation and search, and builds an interactive evidence explorer from the recorded samples and pattern taxonomy.

The reading interface follows the documentation layout of [Claude Platform Docs](https://platform.claude.com/docs/en/get-started) and [Claude Code Docs](https://code.claude.com/docs/en/overview), reviewed in a browser on 2026-11-03. It uses a compact header, grouped chapter navigation, an article column, and an adjacent section index. The overview uses the same document structure as the chapters.

- Desktop: a persistent grouped sidebar, a bounded reading column, and a sticky section index from 1240px. Below that width the section index becomes an expandable contents list.
- Narrow screens: a collapsible chapter menu, single-column content, and horizontally scrollable tables.
- Interaction: language links keep the current chapter; search finds chapter sections; headings have direct links; the contents list follows the reading position; chapter copy buttons copy the Markdown source. Figures open in a keyboard-accessible dialog; the explorer compares pages and filters patterns.
- Print: navigation and controls are removed, expandable gallery items are opened, and content is laid out for paper.

## Visual foundations

| Element | Implemented choice | Reference relationship |
|---|---|---|
| Surfaces | `#FCFCFB` page, `#FFFFFF` media, `#F3F3F0` supporting surfaces | Platform Docs' measured page background; subtle separation between controls and content |
| Text | `#171717` headings, `#3E3E3E` body, `#62615B` secondary text | Dark headings and restrained secondary text, as seen in Code Docs |
| Layout | 60px header, 248px sidebar, article up to 832px, 200px section index | The three-column documentation structure; sizes adapted for this bilingual study |
| Typography | 32px page heading, 24px section heading, 15px article text; 28px page headings on mobile | Compact serif heading hierarchy with sans-serif reading text |
| Fonts | Georgia / Times New Roman headings; system sans-serif body and CJK fallbacks; system monospace code | Local substitutes retain the typographic roles. The study's screenshots show the observed Anthropic fonts |
| Components | Neutral selected navigation, 6–8px control corners, thin borders, horizontal table rules, understated hover states | Documentation controls and content take visual priority |
| Motion and input | Reduced-motion support, visible keyboard focus, 44px mobile controls, menu and dialog focus management | Reading and navigation remain usable across input methods |

No external font service or runtime network request is needed for reading, section search, or copying a chapter. Original screenshots and measurement records remain the research evidence; interface changes do not change the observation date of those samples.

## Build and verify

1. Install `requirements-docs.txt` with Python's package installer.
2. Run `python scripts/build_html.py`.
3. Run `python scripts/validate.py` and `python scripts/validate_html.py`.
4. Preview with `python -m http.server 8765 --bind 127.0.0.1`, then open `http://127.0.0.1:8765/html/en/index.html`.
5. Install `requirements-test.txt` and run `python scripts/test_html.py` with Chrome available. The script starts and stops its own local server. Use `--channel chromium` in CI after installing Playwright's Chromium. Use `--base-url https://aotushi.github.io/anthropic-design-study` to check the published edition.

The generated HTML is committed so a downloaded repository can be opened directly at `html/zh/index.html` or `html/en/index.html`. Search data is embedded locally; no server is required for the downloaded edition. English is the default README and site entrance; `README.zh-CN.md` is the Chinese overview. `README.en.md` remains as a compatibility link.

GitHub Pages serves the same files from the `main` branch at `/`, with `.nojekyll` preserving the static output. Its publishing configuration follows the [GitHub Pages API documentation](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site). The document workflow rebuilds the HTML, checks that the committed output matches, validates both editions, and exercises the browser flows.

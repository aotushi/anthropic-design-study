# HTML edition maintenance

The Chinese and English chapters are the content source. `scripts/build_html.py` renders both editions into `html/`, adds navigation and search, and builds an interactive evidence explorer from the recorded samples and pattern taxonomy.

The primary interface reference is [Claude Academy](https://academy.claude.com/), inspected on 2026-11-03. Its public homepage, catalog, guided start, and lesson provide the examples documented in [the interaction review](../docs/en/05-ux-and-responsive.md#academy-interactions). The overview is a learning hub; articles follow a lesson layout with adjacent chapter and section navigation. Earlier work on copy controls and section links also draws on Claude Platform Docs and Claude Code Docs.

- Desktop: grouped header menus, an 800px article column, and a 252px chapter selector and section index from 1240px. Below that width the section index becomes an expandable contents list.
- Narrow screens: a collapsible chapter menu, single-column content, and horizontally scrollable tables.
- Browsing: three illustrated topic cards lead to a filterable chapter library. Search and topic choices update the result count and URL, survive refresh, and remain selected across language changes. All ten chapters are immediately available.
- Reading: language links keep the current chapter; search finds chapter sections; headings have direct links; the contents list follows the reading position; chapter copy buttons copy the Markdown source. Figures open in a keyboard-accessible dialog. Each comparison sample switches between its screenshot and analysis; the explorer also filters component patterns.
- Themes: a header control switches between light and dark, stores the reader's choice locally, and uses the system preference initially. Source screenshots retain their captured colors.
- Print: navigation and controls are removed, expandable gallery items are opened, and content is laid out for paper.

## Visual foundations

| Element | Implemented choice | Reference relationship |
|---|---|---|
| Surfaces | `#FAFAF8` page, `#FCFCFB` cards, `#EEEDE9` hero; dark page `#181917` | Academy's neutral reading surfaces, with a separate hero panel and colored artwork |
| Text | `#141413` headings, `#41413D` body, `#67665F` secondary text; light text in dark mode | Clear heading, reading, and metadata levels |
| Layout | 60px header; 1080px overview content; 800px article, 64px gap, 252px section rail | Academy's broad catalog and lesson-with-outline arrangements, adapted to the handbook |
| Typography | 48px overview heading, 36px chapter heading, 24px section heading, 15px article text; 30px chapter headings on mobile | Serif display and section headings with sans-serif reading text |
| Fonts | Georgia / Times New Roman headings; system sans-serif body and CJK fallbacks; system monospace code | Local substitutes retain the typographic roles. The study's screenshots show the observed Anthropic fonts |
| Components | 16px topic and chapter cards, 14px menus, 6–8px controls, category underlines, radio-based view switch | Academy's rounded learning cards and visible selected states |
| Artwork | Three original inline SVG illustrations: typography, page layout, and research | Pastel learning-card imagery; separate from original source captures |
| Motion and input | Artwork scales to 1.04 over 300ms with ease-out; menu entrance 160ms; card filtering 180ms with short staggering | The artwork response follows measured Academy behavior; other timings are implementation choices |
| Accessibility | Reduced-motion mode, visible keyboard focus, 44px mobile controls, menu and dialog focus management | Pointer effects have keyboard equivalents; reading and search also work offline |

No external font service or runtime network request is needed for reading, section search, or copying a chapter. Original screenshots and measurement records remain the research evidence; interface changes do not change the observation date of those samples.

`web/style.css` and `web/app.js` supply the document and evidence components. `web/academy.css`, `web/academy.js`, and `web/academy.json` supply the Academy layout, browsing behavior, and bilingual labels. With JavaScript disabled, chapters and navigation links remain readable and both comparison views appear together.

## Build and verify

1. Install `requirements-docs.txt` with Python's package installer.
2. Run `python scripts/build_html.py`.
3. Run `python scripts/validate.py` and `python scripts/validate_html.py`.
4. Preview with `python -m http.server 8765 --bind 127.0.0.1`, then open `http://127.0.0.1:8765/html/en/index.html`.
5. Install `requirements-test.txt` and run `python scripts/test_html.py` with Chrome available. The script starts and stops its own local server. Use `--channel chromium` in CI after installing Playwright's Chromium. Use `--base-url https://aotushi.github.io/anthropic-design-study` to check the published edition.

The generated HTML is committed so a downloaded repository can be opened directly at `html/zh/index.html` or `html/en/index.html`. Search data is embedded locally; no server is required for the downloaded edition. English is the default README and site entrance; `README.zh-CN.md` is the Chinese overview. `README.en.md` remains as a compatibility link.

GitHub Pages serves the same files from the `main` branch at `/`, with `.nojekyll` preserving the static output. Its publishing configuration follows the [GitHub Pages API documentation](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site). The document workflow rebuilds the HTML, checks that the committed output matches, validates both editions, and exercises the browser flows.

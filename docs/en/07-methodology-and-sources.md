# 07 Methods and evidence

[中文](../07-methodology-and-sources.md) · **English**

[Overview](../../README.md) · [Screenshot gallery](06-gallery.md)

## Scope and date

Observation date: **2026-11-02, Asia/Shanghai**. The sample contains 10 representative pages across seven official sites. Academy home and Code Docs also have narrow captures; additional viewports and interaction states do not increase the page count.

The scope includes public company, product, official learning, and documentation pages. It excludes the Claude conversation interface, signed-in pages, third-party tutorials, other language editions, and historical versions. Capture tools block access to `claude.ai`.

## Source index

| ID | Sample | Source | Measurements |
|---|---|---|---|
| S01 | Anthropic company homepage | [Visit](https://www.anthropic.com/) | [JSON](../../data/pages/anthropic-home.json) |
| S02 | Claude product introduction | [Visit](https://claude.com/product/overview) | [JSON](../../data/pages/claude-product.json) |
| S03 | Pricing and comparison | [Visit](https://claude.com/pricing) | [JSON](../../data/pages/claude-pricing.json) |
| S04 | Resource library | [Visit](https://claude.com/resources) | [JSON](../../data/pages/claude-resources.json) |
| S05 | Academy homepage | [Visit](https://academy.claude.com/) | [JSON](../../data/pages/academy-home.json) |
| S06 | Academy lesson | [Visit](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) | [JSON](../../data/pages/academy-lesson.json) |
| S07 | Claude Code documentation | [Visit](https://code.claude.com/docs/en/overview) | [JSON](../../data/pages/code-docs.json) |
| S08 | Claude Platform documentation | [Visit](https://platform.claude.com/docs/en/get-started) | [JSON](../../data/pages/platform-docs.json) |
| S09 | Help center | [Visit](https://support.claude.com/en/) | [JSON](../../data/pages/support-home.json) |
| S10 | Developer blog | [Visit](https://claude.dev/) | [JSON](../../data/pages/developer-blog.json) |

Screenshot content, prices, and product names retain their state on the observation date. Follow the source links for current information.

## Classification and evidence

This handbook is an independent design analysis of public pages. Visual names and pattern categories are the study's framework; typography, color, dimensions, and interaction descriptions are supported by the records below.

| Type | Content | Basis |
|---|---|---|
| Page facts | Fonts, colors, structures, dimensions, and states after actions | Original screenshots, browser measurements, interaction records |
| Design interpretation | Relationships between visual form and reading tasks | Comparison and analysis of page facts |
| Application advice | Choices of layout, typography, and interaction for other projects | Task-based suggestions in the application guide |

**Three visual directions, eight page patterns, twenty component patterns, and font counts describe different levels and are counted independently.** The classification covers inspected samples. Components are grouped by task: browsing cards and plan-comparison cards are separate; a pattern appearing on several sites is counted once. The count describes visible interface patterns rather than source-code components.

## Measurement and capture environment

| Item | Method |
|---|---|
| Desktop | 1440 × 1000 CSS pixels, device scale factor 1, light mode |
| Narrow | 390 × 844 CSS pixels, device scale factor 1; a resized desktop browser |
| Page state | Public, signed out, English content, normal motion preference |
| Screenshots and diagrams | Browser-generated PNG captures preserve the original scene; project-created SVGs explain structure or color |
| Font styles | Record family, size, weight, line height, declarations, and loading state |
| Glyph rendering | Read the fonts actually used by selected text elements |
| Color | Read element styles, interpreting transparency against ancestor backgrounds |
| Dimensions | Record the specific page, element, and viewport |

Font families can have static and variable versions and aliases with different capitalization or separators. The study groups identifiable families while retaining original names. Icon fonts, fallback fonts, and individual weights are separate from core text-family counts.

## Verification coverage and capture states

| Area | Checked | Not yet verified |
|---|---|---|
| Interaction | Pricing audience, blog category, and lesson transcript selection states | Purchase and sign-in flows, video playback, saved progress, quizzes, search quality; code examples were not executed |
| Responsive layout | Two desktop/narrow pairs, text dimensions, document-wide overflow | Physical-phone touch, other devices and breakpoints, all overlays and expanded states |
| Accessibility | Four text/background contrast pairs and the first Resources keyboard focus | Full keyboard flows, target sizes, all interaction-state contrasts, site-wide WCAG auditing |
| Motion and outcomes | Visible dynamic scenes and relationships between structure and task | Animation timing and triggers, reduced-motion behavior, user efficiency, conversion, and performance experiments |

Two capture states affect interpretation and are marked beside the corresponding figures: the support sample used fallback fonts, and lesson video content had not appeared while text remained available. Font and color records retain the specific elements and browser state.

## Reference standards

Contrast calculations follow the [W3C explanation](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): 4.5 : 1 for normal text and 3 : 1 for qualifying large text, with specified exceptions. Calculations use sampled foreground colors and the nearest opaque ancestor background.

For further control inspection, WCAG 2.2 AA's [target-size criterion](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) uses 24 × 24 CSS pixels with spacing and other exceptions. The table above defines the checks performed here.

## Updating the study

1. Install Python and Playwright; source capture used Playwright 1.58.0 with Chrome.
2. Run `python scripts/capture.py --channel chrome` from the repository root for desktop samples.
3. Run `python scripts/capture.py --mobile --ids S05 S07 --channel chrome` for the two narrow samples.
4. Run `python scripts/check-interactions.py` to refresh the recorded interactions.
5. Inspect every screenshot, its loading state, and actual fonts; update both language editions.
6. Run `python scripts/analyze.py`, `python scripts/build_html.py`, `python scripts/validate.py`, and `python scripts/validate_html.py`; update the observation date and change log when evidence changes.

Recapture overwrites the corresponding evidence files, so use a separate branch. A source redesign may require updated selectors before its new results can be interpreted. HTML maintenance is described in the [build guide](../../web/README.md).

[Continue: Application guide](08-application-guide.md)

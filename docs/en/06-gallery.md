# 06 Screenshot gallery

[中文](../06-gallery.md) · **English**

[Overview](../../README.en.md) · [Previous: UX and responsive layouts](05-ux-and-responsive.md) · [Next: Methods and evidence](07-methodology-and-sources.md)

All screenshots were captured on **2026-11-02**. Desktop viewports are **1440 × 1000**, and narrow viewports are **390 × 844**. Expand an entry, then select its image to inspect the original size. Loading and animation states are described with the relevant figure.

## Ten representative pages

<details>
<summary>S01 · Anthropic company homepage</summary>

![Anthropic company homepage](../../assets/screenshots/anthropic-home.png)

The statement mixes Sans and Serif. The lower region shows a frame from dynamic content.

[Source](https://www.anthropic.com/) · [Measurements](../../data/pages/anthropic-home.json)

</details>

<details>
<summary>S02 · Claude product introduction</summary>

![Claude product introduction](../../assets/screenshots/claude-product.png)

The heading, main actions, and scene imagery introduce product use.

[Source](https://claude.com/product/overview) · [Measurements](../../data/pages/claude-product.json)

</details>

<details>
<summary>S03 · Claude pricing</summary>

![Claude pricing in its Individual state](../../assets/screenshots/claude-pricing.png)

The default Individual state organizes plan names, prices, descriptions, and main actions in columns.

[Source](https://claude.com/pricing) · [Measurements](../../data/pages/claude-pricing.json)

</details>

<details>
<summary>S04 · Claude Resources</summary>

![Claude Resources](../../assets/screenshots/claude-resources.png)

A faint grid, large serif heading, search field, and article cards.

[Source](https://claude.com/resources) · [Measurements](../../data/pages/claude-resources.json)

</details>

<details>
<summary>S05 · Claude Academy homepage</summary>

![Claude Academy homepage](../../assets/screenshots/academy-home.png)

Learning entrances, course branding, and product cards.

[Source](https://academy.claude.com/) · [Measurements](../../data/pages/academy-home.json)

</details>

<details>
<summary>S06 · Academy lesson</summary>

![Academy lesson page](../../assets/screenshots/academy-lesson.png)

Learning goals, duration, and contents. Video content had not appeared during capture.

[Source](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) · [Measurements](../../data/pages/academy-lesson.json)

</details>

<details>
<summary>S07 · Claude Code documentation</summary>

![Claude Code documentation](../../assets/screenshots/code-docs.png)

A desktop structure with left navigation, central text, and right page contents.

[Source](https://code.claude.com/docs/en/overview) · [Measurements](../../data/pages/code-docs.json)

</details>

<details>
<summary>S08 · Claude Platform documentation</summary>

![Claude Platform documentation](../../assets/screenshots/platform-docs.png)

Numbered steps and code within a three-column reading structure.

[Source](https://platform.claude.com/docs/en/get-started) · [Measurements](../../data/pages/platform-docs.json)

</details>

<details>
<summary>S09 · Claude help center</summary>

![Claude help center in the captured font-fallback state](../../assets/screenshots/support-home.png)

Search and topic collections organize the page. During capture, headings and body text fell back to Times New Roman, and keyboard hints to Consolas. See the [font records](02-typography.md#declared-loaded-and-rendered-fonts).

[Source](https://support.claude.com/en/) · [Measurements](../../data/pages/support-home.json)

</details>

<details>
<summary>S10 · Claude developer blog</summary>

![Claude developer blog](../../assets/screenshots/developer-blog.png)

A monospace name, topic filter, pixel imagery, and article rows.

[Source](https://claude.dev/) · [Measurements](../../data/pages/developer-blog.json)

</details>

## Narrow viewports and interaction states

<details>
<summary>Academy at a narrow width</summary>

![Academy at a narrow width](../../assets/screenshots/academy-home-mobile.png)

At a 390px-wide desktop-browser viewport, entrances form a single column, the heading wraps, and navigation contracts.

[Record](../../data/pages/academy-home-mobile.json)

</details>

<details>
<summary>Code Docs at a narrow width</summary>

![Code Docs at a narrow width](../../assets/screenshots/code-docs-mobile.png)

Side navigation collapses and the article becomes the main reading area.

[Record](../../data/pages/code-docs-mobile.json)

</details>

<details>
<summary>Pricing: Team & Enterprise</summary>

![Team and Enterprise pricing selection](../../assets/screenshots/pricing-team.png)

The selected tab corresponds to the Team and Enterprise plans below.

[Record](../../data/interaction-checks.json)

</details>

<details>
<summary>Lesson transcript selected</summary>

![Lesson with Transcript selected](../../assets/screenshots/academy-transcript.png)

Transcript is selected. The blank video region reflects its loading state during capture.

[Record](../../data/interaction-checks.json)

</details>

<details>
<summary>Code Docs code area</summary>

![Commands and copy controls in Code Docs](../../assets/screenshots/code-example.png)

Commands use Paper Mono, with copy controls and installation choices close to the code.

[Record](../../data/interaction-checks.json)

</details>

## Original explanatory diagrams

![Three visual directions](../../assets/diagrams/en/design-map.svg)

![Measured color samples](../../assets/diagrams/en/color-samples.svg)

![Three approaches to assigning space](../../assets/diagrams/en/layout-archetypes.svg)

These three diagrams organize visual directions, sampled colors, and spatial arrangements for comparison with the screenshots.

[Next: Methods and evidence](07-methodology-and-sources.md)

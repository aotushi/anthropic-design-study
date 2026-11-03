# 05 UX and responsive observations

[中文](../05-ux-and-responsive.md) · **English**

[Overview](../../README.md) · [Previous: Components](04-components.md) · [Next: Screenshot gallery](06-gallery.md)

## Helping readers take the next step

Visual hierarchy works alongside information structure. A large heading attracts attention, but readers also need a next action. A substantial article needs ways to locate sections and return to context.

| Situation | Support in the samples | Design reading |
|---|---|---|
| First encounter with a product | Brief description, scenarios, prominent main action | Establish use before inviting action |
| Comparing plans | Audience selection, plan cards, detailed table | Separate initial assessment from close comparison |
| Finding technical content | Navigation tree, search, page contents | Support browsing and direct location |
| Following instructions | Numbered steps, code, nearby copy controls | Keep explanation and execution material together |
| Learning in sequence | Goals, duration, next lesson | Supply a starting point and a continuing route |

## Verified interactions

These results come from actions on public pages. See [interaction-checks.json](../../data/interaction-checks.json).

| Check | Observed result | Observed element |
|---|---|---|
| Pricing audience selection | Switching Individual to Team & Enterprise displays the corresponding plans | Selected tab state and plan headings |
| Blog topic filter | The list changes from 10 items to 1, then returns to 10 with ALL | Category selection and visible article count |
| Lesson transcript selection | Transcript becomes selected and the state updates | Selected state of the content switch |
| Documentation code font | Sampled code renders with Paper Mono | Text in the code area |
| Resources first keyboard focus | The first Tab reaches Skip to main content | Keyboard entrance past navigation |

![Academy after selecting the transcript, with chapter navigation alongside the text](../../assets/screenshots/academy-transcript.png)

*Figure 10 · [Lesson S06](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency). The video area was blank while loading during capture; the transcript control and lower text were available.*

This lesson offers video and text as two learning formats. Text and chapter navigation remain available while the video resource is not ready.

## Academy interactions

**Nine interaction patterns were examined on 2026-11-03; eight inform this handbook.** The strongest reference is [Claude Academy](https://academy.claude.com/): readers can see which cards are actionable, narrow a collection, choose a learning path, and keep their place inside a lesson. The follow-up used public pages in a fresh browser session, at 1440 × 1000 and 390 × 844. [Action and measurement record](../../data/academy-interactions.json)

| Pattern | What happened on Academy | Decision for this handbook |
|---|---|---|
| **1. Card hover** | On sampled product and course cards, the inner artwork scales to **1.04** over **300ms**, with an ease-out curve; a subtle overlay appears. The text and outer frame stay in place. | **Adopt.** Topic and chapter illustrations respond to hover and keyboard focus. Keep the title stable so the card remains easy to read. |
| **2. Grouped menus** | Hovering Explore opens a three-column menu; Escape closes it. Resources has a smaller dropdown. | **Adopt.** Explore groups the chapters by subject; Resources gathers the overview, comparison page, and evidence. Click and keyboard access accompany hover. |
| **3. Global search** | The header search opens an overlay. A “Claude Code” query displayed six result options in the inspected state. | **Retain and refine.** Search the handbook's sections in a dialog, with arrow-key navigation and Escape to return to the trigger. |
| **4. Collection filtering** | In [All resources](https://academy.claude.com/all), selecting Courses and searching “Claude Code” changed the cards, count, and address to `?kind=course&q=Claude+Code`. The inspected course count changed from 28 to 12 results. | **Adapt.** Four topic tabs and a chapter search update the cards, result count, and shareable address. Include a clear action and a useful empty state. |
| **5. Guided entry** | In [Get started](https://academy.claude.com/start), choosing Claude Code advances to a choice between learning to use it and rolling it out to a team. | **Simplify.** Three illustrated starting points lead directly to matching chapters. A ten-chapter collection needs only one choice. |
| **6. Theme switching** | The header theme control changes the page from light surfaces to dark surfaces. | **Adopt.** Provide light and dark reading modes, remember the choice in the browser, and keep source screenshots in their original colors. |
| **7. Content format switch** | In the [AI Fluency lesson](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency), Summary and Transcript form a radio group. Selecting Transcript changes both the selected state and the text. | **Adapt.** The comparison page switches each sample between Screenshot and Analysis. This gives the same page two useful reading views. |
| **8. Lesson orientation** | The lesson shows its position within the course, a chapter selector, section links, and a next-lesson entrance. At 390px, the chapter control opens a sheet containing the course list. | **Adapt.** Articles show the current chapter and a desktop chapter selector alongside section links. The mobile chapter drawer and previous/next links retain orientation in a narrow layout. |
| **9. Load more** | In the resource catalog, clicking Load more increased rendered resource cards from **24 to 48**. | **Omit.** Ten chapters fit in one collection. Filtering is useful; an additional reveal step is unnecessary. |

### Menus and visible feedback

![Academy's Explore menu expanded into three grouped columns above the homepage](../../assets/academy-interactions/explore-menu.png)

*Academy interaction capture A1 · [Homepage](https://academy.claude.com/) · 1440 × 1000 · 2026-11-03. The expanded panel groups routes into separate columns while the page stays visible behind it.*

Card movement is deliberately small. Enlarging the illustration supplies a clear response without moving the heading or changing the card's footprint. In this handbook, the same response is available on keyboard focus, and the illustration stays still when the reader requests reduced motion. Menus use a short entrance transition; the selected topic has an underline; filtered cards make a brief, restrained entrance.

### A collection that explains its current state

![Academy's course catalog filtered by Claude Code, showing the selected category, query, result count, and matching cards](../../assets/academy-interactions/filtered-search.png)

*Academy interaction capture A2 · [Filtered catalog](https://academy.claude.com/all?kind=course&q=Claude+Code) · 1440 × 1000 · 2026-11-03.*

The selected category, visible query, count, and cards describe the same state. This is more useful than an animated tab alone. The handbook carries that relationship into its chapter library: readers can copy a filtered address, refresh it, go back to a previous topic, or change language while keeping the filter. Clearing the controls restores all ten chapters.

### A reading surface with a second theme

![Academy homepage in dark mode, with dark surfaces, light text, and colored product illustrations](../../assets/academy-interactions/home-dark.png)

*Academy interaction capture A3 · [Homepage](https://academy.claude.com/) · 1440 × 1000 · 2026-11-03.*

Changing theme affects the reading surface, controls, and text hierarchy. Research images remain source material: the handbook displays their captured colors in both themes so that color comparisons continue to make sense.

### Course navigation on a narrow screen

<img src="../../assets/academy-interactions/mobile-outline-open.png" width="390" alt="Academy's mobile course contents sheet open over the lesson, with the current lesson and grouped lesson links">

*Academy interaction capture A4 · [AI Fluency lesson](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) · 390 × 844 · 2026-11-03.*

The course list becomes an explicit overlay instead of compressing the reading column. The handbook uses its chapter drawer for the same job. On a wide screen, a compact chapter selector sits next to the article; section links below it track the current reading position. The next-chapter link keeps sequential reading available at the end of the page.

## Desktop and narrow viewports

<table>
<tr><th>Academy: 390 × 844</th><th>Code Docs: 390 × 844</th></tr>
<tr>
<td><img src="../../assets/screenshots/academy-home-mobile.png" width="390" alt="Academy at a narrow width, with wrapped headings, compact navigation, and a single column of learning entrances"></td>
<td><img src="../../assets/screenshots/code-docs-mobile.png" width="390" alt="Code Docs at a narrow width, with collapsed side navigation and a wider central reading area"></td>
</tr>
</table>

*Figures 11–12 · Both captures use a desktop browser resized to a 390 × 844 viewport.*

| Element | Desktop, 1440px wide | Narrow, 390px wide |
|---|---|---|
| Academy main heading | 48px, line height 52.8px | 44px, line height 48.4px; wraps across lines |
| Academy description | 18px, line height 28px | Remains 18px / 28px |
| Academy content entrances | Multiple card columns | One vertical column with adjusted image/text relationships |
| Code Docs main heading | 36px, line height 40px | 30px, line height 36px |
| Code Docs introduction | 16px, line height 26.4px | Remains 16px / 26.4px |
| Code Docs navigation | Left navigation, central article, right contents | One main reading column with compact navigation entrances |
| Document-wide horizontal overflow | None detected in either sample | None detected in either sample |

Evidence: [Academy desktop](../../data/pages/academy-home.json), [Academy narrow](../../data/pages/academy-home-mobile.json), [Code Docs desktop](../../data/pages/code-docs.json), [Code Docs narrow](../../data/pages/code-docs-mobile.json).

The narrow layout **redistributes space**: some headings shrink, body text retains its size, navigation becomes compact, and cards form a single column. Content priority drives the arrangement.

## Four text contrast checks

Contrast is calculated from the sampled text color and its nearest opaque ancestor background. The Resources hero sits on `#F5F4ED`, inside a page whose outer background is `#FAF9F5`; the calculation uses the panel behind the text.

| Sample | Text | Background | Approximate contrast |
|---|---|---|---:|
| Resources heading | #141413 | #F5F4ED | 16.72 : 1 |
| Resources description | #30302E | #F5F4ED | 11.99 : 1 |
| Platform heading | #0B0B0B | #FCFCFB | 19.17 : 1 |
| Platform description | #52514E | #FCFCFB | 7.73 : 1 |

W3C's minimum is 4.5 : 1 for normal text and 3 : 1 for qualifying large text, with specified exceptions. [W3C contrast explanation](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

All four pairs exceed the normal-text threshold. Both pages use dark headings and slightly lighter descriptions to establish hierarchy while keeping supporting text at a high contrast. [Calculated data](../../data/derived-checks.json) · [Calculation script](../../scripts/analyze.py)

## Turning observations into design decisions

| Design concern | Concrete treatment | Application |
|---|---|---|
| State matches content | Pricing selection updates the corresponding plans | Keep selected styling aligned with displayed content |
| Learning formats are available | A transcript entrance accompanies the lesson | Make alternate content easy to find |
| Narrow layouts preserve reading priority | Body text stays the same size as navigation collapses | Arrange content order before adjusting dimensions |
| Keyboard entry supports the main task | Resources starts focus at a skip link | Provide a direct route into the main content |
| Hierarchy retains clarity | Descriptions are lighter than headings but still high contrast | Check both hierarchy and legibility |

[Next: Screenshot gallery](06-gallery.md)

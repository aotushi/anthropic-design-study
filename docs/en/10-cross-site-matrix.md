# 10 Cross-site design matrix

[中文](../10-cross-site-matrix.md) · **English**

[Overview](../../README.en.md) · [Previous: Page anatomy](09-page-anatomy.md)

Comparing sites separates the elements that maintain identity from those that change with the task. This chapter compares reading tasks, typographic roles, and recorded pattern distribution.

## Reading tasks across ten samples

| Sample | Main task | Spatial organization | Identifying detail |
|---|---|---|---|
| S01 Company | Understand the company's focus | Large statement and selected content | Sans and Serif within one main heading |
| S02 Product | Recognize product uses | Heading, main actions, scenario demonstrations | Task and outcome imagery |
| S03 Pricing | Choose a suitable plan | Audience selection, plan cards, comparison | Parallel plans and clear action entrances |
| S04 Resources | Browse or find content | Categories, search, cards | Pale grid, large serif heading, line illustrations |
| S05 Academy home | Choose a learning route | Learning topics and cards | Product imagery and course names |
| S06 Lesson | Complete a unit of learning | Goals, material, sections, subsequent links | Duration labels and a goals callout |
| S07 Code Docs | Start using a developer tool | Three reading columns and installation choices | Serif Display headings, Paper Mono code |
| S08 Platform Docs | Complete technical setup | Three reading columns, steps, code | Compact headings and Anthropic Mono |
| S09 Help center | Resolve a problem | Search, topic collections, common questions | Problem-oriented entrances |
| S10 Developer blog | Scan technical articles | Topic filtering and article rows | Monospace labels and pixel graphics |

Page URLs and records appear in the [source index](07-methodology-and-sources.md#source-index).

## Typographic roles compared

| Context | Headings or identity | Reading and controls | Technical material |
|---|---|---|---|
| Company | Mixed Sans and Serif statement | Anthropic Sans | Primarily brand narrative |
| Resources | Anthropic Serif | Anthropic Sans | Card metadata and retrieval controls |
| Academy | Anthropic Serif | Anthropic Sans | Duration, chapters, and learning cues |
| Code Docs | Anthropic Serif Display | Anthropic Sans | Paper Mono code |
| Platform Docs | Anthropic Serif | Anthropic Sans | Anthropic Mono code |
| Developer blog | Anthropic Mono site name | Anthropic Sans article titles and body | Anthropic Mono metadata |

The help center is recorded separately: it declares Anthropic Sans, Anthropic Serif, and local JetBrains Mono, while sampled text fell back to Times New Roman and Consolas. See the [typography chapter](02-typography.md#declared-loaded-and-rendered-fonts).

## Recorded pattern distribution

The table lists verified representative samples for each pattern. One pattern can occur on several pages. The HTML edition also offers filters by task group.

| Pattern | Representative samples | Consider when combining |
|---|---|---|
| P01 Top dropdown navigation | S01, S04 | Grouping site entrances |
| P02 Secondary category bar | S04 | Current content scope |
| P03 Breadcrumbs | S06, S08 | Hierarchy and return paths |
| P04 Sidebar navigation and contents | S06, S07, S08 | Site position and article position |
| P05 Site search | S04, S07, S09 | Direct location of target content |
| P06 Category filtering | S10 | Constraining the article collection |
| P07 Tabs and segmented selection | S03, S07, S08 | Matching selection to displayed content |
| P08 Expand and collapse | S03, S07 | Revealing detail as needed |
| P09 Large-heading hero | S01, S02, S04 | Page topic and primary action |
| P10 Card grid | S04, S05 | Scannable parallel content |
| P11 Article rows | S10 | Alignment of titles and metadata |
| P12 Product demonstration | S02 | Connecting scenarios to use |
| P13 Plan cards | S03 | Overall impressions of options |
| P14 Feature comparison table | S03 | Differences across plans |
| P15 Numbered steps | S08 | Prerequisites, actions, results |
| P16 Next lesson or next step | S06 | Continuing from the current content |
| P17 Video and text switching | S06 | Learning-format choices |
| P18 Highlighted callout | S06 | Goals and key conditions |
| P19 Code block and copy | S07, S08 | Proximity of explanation and execution material |
| P20 Duration and position cues | S05, S06 | Commitment and current position |

Sources: [taxonomy](../../data/taxonomy.json) · [component descriptions](04-components.md).

## Choose a combination for your page

| Content condition | Useful combination | Content preparation |
|---|---|---|
| Many items and varied reader intentions | Category bar + search + cards or rows | Clear types, titles, and summaries |
| Actions depend on earlier steps | Contents + numbered steps + code copying | Prerequisites, results, troubleshooting |
| Several options need comparison | Audience selection + plan cards + comparison | Applicable scope, differences, selection conditions |
| Learning follows a sequence | Goals + duration + sections + next lesson | Objectives, exercises, a continuing route |

Choose the task combination before adjusting typography, color, and density. This turns the observations into a purposeful interface proposal.

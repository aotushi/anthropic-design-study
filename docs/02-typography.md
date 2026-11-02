# 02 字体与排版

**中文** · [English](en/02-typography.md)

[返回总览](../README.zh-CN.md) · [上一章：视觉语言](01-visual-language.md) · [下一章：页面模式](03-page-patterns.md)

## 五个主要名称与四个核心家族

主要文字字体如下表，名称由页面字体设置、加载记录与抽样文字的实际渲染共同核对。

| 名称 | 字体类别 | 主要角色 | 证据 |
|---|---|---|---|
| **Anthropic Sans** | 无衬线 | 正文、导航、按钮、卡片说明 | [S04](../data/pages/claude-resources.json)、[S05](../data/pages/academy-home.json)、[S08](../data/pages/platform-docs.json) |
| **Anthropic Serif** | 衬线 | 品牌标题、页面标题、部分卡片标题 | [S01](../data/pages/anthropic-home.json)、[S04](../data/pages/claude-resources.json)、[S05](../data/pages/academy-home.json) |
| **Anthropic Serif Display** | 衬线展示变体 | Claude Code 文档标题 | [S07](../data/pages/code-docs.json) |
| **Anthropic Mono** | 等宽 | Platform 代码、开发者博客标题及标签 | [S08](../data/pages/platform-docs.json)、[S10](../data/pages/developer-blog.json) |
| **Paper Mono** | 等宽 | Claude Code 文档代码块 | [S07](../data/pages/code-docs.json)、[代码区进一步核验](../data/interaction-checks.json) |

按页面中的主要字体名称计为 **5 个**；将 Serif Display 作为 Serif 的展示变体归并，则为 **4 个核心家族**。这个口径不把同一字体的粗体、斜体、变量版本或备用名称重复计算。

## 字体的三种职责

**标题营造语气，正文保持易读，等宽文字表达技术结构。** 同一类字体也能跨越不同角色，例如公司首页用无衬线与衬线文字共同组成主标题，开发者博客则用等宽字体呈现站名。

![Anthropic 公司首页，一段大标题混合无衬线与衬线文字](../assets/screenshots/anthropic-home.png)

*图 3 · [Anthropic 公司首页 S01](https://www.anthropic.com/) · 同一段主标题的开头使用无衬线字体，后续说明使用衬线字体。下方内容为该时刻的动态展示帧。*

公司首页通过字形与字重的变化，把简短的主张与较长的说明放在同一段视觉结构中。浏览器的渲染记录同时识别到 Sans 和 Serif，对应标题内部两种不同的表达。

开发者博客的站名标题使用 Anthropic Mono，将等宽字形带入站点识别，并与分类、日期等技术性标签呼应。

## 真实页面中的字号层级

以下为 **1440 × 1000** 桌面视口下的测量值，字号与行高均以像素表示。

| 页面与文字角色 | 字号 | 行高 | 字重 | 来源 |
|---|---:|---:|---:|---|
| Claude Resources 主标题 | 72 | 79.2 | 500 | [S04](../data/pages/claude-resources.json) |
| Resources 首屏说明 | 23 | 34.5 | 400 | [S04](../data/pages/claude-resources.json) |
| Pricing 主标题 | 64 | 70.4 | 500 | [S03](../data/pages/claude-pricing.json) |
| Academy 首页主标题 | 48 | 52.8 | 400 | [S05](../data/pages/academy-home.json) |
| Academy 首页说明 | 18 | 28 | 400 | [S05](../data/pages/academy-home.json) |
| Academy 课程内页主标题 | 36 | 54 | 400 | [S06](../data/pages/academy-lesson.json) |
| Code Docs 主标题 | 36 | 40 | 400 | [S07](../data/pages/code-docs.json) |
| Code Docs 介绍段落 | 16 | 26.4 | 400 | [S07](../data/pages/code-docs.json) |
| Code Docs 代码 | 14 | 24 | 400 | [S07](../data/pages/code-docs.json) |
| Platform 文档主标题 | 26.25 | 32.8125 | 520 | [S08](../data/pages/platform-docs.json) |
| 开发者博客站名 | 31.5 | 34.65 | 400 | [S10](../data/pages/developer-blog.json) |

营销和资源入口使用较大的标题，文档用更紧凑的标题为正文留出空间：Resources 主标题为 72px，Platform 文档主标题为 26.25px。表中保留变量字体的实际字重，例如 Platform 标题的 520，以呈现页面真实的排版差异。

## 两个文档站的等宽字体并不相同

![Claude Code 文档代码区，命令、复制按钮、安装方式切换与说明并列](../assets/screenshots/code-example.png)

*图 4 · [Claude Code 文档 S07](https://code.claude.com/docs/en/overview) · 代码区的 Paper Mono 与 Platform 文档的 Anthropic Mono 是不同的字体选择。*

两站共享“正文与代码区分开”的阅读逻辑，但使用不同的等宽字体。对设计复用而言，更值得保留的是代码和自然语言之间的清晰边界，以及复制、平台切换等操作与内容的接近程度。

## 声明加载与实际渲染

| 层次 | 核对内容 | 对应证据 |
|---|---|---|
| 页面声明 | 文字元素设置的首选与备用字体 | 元素样式与字体规则 |
| 字体加载 | 浏览器已加载的字体资源 | 字体加载记录 |
| 实际渲染 | 抽样文字的字形来源 | 浏览器返回的元素字体记录 |

**帮助中心的字体声明与实际渲染存在差异。** 页面声明了 Anthropic Sans、Anthropic Serif 的站点别名，并为快捷键提示指定 JetBrains Mono；本次采集的正文和标题却回退到 Times New Roman，快捷键回退到 Consolas。截图呈现的是这一回退状态。

因此，JetBrains Mono 作为局部声明单独记录，Times New Roman 与 Consolas 作为回退字体记录，均不加入上表的核心字体计数。具体字段见 [S09 的 renderedFonts 与 fontRuleSources](../data/pages/support-home.json)。

## 字体别名与非文字字库

| 样本中出现的名称 | 研究中的归并 |
|---|---|
| `anthropicSans`、`anthropic-sans`、`Anthropic Sans` | Anthropic Sans |
| `anthropicSerif`、`anthropic-serif` | Anthropic Serif |
| `anthropicMono`、`Anthropic Mono` | Anthropic Mono |
| 含 Fallback 的名称，以及 Arial、Georgia 等后备项 | 不独立计为核心品牌字体 |
| `Anthropicons-Variable` | 图标字库，不计入文字字体 |
| 字体文件中的 Text、Web、Variable、Light 等描述 | 保留在原始证据中，不自动视为新的设计家族 |

## 将排版用于中文

原站样本主要是英文。中文排版需要另行确认字体的字符覆盖，并用真实中文内容检查标点、字重、中英文混排和换行。这样才能保留标题与正文的层级，同时适应不同的字面密度和阅读节奏。

[下一章：八类页面模式](03-page-patterns.md)

# Anthropic 与 Claude 网站设计研究

**中文** · [English](README.en.md) · [阅读 HTML 版](https://aotushi.github.io/anthropic-design-study/html/zh/index.html)

**提供中英文文档与 HTML 阅读站点的 UI/UX 图文手册。**

研究 Anthropic 如何用字体、色彩、留白、插画和信息结构，将公司官网、产品介绍、开发文档与课程连接成具有一致识别度的网站体系。10 个章节结合截图、测量、对照表与页面拆解，展示设计细节怎样服务于阅读任务。这里的 Anthropic 指 Claude 的开发公司。

![研究总览：编辑式品牌表达、知识阅读布局与开发者风格三种方向](assets/diagrams/design-map.svg)

> **观察日期：2026-11-02 · 范围：7 个官方站点、10 个代表页面。**
> 另收录 Academy 与 Claude Code 文档的 390 × 844 窄屏样本。完整范围与统计口径见[方法与证据](docs/07-methodology-and-sources.md)。

## 选择阅读形式

| 形式 | 适合做什么 | 入口 |
|---|---|---|
| HTML 手册 | 章节导航、搜索、图片放大与打印阅读 | [中文](https://aotushi.github.io/anthropic-design-study/html/zh/index.html) · [English](https://aotushi.github.io/anthropic-design-study/html/en/index.html) |
| 交互对照 | 页面并排比较、字号图表与模式筛选 | [浏览图像与数据](https://aotushi.github.io/anthropic-design-study/html/zh/explore.html) |
| GitHub 文档 | 阅读原文、查看证据与追踪修改 | 下方章节目录 |
| 离线 HTML | 下载后直接阅读与搜索 | [下载仓库 ZIP](https://github.com/aotushi/anthropic-design-study/archive/refs/heads/main.zip)，打开 `html/zh/index.html` |

## 从这里开始

| 你想了解什么 | 阅读入口 |
|---|---|
| 为什么这些页面具有统一的品牌感 | [01 视觉语言](docs/01-visual-language.md) |
| 究竟用了哪些字体，分别承担什么角色 | [02 字体与排版](docs/02-typography.md) |
| 官网、定价、教程和文档的布局如何变化 | [03 八类页面模式](docs/03-page-patterns.md) |
| 哪些组成部分可以复用 | [04 二十类组件与布局模式](docs/04-components.md) |
| 页面如何帮助阅读、查找和继续学习 | [05 UX 与响应式观察](docs/05-ux-and-responsive.md) |
| 直接对照真实网页 | [06 截图图库](docs/06-gallery.md) |
| 查阅来源、统计口径与验证范围 | [07 方法与证据](docs/07-methodology-and-sources.md) |
| 将研究转化为自己的设计 | [08 应用指南](docs/08-application-guide.md) |
| 看清页面各区域如何配合 | [09 页面拆解](docs/09-page-anatomy.md) |
| 比较不同站点的共同点与变化 | [10 跨站设计矩阵](docs/10-cross-site-matrix.md) |

## 核心发现

**它们共享一套品牌基础，但根据读者任务改变表达方式。** 官网用大标题和图像建立印象，资源中心帮助用户找到内容，文档将空间留给正文与目录，开发者博客则用像素图形和等宽文字强调技术社区的气质。

| 统计层级 | 样本归纳 | 如何理解 |
|---|---:|---|
| 整体视觉方向 | 3 类 | 温暖的编辑式表达、克制的知识界面、复古开发者表达 |
| 页面模式 | 8 类 | 公司官网、产品介绍、定价比较、资源库、技术文档、课程、帮助中心、开发者出版物 |
| 可复用模式 | 20 类 | 按任务和使用方式归并的导航、检索、展示、比较与学习组件 |
| 核心文字字体名称 | 5 个 | Anthropic Sans、Anthropic Serif、Anthropic Serif Display、Anthropic Mono、Paper Mono |
| 核心字体家族 | 4 组 | 将 Serif Display 归入 Serif 家族后的研究口径 |

以上分别回答“整体是什么风格”“页面怎样组织”“哪些模式可复用”和“使用什么字体”。字体的实际渲染与帮助中心的回退情况见[字体证据](docs/02-typography.md#声明加载与实际渲染)。

## 三个页面看懂差异

| 品牌与资源表达 | 知识阅读 | 开发者出版物 |
|---|---|---|
| ![Claude 资源中心，衬线大标题位于浅色网格和文章卡片之间](assets/screenshots/claude-resources.png) | ![Claude Platform 文档，左侧导航、中央正文和右侧目录并列](assets/screenshots/platform-docs.png) | ![Claude 开发者博客，等宽标签、像素图形和按行排列的文章](assets/screenshots/developer-blog.png) |
| [原站 S04](https://claude.com/resources) | [原站 S08](https://platform.claude.com/docs/en/get-started) | [原站 S10](https://claude.dev/) |

点击图片可查看原始尺寸，对照标题、导航和内容区域的空间分配。

## 共同的设计基础

- **背景与文字形成温和但清晰的对比。** 多个官网样本使用接近纸张的浅色背景和接近黑色的文字，形成带有暖色的阅读底色。
- **字体分工比字体数量更重要。** 衬线字体常用于标题，无衬线字体负责正文和控件，等宽字体承担代码及技术标签。Anthropic 公司首页还在同一段大标题里混合使用前两者。
- **内容密度随任务变化。** 品牌页面留白较多；文档把导航、正文和定位工具同时放到桌面视野内；课程突出学习目标和下一步。
- **装饰具有站点差异。** 资源中心用线描插画与漂浮卡片呈现内容，开发者博客用像素图形与等宽标签建立技术社区的识别。

## 证据与维护

本手册提供三层材料：**正文中的设计解读 → 原始截图 → 页面测量记录**。每个代表页面均有原站链接和本地记录，可从[来源索引](docs/07-methodology-and-sources.md#页面来源索引)追溯。

<details>
<summary>查看仓库结构与维护方式</summary>

- `docs/` 与 `docs/en/`：中英文图文手册。
- `html/`：可在线阅读或下载打开的 HTML 版本。
- `assets/screenshots/`：浏览器采集的网页截图。
- `assets/diagrams/`：3 张原创结构与色彩示意图，分别提供中英文版本。
- `data/pages/`：页面字体、颜色、尺寸和采集环境记录。
- `data/sample-manifest.json`：样本范围。
- `web/`：HTML 版共享样式、交互与[构建说明](web/README.md)。
- `scripts/`：采集、构建与验证工具。

修改后运行 `python scripts/build_html.py`、`python scripts/validate.py` 和 `python scripts/validate_html.py`，更新 HTML 并检查引用与证据。重新采集需要 Python、Playwright 和浏览器，具体步骤见[维护说明](docs/07-methodology-and-sources.md#如何更新研究)。

</details>

原创文字与示意图按 [CC BY 4.0](LICENSE) 提供；网页截图、商标与字体的使用范围见[素材说明](NOTICE.md)。

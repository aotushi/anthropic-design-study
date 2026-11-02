# Anthropic 与 Claude 网站设计研究

**一份可直接在 GitHub 阅读的中文 UI/UX 图文手册。**

研究 Anthropic 如何用字体、色彩、留白、插画和信息结构，将公司官网、产品介绍、开发文档与课程连接成具有一致识别度的网站体系。这里的 Anthropic 指 Claude 的开发公司。

![研究总览：编辑式品牌表达、知识阅读布局与开发者风格三种方向](assets/diagrams/design-map.svg)

> **观察日期：2026-11-02 · 范围：7 个官方站点、10 个代表页面。**
> 另对 Academy 与 Claude Code 文档采集 390 × 844 的窄屏样本。研究不包含 Claude 对话界面、登录后账户页面和第三方教程站。
>
> 本项目是独立研究，没有 Anthropic 官方背书。文中的风格命名与模式数量是研究者的归纳；页面截图、字体设置和测量值有对应证据。

## 从这里开始

| 你想了解什么 | 阅读入口 |
|---|---|
| 为什么这些页面具有统一的品牌感 | [01 视觉语言](docs/01-visual-language.md) |
| 究竟用了哪些字体，分别承担什么角色 | [02 字体与排版](docs/02-typography.md) |
| 官网、定价、教程和文档的布局如何变化 | [03 八类页面模式](docs/03-page-patterns.md) |
| 哪些组成部分可以复用 | [04 二十类组件与布局模式](docs/04-components.md) |
| 页面如何帮助阅读、查找和继续学习 | [05 UX 与响应式观察](docs/05-ux-and-responsive.md) |
| 直接对照真实网页 | [06 截图图库](docs/06-gallery.md) |
| 检查来源、测量口径和限制 | [07 方法与证据](docs/07-methodology-and-sources.md) |
| 将研究转化为自己的设计 | [08 应用指南](docs/08-application-guide.md) |

## 核心发现

**它们共享一套品牌基础，但根据读者任务改变表达方式。** 官网用大标题和图像建立印象，资源中心帮助用户找到内容，文档将空间留给正文与目录，开发者博客则用像素图形和等宽文字强调技术社区的气质。

| 统计层级 | 样本归纳 | 如何理解 |
|---|---:|---|
| 整体视觉方向 | 3 类 | 温暖的编辑式表达、克制的知识界面、复古开发者表达 |
| 页面模式 | 8 类 | 公司官网、产品介绍、定价比较、资源库、技术文档、课程、帮助中心、开发者出版物 |
| 可复用模式 | 20 类 | 按任务和使用方式归并的导航、检索、展示、比较与学习组件 |
| 核心文字字体名称 | 5 个 | Anthropic Sans、Anthropic Serif、Anthropic Serif Display、Anthropic Mono、Paper Mono |
| 核心字体家族 | 4 组 | 将 Serif Display 归入 Serif 家族后的研究口径 |

这些数字不能相加：风格、页面、组件与字体描述的是不同层级。它们也不代表全站所有历史版本或全部子页面的穷尽统计。帮助中心另外声明了 JetBrains Mono；本次渲染发生回退，详情见[字体证据](docs/02-typography.md#声明加载与实际渲染)。

## 三个页面看懂差异

| 品牌与资源表达 | 知识阅读 | 开发者出版物 |
|---|---|---|
| ![Claude 资源中心，衬线大标题位于浅色网格和文章卡片之间](assets/screenshots/claude-resources.png) | ![Claude Platform 文档，左侧导航、中央正文和右侧目录并列](assets/screenshots/platform-docs.png) | ![Claude 开发者博客，等宽标签、像素图形和按行排列的文章](assets/screenshots/developer-blog.png) |
| [原站 S04](https://claude.com/resources) | [原站 S08](https://platform.claude.com/docs/en/get-started) | [原站 S10](https://claude.dev/) |

点击图片可查看原始尺寸。截图为浏览器直接采集，没有重绘或生成式修改；首屏内的内容会随网站更新而变化。

## 共同的设计基础

- **背景与文字形成温和但清晰的对比。** 多个官网样本使用接近纸张的浅色背景和接近黑色的文字；这是测量到的页面用色，不是对官方完整色板的宣称。
- **字体分工比字体数量更重要。** 衬线字体常用于标题，无衬线字体负责正文和控件，等宽字体承担代码及技术标签。Anthropic 公司首页还在同一段大标题里混合使用前两者。
- **内容密度随任务变化。** 品牌页面留白较多；文档把导航、正文和定位工具同时放到桌面视野内；课程突出学习目标和下一步。
- **装饰具有站点差异。** 资源中心有线描插画与漂浮卡片，开发者博客有像素图形。不能将局部插画、网格或圆角概括为所有页面必须采用的规则。

## 证据与维护

本手册提供三层材料：**正文中的设计解读 → 原始截图 → 页面测量记录**。每个代表页面均有原站链接和本地记录，可从[来源索引](docs/07-methodology-and-sources.md#页面来源索引)追溯。

<details>
<summary>查看仓库结构与维护方式</summary>

- `docs/`：分章节的图文手册。
- `assets/screenshots/`：未经图像编辑的网页截图。
- `assets/diagrams/`：本项目原创的解释性示意图，不是官网素材。
- `data/pages/`：页面字体、颜色、尺寸和采集环境记录。
- `data/sample-manifest.json`：样本范围。
- `scripts/`：重新采集、验证本地链接与证据的工具。

运行 `python scripts/validate.py` 检查文档链接、图片、样本记录与目录完整性。重新采集需要 Python、Playwright 和浏览器，具体步骤见[维护说明](docs/07-methodology-and-sources.md#如何更新研究)。

</details>

原创文字与示意图按 [CC BY 4.0](LICENSE) 提供。第三方网页截图、商标和字体不纳入该授权；见 [素材说明](NOTICE.md)。仓库不分发 Anthropic 字体文件。

# 07 方法与证据

**中文** · [English](en/07-methodology-and-sources.md)

[返回总览](../README.zh-CN.md) · [查看截图图库](06-gallery.md)

## 范围和时间

观察日期为 **2026-11-02，Asia/Shanghai**。样本包含 7 个官方站点上的 10 个代表页面。Academy 首页与 Claude Code 文档另采集窄屏版本；重复视口与交互状态不增加页面总数。

范围为公开的官网、产品介绍、官方教程与文档，未纳入 Claude 对话界面、登录后页面、第三方教程站及其他语言或历史版本。采集工具阻止对 `claude.ai` 的访问。

## 页面来源索引

| 编号 | 样本 | 原站 | 原始测量 |
|---|---|---|---|
| S01 | Anthropic 公司首页 | [访问](https://www.anthropic.com/) | [JSON](../data/pages/anthropic-home.json) |
| S02 | Claude 产品介绍 | [访问](https://claude.com/product/overview) | [JSON](../data/pages/claude-product.json) |
| S03 | 定价与比较 | [访问](https://claude.com/pricing) | [JSON](../data/pages/claude-pricing.json) |
| S04 | 资源中心 | [访问](https://claude.com/resources) | [JSON](../data/pages/claude-resources.json) |
| S05 | Academy 首页 | [访问](https://academy.claude.com/) | [JSON](../data/pages/academy-home.json) |
| S06 | Academy 课程内页 | [访问](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) | [JSON](../data/pages/academy-lesson.json) |
| S07 | Claude Code 文档 | [访问](https://code.claude.com/docs/en/overview) | [JSON](../data/pages/code-docs.json) |
| S08 | Claude Platform 文档 | [访问](https://platform.claude.com/docs/en/get-started) | [JSON](../data/pages/platform-docs.json) |
| S09 | 帮助中心 | [访问](https://support.claude.com/en/) | [JSON](../data/pages/support-home.json) |
| S10 | 开发者博客 | [访问](https://claude.dev/) | [JSON](../data/pages/developer-blog.json) |

截图中的页面内容、价格和产品名称保留观察日期的状态；当前信息请查阅对应原站。

## 研究口径与证据

本手册是一份基于公开页面的独立设计分析。风格命名与模式分类由本研究归纳，字体、色彩、尺寸及交互描述对应下列证据。

| 类型 | 内容 | 依据 |
|---|---|---|
| 页面事实 | 字体、颜色、结构、尺寸与操作后的状态 | 原始截图、浏览器测量、交互记录 |
| 设计解读 | 视觉形式与阅读任务之间的关系 | 对页面事实的比较与分析 |
| 应用建议 | 为其他项目选择布局、字体与交互方式 | 应用指南中基于任务提出的设计建议 |

**3 类视觉方向、8 类页面模式、20 类组件模式与字体数量分别描述不同层级，独立计数。** 分类范围为已检查的代表页面。组件按任务去重：普通卡片网格用于浏览内容，套餐卡片用于比较方案，分别计数；同一模式出现在多个站点时合并。该数量统计的是可见界面模式，不是源代码组件数量。

## 测量和采集环境

| 项目 | 口径 |
|---|---|
| 桌面 | 1440 × 1000 CSS 像素，设备像素比例 1，浅色模式 |
| 窄屏 | 390 × 844 CSS 像素，设备像素比例 1；通过桌面浏览器缩窄视口采集 |
| 页面状态 | 公开页面，无账户登录；英文内容；正常动态效果偏好 |
| 截图与示意图 | 截图由浏览器直接输出 PNG，保留原始画面；SVG 为本项目绘制的结构或色彩说明图 |
| 字体设置 | 读取元素的字体、大小、字重和行高，并记录字体声明及加载状态 |
| 字形渲染 | 读取浏览器在选定文字元素上实际使用的字体 |
| 颜色 | 读取元素的页面样式；透明背景需结合祖先背景理解 |
| 尺寸 | 记录具体页面、元素和视口下的测量值 |

字体家族会有变量版本、静态版本、大小写与连接符不同的名称。研究按可辨识的家族归并，同时保留原始名称。图标字体、备用字体和字重不混入核心文字字体数量。

## 验证范围与采集状态

| 项目 | 已检查 | 尚未验证 |
|---|---|---|
| 交互 | 定价人群、博客分类、课程文字稿的切换与状态反馈 | 购买和登录流程、视频播放、学习进度与测验、搜索结果质量；未执行代码示例 |
| 响应式 | Academy 与 Code Docs 的两组宽窄视口、正文尺寸与页面横向溢出 | 真实手机触控、其他设备与断点、全部浮层和展开状态 |
| 可访问性 | 四组文字与背景的对比度、Resources 首次键盘焦点 | 全页键盘流程、控件目标尺寸、完整状态对比度与全站 WCAG 审计 |
| 动态与效果 | 首屏动态画面、页面结构与任务的关系 | 动画时长与触发细节、降低动态效果偏好、用户效率、转化及性能实验 |

两种采集状态会影响截图解读，因此同时标注在对应章节和图注中：帮助中心的抽样文字发生系统字体回退；课程视频区域在采集时尚未显示内容，文字内容可用。字体与色值记录保留具体元素和当时的浏览器状态。

## 辅助标准

文字对比度计算参照 W3C 的 [文字对比度说明](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)：普通文字的最低值为 4.5 : 1，符合条件的大字为 3 : 1，规范另列有例外。计算使用抽样文字颜色与最近的不透明祖先背景。

如进一步检查控件，WCAG 2.2 AA 的[目标尺寸条款](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)以 24 × 24 CSS 像素为基准，并包含间距等例外。本手册的实际检查范围列于上表。

## 如何更新研究

1. 安装 Python 和 Playwright；本次使用 Playwright 1.58.0 与 Chrome。
2. 在仓库根目录运行 `python scripts/capture.py --channel chrome` 更新桌面样本。
3. 运行 `python scripts/capture.py --mobile --ids S05 S07 --channel chrome` 更新两个窄屏样本。
4. 运行 `python scripts/check-interactions.py` 重新记录本手册覆盖的交互。
5. 逐张检查截图完整性与加载状态，核对实际字体，再同步修改中英文正文。
6. 运行 `python scripts/analyze.py`、`python scripts/build_html.py`、`python scripts/validate.py` 和 `python scripts/validate_html.py`；证据变化时更新观察日期与变化记录。

更新会覆盖对应的证据文件；请在独立分支中执行。网站改版可能使采集步骤不再适用，需要先调整定位方式，再解释新结果。

HTML 版的构建与交互维护见[构建说明](../web/README.md)。

[继续：应用指南](08-application-guide.md)

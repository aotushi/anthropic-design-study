# 05 UX 与响应式观察

**中文** · [English](en/05-ux-and-responsive.md)

[返回总览](../README.zh-CN.md) · [上一章：组件](04-components.md) · [下一章：截图图库](06-gallery.md)

## 页面如何帮助用户继续行动

视觉层级和信息结构需要一起看。一个大标题能够吸引注意，但用户还需要知道下一步；一份长文内容充分，也需要有定位和返回路径。

| 使用情境 | 样本中的辅助方式 | 设计解读 |
|---|---|---|
| 初次了解产品 | 简短说明、场景、突出主要动作 | 先建立用途，再引导行动 |
| 比较方案 | 人群切换、套餐卡片、详细比较表 | 把快速判断与细节核对分层 |
| 查找技术内容 | 导航树、搜索、页内目录 | 同时支持浏览与定向定位 |
| 逐步执行 | 编号步骤、代码区、相邻复制入口 | 将说明与执行对象放在一起 |
| 顺序学习 | 学习目标、课时信息、下一课 | 为阅读提供起点与后续方向 |

## 已操作核验的交互

以下结果来自公开页面的实际操作，原始记录见 [interaction-checks.json](../data/interaction-checks.json)。

| 检查 | 本次观察结果 | 观察对象 |
|---|---|---|
| 定价的人群切换 | Individual 切换为 Team & Enterprise，显示对应套餐 | 标签选中状态与套餐标题 |
| 博客的主题筛选 | 列表由 10 项变成 1 项，恢复 ALL 后回到 10 项 | 分类选择与可见文章数量 |
| 课程的文字稿切换 | Transcript 被选中，选中状态正确更新 | 内容切换控件的选中状态 |
| 文档代码字体 | 代码文字实际由 Paper Mono 渲染 | 代码区抽样文字 |
| 资源页首次键盘焦点 | 首次 Tab 到达 Skip to main content 链接 | 跳过导航的键盘入口 |

![课程切换为文字稿后的内容区，右侧仍保留章节定位](../assets/screenshots/academy-transcript.png)

*图 10 · [课程 S06](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) · 顶部视频区域在采集时为空白加载状态，文字稿切换与下方文字可用。*

在这节课程中，视频与文字提供了两种学习方式。视频资源尚未就绪时，文字内容与章节目录仍然可用。

## 桌面与窄屏对照

<table>
<tr><th>Academy：390 × 844</th><th>Code Docs：390 × 844</th></tr>
<tr>
<td><img src="../assets/screenshots/academy-home-mobile.png" width="390" alt="Academy 窄屏首页，标题换行，导航收缩，学习入口改成单列"></td>
<td><img src="../assets/screenshots/code-docs-mobile.png" width="390" alt="Code Docs 窄屏，侧边导航收进菜单，正文占据主要宽度"></td>
</tr>
</table>

*图 11–12 · 两页均在桌面浏览器中以 390 × 844 视口采集。*

| 观察点 | 桌面 1440px 宽 | 窄屏 390px 宽 |
|---|---|---|
| Academy 主标题 | 48px，行高 52.8px | 44px，行高 48.4px；标题分行 |
| Academy 首页说明 | 18px，行高 28px | 保持 18px、28px |
| Academy 内容入口 | 多列卡片 | 纵向单列，局部图文关系调整 |
| Code Docs 主标题 | 36px，行高 40px | 30px，行高 36px |
| Code Docs 介绍段落 | 16px，行高 26.4px | 保持 16px、26.4px |
| Code Docs 导航 | 左侧导航、中央正文、右侧目录 | 主阅读区单列，导航以紧凑入口呈现 |
| 整个文档的横向溢出 | 两个样本均未检测到 | 两个样本均未检测到 |

来源：[Academy 桌面](../data/pages/academy-home.json)、[Academy 窄屏](../data/pages/academy-home-mobile.json)、[Code Docs 桌面](../data/pages/code-docs.json)、[Code Docs 窄屏](../data/pages/code-docs-mobile.json)。

窄屏布局通过**重新分配空间**适应阅读：部分标题缩小，正文保持字号，导航收进紧凑入口，卡片转为单列。内容的优先顺序因此比桌面布局的原始比例更重要。

## 四组文字对比度检查

以选定文字颜色和最近的不透明祖先背景进行计算，结果如下。资源中心首屏文字位于 `#F5F4ED` 面板上，外层页面背景则为 `#FAF9F5`；对比度使用文字所在面板的颜色。

| 抽样位置 | 文字 | 背景 | 对比度，约 |
|---|---|---|---:|
| Resources 标题 | #141413 | #F5F4ED | 16.72 : 1 |
| Resources 首屏说明 | #30302E | #F5F4ED | 11.99 : 1 |
| Platform 标题 | #0B0B0B | #FCFCFB | 19.17 : 1 |
| Platform 首屏说明 | #52514E | #FCFCFB | 7.73 : 1 |

W3C 对普通文字的最低对比度要求为 4.5 : 1，符合条件的大字为 3 : 1；存在规范规定的例外。[W3C 对比度说明](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

上述四组均高于普通文字阈值。两页通过深色标题与稍浅的说明文字建立层级，同时让说明文字保持较高对比度。[计算数据](../data/derived-checks.json) · [计算脚本](../scripts/analyze.py)

## 将观察转化为设计判断

| 设计要点 | 页面中的具体做法 | 应用时关注什么 |
|---|---|---|
| 状态与内容对应 | 定价标签切换时更新对应套餐 | 选中样式和当前内容保持一致 |
| 学习方式可选择 | 课程提供文字稿入口 | 让替代内容与主内容一样容易找到 |
| 窄屏保留阅读优先级 | 正文字号保持，导航收起，卡片变为单列 | 先安排内容顺序，再调整尺寸 |
| 键盘入口贴近主要任务 | Resources 首次焦点是跳过导航链接 | 让键盘用户能迅速进入主体内容 |
| 层级与清晰度并存 | 说明文字比标题稍浅，仍保持较高对比度 | 同时检查信息层级和阅读清晰度 |

[下一章：截图图库](06-gallery.md)

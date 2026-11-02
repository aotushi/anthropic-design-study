# 03 八类页面模式

[返回总览](../README.md) · [上一章：字体与排版](02-typography.md) · [下一章：组件](04-components.md)

## 为什么按任务归类

不同域名的文档可以采用相近的结构，同一个 Claude 官网也同时包含产品、定价和资源页面。本章按读者的主要任务归纳八类页面，观察它们怎样分配内容与操作入口。

![布局示意：展示、阅读和开发者列表的空间分配](../assets/diagrams/layout-archetypes.svg)

*结构示意：展示页、阅读页与文章列表采用不同的空间分配。*

## 总体对照

| 类型 | 用户的主要问题 | 页面结构 | 代表样本 |
|---|---|---|---|
| 1 公司与品牌官网 | 这家公司关注什么 | 主张、重点内容、文章入口、公司导航 | [S01](https://www.anthropic.com/) |
| 2 产品介绍 | 产品能帮我做什么 | 标题与动作、使用场景、能力说明、常见问题 | [S02](https://claude.com/product/overview) |
| 3 定价比较 | 哪种方案适合我 | 人群切换、套餐卡片、功能比较、说明 | [S03](https://claude.com/pricing) |
| 4 内容资源库 | 我需要的内容在哪里 | 内容分类、搜索、筛选、卡片与专题分组 | [S04](https://claude.com/resources) |
| 5 技术文档 | 怎样完成具体技术任务 | 导航树、正文、页内目录、步骤和代码 | [S07](https://code.claude.com/docs/en/overview)、[S08](https://platform.claude.com/docs/en/get-started) |
| 6 课程学习 | 学什么，如何继续 | 学习入口、目标、课时、章节、视频和文字 | [S05](https://academy.claude.com/)、[S06](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) |
| 7 帮助知识库 | 如何解决当前问题 | 搜索、问题分类、热门文章、文章集合 | [S09](https://support.claude.com/en/) |
| 8 开发者出版物 | 有什么新经验值得阅读 | 类别、日期、作者、阅读时间、文章行列表 | [S10](https://claude.dev/) |

## 1 公司与品牌官网

Anthropic 首页的主张区采用混合字形的大段文字，随后展示重点内容与文章入口。它首先解释公司的关注点，再引导读者进入具体内容。

**设计解读：** 大段主张建立叙事起点，重点内容与文章入口继续展开公司的关注领域，形成由整体印象进入具体话题的阅读顺序。

## 2 产品介绍

产品页将主题、主要动作和场景演示放在显著位置，再逐步展开能力与使用方式。任务示例把产品说明连接到具体的使用情境。

![Claude 产品介绍首屏的主标题与场景图像](../assets/screenshots/claude-product.png)

*图 5 · [S02](https://claude.com/product/overview) · 首屏包含动态内容，截图保留采集时刻的状态。*

**设计解读：** 标题概括用途，场景演示呈现任务与成果，主要动作提供继续了解或开始使用的入口。三者共同组织了产品介绍的首屏。

## 3 定价比较

![定价页的人群切换与 Team、Enterprise 套餐卡片](../assets/screenshots/pricing-team.png)

*图 6 · [S03](https://claude.com/pricing) · 切换到 Team & Enterprise 后，对应套餐并列呈现。*

定价页先让读者选择 Individual、Team & Enterprise 或 API，再展示对应内容。套餐卡片支持快速判断，功能表支持逐项比较。这两个层次回答的是不同问题，因此同时存在。

选择人群后，标签的选中状态与套餐内容一同更新，使比较范围和当前选择保持对应。[交互记录](../data/interaction-checks.json)

## 4 内容资源库

资源中心包含首页、文章、指南、网络研讨会和视频等分类入口，使用搜索和筛选缩小范围。卡片上的类型、日期或阅读信息帮助用户在进入全文前判断是否相关。

**设计解读：** 资源库同时面向“随便看看”和“带问题来找内容”的读者。丰富的首屏提供探索入口，分类、搜索与列表支持定向检索。

## 5 技术文档

![Claude Platform 文档，左侧导航树、中央步骤与代码、右侧页内目录](../assets/screenshots/platform-docs.png)

*图 7 · [S08](https://platform.claude.com/docs/en/get-started)。*

桌面布局将三个问题同时呈现：

- 左侧导航回答“我在整个文档体系的哪里”。
- 中央正文回答“这个任务如何完成”。
- 右侧目录回答“当前文章有哪些部分”。

Code Docs 与 Platform Docs 都采用这类阅读结构，字体与代码区则各有细节：前者的代码使用 Paper Mono，后者使用 Anthropic Mono。相同的空间分工可以容纳不同的视觉表达。

## 6 课程学习

Academy 首页帮助选择学习方向，课程内页提供目标、课时、视频、总结或文字稿、练习和后续内容。与技术文档相比，它更强调学习顺序和阶段目标。

![Academy 课程内页，目标框与章节定位清晰分离](../assets/screenshots/academy-lesson.png)

*图 8 · [S06](https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency) · 采集时视频区域尚未显示内容，学习目标、正文与目录可见。*

学习目标说明本课要掌握什么，课时帮助判断投入，章节和后续链接标示阅读顺序。文字稿提供另一种学习入口，其切换状态见 [UX 观察](05-ux-and-responsive.md#已操作核验的交互)。

## 7 帮助知识库

帮助中心把搜索与主题集合放在显著位置，同时列出常见问题。与课程的顺序学习相比，它支持直接进入一个待解决的问题。

**设计解读：** 搜索接收具体问题，主题集合帮助浏览，常见问题提供直接入口。这三种路径适应不同程度的问题描述。

## 8 开发者出版物

开发者博客用文章行呈现标题、日期和阅读时间，配合类别筛选与像素图形。与资源中心的大量卡片相比，列表更突出连续扫描和快速比较。

选择 TUTORIALS 后，列表缩小到对应文章；切回 ALL 后，完整列表恢复。分类控件与文章行紧密配合，形成“选择主题—扫描标题—进入文章”的路径。[交互记录](../data/interaction-checks.json)

[下一章：二十类组件与布局模式](04-components.md)

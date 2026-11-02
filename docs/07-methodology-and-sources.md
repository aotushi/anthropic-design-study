# 07 方法与证据

[返回总览](../README.md) · [查看截图图库](06-gallery.md)

## 范围和时间

观察日期为 **2026-11-02，Asia/Shanghai**。样本包含 7 个官方站点上的 10 个代表页面。Academy 首页与 Claude Code 文档另采集窄屏版本；重复视口与交互状态不增加页面总数。

未纳入 Claude 对话界面、需要登录的控制台和账户页面、第三方教程网站、所有地区语言版本或历史版本。访问官方站点中的下载、登录、购买入口不是本研究的测试步骤；采集工具阻止对 `claude.ai` 的访问。

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

页面文字、价格、产品名称和发布内容可能随时间变化。本研究分析页面表达方式，不将截图里的套餐价格或产品版本作为持续有效的产品信息。

## 三种证据如何区分

| 类型 | 本文的表达方式 | 能够支持什么 |
|---|---|---|
| 页面事实 | “页面使用”“测得”“可见” | 截图、字体设置、颜色、结构、已操作的状态变化 |
| 设计解读 | “可理解为”“有助于”“研究归纳” | 对形式与阅读任务之间关系的解释 |
| 应用建议 | 在应用指南中明确给出 | 如何为其他项目做取舍，不代表原团队意图 |

风格、页面与组件的分类是研究者建立的观察框架。组件按用途去重，而不是按代码中的组件文件计数。例如普通卡片网格和套餐卡片承担不同任务，因此分属不同模式。8 类页面模式与 20 类组件模式不能用来推算实际代码量。

## 测量和采集环境

| 项目 | 口径 |
|---|---|
| 桌面 | 1440 × 1000 CSS 像素，设备像素比例 1，浅色模式 |
| 窄屏 | 390 × 844 CSS 像素，设备像素比例 1；桌面浏览器缩窄视口，不等于真实手机测试 |
| 页面状态 | 公开页面，无账户登录；英文内容；正常动态效果偏好 |
| 截图 | 浏览器直接输出 PNG，没有生成式重绘、修图或拼接 |
| 字体设置 | 读取元素的字体、大小、字重和行高，并记录字体声明及加载状态 |
| 字形渲染 | 额外读取浏览器在选定元素上实际使用的字体；不宣称逐字覆盖全站 |
| 颜色 | 读取元素的页面样式；透明背景需结合祖先背景理解 |
| 尺寸 | 本次视口中的测量值，不视为全局设计规范 |

字体家族会有变量版本、静态版本、大小写与连接符不同的名称。研究按可辨识的家族归并，同时保留原始名称。图标字体、备用字体和字重不混入核心文字字体数量。

## 已知限制

- **帮助中心出现字体回退。** 本次浏览器在抽样文字上实际使用 Times New Roman 和 Consolas。页面仍声明 Anthropic 字体和局部 JetBrains Mono，因此截图可分析布局，但不能代表它们成功加载时的字形效果。
- 课程视频及其他外部资源可能延迟加载。静态截图中的播放器占位不代表网站设计了永久空白；相关图片会在图注中说明。
- 对比度计算只检验明确列出的文字与背景组合；没有进行全站 WCAG 合规审计。
- 两个窄屏样本不能代表所有设备、所有断点或所有移动交互。
- 没有真实用户研究、转化实验或性能基准，因此不声称某种视觉选择必然提高效率、信任或转化。
- 动画只做可见观察，没有对其时长、曲线和触发点进行完整测量。

## 辅助标准

可访问性判断仅参照 W3C 的 [文字对比度说明](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) 与 [目标尺寸说明](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)。规范阈值与网站的实际检查结果分开呈现。

## 如何更新研究

1. 安装 Python 和 Playwright；本次使用 Playwright 1.58.0 与 Chrome。
2. 在仓库根目录运行 `python scripts/capture.py --channel chrome` 更新桌面样本。
3. 运行 `python scripts/capture.py --mobile --ids S05 S07 --channel chrome` 更新两个窄屏样本。
4. 运行 `python scripts/check-interactions.py` 重新记录本手册覆盖的交互。
5. 检查每张截图的完整性，核对字体是否加载，再修改对应正文。采集脚本生成文件不等于图文已经人工核验。
6. 运行 `python scripts/validate.py` 检查结构和引用；最后更新观察日期与变化记录。

更新会覆盖对应的证据文件；请在独立分支中执行。网站改版可能使采集步骤不再适用，需要先调整定位方式，再解释新结果。

[继续：应用指南](08-application-guide.md)

"""Build both static reading editions from the Markdown and recorded evidence."""
import html
import json
import os
import re
import struct
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "html"
CONTENT = json.loads((ROOT / "web/content.json").read_text(encoding="utf-8"))
CHAPTERS = CONTENT["chapters"]
MANIFEST = json.loads((ROOT / "data/sample-manifest.json").read_text(encoding="utf-8"))
TAXONOMY = json.loads((ROOT / "data/taxonomy.json").read_text(encoding="utf-8"))
REPO = "https://github.com/aotushi/anthropic-design-study"
DATE = MANIFEST["observedDate"]

COPY = {
    "en": {
        "title": "Anthropic & Claude Design Study", "home": "Overview", "explore": "Explore the evidence",
        "study": "Design study", "handbook": "Handbook", "compareNav": "Compare", "sourcesNav": "Sources",
        "start": "Start here", "navGroups": ["Design foundations", "Patterns & experience", "Study resources", "Page analysis"],
        "copyPage": "Copy page", "pageCopied": "Page copied", "pageCopyFailed": "Could not copy. Open the Markdown source instead.",
        "viewSource": "View Markdown", "sectionLink": "Link to this section", "findings": "At a glance",
        "scope": "Seven official sites, ten representative pages, and two additional narrow-screen samples.",
        "chapters": "The chapters", "contents": "On this page", "search": "Search the study", "searchHint": "Fonts, layouts, patterns…",
        "searchHelp": "Search all ten chapters in this edition.", "noResults": "No results. Try a font, page type, or pattern name.",
        "results": "results", "close": "Close", "menu": "Chapters", "skip": "Skip to content", "print": "Print",
        "enlarge": "Enlarge image", "original": "Open original image", "previous": "Previous", "next": "Next",
        "source": "Source", "record": "Measurements", "date": "Observed", "all": "All patterns", "patterns": "patterns",
        "read": "Start reading", "heroTitle": "Anthropic & Claude website design",
        "heroText": "A visual study of how Anthropic and Claude use type, space, and structure across company pages, product stories, documentation, and courses.",
        "heroCaption": "S04 / Resources — a heading, a search, a world of content.",
        "voices": "Three visual directions", "voicesIntro": "Follow the same brand from editorial storytelling to focused reading and developer culture.",
        "chapterIntro": "Read in order, or follow the question that brought you here.",
        "counts": ["official sites", "sample pages", "page patterns", "component patterns", "principal fonts"],
        "directions": ["Warm editorial", "Focused knowledge", "Retro developer"],
        "directionText": ["Serif headings, paper tones, and illustrated content create an editorial rhythm.", "Stable navigation, compact controls, and clear text make room for the task.", "Monospace details, pixel imagery, and article rows establish a distinct voice."],
        "compare": "Put two pages side by side", "compareIntro": "Choose from the ten recorded pages. Compare their task, typography, and use of space.",
        "left": "First page", "right": "Second page", "task": "Reader’s task", "structure": "Spatial structure", "fonts": "Recorded fonts",
        "typeChart": "The heading changes with the task", "typeIntro": "Seven measured main headings at a 1440 × 1000 desktop viewport. Bar lengths represent CSS font size.",
        "catalog": "Twenty patterns, five jobs", "catalogIntro": "Filter the recorded patterns by the task they support. Source labels link to the sampled pages.",
        "groups": ["Navigation", "Retrieval & switching", "Presentation", "Comparison & steps", "Learning & reading"],
        "about": "About this study", "aboutText": "10 chapters · Chinese & English",
        "footer": "An illustrated study of public websites.", "methods": "Methods & sources", "download": "Download for offline reading",
        "colorTitle": "A small palette, distinct roles", "colorText": "Measured page backgrounds and text colors. Select a swatch to copy its value.", "copied": "Copied", "copyFailed": "Select and copy the color value.",
        "colorNames": ["Site background", "Site text", "Resource description", "Docs background", "Docs text", "Docs description"],
    },
    "zh": {
        "title": "Anthropic 与 Claude · 网站设计手册", "home": "研究总览", "explore": "图像与数据",
        "study": "设计研究", "handbook": "设计手册", "compareNav": "对照研究", "sourcesNav": "来源",
        "start": "开始阅读", "navGroups": ["设计基础", "模式与体验", "研究资料", "页面分析"],
        "copyPage": "复制页面", "pageCopied": "页面已复制", "pageCopyFailed": "复制未成功，可打开 Markdown 源文档。",
        "viewSource": "查看 Markdown", "sectionLink": "链接到本节", "findings": "研究概览",
        "scope": "七个官方站点、十个代表页面，以及两个补充窄屏样本。",
        "chapters": "章节目录", "contents": "本页内容", "search": "搜索研究内容", "searchHint": "字体、布局、设计模式…",
        "searchHelp": "搜索本语言版本的全部十个章节。", "noResults": "没有找到结果。试试字体、页面类型或模式名称。",
        "results": "条结果", "close": "关闭", "menu": "目录", "skip": "跳至正文", "print": "打印",
        "enlarge": "放大图片", "original": "打开原始图片", "previous": "上一章", "next": "下一章",
        "source": "原站", "record": "测量记录", "date": "观察日期", "all": "全部模式", "patterns": "种模式",
        "read": "开始阅读", "heroTitle": "Anthropic 与 Claude 网站设计",
        "heroText": "从公司官网、产品介绍到技术文档与课程，观察 Anthropic 与 Claude 如何用字体、空间和信息结构安排每一次阅读。",
        "heroCaption": "S04 / 资源中心：从标题、搜索进入丰富的内容。",
        "voices": "三种视觉表达", "voicesIntro": "沿着编辑式叙事、知识阅读与开发者文化，理解品牌怎样随任务变化。",
        "chapterIntro": "按顺序阅读，或从你关心的问题开始。",
        "counts": ["个官方站点", "个代表页面", "类页面模式", "类组件模式", "个主要字体名称"],
        "directions": ["温暖的编辑式表达", "克制的知识界面", "复古开发者表达"],
        "directionText": ["衬线标题、纸张底色与图文编排，形成接近出版物的节奏。", "稳定导航、紧凑控件和清晰文字，把空间交给当前任务。", "等宽标签、像素图形与文章行，为技术内容建立独特语气。"],
        "compare": "把两个页面放在一起看", "compareIntro": "从十个代表页面中选择，对照它们的阅读任务、字体与空间组织。",
        "left": "第一个页面", "right": "第二个页面", "task": "读者任务", "structure": "空间组织", "fonts": "记录字体",
        "typeChart": "标题比例随任务变化", "typeIntro": "七个主标题在 1440 × 1000 桌面视口下的实测字号，条形长度表示 CSS 像素值。",
        "catalog": "二十种模式，五类任务", "catalogIntro": "按任务筛选已记录的模式，来源编号链接到对应样本。",
        "groups": ["导航", "检索与切换", "内容展示", "比较与步骤", "学习与阅读"],
        "about": "关于本研究", "aboutText": "10 个章节 · 中英文双语",
        "footer": "一份关于公开网站的图文设计研究。", "methods": "方法与来源", "download": "下载离线阅读",
        "colorTitle": "少量色彩，清晰分工", "colorText": "页面背景与文字的实测色值。选择色块可复制对应值。", "copied": "已复制", "copyFailed": "请选中色值并复制。",
        "colorNames": ["官网背景", "官网文字", "资源说明", "文档背景", "文档文字", "文档说明"],
    },
}

ACADEMY_COPY = json.loads((ROOT / 'web/academy.json').read_text(encoding='utf-8'))
for language, values in ACADEMY_COPY.items():
    COPY[language].update(values)


def esc(value):
    return html.escape(str(value), quote=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def relative(path, origin):
    return Path(os.path.relpath(path, origin.parent)).as_posix()


def source_file(lang, chapter):
    return ROOT / "docs" / ("en" if lang == "en" else "") / (chapter["slug"] + ".md")


def html_file(lang, slug):
    return OUT / lang / (slug + ".html")


MAPPING = {
    (ROOT / "README.md").resolve(): html_file("en", "index"),
    (ROOT / "README.en.md").resolve(): html_file("en", "index"),
    (ROOT / "README.zh-CN.md").resolve(): html_file("zh", "index"),
}
for language in COPY:
    for chapter in CHAPTERS:
        MAPPING[source_file(language, chapter).resolve()] = html_file(language, chapter["slug"])


def rewrite_url(url, source, destination):
    parsed = urlsplit(html.unescape(url))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return html.unescape(url)
    target = (source.parent / unquote(parsed.path)).resolve()
    result = relative(MAPPING.get(target, target), destination)
    if parsed.query:
        result += "?" + parsed.query
    if parsed.fragment:
        result += "#" + parsed.fragment
    return result


def image_dimensions(path):
    if path.suffix == ".png":
        return struct.unpack(">II", path.read_bytes()[16:24])
    if path.suffix == ".svg":
        node = ET.parse(path).getroot()
        return int(node.get("width")), int(node.get("height"))
    return 1440, 1000


def figure(src, alt, lang, width=1440, height=1000, eager=False):
    label = COPY[lang]["enlarge"]
    return (f'<button class="figure-button" type="button" data-zoom aria-label="{esc(label + ": " + alt)}">'
            f'<img src="{esc(src)}" alt="{esc(alt)}" width="{width}" height="{height}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">'
            f'<span class="zoom-hint" aria-hidden="true">{esc(label)} ↗</span></button>')


def strip_markup(value):
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", value)
    return re.sub(r"\s+", " ", html.unescape(value.replace("*", "").replace("`", ""))).strip()


def render_chapter(lang, chapter):
    source = source_file(lang, chapter)
    destination = html_file(lang, chapter["slug"])
    lines = source.read_text(encoding="utf-8").splitlines()
    lines.pop(0)
    while lines and (not lines[0].strip() or lines[0].startswith(("[返回总览]", "[Overview]", "**中文**", "[中文]"))):
        lines.pop(0)
    while lines and (not lines[-1].strip() or lines[-1].startswith(("[下一章", "[继续", "[Next:", "[Continue:"))):
        lines.pop()
    markdown = "\n".join(lines)
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    tokens = md.parse(markdown)
    seen = Counter()
    headings = []
    search = []
    positions = []
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            title = strip_markup(tokens[i + 1].content)
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            number = seen[slug]
            seen[slug] += 1
            anchor = slug + (f"-{number}" if number else "")
            token.attrSet("id", anchor)
            headings.append((token.tag, title, anchor))
            positions.append((i, title, anchor))
    for pos, (i, title, anchor) in enumerate(positions):
        end = positions[pos + 1][0] if pos + 1 < len(positions) else len(tokens)
        section_text = " ".join(t.content for t in tokens[i + 3:end] if t.type in {"inline", "html_block", "fence"})
        search.append({"title": title, "chapter": chapter[lang], "href": chapter["slug"] + ".html#" + anchor,
                       "text": strip_markup(section_text)})
    rendered = md.renderer.render(tokens, md.options, {})
    rendered = re.sub(r'(href|src)="([^"]*)"', lambda m: m[1] + '="' + esc(rewrite_url(m[2], source, destination)) + '"', rendered)

    def enhance_image(match):
        tag = match[0]
        src = html.unescape(re.search(r'src="([^"]*)"', tag)[1])
        alt = html.unescape(re.search(r'alt="([^"]*)"', tag)[1])
        path = (destination.parent / unquote(urlsplit(src).path)).resolve()
        width, height = image_dimensions(path)
        enhanced = figure(src, alt, lang, width, height)
        display_width = re.search(r'\bwidth="(\d+)"', tag)
        if display_width:
            enhanced = enhanced.replace('class="figure-button"', f'class="figure-button" style="max-width: {int(display_width[1])}px"', 1)
        return enhanced

    rendered = re.sub(r"<img\b[^>]*>", enhance_image, rendered)
    def heading_link(match):
        tag, anchor, text = match.groups()
        label = COPY[lang]["sectionLink"] + ': ' + strip_markup(text)
        return f'<{tag} id="{anchor}">{text}<a class="heading-anchor" href="#{anchor}" aria-label="{esc(label)}">#</a></{tag}>'
    rendered = re.sub(r'<(h[23]) id="([^"]+)">(.*?)</\1>', heading_link, rendered, flags=re.DOTALL)
    label = "Scrollable data table" if lang == "en" else "可横向滚动的数据表"
    rendered = rendered.replace("<table>", f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}"><table>')
    rendered = rendered.replace("</table>", "</table></div>")
    return rendered, headings, search


def nav_link(slug, title, current, number=""):
    active = ' aria-current="page"' if current == slug else ""
    num = f'<span class="nav-number">{number}</span>' if number else ""
    return f'<a href="{slug}.html"{active}>{num}<span>{esc(title)}</span></a>'


NAV_GROUPS = [CHAPTERS[:2], CHAPTERS[2:5], CHAPTERS[5:8], CHAPTERS[8:]]
TOPICS = ['foundations', 'experience', 'research']


def chapter_topic(chapter):
    index = CHAPTERS.index(chapter)
    return 0 if index < 2 else 1 if index < 5 else 2


def topic_art(topic):
    backgrounds = ['#edcdbd', '#c5d7d0', '#cfccdf']
    drawings = [
        '<path d="M116 118h91M118 61v61M204 61v61" opacity=".4"/><text x="126" y="112" font-family="Georgia,serif" font-size="59" fill="#25241f" stroke="none">Aa</text><path d="m111 66 7-6 7 6m72 50 7 6 7-6"/>',
        '<rect x="104" y="53" width="112" height="78" rx="5" fill="#fcfcf8"/><path d="M104 70h112M134 70v61M144 83h59M144 92h38M113 82h13M113 91h13M113 100h13"/><rect x="144" y="105" width="24" height="16" rx="2"/><rect x="177" y="105" width="26" height="16" rx="2"/><circle cx="113" cy="62" r="1"/><circle cx="121" cy="62" r="1"/>',
        '<rect x="110" y="48" width="75" height="88" rx="5" fill="#fcfcf8"/><path d="M124 65h46M124 75h35M124 116h29"/><circle cx="181" cy="102" r="24" fill="#e4dfef"/><path d="m199 121 17 18M167 106l10-11 8 5 9-14"/><circle cx="177" cy="95" r="2" fill="#25241f"/>'
    ]
    return f'<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="320" height="180" fill="{backgrounds[topic]}"/><path d="m161 27 44 13 26 38-8 43-34 29-47 2-39-27-11-43 22-38Z" fill="#ffffff70"/><g fill="none" stroke="#25241f" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{drawings[topic]}</g></svg>'


def article_header(lang, title, summary, section, copy_page=False):
    copy = COPY[lang]
    control = ''
    if copy_page:
        control = f'<button class="copy-page" type="button" data-copy-page><svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2"/><path d="M12 7V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h3"/></svg><span>{copy["copyPage"]}</span></button>'
    return f'<header class="article-header"><div class="breadcrumb"><a href="index.html">{copy["handbook"]}</a><span aria-hidden="true">›</span><span>{esc(section)}</span></div><div class="page-title-row"><h1>{esc(title)}</h1>{control}</div><p class="page-description">{esc(summary)}</p><p id="page-copy-status" class="sr-only" role="status"></p></header>'


def shell(lang, slug, title, content, headings=(), chapter=None):
    copy = COPY[lang]
    other = "zh" if lang == "en" else "en"
    chapter_nav = "".join('<div class="nav-group"><p class="nav-label">' + copy["navGroups"][i] + '</p>' + ''.join(nav_link(c["slug"], c[lang], slug, f'{CHAPTERS.index(c) + 1:02}') for c in group) + '</div>' for i, group in enumerate(NAV_GROUPS))
    toc_links = "".join(f'<a class="toc-{tag}" href="#{esc(anchor)}">{esc(text)}</a>' for tag, text, anchor in headings)
    chapter_switcher = ''
    if chapter:
        switch_links = ''.join(nav_link(c['slug'], c[lang], slug, f'{i+1:02}') for i,c in enumerate(CHAPTERS))
        chapter_switcher = f'<details class="chapter-switcher"><summary><span><small>{copy["chapterWord"]} {CHAPTERS.index(chapter)+1} / 10</small><strong>{esc(chapter[lang])}</strong></span><span aria-hidden="true">⌄</span></summary><nav class="nav-group" aria-label="{copy["chooseChapter"]}">{switch_links}</nav></details>'
    toc = f'<aside class="page-toc">{chapter_switcher}<nav class="section-toc" aria-label="{copy["contents"]}"><p class="toc-label">{copy["contents"]}</p>{toc_links}</nav></aside>' if headings else ""
    if headings:
        section_links = "".join(f'<a href="#{esc(anchor)}">{esc(text)}</a>' for tag, text, anchor in headings if tag == "h2")
        inline_toc = f'<details class="inline-toc"><summary>{copy["contents"]}</summary><div>{section_links}</div></details>'
        content = content.replace('</header>', '</header>' + inline_toc, 1)
    body_class = "chapter-page" if chapter else "academy-home" if slug == "index" else "overview-page"
    lang_label = "中文" if other == "zh" else "English"
    pager = ""
    if chapter:
        index = CHAPTERS.index(chapter)
        items = []
        for offset, label in [(-1, copy["previous"]), (1, copy["next"])]:
            neighbor = index + offset
            if 0 <= neighbor < len(CHAPTERS):
                target = CHAPTERS[neighbor]
                items.append(f'<a href="{target["slug"]}.html"><small>{label}</small><span>{esc(target[lang])} {"→" if offset == 1 else ""}</span></a>')
            else:
                items.append(f'<a href="index.html"><small>{label}</small><span>{copy["home"]}</span></a>')
        pager = '<nav class="chapter-pager" aria-label="Chapter navigation">' + "".join(items) + "</nav>"
    js_copy = json.dumps({k: copy[k] for k in ["noResults", "results", "patterns", "copied", "copyFailed", "enlarge", "copyPage", "pageCopied", "pageCopyFailed", "viewSource", "darkTheme", "lightTheme", "chapterUnit", "chapterUnitSingular"]}, ensure_ascii=False).replace("<", "\\u003c")
    page_source = ''
    if chapter:
        markdown = json.dumps(source_file(lang, chapter).read_text(encoding='utf-8'), ensure_ascii=False).replace('<', '\\u003c')
        page_source = f'<script id="page-source" type="application/json">{markdown}</script>'
    menu_groups = ''.join(f'<div><p>{esc(copy["topicLabels"][i])}</p>' + ''.join(f'<a href="{c["slug"]}.html">{esc(c[lang])}</a>' for c in CHAPTERS if chapter_topic(c)==i) + '</div>' for i in range(3))
    resource_links = ''.join(f'<a href="{target}.html">{esc(label)}</a>' for target,label in [('index',copy['home']),('explore',copy['explore']),('06-gallery',CHAPTERS[5][lang]),('07-methodology-and-sources',copy['methods'])])
    primary_nav = f'<details class="header-disclosure"><summary>{copy["browseMenu"]}<span aria-hidden="true">⌄</span></summary><div class="nav-popover mega-menu">{menu_groups}</div></details><details class="header-disclosure"><summary>{copy["resourcesMenu"]}<span aria-hidden="true">⌄</span></summary><div class="nav-popover resource-menu">{resource_links}</div></details>'
    description = chapter["summary"][lang] if chapter else copy["heroText"]
    return f'''<!doctype html>
<html lang="{"zh-CN" if lang == "zh" else "en"}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light dark">
<title>{esc(title)} · {esc(copy["title"])}</title>
<link rel="icon" type="image/svg+xml" href="../shared/favicon.svg">
<link rel="stylesheet" href="../shared/style.css">
<link rel="stylesheet" href="../shared/academy.css">
<link rel="alternate" hreflang="{other}" href="../{other}/{slug}.html">
<script>document.documentElement.classList.add('js');window.STUDY_COPY={js_copy};try{{let theme=localStorage.getItem('anthropic-study-theme');document.documentElement.dataset.theme=theme==='dark'||theme==='light'?theme:matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';}}catch{{document.documentElement.dataset.theme='light';}}</script>
{page_source}
<script src="../shared/search-{lang}.js" defer></script><script src="../shared/app.js" defer></script><script src="../shared/academy.js" defer></script>
</head><body class="{body_class}" data-language="{lang}">
<a class="skip-link" href="#main">{copy["skip"]}</a>
<header class="site-header">
<a class="brand" href="index.html"><span class="brand-name">Anthropic</span><span class="brand-context">{copy["study"]}</span></a>
<nav class="top-nav" aria-label="{copy["study"]}">{primary_nav}</nav>
<div class="header-actions"><button class="menu-toggle" type="button" aria-label="{copy["menu"]}" aria-controls="chapter-nav" aria-expanded="false"><svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14"/></svg><span>{copy["menu"]}</span></button>
<button class="search-trigger" type="button" aria-label="{copy["search"]}" data-open-search><svg class="search-icon" width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5"/><path d="m13 13 4 4"/></svg><span>{copy["search"]}</span><kbd>Ctrl K</kbd></button>
<a class="language-switch" lang="{"zh-CN" if other == "zh" else "en"}" href="../{other}/{slug}.html">{lang_label}</a>
<button class="theme-toggle" type="button" data-theme-toggle aria-label="{copy["darkTheme"]}" title="{copy["darkTheme"]}"><svg class="moon-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M20 15.5A8.7 8.7 0 0 1 8.5 4 8.8 8.8 0 1 0 20 15.5Z"/></svg><svg class="sun-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2"/></svg></button>
<a class="github-link" href="{REPO}">GitHub ↗</a></div>
</header>
<nav id="chapter-nav" class="chapter-nav" aria-label="{copy["chapters"]}">
<div class="nav-group"><p class="nav-label">{copy["start"]}</p>{nav_link("index",copy["home"],slug)}{nav_link("explore",copy["explore"],slug)}</div>
{chapter_nav}
<div class="nav-foot"><p>{copy["aboutText"]}</p><a href="{REPO}/archive/refs/heads/main.zip">{copy["download"]} ↗</a></div></nav>
<div class="nav-scrim" data-close-menu></div>
<div class="site-body"><div class="document-grid"><main id="main" tabindex="-1">{content}{pager}</main>{toc}</div>
<footer class="site-footer"><p>{copy["footer"]}<br><span>{copy["date"]}: {DATE}</span></p><div><a href="07-methodology-and-sources.html">{copy["methods"]}</a><button type="button" data-print>{copy["print"]} ↗</button><a href="../../NOTICE.md">CC BY 4.0 / Credits</a></div></footer></div>
<dialog id="search-dialog" class="search-dialog" aria-labelledby="search-title"><div class="dialog-head"><h2 id="search-title">{copy["search"]}</h2><button type="button" data-close-dialog>{copy["close"]} <kbd>Esc</kbd></button></div><label class="sr-only" for="study-search">{copy["search"]}</label><input id="study-search" type="search" placeholder="{copy["searchHint"]}" autocomplete="off"><p id="search-status" class="search-status" role="status">{copy["searchHelp"]}</p><div id="search-results"></div></dialog>
<dialog id="image-dialog" class="image-dialog" aria-label="{copy["enlarge"]}"><div class="dialog-head"><p id="image-caption"></p><button type="button" data-close-dialog>{copy["close"]} <kbd>Esc</kbd></button></div><div class="image-canvas"><img id="enlarged-image" alt=""></div><a id="original-image" href="#" target="_blank" rel="noopener">{copy["original"]} ↗</a></dialog>
<noscript><p class="no-script">{"All chapters and images are readable without JavaScript. Enable it for search, filtering, and image enlargement." if lang == "en" else "全部章节与图片可直接阅读。启用 JavaScript 后可使用搜索、筛选与图片放大。"}</p></noscript>
</body></html>'''


def home(lang):
    copy = COPY[lang]
    stats = "".join(f'<div><strong>{number}</strong><span>{esc(label)}</span></div>' for number, label in zip([7, 10, 8, 20, 5], copy["counts"]))
    voices = []
    for i, slug in enumerate(["claude-resources", "platform-docs", "developer-blog"]):
        sample = next(p for p in MANIFEST["pages"] if p["slug"] == slug)
        voices.append(f'<article class="voice"><div class="voice-image">{figure("../../assets/screenshots/" + slug + ".png", CONTENT["pages"][sample["id"]][lang],lang)}</div><h3>{copy["directions"][i]}</h3><p>{copy["directionText"][i]}</p><a href="{sample["url"]}">{sample["id"]} · {copy["source"]} ↗</a></article>')
    paths = ''.join(f'<a class="path-card" href="?topic={topic}#chapters" data-path-topic="{topic}"><div class="card-art">{topic_art(i)}</div><div class="card-copy"><h3>{copy["topicLabels"][i]}</h3><p>{copy["topicDescriptions"][i]}</p><span class="card-meta">{sum(chapter_topic(c)==i for c in CHAPTERS)} {copy["chapterUnit"]}<span aria-hidden="true">→</span></span></div></a>' for i,topic in enumerate(TOPICS))
    chapters = []
    for i,c in enumerate(CHAPTERS):
        group = chapter_topic(c)
        search_text = ' '.join([c['en'],c['zh'],c['summary']['en'],c['summary']['zh']])
        chapters.append(f'<a class="catalog-card" href="{c["slug"]}.html" data-chapter-topic="{TOPICS[group]}" data-chapter-search="{esc(search_text)}"><div class="card-art">{topic_art(group)}</div><div class="card-copy"><span class="card-meta">{copy["chapterWord"]} {i+1:02} · {copy["topicLabels"][group]}</span><h3>{esc(c[lang])}</h3><p>{esc(c["summary"][lang])}</p><span class="card-arrow" aria-hidden="true">→</span></div></a>')
    tabs = ''.join(f'<button type="button" role="tab" id="topic-{topic}" aria-selected="{str(i==0).lower()}" aria-controls="chapter-grid" tabindex="{0 if i==0 else -1}" data-topic-filter="{topic}">{esc(label)}</button>' for i,(topic,label) in enumerate(zip(['all',*TOPICS],[copy['allChapters'],*copy['topicLabels']])))
    review_anchor = 'academy-interactions' if lang == 'en' else 'academy-交互研究'
    html_content = f'''<header class="academy-hero"><div class="hero-inner"><p class="hero-kicker">{copy["handbook"]} · Anthropic &amp; Claude</p><h1>{copy["hubTitle"]}</h1><p>{copy["hubIntro"]}</p><div class="intro-actions"><a class="primary-link" href="#paths">{copy["choosePath"]}</a><a class="secondary-link" href="#chapters">{copy["browseChapters"]}</a></div></div></header>
<div class="home-content"><section class="home-section" id="paths"><div class="section-heading"><h2>{copy["pathsTitle"]}</h2><p>{copy["pathsIntro"]}</p></div><div class="path-grid">{paths}</div></section>
<section class="home-section" id="chapters"><div class="section-heading"><h2>{copy["chapters"]}</h2><p>{copy["chapterIntro"]}</p></div><div class="catalog-tools"><div class="topic-tabs" role="tablist" aria-label="{copy["browseChapters"]}">{tabs}</div><div class="catalog-search"><label for="chapter-search">{copy["chapterSearch"]}</label><input id="chapter-search" type="search" placeholder="{copy["searchHint"]}"><button type="button" data-clear-chapters>{copy["clearFilters"]}</button></div></div><p id="chapter-count" role="status">10 {copy["chapterUnit"]}</p><div id="chapter-grid" class="chapter-catalog" role="tabpanel" aria-labelledby="topic-all" tabindex="-1">{"".join(chapters)}</div><div class="catalog-empty" hidden><p>{copy["noChapters"]}</p><button type="button" class="secondary-link" data-clear-chapters>{copy["clearFilters"]}</button></div></section>
<section class="home-section" id="visual-directions"><div class="section-heading"><h2>{copy["voices"]}</h2><p>{copy["voicesIntro"]}</p></div><div class="voices">{"".join(voices)}</div></section>
<section class="home-section" id="findings"><div class="section-heading"><h2>{copy["findings"]}</h2><p>{copy["scope"]}</p></div><div class="study-counts">{stats}</div><p class="scope-note">{copy["date"]}: {DATE} · <a href="07-methodology-and-sources.html">{copy["methods"]}</a></p></section>
<div class="hub-links"><section class="explore-banner" id="compare"><h2>{copy["explore"]}</h2><p>{copy["compareIntro"]}</p><a class="text-link" href="explore.html">{copy["explore"]} →</a></section><section class="explore-banner"><h2>{copy["interactionNotes"]}</h2><p>{copy["interactionIntro"]}</p><a class="text-link" href="05-ux-and-responsive.html#{review_anchor}">{copy["interactionNotes"]} →</a></section></div></div>'''
    return shell(lang, "index", copy["home"], html_content)


def pattern_rows(lang):
    content = source_file(lang, CHAPTERS[3]).read_text(encoding="utf-8")
    rows = {}
    for line in content.splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 4 and re.fullmatch(r"P\d{2}", cells[0]):
            rows[cells[0]] = cells[1:]
    return rows


def comparison_panel(lang, side, selected):
    copy = COPY[lang]
    options = "".join(f'<option value="{p["id"]}"{" selected" if p["id"] == selected else ""}>{p["id"]} · {esc(CONTENT["pages"][p["id"]][lang])}</option>' for p in MANIFEST["pages"])
    panels = []
    for p in MANIFEST["pages"]:
        profile = CONTENT["pages"][p["id"]]
        hidden = " hidden" if p["id"] != selected else ""
        note = f'<p class="capture-note">{esc(profile["note"][lang])}</p>' if "note" in profile else ""
        panels.append(f'<div class="compare-sample" data-sample="{p["id"]}"{hidden}><div class="compare-content"><div class="compare-media">{figure("../../assets/screenshots/" + p["slug"] + ".png",profile[lang],lang)}</div><dl class="compare-analysis"><dt>{copy["task"]}</dt><dd>{esc(profile["task"][lang])}</dd><dt>{copy["structure"]}</dt><dd>{esc(profile["structure"][lang])}</dd><dt>{copy["fonts"]}</dt><dd class="font-names">{esc(profile["fonts"])}</dd></dl></div>{note}<div class="evidence-links"><a href="{p["url"]}">{p["id"]} · {copy["source"]} ↗</a><a href="../../data/pages/{p["slug"]}.json">{copy["record"]} ↗</a></div></div>')
    view_switch = f'<fieldset class="view-switch"><legend class="sr-only">{copy["compareView"]} · {copy[side]}</legend><label><input type="radio" name="view-{side}" value="image" data-compare-view checked><span>{copy["imageView"]}</span></label><label><input type="radio" name="view-{side}" value="analysis" data-compare-view><span>{copy["analysisView"]}</span></label></fieldset>'
    return f'<section class="compare-panel" data-view="image"><label for="compare-{side}">{copy[side]}</label><select id="compare-{side}" data-compare>{options}</select>{view_switch}{"".join(panels)}</section>'


def explorer(lang):
    copy = COPY[lang]
    rows = pattern_rows(lang)
    groups = list(dict.fromkeys(p["group"] for p in TAXONOMY["componentPatterns"]))
    filters = f'<button type="button" class="filter-button" data-filter="all" aria-pressed="true">{copy["all"]} <span>20</span></button>'
    filters += "".join(f'<button type="button" class="filter-button" data-filter="{i}" aria-pressed="false">{esc(label)} <span>4</span></button>' for i, label in enumerate(copy["groups"]))
    cards = []
    for pattern in TAXONOMY["componentPatterns"]:
        name, example, purpose = rows[pattern["id"]]
        group = groups.index(pattern["group"])
        sources = []
        for sid in pattern["sources"]:
            sample = next(p for p in MANIFEST["pages"] if p["id"] == sid)
            sources.append(f'<a href="{sample["url"]}" aria-label="{sid}: {esc(CONTENT["pages"][sid][lang])}">{sid} ↗</a>')
        cards.append(f'<article class="pattern-card" data-pattern-group="{group}"><p class="eyebrow">{pattern["id"]} / {esc(copy["groups"][group])}</p><h3>{esc(name)}</h3><p>{esc(purpose)}</p><p class="pattern-example">{esc(example)}</p><div class="source-pills">{"".join(sources)}</div></article>')
    bars = []
    sizes = []
    for p in MANIFEST["pages"]:
        if p["id"] not in {"S03", "S04", "S05", "S06", "S07", "S08", "S10"}:
            continue
        record = json.loads((ROOT / "data/pages" / (p["slug"] + ".json")).read_text(encoding="utf-8"))
        measure = next(m for m in record["measurements"] if m["selector"] == "h1")
        sizes.append((float(measure["fontSize"].removesuffix("px")), p))
    for size, p in sorted(sizes, key=lambda item: -item[0]):
        bars.append(f'<div class="type-row"><a href="../../data/pages/{p["slug"]}.json">{esc(CONTENT["pages"][p["id"]][lang])}<small>{p["id"]}</small></a><div class="type-track"><span style="width:{size / 72 * 100:.4f}%"></span></div><strong>{size:g}<small>px</small></strong></div>')
    colors = ["#FAF9F5", "#141413", "#30302E", "#FCFCFB", "#0B0B0B", "#52514E"]
    swatches = "".join(f'<button class="swatch" type="button" data-copy-color="{color}" aria-label="{esc(copy["colorNames"][i])}: {color}"><span class="swatch-color" style="background:{color}"></span><strong>{color}</strong><span>{copy["colorNames"][i]}</span><small>{["S01 / S04", "S01 / S04", "S04", "S08", "S08", "S08"][i]}</small></button>' for i, color in enumerate(colors))
    content = article_header(lang, copy["explore"], copy["compareIntro"], copy["compareNav"])
    content += f'''<section class="atlas-section" id="comparison"><div class="section-heading"><h2>{copy["compare"]}</h2></div><div class="comparison-grid">{comparison_panel(lang,"left","S04")}{comparison_panel(lang,"right","S08")}</div></section>
<section class="atlas-section" id="type-scale"><div class="section-heading"><h2>{copy["typeChart"]}</h2><p>{copy["typeIntro"]}</p></div><div class="type-chart">{"".join(bars)}</div><a class="text-link" href="02-typography.html">{CHAPTERS[1][lang]} ↗</a></section>
<section class="atlas-section" id="colors"><div class="section-heading"><h2>{copy["colorTitle"]}</h2><p>{copy["colorText"]}</p></div><div class="swatches">{swatches}</div><p id="copy-status" role="status"></p><a class="text-link" href="01-visual-language.html">{CHAPTERS[0][lang]} ↗</a></section>
<section class="atlas-section" id="patterns"><div class="section-heading"><h2>{copy["catalog"]}</h2><p>{copy["catalogIntro"]}</p></div><div class="pattern-filters" role="group" aria-label="{copy["catalog"]}">{filters}</div><p class="pattern-count" role="status">20 {copy["patterns"]}</p><div class="pattern-grid">{"".join(cards)}</div></section>'''
    headings = [("h2",copy[label],anchor) for label,anchor in [("compare","comparison"),("typeChart","type-scale"),("colorTitle","colors"),("catalog","patterns")]]
    return shell(lang, "explore", copy["explore"], content, headings)


def main():
    for lang in COPY:
        search = []
        write(html_file(lang, "index"), home(lang))
        write(html_file(lang, "explore"), explorer(lang))
        for i, chapter in enumerate(CHAPTERS):
            body, headings, records = render_chapter(lang, chapter)
            search.extend(records)
            group = next(j for j, chapters in enumerate(NAV_GROUPS) if chapter in chapters)
            header = article_header(lang, chapter[lang], chapter["summary"][lang], COPY[lang]["navGroups"][group], copy_page=True)
            source_link = f'<div class="article-source"><a href="{relative(source_file(lang, chapter), html_file(lang, chapter["slug"]))}">{COPY[lang]["viewSource"]} ↗</a><span>{i + 1:02} / 10</span></div>'
            article = header + '<article class="prose">' + body + '</article>' + source_link
            write(html_file(lang, chapter["slug"]), shell(lang, chapter["slug"], chapter[lang], article, headings, chapter))
        search_json = json.dumps(search, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        write(OUT / "shared" / f"search-{lang}.js", "window.STUDY_SEARCH=" + search_json + ";\n")
    for name in ["style.css", "app.js", "academy.css", "academy.js", "favicon.svg"]:
        write(OUT / "shared" / name, (ROOT / "web" / name).read_text(encoding="utf-8"))
    redirect = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><title>Anthropic &amp; Claude Design Study</title><p><a href="{target}">Read in English</a> · <a href="{chinese}">中文</a></p></html>\n'
    write(ROOT / "index.html", redirect.format(target="html/en/index.html", chinese="html/zh/index.html"))
    write(OUT / "index.html", redirect.format(target="en/index.html", chinese="zh/index.html"))
    write(ROOT / ".nojekyll", "")
    print("Built 24 bilingual reading pages, local search indexes, and English default entrances.")


if __name__ == "__main__":
    main()

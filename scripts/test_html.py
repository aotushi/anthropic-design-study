"""Exercise the reading edition in a real browser, including downloaded-file use."""
import argparse
import asyncio
import functools
import json
import re
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / ".preview/html"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def check_layout(page):
    result = await page.evaluate("""async () => {
      const images=[...document.images].filter(i=>i.hasAttribute('src'));
      images.forEach(i=>i.loading='eager');
      await Promise.all(images.map(i=>i.decode().catch(()=>{})));
      return {overflow:document.documentElement.scrollWidth>innerWidth,
        broken:images.filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src'))};
    }""")
    assert not result["overflow"], (page.url, result)
    assert not result["broken"], (page.url, result)


async def check_document_controls(page, context, base):
    await context.grant_permissions(["clipboard-read", "clipboard-write"])
    for lang in ["en", "zh"]:
        await page.goto(f"{base}/html/{lang}/02-typography.html")
        await expect(page.locator(".page-toc")).to_be_visible()
        await expect(page.locator(".inline-toc")).not_to_be_visible()
        article = await page.locator("main").bounding_box()
        toc = await page.locator(".page-toc").bounding_box()
        assert article["x"] + article["width"] < toc["x"], (article, toc)
        await page.locator("[data-copy-page]").click()
        await expect(page.locator("#page-copy-status")).to_have_text("Page copied" if lang == "en" else "页面已复制")
        source = ROOT / "docs" / ("en" if lang == "en" else "") / "02-typography.md"
        copied = await page.evaluate("navigator.clipboard.readText()")
        assert copied.replace("\r\n", "\n") == source.read_text(encoding="utf-8")
        section = page.locator(".section-toc a").nth(1)
        anchor = await section.get_attribute("href")
        await section.click()
        await expect(section).to_have_attribute("aria-current", "location")
        target = page.locator(anchor)
        bounds = await target.bounding_box()
        header = await page.locator(".site-header").bounding_box()
        assert bounds["y"] >= header["height"] - 1, (bounds, header)
        await expect(target.locator(".heading-anchor")).to_have_attribute("href", anchor)
    await page.evaluate("Object.defineProperty(navigator.clipboard,'writeText',{configurable:true,value:async()=>{throw new Error('Clipboard unavailable')}})")
    await page.locator("[data-copy-page]").click()
    await expect(page.locator("#page-copy-status")).to_be_visible()
    assert await page.locator("#page-copy-status a").evaluate("link => link.href") == f"{base}/docs/02-typography.md"
    await page.evaluate("delete navigator.clipboard.writeText")


async def check_academy_controls(page, context, base):
    await page.goto(f"{base}/html/en/index.html")
    menus = page.locator(".header-disclosure")
    await menus.first.locator("summary").hover()
    await expect(menus.first).to_have_attribute("open", "")
    await expect(menus.first.locator("a")).to_have_count(10)
    await check_layout(page)
    await page.screenshot(path=str(SCREENSHOTS / "en-grouped-menu.png"), animations="disabled")
    await page.keyboard.press("Escape")
    await expect(menus.first).not_to_have_attribute("open", "")
    await expect(menus.first.locator("summary")).to_be_focused()
    await page.keyboard.press("ArrowDown")
    await expect(menus.first.locator("a").first).to_be_focused()
    await page.keyboard.press("Escape")
    await menus.last.locator("summary").hover()
    await expect(menus.last).to_have_attribute("open", "")
    await page.locator("main h1").click()
    await expect(menus.last).not_to_have_attribute("open", "")

    art = page.locator(".path-card .card-art svg").first
    await page.locator(".path-card").first.hover()
    await expect(art).to_have_css("transform", "matrix(1.04, 0, 0, 1.04, 0, 0)")
    await page.emulate_media(reduced_motion="reduce")
    await expect(art).to_have_css("transform", "none")
    await page.emulate_media(reduced_motion="no-preference")

    cards = page.locator(".catalog-card:visible")
    await expect(cards).to_have_count(10)
    for topic, count in [("foundations", 2), ("experience", 3), ("research", 5), ("all", 10)]:
        tab = page.locator(f'[data-topic-filter="{topic}"]')
        await tab.click()
        await expect(tab).to_have_attribute("aria-selected", "true")
        await expect(cards).to_have_count(count)
        await expect(page.locator("#chapter-count")).to_have_text(f"{count} chapters")
    await page.locator('[data-topic-filter="all"]').press("ArrowRight")
    await expect(cards).to_have_count(2)
    await expect(page.locator('[data-topic-filter="foundations"]')).to_be_focused()
    await page.locator("#chapter-search").fill("字体与排版")
    await expect(cards).to_have_count(1)
    await expect(page.locator("#chapter-count")).to_have_text("1 chapter")
    assert await page.evaluate("new URL(location.href).searchParams.get('q')") == "字体与排版"
    await page.reload()
    await expect(cards).to_have_count(1)
    await page.locator(".language-switch").click()
    await page.wait_for_url(re.compile(r"/zh/index\.html\?"))
    await expect(cards).to_have_count(1)
    await expect(page.locator("#chapter-search")).to_have_value("字体与排版")
    await page.locator(".language-switch").click()
    await page.wait_for_url(re.compile(r"/en/index\.html\?"))
    await page.locator("#chapter-search").fill("no-such-chapter-3298")
    await expect(cards).to_have_count(0)
    await expect(page.locator(".catalog-empty")).to_be_visible()
    await page.locator(".catalog-empty [data-clear-chapters]").click()
    await expect(cards).to_have_count(10)
    await expect(page.locator("#chapter-search")).to_be_focused()

    await page.locator('[data-path-topic="experience"]').click()
    await expect(cards).to_have_count(3)
    await expect(page.locator('[data-topic-filter="experience"]')).to_be_focused()
    assert await page.evaluate("location.hash") == "#chapters"
    await page.locator('[data-topic-filter="research"]').click()
    await page.go_back()
    await expect(cards).to_have_count(3)
    await expect(page.locator('[data-topic-filter="experience"]')).to_have_attribute("aria-selected", "true")
    await page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    await expect(cards).to_have_count(10)
    await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    await expect(cards).to_have_count(3)
    await page.locator('[data-topic-filter="experience"]').press("Home")
    await expect(cards).to_have_count(10)
    await page.locator('[data-topic-filter="all"]').press("End")
    await expect(cards).to_have_count(5)

    await page.goto(f"{base}/html/en/index.html")
    await page.locator("[data-theme-toggle]").click()
    await expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    await expect(page.locator("[data-theme-toggle]")).to_have_attribute("aria-label", "Switch to light theme")
    await page.reload()
    await expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    for lang in ["en", "zh"]:
        for slug in ["index", "02-typography", "explore"]:
            await page.goto(f"{base}/html/{lang}/{slug}.html")
            await expect(page.locator("html")).to_have_attribute("data-theme", "dark")
            await check_layout(page)
            await page.screenshot(path=str(SCREENSHOTS / f"{lang}-{slug}-dark.png"), animations="disabled")
    await page.locator("[data-theme-toggle]").click()
    await expect(page.locator("html")).to_have_attribute("data-theme", "light")

    await page.goto(f"{base}/html/en/02-typography.html")
    selector = page.locator(".chapter-switcher")
    await selector.locator("summary").click()
    await expect(selector.locator("a")).to_have_count(10)
    await expect(selector.locator('[aria-current="page"]')).to_have_text(re.compile("Typography"))
    await selector.locator("a").first.focus()
    await page.keyboard.press("Escape")
    await expect(selector).not_to_have_attribute("open", "")
    await expect(selector.locator("summary")).to_be_focused()
    await page.keyboard.press("Enter")
    await selector.locator('a[href="10-cross-site-matrix.html"]').click()
    await page.wait_for_url("**/10-cross-site-matrix.html")
    await expect(page.locator("main h1")).to_have_text("Cross-site matrix")

    await page.goto(f"{base}/html/en/explore.html")
    panel = page.locator(".compare-panel").first
    active = panel.locator(".compare-sample:not([hidden])")
    await expect(active.locator(".compare-media")).to_be_visible()
    await expect(active.locator(".compare-analysis")).not_to_be_visible()
    await panel.locator('label:has(input[value="analysis"])').click()
    await expect(active.locator(".compare-analysis")).to_be_visible()
    await expect(active.locator(".compare-media")).not_to_be_visible()
    await page.locator("#compare-left").select_option("S07")
    await expect(active.locator(".compare-analysis")).to_contain_text("Paper Mono")
    await panel.locator('input[value="analysis"]').focus()
    await page.keyboard.press("ArrowLeft")
    await expect(active.locator(".compare-media")).to_be_visible()

    await page.set_viewport_size({"width": 390, "height": 844})
    await page.goto(f"{base}/html/zh/index.html")
    await page.locator('[data-path-topic="foundations"]').click()
    await expect(cards).to_have_count(2)
    await page.wait_for_function("document.querySelector('#chapters').getBoundingClientRect().top < 100")
    await check_layout(page)
    await page.locator("[data-theme-toggle]").click()
    await page.screenshot(path=str(SCREENSHOTS / "zh-library-mobile-dark.png"), animations="disabled")
    await page.locator("[data-theme-toggle]").click()
    await page.set_viewport_size({"width": 1440, "height": 1050})

    no_js = await context.browser.new_context(java_script_enabled=False, viewport={"width": 1440, "height": 1050})
    plain = await no_js.new_page()
    await plain.goto(f"{base}/html/en/index.html")
    await expect(plain.locator(".catalog-card:visible")).to_have_count(10)
    await plain.locator(".header-disclosure summary").first.click()
    await expect(plain.locator(".mega-menu")).to_be_visible()
    await plain.goto(f"{base}/html/en/explore.html")
    first_sample = plain.locator(".compare-sample:not([hidden])").first
    await expect(first_sample.locator(".compare-media")).to_be_visible()
    await expect(first_sample.locator(".compare-analysis")).to_be_visible()
    await no_js.close()


async def run(base, channel):
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    failures = []
    visited = []
    async with async_playwright() as p:
        kwargs = {"headless": True}
        if channel != "chromium":
            kwargs["channel"] = channel
        browser = await p.chromium.launch(**kwargs)
        context = await browser.new_context(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
        page = await context.new_page()
        page.on("pageerror", lambda error: failures.append(str(error)))
        for lang in ["en", "zh"]:
            for file in sorted((ROOT / "html" / lang).glob("*.html")):
                response = await page.goto(f"{base}/html/{lang}/{file.name}", wait_until="load")
                assert response.status == 200, (response.status, page.url)
                await expect(page.locator("main h1")).to_have_count(1)
                await check_layout(page)
                visited.append(f"{lang}/{file.name}")
                if file.stem in {"index", "explore", "02-typography"}:
                    await page.screenshot(path=str(SCREENSHOTS / f"{lang}-{file.stem}-desktop.png"))

        await check_academy_controls(page, context, base)
        await check_document_controls(page, context, base)
        await page.goto(f"{base}/html/en/02-typography.html")
        await page.locator(".language-switch").click()
        await page.wait_for_url("**/zh/02-typography.html")
        await expect(page.locator("main h1")).to_have_text("字体与排版")
        await page.locator(".language-switch").click()
        await page.wait_for_url("**/en/02-typography.html")

        await page.locator(".search-trigger").click()
        await expect(page.locator("#study-search")).to_be_focused()
        await page.locator("#study-search").fill("Paper Mono")
        await expect(page.locator(".search-result").first).to_be_visible()
        target = await page.locator(".search-result").first.get_attribute("href")
        await page.locator("#study-search").press("ArrowDown")
        await page.keyboard.press("Enter")
        await page.wait_for_url("**/en/" + target)
        await expect(page.locator("#search-dialog")).not_to_be_visible()
        await page.locator(".search-trigger").click()
        await page.locator("#study-search").fill("zyx-no-study-result-91827")
        await expect(page.locator(".search-result")).to_have_count(0)
        await expect(page.locator("#search-status")).to_contain_text("No results")
        await page.keyboard.press("Escape")
        await expect(page.locator(".search-trigger")).to_be_focused()

        await page.goto(f"{base}/html/zh/index.html")
        await page.keyboard.press("/")
        await page.locator("#study-search").fill("字体")
        await expect(page.locator(".search-result").first).to_be_visible()
        await page.keyboard.press("Escape")

        await page.goto(f"{base}/html/en/06-gallery.html")
        await page.locator(".prose details summary").first.click()
        figure = page.locator(".prose details .figure-button").first
        await figure.click()
        await expect(page.locator("#image-dialog")).to_be_visible()
        await expect(page.locator("#enlarged-image")).to_have_attribute("alt", "Anthropic company homepage")
        await page.keyboard.press("Escape")
        await expect(figure).to_be_focused()
        await page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        assert await page.locator("main details:not([open])").count() == 0
        await page.emulate_media(media="print")
        await expect(page.locator(".site-header")).not_to_be_visible()
        await page.emulate_media(media="screen", reduced_motion="reduce")
        await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert await page.locator("main details:not([open])").count() > 0
        assert await page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"

        await page.goto(f"{base}/html/en/explore.html")
        await page.locator("#compare-left").select_option("S07")
        await expect(page.locator(".compare-panel").first.locator(".compare-sample:not([hidden])")).to_contain_text("Paper Mono")
        await page.locator("#compare-right").select_option("S09")
        await expect(page.locator(".compare-panel").last.locator(".compare-sample:not([hidden])")).to_contain_text("Consolas")
        await expect(page.locator(".type-row")).to_have_count(7)
        await expect(page.locator(".type-chart")).to_contain_text("26.25")
        for group in range(5):
            await page.locator(f'[data-filter="{group}"]').click()
            await expect(page.locator(".pattern-card:visible")).to_have_count(4)
            await expect(page.locator(".pattern-count")).to_have_text("4 patterns")
        await page.locator('[data-filter="all"]').click()
        await expect(page.locator(".pattern-card:visible")).to_have_count(20)
        await context.grant_permissions(["clipboard-read", "clipboard-write"])
        await page.locator("[data-copy-color]").first.click()
        await expect(page.locator("#copy-status")).to_have_text("Copied: #FAF9F5")
        assert await page.evaluate("navigator.clipboard.readText()") == "#FAF9F5"

        for width in [375, 390, 768, 920, 921, 1024, 1239, 1240]:
            await page.set_viewport_size({"width": width, "height": 844})
            for lang in ["en", "zh"]:
                for slug in ["index", "02-typography", "05-ux-and-responsive", "09-page-anatomy", "explore"]:
                    await page.goto(f"{base}/html/{lang}/{slug}.html")
                    await check_layout(page)
                    if slug == "index":
                        await expect(page.locator("#chapter-grid")).to_be_visible()
                    elif width >= 1240:
                        await expect(page.locator(".page-toc")).to_be_visible()
                        await expect(page.locator(".inline-toc")).not_to_be_visible()
                    else:
                        await expect(page.locator(".page-toc")).not_to_be_visible()
                        await expect(page.locator(".inline-toc")).to_be_visible()
                    if width == 390 and slug in {"index", "explore", "02-typography"}:
                        await page.screenshot(path=str(SCREENSHOTS / f"{lang}-{slug}-mobile.png"))
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.goto(f"{base}/html/en/index.html")
        await page.locator(".menu-toggle").click()
        await expect(page.locator(".menu-toggle")).to_have_attribute("aria-expanded", "true")
        await page.locator("#chapter-nav a").last.focus()
        await page.keyboard.press("Tab")
        await expect(page.locator(".brand")).to_be_focused()
        await page.keyboard.press("Shift+Tab")
        await expect(page.locator("#chapter-nav a").last).to_be_focused()
        await page.locator('#chapter-nav a[href="04-components.html"]').click()
        await page.wait_for_url("**/en/04-components.html")
        await expect(page.locator(".menu-toggle")).to_have_attribute("aria-expanded", "false")
        await page.locator(".menu-toggle").click()
        await page.keyboard.press("Escape")
        await expect(page.locator(".menu-toggle")).to_be_focused()
        await expect(page.locator(".menu-toggle")).to_have_attribute("aria-expanded", "false")

        await page.goto(base + "/")
        await page.wait_for_url("**/html/en/index.html")
        offline = await context.new_page()
        remote_requests = []
        offline.on("request", lambda req: remote_requests.append(req.url) if req.url.startswith(("http:", "https:")) else None)
        offline.on("pageerror", lambda error: failures.append(str(error)))
        await offline.goto((ROOT / "html/en/index.html").as_uri())
        await offline.locator(".search-trigger").click()
        await offline.locator("#study-search").fill("Paper Mono")
        await expect(offline.locator(".search-result").first).to_be_visible()
        await offline.keyboard.press("Escape")
        await offline.locator('[data-path-topic="foundations"]').click()
        await expect(offline.locator(".catalog-card:visible")).to_have_count(2)
        await offline.locator(".language-switch").click()
        await offline.wait_for_url(re.compile(r"/zh/index\.html"))
        await check_layout(offline)
        assert not remote_requests, remote_requests
        assert not failures, failures
        await browser.close()
    print(json.dumps({"pagesChecked": len(visited), "widths": [1440, 1240, 1239, 1024, 921, 920, 768, 390, 375], "interactions": "passed", "academyMenusFiltersThemesViews": "passed", "copyAndSectionNavigation": "passed", "offline": "passed", "noJavaScriptReading": "passed", "consoleErrors": failures}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", help="Use a published base URL instead of the local preview server")
    parser.add_argument("--channel", default="chrome")
    args = parser.parse_args()
    server = None
    if args.base_url:
        base = args.base_url.rstrip("/")
    else:
        handler = functools.partial(QuietHandler, directory=str(ROOT))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}"
    try:
        asyncio.run(run(base, args.channel))
    finally:
        if server:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()

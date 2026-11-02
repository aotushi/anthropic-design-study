"""Exercise the reading edition in a real browser, including downloaded-file use."""
import argparse
import asyncio
import functools
import json
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
        assert await page.locator("details:not([open])").count() == 0
        await page.emulate_media(media="print")
        await expect(page.locator(".site-header")).not_to_be_visible()
        await page.emulate_media(media="screen", reduced_motion="reduce")
        await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert await page.locator("details:not([open])").count() > 0
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

        for width in [375, 390, 768, 1024]:
            await page.set_viewport_size({"width": width, "height": 844})
            for lang in ["en", "zh"]:
                for slug in ["index", "02-typography", "09-page-anatomy", "explore"]:
                    await page.goto(f"{base}/html/{lang}/{slug}.html")
                    await check_layout(page)
                    if width == 390 and slug in {"index", "explore"}:
                        await page.screenshot(path=str(SCREENSHOTS / f"{lang}-{slug}-mobile.png"))
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.goto(f"{base}/html/en/index.html")
        await page.locator(".menu-toggle").click()
        await expect(page.locator(".menu-toggle")).to_have_attribute("aria-expanded", "true")
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
        await offline.locator(".language-switch").click()
        await offline.wait_for_url("**/zh/index.html")
        await check_layout(offline)
        assert not remote_requests, remote_requests
        assert not failures, failures
        await browser.close()
    print(json.dumps({"pagesChecked": len(visited), "widths": [1440, 1024, 768, 390, 375], "interactions": "passed", "offline": "passed", "consoleErrors": failures}, ensure_ascii=False))


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

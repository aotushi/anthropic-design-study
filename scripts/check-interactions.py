"""Read-only interaction samples for this study; never signs in or submits forms."""
import asyncio
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("capture", ROOT / "scripts/capture.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


async def main():
    checks = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1, color_scheme="light", locale="en-US")
        await context.route("**://claude.ai/**", lambda route: route.abort())
        page = await context.new_page()

        async def open_url(url):
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.locator("h1").first.wait_for()
            await page.evaluate("() => Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,5000))])")
            await page.wait_for_timeout(3000)

        async def run(name, function):
            try:
                result = await function()
                checks.append({"name": name, "status": "passed", **result})
            except Exception as error:
                checks.append({"name": name, "status": "not_verified", "detail": (str(error) or repr(error)).splitlines()[0]})

        async def pricing():
            await open_url("https://claude.com/pricing")
            before = await page.locator("[role=tab][aria-selected=true]").all_text_contents()
            tab = page.get_by_role("tab", name="Team & Enterprise", exact=True)
            await tab.click(timeout=10000)
            await expect(tab).to_have_attribute("aria-selected", "true", timeout=10000)
            await page.get_by_role("heading", name="Team", exact=True).wait_for()
            await page.wait_for_timeout(1200)
            await page.screenshot(path=str(ROOT / "assets/screenshots/pricing-team.png"))
            return {"source": "S03", "before": before, "after": await page.locator("[role=tab][aria-selected=true]").all_text_contents(), "screenshot": "assets/screenshots/pricing-team.png"}

        async def blog():
            await open_url("https://claude.dev/")
            before = await page.locator('a[href*="/blog/"]').count()
            await page.get_by_role("button", name="TUTORIALS", exact=True).click()
            await page.wait_for_timeout(300)
            after = await page.locator('a[href*="/blog/"]').count()
            assert 0 < after < before, (before, after)
            await page.get_by_role("button", name="ALL", exact=True).click()
            restored = await page.locator('a[href*="/blog/"]').count()
            assert restored == before
            return {"source": "S10", "before": before, "filtered": after, "restored": restored}

        async def transcript():
            await open_url("https://academy.claude.com/courses/ai-fluency-framework-foundations/introduction-to-ai-fluency")
            radio = page.get_by_role("radio", name="Transcript", exact=True)
            await radio.click(timeout=10000)
            await expect(radio).to_have_attribute("aria-checked", "true", timeout=10000)
            await page.screenshot(path=str(ROOT / "assets/screenshots/academy-transcript.png"))
            return {"source": "S06", "selected": "Transcript", "ariaChecked": True, "screenshot": "assets/screenshots/academy-transcript.png"}

        async def code():
            await open_url("https://code.claude.com/docs/en/overview")
            await page.locator("pre").first.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            fonts = await capture.platform_fonts(page)
            await page.screenshot(path=str(ROOT / "assets/screenshots/code-example.png"))
            return {"source": "S07", "renderedFonts": fonts, "screenshot": "assets/screenshots/code-example.png"}

        async def keyboard():
            await open_url("https://claude.com/resources")
            await page.keyboard.press("Tab")
            return {"source": "S04", "firstFocus": await page.evaluate("() => ({tag:document.activeElement.tagName,text:document.activeElement.textContent.trim().slice(0,90),href:document.activeElement.getAttribute('href')})")}

        for name, fn in [("pricing_audience_tabs", pricing), ("blog_category_filter", blog), ("lesson_transcript_switch", transcript), ("code_example_font_inspection", code), ("first_keyboard_focus", keyboard)]:
            await run(name, fn)
            print(json.dumps(checks[-1], ensure_ascii=False), flush=True)
        await browser.close()
    output = {"checkedAt": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(), "scope": "Public pages; bounded checks, not a full usability or accessibility audit", "checks": checks}
    (ROOT / "data/interaction-checks.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())

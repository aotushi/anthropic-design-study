"""Capture public reference pages without opening the Claude conversation app.

Optional authoring tool. Requires Playwright 1.58+ and Chrome (or installed Chromium).
Usage: python scripts/capture.py --ids S01 S02 --channel chrome
Screenshots are unaltered browser captures. Never saves cookies or page HTML.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "data/sample-manifest.json").read_text(encoding="utf-8"))
INSPECTOR = (ROOT / "scripts/inspect-page.js").read_text(encoding="utf-8")


async def platform_fonts(page):
    session = await page.context.new_cdp_session(page)
    await session.send("DOM.enable")
    await session.send("CSS.enable")
    root = (await session.send("DOM.getDocument"))["root"]["nodeId"]
    result = []
    for selector in ["h1", "h1 span", "main p", "article p", "nav a", "button", "code", "pre", "pre span", "pre span span", "code span", "code span span", "kbd"]:
        node = (await session.send("DOM.querySelector", {"nodeId": root, "selector": selector}))["nodeId"]
        if node:
            fonts = (await session.send("CSS.getPlatformFontsForNode", {"nodeId": node}))["fonts"]
            result.append({"selector": selector, "fonts": fonts})
    await session.detach()
    return result


async def inspect_extra(page):
    return await page.evaluate("""() => {
      const isVisible=e=>e.getBoundingClientRect().height>0&&getComputedStyle(e).visibility!=='hidden';
      const selectors=['h1','h1 span','main p','main button','button','[role=tab]','pre','code','main a'];
      return {
        viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},
        pageSize:{width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight},
        documentVisible:!document.hidden,
        reducedMotion:matchMedia('(prefers-reduced-motion: reduce)').matches,
        colors:{bodyBackground:getComputedStyle(document.body).backgroundColor,bodyColor:getComputedStyle(document.body).color},
        measurements:selectors.map(selector=>{const e=[...document.querySelectorAll(selector)].find(isVisible);if(!e)return{selector};const s=getComputedStyle(e),r=e.getBoundingClientRect();return{selector,text:e.innerText?.slice(0,60),fontFamily:s.fontFamily,fontSize:s.fontSize,lineHeight:s.lineHeight,fontWeight:s.fontWeight,borderRadius:s.borderRadius,padding:s.padding,border:s.border,background:s.backgroundColor,color:s.color,width:Math.round(r.width),height:Math.round(r.height)}}),
        effectiveBackgrounds:['h1','main p'].map(selector=>{let e=[...document.querySelectorAll(selector)].find(isVisible);while(e){const s=getComputedStyle(e);if(s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!=='transparent')return{selector,background:s.backgroundColor,backgroundImage:s.backgroundImage,ancestorTag:e.tagName};e=e.parentElement}return{selector,background:'not determined'}}),
        fontResources:performance.getEntriesByType('resource').filter(r=>/\\.(woff2?|otf|ttf)(\\?|$)|\\/assets\\/font\\//.test(r.name)).map(r=>({url:r.name,duration:Math.round(r.duration)})),
        fontRuleSources:[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules].filter(r=>r.type===5).map(r=>({stylesheet:s.href,family:r.style.fontFamily,src:r.style.src,weight:r.style.fontWeight,style:r.style.fontStyle}))}catch{return[]}})
      };
    }""")


async def capture(browser, entry, mobile=False):
    viewport = MANIFEST["mobileViewport" if mobile else "desktopViewport"]
    context = await browser.new_context(viewport=viewport, device_scale_factor=1, locale="en-US", color_scheme="light", timezone_id="Asia/Shanghai", reduced_motion="no-preference")
    await context.route("**://claude.ai/**", lambda route: route.abort())
    page = await context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)[:200]))
    suffix = "-mobile" if mobile else ""
    slug = entry["slug"] + suffix
    try:
        try:
            await page.goto(entry["url"], wait_until="domcontentloaded", timeout=45000)
        except Exception as error:
            errors.append(str(error).splitlines()[0][:200])
        await page.locator("h1").first.wait_for(state="attached", timeout=20000)
        await page.evaluate("() => Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,8000))])")
        await page.wait_for_timeout(2500)
        if entry["id"] == "S02":
            await page.wait_for_timeout(8000)
        if entry["id"] == "S01":
            await page.mouse.wheel(0, 600)
            await page.wait_for_timeout(2000)
            await page.evaluate("() => window.scrollTo({top:0,behavior:'instant'})")
            await page.wait_for_timeout(1500)
        try:
            await page.wait_for_function("() => {const e=document.querySelector('h1'),s=e&&getComputedStyle(e);return e&&e.getBoundingClientRect().height>0&&s.visibility!=='hidden'&&Number(s.opacity)>0.95}", timeout=8000)
        except Exception:
            errors.append("Heading did not become fully visible during the bounded wait; inspect screenshot.")
        data = await page.evaluate(INSPECTOR)
        data.update(await inspect_extra(page))
        data["renderedFonts"] = await platform_fonts(page)
        now = datetime.now(ZoneInfo("Asia/Shanghai"))
        data.update({"id": entry["id"] + ("-M" if mobile else ""), "name": entry["name"], "slug": slug, "checkedAt": now.isoformat(), "dateLocal": now.date().isoformat(), "timezone": "Asia/Shanghai", "screenshot": f"assets/screenshots/{slug}.png", "captureMethod": "Playwright Chromium browser screenshot, no image edits", "captureIssues": errors})
        await page.screenshot(path=str(ROOT / data["screenshot"]), full_page=False, scale="css", timeout=20000)
        (ROOT / f"data/pages/{slug}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"id": data["id"], "url": data["url"], "screenshot": data["screenshot"], "visible": data["documentVisible"], "heading": data["samples"][1], "issues": errors}, ensure_ascii=False), flush=True)
    finally:
        await context.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--mobile", action="store_true")
    parser.add_argument("--channel", default="chrome")
    args = parser.parse_args()
    pages = [p for p in MANIFEST["pages"] if not args.ids or p["id"] in args.ids]
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel=args.channel, headless=True)
        semaphore = asyncio.Semaphore(2)
        async def run(entry):
            async with semaphore:
                try:
                    await capture(browser, entry, args.mobile)
                except Exception as error:
                    print(json.dumps({"id": entry["id"], "error": str(error)}, ensure_ascii=False), flush=True)
                    raise
        try:
            await asyncio.gather(*(run(entry) for entry in pages))
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

"""Validate the publishable document and its evidence using only the standard library."""
import html
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def anchors(text):
    seen = Counter()
    values = set()
    for line in text.splitlines():
        if re.match(r"^#{1,6} ", line):
            title = re.sub(r"^#+\s+", "", line).strip()
            title = re.sub(r"<[^>]*>", "", title)
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            number = seen[slug]
            seen[slug] += 1
            values.add(slug + (f"-{number}" if number else ""))
    return values


def main():
    markdown = [ROOT / "README.md", ROOT / "README.en.md", *sorted((ROOT / "docs").rglob("*.md")), ROOT / "NOTICE.md", ROOT / "CONTRIBUTING.md", ROOT / "CHANGELOG.md", ROOT / "web/README.md"]
    references = 0
    for file in markdown:
        text = file.read_text(encoding="utf-8")
        check(text.startswith("# "), f"Missing title: {file.name}")
        check("�" not in text, f"Encoding replacement character: {file.name}")
        targets = re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", text)
        targets += re.findall(r'(?:src|href)="([^"]+)"', text)
        for target in targets:
            target = html.unescape(target)
            if target.startswith(("https://", "http://", "mailto:")):
                continue
            references += 1
            parsed = urlsplit(target)
            destination = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
            check(destination.is_relative_to(ROOT), f"Link leaves repository: {file.name}: {target}")
            check(destination.exists(), f"Broken link: {file.relative_to(ROOT)}: {target}")
            if destination.is_file() and destination.suffix == ".md" and parsed.fragment:
                check(unquote(parsed.fragment) in anchors(destination.read_text(encoding="utf-8")), f"Broken anchor: {file.name}: {target}")
        for alt in re.findall(r"!\[([^\]]*)\]\(", text):
            check(bool(alt.strip()), f"Image without alt text: {file.name}")
        for tag in re.findall(r"<img\b[^>]*>", text):
            check(bool(re.search(r'alt="[^"]+"', tag)), f"HTML image without alt text: {file.name}")

    manifest = json.loads((ROOT / "data/sample-manifest.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((ROOT / "data/taxonomy.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]
    source_ids = {p["id"] for p in pages}
    check(len(pages) == 10, "Expected 10 representative pages")
    check(len({urlsplit(p["url"]).hostname for p in pages}) == 7, "Expected 7 official domains")
    check(len(taxonomy["visualDirections"]) == 3, "Visual direction count differs")
    check(len(taxonomy["pagePatterns"]) == 8, "Page pattern count differs")
    check(len(taxonomy["componentPatterns"]) == 20, "Component count differs")
    check(len(taxonomy["primaryFontNames"]) == 5, "Font-name count differs")
    pattern_text = (ROOT / "docs/04-components.md").read_text(encoding="utf-8")
    english_patterns = (ROOT / "docs/en/04-components.md").read_text(encoding="utf-8")
    for pattern in taxonomy["componentPatterns"]:
        check(len(re.findall(r"\| " + pattern["id"] + r" \|", pattern_text)) == 1, f"Pattern missing or duplicated: {pattern['id']}")
        check(len(re.findall(r"\| " + pattern["id"] + r" \|", english_patterns)) == 1, f"English pattern missing or duplicated: {pattern['id']}")
        check(set(pattern["sources"]) <= source_ids, f"Unknown source in {pattern['id']}")
    for file in (ROOT / "data/pages").glob("*.json"):
        data = json.loads(file.read_text(encoding="utf-8"))
        check(data["id"].split("-")[0] in source_ids, f"Unknown page: {file.name}")
        check(urlsplit(data["url"]).hostname != "claude.ai", f"Excluded app in evidence: {file.name}")
        check(data["dateLocal"] == manifest["observedDate"], f"Observation date differs: {file.name}")
        image = ROOT / data["screenshot"]
        check(image.is_file(), f"Missing screenshot: {file.name}")
        if image.is_file():
            content = image.read_bytes()
            check(content.startswith(b"\x89PNG\r\n\x1a\n"), f"Invalid PNG: {image.name}")
            width, height = struct.unpack(">II", content[16:24])
            check((width, height) == (data["viewport"]["width"], data["viewport"]["height"]), f"Screenshot dimensions differ: {image.name}")
        check(data.get("documentVisible"), f"Capture was in a hidden document: {file.name}")
    for page in pages:
        check((ROOT / f"data/pages/{page['slug']}.json").exists(), f"Missing source evidence: {page['id']}")
    screenshots = list((ROOT / "assets/screenshots").glob("*.png"))
    figures = list((ROOT / "assets/diagrams").rglob("*.svg"))
    check(len(screenshots) == 15, "Expected 15 screenshots")
    check(len(figures) == 6, "Expected 3 original figures in each language")
    chinese_chapters = {p.name for p in (ROOT / "docs").glob("[0-9][0-9]-*.md")}
    english_chapters = {p.name for p in (ROOT / "docs/en").glob("[0-9][0-9]-*.md")}
    check(len(chinese_chapters) == 10, "Expected 10 Chinese chapters")
    check(english_chapters == chinese_chapters, "Chinese and English chapter lists differ")
    for file in figures:
        try:
            ET.parse(file)
        except ET.ParseError as error:
            errors.append(f"Invalid SVG: {file.name}: {error}")
    interactions = json.loads((ROOT / "data/interaction-checks.json").read_text(encoding="utf-8"))
    for item in interactions["checks"]:
        check(item["status"] == "passed", f"Interaction needs qualification: {item['name']}")
        if item.get("screenshot"):
            check((ROOT / item["screenshot"]).is_file(), f"Missing interaction screenshot: {item['name']}")
    for file in [*markdown, *ROOT.glob("data/**/*.json"), *ROOT.glob("scripts/*")]:
        if not file.is_file():
            continue
        text = file.read_text(encoding="utf-8")
        check(not re.search(r"gh[pousr]_[A-Za-z0-9]{24,}", text), f"Possible credential in {file.name}")
        check(not re.search(r"[A-Z]:[\\/]Users[\\/]", text), f"Private user path in {file.name}")
    if errors:
        print("FAILED\n" + "\n".join(errors))
        sys.exit(1)
    print(f"PASS: {len(markdown)} Markdown files, {references} local references, {len(pages)} source pages, {len(screenshots)} screenshots, {len(figures)} SVG figures, 20 patterns, 5 bounded interaction checks.")


if __name__ == "__main__":
    main()

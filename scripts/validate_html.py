"""Check generated HTML, local navigation, search destinations, and language parity."""
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.refs = []
        self.images = []
        self.lang = ""
        self.h1 = 0
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and values.get("src"):
            self.images.append(values)
        if tag == "a":
            self.links.append(values)
        for attribute in ["href", "src"]:
            if values.get(attribute):
                self.refs.append(values[attribute])
        if tag == "meta" and values.get("http-equiv") == "refresh":
            self.refs.append(values["content"].split("url=", 1)[1])


def main():
    paths = [ROOT / "index.html", *sorted((ROOT / "html").rglob("*.html"))]
    errors = []
    documents = {p.resolve(): Document(p) for p in paths}
    refs = 0

    def check_reference(origin, ref):
        nonlocal refs
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme and parsed.scheme not in {"https", "http", "mailto"}:
                errors.append(f"Unexpected URL scheme: {origin.name}: {ref}")
            return
        target = (origin.parent / unquote(parsed.path)).resolve() if parsed.path else origin.resolve()
        refs += 1
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f"Missing local target: {origin.relative_to(ROOT)}: {ref}")
        elif parsed.fragment and target in documents and unquote(parsed.fragment) not in documents[target].ids:
            errors.append(f"Missing anchor: {origin.relative_to(ROOT)}: {ref}")

    for path, doc in documents.items():
        if not doc.lang:
            errors.append(f"Missing language: {path.name}")
        if any(count > 1 for count in Counter(doc.ids).values()):
            errors.append(f"Duplicate IDs: {path.relative_to(ROOT)}")
        for ref in doc.refs:
            check_reference(path, ref)
        for image in doc.images:
            if not image.get("alt") or not image.get("width") or not image.get("height"):
                errors.append(f"Image lacks description or size: {path.name}: {image.get('src')}")
        if path.parent.name in {"en", "zh"}:
            expected_lang = "en" if path.parent.name == "en" else "zh-CN"
            if doc.lang != expected_lang or doc.h1 != 1:
                errors.append(f"Wrong language or heading count: {path}")
            counterpart = ROOT / "html" / ("zh" if path.parent.name == "en" else "en") / path.name
            switches = [a for a in doc.links if "language-switch" in a.get("class", "")]
            if len(switches) != 1 or (path.parent / switches[0]["href"]).resolve() != counterpart.resolve():
                errors.append(f"Language link does not preserve page: {path}")
    english = {p.name for p in (ROOT / "html/en").glob("*.html")}
    chinese = {p.name for p in (ROOT / "html/zh").glob("*.html")}
    if english != chinese or len(english) != 12:
        errors.append("Expected 12 matching pages per language")
    if not (ROOT / ".nojekyll").exists():
        errors.append("Missing .nojekyll publishing marker")
    search_counts = {}
    for lang in ["en", "zh"]:
        text = (ROOT / f"html/shared/search-{lang}.js").read_text(encoding="utf-8")
        records = json.loads(text.removeprefix("window.STUDY_SEARCH=").rstrip().removesuffix(";"))
        search_counts[lang] = len(records)
        for record in records:
            check_reference(ROOT / f"html/{lang}/index.html", record["href"])
        chapters = {urlsplit(record["href"]).path for record in records}
        if len(chapters) != 10:
            errors.append(f"Search does not cover ten chapters: {lang}")
    if errors:
        print("FAILED\n" + "\n".join(errors))
        sys.exit(1)
    print(f"PASS: {len(paths)} HTML files, {refs} local references, 12 pages per language, search sections {search_counts}.")


if __name__ == "__main__":
    main()

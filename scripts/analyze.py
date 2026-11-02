"""Derive the limited contrast and viewport comparisons used in chapter 05."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rgb(value):
    return [int(v) for v in re.findall(r"\d+", value)[:3]]


def luminance(color):
    linear = [c / 255 / 12.92 if c / 255 <= .04045 else ((c / 255 + .055) / 1.055) ** 2.4 for c in color]
    return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(foreground, background):
    a, b = sorted([luminance(foreground), luminance(background)])
    return (b + .05) / (a + .05)


def main():
    # Known endpoints guard the numerical calculation, not a full accessibility audit.
    assert abs(contrast([0, 0, 0], [255, 255, 255]) - 21) < 1e-9
    assert contrast([42, 42, 42], [42, 42, 42]) == 1
    results = []
    for slug in ["claude-resources", "platform-docs"]:
        data = json.loads((ROOT / f"data/pages/{slug}.json").read_text(encoding="utf-8"))
        for selector in ["h1", "main p"]:
            sample = next(s for s in data["samples"] if s["selector"] == selector)
            bg = next(s for s in data["effectiveBackgrounds"] if s["selector"] == selector)
            background = rgb(bg["background"])
            foreground = rgb(sample["color"])
            value = contrast(foreground, background)
            results.append({"source": data["id"], "selector": selector, "foreground": foreground, "background": background, "basis": "Nearest ancestor with a nontransparent background, excluding overlaid graphics and anti-aliasing.", "backgroundImage": bg["backgroundImage"], "ratio": value, "normalTextThreshold4_5": value >= 4.5})
    responsive = []
    for slug in ["academy-home", "code-docs"]:
        versions = []
        for suffix in ["", "-mobile"]:
            data = json.loads((ROOT / f"data/pages/{slug}{suffix}.json").read_text(encoding="utf-8"))
            h1 = next(s for s in data["samples"] if s["selector"] == "h1")
            versions.append({"source": data["id"], "viewportWidth": data["viewport"]["width"], "documentWidth": data["pageSize"]["width"], "horizontalDocumentOverflow": data["pageSize"]["width"] > data["viewport"]["width"], "headingSize": h1["size"], "headingLineHeight": h1["line"]})
        responsive.append({"slug": slug, "versions": versions})
    output = {"contrast": results, "responsive": responsive, "scope": "Four text/background pairs and two narrow viewport samples only; not a whole-site accessibility assessment."}
    (ROOT / "data/derived-checks.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()

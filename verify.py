"""Verify the canonical essay, including all rendered paragraphs and separators."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent


class EssayHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.title = []
        self.document_title = []
        self.in_heading = False
        self.in_document_title = False
        self.paragraph = None
        self.emphasis = []
        self.emphasis_start = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.in_heading = True
        if tag == "title":
            self.in_document_title = True
        if "data-source" in attrs:
            index = int(attrs["data-source"])
            if tag == "hr":
                self.blocks.append([index, "HR", ""])
            elif tag == "p":
                self.paragraph = [index, "P", ""]
        if self.paragraph is not None and tag in ("em", "strong"):
            self.emphasis_start = len(self.paragraph[2])

    def handle_data(self, text):
        if self.in_heading:
            self.title.append(text)
        if self.in_document_title:
            self.document_title.append(text)
        if self.paragraph is not None:
            self.paragraph[2] += text

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_heading = False
        if tag == "title":
            self.in_document_title = False
        if tag in ("em", "strong") and self.emphasis_start is not None:
            self.emphasis.append((self.paragraph[0], tag, self.emphasis_start, len(self.paragraph[2])))
            self.emphasis_start = None
        if tag == "p" and self.paragraph is not None:
            self.blocks.append(self.paragraph)
            self.paragraph = None


source = (ROOT / "essay.md").read_bytes()
lock = json.loads((ROOT / "source-integrity.json").read_text())
if sha256(source).hexdigest() != lock["sha256"]:
    raise SystemExit("Canonical essay SHA-256 mismatch")

title, *paragraphs = source.decode("utf-8").strip().split("\n\n")
expected = []
emphasis = []
for index, paragraph in enumerate(paragraphs):
    if paragraph == "---":
        expected.append([index, "HR", ""])
        continue
    expected.append([index, "P", paragraph.replace("**", "").replace("*", "")])
    for match in re.finditer(r"\*\*[^*]+\*\*|\*[^*]+\*", paragraph):
        start = len(paragraph[:match.start()].replace("*", ""))
        tag = "strong" if match[0].startswith("**") else "em"
        emphasis.append((index, tag, start, start + len(match[0].strip("*"))))

heading = title.removeprefix("# ")
for path in [ROOT / "docs/index.html", *(Path(arg) for arg in sys.argv[1:])]:
    if path.suffix == ".json":
        blocks = json.loads(path.read_text(encoding="utf-8"))
        if blocks != expected:
            raise SystemExit(f"Chrome-rendered text mismatch: {path}")
    else:
        rendered = EssayHTML()
        rendered.feed(path.read_text(encoding="utf-8"))
        if ("".join(rendered.title) != heading
                or "".join(rendered.document_title) != f"{heading} — Merary Rodríguez"
                or rendered.blocks != expected or rendered.emphasis != emphasis):
            raise SystemExit(f"Rendered essay mismatch: {path}")
    print(f"{path.name}: 86 paragraphs and 4 separators match the canonical source")

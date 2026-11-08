"""Render the canonical essay into the static literary site."""
from hashlib import sha256
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / "essay.md").read_bytes()
lock = json.loads((ROOT / "source-integrity.json").read_text())
if sha256(source).hexdigest() != lock["sha256"]:
    raise SystemExit("The approved essay has changed.")
title, *paragraphs = source.decode("utf-8").strip().split("\n\n")
assert title == "# You Are Not Only the Observer"

styles = {
    0: "lead", 5: "trust", 7: "trap", 8: "afterimage", 9: "recognition-line",
    12: "chapter-lead", 13: "territory", 19: "statement meaning-line", 24: "chapter-lead",
    29: "pivot", 38: "statement world-pivot", 42: "statement participant-line", 48: "pivot",
    50: "chapter-lead", 53: "pivot", 62: "forest-line", 63: "forest-line",
    64: "forest-line forest-release", 66: "chapter-lead", 75: "statement alarm-line",
    79: "light-line", 81: "chapter-lead", 88: "world-remains", 89: "final-question",
}


def paragraph(index):
    if paragraphs[index] == "---":
        return f'<hr data-source="{index}">'
    text = escape(paragraphs[index], quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    if index == 7:
        text = text.replace("a trap.", "<span>a trap.</span>")
    if index == 9:
        text = text.replace("<strong>", "<strong><span>").replace(
            "trap. The", "trap.</span> <span>The"
        ).replace("</strong>", "</span></strong>")
    if index in (42, 89):
        cue = {42: "you are already", 89: "you'll wonder"}[index]
        text = text.replace(cue, "<span>" + cue).replace("</strong>", "</span></strong>")
    if index == 75:
        text = text.replace("may be an alarm", "<span>may be an alarm</span>")
    style = f' class="{styles[index]}"' if index in styles else ""
    return f'<p data-source="{index}"{style}>{text}</p>'


page = (ROOT / "template.html").read_text(encoding="utf-8")
for name, indices in {
    "opening": range(5),
    "interruption": range(5, 6),
    "approach": range(6, 7),
    "reversal": range(7, 9),
    "recognition": range(9, 12),
    "birdsong": range(12, 24),
    "umwelt_arrival": range(24, 31),
    "senses": range(31, 37),
    "umwelt": range(37, 49),
    "decay": range(49, 62),
    "forest": range(62, 65),
    "ocean": range(65, 79),
    "ocean_pause": range(79, 80),
    "return": range(80, 88),
    "final": range(88, 90),
}.items():
    page = page.replace("{{" + name + "}}", "\n          ".join(map(paragraph, indices)))
(ROOT / "docs/index.html").write_text(page, encoding="utf-8", newline="\n")

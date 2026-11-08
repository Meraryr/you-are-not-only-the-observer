"""Write or check the release's deterministic SHA-256 inventory."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "release-manifest.json"
SOURCES = (
    ".gitattributes", ".gitignore", "ATTRIBUTION.md", "README.md", "build.py", "essay.md",
    "release_manifest.py", "source-integrity.json", "template.html", "verify.py",
)


def inventory(paths):
    records = []
    for path in sorted(paths):
        data = path.read_bytes()
        records.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": len(data),
            "sha256": sha256(data).hexdigest(),
        })
    return records


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
data = {
    "project": "Meraryr/you-are-not-only-the-observer",
    "publish_root": "docs",
    "sources": inventory(ROOT / name for name in SOURCES),
    "production": inventory(path for path in (ROOT / "docs").rglob("*") if path.is_file()),
}
rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
if args.check:
    if MANIFEST.read_text(encoding="utf-8") != rendered:
        raise SystemExit("Release manifest mismatch")
    print("Release manifest verified")
else:
    MANIFEST.write_text(rendered, encoding="utf-8")

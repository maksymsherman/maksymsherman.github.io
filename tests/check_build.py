#!/usr/bin/env python3
"""
Build-output checker for Hugo static site.

Checks:
  2. Front matter completeness  - all posts have title, date, description
  3. JSON-LD validity           - all <script type="application/ld+json"> blocks parse as JSON
  4. Markdown alternates        - every public/p/*/ has both index.html and index.md
  5. RSS feed coverage          - public/index.xml has an <item> for every post
  6. OG share image existence   - static/images/share/{slug}.png exists for every post

Checks 2 and 6 run on source files only (no build required).
Checks 3, 4, and 5 require a built public/ directory.

Usage:
    python3 tests/check_build.py [--public PUBLIC_DIR] [--content CONTENT_DIR] [--static STATIC_DIR]

Defaults (relative to repo root):
    PUBLIC_DIR  = hugo-site/public
    CONTENT_DIR = hugo-site/content/posts
    STATIC_DIR  = hugo-site/static
"""

import sys
import re
import json
import argparse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


SEP = "=" * 60

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def get_post_slugs(content_posts_dir: Path) -> list:
    """Return sorted list of post slugs (filename stems, excluding _index)."""
    return sorted(
        f.stem
        for f in content_posts_dir.glob("*.md")
        if f.name != "_index.md"
    )


# ---------------------------------------------------------------------------
# Check 2: Front matter completeness
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ("title", "date", "description")
FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _parse_front_matter(text: str) -> dict:
    """Extract key: value pairs from YAML front matter. Simple regex-based."""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    return fields


def check_front_matter(content_posts_dir: Path):
    """Verify every post has title, date, and description in front matter."""
    failures = []
    for md_file in sorted(content_posts_dir.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            failures.append({"file": md_file.name, "missing": ["(unreadable)"]})
            continue
        fields = _parse_front_matter(text)
        missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
        if missing:
            failures.append({"file": md_file.name, "missing": missing})
    return failures


# ---------------------------------------------------------------------------
# Check 3: JSON-LD validity
# ---------------------------------------------------------------------------

class JsonLdCollector(HTMLParser):
    """Extract content of all <script type="application/ld+json"> tags."""

    def __init__(self):
        super().__init__()
        self._in_jsonld = False
        self._buf = []
        self.blocks = []  # list of (raw_text,)

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attrs_dict = dict(attrs)
            if attrs_dict.get("type", "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._buf = []

    def handle_endtag(self, tag):
        if tag == "script" and self._in_jsonld:
            self.blocks.append("".join(self._buf).strip())
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_jsonld:
            self._buf.append(data)


def check_jsonld(public_root: Path):
    """Parse all JSON-LD blocks in public/ HTML and report invalid JSON."""
    failures = []
    for html_file in sorted(public_root.rglob("*.html")):
        try:
            text = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        collector = JsonLdCollector()
        collector.feed(text)
        for i, block in enumerate(collector.blocks, 1):
            if not block:
                continue
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                failures.append({
                    "file": str(html_file.relative_to(public_root)),
                    "block": i,
                    "error": str(e),
                    "snippet": block[:120].replace("\n", " "),
                })
    return failures


# ---------------------------------------------------------------------------
# Check 4: Markdown alternates exist
# ---------------------------------------------------------------------------

def check_markdown_alternates(public_root: Path):
    """Every Hugo-generated page under public/p/*/ must have both index.html and index.md.

    Directories that have no index.html (e.g. static asset dirs like /p/images/, /p/pdfs/)
    are skipped — they are not Hugo-generated pages.
    """
    failures = []
    posts_dir = public_root / "p"
    if not posts_dir.is_dir():
        return [{"slug": "(public/p/ missing)", "missing": ["index.html", "index.md"]}]

    for slug_dir in sorted(posts_dir.iterdir()):
        if not slug_dir.is_dir():
            continue
        # Skip non-page directories (static assets like /p/images/, /p/pdfs/)
        if not (slug_dir / "index.html").is_file():
            continue
        if not (slug_dir / "index.md").is_file():
            failures.append({"slug": slug_dir.name, "missing": ["index.md"]})
    return failures


# ---------------------------------------------------------------------------
# Check 5: RSS feed coverage
# ---------------------------------------------------------------------------

RSS_NS = {"atom": "http://www.w3.org/2005/Atom"}


def check_rss_coverage(public_root: Path, content_posts_dir: Path):
    """RSS feed must have a /p/ item for every post in content/posts/.

    The RSS feed also contains non-post pages (blog, books, articles, etc.),
    so we filter to only items whose <link> contains /p/ before counting.
    """
    rss_file = public_root / "index.xml"
    if not rss_file.is_file():
        return [{"error": "public/index.xml not found"}]

    try:
        tree = ET.parse(rss_file)
    except ET.ParseError as e:
        return [{"error": f"RSS XML parse error: {e}"}]

    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        return [{"error": "RSS <channel> element not found"}]

    # Count only items whose <link> is a blog post URL (/p/...)
    post_items = [
        item for item in channel.findall("item")
        if "/p/" in (item.findtext("link") or "")
    ]
    rss_count = len(post_items)

    expected_count = sum(
        1 for f in content_posts_dir.glob("*.md")
        if f.name != "_index.md"
    )

    if rss_count == expected_count:
        return []

    return [{
        "rss_count": rss_count,
        "expected_count": expected_count,
        "detail": (
            f"RSS has {rss_count} post items (/p/ links) "
            f"but {expected_count} post files exist in content/posts/"
        ),
    }]


# ---------------------------------------------------------------------------
# Check 6: OG share image existence
# ---------------------------------------------------------------------------

def check_og_images(content_posts_dir: Path, static_dir: Path):
    """Every post slug must have a corresponding static/images/share/{slug}.png."""
    share_dir = static_dir / "images" / "share"
    failures = []
    for slug in get_post_slugs(content_posts_dir):
        expected = share_dir / f"{slug}.png"
        if not expected.is_file():
            failures.append({
                "slug": slug,
                "expected": str(expected),
            })
    return failures


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _header(title: str):
    print()
    print(SEP)
    print(f"  {title}")
    print(SEP)


def report_front_matter(failures):
    _header("CHECK 2: Front Matter Completeness")
    if not failures:
        print()
        print("  PASS  All posts have title, date, and description.")
        return True
    print()
    print(f"  FAIL  {len(failures)} post(s) missing required front matter:")
    for f in failures:
        print()
        print(f"    File:    {f['file']}")
        print(f"    Missing: {', '.join(f['missing'])}")
    return False


def report_jsonld(failures):
    _header("CHECK 3: JSON-LD Validity")
    if not failures:
        print()
        print("  PASS  All JSON-LD blocks are valid JSON.")
        return True
    print()
    print(f"  FAIL  {len(failures)} invalid JSON-LD block(s) found:")
    for f in failures:
        print()
        print(f"    File:    {f['file']}")
        print(f"    Block:   #{f['block']}")
        print(f"    Error:   {f['error']}")
        print(f"    Snippet: {f['snippet']}")
    return False


def report_markdown_alternates(failures):
    _header("CHECK 4: Markdown Alternates Exist")
    if not failures:
        print()
        print("  PASS  All posts have both index.html and index.md.")
        return True
    print()
    print(f"  FAIL  {len(failures)} post(s) missing alternate files:")
    for f in failures:
        print()
        print(f"    Slug:    /p/{f['slug']}/")
        print(f"    Missing: {', '.join(f['missing'])}")
    return False


def report_rss(failures):
    _header("CHECK 5: RSS Feed Coverage")
    if not failures:
        print()
        print("  PASS  RSS feed item count matches post count.")
        return True
    print()
    print(f"  FAIL  RSS coverage mismatch:")
    for f in failures:
        if "error" in f:
            print(f"    Error: {f['error']}")
        else:
            print(f"    {f['detail']}")
    return False


def report_og_images(failures):
    _header("CHECK 6: OG Share Image Existence")
    if not failures:
        print()
        print("  PASS  All posts have a share image in static/images/share/.")
        return True
    print()
    print(f"  FAIL  {len(failures)} post(s) missing OG share image:")
    for f in failures:
        print()
        print(f"    Slug:     /p/{f['slug']}")
        print(f"    Expected: {f['expected']}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Hugo site build checker")
    parser.add_argument(
        "--public",
        default="hugo-site/public",
        help="Path to Hugo public/ output directory (default: hugo-site/public)",
    )
    parser.add_argument(
        "--content",
        default="hugo-site/content/posts",
        help="Path to Hugo content/posts/ directory (default: hugo-site/content/posts)",
    )
    parser.add_argument(
        "--static",
        default="hugo-site/static",
        help="Path to Hugo static/ directory (default: hugo-site/static)",
    )
    args = parser.parse_args()

    public_root = Path(args.public).resolve()
    content_posts_dir = Path(args.content).resolve()
    static_dir = Path(args.static).resolve()

    if not content_posts_dir.is_dir():
        print(f"ERROR: content/posts directory not found: {content_posts_dir}", file=sys.stderr)
        sys.exit(2)

    if not static_dir.is_dir():
        print(f"ERROR: static directory not found: {static_dir}", file=sys.stderr)
        sys.exit(2)

    needs_public = True
    if not public_root.is_dir():
        print(f"WARNING: public/ directory not found: {public_root}", file=sys.stderr)
        print("  Checks 3, 4, 5 will be skipped. Run 'hugo' first to enable them.", file=sys.stderr)
        needs_public = False

    print("Hugo site build checker")
    print(f"  Public dir:  {public_root}")
    print(f"  Content dir: {content_posts_dir}")
    print(f"  Static dir:  {static_dir}")

    results = {}

    # Checks that don't need public/
    results["front_matter"] = report_front_matter(check_front_matter(content_posts_dir))
    results["og_images"] = report_og_images(check_og_images(content_posts_dir, static_dir))

    # Checks that need public/
    if needs_public:
        results["jsonld"] = report_jsonld(check_jsonld(public_root))
        results["markdown_alternates"] = report_markdown_alternates(check_markdown_alternates(public_root))
        results["rss"] = report_rss(check_rss_coverage(public_root, content_posts_dir))
    else:
        print()
        print(SEP)
        print("  CHECKS 3, 4, 5: Skipped (public/ not found)")
        print(SEP)
        results["jsonld"] = None
        results["markdown_alternates"] = None
        results["rss"] = None

    # Summary
    print()
    print(SEP)
    print("  SUMMARY")
    print(SEP)
    labels = {
        "front_matter": "Front matter completeness",
        "jsonld":        "JSON-LD validity          ",
        "markdown_alternates": "Markdown alternates       ",
        "rss":           "RSS feed coverage         ",
        "og_images":     "OG share images           ",
    }
    all_ok = True
    for key, label in labels.items():
        val = results[key]
        status = "PASS" if val is True else ("SKIP" if val is None else "FAIL")
        if val is False:
            all_ok = False
        print(f"  {label}: {status}")

    print()
    if all_ok:
        print("  All checks passed.")
        sys.exit(0)
    else:
        print("  One or more checks failed. See details above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

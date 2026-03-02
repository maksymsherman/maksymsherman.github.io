#!/usr/bin/env python3
"""
Build-output checker for Hugo static site.

Checks:
  2.  Front matter completeness  - all posts have title, date, description
  3.  JSON-LD validity           - all <script type="application/ld+json"> blocks parse as JSON
  4.  Markdown alternates        - every public/p/*/ has both index.html and index.md
  5.  RSS feed coverage          - public/index.xml has an <item> for every post
  6.  OG share image existence   - static/images/share/{slug}.png exists for every post
  7.  Canonical URL consistency  - <link rel="canonical"> matches expected URL from file path
  8.  No empty post bodies       - public/p/*/index.html files are above a minimum size
  9.  Alias redirect validity    - alias .html redirect targets exist in public/
  10. No duplicate slugs/titles  - post filenames and titles are unique
  11. OG image dimensions        - share PNGs are 1200x630 as declared in meta tags
  12. Sitemap completeness       - public/sitemap.xml has a <loc> for every post

Checks 2, 6, 10, 11 run on source/static files only (no build required).
Checks 3-5 and 7-9 and 12 require a built public/ directory.

Usage:
    python3 tests/check_build.py [--public DIR] [--content DIR] [--static DIR] [--hugo-config FILE]

Defaults (relative to repo root):
    --public       hugo-site/public
    --content      hugo-site/content/posts
    --static       hugo-site/static
    --hugo-config  hugo-site/hugo.toml
"""

import sys
import re
import json
import struct
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


BASE_URL_RE = re.compile(r"""^baseURL\s*=\s*['"]([^'"]+)['"]""", re.MULTILINE)

def read_base_url(hugo_config: Path) -> str:
    """Extract baseURL from hugo.toml. Returns 'https://msherman.xyz/' as fallback."""
    try:
        text = hugo_config.read_text(encoding="utf-8")
        m = BASE_URL_RE.search(text)
        if m:
            url = m.group(1)
            return url if url.endswith("/") else url + "/"
    except OSError:
        pass
    return "https://msherman.xyz/"


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
        self.blocks = []

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

    Directories with no index.html (static asset dirs like /p/images/, /p/pdfs/)
    are skipped — they are not Hugo-generated pages.
    """
    failures = []
    posts_dir = public_root / "p"
    if not posts_dir.is_dir():
        return [{"slug": "(public/p/ missing)", "missing": ["index.html", "index.md"]}]

    for slug_dir in sorted(posts_dir.iterdir()):
        if not slug_dir.is_dir():
            continue
        if not (slug_dir / "index.html").is_file():
            continue  # static asset directory, not a page
        if not (slug_dir / "index.md").is_file():
            failures.append({"slug": slug_dir.name, "missing": ["index.md"]})
    return failures


# ---------------------------------------------------------------------------
# Check 5: RSS feed coverage
# ---------------------------------------------------------------------------

def check_rss_coverage(public_root: Path, content_posts_dir: Path):
    """RSS feed must have a /p/ item for every post in content/posts/.

    The feed also includes non-post pages so we filter to /p/ links only.
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
            failures.append({"slug": slug, "expected": str(expected)})
    return failures


# ---------------------------------------------------------------------------
# Check 7: Canonical URL consistency
# ---------------------------------------------------------------------------

class CanonicalParser(HTMLParser):
    """Extract the href value from <link rel="canonical">."""

    def __init__(self):
        super().__init__()
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        if tag == "link":
            attrs_dict = dict(attrs)
            if attrs_dict.get("rel") == "canonical":
                self.canonical = attrs_dict.get("href")


def check_canonical_urls(public_root: Path, base_url: str):
    """Verify <link rel="canonical"> in each index.html matches the expected URL.

    Expected URL is derived from the file's path within public/:
        public/index.html          -> {base_url}
        public/blog/index.html     -> {base_url}blog/
        public/p/unpredictable/index.html -> {base_url}p/unpredictable/
    """
    failures = []
    for html_file in sorted(public_root.rglob("index.html")):
        try:
            text = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        parser = CanonicalParser()
        parser.feed(text)
        actual = parser.canonical
        if not actual:
            continue  # no canonical tag (e.g. alias redirect files don't have one)

        # Derive expected URL from file path
        rel = html_file.parent.relative_to(public_root)
        expected = base_url + (str(rel).replace("\\", "/") + "/" if str(rel) != "." else "")

        if actual.rstrip("/") != expected.rstrip("/"):
            failures.append({
                "file": str(html_file.relative_to(public_root)),
                "expected": expected,
                "actual": actual,
            })
    return failures


# ---------------------------------------------------------------------------
# Check 8: No empty post bodies
# ---------------------------------------------------------------------------

# Smallest real post is ~7KB; a silently-empty page is <1KB.
# Threshold set at 3KB to give ample headroom.
MIN_POST_SIZE_BYTES = 3072


def check_empty_posts(public_root: Path):
    """Blog post HTML files must be above a minimum size.

    An empty or near-empty page indicates a silent template failure.
    Only checks public/p/*/index.html (blog post pages).
    """
    failures = []
    posts_dir = public_root / "p"
    if not posts_dir.is_dir():
        return []

    for slug_dir in sorted(posts_dir.iterdir()):
        if not slug_dir.is_dir():
            continue
        index = slug_dir / "index.html"
        if not index.is_file():
            continue
        size = index.stat().st_size
        if size < MIN_POST_SIZE_BYTES:
            failures.append({
                "slug": slug_dir.name,
                "size": size,
                "minimum": MIN_POST_SIZE_BYTES,
            })
    return failures


# ---------------------------------------------------------------------------
# Check 9: Alias redirect validity
# ---------------------------------------------------------------------------

class RedirectParser(HTMLParser):
    """Extract redirect URL from <meta http-equiv="refresh" content="0; url=...">."""

    def __init__(self):
        super().__init__()
        self.redirect_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("http-equiv", "").lower() == "refresh":
                content = attrs_dict.get("content", "")
                m = re.search(r"url=(.+)", content, re.IGNORECASE)
                if m:
                    self.redirect_url = m.group(1).strip()


def _url_to_public_path(url: str, base_url: str, public_root: Path):
    """Convert an absolute URL to a Path inside public_root, or None if external."""
    if not url.startswith(base_url):
        return None
    rel = url[len(base_url):].lstrip("/")
    return public_root / rel if rel else public_root


def check_alias_redirects(public_root: Path, base_url: str):
    """Alias .html files must redirect to URLs that exist in public/.

    Hugo creates alias files like public/p/unpredictable.html with a
    meta-refresh redirect. If the redirect target was mistyped it becomes
    a permanent broken redirect.
    """
    failures = []
    for html_file in sorted(public_root.rglob("*.html")):
        # Alias files are named like slug.html directly in a directory,
        # not as index.html. Skip index.html files.
        if html_file.name == "index.html":
            continue
        try:
            text = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        parser = RedirectParser()
        parser.feed(text)
        url = parser.redirect_url
        if not url:
            continue  # not a redirect file

        target = _url_to_public_path(url, base_url, public_root)
        if target is None:
            continue  # external redirect, skip

        # Target must exist as a file or directory with index.html
        exists = (
            target.is_file()
            or (target / "index.html").is_file()
        )
        if not exists:
            failures.append({
                "file": str(html_file.relative_to(public_root)),
                "redirect_url": url,
                "expected_path": str(target),
            })
    return failures


# ---------------------------------------------------------------------------
# Check 10: No duplicate slugs or titles
# ---------------------------------------------------------------------------

def check_duplicates(content_posts_dir: Path):
    """Post filenames (slugs) and titles must be unique (case-insensitive)."""
    failures = []
    slugs_seen = {}   # lowercase slug -> original filename
    titles_seen = {}  # lowercase title -> original filename

    for md_file in sorted(content_posts_dir.glob("*.md")):
        if md_file.name == "_index.md":
            continue

        slug_lower = md_file.stem.lower()
        if slug_lower in slugs_seen:
            failures.append({
                "type": "slug",
                "value": md_file.stem,
                "file1": slugs_seen[slug_lower],
                "file2": md_file.name,
            })
        else:
            slugs_seen[slug_lower] = md_file.name

        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        fields = _parse_front_matter(text)
        title = fields.get("title", "").strip('"\'')
        if not title:
            continue

        title_lower = title.lower()
        if title_lower in titles_seen:
            failures.append({
                "type": "title",
                "value": title,
                "file1": titles_seen[title_lower],
                "file2": md_file.name,
            })
        else:
            titles_seen[title_lower] = md_file.name

    return failures


# ---------------------------------------------------------------------------
# Check 11: OG image dimensions
# ---------------------------------------------------------------------------

EXPECTED_OG_WIDTH = 1200
EXPECTED_OG_HEIGHT = 630


def _read_png_dimensions(path: Path):
    """Read width and height from a PNG file header. Returns (w, h) or None."""
    try:
        with open(path, "rb") as f:
            header = f.read(24)
        if len(header) < 24:
            return None
        # PNG signature: 8 bytes, IHDR chunk: 4 len + 4 type + 4 width + 4 height
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        w, h = struct.unpack(">II", header[16:24])
        return w, h
    except OSError:
        return None


def check_og_image_dimensions(static_dir: Path):
    """All PNG files in static/images/share/ must be 1200x630."""
    share_dir = static_dir / "images" / "share"
    if not share_dir.is_dir():
        return [{"error": "static/images/share/ directory not found"}]

    failures = []
    for png_file in sorted(share_dir.glob("*.png")):
        dims = _read_png_dimensions(png_file)
        if dims is None:
            failures.append({
                "file": png_file.name,
                "error": "could not read PNG dimensions",
            })
            continue
        w, h = dims
        if w != EXPECTED_OG_WIDTH or h != EXPECTED_OG_HEIGHT:
            failures.append({
                "file": png_file.name,
                "actual": f"{w}x{h}",
                "expected": f"{EXPECTED_OG_WIDTH}x{EXPECTED_OG_HEIGHT}",
            })
    return failures


# ---------------------------------------------------------------------------
# Check 12: Sitemap completeness
# ---------------------------------------------------------------------------

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def check_sitemap(public_root: Path, content_posts_dir: Path):
    """public/sitemap.xml must contain a <loc> for every built post page.

    Uses actual public/p/*/ directory names as the source of truth rather than
    content filenames, because Hugo normalises some slugs (e.g. removes
    parentheses from soulbound(less)-tokens -> soulboundless-tokens).
    """
    sitemap_file = public_root / "sitemap.xml"
    if not sitemap_file.is_file():
        return [{"error": "public/sitemap.xml not found"}]

    try:
        tree = ET.parse(sitemap_file)
    except ET.ParseError as e:
        return [{"error": f"Sitemap XML parse error: {e}"}]

    root = tree.getroot()
    locs = set()
    for url_el in root.iter():
        if url_el.tag in ("{http://www.sitemaps.org/schemas/sitemap/0.9}loc", "loc"):
            if url_el.text:
                locs.add(url_el.text.strip().rstrip("/"))

    # Collect built post directory names from public/p/ (these are the
    # Hugo-normalised slugs, not necessarily matching content filenames)
    posts_dir = public_root / "p"
    if not posts_dir.is_dir():
        return [{"error": "public/p/ directory not found"}]

    failures = []
    for slug_dir in sorted(posts_dir.iterdir()):
        if not slug_dir.is_dir() or not (slug_dir / "index.html").is_file():
            continue  # skip static asset directories
        built_slug = slug_dir.name
        found = any(f"/p/{built_slug}" in loc for loc in locs)
        if not found:
            failures.append({"slug": built_slug})
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
    print("  FAIL  RSS coverage mismatch:")
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


def report_canonical(failures):
    _header("CHECK 7: Canonical URL Consistency")
    if not failures:
        print()
        print("  PASS  All canonical URLs match their expected page URLs.")
        return True
    print()
    print(f"  FAIL  {len(failures)} page(s) with mismatched canonical URL:")
    for f in failures:
        print()
        print(f"    File:     {f['file']}")
        print(f"    Expected: {f['expected']}")
        print(f"    Actual:   {f['actual']}")
    return False


def report_empty_posts(failures):
    _header("CHECK 8: No Empty Post Bodies")
    if not failures:
        print()
        print(f"  PASS  All post pages are above {MIN_POST_SIZE_BYTES} bytes.")
        return True
    print()
    print(f"  FAIL  {len(failures)} post(s) suspiciously small (< {MIN_POST_SIZE_BYTES} bytes):")
    for f in failures:
        print()
        print(f"    Slug:  /p/{f['slug']}")
        print(f"    Size:  {f['size']} bytes (minimum: {f['minimum']})")
    return False


def report_alias_redirects(failures):
    _header("CHECK 9: Alias Redirect Validity")
    if not failures:
        print()
        print("  PASS  All alias redirect targets exist.")
        return True
    print()
    print(f"  FAIL  {len(failures)} alias file(s) redirect to missing pages:")
    for f in failures:
        print()
        print(f"    File:   {f['file']}")
        print(f"    URL:    {f['redirect_url']}")
        print(f"    Target: {f['expected_path']}")
    return False


def report_duplicates(failures):
    _header("CHECK 10: No Duplicate Slugs or Titles")
    if not failures:
        print()
        print("  PASS  All post slugs and titles are unique.")
        return True
    print()
    print(f"  FAIL  {len(failures)} duplicate(s) found:")
    for f in failures:
        print()
        print(f"    Type:  {f['type']}")
        print(f"    Value: {f['value']}")
        print(f"    Files: {f['file1']}  vs  {f['file2']}")
    return False


def report_og_dimensions(failures):
    _header("CHECK 11: OG Image Dimensions")
    if not failures:
        print()
        print(f"  PASS  All share images are {EXPECTED_OG_WIDTH}x{EXPECTED_OG_HEIGHT}.")
        return True
    print()
    print(f"  FAIL  {len(failures)} image(s) with wrong dimensions:")
    for f in failures:
        print()
        print(f"    File:     {f['file']}")
        if "error" in f:
            print(f"    Error:    {f['error']}")
        else:
            print(f"    Actual:   {f['actual']}")
            print(f"    Expected: {f['expected']}")
    return False


def report_sitemap(failures):
    _header("CHECK 12: Sitemap Completeness")
    if not failures:
        print()
        print("  PASS  All posts appear in sitemap.xml.")
        return True
    print()
    print(f"  FAIL  {len(failures)} post(s) missing from sitemap:")
    for f in failures:
        if "error" in f:
            print(f"    Error: {f['error']}")
        else:
            print()
            print(f"    Slug: /p/{f['slug']}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Hugo site build checker")
    parser.add_argument("--public", default="hugo-site/public")
    parser.add_argument("--content", default="hugo-site/content/posts")
    parser.add_argument("--static", default="hugo-site/static")
    parser.add_argument("--hugo-config", default="hugo-site/hugo.toml")
    args = parser.parse_args()

    public_root = Path(args.public).resolve()
    content_posts_dir = Path(args.content).resolve()
    static_dir = Path(args.static).resolve()
    hugo_config = Path(args.hugo_config).resolve()

    for label, path in [
        ("content/posts", content_posts_dir),
        ("static", static_dir),
    ]:
        if not path.is_dir():
            print(f"ERROR: {label} directory not found: {path}", file=sys.stderr)
            sys.exit(2)

    needs_public = public_root.is_dir()
    if not needs_public:
        print(f"WARNING: public/ not found: {public_root}", file=sys.stderr)
        print("  Checks 3-5 and 7-9 and 12 skipped. Run 'hugo' first.", file=sys.stderr)

    base_url = read_base_url(hugo_config)

    print("Hugo site build checker")
    print(f"  Public dir:  {public_root}")
    print(f"  Content dir: {content_posts_dir}")
    print(f"  Static dir:  {static_dir}")
    print(f"  Base URL:    {base_url}")

    results = {}

    # Source-only checks (no public/ needed)
    results["front_matter"] = report_front_matter(check_front_matter(content_posts_dir))
    results["og_images"] = report_og_images(check_og_images(content_posts_dir, static_dir))
    results["duplicates"] = report_duplicates(check_duplicates(content_posts_dir))
    results["og_dimensions"] = report_og_dimensions(check_og_image_dimensions(static_dir))

    # Build-output checks (need public/)
    if needs_public:
        results["jsonld"] = report_jsonld(check_jsonld(public_root))
        results["markdown_alternates"] = report_markdown_alternates(check_markdown_alternates(public_root))
        results["rss"] = report_rss(check_rss_coverage(public_root, content_posts_dir))
        results["canonical"] = report_canonical(check_canonical_urls(public_root, base_url))
        results["empty_posts"] = report_empty_posts(check_empty_posts(public_root))
        results["alias_redirects"] = report_alias_redirects(check_alias_redirects(public_root, base_url))
        results["sitemap"] = report_sitemap(check_sitemap(public_root, content_posts_dir))
    else:
        skipped = ["jsonld", "markdown_alternates", "rss", "canonical",
                   "empty_posts", "alias_redirects", "sitemap"]
        print()
        print(SEP)
        print("  CHECKS 3-5, 7-9, 12: Skipped (public/ not found)")
        print(SEP)
        for k in skipped:
            results[k] = None

    # Summary
    print()
    print(SEP)
    print("  SUMMARY")
    print(SEP)
    labels = {
        "front_matter":       "Front matter completeness",
        "jsonld":             "JSON-LD validity         ",
        "markdown_alternates":"Markdown alternates      ",
        "rss":                "RSS feed coverage        ",
        "og_images":          "OG share image existence ",
        "canonical":          "Canonical URL consistency",
        "empty_posts":        "No empty post bodies     ",
        "alias_redirects":    "Alias redirect validity  ",
        "duplicates":         "No duplicate slugs/titles",
        "og_dimensions":      "OG image dimensions      ",
        "sitemap":            "Sitemap completeness     ",
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

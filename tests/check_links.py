#!/usr/bin/env python3
"""
Link checker for Hugo static site.

Checks:
1. Internal link checker - all href links in public/ HTML files resolve to real files
2. Blog coverage check - every content/posts/*.md has a /p/{slug} link in blog/index.html

Usage:
    python3 tests/check_links.py [--public PUBLIC_DIR] [--content CONTENT_DIR]

Defaults (relative to repo root):
    PUBLIC_DIR  = hugo-site/public
    CONTENT_DIR = hugo-site/content/posts
"""

import sys
import argparse
from html.parser import HTMLParser
from pathlib import Path


# ---------------------------------------------------------------------------
# HTML link extraction
# ---------------------------------------------------------------------------

class HrefCollector(HTMLParser):
    """Collect all href attribute values from any HTML tag."""

    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        for attr, val in attrs:
            if attr == "href" and val:
                self.hrefs.append(val)


def extract_hrefs(html_text: str) -> list:
    collector = HrefCollector()
    collector.feed(html_text)
    return collector.hrefs


# ---------------------------------------------------------------------------
# Link resolution
# ---------------------------------------------------------------------------

SKIP_SCHEMES = ("http://", "https://", "mailto:", "javascript:", "data:", "ftp://")


def resolve_link(link: str, source_file: Path, public_root: Path):
    """
    Resolve an href value to a filesystem path in public_root.
    Returns (exists: bool, reason: str).

    Resolution order (mirrors GitHub Pages static server):
      1. Exact file:           public_root / path
      2. Directory index.html: public_root / path / index.html
      3. HTML redirect file:   public_root / path + ".html"
    """
    # Strip fragment and query string
    link = link.split("#")[0].split("?")[0]

    # Nothing left after stripping (was a fragment-only link like "#top")
    if not link:
        return True, "skip_fragment_only"

    for scheme in SKIP_SCHEMES:
        if link.startswith(scheme):
            return True, "skip_external"

    # Resolve to a Path inside public_root
    if link.startswith("/"):
        rel = link.lstrip("/")
        candidate = public_root / rel if rel else public_root
    else:
        # Relative link: resolve from the directory of the source file
        candidate = (source_file.parent / link).resolve()
        # Guard against path traversal outside public_root
        try:
            candidate.relative_to(public_root.resolve())
        except ValueError:
            return False, "path_traversal"

    # Tier 1: exact file (CSS, PDFs, images, .html redirect aliases)
    if candidate.is_file():
        return True, "ok_file"

    # Tier 2: clean URL -> directory index.html
    if (candidate / "index.html").is_file():
        return True, "ok_dir_index"

    # Tier 3: Hugo alias redirect file (e.g. /p/soulbound(less)-tokens.html)
    if candidate.with_suffix(".html").is_file():
        return True, "ok_html_redirect"

    return False, "missing"


# ---------------------------------------------------------------------------
# Check 1: Internal link checker
# ---------------------------------------------------------------------------

def check_internal_links(public_root: Path):
    """
    Walk all .html files in public_root.
    Extract all href attributes, skip external/mailto/etc.
    Verify each internal link resolves on the filesystem.

    Returns (failures: list[dict], stats: dict).
    """
    failures = []
    stats = {"files": 0, "links_checked": 0, "skipped": 0}

    for html_file in sorted(public_root.rglob("*.html")):
        stats["files"] += 1
        try:
            text = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for href in extract_hrefs(text):
            ok, reason = resolve_link(href, html_file, public_root)
            if reason.startswith("skip"):
                stats["skipped"] += 1
                continue
            stats["links_checked"] += 1
            if not ok:
                failures.append({
                    "source": str(html_file.relative_to(public_root)),
                    "link": href,
                })

    return failures, stats


# ---------------------------------------------------------------------------
# Check 2: Blog coverage checker
# ---------------------------------------------------------------------------

def check_blog_coverage(content_posts_dir: Path, public_root: Path):
    """
    Verify every content/posts/*.md file (except _index.md) has a
    corresponding /p/{slug} link in public/blog/index.html.

    Uses content filenames as the source of truth for slugs, matching
    the permalink pattern `posts = '/p/:contentbasename'` in hugo.toml.

    Returns failures: list[dict].
    """
    # Collect expected slugs from content filenames
    expected_slugs = set()
    for md_file in content_posts_dir.glob("*.md"):
        if md_file.name == "_index.md":
            continue
        expected_slugs.add(md_file.stem)  # filename without .md

    # Parse blog/index.html for /p/{slug} links
    blog_index = public_root / "blog" / "index.html"
    if not blog_index.is_file():
        return [{"slug": "(blog page missing)", "content_file": str(blog_index)}]

    text = blog_index.read_text(encoding="utf-8", errors="replace")
    linked_slugs = set()
    for href in extract_hrefs(text):
        href = href.split("#")[0].split("?")[0]
        if href.startswith("/p/"):
            slug = href[3:].rstrip("/")
            linked_slugs.add(slug)

    missing = expected_slugs - linked_slugs
    return [
        {"slug": slug, "content_file": str(content_posts_dir / (slug + ".md"))}
        for slug in sorted(missing)
    ]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEP = "=" * 60


def report_link_failures(failures, stats):
    print()
    print(SEP)
    print("  CHECK 1: Internal Link Checker")
    print(SEP)
    print(f"  Scanned:       {stats['files']} HTML files")
    print(f"  Links checked: {stats['links_checked']} internal links")
    print(f"  Skipped:       {stats['skipped']} external/mailto/fragment-only links")

    if not failures:
        print()
        print("  PASS  No broken internal links found.")
        return True

    print()
    print(f"  FAIL  {len(failures)} broken link(s) found:")
    for f in failures:
        print()
        print(f"    Source: {f['source']}")
        print(f"    Link:   {f['link']}")
    return False


def report_coverage_failures(failures):
    print()
    print(SEP)
    print("  CHECK 2: Blog Coverage")
    print(SEP)

    if not failures:
        print()
        print("  PASS  All posts have a link in blog/index.html.")
        return True

    print()
    print(f"  FAIL  {len(failures)} post(s) missing from blog listing:")
    for f in failures:
        print()
        print(f"    Slug:   /p/{f['slug']}")
        print(f"    File:   {f['content_file']}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Hugo site link checker")
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
    args = parser.parse_args()

    public_root = Path(args.public).resolve()
    content_posts_dir = Path(args.content).resolve()

    if not public_root.is_dir():
        print(f"ERROR: public directory not found: {public_root}", file=sys.stderr)
        print("  Did you run 'hugo' first?", file=sys.stderr)
        sys.exit(2)

    if not content_posts_dir.is_dir():
        print(f"ERROR: content/posts directory not found: {content_posts_dir}", file=sys.stderr)
        sys.exit(2)

    print("Hugo site link checker")
    print(f"  Public dir:  {public_root}")
    print(f"  Content dir: {content_posts_dir}")

    link_failures, stats = check_internal_links(public_root)
    coverage_failures = check_blog_coverage(content_posts_dir, public_root)

    link_ok = report_link_failures(link_failures, stats)
    coverage_ok = report_coverage_failures(coverage_failures)

    print()
    print(SEP)
    print("  SUMMARY")
    print(SEP)
    print(f"  Link checker:   {'PASS' if link_ok else 'FAIL'}")
    print(f"  Blog coverage:  {'PASS' if coverage_ok else 'FAIL'}")
    print()

    if link_ok and coverage_ok:
        print("  All checks passed.")
        sys.exit(0)
    else:
        print("  One or more checks failed. See details above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

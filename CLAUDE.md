# Known Differences: HTML-to-Markdown Conversion

The `transition-to-markdown` branch converts all content files from `.html` to `.md`. The following minor rendering differences exist between the `main` branch (HTML) and `transition-to-markdown` branch (Markdown) output. None affect readability or layout.

## Curly Quotes to Straight Quotes

Some curly/smart quotes (`'` `'` `"` `"`) in the original HTML were converted to straight quotes (`'` `"`) during the Markdown conversion. Affects ~5 files: `some-thoughts`, `striking_while_the_iron_is_hot`, `live-nation`, `boi-favorite-book`, `reasoning-by-inertia`. The visual difference is very subtle.

## `<b>` to `<strong>`

Goldmark renders `**text**` as `<strong>` instead of the original `<b>`. Visually identical. Affects `knowledge-without-explanation`, `unpredictable`, `boi-favorite-book`.

## `<div><hr /></div>` to `<hr>`

Markdown `---` renders as bare `<hr>` instead of `<div><hr /></div>`. Visually identical. Affects 6 files.

## Entity Encoding

Goldmark encodes `"` as `&quot;` in some contexts where the original HTML used literal `"`. Visually identical. Affects ~11 files.

## Heading `id` Attributes

Goldmark auto-generates `id` attributes on headings (e.g., `<h1 id="title">`). The original HTML had no heading IDs except for 4 custom IDs in `striking_while_the_iron_is_hot` (preserved with `{#id}` syntax). The auto-generated IDs are invisible and improve anchor linking.

## Trailing `&nbsp;` Removed

A few trailing non-breaking spaces (`&nbsp;`) at ends of sentences were removed during conversion. No visual impact. Affects `art-clustering-in-renaissance-florence`, `men-and-rubber`, `newsletter-publishing-platforms`, `the-known-world`.

## RSS Feed Encoding

Minor differences in entity encoding within RSS feed `<description>` elements (`&quot;` vs `&#34;`, `&#xA;` newlines). Most RSS readers handle both correctly.

## Stray `</html>` Tags Removed

Three files (`boi-favorite-book`, `soulboundless-tokens`, `unpredictable`) had extraneous `</html>` tags in the original HTML content body. These were correctly omitted in the Markdown version. This is a bug fix, not a regression.

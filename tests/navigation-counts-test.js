const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const glob = require('glob');

const PUBLIC_DIR = path.join(__dirname, '../hugo-site/public');
const CONTENT_DIR = path.join(__dirname, '../hugo-site/content/posts');

function testNavigationCounts() {
  const errors = [];

  // 1. Count actual blog posts in /content/posts/
  const actualPostFiles = glob.sync(`${CONTENT_DIR}/*.html`);
  const actualPostCount = actualPostFiles.length;

  // 2. Count blog post links in blog.html
  const blogHtml = fs.readFileSync(path.join(PUBLIC_DIR, 'blog/index.html'), 'utf-8');
  const $blog = cheerio.load(blogHtml);
  const blogLinkCount = $blog('a[href^="/p/"]').length;

  if (actualPostCount !== blogLinkCount) {
    errors.push(`Blog post count mismatch: ${actualPostCount} actual files, ${blogLinkCount} links in blog.html`);
  }

  if (actualPostCount !== 16) {
    errors.push(`Expected 16 blog posts, found ${actualPostCount}`);
  }

  // 3. Verify books page has content (using minimum threshold, not exact count)
  const booksHtml = fs.readFileSync(path.join(PUBLIC_DIR, 'books/index.html'), 'utf-8');
  const $books = cheerio.load(booksHtml);
  const bookCount = $books('li').length;
  const MIN_BOOKS = 150;

  if (bookCount < MIN_BOOKS) {
    errors.push(`Books page has fewer books than expected (found ${bookCount}, minimum ${MIN_BOOKS})`);
  }

  // 4. Verify articles page has content (using minimum threshold, not exact count)
  const articlesHtml = fs.readFileSync(path.join(PUBLIC_DIR, 'articles/index.html'), 'utf-8');
  const $articles = cheerio.load(articlesHtml);
  const articleCount = $articles('li').length;
  const MIN_ARTICLES = 60;

  if (articleCount < MIN_ARTICLES) {
    errors.push(`Articles page has fewer articles than expected (found ${articleCount}, minimum ${MIN_ARTICLES})`);
  }

  return {
    passed: errors.length === 0,
    errors,
    stats: {
      posts: actualPostCount,
      books: bookCount,
      articles: articleCount
    }
  };
}

module.exports = testNavigationCounts;

if (require.main === module) {
  const result = testNavigationCounts();
  console.log('Navigation Counts Test:', result.passed ? '✅ PASSED' : '❌ FAILED');
  console.log('Stats:', JSON.stringify(result.stats, null, 2));
  result.errors.forEach(err => console.error('  ', err));
  process.exit(result.passed ? 0 : 1);
}

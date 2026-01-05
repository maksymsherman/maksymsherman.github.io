const fs = require('fs');
const path = require('path');
const { XMLParser, XMLValidator } = require('fast-xml-parser');
const cheerio = require('cheerio');

const PUBLIC_DIR = path.join(__dirname, '../hugo-site/public');

function validateRSSFeed() {
  const errors = [];
  const rssPath = path.join(PUBLIC_DIR, 'index.xml');

  if (!fs.existsSync(rssPath)) {
    return { passed: false, errors: ['RSS feed not found at /index.xml'] };
  }

  const rssContent = fs.readFileSync(rssPath, 'utf-8');
  const validationResult = XMLValidator.validate(rssContent);

  if (validationResult !== true) {
    errors.push(`RSS feed has invalid XML: ${validationResult.err.msg}`);
    return { passed: false, errors };
  }

  const parser = new XMLParser();
  const rss = parser.parse(rssContent);

  if (!rss.rss?.channel) {
    errors.push('RSS feed missing required rss.channel structure');
  }

  const items = rss.rss?.channel?.item || [];
  const itemCount = Array.isArray(items) ? items.length : (items ? 1 : 0);

  if (itemCount < 16) {
    errors.push(`RSS feed should contain 16+ items, found ${itemCount}`);
  }

  return { passed: errors.length === 0, errors, stats: { items: itemCount } };
}

function validateSitemap() {
  const errors = [];
  const sitemapPath = path.join(PUBLIC_DIR, 'sitemap.xml');

  if (!fs.existsSync(sitemapPath)) {
    return { passed: false, errors: ['Sitemap not found at /sitemap.xml'] };
  }

  const sitemapContent = fs.readFileSync(sitemapPath, 'utf-8');
  const validationResult = XMLValidator.validate(sitemapContent);

  if (validationResult !== true) {
    errors.push(`Sitemap has invalid XML`);
    return { passed: false, errors };
  }

  const parser = new XMLParser();
  const sitemap = parser.parse(sitemapContent);

  if (!sitemap.urlset?.url) {
    errors.push('Sitemap missing required urlset.url structure');
    return { passed: false, errors };
  }

  const urls = Array.isArray(sitemap.urlset.url) ? sitemap.urlset.url : [sitemap.urlset.url];
  const postUrls = urls.filter(u => u.loc && u.loc.includes('/p/'));

  if (postUrls.length < 16) {
    errors.push(`Sitemap should contain 16+ blog post URLs, found ${postUrls.length}`);
  }

  return { passed: errors.length === 0, errors, stats: { urls: urls.length, posts: postUrls.length } };
}

function validateMetadata() {
  const errors = [];

  const homepageHtml = fs.readFileSync(path.join(PUBLIC_DIR, 'index.html'), 'utf-8');
  const $home = cheerio.load(homepageHtml);

  if (!$home('meta[name="description"]').attr('content')) {
    errors.push('Homepage missing meta description');
  }

  if (!$home('link[rel="canonical"]').attr('href')) {
    errors.push('Homepage missing canonical URL');
  }

  if (!$home('meta[property="og:title"]').attr('content')) {
    errors.push('Homepage missing OpenGraph title');
  }

  return { passed: errors.length === 0, errors };
}

module.exports = { validateRSSFeed, validateSitemap, validateMetadata };

if (require.main === module) {
  const results = {
    rss: validateRSSFeed(),
    sitemap: validateSitemap(),
    metadata: validateMetadata()
  };

  console.log('RSS Feed:', results.rss.passed ? '✅ PASSED' : '❌ FAILED');
  if (results.rss.stats) {
    console.log('  Items:', results.rss.stats.items);
  }
  results.rss.errors.forEach(err => console.error('  ', err));

  console.log('Sitemap:', results.sitemap.passed ? '✅ PASSED' : '❌ FAILED');
  if (results.sitemap.stats) {
    console.log('  URLs:', results.sitemap.stats.urls, 'Posts:', results.sitemap.stats.posts);
  }
  results.sitemap.errors.forEach(err => console.error('  ', err));

  console.log('Metadata:', results.metadata.passed ? '✅ PASSED' : '❌ FAILED');
  results.metadata.errors.forEach(err => console.error('  ', err));

  const allPassed = Object.values(results).every(r => r.passed);
  process.exit(allPassed ? 0 : 1);
}

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const glob = require('glob');

const PUBLIC_DIR = path.join(__dirname, '../hugo-site/public');

function testCSSLoading() {
  const errors = [];
  // Only check index.html files, not Hugo alias redirects
  const htmlFiles = glob.sync(`${PUBLIC_DIR}/**/index.html`)
    .concat(glob.sync(`${PUBLIC_DIR}/404.html`));

  htmlFiles.forEach(file => {
    const html = fs.readFileSync(file, 'utf-8');
    const $ = cheerio.load(html);

    const cssLinks = $('link[rel="stylesheet"]')
      .map((i, el) => $(el).attr('href'))
      .get();

    const hasShared = cssLinks.includes('/shared.css');
    const hasNotebook = cssLinks.includes('/notebook.css');
    const hasMain = cssLinks.includes('/main.css');

    const relativePath = path.relative(PUBLIC_DIR, file);
    const isBlogPost = relativePath.startsWith('p/');
    const isHomepage = relativePath === 'index.html';
    const isListPage = ['blog/index.html', 'books/index.html', 'articles/index.html',
                        'contact/index.html', 'favorite-picture/index.html'].includes(relativePath);

    // Validate shared.css is always loaded
    if (!hasShared) {
      errors.push(`${relativePath}: Missing shared.css`);
    }

    // CRITICAL: Never load both main.css and notebook.css
    if (hasMain && hasNotebook) {
      errors.push(`${relativePath}: ❌ CRITICAL - Loads BOTH main.css AND notebook.css`);
    }

    // Validate correct CSS for page type
    if (isHomepage || isListPage) {
      if (!hasNotebook) {
        errors.push(`${relativePath}: Should load notebook.css (homepage or list page)`);
      }
      if (hasMain) {
        errors.push(`${relativePath}: Should NOT load main.css (homepage or list page)`);
      }
    } else if (isBlogPost) {
      if (!hasMain) {
        errors.push(`${relativePath}: Should load main.css (blog post)`);
      }
      if (hasNotebook) {
        errors.push(`${relativePath}: Should NOT load notebook.css (blog post)`);
      }
    }
  });

  return { passed: errors.length === 0, errors };
}

module.exports = testCSSLoading;

if (require.main === module) {
  const result = testCSSLoading();
  console.log('CSS Loading Test:', result.passed ? '✅ PASSED' : '❌ FAILED');
  result.errors.forEach(err => console.error('  ', err));
  process.exit(result.passed ? 0 : 1);
}

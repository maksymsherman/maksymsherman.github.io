const cssLoadingTest = require('./css-loading-test');
const navigationCountsTest = require('./navigation-counts-test');
const codeCellFormattingTest = require('./code-cell-formatting-test');
const jsonLdValidation = require('./json-ld-validation');
const { validateRSSFeed, validateSitemap, validateMetadata } = require('./rss-sitemap-validation');

async function runAllTests() {
  console.log('🧪 Running custom validation tests...\n');

  const results = {
    cssLoading: cssLoadingTest(),
    navigationCounts: navigationCountsTest(),
    codeCellFormatting: codeCellFormattingTest(),
    jsonLd: jsonLdValidation(),
    rss: validateRSSFeed(),
    sitemap: validateSitemap(),
    metadata: validateMetadata()
  };

  console.log('\n=== Test Results ===');
  console.log('CSS Loading:', results.cssLoading.passed ? '✅ PASSED' : '❌ FAILED');
  console.log('Navigation Counts:', results.navigationCounts.passed ? '✅ PASSED' : '❌ FAILED');
  if (results.navigationCounts.stats) {
    console.log('  Posts:', results.navigationCounts.stats.posts);
    console.log('  Books:', results.navigationCounts.stats.books, '(min: 150)');
    console.log('  Articles:', results.navigationCounts.stats.articles, '(min: 60)');
  }
  console.log('Code Cell Formatting:', results.codeCellFormatting.passed ? '✅ PASSED' : '❌ FAILED');
  console.log('JSON-LD Validation:', results.jsonLd.passed ? '✅ PASSED' : '❌ FAILED');
  console.log('RSS Feed:', results.rss.passed ? '✅ PASSED' : '❌ FAILED');
  if (results.rss.stats) {
    console.log('  Items:', results.rss.stats.items);
  }
  console.log('Sitemap:', results.sitemap.passed ? '✅ PASSED' : '❌ FAILED');
  if (results.sitemap.stats) {
    console.log('  URLs:', results.sitemap.stats.urls);
  }
  console.log('Metadata:', results.metadata.passed ? '✅ PASSED' : '❌ FAILED');

  const allPassed = Object.values(results).every(r => r.passed);

  if (!allPassed) {
    console.log('\n=== Errors ===');
    Object.entries(results).forEach(([name, result]) => {
      if (!result.passed && result.errors && result.errors.length > 0) {
        console.log(`\n${name}:`);
        result.errors.forEach(err => {
          if (typeof err === 'string') {
            console.error('  ', err);
          } else if (err.file) {
            console.error('  ', err.file);
            if (err.errors) {
              err.errors.forEach(e => console.error('    -', e.message || e));
            }
            if (err.details) {
              console.error('    -', err.details);
            }
          }
        });
      }
    });
  }

  process.exit(allPassed ? 0 : 1);
}

runAllTests();

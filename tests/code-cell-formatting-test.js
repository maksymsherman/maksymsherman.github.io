const fs = require('fs');
const path = require('path');
const glob = require('glob');

const CONTENT_DIR = path.join(__dirname, '../hugo-site/content');

function testCodeCellFormatting() {
  const errors = [];
  const htmlFiles = glob.sync(`${CONTENT_DIR}/**/*.html`);

  htmlFiles.forEach(file => {
    const content = fs.readFileSync(file, 'utf-8');
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      const match = line.match(/<div class="code-input">(.*)/);

      if (match) {
        const contentAfterTag = match[1].trim();

        if (contentAfterTag === '' || contentAfterTag === '</div>') {
          if (index + 1 < lines.length && lines[index + 1].trim() !== '</div>') {
            const relativePath = path.relative(CONTENT_DIR, file);
            errors.push(
              `${relativePath}:${index + 1} - code-input content not on same line as opening tag`
            );
          }
        }
      }
    });
  });

  return { passed: errors.length === 0, errors };
}

module.exports = testCodeCellFormatting;

if (require.main === module) {
  const result = testCodeCellFormatting();
  console.log('Code Cell Formatting Test:', result.passed ? '✅ PASSED' : '❌ FAILED');
  result.errors.forEach(err => console.error('  ', err));
  process.exit(result.passed ? 0 : 1);
}

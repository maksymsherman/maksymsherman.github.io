const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const glob = require('glob');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const PUBLIC_DIR = path.join(__dirname, '../hugo-site/public');

const SCHEMAS = {
  WebSite: {
    type: 'object',
    required: ['@context', '@type', 'name', 'url'],
    properties: {
      '@context': { const: 'https://schema.org' },
      '@type': { const: 'WebSite' },
      name: { type: 'string' },
      url: { type: 'string', format: 'uri' }
    }
  },
  Person: {
    type: 'object',
    required: ['@context', '@type', 'name'],
    properties: {
      '@context': { const: 'https://schema.org' },
      '@type': { const: 'Person' },
      name: { type: 'string' }
    }
  },
  BlogPosting: {
    type: 'object',
    required: ['@context', '@type', 'headline', 'author'],
    properties: {
      '@context': { const: 'https://schema.org' },
      '@type': { const: 'BlogPosting' },
      headline: { type: 'string' },
      author: { type: 'object' }
    }
  },
  ItemList: {
    type: 'object',
    required: ['@context', '@type', 'itemListElement'],
    properties: {
      '@context': { const: 'https://schema.org' },
      '@type': { const: 'ItemList' },
      itemListElement: { type: 'array' }
    }
  }
};

function validateJSONLD() {
  const errors = [];
  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);

  const htmlFiles = glob.sync(`${PUBLIC_DIR}/**/*.html`);

  htmlFiles.forEach(file => {
    const html = fs.readFileSync(file, 'utf-8');
    const $ = cheerio.load(html);
    const relativePath = path.relative(PUBLIC_DIR, file);

    $('script[type="application/ld+json"]').each((i, elem) => {
      const jsonText = $(elem).html();

      try {
        const jsonData = JSON.parse(jsonText);
        const schemaType = jsonData['@type'];

        if (SCHEMAS[schemaType]) {
          const validate = ajv.compile(SCHEMAS[schemaType]);
          const valid = validate(jsonData);

          if (!valid) {
            errors.push({
              file: relativePath,
              schemaType,
              errors: validate.errors
            });
          }
        }
      } catch (e) {
        errors.push({
          file: relativePath,
          error: 'Invalid JSON in JSON-LD script tag',
          details: e.message
        });
      }
    });
  });

  return { passed: errors.length === 0, errors };
}

module.exports = validateJSONLD;

if (require.main === module) {
  const result = validateJSONLD();
  console.log('JSON-LD Validation Test:', result.passed ? '✅ PASSED' : '❌ FAILED');
  if (!result.passed) {
    result.errors.forEach(err => {
      console.error('  ', err.file || 'Error');
      if (err.errors) {
        err.errors.forEach(e => console.error('    -', e.message));
      }
      if (err.details) {
        console.error('    -', err.details);
      }
    });
  }
  process.exit(result.passed ? 0 : 1);
}

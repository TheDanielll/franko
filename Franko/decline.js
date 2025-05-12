/**
 * A CLI tool for Ukrainian name declension using the shevchenko-js library.
 * Parses command-line arguments (family, given, patronymic, gender),
 * calls the shevchenko API for each grammatical case,
 * and prints a JSON object with all declined forms.
 */

const shevchenko = require('shevchenko');

/**
 * Parse and validate command-line arguments.
 *
 * Usage:
 *   node decline.js <Family?> <Given?> <Patronymic?> [masculine|feminine]
 *
 * @returns {Object} person - with properties:
 *   - gender: 'masculine' or 'feminine'
 *   - familyName?: string
 *   - givenName: string
 *   - patronymicName?: string
 */
function parseArgs() {
  // Remove 'node' and script name
  const argv = process.argv.slice(2);
  if (argv.length === 0) {
    console.error('Usage: node decline.js <Family?> <Given?> <Patronymic?> [masculine|feminine]');
    process.exit(1);
  }

  // Determine gender (default: 'masculine')
  let gender = 'masculine';
  const last = argv[argv.length - 1].toLowerCase();
  if (['masculine', 'feminine'].includes(last)) {
    gender = last;
    argv.pop();
  }

  // Extract positional name parts
  const fields = argv;
  const familyRaw     = fields[0] || '';
  const givenRaw      = fields[1] || '';
  const patronymicRaw = fields[2] || '';

  // Normalize: treat '-' as missing field
  const family     = familyRaw     !== '-' ? familyRaw     : null;
  const given      = givenRaw      !== '-' ? givenRaw      : null;
  const patronymic = patronymicRaw !== '-' ? patronymicRaw : null;

  // Fallback: ensure at least givenName exists
  let realFamily = family;
  let realGiven = given;
  let realPatronymic = patronymic;
  if (!realGiven) {
    if (realPatronymic) {
      realGiven = realPatronymic;
      realPatronymic = null;
    } else if (realFamily) {
      realGiven = realFamily;
      realFamily = null;
    }
  }

  if (!realGiven) {
    console.error('Name is required for declension');
    process.exit(1);
  }

  // Build the person object for shevchenko API
  const person = { gender, givenName: realGiven };
  if (realFamily)     person.familyName     = realFamily;
  if (realPatronymic) person.patronymicName = realPatronymic;
  return person;
}

/**
 * Join available name parts into a single string.
 *
 * @param {Object} obj - may have familyName, givenName, patronymicName
 * @returns {string}
 */
function joinFields(obj) {
  return [obj.familyName, obj.givenName, obj.patronymicName]
    .filter(Boolean)
    .join(' ');
}

/**
 * Main execution function.
 * - Parses arguments
 * - Retrieves nominative form directly
 * - Calls shevchenko for each case
 * - Outputs JSON with all forms
 */
async function main() {
  const person = parseArgs();

  // Nominative: simply join original fields
  const nominative = joinFields(person);

  // Call shevchenko-js API for all cases
  const genObj  = await shevchenko.inGenitive(person);
  const datObj  = await shevchenko.inDative(person);
  const accObj  = await shevchenko.inAccusative(person);
  const instObj = await shevchenko.inAblative(person);
  const locObj  = await shevchenko.inLocative(person);
  const vocObj  = await shevchenko.inVocative(person);

  // Assemble final output
  const output = {
    nominative,
    genitive:     joinFields(genObj),
    dative:       joinFields(datObj),
    accusative:   joinFields(accObj),
    instrumental: joinFields(instObj),
    locative:     joinFields(locObj),
    vocative:     joinFields(vocObj),
  };

  console.log(JSON.stringify(output, null, 2));
}

// Run main and handle unexpected errors
main().catch(err => {
  console.error('Unexpected error:', err);
  process.exit(1);
});

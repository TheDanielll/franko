// decline.js
const shevchenko = require('shevchenko');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node decline.js <text…> [masculine|feminine]');
    process.exit(1);
  }

  // Вибір статі: тільки masculine або feminine
  let gender = 'masculine';
  let textArgs = args;
  const last = args[args.length - 1].toLowerCase();
  if (['masculine', 'feminine'].includes(last)) {
    gender = last;
    textArgs = args.slice(0, -1);
  }

  // Формуємо текст на вхід
  const input = textArgs.join(' ');
  const person = { gender, givenName: input, familyName: '' };

  // Збираємо відмінки
  const nominative   = input;
  const genitive     = (await shevchenko.inGenitive(person)).givenName;
  const dative       = (await shevchenko.inDative(person)).givenName;
  const accusative   = (await shevchenko.inAccusative(person)).givenName;
  const instrumental = (await shevchenko.inAblative(person)).givenName;
  const locative     = (await shevchenko.inLocative(person)).givenName;
  const vocative     = (await shevchenko.inVocative(person)).givenName;

  // Виводимо результат у вигляді JSON
  console.log(JSON.stringify({
    nominative,
    genitive,
    dative,
    accusative,
    instrumental,
    locative,
    vocative
  }, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});

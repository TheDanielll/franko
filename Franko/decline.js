// decline.js
const shevchenko = require('shevchenko');

function parseArgs() {
  const argv = process.argv.slice(2);
  if (argv.length === 0) {
    console.error('Usage: node decline.js <Family?> <Given?> <Patronymic?> [masculine|feminine]');
    process.exit(1);
  }

  // 1) Стать
  let gender = 'masculine';
  const last = argv[argv.length - 1].toLowerCase();
  if (['masculine', 'feminine'].includes(last)) {
    gender = last;
    argv.pop();
  }

  // 2) Позиційні аргументи
  const fields = argv;
  let familyRaw     = fields[0] || '';
  let givenRaw      = fields[1] || '';
  let patronymicRaw = fields[2] || '';

  // 3) Нормалізація: "-" => пропуск
  let family     = familyRaw     !== '-' ? familyRaw     : null;
  let given      = givenRaw      !== '-' ? givenRaw      : null;
  let patronymic = patronymicRaw !== '-' ? patronymicRaw : null;

  // 4) Фолбек: гарантовано маємо given
  if (!given) {
    if (patronymic) {
      given = patronymic;
      patronymic = null;
    } else if (family) {
      given = family;
      family = null;
    }
  }

  if (!given) {
    console.error('Name is required for declension');
    process.exit(1);
  }

  // 5) Створюємо об’єкт person
  const person = { gender, givenName: given };
  if (family)     person.familyName     = family;
  if (patronymic) person.patronymicName = patronymic;
  return person;
}

function joinFields(obj) {
  return [obj.familyName, obj.givenName, obj.patronymicName]
    .filter(Boolean)
    .join(' ');
}

async function main() {
  const person = parseArgs();

  // Номінатив по безвідмінних полях
  const nominative = joinFields(person);

  // Викликаємо API
  const genObj  = await shevchenko.inGenitive(person);
  const datObj  = await shevchenko.inDative(person);
  const accObj  = await shevchenko.inAccusative(person);
  const instObj = await shevchenko.inAblative(person);
  const locObj  = await shevchenko.inLocative(person);
  const vocObj  = await shevchenko.inVocative(person);

  // Збираємо результат
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

main().catch(err => {
  console.error(err);
  process.exit(1);
});

import subprocess
import json
import shutil
import os

class Franko:
    """
    Клас для відмінювання українських імен та прізвищ за допомогою shevchenko.js.
    Приймає формат:
      <прізвище> <ім'я> <по‑батькові>
    За допомогою "-" можна пропускати окремі поля, наприклад:
      - Ім'я По-батькові  (без прізвища)
      Прізвище - По-батькові  (без імені)  # але тоді ім'я обов'язкове
    """
    def __init__(self, text: str = None, gender: str = 'masculine'):
        """
        :param text: рядок у форматі "прізвище ім'я по-батькові";
                     для пропуску використовуйте "-" у потрібній позиції
        :param gender: "masculine" або "feminine"
        """
        if gender not in ('masculine', 'feminine'):
            raise ValueError("gender must be 'masculine' or 'feminine'")
        self.text = text.strip() if text else None
        self.gender = gender

    def decline_all_cases(self) -> dict:
        if not self.text:
            raise ValueError("No text provided for declension.")

        # 1. Шукаємо Node.js
        node_cmd = shutil.which("node") or shutil.which("nodejs")
        if not node_cmd:
            raise RuntimeError("Node.js не знайдено. Додайте node до PATH.")

        # 2. Шлях до decline.bundle.js поруч із цим файлом
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bundle_path = os.path.join(script_dir, "decline.bundle.js")
        if not os.path.isfile(bundle_path):
            raise FileNotFoundError(f"decline.bundle.js не знайдено: {bundle_path}")

        # 3. Розділяємо текст на аргументи та викликаємо JS-бандл
        name_parts = self.text.split()  # ["Шевченко", "Тарас", "Григорович"]
        cmd = [node_cmd, bundle_path] + name_parts + [self.gender]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode != 0:
            err = proc.stderr.decode('utf-8', errors='replace')
            raise RuntimeError(f"Node.js помилка:\n{err}")

        # 4. Парсимо JSON-вивід
        out = proc.stdout.decode('utf-8')
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            raise ValueError(f"Не вдалося розпарсити JSON:\n{out}")

    def generate(self) -> dict:
        return self.decline_all_cases()


if __name__ == "__main__":
    # Приклади використання
    examples = [
        "Александров Даніла Дмитрович",
        "- Тарас Григорович",            # без прізвища
        "Шевченко - Григорович",         # без імені → помилка
        "Чуєнко Катерина Віталіївна"
    ]
    for text in examples:
        print(f"\n'{text}':")
        try:
            f = Franko(text, gender="feminine")
            for case, form in f.generate().items():
                print(f"{case:12}: {form}")
        except Exception as e:
            print(f"Error: {e}")

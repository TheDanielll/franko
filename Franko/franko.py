import subprocess
import json
import shutil
import os

class Franko:
    """
    Клас для відмінювання українських слів чи словосполучень за допомогою shevchenko.js.
    Використовує локальний Node.js та decline.js у тій самій директорії.
    """
    def __init__(self, text: str = None, gender: str = 'masculine'):
        """
        :param text: слідове слово або словосполучення для відмінювання
        :param gender: "masculine" або "feminine"
        """
        self.text = text
        if gender not in ('masculine', 'feminine'):
            raise ValueError("gender must be 'masculine' or 'feminine'")
        self.gender = gender

    def decline_all_cases(self) -> dict:
        """
        Відмінює self.text у всіх семи відмінках за вказаним self.gender.
        Повертає словник із ключами:
          nominative, genitive, dative, accusative, instrumental, locative, vocative
        """
        if not self.text:
            raise ValueError("No text provided for declension.")

        # 1. Знайти команду node
        node_cmd = shutil.which("node") or shutil.which("nodejs")
        if not node_cmd:
            raise RuntimeError("Node.js не знайдено. Додай node.exe в PATH.")

        # 2. Шлях до decline.js поруч з цим файлом
        # __file__ знаходиться в Franko/franko.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bundle_path = os.path.join(script_dir, "decline.bundle.js")
        if not os.path.isfile(bundle_path):
            raise FileNotFoundError(
                f"Не знайдено decline.bundle.js в:\n  {bundle_path}"
            )
        # 3. Виклик Node.js
        proc = subprocess.run(
            [node_cmd, bundle_path, self.text, self.gender],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode != 0:
            err = proc.stderr.decode('utf-8', errors='replace')
            raise RuntimeError(f"Node.js помилка:\n{err}")

        # 4. Розпізнавання та парсинг JSON
        out = proc.stdout.decode('utf-8')
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            raise ValueError(f"Не вдалося розпарсити JSON:\n{out}")

    def generate(self) -> dict:
        """
        Синонім для decline_all_cases(), повертає словник всіх відмінків.
        """
        return self.decline_all_cases()


if __name__ == "__main__":
    # Приклад використання
    f = Franko("Тарас Шевченко", gender="masculine")
    cases = f.generate()
    for case, form in cases.items():
        print(f"{case}: {form}")

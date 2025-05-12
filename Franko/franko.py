import subprocess
import json
import shutil
import os
from typing import Dict, List

from validate import NameInput


class Franko:
    """
    A simple interface for Ukrainian name declension using shevchenko.js.
    Locates Node.js and the bundled JS script on initialization,
    and provides a generate method to decline names for different inputs.
    """

    def __init__(self) -> None:
        # Locate the Node.js executable once at instance creation
        self.node_cmd: str = shutil.which("node") or shutil.which("nodejs")  # type: ignore
        if not self.node_cmd:
            raise RuntimeError("Node.js not found. Please add 'node' to your PATH.")

        # Determine the path to decline.bundle.js next to this file
        script_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.bundle_path: str = os.path.join(script_dir, "decline.bundle.js")
        if not os.path.isfile(self.bundle_path):
            raise FileNotFoundError(f"decline.bundle.js not found at: {self.bundle_path}")

    def generate(self, txt: str, gender: str = "masculine") -> Dict[str, str]:
        """
        Decline the given Ukrainian full name in all grammatical cases.

        Args:
            txt: A string in the format "<surname> <given> <patronymic>".
                 Use "-" to skip a part (e.g. "- Ivan Petrovych").
            gender: Either "masculine" or "feminine".

        Returns:
            A dictionary with keys: 'nominative', 'genitive', 'dative',
            'accusative', 'instrumental', 'locative', 'vocative',
            mapping to the declined full name.

        Raises:
            ValueError: If gender is invalid or txt is empty.
            RuntimeError: If Node.js execution fails.
            FileNotFoundError: If the JS bundle is missing.
        """

        # Validate
        validated = NameInput(parts=txt, gender=gender)

        # Use validated.parts and validated.gender to build Node.js command
        cmd: List[str] = [self.node_cmd, self.bundle_path] + validated.parts + [validated.gender]

        # Execute the JS bundle via Node.js
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            error_msg: str = proc.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(f"Node.js error:\n{error_msg}")

        # Parse and return the JSON output
        output: str = proc.stdout.decode("utf-8")
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON output:\n{output}")


if __name__ == "__main__":
    # Demonstrate multiple calls with one instance
    fr = Franko()
    examples: List[tuple] = [
        ("123 Даніла Дмитрович", "masculine"),
        ("2 Тарас Григорович", "masculine"),
        ("Шевченко - Григорович", "masculine"),
        ("Косач Лариса Петрівна", "feminine")
    ]
    for text, gender in examples:
        print(f"\nText: '{text}', Gender: '{gender}'")
        try:
            forms = fr.generate(text, gender)
            for case, form in forms.items():
                print(f"{case:12}: {form}")
        except Exception as e:
            print(f"Error: {e}")

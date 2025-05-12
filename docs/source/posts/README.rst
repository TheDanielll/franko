Franko ― Ukrainian Name Declension Library
==========================================

Description
-----------
Franko is a simple yet powerful tool for automatic declension of Ukrainian personal names (family name, given name, patronymic).
It leverages the shevchenko-js engine under the hood and provides:

- A **Node.js** (`decline.js` / `decline.bundle.js`) for quick command-line usage.
- A **Python** module (`Franko.py`) with a `Franko` class, so you can integrate declension directly into your scripts.
- A **build script** (`build.js`) based on esbuild that bundles the CLI into a single file for distribution.

Main Components
---------------
1. **`decline.js` / `decline.bundle.js`**
   - Parses positional arguments (`<Family?> <Given?> <Patronymic?> [masculine|feminine]`).
   - Calls shevchenko-js API to produce all seven Ukrainian cases.
   - Outputs a formatted JSON object.

2. **`Franko.py`**
   - Locates `decline.bundle.js` and Node.js on initialization.
   - Exposes `generate(text: str, gender: str='masculine') -> dict`, returning a dict with keys
     `'nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'`.

3. **`build.js`**
   - Uses esbuild to bundle `decline.js` and its dependencies into `decline.bundle.js`.
   - Targets Node.js 14 (`platform: 'node'`, `target: ['node14']`).

Usage
-----

Installation
~~~~~~~~~~~~
From PyPI (when released) and npm:
.. code-block:: bash

    pip install franko


    npm install shevchenko

Python API
~~~~~~~~~~
.. code-block:: python

   from Franko import Franko

   # Create a single instance
   f = Franko()

   # Decline a masculine name
   result = f.generate("Шевченко Тарас Григорович", "masculine")
   print(result)

   # You can call generate() multiple times with different inputs
   for name, gender in [
       ("Шевченко Тарас Григорович", "masculine"),
       ("Косач Лариса Петрівна", "feminine")
   ]:
       forms = f.generate(name, gender)
       print(forms)


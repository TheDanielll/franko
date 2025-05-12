# Franko ― Ukrainian Name Declension Library

[![Documentation](https://img.shields.io/badge/Documentation-Read%20The%20Docs-blue.svg)](https://franko.readthedocs.io/en/latest/index.html)


## Description
Franko is a simple yet powerful tool for automatic declension of Ukrainian personal names (family name, given name, patronymic).  
It uses the [shevchenko-js](https://shevchenko-js.tooleks.com/) engine under the hood and provides:

- A **Node.js** CLI (`decline.js` / `decline.bundle.js`) for quick command-line usage.  
- A **Python** module (`Franko.py`) with a `Franko` class, allowing you to integrate declension directly into your scripts.  
- A **build script** (`build.js`) based on esbuild that bundles the CLI into a single file for distribution.

## Main Components
1. **`decline.js` / `decline.bundle.js`**  
   - Parses positional arguments (`<Family?> <Given?> <Patronymic?> [masculine|feminine]`).  
   - Calls the shevchenko-js API to generate all seven Ukrainian cases.  
   - Outputs a formatted JSON object.

2. **`Franko.py`**  
   - Locates `decline.bundle.js` and the Node.js executable at initialization.  
   - Exposes `generate(text: str, gender: str = 'masculine') -> dict`, returning a dictionary with keys  
     `nominative`, `genitive`, `dative`, `accusative`, `instrumental`, `locative`, and `vocative`.

3. **`build.js`**  
   - Uses esbuild to bundle `decline.js` and its dependencies into `decline.bundle.js`.  
   - Targets Node.js 14 (`platform: 'node'`, `target: ['node14']`).

## Usage

### Installation
#### Node.js must be installed
From PyPI :
```bash
pip install franko
```

Python code

```python
   from Franko import Franko

   # Create a single instance
   f = Franko()

   # Decline a masculine name
   result = f.generate("Шевченко Тарас Григорович", "masculine")
   print(result)

   # You can call generate() multiple times with different inputs
   for name, gender in [
       ("Шевченко Тарас Григорович", "masculine"),
       ("Чуєнко Катерина Віталіївна", "feminine")
   ]:
       forms = f.generate(name, gender)
       print(forms)
```

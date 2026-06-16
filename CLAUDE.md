# Müllsammelsimulator — Agent Instructions

## Context

This app is built **together with 4th graders (age ~9–10)**. Every decision must prioritize simplicity and readability over cleverness. If a 10-year-old can't follow the code, rewrite it.

**Communication:** English with the user. **Everything in code and UI must be German.**

- Variables: `punktzahl`, `leben`, `aktuelles_level`
- Functions: `punktzahlen_laden()`, `level_auswaehlen()`
- UI text: "Level 1 – Ozean [Punkte: 10]"
- Comments: `# Lädt die Punktzahlen aus der Datei`
- File names stay English: `main.py`, `data.py`, `logic.py`


## Game Mechanics

**Menu screen:** Lists 10 levels (Ozean, Wald, Prärie, Strand, Berg, See, Wüste, Schnee, Dschungel, Stadt), each showing the player's best score loaded from `punktzahlen.json`.

**Game screen (per level):**
- Background: nature landscape photo for the level theme
- Items scattered across the screen — each is either **Müll** (trash) or **Natur** (nature)
- Player drags items to corners: `müll_ecke` = lower right, `natur_ecke` = lower left
- +10 points for correct trash placement, +5 for correct nature placement
- Lose 1 `leben` for each wrong assignment; start with 3 lives
- Best score per level saved to `punktzahlen.json`


## Target Device & Deployment

**Device:** Samsung Galaxy Tab S6 Lite (SM-P610), Android 13, OneUI 5.1.1

**Workflow:** Write on Mac in VS Code → push to GitHub → pull on tablet → run there.
- Use only relative file paths
- Test with `python main.py` before pushing


## Forbidden Patterns

Never use these — not even once:

- `with` — forbidden everywhere: no `with open(...)`, no `with canvas.before:`
- `yield` — no generators
- Comprehensions — no list, dict, or set comprehensions; use `for` loops
- `lambda` functions
- Decorators (`@property`, `@classmethod`, etc.)
- Classes — except required Kivy widget subclasses
- Complex inheritance — one level max, only for Kivy widgets
- `*args` / `**kwargs`
- Type hints
- f-strings with expressions — use string concatenation or `.format()`
- Ternary operator (`x if y else z`)


## Code Rules

- Functions under 25 lines; split if longer
- One concept per function
- Descriptive names: `aktuelle_punktzahl` not `ps`
- Comment every function (one line, what it does)
- No wildcard imports (`from kivy import *`)


## File I/O (without `with`)

```python
# Correct
datei = open(PUNKTZAHLEN_DATEI, "r")
inhalt = json.load(datei)
datei.close()
```

## Canvas Styling (without `with`)

Move all canvas styling to `.kv` files — `canvas.before:` in KV syntax is fine, it is not a Python `with` statement. Avoid `canvas.before:` blocks in Python entirely.


## File Structure

| File | Responsibility |
|------|---------------|
| `data.py` | Level definitions, score load/save |
| `logic.py` | Scoring, life tracking, game logic |
| `main.py` | Kivy app, screen setup |
| `menu.kv` | Menu UI layout |
| `spiel.kv` | Game screen UI layout |

Assets go in `assets/`. Level backgrounds: `level_01_ozean.jpg` … `level_10_stadt.jpg`. Item images: `items/muell_flasche.png`, `items/natur_blume.png`, etc. (transparent PNG, ~150×150px).

Window size: `Window.size = (2000, 1200)`, landscape orientation.


## Verification Workflow

Run these checks after every change. All commands run from the project root.

### 1. Syntax check
```bash
python3 -m py_compile main.py data.py logic.py
```
No output = OK. Any output = syntax error to fix before continuing.

### 2. Forbidden pattern check
```bash
grep -n "with " main.py data.py logic.py
grep -n "yield\|lambda\|\[.*for.*in\|{.*for.*in" main.py data.py logic.py
grep -n "f\".*{.*['\"\[.].*}.*\"" main.py data.py logic.py
```
All three must produce **no output**. Any match is a violation to fix.

### 3. Function and file length check
```bash
python3 -c "
import ast
for filepath in ['main.py', 'data.py', 'logic.py']:
    src = open(filepath).read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            length = node.end_lineno - node.lineno + 1
            if length > 25:
                print(filepath + ':' + str(node.lineno) + ' ' + node.name + '() is ' + str(length) + ' lines')
"
```
No output = OK. Any match is a function that needs splitting.

### 4. Import and logic test (no display needed)
```bash
python3 -c "
import data
import logic
punkte = data.standard_punktzahlen()
data.punktzahlen_speichern(punkte)
geladen = data.punktzahlen_laden()
assert list(geladen.keys()) == list(punkte.keys()), 'Key type mismatch after JSON roundtrip'
print('data OK, logic OK')
"
rm -f punktzahlen.json
```
Must print `data OK, logic OK`. A key type mismatch means integer keys became strings through JSON — fix by using string keys consistently throughout (e.g. `"1"` not `1` in `LEVELS` and `punktzahlen`).

### 5. Asset check
```bash
ls assets/
```
Confirm expected images exist before testing on device. Missing images cause silent errors in Kivy.

### 6. App startup test (Mac only, requires display)
```bash
python3 main.py &
PID=$!
sleep 1
if kill -0 $PID 2>/dev/null; then
  kill $PID
  echo "App started OK"
else
  wait $PID
  echo "App crashed with code: $?"
fi
```
Must print `App started OK`. Any crash output before that line is a real error to fix. Note: `timeout` is not available on macOS — use this background-kill pattern instead.

### What cannot be tested without the device

- Screen layout and widget positioning
- Drag-and-drop behaviour
- Screen transitions
- Font rendering and touch targets on the tablet

These require running on the Galaxy Tab S6 Lite.

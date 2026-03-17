# 🧮 Scientific Calculator

A fully-featured scientific calculator built with Python and Streamlit — clean dark UI with a complete math engine under the hood.

---

## Features

| Category | Functions |
|---|---|
| **Basic Arithmetic** | Add, Subtract, Multiply, Divide |
| **Advanced Math** | Power, Square Root, Nth Root, Logarithm (log₁₀, ln), Factorial |
| **Trigonometry** | sin, cos, tan, asin, acos, atan |
| **Angle Conversion** | Degrees ↔ Radians |
| **Memory** | MS, MR, MC, M+ |
| **Constants** | π, e, φ (golden ratio) |
| **Utility** | Percentage, Absolute Value, Reciprocal (1/x), Modulo |
| **History** | Last 15 calculations, clearable |
| **Function Grapher** | Plot up to 3 functions simultaneously over a custom x range |

---

## Project Structure

```
├── calculator.py   # Core Calculator class — all math logic
├── app.py          # Streamlit UI
├── test.py         # 75 unit tests (unittest)
└── README.md
```

---

## Getting Started

### 1. Install dependencies

```bash
pip install streamlit
```

### 2. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

### 3. Run tests

```bash
python test.py -v
```

All 75 tests should pass.

---

## Usage

### In the UI

1. Type numbers using the numpad
2. Press an operator (`+`, `−`, `×`, `÷`) then a second number, then `=`
3. Scientific functions (sin, log, √, etc.) apply instantly to the current value
4. `xⁿ` and `mod` work like binary operators — enter first number, press the button, enter second number, press `=`
5. Memory buttons: **MS** saves, **MR** recalls, **MC** clears, **M+** adds to memory

### As a Python library

```python
from calculator import Calculator

calc = Calculator()

# Basic arithmetic
calc.add(10, 5)        # 15
calc.divide(22, 7)     # 3.142857...

# Scientific
calc.sqrt(144)         # 12.0
calc.sin(calc.PI / 2)  # 1.0
calc.factorial(6)      # 720.0
calc.log10(1000)       # 3.0

# Memory
calc.memory_store(42)
calc.memory_recall()   # 42

# History
calc.get_history()     # list of HistoryEntry objects
calc.last_result()     # most recent result
```

---

## Function Grapher

The **📈 Function Grapher** tab lets you plot mathematical functions interactively.

- Plot **up to 3 functions** at once (color-coded blue, orange, green)
- Set a **custom x range** (e.g. −10 to 10)
- Choose from **built-in presets** (sin & cos, polynomials, exponentials, etc.)
- Supports all standard math syntax:

```
sin(x)   cos(x)   tan(x)   exp(x)   log(x)
sqrt(x)  abs(x)   x**2     x**3     pi    e
```

**Example expressions:**

| Expression | Description |
|---|---|
| `sin(x)` | Sine wave |
| `x**2 - 4` | Parabola shifted down |
| `exp(-x**2)` | Gaussian bell curve |
| `log(abs(x) + 0.1)` | Log with domain guard |
| `sin(x) / x` | Sinc function |

---

## Requirements

- Python 3.9+
- streamlit
- numpy
- matplotlib

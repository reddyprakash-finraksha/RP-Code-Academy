from .dsl import E, L, M, Q

M01 = M("Getting Started with Python", "Write and run your first programs with print().", [
 L("Your First Program", """
# Your First Program
A **program** is a list of instructions. Python reads them top to bottom, one line at a time.

The `print()` function shows text on the screen:

```python
print("Hello, World!")
```
Text inside quotes is called a **string**. You can use single `'...'` or double `"..."` quotes.

**Remember:** `print` must be lower-case, and the brackets and quotes must match.
""", [
  E("Hello, World!", "Print exactly: `Hello, World!`", 'print("Hello, World!")', hints="Use the print() function.|Put the text inside quotes."),
  E("Three Lines", "Print three lines, one per `print` call:\n```\nHello\nRP Code Academy\nLet's code!\n```",
    'print("Hello")\nprint("RP Code Academy")\nprint("Let\'s code!")', hints="Call print() three times.|Use double quotes around Let's code!"),
  E("Your Favourite Subject", "Print exactly: `I love Python`", 'print("I love Python")', hints="One print call is enough."),
 ]),
 L("Comments and Errors", """
# Comments and Errors
A line starting with `#` is a **comment**. Python ignores it, so you can leave notes for humans.

```python
# This prints a greeting
print("Hi")   # comments can also follow code
```
Mistakes are called **errors** (or bugs). Python tells you the line number and the kind of error. A `SyntaxError` means the code is not written correctly, for example a missing quote or bracket.
""", [
  E("Fix the Bug", "This program has a bug. Fix it so it prints `Fixed!`", 'print("Fixed!")',
    starter='print("Fixed!)\n', hints="Look at the quotes.|A string needs both an opening and a closing quote."),
  E("Leave a Note", "Add a comment line, then print `Comments are ignored`.", '# This is my comment\nprint("Comments are ignored")',
    hints="Start the comment line with #.|Then add the print line."),
  E("Quotes Inside Quotes", 'Print exactly: `She said "Hi"`', "print('She said \"Hi\"')",
    hints="Wrap the whole text in single quotes.|Or use a backslash before inner double quotes."),
 ]),
 L("More print() Tricks", """
# More print() Tricks
`print()` can take several values, separated by commas. It puts a space between them.

```python
print("a", "b", "c")           # a b c
print("a", "b", sep="-")       # a-b
print("Loading", end="...")    # no new line after
```
* `sep` changes the separator.
* `end` changes what is printed at the end (default is a new line).
* `print()` with nothing prints an empty line.
""", [
  E("Many Values", "Using ONE print call with three values, print `Python is great`.", 'print("Python", "is", "great")', hints="Separate values with commas."),
  E("Custom Separator", "Print the date `2026-12-25` using `print(2026, 12, 25, ...)` and `sep`.", "print(2026, 12, 25, sep=\"-\")", hints="Add sep=\"-\" inside the brackets."),
  E("No New Line", "Print `Loading...` on ONE line using four print calls: `Loading`, `.`, `.`, `.`. Use `end=\"\"` so the output stays on the same line.",
    'print("Loading", end="")\nprint(".", end="")\nprint(".", end="")\nprint(".")', hints="Use end=\"\" on the first three prints."),
  E("Blank Line", "Print `Top`, then an empty line, then `Bottom`.", 'print("Top")\nprint()\nprint("Bottom")', hints="print() with nothing inside gives an empty line."),
 ]),
], [
 Q("Which function shows text on the screen?", ["show()", "print()", "echo()", "display()"], 1, "print() displays values."),
 Q("What does a # at the start of a line do?", ["Prints a number", "Makes a comment", "Stops the program", "Imports a module"], 1, "Python ignores comments."),
 Q("What is the output of print('a', 'b', sep='-')?", ["a b", "ab", "a-b", "a,b"], 2, "sep replaces the space between values."),
 Q("Which line causes a SyntaxError?", ["print('hi')", "print(\"hi\")", "print('hi)", "print(1)"], 2, "The string is never closed."),
])

M02 = M("Variables and Data Types", "Store values, understand types, and convert between them.", [
 L("Variables", """
# Variables
A **variable** is a named box that stores a value. Create one with `=`:

```python
age = 15
name = "Asha"
print(name, age)
```
Rules for names: letters, digits and `_`; cannot start with a digit; no spaces. Python is case-sensitive (`Age` and `age` differ).
You can change a value any time, and swap two values with `a, b = b, a`.
""", [
  E("Store and Print", "Create a variable `age` equal to `15` and print it.", "age = 15\nprint(age)", hints="Write age = 15 on one line.|Then print(age)."),
  E("Swap Values", "Start with `a = 1` and `b = 2`. Swap them, then print `a` and `b` on one line separated by a space (expected `2 1`).", "a = 1\nb = 2\na, b = b, a\nprint(a, b)",
    starter="a = 1\nb = 2\n# swap here\n", hints="You can swap in one line: a, b = b, a."),
  E("City Variable", "Create `city = \"Chennai\"` and print it.", 'city = "Chennai"\nprint(city)', hints="Strings need quotes."),
 ]),
 L("Data Types", """
# Data Types
Every value has a **type**:

| Type | Example | Meaning |
|---|---|---|
| `int` | `42` | whole number |
| `float` | `3.14` | decimal number |
| `str` | `"hi"` | text |
| `bool` | `True` | True or False |

Use `type(value)` to find out. `print(type(42))` shows `<class 'int'>`.
""", [
  E("Type of an Integer", "Print the type of `42`.", "print(type(42))", hints="print(type(...))"),
  E("Type of a Float", "Print the type of `3.14`.", "print(type(3.14))", hints="3.14 has a decimal point."),
  E("Two Types", "Print the type of `\"hi\"` on one line and the type of `True` on the next.", 'print(type("hi"))\nprint(type(True))', hints="Two print calls."),
 ]),
 L("Type Conversion", """
# Type Conversion
Convert values with `int()`, `float()`, `str()` and `bool()`:

```python
int("25")      # 25
float("3.5")   # 3.5
str(100)       # "100"
int(7.9)       # 7  (cuts off the decimal)
bool(0)        # False   (0, "" and empty collections are False)
```
You cannot add a string and a number directly: `"5" + 5` is an error. Convert first.
""", [
  E("String to Int", 'Convert `"25"` to an int, add 5, and print the result (`30`).', 'print(int("25") + 5)', hints="int(\"25\") gives a number."),
  E("Float Maths", 'Convert `"3.5"` to a float, multiply by 2, and print (`7.0`).', 'print(float("3.5") * 2)', hints="Use float()."),
  E("Add a Percent Sign", "Convert `100` to a string, add `%`, and print `100%`.", 'print(str(100) + "%")', hints="str(100) + \"%\""),
  E("Truncate and Truth", "Print `int(7.9)` on one line, then `bool(0)` and `bool(\"hi\")` on the next line (separated by a space). Expected: `7` then `False True`.",
    'print(int(7.9))\nprint(bool(0), bool("hi"))', hints="Two print calls; the second has two values."),
 ]),
], [
 Q("Which is a valid variable name?", ["2nd_place", "my score", "my_score", "my-score"], 2, "Names use letters, digits and underscores, and cannot start with a digit."),
 Q("What is type(3.0)?", ["int", "float", "str", "bool"], 1, "Numbers with a decimal point are floats."),
 Q("What does int(7.9) give?", ["8", "7.9", "7", "Error"], 2, "int() cuts off the decimal part."),
 Q("What is bool('')?", ["True", "False", "Error", "None"], 1, "An empty string is False."),
])

M03 = M("Numbers and Math", "Arithmetic, order of operations and handy math functions.", [
 L("Arithmetic Operators", """
# Arithmetic Operators
| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` `-` `*` | add, subtract, multiply | `6 * 7` | `42` |
| `/` | divide (always float) | `7 / 2` | `3.5` |
| `//` | floor division | `7 // 2` | `3` |
| `%` | remainder | `7 % 2` | `1` |
| `**` | power | `2 ** 3` | `8` |
""", [
  E("Multiply", "Print `12 * 8`.", "print(12 * 8)", hints="Use *."),
  E("Divide and Remainder", "Print `17 // 5` on one line and `17 % 5` on the next.", "print(17 // 5)\nprint(17 % 5)", hints="// gives the whole part, % the remainder."),
  E("Power", "Print 2 to the power of 10.", "print(2 ** 10)", hints="Use **."),
 ]),
 L("Order of Operations", """
# Order of Operations
Python follows BODMAS: brackets, powers, then `* / // %`, then `+ -`.

```python
print(2 + 3 * 4)     # 14
print((2 + 3) * 4)   # 20
```
Shortcuts update a variable: `x += 5` means `x = x + 5`. Also `-=`, `*=`, `/=`.
""", [
  E("BODMAS", "Print the value of `(5 + 3) * 2 - 4 / 2`.", "print((5 + 3) * 2 - 4 / 2)", hints="Copy the expression into print()."),
  E("Shortcut Operators", "Set `x = 10`, then `x += 5`, then `x *= 2`, then print `x`.", "x = 10\nx += 5\nx *= 2\nprint(x)", hints="x += 5 adds 5 to x."),
  E("Average", "Print the average of `80`, `90` and `100`.", "print((80 + 90 + 100) / 3)", hints="Add in brackets, then divide by 3."),
 ]),
 L("Math Functions", """
# Math Functions
Built-ins: `round(x, digits)`, `abs(x)`, `min()`, `max()`, `sum()`.

The `math` module has more. Import it first:
```python
import math
print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.14159...
```
""", [
  E("Round", "Print `3.14159` rounded to 2 decimals.", "print(round(3.14159, 2))", hints="round(number, digits)"),
  E("Absolute Value", "Print the absolute value of `-17`.", "print(abs(-17))", hints="abs()"),
  E("Square Root", "Use the math module to print the square root of `144`.", "import math\nprint(math.sqrt(144))", hints="import math first."),
  E("Circle Area", "Radius is `5`. Print the area (pi * r squared) rounded to 2 decimals.", "import math\nr = 5\nprint(round(math.pi * r ** 2, 2))", hints="math.pi * r ** 2|Round at the end."),
 ]),
], [
 Q("What is 17 // 5?", ["3", "3.4", "2", "4"], 0, "Floor division drops the decimal."),
 Q("What is 2 + 3 * 4?", ["20", "14", "24", "9"], 1, "Multiplication comes before addition."),
 Q("What does x += 3 do?", ["Sets x to 3", "Adds 3 to x", "Multiplies x by 3", "Compares x to 3"], 1, "x += 3 is x = x + 3."),
 Q("Which line gives 4.0?", ["math.sqrt(16)", "16 // 4", "round(4)", "abs(4)"], 0, "sqrt returns a float."),
])

M04 = M("Strings", "Work with text: indexing, slicing and string methods.", [
 L("String Basics", """
# String Basics
```python
s = "RP Code"
len(s)        # 7
s.upper()     # "RP CODE"
s.lower()     # "rp code"
"Ha" * 3      # "HaHaHa"
"Py" + "thon" # "Python"
```
`len()` counts every character, including spaces.
""", [
  E("Length", 'Print the length of `"RP Code Academy"`.', 'print(len("RP Code Academy"))', hints="len()"),
  E("Upper Case", 'Print `"python"` in upper case.', 'print("python".upper())', hints=".upper()"),
  E("Repeat", "Print `Ha` repeated 3 times with no spaces: `HaHaHa`.", 'print("Ha" * 3)', hints="Use *."),
 ]),
 L("Indexing and Slicing", """
# Indexing and Slicing
Positions start at **0**. Negative positions count from the end.

```python
w = "Python"
w[0]      # 'P'
w[-1]     # 'n'
w[0:2]    # 'Py'   (end is not included)
w[::-1]   # 'nohtyP' (reversed)
```
""", [
  E("First and Last", 'For `"Python"`, print the first letter, then the last letter on the next line.', 'w = "Python"\nprint(w[0])\nprint(w[-1])', hints="Index 0 and index -1."),
  E("Slice", 'Print the first 7 letters of `"Programming"`.', 'print("Programming"[0:7])', hints="[0:7]"),
  E("Reverse", 'Print `"stressed"` reversed.', 'print("stressed"[::-1])', hints="[::-1]"),
 ]),
 L("String Methods", """
# String Methods
Strings have useful methods:
```python
"I like Java".replace("Java", "Python")
"banana".count("a")          # 3
"  hi  ".strip()             # "hi"
"red,green".split(",")       # ['red', 'green']
"-".join(["a", "b"])         # "a-b"
```
Strings are **immutable**: methods return a new string.
""", [
  E("Replace", 'Replace `Java` with `Python` in `"I like Java"` and print it.', 'print("I like Java".replace("Java", "Python"))', hints=".replace(old, new)"),
  E("Count", 'Print how many times `a` appears in `"banana"`.', 'print("banana".count("a"))', hints=".count()"),
  E("Strip", 'Print `"  hello  "` with the spaces removed from both ends.', 'print("  hello  ".strip())', hints=".strip()"),
  E("Split", 'Print the list made by splitting `"red,green,blue"` at the commas.', 'print("red,green,blue".split(","))', hints=".split(\",\")"),
 ]),
], [
 Q("What is 'Python'[1]?", ["P", "y", "t", "Error"], 1, "Index 0 is P, so index 1 is y."),
 Q("What is len('a b')?", ["2", "3", "1", "4"], 1, "Spaces count."),
 Q("What does 'abc'[::-1] return?", ["abc", "cba", "bca", "Error"], 1, "A step of -1 reverses."),
 Q("Which method removes spaces from both ends?", ["trim()", "strip()", "clean()", "cut()"], 1, "strip() does it."),
])

M05 = M("Input and Output", "Read from the keyboard and format your output nicely.", [
 L("Reading Input", """
# Reading Input
`input()` waits for the user to type and returns a **string**.

```python
name = input()
print("Hello,", name)
n = int(input())    # convert to a number
```
In this course your programs are tested by feeding them input automatically, so do **not** print prompts unless the exercise asks.
""", [
  E("Greeting", "Read a name and print `Hello, <name>!`.", 'name = input()\nprint("Hello, " + name + "!")', tests=["Asha\n", "Ravi\n"], hints="name = input()|Join the pieces with +."),
  E("Last, First", "Read a first name, then a last name (two lines). Print `<last>, <first>`.", 'first = input()\nlast = input()\nprint(last + ", " + first)', tests=["Asha\nRao\n", "Ravi\nKumar\n"], hints="Two input() calls."),
  E("Double It", "Read an integer and print it doubled.", "n = int(input())\nprint(n * 2)", tests=["4\n", "21\n", "-3\n"], hints="Convert with int()."),
 ]),
 L("f-Strings", """
# f-Strings
Put `f` before the quotes and variables inside `{}`:

```python
name = "Asha"
print(f"Hi {name}, 2+3 is {2 + 3}")
```
f-strings can hold any expression, which keerp code short and readable.
""", [
  E("Next Year", "Read a name, then an age (integer). Print `<name> will be <age+1> next year.`", 'name = input()\nage = int(input())\nprint(f"{name} will be {age + 1} next year.")', tests=["Asha\n15\n", "Ravi\n20\n"], hints="age + 1 inside {}"),
  E("Price", "Set `price = 3.5` and print `Price: Rs 3.50` (two decimals).", 'price = 3.5\nprint(f"Price: Rs {price:.2f}")', hints=":.2f gives two decimals."),
  E("Square", "Read an integer n and print `<n> squared is <n squared>`.", 'n = int(input())\nprint(f"{n} squared is {n ** 2}")', tests=["5\n", "12\n"], hints="n ** 2"),
 ]),
 L("Formatting Numbers", """
# Formatting Numbers
Inside `{}` add a colon and a format:

| Format | Example | Result |
|---|---|---|
| `{x:,}` | `1234567` | `1,234,567` |
| `{x:.1%}` | `0.256` | `25.6%` |
| `{s:<10}` | left-align in 10 chars | |
| `{s:>5}` | right-align in 5 chars | |
""", [
  E("Thousands", "Print `1234567` with commas: `1,234,567`.", 'print(f"{1234567:,}")', hints=":, in the braces."),
  E("Percent", "Print `0.256` as a percentage with one decimal: `25.6%`.", 'print(f"{0.256:.1%}")', hints=":.1%"),
  E("Table Header", "Print `Name` left-aligned in 10 characters, then `|`, then `Age` right-aligned in 5 characters, using one f-string.", "print(f\"{'Name':<10}|{'Age':>5}\")", hints="{'Name':<10}|{'Age':>5}"),
  E("Add Two Numbers", "Read two integers (one per line) and print `a + b = total`, for example `3 + 4 = 7`.", 'a = int(input())\nb = int(input())\nprint(f"{a} + {b} = {a + b}")', tests=["3\n4\n", "10\n-2\n"], hints="Use an f-string with three parts."),
 ]),
], [
 Q("What type does input() return?", ["int", "float", "str", "bool"], 2, "input() always returns a string."),
 Q("What does f'{2+3}' give?", ["2+3", "5", "'5'", "Error"], 1, "f-strings evaluate expressions."),
 Q("Which prints 3.14 from x = 3.14159?", ["f'{x:.2f}'", "f'{x:2}'", "f'{x:.2}'", "f'{x.2f}'"], 0, ".2f means two decimals."),
 Q("Which gives 1,000?", ["f'{1000:,}'", "f'{1000,}'", "f'{1000:.}'", "f'{1000:c}'"], 0, ":, adds thousands separators."),
])

MODULES_A = [M01, M02, M03, M04, M05]

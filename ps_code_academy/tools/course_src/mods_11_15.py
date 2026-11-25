from .dsl import E, L, M, Q

M11 = M("Functions", "Package reusable code with def, parameters and return values.", [
 L("Defining Functions", """
# Defining Functions
```python
def greet():
    print("Hello!")

def add(a, b):
    return a + b

greet()
print(add(3, 4))
```
`def` defines a function; **calling** it runs the code. `return` sends a value back; `print` only shows it.
""", [
  E("Say Hello", "Define a function `greet()` that prints `Hello!`, then call it.", 'def greet():\n    print("Hello!")\n\ngreet()', hints="def greet():|Indent the body, then call greet()."),
  E("Add Function", "Define `add(a, b)` that returns the sum. Print `add(3, 4)`.", "def add(a, b):\n    return a + b\n\nprint(add(3, 4))", hints="Use return."),
  E("Square Function", "Define `square(n)` that returns n squared. Print `square(9)`.", "def square(n):\n    return n * n\n\nprint(square(9))", hints="return n * n"),
 ]),
 L("Parameters and Return Values", """
# Parameters and Return Values
Parameters can have **default values**. A function can return several values as a tuple.

```python
def greet(name="friend"):
    return "Hello, " + name + "!"

def min_max(items):
    return min(items), max(items)
```
""", [
  E("Default Parameter", "Define `greet(name=\"friend\")` returning `Hello, <name>!`. Print `greet()` then `greet(\"Asha\")`.", 'def greet(name="friend"):\n    return "Hello, " + name + "!"\n\nprint(greet())\nprint(greet("Asha"))', hints="Give name a default value."),
  E("Min and Max", "Define `min_max(items)` returning `(smallest, largest)`. Print `min_max([3, 1, 4, 1, 5])`.", "def min_max(items):\n    return min(items), max(items)\n\nprint(min_max([3, 1, 4, 1, 5]))", hints="Return two values separated by a comma."),
  E("is_even", "Define `is_even(n)` returning True or False. Read an integer and print `is_even(n)`.", "def is_even(n):\n    return n % 2 == 0\n\nn = int(input())\nprint(is_even(n))", tests=["4\n", "7\n"], hints="Return the comparison itself."),
 ]),
 L("Scope, *args and Recursion", """
# Scope, *args and Recursion
* Variables made inside a function are **local**.
* `*args` collects extra arguments into a tuple.
* A **recursive** function calls itself, and needs a base case to stop.

```python
def total(*nums):
    return sum(nums)

def countdown(n):
    if n == 0:
        return
    print(n)
    countdown(n - 1)
```
""", [
  E("Recursive Factorial", "Write a recursive `factorial(n)`. Print `factorial(6)`.", "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(6))", hints="Base case: n <= 1 returns 1."),
  E("Fibonacci", "Write a recursive `fib(n)` where fib(0)=0 and fib(1)=1. Print `fib(10)`.", "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nprint(fib(10))", hints="fib(n) = fib(n-1) + fib(n-2)"),
  E("Variable Arguments", "Define `total(*nums)` that returns the sum of all arguments. Print `total(1, 2, 3, 4)`.", "def total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3, 4))", hints="*nums is a tuple."),
  E("Count Primes", "Write `is_prime(n)`. Read an integer n and print how many primes are between 1 and n (inclusive).", "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nn = int(input())\nprint(sum(1 for i in range(1, n + 1) if is_prime(i)))", tests=["10\n", "30\n", "1\n"], hints="A prime has no divisors from 2 up to its square root."),
 ]),
], [
 Q("Which keyword defines a function?", ["func", "def", "function", "define"], 1, "def starts a function definition."),
 Q("What does a function return if it has no return statement?", ["0", "''", "None", "Error"], 2, "It returns None."),
 Q("What does *args collect?", ["A dictionary", "Extra positional arguments as a tuple", "A list of strings", "Nothing"], 1, "args is a tuple."),
 Q("A recursive function needs a...", ["loop", "base case", "global variable", "class"], 1, "Without a base case it never stops."),
])

M12 = M("Modules and the Standard Library", "Import tools that Python already ships with.", [
 L("Importing Modules", """
# Importing Modules
A **module** is a file of ready-made code.
```python
import math
from math import sqrt
print(math.floor(7.8), math.ceil(7.2))   # 7 8
print(math.gcd(12, 18))                  # 6
```
""", [
  E("Floor and Ceiling", "Print `math.floor(7.8)` and then `math.ceil(7.2)` on separate lines.", "import math\nprint(math.floor(7.8))\nprint(math.ceil(7.2))", hints="import math first."),
  E("Factorial", "Use the math module to print 5 factorial.", "import math\nprint(math.factorial(5))", hints="math.factorial()"),
  E("GCD", "Print the greatest common divisor of 48 and 18.", "import math\nprint(math.gcd(48, 18))", hints="math.gcd()"),
 ]),
 L("statistics and random", """
# statistics and random
```python
import statistics, random
statistics.mean([2, 4, 6])     # 4
statistics.median([1, 5, 3])   # 3
random.randint(1, 6)           # random whole number 1..6
```
Random results change each run, so tests can only check properties (for example, that a dice roll is between 1 and 6).
""", [
  E("Mean", "Print the mean of `[2, 4, 6, 8]`.", "import statistics\nprint(statistics.mean([2, 4, 6, 8]))", hints="statistics.mean()"),
  E("Median", "Print the median of `[7, 1, 5, 3, 9]`.", "import statistics\nprint(statistics.median([7, 1, 5, 3, 9]))", hints="statistics.median()"),
  E("Dice Check", "Roll a dice with `random.randint(1, 6)` and print `True` if the result is between 1 and 6 (it always should be).", "import random\nroll = random.randint(1, 6)\nprint(1 <= roll <= 6)", hints="Store the roll, then test it."),
 ]),
 L("datetime, collections and More", """
# datetime, collections and More
```python
import datetime, collections, string, json
datetime.date(2026, 1, 1).strftime("%A")     # weekday name
collections.Counter("banana").most_common(1)
string.ascii_uppercase                       # 'ABC...Z'
json.dumps({"a": 1})                         # '{"a": 1}'
```
""", [
  E("Weekday", "Print the weekday name of 18 November 2026 (use `datetime.date` and `strftime(\"%A\")`).", 'import datetime\nprint(datetime.date(2026, 11, 18).strftime("%A"))', hints="strftime(\"%A\") gives the day name."),
  E("Most Common", 'Print `Counter("banana").most_common(1)`.', 'from collections import Counter\nprint(Counter("banana").most_common(1))', hints="from collections import Counter"),
  E("Alphabet", "Print the first five upper-case letters using the `string` module: `ABCDE`.", "import string\nprint(string.ascii_uppercase[:5])", hints="Slice string.ascii_uppercase."),
  E("To JSON", 'Print `json.dumps({"a": 1, "b": [1, 2]})`.', 'import json\nprint(json.dumps({"a": 1, "b": [1, 2]}))', hints="import json"),
 ]),
], [
 Q("What does 'import math' do?", ["Runs a calculator", "Makes math functions available", "Installs Python", "Deletes variables"], 1, "It loads the module."),
 Q("What is math.ceil(7.2)?", ["7", "8", "7.2", "7.5"], 1, "ceil rounds up."),
 Q("Why can't tests check an exact random number?", ["Random is slow", "It changes every run", "It is always 0", "It is an error"], 1, "Random values differ each run."),
 Q("Which module computes a mean?", ["math", "statistics", "random", "string"], 1, "statistics.mean()."),
])

M13 = M("File Handling", "Read and write text, CSV and JSON files.", [
 L("Writing Files", """
# Writing Files
```python
with open("notes.txt", "w") as f:
    f.write("Hello\\n")
```
Modes: `"w"` write (replaces), `"a"` append, `"r"` read. Always use `with`: it closes the file for you. In this course your program runs in a private temporary folder, so files you create are deleted afterwards.
""", [
  E("Write and Read", 'Write `Hello file` to `notes.txt`, then read it back and print it.', 'with open("notes.txt", "w") as f:\n    f.write("Hello file")\nwith open("notes.txt") as f:\n    print(f.read())', hints="Use mode \"w\" then open again to read."),
  E("Three Lines", "Write the lines `1`, `2`, `3` (one per line) to `nums.txt`, then read the whole file and print it.", 'with open("nums.txt", "w") as f:\n    f.write("1\\n2\\n3\\n")\nwith open("nums.txt") as f:\n    print(f.read())', hints="Put \\n after each number."),
  E("Append Mode", "Write `A` plus a newline to `log.txt`, append `B` plus a newline, then print the file contents.", 'with open("log.txt", "w") as f:\n    f.write("A\\n")\nwith open("log.txt", "a") as f:\n    f.write("B\\n")\nwith open("log.txt") as f:\n    print(f.read())', hints="Mode \"a\" appends."),
 ]),
 L("Reading Files", """
# Reading Files
```python
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```
`f.read()` gives everything; `f.readlines()` gives a list of lines; looping reads one line at a time. `strip()` removes the trailing newline.
""", [
  E("Count Lines", "Write three lines to `a.txt`, then use `readlines()` to print how many lines it has.", 'with open("a.txt", "w") as f:\n    f.write("x\\ny\\nz\\n")\nwith open("a.txt") as f:\n    print(len(f.readlines()))', hints="len(f.readlines())"),
  E("Shout Each Line", "Write the lines `red`, `green`, `blue` to `c.txt`. Read it line by line and print each in upper case.", 'with open("c.txt", "w") as f:\n    f.write("red\\ngreen\\nblue\\n")\nwith open("c.txt") as f:\n    for line in f:\n        print(line.strip().upper())', hints="Loop over the file and strip each line."),
  E("Content Length", "Write `Python` to `p.txt` using `with`, read it back, and print the length of the text.", 'with open("p.txt", "w") as f:\n    f.write("Python")\nwith open("p.txt") as f:\n    print(len(f.read()))', hints="len(f.read())"),
 ]),
 L("CSV, JSON and Paths", """
# CSV, JSON and Paths
```python
import csv, json, os
json.dump({"a": 1}, open("d.json", "w"))
data = json.load(open("d.json"))
os.path.exists("d.json")        # True / False
```
The `csv` module reads and writes comma-separated rows (`csv.writer`, `csv.reader`).
""", [
  E("CSV Round Trip", "Write the rows `[\"a\", \"b\"]` and `[\"1\", \"2\"]` with `csv.writer`, read them back with `csv.reader`, and print the list of rows.", 'import csv\nwith open("t.csv", "w", newline="") as f:\n    w = csv.writer(f)\n    w.writerow(["a", "b"])\n    w.writerow(["1", "2"])\nwith open("t.csv", newline="") as f:\n    print(list(csv.reader(f)))', hints="Open with newline=\"\" for csv."),
  E("JSON Round Trip", 'Save `{"name": "Asha", "age": 15}` to `s.json` with `json.dump`, load it back, and print the name.', 'import json\nwith open("s.json", "w") as f:\n    json.dump({"name": "Asha", "age": 15}, f)\nwith open("s.json") as f:\n    data = json.load(f)\nprint(data["name"])', hints="json.dump then json.load."),
  E("Sum a File", "Write `10`, `20`, `30` (one per line) to `n.txt`, read them back as integers, and print the sum.", 'with open("n.txt", "w") as f:\n    f.write("10\\n20\\n30\\n")\nwith open("n.txt") as f:\n    print(sum(int(line) for line in f))', hints="int() ignores the trailing newline."),
  E("Does It Exist?", 'Print `os.path.exists("missing.txt")`, then create that file (write `hi`) and print the check again.', 'import os\nprint(os.path.exists("missing.txt"))\nwith open("missing.txt", "w") as f:\n    f.write("hi")\nprint(os.path.exists("missing.txt"))', hints="import os"),
 ]),
], [
 Q("Which mode appends to a file?", ["'r'", "'w'", "'a'", "'x'"], 2, "'a' appends."),
 Q("Why use 'with open(...)'?", ["It is faster", "It closes the file automatically", "It encrypts the file", "It is required"], 1, "with closes the file."),
 Q("What does readlines() return?", ["One string", "A list of lines", "A number", "A dictionary"], 1, "A list with one string per line."),
 Q("Which module saves dictionaries as text?", ["json", "math", "random", "string"], 0, "json.dump / json.load."),
])

M14 = M("Error Handling", "Handle problems gracefully with try and except.", [
 L("try and except", """
# try and except
```python
try:
    n = int("abc")
except ValueError:
    print("Invalid number")
```
Python runs the `try` block; if an error of the named type happens, the `except` block runs instead of crashing.
Common errors: `ValueError`, `ZeroDivisionError`, `IndexError`, `KeyError`, `TypeError`.
""", [
  E("Bad Number", 'Convert `"abc"` with `int()` inside try/except. On `ValueError` print `Invalid number`.', 'try:\n    int("abc")\nexcept ValueError:\n    print("Invalid number")', hints="except ValueError:"),
  E("Divide by Zero", "Compute `10 / 0` inside try/except. On `ZeroDivisionError` print `Cannot divide by zero`.", 'try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print("Cannot divide by zero")', hints="except ZeroDivisionError:"),
  E("Safe Double", "Read one line. If it is an integer print double it, otherwise print `Not a number`.", 'text = input()\ntry:\n    print(int(text) * 2)\nexcept ValueError:\n    print("Not a number")', tests=["12\n", "abc\n", "-5\n"], hints="Put int(text) inside try."),
 ]),
 L("else, finally and Other Errors", """
# else, finally and Other Errors
```python
try:
    value = int("5")
except ValueError:
    print("bad")
else:
    print("OK")       # runs if no error
finally:
    print("Done")     # always runs
```
""", [
  E("else and finally", 'Convert `"5"` in a try block. Use `else` to print `OK` and `finally` to print `Done`.', 'try:\n    int("5")\nexcept ValueError:\n    print("bad")\nelse:\n    print("OK")\nfinally:\n    print("Done")', hints="Order: try, except, else, finally."),
  E("Index Error", "With `nums = [1, 2, 3]`, try to read `nums[10]`. On `IndexError` print `Out of range`.", 'nums = [1, 2, 3]\ntry:\n    print(nums[10])\nexcept IndexError:\n    print("Out of range")', hints="except IndexError:"),
  E("Key Error", 'With `d = {"a": 1}`, try to read `d["b"]`. On `KeyError` print `No such key`.', 'd = {"a": 1}\ntry:\n    print(d["b"])\nexcept KeyError:\n    print("No such key")', hints="except KeyError:"),
 ]),
 L("Raising and Custom Errors", """
# Raising and Custom Errors
```python
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")

class MyError(Exception):
    pass
```
Use `raise` to signal a problem. `except ValueError as e:` lets you read the message with `str(e)`.
""", [
  E("Raise ValueError", "Define `check_age(age)` that raises `ValueError(\"Age cannot be negative\")` when age < 0. Call it with `-5` inside try/except and print the error message.", 'def check_age(age):\n    if age < 0:\n        raise ValueError("Age cannot be negative")\n\ntry:\n    check_age(-5)\nexcept ValueError as e:\n    print(e)', hints="except ValueError as e: print(e)"),
  E("Custom Exception", "Create `class InsufficientFunds(Exception)`. Raise it with the message `Not enough money` and catch it, printing the message.", 'class InsufficientFunds(Exception):\n    pass\n\ntry:\n    raise InsufficientFunds("Not enough money")\nexcept InsufficientFunds as e:\n    print(e)', hints="A custom exception inherits from Exception."),
  E("safe_divide", "Define `safe_divide(a, b)` that returns `None` when b is 0, else a / b. Print `safe_divide(8, 2)` and `safe_divide(1, 0)` on one line separated by a space.", "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n\nprint(safe_divide(8, 2), safe_divide(1, 0))", hints="Catch ZeroDivisionError and return None."),
  E("Retry Until Valid", "Read lines until one is a valid integer. Print `Got <number>` for the first valid one.", 'while True:\n    text = input()\n    try:\n        n = int(text)\n        break\n    except ValueError:\n        continue\nprint(f"Got {n}")', tests=["x\ny\n7\n", "42\n"], hints="Use while True with try/except and break."),
 ]),
], [
 Q("Which block runs only if no error happened?", ["except", "else", "finally", "raise"], 1, "else runs when try succeeded."),
 Q("What does int('abc') raise?", ["TypeError", "ValueError", "KeyError", "IndexError"], 1, "The text is not a valid number."),
 Q("Which keyword signals an error yourself?", ["throw", "raise", "error", "except"], 1, "raise creates an exception."),
 Q("Which block always runs?", ["try", "except", "else", "finally"], 3, "finally runs no matter what."),
])

M15 = M("Object-Oriented Programming", "Model real things with classes and objects.", [
 L("Classes and Objects", """
# Classes and Objects
A **class** is a blueprint; an **object** is one thing built from it.

```python
class Dog:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} says Woof!"

d = Dog("Rex")
print(d.speak())
```
`__init__` runs when the object is created. `self` is the object itself.
""", [
  E("Dog Name", 'Create `class Dog` whose `__init__` stores `name`. Create `Dog("Rex")` and print its `name`.', 'class Dog:\n    def __init__(self, name):\n        self.name = name\n\nd = Dog("Rex")\nprint(d.name)', hints="self.name = name"),
  E("Speak", 'Give `Dog` a `speak()` method returning `<name> says Woof!`. Print `Dog("Rex").speak()`.', 'class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return f"{self.name} says Woof!"\n\nprint(Dog("Rex").speak())', hints="Methods take self as the first parameter."),
  E("Rectangle", "Create `Rectangle(width, height)` with an `area()` method. Print `Rectangle(3, 4).area()`.", "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\nprint(Rectangle(3, 4).area())", hints="area returns width * height."),
 ]),
 L("Methods and State", """
# Methods and State
Objects remember data in **attributes**. Methods can change that state.

```python
class Counter:
    def __init__(self):
        self.value = 0
    def increment(self):
        self.value += 1
```
`__str__` controls what `print(obj)` shows.
""", [
  E("Counter", "Create a `Counter` class starting at 0 with an `increment()` method. Increment three times and print `value`.", "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n\nc = Counter()\nc.increment()\nc.increment()\nc.increment()\nprint(c.value)", hints="self.value += 1"),
  E("Bank Account", "Create `BankAccount` with `balance` starting at 0 and `deposit(x)` / `withdraw(x)` methods. Deposit 200, withdraw 50, and print the balance.", "class BankAccount:\n    def __init__(self):\n        self.balance = 0\n\n    def deposit(self, x):\n        self.balance += x\n\n    def withdraw(self, x):\n        self.balance -= x\n\nacct = BankAccount()\nacct.deposit(200)\nacct.withdraw(50)\nprint(acct.balance)", hints="Update self.balance in each method."),
  E("__str__", "Create `Point(x, y)` with a `__str__` that returns `(x, y)`. Print `Point(1, 2)` (expected `(1, 2)`).", 'class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        return f"({self.x}, {self.y})"\n\nprint(Point(1, 2))', hints="Return an f-string with parentheses."),
 ]),
 L("Inheritance and Polymorphism", """
# Inheritance and Polymorphism
A **child class** reuses and extends a parent class.

```python
class Animal:
    def speak(self):
        return "..."
class Cat(Animal):
    def speak(self):          # override
        return "Meow"
```
`super().__init__(...)` calls the parent's constructor. **Polymorphism**: different classes respond to the same method call in their own way.
""", [
  E("Override", "Create `Animal` with `speak()` returning `...` and `Dog(Animal)` overriding it to return `Woof`. Print `Animal().speak()` then `Dog().speak()` on separate lines.", 'class Animal:\n    def speak(self):\n        return "..."\n\nclass Dog(Animal):\n    def speak(self):\n        return "Woof"\n\nprint(Animal().speak())\nprint(Dog().speak())', hints="class Dog(Animal):"),
  E("super()", 'Create `Person(name)` and `Student(Person)` whose `__init__(name, school)` calls `super().__init__(name)`. For `Student("Asha", "Joy")` print `Asha Joy` (name then school).', 'class Person:\n    def __init__(self, name):\n        self.name = name\n\nclass Student(Person):\n    def __init__(self, name, school):\n        super().__init__(name)\n        self.school = school\n\ns = Student("Asha", "Joy")\nprint(s.name, s.school)', hints="super().__init__(name)"),
  E("Class Attribute", "Create `Item` with a class attribute `count = 0` that increases every time an object is created (in `__init__`). Create 3 items and print `Item.count`.", "class Item:\n    count = 0\n\n    def __init__(self):\n        Item.count += 1\n\nItem()\nItem()\nItem()\nprint(Item.count)", hints="Item.count += 1 inside __init__."),
  E("Shapes", "Create `Square(side)` with `area()` and `Rectangle(w, h)` with `area()`. Put `Square(2)` and `Rectangle(3, 5)` in a list and print each area on its own line.", "class Square:\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side ** 2\n\nclass Rectangle:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    def area(self):\n        return self.w * self.h\n\nfor shape in [Square(2), Rectangle(3, 5)]:\n    print(shape.area())", hints="Both classes have an area() method."),
 ]),
], [
 Q("What is 'self'?", ["A keyword for loops", "The object the method belongs to", "A module", "A global variable"], 1, "self refers to the current object."),
 Q("Which method runs when an object is created?", ["__start__", "__init__", "__new_obj__", "__str__"], 1, "__init__ is the constructor."),
 Q("How do you inherit from Animal?", ["class Dog(Animal):", "class Dog from Animal:", "class Dog: Animal", "Dog extends Animal"], 0, "Parent in brackets."),
 Q("What does super().__init__() do?", ["Deletes the parent", "Calls the parent constructor", "Creates a module", "Prints the class"], 1, "It runs the parent's __init__."),
])

MODULES_C = [M11, M12, M13, M14, M15]

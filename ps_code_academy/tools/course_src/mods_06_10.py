from .dsl import E, L, M, Q

M06 = M("Conditionals", "Make decisions with if, elif and else.", [
 L("if and else", """
# if and else
```python
age = 16
if age >= 18:
    print("Adult")
else:
    print("Minor")
```
The code under `if` must be **indented** (4 spaces). Comparison operators: `==  !=  <  >  <=  >=`. Note `==` compares, `=` assigns.
""", [
  E("Even or Odd", "Read an integer. Print `Even` or `Odd`.", 'n = int(input())\nif n % 2 == 0:\n    print("Even")\nelse:\n    print("Odd")', tests=["4\n", "7\n", "0\n"], hints="n % 2 == 0 means even."),
  E("Adult or Minor", "Read an age. Print `Adult` if 18 or more, otherwise `Minor`.", 'age = int(input())\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")', tests=["18\n", "17\n", "40\n"], hints="Use >=."),
  E("Sign", "Read an integer. Print `Positive`, `Negative` or `Zero`.", 'n = int(input())\nif n > 0:\n    print("Positive")\nelif n < 0:\n    print("Negative")\nelse:\n    print("Zero")', tests=["5\n", "-2\n", "0\n"], hints="You need if, elif and else."),
 ]),
 L("elif Chains", """
# elif Chains
Python checks conditions from top to bottom and runs the **first** one that is True.

```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C or below")
```
""", [
  E("Grade", "Read a score. Print `A` (90+), `B` (80-89), `C` (70-79) or `F` (below 70).", 'score = int(input())\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelse:\n    print("F")', tests=["95\n", "85\n", "72\n", "40\n", "90\n", "80\n"], hints="Check the highest grade first."),
  E("Largest of Three", "Read three integers (one per line). Print the largest.", 'a = int(input())\nb = int(input())\nc = int(input())\nif a >= b and a >= c:\n    print(a)\nelif b >= c:\n    print(b)\nelse:\n    print(c)', tests=["1\n2\n3\n", "9\n4\n6\n", "5\n5\n2\n"], hints="You may also use max()."),
  E("Leap Year", "Read a year. Print `Leap` if divisible by 4 and (not divisible by 100 or divisible by 400), else `Not leap`.", 'y = int(input())\nif y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):\n    print("Leap")\nelse:\n    print("Not leap")', tests=["2024\n", "1900\n", "2000\n", "2023\n"], hints="Combine conditions with and / or."),
 ]),
 L("Logic: and, or, not", """
# Logic: and, or, not
* `a and b` - True only if both are True
* `a or b` - True if at least one is True
* `not a` - flips True/False

Chained comparisons work too: `10 <= n <= 20`.
""", [
  E("In Range", "Read an integer. Print `In range` if it is between 10 and 20 (inclusive), else `Out of range`.", 'n = int(input())\nif 10 <= n <= 20:\n    print("In range")\nelse:\n    print("Out of range")', tests=["10\n", "20\n", "9\n", "15\n", "21\n"], hints="10 <= n <= 20"),
  E("Login", "Read a username, then a password. Print `Welcome` if the username is `admin` and the password is `python123`, otherwise `Denied`.", 'u = input()\np = input()\nif u == "admin" and p == "python123":\n    print("Welcome")\nelse:\n    print("Denied")', tests=["admin\npython123\n", "admin\nwrong\n", "bob\npython123\n"], hints="Use and."),
  E("FizzBuzz Once", "Read an integer n. Print `FizzBuzz` if divisible by 3 and 5, `Fizz` if by 3, `Buzz` if by 5, otherwise n.", 'n = int(input())\nif n % 15 == 0:\n    print("FizzBuzz")\nelif n % 3 == 0:\n    print("Fizz")\nelif n % 5 == 0:\n    print("Buzz")\nelse:\n    print(n)', tests=["3\n", "5\n", "15\n", "7\n"], hints="Check 15 first."),
  E("Valid Triangle", "Read three side lengths (integers, one per line). Print `Valid` if the sum of any two sides is greater than the third, else `Invalid`.", 'a = int(input())\nb = int(input())\nc = int(input())\nif a + b > c and a + c > b and b + c > a:\n    print("Valid")\nelse:\n    print("Invalid")', tests=["3\n4\n5\n", "1\n2\n3\n", "5\n5\n5\n"], hints="All three conditions must be true."),
 ]),
], [
 Q("Which operator checks equality?", ["=", "==", "!=", "=>"], 1, "== compares; = assigns."),
 Q("What prints? x=5; if x>3: print('A') elif x>1: print('B')", ["A", "B", "A and B", "Nothing"], 0, "Only the first true branch runs."),
 Q("What is not (True and False)?", ["True", "False", "None", "Error"], 0, "True and False is False; not flips it."),
 Q("Which is the correct range check?", ["10 <= n <= 20", "10 <= n >= 20", "n = 10..20", "n in 10-20"], 0, "Chained comparison."),
])

M07 = M("Loops", "Repeat work with for and while loops.", [
 L("for Loops", """
# for Loops
```python
for i in range(5):        # 0,1,2,3,4
    print(i)
for i in range(1, 6):     # 1..5
    print(i)
for i in range(2, 11, 2): # 2,4,6,8,10
    print(i)
```
`range(start, stop, step)` stops **before** `stop`. Use `print(x, end=" ")` to print on one line.
""", [
  E("Count to Five", "Print the numbers 1 to 5, one per line.", "for i in range(1, 6):\n    print(i)", hints="range(1, 6)"),
  E("Sum to 100", "Print the sum of the numbers 1 to 100.", "total = 0\nfor i in range(1, 101):\n    total += i\nprint(total)", hints="Start total at 0 and add each i."),
  E("Evens on One Line", "Print the even numbers from 2 to 20 on ONE line, separated by single spaces.", "print(*range(2, 21, 2))", hints="range(2, 21, 2)|print(*list) prints items separated by spaces."),
 ]),
 L("while Loops", """
# while Loops
A `while` loop repeats as long as its condition is True.

```python
n = 3
while n > 0:
    print(n)
    n -= 1
```
Make sure something inside changes the condition, or the loop never ends!
""", [
  E("Countdown", "Print `5` down to `1` one per line, then `Liftoff!`.", 'n = 5\nwhile n > 0:\n    print(n)\n    n -= 1\nprint("Liftoff!")', hints="Subtract 1 each time."),
  E("Factorial", "Read an integer n (0 or more). Print n factorial (n!). 0! is 1.", "n = int(input())\nresult = 1\nfor i in range(2, n + 1):\n    result *= i\nprint(result)", tests=["5\n", "0\n", "7\n"], hints="Multiply result by each number from 2 to n."),
  E("Sum Until Zero", "Read integers one per line until `0` is entered. Print the sum of all numbers before the 0.", "total = 0\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    total += n\nprint(total)", tests=["3\n4\n5\n0\n", "0\n", "10\n-4\n0\n"], hints="while True with break."),
 ]),
 L("break, continue and Nested Loops", """
# break, continue and Nested Loops
* `break` leaves the loop immediately.
* `continue` skips to the next round.
* A loop inside a loop is **nested**.

```python
for row in range(3):
    for col in range(3):
        print(row, col)
```
""", [
  E("First Match", "Find and print the first number from 1 to 100 that is divisible by both 6 and 8.", "for i in range(1, 101):\n    if i % 6 == 0 and i % 8 == 0:\n        print(i)\n        break", hints="Use break after printing."),
  E("Skip Multiples of 3", "Print the numbers 1 to 10, one per line, but skip multiples of 3.", "for i in range(1, 11):\n    if i % 3 == 0:\n        continue\n    print(i)", hints="continue skips the rest of the loop body."),
  E("Star Triangle", "Print this pattern (4 rows):\n```\n*\n**\n***\n****\n```", 'for i in range(1, 5):\n    print("*" * i)', hints="\"*\" * i"),
  E("Times Table", "Read an integer n. Print its times table from 1 to 10, one line each, like `7 x 1 = 7`.", 'n = int(input())\nfor i in range(1, 11):\n    print(f"{n} x {i} = {n * i}")', tests=["7\n", "12\n"], hints="Use an f-string inside a for loop."),
 ]),
], [
 Q("What does range(1, 4) produce?", ["1,2,3", "1,2,3,4", "0,1,2,3", "2,3,4"], 0, "The stop value is excluded."),
 Q("Which keyword exits a loop early?", ["stop", "exit", "break", "continue"], 2, "break leaves the loop."),
 Q("What does continue do?", ["Ends the loop", "Skips to the next round", "Restarts the program", "Does nothing"], 1, "It jumps to the next iteration."),
 Q("How many times does 'for i in range(3): print(i)' print?", ["2", "3", "4", "0"], 1, "range(3) gives 0, 1, 2."),
])

M08 = M("Lists", "Store collections of items and process them.", [
 L("List Basics", """
# List Basics
```python
fruits = ["apple", "banana", "cherry"]
fruits[0]            # 'apple'
len(fruits)          # 3
fruits.append("fig") # add to end
fruits.remove("banana")
```
Lists are **mutable**: you can change them after creating them.
""", [
  E("Second Item", 'For `fruits = ["apple", "banana", "cherry"]` print the second item, then the length of the list on the next line.', 'fruits = ["apple", "banana", "cherry"]\nprint(fruits[1])\nprint(len(fruits))', hints="Index 1 is the second item."),
  E("Append", "Start with `nums = [1, 2, 3]`, append `4`, and print the list.", "nums = [1, 2, 3]\nnums.append(4)\nprint(nums)", hints=".append()"),
  E("Remove", 'Start with `letters = ["a", "b", "c"]`, remove `"b"`, and print the list.', 'letters = ["a", "b", "c"]\nletters.remove("b")\nprint(letters)', hints=".remove(value)"),
 ]),
 L("Looping and Slicing Lists", """
# Looping and Slicing Lists
```python
nums = [10, 20, 30, 40, 50]
for n in nums:
    print(n)
print(nums[:3])     # [10, 20, 30]
print(nums[::-1])   # reversed copy
```
""", [
  E("Sum with a Loop", "For `nums = [4, 8, 15, 16, 23, 42]` use a for loop to print the sum.", "nums = [4, 8, 15, 16, 23, 42]\ntotal = 0\nfor n in nums:\n    total += n\nprint(total)", hints="Start total at 0."),
  E("First Three", "For `nums = [10, 20, 30, 40, 50]` print the first three items as a list.", "nums = [10, 20, 30, 40, 50]\nprint(nums[:3])", hints="Slice with [:3]."),
  E("Backwards", 'For `items = ["x", "y", "z"]` print each item on its own line in reverse order.', 'items = ["x", "y", "z"]\nfor item in items[::-1]:\n    print(item)', hints="Loop over items[::-1]."),
 ]),
 L("List Methods and Comprehensions", """
# List Methods and Comprehensions
```python
nums = [5, 2, 9, 1]
nums.sort()                 # [1, 2, 5, 9]
sorted(nums, reverse=True)  # new list
squares = [n * n for n in range(1, 6)]
evens = [n for n in range(10) if n % 2 == 0]
```
A **list comprehension** builds a list in one line.
""", [
  E("Sort", "Sort `[5, 2, 9, 1]` ascending and print it.", "nums = [5, 2, 9, 1]\nnums.sort()\nprint(nums)", hints=".sort()"),
  E("Squares", "Use a list comprehension to print the squares of 1 to 5 as a list.", "print([n * n for n in range(1, 6)])", hints="[n * n for n in range(1, 6)]"),
  E("Filter Evens", "Use a list comprehension to print the even numbers from 1 to 10 as a list.", "print([n for n in range(1, 11) if n % 2 == 0])", hints="Add if n % 2 == 0 at the end."),
  E("Max and Min", "Read one line of space-separated integers. Print the largest and smallest separated by a space.", "nums = [int(x) for x in input().split()]\nprint(max(nums), min(nums))", tests=["3 9 1 7\n", "5\n", "-4 -9 0\n"], hints="input().split() gives a list of strings."),
 ]),
], [
 Q("What is [1,2,3][-1]?", ["1", "2", "3", "Error"], 2, "-1 is the last item."),
 Q("Which adds an item to the end?", ["add()", "append()", "push()", "insert_end()"], 1, "append() adds at the end."),
 Q("What is [n*2 for n in range(3)]?", ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"], 0, "range(3) is 0,1,2."),
 Q("What does nums[:2] return for [7,8,9]?", ["[7, 8]", "[8, 9]", "[7]", "[7, 8, 9]"], 0, "The slice stops before index 2."),
])

M09 = M("Tuples and Sets", "Immutable sequences and collections of unique items.", [
 L("Tuples", """
# Tuples
A **tuple** is like a list that cannot change.
```python
p = (3, 4)
x, y = p          # unpacking
p.count(3)        # 1
```
Use tuples for fixed groups such as coordinates.
""", [
  E("Add Coordinates", "Set `p = (3, 4)` and print `p[0] + p[1]`.", "p = (3, 4)\nprint(p[0] + p[1])", hints="Index a tuple like a list."),
  E("Unpack", "Unpack `(1, 2, 3)` into `x, y, z` and print `z y x` on one line (expected `3 2 1`).", "x, y, z = (1, 2, 3)\nprint(z, y, x)", hints="x, y, z = (1, 2, 3)"),
  E("Count", "Print how many times `2` appears in `(1, 2, 2, 3, 2)`.", "print((1, 2, 2, 3, 2).count(2))", hints=".count()"),
 ]),
 L("Sets", """
# Sets
A **set** holds unique items with no order.
```python
s = {1, 2, 2, 3}      # {1, 2, 3}
s.add(4)
2 in s                # True
sorted(s)             # a sorted list
```
Convert a list to a set to remove duplicates.
""", [
  E("Remove Duplicates", "Print the sorted list of unique values in `[3, 1, 3, 2, 1]`.", "print(sorted(set([3, 1, 3, 2, 1])))", hints="sorted(set(...))"),
  E("Membership", 'Print whether `"apple"` is in the set `{"apple", "kiwi"}` (True/False).', 'print("apple" in {"apple", "kiwi"})', hints="Use the in operator."),
  E("Unique Letters", 'Print how many different letters are in `"mississippi"`.', 'print(len(set("mississippi")))', hints="set() of a string gives its letters."),
 ]),
 L("Set Operations", """
# Set Operations
```python
a, b = {1, 2, 3}, {3, 4}
a | b    # union        {1, 2, 3, 4}
a & b    # intersection {3}
a - b    # difference   {1, 2}
```
""", [
  E("Union", "Print the sorted list of the union of `{1, 2, 3}` and `{3, 4}`.", "print(sorted({1, 2, 3} | {3, 4}))", hints="Use |."),
  E("Intersection", "Print the sorted list of the intersection of `{1, 2, 3, 4}` and `{3, 4, 5}`.", "print(sorted({1, 2, 3, 4} & {3, 4, 5}))", hints="Use &."),
  E("Difference", "Print the sorted list of `{1, 2, 3, 4}` minus `{3, 4, 5}`.", "print(sorted({1, 2, 3, 4} - {3, 4, 5}))", hints="Use -."),
  E("Common Numbers", "Read two lines of space-separated integers. Print the numbers found in both lines, sorted, separated by spaces. If none, print `none`.", "a = set(map(int, input().split()))\nb = set(map(int, input().split()))\ncommon = sorted(a & b)\nif common:\n    print(*common)\nelse:\n    print(\"none\")", tests=["1 2 3 4\n3 4 5\n", "1 2\n3 4\n", "5 5 6\n6 5\n"], hints="Use set intersection.|print(*list) prints with spaces."),
 ]),
], [
 Q("Can you change a tuple after creating it?", ["Yes", "No", "Only strings", "Only numbers"], 1, "Tuples are immutable."),
 Q("What is len({1, 1, 2})?", ["3", "2", "1", "Error"], 1, "Sets keep unique items."),
 Q("Which operator gives the common items of two sets?", ["|", "&", "-", "+"], 1, "& is intersection."),
 Q("What does x, y = (5, 6) do?", ["Error", "Sets x=5 and y=6", "Sets x=(5,6)", "Sets y=5"], 1, "Tuple unpacking."),
])

M10 = M("Dictionaries", "Store data as key-value pairs.", [
 L("Dictionary Basics", """
# Dictionary Basics
```python
student = {"name": "Asha", "age": 15}
student["name"]          # 'Asha'
student["grade"] = "A"   # add
student["age"] = 16      # change
```
Keys are unique and usually strings or numbers.
""", [
  E("Read a Value", 'For `student = {"name": "Asha", "age": 15}` print the name.', 'student = {"name": "Asha", "age": 15}\nprint(student["name"])', hints="student[\"name\"]"),
  E("Add a Key", "Start with `d = {\"a\": 1}`, add `\"b\": 2`, and print the dictionary.", 'd = {"a": 1}\nd["b"] = 2\nprint(d)', hints="d[\"b\"] = 2"),
  E("Update a Value", 'Start with `price = {"apple": 40}`, set apple to `50`, and print the dictionary.', 'price = {"apple": 40}\nprice["apple"] = 50\nprint(price)', hints="Assign to an existing key."),
 ]),
 L("Looping over Dictionaries", """
# Looping over Dictionaries
```python
d = {"a": 1, "b": 2}
for key, value in d.items():
    print(key, value)
d.get("z", 0)        # safe lookup with default
sum(d.values())      # 3
```
Reading a missing key with `d["z"]` is a `KeyError`; `.get()` avoids it.
""", [
  E("Safe Lookup", 'For `d = {"a": 1}` print `d.get("z", "missing")`.', 'd = {"a": 1}\nprint(d.get("z", "missing"))', hints=".get(key, default)"),
  E("Print Pairs", 'For `d = {"a": 1, "b": 2}` print each pair as `a: 1` on its own line.', 'd = {"a": 1, "b": 2}\nfor k, v in d.items():\n    print(f"{k}: {v}")', hints="Loop over d.items()."),
  E("Sum Values", 'Print the sum of the values in `{"x": 10, "y": 20, "z": 5}`.', 'print(sum({"x": 10, "y": 20, "z": 5}.values()))', hints="sum(d.values())"),
 ]),
 L("Dictionaries in Practice", """
# Dictionaries in Practice
Counting with a dictionary:
```python
counts = {}
for ch in "hello":
    counts[ch] = counts.get(ch, 0) + 1
```
A **dict comprehension** builds a dictionary: `{n: n * n for n in range(1, 4)}`.
""", [
  E("Count Letters", 'Count the letters of `"hello"` into a dictionary and print it.', 'counts = {}\nfor ch in "hello":\n    counts[ch] = counts.get(ch, 0) + 1\nprint(counts)', hints="counts.get(ch, 0) + 1"),
  E("Word Frequency", "Read one line of text. Print each distinct word and its count as `word: n`, one per line, in alphabetical order.", 'words = input().split()\ncounts = {}\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\nfor w in sorted(counts):\n    print(f"{w}: {counts[w]}")', tests=["the cat and the dog\n", "a a a\n"], hints="Loop over sorted(counts)."),
  E("Swap Keys and Values", 'Invert `{"a": 1, "b": 2}` so values become keys, and print the result.', 'd = {"a": 1, "b": 2}\nprint({v: k for k, v in d.items()})', hints="Use a dict comprehension."),
  E("Squares Dictionary", "Use a dict comprehension to print `{1: 1, 2: 4, 3: 9}`.", "print({n: n * n for n in range(1, 4)})", hints="{n: n * n for n in range(1, 4)}"),
 ]),
], [
 Q("How do you read a value safely with a default?", ["d[key]", "d.get(key, default)", "d.read(key)", "d.find(key)"], 1, "get() avoids a KeyError."),
 Q("What does d.items() give?", ["Only keys", "Only values", "Key-value pairs", "The length"], 2, "items() yields (key, value) pairs."),
 Q("What error occurs for a missing key with d['x']?", ["IndexError", "KeyError", "ValueError", "TypeError"], 1, "Missing dictionary keys raise KeyError."),
 Q("What is {1: 'a'}[1]?", ["1", "'a'", "Error", "None"], 1, "The value for key 1."),
])

MODULES_B = [M06, M07, M08, M09, M10]

"""
Python Basics Tutorial - Learn Python Through Examples
=======================================================
This file contains simple examples to learn Python fundamentals.
Run each section to understand how Python works.
"""

# =============================================================================
# 1. VARIABLES AND DATA TYPES
# =============================================================================

print("=" * 50)
print("1. VARIABLES AND DATA TYPES")
print("=" * 50)

# Variables store data - Python figures out the type automatically
name = "Python"  # String (text)
age = 30  # Integer (whole number)
height = 5.9  # Float (decimal number)
is_active = True  # Boolean (True/False)

print(f"Name: {name}, Type: {type(name)}")
print(f"Age: {age}, Type: {type(age)}")
print(f"Height: {height}, Type: {type(height)}")
print(f"Is Active: {is_active}, Type: {type(is_active)}")

# =============================================================================
# 2. BASIC OPERATIONS
# =============================================================================

print("\n" + "=" * 50)
print("2. BASIC OPERATIONS")
print("=" * 50)

# Math operations
x = 10
y = 3

print(f"Addition: {x} + {y} = {x + y}")
print(f"Subtraction: {x} - {y} = {x - y}")
print(f"Multiplication: {x} * {y} = {x * y}")
print(f"Division: {x} / {y} = {x / y}")
print(f"Integer Division: {x} // {y} = {x // y}")
print(f"Remainder: {x} % {y} = {x % y}")
print(f"Power: {x} ** {y} = {x ** y}")

# String operations
greeting = "Hello"
world = "World"
print(f"Concatenation: {greeting} + ' ' + {world} = {greeting + ' ' + world}")
print(f"Repetition: {greeting} * 3 = {greeting * 3}")

# =============================================================================
# 3. CONTROL STRUCTURES - IF/ELSE
# =============================================================================

print("\n" + "=" * 50)
print("3. CONTROL STRUCTURES - IF/ELSE")
print("=" * 50)

# If-else statements help make decisions
temperature = 25

if temperature > 30:
    print(f"Temperature is {temperature}°C - It's hot!")
elif temperature > 20:
    print(f"Temperature is {temperature}°C - It's warm!")
else:
    print(f"Temperature is {temperature}°C - It's cold!")

# Checking multiple conditions
number = 15
if number > 0 and number < 20:
    print(f"{number} is between 0 and 20")

# =============================================================================
# 4. LOOPS - FOR AND WHILE
# =============================================================================

print("\n" + "=" * 50)
print("4. LOOPS - FOR AND WHILE")
print("=" * 50)

# For loop - repeat a specific number of times
print("Counting from 1 to 5:")
for i in range(1, 6):
    print(f"  Count: {i}")

# While loop - repeat while condition is true
print("\nCounting down from 5:")
count = 5
while count > 0:
    print(f"  Count: {count}")
    count -= 1
print("  Blast off!")

# =============================================================================
# 5. DATA STRUCTURES - LISTS
# =============================================================================

print("\n" + "=" * 50)
print("5. DATA STRUCTURES - LISTS")
print("=" * 50)

# Lists store multiple items in order
fruits = ["apple", "banana", "cherry", "date"]
print(f"Fruits list: {fruits}")
print(f"First fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")

# Adding to lists
fruits.append("elderberry")
print(f"After adding: {fruits}")

# Looping through lists
print("All fruits:")
for fruit in fruits:
    print(f"  - {fruit}")

# List length
print(f"Total fruits: {len(fruits)}")

# =============================================================================
# 6. DATA STRUCTURES - DICTIONARIES
# =============================================================================

print("\n" + "=" * 50)
print("6. DATA STRUCTURES - DICTIONARIES")
print("=" * 50)

# Dictionaries store key-value pairs
student = {
    "name": "Alice",
    "age": 20,
    "major": "Physics",
    "gpa": 3.8
}

print(f"Student info: {student}")
print(f"Student name: {student['name']}")
print(f"Student GPA: {student['gpa']}")

# Adding new key-value pair
student["graduation_year"] = 2025
print(f"Updated student: {student}")

# Looping through dictionary
print("Student details:")
for key, value in student.items():
    print(f"  {key}: {value}")

# =============================================================================
# 7. FUNCTIONS
# =============================================================================

print("\n" + "=" * 50)
print("7. FUNCTIONS")
print("=" * 50)

# Functions are reusable blocks of code
def greet(name):
    """This function greets the person passed as parameter"""
    return f"Hello, {name}!"

def add_numbers(a, b):
    """This function adds two numbers and returns the result"""
    return a + b

def calculate_area(length, width):
    """Calculate area of rectangle"""
    area = length * width
    return area

# Using functions
print(greet("Python Learner"))
print(f"5 + 3 = {add_numbers(5, 3)}")
print(f"Area of 4x5 rectangle: {calculate_area(4, 5)}")

# =============================================================================
# 8. WORKING WITH STRINGS
# =============================================================================

print("\n" + "=" * 50)
print("8. WORKING WITH STRINGS")
print("=" * 50)

text = "Python Programming"

print(f"Original: {text}")
print(f"Uppercase: {text.upper()}")
print(f"Lowercase: {text.lower()}")
print(f"Length: {len(text)}")
print(f"Starts with 'Python': {text.startswith('Python')}")
print(f"Replace 'Programming' with 'Coding': {text.replace('Programming', 'Coding')}")
print(f"Split into words: {text.split()}")

# =============================================================================
# 9. LIST COMPREHENSIONS
# =============================================================================

print("\n" + "=" * 50)
print("9. LIST COMPREHENSIONS")
print("=" * 50)

# Create lists in a concise way
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Original numbers: {numbers}")

# Get squares of all numbers
squares = [n ** 2 for n in numbers]
print(f"Squares: {squares}")

# Get only even numbers
evens = [n for n in numbers if n % 2 == 0]
print(f"Even numbers: {evens}")

# =============================================================================
# 10. ERROR HANDLING
# =============================================================================

print("\n" + "=" * 50)
print("10. ERROR HANDLING")
print("=" * 50)

# Try-except blocks handle errors gracefully
def divide_numbers(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return f"{a} / {b} = {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error: Both inputs must be numbers!"

print(divide_numbers(10, 2))
print(divide_numbers(10, 0))
print(divide_numbers(10, "text"))

print("\n" + "=" * 50)
print("Tutorial Complete! You've learned Python basics!")
print("=" * 50)

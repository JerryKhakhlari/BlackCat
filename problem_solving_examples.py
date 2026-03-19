"""
Problem-Solving Examples - Practice Python with Real Problems
=============================================================
This file contains practical problems to solve and learn Python.
Each problem includes the solution with detailed comments.
"""

# =============================================================================
# PROBLEM 1: Find Maximum Number in a List
# =============================================================================

print("=" * 60)
print("PROBLEM 1: Find Maximum Number in a List")
print("=" * 60)

def find_max(numbers):
    """Find the maximum number in a list"""
    if not numbers:  # Check if list is empty
        return None

    max_num = numbers[0]  # Start with first number
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# Test the function
test_numbers = [3, 7, 2, 9, 1, 5]
print(f"Numbers: {test_numbers}")
print(f"Maximum: {find_max(test_numbers)}")
print(f"Using built-in max(): {max(test_numbers)}")

# =============================================================================
# PROBLEM 2: Check if a Number is Prime
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 2: Check if a Number is Prime")
print("=" * 60)

def is_prime(n):
    """Check if a number is prime (only divisible by 1 and itself)"""
    if n < 2:
        return False

    # Check if n is divisible by any number from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Test with different numbers
test_nums = [2, 3, 4, 5, 10, 13, 17, 20]
for num in test_nums:
    result = "is prime" if is_prime(num) else "is not prime"
    print(f"{num} {result}")

# =============================================================================
# PROBLEM 3: Reverse a String
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 3: Reverse a String")
print("=" * 60)

def reverse_string(text):
    """Reverse a string"""
    return text[::-1]  # Python slice notation for reversal

# Test the function
original = "Python"
reversed_text = reverse_string(original)
print(f"Original: {original}")
print(f"Reversed: {reversed_text}")

# =============================================================================
# PROBLEM 4: Count Vowels in a String
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 4: Count Vowels in a String")
print("=" * 60)

def count_vowels(text):
    """Count the number of vowels in a string"""
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

# Test the function
sentence = "Hello World"
print(f"Text: {sentence}")
print(f"Number of vowels: {count_vowels(sentence)}")

# =============================================================================
# PROBLEM 5: Fibonacci Sequence
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 5: Fibonacci Sequence")
print("=" * 60)

def fibonacci(n):
    """Generate first n numbers of Fibonacci sequence"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[-1] + sequence[-2]  # Sum of last two numbers
        sequence.append(next_num)
    return sequence

# Generate first 10 Fibonacci numbers
fib_numbers = fibonacci(10)
print(f"First 10 Fibonacci numbers: {fib_numbers}")

# =============================================================================
# PROBLEM 6: Factorial of a Number
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 6: Factorial of a Number")
print("=" * 60)

def factorial(n):
    """Calculate factorial of a number (n!)"""
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Test factorials
for num in [5, 6, 7]:
    print(f"{num}! = {factorial(num)}")

# =============================================================================
# PROBLEM 7: Remove Duplicates from List
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 7: Remove Duplicates from List")
print("=" * 60)

def remove_duplicates(items):
    """Remove duplicate items from a list"""
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items

# Test the function
numbers_with_duplicates = [1, 2, 2, 3, 4, 4, 5, 1, 6]
print(f"Original: {numbers_with_duplicates}")
print(f"Without duplicates: {remove_duplicates(numbers_with_duplicates)}")
print(f"Using set: {list(set(numbers_with_duplicates))}")

# =============================================================================
# PROBLEM 8: Check if String is Palindrome
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 8: Check if String is Palindrome")
print("=" * 60)

def is_palindrome(text):
    """Check if a string reads the same forwards and backwards"""
    text = text.lower().replace(" ", "")  # Ignore case and spaces
    return text == text[::-1]

# Test with different strings
test_words = ["racecar", "hello", "madam", "python", "A man a plan a canal Panama"]
for word in test_words:
    result = "is" if is_palindrome(word) else "is not"
    print(f"'{word}' {result} a palindrome")

# =============================================================================
# PROBLEM 9: Sum of Digits
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 9: Sum of Digits in a Number")
print("=" * 60)

def sum_of_digits(number):
    """Calculate the sum of all digits in a number"""
    total = 0
    number = abs(number)  # Handle negative numbers
    while number > 0:
        digit = number % 10  # Get last digit
        total += digit
        number = number // 10  # Remove last digit
    return total

# Test the function
test_number = 12345
print(f"Number: {test_number}")
print(f"Sum of digits: {sum_of_digits(test_number)}")

# =============================================================================
# PROBLEM 10: Find Common Elements in Two Lists
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 10: Find Common Elements in Two Lists")
print("=" * 60)

def find_common(list1, list2):
    """Find common elements between two lists"""
    common = []
    for item in list1:
        if item in list2 and item not in common:
            common.append(item)
    return common

# Test the function
list_a = [1, 2, 3, 4, 5]
list_b = [4, 5, 6, 7, 8]
print(f"List A: {list_a}")
print(f"List B: {list_b}")
print(f"Common elements: {find_common(list_a, list_b)}")
print(f"Using set intersection: {list(set(list_a) & set(list_b))}")

# =============================================================================
# PROBLEM 11: Temperature Converter
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 11: Temperature Converter")
print("=" * 60)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

# Test conversions
celsius_temp = 25
fahrenheit_temp = 77
print(f"{celsius_temp}°C = {celsius_to_fahrenheit(celsius_temp):.1f}°F")
print(f"{fahrenheit_temp}°F = {fahrenheit_to_celsius(fahrenheit_temp):.1f}°C")

# =============================================================================
# PROBLEM 12: Word Frequency Counter
# =============================================================================

print("\n" + "=" * 60)
print("PROBLEM 12: Count Word Frequency")
print("=" * 60)

def count_words(text):
    """Count frequency of each word in text"""
    words = text.lower().split()
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

# Test the function
sample_text = "Python is great and Python is easy to learn"
word_freq = count_words(sample_text)
print(f"Text: {sample_text}")
print("Word frequencies:")
for word, count in word_freq.items():
    print(f"  '{word}': {count}")

print("\n" + "=" * 60)
print("All Problems Solved! Keep practicing!")
print("=" * 60)

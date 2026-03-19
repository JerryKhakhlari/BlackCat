"""
File Handling in Python - Working with Files
============================================
Learn how to read, write, and manipulate files in Python.
"""

import os

# =============================================================================
# 1. WRITING TO FILES
# =============================================================================

print("=" * 60)
print("1. WRITING TO FILES")
print("=" * 60)

# Write to a file (creates new file or overwrites existing)
with open('sample.txt', 'w') as file:
    file.write("Hello, Python!\n")
    file.write("This is a sample file.\n")
    file.write("Learning file operations is fun!\n")

print("Created 'sample.txt' with content")

# Append to a file (adds to existing content)
with open('sample.txt', 'a') as file:
    file.write("This line is appended.\n")

print("Appended a line to 'sample.txt'")

# =============================================================================
# 2. READING FROM FILES
# =============================================================================

print("\n" + "=" * 60)
print("2. READING FROM FILES")
print("=" * 60)

# Read entire file
print("Reading entire file:")
with open('sample.txt', 'r') as file:
    content = file.read()
    print(content)

# Read file line by line
print("Reading line by line:")
with open('sample.txt', 'r') as file:
    line_number = 1
    for line in file:
        print(f"Line {line_number}: {line.strip()}")
        line_number += 1

# Read file into a list
print("\nReading into a list:")
with open('sample.txt', 'r') as file:
    lines = file.readlines()
    print(f"Total lines: {len(lines)}")
    print(f"First line: {lines[0].strip()}")

# =============================================================================
# 3. FILE OPERATIONS WITH ERROR HANDLING
# =============================================================================

print("\n" + "=" * 60)
print("3. SAFE FILE OPERATIONS")
print("=" * 60)

def read_file_safely(filename):
    """Read file with error handling"""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found"
    except PermissionError:
        return f"Error: No permission to read '{filename}'"
    except Exception as e:
        return f"Error: {str(e)}"

# Test with existing and non-existing files
print(read_file_safely('sample.txt')[:50] + "...")
print(read_file_safely('nonexistent.txt'))

# =============================================================================
# 4. WORKING WITH CSV-LIKE DATA
# =============================================================================

print("\n" + "=" * 60)
print("4. WORKING WITH CSV-LIKE DATA")
print("=" * 60)

# Write student data to file
students_data = [
    "Name,Age,Grade",
    "Alice,20,A",
    "Bob,22,B",
    "Carol,21,A",
    "David,23,C"
]

with open('students.txt', 'w') as file:
    for line in students_data:
        file.write(line + "\n")

print("Created 'students.txt' with student data")

# Read and parse student data
print("\nReading student data:")
with open('students.txt', 'r') as file:
    header = file.readline().strip().split(',')
    print(f"Columns: {header}")
    print("-" * 40)

    for line in file:
        name, age, grade = line.strip().split(',')
        print(f"Student: {name}, Age: {age}, Grade: {grade}")

# =============================================================================
# 5. COUNTING WORDS IN A FILE
# =============================================================================

print("\n" + "=" * 60)
print("5. FILE STATISTICS")
print("=" * 60)

def file_statistics(filename):
    """Calculate statistics about a text file"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            words = content.split()

            return {
                'lines': len(lines),
                'words': len(words),
                'characters': len(content)
            }
    except Exception as e:
        return None

# Get statistics
stats = file_statistics('sample.txt')
if stats:
    print(f"File: sample.txt")
    print(f"  Lines: {stats['lines']}")
    print(f"  Words: {stats['words']}")
    print(f"  Characters: {stats['characters']}")

# =============================================================================
# 6. COPYING FILES
# =============================================================================

print("\n" + "=" * 60)
print("6. COPYING FILES")
print("=" * 60)

def copy_file(source, destination):
    """Copy content from source file to destination file"""
    try:
        with open(source, 'r') as src:
            content = src.read()

        with open(destination, 'w') as dest:
            dest.write(content)

        return f"Successfully copied {source} to {destination}"
    except Exception as e:
        return f"Error: {str(e)}"

# Copy the sample file
result = copy_file('sample.txt', 'sample_copy.txt')
print(result)

# =============================================================================
# 7. SEARCHING IN FILES
# =============================================================================

print("\n" + "=" * 60)
print("7. SEARCHING IN FILES")
print("=" * 60)

def search_in_file(filename, search_term):
    """Search for a term in a file and return matching lines"""
    matches = []
    try:
        with open(filename, 'r') as file:
            line_number = 1
            for line in file:
                if search_term.lower() in line.lower():
                    matches.append((line_number, line.strip()))
                line_number += 1
    except Exception as e:
        return None

    return matches

# Search for "Python" in the file
search_results = search_in_file('sample.txt', 'Python')
if search_results:
    print(f"Found 'Python' in {len(search_results)} line(s):")
    for line_num, line_text in search_results:
        print(f"  Line {line_num}: {line_text}")
else:
    print("No matches found")

# =============================================================================
# 8. WRITING MULTIPLE LINES EFFICIENTLY
# =============================================================================

print("\n" + "=" * 60)
print("8. EFFICIENT MULTI-LINE WRITING")
print("=" * 60)

# Create a list of data
data_lines = [
    "Python Programming Concepts\n",
    "=" * 30 + "\n",
    "1. Variables and Data Types\n",
    "2. Control Structures\n",
    "3. Functions\n",
    "4. Classes and Objects\n",
    "5. File Operations\n"
]

# Write all lines at once using writelines
with open('concepts.txt', 'w') as file:
    file.writelines(data_lines)

print("Created 'concepts.txt'")

# Read and display
with open('concepts.txt', 'r') as file:
    print(file.read())

# =============================================================================
# 9. CHECKING IF FILE EXISTS
# =============================================================================

print("=" * 60)
print("9. FILE EXISTENCE CHECK")
print("=" * 60)

files_to_check = ['sample.txt', 'students.txt', 'missing.txt', 'concepts.txt']

for filename in files_to_check:
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✓ {filename} exists ({size} bytes)")
    else:
        print(f"✗ {filename} does not exist")

# =============================================================================
# 10. CLEANUP - REMOVING FILES
# =============================================================================

print("\n" + "=" * 60)
print("10. CLEANING UP")
print("=" * 60)

# Remove created files
files_to_remove = ['sample.txt', 'sample_copy.txt', 'students.txt', 'concepts.txt']

for filename in files_to_remove:
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Removed: {filename}")
    except Exception as e:
        print(f"Could not remove {filename}: {e}")

print("\n" + "=" * 60)
print("File Operations Complete!")
print("=" * 60)

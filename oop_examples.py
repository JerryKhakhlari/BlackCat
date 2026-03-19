"""
Object-Oriented Programming (OOP) in Python
===========================================
Learn OOP concepts through simple examples.
"""

# =============================================================================
# 1. BASIC CLASS DEFINITION
# =============================================================================

print("=" * 60)
print("1. BASIC CLASS - Creating Objects")
print("=" * 60)

class Dog:
    """A simple Dog class"""

    def __init__(self, name, age):
        """Initialize dog with name and age"""
        self.name = name
        self.age = age

    def bark(self):
        """Dog barks"""
        return f"{self.name} says: Woof! Woof!"

    def get_info(self):
        """Get dog's information"""
        return f"{self.name} is {self.age} years old"

# Create dog objects
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1.get_info())
print(dog1.bark())
print(dog2.get_info())
print(dog2.bark())

# =============================================================================
# 2. CLASS WITH MORE METHODS
# =============================================================================

print("\n" + "=" * 60)
print("2. BANK ACCOUNT CLASS")
print("=" * 60)

class BankAccount:
    """Simulates a simple bank account"""

    def __init__(self, owner, balance=0):
        """Initialize account with owner and starting balance"""
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Add money to account"""
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount > self.balance:
            return "Insufficient funds"
        if amount > 0:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Invalid withdrawal amount"

    def get_balance(self):
        """Check current balance"""
        return f"{self.owner}'s balance: ${self.balance}"

# Use the bank account
account = BankAccount("Alice", 1000)
print(account.get_balance())
print(account.deposit(500))
print(account.withdraw(300))
print(account.get_balance())

# =============================================================================
# 3. INHERITANCE - REUSING CODE
# =============================================================================

print("\n" + "=" * 60)
print("3. INHERITANCE - Parent and Child Classes")
print("=" * 60)

class Animal:
    """Base class for all animals"""

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        return "Some generic sound"

    def info(self):
        return f"{self.name} is a {self.species}"

class Cat(Animal):
    """Cat class inherits from Animal"""

    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def make_sound(self):
        """Override the parent method"""
        return "Meow!"

class Bird(Animal):
    """Bird class inherits from Animal"""

    def __init__(self, name, can_fly):
        super().__init__(name, "Bird")
        self.can_fly = can_fly

    def make_sound(self):
        return "Chirp chirp!"

# Create different animals
cat = Cat("Whiskers", "Orange")
bird = Bird("Tweety", True)

print(cat.info())
print(f"{cat.name} says: {cat.make_sound()}")
print(f"{cat.name} is {cat.color}")

print(bird.info())
print(f"{bird.name} says: {bird.make_sound()}")
print(f"Can {bird.name} fly? {bird.can_fly}")

# =============================================================================
# 4. PRACTICAL EXAMPLE - STUDENT MANAGEMENT
# =============================================================================

print("\n" + "=" * 60)
print("4. STUDENT MANAGEMENT SYSTEM")
print("=" * 60)

class Student:
    """Represents a student with grades"""

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        """Add a grade to student's record"""
        if 0 <= grade <= 100:
            self.grades.append(grade)
            return f"Grade {grade} added for {self.name}"
        return "Invalid grade (must be 0-100)"

    def get_average(self):
        """Calculate average grade"""
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self):
        """Convert average to letter grade"""
        avg = self.get_average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'

    def display_report(self):
        """Display student's grade report"""
        avg = self.get_average()
        letter = self.get_letter_grade()
        print(f"\nStudent Report for {self.name} (ID: {self.student_id})")
        print(f"Grades: {self.grades}")
        print(f"Average: {avg:.2f}")
        print(f"Letter Grade: {letter}")

# Create and use student objects
student1 = Student("Bob", "S001")
student1.add_grade(85)
student1.add_grade(92)
student1.add_grade(78)
student1.display_report()

student2 = Student("Carol", "S002")
student2.add_grade(95)
student2.add_grade(98)
student2.add_grade(93)
student2.display_report()

# =============================================================================
# 5. CLASS VARIABLES VS INSTANCE VARIABLES
# =============================================================================

print("\n" + "=" * 60)
print("5. CLASS VARIABLES - Shared Across All Instances")
print("=" * 60)

class Car:
    """Car class demonstrating class variables"""

    # Class variable - shared by all instances
    total_cars = 0

    def __init__(self, brand, model):
        # Instance variables - unique to each instance
        self.brand = brand
        self.model = model
        Car.total_cars += 1  # Increment class variable

    def get_info(self):
        return f"{self.brand} {self.model}"

# Create car objects
car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Civic")
car3 = Car("Ford", "Mustang")

print(f"{car1.get_info()}")
print(f"{car2.get_info()}")
print(f"{car3.get_info()}")
print(f"\nTotal cars created: {Car.total_cars}")

# =============================================================================
# 6. SPECIAL METHODS (MAGIC METHODS)
# =============================================================================

print("\n" + "=" * 60)
print("6. SPECIAL METHODS - Making Classes More Pythonic")
print("=" * 60)

class Book:
    """Book class with special methods"""

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """String representation for users"""
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        """String representation for developers"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    def __len__(self):
        """Return length (number of pages)"""
        return self.pages

    def __eq__(self, other):
        """Check if two books are equal"""
        return self.title == other.title and self.author == other.author

# Create and use book objects
book1 = Book("Python Basics", "John Doe", 250)
book2 = Book("Python Basics", "John Doe", 250)
book3 = Book("Advanced Python", "Jane Smith", 400)

print(f"Book 1: {book1}")
print(f"Book 1 has {len(book1)} pages")
print(f"Are book1 and book2 equal? {book1 == book2}")
print(f"Are book1 and book3 equal? {book1 == book3}")

print("\n" + "=" * 60)
print("OOP Concepts Complete!")
print("=" * 60)

print('Hello to you all')
print('Line 2')
print('Line 3')

import math

def cube(n):
    return n ** 3

def validate_number(num_str):
    try:
        num = int(num_str)
        if num > 99:
            raise ValueError("Number must be up to 99")
        return num
    except ValueError:
        raise ValueError("Invalid input, must be an integer")

num_str = input("Enter a number: ")
try:
    num = validate_number(num_str)
    square = num ** 2
    cube_val = cube(num)
    sqrt_val = math.sqrt(num)
    fact = math.factorial(num)
    print(f"Square: {square}")
    print(f"Cube: {cube_val}")
    print(f"Square root: {sqrt_val:.3f}")
    print(f"Factorial: {fact}")
except ValueError as e:
    print(e)

print('Goodbye!')

for i in range(5):
    print(f"Number {i} cubed is {cube(i)}") 

#print the factorial of 3
print('Factorial of 3 is', math.factorial(3))

print('Cube of 12 is', cube(12))

#

# Print "A final comment to show this is the end of the program"
print("This is the end of the program.")

for i in range(1, 5):
    print(f"Square of {i} is {i**2}")

abd = int(input("Enter a number for abd: "))

if abd < 12:
    print(f"Cube of abd is {cube(abd)}")


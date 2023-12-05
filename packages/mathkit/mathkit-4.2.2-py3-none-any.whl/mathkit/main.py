"""
    Add two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

"""
import math
import sys
import time

def add(num1=None, num2=None):
    """
    Add two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None
    """
    if num1 is None or num2 is None:
        if num1 == "d" and num2 == "d":
            print("Welcome to the Addition Calculator")
        if num1 is None:
            num1 = float(input("Enter the first number: "))
        if num2 is None:
            num2 = float(input("Enter the second number: "))
    print("The sum is", num1 + num2)

def cbrt(num=None):
    """
    Calculate the cube root of a number and print the result.

    Args:
        num (int or float): The number to calculate the cube root of (default: None).

    Returns:
        None
    """
    if num is None:
        num = float(input("Enter the number: "))
    if num == "d":
        print("Welcome to the Cube Root Calculator")
        num = float(input("Enter the number: "))
    cube_root = num ** (1/3)
    print("The cube root of", num, "is", cube_root)

def cube(num=None):
    """
    Calculate the cube of a number and print the result.

    Args:
        num (int or float): The number to calculate the cube of (default: None).

    Returns:
        None
    """
    if num is None:
        num = float(input("Enter the number: "))
    if num == "d":
        print("Welcome to the Cube Calculator")
        num = float(input("Enter the number: "))
    cube_result = num * num * num
    print("Cube of the number is", cube_result)

def div(num1=None, num2=None):
    """
    Divide two numbers and print the result.

    Args:
        num1 (int or float): The numerator (default: None).
        num2 (int or float): The denominator (default: None).

    Returns:
        None
    """
    if num1 is None:
        num1 = float(input("Enter the first number: "))
    if num2 is None:
        num2 = float(input("Enter the second number: "))
    if num1 == "d" and num2 == "d":
        print("Welcome to the Division Calculator")
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    print("Your answer is", num1 / num2)

def fact(num=None):
    """
    Calculate the factorial of a number and print the result.

    Args:
        num (int): The number to calculate the factorial of (default: None).

    Returns:
        None
    """
    if num is None:
        num = int(input("Enter the number: "))
    factorial = 1
    if num < 0:
        print("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        print("The factorial of 0 is 1")
    elif num == "d":
        print("Welcome to the Factorial Calculator")
        num = int(input("Enter the number: "))
        for i in range(1, num + 1):
            factorial = factorial * i
        print("The factorial of", num, "is", factorial)
    else:
        num = int(num)  # Convert num to int in case it was provided as a string
        for i in range(1, num + 1):
            factorial = factorial * i
        print("The factorial of", num, "is", factorial)

def hcf(num1=None, num2=None):
    """
    Calculate the highest common factor (HCF) of two numbers and print the result.

    Args:
        num1 (int): The first number (default: None).
        num2 (int): The second number (default: None).

    Returns:
        None
    """
    print("HCF of two numbers")
    if num1 is None:
        num1 = int(input("Enter the first number: "))
    if num2 is None:
        num2 = int(input("Enter the second number: "))
    if num1 == "d" and num2 == "d":
        print("Welcome to the HCF Calculator")
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
    if num1 > num2:
        smaller = num2
    else:
        smaller = num1
    hcf_value = 1  # Initialize hcf_value with a default value
    for i in range(1, smaller + 1):
        if (num1 % i == 0) and (num2 % i == 0):
            hcf_value = i
    print("The H.C.F. of", num1, "and", num2, "is", hcf_value)

def lcm(num1=None, num2=None):
    """
    Calculate the least common multiple (LCM) of two numbers and print the result.

    Args:
        num1 (int or str): The first number or "d" for a separate calculator (default: None).
        num2 (int or str): The second number or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    print("LCM of two numbers")
    if num1 == "d" and num2 == "d":
        print("Welcome to the LCM Calculator")
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
    else:
        if num1 is None:
            num1 = int(input("Enter the first number: "))
        if num2 is None:
            num2 = int(input("Enter the second number: "))

    if num1 > num2:
        greater = num1
    else:
        greater = num2

    while True:
        if (greater % num1 == 0) and (greater % num2 == 0):
            lcm_value = greater
            break
        greater += 1

    print("The LCM of", num1, "and", num2, "is", lcm_value)
    input("Press Enter to continue")

def log(num=None):
    """
    Calculate the logarithm of a number and print the result.

    Args:
        num (int or float or str): The number to calculate the logarithm of or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    print("Logarithm")
    print("1. Logarithm of 2")
    print("2. Logarithm of 10")
    print("3. Logarithm of any number")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if num == "d":
        print("Welcome to the Logarithm Calculator")
        num = float(input("Enter the number: "))
        print(math.log(num))
    elif choice == "1":
        print(math.log(2))
    elif choice == "2":
        print(math.log(10))
    elif choice == "3":
        if num is None:
            num = float(input("Enter the number: "))
        print(math.log(num))
    elif choice == "4":
        sys.exit()
    else:
        print("Invalid choice!")
        log()

def mod(num1=None, num2=None):
    """
    Calculate the modulus of two numbers and print the result.

    Args:
        num1 (int or float or str): The first number or "d" for a separate calculator (default: None).
        num2 (int or float or str): The second number or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num1 == "d" and num2 == "d":
        print("Welcome to the Modulus Calculator")
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            print("Your answer is", num1 % num2)
    else:
        if num1 is None:
            num1 = int(input("Enter the first number: "))
        if num2 is None:
            num2 = int(input("Enter the second number: "))
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            print("Your answer is", num1 % num2)

def mul(num1=None, num2=None):
    """
    Multiply two numbers and print the result.

    Args:
        num1 (int or float or str): The first number or "d" for a separate calculator (default: None).
        num2 (int or float or str): The second number or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num1 == "d" and num2 == "d":
        print("Welcome to the Multiplication Calculator")
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        print("Product =", num1 * num2)
    else:
        if num1 is None:
            num1 = int(input("Enter the first number: "))
        if num2 is None:
            num2 = int(input("Enter the second number: "))
        print("Product =", num1 * num2)

def percentage(num=None, perc=None):
    """
    Perform percentage calculations and print the result.

    Args:
        num (float or str): The number for percentage calculation or "d" for a separate calculator (default: None).
        perc (float or str): The percentage value or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num == "d" and perc == "d":
        print("Welcome to the Percentage Calculator")
        print("1. Percentage of a number")
        print("2. Percentage increase")
        print("3. Percentage decrease")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            num = float(input("Enter the number: "))
            perc = float(input("Enter the percentage: "))
            result = (perc / 100) * num
            print(f"{perc}% of {num} is {result}")
        elif choice == 2:
            num = float(input("Enter the number: "))
            perc = float(input("Enter the percentage: "))
            result = num + (perc / 100) * num
            print(f"{num} increased by {perc}% is {result}")
        elif choice == 3:
            num = float(input("Enter the number: "))
            perc = float(input("Enter the percentage: "))
            result = num - (perc / 100) * num
            print(f"{num} decreased by {perc}% is {result}")
        elif choice == 4:
            sys.exit()
        else:
            print("Invalid choice!")
            percentage()
    else:
        if num is None:
            num = float(input("Enter the number: "))
        if perc is None:
            perc = float(input("Enter the percentage: "))
        if perc is not None and num is not None:
            result = (perc / 100) * num
            print(f"{perc}% of {num} is {result}")

def power(num=None):
    """
    Calculate the power of a number and print the result.

    Args:
        num (int or float or str): The number or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num == "d":
        print("Welcome to the Power Calculator")
        num = int(input("Enter the number: "))
        power_value = int(input("Enter the power: "))
        result = num ** power_value
        print("The answer is:", result)
    else:
        if num is None:
            num = int(input("Enter the number: "))
        power_value = int(input("Enter the power: "))
        result = num ** power_value
        print("The answer is:", result)

def sqrt(num=None):
    """
    Calculate the square root of a number and print the result.

    Args:
        num (int or float or str): The number to calculate the square root of or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num == "d":
        print("Welcome to the Square Root Calculator")
        num = int(input("Enter a number: "))
        print("Square root of", num, "is", math.sqrt(num))
    else:
        if num is None:
            num = int(input("Enter a number: "))
        print("Square root of", num, "is", math.sqrt(num))

def sqr(num1=None):
    """
    Calculate the square of a number and print the result.

    Args:
        num1 (int or float or str): The number to calculate the square of or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num1 == "d":
        print("Welcome to the Square Calculator")
        num1 = float(input("Enter a number: "))
        print("The square of", num1, "is", num1 * num1)
    else:
        if num1 is None:
            num1 = float(input("Enter a number: "))
        print("The square of", num1, "is", num1 * num1)

def sub(num1=None, num2=None):
    """
    Subtract two numbers and print the result.

    Args:
        num1 (int or float or str): The first number or "d" for a separate calculator (default: None).
        num2 (int or float or str): The second number or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num1 == "d" and num2 == "d":
        print("Welcome to the Subtraction Calculator")
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        print("Your answer is", num1 - num2)
    else:
        if num1 is None:
            num1 = int(input("Enter first number: "))
        if num2 is None:
            num2 = int(input("Enter second number: "))
        print("Your answer is", num1 - num2)

def trig(num=None):
    """
    Perform trigonometric calculations (sine, cosine, tangent) for a number and print the result.

    Args:
        num (float or str): The number to perform trigonometric calculations on or "d" for a separate calculator (default: None).

    Returns:
        None
    """
    if num == "d":
        print("Welcome to the Trigonometry Calculator")
        print("1. Sine")
        print("2. Cosine")
        print("3. Tangent")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            num = float(input("Enter the number: "))
            print("Sine of", num, "is", math.sin(num))
        elif choice == 2:
            num = float(input("Enter the number: "))
            print("Cosine of", num, "is", math.cos(num))
        elif choice == 3:
            num = float(input("Enter the number: "))
            print("Tangent of", num, "is", math.tan(num))
        else:
            print("Invalid choice!")
    else:
        print("Trigonometry")
        print("1. Sine")
        print("2. Cosine")
        print("3. Tangent")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            if num is None:
                num = float(input("Enter the number: "))
            print("Sine of", num, "is", math.sin(num))
        elif choice == 2:
            if num is None:
                num = float(input("Enter the number: "))
            print("Cosine of", num, "is", math.cos(num))
        elif choice == 3:
            if num is None:
                num = float(input("Enter the number: "))
            print("Tangent of", num, "is", math.tan(num))
        elif choice == 4:
            exit()
        else:
            print("Invalid choice!")
            trig(num)

def compound_interest(principal=None, rate=None, time=None):
    """
    Calculate compound interest and print the result.

    Args:
        principal (float): The principal amount (default: None).
        rate (float): The interest rate (default: None).
        time (float): The time in years (default: None).

    Returns:
        None
    """
    print("Compound Interest")
    if principal is None:
        principal = float(input("Enter the principal amount: "))
    if rate is None:
        rate = float(input("Enter the interest rate (as a decimal): "))
    if time is None:
        time = float(input("Enter the time in years: "))
    compound_interest_result = principal * (1 + rate / 100)**time - principal
    final_result = compound_interest_result + principal
    #principal_amount * (1 + rate / 100) ** time
    print("Compound Interest:", compound_interest_result)

def simple_interest(principal=None, rate=None, time=None):
    """
    Calculate simple interest and print the result.

    Args:
        principal (float): The principal amount (default: None).
        rate (float): The interest rate (default: None).
        time (float): The time in years (default: None).

    Returns:
        None
    """
    print("Simple Interest")
    if principal is None:
        principal = float(input("Enter the principal amount: "))
    if rate is None:
        rate = float(input("Enter the interest rate (as a decimal): "))
    if time is None:
        time = float(input("Enter the time in years: "))
    simple_interest_result = principal * rate * time
    print("Simple Interest:", simple_interest_result)

def main():
    """
    The main function.

    Args:
        None

    Returns:
        None
    """
    print("Welcome to the Python Calculator")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Square")
    print("6. Square Root")
    print("7. Cube")
    print("8. Cube Root")
    print("9. Percentage")
    print("10. Power")
    print("11. Trigonometry")
    print("12. Compound Interest")
    print("13. Simple Interest")
    print("12. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add()
        time.sleep(2)
        main()
    elif choice == 2:
        sub()
        time.sleep(2)
        main()
    elif choice == 3:
        mul()
        time.sleep(2)
        main()
    elif choice == 4:
        div()        
        time.sleep(2)
        main()
    elif choice == 5:
        sqr()
        time.sleep(2)
        main()
    elif choice == 6:
        sqrt()
        time.sleep(2)
        main()
    elif choice == 7:
        cube()
        time.sleep(2)
        main()
    elif choice == 8:
        cbrt()
        time.sleep(2)
        main()
    elif choice == 9:
        percentage()
        time.sleep(2)
        main()
    elif choice == 10:
        power()
        time.sleep(2)
        main()
    elif choice == 11:
        trig()
        time.sleep(2)
        main()
    elif choice == 12:
        exit()
    else:
        print("Invalid choice!")
        main()


a = None
sign = None
b = None
import math

while True:
    print("Ввидите число, знак, число")
    a = int(input())
    sign = input()
    b = int(input())
    if sign == "+":
        print(a + b)
    if sign == "*":
        print(a * b)
    if sign == "/":
        print(a / b)
    if sign == "-":
        print(a - b)
    if sign == "**":
        print(a ** b)
    if sign == "//":
        print(a // b)
    if sign == "%":
        print(a % b)
    if sign == "sqrt":
        print("какое число(1-ое или 2-ое)")
        c = int(input())
        if c == 1:
            print(math.sqrt(a))
        elif c == 2:
            print(math.sqrt(b))
        else:
            print("ты даун, тебе написли первое или второе")

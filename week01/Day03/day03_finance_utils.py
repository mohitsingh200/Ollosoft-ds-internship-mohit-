# Factorial Function
def factorial(n):
    fact = 1

    for i in range(1, n + 1):
        fact *= i

    return fact


# Prime Check Function
def is_prime(num):

    if num <= 1:
        return False

    for i in range(2, num):

        if num % i == 0:
            return False

    return True


# Fibonacci Function
def fibonacci(n):

    series = []

    a = 0
    b = 1

    for i in range(n):
        series.append(a)
        a, b = b, a + b

    return series


# Percentage Return Function
def percentage_return(old_price, new_price):

    result = ((new_price - old_price) / old_price) * 100

    return result

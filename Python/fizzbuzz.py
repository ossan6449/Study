def fizzbuzz(n=101):
    for i in range(0, n):
        if i % 15 == 0:
            print('FizzBuzz')
        elif i%3 == 0:
            print('Fizz')
        elif i%3 == 0:
            print('Buzz')
        else:
            print(i)
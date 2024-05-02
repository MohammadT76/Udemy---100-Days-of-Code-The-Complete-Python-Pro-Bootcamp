
# if the number is divisible by 3       --> say Fizz
# if the number is divisible by 5       --> say Buzz
# if the number is divisible by 3 and 5 --> say FizzBuzz


for number in range(0,100):
    if number % 3 == 0 and number % 5 == 0:
        print('FizzBuzz')
    elif number % 3 == 0:
        print('Fizz')
    elif number % 5 == 0:
        print('Buzz')
    else:
        print(number)
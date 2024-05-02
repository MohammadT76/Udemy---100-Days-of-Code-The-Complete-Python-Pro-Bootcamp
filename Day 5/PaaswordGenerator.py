
import string, random

def gen_char(type,num):
    match type:
        case 'char':
            return random.sample(string.ascii_lowercase + string.ascii_uppercase, num)
        case 'digit':
            return random.sample(string.digits, num)
        case 'sym':
            return random.sample(string.punctuation, num)
        case 'random':
            return random.sample(string.printable, num)

def gen_pass():
    num_char = int(input('Number of char in your pass? '))
    num_digit = int(input('Number of digits in your pass? '))
    num_sym = int(input('Number of symbol in your pass? '))

    password = []
    password.extend(gen_char('char',num_char))
    password.extend(gen_char('digit',num_digit))
    password.extend(gen_char('sym',num_sym))
     # shuffling password 
    random.shuffle(password)
   
    return ''.join(password)

print(gen_pass())

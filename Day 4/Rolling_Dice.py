
def Dice_Shape(number):
    match number:
        case 1:
            print(
                """
                _____
               |     |
               |  O  |
               |_____|

                """
            )
        case 2:
            print(
                """
                _____
               |  O  |
               |     |
               |__O__|

                """
            )
        case 3:
            print(
                """
                _____
               |  O  |
               |  O  |
               |__O__|

                """
            )
        case 4:
            print(
                """
                _____
               | O O |
               |     |
               |_O_O_|

                """
            )
        case 5:
            print(
                """
                _____
               | O O |
               |  O  |
               |_O_O_|

                """
            )
        case 6:
            print(
                """
                _____
               | O O |
               | O O |
               |_O_O_|

                """
            )

def Rolling_Dice_Game():
    rand_num = randint(1,6)
    Dice_Shape(rand_num)


from random import randint
repeat = True

while repeat:
    Rolling_Dice_Game()
    print("Do you want to roll again?")
    repeat = ("y" or "yes") in input().lower()
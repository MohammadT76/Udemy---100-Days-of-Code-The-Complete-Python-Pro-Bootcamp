
row1 = ['|___|','|___|','|___|']
row2 = ['|___|','|___|','|___|']
row3 = ['|___|','|___|','|___|']

board = f'{row1}\n{row2}\n{row3}'


counter = 0
while counter<10:
    r,c = map(int,input('Please enter position (row,column): ').split(','))

    match r:
        case 1:
            row1[c] = '  X  '
        case 2:
            row2[c] = '  X  '
        case 3:
            row3[c] = '  X  ' 

    board = f'{row1}\n{row2}\n{row3}'
    print(board)
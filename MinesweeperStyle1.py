from random import randint


def new_game_beginning():
    global size_of_field, repeater, amount_of_mines
    # 1.size  2.repeater  3.mines
    difficulty_dict = {
        'e': (10, 8, 20),  # Easy
        'm': (17, 20, 60), # Medium
        'h': (27, 50, 150) # Hard 
    }

    choice = input('\nChoose difficulty (Easy/Medium/Hard): ').lower()
    print()

    if choice[0] in difficulty_dict:
        size_of_field, repeater, amount_of_mines = difficulty_dict[choice]
    else:
        print('Error! Please, try again.')
        new_game_beginning()

    new_game_setup()


# Global constants
ALPHABET = '.ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_VARS = ('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ')

# Introduction
print('''==========================================
| Welcome!                               |
| This is Console Minesweeper in Python. |
| Input coordinates in format "d2"       |
| Or set a flag by typing "fd2"          |
==========================================''')


def create_mined_field():
    mined_field = [[0] * (size_of_field + 1) for _ in range(size_of_field + 1)]

    mines_coords = []

    # Placement of mines
    mines_counter = amount_of_mines

    while mines_counter:
        mine_x = randint(1, size_of_field - 1)
        mine_y = randint(1, size_of_field - 1)

        if (mine_x, mine_y) not in mines_coords:
            mined_field[mine_x][mine_y] = 1
            mines_coords.append((mine_x, mine_y))
            mines_counter -= 1

    for i in range(size_of_field):
        mined_field[0][i] = 2
        mined_field[i][0] = 2
        mined_field[i][size_of_field] = 2
        mined_field[size_of_field - 1][i] = 2

    return mined_field


def create_showing_field():
    field = [['• '] * size_of_field for _ in range(size_of_field)]
    field[0][0] = '  '

    for element in range(1, size_of_field):
        field[0][element] = ALPHABET[element] + ' '

    for number in range(1, size_of_field):
        field[number][0] = str(number) + ' ' if number < 10 else str(number)

    field[size_of_field - 1] = [' ' * 8]  # Empty space under the field

    return field


def game_over():
    # Output of the playing field with mines
    end_game_mines_show()
    [print(*row) for row in end_game_mines_show()]

    if input('Game Over\n\nDo you want to start a new game? (y/n): ').lower().startswith('y'):
        new_game_beginning()
    else:
        exit(input('\nPress Enter to exit.'))


def error_warning():
    print('''==========================================
| Error! (Wrong Input) Please try again. |
==========================================
''')


def check_neighbouring_mines(x_check, y_check):
    counter = 0

    for i in range(y_check - 1, y_check + 2):
        for j in range(x_check - 1, x_check + 2):
            if mined_field[i][j] == 1:
                counter += 1

    return counter


def check_neighbouring_flags(x_check, y_check):
    counter = 0

    for i in range(y_check - 1, y_check + 2):
        for j in range(x_check - 1, x_check + 2):
            if (i < size_of_field - 1 and j < size_of_field - 1) and showing_field[i][j] == 'F ':
                counter += 1

    return counter


def check_neighbouring_numbers(x_num, y_num):
    for i in range(y_num - 1, y_num + 2):
        for j in range(x_num - 1, x_num + 2):
            if mined_field[i][j] == 1 and showing_field[i][j] != 'F ':
                game_over()
            if mined_field[i][j] == 0  and showing_field[i][j] != 'F ':
                showing_field[i][j] = str(check_neighbouring_mines(j, i)) + ' '


def end_game_mines_show():
    for i in range(1, size_of_field):
        for j in range(1, size_of_field):
            if mined_field[i][j] == 1:
                showing_field[i][j] = '# '


def clear_field():
    for _ in range(repeater):
        for i in range(1, size_of_field - 1):
            for j in range(1, size_of_field - 1):
                if showing_field[i][j] == '0 ':
                    check_neighbouring_numbers(j, i)


def mine_check():
    if mined_field[y][x] == 1:
        game_over()
    else:
        showing_field[y][x] = str(check_neighbouring_mines(x, y)) + ' '

        if showing_field[y][x] in NUM_VARS:
            if str(check_neighbouring_flags(x, y)) + ' ' == showing_field[y][x]:
                check_neighbouring_numbers(x, y)
                clear_field()

        if showing_field[y][x] == '0 ':
            check_neighbouring_numbers(x, y)
            clear_field()

        main()


def prevent_game_crashes(x_prevent, y_prevent):
    try:
        x_prevent = ALPHABET.index(x_prevent.upper())
        y_prevent = int(y_prevent)

        if x_prevent < size_of_field and 0 < y_prevent < size_of_field - 1:
            return x_prevent, y_prevent
        else:
            error_warning()
            main()
    except:
        error_warning()
        main()


def main():
    global x, y

    [print(*row) for row in showing_field]  # Output of the playing field

    try:
        coords_input = input('Input Coordinates: ').lower()
        print()
    except:
        exit()

    if coords_input == '' or coords_input == 'f':
        error_warning()
        main()
    
    if coords_input[0] == 'f' and (len(coords_input) >= 3 and str.isnumeric(coords_input[1]) is False):
        # Flag placement
        # Changing x and y string type to integer
        x = coords_input[1]
        y = coords_input[2:]
        x, y = prevent_game_crashes(x, y)

        # Prevent flag from being placed on the number
        if showing_field[y][x] == '• ':
            showing_field[y][x] = 'F '

        main()
    else:
        # Changing x and y string type to integer
        x = coords_input[0]
        y = coords_input[1:]
        x, y = prevent_game_crashes(x, y)

    mine_check()


def new_game_setup():
    global mined_field, showing_field

    showing_field = create_showing_field()

    [print(*row) for row in showing_field]  # Output of the playing field

    user_input = input('Input Coordinates: ').lower()
    print()

    x = user_input[0]
    y = user_input[1:]
    x, y = prevent_game_crashes(x, y)
    showing_field[y][x] = '0 '

    if x < size_of_field:
        while True:
            mined_field = create_mined_field()

            if mined_field[y][x] == 0 and check_neighbouring_mines(x, y) == 0:
                break

    clear_field()
    main()


# First steps
new_game_beginning()

if __name__ == '__main__':
    main()

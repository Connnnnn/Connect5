from PyInquirer import prompt
from pygments import style

test_board = [['[0,0]', '[ ]', '[ ]', '[3,0]', '[ ]', '[ ]', '[6,0]', '[ ]', '[ ]'],
              ['[ ]', '[1,1]', '[ ]', '[3,1]', '[ ]', '[5,1]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[2,2]', '[3,2]', '[4,2]', '[5,2]', '[6,2]', '[7,2 ]', '[8,2]'],
              ['[0,3]', '[1,3]', '[2,3]', '[3,3]', '[4,3]', '[5,3]', '[6,3]', '[7,3]', '[8,3]'],
              ['[ ]', '[ ]', '[2,4]', '[3,4]', '[4,4]', '[5,4]', '[6,4]', '[ ]', '[ ]'],
              ['[ ]', '[1,5]', '[2,5]', '[3,5]', '[4,5]', '[5,5]', '[6,5]', '[ ]', '[ ]'],
              [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]

test_board2 = [['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[ ]', '[x]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[x]', '[o]', '[x]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[x]', '[o]', '[o]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[o]', '[o]', '[o]', '[x]', '[ ]', '[ ]'],
              [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]

test_board3 = [['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[ ]', '[x]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[x]', '[o]', '[x]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[x]', '[o]', '[o]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[o]', '[o]', '[o]', '[x]', '[ ]', '[ ]'],
              [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]
col = 3
row = 3
#6,1 is the top of 7 col
col2 = 6
row2 = 1

col3 = 2
row3 = 1

if __name__ == '__main__':

    for a in range(4, -4, -1):

        x = row + a
        y = col + a
        if 0 <= x < 6 and 0 <= y < 9:
            print(test_board[x][y])

    print("-------- Vert")
    for b in range(4, -4, -1):

        x = row + b
        y = col
        if 0 <= x < 6 and 0 <= y < 9:
            print(test_board[x][y])

    print("--------")
    for c in range(4, -4, -1):

        x = row + c
        y = col - c
        if 0 <= x < 6 and 0 <= y < 9:
            print(test_board[x][y])

    print("-------- Hor")
    for d in range(4, -4, -1):

        x = row
        y = col + d
        if 0 <= x < 6 and 0 <= y < 9:
            print(test_board[x][y])

    print("-------- NEW diag")
    diag2win = 0

    for e in range(4, -4, -1):
        piece = "x"
        x = row2 + e
        y = col2 - e
        if 0 <= x < 6 and 0 <= y < 9:
            if test_board2[x][y] == f"[{piece}]":
                print(test_board2[x][y])
                diag2win += 1
                if diag2win == 4:
                    print("You've Won Diag!")
            else:
                diag2win = 0
    print(diag2win)

    print("-------- NEW Vert ")
    vertwin = 0

    for f in range(4, -4, -1):
        piece = "x"
        x = row3 + e
        y = col3
        if 0 <= x < 6 and 0 <= y < 9:
            if test_board2[x][y] == f"[{piece}]":
                print(test_board2[x][y])
                vertwin += 1
                if vertwin == 4:
                    print("You've Won Vert!")
            else:
                vertwin = 0
    print(vertwin)

    vertwin = 0
    questions = [
        {
            'type': 'input',
            'message': 'Enter a number between 1-9 to make your move',
            'name': 'move'
        }
    ]
    move_answer = prompt(questions, style=style)
    curr_move = move_answer.get("move")
    i = 5
    for i in range(5, -1, -1):

        if test_board2[i][curr_move] != "[x]" and test_board2[i][curr_move] != "[o]":
            test_board2[i][curr_move] = f"[{piece}]"
            row4 = i
            break

    vertwin = 0
    # Checking for vertical win
    for g in range(4, -4, -1):
        x = row + g
        y = move
        if 0 <= x < 6 and 0 <= y < 9:
            if board[x][y] == f"[{piece}]":
                vertwin = vertwin + 1
                if vertwin == 5:
                    print("You've Won Vert!")
                    break
            else:
                vertwin = 0

    diag_win = 0
    for a in range(4, -4, -1):

        x = row + a
        y = move
        if 0 <= x < 6 and 0 <= y < 9:
            if board[x][y] == f"[{piece}]":
                diag_win = diag_win + 1
                if diag_win == 5:
                    print("You've Won Vert!")
                    break
            else:
                diag_win = 0

    diag_win = 0
    diag2_win = 0
    vert_win = 0
    hor_win = 0
    for a in range(4, -4, -1):
        diag_x = row + a
        diag_y = move

        diag2_x = row + c
        diag2_y = col - c

        vert_x = row + g
        vert_y = move

        hor_x = row
        hor_y = move + g

        if 0 <= diag_x < 6 and 0 <= diag_y < 9:
            if board[diag_x][diag_y] == f"[{piece}]":
                diag_win = diag_win + 1
                if diag_win == 5:
                    print("You've Won Diagonally!")
                    break
            else:
                diag_win = 0

        if 0 <= vert_x < 6 and 0 <= vert_y < 9:
            if board[vert_x][vert_y] == f"[{piece}]":
                vert_win = vert_win + 1
                if vert_win == 5:
                    print("You've Won Vert!")
                    break
            else:
                vert_win = 0

        if 0 <= diag2_x < 6 and 0 <= diag2_y < 9:
            if board[diag2_x][diag2_y] == f"[{piece}]":
                diag2_win = diag_win + 1
                if diag2_win == 5:
                    print("You've Won Diagonally!")
                    break
            else:
                diag2_win = 0

        if 0 <= hor_x < 6 and 0 <= hor_y < 9:
            if board[hor_x][hor_y] == f"[{piece}]":
                hor_win = hor_win + 1
                if hor_win == 5:
                    print("You've Won Diagonally!")
                    break
            else:
                hor_win = 0

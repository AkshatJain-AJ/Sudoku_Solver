import sys
sys.setrecursionlimit(1000000)


def solve(board):
    position = find_empty(board)
    if not position:
        return True

    for i in range(1, 10):
        if valid(board, i, position):
            board[position[0]][position[1]] = i

            if solve(board):
                return True

            board[position[0]][position[1]] = 0

    return False


def valid(board, num, pos):
    # column check
    for i in range(len(board[0])):              # 3 => len(board)
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # row chech
    for i in range(len(board[0])):              # 3 => len(board[0])
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # mini Box check
    # start_row = pos[0] - ( len(board) % 3 )
    # start_col = pos[1] - ( len(board[0]) % 3 )

    # for i in range(3):
    #     for j in range(3):
    #         if board[i + start_row][j + start_col] == num and (i, j) != pos:
    #             return False
    # return True

    # mini Box check
    box_x = pos[0] // 3
    box_y = pos[1] // 3

    for i in range(box_x * 3, box_x * 3 + 3):
        for j in range(box_y * 3, box_y * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - -  - - - -  - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")

            if j == 8:
                print(str(board[i][j]))
            else:
                print(str(board[i][j]) + " ", end = "")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)               # row, col

    return None

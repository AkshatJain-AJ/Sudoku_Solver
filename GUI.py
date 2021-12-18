import pygame
from solver import solve, valid
import time
from random import sample
from random import *
pygame.font.init()


base = 3
side = base * base


# Pattern for a baseline valid solution
def pattern(row, col):
    return (base * (row % base) + row // base + col) % side

# Randomize rows, columns, and numbers (of valid base pattern)
def shuffle(nums_range):
    return sample(nums_range, len(nums_range))

rBase = range(base) 
Rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)] 
Cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
nums = shuffle(range(1, base * base + 1))

# Produce board using randomized baseline pattern
board = [[nums[pattern(r, c)] for c in Cols] for r in Rows]

squares = side * side
fraction = random()                     # any number from 0 to 1
empties = int(squares * fraction)                

for p in sample(range(squares), empties):
    board[p // side][p % side] = 0


class Grid:

    # board = [                                             # sample board
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]


    # board = [                                             # solution of sample board
    #     [7, 8, 5, 4, 3, 9, 1, 2, 6],
    #     [6, 1, 2, 8, 7, 5, 3, 4, 9],
    #     [4, 9, 3, 6, 2, 1, 5, 7, 8],
    #     [8, 5, 7, 9, 4, 3, 2, 6, 1],
    #     [2, 6, 1, 7, 5, 8, 9, 3, 4],
    #     [9, 3, 4, 1, 6, 2, 7, 8, 5],
    #     [5, 7, 8, 3, 9, 4, 6, 1, 2],
    #     [1, 2, 6, 5, 8, 7, 4, 9, 3],
    #     [3, 4, 9, 2, 1, 6, 8, 5, 7]
    # ]

    board = board[:]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if solve(self.model) and valid(self.model, val, (row, col)):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0:                          # for upper dark boundary ==> and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.height, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.width), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # reset all others
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap               # column
            y = pos[1] // gap               # row

            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:              # trying value
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))

        elif not(self.value == 0):                          # final suitable value
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), (y + (gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))

    # Draw Time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 165, 560))

    # Draw strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))

    # Draw grid and board
    board.draw(win)

def format_time(secs):
    seconds = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + " : " + str(seconds)
    return mat


def main():
    win = pygame.display.set_mode((552, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 550, 550)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1

                        key = None

                    if board.is_finished():
                        print("Game Over")
                        font = pygame.font.SysFont('comicsans', 90, bold = True)
                        label = font.render("Game Over", 1, (255, 0, 0))

                        win.blit(label, (77, 250))
                        pygame.display.update()
                        pygame.time.delay(1500)
                        run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()

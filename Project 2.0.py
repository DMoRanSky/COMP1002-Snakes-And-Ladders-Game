import tkinter as tk
import random
import os

# 0: Easy, 1 : Medium, 2: Hard
level = 2

board = [5, 6, 10]
numCell = [5 * 5, 6 * 6, 10 * 10]

players = 3

# 该谁投色子
nowPlayer = 0

# 每个玩家的位置，玩家编号 0 ~ players - 1
playerLocation = [0] * players

end = numCell[level] - 1

snakes = []
ladders = []

NumberOfSnakes = [3, 5, 7]
NumberOfLadder = [3, 5, 7]

# set
S = {}


# Task1
def showGameBoard():
    os.system("cls")

    print("awa")


# Task 2
def getRandomNumber():
    return random.randint(1, 6)


# Task 3


def generateSnakeAndLadderPostion():
    for i in NumberOfSnakes:
        while 1:
            num = numCell[level]
            c = [random.randint(0, num - 1), random.randint(0, num - 1)]
            if c[0] == c[1] or c[0] < c[1] or c[0] in S or c[1] in S or c[0] == end:
                continue
            snakes.append(c)
            S[c[0]] = 1
            S[c[1]] = 1
            break
    for i in NumberOfLadder:
        while 1:
            num = numCell[level]
            c = [random.randint(0, num - 1), random.randint(0, num - 1)]
            if c[0] == c[1] or c[0] > c[1] or c[0] in S or c[1] in S:
                continue
            ladders.append(c)
            S[c[0]] = 1
            S[c[1]] = 1
            break


# Task 4


def Winner():
    res = []
    for i in range(players):
        if playerLocation[i] == end:
            res.append(i)
    return res


generateSnakeAndLadderPostion()


# print(snakes)
# print(ladders)

# 一个在 x 跳到 y 走到哪
def jump(x, y):
    return min(x + y, end)



def draw_board(canvas, size):
    num_cells = size * size

    for i in range(1, num_cells):
        if i % size == 0:
            for j in range(size):
                canvas.create_rectangle(j * 40, (i - 1) * 40, (j + 1) * 40, i * 40, fill='lightgray')
        else:
            for j in range(size - 1, -1, -1):
                canvas.create_rectangle(j * 40, (i - 1) * 40, (j + 1) * 40, i * 40, fill='lightgray')


def roll_dice(canvas, size, player_position):
    w = Winner()
    if len(w) > 0:
        print(w)
        print("Wins")
        exit(0)
    
    print("蛇", snakes)
    print("梯子", ladders)
    for i in range(players):
        print(f'{i} is at {playerLocation[i]}')
    global nowPlayer
    print(f"It's {nowPlayer} turns, please click enter to get dice toll")
    x = getRandomNumber()
    print(f"骰子是 {x}")

    u = playerLocation[nowPlayer]
    v = jump(u, x)
    print(f"{nowPlayer} move to {v}")

    for i in snakes:
        if v == i[0]:
            print(f"{nowPlayer} 遇到蛇了， 掉到 {i[1]}")
            v = i[1]

    for i in ladders:
        if v == i[0]:
            print(f"{nowPlayer} 遇到梯子了， 升到 {i[1]}")
            v = i[1]
    playerLocation[nowPlayer] = v

    nowPlayer = (nowPlayer + 1) % players


def move_player(canvas, size, player_position, steps):
    num_cells = size * size

    for _ in range(steps):
        player_position[1] += 1
        if player_position[1] == size:
            player_position[1] = 0
            player_position[0] += 1
            if player_position[0] % 2 == 0:
                player_position[1] = size - 1

        update_player_token_position(canvas, size, player_position)
        canvas.update()
        canvas.after(500)  # Pause for visualization

        if player_position[0] * size + player_position[1] == num_cells - 1:
            print("Player reached the end of the board!")


def update_player_token_position(canvas, size, player_position):
    x, y = player_position
    x_pixel = y * 40 + 5
    y_pixel = x * 40 + 5
    canvas.coords(player_token, x_pixel, y_pixel)


def choose_player(player_number_var):
    print("Selected Player:", player_number_var.get())
    x = int(player_number_var.get())
    #print(type(x))
    players = x - 1


def choose_difficulty(difficulty_var):
    print("Selected Difficulty:", difficulty_var.get())
    x = int(difficulty_var.get())
    levels = x - 1

def draw():
    root = tk.Tk()
    size = board[level]
    num_cells = size * size

    canvas = tk.Canvas(root, width=size * 40, height=size * 40, bg='white')
    canvas.pack()

    draw_board(canvas, size)

    player_position = [0, 0]
    global player_token
    player_token = canvas.create_oval(5, 5, 25, 25, fill='blue')

    # Player selection
    player_number_var = tk.StringVar()
    player_number_var.set("1")  # Default value
    player_menu = tk.OptionMenu(root, player_number_var, "1", "2", "3", "4", "5")
    player_menu.pack()

    # Difficulty selection
    difficulty_var = tk.StringVar()
    difficulty_var.set("level1")  # Default value
    difficulty_menu = tk.OptionMenu(root, difficulty_var, "level1", "level2", "level3")
    difficulty_menu.pack()

    # Roll Dice button
    roll_button = tk.Button(root, text='Roll Dice', command=lambda: roll_dice(canvas, size, player_position))
    roll_button.pack()

    # Choose Player button
    choose_player_button = tk.Button(root, text='Choose Player', command=lambda: choose_player(player_number_var))
    choose_player_button.pack()

    # Choose Difficulty button
    choose_difficulty_button = tk.Button(root, text='Choose Difficulty', command=lambda: choose_difficulty(difficulty_var))
    choose_difficulty_button.pack()

    root.mainloop()

draw()

"""
2.0：增加了title，加上了数字，修改了一些细枝末节的东西
3.0: 增加了title，加上了数字，修改了一些细枝末节的东西
3.1: Win()函数让结束的时候有窗口显示
"""

import tkinter as tk
import random
import os
from tkinter import messagebox

# 0: Easy, 1 : Medium, 2: Hard
level = 2

# 默认棋盘大小
board = [5, 6, 10]
numCell = [5 * 5, 6 * 6, 10 * 10]

players = 3

# 该谁投色子
nowPlayer = 0

# 每个玩家的位置，玩家编号 0 ~ players - 1 待赋值
playerLocation = []
end = 0

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

# 一个在 x 跳到 y 走到哪
def jump(x, y):
    return min(x + y, end)


color = ['red', 'yellow', 'blue', 'black', 'green']

## 圆的大小

S = 10

## 间隔

V = 2

dx = [0, 0, 0, S + V, S + V]
dy = [0, S + V, 2 * S + 2 * V, 0, S + V]

player_token = []


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


def draw_board(canvas, size):
    """
    绘制棋盘格子

    canvas: 画布对象
    size: 棋盘大小
    """
    num_cells = size * size

    for i in range(1, num_cells + 1):  # 修改循环范围，包括最后一个格子
        if i % 2 == 1:
            m = 1
            for j in range(size):
                x1 = j * 40
                y1 = (i - 1) * 40
                x2 = (j + 1) * 40
                y2 = i * 40
                canvas.create_rectangle(x1, y1, x2, y2, fill='lightblue')  # 绘制矩形

                # 计算数字的位置
                text_x = (x1 + x2) / 2
                text_y = (y1 + y2) / 2
                m = (i - 1) * size + j + 1
                canvas.create_text(text_x, text_y, text=str(m), font=("Arial", 12))  # 显示数字

        else:
            for j in range(size - 1, -1, -1):
                x1 = j * 40
                y1 = (i - 1) * 40
                x2 = (j + 1) * 40
                y2 = i * 40
                canvas.create_rectangle(x1, y1, x2, y2, fill='lightblue')  # 绘制矩形

                # 计算数字的位置
                text_x = (x1 + x2) / 2
                text_y = (y1 + y2) / 2
                m = i * size - j
                canvas.create_text(text_x, text_y, text=str(m), font=("Arial", 12))  # 显示数字


# 给 0 到 ~ 格子编号返回行列号

def get(u):
    n = board[level]

    x = u // n
    y = u % n
    if x % 2 == 1:
        y = n - 1 - y
    return [x, y]


def roll_dice(canvas, size, player_position):
    """
    掷骰子，移动玩家

    canvas: 画布对象
    size: 棋盘大小
    player_position: 玩家的位置，[行, 列]
    """

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

    loc = get(v)

    move_player(canvas, size, getXYbyPosition(loc), nowPlayer)
    nowPlayer = (nowPlayer + 1) % players

    w = Winner()
    if len(w) > 0:
        print(w)
        print("Wins")
        win(w[0] + 1)


def win(player):
    msg = messagebox.showinfo("GAME OVER", f"Player{player} WIN!!!")


def getXYbyPosition(player_position):
    """

    player_position: 玩家的位置，[行, 列]
    """
    x, y = player_position
    x_pixel = y * 40 + 5
    y_pixel = x * 40 + 5
    return [x_pixel, y_pixel]


def move_player(canvas, size, player_position, player):
    """
    移动玩家

    canvas: 画布对象
    size: 棋盘大小
    player_position: 玩家的位置，[行, 列]
    steps: 移动的步数
    """
    x, y = player_position
    global player_token

    canvas.delete(player_token[player])

    i = player
    player_token[i] = canvas.create_oval(x + dx[i], y + dy[i], x + S + dx[i], y + S + dy[i], fill=color[i])

    canvas.update()
    canvas.after(500)  # 可视化时的暂停时间


# def choose(player_number_var, difficulty_var):
#     """
#     选择玩家和难度级别
#
#     player_number_var: 玩家选择的变量对象
#     difficulty_var: 难度选择的变量对象
#     """
#     print("Selected Player:", player_number_var.get())
#     print("Selected Difficulty:", difficulty_var.get())

def draw():
    global playerLocation
    playerLocation = [0] * players
    root = tk.Tk()
    size = board[level]

    title_button = tk.Button(root, text='Snakes and Ladders Game', font='Arial 18')
    title_button.pack()

    canvas = tk.Canvas(root, width=size * 40, height=size * 40, bg='white')
    canvas.pack()

    draw_board(canvas, size)

    player_position = [0, 0]

    global player_token

    print(players)
    for i in range(players):
        x, y = getXYbyPosition([0, 0])
        player_token.append(canvas.create_oval(x + dx[i], y + dy[i], x + S + dx[i], y + S + dy[i], fill=color[i]))
    canvas.update()

    # 掷骰子按钮
    roll_button = tk.Button(root, text='Roll Dice', command=lambda: roll_dice(canvas, size, player_position))
    roll_button.pack()

    # 不想玩儿了按钮
    def close_window():
        root.destroy()

    Quit_button = tk.Button(root, text="QUIT", command=close_window)
    Quit_button.pack()
    root.mainloop()


def start():
    Snakes_and_Ladders_Game = tk.Tk()
    title_button = tk.Button(Snakes_and_Ladders_Game, text='Snakes_and_Ladders_Game', font='Arial 18')
    title_button.pack()
    # 玩家选择

    player_number_var = tk.StringVar()
    player_number_var.set("1 Player")  # 默认值
    player_menu = tk.OptionMenu(Snakes_and_Ladders_Game, player_number_var, "1 Player", "2 Players", "3 Players", "4 Players", "5 Players")
    player_menu.pack()

    difficulty_var = tk.StringVar()
    difficulty_var.set("level 1")  # Default value
    difficulty_menu = tk.OptionMenu(Snakes_and_Ladders_Game, difficulty_var, "level 1", "level 2", "level 3")
    difficulty_menu.pack()

    # 完成设置按钮
    Start_button = tk.Button(Snakes_and_Ladders_Game, text='START', command=lambda: choose(player_number_var, difficulty_var))
    Start_button.pack()

    # 难度选择
    def choose(player_number_var, difficulty_var):
        """
        选择玩家和难度级别

        player_number_var: 玩家选择的变量对象

        difficulty_var: 难度选择的变量对象
        """

        level_text = difficulty_menu.cget('text')
        global level
        level = int(level_text.strip("level")) - 1  # 提取级别数字并减去1以匹配索引
        size = board[level]
        u = int(player_number_var.get().split(" ")[0])
        print("Selected Player:", u)
        print("Selected Difficulty:", level_text)
        print("Board Size:", size)

        global players
        players = u
        global end
        end = numCell[level] - 1
        Snakes_and_Ladders_Game.destroy()
        draw()

    Snakes_and_Ladders_Game.mainloop()


start()

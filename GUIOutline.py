import tkinter as tk
from random import randint

# 默认棋盘大小
board = [5, 6, 10]


def draw_board(canvas, size):
    """
    绘制棋盘格子

    canvas: 画布对象
    size: 棋盘大小
    """
    num_cells = size * size

    for i in range(1, num_cells):
        if i % size == 0:
            for j in range(size):
                canvas.create_rectangle(j * 40, (i - 1) * 40, (j + 1) * 40, i * 40, fill='lightblue')
        else:
            for j in range(size - 1, -1, -1):
                canvas.create_rectangle(j * 40, (i - 1) * 40, (j + 1) * 40, i * 40, fill='lightblue')


def roll_dice(canvas, size, player_position):
    """
    掷骰子，移动玩家

    canvas: 画布对象
    size: 棋盘大小
    player_position: 玩家的位置，[行, 列]
    """
    dice_value = randint(1, 6)
    move_player(canvas, size, player_position, dice_value)


def move_player(canvas, size, player_position, steps):
    """
    移动玩家

    canvas: 画布对象
    size: 棋盘大小
    player_position: 玩家的位置，[行, 列]
    steps: 移动的步数
    """
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
        canvas.after(500)  # 可视化时的暂停时间

        if player_position[0] * size + player_position[1] == num_cells - 1:
            print("Player reached the end of the board!")


def update_player_token_position(canvas, size, player_position):
    """
    更新玩家的标记位置

    canvas: 画布对象
    size: 棋盘大小
    player_position: 玩家的位置，[行, 列]
    """
    x, y = player_position
    x_pixel = y * 40 + 5
    y_pixel = x * 40 + 5
    canvas.coords(player_token, x_pixel, y_pixel)


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
    root = tk.Tk()
    level = 0
    size = board[level]

    canvas = tk.Canvas(root, width=size * 40, height=size * 40, bg='white')
    canvas.pack()

    draw_board(canvas, size)

    player_position = [0, 0]
    global player_token
    player_token = canvas.create_oval(5, 5, 25, 25, fill='blue')

    # 玩家选择
    player_number_var = tk.StringVar()
    player_number_var.set("1")  # 默认值
    player_menu = tk.OptionMenu(root, player_number_var, "1", "2", "3", "4", "5")
    player_menu.pack()

    # 难度选择
    def choose(player_number_var, difficulty_var):
        """
        选择玩家和难度级别

        player_number_var: 玩家选择的变量对象
        difficulty_var: 难度选择的变量对象
        """
        level_text = difficulty_menu.cget('text')
        level = int(level_text.strip("level")) - 1  # 提取级别数字并减去1以匹配索引
        size = board[level]

        print("Selected Player:", player_number_var.get())
        print("Selected Difficulty:", level_text)
        print("Board Size:", size)

    difficulty_var = tk.StringVar()
    difficulty_var.set("level 1")  # Default value
    difficulty_menu = tk.OptionMenu(root, difficulty_var, "level 1", "level 2", "level 3")
    difficulty_menu.pack()

    # 掷骰子按钮(待关联)
    roll_button = tk.Button(root, text='Roll Dice', command=lambda: roll_dice(canvas, size, player_position))
    roll_button.pack()

    # 完成设置按钮(最后要能开始进入board界面)
    Start_button = tk.Button(root, text='START', command=lambda: choose(player_number_var, difficulty_var))
    Start_button.pack()

    # 不想玩儿了按钮
    def close_window():
        root.destroy()
    Quit_button = tk.Button(root, text="QUIT", command=close_window)
    Quit_button.pack()
    root.mainloop()


draw()
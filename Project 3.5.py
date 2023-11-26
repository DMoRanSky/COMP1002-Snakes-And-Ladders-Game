"""
3.0: 增加了title，加上了数字，修改了一些细枝末节的东西
3.1: Win()函数让结束的时候有窗口显示
3.2 改了变量名，在 draw 的时候调用 generateSnakeAndLadderPostion
3.3 画了蛇
3.4 降低了蛇和梯子的数量，画了梯子，把输出的格子编号也是 1开始对应了一下
3.5 注释翻译了一遍成英文，避免了梯子起点是 1
"""

"""
3.0: Added title, added numbers, and modified some details
3.1: Win() function allows a window to be displayed at the end
3.2 Changed the variable name and called generateSnakeAndLadderPostion when drawing
3.3 Draw a snake
3.4 The number of snakes and ladders was reduced, ladders were drawn, and the output grid number was also 1 and started to correspond.
3.5 Comments translated into English
"""


import tkinter as tk
import random
import math
import os
from tkinter import messagebox

# 0: Easy, 1 : Medium, 2: Hard
level = 2

# 默认棋盘大小 
# Default board size
board = [5, 6, 10]
numCell = [5 * 5, 6 * 6, 10 * 10]

players = 3

# 该谁投色子
# Who should cast the dice?
nowPlayer = 0

# 每个玩家的位置，玩家编号 0 ~ players - 1 待赋值
# Position of each player, player number 0 ~ players - 1 to be assigned
playerLocation = []
end = 0

snakes = []
ladders = []
sresolution = 40

NumberOfSnakes = [2, 4, 6]
NumberOfLadder = [4, 4, 4]

# set
Set = {}

# 每一個格子的坐標
# The coordinates of each grid
rect_coords = []

#返回一個list，裏面包括把x1,y1和x2,y2連起的直綫上分成n段的點
#Return a list, which includes the points divided into n segments on the straight line connecting x1, y1 and x2, y2
def getPointsOnLine(x1, x2, y1, y2, n): 
	linelist = []
	linelength = ((x2-x1)**2+(y2-y1)**2)**0.5
	segmentlength = linelength/n
	for i in range(1,n):
		temp = i*segmentlength/linelength
		linelist.append([(1-temp)*x1+temp*x2,(1-temp)*y1+temp*y2])
	return linelist
	
#返回把x1,y1和x2,y2連起的直綫上分成n段的第t個點的x坐標和y坐標，從(x1,y1)數起
# Returns the x coordinate and y coordinate of the tth point on the straight line connecting x1, y1 and x2, y2 divided into n segments, counting from (x1, y1)	
def getPointOnLine(x1, x2, y1, y2, n, t): 
	linelength = ((x2-x1)**2+(y2-y1)**2)**0.5
	temp = t*(linelength/n)/linelength
	return (1-temp)*x1+temp*x2,(1-temp)*y1+temp*y2


# 返回綫(x1,y1)(x2,y2)和綫(x3,y3)(x4,y4)的交叉點
# Return the intersection of line (x1, y1) (x2, y2) and line (x3, y3) (x4, y4)
def getIntersection(x1, y1, x2, y2, x3, y3, x4, y4): 
	return ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)), ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
	


# Task 2
def getRandomNumber():
	return random.randint(1, 6)


# Task 3

# 一个在 x 跳到 y 走到哪
# One jumps from x to y and goes wherever
def jump(x, y):
	return min(x + y, end)


color = ['red', 'yellow', 'blue', 'black', 'green']

## 圆的大小
## Circle size
S = 10

## 间隔
## Interval
V = 2

dx = [0, 0, 0, S + V, S + V]
dy = [0, S + V, 2 * S + 2 * V, 0, S + V]

player_token = []


def generateSnakeAndLadderPostion():
	for i in range(NumberOfSnakes[level]):
		while 1:
			num = numCell[level]
			c = [random.randint(0, num - 1), random.randint(0, num - 1)]

			if c[0] == c[1] or c[0] < c[1] or c[0] in Set or c[1] in Set or c[0] == end:
				continue
			snakes.append(c)
			Set[c[0]] = 1
			Set[c[1]] = 1
			break
	
	for i in range(NumberOfLadder[level]):
		while 1:
			num = numCell[level]
			c = [random.randint(0, num - 1), random.randint(0, num - 1)]
			if c[0] == c[1] or c[0] > c[1] or c[0] in Set or c[1] in Set or c[0] == 0:
				continue
			ladders.append(c)
			Set[c[0]] = 1
			Set[c[1]] = 1
			break


# Task 4


def Winner():
	res = []
	for i in range(players):
		if playerLocation[i] == end:
			res.append(i)
	return res

# Task1
def draw_board(canvas, size):
	global rect_coords
	rect_coords.clear()
	"""
	绘制棋盘格子

	canvas: 画布对象
	size: 棋盘大小
	"""

	"""
	Draw a checkerboard pattern

	canvas: canvas object
	size: chessboard size
	"""
	num_cells = size * size
	rect_coords = [0]*(num_cells)
	# 修改循环范围，包括最后一个格子; William:已把 range(1, num_cells + 1) 修改爲 range(1, size + 1)
	# Modify the loop range, including the last cell; William: range(1, num_cells + 1) has been modified to range(1, size + 1)
	for i in range(1, size + 1):  
		if i % 2 == 1:
			m = 1
			for j in range(size):
				x1 = j * 40
				y1 = (i - 1) * 40
				x2 = (j + 1) * 40
				y2 = i * 40
				# 绘制矩形 
				# Draw a rectangle
				canvas.create_rectangle(x1, y1, x2, y2, fill='lightblue')  
				# 计算数字的位置
				# Calculate the position of a number
				text_x = (x1 + x2) / 2
				text_y = (y1 + y2) / 2
				m = (i - 1) * size + j + 1
				 # 显示数字 
				 # Display numbers
				canvas.create_text(text_x, text_y, text=str(m), font=("Arial", 12)) 
				# 將矩形的坐標放進rect_coords里
				# Put the coordinates of the rectangle into rect_coords
				rect_coords[m-1] = [(x1+x2)/2,(y1+y2)/2] 

		else:
			for j in range(size - 1, -1, -1):
				x1 = j * 40
				y1 = (i - 1) * 40
				x2 = (j + 1) * 40
				y2 = i * 40
				# 绘制矩形
				# Draw a rectangle
				canvas.create_rectangle(x1, y1, x2, y2, fill='lightblue')  
				
				# 计算数字的位置
				# Calculate the position of a number
				text_x = (x1 + x2) / 2
				text_y = (y1 + y2) / 2
				m = i * size - j
				# 显示数字
				# Display numbers
				canvas.create_text(text_x, text_y, text=str(m), font=("Arial", 12))  
				 # 將矩形的坐標放進rect_coords里
				 # Put the coordinates of the rectangle into rect_coords
				rect_coords[m-1] = [(x1+x2)/2,(y1+y2)/2]


# 给 0 到 ~ 格子编号返回行列号
# Give the grid numbers from 0 to ~ and return the row and column numbers.
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
	"""
	Roll the dice, move players

	canvas: canvas object
	size: chessboard size
	player_position: player's position, [row, column]
	"""

	print("Snakes: ")
	for i in snakes:
		print(f"{ i[0] + 1} -> {i[1] + 1}")
	print("Ladders: ")
	for i in ladders:
		print(f"{ i[0] + 1} -> {i[1] + 1}")
	for i in range(players):
		print(f'{i} is at {playerLocation[i] + 1}')
	global nowPlayer
	print(f"It's {nowPlayer} turns, please click enter to get dice toll")
	x = getRandomNumber()
	print(f"Dice number is {x}")

	u = playerLocation[nowPlayer]
	v = jump(u, x)
	print(f"{nowPlayer} move to {v + 1}")

	for i in snakes:
		if v == i[0]:
			print(f"{nowPlayer} Encountered a snake and fell into {i[1] + 1}")
			v = i[1]

	for i in ladders:
		if v == i[0]:
			print(f"{nowPlayer} Encountered a ladder and fell into {i[1] + 1}")
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

	"""
	Player position, [row, column]
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

	"""
	move player

	canvas: canvas object
	size: chessboard size
	player_position: player's position, [row, column]
	steps: number of steps to move
	"""
	x, y = player_position
	global player_token

	canvas.delete(player_token[player])

	i = player
	player_token[i] = canvas.create_oval(x + dx[i], y + dy[i], x + S + dx[i], y + S + dy[i], fill=color[i])

	canvas.update()
	canvas.after(500)  # 可视化时的暂停时间


# def choose(player_number_var, difficulty_var):
#	 """
#	 选择玩家和难度级别
#
#	 player_number_var: 玩家选择的变量对象
#	 difficulty_var: 难度选择的变量对象
#	 """
#	 print("Selected Player:", player_number_var.get())
#	 print("Selected Difficulty:", difficulty_var.get())

def draw_snakes(canvas):
	'''
		snake drawer(why did I chose to do this😭）
	'''
	snakes_coords = []
	snakes_sizes = []
	for item in snakes:
		snakes_coords.append([[rect_coords[item[0]][0]+12,rect_coords[item[0]][1]+12],0,0,[rect_coords[item[1]][0]+12,rect_coords[item[1]][1]+12]])
	for item in snakes_coords: #This for loop generates two random dots on perpendicular lines. Those perpendicular lines are on another line wich connects the start of the snake to the end of the snake, such that those perpendicular lines cut the other line into 3 sections 
		if item[3][0]-item[0][0] == 0:
			slope = 0
		elif (item[3][1]-item[0][1])/(item[3][0]-item[0][0]) == 0:
			slope = 999
		else:
			slope = (-1)/((item[3][1]-item[0][1])/(item[3][0]-item[0][0]))
		midpoint1, midpoint2 = getPointsOnLine(item[0][0],item[3][0],item[0][1],item[3][1],3)
		r = (1+slope**2)**0.5
		side = [-1,1][random.randrange(2)]
		proportionaterange = int(((item[3][0]-item[0][0])**2+(item[3][1]-item[0][1])**2)**0.5)
		randomint = random.randint(0,proportionaterange)*side
		item[1] = [midpoint1[0]+randomint/r,midpoint1[1]+randomint*slope/r]
		randomint = random.randint(0,proportionaterange)*side*-1
		item[2] = [midpoint2[0]+randomint/r,midpoint2[1]+randomint*slope/r]
		snakes_sizes.append(proportionaterange)
		templinelist = []
	counter = 0
	for item in snakes_coords: #A biezer curve is generated based on the randomly generated points and the point where the snake starts and ends. A snake is drawn on that biezer curve.
		templinelist.append([])
		csresolution = int(sresolution*snakes_sizes[counter]/90)
		for i in range(len(item)-1):
			templinelist[-1].append(getPointsOnLine(item[i][0],item[i+1][0],item[i][1],item[i+1][1],csresolution))
		randomcolour = [0,0,0]
		randomcolour[random.randint(0,2)] = 1
		for i in range(csresolution-1):
			lastlinep1x,lastlinep1y = getPointOnLine(templinelist[-1][0][i][0],templinelist[-1][1][i][0],templinelist[-1][0][i][1],templinelist[-1][1][i][1],csresolution,i)
			lastlinep2x,lastlinep2y = getPointOnLine(templinelist[-1][1][i][0],templinelist[-1][2][i][0],templinelist[-1][1][i][1],templinelist[-1][2][i][1],csresolution,i)
			drawpointx,drawpointy = getPointOnLine(lastlinep1x,lastlinep2x,lastlinep1y,lastlinep2y,csresolution,i)
			size = 4 if i<(csresolution*0.7875) else (csresolution-i)/(csresolution*0.2125)*4
			canvas.create_oval(drawpointx+size,drawpointy+size,drawpointx-size,drawpointy-size,fill=("green"*(i%2)+"yellow"*(1-(i%2)))*randomcolour[0]+("red"*(i%2)+"brown"*(1-(i%2)))*randomcolour[1]+("blue"*(i%2)+"purple"*(1-(i%2)))*randomcolour[2],outline="")
		counter += 1
	'''
		end of snake drawer
	'''

def draw_ladders(canvas):
	for i in ladders:
		s = getXYbyPosition(get(i[0]))
		t = getXYbyPosition(get(i[1]))
		s[0] += 15
		s[1] += 15
		t[0] += 15
		t[1] += 15
		# 起点和终点的中心点的位置 (s[0], s[1]) -> (t[0], t[1])
		# Position of the center point of the starting point and end point (s[0], s[1]) -> (t[0], t[1])
		dx = t[0] - s[0]
		dy = t[1] - s[1]
		len = math.sqrt(dx * dx + dy * dy)
		dx /= len
		dy /= len
		# 方向单位向量
		# Direction unit vector
		X = dy
		Y = -dx
		# 旋转 90 读的 法向量，各偏移 20 个
		# Rotate the normal vectors read by 90, offset by 20 each
		X *= 10
		Y *= 10
		
		## create_line(x1, y1, x2, y2) 画 (x1, y1) -> (x2, y2) 的线
		## create_line(x1, y1, x2, y2) draws the line (x1, y1) -> (x2, y2)
		canvas.create_line(s[0] + X, s[1] + Y, t[0] + X, t[1] + Y, fill='brown', width=3)
		canvas.create_line(s[0] - X, s[1] - Y, t[0] - X, t[1] - Y, fill='brown', width=3)

		# 隔 20 个像素一个梯子中间的那个横着的线
		# The horizontal line in the middle of the ladder every 20 pixels
		Z = 15
		dx *= Z
		dy *= Z
		now = 0
		x1, y1 = s[0] + X, s[1] + Y
		x2, y2 = s[0] - X, s[1] - Y
		while now + Z * 2 <= len:
			x1 += dx
			y1 += dy
			x2 += dx
			y2 += dy
			canvas.create_line(x1, y1, x2, y2, fill='brown', width=3)
			now += Z		
	

def draw():
	global playerLocation
	playerLocation = [0] * players
	root = tk.Tk()
	size = board[level]
	generateSnakeAndLadderPostion()

	title_button = tk.Button(root, text='Snakes and Ladders Game', font='Arial 18')
	title_button.pack()

	canvas = tk.Canvas(root, width=size * 40, height=size * 40, bg='white')
	canvas.pack()
	draw_board(canvas, size)
	
	draw_snakes(canvas)
	draw_ladders(canvas)

	player_position = [0, 0]

	global player_token

	print(players)
	for i in range(players):
		x, y = getXYbyPosition([0, 0])
		player_token.append(canvas.create_oval(x + dx[i], y + dy[i], x + S + dx[i], y + S + dy[i], fill=color[i]))
	canvas.update()

	# 掷骰子按钮
	# Roll dice button
	roll_button = tk.Button(root, text='Roll Dice', command=lambda: roll_dice(canvas, size, player_position))
	roll_button.pack()

	# 不想玩儿了按钮
	# button: Don’t want to play anymore 
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
	# Player choice
	player_number_var = tk.StringVar()
	# 默认值
	# default value
	player_number_var.set("1 Player")  
	player_menu = tk.OptionMenu(Snakes_and_Ladders_Game, player_number_var, "1 Player", "2 Players", "3 Players", "4 Players", "5 Players")
	player_menu.pack()

	difficulty_var = tk.StringVar()
	# Default value
	difficulty_var.set("level 1")  
	difficulty_menu = tk.OptionMenu(Snakes_and_Ladders_Game, difficulty_var, "level 1", "level 2", "level 3")
	difficulty_menu.pack()

	# 完成设置按钮
	# Complete setup button
	Start_button = tk.Button(Snakes_and_Ladders_Game, text='START', command=lambda: choose(player_number_var, difficulty_var))
	Start_button.pack()

	# 难度选择
	# Difficulty selection
	def choose(player_number_var, difficulty_var):
		"""
		选择玩家和难度级别
		player_number_var: 玩家选择的变量对象
		difficulty_var: 难度选择的变量对象
		"""

		"""
		Choose player and difficulty level
		player_number_var: variable object selected by the player
		difficulty_var: variable object for difficulty selection
		"""

		level_text = difficulty_menu.cget('text')
		global level
		# 提取级别数字并减去1以匹配索引
		# Extract the level number and subtract 1 to match the index
		level = int(level_text.strip("level")) - 1  
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
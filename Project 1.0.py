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


while True:
    #os.system("cls")
    w = Winner()
    if len(w) > 0:
        print(w)
        print("Wins")
        break
    print("蛇",snakes)
    print("梯子", ladders)
    for i in range(players):
        print(f'{i} is at {playerLocation[i]}')
    print(f"It's {nowPlayer} turns, please click enter to get dice toll")
    a = input()
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
  
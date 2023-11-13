import pygame, sys
from pygame.locals import *
from collections import deque
from tkinter import *
from tkinter import messagebox
import heapq

pygame.init()
Tk().wm_withdraw()

WINDOW_SIZE = 600

surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
 
whiteColor = (255, 255, 255)
redColor = (255,0,0)
pinkColor = (255,182,193)
yellowColor = (255,255,0)
blackColor = (0,0,0)
greenColor = (0,128,0)

RECT_SIZE = 30

START_X = 0
START_Y = 0

END_X = WINDOW_SIZE-RECT_SIZE
END_Y = WINDOW_SIZE-RECT_SIZE

cells = [[None] * (WINDOW_SIZE//RECT_SIZE) for i in range(WINDOW_SIZE//RECT_SIZE)]
isWall = [[False] * (WINDOW_SIZE//RECT_SIZE) for i in range(WINDOW_SIZE//RECT_SIZE)]

def initCells():
    for i in range(WINDOW_SIZE//RECT_SIZE):
        for j in range(WINDOW_SIZE//RECT_SIZE):
            posY = i*RECT_SIZE
            posX = j*RECT_SIZE

            if posY == START_Y and posX == START_X:
                cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
                pygame.draw.rect(surface, redColor, cells[i][j])
            elif posY == END_Y and posX == END_X:
                cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
                pygame.draw.rect(surface, pinkColor, cells[i][j])
            else:
                cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
                pygame.draw.rect(surface, whiteColor, cells[i][j], width=1)
            pygame.display.flip()

def drawCells():
    for i in range(WINDOW_SIZE//RECT_SIZE):
        for j in range(WINDOW_SIZE//RECT_SIZE):
            posY = i*RECT_SIZE
            posX = j*RECT_SIZE
            mousePos = pygame.mouse.get_pos()
            canDraw = not ((posX == START_X and posY == START_Y) or (posX == END_X and posY == END_Y))
            if cells[i][j].collidepoint(mousePos) and pygame.mouse.get_pressed(num_buttons=3)[0] and canDraw:
                cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
                isWall[i][j] = True
                pygame.draw.rect(surface, yellowColor, cells[i][j])
            elif cells[i][j].collidepoint(mousePos) and pygame.mouse.get_pressed(num_buttons=3)[2] and canDraw:
                cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
                isWall[i][j] = False
                pygame.draw.rect(surface, blackColor, cells[i][j])
                pygame.draw.rect(surface, whiteColor, cells[i][j], width=1)

def dfs(i, j, vis):
    if i < 0 or j < 0 or i >= len(cells) or j >= len(cells[i]) or isWall[i][j]:
        return
    
    posY = i*RECT_SIZE
    posX = j*RECT_SIZE
    cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
    pygame.draw.rect(surface, greenColor, cells[i][j])

    if i == len(cells)-1 and j == len(cells[i])-1:
        messagebox.showinfo('Continue','Done!')
        sys.exit()
        return
    
    pygame.display.update()
    pygame.time.delay(20)

    if (i,j) not in vis:
        vis.add((i, j))
        dfs(i+1, j, vis)
        dfs(i, j+1, vis)
        dfs(i-1, j, vis)
        dfs(i, j-1, vis)

def bfs():
    dq = deque([(START_X, START_Y)])
    seen = set()
    while dq:
        i, j = dq.popleft()
        
        if i < 0 or j < 0 or i >= len(cells) or j >= len(cells[i]) or isWall[i][j]:
            continue
        
        posY = i*RECT_SIZE
        posX = j*RECT_SIZE
        cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
        pygame.draw.rect(surface, greenColor, cells[i][j])
        
        if i == len(cells)-1 and j == len(cells[i])-1:
            messagebox.showinfo('Continue','Done!')
            sys.exit()
            return
        
        if (i+1, j) not in seen:
            dq.append((i+1, j))
            seen.add((i+1, j))
        if (i, j+1) not in seen:
            dq.append((i, j+1))
            seen.add((i, j+1))
        if (i-1, j) not in seen:
            dq.append((i-1, j))
            seen.add((i-1, j))
        if (i, j-1) not in seen:
            dq.append((i, j-1))
            seen.add((i, j-1))

        pygame.display.update()
        pygame.time.delay(20)

def dijkstra():
    endGoalX = len(cells[0])-1
    endGoalY = len(cells)
    heap = [(0, 0, 0, [])]
    seen = set()
    
    finalPath = [(0, 0)]

    while heap:
        cost, i, j, path = heapq.heappop(heap)
        
        if i >= len(cells) or j >= len(cells[i]) or isWall[i][j]:
            continue

        if i == len(cells) - 1 and j == len(cells[i]) - 1:
            finalPath = path[:]
            break
        
        path.append((i,j))
        if (i+1, j) not in seen and i+1 < len(cells):
            heapq.heappush(heap, (cost+1, i+1, j, path.copy()))
            seen.add((i+1, j))
        if (i, j+1) not in seen and j+1 < len(cells[i]):
            heapq.heappush(heap, (cost+1, i, j+1, path.copy()))
            seen.add((i, j+1))
        if (i-1, j) not in seen and i-1 >= 0:
            heapq.heappush(heap, (cost+1, i-1, j, path.copy()))
            seen.add((i-1, j))
        if (i, j-1) not in seen and j-1 >= 0:
            heapq.heappush(heap, (cost+1, i, j-1, path.copy()))
            seen.add((i, j-1))

    for i,j in finalPath:        
        posY = i*RECT_SIZE
        posX = j*RECT_SIZE
        cells[i][j] = pygame.Rect(posX, posY, RECT_SIZE, RECT_SIZE)
        pygame.draw.rect(surface, greenColor, cells[i][j])

        pygame.display.update()
        pygame.time.delay(20)

    messagebox.showinfo('Continue','Done!')
    sys.exit()

initCells()
while True:
    drawCells()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                dfs(START_X, START_Y, set())
            elif event.key==pygame.K_b:
                bfs()
            elif event.key==pygame.K_j:
                dijkstra()
    pygame.display.update()
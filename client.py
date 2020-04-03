import socket
import threading
import os
import random
import sys
import time
import pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 600 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

CAM_MOVE_SPEED = 5 # how many pixels per frame the camera moves

# The percentage of outdoor tiles that have additional
# decoration on them, such as a tree or rock.
OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = (  0, 170, 255)
WHITE      = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

def create_connect():
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    # 设置端口号
    port = 9999
    # 连接服务，指定主机和端口
    s.connect((host, port))
    t = threading.Thread(target=process, args=(s,))
    t.start()
    return s

def process(serversocket):
    while True:
        # 这里用于接受服务端同步数据
        data = serversocket.recv(1024).decode('utf-8')
        print (data)
        # 更新游戏画面

def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['start interface'].get_rect()
    topCoord = 0 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Move to any city to collect item',
                       'Sale item to earn coin, get 30 coin will win',
                       'Arrow key move truck, number key use card, enter confirm current operation',
                       'Press any key entering game, Esc to quit',
                       ]

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['start interface'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def terminate():
    pygame.quit()
    sys.exit()

def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, ROLEMAPPING, BASICFONT

    # Pygame initialization and basic set up of the global variables.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('Truck Driver')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    # A global dict value that will contain all the Pygame
    # Surface objects returned by pygame.image.load().
    IMAGESDICT = {'start interface': pygame.image.load('pic/StartInterface.jpeg'),
                  'princess': pygame.image.load('pic/princess.png'),
                  'boy': pygame.image.load('pic/boy.png'),
                  'catgirl': pygame.image.load('pic/catgirl.png'),
                  'horngirl': pygame.image.load('pic/horngirl.png'),
                  'pinkgirl': pygame.image.load('pic/pinkgirl.png'),
                  'rock': pygame.image.load('pic/Rock.png'),
                  'city': pygame.image.load('pic/Wall_Block_Tall.png'),
                  'park': pygame.image.load('pic/Plain_Block.png'),
                  }

    ROLEMAPPING = {'1': IMAGESDICT['princess'],
                  '2': IMAGESDICT['boy'],
                  '3': IMAGESDICT['catgirl'],
                  '4': IMAGESDICT['horngirl']}

    # These dict values are global, and map the character that appears
    # in the level file to the Surface object it represents.
    # TILEMAPPING = {'x': IMAGESDICT['corner'],
    #                '#': IMAGESDICT['wall'],
    #                'o': IMAGESDICT['inside floor'],
    #                ' ': IMAGESDICT['outside floor']}
    # OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
    #                       '2': IMAGESDICT['short tree'],
    #                       '3': IMAGESDICT['tall tree'],
    #                       '4': IMAGESDICT['ugly tree']}

    # PLAYERIMAGES is a list of all possible characters the player can be.
    # PLAYERIMAGES = [IMAGESDICT['red truck'],
    #                 IMAGESDICT['blue truck'],
    #                 IMAGESDICT['white truck'],
    #                 IMAGESDICT['grey truck']]

    startScreen()  # 开始画面
    # server_socket = create_connect()  # 与服务器建立连接

    # 载入地图
    maps = [['#', '#', '#', '#', '#', '#'],
            ['#', ' ', '#', ' ', '#', ' '],
            ['#', '#', '1', '2', '#', '#'],
            ['#', ' ', '3', '4', '#', ' '],
            ['#', '#', '#', '#', '#', '#'],
            ['#', ' ', '#', ' ', '#', ' '],]

    # 游戏开始
    # 生成本局地图
    mapSurf = generate_game_surface(maps)
    while True:  # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate() # Esc key quits.
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pass
            elif event.type == MOUSEMOTION:
                pass
        DISPLAYSURF.fill(BGCOLOR)
        mapSurfRect = mapSurf.get_rect()
        # 将游戏地图中心坐标设为窗口中心
        mapSurfRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

        # Draw mapSurf to the DISPLAYSURF Surface object.
        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        pygame.display.update()  # draw DISPLAYSURF to the screen.
        FPSCLOCK.tick()

def generate_game_surface(map):
    mapSurfWidth = len(map) * TILEWIDTH
    mapSurfHeight = (len(map[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)

    for x in range(len(map)):
        for y in range(len(map[x])):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if map[x][y] == '#':
                obj = IMAGESDICT['rock']
            elif map[x][y] == ' ':
                obj = IMAGESDICT['park']
            elif map[x][y] in ['1', '2', '3', '4']:
                obj = ROLEMAPPING[map[x][y]]
            mapSurf.blit(obj, spaceRect)
    return mapSurf

if __name__ == '__main__':
    main()



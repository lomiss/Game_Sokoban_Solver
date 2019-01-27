# _*_ coding:utf-8 _*_
__author__ = 'lomiss'
__data__ = '2018/12/10 19:10'

import random
import sys
import copy
import os
import pygame
from pygame.locals import *
from Python_BFS import BFS
from C_DLL import C_algo


pygame.init()

# 帧率
FPS = 30
# 宽高
WINWIDTH = 600
WINHEIGHT = 500
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# 定义游戏地图中每个方块的大小
TILEWIDTH = 50
TILEHEIGHT = 85
# 瓷板地板高度
TILEFLOORHEIGHT = 40

OUTSIDE_DECORATION_PCT = 20

# 颜色定义
BRIGHTBLUE = (156, 156, 156)
WHITE = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

# 方向定义
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 地图文本
level_text_list = []


# 主函数(预处理工作)
def main():
    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

    # pygame初始化，加载游戏时钟
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # 加载游戏主窗口，宽高，标题，字体等
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('welcome to play Sokoban')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    # 从源文件加载图片
    IMAGESDICT = {'uncovered goal': pygame.image.load('images/RedSelector.png'),
                  'covered goal': pygame.image.load('images/Selector.png'),
                  'star': pygame.image.load('images/Star.png'),
                  'corner': pygame.image.load('images/Wall_Block_Tall.png'),
                  'wall': pygame.image.load('images/Wood_Block_Tall.png'),
                  'inside floor': pygame.image.load('images/Plain_Block.png'),
                  'outside floor': pygame.image.load('images/Grass_Block.png'),
                  'title': pygame.image.load('images/star_title.png'),
                  'solved': pygame.image.load('images/star_solved.png'),
                  'princess': pygame.image.load('images/princess.png'),
                  'boy': pygame.image.load('images/boy.png'),
                  'catgirl': pygame.image.load('images/catgirl.png'),
                  'horngirl': pygame.image.load('images/horngirl.png'),
                  'pinkgirl': pygame.image.load('images/pinkgirl.png'),
                  'rock': pygame.image.load('images/Rock.png'),
                  'short tree': pygame.image.load('images/Tree_Short.png'),
                  'tall tree': pygame.image.load('images/Tree_Tall.png'),
                  'ugly tree': pygame.image.load('images/Tree_Ugly.png')}

    # 定义地图皮肤
    TILEMAPPING = {'x': IMAGESDICT['corner'],
                   '#': IMAGESDICT['wall'],
                   'o': IMAGESDICT['inside floor'],
                   ' ': IMAGESDICT['outside floor']}
    # 定义装饰物皮肤
    OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                          '2': IMAGESDICT['short tree'],
                          '3': IMAGESDICT['tall tree'],
                          '4': IMAGESDICT['ugly tree']}

    # 定义玩家皮肤
    currentImage = 0
    PLAYERIMAGES = [IMAGESDICT['princess'],
                    IMAGESDICT['boy'],
                    IMAGESDICT['catgirl'],
                    IMAGESDICT['horngirl'],
                    IMAGESDICT['pinkgirl']]

    # 当用户按下任意键后进入游戏
    startScreen()

   # 读取文本信息，获取宽度和高度，以及每个坐标代表的信息，同时将每个关卡信息转为文本，方便自动推箱子算法读取
    levels = readLevelsFile('Levels.txt')
    currentLevelIndex = 0
    for i in range(len(levels)):
        level_text = ""
        for each in levels[i].get('mapObj'):
            s = "".join(each)
            level_text += s
        level_text_list.append(level_text)
    # 开始游戏主循环，为每一个关卡循环，当前关卡完成后，下一关卡进行新的循环
    while True:
        # 将地图和当前关数传入读取关数函数
        result = runLevel(levels, currentLevelIndex)
        if result in ('solved', 'next'):
            # 进行下一关，并将当前关卡数加1
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                # 进行到最后一关时，跳至第一关
                currentLevelIndex = 0
        elif result == 'back':
            # 返回到上一关
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                # 从第一关直接跳至最后一关
                currentLevelIndex = len(levels)-1
        elif result == 'reset':
            pass


# 运行地图
def runLevel(levels, levelNum):
    global currentImage
    # 获取当前关卡对象
    levelObj = levels[levelNum]
    # 装饰地图
    mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
    # 将地图关键信息拷贝，以便游戏进行时修改
    gameStateObj = copy.deepcopy(levelObj['startState'])
    # 初始化变量，重新绘制为真
    mapNeedsRedraw = True
    # 定义地图额外信息
    levelSurf = BASICFONT.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, WINHEIGHT - 35)
    # 初始化关卡通过为False
    levelIsComplete = False
    # 定义视角偏移参数
    cameraOffsetX = 0
    cameraOffsetY = 0
    # 初始化路径
    path = ""

    # 游戏主循环
    while True:
        # 重置变量
        playerMoveTo = None
        keyPressed = False
        # 开始事件监听
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                # 获取人物移动方向
                keyPressed = True
                if event.key == K_LEFT:
                    playerMoveTo = UP
                elif event.key == K_RIGHT:
                    playerMoveTo = DOWN
                elif event.key == K_UP:
                    playerMoveTo = LEFT
                elif event.key == K_DOWN:
                    playerMoveTo = RIGHT

                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'
                # 暂停
                elif event.key == K_ESCAPE:
                    terminate()
                # 重置
                elif event.key == K_BACKSPACE:
                    return 'reset'
                # 更换人物皮肤
                elif event.key == K_p:
                    currentImage += 1
                    if currentImage >= len(PLAYERIMAGES):
                        # 若为最后一个，跳至第一个
                        currentImage = 0
                    mapNeedsRedraw = True
                # 若为1键，开始C_BFS算法
                elif event.key == K_1:
                    auto_game = C_algo(level_text_list[levelNum], levels[levelNum].get('width'))
                    path = auto_game.C_BFS()
                # 若为2键，开始C_Astar算法
                elif event.key == K_2:
                    auto_game = C_algo(level_text_list[levelNum], levels[levelNum].get('width'))
                    path = auto_game.C_Astar()
                # 若为3键，开始C_DFS算法
                elif event.key == K_3:
                    auto_game = C_algo(level_text_list[levelNum], levels[levelNum].get('width'))
                    path = auto_game.C_DFS()
                # 若为4键，开始Py_BFS算法
                elif event.key == K_4:
                    auto_game = BFS(level_text_list[levelNum], levels[levelNum].get('width'))
                    path = auto_game.gen_shortest_paths()[0]

        if path != "":
            for each in path:
                pygame.time.delay(150)
                if each == 'u' or each == 'U':
                    playerMoveTo = LEFT
                elif each == 'd' or each == 'D':
                    playerMoveTo = RIGHT
                elif each == 'l' or each == 'L':
                    playerMoveTo = UP
                elif each == 'r' or each == 'R':
                    playerMoveTo = DOWN
                moved = makeMove(mapObj, gameStateObj, playerMoveTo)
                if moved:
                    gameStateObj['stepCounter'] += 1
                    mapNeedsRedraw = True
                DISPLAYSURF.fill(BGCOLOR)
                if mapNeedsRedraw:
                    mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals'])
                    mapNeedsRedraw = False
                mapSurfRect = mapSurf.get_rect()
                mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)

                DISPLAYSURF.blit(mapSurf, mapSurfRect)
                DISPLAYSURF.blit(levelSurf, levelRect)
                stepSurf = BASICFONT.render('Steps: %s' % (gameStateObj['stepCounter']), 1, TEXTCOLOR)
                stepRect = stepSurf.get_rect()
                stepRect.bottomleft = (20, WINHEIGHT - 10)
                DISPLAYSURF.blit(stepSurf, stepRect)
                pygame.display.update()
                FPSCLOCK.tick()
            playerMoveTo = None
            levelIsComplete = True
            keyPressed = False
            path = ""

        if playerMoveTo != None and not levelIsComplete:
            # 控制移动
            moved = makeMove(mapObj, gameStateObj, playerMoveTo)

            # 步数加一
            if moved:
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = True

            # 判断游戏是否结束
            if isLevelFinished(levelObj, gameStateObj):
                levelIsComplete = True
                keyPressed = False

        DISPLAYSURF.fill(BGCOLOR)
        # 是否重新绘制
        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals'])
            mapNeedsRedraw = False

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        DISPLAYSURF.blit(levelSurf, levelRect)
        stepSurf = BASICFONT.render('Steps: %s' % (gameStateObj['stepCounter']), 1, TEXTCOLOR)
        stepRect = stepSurf.get_rect()
        stepRect.bottomleft = (20, WINHEIGHT - 10)
        DISPLAYSURF.blit(stepSurf, stepRect)

        if levelIsComplete:
            solvedRect = IMAGESDICT['solved'].get_rect()
            solvedRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
            DISPLAYSURF.blit(IMAGESDICT['solved'], solvedRect)

            if keyPressed:
                return 'solved'

        pygame.display.update()
        FPSCLOCK.tick()


# 是否是墙
def isWall(mapObj, x, y):
    """判断当前坐标是否为墙"""
    # 判断坐标是否越界
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False
    # 判断是否有墙
    elif mapObj[x][y] in ('#', 'x'):
        return True
    return False


# 装饰地图
def decorateMap(mapObj, startxy):
    """拷贝一份以便修改：
         1.角落的墙壁变成了角落。
         2.外部/内部地板砖不同。
         3.树/岩石装饰随机添加到外部坐标上。"""

    # 获取人物坐标
    startx, starty = startxy

    # 拷贝
    mapObjCopy = copy.deepcopy(mapObj)

    # 将墙内非空地部分替换为空，为非地图元素下方绘制瓷砖
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
                mapObjCopy[x][y] = ' '

    # 以人物坐标为基点，递归绘制成墙内元素'o'
    floodFill(mapObjCopy, startx, starty, ' ', 'o')

    # 遍历墙体，将墙角位置转化为'x'单独用图片绘制
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] == '#':
                if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
                   (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
                   (isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
                   (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'
            # 对墙外空地进行随机绘制
            elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
                mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

    return mapObjCopy


# 是否可以移动
def isBlocked(mapObj, gameStateObj, x, y):
    """如果地图上的（x，y）位置是可以移动的，则返回True
     被墙或者箱子阻挡，否则返回False。"""

    if isWall(mapObj, x, y):
        return True

    # x和y越界。
    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True

    # 被箱子阻挡
    elif (x, y) in gameStateObj['stars']:
        return True

    return False


# 控制移动
def makeMove(mapObj, gameStateObj, playerMoveTo):
    """给定一个地图和游戏状态对象，并且人物的移动方向。 如果可以移动，
    则更改人物位置（和任何推动的星的位置），如果玩家移动则返回True，
    否则返回False。"""

    # 获取人物当前坐标.
    playerx, playery = gameStateObj['player']

    # 获取箱子的坐标
    stars = gameStateObj['stars']

    #根据传进来的参数，对人物移动进行偏移
    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0

    # 判断人物下一个位置是否有墙
    if isWall(mapObj, playerx + xOffset, playery + yOffset):
        return False
    else:
        if (playerx + xOffset, playery + yOffset) in stars:
            # 如果下一个位置有箱子，判断是否可以移动它
            if not isBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery + (yOffset*2)):
                # 移动箱子
                ind = stars.index((playerx + xOffset, playery + yOffset))
                stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
            else:
                return False
        # 更新人物移动后的坐标
        gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
        return True


# 开始界面
def startScreen():
    """显示开始屏幕，直到用户按下任意键后进入游戏"""
    # 开始界面参数初始化.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    instructionText = ['Push the stars over the marks.',
                       'Arrow keys to move, P to change character.',
                       'Backspace to reset level, Esc to quit.',
                       'N for next level, B to go back a level.',
                       '1 2 3 4 for auto play!']

    # 绘制背景颜色
    DISPLAYSURF.fill(BGCOLOR)

    # 显示开始图片
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # 显示游戏帮助
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height
        DISPLAYSURF.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPSCLOCK.tick()


# 读文本地图
def readLevelsFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    # 读取每一行
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()
    levels = []
    levelNum = 0
    mapTextLines = []
    mapObj = []
    for lineNum in range(len(content)):
        # 清洗数据
        line = content[lineNum].rstrip('\r\n')
        # 排除不相关的文本
        if ';' in line:
            line = line[:line.find(';')]
        # 不为空，说明该部分是地图
        if line != '':
            mapTextLines.append(line)
        # 为空，代表着上一关读取完毕，前提是有内容
        elif line == '' and len(mapTextLines) > 0:

            maxWidth = -1
            # 获取该地图的最大宽度
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            # 其余部分不及该宽度，用空格补齐，方便后面绘制以及自动求解算法读取

            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))
            # 将读取的文本进行处理成单个字符存进列字典对象中的列表里，方便读取绘制操作
            # print(mapTextLines)
            # 矩形
            for x in range(len(mapTextLines)):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[y].append(mapTextLines[y][x])
            # print(mapObj)
            # 参数初定义，将开始状态，终点，箱子坐标存进字典中
            startx = None
            starty = None
            goals = []
            stars = []
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    # 存储人物
                    if mapObj[x][y] in ('@', '+'):
                        startx = x
                        starty = y
                    # 存储终点
                    if mapObj[x][y] in ('.', '+', '*'):
                        goals.append((x, y))
                    # 存储箱子
                    if mapObj[x][y] in ('$', '*'):
                        stars.append((x, y))
            # 断言处理
            assert startx != None and starty != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (levelNum+1, lineNum, filename)
            assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (levelNum+1, lineNum, filename)
            assert len(stars) >= len(goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s stars.' % (levelNum+1, lineNum, filename, len(goals), len(stars))

            # 将地图信息存入字典对象中
            gameStateObj = {'player': (startx, starty),
                            'stepCounter': 0,
                            'stars': stars}
            levelObj = {'width': maxWidth,
                        'height': len(mapObj),
                        'mapObj': mapObj,
                        'goals': goals,
                        'startState': gameStateObj}

            levels.append(levelObj)

            # 重置变量，以便读取下一关的信息
            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelNum += 1
    return levels


# 对墙内元素递归替换
def floodFill(mapObj, x, y, oldCharacter, newCharacter):
    """
    采用递归的方式将文本替换
    """
    if mapObj[x][y] == oldCharacter:
        mapObj[x][y] = newCharacter
    # 向右递归
    if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
        floodFill(mapObj, x+1, y, oldCharacter, newCharacter)
    # 向左递归
    if x > 0 and mapObj[x-1][y] == oldCharacter:
        floodFill(mapObj, x-1, y, oldCharacter, newCharacter)
    # 向下递归
    if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
        floodFill(mapObj, x, y+1, oldCharacter, newCharacter)
    # 向上递归
    if y > 0 and mapObj[x][y-1] == oldCharacter:
        floodFill(mapObj, x, y-1, oldCharacter, newCharacter)


# 绘制地图
def drawMap(mapObj, gameStateObj, goals):
    # 整个地图宽度
    mapSurfWidth = len(mapObj) * TILEWIDTH
    # 整个地图高度
    mapSurfHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT

    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)
    # 开始遍历绘制地图元素
    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            spaceRect = pygame.Rect((y * TILEWIDTH, x * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if mapObj[x][y] in TILEMAPPING:
                baseTile = TILEMAPPING[mapObj[x][y]]
            elif mapObj[x][y] in OUTSIDEDECOMAPPING:
                baseTile = TILEMAPPING[' ']

            # 绘制地图
            mapSurf.blit(baseTile, spaceRect)

            if mapObj[x][y] in OUTSIDEDECOMAPPING:
                # 绘制装饰物
                mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)
            elif (x, y) in gameStateObj['stars']:
                if (x, y) in goals:
                    # 绘制箱子到达终点后的图片
                    mapSurf.blit(IMAGESDICT['covered goal'], spaceRect)
                # 绘制箱子
                mapSurf.blit(IMAGESDICT['star'], spaceRect)
            elif (x, y) in goals:
                # 绘制图片
                mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect)

            # 绘制人物
            if (x, y) == gameStateObj['player']:
                mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)
    return mapSurf


# 判断关卡是否结束
def isLevelFinished(levelObj, gameStateObj):
    for goal in levelObj['goals']:
        # 获取游戏状态字典中箱子的位置是否均与终点的坐标重合
        if goal not in gameStateObj['stars']:
            return False
    return True


# 退出游戏
def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

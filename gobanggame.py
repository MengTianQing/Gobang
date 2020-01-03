import pygame
import time
import computer
from button import Button

img_chess_white = pygame.image.load('imgs/white.gif')
img_chess_black = pygame.image.load('imgs/black.gif')
img_btn_restart = ''

SCREEN_WIDTH=900
SCREEN_HEIGHT=800
BG_COLOR=pygame.Color(200, 200, 200)
Line_COLOR=pygame.Color(255, 255, 200)
TEXT_COLOR=pygame.Color(255, 0, 0)
# 定义颜色
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)


class MainGame():
    window = None
    Start_X = 50
    Start_Y = 50
    Line_Span = 40
    Max_X = Start_X + 18 * Line_Span
    Max_Y = Start_Y + 18 * Line_Span

    player1Color = 'B'
    player2Color = 'W'
    overColor = 'S'

    # 1代表玩家1 ， 2代表到玩家2  0代表结束
    Putdownflag = player1Color

    ChessmanList = []
    button_go =None

    def __init__(self):
        '''初始化'''

    def startGame(self):
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("五子棋")
        MainGame.button_go = Button(MainGame.window, "重新开始", SCREEN_WIDTH - 100, 300)  # 创建开始按钮

        #初始化
        while True:
            time.sleep(0.1)
            #获取事件
            MainGame.window.fill(BG_COLOR)
            self.drawchChessboard()
            self.bitechessman()

            MainGame.button_go.draw_button()

            self.VictoryOrDefeat()
            self.Computerplay()
            self.getEvent()

            pygame.display.update()
            pygame.display.flip()


    def drawchChessboard(self):

        for i in range(0,19):
            x = MainGame.Start_X + i * MainGame.Line_Span
            y = MainGame.Start_Y + i * MainGame.Line_Span
            pygame.draw.line(MainGame.window, BLACK, [x,  MainGame.Start_Y], [x, MainGame.Max_Y], 1)
            pygame.draw.line(MainGame.window, BLACK, [MainGame.Start_X, y], [MainGame.Max_X, y], 1)


    def getEvent(self):
        # 获取所有的事件
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                if (mouse_x > MainGame.Start_X- MainGame.Line_Span/2 and mouse_x < MainGame.Max_X + MainGame.Line_Span / 2) and (mouse_y > MainGame.Start_Y- MainGame.Line_Span/2 and mouse_y < MainGame.Max_Y + MainGame.Line_Span / 2):
                    #print( str(mouse_x) + "" + str(mouse_y))
                    #print(str(MainGame.Putdownflag))
                    if MainGame.Putdownflag != MainGame.player1Color:
                        return

                    click_x = round((mouse_x - MainGame.Start_X) / MainGame.Line_Span)
                    click_y = round((mouse_y - MainGame.Start_Y) / MainGame.Line_Span)
                    click_mod_x = (mouse_x - MainGame.Start_X) % MainGame.Line_Span
                    click_mod_y = (mouse_y - MainGame.Start_Y) % MainGame.Line_Span
                    if abs(click_mod_x-MainGame.Line_Span/2) >=5 and abs(click_mod_y-MainGame.Line_Span/2) >=5:
                        #print("有效点：x="+str(click_x)+" y="+str(click_y))
                        #有效点击点
                        self.putdownchess(MainGame.player1Color, click_x, click_y)

                else:
                    print("out")
                if MainGame.button_go.is_click():
                    self.restart()
                    print("button_go click")
                else:
                    print("button_go click out")

    def putdownchess(self, t, x, y):
        flag = False
        for item in  MainGame.ChessmanList:
            if item.x == x and item.y == y:
                flag = True
        if not flag:
            cm = Chessman(t, x, y)
            MainGame.ChessmanList.append(cm)
            MainGame.Putdownflag = MainGame.player2Color

        #print("ChessmanListlen:" + str(len(MainGame.ChessmanList)))

    def bitechessman(self):
        for item in MainGame.ChessmanList:
            item.displaychessman()

    def bureautime(self):
            ''''''

    def Computerplay(self):

        if MainGame.Putdownflag == MainGame.player2Color:
            print("轮到电脑了")
            computer = self.getComputerplaychess()
            if computer==None:
                return
            #print("computer x="+str(computer.x) + "  y="+str(computer.y))
            MainGame.ChessmanList.append(computer)
            MainGame.Putdownflag = MainGame.player1Color



    #判断游戏胜利
    def VictoryOrDefeat(self):
        for item in  MainGame.ChessmanList:
            if self.calHorizontalCount(item) == 5 or self.calVerticalityCount(item) == 5 or self.calBevelsUpCount(item) == 5 or self.calBevelsDownCount(item)==5:
                txt =""
                if item.troops == MainGame.player1Color :
                    txt = "玩家"
                else:
                    txt = "电脑"
                MainGame.window.blit(self.getTextSuface("%s获胜" % txt), (SCREEN_WIDTH-100, 200))
                MainGame.Putdownflag = MainGame.overColor

                return
    def restart(self):
        MainGame.ChessmanList = []
        MainGame.Putdownflag = MainGame.player1Color

    def calHorizontalCount(self,chessman):
        count = 1
        for i in range(1, 5):
            fi = filter(lambda x: x.troops == chessman.troops and x.x == chessman.x and x.y == chessman.y + i,
                        MainGame.ChessmanList)
            if len(list(fi)) == 1:
                count += 1
            else:
                break
        return count

    def calVerticalityCount(self, chessman):
        count = 1
        for i in range(1, 5):
            fi = filter(lambda x:x.troops==chessman.troops and x.x == chessman.x+ i and x.y == chessman.y  , MainGame.ChessmanList)
            if len(list(fi)) == 1:
                count += 1
            else:
                break
        return count

    def calBevelsUpCount(self, chessman):
        count = 1
        for i in range(1, 5):
            fi = filter(lambda x: x.troops == chessman.troops and x.x == chessman.x + i and x.y == chessman.y - i,
                        MainGame.ChessmanList)
            if len(list(fi)) == 1:
                count += 1
            else:
                break
        return count

    def calBevelsDownCount(self, chessman):
        count = 1
        for i in range(1, 5):
            fi = filter(lambda x: x.troops == chessman.troops and x.x == chessman.x + i and x.y == chessman.y + i,
                        MainGame.ChessmanList)
            if len(list(fi)) == 1:
                count += 1
            else:
                break
        return count

    def getTextSuface(self, text):
        pygame.font.init()
        # print(pygame.font.get_fonts())
        font = pygame.font.SysFont('kaiti', 18)
        txt = font.render(text, True, TEXT_COLOR)
        return txt
    def endGame(self):
        print("exit")
        exit()


    def getComputerplaychess(self):
        if len(MainGame.ChessmanList) == 0:
            return Chessman(MainGame.player2Color, 9, 9)

        arr = [[0 for i in range(19)] for j in range(19)]

        for i in range(0, 19):
            for j in range(0, 19):
                if len(list(filter(lambda cm: cm.x == i and cm.y == j and cm.troops==MainGame.player1Color , MainGame.ChessmanList))):
                    arr[i][j] = 1
                elif len(list(filter(lambda x: x.x == i and x.y == j and x.troops==MainGame.player2Color, MainGame.ChessmanList))):
                    arr[i][j] = 2
        '''
        newarr = computer.getPoint(arr)
        if newarr.x != -1 and newarr.y != -1:
            print("结果："+ str(newarr.x) +"  "+ str(newarr.y))
            return Chessman(MainGame.player2Color, newarr.x, newarr.y)
        '''
        newarr = computer.getPoint(arr)
        if newarr[0] != -1 and newarr[1] != -1:
            print("结果：" + str(newarr[0]) + "  " + str(newarr[1]))
            return Chessman(MainGame.player2Color, newarr[0], newarr[1])

        # 进攻

        # 防守
        for item in MainGame.ChessmanList:
            if item.troops == MainGame.player1Color:
                prev_x = item.x - 1
                prev_y = item.y - 1
                next_x = item.x + 1
                next_y = item.y + 1

                if next_x < 19 and len(list(filter(lambda x: x.x == next_x and x.y == item.y,  MainGame.ChessmanList)))==0:
                    return Chessman(MainGame.player2Color, next_x, item.y)
                if next_y < 19 and len(list(filter(lambda x: x.x == item.x and x.y == next_y,  MainGame.ChessmanList)))==0:
                    return Chessman(MainGame.player2Color, item.x, next_y)


        for i in range(0,18):
            for j in range(0, 18):
                fi= filter(lambda x: x.x == i and x.y == j,  MainGame.ChessmanList)
                if len(list(fi)) == 0 :
                    return  Chessman(MainGame.player2Color, i, j)


        return None



class   Chessman():
    def __init__(self,t,x,y):
        self.images = {
            'B' : img_chess_black,
            'W' : img_chess_white,
        }
        self.troops = t
        self.image = self.images[self.troops]
        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.left = MainGame.Start_X + x * MainGame.Line_Span - MainGame.Line_Span/2
        self.rect.top =  MainGame.Start_Y + y * MainGame.Line_Span - MainGame.Line_Span/2

    def displaychessman(self):
        if self.troops != 'N':
            self.image = self.images[self.troops]
            MainGame.window.blit(self.image,self.rect)


if __name__ == '__main__':
    MainGame().startGame()


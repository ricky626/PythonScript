import urllib.request
import xml.etree.ElementTree as etree

import pygame
from pygame.locals import *
from my_data import GetData


#### DEFINE ####

WHITE = (255, 255, 255) # 하얀색 정의
BLUE = (0, 0, 255) # 파란색 정의
BLACK = (0, 0, 0)
MOUSE_LEFT = 1  # 마우스 왼쪽 버튼에 대한 버튼 인덱스
MOUSE_WHEEL_CLICK = 2  # 마우스 휠 클릭에 대한 버튼 인덱스
MOUSE_RIGHT = 3  # 마우스 오른쪽 버튼에 대한 버튼 인덱스
MOUSE_WHEEL_UP = 4  # 마우스 휠을 위로 올렸을 때에 대한 버튼 인덱스
MOUSE_WHEEL_DOWN = 5  # 마우스 휠을 아래로 내렸을 때에 대한 버튼 인덱스

#### DEFINE ####


my_data = GetData()
pygame.mixer.init()

class Data:
    home = None
    button = [None for i in range(0, 5)]

    SERVICE_AREA_NAME, ROUTE_NAME, DIRECTION, BATCH_MENU, SALE_PRICE, MY_MENU = range(0, 6)


    def __init__(self):
        my_data.save()

        self.tree = etree.parse("res/xml/data.xml")
        self.root = self.tree.getroot()

        # for i in self.root.iter("list"):
        #     print(i.findtext("batchMenu"))

        self.buttonX = [0 for i in range(0, 5)]
        self.buttonY = [0 for i in range(0, 5)]

        if(Data.home == None):
            Data.home = pygame.image.load("res/gfx/home.png")
            self.board = pygame.image.load("res/gfx/board.png")
            self.loginboard = pygame.image.load("res/gfx/loginboard.png")
            self.login = pygame.image.load("res/gfx/login.png")
            self.memberboard = pygame.image.load("res/gfx/memberboard.png")

            for i in range(0, 5):
                self.button[i] = pygame.image.load("res/gfx/button.png")
                self.buttonX[i] = 312
                self.buttonY[i] = (i * 120) + 140


            self.font30 = pygame.font.Font("res/font/HoonWhitecatR.ttf", 30)
            self.font50 = pygame.font.Font("res/font/HoonWhitecatR.ttf", 50)
            self.font80 = pygame.font.Font("res/font/HoonWhitecatR.ttf", 80)

            self.mainsound = pygame.mixer.Sound("res/mfx/main.wav")
            self.clicksound = pygame.mixer.Sound("res/mfx/click.wav")
            self.clearsound = pygame.mixer.Sound("res/mfx/clear.wav")
            self.failsound = pygame.mixer.Sound("res/mfx/fail.wav")

        self.mainsound.play(-1)

        self.batchMenu = [] # 대표 메뉴 이름
        self.direction = [] # 방향
        self.routeName = [] # ㅇㅇ고속도로
        self.salePrice = [] # 대표 메뉴 가격
        self.serviceAreaName = [] #휴게소이름

        self.count = -1
        self.listlen = -1

        self.state = -1
        self.serstate = -1

        self.scrollmax = 0

        self.page = 0
        self.maxpage = 0

        self.serpage = 0
        self.maxserpage = 0
        self.serscrollmax = 0

        self.mcount = -1
        self.m_list = []
        self.m_listlen = 0
        self.maxlistpage = 0
        self.listpage = 0

        self.idscanf = str()
        self.idcheck = False

        self.pwscanf = str()
        self.pwcheck = False

        self.DownKeyCheck = False
        self.UpKeyCheck =  False
        self.MenuKeyCheck = -100
        self.loginCheck = False
        self.memberlogincheck = False
        self.memberboardcheck = False

        self.memnamecheck = False
        self.memnamescanf = str()

        self.memidcheck = False
        self.memidscanf = str()

        self.mempwcheck = False
        self.mempwscanf= str()

        self.memdircheck = False
        self.memdirscanf = str()

        self.memphonecheck = False
        self.memphonescanf = str()

        self.loginindex = -1
        self.loginok = 0


        for a in self.root.iter("list"):
            if(a.findtext("batchMenu") == None):
                self.batchMenu.append(" ")
            else:
                self.batchMenu.append(a.findtext("batchMenu"))

            if(a.findtext("direction") == None):
                self.direction.append(" ")
            else:
                self.direction.append(a.findtext("direction"))

            if(a.findtext("routeName") == None):
                self.routeName.append(" ")
            else:
                self.routeName.append(a.findtext("routeName"))

            if(a.findtext("salePrice") == None):
                self.salePrice.append(" ")
            else:
                self.salePrice.append(a.findtext("salePrice"))

            if(a.findtext("serviceAreaName") == None):
                self.serviceAreaName.append(" ")
            else:
                self.serviceAreaName.append(a.findtext("serviceAreaName"))

        self.sbatchMenu = []
        self.sdirection = []
        self.srouteName = []
        self.ssalePrice = []
        self.sserviceAreaName = []

        self.ibatchMenu = []
        self.idirection = []
        self.irouteName = []
        self.isalePrice = []
        self.iserviceAreaName = []



        self.sbatchMenu.extend(self.batchMenu)
        self.sdirection.extend(self.direction)
        self.srouteName.extend(self.routeName)
        self.ssalePrice.extend(self.salePrice)


        self.sserviceAreaName.extend(self.serviceAreaName)


        self.batchMenu = list(set(self.batchMenu))
        self.direction = list(set(self.direction))
        self.routeName = list(set(self.routeName))
        self.salePrice = list(set(self.salePrice))
        self.serviceAreaName = list(set(self.serviceAreaName))


        self.batchMenu.sort()
        self.direction.sort()
        self.routeName.sort()
        self.salePrice.sort()
        self.serviceAreaName.sort()

        self.salePrice.pop(0)


        # print(len(self.serviceAreaName))
        # print(len(self.routeName))
        # print(len(self.direction))
        # print(len(self.batchMenu))
        # print(len(self.salePrice))

        self.memberID = []
        self.memberPW = []
        self.memberNAME = []
        self.memberINDEX = []


        self.fileloading()


        pass

    def filewrite(self, list, filename):
        f = open(filename, 'w')
        f.write(" ".join(list))
        f.close()

    def fileread(self, filename):
        f = open(filename, 'r')
        return f.read().split()

    def filesetting(self):
        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
        self.filewrite(self.memberNAME, "res/memberDB/memberNAME.datab")
        self.filewrite(self.memberINDEX, "res/memberDB/memberINDEX.datab")

    def fileloading(self):
        self.memberID = self.fileread("res/memberDB/memberID.datab")
        self.memberPW = self.fileread("res/memberDB/memberPW.datab")
        self.memberNAME = self.fileread("res/memberDB/memberNAME.datab")
        self.memberINDEX = self.fileread("res/memberDB/memberINDEX.datab")



    def collide(self, aX, aY, bX, bY, bsizeX, bsizeY):
        left_a, top_a, right_a, bottom_a = aX, aY, aX, aY
        left_b, top_b, right_b, bottom_b = bX, bY, bX + bsizeX, bY + bsizeY

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a > bottom_b: return False
        if bottom_a < top_b: return False
        return True



    def update(self):

        pass

    def print_all(self, SCREEN, numlist):

        if(self.serpage == 0):
            SCREEN.blit(self.font30.render("===============", True, BLACK), (120, 184))

        for i in numlist:

            if(214 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 214 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                if(self.sserviceAreaName[i] != " "):
                    SCREEN.blit(self.font30.render(self.sserviceAreaName[i] + "휴게소", True, BLACK), (120, 214 + (numlist.index(i) * 180) - (self.serpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("휴게소 정보 없음", True, BLACK), (120, 214 + (numlist.index(i) * 180) - (self.serpage * 30)))

            if(244 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 244 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                if(self.srouteName[i] != " "):
                    SCREEN.blit(self.font30.render(self.srouteName[i], True, BLACK), (120, 244 + (numlist.index(i) * 180) - (self.serpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("지역 정보 없음", True, BLACK), (120, 244 + (numlist.index(i) * 180) - (self.serpage * 30)))

            if(274 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 274 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                if(self.sdirection[i] != " "):
                    SCREEN.blit(self.font30.render(self.sdirection[i], True, BLACK), (120, 274 + (numlist.index(i) * 180) - (self.serpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("고속도로방향 정보 없음", True, BLACK), (120, 274 + (numlist.index(i) * 180) - (self.serpage * 30)))

            if(304 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 304 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                if(self.sbatchMenu[i] != " "):
                    SCREEN.blit(self.font30.render(self.sbatchMenu[i], True, BLACK), (120, 304 + (numlist.index(i) * 180) - (self.serpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("대표메뉴 정보 없음", True, BLACK), (120, 304 + (numlist.index(i) * 180) - (self.serpage * 30)))

            if(334 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 334 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                if(self.ssalePrice[i] != " "):
                    SCREEN.blit(self.font30.render(self.ssalePrice[i].lstrip("￦") + "원", True, BLACK), (120, 334 + (numlist.index(i) * 180) - (self.serpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("가격 정보 없음", True, BLACK), (120, 334 + (numlist.index(i) * 180) - (self.serpage * 30)))

            if(364 + (numlist.index(i) * 180) - (self.serpage * 30) > 185 and 364 + (numlist.index(i) * 180) - (self.serpage * 30) < 695):
                SCREEN.blit(self.font30.render("===============", True, BLACK), (120, 364 + (numlist.index(i) * 180) - (self.serpage * 30)))
                
    def print_mymenu(self, SCREEN, numlist):

        if(self.listpage == 0):
            SCREEN.blit(self.font30.render("===============", True, BLACK), (120, 184))

        for i in numlist:

            if(214 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 214 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                if(self.sserviceAreaName[i] != " "):
                    SCREEN.blit(self.font30.render(self.sserviceAreaName[i] + "휴게소", True, BLACK), (120, 214 + (numlist.index(i) * 180) - (self.listpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("휴게소 정보 없음", True, BLACK), (120, 214 + (numlist.index(i) * 180) - (self.listpage * 30)))

            if(244 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 244 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                if(self.srouteName[i] != " "):
                    SCREEN.blit(self.font30.render(self.srouteName[i], True, BLACK), (120, 244 + (numlist.index(i) * 180) - (self.listpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("지역 정보 없음", True, BLACK), (120, 244 + (numlist.index(i) * 180) - (self.listpage * 30)))

            if(274 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 274 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                if(self.sdirection[i] != " "):
                    SCREEN.blit(self.font30.render(self.sdirection[i], True, BLACK), (120, 274 + (numlist.index(i) * 180) - (self.listpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("고속도로방향 정보 없음", True, BLACK), (120, 274 + (numlist.index(i) * 180) - (self.listpage * 30)))

            if(304 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 304 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                if(self.sbatchMenu[i] != " "):
                    SCREEN.blit(self.font30.render(self.sbatchMenu[i], True, BLACK), (120, 304 + (numlist.index(i) * 180) - (self.listpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("대표메뉴 정보 없음", True, BLACK), (120, 304 + (numlist.index(i) * 180) - (self.listpage * 30)))

            if(334 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 334 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                if(self.ssalePrice[i] != " "):
                    SCREEN.blit(self.font30.render(self.ssalePrice[i].lstrip("￦") + "원", True, BLACK), (120, 334 + (numlist.index(i) * 180) - (self.listpage * 30)))
                else:
                    SCREEN.blit(self.font30.render("가격 정보 없음", True, BLACK), (120, 334 + (numlist.index(i) * 180) - (self.listpage * 30)))

            if(364 + (numlist.index(i) * 180) - (self.listpage * 30) > 185 and 364 + (numlist.index(i) * 180) - (self.listpage * 30) < 695):
                SCREEN.blit(self.font30.render("===============", True, BLACK), (120, 364 + (numlist.index(i) * 180) - (self.listpage * 30)))


    def draw(self, SCREEN):
        if(self.memberlogincheck == True):
            SCREEN.blit(self.font30.render(self.memberNAME[self.loginindex] + "님 환영합니다.", True, BLACK), (10, 20))

            if(self.state == -1):
                pygame.draw.polygon(SCREEN, (80, 80, 255), ((10, 80), (210, 80), (210, 130), (10, 130))) # 10, 80, 210, 130
                SCREEN.blit(self.font50.render("나만의 기능", True, BLACK), (29, 82))
                #pygame.draw.polygon(SCREEN, (255, 80, 80), ((10, 80), (210, 80), (210, 130), (10, 130))) # 10, 80, 210, 130
                pygame.draw.polygon(SCREEN, (255, 80, 80), ((200, 10), (275, 10), (275, 70), (200, 70))) # 200, 10 75, 60
                SCREEN.blit(self.font30.render("로그아웃", True, BLACK), (205, 25))

        else:
            SCREEN.blit(self.font30.render("로그인 되어있지 않음", True, (255, 0, 0)), (10, 20))


        SCREEN.blit(self.home, (8, 680))
        SCREEN.blit(self.font80.render("휴게소 맛집 Finder", True, BLACK), (300, 20))

        if(self.state == -1 and self.memberlogincheck == False):
            SCREEN.blit(self.login, (935, 9))

        if(self.state == -1):
            for i in range(0, 5):
                SCREEN.blit(self.button[i], (self.buttonX[i], self.buttonY[i]))

            SCREEN.blit(self.font50.render("휴게소 검색", True, BLACK), (self.buttonX[0] + 110, self.buttonY[0] + 15))  # 설정한 위치에 텍스트 객체를 출력
            SCREEN.blit(self.font50.render("지역별 검색", True, BLACK), (self.buttonX[1] + 110, self.buttonY[1] + 15))
            SCREEN.blit(self.font50.render("방향별 검색", True, BLACK), (self.buttonX[2] + 110, self.buttonY[2] + 15))
            SCREEN.blit(self.font50.render("대표메뉴 검색", True, BLACK), (self.buttonX[3] + 100, self.buttonY[3] + 15))
            SCREEN.blit(self.font50.render("가격별 검색", True, BLACK), (self.buttonX[4] + 110, self.buttonY[4] + 15))

            if(self.loginCheck == True and self.memberboardcheck == False):
                SCREEN.blit(self.loginboard, (240, 220))

                if(self.idcheck == True):
                    pygame.draw.line(SCREEN, BLACK, [417, 342], [734, 342], 5)
                    pygame.draw.line(SCREEN, BLACK, [734, 342], [734, 395], 5)
                    pygame.draw.line(SCREEN, BLACK, [734, 395], [417, 395], 5)
                    pygame.draw.line(SCREEN, BLACK, [417, 395], [417, 342], 5)
                elif(self.pwcheck == True):
                    pygame.draw.line(SCREEN, BLACK, [415, 402], [732, 402], 5)
                    pygame.draw.line(SCREEN, BLACK, [732, 402], [732, 455], 5)
                    pygame.draw.line(SCREEN, BLACK, [732, 455], [415, 455], 5)
                    pygame.draw.line(SCREEN, BLACK, [415, 455], [415, 402], 5)

                SCREEN.blit(self.font30.render(self.idscanf, True, BLACK), (422, 350))

                for i in range(0, len(self.pwscanf)):
                    SCREEN.blit(self.font30.render("*", True, BLACK), (422 + (i * 15), 412))

                if(self.loginok == -1):
                    SCREEN.blit(self.font30.render("입력하신 정보가 맞지 않습니다.", True, (255, 0, 0)), (452, 466))
                pass
                #pygame.draw.polygon(SCREEN, (128, 100, 200), ((425, 500), (625, 500), (625, 600), (425, 600))) # 425, 500, 625, 600
                #pygame.draw.polygon(SCREEN, (128, 100, 200), ((425, 500), (625, 500), (625, 600), (425, 600))) # 425, 500, 625, 600

            if(self.memberboardcheck == True):
                SCREEN.blit(self.memberboard, (212, 110))
                pygame.draw.polygon(SCREEN, WHITE, ((369, 257), (647, 257), (647, 302), (369, 302))) # NAME
                pygame.draw.polygon(SCREEN, WHITE, ((369, 310), (647, 310), (647, 355), (369, 355))) # ID
                pygame.draw.polygon(SCREEN, WHITE, ((369, 363), (647, 363), (647, 408), (369, 408))) # PW
                pygame.draw.polygon(SCREEN, WHITE, ((369, 416), (647, 416), (647, 461), (369, 461))) # DIR
                pygame.draw.polygon(SCREEN, WHITE, ((369, 469), (647, 469), (647, 514), (369, 514))) # PHONE

                SCREEN.blit(self.font30.render(self.memnamescanf, True, BLACK), (374, 260))
                SCREEN.blit(self.font30.render(self.memidscanf, True, BLACK), (374, 313))

                for i in range(0, len(self.mempwscanf)):
                    SCREEN.blit(self.font30.render("*", True, BLACK), (374 + (i * 15), 368))

                SCREEN.blit(self.font30.render(self.memdirscanf, True, BLACK), (374, 421))
                SCREEN.blit(self.font30.render(self.memphonescanf, True, BLACK), (374, 474))

                if(self.memnamecheck == True):
                    pygame.draw.line(SCREEN, BLACK, [369, 257], [647, 257], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 257], [647, 302], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 302], [369, 302], 5)
                    pygame.draw.line(SCREEN, BLACK, [369, 302], [369, 257], 5)

                elif(self.memidcheck == True):
                    pygame.draw.line(SCREEN, BLACK, [369, 310], [647, 310], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 310], [647, 355], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 355], [369, 355], 5)
                    pygame.draw.line(SCREEN, BLACK, [369, 355], [369, 310], 5)

                elif(self.mempwcheck == True):
                    pygame.draw.line(SCREEN, BLACK, [369, 363], [647, 363], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 363], [647, 408], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 408], [369, 408], 5)
                    pygame.draw.line(SCREEN, BLACK, [369, 408], [369, 363], 5)

                elif(self.memdircheck == True):
                    pygame.draw.line(SCREEN, BLACK, [369, 416], [647, 416], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 416], [647, 461], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 461], [369, 461], 5)
                    pygame.draw.line(SCREEN, BLACK, [369, 461], [369, 416], 5)

                elif(self.memphonecheck == True):
                    pygame.draw.line(SCREEN, BLACK, [369, 469], [647, 469], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 469], [647, 514], 5)
                    pygame.draw.line(SCREEN, BLACK, [647, 514], [369, 514], 5)
                    pygame.draw.line(SCREEN, BLACK, [369, 514], [369, 469], 5)



        else:
            SCREEN.blit(self.board, (112, 134))

            if(self.state == self.MY_MENU): # 회원의 나만의 기능
                SCREEN.blit(self.font50.render("== " + self.memberNAME[self.loginindex] + "님의 위치에서 가장 가까운 맛집입니다. ==", True, BLACK), (139, 138))  # 설정한 위치에 텍스트 객체를 출력
                self.print_mymenu(SCREEN, self.m_list)


                # SCREEN.blit(self.font50.render(self.sserviceAreaName[int(self.memberINDEX[self.loginindex])] + "휴게소", True, BLACK), (120, 254))
                # SCREEN.blit(self.font50.render(self.srouteName[int(self.memberINDEX[self.loginindex])], True, BLACK), (120, 304))
                # SCREEN.blit(self.font50.render(self.sdirection[int(self.memberINDEX[self.loginindex])], True, BLACK), (120, 354))
                # SCREEN.blit(self.font50.render(self.sbatchMenu[int(self.memberINDEX[self.loginindex])], True, BLACK), (120, 404))
                # SCREEN.blit(self.font50.render(self.ssalePrice[int(self.memberINDEX[self.loginindex])].lstrip("￦") + "원", True, BLACK), (120, 454))

            if(self.serstate == -1):
                if(self.state == self.SERVICE_AREA_NAME):
                    for i in range(self.page, self.page + self.maxpage):
                        SCREEN.blit(self.font30.render(self.serviceAreaName[i] + "휴게소", True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                    if(self.MenuKeyCheck != -100):
                        SCREEN.blit(self.font30.render(self.serviceAreaName[self.MenuKeyCheck] + "휴게소", True, BLUE), (550, 385))
                    pass

                if(self.state == self.ROUTE_NAME):
                    for i in range(self.page, self.page + self.maxpage):
                        SCREEN.blit(self.font30.render(self.routeName[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                    if(self.MenuKeyCheck != -100):
                        SCREEN.blit(self.font30.render(self.routeName[self.MenuKeyCheck], True, BLUE), (550, 385))
                    pass

                if(self.state == self.DIRECTION):
                    for i in range(self.page, self.page + self.maxpage):
                        SCREEN.blit(self.font30.render(self.direction[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))

                    if(self.MenuKeyCheck != -100):
                        SCREEN.blit(self.font30.render(self.direction[self.MenuKeyCheck], True, BLUE), (650, 385))
                    pass

                if(self.state == self.BATCH_MENU):
                    for i in range(self.page, self.page + self.maxpage):
                        SCREEN.blit(self.font30.render(self.batchMenu[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))

                    if(self.MenuKeyCheck != -100):
                        SCREEN.blit(self.font30.render(self.batchMenu[self.MenuKeyCheck], True, BLUE), (550, 385))

                    pass

                if(self.state == self.SALE_PRICE):
                    for i in range(self.page, self.page + self.maxpage):
                        SCREEN.blit(self.font30.render(self.salePrice[i].lstrip("￦") + "원", True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))

                    if(self.MenuKeyCheck != -100):
                        SCREEN.blit(self.font30.render(self.salePrice[self.MenuKeyCheck].lstrip("￦") + "원", True, BLUE), (620, 385))
                    pass

                if(self.MenuKeyCheck != -100):
                    if((self.MenuKeyCheck >= self.page) and (self.MenuKeyCheck - self.page < 20)):
                        pygame.draw.line(SCREEN, BLACK, [115, 134 + (self.MenuKeyCheck * 30) - (self.page * 30)], [400, 134 + (self.MenuKeyCheck * 30) - (self.page * 30)], 5)
                        pygame.draw.line(SCREEN, BLACK, [115, 164 + (self.MenuKeyCheck * 30) - (self.page * 30)], [400, 164 + (self.MenuKeyCheck * 30) - (self.page * 30)], 5)
                        pygame.draw.line(SCREEN, BLACK, [115, 134 + (self.MenuKeyCheck * 30) - (self.page * 30)], [115, 164 + (self.MenuKeyCheck * 30) - (self.page * 30)], 5)
                        pygame.draw.line(SCREEN, BLACK, [400, 134 + (self.MenuKeyCheck * 30) - (self.page * 30)], [400, 164 + (self.MenuKeyCheck * 30) - (self.page * 30)], 5)
                    pygame.draw.polygon(SCREEN, (255, 100, 200), ((775, 350), (875, 350), (875, 450), (775, 450))) # 775, 350, 875, 450


                    SCREEN.blit(self.font50.render("검색", True, BLACK), (790, 375))

                if(self.state != self.MY_MENU):
                    SCREEN.blit(self.font50.render("1. 마우스 휠로 스크롤 하세요.", True, BLACK), (510, 150))
                    SCREEN.blit(self.font50.render("2. 찾으시는 것을 클릭하시고", True, BLACK), (510, 200))
                    SCREEN.blit(self.font50.render("3. 검색 버튼을 눌러주세요.", True, BLACK), (515, 250))

            else:
                if(self.serstate == 1):
                    SCREEN.blit(self.font50.render("== 검색하신 결과 ==", True, BLACK), (350, 134))  # 설정한 위치에 텍스트 객체를 출력
                    SCREEN.blit(self.font50.render("마우스 휠로 스크롤 하세요.", True, BLACK), (550, 200))


                    if(self.state == self.SERVICE_AREA_NAME):
                        self.print_all(SCREEN, self.iserviceAreaName)
                    elif(self.state == self.ROUTE_NAME):
                        self.print_all(SCREEN, self.irouteName)
                    elif(self.state == self.DIRECTION):
                        self.print_all(SCREEN, self.idirection)
                    elif(self.state == self.BATCH_MENU):
                        self.print_all(SCREEN, self.ibatchMenu)
                    elif(self.state == self.SALE_PRICE):
                        self.print_all(SCREEN, self.isalePrice)

            pass


    def handle_events(self, event):

        if(event.type == pygame.KEYDOWN):


            if(self.loginCheck == True):
                if(self.idcheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.idscanf = self.idscanf[:-1]

                    elif(event.key == K_TAB):
                        self.idcheck = False
                        self.pwcheck = True

                    elif(event.key == K_RETURN):
                        for i in range(0, len(self.memberID)):
                            if(self.memberID[i] == self.idscanf and self.memberPW[i] == self.pwscanf): # 로그인
                                self.loginindex = i
                                self.loginCheck = False
                                self.memberlogincheck = True
                                self.idcheck = False
                                self.pwcheck = False
                                self.idscanf = str()
                                self.pwscanf = str()
                                self.loginok = 0
                                self.clearsound.play(0)
                                break
                            elif(i == len(self.memberID)-1):
                                self.loginok = -1
                                self.failsound.play(0)

                    else:
                        self.idscanf += chr(event.key)

                elif(self.pwcheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.pwscanf = self.pwscanf[:-1]

                    elif(event.key == K_TAB):
                        self.pwcheck = False
                        self.idcheck = True

                    elif(event.key == K_RETURN):
                        for i in range(0, len(self.memberID)):
                            if(self.memberID[i] == self.idscanf and self.memberPW[i] == self.pwscanf): # 로그인
                                self.loginindex = i
                                self.loginCheck = False
                                self.memberlogincheck = True
                                self.idcheck = False
                                self.pwcheck = False
                                self.idscanf = str()
                                self.pwscanf = str()
                                self.loginok = 0
                                self.clearsound.play(0)
                                break
                            elif(i == len(self.memberID)-1):
                                self.loginok = -1
                                self.failsound.play(0)


                    else:
                        self.pwscanf += chr(event.key)

            if(self.memberboardcheck == True):

                if(self.memnamecheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.memnamescanf = self.memnamescanf[:-1]
                    elif(event.key == K_TAB):
                        self.memnamecheck = False
                        self.memidcheck = True
                    elif(event.key == K_RETURN): # 회원가입 완료
                        self.clearsound.play(0)
                        self.memberID.append(self.memidscanf)
                        self.memberPW.append(self.mempwscanf)
                        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                        self.memberboardcheck = False
                        self.memnamescanf = str()
                        self.memidscanf = str()
                        self.mempwscanf = str()
                        self.memdirscanf = str()
                        self.memphonescanf = str()

                    else:
                        self.memnamescanf += chr(event.key)



                elif(self.memidcheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.memidscanf = self.memidscanf[:-1]
                    elif(event.key == K_TAB):
                        self.memidcheck = False
                        self.mempwcheck = True
                    elif(event.key == K_RETURN): # 회원가입 완료
                        self.clearsound.play(0)
                        self.memberID.append(self.memidscanf)
                        self.memberPW.append(self.mempwscanf)
                        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                        self.memberboardcheck = False
                        self.memnamescanf = str()
                        self.memidscanf = str()
                        self.mempwscanf = str()
                        self.memdirscanf = str()
                        self.memphonescanf = str()

                    else:
                        self.memidscanf += chr(event.key)

                elif(self.mempwcheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.mempwscanf = self.mempwscanf[:-1]
                    elif(event.key == K_TAB):
                        self.mempwcheck = False
                        self.memdircheck = True
                    elif(event.key == K_RETURN): # 회원가입 완료
                        self.clearsound.play(0)
                        self.memberID.append(self.memidscanf)
                        self.memberPW.append(self.mempwscanf)
                        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                        self.memberboardcheck = False
                        self.memnamescanf = str()
                        self.memidscanf = str()
                        self.mempwscanf = str()
                        self.memdirscanf = str()
                        self.memphonescanf = str()

                    else:
                        self.mempwscanf += chr(event.key)

                elif(self.memdircheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.memdirscanf = self.memdirscanf[:-1]
                    elif(event.key == K_TAB):
                        self.memdircheck = False
                        self.memphonecheck = True
                    elif(event.key == K_RETURN): # 회원가입 완료
                        self.clearsound.play(0)
                        self.memberID.append(self.memidscanf)
                        self.memberPW.append(self.mempwscanf)
                        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                        self.memberboardcheck = False
                        self.memnamescanf = str()
                        self.memidscanf = str()
                        self.mempwscanf = str()
                        self.memdirscanf = str()
                        self.memphonescanf = str()

                    else:
                        self.memdirscanf += chr(event.key)

                elif(self.memphonecheck == True):
                    self.clicksound.play(0)
                    if(event.key == K_BACKSPACE):
                        self.memphonescanf = self.memphonescanf[:-1]
                    elif(event.key == K_TAB):
                        self.memphonecheck = False
                        self.memnamecheck = True
                    elif(event.key == K_RETURN): # 회원가입 완료
                        self.clearsound.play(0)
                        self.memberID.append(self.memidscanf)
                        self.memberPW.append(self.mempwscanf)
                        self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                        self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                        self.memberboardcheck = False
                        self.memnamescanf = str()
                        self.memidscanf = str()
                        self.mempwscanf = str()
                        self.memdirscanf = str()
                        self.memphonescanf = str()

                    else:
                        self.memphonescanf += chr(event.key)


        if(event.type == pygame.MOUSEBUTTONDOWN):
            (mx, my) = pygame.mouse.get_pos()

            if(event.button == MOUSE_LEFT):
                self.clicksound.play(0)
                if(self.state == -1 and self.loginCheck == False and self.memberboardcheck == False):
                    for i in range(0, 5):
                        if(self.collide(mx, my, self.buttonX[i], self.buttonY[i], 400, 80)):
                            self.state = i
                            if(self.state == self.SERVICE_AREA_NAME):
                                self.scrollmax = len(self.serviceAreaName)
                                self.maxpage = 20

                            elif(self.state == self.ROUTE_NAME):
                                self.scrollmax = len(self.routeName)
                                self.maxpage = 19

                            elif(self.state == self.DIRECTION):
                                self.scrollmax = len(self.direction)
                                self.maxpage = 20

                            elif(self.state == self.BATCH_MENU):
                                self.scrollmax = len(self.batchMenu)
                                self.maxpage = 20

                            elif(self.state == self.SALE_PRICE):
                                self.scrollmax = len(self.salePrice)
                                self.maxpage = 15

                            break


                if(self.collide(mx, my, 935, 9, 80, 80) and self.state == -1 and self.memberlogincheck == False): # 우측상단 로그인하기 버튼
                    if(self.loginCheck == False):
                        self.loginCheck = True


                    else:
                        self.loginCheck = False
                        self.idcheck = False
                        self.pwcheck = False
                        self.idscanf = str()
                        self.pwscanf = str()
                        self.loginok = 0
                    self.memberboardcheck = False

                if(self.collide(mx, my, 200, 10, 75, 60) and self.state == -1 and self.memberlogincheck == True):
                    self.failsound.play(0)
                    self.memberlogincheck = False
                    self.loginindex = -1
                    self.m_list.clear()


                    pass

                if(self.loginCheck == True):
                    if(self.collide(mx, my, 417, 341, 314, 50) and self.memberboardcheck == False): # ID
                        if(self.idcheck == False):
                            self.idcheck = True
                            if(self.pwcheck == True):
                                self.pwcheck = False
                        pass

                    elif(self.collide(mx, my, 418, 403, 314, 50) and self.memberboardcheck == False): # PASSWORD
                        if(self.pwcheck == False):
                            self.pwcheck = True
                            if(self.idcheck == True):
                                self.idcheck = False
                        pass

                    elif(self.collide(mx, my, 579, 507, 165, 83) and self.memberboardcheck == False): # 로그인하기

                        for i in range(0, len(self.memberID)):
                            if(self.memberID[i] == self.idscanf and self.memberPW[i] == self.pwscanf): # 로그인
                                self.loginindex = i
                                self.loginCheck = False
                                self.memberlogincheck = True
                                self.idcheck = False
                                self.pwcheck = False
                                self.idscanf = str()
                                self.pwscanf = str()
                                self.loginok = 0
                                self.clearsound.play(0)
                                break

                            elif(i == len(self.memberID)-1):
                                self.loginok = -1
                                self.failsound.play(0)

                    elif(self.collide(mx, my, 276, 511, 157, 80)): # 회원가입창 띄우기
                        if(self.memberboardcheck == False):
                            self.memberboardcheck = True
                            self.loginCheck = False


                        pass
                    else:
                        self.idcheck = False
                        self.pwcheck = False
                        self.idscanf = str()
                        self.pwscanf = str()



                if(self.collide(mx, my, 369, 257, 278, 45) and self.memberboardcheck == True): # 회원 가입창 성명
                    if(self.memnamecheck == False):
                        self.memnamecheck = True
                        self.memidcheck = False
                        self.mempwcheck = False
                        self.memdircheck = False
                        self.memphonecheck = False
                                
                elif(self.collide(mx, my, 369, 310, 278, 45) and self.memberboardcheck == True): # 회원가입창 아이디
                    if(self.memidcheck == False):
                        self.memidcheck = True
                        self.memnamecheck = False
                        self.mempwcheck = False
                        self.memdircheck = False
                        self.memphonecheck = False
                                
                elif(self.collide(mx, my, 369, 363, 278, 45) and self.memberboardcheck == True): # 회원가입창 비번
                    if(self.mempwcheck == False):
                        self.mempwcheck = True
                        self.memnamecheck = False
                        self.memidcheck = False
                        self.memdircheck = False
                        self.memphonecheck = False
                                
                elif(self.collide(mx, my, 369, 416, 278, 45) and self.memberboardcheck == True): # 회원가입창 지역
                    if(self.memdircheck == False):
                        self.memdircheck = True
                        self.memnamecheck = False
                        self.mempwcheck = False
                        self.memidcheck = False
                        self.memphonecheck = False
                                
                elif(self.collide(mx, my, 369, 469, 278, 45) and self.memberboardcheck == True): # 회원가입창 연락처
                    if(self.memphonecheck == False):
                        self.memphonecheck = True
                        self.memnamecheck = False
                        self.mempwcheck = False
                        self.memdircheck = False
                        self.memidcheck = False

                elif(self.collide(mx, my, 384, 562, 232, 91) and self.memberboardcheck == True): # 회원 가입하기 버튼
                    self.clearsound.play(0)
                    self.memberID.append(self.memidscanf)
                    self.memberPW.append(self.mempwscanf)
                    self.filewrite(self.memberID, "res/memberDB/memberID.datab")
                    self.filewrite(self.memberPW, "res/memberDB/memberPW.datab")
                    self.memberboardcheck = False
                    self.memnamescanf = str()
                    self.memidscanf = str()
                    self.mempwscanf = str()
                    self.memdirscanf = str()
                    self.memphonescanf = str()

    
                elif(self.memberboardcheck == True):
                    self.memnamecheck = False
                    self.memidcheck = False
                    self.mempwcheck = False
                    self.memdircheck = False
                    self.memphonecheck = False

                if(self.state == -1 and self.memberlogincheck == True):
                    if(self.collide(mx, my, 10, 80, 200, 50)):
                        self.state = self.MY_MENU


                        self.mcount = self.sdirection.count(self.memberINDEX[self.loginindex])


                        for i in range(0, 185):
                            if(self.mcount == len(self.m_list)):
                                 break

                            if(self.sdirection[i] == self.memberINDEX[self.loginindex]):
                                self.m_list.append(i)


                        self.m_listlen = len(self.m_list)
                        self.maxlistpage = self.m_listlen * 5




                if(self.collide(mx, my, 8, 680, 80, 80)): # home 버튼 + 마우스 충돌 시

                    self.page = 0
                    self.scrollmax = 0
                    self.maxpage = 0
                    self.serstate = -1
                    self.serpage = 0
                    self.maxserpage = 0
                    self.listpage = 0
                    self.maxlistpage = 0
                    self.MenuKeyCheck = -100
                    self.count = -1
                    self.loginCheck = False
                    self.idcheck = False
                    self.pwcheck = False
                    self.idscanf = str()
                    self.pwscanf = str()
                    self.loginok = 0
                    self.memberboardcheck = False

                    if(self.state == self.SERVICE_AREA_NAME):
                        self.iserviceAreaName.clear()
                    elif(self.state == self.ROUTE_NAME):
                        self.irouteName.clear()
                    elif(self.state == self.DIRECTION):
                        self.idirection.clear()
                    elif(self.state == self.BATCH_MENU):
                        self.ibatchMenu.clear()
                    elif(self.state == self.SALE_PRICE):
                        self.isalePrice.clear()

                    self.listlen = -1
                    self.state = -1



            if(self.state != -1):
                if(event.type == pygame.MOUSEBUTTONDOWN):

                    if(self.serstate != 1 and self.state != self.MY_MENU):
                        if(event.button == MOUSE_WHEEL_DOWN):
                            if(self.page < self.scrollmax - 20):
                                self.page += 1
                                #self.MenuKeyCheck -= 1

                        if(event.button == MOUSE_WHEEL_UP):
                            if(self.page > 0):
                                self.page -= 1
                                #self.MenuKeyCheck += 1

                    elif(self.serstate == 1 and self.state != self.MY_MENU):
                        if(event.button == MOUSE_WHEEL_DOWN):
                            if(self.serpage < self.maxserpage):
                                self.serpage += 1
                            pass

                        if(event.button == MOUSE_WHEEL_UP):
                            if(self.serpage > 0):
                                self.serpage -= 1
                            pass

                    elif(self.state == self.MY_MENU):
                        if(event.button == MOUSE_WHEEL_DOWN):
                            if(self.listpage < self.maxlistpage):
                                self.listpage += 1

                            pass

                        if(event.button == MOUSE_WHEEL_UP):
                            if(self.listpage > 0):
                                self.listpage -= 1
                            pass

                    if(event.button == MOUSE_LEFT):
                        for i in range(self.page, self.page + self.maxpage):
                            #print(self.page)
                            #print(self.MenuKeyCheck)

                            # print(self.count)
                            #
                            # for i in self.idirection:
                            #     print(i)


                            if(self.collide(mx, my, 120, 134 + (i * 30) - (self.page * 30), 200, 30)):
                                self.MenuKeyCheck = i


                            elif(self.collide(mx, my, 775, 350, 100, 100) and self.MenuKeyCheck != -100): # 검색
                                self.serstate = 1

                                if(self.state == self.SERVICE_AREA_NAME):
                                    self.count = self.sserviceAreaName.count(self.serviceAreaName[self.MenuKeyCheck])
                                    #self.index = self.sserviceAreaName.index(self.serviceAreaName[self.MenuKeyCheck])

                                    for i in range(0, 185):
                                        if(self.count == len(self.iserviceAreaName)):
                                            break

                                        if(self.sserviceAreaName[i] == self.serviceAreaName[self.MenuKeyCheck]):
                                            self.iserviceAreaName.append(i)

                                    self.listlen = len(self.iserviceAreaName)
                                    self.maxserpage = self.listlen * 5


                                elif(self.state == self.ROUTE_NAME):
                                    self.count = self.srouteName.count(self.routeName[self.MenuKeyCheck])
                                   # self.index = self.srouteName.index(self.routeName[self.MenuKeyCheck])

                                    for i in range(0, 185):
                                        if(self.count == len(self.irouteName)):
                                            break

                                        if(self.srouteName[i] == self.routeName[self.MenuKeyCheck]):
                                            self.irouteName.append(i)

                                    self.listlen = len(self.irouteName)
                                    self.maxserpage = self.listlen * 5


                                elif(self.state == self.DIRECTION):
                                    self.count = self.sdirection.count(self.direction[self.MenuKeyCheck])
                                    #self.index = self.sdirection.index(self.direction[self.MenuKeyCheck])

                                    for i in range(0, 185):
                                        if(self.count == len(self.idirection)):
                                            break

                                        if(self.sdirection[i] == self.direction[self.MenuKeyCheck]):
                                            self.idirection.append(i)

                                    self.listlen = len(self.idirection)
                                    self.maxserpage = self.listlen * 5



                                elif(self.state == self.BATCH_MENU):
                                    self.count = self.sbatchMenu.count(self.batchMenu[self.MenuKeyCheck])
                                    #self.index = self.sbatchMenu.index(self.batchMenu[self.MenuKeyCheck])

                                    for i in range(0, 185):
                                        if(self.count == len(self.ibatchMenu)):
                                            break

                                        if(self.sbatchMenu[i] == self.batchMenu[self.MenuKeyCheck]):
                                            self.ibatchMenu.append(i)

                                    self.listlen = len(self.ibatchMenu)
                                    self.maxserpage = self.listlen * 5


                                elif(self.state == self.SALE_PRICE):
                                    self.count = self.ssalePrice.count(self.salePrice[self.MenuKeyCheck])
                                    #self.index = self.ssalePrice.index(self.salePrice[self.MenuKeyCheck])

                                    for i in range(0, 185):
                                        if(self.count == len(self.isalePrice)):
                                            break

                                        if(self.ssalePrice[i] == self.salePrice[self.MenuKeyCheck]):
                                            self.isalePrice.append(i)

                                    self.listlen = len(self.isalePrice)
                                    self.maxserpage = self.listlen * 5


                                break

                                pass



        pass




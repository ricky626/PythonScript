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


class Data:
    home = None
    button = [None for i in range(0, 5)]

    SERVICE_AREA_NAME, ROUTE_NAME, BATCH_MENU, DIRECTION, SALE_PRICE = range(0, 5)


    def __init__(self):
        my_data.save()

        self.tree = etree.parse("data.xml")
        self.root = self.tree.getroot()

        # for i in self.root.iter("list"):
        #     print(i.findtext("batchMenu"))

        self.buttonX = [0 for i in range(0, 5)]
        self.buttonY = [0 for i in range(0, 5)]

        if(Data.home == None):
            Data.home = pygame.image.load("res/home.png")
            self.board = pygame.image.load("res/board.png")

            for i in range(0, 5):
                self.button[i] = pygame.image.load("res/button.png")
                self.buttonX[i] = 320
                self.buttonY[i] = (i * 120) + 140

            self.loading = pygame.image.load("res/loading.png")

        self.font30 = pygame.font.Font("res/HoonWhitecatR.ttf", 30)
        self.font50 = pygame.font.Font("res/HoonWhitecatR.ttf", 50)
        self.font80 = pygame.font.Font("res/HoonWhitecatR.ttf", 80)

        self.batchMenu = [] # 대표 메뉴 이름
        self.direction = [] # 방향
        self.routeName = [] # ㅇㅇ고속도로
        self.salePrice = [] # 대표 메뉴 가격
        self.serviceAreaName = [] #휴게소이름
        self.nodecount = 185
        self.state = -1
        self.scrollmax = 0
        self.menustate = [-1 for i in range(0, 3)]

        self.page = 0
        self.DownKeyCheck = False
        self.UpKeyCheck =  False

        for a in self.root.iter("list"):
            if(a.findtext("batchMenu") != None):
                self.batchMenu.append(a.findtext("batchMenu"))
            if(a.findtext("direction") != None):
                self.direction.append(a.findtext("direction"))
            if(a.findtext("routeName") != None):
                self.routeName.append(a.findtext("routeName"))
            if(a.findtext("salePrice") != None):
                self.salePrice.append(a.findtext("salePrice"))
            if(a.findtext("serviceAreaName") != None):
                self.serviceAreaName.append(a.findtext("serviceAreaName") + " 휴게소")

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

        print(len(self.serviceAreaName))
        print(len(self.routeName))
        print(len(self.direction))
        print(len(self.batchMenu))
        print(len(self.salePrice))



        pass

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

    def draw(self, SCREEN):

        SCREEN.blit(self.home, (8, 680))
        SCREEN.blit(self.font80.render("휴게소 맛집 Finder", True, BLACK), (300, 20))

        if(self.state == -1):
            for i in range(0, 5):
                SCREEN.blit(self.button[i], (self.buttonX[i], self.buttonY[i]))


            SCREEN.blit(self.font50.render("휴게소 검색", True, BLACK), (self.buttonX[0] + 110, self.buttonY[0] + 15))  # 설정한 위치에 텍스트 객체를 출력
            SCREEN.blit(self.font50.render("지역별 검색", True, BLACK), (self.buttonX[1] + 110, self.buttonY[1] + 15))
            SCREEN.blit(self.font50.render("방향별 검색", True, BLACK), (self.buttonX[2] + 110, self.buttonY[2] + 15))
            SCREEN.blit(self.font50.render("대표메뉴 검색", True, BLACK), (self.buttonX[3] + 100, self.buttonY[3] + 15))
            SCREEN.blit(self.font50.render("가격별 검색", True, BLACK), (self.buttonX[4] + 110, self.buttonY[4] + 15))

        else:
            SCREEN.blit(self.board, (112, 134))

            if(self.state == 0):
                for i in range(self.page, self.page + 20):
                    SCREEN.blit(self.font30.render(self.serviceAreaName[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                pass

            if(self.state == 1):
                for i in range(self.page, self.page + 19):
                    SCREEN.blit(self.font30.render(self.routeName[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                pass

            if(self.state == 2):
                for i in range(self.page, self.page + 20):
                    SCREEN.blit(self.font30.render(self.direction[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                pass

            if(self.state == 3):
                for i in range(self.page, self.page + 20):
                    SCREEN.blit(self.font30.render(self.batchMenu[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                pass

            if(self.state == 4):
                for i in range(self.page, self.page + 16):
                    SCREEN.blit(self.font30.render(self.salePrice[i], True, BLACK), (120, 134 + (i * 30) - (self.page * 30)))
                pass


            pass


    def handle_events(self, event):

        if(event.type == pygame.MOUSEBUTTONDOWN):
            (mx, my) = pygame.mouse.get_pos()

            if(event.button == MOUSE_LEFT):

                for i in range(0, 5):
                    if(self.collide(mx, my, self.buttonX[i], self.buttonY[i], 400, 80) and self.state == -1):
                        self.state = i
                        if(self.state == self.SERVICE_AREA_NAME):
                            self.scrollmax = len(self.serviceAreaName)
                        elif(self.state == self.ROUTE_NAME):
                            self.scrollmax = len(self.routeName)
                        elif(self.state == self.DIRECTION):
                            self.scrollmax = len(self.direction)
                        elif(self.state == self.BATCH_MENU):
                            self.scrollmax = len(self.batchMenu)
                        elif(self.state == self.SALE_PRICE):
                            self.scrollmax = len(self.salePrice)

                        break
                if(self.collide(mx, my, 8, 680, 80, 80) and self.state != -1): # home 버튼 + 마우스 충돌 시
                        self.state = -1
                        self.page = 0
                        self.scrollmax = 0


            if(self.state != -1):
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if(event.button == MOUSE_WHEEL_DOWN):
                        if(self.page < self.scrollmax - 20):
                            self.page += 1
                    if(event.button == MOUSE_WHEEL_UP):
                        if(self.page > 0):
                            self.page -= 1

        pass




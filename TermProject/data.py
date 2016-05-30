from sdl2.events import SDL_KEYDOWN

import my_framework

from my_engine import *
from my_data import GetData

import urllib.request
import xml.etree.ElementTree as etree


name = "Data"
my_data = GetData()

class Data:
    home = None
    button = [None for i in range(0, 5)]


    def __init__(self):
        my_data.save()

        self.tree = etree.parse("data.xml")
        self.root = self.tree.getroot()


        for i in self.root.iter("list"):
            print(i.findtext("batchMenu"))

        self.buttonX = [0 for i in range(0, 5)]
        self.buttonY = [0 for i in range(0, 5)]


        if(Data.home == None):
            Data.home = load_image("res/home.png")
            self.board = load_image("res/board.png")

            for i in range(0, 5):
                self.button[i] = load_image("res/button.png")
                self.buttonX[i] = 320
                self.buttonY[i] = (i * 120) + 140


        self.font20 = load_font("res/malgun.ttf", 20)
        self.font50 = load_font("res/HoonWhitecatR.ttf", 50)
        self.font80 = load_font("res/HoonWhitecatR.ttf", 80)



        self.batchMenu = [] # 대표 메뉴 이름
        self.direction = [] # 방향
        self.routeName = [] # ㅇㅇ고속도로
        self.salePrice = [] # 대표 메뉴 가격
        self.serviceAreaName = [] #휴게소이름
        self.nodecount = 185
        self.state = -1
        self.page = 0
        self.DownKeyCheck = False
        self.UpKeyCheck =  False

        for a in self.root.iter("list"):
            self.batchMenu.append(a.findtext("batchMenu"))
            self.direction.append(a.findtext("direction"))
            self.routeName.append(a.findtext("routeName"))

            self.salePrice.append(a.findtext("salePrice"))

            self.serviceAreaName.append(a.findtext("serviceAreaName") + " 휴게소")






    def collide(self, aX, aY, bX, bY):
        left_a, top_a, right_a, bottom_a = aX, aY, aX, aY
        left_b, top_b, right_b, bottom_b = bX, bY, bX + 400, bY + 80

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a > bottom_b: return False
        if bottom_a < top_b: return False
        return True


        pass

    def update(self):
        if(self.DownKeyCheck):
            if(self.page < 185 - 30):
                self.page += 1

        if(self.UpKeyCheck):
            if(self.page > 0):
                self.page -= 1

        pass

    def draw(self):

        self.home.draw(8, 680)
        self.font80.draw_unicode(50, 20, "휴게소 맛집 Finder")



        if(self.state == -1):
            for i in range(0, 5):
                self.button[i].draw(self.buttonX[i], self.buttonY[i])

            self.font50.draw(self.buttonX[0] - 140, self.buttonY[0] + 15, "Area Name Finder")
            self.font50.draw(self.buttonX[1] - 160, self.buttonY[1] + 15, "Route Name Finder")
            self.font50.draw(self.buttonX[2] - 110, self.buttonY[2] + 15, "Direction Finder")
            self.font50.draw(self.buttonX[3] - 150, self.buttonY[3] + 15, "Batch Menu Finder")
            self.font50.draw(self.buttonX[4] - 120, self.buttonY[4] + 15, "Sale Price Finder")
        else:
            self.board.draw(112, 134)
            if(self.state == 0):
                for i in range(self.page, self.page + 30):
                   self.font20.draw_unicode(112, 134 + (i * 20) - (self.page * 20), str(self.serviceAreaName[i]))
                pass

            elif(self.state == 1):
                for i in range(self.page, self.page + 30):
                   self.font20.draw_unicode(112, 134 + (i * 20) - (self.page * 20), str(self.routeName[i]))
                pass

            elif(self.state == 2):
                for i in range(self.page, self.page + 30):
                   self.font20.draw_unicode(112, 134 + (i * 20) - (self.page * 20), str(self.direction[i]))
                pass

            elif(self.state == 3):
                for i in range(self.page, self.page + 30):
                   self.font20.draw_unicode(112, 134 + (i * 20) - (self.page * 20), str(self.batchMenu[i]))

            elif(self.state == 4):
                for i in range(self.page, self.page + 30):
                   self.font20.draw_unicode(112, 134 + (i * 20) - (self.page * 20), str(self.salePrice[i]))
                pass


        pass

    def handle_events(self, event):
        global mx, my
        if(event.type == SDL_MOUSEBUTTONDOWN):
            mx, my = event.x, event.y

            if(event.button == SDL_BUTTON_LEFT):
                for i in range(0, 5):
                    if(self.collide(mx, my, self.buttonX[i], self.buttonY[i]) and self.state == -1):
                        self.state = i
                        break
                if(self.collide(mx, my, 8, 680)): # home 버튼 + 마우스 충돌 시
                    if(self.state != -1):
                        self.state = -1
                        self.page = 0


        if(self.state != -1):
            if(event.type == SDL_KEYDOWN):
                if(event.key == SDLK_DOWN):
                    self.DownKeyCheck = True
                if(event.key == SDLK_UP):
                    self.UpKeyCheck = True

            if(event.type == SDL_KEYUP):
                self.DownKeyCheck = False
                self.UpKeyCheck = False


        pass






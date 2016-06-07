import pygame
from pygame.locals import *
import time # time 모듈을 import
import random


name                                = "Background"


class Background:
    #Polygon                         = [[None for j in range(0, 5)] for i in range(0, 5)]

    def __init__(self):

        self.screenSizeX            = 1024
        self.screenSizeY            = 768
        # self.rect                   = "res/rect/rect-.png"
        # self.tr                     = "res/tr/tr-.png"
        # self.cir                    = "res/cir/cir-.png"
        # self.fa                     = "res/fa/fa-.png"
        # self.yut                    = "res/yut/yut-.png"

        self.moveTime               = pygame.time.get_ticks()
        self.PolygonDegree          = 0
        self.PolygonX               = [[0.0 for j in range(0, 5)] for i in range(0, 5)]
        self.PolygonY               = [[0.0 for j in range(0, 5)] for i in range(0, 5)]
        self.moveX                  = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.moveY                  = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.colorR                  = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.colorG                  = [[0 for j in range(0, 5)] for i in range(0, 5)]
        self.colorB                  = [[0 for j in range(0, 5)] for i in range(0, 5)]


        for i in range(0, 5):
            for j in range(0, 5):
                #self.PolygonX[i][j], self.PolygonY[i][j]    = random.randint(-self.ScreenSizeX/2, self.ScreenSizeX + 500), random.randint(-self.ScreenSizeY/2, self.ScreenSizeY + 500)
                self.PolygonX[i][j], self.PolygonY[i][j] = self.screenSizeX/2-160, self.screenSizeY/2-130
                self.moveX[i][j], self.moveY[i][j] = random.randint(-5, 5), random.randint(-5, 5)
                self.colorR[i][j], self.colorG[i][j], self.colorB[i][j] = random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)


        # if(Background.Polygon[0][0] == None):
        #
        #     for i in range(0, 5):
        #         self.Polygon[0][i] = pygame.image.load(self.rect.replace('-', str(i+1)))
        #         self.Polygon[1][i] = pygame.image.load(self.tr.replace('-', str(i+1)))
        #         self.Polygon[2][i] = pygame.image.load(self.cir.replace('-', str(i+1)))
        #         self.Polygon[3][i] = pygame.image.load(self.fa.replace('-', str(i+1)))
        #         self.Polygon[4][i] = pygame.image.load(self.yut.replace('-', str(i+1)))




    def update(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if(self.PolygonX[i][j] > self.screenSizeX+200 or self.PolygonX[i][j] < -self.screenSizeX+400):
                    self.moveX[i][j] *= -1
                elif(self.PolygonY[i][j] > self.screenSizeY+200 or self.PolygonY[i][j] < -self.screenSizeY+400):
                    self.moveY[i][j] *= -1

                self.PolygonX[i][j] += self.moveX[i][j]
                self.PolygonY[i][j] += self.moveY[i][j]
                #self.Polygon[i][j] = pygame.transform.rotate(self.Polygon[i][j], 1)
        #self.PolygonDegree += 0.02


        pass

    def draw(self, SCREEN):

        for i in range(0, 5):
             for j in range(0, 5):
                #SCREEN.blit(self.Polygon[i][j], (self.PolygonX[i][j], self.PolygonY[i][j]))

                pygame.draw.polygon(SCREEN, (self.colorR[i][j], self.colorG[i][j], self.colorB[i][j]), ((self.PolygonX[i][j],self.PolygonY[i][j]),(self.PolygonX[i][j] + 400, self.PolygonY[i][j]),(self.PolygonX[i][j] + 400, self.PolygonY[i][j] + 400),(self.PolygonX[i][j], self.PolygonY[i][j] + 400)))

        pass

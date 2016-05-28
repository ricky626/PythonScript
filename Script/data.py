import my_framework

from my_engine import *
from my_data import GetData

import urllib.request
import xml.etree.ElementTree as etree


name = "Data"
my_data = GetData()

class Data:
    background = None
    button = [None for i in range(0, 5)]



    def __init__(self):
        my_data.save()

        self.tree = etree.parse("data.xml")
        self.root = self.tree.getroot()


        for i in self.root.iter("list"):
            print(i.findtext("batchMenu"))

        self.buttonX = [0 for i in range(0, 5)]
        self.buttonY = [0 for i in range(0, 5)]


        if(Data.background == None):
            Data.background = load_image("res/background.png")

            for i in range(0, 5):
                self.button[i] = load_image("res/button.png")
                self.buttonX[i] = 300
                self.buttonY[i] = (i * 130) + 50




        pass

    def update(self):

        pass

    def draw(self):
        self.background.draw(0, 0)

        for i in range(0, 5):
            self.button[i].draw(self.buttonX[i], self.buttonY[i])

        pass

    def handle_events(self):

        pass






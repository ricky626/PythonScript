
class DataManager:
    def __init__(self):
        self.name = list()
        self.place = list()
        self.money = list()
        self.persons = list()
        self.age = list()
        self.etc = list()

        pass

    def load(self, filename):
        f = open("data/" + filename + ".txt")

        self.data_list = f.readline().split()

        for i in range(0, 6):
            self.data_list.pop(0)

        while(1):
            self.data_list = f.readline().split()

            if not self.data_list: break

            self.name.append(self.data_list[0])
            self.place.append(self.data_list[1])
            self.money.append(self.data_list[2])
            self.persons.append(self.data_list[3])
            self.age.append(self.data_list[4])
            self.etc.append(self.data_list[5])
        pass



class LotteWorld(DataManager):

    def __init__(self):
        DataManager.__init__(self)

        self.load("롯데월드")
        pass

    pass

class Everland(DataManager):
    def __init__(self):
        DataManager.__init__(self)

        self.load("에버랜드")
        pass

    pass

class Seoulland(DataManager):
    def __init__(self):
        DataManager.__init__(self)

        self.load("서울랜드")
        pass

    pass


def main():
    lotteworld = LotteWorld()
    seoulland = Seoulland()
    everland = Everland()



    print(lotteworld.name)
    print(lotteworld.place)
    print(lotteworld.money)
    print(lotteworld.persons)
    print(lotteworld.age)
    print(lotteworld.etc)

    print(seoulland.name)
    print(seoulland.place)
    print(seoulland.money)
    print(seoulland.persons)
    print(seoulland.age)
    print(seoulland.etc)

    print(everland.name)
    print(everland.place)
    print(everland.money)
    print(everland.persons)
    print(everland.age)
    print(everland.etc)

    pass


main()


import urllib.request
import xml.etree.ElementTree as etree


class GetData:

    key = "aeQOITO0q7hDO2TJM7Be6LosLu7ShLAcPcI8wkDhUf0%2B0nxs5zgY%2FmJfBYo%2BmPdmcxo2zEH%2FgmdCl%2BsDkaSu%2Bw%3D%3D"
    url = "http://data.ex.co.kr/exopenapi/business/representFoodServiceArea?serviceKey=aeQOITO0q7hDO2TJM7Be6LosLu7ShLAcPcI8wkDhUf0%2B0nxs5zgY%2FmJfBYo%2BmPdmcxo2zEH%2FgmdCl%2BsDkaSu%2Bw%3D%3D&type=xml"

    def __init__(self):
        self.tree = etree.parse("res/xml/data.xml")
        self.root = self.tree.getroot()

        pass


    def save(self):
        xml = urllib.request.urlopen(self.url).read()
        f = open("res/xml/data.xml", "wb")
        f.write(xml)
        f.close()
        pass


    def test_print(self):
        count = 0

        for a in self.root.iter("list"):
            print(count)
            print(a.findtext("batchMenu"))
            print(a.findtext("direction"))
            print(a.findtext("routeCode"))
            print(a.findtext("routeName"))
            print(a.findtext("salePrice"))
            print(a.findtext("serviceAreaCode"))
            print(a.findtext("serviceAreaName"))
            print(count)
            count += 1



        pass

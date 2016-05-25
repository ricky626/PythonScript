
import urllib.request
import xml.etree.ElementTree as etree

def main():
    tree = etree.parse("data.xml")
    root = tree.getroot()

    for a in root.iter("list"):
        print(a.findtext("batchMenu"))
        print(a.findtext("direction"))
        print(a.findtext("routeCode"))
        print(a.findtext("routeName"))
        print(a.findtext("salePrice"))
        print(a.findtext("serviceAreaCode"))
        print(a.findtext("serviceAreaName"))


class GetData:

    key = "aeQOITO0q7hDO2TJM7Be6LosLu7ShLAcPcI8wkDhUf0%2B0nxs5zgY%2FmJfBYo%2BmPdmcxo2zEH%2FgmdCl%2BsDkaSu%2Bw%3D%3D"
    url = "http://data.ex.co.kr/exopenapi/business/representFoodServiceArea?serviceKey=aeQOITO0q7hDO2TJM7Be6LosLu7ShLAcPcI8wkDhUf0%2B0nxs5zgY%2FmJfBYo%2BmPdmcxo2zEH%2FgmdCl%2BsDkaSu%2Bw%3D%3D&type=xml"

    def main(self):
        data = urllib.request.urlopen(self.url).read()
        f = open("data.xml", "wb")
        f.write(data)
        f.close()
        print("정보 가져오기 완료")


getData = GetData()

getData.main()


main()

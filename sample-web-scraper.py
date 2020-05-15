from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

class Dam:
    def __init__(self, name, date1, time1, water_level1, date2, time2, water_level2, nhwl):
        self.name = name
        self.date1 = date1
        self.time1 = time1
        self.water_level1 = water_level1
        self.date2 = date2
        self.time2 = time2
        self.water_level2 = water_level2
        self.nhwl = nhwl

def process_dam_info(name, details):
    # date today
    date1 = details[13]
    # time taken today
    time1 = details[1]
    # water level today
    water_level1 = details[2]
    # date yesterday
    date2 = details[23]
    # time taken yesterday
    time2 = details[14]
    # water level yesterday
    water_level2 = details[15]
    # normwal high water level
    nhwl = details[5]

    dam = Dam(name, date1, time1, water_level1, date2, time2, water_level2, nhwl)

    print(dam.name)
    print(dam.date1.text, dam.time1.text)
    print("Water Level (m):", dam.water_level1.text)
    print(dam.date2.text, dam.time2.text)
    print("Water Level (m):", dam.water_level2.text)
    print("Difference:", "{:.2f}".format(float(dam.water_level1.text) - float(dam.water_level2.text)), "\n")

r = get('http://bagong.pagasa.dost.gov.ph/flood')
soup = BeautifulSoup(r.text)
table = soup.find("table", attrs={'class':'dam-table'})
table_body = table.find("tbody")

ctr = 0
rows = table_body.find_all("tr")
for row in rows:
    ctr += 1
    # get the row that has the dam name
    dam_row = row.find("td", attrs={'class':'current-dam'})

    # collate the information per dam
    if dam_row != None:
        dam_name = dam_row.text
        dam_info = row.find_all("td", attrs={'class':'td-' + dam_name.replace(" ", "-")})
    else:
        dam_info2 = row.find_all("td", attrs={'class':'td-' + dam_name.replace(" ", "-")})
        dam_info.extend(dam_info2)

    # only process the information once all items are gathered (every 4th row)
    if ctr % 4 == 0:
        process_dam_info(dam_name, dam_info)
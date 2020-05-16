from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import json

class Dam:
    def __init__(self, name, date1, time1, water_level1, date2, time2, water_level2, difference, nhwl):
        self.name = name
        self.date1 = date1
        self.time1 = time1
        self.water_level1 = water_level1
        self.date2 = date2
        self.time2 = time2
        self.water_level2 = water_level2
        self.difference = difference
        self.nhwl = nhwl 

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def process_dam_info(name, details):
    # date today
    date1 = details[13].text
    # time taken today
    time1 = details[1].text
    # water level today
    water_level1 = details[2].text
    # date yesterday
    date2 = details[23].text
    # time taken yesterday
    time2 = details[14].text
    # water level yesterday
    water_level2 = details[15].text
    # water level difference between today ad yesterday
    difference = float(water_level1) - float(water_level2)
    # normwal high water level
    nhwl = details[5].text

    dam = Dam(name, date1, time1, water_level1, date2, time2, water_level2, difference, nhwl)

    return dam

def print_dam_info(dam):
    damJSONData = json.dumps(dam.toJson(), indent=4)
    print(json.loads(damJSONData))
    
    # for printing in console not using JSON
    # print(dam.name)
    # print(dam.date1, dam.time1)
    # print("Water Level (m):", dam.water_level1)
    # print(dam.date2, dam.time2)
    # print("Water Level (m):", dam.water_level2)
    # print("Difference:", "{:.2f}".format(dam.difference), "\n")

r = get('http://bagong.pagasa.dost.gov.ph/flood')
soup = BeautifulSoup(r.text, features="html.parser")
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
        dam_info =  process_dam_info(dam_name, dam_info)
        print_dam_info(dam_info)
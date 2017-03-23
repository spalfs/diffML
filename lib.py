import xml.etree.ElementTree as ET
from pprint import pprint
import csv

def getXML(n):
    tree = ET.parse("xmldata/"+n+".XML")
    root = tree.getroot()

    data = []

    for apartment in root:
        screens = apartment.findall('Picture')
        for screen in screens:
            tmp = {}
            tmp['info'] = []
            for screenObject in screen:
                if screenObject.tag == "Title":
                    tmp['title'] = screenObject.text
                    data.append(tmp)

                if str(screenObject.tag).find("Elements") != -1:
                    name = screenObject.findall("Name")
                    plvl = screenObject.findall("Passwordlevel")
                    dyne = screenObject.findall("DynEleFkt_0")
                    if not name or not plvl or not dyne:
                        continue
                    if name[0].text == None:
                        continue
                    func = dyne[0].findall("Name")
                    tmp['info'].append({ "name" : name[0].text,
                                         "plvl" : plvl[0].text,
                                         "func" : func[0].text })

    return data

def writeCSV(n,data):
    with open(n+'.csv','w') as f:
        writer = csv.writer(f)
        for screen in data:
            writer.writerow([screen['title']])
            for v in screen['info']:
                writer.writerow((v['func'],v['name'],v['plvl']))

def diff(n1,n2):
    f = open(n1+'.csv','r')
    reader = csv.reader(f)
    data1 = []
    for row in reader:
        tmp = {}
        if len(row) == 1:
            tmp["title"] = row[0]

        if tmp == {}:
            continue
        data1.append(tmp)

    pprint(data1)







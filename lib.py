import xml.etree.ElementTree as ET
import csv

def getXML(num):
    tree = ET.parse("xmldata/"+num+".XML")
    root = tree.getroot()

    data = []

    for apartment in root:
        screens = apartment.findall('Picture')
        for screen in screens:
            tmp = {}
            tmp['namesAndLevels'] = []
            for screenObject in screen:
                if screenObject.tag == "Title":
                    tmp['title'] = screenObject.text
                    data.append(tmp)

                if str(screenObject.tag).find("Elements") != -1:
                    name = screenObject.findall("Name")
                    plvl = screenObject.findall("Passwordlevel")
                    if not name or not plvl:
                        continue
                    if name[0].text == None:
                        continue
                    tmp['namesAndLevels'].append((name[0].text,plvl[0].text))

    return data

def writeCSV(num,data):
    with open(num+'.csv','w') as f:
        writer = csv.writer(f)
        for screen in data:
            writer.writerow([screen['title']])
            writer.writerows(screen['namesAndLevels'])

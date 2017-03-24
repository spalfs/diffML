import xml.etree.ElementTree as ET

def getXML(n):
    tree = ET.parse("xmldata/"+n)
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

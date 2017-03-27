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
                    dynf = screenObject.findall("DynEleFkt_0")
                    dynv = screenObject.findall("DynEleVar_0")
                    func = screenObject.findall("Function")

                    if not name:
                        continue
                    n = str(name[0].text)

                    findin = []
                    findin.append(n.find("Zahlenwert"))
                    findin.append(n.find("Bitmap Button"))
                    findin.append(n.find("Schalter"))
                    findin.append(n.find("Switch"))

                    worth = False
                    for i in findin:
                        if i != -1:
                            worth = True

                    if not worth:
                        continue

                    if dynv:
                        func = dynv[0].findall("ProjectVar")[0].text
                    elif dynf:
                        func = dynf[0].findall("Name")[0].text
                    elif func:
                        func = func[0].text
                    else:
                        func = ""

                    tmp['info'].append({ "name" : name[0].text,
                                         "plvl" : plvl[0].text,
                                         "func" : func          })


    return data

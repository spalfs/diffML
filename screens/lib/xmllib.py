import xml.etree.ElementTree as ET

def getXML(n,ver):
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
                    if ver == 6.5:
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

                    elif ver == 7.2:
                        for element in screenObject:
                            if element.tag == "Name":
                                name = element.text

                            find = str(element.tag).find("ExpProps")
                            if find != -1:
                                for i in range(len(element)):
                                    if element[i].text == "Value.Variable":
                                        func = element[i+1].text
                                        start = func.find("<SymVarName>") + len("<SymVarName") + 1
                                        end = func.find("</SymVarName>")
                                        func = func[start:end]
                                    elif element[i].text == "Value.Passwordlevel":
                                        plvl = element[i+1].text
                                        plvl = plvl[15:16]

                        if name == "":
                            func = ""
                            plvl = ""
                            name = ""
                            continue
                        else:
                            tmp['info'].append({    "name" : name,
                                                    "plvl" : plvl,
                                                    "func" : func})
                            func = ""
                            plvl = ""
                            name = ""

    return data

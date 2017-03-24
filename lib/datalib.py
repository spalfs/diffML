
def diffScreens(data1, data2):
    diffData = {}
    diffData["data1missing"] = []
    diffData["data2missing"] = []
    for data1Screen in data1:
        found = False
        for data2Screen in data2:
            if data1Screen['title'] == data2Screen['title']:
                found = True
        if not found:
            diffData["data2missing"].append(data1Screen['title'])

    for data2Screen in data2:
        found = False
        for data1Screen in data1:
            if data1Screen['title'] == data2Screen['title']:
                found = True
        if not found:
            diffData["data1missing"].append(data2Screen['title'])

    return diffData

def diffScreenVars(screen1, screen2):
    tmp = {}
    tmp['title'] = screen1['title']
    tmp['missingVars'] = []
    tmp['diffVars'] = []

    for var1 in screen1['info']:
        found = False
        for var2 in screen2['info']:
            if var1['name'] == var2['name']:
                found = True
                if var1['func'] == var2['func'] and var1['plvl'] == var2['plvl']:
                    continue
                else:
                    tmp['diffVars'].append({ "data1" : var1, "data2" : var2 })
        if not found:
            tmp['missingVars'].append(var1)

        if tmp['diffVars'] == [] and tmp['missingVars'] == []:
            return False

    return tmp

def diffAll(data1, data2):
    diffData = []

    for data1Screen in data1:
        for data2Screen in data2:
            if data1Screen['title'] == data2Screen['title']:
                tmp = diffScreenVars(data1Screen,data2Screen)
                if tmp:
                    diffData.append(tmp)

    for data2Screen in data2:
        for data1Screen in data1:
            if data1Screen['title'] == data2Screen['title']:
                tmp = diffScreenVars(data2Screen,data1Screen)
                if tmp:
                    diffData.append(tmp)

    if diffData == []:
        return False

    return diffData



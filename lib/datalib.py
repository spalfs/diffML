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

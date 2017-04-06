def diffRecipes(data1, data2):
    diffData = {}
    diffData["data1missing"] = []
    diffData["data2missing"] = []
    for data1Screen in data1:
        found = False
        for data2Screen in data2:
            if data1Screen['Variable'] == data2Screen['Variable']:
                found = True
        if not found:
            diffData["data2missing"].append(data1Screen['Variable'])

    for data2Screen in data2:
        found = False
        for data1Screen in data1:
            if data1Screen['Variable'] == data2Screen['Variable']:
                found = True
        if not found:
            diffData["data1missing"].append(data2Screen['Variable'])

    return diffData

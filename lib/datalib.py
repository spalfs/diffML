def diff(data1, data2):
    for data1Screen in data1:
        found = False
        for data2Screen in data2:
            if data1Screen['title'] == data2Screen['title']:
                found = True
        if not found:
            print("No matching screen for " + data1Screen['title'] + " in data2.")



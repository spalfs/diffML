import csv

def writeCSV(n,data):
    with open(n+'.csv','w') as f:
        writer = csv.writer(f)
        for screen in data:
            writer.writerow([screen['title']])
            for v in screen['info']:
                writer.writerow((v['func'],v['name'],v['plvl']))

def readCSV(n):
    with open(n+'.csv','r') as f:
        reader = csv.reader(f)
        data = []
        tmp = {}
        for row in reader:
            if len(row) == 1:
                data.append(tmp)
                tmp = {}
                tmp['info'] = []
                tmp["title"] = row[0]
            else:
                tmp['info'].append({ "func" : row[0],
                                     "name" : row[1],
                                     "plvl" : row[2] })
        return data[1:]

def writeCSVDiff(diffData):
    with open("diff.csv",'w') as f:
        writer = csv.writer(f)
        for screen in diffData:
            if screen['missingVars'] != []:
                writer.writerow([screen['title'],'MISSING'])
                for var in screen['missingVars']:
                    writer.writerow([var[1]['name'],var[1]['func'],var[1]['plvl'],var[0]])
            if screen['diffVars'] != []:
                writer.writerow([screen['title'],'DIFFERENCES'])
                for var in screen['diffVars']:
                    writer.writerow([var['data1']['name'], var['data1']['func'], var['data2']['func'], var['data1']['plvl'], var['data2']['plvl']])

def writeCSVScreensDiff(diffData):
    with open("diff.csv","w") as f:
        writer = csv.writer(f)
        while len(diffData['data1missing']) > len(diffData['data2missing']):
            diffData['data2missing'].append("")

        while len(diffData['data2missing']) > len(diffData['data1missing']):
            diffData['data1missing'].append("")

        for row in range(len(diffData['data1missing'])):
            writer.writerow([diffData['data1missing'][row],diffData['data2missing'][row]])

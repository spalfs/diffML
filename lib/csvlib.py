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



import csv

def writeCSVVarsDiff(diffData):
    with open("diff.csv","w") as f:
        writer = csv.writer(f)
        while len(diffData['data1missing']) > len(diffData['data2missing']):
            diffData['data2missing'].append("")

        while len(diffData['data2missing']) > len(diffData['data1missing']):
            diffData['data1missing'].append("")

        for row in range(len(diffData['data1missing'])):
            writer.writerow([diffData['data1missing'][row],diffData['data2missing'][row]])

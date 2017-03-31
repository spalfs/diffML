import csv

def csvSave(path,differences):
    with open(path,'w') as f:
        writer = csv.writer(f)
        for difference in differences:
            writer.writerow(difference.split(','))

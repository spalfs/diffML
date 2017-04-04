import xml.etree.ElementTree as ET
import csv

def csvSave(path,differences):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for difference in differences:
            writer.writerow(difference.split(','))

def csvExport(path, tree):
    root = tree.getroot()
    with open(path, 'w') as f:
        writer = csv.writer(f)
        pathFind(root, writer)

def pathFind(root, writer, depth = -1):
    depth += 1
    for element in root:
        indent = []
        for i in range(depth):
            indent.append(',')
        data = [str(element.tag), str(element.text), str(element.attrib)]
        writer.writerow(indent+data)
        pathFind(element,writer,depth)

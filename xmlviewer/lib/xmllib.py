import xml.etree.ElementTree as ET
from pprint import pprint

def getXML(path):
    tree = ET.parse(path)

    root = tree.getroot()

    xmlData = []
    for element in root:
        tmp = {}
        tmp['info'] = (str(element.tag), str(element.text), str(element.attrib))
        xmlData.append(tmp)



    #xmlData = getChildren(root)

    return xmlData

def getChildren(root):
    # Fancy recursive algorithm
    #for element in root:
    #    tmp = {}
    #    tmp['info'] = (str(element.tag), str(element.text), str(element.attrib))
    #
    #tmp['children'] = getChildren(element)
    return

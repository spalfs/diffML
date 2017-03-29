def find(root, tag, text, attrib):
    for element in root.iter(tag):
        if str(element.text) == text and str(element.attrib) == attrib:
            return element

def compareXML(matching, treeOne, selectedOne, treeTwo, selectedTwo):
    rootOne = treeOne.getroot()
    rootTwo = treeTwo.getroot()

    elementOne = find(rootOne, selectedOne[0].data(), selectedOne[1].data(), selectedOne[2].data())
    elementTwo = find(rootTwo, selectedTwo[0].data(), selectedTwo[1].data(), selectedTwo[2].data())

    differences = []

    for eA in elementOne:
        difference = {}
        found = False
        for eB in elementTwo:
            if matching == "Tag":
                if str(eA.tag) == str(eB.tag):
                    found = True
                    if str(eA.text) != str(eB.text):
                        difference['text'] = str(eA.text) + " vs " + str(eB.text)
                    if str(eA.attrib) != str(eB.attrib):
                        difference['attrib'] = str(eA.attrib) + " vs " + str(eB.attrib)

            elif matching == "Attribute":
                if str(eA.attrib) == str(eB.attrib):
                    found = True
                    if str(eA.text) != str(eB.text):
                        difference['text'] = str(eA.text) + " vs " + str(eB.text)
                    if str(eA.tag) != str(eB.tag):
                        difference['tag'] = str(eA.tag) + " vs " + str(eB.tag)

            elif matching == "Text":
                if str(eA.text) == str(eB.text):
                    found = True
                    if str(eA.attrib) != str(eB.attrib):
                        difference['attrib'] = str(eA.attrib) + " vs " + str(eB.attrib)
                    if str(eA.tag) != str(eB.tag):
                        difference['tag'] = str(eA.tag) + " vs " + str(eB.tag)

        if not found:
            difference['tag'] = "ElementTwo missing " + str(eA.tag)

        if difference != {}:
            differences.append(difference)

    for eA in elementTwo:
        difference = {}
        found = False
        for eB in elementOne:
            if matching == "Tag":
                if str(eA.tag) == str(eB.tag):
                    found = True
            elif matching == "Attribute":
                if str(eA.attrib) == str(eB.attrib):
                    found = True
            elif matching == "Text":
                if str(eA.text) == str(eB.text):
                    found = True

        if not found:
            difference['tag'] = "ElementOne missing " + str(eA.tag)

        if difference != {}:
            differences.append(difference)

    return differences

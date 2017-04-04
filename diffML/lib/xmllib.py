def find(root, tag, text, attrib):
    for element in root.iter(tag):
        tryText = str(element.text)
        if tryText == "None":
            tryText = ''
        if tryText == text and str(element.attrib) == attrib:
            return element

def compareXML(matching, treeOne, selectedOne, treeTwo, selectedTwo):
    rootOne = treeOne.getroot()
    rootTwo = treeTwo.getroot()

    elementOne = find(rootOne, selectedOne[0].data(), selectedOne[1].data(), selectedOne[2].data())
    elementTwo = find(rootTwo, selectedTwo[0].data(), selectedTwo[1].data(), selectedTwo[2].data())

    differences = []

    for eA in elementOne:
        difference = str()
        found = False
        for eB in elementTwo:
            if matching == "Tag":
                if eA.tag == eB.tag:
                    found = True
                    if eA.text != eB.text:
                        difference = eA.tag + " , " + str(eA.text) + " , " + str(eB.text) + '.'
                    if eA.attrib != eB.attrib:
                        difference += eA.tag + " , " + str(eA.attrib) + " , " + str(eB.attrib)

            elif matching == "Attribute":
                if eA.attrib == eB.attrib:
                    found = True
                    if eA.text != eB.text:
                        difference = str(eA.attrib) + " , " + str(eA.text) + " , " + str(eB.text) + '.'
                    if eA.tag != eB.tag:
                        difference += str(eA.attrib) + " , " + eA.tag + " , " + eB.tag

            elif matching == "Text":
                if eA.text == eB.text:
                    found = True
                    if eA.attrib != eB.attrib:
                        difference = str(eA.text) + " , " + str(eA.attrib) + " , " + str(eB.attrib) + '.'
                    if eA.tag != eB.tag:
                        difference += str(eA.text) + " , " + eA.tag + " , " + eB.tag

        if difference.count(',') == 4:
            differences.append(difference[:difference.find('.')])
            difference = difference[difference.find('.')+1:]

        difference = difference.replace(".","")

        if not found:
            if matching == "Tag":
                difference = elementTwo.tag + " missing " + eA.tag
            elif matching == "Attribute":
                difference = str(elementTwo.attrib) + " missing " + str(eA.attrib)
            elif matching == "Text":
                difference = str(elementTwo.text) + " missing " + str(eA.text)

        if difference != "":
            differences.append(difference)

    for eA in elementTwo:
        difference = str()
        found = False
        for eB in elementOne:
            if matching == "Tag":
                if eA.tag == eB.tag:
                    found = True
            elif matching == "Attribute":
                if eA.attrib == eB.attrib:
                    found = True
            elif matching == "Text":
                if eA.text == eB.text:
                    found = True

        if not found:
            if matching == "Tag":
                difference = elementOne.tag + " missing " + eA.tag
            elif matching == "Attribute":
                difference = str(elementOne.attrib) + " missing " + str(eA.attrib)
            elif matching == "Text":
                difference = str(elementOne.text) + " missing " + str(eA.text)

        if difference != "":
            differences.append(difference)

    return differences

from tkinter import messagebox
import xml.etree.ElementTree as ET

def readDoc(docName):
    tree = ET.parse(docName.get()+'.fods')
    root = tree.getroot()
    officeSpace = '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}'
    tableSpace = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table'

    body = root.findall(officeSpace+'body')[0]
    workbook = body.findall(officeSpace+'spreadsheet')[0]

    data = []
    for sheet in workbook:
        for row in sheet:
            rowTmp = []
            for cell in row:
                if cell and cell[0].text != None:
                    findIfRepeat = str(cell.attrib).find("number-columns-repeated")
                    if findIfRepeat == -1:
                        rowTmp.append(cell[0].text)
                    else:
                        times = int(str(cell.attrib)[findIfRepeat+27:findIfRepeat+28])
                        for i in range(times):
                            rowTmp.append(cell[0].text)
            if rowTmp == []:
                continue
            if rowTmp == ['Schlüsselwort', 'ZENONSTR.TXT', 'GB_EN.TXT', 'FR_FR.TXT']:
                continue
            data.append(rowTmp)

    return data

def writeCSV(docName,csvName):
    data = readDoc(docName)

    f = open(csvName.get()+'.csv','w')

    for row in data:
        for cell in row:
            tmp = cell.replace('\x81','')
            f.write(tmp+',')
        f.write('\n')

    f.close()

def checkDuplicates(docName):
    data = readDoc(docName)

    seen = set()
    dupes = set()

    for row in data:
        if row[0] not in seen:
            seen.add(row[0])
        else:
            dupes.add(row[0])

    messagebox.showinfo("The duplicate strings:",dupes)

def checkMissing(docName):
    data = readDoc(docName)

    notFilled = list()
    for row in data:
        if len(row) != 4:
            notFilled.append(row)

    messagebox.showinfo("Rows without four cells:",notFilled)



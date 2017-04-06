def save(main,docName,csvName,svnName):
    f = open("savedata.txt","w")
    data = docName.get() + ',' + csvName.get() + ',' + svnName.get()
    f.write(data)
    f.close()
    main.destroy()

def load():
    data = []
    try:
        f = open("savedata.txt","r")
        data = f.read().split(',')
    except:
        data.append("CSVGenerator")
        data.append("output")
        data.append("https://hhsvn.hoefliger.de:50443/svn/vorlagen/LRT100/csv")
    return data



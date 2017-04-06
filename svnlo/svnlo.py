#!/usr/bin/python3
from tkinter import Tk, Frame, Button, Entry, Label, LEFT, RIGHT, END, X, BOTH
from lib.docCalls import readDoc, writeCSV, checkDuplicates, checkMissing
from lib.svnCalls import checkout, revert, difference, commit
from lib.manCalls import save, load

saveNames = load()
main = Tk()

main.title("svnlo")

frame1 = Frame()
frame1.pack(fill=X)

Label(frame1,text="Generate from").pack(side=LEFT,padx=5,pady=5)

docName = Entry(frame1)
docName.pack(fill=X, padx=5, expand=True)
docName.delete(0, END)
docName.insert(0, saveNames[0])

frame2 = Frame()
frame2.pack(fill=X)

Label(frame2,text="Generate to").pack(side=LEFT,padx=5,pady=5)

csvName = Entry(frame2)
csvName.pack(fill=X, padx=5, expand=True)
csvName.delete(0, END)
csvName.insert(0, saveNames[1])

frame3 = Frame()
frame3.pack(fill=X)

Button(frame3,text="Check Duplicates",  command=lambda:checkDuplicates(docName)).pack(side=LEFT,padx=5,pady=5)
Button(frame3,text="Check Missing",     command=lambda:checkMissing(docName)).pack(side=LEFT,padx=5,pady=5)
Button(frame3,text="Generate",          command=lambda:writeCSV(docName,csvName)).pack(side=RIGHT,padx=5,pady=5)

frame4 = Frame()
frame4.pack(fill=BOTH, expand=True)

svnName = Entry(frame4)
svnName.pack(fill=X, padx=5, expand=True)
svnName.delete(0, END)
svnName.insert(0, saveNames[2])

Button(frame4,text="Checkout",          command=lambda:checkout(svnName,csvName)).pack(side=LEFT,padx=5,pady=5)
Button(frame4,text="Revert",            command=lambda:revert(svnName)).pack(side=LEFT,padx=5,pady=5)
Button(frame4,text="Commit",            command=lambda:commit(svnName)).pack(side=RIGHT,padx=5,pady=5)
Button(frame4,text="Difference",        command=lambda:difference(svnName)).pack(side=RIGHT,padx=5,pady=5)

main.protocol("WM_DELETE_WINDOW",               lambda:save(main,docName,csvName,svnName))

main.mainloop()

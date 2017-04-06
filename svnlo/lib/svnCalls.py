from tkinter import messagebox, END
import subprocess
import win32process

def call(a,b,c):
    cmd = []
    cmd.append('svn.exe')
    cmd.append(a)
    cmd.append(b)
    if c != '':
        cmd.append(c)
    print(cmd)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.check_output(cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=si)

    return process


def checkout(svnName,csvName):
    folder = svnName.get().split('/')[-1]+'/'
    csvName.delete(0, END)
    csvName.insert(0, folder + "output")

    process = call(r'checkout',svnName.get(),'')
 
    parse = str(process)
    n = parse.find("Checked out revision")
    good = parse[n:n+27]

    messagebox.showinfo("Checkout Message:",good)

def revert(svnName):
   
    process = call(r'revert',svnName.get().split('/')[-1]+r"\*",'')

    messagebox.showinfo("Revert Message:","Revert Successful")

def difference(svnName):
    
    process = call(r'diff',svnName.get().split('/')[-1],'')

    parse = str(process).split('\\n')
    good = []
    for line in parse:
        line = line.replace('\\r','')
        line = line.replace('\\',' ')
        if line[0] == '-':
            good.append(line+'\n')
        elif line[0] == '+':
            good.append(line+'\n')

    if good == []:
        messagebox.showinfo("Difference Message:","No difference.")
    else:
        messagebox.showinfo("Difference Message:",good)

def commit(svnName):
   
    process = call(r'commit',r'-m commit from svnlo',svnName.get().split('/')[-1]+r'\*')

    print(process)

    messagebox.showinfo("Commit Message:",process)



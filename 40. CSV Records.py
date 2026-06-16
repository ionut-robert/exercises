#40. CSV Records.py
from tkinter import *
import csv 

def opencsv(e):
    global ids,name,salary,data

    file_csv = open('Tkinter/39.  Emplyees.csv','r')
    reader = csv.reader(file_csv)
    
    data = []
    for t in reader:
        data.append(t)

    file_csv.close()

    ids = [row[0] for row in data]
    name = [row[1] for row in data]
    salary = [row[2] for row in data]


def InfoUpload(e):
    idvar.set(next(row[0] for row in data if row[0]==e))
    NameVar.set(next(row[1] for row in data if row[0]==e))
    SalaryVar.set(next(row[2] for row in data if row[0]==e))
    

def OverwriteCSV():
    for row in data:
        if row[0] == idvar.get():
            row[1] = employeeName_Entry.get()
            row[2] = employeeSal_entry.get()

    file_csv = open('Tkinter/39.  Emplyees.csv','w')
    writer = csv.writer(file_csv)
    for row in data:
        writer.writerow(row)
    file_csv.close()

def Savexit():
    OverwriteCSV()
    win.destroy()

win = Tk()
win.title('CSV Records')
win.geometry('700x300+600+350')

employee_label = Label(win,text='Employee list')
employee_label.grid(row=0,column=0)

opencsv(None)
var = StringVar(value='Select Emplyee')
employee_spnbox = OptionMenu(win,var,*ids,command=InfoUpload)
employee_spnbox.grid(row=0,column=1)

employeeId_label = Label(win,text='Emplyee ID')
employeeId_label.grid(row=2,column=0)
idvar=StringVar(value=None)
employeeId_label = Entry(win,width=20,textvariable=idvar)
employeeId_label.grid(row=2,column=1)

employeeName_label = Label(win,text='Name')
employeeName_label.grid(row=2,column=3)
NameVar = StringVar(value=None)
employeeName_Entry = Entry(win,width=20,textvariable=NameVar)
employeeName_Entry.grid(row=2,column=4)

employeeSal_label = Label(win,text='Salary')
employeeSal_label.grid(row=3,column=0)
SalaryVar=StringVar(value=None)
employeeSal_entry = Entry(win,width=20,textvariable=SalaryVar)
employeeSal_entry.grid(row=3,column=1)

btn = Button(win,text='Save',command=OverwriteCSV)
btn.grid(row=4,column=1)

btn2 = Button(win,text='Save&Exit',command=Savexit)
btn2.grid(row=4,column=3,columnspan=2)

win.mainloop()

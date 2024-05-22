from tkinter import *
from tkinter import ttk
import sqlite3 as sl

class LabEnt:
    def __init__(self, form, label, data, packside):
        self.Lab1=Label(form, text=label)
        self.Ent1=Entry(form)
        self.Lab1.pack(side=packside)
        self.Ent1.pack(side=packside)
        self.Ent1.insert(0,data)
    def get(self):
        return self.Ent1.get()
    def set(self,data):
        self.Ent1.delete(0,END)
        self.Ent1.insert(0,data)
        

class scene_main:
    def __init__(self):
        
        con = sl.connect('Logs.db')
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM DEVICES""")
            device_list=cursor.fetchall()
            cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(device_list[0][0]+"""'"""))
            device_data=cursor.fetchall()
        
        self.device_id=device_data[0][0]
        self.device_imei=device_data[0][1]
        self.device_name=device_data[0][2]
        self.device_type=device_data[0][3]
        
        self.FormMain=Tk()
        self.FormMain.geometry("400x360")
        self.FormMain.title("Тестовый сервер")
        self.Lframe=Frame(self.FormMain)
        self.Lframe.pack(side=LEFT)
        self.Rframe=Frame(self.FormMain)
        self.Rframe.pack(side=LEFT)
        self.LBframe=Frame(self.Lframe)
        self.LBframe.pack(side=BOTTOM)
        
        self.Bx=Listbox(self.Lframe, selectmode=SINGLE, height=20, width=40)
        self.Bx.pack(side=LEFT)
        self.Scrl=Scrollbar(self.Lframe, command=self.Bx.yview)
        self.Scrl.pack(side=LEFT, fill=Y)
        self.RefreshBox(device_list)
        
        self.ButSelect=Button(self.LBframe,text="Выбрать")
        self.ButSelect.config(command=lambda:self.Select(device_list))
        self.ButSelect.pack(side=LEFT)
        
        self.ButSelect=Button(self.LBframe,text="Тест")
        self.ButSelect.config(command=lambda:self.Select(device_list))
        self.ButSelect.pack(side=LEFT)
        
        self.LabEntID=LabEnt(self.Rframe,"ID",self.device_id,TOP)
        self.LabEntImei=LabEnt(self.Rframe,"IMEI",self.device_imei,TOP)
        self.LabEntName=LabEnt(self.Rframe,"Номер",self.device_name,TOP)
        self.LabEntType=LabEnt(self.Rframe,"Тип",self.device_type,TOP)
        
        self.FormMain.mainloop()
        
    def RefreshBox(self, data):
        self.Bx.delete(0,END)
        i=0 
        for str in data:
            self.Bx.insert(i,str)
            i+=1 
        
    def Select(self,device_list):
        index=device_list[self.Bx.curselection()[0]][0]
        con = sl.connect('Logs.db')
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(index)+"""'""")
            answear=cursor.fetchall()
        self.LabEntID.set(answear[0][0])
        self.LabEntImei.set(answear[0][1])
        self.LabEntName.set(answear[0][2])
        self.LabEntType.set(answear[0][3])
        
    def AddDevice(self):
        pass
    
m=scene_main()
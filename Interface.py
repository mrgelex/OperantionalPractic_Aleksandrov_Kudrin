from tkinter import *
from tkinter import ttk
import sqlite3 as sl
from Device import Device
from inter.comand import runserver
from threading import Thread

pathDB='inter/Logs.db'

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
        
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM DEVICES""")
            self.device_list=cursor.fetchall()
            cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(self.device_list[0][0]+"""'"""))
            device_data=cursor.fetchall()
        
        self.device_id=device_data[0][0]
        self.device_serial=device_data[0][1]
        self.device_imei=device_data[0][2]
        self.device_name=device_data[0][3]
        self.device_type=device_data[0][4]
        
        self.port="COM3"
        self.baudrate=9600
        self.timeout=1
        self.bytesize=8
        self.parity="N"
        self.stopbits=1
        
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
        self.RefreshBox()
        
        self.ButSelect=Button(self.LBframe,text="Выбрать")
        self.ButSelect.config(command=lambda:self.Select(self.device_list))
        self.ButSelect.pack(side=LEFT)
        
        self.ButSave=Button(self.LBframe,text="Добавить")
        self.ButSave.config(command=lambda:self.AddDevice())
        self.ButSave.pack(side=LEFT)
        
        self.ButSave=Button(self.LBframe,text="Сохранить")
        self.ButSave.config(command=lambda:self.SaveDevice())
        self.ButSave.pack(side=LEFT)
        
        self.ButSave=Button(self.LBframe,text="Удалить")
        self.ButSave.config(command=lambda:self.SaveDevice())
        self.ButSave.pack(side=LEFT)
        
        self.LabEntID=LabEnt(self.Rframe,"ID",self.device_id,TOP)
        self.LabEntSerial=LabEnt(self.Rframe,"serial",self.device_serial,TOP)
        self.LabEntImei=LabEnt(self.Rframe,"IMEI",self.device_imei,TOP)
        self.LabEntName=LabEnt(self.Rframe,"Номер",self.device_name,TOP)
        self.LabEntType=LabEnt(self.Rframe,"Тип",self.device_type,TOP)
        
        self.ButStart=Button(self.Rframe,text="Запуск опроса")
        self.ButStart.config(command=lambda:self.StartWork(self.LabEntID.get()))
        self.ButStart.pack(side=TOP)
        
        self.ButStart=Button(self.Rframe,text="Остановка опроса")
        self.ButStart.config(command=lambda:self.StopWork())
        self.ButStart.pack(side=TOP)
        
        self.ButStart=Button(self.Rframe,text="Запуск web сервера")
        self.ButStart.config(command=lambda:self.RunServer())
        self.ButStart.pack(side=TOP)
        
        self.ButComSet=Button(self.Rframe,text="Настройки COM")
        self.ButComSet.config(command=lambda:self.ComSetting())
        self.ButComSet.pack(side=TOP)
        
        self.FormMain.mainloop()
        
    def RefreshBox(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM DEVICES""")
            self.device_list=cursor.fetchall()
        self.Bx.delete(0,END)
        i=0 
        for str in self.device_list:
            self.Bx.insert(i,str)
            i+=1 
        
    def Select(self,device_list):
        index=device_list[self.Bx.curselection()[0]][0]
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(index)+"""'""")
            answear=cursor.fetchall()
        self.LabEntID.set(answear[0][0])
        self.LabEntSerial.set(answear[0][1])
        self.LabEntImei.set(answear[0][2])
        self.LabEntName.set(answear[0][3])
        self.LabEntType.set(answear[0][4])
        
    def SaveDevice(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""UPDATE DEVICES SET serial='"""+self.LabEntSerial.get()+"""',IMEI='"""+self.LabEntImei.get()+"""',name='"""+self.LabEntName.get()+"""',type='"""+self.LabEntType.get()+"""' WHERE id_device="""+self.LabEntID.get())
            con.commit()
        self.RefreshBox()
            
    def AddDevice(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""INSERT INTO DEVICES (serial,IMEI,name,type) VALUES ('"""+self.LabEntSerial.get()+"""','"""+self.LabEntImei.get()+"""','"""+self.LabEntName.get()+"""','"""+self.LabEntType.get()+"""')""")
            con.commit()
        self.RefreshBox()
        
    def DeleteDevice(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""DELETE FROM DEVICES WHERE id_device="""+self.LabEntID.get())
            con.commit()
        self.RefreshBox()
        
    def StartWork(self,id_device):
        self.Device=Device(id_device,self.port,self.baudrate,self.timeout,self.bytesize,self.parity,self.stopbits)
        self.Device.Start()
    
    def StopWork(self):
        self.Device.Stop()
        
    def RunServer(self):
        self.th2=Thread(target=runserver)
        self.th2.daemon=True
        self.th2.start()
        
    def ComSetting(self):
        self.FormComSet=Tk()
        self.FormComSet.geometry("150x280")
        self.FormComSet.title("Тестовый сервер")
        
        self.LabEntPort=LabEnt(self.FormComSet,"Порт",self.port,TOP)
        self.LabEntBaudrate=LabEnt(self.FormComSet,"Скорость",self.baudrate,TOP)
        self.LabEntTimeout=LabEnt(self.FormComSet,"Таймаут",self.timeout,TOP)
        self.LabEntBytesize=LabEnt(self.FormComSet,"Биты данных",self.bytesize,TOP)
        self.LabEntParity=LabEnt(self.FormComSet,"Четность",self.parity,TOP)
        self.LabEntStopBit=LabEnt(self.FormComSet,"Стоп бит",self.stopbits,TOP)
        self.ButStart=Button(self.FormComSet,text="Ок")
        self.ButStart.config(command=lambda:self.SaveCom())
        self.ButStart.pack(side=TOP)
        
        self.FormComSet.mainloop()
        
    def SaveCom(self):
        self.port=self.LabEntPort.get()
        self.baudrate=self.LabEntBaudrate.get()
        self.timeout=self.LabEntTimeout.get()
        self.bytesize=self.LabEntBytesize.get()
        self.parity=self.LabEntParity.get()
        self.stopbits=self.LabEntStopBit.get()
        self.FormComSet.destroy()
    
m=scene_main()
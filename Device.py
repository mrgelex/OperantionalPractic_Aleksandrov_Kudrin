import pymodbus.client as modbusClient
from pymodbus import ModbusException
from pymodbus import Framer
import sqlite3 as sl
from datetime import datetime
from threading import Thread
import time

pathDB='inter/Logs.db'

class Device:
    def __init__(self,id_device):
        con = sl.connect(pathDB)
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM DEVICES""")
        self.enable=False
        self.id_device=id_device
        self.adt1=0
        self.adt2=0
        self.adt3=0
        
        
    def Start(self):
        self.enable=True
        th=Thread(target=self.Thread)
        th.start()
        #th.join()
        
    def Stop(self):
        self.enable=False
        
    def Request1(self):
        try:
            response = self.client.read_holding_registers(address=512,count=64,slave=10)
            return response
        except ModbusException as exc:
            print("No connect")
            return exc
    
    def CheckVersion(self,resp):
        v9012=["DT1","DT2","DT3","Status_v9","Depth","Power","AI2","StringStatus","Status_v5","TimeBeforeStart","Depth2","Speed","Power2","NSucYes","NSucTod","NSucTot",
               "NWires","WorkDepth","WorkSpeed","TmClearDelta","TmClearAbs","TmWaitWorkDepth","TmWaitLubr","DepthClearUst","TmClearUst","TmIgnECN","TmWaitECN","EnUpECN",
               "ManualSpeed","CollarSpeed","CollarDepth","res1","res2","HLimService","LimPlugUp","LimPlugDown","TmWaitDatPro","DeltaTmWaitDatPro","TmWaitDatZak","Overload",
               "TmOverload","TmWaitAlarmDat","TmWaitEM","res3","res4","res5","Pot485","BitDat485","PowINV485","ControlWord_v5","SpeedINV_v5","BitMask_v5","AcrDT1","AcrDT2",
               "ArcDT3","AcrStatus","ArcDepth","ArcPower","ArcAI2","ArcStringStatus","Username1","Username2","DistControl","Verion"]
        v9024=["DT1","DT2","DT3","Status_v9","Depth","Power","AI2","StringStatus","Status_v5","TimeBeforeStart","Depth2","Speed","Power2","NSucYes","NSucTod","NSucTot",
               "NWires","WorkDepth","WorkSpeed","TmClearDelta","TmClearAbs","TmWaitWorkDepth","TmWaitLubr","DepthClearUst","TmClearUst","TmIgnECN","TmWaitECN","EnUpECN",
               "ManualSpeed","CollarSpeed","CollarDepth","res1","res2","HLimService","LimPlugUp","LimPlugDown","TmWaitDatPro","DeltaTmWaitDatPro","TmWaitDatZak","Overload",
               "TmOverload","TmDpS1","TmDpS2","TmDpS3","TmDpS4","TmDelayDay","Pot485","BitDat485","PowINV485","ControlWord_v5","SpeedINV_v5","BitMask_v5","AcrDT1","AcrDT2",
               "ArcDT3","AcrStatus","ArcDepth","ArcPower","ArcAI2","ArcStringStatus","Username1","Username2","DistControl","Verion"]
        if resp.registers[63]<9024:
            dict_ver=v9012
        if resp.registers[63]>=9024:
            dict_ver=v9024
        i=0
        dict_resp={}
        for name in dict_ver:
            dict_resp[name]=resp.registers[i]
            i+=1
        return dict_resp
        
    def WriteTimeLog(self,dr):
        date_local=datetime.today().strftime("%Y.%m.%d")
        time_local=datetime.today().strftime("%H:%M:%S")
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""INSERT INTO LOG_TIME (id_device, date_local, time_local, status, depth, power) VALUES ('"""+str(self.id_device)+"""', '"""+str(date_local)+"""', 
                           '"""+str(time_local)+"""', """+str(dr["Status_v9"])+""", """+str(dr["Depth"])+""", """+str(dr["Power"])+""")""")
            con.commit()
            cursor.close()
        
    def WriteEventLog(self,dr):
        if self.adt1 != dr["AcrDT1"] or self.adt2 != dr["AcrDT2"] or self.adt3 != dr["ArcDT3"]:
            date_local=datetime.today().strftime("%Y-%m-%d")
            time_local=datetime.today().strftime("%H:%M:%S")
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""INSERT INTO LOG_EVENT (id_device, date_local, time_local, status, depth, power) VALUES ('"""+str(self.id_device)+"""', '"""+str(date_local)+"""', 
                            '"""+str(time_local)+"""', """+str(dr["AcrStatus"])+""", """+str(dr["ArcDepth"])+""", """+str(dr["ArcPower"])+""")""")
                con.commit()
                cursor.close()
            self.adt1=dr["AcrDT1"]
            self.adt2=dr["AcrDT2"]
            self.adt3=dr["ArcDT3"]
            
    def Thread(self):
        self.client = modbusClient.ModbusSerialClient(port="COM3",framer=Framer.RTU,baudrate=9600,timeout=1,bytesize=8,parity="N",stopbits=1,strict=False)
        self.client.connect()
        while self.enable:
            rr=self.Request1()
            print(rr)
            if not rr.isError():  
                dr=self.CheckVersion(rr)
                self.WriteTimeLog(dr)
                self.WriteEventLog(dr)
            time.sleep(1)
        self.client.close()
        
        
#D=Device("123")     
#D.Start()
#time.sleep(10)
#D.Stop()
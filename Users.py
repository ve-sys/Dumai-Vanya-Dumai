import sqlite3
import Data.date as dd
databasename=dd.databasename
baseUser=[0,0,"",False,"",0]
class User:
    def __init__(self, ID:int, prfl=0, name="",status=False, mes="",cash=0):# Метод инициализации
        self.ID = ID
        self.prfl = prfl
        self.status = status
        self.name = name
        self.mes = mes
        self.cash = cash
    def add(self,FULLEDIT=True,Show=False):
        db = sqlite3.connect(databasename)
        cursor = db.cursor()
        if not (self.exists()):
            cursor.execute("INSERT INTO user(uid,prfl,status,name,mess,cash) VALUES(?,?,?,?,?,?)", (self.ID,self.prfl,self.status,self.name,self.mes,self.cash))
        else:
            if FULLEDIT:
                cursor.execute(f'UPDATE user SET prfl = ?,status = ?,name = ?,mess = ?,cash = ? WHERE uid= ?',(self.prfl, self.status, self.name, self.mes, self.cash, self.ID))
            else:
                data=cursor.execute(f"SELECT prfl,status,name,mess,cash FROM user WHERE uid = ?", (self.ID,)).fetchall()
                if Show:print(data)
                sl=self.list()
                #print(sl)
                global baseUser
                coulm=["prfl","status","name","mess","cash"]
                ADD=[[sl[x],coulm[x]] for x in range(len(data)) if data[x]!=sl[x] and sl[x]!=baseUser[x]]
                [cursor.execute(f'UPDATE user SET {i[1]} = ? WHERE uid= ?',(i[0],self.ID)) for i in ADD]
                if Show:print(ADD)
        db.commit()
    def __str__(self) -> str:
        return f"<ID:{self.ID};ProfilID:{self.prfl};status:{self.status};name:{self.name};messanger:'{self.mes}';cash:'{self.cash}'>"
    def list(self):
        return [self.prfl,self.status,self.name,self.mes,self.cash]
    def exists(self):
        db = sqlite3.connect(databasename)
        cursor = db.cursor()
        reg=cursor.execute(f"SELECT uid FROM user WHERE uid = ?",(self.ID,))
        return bool(len(reg.fetchall()))
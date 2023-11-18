import sqlite3
import numpy as np
import Data.date as dd
databasename=dd.databasename
class tema:
    def __init__(self,Name:str,Author=[],prfl=0,Decisive=[],follower=[],Description=[],Viewers=[]):
        self.Name=Name
        self.Author=Author
        self.prfl=prfl
        self.follower=follower
        self.Decisive=Decisive
        self.Description=Description
        self.Viewers=Viewers
    def __str__(self) -> str:
        return f"<Name:{self.Name};ProfilID:{self.prfl};Author:{self.Author};Decisive:{self.Decisive};follower:'{self.follower}';Description:'{self.Description}';Viewers:'{self.Viewers}'>"
    def exist(self):
        db = sqlite3.connect(databasename)
        cursor = db.cursor()
        reg = cursor.execute(f"SELECT tema FROM main WHERE tema = ?", (self.Name,))
        return bool(len(reg.fetchall()))
    def add(self,show=False,remove=False):
        db = sqlite3.connect(databasename)
        cursor = db.cursor()
        coulm = ["auth", "foll", "dec", "dis", "viewer"]
        if remove:
            if self.exist():
                iN = [self.Author, self.follower, self.Decisive, self.Description, self.Viewers]
                lastdata = np.array(
                    cursor.execute("SELECT auth,foll,dec,dis,viewer FROM reg WHERE tema = ?", (self.Name,)).fetchall()
                )
                ratio = lastdata.transpose()
                Out = sorted(
                    [[set(iN[x])&set(filter(lambda x: (x != None), ratio[x])), coulm[x]] for x in range(len(ratio))],key=lambda x: (-len(x[0]))
                )
                if show: print(Out,lastdata)#print(ratio, Out)
                for i in Out:
                    a = list(i[0])
                    Coulm = i[1]
                    Y = int(cursor.execute(f"SELECT {coulm} FROM main WHERE tema = ?", (self.Name,)).fetchone()[0])-len(a)
                    cursor.execute(f"UPDATE main SET {coulm} = ? WHERE tema = ?", (Y, self.Name))
                    if show: print(a, Coulm, cursor.execute(f"SELECT * FROM main WHERE tema = ?", (self.Name,)).fetchone())
                    for x in a:
                        Ncoulm = list(set([Coulm]) ^ set(coulm))
                        cursor.execute(f"UPDATE reg SET {Coulm} = NULL WHERE tema = ? AND {Coulm} = ?",(self.Name,x))
                        if show: print(Ncoulm, x)
                cursor.execute(f"DELETE FROM reg WHERE tema = ? AND ({coulm[0]} IS NULL) AND ({coulm[1]} IS NULL) AND ({coulm[2]} IS NULL) AND ({coulm[3]} IS NULL) AND ({coulm[4]} IS NULL)", (self.Name,))
                db.commit()
        else:
            if not (self.exist()):
                cursor.execute("INSERT INTO main(tema,prfl,auth,foll,viewer,dis,dec) VALUES(?,?,?,?,?,?,?)",
                               (self.Name, self.prfl, len(self.Author), len(self.follower), len(self.Viewers), len(set(self.Description)),len(set(self.Decisive))))
                mx = max([len(set(self.Author)), len(set(self.Decisive)), len(set(self.follower)),
                          len(set(self.Description)), len(set(self.Viewers))])
                ADD = np.array([
                    [self.Name] * mx,
                    list(set(self.Author)) + [None] * (mx - len(set(self.Author))),
                    list(set(self.follower)) + [None] * (mx - len(set(self.follower))),
                    list(set(self.Decisive)) + [None] * (mx - len(set(self.Decisive))),
                    self.Description + [None] * (mx - len(self.Description)),
                    list(set(self.Viewers)) + [None] * (mx - len(set(self.Viewers)))
                ]).transpose()
                if show: print("if" + str(ADD.transpose()))
                [cursor.execute("INSERT INTO reg(tema,auth,foll,dec,dis,viewer) VALUES(?,?,?,?,?,?)", list(x)) for x in ADD]
                db.commit()
            else:
                iN = [self.Author, self.follower, self.Decisive, self.Description, self.Viewers]
                lastdata = np.array(
                    cursor.execute("SELECT auth,foll,dec,dis,viewer FROM reg WHERE tema = ?", (self.Name,)).fetchall())
                ratio = lastdata.transpose()
                Out = sorted(
                    [[set(iN[x]) - set(filter(lambda x: (x != None), ratio[x])), coulm[x]] for x in range(len(ratio))],
                    key=lambda x: (-len(x[0])))
                if show: print(lastdata, Out)
                for i in Out:
                    a = list(i[0])
                    coulm = i[1]
                    Y=int(cursor.execute(f"SELECT {coulm} FROM main WHERE tema = ?", (self.Name,)).fetchone()[0])+len(a)
                    cursor.execute(f"UPDATE main SET {coulm} = ? WHERE tema = ?", (Y, self.Name))
                    if show: print(a, coulm,cursor.execute(f"SELECT * FROM main WHERE tema = ?", (self.Name,)).fetchone())
                    for x in a:
                        if len(cursor.execute(f"SELECT * FROM reg WHERE tema = ? AND {coulm} IS NULL",
                                              (self.Name,)).fetchall()) > 0:
                            minID = min(cursor.execute(f"SELECT ID FROM reg WHERE tema = ? AND {coulm} IS NULL",
                                                       (self.Name,)).fetchall(), key=lambda x: (x[0]))[0]
                            cursor.execute(f"UPDATE reg SET {coulm} = ? WHERE ID = ? AND {coulm} IS NULL", (x, minID))
                        else:
                            cursor.execute(f"INSERT INTO reg(tema,{coulm}) VALUES (?,?)", (self.Name, x))
                    db.commit()
        cursor.close()
        db.close()
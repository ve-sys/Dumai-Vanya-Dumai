import sqlite3
import numpy as np
import Data.date as dd
databasename=dd.databasename
from Data.Users import User
from Data.Tema import tema
with sqlite3.connect(databasename) as db:
    cursor= db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS main(tema TEXT,prfl TINYINT,auth INTEGER,foll INTEGER,viewer INTEGER,dec INTEGER, dis INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS reg(ID INTEGER PRIMARY KEY,tema TEXT,auth BIGINT,foll BIGINT,dec BIGINT,dis TEXT,viewer BIGINT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user(uid BIGINT,prfl TINYINT,status BOOL,name TEXT,mess CHAR,cash TINYINT)")
def getuser(ID:int):
    db = sqlite3.connect(databasename)
    cursor = db.cursor()
    reg = cursor.execute(f"SELECT uid,prfl,status,name,mess,cash FROM user WHERE uid = ?", (ID,)).fetchone()
    Usr=User(reg[0],reg[1],reg[3],bool(reg[2]),reg[4],reg[5])
    return Usr
def gettema(Name:str):
    db = sqlite3.connect(databasename)
    cursor = db.cursor()
    Out=tema(Name)
    Out.prfl=cursor.execute(f"SELECT prfl FROM main WHERE tema = ?", (Name,)).fetchone()[0]
    ratio = np.array(cursor.execute("SELECT auth,foll,dec,dis,viewer FROM reg WHERE tema = ?", (Name,)).fetchall()).transpose()
    Out.Author = list(filter(lambda x :(x!=None), ratio[0]))
    Out.follower = list(filter(lambda x :(x!=None), ratio[1]))
    Out.Decisive = list(filter(lambda x: (x != None), ratio[2]))
    Out.Description = list(filter(lambda x: (x != None), ratio[3]))
    Out.Viewers = list(filter(lambda x: (x != None), ratio[4]))
    return Out
def gettemes(ID:int):
    user=getuser(ID)
    View=cursor.execute("""
    SELECT MIN(viewer) FROM main 
    WHERE NOT (? IN (SELECT viewer FROM reg WHERE tema = main.tema)) AND prfl = ?
    """, (user.ID,user.prfl)).fetchone()[0]
    Auth=cursor.execute("""
    SELECT MAX(auth) FROM main WHERE 
    NOT (? IN (SELECT viewer FROM reg WHERE tema = main.tema)) AND prfl = ?  AND viewer = ?
    """, (user.ID,user.prfl,View))
    Dec=cursor.execute("""
    SELECT MIN(dec) FROM main WHERE 
    NOT (? IN (SELECT viewer FROM reg WHERE tema = main.tema)) AND prfl = ?  AND viewer = ? AND auth = ?
    """, (user.ID,user.prfl,View,Auth))
    temes=cursor.execute("""
    SELECT tema FROM main WHERE
    NOT (? IN (SELECT viewer FROM reg WHERE tema = main.tema)) AND prfl = ?  AND viewer = ? AND auth = ? AND dec = ?
    """, (user.ID,user.prfl,View,Auth,Dec)).fetchall()
    return temes
def getUserTemes(ID):
    Author=cursor.execute("""
    SELECT tema FROM reg WHERE auth = ?
    """,(ID,))
    follower=cursor.execute("""
    SELECT tema FROM reg WHERE foll = ?
    """,(ID,))
    dec=cursor.execute("""
    SELECT tema FROM reg WHERE dec = ?
    """,(ID,))
    return [Author,follower,dec]






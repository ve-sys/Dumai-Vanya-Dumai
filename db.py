import sqlite3

class BotDB:


    def __init__(self, db_file):

        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    # Инициализация соединения с БД

    def user_exists(self, user_id):
        
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ? ", (user_id,))
        return bool(len(result.fetchall()))
    # Проверка на наличие челика в БД

    def get_user_id(self, user_id):

        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result.fetchone()[0]
    # Получение id челика по его id в тг

    def add_user(self, user_id):

        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()
    # Добавление челика в БД

    def add_record(self, user_id, operation, favourite):

        self.cursor.execute("INSERT INTO 'Records' ('user_id', 'operation', 'favourite') VALUES (? , ? , ?)",
            (self.get_user_id(user_id),
             operation == '+',
             favourite))
        return self.conn.commit() 

    def delete_record(self, user_id,):
       
        result = self.cursor.execute("DELETE FROM 'Records' WHERE 'favourite' = ?", (user_id,))
        return self.conn.commit()


    def add_tema(self, user_id, operation, Tema):

        self.cursor.execute("INSERT INTO 'Tems' ('user_id', 'operation', 'Tema') VALUES (? , ? , ?)",
            (self.get_user_id(user_id),
             operation == '+',
             Tema))
        return self.conn.commit()    

    def add_profile(self, user_id, operation, Profile):

        self.cursor.execute("INSERT INTO 'Tems' ('user_id', 'operation', 'Profile') VALUES (? , ? , ?)",
            (self.get_user_id(user_id),
             operation == '+',
             Profile))
        return self.conn.commit() 
    

    def add_record(self, user_id, operation, Tema):

        self.cursor.execute("INSERT INTO 'Tems' ('user_id', 'operation', 'Tema') VALUES (? , ? , ?)",
            (self.get_user_id(user_id),
             operation == '+',
             Tema))
        return self.conn.commit()
    
    def get_records (self, user_id, within = "+"):

        if(within == 'day'):

            result = self.cursor.execute("SELECT * FROM 'Tems' WHERE 'user_id' = ?  AND 'date' BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))
            
        elif(within == 'month'):

            result = self.cursor.execute("SELECT * FROM 'Tems' WHERE 'user_id' = ?  AND 'date' BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))
        
        elif(within == 'month'):

            result = self.cursor.execute("SELECT * FROM 'Tems' WHERE 'user_id' = ?  AND 'date' BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))
            
        else:

            result = self.cursor.execute("SELECT * FROM 'Tems' WHERE 'user_id' = ? ORDER BY 'date'",
                self.get_user_id(user_id))
          
        return result.fetchall()




    def close(self):
        self.conn.close()
    # Закрытие БД



        
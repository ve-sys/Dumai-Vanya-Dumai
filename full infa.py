import sqlite3
databasename="User_data.db"



def infa_full(msg,flw,view,avtor,user_id):
    
    db = sqlite3.connect(databasename)
    cursor = db.cursor()

    tm = msg.replace('!просмотреть информацию','',1)

    cursor.execute(f"SELECT tema FROM theme WHERE tema=='{tm}'")

                                 # проверка на наличие темы
    if not(cursor.fetchone() is None):
    

                                 # подсчёт кол-во просмотров
        view = cursor.execute(f"SELECT view FROM theme WHERE tema=='{tm}'").fetchone()

        if not(view is None):
            
            view = cursor.execute(f"SELECT view FROM theme WHERE tema=='{tm}'").fetchone()

            return('Общее кол-во просмотров:',int(view))
        
        elif view is None:
            return('Эта тема ещё никому не попалась')
        
        
                                 # подсчёт кол-ва фолловеров данной темы 
        flw = cursor.execute(f"SELECT followers FROM theme WHERE tema=='{tm}'").fetchone()
                                # Проверка на наличие фолловеров
        if not(flw is None):
        
            cursor.execute(f"SELECT COUNT followers FROM theme WHERE tema=='{tm}'" )
            total_users = cursor.fetchone()[0]
        
            return('Общее кол-во фолловеров:', total_users)
        
        elif flw is None:
            return "У этой темы нет фолловеров "
        
        
        
        avtor = cursor.execute(f"SELECT authors FROM theme WHERE tema=='{tm}'").fetchone()
        Avtors = cursor.execute(f"SELECT authors FROM theme WHERE tema=='{tm}'")
        Avtors = cursor.fetchall
        
        if not(avtor is None) and f'<@{user_id}>' in avtor:

            
                                    # вывод списка авторов данной темы
            Avtors_list = []
            for avtor in Avtors:
                avtor_dict = {
                    'avtorname': avtor[0]
                }
            Avtors_list.append(avtor_dict)


            for avtor in Avtors_list:
                return ('Авторы темы:',avtor)
 

        
        
        
    else:
        return "Тема не найдена, информации нет"
    

    db.close()
    cursor.close()



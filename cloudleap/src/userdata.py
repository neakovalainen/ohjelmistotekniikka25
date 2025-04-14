from sql_connect import get_database_connection
from sql_queries import initialize_database
class UserData:
    def __init__(self, connection):
        self._connection = connection

    def save_username(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            INSERT INTO Users (username)
            VALUES (:username)          
            ''', {"username":username})
        
        self._connection.commit()
    
    def get_all_scores(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT *
            FROM    Scores
            ''')
        
        rows = cursor.fetchall()
        print(rows)
        return []
    
    def get_all_users(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT *
            FROM    Users
            ''')
        
        rows = cursor.fetchall()
        return list(rows)
    
 #initialize_database()
    
#userdata = UserData(get_database_connection())
#userdata.save_username("jeje")
#userdata.get_all_users()
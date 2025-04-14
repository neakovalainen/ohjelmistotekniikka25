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

    def get_username(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT username
            FROM Users
            WHERE username = :username
            ''', {"username":username})

        user = cursor.fetchone()
        return list(user)[1]

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

    def delete_user(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM Users
            WHERE username = :username
            ''', {"username":username})

        self._connection.commit()

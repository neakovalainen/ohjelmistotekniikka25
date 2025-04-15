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

    def update_score(self, best_score, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            INSERT INTO Scores (best_score, username)
            VALUES  (:best_score, :username)
            ON CONFLICT(username) DO UPDATE SET
            best_score = EXCLUDED.best_score
            ''', {"best_score":best_score, "username":username})

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

    def get_score(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT best_score
            FROM    Scores
            WHERE username = :username
            ''', {"username":username})

        score = cursor.fetchone()
        if score:
            return list(score)[0]
        return -2 #score cannot be -2 so if score = None return this (easier to compare in index.py)


    def get_all_scores(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT *
            FROM Scores
            ORDER BY best_score DESC
            LIMIT 5
            ''')

        rows = cursor.fetchall()
        return list(rows)

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

    def delete_score(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM Scores
            WHERE username = :username
            ''', {"username":username})

        self._connection.commit()

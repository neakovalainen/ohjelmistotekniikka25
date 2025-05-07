class UserData:
    """
        Luokka, joka hoitaa käyttäjään liittyvien
        sql komentojen suorittamisen
    """
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
        """
            Käyttäjän tulos tallennetaan, jos käyttäjälle on jo olemassa
            vanhempi tulos, se korvataan uudella parhaalla, jos ei
            luodaan uusi

            Args:
                best_score: käyttäjän paras tulos, joka tallennetaan
                username: käyttäjä kenelle tulos kuuluu
        """
        cursor = self._connection.cursor()

        cursor.execute('''
            INSERT INTO Scores (best_score, username)
            VALUES  (:best_score, :username)
            ON CONFLICT(username) DO UPDATE SET
            best_score = EXCLUDED.best_score
            ''', {"best_score":best_score, "username":username})

        self._connection.commit()

    def get_username(self, username):
        """
            Metodi, jonka avulla tarkastetaan onko käyttäjää jo olemassa

            Args:
                username: käyttäjä, jonka olemassa olo halutaan varmistaa
        """
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT username
            FROM Users
            WHERE username = :username
            ''', {"username":username})

        user = cursor.fetchone()
        return list(user)[0] if user else False

    def get_score(self, username):
        """
            Palauttaa käyttäjän parhaan tuloksen

            Args:
                username: käyttäjä, jonka tulos halutaan palauttaa
        """
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT best_score
            FROM    Scores
            WHERE username = :username
            ''', {"username":username})

        score = cursor.fetchone()
        if score:
            return list(score)[0]
        return -2 #score cannot be -2 so if score = None return this (easy to compare)


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
        return [row['username'] for row in rows]

    def delete_user(self, username):
        """
            Metodia kutsutaan, jos käyttäjä haluaa poistaa käyttäjänsä

            Args:
                username: poistettava käyttäjä
        """
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

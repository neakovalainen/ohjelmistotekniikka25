from sql_connect import get_database_connection

def delete_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS Users;
    ''')

    cursor.execute('''
        DROP TABLE IF EXISTS Scores;
    ''')


    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE Users (
        id  SERIAL PRIMARY KEY,
        username    TEXT UNIQUE
        );
    ''')

    cursor.execute('''
        CREATE TABLE Scores (
            id  SERIAL PRIMARY KEY,
            best_score  INTEGER,
            username    TEXT,

            UNIQUE(username),
            FOREIGN KEY (username) REFERENCES Users(username)
                ON DELETE CASCADE
        );
    ''')

    connection.commit()

def initialize_database():
    connection = get_database_connection()

    delete_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()

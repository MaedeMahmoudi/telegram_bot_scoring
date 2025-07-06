import sqlite3

# connect to db
connection = sqlite3.connect('scores.db')
cursor = connection.cursor()

# create table if there weren't
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            score INTEGER
        ) 
    ''')
    connection.commit()
    

# add score
def add_score(user_id, user_name, points):
    cursor.execute('SELECT score FROM scores WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
         new_score = row[0] + points
         cursor.execute('UPDATE scores SET score = ?, user_name = ? WHERE user_id = ?', 
                       (new_score, user_name, user_id))
    else:
        new_score = points
        cursor.execute('INSERT INTO scores (user_id, user_name, score) VALUES (?, ?, ?)', 
                      (user_id, user_name, new_score))
    connection.commit()
    return new_score


# get score
def get_score(user_id):
    cursor.execute('SELECT score FROM scores WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        return row[0]
    return 0

# exit from db
def close_db():
     connection.close()


# init execute
init_db()
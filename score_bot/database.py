import sqlite3

# connect to db
connection = sqlite3.connect('scores.db')
cursor = connection.cursor()

def init_db():
    # create db if it wasn't
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            score INTEGER
        )
    ''')
    connection.commit()

    # score
    cursor.execute("PRAGMA table_info(scores)")
    columns = cursor.fetchall()

    # add score if it wasn't
    column_names = [col[1] for col in columns]
    if 'score' not in column_names:
        cursor.execute("ALTER TABLE scores ADD COLUMN score INTEGER")
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

#get score
def get_score(user_id):
    cursor.execute('SELECT score FROM scores WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        return row[0]
    return 0

#exit db
def close_db():
    connection.close()


init_db()

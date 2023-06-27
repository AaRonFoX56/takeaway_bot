import sqlite3


connection = sqlite3.connect('app.db')
cursor = connection.cursor()

#cursor.execute('CREATE TABLE app (id INTEGER PRIMARY KEY, name VARCHAR(64), phone VARCHAR(64))')
#connection.commit()


def create_user_with_name_and_tg_id(name, tg_id, message):
    cursor.execute('SELECT id FROM app WHERE id=?', (message.chat.id,))
    user = cursor.fetchone()
    cursor.execute('UPDATE app SET name=? WHERE id=?', (message.text, message.chat.id,))
    connection.commit()
    if not user:
        cursor.execute('INSERT INTO app VALUES(?, ?, ?)', (message.chat.id, message.text, 'phone'))
        connection.commit()
    else:
        pass


def add_user_phone(contact, user_id):
    cursor.execute('UPDATE app SET phone=? WHERE id=?', (contact.phone_number, user_id))
    connection.commit()
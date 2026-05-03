import sqlite3
conn = sqlite3.connect('smartstay.db')
cur = conn.cursor()
cur.execute('SELECT id, email, role FROM users')
users = cur.fetchall()
print('Users:')
for user in users:
    print(user)
conn.close()
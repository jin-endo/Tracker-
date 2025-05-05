
import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("✅ Tables in database:")
for table in tables:
    print(table[0])

cursor.execute("SELECT id, email FROM user;")
users = cursor.fetchall()
print("✅ Registered users:")
for user in users:
    print(user)

conn.close()

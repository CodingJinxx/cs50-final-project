import sqlite3

__DATABASE__ = "nonogram.db"

def InitDatabase():
    db = sqlite3.connect(__DATABASE__)
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS "users"''')
    cursor.execute('''DROP TABLE IF EXISTS "stats"''')
    cursor.execute('''CREATE TABLE "users" 
    (
	"id"	INTEGER UNIQUE PRIMARY KEY NOT NULL,
	"username"	VARCHAR(64) NOT NULL UNIQUE,
	"passwordhash"	VARCHAR(128) NOT NULL
    );
    ''')
    cursor.execute('''CREATE TABLE "stats"
    (
    "id"   INTEGER UNIQUE PRIMARY KEY NOT NULL,
    "starsCollected" INTEGER NOT NULL DEFAULT 0
    );''')

def AddUser(Username, PasswordHash):
    db = sqlite3.connect(__DATABASE__)
    cursor = db.cursor()

    
import sqlite3

def run():
  con = sqlite3.connect("hotel.db")
  print("Connected to database successfully!")
  
  con.execute('''CREATE TABLE IF NOT EXISTS guests (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  bookingnr INTEGER,
                  First_name TEXT,
                  Last_name TEXT,
                  email TEXT,
                  phonenumber TEXT,
                  room_type TEXT,
                  check_in_date TEXT,
                  check_out_date TEXT,
                  room_id INTEGER,
                  FOREIGN KEY(room_id) REFERENCES rooms(id)
                  )''')
  print("Created table successfully!")

  con.execute('''CREATE TABLE IF NOT EXISTS rooms (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  room_nr INTEGER,
                  room_type TEXT,
                  price INTEGER,
                  status TEXT
                  )''')
  print("Created table successfully!")

  con.close()
  
import sqlite3


single = {"room_nr": 100, "room_type": "single", "price": 100, "status": "vacant"}
double = {"room_nr": 200, "room_type": "double", "price": 150, "status": "vacant"}
suite = {"room_nr": 300, "room_type": "suite", "price": 200, "status": "vacant"}

def run():
  with sqlite3.connect("hotel.db") as con:
    for i in range(6):
      single["room_nr"] += i
      cur = con.cursor()
      cur.execute("INSERT INTO rooms (room_nr, room_type, price, status) VALUES (?, ?, ?, ?)", (single["room_nr"], single["room_type"], single["price"], single["status"]))
      con.commit()
    print(str(i+1) + " single rooms added")

    for i in range(6):
      double["room_nr"] += i
      cur = con.cursor()
      cur.execute("INSERT INTO rooms (room_nr, room_type, price, status) VALUES (?, ?, ?, ?)", (double["room_nr"], double["room_type"], double["price"], double["status"]))
      con.commit()
    print(str(i+1) + " double rooms added")

    for i in range(6):
      suite["room_nr"] += i
      cur = con.cursor()
      cur.execute("INSERT INTO rooms (room_nr, room_type, price, status) VALUES (?, ?, ?, ?)", (suite["room_nr"], suite["room_type"], suite["price"], suite["status"]))
      con.commit()
    print(str(i+1) + " suites added")

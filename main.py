from flask import Flask, redirect, render_template, request
import sqlite3
import ourSQL
import create_rooms
import random
from datetime import datetime


app = Flask(__name__)

guests = [
    {"bookingnr": 1000, "fname": "Peter", "lname": "Alderete", "email": "PA@gmail.com", "phonenumber": 111},
    {"bookingnr": 1001, "fname": "Arin", "lname": "Minasian", "email": "AN@gmail.com", "phonenumber": 222},
    {"bookingnr": 1002, "fname": "Andreas", "lname": "Liljedahl", "email": "AL@gmail.com", "phonenumber": 333},
    {"bookingnr": 1003, "fname": "Jimmy", "lname": "Berlin", "email": "JB@gmail.com", "phonenumber": 444},
    {"bookingnr": 1004, "fname": "Dwayne", "lname": "Johnson", "email": "DJ@gmail.com", "phonenumber": 555},
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/remove', methods=["POST"])
def remove():
    id = request.form["id"]

    with sqlite3.connect("hotel.db") as con:
        cur = con.cursor()
        
        cur.execute("SELECT room_id FROM guests WHERE id=?", (id,))
        room_id = cur.fetchone()[0]

        cur.execute("UPDATE rooms SET status='vacant' WHERE id=?", (room_id,))
        
        cur.execute("DELETE FROM guests WHERE id=?", (id,))

        con.commit()
        print("Successfully removed guest")
        
        if request.referrer.endswith('/customerlogin'):
            return redirect('/cancelbooking')    

    return redirect('/admindashboard')


@app.route('/admindashboard', methods=["GET", "POST"])
def admindashboard():
    if request.method == "GET":
        con = sqlite3.connect("hotel.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT rowid, * FROM rooms")
        rooms_data = cur.fetchall()
        con.close()

        con = sqlite3.connect("hotel.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT rowid, * FROM guests")
        guests_data = cur.fetchall()
        con.close()

        return render_template("admindashboard.html", guests_data=guests_data, rooms_data=rooms_data)


@app.route('/add_rooms', methods=["GET", "POST"])
def add_rooms():
    if request.method == "POST":
        room_nr = request.form["room_nr"]
        room_type = request.form["room_type"]
        price = request.form["price"]

        with sqlite3.connect("hotel.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO rooms (room_nr, room_type, price, status) VALUES (?, ?, ?, ?)",
                        (room_nr, room_type, price, "vacant"))
            con.commit()
            print("Room added successfully!")

        return redirect('/admindashboard')

    return render_template("add_rooms.html")

@app.route('/add', methods=["POST"])
def add():
    bookingnr = random.randint(1000, 2001)  # TODO If bookingnr exists, roll again
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    phonenumber = request.form["phonenumber"]
    room_type = request.form["room"]
    check_in_date_str = request.form["check_in_date"]
    check_out_date_str = request.form["check_out_date"]

    check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d").date()
    check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d").date()

    with sqlite3.connect("hotel.db") as con:
        cur = con.cursor()
        
        cur.execute("SELECT id FROM rooms WHERE room_type=? AND status='vacant'", (room_type,))
        available_rooms = cur.fetchall()

        if available_rooms:
          room_id = random.choice(available_rooms)[0]
          cur.execute("INSERT INTO guests (bookingnr, First_name, Last_name, email, phonenumber, room_type, check_in_date, check_out_date, room_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (bookingnr, fname, lname, email, phonenumber, room_type, check_in_date, check_out_date, room_id))
          
          cur.execute("UPDATE rooms SET status='occupied' WHERE id=?", (room_id,))

          con.commit()

          confirmation_letter = f"Dear {fname} {lname},\n\nYour booking has been confirmed.\nBooking Number: {bookingnr}\nCheck-in Date: {check_in_date}\nCheck-out Date: {check_out_date}\n\nThank you for choosing our hotel."
          return render_template("confirmation.html", bookingnr=bookingnr, fname=fname, lname=lname, email=email, phonenumber=phonenumber, room_type=room_type, check_in_date=check_in_date, check_out_date=check_out_date, confirmation_letter=confirmation_letter)
          print("Booking made successfully!")
        else:
          print("No available rooms")
    return redirect('/booking')

@app.route('/info')
def info():
    guest_index = int(request.args["guest"])
    return render_template("guest_info.html", 
                           fname = guests[guest_index]["fname"], 
                           lname = guests[guest_index]["lname"],
                           email = guests[guest_index]["email"],
                           phonenumber = guests[guest_index]["phonenumber"],
                           room_type = guests[guest_index]["room_type"])

@app.route('/booking')
def booking():
    return render_template("booking.html")

@app.route('/booknow')
def booknow():
    con = sqlite3.connect("hotel.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM rooms")

    rows = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM rooms WHERE room_type='single' AND status='vacant'")
    single_rooms_available = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM rooms WHERE room_type='double' AND status='vacant'")
    double_rooms_available = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM rooms WHERE room_type='suite' AND status='vacant'")
    suites_available = cur.fetchone()[0]

    con.close()

    return render_template("booknow.html", rows=rows, single_rooms_available=single_rooms_available, double_rooms_available=double_rooms_available, suites_available=suites_available)


@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    username = request.form.get("username")
    password = request.form.get("password")
        
    if username == "qwe" and password == "qwe":

        con = sqlite3.connect("hotel.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT rowid, * FROM guests")
        guests_data = cur.fetchall()

        cur.execute("SELECT rowid, * FROM rooms")
        rooms_data = cur.fetchall()

        con.close()

        return render_template("admindashboard.html", guests_data=guests_data, rooms_data=rooms_data)
    else:
        error_message_admin = "Invalid username or password"
        return render_template("login.html", error_message_admin=error_message_admin)

@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    error_message = None
    
    if request.method == 'POST':
        email = request.form['email']
        bookingnr = request.form['bookingnr']
        
        with sqlite3.connect("hotel.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM guests WHERE email = ? AND bookingnr = ?", (email, bookingnr))
            customer = cursor.fetchone()
            
            if customer:
                return render_template("customerlogin.html", customer=customer)
            else:
                error_message = "Invalid email or booking number. Please try again."
    
    return render_template("login.html", error_message=error_message)

@app.route('/cancelbooking')
def cancelbooking():
    return render_template("cancelbooking.html")

@app.route('/contacts')
def contacts():
    return render_template("contacts.html")

@app.route('/foodanddrinks')
def foodanddrinks():
    return render_template("foodanddrinks.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/spa')
def spa():
    return render_template("spa.html")


if __name__ == '__main__':
    ourSQL.run()
    #create_rooms.run()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
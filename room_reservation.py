from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql


# ---------------------------------------------------------------Login Function --------------------------------------
def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)


def close():
    win.destroy()


def login():
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror(
            "Error", "Enter User Name And Password", parent=win)
    else:
        try:
            con = pymysql.connect(host="localhost", user="root",
                                  password="new_password", database="room_reservation")
            cur = con.cursor()

            cur.execute("select * from users where username=%s and password = %s",
                        (user_name.get(), password.get()))
            row = cur.fetchone()
            user_id = row[2]
            if row == None:
                messagebox.showerror(
                    "Error", "Invalid User Name And Password", parent=win)

            else:
                messagebox.showinfo(
                    "Success", "Successfully Logged in", parent=win)
                close()
                dashboard()

            con.close()
        except Exception as es:
            messagebox.showerror(
                "Error", f"Error Dui to : {str(es)}", parent=win)

# ---------------------------------------------------------------End Login Function ---------------------------------

# ---------------------------------------------------- DashBoard Panel -----------------------------------------


def dashboard():

    def book():
        if room_var.get() == "" or semester_var.get() == "" or year.get() == "":
            messagebox.showerror(
                "Error", "All Fields Are Required", parent=des)

        else:
            con = pymysql.connect(host="localhost", user="root",
                                  password="new_password", database="room_reservation")
            cur = con.cursor()
            cur.execute(
                "select sum(room_no) from reservation_requests where room_no=%s", (Room_box.get()))
            row = cur.fetchone()
            print(row[0])
            if (row[0] == None or row[0] > 4):
                cur.execute("insert into reservation_requests(room_no,semester,year,user_student_id,approval_status) VALUES(%s,%s,%s,%s,%s)", (
                    Room_box.get(), semester_box.get(), Year.get(), 1, 0))
                con.commit()
                con.close()
                messagebox.showinfo(
                    "Success", "Booked Room, awaiting approval ", parent=des)
            else:
                messagebox.showinfo(
                    "Success", "Selected room is fully booked,Please select another room", parent=des)

    des = Tk()
    des.title("Room reservation panel")
    des.maxsize(width=800,  height=500)
    des.minsize(width=800,  height=500)

    # heading label
    heading = Label(
        des, text=f"User Name : {user_name.get()}", font='Verdana 20 bold', bg='green')
    heading.place(x=220, y=50)

    f = Frame(des, height=1, width=800, bg="green")
    f.place(x=0, y=95)

    con = pymysql.connect(host="localhost", user="root",
                          password="new_password", database="room_reservation")
    cur = con.cursor()

    cur.execute("select * from users u left join reservation_requests r on u.id=r.user_student_id where username ='" + user_name.get() + "'")
    row1 = cur.fetchall()
    a = Frame(des, height=1, width=400, bg="green")
    a.place(x=0, y=195)

    b = Frame(des, height=100, width=1, bg="green")
    b.place(x=400, y=97)

    for data in row1:
        user = Label(des, text=f"ID : {data[1]}", font='Verdana 10 bold')
        user.place(x=20, y=100)

        userid = Label(des, text=f"Name : {data[4]}", font='Verdana 10 bold')
        userid.place(x=20, y=130)

    # Book Docter Appointment App
    cur.execute("select * from users u inner join reservation_requests r on u.id=r.user_student_id where username ='" + user_name.get() + "'")
    row2 = cur.fetchone()
    print(row2)

    if (row2 == None or row2[6] == 2):

        heading = Label(des, text="Book a room", font='Verdana 20 bold')
        heading.place(x=420, y=100)

        # Book DocterLabel
        Room = Label(des, text="Room No:", font='Verdana 10 bold')
        Room.place(x=420, y=145)

        Semester = Label(des, text="Semester:",
                         font='Verdana 10 bold')
        Semester.place(x=420, y=180)

        Year = Label(des, text="Year:", font='Verdana 10 bold')
        Year.place(x=420, y=205)

        # Book Docter Entry Box

        room_var = tk.StringVar()
        semester_var = tk.StringVar()
        year = StringVar()

        Room_box = ttk.Combobox(
            des, width=30, textvariable=room_var, state='readonly')
        Room_box['values'] = list(range(1, 200))
        Room_box.current(0)
        Room_box.place(x=500, y=145)

        semester_box = ttk.Combobox(
            des, width=30, textvariable=semester_var, state='readonly')
        semester_box['values'] = ('1', '2', '3', '4')
        semester_box.current(0)
        semester_box.place(x=500, y=180)

        Year = Entry(des, width=30, textvariable=year)
        Year.place(x=500, y=205)

        # button

        btn = Button(des, text="Book", font='Verdana 10 bold',
                     width=20, command=book)
        btn.place(x=503, y=230)
    elif (row2[6] == 1):
        heading = Label(
            des, text="Your have successfully booked a room,", font='Verdana 10 bold')
        heading.place(x=420, y=100)
        heading = Label(
            des, text=" Check for the details at the bottom left of this page", font='Verdana 10 bold')
        heading.place(x=420, y=130)
    else:
        heading = Label(
            des, text="Your have successfully booked a room,", font='Verdana 10 bold')
        heading.place(x=420, y=100)
        heading = Label(
            des, text="Wait for approval from the administrator", font='Verdana 10 bold')
        heading.place(x=420, y=130)

    con = pymysql.connect(host="localhost", user="root",
                              password="new_password", database="room_reservation")
    cur = con.cursor()

    cur.execute(
            "select * from users u left join reservation_requests r on u.id=r.user_student_id where username ='" + user_name.get() + "'")
    rows = cur.fetchall()

        # book Appoitment Details
    heading = Label(des, text=f"Booking Status", font='Verdana 15 bold')
    heading.place(x=20, y=250)

    for book in rows:
        r1 = Label(
            des, text=f"Room number booked: {book[6]}", font='Verdana 10 bold')
        r1.place(x=20, y=300)
        status = book[11]
        print(status)
        if (status == 0):
            r2 = Label(des, text=f"Approval Status: Awaiting approval",
                        font='Verdana 10 bold')
            r2.place(x=20, y=330)
        elif (status == 1):
            r2 = Label(des, text=f"Approval Status: Approved",
                           font='Verdana 10 bold')
            r2.place(x=20, y=330)
        elif (status == None):
            r2 = Label(des, text=f"Approval Status: No booking request made",
                           font='Verdana 10 bold')
            r2.place(x=20, y=330)
        else:
            r2 = Label(des, text=f"Approval Status: Request rejected",
                           font='Verdana 10 bold')
            r2.place(x=20, y=330)


# -----------------------------------------------------End Dashboard Panel -------------------------------------
# ------------------------------------------------------------ Login Window -----------------------------------------
win = Tk()

# app title
win.title("Room Reservation App")

# window size
win.maxsize(width=1000,  height=1000)
win.minsize(width=600,  height=600)


# heading label
heading = Label(win, text="Login", font='Verdana 25 bold')
heading.place(x=80, y=150)

username = Label(win, text="User Name :", font='Verdana 10 bold')
username.place(x=80, y=220)

userpass = Label(win, text="Password :", font='Verdana 10 bold')
userpass.place(x=80, y=260)

# Entry Box
user_name = StringVar()
password = StringVar()

userentry = Entry(win, width=40, textvariable=user_name)
userentry.focus()
userentry.place(x=200, y=223)

passentry = Entry(win, width=40, show="*", textvariable=password)
passentry.place(x=200, y=260)


# button login and clear

btn_login = Button(win, text="Login", font='Verdana 10 bold', command=login)
btn_login.place(x=200, y=293)


btn_login = Button(win, text="Clear", font='Verdana 10 bold', command=clear)
btn_login.place(x=260, y=293)

win.mainloop()

# -------------------------------------------------------------------------- End Login Window ---------------------------------------------------

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

            cur.execute("select * from admin where username=%s and password = %s",
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
                "Error", f"Error User not found : {str(es)}", parent=win)

# ---------------------------------------------------------------End Login Function ---------------------------------

# ---------------------------------------------------- DashBoard Panel -----------------------------------------


def dashboard():
    def approval_btn(valuee):
        con = pymysql.connect(host="localhost", user="root",
                              password="new_password", database="room_reservation")
        cur = con.cursor()

        cur.execute("update reservation_requests SET approval_status=1 where user_student_id=%s ",(valuee))

        for data in cur:
            print(data)

    def reject_btn(valuee):
        con = pymysql.connect(host="localhost", user="root",
                              password="new_password", database="room_reservation")
        cur = con.cursor()

        cur.execute("update reservation_requests SET approval_status=2 where user_student_id=%s ",(valuee))

        for data in cur:
            print(data)
    my_w = tk.Tk()
    my_w.title("Room reservations approval panel")
    my_w.minsize(width=800,  height=500)
    my_w.maxsize(width=1400,  height=700)

    # heading label
    heading = Label(
        my_w, text=f"User Name : {user_name.get()}", font='Verdana 20 bold', bg='green')
    heading.place(x=220, y=20)
    heading1 = Label(
        my_w, text=f"List of bookings", font='Verdana 15 bold', bg='green')
    heading1.place(x=250, y=65)

    f = Frame(my_w, height=1, width=800, bg="green")
    f.place(x=0, y=95)

    con = pymysql.connect(host="localhost", user="root",
                          password="new_password", database="room_reservation")
    cur = con.cursor()

    cur.execute(
        "select * from users u left join reservation_requests r on u.id=r.user_student_id")

    id = Label(my_w, width=10, text='id',
               borderwidth=2, relief='ridge', anchor="w", background="blue")
    id.grid(row=0, column=0)
    id.place(x=0, y=95)
    name = Label(my_w, width=10, text='Name',
                 borderwidth=2, relief='ridge', anchor="w", background="blue")
    name.grid(row=0, column=1)
    name.place(x=83, y=95)
    room = Label(my_w, width=10, text='room',
                 borderwidth=2, relief='ridge', anchor="w", background="blue")
    room.grid(row=0, column=2)
    room.place(x=166, y=95)
    approve = Label(my_w, width=10, text='Approve',
                    borderwidth=2, relief='ridge', anchor="w", background="blue")
    approve.grid(row=0, column=3)
    approve.place(x=250, y=95)
    reject = Label(my_w, width=10, text='Reject',
                   borderwidth=2, relief='ridge', anchor="w", background="blue")
    reject.grid(row=0, column=3)
    reject.place(x=333, y=95)
    approval = Label(my_w, width=20, text='Approval status',
                     borderwidth=2, relief='ridge', anchor="w", background="blue")
    approval.grid(row=0, column=3)
    approval.place(x=420, y=95)
    # a = Frame(des, height=1, width=400, bg="green")
    # a.place(x=0, y=195)

    # b = Frame(des, height=100, width=1, bg="green")
    # b.place(x=400, y=97)
    i = 1
    x = 0
    y = 120
    for data in cur:
        e = Label(my_w, width=10, text=data[5],
                  borderwidth=2, relief='ridge', anchor="center")
        e.grid(row=i)
        e.place(y=y, x=x)
        e1 = Label(my_w, width=10, text=data[1],
                   borderwidth=2, relief='ridge', anchor="center")
        e1.grid(row=i)
        e1.place(y=y, x=83)
        e2 = Label(my_w, width=10, text=data[6],
                   borderwidth=2, relief='ridge', anchor="center")
        e2.grid(row=i)
        e2.place(y=y, x=166)
        btn_approve = Button(my_w, width=10, text=(data[5], "Approve"), font='Verdana 7 bold',
                             command=approval_btn(data[5]), bg="green")
        btn_approve.place(x=250, y=y)
        btn_reject = Button(my_w, width=10, text="Reject",
                            font='Verdana 7 bold', command=reject_btn(data[5]), bg="red")
        btn_reject.place(x=333, y=y)
        approval = data[11]
        if (approval == 0):
            e2 = Label(my_w, width=20, text="Not Approved",
                       borderwidth=2, relief='ridge', anchor="center", bg="blue")
            e2.grid(row=i)
            e2.place(y=y, x=420)
        elif (approval == 1):
            e2 = Label(my_w, width=20, text="Approved",
                       borderwidth=2, relief='ridge', anchor="center", bg="green")
            e2.grid(row=i)
            e2.place(y=y, x=420)
        elif (approval == 2):
            e2 = Label(my_w, width=20, text="Rejected",
                       borderwidth=2, relief='ridge', anchor="center", bg="red")
            e2.grid(row=i)
            e2.place(y=y, x=420)
        i = i+1
        y += 30

    my_w.mainloop()


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

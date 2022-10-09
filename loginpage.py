import flet
import sqlite3
import counter
from flet import (
    ElevatedButton,
    TextField,
)


def main(page):
    # Actual text boxes for user to input US/PW
    usrname = TextField(label="Type your username.")
    psswrd = TextField(label="Type your password.")

    def btn_click(e):
        # These variables hold the string value of what was input into the text fields
        usrstr = usrname.value
        pssstr = psswrd.value
        # Initializing variable which will hold the actual password stored in the DB
        truepass = ''

        #making connection to sqlite db and making query to get password
        connection = sqlite3.connect("course_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT password from Users where username =?", [usrstr])

        # Stores what I believe is a tuple of information gotten from said query
        # Truepass then stores the password via a loop to break it out of the tuple.
        result = cursor.fetchone()
        for i in result:
            truepass = i

        # print statements for testing purposes.
        # print("pssstr is: " + pssstr)
        # print("truepass is: " + str(truepass))

        # This is where the function call will be held to change views upon successful login.
        if truepass == pssstr:
            print("Login successful!")
            page.route = "counter.py"
        else:
            print("Login failed. Check password.")

    page.add(usrname, psswrd, ElevatedButton("Login", on_click=btn_click))


flet.app(target=main)

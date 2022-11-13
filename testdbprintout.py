import sqlite3

def get_prefix(value):
    connection = sqlite3.connect("group_2_db.db")
    cursor = connection.cursor()

    # example of what inserting a task into the DB will look like:
    # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
    # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
    cursor.execute(f"SELECT dept_ID FROM class WHERE course_name=?", [value])
    rows = cursor.fetchall()
    print(rows[0][0])
    connection.close()
    return str(rows[0][0])


def get_coursenum(value):
    connection = sqlite3.connect("group_2_db.db")
    cursor = connection.cursor()

    # example of what inserting a task into the DB will look like:
    # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
    # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
    cursor.execute(f"SELECT course_num FROM class WHERE course_name=?", [value])
    rows = cursor.fetchall()
    print(rows[0][0])
    connection.close()
    return str(rows[0][0])

get_prefix("Malware")

get_coursenum("Malware")

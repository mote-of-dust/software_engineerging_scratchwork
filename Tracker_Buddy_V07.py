import inspect
import sqlite3
import bcrypt
import flet
import re
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
    NavigationRail,
    NavigationRailDestination,
    VerticalDivider,
    Icon,
    icons,
    Container,
    alignment,
    PopupMenuButton,
    PopupMenuItem,
    AppBar,
    FilledButton,
    Dropdown,
    dropdown,
    Tab,
    Tabs,
    Card,
    ListTile,
    padding,
    View,
    view,
    ElevatedButton,
    AlertDialog,
    padding,
    Banner,
    Card,
    Switch,
    AnimatedSwitcher,
    theme,
    Theme,
    border_radius,
    Divider,
    ListView,
    ProgressRing,
    ProgressBar
)

# SHSU colors
shsu_orange = "#f88f00"
shsu_blue = "#333798"

# global login ID
userID = ''
CURRENTCLASS = ''
CURRENTASSIGNMENT = ''
progress_value = 0.5
current_level = 0


def get_courses():  # access the DB and get all the courses and puts them in a list
    courses_list = []

    connection = sqlite3.connect("group_2_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM class")
    results = cursor.fetchall()
    # print(results[2])
    connection.close()

    for result in results:
        print(result[2])
        courses_list.append(str(result[2]))

    return courses_list


def your_courses():  # gets all the courses you are enrolled in and puts them in a list

    your_list = []

    connection = sqlite3.connect("group_2_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_class where user_ID=?", [userID])
    results = cursor.fetchall()
    connection.close()

    for result in results:
        your_list.append(result[4])

    return your_list


# function to get assignments once you click on a class, to populate your assignment page
# not yet implemented as of 11/13/2022. written for v_0.6 by Marc for later use.
def your_assignments():
    your_list = []

    connection = sqlite3.connect("group_2_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT task_name FROM task where user_ID=? AND course_name=?", [userID, CURRENTCLASS])
    results = cursor.fetchall()
    # print(results)
    connection.close()

    for result in results:
        your_list.append(result[0])
    # print(your_list)

    return your_list


def check_email(regular_expression, email):
    if (re.fullmatch(regular_expression, email)):
        return True
    else:
        return False


class SearchCourse(UserControl):

    def build(self):
        self.course_list = get_courses()
        self.your_course_list = [Text("Test")]
        self.return_list = []

        self.search = TextField(
            hint_text="Search for a course",
            border_color=shsu_orange,
            expand=True
        )

        self.confirm_search = FloatingActionButton(
            icon=icons.SEARCH,
            bgcolor=shsu_orange,
            on_click=self.search_clicked
        )

        self.confirm_button = ElevatedButton(
            text="Confirm Course",
            color=colors.WHITE,
            bgcolor=shsu_orange,
            on_click=self.confirm,
        )

        self.clear_button = ElevatedButton(
            text="Clear Search",
            color=colors.WHITE,
            bgcolor=shsu_orange,
            on_click=self.clear,
        )

        self.your_courses_row = Row(
            alignment="center",
            controls=[]
        )

        self.courses = Column(
            width=600,
            alignment="center",
            horizontal_alignment="center",
            scroll="always",
            controls=[
                Row(
                    alignment="center",
                    controls=[
                        self.search,
                        self.confirm_search,
                    ],
                ),
                Column(
                    width=600,
                    alignment="center",
                    controls=[
                    ]
                ),
                Row(
                    alignment="center",
                    controls=[
                        self.confirm_button,
                        self.clear_button,
                    ],
                ),
                Column(
                    width=600,
                    alignment="center",
                    controls=[
                        Text("Your Courses", size=30),
                        Divider(height=10, color=shsu_orange),
                        self.your_courses_row,
                    ]
                ),
            ],
        )

        return self.courses

    def get_description(self, value):
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        # example of what inserting a task into the DB will look like:
        # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
        # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
        cursor.execute(f"SELECT course_descrip FROM class WHERE course_name=?", [value])
        rows = cursor.fetchall()
        connection.close()
        return str(rows[0][0])

    def get_prefix(self, value):
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        # example of what inserting a task into the DB will look like:
        # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
        # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
        cursor.execute(f"SELECT dept_ID FROM class WHERE course_name=?", [value])
        rows = cursor.fetchall()
        print(rows)
        connection.close()
        return str(rows[0][0])

    def get_coursenum(self, value):
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        # example of what inserting a task into the DB will look like:
        # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
        # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
        cursor.execute(f"SELECT course_num FROM class WHERE course_name=?", [value])
        rows = cursor.fetchall()
        print(rows)
        connection.close()
        return str(rows[0][0])

    def search_clicked(self, e):
        if self.search.value in self.course_list:
            self.courses.controls[1].controls.append(
                ListTile(
                    leading=Checkbox(),
                    title=Text(self.search.value),
                    subtitle=Text(self.get_description(self.search.value)),
                )
            )

            self.search.value = ''
            self.confirm_search.bgcolor = "#87817a"
            self.confirm_search.disabled = True
            self.update()

    def confirm(self, e):

        # print(self.courses.controls[1].controls[0].leading.value)
        try:
            if self.courses.controls[1].controls[0].leading.value == True:
                your_course = YourCourse(self.courses.controls[1].controls[0].title.value)
                self.courses.controls[1].controls.pop()

                #                 self.courses.controls[3].controls[2].controls.append(your_course)
                #                 self.your_course_list.append(your_course)

                self.your_course_list.append(your_course)
                self.confirm_search.bgcolor = shsu_orange
                self.confirm_search.disabled = False

                deptID = self.get_prefix(your_course.course_name)
                print(deptID)

                coursenum = self.get_coursenum(your_course.course_name)
                print(coursenum)

                connection = sqlite3.connect("group_2_db.db")
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO user_class(user_ID, dept_ID, course_num, course_name, current_bool, course_level, course_exp) VALUES (:user, :dept_ID, :course_num, :course_name, :current_bool, :course_level, :course_exp)",
                    {'user': userID, 'dept_ID': deptID, 'course_num': coursenum,
                     'course_name': f"{your_course.course_name}", 'current_bool': 1, 'course_level': 1,
                     'course_exp': 0.0}
                )
                connection.commit()
                connection.close()

                #                 self.print_list()

                self.update()
                return True
        except:
            print("Nothing to match with")

    def clear(self, e):
        self.courses.controls[1].controls.pop()
        self.confirm_search.bgcolor = shsu_orange
        self.confirm_search.disabled = False
        self.update()

    def get_signal(self):
        self.update()

    def print_list(self):
        self.test = your_courses()
        return self.test


class YourCourse(UserControl):

    def __init__(self, course_name):  # course_delete
        super().__init__()
        self.course_name = course_name

    #         self.course_delete = course_delete

    def build(self):
        self.course_button = ElevatedButton(
            text=self.course_name,
            color=colors.WHITE,
            bgcolor=shsu_orange,
            on_click=self.course_clicked,
        )

        return self.course_button

    def course_clicked(self, e):
        self.update()


class TrackerBuddy(UserControl):

    def build(self):
        self.assignment_title = TextField(
            hint_text="Assignment Title",
            border_color=shsu_orange,
            expand=True
        )

        self.board = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )

        self.wall = Column(
            width=600,
            alignment="center",
            scroll="always",
            controls=[
                Row(
                    controls=[
                        self.assignment_title,
                        FloatingActionButton(
                            icon=icons.ADD,
                            bgcolor=shsu_orange,
                            on_click=self.add_clicked
                        ),
                    ],
                ),
                self.board,
            ],
        )

        return self.wall

    def add_clicked(self, e):
        if self.assignment_title.value == "":
            return

        assignment = Assignment(
            self.assignment_title.value,
            self.assignment_status_change,
            self.assignment_delete,
            self.assignment_complete,
        )
        class_info = []
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        cursor.execute("SELECT dept_ID, course_num FROM user_class WHERE user_ID=? AND course_name=?",
                       [userID, CURRENTCLASS])
        results = cursor.fetchall()
        for i in results:
            for j in i:
                class_info.append(j)

        print(class_info)
        print(self.assignment_title.value)

        cursor.execute(
            "INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, course_name) VALUES (1, "
            "strftime('%s', 'now'), ?, ?, ?, ?, ?)",
            [userID, class_info[0], class_info[1], self.assignment_title.value, CURRENTCLASS]
        )
        connection.commit()
        connection.close()
        print("current class: " + str(CURRENTCLASS))

        self.board.controls.append(assignment)
        self.assignment_title.value = ""
        self.update()

    def level_update(self):
        levelinfo = []
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT course_level, course_exp FROM user_class WHERE user_ID=? AND course_name=?",
                       [userID, CURRENTCLASS])
        results = cursor.fetchall()

        for i in results:
            for j in i:
                levelinfo.append(j)
        print("Level info is: %d, %f" % (levelinfo[0], levelinfo[1]))
        connection.commit()
        connection.close()
        return levelinfo

    def call_check(self, e):

        tasks = []
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT task_name FROM task WHERE user_ID =? and course_name=? AND date_completed is NULL",
                       [userID, CURRENTCLASS])
        results = cursor.fetchall()
        print(CURRENTCLASS)
        for i in results:
            for j in i:
                tasks.append(j)
        # print(tasks)

        for item in tasks:
            assignment = Assignment(
                item,
                self.assignment_status_change,
                self.assignment_delete,
                self.assignment_complete,
            )
            self.board.controls.append(assignment)
            self.assignment_title.value = ""
            self.update()
            assignment.auto_step(item)
        connection.commit()
        connection.close()
        self.update()

    def assignment_status_change(self, assignment):
        self.update()

    def assignment_delete(self, assignment):
        self.board.controls.remove(assignment)
        self.update()

    def assignment_complete(self, assignment):
        print(assignment.assignment_name)

        levelinfo = []
        self.board.controls.remove(assignment)
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT course_level, course_exp FROM user_class WHERE user_ID=? AND course_name=?",
                       [userID, CURRENTCLASS])
        results = cursor.fetchall()

        for i in results:
            for j in i:
                levelinfo.append(j)

        connection.commit()
        connection.close()

        levelinfo[1] += 0.15
        if levelinfo[1] >= 1.0:
            levelinfo[0] += 1
            levelinfo[1] = levelinfo[1] - 1.0

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        cursor.execute("UPDATE user_class SET course_level =?, course_exp=? WHERE user_ID=? and course_name=?",
                       [levelinfo[0], levelinfo[1], userID, CURRENTCLASS])

        connection.commit()

        cursor.execute("UPDATE task SET date_completed = strftime('%s', 'now') WHERE user_ID=? AND task_name=? and "
                       "course_name=?", [userID, assignment.assignment_name, CURRENTCLASS])
        connection.commit()
        connection.close()

        # logic for adding points goes here

        self.update()

    def tabs_changed(self, e):
        self.update()


class SubTask(UserControl):

    def __init__(self, subtask_name, subtask_delete):
        super().__init__()
        self.subtask_name = subtask_name
        self.subtask_delete = subtask_delete

    def build(self):
        self.counter = 0

        self.display_subtask = Checkbox(
            value=False,
            label=self.subtask_name,
            #             on_change=self.assignment_status
        )

        self.edit_icon = IconButton(
            icon=icons.CREATE_OUTLINED,
            tooltip="Edit To-Do",
            on_click=self.edit_clicked,
        )

        self.delete_icon = IconButton(
            icons.DELETE_OUTLINE,
            icon_color=colors.RED,
            tooltip="Delete To-Do",
            on_click=self.delete_clicked,
        )

        self.edit_title = TextField(expand=1)

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_title,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )

        return Column(
            controls=[
                Row(
                    alignment="spaceBetween",
                    controls=[
                        self.display_subtask,
                        Row(
                            controls=[
                                self.edit_icon,
                                self.delete_icon,
                            ]
                        ),
                    ]
                ),
                self.edit_view,
            ]
        )

    def edit_clicked(self, e):
        self.edit_title.value = self.display_subtask.label
        self.display_subtask.visible = False
        self.edit_icon.visible = False
        self.delete_icon.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_subtask.label = self.edit_title.value
        self.display_subtask.visible = True
        self.edit_icon.visible = True
        self.delete_icon.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.subtask_delete(self)


class Assignment(UserControl):

    def __init__(
            self,
            assignment_name,
            assignment_status,
            assignment_delete,
            assignment_complete
    ):
        super().__init__()
        self.completed = False
        self.assignment_name = assignment_name
        self.assignment_status = assignment_status
        self.assignment_delete = assignment_delete
        self.assignment_complete = assignment_complete

    def build(self):
        self.new_step = TextField(
            hint_text="Add a step",
            border_color=shsu_orange,
            expand=True
        )

        self.edit_icon = IconButton(
            icon=icons.CREATE_OUTLINED,
            tooltip="Edit Assignment",
            on_click=self.edit_clicked,
        )

        self.delete_icon = IconButton(
            icons.DELETE_OUTLINE,
            icon_color=colors.RED,
            tooltip="Delete Assignment",
            on_click=self.delete_clicked,
        )

        self.complete_icon = IconButton(
            icon=icons.DONE_OUTLINE_OUTLINED,
            icon_color=colors.GREEN,
            tooltip="Complete Assignment",
            on_click=self.complete_clicked,
        )

        self.save_icon = IconButton(
            icon=icons.DONE_OUTLINE_OUTLINED,
            icon_color=colors.GREEN,
            visible=False,
            tooltip="Save Change",
            on_click=self.save_clicked,
        )

        self.edit_title = TextField(expand=1)

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_title,
                self.save_icon,
            ],
        )

        self.name = Text(self.assignment_name, size=30)

        self.item = Column()

        self.card = Card(
            content=Container(
                content=Column(
                    [
                        Row(
                            alignment="spaceBetween",
                            controls=[
                                self.name,
                                Row(
                                    controls=[
                                        self.edit_icon,
                                        self.complete_icon,
                                        self.delete_icon,
                                    ]
                                ),
                            ]
                        ),
                        self.edit_view,
                        Divider(height=10, color=shsu_orange),
                        self.item,
                        Row(
                            controls=[
                                self.new_step,
                                FloatingActionButton(
                                    icon=icons.ADD,
                                    bgcolor=shsu_orange,
                                    on_click=self.add_step
                                ),
                            ]
                        ),
                    ],
                ),
                width=600,
                padding=50,
                border_radius=border_radius.all(15),
            )
        )

        return self.card

    def find_taskID(self, e):
        taskID = ''
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT task_ID FROM task WHERE user_ID=? AND task_name=?", [e[1], e[0]])
        results = cursor.fetchall()
        for i in results:
            for j in i:
                taskID = j
                # print(j)
        connection.close()
        return taskID

    def add_step(self, e):
        search_values = []

        subtask = SubTask(self.new_step.value, self.subtask_delete)
        search_values.append(self.assignment_name)
        search_values.append(userID)
        taskID = self.find_taskID(search_values)

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO subtask(user_ID, task_ID, description, completion) VALUES(:user_ID, :task_ID, :description, :completion)",
            {'user_ID': userID, 'task_ID': taskID, 'description': f"{self.new_step.value}", 'completion': 0}
        )
        connection.commit()
        connection.close()
        self.item.controls.append(subtask)
        self.new_step.value = ""
        self.update()

    def auto_comp(self, items):
        for item in items:
            subtask = SubTask(item, self.subtask_delete)
            self.item.controls.append(subtask)
            self.new_step.value = ""
            self.update()

    # testing function to populate subtasks from line 389ish
    def auto_step(self, e):
        print(e)
        your_list = []
        # testclass = Assignment()

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT description FROM subtask where user_ID=? AND task_ID=(SELECT task_ID FROM task WHERE task_name =?)",
            [userID, e])
        results = cursor.fetchall()
        for i in results:
            for j in i:
                subtask = SubTask(j, self.subtask_delete)
                self.item.controls.append(subtask)
                self.new_step.value = ""
                self.update()
                # your_list.append(j)
                # testclass.add_step(j)
                print(j)

        print(your_list)
        connection.close()
        print("You're in!")

    def subtask_delete(self, subtask):
        self.item.controls.remove(subtask)
        self.update()

    def edit_clicked(self, e):
        self.edit_title.value = self.assignment_name
        self.name.visible = False
        self.edit_icon.visible = False
        self.delete_icon.visible = False
        self.complete_icon.visible = False
        self.edit_view.visible = True
        self.save_icon.visible = True
        self.update()

    def save_clicked(self, e):
        self.name.value = self.edit_title.value
        self.name.visible = True
        self.edit_icon.visible = True
        self.complete_icon.visible = True
        self.delete_icon.visible = True
        self.edit_view.visible = False
        self.save_icon.visible = False
        self.update()

    def delete_clicked(self, e):
        self.assignment_delete(self)

    def complete_clicked(self, e):
        self.assignment_complete(self)


# this bit of code I use to check individual things quickly

def main(page: Page):
    page.title = "Tracker Buddy"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#14152b"
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"
    page.auto_scroll = True

    tb = TrackerBuddy()
    course = SearchCourse()

    page.add(tb)


class User(UserControl):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password


class SignUp(UserControl):

    def build(self):
        self.enter_email = TextField(
            hint_text="Username",
            label="Username",
            border_color=shsu_orange,
            expand=True
        )

        self.enter_password = TextField(
            hint_text="Password",
            label="Password",
            border_color=shsu_orange,
            password=True,
            can_reveal_password=True,
            expand=True
        )

        self.signup_page = Column(
            width=600,
            horizontal_alignment="center",
            controls=[
                Text("Sign Up Page", size=40),
                Row(
                    controls=[
                        self.enter_email,
                    ],
                ),
                Row(
                    controls=[
                        self.enter_password,
                    ],
                ),
            ],

        )

        return Column(
            controls=[
                self.signup_page
            ]
        )

    def signup_button(self, e):

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        email = self.enter_email.value
        password = self.enter_password.value

        email_salt = bcrypt.gensalt()
        password_salt = bcrypt.gensalt()

        hashed_email = bcrypt.hashpw(email.encode('utf8'), email_salt)
        hashed_email = hashed_email.decode('utf8')

        hashed_password = bcrypt.hashpw(password.encode('utf8'), password_salt)
        hashed_password = hashed_password.decode('utf8')

        # Believe this needs to select for {hashed_email} not email, to check later.
        cursor.execute(f"SELECT * FROM user WHERE user_name ='{email}'")
        search = cursor.fetchone()

        if search == None:
            search = ("", "")

        valid_email = check_email(email_regex, email)

        if valid_email:
            print("Valid Email")
        else:
            return False

        if email == search[0]:
            print("This email has already been used. Try a different one.")
            return False

        else:
            cursor.execute(
                "INSERT INTO user (user_name, password) VALUES (:user_name, :password)",
                {'user_name': f"{email}", 'password': f"{hashed_password}"}
            )

            connection.commit()
            connection.close()

            print("User Created")
            return True

        self.update()


class Login(UserControl):

    def build(self):
        self.enter_email = TextField(
            hint_text="Username",
            label="Username",
            border_color=shsu_orange,
            expand=True
        )

        self.enter_password = TextField(
            hint_text="Password",
            label="Password",
            border_color=shsu_orange,
            password=True,
            can_reveal_password=True,
            expand=True
        )

        self.login_page = Column(
            width=600,
            horizontal_alignment="center",
            controls=[
                Text("Login Page", size=40),
                Row(
                    controls=[
                        self.enter_email,
                    ],
                ),
                Row(
                    controls=[
                        self.enter_password,
                    ],
                ),
            ],

        )

        return Column(
            controls=[
                self.login_page
            ]
        )

    def login_button(self, e):
        global userID
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        email = self.enter_email.value
        password = self.enter_password.value

        password = password.encode('utf8')

        cursor.execute(f"SELECT * FROM user WHERE user_name ='{email}'")
        search = cursor.fetchone()

        if search == None:
            return False

        hashed = str.encode(search[2])

        if email == search[1] and bcrypt.checkpw(password, hashed):
            print("Match")
            userID = int(search[0])
            print(int(userID))
            connection.close()
            return True
        else:
            print("No Match")
            connection.close()
            return False

        connection.commit()
        connection.close()


def main(page: Page):
    # page theme & settings
    page.title = "Tracker Buddy"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    page.window_resizable = False
    page.window_width = 1000
    page.window_height = 600
    page.scroll = "always"
    page.update()
    # ---------------------

    # theme switch
    sun = icons.LIGHT_MODE_OUTLINED
    moon = icons.MODE_NIGHT_OUTLINED

    def theme_mode(e):
        if theme_button.icon == moon:
            theme_button.icon = sun
            page.theme_mode = "light"
            page.update()

        else:
            theme_button.icon = moon
            page.theme_mode = "dark"
            page.update()

    theme_button = IconButton(
        icon=moon,
        icon_color=colors.WHITE,
        on_click=theme_mode,
    )

    # ---------------------

    # level & progress ring
    # level_display = Text(
    #     value="5",  # display purpose global variable would go here
    #     size=30,
    #     color=shsu_orange,
    # )
    #
    # level_ring = ProgressRing(
    #     value=0.5,
    #     color=shsu_orange,
    #     tooltip="Progress to the next level",
    #     width=20,
    #     height=20,
    #     stroke_width=2
    # )

    def level_up():
        pass  # logic to level up

    # ---------------------

    # appbar theme
    icon = moon
    check_list = Icon(
        icons.ASSIGNMENT,
        color=colors.WHITE,
    )

    def logout(e):
        page.controls.clear()
        page.controls.append(login)
        page.controls.append(login_row)
        courses_row.controls.clear()
        page.update()

    logout_button = IconButton(
        icon=icons.LOGOUT_OUTLINED,
        icon_color=colors.WHITE,
        on_click=logout,
    )

    appbar = page.appbar = AppBar(
        color=colors.WHITE,
        leading=check_list,
        leading_width=40,
        title=Text("Tracker Buddy"),
        center_title=True,
        bgcolor=shsu_blue,
        actions=[theme_button, logout_button]
    )
    # ---------------------

    # classes/pages
    login = Login()
    signup = SignUp()
    searchcourse = SearchCourse()
    tracker = TrackerBuddy()

    # ---------------------

    # banner
    def open_banner(e):
        page.banner.open = True
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    banner = page.banner = Banner(
        bgcolor=shsu_blue,
        leading=Icon(
            icons.WARNING_AMBER_ROUNDED,
            color=colors.WHITE,
            size=40
        ),
        content=Text(
            "Not a valid email. Please, try again.",
            color=colors.WHITE,
            size=20
        ),
        actions=[
            ElevatedButton(
                text="Retry",
                color=colors.WHITE,
                bgcolor=shsu_orange,
                on_click=close_banner
            ),
        ],
    )

    # ---------------------

    # button actions
    def log_in(e):
        verify = login.login_button(e)

        if verify:
            page.controls.remove(login)
            page.controls.remove(login_row)
            create_courses_button(e)
            page.controls.append(searchcourse)
            page.controls.append(courses_row)
            page.controls.append(refresh_list_button)
            page.update()
        else:
            open_banner(e)

    def to_sign_up(e):
        page.controls.remove(login)
        page.controls.remove(login_row)
        page.controls.append(signup)
        page.controls.append(signup_row)
        page.update()

    def sign_up(e):
        verify = signup.signup_button(e)

        if verify:
            page.controls.remove(signup)
            page.controls.remove(signup_row)
            page.controls.append(login)
            page.controls.append(login_row)
            page.update()
        else:
            open_banner(e)

    def to_login(e):
        page.controls.remove(signup)
        page.controls.remove(signup_row)
        page.controls.append(login)
        page.controls.append(login_row)
        page.update()

    def to_assignemnts(e):
        global CURRENTCLASS
        CURRENTCLASS = str(e.control.data)
        print(CURRENTCLASS)

        levelinfo = []
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT course_level, course_exp FROM user_class WHERE user_ID=? AND course_name=?",
                       [userID, CURRENTCLASS])
        results = cursor.fetchall()

        for i in results:
            for j in i:
                levelinfo.append(j)
        connection.commit()
        connection.close()

        page.controls.remove(searchcourse)
        page.controls.remove(courses_row)
        page.controls.remove(refresh_list_button)
        page.controls.append(back_to_courses_button)
        page.controls.append(tracker)
        page.controls.append(refresh_assignments_button)
        # page.controls.append(level_ring)
        # page.controls.append(level_display)
        page.controls.append(progress_card)
        progress_bar.value = levelinfo[1]
        progress_tile.leading = Text(str(levelinfo[0]), size=30)

        page.update()

    # probably useless function, trying to find a way to set a global var
    # via the course_button click within create_courses_button()
    def set_class(course):
        global CURRENTCLASS
        CURRENTCLASS = course
        print(CURRENTCLASS)

    def create_courses_button(e):
        my_courses = searchcourse.print_list()
        for item in my_courses:
            course_name = item
            print('-----------')
            print(course_name)
            course_button = ElevatedButton(
                text=item,
                color=colors.WHITE,
                bgcolor=shsu_orange,
                # on_click=set_class(course_name),
                # on_click=to_assignemnts,
                on_click=to_assignemnts,
                data=item,
            )
            courses_row.controls.append(course_button)
            page.update()

    def refresh_list(e):
        courses_row.controls.clear()
        create_courses_button(e)

    def refresh_assignments(e):
        tracker.call_check(e)

    def to_courses(e):
        #         appbar.title = Text("Tracker Buddy") # this will change the name to the class name
        page.controls.remove(back_to_courses_button)
        page.controls.remove(tracker)
        page.controls.remove(refresh_assignments_button)
        page.controls.remove(progress_card)
        # page.controls.remove(level_ring)
        # page.controls.remove(level_display)
        page.controls.append(searchcourse)
        page.controls.append(courses_row)
        page.controls.append(refresh_list_button)
        page.update()

    # ---------------------

    # buttons
    log_in_button = ElevatedButton(
        text="Log In",
        color=colors.WHITE,
        bgcolor=shsu_orange,
        on_click=log_in,
    )

    make_account_button = ElevatedButton(
        text="Make an Account",
        color=colors.WHITE,
        bgcolor=shsu_orange,
        on_click=to_sign_up,
    )

    sign_up_button = ElevatedButton(
        text="Sign Up",
        color=colors.WHITE,
        bgcolor=shsu_orange,
        on_click=sign_up,
    )

    back_to_login_button = ElevatedButton(
        text="I Have an Account",
        color=colors.WHITE,
        bgcolor=shsu_orange,
        on_click=to_login,
    )

    back_to_courses_button = ElevatedButton(
        text="Back To Courses",
        color=colors.WHITE,
        bgcolor=shsu_orange,
        on_click=to_courses,
    )

    refresh_list_button = FloatingActionButton(
        icon=icons.REFRESH,
        bgcolor=shsu_orange,
        on_click=refresh_list,
    )

    refresh_assignments_button = FloatingActionButton(
        icon=icons.REFRESH,
        bgcolor=shsu_blue,
        on_click=refresh_assignments,
    )

    login_buttons_list = [log_in_button, make_account_button]
    sign_up_buttons_list = [sign_up_button, back_to_login_button]
    # ---------------------

    # rows
    login_row = Row(
        alignment="center",
        controls=login_buttons_list,
    )

    signup_row = Row(
        alignment="center",
        controls=sign_up_buttons_list,
    )

    courses_row = Row(
        alignment="center",
        controls=[],
    )
    # ---------------------

    progress_bar = ProgressBar(
        value=progress_value,
        color=shsu_orange,
        bgcolor=shsu_blue,
        bar_height=10,
        width=1000,
    )

    progress_tile = ListTile(
        leading=Text(str(current_level), size=30),
        title=Text("Level"),
        subtitle=progress_bar,
        dense=True,
    )

    progress_card = Card(
        content=Container(
            width=500,
            content=progress_tile,
            padding=1,
        )
    )

    # Start the machine
    page.add(login, login_row)


flet.app(target=main)  # app

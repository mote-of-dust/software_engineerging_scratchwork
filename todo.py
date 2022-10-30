import sqlite3
import bcrypt
import flet
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
    ListView,
    GridView,
    alignment,
    border,
    border_radius,
    colors
)

unsafe_un = ''


class Assignment(UserControl):
    # db_test()
    # select * from user_task where user_name == name, and class_id == #

    def __init__(self, assignment_name):
        super().__init__()
        self.assignment_name = assignment_name

    def build(self):
        self.new_step = TextField(
            hint_text="Add a step",
            border_color="#622678",
            expand=True
        )

        self.display_assignment = Checkbox(
            value=False,
            label="",
        )

        self.item = Column()
        # self.touch_db()
        self.card = Card(
            content=Container(
                content=Column(
                    [
                        Text(self.assignment_name),
                        self.item,
                        Row(
                            controls=[
                                self.new_step,
                                FloatingActionButton(
                                    icon=icons.ADD,
                                    bgcolor="#622678",
                                    on_click=self.add_step
                                ),
                            ]
                        ),
                    ],
                ),
                width=600,
                padding=50,
                bgcolor="#26284a",
                border_radius=border_radius.all(15),
            )
        )

        return self.card

    def add_step(self, e):
        self.item.controls.append(Checkbox(label=self.new_step.value))
        self.new_step.value = ""
        self.update()


class TrackerBuddy(UserControl):

    def build(self):

        self.assignment_title = TextField(
            hint_text="Assignment Title",
            border_color="#622678",
            expand=True

        )

        self.board = Column()

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
                            bgcolor="#622678",
                            on_click=self.auto_pop),
                    ],
                ),
                self.board,
            ],
        )
        return self.wall

    def touch_db(self):
        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        # example of what inserting a task into the DB will look like:
        # INSERT into task(t_type, date_added, user_ID, dept_ID, course_num, task_name, task_descrip) VALUES (1,
        # strftime('%s', 'now'), 2, "COSC", 3319, "Heap Sort", "build max heap")
        cursor.execute(f"SELECT (task_name) FROM task WHERE user_ID=?", [unsafe_un])
        rows = cursor.fetchall()
        connection.close()
        return rows

    def add_clicked(self, e):

        if self.assignment_title.value == "":
            return

        assignment = Assignment(self.assignment_title.value)

        self.final_pop(assignment)
        # self.board.controls.append(assignment)
        # self.assignment_title.value = ""
        # self.update()

    def final_pop(self, j):
        self.board.controls.append(j)
        self.assignment_title.value = ""
        self.update()

    def auto_pop(self, k):
        populate = self.touch_db()
        print("You have: %d tasks" % len(populate))
        tasknum = 1
        for i in populate:
            for j in i:
                print("Task %d: %s" % (tasknum, j))
                assignment = Assignment(j)
                self.final_pop(assignment)
                tasknum += 1


class User(UserControl):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password


class SignUp(UserControl):

    def build(self):
        self.enter_username = TextField(
            hint_text="Username",
            label="Username",
            border_color="#622678",
            expand=True
        )

        self.enter_password = TextField(
            hint_text="Password",
            label="Password",
            border_color="#622678",
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
                        self.enter_username,
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

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        username = self.enter_username.value
        password = self.enter_password.value

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
        hashed_password = hashed_password.decode('utf8')

        cursor.execute(f"SELECT * FROM user WHERE user_name ='{username}'")
        search = cursor.fetchone()

        if search == None:
            search = ("", "")

        if username == search[1]:
            print("Username already exists. Try a different one.")
            return False

        else:
            cursor.execute(
                "INSERT INTO user (user_name, password) VALUES (:user_name, :password)",
                {'user_name': f"{username}", 'password': f"{hashed_password}"}
            )

            connection.commit()
            connection.close()

            print("User Created")
            return True

        self.update()


class Login(UserControl):

    def build(self):
        self.enter_username = TextField(
            hint_text="Username",
            label="Username",
            border_color="#622678",
            expand=True
        )

        self.enter_password = TextField(
            hint_text="Password",
            label="Password",
            border_color="#622678",
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
                        self.enter_username,
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

        connection = sqlite3.connect("group_2_db.db")
        cursor = connection.cursor()

        username = self.enter_username.value
        password = self.enter_password.value

        password = password.encode('utf8')

        cursor.execute(f"SELECT * FROM user WHERE user_name ='{username}'")
        search = cursor.fetchone()

        if search == None:
            return False

        hashed = str.encode(search[2])

        if username == search[1] and bcrypt.checkpw(password, hashed):
            print("Match")
            user_ID = search[0]
            connection.commit()
            connection.close()
            self.update()
            # Needs to return a tuple, containing (bool, username)
            results = [True, user_ID]
            return results
        else:
            print("No Match")
            connection.commit()
            connection.close()
            self.update()
            return False

        self.update()


def main(page: Page):
    # page theme & settings

    page.title = "Tracker Buddy"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # bg = page.bgcolor = "#7478c2"
    # #     page.bgcolor="#14152b"
    # #     page.platform = "window"
    # page.overlay

    page.window_width = 1000
    page.window_height = 600
    page.scroll = "always"
    page.update()

    sun = Icon(icons.LIGHT_MODE_OUTLINED)
    moon = Icon(icons.MODE_NIGHT_OUTLINED)

    # ---------------------

    # theme switch
    def switch_mode(e):

        if switch.label == "Light Mode":
            # page.bgcolor = "#14152b"
            switch.label = "Dark Mode"
            page.theme_mode = "dark"
            page.update()

        elif switch.label == "Dark Mode":
            # page.bgcolor = "#7478c2"
            switch.label = "Light Mode"
            page.theme_mode = "light"
            page.bgcolor = colors.TRANSPARENT
            page.update()

    switch = Switch(
        label="Dark Mode",
        label_position="left",
        on_change=switch_mode
    )
    # ---------------------

    # appbar theme
    appbar = page.appbar = AppBar(
        leading=Icon(icons.ASSIGNMENT),
        leading_width=40,
        title=Text("Tracker Buddy"),
        center_title=True,
        bgcolor="#26284a",
        actions=[switch]
    )
    # ---------------------

    # classes/pages
    login = Login()
    signup = SignUp()
    tracker = TrackerBuddy()

    # ---------------------

    # Failed to login banner
    def open_banner(e):
        page.banner.open = True
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    banner = page.banner = Banner(
        bgcolor="#450a1f",
        leading=Icon(
            icons.WARNING_AMBER_ROUNDED,
            color=colors.WHITE,
            size=40
        ),
        content=Text(
            "User not found. Please, try again.",
            size=20
        ),
        actions=[
            ElevatedButton(
                text="Retry",
                color=colors.WHITE,
                bgcolor="#2e0313",
                on_click=close_banner
            ),
        ],
    )

    # ---------------------

    # button actions
    def log_in(e):
        verify = login.login_button(e)

        if verify[0] is True:
            global unsafe_un
            # ensuring that verify holds both the results bool, and username
            # print(verify[1])
            unsafe_un = verify[1]

            page.go("/home")
            # tracker.build()
            # tracker.auto_pop()
        else:
            open_banner(e)

    def sign_up(e):
        verify = signup.signup_button(e)

        if verify:
            page.go("/login")
        else:
            open_banner(e)

    # ---------------------

    # buttons
    log_in_button = ElevatedButton(
        text="Log In",
        color=colors.WHITE,
        bgcolor="#622678",
        on_click=log_in,
    )

    make_account_button = ElevatedButton(
        text="Make an Account",
        color=colors.WHITE,
        bgcolor="#622678",
        on_click=lambda _: page.go("/signup")
    )

    sign_up_button = ElevatedButton(
        text="Sign Up",
        color=colors.WHITE,
        bgcolor="#622678",
        on_click=sign_up,
    )

    back_to_login_button = ElevatedButton(
        text="I Have an Account",
        color=colors.WHITE,
        bgcolor="#622678",
        on_click=lambda _: page.go("/login")
    )

    login_buttons_list = [log_in_button, make_account_button]
    sign_up_buttons_list = [sign_up_button, back_to_login_button]

    # ---------------------

    # navigation across app
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/login",
                [
                    appbar,
                    login,
                    Row(
                        alignment="center",
                        controls=login_buttons_list,
                    ),
                ],
                horizontal_alignment="center",
            )
        )

        if page.route == "/signup":
            page.views.append(
                View(
                    "/signup",
                    [
                        appbar,
                        signup,
                        Row(
                            alignment="center",
                            controls=sign_up_buttons_list,
                        ),
                    ],
                    horizontal_alignment="center",

                )
            )

        elif page.route == "/home":
            page.views.append(
                View(
                    "/home",
                    [
                        appbar,
                        tracker,
                    ],
                    horizontal_alignment="center",
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    # ---------------------
    page.add()
    page.theme_mode = "system"
    page.update()


flet.app(target=main)
# flet.app(target=main, view=flet.WEB_BROWSER)

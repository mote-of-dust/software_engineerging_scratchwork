#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Imports


# In[4]:


import flet
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
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
)


# In[5]:


# classes


# In[6]:


class Task(UserControl):
    
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
    
    def build(self):
        self.new_task = TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = Column()

        # application's root control (i.e. "view") containing all other controls
        return Column(
            width=600,
            alignment="center",
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )

    def add_clicked(self, e):
        self.tasks.controls.append(Checkbox(label=self.new_task.value))
        self.new_task.value = ""
        self.update()


# In[7]:


class Course(UserControl):
    
    def build(self):
        self.new_course = FilledButton(text="COSC 3337")
        
        return Column(
            width=600,
            alignment="center",
            controls=[
                Row(
                    controls=[
                        self.new_course,
                    ],
                ),

            ],
        )


# In[179]:


class TrackerBuddy(UserControl):
    
    def build(self):
        self.new_course = TextField(hint_text="Course Name and Number", expand=True)
#         self.new_course = TextField(hint_text="Course Name and Number", expand=True)
#         self.courses = Tabs(
#             tabs=[],
#         )

        self.courses = Column()

#         application's root control (i.e. "view") containing all other controls
        return Column(
            width=600,
            alignment="center",
            controls=[
                Row(
                    controls=[
                        self.new_course,
                        FloatingActionButton(icon=icons.ADD,
                                             bgcolor="#363975",
                                             on_click=self.add_clicked),
                    ],
                ),
                self.courses,
            ],
        )

    def add_clicked(self, e):
        
        if self.new_course.value == "":
            return
        
#         self.courses.tabs.append(Tab(text=self.new_course.value))
#         self.courses.tab_content.append(Checkbox(label=self.new_course.value))
        self.courses.controls.append(Checkbox(label=self.new_course.value))
        self.new_course.value = ""
        self.update()


# In[180]:


# page


# In[181]:


def main(page: Page):
    page.title="Tracker Buddy"
    page.horizontal_alignment="center"
    page.vertical_alignment="center"
    page.bgcolor="#14152b" 
    page.window_width=1000
    page.window_height=600
    page.scroll="auto"
    
#     page.appbar = AppBar(
#         leading=Icon(icons.ASSIGNMENT),
#         leading_width=40,
#         title=Text("Tracker Buddy"),
#         center_title=True,
#         bgcolor="#26284a",
#     )
    
    tb = TrackerBuddy()
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                    leading=Icon(icons.ASSIGNMENT),
                    leading_width=40,
                    title=Text("Tracker Buddy Home"),
                    center_title=True,
                    bgcolor="#26284a",
                    ),
                    tb,
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                View(
                    "/store",
                    [
                        AppBar(
                        leading=Icon(icons.ASSIGNMENT),
                        leading_width=40,
                        title=Text("Tracker Buddy Course"),
                        center_title=True,
                        bgcolor="#26284a",
                        ),
                        ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
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

    tb = TrackerBuddy()
#     page.add(tb)

flet.app(target=main)


# In[ ]:





# In[172]:


def main(page: Page):
    page.title="Tracker Buddy"
    page.horizontal_alignment="center"
    page.vertical_alignment="center"
    page.bgcolor="#14152b" 
    page.window_width=1000
    page.window_height=600
    page.scroll="auto"
    
    page.appbar = AppBar(
        leading=Icon(icons.ASSIGNMENT),
        leading_width=40,
        title=Text("Tracker Buddy"),
        center_title=True,
        bgcolor="#26284a",
    )


    tb = TrackerBuddy()
    page.add(tb)

flet.app(target=main)


# In[ ]:





# In[ ]:


import flet
from flet import Container, Icon, Page, Tab, Tabs, Text, alignment, icons

def main(page: Page):
    track = TrackerBuddy()
    

    t = Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            Tab(
                text="Tab 1",
                content=Container(
                    track,
                ),
            ),
            Tab(
                tab_content=Icon(icons.SEARCH),
                content=Text("This is Tab 2"),
            ),
        ],
        expand=1,
    )

    page.add(t)

flet.app(target=main)


# In[ ]:





# In[ ]:


Row(
            [
                Column([
                    # add application's root control to the page
                    task
                ], 
                    horizontal_alignment="center",
                    expand=True
                ),
            ],
            
            expand=True,
            
        )


# In[154]:


import flet
from flet import AppBar, ElevatedButton, Page, Text, View, colors

def main(page: Page):
    page.title = "Routes Example"
    tb = TrackerBuddy()

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Flet app"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                    tb,
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                View(
                    "/store",
                    [
                        AppBar(title=Text("Store"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
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


flet.app(target=main)


# In[ ]:





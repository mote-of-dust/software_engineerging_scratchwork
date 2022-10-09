#!/usr/bin/env python
# coding: utf-8

# In[7]:


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
)


# In[2]:


import sqlite3


# In[31]:


class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last 
        self.pay = pay
        
    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)
    
    def __repr__(self):
        return "Employee('{}' '{}' '{}')".format(self.first, self.last, self.pay)


# In[55]:


employee_1 = Employee("John", "Dose", 30000)
employee_2 = Employee("Jane", "Dope", 50000)
employee_3 = Employee("Jack", "Dose", 70000)


# In[3]:


class Course:
    
    def __init__(self, name, number):
        self.name = name
        self.number = number
    
    @property
    def name_and_number(self):
        return "{} {}".format(self.name, self.number)
    
    def __repr__(self):
        return "Course('{}' '{}')".format(self.name, self.number)


# In[4]:


course_1 = Course("COSC", 3327)
course_2 = Course("MATH", 3019)
course_3 = Course("BIOL", 4201)
course_4 = Course("HIST", 2052)


# In[ ]:





# In[10]:


connection = sqlite3.connect("course_db.db")
cursor = connection.cursor()

# cursor.execute("""CREATE TABLE courses (
#     name text,
#     number integer
# )
# """)

# cursor.execute("INSERT INTO employees VALUES (:first, :last , :pay)", {'first': employee_3.first,
#                                                                        'last': employee_3.last,
#                                                                        'pay': employee_3.pay})

# cursor.execute("INSERT INTO courses VALUES (:name, :number)", {'name': course_1.name,
#                                                                  'number': course_1.number})
# cursor.execute("INSERT INTO courses VALUES (:name, :number)", {'name': course_2.name,
#                                                                  'number': course_2.number})
# cursor.execute("INSERT INTO courses VALUES (:name, :number)", {'name': course_3.name,
#                                                                  'number': course_3.number})
# cursor.execute("INSERT INTO courses VALUES (:name, :number)", {'name': course_4.name,
#                                                                  'number': course_4.number})

cursor.execute("SELECT * FROM courses")
search = cursor.fetchall()
cursor.execute("SELECT * FROM courses")
# search = cursor.fetchone()


# In[11]:


print(search)


# In[12]:


connection.commit()
connection.close()


# In[ ]:





# In[106]:


def main(page: Page):
    page.title = "Testing database with sqlite3"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    txt = Text(
        "Our flet project getting info from a .db file:", 
        size=40
    )
    
#     db_result = Text(
#         search,
#         size=30
#     )
    
    t = Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            Tab(
                text=(search[0] + str(search[1])),
                content=Container(
                    content=Text("This is Tab 1"), alignment=alignment.center
                ),
            ),
            Tab(
                tab_content=Icon(icons.SEARCH),
                content=Text("This is Tab 2"),
            ),
            Tab(
                text="Tab 3",
                icon=icons.SETTINGS,
                content=Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

flet.app(target=main)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





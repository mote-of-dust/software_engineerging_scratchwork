#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Trying to get it all to work
import time
import flet
from flet import Slider, Text, Container, ElevatedButton, OutlinedButton, Page, colors

def main(page):
    def con_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60 
        hours = minutes // 60
        minutes = minutes % 60
        print("time ", int(hours), int(minutes), int(seconds))
        
    # button actions
    def start_time():
        global stime
        start_time_button = ElevatedButton(
            text="Start",
            color=colors.WHITE,
            bgcolor="#c65e2e",
            on_click=start_time,
        )
        stime = time.time()
        return stime
    
    def end_time():
        global etime
        end_time_button = ElevatedButton(
            text="End",
            color=colors.WHITE,
            bgcolor="#c65e2e",
            on_click=end_time,
        )
        etime = time.time()
        return etime

    end_time()
    start_time()
    timelap = etime - stime
    con_time(timelap)
    
flet.app(target=main)


# In[3]:


# buttons work but trying to figure out the timer part
import flet
from flet import ElevatedButton, Page, Text

def main(page: Page):
    def con_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60 
        hours = minutes // 60
        minutes = minutes % 60
        Text("time ", int(hours), int(minutes), int(seconds))
        
    def start_time(e):
        start_button.stime = time.time()
        print(stime)
        page.update()
        
    def end_time(e):
        end_button.etime = time.time()
        print(etime)
        page.update()

    start_button = ElevatedButton("START", on_click=start_time)
    end_button = ElevatedButton("END", on_click=end_time)
    timelap = etime - stime
    con_time(timelap)

    page.add(start_button, end_button)
flet.app(target=main)


# In[32]:


# Used to get button
import flet
from flet import ElevatedButton, Page, Text

def main(page: Page):
    page.title = "Elevated button with 'click' event"

    def button_clicked(e):
        b.data += 1
        t.value = f"Button clicked {b.data} time(s)"
        page.update()

    b = ElevatedButton("START", on_click=button_clicked, data=0)
    t = Text()

    page.add(b, t)

flet.app(target=main)


# In[53]:


# OG time feature
import time
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

input("Press Enter to start")
start_time = time.time()
print(start_time)

input("Press Enter to stop")
end_time = time.time()
print(end_time)

time_lapsed = end_time - start_time
time_convert(time_lapsed)


# In[ ]:





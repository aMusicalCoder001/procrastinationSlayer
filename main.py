import time

import ctypes, sys

from pywinauto import Application, keyboard
import requests
import os

websites = ["www.youtube.com"]

app = Application(backend="uia")
url = ""

screentime = 1800
free_time_used_today = 0
break_start = time.time()
using_break = False

def main_url(url):
    start = 0
    while url[start:start+4] != ".com" and start < len(url):
        start += 1
    print("www."+url[:start+4])
    return "www."+url[:start+4]

print("OK")
while True:
    try:

        # establish a connection with the current chrome window
        app.connect(title_re=".*Chrome.*")
        element_name = "Address and search bar"
        dlg = app.top_window()
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()

        # if the url is in the list of controlled websites *ahem* and the user hasn't
        # yet surpassed their screentime, let them take their break and keep track
        # of the amount of time they spend
        if main_url(url) in websites and free_time_used_today <= screentime:
            if using_break == False:
                break_start = time.time()
            using_break = True
            free_time_used_today = time.time() - break_start
            print("Free time left:", screentime - free_time_used_today)

        # if they go over their screentime, the moment they try to access their
        # restricted website, the entire chrome window will close without mercy
        elif free_time_used_today >= screentime:
            using_break = False
            print("Oof! Break time for today is up!")
            if main_url(url) in websites:
                app.kill()
        
    except:
        print("OOF")
            
    
    print(url)
    time.sleep(5)
    

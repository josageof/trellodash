  # -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 23:06:09 2022

@author: Josa - josageof@gmail.com

"""

import subprocess
import threading


def run_script(script_name):
    subprocess.run(["python", script_name])


thread1 = threading.Thread(target=run_script, args=("trello_get_data.py",))
thread2 = threading.Thread(target=run_script, args=("trello_data_dash.py",))

thread1.start()
thread2.start()

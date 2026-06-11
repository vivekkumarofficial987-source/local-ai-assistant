from datetime import datetime

import psutil

def system_info():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    }

def get_time():
    return datetime.now().strftime("%H:%M:%S")



def add(a, b):
    return a + b
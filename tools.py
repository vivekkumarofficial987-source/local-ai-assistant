from datetime import datetime

import psutil



import json

def save_profile(key, value):

    try:
        with open("user_profile.json", "r") as file:
            profile = json.load(file)

    except:
        profile = {}

    profile[key] = value

    with open("user_profile.json", "w") as file:
        json.dump(profile, file, indent=4)

    return "Saved"


def get_profile(key):

    try:
        with open("user_profile.json", "r") as file:
            profile = json.load(file)

    except:
        return "No profile found"

    return profile.get(key, "Not found")

def system_info():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    }

def get_time():
    return datetime.now().strftime("%H:%M:%S")



def add(a, b):
    return a + b
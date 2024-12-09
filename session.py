import json
import os

SESSION_FILE = "session.json"

def save_session(data):
    with open(SESSION_FILE, 'w') as session_file:
        json.dump(data, session_file)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as session_file:
            return json.load(session_file)
    else:
        return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
